#!/bin/bash
# Build kubeconfig with dashboard token for k3d cgp-cluster.
# The dashboard runs in-cluster and needs server: https://kubernetes.default.svc
# plus token-based auth (it does not support X.509 for kubeconfig upload).
set -e

KUBECONFIG_PATH="${K3D_KUBECONFIG:-/tmp/k3d-cgp-kubeconfig.yaml}"
TMP_CONFIG="/tmp/k3d-cgp-kubeconfig-tmp.yaml"

# 1. Get k3d kubeconfig
k3d kubeconfig get cgp-cluster > "$TMP_CONFIG"

# 2. Fix host server URL (k3d may give 172.x:6443; we need 127.0.0.1:6550)
# 3. Extract CA for in-cluster cluster
export KUBECONFIG="$TMP_CONFIG"
kubectl config set-cluster k3d-cgp-cluster --server=https://127.0.0.1:6550 --kubeconfig="$TMP_CONFIG"

# 4. Generate dashboard token
TOKEN=$(kubectl create token dashboard-admin --duration=8760h 2>/dev/null || kubectl create token dashboard-admin)

# 5. Add token user and in-cluster cluster + context for dashboard
#    Dashboard runs in-cluster; it needs server: https://kubernetes.default.svc
#    kubectl set-cluster only accepts --certificate-authority=path, so write CA to temp file
CA_FILE=$(mktemp)
kubectl config view --raw -o jsonpath='{.clusters[0].cluster.certificate-authority-data}' --kubeconfig="$TMP_CONFIG" | base64 -d > "$CA_FILE"

kubectl config set-credentials dashboard-admin --token="$TOKEN" --kubeconfig="$TMP_CONFIG"
kubectl config set-cluster k3d-cgp-cluster-internal \
  --server=https://kubernetes.default.svc \
  --certificate-authority="$CA_FILE" \
  --embed-certs \
  --kubeconfig="$TMP_CONFIG"
rm -f "$CA_FILE"
kubectl config set-context dashboard-admin \
  --cluster=k3d-cgp-cluster-internal \
  --user=dashboard-admin \
  --kubeconfig="$TMP_CONFIG"
kubectl config use-context dashboard-admin --kubeconfig="$TMP_CONFIG"

cp "$TMP_CONFIG" "$KUBECONFIG_PATH"
rm -f "$TMP_CONFIG"

echo ""
echo "=== Kubernetes Dashboard ==="
echo "Kubeconfig: $KUBECONFIG_PATH"
echo "  - Context 'dashboard-admin': in-cluster API (https://kubernetes.default.svc) + token"
echo "  - Context 'k3d-cgp-cluster': host API (127.0.0.1:6550) + cert auth"
echo "  - current-context: dashboard-admin (for Kubeconfig upload)"
echo ""
echo "URL: https://localhost:8443"
echo ""
echo "Token (paste when prompted for Token login):"
echo "$TOKEN"
echo ""
echo "Starting port-forward (Ctrl+C to stop)..."
KUBECONFIG="$KUBECONFIG_PATH" kubectl port-forward -n kubernetes-dashboard service/kubernetes-dashboard 8443:443 --address 0.0.0.0 --context=k3d-cgp-cluster
