@echo off
REM Quick Minikube Deployment Script for Windows

echo.
echo 🚀 Heart Disease ML - Minikube Quick Start
echo ==========================================
echo.

REM Step 1: Check Minikube is installed
echo  Checking Minikube...
minikube version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Minikube not found. Please install it first.
    echo    https://minikube.sigs.k8s.io/docs/start/
    exit /b 1
)

REM Step 2: Start Minikube
echo.
echo  Starting Minikube...
minikube start --driver=docker
if %errorlevel% neq 0 (
    echo ❌ Failed to start Minikube
    exit /b 1
)

REM Step 3: Verify kubectl
echo.
echo  Verifying kubectl...
kubectl cluster-info

REM Step 4: Build Docker image
echo.
echo  Building Docker image...
docker build -t heart-disease-model:latest .
if %errorlevel% neq 0 (
    echo ❌ Docker build failed
    exit /b 1
)

REM Step 5: Load image to Minikube
echo.
echo  Loading image to Minikube...
minikube image load heart-disease-model:latest

REM Step 6: Deploy to Minikube
echo.
echo  Deploying to Minikube...
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

REM Step 7: Wait for pods to be ready
echo.
echo  Waiting for pods to be ready...
timeout /t 5 /nobreak
kubectl get pods

REM Step 8: Get service info
echo.
echo  Service Information:
kubectl get svc heart-disease-service

REM Step 9: Display access information
echo.
echo ==========================================
echo  Deployment Complete!
echo.
echo  Access Methods:
echo.
echo 1. Port Forwarding (Recommended for localhost):
echo    kubectl port-forward svc/heart-disease-service 8000:8000
echo    Then visit: http://localhost:8000
echo.
echo 2. Minikube Service (Auto port-forward):
echo    minikube service heart-disease-service
echo.
echo 3. NodePort (Direct access):
echo    minikube ip
echo    Then visit: http://^<minikube-ip^>:30080
echo.
echo  API Documentation: http://localhost:8000/docs
echo  Metrics: http://localhost:8000/metrics
echo.
echo  Useful Commands:
echo    - View logs: kubectl logs -f deployment/heart-disease-model
echo    - Pod status: kubectl get pods -w
echo    - Delete all: kubectl delete -f deployment.yaml, service.yaml
echo    - Stop Minikube: minikube stop
echo.
echo ==========================================
pause
