# Quick connect (assumes Gefyra already installed and client configured):
# For full setup from scratch, use: make k3d_gefyra  OR  sh k8s/k3d/gefyra_setup.sh

# Optional test workload:
# kubectl apply -f k8s/k3d/k3d_yaml/000-gefyra-basic-workload.yaml

# Regenerate kubeconfig and connect (when operator + client already exist)
kubectl config view --raw --minify > /tmp/gefyra-kubeconfig.yaml
kubectl config set-cluster k3d-cgp-cluster --server=https://127.0.0.1:6550 --kubeconfig=/tmp/gefyra-kubeconfig.yaml

GATEWAY_IP=$(docker exec k3d-cgp-cluster-server-0 sh -lc "ip route | awk '/default/ {print \$3; exit}'" 2>/dev/null || echo "172.17.0.1")
env -i HOME="$HOME" PATH="$PATH" KUBECONFIG=/tmp/gefyra-kubeconfig.yaml \
  gefyra clients config local -h "$GATEWAY_IP" -p 31820 -o /tmp/gefyra-local.json

env -i HOME="$HOME" PATH="$PATH" KUBECONFIG=/tmp/gefyra-kubeconfig.yaml \
  gefyra clients config local -h 172.19.0.1 -p 31820 -o /tmp/gefyra-local.json

# this will fail as cgp already created:
# gefyra connections connect -f /tmp/gefyra-local.json -n cgp
# so:
gefyra connections connect -n cgp
