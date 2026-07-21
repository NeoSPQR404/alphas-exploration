#!/usr/bin/env python3
"""robust_2026 backtest figure: decile curves (historical + 2026) and the
2026 long-excess comparison vs the source sets."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import plotutil

ROOT = Path(__file__).resolve().parents[1]
S = ROOT / "results" / "mining" / "sets"
plotutil.setup_cjk_font()
NAVY, BLUE, AMBER, RED, GREY = plotutil.NAVY, plotutil.BLUE, plotutil.AMBER, plotutil.RED, plotutil.GREY

bt = json.loads((S / "robust_2026" / "backtest_neutral.json").read_text())
ne = json.loads((S / "robust_2026" / "neutralize_eval.json").read_text())
hist_dec = [x * 100 for x in bt["decile_mean_period_ret"]]
y26_dec = [x * 100 for x in ne["variants"]["neutralized"]["y2026"]["deciles"]]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.3))

# -- panel 1: decile curves
x = np.arange(1, 11)
ax1.plot(x, hist_dec, "-o", color=NAVY, lw=1.8, ms=4, label="历史 2017-25")
ax1.plot(x, y26_dec, "-o", color=AMBER, lw=1.8, ms=4, label="2026 (样本外*)")
ax1.axhline(0, color="#888", lw=0.8)
ax1.set_xticks(x); ax1.set_xlabel("因子分位 (1=低 → 10=高)", fontsize=9.5)
ax1.set_ylabel("每期均值收益 (%)", fontsize=9.5)
ax1.set_title("分位单调性：中性化复合", color=NAVY, fontsize=11, pad=6)
ax1.legend(frameon=False, fontsize=8.5, loc="upper left")
ax1.grid(color="#eef2f8", lw=0.7)

# -- panel 2: 2026 long-excess vs source sets
sets = [("robust_2026", "robust_2026\n(精选)"), ("behavioral_full", "行为全量集"),
        ("canonical", "规范价量集"), ("canonical_composite", "规范复合集")]
vals, cols = [], []
for s, _ in sets:
    e = json.loads((S / s / "neutralize_eval.json").read_text())
    vals.append(e["variants"]["neutralized"]["y2026"]["long_excess_ann"] * 100)
cols = [AMBER, BLUE, GREY, GREY]
bars = ax2.bar(range(len(sets)), vals, color=cols, edgecolor="white", lw=0.5)
ax2.axhline(0, color="#444", lw=0.9)
ax2.set_xticks(range(len(sets))); ax2.set_xticklabels([n for _, n in sets], fontsize=8.5)
ax2.set_ylabel("2026 多头超额 年化 (%)", fontsize=9.5)
ax2.set_title("2026 多头超额：精选 vs 源因子集", color=NAVY, fontsize=11, pad=6)
for b, v in zip(bars, vals):
    ax2.text(b.get_x() + b.get_width() / 2, v + (1.5 if v >= 0 else -3),
             f"{v:+.0f}%", ha="center", fontsize=8.5,
             color=NAVY if v >= 0 else RED)
ax2.grid(axis="y", color="#eef2f8", lw=0.7)
for ax in (ax1, ax2):
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)

fig.text(0.5, -0.02, "* 2026 精选数值受选择偏差影响（24 因子中 19 个按 2026 表现挑选）；前瞻预期应参考历史 +10% 超额。",
         ha="center", fontsize=7.5, color="#777")
fig.tight_layout()
FIGS = ROOT / "results" / "mining" / "figs"
fig.savefig(FIGS / "fig_robust_2026_backtest.png", dpi=150, bbox_inches="tight")
print("saved", FIGS / "fig_robust_2026_backtest.png")
