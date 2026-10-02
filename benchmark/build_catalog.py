"""Regenerate research/FINAL_PUBLIC_AGENT_CATALOG.csv from the files on disk.

Digests are RECOMPUTED, never transcribed. A hand-maintained digest column is a
standing invitation to publish a number that describes nothing, which is
exactly what happened when a previous version of this catalog was written by
hand. Everything not derivable from a file or a manifest is left empty rather
than guessed.
"""
import csv
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "opponents", "meta", "MANIFEST.csv")
OUT = os.path.join(ROOT, "research", "FINAL_PUBLIC_AGENT_CATALOG.csv")
RESULTS = os.path.join(ROOT, "experiments", "final_meta_results.csv")

# Facts that cannot be derived from a file. Anything not listed here is left
# blank rather than invented.
NOTES = {
    "ahmedberatozer-v51-lean-flock":
        "POSTMORTEM PRIMARY. 1039-945 vs the 2945 Farm over 1984 paired "
        "ladder-derived games, Wilson 95% [0.5017,0.5456], exact binomial "
        "p=0.0368. SAME LINEAGE as the 2945 Farm: 1205 shared identifiers, "
        "containment 0.82, one identical 3352-token run, identical nine-author "
        "credit list. Benchmarked by benchmark/lineage_check.py.",
    "farm_2945_original":
        "POSTMORTEM HEDGE. Second by direct evidence. NOT a diversifying "
        "hedge: same lineage as the PRIMARY. Verbatim public artifact; the "
        "previously shipped seat patch is retracted and retained only as a "
        "challenger.",
    "ahmedberatozer-v49-funded-sale-timing":
        "Undefeated inside the 9-agent round robin. Plays identically to v50 "
        "(24/24 exact ties), so v49 and v50 are one agent, not two.",
    "ahmedberatozer-v50-early-yarn-commit":
        "Plays identically to v49. One lineage counted twice.",
    "v16_rc5":
        "GENUINELY DISTINCT lineage: Jaccard 0.063 against v51, longest shared "
        "run 27 tokens. But 0-232 to BOTH top agents, median $82k against their "
        "$116k, so too weak to serve as a diversifying hedge.",
    "barnyard_v7":
        "UNKNOWN_LICENSE - the author declared none, so it is excluded from "
        "competitive use and retained for analysis only. Genuinely plays "
        "(719 turns/game) and genuinely loses 0-144 to the two hubs. The "
        "'hinge' price patch is UNREACHABLE code: the agent reads live prices "
        "from observation.market.prices, and the patched agent finished at "
        "$74,991, identical to the dollar across 24 games.",
    "sunrise_v5":
        "COMPETITION SUBMISSION. Ladder rating 252.6 (live Kaggle "
        "publicScore). Offline: 0-792, $0.19 cash per field action against the "
        "champion's $5.64.",
    "sunrise_v4":
        "COMPETITION SUBMISSION. Ladder rating 138.5 (live Kaggle publicScore).",
    "v38_feed": "Regularized BT places it at the bottom of the 9-agent round robin.",
}

LINEAGE_OVERRIDE = {
    "ahmedberatozer-v51-lean-flock": "Ozer / 2945-Farm lineage",
    "farm_2945_original": "Ozer / 2945-Farm lineage",
    "v16_rc5": "boatlee (DISTINCT from everything else)",
    "barnyard_v7": "romanrozen standalone",
    "sunrise_v5": "original (this repository)",
    "sunrise_v4": "original (this repository)",
}
for n in os.listdir(os.path.join(ROOT, "opponents", "meta")):
    if n.startswith("ahmedberatozer-"):
        LINEAGE_OVERRIDE.setdefault(n[:-3], "Ozer / 2945-Farm lineage")
LINEAGE_OVERRIDE.setdefault("v38_feed", "Ozer / 2945-Farm lineage")

LADDER = {"sunrise_v5": "252.6", "sunrise_v4": "138.5"}


def main():
    man = {}
    if os.path.exists(MANIFEST):
        for r in csv.DictReader(open(MANIFEST, encoding="utf-8")):
            man[r["name"]] = r

    # Extra agents that are not league members.
    extra = []
    for rel, name in (("champions/champion_001/main.py", "sunrise_v5"),
                      ("champions/champion_000/main.py", "sunrise_v4")):
        p = os.path.join(ROOT, rel)
        if os.path.exists(p):
            extra.append((name, p, "original (this repository)"))
    pw = os.path.join(ROOT, "postmortem_champion", "main.py")
    if os.path.exists(pw):
        extra.append(("ahmedberatozer-v51-lean-flock", pw, ""))

    # Evidence per agent from the canonical results only.
    ev = {}
    if os.path.exists(RESULTS):
        for r in csv.DictReader(open(RESULTS, encoding="utf-8")):
            if r["valid"] != "1":
                continue
            for me, opp, w, l in ((r["candidate_sha"], r["opponent_sha"],
                                   r["win"], r["loss"]),
                                  (r["opponent_sha"], r["candidate_sha"],
                                   r["loss"], r["win"])):
                e = ev.setdefault(me, [0, 0, 0])
                e[0] += int(w); e[1] += int(l); e[2] += 1

    rows = []
    seen = set()
    sources = [(n, os.path.join(ROOT, "opponents", "meta", n + ".py"),
                os.path.join(ROOT, "opponents", "meta", n + ".py"))
               for n in sorted(man)]
    sources += [(n, p, "") for n, p, _ in extra]

    for name, p, rel in sources:
        if name in seen or not os.path.exists(p):
            continue
        seen.add(name)
        raw = open(p, "rb").read()
        sha = hashlib.sha256(raw).hexdigest()
        m = man.get(name, {})
        w, l, n = ev.get(sha, [0, 0, 0])
        rows.append({
            "agent_name": name,
            "author": m.get("author", ""),
            "source": m.get("source", ""),
            "license": m.get("license", ""),
            "sha256": sha,
            "bytes": len(raw),
            "path": (rel or os.path.relpath(p, ROOT)).replace("\\", "/"),
            "lineage": LINEAGE_OVERRIDE.get(name, m.get("lineage", "")),
            "ladder_rating": LADDER.get(name, ""),
            "notebook_public_score": m.get("notes", "")[:0] or "",
            "playable": "yes",
            "league_eligible": m.get("league_eligible", "no"),
            "offline_W": w, "offline_L": l, "offline_games": n,
            "offline_win_rate": (round(w / (w + l), 4) if (w + l) else ""),
            "notes": NOTES.get(name, ""),
        })

    fields = list(rows[0].keys())
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        wri = csv.DictWriter(fh, fieldnames=fields)
        wri.writeheader()
        wri.writerows(rows)

    print(f"wrote {os.path.relpath(OUT, ROOT)}: {len(rows)} agents")
    print(f"  all sha256 recomputed from disk: "
          f"{all(len(r['sha256']) == 64 for r in rows)}")
    print(f"  agents with a licence declared : "
          f"{sum(1 for r in rows if r['license'])}")
    print(f"  league-eligible                : "
          f"{sum(1 for r in rows if r['league_eligible'] == 'yes')}")
    for r in rows:
        print(f"    {r['agent_name'][:44]:<44} {r['sha256'][:16]} "
              f"{r['offline_W']}-{r['offline_L']}/{r['offline_games']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
