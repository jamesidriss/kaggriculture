# KAGGRICULTURE ENVIRONMENT CHANGELOG (competition era)

Mechanism-level record of environment changes that materially affect strategy.
Compiled by comparing the currently installed `kaggle-environments` 1.32.7
against the price models and action rules embedded in public agents published at
different dates.

## 1. Market scarcity curve: `linear`/`log` → `hinge` (mid-competition)

**Affected products:** CARROT, TOMATO, EGG.
**Impacted agent families:** every agent that embeds a local price model
(Barnyard V7 family). Agents that read `obs["market"]["prices"]` directly are
unaffected.

Current definition:

```
f_hinge(x) = x/T + 8 * max(0, x/T - 1)^2        # x = I0 - inv (scarcity side)
```

Below `x = T` this is identical to the old normalised `linear` curve. Above
`T` it is quadratic, so price goes vertical as a product is consumed.

### Measured divergence (official `market_price` vs Barnyard V7's embedded model)

| product | market inv | current env | Barnyard V7 | error |
|---|---|---|---|---|
| CARROT | 9,900 | $43 | $40 | −7% |
| CARROT | 9,600 | $66 | $42 | −36% |
| CARROT | 9,400 | $113 | $42 | −63% |
| CARROT | 9,100 | $385 | $43 | −89% |
| CARROT | 8,500 | $1,676 | $43 | −97% (39×) |
| CARROT | 7,000 | $9,259 | $44 | −99.5% (210×) |
| TOMATO | 7,000 | $38,052 | $420 | −99% (91×) |
| EGG | 8,500 | $2,121 | $140 | −93% (15×) |
| EGG | 7,000 | $10,563 | $231 | −98% (46×) |

### Strategic consequence

An agent that models scarcity correctly recognises that selling into a drained
market is enormously profitable and does it early and aggressively. Barnyard's
`log` model sees no price signal and mis-times those sales. This alone explains
most of its 0-22 record against farm_2945.

### Why rankings inverted

August-era scores put Barnyard (3034.8) above the 2945 Farm (2945). Under the
current environment the 2945 Farm wins **22 of 22**. Published scores reflect the
environment that existed when they were earned.

**Partially falsified test:** patching Barnyard's three curves to `hinge` left it
**0-10** against farm_2945. The price model was *necessary but not sufficient* —
the remaining gap comes from routing, worker allocation and sale scheduling.

## 2. Observation schema: `step` is player-0-only

The official observation schema (`kaggriculture.json`) declares:
`player, farms, private, market, town, day, hour, remainingOverageTime`.
`step` is **not declared**. The interpreter sets `state[0].observation.step`,
so only player 0 receives it.

Verified directly in downloaded Kaggle replays: at step 5, player 0's observation
contains `step: 5`, player 1's does not contain the key at all.

**Impacted agent families:** any agent reading `observation["step"]`
unconditionally. `farm_2945` does so at 30 sites and **crashes with `KeyError`
at step 0 in seat 1** — locally and on Kaggle. This is a latent half-broken
submission that a seat-1 evaluation exposes immediately.

Fix: `research/seat_safe_patch.py` rewrites such reads to `day*24 + hour`, which
is numerically identical (`turnsPerDay = 24`). Seat-0 behaviour is unchanged.

## 3. Unchanged (verified current)

These were checked against the installed environment and match the values in
public agents, so no migration is needed:

- Season 720 turns = 24 turns/day × 30 days
- `startingMoney` 3000; land costs 1000 / 2000 / 4000
- `maxMarketOrdersPerTurn` 10; `shedCapacity` 100
- `weedSpawnChance` 0.005; shop unlock every 3 days (with replacement, cap 8);
  shop consumption every 4 turns; town centre every 24 turns
- Crop table (wheat/carrot/tomato/strawberry/melon) and animal table
  (goose/cow/sheep) identical to the values assumed by all recovered agents
- Melon has **no** shop demand (only the town centre's flat 1/day)
- Price floor $1; sell price quoted pre-sale, buy price post-buy
- Shared market: both players' orders process one unit at a time, concurrently

## Detection tooling

`research/compat_linter.py` scans any public agent for embedded copies of
market functions, crop constants, town/shop tables and land costs, and emits
`STALE_PRICE_MODEL` / `STALE_CROP_MODEL` / `STALE_TOWN_MODEL` / `NATIVE_AGENT`.
Run it on every new artifact before adding it to a league.

`tests/test_invariants.py` additionally enforces that the postmortem champion
contains **no** hard `observation["step"]` reads.

## Standing lesson

Re-test every historical agent against the *current* environment before trusting
its score. Two of the strongest-looking public agents (Barnyard V7, The 2945
Farm as published) are either mis-specified or seat-broken, and neither fact is
visible from a leaderboard number.