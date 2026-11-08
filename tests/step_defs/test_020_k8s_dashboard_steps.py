import re

import pytest
from pytest_bdd import scenarios, given, when, then

from tests.k8s_helpers import find_lines, fmt_hits, logical_lines, read_text, repo_files, yaml_docs

scenarios("../features/020_k8s_dashboard.feature")

DASHBOARD_MANIFEST = "k8s/11-headlamp.yaml"
VIEWER_MANIFEST = "k8s/12-dashboard-viewer.yaml"
EXECUTABLE_FILES = {".yaml", ".yml", ".sh", "Makefile"}  # things that run; notes are checked separately
SCRIPT_FILES = {".sh", "Makefile"}
LOOPBACK = {"127.0.0.1", "localhost", "::1", "[::1]"}
DASHBOARD_ACCOUNTS = {"dashboard-viewer", "dashboard-admin", "headlamp", "kubernetes-dashboard"}
DASHBOARD_NAMESPACES = {"headlamp", "kubernetes-dashboard"}
BINDINGS = ("RoleBinding", "ClusterRoleBinding")


def _all_docs(files):
    return [(str(rel), doc) for rel in files if rel.suffix in (".yaml", ".yml") for doc in yaml_docs(rel)]


def _by_kind(docs, kind):
    return [d for d in docs if d.get("kind") == kind]


def _subjects(binding):
    return [s for s in binding.get("subjects") or [] if s.get("kind") == "ServiceAccount"]


def _is_dashboard_subject(subject):
    return subject.get("name") in DASHBOARD_ACCOUNTS or subject.get("namespace") in DASHBOARD_NAMESPACES


# ---------------------------------------------------------------- scenario 1


@when("I search the manifests and scripts for the retired Kubernetes Dashboard", target_fixture="hits")
def search_retired_dashboard(files):
    pattern = (
        r"kubernetesui/(?:dashboard|metrics-scraper)"
        r"|kubernetes/dashboard/"
        r"|kubernetes-dashboard/kubernetes-dashboard"
        r"|kubernetes\.github\.io/dashboard"
        r"|microk8s\s+enable\s+dashboard"  # the MicroK8s addon installs the retired v2.x dashboard
        r"|microk8s\s+dashboard-proxy"
    )
    return find_lines(files, pattern, suffixes=EXECUTABLE_FILES)


@then("it is not installed anywhere")
def not_installed(hits):
    assert not hits, "The retired Kubernetes Dashboard (v2.x) is still referenced:\n" + fmt_hits(hits)


# ---------------------------------------------------------------- manifest scenarios


@given("the dashboard manifest", target_fixture="dash")
def dashboard_manifest():
    docs = yaml_docs(DASHBOARD_MANIFEST)
    assert docs, f"{DASHBOARD_MANIFEST} is missing or is not valid YAML"
    deployments = _by_kind(docs, "Deployment")
    assert len(deployments) == 1, "expected exactly one Deployment (the dashboard)"
    return {
        "docs": docs,
        "deployment": deployments[0],
        "pod": deployments[0]["spec"]["template"]["spec"],
        "container": deployments[0]["spec"]["template"]["spec"]["containers"][0],
        "services": _by_kind(docs, "Service"),
    }


@then("its image has an explicit version tag and is not latest")
def image_pinned(dash):
    image = dash["container"]["image"]
    name = image.split("/")[-1]
    has_digest = "@sha256:" in image
    tag = name.split(":", 1)[1] if ":" in name else ""
    assert has_digest or (tag and tag != "latest"), f"image '{image}' is not pinned to a version"


@then("the container runs non-root, without privilege escalation or capabilities, on a read-only filesystem with the default seccomp profile")
def container_hardened(dash):
    sc = dash["container"].get("securityContext") or {}
    pod_sc = dash["pod"].get("securityContext") or {}
    problems = []
    if sc.get("runAsNonRoot") is not True and pod_sc.get("runAsNonRoot") is not True:
        problems.append("runAsNonRoot is not true")
    if sc.get("allowPrivilegeEscalation") is not False:
        problems.append("allowPrivilegeEscalation is not false")
    if sc.get("privileged") is True:
        problems.append("container is privileged")
    if sc.get("readOnlyRootFilesystem") is not True:
        problems.append("readOnlyRootFilesystem is not true")
    if "ALL" not in ((sc.get("capabilities") or {}).get("drop") or []):
        problems.append("capabilities are not dropped (drop: [ALL])")
    seccomp = (sc.get("seccompProfile") or pod_sc.get("seccompProfile") or {}).get("type")
    if seccomp != "RuntimeDefault":
        problems.append(f"seccompProfile is {seccomp!r}, not RuntimeDefault")
    assert not problems, "; ".join(problems)


@then("it has CPU and memory limits and mounts no host path")
def limits_and_no_hostpath(dash):
    limits = (dash["container"].get("resources") or {}).get("limits") or {}
    assert {"cpu", "memory"} <= set(limits), f"limits are {limits}"
    pod = dash["pod"]
    host = [v["name"] for v in pod.get("volumes", []) if "hostPath" in v]
    assert not host, f"host paths mounted: {host}"
    for flag in ("hostNetwork", "hostPID", "hostIPC"):
        assert not pod.get(flag), f"{flag} is enabled"


@then("its Service is ClusterIP and nothing in the manifests exposes it through an Ingress")
def only_inside_cluster(dash):
    files = repo_files()
    assert dash["services"], "the dashboard has no Service"
    for service in dash["services"]:
        assert service["spec"].get("type", "ClusterIP") == "ClusterIP", f"Service type is {service['spec'].get('type')}"
    names = {s["metadata"]["name"] for s in dash["services"]}
    exposed = []
    for rel, doc in _all_docs(files):
        if doc.get("kind") != "Ingress":
            continue
        for rule in (doc.get("spec") or {}).get("rules") or []:
            for path in (rule.get("http") or {}).get("paths") or []:
                if path["backend"]["service"]["name"] in names:
                    exposed.append(rel)
    assert not exposed, f"Ingress objects expose the dashboard: {exposed}"


@then("no binding anywhere grants anything to the dashboard's service account")
def pod_account_has_no_permissions(dash):
    files = repo_files()
    account = dash["pod"]["serviceAccountName"]
    granted = []
    for rel, doc in _all_docs(files):
        if doc.get("kind") in BINDINGS:
            if any(s.get("name") == account and s.get("namespace") in (None, dash["deployment"]["metadata"]["namespace"])
                   for s in _subjects(doc)):
                granted.append(f"{rel}: {doc['metadata']['name']} -> {doc['roleRef']['name']}")
    assert not granted, "the dashboard pod's own account has permissions:\n  " + "\n  ".join(granted)


@then("the Service selects the Deployment's pods and targets its named container port")
def service_wired(dash):
    labels = dash["deployment"]["spec"]["template"]["metadata"]["labels"]
    assert dash["deployment"]["spec"]["selector"]["matchLabels"].items() <= labels.items()
    ports = {p.get("name"): p["containerPort"] for p in dash["container"].get("ports", [])}
    for service in dash["services"]:
        assert service["spec"]["selector"].items() <= labels.items(), "Service selector does not match the pods"
        for port in service["spec"]["ports"]:
            target = port["targetPort"]
            assert target in ports or target in ports.values(), f"targetPort {target!r} is not a container port {ports}"
    account = dash["pod"]["serviceAccountName"]
    assert any(d["metadata"]["name"] == account for d in _by_kind(dash["docs"], "ServiceAccount")), (
        f"ServiceAccount '{account}' is not defined in the manifest"
    )


@then("the viewer account lives in the dashboard's namespace")
def viewer_in_namespace(dash):
    namespace = dash["deployment"]["metadata"]["namespace"]
    docs = yaml_docs(VIEWER_MANIFEST)
    assert docs, f"{VIEWER_MANIFEST} is missing or is not valid YAML"
    viewer = [d for d in _by_kind(docs, "ServiceAccount") if d["metadata"]["name"] == "dashboard-viewer"]
    assert viewer and viewer[0]["metadata"]["namespace"] == namespace, f"dashboard-viewer is not in '{namespace}'"
    for binding in (d for d in docs if d.get("kind") in BINDINGS):
        for subject in _subjects(binding):
            assert subject.get("namespace") == namespace, f"{binding['metadata']['name']} points at namespace {subject.get('namespace')!r}"


# ---------------------------------------------------------------- RBAC scenarios


@when("I read every RBAC object that mentions a dashboard account", target_fixture="rbac")
def read_rbac(files):
    docs = _all_docs(files)
    bindings = []
    for rel, doc in docs:
        if doc.get("kind") in BINDINGS:
            for subject in _subjects(doc):
                if _is_dashboard_subject(subject):
                    bindings.append((rel, doc, subject))
    roles = {d["metadata"]["name"]: d for _, d in docs if d.get("kind") in ("ClusterRole", "Role")}
    return {"bindings": bindings, "roles": roles}


@then("no dashboard account is bound to cluster-admin, admin or edit")
def not_privileged(rbac):
    bad = [f"{rel}: {doc['metadata']['name']} binds {subject['name']} to {doc['roleRef']['name']}"
           for rel, doc, subject in rbac["bindings"] if doc["roleRef"]["name"] in ("cluster-admin", "admin", "edit")]
    assert not bad, "\n".join(bad)


@then("the viewer account is bound to the built-in view role")
def viewer_is_view(rbac):
    assert any(s["name"] == "dashboard-viewer" and d["roleRef"]["name"] == "view" for _, d, s in rbac["bindings"]), (
        "no binding gives dashboard-viewer the built-in 'view' role"
    )


@then("every extra rule it has is get, list or watch and none touches Secrets")
def extras_are_read_only(rbac):
    problems = []
    for rel, doc, subject in rbac["bindings"]:
        role_name = doc["roleRef"]["name"]
        if subject["name"] != "dashboard-viewer" or role_name == "view":
            continue
        role = rbac["roles"].get(role_name)
        if role is None:
            problems.append(f"{role_name}: role is not defined in the repo, cannot be checked")
            continue
        for rule in role.get("rules") or []:
            if not set(rule.get("verbs") or []) <= {"get", "list", "watch"}:
                problems.append(f"{role_name}: verbs {rule.get('verbs')}")
            if {"secrets", "*"} & set(rule.get("resources") or []):
                problems.append(f"{role_name}: resources {rule.get('resources')}")
    assert not problems, "\n".join(problems)


@when("I read every kubectl command that creates a role binding", target_fixture="binding_commands")
def read_binding_commands(files):
    return [c for c in logical_lines(files, SCRIPT_FILES)
            if re.search(r"kubectl\s+create\s+(?:cluster)?rolebinding", c[2]) and not c[2].lstrip().startswith("#")]


@then("none of them binds cluster-admin")
def none_bind_admin(binding_commands):
    bad = [c for c in binding_commands if "cluster-admin" in c[2]]
    assert not bad, "scripts create a cluster-admin binding:\n" + fmt_hits(bad)


# ---------------------------------------------------------------- address scenarios


def _port_forwards(files):
    commands = []
    for rel, number, command in logical_lines(files):
        if re.search(r"(?:kubectl|\bk)\s+(?:\S+\s+)*?(?:port-forward|proxy)\b", command) and not command.lstrip().startswith("#"):
            commands.append((rel, number, command))
    return commands


@when("I read every kubectl port-forward and kubectl proxy command", target_fixture="forwards")
def read_port_forwards(files):
    return _port_forwards(files)


@then("none binds an address other than 127.0.0.1, localhost or ::1")
def forwards_on_loopback(forwards):
    bad = []
    for rel, number, command in forwards:
        for match in re.finditer(r"--address(?:\s+|=)(\S+)", command):
            if not set(match.group(1).strip("'\"").split(",")) <= LOOPBACK:
                bad.append((rel, number, command))
    assert not bad, "port-forward is exposed beyond this machine:\n" + fmt_hits(bad)


# ---------------------------------------------------------------- Makefile target


@when("I read the dashboard commands in the Makefile", target_fixture="makefile")
def read_makefile(files):
    text = read_text("Makefile")
    assert text is not None, "Makefile is missing"
    return text


@then("the dashboard target port-forwards the headlamp service and logs in with a short-lived token")
def dashboard_target(makefile):
    recipe = re.search(r"^k(?:_|3_)dash\w*:\s*\n((?:\t.*\n?)+)", makefile, re.M)
    assert recipe, "no dashboard target (k_dash or k3_dash) in the Makefile"
    body = recipe.group(1)
    assert re.search(r"-n\s+headlamp\s+create\s+token\s+dashboard-viewer", body), body
    assert re.search(r"port-forward\s+service/headlamp\s+4466:80", body), body
    assert "dashboard-proxy" not in body
