# K3S attempted, as simpler than k8s

## REF: https://medium.com/@vincent_turrin/crafting-a-complete-kubernetes-home-lab-building-a-k3s-cluster-on-raspberry-pi-4fc9106bd94f

- trying this one first




# OTHER k3s refs:
https://www.digitalocean.com/community/tutorials/how-to-setup-k3s-kubernetes-cluster-on-ubuntu


# trying this, from k3s site:
...https://docs.k3s.io/installation/requirements?os=debian
https://docs.k3s.io/quick-start

on master:
  curl -sfL https://get.k3s.io | sh -s - --write-kubeconfig-mode 644

on node:
  curl -sfL https://get.k3s.io | K3S_URL=https://<PRIMARY_NODE_IP>:6443
K3S_TOKEN=<TOKEN> sh -

i.e.:
curl -sfL https://get.k3s.io | K3S_URL=https://192.168.1.100:6443 K3S_TOKEN= sh -


- this ref shows some useful obvious bits:
- https://medium.com/@vincent_turrin/crafting-a-complete-kubernetes-home-lab-building-a-k3s-cluster-on-raspberry-pi-4fc9106bd94f
- e.g
  - # Run this on the primary node to retrieve the server token
sudo cat /var/lib/rancher/k3s/server/token


- this worked, but needed to stop an existing process:
      sudo netstat -tulpn | grep 10250
- showed kubelite with PID 3254
- so:
      sudo kill 3254



- also, ran uninstall to clear out and reinstall/join line again
- script for agent uninstall:
      sh /usr/local/bin/k3s-agent-uninstall.sh
- uninstall on master:
      sh /usr/local/bin/k3s-uninstall.sh



# got proxy server
- kubectl proxy
- http://127.0.0.1:8001/
-


http://localhost:8080/api/
lists:
  192.168.1.100:6443

going to:
  https://192.168.1.100:6443/
gives unauthorised
  need a user


# this ref seems helpful:
https://kubernetes.io/docs/reference/kubectl/quick-reference/#kubectl-context-and-configuration


# also some useful commands in here:
https://pgillich.medium.com/setup-lightweight-kubernetes-with-k3s-6a1c57d62217

including:
- k3s check-config
- kubectl cluster-info
- kubectl get nodes -o wide
- # Wait until all pods and deployments aren't Running or Completed,
# see READY and STATUS columns
kubectl get all -A -o wide
kubectl get endpoints -A
sudo k3s crictl ps -a
kubectl top pod --containers -A

recommends something like:
http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/


kubectl get service -n kubernetes-dashboard

192.168.1.100:32087/#/login


# KUBENETES DASHBOARD INSTALLATION
from
  https://github.com/kubernetes/dashboard/releases/tag/kubernetes-dashboard-7.10.1

helm repo add kubernetes-dashboard https://kubernetes.github.io/dashboard/
with SUDO
fails with:
  Error: Kubernetes cluster unreachable: Get "http://localhost:8080/version": dial tcp 127.0.0.1:8080: connect: connection refused

  which is what i have seen...


kubectl delete namespace kubernetes-dashboard
>> deleted existing dashboard

then

helm install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard

seemed to work:
gave:
NAME: kubernetes-dashboard
LAST DEPLOYED: Sun Jan 26 22:49:31 2025
NAMESPACE: kubernetes-dashboard
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
*************************************************************************************************
*** PLEASE BE PATIENT: Kubernetes Dashboard may need a few minutes to get up and become ready ***
*************************************************************************************************

Congratulations! You have just installed Kubernetes Dashboard in your cluster.

To access Dashboard run:
  kubectl -n kubernetes-dashboard port-forward svc/kubernetes-dashboard-kong-proxy 8443:443

NOTE: In case port-forward command does not work, make sure that kong service name is correct.
      Check the services in Kubernetes Dashboard namespace using:
        kubectl -n kubernetes-dashboard get svc

Dashboard will be available at:
  https://localhost:8443

but doesn't load at all after 10 minutes
https://localhost:8443

the port forwarding seems to be correct, i.e. kubernetes-dashboard-kong-proxy

but eventually, this almost worked:
https://localhost:8443
redirected to:
https://localhost:8443/#/login
