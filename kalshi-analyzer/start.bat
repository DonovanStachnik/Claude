@echo off
echo ============================================================
echo KALSHI ANALYZER - STARTING
echo ============================================================
echo.

cd /d "%~dp0"

REM Check if .env exists
if not exist ".env" (
    echo ERROR: No .env file found!
    echo Please add your Kalshi API credentials first.
    pause
    exit /b 1
)

REM Install dependencies
echo [1/3] Checking dependencies...
pip install -q -r requirements.txt flask flask-cors schedule
echo ✓ Dependencies ready
echo.

REM Create logs directory
if not exist "logs" mkdir logs

REM Start background scanner
echo [2/3] Starting background scanner...
cd src
start /B python background_scanner.py > ..\logs\scanner.log 2>&1
echo ✓ Scanner running
echo.

REM Wait a moment
timeout /t 5 /nobreak > nul

REM Start web dashboard
echo [3/3] Starting web dashboard...
start /B python web_dashboard.py > ..\logs\dashboard.log 2>&1
echo ✓ Dashboard running
echo.

echo ============================================================
echo ✓ KALSHI ANALYZER IS RUNNING
echo ============================================================
echo.
echo 📊 Dashboard: http://localhost:5000
echo 🔄 Scanner: Running every 15 minutes
echo.
echo Logs:
echo   Scanner: logs\scanner.log
echo   Dashboard: logs\dashboard.log
echo.
echo Press Ctrl+C to stop
echo ============================================================
echo.

REM Keep window open
pause
