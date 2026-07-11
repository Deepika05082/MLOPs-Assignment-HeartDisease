#!/bin/bash
# CI/CD Pipeline Setup Script

set -e

echo "🚀 Heart Disease ML - CI/CD Pipeline Setup"
echo "==========================================="
echo ""

# Step 1: Create GitHub workflow directory if it doesn't exist
echo "📁 Creating GitHub Actions workflow directory..."
mkdir -p .github/workflows

# Step 2: Check if workflow file exists
if [ -f ".github/workflows/ci-cd.yml" ]; then
    echo "✅ Workflow file already exists at .github/workflows/ci-cd.yml"
else
    echo "❌ Workflow file not found. Please ensure it's created."
    exit 1
fi

# Step 3: Validate Python environment
echo ""
echo "🐍 Checking Python environment..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✅ Python version: $python_version"

# Step 4: Install dependencies for testing
echo ""
echo "📦 Installing test dependencies..."
pip install pytest pytest-cov flake8

# Step 5: Run local tests
echo ""
echo "🧪 Running local tests..."
if python -m pytest tests/ -v; then
    echo "✅ All tests passed!"
else
    echo "❌ Some tests failed. Please fix them before pushing."
    exit 1
fi

# Step 6: Run linting
echo ""
echo "🔍 Running code linting..."
if flake8 src tests --max-line-length=127 --exit-zero; then
    echo "✅ Linting complete!"
else
    echo "⚠️  Linting warnings found (non-blocking)"
fi

# Step 7: Build Docker image locally
echo ""
echo "🐳 Building Docker image locally..."
if docker build -t heart-disease-model:local .; then
    echo "✅ Docker image built successfully!"
else
    echo "❌ Docker build failed. Please check Dockerfile."
    exit 1
fi

# Step 8: Display next steps
echo ""
echo "==========================================="
echo "✅ Local setup complete!"
echo ""
echo "📋 Next steps:"
echo ""
echo "1. Update deployment image URL:"
echo "   Edit deployment.yaml and set:"
echo "   image: ghcr.io/YOUR-USERNAME/YOUR-REPO:latest"
echo ""
echo "2. Add GitHub secrets:"
echo "   - Go to GitHub repo → Settings → Secrets → Actions"
echo "   - Add 'KUBE_CONFIG' (base64 encoded kubeconfig)"
echo ""
echo "3. Commit and push to main:"
echo "   git add ."
echo "   git commit -m 'Add CI/CD pipeline'"
echo "   git push origin main"
echo ""
echo "4. Monitor pipeline:"
echo "   - Go to repository → Actions tab"
echo "   - Click on your workflow run to see detailed logs"
echo ""
echo "5. For Kubernetes deployment:"
echo "   kubectl apply -f deployment-cicd.yaml"
echo "   kubectl get pods"
echo "   kubectl logs -f deployment/heart-disease-model"
echo ""
echo "==========================================="
