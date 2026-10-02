"""Runtime observation probe: does Kaggle deliver `step` to BOTH players?

The previous session claimed `observation["step"]` exists only for player 0 and
that The 2945 Farm therefore crashes in seat 1. That claim must be settled with
executable evidence, not inference from a JSON schema.

This probe runs a REAL `env.run([probe0, probe1])` on the installed
kaggle-environments and records, per seat, the keys actually delivered and the
values of step/day/hour.

Exit code 0 only if `step` is present and self-consistent for BOTH seats.
"""
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import kaggle_environments  # noqa: E402
from kaggle_environments import make  # noqa: E402

SEED = 70117
TURNS = 6
RECORDS = {0: [], 1: []}


def probe(player_index):
    """A real agent function; it only records and returns a legal PASS action."""
    def _agent(obs, configuration=None):
        rec = {
            "player": obs.get("player"),
            "has_step": "step" in obs,
            "step": obs.get("step", "<MISSING>"),
            "day": obs.get("day"),
            "hour": obs.get("hour"),
            "keys": sorted(obs.keys()),
        }
        if len(RECORDS[player_index]) < TURNS:
            RECORDS[player_index].append(rec)
        return {"farmer": ["PASS"], "hands": [], "market": []}
    return _agent


def main():
    print(f"kaggle_environments at {os.path.dirname(kaggle_environments.__file__)}")
    print(f"python {sys.version.split()[0]}")
    try:
        from importlib.metadata import version
        print(f"kaggle-environments version {version('kaggle-environments')}")
    except Exception as exc:
        print(f"version lookup failed: {exc}")

    env = make("kaggriculture", configuration={"seed": SEED, "episodeSteps": 720})
    env.run([probe(0), probe(1)])

    print("\n=== delivered observation keys, first turn ===")
    for p in (0, 1):
        if RECORDS[p]:
            r = RECORDS[p][0]
            print(f"  seat {p}: step_present={r['has_step']} step={r['step']} "
                  f"day={r['day']} hour={r['hour']}")
            print(f"         keys={r['keys']}")

    failures = []
    print("\n=== per-turn values ===")
    print(f"{'seat':>4} {'turn':>4} {'step':>6} {'day':>4} {'hour':>5} "
          f"{'day*24+hour':>12} {'match':>6}")
    for p in (0, 1):
        for i, r in enumerate(RECORDS[p]):
            implied = None
            if r["day"] is not None and r["hour"] is not None:
                implied = r["day"] * 24 + r["hour"]
            match = (implied == r["step"]) if r["has_step"] else None
            print(f"{p:>4} {i:>4} {str(r['step']):>6} {str(r['day']):>4} "
                  f"{str(r['hour']):>5} {str(implied):>12} {str(match):>6}")
            if not r["has_step"]:
                failures.append(f"seat {p} turn {i}: observation has NO 'step' key")
            elif r["step"] != i:
                failures.append(f"seat {p} turn {i}: step={r['step']} (expected {i})")
            elif match is False:
                failures.append(
                    f"seat {p} turn {i}: step={r['step']} != day*24+hour={implied}")

    # Cross-seat agreement
    n = min(len(RECORDS[0]), len(RECORDS[1]))
    for i in range(n):
        a, b = RECORDS[0][i], RECORDS[1][i]
        if a["step"] != b["step"]:
            failures.append(f"turn {i}: seat0 step={a['step']} != seat1 step={b['step']}")
        if a["day"] != b["day"] or a["hour"] != b["hour"]:
            failures.append(f"turn {i}: seat0 day/hour != seat1 day/hour")

    print()
    if failures:
        print(f"RESULT: FAIL ({len(failures)} problem(s))")
        for f in failures[:12]:
            print("  -", f)
        return 1
    print("RESULT: PASS -- `step` is delivered to BOTH seats and is self-consistent")
    print("        (step == day*24+hour, and both seats agree)")
    return 0


if __name__ == "__main__":
    sys.exit(main())