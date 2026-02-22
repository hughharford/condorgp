# REFS:
https://palark.com/blog/small-local-kubernetes-comparison/
Half decent comparisons
No more needed

https://brettmostert.medium.com/k3d-kubernetes-up-and-running-quickly-d80f47bab48e
Useful starting point, many obvious simple commands
Refer to this as needed

https://www.sokube.io/en/blog/k3s-k3d-k8s-a-new-perfect-match-for-dev-and-test-en
Goes into a reasonable amount of detail, e.g. replacing ingress controller etc


https://medium.com/@nklokanatha/getting-started-with-k3d-9e2228666ce7
Likely useful

on environment variables from a .env file
https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-via-file/


# API
apiVersion: k3d.io/v1alpha3

# CONFIG NATIVE:
/home/hsth/.config/k3d/kubeconfig-cgp-cluster.yaml


# MANUALLY RESET CERTIFICATION CERTS
k3d cluster create --volume /path/to/your/certs.crt:/etc/ssl/certs/yourcert.crt

kubeadm certs check-expiration
kubeadm certs renew all
systemctl restart kubelet


# PREREQUISITES

## NB first time k3d is setup, run this to ensure ip forwarding on
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
# NB this is not quite enough, see IPTABLES ISSUE BELOW


# EARLY ERRORS
Error response from daemon: add inter-network communication rule

ERRO[0000] Failed Cluster Preparation: Failed Network Preparation: failed to create cluster network: docker failed to create new network 'k3d-first-cluster': Error response from daemon: add inter-network communication rule:  (iptables failed: iptables --wait -t filter -A DOCKER-ISOLATION-STAGE-1 -i br-257eedbd73c2 ! -o br-257eedbd73c2 -j DOCKER-ISOLATION-STAGE-2: iptables v1.8.10 (nf_tables): Chain 'DOCKER-ISOLATION-STAGE-2' does not exist
Try `iptables -h' or 'iptables --help' for more information.
 (exit status 2))

# IPTABLES ISSUE:
please can you suggest the iptables line that is required to allow k3d to operate, somehow it's been changed

Here are the iptables-related fixes that usually resolve this k3d/Docker error.
1. Restart Docker (first step)
Docker creates the DOCKER-ISOLATION chains when it starts. If they’re missing or broken, restart Docker so it recreates them:
sudo systemctl restart docker
2. Switch to iptables-legacy - DID NOT APPLY THIS
If you see iptables v1.8.10 (nf_tables), you’re using the nftables backend. Docker has had issues with this. Force iptables-legacy:
sudo update-alternatives --set iptables /usr/sbin/iptables-legacysudo update-alternatives --set ip6tables /usr/sbin/ip6tables-legacysudo systemctl restart docker
3. IP forwarding (from your notes)
k3d needs IP forwarding enabled:
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
To make it persistent:
# Add to /etc/sysctl.conf or create /etc/sysctl.d/99-k3d.confnet.ipv4.ip_forward = 1
Then: sudo sysctl -p
4. Manually create chains (only if restart doesn’t work)
If Docker still fails to create the chains, you can create them in the filter table:
sudo iptables -t filter -N DOCKER-ISOLATION-STAGE-1 2>/dev/null || truesudo iptables -t filter -N DOCKER-ISOLATION-STAGE-2 2>/dev/null || truesudo iptables -t filter -A DOCKER-ISOLATION-STAGE-1 -j RETURNsudo iptables -t filter -A DOCKER-ISOLATION-STAGE-2 -j RETURN
Then retry creating the k3d cluster. This can work if the chains were flushed but the FORWARD rules that reference them are still present.
Recommended order: try (1), then (2) if needed, and keep (3) in place. Use (4) only if Docker restart and iptables-legacy do not help.


# DOCKER MUST BE LESS THAN 28 to work
See specific version instal here:
https://docs.docker.com/engine/install/ubuntu/
And post installation steps here:



# DASHBOARD KUBECONFIG (Kubeconfig login)
# The dashboard runs in-cluster; uploaded kubeconfig must have:
#   - cluster.server: https://kubernetes.default.svc (reachable from dashboard pod)
#   - user with token (dashboard does NOT support X.509 cert for kubeconfig upload)
#   - context linking cluster + user
#   - current-context set
# See dash_kubeconfig.sh for the full structure.

# DASHBOARD CLUSTER
k3d cluster create dashboard-cluster --api-port 6550 -p "8080:80@loadbalancer" --agents 2

kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
kubectl create serviceaccount dashboard-admin
kubectl create clusterrolebinding dashboard-admin --clusterrole=cluster-admin --serviceaccount=default:dashboard-admin
kubectl create token dashboard-admin

kubectl port-forward -n kubernetes-dashboard service/kubernetes-dashboard 8443:443 --address 0.0.0.0
https://localhost:8443



# TLS for host access (127.0.0.1)
# k3s API cert does not include 127.0.0.1 by default -> SSL verify fails.
# Fix: add --tls-san when creating cluster (see w_reg_n_api_reg_start_k3d.sh):
#   --k3s-arg "--tls-san=127.0.0.1@server:0" --k3s-arg "--tls-san=localhost@server:0"