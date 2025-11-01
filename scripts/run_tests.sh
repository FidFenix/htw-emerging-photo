#!/bin/bash
# Run tests

set -e

echo "🧪 Running tests..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run pytest
pytest tests/ -v

echo "✅ Tests complete!"

