#!/usr/bin/env python3
"""The honest test: evaluate the full alpha set on the 2024-2025 holdout.

The holdout window (config.HOLDOUT_START..HOLDOUT_END) was never used for
accept/reject decisions and never distilled into experience memory. This
script reads it ONCE for all active factors and the combined set.

Outputs:
  results/mining/holdout/full_set_eval.json   per-factor + composite stats
Run:
  python3 code/holdout_eval.py
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mining import alphaseval as ae          # noqa: E402
from mining import config as cfg             # noqa: E402
from mining.data import Panel                # noqa: E402
from mining.registry import Registry         # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

WINDOWS = {
    "is": (cfg.IS_START, cfg.IS_END),
    "oos_gate": (cfg.OOS_START, cfg.OOS_END),
    "holdout": (cfg.HOLDOUT_START, cfg.HOLDOUT_END),
}


def window_stats(F, label, mask, start, end, horizon):
    Fw = ae.slice_dates(F, start, end)
    lw = ae.slice_dates(label, start, end)
    mw = ae.slice_dates(mask, start, end)
    ic = ae.daily_ic(Fw, lw, mw)
    st = ae.ic_stats(ic)
    q = ae.quantile_returns(Fw, lw, mw, step=horizon)
    st["ls_mean"] = q["ls_mean"]
    years = ic.index.str[:4]
    st["yearly"] = {y: float(v) for y, v in ic.groupby(years).mean().items()
                    if np.isfinite(v)}
    return st


def main(set_name: str = "main"):
    if set_name == "main":
        out = (ROOT / "results" / "mining" / "sets" / "behavioral_full"
               / "holdout" / "full_set_eval.json")
    else:
        out = (ROOT / "results" / "mining" / "sets" / set_name
               / "holdout" / "full_set_eval.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    panel = Panel()
    reg = Registry(set_name)
    mask = panel.universe_mask("all")
    label = panel.label(cfg.HORIZON)
    actives = reg.active()
    print(f"honest test: {len(actives)} factors, holdout "
          f"{cfg.HOLDOUT_START}..{cfg.HOLDOUT_END}")

    per_factor = {}
    rank_sum = None      # equal-weight oriented rank composite
    icir_sum = None      # IS-ICIR-weighted composite
    icir_wtot = 0.0

    for i, a in enumerate(actives):
        F = reg.values(a["name"]) * a["direction"]
        res = {"family": a["family"], "round": a["accepted_round"],
               "direction": a["direction"], "expression": a["expression"]}
        for wname, (s, e) in WINDOWS.items():
            res[wname] = window_stats(F, label, mask, s, e, cfg.HORIZON)
        is_ic = res["is"]["ic_mean"]
        ho_ic = res["holdout"]["ic_mean"]
        res["sign_consistent"] = bool(np.sign(ho_ic) == np.sign(is_ic))
        res["holdout_over_is"] = float(ho_ic / is_ic) if is_ic else None
        oos_ic = res["oos_gate"]["ic_mean"]
        res["holdout_over_oos"] = float(ho_ic / oos_ic) if oos_ic else None
        per_factor[a["name"]] = res

        r = ae._masked(F, mask).rank(axis=1, pct=True)
        rank_sum = r if rank_sum is None else rank_sum.add(r, fill_value=0)
        w = abs(a["metrics"]["is"]["icir"] or 0)
        icir_sum = r * w if icir_sum is None else icir_sum.add(r * w,
                                                               fill_value=0)
        icir_wtot += w
        if (i + 1) % 15 == 0:
            print(f"{i+1}/{len(actives)} [{time.time()-t0:.0f}s]")

    composites = {}
    for cname, comp in (("equal_weight", rank_sum / len(actives)),
                        ("icir_weight", icir_sum / icir_wtot)):
        centry = {}
        for wname, (s, e) in WINDOWS.items():
            centry[wname] = window_stats(comp, label, mask, s, e, cfg.HORIZON)
        composites[cname] = centry

    hos = [v["holdout"]["ic_mean"] for v in per_factor.values()]
    summary = {
        "n_factors": len(actives),
        "holdout_window": [cfg.HOLDOUT_START, cfg.HOLDOUT_END],
        "median_holdout_ic": float(np.median(hos)),
        "mean_holdout_ic": float(np.mean(hos)),
        "sign_consistency_rate": float(np.mean(
            [v["sign_consistent"] for v in per_factor.values()])),
        "share_holdout_ic_ge_003": float(np.mean(
            [abs(x) >= 0.03 for x in hos])),
        "share_holdout_ic_ge_002": float(np.mean(
            [abs(x) >= 0.02 for x in hos])),
        "median_holdout_over_oos": float(np.median(
            [v["holdout_over_oos"] for v in per_factor.values()
             if v["holdout_over_oos"] is not None])),
    }

    out.write_text(json.dumps(
        {"summary": summary, "composites": composites,
         "factors": per_factor}, indent=2, default=float))
    print(json.dumps(summary, indent=2))
    print("composites (holdout):",
          {k: round(v["holdout"]["ic_mean"], 4) for k, v in composites.items()})
    print(f"done in {time.time()-t0:.0f}s -> {out}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "main")
