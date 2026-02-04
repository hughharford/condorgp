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


# PREREQUISITES

## NB first time k3d is setup, run this to ensure ip forwarding on
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward


# EARLY ERRORS
Error response from daemon: add inter-network communication rule

ERRO[0000] Failed Cluster Preparation: Failed Network Preparation: failed to create cluster network: docker failed to create new network 'k3d-first-cluster': Error response from daemon: add inter-network communication rule:  (iptables failed: iptables --wait -t filter -A DOCKER-ISOLATION-STAGE-1 -i br-257eedbd73c2 ! -o br-257eedbd73c2 -j DOCKER-ISOLATION-STAGE-2: iptables v1.8.10 (nf_tables): Chain 'DOCKER-ISOLATION-STAGE-2' does not exist
Try `iptables -h' or 'iptables --help' for more information.
 (exit status 2))

# DOCKER MUST BE LESS THAN 28 to work
See specific version instal here:
https://docs.docker.com/engine/install/ubuntu/
And post installation steps here:



# DASHBOARD CLUSTER
k3d cluster create dashboard-cluster --api-port 6550 -p "8080:80@loadbalancer" --agents 2

kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
kubectl create serviceaccount dashboard-admin
kubectl create clusterrolebinding dashboard-admin --clusterrole=cluster-admin --serviceaccount=default:dashboard-admin
kubectl create token dashboard-admin

kubectl port-forward -n kubernetes-dashboard service/kubernetes-dashboard 8443:443 --address 0.0.0.0
https://localhost:8443
