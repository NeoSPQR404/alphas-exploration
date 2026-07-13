# CLAUDE.md — alphas-exploration

Alpha-factor mining for the full A-share universe, 2017–2025, on a local
tushare panel. Round-based Retrieve → Generate → Evaluate → Distill loop;
factors live in independent **sets**, each with its own registry,
experience memory, rounds, and reports.

## The three sets

| set | registry arg | contents | artifacts |
|---|---|---|---|
| behavioral_full | `"main"` | 105 factors, full field vocabulary (OHLCV, vwap, turnover, VR, amplitude, limit boards, moneyflow, valuation, industry) | `results/mining/sets/behavioral_full/` |
| canonical | `"canonical"` | 105 individual factors, **only** OPEN/HIGH/LOW/CLOSE/VOLUME/AMOUNT/VWAP/RET (AST-enforced) | `results/mining/sets/canonical/` |
| canonical_composite | `"canonical_composite"` | 26 rank-product compositions split from canonical | `results/mining/sets/canonical_composite/` |

`Registry("main")` and `Memory("main")` point at `sets/behavioral_full/`
(consolidated 2026-07-09 — there is no separate live copy at
`results/mining/` root).

## Running a round

```bash
python3 code/mining/round.py rounds/<candidates_file>.py
```

The candidates file defines `CANDIDATES = [{name, expr, family,
rationale, logic_score}, ...]` plus optional `SET_NAME` (default
`"main"`) and `FIELD_WHITELIST` (AST-enforced in `compute_factor`).
Expressions evaluate in a sandboxed namespace of operators
(`code/mining/operators.py`) + panel fields (`code/mining/data.py`
`FIELD_MAP` / `EXT_FIELDS` / derived EP/BP/SP/CFP / `IND`).

**Round checklist (never skip a step):** run round → distill lessons into
the set's experience memory (`Memory(set).add_success/add_forbidden`) →
write `round_NN.md` (funnel, accepted table with IS/OOS IC+ICIR,
rejection tiers by stage, distilled lessons, **all evaluation
parameters displayed**) → commit + push. One commit per round.

## Evaluation gates (config.py — do not change without user direction)

- Label `fwd_ret_10d` (entry t+1 vwap, suspension-aware), full-A
  `tradable_entry` mask, ≥50 names/date, daily Spearman rank IC.
- Windows: IS 2017–2021 · OOS-gate 2022–2023 · holdout 2024–2025.
- S1: |IS IC| ≥ 0.03, |ICIR| ≥ 0.30, coverage ≥ 0.60.
- S2: |corr| < 0.70 vs the set's residents; replacement if ≥ 1.3× |IS IC|.
- S3: intra-round dedup at 0.70, keep-best by |ICIR|.
- S4 (five tests): OOS same-sign ≥ max(0.03, 0.4×|IS|); ≥2/3 of
  {HS300, CSI500, CSI1000} same-sign ≥ 0.005; yearly sign-rate ≥ 0.60;
  rolling 120d/step-20 sign-rate ≥ 0.70; moving-block bootstrap B=1000,
  block=10, seed=11, one-sided p ≤ 0.05.

## Hard invariants

- **The 2024–25 holdout is SPENT for behavioral_full and canonical**
  (read once each, 2026-07-08/09). Never gate, tune, or distill against
  it. Canonical factors accepted after cR10 have not been holdout-tested.
- Factor direction is stored per entry; gates use |IC| with
  sign-consistency. Registries record retired factors with provenance —
  never delete entries, retire them.
- Read the set's `experience_memory.json` BEFORE generating candidates.
  Key distilled laws: novelty = untouched structural CLASS (not new
  formulas in old classes); jitter thresholds not just windows;
  magnitude-on-type > count-of-type; one representative per event type;
  monotone transforms of residents corr-lock (assume >0.7).

## Evaluation / analysis scripts

```bash
python3 code/holdout_eval.py <set>       # honest test (holdout is spent — rerun only if user asks)
python3 code/reevaluate_stage4.py <set>  # full stage-4 re-run, report-only (never retires)
python3 code/backtest_composite.py <set> # EW rank-composite backtest, 10d rebalance, 15/30bp costs
```

## Data & storage (this machine)

- Panel: `data/base/year=YYYY/base.parquet` (10.6M rows × 89 cols); wide
  frames cached in `data/_wide_cache/`; factor values in
  `data/mining/alpha_values*/` (float32, rebuildable from expressions).
- **`data/` is a symlink to `~/quant_local/alphas-exploration/data`** —
  moved off the iCloud-synced Desktop after "Optimize Mac Storage"
  evicted files mid-run (`TimeoutError [Errno 60]` on parquet reads =
  eviction; fix with `brctl download <path>`). Never relocate data back
  under Desktop/Documents. `data_icloud_backup/` on Desktop is
  disposable.
- Raw tushare data lives in the sibling `../tushare-data/` repo. Network
  calls to tushare need the sandbox disabled and polite rate limits.
- Runs are long (20–60 min): always `run_in_background` with output to a
  scratchpad log; the runner only persists state at round completion, so
  a killed run leaves the registry clean.

## Git

Remote: `github.com:NeoSPQR404/alphas-exploration` (lowercase; the old
capitalized URL redirects). Commit and push after every round/step. If a
push is rejected, inspect remote commits before merging — the user
sometimes edits via the GitHub web UI.
