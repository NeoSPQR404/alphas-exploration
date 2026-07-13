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
SET_PATH = (ROOT / "results" / "mining" / "sets"
            / "behavioral_full" / "alpha_set.json")
VALUES_DIR = ROOT / "data" / "mining" / "alpha_values"


class Registry:
    def __init__(self, set_name: str = "main"):
        self.set_name = set_name
        if set_name == "main":
            self.set_path = SET_PATH
            self.values_dir = VALUES_DIR
            self.prefix = "alpha"
        else:
            self.set_path = (ROOT / "results" / "mining" / "sets"
                             / set_name / "alpha_set.json")
            self.values_dir = ROOT / "data" / "mining" / f"alpha_values_{set_name}"
            # canonical_composite gets a distinct prefix so its names never
            # collide with canonical's calpha_* ids
            self.prefix = ("cxalpha" if set_name == "canonical_composite"
                           else f"{set_name[0]}alpha")
        self.set_path.parent.mkdir(parents=True, exist_ok=True)
        self.values_dir.mkdir(parents=True, exist_ok=True)
        if self.set_path.exists():
            self.state = json.loads(self.set_path.read_text())
        else:
            self.state = {"next_id": 1, "alphas": [], "retired": []}

    # ------------------------------------------------------------ accessors
    def active(self) -> list[dict]:
        return self.state["alphas"]

    def get(self, name: str) -> dict | None:
        return next((a for a in self.active() if a["name"] == name), None)

    def values(self, name: str) -> pd.DataFrame:
        # retry: reads can hit transient ETIMEDOUT under disk pressure /
        # cloud-sync eviction on this machine
        import time
        for attempt in range(3):
            try:
                return pd.read_parquet(self.values_dir / f"{name}.parquet")
            except (TimeoutError, OSError):
                if attempt == 2:
                    raise
                time.sleep(5 * (attempt + 1))

    # ------------------------------------------------------------ mutation
    def add(self, expr: str, family: str, rationale: str, direction: int,
            metrics: dict, round_id: int, values: pd.DataFrame,
            logic_score: float) -> dict:
        name = f"{self.prefix}_{self.state['next_id']:04d}"
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
        # float32 halves the on-disk footprint; rank-based metrics are
        # insensitive to the precision loss
        values.astype("float32").to_parquet(self.values_dir / f"{name}.parquet")
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
        self.set_path.write_text(json.dumps(self.state, indent=2,
                                            ensure_ascii=False))

    # ------------------------------------------------------------ export
    def export_csv(self, path: Path | None = None) -> Path:
        path = path or self.set_path.with_suffix(".csv")
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
