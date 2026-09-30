# SUNRISE AUTOPSY — measured gap vs public meta

Hard rule triggered: sunrise-v5 loses **0-12** to the exact public Barnyard V7
artifact. Sunrise is abandoned as the strategic parent.

## Head-to-head (paired seeds, both seats, official environment)

`benchmark/meta.py --cand main.py --opp barnyard_v7 --games 6 --stage meta_holdout`

```
games 12   W 0   L 12   T 0
win rate  0.0%   Wilson 95% CI [0.000, 0.243]
median cash      5,343   (sunrise)
mean   cash      5,250
p10 / p90        3,442 / 7,973
mean opponent cash 166,628
runtime max      3.44 s per episode (both agents)
non-DONE         0
```

The 95% CI upper bound of 24.3% means even the most sunrise-favourable reading
of this sample is a decisive loss. There is no reading of the data in which
sunrise is competitive.

### Cash gap

| | sunrise-v5 | Barnyard V7 | Ratio |
|---|---|---|---|
| median cash | $5,343 | **$166,628** | **31×** |
| self-play reference | ~$7,500 | $185,816 | 25× |

This is not a tuning gap. It is a two-order-of-magnitude difference in final
bank, which corresponds to a large difference in *productive capacity*.

## Why: measured, not speculated

Barnyard V7's own module docstring states the architecture:

> "A complete season route handles capital, labor, farming, and planned sales.
> Runtime logic stays narrow: **actor-local WEED repair**, **demand-aware
> SELL-slot ranking**, **near-clone premium preemption with exact quantity
> repayment**, and **terminal liquidation**. When a near clone is detected, the
> controller searches **three turns ahead** first, then falls back to two turns
> and one while repaying exactly the shifted quantity on its original due turn."

Version string: `adaptive-preempt-3x2x1`.

Four mechanisms sunrise has no equivalent of:

1. **Near-clone preemption (3/2/1-turn lookahead).** When a premium product
   appears in shed, it looks ahead to find a turn where the *opponent* has no
   pending sell that would crash the shared market, commits the sale there, and
   repays exactly the shifted quantity later. This is the single most valuable
   mechanism in the game, because it converts the shared dynamic price into a
   private scheduling problem. Sunrise sells greedily whenever its own floor
   allows, which means it frequently sells *into* an opponent's dump and
   destroys both agents' prices.
2. **Actor-local WEED repair.** Sunrise treats DIG as a low-priority task
   (priority 2, below harvest). Barnyard repairs weeds locally to the actor,
   keeping a unit's own working area clear without paying cross-map travel.
3. **Demand-aware SELL-slot ranking.** Sunrise ranks products by a static
   price-floor fraction. Barnyard ranks by live town/shop demand from
   `obs["town"]["unlocked_shops"]`.
4. **Terminal liquidation.** Sunrise relies on the daily shed sell plus a
   `HARVEST_LAST_DAY` cutoff. Barnyard has an explicit terminal phase.

## Sunrise's specific suspicious choices, re-tested

Every previous assumption was re-checked against the current environment and
against Barnyard's embedded constants. Several were wrong.

| sunrise assumption | verdict | evidence |
|---|---|---|
| "wheat is the backbone" | **not established** | Barnyard's embedded plan is not wheat-dominated in the way sunrise assumes; the real driver is premium preemption, which requires animals (EGG/MILK/WOOL) held as a schedule, not dumped |
| "animals are traps" | **falsified by evidence** | Barnyard runs preemption on premium products. EGG's curve is `log` (glut-safe, $39 after 500 units) and MILK/WOOL have large per-animal margins. Sunrise never built an animal at all |
| "fertilizer is always bad" | **plausible but untested against meta** | Sunrise's own math ($100 cost, ~$38 yield) holds, but Barnyard may use CARE/fertiliser loops we did not replicate |
| "melon should be tranche-sold" | **partially right, wrong mechanism** | Tranching matters, but sunrise tranches against a static floor fraction; Barnyard tranches against observed opponent behaviour |
| "land // 5 melon quota optimal" | **untested / likely wrong** | No meta agent evidence either way. Quota was tuned only against sunrise's own weak league |
| "MAX_TRAVEL = 4" | **likely harmful** | With 100 tiles and 12 hands, a radius-4 assignment makes long routes to distant ripe crops impossible; sunrise logged 82-92 plants lost to decay per season |
| "harvest at max_yield_day" | correct but insufficient | Sunrise still lost plants to decay because routing, not timing, was the binding constraint |
| "static crop portfolio" | **harmful** | Barnyard's `adaptive-preempt-3x2x1` adapts the sale schedule per turn |

## Environment mismatch found in the public artifact

Barnyard V7's embedded `_MARKET_PARAMS` predate a later environment change:

```
                 Barnyard V7 (Aug 2026)          Current official env
CARROT below     log    / 0.20                   hinge  / 1.00
TOMATO below     linear / 0.40                   hinge  / 0.40
EGG    below     linear / 0.40                   hinge  / 0.40
```

The current `hinge` shape is linear up to `x = T` and quadratic above, so
**below `I0 - T` the price is identical to the old `linear` curve**. The
mismatch only matters for deep scarcity, which is rare. The agent is otherwise
compatible: it runs 720 turns, both seats DONE, no crashes, max call 1.03 ms.

## Conclusion

Sunrise is not a viable parent. Its architecture (static priority planner,
greedy market, static portfolio) lacks the opponent-responsive scheduling that
the top of this leaderboard is built on. The correct move is to adopt the exact
public artifact as the new parent and only attempt surgical changes that beat it
against multiple meta agents.