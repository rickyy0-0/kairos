#!/usr/bin/env bash
set -e

echo "================================================================="
echo "  KAIROS — Urban Heat Intelligence & Response System"
echo "  From Heat Detection → Cause Analysis → Impact → Optimal Cooling"
echo "================================================================="

# Start Backend
echo "[1/2] Starting Python FastAPI backend on http://localhost:8000..."
./backend/venv/bin/python backend/main.py &
BACKEND_PID=$!

# Start Frontend
echo "[2/2] Starting Vite React frontend on http://localhost:5173..."
npm run dev --prefix frontend &
FRONTEND_PID=$!

cleanup() {
  echo ""
  echo "Shutting down KAIROS servers..."
  kill $BACKEND_PID 2>/dev/null || true
  kill $FRONTEND_PID 2>/dev/null || true
  exit 0
}

trap cleanup SIGINT SIGTERM EXIT

echo ""
echo ">>> KAIROS is now live at http://localhost:5173 <<<"
echo ">>> API Documentation at http://localhost:8000/docs <<<"
echo "Press Ctrl+C to stop both servers."
echo ""

wait
