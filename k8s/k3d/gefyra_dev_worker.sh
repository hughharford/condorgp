#!/bin/bash
#
# Run a persistent Gefyra dev container with local code mounted.
# Edit code locally in the IDE; the container sees updates immediately.
# Requires an active Gefyra connection to cgp-system.
#
# Usage examples:
#   bash k8s/k3d/gefyra_dev_worker.sh
#   bash k8s/k3d/gefyra_dev_worker.sh
#   DETACH=0 DEV_CMD="python k8s/k3d/gefyra/local.py 2727" bash k8s/k3d/gefyra_dev_worker.sh
#   DEV_CONTAINER_NAME=worker-dev-2 bash k8s/k3d/gefyra_dev_worker.sh

# If invoked via "sh", re-exec with bash so pipefail works.
if [ -z "${BASH_VERSION:-}" ]; then
  exec bash "$0" "$@"
fi

set -euo pipefail

KUBECONFIG_FILE="${KUBECONFIG_FILE:-$HOME/.kube/gefyra-kubeconfig.yaml}"
NAMESPACE="${NAMESPACE:-cgp-system}"
CONNECTION_NAME="${CONNECTION_NAME:-cgp-system}"
DEV_CONTAINER_NAME="${DEV_CONTAINER_NAME:-worker-dev}"
IMAGE="${IMAGE:-k3d-cgp-registry.localhost:30123/cgp-nt-again}"
WORKSPACE="${WORKSPACE:-$(pwd)}"
MOUNT_PATH="${MOUNT_PATH:-/condorgp}"
DEV_CMD="${DEV_CMD:-sleep infinity}"
DETACH="${DETACH:-1}"

echo "Starting Gefyra dev container:"
echo "  name: $DEV_CONTAINER_NAME"
echo "  namespace: $NAMESPACE"
echo "  image: $IMAGE"
echo "  mount: $WORKSPACE -> $MOUNT_PATH"
echo "  command: $DEV_CMD"
echo "  detach: $DETACH"
echo ""

GEFYRA_ARGS=(
  -N "$DEV_CONTAINER_NAME"
  -n "$NAMESPACE"
  --connection-name "$CONNECTION_NAME"
  -i "$IMAGE"
  -v "$WORKSPACE:$MOUNT_PATH"
  -c "$DEV_CMD"
)

if [ "$DETACH" = "1" ]; then
  KUBECONFIG="$KUBECONFIG_FILE" gefyra run -d "${GEFYRA_ARGS[@]}"
  echo ""
  echo "Dev container started in background."
  echo "Edit files locally and run commands inside it with:"
  echo "  docker exec -it $DEV_CONTAINER_NAME bash"
  echo "Stop it with:"
  echo "  docker rm -f $DEV_CONTAINER_NAME"
else
  KUBECONFIG="$KUBECONFIG_FILE" gefyra run --rm "${GEFYRA_ARGS[@]}"
fi
