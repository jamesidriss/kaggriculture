"""Parity gates: prove the harness sees what Kaggle sees.

The bug these exist to catch is subtle and expensive: `Environment.run`
delivers a *runtime* observation built with `__get_shared_state`, which carries
shared fields (including `step`) to both seats, while the *persisted*
`env.steps[i][seat].observation` snapshot does not. Any harness that feeds
agents from snapshots will therefore crash in seat 1 for an agent that is
perfectly legal on Kaggle.
"""
import kaggle_environments as ke
from kaggle_environments import make


def _probe_factory(sink, limit, keys=("step", "day", "hour", "player")):
    def _agent(obs, configuration=None):
        if len(sink) < limit:
            sink.append({k: obs.get(k, "<MISSING>") for k in keys})
        return {"farmer": ["PASS"], "hands": [], "market": []}
    return _agent


def observe_both_seats(env_name="kaggriculture", seed=999, turns=6):
    """Return what each seat actually receives through env.run()."""
    rec = {0: [], 1: []}
    env = make(env_name, configuration={"seed": seed, "episodeSteps": 720})
    env.run([_probe_factory(rec[0], turns), _probe_factory(rec[1], turns)])
    return rec


def assert_shared_delivery(env_name="kaggriculture", seed=999, turns=6,
                            field="step", turns_per_day=24):
    """Assert `field` reaches BOTH seats and is self-consistent.

    Raises AssertionError with the exact offending record on failure, so a
    failure is a piece of evidence rather than a shrug.
    """
    rec = observe_both_seats(env_name, seed, turns)
    bad = []
    for seat in (0, 1):
        for i, r in enumerate(rec[seat]):
            if r[field] == "<MISSING>":
                bad.append(f"seat {seat} turn {i}: {field!r} absent from the "
                           f"delivered observation")
            elif r[field] != i:
                bad.append(f"seat {seat} turn {i}: {field}={r[field]}, expected {i}")
            elif field == "step" and r["day"] is not None:
                implied = r["day"] * turns_per_day + r["hour"]
                if implied != r[field]:
                    bad.append(f"seat {seat} turn {i}: step={r[field]} but "
                               f"day*24+hour={implied}")
    n = min(len(rec[0]), len(rec[1]))
    for i in range(n):
        if rec[0][i][field] != rec[1][i][field]:
            bad.append(f"turn {i}: seat0 {field}={rec[0][i][field]} != "
                       f"seat1 {field}={rec[1][i][field]}")
    if bad:
        raise AssertionError(
            f"{env_name}: {field!r} is NOT correctly shared to both seats.\n  "
            + "\n  ".join(bad))
    return rec


def assert_both_seats(result):
    """Assert a Result covered every seed from both seats."""
    seeds0 = {m.seed for m in result.matches if m.seat == 0}
    seeds1 = {m.seed for m in result.matches if m.seat == 1}
    if not seeds0 or seeds0 != seeds1:
        raise AssertionError(
            f"{result.candidate} vs {result.opponent}: seat sets differ. "
            f"seat0={len(seeds0)} seeds, seat1={len(seeds1)} seeds, "
            f"asymmetric={sorted(seeds0 ^ seeds1)[:5]}")
    return result


def snapshot_divergence(env_name="kaggriculture", seed=999, probe=3,
                        field="step"):
    """Document the trap: the PERSISTED snapshot differs from what is delivered.

    Returns (delivered, persisted). `delivered[seat][i][field]` is what the
    agent sees; `persisted[seat][i][field]` is what a snapshot-reading harness
    would see. They differ for seat 1, which is the whole bug.
    """
    delivered = observe_both_seats(env_name, seed, probe)
    env = make(env_name, configuration={"seed": seed, "episodeSteps": 720})
    env.reset()
    env.run(["starter", "starter"])
    persisted = {0: [], 1: []}
    for i in range(probe):
        for seat in (0, 1):
            persisted[seat].append(env.steps[i][seat].observation.get(field,
                                                                     "<MISSING>"))
    return ({s: [r[field] for r in delivered[s]] for s in (0, 1)}, persisted)


def runtime_info():
    from importlib.metadata import version
    import sys
    return {"python": sys.version.split()[0],
            "kaggle_environments": version("kaggle-environments"),
            "location": ke.__file__}
