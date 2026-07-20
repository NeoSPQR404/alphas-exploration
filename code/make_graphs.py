#!/usr/bin/env python3
"""Render the report's figures as PNGs into results/mining/figs/."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SETS = Path(ROOT, "results", "mining", "sets")
FIGS = Path(ROOT, "results", "mining", "figs"); FIGS.mkdir(parents=True, exist_ok=True)

# CJK font
for p in ("/System/Library/Fonts/Hiragino Sans GB.ttc",
          "/System/Library/Fonts/STHeiti Medium.ttc"):
    if Path(p).exists():
        fm.fontManager.addfont(p)
        matplotlib.rcParams["font.family"] = fm.FontProperties(fname=p).get_name()
        break
matplotlib.rcParams["axes.unicode_minus"] = False
plt.rcParams.update({"figure.dpi": 150, "savefig.dpi": 150, "font.size": 11,
                     "axes.edgecolor": "#c9d3e0", "axes.linewidth": 0.8})

NAVY, BLUE, AMBER, RED, GREY = "#1a2b4a", "#2e5b9e", "#e08a1e", "#b3261e", "#8a8a8a"
NAMES = {"behavioral_full": "行为全量集", "canonical": "规范价量集",
         "canonical_composite": "规范复合集"}
COL = {"behavioral_full": BLUE, "canonical": AMBER, "canonical_composite": RED}
ORDER = ["behavioral_full", "canonical", "canonical_composite"]


def load(s, name):
    return json.loads(Path(SETS, s, name).read_text())


# ---------- 1. 2026 decile inversion (hero) ----------
def fig_decile():
    fig, ax = plt.subplots(figsize=(7.4, 3.5))
    x = np.arange(10); w = 0.26
    for i, s in enumerate(ORDER):
        d = load(s, "backtest_2026.json")["decile_mean_period_ret"]
        ax.bar(x + (i - 1) * w, [v * 100 for v in d], w, label=NAMES[s],
               color=COL[s], edgecolor="white", linewidth=0.4)
    ax.axhline(0, color="#444", lw=0.8)
    ax.set_xticks(x); ax.set_xticklabels([f"D{i+1}" for i in range(10)])
    ax.set_ylabel("每组 10 日平均收益 (%)")
    ax.set_title("2026 分组收益：模型评分越低反而收益越高（倒挂）", color=NAVY, fontsize=12, pad=8)
    ax.text(0.5, 0.92, "D1 = 模型最不看好   →   D10 = 最看好", transform=ax.transAxes,
            ha="center", color=GREY, fontsize=9)
    ax.legend(frameon=False, fontsize=9, loc="upper right")
    ax.grid(axis="y", color="#e8eef7", lw=0.8)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    fig.tight_layout(); fig.savefig(FIGS / "fig_decile_2026.png", bbox_inches="tight"); plt.close()


# ---------- 2. composite IC trajectory ----------
def fig_ic():
    an = json.loads(Path(ROOT, "results", "mining", "analysis_2026.json").read_text())
    wins = ["is", "oos_gate", "holdout", "y2026"]
    wl = ["样本内\n2017–21", "样本外门槛\n2022–23", "留出\n2024–25", "样本外真检验\n2026"]
    fig, ax = plt.subplots(figsize=(7.4, 3.6))
    akey = {"behavioral_full": "main", "canonical": "canonical",
            "canonical_composite": "canonical_composite"}
    for s in ORDER:
        vals = [an[akey[s]]["ic_by_window"][w] for w in wins]
        ax.plot(range(4), vals, "-o", color=COL[s], lw=2, ms=6, label=NAMES[s])
    ax.axhline(0, color="#444", lw=0.9)
    ax.set_xticks(range(4)); ax.set_xticklabels(wl, fontsize=9)
    ax.set_ylabel("等权合成组合日度秩 IC")
    ax.set_ylim(bottom=0)
    ax.set_title("复合日度秩 IC 轨迹：2026 显著衰减但仍为弱正（约历史一半）", color=NAVY, fontsize=12, pad=8)
    ax.legend(frameon=False, fontsize=9, loc="lower left")
    ax.grid(axis="y", color="#e8eef7", lw=0.8)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    fig.tight_layout(); fig.savefig(FIGS / "fig_ic_trajectory.png", bbox_inches="tight"); plt.close()


# ---------- 3. historical long-only cumulative (equity curve) ----------
def fig_equity_hist():
    fig, ax = plt.subplots(figsize=(7.4, 3.6))
    years = [str(y) for y in range(2017, 2026)]
    for s in ORDER:
        y = load(s, "backtest.json")["yearly"]
        cum = np.cumprod([1 + y[yr]["long_net_base"] for yr in years])
        ax.plot(years, cum, "-o", color=COL[s], lw=2, ms=4, label=NAMES[s] + " 多头(扣费)")
    # benchmarks from one set (same universe/csi300)
    y = load("canonical", "backtest.json")["yearly"]
    ax.plot(years, np.cumprod([1 + y[yr]["mkt"] for yr in years]), "--", color=GREY, lw=1.5, label="等权股票池")
    ax.plot(years, np.cumprod([1 + y[yr]["csi300"] for yr in years]), ":", color="#555", lw=1.5, label="沪深300")
    ax.set_ylabel("累计净值 (起点=1)")
    ax.set_title("历史多头累计净值 2017–2025（扣双边 15bp）", color=NAVY, fontsize=12, pad=8)
    ax.legend(frameon=False, fontsize=8.5, loc="upper left", ncol=2)
    ax.grid(axis="y", color="#e8eef7", lw=0.8)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    fig.tight_layout(); fig.savefig(FIGS / "fig_equity_hist.png", bbox_inches="tight"); plt.close()


# ---------- 4. historical vs 2026 excess (the punchline) ----------
def fig_contrast():
    fig, ax = plt.subplots(figsize=(7.4, 3.4))
    x = np.arange(3); w = 0.36
    hist = [load(s, "backtest.json")["windows"]["full"]["long_excess_mkt"]["ann_return"] * 100 for s in ORDER]
    y26 = [load(s, "backtest_2026.json")["long_excess_mkt"]["ann_return"] * 100 for s in ORDER]
    b1 = ax.bar(x - w/2, hist, w, label="历史 2017–2025", color=BLUE, edgecolor="white")
    b2 = ax.bar(x + w/2, y26, w, label="样本外 2026", color=RED, edgecolor="white")
    ax.axhline(0, color="#444", lw=0.8)
    ax.set_xticks(x); ax.set_xticklabels([NAMES[s] for s in ORDER])
    ax.set_ylabel("多头相对股票池年化超额 (%)")
    ax.set_title("多头超额收益：历史 vs 2026 样本外", color=NAVY, fontsize=12, pad=8)
    for bars in (b1, b2):
        for r in bars:
            h = r.get_height()
            ax.annotate(f"{h:+.0f}%", (r.get_x() + r.get_width()/2, h),
                        ha="center", va="bottom" if h >= 0 else "top",
                        fontsize=8.5, color="#333")
    ax.legend(frameon=False, fontsize=9)
    ax.grid(axis="y", color="#e8eef7", lw=0.8)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    fig.tight_layout(); fig.savefig(FIGS / "fig_excess_contrast.png", bbox_inches="tight"); plt.close()


# ---------- 5. 2026 cumulative curve (long vs benchmarks) ----------
def fig_equity_2026():
    an = json.loads(Path(ROOT, "results", "mining", "analysis_2026.json").read_text())
    fig, ax = plt.subplots(figsize=(7.4, 3.4))
    for s in ORDER:
        ser = an[{"behavioral_full":"main"}.get(s, s)]["y2026_series"]
        cum = np.cumprod([1 + r["long"] for r in ser])
        ax.plot(range(len(cum)), (cum - 1) * 100, "-o", color=COL[s], lw=2, ms=4, label=NAMES[s] + " 多头")
    ser = an["canonical"]["y2026_series"]
    ax.plot(range(len(ser)), (np.cumprod([1 + r["mkt"] for r in ser]) - 1) * 100, "--", color=GREY, lw=1.5, label="等权股票池")
    ax.axhline(0, color="#444", lw=0.8)
    ax.set_xlabel("2026 调仓期序号（每期 10 交易日）"); ax.set_ylabel("累计收益 (%)")
    ax.set_title("2026 样本外多头累计收益：可交易组合跑输股票池", color=NAVY, fontsize=12, pad=8)
    ax.legend(frameon=False, fontsize=8.5, loc="lower left")
    ax.grid(axis="y", color="#e8eef7", lw=0.8)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    fig.tight_layout(); fig.savefig(FIGS / "fig_equity_2026.png", bbox_inches="tight"); plt.close()


if __name__ == "__main__":
    fig_decile(); print("decile")
    fig_equity_hist(); print("equity_hist")
    fig_contrast(); print("contrast")
    if Path(ROOT, "results", "mining", "analysis_2026.json").exists():
        fig_ic(); print("ic")
        fig_equity_2026(); print("equity_2026")
    print("figs ->", FIGS)
