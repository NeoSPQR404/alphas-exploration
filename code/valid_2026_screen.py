#!/usr/bin/env python3
"""Per-factor 2026 screen: which individual alphas are VALID and EFFICIENT in
the genuinely-unseen 2026 window.

For every active factor in all three sets, recompute it from its expression
over the 2017-2026 panel (stored values stop at 2025) and score it on 2026:

  valid_2026      the factor still predicts in its stored direction:
                  sign(IC_2026) == direction AND |IC_2026| >= IC_MIN
  efficient_2026  it survives its OWN turnover cost standalone:
                  cost_aware long-excess net of 15bp turnover cost > 0
                  (the tradable, A-share-relevant leg; short leg unshortable)

Both are measured on the raw factor (as gated historically); neutralization is
a composite-construction overlay, not a per-factor property. Context columns:
historical IS/OOS IC (from the registry), 2026 turnover, gross vs net excess.

Outputs results/mining/valid_2026_screen.json (+ VALID_2026.md written after).
Run: python3 code/valid_2026_screen.py
"""
import json
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mining import alphaseval as ae          # noqa: E402
from mining import config as cfg             # noqa: E402
from mining import pipeline as pl            # noqa: E402
from mining.data import Panel                # noqa: E402
from mining.registry import Registry         # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
W26 = ("20260101", "20261231")
IC_MIN = 0.03                                 # project validity bar
BP = cfg.SCORING_COST_BP                       # 15bp efficiency bar
SETS = [("main", "behavioral_full"), ("canonical", "canonical"),
        ("canonical_composite", "canonical_composite")]


def main():
    t0 = time.time()
    panel = Panel(years=range(2017, 2027))
    mask = panel.universe_mask("all")
    label = panel.label(cfg.HORIZON)
    m26 = ae.slice_dates(mask, *W26)
    l26 = ae.slice_dates(label, *W26)
    print(f"panel ready [{time.time()-t0:.0f}s]; 2026 dates={len(l26)}", flush=True)

    rows = []
    for arg, name in SETS:
        reg = Registry(arg)
        actives = reg.active()
        for i, a in enumerate(actives):
            try:
                F = pl.compute_factor(a["expression"], panel)
            except Exception:
                continue
            d = int(a["direction"])
            F26 = ae.slice_dates(F, *W26)
            ic26 = float(ae.daily_ic(F26, l26, m26).mean())
            signed_ic26 = ic26 * d                      # >0 = still works
            ca = ae.cost_aware(F26 * d, l26, m26, cfg.HORIZON, cost_bps=cfg.COST_BPS)
            net = ca[f"long_excess_net_{BP}bp_ann"]
            gross = ca["long_excess_gross_ann"]
            turn = ca["turnover_long"]
            is_ic = float(a.get("metrics", {}).get("is", {}).get("ic_mean", np.nan))
            valid = np.isfinite(signed_ic26) and signed_ic26 >= IC_MIN
            eff = np.isfinite(net) and net > 0
            rows.append({
                "set": name, "name": a["name"], "family": a.get("family", ""),
                "direction": d, "is_ic": is_ic,
                "ic_2026": ic26, "signed_ic_2026": signed_ic26,
                "gross_excess_2026": gross, f"net_excess_{BP}bp_2026": net,
                "turnover_2026": turn, "n_rebal_2026": ca.get("n_rebal"),
                "valid": bool(valid), "efficient": bool(eff),
                "valid_and_efficient": bool(valid and eff),
            })
            if (i + 1) % 20 == 0:
                print(f"  [{name}] {i+1}/{len(actives)} [{time.time()-t0:.0f}s]", flush=True)
        print(f"[{name}] done: {len(actives)} factors [{time.time()-t0:.0f}s]", flush=True)

    netkey = f"net_excess_{BP}bp_2026"
    survivors = sorted((r for r in rows if r["valid_and_efficient"]),
                       key=lambda r: -r[netkey])
    by_set = {}
    for name in [s[1] for s in SETS]:
        s = [r for r in rows if r["set"] == name]
        by_set[name] = {
            "n": len(s),
            "valid": sum(r["valid"] for r in s),
            "efficient": sum(r["efficient"] for r in s),
            "valid_and_efficient": sum(r["valid_and_efficient"] for r in s),
            "median_signed_ic_2026": float(np.median([r["signed_ic_2026"] for r in s])) if s else None,
            "median_net_2026": float(np.median([r[netkey] for r in s])) if s else None,
        }

    out = {"window": W26, "ic_min": IC_MIN, "cost_bp": BP,
           "criteria": {"valid": "sign(IC_2026)==direction & |IC_2026|>=IC_MIN",
                        "efficient": f"long-excess net of {BP}bp turnover cost > 0"},
           "by_set": by_set,
           "survivors": survivors, "all_factors": rows}
    p = ROOT / "results" / "mining" / "valid_2026_screen.json"
    p.write_text(json.dumps(out, indent=2, default=float))

    print(f"\n=== 2026 per-factor screen ===")
    for name, s in by_set.items():
        print(f"{name:22} n={s['n']:3}  valid={s['valid']:3}  "
              f"efficient={s['efficient']:3}  BOTH={s['valid_and_efficient']:3}  "
              f"med_signedIC={s['median_signed_ic_2026']:+.3f}  med_net={s['median_net_2026']:+.1%}")
    print(f"\nTop valid+efficient (by 2026 net excess):")
    print(f"{'name':16} {'set':20} {'sIC26':>7} {'net15':>7} {'gross':>7} {'turn':>6} {'family'}")
    for r in survivors[:25]:
        print(f"{r['name']:16} {r['set']:20} {r['signed_ic_2026']:>+7.3f} "
              f"{r[netkey]:>+7.1%} {r['gross_excess_2026']:>+7.1%} "
              f"{r['turnover_2026']:>6.2f} {r['family']}")
    print(f"\ntotal valid+efficient: {len(survivors)}  ->  {p}  [{time.time()-t0:.0f}s]")


if __name__ == "__main__":
    main()
