#!/bin/bash

# Kubernetes Microservice Deployment Script

set -e

echo "==================================="
echo "Kubernetes Microservice Deployment"
echo "==================================="

NAMESPACE=${1:-default}
RELEASE_NAME=${2:-microservice-api}
HELM_CHART=${3:-./kubernetes/helm}
ENVIRONMENT=${4:-development}

echo "Namespace: $NAMESPACE"
echo "Release Name: $RELEASE_NAME"
echo "Helm Chart: $HELM_CHART"
echo "Environment: $ENVIRONMENT"
echo ""

# Create namespace if it doesn't exist
echo "Creating namespace..."
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Add Helm repositories (optional)
echo "Adding Helm repositories..."
helm repo add stable https://charts.helm.sh/stable || true
helm repo add nginx-stable https://helm.nginx.com/stable || true
helm repo update || true

# Install or upgrade the Helm chart
if helm list -n $NAMESPACE | grep -q "^$RELEASE_NAME"; then
    echo "Upgrading existing release: $RELEASE_NAME"
    helm upgrade $RELEASE_NAME $HELM_CHART \
        --namespace $NAMESPACE \
        -f $HELM_CHART/values-$ENVIRONMENT.yaml \
        --create-namespace \
        --wait \
        --timeout 5m
else
    echo "Installing new release: $RELEASE_NAME"
    helm install $RELEASE_NAME $HELM_CHART \
        --namespace $NAMESPACE \
        -f $HELM_CHART/values-$ENVIRONMENT.yaml \
        --create-namespace \
        --wait \
        --timeout 5m
fi

echo ""
echo "==================================="
echo "Deployment Status"
echo "==================================="

# Get deployment status
echo ""
echo "Deployments:"
kubectl get deployments -n $NAMESPACE

echo ""
echo "Services:"
kubectl get services -n $NAMESPACE

echo ""
echo "Ingress:"
kubectl get ingress -n $NAMESPACE

echo ""
echo "Pods:"
kubectl get pods -n $NAMESPACE

echo ""
echo "HPA Status:"
kubectl get hpa -n $NAMESPACE

echo ""
echo "==================================="
echo "Deployment completed successfully!"
echo "==================================="
