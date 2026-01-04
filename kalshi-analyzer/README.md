# Kalshi Opportunity Analyzer

Automated system that scans ALL Kalshi prediction markets, conducts independent research, and identifies the best betting opportunities with positive expected value.

## Features

- **Complete Market Coverage**: Scans all active Kalshi markets across ALL categories
- **Independent Research**: Doesn't rely solely on Kalshi odds - conducts external research
- **Multi-Source Analysis**: Pulls data from sports APIs, news, weather, economic indicators, etc.
- **Edge Detection**: Calculates true probability vs market price to find mispriced opportunities
- **Smart Recommendations**: Ranks opportunities by expected value (edge × confidence)
- **Automated Scanning**: Run on demand or schedule for continuous monitoring

## Market Categories Analyzed

- **Sports**: NFL, NBA, MLB, NHL, Soccer - using stats, injuries, weather
- **Politics**: Elections, polls - using polling aggregators, models, sentiment
- **Economics**: Fed decisions, jobs data - using economic indicators, forecasts
- **Weather**: Temperature, precipitation - using NOAA data, forecast models
- **Entertainment**: Box office, awards - using tracking data, social sentiment
- **Crypto**: Price movements - using on-chain data, technicals
- **General**: Any other markets - using news sentiment

## How It Works

1. **Authenticate** with Kalshi API
2. **Fetch** all active markets (all categories)
3. **Categorize** markets by type (sports, politics, economics, etc.)
4. **Research** each market using external data sources
5. **Calculate** true probability using independent analysis
6. **Compare** true probability vs market price to find edge
7. **Rank** opportunities by expected value
8. **Recommend** top bets with highest probability of profit

## Setup

### 1. Install Dependencies

```bash
cd kalshi-analyzer
pip install -r requirements.txt
```

### 2. Configure API Keys

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
# REQUIRED: Kalshi API credentials
KALSHI_API_KEY=your_kalshi_api_key
KALSHI_API_SECRET=your_kalshi_api_secret

# OPTIONAL: External data sources (for better analysis)
NEWS_API_KEY=your_newsapi_key
SPORTS_API_KEY=your_sports_api_key
WEATHER_API_KEY=your_weather_api_key
POLYGON_API_KEY=your_polygon_api_key  # for crypto data

# Analysis settings
MIN_EDGE_PERCENTAGE=5.0      # Minimum edge to consider (%)
MIN_LIQUIDITY=1000           # Minimum market volume
MAX_POSITIONS=10             # Max simultaneous positions
```

### 3. Get API Keys

**Kalshi API** (REQUIRED):
- Go to Kalshi settings
- Generate new API key and secret
- **IMPORTANT**: Revoke the old key you accidentally exposed
- Add new credentials to `.env`

**News API** (Recommended):
- Sign up at https://newsapi.org
- Free tier: 100 requests/day

**Sports Data** (Recommended for sports betting):
- ESPN API or SportsData.io
- Provides stats, injuries, schedules

**Weather API** (For weather markets):
- OpenWeatherMap or Weather.gov API
- Free tier available

**Polygon.io** (For crypto markets):
- https://polygon.io
- Real-time crypto data

## Usage

### Run Complete Scan

```bash
cd src
python main_analyzer.py
```

This will:
1. Scan ALL active Kalshi markets
2. Conduct independent research on each
3. Calculate true probabilities
4. Find opportunities with positive edge
5. Display top 10 recommendations
6. Save full results to `data/opportunities_TIMESTAMP.json`

### Example Output

```
================================================================================
TOP OPPORTUNITIES (23 total)
================================================================================

#1 - STRONG_BUY
Market: Will the Lakers beat the Celtics on 2026-01-15?
Ticker: NBA-LAL-BOS-2026-01-15
Category: sports

Market Price: 42.0%
True Probability: 58.5%
Edge: +16.5%
Confidence: 75.0%

Reasoning: True probability (58.5%) significantly higher than market (42.0%). Edge: 16.5%
Data Sources: sports_analysis, injury_reports, betting_lines

================================================================================

#2 - BUY
Market: Will it snow >2 inches in NYC on 2026-01-20?
Ticker: WEATHER-NYC-SNOW-2026-01-20
Category: weather

Market Price: 35.0%
True Probability: 48.0%
Edge: +13.0%
Confidence: 80.0%

Reasoning: True probability (48.0%) significantly higher than market (35.0%). Edge: 13.0%
Data Sources: weather_analysis, noaa_data, forecast_models

================================================================================
```

## Advanced Usage

### Filter by Category

Edit `main_analyzer.py` to only analyze specific categories:

```python
# Only analyze sports markets
categories_to_analyze = ['sports', 'weather']

for market in markets:
    category = self.kalshi.categorize_market(market)
    if category not in categories_to_analyze:
        continue
    # ... rest of analysis
```

### Adjust Criteria

Edit `.env` to change filtering:

```env
MIN_EDGE_PERCENTAGE=10.0    # Only show opportunities with 10%+ edge
MIN_LIQUIDITY=5000          # Only liquid markets
```

### Schedule Automatic Scans

Use cron (Linux/Mac) to run hourly:

```bash
0 * * * * cd /path/to/kalshi-analyzer/src && python main_analyzer.py >> ../logs/scan.log 2>&1
```

Or Windows Task Scheduler for automated scanning.

## Next Steps to Improve

### 1. Implement Real Data Sources

Currently using placeholder analysis. Integrate real APIs:

**Sports**:
```python
# In research_engine.py _analyze_sports()
def _get_team_stats(team_name):
    url = f"https://api.espn.com/v2/sports/basketball/leagues/nba/teams"
    response = requests.get(url)
    # Parse team stats, calculate win probability
    return probability
```

**Politics**:
```python
# Integrate 538 polling data
def _get_polling_average(candidate):
    # Scrape or API call to 538
    # Weight polls by quality/recency
    # Calculate probability
    return probability
```

**Weather**:
```python
# Use NOAA API
def _get_weather_forecast(location, date):
    url = f"https://api.weather.gov/points/{lat},{lon}/forecast"
    # Get ensemble model forecasts
    # Calculate probability
    return probability
```

### 2. Add Machine Learning

Train models on historical Kalshi market data:

```python
from sklearn.ensemble import RandomForestClassifier

# Train on past markets + outcomes
model = RandomForestClassifier()
model.fit(X_historical, y_outcomes)

# Predict current markets
probability = model.predict_proba(X_current)
```

### 3. Add Position Sizing

Kelly Criterion for optimal bet sizing:

```python
def kelly_criterion(probability, odds, fraction=0.25):
    """
    Calculate optimal bet size using Kelly Criterion

    Args:
        probability: Your estimated probability of winning
        odds: Market odds
        fraction: Fraction of Kelly to bet (0.25 = quarter Kelly for safety)
    """
    edge = (probability * odds) - 1
    kelly = edge / odds
    return max(0, kelly * fraction)  # Never bet more than fractional Kelly
```

### 4. Add Trade Execution

Automatically execute trades on top opportunities:

```python
def execute_trade(market_ticker, side, quantity, price):
    """
    Place order on Kalshi

    Args:
        market_ticker: Market identifier
        side: 'yes' or 'no'
        quantity: Number of contracts
        price: Limit price (cents)
    """
    endpoint = "/v1/orders"
    order = {
        'ticker': market_ticker,
        'side': side,
        'quantity': quantity,
        'type': 'limit',
        'price': price
    }
    # Submit order via Kalshi API
```

### 5. Add Backtesting

Test strategies on historical data:

```python
def backtest_strategy(historical_markets, strategy):
    """
    Test edge-finding strategy on past markets

    Returns:
        {
            'total_bets': int,
            'wins': int,
            'losses': int,
            'win_rate': float,
            'roi': float,
            'sharpe_ratio': float
        }
    """
    # Simulate placing bets based on strategy
    # Calculate performance metrics
    pass
```

## Risk Management

**IMPORTANT**: This is a research tool. Always:

1. **Start small** - Test with small positions first
2. **Diversify** - Don't put all capital in one market
3. **Set limits** - Never bet more than you can afford to lose
4. **Verify research** - Double-check the analysis before betting
5. **Track performance** - Monitor win rate and ROI
6. **Adjust** - Refine strategy based on results

## File Structure

```
kalshi-analyzer/
├── src/
│   ├── kalshi_client.py       # Kalshi API client
│   ├── research_engine.py     # Independent research & probability calculation
│   └── main_analyzer.py       # Main scanner & opportunity finder
├── config/
│   └── .env                   # API keys and settings (DO NOT COMMIT)
├── data/
│   └── opportunities_*.json   # Saved analysis results
├── logs/
│   └── scan.log              # Execution logs
├── .env.example              # Example environment file
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Security Notes

- **NEVER** commit `.env` file to git
- **NEVER** share API keys publicly
- Add `.env` to `.gitignore`:
  ```bash
  echo ".env" >> .gitignore
  echo "data/" >> .gitignore
  echo "logs/" >> .gitignore
  ```

## Support

For Kalshi API documentation:
- https://docs.kalshi.com

For issues with this analyzer:
- Review code and customize for your needs
- Add real data source integrations
- Backtest before live trading

## Disclaimer

This tool is for educational and research purposes. Prediction market trading involves risk. Past performance does not guarantee future results. Always conduct your own due diligence before placing any bets.
