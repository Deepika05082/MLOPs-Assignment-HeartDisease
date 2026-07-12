@echo off
REM CI/CD Pipeline Setup Script for Windows

echo.
echo  Heart Disease ML - CI/CD Pipeline Setup
echo ===========================================
echo.

REM Step 1: Create GitHub workflow directory
echo 📁 Creating GitHub Actions workflow directory...
if not exist ".github\workflows" mkdir ".github\workflows"

REM Step 2: Check if workflow file exists
if exist ".github\workflows\ci-cd.yml" (
    echo  Workflow file already exists at .github\workflows\ci-cd.yml
) else (
    echo ❌ Workflow file not found. Please ensure it's created.
    exit /b 1
)

REM Step 3: Check Python
echo.
echo  Checking Python environment...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.10+
    exit /b 1
)

REM Step 4: Install dependencies
echo.
echo  Installing test dependencies...
pip install pytest pytest-cov flake8

REM Step 5: Run tests
echo.
echo 🧪 Running local tests...
python -m pytest tests\ -v
if %errorlevel% neq 0 (
    echo ❌ Some tests failed. Please fix them before pushing.
    exit /b 1
)
echo  All tests passed!

REM Step 6: Run linting
echo.
echo 🔍 Running code linting...
flake8 src tests --max-line-length=127 --exit-zero
echo  Linting complete!

REM Step 7: Build Docker image
echo.
echo  Building Docker image locally...
docker build -t heart-disease-model:local .
if %errorlevel% neq 0 (
    echo ❌ Docker build failed. Please check Dockerfile.
    exit /b 1
)
echo  Docker image built successfully!

REM Step 8: Display next steps
echo.
echo ===========================================
echo  Local setup complete!
echo.
echo  Next steps:
echo.
echo 1. Update deployment image URL:
echo    Edit deployment.yaml and set:
echo    image: ghcr.io/YOUR-USERNAME/YOUR-REPO:latest
echo.
echo 2. Add GitHub secrets:
echo    - Go to GitHub repo ^> Settings ^> Secrets ^> Actions
echo    - Add 'KUBE_CONFIG' (base64 encoded kubeconfig)
echo.
echo 3. Commit and push to main:
echo    git add .
echo    git commit -m "Add CI/CD pipeline"
echo    git push origin main
echo.
echo 4. Monitor pipeline:
echo    - Go to repository ^> Actions tab
echo    - Click on your workflow run to see detailed logs
echo.
echo 5. For Kubernetes deployment:
echo    kubectl apply -f deployment-cicd.yaml
echo    kubectl get pods
echo    kubectl logs -f deployment/heart-disease-model
echo.
echo ===========================================
