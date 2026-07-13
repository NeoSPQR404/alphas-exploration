#!/usr/bin/env python3
"""Rebuild each set's experience memory into schema v2.

Idempotent: family-level pattern stats are derived purely from the round
JSONs (occurrence/accept counts, success rate); curated narrative
patterns are carried over from the pre-existing memory as pinned,
zero-occurrence entries; a small set of exploration insights is seeded.

Run: python3 code/rebuild_memory.py
"""
import glob
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from mining.memory import Memory, _slug   # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SETS = ["behavioral_full", "canonical", "canonical_composite"]

# short human templates for the families we know; fallback is a
# representative expression pulled from the round JSONs.
FAMILY_TEMPLATE = {
    "reversal": "-TsSum(intraday_or_close_return, n)  /  -median-stretch",
    "overnight": "aggregate(gap = OPEN/Delay(CLOSE,1)-1) over n",
    "lottery": "-TsMax/TsMin(RET, n)  /  extreme-day counts",
    "volatility": "vol shape/term/semivol-asymmetry over n",
    "aggression": "aggregate(CLOSE/VWAP-1) over n",
    "volume": "normalized-volume level/rank/clock structures",
    "turnover": "-TsMean/rank(turnover) structures",
    "conditional": "-TsSum(X * day_condition, n)",
    "asymmetry": "-(TsStd(X*(RET>0),n) - TsStd(X*(RET<0),n))",
    "coupling": "-TsCorr(quantity_A, quantity_B, n)",
    "daytype": "count/magnitude/texture over gap x intraday day-types",
    "truegap": "range-breaking gaps: OPEN vs prior HIGH/LOW",
    "stalemate": "-TsCount(|CLOSE/VWAP-1| < eps, n)  (pins/dojis)",
    "vol_at_ext": "aggregate(X on days making 20d high/low)",
    "occupancy": "-TsCount(price in zone, n)",
    "acceleration": "-(mean_n / mean_n_lagged)  fortnight/month ratios",
    "liquidity": "Amihud / zero-return / dollar-depth structures",
    "event": "-TsCount(threshold event, n)",
    "pair": "(CsRank(A)-.5)*(CsRank(B)-.5)  demeaned-rank product",
    "threeway": "(CsRank(A)-.5)*(CsRank(B)-.5)*(CsRank(C)-.5)",
    "composition": "demeaned-rank pair product of two parents",
    "composition3": "demeaned-rank three-way product",
}

# exploration insights to seed per set (untested factor directions)
INSIGHTS = {
    "canonical": [
        ("gap-path-shape",
         "Shape of the intraday path relative to the open, not just its endpoint",
         "Constructs summarizing whether price trended or churned within "
         "the day (e.g. area between CLOSE-path proxy and OPEN) may carry "
         "signal the leg-return factors miss."),
        ("regime-conditional-signals",
         "Condition an existing factor on the stock's own trend/vol regime",
         "A factor's edge may concentrate in one regime; splitting by "
         "own 60d trend sign or vol tercile could sharpen it — a new "
         "structural axis, not a new formula."),
        ("twenty-day-label-track",
         "Mine the slow material (value/quality/northbound) at a 20d horizon",
         "EP/CFP levels and northbound accumulation half-pass at 10d; a "
         "20d-label sub-track may clear them and open a low-turnover set."),
    ],
    "behavioral_full": [
        ("northbound-flow-acceleration",
         "Second-difference of northbound holding ratio",
         "Levels/deltas of HK_RATIO were dead at 10d; the acceleration of "
         "foreign accumulation may be the event that prices."),
        ("margin-unwind-events",
         "Detect forced-deleveraging days from margin balance drops",
         "Sharp financing-balance contractions on down days may mark "
         "capitulation the flow-level factors cannot see."),
    ],
    "canonical_composite": [
        ("four-way-products",
         "Extend the composition tier to four-parent products",
         "3-ways are the richest tier; a 4th demeaned-rank factor may add "
         "orthogonal conditioning before the tier self-locks."),
        ("sign-conditioned-composition",
         "Gate a parent by the sign of another rather than multiply ranks",
         "Products blend two rankings symmetrically; a sign-gate "
         "(A where B>median) is a different, asymmetric interaction."),
    ],
}


def scan_families(set_name: str):
    folder = set_name
    rounds = sorted(glob.glob(str(ROOT / "results" / "mining" / "sets"
                                  / folder / "rounds" / "round_*.json")))
    stats = {}
    for f in rounds:
        rd = json.loads(Path(f).read_text().replace("NaN", "null"))
        rid = rd.get("round")
        for c in rd.get("results", []):
            fam = c.get("family", "unknown")
            s = stats.setdefault(fam, {"occ": 0, "acc": 0, "rounds": set(),
                                       "expr_any": None, "expr_acc": None})
            s["occ"] += 1
            s["rounds"].add(rid)
            if c.get("expr") and s["expr_any"] is None:
                s["expr_any"] = c["expr"]
            if "accepted_name" in c:
                s["acc"] += 1
                if c.get("expr") and (s["expr_acc"] is None
                                      or len(c["expr"]) < len(s["expr_acc"])):
                    s["expr_acc"] = c["expr"]
    return stats


def carry_curated(old_state: dict):
    """Yield (name, description, evidence, classification, rounds) for the
    curated narrative patterns in a pre-existing memory (old or new)."""
    for bucket, cls in (("successful_patterns", "success"),
                        ("forbidden_patterns", "forbidden")):
        for p in old_state.get(bucket, []):
            if "pattern" in p:          # old free-text format
                yield (_slug(p["pattern"]), p["pattern"],
                       p.get("evidence", ""), cls, p.get("rounds", []))
    for p in old_state.get("patterns", {}).values():   # already-v2 curated
        if p.get("curated"):
            yield (p["name"], p["description"], p.get("evidence", ""),
                   p["classification"], p.get("rounds", []))


def rebuild(set_name: str):
    reg_name = "main" if set_name == "behavioral_full" else set_name
    raw = _mem_raw(set_name)
    curated = list(carry_curated(raw))
    existing_insights = raw.get("insights", {})
    rounds_log = raw.get("rounds", [])

    m = Memory(reg_name)
    m.state["patterns"] = {}            # fresh: idempotent rebuild
    m.state["rounds"] = rounds_log
    m.state["insights"] = existing_insights

    fam_stats = scan_families(set_name)
    for fam, s in sorted(fam_stats.items()):
        tmpl = FAMILY_TEMPLATE.get(fam) or (s["expr_acc"] or s["expr_any"] or fam)
        for r in sorted(x for x in s["rounds"] if x is not None):
            m.merge(fam, description=f"factor family: {fam}", template=tmpl,
                    occurrences=0, accepts=0, round_id=r)
        # add the totals in one shot (rounds already recorded)
        m.merge(fam, occurrences=s["occ"], accepts=s["acc"])

    # curated narrative patterns as pinned, zero-occurrence entries
    for name, desc, ev, cls, rnds in curated:
        m.merge(name, description=desc, evidence=ev, classification=cls,
                curated=True)
        for r in rnds:
            m.state["patterns"][name]["rounds"] = sorted(
                set(m.state["patterns"][name]["rounds"] + [r]))

    for name, desc, hyp in INSIGHTS.get(set_name, []):
        if name not in m.state["insights"]:
            m.insight(name, description=desc, hypothesis=hyp)

    m.save()
    succ = len(m.successful_patterns()); forb = len(m.forbidden_patterns())
    und = len(m.undetermined_patterns()); ins = len(m.state["insights"])
    print(f"[{set_name}] families {len(fam_stats)} | patterns "
          f"success {succ} forbidden {forb} undetermined {und} "
          f"| curated {len(curated)} | insights {ins}")


def _mem_raw(set_name: str) -> dict:
    p = (ROOT / "results" / "mining" / "sets" / set_name
         / "experience_memory.json")
    return json.loads(p.read_text()) if p.exists() else {}


if __name__ == "__main__":
    for s in SETS:
        rebuild(s)
