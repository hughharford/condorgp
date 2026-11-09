"""Topic B: join tokens are never committed (feature 018)."""

import re
from collections.abc import Collection
from pathlib import Path

from pytest_bdd import given, scenarios, then, when

from tests.k8s_helpers import (
    REPO_ROOT,
    Hit,
    assert_scan_skips,
    fmt_hits,
    is_git_ignored,
    read_text,
    require_text,
)

scenarios("../features/018_k8s_join_tokens.feature")

GUIDE = "kubernetes/secrets_management.md"

# kubeadm bootstrap token = [a-z0-9]{6}.[a-z0-9]{16}; only flagged on lines
# that mention a token.
KUBEADM_TOKEN = re.compile(r"\b[a-z0-9]{6}\.[a-z0-9]{16}\b")
# k3s: full token "K10<ca-hash>::server:<secret>", or a literal value given to
# a token
# variable or flag.
K3S_FULL_TOKEN = re.compile(r"\bK10[0-9a-f]{20,}::(?:server|node):\S+")
K3S_TOKEN_ASSIGN = re.compile(
    r"""\bK3S(?:_AGENT)?_TOKEN=["']?([^\s"'<$]\S*)"""
)
SWARM_TOKEN = re.compile(
    r"\bSWMTKN-1-[A-Za-z0-9-]{20,}"
)  # Docker Swarm join token
TOKEN_ARG = re.compile(r"""--token(?:\s+|=)["']?([^\s"'\\]+)""")
CA_HASH_ARG = re.compile(r"--discovery-token-ca-cert-hash\s+sha256:([^\s\\]+)")
CERT_KEY_ARG = re.compile(r"--certificate-key\s+([^\s\\]+)")
MICROK8S_JOIN = re.compile(r"microk8s join \S+?/([^\s]+)")
CERT_KEY_BLOCK = re.compile(r"certificate key:?\s*\n?\s*([0-9a-f]{64})\b")

# Paths that .gitignore must stop being committed.
MUST_IGNORE = (
    "node-token",
    "agent-token",
    "hub.token",
    "admin.conf",
    "super-admin.conf",
    "join-command.txt",
)
# What the secrets guide must explain: topic -> phrase that shows it is
# covered.
GUIDE_TOPICS = {
    "a separate agent token": "agent-token-file",
    "token files": "token-file",
    "rotating a k3s token": "k3s token rotate",
    "listing/deleting kubeadm tokens": "kubeadm token delete",
    "shell history": "shell history",
}

CANARY_FILE = "tests/test_data/k8s/canary-join-tokens.example.txt"

# The kinds of join credential the checks look for. The canary must hold at
# least one of each, so no kind can quietly stop being checked.
KIND_KUBEADM = "kubeadm bootstrap token"
KIND_K3S = "k3s join token"
KIND_SWARM = "Docker Swarm join token"
KIND_K3S_VARIABLE = "k3s token variable with a real value"
KIND_TOKEN_ARG = "--token argument with a real value"
KIND_CA_HASH = "CA hash argument with a real value"
KIND_CERT_ARG = "--certificate-key argument with a real value"
KIND_MICROK8S = "microk8s join value"
KIND_CERT_BLOCK = "kubeadm certificate key"

# Arguments whose value must be a placeholder, by kind.
JOIN_ARGUMENTS = {
    KIND_TOKEN_ARG: TOKEN_ARG,
    KIND_CA_HASH: CA_HASH_ARG,
    KIND_CERT_ARG: CERT_KEY_ARG,
    KIND_MICROK8S: MICROK8S_JOIN,
}
# Checks by scenario.
KUBEADM_KINDS = {KIND_KUBEADM}
TOKEN_KINDS = {KIND_K3S, KIND_SWARM, KIND_K3S_VARIABLE}
ARGUMENT_KINDS = set(JOIN_ARGUMENTS)
CERT_KEY_KINDS = {KIND_CERT_BLOCK}
ALL_KINDS = KUBEADM_KINDS | TOKEN_KINDS | ARGUMENT_KINDS | CERT_KEY_KINDS

# (kind, line number, line text)
Finding = tuple[str, int, str]


def _is_placeholder(value: str) -> bool:
    """Return True for an obviously fake value (<TOKEN>, $VAR, REDACTED)."""
    value = value.strip("'\"` ")
    return (
        value == ""
        or re.fullmatch(r"[.…*]+", value)
        is not None  # "..." as in K3S_TOKEN=... in prose
        or value.startswith(("<", "$", "{{"))
        or value.upper().startswith(("REDACTED", "CHANGEME", "YOUR", "XXXX"))
    )


def _line_kinds(line: str) -> list[str]:
    """Return the kinds of join credential found on one line."""
    kinds: list[str] = []
    if (
        re.search(r"(?i)token", line)
        and KUBEADM_TOKEN.search(line)
        and "REDACTED" not in line
    ):
        kinds.append(KIND_KUBEADM)
    if K3S_FULL_TOKEN.search(line):
        kinds.append(KIND_K3S)
    if SWARM_TOKEN.search(line):
        kinds.append(KIND_SWARM)
    assignment = K3S_TOKEN_ASSIGN.search(line)
    if assignment and not _is_placeholder(assignment.group(1)):
        kinds.append(KIND_K3S_VARIABLE)
    for kind, pattern in JOIN_ARGUMENTS.items():
        values = [match.group(1) for match in pattern.finditer(line)]
        if any(not _is_placeholder(value) for value in values):
            kinds.append(kind)
    return kinds


def _findings(text: str) -> list[Finding]:
    """Return every join credential in a text, as (kind, line, text).

    This is the one place the credential patterns are applied, so the real
    scan and the canary can never drift apart.
    """
    found: list[Finding] = []
    for number, line in enumerate(text.splitlines(), 1):
        found += [(kind, number, line.strip()) for kind in _line_kinds(line)]
    for match in CERT_KEY_BLOCK.finditer(text):
        number = text.count("\n", 0, match.start()) + 1
        found.append(
            (
                KIND_CERT_BLOCK,
                number,
                "a kubeadm certificate key (64 hex characters)",
            )
        )
    return found


def _repo_hits(files: list[Path], kinds: Collection[str]) -> list[Hit]:
    """Return (path, line, text) for credentials of the given kinds."""
    hits: list[Hit] = []
    for rel in files:
        text = read_text(rel)
        if text is not None:
            hits += [
                (str(rel), number, line)
                for kind, number, line in _findings(text)
                if kind in kinds
            ]
    return hits


# ---------------------------------------------------------------- scenario 1


@when("I search for kubeadm bootstrap tokens", target_fixture="hits")
def search_kubeadm_tokens(files: list[Path]) -> list[Hit]:
    """Find kubeadm bootstrap tokens on lines that talk about a token."""
    return _repo_hits(files, KUBEADM_KINDS)


@then("none is found")
def none_found(hits: list[Hit]) -> None:
    """Fail, listing every credential found."""
    assert not hits, (
        "Credentials found in committed files "
        "(rotate/delete them, then redact):\n" + fmt_hits(hits)
    )


# ---------------------------------------------------------------- scenario 2


@when("I search for k3s and Docker Swarm join tokens", target_fixture="hits")
def search_k3s_and_swarm_tokens(files: list[Path]) -> list[Hit]:
    """Find k3s tokens, Swarm join tokens and k3s token variables."""
    return _repo_hits(files, TOKEN_KINDS)


# ---------------------------------------------------------------- scenario 3


@when(
    "I read every join command and token argument", target_fixture="join_args"
)
def read_join_arguments(files: list[Path]) -> list[Hit]:
    """Find every --token, CA hash, certificate key and join value."""
    return _repo_hits(files, ARGUMENT_KINDS)


@then("each token, CA hash and certificate key is a placeholder")
def join_args_are_placeholders(join_args: list[Hit]) -> None:
    """Fail on any join value that is not a placeholder."""
    assert not join_args, (
        "Real join values committed (use <PLACEHOLDER> or REDACTED):\n"
        + fmt_hits(join_args)
    )


# ---------------------------------------------------------------- scenario 4


@when("I search the files for kubeadm certificate keys", target_fixture="hits")
def search_certificate_keys(files: list[Path]) -> list[Hit]:
    """Find kubeadm certificate keys (64 hex characters)."""
    return _repo_hits(files, CERT_KEY_KINDS)


# ---------------------------------------------------------------- scenario 5


@given("the repository ignore rules")
def ignore_rules() -> None:
    """Require a .gitignore at the repo root."""
    assert (REPO_ROOT / ".gitignore").is_file()


@then("join tokens and admin kubeconfigs are ignored")
def token_files_ignored() -> None:
    """Fail if .gitignore would let a token or kubeconfig be committed."""
    leaking = [path for path in MUST_IGNORE if not is_git_ignored(path)]
    assert (
        not leaking
    ), f".gitignore would NOT stop these being committed: {leaking}"


# ---------------------------------------------------------------- scenario 6


@given("the secrets management guide", target_fixture="guide")
def secrets_guide() -> str:
    """Load the secrets management guide."""
    return require_text(GUIDE)


@then(
    "it covers separate agent tokens, token files, rotation, "
    "deleting kubeadm tokens and shell history"
)
def guide_covers_tokens(guide: str) -> None:
    """Fail if the guide skips any topic in GUIDE_TOPICS."""
    missing = [
        topic for topic, phrase in GUIDE_TOPICS.items() if phrase not in guide
    ]
    assert not missing, f"{GUIDE} does not explain: {missing}"


# ---------------------------------------------------------------- canary


def _canary_text() -> str:
    """Return the canary's text, failing clearly if it was removed."""
    return require_text(CANARY_FILE)


def _assert_canary_still_bad(text: str) -> None:
    """Fail unless the text still holds every kind of join credential."""
    found = {kind for kind, _, _ in _findings(text)}
    missing = sorted(ALL_KINDS - found)
    assert not missing, (
        f"{CANARY_FILE} no longer holds these kinds of credential, so those "
        f"checks could no longer fail: {missing}"
    )


def _redacted(text: str) -> str:
    """Return a copy with every credential replaced by a placeholder."""
    for pattern in (KUBEADM_TOKEN, K3S_FULL_TOKEN, SWARM_TOKEN):
        text = pattern.sub("REDACTED", text)
    for pattern in (K3S_TOKEN_ASSIGN, *JOIN_ARGUMENTS.values()):
        text = re.sub(
            pattern,
            lambda m: m.group(0).replace(m.group(1), "<PLACEHOLDER>"),
            text,
        )
    return CERT_KEY_BLOCK.sub(
        lambda m: m.group(0).replace(m.group(1), "REDACTED"), text
    )


def _without_kind(text: str, kind: str) -> str:
    """Return a copy with every credential of one kind removed."""
    if kind == KIND_CERT_BLOCK:
        return CERT_KEY_BLOCK.sub("", text)
    return "\n".join(
        line for line in text.splitlines() if kind not in _line_kinds(line)
    )


@given("the token canary kept in the test data", target_fixture="canary")
def token_canary() -> str:
    """Load the canary text."""
    return _canary_text()


@then("it says plainly that every value in it is fake")
def canary_is_marked_fake(canary: str) -> None:
    """Check the canary announces that it is fake and must stay bad."""
    assert "CANARY" in canary and "FAKE" in canary, (
        "the canary must say it is a fake, deliberately bad example "
        "(CANARY, FAKE) so nobody mistakes it for a real leak"
    )


@then("every kind of join credential the checks look for is found in it")
def canary_holds_every_kind(canary: str) -> None:
    """Check every kind of credential is flagged in the canary."""
    _assert_canary_still_bad(canary)


@when(
    "I redact, empty or strip one kind of credential from a copy",
    target_fixture="sanitised_copies",
)
def sanitise_canary_copies(canary: str) -> dict[str, str]:
    """Make copies of the canary that someone has 'fixed'."""
    copies = {"redacted": _redacted(canary), "emptied": ""}
    for kind in sorted(ALL_KINDS):
        copies[f"without: {kind}"] = _without_kind(canary, kind)
    return copies


@then("the canary guard rejects that copy")
def canary_guard_rejects(sanitised_copies: dict[str, str]) -> None:
    """Check the guard rejects every sanitised copy, accepts the real one."""
    _assert_canary_still_bad(_canary_text())  # the real one passes the guard
    accepted: list[str] = []
    for name, copy in sanitised_copies.items():
        try:
            _assert_canary_still_bad(copy)
        except AssertionError:
            continue  # rejected, as it should be
        accepted.append(name)
    assert (
        not accepted
    ), f"the canary guard wrongly accepted these safe copies: {accepted}"


@then("the repository scan skips it")
def scan_skips_canary(canary: str) -> None:
    """Check the real scan never reads tests/, or the canary would fail it."""
    assert_scan_skips(CANARY_FILE)
