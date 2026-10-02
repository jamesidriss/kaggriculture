# LOCAL BRADLEY-TERRY — PARITY-SAFE

Offline estimate. **Not** an official Kaggle ranking. Fitted only from
parity-corrected games: official `env.run()` delivery, both seats, real ladder
seeds, unique digests, no self-play, no error rows.

Candidate: `ahmedberatozer-v51-lean-flock`. Games: 792 (33 opponents × 24
paired games) across `REAL_dev` / `REAL_holdout` / `REAL_final`.

| agent | beta | P(vs league average) |
|---|---|---|
| **ahmedberatozer-v51-lean-flock** | **57.667** | 1.000 |
| farm_2945_original | 24.212 | 1.000 |
| ahmedberatozer-v49-funded-sale-timing | −1.788 | 0.143 |
| ahmedberatozer-v50-early-yarn-commit | −1.788 | 0.143 |
| ahmedberatozer-v43-recovering-lost-harvests | −9.788 | 0.000 |
| ahmedberatozer-v44-winning-the-same-turn-sale-race | −9.788 | 0.000 |
| ahmedberatozer-v46-first-turn-microstructure | −9.788 | 0.000 |
| ahmedberatozer-v48-clear-the-queue | −9.788 | 0.000 |
| barnyard_v7 | −9.788 | 0.000 |
| shop_router | −9.788 | 0.000 |
| v16_rc5 | −9.788 | 0.000 |
| v38_feed | −9.788 | 0.000 |

## Observed win rates (not model output)

| opponent | dev | holdout | final |
|---|---|---|---|
| v43 recovering-lost-harvests | 24-0 | 24-0 | 24-0 |
| v44 same-turn-sale-race | 24-0 | 24-0 | 24-0 |
| v46 first-turn-microstructure | 24-0 | 24-0 | 24-0 |
| v48 clear-the-queue | 24-0 | 24-0 | 24-0 |
| v49 funded-sale-timing | 22-2 | 18-6 | 24-0 |
| v50 early-yarn-commit | 22-2 | 18-6 | 24-0 |
| **farm_2945_original** | **12-12** | **10-14** | **16-8** |
| barnyard_v7 | 24-0 | 24-0 | 24-0 |
| shop_router | 24-0 | 24-0 | 24-0 |
| v16_rc5 | 24-0 | 24-0 | 24-0 |
| v38_feed | 24-0 | 24-0 | 24-0 |
| **overall** | **248-16** | **238-26** | **256-8** |

Aggregate 742-50, **93.68% observed**, Wilson 95% [0.918, 0.951].

## Uncertainty and known limits

- **The betas are not calibrated to Kaggle ratings.** They order *this* league.
  `v51` and `farm_2945` are separated by 33 beta units, but their observed
  head-to-head is only 38-34 across 72 games (52.8%, Wilson [0.41, 0.65]). The
  model exaggerates that gap because the other ten opponents are far weaker and
  dominate the likelihood.
- **Only two agents are genuinely close.** v51 and farm_2945 are separated by
  three opponents, not by thirty-three rating points of real strength.
- **Ten of twelve league members never beat v51**, so the bottom of the scale is
  degenerate: every undefeated opponent lands on the same beta. Those entries
  carry no information.
- **v49 and v50 are effectively one agent** — 24/24 exact ties against each
  other. They are a single lineage counted twice.
- The model is fitted to a champion-vs-league sweep, not a full round robin, so
  pairwise betas between two *opponents* are not identified by these data.

## What this does establish

1. `v51` and `farm_2945` are the only two agents that beat each other at all.
2. `farm_2945` is **not** the strongest reproduced agent: v51 beats it 38-34
   observed, 52.8% Wilson [0.41, 0.65].
3. Everything else in the league is decisively weaker.

Reproduce: `python benchmark/bt_from_sweep.py <result.json...> --candidate <name>`