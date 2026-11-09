"""Topic G: the k3s kubeconfig is written with mode 600 (feature 022)."""

import re
from pathlib import Path

from pytest_bdd import scenarios, then, when

from tests.k8s_helpers import Hit, find_lines, fmt_hits, require_text

scenarios("../features/022_k3s_kubeconfig_mode.feature")

SERVER_CONFIG = "k3s/config.server.example.yaml"
GUIDE = "kubernetes/k3s_again/k3s_hub_spoke.md"

# CLI flag (--write-kubeconfig-mode 644 / =644), YAML key (write-kubeconfig-mode: "0644"),
# env var (K3S_KUBECONFIG_MODE=644).
SETTING = re.compile(
    r"""(?:write-kubeconfig-mode|K3S_KUBECONFIG_MODE)(?:\s*[:=]\s*|\s+)["']?([0-9]+)""", re.I
)
MENTION = r"(?i)write-kubeconfig-mode|K3S_KUBECONFIG_MODE"
GOOD_MODES = {"600", "0600"}
# A line in prose saying "never use --write-kubeconfig-mode 644" is advice, not a setting.
ADVICE = re.compile(r"(?i)\b(never|do not|don't|avoid|instead of|not)\b")
GUIDE_MUST_MENTION = (
    "0600",
    "644",
    "sudo k3s kubectl",
    "KUBECONFIG",
    "/etc/rancher/k3s/k3s.yaml",
)
WARNING_AGAINST_644 = re.compile(r"(?i)(never|do not|don't).{0,60}644")

# (path, line number, line text, the mode found on that line or None)
ModeHit = tuple[str, int, str, str | None]


def _mode_hits(files: list[Path]) -> list[ModeHit]:
    """Every line that mentions the kubeconfig mode, with the mode it sets (if any)."""
    hits: list[ModeHit] = []
    for rel, number, line in find_lines(files, MENTION):
        if rel.endswith(".md") and ADVICE.search(line):
            continue
        match = SETTING.search(line)
        hits.append((rel, number, line, match.group(1) if match else None))
    return hits


# ---------------------------------------------------------------- scenario 1


@when("I read every write-kubeconfig-mode setting", target_fixture="settings")
def read_settings(files: list[Path]) -> list[ModeHit]:
    """Collect every kubeconfig-mode setting in the repo."""
    return _mode_hits(files)


@then("each one is 600 or 0600")
def each_is_600(settings: list[ModeHit]) -> None:
    """Fail on any setting that is not 600 or 0600."""
    bad: list[Hit] = [
        (path, number, line) for path, number, line, mode in settings if mode not in GOOD_MODES
    ]
    assert not bad, "kubeconfig mode other than 600:\n" + fmt_hits(bad)


# ---------------------------------------------------------------- scenario 2


@when("I read the k3s server config example", target_fixture="config")
def read_config(files: list[Path]) -> str:
    """Load the example hub config."""
    return require_text(SERVER_CONFIG)


@then('it sets write-kubeconfig-mode to "0600"')
def sets_0600(config: str) -> None:
    """Require the quoted string "0600", so YAML cannot read it as a number."""
    assert re.search(r'^write-kubeconfig-mode:\s*"0600"\s*$', config, re.M), (
        'config must contain: write-kubeconfig-mode: "0600" ' "(quoted, so YAML keeps it a string)"
    )


@then("it does not set it anywhere else to a different value")
def has_no_other_value(config: str) -> None:
    """Every mode mentioned in the config must be an accepted one."""
    values = SETTING.findall(config)
    assert values and all(value in GOOD_MODES for value in values), values


# ---------------------------------------------------------------- scenario 3


@when("I read the k3s hub-and-spoke guide", target_fixture="guide")
def read_guide(files: list[Path]) -> str:
    """Load the hub-and-spoke guide."""
    return require_text(GUIDE)


@then("it explains how to use a 0600 kubeconfig and why 644 must not be used")
def explains_0600(guide: str) -> None:
    """Require the guide to show kubectl use with a 0600 file and to warn against 644."""
    missing = [phrase for phrase in GUIDE_MUST_MENTION if phrase not in guide]
    assert not missing, f"guide is missing: {missing}"
    assert WARNING_AGAINST_644.search(guide), "guide must warn against 644"
