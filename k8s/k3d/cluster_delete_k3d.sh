
export CLUSTER_NAME=cgp-cluster
export REGISTRY_NAME=cgp-registry

# delete pattern
k3d cluster stop cgp-cluster

k3d registry delete k3d-cgp-registry.localhost
# k3d registry delete k3d-$REGISTRY_NAME.localhost
docker network rm k3d-cgp-cluster
docker system prune

k3d cluster delete cgp-cluster

sudo fuser -k 6550/tcp
sudo fuser -k 8080/tcp
sudo fuser -k 6443/tcp
sudo fuser -k 8443/tcp

rm -f $(docker ps -af label=k3d.io -q)
