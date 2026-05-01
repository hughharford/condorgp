#!/usr/bin/env bash

set -euo pipefail

if ! command -v apt-get >/dev/null 2>&1; then
  echo "Unsupported package manager. Use manual installs for docker, kubectl, and k3d."
  exit 1
fi

echo "Installing k3d packages..."
sudo apt-get update
sudo apt-get install -y curl ca-certificates gnupg lsb-release

if ! command -v kubectl >/dev/null 2>&1; then
  echo "Installing kubectl..."
  sudo snap install kubectl --classic
else
  echo "kubectl already installed."
fi

if ! command -v k3d >/dev/null 2>&1; then
  echo "Installing k3d..."
  curl -s https://raw.githubusercontent.com/k3d-io/k3d/main/install.sh | bash
else
  echo "k3d already installed."
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is not installed. Install Docker Engine manually:"
  echo "https://docs.docker.com/engine/install/"
else
  echo "docker already installed."
fi

echo "Bootstrap finished. Run: make k3d_check"
echo " "
echo " "
echo " "
