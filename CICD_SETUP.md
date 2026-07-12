#!/bin/bash
# setup-cicd.sh
# Unified setup script for CI/CD pipeline (Linux/Mac/WSL)

set -e

echo "🔧 Setting up CI/CD pipeline for Heart Disease ML Model..."

# Step 1: Verify prerequisites
echo "✅ Checking prerequisites..."
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
echo "📁 Creating Kubernetes deployment manifest..."
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

# Step 4: Create documentation file (Setup Guide)
echo "📁 Creating CI/CD Pipeline Setup Guide..."
cat > CICD_SETUP.md <<'EOF'
# CI/CD Pipeline Setup Guide

## Overview
This CI/CD pipeline automates testing, building, and deployment of your Heart Disease ML model using GitHub Actions.

## Pipeline Stages
1. **Lint** – flake8 checks for code quality
2. **Test** – pytest unit tests + coverage
3. **Build** – Docker image pushed to GHCR
4. **Deploy** – Kubernetes rollout (main branch only)
5. **Notify** – Status validation

## Prerequisites
- Enable GitHub Actions in repo settings
- Configure secrets:
  - `KUBE_CONFIG`: base64 encoded kubeconfig
  - `DOCKER_REGISTRY_PASSWORD`: if using private registry

Encode kubeconfig:
bash
cat ~/.kube/config | base64 | tr -d '\n'
