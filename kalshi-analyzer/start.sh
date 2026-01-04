#!/bin/bash

echo "============================================================"
echo "KALSHI ANALYZER - STARTING"
echo "============================================================"
echo ""

cd "$(dirname "$0")"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠ No .env file found!"
    echo "Please add your Kalshi API credentials first."
    exit 1
fi

# Install dependencies if needed
echo "[1/3] Checking dependencies..."
pip install -q -r requirements.txt flask flask-cors schedule
echo "✓ Dependencies ready"
echo ""

# Start background scanner
echo "[2/3] Starting background scanner..."
cd src
python background_scanner.py > ../logs/scanner.log 2>&1 &
SCANNER_PID=$!
echo "✓ Scanner running (PID: $SCANNER_PID)"
echo ""

# Wait a moment for first scan
sleep 5

# Start web dashboard
echo "[3/3] Starting web dashboard..."
python web_dashboard.py > ../logs/dashboard.log 2>&1 &
DASHBOARD_PID=$!
echo "✓ Dashboard running (PID: $DASHBOARD_PID)"
echo ""

echo "============================================================"
echo "✓ KALSHI ANALYZER IS RUNNING"
echo "============================================================"
echo ""
echo "📊 Dashboard: http://localhost:5000"
echo "🔄 Scanner: Running every 15 minutes"
echo ""
echo "Logs:"
echo "  Scanner: logs/scanner.log"
echo "  Dashboard: logs/dashboard.log"
echo ""
echo "To stop:"
echo "  kill $SCANNER_PID $DASHBOARD_PID"
echo ""
echo "Or use: pkill -f background_scanner && pkill -f web_dashboard"
echo "============================================================"

# Save PIDs
echo "$SCANNER_PID" > ../logs/scanner.pid
echo "$DASHBOARD_PID" > ../logs/dashboard.pid

# Keep script running
wait
