"""Topic G: the k3s kubeconfig is written with mode 600 (feature 022)."""

import re
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from pytest_bdd import given, scenarios, then, when

from tests.k8s_helpers import (
    Hit,
    assert_all_checks_fail,
    assert_scan_skips,
    find_lines_in_text,
    fmt_hits,
    read_text,
    require_text,
)

scenarios("../features/022_k3s_kubeconfig_mode.feature")

SERVER_CONFIG = "k3s/config.server.example.yaml"
GUIDE = "kubernetes/k3s_again/k3s_hub_spoke.md"
CANARY_CONFIG = "tests/test_data/k8s/canary-k3s-config-bad.example.yaml"
CANARY_INSTALL = "tests/test_data/k8s/canary-k3s-install-bad.example.sh"
CANARY_GUIDE = "tests/test_data/k8s/canary-k3s-guide-bad.example.md"

# CLI flag (--write-kubeconfig-mode 644 / =644), YAML key (write-kubeconfig-
# mode: "0644"),
# env var (K3S_KUBECONFIG_MODE=644).
SETTING = re.compile(
    r"(?:write-kubeconfig-mode|K3S_KUBECONFIG_MODE)"
    r"""(?:\s*[:=]\s*|\s+)["']?([0-9]+)""",
    re.I,
)
MENTION = r"(?i)write-kubeconfig-mode|K3S_KUBECONFIG_MODE"
GOOD_MODES = {"600", "0600"}
# A line in prose saying "never use --write-kubeconfig-mode 644" is advice, not
# a setting.
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


def _mode_hits_in_text(rel: str, text: str) -> list[ModeHit]:
    """Return lines of one text naming the kubeconfig mode, and its mode."""
    hits: list[ModeHit] = []
    for _, number, line in find_lines_in_text(rel, text, MENTION):
        if rel.endswith(".md") and ADVICE.search(line):
            continue
        match = SETTING.search(line)
        hits.append((rel, number, line, match.group(1) if match else None))
    return hits


def _mode_hits(files: list[Path]) -> list[ModeHit]:
    """Return lines naming the kubeconfig mode, with the mode they set."""
    hits: list[ModeHit] = []
    for rel in files:
        text = read_text(rel)
        if text is not None:
            hits += _mode_hits_in_text(str(rel), text)
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
        (path, number, line)
        for path, number, line, mode in settings
        if mode not in GOOD_MODES
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
        'config must contain: write-kubeconfig-mode: "0600" '
        "(quoted, so YAML keeps it a string)"
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
    """Require the guide to show a 0600 file and warn against 644."""
    missing = [phrase for phrase in GUIDE_MUST_MENTION if phrase not in guide]
    assert not missing, f"guide is missing: {missing}"
    assert WARNING_AGAINST_644.search(guide), "guide must warn against 644"


# ---------------------------------------------------------------- canary


@dataclass
class Canary:
    """The three kinds of input the kubeconfig checks look at."""

    config: str  # the k3s server config
    install: str  # an install command
    guide: str  # the hub-and-spoke notes


def _canary_checks(canary: Canary) -> dict[str, Callable[[], None]]:
    """Return every kubeconfig check, ready to run on the canary."""
    return {
        "every config setting is 600 or 0600": lambda: each_is_600(
            _mode_hits_in_text(CANARY_CONFIG, canary.config)
        ),
        "every install setting is 600 or 0600": lambda: each_is_600(
            _mode_hits_in_text(CANARY_INSTALL, canary.install)
        ),
        "every guide setting is 600 or 0600": lambda: each_is_600(
            _mode_hits_in_text(CANARY_GUIDE, canary.guide)
        ),
        'the config sets "0600"': lambda: sets_0600(canary.config),
        "the config has no other value": lambda: has_no_other_value(
            canary.config
        ),
        "the guide explains 0600 and warns against 644": lambda: (
            explains_0600(canary.guide)
        ),
    }


def _load_canary() -> Canary:
    """Load the three canary files, failing clearly if any is gone."""
    return Canary(
        config=require_text(CANARY_CONFIG),
        install=require_text(CANARY_INSTALL),
        guide=require_text(CANARY_GUIDE),
    )


def _assert_canary_still_bad(canary: Canary) -> None:
    """Fail unless every check still rejects the canary, for real reasons.

    An empty or broken file fails every check too, so first require that
    each file still talks about the kubeconfig mode: a failing check must
    mean a defect, not a missing file.
    """
    for rel, text in (
        (CANARY_CONFIG, canary.config),
        (CANARY_INSTALL, canary.install),
        (CANARY_GUIDE, canary.guide),
    ):
        assert _mode_hits_in_text(
            rel, text
        ), f"{rel} no longer mentions the kubeconfig mode at all"
    assert_all_checks_fail(
        _canary_checks(canary),
        f"{CANARY_CONFIG}, {CANARY_INSTALL} and {CANARY_GUIDE}",
    )


@given(
    "the bad k3s config, install command and guide kept in the test data",
    target_fixture="canary",
)
def bad_k3s_canary() -> Canary:
    """Load the canary config, install command and guide."""
    return _load_canary()


@then("they say plainly that they are fake, deliberately bad examples")
def canary_is_marked_fake() -> None:
    """Check every canary file announces that it is fake and must stay bad."""
    for rel in (CANARY_CONFIG, CANARY_INSTALL, CANARY_GUIDE):
        text = require_text(rel)
        assert "CANARY" in text and "FAKE" in text, (
            f"{rel} must say it is a fake, deliberately bad example "
            "(CANARY, FAKE) so nobody mistakes it for a real file"
        )


@then("every kubeconfig check fails on them")
def every_check_fails_on_canary(canary: Canary) -> None:
    """Check every kubeconfig check rejects the canary."""
    _assert_canary_still_bad(canary)


@when("I fix or empty a copy of the canary", target_fixture="sanitised_copies")
def sanitise_canary_copies(canary: Canary) -> dict[str, Canary]:
    """Make copies of the canary that someone has 'fixed'."""
    real_config = require_text(SERVER_CONFIG)
    real_guide = require_text(GUIDE)
    clean_install = (
        "curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 600\n"
    )
    return {
        "the real files": Canary(real_config, clean_install, real_guide),
        "config fixed": Canary(real_config, canary.install, canary.guide),
        "install fixed": Canary(canary.config, clean_install, canary.guide),
        "guide fixed": Canary(canary.config, canary.install, real_guide),
        "emptied": Canary("", "", ""),
    }


@then("the canary guard rejects that copy")
def canary_guard_rejects(
    canary: Canary, sanitised_copies: dict[str, Canary]
) -> None:
    """Check the guard rejects every fixed copy and accepts the real canary."""
    _assert_canary_still_bad(canary)  # the real canary passes the guard
    accepted: list[str] = []
    for name, copied in sanitised_copies.items():
        try:
            _assert_canary_still_bad(copied)
        except AssertionError:
            continue  # rejected, as it should be
        accepted.append(name)
    assert (
        not accepted
    ), f"the canary guard wrongly accepted these good copies: {accepted}"


@then("the repository scan skips all three")
def scan_skips_canaries() -> None:
    """Check the real scan never reads tests/, or the canary would fail it."""
    for rel in (CANARY_CONFIG, CANARY_INSTALL, CANARY_GUIDE):
        assert_scan_skips(rel)
