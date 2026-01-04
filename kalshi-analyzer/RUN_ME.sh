#!/bin/bash

echo "============================================================"
echo "KALSHI ANALYZER - QUICK START"
echo "============================================================"
echo ""
echo "Installing dependencies..."
pip install -q requests python-dotenv cryptography flask flask-cors schedule
echo "✓ Dependencies installed"
echo ""

cd "$(dirname "$0")"

# Setup already done, credentials stored
echo "Credentials: ✓ Already configured"
echo ""

# Create data/logs directories
mkdir -p data logs

echo "Starting system..."
echo ""
echo "1. Background Scanner - Scanning markets every 15 min"
echo "2. Web Dashboard - http://localhost:5000"
echo ""

cd src
python background_scanner.py > ../logs/scanner.log 2>&1 &
SCANNER_PID=$!
sleep 2
python web_dashboard.py &
DASHBOARD_PID=$!

echo "============================================================"
echo "✓ SYSTEM RUNNING"
echo "============================================================"
echo ""
echo "📊 Open browser: http://localhost:5000"
echo ""
echo "Scanner PID: $SCANNER_PID"
echo "Dashboard PID: $DASHBOARD_PID"
echo ""
echo "To stop:"
echo "  kill $SCANNER_PID $DASHBOARD_PID"
echo "============================================================"
echo ""
echo "Waiting for first scan (this takes ~1 minute)..."
echo "Then open http://localhost:5000 to see opportunities!"
echo ""

# Keep running
wait
