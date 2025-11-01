#!/bin/zsh
# Setup script for running HTW Emerging Photo locally with Conda

set -e

echo "🚀 Setting up HTW Emerging Photo with Conda..."

# Source conda from shell config
if [ -f ~/.zshrc ]; then
    source ~/.zshrc
fi

# Check if conda is available now
if ! command -v conda &> /dev/null; then
    echo "❌ Conda not found even after sourcing .zshrc"
    echo "   Please run 'conda init zsh' and restart your terminal"
    exit 1
fi

ENV_NAME="quick_htw"
PYTHON_VERSION="3.10"

echo "✓ Found conda: $(which conda)"
echo ""

# Check if environment exists
if conda env list | grep -q "^${ENV_NAME} "; then
    echo "📦 Environment '$ENV_NAME' already exists"
    echo "   Activating..."
else
    echo "📦 Creating conda environment '$ENV_NAME' with Python $PYTHON_VERSION..."
    conda create -n "$ENV_NAME" python="$PYTHON_VERSION" -y
fi

# Activate environment
echo "🔧 Activating environment..."
conda activate "$ENV_NAME"

# Install PyTorch (CPU version for now)
echo "🔥 Installing PyTorch..."
pip install torch torchvision torchaudio

# Install other dependencies
echo "📚 Installing other dependencies..."
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
echo "  1. conda activate $ENV_NAME"
echo "  2. python main.py &"
echo "  3. streamlit run frontend/app.py"
echo ""
echo "Or run: conda activate $ENV_NAME && ./run_local_simple.sh"

