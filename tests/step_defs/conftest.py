"""Shared pytest configuration for the cluster-security BDD tests (topics A-G).

Each topic's feature carries a tag, which pytest-bdd turns into a marker, so one topic
can be run on its own:  python -m pytest -m A_secrets   (or B_tokens, D_postgres_init, ...)
"""

from pathlib import Path

import pytest
from pytest_bdd import given

from tests.k8s_helpers import repo_files

_TOPIC_MARKERS = {
    "A_secrets": "A: cluster secrets are encrypted in the repo",
    "B_tokens": "B: kubeadm / k3s join tokens are never committed",
    "D_postgres_init": "D: Postgres init script is delivered by ConfigMap and works",
    "E_dashboard": "E: maintained dashboard, read-only login, loopback-only addresses",
    "F_ufw": "F: ufw rules are limited to the cluster's own nodes",
    "G_kubeconfig": "G: k3s kubeconfig is written with mode 600",
}


def pytest_configure(config: pytest.Config) -> None:
    """Register one marker per topic so `-m A_secrets` etc. work without warnings."""
    for name, text in _TOPIC_MARKERS.items():
        config.addinivalue_line("markers", f"{name}: {text}")


@given("the repository files", target_fixture="files")
def repository_files() -> list[Path]:
    """Every repo file the checks should look at (see tests.k8s_helpers.repo_files)."""
    return repo_files()
