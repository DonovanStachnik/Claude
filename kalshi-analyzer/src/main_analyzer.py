"""
Main Kalshi Analyzer
Scans all markets, conducts research, finds best opportunities
"""

import os
import json
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv

from kalshi_client_rsa import KalshiClient
from research_engine import ResearchEngine


class KalshiAnalyzer:
    """Main analyzer - finds best betting opportunities across all Kalshi markets"""

    def __init__(self):
        load_dotenv()
        self.kalshi = KalshiClient()
        self.research = ResearchEngine()
        self.min_edge = float(os.getenv('MIN_EDGE_PERCENTAGE', 5.0))
        self.min_liquidity = float(os.getenv('MIN_LIQUIDITY', 1000))
        self.max_positions = int(os.getenv('MAX_POSITIONS', 10))

    def run_full_scan(self) -> List[Dict]:
        """
        Scan all Kalshi markets and find best opportunities

        Returns:
            List of opportunities sorted by edge/confidence
        """
        print("=" * 80)
        print("KALSHI OPPORTUNITY SCANNER")
        print("=" * 80)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # Step 1: Fetch all markets (authentication happens per-request)
        print("[1/4] Fetching all active markets...")
        markets = self.kalshi.get_all_markets(status="open")
        print(f"✓ Found {len(markets)} active markets")
        print()

        # Step 2: Categorize markets
        print("[2/4] Categorizing markets...")
        categorized = {}
        for market in markets:
            category = self.kalshi.categorize_market(market)
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(market)

        for category, mkts in sorted(categorized.items(), key=lambda x: len(x[1]), reverse=True):
            print(f"  {category}: {len(mkts)} markets")
        print()

        # Step 3: Analyze markets for opportunities
        print("[3/4] Analyzing markets for opportunities...")
        print("(This may take a few minutes for all markets)")
        print()

        opportunities = []
        total = len(markets)

        for idx, market in enumerate(markets, 1):
            if idx % 50 == 0:
                print(f"  Progress: {idx}/{total} markets analyzed...")

            # Get category
            category = self.kalshi.categorize_market(market)

            # Check basic filters first
            if not self._meets_basic_criteria(market):
                continue

            # Conduct independent research
            analysis = self.research.analyze_market(market, category)

            # Check if opportunity meets our criteria
            if self._is_good_opportunity(analysis):
                opportunities.append({
                    'market': market,
                    'analysis': analysis
                })

        print(f"✓ Analysis complete - {len(opportunities)} opportunities found")
        print()

        # Step 5: Rank and display opportunities
        print("[4/4] Ranking opportunities...")
        ranked = self._rank_opportunities(opportunities)

        print()
        print("=" * 80)
        print(f"TOP OPPORTUNITIES ({len(ranked)} total)")
        print("=" * 80)
        print()

        return ranked

    def _meets_basic_criteria(self, market: Dict) -> bool:
        """Check if market meets basic filtering criteria"""

        # Check liquidity (volume)
        volume = market.get('volume', 0)
        if volume < self.min_liquidity:
            return False

        # Check if market has pricing data
        if 'last_price' not in market or market['last_price'] is None:
            return False

        # Market must have reasonable time to close
        close_time = market.get('close_time')
        if close_time:
            # Would check if close_time is not too soon/far
            pass

        return True

    def _is_good_opportunity(self, analysis: Dict) -> bool:
        """Check if analysis reveals a good opportunity"""

        # Must have sufficient edge
        if abs(analysis.get('edge', 0)) < self.min_edge:
            return False

        # Must have decent confidence
        if analysis.get('confidence', 0) < 60:
            return False

        # Must have clear recommendation
        rec = analysis.get('recommendation', 'HOLD')
        if rec == 'HOLD':
            return False

        return True

    def _rank_opportunities(self, opportunities: List[Dict]) -> List[Dict]:
        """Rank opportunities by expected value"""

        def score_opportunity(opp):
            analysis = opp['analysis']
            edge = abs(analysis.get('edge', 0))
            confidence = analysis.get('confidence', 0)

            # Expected value score = edge * confidence
            return edge * (confidence / 100)

        # Sort by score (highest first)
        ranked = sorted(opportunities, key=score_opportunity, reverse=True)

        return ranked

    def display_opportunities(self, opportunities: List[Dict], max_display: int = 20):
        """Display top opportunities in formatted output"""

        for idx, opp in enumerate(opportunities[:max_display], 1):
            market = opp['market']
            analysis = opp['analysis']

            print(f"#{idx} - {analysis['recommendation']}")
            print(f"Market: {market.get('title', 'N/A')}")
            print(f"Ticker: {market.get('ticker', 'N/A')}")
            print(f"Category: {analysis.get('category', 'N/A')}")
            print(f"")
            print(f"Market Price: {analysis.get('market_probability', 0):.1f}%")
            print(f"True Probability: {analysis.get('true_probability', 0):.1f}%")
            print(f"Edge: {analysis.get('edge', 0):+.1f}%")
            print(f"Confidence: {analysis.get('confidence', 0):.1f}%")
            print(f"")
            print(f"Reasoning: {analysis.get('reasoning', 'N/A')}")
            print(f"Data Sources: {', '.join(analysis.get('sources', []))}")
            print("=" * 80)
            print()

    def save_opportunities(self, opportunities: List[Dict], filename: str = None):
        """Save opportunities to JSON file"""

        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"data/opportunities_{timestamp}.json"

        # Prepare data for JSON
        output = {
            'timestamp': datetime.now().isoformat(),
            'total_opportunities': len(opportunities),
            'opportunities': []
        }

        for opp in opportunities:
            output['opportunities'].append({
                'market': opp['market'],
                'analysis': opp['analysis']
            })

        # Save to file
        os.makedirs('data', exist_ok=True)
        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"✓ Opportunities saved to: {filename}")


def main():
    """Main entry point"""

    analyzer = KalshiAnalyzer()

    # Run full scan
    opportunities = analyzer.run_full_scan()

    # Display top opportunities
    if opportunities:
        analyzer.display_opportunities(opportunities, max_display=10)

        # Save all opportunities
        analyzer.save_opportunities(opportunities)

        print()
        print(f"✓ Found {len(opportunities)} total opportunities")
        print(f"✓ Displayed top 10")
        print()
        print("NEXT STEPS:")
        print("1. Review the opportunities above")
        print("2. Conduct additional due diligence on top picks")
        print("3. Check liquidity and position sizing")
        print("4. Place bets on highest conviction opportunities")
        print()

    else:
        print("No opportunities found meeting criteria.")
        print("Try adjusting MIN_EDGE_PERCENTAGE or other filters in .env file")


if __name__ == "__main__":
    main()
