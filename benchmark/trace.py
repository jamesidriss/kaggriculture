"""Step-by-step trace of a single episode for debugging."""
import importlib.util
import sys
import collections

path = sys.argv[1] if len(sys.argv) > 1 else "main.py"
seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1001
opp = sys.argv[3] if len(sys.argv) > 3 else "random"

spec = importlib.util.spec_from_file_location("m", path)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

from kaggle_environments import make
from kaggle_environments.envs.kaggriculture.kaggriculture import (
    starter_agent, random_agent, pass_agent)

BUILTIN_FN = {"random": random_agent, "starter": starter_agent, "pass": pass_agent}

env = make("kaggriculture", configuration={"seed": seed, "episodeSteps": 720})
env.reset()
agent1 = BUILTIN_FN[opp] if opp in BUILTIN_FN else opp

hist = []
for step in range(720):
    o = env.steps[step][0].observation
    a = m.agent(o)
    acts = [a, agent1(env.steps[step][1].observation)]
    hist.append(acts)
    if step < 720 - 1:
        env.step(acts)
    if step % 24 == 12 or step in (0, 1, 2):
        f = o.farms[0]
        c = collections.Counter()
        for row in f["tiles"]:
            for t in row:
                c["L" if t == "LOCKED" else ("e" if t is None else (t.get("crop") or t.get("kind")))] += 1
        sh = {k2: v for k2, v in o.private["shed"].items() if v}
        sd = {k2: v for k2, v in o.private["seeds"].items() if v}
        nfarm = sum(1 for x in hist[-1][0]["farmer"] if x)
        print(f"st{step:3d} d{o.day:2d}h{o.hour:2d} ${round(f['money']):6d} hands{len(f['hands']):2d} "
              f"{dict(c)} shed{sh} seed{sd} F{a['farmer']} M{a['market'][:5]}")