# START HERE - Automated Setup

## Step 1: Give Me Your API Credentials

Just paste your Kalshi API key and secret when you're ready.

## Step 2: I'll Run These Commands

```bash
cd /home/user/Claude/kalshi-analyzer
python setup_credentials.py
pip install -r requirements.txt
./start.sh
```

## What You'll Get

1. **Background Scanner** - Runs every 15 minutes, scans ALL Kalshi markets
2. **Web Dashboard** - Clean interface at http://localhost:5000
3. **Automatic Updates** - New opportunities appear in real-time

## Dashboard Features

- 📊 **Stats Summary** - Total opportunities, strong buys, average edge
- 🎯 **Top Bets** - Ranked by expected value (edge × confidence)
- 🔄 **Auto-Refresh** - Updates every 60 seconds
- 🎨 **Clean Design** - Dark theme, easy to read

## Each Opportunity Shows

- **Recommendation** - STRONG BUY, BUY, SELL
- **Market Price** - Current Kalshi odds
- **True Probability** - Calculated from research
- **Edge** - Your advantage (%)
- **Confidence** - How reliable the analysis is
- **Reasoning** - Why it's a good bet
- **Category** - Sports, politics, economics, etc.

## Commands

**Start everything:**
```bash
./start.sh
```

**Stop everything:**
```bash
pkill -f background_scanner && pkill -f web_dashboard
```

**View logs:**
```bash
tail -f logs/scanner.log
tail -f logs/dashboard.log
```

## What Happens

1. Scanner authenticates with Kalshi
2. Fetches all active markets (all categories)
3. Analyzes each market independently
4. Calculates true probability vs market price
5. Finds opportunities with positive edge
6. Saves to data/opportunities_TIMESTAMP.json
7. Dashboard displays latest opportunities
8. Repeats every 15 minutes

## Ready?

Just give me your Kalshi API credentials and I'll set everything up and start it running.
