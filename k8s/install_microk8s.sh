#!/bin/bash

# Update package list
sudo apt update

# Install MicroK8s
sudo snap install microk8s --classic

# Add current user to microk8s group
sudo usermod -a -G microk8s $USER
sudo chown -R $USER ~/.kube

# Create .kube directory if it doesn't exist
mkdir -p ~/.kube

# Wait for MicroK8s to be ready
microk8s status --wait-ready

# Enable necessary addons
microk8s enable dns
microk8s enable storage
microk8s enable ingress
microk8s enable registry
microk8s enable dashboard

# Configure kubectl alias (optional)
echo "alias kubectl='microk8s kubectl'" >> ~/.bashrc

# Generate and save kubeconfig
microk8s config > ~/.kube/config

# Reload shell to apply group changes
echo "Please log out and log back in to apply group changes, or run: 'newgrp microk8s'"
