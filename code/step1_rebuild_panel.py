"""Step 1 — rebuild the tushare-data daily panel (2017-2025), I/O-optimized.

Same output as `python -m tsbarra.run panel`, with two fixes for this
machine's pathological sequential small-file reads (~5 s/file cold while the
fetcher competes for I/O; 16 threads ≈ 200 ms/file):

  * storage.load_dataset (statements/forecast/express) -> thread-pool reads,
    and the five prepped frames are cached to parquet so a re-run skips the
    ~1 h prep entirely;
  * build_panel._load_year_prices (daily/daily_basic/adj_factor per year)
    -> thread-pool reads.

Usage: python3 step1_rebuild_panel.py [year ...]   (default 2017..2025)
"""
from __future__ import annotations

import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[2] / "tushare-data"
sys.path.insert(0, str(REPO))

from tsbarra import config, storage  # noqa: E402

CACHE = Path(__file__).resolve().parents[1] / "data" / "_prep_cache"
CACHE.mkdir(parents=True, exist_ok=True)


def _read_many(files):
    with ThreadPoolExecutor(16) as ex:
        return [df for df in ex.map(pd.read_parquet, files) if not df.empty]


def load_dataset_parallel(dataset: str) -> pd.DataFrame:
    root = config.RAW_DIR / dataset
    files = sorted(root.rglob("*.parquet")) if root.exists() else []
    frames = _read_many(files)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


storage.load_dataset = load_dataset_parallel

from tsbarra import build_panel  # noqa: E402
from tsbarra.logutil import setup  # noqa: E402


def _load_year_prices_fast(year: int) -> pd.DataFrame:
    def yr(ds):
        root = config.RAW_DIR / ds / str(year)
        files = sorted(root.glob("*.parquet")) if root.exists() else []
        frames = _read_many(files)
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    daily = yr("daily")
    if daily.empty:
        return daily
    db = yr("daily_basic")
    adj = yr("adj_factor")
    base = daily.copy()
    if not db.empty:
        cols = ["ts_code", "trade_date"] + \
            [c for c in build_panel.DAILY_BASIC_COLS if c in db.columns]
        base = base.merge(db[cols], on=["ts_code", "trade_date"], how="left",
                          suffixes=("", "_db"))
    if not adj.empty:
        base = base.merge(adj[["ts_code", "trade_date", "adj_factor"]],
                          on=["ts_code", "trade_date"], how="left")
    base["amplitude"] = (base["high"] - base["low"]) / base["pre_close"] * 100.0
    if "adj_factor" in base:
        base["close_hfq"] = base["close"] * base["adj_factor"]
    return base


build_panel._load_year_prices = _load_year_prices_fast

_orig_preps = {name: getattr(build_panel, f"_prep_{name}")
               for name in ("income", "cashflow", "balance", "forecast", "express")}


def _cached_prep(name):
    def run():
        p = CACHE / f"{name}.parquet"
        if p.exists():
            df = pd.read_parquet(p)
            print(f"prep cache hit: {name} ({len(df)} rows)", flush=True)
            return df
        df = _orig_preps[name]()
        if not df.empty:
            df.to_parquet(p, index=False)
        return df
    return run


for _name in _orig_preps:
    setattr(build_panel, f"_prep_{_name}", _cached_prep(_name))

if __name__ == "__main__":
    setup()
    years = [int(a) for a in sys.argv[1:]] or None
    build_panel.build(years)
