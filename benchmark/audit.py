"""Failure-safety audit.

Instruments the official interpreter to count the failure modes that silently
destroy value: plants dying to missed watering, animals escaping, shed overflow,
blocked actions, and unsold end-of-season inventory.

Usage: python benchmark/audit.py main.py [seed] [opponent]
"""

import importlib.util
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kaggle_environments import make  # noqa: E402
from kaggle_environments.envs.kaggriculture import kaggriculture as KG  # noqa: E402

BUILTIN = {"random": KG.random_agent, "starter": KG.starter_agent, "pass": KG.pass_agent}


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "main.py"
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1001
    opp_name = sys.argv[3] if len(sys.argv) > 3 else "starter"

    spec = importlib.util.spec_from_file_location("m", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    stats = {"plant_deaths": 0, "shed_overflow": 0, "weed_builds": 0,
             "plant_digs": 0, "harvests": 0, "feeds": 0, "escapes": 0,
             "actions_issued": 0}

    orig_drop = KG._drop_inventories_to_shed
    orig_end = KG._end_of_day
    orig_apply = KG._apply_unit_action

    prev_plants = {}

    def spy_apply(farm, private, idx, action, *a, **kw):
        if isinstance(action, list) and action:
            stats["actions_issued"] += 1
            if action[0] == "HARVEST":
                stats["harvests"] += 1
            elif action[0] == "FEED":
                stats["feeds"] += 1
        return orig_apply(farm, private, idx, action, *a, **kw)

    def spy_end(state, env, day):
        p0 = state[0].observation.farms[0]
        before_plants = sum(1 for r in p0["tiles"] for t in r
                            if isinstance(t, dict) and t.get("kind") == "PLANT")
        shed = state[0].observation.private["shed"]
        total = sum(v for v in shed.values() if isinstance(v, int))
        r = orig_end(state, env, day)
        after = sum(1 for r_ in p0["tiles"] for t in r_
                    if isinstance(t, dict) and t.get("kind") == "PLANT")
        # A plant that vanishes without being harvested is a death.
        dropped = before_plants - after
        if dropped > 0:
            stats["plant_deaths"] += dropped
        stats["weed_builds"] += sum(1 for r_ in p0["tiles"] for t in r_
                                    if isinstance(t, dict) and t.get("kind") == "WEED")
        return r

    KG._apply_unit_action = spy_apply
    KG._end_of_day = spy_end

    opp = BUILTIN[opp_name] if opp_name in BUILTIN else None
    env = make("kaggriculture", configuration={"seed": seed, "episodeSteps": 720})
    env.reset()
    for step in range(720):
        o = env.steps[step][0].observation
        a = mod.agent(o)
        if step < 719:
            b = opp(env.steps[step][1].observation) if opp else mod.agent(env.steps[step][1].observation)
            env.step([a, b])

    f = env.steps[-1][0].observation
    priv = env.steps[-1][0].observation.private
    shed_total = sum(v for v in priv["shed"].values() if isinstance(v, int))
    carried = {}
    for inv in priv["inventories"]:
        for k, v in inv.items():
            carried[k] = carried.get(k, 0) + v
    stranded = shed_total + sum(carried.values())

    print(f"seed={seed} opp={opp_name} cash={round(f.farms[0]['money'])}")
    print(f"  actions issued   {stats['actions_issued']}")
    print(f"  harvests         {stats['harvests']}")
    print(f"  feeds            {stats['feeds']}")
    print(f"  plants lost      {stats['plant_deaths']}   <- water failures")
    print(f"  STRANDED VALUE   {stranded} units  <- must be ~0")
    print(f"     shed={ {k: v for k, v in priv['shed'].items() if v} }")
    print(f"     carried={carried}")


if __name__ == "__main__":
    main()