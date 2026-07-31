# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Alpha-factor mining for the full A-share universe, 2017–2026 (2026 = the
fresh out-of-sample window), on a local tushare panel. A round-based
Retrieve → Generate → Evaluate → Distill loop
produces factors that live in independent **sets**, each with its own
registry, experience memory, per-round reports, and evaluation artifacts.
Per-folder `CLAUDE.md` files give finer detail (`code/`, `code/mining/`,
`docs/`, `rounds/`, `results/mining/`, and each set folder).

## Commands

```bash
# run one mining round (the core workflow)
python3 code/mining/round.py rounds/<candidates_file>.py

# rebuild v2 pattern statistics from round JSONs (idempotent)
python3 code/rebuild_memory.py

# evaluation / analysis (each takes a set name; "main" = behavioral_full)
python3 code/holdout_eval.py <set>        # 2024–25 honest test (holdout is SPENT — rerun only if asked)
python3 code/reevaluate_stage4.py <set>   # full 5-test stage-4 re-run, report-only (never retires)
python3 code/backtest_composite.py <set> [neutral] [buffer=2.5]  # EW composite backtest; neutral=recommended construction, buffer=turnover overlay
python3 code/walkforward.py                # walk-forward validation of factor selection (bias-free OOS IC)
python3 code/turnover_overlay.py <set>     # hysteresis buffer-band sweep (turnover vs net-of-cost)

# Step-1 data build (rebuilds the base panel from tushare; needs sandbox off)
python3 code/step1_rebuild_panel.py && python3 code/step1_build_base.py && python3 code/step1_validate_base.py
```

There is no test suite; correctness is checked by inline sanity scripts
and the 4-stage evaluation gates. Runs are long (20–60 min): always
`run_in_background` with output to a scratchpad log. The runner persists
state only at round completion, so a killed run leaves the registry clean.

## Architecture — how a round flows

A candidates file (`rounds/<name>_candidates.py`) defines
`CANDIDATES = [{name, expr, family, rationale, logic_score}, ...]` plus
optional `SET_NAME` (default `"main"`) and `FIELD_WHITELIST`. Running it
threads through `code/mining/`:

1. **`data.py` `Panel`** pivots the base panel into wide (date × ts_code)
   frames, cached on disk. Exposes price/volume/valuation fields
   (`FIELD_MAP`), flow fields (`EXT_FIELDS`: moneyflow/northbound/margin),
   derived yields (EP/BP/SP/CFP), `INDUSTRY`, `fwd_ret_*` labels, and
   per-universe masks (full-A / HS300 / CSI500 / CSI1000).
2. **`pipeline.py` `compute_factor`** evaluates each expression in a
   sandbox of `operators.py` operators + panel fields. If a
   `FIELD_WHITELIST` is set it is **AST-enforced** — a canonical candidate
   physically cannot reference turnover/flow/limit fields.
3. The **4 gates** (`pipeline.py`, thresholds in `config.py`) filter
   candidates; `alphaseval.py` computes all metrics (rank IC/ICIR,
   deciles, turnover, decay, rolling-window consistency, block bootstrap).
4. **`registry.py` `Registry(set)`** stores accepted factors
   (retire-never-delete, provenance kept) and their float32 values.
5. **`memory.py` `Memory(set)`** holds experience: statistical patterns +
   curated lessons + exploration insights (see below).
6. `round.py` writes `results/mining/sets/<set>/rounds/round_NN.json` and a
   holdout snapshot, then logs the round into memory.

**The set is the top-level unit.** `Registry("main")`/`Memory("main")`
resolve to `sets/behavioral_full/` (consolidated 2026-07-09; there is no
live copy at the `results/mining/` root). Current sets:

| set | arg | contents |
|---|---|---|
| behavioral_full | `"main"` | 112 factors, full vocabulary (OHLCV, vwap, turnover, VR, amplitude, limit boards, moneyflow, northbound, margin, valuation, industry). Rounds 13-14 added 12; 5 moved to robust_2026. |
| canonical | `"canonical"` | 105 individual factors, **only** OPEN/HIGH/LOW/CLOSE/VOLUME/AMOUNT/VWAP/RET (AST-enforced) |
| canonical_composite | `"canonical_composite"` | 119 rank-product compositions (`cxalpha_` names) of canonical parents |
| robust_2026 | `"robust_2026"` | 25 curated (`ralpha_`): robust in BOTH 2017-25 & 2026, cost-efficient, **non-overnight**. See `results/mining/sets/robust_2026/CLAUDE.md`. |
| value_20d | `"value_20d"` | 4 value/fundamental (`valpha_`) at the **20-day** horizon (gates on fwd_ret_20d; candidates set `cfg.HORIZON=20`). Value is weak at 10d, strong at 20d. See its `CLAUDE.md`. |

## Experience memory (schema v2)

Each set's `experience_memory.json` has a `patterns` dict — every pattern
carries `{name, description, template, occurrence_count, accept_count,
success_rate, classification}` — plus `insights` (exploration ideas).
- `merge()` is the single upsert path: accumulates stats and
  **re-classifies** (success ≥0.40 rate & ≥3 occ; forbidden ≤0.15 & ≥4;
  else undetermined). `add_success`/`add_forbidden` pin curated narrative
  patterns (immune to stat re-classification).
- `insight()` / `record_insight()` register and auto-promote/refute new
  factor ideas from their trial results.
- `generation_plan(n)` balances a round's candidate budget across
  **exploit** (success patterns) / **probe** (undetermined) / **explore**
  (insights), adapting to the recent accept rate, and returns a forbidden
  **avoid-list**. Use it to guide candidate generation.

## Evaluation gates (`config.py` — do not change without user direction)

- Label `fwd_ret_10d` (entry t+1 vwap, suspension-aware), full-A
  `tradable_entry` mask, ≥50 names/date, daily Spearman rank IC.
- Windows: IS 2017–2021 · OOS-gate 2022–2023 · holdout 2024–2025.
- **S1** |IS IC| ≥ 0.03, |ICIR| ≥ 0.30, coverage ≥ 0.60.
- **S2** |corr| < 0.70 vs the set's residents; replace incumbent if ≥1.3× |IS IC|.
- **S3** intra-round dedup at 0.70, keep-best by |ICIR|.
- **S4** (6 tests) OOS same-sign ≥ max(0.03, 0.4×|IS|); ≥2/3 of
  {HS300, CSI500, CSI1000} same-sign ≥0.005; yearly sign-rate ≥0.60;
  rolling 120d/step-20 sign-rate ≥0.70; block bootstrap B=1000, block=10,
  seed=11, one-sided p ≤ 0.05; **decile-monotonicity ≥0.60** same sign
  (Spearman of decile mean-return vs rank, IS+OOS).
- **Construction (2026-07-20):** `GATE_ON_NEUTRALIZED=True` — S1/S4 score
  the size+industry **neutralized** signal (residual alpha), so new rounds
  are judged on residual, not a style tilt; raw values still feed the
  correlation gates and registry. Neutralization/composite/investable-mask
  live in `code/mining/construct.py`. Backtest the recommended construction
  with `python3 code/backtest_composite.py <set> neutral`. Rationale +
  numbers: `results/mining/NEUTRALIZE_REPORT.md`.
- **Cost-aware scoring (2026-07-20):** every factor carries a
  `cost_aware_score` (long-excess net of its own turnover, 15/30bp) in its
  stored metrics + S4. Reported, **not** a hard gate (`GATE_ON_NET_COST=False`):
  single factors are turnover-heavy and mostly fail net>0 standalone, but the
  composite nets +5%/yr — cost binds at the composite, not per factor.
  See `results/mining/COST_ANALYSIS.md`.
- **Turnover buffer overlay (2026-07-21):** `backtest_composite.py <set> neutral
  buffer=B` adds hysteresis (enter in the decile, HOLD until a name falls out of
  the wider `rank>1-B/Q` band). **buffer≈2.5 halves turnover at almost no gross
  cost** (net@30bp +2 to +3.5pp) — the highest-value change after neutralization.
  See `results/mining/TURNOVER_OVERLAY.md`.
- **Deployable book:** robust_2026 → neutralized → status-only universe → EW
  top-decile → buffer 2.5 → 10d = ~+9%/yr excess, IR 1.69, net@15bp +15%,
  turnover 0.25. 10d beats 20d for behavioral (fast/reversal edge).
- **Walk-forward validated (2026-07-21):** the selection process generalizes —
  OOS IC is 88-97% of in-sample (~10% haircut), positive in all 7 test years;
  bias-free forward IC ≈ 0.06-0.07 (contrast the selection-inflated robust_2026
  2026 number). `results/mining/WALKFORWARD.md`.

## Round checklist (never skip a step)

run round → distill into the set's memory (`add_success`/`add_forbidden`,
`record_insight` for any insight trialed) → write `round_NN.md` (funnel,
accepted table with IS/OOS IC+ICIR, rejection tiers, distilled lessons,
**all evaluation parameters displayed in full**) → commit + push. One
commit per round.

## Hard invariants

- **The 2024–25 holdout is SPENT for behavioral_full and canonical**
  (read once each, 2026-07-08/09). Never gate, tune, or distill against
  it. Factors accepted after those reads are not holdout-tested.
- Factor direction is stored per entry; gates use |IC| with
  sign-consistency. Never delete registry entries — retire with provenance.
- Read the set's memory BEFORE generating candidates. Distilled laws:
  novelty = an untouched structural CLASS, not new formulas in old
  classes; jitter thresholds not just windows; magnitude-on-type >
  count-of-type; monotone transforms of residents corr-lock (assume >0.7);
  compositions — pairs negative sign, 3-ways positive (parity rule),
  parents below ~0.05 IS IC don't compose.

## Data & storage (this machine)

- Panel: `data/base/year=YYYY/base.parquet` (10.6M rows × 89 cols); wide
  cache `data/_wide_cache/`; factor values `data/mining/alpha_values*/`
  (float32, git-ignored, rebuildable from expressions).
- **Wide-cache staleness gotcha:** `data/_wide_cache/*.parquet` are NOT
  auto-invalidated when the base gains a new year. Extending to 2026 refreshed
  only the daily-field caches; fundamentals/valuations/labels
  (`total_mv`, `n_income_attr_p_ttm`, `pb`, `fwd_ret_{1,5,20}d`, `bench_close`,
  `EXT_MF_*`) stayed frozen at the prior year-end → EP/CFP silently NaN in the
  new year. After adding a year, delete any cache whose max index < the new
  year (they rebuild from base). Fixed 2026-07-21.
- **`data/` is a symlink to `~/quant_local/alphas-exploration/data`** —
  moved off the iCloud-synced Desktop after "Optimize Mac Storage" evicted
  files mid-run. `TimeoutError [Errno 60]` on a parquet read = eviction;
  fix with `brctl download <path>`. Never relocate data back under
  Desktop/Documents. `data_icloud_backup/` on Desktop is disposable.
- Raw tushare data lives in the sibling `../tushare-data/` repo. Network
  calls (step1/step2) need the Bash sandbox disabled and polite rate limits.

## Git

Remote `github.com:NeoSPQR404/alphas-exploration` (lowercase; old
capitalized URL redirects). Commit and push after every round/step. If a
push is rejected, inspect remote commits before merging — the user
sometimes edits via the GitHub web UI.
