"""Experience memory: successful / forbidden generation patterns.

State lives in results/mining/experience_memory.json (committed). Each
pattern is a natural-language rule with evidence, written by the mining
agent during the Distill step and read back during Retrieve.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MEM_PATH = (ROOT / "results" / "mining" / "sets"
            / "behavioral_full" / "experience_memory.json")


class Memory:
    def __init__(self, set_name: str = "main"):
        if set_name == "main":
            self.mem_path = MEM_PATH
        else:
            self.mem_path = (ROOT / "results" / "mining" / "sets"
                             / set_name / "experience_memory.json")
        self.mem_path.parent.mkdir(parents=True, exist_ok=True)
        if self.mem_path.exists():
            self.state = json.loads(self.mem_path.read_text())
        else:
            self.state = {"rounds": [], "successful_patterns": [],
                          "forbidden_patterns": []}

    def next_round_id(self) -> int:
        return len(self.state["rounds"]) + 1

    def retrieve(self) -> dict:
        return {
            "successful_patterns": self.state["successful_patterns"],
            "forbidden_patterns": self.state["forbidden_patterns"],
        }

    def _upsert(self, bucket: str, pattern: str, evidence: str,
                round_id: int):
        for p in self.state[bucket]:
            if p["pattern"] == pattern:
                p["evidence"] = evidence
                p["rounds"] = sorted(set(p["rounds"] + [round_id]))
                p["strength"] = len(p["rounds"])
                return
        self.state[bucket].append({
            "pattern": pattern,
            "evidence": evidence,
            "rounds": [round_id],
            "strength": 1,
        })

    def add_success(self, pattern: str, evidence: str, round_id: int):
        self._upsert("successful_patterns", pattern, evidence, round_id)

    def add_forbidden(self, pattern: str, evidence: str, round_id: int):
        self._upsert("forbidden_patterns", pattern, evidence, round_id)

    def log_round(self, round_id: int, summary: dict):
        self.state["rounds"].append(
            {"round": round_id, "date": date.today().isoformat(), **summary})

    def save(self):
        self.mem_path.write_text(json.dumps(self.state, indent=2,
                                            ensure_ascii=False))
