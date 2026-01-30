#!/bin/bash

microk8s kubectl delete -f k8s/07-worker.yaml
microk8s kubectl apply -f k8s/07-worker.yaml
