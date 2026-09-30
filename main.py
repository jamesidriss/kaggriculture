"""
Kaggriculture agent -- "Sunrise v1"

Design notes
------------
Primary metric is PAIRWISE WIN RATE, so this agent optimises *banked cash by the
final turn*, not throughput.

Four pillars:

1. ACTION SAFETY.  Every plant starts at consecutive_unwatered == 1, and the
   planting day counts as a miss, so an unwatered seedling dies that night.
   Watering a plant that has already missed a day is therefore the single
   highest-priority task and is scheduled before anything else.

2. REPLICATED PRICE FUNCTION.  MARKET_PARAMS from the official environment is
   mirrored below, so we can compute the exact sale price of every product at
   any market inventory.  That lets us sell in *tranches*: dump staples
   (WHEAT / EGG / FERTILIZER use `log`/`linear` glut curves and never really
   crash) wholesale, while rationing premiums (MELON / WOOL / MILK /
   STRAWBERRY use `sq`/`linear` with above_target > 1 and hit the $1 floor on
   modest gluts) down to whatever keeps the unit price above a floor fraction
   of base.  Melon is the highest-margin crop in the game and has *no* town
   shop demand, so its whole season is a single finite ~$25k budget that we
   extract with tranche selling rather than dumping at once.

3. MARKET ORDERS ARE FREE.  Only field actions cost a worker action.  Seeds,
   land, hiring and sales all ride the 10-orders-per-turn queue, so we can run
   a wide harvest with very few hands.

4. HORIZON DISCIPLINE.  Unsold inventory is worth nothing, so nothing is
   planted or harvested that cannot still be converted to cash before step 720.

No fertilizer is ever purchased: at the official fixed $100 buy price, the
+1/+2 yield bonus on a 4-day wheat cycle is worth about $38 of extra product.
It is a net loss and it also burns a field action.

Public domain / original work.  Mirrors constants from
kaggle_environments.envs.kaggriculture.kaggriculture (Apache-2.0) for exactness.
"""

import math

# --------------------------------------------------------------------------
# Official constants (mirrored from kaggle_environments kaggriculture.py)
# --------------------------------------------------------------------------

CROPS = {
    "WHEAT":      {"seed": 10,  "first": 2,  "max": 4,  "maxy": 6, "ongoing": False},
    "CARROT":     {"seed": 20,  "first": 2,  "max": 3,  "maxy": 4, "ongoing": False},
    "TOMATO":     {"seed": 50,  "first": 8,  "max": 8,  "maxy": 4, "ongoing": True,  "iv": 1},
    "STRAWBERRY": {"seed": 100, "first": 10, "max": 10, "maxy": 4, "ongoing": True,  "iv": 2},
    "MELON":      {"seed": 80,  "first": 10, "max": 12, "maxy": 6, "ongoing": False},
}

MARKET_PARAMS = {
    "WHEAT":      {"base":  25, "I0": 10000, "T": 400, "bf": "sqrt",  "bt": 0.80, "af": "log",    "at": 0.20},
    "CARROT":     {"base":  35, "I0": 10000, "T": 450, "bf": "hinge", "bt": 1.00, "af": "sqrt",   "at": 0.70},
    "TOMATO":     {"base":  60, "I0": 10000, "T": 200, "bf": "hinge", "bt": 0.40, "af": "sqrt",   "at": 0.60},
    "STRAWBERRY": {"base": 120, "I0": 10000, "T": 100, "bf": "sqrt",  "bt": 0.70, "af": "linear", "at": 1.60},
    "MELON":      {"base": 250, "I0": 10000, "T": 300, "bf": "log",   "bt": 0.20, "af": "sq",     "at": 3.60},
    "EGG":        {"base":  50, "I0": 10000, "T": 332, "bf": "hinge", "bt": 0.40, "af": "log",    "at": 0.20},
    "MILK":       {"base": 160, "I0": 10000, "T": 122, "bf": "sqrt",  "bt": 0.60, "af": "linear", "at": 1.60},
    "WOOL":       {"base": 200, "I0": 10000, "T": 105, "bf": "log",   "bt": 0.20, "af": "sq",     "at": 3.20},
    "FERTILIZER": {"base": 100, "I0": 10000, "T": 200, "bf": "linear", "bt": 0.40, "af": "linear", "at": 0.40},
}

PRODUCTS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON",
            "EGG", "MILK", "WOOL", "FERTILIZER"]

LAND_PRICES = [1000, 2000, 4000]
SHED_CAPACITY = 100
MAX_MARKET_ORDERS = 10
TURNS_PER_DAY = 24
LAST_DAY = 29

# Fraction of base price we refuse to sell below. Staples absorb gluts so this
# never binds for them; for premiums it is the whole strategy.
SELL_FLOOR = {
    "WHEAT": 0.40, "CARROT": 0.45, "TOMATO": 0.45, "STRAWBERRY": 0.50,
    "MELON": 0.42, "EGG": 0.40, "MILK": 0.55, "WOOL": 0.55,
    "FERTILIZER": 0.50,
}

# --------------------------------------------------------------------------
# Policy constants
# --------------------------------------------------------------------------

MAX_TRAVEL = 4        # how far a worker will walk for a task (Manhattan)
HAND_CAP = 12         # fib ladder: 12 hands already costs $376/day
SEED_BATCH = 26       # max seeds of a crop bought per turn
HAND_SPEND_FRAC = 0.30  # never spend more than this share of the bank on hands
LAND_CASH_MULT = 2.2  # only buy land while the surplus covers it many times over
LAND_BUFFER = 800
MELON_SEED_MIN_CASH = 1500  # melon seed competes with the hand ladder

# Planting windows: last day a planting can still be harvested AND sold.
PLANT_LAST_DAY = {"WHEAT": 24, "CARROT": 25, "MELON": 16, "TOMATO": 20, "STRAWBERRY": 18}
HARVEST_LAST_DAY = 28  # day 29 produce is dropped at end of day and never sold


# --------------------------------------------------------------------------
# Price function (exact replica of the official market_price)
# --------------------------------------------------------------------------

def _shape(func, x, T):
    x = max(0.0, x)
    if func == "linear":
        return x
    if func == "sq":
        return x * x
    if func == "sqrt":
        return math.sqrt(x)
    if func == "log":
        return math.log(1.0 + x)
    if func == "log10":
        return math.log10(1.0 + x)
    if func == "hinge":
        if not T or T <= 0:
            return x
        u = x / T
        return u + 8.0 * max(0.0, u - 1.0) ** 2
    return x


def _price(item, inventory):
    p = MARKET_PARAMS[item]
    base, I0, T = p["base"], p["I0"], p["T"]
    if inventory < I0:
        f, tgt = p["bf"], p["bt"]
        amp = tgt * base / _shape(f, T, T)
        price = base + amp * _shape(f, I0 - inventory, T)
    else:
        f, tgt = p["af"], p["at"]
        amp = tgt * base / _shape(f, T, T)
        price = base - amp * _shape(f, inventory - I0, T)
    return max(1, int(round(price)))


def _sell_quantity(item, inventory, available):
    """How many units of `item` to sell now.

    Sells everything for glut-safe goods.  For crash-prone premiums it finds the
    largest k <= available such that the *post-sale* unit price still clears the
    floor fraction of base, which keeps total season value near the integral of
    the price curve instead of collapsing it in one dump.
    """
    if available <= 0:
        return 0
    if item not in MARKET_PARAMS:
        return 0
    floor = SELL_FLOOR[item] * MARKET_PARAMS[item]["base"]
    if _price(item, inventory + available) >= floor:
        return available
    lo, hi = 0, available          # price(inv+lo) ok, price(inv+hi) too low
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if _price(item, inventory + mid) >= floor:
            lo = mid
        else:
            hi = mid
    return lo


# --------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------

def _fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _shed_tiles(n):
    h = n // 2
    return [(h - 1, h - 1), (h, h - 1), (h - 1, h), (h, h)]


def _step_towards(ux, uy, tx, ty, n):
    """One move that reduces Manhattan distance, staying on the board.

    Must return a *list*: `_apply_unit_action` bails out on anything that is not
    a list, so a bare "NORTH" string is a silent no-op that costs a whole turn.
    """
    dx, dy = tx - ux, ty - uy
    if dx == 0 and dy == 0:
        return ["PASS"]
    # Prefer the axis with the larger remaining gap to snake around obstacles.
    if abs(dx) >= abs(dy):
        if dx > 0:
            if ux + 1 < n:
                return ["EAST"]
            if uy + 1 < n:
                return ["SOUTH"]
            return ["NORTH"] if uy > 0 else ["PASS"]
        if dx < 0:
            if ux > 0:
                return ["WEST"]
            if uy + 1 < n:
                return ["SOUTH"]
            return ["NORTH"] if uy > 0 else ["PASS"]
    if dy > 0:
        if uy + 1 < n:
            return ["SOUTH"]
        if ux + 1 < n:
            return ["EAST"]
        return ["WEST"] if ux > 0 else ["PASS"]
    if dy < 0:
        if uy > 0:
            return ["NORTH"]
        if ux + 1 < n:
            return ["EAST"]
        return ["WEST"] if ux > 0 else ["PASS"]
    return ["PASS"]


# --------------------------------------------------------------------------
# Portfolio
# --------------------------------------------------------------------------

def _melon_quota(unlocked_tiles):
    """Melon is the whole season's jackpot; everything else is operating cost.

    Melon's price curve is `sq` with above_target 3.60, so total season revenue is
    a *finite* pot of roughly $24k (the integral of 250 - 0.01*x^2 down to a 42%
    floor).  Dumping it all at once instead of in tranches roughly halves it.
    ~14 tiles harvested twice (~170 units, of which ~120 clear the floor) gets
    essentially all of that pot.
    """
    if unlocked_tiles <= 0:
        return 0
    return min(14, max(4, unlocked_tiles // 2))


def _crop_pref(x, y, n, melon_quota, melon_used):
    """Ordered crop preference for one free tile.

    Returns a *list* rather than a single crop: the caller walks it and takes the
    first entry whose planting window is still open and whose seed we actually
    hold.  Returning a single crop here livelocks the whole board -- once the
    melon window closes every free tile resolves to MELON, gets skipped, and
    nothing is ever planted again.
    """
    prefs = []
    if melon_used < melon_quota:
        prefs.append("MELON")
    if (x * 7 + y * 13 + n) % 5 == 0:
        prefs.append("CARROT")
    prefs.append("WHEAT")
    return prefs


# --------------------------------------------------------------------------
# Market orders
# --------------------------------------------------------------------------

def _market_orders(obs, farm, private, day, shed_total, melon_on_board):
    market = obs.get("market") or {}
    m_inv = market.get("inventory") or {}
    shed = private.get("shed") or {}
    seeds = private.get("seeds") or {}
    money = farm.get("money", 0)
    unlocked = farm.get("unlocked_quadrants") or ["NW"]
    unlocked_tiles = 25 * len(unlocked)
    hands_today = farm.get("hires_today", 0)
    current_hands = len(farm.get("hands") or [])

    orders = []

    # --- 1. Land.  A quadrant is 25 tiles and at ~$20/tile/day that is ~$500/day
    #     of gross, so $1,000 genuinely pays back in two days.  But the purchase
    #     is paid out of the same bank that has to fund hands and seeds first, and
    #     a farm that cannot work the land it already owns is worse than one that
    #     does.  So land is only bought out of clear surplus.
    land_idx = len(unlocked) - 1
    if land_idx < len(LAND_PRICES):
        cost = LAND_PRICES[land_idx]
        if money >= cost * LAND_CASH_MULT + LAND_BUFFER:
            orders.append(["BUY_LAND"])
            money -= cost
            unlocked_tiles += 25

    # --- 2. Hire.  fib(n) ladder: 1,1,2,3,5,8,13,21,34,55,89,144,233,...
    #     Hands are the multiplier on every other mechanic, so they are bought
    #     BEFORE seeds: seeds are worthless without workers to plant them and
    #     only cost money, while a hand pays for itself inside one harvest.
    #
    #     The ladder is exponential, so an unconstrained hand count bankrupts the
    #     farm: 12 hands cost $376/day, which is most of what 50 wheat tiles
    #     earn.  Target scales with LAND (one worker per ~5 tiles) and is capped
    #     by what a fixed share of the bank can safely cover.
    hand_target = min(HAND_CAP, max(3, (unlocked_tiles + 4) // 5))
    hand_budget = money * HAND_SPEND_FRAC
    spent = 0
    while current_hands < hand_target and len(orders) < MAX_MARKET_ORDERS - 5:
        cost = _fib(hands_today)
        if spent + cost > hand_budget:
            break
        orders.append(["HIRE"])
        spent += cost
        money -= cost
        hands_today += 1

    # --- 3. Seed top-up.  Bought in bulk: seeds are consumed directly by PLANT and
    #     never pass through the shed, so a big standing buffer costs nothing to
    #     carry and guarantees every free tile always has something to plant.
    #     MELON stays capped because an $80 seed is 8x a wheat seed.
    want = {}
    if day <= PLANT_LAST_DAY["WHEAT"]:
        want["WHEAT"] = unlocked_tiles
    if day <= PLANT_LAST_DAY["CARROT"]:
        want["CARROT"] = unlocked_tiles // 5
    if (day <= PLANT_LAST_DAY["MELON"]
            and money > MELON_SEED_MIN_CASH):
        want["MELON"] = min(4, _melon_quota(unlocked_tiles))

    for crop, target in want.items():
        need = target - seeds.get(crop, 0)
        if need <= 0:
            continue
        unit = CROPS[crop]["seed"]
        n = min(need, int(max(0.0, money) // unit))
        if n > 0:
            orders.append(["BUY_SEED", crop, n])
            money -= n * unit

    # --- 4. Liquidation.  Free (no action cost) and the only way inventory
    #        becomes score.  Goods still sitting in worker inventories at
    #        end of day land in the shed, so the shed is drained every turn and
    #        the last two days drain it to zero unconditionally.
    endgame = day >= HARVEST_LAST_DAY - 1
    sell_order_items = []
    for item in PRODUCTS:
        qty = shed.get(item, 0)
        if qty <= 0:
            continue
        if endgame:
            sell_order_items.append((item, qty))
            continue
        inv = m_inv.get(item, 10000)
        n = _sell_quantity(item, inv, qty)
        if n > 0:
            sell_order_items.append((item, n))

    # Shed must never overflow: the shed is the only sink for harvested goods
    # and anything past 100 at end of day is destroyed outright.
    for item, n in sell_order_items:
        if len(orders) >= MAX_MARKET_ORDERS:
            break
        orders.append(["SELL", item, n])

    return orders


# --------------------------------------------------------------------------
# Field task planning
# --------------------------------------------------------------------------

P_WATER_NOW = 0    # unwatered and already missed a day -> dies tonight
P_HARVEST = 1      # ripe product -> realise value AND stop decay turning it to weed
P_DIG = 2          # a weed permanently blocks its tile until cleared
P_PLANT = 3        # keep the board full
P_WATER_BONUS = 4  # inside the yield window, still climbing
P_WATER_NEXT = 5   # safe for now, but must happen tomorrow
P_FEED = 6
P_GOTO_SHED = 7    # carrying goods -> walk them home


def _build_tasks(farm, private, day, seeds, melon_on_board, unlocked_tiles):
    tiles = farm["tiles"]
    n = len(tiles)
    plants = []
    melon_used = melon_on_board
    free_tiles = 0

    for y in range(n):
        row = tiles[y]
        for x in range(n):
            t = row[x]
            if t is None or t == "LOCKED":
                free_tiles += 1
                continue
            if t.get("kind") == "PLANT":
                plants.append((x, y, t))
                if t.get("crop") == "MELON":
                    melon_used += 1

    tasks = []

    # --- plants
    for (x, y, t) in plants:
        crop = t["crop"]
        cd = CROPS[crop]
        age = day - t["planted_day"]
        unwatered = not t.get("watered_today", False)
        cu = t.get("consecutive_unwatered", 0)

        if unwatered and cu >= 1:
            tasks.append((P_WATER_NOW, x, y, ["WATER"]))
            continue                      # most urgent; nothing below matters

        # Bonus window: ceil(max/2) .. max, doubled while fertilized.
        if not cd["ongoing"]:
            w0 = (cd["max"] + 1) // 2
            fert = t.get("fertilized_until_day", -1) >= day
            if unwatered and w0 <= age <= cd["max"] and t.get("yield_units", 0) < cd["maxy"]:
                tasks.append((P_WATER_BONUS, x, y, ["WATER"]))
                continue

        # Harvest rule.  For one-time crops the yield keeps climbing right up to
        # `max_yield_day` because each bonus-window WATER adds a unit, so cutting
        # at `first_yield_day` throws most of the crop away: WHEAT reaches 2 units
        # at age 2 but 4 at age 4.  Wait for the yield to stop growing.
        # Ongoing crops are different -- they fire on a fixed schedule, so take
        # the product whenever it exists.
        if t.get("yield_units", 0) > 0 and day <= HARVEST_LAST_DAY:
            if cd["ongoing"]:
                if age >= cd["first"]:
                    tasks.append((P_HARVEST, x, y, ["HARVEST"]))
                    continue
            elif age >= cd["max"] or t.get("yield_units", 0) >= cd["maxy"]:
                tasks.append((P_HARVEST, x, y, ["HARVEST"]))
                continue

        if unwatered:
            tasks.append((P_WATER_NEXT, x, y, ["WATER"]))

    # --- empty tiles: plant anything we already own seed for
    if day <= PLANT_LAST_DAY["WHEAT"]:
        melon_quota = _melon_quota(unlocked_tiles)
        for y in range(n):
            row = tiles[y]
            for x in range(n):
                if row[x] is not None:
                    continue
                for crop in _crop_pref(x, y, n, melon_quota, melon_used):
                    if day > PLANT_LAST_DAY.get(crop, 0):
                        continue
                    if seeds.get(crop, 0) <= 0:
                        continue
                    tasks.append((P_PLANT, x, y, ["PLANT", crop]))
                    if crop == "MELON":
                        melon_used += 1
                    break

    # --- animals (none in v1, but never let one die if one exists)
    for y in range(n):
        row = tiles[y]
        for x in range(n):
            t = row[x]
            if isinstance(t, dict) and t.get("animal"):
                if not t.get("fed_today", False):
                    tasks.append((P_FEED, x, y, ["FEED"]))

    # --- weeds
    for y in range(n):
        row = tiles[y]
        for x in range(n):
            if isinstance(row[x], dict) and row[x].get("kind") == "WEED":
                tasks.append((P_DIG, x, y, ["DIG"]))

    return tasks, n


def _assign(units, tasks, n, shed_tiles, inventories):
    """Greedy per-unit assignment: lowest (priority, distance) unclaimed task."""
    out = []
    claimed = set()
    shed_set = set(shed_tiles)
    for ui, (ux, uy) in enumerate(units):
        inv = inventories[ui] if ui < len(inventories) else {}
        # Banking goods is strictly better than carrying them another day.
        bank_first = bool(inv) and (ux, uy) in shed_set
        best = None
        best_key = None
        for (prio, tx, ty, op) in tasks:
            if (tx, ty) in claimed:
                continue
            d = abs(tx - ux) + abs(ty - uy)
            if d > MAX_TRAVEL:
                continue
            p = prio - 1 if (prio == P_GOTO_SHED and bank_first) else prio
            if d == 0:
                key = (p, 0)
                if best_key is None or key < best_key:
                    best_key, best = key, (tx, ty, op)
                continue
            key = (p, d)
            if best_key is None or key < best_key:
                best_key, best = key, (tx, ty, op)
        if best is None:
            # Nothing to do. If carrying goods, walk toward the nearest shed tile.
            if inv:
                tx, ty = min(shed_tiles, key=lambda s: abs(s[0] - ux) + abs(s[1] - uy))
                out.append(_step_towards(ux, uy, tx, ty, n))
                continue
            out.append(["PASS"])
            continue
        tx, ty, op = best
        claimed.add((tx, ty))
        if (tx, ty) == (ux, uy):
            act = list(op)
            if act[0] == "FEED" and inv.get("WHEAT", 0) <= 0:
                # No wheat in hand: the FEED would silently no-op. Go get some.
                tx, ty = min(shed_tiles, key=lambda s: abs(s[0] - ux) + abs(s[1] - uy))
                out.append(_step_towards(ux, uy, tx, ty, n))
                continue
            out.append(act)
            continue
        out.append(_step_towards(ux, uy, tx, ty, n))
    return out


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def _agent(obs):
    farms = obs.get("farms") or []
    player = obs.get("player", 0)
    if not farms or player >= len(farms):
        return {"farmer": ["PASS"], "hands": [], "market": []}
    farm = farms[player]
    private = obs.get("private") or {}
    day = obs.get("day", 0)
    tiles = farm.get("tiles") or []
    if not tiles:
        return {"farmer": ["PASS"], "hands": [], "market": []}
    n = len(tiles)
    shed = private.get("shed") or {}
    seeds = private.get("seeds") or {}
    inventories = private.get("inventories") or [{}]

    shed_total = 0
    for v in shed.values():
        if isinstance(v, int) and v > 0:
            shed_total += v

    # Count melon already planted so the portfolio quota is respected.
    melon_on_board = 0
    for row in tiles:
        for t in row:
            if isinstance(t, dict) and t.get("kind") == "PLANT" and t.get("crop") == "MELON":
                melon_on_board += 1

    unlocked_tiles = 25 * len(farm.get("unlocked_quadrants") or ["NW"])
    orders = _market_orders(obs, farm, private, day, shed_total, melon_on_board)

    tasks, n = _build_tasks(farm, private, day, seeds, melon_on_board, unlocked_tiles)
    shed_tiles = _shed_tiles(n)

    units = [tuple(farm["farmer"])]
    for p in (farm.get("hands") or []):
        units.append((p[0], p[1]))

    acts = _assign(units, tasks, n, shed_tiles, inventories)

    return {
        "farmer": acts[0] if acts else ["PASS"],
        "hands": [acts[i] if i < len(acts) else ["PASS"] for i in range(1, len(units))],
        "market": orders[:MAX_MARKET_ORDERS],
    }


VALID_UNIT_OPS = {
    "NORTH", "SOUTH", "EAST", "WEST", "PASS", "PICKUP", "PLACE", "DROP",
    "PLANT", "WATER", "HARVEST", "FERTILIZE", "BUILD_COOP", "BUILD_PASTURE",
    "FEED", "COLLECT_FERTILIZER", "CARE", "DIG",
}
VALID_MARKET_OPS = {"BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL", "SELL", "HIRE", "BUY_LAND"}


def _valid_unit(a):
    return (isinstance(a, list) and len(a) >= 1 and isinstance(a[0], str)
            and a[0] in VALID_UNIT_OPS)


def _valid_order(o):
    return (isinstance(o, list) and len(o) >= 1 and isinstance(o[0], str)
            and o[0] in VALID_MARKET_OPS)


def _sanitize(out, n_hands):
    """Last line of defence.

    The environment treats any malformed action as a *silent* no-op, so a
    malformed action costs a turn and produces no error.  Sanitising here means
    a bug can never silently degrade a submitted run -- worst case we lose one
    turn instead of the whole episode.
    """
    out["farmer"] = out["farmer"] if _valid_unit(out.get("farmer")) else ["PASS"]
    hands = out.get("hands")
    if not isinstance(hands, list):
        hands = []
    hands = [h if _valid_unit(h) else ["PASS"] for h in hands]
    if len(hands) > n_hands:
        hands = hands[:n_hands]
    while len(hands) < n_hands:
        hands.append(["PASS"])
    out["hands"] = hands
    mkt = out.get("market")
    if not isinstance(mkt, list):
        mkt = []
    out["market"] = [o for o in mkt if _valid_order(o)][:MAX_MARKET_ORDERS]
    return out


def agent(obs):
    try:
        farms = obs.get("farms") or []
        player = obs.get("player", 0)
        n_hands = 0
        if farms and player < len(farms):
            n_hands = len(farms[player].get("hands") or [])
        return _sanitize(_agent(obs), n_hands)
    except Exception:
        return {"farmer": ["PASS"], "hands": [], "market": []}