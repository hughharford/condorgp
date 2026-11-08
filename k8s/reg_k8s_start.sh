
microk8s start

# Wait for MicroK8s to be ready
microk8s status --wait-ready

# Enable necessary addons
microk8s enable dns
microk8s enable storage
microk8s enable ingress
microk8s enable registry
# (dashboard addon removed: it installs the retired Kubernetes Dashboard v2.x. Use Headlamp: make k_dash)

