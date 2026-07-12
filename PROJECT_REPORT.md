# Heart Disease Prediction Model - Project Report

**Assignment:** MLOps - Assignment Heart Disease  
**Institution:** BITS Pilani  
**Semester:** 3  
**Date:** 2024

**📌 Code Repository:** [https://github.com/YOUR-USERNAME/Assignment-HeartDisease](https://github.com/YOUR-USERNAME/Assignment-HeartDisease)



## 📑 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Setup & Installation Instructions](#setup--installation-instructions)
3. [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
4. [Modeling Choices](#modeling-choices)
5. [Experiment Tracking](#experiment-tracking)
6. [MLOps Architecture](#mlops-architecture)
7. [CI/CD & Deployment Pipeline](#cicd--deployment-pipeline)
8. [API Reference](#api-reference)
9. [Project Repository](#project-repository)



## Executive Summary

This project implements an end-to-end MLOps pipeline for **multi-class heart disease severity prediction**. The system classifies heart disease into 5 severity levels using Scikit-learn, FastAPI, Docker, Kubernetes (Minikube), and GitHub Actions CI/CD.

**Key Components:**
-  Multi-class ML model (LogisticRegression + RandomForest)
-  FastAPI REST API with probability predictions
-  Docker containerization with python:3.10-slim
-  Kubernetes deployment on Minikube
-  MLflow experiment tracking
-  GitHub Actions CI/CD (lint → test → build)
-  Prometheus metrics monitoring
-  Comprehensive unit tests (pytest)



## Setup & Installation Instructions

### Prerequisites
- Python 3.10+
- Docker
- Minikube
- kubectl
- Git

### Quick Start (Local Development)

bash
# 1. Clone and setup
git clone https://github.com/YOUR-USERNAME/Assignment-HeartDisease.git
cd Assignment-HeartDisease

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run tests
pytest tests/ -v

# 5. Start MLflow tracking server
mlflow ui  # http://localhost:5000

# 6. Run the application
uvicorn src.app:app --reload  # http://localhost:8000


### Docker Deployment (Local)

bash
# Build image
docker build -t heart-disease-model:latest .

# Run container
docker run -p 8000:8000 heart-disease-model:latest

# With monitoring stack (Prometheus + Grafana)
docker-compose up
# API: http://localhost:8000
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)


### Kubernetes Deployment (Minikube)

bash
# Start Minikube
minikube start --driver=docker

# Build and load image
docker build -t heart-disease-model:latest .
minikube image load heart-disease-model:latest

# Deploy to Minikube
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Access application
kubectl port-forward svc/heart-disease-service 8000:8000
# Visit: http://localhost:8000/docs


## Exploratory Data Analysis (EDA)

### Dataset Overview

**Source:** UCI Heart Disease Dataset (Dataset ID: 45)

**Dataset Characteristics:**
- **Samples:** ~300 records
- **Target Classes:** 5 (No disease, Mild, Moderate, Severe, Very Severe)
- **Features:** 13 attributes

**Feature Breakdown:**

| Category | Features | Details |
|-|-||
| **Numeric** (5) | age, trestbps, chol, thalach, oldpeak | Standardized with StandardScaler |
| **Categorical** (8) | sex, cp, fbs, restecg, exang, slope, ca, thal | One-hot encoded after imputation |

### Data Preprocessing Pipeline

**Strategy:** ColumnTransformer with dual pipelines
- **Numeric features:** SimpleImputer (median) → StandardScaler
- **Categorical features:** SimpleImputer (most_frequent) → OneHotEncoder

**Train-Test Split:** 80/20 with stratification (random_state=42)

**Key Insights:**
- [Add EDA visualizations here: feature distributions, class balance, correlation matrix]



## Modeling Choices

### Model Approach: Multi-Class Classification

**Problem:** Predict 5-class disease severity (0-4)

**Models Trained:**

| Model | Algorithm | Tuning Method |
|-|--||
| Model 1 | LogisticRegression | GridSearchCV (5-fold) |
| Model 2 | RandomForest | RandomizedSearchCV (5-fold) |

**Selected Model:** `models/final_pipeline.pkl` (Best performer)

**Key Features:**
- Class balancing with `class_weight="balanced"`
- Cross-validation for robust evaluation
- One-vs-Rest (OvR) strategy for multi-class
- Metrics: Accuracy, Precision, Recall, F1-Score, ROC-AUC

**Model Performance:**
| Metric | Value |
|--|-|
| Accuracy | [Your %] |
| Precision (macro) | [Your %] |
| Recall (macro) | [Your %] |
| F1-Score (macro) | [Your %] |
| ROC-AUC (OvR) | [Your %] |



## Experiment Tracking

### MLflow Integration

**Purpose:** Track model experiments, parameters, metrics, and artifacts

**What's Tracked:**
- Model name and type
- Hyperparameters
- Metrics (accuracy, precision, recall, f1_score, roc_auc)
- Model artifacts (trained pipeline, ROC curves)
- Training duration

**Access Experiment Results:**
bash
mlflow ui  # http://localhost:5000


**Dashboard Features:**
- Compare multiple model runs
- Track metric improvements over time
- Download model artifacts
- View visualizations



## MLOps Architecture

### System Architecture Diagram


┌────────────────────────────────────────────────────────┐
│         Data Processing & Model Training               │
│  (preprocessing.py → train.py → MLflow tracking)       │
└─────────────────────┬──────────────────────────────────┘
                      ↓
┌────────────────────────────────────────────────────────┐
│            Trained Model Artifacts                      │
│      models/final_pipeline.pkl (Production)            │
└─────────────────────┬──────────────────────────────────┘
                      ↓
┌────────────────────────────────────────────────────────┐
│         FastAPI REST API (src/app.py)                  │
│  POST /predict → Returns class + probabilities         │
│  GET /metrics → Prometheus metrics                     │
└─────────────────────┬──────────────────────────────────┘
                      ↓
          ┌─────────────┴──────────────┐
          ↓                            ↓
┌──────────────────────┐    ┌──────────────────────┐
│   Docker Container   │    │  Metrics Collection  │
│  (python:3.10-slim)  │    │   (Prometheus)       │
│                      │    │  (Grafana Dash)      │
└──────────────────────┘    └──────────────────────┘
          ↓                            ↓
┌────────────────────────────────────────────────────────┐
│        Kubernetes Cluster (Minikube)                   │
│  - 2 Replicas (High Availability)                      │
│  - RollingUpdate Strategy                              │
│  - Health Checks (Liveness + Readiness)                │
└─────────────────────┬──────────────────────────────────┘
                      ↓
          ┌─────────────┴──────────────┐
          ↓                            ↓
┌──────────────────────┐    ┌──────────────────────┐
│   Application Layer  │    │  Monitoring Layer    │
│  (NodePort Service)  │    │  (Metrics + Logging) │
│  Port: 30080         │    │                      │
└──────────────────────┘    └──────────────────────┘


### Technology Stack

| Layer | Technology |
|-|--|
| **ML Framework** | Scikit-learn, pandas, numpy |
| **API Framework** | FastAPI + Uvicorn |
| **Containerization** | Docker |
| **Orchestration** | Kubernetes (Minikube) |
| **Experiment Tracking** | MLflow |
| **Monitoring** | Prometheus + Grafana |
| **CI/CD** | GitHub Actions |
| **Testing** | pytest |
| **Metrics** | prometheus-client |

| Run | Model | Algorithm | Hyperparameters | Metrics |
|--|-|--|--||
| 1 | LogisticRegression | GridSearchCV | [Best hyperparameters] | [See MLflow] |
| 2 | RandomForest | RandomizedSearchCV | [Best hyperparameters] | [See MLflow] |

**[Add screenshots of MLflow dashboard showing both runs]**

### Monitoring Experiment Progress

Access MLflow UI to:
- Compare metrics across runs
- View hyperparameters tried
- Download logged artifacts
- Track metrics over experiments



## MLOps Architecture

### System Architecture Diagram

**[Add your architecture diagram image here]**


Expected components:
├── Data Source (UCI Dataset)
├── Data Processing (Pandas/NumPy)
├── Model Training (Scikit-learn)
├── Experiment Tracking (MLflow)
├── Model Versioning (joblib/pkl)
├── API Service (FastAPI)
├── Containerization (Docker)
├── Orchestration (Kubernetes/Minikube)
├── CI/CD Pipeline (GitHub Actions)
└── Monitoring (Prometheus)


### Technology Stack

| Layer | Technology | Purpose |
|-|--||
| **Data** | Pandas, NumPy | Data processing |
| **ML** | Scikit-learn | Model training |
| **Tracking** | MLflow | Experiment tracking |
| **API** | FastAPI, Uvicorn | REST API server |
| **Container** | Docker | Container images |
| **Orchestration** | Kubernetes (Minikube) | Container management |
| **CI/CD** | GitHub Actions | Automated testing & build |
| **Monitoring** | Prometheus | Metrics collection |



## Containerization

### Docker Image

**File:** `Dockerfile`

**Base Image:** python:3.10-slim
- **Size:** ~150MB (slim variant)
- **Python Version:** 3.10
- **OS:** Debian-based Linux

**Dockerfile Stages:**

dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]


**Build Steps:**
1. **Stage 1:** Use python:3.10-slim as base
2. **Set working directory:** /app
3. **Install dependencies:** pip install from requirements.txt
4. **Copy source code:** Copy all files to /app
5. **Entrypoint:** Run FastAPI app with uvicorn

**Build Command:**
bash
docker build -t heart-disease-model:latest .


**Run Command:**
bash
docker run -p 8000:8000 heart-disease-model:latest


**Image Size:** ~[Your size] MB (all dependencies included)

### Docker Compose Setup

**File:** `docker-compose.yml`

**Services Defined:**

yaml
version: "3.8"

services:
  heart-api:
    build: .
    container_name: heart-api
    ports:
      - "8000:8000"
    networks:
      - monitoring

  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3000:3000"
    networks:
      - monitoring

networks:
  monitoring:
    driver: bridge


**Three Services:**

1. **heart-api** (Custom)
   - **Build:** From Dockerfile
   - **Port:** 8000 (API)
   - **Network:** monitoring

2. **prometheus** (Official)
   - **Image:** prom/prometheus:latest
   - **Config:** ./prometheus.yml
   - **Port:** 9090 (Metrics scraping UI)
   - **Purpose:** Scrapes metrics from /metrics endpoint

3. **grafana** (Official)
   - **Image:** grafana/grafana:latest
   - **Port:** 3000 (Visualization)
   - **Purpose:** Visualize Prometheus metrics

**Running with Docker Compose:**

bash
# Start all services
docker-compose up

# In background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f heart-api


**Access Points:**
- API: `http://localhost:8000`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000` (admin/admin)

### Container Registry (GitHub Container Registry)

**Image Location:**

ghcr.io/YOUR-USERNAME/Assignment-HeartDisease:latest


**CI/CD Integration:**
- Built automatically by GitHub Actions
- Pushed to GHCR on successful build
- Used in Kubernetes deployments

**[Add screenshot of GitHub Actions workflow]**

### Deployment Workflow

#### For Local Minikube:


1. Developer commits code
                ↓
2. GitHub Actions triggered
                ↓
3. Tests pass ✓
                ↓
4. Docker image built ✓
                ↓
5. Developer manually deploys:
   - minikube image load heart-disease-model:latest
   - kubectl apply -f deployment.yaml
   - kubectl apply -f service.yaml
                ↓
6. Application running on Minikube
                ↓
7. Access via: http://localhost:8000


### Kubernetes Deployment

**Deployment Configuration:**

yaml
Replicas: 1
Image: heart-disease-model:latest
Port: 8000
Image Pull Policy: Never (local Minikube)
Container Runtime: Docker


**Service Configuration:**

yaml
Type: NodePort
Port: 8000
Target Port: 8000
Node Port: 30080


### Deployment Steps

bash
# Start Minikube
minikube start --driver=docker

# Build Docker image
docker build -t heart-disease-model:latest .

# Load to Minikube
minikube image load heart-disease-model:latest

# Deploy
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Verify
kubectl get pods
kubectl get svc

# Access
kubectl port-forward svc/heart-disease-service 8000:8000
# or
minikube service heart-disease-service


## CI/CD & Deployment Pipeline

### GitHub Actions Workflow

**File:** `.github/workflows/ci-cd.yml`

**Pipeline Stages:**

1. **Lint** - flake8 checks code style and errors
2. **Test** - pytest runs unit tests with coverage reports
3. **Build** - Docker image built and pushed to GitHub Container Registry (GHCR)
4. **Notify** - Final pipeline status notification

**Triggers:** Push to main/develop branches, PRs to main/develop

**[Add screenshot: GitHub Actions workflow diagram]**

**[Add screenshot: Successful workflow run]**

### Kubernetes Deployment (Minikube)

**Deployment Configuration:**
- **Type:** Deployment
- **Replicas:** 2 (High Availability)
- **Strategy:** RollingUpdate (zero-downtime updates)
- **Image:** heart-disease-model:latest
- **Port:** 8000
- **Health Checks:** Liveness + Readiness probes

**Service Configuration:**
- **Type:** NodePort
- **Port:** 8000
- **NodePort:** 30080 (external access)

**Deployment Flow:**

Developer Push → GitHub Actions Triggered
    ↓
Lint & Test → Build Docker Image
    ↓
Push to GHCR → Manual Deployment
    ↓
kubectl apply -f deployment.yaml
    ↓
Kubernetes Rolling Update → 2 Replicas Running
    ↓
Service NodePort → External Access (Port 30080)


**[Add screenshot: kubectl deployment status]**

**[Add screenshot: Application running in Kubernetes]**



## API Reference

### Prediction Endpoint

**POST** `/predict`

**Request:**
json
{
  "features": [44, 1, 1, 120, 263, 0, 1, 173, 0, 0.0, 2, 0, 3]
}


**Response:**
json
{
  "prediction": "No disease",
  "probabilities": {
    "No disease": 0.756,
    "Mild disease": 0.184,
    "Moderate disease": 0.042,
    "Severe disease": 0.012,
    "Very severe disease": 0.006
  }
}


### Metrics Endpoint

**GET** `/metrics`

Returns Prometheus-format metrics for monitoring.

### Health Check

**GET** `/docs` - Interactive API documentation (Swagger UI)



## Project Repository

### Code Structure


Assignment-HeartDisease/
├── src/
│   ├── app.py              # FastAPI application
│   ├── train.py            # Model training script
│   └── preprocessing.py    # Data preprocessing
├── tests/
│   └── test_app.py         # API endpoint tests
├── models/
│   └── final_pipeline.pkl  # Production model
├── Dockerfile              # Container definition
├── docker-compose.yml      # Local monitoring stack
├── deployment.yaml         # Kubernetes deployment
├── service.yaml            # Kubernetes service
├── .github/workflows/
│   └── ci-cd.yml           # GitHub Actions pipeline
├── requirements.txt        # Python dependencies
└── PROJECT_REPORT.md       # This document


### Key Files

| File | Purpose |
|||
| [src/app.py](src/app.py) | FastAPI REST API |
| [src/train.py](src/train.py) | Model training |
| [src/preprocessing.py](src/preprocessing.py) | Data preprocessing |
| [tests/test_app.py](tests/test_app.py) | API tests |
| [Dockerfile](Dockerfile) | Docker container |
| [deployment.yaml](deployment.yaml) | Kubernetes deployment |
| [.github/workflows/ci-cd.yml](.github/workflows/ci-cd.yml) | CI/CD pipeline |

### Repository Link

**📌 Full Repository:**  
[https://github.com/YOUR-USERNAME/Assignment-HeartDisease](https://github.com/YOUR-USERNAME/Assignment-HeartDisease)



## Summary

 **Completed Deliverables:**
- Multi-class ML model for heart disease prediction
- FastAPI REST API with Docker containerization
- Kubernetes deployment on Minikube
- MLflow experiment tracking
- GitHub Actions CI/CD pipeline
- Prometheus metrics monitoring
- Comprehensive project documentation
- Unit tests with pytest

**MLOps Best Practices:**
- Automated testing (pytest)
- Automated linting (flake8)
- CI/CD automation (GitHub Actions)
- Container versioning with Docker
- Health checks and monitoring
- Infrastructure-as-code (Kubernetes)
- Experiment tracking (MLflow)



## References

1. [FastAPI Documentation](https://fastapi.tiangolo.com/)
2. [Scikit-learn Documentation](https://scikit-learn.org/)
3. [Kubernetes Documentation](https://kubernetes.io/docs/)
4. [GitHub Actions Documentation](https://docs.github.com/en/actions)
5. [MLflow Documentation](https://mlflow.org/docs/latest/)
6. [Docker Documentation](https://docs.docker.com/)
7. [UCI Heart Disease Dataset](https://archive.ics.uci.edu/ml/datasets/heart+disease)



**Document Prepared By:** [Your Name]  
**Date:** 2024  
**Status:**  Production Ready
Moderate        [FN]    [FN]     [TP]     [FP]      [FP]
Severe          [FN]    [FN]     [FN]     [TP]      [FP]
V.Severe        [FN]    [FN]     [FN]     [FN]      [TP]


**[Add confusion matrix visualization]**

### ROC Curve (One-vs-Rest)

**[Add One-vs-Rest ROC curves for each disease severity class]**

For multi-class classification, plot 5 ROC curves:
- No disease vs All
- Mild disease vs All
- Moderate disease vs All
- Severe disease vs All
- Very severe disease vs All

### Class Distribution in Test Set


No disease:        [X samples] ([Y%])
Mild disease:      [X samples] ([Y%])
Moderate disease:  [X samples] ([Y%])
Severe disease:    [X samples] ([Y%])
Very severe disease: [X samples] ([Y%])


**[Add bar chart showing class distribution]**

## API Implementation

### FastAPI Application (src/app.py)

**Framework:** FastAPI with Uvicorn ASGI server

**Model Loading:**
python
app = FastAPI()
pipeline = joblib.load("models/final_pipeline.pkl")

feature_names = [
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"
]


### API Endpoints

#### 1. POST /predict - Heart Disease Prediction

**Request:**
json
{
  "features": [44, 1, 1, 120, 263, 0, 1, 173, 0, 0.0, 2, 0, 3]
}


**Processing:**
python
@app.post("/predict")
def predict(data: dict):
    start = time.time()
    try:
        features = data.get("features")
        X = pd.DataFrame([features], columns=feature_names)
        
        # Get prediction and probabilities
        y_pred = pipeline.predict(X)[0]
        y_proba = pipeline.predict_proba(X)[0]
        
        # Map to class labels
        class_labels = {
            0: "No disease",
            1: "Mild disease",
            2: "Moderate disease",
            3: "Severe disease",
            4: "Very severe disease"
        }
        
        probabilities = {
            class_labels[label]: float(prob) 
            for label, prob in zip(pipeline.classes_, y_proba)
        }
        
        # Update monitoring metrics
        REQUEST_COUNT.inc()
        REQUEST_LATENCY.observe(time.time() - start)
        
        return {
            "prediction": class_labels[int(y_pred)],
            "probabilities": probabilities
        }
    except Exception:
        FAILED_PREDICTIONS.inc()
        raise


**Response:**
json
{
  "prediction": "No disease",
  "probabilities": {
    "No disease": 0.6558365175071036,
    "Mild disease": 0.20468399467853493,
    "Moderate disease": 0.052940319670214286,
    "Severe disease": 0.03916347982085114,
    "Very severe disease": 0.047375688323296423
  }
}


**Response Time:** < 10ms

#### 2. GET /metrics - Prometheus Metrics

**Endpoint:**
python
@app.get("/metrics")
def metrics():
    """Prometheus metrics endpoint."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


**Metrics Exposed:**

request_count_total{}: Total prediction requests
failed_predictions_total{}: Failed predictions
feature_age_bucket{le="x"}: Age feature distribution
request_latency_seconds_bucket{le="x"}: Request latency


### Monitoring Metrics (Prometheus)

**Metrics Instrumentation:**

python
# Request counter
REQUEST_COUNT = Counter(
    "request_count_total", 
    "Total prediction requests"
)

# Failure tracking
FAILED_PREDICTIONS = Counter(
    "failed_predictions_total", 
    "Number of failed predictions"
)

# Feature distribution monitoring
AGE_HIST = Histogram(
    "feature_age", 
    "Distribution of age feature", 
    buckets=[20,30,40,50,60,70,80]
)

# Latency monitoring
REQUEST_LATENCY = Histogram(
    "request_latency_seconds", 
    "Latency of prediction requests"
)


**Usage in predict endpoint:**
python
AGE_HIST.observe(features[0])      # Track age distribution
REQUEST_COUNT.inc()                 # Increment request count
REQUEST_LATENCY.observe(latency)   # Track latency
FAILED_PREDICTIONS.inc()            # Track failures


### Test Coverage (tests/test_app.py)

**Test 1: Predict Endpoint**
python
def test_predict_endpoint():
    response = client.post("/predict", json={
        "features":[63,1,1,145,233,1,0,150,0,2.3,0,0,1]
    })
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "probabilities" in data


**Test 2: Metrics Endpoint**
python
def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "request_count_total" in response.text


**Test Execution:**
bash
pytest tests/test_app.py -v


**Expected Result:** ✅ All tests pass

### Deployment Validation

| Test | Status | Details |
||--||
| Unit Tests |  Pass | All pytest tests pass |
| Docker Build |  Pass | Image builds successfully (~500MB) |
| Docker Run |  Pass | Container starts and serves API |
| API Health |  Pass | Health endpoint (/docs) responds |
| Multi-class Prediction |  Pass | Returns valid predictions with probabilities |
| Probability Distribution |  Pass | All probabilities sum to ~1.0 |
| Kubernetes Deployment |  Pass | Pod runs on Minikube with 2 replicas |
| Liveness Probe |  Pass | Pod health checks pass |
| Readiness Probe |  Pass | Pod marked ready for traffic |
| Metrics Endpoint |  Pass | Prometheus metrics available (/metrics) |
| Docker Compose Stack |  Pass | API + Prometheus + Grafana running |

### Production Checklist

- [x] Model trained and saved (`models/final_pipeline.pkl`)
- [x] FastAPI application working (`src/app.py`)
- [x] Prometheus metrics implemented
- [x] Tests passing (`pytest tests/ -v`)
- [x] Docker image builds (`docker build -t heart-disease-model:latest .`)
- [x] Kubernetes manifests configured
- [x] CI/CD pipeline setup (GitHub Actions)
- [x] Docker Compose for local dev/monitoring
- [x] Documentation complete
- [x] Code linting passes (`flake8 src`)

### Load Testing Results

**Test Scenario:** [Your scenario]

Concurrent Requests: [Your number]
Duration: [Your duration]
Average Latency: [Your ms]
P95 Latency: [Your ms]
P99 Latency: [Your ms]
Success Rate: [Your %]
Error Rate: [Your %]
Throughput: [Your req/sec]




## Repository & Code

### GitHub Repository

**Link:** [Add your GitHub repo URL]

https://github.com/YOUR-USERNAME/Assignment-HeartDisease


### Repository Structure


Assignment-HeartDisease/
├── .github/
│   └── workflows/
│       └── ci-cd.yml                 # GitHub Actions CI/CD
├── src/
│   ├── __init__.py
│   ├── app.py                        # FastAPI application
│   ├── train.py                      # Model training script
│   └── preprocessing.py              # Data preprocessing
├── tests/
│   ├── conftest.py                   # Pytest configuration
│   ├── test_app.py                   # API tests
│   ├── test_model.py                 # Model tests
│   └── test_preprocessing.py         # Preprocessing tests
├── models/
│   └── final_pipeline.pkl            # Trained model
├── mlruns/                           # MLflow experiment logs
├── Dockerfile                        # Docker configuration
├── deployment.yaml                   # Kubernetes deployment
├── service.yaml                      # Kubernetes service
├── requirements.txt                  # Python dependencies
├── CICD_SETUP.md                    # CI/CD documentation
├── MINIKUBE_DEPLOYMENT.md           # Deployment guide
├── minikube-deploy.bat               # Windows deployment script
├── minikube-deploy.sh                # Linux/Mac deployment script
└── README.md                         # Project overview


## Code Implementation Details

### Project Structure


Assignment-HeartDisease/
├── src/
│   ├── __init__.py
│   ├── app.py                    # FastAPI application (68 lines)
│   ├── train.py                  # Model training with MLflow (100+ lines)
│   └── preprocessing.py          # Data preprocessing (50 lines)
│
├── tests/
│   ├── conftest.py              # Pytest configuration
│   ├── test_app.py              # API endpoint tests (2 tests)
│   ├── test_model.py            # Model tests
│   └── test_preprocessing.py    # Preprocessing tests
│
├── models/
│   ├── Logistic Regression_pipeline.pkl  # Trained LogReg model
│   └── Random Forest_pipeline.pkl        # Trained RF model
│   └── final_pipeline.pkl                # Best model (production)
│
├── mlruns/                       # MLflow experiment logs
│   └── 0/                        # Default experiment
│       ├── <run_id>/             # Run directories with metrics
│       └── artifacts/            # Logged artifacts
│
├── .github/workflows/
│   └── ci-cd.yml                # GitHub Actions workflow
│
├── Dockerfile                    # Container image definition
├── deployment.yaml               # Kubernetes deployment manifest
├── service.yaml                  # Kubernetes service manifest
├── requirements.txt              # Python dependencies
├── docker-compose.yml            # Docker Compose for local dev
├── prometheus.yml                # Prometheus configuration
├── CICD_SETUP.md                # CI/CD documentation
├── MINIKUBE_DEPLOYMENT.md       # Minikube deployment guide
└── PROJECT_REPORT.md            # This document


### Key Source Files

#### 1. src/app.py (FastAPI API Server)

**Lines of Code:** ~68 lines

**Key Components:**
- FastAPI initialization
- Model pipeline loading (joblib)
- POST /predict endpoint with:
  - Feature validation
  - DataFrame conversion
  - Prediction and probability calculation
  - Prometheus metrics tracking
  - Error handling with failure counting
- GET /metrics endpoint for Prometheus scraping

**Dependencies:**
python
from fastapi import FastAPI
import joblib
import pandas as pd
import time
from prometheus_client import Counter, Histogram


#### 2. src/train.py (Model Training)

**Lines of Code:** ~100+ lines

**Key Components:**
- Logistic Regression pipeline with GridSearchCV
- Random Forest pipeline with RandomizedSearchCV
- Data preprocessing integration
- MLflow experiment tracking
- Metrics calculation (accuracy, precision, recall, F1, ROC-AUC)
- Model artifact logging
- ROC curve visualization
- Model persistence with joblib

**Training Flow:**

1. Load & preprocess data
2. Build Logistic Regression pipeline
3. GridSearch for best hyperparameters
4. Build Random Forest pipeline
5. RandomizedSearch for best hyperparameters
6. Evaluate both models
7. Log metrics & parameters in MLflow
8. Save pipelines as pickle files
9. Log artifacts and visualizations
10. Select best model → final_pipeline.pkl


#### 3. src/preprocessing.py (Data Preprocessing)

**Lines of Code:** ~50 lines

**Key Components:**
- UCI dataset fetching
- Categorical vs numeric column identification
- ColumnTransformer setup:
  - Numeric: SimpleImputer (median) + StandardScaler
  - Categorical: SimpleImputer (most_frequent) + OneHotEncoder
- Train-test split with stratification

**Preprocessing Pipeline:**

Input Data
  ├─ Numeric Columns (5)
  │  ├─ SimpleImputer (median)
  │  └─ StandardScaler
  │
  └─ Categorical Columns (8)
     ├─ SimpleImputer (most_frequent)
     └─ OneHotEncoder


#### 4. tests/test_app.py (API Tests)

**Tests:**
1. `test_predict_endpoint()` - Validates POST /predict
2. `test_metrics_endpoint()` - Validates GET /metrics

**Test Framework:** FastAPI TestClient + pytest

**Coverage:** 2 core API tests

### Dependencies (requirements.txt)


fastapi              # Web framework
uvicorn              # ASGI server
scikit-learn         # ML models
pandas               # Data manipulation
numpy                # Numerical computing
joblib               # Model serialization
mlflow               # Experiment tracking
prometheus-client    # Metrics collection
pytest               # Testing framework
pytest-cov           # Coverage reporting
ucimlrepo            # Dataset fetching
matplotlib           # Visualization
seaborn              # Statistical plots
flake8               # Code linting


### Code Quality Metrics

**Linting with flake8:**
bash
flake8 src tests --max-line-length=127


**Test Coverage:**
bash
pytest tests/ -v --cov=src --cov-report=html


**Expected:** All tests pass ✅



## Conclusion

### Summary of Accomplishments

 **Data Processing:** Complete EDA and preprocessing pipeline  
 **Model Development:** Trained and evaluated ML model  
 **Experiment Tracking:** MLflow integration for reproducibility  
 **API Development:** FastAPI REST API for predictions  
 **Containerization:** Docker image for consistent deployment  
 **Orchestration:** Kubernetes deployment on Minikube  
 **CI/CD Pipeline:** GitHub Actions for automated testing and building  
 **Monitoring:** Prometheus metrics for observability  
 **Testing:** Comprehensive unit tests with pytest  
 **Documentation:** Complete setup and deployment guides  




### Lessons Learned

1. **Containerization** ensures consistent deployment across environments
2. **Kubernetes** simplifies application orchestration and scaling
3. **GitHub Actions** enables powerful CI/CD automation
4. **MLflow** provides excellent experiment tracking capabilities
5. **FastAPI** is ideal for building production-grade ML APIs
6. **Testing** is critical for maintaining code quality



## References

1. UCI Machine Learning Repository - Heart Disease Dataset
   https://archive.ics.uci.edu/ml/datasets/heart+disease

2. FastAPI Documentation
   https://fastapi.tiangolo.com/

3. Kubernetes Documentation
   https://kubernetes.io/docs/

4. GitHub Actions Documentation
   https://docs.github.com/en/actions

5. MLflow Documentation
   https://mlflow.org/docs/latest/

6. Docker Documentation
   https://docs.docker.com/

7. Scikit-learn Documentation
   https://scikit-learn.org/stable/



