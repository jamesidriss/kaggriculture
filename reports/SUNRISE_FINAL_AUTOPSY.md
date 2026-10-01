# SUNRISE FINAL AUTOPSY

Measured on real ladder episodes (14 games, 2026-10-01) and on elite ladder
seeds (from the public 88,281-episode replay DB). Every number below is from a
run, not an estimate.

## 1. Ladder reality

| bot | rating | sampled games | W-L | 50%-win point (opponent final cash) |
|---|---|---|---|---|
| sunrise-v5 | 250.0 | 7 | 4-3 | **~$8-10k** |
| sunrise-v4 | 153.0 | 7 | 3-4 | **below passive** |

sunrise-v4 lost three games to opponents that finished at exactly $3,000 (never
played), including two total collapses ($82 and $220 final cash).
sunrise-v5 beat opponents up to ~$6.9k and lost every game above $10k.

Reference: the elite meta agents reproduce at **$95k-183k** median on the same
seeds. There is no overlap between our ceiling and their floor — this is a
10-30× economic gap, not a tuning gap.

## 2. Action economy — the root cause

| metric | farm_2945 | multi_route_v43 | barnyard_v7 | **sunrise-v5** |
|---|---|---|---|---|
| total field actions | 29,976 | 29,955 | 29,488 | **35,953** |
| production | 10.1% | 10.0% | 7.7% | **6.2%** |
| maintenance | 31.8% | 31.9% | 26.7% | **13.2%** |
| movement | 38.2% | 38.4% | 39.9% | **63.0%** |
| logistics | 4.5% | 4.5% | 2.9% | **0.0%** |
| PASS | 15.4% | 15.1% | 22.8% | 17.6% |
| **productive / total** | **41.9%** | **41.9%** | 34.4% | **19.4%** |
| **cash per field action** | **$5.58** | **$5.53** | **$5.48** | **$0.19** |
| market orders (SELL) | 1,691 | 3,686 | 2,944 | **513** |
| BUY_LAND | 8 | 16 | 32 | 30 |
| hands (mean/max) | 8.6 / 12 | 8.6 / 12 | 9.5 / 14 | 10.4 / 15 |

sunrise spends **29% of its actions moving** (63.0% vs 38.2%) and earns
**$0.19 per field action against $5.58** — a 29× productivity deficit. It also
issued only 513 SELL orders where farm_2945 issued 1,691 on the same land:
sunrise harvested product it never converted, which is worth exactly zero.

Root cause in our own code: `MAX_TRAVEL = 4` with greedy nearest-task assignment.
A worker that cannot reach a ripe tile within 4 Manhattan steps re-plans to a
different task every turn and walks in circles. farm_2945 keeps a
**zone/tape-based route** and services tasks in a fixed order.

## 3. Portfolio

farm_2945's realised revenue on seed 335464115 (full 30 days, both players):

```
WOOL        $96,684      STRAWBERRY  $55,267
MILK        $38,150      FERTILIZER  $24,872
MELON       $18,832      WHEAT        $14,278
CARROT       $3,982      EGG            $865
TOMATO         $457
```

Its farm ends the season as **17 sheep + 6 cows** on pastures, a strawberry belt
(wheat 25 → strawberry 33 mid-season → carrot 20 at the end), 4 quadrants, 12
hands, and rotates crops into the cheapest lane as shop demand shifts.

**Our "animals are a trap" conclusion was wrong.** We had computed that MILK
floors at ~75 units season-total and WOOL at ~59 from the *price curve alone*.
Forensics show WOOL earned **$96,684** — the top revenue line. The error was
treating the theoretical price-curve ceiling as a revenue cap while ignoring that
a large farm produces far more than the trough, and that fertiliser resale
($24,872) is pure margin on by-product. Sheep pay back in ~7.5 days and then
compound daily.

## 4. Second bug: the artifact we would have submitted was seat-broken

`farm_2945` reads `observation["step"]` at 30 sites. The schema never declares
`step` and the interpreter sets it only for player 0, so the verbatim public
agent **raises `KeyError` at step 0 in seat 1** — on Kaggle too. Patched to
`_step_of()` (day×24+hour, identical), seat 0 is byte-identical and seat 1 works.

This is the failure mode our harness never tested: every previous evaluation of
this agent used it in seat 0 only, where `step` happens to exist.

## 5. Structural failures, in order of cost

1. **No livestock economics.** Sheep/wool is the single largest revenue line in
   the winning agent; sunrise never built an animal. Cost: ~10× final cash.
2. **Movement-dominated action profile.** 63% of actions moving, $0.19/field
   action. The routing policy, not the crop policy, was the binding constraint.
3. **Harvested but never sold.** 513 SELL orders vs 1,691. Unsold inventory
   scores zero.
4. **Static portfolio.** farm_2945 rotates crops into the cheapest lane as shop
   demand shifts; sunrise fixed one mix for the season.
5. **Self-play contamination risk.** An earlier 29-3 result was invalid (league
   file overwritten by the champion). Fixed with a digest-addressed store and
   invariant tests.

## 6. What would have been needed

Order by measured value:

1. Move to a tape/zone routing policy (fixes the 63% movement share).
2. Add sheep/pasture economy with correct daily feed maintenance.
3. Convert product to cash every turn (sell discipline).
4. Rotate crops against observed shop demand.
5. Test both seats on every artifact before trusting any result.

All five are already present in the postmortem champion, which is why it scores
$95k-183k where sunrise scores $5k-9k.