#!/usr/bin/env python3
"""Style/status filter + size&industry neutralization — evaluation layer.

For each set, recompute the EW oriented-rank composite once, then evaluate
four portfolio-construction variants on the historical (2017-25) and the
fresh 2026 window:

  raw            top-decile long over all tradable names (baseline)
  filtered       + investable universe (drop ST, <250d listed, smallest
                 30% by circ_mv — the shell/micro-cap speculative names)
  neutralized    composite residualized per-date against log(circ_mv) and
                 SW-L1 industry (Barra-lite), over all tradable names
  filt_neutral   both

Reports, per variant/window: decile curve, long-only excess-vs-universe
ann return, long-short gross ann return, and the signal's daily rank IC.

Run: python3 code/neutralize_eval.py <set_name>
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mining import alphaseval as ae          # noqa: E402
from mining import config as cfg             # noqa: E402
from mining import construct as cs           # noqa: E402
from mining.data import Panel                # noqa: E402
from mining.registry import Registry         # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SIZE_DROP = cfg.FILTER_SIZE_DROP   # drop the smallest 30% by circ_mv
MIN_DAYS = cfg.FILTER_MIN_DAYS     # exclude names listed < 250 trading days
WINDOWS = {"full": ("20170101", "20251231"), "y2026": ("20260101", "20261231")}


def main(set_name):
    t0 = time.time()
    panel = Panel(years=range(2017, 2027))
    reg = Registry(set_name)
    mask = panel.universe_mask("all")                 # tradable_entry
    label = panel.label(cfg.HORIZON)
    print(f"[{set_name}] recompute {len(reg.active())} factors")

    comp, n = cs.set_composite(reg, panel, mask, "expr")
    print(f"  composite done [{time.time()-t0:.0f}s]; building style/status")

    # 'filtered' variant keeps the size cut (status_only=False) so this eval
    # still contrasts the micro-cap filter against status-only construction.
    invest = cs.investable_mask(panel, mask, status_only=False,
                                min_days=MIN_DAYS, size_drop=SIZE_DROP)
    comp_neu = cs.neutralize_factor(comp, panel, mask)
    print(f"  neutralized [{time.time()-t0:.0f}s]")

    variants = {"raw": (comp, mask), "filtered": (comp, invest),
                "neutralized": (comp_neu, mask), "filt_neutral": (comp_neu, invest)}
    out = {"set": set_name, "n_factors": n,
           "filter": {"drop_ST": True, "min_days_on_market": MIN_DAYS,
                      "drop_smallest_pct": SIZE_DROP},
           "neutralize": "per-date residual on [SW-L1 industry, log circ_mv]",
           "variants": {}}
    for vname, (sig, univ) in variants.items():
        out["variants"][vname] = {w: ae.window_backtest(sig, label, univ, win,
                                                         cfg.HORIZON)
                                  for w, win in WINDOWS.items()}
    p = (ROOT / "results" / "mining" / "sets"
         / ("behavioral_full" if set_name == "main" else set_name) / "neutralize_eval.json")
    p.write_text(json.dumps(out, indent=2, default=float))
    # console summary
    for v in variants:
        f = out["variants"][v]["full"]; y = out["variants"][v]["y2026"]
        print(f"  {v:13} full: exc {f['long_excess_ann']:+.1%} IC {f['ic_mean']:+.3f} | "
              f"2026: exc {y['long_excess_ann']:+.1%} LS {y['ls_gross_ann']:+.1%} IC {y['ic_mean']:+.3f}")
    print(f"done [{time.time()-t0:.0f}s] -> {p}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "main")
