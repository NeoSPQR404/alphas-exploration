"""Portfolio-construction layer: the single source of truth for how factor
values are turned into a deployable signal.

Three primitives, shared by the gates (pipeline.py), the composite backtest
(backtest_composite.py), and the neutralization eval (neutralize_eval.py):

- ``neutralize``        per-date residual of a signal on [SW-L1 industry,
                        log circ_mv] (Barra-lite). Removes the size/industry
                        style bet that drove the 2026 drawdown (see
                        results/mining/NEUTRALIZE_REPORT.md).
- ``oriented_composite``EW mean of oriented per-date pct ranks.
- ``investable_mask``   status filter (drop ST + names listed < N days),
                        optionally the smallest ``size_drop`` by circ_mv.
                        Default is *status only* — the blunt micro-cap cut
                        was shown to subtract signal without fixing the
                        regime risk, so it is opt-in, not the default.

The neutralization finding: size+industry neutralization halved the 2026
long-short loss at zero historical cost, so it is the recommended default
construction. ``config.GATE_ON_NEUTRALIZED`` routes the S1/S4 gates through
the neutralized signal so future rounds are judged on residual alpha.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import alphaseval as ae
from . import config as cfg


# ------------------------------------------------------------ style inputs
# Cached per Panel instance (log-size and industry are reused across every
# candidate in a round); keyed by id() so a fresh Panel invalidates them.
_STYLE_CACHE: dict[int, dict] = {}


def _style(panel) -> dict:
    key = id(panel)
    if key not in _STYLE_CACHE:
        size = panel.wide("CMV").astype(float)
        _STYLE_CACHE[key] = {
            "size_log": np.log(size.where(size > 0)),
            "size_rank": size.rank(axis=1, pct=True),
            "industry": panel.wide("INDUSTRY"),
        }
    return _STYLE_CACHE[key]


# ------------------------------------------------------------ neutralization

def neutralize(sig: pd.DataFrame, size_log: pd.DataFrame,
               ind_codes: pd.DataFrame, univ: pd.DataFrame) -> pd.DataFrame:
    """Per-date residual of ``sig`` on [industry dummies, log size], within
    the ``univ`` mask. Sequential: industry-demean, then regress out size.

    Dates with < 50 valid names are left NaN (matches the gate's MIN_NAMES).
    """
    S = sig.where(univ)
    Z = size_log.where(univ)
    sv = S.to_numpy(); zv = Z.to_numpy(); iv = ind_codes.to_numpy()
    out = np.full_like(sv, np.nan)
    for t in range(sv.shape[0]):
        row, z, ic = sv[t], zv[t], iv[t]
        ok = ~np.isnan(row) & ~np.isnan(z) & ~np.isnan(ic)
        if ok.sum() < 50:
            continue
        r = row.copy()
        g = ic[ok].astype(int)
        # industry demean
        ng = int(g.max()) + 1
        gsum = np.bincount(g, weights=r[ok], minlength=ng)
        gcnt = np.bincount(g, minlength=ng)
        gmean = np.divide(gsum, gcnt, out=np.zeros_like(gsum), where=gcnt > 0)
        r[ok] = r[ok] - gmean[g]
        # regress out size (centered)
        zz = z[ok]; zz = (zz - zz.mean())
        denom = (zz * zz).sum()
        if denom > 0:
            beta = (r[ok] * zz).sum() / denom
            r[ok] = r[ok] - beta * zz
        out[t] = np.where(ok, r, np.nan)
    return pd.DataFrame(out, index=sig.index, columns=sig.columns)


def neutralize_factor(factor: pd.DataFrame, panel,
                      mask: pd.DataFrame | None = None) -> pd.DataFrame:
    """Convenience wrapper: neutralize a single factor against the panel's
    style (log size + SW-L1 industry) over ``mask`` (default: full-A
    tradable). Used by the gates when ``config.GATE_ON_NEUTRALIZED``."""
    if mask is None:
        mask = panel.universe_mask("all")
    st = _style(panel)
    return neutralize(factor, st["size_log"], st["industry"], mask)


# ------------------------------------------------------------ composite

def oriented_composite(oriented_frames, mask: pd.DataFrame,
                       weights=None) -> pd.DataFrame:
    """(Weighted) mean of per-date pct ranks of already-oriented factor frames.

    ``oriented_frames`` is any iterable of wide frames already multiplied by
    their stored direction (so higher rank = predicted higher return).
    ``weights`` (if given) must align 1:1 with the frames; None = equal weight.
    """
    pairs = ((F, 1.0) for F in oriented_frames) if weights is None \
        else zip(oriented_frames, weights)
    rank_sum, wsum = None, 0.0
    for F, w in pairs:
        r = ae._masked(F, mask).rank(axis=1, pct=True) * w
        rank_sum = r if rank_sum is None else rank_sum.add(r, fill_value=0)
        wsum += w
    if rank_sum is None:
        raise ValueError("oriented_composite: no factors")
    return rank_sum / wsum


def set_composite(reg, panel, mask, source="stored"):
    """Oriented EW-rank composite of a registry's active factors, and the
    factor count used. ``source='stored'`` reads the float32 registry values
    (fast, 2017-2025 only); ``source='expr'`` recomputes from expressions over
    the full panel (slow, but covers 2026). The one place the "build a set's
    deployable composite" ritual lives — callers neutralize as needed."""
    actives = reg.active()
    if source == "stored":
        frames = (reg.values(a["name"]) * a["direction"] for a in actives)
        return oriented_composite(frames, mask), len(actives)
    from . import pipeline as pl          # lazy: avoid an import cycle
    count = {"n": 0}

    def _oriented():
        for a in actives:
            try:
                F = pl.compute_factor(a["expression"], panel) * a["direction"]
            except Exception:
                continue
            count["n"] += 1
            yield F

    return oriented_composite(_oriented(), mask), count["n"]


# ------------------------------------------------------------ investability

def investable_mask(panel, base_mask: pd.DataFrame, *, status_only=None,
                    min_days=None, size_drop=None) -> pd.DataFrame:
    """Restrict ``base_mask`` (tradable_entry) to an investable universe.

    Always drops ST names and names listed < ``min_days`` trading days.
    When ``status_only`` is False, additionally drops the smallest
    ``size_drop`` fraction by circulating market cap. The size cut is
    opt-in: the neutralization eval showed it hurts out-of-sample because
    the behavioral edge lives partly in small caps (NEUTRALIZE_REPORT.md).

    Unset args fall back to config (``FILTER_*``) so the thresholds have a
    single source of truth.
    """
    status_only = cfg.FILTER_STATUS_ONLY if status_only is None else status_only
    min_days = cfg.FILTER_MIN_DAYS if min_days is None else min_days
    size_drop = cfg.FILTER_SIZE_DROP if size_drop is None else size_drop
    is_st = panel.wide("is_st").astype(float) > 0
    days = panel.wide("DAYS_ON").astype(float)
    inv = base_mask & (~is_st.reindex_like(base_mask).fillna(False)) \
        & (days >= min_days)
    if not status_only:
        inv = inv & (_style(panel)["size_rank"] > size_drop)
    return inv.fillna(False)
