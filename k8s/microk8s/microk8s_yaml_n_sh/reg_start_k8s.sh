
microk8s start

# Wait for MicroK8s to be ready
microk8s status --wait-ready

# Enable necessary addons
microk8s enable dns
microk8s enable storage
microk8s enable hostpath-storage
microk8s enable ingress
microk8s enable registry
microk8s enable dashboard
# microk8s enable rbac

# microk8s kubectl describe secret -n kube-system microk8s-dashboard-token

microk8s dashboard-proxy --token-ttl=43200
# makes for 12 hour timeout
