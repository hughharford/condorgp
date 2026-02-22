#!/bin/bash
# Full Gefyra setup for k3d - run after cluster is up (use w_reg_n_api_reg_start_k3d.sh)
# Requires: cluster created with -p 31820:31820/UDP@agent:1 and --api-port 6550
set -e

KUBECONFIG_FILE="/tmp/gefyra-kubeconfig.yaml"
CLIENT_JSON="/tmp/gefyra-local.json"
CLIENT_ID="local"
NAMESPACE="${GEFYRA_NAMESPACE:-cgp-system}"   # K8s namespace to bridge (workloads in cgp-system)
K8S_API_PORT=6550    # Kubernetes API - for kubectl/gefyra CLI
WIREGUARD_PORT=31820 # WireGuard UDP - for VPN tunnel (passed to clients config -p)

# 1. Kubeconfig: must use K8s API port (6550), not WireGuard port (31820)
#    Cluster must be created with --tls-san=127.0.0.1 so cert matches (see w_reg_n_api_reg_start_k3d.sh)
kubectl config view --raw --minify > "$KUBECONFIG_FILE"
kubectl config set-cluster k3d-cgp-cluster \
  --server="https://127.0.0.1:${K8S_API_PORT}" \
  --kubeconfig="$KUBECONFIG_FILE"
echo "Kubeconfig: $KUBECONFIG_FILE (API server: 127.0.0.1:${K8S_API_PORT}, TLS verify enabled)"

# 2. Install Gefyra operator (LoadBalancer needed for k3d host access)
echo "Installing Gefyra operator..."
env -i HOME="$HOME" PATH="$PATH" KUBECONFIG="$KUBECONFIG_FILE" \
  gefyra install --apply --wait --service-type=LoadBalancer
# Brief wait for operator to create service accounts / WireGuard endpoint
sleep 5

# 3. Get Docker gateway (IP that host uses to reach cluster nodes)
GATEWAY_IP=$(docker exec k3d-cgp-cluster-server-0 sh -lc "ip route | awk '/default/ {print \$3; exit}'" 2>/dev/null || true)
if [ -z "$GATEWAY_IP" ]; then
  echo "WARNING: Could not get gateway IP from k3d node. Using 172.17.0.1 as fallback."
  GATEWAY_IP="172.17.0.1"
fi
echo "Using gateway IP for WireGuard: $GATEWAY_IP"

# 4. Create and configure client
echo "Configuring Gefyra client..."
env -i HOME="$HOME" PATH="$PATH" KUBECONFIG="$KUBECONFIG_FILE" \
  gefyra clients create --client-id "$CLIENT_ID" 2>/dev/null || true

env -i HOME="$HOME" PATH="$PATH" KUBECONFIG="$KUBECONFIG_FILE" \
  gefyra clients config "$CLIENT_ID" -h "$GATEWAY_IP" -p "$WIREGUARD_PORT" -o "$CLIENT_JSON"

# Remove any existing connection (e.g. from previous failed run); ignore if none exists
env -i HOME="$HOME" PATH="$PATH" KUBECONFIG="$KUBECONFIG_FILE" \
  gefyra connections remove "$NAMESPACE" 2>/dev/null || true

# 5. Connect to namespace (-n is K8s namespace to bridge, e.g. where cgp-worker lives)
echo "Connecting to namespace $NAMESPACE..."
env -i HOME="$HOME" PATH="$PATH" KUBECONFIG="$KUBECONFIG_FILE" \
  gefyra connections connect -f "$CLIENT_JSON" -n "$NAMESPACE"

echo "=== Gefyra connected to $NAMESPACE ==="
echo ""
echo "For other gefyra commands (list, status), use: KUBECONFIG=$KUBECONFIG_FILE gefyra ..."
