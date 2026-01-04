"""
Background Scanner - Runs continuously and updates opportunities
"""

import time
import schedule
from main_analyzer import KalshiAnalyzer
from datetime import datetime

def run_scan():
    """Run a complete scan"""
    print("\n" + "=" * 80)
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting scan...")
    print("=" * 80)

    try:
        analyzer = KalshiAnalyzer()
        opportunities = analyzer.run_full_scan()

        if opportunities:
            analyzer.save_opportunities(opportunities)
            print(f"\n✓ Scan complete - {len(opportunities)} opportunities saved")
        else:
            print("\n⚠ No opportunities found this scan")

    except Exception as e:
        print(f"\n✗ Scan failed: {e}")

    print("=" * 80)
    print(f"Next scan in 15 minutes...")
    print("=" * 80)

if __name__ == "__main__":
    print("=" * 80)
    print("KALSHI BACKGROUND SCANNER")
    print("=" * 80)
    print("\nScanning all Kalshi markets every 15 minutes")
    print("Dashboard will show latest opportunities")
    print("\nPress Ctrl+C to stop")
    print("=" * 80)
    print()

    # Run immediately on start
    run_scan()

    # Schedule to run every 15 minutes
    schedule.every(15).minutes.do(run_scan)

    # Keep running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
