#!/usr/bin/env python3
"""Build the curated `robust_2026` set: factors that are robust in BOTH 2017-25
and 2026, tradable net of cost, and NOT overnight-gap.

Membership (24):
  - 5 newly-mined robust+efficient factors (Rounds 13-14) — MOVED out of
    behavioral_full (retired there, they live only here).
  - 19 distinct "past" factors that were valid AND efficient in the 2026
    per-factor screen (VALID_2026.md), excluding the overnight-gap vein,
    deduped cross-set (behavioral_full preferred over its canonical twins).

Copies each factor's stored values + metrics into the new set's registry with
provenance (source_set/source_name + 2026 stats). Run once.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mining.registry import Registry            # noqa: E402
from mining.memory import Memory                # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
NEW = "robust_2026"

# 5 newly-mined robust+efficient (all in behavioral_full / "main"), with 2026 net
NEW5 = [("main", "alpha_0155"), ("main", "alpha_0144"), ("main", "alpha_0152"),
        ("main", "alpha_0146"), ("main", "alpha_0153")]


def stats_2026():
    """signed_ic_2026 + net for every factor we copy, from the screen/round JSONs."""
    s = {}
    scr = json.loads((ROOT / "results/mining/valid_2026_screen.json").read_text())
    for r in scr["all_factors"]:
        s[(r["set"], r["name"])] = (r["signed_ic_2026"], r["net_excess_15bp_2026"])
    for rj in ("round13_2026.json", "round14_2026.json"):
        for r in json.loads((ROOT / "results/mining/sets/behavioral_full" / rj).read_text()):
            s[("behavioral_full", r["name"])] = (r["signed_ic_2026"], r["net15_2026"])
    return s


SET_ARG = {"behavioral_full": "main", "canonical": "canonical",
           "canonical_composite": "canonical_composite"}


def main():
    st = stats_2026()
    past = json.loads((ROOT / "results/mining/_robust2026_past.json").read_text())

    # provenance rows: (source_set_label, source_name, tag)
    rows = [("behavioral_full", n, "mined_R13-14") for _, n in NEW5]
    rows += [(r["set"], r["name"], "past_valid_2026") for r in past]

    reg_new = Registry(NEW)
    if reg_new.active():
        raise SystemExit(f"{NEW} already has factors; refusing to rebuild.")
    src_regs = {}
    for src_label, name, tag in rows:
        arg = SET_ARG[src_label]
        reg = src_regs.setdefault(arg, Registry(arg))
        e = reg.get(name)
        if e is None:
            print(f"  !! {src_label}:{name} not active, skipping"); continue
        vals = reg.values(name)
        sic, net = st.get((src_label, name), (None, None))
        entry = reg_new.add(e["expression"], e["family"],
                            f"[{tag} from {src_label}:{name}] {e.get('rationale','')}",
                            e["direction"], e["metrics"], 0, vals,
                            e.get("logic_score", 0.0))
        entry["source_set"] = src_label
        entry["source_name"] = name
        entry["provenance"] = tag
        entry["signed_ic_2026"] = sic
        entry["net_excess_15bp_2026"] = net
        print(f"  {entry['name']} <- {src_label}:{name} [{e['family']}] "
              f"2026 sIC {sic:+.3f} net {net:+.1%}" if sic is not None
              else f"  {entry['name']} <- {src_label}:{name}")
    reg_new.save(); reg_new.export_csv()
    print(f"{NEW}: {len(reg_new.active())} factors written")

    # MOVE: retire the 5 newly-mined from behavioral_full
    main_reg = src_regs.get("main") or Registry("main")
    for _, name in NEW5:
        main_reg.retire(name, f"moved to {NEW} curated set", 14)
    main_reg.save(); main_reg.export_csv()
    print(f"behavioral_full: {len(main_reg.active())} active after moving 5 out")

    # minimal experience memory so future rounds can target this set
    Memory(NEW).save()
    print("wrote empty experience_memory for future mining")


if __name__ == "__main__":
    main()
