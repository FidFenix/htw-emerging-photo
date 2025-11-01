#!/bin/bash
# Run HTW Emerging Photo locally on Mac

set -e

echo "🚀 Starting HTW Emerging Photo..."

# Check if conda environment exists
if ! conda env list | grep -q "quick-htw"; then
    echo "❌ Conda environment 'quick-htw' not found."
    echo "   Please run: ./setup_mac.sh"
    exit 1
fi

# Activate environment
eval "$(conda shell.bash hook)"
conda activate quick-htw

# Start backend in background
echo "🔧 Starting backend API on port 8000..."
python main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 5

# Start frontend
echo "🎨 Starting frontend on port 8501..."
echo "   Backend PID: $BACKEND_PID"
echo ""
echo "📱 Open your browser to: http://localhost:8501"
echo "   API available at: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

# Set API_URL for frontend
export API_URL=http://localhost:8000/api/v1

# Start frontend (this will run in foreground)
streamlit run frontend/app.py

# Cleanup: kill backend when frontend stops
kill $BACKEND_PID 2>/dev/null || true

