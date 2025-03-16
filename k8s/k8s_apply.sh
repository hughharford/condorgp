#!/bin/bash

# 3. Apply them in order:


microk8s kubectl apply -f k8s/00-namespace.yaml
microk8s kubectl apply -f k8s/01-configmap.yaml
microk8s kubectl apply -f k8s/02-secrets.yaml
microk8s kubectl apply -f k8s/03-persistent-volumes.yaml
microk8s kubectl apply -f k8s/04-postgres.yaml
microk8s kubectl apply -f k8s/05-rabbitmq.yaml
microk8s kubectl apply -f k8s/06-grafana.yaml
microk8s kubectl apply -f k8s/07-worker.yaml
