# code/ — pipeline, mining engine, and analysis scripts

## Step-1 data pipeline (build the base panel from tushare)
- `step1_fetch_missing.py` — fetch missing tushare endpoints (resumable).
- `step1_rebuild_panel.py` — threaded panel rebuild (I/O-optimized; use
  this, not a plain tsbarra run).
- `step1_build_base.py` — assemble the mining base + PIT labels.
- `step1_validate_base.py` — sanity checks → `results/step1_*`.
- `step1_audit_dataset.py`, `step1_progress_live.py[.command]` — audit +
  live terminal dashboard.
- `step2_fetch_csi1000.py` — CSI1000 (000852.SH) index_weight fetch.

## Mining engine
- `mining/` — the round-based factor-mining package (operators, data
  context, AlphasEval metrics, 4-stage pipeline, registry, memory, round
  runner). See `mining/CLAUDE.md`.

## Analysis scripts (all take a set name arg; "main" = behavioral_full)
- `holdout_eval.py <set>` — the honest test on the 2024–25 holdout.
  **Both holdouts are already spent — rerun only if the user asks.**
- `reevaluate_stage4.py <set>` — re-run the full stage-4 suite for every
  active factor; report-only, never retires.
- `backtest_composite.py <set> [neutral] [buffer=B]` — EW rank-composite
  portfolio backtest, 10-day rebalance, t+1 vwap entry, 15/30bp costs.
  `neutral` = recommended construction (size+industry neutralized + status-only
  investable); `buffer=B` (B>1) = hysteresis turnover overlay (hold names down
  to the top B/Q band). Variants write `backtest_neutral_h{H}_buf{B}.json`. For
  a 20d run set `cfg.HORIZON=20` **before importing** (PERIODS_PER_YEAR is
  module-level).

## Construction / OOS / health artifacts (2026-07)
- `neutralize_eval.py <set>` — size+industry neutralization vs micro-cap
  filter, 4 variants, 2017-25 + 2026 → `NEUTRALIZE_REPORT.md`.
- `meta_composite.py` — cross-set blend of the 3 neutralized composites
  (all sets in one run) → `META_COMPOSITE.md` (negative result).
- `monitor_ic.py [set]` — rolling-IC decay monitor (120d trailing IC vs IS
  baseline, health bands) → `IC_MONITOR.md` + `ic_monitor/<set>.json`.
- `valid_2026_screen.py` — per-factor 2026 screen (valid = IC≥0.03 same-sign;
  efficient = cost-aware net>0) across all sets → `VALID_2026.md`.
- `turnover_overlay.py <set>` — hysteresis buffer-band sweep (turnover vs
  net-of-cost) → `TURNOVER_OVERLAY.md`.
- `walkforward.py` — expanding-window walk-forward of factor selection (bias-free
  OOS IC, ~10% haircut) → `WALKFORWARD.md`.
- `blend_behavioral_value.py` — behavioral×value blend sweep (negative: value
  doesn't diversify) → `BLEND_BEHAVIORAL_VALUE.md`.
- `build_robust_2026_set.py` — one-off builder of the curated robust_2026 set.
- `backtest_2026.py`, `analysis_for_report.py` — 2026 OOS backtest + analysis.
- `make_graphs.py`, `fig_*.py`, `make_report.py` — report figures + the
  comprehensive Chinese PDF (`因子挖掘研究报告.pdf`). `plotutil.py` = shared
  CJK-font + palette for all figure scripts.

The construction layer lives in `mining/construct.py` (neutralize, composite,
`set_composite`, investable mask); these scripts route through it. Network calls
(step1/step2) need the Bash sandbox disabled and polite rate limits. Analysis
scripts are long (I/O-bound, minutes–1h): run in background.
