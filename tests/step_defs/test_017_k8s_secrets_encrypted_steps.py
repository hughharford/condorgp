import base64
import os
import re
import shutil
import stat

import pytest
from pytest_bdd import scenarios, given, when, then

from tests.k8s_helpers import REPO_ROOT, fmt_hits, is_git_ignored, read_text, run, yaml_docs

scenarios("../features/017_k8s_secrets_encrypted.feature")

SECRET_KIND = re.compile(r"(?m)^kind:\s*Secret\s*$")
PLACEHOLDER = "CHANGEME"
WELL_KNOWN_DEFAULTS = {"postgres", "cgp-pass", "cgp_pass", "guest", "admin", "password"}
ENC_FILE = "k8s/02-secrets.enc.yaml"
TEMPLATE_FILE = "k8s/02-secrets.example.yaml"
SOPS_PLACEHOLDER = "AGE_PUBLIC_KEY_NOT_SET"
SECRET_KEYS_RANDOM = ["postgres-password", "app-db-pass", "rabbitmq-pass", "grafana-admin-password"]


def _values(doc):
    return {**(doc.get("data") or {}), **(doc.get("stringData") or {})}


def _is_enc(value):
    return str(value).startswith("ENC[AES256_GCM,")


def _need(*tools):
    missing = [t for t in tools if not shutil.which(t)]
    if missing:
        pytest.skip(f"needs {', '.join(missing)} on PATH (see kubernetes/secrets_management.md, Prerequisites)")


def _scratch_tooling(tmp_path):
    """Copy the secrets script (and sops config) into an empty dir so tests never touch the repo."""
    script = REPO_ROOT / "k8s/secrets/secrets.sh"
    assert script.is_file(), "k8s/secrets/secrets.sh is missing"
    (tmp_path / "k8s/secrets").mkdir(parents=True)
    shutil.copy(script, tmp_path / "k8s/secrets/secrets.sh")
    config = REPO_ROOT / "k8s/.sops.yaml"
    assert config.is_file(), "k8s/.sops.yaml is missing"
    shutil.copy(config, tmp_path / "k8s/.sops.yaml")
    return tmp_path


def _isolated_env(tmp_path, key_file):
    """Environment that can only ever see the throwaway key, never the user's real one."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("SOPS_")}
    env["HOME"] = str(tmp_path)
    env["SOPS_AGE_KEY_FILE"] = str(key_file)
    return env


def _new_age_key(path):
    res = run(["age-keygen", "-o", str(path)])
    assert res.returncode == 0, res.stderr
    path.chmod(0o600)


def _decrypt_value(root, env, key):
    res = run(["bash", "k8s/secrets/secrets.sh", "get", key], cwd=root, env=env)
    assert res.returncode == 0, f"could not read {key}: {res.stderr}"
    return res.stdout.strip()


# ---------------------------------------------------------------- scenarios 1-2


@when("I list the Kubernetes Secret manifests", target_fixture="secrets")
def list_secret_manifests(files):
    found = []
    for rel in files:
        if rel.suffix not in (".yaml", ".yml"):
            continue
        text = read_text(rel)
        if not text or not SECRET_KIND.search(text):
            continue
        docs = [d for d in yaml_docs(rel) if d.get("kind") == "Secret"]
        found += [(str(rel), d) for d in docs] or [(str(rel), {"_unparseable": True})]
    return found


def _classify(doc):
    if doc.get("_unparseable"):
        return "PLAINTEXT? (YAML could not be parsed, so it cannot be shown safe)"
    values = _values(doc)
    if "sops" in doc:
        return "encrypted" if all(_is_enc(v) for v in values.values()) else "PLAINTEXT (sops block but readable values)"
    if all(str(v).strip() == "" for v in values.values()):
        return "empty shell"  # e.g. the Dashboard's own Secrets, which it fills in itself
    if all(str(v).strip() == PLACEHOLDER for v in values.values()):
        return "template"
    return "PLAINTEXT"


@then("every Secret is SOPS-encrypted, an empty shell or a CHANGEME template")
def secrets_are_safe(secrets):
    bad = [f"  {rel}: {_classify(doc)}" for rel, doc in secrets if _classify(doc).startswith("PLAINTEXT")]
    assert not bad, "Committed Secret manifests with readable values:\n" + "\n".join(bad)


@when("I decode the values of every Secret manifest", target_fixture="decoded")
def decode_secret_values(files):
    decoded = []
    for rel in files:
        if rel.suffix not in (".yaml", ".yml"):
            continue
        for doc in yaml_docs(rel):
            if doc.get("kind") != "Secret":
                continue
            for key, value in (doc.get("data") or {}).items():
                try:
                    value = base64.b64decode(str(value), validate=True).decode("utf-8")
                except Exception:
                    value = str(value)
                decoded.append((str(rel), key, value))
            for key, value in (doc.get("stringData") or {}).items():
                decoded.append((str(rel), key, str(value)))
    return decoded


@then("none of them is a well-known default password")
def no_default_passwords(decoded):
    bad = [f"  {rel}: {key}" for rel, key, value in decoded if value.strip().lower() in WELL_KNOWN_DEFAULTS]
    assert not bad, "Secrets still hold default credentials (these are in the public git history, so rotate them):\n" + "\n".join(bad)


# ---------------------------------------------------------------- scenario 3


@when("I list the SOPS-encrypted files", target_fixture="enc_files")
def list_encrypted_files(files):
    return [rel for rel in files if re.search(r"\.enc\.ya?ml$", str(rel))]


@then("each one has SOPS metadata and only ENC tokens as values")
def encrypted_files_are_encrypted(enc_files):
    problems = []
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
                    problems.append(f"  {rel}: value of '{key}' is not an ENC[...] token")
    assert not problems, "\n".join(problems)


# ---------------------------------------------------------------- scenario 4


@given("the repository ignore rules")
def ignore_rules():
    assert (REPO_ROOT / ".gitignore").is_file()


@then("age keys, decrypted copies and kubeconfigs are ignored")
def secrets_paths_ignored():
    must_ignore = [
        "keys.txt",
        "k8s/secrets/age-key.txt",
        "backup.agekey",
        "k8s/02-secrets.dec.yaml",
        "k8s/02-secrets.plain.yaml",
        "k3s.yaml",
        "kubeconfig",
        "hub.kubeconfig",
    ]
    leaking = [p for p in must_ignore if not is_git_ignored(p)]
    assert not leaking, f".gitignore would NOT stop these being committed: {leaking}"


@then("the encrypted Secret and the CHANGEME template are not ignored")
def encrypted_and_template_not_ignored():
    wrongly = [p for p in (ENC_FILE, TEMPLATE_FILE) if is_git_ignored(p)]
    assert not wrongly, f".gitignore would hide files that must be committed: {wrongly}"


# ---------------------------------------------------------------- scenario 5


@given("a scratch git repository using the repo's secrets script", target_fixture="scratch")
def scratch_repo(tmp_path):
    root = _scratch_tooling(tmp_path)
    assert run(["git", "init", "-q"], cwd=root).returncode == 0
    return root


@when("I add a plaintext Secret manifest and run the secrets check", target_fixture="check_result")
def add_plaintext_and_check(scratch):
    (scratch / "oops.yaml").write_text(
        "apiVersion: v1\nkind: Secret\nmetadata:\n  name: x\nstringData:\n  password: hunter2\n"
    )
    return run(["bash", "k8s/secrets/secrets.sh", "check"], cwd=scratch)


@then("the check fails and names the plaintext file")
def check_fails(check_result):
    assert check_result.returncode != 0, "check passed although a plaintext Secret is present"
    assert "oops.yaml" in check_result.stdout + check_result.stderr


@then("the check passes again once the plaintext Secret is removed")
def check_passes_after_removal(scratch):
    (scratch / "oops.yaml").unlink()
    res = run(["bash", "k8s/secrets/secrets.sh", "check"], cwd=scratch)
    assert res.returncode == 0, res.stdout + res.stderr


# ---------------------------------------------------------------- scenario 6


@given("a scratch copy of the secrets tooling and a throwaway age key", target_fixture="vault")
def scratch_vault(tmp_path):
    _need("sops", "age-keygen", "openssl")
    root = _scratch_tooling(tmp_path)
    key = tmp_path / "owner-key.txt"
    _new_age_key(key)
    env = _isolated_env(tmp_path, key)
    res = run(["bash", "k8s/secrets/secrets.sh", "init"], cwd=root, env=env)
    assert res.returncode == 0, res.stdout + res.stderr
    return {"root": root, "env": env, "key": key, "enc": root / ENC_FILE}


@when("I generate the encrypted Secret")
def generate_secret(vault):
    res = run(["bash", "k8s/secrets/secrets.sh", "generate"], cwd=vault["root"], env=vault["env"])
    assert res.returncode == 0, res.stdout + res.stderr
    assert vault["enc"].is_file()


@then("the file holds none of the generated passwords in readable form")
def nothing_readable(vault):
    text = vault["enc"].read_text()
    assert "ENC[AES256_GCM," in text and "sops:" in text
    for key in SECRET_KEYS_RANDOM:
        assert _decrypt_value(vault["root"], vault["env"], key) not in text, f"{key} is readable in the file"


@then("the owner's key decrypts it to random 48-character passwords")
def owner_can_decrypt(vault):
    values = [_decrypt_value(vault["root"], vault["env"], k) for k in SECRET_KEYS_RANDOM]
    assert all(re.fullmatch(r"[0-9a-f]{48}", v) for v in values), "passwords are not 48 hex characters"
    assert len(set(values)) == len(values), "two secrets share the same password"
    user = _decrypt_value(vault["root"], vault["env"], "rabbitmq-user")
    assert user and user.lower() not in WELL_KNOWN_DEFAULTS


@then("a different age key cannot decrypt it")
def stranger_cannot_decrypt(vault, tmp_path):
    other = tmp_path / "other-key.txt"
    _new_age_key(other)
    res = run(["sops", "--decrypt", str(vault["enc"])], cwd=vault["root"], env=_isolated_env(tmp_path, other))
    assert res.returncode != 0, "a different key decrypted the file"


# ---------------------------------------------------------------- scenario 7


@given("a scratch copy of the secrets tooling with a generated Secret and a fake kubectl", target_fixture="applying")
def vault_with_fake_kubectl(tmp_path):
    vault = scratch_vault(tmp_path)
    generate_secret(vault)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    capture = tmp_path / "kubectl.stdin"
    fake = bin_dir / "kubectl"
    fake.write_text(f'#!/bin/sh\necho "$@" > "{capture}.args"\ncat > "{capture}"\n')
    fake.chmod(fake.stat().st_mode | stat.S_IXUSR)
    vault["env"]["PATH"] = f"{bin_dir}{os.pathsep}{vault['env']['PATH']}"
    vault["capture"] = capture
    return vault


@when("I run the apply command")
def run_apply(applying):
    res = run(["bash", "k8s/secrets/secrets.sh", "apply"], cwd=applying["root"], env=applying["env"])
    assert res.returncode == 0, res.stdout + res.stderr


@then("kubectl receives the decrypted Secret on stdin")
def kubectl_gets_secret(applying):
    sent = applying["capture"].read_text()
    assert applying["capture"].with_name("kubectl.stdin.args").read_text().strip() == "apply -f -"
    assert "kind: Secret" in sent and "name: cgp-secrets" in sent
    assert "ENC[AES256_GCM" not in sent, "kubectl was given the ENCRYPTED manifest"
    assert re.search(r"postgres-password: [0-9a-f]{48}", sent)


@then("no decrypted copy is left on disk")
def no_plaintext_on_disk(applying):
    secret = _decrypt_value(applying["root"], applying["env"], "postgres-password")
    leaks = []
    for path in applying["root"].rglob("*"):
        if not path.is_file() or path == applying["key"] or path.name.startswith("kubectl.stdin"):
            continue
        try:
            if secret in path.read_text(errors="ignore"):
                leaks.append(str(path.relative_to(applying["root"])))
        except OSError:
            pass
    assert not leaks, f"decrypted password found on disk in: {leaks}"


# ---------------------------------------------------------------- scenario 8


@then("the encrypted cluster Secret exists for a real age recipient")
def real_secret_committed(files):
    enc = REPO_ROOT / ENC_FILE
    config = read_text("k8s/.sops.yaml") or ""
    if not enc.is_file() or SOPS_PLACEHOLDER in config:
        pytest.skip(
            "PENDING (needs your private key, so it cannot be done for you): run "
            "`bash k8s/secrets/secrets.sh init && bash k8s/secrets/secrets.sh generate`, "
            "then commit k8s/.sops.yaml and " + ENC_FILE
        )
    recipients = [r.get("recipient", "") for d in yaml_docs(ENC_FILE) for r in (d.get("sops") or {}).get("age", [])]
    assert recipients and all(r.startswith("age1") for r in recipients), f"bad recipients: {recipients}"
    assert any(r in config for r in recipients), "k8s/.sops.yaml does not list the recipient the file is encrypted for"
