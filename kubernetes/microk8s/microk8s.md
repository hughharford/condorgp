# followed these instructions:
## https://microk8s.io/


# MASTER SETUP
sudo snap install microk8s --classic

sudo microk8s start
sudo microk8s status --wait-ready


>> enabled user to microk8s group






# ADD NODE
## https://microk8s.io/docs/clustering

### on master:
  microk8s add-node
  > get worker node join line, with --worker

do this on master:
sudo ufw allow 1338
sudo ufw allow 2380
sudo ufw allow 12379
sudo ufw allow 16443
sudo ufw allow 19001
sudo ufw allow 25000
sudo ufw allow 10248
sudo ufw allow 10249
sudo ufw allow 10250
sudo ufw allow 10251
sudo ufw allow 10252
sudo ufw allow 10253
sudo ufw allow 10254
sudo ufw allow 10255
sudo ufw allow 10256
sudo ufw allow 10257
sudo ufw allow 10258
sudo ufw allow 10259

sudo ufw status

this covers all the ports listed:
https://microk8s.io/docs/ports

### on node:
sudo snap install microk8s --classic

microk8s join 192.168.1.100:25000/<token> --worker


## already done, so not needed on startup:
- microk8s enable dashboard
- microk8s enable registry

# useful commands now K3S up and running
- nb 'k' is alias for microk3s kubectl



sudo microk8s start
sudo microk8s status --wait-ready



## daily, to get started

+ provide proxy for dashboard
microk8s dashboard-proxy

+ check services:
k get service cgp-database
k get service cgp-grafana
k get service cgp-rabbitmq

+ expose services to access them:
<!-- k port-forward service/cgp-database 5432:5432 -->
k port-forward statefulset/cgp-database-statefulset 5432:5432
k port-forward service/cgp-grafana 3000:3000
k port-forward service/cgp-rabbitmq 15672:15672
k port-forward service/cgp-rabbitmq 5672:5672

+ the above will timeout, can try this:
while true; do <<YOUR COMMAND HERE>>; done
with one of the commands above in the <<X>>
+ have set in:
  + /var/snap/microk8s/current/args/kubelet
  + --streaming-connection-idle-timeout=30m


+ connections strings:
rabbitmq:
  localhost:5672
cgp-database:
  - in general:
  localhost:5432
  - via DBeaver:
  jdbc:postgresql://localhost:5432/
  - SEE .envrc for Grafana connection


## refinding kubeconfig
Calico config: /var/snap/microk8s/current/args/cni-network/calico-kubeconfig
Overall at default location:
  ~/.kube/config
  // but this is kubernetes overall, not microk8s...


Note microk8s args folder and credentials folder:
  /var/snap/microk8s/current/args
    admission-control-config-file.yaml  containerd                eventconfig.yaml            k8s-dqlite-env           kubelite
    apiserver-proxy                     containerd-env            flanneld                    kube-apiserver           kube-proxy
    certs.d                             containerd-template.toml  flannel-network-mgr-config  kube-controller-manager  kube-scheduler
    cluster-agent                       containerd.toml           flannel-template.conflist   kubectl                  traefik
    cni-env                             ctr                       ha-conf                     kubectl-env
    cni-network                         etcd                      k8s-dqlite                  kubelet


  /var/snap/microk8s/current/credentials
    callback-token.txt        client.config       controller.config  proxy.config
    certs-request-tokens.txt  cluster-tokens.txt  kubelet.config     scheduler.config

# overall config
/var/snap/microk8s/current/credentials/client.config

# kubelet config
/var/snap/microk8s/current/credentials/kubelet.config
- but really:
/var/snap/microk8s/current/args/kubelet
