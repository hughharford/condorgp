### was using this:


# set the cluster server and check (must match --api-port in cluster create, e.g. 6550)
kubectl config set-cluster k3d-cgp-cluster --server=https://127.0.0.1:6550
kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}{"\n"}'
curl -k https://127.0.0.1:6550/version


# use this once the cluster is created to ensure gefyra uses the right setup:
kubectl config view --raw --minify > /tmp/gefyra-kubeconfig.yaml
grep -n '^ *server:' /tmp/gefyra-kubeconfig.yaml


# this eventually worked:
env -i HOME="$HOME" PATH="$PATH" KUBECONFIG=/tmp/gefyra-kubeconfig.yaml gefyra install --apply --wait


# create and setup gefyra client
env -i HOME="$HOME" PATH="$PATH" KUBECONFIG=/tmp/gefyra-kubeconfig.yaml \
  gefyra clients create --client-id local

env -i HOME="$HOME" PATH="$PATH" KUBECONFIG=/tmp/gefyra-kubeconfig.yaml \
  gefyra clients config local -h 172.19.0.1 -p 31820 -o /tmp/gefyra-local.json


## NOTE: 172.19.0.1 comes via:
docker exec -it k3d-cgp-cluster-server-0 sh -lc "ip route | awk '/default/ {print \$3; exit}'"


# then attempted:
gefyra connections connect -f /tmp/gefyra-local.json -n cgp-system
