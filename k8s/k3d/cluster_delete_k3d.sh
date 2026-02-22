
export CLUSTER_NAME=cgp-cluster
export REGISTRY_NAME=cgp-registry

# delete pattern
k3d cluster stop cgp-cluster
k3d cluster stop k3s-default

# k3d registry delete k3d-cgp-registry.localhost
# this might not be required, and would speed up restart

docker network rm k3d-cgp-cluster
docker network rm k3d-k3s-default
docker system prune

k3d cluster delete cgp-cluster
k3d cluster delete k3s-default

sudo fuser -k 6550/tcp
sudo fuser -k 8080/tcp
sudo fuser -k 6443/tcp
sudo fuser -k 8443/tcp

rm -f $(docker ps -af label=k3d.io -q)
