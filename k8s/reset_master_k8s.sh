#!/bin/bash

microk8s kubectl delete -f k8s/08-cgp-master.yaml
microk8s kubectl apply -f k8s/08-cgp-master.yaml
