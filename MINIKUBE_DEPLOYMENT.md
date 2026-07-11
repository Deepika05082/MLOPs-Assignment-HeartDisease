# Minikube Local Deployment Guide

This guide covers deploying your Heart Disease ML model to a local Minikube cluster.

## 📋 Prerequisites

- ✅ Minikube installed ([Install Guide](https://minikube.sigs.k8s.io/docs/start/))
- ✅ kubectl installed
- ✅ Docker installed
- ✅ Project built locally

## 🚀 Quick Start

### Step 1: Start Minikube

```powershell
# Windows
minikube start --driver=docker

# Mac/Linux
minikube start
```

Verify it's running:
```bash
kubectl cluster-info
kubectl get nodes
```

### Step 2: Build Docker Image

Build locally:
```bash
docker build -t heart-disease-model:latest .
```

### Step 3: Load Image to Minikube

```powershell
# Important: Use Minikube's Docker daemon to avoid pulling from registry
minikube image load heart-disease-model:latest
```

Or, if using Minikube's Docker daemon directly:
```bash
# Use Minikube's Docker environment
@FOR /f "tokens=*" %i IN ('minikube docker-env') DO @%i

# Build inside Minikube's Docker
docker build -t heart-disease-model:latest .
```

### Step 4: Deploy to Minikube

```bash
# Apply deployment
kubectl apply -f deployment.yaml

# Create service
kubectl apply -f service.yaml

# Verify deployment
kubectl get deployments
kubectl get pods
kubectl get services
```

### Step 5: Access the Application

#### Port Forward Method
```bash
# Forward local port to service
kubectl port-forward svc/heart-disease-service 8000:8000
```

Access at: `http://localhost:8000`

#### Minikube Service Method
```bash
# Automatically opens in browser (Mac/Windows)
minikube service heart-disease-service

# Or get the URL
minikube service heart-disease-service --url
```

## 📊 Useful Commands

### Check Deployment Status
```bash
# Detailed deployment info
kubectl describe deployment heart-disease-model

# Watch pods starting up
kubectl get pods -w

# Check pod logs
kubectl logs -f deployment/heart-disease-model

# Get into pod for debugging
kubectl exec -it <pod-name> -- /bin/bash
```

### Check Service
```bash
# List all services
kubectl get svc

# Describe service
kubectl describe svc heart-disease-service

# Get service endpoints
kubectl get endpoints
```

### Scale Deployment
```bash
# Scale to 3 replicas
kubectl scale deployment heart-disease-model --replicas=3

# View replicas
kubectl get pods
```

### Update Deployment
```bash
# Rebuild image
docker build -t heart-disease-model:v1.0 .

# Load to Minikube
minikube image load heart-disease-model:v1.0

# Update deployment
kubectl set image deployment/heart-disease-model \
  heart-disease-model=heart-disease-model:v1.0

# Watch rollout
kubectl rollout status deployment/heart-disease-model
```

### Clean Up
```bash
# Delete deployment and service
kubectl delete deployment heart-disease-model
kubectl delete service heart-disease-service

# Or delete using YAML files
kubectl delete -f deployment.yaml
kubectl delete -f service.yaml

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete
```

## 🔍 Testing the Deployment

### Health Check
```bash
# Check if API is responding
curl http://localhost:8000/docs
```

### Make Prediction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 45,
    "sex": 1,
    "cp": 1,
    "trestbps": 130,
    "chol": 200,
    "fbs": 0,
    "restecg": 0,
    "thalach": 130,
    "exang": 0,
    "oldpeak": 0.5,
    "slope": 1,
    "ca": 0,
    "thal": 2
  }'
```

### View Metrics
```bash
curl http://localhost:8000/metrics
```

## 🐛 Troubleshooting

### Pod stays in "ImagePullBackOff"
```bash
# This means image not found in Minikube
# Solution: Reload the image
minikube image load heart-disease-model:latest

# Verify image is loaded
minikube image ls | grep heart-disease-model
```

### Pod crashes or "CrashLoopBackOff"
```bash
# Check pod logs
kubectl logs <pod-name>

# Check for common issues:
# - Wrong port in deployment.yaml (must be 8000)
# - Missing model file
# - Import errors

# Rebuild and reload
docker build -t heart-disease-model:latest .
minikube image load heart-disease-model:latest
kubectl rollout restart deployment/heart-disease-model
```

### Cannot connect to service
```bash
# Check service is created
kubectl get svc

# Check endpoints
kubectl get endpoints

# If no endpoints, check pod status
kubectl get pods

# Port-forward directly
kubectl port-forward pod/<pod-name> 8000:8000
```

### Docker image not found error
```bash
# Ensure you're using Minikube's Docker daemon
eval $(minikube docker-env)

# Or load image explicitly
docker build -t heart-disease-model:latest .
minikube image load heart-disease-model:latest

# Verify with imagePullPolicy: Never in deployment.yaml
```

### Minikube won't start
```bash
# Reset Minikube
minikube delete
minikube start --driver=docker

# Check Docker is running
docker ps

# Check system resources
# Minikube needs ~2GB RAM, 2 CPU cores
```

## 📈 Monitoring with Minikube

### View Dashboard
```bash
# Opens Kubernetes dashboard in browser
minikube dashboard
```

### Check Resource Usage
```bash
# CPU and memory of pods
kubectl top pods

# Node resources
kubectl top nodes
```

### View Events
```bash
# Recent events in cluster
kubectl get events

# Follow events
kubectl get events -w
```

## 🔐 Environment Variables

Set in deployment.yaml if needed:
```yaml
env:
- name: ENVIRONMENT
  value: "production"
- name: LOG_LEVEL
  value: "INFO"
```

## 📁 File Locations

- **Deployment manifest:** `deployment.yaml`
- **Service manifest:** `service.yaml`
- **Docker image:** Built from `Dockerfile`
- **Application code:** `src/app.py`
- **Model:** `models/final_pipeline.pkl`

## ✅ Deployment Checklist

- [ ] Minikube started (`minikube start`)
- [ ] Docker image built (`docker build -t heart-disease-model:latest .`)
- [ ] Image loaded to Minikube (`minikube image load heart-disease-model:latest`)
- [ ] Deployment created (`kubectl apply -f deployment.yaml`)
- [ ] Service created (`kubectl apply -f service.yaml`)
- [ ] Pods running (`kubectl get pods`)
- [ ] Port forwarded (`kubectl port-forward svc/heart-disease-service 8000:8000`)
- [ ] API accessible (`curl http://localhost:8000/docs`)

## 🎯 Next Steps

1. Test predictions with sample data
2. View logs and metrics
3. Scale deployment if needed
4. Set up monitoring (Prometheus/Grafana)
5. Configure CI/CD for automated deployment

---

**For CI/CD cloud deployments**, see [CICD_SETUP.md](CICD_SETUP.md)
