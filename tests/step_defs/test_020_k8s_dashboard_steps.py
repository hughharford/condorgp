"""Topic E: maintained dashboard, loopback only (feature 020)."""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pytest_bdd import given, scenarios, then, when

from tests.k8s_helpers import (
    Hit,
    find_lines,
    fmt_hits,
    logical_lines,
    repo_files,
    require_text,
    yaml_docs,
)

scenarios("../features/020_k8s_dashboard.feature")

DASHBOARD_MANIFEST = "k8s/11-headlamp.yaml"
VIEWER_MANIFEST = "k8s/12-dashboard-viewer.yaml"
# Things that run. Notes (.md) are checked separately, as they may mention old
# commands.
EXECUTABLE_FILES = {".yaml", ".yml", ".sh", "Makefile"}
SCRIPT_FILES = {".sh", "Makefile"}
LOOPBACK = {"127.0.0.1", "localhost", "::1", "[::1]"}
DASHBOARD_ACCOUNTS = {
    "dashboard-viewer",
    "dashboard-admin",
    "headlamp",
    "kubernetes-dashboard",
}
DASHBOARD_NAMESPACES = {"headlamp", "kubernetes-dashboard"}
BINDINGS = ("RoleBinding", "ClusterRoleBinding")
PRIVILEGED_ROLES = ("cluster-admin", "admin", "edit")
READ_ONLY_VERBS = {"get", "list", "watch"}
HOST_NAMESPACES = ("hostNetwork", "hostPID", "hostIPC")

RETIRED_DASHBOARD = (
    r"kubernetesui/(?:dashboard|metrics-scraper)"
    r"|kubernetes/dashboard/"
    r"|kubernetes-dashboard/kubernetes-dashboard"
    r"|kubernetes\.github\.io/dashboard"
    # the MicroK8s addon installs the retired v2.x dashboard
    r"|microk8s\s+enable\s+dashboard"
    r"|microk8s\s+dashboard-proxy"
)
PORT_FORWARD_OR_PROXY = re.compile(
    r"(?:kubectl|\bk)\s+(?:\S+\s+)*?(?:port-forward|proxy)\b"
)
ROLEBINDING_COMMAND = re.compile(r"kubectl\s+create\s+(?:cluster)?rolebinding")
DASHBOARD_TARGET = re.compile(r"^k(?:_|3_)dash\w*:\s*\n((?:\t.*\n?)+)", re.M)

Doc = dict[str, Any]  # one parsed YAML document
Subject = dict[str, Any]  # one `subjects` entry of a binding
Binding = tuple[
    str, Doc, Subject
]  # (path, binding document, the dashboard subject)


@dataclass
class Dashboard:
    """The parts of the dashboard manifest the checks look at."""

    docs: list[Doc]
    deployment: Doc
    services: list[Doc]

    @property
    def pod(self) -> Doc:
        """The pod spec of the dashboard Deployment."""
        return self.deployment["spec"]["template"]["spec"]

    @property
    def container(self) -> Doc:
        """The dashboard's (only) container."""
        return self.pod["containers"][0]

    @property
    def namespace(self) -> str:
        """The namespace the Deployment lives in."""
        return self.deployment["metadata"]["namespace"]


@dataclass
class Rbac:
    """Return dashboard bindings plus the roles defined in the repo."""

    bindings: list[Binding]
    roles: dict[str, Doc]


def _all_docs(files: list[Path]) -> list[tuple[str, Doc]]:
    """Return (path, document) for every YAML document in the given files."""
    return [
        (str(rel), doc)
        for rel in files
        if rel.suffix in (".yaml", ".yml")
        for doc in yaml_docs(rel)
    ]


def _by_kind(docs: list[Doc], kind: str) -> list[Doc]:
    """Return the documents of the given Kubernetes kind."""
    return [doc for doc in docs if doc.get("kind") == kind]


def _subjects(binding: Doc) -> list[Subject]:
    """Return the ServiceAccount subjects of a binding."""
    return [
        s
        for s in binding.get("subjects") or []
        if s.get("kind") == "ServiceAccount"
    ]


def _is_dashboard_subject(subject: Subject) -> bool:
    """Return True if the subject is one of the dashboard's accounts."""
    return (
        subject.get("name") in DASHBOARD_ACCOUNTS
        or subject.get("namespace") in DASHBOARD_NAMESPACES
    )


def _is_comment(command: str) -> bool:
    """Return True if a shell line is only a comment."""
    return command.lstrip().startswith("#")


# ---------------------------------------------------------------- scenario 1


@when(
    "I search the manifests and scripts for the retired Kubernetes Dashboard",
    target_fixture="hits",
)
def search_retired_dashboard(files: list[Path]) -> list[Hit]:
    """Find any reference to the retired v2.x dashboard in files that run."""
    return find_lines(files, RETIRED_DASHBOARD, suffixes=EXECUTABLE_FILES)


@then("it is not installed anywhere")
def not_installed(hits: list[Hit]) -> None:
    """Fail, listing every reference to the retired dashboard."""
    assert not hits, (
        "The retired Kubernetes Dashboard (v2.x) is still referenced:\n"
        + fmt_hits(hits)
    )


# ---------------------------------------------------------------- manifest
# scenarios


@given("the dashboard manifest", target_fixture="dash")
def dashboard_manifest() -> Dashboard:
    """Load the dashboard manifest, which must hold exactly one Deployment."""
    docs = yaml_docs(DASHBOARD_MANIFEST)
    assert docs, f"{DASHBOARD_MANIFEST} is missing or is not valid YAML"
    deployments = _by_kind(docs, "Deployment")
    assert (
        len(deployments) == 1
    ), "expected exactly one Deployment (the dashboard)"
    return Dashboard(
        docs=docs,
        deployment=deployments[0],
        services=_by_kind(docs, "Service"),
    )


@then("its image has an explicit version tag and is not latest")
def image_pinned(dash: Dashboard) -> None:
    """Require a version tag other than latest, or a digest."""
    image = dash.container["image"]
    name = image.split("/")[-1]
    has_digest = "@sha256:" in image
    tag = name.split(":", 1)[1] if ":" in name else ""
    assert has_digest or (
        tag and tag != "latest"
    ), f"image '{image}' is not pinned to a version"


@then(
    "the container runs non-root, without privilege escalation "
    "or capabilities, "
    "on a read-only filesystem with the default seccomp profile"
)
def container_hardened(dash: Dashboard) -> None:
    """Require the standard container hardening settings."""
    sc = dash.container.get("securityContext") or {}
    pod_sc = dash.pod.get("securityContext") or {}
    problems: list[str] = []
    if (
        sc.get("runAsNonRoot") is not True
        and pod_sc.get("runAsNonRoot") is not True
    ):
        problems.append("runAsNonRoot is not true")
    if sc.get("allowPrivilegeEscalation") is not False:
        problems.append("allowPrivilegeEscalation is not false")
    if sc.get("privileged") is True:
        problems.append("container is privileged")
    if sc.get("readOnlyRootFilesystem") is not True:
        problems.append("readOnlyRootFilesystem is not true")
    if "ALL" not in ((sc.get("capabilities") or {}).get("drop") or []):
        problems.append("capabilities are not dropped (drop: [ALL])")
    seccomp = (
        sc.get("seccompProfile") or pod_sc.get("seccompProfile") or {}
    ).get("type")
    if seccomp != "RuntimeDefault":
        problems.append(f"seccompProfile is {seccomp!r}, not RuntimeDefault")
    assert not problems, "; ".join(problems)


@then("it has CPU and memory limits and mounts no host path")
def limits_and_no_hostpath(dash: Dashboard) -> None:
    """Require CPU and memory limits and no access to the host."""
    limits = (dash.container.get("resources") or {}).get("limits") or {}
    assert {"cpu", "memory"} <= set(limits), f"limits are {limits}"
    host_paths = [
        vol["name"] for vol in dash.pod.get("volumes", []) if "hostPath" in vol
    ]
    assert not host_paths, f"host paths mounted: {host_paths}"
    for flag in HOST_NAMESPACES:
        assert not dash.pod.get(flag), f"{flag} is enabled"


def _ingresses_exposing(service_names: set[str]) -> list[str]:
    """Return Ingress manifests that route to any of the Services."""
    exposed: list[str] = []
    for rel, doc in _all_docs(repo_files()):
        if doc.get("kind") != "Ingress":
            continue
        for rule in (doc.get("spec") or {}).get("rules") or []:
            for path in (rule.get("http") or {}).get("paths") or []:
                if path["backend"]["service"]["name"] in service_names:
                    exposed.append(rel)
    return exposed


@then(
    "its Service is ClusterIP and nothing in the manifests "
    "exposes it through an Ingress"
)
def only_inside_cluster(dash: Dashboard) -> None:
    """Require a ClusterIP Service that no Ingress routes to."""
    assert dash.services, "the dashboard has no Service"
    for service in dash.services:
        service_type = service["spec"].get("type", "ClusterIP")
        assert service_type == "ClusterIP", f"Service type is {service_type}"
    exposed = _ingresses_exposing(
        {service["metadata"]["name"] for service in dash.services}
    )
    assert not exposed, f"Ingress objects expose the dashboard: {exposed}"


@then("no binding anywhere grants anything to the dashboard's service account")
def pod_account_has_no_permissions(dash: Dashboard) -> None:
    """Require that the pod's own account has no RBAC bindings at all."""
    account = dash.pod["serviceAccountName"]
    granted: list[str] = []
    for rel, doc in _all_docs(repo_files()):
        if doc.get("kind") not in BINDINGS:
            continue
        for subject in _subjects(doc):
            same_account = subject.get("name") == account
            same_namespace = subject.get("namespace") in (None, dash.namespace)
            if same_account and same_namespace:
                granted.append(
                    f"{rel}: {doc['metadata']['name']} -> "
                    f"{doc['roleRef']['name']}"
                )
    assert (
        not granted
    ), "the dashboard pod's own account has permissions:\n  " + "\n  ".join(
        granted
    )


@then(
    "the Service selects the Deployment's pods and targets "
    "its named container port"
)
def service_wired(dash: Dashboard) -> None:
    """Service selector and targetPort must match the Deployment."""
    labels = dash.deployment["spec"]["template"]["metadata"]["labels"]
    assert (
        dash.deployment["spec"]["selector"]["matchLabels"].items()
        <= labels.items()
    )
    ports = {
        port.get("name"): port["containerPort"]
        for port in dash.container.get("ports", [])
    }
    for service in dash.services:
        selector = service["spec"]["selector"]
        assert (
            selector.items() <= labels.items()
        ), "Service selector does not match the pods"
        for port in service["spec"]["ports"]:
            target = port["targetPort"]
            assert (
                target in ports or target in ports.values()
            ), f"targetPort {target!r} is not a container port {ports}"
    account = dash.pod["serviceAccountName"]
    defined = {
        doc["metadata"]["name"]
        for doc in _by_kind(dash.docs, "ServiceAccount")
    }
    assert (
        account in defined
    ), f"ServiceAccount '{account}' is not defined in the manifest"


@then("the viewer account lives in the dashboard's namespace")
def viewer_in_namespace(dash: Dashboard) -> None:
    """Require the viewer account and its subjects to share a namespace."""
    docs = yaml_docs(VIEWER_MANIFEST)
    assert docs, f"{VIEWER_MANIFEST} is missing or is not valid YAML"
    viewers = [
        doc
        for doc in _by_kind(docs, "ServiceAccount")
        if doc["metadata"]["name"] == "dashboard-viewer"
    ]
    assert (
        viewers and viewers[0]["metadata"]["namespace"] == dash.namespace
    ), f"dashboard-viewer is not in '{dash.namespace}'"
    for binding in (doc for doc in docs if doc.get("kind") in BINDINGS):
        for subject in _subjects(binding):
            assert subject.get("namespace") == dash.namespace, (
                f"{binding['metadata']['name']} points at namespace "
                f"{subject.get('namespace')!r}"
            )


# ---------------------------------------------------------------- RBAC
# scenarios


@when(
    "I read every RBAC object that mentions a dashboard account",
    target_fixture="rbac",
)
def read_rbac(files: list[Path]) -> Rbac:
    """Collect every dashboard binding and every role in the repo."""
    docs = _all_docs(files)
    bindings: list[Binding] = [
        (rel, doc, subject)
        for rel, doc in docs
        if doc.get("kind") in BINDINGS
        for subject in _subjects(doc)
        if _is_dashboard_subject(subject)
    ]
    roles = {
        doc["metadata"]["name"]: doc
        for _, doc in docs
        if doc.get("kind") in ("ClusterRole", "Role")
    }
    return Rbac(bindings=bindings, roles=roles)


@then("no dashboard account is bound to cluster-admin, admin or edit")
def not_privileged(rbac: Rbac) -> None:
    """Fail if any dashboard account is bound to a write-capable role."""
    bad = [
        f"{rel}: {doc['metadata']['name']} binds {subject['name']} "
        f"to {doc['roleRef']['name']}"
        for rel, doc, subject in rbac.bindings
        if doc["roleRef"]["name"] in PRIVILEGED_ROLES
    ]
    assert not bad, "\n".join(bad)


@then("the viewer account is bound to the built-in view role")
def viewer_is_view(rbac: Rbac) -> None:
    """Require a binding that gives dashboard-viewer the built-in view role."""
    assert any(
        subject["name"] == "dashboard-viewer"
        and doc["roleRef"]["name"] == "view"
        for _, doc, subject in rbac.bindings
    ), "no binding gives dashboard-viewer the built-in 'view' role"


@then("every extra rule it has is get, list or watch and none touches Secrets")
def extras_are_read_only(rbac: Rbac) -> None:
    """Any extra role bound to the viewer must be read-only, no Secrets."""
    problems: list[str] = []
    for _, doc, subject in rbac.bindings:
        role_name = doc["roleRef"]["name"]
        if subject["name"] != "dashboard-viewer" or role_name == "view":
            continue
        role = rbac.roles.get(role_name)
        if role is None:
            problems.append(
                f"{role_name}: role is not defined in the repo, "
                "cannot be checked"
            )
            continue
        for rule in role.get("rules") or []:
            if not set(rule.get("verbs") or []) <= READ_ONLY_VERBS:
                problems.append(f"{role_name}: verbs {rule.get('verbs')}")
            if {"secrets", "*"} & set(rule.get("resources") or []):
                problems.append(
                    f"{role_name}: resources {rule.get('resources')}"
                )
    assert not problems, "\n".join(problems)


@when(
    "I read every kubectl command that creates a role binding",
    target_fixture="binding_commands",
)
def read_binding_commands(files: list[Path]) -> list[Hit]:
    """Find every script command that creates a (cluster) role binding."""
    return [
        hit
        for hit in logical_lines(files, SCRIPT_FILES)
        if ROLEBINDING_COMMAND.search(hit[2]) and not _is_comment(hit[2])
    ]


@then("none of them binds cluster-admin")
def none_bind_admin(binding_commands: list[Hit]) -> None:
    """Fail if any script grants cluster-admin."""
    bad = [hit for hit in binding_commands if "cluster-admin" in hit[2]]
    assert not bad, "scripts create a cluster-admin binding:\n" + fmt_hits(bad)


# ---------------------------------------------------------------- address
# scenarios


@when(
    "I read every kubectl port-forward and kubectl proxy command",
    target_fixture="forwards",
)
def read_port_forwards(files: list[Path]) -> list[Hit]:
    """Find every kubectl port-forward and proxy command."""
    return [
        hit
        for hit in logical_lines(files)
        if PORT_FORWARD_OR_PROXY.search(hit[2]) and not _is_comment(hit[2])
    ]


@then("none binds an address other than 127.0.0.1, localhost or ::1")
def forwards_on_loopback(forwards: list[Hit]) -> None:
    """Fail if any --address option is not a loopback address."""
    bad: list[Hit] = []
    for rel, number, command in forwards:
        for match in re.finditer(r"--address(?:\s+|=)(\S+)", command):
            if not set(match.group(1).strip("'\"").split(",")) <= LOOPBACK:
                bad.append((rel, number, command))
    assert (
        not bad
    ), "port-forward is exposed beyond this machine:\n" + fmt_hits(bad)


# ---------------------------------------------------------------- Makefile
# target


@when(
    "I read the dashboard commands in the Makefile", target_fixture="makefile"
)
def read_makefile(files: list[Path]) -> str:
    """Load the Makefile."""
    return require_text("Makefile")


@then(
    "the dashboard target port-forwards the headlamp service "
    "and logs in with a short-lived token"
)
def dashboard_target(makefile: str) -> None:
    """Require a target that mints a short-lived token for Headlamp."""
    recipe = DASHBOARD_TARGET.search(makefile)
    assert recipe, "no dashboard target (k_dash or k3_dash) in the Makefile"
    body = recipe.group(1)
    assert re.search(
        r"-n\s+headlamp\s+create\s+token\s+dashboard-viewer", body
    ), body
    assert re.search(r"port-forward\s+service/headlamp\s+4466:80", body), body
    assert "dashboard-proxy" not in body
