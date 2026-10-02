"""Per-matchup canonical metrics from any result CSV, with the correct interval.

One place that computes a matchup's numbers, so no report can quote a
decided-only rate when it means the BT score rate, or a game-level interval when
the experiment is paired and both-seat.

    python benchmark/match_metrics.py experiments/p3066/c001_vs_farm_full.csv
"""
import argparse
import csv
import json
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))

from stats import (binom_two_sided, mcnemar_exact,  # noqa: E402
                   paired_seed_bootstrap, win_interval)

MIGRATION_BACKUP = ".pre_tie_fix"


def load(paths):
    rows = []
    for p in paths:
        if os.sep + "seeds" + os.sep in p:
            continue
        base = os.path.basename(p)
        if MIGRATION_BACKUP in base:
            # A preserved original from the tie migration. Aggregating it would
            # double-count every restored game.
            continue
        with open(p, encoding="utf-8", newline="") as fh:
            rows += list(csv.DictReader(fh))
    return rows


def metrics(rows, label=""):
    valid, broken = [], []
    for r in rows:
        if r.get("valid") == "1":
            valid.append(r)
            continue

        def ok(side):
            try:
                return (int(r.get(f"{side}_calls", 0)) >= 714
                        and r.get(f"{side}_status") == "DONE")
            except (TypeError, ValueError):
                return False
        (valid if ok("candidate") and ok("opponent") else broken).append(r)

    W = sum(int(r["win"]) for r in valid)
    L = sum(int(r["loss"]) for r in valid)
    T = sum(int(r["tie"]) for r in valid)
    d = win_interval(W, L, T)

    per = defaultdict(list)
    for r in valid:
        s = 1.0 if int(r["win"]) else (0.5 if int(r["tie"]) else 0.0)
        per[int(r["seed"])].append(s)
    bm, blo, bhi, nk = paired_seed_bootstrap(per, iters=20000)

    seat = {0: [0, 0], 1: [0, 0]}
    disc = [0, 0]
    for r in valid:
        w, l = int(r["win"]), int(r["loss"])
        if w:
            seat[int(r["seat"])][0] += 1
        if l:
            seat[int(r["seat"])][1] += 1
        if w and not l:
            disc[0] += 1
        elif l and not w:
            disc[1] += 1
    mcp, _nd = mcnemar_exact(disc[0], disc[1])
    margins = sorted(int(r["candidate_cash"]) - int(r["opponent_cash"])
                     for r in valid)
    rt = sorted([float(r.get("candidate_runtime_max") or 0) for r in valid]
                + [float(r.get("opponent_runtime_max") or 0) for r in valid])

    return {
        "label": label or (valid[0].get("candidate_name") if valid else "?"),
        "opponent": valid[0].get("opponent_name") if valid else "?",
        "games_run": len(rows), "valid": len(valid), "broken": len(broken),
        "W": W, "L": L, "T": T, "N": W + L + T,
        "PRIMARY_bt_score_rate": round(d["bt_score_rate"], 6),
        "bt_lo95_seed_bootstrap": round(blo, 6),
        "bt_hi95_seed_bootstrap": round(bhi, 6),
        "n_seeds": nk,
        "secondary_decided_win_rate": round(d["decided_win_rate"], 6),
        "decided_wilson_lo": round(d["wilson_decided_lo"], 6),
        "decided_wilson_hi": round(d["wilson_decided_hi"], 6),
        "tie_rate": round(d["tie_rate"], 6),
        "binom_p_decided": binom_two_sided(W, W + L),
        "mcnemar_p": mcp,
        "seat0_W_L": seat[0], "seat1_W_L": seat[1],
        "mean_margin": round(sum(margins) / len(margins), 1) if margins else 0,
        "median_margin": margins[len(margins) // 2] if margins else 0,
        "runtime_max_ms": rt[-1] if rt else 0,
        "runtime_median_ms": rt[len(rt) // 2] if rt else 0,
        "clear_of_50": blo > 0.5,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    paths = []
    for p in a.paths:
        if os.path.isdir(p):
            import glob
            paths += sorted(glob.glob(os.path.join(p, "*.csv")))
        else:
            paths.append(p)
    rows = load(paths)
    m = metrics(rows)
    if a.json:
        print(json.dumps(m, indent=2))
        return 0
    print(f"{m['label']} vs {m['opponent']}")
    print(f"  W-L-T              : {m['W']}-{m['L']}-{m['T']}  of {m['N']} "
          f"(broken {m['broken']})")
    print(f"  BT score rate      : {m['PRIMARY_bt_score_rate']:.4f}   <- PRIMARY")
    print(f"  95% (seed bootstrap): [{m['bt_lo95_seed_bootstrap']:.4f}, "
          f"{m['bt_hi95_seed_bootstrap']:.4f}]  over {m['n_seeds']} seeds")
    print(f"    clears 0.50      : {m['clear_of_50']}")
    print(f"  decided-only       : {m['secondary_decided_win_rate']:.4f}   "
          f"Wilson [{m['decided_wilson_lo']:.4f}, {m['decided_wilson_hi']:.4f}]")
    print(f"  tie rate           : {m['tie_rate']:.4f}")
    print(f"  seat 0 W/L         : {m['seat0_W_L']}")
    print(f"  seat 1 W/L         : {m['seat1_W_L']}")
    print(f"  mean/median margin : ${m['mean_margin']} / ${m['median_margin']}")
    print(f"  runtime max/median : {m['runtime_max_ms']} / "
          f"{m['runtime_median_ms']} ms")
    return 0


if __name__ == "__main__":
    sys.exit(main())
