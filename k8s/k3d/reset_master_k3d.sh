#!/bin/bash

kubectl delete -f k8s/k3d/k3d_yaml/09-cgp-master-k3d.yaml
kubectl apply -f k8s/k3d/k3d_yaml/09-cgp-master-k3d.yaml
