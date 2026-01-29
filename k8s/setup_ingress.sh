#!/bin/bash

# Install NGINX Ingress Controller using Helm
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install ingress-nginx ingress-nginx/ingress-nginx

# Wait for the Ingress Controller to be ready
echo "Waiting for Ingress Controller to be ready..."
microk8s kubectl wait --namespace default \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

# Apply the Ingress configuration
microk8s kubectl apply -f k8s/09-ingress.yaml

echo "Ingress Controller and configuration have been set up!"
