"""Data context for alpha mining: wide frames from the Step-1 base panel.

Loads data/base/year=YYYY/base.parquet, pivots requested fields into wide
(date x ts_code) frames with an on-disk parquet cache, and exposes:

- price/volume/valuation fields (hfq prices; see FIELD_MAP)
- derived yield fields (EP, BP, SP, CFP) built from PIT TTM fundamentals
- labels fwd_ret_{1,5,10,20}d (entry at t+1 vwap, suspension-aware)
- evaluation masks: tradable_entry per universe (full A, HS300, CSI500,
  CSI1000) from tushare index_weight monthly snapshots, forward-filled
- INDUSTRY: SW L1 integer codes for CsIndNeutralize
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
BASE_DIR = ROOT / "data" / "base"
WIDE_CACHE = ROOT / "data" / "_wide_cache"
RAW = ROOT.parent / "tushare-data" / "data" / "raw"

INDEX_CODES = {"hs300": "000300.SH", "csi500": "000905.SH", "csi1000": "000852.SH"}

# expression-visible name -> base panel column
FIELD_MAP = {
    "OPEN": "open_hfq",
    "HIGH": "high_hfq",
    "LOW": "low_hfq",
    "CLOSE": "close_hfq",
    "VWAP": "vwap_hfq",
    "VOLUME": "vol",
    "AMOUNT": "amount",
    "TURN": "turnover_rate",
    "TURN_F": "turnover_rate_f",
    "VR": "volume_ratio",
    "RET": "ret_1d",
    "AMP": "amplitude",
    "PE": "pe_ttm",
    "PB": "pb",
    "PS": "ps_ttm",
    "MV": "total_mv",
    "CMV": "circ_mv",
    "FREE_SHARE": "free_share",
    "BENCH_RET": "bench_pct_chg",
    "DAYS_ON": "days_on_market",
}

_RAW_NUMERIC = {
    "total_mv", "circ_mv", "n_income_attr_p_ttm", "revenue_ttm",
    "n_cashflow_act_ttm", "total_hldr_eqy_exc_min_int",
}

# Step-2 base extension: flow fields built from raw tushare endpoint dirs
# (tushare-data/data/raw/<ep>/YYYY/*.parquet), pivoted and 0-filled where
# absence is economically a zero (no northbound access / no margin
# eligibility / no flow), NaN on non-traded cells. Cached in _wide_cache.
EXT_FIELDS = {
    # moneyflow: order-size-bucketed flows, normalized by total two-sided amount
    "MF_LG_NET",   # (buy_lg+buy_elg - sell_lg - sell_elg) / total  [institutional direction]
    "MF_SM_NET",   # (buy_sm - sell_sm) / total                     [retail direction]
    "MF_NET",      # net_mf_amount / total
    # hk_hold: northbound (Stock Connect) holdings
    "HK_RATIO",    # holding as % of shares (0 where not connect-eligible)
    # margin_detail: margin financing / securities lending
    "RZ_MV",       # financing balance rzye / circ mv
    "RQ_MV",       # short balance rqye / circ mv
    "RZ_NET",      # daily net financing buys (rzmre - rzche) / circ mv
}


class Panel:
    def __init__(self, years=range(2017, 2026)):
        self.years = list(years)
        self._long: pd.DataFrame | None = None
        self._wide: dict[str, pd.DataFrame] = {}
        self._dates: pd.Index | None = None
        self._codes: pd.Index | None = None
        WIDE_CACHE.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------ long panel
    def long(self, columns: list[str]) -> pd.DataFrame:
        need = sorted(set(columns) | {"ts_code", "trade_date"})
        if self._long is not None and set(need) <= set(self._long.columns):
            return self._long[need]
        frames = [
            pd.read_parquet(BASE_DIR / f"year={y}" / "base.parquet", columns=need)
            for y in self.years
        ]
        df = pd.concat(frames, ignore_index=True)
        df = df.sort_values(["trade_date", "ts_code"])
        self._long = df
        return df

    # ------------------------------------------------------------ wide frames
    def _pivot(self, col: str, dtype=float) -> pd.DataFrame:
        cache = WIDE_CACHE / f"{col}.parquet"
        if cache.exists():
            return pd.read_parquet(cache)
        df = self.long([col])
        wide = df.pivot(index="trade_date", columns="ts_code", values=col)
        if dtype is float:
            wide = wide.astype(float)
        wide.to_parquet(cache)
        return wide

    def wide(self, name: str) -> pd.DataFrame:
        """Wide frame by expression-visible name or raw base column name."""
        if name in self._wide:
            return self._wide[name]
        if name == "INDUSTRY":
            out = self._industry()
        elif name in ("EP", "BP", "SP", "CFP"):
            out = self._yield_field(name)
        elif name in EXT_FIELDS:
            out = self._ext_field(name)
        elif name in FIELD_MAP:
            out = self._pivot(FIELD_MAP[name])
        else:
            out = self._pivot(name)
        out = self._align(out)
        self._wide[name] = out
        return out

    def _align(self, wide: pd.DataFrame) -> pd.DataFrame:
        if self._dates is None:
            self._dates = wide.index
            self._codes = wide.columns
            return wide
        return wide.reindex(index=self._dates, columns=self._codes)

    # ------------------------------------------------------------ derived
    def _yield_field(self, name: str) -> pd.DataFrame:
        # total_mv is in 万元 (1e4 CNY); TTM/balance items are in CNY.
        num_col = {
            "EP": "n_income_attr_p_ttm",
            "BP": "total_hldr_eqy_exc_min_int",
            "SP": "revenue_ttm",
            "CFP": "n_cashflow_act_ttm",
        }[name]
        num = self._pivot(num_col)
        mv = self._pivot("total_mv") * 1e4
        return num / mv.where(mv > 0)

    # ------------------------------------------------------------ extension
    def _read_endpoint(self, ep: str, columns: list[str]) -> pd.DataFrame:
        """Threaded read of a raw tushare endpoint dir (per-date parquets)."""
        from concurrent.futures import ThreadPoolExecutor

        files = sorted(
            f for y in self.years
            for f in (RAW / ep / str(y)).glob("*.parquet")
        )
        cols = sorted(set(columns) | {"ts_code", "trade_date"})

        def _read(f):
            try:
                return pd.read_parquet(f, columns=cols)
            except Exception:
                df = pd.read_parquet(f)
                keep = [c for c in cols if c in df.columns]
                return df[keep]

        with ThreadPoolExecutor(16) as pool:
            frames = list(pool.map(_read, files))
        out = pd.concat(frames, ignore_index=True)
        return out.drop_duplicates(subset=["ts_code", "trade_date"], keep="last")

    def _ext_pivot(self, name, ep, columns, builder, fill_zero) -> pd.DataFrame:
        """Build one extension wide frame; NaN -> 0 where absence means zero
        exposure (non-eligible stock), but only on traded cells."""
        cache = WIDE_CACHE / f"EXT_{name}.parquet"
        if cache.exists():
            return pd.read_parquet(cache)
        df = self._read_endpoint(ep, columns)
        series = builder(df)
        df = df.assign(_v=series)
        wide = df.pivot(index="trade_date", columns="ts_code", values="_v")
        wide = wide.astype(float)
        wide = wide.reindex(index=self.wide("CLOSE").index,
                            columns=self.wide("CLOSE").columns)
        if fill_zero:
            traded = self.wide("CLOSE").notna()
            wide = wide.where(~(traded & wide.isna()), 0.0).where(traded)
        wide.to_parquet(cache)
        return wide

    def _ext_field(self, name: str) -> pd.DataFrame:
        mf_amt = ["buy_sm_amount", "sell_sm_amount", "buy_md_amount",
                  "sell_md_amount", "buy_lg_amount", "sell_lg_amount",
                  "buy_elg_amount", "sell_elg_amount", "net_mf_amount"]

        def _mf_total(df):
            return sum(df[c] for c in mf_amt[:8]).replace(0, np.nan)

        spec = {
            "MF_LG_NET": ("moneyflow", mf_amt, lambda d: (
                d["buy_lg_amount"] + d["buy_elg_amount"]
                - d["sell_lg_amount"] - d["sell_elg_amount"]) / _mf_total(d),
                False),
            "MF_SM_NET": ("moneyflow", mf_amt, lambda d: (
                d["buy_sm_amount"] - d["sell_sm_amount"]) / _mf_total(d),
                False),
            "MF_NET": ("moneyflow", mf_amt,
                       lambda d: d["net_mf_amount"] / _mf_total(d), False),
            "HK_RATIO": ("hk_hold", ["ratio"], lambda d: d["ratio"], True),
            "RZ_MV": ("margin_detail", ["rzye"], lambda d: d["rzye"], True),
            "RQ_MV": ("margin_detail", ["rqye"], lambda d: d["rqye"], True),
            "RZ_NET": ("margin_detail", ["rzmre", "rzche"],
                       lambda d: d["rzmre"] - d["rzche"], True),
        }
        ep, cols, builder, fill_zero = spec[name]
        wide = self._ext_pivot(name, ep, cols, builder, fill_zero)
        if name in ("RZ_MV", "RQ_MV", "RZ_NET"):
            cmv = self.wide("CMV") * 1e4   # circ_mv 万元 -> CNY
            wide = wide / cmv.where(cmv > 0)
        return wide

    def _industry(self) -> pd.DataFrame:
        df = self.long(["sw_l1_code"])
        codes = df["sw_l1_code"].astype("category")
        df = df.assign(_ind=codes.cat.codes.astype(float))
        df.loc[df["sw_l1_code"].isna(), "_ind"] = np.nan
        wide = df.pivot(index="trade_date", columns="ts_code", values="_ind")
        return wide

    # ------------------------------------------------------------ labels/masks
    def label(self, horizon: int = 10) -> pd.DataFrame:
        return self.wide(f"fwd_ret_{horizon}d")

    def tradable(self) -> pd.DataFrame:
        if "TRADABLE" not in self._wide:
            df = self.long(["tradable_entry"])
            wide = df.pivot(index="trade_date", columns="ts_code",
                            values="tradable_entry").astype(float)
            self._wide["TRADABLE"] = self._align(wide) > 0
        return self._wide["TRADABLE"]

    def universe_mask(self, universe: str = "all") -> pd.DataFrame:
        """Boolean wide frame: evaluable at t (tradable entry + membership)."""
        key = f"MASK_{universe}"
        if key in self._wide:
            return self._wide[key]
        mask = self.tradable()
        if universe != "all":
            idx_code = INDEX_CODES[universe]
            w = pd.read_parquet(RAW / f"index_weight_{idx_code}.parquet")
            w = w[["con_code", "trade_date", "weight"]].copy()
            snap = w.pivot_table(index="trade_date", columns="con_code",
                                 values="weight", aggfunc="last")
            # snapshots are ~monthly; forward-fill membership to trading days
            union_dates = snap.index.union(mask.index)
            member = (
                snap.notna()
                .reindex(union_dates)
                .astype("boolean")
                .ffill()
                .reindex(mask.index)
                .reindex(columns=mask.columns)
                .fillna(False)
                .astype(bool)
            )
            mask = mask & member
        self._wide[key] = mask
        return mask

    # ------------------------------------------------------------ namespace
    def namespace(self) -> dict:
        """Lazy field namespace for evaluating candidate expressions."""
        class _NS(dict):
            def __missing__(_self, k):
                v = self.wide(k)
                _self[k] = v
                return v
        return _NS()
