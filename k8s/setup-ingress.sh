#!/bin/bash

# Install NGINX Ingress Controller using Helm
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install ingress-nginx ingress-nginx/ingress-nginx

# Wait for the Ingress Controller to be ready
echo "Waiting for Ingress Controller to be ready..."
kubectl wait --namespace default \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

# Apply the Ingress configuration
kubectl apply -f ingress.yaml

echo "Ingress Controller and configuration have been set up!" 