"""Forensic trace of an agent: per-day farm, market, shed and action profile.

Usage:
  python benchmark/forensic.py <agent.py> <opp_agent.py|builtin> --seed 335464115 --days 5
"""
import argparse
import importlib.util
import json
from collections import Counter

from kaggle_environments import make
from kaggle_environments.envs.kaggriculture import kaggriculture as KG

MARKET_LOG = []
_sell = KG._commit_unit


def spy(op, item, price, farm, private, market, shed_capacity=100):
    if op == "SELL":
        pre = market["inventory"].get(item, 10000)
        MARKET_LOG.append({"item": item, "qty": 1, "pre_inv": pre, "price": price})
    return _sell(op, item, price, farm, private, market, shed_capacity)


KG._commit_unit = spy


def load(p):
    if p in ("starter", "random", "pass"):
        return {"starter": KG.starter_agent, "random": KG.random_agent,
                "pass": KG.pass_agent}[p]
    s = importlib.util.spec_from_file_location("f_" + str(abs(hash(p))), p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m.agent


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("agent"); ap.add_argument("opp")
    ap.add_argument("--seed", type=int, default=335464115)
    ap.add_argument("--days", type=int, default=6)
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    a, b = load(args.agent), load(args.opp)
    env = make("kaggriculture", configuration={"seed": args.seed, "episodeSteps": 720})
    env.reset()
    rows = []
    for st in range(720):
        o = env.steps[st][0].observation
        if st % 24 == 12:
            f = o.farms[0]
            crops = Counter()
            animals = Counter()
            weeds = empty = 0
            for row in f["tiles"]:
                for t in row:
                    if t is None:
                        empty += 1
                    elif t == "LOCKED":
                        pass
                    elif t.get("kind") == "PLANT":
                        crops[t["crop"]] += 1
                    elif t.get("kind") == "WEED":
                        weeds += 1
                    elif t.get("animal"):
                        animals[t["animal"]] += 1
            shed = {k: v for k, v in o.private["shed"].items() if v}
            rows.append({
                "day": o.day,
                "money": round(f["money"]),
                "land": len(f["unlocked_quadrants"]),
                "hands": len(f["hands"]),
                "crops": dict(crops), "animals": dict(animals),
                "weeds": weeds, "empty": empty,
                "shed": shed,
                "shed_total": sum(shed.values()),
                "market_inv": {k: v - 10000 for k, v in o.market["inventory"].items() if v != 10000},
                "prices": dict(o.market["prices"]),
                "shops": list(o.town["unlocked_shops"]),
            })
            if o.day >= args.days:
                break
        act = a(env.steps[st][0].observation)
        if st < 719:
            env.step([act, b(env.steps[st][1].observation)])

    print(f"seed {args.seed}   agent={args.agent}")
    hdr = f"{'d':>2} {'$':>8} {'land':>4} {'hnd':>3} {'weed':>4} {'empty':>5} {'shedT':>5}  crops / animals"
    print(hdr)
    for r in rows:
        print(f"{r['day']:2d} {r['money']:8d} {r['land']:4d} {r['hands']:3d} {r['weeds']:4d} "
              f"{r['empty']:5d} {r['shed_total']:5d}  {r['crops']} {r['animals']}")
    if rows:
        print(f"\nfinal shops ({len(rows[-1]['shops'])}): {rows[-1]['shops']}")
        print(f"final market excess: {rows[-1]['market_inv']}")
    agg = Counter()
    for m in MARKET_LOG:
        agg[m["item"]] += m["price"]
    print("\nrealised revenue by product (all sells, both players):")
    for k, v in agg.most_common():
        print(f"  {k:11s} ${v:,}")
    print(f"  TOTAL       ${sum(agg.values()):,}")
    if args.out:
        json.dump({"rows": rows, "revenue": dict(agg)}, open(args.out, "w"), indent=1)


if __name__ == "__main__":
    main()