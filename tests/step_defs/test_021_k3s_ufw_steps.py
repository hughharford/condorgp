import os
import re
import stat

import pytest
from pytest_bdd import scenarios, given, when, then

from tests.k8s_helpers import REPO_ROOT, find_lines, fmt_hits, run

scenarios("../features/021_k3s_ufw.feature")

SCRIPT = REPO_ROOT / "k3s/ufw_rules.sh"

ADMIN = "203.0.113.10"
HUB = "198.51.100.1"
SPOKE_1 = "198.51.100.2"
SPOKE_2 = "198.51.100.3"
CLUSTER_CIDRS = {"10.42.0.0/16", "10.43.0.0/16"}  # k3s default pod + service networks
WORLD = {"any", "anywhere", "0.0.0.0", "0.0.0.0/0", "::/0", "::"}

# Ports the script is allowed to open, and nothing else (k3s docs, "Inbound rules").
API = "6443"
WIREGUARD = {"51820", "51821"}
KUBELET = "10250"
VXLAN = "8472"

UFW_OPEN = re.compile(r"\bufw\s+(?:allow|limit)\b")
FROM_SRC = re.compile(r"\bfrom\s+(\S+)")
RULE_FROM = re.compile(r"^ufw (allow|limit) from (\S+) to any(?: port (\d+) proto (tcp|udp))?$")


def rules(stdout) -> list:
    """The `ufw ...` lines the script printed, in order."""
    return [line.strip() for line in stdout.splitlines() if line.startswith("ufw ")]


def env(**extra) -> dict:
    env = {"PATH": os.environ["PATH"], "HOME": os.environ.get("HOME", "/tmp")}
    env.update(extra)
    return env


def run_script(env, extra_path=None) -> None:
    assert SCRIPT.is_file(), f"{SCRIPT.relative_to(REPO_ROOT)} does not exist"
    if extra_path:
        env["PATH"] = f"{extra_path}:{env['PATH']}"
    return run(["bash", str(SCRIPT)], env=env, cwd=str(REPO_ROOT))


def parsed(rules) -> list:
    """Each allow rule as (source, port, proto); anything unparseable fails the test."""
    out = []
    for rule in rules:
        if rule.startswith(("ufw default", "ufw --force enable")):
            continue
        m = RULE_FROM.match(rule)
        assert m, f"rule is not a 'from <source> to any [port <n> proto <p>]' rule: {rule!r}"
        source, port, proto = m.group(2), m.group(3), m.group(4)
        if port is None:  # portless rule: only the k3s pod/service networks may have one
            assert source in CLUSTER_CIDRS, f"portless rule for a non-cluster source: {rule!r}"
            continue
        out.append((source, port, proto))
    return out


def by_source(rules) -> dict:
    result = {}
    for source, port, proto in _parsed(rules):
        result.setdefault(source, set()).add((port, proto))
    return result


# ---------------------------------------------------------------- scenario 1


@when("I read every ufw allow or limit rule", target_fixture="open_rules")
def read_ufw_rules(files) -> list:
    bad = []
    for hit in find_lines(files, UFW_OPEN.pattern):
        src = FROM_SRC.search(hit[2])
        value = src.group(1).strip("\"'") if src else None
        if value is None or value.lower() in WORLD:
            bad.append(hit)
    return bad


@then("each one is limited to a source address")
def all_limited(open_rules) -> None:
    assert not open_rules, "ufw rules that open a port to every source:\n" + fmt_hits(open_rules)


# ---------------------------------------------------------------- scenarios 2-4


@given("the firewall script")
def firewall_script() -> None:
    assert SCRIPT.is_file(), f"{SCRIPT.relative_to(REPO_ROOT)} does not exist"


@when("I generate the rules for a hub with two spokes", target_fixture="out")
def hub_rules() -> None:
    res = _run_script(_env(ROLE="hub", ADMIN_IP=ADMIN, NODE_IPS=f"{SPOKE_1} {SPOKE_2}"))
    assert res.returncode == 0, res.stderr
    return res.stdout


@when("I generate the rules for a spoke with a hub and one other spoke", target_fixture="out")
def spoke_rules() -> None:
    res = _run_script(_env(ROLE="spoke", ADMIN_IP=ADMIN, NODE_IPS=f"{HUB} {SPOKE_2}"))
    assert res.returncode == 0, res.stderr
    return res.stdout


@then("SSH is allowed from the admin address only")
def ssh_admin_only(out) -> None:
    ssh = [(s, p, pr) for s, p, pr in _parsed(_rules(out)) if p == "22"]
    assert ssh == [(ADMIN, "22", "tcp")], f"SSH rules: {ssh}"


@then("the API port is allowed from the admin and each node only")
def api_hub(out) -> None:
    sources = {s for s, p, pr in _parsed(_rules(out)) if p == API}
    assert sources == {ADMIN, SPOKE_1, SPOKE_2}, f"6443 allowed from: {sources}"


@then("the API port is not opened")
def api_spoke(out) -> None:
    assert [r for r in _rules(out) if API in r.split()] == []


@then("WireGuard and kubelet ports are allowed from each node only")
def node_ports(out) -> None:
    by_source = _by_source(_rules(out))
    peers = {s for s in by_source if s not in {ADMIN} | CLUSTER_CIDRS}
    assert peers, "no node rules at all"
    for peer in peers:
        ports = {p for p, _ in by_source[peer]}
        assert KUBELET in ports and WIREGUARD <= ports, f"{peer} gets {sorted(ports)}"
    # the admin gets SSH (+ the API on a hub), never node-to-node traffic
    admin_ports = {p for p, _ in by_source.get(ADMIN, set())}
    assert not admin_ports & (WIREGUARD | {KUBELET}), f"admin was given node ports: {admin_ports}"


@then("nothing else is opened, and in particular not the Flannel VXLAN port")
def nothing_else(out) -> None:
    allowed_ports = {"22", API, KUBELET} | WIREGUARD
    for source, port, proto in _parsed(_rules(out)):
        assert port in allowed_ports, f"unexpected port {port}/{proto} for {source}"
        assert port != VXLAN, "8472/udp (unencrypted VXLAN) must never be opened"
        assert source not in WORLD, f"{port} opened to {source}"
    sources = set(_by_source(_rules(out)))
    assert sources <= {ADMIN, SPOKE_1, SPOKE_2, HUB} | CLUSTER_CIDRS, f"unexpected sources: {sources}"


@then("incoming traffic is denied by default")
def default_deny(out) -> None:
    assert "ufw default deny incoming" in _rules(out)
    assert "ufw default allow outgoing" in _rules(out)


@then("the SSH rule comes before the default policy and before the firewall is enabled")
def ssh_first(out) -> None:
    rules = _rules(out)
    ssh = next(i for i, r in enumerate(rules) if " port 22 " in r)
    deny = rules.index("ufw default deny incoming")
    enable = rules.index("ufw --force enable")
    assert ssh < deny < enable or ssh < enable, rules
    assert ssh < deny, "default deny is applied before SSH is allowed: that can lock you out"
    assert enable == len(rules) - 1, "enable must be the last step"
    assert not [r for r in rules[:ssh] if r.startswith("ufw allow") or r.startswith("ufw limit")], \
        "another rule precedes the SSH rule"


# ---------------------------------------------------------------- scenario 5


@then(
    "it rejects an admin address of 0.0.0.0/0, an admin address of any, a huge admin range, "
    "no admin address, an unknown role, a node address of 0.0.0.0 and an unusable SSH port, "
    "and prints no rules for any of them"
)
def rejects_unsafe() -> None:
    good = dict(ROLE="hub", ADMIN_IP=ADMIN, NODE_IPS=f"{SPOKE_1} {SPOKE_2}")
    cases = {
        "admin 0.0.0.0/0": {"ADMIN_IP": "0.0.0.0/0"},
        "admin any": {"ADMIN_IP": "any"},
        "admin /8": {"ADMIN_IP": "10.0.0.0/8"},
        "no admin": {"ADMIN_IP": ""},
        "unknown role": {"ROLE": "middle"},
        "node 0.0.0.0": {"NODE_IPS": f"{SPOKE_1} 0.0.0.0"},
        "node 0.0.0.0/0": {"NODE_IPS": "0.0.0.0/0"},
        "ssh port not a number": {"SSH_PORT": "22; rm -rf /"},
        "admin not an address": {"ADMIN_IP": "evil.example.com"},
    }
    failures = []
    for name, override in cases.items():
        res = _run_script(_env(**{**good, **override}))
        if res.returncode == 0 or _rules(res.stdout):
            failures.append(f"{name}: exit={res.returncode}, printed {len(_rules(res.stdout))} rules")
        elif not res.stderr.strip():
            failures.append(f"{name}: rejected silently (no explanation on stderr)")
    assert not failures, "Unsafe input was accepted:\n  " + "\n  ".join(failures)


# ---------------------------------------------------------------- scenarios 6-7


@pytest.fixture
def fake_ufw(tmp_path) -> tuple:
    """A `ufw` on PATH that only records its arguments, so nothing real is ever changed."""
    bindir = tmp_path / "bin"
    bindir.mkdir()
    log = tmp_path / "ufw.log"
    exe = bindir / "ufw"
    exe.write_text(f'#!/bin/sh\necho "ufw $*" >> "{log}"\n')
    exe.chmod(exe.stat().st_mode | stat.S_IXUSR)
    return bindir, log


@given("the firewall script with a recording fake ufw", target_fixture="fake")
def script_with_fake(fake_ufw) -> None:
    assert SCRIPT.is_file(), f"{SCRIPT.relative_to(REPO_ROOT)} does not exist"
    return fake_ufw


_HUB_ENV = dict(ROLE="hub", ADMIN_IP=ADMIN, NODE_IPS=f"{SPOKE_1} {SPOKE_2}")


@when("I run it without APPLY", target_fixture="result")
def run_dry(fake) -> None:
    bindir, log = fake
    return _run_script(_env(**_HUB_ENV), extra_path=str(bindir))


@then("ufw was never called and it says it is a dry run")
def dry_run(fake, result) -> None:
    _, log = fake
    assert result.returncode == 0, result.stderr
    assert not log.exists(), f"ufw was called in a dry run:\n{log.read_text()}"
    assert "dry run" in (result.stdout + result.stderr).lower()
    assert _rules(result.stdout), "a dry run must still print the rules"


@when("I run it with APPLY=1", target_fixture="result")
def run_apply(fake) -> None:
    bindir, log = fake
    return _run_script(_env(APPLY="1", **_HUB_ENV), extra_path=str(bindir))


@then("ufw was called with exactly the printed rules, in the same order")
def applied(fake, result) -> None:
    _, log = fake
    assert result.returncode == 0, result.stderr
    assert log.exists(), "ufw was never called"
    called = log.read_text().splitlines()
    assert called == _rules(result.stdout)
    assert len(called) > 5
