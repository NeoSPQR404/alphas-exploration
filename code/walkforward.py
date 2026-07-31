#!/usr/bin/env python3
"""Walk-forward validation of the factor-selection process.

The composite is EW (no fitted weights), so the only overfitting source is
FACTOR SELECTION. This simulates production honestly: at each yearly test block,
select the top-K factors by IC on the EXPANDING past-only training window
(orienting by the train-window sign — never the stored full-sample direction),
then measure their IC on the never-seen test year.

Reports, per test year and per K: in-sample (train) IC of the selected set vs the
realized OUT-OF-SAMPLE IC on the test year, and the IS->OOS haircut. Answers the
selection-bias critique: what does the selection process actually generalize to?

Pool: behavioral_full (stored raw values, 2017-2025). Run: python3 code/walkforward.py
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mining import alphaseval as ae          # noqa: E402
from mining import config as cfg             # noqa: E402
from mining.data import Panel                # noqa: E402
from mining.registry import Registry         # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TEST_YEARS = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
KS = [10, 20, 30, 50, None]                   # None = all factors (no selection)
MIN_TRAIN_DAYS = 250


def main():
    panel = Panel()
    mask = panel.universe_mask("all")
    label = panel.label(cfg.HORIZON)
    reg = Registry("main")
    actives = reg.active()
    print(f"computing daily IC series for {len(actives)} factors...", flush=True)

    ic = {}
    for i, a in enumerate(actives):
        F = reg.values(a["name"])              # RAW (do not use stored direction)
        ic[a["name"]] = ae.daily_ic(F, label, mask)
        if (i + 1) % 25 == 0:
            print(f"  {i+1}/{len(actives)}", flush=True)
    icdf = pd.DataFrame(ic)                     # dates x factors (raw, unsigned)
    yr = icdf.index.str[:4]

    rows = []
    for K in KS:
        for ty in TEST_YEARS:
            train = icdf[yr < str(ty)]
            test = icdf[yr == str(ty)]
            if len(train) < MIN_TRAIN_DAYS or len(test) < 20:
                continue
            train_ic = train.mean()            # per-factor IC on past-only data
            sign = np.sign(train_ic)
            oriented_train = (train_ic * sign)             # = |train_ic|
            oriented_test = (test.mean() * sign)           # test IC, oriented by TRAIN sign
            order = oriented_train.sort_values(ascending=False).index
            sel = order[:K] if K else order
            rows.append({
                "K": K if K else len(actives), "test_year": ty,
                "n_selected": len(sel),
                "is_ic": float(oriented_train[sel].mean()),
                "oos_ic": float(oriented_test[sel].mean()),
            })

    # aggregate per K
    agg = {}
    for K in KS:
        kk = K if K else len(actives)
        r = [x for x in rows if x["K"] == kk]
        if not r:
            continue
        oos = np.array([x["oos_ic"] for x in r])
        iss = np.array([x["is_ic"] for x in r])
        agg[kk] = {"mean_is_ic": float(iss.mean()), "mean_oos_ic": float(oos.mean()),
                   "oos_ic_std": float(oos.std()), "haircut": float(oos.mean() / iss.mean()),
                   "oos_pos_years": int((oos > 0).sum()), "n_years": len(r)}

    out = {"pool": "behavioral_full", "n_factors": len(actives),
           "test_years": TEST_YEARS, "window": "expanding, past-only",
           "orientation": "train-window sign (no full-sample lookahead)",
           "per_year": rows, "by_K": agg}
    (ROOT / "results" / "mining" / "walkforward.json").write_text(
        json.dumps(out, indent=2, default=float))

    print(f"\n=== walk-forward selection (expanding window, behavioral_full) ===")
    print(f"{'K':>5} {'mean_IS_IC':>11} {'mean_OOS_IC':>12} {'haircut':>8} "
          f"{'OOS_std':>8} {'pos_yrs':>8}")
    for kk, s in agg.items():
        print(f"{kk:>5} {s['mean_is_ic']:>+11.4f} {s['mean_oos_ic']:>+12.4f} "
              f"{s['haircut']:>8.2f} {s['oos_ic_std']:>8.4f} {s['oos_pos_years']:>4}/{s['n_years']}")
    print("\nper-year OOS IC (K=30):")
    for x in [r for r in rows if r["K"] == 30]:
        print(f"  {x['test_year']}: IS {x['is_ic']:+.4f}  OOS {x['oos_ic']:+.4f}")
    print("\n-> results/mining/walkforward.json")


if __name__ == "__main__":
    main()
