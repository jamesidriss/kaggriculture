"""Measurement batch for the 3066 generation: the two numbers that decide everything.

Batch 1  C001 vs the 2945 Farm, at scale.
        This is the only matchup where the outcome is genuinely uncertain: BT
        0.5423 with a seed-bootstrap lower bound of 0.4990, i.e. the edge does
        not clear the promotion threshold. More games is the only way to resolve
        it, and it is the most important single measurement available.

Batch 2  C001 vs the newly recovered public agents.
        The calibration curve only has resolution where the win rate is
        mid-range. Every previously available opponent was either a near-total
        win or a near-total loss, so nothing landed mid-curve. Measuring the
        recovered pool tells us whether a usable spread of strengths exists,
        which decides whether a rating can be estimated at all.

Everything runs through the cached parallel runner, so re-running this is nearly
free.
"""
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
RUNNER = os.path.join(ROOT, "benchmark", "parallel_tournament.py")
OUT = os.path.join(ROOT, "experiments", "p3066")
WORKERS = os.cpu_count() or 8

C001 = "champions/research/C001_room_guard/main.py"
FARM = "opponents/meta/farm_2945_original.py"
V51 = "postmortem_champion/main.py"

BATCHES = [
    # (label, A, B, seeds file, extra args)
    ("c001_vs_farm_full", C001, FARM, "seeds/REAL_scale.txt",
     ["--experiment-id", "p3066_c001_farm"]),
    ("c001_vs_v51_full", C001, V51, "seeds/REAL_scale.txt",
     ["--experiment-id", "p3066_c001_v51"]),
    ("c001_vs_moon_q13", C001, "opponents/unlicensed/kaggriculture-r88-rivals__moon_q13_mg.py",
     "seeds/REAL_scale.txt", ["--limit", "250", "--experiment-id", "p3066_moon"]),
    ("c001_vs_moon_parent", C001, "opponents/unlicensed/kaggriculture-r88-rivals__moon_parent.py",
     "seeds/REAL_scale.txt", ["--limit", "250", "--experiment-id", "p3066_moon"]),
    ("c001_vs_thomas", C001, "opponents/unlicensed/kaggriculture-r88-rivals__thomas.py",
     "seeds/REAL_scale.txt", ["--limit", "250", "--experiment-id", "p3066_thomas"]),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    print("=" * 78)
    print("P3066 MEASUREMENT BATCH")
    print("=" * 78)
    for label, a, b, seeds, extra in BATCHES:
        out = os.path.join("experiments", "p3066", label + ".csv")
        cmd = [PY, RUNNER, "--a", a, "--b", b, "--seeds-file", seeds,
               "--out", out, "--workers", str(WORKERS)] + extra
        t0 = time.time()
        print(f"\n--- {label}  ({time.strftime('%H:%M:%S')})")
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        tail = [l for l in (p.stdout or "").strip().splitlines()
                if l.strip().startswith(("matches", "W-L-T", "BT score",
                                         "decided", "tie rate", "throughput",
                                         "cache_hits"))]
        for l in tail:
            print("   " + l.strip())
        if p.returncode != 0:
            err = (p.stderr or "").strip().splitlines()
            print("   FAILED:", err[-1][:150] if err else "no stderr")
        print(f"   ({time.time()-t0:.0f}s)")
    print("\nbatch complete")


if __name__ == "__main__":
    sys.exit(main())
