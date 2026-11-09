"""Topic A: cluster secrets are encrypted in the repo (feature 017)."""

import base64
import os
import re
import shutil
import stat
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest
from pytest_bdd import given, scenarios, then, when

from tests.k8s_helpers import (
    REPO_ROOT,
    assert_scan_skips,
    is_git_ignored,
    read_text,
    run,
    yaml_docs,
)

scenarios("../features/017_k8s_secrets_encrypted.feature")

SECRET_KIND = re.compile(r"(?m)^kind:\s*Secret\s*$")
PLACEHOLDER = "CHANGEME"
WELL_KNOWN_DEFAULTS = {
    "postgres",
    "cgp-pass",
    "cgp_pass",
    "guest",
    "admin",
    "password",
}
ENC_FILE = "k8s/02-secrets.enc.yaml"
TEMPLATE_FILE = "k8s/02-secrets.example.yaml"
SOPS_PLACEHOLDER = "AGE_PUBLIC_KEY_NOT_SET"
SECRET_KEYS_RANDOM = (
    "postgres-password",
    "app-db-pass",
    "rabbitmq-pass",
    "grafana-admin-password",
)
SECRETS_SCRIPT = ["bash", "k8s/secrets/secrets.sh"]
# A deliberately bad Secret kept so the checks can always be seen to fail. It
# is named
# *.example.yaml so that `secrets.sh check` skips it, and it lives under
# tests/, which the
# repository scan never reads. Every value in it is fake.
CANARY_FILE = "tests/test_data/k8s/canary-plaintext-secret.example.yaml"
CANARY_FAKE_PREFIX = "FAKE-NOT-A-REAL-SECRET"
GITIGNORE_MUST_HIDE = (
    "keys.txt",
    "k8s/secrets/age-key.txt",
    "backup.agekey",
    "k8s/02-secrets.dec.yaml",
    "k8s/02-secrets.plain.yaml",
    "k3s.yaml",
    "kubeconfig",
    "hub.kubeconfig",
)

# One Secret manifest in the repo: (path, parsed YAML document)
SecretDoc = tuple[str, dict[str, Any]]


@dataclass
class Vault:
    """A throwaway copy of the secrets tooling and its own key."""

    root: Path
    env: dict[str, str]
    key: Path
    enc: Path
    capture: Path | None = (
        None  # where the fake kubectl records what it was given
    )


def _values(doc: dict[str, Any]) -> dict[str, Any]:
    """All values of a Secret, from both `data` and `stringData`."""
    return {**(doc.get("data") or {}), **(doc.get("stringData") or {})}


def _is_enc(value: object) -> bool:
    """Return True if the value is a SOPS ENC[...] token."""
    return str(value).startswith("ENC[AES256_GCM,")


def _need(*tools: str) -> None:
    """Skip the test if any of the given tools is not installed."""
    missing = [tool for tool in tools if not shutil.which(tool)]
    if missing:
        pytest.skip(
            f"needs {', '.join(missing)} on PATH "
            "(see kubernetes/secrets_management.md, Prerequisites)"
        )


def _scratch_tooling(tmp_path: Path) -> Path:
    """Copy the secrets script and sops config into an empty dir."""
    script = REPO_ROOT / "k8s/secrets/secrets.sh"
    assert script.is_file(), "k8s/secrets/secrets.sh is missing"
    (tmp_path / "k8s/secrets").mkdir(parents=True)
    shutil.copy(script, tmp_path / "k8s/secrets/secrets.sh")
    config = REPO_ROOT / "k8s/.sops.yaml"
    assert config.is_file(), "k8s/.sops.yaml is missing"
    shutil.copy(config, tmp_path / "k8s/.sops.yaml")
    return tmp_path


def _isolated_env(tmp_path: Path, key_file: Path) -> dict[str, str]:
    """Return an environment that sees only the throwaway key."""
    env = {
        name: value
        for name, value in os.environ.items()
        if not name.startswith("SOPS_")
    }
    env["HOME"] = str(tmp_path)
    env["SOPS_AGE_KEY_FILE"] = str(key_file)
    return env


def _new_age_key(path: Path) -> None:
    """Create a throwaway age private key at path (mode 600)."""
    res = run(["age-keygen", "-o", str(path)])
    assert res.returncode == 0, res.stderr
    path.chmod(0o600)


def _decrypt_value(root: Path, env: dict[str, str], key: str) -> str:
    """Read one decrypted value through the repo's own `secrets.sh get`."""
    res = run([*SECRETS_SCRIPT, "get", key], cwd=root, env=env)
    assert res.returncode == 0, f"could not read {key}: {res.stderr}"
    return res.stdout.strip()


# ---------------------------------------------------------------- scenarios
# 1-2


@when("I list the Kubernetes Secret manifests", target_fixture="secrets")
def list_secret_manifests(files: list[Path]) -> list[SecretDoc]:
    """Find every Secret document (or flag files that cannot be parsed)."""
    found: list[SecretDoc] = []
    for rel in files:
        if rel.suffix not in (".yaml", ".yml"):
            continue
        text = read_text(rel)
        if not text or not SECRET_KIND.search(text):
            continue
        docs = [d for d in yaml_docs(rel) if d.get("kind") == "Secret"]
        found += [(str(rel), d) for d in docs] or [
            (str(rel), {"_unparseable": True})
        ]
    return found


def _by_kind(docs: list[dict[str, Any]], kind: str) -> list[dict[str, Any]]:
    """Return the documents of the given Kubernetes kind."""
    return [doc for doc in docs if doc.get("kind") == kind]


def _classify(doc: dict[str, Any]) -> str:
    """Say if a Secret is encrypted, empty, a template or PLAINTEXT."""
    if doc.get("_unparseable"):
        return (
            "PLAINTEXT? (YAML could not be parsed, so it cannot be shown safe)"
        )
    values = _values(doc)
    if "sops" in doc:
        if all(_is_enc(value) for value in values.values()):
            return "encrypted"
        return "PLAINTEXT (sops block but readable values)"
    if all(str(value).strip() == "" for value in values.values()):
        # e.g. the Dashboard's own Secrets, which it fills in itself
        return "empty shell"
    if all(str(value).strip() == PLACEHOLDER for value in values.values()):
        return "template"
    return "PLAINTEXT"


@then("every Secret is SOPS-encrypted, an empty shell or a CHANGEME template")
def secrets_are_safe(secrets: list[SecretDoc]) -> None:
    """Fail on any Secret whose values can be read."""
    verdicts = [(rel, _classify(doc)) for rel, doc in secrets]
    bad = [
        f"  {rel}: {verdict}"
        for rel, verdict in verdicts
        if verdict.startswith("PLAINTEXT")
    ]
    assert (
        not bad
    ), "Committed Secret manifests with readable values:\n" + "\n".join(bad)


def _decoded_values(
    rel: str, doc: dict[str, Any]
) -> list[tuple[str, str, str]]:
    """Return (path, key, value) for a Secret, decoding base64 `data`."""
    decoded: list[tuple[str, str, str]] = []
    for key, value in (doc.get("data") or {}).items():
        try:
            value = base64.b64decode(str(value), validate=True).decode("utf-8")
        except ValueError:  # not base64 or not UTF-8: compare the raw text
            value = str(value)
        decoded.append((rel, key, value))
    for key, value in (doc.get("stringData") or {}).items():
        decoded.append((rel, key, str(value)))
    return decoded


def _default_password_findings(
    decoded: list[tuple[str, str, str]],
) -> list[str]:
    """Describe every decoded value that is a well-known default password."""
    return [
        f"  {rel}: {key}"
        for rel, key, value in decoded
        if value.strip().lower() in WELL_KNOWN_DEFAULTS
    ]


@when("I decode the values of every Secret manifest", target_fixture="decoded")
def decode_secret_values(files: list[Path]) -> list[tuple[str, str, str]]:
    """Decode every Secret value (base64 for `data`, raw otherwise)."""
    decoded: list[tuple[str, str, str]] = []
    for rel in files:
        if rel.suffix not in (".yaml", ".yml"):
            continue
        for doc in _by_kind(yaml_docs(rel), "Secret"):
            decoded += _decoded_values(str(rel), doc)
    return decoded


@then("none of them is a well-known default password")
def no_default_passwords(decoded: list[tuple[str, str, str]]) -> None:
    """Fail on any Secret value that is a well-known default password."""
    bad = _default_password_findings(decoded)
    assert not bad, (
        "Secrets still hold default credentials "
        "(these are in the public git history, so rotate them):\n"
        + "\n".join(bad)
    )


# ---------------------------------------------------------------- scenario 3


@when("I list the SOPS-encrypted files", target_fixture="enc_files")
def list_encrypted_files(files: list[Path]) -> list[Path]:
    """Find every *.enc.yaml file."""
    return [rel for rel in files if re.search(r"\.enc\.ya?ml$", str(rel))]


@then("each one has SOPS metadata and only ENC tokens as values")
def encrypted_files_are_encrypted(enc_files: list[Path]) -> None:
    """Each file must carry SOPS metadata and hold only ENC[...] values."""
    problems: list[str] = []
    for rel in enc_files:
        docs = yaml_docs(rel)
        if not docs:
            problems.append(f"  {rel}: not readable as YAML")
            continue
        for doc in docs:
            sops = doc.get("sops") or {}
            if not (sops.get("age") and sops.get("mac")):
                problems.append(f"  {rel}: missing sops age recipients / mac")
            for key, value in _values(doc).items():
                if not _is_enc(value):
                    problems.append(
                        f"  {rel}: value of '{key}' is not an ENC[...] token"
                    )
    assert not problems, "\n".join(problems)


# ---------------------------------------------------------------- scenario 4


@given("the repository ignore rules")
def ignore_rules() -> None:
    """Require a .gitignore at the repo root."""
    assert (REPO_ROOT / ".gitignore").is_file()


@then("age keys, decrypted copies and kubeconfigs are ignored")
def secrets_paths_ignored() -> None:
    """Fail if .gitignore would let a key or kubeconfig be committed."""
    leaking = [
        path for path in GITIGNORE_MUST_HIDE if not is_git_ignored(path)
    ]
    assert (
        not leaking
    ), f".gitignore would NOT stop these being committed: {leaking}"


@then("the encrypted Secret and the CHANGEME template are not ignored")
def encrypted_and_template_not_ignored() -> None:
    """Fail if .gitignore would hide the files that must be committed."""
    wrongly = [
        path for path in (ENC_FILE, TEMPLATE_FILE) if is_git_ignored(path)
    ]
    assert (
        not wrongly
    ), f".gitignore would hide files that must be committed: {wrongly}"


# ---------------------------------------------------------------- scenario 5


@given(
    "a scratch git repository using the repo's secrets script",
    target_fixture="scratch",
)
def scratch_repo(tmp_path: Path) -> Path:
    """Create an empty git repo holding only a copy of the secrets script."""
    root = _scratch_tooling(tmp_path)
    assert run(["git", "init", "-q"], cwd=root).returncode == 0
    return root


@when(
    "I add a plaintext Secret manifest and run the secrets check",
    target_fixture="check_result",
)
def add_plaintext_and_check(scratch: Path) -> subprocess.CompletedProcess[str]:
    """Add a plaintext Secret and run `secrets.sh check`."""
    (scratch / "oops.yaml").write_text(
        "apiVersion: v1\nkind: Secret\nmetadata:\n  name: x\n"
        "stringData:\n  password: hunter2\n"
    )
    return run([*SECRETS_SCRIPT, "check"], cwd=scratch)


@then("the check fails and names the plaintext file")
def check_fails(check_result: subprocess.CompletedProcess[str]) -> None:
    """Require the check to exit non-zero and name oops.yaml."""
    assert (
        check_result.returncode != 0
    ), "check passed although a plaintext Secret is present"
    assert "oops.yaml" in check_result.stdout + check_result.stderr


@then("the check passes again once the plaintext Secret is removed")
def check_passes_after_removal(scratch: Path) -> None:
    """With the plaintext file gone, the check must pass again."""
    (scratch / "oops.yaml").unlink()
    res = run([*SECRETS_SCRIPT, "check"], cwd=scratch)
    assert res.returncode == 0, res.stdout + res.stderr


# ---------------------------------------------------------------- scenario 6


@given(
    "a scratch copy of the secrets tooling and a throwaway age key",
    target_fixture="vault",
)
def scratch_vault(tmp_path: Path) -> Vault:
    """Copy the tooling to a scratch dir and make a throwaway age key."""
    _need("sops", "age-keygen", "openssl")
    root = _scratch_tooling(tmp_path)
    key = tmp_path / "owner-key.txt"
    _new_age_key(key)
    env = _isolated_env(tmp_path, key)
    res = run([*SECRETS_SCRIPT, "init"], cwd=root, env=env)
    assert res.returncode == 0, res.stdout + res.stderr
    return Vault(root=root, env=env, key=key, enc=root / ENC_FILE)


@when("I generate the encrypted Secret")
def generate_secret(vault: Vault) -> None:
    """Run `secrets.sh generate` and require the encrypted file to appear."""
    res = run([*SECRETS_SCRIPT, "generate"], cwd=vault.root, env=vault.env)
    assert res.returncode == 0, res.stdout + res.stderr
    assert vault.enc.is_file()


@then("the file holds none of the generated passwords in readable form")
def nothing_readable(vault: Vault) -> None:
    """No generated password may appear in the encrypted file."""
    text = vault.enc.read_text()
    assert "ENC[AES256_GCM," in text and "sops:" in text
    for key in SECRET_KEYS_RANDOM:
        value = _decrypt_value(vault.root, vault.env, key)
        assert value not in text, f"{key} is readable in the file"


@then("the owner's key decrypts it to random 48-character passwords")
def owner_can_decrypt(vault: Vault) -> None:
    """Require distinct random 48-character passwords from the owner's key."""
    values = [
        _decrypt_value(vault.root, vault.env, key)
        for key in SECRET_KEYS_RANDOM
    ]
    assert all(
        re.fullmatch(r"[0-9a-f]{48}", value) for value in values
    ), "passwords are not 48 hex characters"
    assert len(set(values)) == len(
        values
    ), "two secrets share the same password"
    user = _decrypt_value(vault.root, vault.env, "rabbitmq-user")
    assert user and user.lower() not in WELL_KNOWN_DEFAULTS


@then("a different age key cannot decrypt it")
def stranger_cannot_decrypt(vault: Vault, tmp_path: Path) -> None:
    """Require that a key which is not a recipient cannot decrypt the file."""
    other = tmp_path / "other-key.txt"
    _new_age_key(other)
    res = run(
        ["sops", "--decrypt", str(vault.enc)],
        cwd=vault.root,
        env=_isolated_env(tmp_path, other),
    )
    assert res.returncode != 0, "a different key decrypted the file"


# ---------------------------------------------------------------- scenario 7


@given(
    "a scratch copy of the secrets tooling with a generated Secret "
    "and a fake kubectl",
    target_fixture="applying",
)
def vault_with_fake_kubectl(tmp_path: Path) -> Vault:
    """Generate a vault and put a recording fake `kubectl` on PATH."""
    vault = scratch_vault(tmp_path)
    generate_secret(vault)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    capture = tmp_path / "kubectl.stdin"
    fake = bin_dir / "kubectl"
    fake.write_text(
        f'#!/bin/sh\necho "$@" > "{capture}.args"\ncat > "{capture}"\n'
    )
    fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
    vault.env["PATH"] = f"{bin_dir}{os.pathsep}{vault.env['PATH']}"
    vault.capture = capture
    return vault


@when("I run the apply command")
def run_apply(applying: Vault) -> None:
    """Run `secrets.sh apply`, which pipes the decrypted Secret to kubectl."""
    res = run([*SECRETS_SCRIPT, "apply"], cwd=applying.root, env=applying.env)
    assert res.returncode == 0, res.stdout + res.stderr


@then("kubectl receives the decrypted Secret on stdin")
def kubectl_gets_secret(applying: Vault) -> None:
    """Require `kubectl apply -f -` to be fed the decrypted manifest."""
    assert applying.capture is not None
    sent = applying.capture.read_text()
    args = applying.capture.with_name("kubectl.stdin.args").read_text().strip()
    assert args == "apply -f -"
    assert "kind: Secret" in sent and "name: cgp-secrets" in sent
    assert (
        "ENC[AES256_GCM" not in sent
    ), "kubectl was given the ENCRYPTED manifest"
    assert re.search(r"postgres-password: [0-9a-f]{48}", sent)


@then("no decrypted copy is left on disk")
def no_plaintext_on_disk(applying: Vault) -> None:
    """Apart from the key and kubectl's capture, no file holds the password."""
    secret = _decrypt_value(applying.root, applying.env, "postgres-password")
    leaks: list[str] = []
    for path in applying.root.rglob("*"):
        if (
            not path.is_file()
            or path == applying.key
            or path.name.startswith("kubectl.stdin")
        ):
            continue
        try:
            found = secret in path.read_text(errors="ignore")
        except OSError:  # unreadable file: nothing to leak from it
            continue
        if found:
            leaks.append(str(path.relative_to(applying.root)))
    assert not leaks, f"decrypted password found on disk in: {leaks}"


# ---------------------------------------------------------------- scenario 8


@then("the encrypted cluster Secret exists for a real age recipient")
def real_secret_committed(files: list[Path]) -> None:
    """Once the owner has a key, the committed Secret must be real."""
    enc = REPO_ROOT / ENC_FILE
    config = read_text("k8s/.sops.yaml") or ""
    if not enc.is_file() or SOPS_PLACEHOLDER in config:
        pytest.skip(
            "PENDING (needs your private key, so it cannot be done for you): "
            "run `bash k8s/secrets/secrets.sh init && "
            "bash k8s/secrets/secrets.sh generate`, "
            "then commit k8s/.sops.yaml and " + ENC_FILE
        )
    recipients = [
        entry.get("recipient", "")
        for doc in yaml_docs(ENC_FILE)
        for entry in (doc.get("sops") or {}).get("age", [])
    ]
    assert recipients and all(
        r.startswith("age1") for r in recipients
    ), f"bad recipients: {recipients}"
    assert any(
        r in config for r in recipients
    ), "k8s/.sops.yaml does not list the recipient the file is encrypted for"


# ---------------------------------------------------------------- canary
# scenarios


def _canary_secret() -> dict[str, Any]:
    """Load the canary Secret, failing clearly if it was removed."""
    docs = _by_kind(yaml_docs(CANARY_FILE), "Secret")
    assert len(docs) == 1, (
        f"{CANARY_FILE} must hold exactly one Secret: it is the known-bad "
        "example that "
        "proves the checks can fail. Do not delete it."
    )
    return docs[0]


def _assert_canary_still_bad(doc: dict[str, Any]) -> None:
    """Fail unless the canary is still plaintext with a default credential."""
    verdict = _classify(doc)
    assert verdict.startswith("PLAINTEXT"), (
        f"the canary is classified as {verdict!r}: "
        "the plaintext check could no longer fail"
    )
    findings = _default_password_findings(_decoded_values(CANARY_FILE, doc))
    assert findings, (
        "the canary holds no default credential: "
        "that check could no longer fail"
    )


@given("the canary Secret kept in the test data", target_fixture="canary")
def canary_secret() -> dict[str, Any]:
    """Load the canary Secret."""
    return _canary_secret()


@then("it is a readable, unencrypted Kubernetes Secret with only fake values")
def canary_is_fake_and_readable(canary: dict[str, Any]) -> None:
    """Check the canary is readable, unencrypted and clearly fake."""
    assert "sops" not in canary, "the canary must stay unencrypted"
    values = _values(canary)
    assert values, "the canary has no values"
    decoded = _decoded_values(CANARY_FILE, canary)
    for _, key, value in decoded:
        is_default = value.strip().lower() in WELL_KNOWN_DEFAULTS
        assert is_default or value.startswith(CANARY_FAKE_PREFIX), (
            f"canary value '{key}' is neither a well-known default nor marked "
            f"{CANARY_FAKE_PREFIX}: it must not look like a real credential"
        )
    assert _default_password_findings(
        decoded
    ), "the canary needs a default password"


@then("the plaintext check classifies it as PLAINTEXT")
def canary_is_plaintext(canary: dict[str, Any]) -> None:
    """Check the plaintext check flags the canary."""
    assert _classify(canary).startswith("PLAINTEXT")


@then("the default-password check flags the default credentials in it")
def canary_has_defaults(canary: dict[str, Any]) -> None:
    """Check the default-password check flags the canary."""
    assert _default_password_findings(_decoded_values(CANARY_FILE, canary))


@when(
    "I encrypt or empty the values of a copy of the canary",
    target_fixture="sanitised_copies",
)
def sanitise_canary_copies(
    canary: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Make copies of the canary that someone has 'fixed'."""
    keys = list(_values(canary))
    base = {k: v for k, v in canary.items() if k not in ("data", "stringData")}
    return {
        "encrypted": {
            **base,
            "stringData": {
                key: "ENC[AES256_GCM,data:x,tag:y]" for key in keys
            },
            "sops": {"age": [{"recipient": "age1x"}], "mac": "m"},
        },
        "emptied": {**base, "stringData": {key: "" for key in keys}},
        "template": {**base, "stringData": {key: PLACEHOLDER for key in keys}},
        "removed": {**base, "stringData": {}},
    }


@then("the canary guard rejects that copy")
def canary_guard_rejects(sanitised_copies: dict[str, dict[str, Any]]) -> None:
    """Check the guard rejects every sanitised copy, accepts the real one."""
    _assert_canary_still_bad(_canary_secret())  # the real one passes the guard
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
def scan_skips_canary(canary: dict[str, Any]) -> None:
    """Check the real scan never reads tests/, or the canary would fail it."""
    assert_scan_skips(CANARY_FILE)


@then("the repository's own secrets check ignores it")
def secrets_check_ignores_canary(
    canary: dict[str, Any], tmp_path: Path
) -> None:
    """`secrets.sh check` must pass with the canary present (*.example)."""
    root = _scratch_tooling(tmp_path)
    assert run(["git", "init", "-q"], cwd=root).returncode == 0
    target = root / CANARY_FILE
    target.parent.mkdir(parents=True)
    shutil.copy(REPO_ROOT / CANARY_FILE, target)
    result = run([*SECRETS_SCRIPT, "check"], cwd=root)
    assert result.returncode == 0, result.stdout + result.stderr
