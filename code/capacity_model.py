#!/usr/bin/env python3
"""Capacity-aware cost model: how much AUM can the deployable book run before
market impact erodes the alpha?

Book = robust_2026 neutralized composite, buffer 2.5, top-decile EW long (the
deployable book). For a given AUM, each of the N held names is a position of
AUM/N; at each rebalance we trade the entries (buy) and exits (sell). Cost per
name = fixed (commission + half-spread [+ stamp on sells]) + market impact, with
a **square-root impact law** impact_bp = Y * sqrt(trade_value / ADV) (Almgren-
style), capped. ADV = trailing-20d median dollar volume. We sweep AUM and report
the net-excess capacity curve for an impact coefficient Y with a sensitivity band.

ASSUMPTIONS (stated so they can be recalibrated) — A-share retail/institutional:
  commission 2.5bp/side, half-spread 5bp/side, stamp duty 5bp SELL-side only,
  impact Y=120bp at 100% ADV participation (opt 80 / pess 180), impact cap 300bp.
Everything is transparent; exact capacity scales with Y and the ADV distribution.

Run: python3 code/capacity_model.py
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mining import alphaseval as ae          # noqa: E402
from mining import config as cfg             # noqa: E402
from mining import construct as cs           # noqa: E402
from mining.data import Panel                # noqa: E402
from mining.registry import Registry         # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
Q, BUFFER = 10, 2.5
PPY = 250 / cfg.HORIZON
COMMISSION, HALF_SPREAD, STAMP = 2.5, 5.0, 5.0     # bp
Y_VARIANTS = {"optimistic": 80.0, "base": 120.0, "pessimistic": 180.0}
IMPACT_CAP = 300.0                                  # bp one-way
AUM_GRID = [1e8, 3e8, 1e9, 3e9, 1e10, 3e10, 1e11]   # 0.1B .. 100B CNY


def build_book(comp, label, adv, mask):
    """Walk the buffered top-decile book; per rebalance record entries/exits ADV,
    N, long gross, universe mean."""
    entry, exit_ = 1 - 1.0 / Q, 1 - BUFFER / Q
    dates = comp.index[::cfg.HORIZON]
    C, L = ae._masked(comp, mask), ae._masked(label, mask)
    prev, recs = set(), []
    for d in dates:
        s, l, a = C.loc[d], L.loc[d], adv.loc[d]
        ok = s.notna() & l.notna()
        if ok.sum() < 200:
            continue
        rk = s[ok].rank(pct=True)
        strong = set(rk.index[rk > entry])
        kept = {n for n in prev if n in rk.index and rk[n] > exit_}
        book = strong | kept
        if not book:
            continue
        entries, exits = book - prev, prev - book

        def advs(names):
            v = a.reindex(list(names)).to_numpy(dtype=float)
            v[~np.isfinite(v) | (v <= 0)] = np.nan     # missing -> illiquid
            return v
        recs.append({"N": len(book), "long": float(l[list(book)].mean()),
                     "uni": float(l[ok].mean()),
                     "adv_e": advs(entries), "adv_x": advs(exits)})
        prev = book
    return recs


def cost_frac(rec, aum, Y):
    """Per-rebalance trading cost as a fraction of AUM (sum over traded names of
    (position/AUM) * cost_bp / 1e4, with position = AUM/N)."""
    N = rec["N"]
    pos = aum / N

    def leg(adv, extra):
        if adv.size == 0:
            return 0.0
        part = pos / adv                              # nan where ADV missing
        imp = np.minimum(Y * np.sqrt(np.clip(part, 0, None)), IMPACT_CAP)
        imp = np.where(np.isfinite(imp), imp, IMPACT_CAP)   # illiquid -> cap
        cb = COMMISSION + HALF_SPREAD + extra + imp
        return float(np.sum(cb)) / N / 1e4
    return leg(rec["adv_e"], 0.0) + leg(rec["adv_x"], STAMP)


def ann(series):
    a = np.array(series)
    return float((1 + a).prod() ** (PPY / len(a)) - 1)


def main():
    panel = Panel()
    mask = panel.universe_mask("all")
    label = panel.label(cfg.HORIZON)
    comp, n = cs.set_composite(Registry("robust_2026"), panel, mask, "stored")
    comp = cs.neutralize_factor(comp, panel, mask)
    adv = (panel.wide("AMOUNT") * 1000.0).rolling(20).median()   # yuan
    print(f"robust_2026 {n} factors; building book + capacity curve\n")
    recs = build_book(comp, label, adv, mask)
    gross = ann([r["long"] - r["uni"] for r in recs])
    avg_N = np.mean([r["N"] for r in recs])
    print(f"book: {len(recs)} rebalances, avg {avg_N:.0f} names, "
          f"frictionless gross excess {gross:+.1%}\n")

    out = {"set": "robust_2026", "n_factors": n, "buffer": BUFFER,
           "assumptions": {"commission_bp": COMMISSION, "half_spread_bp": HALF_SPREAD,
                           "stamp_bp_sell": STAMP, "impact_Y_bp": Y_VARIANTS,
                           "impact_cap_bp": IMPACT_CAP, "law": "impact=Y*sqrt(trade/ADV)"},
           "gross_excess_ann": gross, "avg_book": avg_N, "curve": {}}
    hdr = "     AUM(CNY)  " + "".join(f"{k:>13}" for k in Y_VARIANTS)
    print(hdr + "   (net excess ann)")
    for aum in AUM_GRID:
        nets = {}
        for k, Y in Y_VARIANTS.items():
            nets[k] = ann([r["long"] - cost_frac(r, aum, Y) - r["uni"] for r in recs])
        out["curve"][f"{aum:.0f}"] = nets
        lab = f"{aum/1e8:.0f}亿" if aum < 1e10 else f"{aum/1e8:.0f}亿"
        print(f"  {aum:>12,.0f}  " + "".join(f"{nets[k]:>+13.1%}" for k in Y_VARIANTS))

    # capacity: AUM where BASE net excess falls to half of the small-AUM (1e8) level
    base = {a: out["curve"][f"{a:.0f}"]["base"] for a in AUM_GRID}
    small = base[AUM_GRID[0]]
    half_cap = None
    for a in AUM_GRID:
        if base[a] < small / 2 and half_cap is None:
            half_cap = a
    out["small_aum_net"] = small
    out["half_capacity_cny"] = half_cap
    (ROOT / "results" / "mining" / "capacity_model.json").write_text(
        json.dumps(out, indent=2, default=float))
    print(f"\nsmall-AUM (0.1B) base net excess: {small:+.1%}")
    print(f"half-alpha capacity (base Y): ~{half_cap/1e8:.0f}亿 CNY" if half_cap
          else "half-alpha capacity: > 100B (not reached in grid)")
    print("-> results/mining/capacity_model.json")


if __name__ == "__main__":
    main()
