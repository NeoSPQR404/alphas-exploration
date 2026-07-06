"""Step 1 — audit the tushare-data dataset (2010-2025).

Inspects the assembled daily panels and raw endpoint dumps under
../tushare-data/data, and reports:
  * schema (columns / dtypes) of each panel
  * date coverage vs the tushare trade calendar
  * universe coverage vs stock_basic (per year)
  * per-column missing-value rates on key fields
  * which raw endpoints exist and their spans

Output: results/step1_audit.json + printed summary.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow.dataset as ds
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[2]  # Quant Research/
TS = ROOT / "tushare-data" / "data"
OUT = Path(__file__).resolve().parents[1] / "results"
OUT.mkdir(exist_ok=True)

report = {}


def panel_paths():
    out = {}
    for name in ["panel", "panel_insample_full"]:
        d = TS / name
        if d.exists():
            years = sorted(p.name.split("=")[1] for p in d.glob("year=*"))
            out[name] = years
    return out


def audit_panel(name):
    d = TS / name
    dataset = ds.dataset(d, format="parquet", partitioning="hive")
    schema = dataset.schema
    cols = {schema.field(i).name: str(schema.field(i).type) for i in range(len(schema))}

    # Trade calendar
    cal = pd.read_parquet(TS / "raw" / "trade_cal.parquet")
    cal_open = cal[cal["is_open"] == 1]["cal_date"].astype(str)

    # Scan per-year stats without loading everything at once
    year_stats = []
    key_fields = [c for c in [
        "open", "high", "low", "close", "vol", "amount", "pct_chg",
        "adj_factor", "turnover_rate", "turnover_rate_f", "total_mv",
        "circ_mv", "pe_ttm", "pb", "float_share", "total_share",
        "n_income_attr_p_ttm", "n_cashflow_act_ttm",
        "total_hldr_eqy_exc_min_int", "total_liab", "total_assets",
    ] if c in cols]
    id_date = "trade_date" if "trade_date" in cols else None
    id_code = "ts_code" if "ts_code" in cols else None

    for ydir in sorted(d.glob("year=*")):
        year = ydir.name.split("=")[1]
        df = pd.read_parquet(ydir, columns=[id_date, id_code] + key_fields)
        dates = df[id_date].astype(str)
        exp = cal_open[cal_open.str.startswith(year)]
        missing_days = sorted(set(exp) - set(dates.unique()))
        nan_rate = df[key_fields].isna().mean().round(4).to_dict()
        year_stats.append({
            "year": year,
            "rows": int(len(df)),
            "n_days": int(dates.nunique()),
            "n_days_expected": int(len(exp)),
            "missing_days": missing_days[:10],
            "n_missing_days": len(missing_days),
            "n_stocks": int(df[id_code].nunique()),
            "nan_rate": nan_rate,
        })
        del df

    return {"columns": cols, "n_columns": len(cols), "years": year_stats}


def audit_raw():
    raw = TS / "raw"
    out = {}
    for f in sorted(raw.glob("*.parquet")):
        try:
            n = pq.ParquetFile(f).metadata.num_rows
        except Exception as e:
            n = str(e)
        out[f.name] = {"rows": n}
    for d in sorted(p for p in raw.iterdir() if p.is_dir() and not p.name.startswith("_")):
        files = list(d.rglob("*.parquet"))
        out[d.name + "/"] = {"n_files": len(files)}
    for f in sorted((raw / "_consolidated").glob("*.parquet")):
        pf = pq.ParquetFile(f)
        out["_consolidated/" + f.name] = {
            "rows": pf.metadata.num_rows,
            "columns": pf.metadata.num_columns,
        }
    return out


def detail_small_tables():
    """Content-level look at the small reference tables."""
    raw = TS / "raw"
    det = {}
    sb = pd.read_parquet(raw / "stock_basic.parquet")
    det["stock_basic"] = {
        "rows": len(sb),
        "columns": list(sb.columns),
        "list_status": sb["list_status"].value_counts().to_dict() if "list_status" in sb else None,
        "exchanges": sb["ts_code"].str[-2:].value_counts().to_dict(),
    }
    swm = pd.read_parquet(raw / "sw_member_all.parquet")
    det["sw_member_all"] = {"rows": len(swm), "columns": list(swm.columns),
                            "n_codes": int(swm["con_code"].nunique()) if "con_code" in swm else None}
    nc = pd.read_parquet(raw / "namechange.parquet")
    det["namechange"] = {"rows": len(nc), "columns": list(nc.columns)}
    cal = pd.read_parquet(raw / "trade_cal.parquet")
    det["trade_cal"] = {"rows": len(cal),
                        "span": [str(cal["cal_date"].min()), str(cal["cal_date"].max())]}
    for idx in ["000300.SH", "000905.SH"]:
        p = raw / "index_daily" / f"{idx}.parquet"
        if not p.exists():
            p = raw / f"index_daily_{idx}.parquet"
        if p.exists():
            df = pd.read_parquet(p)
            det[f"index_daily_{idx}"] = {"rows": len(df),
                                         "span": [str(df['trade_date'].min()), str(df['trade_date'].max())]}
    return det


if __name__ == "__main__":
    report["panels_found"] = panel_paths()
    print("panels:", report["panels_found"])
    for name in report["panels_found"]:
        print(f"auditing {name} ...", flush=True)
        report[name] = audit_panel(name)
    report["raw"] = audit_raw()
    report["reference_tables"] = detail_small_tables()

    with open(OUT / "step1_audit.json", "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)

    # summary print
    for name in report["panels_found"]:
        r = report[name]
        print(f"\n=== {name}: {r['n_columns']} columns ===")
        for ys in r["years"]:
            print(f"  {ys['year']}: rows={ys['rows']:>9,} days={ys['n_days']}/{ys['n_days_expected']} "
                  f"missing_days={ys['n_missing_days']} stocks={ys['n_stocks']}")
    print("\nraw endpoints:")
    for k, v in report["raw"].items():
        print(f"  {k}: {v}")
    print("\nwritten:", OUT / "step1_audit.json")
