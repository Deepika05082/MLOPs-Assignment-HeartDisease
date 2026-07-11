# CI/CD Pipeline Setup Guide

## Overview
This CI/CD pipeline automates testing, building, and deployment of your Heart Disease ML model using GitHub Actions.

## Pipeline Stages

### 1. **Lint** (Code Quality)
- Runs `flake8` to check code syntax and style
- Ensures code quality before testing

### 2. **Test** (Unit Tests)
- Runs all pytest tests in the `tests/` directory
- Generates coverage reports
- Uploads coverage to Codecov
- Only proceeds if linting passes

### 3. **Build** (Docker Image)
- Builds Docker image using your Dockerfile
- Pushes to GitHub Container Registry (GHCR)
- Only proceeds if tests pass
- Skips push on pull requests (dry run only)

### 4. **Deploy** (Kubernetes)
- Deploys only on `main` branch push
- Applies Kubernetes manifests (deployment.yaml, service.yaml)
- Monitors rollout status
- Requires kubeconfig secret

### 5. **Notify** (Status Check)
- Validates all previous jobs
- Fails if any previous stage failed

## Prerequisites

### 1. Enable GitHub Actions
- Go to your repository → Settings → Actions → General
- Ensure "Allow all actions and reusable workflows" is selected

### 2. Configure Secrets
Add these secrets to your repository (Settings → Secrets and variables → Actions):

```
KUBE_CONFIG: <base64 encoded kubeconfig>
DOCKER_REGISTRY_PASSWORD: <if using private registry>
```

**To encode kubeconfig:**
```bash
cat ~/.kube/config | base64 | tr -d '\n'
```

### 3. Update deployment.yaml
Update the image name in your `deployment.yaml`:

```yaml
image: ghcr.io/<your-username>/<your-repo>:sha-<commit-hash>
```

## Setup Steps

### Step 1: Push workflow file
The workflow file is already created at `.github/workflows/ci-cd.yml`

### Step 2: Create tests directory structure
Ensure your `tests/` directory has:
- `conftest.py` (pytest configuration)
- `test_app.py` (API tests)
- `test_model.py` (model tests)
- `test_preprocessing.py` (preprocessing tests)

### Step 3: Configure GitHub secrets
```bash
# Get your kubeconfig in base64
cat ~/.kube/config | base64

# Add as KUBE_CONFIG secret in GitHub
```

### Step 4: Test locally before pushing
```bash
# Lint
flake8 src tests

# Test
pytest tests/ -v

# Build Docker image
docker build -t heart-disease-model:latest .

# Run Docker container
docker run -p 8000:8000 heart-disease-model:latest
```

## Manual Triggers

You can manually trigger the pipeline via GitHub Actions tab:

```bash
# Or via GitHub CLI
gh workflow run ci-cd.yml
```

## Monitoring

### View pipeline status
1. Go to repository → Actions tab
2. Select workflow run to see detailed logs
3. Check each job for failures

### View deployment status
```bash
kubectl get deployments
kubectl get pods
kubectl logs -f deployment/heart-disease-model
```

## Customization

### Change branch triggers
Edit `.github/workflows/ci-cd.yml`:
```yaml
on:
  push:
    branches: [ main, develop, production ]  # Add branches
  pull_request:
    branches: [ main ]
```

### Disable deploy job
Comment out the `deploy` job or modify the condition:
```yaml
if: github.ref == 'refs/heads/main' && github.event_name == 'push'
```

### Add notifications (Slack/Email)
```yaml
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## Troubleshooting

### Docker login fails
- Verify `GITHUB_TOKEN` is available (automatic)
- Check repository settings for Actions permissions

### Kubernetes deployment fails
- Verify kubeconfig is correctly encoded and added as secret
- Check cluster connectivity: `kubectl cluster-info`
- Verify RBAC permissions

### Tests fail locally but pass in CI
- Check Python version matches (3.10)
- Verify all dependencies in requirements.txt
- Check for environment-specific issues

### Pod stays in pending
```bash
kubectl describe pod <pod-name>
kubectl get events
```

## Next Steps

1. Push this workflow to your repository
2. Add GitHub secrets (KUBE_CONFIG if deploying)
3. Create/update your tests
4. Commit and push to trigger the pipeline
5. Monitor via GitHub Actions tab

