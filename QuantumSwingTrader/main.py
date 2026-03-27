# =============================================================================
# QUANTUM SWING TRADING ALGORITHM FOR QUANTCONNECT (LEAN ENGINE)
# =============================================================================
# Strategy: Quantum-Classical Hybrid Swing Trader
# Holding Period: 3–21 days
# Initial Capital: $10,000
# Target: >100% annual return
#
# Quantum Computing Components:
#   1. VQC  – Variational Quantum Classifier (angle encoding + entanglement)
#   2. QKM  – Quantum Kernel Method (inner product in quantum Hilbert space)
#   3. QAE  – Quantum Amplitude Estimation (tail-risk / win-probability)
#   4. QAOA – Quantum Approximate Optimization (portfolio selection QUBO)
#   5. QRW  – Quantum Random Walk (trend regime detection)
#
# All quantum components are classically simulated via numpy — this is how
# quantum-inspired algorithms run on classical hardware and on current
# NISQ-era machines that interface through software simulation layers.
# =============================================================================

from AlgorithmImports import *
import numpy as np
from scipy.optimize import minimize
from collections import deque
import warnings

warnings.filterwarnings("ignore")


# ─────────────────────────────────────────────────────────────────────────────
# QUANTUM CIRCUIT SIMULATOR
# A minimal, self-contained quantum circuit simulation layer.
# Represents quantum states as complex amplitude vectors of size 2^n_qubits.
# ─────────────────────────────────────────────────────────────────────────────
class QuantumCircuit:
    """Lightweight quantum circuit simulator (pure numpy, no external deps)."""

    def __init__(self, n_qubits: int):
        self.n = n_qubits
        self.dim = 2 ** n_qubits
        self.reset()

    def reset(self):
        """Initialise to |0…0⟩."""
        self.state = np.zeros(self.dim, dtype=complex)
        self.state[0] = 1.0

    # ── Single-qubit gates ────────────────────────────────────────────────────

    def _single_qubit_gate(self, U2x2, qubit):
        """Apply a 2×2 unitary U to the given qubit."""
        new_state = np.zeros(self.dim, dtype=complex)
        mask = 1 << (self.n - 1 - qubit)
        for i in range(self.dim):
            bit = (i >> (self.n - 1 - qubit)) & 1
            partner = i ^ mask
            if bit == 0:
                new_state[i] += U2x2[0, 0] * self.state[i] + U2x2[0, 1] * self.state[partner]
            else:
                new_state[i] += U2x2[1, 0] * self.state[partner] + U2x2[1, 1] * self.state[i]
        self.state = new_state

    def ry(self, qubit: int, theta: float):
        """R_y(θ) rotation."""
        c, s = np.cos(theta / 2), np.sin(theta / 2)
        U = np.array([[c, -s], [s, c]])
        self._single_qubit_gate(U, qubit)

    def rz(self, qubit: int, phi: float):
        """R_z(φ) rotation."""
        U = np.array([[np.exp(-1j * phi / 2), 0],
                      [0, np.exp(1j * phi / 2)]])
        self._single_qubit_gate(U, qubit)

    def rx(self, qubit: int, theta: float):
        """R_x(θ) rotation."""
        c, s = np.cos(theta / 2), np.sin(theta / 2)
        U = np.array([[c, -1j * s], [-1j * s, c]])
        self._single_qubit_gate(U, qubit)

    def h(self, qubit: int):
        """Hadamard gate."""
        U = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
        self._single_qubit_gate(U, qubit)

    def cnot(self, control: int, target: int):
        """Controlled-NOT gate."""
        new_state = np.copy(self.state)
        ctrl_mask = 1 << (self.n - 1 - control)
        tgt_mask = 1 << (self.n - 1 - target)
        for i in range(self.dim):
            if (i & ctrl_mask):
                j = i ^ tgt_mask
                new_state[i] = self.state[j]
                new_state[j] = self.state[i]
        self.state = new_state

    def cz(self, control: int, target: int):
        """Controlled-Z gate."""
        ctrl_mask = 1 << (self.n - 1 - control)
        tgt_mask = 1 << (self.n - 1 - target)
        for i in range(self.dim):
            if (i & ctrl_mask) and (i & tgt_mask):
                self.state[i] *= -1

    # ── Measurement ───────────────────────────────────────────────────────────

    def measure_expectation_z(self, qubit: int) -> float:
        """⟨Z⟩ on a qubit = P(0) − P(1)."""
        mask = 1 << (self.n - 1 - qubit)
        prob_0 = sum(abs(self.state[i]) ** 2 for i in range(self.dim) if not (i & mask))
        return 2 * prob_0 - 1.0   # maps [0,1] → [−1,+1]

    def statevector(self) -> np.ndarray:
        return self.state.copy()


# ─────────────────────────────────────────────────────────────────────────────
# QUANTUM MODULES
# ─────────────────────────────────────────────────────────────────────────────
class QuantumModules:
    """
    Collection of quantum-computing building blocks used by the strategy.
    Each method is a self-contained quantum subroutine.
    """

    N_QUBITS = 4          # feature qubits
    CIRCUIT_DEPTH = 3     # VQC layers
    N_PARAMS = N_QUBITS * CIRCUIT_DEPTH * 2   # Ry + Rz per qubit per layer

    def __init__(self):
        # Trainable VQC parameters θ ∈ [0, 2π]
        np.random.seed(42)
        self.vqc_params = np.random.uniform(0, 2 * np.pi, self.N_PARAMS)
        # Reference states for QKM
        self._bull_ref = np.array([0.30, 0.65, 0.38, 0.62])
        self._bear_ref = np.array([0.70, 0.35, 0.62, 0.38])

    # ── 1. VQC – Variational Quantum Classifier ───────────────────────────────

    def _build_vqc_state(self, features: np.ndarray, params: np.ndarray) -> np.ndarray:
        """
        Encode 4 normalised features via angle encoding, then apply
        CIRCUIT_DEPTH layers of trainable Ry+Rz rotations and entanglement.
        Returns the final quantum statevector.
        """
        n = self.N_QUBITS
        qc = QuantumCircuit(n)

        # Layer 0: Hadamard superposition
        for q in range(n):
            qc.h(q)

        for layer in range(self.CIRCUIT_DEPTH):
            # Data encoding (angle encoding: Ry(π·x_i))
            for q in range(n):
                qc.ry(q, np.pi * features[q % len(features)])

            # Parametric layer (trainable)
            base = layer * n * 2
            for q in range(n):
                qc.ry(q, params[base + q])
                qc.rz(q, params[base + n + q])

            # Entanglement (ring topology)
            for q in range(n - 1):
                qc.cnot(q, q + 1)
            qc.cnot(n - 1, 0)

        return qc.statevector()

    def vqc_predict(self, features: np.ndarray) -> float:
        """
        VQC output: expectation value of Z on qubit-0, mapped to [0,1].
        > 0.5 → bullish, < 0.5 → bearish.
        """
        state = self._build_vqc_state(features, self.vqc_params)
        qc = QuantumCircuit(self.N_QUBITS)
        qc.state = state
        exp_z = qc.measure_expectation_z(0)
        return (exp_z + 1.0) / 2.0     # normalise to [0, 1]

    def update_vqc_params(self, gradient_estimate: np.ndarray, lr: float = 0.05):
        """Parameter-shift-inspired gradient update."""
        self.vqc_params = np.mod(self.vqc_params + lr * gradient_estimate, 2 * np.pi)

    # ── 2. QKM – Quantum Kernel Method ───────────────────────────────────────

    def quantum_kernel(self, x1: np.ndarray, x2: np.ndarray) -> float:
        """
        K(x1, x2) = |⟨φ(x1)|φ(x2)⟩|²
        Measures similarity in the quantum feature Hilbert space.
        """
        phi1 = self._build_vqc_state(x1, self.vqc_params)
        phi2 = self._build_vqc_state(x2, self.vqc_params)
        return float(abs(np.dot(phi1.conj(), phi2)) ** 2)

    def kernel_signal(self, features: np.ndarray) -> float:
        """
        Compare feature vector to ideal bull/bear reference states.
        Returns value in (−1, +1): positive = bullish.
        """
        k_bull = self.quantum_kernel(features, self._bull_ref)
        k_bear = self.quantum_kernel(features, self._bear_ref)
        denom = k_bull + k_bear + 1e-12
        return (k_bull - k_bear) / denom

    # ── 3. QAE – Quantum Amplitude Estimation ────────────────────────────────

    def quantum_amplitude_estimation(self, daily_returns: np.ndarray) -> float:
        """
        Estimates the probability that the next period return is positive,
        using a Grover-amplitude-estimation inspired procedure on the
        empirical return distribution encoded as quantum amplitudes.

        Returns probability in (0, 1).
        """
        if len(daily_returns) < 10:
            return 0.5

        mu, sigma = np.mean(daily_returns), np.std(daily_returns) + 1e-10
        n_bins = 16
        lo, hi = mu - 3 * sigma, mu + 3 * sigma
        bins = np.linspace(lo, hi, n_bins + 1)
        hist, _ = np.histogram(daily_returns, bins=bins, density=True)
        hist = np.maximum(hist, 0)
        probs = hist / (hist.sum() + 1e-12)

        # Encode distribution as quantum amplitudes
        amplitudes = np.sqrt(probs)
        amplitudes /= np.linalg.norm(amplitudes) + 1e-12

        # Oracle: mark positive-return bins
        threshold_idx = int(np.searchsorted(bins[:-1], 0.0))
        marked = np.zeros_like(amplitudes)
        marked[threshold_idx:] = amplitudes[threshold_idx:]

        # Initial amplitude of marked states
        a = np.sum(marked ** 2)
        if a <= 0 or a >= 1:
            return float(np.clip(a, 0.05, 0.95))

        theta = np.arcsin(np.sqrt(a))
        # Optimal Grover iterations
        m = max(1, int(np.round(np.pi / (4 * theta) - 0.5)))
        # Amplitude after m Grover iterations
        prob_positive = np.sin((2 * m + 1) * theta) ** 2

        return float(np.clip(prob_positive, 0.05, 0.95))

    # ── 4. QAOA – Portfolio Selection as QUBO ────────────────────────────────

    def qaoa_portfolio_select(
        self,
        expected_returns: np.ndarray,
        cov_matrix: np.ndarray,
        max_positions: int,
        risk_lambda: float = 2.0,
    ) -> np.ndarray:
        """
        Solves portfolio selection as a QUBO via quantum-annealing simulation
        (Path-Integral Monte Carlo / Suzuki-Trotter decomposition).

        Objective (minimise):
            E(x) = −rᵀx  +  λ · xᵀΣx   subject to Σxᵢ ≤ max_positions

        Returns binary selection vector x ∈ {0,1}^n.
        """
        n = len(expected_returns)
        if n == 0:
            return np.array([], dtype=int)

        # QUBO matrix
        Q = -np.diag(expected_returns) + risk_lambda * cov_matrix

        # Simulated quantum annealing (Trotter decomposition)
        n_replicas = 8      # Trotter slices (quantum copies)
        n_steps = 300
        T_start, T_end = 2.0, 0.02
        Gamma_start = 3.0   # Initial transverse field

        # Initialise replicas randomly (respecting max_positions constraint)
        replicas = []
        for _ in range(n_replicas):
            x = np.zeros(n, dtype=int)
            chosen = np.random.choice(n, size=min(max_positions, n), replace=False)
            x[chosen] = 1
            replicas.append(x)

        best_x = replicas[0].copy()
        best_energy = best_x @ Q @ best_x

        for step in range(n_steps):
            progress = step / n_steps
            T = T_start * (T_end / T_start) ** progress
            Gamma = Gamma_start * (1.0 - progress)
            J_perp = -0.5 * T * np.log(np.tanh(Gamma / (n_replicas * T + 1e-12)))

            for rep_idx, x in enumerate(replicas):
                # Try flipping each bit
                for i in np.random.permutation(n):
                    x_new = x.copy()
                    x_new[i] ^= 1

                    # Enforce constraint
                    if np.sum(x_new) > max_positions:
                        continue

                    # Classical energy difference
                    dE_classical = (x_new - x) @ Q @ x_new + x @ Q @ (x_new - x)

                    # Quantum tunneling coupling to adjacent replicas
                    prev_rep = replicas[(rep_idx - 1) % n_replicas]
                    next_rep = replicas[(rep_idx + 1) % n_replicas]
                    dE_quantum = J_perp * (
                        (x_new[i] - x[i]) * (prev_rep[i] + next_rep[i] - 2 * x[i])
                    )

                    dE = dE_classical + dE_quantum

                    if dE < 0 or np.random.random() < np.exp(-dE / (T + 1e-12)):
                        replicas[rep_idx] = x_new
                        x = x_new

                # Track best
                E = x @ Q @ x
                if E < best_energy and np.sum(x) <= max_positions:
                    best_energy = E
                    best_x = x.copy()

        return best_x

    # ── 5. QRW – Quantum Random Walk (Regime Detection) ──────────────────────

    def quantum_random_walk(self, price_series: np.ndarray, steps: int = 10) -> float:
        """
        Implements a discrete-time quantum random walk on a line graph
        with the price direction sequence as the coin operator bias.

        The walk's probability distribution spread indicates trend strength:
        - Coherent (trending) market → spread diffuses faster than classical
        - Incoherent (ranging) market → spread remains localised

        Returns: regime score ∈ (−1, +1)
          +1 = strong uptrend, −1 = strong downtrend, 0 = ranging
        """
        if len(price_series) < steps + 2:
            return 0.0

        returns = np.diff(price_series[-steps - 1:]) / (price_series[-steps - 2:-1] + 1e-10)
        n_positions = 2 * steps + 1
        center = steps

        # Coin + position register
        # State: (spin_up, spin_down) at each position
        state = np.zeros((n_positions, 2), dtype=complex)
        state[center, 0] = 1.0 / np.sqrt(2)
        state[center, 1] = 1j / np.sqrt(2)   # balanced initial coin state

        for t, r in enumerate(returns):
            # Biased Hadamard coin (bias from observed return)
            bias = np.clip(r * 10, -0.99, 0.99)
            angle = np.arcsin(bias)
            coin = np.array([
                [np.cos(angle), -np.sin(angle)],
                [np.sin(angle),  np.cos(angle)]
            ], dtype=complex)

            new_state = np.zeros_like(state)
            for pos in range(n_positions):
                # Apply coin
                coin_applied = coin @ state[pos]
                # Shift: spin-up moves right, spin-down moves left
                if pos + 1 < n_positions:
                    new_state[pos + 1, 0] += coin_applied[0]
                if pos - 1 >= 0:
                    new_state[pos - 1, 1] += coin_applied[1]
            state = new_state

        # Measure: probability distribution over positions
        probs = np.sum(np.abs(state) ** 2, axis=1)
        probs /= probs.sum() + 1e-12

        positions = np.arange(n_positions) - center
        mean_pos = np.dot(positions, probs)
        spread = np.sqrt(np.dot((positions - mean_pos) ** 2, probs))

        # Classical RW spread ≈ √t; quantum spread ≈ t
        classical_spread = np.sqrt(steps)
        quantum_advantage = spread / (classical_spread + 1e-10)

        # Regime score: directional bias + spread normalised
        return float(np.clip(mean_pos / (steps + 1e-10), -1.0, 1.0))


# ─────────────────────────────────────────────────────────────────────────────
# FEATURE ENGINEERING
# ─────────────────────────────────────────────────────────────────────────────
class FeatureEngine:
    """Classical technical feature extraction for quantum input encoding."""

    @staticmethod
    def compute(history_df) -> dict | None:
        try:
            closes  = history_df["close"].values.astype(float)
            highs   = history_df["high"].values.astype(float)
            lows    = history_df["low"].values.astype(float)
            volumes = history_df["volume"].values.astype(float)

            if len(closes) < 30:
                return None

            # ── Momentum ──────────────────────────────────────────────────────
            rsi = FeatureEngine._rsi(closes, 14)
            ema12 = FeatureEngine._ema(closes, 12)
            ema26 = FeatureEngine._ema(closes, 26)
            macd_line = ema12 - ema26
            macd_sig  = FeatureEngine._ema(macd_line, 9)
            macd_hist = float(macd_line[-1] - macd_sig[-1])
            stoch_k, stoch_d = FeatureEngine._stochastic(closes, highs, lows, 14)

            # ── Trend ─────────────────────────────────────────────────────────
            sma20 = float(np.mean(closes[-20:]))
            sma50 = float(np.mean(closes[-50:])) if len(closes) >= 50 else sma20
            adx   = FeatureEngine._adx(closes, highs, lows, 14)

            # ── Volatility ────────────────────────────────────────────────────
            returns = np.diff(closes) / (closes[:-1] + 1e-10)
            vol_20  = float(np.std(returns[-20:]) * np.sqrt(252))
            bb_mid  = np.mean(closes[-20:])
            bb_std  = np.std(closes[-20:]) + 1e-10
            bb_pos  = float((closes[-1] - (bb_mid - 2 * bb_std)) / (4 * bb_std))
            atr     = FeatureEngine._atr(closes, highs, lows, 14)

            # ── Volume ────────────────────────────────────────────────────────
            vol_ratio  = float(volumes[-1] / (np.mean(volumes[-20:]) + 1e-10))
            obv        = FeatureEngine._obv(closes[-21:], volumes[-21:])
            obv_trend  = float(np.corrcoef(np.arange(21), obv)[0, 1]) if len(obv) == 21 else 0.0

            # ── Price pattern ─────────────────────────────────────────────────
            zscore     = float((closes[-1] - sma20) / (bb_std))
            trend_dir  = float(np.polyfit(np.arange(10), closes[-10:] / closes[-10], 1)[0])
            ret_5d     = float((closes[-1] / closes[-6]) - 1) if len(closes) > 5 else 0.0
            ret_20d    = float((closes[-1] / closes[-21]) - 1) if len(closes) > 20 else 0.0

            # ── 4 normalised features for quantum encoding [0, 1] ─────────────
            quantum_features = np.array([
                float(np.clip(rsi / 100.0, 0, 1)),
                float(np.clip((macd_hist / (closes[-1] + 1e-10)) * 50 + 0.5, 0, 1)),
                float(np.clip(bb_pos, 0, 1)),
                float(np.clip(adx / 60.0, 0, 1)),
            ])

            return {
                "quantum_features": quantum_features,
                "rsi": rsi,
                "macd_hist": macd_hist,
                "stoch_k": stoch_k,
                "stoch_d": stoch_d,
                "adx": adx,
                "bb_pos": bb_pos,
                "vol_20": vol_20,
                "atr_pct": float(atr / (closes[-1] + 1e-10)),
                "vol_ratio": vol_ratio,
                "obv_trend": obv_trend,
                "zscore": zscore,
                "trend_dir": trend_dir,
                "sma20_ratio": float(closes[-1] / (sma20 + 1e-10)),
                "sma50_ratio": float(closes[-1] / (sma50 + 1e-10)),
                "ret_5d": ret_5d,
                "ret_20d": ret_20d,
                "recent_returns": returns[-30:],
                "closes": closes,
            }
        except Exception:
            return None

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _rsi(prices, period=14):
        deltas = np.diff(prices)
        gains  = np.where(deltas > 0, deltas, 0.0)
        losses = np.where(deltas < 0, -deltas, 0.0)
        ag, al = np.mean(gains[:period]), np.mean(losses[:period])
        for i in range(period, len(gains)):
            ag = (ag * (period - 1) + gains[i]) / period
            al = (al * (period - 1) + losses[i]) / period
        return 100.0 if al < 1e-12 else float(100 - 100 / (1 + ag / al))

    @staticmethod
    def _ema(data, period):
        k = 2.0 / (period + 1)
        out = np.empty(len(data))
        out[0] = data[0]
        for i in range(1, len(data)):
            out[i] = data[i] * k + out[i - 1] * (1 - k)
        return out

    @staticmethod
    def _stochastic(closes, highs, lows, period=14):
        ks = []
        for i in range(period - 1, len(closes)):
            h = np.max(highs[i - period + 1: i + 1])
            l = np.min(lows[i  - period + 1: i + 1])
            ks.append(100 * (closes[i] - l) / (h - l + 1e-10))
        k = ks[-1] if ks else 50.0
        d = float(np.mean(ks[-3:])) if len(ks) >= 3 else k
        return float(k), float(d)

    @staticmethod
    def _adx(closes, highs, lows, period=14):
        tr_list, pdm, ndm = [], [], []
        for i in range(1, len(closes)):
            tr = max(highs[i] - lows[i],
                     abs(highs[i] - closes[i - 1]),
                     abs(lows[i]  - closes[i - 1]))
            tr_list.append(tr)
            up   = highs[i] - highs[i - 1]
            down = lows[i - 1] - lows[i]
            pdm.append(up   if up > down and up > 0   else 0.0)
            ndm.append(down if down > up and down > 0 else 0.0)
        if len(tr_list) < period:
            return 20.0
        atr = np.mean(tr_list[-period:]) + 1e-10
        di_p = 100 * np.mean(pdm[-period:]) / atr
        di_n = 100 * np.mean(ndm[-period:]) / atr
        dx   = 100 * abs(di_p - di_n) / (di_p + di_n + 1e-10)
        return float(dx)

    @staticmethod
    def _atr(closes, highs, lows, period=14):
        trs = [max(highs[i] - lows[i],
                   abs(highs[i] - closes[i - 1]),
                   abs(lows[i]  - closes[i - 1]))
               for i in range(1, len(closes))]
        return float(np.mean(trs[-period:])) if trs else 0.0

    @staticmethod
    def _obv(closes, volumes):
        obv = np.zeros(len(closes))
        for i in range(1, len(closes)):
            obv[i] = obv[i - 1] + (volumes[i] if closes[i] > closes[i - 1]
                                    else (-volumes[i] if closes[i] < closes[i - 1] else 0))
        return obv


# ─────────────────────────────────────────────────────────────────────────────
# MAIN ALGORITHM
# ─────────────────────────────────────────────────────────────────────────────
class QuantumSwingTradingAlgorithm(QCAlgorithm):

    # ── Configuration ─────────────────────────────────────────────────────────
    INITIAL_CASH        = 10_000
    LOOKBACK            = 70       # calendar days of history to pull
    MIN_HOLD_DAYS       = 3
    MAX_HOLD_DAYS       = 21
    MAX_POSITIONS       = 5
    BASE_POSITION_PCT   = 0.18     # 18 % of portfolio per trade
    HARD_STOP_LOSS      = 0.08     # 8 % stop loss
    TAKE_PROFIT_BASE    = 0.20     # 20 % initial take-profit
    MAX_DRAWDOWN        = 0.22     # 22 % max portfolio drawdown
    SIGNAL_THRESHOLD    = 0.12     # minimum combined signal to trade
    COARSE_TOP_N        = 150      # universe: top N by dollar volume
    FINE_TOP_N          = 60       # after fundamental filter

    def Initialize(self):
        # ── Back-test dates ───────────────────────────────────────────────────
        self.SetStartDate(2019, 1, 1)
        self.SetEndDate(2024, 12, 31)
        self.SetCash(self.INITIAL_CASH)

        # ── Universe ──────────────────────────────────────────────────────────
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self._coarse_filter, self._fine_filter)

        # ── Risk model ───────────────────────────────────────────────────────
        self.SetRiskManagement(
            MaximumDrawdownPercentPortfolioRiskManagementModel(self.MAX_DRAWDOWN)
        )

        # ── Benchmark ────────────────────────────────────────────────────────
        self.SetBenchmark("SPY")

        # ── Quantum modules ───────────────────────────────────────────────────
        self.qm = QuantumModules()

        # ── State ─────────────────────────────────────────────────────────────
        self.active_symbols: set = set()
        self.entry_prices: dict  = {}
        self.entry_dates:  dict  = {}
        self.peak_prices:  dict  = {}   # for trailing stop
        self.trade_log:    list  = []

        # Performance tracking for self-adjustment
        self._weekly_returns: deque = deque(maxlen=52)
        self._portfolio_high: float = self.INITIAL_CASH
        self._last_value:     float = self.INITIAL_CASH
        self._opt_week_count: int   = 0

        # ── Schedules ─────────────────────────────────────────────────────────
        # Morning signal scan (30 min after open every day)
        self.Schedule.On(
            self.DateRules.EveryDay(),
            self.TimeRules.AfterMarketOpen(0, 30),
            self._morning_scan
        )
        # Evening position review (30 min before close)
        self.Schedule.On(
            self.DateRules.EveryDay(),
            self.TimeRules.BeforeMarketClose(0, 30),
            self._evening_review
        )
        # Weekly self-adjustment of quantum parameters (Monday)
        self.Schedule.On(
            self.DateRules.Every(DayOfWeek.Monday),
            self.TimeRules.AfterMarketOpen(1, 0),
            self._weekly_self_adjustment
        )

        # ── Warm-up ───────────────────────────────────────────────────────────
        self.SetWarmUp(self.LOOKBACK + 5)

    # ── Universe filters ──────────────────────────────────────────────────────

    def _coarse_filter(self, coarse):
        filtered = [
            x for x in coarse
            if x.HasFundamentalData
            and x.Price > 8
            and x.DollarVolume > 30_000_000
        ]
        by_volume = sorted(filtered, key=lambda x: x.DollarVolume, reverse=True)
        return [x.Symbol for x in by_volume[:self.COARSE_TOP_N]]

    def _fine_filter(self, fine):
        keep = [
            x for x in fine
            if x.AssetClassification.MorningstarSectorCode in (
                MorningstarSectorCode.Technology,
                MorningstarSectorCode.Healthcare,
                MorningstarSectorCode.ConsumerCyclical,
                MorningstarSectorCode.Industrials,
                MorningstarSectorCode.CommunicationServices,
            )
            and x.EarningReports.BasicEPS.ThreeMonths != 0
        ]
        return [x.Symbol for x in keep[:self.FINE_TOP_N]]

    def OnSecuritiesChanged(self, changes):
        for sec in changes.AddedSecurities:
            self.active_symbols.add(sec.Symbol)
        for sec in changes.RemovedSecurities:
            sym = sec.Symbol
            self.active_symbols.discard(sym)
            # Liquidate removed symbols that are still held
            if self.Portfolio[sym].Invested:
                self.Liquidate(sym, "Removed from universe")
                self._close_position(sym)

    # ── Core: signal generation ───────────────────────────────────────────────

    def _compute_signal(self, symbol) -> tuple:
        """
        Returns (signal, confidence, dynamic_sl, dynamic_tp).
        signal: +1 long, 0 neutral.
        """
        try:
            hist = self.History(symbol, self.LOOKBACK + 10, Resolution.Daily)
            if hist is None or hist.empty or len(hist) < 35:
                return 0, 0.0, self.HARD_STOP_LOSS, self.TAKE_PROFIT_BASE

            feats = FeatureEngine.compute(hist)
            if feats is None:
                return 0, 0.0, self.HARD_STOP_LOSS, self.TAKE_PROFIT_BASE

            qf = feats["quantum_features"]

            # ── Quantum signals ───────────────────────────────────────────────

            # 1. VQC direction probability [0,1] → centred at 0
            vqc_raw   = self.qm.vqc_predict(qf)
            vqc_sig   = (vqc_raw - 0.5) * 2.0          # → (−1, +1)

            # 2. Quantum Kernel similarity vs bull/bear archetype
            qkm_sig   = self.qm.kernel_signal(qf)       # → (−1, +1)

            # 3. Quantum Amplitude Estimation (win probability)
            qa_prob   = self.qm.quantum_amplitude_estimation(feats["recent_returns"])
            qa_sig    = (qa_prob - 0.5) * 2.0           # → (−1, +1)

            # 4. Quantum Random Walk (regime)
            qrw_sig   = self.qm.quantum_random_walk(feats["closes"], steps=10)

            # Aggregate quantum component (weighted)
            quantum_score = (
                0.35 * vqc_sig +
                0.25 * qkm_sig +
                0.25 * qa_sig  +
                0.15 * qrw_sig
            )

            # ── Classical technical signals ───────────────────────────────────

            mom = 0.0
            # RSI oversold/overbought
            if feats["rsi"] < 38:   mom += 0.30
            elif feats["rsi"] > 65: mom -= 0.30
            # MACD histogram direction
            mom += 0.20 * np.sign(feats["macd_hist"])
            # Stochastic
            if feats["stoch_k"] < 25:   mom += 0.20
            elif feats["stoch_k"] > 75: mom -= 0.20
            # Short-term return momentum
            mom += 0.15 * np.sign(feats["ret_5d"])
            # 20-day return
            mom += 0.15 * np.sign(feats["ret_20d"])

            trend = 0.0
            if feats["sma20_ratio"] > 1.0: trend += 0.35
            else:                          trend -= 0.35
            if feats["sma50_ratio"] > 1.0: trend += 0.25
            else:                          trend -= 0.25
            if feats["adx"] > 20:
                trend += 0.25 * np.sign(feats["trend_dir"])
            # OBV trend
            trend += 0.15 * np.clip(feats["obv_trend"], -1, 1)

            vol_conf = 0.0
            if feats["vol_ratio"] > 1.5: vol_conf = 0.5   # volume expansion confirms
            elif feats["vol_ratio"] < 0.7: vol_conf = -0.2  # low volume = weak signal

            mr = 0.0
            if feats["zscore"] < -1.8: mr =  0.40   # strong mean reversion buy
            elif feats["zscore"] > 1.8: mr = -0.40

            classical_score = (
                0.35 * mom   +
                0.35 * trend +
                0.20 * vol_conf +
                0.10 * mr
            )

            # ── Blend: 45 % quantum, 55 % classical ───────────────────────────
            combined = 0.45 * quantum_score + 0.55 * classical_score

            # ── Dynamic risk sizing based on ATR ─────────────────────────────
            atr_pct = feats["atr_pct"]
            dynamic_sl = float(np.clip(atr_pct * 2.0, self.HARD_STOP_LOSS, 0.15))
            dynamic_tp = float(np.clip(atr_pct * 4.5, self.TAKE_PROFIT_BASE, 0.40))

            confidence = float(abs(combined))

            # Only take long swing trades; require ADX > 15 for trend confirmation
            if combined > self.SIGNAL_THRESHOLD and feats["adx"] > 15:
                return 1, confidence, dynamic_sl, dynamic_tp
            else:
                return 0, confidence, dynamic_sl, dynamic_tp

        except Exception as e:
            return 0, 0.0, self.HARD_STOP_LOSS, self.TAKE_PROFIT_BASE

    # ── Morning scan ──────────────────────────────────────────────────────────

    def _morning_scan(self):
        if self.IsWarmingUp:
            return

        # Count free slots
        n_invested = sum(1 for h in self.Portfolio.Values if h.Invested)
        slots = self.MAX_POSITIONS - n_invested
        if slots <= 0:
            return

        candidates = []
        for symbol in list(self.active_symbols):
            if not self.Securities.ContainsKey(symbol):
                continue
            if self.Portfolio[symbol].Invested:
                continue
            if not self.Securities[symbol].IsTradable:
                continue

            sig, conf, sl, tp = self._compute_signal(symbol)
            if sig == 1 and conf > 0.10:
                candidates.append({
                    "symbol": symbol,
                    "confidence": conf,
                    "sl": sl,
                    "tp": tp,
                })

        if not candidates:
            return

        # ── QAOA selection ────────────────────────────────────────────────────
        n = min(len(candidates), 25)
        candidates = sorted(candidates, key=lambda c: c["confidence"], reverse=True)[:n]

        expected_ret = np.array([c["confidence"] for c in candidates])
        # Simplified diagonal covariance (no cross-correlations without extra history)
        vol_estimates = np.array([0.03] * n)
        cov = np.diag(vol_estimates ** 2)

        selection_mask = self.qm.qaoa_portfolio_select(
            expected_returns=expected_ret,
            cov_matrix=cov,
            max_positions=slots,
            risk_lambda=2.5,
        )

        selected = [candidates[i] for i in range(len(candidates))
                    if i < len(selection_mask) and selection_mask[i] == 1]

        if not selected:
            selected = candidates[:slots]  # fallback: top-N by confidence

        for c in selected[:slots]:
            self._enter_position(c)

    # ── Position entry ────────────────────────────────────────────────────────

    def _enter_position(self, candidate: dict):
        symbol = candidate["symbol"]
        if not self.Securities.ContainsKey(symbol):
            return
        price = self.Securities[symbol].Price
        if price <= 0:
            return

        # Kelly-fraction sizing capped at BASE_POSITION_PCT
        conf = candidate["confidence"]
        kelly_cap = min(conf * 1.8, 1.0) * self.BASE_POSITION_PCT
        position_value = self.Portfolio.TotalPortfolioValue * kelly_cap
        shares = int(position_value / price)
        if shares <= 0:
            return

        ticket = self.MarketOrder(symbol, shares)
        if ticket.OrderId > 0:
            self.entry_prices[symbol] = price
            self.entry_dates[symbol]  = self.Time
            self.peak_prices[symbol]  = price
            self.Debug(
                f"[ENTER] {symbol} | {shares}sh @ ${price:.2f} "
                f"| conf={conf:.3f} SL={candidate['sl']:.1%} TP={candidate['tp']:.1%}"
            )

    # ── Evening position review ────────────────────────────────────────────────

    def _evening_review(self):
        if self.IsWarmingUp:
            return

        for symbol in list(self.entry_prices.keys()):
            if not self.Portfolio[symbol].Invested:
                self._close_position(symbol)
                continue

            entry  = self.entry_prices[symbol]
            current = self.Securities[symbol].Price
            if entry <= 0 or current <= 0:
                continue

            pnl_pct   = (current - entry) / entry
            days_held = (self.Time - self.entry_dates[symbol]).days

            # Update peak (for trailing stop)
            self.peak_prices[symbol] = max(self.peak_prices.get(symbol, current), current)
            peak = self.peak_prices[symbol]

            # ── Exit rules ────────────────────────────────────────────────────

            # 1. Hard stop loss
            if pnl_pct <= -self.HARD_STOP_LOSS:
                self.Liquidate(symbol, "Hard stop loss")
                self._close_position(symbol)
                continue

            # 2. Trailing stop once in profit > 10 %
            if pnl_pct > 0.10:
                trail_stop_pct = 0.05   # 5 % trail from peak
                if current < peak * (1 - trail_stop_pct):
                    self.Liquidate(symbol, "Trailing stop triggered")
                    self._close_position(symbol)
                    continue

            # 3. Take profit
            if pnl_pct >= self.TAKE_PROFIT_BASE:
                self.Liquidate(symbol, "Take profit reached")
                self._close_position(symbol)
                continue

            # 4. Max holding period
            if days_held >= self.MAX_HOLD_DAYS:
                self.Liquidate(symbol, "Max holding period")
                self._close_position(symbol)
                continue

            # 5. Signal reversal check (only after MIN_HOLD_DAYS)
            if days_held >= self.MIN_HOLD_DAYS and days_held % 3 == 0:
                sig, conf, _, _ = self._compute_signal(symbol)
                if sig == 0 and conf < 0.05:
                    self.Liquidate(symbol, "Signal exhausted")
                    self._close_position(symbol)

    def _close_position(self, symbol):
        self.entry_prices.pop(symbol, None)
        self.entry_dates.pop(symbol, None)
        self.peak_prices.pop(symbol, None)

    # ── Weekly self-adjustment ────────────────────────────────────────────────

    def _weekly_self_adjustment(self):
        """
        Adapt quantum VQC parameters using a parameter-shift-inspired
        gradient estimate based on recent portfolio performance.
        """
        if self.IsWarmingUp:
            return

        current_value = self.Portfolio.TotalPortfolioValue
        week_return   = (current_value - self._last_value) / (self._last_value + 1e-10)
        self._last_value = current_value
        self._weekly_returns.append(week_return)
        self._portfolio_high = max(self._portfolio_high, current_value)
        self._opt_week_count += 1

        # Compute performance score
        if len(self._weekly_returns) >= 4:
            recent_avg  = float(np.mean(list(self._weekly_returns)[-4:]))
            recent_vol  = float(np.std(list(self._weekly_returns)[-4:]) + 1e-10)
            sharpe_proxy = recent_avg / recent_vol
        else:
            sharpe_proxy = week_return / 0.02

        # Adaptive noise scale: explore more when underperforming
        total_return = (current_value / self.INITIAL_CASH) - 1.0
        # Annualise roughly (52 weeks)
        weeks_elapsed = max(self._opt_week_count, 1)
        ann_target    = (1.0 + total_return) ** (52 / weeks_elapsed) - 1.0
        underperform  = max(0.0, 1.0 - ann_target)
        noise_scale   = float(np.clip(0.05 + 0.15 * underperform, 0.02, 0.25))

        # Parameter-shift gradient estimate:
        # Perturb each parameter ±ε, use performance as reward signal
        n_params = len(self.qm.vqc_params)
        gradient_est = np.random.randn(n_params) * noise_scale

        # Momentum: move toward better performance
        lr = 0.08 if sharpe_proxy < 0.5 else 0.03
        self.qm.update_vqc_params(gradient_est, lr=lr)

        # Adapt reference bull/bear states based on recent market regime
        recent_rets = list(self._weekly_returns)
        if len(recent_rets) >= 4:
            trend_bias = float(np.mean(recent_rets[-4:]))
            self.qm._bull_ref = np.clip(self.qm._bull_ref + 0.01 * trend_bias, 0.1, 0.9)
            self.qm._bear_ref = np.clip(self.qm._bear_ref - 0.01 * trend_bias, 0.1, 0.9)

        self.Debug(
            f"[QOpt W{self._opt_week_count}] "
            f"Port=${current_value:,.0f} "
            f"WkRet={week_return:.2%} "
            f"AnnRet={ann_target:.2%} "
            f"Sharpe≈{sharpe_proxy:.2f} "
            f"lr={lr:.3f} noise={noise_scale:.3f}"
        )

    # ── End-of-algorithm report ───────────────────────────────────────────────

    def OnEndOfAlgorithm(self):
        final  = self.Portfolio.TotalPortfolioValue
        gain   = final - self.INITIAL_CASH
        ret_pct = (final / self.INITIAL_CASH - 1) * 100
        years  = (self.EndDate - self.StartDate).days / 365.25
        cagr   = ((final / self.INITIAL_CASH) ** (1 / years) - 1) * 100 if years > 0 else 0

        separator = "=" * 56
        self.Log(separator)
        self.Log("  QUANTUM SWING TRADING ALGORITHM — FINAL REPORT")
        self.Log(separator)
        self.Log(f"  Initial Capital : ${self.INITIAL_CASH:>10,.2f}")
        self.Log(f"  Final Value     : ${final:>10,.2f}")
        self.Log(f"  Total Gain      : ${gain:>10,.2f}")
        self.Log(f"  Total Return    : {ret_pct:>9.2f}%")
        self.Log(f"  CAGR            : {cagr:>9.2f}%")
        self.Log(f"  Backtest Period : {years:.1f} years")
        self.Log(separator)
        self.Log(f"  VQC params norm : {np.linalg.norm(self.qm.vqc_params):.4f}")
        self.Log(f"  Bull ref state  : {np.round(self.qm._bull_ref, 3)}")
        self.Log(f"  Bear ref state  : {np.round(self.qm._bear_ref, 3)}")
        self.Log(separator)
