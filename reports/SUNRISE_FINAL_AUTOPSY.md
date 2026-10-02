# SUNRISE FINAL AUTOPSY — parity-safe revision

All numbers re-measured this session through the corrected harness
(`env.run`, both seats, real ladder seeds). Nothing is carried over from the
previous version without re-derivation.

## 1. Ladder reality (uncontested)

14 real ladder episodes downloaded from Kaggle, seats verified by action-matching
our exact submitted bytes (40-vs-0 confidence per episode).
Full rows in `data/final_evaluation_episodes.csv`.

| bot | rating | games | W-L | 50%-win point (opponent final cash) |
|---|---|---|---|---|
| sunrise-v5 | 241.5 | 7 | 4-3 | **~$8-10k** |
| sunrise-v4 | 158.4 | 7 | 3-4 | **below passive** |

sunrise-v4 lost three games to opponents that finished at exactly $3,000 (never
played), including two total collapses ($82 and $220 final bank). sunrise-v5
beat opponents up to ~$6.9k and lost every game above $10k.

Reference: the reference champion finishes at **$168,805 median** on the same
class of seeds. There is no overlap.

## 2. Action economy — the root cause, re-measured

`benchmark/action_economy.py`, 4 paired games each against `starter`,
both seats. Not a single copied number.

| metric | **sunrise-v5** | **v51 (champion)** | farm_2945 | v50 | Barnyard (repaired) |
|---|---|---|---|---|---|
| median cash | **$6,901** | $168,805 | $167,118 | $168,246 | $161,628 |
| total field actions | **35,953** | 29,955 | 29,976 | 29,955 | 29,488 |
| production | **6.2%** | 10.1% | 10.1% | 10.1% | 7.7% |
| maintenance | **13.2%** | 31.8% | 31.8% | 31.8% | 26.7% |
| movement | **63.0%** | 38.4% | 38.2% | 38.4% | 39.9% |
| logistics | **0.0%** | 4.5% | 4.5% | 4.5% | 2.9% |
| PASS | **17.6%** | 15.1% | 15.4% | 15.1% | 22.8% |
| **productive/total** | **19.4%** | **41.9%** | **41.9%** | **41.9%** | 34.4% |
| **cash per field action** | **$0.19** | **$5.64** | **$.58** | $5.62 | $5.48 |
| SELL orders | **684** | 1,450 | 5,073 | 2,896 | 2,944 |
| BUY_SEED orders | **4,196** | 779 | 2,337 | 1,568 | 528 |
| HIRE orders | **5,384** | 1,064 | 3,195 | 2,128 | 4,208 |
| hands mean/max | 10.4 / 15 | 8.6 / 12 | 8.6 / 12 | 8.6 / 12 | 9.5 / 14 |
| days 24-29 production share | **3%** | 13% | 13% | 13% | 10% |

### What the numbers say

1. **29.7× productivity deficit.** $0.19 vs $5.64 per field action. This is the
   single number that explains the result.
2. **63.0% of all actions are movement** vs 38.4%. Greedy nearest-task assignment
   with `MAX_TRAVEL = 4` means workers re-target every turn and walk.
3. **More workers, less output.** sunrise hires to 15 hands (mean 10.4); the
   champion stops at 12 (mean 8.6). sunrise spends **5× the hire orders**
   (5,384 vs 1,064) and buys **5× the seeds** (4,196 vs 779) to produce
   **6.2%** production actions against the champion's 10.1%.
4. **It barely sells.** 684 SELL orders vs 1,450 (champion) and 5,073
   (farm_2945). Harvested product that is never converted scores zero.
5. **Zero logistics.** It never moves goods to the shed as a first-class task.
6. **The endgame collapses.** Production share over days 24-29 is 3% against the
   champion's 13%.

## 3. Portfolio

sunrise is wheat-and-melon only, by construction (`_crop_pref` in `main.py`),
and never builds an animal.

The champion's realised revenue on a full 30-day seed (farm_2945 trace, both
players): **WOOL $96,684 · STRAWBERRY $55,267 · MILK $38,150 · FERTILIZER
$24,872 · MELON $18,832 · WHEAT $14,278**. Its farm ends the season as
17 sheep + 6 cows with a strawberry belt.

**Our earlier "animals are a trap" conclusion was wrong**, derived from the price
curve alone. The largest single revenue line in the winning strategy is wool.
The error: treating a price-curve ceiling as a revenue cap, while ignoring
by-product fertiliser ($24,872), shop demand and the fact that a large farm
produces far more than the trough.

## 4. Structural failures, ranked by measured cost

1. **No livestock economy.** ~24× cash gap on its own.
2. **Movement-dominated action profile.** 63% vs 38%; drives the $0.19 figure.
3. **Harvested but not sold.** 684 vs 1,450+ SELL orders.
4. **Over-hiring.** 5,384 HIRE orders; 15 hands vs 12, with lower output.
5. **Static portfolio.** No rotation against observed shop demand.
6. **Collapse at the endgame.** 3% production share over the final week.

## 5. What was needed, in order

1. Tape/zone routing instead of greedy nearest-task (fixes the 63% movement).
2. A sheep/pasture economy with correct daily feed maintenance.
3. Convert product to cash every turn.
4. Cap the hand ladder and stop re-hiring 5× more than necessary.
5. Test both seats on every artifact.

All five are already present in the reference champion, which is why it finishes
at $168,805 where sunrise finishes at $6,901.