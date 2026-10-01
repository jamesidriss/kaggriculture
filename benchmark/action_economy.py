"""Action-economy and worker-utilisation forensics for a candidate agent.

Instruments the official interpreter to attribute every unit action to a
category, then reports productivity ratios per agent and per day. Also measures
worker ROI (hands hired vs actions delivered).

Usage:
  python benchmark/action_economy.py a.py b.py --seeds 5
"""
import argparse
import importlib.util
import statistics
from collections import Counter, defaultdict

from kaggle_environments import make
from kaggle_environments.envs.kaggriculture import kaggriculture as KG

CATS = {"NORTH": "movement", "SOUTH": "movement", "EAST": "movement", "WEST": "movement",
        "PASS": "pass", "WATER": "maintenance", "FEED": "maintenance", "CARE": "maintenance",
        "COLLECT_FERTILIZER": "maintenance", "DIG": "maintenance", "FERTILIZE": "maintenance",
        "PLANT": "production", "HARVEST": "production", "BUILD_COOP": "production",
        "BUILD_PASTURE": "production", "PICKUP": "logistics", "PLACE": "logistics",
        "DROP": "logistics"}

MARKET = Counter()


def load(p):
    s = importlib.util.spec_from_file_location("a_" + str(abs(hash(p))), p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m.agent


def instrument():
    stats = {"cats": Counter(), "hands_hist": [], "day_cats": defaultdict(Counter)}
    orig = KG._apply_unit_action
    orig_proc = KG._process_market

    def spy(farm, private, idx, action, board_size, day, turns_per_day, shed_capacity=100):
        if isinstance(action, list) and action:
            op = action[0]
            stats["cats"][CATS.get(op, "other:" + str(op))] += 1
            stats["day_cats"][day][CATS.get(op, "other")] += 1
            stats["hands_hist"].append(len(farm.get("hands") or []))
        return orig(farm, private, idx, action, board_size, day, turns_per_day, shed_capacity)

    def spy_mkt(state, env):
        for s in state:
            a = s.action if isinstance(s.action, dict) else {}
            for o in (a.get("market") or []):
                if isinstance(o, list) and o:
                    MARKET[o[0]] += 1
        return orig_proc(state, env)

    KG._apply_unit_action = spy
    KG._process_market = spy_mkt
    return stats


def _resolve(x):
    """Accept either a path or an already-loaded callable."""
    return x if callable(x) else load(x)


def report(name, agent_path, opp_path, seeds):
    stats = instrument()
    MARKET.clear()
    cash = []
    for sd in seeds:
        a, b = _resolve(agent_path), _resolve(opp_path)
        env = make("kaggriculture", configuration={"seed": sd, "episodeSteps": 720})
        env.reset()
        env.run([a, b])
        cash.append(int(env.steps[-1][0].observation.farms[0]["money"]))
    c = stats["cats"]
    tot = sum(c.values()) or 1
    print(f"\n=== {name}  (median cash ${int(statistics.median(cash)):,})")
    print(f"  total field actions {tot}")
    for k in ("production", "maintenance", "movement", "logistics", "pass"):
        v = c.get(k, 0)
        print(f"  {k:12s} {v:7d}  {v/tot:6.1%}")
    prod = c.get("production", 0) + c.get("maintenance", 0)
    print(f"  productive/total  {prod/tot:6.1%}")
    print(f"  cash per field action  ${statistics.median(cash)/tot:,.2f}")
    mt = sum(MARKET.values()) or 1
    print(f"  market orders {mt}: " +
          ", ".join(f"{k}={v}" for k, v in MARKET.most_common(6)))
    hh = stats["hands_hist"]
    if hh:
        print(f"  hands: mean {statistics.mean(hh):.1f} max {max(hh)}")
    late = Counter()
    for d in range(24, 30):
        late.update(stats["day_cats"].get(d, {}))
    lt = sum(late.values()) or 1
    if late:
        print(f"  days 24-29 actions {lt}: production {late.get('production',0)/lt:.0%} "
              f"maintenance {late.get('maintenance',0)/lt:.0%} movement {late.get('movement',0)/lt:.0%}")
    KG._apply_unit_action = KG._apply_unit_action
    return tot


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("agents", nargs="+")
    ap.add_argument("--seeds", type=int, default=5)
    ap.add_argument("--opp", default="starter")
    a = ap.parse_args()
    seeds = [335464115, 846389409, 1184506355, 955895442, 725584983][: a.seeds]
    BUILTIN = {"starter": KG.starter_agent, "random": KG.random_agent, "pass": KG.pass_agent}
    opp_path = BUILTIN[a.opp] if a.opp in BUILTIN else a.opp
    for p in a.agents:
        report(p, p, opp_path, seeds)