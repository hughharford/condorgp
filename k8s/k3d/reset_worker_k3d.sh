#!/bin/bash

kubectl delete -f k8s/k3d/k3d_yaml/08-cgp-worker-k3d.yaml
kubectl apply -f k8s/k3d/k3d_yaml/08-cgp-worker-k3d.yaml
