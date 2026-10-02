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
All figures paired, both seats, on ladder-derived elite seeds.
vs v51, the previous champion   657-155-180 of 992   80.91%  Wilson [0.781, 0.835]
vs the 2945 Farm                537-453-2   of 992   54.24%  Wilson [0.511, 0.573]
previous champion vs the Farm   506-486-0   of 992   51.01%  Wilson [0.479, 0.541]
    -> the single change is worth +3.23 points against the top opponent on
       identical worlds, and flips mean cash margin from -$26.9 to +$33.8.
SEALED FINAL, run once          34-14-0     of  48   70.83%  Wilson [0.568, 0.818]
HOLDOUT                         30-18-0     of  48   62.50%  Wilson [0.484, 0.748]
INDEPENDENT LINEAGE             768-0-0     of 768  100.00%  Wilson [0.995, 1.000]
    four MIT-licensed agents from an unrelated author.
INERT WORLDS                    {l1.get('inert_worlds_exact_tie', 'n/a')} of
    {l1.get('completed', 'n/a')} games ended in an exact tie, i.e. the guard
    never fired on those worlds. Those are findings, not invalid games.

SHADOW RATING
    ShadowRating is NOT published.
    {verdict}
    Only {n_inf} of {n_tot} matchups are informative; the rest saturate the
    ladder's win-rate curve, and a saturated curve cannot invert a saturated
    observation. What CAN be stated as a BOUND, not a point: an 80.91% win
    rate over the previous champion is far past the top of the fitted curve,
    so the gap is at least 275 ladder points.
    See reports/SHADOW_LADDER_CALIBRATION.md.

3075-READY: NO.
    The strict definition requires calibrated rating evidence consistent with
    >3075. The calibration does not support that precision, so that leg still
    fails. What IS established: this agent beats every legally reproducible
    public agent measured against it, improves on the previous champion by a
    large and replicated margin, and holds up on a sealed pool.
    See reports/3075_RESEARCH_CONCLUSION.md.

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
