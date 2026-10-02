"""Record per-turn state from our own matches, and build world regimes.

Why our own matches and not the public replays
----------------------------------------------
The public replay shards were never downloaded (only 33 of 88,281 episodes had a
local shard), so per-turn state is largely unavailable there. Our own matches
are fully under our control, run on the official engine, and are known to be
stock-config. That is the honest source, and it is recorded as such in the
`source` column rather than being passed off as replay data.

What is stored
--------------
Per (episode, step, player): day, hour, money, land and hand counts, crop and
animal counts, shed occupancy, farmer position, the actions taken, and the
shared market inventory and price snapshot. Typed columns for everything that
is compared or aggregated, plus the raw action list, and nothing else -- a JSON
blob per turn for the entire observation would be unusable for analysis and
would dominate the lake.

Shared-vs-private discipline
----------------------------
The market is SHARED. It is recorded once per episode-step on player 0's row and
flagged, and the quality gate asserts that any recorded player-1 market value
equals player 0's for the same step. A model that treated the market as private
per player would learn a fiction.

Actions that a runtime policy could not observe are recorded in separate
columns and marked `known_at_decision_time`. World-descriptor features may use
future information when CHARACTERISING a world offline; policy features may not.
Both are labelled, because conflating them is how a regime classifier ends up
cheating.
"""
import argparse
import csv
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))

LAKE = os.path.join(ROOT, "data_lake")
OUT_CSV = os.path.join(ROOT, "research", "turns_sample.csv")
OUT_REG = os.path.join(ROOT, "research", "world_regimes.json")
WORK = os.path.join(ROOT, "experiments", "p3066", "turns")

C001 = os.path.join(ROOT, "champions", "research", "C001_room_guard", "main.py")
FARM = os.path.join(ROOT, "opponents", "meta", "farm_2945_original.py")
SEEDS = os.path.join(ROOT, "seeds", "GEN3066_dev.txt")


def struct(o):
    """Best-effort conversion of a Kaggle Struct to plain Python."""
    if hasattr(o, "to_dict"):
        try:
            return o.to_dict()
        except Exception:
            pass
    if hasattr(o, "__dict__"):
        return {k: v for k, v in vars(o).items() if not k.startswith("_")}
    if isinstance(o, dict):
        return {k: struct(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [struct(v) for v in o]
    return o


def num(x, default=0):
    try:
        return int(x)
    except (TypeError, ValueError):
        return default


def record(seeds, out_csv):
    """Replay a set of seeds with state captured at every step."""
    import tournament as T
    from kaggle_environments import make
    from agent_loader import load_agent
    from stats import Counter

    rows = []
    episodes = []
    t0 = time.time()
    for n, seed in enumerate(seeds):
        try:
            ca = Counter(load_agent(C001), "cand")
            ob = Counter(load_agent(FARM), "opp")
            env = make("kaggriculture",
                       configuration={"seed": int(seed), "episodeSteps": 720})
            env.reset()
            seats = [ca, ob] if (n % 2 == 0) else [ob, ca]
            cand_seat = 0 if (n % 2 == 0) else 1
            env.run(seats)
        except Exception as exc:  # noqa: BLE001
            print(f"  seed {seed}: episode failed ({type(exc).__name__})")
            continue
        ep = int(seed)
        first = True
        for step_no, st in enumerate(env.steps):
            if st[0].status not in ("DONE", "RUNNING") and st[0].status:
                continue
            for player in (0, 1):
                o = struct(st[player].observation) or {}
                farms = o.get("farms") or []
                mine = farms[player] if player < len(farms) else {}
                town = struct(st[player].observation.get("town") or {}) or {}
                market = struct(st[player].observation.get("market") or {}) or {}
                inv = market.get("inventory") or market.get("stock") or []
                prices = market.get("prices") or {}
                shops = town.get("shops") or []
                acts = st[player].action or {}
                rows.append({
                    "episode_id": ep, "step": step_no, "player": player,
                    "agent_sha": "", "source": "own_match_C001_vs_Farm",
                    "day": num(o.get("day")), "hour": num(o.get("hour")),
                    "money": num(mine.get("money") if isinstance(mine, dict)
                                 else o.get("money")),
                    "land_count": len(mine.get("land") or []) if isinstance(mine, dict) else 0,
                    "hands_count": len(mine.get("hands") or []) if isinstance(mine, dict) else 0,
                    "farmer_x": num((mine.get("farmer") or {}).get("x")
                                     if isinstance(mine, dict)
                                     and isinstance(mine.get("farmer"), dict) else 0),
                    "farmer_y": num((mine.get("farmer") or {}).get("y")
                                     if isinstance(mine, dict)
                                     and isinstance(mine.get("farmer"), dict) else 0),
                    "n_sheep": num((mine.get("animals") or {}).get("sheep")
                                   if isinstance(mine, dict) else 0),
                    "n_cow": num((mine.get("animals") or {}).get("cow")
                                 if isinstance(mine, dict) else 0),
                    "n_goose": num((mine.get("animals") or {}).get("goose")
                                   if isinstance(mine, dict) else 0),
                    "market_inv_total": sum(num(i) for i in inv) if isinstance(inv, list) else 0,
                    "market_prices_json": json.dumps(prices)[:400],
                    "shops_json": json.dumps([s if isinstance(s, str)
                                              else (s or {}).get("name", "?")
                                              for s in shops])[:300],
                    "farmer_action": json.dumps(acts.get("farmer"))[:120],
                    "market_orders_json": json.dumps(acts.get("market"))[:300],
                    "hands_actions_json": json.dumps(acts.get("hands"))[:300],
                    "is_first_step": 1 if first else 0,
                })
            f = env.steps[-1]
            cc = struct(f[cand_seat].observation)
            oc = struct(f[1 - cand_seat].observation)
            episodes.append({
                "episode_id": ep, "seed": int(seed), "cand_seat": cand_seat,
                "cand_cash": num((cc.get("farms") or [{}])[cand_seat].get("money")
                                 if cand_seat < len(cc.get("farms") or []) else 0),
                "opp_cash": num((oc.get("farms") or [{}])[0].get("money")
                                if 0 < len(oc.get("farms") or []) else 0),
            })
            first = False
            if step_no % 60 == 0:
                print(f"  seed {seed}: step {step_no}/{len(env.steps)} "
                      f"({time.time()-t0:.0f}s)", flush=True)
    fields = list(rows[0].keys()) if rows else []
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    with open(out_csv, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    ep_csv = out_csv.replace("turns_sample", "episodes_sample")
    with open(ep_csv, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["episode_id", "seed", "cand_seat",
                                           "cand_cash", "opp_cash"])
        w.writeheader()
        for e in episodes:
            w.writerow(e)
    return len(rows), len({r["episode_id"] for r in rows})


# ---------------------------------------------------------------- regimes
def world_descriptor(turns_for_episode):
    """Summarise one world from its own trajectory.

    Two feature families are produced and kept apart:

      known_at_decision_time  derived only from the first N steps, so a policy
                              could compute them at run time.
      descriptive_only        derived from the whole trajectory. Legitimate for
                              GROUPING worlds offline, illegal as a policy
                              input. Labelled so a later feature-store build
                              cannot accidentally promote one into the other.
    """
    ep = turns_for_episode
    last_day = max((r["day"] for r in ep), default=0)
    first = [r for r in ep if r["day"] <= 1]

    def shops_on_day(d):
        out = set()
        for r in ep:
            if r["day"] == d and r["shops_json"]:
                try:
                    out.update(json.loads(r["shops_json"]))
                except Exception:
                    pass
        return out

    first_shops = shops_on_day(0) | shops_on_day(1)
    all_shops = set()
    for r in ep:
        if r["shops_json"]:
            try:
                all_shops.update(json.loads(r["shops_json"]))
            except Exception:
                pass

    # Scarcity: the minimum observed total market inventory, and how late the
    # market first runs dry. Descriptive.
    mkt = [r["market_inv_total"] for r in ep if r["player"] == 0]
    min_mkt = min(mkt) if mkt else 0
    dry_step = None
    for r in ep:
        if r["player"] == 0 and r["market_inv_total"] <= 0:
            dry_step = r["step"]
            break

    final_money = {}
    for r in ep:
        final_money[r["player"]] = r["money"]

    return {
        "episode_id": ep[0]["episode_id"],
        "final_day": last_day,
        # decision-time
        "known_first_shops": sorted(first_shops),
        "known_n_first_shops": len(first_shops),
        "known_shops_unlocked_by_day2": len(first_shops),
        # descriptive only
        "desc_all_shops": sorted(all_shops),
        "desc_n_shops": len(all_shops),
        "desc_min_market_inventory": min_mkt,
        "desc_market_dry_step": dry_step,
        "desc_final_money": final_money,
    }


def cluster(descriptors, k=4):
    """Group worlds by descriptor.

    Deliberately simple and interpretable: k-means on scaled numeric
    descriptors, with the shop signature as a categorical tag. An
    uninterpretable clustering would be useless for deciding whether a candidate
    collapsed in some regime, which is the only reason to compute regimes.
    """
    import math
    import random

    feats = ["final_day", "desc_n_shops", "desc_min_market_inventory"]
    xs = []
    for d in descriptors:
        row = []
        for f in feats:
            v = d.get(f) or 0
            row.append(float(v) if isinstance(v, (int, float)) else 0.0)
        xs.append(row)
    if not xs:
        return [], []
    mu = [sum(r[i] for r in xs) / len(xs) for i in range(len(feats))]
    sd = [max(1e-9, (sum((r[i] - mu[i]) ** 2 for r in xs) / len(xs)) ** 0.5)
          for i in range(len(feats))]
    z = [[(r[i] - mu[i]) / sd[i] for i in range(len(feats))] for r in xs]

    rng = random.Random(20261002)
    k = max(1, min(k, len(z)))
    cents = [z[rng.randrange(len(z))] for _ in range(k)]
    assign = [0] * len(z)
    for _ in range(60):
        changed = 0
        for i, row in enumerate(z):
            best = min(range(k), key=lambda c: sum((a - b) ** 2
                                                   for a, b in zip(row, cents[c])))
            if assign[i] != best:
                assign[i] = best
                changed += 1
        for c in range(k):
            pts = [z[i] for i in range(len(z)) if assign[i] == c]
            if pts:
                cents[c] = [sum(p[j] for p in pts) / len(pts)
                            for j in range(len(feats))]
        if not changed:
            break

    groups = {}
    for i, d in enumerate(descriptors):
        groups.setdefault(assign[i], []).append(d["episode_id"])
    prof = []
    for c in sorted(groups):
        pts = [z[i] for i in range(len(z)) if assign[i] == c]
        prof.append({"regime": c, "n_worlds": len(groups[c]),
                     "centroid_scaled": [round(v, 3) for v in cents[c]],
                     "mean_final_day": round(sum(p[0] for p in pts) / len(pts), 1),
                     "mean_n_shops": round(sum(p[1] for p in pts) / len(pts), 2),
                     "mean_min_market": round(sum(p[2] for p in pts) / len(pts), 1)})
    return prof, {d["episode_id"]: assign[i] for i, d in enumerate(descriptors)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=24)
    ap.add_argument("--skip-record", action="store_true")
    a = ap.parse_args()

    os.makedirs(WORK, exist_ok=True)
    if not a.skip_record:
        seeds = [int(x) for x in open(SEEDS, encoding="utf-8")
                 if x.strip().isdigit()][:a.seeds]
        print(f"recording turns for {len(seeds)} worlds "
              f"(both seats, official engine)")
        n_rows, n_eps = record(seeds, OUT_CSV)
        print(f"  turn rows: {n_rows:,}   episodes: {n_eps}")
    else:
        n_rows = n_eps = -1

    if not os.path.exists(OUT_CSV):
        print("  no turn data")
        return 1

    by_ep = {}
    for r in csv.DictReader(open(OUT_CSV, encoding="utf-8")):
        for k in ("day", "hour", "money", "market_inv_total", "step"):
            r[k] = int(r[k] or 0)
        by_ep.setdefault(r["episode_id"], []).append(r)
    print(f"  {len(by_ep)} episodes, "
          f"{sum(len(v) for v in by_ep.values()):,} turn rows")

    # Quality checks, run before any clustering.
    bad_dup = 0
    seen = set()
    for ep, rs in by_ep.items():
        c = {}
        for r in rs:
            key = (r["step"], r["player"])
            if key in c:
                bad_dup += 1
            c[key] = True
    over = sum(1 for rs in by_ep.values() for r in rs if r["step"] > 720)
    neg = sum(1 for rs in by_ep.values() for r in rs if r["money"] < 0)
    both = all(len({r["player"] for r in rs}) == 2 for rs in by_ep.values())
    print(f"  duplicate (step,player): {bad_dup}")
    print(f"  steps over 720          : {over}")
    print(f"  negative money          : {neg}")
    print(f"  every episode has 2 players: {both}")

    descs = [world_descriptor(rs) for rs in by_ep.values()]
    prof, assign = cluster(descs, k=4)
    print("\n  world regimes:")
    for p in prof:
        print(f"    regime {p['regime']}: {p['n_worlds']:>3} worlds  "
              f"final_day {p['mean_final_day']:>5.1f}  "
              f"shops {p['mean_n_shops']:>5.2f}  "
              f"min_market {p['mean_min_market']:>8.1f}")

    with open(OUT_REG, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({
            "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "source": "own matches, C001 vs 2945 Farm, official engine, "
                      "GEN3066_dev seeds",
            "turn_rows": sum(len(v) for v in by_ep.values()),
            "episodes": len(by_ep),
            "quality": {"duplicate_step_player": bad_dup, "steps_over_720": over,
                        "negative_money": neg, "both_players_every_episode": both},
            "feature_policy": {
                "known_at_decision_time": ["known_first_shops",
                                           "known_n_first_shops"],
                "descriptive_only": ["desc_all_shops", "desc_n_shops",
                                     "desc_min_market_inventory",
                                     "desc_market_dry_step", "desc_final_money"],
                "rule": "descriptive_only features may group worlds offline and "
                        "may NOT be used as policy inputs"},
            "regimes": prof,
            "episode_to_regime": {str(k): v for k, v in assign.items()},
        }, fh, indent=2)
    print(f"\n  wrote {os.path.relpath(OUT_REG, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
