# echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
## NB first time k3d is setup, run this to ensure ip forwarding on

# k3d cluster create first-cluster -p 8080:31080@server:0
# k3d cluster create dashboard-cluster --api-port 6550 -p "8080:80@loadbalancer" --agents 2

export CLUSTER_NAME=cgp-cluster
export REGISTRY_NAME=cgp-registry

echo $LOCAL_PATH

echo "Ensuring ip forwarding is on..."
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward


# create
k3d registry create $REGISTRY_NAME.localhost --port 30123
k3d cluster create $CLUSTER_NAME \
        --api-port 6550 \
        --registry-use k3d-$REGISTRY_NAME.localhost:30123 \
        --agents 2 -p 8080:80@agent:0 -p 31820:31820/UDP@agent:1 \
        --k3s-arg "--tls-san=127.0.0.1@server:0" \
        --k3s-arg "--tls-san=localhost@server:0"


# kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
kubectl apply -f k8s/k3d/k3d_yaml/000-kubernetes-dashboard.yaml
kubectl create serviceaccount dashboard-admin
kubectl create clusterrolebinding dashboard-admin --clusterrole=cluster-admin --serviceaccount=default:dashboard-admin

# kubectl create token dashboard-admin
# get token

# added to ensure server set:
kubectl config set-cluster k3d-cgp-cluster --server=https://127.0.0.1:6550
kubectl config view --raw --minify > /tmp/gefyra-kubeconfig.yaml

# sleep 30
# kubectl port-forward -n kubernetes-dashboard service/kubernetes-dashboard 8443:443 --address 0.0.0.0
# https://localhost:8443
