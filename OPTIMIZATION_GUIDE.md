# 🔧 Optimization Guide - Backtesting & Parameter Tuning

## 📊 Backtesting Methodology

### Step 1: Initial Test (Default Parameters)
1. Load indicator on 1H chart
2. Select ticker (SOUN, UPWK, or CLSK)
3. Go back 6-12 months of data
4. Mark every BUY and SELL signal
5. Record results in spreadsheet

### Step 2: Track These Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| **Total Signals** | Count all buy signals | 15-30 per 6 months |
| **Winning Trades** | Signals that hit targets before stop | - |
| **Losing Trades** | Signals that hit stop first | - |
| **Win Rate** | (Wins / Total) × 100 | 60-80% |
| **Avg Win** | Sum of wins / # wins | +12-20% |
| **Avg Loss** | Sum of losses / # losses | -8-10% |
| **Profit Factor** | Gross profit / Gross loss | >1.5 |
| **Max Drawdown** | Largest peak-to-valley drop | <20% |
| **Consecutive Losses** | Longest losing streak | <4 |

### Step 3: Backtest Template (Spreadsheet)

```
| Date | Ticker | Score | Entry | Stop | T1 | T2 | Exit | P/L % | Notes |
|------|--------|-------|-------|------|----|----|------|-------|-------|
| 1/15 | SOUN   | 6/10  | 5.00  | 4.50 | 5.50 | 5.75 | 5.60 | +12% | Hit T1, trailed |
| 1/22 | UPWK   | 5/10  | 14.20 | 12.78 | - | - | 12.78 | -10% | Stopped out |
```

## ⚙️ Parameter Optimization

### If Win Rate < 60% (Too Many False Signals)

**Tighten Criteria:**
```
Minimum Criteria: 4 → 5 or 6
ADX Threshold: 25 → 30-35
Volume Increase %: 20 → 30-40
RSI Oversold: 30 → 25
RSI Overbought: 70 → 75
```

**Result:** Fewer signals, higher quality

---

### If Win Rate > 75% but Few Signals (Missing Opportunities)

**Loosen Criteria:**
```
Minimum Criteria: 4 → 3
ADX Threshold: 25 → 20
Volume Increase %: 20 → 15
Suite Fast/Slow: 8/21 → 6/17
```

**Result:** More signals, slightly lower win rate but higher total profit

---

### If Stopped Out Too Often (Avg Loss > -8%)

**Widen Stops:**
```
Stop Loss %: 10 → 12-15
```

**Or Add Volatility Filter:**
```
Only trade when ATR is in middle range (not extreme high/low)
```

**Or Adjust Entry Timing:**
```
Wait for deeper pullback to VWAP
Require price to be closer to support
```

---

### If Average Win < +12%

**Adjust Targets:**
```
First Target %: 10 → 8
Second Target %: 15 → 12
```

**Or Trail More Aggressively:**
```
Use tighter trailing stop (e.g., 3 ATR instead of 4 ATR)
```

---

### If Too Many Whipsaws (In and out quickly)

**Add Trend Filter:**
```
ADX Threshold: 25 → 30
Only trade when daily 50 EMA > 200 EMA (strong trend)
```

**Add Volatility Filter:**
```
Require Bollinger Band squeeze before signal
ATR must be expanding (not contracting)
```

---

## 📈 Stock-Specific Optimization

### SOUN (High Beta Tech Stock)

**Characteristics:** High volatility, large moves, frequent gaps

**Recommended Settings:**
```
Stop Loss %: 15%
First Target %: 12%
Second Target %: 20%
Minimum Criteria: 5
ADX Threshold: 25
Volume Increase %: 30%
Suite Fast/Slow: 8/21 (default)
Green Mountain Trend: 50 (default)
```

**Notes:**
- Wider stops needed due to volatility
- Can achieve larger gains, so extend targets
- Require strong volume confirmation (30%)
- Best during tech sector strength

---

### UPWK (Medium Volatility Service Stock)

**Characteristics:** Moderate volatility, steady trends, responds to earnings

**Recommended Settings:**
```
Stop Loss %: 10%
First Target %: 10%
Second Target %: 15%
Minimum Criteria: 4
ADX Threshold: 25
Volume Increase %: 20%
Suite Fast/Slow: 8/21 (default)
Green Mountain Trend: 50 (default)
```

**Notes:**
- Default settings work well
- Avoid trading week before/after earnings
- Watch for sector rotation (gig economy sentiment)
- Best during stable market conditions

---

### CLSK (Crypto-Related Mining Stock)

**Characteristics:** Extreme volatility, follows Bitcoin, sentiment-driven

**Recommended Settings:**
```
Stop Loss %: 15-20%
First Target %: 15%
Second Target %: 25%
Minimum Criteria: 5-6
ADX Threshold: 30
Volume Increase %: 40%
Suite Fast/Slow: 6/17 (faster)
Green Mountain Trend: 40 (more sensitive)
```

**Notes:**
- Extremely volatile - size down to 3-5% of account
- Follow Bitcoin price closely
- Require very strong confirmation (5-6 criteria)
- Can achieve explosive gains but high risk
- Best during crypto bull markets

---

## 🎯 Optimization by Market Condition

### Bull Market (Strong Uptrend)

**Settings:**
```
Focus on: BUY signals only
Daily Trend: Must be in uptrend
Minimum Criteria: 4 (can be lenient)
Stop Loss %: 10% (standard)
Targets: 10% / 15%
```

**Strategy:** Ride the wave, take quick profits, re-enter dips

---

### Bear Market (Strong Downtrend)

**Settings:**
```
Focus on: SELL signals or stay in cash
Daily Trend: Must be in downtrend for shorts
Minimum Criteria: 5-6 (be selective)
Stop Loss %: 8% (tighter)
Targets: 8% / 12%
```

**Strategy:** Short rallies, take profits faster, preserve capital

---

### Sideways / Range-Bound Market

**Settings:**
```
Minimum Criteria: 6 (very selective)
ADX Threshold: 20 (lower, as no strong trends)
RSI: Focus on extremes (<25 or >75)
Bollinger Bands: Use squeezes for breakouts
Volume %: 30-40% (require strong volume)
```

**Strategy:** Mean reversion, buy support / sell resistance, quick profits

---

## 📊 Advanced Optimization

### Sector Strength Filter
Add this manual check:
- Only trade stocks where sector is outperforming SPY
- Use sector ETF comparison (e.g., XLK for tech, XLC for communications)

### Relative Strength
Add this manual check:
- Stock should be making higher highs while market makes lower highs (relative strength)
- Or stock should be outperforming sector ETF by >5% over 1 month

### Volatility Regime
Add this manual check:
- Calculate 20-day ATR
- Only trade when ATR is in middle 40-60% range
- Avoid when ATR is at extremes (too quiet or too wild)

### Earnings Avoidance
Add this manual check:
- Don't enter positions within 5 days before earnings
- Exit positions 2 days before earnings (or tighten stops to breakeven)

---

## 🧪 A/B Testing Framework

### Test 1: Conservative vs Aggressive
```
Setup A (Conservative):
- Min Criteria: 6
- Stop: 8%
- ADX: 30
- Expected: 75%+ win rate, fewer signals

Setup B (Aggressive):
- Min Criteria: 3
- Stop: 12%
- ADX: 20
- Expected: 55-65% win rate, more signals
```

Run both for 3 months, compare total P/L

---

### Test 2: Fast vs Slow Suite Diamonds
```
Setup A (Fast):
- Suite Fast/Slow: 5/13
- Expected: Earlier entries, more signals, more whipsaws

Setup B (Slow):
- Suite Fast/Slow: 13/34
- Expected: Later entries, fewer signals, higher quality
```

Run both for 3 months, compare win rate and profit factor

---

### Test 3: Tight vs Wide Stops
```
Setup A (Tight):
- Stop: 7%
- Expected: Lower max drawdown, lower win rate

Setup B (Wide):
- Stop: 15%
- Expected: Higher win rate, higher max drawdown
```

Run both for 3 months, compare risk-adjusted returns

---

## 📝 Optimization Checklist

When adjusting parameters, follow this process:

1. **Change ONE parameter at a time**
   - Don't adjust multiple settings simultaneously
   - You won't know what worked/didn't work

2. **Test for adequate sample size**
   - Minimum 20 signals to draw conclusions
   - Preferably 30-50 signals over 6 months

3. **Account for market regime**
   - Bull market? Bear market? Sideways?
   - Settings that work in bull may fail in bear

4. **Document everything**
   - Keep a log of parameter changes
   - Note market conditions during test period
   - Track specific metrics (win rate, profit factor, drawdown)

5. **Avoid overfitting**
   - Don't optimize to perfection on historical data
   - Settings that give 95% win rate in backtest will fail live
   - Aim for realistic 60-70% win rate

6. **Forward test before live trading**
   - Paper trade for 1-2 months with new settings
   - Ensure results match backtest

---

## 🎯 Target Optimization Results

| Metric | Minimum | Good | Excellent |
|--------|---------|------|-----------|
| Win Rate | 55% | 65% | 75% |
| Profit Factor | 1.3 | 1.8 | 2.5+ |
| Avg Win / Avg Loss | 1.2 | 1.8 | 2.5+ |
| Max Drawdown | <25% | <18% | <12% |
| Signals per Month | 2+ | 4-6 | 8-10 |
| Consecutive Losses | <5 | <4 | <3 |

---

## 🚨 Warning Signs (Stop Using These Settings)

- Win rate < 50% consistently
- Profit factor < 1.0
- Max drawdown > 30%
- Average loss > average win
- 5+ consecutive losses
- Signals per month < 1 (too restrictive)
- Signals per month > 20 (too loose, overtrading)

If any of the above occur, **STOP trading live** and re-optimize.

---

## 💡 Final Tips

1. **Backtest is not live trading**
   - You'll execute some signals late
   - Slippage and commissions matter
   - Emotions will affect your decisions
   - Expect live results to be 10-20% worse than backtest

2. **Track forward performance**
   - Keep a live trading journal
   - Compare to backtest monthly
   - Adjust if divergence occurs

3. **Review quarterly**
   - Every 3 months, review all parameters
   - Adjust for changing market conditions
   - Don't change too frequently (parameter drift)

4. **Trust the process**
   - Losing streaks happen (even with 70% win rate)
   - Don't abandon system after 3 losses
   - Evaluate over 30+ trades minimum

---

**Remember: The goal isn't perfection. The goal is a consistent edge executed with discipline.**

Good luck with your optimization! 📈
