"""
Independent Research Engine
Pulls data from external sources to calculate true probabilities
"""

import os
import requests
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import json


class ResearchEngine:
    """Conducts independent research to calculate true probabilities"""

    def __init__(self):
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.sports_api_key = os.getenv('SPORTS_API_KEY')
        self.weather_api_key = os.getenv('WEATHER_API_KEY')
        self.polygon_api_key = os.getenv('POLYGON_API_KEY')

    def analyze_market(self, market: Dict, category: str) -> Dict:
        """
        Analyze a market using independent research

        Returns:
            {
                'true_probability': float (0-100),
                'confidence': float (0-100),
                'edge': float (percentage edge vs market),
                'sources': list of data sources used,
                'recommendation': str (STRONG_BUY, BUY, HOLD, SELL, STRONG_SELL),
                'reasoning': str
            }
        """
        analysis = {
            'market_ticker': market.get('ticker'),
            'category': category,
            'sources': [],
            'data_points': []
        }

        # Route to appropriate analyzer based on category
        if category == 'sports':
            return self._analyze_sports(market, analysis)
        elif category == 'politics':
            return self._analyze_politics(market, analysis)
        elif category == 'economics':
            return self._analyze_economics(market, analysis)
        elif category == 'weather':
            return self._analyze_weather(market, analysis)
        elif category == 'entertainment':
            return self._analyze_entertainment(market, analysis)
        elif category == 'crypto':
            return self._analyze_crypto(market, analysis)
        else:
            return self._analyze_general(market, analysis)

    def _analyze_sports(self, market: Dict, analysis: Dict) -> Dict:
        """Analyze sports markets using stats, injuries, weather, etc."""
        title = market.get('title', '')
        analysis['sources'].append('sports_analysis')

        # Extract teams/players from title
        # This would integrate with real sports APIs
        analysis['data_points'].append({
            'source': 'sports_stats',
            'note': 'Would pull team stats, player injuries, head-to-head records'
        })

        # Placeholder - real implementation would call:
        # - ESPN API for stats
        # - Injury reports
        # - Weather for outdoor games
        # - Betting line movement
        # - Public betting percentages

        true_prob = 50.0  # Placeholder
        confidence = 60.0

        return self._finalize_analysis(market, analysis, true_prob, confidence)

    def _analyze_politics(self, market: Dict, analysis: Dict) -> Dict:
        """Analyze political markets using polls, models, news"""
        analysis['sources'].append('politics_analysis')

        # Would integrate with:
        # - 538 polling averages
        # - RealClearPolitics
        # - Prediction models
        # - News sentiment analysis
        # - Historical election data

        analysis['data_points'].append({
            'source': 'polling_data',
            'note': 'Would aggregate multiple poll sources with weighting'
        })

        true_prob = 50.0  # Placeholder
        confidence = 70.0

        return self._finalize_analysis(market, analysis, true_prob, confidence)

    def _analyze_economics(self, market: Dict, analysis: Dict) -> Dict:
        """Analyze economic markets using Fed data, indicators, forecasts"""
        analysis['sources'].append('economics_analysis')

        # Would integrate with:
        # - FRED (Federal Reserve Economic Data)
        # - BLS (Bureau of Labor Statistics)
        # - Analyst forecasts
        # - Economic models

        analysis['data_points'].append({
            'source': 'economic_indicators',
            'note': 'Would pull Fed data, unemployment, GDP forecasts'
        })

        true_prob = 50.0  # Placeholder
        confidence = 65.0

        return self._finalize_analysis(market, analysis, true_prob, confidence)

    def _analyze_weather(self, market: Dict, analysis: Dict) -> Dict:
        """Analyze weather markets using NOAA, weather models"""
        analysis['sources'].append('weather_analysis')

        # Would integrate with:
        # - NOAA weather data
        # - Historical climate data
        # - Multiple weather models (GFS, Euro, etc.)

        analysis['data_points'].append({
            'source': 'weather_models',
            'note': 'Would aggregate multiple weather forecast models'
        })

        true_prob = 50.0  # Placeholder
        confidence = 75.0

        return self._finalize_analysis(market, analysis, true_prob, confidence)

    def _analyze_entertainment(self, market: Dict, analysis: Dict) -> Dict:
        """Analyze entertainment markets using box office, streaming, social"""
        analysis['sources'].append('entertainment_analysis')

        # Would integrate with:
        # - Box office trackers
        # - Streaming viewership data
        # - Social media sentiment
        # - Historical award patterns

        analysis['data_points'].append({
            'source': 'box_office',
            'note': 'Would track opening weekend projections, social buzz'
        })

        true_prob = 50.0  # Placeholder
        confidence = 60.0

        return self._finalize_analysis(market, analysis, true_prob, confidence)

    def _analyze_crypto(self, market: Dict, analysis: Dict) -> Dict:
        """Analyze crypto markets using on-chain data, technicals"""
        analysis['sources'].append('crypto_analysis')

        # Would integrate with:
        # - On-chain metrics
        # - Exchange data
        # - Technical indicators
        # - Whale wallet tracking

        if self.polygon_api_key:
            analysis['data_points'].append({
                'source': 'crypto_data',
                'note': 'Would pull price data, volume, on-chain metrics'
            })

        true_prob = 50.0  # Placeholder
        confidence = 55.0

        return self._finalize_analysis(market, analysis, true_prob, confidence)

    def _analyze_general(self, market: Dict, analysis: Dict) -> Dict:
        """Analyze general markets using news sentiment"""
        analysis['sources'].append('news_sentiment')

        if self.news_api_key:
            # Would do news sentiment analysis
            analysis['data_points'].append({
                'source': 'news_api',
                'note': 'Would analyze news sentiment and volume'
            })

        true_prob = 50.0  # Placeholder
        confidence = 50.0

        return self._finalize_analysis(market, analysis, true_prob, confidence)

    def _finalize_analysis(self, market: Dict, analysis: Dict, true_prob: float, confidence: float) -> Dict:
        """Calculate edge and make recommendation"""

        # Get current market probability (last traded price)
        market_prob = market.get('last_price', 50.0)
        if isinstance(market_prob, int):
            market_prob = float(market_prob)

        # Calculate edge (difference between true prob and market prob)
        edge = true_prob - market_prob

        # Make recommendation based on edge and confidence
        min_edge = float(os.getenv('MIN_EDGE_PERCENTAGE', 5.0))

        if edge > min_edge and confidence > 60:
            recommendation = 'STRONG_BUY' if edge > min_edge * 2 else 'BUY'
            reasoning = f"True probability ({true_prob:.1f}%) significantly higher than market ({market_prob:.1f}%). Edge: {edge:.1f}%"
        elif edge < -min_edge and confidence > 60:
            recommendation = 'STRONG_SELL' if edge < -min_edge * 2 else 'SELL'
            reasoning = f"True probability ({true_prob:.1f}%) significantly lower than market ({market_prob:.1f}%). Edge: {abs(edge):.1f}%"
        else:
            recommendation = 'HOLD'
            reasoning = f"No significant edge. Market fairly priced or low confidence."

        analysis.update({
            'true_probability': true_prob,
            'market_probability': market_prob,
            'confidence': confidence,
            'edge': edge,
            'edge_percentage': abs(edge),
            'recommendation': recommendation,
            'reasoning': reasoning
        })

        return analysis

    def get_news_sentiment(self, query: str, days_back: int = 7) -> Dict:
        """Get news sentiment for a topic"""
        if not self.news_api_key:
            return {'sentiment': 0, 'article_count': 0}

        try:
            # NewsAPI or similar
            url = "https://newsapi.org/v2/everything"
            params = {
                'q': query,
                'from': (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d'),
                'sortBy': 'relevancy',
                'apiKey': self.news_api_key
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            articles = data.get('articles', [])

            # Simple sentiment scoring (would use NLP in real version)
            sentiment_score = 0
            for article in articles:
                title = article.get('title', '').lower()
                description = article.get('description', '').lower()

                # Placeholder sentiment (would use real sentiment analysis)
                if any(word in title or word in description for word in ['surge', 'win', 'success', 'gain']):
                    sentiment_score += 1
                elif any(word in title or word in description for word in ['fall', 'lose', 'fail', 'drop']):
                    sentiment_score -= 1

            return {
                'sentiment': sentiment_score,
                'article_count': len(articles),
                'recent_articles': articles[:5]
            }

        except Exception as e:
            print(f"Error fetching news: {e}")
            return {'sentiment': 0, 'article_count': 0}


if __name__ == "__main__":
    # Test research engine
    from dotenv import load_dotenv
    load_dotenv()

    engine = ResearchEngine()

    # Test market
    test_market = {
        'ticker': 'TEST-MARKET',
        'title': 'Will Team A beat Team B?',
        'last_price': 45.0
    }

    analysis = engine.analyze_market(test_market, 'sports')
    print(json.dumps(analysis, indent=2))
