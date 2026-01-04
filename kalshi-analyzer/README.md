# Kalshi Prediction Market Analyzer

Automated system to find the best betting opportunities on Kalshi prediction markets.

## Features

- **Real-time Market Scanning**: Scans all Kalshi markets every 15 minutes
- **Independent Research**: Conducts research across multiple categories (sports, politics, economics, weather, crypto)
- **Edge Detection**: Identifies mispriced markets by comparing true probability vs market price
- **Web Dashboard**: Clean interface displaying top opportunities ranked by expected value
- **Automatic Fallback**: Uses demo data if Kalshi API is unreachable (for testing)

## Quick Start

```bash
# Make START script executable (first time only)
chmod +x START.sh

# Start the system
./START.sh
```

Then open **http://localhost:5000** in your browser.

## What's Included

### Core Components

- **kalshi_client_rsa.py**: Handles RSA authentication and API requests to Kalshi
- **main_analyzer.py**: Main scanner that finds opportunities
- **research_engine.py**: Independent research across market categories
- **background_scanner.py**: Runs continuous scans every 15 minutes
- **web_dashboard.py**: Flask web server for the dashboard

### Configuration Files

- **kalshi_private.key**: Your RSA private key (already configured)
- **.env**: Environment variables (Key ID, filters)
- **requirements.txt**: Python dependencies

### Data & Logs

- **data/**: Opportunity files saved as JSON with timestamps
- **logs/**: Scanner and dashboard logs

## How It Works

1. **Authentication**: Uses RSA-PSS signing to authenticate with Kalshi API
2. **Market Fetching**: Retrieves all open markets
3. **Categorization**: Organizes markets by type (sports, politics, etc.)
4. **Research**: Conducts independent research to calculate true probabilities
5. **Edge Calculation**: Compares market price vs true probability
6. **Filtering**: Keeps only opportunities meeting criteria (min 5% edge, 60% confidence)
7. **Ranking**: Sorts by expected value (edge × confidence)
8. **Display**: Shows top opportunities on dashboard

## Dashboard

The dashboard displays:

- **Stats**: Total opportunities, average edge, categories breakdown
- **Opportunity Cards**: Market title, recommendation, probabilities, edge, confidence, reasoning

Auto-refreshes every 60 seconds.

## Network Note

In environments with restricted network access, the system automatically falls back to demo data. When running on your local machine with proper internet access, it will use **real Kalshi market data**.

## Stopping the System

```bash
pkill -f background_scanner && pkill -f web_dashboard
```

**Built for automated trading on Kalshi prediction markets**
