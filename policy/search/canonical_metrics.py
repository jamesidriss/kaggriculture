"""Canonical match metrics, recomputed from migrated raw rows.

Every number the project has ever published about C001 was computed under the
wrong rule in one of two ways:

  * it counted an exact cash tie as an INVALID game and threw it away, or
  * it reported W/(W+L) and called it a "win rate" when 18% of the games were
    draws and Kaggle scores a draw as half a win.

This script recomputes everything from the raw per-game rows, after migration,
and prints all three numbers side by side with their intervals. Nothing here is
transcribed by hand.

The headline correction:

    657-155-180 of 992      decided-only win rate  80.91%   <- what we said
                            BT score rate         75.30%   <- the match score
                            tie rate              18.15%

and the replication is the real story:

    638-138-216 of 992      decided-only 82.22%,  BT score 75.20%
    657-155-180 of 992      decided-only 80.91%,  BT score 75.30%

The two runs disagree by 1.3 points on the decided-only rate but agree to a
tenth of a point on the score that Kaggle actually uses. That is much stronger
evidence than either figure alone.
"""
import csv
import glob
import json
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))

from stats import (bt_score_rate, paired_seed_bootstrap,  # noqa: E402
                   win_interval)

OUT = os.path.join(ROOT, "simulation", "search", "canonical_metrics.json")

# (label, glob, candidate label filter, opponent label filter)
MATCHUPS = [
    ("C001 vs v51  (decisive leg 1)",
     "simulation/search/decisive/vh/r_*.csv", None, None),
    ("C001 vs v51  (promotion leg B)",
     "experiments/promotion/b_parent/r_*.csv", None, None),
    ("C001 vs 2945 Farm  (decisive leg 2)",
     "simulation/search/decisive/vf/r_*.csv", None, None),
    ("C001 vs 2945 Farm  (promotion leg B)",
     "experiments/promotion/b_farm/r_*.csv", None, None),
    ("v51 vs 2945 Farm  (decisive leg 3)",
     "simulation/search/decisive/pf/r_*.csv", None, None),
]


# Preserved originals from the tie migration must NEVER be aggregated as
# results. They end in `.csv`, so a glob of `r_*.csv` matches both the live
# file and its backup, which silently DOUBLE-COUNTED every restored game: the
# decisive leg reported 1,984 games when only 992 were ever played.
# The first version of this script had exactly that bug.
MIGRATION_BACKUP = ".pre_tie_fix"


def load(pattern):
    rows = []
    for f in sorted(glob.glob(os.path.join(ROOT, pattern))):
        if MIGRATION_BACKUP in os.path.basename(f):
            continue
        with open(f, encoding="utf-8", newline="") as fh:
            rows += list(csv.DictReader(fh))
    return rows


def canonical(rows):
    """Recompute from raw rows using the corrected validity rule."""
    valid, broken = [], []
    for r in rows:
        if r.get("valid") == "1":
            valid.append(r)
            continue
        # Independently re-derive: a game is broken only for a real defect.
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

    scores = [0.0] * W + [1.0] * L + [0.5] * T
    per_seed = defaultdict(list)
    for r in valid:
        s = 1.0 if int(r["win"]) else (0.5 if int(r["tie"]) else 0.0)
        per_seed[int(r["seed"])].append(s)
    bm, blo, bhi, nseeds = paired_seed_bootstrap(per_seed, iters=20000)

    margins = sorted(int(r["candidate_cash"]) - int(r["opponent_cash"])
                     for r in valid)
    seat = {0: [0, 0], 1: [0, 0]}
    for r in valid:
        if int(r["win"]):
            seat[int(r["seat"])][0] += 1
        elif int(r["loss"]):
            seat[int(r["seat"])][1] += 1
    rt = [float(r["candidate_runtime_max"] or 0) for r in valid]
    rt += [float(r["opponent_runtime_max"] or 0) for r in valid]
    rt.sort()

    return {
        "games": len(rows), "valid": len(valid), "broken": len(broken),
        "W": W, "L": L, "T": T,
        "bt_score_rate": round(d["bt_score_rate"], 6),
        "bt_score_lo95_seed_bootstrap": round(blo, 6),
        "bt_score_hi95_seed_bootstrap": round(bhi, 6),
        "n_seeds": nseeds,
        "decided_win_rate": round(d["decided_win_rate"], 6),
        "decided_wilson_lo": round(d["wilson_decided_lo"], 6),
        "decided_wilson_hi": round(d["wilson_decided_hi"], 6),
        "tie_rate": round(d["tie_rate"], 6),
        "mean_margin": round(sum(margins) / len(margins), 1) if margins else 0,
        "median_margin": margins[len(margins) // 2] if margins else 0,
        "seat_wins": {str(k): v for k, v in seat.items()},
        "runtime_max_ms": rt[-1] if rt else 0,
        "runtime_median_ms": rt[len(rt) // 2] if rt else 0,
    }


def main():
    print("=" * 92)
    print("CANONICAL MATCH METRICS - recomputed from migrated raw rows")
    print("=" * 92)
    print("PRIMARY metric = BT score rate = (W + 0.5T)/N, which is how Kaggle's")
    print("final Bradley-Terry scores a draw.  Secondary = decided-only W/(W+L).\n")
    hdr = (f"{'matchup':<38}{'W-L-T':>16}{'N':>6}{'BT':>8}"
           f"{'BT 95% (seed)':>20}{'dec%':>8}{'ties':>7}{'mean$':>9}")
    print(hdr)
    print("-" * 92)
    results = {}
    for label, pattern, _a, _b in MATCHUPS:
        rows = load(pattern)
        if not rows:
            continue
        m = canonical(rows)
        results[label] = m
        rec = f"{m['W']}-{m['L']}-{m['T']}"
        ci = f"[{m['bt_score_lo95_seed_bootstrap']:.4f}, {m['bt_score_hi95_seed_bootstrap']:.4f}]"
        print(f"{label:<38}{rec:>16}{m['valid']:>6}{m['bt_score_rate']:>8.4f}"
              f"{ci:>20}{m['decided_win_rate']:>8.4f}{m['tie_rate']:>7.3f}"
              f"{m['mean_margin']:>9.0f}")

    # The replication is the finding.
    k1 = "C001 vs v51  (decisive leg 1)"
    k2 = "C001 vs v51  (promotion leg B)"
    if k1 in results and k2 in results:
        a, b = results[k1], results[k2]
        print("\n" + "=" * 92)
        print("THE REPLICATION, IN BOTH METRICS")
        print("=" * 92)
        print(f"  decided-only : {a['decided_win_rate']:.4f}  vs "
              f"{b['decided_win_rate']:.4f}   "
              f"disagreement {abs(a['decided_win_rate']-b['decided_win_rate'])*100:.2f} pts")
        print(f"  BT score rate: {a['bt_score_rate']:.4f}  vs "
              f"{b['bt_score_rate']:.4f}   "
              f"disagreement {abs(a['bt_score_rate']-b['bt_score_rate'])*100:.2f} pts")
        print("\n  Two independent seed sets agree to a tenth of a point on the")
        print("  metric the competition actually uses. That is the strong form")
        print("  of this evidence, and it was invisible while the primary number")
        print("  was the decided-only rate.")

    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(results, fh, indent=2)
    print(f"\nwrote {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
