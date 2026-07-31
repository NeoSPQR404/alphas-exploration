#!/usr/bin/env python3
"""Capacity curve: net long-excess vs AUM, with impact sensitivity band."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import plotutil

ROOT = Path(__file__).resolve().parents[1]
plotutil.setup_cjk_font()
NAVY, BLUE, AMBER, RED, GREY = plotutil.NAVY, plotutil.BLUE, plotutil.AMBER, plotutil.RED, plotutil.GREY
d = json.loads((ROOT / "results/mining/capacity_model.json").read_text())
curve = d["curve"]
aums = sorted(float(a) for a in curve)
base = [curve[f"{a:.0f}"]["base"] * 100 for a in aums]
opt = [curve[f"{a:.0f}"]["optimistic"] * 100 for a in aums]
pess = [curve[f"{a:.0f}"]["pessimistic"] * 100 for a in aums]
x = [a / 1e8 for a in aums]           # 亿 CNY

fig, ax = plt.subplots(figsize=(8.6, 4.8))
ax.fill_between(x, opt, pess, color=BLUE, alpha=0.15, label="乐观-悲观冲击区间")
ax.plot(x, base, "-o", color=NAVY, lw=2, ms=4, label="基准冲击 (Y=120bp)")
ax.axhline(0, color=RED, lw=1, ls="--")
ax.axhline(d["small_aum_net"] * 100 / 2, color=GREY, lw=0.9, ls=":")
ax.text(x[0], d["small_aum_net"] * 100 / 2 + 0.3, "半衰alpha线", fontsize=7.5, color="#666")
ax.axhline(d["gross_excess_ann"] * 100, color="#3a9e5e", lw=0.9, ls="--")
ax.text(x[0], d["gross_excess_ann"] * 100 + 0.3, f"无摩擦毛超额 {d['gross_excess_ann']*100:.1f}%", fontsize=7.5, color="#3a9e5e")
if d.get("half_capacity_cny"):
    hc = d["half_capacity_cny"] / 1e8
    ax.axvline(hc, color=AMBER, lw=0.9, ls=":")
    ax.text(hc * 1.05, min(base) + 2, f"半衰容量\n约{hc:.0f}亿", fontsize=8, color=AMBER)
ax.set_xscale("log")
ax.set_xlabel("管理规模 AUM (亿元, 对数轴)", fontsize=10)
ax.set_ylabel("多头净超额 年化 (%)", fontsize=10)
ax.set_title("容量曲线：净超额随规模衰减（robust_2026 中性化+缓冲2.5, 长多）",
             color=NAVY, fontsize=12, pad=8)
ax.grid(color="#eef2f8", lw=0.7, which="both")
ax.legend(frameon=False, fontsize=8.5, loc="upper right")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.text(0.5, -0.02, "平方根冲击 impact=Y*sqrt(成交/ADV)；固定成本 佣金2.5+价差5+印花5(卖)bp。容量受小盘持仓限制。",
         ha="center", fontsize=7.5, color="#777")
fig.tight_layout()
p = ROOT / "results/mining/figs/fig_capacity.png"
fig.savefig(p, dpi=150, bbox_inches="tight")
print("saved", p)
