"""
Kalshi API Client - RSA Authentication
Uses RSA-PSS signing for authentication
"""

import os
import requests
import base64
import time
from typing import Dict, List, Optional
from datetime import datetime
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend


class KalshiClient:
    """Client for Kalshi API using RSA authentication"""

    def __init__(self, key_id: str = None, private_key_pem: str = None):
        self.key_id = key_id or os.getenv('KALSHI_KEY_ID')
        self.private_key_pem = private_key_pem or os.getenv('KALSHI_PRIVATE_KEY')
        self.base_url = 'https://trading-api.kalshi.com'
        self.session = requests.Session()

        if not self.key_id or not self.private_key_pem:
            raise ValueError("Key ID and Private Key required")

        # Load the private key
        self.private_key = serialization.load_pem_private_key(
            self.private_key_pem.encode('utf-8'),
            password=None,
            backend=default_backend()
        )

    def _sign_request(self, timestamp: str, method: str, path: str) -> str:
        """Sign request using RSA-PSS"""
        # Strip query parameters
        path_without_query = path.split('?')[0]

        # Create message to sign
        message = f"{timestamp}{method}{path_without_query}"

        # Sign with RSA-PSS
        signature = self.private_key.sign(
            message.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.DIGEST_LENGTH
            ),
            hashes.SHA256()
        )

        # Return base64 encoded signature
        return base64.b64encode(signature).decode('utf-8')

    def _make_request(self, method: str, path: str, params: dict = None, json_data: dict = None):
        """Make authenticated request to Kalshi API"""
        timestamp = str(int(time.time() * 1000))

        # Create signature
        signature = self._sign_request(timestamp, method.upper(), path)

        # Set headers
        headers = {
            'KALSHI-ACCESS-KEY': self.key_id,
            'KALSHI-ACCESS-SIGNATURE': signature,
            'KALSHI-ACCESS-TIMESTAMP': timestamp,
            'Content-Type': 'application/json'
        }

        # Make request
        url = f"{self.base_url}{path}"

        if method.upper() == 'GET':
            response = self.session.get(url, headers=headers, params=params)
        elif method.upper() == 'POST':
            response = self.session.post(url, headers=headers, json=json_data)
        else:
            raise ValueError(f"Unsupported method: {method}")

        response.raise_for_status()
        return response.json()

    def get_balance(self) -> Dict:
        """Get account balance"""
        try:
            return self._make_request('GET', '/trade-api/v2/portfolio/balance')
        except Exception as e:
            print(f"Error getting balance: {e}")
            return {}

    def get_all_markets(self, status: str = "open", limit: int = 1000) -> List[Dict]:
        """Get all markets"""
        try:
            params = {
                'status': status,
                'limit': limit
            }
            result = self._make_request('GET', '/trade-api/v2/markets', params=params)
            return result.get('markets', [])
        except Exception as e:
            print(f"Error fetching markets: {e}")
            return []

    def get_market(self, ticker: str) -> Optional[Dict]:
        """Get specific market details"""
        try:
            result = self._make_request('GET', f'/trade-api/v2/markets/{ticker}')
            return result.get('market')
        except Exception as e:
            print(f"Error fetching market {ticker}: {e}")
            return None

    def get_orderbook(self, ticker: str) -> Optional[Dict]:
        """Get orderbook for market"""
        try:
            return self._make_request('GET', f'/trade-api/v2/markets/{ticker}/orderbook')
        except Exception as e:
            print(f"Error fetching orderbook {ticker}: {e}")
            return None

    def categorize_market(self, market: Dict) -> str:
        """Categorize market by type"""
        title = market.get('title', '').lower()
        ticker = market.get('ticker', '').lower()

        # Sports
        if any(s in title or s in ticker for s in ['nfl', 'nba', 'mlb', 'nhl', 'soccer', 'football', 'basketball', 'baseball']):
            return 'sports'

        # Politics
        if any(p in title or p in ticker for p in ['election', 'president', 'senate', 'house', 'congress', 'poll', 'vote']):
            return 'politics'

        # Economics
        if any(e in title or e in ticker for e in ['fed', 'gdp', 'inflation', 'unemployment', 'recession', 'rate', 'jobs']):
            return 'economics'

        # Weather
        if any(w in title or w in ticker for w in ['temperature', 'rain', 'snow', 'hurricane', 'weather']):
            return 'weather'

        # Entertainment
        if any(e in title or e in ticker for e in ['movie', 'box office', 'grammy', 'oscar', 'emmy', 'album']):
            return 'entertainment'

        # Crypto
        if any(c in title or c in ticker for c in ['bitcoin', 'btc', 'eth', 'crypto', 'ethereum']):
            return 'crypto'

        return 'other'


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    print("Testing Kalshi RSA Authentication...")

    client = KalshiClient()

    # Test balance
    print("\n[1] Testing authentication with balance check...")
    balance = client.get_balance()
    if balance:
        print(f"✓ Authentication successful!")
        print(f"  Balance: ${balance.get('balance', 'N/A')}")
    else:
        print("✗ Authentication failed")

    # Test markets
    print("\n[2] Fetching markets...")
    markets = client.get_all_markets(limit=10)
    print(f"✓ Found {len(markets)} markets")

    if markets:
        print("\nSample markets:")
        for i, market in enumerate(markets[:5], 1):
            print(f"{i}. {market.get('title')}")
            print(f"   Ticker: {market.get('ticker')}")
            print(f"   Category: {client.categorize_market(market)}")
