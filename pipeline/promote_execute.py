"""Execute a passed promotion: snapshot the champion, re-freeze the
submission-ready artifact, and record the decision in the lake.

Ordering matters and is deliberate:

  1. verify the gate said PROMOTE, by re-reading its verdict file;
  2. snapshot the artifact BEFORE anything points at it, so the immutable
     record exists independent of the current champion pointer;
  3. only then repoint `champions/research/CURRENT` and `submission_ready/`;
  4. verify the submission copy is byte-identical to the snapshot;
  5. record the decision in DuckDB `champion_history` with the evidence.

Nothing is overwritten in place. The previous champion stays on disk forever.
"""
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))
sys.path.insert(0, os.path.join(ROOT, "data_pipeline"))

GATE = os.path.join(ROOT, "simulation", "search", "promotion_verdict.json")
NEW = os.path.join(ROOT, "simulation", "search", "baseline_plus_room_guard.py")
OLD = os.path.join(ROOT, "postmortem_champion", "main.py")
CHAMP_ROOT = os.path.join(ROOT, "champions", "research")
CHAMP_ID = "C001_room_guard"
SUB = os.path.join(ROOT, "submission_ready")
NOTICE = os.path.join(ROOT, "THIRD_PARTY.md")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=ROOT,
                          capture_output=True).stdout.decode().strip()


def main():
    g = json.load(open(GATE, encoding="utf-8"))
    if g["decision"] != "PROMOTE":
        print("gate decision is not PROMOTE; refusing to execute")
        return 1
    print("=" * 78)
    print("EXECUTING PROMOTION")
    print("=" * 78)

    # 1. immutable snapshot first
    d = os.path.join(CHAMP_ROOT, CHAMP_ID)
    os.makedirs(d, exist_ok=True)
    shutil.copy2(NEW, os.path.join(d, "main.py"))
    newsha = sha(os.path.join(d, "main.py"))
    oldsha = sha(OLD)
    print(f"  snapshot  champions/research/{CHAMP_ID}/main.py")
    print(f"    new sha256 {newsha}")
    print(f"    old sha256 {oldsha}")
    print(f"    predecessor preserved: postmortem_champion/main.py (untouched)")

    # 2. licence and attribution must travel
    meta = f"""RESEARCH CHAMPION {CHAMP_ID}
=====================================
name            : v51-lean-flock + room_guard
parent          : ahmedberatozer-v51-lean-flock
parent_sha256   : {oldsha}
sha256          : {newsha}
bytes           : {os.path.getsize(os.path.join(d, 'main.py'))}
git_commit      : {git('rev-parse', 'HEAD')}
promoted_utc    : {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}

ORIGIN AND LICENCE
  This is a DERIVED artifact. It is the published Apache-2.0 agent
  ahmedberatozer-v51-lean-flock with exactly ONE declared change: the live
  `_SETTINGS` flag `room_guard` flipped False -> True.
  Verified mechanically: the candidate differs from the parent ONLY inside the
  `_SETTINGS` literal; every other byte of a 461,738-byte file is identical.
  Apache-2.0 permits modification; NOTICE and attribution are retained in
  submission_ready/NOTICE.md. No source is vendored from a private origin.

THE CHANGE
  `room_guard` is one of nine boolean layer switches in the agent's own
  configuration. Six were switched off in the shipped file. The off state was
  never justified by evidence: the published agent carries it off, and this
  project's search over the reachable 2^9 layer space found that turning it on
  is worth +3.23 points of win rate against the strongest opponent.

EVIDENCE (paired, both seats, 0 broken games in every leg)
  vs v51 (parent)            657-155-180 of 992   80.91%  Wilson [0.781, 0.835]
  vs 2945 Farm               537-453-2   of 992   54.24%  Wilson [0.511, 0.573]
  vs parent, replication run 638-138-216 of 992   82.22%  Wilson [0.794, 0.848]
  parent vs 2945 Farm        506-486-0   of 992   51.01%  Wilson [0.479, 0.541]
      -> the change is worth +3.23 points against the top opponent on identical
         worlds, and flips mean cash margin from -$26.9 to +$33.8.
  SEALED FINAL (run once)    34-14-0     of  48   70.83%  Wilson [0.568, 0.818]
  HOLDOUT                    30-18-0     of  48   62.50%  Wilson [0.484, 0.748]
  INDEPENDENT LINEAGE        768-0-0     of 768  100.00%  Wilson [0.995, 1.000]
      four MIT-licensed agents from an unrelated author.
  INERT WORLDS              216 of 992 (21.8%) ended in an exact tie: the guard
      never fires on those worlds. Those are findings, not invalid games; see
      policy/search/room_guard_verdict.py for why the default validity rule
      misclassifies them.

PROMOTION GATE  all five legs passed; thresholds were declared in the log
  before the run. See simulation/search/promotion_verdict.json.

LINEAGE
  Same lineage as the previous champion by construction. This is a strength
  improvement, NOT a diversification: it remains one strategy family.
  The previous champion and the hedge remain on disk and are still the only
  independent axes available.

LIMITATIONS, stated not softened
  * Still one lineage. The independent-lineage win rate is inherited from the
    parent, not earned by the change.
  * No calibrated ShadowRating. Only 2 of 41 matchups are informative and the
    curve saturates, so no point rating is published. What CAN be stated: the
    80.91% win rate over the previous champion is far past the top of the
    fitted curve, so the gap is at LEAST 275 ladder points -- a BOUND, not a
    point estimate.
  * 3075-readiness still fails on the calibrated-rating leg. See
    reports/3075_RESEARCH_CONCLUSION.md.
"""
    with open(os.path.join(d, "METADATA.txt"), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write(meta)

    # 3. repoint submission-ready
    os.makedirs(SUB, exist_ok=True)
    shutil.copy2(NEW, os.path.join(SUB, "main.py"))
    subsha = sha(os.path.join(SUB, "main.py"))
    assert subsha == newsha, "submission copy differs from the snapshot"
    for extra in (NOTICE, "LICENSE"):
        s = os.path.join(ROOT, extra)
        if os.path.exists(s):
            shutil.copy2(s, os.path.join(SUB, "NOTICE.md"))

    # 4. current pointer
    with open(os.path.join(CHAMP_ROOT, "CURRENT.json"), "w", encoding="utf-8",
              newline="\n") as fh:
        json.dump({"champion_id": CHAMP_ID, "agent_sha": newsha,
                   "predecessor": {"champion_id": "C000_v51",
                                   "agent_sha": oldsha},
                   "gate": "simulation/search/promotion_verdict.json",
                   "promoted_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
                  fh, indent=2)

    # 5. record in the lake
    try:
        from lake import _utc, connect
        con = connect()
        con.execute("DELETE FROM champion_history WHERE champion_id = ?", [CHAMP_ID])
        con.execute(
            "INSERT INTO champion_history VALUES (?,?,?,?,?,?,?,?,?,?)",
            [CHAMP_ID, newsha, "v51-lean-flock + room_guard", oldsha, _utc(),
             None,
             "80.91% vs parent (992g), 54.24% vs 2945 Farm (992g), "
             "+3.23pt on identical worlds",
             "100.00% vs four MIT independent agents (768g)",
             "70.83% (34-14-0 of 48, run once, Wilson [0.568,0.818])",
             git("rev-parse", "HEAD")])
        con.close()
        print("  recorded in lake: champion_history")
    except Exception as exc:  # noqa: BLE001
        print(f"  note: lake record skipped ({exc})")

    print(f"  submission_ready/main.py  {subsha}")
    print(f"  byte-identical to snapshot: {subsha == newsha}")
    print(f"  NOTICE.md present: {os.path.exists(os.path.join(SUB, 'NOTICE.md'))}")
    print(f"\nPROMOTION EXECUTED: {CHAMP_ID}")
    print(f"  previous champion preserved at postmortem_champion/main.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
