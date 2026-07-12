#!/bin/bash
# setup-cicd.sh
# Unified setup script for CI/CD pipeline (Linux/Mac/WSL)

set -e

echo "Setting up CI/CD pipeline for Heart Disease ML Model..."

# Step 1: Verify prerequisites
echo " Checking prerequisites..."
command -v git >/dev/null 2>&1 || { echo "❌ Git not found. Install Git first."; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "❌ Docker not found. Install Docker first."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ Python3 not found. Install Python 3.10+."; exit 1; }

# Step 2: Create workflow file
echo "📁 Creating GitHub Actions workflow..."
mkdir -p .github/workflows
cat > .github/workflows/ci-cd.yml <<'EOF'
name: CI/CD Pipeline

on:
  push:
    branches: [ "main", "develop" ]
  pull_request:
    branches: [ "main", "develop" ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install flake8
      - name: Run flake8
        run: flake8 src tests

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install pytest pytest-cov
      - name: Run tests
        run: pytest tests/ --cov=src

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t ghcr.io/${{ github.repository }}:${{ github.sha }} .
      - name: Log in to GHCR
        run: echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin
      - name: Push Docker image
        run: docker push ghcr.io/${{ github.repository }}:${{ github.sha }}

  deploy:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - name: Set up kubectl
        run: |
          echo "${{ secrets.KUBE_CONFIG }}" | base64 --decode > kubeconfig
          export KUBECONFIG=kubeconfig
      - name: Deploy to Kubernetes
        run: |
          kubectl apply -f deployment-cicd.yaml
          kubectl rollout status deployment/heart-disease-model
EOF

# Step 3: Create Kubernetes deployment file
echo " Creating Kubernetes deployment manifest..."
cat > deployment-cicd.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: heart-disease-model
spec:
  replicas: 2
  selector:
    matchLabels:
      app: heart-disease-model
  template:
    metadata:
      labels:
        app: heart-disease-model
    spec:
      containers:
      - name: heart-disease-model
        image: ghcr.io/YOUR-GITHUB-USERNAME/YOUR-REPO-NAME:latest
        ports:
        - containerPort: 8000
        securityContext:
          runAsUser: 1000
          runAsGroup: 1000
          allowPrivilegeEscalation: false
EOF

# Step 4: Create documentation file
echo " Creating CICD_SETUP.md..."
cat > CICD_SETUP.md <<'EOF'
# CI/CD Setup Guide

This document explains how to configure and run the CI/CD pipeline for the Heart Disease ML Model.

1. Verify prerequisites (GitHub Actions enabled, Docker, Python 3.10+, Kubernetes cluster optional).
2. Configure GitHub Secrets:
   - `KUBE_CONFIG`: base64 encoded kubeconfig for Kubernetes deployment.
3. Update `deployment-cicd.yaml` with your GHCR image path.
4. Push changes to trigger the pipeline.
5. Monitor workflow runs in the GitHub Actions tab.
EOF

echo " CI/CD pipeline setup complete!"
echo " Next: Commit and push these files to your repository."
