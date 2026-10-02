# OPTIMAL FINAL PAIR — parity- and signature-safe revision

Third revision. Both earlier versions are void:

- the first was written before the runtime-parity audit, and recommended a
  **patched** artifact whose patch was unnecessary;
- the second was written after parity but before the signature audit, and
  recommended two agents on the strength of results in which three of the
  league members — including the hedge's own comparison baseline — were never
  actually playing.

Kaggle submissions are closed (`400 FAILED_PRECONDITION`, verified once at
audit time), so this records the decision that should have been made, not an
action taken.

## PRIMARY

**`ahmedberatozer-v51-lean-flock`**

| | |
|---|---|
| Artifact | `postmortem_champion_000/main.py` |
| SHA256 | `c1e3590d02e42d16091c5377e87a3db16496e5a462d558dc2925887f835f9891` |
| Size | 461,739 bytes |
| Licence | Apache-2.0 |
| Author | ahmedberatozer |
| Source | Kaggle dataset `destbreso/kaggriculture-donor-agents-20260902`, `agents/ahmedberatozer-v51-lean-flock.py` |
| Modifications | **none** — byte-identical to the published artifact |

**Evidence.** 670-50 over 720 parity-correct games against 10 distinct public
agents — 93.06%, Wilson 95% **[0.9096, 0.9469]**, 0 errors, both seats, real
ladder seeds, official `Environment.run`, verified 719 agent turns per game.

| pool | record |
|---|---|
| REAL_dev (12 seeds) | 224-16 |
| REAL_holdout (12 seeds) | 214-26 |
| REAL_final (12 seeds, sealed before evaluation, run once) | 232-8 |

Artifact gate: 2,880 calls, 0 schema violations, both seats, full 720-turn
episodes, no stdout, no stderr, max 33.1 ms against a 1000 ms `actTimeout`.

## HEDGE

**`farm_2945_original`** — The 2945 Farm v9/3

| | |
|---|---|
| Artifact | `opponents/meta/farm_2945_original.py` |
| SHA256 | `bfee70e9daaebeae0737a880f1df8f1c60d0783c59af620136cc0d28ef482bc7` |
| Licence | Apache-2.0, upstream attribution retained in-file |
| Author | thomastschinkel |
| Source | `kaggle.com/code/thomastschinkel/the-2945-farm-96-vs-the-top-10-public-bots` |
| Modifications | **none** — the verbatim artifact |

**Evidence.** 596-124 over 720 games, 82.78%, Wilson [0.7985, 0.8536], 0
errors. It is the only agent in the league that v51 does not decisively beat.

### Honest statement about the hedge's strength

**v51 and farm_2945 are statistically tied.** The direct comparison over 144
paired games is **76-68 to v51 — 52.78%, Wilson 95% [0.3925, 0.5534]**. The
interval comfortably straddles 50%.

v51 is still the right PRIMARY, and the reasoning is stated rather than hidden:

- higher aggregate against the same league (93.06% vs 82.78%, non-overlapping
  intervals);
- it beats v49/v50 decisively, 64-8, where farm_2945 ties them at 38-34 — and
  v49/v50 are the only other agents near the top.

But this is a **preference on indirect evidence, not a measured superiority**.
The hedge is genuinely competitive, which is exactly what makes it a hedge.

### Why this is a real hedge and not a near-duplicate

Different lineage, different portfolio, different labour and market cadence:

| | v51 | farm_2945 |
|---|---|---|
| end-of-season farm | lean flock | 17 sheep + 6 cows, strawberry belt |
| total market orders / 4 games | 3,618 | 7,684 |
| SELL orders | 1,450 | 3,382 |
| HIRE orders | 1,064 | 2,130 |
| cash per field action | $5.64 | $5.58 |
| hands mean / max | 8.6 / 12 | 8.6 / 12 |

They differ on sale volume, labour cadence and portfolio, and they split their
mutual games almost evenly.

## Rejected, with reasons

| candidate | reason |
|---|---|
| sunrise-v5 / v4 | **0 for 792**, Wilson upper bound 0.48%. $0.19 cash per field action against $5.64; 63% of actions spent moving; 0-264 in every pool |
| `barnyard_v7` | **no licence declared** by the author, so not usable; separately, it genuinely loses 0-144 to the two hubs |
| `shop_router` | **not self-contained** — raises `FileNotFoundError` for `actions.json` on turn 1; that file is not in the public notebook. It was also a phantom $3,000 victim before the signature fix |
| `ahmedberatozer` v49 / v50 | tie farm_2945 38-34, lose 8-64 to v51, and are **the same agent** — 24/24 exact ties against each other. One lineage, not two |
| `ahmedberatozer` v43 / v44 / v46 / v48 | 0-72 to v51 and 0-144 to the hubs |
| `v16_rc5` | 0-144 to the hubs. A genuine agent — $138,247 vs `starter` — but clearly below the top tier |
| `thomas_2944` | not self-contained; `RuntimeError` at import, needs `\kaggle\input` |
| three-day shop router (native) | `agent.so` is Linux/macOS only; `WinError 193` on this host, so unevaluable |
| the seat-patched farm_2945 | patch is **retracted**; the verbatim artifact is correct and is the artifact recorded above |
| farm_2945 + hinge-price patch | the patched price table is **unreachable code**; the counterfactual changed the result by exactly $0 across 24 games |

## What changed across the three revisions

| | rev 1 | rev 2 | rev 3 (this) |
|---|---|---|---|
| primary | farm_2945, seat-patched | v51, verbatim | v51, verbatim |
| hedge | multi_route v43 | farm_2945, verbatim | farm_2945, verbatim |
| basis | 300-0 vs 5 weak agents | 742-50 vs 11 agents, 3 sealed pools | **670-50 vs 10 agents, 3 sealed pools, 0 phantom opponents** |
| top-two claim | "farm_2945 wins" | "v51 wins" | **"v51 and farm_2945 are tied; v51 preferred on indirect evidence"** |
| league lineages | 2 | 5 | 4 (7 of 10 agents are one author's series) |

Three reasons for the final revision: the strengthened league showed farm_2945
was not dominant; the runtime-parity audit showed the seat patch was
unnecessary; and the signature audit removed three phantom opponents and
revealed that a fitted BT ranking was not identifiable for this league.

## Counterfactual placement — calibrated

**Not** claiming #1 of 10,246, and not claiming a Kaggle rating.

- Our submitted pair finished at 348.1 (v1) down to 138.5 (v4); the leader was
  3052.1, so we were ~2,700 points off the top.
- This pair finishes at **$158k-$183k median** on real ladder seeds and on
  `starter`. Elite games in the public replay index (both players rated 2900+)
  end between roughly $64k and $158k.
- Therefore: **this pair is competitive with 2800-3000-level agents** and is
  above every other agent we can legally obtain and reproduce.
- Whether that is **#1 is not established.** The league contains two credible
  top lineages and the elite public field has almost no extractable artifacts;
  7 of our 10 eligible agents are a single author's incremental series, which is
  not a diverse field.
- Costs avoided: rev 1 would have submitted a **patched** artifact carrying an
  unnecessary 30-site edit; rev 2 rested on a league containing two agents that
  never played.
