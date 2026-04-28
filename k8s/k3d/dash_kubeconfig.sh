#!/bin/bash
# Build kubeconfig with dashboard token for k3d cgp-cluster.
# The dashboard runs in-cluster and needs server: https://kubernetes.default.svc
# plus token-based auth (it does not support X.509 for kubeconfig upload).
set -e

KUBECONFIG_PATH="${K3D_KUBECONFIG:-$HOME/.kube/k3d-dashboard.yaml}"
CLUSTER_NAME="k3d-cgp-cluster"
HOST_API_SERVER="https://127.0.0.1:6550"

# 1. Get k3d kubeconfig
mkdir -p "$(dirname "$KUBECONFIG_PATH")"
k3d kubeconfig get cgp-cluster > "$KUBECONFIG_PATH"

# 2. Fix host server URL (k3d may give 172.x:6443; we need 127.0.0.1:6550)
#    Also pin TLS server name to 127.0.0.1 to avoid mismatches with rotated 172.x node IPs.
kubectl --kubeconfig="$KUBECONFIG_PATH" config set-cluster "$CLUSTER_NAME" \
  --server="$HOST_API_SERVER" \
  --tls-server-name=127.0.0.1
echo "Kubeconfig host API fixed to $HOST_API_SERVER"

# 3. Extract CA for in-cluster cluster

# 4. Generate dashboard token
TOKEN=$(kubectl --kubeconfig="$KUBECONFIG_PATH" create token dashboard-admin --duration=8760h 2>/dev/null || kubectl --kubeconfig="$KUBECONFIG_PATH" create token dashboard-admin)

# 5. Add token user and in-cluster cluster + context for dashboard
#    Dashboard runs in-cluster; it needs server: https://kubernetes.default.svc
#    kubectl set-cluster only accepts --certificate-authority=path, so write CA to temp file
CA_FILE=$(mktemp)
kubectl --kubeconfig="$KUBECONFIG_PATH" config view --raw -o jsonpath="{.clusters[?(@.name=='$CLUSTER_NAME')].cluster.certificate-authority-data}" | base64 -d > "$CA_FILE"

kubectl --kubeconfig="$KUBECONFIG_PATH" config set-credentials dashboard-admin --token="$TOKEN"
kubectl --kubeconfig="$KUBECONFIG_PATH" config set-cluster k3d-cgp-cluster-internal \
  --server=https://kubernetes.default.svc \
  --certificate-authority="$CA_FILE" \
  --embed-certs
rm -f "$CA_FILE"
kubectl --kubeconfig="$KUBECONFIG_PATH" config set-context dashboard-admin \
  --cluster=k3d-cgp-cluster-internal \
  --user=dashboard-admin
kubectl --kubeconfig="$KUBECONFIG_PATH" config use-context dashboard-admin
chmod 600 "$KUBECONFIG_PATH"

echo ""
echo "=== Kubernetes Dashboard ==="
echo "Kubeconfig: $KUBECONFIG_PATH"
echo "  - Context 'dashboard-admin': in-cluster API (https://kubernetes.default.svc) + token"
echo "  - Context 'k3d-cgp-cluster': host API (127.0.0.1:6550) + cert auth"
echo "  - current-context: dashboard-admin (for Kubeconfig upload, if needed)"
echo "  - Dashboard deployment enables skip-login for local dev"
echo ""
echo "URL: https://localhost:8443"
echo ""
echo "Stored token (fallback, if prompted):"
echo "$TOKEN"
echo ""
echo "Starting port-forward (Ctrl+C to stop)..."
KUBECONFIG="$KUBECONFIG_PATH" kubectl port-forward -n kubernetes-dashboard service/kubernetes-dashboard 8443:443 --address 0.0.0.0 --context=k3d-cgp-cluster
