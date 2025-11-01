#!/bin/bash
# Setup script for running HTW Emerging Photo locally on Mac

set -e

echo "🚀 Setting up HTW Emerging Photo for local development..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Found Python $PYTHON_VERSION"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies (this may take a few minutes)..."
pip install -r requirements.txt

# Create data directories
echo "📁 Creating data directories..."
mkdir -p data/models
mkdir -p data/uploads

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  1. Activate the environment: source venv/bin/activate"
echo "  2. Start the backend: python main.py &"
echo "  3. Start the frontend: streamlit run frontend/app.py"
echo ""
echo "Or simply run: ./run_local.sh"

