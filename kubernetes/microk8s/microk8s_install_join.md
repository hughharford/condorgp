# followed these instructions:
## https://microk8s.io/

# uninstalling and resetting
### REF: https://microk8s.io/docs/command-reference#heading--microk8s-reset

microk8s kubectl get nodes
k get nodes

### on master only:
+ by ip, or by node name:
  microk8s remove-node 10.128.63.163
  microk8s remove-node cgp02.local
+ then, still on master
  sudo microk8s reset --destroy-storage
+ on nodes
  sudo microk8s leave
+ actually uninstall (potentially optional, but to be sure)
  sudo snap remove microk8s


# MASTER SETUP
sudo snap install microk8s --classic
+ gives:
    microk8s (1.31/stable) v1.31.5 from Canonical✓ installed

# first attempt:
+ current version: MicroK8s v1.31.5 revision 7661
+ therefore
/snap/microk8s/7661/

sudo microk8s start
sudo microk8s status --wait-ready


>> enabled user to microk8s group


# ADD NODE
## https://microk8s.io/docs/clustering

### on master:
  microk8s add-node
  > get worker node join line, with --worker


### on node:
sudo snap install microk8s --classic

microk8s join 192.168.1.100:25000/<token> --worker


## already done, so not needed on startup:
microk8s enable dashboard
microk8s enable registry
microk8s enable dns
+ https://microk8s.io/docs/addon-dns

# useful commands now K3S up and running
- nb 'k' is alias for microk3s kubectl



sudo microk8s start
sudo microk8s status --wait-ready
