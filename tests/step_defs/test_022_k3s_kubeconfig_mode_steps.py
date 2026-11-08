import re

from pytest_bdd import scenarios, when, then

from tests.k8s_helpers import find_lines, fmt_hits, read_text

scenarios("../features/022_k3s_kubeconfig_mode.feature")

SERVER_CONFIG = "k3s/config.server.example.yaml"
GUIDE = "kubernetes/k3s_again/k3s_hub_spoke.md"

# CLI flag (--write-kubeconfig-mode 644 / =644), YAML key (write-kubeconfig-mode: "0644"),
# env var (K3S_KUBECONFIG_MODE=644).
SETTING = re.compile(
    r"""(?:write-kubeconfig-mode|K3S_KUBECONFIG_MODE)(?:\s*[:=]\s*|\s+)["']?([0-9]+)""", re.I
)
GOOD_MODES = {"600", "0600"}
# A line in prose saying "never use --write-kubeconfig-mode 644" is advice, not a setting.
ADVICE = re.compile(r"(?i)\b(never|do not|don't|avoid|instead of|not)\b")


def _mode_hits(files):
    hits = []
    for rel, number, line in find_lines(files, r"(?i)write-kubeconfig-mode|K3S_KUBECONFIG_MODE"):
        if rel.endswith(".md") and ADVICE.search(line):
            continue
        m = SETTING.search(line)
        hits.append((rel, number, line, m.group(1) if m else None))
    return hits


# ---------------------------------------------------------------- scenario 1


@when("I read every write-kubeconfig-mode setting", target_fixture="settings")
def read_settings(files):
    return _mode_hits(files)


@then("each one is 600 or 0600")
def each_600(settings):
    bad = [(r, n, l) for r, n, l, mode in settings if mode not in GOOD_MODES]
    assert not bad, "kubeconfig mode other than 600:\n" + fmt_hits(bad)


# ---------------------------------------------------------------- scenario 2


@when("I read the k3s server config example", target_fixture="config")
def read_config(files):
    text = read_text(SERVER_CONFIG)
    assert text is not None, f"{SERVER_CONFIG} does not exist"
    return text


@then('it sets write-kubeconfig-mode to "0600"')
def sets_0600(config):
    assert re.search(r'^write-kubeconfig-mode:\s*"0600"\s*$', config, re.M), \
        'config must contain: write-kubeconfig-mode: "0600" (quoted, so YAML keeps it a string)'


@then("it does not set it anywhere else to a different value")
def no_other_value(config):
    values = SETTING.findall(config)
    assert values and all(v in GOOD_MODES for v in values), values


# ---------------------------------------------------------------- scenario 3


@when("I read the k3s hub-and-spoke guide", target_fixture="guide")
def read_guide(files):
    text = read_text(GUIDE)
    assert text is not None, f"{GUIDE} does not exist"
    return text


@then("it explains how to use a 0600 kubeconfig and why 644 must not be used")
def explains(guide):
    missing = [w for w in ("0600", "644", "sudo k3s kubectl", "KUBECONFIG", "/etc/rancher/k3s/k3s.yaml") if w not in guide]
    assert not missing, f"guide is missing: {missing}"
    assert re.search(r"(?i)(never|do not|don't).{0,60}644", guide), "guide must warn against 644"
