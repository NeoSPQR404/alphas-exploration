"""Run one mining round: Retrieve -> Generate(candidates file) -> Evaluate
-> Distill scaffolding.

Usage:
    python3 code/mining/round.py rounds/round01_candidates.py

The candidates file defines CANDIDATES = [ {name, expr, family, rationale,
logic_score}, ... ] (the Generate step, written by the mining agent after
reading experience memory). This runner executes the 4-stage evaluation,
updates the alpha registry, writes a round report + holdout file, and logs
the round skeleton into experience memory (the agent then adds distilled
patterns via memory.py).
"""
from __future__ import annotations

import json
import runpy
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mining import alphaseval as ae            # noqa: E402
from mining import config as cfg               # noqa: E402
from mining import pipeline as pl              # noqa: E402
from mining.data import Panel                  # noqa: E402
from mining.memory import Memory               # noqa: E402
from mining.registry import Registry           # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
# main-set round artifacts live under sets/behavioral_full/ (moved
# 2026-07-09; main registry == behavioral_full membership)
ROUNDS_DIR = ROOT / "results" / "mining" / "sets" / "behavioral_full" / "rounds"
HOLDOUT_DIR = ROOT / "results" / "mining" / "sets" / "behavioral_full" / "holdout"


def _fmt(v, nd=4):
    return "n/a" if v is None or not np.isfinite(v) else f"{v:.{nd}f}"


def run(candidates_path: str):
    t0 = time.time()
    module = runpy.run_path(candidates_path)
    candidates = module["CANDIDATES"]
    set_name = module.get("SET_NAME", "main")
    whitelist = module.get("FIELD_WHITELIST")

    panel = Panel()
    reg = Registry(set_name)
    mem = Memory(set_name)
    round_id = mem.next_round_id()
    mask_all = panel.universe_mask("all")
    noise_var = ae.noise_variance(panel)
    print(f"=== [{set_name}] Round {round_id}: {len(candidates)} candidates, "
          f"noise_var={noise_var:.5f}, whitelist="
          f"{'none' if whitelist is None else ','.join(whitelist)} ===")

    results = []
    for cand in candidates:
        rec = dict(cand)
        try:
            factor = pl.compute_factor(cand["expr"], panel, whitelist)
        except Exception as e:
            rec["error"] = f"{type(e).__name__}: {e}"
            rec["s1"] = {"pass": False}
            results.append(rec)
            print(f"[{cand['name']}] ERROR {rec['error']}")
            continue
        rec["factor"] = factor
        rec["s1"] = pl.stage1_quick_ic(factor, panel, mask_all)
        s1 = rec["s1"]
        print(f"[{cand['name']}] S1 ic={_fmt(s1['ic_mean'])} "
              f"icir={_fmt(s1['icir'], 2)} cov={_fmt(s1['coverage'], 2)} "
              f"-> {'PASS' if s1['pass'] else 'reject'}")
        results.append(rec)

    # ---- stage 2
    s1_survivors = [r for r in results if r["s1"]["pass"]]
    for r in s1_survivors:
        r["s2"] = pl.stage2_set_correlation(
            r["factor"], abs(r["s1"]["ic_mean"]), reg, panel, mask_all)
        s2 = r["s2"]
        tag = "PASS" if s2["pass"] else f"reject (|corr|={s2['max_corr']:.2f} vs {s2['against']})"
        if s2["pass"] and s2.get("replace"):
            tag = f"PASS, replaces {s2['replace']}"
        print(f"[{r['name']}] S2 max_corr={_fmt(s2['max_corr'], 2)} -> {tag}")

    # ---- stage 3
    s2_survivors = [r for r in s1_survivors if r["s2"]["pass"]]
    pl.stage3_dedup(s2_survivors, panel, mask_all)
    for r in s2_survivors:
        s3 = r["s3"]
        print(f"[{r['name']}] S3 -> "
              f"{'PASS' if s3['pass'] else 'dup of ' + s3['duplicate_of']}")

    # ---- stage 4
    s3_survivors = [r for r in s2_survivors if r["s3"]["pass"]]
    for r in s3_survivors:
        r["s4"] = pl.stage4_coverage(r["factor"], panel, r["s1"]["ic_mean"])
        s4 = r["s4"]
        print(f"[{r['name']}] S4 oos_ic={_fmt(s4['oos']['ic_mean'])} "
              f"uni_pass={sum(u['pass'] for u in s4['universes'].values())}/3 "
              f"year_rate={_fmt(s4['year_sign_rate'], 2)} "
              f"-> {'ACCEPT' if s4['pass'] else 'reject'}")

    # ---- accept + registry update
    accepted = []
    holdout_report = {}
    for r in s3_survivors:
        if not r["s4"]["pass"]:
            continue
        metrics = pl.full_metrics(r["factor"], panel, mask_all, noise_var)
        metrics["s4"] = {k: v for k, v in r["s4"].items() if k != "oos"}
        direction = int(np.sign(r["s1"]["ic_mean"]))
        if r["s2"].get("replace"):
            reg.retire(r["s2"]["replace"],
                       f"replaced by stronger correlated factor", round_id)
        entry = reg.add(r["expr"], r["family"], r["rationale"], direction,
                        metrics, round_id, r["factor"], r["logic_score"])
        r["accepted_name"] = entry["name"]
        accepted.append(r)
        holdout_report[entry["name"]] = pl.holdout_metrics(
            r["factor"], panel, mask_all)

    # ---- set-level diversity
    div = np.nan
    if len(reg.active()) >= 2:
        facs = [ae.slice_dates(reg.values(a["name"]), cfg.IS_START,
                               cfg.OOS_END) for a in reg.active()]
        div = ae.diversity_entropy(
            facs, ae.slice_dates(mask_all, cfg.IS_START, cfg.OOS_END))

    reg.save()
    reg.export_csv()

    # ---- artifacts
    rounds_dir = ROUNDS_DIR if set_name == "main" else \
        ROOT / "results" / "mining" / "sets" / set_name / "rounds"
    holdout_dir = HOLDOUT_DIR if set_name == "main" else \
        ROOT / "results" / "mining" / "sets" / set_name / "holdout"
    rounds_dir.mkdir(parents=True, exist_ok=True)
    holdout_dir.mkdir(parents=True, exist_ok=True)
    (holdout_dir / f"round_{round_id:02d}.json").write_text(
        json.dumps(holdout_report, indent=2))

    detail = []
    for r in results:
        d = {k: r[k] for k in ("name", "expr", "family", "rationale",
                               "logic_score") if k in r}
        for s in ("s1", "s2", "s3", "s4"):
            if s in r:
                d[s] = r[s]
        if "error" in r:
            d["error"] = r["error"]
        if "accepted_name" in r:
            d["accepted_name"] = r["accepted_name"]
        detail.append(d)
    (rounds_dir / f"round_{round_id:02d}.json").write_text(
        json.dumps({"round": round_id, "diversity": None if not np.isfinite(div) else div,
                    "results": detail}, indent=2, default=float))

    summary = {
        "candidates": len(candidates),
        "s1_pass": len(s1_survivors),
        "s2_pass": len(s2_survivors),
        "s3_pass": len(s3_survivors),
        "accepted": [r["accepted_name"] for r in accepted],
        "alpha_set_size": len(reg.active()),
        "diversity_entropy": None if not np.isfinite(div) else float(div),
        "candidates_file": str(candidates_path),
    }
    mem.log_round(round_id, summary)
    mem.save()

    print(f"\n=== Round {round_id} done in {time.time()-t0:.0f}s: "
          f"{len(accepted)}/{len(candidates)} accepted, "
          f"set size {len(reg.active())}, diversity={_fmt(div, 3)} ===")
    print("Distill step: agent should now write patterns into "
          "experience_memory.json via mining.memory.Memory")
    return summary


if __name__ == "__main__":
    run(sys.argv[1])
