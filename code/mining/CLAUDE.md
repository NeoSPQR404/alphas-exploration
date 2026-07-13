# code/mining/ — the factor-mining engine

Round-based Retrieve → Generate → Evaluate → Distill loop. Entry point:
`round.py`.

| module | role |
|---|---|
| `operators.py` | Wide-frame (date × ts_code) operator library: Calculation, Time-Series, Cross-Section, Difference, Correlation, Smooth, Regression. NaN-safe, no lookahead, no `fillna(0)`. `OPERATORS` dict is the expression sandbox namespace. |
| `data.py` | `Panel`: pivots base-panel fields into cached wide frames (`data/_wide_cache/`). `FIELD_MAP` (OHLCV/vwap/turnover/…), `EXT_FIELDS` (moneyflow/northbound/margin flow fields), derived EP/BP/SP/CFP, `INDUSTRY`, `fwd_ret_*` labels, per-universe masks (full-A / HS300 / CSI500 / CSI1000). |
| `alphaseval.py` | AlphasEval metrics: rank IC/ICIR, decile spreads, turnover, decay, coverage, PPS/RRE/PFS/diversity, plus `rolling_ic_consistency` and `block_bootstrap_pvalue` (the stage-4 additions). |
| `pipeline.py` | `compute_factor` (sandboxed eval + AST field-whitelist enforcement) and the 4 gates. `stage4_coverage` runs all 5 sub-tests. |
| `config.py` | **All thresholds live here.** HORIZON, window dates, S1–S4 gate values incl. rolling (120/20/0.70) and bootstrap (B=1000/block=10/seed=11/p≤0.05). Do not change without user direction. |
| `registry.py` | `Registry(set_name)`: per-set alpha_set.json + values dir + name prefix (`alpha`/`calpha`/`cxalpha`). Retire-never-delete; ETIMEDOUT read-retry; float32 values. |
| `memory.py` | `Memory(set_name)`: per-set experience_memory.json (successful/forbidden patterns + round log). |
| `round.py` | Runner. Reads `CANDIDATES`, optional `SET_NAME`/`FIELD_WHITELIST` from the candidates file; runs 4 stages; writes registry, per-round JSON, holdout snapshot; persists ONLY at completion (killed runs leave clean state). |

`"main"` set → `sets/behavioral_full/` paths. Read the set's
experience_memory.json before generating candidates.
