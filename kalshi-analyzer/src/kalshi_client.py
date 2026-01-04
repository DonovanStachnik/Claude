"""
Kalshi API Client
Handles authentication and market data fetching from Kalshi
"""

import os
import requests
import hashlib
import hmac
import time
from typing import Dict, List, Optional
from datetime import datetime
import json


class KalshiClient:
    """Client for interacting with Kalshi prediction markets API"""

    def __init__(self, api_key: str = None, api_secret: str = None, base_url: str = None):
        self.api_key = api_key or os.getenv('KALSHI_API_KEY')
        self.api_secret = api_secret or os.getenv('KALSHI_API_SECRET')
        self.base_url = base_url or os.getenv('KALSHI_BASE_URL', 'https://api.elections.kalshi.com')
        self.session = requests.Session()
        self.token = None

        if not self.api_key or not self.api_secret:
            raise ValueError("API credentials not provided. Set KALSHI_API_KEY and KALSHI_API_SECRET")

    def _generate_signature(self, timestamp: str, method: str, path: str, body: str = "") -> str:
        """Generate HMAC signature for API request"""
        message = f"{timestamp}{method}{path}{body}"
        signature = hmac.new(
            self.api_secret.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature

    def authenticate(self) -> bool:
        """Authenticate with Kalshi API"""
        try:
            endpoint = "/v1/login"
            timestamp = str(int(time.time() * 1000))

            headers = {
                'Content-Type': 'application/json',
                'X-Kalshi-Key': self.api_key,
                'X-Kalshi-Timestamp': timestamp
            }

            response = self.session.post(f"{self.base_url}{endpoint}", headers=headers)
            response.raise_for_status()

            data = response.json()
            self.token = data.get('token')
            return True

        except Exception as e:
            print(f"Authentication failed: {e}")
            return False

    def get_all_markets(self, status: str = "open") -> List[Dict]:
        """
        Get all active markets from Kalshi

        Args:
            status: Market status (open, closed, settled)

        Returns:
            List of market dictionaries
        """
        try:
            endpoint = f"/v1/markets?status={status}&limit=1000"
            headers = {'Authorization': f'Bearer {self.token}'}

            response = self.session.get(f"{self.base_url}{endpoint}", headers=headers)
            response.raise_for_status()

            data = response.json()
            return data.get('markets', [])

        except Exception as e:
            print(f"Error fetching markets: {e}")
            return []

    def get_market_details(self, market_ticker: str) -> Optional[Dict]:
        """Get detailed information about a specific market"""
        try:
            endpoint = f"/v1/markets/{market_ticker}"
            headers = {'Authorization': f'Bearer {self.token}'}

            response = self.session.get(f"{self.base_url}{endpoint}", headers=headers)
            response.raise_for_status()

            return response.json()

        except Exception as e:
            print(f"Error fetching market {market_ticker}: {e}")
            return None

    def get_orderbook(self, market_ticker: str) -> Optional[Dict]:
        """Get current orderbook (bids/asks) for a market"""
        try:
            endpoint = f"/v1/markets/{market_ticker}/orderbook"
            headers = {'Authorization': f'Bearer {self.token}'}

            response = self.session.get(f"{self.base_url}{endpoint}", headers=headers)
            response.raise_for_status()

            return response.json()

        except Exception as e:
            print(f"Error fetching orderbook for {market_ticker}: {e}")
            return None

    def get_market_history(self, market_ticker: str) -> Optional[List[Dict]]:
        """Get historical trades for a market"""
        try:
            endpoint = f"/v1/markets/{market_ticker}/history"
            headers = {'Authorization': f'Bearer {self.token}'}

            response = self.session.get(f"{self.base_url}{endpoint}", headers=headers)
            response.raise_for_status()

            return response.json().get('history', [])

        except Exception as e:
            print(f"Error fetching history for {market_ticker}: {e}")
            return None

    def categorize_market(self, market: Dict) -> str:
        """Categorize market by type"""
        title = market.get('title', '').lower()
        ticker = market.get('ticker', '').lower()

        # Sports categories
        if any(sport in title or sport in ticker for sport in ['nfl', 'nba', 'mlb', 'nhl', 'soccer', 'football', 'basketball', 'baseball']):
            return 'sports'

        # Politics categories
        if any(pol in title or pol in ticker for pol in ['election', 'president', 'senate', 'house', 'congress', 'poll', 'vote']):
            return 'politics'

        # Economics categories
        if any(econ in title or econ in ticker for econ in ['fed', 'gdp', 'inflation', 'unemployment', 'recession', 'rate', 'jobs']):
            return 'economics'

        # Weather categories
        if any(weather in title or weather in ticker for weather in ['temperature', 'rain', 'snow', 'hurricane', 'weather']):
            return 'weather'

        # Entertainment categories
        if any(ent in title or ent in ticker for ent in ['movie', 'box office', 'grammy', 'oscar', 'emmy', 'album']):
            return 'entertainment'

        # Crypto categories
        if any(crypto in title or crypto in ticker for crypto in ['bitcoin', 'btc', 'eth', 'crypto', 'ethereum']):
            return 'crypto'

        return 'other'


if __name__ == "__main__":
    # Test the client
    from dotenv import load_dotenv
    load_dotenv()

    client = KalshiClient()

    if client.authenticate():
        print("✓ Authentication successful")

        markets = client.get_all_markets()
        print(f"✓ Found {len(markets)} active markets")

        # Categorize markets
        categories = {}
        for market in markets:
            cat = client.categorize_market(market)
            categories[cat] = categories.get(cat, 0) + 1

        print("\nMarket breakdown:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"  {cat}: {count} markets")
    else:
        print("✗ Authentication failed")
