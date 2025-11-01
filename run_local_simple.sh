#!/bin/bash
# Run HTW Emerging Photo locally

set -e

echo "🚀 Starting HTW Emerging Photo..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found."
    echo "   Please run: ./setup_local.sh"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Start backend in background
echo "🔧 Starting backend API on port 8000..."
python main.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Check if backend is running
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ Backend failed to start. Check backend.log for errors."
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

echo "✅ Backend started successfully!"
echo ""
echo "🎨 Starting frontend on port 8501..."
echo ""
echo "📱 Open your browser to: http://localhost:8501"
echo "   API available at: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both services"
echo ""

# Set API_URL for frontend
export API_URL=http://localhost:8000/api/v1

# Start frontend (this will run in foreground)
streamlit run frontend/app.py

# Cleanup: kill backend when frontend stops
echo ""
echo "🛑 Stopping backend..."
kill $BACKEND_PID 2>/dev/null || true
echo "✅ All services stopped"

