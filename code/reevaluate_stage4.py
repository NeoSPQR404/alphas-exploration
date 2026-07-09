#!/usr/bin/env python3
"""Re-run the (upgraded) stage-4 evaluation for every active factor of a
set, using stored factor values. Reports pass/fail per sub-test; does NOT
retire anything — purge decisions are left to the user.

Run: python3 code/reevaluate_stage4.py <set_name>
Output: <set_dir>/stage4_reeval.json
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mining import config as cfg             # noqa: E402
from mining import pipeline as pl            # noqa: E402
from mining.data import Panel                # noqa: E402
from mining.registry import Registry         # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

PARAMS = {
    "label": f"fwd_ret_{cfg.HORIZON}d (entry t+1 vwap, suspension-aware)",
    "universe": "full-A tradable_entry, min 50 names/date",
    "ic_type": "daily cross-sectional Spearman rank IC, oriented by "
               "stored factor direction",
    "windows": {"is": [cfg.IS_START, cfg.IS_END],
                "oos_gate": [cfg.OOS_START, cfg.OOS_END],
                "test_span_for_rolling_bootstrap_yearly":
                    [cfg.IS_START, cfg.OOS_END]},
    "oos_test": f"same sign as IS and |OOS IC| >= max({cfg.S4_MIN_OOS_ABS_IC}, "
                f"{cfg.S4_MIN_OOS_IC_RATIO} x |IS IC|)",
    "universes_test": f">= {cfg.S4_MIN_UNIVERSES_PASS} of "
                      f"{list(cfg.S4_UNIVERSES)} with same-sign IC >= "
                      f"{cfg.S4_UNIVERSE_MIN_ABS_IC} over IS+OOS",
    "yearly_test": f"share of same-sign yearly ICs >= {cfg.S4_MIN_YEAR_SIGN_RATE}",
    "rolling_test": {"window_days": cfg.S4_ROLL_WINDOW,
                     "step_days": cfg.S4_ROLL_STEP,
                     "min_sign_rate": cfg.S4_ROLL_MIN_SIGN_RATE},
    "bootstrap_test": {"method": "moving-block bootstrap of mean daily IC",
                       "n_boot": cfg.S4_BOOT_B,
                       "block_days": cfg.S4_BOOT_BLOCK,
                       "seed": cfg.S4_BOOT_SEED,
                       "h0": "mean oriented IC <= 0",
                       "max_p_value": cfg.S4_BOOT_MAX_P},
}


def main(set_name: str):
    t0 = time.time()
    panel = Panel()
    reg = Registry(set_name)
    set_dir = (ROOT / "results" / "mining" if set_name == "main"
               else ROOT / "results" / "mining" / "sets" / set_name)
    actives = reg.active()
    print(f"stage-4 re-eval [{set_name}]: {len(actives)} factors")

    results = {}
    for i, a in enumerate(actives):
        F = reg.values(a["name"])
        is_ic = a["metrics"]["is"]["ic_mean"]
        s4 = pl.stage4_coverage(F, panel, is_ic)
        s4.pop("yearly_ic", None)
        s4["oos"] = {k: s4["oos"][k] for k in ("ic_mean", "icir")}
        results[a["name"]] = {
            "family": a["family"], "round": a["accepted_round"],
            "expression": a["expression"], "is_ic": is_ic, **s4}
        if (i + 1) % 15 == 0:
            print(f"{i+1}/{len(actives)} [{time.time()-t0:.0f}s]")

    n = len(results)
    summary = {
        "n_factors": n,
        "pass_all": sum(v["pass"] for v in results.values()),
        "fail_oos": sum(not v["oos_pass"] for v in results.values()),
        "fail_universes": sum(not v["universes_pass"] for v in results.values()),
        "fail_yearly": sum(not v["year_pass"] for v in results.values()),
        "fail_rolling": sum(not v["rolling_pass"] for v in results.values()),
        "fail_bootstrap": sum(not v["bootstrap_pass"] for v in results.values()),
    }
    out = set_dir / "stage4_reeval.json"
    out.write_text(json.dumps({"parameters": PARAMS, "summary": summary,
                               "factors": results}, indent=2, default=float))
    print(json.dumps(summary, indent=2))
    print(f"done in {time.time()-t0:.0f}s -> {out}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "main")
