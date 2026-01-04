"""
Setup Script - Adds Kalshi API credentials to .env file
"""

import os

def setup_credentials(api_key, api_secret):
    """Add credentials to .env file"""

    env_content = f"""# Kalshi API Credentials
KALSHI_API_KEY={api_key}
KALSHI_API_SECRET={api_secret}
KALSHI_BASE_URL=https://api.elections.kalshi.com

# External Data Sources (Optional - add later for better analysis)
NEWS_API_KEY=
SPORTS_API_KEY=
WEATHER_API_KEY=
POLYGON_API_KEY=

# Analysis Settings
MIN_EDGE_PERCENTAGE=5.0
MIN_LIQUIDITY=1000
MAX_POSITIONS=10
POSITION_SIZE_PCT=0.05

# Research Settings
ENABLE_NEWS_ANALYSIS=true
ENABLE_SPORTS_STATS=true
ENABLE_WEATHER_DATA=true
ENABLE_POLLING_DATA=true
ENABLE_ECONOMIC_DATA=true
"""

    # Write to .env file
    with open('.env', 'w') as f:
        f.write(env_content)

    print("✓ Credentials saved to .env file")
    print("")
    print("Next steps:")
    print("  1. Run: pip install -r requirements.txt flask flask-cors schedule")
    print("  2. Start system:")
    print("     Linux/Mac: ./start.sh")
    print("     Windows: start.bat")
    print("")
    print("Dashboard will be at: http://localhost:5000")

if __name__ == "__main__":
    print("=" * 60)
    print("KALSHI ANALYZER - CREDENTIAL SETUP")
    print("=" * 60)
    print()

    api_key = input("Enter your Kalshi API Key: ").strip()
    api_secret = input("Enter your Kalshi API Secret: ").strip()

    if not api_key or not api_secret:
        print("\n✗ Error: Both API key and secret are required")
        exit(1)

    setup_credentials(api_key, api_secret)
