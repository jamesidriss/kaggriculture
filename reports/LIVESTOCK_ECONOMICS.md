# LIVESTOCK ECONOMICS — why "animals are a trap" was wrong

## The retracted claim

The early project concluded from a price-curve calculation that livestock was
a trap: MILK floored near 75 and WOOL near 59, so a pasture could not pay for
its own upkeep. The winning public agents then built large herds anyway. This
report explains exactly why the price-curve reasoning fails.

## 1. What the price-curve argument actually assumed

The argument treated a **price floor as a revenue cap**. It computed, for a
single unit of milk or wool at a given inventory, the price the environment
would pay, and compared it to the animal's purchase and feed cost.

That arithmetic is not wrong. It is answering the wrong question. It models one
unit sold in isolation. An actual farm sells many units, over many turns,
against a market whose price depends on *every* participant's inventory —
including the opponent's — and it earns by-products that never appear in a unit
price.

## 2. Four mechanisms the unit-price model omits

### 2.1 By-product fertiliser

A fed animal produces manure. In this environment `COLLECT_FERTILIZER` is a
worker action that yields fertiliser, which is a sellable good in its own right
and also raises crop yield on the tile. None of that appears in the price of
milk.

The 2945 Farm's realised revenue on a full 30-day seed is:

| product | revenue |
|---|---|
| **WOOL** | **$96,684** |
| STRAWBERRY | $55,267 |
| MILK | $38,150 |
| FERTILIZER | $24,872 |
| MELON | $18,832 |
| WHEAT | $14,278 |

**WOOL is the single largest revenue line in a winning strategy**, ahead of every
crop. The claim that animals were unprofitable is refuted by the strongest
available evidence: the top agents' own books.

### 2.2 Scale moves you off the floor

The price floor is an equilibrium at high inventory. A herd that starts small
sells into the *steep* part of the curve for many turns, and a large farm
produces far more than the trough the floor was measured at. The relevant
quantity is total revenue across a season at a realistic inventory path, not the
asymptotic price.

### 2.3 The by-product feeds the crops that do pay

Fertiliser is not only sold, it is applied. Raising crop yield on a strawberry
belt is a compounding gain over 30 days, and it is invisible in an animal's unit
price. The 2945 Farm pairs 17 sheep and 6 cows with a strawberry belt
specifically, which only makes sense if the animals are subsidising the crops.

### 2.4 Maintenance is a *shared* cost

A unit-price model charges the full daily upkeep to the animal and credits
nothing for the fact that a working herd occupies land and worker-days a
crop-only farm would spend on walking. The correct comparison is at the level
of the whole farm, which is what `benchmark/action_economy.py` measures.

## 3. The farm-level measurement, not the price curve

| metric | v51 (champion) | Farm 2945 | Barnyard V7 | v16_rc5 | sunrise-v5 |
|---|---|---|---|---|---|
| median final cash | $168,805 | $167,118 | $161,628 | $158,425 | **$6,901** |
| BUY_ANIMAL orders (4 games) | 49 | 96 | 96 | 96 | **0** |
| production action share | 10.1% | 10.1% | 7.7% | 8.4% | 6.2% |
| productive / total | 41.9% | 41.9% | 34.4% | 45.0% | **19.4%** |
| cash per field action | $5.64 | $5.58 | $5.48 | $5.36 | **$0.19** |
| cash per field action vs `starter` (1 game) | $182,861 | $182,343 | $167,711 | $138,247 | **$6,280** |

The pattern is unambiguous and it is the opposite of the retracted claim:

- every competitive top agent buys animals; sunrise buys **none**;
- sunrise, the only agent with no livestock, finishes at **$6,901** against
  $158k-$183k for the rest;
- sunrise's cash per field action is **0.19** against **5.36-5.64** for every
  agent that keeps livestock.

sunrise's failure is not a single missing product. It is a **29.7× productivity
deficit** that co-occurs with, and is at least partly caused by, having no
animal economy at all.

## 4. What this does not prove

Stated plainly, because the retracted claim deserves the same care in the other
direction:

- This does **not** prove that adding animals to any agent improves it. The
  evidence is observational: strong agents keep herds, and the one agent that
  does not is catastrophically weak.
- The causal experiment — take a strong agent, remove its herd, measure — was
  not run, and removing a herd from a 460 KB agent is not a one-line change.
- Barnyard V7 keeps 96 animals and is still beaten 0-144 by the two hubs, with a
  *lower* cash per field action than either. Animals are necessary, not
  sufficient. The binding constraint in Barnyard is a 2.8% action-efficiency
  deficit and 4× hire churn, not its portfolio.

## 5. The generalisable lesson

A price curve is a *marginal* statement about one unit at one inventory level.
A season is a *path*: many units, many turns, a shared market, by-products that
are consumed as well as sold, and land and labour that the alternative use would
also have to pay for.

Deriving "this product is not worth producing" from a marginal price requires
knowing the whole farm. We did not, and the early conclusion was confidently
wrong. The check that would have caught it is cheap: **look at the revenue
composition of an agent that actually wins.**
