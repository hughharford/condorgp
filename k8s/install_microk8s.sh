#!/bin/bash

# Update package list
# sudo apt update

# Install MicroK8s
sudo snap install microk8s --classic

# Add current user to microk8s group
sudo usermod -a -G microk8s $USER

# Create .kube directory if it doesn't exist
mkdir -p ~/.kube
sudo chown -R $USER ~/.kube


# Wait for MicroK8s to be ready
microk8s status --wait-ready

# Enable necessary addons
microk8s enable dns
microk8s enable hostpath-storage
microk8s enable ingress
microk8s enable registry
microk8s enable dashboard

# Configure kubectl alias (optional)
echo "alias k='sudo microk8s kubectl'" >> ~/.zshrc

# Generate and save kubeconfig
microk8s config > ~/.kube/config

# Reload shell to apply group changes

echo "NOW _______________________________________ reload shell to apply changes.."
# source ~/.zshrc
