#!/bin/bash
# Verify HTW Emerging Photo installation

set -e

echo "🔍 HTW Emerging Photo - Installation Verification"
echo "=================================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check function
check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
        return 0
    else
        echo -e "${RED}✗${NC} $1"
        return 1
    fi
}

# Check Python version
echo "Checking Python version..."
python3 --version | grep -q "3.10\|3.11\|3.12"
check "Python 3.10+ installed"

# Check pip
echo "Checking pip..."
pip --version > /dev/null 2>&1
check "pip installed"

# Check virtual environment
echo "Checking virtual environment..."
if [ -d "venv" ]; then
    echo -e "${GREEN}✓${NC} Virtual environment exists"
else
    echo -e "${YELLOW}⚠${NC} Virtual environment not found (run: make setup)"
fi

# Check .env file
echo "Checking configuration..."
if [ -f ".env" ]; then
    echo -e "${GREEN}✓${NC} .env file exists"
else
    echo -e "${YELLOW}⚠${NC} .env file not found (will use defaults)"
fi

# Check directory structure
echo "Checking directory structure..."
[ -d "src" ] && check "src/ directory exists"
[ -d "frontend" ] && check "frontend/ directory exists"
[ -d "tests" ] && check "tests/ directory exists"
[ -d "docs" ] && check "docs/ directory exists"
[ -d "scripts" ] && check "scripts/ directory exists"
[ -d "data/models" ] && check "data/models/ directory exists"
[ -d "data/uploads" ] && check "data/uploads/ directory exists"

# Check key files
echo "Checking key files..."
[ -f "main.py" ] && check "main.py exists"
[ -f "requirements.txt" ] && check "requirements.txt exists"
[ -f "Dockerfile" ] && check "Dockerfile exists"
[ -f "docker-compose.yml" ] && check "docker-compose.yml exists"
[ -f "README.md" ] && check "README.md exists"

# Check source files
echo "Checking source code..."
[ -f "src/api/app.py" ] && check "API app exists"
[ -f "src/detection/faces/detector.py" ] && check "Face detector exists"
[ -f "src/detection/plates/detector.py" ] && check "Plate detector exists"
[ -f "src/anonymization/anonymizer.py" ] && check "Anonymizer exists"
[ -f "frontend/app.py" ] && check "Frontend app exists"

# Check Docker (optional)
echo "Checking Docker (optional)..."
if command -v docker &> /dev/null; then
    docker --version > /dev/null 2>&1
    check "Docker installed"
    
    if command -v docker-compose &> /dev/null; then
        docker-compose --version > /dev/null 2>&1
        check "Docker Compose installed"
    else
        echo -e "${YELLOW}⚠${NC} Docker Compose not found (optional)"
    fi
else
    echo -e "${YELLOW}⚠${NC} Docker not found (optional, but recommended)"
fi

# Check if dependencies are installed (if venv exists)
if [ -d "venv" ]; then
    echo "Checking Python dependencies..."
    source venv/bin/activate
    
    python -c "import fastapi" 2>/dev/null && check "FastAPI installed" || echo -e "${RED}✗${NC} FastAPI not installed"
    python -c "import streamlit" 2>/dev/null && check "Streamlit installed" || echo -e "${RED}✗${NC} Streamlit not installed"
    python -c "import torch" 2>/dev/null && check "PyTorch installed" || echo -e "${RED}✗${NC} PyTorch not installed"
    python -c "import cv2" 2>/dev/null && check "OpenCV installed" || echo -e "${RED}✗${NC} OpenCV not installed"
    
    deactivate
fi

echo ""
echo "=================================================="
echo "Verification complete!"
echo ""
echo "Next steps:"
echo "  1. If virtual environment not found: make setup"
echo "  2. If dependencies missing: make install"
echo "  3. To run with Docker: make run-docker"
echo "  4. To run locally: make run-backend (Terminal 1) + make run-frontend (Terminal 2)"
echo ""
echo "For more information, see:"
echo "  - README.md"
echo "  - QUICKSTART.md"
echo "  - docs/DEPLOYMENT.md"
echo ""

