
microk8s start

# Wait for MicroK8s to be ready
microk8s status --wait-ready

# Enable necessary addons
microk8s enable dns
microk8s enable storage
microk8s enable ingress
microk8s enable registry
microk8s enable dashboard

# copy images
export CGP_WORKER_IMAGE_NAME="cgp-nt-again"
microk8s ctr image import ../hughharford/00_LOCAL_IMAGES/${CGP_WORKER_IMAGE_NAME}.tar

# microk8s kubectl describe secret -n kube-system microk8s-dashboard-token

microk8s dashboard-proxy
