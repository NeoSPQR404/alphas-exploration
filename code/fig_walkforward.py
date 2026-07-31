#!/usr/bin/env python3
"""Walk-forward figure: per-year IS vs OOS IC, and OOS IC / haircut vs K."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import plotutil

ROOT = Path(__file__).resolve().parents[1]
plotutil.setup_cjk_font()
NAVY, BLUE, AMBER, RED = plotutil.NAVY, plotutil.BLUE, plotutil.AMBER, plotutil.RED
d = json.loads((ROOT / "results/mining/walkforward.json").read_text())

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.3))

# panel 1: per-year IS vs OOS IC (K=30)
r30 = [x for x in d["per_year"] if x["K"] == 30]
yrs = [x["test_year"] for x in r30]
x = np.arange(len(yrs)); w = 0.38
ax1.bar(x - w / 2, [r["is_ic"] for r in r30], w, color=NAVY, label="样本内 (训练期)")
ax1.bar(x + w / 2, [r["oos_ic"] for r in r30], w, color=AMBER, label="样本外 (测试年)")
ax1.set_xticks(x); ax1.set_xticklabels(yrs, fontsize=9)
ax1.set_ylabel("方向化 rank IC", fontsize=9.5)
ax1.set_title("逐年 样本内 vs 样本外 IC (选Top30)", color=NAVY, fontsize=11, pad=6)
ax1.legend(frameon=False, fontsize=8.5, loc="lower right")
ax1.grid(axis="y", color="#eef2f8", lw=0.7)

# panel 2: OOS IC and haircut vs K
by_k = d["by_K"]
ks = sorted(int(k) for k in by_k)
oos = [by_k[str(k)]["mean_oos_ic"] for k in ks]
iss = [by_k[str(k)]["mean_is_ic"] for k in ks]
ax2.plot(range(len(ks)), iss, "-o", color=NAVY, lw=1.6, ms=4, label="样本内 IC")
ax2.plot(range(len(ks)), oos, "-o", color=AMBER, lw=1.8, ms=4, label="样本外 IC")
ax2.set_xticks(range(len(ks))); ax2.set_xticklabels([str(k) for k in ks], fontsize=9)
ax2.set_xlabel("选取因子数 K (最后=全部)", fontsize=9.5)
ax2.set_ylabel("平均 IC (7个测试年)", fontsize=9.5)
ax2.set_title("选择增益：Top-K 样本外IC vs 全部", color=NAVY, fontsize=11, pad=6)
ax2.legend(frameon=False, fontsize=8.5)
ax2.grid(color="#eef2f8", lw=0.7)
for ax in (ax1, ax2):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
fig.text(0.5, -0.02, "样本外IC达样本内约88-97%(仅约10%缩水)，7/7测试年为正；选Top因子(OOS 0.070)优于全部(0.049)=选择有效非噪声。",
         ha="center", fontsize=7.5, color="#777")
fig.tight_layout()
p = ROOT / "results/mining/figs/fig_walkforward.png"
fig.savefig(p, dpi=150, bbox_inches="tight")
print("saved", p)
