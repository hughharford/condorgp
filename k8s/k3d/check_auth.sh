k3d kubeconfig get cgp-cluster > /tmp/k3d-cgp-kubeconfig.yaml
kubectl --kubeconfig /tmp/k3d-cgp-kubeconfig.yaml --context k3d-cgp-cluster cluster-info
kubectl --kubeconfig /tmp/k3d-cgp-kubeconfig.yaml --context k3d-cgp-cluster auth can-i '*' '*' --all-namespaces