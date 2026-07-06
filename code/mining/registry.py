"""Alpha factor set registry: accepted factors + their metrics.

State lives in results/mining/alpha_set.json (committed, exportable).
Factor values are cached as parquet under data/mining/alpha_values/
(git-ignored, rebuildable from expressions).
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SET_PATH = ROOT / "results" / "mining" / "alpha_set.json"
VALUES_DIR = ROOT / "data" / "mining" / "alpha_values"


class Registry:
    def __init__(self):
        SET_PATH.parent.mkdir(parents=True, exist_ok=True)
        VALUES_DIR.mkdir(parents=True, exist_ok=True)
        if SET_PATH.exists():
            self.state = json.loads(SET_PATH.read_text())
        else:
            self.state = {"next_id": 1, "alphas": [], "retired": []}

    # ------------------------------------------------------------ accessors
    def active(self) -> list[dict]:
        return self.state["alphas"]

    def get(self, name: str) -> dict | None:
        return next((a for a in self.active() if a["name"] == name), None)

    def values(self, name: str) -> pd.DataFrame:
        return pd.read_parquet(VALUES_DIR / f"{name}.parquet")

    # ------------------------------------------------------------ mutation
    def add(self, expr: str, family: str, rationale: str, direction: int,
            metrics: dict, round_id: int, values: pd.DataFrame,
            logic_score: float) -> dict:
        name = f"alpha_{self.state['next_id']:04d}"
        self.state["next_id"] += 1
        entry = {
            "name": name,
            "expression": expr,
            "family": family,
            "rationale": rationale,
            "direction": direction,   # +1: raw expr long-high; -1: flipped
            "logic_score": logic_score,
            "metrics": metrics,
            "accepted_round": round_id,
            "accepted_date": date.today().isoformat(),
        }
        self.state["alphas"].append(entry)
        values.to_parquet(VALUES_DIR / f"{name}.parquet")
        return entry

    def retire(self, name: str, reason: str, round_id: int):
        entry = self.get(name)
        if entry is None:
            return
        self.state["alphas"].remove(entry)
        entry["retired_round"] = round_id
        entry["retired_reason"] = reason
        self.state["retired"].append(entry)

    def save(self):
        SET_PATH.write_text(json.dumps(self.state, indent=2,
                                       ensure_ascii=False))

    # ------------------------------------------------------------ export
    def export_csv(self, path: Path | None = None) -> Path:
        path = path or SET_PATH.with_suffix(".csv")
        rows = []
        for a in self.active():
            row = {k: a[k] for k in ("name", "expression", "family",
                                     "direction", "accepted_round")}
            for w in ("is", "oos"):
                for k in ("ic_mean", "icir", "ls_mean"):
                    row[f"{w}_{k}"] = a["metrics"].get(w, {}).get(k)
            rows.append(row)
        pd.DataFrame(rows).to_csv(path, index=False)
        return path
