#!/usr/bin/env python3
"""Blend sweep figure: ICIR and long-excess vs value weight (value does not help)."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import plotutil

ROOT = Path(__file__).resolve().parents[1]
plotutil.setup_cjk_font()
d = json.loads((ROOT / "results" / "mining" / "blend_behavioral_value.json").read_text())
g = d["grid"]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
for h, c in [(10, plotutil.NAVY), (20, plotutil.AMBER)]:
    rows = [r for r in g if r["horizon"] == h]
    w = [r["wV"] for r in rows]
    ax1.plot(w, [r["icir"] for r in rows], "-o", color=c, lw=1.8, ms=4, label=f"{h}日")
    ax2.plot(w, [r["excess_ann"] * 100 for r in rows], "-o", color=c, lw=1.8, ms=4, label=f"{h}日")
ax1.set_title(f"风险调整信号质量 ICIR (corr B,V={d['corr_BV']:+.2f})", color=plotutil.NAVY, fontsize=11, pad=6)
ax1.set_ylabel("ICIR (全期 2017-25)", fontsize=9.5)
ax2.set_title("多头超额 年化", color=plotutil.NAVY, fontsize=11, pad=6)
ax2.set_ylabel("超额 年化 (%)", fontsize=9.5)
for ax in (ax1, ax2):
    ax.set_xlabel("价值权重 wV (0=纯行为, 1=纯价值)", fontsize=9.5)
    ax.legend(frameon=False, fontsize=9, title="持有期")
    ax.grid(color="#eef2f8", lw=0.7)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
fig.text(0.5, -0.02, "加入价值(wV>0)在两个持有期均单调降低 ICIR 与超额 → 价值不分散行为组合（IC时序相关约0.71）。",
         ha="center", fontsize=7.5, color="#777")
fig.tight_layout()
p = ROOT / "results" / "mining" / "figs" / "fig_blend.png"
fig.savefig(p, dpi=150, bbox_inches="tight")
print("saved", p)
