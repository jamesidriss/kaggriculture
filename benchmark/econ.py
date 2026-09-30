"""Economic breakdown: where does the bank actually go?"""
import importlib.util
import sys
import collections

from kaggle_environments import make
from kaggle_environments.envs.kaggriculture import kaggriculture as KG

path = sys.argv[1] if len(sys.argv) > 1 else "main.py"
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1001
opp = sys.argv[3] if len(sys.argv) > 3 else "starter"

spec = importlib.util.spec_from_file_location("m", path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

ORIG_MONEY = KG._new_farm
sold = collections.Counter()
prev_money = None

orig_process = KG._process_market


def spy(state, env):
    before = [f["money"] for f in state[0].observation.farms]
    r = orig_process(state, env)
    after = [f["money"] for f in state[0].observation.farms]
    if len(after) > 0:
        d = after[0] - before[0]
        if d < 0:
            sold["_spend"] -= d
    return r


KG._process_market = spy

BUILTIN_FN = {"random": KG.random_agent, "starter": KG.starter_agent, "pass": KG.pass_agent}
env = make("kaggriculture", configuration={"seed": seed, "episodeSteps": 720})
env.reset()
a1 = BUILTIN_FN[opp] if opp in BUILTIN_FN else opp

final = None
planted = collections.Counter()
for step in range(720):
    o = env.steps[step][0].observation
    if step % 24 == 0:
        for row in o.farms[0]["tiles"]:
            for t in row:
                if isinstance(t, dict) and t.get("kind") == "PLANT":
                    planted[t["crop"]] += 1
    a = m.agent(o)
    if step < 719:
        env.step([a, a1(env.steps[step][1].observation)])

final = env.steps[-1]
me = final[0].observation.farms[0]
you = final[1].observation.farms[1]
sh = {k: v for k, v in final[0].observation.private["shed"].items() if v}
inv = final[0].observation.private["inventories"]
carried = collections.Counter()
for i in inv:
    for k, v in i.items():
        carried[k] += v

print("seed", seed, "vs", opp)
print("MY CASH   ", round(me["money"]), " OPP CASH", round(you["money"]))
print("quadrants", len(me["unlocked_quadrants"]))
print("market inv excess:", {k: round(v - 10000) for k, v in final[0].observation.market["inventory"].items() if v > 9990})
print("shed leftover ", sh)
print("carried      ", dict(carried))
print("crops seen/planted-counts:", dict(planted))