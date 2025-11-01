#!/bin/bash
# Setup script for HTW Emerging Photo project

set -e

echo "🚀 Setting up HTW Emerging Photo project..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data/models
mkdir -p data/uploads
mkdir -p logs

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created. Please update it with your configuration."
else
    echo "✅ .env file already exists."
fi

# Download model weights (optional)
echo "🤖 Model weights will be downloaded on first run."

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Start backend: python main.py"
echo "  3. Start frontend: streamlit run frontend/app.py"
echo ""
echo "Or use Docker:"
echo "  docker-compose up --build"
echo ""

