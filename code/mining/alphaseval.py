"""AlphasEval: factor evaluation on the wide-frame panel.

Implements the practical metrics the 4-stage pipeline gates on (daily rank
IC / ICIR, quantile long-short spread, turnover, decay profile, coverage)
plus the AlphaEval-paper dimensions (arXiv 2508.13174), reimplemented
natively for our tushare parquet panel instead of Qlib:

  PPS  = 0.5*IC + 0.5*RankIC          (predictive power)
  RRE  = mean 1/(1+KL(rank_t || rank_{t-1}))   (temporal stability)
  PFS  = min(rankcorr under Gaussian noise, under t(3) noise)  (robustness)
  DH   = eigen-entropy of the accepted-set covariance (diversity, set level)
  Logic score is supplied by the mining agent (LLM) per candidate.

All functions take wide frames (index trade_date str YYYYMMDD, columns
ts_code) and a boolean mask of evaluable (stock, date) cells.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

MIN_NAMES = 50  # minimum cross-section size for a date to count


# ------------------------------------------------------------------ helpers

def _row_corr(X: pd.DataFrame, Y: pd.DataFrame) -> pd.Series:
    """Row-wise Pearson correlation of two aligned wide frames."""
    valid = X.notna() & Y.notna()
    Xv = X.where(valid)
    Yv = Y.where(valid)
    n = valid.sum(axis=1)
    mx = Xv.mean(axis=1)
    my = Yv.mean(axis=1)
    xc = Xv.sub(mx, axis=0)
    yc = Yv.sub(my, axis=0)
    cov = (xc * yc).sum(axis=1)
    sx = (xc ** 2).sum(axis=1).pow(0.5)
    sy = (yc ** 2).sum(axis=1).pow(0.5)
    corr = cov / (sx * sy).replace(0, np.nan)
    return corr.where(n >= MIN_NAMES)


def _masked(F: pd.DataFrame, mask: pd.DataFrame) -> pd.DataFrame:
    return F.where(mask.reindex(index=F.index, columns=F.columns).fillna(False))


def slice_dates(F: pd.DataFrame, start: str, end: str) -> pd.DataFrame:
    idx = F.index
    return F.loc[(idx >= start) & (idx <= end)]


# ------------------------------------------------------------------ IC

def daily_ic(factor, label, mask, method="rank") -> pd.Series:
    F = _masked(factor, mask)
    L = _masked(label, mask)
    if method == "rank":
        F = F.rank(axis=1)
        L = L.rank(axis=1)
    return _row_corr(F, L)


def ic_stats(ic: pd.Series) -> dict:
    ic = ic.dropna()
    if len(ic) < 20:
        return {"ic_mean": np.nan, "ic_std": np.nan, "icir": np.nan,
                "t_stat": np.nan, "n_days": len(ic), "pos_rate": np.nan}
    mean = ic.mean()
    std = ic.std()
    icir = mean / std if std > 0 else np.nan
    return {
        "ic_mean": float(mean),
        "ic_std": float(std),
        "icir": float(icir),
        "t_stat": float(icir * np.sqrt(len(ic))),
        "n_days": int(len(ic)),
        "pos_rate": float((ic > 0).mean()),
    }


def pps(factor, label, mask) -> float:
    """AlphaEval predictive power score: 0.5*PearsonIC + 0.5*RankIC."""
    ic_p = daily_ic(factor, label, mask, method="pearson").mean()
    ic_r = daily_ic(factor, label, mask, method="rank").mean()
    return float(0.5 * ic_p + 0.5 * ic_r)


# ------------------------------------------------------------------ portfolio

def quantile_returns(factor, label, mask, q=10, step=10) -> dict:
    """Mean forward return per factor decile on every `step`-th date
    (pseudo non-overlapping for a `step`-day horizon), plus L/S spread."""
    F = _masked(factor, mask)
    L = _masked(label, mask)
    dates = F.index[::step]
    buckets = np.full((len(dates), q), np.nan)
    for i, d in enumerate(dates):
        f = F.loc[d]
        l = L.loc[d]
        ok = f.notna() & l.notna()
        if ok.sum() < MIN_NAMES:
            continue
        ranks = f[ok].rank(pct=True)
        grp = np.minimum((ranks * q).astype(int), q - 1)
        buckets[i] = l[ok].groupby(grp).mean().reindex(range(q)).values
    mean_q = np.nanmean(buckets, axis=0)
    spread = buckets[:, q - 1] - buckets[:, 0]
    spread = spread[~np.isnan(spread)]
    return {
        "quantile_means": [float(x) for x in mean_q],
        "ls_mean": float(np.mean(spread)) if len(spread) else np.nan,
        "ls_tstat": float(np.mean(spread) / np.std(spread, ddof=1)
                          * np.sqrt(len(spread))) if len(spread) > 5 else np.nan,
        "monotonicity": float(pd.Series(mean_q).corr(
            pd.Series(range(q)), method="spearman")),
    }


def turnover(factor, mask, horizon=10) -> dict:
    """Rank autocorrelation at 1d and at the rebalance horizon."""
    F = _masked(factor, mask).rank(axis=1)
    ac1 = _row_corr(F, F.shift(1)).mean()
    ach = _row_corr(F, F.shift(horizon)).mean()
    return {"rank_ac_1d": float(ac1), f"rank_ac_{horizon}d": float(ach)}


def cost_aware(factor, label, mask, horizon=10, q=10, cost_bps=(15, 30),
               min_names=200) -> dict:
    """Cost-aware scoring: top-decile long-excess and long-short returns net
    of trading costs, using the factor's OWN decile-membership turnover.

    `factor` must be oriented (higher value = predicted higher return). On
    each rebalance the top/bottom decile is formed; turnover is the fraction
    of decile names replaced vs the previous rebalance; the per-period cost
    drag is turnover x 2 (round-trip) x cost, subtracted before annualizing.

    A-share short legs are effectively untradable, so `long_excess_net_*` is
    the headline tradable number; LS-net is reported for completeness.
    """
    F = _masked(factor, mask)
    L = _masked(label, mask)
    dates = F.index[::horizon]
    ppy = 250 / horizon
    longx, ls, to_l, to_s = [], [], [], []
    prev_top, prev_bot = None, None
    for d in dates:
        f = F.loc[d]; l = L.loc[d]
        ok = f.notna() & l.notna()
        if ok.sum() < min_names:
            continue
        rk = f[ok].rank(pct=True)
        top = set(rk.index[rk > 1 - 1.0 / q])
        bot = set(rk.index[rk <= 1.0 / q])
        uni = l[ok].mean()
        longx.append(float(l[list(top)].mean()) - uni)
        ls.append(float(l[list(top)].mean()) - float(l[list(bot)].mean()))
        to_l.append(1.0 if prev_top is None
                    else 1 - len(top & prev_top) / max(len(top), 1))
        to_s.append(1.0 if prev_bot is None
                    else 1 - len(bot & prev_bot) / max(len(bot), 1))
        prev_top, prev_bot = top, bot
    if len(longx) < 8:
        base = {"long_excess_gross_ann": np.nan, "ls_gross_ann": np.nan,
                "turnover_long": np.nan, "turnover_short": np.nan}
        for bp in cost_bps:
            base[f"long_excess_net_{int(bp)}bp_ann"] = np.nan
            base[f"ls_net_{int(bp)}bp_ann"] = np.nan
        return base
    longx = np.array(longx); ls = np.array(ls)
    to_l = np.array(to_l); to_s = np.array(to_s)
    ann = lambda a: float((1 + a).prod() ** (ppy / len(a)) - 1)
    out = {"long_excess_gross_ann": ann(longx), "ls_gross_ann": ann(ls),
           "turnover_long": float(to_l.mean()),
           "turnover_short": float(to_s.mean())}
    for bp in cost_bps:
        c = bp / 1e4
        out[f"long_excess_net_{int(bp)}bp_ann"] = ann(longx - to_l * 2 * c)
        out[f"ls_net_{int(bp)}bp_ann"] = ann(ls - (to_l + to_s) * 2 * c)
    return out


def decay_profile(factor, panel, mask, horizons=(1, 5, 10, 20)) -> dict:
    return {
        f"ic_{h}d": float(daily_ic(factor, panel.label(h), mask).mean())
        for h in horizons
    }


def coverage(factor, mask) -> float:
    """Share of evaluable (stock, date) cells where the factor has a value."""
    m = mask.reindex(index=factor.index, columns=factor.columns).fillna(False)
    tot = int(m.values.sum())
    return float((factor.notna() & m).values.sum() / tot) if tot else np.nan


# ------------------------------------------------------------------ AlphaEval dims

def rre(factor, mask) -> float:
    """Relative rank entropy: consistency of consecutive-day rankings."""
    F = _masked(factor, mask)
    valid = F.notna() & F.shift(1).notna()
    Fc = F.where(valid)
    Fp = F.shift(1).where(valid)
    r = Fc.rank(axis=1)
    rp = Fp.rank(axis=1)
    p = r.div(r.sum(axis=1), axis=0)
    q = rp.div(rp.sum(axis=1), axis=0)
    eps = 1e-8
    kl = (p * np.log((p + eps) / (q + eps))).sum(axis=1)
    kl = kl.where(valid.sum(axis=1) >= MIN_NAMES).dropna()
    return float((1.0 / (1.0 + kl)).mean()) if len(kl) else np.nan


def noise_variance(panel, start="20170101", end="20211231") -> float:
    """AlphaEval noise calibration: variance of min-max-normalized bench close
    over the training window."""
    b = panel.wide("bench_close").iloc[:, 0]
    b = slice_dates(b.to_frame(), start, end).iloc[:, 0].dropna()
    b = (b - b.min()) / (b.max() - b.min())
    return float(b.var(ddof=1))


def pfs(factor, mask, var: float, seed=7) -> dict:
    """Perturbation fidelity: rank corr of factor vs multiplicatively noised
    factor, Gaussian and Student-t(3); PFS = min of the two."""
    F = _masked(factor, mask)
    rng = np.random.default_rng(seed)
    sigma = np.sqrt(var)
    g = rng.normal(0, sigma, size=F.shape)
    t_raw = rng.standard_t(3, size=F.shape)
    t = t_raw * sigma * np.sqrt((3 - 2) / 3)
    Fg = F * (1.0 + g)
    Ft = F * (1.0 + t)
    pfs_g = _row_corr(F.rank(axis=1), Fg.rank(axis=1)).mean()
    pfs_t = _row_corr(F.rank(axis=1), Ft.rank(axis=1)).mean()
    return {"pfs_gaussian": float(pfs_g), "pfs_t": float(pfs_t),
            "pfs": float(min(pfs_g, pfs_t))}


def factor_corr(A, B, mask, step=5) -> float:
    """Mean cross-sectional Spearman correlation between two factors,
    sampled every `step` days."""
    Fa = _masked(A, mask).iloc[::step].rank(axis=1)
    Fb = _masked(B, mask).iloc[::step].rank(axis=1)
    return float(_row_corr(Fa, Fb).mean())


def diversity_entropy(factors: list[pd.DataFrame], mask, step=10) -> float:
    """Eigen-entropy of the covariance of per-date z-scored factor values
    (AlphaEval DH), sampled every `step` days. 1.0 = fully diverse."""
    if len(factors) < 2:
        return np.nan
    cols = []
    for F in factors:
        Fm = _masked(F, mask).iloc[::step]
        m = Fm.mean(axis=1)
        s = Fm.std(axis=1).replace(0, np.nan)
        z = Fm.sub(m, axis=0).div(s, axis=0)
        cols.append(z.values.ravel())
    mat = np.column_stack(cols)
    ok = ~np.isnan(mat).any(axis=1)
    mat = mat[ok]
    if mat.shape[0] < 100:
        return np.nan
    C = np.cov(mat, rowvar=False)
    eigs = np.clip(np.linalg.eigvalsh(C), 0, None)
    tot = eigs.sum()
    if tot <= 0:
        return np.nan
    p = eigs / tot
    p = p[p > 0]
    return float(-(p * np.log(p)).sum() / np.log(len(factors)))


# ------------------------------------------------------------------ full report

def evaluate_window(factor, panel, mask, horizon, start, end,
                    noise_var=None) -> dict:
    """All single-factor metrics restricted to [start, end]."""
    F = slice_dates(factor, start, end)
    m = slice_dates(mask, start, end)
    label = slice_dates(panel.label(horizon), start, end)
    ic = daily_ic(F, label, m)
    out = ic_stats(ic)
    out["pearson_ic"] = float(daily_ic(F, label, m, method="pearson").mean())
    out["pps"] = 0.5 * out["pearson_ic"] + 0.5 * out["ic_mean"] \
        if np.isfinite(out["ic_mean"]) else np.nan
    out.update(quantile_returns(F, label, m, step=horizon))
    out.update(turnover(F, m, horizon))
    # cost-aware: orient by IC sign so the top decile is the predicted-high leg
    sgn = np.sign(out["ic_mean"]) if np.isfinite(out["ic_mean"]) else 1.0
    out.update(cost_aware(F * sgn, label, m, horizon))
    out["coverage"] = coverage(F, m)
    if noise_var is not None:
        out["rre"] = rre(F, m)
        out.update(pfs(F, m, noise_var))
    return out


def rolling_ic_consistency(ic: pd.Series, window: int, step: int) -> dict:
    """Sign consistency of mean IC over rolling windows of the daily
    (oriented) IC series. Returns rate of positive windows, median and
    min window IC, and window count."""
    ic = ic.dropna()
    means = []
    for start in range(0, max(1, len(ic) - window + 1), step):
        w = ic.iloc[start:start + window]
        if len(w) >= window // 2:
            means.append(float(w.mean()))
    if not means:
        return {"n_windows": 0, "sign_rate": np.nan,
                "median_window_ic": np.nan, "min_window_ic": np.nan}
    means = np.array(means)
    return {
        "n_windows": int(len(means)),
        "sign_rate": float((means > 0).mean()),
        "median_window_ic": float(np.median(means)),
        "min_window_ic": float(means.min()),
    }


def block_bootstrap_pvalue(ic: pd.Series, n_boot: int, block: int,
                           seed: int) -> dict:
    """Moving-block bootstrap of the mean of the (oriented) daily IC
    series. One-sided test of H0: mean <= 0. Block length should match
    the label horizon to preserve overlap autocorrelation."""
    x = ic.dropna().to_numpy()
    n = len(x)
    if n < 5 * block:
        return {"p_value": np.nan, "ci5": np.nan, "ci95": np.nan,
                "boot_mean": np.nan, "n_obs": int(n)}
    rng = np.random.default_rng(seed)
    n_blocks = int(np.ceil(n / block))
    starts = rng.integers(0, n - block + 1, size=(n_boot, n_blocks))
    idx = (starts[:, :, None] + np.arange(block)[None, None, :])
    samples = x[idx.reshape(n_boot, -1)[:, :n]]
    means = samples.mean(axis=1)
    return {
        "p_value": float((means <= 0).mean()),
        "ci5": float(np.percentile(means, 5)),
        "ci95": float(np.percentile(means, 95)),
        "boot_mean": float(means.mean()),
        "n_obs": int(n),
    }


def yearly_ic(factor, panel, mask, horizon) -> dict:
    label = panel.label(horizon)
    ic = daily_ic(factor, label, mask)
    years = ic.index.str[:4]
    return {y: float(v) for y, v in ic.groupby(years).mean().items()
            if np.isfinite(v)}  # drop years with no evaluable dates
