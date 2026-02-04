#!/usr/bin/env bash
# chatgpt provided

# set -euo pipefail

echo "🚨 Killing ALL k3d clusters..."

# Delete all k3d clusters
if k3d cluster list -o json | grep -q name; then
  k3d cluster list -o json | jq -r '.[].name' | xargs -r k3d cluster delete
else
  echo "No k3d clusters found."
fi

echo "🧹 Removing leftover k3d Docker containers..."
docker ps -aq --filter "name=k3d-" | xargs -r docker rm -f

echo "🧹 Removing k3d Docker networks..."
docker network ls -q --filter "name=k3d" | xargs -r docker network rm

echo "🧹 Removing k3d Docker volumes..."
docker volume ls -q --filter "name=k3d" | xargs -r docker volume rm

echo "✅ k3d cleanup complete."
