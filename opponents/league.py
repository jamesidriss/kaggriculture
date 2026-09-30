"""Stronger opponent league for Kaggriculture.

The three built-ins are smoke tests, not evidence. This file adds distinct
strategy families written from the official rules so that a regression in any
one dimension shows up as a regression against that family.

Families:
  crop_wheat   - glut-safe wheat treadmill, the same backbone as our champion
  crop_melon   - premium tranches against a finite price pot
  land_rush    - buys all four quadrants immediately and hires hard
  hands_max    - maximum fib hand ladder, minimal crops
  patient      - plays few crops well, hoards cash for late land
"""

from kaggle_environments.envs.kaggriculture.kaggriculture import CROPS, MARKET_PARAMS


def _farm(obs):
    return obs["farms"][obs["player"]]


def _empty_tiles(farm):
    return [(x, y) for y, row in enumerate(farm["tiles"])
            for x, t in enumerate(row) if t is None]


def _shed_adjacent(board):
    h = board // 2
    return [(h - 1, h - 1), (h, h - 1), (h - 1, h), (h, h)]


def _move(ux, uy, tx, ty, n):
    dx, dy = tx - ux, ty - uy
    if dx == 0 and dy == 0:
        return ["PASS"]
    if abs(dx) >= abs(dy):
        if dx > 0 and ux + 1 < n:
            return ["EAST"]
        if dx < 0 and ux > 0:
            return ["WEST"]
    if dy > 0 and uy + 1 < n:
        return ["SOUTH"]
    if dy < 0 and uy > 0:
        return ["NORTH"]
    return ["PASS"]


def _make_unit_op(obs, pos, crop, mode):
    farm = _farm(obs)
    day = obs["day"]
    priv = obs["private"]
    n = len(farm["tiles"])
    x, y = pos
    tile = farm["tiles"][y][x]
    seeds = priv["seeds"]

    if tile is None:
        if seeds.get(crop, 0) > 0:
            return ["PLANT", crop]
        # Go find an empty tile nearby to plant.
        best = None
        for (tx, ty) in _empty_tiles(farm):
            d = abs(tx - x) + abs(ty - y)
            if d <= 3 and (best is None or d < best[0]):
                best = (d, tx, ty)
        if best and best[1:] != (x, y):
            return _move(x, y, best[1], best[2], n)
        return ["PASS"]

    if isinstance(tile, dict):
        if tile.get("kind") == "PLANT":
            cd = CROPS[tile["crop"]]
            age = day - tile["planted_day"]
            if (tile.get("yield_units", 0) > 0 and age >= cd["max_yield_day"]
                    and day <= 27):
                return ["HARVEST"]
            if not tile.get("watered_today", False):
                return ["WATER"]
        elif tile.get("kind") == "WEED":
            return ["DIG"]
    return ["PASS"]


def _market(obs, mode, sell_floor_frac):
    farm = _farm(obs)
    priv = obs["private"]
    day = obs["day"]
    money = farm["money"]
    shed = priv["shed"]
    orders = []

    unlocked = len(farm.get("unlocked_quadrants") or ["NW"])

    if mode == "land_rush":
        prices = [1000, 2000, 4000]
        idx = unlocked - 1
        if idx < 3 and money >= prices[idx]:
            orders.append(["BUY_LAND"])
            money -= prices[idx]
    elif mode == "patient":
        idx = unlocked - 1
        if idx < 3 and money >= prices_needed(obs) + 2500:
            orders.append(["BUY_LAND"])

    crop = "MELON" if mode == "crop_melon" else "WHEAT"
    if mode == "patient":
        crop = "CARROT"

    # Seeds in bulk, the lesson our own agent learned the hard way.
    want = 100 if mode != "hands_max" else 20
    if seeds_have(priv, crop) < want and money > CROPS[crop]["seed"] * 4:
        orders.append(["BUY_SEED", crop, min(want, int(money // CROPS[crop]["seed"]))])

    if mode == "hands_max":
        target = 14
    elif mode == "patient":
        target = 4
    else:
        target = min(10, max(3, unlocked * 5 // 5))
    cap = 14 if mode == "hands_max" else (4 if mode == "patient" else 12)
    target = min(target, cap)
    spent = 0
    while len(farm.get("hands") or []) < target and spent < money * 0.35:
        n = farm.get("hires_today", 0)
        cost = fib(n)
        orders.append(["HIRE"])
        spent += cost
        money -= cost

    inv = obs["market"]["inventory"]
    for item in MARKET_PARAMS:
        qty = shed.get(item, 0)
        if qty <= 0:
            continue
        floor = MARKET_PARAMS[item]["base"] * sell_floor_frac
        if price_at(item, inv.get(item, 10000) + qty) >= floor or inv.get(item, 10000) >= 10000:
            orders.append(["SELL", item, qty])
    return orders[:10]


def prices_needed(obs):
    idx = len(obs["farms"][obs["player"]].get("unlocked_quadrants") or ["NW"]) - 1
    return [1000, 2000, 4000][idx] if idx < 3 else 0


def seeds_have(priv, crop):
    return priv["seeds"].get(crop, 0)


def price_at(item, inventory):
    p = MARKET_PARAMS[item]
    base, T = p["base"], p["T"]
    I0 = p["I0"]
    if inventory < I0:
        f = {"sqrt": lambda x: x ** 0.5, "log": lambda x: __import__("math").log(1 + x),
             "linear": lambda x: x, "hinge": lambda x: x / T}[p["below_func"]]
        amp = p["below_target"] * base / f(T)
        return max(1, round(base + amp * f(I0 - inventory)))
    f = {"sq": lambda x: x * x, "log": lambda x: __import__("math").log(1 + x),
         "sqrt": lambda x: x ** 0.5, "linear": lambda x: x}[p["above_func"]]
    amp = p["above_target"] * base / f(T)
    return max(1, round(base - amp * f(inventory - I0)))


def fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _build(mode, crop, hands, floor):
    def agent(obs):
        try:
            farm = _farm(obs)
            n = len(farm["tiles"])
            units = [tuple(farm["farmer"])] + [(p[0], p[1]) for p in (farm.get("hands") or [])]
            acts = [_make_unit_op(obs, u, crop, mode) for u in units[:hands + 1]]
            return {
                "farmer": acts[0],
                "hands": acts[1:],
                "market": _market(obs, mode, floor),
            }
        except Exception:
            return {"farmer": ["PASS"], "hands": [], "market": []}
    return agent


crop_wheat = _build("crop_wheat", "WHEAT", 10, 0.40)
crop_melon = _build("crop_melon", "MELON", 10, 0.42)
land_rush = _build("land_rush", "WHEAT", 12, 0.40)
hands_max = _build("hands_max", "WHEAT", 14, 0.40)
patient = _build("patient", "CARROT", 4, 0.45)

LEAGUE = {
    "crop_wheat": crop_wheat,
    "crop_melon": crop_melon,
    "land_rush": land_rush,
    "hands_max": hands_max,
    "patient": patient,
}