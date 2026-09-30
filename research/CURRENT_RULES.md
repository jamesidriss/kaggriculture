# Kaggriculture — CURRENT Rules Audit

Source of truth: official competition files `README.md` + `AGENTS.md` (downloaded via Kaggle CLI,
2026-09-30) cross-checked against the installed `kaggle_environments` `kaggriculture.py`.

- Environment: `kaggle_environments`, env name **`kaggriculture`**
- Season: **720 turns** = 24 turns/day × 30 days
- Win condition: **most coins in the bank at end of season.** Unsold inventory is WORTHLESS.
  Ties are possible.

## CRITICAL ECONOMIC CONSTANTS

| Resource | Base | T (glut anchor) | Below func / target | Above func / target | P(I0−T) | P(I0+T) | P(I0+2T) |
|---|---|---|---|---|---|---|---|
| WHEAT | 25 | 400 | sqrt / 0.80 | log / 0.20 | 45 | 20 | 19 |
| CARROT | 35 | 450 | hinge / 1.00 | sqrt / 0.70 | 70 | 10 | 1 |
| TOMATO | 60 | 200 | hinge / 0.40 | sqrt / 0.60 | 84 | 24 | 9 |
| STRAWBERRY | 120 | 100 | sqrt / 0.70 | linear / 1.60 | 204 | 1 | 1 |
| MELON | 250 | 300 | log / 0.20 | sq / 3.60 | 300 | 1 | 1 |
| EGG | 50 | 332 | hinge / 0.40 | log / 0.20 | 70 | 40 | 39 |
| MILK | 160 | 122 | sqrt / 0.60 | linear / 1.60 | 256 | 1 | 1 |
| WOOL | 200 | 105 | log / 0.20 | sq / 3.20 | 240 | 1 | 1 |
| FERTILIZER | 100 | 200 | linear / 0.40 | linear / 0.40 | 140 | 60 | 20 |

`I0 = 10,000` for every product at start. Price floored at **$1**.

### The single most important strategic fact

**T is calibrated to one 5×5 field's 24-day output.** Selling much more than ~T units past
I0 drives premium goods straight to the $1 floor.

- **STAPLES (WHEAT, EGG, FERTILIZER) are glut-safe.** `log`/`linear` shapes mean oversupply is
  absorbed gently. You may dump volume.
- **PREMIUMS (MELON, WOOL, MILK, STRAWBERRY) crash to $1 on modest gluts.**
  `above_target > 1` (melon 3.60, wool 3.20, milk 1.60, strawberry 1.60).
  These must be **sold in controlled tranches / timed**, or matched to town demand.

Corollary: **MELON has NO town shop demand** (see shop table). Its only town sink is the town
center's flat 1/day. Melon volume beyond ~T is near-worthless → melon is a *high-margin,
low-volume* crop (1500 gross per tile per 10 days at base price), not a scale crop.

## Production table

| Type | Yield kind | Seed cost | Base px | 1st yield | Max yield | Subsequent | Max yield units | Yield/tile/day |
|---|---|---|---|---|---|---|---|---|
| WHEAT | one-time | 10 | 25 | 2d | 4d | — | 6 (4 unfert.) | 0.80 |
| CARROT | one-time | 20 | 35 | 2d | 3d | — | 4 (3 unfert.) | 0.75 |
| TOMATO | ongoing | 50 | 60 | 8d | 11d | daily ×4 | 4 | 0.33 |
| STRAWBERRY | ongoing | 100 | 120 | 10d | 16d | every other day ×4 | 4 | 0.24 |
| MELON | one-time | 80 | 250 | 10d | 10d | — | 6 | 0.55 |
| GOOSE→EGG | ongoing | 300 (+coop) | 50 | 4d | ∞ | daily | 4 held | 1.00 |
| COW→MILK | ongoing | 400 (+pasture) | 160 | 8d | ∞ | every 2d | 6 held | 0.50 |
| SHEEP→WOOL | ongoing | 500 (+pasture) | 200 | 6d | ∞ | every 3d | 6 held | 0.33 |
| FERTILIZER | from animals | — | 100 | — | — | 1/animal/day | — | — |

### Pure margin per tile-day at BASE price (unfertilized)

- MELON: 6 / 10d × 250 = **$150/tile/day**  ← highest single-crop rate, but volume-capped
- WHEAT: 4 / 4d × 25 = **$25/tile/day** (fert: $37.5) — glut-safe, so the workhorse
- CARROT: 3 / 3d × 35 = **$35/tile/day**
- EGG: 50/day but $300 sunk into a coop → pays back on day 6
- MILK: 80/day, $400 sunk → pays back day 5
- WOOL: 66.7/day, $500 sunk → pays back day 7.5

**Action economy is the real bottleneck**, not tiles: every unit gets exactly 1 action/turn,
and ongoing production costs ~1 WATER/FEED action per tile per day.

## Watering / feeding (death rules — ZERO TOLERANCE)

- Plants must be watered once per day. **Two consecutive missed end-of-day refreshes → WEED.**
- `PLANT` day counts as the first unwatered day: a seed planted and *not watered the same day*
  hits 2 at end-of-day and dies that night. **There is no grace period.**
- Newly placed animal starts `consecutive_unfed = 0`, so it survives its first day unfed.
  A second consecutive miss → **animal escapes, unrecoverable.**
- Watering is once-per-day; repeat watering is a no-op (so a wasted action, never a bug).

### Yield rules

- One-time crops: from `ceil(max_yield_day/2)` onward, each day watered **inside the bonus
  window** adds +1 to harvestable yield; **fertilized adds +2** (`FERTILIZE` doubles the bonus
  for 3 days).
- Ongoing crops: scheduled production yields 1, **2 if fertilized AND watered that day.**
- Decay: past max lifespan, `yield_units` −1 every other turn until 0 → weed.
  One-time: max lifespan = `max_yield_day + 1`. Ongoing: decay starts 1 day after cumulative
  production hits `max_yield`.
- Animals: unlike crops they produce **indefinitely**; `max_held` caps unharvested product
  on the tile. `CARE` banks +1 per fed-and-cared day, paid out in full on next production.
  `COLLECT_FERTILIZER` = 1 fertilizer/animal/day.
- Weeds: every empty unlocked tile has `weedSpawnChance` = **0.005**/end-of-day. Clear with `DIG`.

## Land & shed

- 10×10 grid, four 5×5 quadrants. **NW unlocked at start.** `BUY_LAND` costs **$1k / $2k / $4k**
  for NE / SW / SE.
- Shed cap **100 non-seed items**. Overflow at end-of-day drop is **DISCARDED — no holding
  area.** Stockpiling on unit inventories does NOT bypass the cap.
- Shed-adjacent tiles = the four centre tiles **(4,4) (5,4) (4,5) (5,5)**. Shed is not a tile.
- `DROP` (shed-adjacent) dumps whole inventory. `PICKUP item [n]` pulls from shed.
  `PLACE item [n]` places an animal on a matching structure underfoot, else drops into shed.
- Seeds live in a **separate uncapped slot** and are consumed directly by `PLANT` — never
  picked up by `PICKUP`.
- All units (farmer + hands) **spawn at the shed each day** and drop inventory at end of day.
  Hands must be re-hired every day.

## Workers

- `HIRE` is a market order. Cost = `farmHandCostMult * fib(n)`, n = hires already today
  → **1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144…** Resets daily.
  Day-1 hire ladder total for k hands = sum of fib.
- Hands spawn NWSE-preferring among the four shed-adjacent tiles, ignoring lock. First hire of
  the day lands on **(5,4)** which is locked until NE is bought — locked tiles are **passable**.

## Market

- Up to **10 orders/turn/player** (`maxMarketOrdersPerTurn`); extras **silently dropped**.
- Orders are processed **one unit at a time across both players concurrently**, in list order.
- Sell price quoted at pre-sell inventory; buy price at post-buy inventory.
- At the **$1 floor the unit is still purchased but NOT added to inventory** — the floor stays
  responsive.
- Only **WHEAT and FERTILIZER** are buyable (`BUY_PRODUCT`). Everything is sellable.
- Seeds and animals are unlimited supply at fixed price.
- **Invalid actions are silent no-ops** — never raises, always costs a turn.

## Town demand

- Town **center**: 1 of every product **excluding fertilizer**, every **24 turns** (= daily),
  flat all season.
- Shops unlock every **3 days**, drawn uniformly **with replacement** (duplicates possible),
  capped at **8 total instances**, and persist once unlocked.
- Each shop instance consumes one of every demanded product every **4 turns**
  (single-product shops consume **2×**).

| Shop | Demands |
|---|---|
| Bakery | eggs, wheat |
| Pizza Shop | milk, tomatoes, wheat |
| Brunch Spot | eggs, wheat, strawberries |
| Yarn Store | wool (2×) |
| Ice Cream Shop | strawberries, milk, wheat |
| Pet Cafe | carrots (2×) |
| Smoothie Shop | strawberries, milk |
| Farmers Market | wheat, carrots, tomatoes, strawberries |

**No shop demands MELON.** Melon's only town sink is the flat 1/day at the town center.

## Turn processing order

1. Action validation
2. Player actions recorded (simultaneous)
3. Market queue processed in order per player
4. Town buy actions (center + shops reduce inventory)
5. Observation update
   - Day refresh (plant/animal condition, reset watered/fed flags)
   - Market price refresh
   - Income update
   - Farm update

## Config defaults (all overridable at episode creation)

`episodeSteps 720`, `boardSize 10`, `startingMoney 3000`, `maxMarketOrdersPerTurn 10`,
`turnsPerDay 24`, `shedCapacity 100`, `weedSpawnChance 0.005`,
`townShopUnlockInterval 3`, `townShopSellInterval 4`, `townCenterSellInterval 24`,
`seed null` (cleared from config after read so it never leaks into observations).

## Deadlines / competition state (2026-09-30)

- Deadline **2026-09-30 23:59**. 10222 teams entered.
- Built-in agents: `pass`, `random`, `starter` (deterministic baseline).
- Submission: `main.py` with `agent(obs)` at archive root.