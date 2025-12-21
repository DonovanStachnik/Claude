"""
Suite Diamond Signal Scanner
Detects Green X (bullish) and Red X (bearish) signals from TradingView Pine Script strategy
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Tuple


def calculate_ema(data: pd.Series, period: int) -> pd.Series:
    """Calculate Exponential Moving Average"""
    return data.ewm(span=period, adjust=False).mean()


def calculate_sma(data: pd.Series, period: int) -> pd.Series:
    """Calculate Simple Moving Average"""
    return data.rolling(window=period).mean()


def detect_suite_diamond_signals(df: pd.DataFrame) -> Tuple[bool, bool, bool, bool]:
    """
    Detect Suite Diamond signals based on TradingView Pine Script logic

    Returns:
        (green_x_today, red_x_today, current_green_x, current_red_x)
    """
    if len(df) < 50:  # Need enough data
        return False, False, False, False

    # Calculate Suite Diamond components (from Pine Script)
    fast_ema = calculate_ema(df['Close'], 8)
    slow_ema = calculate_ema(df['Close'], 21)
    suite_macd = fast_ema - slow_ema
    suite_signal = calculate_sma(suite_macd, 5)

    # Detect crossovers/crossunders
    macd_above_signal = suite_macd > suite_signal
    macd_below_signal = suite_macd < suite_signal

    macd_above_signal_prev = macd_above_signal.shift(1)
    macd_below_signal_prev = macd_below_signal.shift(1)

    # Crossover = MACD crosses above signal
    crossover = (~macd_above_signal_prev) & macd_above_signal

    # Crossunder = MACD crosses below signal
    crossunder = (~macd_below_signal_prev) & macd_below_signal

    # Green X signals (Bullish)
    # suiteBlueDiamond = crossover AND macd > 0
    # suiteBlueDiamondEarly = crossover AND macd <= 0
    blue_diamond = crossover & (suite_macd > 0)
    blue_diamond_early = crossover & (suite_macd <= 0)
    green_x = blue_diamond | blue_diamond_early

    # Red X signals (Bearish)
    # suitePinkDiamond = crossunder AND macd < 0
    # suitePinkDiamondEarly = crossunder AND macd >= 0
    pink_diamond = crossunder & (suite_macd < 0)
    pink_diamond_early = crossunder & (suite_macd >= 0)
    red_x = pink_diamond | pink_diamond_early

    # Check if signal happened today (last bar)
    green_x_today = green_x.iloc[-1] if len(green_x) > 0 else False
    red_x_today = red_x.iloc[-1] if len(red_x) > 0 else False

    # Check if there's an active signal in last 5 bars
    current_green_x = green_x.iloc[-5:].any() if len(green_x) >= 5 else False
    current_red_x = red_x.iloc[-5:].any() if len(red_x) >= 5 else False

    return green_x_today, red_x_today, current_green_x, current_red_x


def scan_ticker(symbol: str, timeframe: str = '1d') -> Dict:
    """
    Scan a single ticker for Suite Diamond signals

    Args:
        symbol: Stock ticker symbol
        timeframe: Timeframe for data ('1d', '1h', etc.)

    Returns:
        Dictionary with signal information
    """
    try:
        # Download data (60 days for daily, more for intraday)
        period = '60d' if timeframe == '1d' else '5d'
        interval = timeframe

        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)

        if df.empty or len(df) < 50:
            return {
                'symbol': symbol,
                'error': 'Insufficient data',
                'green_x_today': False,
                'red_x_today': False
            }

        # Detect signals
        green_x_today, red_x_today, current_green, current_red = detect_suite_diamond_signals(df)

        # Get current price and volume
        current_price = df['Close'].iloc[-1]
        current_volume = df['Volume'].iloc[-1]

        # Calculate price change
        if len(df) >= 2:
            price_change_pct = ((df['Close'].iloc[-1] - df['Close'].iloc[-2]) / df['Close'].iloc[-2]) * 100
        else:
            price_change_pct = 0

        return {
            'symbol': symbol,
            'green_x_today': bool(green_x_today),
            'red_x_today': bool(red_x_today),
            'current_green': bool(current_green),
            'current_red': bool(current_red),
            'price': float(current_price),
            'volume': int(current_volume),
            'change_pct': float(price_change_pct),
            'error': None
        }

    except Exception as e:
        return {
            'symbol': symbol,
            'error': str(e),
            'green_x_today': False,
            'red_x_today': False
        }


def scan_all_tickers(ticker_file: str = 'tickers.txt', signal_type: str = 'bullish',
                     timeframe: str = '1d') -> List[Dict]:
    """
    Scan all tickers from file for signals

    Args:
        ticker_file: Path to file containing ticker symbols
        signal_type: 'bullish' for green X, 'bearish' for red X, 'all' for both
        timeframe: Timeframe to scan ('1d' for daily)

    Returns:
        List of dictionaries containing signal results
    """
    # Load tickers
    with open(ticker_file, 'r') as f:
        tickers = [line.strip() for line in f if line.strip()]

    print(f"Scanning {len(tickers)} tickers for {signal_type} signals on {timeframe} timeframe...")

    results = []
    for i, symbol in enumerate(tickers):
        if (i + 1) % 50 == 0:
            print(f"Progress: {i + 1}/{len(tickers)}...")

        result = scan_ticker(symbol, timeframe)

        # Filter based on signal type
        if signal_type == 'bullish' and result.get('green_x_today'):
            results.append(result)
        elif signal_type == 'bearish' and result.get('red_x_today'):
            results.append(result)
        elif signal_type == 'all' and (result.get('green_x_today') or result.get('red_x_today')):
            results.append(result)

    print(f"Scan complete! Found {len(results)} signals.")
    return results


def format_results(results: List[Dict], signal_type: str) -> str:
    """
    Format scan results for display

    Args:
        results: List of signal result dictionaries
        signal_type: 'bullish' or 'bearish'

    Returns:
        Formatted string for Telegram message
    """
    if not results:
        return f"🔍 No fresh {signal_type.upper()} signals found today."

    emoji = "🟢" if signal_type == 'bullish' else "🔴"
    signal_name = "GREEN X" if signal_type == 'bullish' else "RED X"

    message = f"{emoji} *{signal_name} SIGNALS TODAY* {emoji}\n"
    message += f"Found {len(results)} fresh signals:\n\n"

    # Sort by volume (most liquid first)
    results_sorted = sorted(results, key=lambda x: x.get('volume', 0), reverse=True)

    for i, result in enumerate(results_sorted[:20], 1):  # Limit to top 20
        symbol = result['symbol']
        price = result.get('price', 0)
        change = result.get('change_pct', 0)
        volume = result.get('volume', 0)

        change_emoji = "📈" if change > 0 else "📉"

        message += f"{i}. *{symbol}*\n"
        message += f"   💵 ${price:.2f} {change_emoji} {change:+.2f}%\n"
        message += f"   📊 Vol: {volume:,}\n\n"

    if len(results) > 20:
        message += f"_(Showing top 20 by volume, {len(results) - 20} more found)_\n"

    message += f"\n🕐 Scanned: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    return message


if __name__ == "__main__":
    # Test the scanner
    print("Testing scanner with a few tickers...")
    test_results = scan_ticker('AAPL', '1d')
    print(f"\nTest result for AAPL: {test_results}")
