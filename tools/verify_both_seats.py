"""Verify the VERBATIM public artifact (The 2945 Farm v9/3) in BOTH seats.

Run through the real Kaggle path (`env.run([...])`), never hand-built
observations. This is the test the previous session got wrong.
"""
import hashlib
import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kaggle_environments import make  # noqa: E402
from kaggle_environments.envs.kaggriculture import kaggriculture as KG  # noqa: E402

ORIG = os.path.join(ROOT, "research", "public_src",
                    "the-2945-farm-96-vs-the-top-10-public-bots", "extracted", "main.py")
PATCHED = os.path.join(ROOT, "postmortem_champion", "main.py")
SEEDS = [335464115, 846389409]


def load(p):
    s = importlib.util.spec_from_file_location("a" + str(abs(hash(p))), p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m.agent


def run_one(agent, seat, seed):
    env = make("kaggriculture", configuration={"seed": seed, "episodeSteps": 720})
    env.reset()
    agent0, agent1 = (agent, KG.starter_agent) if seat == 0 else (KG.starter_agent, agent)
    env.run([agent0, agent1])
    f = env.steps[-1]
    return [int(f[i].observation.farms[i]["money"]) for i in range(2)], \
           [f[i].status for i in range(2)]


def main():
    print(f"ORIGINAL sha256: {hashlib.sha256(open(ORIG,'rb').read()).hexdigest()}")
    print(f"  starts with bfee70e9: "
          f"{hashlib.sha256(open(ORIG,'rb').read()).hexdigest().startswith('bfee70e9')}")
    print(f"PATCHED  sha256: {hashlib.sha256(open(PATCHED,'rb').read()).hexdigest()}")

    orig = load(ORIG)
    patched = load(PATCHED)

    print("\n=== VERBATIM original, both seats, real env.run() ===")
    crashes = 0
    for seed in SEEDS:
        for seat in (0, 1):
            try:
                cash, status = run_one(orig, seat, seed)
                print(f"  seed {seed} seat{seat}: cash={cash} status={status}")
            except Exception as exc:  # noqa: BLE001
                crashes += 1
                print(f"  seed {seed} seat{seat}: CRASH {type(exc).__name__}: {exc}")
    print(f"  crashes: {crashes}")

    print("\n=== patch equivalence in seat 0 (must be identical) ===")
    same = True
    for seed in SEEDS:
        c0, _ = run_one(orig, 0, seed)
        c1, _ = run_one(patched, 0, seed)
        eq = c0 == c1
        same &= eq
        print(f"  seed {seed}: orig={c0[0]:>8} patched={c1[0]:>8} identical={eq}")
    print(f"  seat-0 identical on all seeds: {same}")

    print("\n=== VERDICT ===")
    if crashes == 0:
        print("  The verbatim artifact runs in BOTH seats under the real Kaggle path.")
        print("  -> the previous session's seat-1 crash claim is RETRACTED.")
    else:
        print(f"  verbatim artifact crashed {crashes} time(s) in real runs.")
    return 0 if crashes == 0 else 1


if __name__ == "__main__":
    sys.exit(main())