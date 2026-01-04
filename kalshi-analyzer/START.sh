#!/bin/bash
#
# Kalshi Analyzer - Start Script
#
# Starts the background scanner and web dashboard
#

echo "===================================================================="
echo "KALSHI PREDICTION MARKET ANALYZER"
echo "===================================================================="
echo ""
echo "Starting services..."
echo ""

cd "$(dirname "$0")"

# Create directories
mkdir -p data logs

# Kill any existing instances
pkill -f background_scanner.py
pkill -f web_dashboard.py
sleep 1

# Start background scanner
cd src
echo "✓ Starting background scanner (scans every 15 minutes)"
nohup python3 background_scanner.py > ../logs/scanner.log 2>&1 &
SCANNER_PID=$!

sleep 2

# Start web dashboard
echo "✓ Starting web dashboard"
nohup python3 web_dashboard.py > ../logs/dashboard.log 2>&1 &
DASHBOARD_PID=$!

cd ..

echo ""
echo "===================================================================="
echo "✓ SYSTEM RUNNING"
echo "===================================================================="
echo ""
echo "📊 Dashboard: http://localhost:5000"
echo "📁 Data folder: ./data/"
echo "📋 Logs: ./logs/"
echo ""
echo "Background Scanner PID: $SCANNER_PID"
echo "Web Dashboard PID: $DASHBOARD_PID"
echo ""
echo "To stop all services:"
echo "  kill $SCANNER_PID $DASHBOARD_PID"
echo ""
echo "Or use: pkill -f background_scanner && pkill -f web_dashboard"
echo ""
echo "===================================================================="
echo ""
echo "The scanner will:"
echo "  • Try to fetch real Kalshi market data using your API credentials"
echo "  • Fall back to demo data if API is unreachable"
echo "  • Scan every 15 minutes automatically"
echo "  • Save opportunities to the data/ folder"
echo ""
echo "Open http://localhost:5000 in your browser to see the dashboard!"
echo "===================================================================="
