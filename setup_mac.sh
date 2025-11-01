#!/bin/bash
# Setup script for running HTW Emerging Photo on Mac with MPS GPU support

set -e

echo "🚀 Setting up HTW Emerging Photo for Mac with MPS GPU support..."

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Conda not found. Please install Miniconda or Anaconda first."
    echo "   Download from: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# Create conda environment
echo "📦 Creating conda environment 'quick-htw'..."
conda create -n quick-htw python=3.10 -y

# Activate environment
echo "🔧 Activating environment..."
eval "$(conda shell.bash hook)"
conda activate quick-htw

# Install dependencies
echo "📚 Installing dependencies..."
pip install --upgrade pip
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
echo "  1. Activate the environment: conda activate quick-htw"
echo "  2. Start the backend: python main.py"
echo "  3. In another terminal, start the frontend: streamlit run frontend/app.py"
echo ""
echo "The application will use MPS (Apple Silicon GPU) for acceleration."

