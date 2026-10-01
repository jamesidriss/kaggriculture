"""Simulate an agent on real ladder seeds against a reference, per product.

Reports final cash, per-product shed carryover and whether inventory was left
stranded at step 719 (terminal regret). Stranded inventory is worth zero, so
any agent carrying goods at the end is leaving score on the table.

Usage:
  python benchmark/endgame.py <agent.py> --opp <agent.py> --seeds 5
"""
import argparse
import importlib.util

from kaggle_environments import make
from kaggle_environments.envs.kaggriculture import kaggriculture as KG

BUILTIN = {"starter": KG.starter_agent, "random": KG.random_agent, "pass": KG.pass_agent}


def load(p):
    if p in BUILTIN:
        return BUILTIN[p]
    s = importlib.util.spec_from_file_location("e_" + str(abs(hash(p))), p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m.agent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("agent")
    ap.add_argument("--opp", default="starter")
    ap.add_argument("--seeds", type=int, default=4)
    ap.add_argument("--prices-at", default="day27")
    args = ap.parse_args()

    seeds = [335464115, 846389409, 1184506355, 955895442][: args.seeds]
    a, b = load(args.agent), load(args.opp)
    print(f"{'seed':>11} {'cash':>9} {'shedT':>6} {'carry':>6} {'stranded$':>10} "
          f"{'unharv.':>8}  shed contents")
    tot_stranded = 0
    for sd in seeds:
        env = make("kaggriculture", configuration={"seed": sd, "episodeSteps": 720})
        env.reset()
        for st in range(719):
            o = env.steps[st][0].observation
            env.step([a(o), b(env.steps[st][1].observation)])
        f = env.steps[-1]
        cash = int(f[0].observation.farms[0]["money"])
        priv = f[0].observation.private
        shed = {k: v for k, v in priv["shed"].items() if v}
        shed_t = sum(shed.values())
        carry = {}
        for inv in priv["inventories"]:
            for k, v in inv.items():
                carry[k] = carry.get(k, 0) + v
        carry_t = sum(carry.values())
        prices = f[0].observation.market["prices"]
        stranded = sum(v * prices.get(k, 1) for k, v in {**shed, **carry}.items())
        # mature, unharvested yield still standing on the board
        unharv = 0
        for row in f[0].observation.farms[0]["tiles"]:
            for t in row:
                if isinstance(t, dict) and t.get("kind") == "PLANT":
                    unharv += t.get("yield_units", 0)
        tot_stranded += stranded
        print(f"{sd:>11} {cash:9d} {shed_t:6d} {carry_t:6d} {stranded:10d} {unharv:8d}  {shed or '{}'}")
    print(f"\nmean stranded value at step 719: ${tot_stranded/max(1,len(seeds)):,.0f}")


if __name__ == "__main__":
    main()