#!/usr/bin/env python3
"""Rolling-IC decay monitor — a first-class health artifact for each set.

The 2026 out-of-sample test showed the behavioral edge degrades in adverse
regimes (BACKTEST_2026.md); NEUTRALIZE_REPORT.md removed the style component
but a residual decay remains. This monitor operationalizes "reduce
conviction when the signal weakens" instead of leaving it as a footnote.

For each set it builds the recommended production signal (the size+industry
**neutralized** EW-rank composite), computes its daily rank IC, and tracks a
trailing rolling-IC against the in-sample baseline. It classifies the health
of the signal into HEALTHY / WATCH / IMPAIRED / BROKEN bands and flags the
first date the trailing IC breached the WATCH line. The fresh-2026 reading
is spliced from the neutralization eval (the genuinely-unseen window).

Fast: builds composites from the STORED registry values (seconds), not from
expressions (which take ~1 h over the extended panel). 2017-2025 only.

Outputs: results/mining/ic_monitor/<set>.json, ic_monitor/summary.json,
IC_MONITOR.md, and figs/fig_ic_monitor.png.

Run: python3 code/monitor_ic.py [set_name]   (default: all three sets)
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mining import alphaseval as ae          # noqa: E402
from mining import config as cfg             # noqa: E402
from mining import construct as cs           # noqa: E402
from mining.data import Panel                # noqa: E402
from mining.registry import Registry         # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "mining" / "ic_monitor"
FIGS = ROOT / "results" / "mining" / "figs"

WINDOW = 120          # trailing trading days (~6 months, ~12 rebalances)
MIN_PERIODS = 60      # need at least this many IC obs in the window

# Health bands: trailing IC as a fraction of the in-sample baseline IC.
HEALTHY_RATIO = 0.60   # >= 60% of baseline -> HEALTHY
WATCH_RATIO = 0.30     # 30-60% -> WATCH; 0-30% -> IMPAIRED; <=0 -> BROKEN
BANDS = [("HEALTHY", HEALTHY_RATIO), ("WATCH", WATCH_RATIO),
         ("IMPAIRED", 0.0), ("BROKEN", -np.inf)]

SETS = [("main", "behavioral_full", "行为全量集"),
        ("canonical", "canonical", "规范价量集"),
        ("canonical_composite", "canonical_composite", "规范复合集")]


def classify(trailing_ic, baseline):
    """Health band from the ratio of trailing IC to the baseline IC."""
    if not np.isfinite(trailing_ic) or baseline <= 0:
        return "n/a", np.nan
    ratio = trailing_ic / baseline
    for name, lo in BANDS:          # last band ("BROKEN", -inf) always matches
        if ratio >= lo:
            return name, float(ratio)


def neutralized_ic_series(set_name, panel, mask, label, t0):
    """Daily rank IC of the neutralized composite, from STORED values."""
    reg = Registry(set_name)
    actives = reg.active()

    def oriented():
        for a in actives:
            yield reg.values(a["name"]) * a["direction"]

    comp = cs.oriented_composite(oriented(), mask)
    neu = cs.neutralize_factor(comp, panel, mask)
    ic = ae.daily_ic(neu, label, mask).dropna()
    print(f"  [{set_name}] {len(actives)} factors, IC series {len(ic)} days "
          f"[{time.time()-t0:.0f}s]", flush=True)
    return ic


def oos_2026_reading(set_name):
    """Neutralized 2026 window IC, spliced from the neutralization eval."""
    d = ROOT / "results" / "mining" / "sets" / set_name / "neutralize_eval.json"
    if not d.exists():
        return None
    j = json.loads(d.read_text())
    y = j["variants"]["neutralized"]["y2026"]
    return {"ic_mean": y["ic_mean"], "n_rebal": y["n_rebal"],
            "source": "neutralize_eval.json (neutralized, fresh 2026)"}


def monitor_set(arg, set_dir, panel, mask, label, t0):
    ic = neutralized_ic_series(arg, panel, mask, label, t0)
    baseline = float(ic[(ic.index >= cfg.IS_START) & (ic.index <= cfg.IS_END)].mean())
    trailing = ic.rolling(WINDOW, min_periods=MIN_PERIODS).mean()

    # per-year mean IC (decay table)
    yearly = {y: float(v) for y, v in ic.groupby(ic.index.str[:4]).mean().items()}

    # latest historical reading (end of stored history)
    last_ic = float(trailing.dropna().iloc[-1])
    last_date = str(trailing.dropna().index[-1])
    last_state, last_ratio = classify(last_ic, baseline)

    # worst trailing reading and its date
    tmin = trailing.dropna()
    min_ic = float(tmin.min()); min_date = str(tmin.idxmin())
    min_state, min_ratio = classify(min_ic, baseline)

    # first WATCH breach after the IS window (trailing < HEALTHY line)
    post = trailing[(trailing.index > cfg.IS_END)].dropna()
    breach = post[post < HEALTHY_RATIO * baseline]
    first_breach = str(breach.index[0]) if len(breach) else None

    # fresh 2026 reading (spliced)
    oos = oos_2026_reading(set_dir)
    oos_out = None
    if oos:
        st, ratio = classify(oos["ic_mean"], baseline)
        oos_out = {**oos, "ratio_to_baseline": ratio, "state": st}

    out = {
        "set": set_dir, "window_days": WINDOW, "min_periods": MIN_PERIODS,
        "baseline_is_ic": baseline,
        "bands": {"HEALTHY": f">= {HEALTHY_RATIO:.2f}x baseline",
                  "WATCH": f"{WATCH_RATIO:.2f}-{HEALTHY_RATIO:.2f}x",
                  "IMPAIRED": f"0-{WATCH_RATIO:.2f}x", "BROKEN": "<= 0"},
        "current_historical": {"date": last_date, "trailing_ic": last_ic,
                               "ratio_to_baseline": last_ratio, "state": last_state},
        "worst_trailing": {"date": min_date, "trailing_ic": min_ic,
                           "ratio_to_baseline": min_ratio, "state": min_state},
        "first_watch_breach": first_breach,
        "yearly_ic": yearly,
        "latest_oos_2026": oos_out,
        # downsample the trailing series (~every 10 days) for the artifact
        "trailing_series": [{"date": str(d_), "ic": float(v)}
                            for d_, v in trailing.dropna().iloc[::10].items()],
    }
    (OUT / f"{set_dir}.json").write_text(json.dumps(out, indent=2, default=float))
    return out, trailing, baseline


def make_graph(rows):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import plotutil
    except Exception as e:
        print(f"  (graph skipped: {e})")
        return
    plotutil.setup_cjk_font()
    NAVY, AMBER = plotutil.NAVY, plotutil.AMBER
    colors = [NAVY, plotutil.BLUE, AMBER]
    fig, ax = plt.subplots(figsize=(10, 4.2))
    for idx, ((out, trailing, baseline, label), c) in enumerate(zip(rows, colors)):
        t = trailing.dropna()
        x = pd.to_datetime(t.index, format="%Y%m%d")
        ax.plot(x, t.values, color=c, lw=1.6, label=f"{label} (基线 {baseline:.3f})")
        # baseline health lines for the first (production) set only
        if idx == 0:
            ax.axhline(HEALTHY_RATIO * baseline, color="#3a9e5e", lw=0.9, ls="--")
            ax.axhline(WATCH_RATIO * baseline, color=AMBER, lw=0.9, ls="--")
            ax.axhline(0, color="#c0392b", lw=0.9, ls="--")
        # 2026 reading marker
        oos = out.get("latest_oos_2026")
        if oos:
            ax.scatter([pd.Timestamp("2026-03-31")], [oos["ic_mean"]],
                       color=c, s=45, zorder=5, edgecolor="white", lw=0.7)
    ax.text(pd.Timestamp("2026-03-31"), ax.get_ylim()[1] * 0.96, "2026\n样本外",
            fontsize=7.5, ha="center", va="top", color="#555")
    ax.set_title("滚动IC健康监测：中性化复合信号的120日移动IC vs 样本内基线",
                 color=NAVY, fontsize=11.5, pad=8)
    ax.set_ylabel("120日移动 rank IC", fontsize=9.5)
    ax.grid(color="#e8eef7", lw=0.8)
    ax.legend(frameon=False, fontsize=8.5, loc="lower left")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    FIGS.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGS / "fig_ic_monitor.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  saved {FIGS / 'fig_ic_monitor.png'}")


def main(only=None):
    t0 = time.time()
    OUT.mkdir(parents=True, exist_ok=True)
    panel = Panel()
    mask = panel.universe_mask("all")
    label = panel.label(cfg.HORIZON)
    sets = [s for s in SETS if only is None or s[0] == only or s[1] == only]

    rows, summary = [], {}
    for arg, set_dir, cn in sets:
        out, trailing, baseline = monitor_set(arg, set_dir, panel, mask, label, t0)
        rows.append((out, trailing, baseline, cn))
        summary[set_dir] = {
            "baseline_is_ic": out["baseline_is_ic"],
            "current_historical_state": out["current_historical"]["state"],
            "current_historical_ic": out["current_historical"]["trailing_ic"],
            "latest_oos_2026_state": (out["latest_oos_2026"] or {}).get("state"),
            "latest_oos_2026_ic": (out["latest_oos_2026"] or {}).get("ic_mean"),
            "first_watch_breach": out["first_watch_breach"],
        }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, default=float))
    make_graph(rows)

    print("\n=== IC decay monitor ===")
    print(f"{'set':22} {'baseline':>9} {'hist_trail':>11} {'state':>10} "
          f"{'2026_IC':>8} {'2026_state':>11}")
    for arg, set_dir, cn in sets:
        s = summary[set_dir]
        print(f"{set_dir:22} {s['baseline_is_ic']:>9.4f} "
              f"{s['current_historical_ic']:>11.4f} {s['current_historical_state']:>10} "
              f"{(s['latest_oos_2026_ic'] or float('nan')):>8.4f} "
              f"{str(s['latest_oos_2026_state']):>11}")
    print(f"\ndone [{time.time()-t0:.0f}s] -> {OUT}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
