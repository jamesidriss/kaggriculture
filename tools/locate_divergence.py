"""Locate the exact harness divergence behind the retracted "seat 1 has no step" claim.

Two delivery paths exist in kaggle-environments:
  A. env.run([a0, a1])            -> framework calls agents directly
  B. manual env.step([a0, a1])    -> caller supplies action callables
  C. env.steps[i][seat].observation -> the STORED snapshot, which is what the
     previous session's ad-hoc probes read

The previous session read path C and concluded seat 1 lacks `step`. This probe
measures all three under one env so the divergence is pinned to a specific path.
"""
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from kaggle_environments import make  # noqa: E402

SEED = 70117
TURNS = 5
via_agent = {0: [], 1: []}
via_stored = {0: [], 1: []}
via_manual = {0: [], 1: []}


def mk(p, sink, key="step"):
    def _agent(obs, configuration=None):
        if len(sink[p]) < TURNS:
            sink[p].append(obs.get(key, "<MISSING>"))
        return {"farmer": ["PASS"], "hands": [], "market": []}
    return _agent


def show(title, data, expect):
    print(f"\n=== {title} ===")
    for p in (0, 1):
        vals = data[p]
        ok = all(v == expect[i] for i, v in enumerate(vals))
        print(f"  seat {p}: {vals}   consistent={ok}")
    return all(all(v == expect[i] for i, v in enumerate(data[p])) for p in (0, 1))


def main():
    expect = list(range(TURNS))

    # Path A: framework-driven run
    a = make("kaggriculture", configuration={"seed": SEED, "episodeSteps": 720})
    a.reset()
    a.run([mk(0, via_agent), mk(1, via_agent)])
    print(f"{'path':<34} {'seat0':<22} {'seat1':<22} verdict")
    okA = show("A) env.run([a0,a1]) -- agent receives", via_agent, expect)
    print(f"{'A env.run (agent receives)':<34} {str(via_agent[0]):<22} "
          f"{str(via_agent[1]):<22} {'OK' if okA else 'FAIL'}")

    # Path C: the stored snapshot the previous session read
    for p in (0, 1):
        for i in range(TURNS):
            o = a.steps[i][p].observation
            if len(via_stored[p]) < TURNS:
                via_stored[p].append(o.get("step", "<MISSING>"))
    okC = show("C) env.steps[i][seat].observation -- stored snapshot", via_stored, expect)
    print(f"{'C stored snapshot':<34} {str(via_stored[0]):<22} "
          f"{str(via_stored[1]):<22} {'OK' if okC else 'FAIL'}")

    # Path B: manual env.step with callables
    b = make("kaggriculture", configuration={"seed": SEED, "episodeSteps": 720})
    b.reset()
    for i in range(TURNS):
        b.step([mk(0, via_manual), mk(1, via_manual)])
    okB = show("B) manual env.step([callable, callable])", via_manual, expect)
    print(f"{'B manual env.step':<34} {str(via_manual[0]):<22} "
          f"{str(via_manual[1]):<22} {'OK' if okB else 'FAIL'}")

    print("\n=== VERDICT ===")
    print(f"  env.run (real Kaggle path) delivers step to both seats : {okA}")
    print(f"  stored env.steps snapshot carries step for seat 1      : {okC}")
    print(f"  manual env.step(callable) delivers step to both seats  : {okB}")
    if okA and not okC:
        print("\n  DIVERGENCE FOUND: the framework's *delivered* observation has `step`")
        print("  for both seats, but the *stored* env.steps[i][1].observation does not.")
        print("  Any harness that feeds agents from env.steps snapshots instead of")
        print("  letting the framework call them will produce a false 'seat 1 lacks step'.")
    return 0 if okA else 1


if __name__ == "__main__":
    sys.exit(main())