#!/usr/bin/env python3
"""Turnover-overlay figure: net-of-cost excess and turnover vs buffer width."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import plotutil

ROOT = Path(__file__).resolve().parents[1]
plotutil.setup_cjk_font()
NAVY, BLUE, AMBER, RED = plotutil.NAVY, plotutil.BLUE, plotutil.AMBER, plotutil.RED

d = json.loads((ROOT / "results/mining/sets/robust_2026/turnover_overlay.json").read_text())
rows = d["rows"]
b = [r["buffer"] for r in rows]

fig, ax = plt.subplots(figsize=(8.4, 4.6))
ax.plot(b, [r["excess_gross_ann"] * 100 for r in rows], "-o", color=NAVY, lw=1.8, ms=4, label="毛超额")
ax.plot(b, [r["excess_net_15bp_ann"] * 100 for r in rows], "-o", color=BLUE, lw=1.8, ms=4, label="净超额 @15bp")
ax.plot(b, [r["excess_net_30bp_ann"] * 100 for r in rows], "-o", color=AMBER, lw=1.8, ms=4, label="净超额 @30bp")
ax.set_xlabel("缓冲带宽度 (× 分位宽; 1.0 = 无缓冲)", fontsize=10)
ax.set_ylabel("多头超额 年化 (%)", fontsize=10)
ax.set_title("换手缓冲带：净超额随缓冲带提升（robust_2026, 全期）", color=NAVY, fontsize=12, pad=8)
ax.grid(color="#eef2f8", lw=0.7)
ax.legend(frameon=False, fontsize=9, loc="center right")
ax2 = ax.twinx()
ax2.plot(b, [r["avg_turnover"] for r in rows], "--s", color=RED, lw=1.4, ms=3, label="换手率")
ax2.set_ylabel("每期换手率", fontsize=10, color=RED)
ax2.tick_params(axis="y", labelcolor=RED)
ax2.set_ylim(0, 0.5)
for sp in ("top",):
    ax.spines[sp].set_visible(False)
best = max(rows, key=lambda r: r["excess_net_15bp_ann"])
ax.axvline(best["buffer"], color="#999", lw=0.8, ls=":")
ax.text(best["buffer"], ax.get_ylim()[0] + 0.4, f"  最优@15bp\n  缓冲{best['buffer']:.1f}", fontsize=8, color="#555")
fig.tight_layout()
p = ROOT / "results/mining/figs/fig_turnover_overlay.png"
fig.savefig(p, dpi=150, bbox_inches="tight")
print("saved", p)
