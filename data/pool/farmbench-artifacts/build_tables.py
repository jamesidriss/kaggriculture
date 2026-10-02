"""Offline table builder for FarmBench (run locally, <= 3 workers; never on Kaggle).

For every SIM task, every menu arm is played by the engine: hero = kaggriculture/submissions_v32_main.py with the
arm's knob overrides (+ optional BUY_LAND injection), opponent = Tschinkel's public shop-router (league2 gate bot),
fixtown applied (town = f(seed)), both seats, the task's seeds. Output:
  tables/games.jsonl            one line per game (resumable)
  tables/farmbench_tables.json  per task: arms, per-arm mean hero coins / margin, best arm, naive arm
  states/<task>.json            the hero's observation at the decision step (default arm, first seed, seat 0) + text

python build_tables.py [--workers 3] [--tasks opening,sheep_yarn,...] [--states-only]
"""
import os, sys, json, time, argparse, collections
from concurrent.futures import ProcessPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))                       # kaggle-competition
KAG = os.path.join(ROOT, "kaggriculture")
LEAGUE2 = os.path.join(KAG, "variants", "league2")
FIXTOWN = os.path.join(KAG, "variants", "late")
HERO_PATH = os.path.join(KAG, "submissions_v32_main.py")
OPP_NAME = "tschinkel"
SHOPS = {"BAKERY": ["EGG", "WHEAT"], "PIZZA_SHOP": ["MILK", "TOMATO", "WHEAT"], "BRUNCH_SPOT": ["EGG", "WHEAT", "STRAWBERRY"],
         "YARN_STORE": ["WOOL"], "ICE_CREAM_SHOP": ["STRAWBERRY", "MILK", "WHEAT"], "PET_CAFE": ["CARROT"],
         "SMOOTHIE_SHOP": ["STRAWBERRY", "MILK"], "FARMERS_MARKET": ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY"]}
PRODUCTS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER"]

MIX6 = [9300, 9301, 9303, 9305, 9310, 9316]
YARN4 = [9301, 9308, 9309, 9312]          # yarn store unlocked by day 6
NOYARN4 = [9300, 9304, 9305, 9307]        # no yarn store all season
TOMATO4 = [9300, 9310, 9316, 9318]        # pizza shop / farmers market towns
CARROT4 = [9300, 9301, 9302, 9305]        # pet cafe towns

def _term_tomato(day):
    return dict(term_tomato=True, term_tomato_days=(day,), term_tomato_min_price=0, term_tomato_floor=0)

def _term_carrot(day):
    return dict(term_carrot=True, term_carrot_days=(day,), term_carrot_min_price=0, term_carrot_floor=0)

SHEEP_BASE = dict(demand_aware=False, max_cows=8, max_geese=4, min_sheep=0)

# arm = (knob overrides, injection) ; injection = dict(from_day=D, quadrants=N): BUY_LAND every hour from day D until N owned
TASKS = {
    "opening": dict(day=0, seeds=MIX6, naive="cautious", arms={
        "meta_a":   (dict(cows_day0=2, sheep_day0=3, melon_tiles=6, wheat_day0=10, geese_day0=0, straw_day0=0), None),
        "default":  (dict(), None),
        "melon_max": (dict(cows_day0=0, melon_tiles=25, wheat_day0=10), None),
        "goose_farm": (dict(cows_day0=0, geese_day0=6, melon_tiles=6, wheat_day0=10), None),
        "cautious": (dict(cows_day0=0, melon_tiles=4, wheat_day0=6), None),
        "strawberry_rush": (dict(cows_day0=0, melon_tiles=0, straw_day0=20, wheat_day0=6), None),
        "land_first": (dict(cows_day0=0, land_day0=True, melon_tiles=12, wheat_day0=8), None),
        "cows_only": (dict(cows_day0=6, melon_tiles=0, wheat_day0=6), None),
    }),
    "sheep_yarn": dict(day=6, seeds=YARN4, naive="sheep_0", arms={
        f"sheep_{n}": (dict(SHEEP_BASE, max_sheep=n), None) for n in (0, 2, 4, 6, 8)}),
    "sheep_no_yarn": dict(day=6, seeds=NOYARN4, naive="sheep_0", arms={
        f"sheep_{n}": (dict(SHEEP_BASE, max_sheep=n), None) for n in (0, 2, 4, 6, 8)}),
    "se_quadrant": dict(day=12, seeds=MIX6, naive="never", arms={
        "never": (dict(), None),
        "buy_day12": (dict(), dict(from_day=12, quadrants=4)),
        "buy_day16": (dict(), dict(from_day=16, quadrants=4)),
        "buy_day20": (dict(), dict(from_day=20, quadrants=4)),
    }),
    "land_ne_timing": dict(day=2, seeds=MIX6, naive="never", arms=dict(
        {f"day{d}": (dict(), dict(from_day=d, quadrants=2)) for d in (2, 4, 6, 8, 10)},
        never=(dict(land_last_day=-1), None),
        default=(dict(), None),
    )),
    "max_hands": dict(day=0, seeds=MIX6, naive="hands_2", arms={
        f"hands_{n}": (dict(max_hands=n), None) for n in (2, 4, 6, 8, 10, 12, 14)}),
    "terminal_tomato": dict(day=16, seeds=TOMATO4, naive="off", arms=dict(
        {f"plant_day{d}": (_term_tomato(d), None) for d in (16, 18, 20, 22)},
        off=(dict(term_tomato=False), None),
    )),
    "terminal_carrot": dict(day=24, seeds=CARROT4, naive="off", arms=dict(
        {f"plant_day{d}": (_term_carrot(d), None) for d in (24, 25, 26, 27)},
        off=(dict(term_carrot=False), None),
    )),
}


def _setup():
    for p in (LEAGUE2, FIXTOWN):
        if p not in sys.path: sys.path.insert(0, p)
    import fixtown; fixtown.apply()


def make_hero(knobs, inject, record=None):
    from league import load
    agent = load(HERO_PATH, dict(knobs) if knobs else None)
    n_in = getattr(getattr(agent, "__code__", None), "co_argcount", 2)
    def hero(obs, cfg=None):
        step = int(obs["step"]); me = int(obs["player"])
        if record is not None and step == record["step"] and "obs" not in record:
            record["obs"] = json.loads(json.dumps(obs))
        a = agent(obs, cfg) if n_in >= 2 else agent(obs)
        if inject and step >= inject["from_day"] * 24 and len(obs["farms"][me]["unlocked_quadrants"]) < inject["quadrants"]:
            mk = [o for o in list(a.get("market", [])) if o and o[0] != "BUY_LAND"]
            a = dict(a); a["market"] = ([["BUY_LAND"]] + mk)[:10]
        return a
    return hero


def play(job):
    task, arm, seed, first, knobs, inject, want_state = job
    _setup()
    os.environ["L2_SEED"] = str(seed)
    from league import load
    import bots
    from kaggle_environments import make
    t0 = time.time()
    try:
        rec = {"step": TASKS[task]["day"] * 24} if want_state else None
        H = make_hero(knobs, inject, rec)
        spec = bots.OPPS[OPP_NAME]; O = load(spec["path"], spec.get("ov"))
        env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": seed})
        env.run([H, O] if first else [O, H])
        st = env.steps[-1]; i = 0 if first else 1
        r = [s.reward for s in st]
        out = {"task": task, "arm": arm, "seed": seed, "first": first, "me": r[i], "them": r[1 - i],
               "status": [s.status for s in st], "secs": round(time.time() - t0, 1),
               "quads": env.steps[-1][0].observation["farms"][i]["unlocked_quadrants"]}
        if rec is not None and "obs" in rec:
            out["state"] = rec["obs"]
        return out
    except Exception as e:
        import traceback
        return {"task": task, "arm": arm, "seed": seed, "first": first, "error": repr(e), "tb": traceback.format_exc()[-600:]}


# ---------------------------------------------------------------- state rendering
def farm_summary(farm, day):
    plants = collections.Counter(); animals = collections.Counter(); structures = collections.Counter(); weeds = 0; empty = 0
    for row in farm["tiles"]:
        for t in row:
            if t is None: empty += 1
            elif t == "LOCKED": continue
            elif t.get("kind") == "WEED": weeds += 1
            elif t.get("kind") == "PLANT": plants[(t["crop"], day - t["planted_day"])] += 1
            elif "animal" in t: animals[t["animal"]] += 1
            else: structures[t["kind"]] += 1
    parts = [f"{n} {crop} (age {age})" for (crop, age), n in sorted(plants.items())]
    parts += [f"{n} {a}" for a, n in sorted(animals.items())]
    parts += [f"{n} empty {k}" for k, n in sorted(structures.items())]
    if weeds: parts.append(f"{weeds} weeds")
    return ", ".join(parts) or "empty", empty


def render_state(obs):
    me = obs["player"]; op = 1 - me; day = obs["day"]; hour = obs["hour"]
    farm = obs["farms"][me]; ofarm = obs["farms"][op]; priv = obs["private"]; mk = obs["market"]
    mine, empty = farm_summary(farm, day); theirs, _ = farm_summary(ofarm, day)
    shops = obs["town"]["unlocked_shops"]
    shop_txt = ", ".join(f"{s} (buys {'/'.join(SHOPS[s])}{' x2' if len(SHOPS[s]) == 1 else ''})" for s in shops) or "none yet"
    prices = ", ".join(f"{p} ${mk['prices'][p]}" for p in PRODUCTS)
    invs = ", ".join(f"{p} {mk['inventory'][p] - 10000:+d}" for p in PRODUCTS if mk["inventory"][p] != 10000) or "all at I0"
    shed = ", ".join(f"{k} {v}" for k, v in priv["shed"].items() if v) or "empty"
    seeds = ", ".join(f"{k} {v}" for k, v in priv["seeds"].items() if v) or "none"
    lines = [
        f"Day {day}, hour {hour} of 24 ({30 - day} days including today remain). Cash ${farm['money']:,.0f}.",
        f"Your land: {', '.join(farm['unlocked_quadrants'])} ({25 * len(farm['unlocked_quadrants'])} tiles, {empty} empty). Hands hired today: {len(farm['hands'])}.",
        f"Town shops open: {shop_txt}.",
        f"Market prices: {prices}.",
        f"Market inventory relative to neutral I0 (negative = scarce, positive = glut): {invs}.",
        f"Your farm: {mine}. Shed: {shed}. Seeds in hand: {seeds}.",
        f"Opponent's visible farm: {theirs}; land {', '.join(ofarm['unlocked_quadrants'])}; cash ${ofarm['money']:,.0f}; hands today {len(ofarm['hands'])}.",
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--tasks", default=",".join(TASKS))
    ap.add_argument("--states-only", action="store_true")
    a = ap.parse_args()
    tasks = [t for t in a.tasks.split(",") if t]
    os.makedirs(os.path.join(HERE, "tables"), exist_ok=True); os.makedirs(os.path.join(HERE, "states"), exist_ok=True)
    games_path = os.path.join(HERE, "tables", "games.jsonl")
    done = set(); rows = []
    if os.path.exists(games_path):
        for line in open(games_path):
            d = json.loads(line)
            if "error" in d: continue
            done.add((d["task"], d["arm"], d["seed"], d["first"])); rows.append(d)
    jobs = []
    for t in tasks:
        T = TASKS[t]
        for arm, (knobs, inject) in T["arms"].items():
            for seed in T["seeds"]:
                for first in (True, False):
                    want_state = (arm == T["naive"] and seed == T["seeds"][0] and first)
                    if a.states_only and not want_state: continue
                    if (t, arm, seed, first) in done and not (want_state and not os.path.exists(os.path.join(HERE, "states", f"{t}.json"))):
                        continue
                    jobs.append((t, arm, seed, first, knobs, inject, want_state))
    print(f"{len(jobs)} games to play ({len(done)} done), workers {a.workers}", flush=True)
    t0 = time.time(); errs = 0
    with ProcessPoolExecutor(a.workers) as ex, open(games_path, "a") as fh:
        futs = [ex.submit(play, j) for j in jobs]
        for k, fu in enumerate(as_completed(futs), 1):
            r = fu.result()
            if "error" in r:
                errs += 1; print(f"[{k}/{len(jobs)}] ERROR {r['task']} {r['arm']} s{r['seed']}: {r['error']}\n{r['tb']}", flush=True); continue
            if "state" in r:
                st = r.pop("state")
                json.dump({"task": r["task"], "arm": r["arm"], "seed": r["seed"], "obs": st, "text": render_state(st)},
                          open(os.path.join(HERE, "states", f"{r['task']}.json"), "w"), indent=1)
            if (r["task"], r["arm"], r["seed"], r["first"]) not in done:
                fh.write(json.dumps(r) + "\n"); fh.flush(); rows.append(r); done.add((r["task"], r["arm"], r["seed"], r["first"]))
            if k % 10 == 0 or k == len(jobs):
                print(f"[{k}/{len(jobs)} {time.time()-t0:5.0f}s] {r['task']} {r['arm']} s{r['seed']} {'1st' if r['first'] else '2nd'}: {r['me']:7.0f} - {r['them']:7.0f} ({r['secs']}s) quads={r['quads']}", flush=True)
    print(f"done in {time.time()-t0:.0f}s, {errs} errors", flush=True)
    summarize(rows)


def summarize(rows):
    out = {}
    by = collections.defaultdict(list)
    for r in rows: by[(r["task"], r["arm"])].append(r)
    for t, T in TASKS.items():
        arms = {}
        for arm in T["arms"]:
            g = by.get((t, arm), [])
            if not g: continue
            me = [x["me"] for x in g]; mg = [x["me"] - x["them"] for x in g]
            arms[arm] = dict(n=len(g), coins=round(sum(me) / len(me)), margin=round(sum(mg) / len(mg)),
                             wins=sum(1 for x in g if x["me"] > x["them"]),
                             per_game={f"{x['seed']}{'a' if x['first'] else 'b'}": round(x["me"]) for x in g})
        if not arms: continue
        best = max(arms, key=lambda k: arms[k]["coins"])
        out[t] = dict(day=T["day"], seeds=T["seeds"], naive=T["naive"], best=best, arms=arms,
                      knobs={arm: {"knobs": kn, "inject": inj} for arm, (kn, inj) in T["arms"].items()})
    json.dump(out, open(os.path.join(HERE, "tables", "farmbench_tables.json"), "w"), indent=1)
    for t, d in out.items():
        print(f"\n== {t} (day {d['day']}, naive {d['naive']}, best {d['best']})")
        for arm, s in sorted(d["arms"].items(), key=lambda kv: -kv[1]["coins"]):
            print(f"  {arm:16s} n={s['n']:2d} coins {s['coins']:7d} margin {s['margin']:+7d} wins {s['wins']}")


if __name__ == "__main__":
    main()
