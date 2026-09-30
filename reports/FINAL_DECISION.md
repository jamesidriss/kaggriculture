# Kaggriculture — FINAL_DECISION

Written 2026-09-30 21:10 UTC, ahead of the 23:59 deadline.

## Final champion

- **Version:** `champion_000` / `sunrise-v4`
- **Git commit:** `d6f79ce6d364b80c7b538b16cf4aecac8d5b0a26`
- **SHA256 (`main.py`):** `2700d073dac8e58de044b5aebe48b81d9825345a2b5509bb035f45858e610608`
- **Lineage:** official `starter` carrot loop → `sunrise-v1` → v2 (bulk seeds) →
  v3 (floor liquidation) → v4 (market-slot reservation)
- **Licence:** original work. Mirrors Apache-2.0 game constants from
  `kaggle-environments` for exact price prediction; see `THIRD_PARTY.md`.
- **Snapshot:** `champions/champion_000/` (source + `METADATA.txt`)

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

## Validation

Opponent league: five distinct families written from the official rules
(`opponents/league.py`) — `crop_wheat`, `crop_melon`, `land_rush`, `hands_max`,
`patient` — plus the official `starter`, `random` and `pass`.

| Suite | Games | W | L | T | Win rate | Mean cash | Max runtime |
|---|---|---|---|---|---|---|---|
| DEV vs LEAGUE | 20 | 20 | 0 | 0 | **100%** | ~$4.5k | 1.85 s/ep |
| HOLDOUT vs LEAGUE | 20 | 20 | 0 | 0 | **100%** | ~$4.5k | 1.80 s/ep |
| DEV vs `starter` | 8 | 8 | 0 | 0 | **100%** | $4,813 | 2.01 s/ep |
| HOLDOUT vs `starter` | 10 | 9 | 1 | 0 | **90%** | $4,757 | 2.03 s/ep |
| DEV vs `random` | 12 | 12 | 0 | 0 | **100%** | $4,975 | 2.11 s/ep |
| DEV vs `pass` | 8 | 8 | 0 | 0 | **100%** | $5,348 | 2.04 s/ep |

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

| Submission ID | Version | Status | Rating |
|---|---|---|---|
| 56716289 | sunrise-v1 | COMPLETE | 407.9 |
| 56716337 | sunrise-v2 | COMPLETE | 501.2 |
| 56716446 | sunrise-v3 | COMPLETE | 600.0 |
| **56716532** | **sunrise-v4 (FINAL)** | PENDING | — |

- Submissions before the final: v1, v2, v3 — all completed, v3 currently the
  best-rated at 600.0.
- **Final submission ID: 56716532** (`sunrise-v4`), mapping to commit `d6f79ce`.
- **Bots left active:** `sunrise-v4` (56716532) and `sunrise-v3` (56716446).
  v4 retired the weaker `sunrise-v2`; v3 was preserved because it was the
  highest-rated submission at the time of the swap.
- **1 submission attempt held in reserve** for an emergency.
- Validation scores are the Kaggle default for a completed validation episode.
  The meaningful rating only moves once real matches are played.