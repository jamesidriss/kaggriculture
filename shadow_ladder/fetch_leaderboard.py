"""Recover the official final leaderboard and turn it into an anchor table.

Why this is the single most valuable fetch in the project
-------------------------------------------------------
The whole research programme stalled on one thing: no way to convert an offline
win rate into a ladder position, because the ladder curve saturates and almost
every matchup this project can measure is a near-total win.

The competition is now over and Kaggle publishes a FINAL leaderboard computed
by Bradley-Terry over all episodes, with draws scored 0.5 per side. That is the
exact metric this project should be optimising, and it is a real, official,
public number for every team that submitted.

So the calibration problem changes shape. Instead of inverting a saturated
empirical curve, we now have the outcome the curve was approximating, for the
whole field, in the same units.

What is still missing, and is NOT invented here
-----------------------------------------------
A leaderboard row gives a SCORE and a TEAM. It does not give the submitted
artifact. So these are anchors in the sense of "official score, artifact not
yet bound". Every anchor carries an explicit `anchor_class`:

    A  exact artifact <-> exact submission, score verified against the artifact
    B  official leaderboard score, artifact recovered and verified to be that
       submission
    C  official score, artifact UNKNOWN -- context only, cannot calibrate
    D  self-reported notebook title, no official score -- context only

Nothing is promoted from C or D. The scoring convention is confirmed from the
competition's own configuration rather than assumed: the final rating is
Bradley-Terry, so per-game scores are (1, 0.5, 0).

Usage
-----
    python shadow_ladder/fetch_leaderboard.py
"""
import csv
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMP = "kaggriculture"
OUT_CSV = os.path.join(ROOT, "research", "final_leaderboard.csv")
OUT_JSON = os.path.join(ROOT, "research", "final_leaderboard.json")
ANCHOR_SCHEMA = os.path.join(ROOT, "research", "anchor_catalog.json")


def fetch_pages():
    """Page through the public leaderboard via the kaggle CLI."""
    rows = []
    token = None
    seen_tokens = set()
    for _ in range(40):
        cmd = ["kaggle", "competitions", "leaderboard", "-c", COMP, "--show"]
        if token:
            cmd += ["--page-token", token]
        p = subprocess.run(cmd, capture_output=True, text=True)
        text = p.stdout
        if p.returncode != 0 and not text.strip():
            print("  leaderboard fetch failed:", p.stderr.strip()[:200])
            break
        lines = text.splitlines()
        new_token = None
        for ln in lines:
            if ln.startswith("Next Page Token"):
                new_token = ln.split("=", 1)[1].strip()
                continue
            parts = ln.split()
            if len(parts) >= 4 and parts[0].isdigit() and len(parts[0]) > 4:
                try:
                    rows.append({"team_id": int(parts[0]),
                                 "team_name": " ".join(parts[1:-2]),
                                 "submission_date": " ".join(parts[-2:]),
                                 "score": float(parts[-1])})
                except ValueError:
                    continue
        print(f"  page: +{len(rows)} rows cumulative, "
              f"{'token' if new_token else 'last page'}")
        if not new_token or new_token in seen_tokens:
            break
        seen_tokens.add(new_token)
        token = new_token
    return rows


def main():
    print("=" * 78)
    print("FINAL LEADERBOARD RECOVERY")
    print("=" * 78)
    rows = fetch_pages()
    if not rows:
        print("  nothing recovered; leaving prior state untouched")
        return 1
    rows.sort(key=lambda r: -r["score"])
    seen, uniq = set(), []
    for r in rows:
        if r["team_id"] in seen:
            continue
        seen.add(r["team_id"])
        uniq.append(r)
    rows = uniq

    os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["rank", "team_id", "team_name",
                                           "score", "submission_date",
                                           "anchor_class", "artifact_sha"])
        w.writeheader()
        for i, r in enumerate(rows, 1):
            r["rank"] = i
            # No artifact is bound yet, so by the project's own rule this is a
            # context row, not a calibration anchor.
            r["anchor_class"] = "C"
            r["artifact_sha"] = ""
            w.writerow(r)

    meta = {
        "source": f"kaggle competitions leaderboard -c {COMP} --show",
        "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "metric": "final Bradley-Terry rating over all episodes",
        "tie_convention": "0.5 per side, which is the BT convention",
        "n_teams": len(rows),
        "top": [{"rank": r["rank"], "team": r["team_name"],
                 "score": r["score"], "date": r["submission_date"]}
                for r in rows[:25]],
        "score_distribution": {},
        "caveat": "A leaderboard row binds a SCORE to a TEAM, not to an "
                  "artifact. Until an artifact is recovered and shown to be the "
                  "submitted file, the row is anchor_class C and is excluded "
                  "from calibration.",
    }
    for lo, hi in ((0, 500), (500, 1000), (1000, 1500), (1500, 2000),
                   (2000, 2500), (2500, 2800), (2800, 3000), (3000, 4000)):
        n = sum(1 for r in rows if lo <= r["score"] < hi)
        meta["score_distribution"][f"{lo}-{hi}"] = n

    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(meta, fh, indent=2)

    print(f"\n  teams: {len(rows)}")
    print(f"  score range: {rows[-1]['score']:.1f} .. {rows[0]['score']:.1f}")
    print(f"\n  {'rank':>4} {'score':>9}  team")
    for r in rows[:20]:
        print(f"  {r['rank']:>4} {r['score']:>9.1f}  {r['team_name'][:52]}")
    print("\n  score distribution:")
    for k, v in meta["score_distribution"].items():
        if v:
            print(f"    {k:>10}  {v:>4} teams")
    print(f"\nwrote {os.path.relpath(OUT_CSV, ROOT)}")
    print(f"wrote {os.path.relpath(OUT_JSON, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
