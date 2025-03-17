#!/bin/bash

# Function to check ingress status
check_ingress() {
    echo "Checking Ingress Status..."
    kubectl get ingress
    echo -e "\nDetailed Ingress Description:"
    kubectl describe ingress cgp-ingress
}

# Function to check ingress controller pods
check_controller() {
    echo "Checking Ingress Controller Pods..."
    kubectl get pods -l app.kubernetes.io/component=controller
    echo -e "\nIngress Controller Logs:"
    CONTROLLER_POD=$(kubectl get pods -l app.kubernetes.io/component=controller -o jsonpath='{.items[0].metadata.name}')
    kubectl logs $CONTROLLER_POD
}

# Function to create TLS secret
create_tls_secret() {
    if [ -z "$1" ] || [ -z "$2" ]; then
        echo "Usage: create_tls_secret <path/to/tls.key> <path/to/tls.crt>"
        return 1
    fi
    kubectl create secret tls cgp-tls-secret \
        --key $1 \
        --cert $2
}

# Show usage
echo "Available commands:"
echo "1. check_ingress - Check status of Ingress resources"
echo "2. check_controller - Check Ingress Controller status and logs"
echo "3. create_tls_secret - Create TLS secret (requires key and cert files)" 