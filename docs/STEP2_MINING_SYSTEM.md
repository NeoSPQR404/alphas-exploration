# Step 2 — Repeatable factor-mining system

Implements the factor-mining loop from the mining prompt: a round-based
Retrieve → Generate → Evaluate → Distill cycle over the Step-1 base panel
(full A-share, 2017–2025, suspension-aware labels).

## Components (`code/mining/`)

| Module | Role |
|---|---|
| `operators.py` | Operator set on wide (date × stock) frames: Calculation (Log, Sign, SignedPower, …), Time-Series (TsMean/Std/Skew/Kurt/Med/Rank/Max/Min, HighDay/LowDay), Cross-Section (CsRank, CsZscore, CsIndNeutralize, …), Difference (Delta, PctChange, Delay), Correlation (TsCorr, TsCov), Smooth (SMA, EMA, WMA, DecayLinear), Regression (TsSlope, TsRSquare, TsResi, RegBeta, RegResi). NaN-safe, no lookahead, no `fillna(0)`. |
| `data.py` | `Panel`: pivots base-panel fields into cached wide frames (`data/_wide_cache/`), exposes hfq prices, turnover, valuation, PIT yield fields (EP/BP/SP/CFP), SW L1 industry, `fwd_ret_{h}d` labels, and universe masks (full-A `tradable_entry`, HS300 / CSI500 / CSI1000 from tushare `index_weight` monthly snapshots, forward-filled). |
| `alphaseval.py` | AlphasEval metrics. Practical: daily rank IC, ICIR, t-stat, decile returns + long-short spread, rank-autocorrelation turnover, decay profile (1/5/10/20d), coverage. AlphaEval-paper dimensions (arXiv 2508.13174, reimplemented from the Qlib reference in `../alphaeval-reference/`): PPS, RRE (rank-distribution KL stability), PFS (Gaussian + t(3) multiplicative noise, variance calibrated to the min-max-normalized CSI300 close over the IS window), diversity eigen-entropy at set level. Logic score is assigned by the mining agent. |
| `pipeline.py` | The 4 evaluation gates + expression sandbox (`compute_factor` evaluates candidate expressions in a namespace of operators + panel fields, then MAD-winsorizes). |
| `registry.py` | Alpha factor set: `results/mining/alpha_set.json` (+ CSV export); factor values under `data/mining/alpha_values/` (local, rebuildable). |
| `memory.py` | Experience memory: `results/mining/experience_memory.json`, successful / forbidden patterns with evidence and per-round strength. |
| `round.py` | Round runner: `python3 code/mining/round.py rounds/roundNN_candidates.py`. |

## Evaluation design

- **Label**: `fwd_ret_10d` (entry t+1 vwap, suspension-aware), evaluated on
  `tradable_entry`-masked cross-sections (≥50 names/date).
- **Windows**: IS 2017–2021 (stages 1–3), OOS-gate 2022–2023 (stage 4),
  **final holdout 2024–2025** — computed for accepted factors, written to
  `results/mining/holdout/`, never used for accept/reject and never
  distilled into memory, so repeated rounds don't burn it.
- **Direction**: factors may carry negative IC; the sign is recorded as
  `direction` and gates use |IC| with sign-consistency requirements.

### The 4 gates (thresholds in `config.py`)

1. **Quick IC screen** — IS full-A: |rank IC| ≥ 0.02, |ICIR| ≥ 0.30,
   coverage ≥ 60%.
2. **Alpha-set correlation** — mean cross-sectional Spearman correlation of
   factor values vs every accepted factor < 0.70; exemption: if the new
   factor's |IS IC| ≥ 1.3× the incumbent's, it **replaces** the incumbent
   (retired with provenance).
3. **Duplication removal** — same 0.70 rule pairwise within the round,
   greedy keep-best by |ICIR|.
4. **Coverage test** — (a) OOS 2022–2023 full-A IC same sign and
   |OOS IC| ≥ max(0.01, 0.4×|IS IC|); (b) ≥2 of {HS300, CSI500, CSI1000}
   with same-sign IC ≥ 0.005 over 2017–2023; (c) ≥60% of 2017–2023 years
   with same-sign yearly IC.

## One round

1. **Retrieve** — read `experience_memory.json` (successful / forbidden
   patterns).
2. **Generate** — the mining agent writes `rounds/roundNN_candidates.py`
   with `CANDIDATES = [{name, expr, family, rationale, logic_score}, …]`,
   biased toward successful patterns, avoiding forbidden ones.
3. **Evaluate** — `python3 code/mining/round.py rounds/roundNN_candidates.py`
   runs the gates, updates the registry, writes
   `results/mining/rounds/round_NN.json` and the holdout file.
4. **Distill** — the agent writes successes/failures back into memory
   (patterns, not per-factor OOS tuning) and commits.

## Base extension: flow fields (added after Round 5)

`data.py` exposes seven expression-visible fields built lazily from the
raw tushare endpoint dirs (threaded reads, cached as `EXT_*.parquet` in
`_wide_cache/`):

| field | source | definition |
|---|---|---|
| `MF_LG_NET` | moneyflow | (buy_lg+buy_elg − sell_lg − sell_elg) / total two-sided amount |
| `MF_SM_NET` | moneyflow | (buy_sm − sell_sm) / total (retail direction) |
| `MF_NET` | moneyflow | net_mf_amount / total |
| `HK_RATIO` | hk_hold | northbound holding % of shares |
| `RZ_MV` | margin_detail | financing balance / circulating MV |
| `RQ_MV` | margin_detail | short balance / circulating MV |
| `RZ_NET` | margin_detail | daily net financing buys / circulating MV |

Validation (full-A tradable cells): MF_* coverage 0.98, fully nonzero;
HK_RATIO / RZ_* are 0-filled where a stock is not connect/margin eligible
(economically a true zero), so coverage is 1.00 with 38–49% nonzero.
Timing: moneyflow derives from day-T trades (known at T close); northbound
holdings and margin balances for day T are published before T+1 open —
compatible with labels entering at T+1 vwap.

## Known caveats

- Stage-4 reuses 2022–2023 every round, so that window degrades as a true
  OOS test over many rounds; the 2024–2025 holdout is the honest number.
- Overlapping daily ICs at a 10-day horizon inflate t-stats; decile
  spreads are computed on non-overlapping (every 10th day) rebalances.
- `index_weight` membership is monthly snapshots forward-filled, so
  intra-month index changes lag by up to a month.
