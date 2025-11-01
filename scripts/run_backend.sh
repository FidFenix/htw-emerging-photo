#!/bin/bash
# Run the FastAPI backend

set -e

echo "🚀 Starting HTW Emerging Photo Backend..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found. Using defaults."
fi

# Run the application
python main.py

