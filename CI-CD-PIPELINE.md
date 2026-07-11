# CI/CD Pipeline for Heart Disease ML Model

A complete automated CI/CD pipeline using GitHub Actions for your FastAPI ML application with Docker and Kubernetes deployment.

## 📊 Pipeline Overview

```
┌─────────────────────────────────────────────────────────┐
│                 GitHub Actions Workflow                  │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  Trigger: Push to main/develop or Pull Request          │
│           │                                              │
│           ├── 🔍 LINT (Code Quality)                    │
│           │    └─ flake8 checks                         │
│           │                                              │
│           ├── 🧪 TEST (Unit Tests)                      │
│           │    ├─ pytest runs                           │
│           │    └─ Coverage reports                      │
│           │                                              │
│           ├── 🐳 BUILD (Docker Image)                   │
│           │    ├─ Build image                           │
│           │    └─ Push to GHCR                          │
│           │                                              │
│           └── 🚀 DEPLOY (Kubernetes)                    │
│                ├─ Apply manifests                       │
│                └─ Rollout verification                  │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Windows
```powershell
.\setup-cicd.bat
```

### Linux/Mac
```bash
chmod +x setup-cicd.sh
./setup-cicd.sh
```

## 📁 Files Created/Modified

| File | Purpose |
|------|---------|
| `.github/workflows/ci-cd.yml` | Main GitHub Actions workflow |
| `deployment-cicd.yaml` | Production-ready K8s deployment |
| `CICD_SETUP.md` | Detailed setup documentation |
| `setup-cicd.sh` | Linux/Mac setup script |
| `setup-cicd.bat` | Windows setup script |

## 🔧 Prerequisites

- ✅ GitHub repository with Actions enabled
- ✅ Docker installed locally
- ✅ Python 3.10+
- ✅ (Optional) Kubernetes cluster for deployment
- ✅ (Optional) kubectl configured

## 📋 Setup Instructions

### Step 1: Verify Files
All files are already created in your repository:
```
.github/workflows/ci-cd.yml        ✅
deployment-cicd.yaml               ✅
CICD_SETUP.md                      ✅
```

### Step 2: Configure GitHub Secrets

#### Option A: Using GitHub Web UI
1. Go to your repository → **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
3. For Kubernetes deployment only:
   - Name: `KUBE_CONFIG`
   - Value: (base64 encoded kubeconfig - see below)

#### Option B: Get Your Kubeconfig
```bash
# On your machine with kubectl configured
cat ~/.kube/config | base64

# Copy the output and paste as KUBE_CONFIG secret in GitHub
```

### Step 3: Update Deployment Configuration

Edit `deployment.yaml` or use `deployment-cicd.yaml`:

```yaml
image: ghcr.io/YOUR-GITHUB-USERNAME/YOUR-REPO-NAME:latest
```

### Step 4: Test Locally (Optional but Recommended)

```bash
# Run lint
flake8 src tests

# Run tests
pytest tests/ -v

# Build Docker image
docker build -t heart-disease-model:test .

# Run container
docker run -p 8000:8000 heart-disease-model:test
```

### Step 5: Commit and Push

```bash
git add .
git commit -m "Add CI/CD pipeline with GitHub Actions"
git push origin main
```

### Step 6: Monitor Pipeline

1. Go to your GitHub repository
2. Click on **Actions** tab
3. Select your workflow run
4. Watch the pipeline execute

## 🔄 Pipeline Stages Explained

### 1️⃣ Lint Stage
- **Runs:** `flake8` on all Python files
- **Fails if:** Syntax errors or undefined names found
- **Purpose:** Ensure code quality before testing

### 2️⃣ Test Stage
- **Runs:** `pytest` on `tests/` directory
- **Generates:** Coverage reports
- **Uploads:** Results to Codecov
- **Purpose:** Validate functionality and catch bugs

### 3️⃣ Build Stage
- **Builds:** Docker image from `Dockerfile`
- **Tags:** Image with commit SHA and branch name
- **Pushes:** To GitHub Container Registry (GHCR)
- **Skips push:** On pull requests (dry run only)
- **Purpose:** Create deployable artifact

### 4️⃣ Deploy Stage
- **Triggers:** Only on `main` branch push
- **Deploys:** Using `deployment-cicd.yaml`
- **Verifies:** Kubernetes rollout status
- **Requires:** `KUBE_CONFIG` secret configured
- **Purpose:** Automated deployment to cluster

### 5️⃣ Notify Stage
- **Checks:** All previous job statuses
- **Fails if:** Any previous stage failed
- **Purpose:** Final validation and reporting

## 📊 View Logs and Results

### GitHub Actions Logs
```bash
# Via GitHub CLI
gh run list
gh run view <run-id>
gh run view <run-id> --log

# Via Web UI
1. Repository → Actions
2. Select workflow run
3. Click job to expand logs
```

### Kubernetes Logs
```bash
# Check deployment status
kubectl get deployments
kubectl get pods

# View application logs
kubectl logs -f deployment/heart-disease-model

# Check pod events
kubectl describe pod <pod-name>

# Check service
kubectl get svc
```

### Docker Logs (Local)
```bash
# Build image
docker build -t heart-disease-model .

# Run with logs
docker run --rm -it heart-disease-model

# Run with port mapping
docker run -p 8000:8000 heart-disease-model
```

## 🔐 Security Best Practices

1. **Never commit secrets** (kubeconfig, credentials)
2. **Use GitHub Secrets** for sensitive data
3. **Enable branch protection** on main
4. **Review pull requests** before merge
5. **Use non-root container** user (already configured)
6. **Enable image scanning** in GHCR settings

## 🐛 Troubleshooting

### Pipeline fails at Lint stage
```bash
# Fix locally
flake8 src tests --show-source
# Make corrections and commit
```

### Pipeline fails at Test stage
```bash
# Run locally
pytest tests/ -v
# Check test output and fix issues
```

### Docker build fails
```bash
# Test locally
docker build -t test .
# Check Dockerfile syntax and dependencies
```

### Kubernetes deployment fails
```bash
# Verify kubeconfig is set
kubectl cluster-info

# Check if secret is properly configured
echo $KUBE_CONFIG | base64 --decode | kubectl apply -f -

# Check pod logs
kubectl logs <pod-name>
```

### GHCR login issues
- Verify `GITHUB_TOKEN` secret exists (auto-created by GitHub)
- Check repository Actions permissions
- Verify Docker registry settings

## 📈 Monitoring & Observability

### Built-in Metrics (from app.py)
- Request count: `request_count_total`
- Failed predictions: `failed_predictions_total`
- Feature distribution: `feature_age`

### View Metrics
```bash
# From within container
curl http://localhost:8000/metrics

# From Prometheus (if configured)
# Visit http://prometheus:9090
```

### Configure Prometheus
```bash
# Already have prometheus.yml
# Update to scrape your Kubernetes service:
- job_name: 'heart-disease-model'
  kubernetes_sd_configs:
    - role: pod
```

## 🎯 Next Steps

1. ✅ Review [CICD_SETUP.md](CICD_SETUP.md) for detailed documentation
2. ✅ Set GitHub secrets if deploying to Kubernetes
3. ✅ Test locally using setup script
4. ✅ Push changes to trigger pipeline
5. ✅ Monitor via GitHub Actions dashboard
6. ✅ Set up Slack notifications (optional)
7. ✅ Configure auto-scaling (optional)

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [MLflow Documentation](https://mlflow.org/)

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review GitHub Actions logs
3. Check Kubernetes pod events
4. Review CICD_SETUP.md

---

**Last Updated:** 2024
**Pipeline Version:** 1.0
**Status:** ✅ Production Ready
