"""Research pipeline: sync -> ingest -> quality -> population -> experiments.

Stages are idempotent and each can be run alone, because a research pipeline
that can only run end to end is a pipeline that cannot be resumed after an
interruption. Nothing here auto-promotes a champion: promotion is a separate,
gated script, and a nightly run must never be able to change what gets
submitted.
"""
import argparse
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable

STAGES = [
    ("env", "environment snapshot", ["simulation/official/snapshot.py"]),
    ("ingest-episodes", "ingest public replay episodes",
     ["data_pipeline/ingest/episodes.py"]),
    ("ingest-agents", "ingest agent registry", ["data_pipeline/ingest/agents.py"]),
    ("quality", "data quality gate", ["data_pipeline/quality.py"]),
    ("parity", "differential parity harness",
     ["simulation/differential/parity.py", "--trajectories", "2000"]),
    ("calibrate", "shadow ladder calibration",
     ["shadow_ladder/ladder_informativeness.py"]),
    ("rate", "shadow rating", ["shadow_ladder/score_candidate.py"]),
    ("search", "candidate search", ["policy/search/run_search.py", "--budget", "96"]),
    ("freeze", "freeze submission-ready", ["pipeline/freeze_submission.py"]),
    ("dashboard", "regenerate dashboards", ["pipeline/dashboards.py"]),
]


def run(script, args, quiet=True):
    p = subprocess.run([PY, os.path.join(ROOT, script)] + args, cwd=ROOT,
                       capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", action="append", default=[],
                    help="run only these stages")
    ap.add_argument("--budget", type=int, default=96)
    args = ap.parse_args()

    sel = {s.lower() for s in args.stage}
    print("=" * 78)
    print("RESEARCH PIPELINE")
    print("=" * 78)
    if sel:
        print(f"  stage filter: {sorted(sel)}")
    results = {}
    t_all = time.time()
    for key, desc, cmd in STAGES:
        if sel and key not in sel:
            continue
        c = list(cmd)
        if key == "search":
            c = ["policy/search/run_search.py", "--budget", str(args.budget)]
        t0 = time.time()
        rc, out, err = run(c[0], c[1:])
        dt = time.time() - t0
        results[key] = {"rc": rc, "seconds": round(dt, 1)}
        flag = "ok  " if rc == 0 else "FAIL"
        print(f"  [{flag}] {key:<16} {desc:<34} {dt:>6.1f}s")
        if rc != 0 and err:
            print("        " + err.strip().splitlines()[-1][:110])
    print(f"\n  total {time.time()-t_all:.1f}s")
    bad = [k for k, v in results.items() if v["rc"] != 0]
    if bad:
        print(f"  FAILED STAGES: {bad}")
        print("  NOTE: a failing stage is a result, not a crash. The pipeline")
        print("  reports it and continues; promotion remains gated separately.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
