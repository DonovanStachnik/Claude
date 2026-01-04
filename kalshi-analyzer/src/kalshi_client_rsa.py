"""
Kalshi API Client - RSA Authentication using pycryptodome
"""

import os
import requests
import base64
import time
from typing import Dict, List, Optional
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


class KalshiClient:
    """Client for Kalshi API using RSA authentication"""

    def __init__(self, key_id: str = None, private_key_pem: str = None):
        self.key_id = key_id or os.getenv('KALSHI_KEY_ID')
        self.base_url = 'https://trading-api.kalshi.com'
        self.session = requests.Session()

        if not self.key_id:
            raise ValueError("Key ID required")

        # Load private key from file or parameter
        if private_key_pem:
            self.private_key = RSA.import_key(private_key_pem)
        else:
            # Try loading from separate file first
            key_file = os.path.join(os.path.dirname(__file__), '..', 'kalshi_private.key')
            if os.path.exists(key_file):
                with open(key_file, 'r') as f:
                    self.private_key = RSA.import_key(f.read())
            else:
                # Fall back to environment variable
                private_key_pem = os.getenv('KALSHI_PRIVATE_KEY')
                if not private_key_pem:
                    raise ValueError("Private key not found in file or environment")
                self.private_key = RSA.import_key(private_key_pem)

    def _sign_request(self, timestamp: str, method: str, path: str) -> str:
        """Sign request using RSA-PSS"""
        # Strip query parameters
        path_without_query = path.split('?')[0]

        # Create message to sign
        message = f"{timestamp}{method}{path_without_query}"

        # Create hash
        h = SHA256.new(message.encode('utf-8'))

        # Sign with PKCS#1 v1.5 (Kalshi uses this, not PSS)
        signature = pkcs1_15.new(self.private_key).sign(h)

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

        try:
            if method.upper() == 'GET':
                response = self.session.get(url, headers=headers, params=params, timeout=10)
            elif method.upper() == 'POST':
                response = self.session.post(url, headers=headers, json=json_data, timeout=10)
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return None

    def get_balance(self) -> Dict:
        """Get account balance"""
        result = self._make_request('GET', '/trade-api/v2/portfolio/balance')
        return result if result else {}

    def get_all_markets(self, status: str = "open", limit: int = 200) -> List[Dict]:
        """Get all markets"""
        params = {
            'status': status,
            'limit': limit
        }
        result = self._make_request('GET', '/trade-api/v2/markets', params=params)
        return result.get('markets', []) if result else []

    def get_market(self, ticker: str) -> Optional[Dict]:
        """Get specific market details"""
        result = self._make_request('GET', f'/trade-api/v2/markets/{ticker}')
        return result.get('market') if result else None

    def get_orderbook(self, ticker: str) -> Optional[Dict]:
        """Get orderbook for market"""
        return self._make_request('GET', f'/trade-api/v2/markets/{ticker}/orderbook')

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
    print("\n[1] Testing authentication...")
    balance = client.get_balance()
    if balance:
        print(f"✓ Authentication successful!")
        print(f"  Balance: ${balance.get('balance', 0) / 100:.2f}")
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
            print(f"   Last Price: {market.get('yes_bid', 'N/A')}")
            print()
