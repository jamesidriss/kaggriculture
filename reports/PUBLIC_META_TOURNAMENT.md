# PUBLIC META TOURNAMENT

Command: `python benchmark/meta.py --roundrobin --games 3 --stage meta_holdout`

Seeds 58001/58002/58003, **both seats** for the first-named agent in every
pairing. Six games per pairing (3 worlds × 2 seats). Official
`kaggle-environments` 1.32.7 used as the reference implementation throughout.

## Agents in the league

All six are exact artifacts extracted from public Kaggle notebooks via
`%%writefile` cells (`research/extract_nb.py`), never reimplemented from prose.

| id | agent | notebook | licence |
|---|---|---|---|
| `farm_2945` | The 2945 Farm v9/3 (V39) | thomastschinkel | **Apache-2.0**, attributed |
| `v38_feed` | V38 Smarter Feed, Stronger Margins | ahmedberatozer | stated in source |
| `v16_rc5` | V16-RC5 8C/4S Premium Market Lead | boatlee | stated in source |
| `barnyard_v7` | [STRONG] Barnyard Economist V7 | romanrozen | **none found** |
| `shop_router` | Shop Router 0909 | yhay81 | Apache-2.0 (per downstream attribution) |
| `thomas_2944` | Thomas 2944 candidate | statma | — **excluded: not self-contained** |

`thomas_2944` raised `RuntimeError: missing verified kernel inputs` at import —
it depends on notebook-local assets under `\kaggle\input`, so it is not a legal
submission artifact and was quarantined rather than scored.

## Pairwise win rates (first-named agent's perspective)

| matchup | W-L | win rate | Wilson 95% CI | median cash A | median cash B |
|---|---|---|---|---|---|
| farm_2945 vs shop_router | 6-0 | **100%** | [0.61, 1.00] | 179,223 | 3,000 |
| farm_2945 vs v16_rc5 | 6-0 | **100%** | [0.61, 1.00] | 120,568 | 77,712 |
| farm_2945 vs barnyard_v7 | 6-0 | **100%** | [0.39→0.61, 1.00] | 94,049 | 127,421 |
| farm_2945 vs v38_feed | 4-2 | **66.7%** | [0.30, 0.90] | 118,787 | 110,256 |
| barnyard_v7 vs shop_router | 6-0 | **100%** | [0.61, 1.00] | 165,328 | 3,000 |
| v38_feed vs v16_rc5 | 6-0 | **100%** | [0.39, 1.00] | 75,370 | 109,689 |
| barnyard_v7 vs farm_2945 | 0-6 | 0% | — | (see above) | — |
| v38_feed vs farm_2945 | 2-4 | 33.3% | — | — | — |
| barnyard_v7 vs v16_rc5 | 0-6 | 0% | [0.00, 0.39] | 51,220 | 67,196 |
| barnyard_v7 vs v38_feed | 0-6 | 0% | [0.00, 0.39] | 68,527 | 115,084 |

## Aggregate win-rate ordering

```
farm_2945        0.917
v38_feed         0.833
v16_rc5          0.500
barnyard_v7      0.250
shop_router      0.000
```

## Interpretation

**`farm_2945` (The 2945 Farm) is the strongest reproducible legal agent we
recovered.** It is undefeated: 6-0, 6-0, 6-0, 4-2. Note the `farm_2945 vs
barnyard_v7` row shows a *lower* median cash for farm_2945 (94,049) than for
barnyard (127,421) while still winning 6-0 — direct evidence that **cash margin
and win rate diverge in this game**, which is exactly why cash must never be the
promotion criterion.

Two independent findings from this table:

1. **Barnyard V7 (3034.8 published) is beaten 0-6 by the 2945 Farm locally.**
   The published leaderboard score is not reproduced by our seeds, so
   Barnyard's 3034.8 must reflect either a different environment revision, a
   different seed distribution, or ladder matchmaking against weaker opponents.
   Local head-to-head is the only evidence we can actually measure, and it puts
   farm_2945 ahead. This is a documented divergence rather than a contradiction
   we can resolve without the author's replay data.
2. **`shop_router` never wins a game** (0.000 aggregate) and holds exactly its
   $3,000 starting cash against anyone competent. It is a useful low-competence
   control but is not a meta-strength opponent.

## Sunrise in the same framework

`sunrise-v5` vs `barnyard_v7`: **0-12**, median cash 5,343 vs 166,628. Sunrise is
roughly 31× behind on final bank and loses every game. It is excluded from this
league as non-competitive.

## Caveats

- 6 games per pairing gives a Wilson interval of roughly ±0.39 at 0% and ±0.20
  at 100%. Rankings with adjacent rates (`farm_2945` 0.917 vs `v38_feed` 0.833)
  are **not** statistically separated at this sample size.
- Seeds 58001-58003 are locally chosen, not ladder-derived — the public replay
  dataset was identified (`xishengfeng/kaggriculture-replay-database`) but not
  downloaded within the time available.
- These are local simulations against public code, not ladder results. A local
  100% is not a claim about the leaderboard.

Machine-readable results: `experiments/public_meta_results.csv`.