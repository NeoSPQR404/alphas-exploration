"""Step 1 — build the cleaned full-A mining base (2016-2025).

Input:  tushare-data panel (2017-2025), panel_insample_full (2016 tail for
        lookback), raw stk_limit / suspend_d / stock_basic / namechange /
        sw_member_all.
Output: data/base/year=YYYY/base.parquet — one row per (ts_code, trade_date)
        actually traded, carrying every panel column plus:

  derived prices   vwap (amount/vol), *_hfq versions of open/high/low/vwap,
                   ret_1d (hfq close-to-close, gap-aware = NaN after a
                   suspension gap > 10 trading days)
  tradability      up_limit/down_limit (stk_limit), touch/close limit flags,
                   one_word_board, is_st (namechange intervals), days_on_market
                   (calendar days since list_date), board (MAIN/GEM/STAR/BSE),
                   gap_days (trading days since previous bar of the stock)
  industry         sw_l1 code+name as of the day (sw_member_all intervals)
  labels           fwd_ret_{1,5,10,20}d: vwap(t+1) -> vwap(t+1+h), hfq;
                   tradable_entry: at t+1 the stock traded, didn't open at the
                   limit-up one-word board, is not ST, listed > 120 days
                   (labels use ONLY t+1.. information; features must use <= t)

Cleaning: drops duplicate (ts_code, trade_date) rows; asserts calendar
alignment; leaves NaN where a source is genuinely missing.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
TS = ROOT / "tushare-data" / "data"
OUT_DIR = Path(__file__).resolve().parents[1] / "data" / "base"
OUT_DIR.mkdir(parents=True, exist_ok=True)

YEARS = list(range(2017, 2027))  # load set for derived series (incl. 2026)
# Optional CLI args restrict which years are WRITTEN (slim still loads all
# of YEARS so cross-year boundary labels are correct). Default: write all.
EMIT_YEARS = [int(a) for a in sys.argv[1:]] or YEARS
LOOKBACK_YEARS = [2016]          # from panel_insample_full, for cross-year labels/returns
MAX_GAP_FOR_RET = 10             # trading-day gap beyond which ret_1d is NaN
LABEL_HORIZONS = [1, 5, 10, 20]
MIN_DAYS_ON_MARKET = 120         # calendar days for tradable_entry


def _read_raw_by_date(name: str, years) -> pd.DataFrame:
    frames = []
    for y in years:
        d = TS / "raw" / name / str(y)
        if d.exists():
            for f in sorted(d.glob("*.parquet")):
                df = pd.read_parquet(f)
                if len(df):
                    frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def load_panel_slim(cols):
    """Panel 2016(tail)+2017-2025 with just the columns needed for derived series."""
    frames = []
    for y in LOOKBACK_YEARS:
        p = TS / "panel_insample_full" / f"year={y}"
        df = pd.read_parquet(p, columns=cols)
        frames.append(df.assign(year=y))
    for y in YEARS:
        p = TS / "panel" / f"year={y}"
        df = pd.read_parquet(p, columns=cols)
        frames.append(df.assign(year=y))
    df = pd.concat(frames, ignore_index=True)
    df = df.drop_duplicates(["ts_code", "trade_date"], keep="last")
    return df


def interval_lookup(df, code_col, start_col, end_col, value_cols):
    """Return a function mapping (ts_code, trade_date str) via interval table."""
    t = df[[code_col, start_col, end_col] + value_cols].copy()
    t[start_col] = t[start_col].fillna("00000000").astype(str)
    t[end_col] = t[end_col].fillna("99999999").replace("", "99999999").astype(str)
    return t


def build_st_intervals():
    nc = pd.read_parquet(TS / "raw" / "namechange.parquet")
    nc["is_st"] = nc["name"].str.contains("ST|退", na=False)
    return interval_lookup(nc, "ts_code", "start_date", "end_date", ["is_st"])


def build_sw_intervals():
    sw = pd.read_parquet(TS / "raw" / "sw_member_all.parquet")
    sw = sw.rename(columns={"con_code": "ts_code"}) if "con_code" in sw else sw
    return interval_lookup(sw, "ts_code", "in_date", "out_date", ["l1_code", "l1_name"])


def apply_intervals(base_keys: pd.DataFrame, ivl: pd.DataFrame, value_cols):
    """As-of join: last interval starting <= date, then validate end >= date."""
    left = base_keys.copy()
    left["_td"] = left["trade_date"].astype("int64")
    left = left.sort_values("_td")
    right = ivl.rename(columns={ivl.columns[1]: "_start", ivl.columns[2]: "_end"})
    right["_start"] = right["_start"].astype("int64")
    right["_end"] = right["_end"].astype("int64")
    right = right.sort_values("_start")
    merged = pd.merge_asof(
        left, right, left_on="_td", right_on="_start", by="ts_code",
        direction="backward")
    expired = merged["_end"].notna() & (merged["_end"] < merged["_td"])
    for c in value_cols:
        merged.loc[expired, c] = np.nan if merged[c].dtype != object else None
    return merged.drop(columns=["_td", "_start", "_end"])


def main():
    # ---------------- derived global series (need cross-year continuity) ------
    slim_cols = ["ts_code", "trade_date", "open", "high", "low", "close",
                 "pre_close", "vol", "amount", "adj_factor", "close_hfq"]
    print("loading slim panel ...", flush=True)
    slim = load_panel_slim(slim_cols)
    slim = slim.sort_values(["ts_code", "trade_date"]).reset_index(drop=True)
    print(f"  {len(slim):,} rows")

    # vwap: amount 千元, vol 手(100 shares) -> yuan per share
    with np.errstate(divide="ignore", invalid="ignore"):
        slim["vwap"] = np.where(slim["vol"] > 0,
                                slim["amount"] * 1000.0 / (slim["vol"] * 100.0),
                                np.nan)
    # clip pathological vwap outside [low, high] (rounding / unit noise)
    slim["vwap"] = slim["vwap"].clip(lower=slim["low"], upper=slim["high"])
    for c in ("open", "high", "low", "vwap"):
        slim[c + "_hfq"] = slim[c] * slim["adj_factor"]

    g = slim.groupby("ts_code", sort=False)
    dt = pd.to_datetime(slim["trade_date"], format="%Y%m%d")
    # trading-day index for gap measurement
    cal = np.sort(slim["trade_date"].unique())
    day_idx = pd.Series(np.arange(len(cal)), index=cal)
    slim["_didx"] = slim["trade_date"].map(day_idx)
    slim["gap_days"] = g["_didx"].diff()
    slim["ret_1d"] = g["close_hfq"].pct_change()
    slim.loc[slim["gap_days"] > MAX_GAP_FOR_RET, "ret_1d"] = np.nan

    # labels: entry at t+1 vwap, exit at t+1+h vwap (hfq). Use shifted series
    # per stock; contiguity enforced via _didx distance == h.
    v = slim["vwap_hfq"]
    nxt_v = g["vwap_hfq"].shift(-1)
    nxt_didx = g["_didx"].shift(-1)
    entry_ok_gap = (nxt_didx - slim["_didx"]) == 1  # stock trades tomorrow
    for h in LABEL_HORIZONS:
        exit_v = g["vwap_hfq"].shift(-1 - h)
        exit_didx = g["_didx"].shift(-1 - h)
        contig = (exit_didx - slim["_didx"]) == (1 + h)  # no suspension inside
        slim[f"fwd_ret_{h}d"] = np.where(
            entry_ok_gap & contig & nxt_v.notna() & exit_v.notna(),
            exit_v / nxt_v - 1.0, np.nan)

    # entry one-word limit-up at t+1 (open==high==low==up_limit) -> can't buy
    derived_keep = ["ts_code", "trade_date", "vwap", "open_hfq", "high_hfq",
                    "low_hfq", "vwap_hfq", "gap_days", "ret_1d"] + \
                   [f"fwd_ret_{h}d" for h in LABEL_HORIZONS]

    # ---------------- static / interval reference ----------------------------
    sb = pd.read_parquet(TS / "raw" / "stock_basic.parquet",
                         columns=["ts_code", "list_date", "delist_date", "market"])
    board = {"主板": "MAIN", "创业板": "GEM", "科创板": "STAR", "北交所": "BSE",
             "中小板": "SME", "CDR": "CDR"}
    sb["board"] = sb["market"].map(board).fillna("OTHER")

    st_ivl = build_st_intervals()
    sw_ivl = build_sw_intervals()

    lim = _read_raw_by_date("stk_limit", LOOKBACK_YEARS + YEARS)
    lim = lim[["ts_code", "trade_date", "up_limit", "down_limit"]].drop_duplicates(
        ["ts_code", "trade_date"], keep="last") if len(lim) else lim
    print(f"stk_limit rows: {len(lim):,}")

    # next-day entry blocked if t+1 opens as one-word limit-up board
    if len(lim):
        el = slim[["ts_code", "trade_date", "open", "high", "low"]].merge(
            lim, on=["ts_code", "trade_date"], how="left")
        one_word_up = (el["open"] == el["high"]) & (el["high"] == el["low"]) & \
                      np.isclose(el["open"], el["up_limit"], atol=0.001)
        slim["_oneword_up"] = one_word_up.values
        slim["entry_blocked_next"] = slim.groupby("ts_code", sort=False)["_oneword_up"] \
            .shift(-1).astype("boolean").fillna(False).astype(bool)
    else:
        slim["entry_blocked_next"] = False
    derived_keep.append("entry_blocked_next")

    derived = slim[derived_keep].copy()
    del slim

    # ---------------- per-year assembly --------------------------------------
    for y in YEARS:
        if y not in EMIT_YEARS:
            continue
        print(f"year {y} ...", flush=True)
        df = pd.read_parquet(TS / "panel" / f"year={y}")
        if "year" in df.columns:
            df = df.drop(columns=["year"])
        n0 = len(df)
        df = df.drop_duplicates(["ts_code", "trade_date"], keep="last")
        if len(df) != n0:
            print(f"  dropped {n0 - len(df)} duplicate rows")
        df = df.merge(derived, on=["ts_code", "trade_date"], how="left")
        if len(lim):
            df = df.merge(lim, on=["ts_code", "trade_date"], how="left")
            df["limit_up_close"] = np.isclose(df["close"], df["up_limit"], atol=0.001)
            df["limit_down_close"] = np.isclose(df["close"], df["down_limit"], atol=0.001)
            df["limit_up_touch"] = np.isclose(df["high"], df["up_limit"], atol=0.001)
            df["one_word_board"] = (df["open"] == df["high"]) & (df["high"] == df["low"]) & \
                (df["limit_up_close"] | df["limit_down_close"])

        keys = df[["ts_code", "trade_date"]]
        df["is_st"] = apply_intervals(keys, st_ivl, ["is_st"])["is_st"] \
            .astype("boolean").fillna(False).astype(bool).values
        swm = apply_intervals(keys, sw_ivl, ["l1_code", "l1_name"])
        df["sw_l1_code"] = swm["l1_code"].values
        df["sw_l1_name"] = swm["l1_name"].values
        # sw_member_all is a current snapshot: pre-reclassification years lose
        # coverage (71% in 2017). Fall back to the stock's earliest known
        # membership for dates before its first interval (mild look-ahead,
        # noted in the audit doc).
        first = sw_ivl.sort_values("in_date").drop_duplicates("ts_code")
        first = first.set_index("ts_code")[["l1_code", "l1_name"]]
        miss = df["sw_l1_code"].isna()
        df.loc[miss, "sw_l1_code"] = df.loc[miss, "ts_code"].map(first["l1_code"])
        df.loc[miss, "sw_l1_name"] = df.loc[miss, "ts_code"].map(first["l1_name"])

        df = df.merge(sb[["ts_code", "list_date", "board"]], on="ts_code", how="left")
        dtd = pd.to_datetime(df["trade_date"], format="%Y%m%d")
        dtl = pd.to_datetime(df["list_date"], format="%Y%m%d", errors="coerce")
        df["days_on_market"] = (dtd - dtl).dt.days
        df = df.drop(columns=["list_date"])

        # label-side tradability (t+1 info only: traded t+1, not blocked entry)
        df["tradable_entry"] = (~df["entry_blocked_next"]) & (~df["is_st"]) & \
            (df["days_on_market"] >= MIN_DAYS_ON_MARKET) & df["fwd_ret_1d"].notna()

        df = df.sort_values(["trade_date", "ts_code"])
        out = OUT_DIR / f"year={y}"
        out.mkdir(exist_ok=True)
        df.to_parquet(out / "base.parquet", index=False)
        print(f"  -> {len(df):,} rows, {df.shape[1]} cols")

    print("done.")


if __name__ == "__main__":
    main()
