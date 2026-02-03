# echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
## NB first time k3d is setup, run this to ensure ip forwarding on

# k3d cluster create first-cluster -p 8080:31080@server:0
# k3d cluster create dashboard-cluster --api-port 6550 -p "8080:80@loadbalancer" --agents 2

export CLUSTER_NAME=cgp-cluster

echo $LOCAL_PATH

# delete pattern
k3d cluster delete $CLUSTER_NAME
k3d registry delete k3d-cgp-registry.localhost
docker network rm k3d-cgp-cluster


# create
k3d registry create cgp-registry.localhost --port 30123
k3d cluster create $CLUSTER_NAME \
        --api-port 6550 \
        -p "8080:80@loadbalancer" --agents 2 \
        --registry-use k3d-cgp-registry.localhost:30123 \
#       --volume $LOCAL_PATH:/condorgp/

# export KUBECONFIG="$(k3d kubeconfig get cgp-cluster)"                              [🐍 3.12.0]
# echo $KUBECONFIG

kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
kubectl create serviceaccount dashboard-admin
kubectl create clusterrolebinding dashboard-admin --clusterrole=cluster-admin --serviceaccount=default:dashboard-admin
kubectl create token dashboard-admin
# get token




sleep 30
kubectl port-forward -n kubernetes-dashboard service/kubernetes-dashboard 8443:443 --address 0.0.0.0
# https://localhost:8443
