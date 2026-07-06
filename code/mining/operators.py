"""Factor operator set for alpha mining (Step 2).

All operators work on *wide* frames: index = trade_date (ascending),
columns = ts_code, values = float. Time-series operators roll down the
date axis per stock; cross-section operators work across stocks per date.

Conventions
-----------
- No lookahead: every op uses only rows <= t.
- NaN-safe: NaN stays NaN (no fillna(0) — the original Factor_Operator.py
  filled 0s, which poisons cross-sectional ranks; we deliberately don't).
- Rolling pandas ops use min_periods = ceil(0.75*n) to tolerate short
  suspensions; shift-based weighted ops (decay/slope/wma) need full windows.

Families (per the mining prompt's operator table, extending
Factor_Operator.py):
  Calculation    Log, Sign, SignedPower, Abs, Sqrt
  Time-Series    TsMean, TsStd, TsSkew, TsKurt, TsMed, TsRank, TsMax,
                 TsMin, TsSum, TsZscore, HighDay, LowDay, TsCount
  Cross-Section  CsRank, CsZscore, CsScale, CsDemean, CsWinsor,
                 CsIndNeutralize
  Difference     Delta, PctChange, Delay
  Correlation    TsCorr, TsCov
  Smooth         SMA, EMA, WMA, DecayLinear
  Regression     TsSlope, TsRSquare, TsResi, RegBeta, RegResi
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd


def _mp(n: int) -> int:
    """Default min_periods: tolerate up to ~25% missing rows in a window."""
    return max(2, math.ceil(0.75 * n))


# ---------------------------------------------------------------- calculation

def Log(A):
    """Natural log; non-positive values -> NaN (not -inf)."""
    with np.errstate(divide="ignore", invalid="ignore"):
        out = np.log(A.where(A > 0))
    return out


def Sign(A):
    return np.sign(A)


def Abs(A):
    return A.abs()


def Sqrt(A):
    return np.sqrt(A.where(A >= 0))


def SignedPower(A, a):
    """sign(A) * |A|^a — compresses/expands magnitudes, keeps direction."""
    return np.sign(A) * A.abs().pow(a)


# ---------------------------------------------------------------- time-series

def TsMean(A, n):
    return A.rolling(n, min_periods=_mp(n)).mean()


def TsStd(A, n):
    return A.rolling(n, min_periods=_mp(n)).std()


def TsSkew(A, n):
    return A.rolling(n, min_periods=max(3, _mp(n))).skew()


def TsKurt(A, n):
    return A.rolling(n, min_periods=max(4, _mp(n))).kurt()


def TsMed(A, n):
    return A.rolling(n, min_periods=_mp(n)).median()


def TsRank(A, n):
    """Rank of today's value within the trailing n rows, scaled to (0, 1]."""
    r = A.rolling(n, min_periods=_mp(n)).rank()
    cnt = A.rolling(n, min_periods=_mp(n)).count()
    return r / cnt


def TsMax(A, n):
    return A.rolling(n, min_periods=_mp(n)).max()


def TsMin(A, n):
    return A.rolling(n, min_periods=_mp(n)).min()


def TsSum(A, n):
    return A.rolling(n, min_periods=_mp(n)).sum()


def TsZscore(A, n):
    m = TsMean(A, n)
    s = TsStd(A, n)
    return (A - m) / s.where(s > 1e-12)


def TsCount(cond, n):
    """Count of True in trailing n rows. `cond` is a boolean wide frame."""
    return cond.astype(float).rolling(n, min_periods=_mp(n)).sum()


def _rolling_arg(A: pd.DataFrame, n: int, take_max: bool) -> pd.DataFrame:
    """Days since the window max (HighDay) or min (LowDay), chunked numpy."""
    vals = A.to_numpy(dtype=float)
    T, N = vals.shape
    out = np.full((T, N), np.nan)
    if T >= n:
        fn = np.nanargmax if take_max else np.nanargmin
        chunk = max(1, int(2e7 // (T * n)))  # keep window views ~160MB
        for c0 in range(0, N, chunk):
            sub = vals[:, c0:c0 + chunk]
            win = np.lib.stride_tricks.sliding_window_view(sub, n, axis=0)
            allnan = np.isnan(win).all(axis=2)
            safe = np.where(allnan[..., None], -np.inf if take_max else np.inf, win)
            with np.errstate(invalid="ignore"):
                idx = fn(safe, axis=2).astype(float)
            idx[allnan] = np.nan
            out[n - 1:, c0:c0 + chunk] = (n - 1) - idx
    return pd.DataFrame(out, index=A.index, columns=A.columns)


def HighDay(A, n):
    """Days since the trailing-n-window maximum (0 = today)."""
    return _rolling_arg(A, n, take_max=True)


def LowDay(A, n):
    """Days since the trailing-n-window minimum (0 = today)."""
    return _rolling_arg(A, n, take_max=False)


# ---------------------------------------------------------------- difference

def Delay(A, n):
    return A.shift(n)


def Delta(A, n=1):
    return A - A.shift(n)


def PctChange(A, n=1):
    prev = A.shift(n)
    return (A - prev) / prev.abs().where(prev.abs() > 1e-12)


# ---------------------------------------------------------------- correlation

def TsCorr(A, B, n):
    return A.rolling(n, min_periods=_mp(n)).corr(B)


def TsCov(A, B, n):
    return A.rolling(n, min_periods=_mp(n)).cov(B)


# ---------------------------------------------------------------- smooth

def SMA(A, n, m):
    """China-style SMA: Y_t = (A_t*m + Y_{t-1}*(n-m))/n == EWM(alpha=m/n)."""
    return A.ewm(alpha=m / n, adjust=False, ignore_na=True).mean()


def EMA(A, n):
    return A.ewm(span=n, adjust=False, ignore_na=True).mean()


def _weighted_shift_sum(A: pd.DataFrame, weights: np.ndarray) -> pd.DataFrame:
    """sum_j w_j * A.shift(j); NaN if any window element is NaN."""
    out = None
    for j, w in enumerate(weights):
        term = A.shift(j) * w
        out = term if out is None else out + term
    return out


def WMA(A, n):
    """Weights 0.9^i, i = distance from today (i=0 today), normalized."""
    w = np.array([0.9 ** i for i in range(n)], dtype=float)
    w /= w.sum()
    return _weighted_shift_sum(A, w)


def DecayLinear(A, d):
    """Linearly decaying weights d, d-1, ..., 1 (today heaviest)."""
    w = np.arange(d, 0, -1, dtype=float)
    w /= w.sum()
    return _weighted_shift_sum(A, w)


# ---------------------------------------------------------------- regression

def TsSlope(A, n):
    """OLS slope of A on time trend t = 1..n over trailing window."""
    tbar = (n + 1) / 2.0
    denom = n * (n * n - 1) / 12.0
    # shift j corresponds to t = n - j
    w = np.array([((n - j) - tbar) / denom for j in range(n)])
    return _weighted_shift_sum(A, w)


def TsRSquare(A, n):
    """R^2 of A on time trend over trailing window: corr(A, t)^2."""
    slope = TsSlope(A, n)
    std_a = A.rolling(n, min_periods=n).std()
    std_t = math.sqrt(n * (n + 1) / 12.0)
    corr = slope * std_t / std_a.where(std_a > 1e-12)
    return (corr ** 2).clip(upper=1.0)


def TsResi(A, n):
    """Endpoint residual of A regressed on time trend over trailing window."""
    slope = TsSlope(A, n)
    mean_a = A.rolling(n, min_periods=n).mean()
    return A - (mean_a + slope * (n - (n + 1) / 2.0))


def RegBeta(A, B, n):
    """Rolling OLS beta of A on B."""
    cov = A.rolling(n, min_periods=_mp(n)).cov(B)
    var = B.rolling(n, min_periods=_mp(n)).var()
    return cov / var.where(var > 1e-12)


def RegResi(A, B, n):
    """Endpoint residual of rolling OLS of A on B."""
    beta = RegBeta(A, B, n)
    alpha = TsMean(A, n) - beta * TsMean(B, n)
    return A - (alpha + beta * B)


# ---------------------------------------------------------------- cross-section

def CsRank(A):
    """Cross-sectional percentile rank in (0, 1] per date."""
    return A.rank(axis=1, pct=True)


def CsZscore(A):
    m = A.mean(axis=1)
    s = A.std(axis=1).replace(0, np.nan)
    return A.sub(m, axis=0).div(s, axis=0)


def CsDemean(A):
    return A.sub(A.mean(axis=1), axis=0)


def CsScale(A, a=1.0):
    """Scale so sum(|A|) = a per date."""
    denom = A.abs().sum(axis=1).replace(0, np.nan)
    return A.div(denom, axis=0) * a


def CsWinsor(A, k=5.0):
    """Clip per date to median +- k * MAD (robust winsorization)."""
    med = A.median(axis=1)
    mad = (A.sub(med, axis=0)).abs().median(axis=1).replace(0, np.nan)
    lo = med - k * mad
    hi = med + k * mad
    return A.clip(lower=lo, upper=hi, axis=0)


def CsIndNeutralize(A: pd.DataFrame, industry: pd.DataFrame) -> pd.DataFrame:
    """Demean A within industry groups per date.

    `industry` is a wide frame of integer industry codes aligned with A
    (NaN/-1 where unknown; those cells are demeaned against the global mean).
    """
    vals = A.to_numpy(dtype=float)
    codes = industry.reindex(index=A.index, columns=A.columns).to_numpy()
    codes = np.where(np.isnan(codes), -1, codes).astype(int)
    ngroups = int(codes.max()) + 1
    out = np.full_like(vals, np.nan)
    for i in range(vals.shape[0]):
        row = vals[i]
        grp = codes[i]
        ok = ~np.isnan(row)
        if not ok.any():
            continue
        res = row.copy()
        gok = ok & (grp >= 0)
        if gok.any() and ngroups > 0:
            sums = np.bincount(grp[gok], weights=row[gok], minlength=ngroups)
            cnts = np.bincount(grp[gok], minlength=ngroups)
            means = np.divide(sums, cnts, out=np.zeros_like(sums), where=cnts > 0)
            res[gok] = row[gok] - means[grp[gok]]
        rest = ok & (grp < 0)
        if rest.any():
            res[rest] = row[rest] - np.nanmean(row[ok])
        out[i] = np.where(ok, res, np.nan)
    return pd.DataFrame(out, index=A.index, columns=A.columns)


# Registry of every public operator, for expression sandboxing.
OPERATORS = {
    name: fn
    for name, fn in list(globals().items())
    if callable(fn) and not name.startswith("_") and name[0].isupper()
}
