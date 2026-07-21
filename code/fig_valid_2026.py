#!/usr/bin/env python3
"""Scatter of the 2026 per-factor screen: 2026 signed IC (validity) vs 2026
long-excess net of turnover cost (efficiency). Quadrant = valid & efficient."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import plotutil

ROOT = Path(__file__).resolve().parents[1]
plotutil.setup_cjk_font()
GREEN, AMBER, BLUE, GREY = "#3a9e5e", plotutil.AMBER, plotutil.BLUE, plotutil.GREY

d = json.loads((ROOT / "results" / "mining" / "valid_2026_screen.json").read_text())
rows = [r for r in d["all_factors"] if np.isfinite(r["net_excess_15bp_2026"])
        and np.isfinite(r["signed_ic_2026"])]
icmin = d["ic_min"]


def colour(r):
    if r["valid"] and r["efficient"]:
        return GREEN
    if r["valid"]:
        return AMBER
    if r["efficient"]:
        return BLUE
    return GREY


fig, ax = plt.subplots(figsize=(9, 5.4))
xs = [r["signed_ic_2026"] for r in rows]
ys = [min(r["net_excess_15bp_2026"] * 100, 60) for r in rows]   # clip for view
cs = [colour(r) for r in rows]
ax.scatter(xs, ys, c=cs, s=26, alpha=0.8, edgecolor="white", lw=0.3)
ax.axvline(icmin, color="#888", lw=0.9, ls="--")
ax.axvline(0, color="#ccc", lw=0.8)
ax.axhline(0, color="#888", lw=0.9, ls="--")
ax.set_xlim(-0.06, 0.11)
ax.set_xlabel("2026 有效性：方向化 rank IC（≥0.03 且同号 = 有效）", fontsize=10)
ax.set_ylabel("2026 效率：多头超额 扣15bp换手成本 年化 (%)", fontsize=10)
ax.set_title("2026 逐因子筛选：有效性 × 效率（绿=两者兼备 29 个）",
             color=plotutil.NAVY, fontsize=12.5, pad=8)
# annotate the top overnight-gap alpha
top = max(rows, key=lambda r: r["net_excess_15bp_2026"])
ax.annotate("隔夜跳空持续\nOPEN/Delay(CLOSE,1)-1", xy=(top["signed_ic_2026"], 46.6),
            xytext=(0.055, 40), fontsize=8, color=plotutil.NAVY,
            arrowprops=dict(arrowstyle="->", color="#888", lw=0.8))
handles = [plt.Line2D([], [], marker="o", ls="", mfc=c, mec="white", ms=8, label=l)
           for c, l in [(GREEN, "有效+高效 (29)"), (AMBER, "仅有效 (82)"),
                        (BLUE, "仅高效 (5)"), (GREY, "两者皆非")]]
ax.legend(handles=handles, frameon=False, fontsize=8.5, loc="upper left")
ax.grid(color="#eef2f8", lw=0.7)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
fig.tight_layout()
FIGS = ROOT / "results" / "mining" / "figs"
fig.savefig(FIGS / "fig_valid_2026.png", dpi=150, bbox_inches="tight")
print("saved", FIGS / "fig_valid_2026.png")
