### was using this:


# set the cluster server and check (must match --api-port in cluster create, e.g. 6550)
kubectl config set-cluster k3d-cgp-cluster --server=https://127.0.0.1:6550
kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}{"\n"}'
curl -k https://127.0.0.1:6550/version


# use this once the cluster is created to ensure gefyra uses the right setup:
kubectl config view --raw --minify > "$HOME/.kube/gefyra-kubeconfig.yaml"
grep -n '^ *server:' "$HOME/.kube/gefyra-kubeconfig.yaml"


# this eventually worked:
env -i HOME="$HOME" PATH="$PATH" KUBECONFIG="$HOME/.kube/gefyra-kubeconfig.yaml" gefyra install --apply --wait


# create and setup gefyra client
env -i HOME="$HOME" PATH="$PATH" KUBECONFIG="$HOME/.kube/gefyra-kubeconfig.yaml" \
  gefyra clients create --client-id local

env -i HOME="$HOME" PATH="$PATH" KUBECONFIG="$HOME/.kube/gefyra-kubeconfig.yaml" \
  gefyra clients config local -h 172.19.0.1 -p 31820 -o "$HOME/.kube/gefyra-local.json"


## NOTE: 172.19.0.1 comes via:
docker exec -it k3d-cgp-cluster-server-0 sh -lc "ip route | awk '/default/ {print \$3; exit}'"


# then attempted:
gefyra connections connect -f "$HOME/.kube/gefyra-local.json" -n cgp-system


## local dev without rebuild/push

# start a long-running dev container with local repo bind-mounted:
make gefyra_dev_shell

# then open shell in that container and run anything you need:
docker exec -it worker-dev bash
# examples in container:
#   cd /condorgp
#   python condorgp/cgp_rabbitmq/delegate/run_delegated_evals_4_w_strat.py
#   pytest tests/...

# this is the core "edit/develop" loop:
#   1) edit code locally in IDE
#   2) rerun commands in the same container shell
#   3) no image rebuild/push

# quick visible demo endpoint in cluster context:
make gefyra_dev_local_http

# override command if needed:
DETACH=0 DEV_CMD="python condorgp/cgp_rabbitmq/sample_consumer.py" bash k8s/k3d/gefyra_dev_worker.sh
