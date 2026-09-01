#!/bin/bash
# Sarvagya - One-Click Launcher for Mac/Linux/Unix
# This script starts both backend and frontend in the background

# Set API key
export GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

clear
echo "================================================================"
echo "                     SARVAGYA LAUNCHER"
echo "           AI Trading Chart Analysis Platform"
echo "================================================================"
echo ""
echo "Starting Sarvagya..."
echo ""
echo "Backend will start on: http://localhost:8000"
echo "Frontend will start on: http://localhost:3000"
echo ""
echo "================================================================"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Start Backend
echo "[1/2] Starting Backend..."
cd "$SCRIPT_DIR/backend"

# Activate venv based on OS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Start backend in background
python main.py > backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend started (PID: $BACKEND_PID)"

# Wait for backend to initialize
sleep 5

# Start Frontend
echo "[2/2] Starting Frontend..."
cd "$SCRIPT_DIR/frontend"
npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend started (PID: $FRONTEND_PID)"

# Wait for frontend to initialize
sleep 10

# Open browser
echo "[3/3] Opening browser..."
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:3000 &
elif command -v open > /dev/null; then
    open http://localhost:3000 &
else
    echo "Please manually open: http://localhost:3000"
fi

echo ""
echo "================================================================"
echo ""
echo -e "${GREEN}Sarvagya is running!${NC}"
echo ""
echo "Backend: http://localhost:8000 (PID: $BACKEND_PID)"
echo "Frontend: http://localhost:3000 (PID: $FRONTEND_PID)"
echo ""
echo "Logs:"
echo "  Backend:  $SCRIPT_DIR/backend/backend.log"
echo "  Frontend: $SCRIPT_DIR/frontend/frontend.log"
echo ""
echo "To stop Sarvagya, press Ctrl+C"
echo ""
echo "================================================================"
echo ""

# Save PIDs for cleanup
echo $BACKEND_PID > /tmp/sarvagya_backend.pid
echo $FRONTEND_PID > /tmp/sarvagya_frontend.pid

# Wait for user interrupt
trap "echo ''; echo 'Stopping Sarvagya...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; rm -f /tmp/sarvagya_*.pid; echo 'Stopped.'; exit" INT TERM

# Keep script running
wait
