#!/usr/bin/env python3
"""Turnover-reduction overlay: hysteresis / buffer bands on the top-decile long
book. A name ENTERS only in the top decile (rank > 1-1/Q) but is HELD until it
falls out of a wider band (rank > 1 - buffer/Q), so boundary names don't churn.

COST_ANALYSIS showed cost binds at the composite (turnover ~0.48/rebalance). This
sweep finds the buffer that maximizes net-of-cost long-excess: wider band -> lower
turnover, but too wide holds decayed names and gross excess fades.

Run: python3 code/turnover_overlay.py <set_name>  (neutralized composite, stored values)
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
Q = 10
PPY = 250 / cfg.HORIZON
COST_BPS = (15, 30)
BUFFERS = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0]     # 1.0 = no buffer (plain top decile)


def run_book(comp, label, mask, buffer):
    """Walk rebalances with a hysteresis long book; return per-period excess,
    turnover, book size."""
    entry = 1 - 1.0 / Q
    exit_ = 1 - buffer / Q
    dates = comp.index[::cfg.HORIZON]
    C = ae._masked(comp, mask); L = ae._masked(label, mask)
    prev = set()
    exc, turn, sizes = [], [], []
    for d in dates:
        s, l = C.loc[d], L.loc[d]
        ok = s.notna() & l.notna()
        if ok.sum() < 200:
            continue
        rk = s[ok].rank(pct=True)
        strong = set(rk.index[rk > entry])
        kept = {n for n in prev if n in rk.index and rk[n] > exit_}
        book = strong | kept
        if not book:
            continue
        exc.append(float(l[list(book)].mean()) - float(l[ok].mean()))
        turn.append(1.0 if not prev else 1 - len(book & prev) / max(len(book), 1))
        sizes.append(len(book))
        prev = book
    exc, turn = np.array(exc), np.array(turn)
    ann = lambda a: float((1 + a).prod() ** (PPY / len(a)) - 1)
    out = {"buffer": buffer, "avg_turnover": float(turn.mean()),
           "avg_book": float(np.mean(sizes)), "n_rebal": len(exc),
           "excess_gross_ann": ann(exc)}
    for bp in COST_BPS:
        c = bp / 1e4
        out[f"excess_net_{bp}bp_ann"] = ann(exc - turn * 2 * c)
    return out


def main(set_name):
    panel = Panel()
    mask = panel.universe_mask("all")
    label = panel.label(cfg.HORIZON)
    comp, n = cs.set_composite(Registry(set_name), panel, mask, "stored")
    comp = cs.neutralize_factor(comp, panel, mask)
    print(f"[{set_name}] {n} factors, neutralized composite; sweeping buffers\n")
    rows = [run_book(comp, label, mask, b) for b in BUFFERS]
    print(f"{'buffer':>7} {'turnover':>9} {'book':>6} {'gross':>8} {'net15':>8} {'net30':>8}")
    for r in rows:
        print(f"{r['buffer']:>7.1f} {r['avg_turnover']:>9.2f} {r['avg_book']:>6.0f} "
              f"{r['excess_gross_ann']:>+8.1%} {r['excess_net_15bp_ann']:>+8.1%} "
              f"{r['excess_net_30bp_ann']:>+8.1%}")
    base = rows[0]
    best15 = max(rows, key=lambda r: r["excess_net_15bp_ann"])
    print(f"\nbaseline (no buffer): turnover {base['avg_turnover']:.2f}, "
          f"net15 {base['excess_net_15bp_ann']:+.1%}, net30 {base['excess_net_30bp_ann']:+.1%}")
    print(f"best net15 at buffer {best15['buffer']:.1f}: turnover {best15['avg_turnover']:.2f}, "
          f"net15 {best15['excess_net_15bp_ann']:+.1%} "
          f"(+{(best15['excess_net_15bp_ann']-base['excess_net_15bp_ann'])*100:.1f}pp), "
          f"net30 {best15['excess_net_30bp_ann']:+.1%} "
          f"(+{(best15['excess_net_30bp_ann']-base['excess_net_30bp_ann'])*100:.1f}pp)")
    p = ROOT / "results" / "mining" / "sets" / \
        ("behavioral_full" if set_name == "main" else set_name) / "turnover_overlay.json"
    p.write_text(json.dumps({"set": set_name, "n_factors": n, "Q": Q,
                             "rows": rows}, indent=2, default=float))
    print(f"-> {p}")
    return rows


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "robust_2026")
