"""Experience memory: pattern statistics + insights, per factor set.

State lives in results/mining/sets/<set>/experience_memory.json.

Schema v2 (2026-07-10) — every pattern carries:
  name              short identifier (slug)
  description       what the pattern is
  template          the generator skeleton it produces
  occurrence_count  candidates attributed to it (lifetime)
  accept_count      how many were accepted
  success_rate      accept_count / occurrence_count  (None if occ == 0)
  classification    "success" | "forbidden" | "undetermined"
  rounds, evidence, curated

Patterns live in one `patterns` dict keyed by name; `classification`
routes them (merge() re-classifies on every update). `insights` are
forward-looking factor ideas under exploration, promoted to patterns
once they earn enough trials.

Key methods:
  merge()             upsert a pattern's stats + re-classify (the single
                      path by which anything enters success/forbidden)
  classify()          decide success/forbidden/undetermined from stats
  insight()           register a new factor idea
  record_insight()    fold trial results into an insight; auto-promote
  generation_plan()   balance a round's candidate budget across
                      exploit(success) / probe(undetermined) / explore(insight)
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _mem_path(set_name: str) -> Path:
    folder = "behavioral_full" if set_name == "main" else set_name
    return ROOT / "results" / "mining" / "sets" / folder / "experience_memory.json"


def _slug(text: str, n: int = 7) -> str:
    words = re.findall(r"[A-Za-z0-9]+", text.lower())
    return "-".join(words[:n]) or "pattern"


class Memory:
    # classification thresholds (a pattern with enough trials is routed
    # by its accept rate; too few trials stays undetermined)
    SUCCESS_MIN_RATE = 0.40
    SUCCESS_MIN_OCC = 3
    FORBIDDEN_MAX_RATE = 0.15
    FORBIDDEN_MIN_OCC = 4
    # insight promotion / refutation once it has been tried
    INSIGHT_MIN_TRIALS = 3
    INSIGHT_PROMOTE_RATE = 0.40
    INSIGHT_REFUTE_RATE = 0.15

    def __init__(self, set_name: str = "main"):
        self.set_name = set_name
        self.mem_path = _mem_path(set_name)
        self.mem_path.parent.mkdir(parents=True, exist_ok=True)
        if self.mem_path.exists():
            self.state = json.loads(self.mem_path.read_text())
        else:
            self.state = {}
        self.state.setdefault("schema", 2)
        self.state.setdefault("rounds", [])
        self.state.setdefault("patterns", {})
        self.state.setdefault("insights", {})

    # ------------------------------------------------------------ rounds
    def next_round_id(self) -> int:
        return len(self.state["rounds"]) + 1

    def log_round(self, round_id: int, summary: dict):
        self.state["rounds"].append(
            {"round": round_id, "date": date.today().isoformat(), **summary})

    # ------------------------------------------------------------ classify
    def classify(self, occurrence_count: int, success_rate) -> str:
        """success / forbidden / undetermined from a pattern's stats."""
        if success_rate is None or occurrence_count == 0:
            return "undetermined"
        if (occurrence_count >= self.SUCCESS_MIN_OCC
                and success_rate >= self.SUCCESS_MIN_RATE):
            return "success"
        if (occurrence_count >= self.FORBIDDEN_MIN_OCC
                and success_rate <= self.FORBIDDEN_MAX_RATE):
            return "forbidden"
        return "undetermined"

    # ------------------------------------------------------------ merge
    def merge(self, name: str, *, description: str | None = None,
              template: str | None = None, occurrences: int = 0,
              accepts: int = 0, round_id: int | None = None,
              evidence: str | None = None,
              classification: str | None = None,
              curated: bool = False) -> dict:
        """Upsert pattern `name`, accumulate stats, re-classify.

        `occurrences`/`accepts` are ADDED to the running totals.
        `classification` (if given) pins the label (curated narrative
        patterns); otherwise the label is derived from the stats via
        classify(). This is the single entry point to the pattern store.
        """
        p = self.state["patterns"].get(name)
        if p is None:
            p = {"name": name, "description": description or name,
                 "template": template or "", "occurrence_count": 0,
                 "accept_count": 0, "success_rate": None,
                 "classification": "undetermined", "rounds": [],
                 "curated": curated, "pinned": classification is not None}
            self.state["patterns"][name] = p
        if description is not None:
            p["description"] = description
        if template is not None:
            p["template"] = template
        if evidence is not None:
            p["evidence"] = evidence
        if curated:
            p["curated"] = True
        p["occurrence_count"] += max(0, occurrences)
        p["accept_count"] += max(0, accepts)
        if round_id is not None and round_id not in p["rounds"]:
            p["rounds"] = sorted(p["rounds"] + [round_id])
        p["success_rate"] = (p["accept_count"] / p["occurrence_count"]
                             if p["occurrence_count"] else None)
        if classification is not None:
            p["classification"] = classification
            p["pinned"] = True
        elif not p.get("pinned"):
            p["classification"] = self.classify(
                p["occurrence_count"], p["success_rate"])
        return p

    # ------------------------------------------------------------ insights
    def insight(self, name: str, *, description: str, hypothesis: str,
                round_id: int | None = None) -> dict:
        """Register a new factor idea to explore (not yet a pattern)."""
        i = self.state["insights"].get(name)
        if i is None:
            i = {"name": name, "description": description,
                 "hypothesis": hypothesis, "status": "proposed",
                 "occurrence_count": 0, "accept_count": 0, "rounds": [],
                 "spawned_pattern": None,
                 "created": date.today().isoformat()}
            self.state["insights"][name] = i
        else:
            i["description"] = description
            i["hypothesis"] = hypothesis
        if round_id is not None and round_id not in i["rounds"]:
            i["rounds"] = sorted(i["rounds"] + [round_id])
        return i

    def record_insight(self, name: str, *, occurrences: int, accepts: int,
                       round_id: int | None = None,
                       pattern_name: str | None = None) -> dict:
        """Fold a round's trial of an insight into its record and
        auto-promote (to a success pattern) or refute it once it has
        enough trials."""
        i = self.state["insights"].get(name)
        if i is None:
            i = self.insight(name, description=name, hypothesis="",
                             round_id=round_id)
        i["occurrence_count"] += max(0, occurrences)
        i["accept_count"] += max(0, accepts)
        if round_id is not None and round_id not in i["rounds"]:
            i["rounds"] = sorted(i["rounds"] + [round_id])
        rate = (i["accept_count"] / i["occurrence_count"]
                if i["occurrence_count"] else None)
        i["status"] = "testing"
        if i["occurrence_count"] >= self.INSIGHT_MIN_TRIALS and rate is not None:
            if rate >= self.INSIGHT_PROMOTE_RATE:
                i["status"] = "promoted"
                pn = pattern_name or i["spawned_pattern"] or name
                i["spawned_pattern"] = pn
                self.merge(pn, description=i["description"],
                           template=i.get("hypothesis", ""),
                           occurrences=i["occurrence_count"],
                           accepts=i["accept_count"], round_id=round_id,
                           evidence=f"promoted from insight '{name}'")
            elif rate <= self.INSIGHT_REFUTE_RATE:
                i["status"] = "refuted"
        return i

    # ------------------------------------------------------------ accessors
    def _by_class(self, cls: str) -> list:
        ps = [p for p in self.state["patterns"].values()
              if p["classification"] == cls]
        return sorted(ps, key=lambda p: (-(p["success_rate"] or 0),
                                         -p["occurrence_count"]))

    def successful_patterns(self) -> list:
        return self._by_class("success")

    def forbidden_patterns(self) -> list:
        return self._by_class("forbidden")

    def undetermined_patterns(self) -> list:
        return self._by_class("undetermined")

    def active_insights(self) -> list:
        return [i for i in self.state["insights"].values()
                if i["status"] in ("proposed", "testing")]

    def retrieve(self) -> dict:
        return {"successful_patterns": self.successful_patterns(),
                "forbidden_patterns": self.forbidden_patterns(),
                "undetermined_patterns": self.undetermined_patterns(),
                "insights": self.active_insights()}

    # ------------------------------------------------------------ balance
    def _recent_accept_rate(self, k: int = 2) -> float | None:
        rounds = [r for r in self.state["rounds"] if "s1_pass" in r
                  or "accepted" in r]
        rounds = self.state["rounds"][-k:]
        occ = acc = 0
        for r in rounds:
            occ += r.get("candidates", 0)
            acc += len(r.get("accepted", []) or [])
        return acc / occ if occ else None

    def generation_plan(self, n_candidates: int = 40) -> dict:
        """Balance a round's candidate budget across three modes and name
        the specific patterns/insights to draw from.

        exploit  proven success patterns (highest success-rate veins)
        probe    undetermined patterns (need more trials to classify)
        explore  active insights (new ideas)

        The split adapts to the recent acceptance rate: a saturating set
        (low recent yield) shifts budget toward exploration; a rich vein
        shifts toward exploitation. Forbidden patterns are returned as an
        avoid-list, not a generation source.
        """
        rate = self._recent_accept_rate()
        if rate is None:
            w = (0.55, 0.20, 0.25)          # cold start: balanced
        elif rate < 0.15:
            w = (0.35, 0.20, 0.45)          # saturating: explore more
        elif rate > 0.40:
            w = (0.70, 0.15, 0.15)          # rich vein: exploit
        else:
            w = (0.55, 0.20, 0.25)          # steady
        n_exploit = round(n_candidates * w[0])
        n_probe = round(n_candidates * w[1])
        n_explore = n_candidates - n_exploit - n_probe

        succ = self.successful_patterns()
        und = self.undetermined_patterns()
        ins = self.active_insights()

        def _spread(items, budget, key):
            if not items or budget <= 0:
                return []
            # weight by score; at least 1 each until budget exhausted
            scores = [max(0.01, key(it)) for it in items]
            tot = sum(scores)
            out = []
            for it, s in zip(items, scores):
                out.append((it["name"], max(1, round(budget * s / tot))))
            # trim to budget
            while sum(c for _, c in out) > budget and out:
                out.sort(key=lambda x: -x[1])
                out[0] = (out[0][0], out[0][1] - 1)
                out = [(nm, c) for nm, c in out if c > 0]
            return out

        return {
            "n_candidates": n_candidates,
            "recent_accept_rate": rate,
            "weights": {"exploit": w[0], "probe": w[1], "explore": w[2]},
            "exploit": _spread(succ, n_exploit,
                               lambda p: p["success_rate"] or 0),
            "probe": _spread(und, n_probe,
                             lambda p: (p["success_rate"] or 0) + 0.1),
            "explore": _spread(ins, n_explore, lambda i: 1.0),
            "avoid": [p["name"] for p in self.forbidden_patterns()],
        }

    # ------------------------------------------------------------ persist
    def save(self):
        self.mem_path.write_text(json.dumps(self.state, indent=2,
                                            ensure_ascii=False))

    # ------------------------------------------------------------ back-compat
    # legacy free-text distill calls -> curated pinned patterns
    def add_success(self, pattern: str, evidence: str, round_id: int):
        return self.merge(_slug(pattern), description=pattern,
                          evidence=evidence, round_id=round_id,
                          classification="success", curated=True)

    def add_forbidden(self, pattern: str, evidence: str, round_id: int):
        return self.merge(_slug(pattern), description=pattern,
                          evidence=evidence, round_id=round_id,
                          classification="forbidden", curated=True)
