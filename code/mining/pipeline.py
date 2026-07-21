"""Multi-stage evaluation pipeline (the 4 gates from the mining prompt).

Stage 1  Quick IC screen        in-sample full-A rank IC / ICIR / coverage
Stage 2  Alpha-set correlation  vs accepted factors, with the "30%-better
                                IC" replacement exemption
Stage 3  Duplication removal    pairwise within the surviving round batch
Stage 4  Coverage test          OOS window + sub-universe + yearly sign
                                consistency (robustness, not luck)

A final 2024-2025 holdout is computed for accepted factors but written
separately (results/mining/holdout/) and never used for gating.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import alphaseval as ae
from . import config as cfg
from . import operators as ops
from .data import Panel


# ------------------------------------------------------------ expression eval

def compute_factor(expr: str, panel: Panel,
                   field_whitelist: list[str] | None = None) -> pd.DataFrame:
    """Evaluate a candidate expression in a sandboxed operator namespace.

    If `field_whitelist` is given, every non-operator name in the
    expression must be in it (AST-enforced) — used by restricted sets
    like the canonical-OHLCV set.
    """
    if field_whitelist is not None:
        import ast
        names = {n.id for n in ast.walk(ast.parse(expr, mode="eval"))
                 if isinstance(n, ast.Name)}
        allowed = set(ops.OPERATORS) | set(field_whitelist) | {"np"}
        illegal = names - allowed
        if illegal:
            raise ValueError(f"fields outside whitelist: {sorted(illegal)}")
    ns = panel.namespace()          # lazy field lookup (OPEN, CLOSE, EP, ...)
    ns.update(ops.OPERATORS)
    if field_whitelist is None:
        ns["IND"] = panel.wide("INDUSTRY")
    ns["np"] = np
    out = eval(expr, {"__builtins__": {}}, ns)  # noqa: S307 - curated ns
    if not isinstance(out, pd.DataFrame):
        raise ValueError(f"expression did not return a wide frame: {expr}")
    out = out.replace([np.inf, -np.inf], np.nan)
    return ops.CsWinsor(out)


# ------------------------------------------------------------ stages

def stage1_quick_ic(factor, panel, mask) -> dict:
    F = ae.slice_dates(factor, cfg.IS_START, cfg.IS_END)
    m = ae.slice_dates(mask, cfg.IS_START, cfg.IS_END)
    label = ae.slice_dates(panel.label(cfg.HORIZON), cfg.IS_START, cfg.IS_END)
    stats = ae.ic_stats(ae.daily_ic(F, label, m))
    stats["coverage"] = ae.coverage(F, m)
    stats["pass"] = bool(
        np.isfinite(stats["ic_mean"])
        and abs(stats["ic_mean"]) >= cfg.S1_MIN_ABS_IC
        and abs(stats["icir"]) >= cfg.S1_MIN_ABS_ICIR
        and stats["coverage"] >= cfg.S1_MIN_COVERAGE
    )
    return stats


def stage2_set_correlation(factor, is_abs_ic, registry, panel, mask) -> dict:
    """Check vs accepted set. Returns pass/fail and any replacement target."""
    out = {"max_corr": 0.0, "against": None, "replace": None, "pass": True}
    F = ae.slice_dates(factor, cfg.IS_START, cfg.IS_END)
    m = ae.slice_dates(mask, cfg.IS_START, cfg.IS_END)
    for entry in registry.active():
        inc = registry.values(entry["name"])
        c = ae.factor_corr(F, ae.slice_dates(inc, cfg.IS_START, cfg.IS_END), m)
        if np.isfinite(c) and abs(c) > abs(out["max_corr"]):
            out["max_corr"] = float(c)
            out["against"] = entry["name"]
        if np.isfinite(c) and abs(c) >= cfg.S2_MAX_ABS_CORR:
            old_ic = abs(entry["metrics"]["is"]["ic_mean"])
            if is_abs_ic >= cfg.S2_REPLACE_IC_RATIO * old_ic:
                out["replace"] = entry["name"]   # exemption: much stronger
            else:
                out["pass"] = False
                return out
    return out


def stage3_dedup(survivors: list[dict], panel, mask) -> list[dict]:
    """Greedy keep-best: sort by |IS ICIR|, drop later ones correlated
    >= threshold with anything kept."""
    ranked = sorted(survivors, key=lambda r: -abs(r["s1"]["icir"]))
    kept = []
    m = ae.slice_dates(mask, cfg.IS_START, cfg.IS_END)
    for r in ranked:
        F = ae.slice_dates(r["factor"], cfg.IS_START, cfg.IS_END)
        dup_of = None
        for k in kept:
            c = ae.factor_corr(F, ae.slice_dates(k["factor"], cfg.IS_START,
                                                 cfg.IS_END), m)
            if np.isfinite(c) and abs(c) >= cfg.S3_MAX_ABS_CORR:
                dup_of = k["name"]
                break
        if dup_of:
            r["s3"] = {"pass": False, "duplicate_of": dup_of}
        else:
            r["s3"] = {"pass": True}
            kept.append(r)
    return survivors


def stage4_coverage(factor, panel, is_ic_mean) -> dict:
    """OOS + sub-universe + yearly sign-consistency gate."""
    sign = np.sign(is_ic_mean)
    mask_all = panel.universe_mask("all")
    label = panel.label(cfg.HORIZON)

    F_oos = ae.slice_dates(factor, cfg.OOS_START, cfg.OOS_END)
    m_oos = ae.slice_dates(mask_all, cfg.OOS_START, cfg.OOS_END)
    l_oos = ae.slice_dates(label, cfg.OOS_START, cfg.OOS_END)
    oos = ae.ic_stats(ae.daily_ic(F_oos, l_oos, m_oos))
    oos_ok = (
        np.isfinite(oos["ic_mean"])
        and np.sign(oos["ic_mean"]) == sign
        and abs(oos["ic_mean"]) >= max(cfg.S4_MIN_OOS_ABS_IC,
                                       cfg.S4_MIN_OOS_IC_RATIO * abs(is_ic_mean))
    )

    # sub-universes over IS+OOS combined (20170101 - OOS_END)
    uni = {}
    n_uni_pass = 0
    for u in cfg.S4_UNIVERSES:
        mu = ae.slice_dates(panel.universe_mask(u), cfg.IS_START, cfg.OOS_END)
        Fu = ae.slice_dates(factor, cfg.IS_START, cfg.OOS_END)
        lu = ae.slice_dates(label, cfg.IS_START, cfg.OOS_END)
        ic_u = ae.daily_ic(Fu, lu, mu).mean()
        ok = (np.isfinite(ic_u) and np.sign(ic_u) == sign
              and abs(ic_u) >= cfg.S4_UNIVERSE_MIN_ABS_IC)
        uni[u] = {"ic_mean": float(ic_u) if np.isfinite(ic_u) else None,
                  "pass": bool(ok)}
        n_uni_pass += int(ok)

    # yearly sign consistency, IS+OOS years only (holdout untouched)
    F_all = ae.slice_dates(factor, cfg.IS_START, cfg.OOS_END)
    m_all = ae.slice_dates(mask_all, cfg.IS_START, cfg.OOS_END)
    yic = ae.yearly_ic(F_all, panel, m_all, cfg.HORIZON)
    year_sign_rate = float(np.mean([np.sign(v) == sign for v in yic.values()]))

    l_isoos = ae.slice_dates(label, cfg.IS_START, cfg.OOS_END)

    # decile-monotonicity over IS+OOS: the decile mean-return curve must
    # rise in the factor's direction, not just spike in the tails (added
    # 2026-07-20). quantile_returns already returns Spearman(mean_q, rank).
    qr = ae.quantile_returns(F_all, l_isoos, m_all, step=cfg.HORIZON)
    mono = qr.get("monotonicity", np.nan)
    mono_ok = (np.isfinite(mono) and np.sign(mono) == sign
               and abs(mono) >= cfg.S4_MIN_MONOTONICITY)

    # cost-aware: the factor must earn a positive long-excess after its own
    # trading costs to be tradable (added 2026-07-20). Orient by IC sign.
    ca = ae.cost_aware(F_all * sign, l_isoos, m_all, cfg.HORIZON,
                       cost_bps=cfg.COST_BPS)
    net_le = ca.get(f"long_excess_net_{cfg.SCORING_COST_BP}bp_ann", np.nan)
    net_ok = (not cfg.GATE_ON_NET_COST) or (
        np.isfinite(net_le) and net_le > cfg.S4_MIN_NET_LONG_EXCESS_ANN)

    # rolling-window + bootstrap tests on the oriented daily IC series
    # over IS+OOS (added 2026-07-09)
    l_all = ae.slice_dates(label, cfg.IS_START, cfg.OOS_END)
    ic_all = ae.daily_ic(F_all, l_all, m_all) * sign
    roll = ae.rolling_ic_consistency(ic_all, cfg.S4_ROLL_WINDOW,
                                     cfg.S4_ROLL_STEP)
    boot = ae.block_bootstrap_pvalue(ic_all, cfg.S4_BOOT_B,
                                     cfg.S4_BOOT_BLOCK, cfg.S4_BOOT_SEED)
    roll_ok = (np.isfinite(roll["sign_rate"])
               and roll["sign_rate"] >= cfg.S4_ROLL_MIN_SIGN_RATE)
    boot_ok = (np.isfinite(boot["p_value"])
               and boot["p_value"] <= cfg.S4_BOOT_MAX_P)

    return {
        "oos": oos,
        "oos_pass": bool(oos_ok),
        "universes": uni,
        "universes_pass": bool(n_uni_pass >= cfg.S4_MIN_UNIVERSES_PASS),
        "yearly_ic": yic,
        "year_sign_rate": year_sign_rate,
        "year_pass": bool(year_sign_rate >= cfg.S4_MIN_YEAR_SIGN_RATE),
        "rolling": roll,
        "rolling_pass": bool(roll_ok),
        "bootstrap": boot,
        "bootstrap_pass": bool(boot_ok),
        "monotonicity": float(mono) if np.isfinite(mono) else None,
        "monotonicity_pass": bool(mono_ok),
        "cost_aware": ca,
        "cost_aware_score": float(net_le) if np.isfinite(net_le) else None,
        "cost_aware_pass": bool(net_ok),
        "pass": bool(oos_ok and n_uni_pass >= cfg.S4_MIN_UNIVERSES_PASS
                     and year_sign_rate >= cfg.S4_MIN_YEAR_SIGN_RATE
                     and roll_ok and boot_ok and mono_ok and net_ok),
    }


# ------------------------------------------------------------ full metrics

def full_metrics(factor, panel, mask, noise_var) -> dict:
    out = {
        "is": ae.evaluate_window(factor, panel, mask, cfg.HORIZON,
                                 cfg.IS_START, cfg.IS_END, noise_var),
        "oos": ae.evaluate_window(factor, panel, mask, cfg.HORIZON,
                                  cfg.OOS_START, cfg.OOS_END, noise_var),
        "decay": ae.decay_profile(
            ae.slice_dates(factor, cfg.IS_START, cfg.OOS_END), panel,
            ae.slice_dates(mask, cfg.IS_START, cfg.OOS_END)),
    }
    return out


def holdout_metrics(factor, panel, mask) -> dict:
    return ae.evaluate_window(factor, panel, mask, cfg.HORIZON,
                              cfg.HOLDOUT_START, cfg.HOLDOUT_END)
