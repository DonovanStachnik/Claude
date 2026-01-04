"""
Demo Data Generator - Creates sample opportunities to show dashboard
"""

import json
import os
from datetime import datetime

def generate_demo_opportunities():
    """Generate sample opportunities for demo"""

    opportunities = [
        {
            'market': {
                'ticker': 'NBA-LAL-BOS-2026-01-15',
                'title': 'Will the Lakers beat the Celtics on 2026-01-15?',
                'last_price': 42.0
            },
            'analysis': {
                'market_ticker': 'NBA-LAL-BOS-2026-01-15',
                'category': 'sports',
                'market_probability': 42.0,
                'true_probability': 58.5,
                'edge': 16.5,
                'confidence': 75.0,
                'recommendation': 'STRONG_BUY',
                'reasoning': 'Lakers have home court advantage, Celtics missing key player due to injury. Historical matchup favors Lakers at home by 62%.',
                'sources': ['sports_stats', 'injury_reports']
            }
        },
        {
            'market': {
                'ticker': 'WEATHER-NYC-SNOW-20260120',
                'title': 'Will it snow more than 2 inches in NYC on 2026-01-20?',
                'last_price': 35.0
            },
            'analysis': {
                'market_ticker': 'WEATHER-NYC-SNOW-20260120',
                'category': 'weather',
                'market_probability': 35.0,
                'true_probability': 48.0,
                'edge': 13.0,
                'confidence': 80.0,
                'recommendation': 'BUY',
                'reasoning': 'All major weather models (GFS, Euro, NAM) agree on significant snowfall. Historical climate data shows 55% probability for this weather pattern.',
                'sources': ['weather_models', 'noaa_data']
            }
        },
        {
            'market': {
                'ticker': 'ECON-FED-RATE-FEB2026',
                'title': 'Will the Fed raise interest rates in February 2026?',
                'last_price': 52.0
            },
            'analysis': {
                'market_ticker': 'ECON-FED-RATE-FEB2026',
                'category': 'economics',
                'market_probability': 52.0,
                'true_probability': 38.0,
                'edge': -14.0,
                'confidence': 70.0,
                'recommendation': 'SELL',
                'reasoning': 'Recent inflation data trending down, Fed Chair comments suggest patience. Market overestimating probability of rate hike.',
                'sources': ['fed_data', 'economic_indicators']
            }
        },
        {
            'market': {
                'ticker': 'NFL-CHIEFS-BILLS-PLAYOFF',
                'title': 'Will Chiefs beat Bills in AFC Championship?',
                'last_price': 48.0
            },
            'analysis': {
                'market_ticker': 'NFL-CHIEFS-BILLS-PLAYOFF',
                'category': 'sports',
                'market_probability': 48.0,
                'true_probability': 62.0,
                'edge': 14.0,
                'confidence': 72.0,
                'recommendation': 'STRONG_BUY',
                'reasoning': 'Chiefs have won last 3 playoff matchups. Home field advantage worth 7%. QB advantage favors Mahomes.',
                'sources': ['sports_stats', 'betting_lines', 'historical_data']
            }
        },
        {
            'market': {
                'ticker': 'CRYPTO-BTC-50K-JAN2026',
                'title': 'Will Bitcoin hit $50,000 by end of January 2026?',
                'last_price': 58.0
            },
            'analysis': {
                'market_ticker': 'CRYPTO-BTC-50K-JAN2026',
                'category': 'crypto',
                'market_probability': 58.0,
                'true_probability': 65.0,
                'edge': 7.0,
                'confidence': 62.0,
                'recommendation': 'BUY',
                'reasoning': 'Strong momentum, institutional buying increasing. Technical indicators show bullish trend. On-chain metrics support continued growth.',
                'sources': ['crypto_data', 'on_chain_metrics']
            }
        }
    ]

    return {
        'timestamp': datetime.now().isoformat(),
        'total_opportunities': len(opportunities),
        'opportunities': opportunities
    }

if __name__ == "__main__":
    # Create data directory
    os.makedirs('../data', exist_ok=True)

    # Generate and save demo data
    data = generate_demo_opportunities()

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'../data/opportunities_{timestamp}.json'

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"✓ Demo data created: {filename}")
    print(f"✓ {len(data['opportunities'])} sample opportunities")
    print("\nNow start the dashboard:")
    print("  python web_dashboard.py")
