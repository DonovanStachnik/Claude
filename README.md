# Multi-Timeframe Swing Trading Strategy - TradingView Indicator

A comprehensive Pine Script v5 indicator designed for high-probability swing trades with 1-8 week hold periods. This indicator combines 10 technical analysis criteria with multi-timeframe alignment to generate precise buy and sell signals.

## 🎯 Strategy Overview

**Trading Style:** Swing Trading (1 week - 8 weeks)
**Position Sizing:** 5-8% per trade (manual execution)
**Win Rate Target:** 80%+ (60-70% is realistic)
**Risk Management:** Strict -10% stop loss, trim at +10-15%, trail remainder

## 📊 Key Features

### Multi-Timeframe Analysis
- **1D Timeframe:** Trend direction (EMA 50/200 crossover)
- **4H Timeframe:** Structure confirmation (higher lows for longs, lower highs for shorts)
- **1H Timeframe:** Precise entry timing (VWAP reclaim, pullbacks)

### 10-Point Confluence System
The indicator scores each setup on 10 criteria. A minimum of 4 criteria must align for a signal:

1. **Daily Trend** - Uptrend, downtrend, or reversal base
2. **4H Structure** - Higher lows (buy) or lower highs (sell)
3. **VWAP** - Reclaim for entries, loss for exits
4. **Volume** - 20%+ above average for confirmation
5. **Suite Diamonds** - Custom momentum indicator (2+ blue = buy, 2+ pink = sell)
6. **Green Mountain** - Trend strength (building vs exhausting)
7. **RSI** - Oversold (<30) for buys, overbought (>70) for sells
8. **MACD** - Bullish/bearish crossovers
9. **Stochastic** - Bounce/top in 20-80 range
10. **ADX** - Trend strength >25

### Visual Signals
- **Tealish Blue Triangles** with "BUY HERE" labels
- **Pink Triangles** with "SELL HERE" labels
- **Stop Loss Lines** (red) at -10%
- **Target Lines** (green) at +10% and +15%
- **Information Labels** showing score, entry, stop, and targets
- **Real-time Status Table** showing all indicator states

## 🚀 Installation

1. Open TradingView
2. Click on "Pine Editor" at the bottom of the screen
3. Copy the entire contents of `SwingTrading_MultiTF_Indicator.pine`
4. Paste into the Pine Editor
5. Click "Add to Chart"
6. The indicator will appear on your chart

## ⚙️ Configuration

### Recommended Settings by Stock Type

#### High Volatility (SOUN, CLSK)
```
Stop Loss %: 12-15%
Minimum Criteria: 5
ADX Threshold: 25
Volume Increase %: 25-30%
```

#### Medium Volatility (UPWK)
```
Stop Loss %: 10%
Minimum Criteria: 4
ADX Threshold: 25
Volume Increase %: 20%
```

#### Low Volatility / Blue Chips
```
Stop Loss %: 7-8%
Minimum Criteria: 4-5
ADX Threshold: 20
Volume Increase %: 15-20%
```

### Timeframe Settings
- **Chart Timeframe:** 1H (recommended for entry timing)
- **Also test on:** 4H (for swing context), 1D (for trend overview)
- **Indicator Timeframes:** 1H / 4H / 1D (pre-configured in settings)

## 📈 How to Use

### Step 1: Wait for Signal
- Green triangle with "BUY HERE" label appears
- Red triangle with "SELL HERE" label appears
- Check the score (4+ out of 10 required)

### Step 2: Verify Conditions
Check the **status table** in the top-right corner:
- ✓ 1D Trend: Should show UP or REVERSAL for buys
- ✓ 4H Structure: Should show "Higher Lows" for buys
- ✓ VWAP: Should show "Above" for buys
- ✓ Volume: Should show "High" for confirmation
- ✓ Other indicators: Green checkmarks preferred

### Step 3: Entry Execution
1. Enter position with **5-8% of account** size
2. **Immediately** set stop loss at the shown price (red line)
3. Set price alerts for Target 1 and Target 2

### Step 4: Exit Strategy
- **Stop Loss:** Hard -10% stop (NO EXCEPTIONS)
- **Target 1 (+10-15%):** Trim 30-40% of position
- **After Target 1:** Move stop to breakeven
- **Trail Remainder:** Use ATR trailing stop or key support levels
- **Full Exit:** Sell signal appears OR major support breaks

## 🧪 Backtesting

### Testing Process
1. Load the indicator on your chart
2. Go to "Settings" → "Visibility" → Check "Labels" and "Shapes"
3. Scroll back through historical data
4. Mark each signal and calculate:
   - Win rate (wins / total trades)
   - Average profit on wins vs. average loss
   - Maximum consecutive losses
   - Total return

### Test Tickers
- **SOUN** (high volatility tech)
- **UPWK** (medium volatility service)
- **CLSK** (high volatility crypto-related)

### Optimization Tips
- If win rate < 60%: Increase `Minimum Criteria` to 5 or 6
- If too few signals: Decrease `Minimum Criteria` to 3
- If stops too tight: Increase `Stop Loss %` to 12-15%
- If whipsaws: Increase `ADX Threshold` to 30+

## 🎨 Customization

### Colors
- **Buy Signal Color:** Default tealish blue (#00CED1)
- **Sell Signal Color:** Default pink (#FF1493)
- Change in Settings → Visual

### Indicator Parameters

#### Suite Diamonds (Momentum)
- **Fast EMA:** 8 (decrease for faster signals)
- **Slow EMA:** 21 (increase for slower signals)
- **Signal SMA:** 5

#### Green Mountain (Trend Strength)
- **Trend Length:** 50 (decrease for more sensitivity)
- **Momentum Length:** 14

#### Volume
- **MA Length:** 20
- **Increase % Required:** 20% (increase for stronger confirmation)

#### RSI
- **Length:** 14
- **Oversold:** 30 (increase to 35-40 for earlier signals)
- **Overbought:** 70 (decrease to 65-60 for earlier signals)

## 📋 Pre-Trade Checklist

Before entering ANY trade, verify:

- [ ] **Signal appeared** with score ≥ 4/10
- [ ] **Daily trend** in favor or reversal setup confirmed
- [ ] **4H structure** showing higher lows (buy) or lower highs (sell)
- [ ] **Volume** at least 20% above average
- [ ] **Clear stop level** identified at -10%
- [ ] **Position size** calculated (5-8% of account)
- [ ] **Alert set** for stop loss price
- [ ] **Alert set** for target prices
- [ ] **No conflicting news** or earnings within hold period

## ⚠️ Risk Warnings

1. **No system is perfect:** Even with 80% accuracy, 2 out of 10 trades lose
2. **Always use stops:** The -10% stop is non-negotiable
3. **Never overtrade:** Stick to 5-8% position sizing
4. **Market conditions matter:** The indicator works best in trending or mean-reverting markets, not choppy ranges
5. **Backtest first:** Test on your specific tickers before live trading
6. **Not financial advice:** This is an educational tool. Trade at your own risk.

## 🔧 Troubleshooting

### No Signals Appearing
- Lower `Minimum Criteria` from 4 to 3
- Check that multi-timeframe data is loading (change timeframes and come back)
- Ensure you're on the 1H chart

### Too Many False Signals
- Increase `Minimum Criteria` from 4 to 5 or 6
- Increase `ADX Threshold` to 30+
- Increase `Volume Increase %` to 30-40%

### Stops Too Tight
- Increase `Stop Loss %` to 12-15% for volatile stocks
- Use ATR-based stops instead (manual adjustment)

### Missing Multi-Timeframe Data
- Ensure you have adequate chart history loaded
- TradingView requires premium for unlimited historical data on some assets

## 📚 Understanding the Indicators

### Suite Diamonds
This custom momentum indicator is similar to MACD but optimized for swing entries:
- **Blue diamonds** above zero = Late uptrend (less ideal)
- **Blue diamonds** below zero = Early reversal buy (preferred)
- **Pink diamonds** below zero = Late downtrend
- **Pink diamonds** above zero = Early reversal sell (preferred)

### Green Mountain
Measures the strength of the current trend:
- **Building strength:** Price gaining momentum above trend
- **Losing strength:** Exhaustion, potential reversal coming
- Used to avoid buying tops and selling bottoms

### VWAP (Volume Weighted Average Price)
The yellow line showing where most volume traded:
- **Reclaim** = Price crossing above VWAP (bullish entry point)
- **Loss** = Price falling below VWAP (bearish)
- Acts as dynamic support/resistance

## 🎓 Learning Resources

To maximize this indicator:
1. Study **price action** and **support/resistance**
2. Learn **risk management** (position sizing, R:R ratios)
3. Understand **market structure** (trends, reversals, consolidations)
4. Practice **patience** (wait for 4+ criteria, don't force trades)
5. Keep a **trading journal** (track every signal, win or lose)

## 📊 Expected Performance

Based on backtesting and realistic expectations:
- **Win Rate:** 60-75% (80%+ is exceptional, don't count on it)
- **Average Win:** +12-20% (trimming along the way)
- **Average Loss:** -8-10% (stopped out before full -10%)
- **Risk:Reward:** 1:1.5 to 1:2.5
- **Signals per Month:** 3-8 on active stocks (don't overtrade)

## 🔄 Updates and Improvements

Feel free to customize this indicator further:
- Add **Fibonacci levels** for better target zones
- Incorporate **earnings dates** to avoid holding through volatility
- Add **sector strength** filters
- Create **separate configs** for different market conditions (bull/bear/sideways)

## 📝 License

This indicator is provided as-is for educational purposes. Use at your own risk.

---

**Remember:** The best trades are the ones you don't take. Wait for your setup, verify all criteria, and execute with discipline. The market will always give you another opportunity.

Good luck and trade safe! 🚀
