# %% [markdown]
# # FarmBench: can a language model run a farm?
#
# Fifteen economic decisions from **Kaggriculture** (Kaggle's two-player farming economy: finite product pools,
# price curves, a town that refills demand, Fibonacci-priced labour, $1k/$2k/$4k land). Each task shows the model
# a real game state and asks for one structured decision. **The grader is the game engine, not a judge**:
#
# * *Exact tasks* are scored in this notebook with the engine's own price function and its per-unit lockstep
#   market loop; the optimum is found by brute force / dynamic programming.
# * *Simulation tasks* offer a small menu of strategies. Every menu arm was played offline by the engine
#   (our knob-driven policy bot vs. a strong public bot, several towns, both seats); the mean final coins per arm
#   are embedded below, so the Kaggle run only needs the LLM call plus a lookup.
#
# Score per task = share of the available gain captured: `clip((value(choice) - value(naive)) / (value(best) - value(naive)), 0, 1)`.
# Two sanity tasks (unambiguous rules arithmetic) score 0 / 0.5 / 1. The benchmark score is the mean over tasks.
# Rationales are also scanned for three ideas (pool saturation, the SE-quadrant trap, Fibonacci hand cost); these
# flags are reported, not scored. Engine constants (`MARKET_PARAMS`, `market_price`) are copied from
# `kaggle_environments.envs.kaggriculture` (Apache-2.0, Kaggle Inc.).

# %%
import dataclasses
import functools
import json
import math
import os
import re

import pandas as pd

import kaggle_benchmarks as kbench

# %% [markdown]
# ## 1. The engine's market, verbatim

# %%
MARKET_I0 = 10000
PRICE_FLOOR = 1
MARKET_PARAMS = {
    "WHEAT":      {"base":  25, "I0": MARKET_I0, "T": 400, "below_func": "sqrt",   "below_target": 0.80, "above_func": "log",    "above_target": 0.20},
    "CARROT":     {"base":  35, "I0": MARKET_I0, "T": 450, "below_func": "hinge",  "below_target": 1.00, "above_func": "sqrt",   "above_target": 0.70},
    "TOMATO":     {"base":  60, "I0": MARKET_I0, "T": 200, "below_func": "hinge",  "below_target": 0.40, "above_func": "sqrt",   "above_target": 0.60},
    "STRAWBERRY": {"base": 120, "I0": MARKET_I0, "T": 100, "below_func": "sqrt",   "below_target": 0.70, "above_func": "linear", "above_target": 1.60},
    "MELON":      {"base": 250, "I0": MARKET_I0, "T": 300, "below_func": "log",    "below_target": 0.20, "above_func": "sq",     "above_target": 3.60},
    "EGG":        {"base":  50, "I0": MARKET_I0, "T": 332, "below_func": "hinge",  "below_target": 0.40, "above_func": "log",    "above_target": 0.20},
    "MILK":       {"base": 160, "I0": MARKET_I0, "T": 122, "below_func": "sqrt",   "below_target": 0.60, "above_func": "linear", "above_target": 1.60},
    "WOOL":       {"base": 200, "I0": MARKET_I0, "T": 105, "below_func": "log",    "below_target": 0.20, "above_func": "sq",     "above_target": 3.20},
    "FERTILIZER": {"base": 100, "I0": MARKET_I0, "T": 200, "below_func": "linear", "below_target": 0.40, "above_func": "linear", "above_target": 0.40},
}
HINGE_GAIN = 8.0
SHOPS = {"BAKERY": ["EGG", "WHEAT"], "PIZZA_SHOP": ["MILK", "TOMATO", "WHEAT"], "BRUNCH_SPOT": ["EGG", "WHEAT", "STRAWBERRY"],
         "YARN_STORE": ["WOOL"], "ICE_CREAM_SHOP": ["STRAWBERRY", "MILK", "WHEAT"], "PET_CAFE": ["CARROT"],
         "SMOOTHIE_SHOP": ["STRAWBERRY", "MILK"], "FARMERS_MARKET": ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY"]}
PRODUCTS = list(MARKET_PARAMS)


def _shape(func, x, T=None):
    x = max(0.0, x)
    if func == "linear": return x
    if func == "sq":     return x * x
    if func == "sqrt":   return math.sqrt(x)
    if func == "log":    return math.log(1.0 + x)
    if func == "log10":  return math.log10(1.0 + x)
    if func == "hinge":
        if not T or T <= 0:
            return x
        u = x / T
        return u + HINGE_GAIN * max(0.0, u - 1.0) ** 2
    return x


def market_price(item, inventory):
    """Engine price for `item` at market inventory `inventory` (verbatim from kaggriculture.py)."""
    p = MARKET_PARAMS[item]
    base, I0, T = p["base"], p["I0"], p["T"]
    if inventory < I0:
        f = p["below_func"]
        amp = p["below_target"] * base / _shape(f, T, T)
        price = base + amp * _shape(f, I0 - inventory, T)
    else:
        f = p["above_func"]
        amp = p["above_target"] * base / _shape(f, T, T)
        price = base - amp * _shape(f, inventory - I0, T)
    return max(PRICE_FLOOR, int(round(price)))


def sell_run(item, inv, n):
    """One player sells n units in one hour: each unit is quoted at the current inventory, then adds 1 to it
    (units sold at the $1 floor do not). Mirrors _process_market/_commit_unit for a single seller."""
    rev = 0
    for _ in range(n):
        p = market_price(item, inv)
        rev += p
        if p > 1:
            inv += 1
    return rev, inv


def lockstep_sell(item, inv, mine, theirs):
    """Both players sell in the same hour. Per round both are quoted the same pre-commit price, then both units
    commit (inventory +2). Returns (my revenue, their revenue, inventory after)."""
    rev_me = rev_them = 0
    while mine > 0 or theirs > 0:
        p = market_price(item, inv)
        if mine > 0:
            rev_me += p; mine -= 1
            if p > 1: inv += 1
        if theirs > 0:
            rev_them += p; theirs -= 1
            if p > 1: inv += 1
    return rev_me, rev_them, inv


def schedule_value(item, inv0, sales, drains):
    """Sell sales[i] units at the start of period i, then the town drains drains[i] units. Returns revenue."""
    inv, rev = inv0, 0
    for q, d in zip(sales, drains):
        r, inv = sell_run(item, inv, q)
        rev += r
        inv -= d
    return rev


def best_schedule(item, inv0, units, drains):
    """Exact optimum of schedule_value over all schedules selling at most `units` (DP over period, units left, inventory)."""
    n = len(drains)

    @functools.lru_cache(maxsize=None)
    def go(i, left, inv):
        if i == n or left == 0:
            return 0, ()
        best_v, best_plan = -1, None
        rev, cur = 0, inv
        for q in range(0, left + 1):
            if q > 0:
                p = market_price(item, cur)
                rev += p
                if p > 1: cur += 1
            v, plan = go(i + 1, left - q, cur - drains[i])
            if rev + v > best_v:
                best_v, best_plan = rev + v, (q,) + plan
        return best_v, best_plan

    v, plan = go(0, units, inv0)
    return v, list(plan) + [0] * (n - len(plan))


def units_to_floor(item):
    """Units sold above I0 (single seller, no refill) before the price reaches $1; None if it never does within 5000."""
    inv = MARKET_I0
    for k in range(1, 5001):
        if market_price(item, inv + k) <= 1:
            return k
    return None


def daily_drain(item, shops):
    """Units the town removes per day: 1 (town centre, not fertilizer) + 6 per shop that buys it (12 if single-product)."""
    d = 0 if item == "FERTILIZER" else 1
    for s in shops:
        if item in SHOPS[s]:
            d += 12 if len(SHOPS[s]) == 1 else 6
    return d

# %% [markdown]
# ## 2. The rules digest every task starts with (numbers generated from the engine function above)

# %%
def _price_table_text():
    rows = []
    for item in PRODUCTS:
        p = MARKET_PARAMS[item]
        k = units_to_floor(item)
        glut = f"$1 after {k} units" if k else f"never $1 (${market_price(item, MARKET_I0 + 800)} after 800 units)"
        rows.append(f"{item} base ${p['base']}: glut side {p['above_func']}, {glut}; scarcity side {p['below_func']}, "
                    f"${market_price(item, MARKET_I0 - p['T'])} at I0-{p['T']}")
    return "\n".join("  - " + r for r in rows)


RULES = f"""KAGGRICULTURE IN BRIEF (these are the real engine's rules; the grader applies them exactly)
- Two farmers share ONE market for 30 days x 24 hours. Winner = most cash at the end of day 29. You start with $3,000.
- Each unit (the farmer or a hired hand) does one action per hour: move one tile, plant, water, harvest, feed, build, pick up / drop at the shed.
- Land: you start with one 5x5 quadrant (NW, 25 tiles). Extra quadrants cost $1,000, then $2,000, then $4,000 (NE, SW, SE in that order).
- Hands are hired per day and vanish at night. The n-th hire of a day costs fib(n) dollars: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233 ... (resets every day).
- One-time crops (seed cost / units at harvest with daily watering / days from planting to harvest): WHEAT $10 / 4 / 4; CARROT $20 / 3 / 3; MELON $80 / 6 / 10.
  They start at 1 unit and gain +1 per watered day inside their bonus window (WHEAT ages 2-4, CARROT ages 2-3, MELON ages 6-12); fertilizer ($100 at base, or collected from animals) makes it +2 per watered day for 3 days (the day applied and the next two). Caps: WHEAT 6, CARROT 4, MELON 6. Harvest removes the plant.
- Ongoing crops: TOMATO $50 makes 1 unit per day on days 8-11 after planting (4 units total); STRAWBERRY $100 makes 1 unit on days 10, 12, 14, 16 after planting. Then the plant decays.
- Any plant not watered on two consecutive days becomes a weed.
- Animals (cost; a coop or pasture must be built first): GOOSE $300 gives 1 EGG per day from day 4 after placing; COW $400 gives 1 MILK every 2 days from day 8; SHEEP $500 gives 1 WOOL every 3 days from day 6. Every animal eats 1 WHEAT per day; an animal unfed on two consecutive days escapes for good. Daily CARE banks +1 unit onto the next production.
- Market: seeds and animals have fixed prices. Product SELL prices move with the market's inventory of that product. Every unit sold adds 1 to that inventory and lowers the price; the town removes units and raises it. Price = base at the neutral inventory I0; floored at $1; units sold at $1 do not add to the inventory. Only WHEAT and FERTILIZER can be bought back.
- Both players' market orders are matched one unit at a time in lockstep: if both sell 10 melons in the same hour, the units alternate and both ride the same falling curve.
- Town demand: the town centre removes 1 unit of every product per day. A new shop opens every 3 days (day 3, 6, ..., 24; drawn at random WITH replacement, so duplicates happen). Each shop removes 1 unit of every product it buys every 4 hours (6 per day); single-product shops remove 2 at a time (12 per day). BAKERY: egg, wheat. PIZZA_SHOP: milk, tomato, wheat. BRUNCH_SPOT: egg, wheat, strawberry. YARN_STORE: wool x2. ICE_CREAM_SHOP: strawberry, milk, wheat. PET_CAFE: carrot x2. SMOOTHIE_SHOP: strawberry, milk. FARMERS_MARKET: wheat, carrot, tomato, strawberry. Nothing except the town centre ever buys MELON.
- Price curves (single seller, no refill):
{_price_table_text()}
- The shed holds 100 items (seeds excluded); anything beyond that is lost."""

# %% [markdown]
# ## 3. Offline simulation tables (built by `build_tables.py`; see README)

# %%
# --- BEGIN TABLES
TABLES = json.loads(r'''{"opening":{"day":0,"seeds":[9300,9301,9303,9305,9310,9316],"naive":"cautious","best":"goose_farm","arms":{"meta_a":{"n":12,"coins":64656,"margin":-17607,"wins":0},"default":{"n":12,"coins":68484,"margin":-14188,"wins":2},"melon_max":{"n":12,"coins":61911,"margin":-45870,"wins":0},"goose_farm":{"n":12,"coins":72419,"margin":-13403,"wins":2},"cautious":{"n":12,"coins":67713,"margin":-11066,"wins":2},"strawberry_rush":{"n":12,"coins":55700,"margin":-43224,"wins":0},"land_first":{"n":12,"coins":70239,"margin":-20976,"wins":0},"cows_only":{"n":12,"coins":57681,"margin":-20061,"wins":0}}},"sheep_yarn":{"day":6,"seeds":[9301,9308,9309,9312],"naive":"sheep_0","best":"sheep_8","arms":{"sheep_0":{"n":8,"coins":74725,"margin":-56260,"wins":0},"sheep_2":{"n":8,"coins":83475,"margin":-48409,"wins":0},"sheep_4":{"n":8,"coins":91866,"margin":-38613,"wins":0},"sheep_6":{"n":8,"coins":95134,"margin":-32388,"wins":0},"sheep_8":{"n":8,"coins":96818,"margin":-25631,"wins":0}}},"sheep_no_yarn":{"day":6,"seeds":[9300,9304,9305,9307],"naive":"sheep_0","best":"sheep_0","arms":{"sheep_0":{"n":8,"coins":95277,"margin":-5602,"wins":2},"sheep_2":{"n":8,"coins":91124,"margin":-8589,"wins":0},"sheep_4":{"n":8,"coins":91446,"margin":-7481,"wins":2},"sheep_6":{"n":8,"coins":86632,"margin":-12614,"wins":0},"sheep_8":{"n":8,"coins":84478,"margin":-14718,"wins":0}}},"se_quadrant":{"day":12,"seeds":[9300,9301,9303,9305,9310,9316],"naive":"never","best":"never","arms":{"never":{"n":12,"coins":68484,"margin":-14188,"wins":2},"buy_day12":{"n":12,"coins":67140,"margin":-15359,"wins":2},"buy_day16":{"n":12,"coins":66658,"margin":-16963,"wins":2},"buy_day20":{"n":12,"coins":66141,"margin":-16372,"wins":2}}},"land_ne_timing":{"day":2,"seeds":[9300,9301,9303,9305,9310,9316],"naive":"never","best":"day10","arms":{"day2":{"n":12,"coins":68044,"margin":-13370,"wins":2},"day4":{"n":12,"coins":68044,"margin":-13370,"wins":2},"day6":{"n":12,"coins":68453,"margin":-14399,"wins":2},"day8":{"n":12,"coins":67162,"margin":-17043,"wins":2},"day10":{"n":12,"coins":68484,"margin":-14188,"wins":2},"never":{"n":12,"coins":50455,"margin":-50631,"wins":0},"default":{"n":12,"coins":68484,"margin":-14188,"wins":2}}},"max_hands":{"day":0,"seeds":[9300,9301,9303,9305,9310,9316],"naive":"hands_2","best":"hands_12","arms":{"hands_2":{"n":12,"coins":33539,"margin":-85518,"wins":0},"hands_4":{"n":12,"coins":44925,"margin":-63324,"wins":0},"hands_6":{"n":12,"coins":58716,"margin":-41488,"wins":0},"hands_8":{"n":12,"coins":64684,"margin":-27414,"wins":0},"hands_10":{"n":12,"coins":67974,"margin":-15406,"wins":2},"hands_12":{"n":12,"coins":68484,"margin":-14188,"wins":2},"hands_14":{"n":12,"coins":61972,"margin":-20184,"wins":2}}},"terminal_tomato":{"day":16,"seeds":[9300,9310,9316,9318],"naive":"off","best":"plant_day18","arms":{"plant_day16":{"n":8,"coins":66415,"margin":-14719,"wins":2},"plant_day18":{"n":8,"coins":66669,"margin":-14369,"wins":2},"plant_day20":{"n":8,"coins":59850,"margin":-22002,"wins":0},"plant_day22":{"n":8,"coins":59199,"margin":-22391,"wins":0},"off":{"n":8,"coins":61225,"margin":-20345,"wins":0}}},"terminal_carrot":{"day":24,"seeds":[9300,9301,9302,9305],"naive":"off","best":"plant_day24","arms":{"plant_day24":{"n":8,"coins":75010,"margin":-12797,"wins":2},"plant_day25":{"n":8,"coins":74848,"margin":-13078,"wins":2},"plant_day26":{"n":8,"coins":74051,"margin":-13983,"wins":2},"plant_day27":{"n":8,"coins":73341,"margin":-14897,"wins":2},"off":{"n":8,"coins":74277,"margin":-13977,"wins":2}}}}''')
# --- END TABLES
STATES = json.loads(r'''{"land_ne_timing":{"seed":9300,"text":"Day 2, hour 0 of 24 (28 days including today remain). Cash $36.\nYour land: NW (25 tiles, 1 empty). Hands hired today: 0.\nTown shops open: none yet.\nMarket prices: WHEAT $30, CARROT $35, TOMATO $60, STRAWBERRY $132, MELON $260, EGG $50, MILK $172, WOOL $209, FERTILIZER $99.\nMarket inventory relative to neutral I0 (negative = scarce, positive = glut): WHEAT -21, CARROT -2, TOMATO -2, STRAWBERRY -2, MELON -2, EGG -2, MILK -2, WOOL -2, FERTILIZER +3.\nYour farm: 14 MELON (age 2), 6 WHEAT (age 2), 4 COW. Shed: FERTILIZER 4. Seeds in hand: none.\nOpponent's visible farm: 12 MELON (age 2), 7 WHEAT (age 2), 2 COW, 2 SHEEP, 2 empty PASTURE; land NW; cash $62; hands today 0."},"max_hands":{"seed":9300,"text":"Day 0, hour 0 of 24 (30 days including today remain). Cash $3,000.\nYour land: NW (25 tiles, 25 empty). Hands hired today: 0.\nTown shops open: none yet.\nMarket prices: WHEAT $25, CARROT $35, TOMATO $60, STRAWBERRY $120, MELON $250, EGG $50, MILK $160, WOOL $200, FERTILIZER $100.\nMarket inventory relative to neutral I0 (negative = scarce, positive = glut): all at I0.\nYour farm: empty. Shed: empty. Seeds in hand: none.\nOpponent's visible farm: empty; land NW; cash $3,000; hands today 0."},"opening":{"seed":9300,"text":"Day 0, hour 0 of 24 (30 days including today remain). Cash $3,000.\nYour land: NW (25 tiles, 25 empty). Hands hired today: 0.\nTown shops open: none yet.\nMarket prices: WHEAT $25, CARROT $35, TOMATO $60, STRAWBERRY $120, MELON $250, EGG $50, MILK $160, WOOL $200, FERTILIZER $100.\nMarket inventory relative to neutral I0 (negative = scarce, positive = glut): all at I0.\nYour farm: empty. Shed: empty. Seeds in hand: none.\nOpponent's visible farm: empty; land NW; cash $3,000; hands today 0."},"se_quadrant":{"seed":9300,"text":"Day 12, hour 0 of 24 (18 days including today remain). Cash $11,573.\nYour land: NW, NE, SW (75 tiles, 4 empty). Hands hired today: 0.\nTown shops open: FARMERS_MARKET (buys WHEAT/CARROT/TOMATO/STRAWBERRY), FARMERS_MARKET (buys WHEAT/CARROT/TOMATO/STRAWBERRY), BRUNCH_SPOT (buys EGG/WHEAT/STRAWBERRY), PIZZA_SHOP (buys MILK/TOMATO/WHEAT).\nMarket prices: WHEAT $41, CARROT $43, TOMATO $72, STRAWBERRY $212, MELON $43, EGG $52, MILK $47, WOOL $196, FERTILIZER $77.\nMarket inventory relative to neutral I0 (negative = scarce, positive = glut): WHEAT -250, CARROT -102, TOMATO -102, STRAWBERRY -120, MELON +144, EGG -30, MILK +54, WOOL +8, FERTILIZER +113.\nYour farm: 12 STRAWBERRY (age 1), 7 STRAWBERRY (age 2), 2 STRAWBERRY (age 3), 16 STRAWBERRY (age 4), 3 STRAWBERRY (age 7), 3 STRAWBERRY (age 8), 1 STRAWBERRY (age 9), 13 WHEAT (age 1), 2 WHEAT (age 3), 2 WHEAT (age 4), 4 COW, 4 GOOSE, 2 SHEEP. Shed: WHEAT 2, FERTILIZER 12. Seeds in hand: WHEAT 4.\nOpponent's visible farm: 13 STRAWBERRY (age 1), 4 STRAWBERRY (age 4), 4 STRAWBERRY (age 5), 8 STRAWBERRY (age 6), 4 STRAWBERRY (age 7), 11 WHEAT (age 1), 7 WHEAT (age 2), 2 WHEAT (age 3), 6 COW, 5 GOOSE, 6 SHEEP, 1 empty COOP; land NW, NE, SW; cash $11,343; hands today 0."},"sheep_no_yarn":{"seed":9300,"text":"Day 6, hour 0 of 24 (24 days including today remain). Cash $1,002.\nYour land: NW (25 tiles, 0 empty). Hands hired today: 0.\nTown shops open: FARMERS_MARKET (buys WHEAT/CARROT/TOMATO/STRAWBERRY), FARMERS_MARKET (buys WHEAT/CARROT/TOMATO/STRAWBERRY).\nMarket prices: WHEAT $31, CARROT $37, TOMATO $63, STRAWBERRY $161, MELON $267, EGG $50, MILK $181, WOOL $217, FERTILIZER $92.\nMarket inventory relative to neutral I0 (negative = scarce, positive = glut): WHEAT -35, CARROT -24, TOMATO -24, STRAWBERRY -24, MELON -6, EGG -6, MILK -6, WOOL -6, FERTILIZER +40.\nYour farm: 14 MELON (age 6), 3 STRAWBERRY (age 1), 3 STRAWBERRY (age 2), 1 STRAWBERRY (age 3), 4 COW. Shed: WHEAT 2, FERTILIZER 4. Seeds in hand: none.\nOpponent's visible farm: 12 MELON (age 6), 4 STRAWBERRY (age 1), 3 WHEAT (age 2), 4 COW, 2 SHEEP; land NW; cash $231; hands today 0."},"sheep_yarn":{"seed":9301,"text":"Day 6, hour 0 of 24 (24 days including today remain). Cash $1,002.\nYour land: NW (25 tiles, 0 empty). Hands hired today: 0.\nTown shops open: ICE_CREAM_SHOP (buys STRAWBERRY/MILK/WHEAT), YARN_STORE (buys WOOL x2).\nMarket prices: WHEAT $31, CARROT $35, TOMATO $61, STRAWBERRY $161, MELON $267, EGG $50, MILK $203, WOOL $217, FERTILIZER $92.\nMarket inventory relative to neutral I0 (negative = scarce, positive = glut): WHEAT -35, CARROT -6, TOMATO -6, STRAWBERRY -24, MELON -6, EGG -6, MILK -24, WOOL -6, FERTILIZER +40.\nYour farm: 14 MELON (age 6), 3 STRAWBERRY (age 1), 3 STRAWBERRY (age 2), 1 STRAWBERRY (age 3), 4 COW. Shed: WHEAT 2, FERTILIZER 4. Seeds in hand: none.\nOpponent's visible farm: 12 MELON (age 6), 4 STRAWBERRY (age 1), 3 WHEAT (age 2), 4 COW, 2 SHEEP; land NW; cash $231; hands today 0."},"terminal_carrot":{"seed":9300,"text":"Day 24, hour 0 of 24 (6 days including today remain). Cash $54,712.\nYour land: NW, NE, SW (75 tiles, 1 empty). Hands hired today: 0.\nTown shops open: FARMERS_MARKET (buys WHEAT/CARROT/TOMATO/STRAWBERRY), FARMERS_MARKET (buys WHEAT/CARROT/TOMATO/STRAWBERRY), BRUNCH_SPOT (buys EGG/WHEAT/STRAWBERRY), PIZZA_SHOP (buys MILK/TOMATO/WHEAT), PET_CAFE (buys CARROT x2), PIZZA_SHOP (buys MILK/TOMATO/WHEAT), BRUNCH_SPOT (buys EGG/WHEAT/STRAWBERRY), BRUNCH_SPOT (buys EGG/WHEAT/STRAWBERRY).\nMarket prices: WHEAT $47, CARROT $63, TOMATO $236, STRAWBERRY $55, MELON $76, EGG $44, MILK $15, WOOL $5, FERTILIZER $45.\nMarket inventory relative to neutral I0 (negative = scarce, positive = glut): WHEAT -467, CARROT -366, TOMATO -366, STRAWBERRY +34, MELON +132, EGG +35, MILK +69, WOOL +58, FERTILIZER +276.\nYour farm: 12 STRAWBERRY (age 13), 7 STRAWBERRY (age 14), 2 STRAWBERRY (age 15), 16 STRAWBERRY (age 16), 4 TOMATO (age 7), 6 TOMATO (age 8), 8 WHEAT (age 1), 5 WHEAT (age 2), 3 WHEAT (age 3), 1 WHEAT (age 5), 4 COW, 4 GOOSE, 2 SHEEP. Shed: WHEAT 35, STRAWBERRY 23, EGG 2, WOOL 23, FERTILIZER 12. Seeds in hand: WHEAT 1.\nOpponent's visible farm: 13 STRAWBERRY (age 13), 4 STRAWBERRY (age 16), 4 STRAWBERRY (age 17), 14 WHEAT (age 1), 10 WHEAT (age 2), 6 WHEAT (age 3), 7 WHEAT (age 4), 6 COW, 5 GOOSE, 6 SHEEP; land NW, NE, SW; cash $65,344; hands today 0."},"terminal_tomato":{"seed":9300,"text":"Day 16, hour 0 of 24 (14 days including today remain). Cash $16,353.\nYour land: NW, NE, SW (75 tiles, 3 empty). Hands hired today: 0.\nTown shops open: FARMERS_MARKET (buys WHEAT/CARROT/TOMATO/STRAWBERRY), FARMERS_MARKET (buys WHEAT/CARROT/TOMATO/STRAWBERRY), BRUNCH_SPOT (buys EGG/WHEAT/STRAWBERRY), PIZZA_SHOP (buys MILK/TOMATO/WHEAT), PET_CAFE (buys CARROT x2).\nMarket prices: WHEAT $43, CARROT $48, TOMATO $81, STRAWBERRY $235, MELON $54, EGG $52, MILK $3, WOOL $61, FERTILIZER $63.\nMarket inventory relative to neutral I0 (negative = scarce, positive = glut): WHEAT -315, CARROT -166, TOMATO -178, STRAWBERRY -188, MELON +140, EGG -29, MILK +75, WOOL +49, FERTILIZER +185.\nYour farm: 12 STRAWBERRY (age 5), 7 STRAWBERRY (age 6), 2 STRAWBERRY (age 7), 16 STRAWBERRY (age 8), 3 STRAWBERRY (age 11), 3 STRAWBERRY (age 12), 1 STRAWBERRY (age 13), 9 WHEAT (age 1), 2 WHEAT (age 2), 6 WHEAT (age 4), 1 WHEAT (age 5), 4 COW, 4 GOOSE, 2 SHEEP. Shed: WHEAT 39, STRAWBERRY 8, EGG 6, FERTILIZER 10. Seeds in hand: WHEAT 3.\nOpponent's visible farm: 13 STRAWBERRY (age 5), 4 STRAWBERRY (age 8), 4 STRAWBERRY (age 9), 8 STRAWBERRY (age 10), 4 STRAWBERRY (age 11), 8 WHEAT (age 1), 7 WHEAT (age 2), 6 WHEAT (age 3), 4 WHEAT (age 4), 6 COW, 5 GOOSE, 6 SHEEP; land NW, NE, SW; cash $21,924; hands today 0."}}''')
# --- END STATES

# %% [markdown]
# ## 4. Task specifications
#
# Each spec has: `state` (the situation shown to the model), `question`, a dataclass `schema`, and `grade(decision)`
# returning `value / naive / best / score` (+ details). `snap` maps a free-form number onto the nearest simulated arm.

# %%
FLAG_PATTERNS = {
    "pool": r"(?i)(pool|saturat|glut|crash|floor|\$1\b|inventory|oversuppl|flood)",
    "se_trap": r"(?i)(\bSE\b|south-?east|fourth quadrant|4,?000)",
    "fibonacci": r"(?i)(fib|escalat|each (extra|additional) hand|144|\b89\b|\b55\b|grows? (fast|quickly))",
    "refill": r"(?i)(refill|recover|replenish|per day|consum|drain|demand)",
}


def clip01(x):
    return max(0.0, min(1.0, float(x)))


def gain_score(value, naive, best):
    if best <= naive:
        return 1.0 if value >= best else 0.0
    return clip01((value - naive) / (best - naive))


def snap(x, arms):
    return min(arms, key=lambda a: (abs(a - x), a))


def sim_arm_value(task, arm):
    return TABLES[task]["arms"][arm]["coins"]


def sim_grade(task, arm):
    t = TABLES[task]
    naive, best = t["arms"][t["naive"]]["coins"], t["arms"][t["best"]]["coins"]
    v = sim_arm_value(task, arm)
    return dict(arm=arm, value=v, naive=naive, best=best, best_arm=t["best"], score=gain_score(v, naive, best),
                margin=t["arms"][arm]["margin"], n_games=t["arms"][arm]["n"])


def sim_menu_text(task, labels):
    t = TABLES.get(task, {})
    return "\n".join(f"  - {arm}: {labels[arm]}" for arm in labels if arm in t.get("arms", {}) or not t)


# ---------------------------------------------------------------------------------------------- schemas
@dataclasses.dataclass
class HireDecision:
    hire_more: int
    extra_cost: int
    rationale: str


@dataclasses.dataclass
class FeedDecision:
    feed: list[str]
    rationale: str


@dataclasses.dataclass
class FertilizerAnswer:
    units_with_fertilizer: int
    units_without_fertilizer: int
    age_first_full_with_fertilizer: int
    rationale: str


@dataclasses.dataclass
class SellNow:
    sell_now: int
    rationale: str


@dataclasses.dataclass
class HarvestDay:
    harvest_day: int
    rationale: str


@dataclasses.dataclass
class ThreeDayPlan:
    day27: int
    day28: int
    day29: int
    rationale: str


@dataclasses.dataclass
class CropChoice:
    crop: str
    rationale: str


@dataclasses.dataclass
class HourlyPlan:
    units_per_hour: list[int]
    rationale: str


@dataclasses.dataclass
class OptionChoice:
    option: str
    rationale: str


@dataclasses.dataclass
class IntChoice:
    value: int
    rationale: str


# ---------------------------------------------------------------------------------------------- exact tasks
MELON_DUMP = dict(units=72, opp_units=72)


def grade_melon_dump(d):
    n = int(max(0, min(72, d.sell_now)))

    def value(k):
        rev_now, _, inv = lockstep_sell("MELON", MARKET_I0, k, MELON_DUMP["opp_units"])
        rev_later, _ = sell_run("MELON", inv - 1, 72 - k)   # town centre removes 1 melon overnight
        return rev_now + rev_later

    vals = {k: value(k) for k in range(0, 73)}
    best_k = max(vals, key=lambda k: (vals[k], k))
    return dict(choice=n, value=vals[n], naive=vals[0], best=vals[best_k], best_choice=best_k,
                score=gain_score(vals[n], vals[0], vals[best_k]))


def grade_melon_race(d):
    day9 = sell_run("MELON", MARKET_I0, 12 * 5)[0]                      # 5 units per plant at age 9, sold alone
    day10 = lockstep_sell("MELON", MARKET_I0 - 1, 12 * 6, 72)[0]         # 6 units at age 10, in lockstep with 72
    vals = {9: day9, 10: day10}
    h = 9 if int(d.harvest_day) <= 9 else 10
    return dict(choice=h, value=vals[h], naive=vals[10], best=max(vals.values()), best_choice=max(vals, key=vals.get),
                score=gain_score(vals[h], vals[10], max(vals.values())), detail=vals)


WOOL = dict(units=30, inv0=MARKET_I0 + 40, shops=["YARN_STORE"])


def grade_wool_lot(d):
    plan = [int(max(0, x)) for x in (d.day27, d.day28, d.day29)]
    tot = sum(plan)
    if tot > WOOL["units"]:                       # cannot sell what you do not have: trim from the end
        over = tot - WOOL["units"]
        for i in (2, 1, 0):
            cut = min(over, plan[i]); plan[i] -= cut; over -= cut
    drains = [daily_drain("WOOL", WOOL["shops"])] * 3
    v = schedule_value("WOOL", WOOL["inv0"], plan, drains)
    naive = schedule_value("WOOL", WOOL["inv0"], [WOOL["units"], 0, 0], drains)
    best, best_plan = best_schedule("WOOL", WOOL["inv0"], WOOL["units"], drains)
    return dict(choice=plan, value=v, naive=naive, best=best, best_choice=best_plan, score=gain_score(v, naive, best))


def lockstep_schedule_value(item, inv0, mine, theirs, drains):
    """Per period: my mine[i] units and the opponent's theirs[i] units are matched in lockstep, then the town drains."""
    inv, rev = inv0, 0
    for q, s, d in zip(mine, theirs, drains):
        r, _, inv = lockstep_sell(item, inv, q, s)
        rev += r
        inv -= d
    return rev


def best_lockstep_schedule(item, inv0, units, theirs, drains):
    """Exact optimum of lockstep_schedule_value over my schedules (DP over period, units left, inventory)."""
    n = len(drains)

    @functools.lru_cache(maxsize=None)
    def tail(inv, m):                       # inventory after the opponent sells m units alone from inv
        for _ in range(m):
            if market_price(item, inv) > 1: inv += 1
        return inv

    @functools.lru_cache(maxsize=None)
    def go(i, left, inv):
        if i == n:
            return 0, ()
        s = theirs[i]
        best_v, best_plan = -1, None
        rev, cur, k = 0, inv, 0             # state after k lockstep rounds in which I sold
        for q in range(0, left + 1):
            if q > 0:
                p = market_price(item, cur)
                rev += p
                if p > 1: cur += 1          # my unit
                if k < s:
                    if p > 1: cur += 1      # the opponent's unit of the same round, same quote
                k += 1
            end_inv = tail(cur, max(0, s - k)) - drains[i]
            v, plan = go(i + 1, left - q, end_inv)
            if rev + v > best_v:
                best_v, best_plan = rev + v, (q,) + plan
        return best_v, best_plan

    v, plan = go(0, units, inv0)
    return v, list(plan) + [0] * (n - len(plan))


MILK = dict(units=24, inv0=MARKET_I0 + 20, shops=["PIZZA_SHOP", "SMOOTHIE_SHOP"], opp=[4] * 6 + [0] * 18)


def milk_hourly_drains():
    """Day 29 (steps 696..719): shops drain at hours 0,4,...,20 (2 units: two milk shops), the centre 1 at hour 0."""
    return [(2 if h % 4 == 0 else 0) + (1 if h == 0 else 0) for h in range(24)]


def grade_milk_front_run(d):
    plan = [int(max(0, x)) for x in list(d.units_per_hour)[:24]]
    plan += [0] * (24 - len(plan))
    tot = sum(plan)
    if tot > MILK["units"]:
        over = tot - MILK["units"]
        for i in range(23, -1, -1):
            cut = min(over, plan[i]); plan[i] -= cut; over -= cut
    drains = milk_hourly_drains()
    v = lockstep_schedule_value("MILK", MILK["inv0"], plan, MILK["opp"], drains)
    naive = lockstep_schedule_value("MILK", MILK["inv0"], [0] * 23 + [MILK["units"]], MILK["opp"], drains)
    dump = lockstep_schedule_value("MILK", MILK["inv0"], [MILK["units"]] + [0] * 23, MILK["opp"], drains)
    best, best_plan = best_lockstep_schedule("MILK", MILK["inv0"], MILK["units"], MILK["opp"], drains)
    return dict(choice=plan, value=v, naive=naive, best=best, best_choice=best_plan, score=gain_score(v, naive, best),
                detail={"dump_hour0": dump, "wait_hour23": naive})


CROP = dict(tiles=25, day=12, last_day=29,
            offsets={"WHEAT": -250, "CARROT": -102, "TOMATO": -102, "STRAWBERRY": -120, "MELON": 144},
            shops=["FARMERS_MARKET", "FARMERS_MARKET", "BRUNCH_SPOT", "PIZZA_SHOP"],
            seed={"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80},
            # (days after planting, units per plant) for each sale of one planting, watered daily, no fertilizer
            harvests={"WHEAT": [(4, 4)], "CARROT": [(3, 3)], "MELON": [(10, 6)],
                      "TOMATO": [(8, 1), (9, 1), (10, 1), (11, 1)], "STRAWBERRY": [(10, 1), (12, 1), (14, 1), (16, 1)]})


def crop_value(crop):
    """Revenue minus seeds for one planting of `crop` on all tiles today; each harvest is sold at hour 0 of its day
    (single seller); the town drains the pool every day meanwhile; harvests after the last day are lost."""
    n = CROP["tiles"]
    inv = MARKET_I0 + CROP["offsets"][crop]
    drain = daily_drain(crop, CROP["shops"])
    rev, day = 0, CROP["day"]
    for age, units in CROP["harvests"][crop]:
        sale_day = CROP["day"] + age
        if sale_day > CROP["last_day"]:
            break
        inv -= drain * (sale_day - day); day = sale_day
        r, inv = sell_run(crop, inv, n * units)
        rev += r
    return rev - n * CROP["seed"][crop]


def grade_crop_choice(d):
    crop = str(d.crop).strip().upper()
    vals = {c: crop_value(c) for c in CROP["harvests"]}
    vals["NONE"] = 0
    if crop not in vals:
        crop = "NONE"
    best = max(vals, key=vals.get)
    return dict(choice=crop, value=vals[crop], naive=0, best=vals[best], best_choice=best,
                score=gain_score(vals[crop], 0, vals[best]), detail=vals)


def grade_hire_math(d):
    ok_n = int(d.hire_more) == 1
    ok_c = int(d.extra_cost) == 8
    return dict(choice=[int(d.hire_more), int(d.extra_cost)], value=(ok_n + ok_c) / 2, naive=0, best=1,
                best_choice=[1, 8], score=(0.5 if ok_n else 0.0) + (0.5 if ok_c else 0.0))


def grade_feed(d):
    feed = {str(x).strip().upper()[:1] for x in d.feed}
    at_risk = {"A", "B"}
    hit = len(feed & at_risk)
    score = 1.0 if hit == 2 and len(feed) <= 3 else (0.5 if hit == 1 and len(feed) <= 3 else 0.0)
    return dict(choice=sorted(feed), value=score, naive=0, best=1, best_choice=["A", "B", "any one of C/D/E"], score=score)


def grade_fertilizer(d):
    ans = (int(d.units_with_fertilizer) == 6, int(d.units_without_fertilizer) == 6, int(d.age_first_full_with_fertilizer) == 8)
    score = sum(ans) / 3
    return dict(choice=[int(d.units_with_fertilizer), int(d.units_without_fertilizer), int(d.age_first_full_with_fertilizer)],
                value=score, naive=0, best=1, best_choice=[6, 6, 8], score=score)


# ---------------------------------------------------------------------------------------------- sim tasks
OPENING_LABELS = {
    "meta_a": "2 cows, 3 sheep, 6 melon seeds, 10 wheat seeds, 5 wheat to feed the animals, hire 4-6 hands (about $2,900)",
    "default": "4 cows, 14 melon seeds, 6 wheat seeds, 4 wheat (about $2,900)",
    "melon_max": "25 melon seeds, 10 wheat seeds, no animals (about $2,100; the rest stays as cash)",
    "goose_farm": "6 geese (+coops), 6 melon seeds, 10 wheat seeds, 3 wheat (about $2,500)",
    "cautious": "4 melon seeds, 6 wheat seeds, no animals; keep about $2,600 in cash for later",
    "strawberry_rush": "20 strawberry seeds, 6 wheat seeds, no animals (about $2,100)",
    "land_first": "buy the NE quadrant now ($1,000), 12 melon seeds, 8 wheat seeds (about $2,050)",
    "cows_only": "6 cows (+pastures), 6 wheat seeds, 6 wheat (about $2,650)",
}
SHEEP_ARMS = [0, 2, 4, 6, 8]
HANDS_ARMS = [2, 4, 6, 8, 10, 12, 14]
SE_LABELS = {"buy_day12": "buy SE now (day 12)", "buy_day16": "buy SE on day 16", "buy_day20": "buy SE on day 20", "never": "never buy SE"}
TOMATO_ARMS = [16, 18, 20, 22]
CARROT_ARMS = [24, 25, 26, 27]


def grade_opening(d):
    opt = str(d.option).strip().lower().replace(" ", "_")
    arm = opt if opt in TABLES["opening"]["arms"] else "cautious"
    return sim_grade("opening", arm)


def grade_sheep(task):
    def g(d):
        return sim_grade(task, f"sheep_{snap(int(d.value), SHEEP_ARMS)}")
    return g


def grade_se(d):
    opt = str(d.option).strip().lower().replace(" ", "_")
    arm = opt if opt in SE_LABELS else ("never" if "never" in opt or "no" in opt else "buy_day12")
    return sim_grade("se_quadrant", arm)


def grade_hands(d):
    return sim_grade("max_hands", f"hands_{snap(int(d.value), HANDS_ARMS)}")


def grade_tomato(d):
    v = int(d.value)
    arm = "off" if v < 0 else f"plant_day{snap(v, TOMATO_ARMS)}"
    return sim_grade("terminal_tomato", arm)


def grade_carrot(d):
    v = int(d.value)
    arm = "off" if v < 0 else f"plant_day{snap(v, CARROT_ARMS)}"
    return sim_grade("terminal_carrot", arm)


def state_of(task):
    return STATES[task]["text"]


SIM_NOTE = ("Your farm is run by a competent scripted farmhand policy (it waters, feeds, harvests, hires and sells on "
            "its own); you only set the strategic decision below and the policy plays the rest of the season.")

TASK_SPECS = {
    # --- sanity (rules arithmetic)
    "hire_math": dict(family="sanity", schema=HireDecision, grade=grade_hire_math,
        state="Day 12, hour 18 of 24 (6 action-hours remain today). Cash $900. You (the farmer) plus 5 hands hired today "
              "(their hires cost 1+1+2+3+5 = $12). 40 plants have not been watered today and were NOT watered yesterday: "
              "any of them left unwatered tonight becomes a weed. Each unit can water exactly 1 plant per hour (they are all "
              "standing among the plants; ignore walking).",
        question="How many MORE hands must you hire right now, at minimum, so that all 40 plants get watered today, and what "
                 "do those extra hires cost in total? Reply with hire_more (integer) and extra_cost (dollars, integer)."),
    "feed_or_lose": dict(family="sanity", schema=FeedDecision, grade=grade_feed,
        state="Day 9, hour 0. Cash $0 (you cannot buy wheat today). The shed holds exactly 3 WHEAT. You own 5 cows on "
              "pastures, labelled A, B, C, D, E. Yesterday cows A and B were NOT fed; cows C, D and E were fed. Feeding costs "
              "1 wheat per cow per day.",
        question="Which cows do you feed today? Reply with the list of labels in `feed`."),
    "fertilizer_melon": dict(family="sanity", schema=FertilizerAnswer, grade=grade_fertilizer,
        state="A MELON was planted on day 0 and is watered every day. You are deciding whether to spend one FERTILIZER "
              "($100) on it at age 6 (the first day of its bonus window).",
        question="(1) How many units will the fertilized plant hold when harvested at age 10? (2) How many units without "
                 "fertilizer at age 10? (3) At what age does the fertilized plant first hold its maximum 6 units? Reply with "
                 "units_with_fertilizer, units_without_fertilizer, age_first_full_with_fertilizer (integers)."),
    # --- exact market tasks
    "melon_dump": dict(family="exact", schema=SellNow, grade=grade_melon_dump,
        state="Day 10, hour 0. Your shed holds 72 MELON (12 plants x 6 units, harvested this morning). Melon market "
              "inventory is exactly at I0, price $250. The town has no shop that buys melons (only the town centre, 1 unit "
              "per day). Your opponent also holds 72 melons and WILL sell all 72 this same hour (their bot always does). "
              "Whatever you do not sell now, your bot sells at hour 0 tomorrow (day 11).",
        question="How many melons do you sell this hour? Reply with sell_now (0-72)."),
    "melon_race_timing": dict(family="exact", schema=HarvestDay, grade=grade_melon_race,
        state="Day 9, hour 0. You have 12 MELON plants planted on day 0 and watered daily: after today's watering they hold "
              "5 units each (they reach the 6-unit cap tomorrow, age 10). Melon inventory is at I0 ($250). The opponent has "
              "12 identical melon plants and their bot harvests at age 10 and sells all 72 units at hour 0 of day 10. No "
              "shop buys melons; the town centre removes 1 per day. If you harvest today you sell 60 units alone today; if "
              "you harvest tomorrow you sell 72 units in the same hour as the opponent's 72 (lockstep).",
        question="Harvest today (day 9, 60 units) or tomorrow (day 10, 72 units)? Reply with harvest_day = 9 or 10."),
    "wool_lot": dict(family="exact", schema=ThreeDayPlan, grade=grade_wool_lot,
        state="Day 27, hour 0. Your shed holds 30 WOOL. Wool inventory is at I0+40 (a glut: price $107). The town has one "
              "YARN_STORE (removes 2 wool every 4 hours = 12 per day) plus the town centre (1 per day). Your bot sells the "
              "day's quota at hour 0; the opponent holds no wool. Three selling days remain: 27, 28, 29. Unsold wool is "
              "worth nothing after day 29.",
        question="How many wool units do you sell on day 27, day 28 and day 29 (integers summing to at most 30)?"),
    "milk_front_run": dict(family="exact", schema=HourlyPlan, grade=grade_milk_front_run,
        state="Day 29 (the last day), hour 0. Your shed holds 24 MILK. Milk inventory is at I0+20 (price $118). Open shops "
              "that buy milk: PIZZA_SHOP and SMOOTHIE_SHOP (each removes 1 milk at hours 0, 4, 8, 12, 16, 20, right after "
              "that hour's market); the town centre removes 1 at hour 0. The opponent holds 24 MILK too and their bot "
              "sells 4 milk in each of hours 0, 1, 2, 3, 4, 5 (you know this from their replays); in any hour where you "
              "both sell, units are matched in lockstep. Unsold milk is worth nothing after hour 23.",
        question="Give the number of milk units you sell in each of the 24 hours (a list of 24 integers, sum at most 24)."),
    "crop_choice": dict(family="exact", schema=CropChoice, grade=grade_crop_choice,
        state="Day 12, hour 0. You just unlocked 25 empty tiles and have idle labour and cash for seeds. Open shops: "
              "FARMERS_MARKET x2, BRUNCH_SPOT, PIZZA_SHOP, so the town removes per day: WHEAT 25, CARROT 13, TOMATO 19, "
              "STRAWBERRY 19, MELON 1 (town centre only). Market inventory relative to I0 right now: WHEAT -250, CARROT "
              "-102, TOMATO -102, STRAWBERRY -120, MELON +144. Prices now: WHEAT $41, CARROT $43, TOMATO $72, STRAWBERRY "
              "$212, MELON $43. Assume the opponent sells nothing of the crop you pick, you plant ONE crop on all 25 "
              "tiles today (one planting only; tiles idle afterwards), water daily, no fertilizer, and sell each harvest "
              "at hour 0 of its day (all 25 plants at once; one-time crops sell their whole yield, ongoing crops sell each "
              "picking on its day). Harvests that would land after day 29 are lost.",
        question="Which crop maximises revenue minus seed cost: WHEAT, CARROT, TOMATO, STRAWBERRY, MELON, or NONE? Reply with `crop`."),
    # --- simulation tasks (menus; each arm was played by the engine)
    "opening": dict(family="sim", schema=OptionChoice, grade=grade_opening,
        state="Day 0, hour 0. Cash $3,000, one empty 5x5 quadrant, no shops open yet (the first opens on day 3, at random). "
              "The opponent starts identically. " + SIM_NOTE,
        question="Choose ONE opening shopping list for day 0 (reply with the option key in `option`):\n" +
                 "\n".join(f"  - {k}: {v}" for k, v in OPENING_LABELS.items())),
    "sheep_yarn": dict(family="sim", schema=IntChoice, grade=grade_sheep("sheep_yarn"),
        state=lambda: state_of("sheep_yarn") + "\n" + SIM_NOTE,
        question="A YARN_STORE just opened. Set the maximum number of SHEEP ($500 each, 1 WOOL every 3 days, 1 wheat/day) "
                 "your policy may own from now on: 0, 2, 4, 6 or 8 (it buys them as cash allows). Reply with `value`."),
    "sheep_no_yarn": dict(family="sim", schema=IntChoice, grade=grade_sheep("sheep_no_yarn"),
        state=lambda: state_of("sheep_no_yarn") + "\n" + SIM_NOTE,
        question="Set the maximum number of SHEEP ($500 each, 1 WOOL every 3 days, 1 wheat/day) your policy may own from now "
                 "on: 0, 2, 4, 6 or 8 (it buys them as cash allows). Reply with `value`."),
    "se_quadrant": dict(family="sim", schema=OptionChoice, grade=grade_se,
        state=lambda: state_of("se_quadrant") + "\n" + SIM_NOTE,
        question="The last quadrant (SE, 25 tiles) costs $4,000. Choose ONE (reply with the key in `option`):\n" +
                 "\n".join(f"  - {k}: {v}" for k, v in SE_LABELS.items())),
    "max_hands": dict(family="sim", schema=IntChoice, grade=grade_hands,
        state="Day 0, hour 0, cash $3,000 (the standard opening: 4 cows, 14 melons, 6 wheat; the policy expands to 75 tiles by "
              "day 10 and keeps 6-10 animals, a strawberry field, wheat for feed and late crops). Every plant needs watering "
              "every day and every animal feeding and care; each unit, including the farmer, gets 24 actions a day and "
              "walking between tiles costs actions. The n-th hand of a day costs fib(n): 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, "
              "89, 144, 233, 377. " + SIM_NOTE,
        question="Set the season-long cap on hands hired per day: 2, 4, 6, 8, 10, 12 or 14. Reply with `value`."),
    "terminal_tomato": dict(family="sim", schema=IntChoice, grade=grade_tomato,
        state=lambda: state_of("terminal_tomato") + "\n" + SIM_NOTE,
        question="Should your policy plant up to 10 TOMATO ($50 seed; 1 unit per day on days 8-11 after planting) as a "
                 "late-season play, and when? Reply with `value` = the planting day (16, 18, 20 or 22) or -1 for no tomatoes."),
    "terminal_carrot": dict(family="sim", schema=IntChoice, grade=grade_carrot,
        state=lambda: state_of("terminal_carrot") + "\n" + SIM_NOTE,
        question="Should your policy plant up to 40 CARROT ($20 seed; harvest at age 3 with 3 units) as a last cash crop, and "
                 "when? Reply with `value` = the planting day (24, 25, 26 or 27) or -1 for no carrots."),
}
TASK_IDS = list(TASK_SPECS)


def build_prompt(task_id):
    spec = TASK_SPECS[task_id]
    state = spec["state"]() if callable(spec["state"]) else spec["state"]
    return (f"{RULES}\n\n=== SITUATION (task id: {task_id}) ===\n{state}\n\n=== DECISION ===\n{spec['question']}\n\n"
            "Think it through, then answer in the requested JSON structure and give a 1-3 sentence `rationale`.")

# %% [markdown]
# ## 5. Tasks

# %%
def flags_in(text):
    return {k: bool(re.search(p, text or "")) for k, p in FLAG_PATTERNS.items()}


def example_json(schema):
    ex = {}
    for f in dataclasses.fields(schema):
        t = str(f.type)
        ex[f.name] = [] if "list" in t else (0 if f.type is int else "...")
    return json.dumps(ex)


def _prompt_with_backoff(llm, text, schema, extra):
    """The model proxy answers 429 'heavy load, try again later' for busy models: wait and retry a few times."""
    import time
    delays = [20, 45, 90]
    for i in range(len(delays) + 1):
        try:
            return llm.prompt(text, schema=schema, extra_api_params=extra)
        except Exception as e:
            if type(e).__name__ != "RateLimitError" or i == len(delays):
                raise
            time.sleep(delays[i])


def ask(llm, prompt, schema):
    """Structured decision. Attempt 1 with a modest completion budget (the model proxy reserves quota from
    max_tokens, so an uncapped call is refused for the priciest models); if the model ran out of room while reasoning
    (LengthFinishReasonError) attempt 2 raises the budget; a last attempt asks for the bare JSON object.
    Returns (decision or None, note or None); the note records what the first attempt(s) did."""
    is_openai = type(llm).__name__ == "OpenAI"
    notes = []
    budgets = [6000, 24000] if is_openai else [None]
    for b in budgets:
        try:
            extra = {"max_tokens": b} if b else None
            return _prompt_with_backoff(llm, prompt, schema, extra), (" | ".join(notes) or None)
        except Exception as e:
            notes.append(f"{type(e).__name__}@{b}: {str(e)[:160]}")
            if type(e).__name__ != "LengthFinishReasonError":
                break
    try:
        retry = ("Your previous reply could not be parsed as the requested object. Reply with ONLY a JSON object with exactly "
                 f"these fields and nothing else (no schema, no prose): {example_json(schema)}")
        extra = {"max_tokens": 24000} if is_openai else None
        return _prompt_with_backoff(llm, retry, schema, extra), "strict retry after " + " | ".join(notes)
    except Exception as e2:
        return None, " | ".join(notes) + f" | retry: {type(e2).__name__}: {str(e2)[:160]}"


@kbench.task(name="farm_decision", store_task=False, description="One Kaggriculture decision, graded by the engine.")
def farm_decision(llm, task_id: str) -> dict:
    spec = TASK_SPECS[task_id]
    if spec["family"] == "sim" and task_id not in TABLES:
        kbench.assertions.assert_fail(expectation=f"offline table for {task_id} is missing")
        return {"task_id": task_id, "family": spec["family"], "score": 0.0, "error": "missing table"}
    kbench.system.send("You manage a farm in the Kaggriculture simulation. Decide like a careful economist: the market "
                       "rules in the briefing are exact and the grader applies them literally.")
    decision, err = ask(llm, build_prompt(task_id), spec["schema"])
    if decision is None:
        kbench.assertions.assert_fail(expectation=f"{task_id}: no parseable decision ({err})")
        return {"task_id": task_id, "family": spec["family"], "score": 0.0, "choice": None, "value": None, "naive": None,
                "best": None, "best_choice": None, "flags": flags_in(""), "rationale": "", "error": err}
    try:
        g = spec["grade"](decision)
    except Exception as e:
        kbench.assertions.assert_fail(expectation=f"{task_id}: decision could not be graded ({type(e).__name__}: {str(e)[:200]})")
        return {"task_id": task_id, "family": spec["family"], "score": 0.0, "choice": str(decision)[:80], "value": None,
                "naive": None, "best": None, "best_choice": None, "flags": flags_in(""), "rationale": "", "error": str(e)[:300]}
    kbench.assertions.assert_true(g["score"] >= 0.5, expectation=f"{task_id}: capture at least half of the available gain")
    rationale = getattr(decision, "rationale", "")
    return {"task_id": task_id, "family": spec["family"], "score": float(g["score"]),
            "choice": g.get("choice", g.get("arm")), "value": g["value"], "naive": g["naive"], "best": g["best"],
            "best_choice": g.get("best_choice", g.get("best_arm")), "flags": flags_in(rationale), "rationale": rationale,
            "error": err}


@kbench.task(name="farm_economy_benchmark",
             description="Mean captured gain over 15 Kaggriculture economic decisions graded by the game engine (0-1).")
def farm_economy_benchmark(llm) -> float:
    df = pd.DataFrame({"task_id": TASK_IDS})
    with kbench.client.enable_cache():
        runs = farm_decision.evaluate(llm=[llm], evaluation_data=df, n_jobs=3, timeout=900,
                                      on_failure="continue", max_attempts=1)
    rows = []
    if len(runs.completed_runs):
        rows = [r for r in runs.completed_runs.as_dataframe().result.tolist() if isinstance(r, dict) and "task_id" in r]
    for r in runs.errored_runs:
        print(f"ERRORED {r.params.get('task_id')}: {str(r.error_message).strip()[-400:]}")
    scores = {t: 0.0 for t in TASK_IDS}            # a task that produced no graded decision counts as 0
    for r in rows:
        scores[r["task_id"]] = float(r.get("score") or 0.0)
    if rows:
        table = pd.DataFrame(rows)
        show = table[["task_id", "family", "choice", "value", "naive", "best", "best_choice", "score"]].copy()
        money = lambda v: "-" if v is None or (isinstance(v, float) and math.isnan(v)) else (f"{v:,.0f}" if abs(float(v)) >= 10 else f"{float(v):.2f}")
        for c in ("value", "naive", "best"):
            show[c] = show[c].map(money)
        show["score"] = show["score"].map(lambda v: f"{v:.2f}")
        show["choice"] = show["choice"].map(lambda v: str(v)[:40])
        show["best_choice"] = show["best_choice"].map(lambda v: str(v)[:40])
        print(show.to_string(index=False))
        fl = pd.DataFrame(table["flags"].tolist())
        print("\nrationale flags:", {k: int(v) for k, v in fl.sum().items()})
        fam = {}
        for r in rows:
            fam.setdefault(r["family"], []).append(float(r.get("score") or 0.0))
        print("mean score by family:", {k: round(sum(v) / len(v), 3) for k, v in fam.items()})
        print("\n--- rationales ---")
        for r in rows:
            tag = f" [error: {r['error'][:120]}]" if r.get("error") else ""
            print(f"[{r['task_id']}] (score {float(r.get('score') or 0):.2f}){tag} {str(r.get('rationale', ''))[:500]}")
    graded = sum(1 for r in rows if r.get("choice") is not None)
    kbench.assertions.assert_equal(len(TASK_IDS), graded, expectation="every task produced a graded decision")
    print(f"graded {graded}/{len(TASK_IDS)} tasks")
    return float(sum(scores.values()) / len(TASK_IDS))

# %% [markdown]
# ## 6. Run

# %%
_LLM = kbench.llm
if os.environ.get("FARMBENCH_STUB"):        # local development only: kbench.llm is not configured outside Kaggle
    from stub_llm import StubLLM
    _LLM = StubLLM(os.environ["FARMBENCH_STUB"])

run = farm_economy_benchmark.run(_LLM)
print("FARMBENCH SCORE:", run.result)
