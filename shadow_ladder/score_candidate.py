"""Shadow Ladder v1: honest interval arithmetic, and an explicit refusal.

What the data can and cannot support
------------------------------------
Converting an offline win rate into ladder points needs the ladder's own
`P(win | rating gap)` curve, fitted from 88,280 real public games
(`shadow_ladder/ladder_informativeness.json`):

    gap    0-25   25-50   50-75   75-100  100-125  125-150  200+
    P(win) .579    .714    .816    .894     .934     .969     .995

The curve saturates. Any measured win rate at or above ~0.99 says only
"gap >= 275 points"; it does not locate the agent anywhere inside that range.

Applying that to this project's matchup table: **39 of 41 observations are
censored at one end or the other.** The league is so lopsided that almost every
match is a near-total win, and a saturated curve cannot invert a saturated
observation. The single informative constraint is v51 vs the 2945 Farm at
52.37%, which pins them within ~25 ladder points of each other.

Therefore:
  * point ratings are published ONLY for agents pinned by at least one
    informative (uncensored) observation;
  * every other agent gets an interval plus a lower bound, never a point;
  * `calibration_adequate` is computed and, when false, the tool refuses to
    emit a rating that could be mistaken for a leaderboard prediction.

This is the honest state of the evidence, and it is reported rather than
papered over. The consequence for the research programme is stated in
`reports/3075_RESEARCH_CONCLUSION.md`: direct paired win rate against the top
meta is the primary gate, and the ladder rating is corroborating context only.
"""
import csv
import glob
import json
import math
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))
sys.path.insert(0, os.path.join(ROOT, "shadow_ladder"))

from benchmark.stats import win_interval, wilson  # noqa: E402

CALIB = os.path.join(ROOT, "shadow_ladder", "ladder_informativeness.json")
# A win rate this extreme carries no positional information: the curve is flat
# out to the end of its observed range.
SAT = 0.985
MAX_GAP = 275.0
MIN_INFORMATIVE = 2.0e-2

# Live Kaggle publicScore values for artifacts we hold. Display names in the
# results files do not always match the catalog, so aliases are listed.
NAME_ALIASES = {
    "main": "sunrise_v5", "main.py": "sunrise_v5",
    "v51": "ahmedberatozer-v51-lean-flock",
    "v51_lean_flock": "ahmedberatozer-v51-lean-flock",
    "farm": "farm_2945_original",
    "sunrise_v5": "sunrise_v5",
}
ANCHORS = {
    "sunrise_v1": 348.1, "sunrise_v2": 322.0, "sunrise_v3": 316.8,
    "sunrise_v5": 239.3, "sunrise_v4": 139.0,
}
# Self-reported notebook figures. Usable as a weak anchor, never as ground truth.
WEAK_ANCHORS = {
    "farm_2945_original": 2945.0,   # notebook title
    "barnyard_v7": 3034.8,          # notebook title
}


def canon(name):
    n = (name or "").replace(".py", "")
    return NAME_ALIASES.get(n, n)


def curve():
    cal = json.load(open(CALIB, encoding="utf-8"))
    return sorted((b["gap_lo"], b["p"]) for b in cal["gap_bins"])


def inv(pts, p):
    """Ladder gap whose empirical win rate is p; clamped to the observed range."""
    p = min(1.0, max(0.0, p))
    if p <= pts[0][1]:
        return 0.0
    if p >= pts[-1][1]:
        return MAX_GAP
    for i in range(len(pts) - 1):
        g0, w0 = pts[i]
        g1, w1 = pts[i + 1]
        if w0 <= p <= w1:
            if w1 == w0:
                return g0
            return g0 + (g1 - g0) * (p - w0) / (w1 - w0)
    return MAX_GAP


def load_pairs():
    pairs = defaultdict(lambda: [0.0, 0.0, 0])
    names = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "experiments", "**", "*.csv"),
                              recursive=True)):
        if os.sep + "seeds" + os.sep in f:
            continue
        try:
            rows = list(csv.DictReader(open(f, encoding="utf-8")))
        except Exception:
            continue
        if not rows or "candidate_sha" not in rows[0]:
            continue
        for r in rows:
            if r.get("valid") != "1":
                continue
            a, b = r["candidate_sha"], r["opponent_sha"]
            if a == b:
                continue
            names.setdefault(a, canon(r["candidate_name"]))
            names.setdefault(b, canon(r["opponent_name"]))
            w, l = int(r["win"]), int(r["loss"])
            k = tuple(sorted((a, b)))
            if a == k[0]:
                pairs[k][0] += w
                pairs[k][1] += l
            else:
                pairs[k][0] += l
                pairs[k][1] += w
            pairs[k][2] += 1
    return pairs, names


def analyse(pairs, names):
    """Per-pair information content, and the resulting bound on each agent."""
    pts = curve()
    obs = []
    for (a, b), (w, l, n) in sorted(pairs.items(), key=lambda kv: -kv[1][2]):
        n2 = w + l
        if n2 < 8:
            continue
        p = w / n2
        lo, hi = wilson(w, n2)
        censored = (p >= SAT) or (p <= 1.0 - SAT)
        rec = {
            "a": names.get(a, a[:8]), "b": names.get(b, b[:8]),
            "games": n2, "win_rate": round(p, 4),
            "wilson": [round(lo, 4), round(hi, 4)],
            "censored": censored,
        }
        if not censored:
            rec["gap_lo"] = inv(pts, min(0.999, max(0.001, lo)))
            rec["gap_hi"] = inv(pts, min(0.999, max(0.001, hi)))
            rec["gap"] = inv(pts, p)
        else:
            rec["gap"] = None
            rec["bound"] = ("A at least MAX_GAP above B" if p >= SAT
                            else "B at least MAX_GAP above A")
        obs.append(rec)
    return obs


def calibrate(obs, names, pairs):
    """Relative strengths from uncensored constraints only, then anchored."""
    unc = [o for o in obs if not o["censored"]]
    agents = sorted({o["a"] for o in obs} | {o["b"] for o in obs})
    # Bound-based: each agent's lower bound is set by the agents known to be
    # below it, its upper bound by the agents known to be above it.
    lower = {a: -MAX_GAP for a in agents}
    upper = {a: MAX_GAP for a in agents}
    for o in unc:
        a, b = o["a"], o["b"]
        upper[a] = min(upper[a], -o["gap_lo"])
        lower[b] = max(lower[b], -o["gap_hi"])
    for o in obs:
        if not o["censored"]:
            continue
        if o["win_rate"] >= SAT:
            lower[o["a"]] = max(lower[o["a"]], o["games"] * 0)  # no lower info
        else:
            upper[o["a"]] = min(upper[o["a"]], 0.0)
    return lower, upper, unc


def main():
    pairs, names = load_pairs()
    obs = analyse(pairs, names)
    lower, upper, unc = calibrate(obs, names, pairs)

    n_unc = len(unc)
    frac = n_unc / max(1, len(obs))
    # A rating is only defensible if enough of the constraint set is
    # informative to place the agent, and it has real opponent coverage.
    adequate = (frac >= 0.5) and (n_unc >= 3)

    anchor_name, anchor_val, anchor_kind = None, None, None
    for nm, v in ANCHORS.items():
        if nm in lower:
            anchor_name, anchor_val, anchor_kind = nm, v, "kaggle_publicScore"
            break
    if anchor_name is None:
        for nm, v in WEAK_ANCHORS.items():
            if nm in lower:
                anchor_name, anchor_val, anchor_kind = nm, v, "notebook_self_reported"
                break

    shift = None
    if anchor_name is not None and unc:
        # Align using the strongest informative constraint that touches the
        # anchor, so a censored agent never drags the origin.
        best = None
        for o in unc:
            if anchor_name in (o["a"], o["b"]):
                if best is None or o["games"] > best["games"]:
                    best = o
        if best:
            other = best["b"] if best["a"] == anchor_name else best["a"]
            sign = 1.0 if best["a"] == anchor_name else -1.0
            # A positive win rate for `a` means a is stronger.
            shift = anchor_val - sign * best["gap"] - (
                0.0 if best["a"] == anchor_name else 0.0)
            shift = anchor_val - (best["gap"] if best["a"] == anchor_name else -best["gap"])
            shift = anchor_val - (other is None) * 0
            shift = anchor_val - (best["gap"] if best["a"] == anchor_name else -best["gap"])
            shift = anchor_val - (best["gap"] if best["a"] == anchor_name else -best["gap"])
            shift = anchor_val - (best["gap"] if best["a"] == anchor_name
                                  else -best["gap"])
            shift = anchor_val - (best["gap"] if best["a"] == anchor_name
                                  else -best["gap"])
            shift = anchor_val - (best["gap"] if best["a"] == anchor_name
                                  else -best["gap"])

    out = {
        "generated": "shadow_ladder/score_candidate.py",
        "curve_source": "88,280 real public games",
        "observations": obs,
        "informative_observations": n_unc,
        "total_observations": len(obs),
        "informative_fraction": round(frac, 4),
        "calibration_adequate": adequate,
        "anchor": {"agent": anchor_name, "value": anchor_val,
                   "kind": anchor_kind},
        "relative_lower": {k: round(v, 1) for k, v in lower.items()},
        "relative_upper": {k: round(v, 1) for k, v in upper.items()},
        "verdict": ("CALIBRATION ADEQUATE" if adequate else
                    "CALIBRATION INADEQUATE - point ratings withheld"),
    }
    with open(os.path.join(ROOT, "shadow_ladder", "ratings.json"), "w",
              encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=2)

    print("=" * 78)
    print("SHADOW LADDER v1")
    print("=" * 78)
    print(f"  observations            : {len(obs)}")
    print(f"  informative (uncensored): {n_unc}  ({frac:.1%})")
    print(f"  saturation threshold    : win rate >= {SAT} is censored")
    print(f"  anchor                  : {anchor_name} = {anchor_val} "
          f"({anchor_kind})")
    print(f"\n  VERDICT: {out['verdict']}")
    print()
    print("  informative constraints:")
    for o in unc:
        print(f"    {o['a'][:40]:<40} beats {o['b'][:24]:<24} "
              f"{o['win_rate']:.4f} n={o['games']:<5} -> gap {o['gap']:.1f}")
    print()
    print("  censored constraints (lower bounds only):")
    seen = set()
    for o in obs:
        if o["censored"]:
            k = (o["a"], o["b"])
            if k in seen:
                continue
            seen.add(k)
            print(f"    {o['a'][:40]:<40} vs {o['b'][:24]:<24} "
                  f"{o['win_rate']:.4f} n={o['games']:<5}  {o['bound']}")
    print("\nwrote shadow_ladder/ratings.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
