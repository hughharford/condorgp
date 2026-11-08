# Microk8s Networking notes

### do this on master and all nodes:
# These ports were found while getting microk8s + istio running. They are node-to-node
# ports, so they are opened ONLY to the other cluster machines, never to "anywhere".
# (A rule with no "from <address>" part opens the port to the whole internet.)
# For k3s hub-and-spoke use k3s/ufw_rules.sh instead; it is dry-run by default.
#
#   export NODE_IPS="<ip of each other cluster node>" first, then paste this block
: "${NODE_IPS:?set NODE_IPS to the other nodes public IPs, space separated}"
open_to_nodes() {   # usage: open_to_nodes <port> [<port> ...]
  for ip in $NODE_IPS; do
    for port in "$@"; do sudo ufw allow from "$ip" to any port "$port"; done
  done
}
# base (dns, postgres, misc)
open_to_nodes 53 9153 5432 42102 47371
# kube-prom-stack
open_to_nodes 9095 45008
# istio sidecar (Envoy)
open_to_nodes 15000 15001 15004 15006 15008 15020 15021 15053 15090
# istiod
open_to_nodes 443 8080 15010 15012 15014 15017
# istio ztunnel
open_to_nodes 15080
# other around istio
open_to_nodes 3101 31322 80 31482 31549 31633 30550
# istio egressgateway
open_to_nodes 80 443
# kiali
open_to_nodes 20001 9090
# istio ingressgateway
open_to_nodes 80 443 8080 8443 15021 15090 15443 31400 1338 2380 12379 16443 19001 25000 10248 10249 10250 10251 10252 10253 10254 10255 10256 10257 10258 10259
# Above, 80/443 are opened to the nodes only. Letting the public reach the ingress gateway
# is a separate, deliberate decision; it is not part of this block.

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
