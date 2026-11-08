#!/usr/bin/env bash
# secrets.sh - manage SOPS + age encrypted Kubernetes secrets for CondorGP.
#
#   bash k8s/secrets/secrets.sh init            one-off: create your age key, set the recipient
#   bash k8s/secrets/secrets.sh generate        create the encrypted Secret with fresh random values
#   bash k8s/secrets/secrets.sh get <key>       print one decrypted value (e.g. grafana-admin-password)
#   bash k8s/secrets/secrets.sh edit            edit the encrypted Secret in $EDITOR
#   bash k8s/secrets/secrets.sh apply           decrypt and `kubectl apply` into the current cluster
#                                               (KUBECTL="k3s kubectl" or KUBECTL="microk8s kubectl" to pick one)
#   bash k8s/secrets/secrets.sh check           fail if a plaintext Kubernetes Secret is in the repo
#
# Full guide: kubernetes/secrets_management.md
#
# Plaintext never touches disk here: values are generated in memory and piped
# straight into sops, and `apply` pipes the decrypted manifest straight to kubectl.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SOPS_CONFIG="$REPO_ROOT/k8s/.sops.yaml"
SECRETS_ENC="${CGP_SECRETS_FILE:-$REPO_ROOT/k8s/02-secrets.enc.yaml}"
PLACEHOLDER="AGE_PUBLIC_KEY_NOT_SET"
KUBECTL="${KUBECTL:-kubectl}"
export SOPS_AGE_KEY_FILE="${SOPS_AGE_KEY_FILE:-$HOME/.config/sops/age/keys.txt}"

# Files that legitimately contain `kind: Secret` with no real values, as paths relative
# to the repo root. Empty: the retired Kubernetes Dashboard manifest that needed an
# entry here was replaced by Headlamp, which has no Secret objects.
CHECK_ALLOWLIST=()

die()  { echo "ERROR: $*" >&2; exit 1; }
need() { command -v "$1" >/dev/null 2>&1 || die "'$1' not found. See kubernetes/secrets_management.md (Prerequisites)."; }

recipient_configured() {
  [ -f "$SOPS_CONFIG" ] && ! grep -q "$PLACEHOLDER" "$SOPS_CONFIG"
}

cmd_init() {
  need age-keygen
  need sops
  [ -f "$SOPS_CONFIG" ] || die "$SOPS_CONFIG is missing"

  if [ ! -f "$SOPS_AGE_KEY_FILE" ]; then
    ( umask 077; mkdir -p "$(dirname "$SOPS_AGE_KEY_FILE")"; age-keygen -o "$SOPS_AGE_KEY_FILE" 2>/dev/null )
    chmod 600 "$SOPS_AGE_KEY_FILE"
    echo "Created a new age private key: $SOPS_AGE_KEY_FILE"
    echo "  >>> BACK THIS FILE UP NOW (password manager / offline copy)."
    echo "  >>> If it is lost, every encrypted secret in this repo is unrecoverable."
  else
    echo "Using existing age key: $SOPS_AGE_KEY_FILE"
  fi

  local pub
  pub="$(age-keygen -y "$SOPS_AGE_KEY_FILE" | head -n1)"
  [ -n "$pub" ] || die "could not read a public key from $SOPS_AGE_KEY_FILE"

  if grep -q "$PLACEHOLDER" "$SOPS_CONFIG"; then
    sed "s|$PLACEHOLDER|$pub|" "$SOPS_CONFIG" > "$SOPS_CONFIG.tmp" && mv "$SOPS_CONFIG.tmp" "$SOPS_CONFIG"
    echo "Set recipient in $SOPS_CONFIG to: $pub"
    echo "Commit that file (public key only). Next: bash k8s/secrets/secrets.sh generate"
  elif grep -q "$pub" "$SOPS_CONFIG"; then
    echo "Your public key is already a recipient in $SOPS_CONFIG. Nothing to do."
  else
    echo "WARNING: $SOPS_CONFIG already lists other recipient(s) and not this key:"
    echo "  $pub"
    echo "To be able to decrypt, ask a current key holder to add it and run 'sops updatekeys'."
  fi
}

cmd_generate() {
  need sops
  need openssl
  recipient_configured || die "no age recipient set. Run: bash k8s/secrets/secrets.sh init"
  if [ -e "$SECRETS_ENC" ] && [ "${1:-}" != "--force" ]; then
    die "$SECRETS_ENC already exists. Use 'edit' to change values.
       --force regenerates ALL values, but note: new passwords do NOT change an
       existing Postgres/Grafana volume. See 'Rotating credentials' in the guide."
  fi

  rand() { openssl rand -hex 24; }   # 48 hex chars, 192 bits

  mkdir -p "$(dirname "$SECRETS_ENC")"
  cat <<EOF | sops --config "$SOPS_CONFIG" --encrypt \
        --input-type yaml --output-type yaml \
        --filename-override "$SECRETS_ENC" /dev/stdin > "$SECRETS_ENC.tmp"
apiVersion: v1
kind: Secret
metadata:
  name: cgp-secrets
  namespace: cgp-system
type: Opaque
stringData:
  postgres-password: $(rand)
  app-db-pass: $(rand)
  rabbitmq-user: cgp-mq
  rabbitmq-pass: $(rand)
  grafana-admin-password: $(rand)
EOF
  mv "$SECRETS_ENC.tmp" "$SECRETS_ENC"
  echo "Wrote encrypted secrets: ${SECRETS_ENC#"$REPO_ROOT"/}"
  echo "Values were not displayed. Read one with: bash k8s/secrets/secrets.sh get grafana-admin-password"
  echo "Commit the .enc.yaml file; it is safe to push."
}

cmd_get() {
  [ -n "${1:-}" ] || die "usage: secrets.sh get <key>   (e.g. grafana-admin-password)"
  need sops
  [ -f "$SECRETS_ENC" ] || die "$SECRETS_ENC not found"
  sops --decrypt --extract "[\"stringData\"][\"$1\"]" "$SECRETS_ENC"
  echo
}

cmd_edit() {
  need sops
  [ -f "$SECRETS_ENC" ] || die "$SECRETS_ENC not found. Run: bash k8s/secrets/secrets.sh generate"
  sops --config "$SOPS_CONFIG" "$SECRETS_ENC"
}

cmd_apply() {
  need sops
  # shellcheck disable=SC2086  # KUBECTL may be several words, e.g. "microk8s kubectl"
  need ${KUBECTL%% *}
  [ -f "$SECRETS_ENC" ] || die "$SECRETS_ENC not found. Run: bash k8s/secrets/secrets.sh generate"
  # shellcheck disable=SC2086
  sops --decrypt "$SECRETS_ENC" | $KUBECTL apply -f -
}

cmd_check() {
  local bad=0 f rel allowed a
  while IFS= read -r -d '' f; do
    rel="${f#"$REPO_ROOT"/}"
    case "$rel" in *.example.yaml|*.example.yml) continue ;; esac
    allowed=0
    # ${arr[@]+...} keeps an empty array legal under `set -u` on bash < 4.4 (macOS ships 3.2)
    for a in ${CHECK_ALLOWLIST[@]+"${CHECK_ALLOWLIST[@]}"}; do [ "$rel" = "$a" ] && allowed=1; done
    [ "$allowed" = 1 ] && continue
    if grep -qE '^kind:[[:space:]]*Secret[[:space:]]*$' "$f" && ! grep -qE '^sops:' "$f"; then
      echo "PLAINTEXT SECRET (not sops-encrypted): $rel" >&2
      bad=1
    fi
  done < <(cd "$REPO_ROOT" && git ls-files -z --cached --others --exclude-standard -- '*.yaml' '*.yml' | sed -z "s|^|$REPO_ROOT/|")
  if [ "$bad" = 1 ]; then
    echo "Encrypt it (see kubernetes/secrets_management.md) or rename a template to *.example.yaml." >&2
    exit 1
  fi
  echo "OK: no plaintext Kubernetes Secret manifests found."
}

case "${1:-}" in
  init)     shift; cmd_init "$@" ;;
  generate) shift; cmd_generate "$@" ;;
  get)      shift; cmd_get "$@" ;;
  edit)     shift; cmd_edit "$@" ;;
  apply)    shift; cmd_apply "$@" ;;
  check)    shift; cmd_check "$@" ;;
  *) sed -n '2,13p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 1 ;;
esac
