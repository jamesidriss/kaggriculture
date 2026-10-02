# LOCAL BRADLEY-TERRY — corrected, and the ranking is WITHDRAWN

**Supersedes the previous version of this report, which published a beta
ranking that does not exist.**

## The result: no BT ranking is reportable for this league

`benchmark/league_table.py` attempts the fit and refuses:

```
NO BRADLEY-TERRY RANKING IS REPORTABLE FOR THIS LEAGUE.

Unbounded likelihood: these agents lose EVERY game to EVERY opponent they were
measured against, so their maximum-likelihood strength is -infinity and the
model has no finite solution:
  ahmedberatozer-v43-recovering-lost-harvests   record 0-144 (0 wins)
  barnyard_v7                                   record 0-144 (0 wins)
  v16_rc5                                       record 0-144 (0 wins)
  v38_feed                                      record 0-144 (0 wins)
```

This is not a numerical accident. The maximum-likelihood strength of an agent
that never wins is unbounded below, so the log-likelihood has no maximum and no
finite optimum exists. Any "beta" printed for such an agent is decided entirely
by where the iteration happened to stop.

The previous report published betas of `17.758`, `5.424`, `-2.576`, `-9.788`.
Those were the output of a fixed 400-iteration loop that had not converged,
presented as a ranking. The identical value `-9.788` for six different agents
was the visible symptom and it was read as "the bottom of the scale is
degenerate" rather than "this number is meaningless."

## Why the league has this shape

It is a two-tier star, and that is a consequence of how the tournament was run:

```
                 v51  <-- hub, played all 10 others
                  |
   v43  v44  v46  v48  v49  v50  barnyard  v16  v38
                  |
      farm_2945  <-- hub, played all 10 others
```

The bottom tier only ever meets the two hubs. A scalar rating cannot order a
tier that is uniformly dominated by the same two agents, and the hubs' mutual
result is a coin flip, so the whole graph is one rank short of informative.

## What to use instead: the observed head-to-heads

The measurement is the head-to-head table with its intervals. From
`reports/LEAGUE_TABLE.txt`:

| A | B | record | n | win% | Wilson 95% | separable? |
|---|---|---|---|---|---|---|
| v51 | farm_2945 | 76-68 | 144 | 52.78% | [0.3925, 0.5534] | **NO** |
| v49 | farm_2945 | 38-34 | 72 | 52.78% | [0.4140, 0.6387] | **NO** |
| v50 | farm_2945 | 38-34 | 72 | 52.78% | [0.4140, 0.6387] | **NO** |
| v51 | v49 | 64-8 | 72 | 88.89% | [0.7958, 0.9494] | yes |
| v51 | v50 | 64-8 | 72 | 88.89% | [0.7958, 0.9494] | yes |
| v51 | v43 | 72-0 | 72 | 100% | [0.9493, 1.0000] | yes |
| v51 | v44 | 72-0 | 72 | 100% | [0.9493, 1.0000] | yes |
| v51 | v46 | 72-0 | 72 | 100% | [0.9493, 1.0000] | yes |
| v51 | v48 | 72-0 | 72 | 100% | [0.9493, 1.0000] | yes |
| v51 | barnyard_v7 | 72-0 | 72 | 100% | [0.9493, 1.0000] | yes |
| v51 | v16_rc5 | 72-0 | 72 | 100% | [0.9493, 1.0000] | yes |
| v51 | v38_feed | 72-0 | 72 | 100% | [0.9493, 1.0000] | yes |
| v51 | v49/v50 identity | 24/24 ties | 24 | — | — | same agent |

Aggregate records, which are the only summary statistics that *are* identified:

| agent | W-L-T | games | win% | Wilson 95% | verdict |
|---|---|---|---|---|---|
| **v51** | **670-50-0** | 720 | 93.06% | [0.9096, 0.9469] | stronger than the field |
| farm_2945 | 596-124-0 | 720 | 82.78% | [0.7985, 0.8536] | stronger than the field |
| sunrise-v5 | 0-792-0 | 792 | 0.00% | [0.0000, 0.0048] | weaker than the field |

## The honest ordering

There are exactly **two** tiers, and the ordering within the top tier is
**not resolved by this evidence**:

1. **Top tier — statistically tied.** `{v51, farm_2945}`. v51 leads on
   aggregate (93.06% vs 82.78%, intervals do not overlap) and beats v49/v50
   decisively (64-8) where farm ties them (38-34). But the direct comparison,
   144 paired games, is 76-68 with a Wilson interval of [0.3925, 0.5534] that
   straddles 50% comfortably. **Calling v51 "better than" farm_2945 is not
   supported.** v51 is the pick, on the strength of the aggregate and the v49
   result, and that reasoning is stated rather than hidden behind a beta.

2. **Second tier — one lineage, tied with the top on the one thing measured.**
   `{v49, v50}` are byte-different files that play *identically* (24/24 exact
   ties). Each ties farm_2945 (38-34) and loses 8-64 to v51. Two files, one
   agent.

3. **Bottom tier — uniformly dominated, ordering not determined.**
   `{v43, v44, v46, v48, barnyard_v7, v16_rc5, v38_feed}`. Each is 0-144 against
   the two hubs. They are separated from the top tier beyond doubt and from each
   other not at all — they have never been played against each other. A
   round-robin among them would be the next useful measurement.

4. **sunrise-v5 — 0 for 792**, Wilson upper bound 0.48%.

## Method notes

- Fitted only from parity-corrected games: official `Environment.run`
  delivery, adapted agent signatures, both seats, real ladder seeds, unique
  content digests, no self-play, no error rows, no ties.
- **Identity is the content digest**, never the label. The same agent appears as
  `v51` when it is the candidate and `ahmedberatozer-v51-lean-flock` when it is
  an opponent; keying on labels silently splits one agent into two and produced
  a nonsense matrix in an earlier version of this analysis.
- Mirrored rows (`A vs B` and `B vs A`) are the same paired games with the seats
  swapped. Each unordered pair is counted once.
- Ties are split 0.5/0.5 for modelling purposes; the 24 v49-vs-v50 ties are
  excluded entirely as a same-content signal.
- This is an **offline estimate over a self-selected league**. It is not an
  official Kaggle ranking and is not calibrated to Kaggle ratings.

Reproduce: `python benchmark/league_table.py` (writes `reports/LEAGUE_TABLE.txt`).
