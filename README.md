# Kaggriculture — post-competition reference repository

The Kaggriculture submission deadline passed. Kaggle's API returns
`400 FAILED_PRECONDITION: "Submission not allowed: Submissions have been disabled
for this competition."` (deadline extended to 2026-10-14, entry gate closed).
**No repository change can affect the competition result.** See
`reports/POST_DEADLINE_ACTIONABILITY.md`.

What this repository now contains is the strongest reproducible legal
Kaggriculture agent we could build, plus the framework that produces trustworthy
evidence about it.

## Reference champion

```
postmortem_champion/main.py
sha256 c936e5a71ba40e1700ca1ab3a3271132407446bbb8b7523ced2cf4450ed8463f
```

The 2945 Farm v9/3 (thomastschinkel, **Apache-2.0**, upstream attribution
retained in-file), with one necessary fix: the verbatim artifact reads
`observation["step"]`, which the schema never declares and the interpreter sets
only for player 0 — so it **crashes at step 0 in seat 1**, on Kaggle included.
`research/seat_safe_patch.py` rewrites 30 such reads to the agent's own
`_step_of()`; seat-0 output is byte-identical before and after.

| pool | seeds | games | W-L-T | errors |
|---|---|---|---|---|
| dev | 10 elite ladder seeds | 100 | 100-0-0 | 0 |
| holdout | 10 (disjoint) | 100 | 100-0-0 | 0 |
| final | 10 (disjoint, untouched until last) | 100 | 100-0-0 | 0 |

All games both seats, official `kaggle-environments` 1.32.7, median final cash
$95k-183k. Bradley-Terry beta 10.203, highest of six agents. Runtime max 28.9 ms
of a 1000 ms `actTimeout`.

## Four findings worth keeping

1. **Published scores are not current evidence.** Barnyard V7 (published 3034.8)
   loses 0-22 to the 2945 Farm (published 2945) under the current environment.
   The `hinge` scarcity change makes CARROT worth $9,259 where Barnyard's model
   says $44 — a 210× mispricing.
2. **Cash and win rate diverge.** farm_2945 often ends a game with *lower* cash
   than the agent it beats. Promotion decisions are win-rate only.
3. **Our livestock conclusion was wrong.** We ruled animals a trap from the price
   curve alone; the winning agent's top revenue line is WOOL at $96,684.
4. **Both seats, always.** A seat-1 crash hid in an artifact that looked strong
   in seat 0. Every evaluation now runs both seats, and the harness asserts it.

## Evidence pipeline

```
CURRENT ENVIRONMENT  (kaggle-environments 1.32.7 is the only source of truth)
  ↓
PUBLIC META         opponents/store/  digest-addressed, licence-checked
  ↓
REAL LADDER WORLDS  seeds/ladder_real_{dev,holdout,final}.txt (from an
                    88,281-episode public replay DB; games both ≥2900)
  ↓
PAIRED BOTH-SEAT    benchmark/meta.py --seeds-file ...
  ↓
INVARIANTS          tests/test_invariants.py  (15 checks, incl. self-play guard)
  ↓
ARTIFACT GATE       benchmark/validate_artifact.py (exact bytes, both seats)
```

Reproduce the champion's record:

```
python benchmark/opponent_store.py verify
python tests/test_invariants.py
python benchmark/meta.py --cand postmortem_champion/main.py \
    --seeds-file seeds/ladder_real_holdout.txt
```

## Tools

| tool | purpose |
|---|---|
| `benchmark/meta.py` | paired both-seat harness; content-digest self-play guard |
| `benchmark/opponent_store.py` | digest-addressed store + manifest verification |
| `benchmark/bradley_tery.py` | offline strength model |
| `benchmark/action_economy.py` | action-category and cash-per-action forensics |
| `benchmark/forensic.py` | per-day farm / market / revenue trace |
| `benchmark/close_games.py` | near-tie mining and divergence location |
| `benchmark/endgame.py` | terminal regret (stranded value at step 719) |
| `benchmark/ingest_replay.py` | ladder replay → episode DB, seat-verified |
| `benchmark/replaydb_query.py` | query the public replay database |
| `research/compat_linter.py` | stale-environment scan for any agent |
| `research/seat_safe_patch.py` | remove hard `observation["step"]` reads |
| `tests/test_invariants.py` | harness correctness gate |

## Reports

`POST_DEADLINE_ACTIONABILITY.md` · `ACTIVE_BOT_REAL_STRENGTH.md` ·
`SUNRISE_FINAL_AUTOPSY.md` · `LOCAL_BRADLEY_TERRY.md` · `OPTIMAL_FINAL_PAIR.md` ·
`FINAL_TOURNAMENT_TRACKER.md`
Research: `research/FINAL_PUBLIC_AGENT_CATALOG.md` · `ENVIRONMENT_CHANGELOG.md` ·
`CURRENT_RULES.md`

## Licence note

`main.py` (the sunrise series) and `benchmark/opponents/league.py` are original
work and are retained only as the record of what we tried. Public agent artifacts
are reused under their declared licences — see `THIRD_PARTY.md`. `barnyard_v7`
declares no licence and lives in `opponents/unlicensed/`, out of the competitive
store.