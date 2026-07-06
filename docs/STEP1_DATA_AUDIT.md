# Step 1 — Dataset audit, gap-filling, cleaning (2026-07-06)

Goal: prepare a clean full-A daily dataset for alpha mining over **2017–2025**,
starting from the local `tushare-data` repo (fetched 2010–2025).

## 1. What was already there

`tushare-data/data` (all parquet, git-ignored in that repo):

| asset | span | contents |
|---|---|---|
| `panel/year=2017..2025` | 2017–2025 | 66-col daily panel: OHLCV + `pre_close/pct_chg/amount`, `adj_factor`, `close_hfq`, daily_basic (turnover, pe/pb/ps, mv, shares), PIT forward-filled TTM fundamentals (income/cashflow/balance), forecast+express guidance, CSI300 bench |
| `panel_insample_full/year=2010..2017` | 2010–2017/04 | 57-col variant (no bench / express detail) for lookback |
| `raw/daily, daily_basic, adj_factor` | 2010–2025 | per-day dumps, 3,886 trading days |
| `raw/income, balancesheet, cashflow` | 2005+ | per-stock statements (5,858 codes), every version kept |
| `raw/forecast, express` | 2016H2+ | guidance announcements |
| reference | — | `stock_basic` (5,855 codes incl. delisted), `trade_cal`, `namechange` (20,406 rows), `sw_member_all` (SW industry membership w/ in/out dates), CSI500 daily+weights |

Audit script: [`code/step1_audit_dataset.py`](../code/step1_audit_dataset.py) →
[`results/step1_audit.json`](../results/step1_audit.json).

## 2. Problems found & fixes

| # | problem | fix |
|---|---|---|
| 1 | Panel missing 3 trading days: **2024-11-05, 2025-06-06, 2025-12-02** — the raw `daily` files existed but held **0 rows** (transient empty API responses persisted forever by the resumable skip) | deleted + refetched (~5,400 rows each), rebuilt panel |
| 2 | Same failure mode found **systemically**: a 0-row scan across all by-date endpoints exposed 51 more empty files — `daily` 23 (all 2010), `daily_basic` 22 (2017–2021, the cause of the "early-year NaN" pattern), `adj_factor` 1 (2017-10-18), `suspend_d` 6 | all refetched successfully (none were genuinely empty); affected panel years rebuilt. 2017 daily_basic NaN fell 3.8%→1.4%, adj_factor NaN →0% |
| 3 | `raw/index_daily/000300.SH.parquet` truncated to 2010–2017/04 (overwritten during the in-sample backfill); a naive rebuild would have wiped `bench_close` for 2017-25 | refetched full 2010–2025 (3,886 rows) **before** rebuilding |
| 4 | Panel was built 06-16 but statements were refetched 06-26 → stale fundamentals snapshot | rebuild picks up the newer raw statements |
| 5 | No CSI300 membership | fetched `index_weight` 399300.SZ 2016–2025 (68,000 rows, monthly) |
| 6 | **No tradability data**: limit prices, suspensions | fetched `stk_limit` + `suspend_d` 2016–2025 by trade date |
| 7 | No flow-type raw material for mining | fetched `moneyflow` (order-size flows), `hk_hold` (northbound), `margin_detail` (margin balances) 2016–2025 |
| 8 | `sw_member_all` is a **current snapshot** → industry coverage decayed backwards (99.6% in 2025 → 71% in 2017) | interval join first, then fall back to the stock's earliest known membership (mild look-ahead, acceptable for neutralization); coverage now ≥ 99.97% every year |
| 9 | `pe_ttm` NaN ≈ 12–24%/yr | expected: tushare returns NaN for negative-earnings names; keep NaN, use `n_income_attr_p_ttm/total_mv` for a signed E/P instead |

Rebuild note: sequential reads of the small per-stock/per-day parquets ran at
~5 s/file on this machine while the fetcher competed for I/O; the rebuild
([`code/step1_rebuild_panel.py`](../code/step1_rebuild_panel.py)) thread-pools
them (~200 ms/file) and caches the five prepped statement frames under
`data/_prep_cache/`, cutting a rebuild from ~10 h to minutes.

Token probe (2026-07-06): `stk_limit / suspend_d / moneyflow / hk_hold /
margin_detail / index_weight / fina_indicator / dividend / block_trade /
share_float / stk_holdertrade / stk_holdernumber` all licensed;
`limit_list_d` **not** licensed (derived limit-hit flags from `stk_limit` instead).

Fetcher: [`code/step1_fetch_missing.py`](../code/step1_fetch_missing.py)
(resumable, per-day parquet into `tushare-data/data/raw/<endpoint>/YYYY/`).

## 3. Cleaned mining base

[`code/step1_build_base.py`](../code/step1_build_base.py) →
`data/base/year=2017..2025/base.parquet` (local only, git-ignored).
One row per (ts_code, trade_date) actually traded. All 66 panel columns plus:

**Derived prices** — `vwap` (= amount·1000 / vol·100, clipped to [low, high]),
`open/high/low/vwap_hfq`, `ret_1d` (hfq close-to-close, NaN across suspension
gaps > 10 trading days), `gap_days`.

**Tradability** — `up_limit/down_limit`; `limit_up_close`, `limit_down_close`,
`limit_up_touch`, `one_word_board`; `is_st` (from `namechange` name intervals,
matches ST/*ST/退); `days_on_market`; `board` (MAIN/SME/GEM/STAR/BSE);
`entry_blocked_next` (t+1 opens as one-word limit-up board → position can't be
entered).

**Industry** — `sw_l1_code/name` as of the day (SW 2021, membership intervals).

**Labels** (t+1 information only — features must use ≤ t) —
`fwd_ret_{1,5,10,20}d`: enter at t+1 **vwap**, exit at t+1+h vwap, hfq-adjusted,
NaN if the stock was suspended anywhere inside the window;
`tradable_entry`: traded at t+1 ∧ not one-word limit-up at t+1 ∧ not ST ∧
listed ≥ 120 calendar days.

## 4. Validation

[`code/step1_validate_base.py`](../code/step1_validate_base.py) →
[`results/step1_base_validation.json`](../results/step1_base_validation.json).

All 9 years pass: unique keys, full calendar alignment (0 missing days),
0 vwap outside [low, high], `ret_1d` ≡ `pct_chg` (p99 diff ≤ 0.005 pp).

| year | rows | ST share | tradable entry | up_limit NaN | fwd_ret_20d cov | SW L1 cov |
|---|---|---|---|---|---|---|
| 2017 | 754,372 | 1.7% | 91.7% | 1.4% | 94.5% | 100.0% |
| 2018 | 824,535 | 2.0% | 95.3% | 0.9% | 96.7% | 100.0% |
| 2019 | 894,177 | 3.1% | 94.1% | 1.0% | 97.8% | 100.0% |
| 2020 | 964,131 | 4.5% | 90.6% | 1.9% | 97.7% | 100.0% |
| 2021 | 1,085,445 | 4.3% | 90.8% | 2.2% | 98.3% | 100.0% |
| 2022 | 1,179,072 | 3.2% | 93.2% | 0.7% | 98.7% | 100.0% |
| 2023 | 1,258,734 | 2.4% | 95.2% | 0.0% | 99.4% | 100.0% |
| 2024 | 1,293,893 | 2.3% | 96.8% | 0.0% | 99.4% | 100.0% |
| 2025 | 1,313,898 | 3.0% | 95.4% | 0.0% | 90.5% | 100.0% |

Lower 2025 label coverage is year-end truncation (no forward window for the
last ~21 trading days of the sample). `up_limit` NaN in 2017–2021 is stocks
absent from `stk_limit` those years (mostly new listings / special boards);
limit flags default to False there.

## 5. Known limitations

* No sell-side consensus on this token (EPIBS/EGIB proxied by company guidance).
* `limit_list_d` unlicensed → limit-hit stats derived from prices vs `stk_limit`.
* BSE (北交所) rows are present from 2021+; filter `board != "BSE"` if the
  mining universe should exclude it.
* SW industry uses the *current* membership table with in/out dates — new
  listings before first classification have NaN industry for a few days.
