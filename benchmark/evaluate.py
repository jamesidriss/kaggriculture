"""Paired evaluation harness for Kaggriculture.

Primary metric is PAIRWISE WIN RATE.  Same opponent + same seed, both seats.

Usage:
  python benchmark/evaluate.py --cand main.py --opp starter --games 6 --stage dev
"""

import argparse
import importlib.util
import json
import os
import statistics
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kaggle_environments import make  # noqa: E402

BUILTIN = {"pass", "random", "starter"}

# Deterministic, non-overlapping seed pools.
DEV_SEEDS = [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010,
             1011, 1012, 1013, 1014, 1015, 1016]
HOLDOUT_SEEDS = [9001, 9002, 9003, 9004, 9005, 9006, 9007, 9008, 9009, 9010,
                 9011, 9012, 9013, 9014, 9015, 9016]
SMOKE_SEEDS = [77, 78, 79, 80]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_cache = {}


def load_agent(path):
    path = os.path.abspath(path)
    if path in _cache:
        return _cache[path]
    spec = importlib.util.spec_from_file_location("cand_" + str(abs(hash(path))), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fn = getattr(mod, "agent")
    _cache[path] = fn
    return fn


def run_game(agent_path, opp_path, seed, cand_seat):
    cand = load_agent(agent_path)
    agent0 = cand if cand_seat == 0 else opp_path
    agent1 = opp_path if cand_seat == 0 else cand
    env = make("kaggriculture", configuration={"seed": seed, "episodeSteps": 720})
    t0 = time.time()
    try:
        env.reset()
        env.run([agent0, agent1])
        final = env.steps[-1]
        money = [int(final[i].observation.farms[i]["money"]) for i in range(2)]
        rewards = [final[i].reward for i in range(2)]
        statuses = [final[i].status for i in range(2)]
    except Exception as exc:  # noqa: BLE001
        return {"error": repr(exc)[:200], "seed": seed, "seat": cand_seat,
                "runtime_s": time.time() - t0}
    rt = time.time() - t0
    c = money[cand_seat]
    o = money[1 - cand_seat]
    return {
        "seed": seed, "seat": cand_seat,
        "candidate_cash": c, "opponent_cash": o, "margin": c - o,
        "win": c > o, "loss": c < o, "tie": c == o,
        "reward": rewards[cand_seat], "status": statuses[cand_seat],
        "opp_status": statuses[1 - cand_seat],
        "runtime_s": round(rt, 2),
    }


def evaluate(cand_path, opp_path, seeds, label=""):
    rows = []
    for s in seeds:
        for seat in (0, 1):
            rows.append(run_game(cand_path, opp_path, s, seat))
    ok = [r for r in rows if "error" not in r]
    errs = [r for r in rows if "error" in r]
    wins = sum(1 for r in ok if r["win"])
    losses = sum(1 for r in ok if r["loss"])
    ties = sum(1 for r in ok if r["tie"])
    n = len(ok)
    res = {
        "label": label,
        "candidate": cand_path, "opponent": opp_path,
        "games": n, "errors": len(errs),
        "wins": wins, "losses": losses, "ties": ties,
        "win_rate": round(wins / n, 4) if n else 0.0,
        "score_rate": round((wins + 0.5 * ties) / n, 4) if n else 0.0,
        "mean_cash": round(statistics.mean([r["candidate_cash"] for r in ok])) if ok else 0,
        "mean_opp": round(statistics.mean([r["opponent_cash"] for r in ok])) if ok else 0,
        "mean_margin": round(statistics.mean([r["margin"] for r in ok])) if ok else 0,
        "max_runtime_s": max([r["runtime_s"] for r in ok]) if ok else 0,
        "seat0": {"w": sum(1 for r in ok if r["seat"] == 0 and r["win"]),
                  "l": sum(1 for r in ok if r["seat"] == 0 and r["loss"]),
                  "t": sum(1 for r in ok if r["seat"] == 0 and r["tie"])},
        "seat1": {"w": sum(1 for r in ok if r["seat"] == 1 and r["win"]),
                  "l": sum(1 for r in ok if r["seat"] == 1 and r["loss"]),
                  "t": sum(1 for r in ok if r["seat"] == 1 and r["tie"])},
        "error_samples": [e["error"] for e in errs[:3]],
    }
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cand", default="main.py")
    ap.add_argument("--opp", default="starter")
    ap.add_argument("--games", type=int, default=4)
    ap.add_argument("--stage", default="dev", choices=["smoke", "dev", "holdout"])
    ap.add_argument("--json", default="")
    args = ap.parse_args()

    seeds = {"smoke": SMOKE_SEEDS, "dev": DEV_SEEDS, "holdout": HOLDOUT_SEEDS}[args.stage]
    seeds = seeds[: max(1, args.games)]

    opp = args.opp
    opp_path = opp if opp in BUILTIN else opp
    res = evaluate(args.cand, opp_path, seeds, label=f"{args.stage}:{opp}")
    print(json.dumps(res, indent=2))
    if args.json:
        with open(args.json, "w") as f:
            json.dump(res, f, indent=2)


if __name__ == "__main__":
    main()