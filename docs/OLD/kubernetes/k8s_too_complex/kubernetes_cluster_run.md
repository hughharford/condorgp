# step by step

follow these instructions
https://cavecafe.medium.com/setup-homelab-kubernetes-cluster-cfc3acd4dca5

except gpg and repository, which needs more up to date
from:
https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/

include this line after kublet kubeadm and kubectl installs:

sudo systemctl enable --now kubelet

Configure the cgroup driver
https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/configure-cgroup-driver/
must include:
  kubeadm init --config kubeadm-config.yaml

so kubeadm init:

sudo kubeadm init --control-plane-endpoint=cgp.k8s.local --ignore-preflight-errors=all



# issue? as this fails:
                            nc 127.0.0.1 6443 -v
YET:
sudo iptables -L | grep 6443
 does show ACCEPT tcp



# this shortened version of the init runs better
sudo kubeadm init



mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config


kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.25.0/manifests/calico.yaml
