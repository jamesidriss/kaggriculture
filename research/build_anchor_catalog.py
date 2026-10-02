"""Build the calibration anchor catalog.

The hard part is not collecting scores. It is refusing to attach a score to an
artifact without evidence, because that single mistake destroys calibration
quietly: a "2945 agent" that is actually a 2600 agent shifts the whole scale and
nothing errors.

Classes, by evidence strength
----------------------------
  A  the artifact digest IS the submitted file, and the score is official.
     Requires a verifiable link. Nothing in this project qualifies yet.
  B  the score is official AND the artifact was recovered and probed, but the
     artifact-to-team binding is INFERRED rather than proven.
  C  official score, artifact unknown. Context only. Never calibrates.
  D  self-reported notebook title. Context only. Never calibrates.

Only A and B may enter a calibration fit, and B carries its inference on the
record so a reader can reject it.

Every candidate binding below was assembled from evidence that is written down.
Where the evidence is circumstantial, the `binding` field says so.
"""
import csv
import hashlib
import json
import os
import sys
import time

# This file lives at research/build_anchor_catalog.py, so the repository root is
# ONE directory up. Getting the depth wrong makes every path resolve to nothing
# and the script reports "0 teams" instead of failing loudly, which is the same
# silent-nothing failure that has bitten this project more than once.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LB = os.path.join(ROOT, "research", "final_leaderboard.csv")
OUT = os.path.join(ROOT, "research", "anchor_catalog.json")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def load_lb():
    if not os.path.exists(LB):
        return {}
    out = {}
    for r in csv.DictReader(open(LB, encoding="utf-8")):
        try:
            out[r["team_name"].strip()] = (float(r["score"]), int(r["rank"]))
        except ValueError:
            continue
    return out


# Each candidate: what we hold, and the evidence for the score binding.
CANDIDATES = [
    {
        "agent": "farm_2945_original",
        "artifact": "postmortem_hedge/main.py",
        "lineage_id": "L-OZER-2945",
        "declared_license": "Apache-2.0",
        "team_name_claim": "DSM",
        "binding": "inferred",
        "evidence": [
            "The agent's own public notebook is titled 'The 2945 Farm 2945', a "
            "self-reported score of 2945 (class D evidence on its own).",
            "The official final leaderboard has exactly one team named 'DSM' at "
            "2945.4 (rank 3 of 744).",
            "Two independently derived numbers agree to 0.4 ladder points.",
        ],
        "why_not_class_A": [
            "The notebook title is self-reported, not a Kaggle field.",
            "There is no public API that maps a submission id to a team, so the "
            "artifact-to-team link is a strong coincidence, not a proof.",
            "'DSM' could be an unrelated team that happened to land on 2945.4.",
        ],
        "anchor_class": "B",
    },
    {
        "agent": "ahmedberatozer-v51-lean-flock",
        "artifact": "postmortem_champion/main.py",
        "lineage_id": "L-OZER-2945",
        "declared_license": "Apache-2.0",
        "team_name_claim": None,
        "binding": "none",
        "evidence": [
            "Verbatim copy of a published public artifact from an Apache-2.0 "
            "donor dataset, so the artifact is exactly what its author wrote.",
        ],
        "why_not_class_A": [
            "The author is not known to have submitted this exact file. The "
            "notebook family reports 'Best Score' figures for specific versions "
            "and we cannot prove which version was submitted.",
            "Attaching a notebook's best score to a different version is exactly "
            "the error this class exists to prevent.",
        ],
        "anchor_class": "D",
    },
]


def main():
    lb = load_lb()
    print("=" * 78)
    print("ANCHOR CATALOG")
    print("=" * 78)
    print(f"  official leaderboard loaded: {len(lb)} teams\n")

    anchors = []
    for c in CANDIDATES:
        ap = os.path.join(ROOT, c["artifact"])
        if not os.path.exists(ap):
            print(f"  {c['agent']:<44} artifact missing, skipped")
            continue
        rec = {k: c[k] for k in ("agent", "lineage_id", "declared_license",
                                 "team_name_claim", "binding", "evidence",
                                 "why_not_class_A", "anchor_class")}
        rec["artifact_sha256"] = sha(ap)
        rec["artifact_path"] = c["artifact"]
        rec["bytes"] = os.path.getsize(ap)
        score = None
        if c["team_name_claim"] and c["team_name_claim"] in lb:
            score, rank = lb[c["team_name_claim"]]
            rec["official_score"] = score
            rec["official_rank"] = rank
            rec["official_team"] = c["team_name_claim"]
        else:
            rec["official_score"] = None
            rec["official_score_reason"] = (
                "no team-name binding proposed, or the proposed name is not on "
                "the leaderboard")
        rec["score_verified_official"] = rec["official_score"] is not None
        # `score` is the field name the calibration code consumes. It is set
        # ONLY from an official leaderboard value, never from a notebook title,
        # so there is no path by which a self-reported number reaches a fit.
        rec["score"] = rec["official_score"]
        rec["usable_for_calibration"] = rec["anchor_class"] in ("A", "B") \
            and rec["score_verified_official"]
        anchors.append(rec)
        flag = "USABLE" if rec["usable_for_calibration"] else "excluded"
        print(f"  {c['agent']:<44} class {rec['anchor_class']}  "
              f"score {rec['official_score']}  {flag}")

    cat = {
        "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "leaderboard": {
            "source": "kaggle competitions leaderboard -c kaggriculture",
            "metric": "final Bradley-Terry, draw = 0.5 per side",
            "teams": len(lb),
            "top_score": max((v[0] for v in lb.values()), default=None),
            "bottom_score": min((v[0] for v in lb.values()), default=None),
        },
        "class_rules": {
            "A": "artifact digest IS the submitted file and the score is official",
            "B": "official score with a recovered, probed artifact, binding inferred",
            "C": "official score, artifact unknown - context only",
            "D": "self-reported title only - context only",
        },
        "usable_rule": "A or B with an official score; nothing else calibrates",
        "n_anchors": len(anchors),
        "n_usable": sum(1 for a in anchors if a["usable_for_calibration"]),
        "anchors": anchors,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(cat, fh, indent=2)
    print(f"\n  usable anchors: {cat['n_usable']} of {cat['n_anchors']}")
    print(f"  wrote {os.path.relpath(OUT, ROOT)}")
    if cat["n_usable"] < 5:
        print(f"\n  The publication gate needs >= 5 usable anchors. "
              f"{cat['n_usable']} is far short, so no rating can be published "
              f"and that is the finding, not an obstacle to route around.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
