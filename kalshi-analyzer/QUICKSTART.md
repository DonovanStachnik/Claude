# Quick Start Guide

## 1. Security First!

**⚠️ REVOKE THE EXPOSED API KEY IMMEDIATELY ⚠️**

1. Go to your Kalshi account settings
2. Find the API key you accidentally pasted in chat
3. Delete/revoke it immediately
4. Generate a NEW API key and secret

## 2. Setup (5 minutes)

```bash
# Navigate to project
cd kalshi-analyzer

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your NEW API credentials
nano .env  # or use any text editor
```

Add your NEW Kalshi credentials to `.env`:
```env
KALSHI_API_KEY=your_new_key_here
KALSHI_API_SECRET=your_new_secret_here
```

## 3. Run Your First Scan

```bash
cd src
python main_analyzer.py
```

This will:
- ✓ Scan ALL active Kalshi markets
- ✓ Analyze each one independently
- ✓ Find opportunities with positive edge
- ✓ Show you the top 10 best bets
- ✓ Save results to `data/opportunities_TIMESTAMP.json`

## 4. What You'll See

```
================================================================================
KALSHI OPPORTUNITY SCANNER
================================================================================

[1/5] Authenticating with Kalshi...
✓ Authenticated successfully

[2/5] Fetching all active markets...
✓ Found 247 active markets

[3/5] Categorizing markets...
  sports: 89 markets
  politics: 67 markets
  economics: 45 markets
  weather: 23 markets
  crypto: 15 markets
  entertainment: 8 markets

[4/5] Analyzing markets for opportunities...
  Progress: 50/247 markets analyzed...
  Progress: 100/247 markets analyzed...
  Progress: 150/247 markets analyzed...
  Progress: 200/247 markets analyzed...
✓ Analysis complete - 23 opportunities found

[5/5] Ranking opportunities...

================================================================================
TOP OPPORTUNITIES (23 total)
================================================================================

#1 - STRONG_BUY
Market: [Market Title]
Ticker: [TICKER]
Category: sports

Market Price: 42.0%
True Probability: 58.5%
Edge: +16.5%
Confidence: 75.0%

Reasoning: True probability significantly higher than market price
Data Sources: sports_analysis, news_sentiment
================================================================================
```

## 5. Understand the Results

**Edge**: Difference between true probability and market price
- Positive edge = Market undervalues outcome (BUY opportunity)
- Negative edge = Market overvalues outcome (SELL opportunity)

**Confidence**: How reliable the probability calculation is
- Higher confidence = More reliable data sources

**Recommendation**:
- `STRONG_BUY`: Large edge (10%+), high confidence - Best opportunities
- `BUY`: Good edge (5-10%), decent confidence
- `SELL`: Negative edge, market overvalued
- `STRONG_SELL`: Large negative edge
- `HOLD`: No significant edge or low confidence

## 6. Take Action

1. **Review top recommendations** - Focus on STRONG_BUY first
2. **Do additional research** - Verify the analysis makes sense
3. **Check liquidity** - Make sure market has enough volume
4. **Size positions appropriately** - Start small!
5. **Place bets** on highest conviction opportunities

## 7. Monitor Performance

- Save results: `data/opportunities_TIMESTAMP.json`
- Track which bets you took
- Monitor win rate and ROI
- Adjust strategy based on results

## 8. Run Regularly

Set up automated scanning:

**Every hour** (Linux/Mac cron):
```bash
0 * * * * cd /path/to/kalshi-analyzer/src && python main_analyzer.py >> ../logs/scan.log 2>&1
```

**Every hour** (Windows Task Scheduler):
- Create task that runs `python main_analyzer.py`
- Set trigger: hourly
- Save logs for review

## Next Steps

- **Add real data sources** - Integrate sports APIs, news feeds, etc.
- **Backtest** - Test strategy on historical data
- **Automate execution** - Auto-place orders on best opportunities
- **Track performance** - Build dashboard to monitor results

## Troubleshooting

**Authentication fails**:
- Check API key is correct in `.env`
- Make sure you revoked old key and generated NEW one
- Verify no extra spaces in `.env` file

**No opportunities found**:
- Lower `MIN_EDGE_PERCENTAGE` in `.env` (try 3.0)
- Lower `MIN_LIQUIDITY` (try 500)
- Check that markets are actually open

**Analysis seems wrong**:
- Currently using placeholder probabilities (50%)
- Need to integrate real data sources (see README)
- This is the framework - you add real research!

## Remember

- Start small
- Verify research
- Track results
- Adjust strategy
- Never bet more than you can afford to lose

**Good luck printing! 🚀**
