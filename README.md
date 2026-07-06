# alphas-exploration

Mining efficient, tradable alpha factors for the **full A-share universe,
2017–2025**, on a local tushare data panel. Successor to the gtja191
replication work (those 191 alphas have largely decayed post-2017); the goal
here is new factors that hold up out-of-sample in the 2017–2025 window.

## Plan

1. **Data** (done — see [docs/STEP1_DATA_AUDIT.md](docs/STEP1_DATA_AUDIT.md)):
   audit the local tushare dataset, fill the gaps (tradability, flows,
   benchmark), clean it into a mining base with point-in-time labels.
2. **Mining**: ML / NN factor mining on the base panel, evaluated with
   AlphasEval (IC/ICIR, quantile spreads, turnover, decay).
3. **Validation**: strict 2017–2021 train / 2022–2025 OOS discipline,
   tradability-aware backtests, comparison against the gtja191 baseline.

## Layout

```
code/     step1_* data pipeline scripts (audit, fetch, rebuild, base, validate)
docs/     audit + methodology notes
results/  audit / validation JSON artifacts (small, committed)
data/     LOCAL ONLY (git-ignored): base/year=YYYY/base.parquet mining base
```

The raw tushare data lives in the sibling `tushare-data/` repo (also local
only); scripts here reference it by relative path.

## The mining base

`data/base/year=YYYY/base.parquet` — one row per (ts_code, trade_date) traded,
2017–2025: 10.6M rows × 89 cols. All 66 panel columns (OHLCV, adjustment,
valuation, PIT TTM fundamentals, guidance, CSI300 bench) plus derived vwap /
hfq prices, tradability flags (limit hits, one-word boards, ST, days on
market, board), SW L1 industry, and suspension-aware forward-return labels
(`fwd_ret_{1,5,10,20}d`, entry at t+1 vwap) with a `tradable_entry` mask.

Rebuild from scratch:

```bash
python3 code/step1_fetch_missing.py    # missing endpoints (resumable)
python3 code/step1_rebuild_panel.py    # tushare panel, I/O-optimized
python3 code/step1_build_base.py       # mining base + labels
python3 code/step1_validate_base.py    # sanity checks
python3 code/step1_progress_live.py    # live terminal dashboard
```
