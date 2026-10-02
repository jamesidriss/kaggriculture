"""Correct the classification of the room_guard experiment's games, and report
it honestly.

The trap
--------
`benchmark/tournament.py` marks a game INVALID when the two sides finish with
exactly equal cash, and records the reason as "exact tie (duplicate-content
signal)". That rule exists: the project's worst historical error was fake
self-play, where two content-identical files were scored against each other and
the resulting numbers looked like a real result.

But it is a heuristic about a DIFFERENT situation, and applying it here is
wrong in a way that inflates the answer:

  * the two files here have different SHA256 digests, so this is not self-play;
  * the only change is one gene in a settings literal;
  * on worlds where that gene never fires, both agents follow identical
    trajectories and finish with identical cash.

So those 216 games are genuine no-op worlds, not invalid ones. Counting them as
invalid REMOVES EXACTLY THE WORLDS WHERE THE CHANGE DID NOTHING, which biases
the measured win rate upward. The screen that produced a 0.82 win rate was
partly measuring its own exclusion rule.

What is reported instead
------------------------
  * every game where both agents ran to completion is VALID;
  * exact ties are recorded separately as `inert_worlds`, because a tie here is
    a finding about the gene, not a defect;
  * win rate is given over DECIDED games (the statistically correct denominator)
    AND as a share of all games, so nothing is hidden;
  * the guard's behaviour is checked explicitly, and the fact that it fired on
    216 legitimate games is reported as a defect in the guard.

If the verdict survives reclassification, it is real. If it does not, the
reclassification is what caught it.
"""
import csv
import glob
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))

from benchmark.stats import (binom_two_sided, mcnemar_exact,  # noqa: E402
                             win_interval)

VARIANT = os.path.join(ROOT, "simulation", "search", "baseline_plus_room_guard.py")
PARENT = os.path.join(ROOT, "opponents", "meta", "ahmedberatozer-v51-lean-flock.py")
OUT = os.path.join(ROOT, "simulation", "search", "room_guard_verdict.json")
COMPLETE_CALLS = 714          # 719 expected; the gate allows EXPECTED_TURNS - 5


def load(tag):
    rows = []
    for f in sorted(glob.glob(os.path.join(ROOT, "simulation", "search",
                                           "decisive", tag, "r_*.csv"))):
        rows += list(csv.DictReader(open(f, encoding="utf-8")))
    return rows


def classify(rows):
    """Split a raw result set into: completed, exact-tie, and genuinely broken."""
    done, ties, broken = [], [], []
    for r in rows:
        if (r.get("candidate_status") != "DONE"
                or r.get("opponent_status") != "DONE"):
            broken.append((r, "status not DONE"))
            continue
        try:
            if (int(r["candidate_calls"]) < COMPLETE_CALLS
                    or int(r["opponent_calls"]) < COMPLETE_CALLS):
                broken.append((r, "under-called"))
                continue
        except (TypeError, ValueError):
            broken.append((r, "call count unreadable"))
            continue
        if int(r["tie"]):
            ties.append(r)
        else:
            done.append(r)
    return done, ties, broken


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def analyse(rows, label):
    done, ties, broken = classify(rows)
    W = sum(int(r["win"]) for r in done)
    L = sum(int(r["loss"]) for r in done)
    iv = win_interval(W, L, len(ties))
    all_games = len(done) + len(ties) + len(broken)
    seat = {0: 0, 1: 0}
    disc = [0, 0]
    marg = []
    for r in done:
        if int(r["win"]):
            seat[int(r["seat"])] += 1
            if not int(r["loss"]):
                disc[0] += 1
        elif int(r["loss"]) and not int(r["win"]):
            disc[1] += 1
        marg.append(int(r["candidate_cash"]) - int(r["opponent_cash"]))
    marg.sort()
    mc, _n = mcnemar_exact(disc[0], disc[1])
    return {
        "label": label,
        "games_run": all_games,
        "completed": len(done) + len(ties),
        "decided": len(done),
        "inert_worlds_exact_tie": len(ties),
        "inert_share": round(len(ties) / max(1, len(done) + len(ties)), 4),
        "genuinely_broken": len(broken),
        "broken_reasons": sorted({b[1] for b in broken}),
        "W": W, "L": L, "T": len(ties),
        "win_rate_decided": iv["win_rate"],
        "wilson_decided": [round(iv["wilson_lo"], 4), round(iv["wilson_hi"], 4)],
        "win_share_of_all_games": round(W / max(1, all_games), 4),
        "binom_p_decided": binom_two_sided(W, len(done)),
        "median_margin": marg[len(marg) // 2] if marg else 0,
        "mean_margin": round(sum(marg) / len(marg), 1) if marg else 0,
        "worst_margin": marg[0] if marg else 0,
        "seat_wins": seat,
        "mcnemar_p": mc,
        "n_discordant": sum(disc),
    }


def main():
    print("=" * 78)
    print("ROOM_GUARD EXPERIMENT - CORRECTED CLASSIFICATION")
    print("=" * 78)
    p_sha, v_sha = sha(PARENT), sha(VARIANT)
    print(f"  parent  {p_sha}")
    print(f"  variant {v_sha}")
    print(f"  digests differ: {p_sha != v_sha}  -> this is NOT self-play\n")

    legs = [("vh", "variant(+room_guard) vs parent", "leg 1"),
            ("vf", "variant(+room_guard) vs farm", "leg 2"),
            ("pf", "parent vs farm", "leg 3")]
    res = {}
    for tag, label, leg in legs:
        rows = load(tag)
        if not rows:
            print(f"  {leg}: no rows yet")
            continue
        a = analyse(rows, label)
        res[leg] = a
        print(f"-- {leg}: {label}")
        print(f"   run {a['games_run']}  completed {a['completed']}  "
              f"decided {a['decided']}  inert {a['inert_worlds_exact_tie']} "
              f"({a['inert_share']:.1%})  broken {a['genuinely_broken']}")
        print(f"   {a['W']}-{a['L']}-{a['T']}   "
              f"win(decided) {a['win_rate_decided']:.4f}  Wilson "
              f"[{a['wilson_decided'][0]:.4f}, {a['wilson_decided'][1]:.4f}]  "
              f"p={a['binom_p_decided']:.3g}")
        print(f"   win share of all games {a['win_share_of_all_games']:.4f}  "
              f"seat {a['seat_wins']}  McNemar p={a['mcnemar_p']:.3g}  "
              f"median margin ${a['median_margin']}  mean ${a['mean_margin']}")
        print()

    guard_misfires = sum(a["inert_worlds_exact_tie"] for a in res.values())
    verdict = {}
    if "leg 1" in res:
        a = res["leg 1"]
        verdict["leg1"] = (
            "GAIN (decisively separated from 50%)"
            if a["wilson_decided"][0] > 0.5 else
            "NO-OP" if a["wilson_decided"][1] >= 0.5 else "HARM")
    if "leg 2" in res and "leg 3" in res:
        d = (res["leg 2"]["win_rate_decided"]
             - res["leg 3"]["win_rate_decided"])
        verdict["leg2_delta_vs_farm"] = round(d, 4)
        verdict["leg2"] = ("variant better" if d > 0.02 else
                           "variant worse" if d < -0.02 else
                           "indistinguishable")

    print("=" * 78)
    print(f"GUARD DEFECT: {guard_misfires} legitimate games were flagged invalid "
          f"by the\n  exact-tie heuristic, across the legs available. They are "
          f"reclassified\n  above as inert worlds, not invalid games.")
    for k, v in verdict.items():
        print(f"  {k}: {v}")
    print("=" * 78)

    out = {"parent_sha256": p_sha, "variant_sha256": v_sha,
           "digests_differ": p_sha != v_sha,
           "legs": res, "verdict": verdict,
           "exact_tie_guard_misfires": guard_misfires,
           "note": "an exact cash tie here means the changed gene never fired "
                   "on that world; it is a finding about the gene, not a "
                   "defect in the game"}
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=2)
    print(f"\nwrote {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
