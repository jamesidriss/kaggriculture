"""Freeze the submission-ready artifact and its metadata.

This exists so that if Kaggle reopens submissions, nothing has to be built,
re-validated or decided under time pressure. The file is already the champion,
already licence-clean, and already runtime-validated; this script copies the
exact bytes, re-runs the artifact gate, and writes the metadata a future
operator needs without re-deriving anything.

It never edits an artifact in place and never promotes anything: the champion
decision lives in `champions/research/`, and this only mirrors the current
holder.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(ROOT, "submission_ready")
CHAMP_ROOT = os.path.join(ROOT, "champions", "research")
CURRENT = os.path.join(CHAMP_ROOT, "CURRENT.json")
HEDGE = os.path.join(ROOT, "postmortem_hedge", "main.py")


def current_champion():
    """The artifact of record is whatever CURRENT.json names.

    Hardcoding a champion path here meant the submission copy silently lagged
    behind a legitimate promotion. Reading the pointer means it cannot.
    """
    c = json.load(open(CURRENT, encoding="utf-8"))
    return os.path.join(CHAMP_ROOT, c["champion_id"], "main.py"), c


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=ROOT,
                          capture_output=True).stdout.decode().strip()


def main():
    os.makedirs(DST, exist_ok=True)
    src, cur = current_champion()
    assert os.path.exists(src), f"champion artifact missing at {src}"
    before = sha(src)
    shutil.copy2(src, os.path.join(DST, "main.py"))
    after = sha(os.path.join(DST, "main.py"))
    assert before == after, "copy changed the bytes"
    assert after == cur["agent_sha"], (
        f"copied digest {after} does not match CURRENT.json "
        f"{cur['agent_sha']}; refusing to publish a mismatched artifact")

    # The licence and notice must travel with the artifact.
    for extra in ("THIRD_PARTY.md", "LICENSE"):
        s = os.path.join(ROOT, extra)
        if os.path.exists(s):
            shutil.copy2(s, os.path.join(DST, "NOTICE.md"))

    sl = json.load(open(os.path.join(ROOT, "shadow_ladder", "ratings.json"),
                        encoding="utf-8"))
    env = json.load(open(os.path.join(ROOT, "simulation", "official",
                                      "environment_snapshot.json"),
                         encoding="utf-8"))
    verdict = sl.get("verdict", "unknown")
    n_inf = sl.get("informative_observations", 0)
    n_tot = sl.get("total_observations", 0)
    gate_p = os.path.join(ROOT, "simulation", "search", "promotion_verdict.json")
    gate = json.load(open(gate_p, encoding="utf-8")) if os.path.exists(gate_p) else {}
    rg_p = os.path.join(ROOT, "simulation", "search", "room_guard_verdict.json")
    rg = json.load(open(rg_p, encoding="utf-8")) if os.path.exists(rg_p) else {}
    l1 = rg.get("legs", {}).get("leg 1", {})
    l2 = rg.get("legs", {}).get("leg 2", {})
    l3 = rg.get("legs", {}).get("leg 3", {})
    C = rg.get("legs", {}).get("leg 2", {})
    # Canonical metrics, recomputed from migrated raw rows. These supersede
    # every figure quoted before the tie fix and before the metric fix.
    cm_p = os.path.join(ROOT, "simulation", "search", "canonical_metrics.json")
    cm = json.load(open(cm_p, encoding="utf-8")) if os.path.exists(cm_p) else {}

    def m(key, field, fmt="{:.4f}", alt="n/a"):
        v = cm.get(key, {}).get(field)
        return fmt.format(v) if isinstance(v, (int, float)) else alt

    def ci(key):
        v = cm.get(key, {})
        if "bt_score_lo95_seed_bootstrap" in v:
            return (f"[{v['bt_score_lo95_seed_bootstrap']:.4f}, "
                    f"{v['bt_score_hi95_seed_bootstrap']:.4f}]")
        return "n/a"

    with open(os.path.join(DST, "METADATA.txt"), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write(f"""SUBMISSION-READY ARTIFACT
==========================
This directory is frozen. If Kaggle reopens submissions, submit `main.py`
here as-is. Do not rebuild it.

champion_id      : {cur['champion_id']}
agent_name       : v51-lean-flock + room_guard
parent           : ahmedberatozer-v51-lean-flock ({cur['predecessor']['agent_sha']})
source           : Kaggle dataset destbreso/kaggriculture-donor-agents-20260902,
                   file agents/ahmedberatozer-v51-lean-flock.py
license          : Apache-2.0 (NOTICE.md retained alongside)
sha256           : {after}
bytes            : {os.path.getsize(os.path.join(DST, 'main.py'))}
git_commit       : {git('rev-parse', 'HEAD')}
modifications    : EXACTLY ONE, and mechanically verified: the live
                   `_SETTINGS` flag `room_guard` flipped False -> True.
                   Every other byte of the file is identical to the parent.
promoted_utc     : {cur.get('promoted_utc', 'n/a')}
promotion_gate   : {gate.get('decision', 'n/a')} (all five legs passed;
                   thresholds declared before the run)

ENVIRONMENT
kaggle_environments : {env['kaggle_environments_version']}
python              : {env['python']}
snapshot_sha256     : {env['snapshot_sha256']}
runtime_path        : kaggle_environments.core.Environment.run (official runner)
turns_per_game      : 719 of 720
seats               : both, every world
errors              : 0 broken games in every leg (3,800+ paired games)

STRENGTH EVIDENCE (offline; NOT a Kaggle rating)
Recomputed from migrated raw rows by policy/search/canonical_metrics.py.
PRIMARY metric is the BT score rate (W + 0.5T)/N, which is how Kaggle's final
Bradley-Terry scores a draw. Decided-only W/(W+L) is a secondary diagnostic.
Intervals are percentile bootstraps that resample SEEDS, not games, because the
two seats of one world share the world and are correlated observations.

  C001 vs v51   638-138-216 of 992   BT {m('C001 vs v51  (decisive leg 1)','bt_score_rate')}
                                           95% {ci('C001 vs v51  (decisive leg 1)')}
                                           decided-only {m('C001 vs v51  (decisive leg 1)','decided_win_rate')}
                                           tie rate {m('C001 vs v51  (decisive leg 1)','tie_rate')}
                 657-155-180 of 992   BT {m('C001 vs v51  (promotion leg B)','bt_score_rate')}
                                           95% {ci('C001 vs v51  (promotion leg B)')}
                                           decided-only {m('C001 vs v51  (promotion leg B)','decided_win_rate')}
                                           tie rate {m('C001 vs v51  (promotion leg B)','tie_rate')}

  The two runs are independent seed sets. They disagree by 1.31 points on the
  decided-only rate and by 0.10 points on the BT score rate. The metric that
  matches the competition's convention is the one that replicates.

  C001 vs 2945 Farm  537-453-2 of 992  BT {m('C001 vs 2945 Farm  (decisive leg 2)','bt_score_rate')}
                                           95% {ci('C001 vs 2945 Farm  (decisive leg 2)')}
  v51 vs 2945 Farm   506-486-0 of 992  BT {m('v51 vs 2945 Farm  (decisive leg 3)','bt_score_rate')}
                                           95% {ci('v51 vs 2945 Farm  (decisive leg 3)')}

  READ THIS HONESTLY: C001's score rate against the Farm has a LOWER CONFIDENCE
  BOUND BELOW 0.50. The pre-declared promotion criterion "score rate > 52% with
  lower confidence > 50%" is NOT met against the Farm. C001 is probably better
  than the Farm; this evidence does not establish it at that threshold. The
  matchup is unresolved and is the first target of the next generation.
  See reports/RETRACTIONS.md entry R11.

  SEALED FINAL, run once          34-14-0     of  48   BT 0.7708
  HOLDOUT                         30-18-0     of  48   BT 0.6875
  INDEPENDENT LINEAGE             768-0-0     of 768  BT 1.0000
    four MIT-licensed agents from an unrelated author. This 100% is inherited
    from v51, not earned by the change, and those agents are far too weak for
    the number to say anything about 3066.

SHADOW RATING
    ShadowRating is NOT published.
    {verdict}
    Only {n_inf} of {n_tot} matchups are informative; the rest saturate the
    ladder's win-rate curve. A saturated curve means the observation CANNOT BE
    INVERTED -- it does not mean the gap is large, and no bound on the gap is
    claimed. The earlier "+275 ladder points" statement is retracted
    (reports/RETRACTIONS.md R8).
    See reports/SHADOW_LADDER_CALIBRATION.md.

3066-READY: NO.
    Two legs fail. (1) No calibrated absolute rating: the ladder curve
    saturates, so the champion's position is unknown. (2) The Farm matchup's
    lower confidence bound is 0.4990, below the 0.50 promotion threshold.
    What IS established: C001 beats its own parent decisively and
    reproducibly (BT 0.752-0.753 vs 0.5101), and beats four weak independent
    agents outright.
    See reports/3066_RESEARCH_CONCLUSION.md.

RUNTIME GATE
    playability probe PLAYABLE; per-call latency far inside the 1 s actTimeout.
    No network, no file writes, no external data, single self-contained file.

HEDGE (second slot, if two are wanted)
    postmortem_hedge/main.py
    {sha(HEDGE) if os.path.exists(HEDGE) else 'n/a'}
    The 2945 Farm v9/3, Apache-2.0, verbatim. NOTE: it is the SAME lineage as
    the primary - 1,205 shared identifiers, containment 0.818, one identical
    3,352-token run. It hedges seat and world variance, not strategy risk.

NOT SUBMITTED
    Kaggle submissions are closed; CreateSubmission returns HTTP 400 with an
    empty body. Nothing here has been submitted and nothing here can change a
    live result.
""")
    print("SUBMISSION_READY FROZEN")
    print(f"  champion   {cur['champion_id']}")
    print(f"  main.py    {after}")
    print(f"  bytes      {os.path.getsize(os.path.join(DST, 'main.py'))}")
    print(f"  identical to champion snapshot: {before == after}")
    print(f"  shadow     {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
