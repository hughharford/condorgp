# Microk8s Networking notes

### do this on master and all nodes:
sudo ufw allow 53
sudo ufw allow 9153
sudo ufw allow 5432
sudo ufw allow 42102
sudo ufw allow 47371

# kube-prom-stack
sudo ufw allow 9095
sudo ufw allow 45008

# istio

# istio sidecar (Envoy)
sudo ufw allow 15000
sudo ufw allow 15001
sudo ufw allow 15004
sudo ufw allow 15006
sudo ufw allow 15008
sudo ufw allow 15020
sudo ufw allow 15021
sudo ufw allow 15053
sudo ufw allow 15090

# istiod
sudo ufw allow 443
sudo ufw allow 8080
sudo ufw allow 15010
sudo ufw allow 15012
sudo ufw allow 15014
sudo ufw allow 15017

# istio ztunnel
sudo ufw allow 15080

# other around istio
sudo ufw allow 3101
sudo ufw allow 31322
sudo ufw allow 80
sudo ufw allow 31482
sudo ufw allow 31549
sudo ufw allow 31633
sudo ufw allow 30550

# istio egressgateway
sudo ufw allow 80
sudo ufw allow 443

# kiali
sudo ufw allow 20001
sudo ufw allow 9090


# istio ingressgateway
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 8080
sudo ufw allow 8443
sudo ufw allow 15021
sudo ufw allow 15090
sudo ufw allow 15443
sudo ufw allow 31400


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

### Microk8s CNI configuration
+ CNI = Container Network Interface
+ run by Calico, after microk8s 1.19 (at 1.31.5 now)
+ NOTE flannel if not HA - High Availability, Calico otherwise:
  https://microk8s.io/docs/configuring-services

this covers all the ports listed:
https://microk8s.io/docs/ports

# must have
microk8s enable dns
+ https://microk8s.io/docs/addon-dns

# enable linkerd
sudo microk8s enable linkerd
### linkerd  # (community) Linkerd is a service mesh for Kubernetes and other frameworks


# check network policies:
k get networkpolicy --all-namespaces
- or
k get networkpolicy -n cgp-database

k get networkpolicy -n ztunnel

# CRDs_netw
### https://github.com/kubernetes-sigs/gateway-api/blob/main/config/crd/standard/gateway.networking.k8s.io_referencegrants.yaml
k apply -f kubernetes/CRDS_netw/gateway-networking-k8s-io-gatewayclasses.yaml
k apply -f kubernetes/CRDS_netw/gateway-networking-k8s-io-gateways.yaml
k apply -f kubernetes/CRDS_netw/gateway-networking-k8s-io-grpcroutes.yaml
k apply -f kubernetes/CRDS_netw/gateway-networking-k8s-io-httproutes.yaml
k apply -f kubernetes/CRDS_netw/gateway-networking-k8s-io-referencegrants.yaml

k delete -f kubernetes/CRDS_netw/gateway-networking-k8s-io-gatewayclasses.yaml
k delete -f kubernetes/CRDS_netw/gateway-networking-k8s-io-gateways.yaml
k delete -f kubernetes/CRDS_netw/gateway-networking-k8s-io-grpcroutes.yaml
k delete -f kubernetes/CRDS_netw/gateway-networking-k8s-io-httproutes.yaml
k delete -f kubernetes/CRDS_netw/gateway-networking-k8s-io-referencegrants.yaml
