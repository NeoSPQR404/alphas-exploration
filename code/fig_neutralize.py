#!/usr/bin/env python3
"""Neutralization/filter comparison figure."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
for p in ("/System/Library/Fonts/Hiragino Sans GB.ttc", "/System/Library/Fonts/STHeiti Medium.ttc"):
    if Path(p).exists():
        fm.fontManager.addfont(p)
        matplotlib.rcParams["font.family"] = fm.FontProperties(fname=p).get_name()
        break
matplotlib.rcParams["axes.unicode_minus"] = False
NAVY, BLUE, AMBER, GREY = "#1a2b4a", "#2e5b9e", "#e08a1e", "#8a8a8a"
FIGS = ROOT / "results" / "mining" / "figs"
sets = [("behavioral_full", "行为全量集"), ("canonical", "规范价量集"), ("canonical_composite", "规范复合集")]
variants = [("raw", "原始"), ("filtered", "筛选"), ("neutralized", "中性化"), ("filt_neutral", "筛选+中性化")]
vcol = [GREY, AMBER, BLUE, NAVY]
D = {s: json.loads((ROOT / "results" / "mining" / "sets" / s / "neutralize_eval.json").read_text()) for s, _ in sets}

fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.6))
x = np.arange(3); w = 0.2
for j, (v, vl) in enumerate(variants):
    axes[0].bar(x + (j - 1.5) * w, [D[s]["variants"][v]["y2026"]["ls_gross_ann"] * 100 for s, _ in sets], w, label=vl, color=vcol[j], edgecolor="white", lw=0.4)
    axes[1].bar(x + (j - 1.5) * w, [D[s]["variants"][v]["full"]["long_excess_ann"] * 100 for s, _ in sets], w, label=vl, color=vcol[j], edgecolor="white", lw=0.4)
for ax, ttl, yl in ((axes[0], "2026 多空毛年化：中性化显著减损", "多空毛年化 (%)"),
                    (axes[1], "历史多头超额：中性化无损", "相对股票池年化超额 (%)")):
    ax.axhline(0, color="#444", lw=0.8); ax.set_xticks(x); ax.set_xticklabels([n for _, n in sets], fontsize=8.5)
    ax.set_ylabel(yl, fontsize=9); ax.set_title(ttl, color=NAVY, fontsize=10.5, pad=6)
    ax.grid(axis="y", color="#e8eef7", lw=0.8)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
axes[0].legend(frameon=False, fontsize=8, loc="lower right", ncol=2)
fig.tight_layout(); fig.savefig(FIGS / "fig_neutralize.png", dpi=150, bbox_inches="tight"); plt.close()
print("saved fig_neutralize.png")
