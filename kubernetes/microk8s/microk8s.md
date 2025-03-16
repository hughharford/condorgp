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

# install kubectl
https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/


# MASTER SETUP
sudo snap install microk8s --classic

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

# useful commands now K3S up and running
- nb 'k' is alias for microk3s kubectl



sudo microk8s start;
sudo microk8s status --wait-ready


# getting latest code loaded into cluster
- until things settle down
- until mounts are working
- >> rebuild the container, this copies the latest code in
DOCKER_BUILDKIT=1 docker build -f docker/Dockerfile_nt_builder --target=cgp_nt_theirs_plus -t cgp-w .

SEE: https://microk8s.io/docs/registry-images
check with:
  microk8s ctr images ls | grep cgp

save file with:
  docker save cgp-w > ../00_LOCAL_IMAGES/cgp-w.tar

import image with:
  microk8s ctr image import ../00_LOCAL_IMAGES/cgp-w.tar

# with cgp-nt-again
docker save cgp-nt-again > ../00_LOCAL_IMAGES/cgp-nt-again.tar;
microk8s ctr image import ../00_LOCAL_IMAGES/cgp-nt-again.tar



## daily, to get started
+ provide proxy for dashboard
microk8s dashboard-proxy --request-timeout='0'

+ check services:
k get service cgp-database -n cgp-system
k get service cgp-grafana -n cgp-system
k get service cgp-rabbitmq -n cgp-system

+ expose services to access them:
k port-forward service/cgp-database  -n cgp-system 5432:5432
k port-forward statefulset/cgp-database-statefulset 5432:5432 --request-timeout='0'
k port-forward pod/cgp-database-statefulset-0 5432:5432 --request-timeout='0'


k port-forward service/cgp-grafana 3000:3000  -n cgp-system --request-timeout='0'
k port-forward service/cgp-rabbitmq 15672:15672  -n cgp-system --request-timeout='0'
k port-forward service/cgp-rabbitmq 5672:5672  -n cgp-system --request-timeout='0'

# delete and reapply services
## RMQ
k delete -f kubernetes/2/062-cgp-rabbitmq-service.yaml -f kubernetes/2/061-cgp-rabbitmq-deployment.yaml

k apply -f kubernetes/2/062-cgp-rabbitmq-service.yaml -f kubernetes/2/061-cgp-rabbitmq-deployment.yaml

# DB:
### Latest on database:
- still available on any node, so often needs some of the following:
- exec into pod and
- psql --user=postgres
- CREATE DATABASE cgpbackbone;
- alembic upgrade head
k delete -f kubernetes/2db/020-cgp-database-service.yaml -f kubernetes/2db/021-cgp-database-statefulset.yaml -f kubernetes/2db/022-cgp-database-cm0-configmap.yaml -f kubernetes/2db/023-cgp-database-pv.yaml -f kubernetes/2db/024-cgp-database-pvc.yaml

k apply -f kubernetes/2db/020-cgp-database-service.yaml -f kubernetes/2db/021-cgp-database-statefulset.yaml -f kubernetes/2db/022-cgp-database-cm0-configmap.yaml -f kubernetes/2db/023-cgp-database-pv.yaml -f kubernetes/2db/024-cgp-database-pvc.yaml

## lwb postgres...
k apply -f kubernetes/2_db_lwb/postgres-pv.yaml
k apply -f kubernetes/2_db_lwb/postgres-pvc.yaml
k apply -f kubernetes/2_db_lwb/postgres-secret.yaml
k apply -f kubernetes/2_db_lwb/postgres-service-cluster-ip.yaml
k apply -f kubernetes/2_db_lwb/postgres-service-load-balancer.yaml
k apply -f kubernetes/2_db_lwb/postgres-statefulset.yaml

k apply -f kubernetes/2_db_lwb/postgres-pv.yaml
k apply -f kubernetes/2_db_lwb/postgres-pvc.yaml
k apply -f kubernetes/2_db_lwb/postgres-secret.yaml
k apply -f kubernetes/2_db_lwb/postgres-service.yaml
k apply -f kubernetes/2_db_lwb/postgres-statefulset.yaml

k delete -f kubernetes/2_db_lwb/postgres-pv.yaml
k delete -f kubernetes/2_db_lwb/postgres-pvc.yaml
k delete -f kubernetes/2_db_lwb/postgres-secret.yaml
k delete -f kubernetes/2_db_lwb/postgres-service.yaml
k delete -f kubernetes/2_db_lwb/postgres-statefulset.yaml

# CGP worker
k apply -f kubernetes/010-cgp-worker-1-service.yaml
k apply -f kubernetes/011-cgp-worker-1-cm0-configmap.yaml
k apply -f kubernetes/012-cgp-worker-pv.yaml
k apply -f kubernetes/013-cgp-worker-pvc.yaml
k apply -f kubernetes/014-cgp-pod-vol-bind.yaml
+ k apply -f kubernetes/015-cgp-pod-vol-bind_sample_c.yaml

k delete -f kubernetes/010-cgp-worker-1-service.yaml
k delete -f kubernetes/011-cgp-worker-1-cm0-configmap.yaml
k delete -f kubernetes/012-cgp-worker-pv.yaml
k delete -f kubernetes/013-cgp-worker-pvc.yaml
k delete -f kubernetes/014-cgp-pod-vol-bind.yaml

# Grafana
k apply -f kubernetes/3graf/050-cgp-grafana-service.yaml -f kubernetes/3graf/051-cgp-grafana-deployment.yaml -f kubernetes/3graf/053-cgp-grafana-env-configmap.yaml -f kubernetes/3graf/054-cgp-grafana-cm0-configmap.yaml

k delete -f kubernetes/3graf/050-cgp-grafana-service.yaml -f kubernetes/3graf/051-cgp-grafana-deployment.yaml -f kubernetes/3graf/053-cgp-grafana-env-configmap.yaml -f kubernetes/3graf/054-cgp-grafana-cm0-configmap.yaml

# trying
https://grafana.com/docs/grafana/latest/setup-grafana/installation/kubernetes/
k create namespace cgp-grafana
k get namespace cgp-grafana
k apply -f grafana.yaml --namespace=cgp-grafana
...
k get all --namespace=cgp-grafana
k port-forward service/grafana 3000:3000 --namespace=cgp-grafana
k expose deployment grafana --type=LoadBalancer --name=grafana

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
  - from Grafana:
  cgp-database:5432
  postgres
  postgres
  postgres


## refinding kubeconfig
Calico config: /var/snap/microk8s/current/args/cni-network/calico-kubeconfig
Overall at default location:
  ~/.kube/config
  // but this is kubernetes overall, not microk8s...??
  + tried adding dashboard token: ... worked.

# trying calicoctl
cd /usr/local/bin/
sudo curl -L https://github.com/projectcalico/calico/releases/download/v3.29.1/calicoctl-linux-amd64 -o kubectl-calico
sudo chmod +x kubectl-calico

can now run with
k calico

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
