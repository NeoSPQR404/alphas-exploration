# code/mining/ — the factor-mining engine

Round-based Retrieve → Generate → Evaluate → Distill loop. Entry point:
`round.py`.

| module | role |
|---|---|
| `operators.py` | Wide-frame (date × ts_code) operator library: Calculation, Time-Series, Cross-Section, Difference, Correlation, Smooth, Regression. NaN-safe, no lookahead, no `fillna(0)`. `OPERATORS` dict is the expression sandbox namespace. |
| `data.py` | `Panel`: pivots base-panel fields into cached wide frames (`data/_wide_cache/`). `FIELD_MAP` (OHLCV/vwap/turnover/…), `EXT_FIELDS` (moneyflow/northbound/margin flow fields), derived EP/BP/SP/CFP, `INDUSTRY`, `fwd_ret_*` labels, per-universe masks (full-A / HS300 / CSI500 / CSI1000). |
| `alphaseval.py` | AlphasEval metrics: rank IC/ICIR, decile spreads, turnover, decay, coverage, PPS/RRE/PFS/diversity, `rolling_ic_consistency`, `block_bootstrap_pvalue`, `cost_aware` (net-of-turnover long-excess/LS), and `window_backtest` (shared window-sliced decile backtester used by the evals). |
| `pipeline.py` | `compute_factor` (sandboxed eval + AST field-whitelist enforcement) and the 4 gates. `stage4_coverage` runs all 6 sub-tests (OOS · sub-universe · yearly sign · rolling · bootstrap · **decile-monotonicity**). |
| `construct.py` | **Portfolio-construction layer — single source of truth.** `neutralize`/`neutralize_factor` (per-date residual on [SW-L1 industry, log circ_mv]), `oriented_composite` (EW/weighted mean of oriented pct ranks), `set_composite` (a registry → oriented composite, from `stored` values or `expr`), `investable_mask` (config-driven; status-only by default, opt-in micro-cap size cut). Shared by the gates and every eval script. |
| `config.py` | **All thresholds live here.** HORIZON, window dates, S1–S4 gate values incl. rolling (120/20/0.70), bootstrap (B=1000/block=10/seed=11/p≤0.05), and monotonicity (≥0.60). `GATE_ON_NEUTRALIZED` (default True) routes S1/S4 scoring through the neutralized signal; `FILTER_*` control the investable mask; `COST_BPS`/`SCORING_COST_BP` + `GATE_ON_NET_COST` (default **off**) control cost-aware scoring. Do not change without user direction. |
| `registry.py` | `Registry(set_name)`: per-set alpha_set.json + values dir + name prefix (`alpha`/`calpha`/`cxalpha`). Retire-never-delete; ETIMEDOUT read-retry; float32 values. |
| `memory.py` | `Memory(set_name)`: per-set experience_memory.json (schema v2). Patterns carry {name, description, template, occurrence_count, accept_count, success_rate, classification}. `merge()` is the single upsert path — accumulates stats and re-classifies (success ≥0.40 rate & ≥3 occ; forbidden ≤0.15 & ≥4; else undetermined; `add_success/add_forbidden` pin curated narrative patterns). `insight()`/`record_insight()` register + auto-promote new factor ideas. `generation_plan(n)` balances a round's budget across exploit(success)/probe(undetermined)/explore(insight), adapting to the recent accept rate, and returns an avoid-list of forbidden patterns. Rebuild from round JSONs with `code/rebuild_memory.py`. |
| `round.py` | Runner. Reads `CANDIDATES`, optional `SET_NAME`/`FIELD_WHITELIST` from the candidates file; runs 4 stages; writes registry, per-round JSON, holdout snapshot; persists ONLY at completion (killed runs leave clean state). When `GATE_ON_NEUTRALIZED`, S1/S4 score the neutralized factor while raw values feed the correlation gates and registry. |

`"main"` set → `sets/behavioral_full/` paths. Read the set's
experience_memory.json before generating candidates.
