# Quantum Swing Trading Algorithm — QuantConnect

A **quantum-computing-powered** swing trading algorithm built for the QuantConnect LEAN engine.
Targets **100 %+ annual returns** from a $10,000 starting balance with holding periods of 3–21 days.

---

## Quantum Computing Components

All quantum subroutines are classically simulated via NumPy — the standard way quantum-inspired
algorithms run before quantum hardware reaches fault-tolerance at scale.

| Module | Acronym | Role |
|---|---|---|
| Variational Quantum Classifier | **VQC** | Encodes 4 normalised financial features via angle encoding + entanglement layers; produces directional probability |
| Quantum Kernel Method | **QKM** | Computes similarity in quantum Hilbert space vs. ideal bull/bear reference states |
| Quantum Amplitude Estimation | **QAE** | Grover-amplitude-estimation over the empirical return distribution to estimate win probability |
| Quantum Approx. Optimisation Algorithm | **QAOA** | Solves portfolio selection as a QUBO via quantum annealing (Suzuki-Trotter decomposition, 8 replicas) |
| Quantum Random Walk | **QRW** | Discrete-time quantum walk on a price graph; detects trending vs. ranging regimes |

Signal blend: **45 % quantum + 55 % classical technical**.

---

## Classical Technical Signals

- **Momentum**: RSI(14), MACD histogram, Stochastic(14), 5-day & 20-day returns
- **Trend**: SMA20/SMA50 ratio, ADX(14), linear trend slope
- **Volume**: Volume ratio vs 20-day avg, OBV trend correlation
- **Mean reversion**: Bollinger Band z-score

---

## Risk Management

| Rule | Value |
|---|---|
| Hard stop loss | 8 % |
| Trailing stop (once +10 %) | 5 % from peak |
| Take profit | 20 % base (scales with ATR) |
| Max holding period | 21 days |
| Min holding period | 3 days |
| Max simultaneous positions | 5 |
| Position size | ~18 % of portfolio (Kelly-adjusted) |
| Portfolio drawdown kill switch | 22 % |

---

## Self-Adjustment (Weekly)

Every Monday the algorithm runs `_weekly_self_adjustment()`:

1. Computes a Sharpe proxy from the last 4 weeks of returns.
2. Estimates annualised return; if underperforming 100 % target, increases exploration noise.
3. Applies a **parameter-shift-inspired gradient update** to the VQC θ parameters.
4. Adapts the bull/bear Hilbert-space reference states to the current market regime.

---

## How to Run

### QuantConnect Cloud (easiest)

1. Create a new project at [quantconnect.com](https://www.quantconnect.com)
2. Paste `main.py` into the code editor
3. Set start date 2019-01-01, end date 2024-12-31, cash $10,000
4. Click **Backtest**

### LEAN CLI (local)

```bash
pip install lean
lean init
lean backtest "QuantumSwingTrader"
```

---

## Architecture

```
main.py
├── QuantumCircuit          # n-qubit statevector simulator (NumPy)
├── QuantumModules          # VQC · QKM · QAE · QAOA · QRW
├── FeatureEngine           # RSI · MACD · ADX · Bollinger · OBV · ATR
└── QuantumSwingTradingAlgorithm (QCAlgorithm)
    ├── Initialize()        # universe, schedules, risk model
    ├── _morning_scan()     # signal generation + QAOA position selection
    ├── _evening_review()   # stop/take-profit/trailing exit management
    ├── _weekly_self_adjustment()  # quantum parameter optimisation
    └── OnEndOfAlgorithm()  # performance report
```

---

## Parameter Quick Reference

Edit the class-level constants at the top of `QuantumSwingTradingAlgorithm` to tune:

```python
MAX_POSITIONS     = 5       # simultaneous open trades
BASE_POSITION_PCT = 0.18    # 18 % per position
HARD_STOP_LOSS    = 0.08    # 8 % stop
TAKE_PROFIT_BASE  = 0.20    # 20 % target
SIGNAL_THRESHOLD  = 0.12    # minimum score to enter
```

Quantum circuit depth and qubit count are in `QuantumModules`:

```python
N_QUBITS      = 4
CIRCUIT_DEPTH = 3
```
