# Kaggriculture — FINAL_DECISION

Written 2026-09-30 21:10 UTC, ahead of the 23:59 deadline.

## Final champion

- **Version:** `champion_001` / `sunrise-v5`
- **Git commit:** `8919b23841632153423465b2dadcdc4cdb8c4339`
- **SHA256 (`main.py`):** `97ede93268ce2deacc1010005c1d28775c777f3b83a670f25b6c3ff6a8ffd53d`
- **Runner-up preserved:** `champion_000` / `sunrise-v4`, commit `d6f79ce6`,
  SHA256 `2700d073...` — submitted as 56716532 and still active.
- **Lineage:** official `starter` carrot loop → `sunrise-v1` → v2 (bulk seeds) →
  v3 (floor liquidation) → v4 (market-slot reservation) → v5 (melon quota)
- **Licence:** original work. Mirrors Apache-2.0 game constants from
  `kaggle-environments` for exact price prediction; see `THIRD_PARTY.md`.
- **Snapshots:** `champions/champion_000/`, `champions/champion_001/`
  (each with source + `METADATA.txt`)

## Strategy

A hand-laddered wheat treadmill with a reserved melon tranche.

1. **Wheat is the scale crop.** Every unit of WHEAT sells for ~$19-25 forever
   because its glut curve is `log`: oversupply barely moves the price. The farm
   is built to keep as many tiles planted in wheat as the worker budget allows.
2. **Melon is the profit, not the volume.** Melon's `sq` glut curve with
   `above_target` 3.60 means the whole season is a *finite* pot worth about
   $24k — the integral of `250 - 0.01x²` down to a 42% floor. Roughly 14 tiles
   harvested twice extracts essentially all of it. The agent replicates the
   official price function exactly and sells melon in tranches that hold the unit
   price above the floor, because dumping the whole crop at once roughly halves
   the value.
3. **Nothing is ever held at the $1 floor.** Cash is the only thing that scores,
   so stock already priced at the floor is dumped immediately.
4. **Market orders are free.** Only field actions consume a worker turn, so the
   10-order queue runs seeds, land, hires and liquidation in parallel with the
   hands actually farming.
5. **Survival beats profit.** A plant that missed a day must be watered tonight
   or it becomes a weed. That task outranks everything else in the planner.
6. **Horizon discipline.** Nothing is planted or harvested that cannot be sold
   before step 720.

## Changes from baseline

| # | Change | Effect |
|---|---|---|
| 1 | Portfolio planner replacing the single-tile carrot loop | board actually gets worked |
| 2 | List-typed unit actions | fixed silent no-op that discarded every move |
| 3 | Crop preference fall-through | fixed livelock that left the board empty |
| 4 | Harvest at `max_yield_day`, not `first_yield_day` | +32% cash from the same land |
| 5 | Bulk seed purchasing | 141 → 567 wheat units reaching the market |
| 6 | Replicated price function + tranche selling | melon value roughly doubled vs dumping |
| 7 | Land-scaled hand target, capped at 30% of bank | stopped the exponential fib ladder from bankrupting the farm |
| 8 | Sell stock already at the $1 floor | no unsellable inventory carried |
| 9 | Reserve market slots for liquidation before hiring | no shed overflow from truncated SELL lists |
| 10 | Action schema sanitiser | malformed actions cannot ship silently |
| 11 | Melon quota rebalanced to `land // 5` | holdout mean cash vs starter $4,757 → **$7,520** |

## Validation

Opponent league: five distinct families written from the official rules
(`opponents/league.py`) — `crop_wheat`, `crop_melon`, `land_rush`, `hands_max`,
`patient` — plus the official `starter`, `random` and `pass`.

Measured on the **final** source (`champion_001` / `sunrise-v5`):

| Suite | Games | W | L | T | Win rate | Mean cash | Max runtime |
|---|---|---|---|---|---|---|---|
| DEV vs LEAGUE | 20 | 20 | 0 | 0 | **100%** | ~$4.5k | 2.05 s/ep |
| HOLDOUT vs LEAGUE | 20 | 20 | 0 | 0 | **100%** | **$6,717-$7,726** | 1.96 s/ep |
| HOLDOUT vs `starter` | 8 | 8 | 0 | 0 | **100%** | **$7,520** | — |
| DEV vs `starter` | 8 | 8 | 0 | 0 | **100%** | $4,813 | 2.01 s/ep |

Per-family holdout mean cash vs the league: `crop_wheat` $6,704 · `crop_melon`
$6,917 · `land_rush` $7,044 · `hands_max` $7,451 · `patient` $7,726. The
candidate clears every strategy family by a wide margin.

Earlier builds, same harness: vs `random` 12-0, vs `pass` 8-0, DEV vs `starter`
8-0, HOLDOUT vs `starter` 9-1.

Both seats tested on every seed; seeds paired across opponents.

### Execution safety

- **Runtime:** median 0.105 ms, p95 0.173 ms, p99 0.32 ms, **max 0.74 ms** per
  `agent()` call against a 1 s `actTimeout`. Total agent time 0.08 s of the
  1200 s `runTimeout`.
- **Crashes:** 0 across 100+ simulated episodes.
- **Malformed actions:** 0 (schema sanitiser as a hard backstop).
- **Stranded end-of-season value:** **0 units** (shed empty, no carried
  inventory) — the endgame liquidation requirement.
- **Plant losses:** ~92 over a season, caused by crop decay past
  `max_lifespan_step`, not by missed watering.

## Rejected experiments (NO_GO)

| ID | Experiment | Why it was rejected |
|---|---|---|
| E007 | Goose/livestock pipeline | Cash fell $4,672 → $852 and win rate 12-0 → 0-12. Coop construction starved the crop board. Reverted immediately. |
| E008 | Always allow the cheap fib tail (`FIB_MARGINAL_CAP`) | Win rate 12-0 → 7-5. Over-hiring costs more than the extra harvest earns. |
| E004 | Unconstrained hand ladder to the cap | Cash-flow negative: $987/day of hands against ~$1,000/day gross income. |
| E001 | First portfolio draft | Silent no-op bug meant nothing was ever planted. |

## Known weaknesses

- **Cows and sheep are deliberately excluded.** MILK floors at ~75 units
  season-total and WOOL at ~59, so their entire season pot is a few thousand
  dollars regardless of herd size, while each animal consumes a tile plus a daily
  FEED action. Geese would be worth adding, but the measured goose attempt
  (E007) was a large regression and there was no time to land a correct version.
- **Not tuned against the real ladder.** The local league is strong on the
  dimensions it covers, but the actual meta is unknown. `starter` is the only
  opponent whose behaviour is confirmed by a published score.
- **92 plant losses per season** come from crops decaying after
  `max_lifespan_step` when a worker cannot reach them in time. Worth attacking
  with better routing if more time were available.
- **Weeds peak at ~22 tiles** on a 100-tile board.

## Kaggle

| Submission ID | Version | Commit | Status | Validation rating |
|---|---|---|---|---|
| 56716289 | sunrise-v1 | `fd4c370` | COMPLETE | 348.1 |
| 56716337 | sunrise-v2 | `fd4c370` | COMPLETE | 322.0 |
| 56716446 | sunrise-v3 | `f4f58a6` | COMPLETE | 506.8 |
| 56716532 | sunrise-v4 | `d6f79ce` | COMPLETE | **600.0** |
| **56716646** | **sunrise-v5 (FINAL)** | `8919b23` | PENDING | — |

- Submissions before the final: v1, v2, v3, v4 — all completed without error.
- **Final submission ID: 56716646** (`sunrise-v5`) = `champion_001`, commit
  `8919b23`, SHA256 `97ede932...`.
- **Bots left active: `sunrise-v5` (56716646) and `sunrise-v4` (56716532).**
  The swap retired `sunrise-v3` (506.8), the weaker member of the pair — the
  600.0 bot was deliberately preserved.
- **0 submissions remain in today's quota.** The two active slots are final.
- Validation ratings (322-600) are Kaggle's default for a completed validation
  episode and are **not** ladder performance. They confirm only that the agent
  executed cleanly on Kaggle's side. The leaderboard top is ~3053, so none of
  these figures indicate real ladder strength.