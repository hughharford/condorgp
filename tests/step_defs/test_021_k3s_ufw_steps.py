"""Topic F: ufw rules are limited to the cluster's own machines (feature 021)."""

import os
import re
import stat
import subprocess
from dataclasses import dataclass
from pathlib import Path

import pytest
from pytest_bdd import given, scenarios, then, when

from tests.k8s_helpers import REPO_ROOT, Hit, find_lines, fmt_hits, run

scenarios("../features/021_k3s_ufw.feature")

SCRIPT = REPO_ROOT / "k3s/ufw_rules.sh"

ADMIN = "203.0.113.10"
HUB = "198.51.100.1"
SPOKE_1 = "198.51.100.2"
SPOKE_2 = "198.51.100.3"
CLUSTER_CIDRS = {"10.42.0.0/16", "10.43.0.0/16"}  # k3s default pod + service networks
WORLD = {"any", "anywhere", "0.0.0.0", "0.0.0.0/0", "::/0", "::"}

# Ports the script is allowed to open, and nothing else (k3s docs, "Inbound rules").
SSH = "22"
API = "6443"
WIREGUARD = {"51820", "51821"}
KUBELET = "10250"
VXLAN = "8472"

UFW_OPEN = re.compile(r"\bufw\s+(?:allow|limit)\b")
FROM_SRC = re.compile(r"\bfrom\s+(\S+)")
RULE_FROM = re.compile(r"^ufw (allow|limit) from (\S+) to any(?: port (\d+) proto (tcp|udp))?$")
POLICY_RULES = ("ufw default", "ufw --force enable")
DENY_INCOMING = "ufw default deny incoming"
ALLOW_OUTGOING = "ufw default allow outgoing"
ENABLE = "ufw --force enable"

HUB_ENV = {"ROLE": "hub", "ADMIN_IP": ADMIN, "NODE_IPS": f"{SPOKE_1} {SPOKE_2}"}
SPOKE_ENV = {"ROLE": "spoke", "ADMIN_IP": ADMIN, "NODE_IPS": f"{HUB} {SPOKE_2}"}
# Inputs the script must refuse, with a name for the failure message.
UNSAFE_INPUTS = {
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

# One allow rule: (source, port, protocol)
Allow = tuple[str, str, str]


@dataclass
class FakeUfw:
    """A `ufw` that only records its arguments, so nothing real is ever changed."""

    bindir: Path
    log: Path


def _rules(stdout: str) -> list[str]:
    """Return the `ufw ...` lines the script printed, in order."""
    return [line.strip() for line in stdout.splitlines() if line.startswith("ufw ")]


def _env(**extra: str) -> dict[str, str]:
    """Return a minimal environment for the script, plus the given variables."""
    env = {"PATH": os.environ["PATH"], "HOME": os.environ.get("HOME", "/tmp")}
    env.update(extra)
    return env


def _run_script(
    env: dict[str, str], extra_path: str | None = None
) -> subprocess.CompletedProcess[str]:
    """Run the firewall script with env, optionally putting extra_path first on PATH."""
    assert SCRIPT.is_file(), f"{SCRIPT.relative_to(REPO_ROOT)} does not exist"
    env = dict(env)  # never change the caller's copy
    if extra_path:
        env["PATH"] = f"{extra_path}:{env['PATH']}"
    return run(["bash", str(SCRIPT)], env=env, cwd=str(REPO_ROOT))


def _generate(role_env: dict[str, str]) -> str:
    """Run the script in dry-run mode for the given role and return what it printed."""
    result = _run_script(_env(**role_env))
    assert result.returncode == 0, result.stderr
    return result.stdout


def _parsed(rules: list[str]) -> list[Allow]:
    """Return each allow rule as (source, port, proto); anything unparseable fails the test."""
    allows: list[Allow] = []
    for rule in rules:
        if rule.startswith(POLICY_RULES):
            continue
        match = RULE_FROM.match(rule)
        assert match, f"rule is not a 'from <source> to any [port <n> proto <p>]' rule: {rule!r}"
        source, port, proto = match.group(2), match.group(3), match.group(4)
        if port is None:  # portless rule: only the k3s pod/service networks may have one
            assert source in CLUSTER_CIDRS, f"portless rule for a non-cluster source: {rule!r}"
            continue
        allows.append((source, port, proto))
    return allows


def _by_source(rules: list[str]) -> dict[str, set[tuple[str, str]]]:
    """Group the allowed (port, proto) pairs by the source they are allowed from."""
    grouped: dict[str, set[tuple[str, str]]] = {}
    for source, port, proto in _parsed(rules):
        grouped.setdefault(source, set()).add((port, proto))
    return grouped


# ---------------------------------------------------------------- scenario 1


@when("I read every ufw allow or limit rule", target_fixture="open_rules")
def read_ufw_rules(files: list[Path]) -> list[Hit]:
    """Find every ufw allow/limit line that names no source, or names the whole world."""
    bad: list[Hit] = []
    for hit in find_lines(files, UFW_OPEN.pattern):
        source = FROM_SRC.search(hit[2])
        value = source.group(1).strip("\"'") if source else None
        if value is None or value.lower() in WORLD:
            bad.append(hit)
    return bad


@then("each one is limited to a source address")
def all_limited(open_rules: list[Hit]) -> None:
    """Fail, listing every rule that opens a port to every source."""
    assert not open_rules, "ufw rules that open a port to every source:\n" + fmt_hits(open_rules)


# ---------------------------------------------------------------- scenarios 2-4


@given("the firewall script")
def firewall_script() -> None:
    """Require the script to exist."""
    assert SCRIPT.is_file(), f"{SCRIPT.relative_to(REPO_ROOT)} does not exist"


@when("I generate the rules for a hub with two spokes", target_fixture="out")
def hub_rules() -> str:
    """Generate the rules for a hub."""
    return _generate(HUB_ENV)


@when("I generate the rules for a spoke with a hub and one other spoke", target_fixture="out")
def spoke_rules() -> str:
    """Generate the rules for a spoke."""
    return _generate(SPOKE_ENV)


@then("SSH is allowed from the admin address only")
def ssh_admin_only(out: str) -> None:
    """Require SSH to be allowed from the admin address and nowhere else."""
    ssh = [rule for rule in _parsed(_rules(out)) if rule[1] == SSH]
    assert ssh == [(ADMIN, SSH, "tcp")], f"SSH rules: {ssh}"


@then("the API port is allowed from the admin and each node only")
def api_hub(out: str) -> None:
    """Require the API port to be open to the admin and each spoke, and no one else."""
    sources = {source for source, port, _ in _parsed(_rules(out)) if port == API}
    assert sources == {ADMIN, SPOKE_1, SPOKE_2}, f"6443 allowed from: {sources}"


@then("the API port is not opened")
def api_spoke(out: str) -> None:
    """Require that a spoke does not open the API port at all."""
    assert [rule for rule in _rules(out) if API in rule.split()] == []


@then("WireGuard and kubelet ports are allowed from each node only")
def node_ports(out: str) -> None:
    """Every peer node gets WireGuard and kubelet access; the admin gets neither."""
    by_source = _by_source(_rules(out))
    peers = {source for source in by_source if source not in {ADMIN} | CLUSTER_CIDRS}
    assert peers, "no node rules at all"
    for peer in peers:
        ports = {port for port, _ in by_source[peer]}
        assert KUBELET in ports and ports >= WIREGUARD, f"{peer} gets {sorted(ports)}"
    # the admin gets SSH (+ the API on a hub), never node-to-node traffic
    admin_ports = {port for port, _ in by_source.get(ADMIN, set())}
    assert not admin_ports & (WIREGUARD | {KUBELET}), f"admin was given node ports: {admin_ports}"


@then("nothing else is opened, and in particular not the Flannel VXLAN port")
def nothing_else(out: str) -> None:
    """Only the expected ports are open, to known sources, and never 8472/udp."""
    allowed_ports = {SSH, API, KUBELET} | WIREGUARD
    for source, port, proto in _parsed(_rules(out)):
        assert port in allowed_ports, f"unexpected port {port}/{proto} for {source}"
        assert port != VXLAN, "8472/udp (unencrypted VXLAN) must never be opened"
        assert source not in WORLD, f"{port} opened to {source}"
    sources = set(_by_source(_rules(out)))
    known = {ADMIN, SPOKE_1, SPOKE_2, HUB} | CLUSTER_CIDRS
    assert sources <= known, f"unexpected sources: {sources}"


@then("incoming traffic is denied by default")
def default_deny(out: str) -> None:
    """Require default-deny incoming and default-allow outgoing."""
    assert DENY_INCOMING in _rules(out)
    assert ALLOW_OUTGOING in _rules(out)


@then("the SSH rule comes before the default policy and before the firewall is enabled")
def ssh_first(out: str) -> None:
    """Require SSH to be the first rule, before default-deny, with enable last."""
    rules = _rules(out)
    ssh = next(index for index, rule in enumerate(rules) if f" port {SSH} " in rule)
    assert ssh < rules.index(
        DENY_INCOMING
    ), "default deny is applied before SSH is allowed: that can lock you out"
    assert rules.index(ENABLE) == len(rules) - 1, "enable must be the last step"
    earlier_allows = [rule for rule in rules[:ssh] if rule.startswith(("ufw allow", "ufw limit"))]
    assert not earlier_allows, "another rule precedes the SSH rule"


# ---------------------------------------------------------------- scenario 5


@then(
    "it rejects an admin address of 0.0.0.0/0, an admin address of any, a huge admin range, "
    "no admin address, an unknown role, a node address of 0.0.0.0 and an unusable SSH port, "
    "and prints no rules for any of them"
)
def rejects_unsafe() -> None:
    """Every unsafe input must make the script exit non-zero, explain why, and print no rules."""
    failures: list[str] = []
    for name, override in UNSAFE_INPUTS.items():
        result = _run_script(_env(**{**HUB_ENV, **override}))
        printed = len(_rules(result.stdout))
        if result.returncode == 0 or printed:
            failures.append(f"{name}: exit={result.returncode}, printed {printed} rules")
        elif not result.stderr.strip():
            failures.append(f"{name}: rejected silently (no explanation on stderr)")
    assert not failures, "Unsafe input was accepted:\n  " + "\n  ".join(failures)


# ---------------------------------------------------------------- scenarios 6-7


@pytest.fixture
def fake_ufw(tmp_path: Path) -> FakeUfw:
    """Create a `ufw` that records its arguments to a log instead of changing the firewall."""
    bindir = tmp_path / "bin"
    bindir.mkdir()
    log = tmp_path / "ufw.log"
    exe = bindir / "ufw"
    exe.write_text(f'#!/bin/sh\necho "ufw $*" >> "{log}"\n')
    exe.chmod(exe.stat().st_mode | stat.S_IXUSR)
    return FakeUfw(bindir=bindir, log=log)


@given("the firewall script with a recording fake ufw", target_fixture="fake")
def script_with_fake(fake_ufw: FakeUfw) -> FakeUfw:
    """Require the script, and hand the recording fake ufw to the scenario."""
    assert SCRIPT.is_file(), f"{SCRIPT.relative_to(REPO_ROOT)} does not exist"
    return fake_ufw


@when("I run it without APPLY", target_fixture="result")
def run_dry(fake: FakeUfw) -> subprocess.CompletedProcess[str]:
    """Run the script as a hub without APPLY."""
    return _run_script(_env(**HUB_ENV), extra_path=str(fake.bindir))


@then("ufw was never called and it says it is a dry run")
def dry_run(fake: FakeUfw, result: subprocess.CompletedProcess[str]) -> None:
    """Require no ufw calls, a dry-run notice, and the rules still printed."""
    assert result.returncode == 0, result.stderr
    assert not fake.log.exists(), f"ufw was called in a dry run:\n{fake.log.read_text()}"
    assert "dry run" in (result.stdout + result.stderr).lower()
    assert _rules(result.stdout), "a dry run must still print the rules"


@when("I run it with APPLY=1", target_fixture="result")
def run_apply(fake: FakeUfw) -> subprocess.CompletedProcess[str]:
    """Run the script as a hub with APPLY=1."""
    return _run_script(_env(APPLY="1", **HUB_ENV), extra_path=str(fake.bindir))


@then("ufw was called with exactly the printed rules, in the same order")
def applied(fake: FakeUfw, result: subprocess.CompletedProcess[str]) -> None:
    """Require the fake ufw to have received exactly the printed rules, in order."""
    assert result.returncode == 0, result.stderr
    assert fake.log.exists(), "ufw was never called"
    called = fake.log.read_text().splitlines()
    assert called == _rules(result.stdout)
    assert len(called) > 5
