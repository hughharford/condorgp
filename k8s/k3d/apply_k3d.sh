#!/bin/bash

# 3. Apply them in order:


kubectl apply -f k8s/k3d/k3d_yaml/00-namespace-k3d.yaml
kubectl apply -f k8s/k3d/k3d_yaml/01-configmap-k3d.yaml
kubectl apply -f k8s/k3d/k3d_yaml/02-secrets-k3d.yaml
kubectl apply -f k8s/k3d/k3d_yaml/03-persistent-volumes-k3d.yaml
kubectl apply -f k8s/k3d/k3d_yaml/04-postgres-k3d.yaml
kubectl apply -f k8s/k3d/k3d_yaml/05-rabbitmq-k3d.yaml
kubectl apply -f k8s/k3d/k3d_yaml/06-grafana-k3d.yaml
kubectl apply -f k8s/k3d/k3d_yaml/07-ingress-k3d.yaml
kubectl apply -f k8s/k3d/k3d_yaml/08-cgp-worker-k3d.yaml
kubectl apply -f k8s/k3d/k3d_yaml/09-cgp-master-k3d.yaml
