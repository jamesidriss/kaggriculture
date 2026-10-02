# SUNRISE FINAL AUTOPSY — corrected

All numbers re-measured this session on the **corrected** harness. The previous
version of this report is void: `sunrise-v5` defines `agent(obs)` with one
argument, so under the old harness it was never actually played and every
sunrise number in it — including the 792-game record — was a measurement of an
inert agent. See `reports/HARNESS_SIGNATURE_AUDIT.md`.

The failure is real. It is worse than previously reported.

## 1. Ladder reality (uncontested)

14 real ladder episodes downloaded from Kaggle; seats verified 40-vs-0 by
action-matching our exact submitted bytes. Full rows in
`data/final_evaluation_episodes.csv`.

| bot | ladder rating | games | W-L | opponent cash at which it starts losing |
|---|---|---|---|---|
| sunrise-v1 | **348.1** | — | — | best of our five, and still 2,700 points off the lead |
| sunrise-v2 | 322.0 | — | — | |
| sunrise-v3 | 316.8 | — | — | |
| sunrise-v5 | 252.6 | 7 | 4-3 | ~$8-10k |
| sunrise-v4 | 138.5 | 7 | 3-4 | below a passive opponent |

sunrise-v4 lost three games to opponents that finished at exactly $3,000 —
players who never acted — including two total collapses ($82 and $220 final
bank). sunrise-v5 beat opponents up to ~$6.9k and lost every game above $10k.

The five submissions and their scores are live on the competition page; the
ratings above are the official `publicScore` values read at audit time.

## 1b. Reconfirmation on the corrected harness

Because a harness bug previously produced a false 72-win record for this very
agent, the 0-792 result was re-verified rather than assumed. Sunrise is a
one-argument agent, and the retracted explanation ("Kaggle requires two
arguments") was false; what is true is that our own diagnostics invoked agents
directly. Re-run through the canonical runner with the behavioural playability
probe: **719 invocations, seat status DONE in both seats, a non-trivial action
trace, and real market activity.** Sunrise genuinely plays, and genuinely loses.
See `reports/RETRACTIONS.md` R1.

## 2. Corrected local record

Real ladder seeds, 12 per pool, both seats, official `Environment.run`,
719 turns per game, 0 errors:

| pool | record |
|---|---|
| REAL_dev | 0-264 |
| REAL_holdout | 0-264 |
| REAL_final (sealed) | 0-264 |
| **total** | **0-792, 0.00%, Wilson 95% [0.0000, 0.0048]** |

It did not win a single game against any of ten distinct public agents, from
either seat, on any real ladder world. The previous claim of 72 wins came
entirely from the three agents that were also not playing.

## 3. Action economy — the root cause, re-measured

`benchmark/action_economy.py`, 4 paired games each against `starter`, both
seats, after the signature fix. Every number below is from this run.

| metric | **sunrise-v5** | **v51 (champion)** | farm_2945 | barnyard_v7 | v16_rc5 |
|---|---|---|---|---|---|
| median cash | **$6,901** | $168,805 | $167,118 | $161,628 | $158,425 |
| cash vs `starter` (1 game) | **$6,280** | $182,861 | $182,343 | $167,711 | $138,247 |
| total field actions | **35,953** | 29,955 | 29,976 | 29,488 | 29,564 |
| production | **6.2%** | 10.1% | 10.1% | 7.7% | 8.4% |
| maintenance | **13.2%** | 31.8% | 31.8% | 26.7% | 36.6% |
| movement | **63.0%** | 38.4% | 38.2% | 39.9% | 38.6% |
| logistics | **0.0%** | 4.5% | 4.5% | 2.9% | 2.9% |
| PASS | **17.6%** | 15.1% | 15.4% | 22.8% | 13.5% |
| **productive / total** | **19.4%** | **41.9%** | 41.9% | 34.4% | **45.0%** |
| **cash per field action** | **$0.19** | **$5.64** | $5.58 | $5.48 | $5.36 |
| SELL orders | **855** | 1,450 | 3,382 | 2,208 | 3,272 |
| BUY_SEED orders | **5,245** | 779 | 1,558 | 396 | 1,120 |
| BUY_PRODUCT orders | **0** | 268 | 502 | **1,980** | 1,584 |
| HIRE orders | **6,730** | 1,064 | 2,130 | 3,156 | 4,224 |
| total market orders | **12,880** | 3,618 | 7,684 | 7,860 | **10,328** |
| hands mean / max | **10.4 / 15** | 8.6 / 12 | 8.6 / 12 | 9.5 / 14 | 9.1 / 14 |
| production share, days 24-29 | **3%** | 13% | 13% | 10% | 11% |

### What the numbers say

1. **A 29.7× productivity deficit.** $0.19 per field action against the
   champion's $5.64. This single ratio is the result. sunrise issues 35,953
   field actions and converts them into $6,901; the champion issues 29,955 —
   **17% fewer** — and converts them into $168,805, a **24.5× larger** bank.

2. **63.0% of all actions are movement**, against 38.4%. Greedy nearest-task
   assignment with a small travel horizon means workers re-target every turn and
   walk. It spends 11,501 more actions moving than the champion and gets less
   for them.

3. **Maintenance is half the champion's** (13.2% vs 31.8%). This is not an
   efficiency win. It is under-maintenance: crops and animals need daily tending,
   and skipping it suppresses the harvest. v16_rc5 maintains 36.6% and converts
   45.0% of its actions productively.

4. **Zero logistics.** It never moves goods to the shed as a first-class task,
   against 4.5% for both top agents.

5. **It over-buys and under-sells.** 5,245 BUY_SEED orders to the champion's
   779, and 6,730 HIRE orders to 1,064, reaching 15 hands against 12 — with
   *lower* output. Meanwhile it issues only 855 SELL orders against the
   champion's 1,450 and farm_2945's 3,382, and **zero** BUY_PRODUCT orders.
   Harvested product that is never converted to cash scores nothing.

6. **The endgame collapses.** Production share over days 24-29 is **3%** against
   the champion's 13%, with 40% of the same window still spent moving.

## 4. Portfolio

sunrise is wheat-and-melon only, by construction (`_crop_pref` in `main.py`),
and never builds an animal.

The strongest public agents run livestock. The realised revenue on a full
30-day seed (farm_2945 trace, both players) is **WOOL $96,684 · STRAWBERRY
$55,267 · MILK $38,150 · FERTILIZER $24,872 · MELON $18,832 · WHEAT $14,278**,
and the farm ends the season as 17 sheep + 6 cows behind a strawberry belt.

**The earlier "animals are a trap" conclusion was wrong.** It was derived from
the price curve alone, treating a price ceiling as a revenue cap, and it ignored
by-product fertiliser ($24,872), shop demand, and the fact that a large farm
produces far more than the trough. The largest single revenue line in a winning
strategy is wool.

## 5. Structural failures, ranked by measured cost

1. **No livestock economy** — forfeits the largest revenue line outright.
2. **Movement-dominated action profile** — 63% vs 38%; this is what produces the
   $0.19 figure.
3. **Under-maintenance** — 13.2% vs 31.8%; suppresses harvest yield.
4. **Harvested but not sold** — 855 SELL orders; zero BUY_PRODUCT.
5. **Over-hiring and over-sowing** — 6,730 hires and 5,245 seed buys to
   6.2% production.
6. **No logistics** — 0.0%.
7. **Endgame collapse** — 3% production share over the final week.

## 6. What was needed, in order

1. **Tape/zone routing instead of greedy nearest-task.** Kills the 63%.
2. **A sheep/pasture economy** with correct daily feed maintenance.
3. **Convert product to cash every turn** — sell, and buy product when cheap.
4. **Cap the hand ladder**; stop rebuilding labour 6× more than necessary.
5. **Test both seats and verify the agent actually plays**, on every artifact,
   every time.

All five are present in the reference champion, which is why it finishes at
$168,805 where sunrise finishes at $6,901 — and why the gap is 24.5× rather
than the 1.2× the old harness suggested.
