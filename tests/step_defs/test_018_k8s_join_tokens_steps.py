import re

from pytest_bdd import scenarios, given, when, then

from tests.k8s_helpers import REPO_ROOT, find_lines, fmt_hits, is_git_ignored, read_text

scenarios("../features/018_k8s_join_tokens.feature")

GUIDE = "kubernetes/secrets_management.md"

# kubeadm bootstrap token = [a-z0-9]{6}.[a-z0-9]{16}; only flagged on lines that talk about a token.
KUBEADM_TOKEN = re.compile(r"\b[a-z0-9]{6}\.[a-z0-9]{16}\b")
# k3s: full token "K10<ca-hash>::server:<secret>", or a literal value given to a token variable/flag.
K3S_FULL_TOKEN = re.compile(r"\bK10[0-9a-f]{20,}::(?:server|node):\S+")
K3S_TOKEN_ASSIGN = re.compile(r"""\bK3S(?:_AGENT)?_TOKEN=["']?([^\s"'<$]\S*)""")
SWARM_TOKEN = re.compile(r"\bSWMTKN-1-[A-Za-z0-9-]{20,}")  # Docker Swarm join token
TOKEN_ARG = re.compile(r"""--token(?:\s+|=)["']?([^\s"'\\]+)""")
CA_HASH_ARG = re.compile(r"--discovery-token-ca-cert-hash\s+sha256:([^\s\\]+)")
CERT_KEY_ARG = re.compile(r"--certificate-key\s+([^\s\\]+)")
MICROK8S_JOIN = re.compile(r"microk8s join \S+?/([^\s]+)")
CERT_KEY_BLOCK = re.compile(r"certificate key:?\s*\n?\s*([0-9a-f]{64})\b")


def _is_placeholder(value):
    value = value.strip("'\"` ")
    return (
        value == ""
        or re.fullmatch(r"[.…*]+", value) is not None  # "..." as in K3S_TOKEN=... in prose
        or value.startswith(("<", "$", "{{"))
        or value.upper().startswith(("REDACTED", "CHANGEME", "YOUR", "XXXX"))
    )


# ---------------------------------------------------------------- scenario 1


@when("I search for kubeadm bootstrap tokens", target_fixture="hits")
def search_kubeadm_tokens(files):
    candidates = find_lines(files, r"(?i)token")
    return [h for h in candidates if KUBEADM_TOKEN.search(h[2]) and "REDACTED" not in h[2]]


@then("none is found")
def none_found(hits):
    assert not hits, "Credentials found in committed files (rotate/delete them, then redact):\n" + fmt_hits(hits)


# ---------------------------------------------------------------- scenario 2


@when("I search for k3s and Docker Swarm join tokens", target_fixture="hits")
def search_k3s_and_swarm_tokens(files):
    hits = find_lines(files, K3S_FULL_TOKEN.pattern)
    hits += find_lines(files, SWARM_TOKEN.pattern)
    for hit in find_lines(files, K3S_TOKEN_ASSIGN.pattern):
        if not _is_placeholder(K3S_TOKEN_ASSIGN.search(hit[2]).group(1)):
            hits.append(hit)
    return hits


# ---------------------------------------------------------------- scenario 3


@when("I read every join command and token argument", target_fixture="join_args")
def read_join_arguments(files):
    found = []
    for pattern in (TOKEN_ARG, CA_HASH_ARG, CERT_KEY_ARG, MICROK8S_JOIN):
        for rel, number, line in find_lines(files, pattern.pattern):
            for match in pattern.finditer(line):
                found.append((rel, number, line, match.group(1)))
    return found


@then("each token, CA hash and certificate key is a placeholder")
def join_args_are_placeholders(join_args):
    bad = [(rel, n, line) for rel, n, line, value in join_args if not _is_placeholder(value)]
    assert not bad, "Real join values committed (use <PLACEHOLDER> or REDACTED):\n" + fmt_hits(bad)


# ---------------------------------------------------------------- scenario 4


@when("I search the files for kubeadm certificate keys", target_fixture="hits")
def search_certificate_keys(files):
    hits = []
    for rel in files:
        text = read_text(rel)
        if text and CERT_KEY_BLOCK.search(text):
            hits.append((str(rel), 0, "a kubeadm certificate key (64 hex characters)"))
    return hits


# ---------------------------------------------------------------- scenario 5


@given("the repository ignore rules")
def ignore_rules():
    assert (REPO_ROOT / ".gitignore").is_file()


@then("join tokens and admin kubeconfigs are ignored")
def token_files_ignored():
    must_ignore = [
        "node-token",
        "agent-token",
        "hub.token",
        "admin.conf",
        "super-admin.conf",
        "join-command.txt",
    ]
    leaking = [p for p in must_ignore if not is_git_ignored(p)]
    assert not leaking, f".gitignore would NOT stop these being committed: {leaking}"


# ---------------------------------------------------------------- scenario 6


@given("the secrets management guide", target_fixture="guide")
def secrets_guide():
    text = read_text(GUIDE)
    assert text, f"{GUIDE} is missing"
    return text


@then("it covers separate agent tokens, token files, rotation, deleting kubeadm tokens and shell history")
def guide_covers_tokens(guide):
    required = {
        "a separate agent token": "agent-token-file",
        "token files": "token-file",
        "rotating a k3s token": "k3s token rotate",
        "listing/deleting kubeadm tokens": "kubeadm token delete",
        "shell history": "shell history",
    }
    missing = [what for what, phrase in required.items() if phrase not in guide]
    assert not missing, f"{GUIDE} does not explain: {missing}"
