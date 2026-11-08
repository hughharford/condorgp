# Secrets management for the CondorGP cluster

Secrets are stored in this repository **encrypted** with [SOPS](https://github.com/getsops/sops)
using [age](https://github.com/FiloSottile/age) keys. Only the encrypted file is committed; the
private key never is. Deployment decrypts in memory and pipes straight into `kubectl`.

Why this and not base64: a Kubernetes `Secret` manifest only *encodes* values (base64), it does not
protect them. Anything committed that way is public in a public repo.

Why SOPS + age: no component to run inside the cluster, identical behaviour on k3s, microk8s and
microk8s, and secrets stay portable if you rebuild or move clusters. (Alternatives are noted at the
end.)

---

## What lives where

| Item | Location | Committed? |
|---|---|---|
| age **private** key | `~/.config/sops/age/keys.txt` (or `$SOPS_AGE_KEY_FILE`) | **Never.** Back it up (see below) |
| age **public** key(s) = recipients | `k8s/.sops.yaml` | Yes |
| Encrypted Secret | `k8s/02-secrets.enc.yaml` | Yes |
| Template (shape only, `CHANGEME`) | `k8s/02-secrets.example.yaml` | Yes |
| Helper script | `k8s/secrets/secrets.sh` | Yes |
| Decrypted values at runtime | Secret `cgp-secrets` in namespace `cgp-system` | n/a (cluster only) |

Keys in the Secret: `postgres-password`, `app-db-pass`, `rabbitmq-user`, `rabbitmq-pass`,
`grafana-admin-password`. Key names, namespace and metadata stay readable in the encrypted file;
only the values are encrypted, so code review and diffs still work.

---

## Prerequisites

```bash
# age (Ubuntu 22.04+; otherwise see the age releases page)
sudo apt install age

# sops: download a pinned release and verify it against the checksums file on the release page
curl -LO https://github.com/getsops/sops/releases/download/v3.9.4/sops-v3.9.4.linux.amd64
sudo install -m 0755 sops-v3.9.4.linux.amd64 /usr/local/bin/sops
sops --version
```

You also need `kubectl` pointed at the target cluster and `openssl` (present on most systems).

---

## First-time setup (once per person/machine)

```bash
# 1. Create your age key and put its public half into k8s/.sops.yaml
bash k8s/secrets/secrets.sh init

# 2. BACK UP THE PRIVATE KEY NOW (see "Key custody"). If it is lost, the encrypted
#    secrets are unrecoverable and every credential must be regenerated.

# 3. Generate the encrypted Secret with fresh random values (nothing is printed)
bash k8s/secrets/secrets.sh generate

# 4. Commit the public config and the encrypted file (both are safe to push)
git add k8s/.sops.yaml k8s/02-secrets.enc.yaml
git commit -m "Add SOPS-encrypted cluster secrets"

# 5. Deploy (the apply scripts call `secrets.sh apply` for you)
make k3_kapply        # k3s     (uses KUBECTL="k3s kubectl")
make k_apply          # microk8s (uses KUBECTL="microk8s kubectl"; the Makefile passes your
                      #   age key path through sudo, because sudo changes $HOME)
```

`generate` creates 192-bit random passwords, and uses RabbitMQ user `cgp-mq` rather than the
well-known `guest`.

### Key custody

- The private key file is the single point of trust. Treat it like an SSH private key (`chmod 600`,
  which `init` sets).
- Keep **two copies in two places**: your password manager (paste the whole file) and an offline
  copy (encrypted USB or printed in a safe). Test the restore once: copy the key to another
  machine and run `bash k8s/secrets/secrets.sh get rabbitmq-user`.
- Better still, add a second **recipient** (a separate backup key kept offline) so losing one key is
  survivable. See "Adding or removing a recipient".
- Never put the key in the repo, in a ConfigMap, in CI logs, or in chat/e-mail.

---

## Day-to-day use

| Task | Command |
|---|---|
| Read one value (e.g. to log in to Grafana) | `bash k8s/secrets/secrets.sh get grafana-admin-password` |
| Change values | `bash k8s/secrets/secrets.sh edit` (opens `$EDITOR`, re-encrypts on save) |
| Apply to the current cluster | `bash k8s/secrets/secrets.sh apply` |
| Check nothing plaintext is committed | `bash k8s/secrets/secrets.sh check` |

Environment variables sourced from a Secret are read **at pod start only**. After changing a value
and applying, restart whatever consumes it:

```bash
kubectl -n cgp-system rollout restart deploy/cgp-rabbitmq deploy/cgp-master deploy/cgp-worker-1
```

Run `get` only when you need the value; it prints to the terminal (and your scrollback).

---

## Rotating credentials

Changing a value in the Secret changes what the *pods are told*. For stateful services it does not
change what the *service already has stored*, so the service must be changed too.

| Credential | How |
|---|---|
| `rabbitmq-user` / `rabbitmq-pass` | RabbitMQ has no persistent volume here, so users are recreated from the Secret at every start. `edit` -> `apply` -> restart `cgp-rabbitmq`, then master and workers. |
| `postgres-password` | The init script runs **only on an empty data volume**, so a new value does not change an existing database. Change it in Postgres first: `kubectl -n cgp-system exec -it deploy/cgp-database -- psql -U postgres`, then at the prompt `\password postgres` (type or paste the new value twice). Then `edit` the same value into the Secret, `apply`, restart consumers. |
| `app-db-pass` | Same as above, for the application role: `\password <app user>` (the role name is `APP_DB_USER` from `cgp-config`). |
| `grafana-admin-password` | The env var only applies when Grafana first creates its database. For an existing `grafana-data` volume: Grafana UI -> Profile -> Change password, or `kubectl -n cgp-system exec deploy/cgp-grafana -- grafana cli admin reset-admin-password '<new>'`. Then `edit` the same value into the Secret. |
| SOPS data key (routine hygiene) | `sops rotate -i k8s/02-secrets.enc.yaml` re-encrypts with a new data key (recipients unchanged). |

Rotate on a schedule you will actually keep (for example every 6-12 months) and always after anyone
with access leaves.

---

## Adding or removing a recipient

Recipients are the age public keys in `k8s/.sops.yaml`. List several, comma separated:

```yaml
    age: >-
      age1firstpublickey...,
      age1secondpublickey...
```

After editing, re-wrap the encrypted file so the new set of keys applies:

```bash
sops --config k8s/.sops.yaml updatekeys k8s/02-secrets.enc.yaml
```

Get someone's public key with `age-keygen -y <their keyfile>` (the public key is safe to send).

**Removing a recipient does not revoke what they could already read.** Older versions of the file
remain in git history and can still be decrypted with their old key. After removing anyone,
treat all values as exposed to them: `generate --force` (or `edit`) new values and rotate them in
each service per the table above.

---

## If a key or a value leaks

1. Treat every value in the Secret as compromised.
2. Create a new age key (`age-keygen -o newkey.txt`), put its public key in `k8s/.sops.yaml`
   (replacing the compromised recipient), keep the new private key per "Key custody".
3. `bash k8s/secrets/secrets.sh generate --force` for fresh values.
4. Rotate each credential in its service (table above), `apply`, restart consumers.
5. Check Postgres/Grafana/RabbitMQ logs for use of the old credentials.
6. Only then consider scrubbing git history (see below); rotation is the actual remediation.

---

## Cluster-level secrets (k3s)

These are not application secrets but are just as sensitive.

**Encrypt Secrets at rest.** By default Kubernetes Secrets sit unencrypted in the cluster datastore
(SQLite/etcd) and in its backups. On a **new** cluster, enable it before first start in
`/etc/rancher/k3s/config.yaml` on each server:

```yaml
secrets-encryption: true
```

For an **existing** cluster follow the procedure in the k3s docs (enable, restart, `k3s
secrets-encrypt rotate-keys`, wait for `reencrypt_finished`; needs a recent k3s release). Check
state with `k3s secrets-encrypt status`. This protects the datastore and backups on disk; it does
not stop someone who already has API access. The encryption keys live on the server node under
`/var/lib/rancher/k3s/server/`, so snapshot backups must be protected like secrets themselves.

**Join tokens (hub-and-spoke).**

- The **server token** (`/var/lib/rancher/k3s/server/token`) can join servers *and* agents and
  grants full administrator access. It is also the passphrase protecting bootstrap data.
- The **agent token** (`/var/lib/rancher/k3s/server/agent-token`) joins agents only. **By default it
  is the same as the server token**, which would mean every spoke holds the hub's admin credential.
  Set a separate one on the hub (`agent-token-file: /etc/rancher/k3s/agent-token` in `config.yaml`)
  and give spokes only that.
- Put tokens in files with mode `0600` and reference them with `token-file` /
  `agent-token-file` in `config.yaml` (or `K3S_TOKEN_FILE` / `K3S_AGENT_TOKEN_FILE`). Avoid
  `K3S_TOKEN=... sh` on the command line: it lands in shell history and the process list.
- Never paste tokens into notes, docs, logs or chat (the old `k3s_1st_attempt.md` workflow of
  copying them around is how they leak).
- Rotate with `k3s token rotate --token <old> --new-token <new>` on a server, then restart every
  server and every agent that joined with the old token using the new one. Backups taken before a
  rotation need the **old** server token to restore.

**Kubeconfig.** k3s writes `/etc/rancher/k3s/k3s.yaml` with mode 600; keep it that way
(never use `--write-kubeconfig-mode 644`; see `kubernetes/k3s_again/k3s_hub_spoke.md`). Copy it to your own `~/.kube/config` and `chmod 600` it. A
kubeconfig is a credential; never commit one.

**kubeadm bootstrap tokens** (from the earlier kubeadm attempt): they expire after 24 hours by
default. A token appeared in `docs/OLD/kubernetes/k8s_too_complex/log_inc_kubadm_init.txt`; it is now
redacted. On any cluster still running from that attempt run `kubeadm token list` and
`kubeadm token delete <id>` for anything listed, or `kubeadm reset` if the cluster is abandoned.

**Docker Swarm join tokens** (from the overlay-network experiment): a worker token was committed in
`docker_compose/old/docker_network/docker_networking_overlay_n_swarm.md`, together with the
manager's address. It is now redacted, but it is in the public git history, so treat it as leaked.
On any swarm that is still running, run `docker swarm join-token --rotate worker` (and `manager`).
If the swarm is abandoned, `docker swarm leave --force` on every node removes it. Swarm tokens
grant the same kind of access as the k3s tokens above: never commit them.

**Automated guard.** `python -m pytest -m B_tokens` fails if a kubeadm, k3s or Swarm token, a CA
hash or a certificate key is committed with a real value (placeholders such as `<TOKEN>` and
`REDACTED` are fine). It also scans files that are not yet `git add`-ed.

---

## Guardrails (keep it from happening again)

1. **Local check** - `bash k8s/secrets/secrets.sh check` fails if a Kubernetes `Secret` manifest
   that is not SOPS-encrypted is in the repo (templates named `*.example.yaml` are exempt). Run it
   before pushing, or install it as a hook:

   ```bash
   printf '#!/bin/sh\nexec bash k8s/secrets/secrets.sh check\n' > .git/hooks/pre-commit
   chmod +x .git/hooks/pre-commit
   ```

2. **CI** - add this step to a GitHub Actions job (after checkout):

   ```yaml
   - name: No plaintext Kubernetes secrets
     run: bash k8s/secrets/secrets.sh check
   ```

3. **GitHub secret scanning and push protection** - free for public repositories; enable under
   Settings -> Code security. It blocks many token and key formats at push time.
4. **A general scanner** such as `gitleaks` as a pre-commit hook catches credentials the check above
   can't (for example passwords inside ConfigMaps, scripts or notes).
5. `.gitignore` already excludes `*.dec.yaml`, `*.plain.yaml`, age key files, kubeconfigs, join
   token files (`node-token`, `agent-token`, `*.token`) and `admin.conf`; use those names if you ever
   decrypt or copy a credential to a file, and delete the file afterwards.
6. **The BDD guards** - `python -m pytest -m A_secrets` and `-m B_tokens` (see `tests/features/017_*`
   and `018_*`) check all of the above, including a real encrypt/decrypt round trip.

---

## Credentials already exposed

The previous manifests committed these defaults: Postgres `postgres`/`postgres`, application
password `cgp-pass`, RabbitMQ `guest`/`guest`, Grafana `admin`/`admin`; and
`k8s/01-configmap.yaml` contains a literal `cgp:cgp-pass` in `POSTGRES_DATABASE_URL`. They are in
git history of a public repository, so treat them as public forever.

**The fix is rotation**, not deletion: after `generate`, change each credential inside any existing
Postgres/Grafana volume as described in "Rotating credentials". Fresh clusters need nothing extra
(the new values are used from first start).

Scrubbing history is optional and has real costs: it rewrites every commit hash, needs a force
push, every collaborator must re-clone, and forks and caches keep the old data anyway. If you still
want to, work on a fresh clone and keep a backup:

```bash
pip install git-filter-repo
git filter-repo \
  --path k8s/02-secrets.yaml \
  --path k8s/microk8s/microk8s_yaml_n_sh/02-secrets.yaml \
  --path k8s/k3d/k3d_yaml/02-secrets-k3d.yaml \
  --invert-paths
```

---

## Known limits and open items

- `k8s/01-configmap.yaml` is **not** encrypted and ConfigMaps are not a place for
  credentials. It still contains `${...}` placeholders (including `POSTGRES_PASSWORD` and
  `APP_DB_PASS`) and the literal URL mentioned above; this is intentionally untouched pending a
  decision on how those values are injected.
- microk8s and k3s share the manifests in `k8s/`. The plaintext `k8s/02-secrets.yaml` was removed;
  the apply scripts and Makefile now run `secrets.sh apply` instead (`KUBECTL` selects k3s or microk8s).
- One recipient means one person/key to lose. Add a second, offline recipient.
- Alternatives considered: **Sealed Secrets** (a controller in the cluster; `kubeseal` encrypts
  with the cluster's public key, which suits a Git-only workflow but ties ciphertext to one cluster
  and requires backing up the controller key) and **External Secrets / Vault** (right at larger
  scale, heavy for one operator). SOPS + age is the smallest approach that fixes the problem today
  and is easy to move off later.
