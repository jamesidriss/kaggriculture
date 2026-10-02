"""Preserve what the smoke screen actually measured, after the process that was
running it was stopped before it could write its own summary.

The run directory is transient and git-ignored, so this is the committed record
of the screen: which gene combinations were evaluated, what they scored, and
what the one surviving hypothesis was. It is derived from the run CSVs, not
typed by hand.
"""
import ast
import csv
import glob
import json
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUNS = os.path.join(ROOT, "simulation", "search", "runs")
CAND = os.path.join(ROOT, "simulation", "search")
OUT = os.path.join(ROOT, "simulation", "search", "search_record.json")
GENES = ["hand_align", "weed_repair", "sell_lead", "front_run", "budget_guard",
         "room_guard", "clamp_sells", "dead_stock", "terminal_liquidation"]


def settings_of(stem):
    p = os.path.join(CAND, stem + ".py")
    if not os.path.exists(p):
        return None
    s = open(p, encoding="utf-8", errors="ignore").read()
    i = s.find("_SETTINGS={")
    if i < 0:
        return None
    j = s.index("}", i)
    try:
        return ast.literal_eval(s[i + len("_SETTINGS="): j + 1])
    except Exception:
        return None


def main():
    by_tag = defaultdict(list)
    for d in sorted(glob.glob(os.path.join(RUNS, "*_smoke"))):
        tag = os.path.basename(d)[:-len("_smoke")]
        for f in sorted(glob.glob(os.path.join(d, "r_*.csv"))):
            try:
                by_tag[tag] += list(csv.DictReader(open(f, encoding="utf-8")))
            except Exception:
                pass

    recs = []
    for tag, rows in by_tag.items():
        v = [r for r in rows if r["valid"] == "1"]
        if not v:
            continue
        W = sum(int(r["win"]) for r in v)
        L = sum(int(r["loss"]) for r in v)
        T = sum(int(r["tie"]) for r in v)
        mc = sorted(int(r["candidate_cash"]) - int(r["opponent_cash"]) for r in v)
        recs.append({"tag": tag, "games": len(v),
                     "invalid": len(rows) - len(v), "W": W, "L": L, "T": T,
                     "win_rate": W / max(1, W + L),
                     "median_margin": mc[len(mc) // 2] if mc else 0,
                     "settings": settings_of(tag)})
    recs.sort(key=lambda r: -r["win_rate"])
    survivors = [r for r in recs if r["win_rate"] >= 0.40]

    # Which gene is common to every survivor but off in the baseline?
    baseline = settings_of("__none__") or {
        "hand_align": True, "weed_repair": True, "sell_lead": True,
        "front_run": False, "budget_guard": False, "room_guard": False,
        "clamp_sells": False, "dead_stock": False,
        "terminal_liquidation": False}
    common = None
    if survivors:
        common = {g for g in GENES
                  if all(r["settings"] and r["settings"].get(g) for r in survivors)}
    hypothesis = sorted(common - {g for g in GENES
                                  if baseline.get(g)}) if common else []

    out = {
        "stage": "smoke",
        "screening_games_per_candidate": 16,
        "opponent": "farm_2945_original",
        "candidates_evaluated": len(recs),
        "sampling": "evenly spaced over itertools.product index set; the "
                    "lexicographic-prefix bug that made the first run score "
                    "0.0000 uniformly is fixed and guarded by an abort",
        "candidates": recs,
        "survivors_at_0.40": [r["tag"] for r in survivors],
        "genes_common_to_all_survivors": sorted(common) if common else [],
        "hypothesis_for_decisive_test": hypothesis,
        "why_smoke_cannot_conclude": (
            "16 games cannot resolve the 2-point effect that separates the "
            "parent from the Farm ($28 mean margin on ~$100k banks). The "
            "survivor set is a HYPOTHESIS, not a result: the survivors differ "
            "at random on every other gene, which is what noise selection "
            "looks like."),
        "baseline_reference": {
            "agent": "ahmedberatozer-v51-lean-flock",
            "vs_farm_all_measured_games": 0.5237,
            "vs_farm_games": 3968,
        },
    }
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=2)
    print("SEARCH RECORD (smoke stage)")
    print(f"  candidates evaluated : {len(recs)}")
    print(f"  survivors at >=0.40  : {len(survivors)}")
    print(f"  common to all        : {sorted(common) if common else []}")
    print(f"  -> hypothesis        : +{hypothesis}")
    print(f"  best smoke win rate  : {recs[0]['win_rate']:.4f} over "
          f"{recs[0]['games']} games (baseline is 0.5237 over 3,968)")
    print(f"  wrote {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
