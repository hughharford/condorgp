import json
import os
import shutil
import subprocess
import time
import warnings
from pathlib import Path

import pytest
import requests
import urllib3
from pytest_bdd import given, parsers, scenario, then, when

from condorgp.params import Params

K3D_PARAMS = Params().get_params("k3d_dict")
K3D_CLUSTER_NAME = K3D_PARAMS["K3D_CLUSTER_NAME"]
KUBECONFIG_FILE = K3D_PARAMS["KUBECONFIG_FILE"]
KUBECONFIG_CONTEXT = K3D_PARAMS["KUBECONFIG_CONTEXT"]
CONDORGP_NAMESPACES = K3D_PARAMS["CONDORGP_NAMESPACES"]
K8S_DASHBOARD_NAMESPACE = K3D_PARAMS["K8S_DASHBOARD_NAMESPACE"]
K8S_DASHBOARD_DEPLOYMENT = K3D_PARAMS["K8S_DASHBOARD_DEPLOYMENT"]
K8S_DASHBOARD_SERVICE = K3D_PARAMS["K8S_DASHBOARD_SERVICE"]
K3D_DASHBOARD_MANIFEST = K3D_PARAMS["K3D_DASHBOARD_MANIFEST"]
K3D_DASH_KUBECONFIG_SCRIPT = K3D_PARAMS["K3D_DASH_KUBECONFIG_SCRIPT"]
K8S_DASHBOARD_URL = K3D_PARAMS["K8S_DASHBOARD_URL"]

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# =============================================================================
# Scenario registrations — order matches tests/features/015_k3d_start.feature
# =============================================================================


@scenario(
    "../features/015_k3d_start.feature",
    "Cluster starts from a stopped state",
)
def test_cluster_starts_from_a_stopped_state():
    pass


@scenario(
    "../features/015_k3d_start.feature",
    "Cluster starts and becomes ready",
)
def test_cluster_starts_and_becomes_ready():
    pass


@scenario(
    "../features/015_k3d_start.feature",
    "Kubernetes dashboard is up and available",
)
def test_kubernetes_dashboard_is_up_and_available():
    pass


@scenario(
    "../features/015_k3d_start.feature",
    "Core services report ready status",
)
def test_core_services_report_ready_status():
    pass


# =============================================================================
# Shared: pytest fixture and helpers (used by all scenarios)
# =============================================================================


def _ensure_kubeconfig_dir(kubeconfig_file):
    kubeconfig_dir = os.path.dirname(kubeconfig_file)
    if kubeconfig_dir:
        os.makedirs(kubeconfig_dir, mode=0o700, exist_ok=True)


def _merge_k3d_into_kubeconfig(cluster_name, kubeconfig_file):
    _ensure_kubeconfig_dir(kubeconfig_file)
    _run(
        [
            "k3d",
            "kubeconfig",
            "merge",
            cluster_name,
            "-o",
            kubeconfig_file,
        ]
    )


@pytest.fixture
def k3d_context():
    if shutil.which("k3d") is None:
        pytest.skip("k3d binary is not available on this host")
    if shutil.which("kubectl") is None:
        pytest.skip("kubectl binary is not available on this host")
    cluster_name = K3D_CLUSTER_NAME
    kubeconfig_file = KUBECONFIG_FILE

    _merge_k3d_into_kubeconfig(cluster_name, kubeconfig_file)

    yield {
        "cluster_name": cluster_name,
        "kubeconfig_file": kubeconfig_file,
        "kubeconfig_context": KUBECONFIG_CONTEXT,
    }


def _run(command, env=None):
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
        env=env,
    )
    if completed.returncode != 0:
        raise AssertionError(
            f"Command failed: {' '.join(command)}\n"
            f"stdout:\n{completed.stdout}\n"
            f"stderr:\n{completed.stderr}"
        )
    return completed.stdout


def _run_kubectl(args, kubeconfig_file, context):
    env = os.environ.copy()
    env["KUBECONFIG"] = kubeconfig_file
    return _run(
        ["kubectl", "--context", context, *args],
        env=env,
    )


def _cluster_running(cluster_name):
    output = _run(["k3d", "cluster", "list", "-o", "json"])
    clusters = json.loads(output)
    for cluster in clusters:
        if cluster.get("name") == cluster_name:
            servers_running = cluster.get("serversRunning", 0)
            agents_running = cluster.get("agentsRunning", 0)
            return (servers_running + agents_running) > 0
    return False


# =============================================================================
# Step implementations grouped by scenario (015_k3d_start.feature)
#
# Each block lists the exact Given / When / Then lines for that scenario.
# Step functions are registered globally in pytest-bdd: when the same phrase
# appears in another scenario, the same function runs (no duplicate defs).
# =============================================================================


# -----------------------------------------------------------------------------
# Scenario: Cluster starts from a stopped state
#
#   Given k3d installs are in place and cluster is not started
#   When the cluster is started
#   Then the cluster status is healthy
#   And all CondorGP namespaces are available
# -----------------------------------------------------------------------------


@given("k3d installs are in place and cluster is not started")
def given_k3d_installs_and_cluster_not_started(k3d_context):
    cluster_name = k3d_context["cluster_name"]
    if _cluster_running(cluster_name):
        _run(["k3d", "cluster", "stop", cluster_name])
    assert not _cluster_running(cluster_name), f"{cluster_name} should be stopped"


@when("the cluster is started")
def when_cluster_is_started(k3d_context):
    cluster_name = k3d_context["cluster_name"]
    if not _cluster_running(cluster_name):
        _run(["k3d", "cluster", "start", cluster_name])


@then("the cluster status is healthy")
def then_cluster_status_is_healthy(k3d_context):
    cluster_name = k3d_context["cluster_name"]
    assert _cluster_running(cluster_name), f"{cluster_name} is not running"
    nodes = _run_kubectl(
        ["get", "nodes", "-o", "name"],
        k3d_context["kubeconfig_file"],
        k3d_context["kubeconfig_context"],
    )
    assert nodes.strip(), "kubectl returned no nodes for the cluster"


@then("all CondorGP namespaces are available")
def then_condorgp_namespaces_available(k3d_context):
    namespaces_json = _run_kubectl(
        ["get", "namespaces", "-o", "json"],
        k3d_context["kubeconfig_file"],
        k3d_context["kubeconfig_context"],
    )
    namespaces = {
        item["metadata"]["name"] for item in json.loads(namespaces_json)["items"]
    }
    for namespace in CONDORGP_NAMESPACES:
        assert namespace in namespaces, f"Missing namespace: {namespace}"


# -----------------------------------------------------------------------------
# Scenario: Cluster starts and becomes ready
#
#   Given the initial k3d setup
#   When the cluster is started          → see "Cluster starts from a stopped state"
#   Then the cluster status is healthy   → (shared)
#   And all CondorGP namespaces are available → (shared)
# -----------------------------------------------------------------------------


@given("the initial k3d setup")
def given_initial_k3d_setup(k3d_context):
    assert k3d_context["cluster_name"] == K3D_CLUSTER_NAME


# -----------------------------------------------------------------------------
# Scenario: Kubernetes dashboard is up and available
#
#   Given the k3d cluster has settled
#   When the kubernetes dashboard is deployed from repo manifests
#   Then the kubernetes dashboard deployment is ready
#   And the kubernetes dashboard service has ready endpoints
#   And the kubernetes dashboard is available at the configured URL
#         (K8S_DASHBOARD_URL; runs k8s/k3d/dash_kubeconfig.sh if nothing listens)
# -----------------------------------------------------------------------------


@given("the k3d cluster has settled")
def given_k3d_cluster_has_settled(k3d_context):
    cluster_name = k3d_context["cluster_name"]
    if not _cluster_running(cluster_name):
        _run(["k3d", "cluster", "start", cluster_name])
    _run_kubectl(
        ["wait", "--for=condition=Ready", "nodes", "--all", "--timeout=180s"],
        k3d_context["kubeconfig_file"],
        k3d_context["kubeconfig_context"],
    )


@when("the kubernetes dashboard is deployed from repo manifests")
def when_kubernetes_dashboard_deployed_from_repo(k3d_context):
    _run_kubectl(
        ["apply", "-f", K3D_DASHBOARD_MANIFEST],
        k3d_context["kubeconfig_file"],
        k3d_context["kubeconfig_context"],
    )


@then("the kubernetes dashboard deployment is ready")
def then_kubernetes_dashboard_deployment_ready(k3d_context):
    _run_kubectl(
        [
            "rollout",
            "status",
            f"deployment/{K8S_DASHBOARD_DEPLOYMENT}",
            "-n",
            K8S_DASHBOARD_NAMESPACE,
            "--timeout=180s",
        ],
        k3d_context["kubeconfig_file"],
        k3d_context["kubeconfig_context"],
    )


@then("the kubernetes dashboard service has ready endpoints")
def then_kubernetes_dashboard_service_has_ready_endpoints(k3d_context):
    endpoints_json = _run_kubectl(
        [
            "get",
            "endpoints",
            K8S_DASHBOARD_SERVICE,
            "-n",
            K8S_DASHBOARD_NAMESPACE,
            "-o",
            "json",
        ],
        k3d_context["kubeconfig_file"],
        k3d_context["kubeconfig_context"],
    )
    endpoints = json.loads(endpoints_json)
    subsets = endpoints.get("subsets") or []
    has_address = any(
        subset.get("addresses") for subset in subsets
    )
    assert has_address, "kubernetes-dashboard service has no endpoint addresses yet"


def _dashboard_http_responds(url):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", urllib3.exceptions.InsecureRequestWarning)
        try:
            response = requests.get(url, verify=False, timeout=8)
            return response.status_code in (200, 301, 302, 303, 307, 308)
        except requests.RequestException:
            return False


def _dash_kubeconfig_script_path():
    script = Path(K3D_DASH_KUBECONFIG_SCRIPT)
    if not script.is_file():
        script = Path(__file__).resolve().parents[2] / "k8s/k3d/dash_kubeconfig.sh"
    return script.resolve()


@then("the kubernetes dashboard is available at the configured URL")
def then_kubernetes_dashboard_available_at_configured_url():
    url = K8S_DASHBOARD_URL
    if _dashboard_http_responds(url):
        return
    dash_script = _dash_kubeconfig_script_path()
    if not dash_script.is_file():
        raise AssertionError(f"Missing dashboard script: {dash_script}")
    repo_root = dash_script.parent.parent.parent
    proc = subprocess.Popen(
        ["bash", str(dash_script)],
        cwd=str(repo_root),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        for _ in range(60):
            if proc.poll() is not None:
                err = (proc.stderr.read() or "").strip()
                raise AssertionError(
                    f"dash_kubeconfig.sh exited before dashboard was reachable: {err}"
                )
            if _dashboard_http_responds(url):
                return
            time.sleep(1)
        raise AssertionError(
            f"Dashboard did not respond at {url} after dash_kubeconfig.sh (see k8s/k3d/dash_kubeconfig.sh)"
        )
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()


# -----------------------------------------------------------------------------
# Scenario Outline: Core services report ready status
#
#   Given the k3d cluster has settled    → see "Kubernetes dashboard..." block
#   Then deployment "<deployment>" reports ready
# -----------------------------------------------------------------------------


@then(parsers.parse('deployment "{deployment}" reports ready'))
def then_deployment_reports_ready(k3d_context, deployment):
    _run_kubectl(
        [
            "rollout",
            "status",
            f"deployment/{deployment}",
            "-n",
            CONDORGP_NAMESPACES[0],
            "--timeout=180s",
        ],
        k3d_context["kubeconfig_file"],
        k3d_context["kubeconfig_context"],
    )
