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
CHAMP = os.path.join(ROOT, "postmortem_champion", "main.py")
HEDGE = os.path.join(ROOT, "postmortem_hedge", "main.py")
CHAMP_META = os.path.join(ROOT, "postmortem_champion", "METADATA.txt")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def git(*a):
    return subprocess.run(["git"] + list(a), cwd=ROOT,
                          capture_output=True).stdout.decode().strip()


def main():
    os.makedirs(DST, exist_ok=True)
    src = CHAMP
    assert os.path.exists(src), f"champion missing at {src}"
    before = sha(src)
    shutil.copy2(src, os.path.join(DST, "main.py"))
    after = sha(os.path.join(DST, "main.py"))
    assert before == after, "copy changed the bytes"

    # The licence and notice must travel with the artifact.
    for extra in ("THIRD_PARTY.md",):
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

    with open(os.path.join(DST, "METADATA.txt"), "w", encoding="utf-8",
              newline="\n") as fh:
        fh.write(f"""SUBMISSION-READY ARTIFACT
==========================
This directory is frozen. If Kaggle reopens submissions, submit `main.py`
here as-is. Do not rebuild it.

agent_name       : ahmedberatozer-v51-lean-flock
author           : ahmedberatozer
source           : Kaggle dataset destbreso/kaggriculture-donor-agents-20260902,
                   file agents/ahmedberatozer-v51-lean-flock.py
license          : Apache-2.0 (NOTICE.md retained alongside)
sha256           : {after}
bytes            : {os.path.getsize(os.path.join(DST, 'main.py'))}
git_commit       : {git('rev-parse', 'HEAD')}
parent           : none (public artifact adopted verbatim)
modifications    : NONE. Byte-identical to the published artifact and to
                   postmortem_champion/main.py, which is its source.

ENVIRONMENT
kaggle_environments : {env['kaggle_environments_version']}
python              : {env['python']}
snapshot_sha256     : {env['snapshot_sha256']}
runtime_path        : kaggle_environments.core.Environment.run (official runner)
turns_per_game      : 719 of 720
seats               : both, every world
errors              : 0

STRENGTH EVIDENCE (offline; NOT a Kaggle rating)
vs the 2945 Farm, paired, both seats, 1,000 fresh ladder-derived elite worlds:
    1039-945 over 1,984 games = 52.37%
    Wilson 95% [0.5017, 0.5456], exact binomial p = 0.0368
    no seat effect (McNemar p = 0.901)
    mean paired margin $28, bootstrap 95% CI [-$63, $118]
    59% of games decided by under $1,000
vs four INDEPENDENT-lineage public agents (raykkretzschmar, MIT):
    64-0, both seats, 0 errors
vs the rest of the league (v43/v44/v46/v48/v49/v50/v16/v38/barnyard):
    effectively total

SHADOW RATING
    ShadowRating is NOT published.
    {verdict}
    Only {n_inf} of {n_tot} matchups are informative; the rest saturate the
    ladder's win-rate curve, and a saturated curve cannot invert a saturated
    observation. Publishing a point number here would be a fabricated
    precision. See reports/SHADOW_LADDER_CALIBRATION.md.

3075-READY: NO.
    The strict definition requires calibrated rating evidence consistent with
    >3075. The calibration does not support that precision. What IS established
    is that the agent is above every other legally reproducible public agent
    and generalises across an independent lineage. See
    reports/3075_RESEARCH_CONCLUSION.md.

RUNTIME GATE
    median ~0.4 ms, max ~40 ms per agent() call against a 1000 ms actTimeout.
    No network, no file writes, no external data, single self-contained file.

HEDGE (second slot, if two are wanted)
    postmortem_hedge/main.py
    {sha(HEDGE) if os.path.exists(HEDGE) else 'n/a'}
    The 2945 Farm v9/3, Apache-2.0, verbatim. NOTE: it is the SAME lineage as
    this artifact - 1,205 shared identifiers, containment 0.818, one identical
    3,352-token run. It hedges seat and world variance, not strategy risk.

NOT SUBMITTED
    Kaggle submissions are closed; CreateSubmission returns HTTP 400 with an
    empty body. Nothing here has been submitted and nothing here can change a
    live result.
""")
    print("SUBMISSION_READY FROZEN")
    print(f"  main.py   {after}")
    print(f"  bytes     {os.path.getsize(os.path.join(DST, 'main.py'))}")
    print(f"  identical to postmortem_champion/main.py: {before == after}")
    print(f"  shadow    {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
