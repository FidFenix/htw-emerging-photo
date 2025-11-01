#!/bin/bash
# Run the Streamlit frontend

set -e

echo "🚀 Starting HTW Emerging Photo Frontend..."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Set API URL if not set
export API_URL=${API_URL:-"http://localhost:8000/api/v1"}

# Run Streamlit
streamlit run frontend/app.py --server.port=8501 --server.address=0.0.0.0

