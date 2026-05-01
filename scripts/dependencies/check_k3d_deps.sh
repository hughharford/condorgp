#!/usr/bin/env bash

set -euo pipefail

MIN_K3D_VERSION="5.6.0"
MIN_KUBECTL_VERSION="1.30.0"

has_failed=0

log_ok() {
  echo "[ok] $1"
}

log_fail() {
  echo "[fail] $1"
  has_failed=1
}

version_ge() {
  local current="$1"
  local minimum="$2"
  [ "$(printf '%s\n' "$minimum" "$current" | sort -V | head -n1)" = "$minimum" ]
}

extract_semver() {
  local value="$1"
  echo "$value" | sed -E 's/^v//' | sed -E 's/[^0-9.].*$//'
}

check_binary() {
  local bin_name="$1"
  local install_hint="$2"
  if command -v "$bin_name" >/dev/null 2>&1; then
    log_ok "$bin_name is installed"
  else
    log_fail "$bin_name is missing. Install hint: $install_hint"
  fi
}

check_binary "docker" "https://docs.docker.com/engine/install/"
check_binary "k3d" "https://k3d.io/stable/#installation"
check_binary "kubectl" "https://kubernetes.io/docs/tasks/tools/"

if command -v docker >/dev/null 2>&1; then
  if docker info >/dev/null 2>&1; then
    log_ok "docker daemon is reachable"
  else
    log_fail "docker is installed but daemon is not reachable/running"
  fi
fi

if command -v k3d >/dev/null 2>&1; then
  k3d_version_raw="$(k3d version | sed -n 's/.*k3d version v\([0-9.]*\).*/\1/p' | head -n1)"
  k3d_version="$(extract_semver "${k3d_version_raw:-0.0.0}")"
  if version_ge "$k3d_version" "$MIN_K3D_VERSION"; then
    log_ok "k3d version $k3d_version (min $MIN_K3D_VERSION)"
  else
    log_fail "k3d version $k3d_version is below minimum $MIN_K3D_VERSION"
  fi
fi

if command -v kubectl >/dev/null 2>&1; then
  kubectl_version_raw="$(kubectl version --client -o json 2>/dev/null | sed -n 's/.*"gitVersion":[[:space:]]*"\(v[^"]*\)".*/\1/p' | head -n1)"
  kubectl_version="$(extract_semver "${kubectl_version_raw:-0.0.0}")"
  if version_ge "$kubectl_version" "$MIN_KUBECTL_VERSION"; then
    log_ok "kubectl version $kubectl_version (min $MIN_KUBECTL_VERSION)"
  else
    log_fail "kubectl version $kubectl_version is below minimum $MIN_KUBECTL_VERSION"
  fi
fi

if [ "$has_failed" -ne 0 ]; then
  echo ""
  echo "k3d dependency preflight failed."
  exit 1
fi

echo ""
echo "k3d dependency preflight passed."
