# ARTIFACT INVENTORY

Digests recalculated at audit time (2026-10-02) and checked by
`tests/test_audit_regressions.py` (26/26). League integrity:

```
python benchmark/opponent_store.py verify    # digest-addressed store
python benchmark/league_manifest.py           # league provenance
python benchmark/agent_loader.py              # shared, correct agent loader
python -m simcomp.selftest                    # framework self-test
```

## Reference champion

| role | file | sha256 | immutable | notes |
|---|---|---|---|---|
| **postmortem_champion_000** | `postmortem_champion_000/main.py` | `c1e3590d02e42d16091c5377e87a3db16496e5a462d558dc2925887f835f9891` | yes | `ahmedberatozer-v51-lean-flock`, Apache-2.0, **verbatim**, 461,739 B, 2-arg |
| retired candidate | `postmortem_champion/main.py` | `c936e5a71ba40e1700ca1ab3a3271132407446bbb8b7523ced2cf4450ed8463f` | yes | farm_2945 + seat patch. **Patch retracted** — kept only for the record |
| challenger | `challengers/challenger_001_farm2945_seatsafe.py` | `c936e5a71ba40e1700ca1ab3a3271132407446bbb8b7523ced2cf4450ed8463f` | yes | the retracted patch |

## Our competition submissions (all `def agent(obs)`, 1-argument)

| bot | file | sha256 | ladder score |
|---|---|---|---|
| sunrise-v1 | *(git history, pre-`champion_000`)* | — | 348.1 |
| sunrise-v2 | *(git history)* | — | 322.0 |
| sunrise-v3 | *(git history)* | — | 316.8 |
| sunrise-v5 | `champions/champion_001/main.py` | `97ede93268ce2deacc1010005c1d28775c777f3b83a670f25b6c3ff6a8ffd53d` | 252.6 |
| sunrise-v4 | `champions/champion_000/main.py` | `4838f8f05b44975b783653b6f69fb6bea8f01ae3a69a81d962be5d7b3ead8f13` | 138.5 |
| sunrise-v5 (working copy) | `main.py` | `97ede93268ce2deacc1010005c1d28775c777f3b83a670f25b6c3ff6a8ffd53d` | — |

These are 1-argument agents, which is why they were silently never played by the
pre-audit harness. See `reports/HARNESS_SIGNATURE_AUDIT.md`.

## League — `opponents/meta/` (10 eligible, 1 withheld)

Authoritative record: `opponents/meta/MANIFEST.csv`.

| agent | author | licence | verbatim | arity | plays? | sha256 |
|---|---|---|---|---|---|---|
| ahmedberatozer-v43-recovering-lost-harvests | ahmedberatozer | Apache-2.0 | yes | 2 | yes | `919fc1d61050cd96…` |
| ahmedberatozer-v44-winning-the-same-turn-sale-race | ahmedberatozer | Apache-2.0 | yes | 2 | yes | `797d9bca309d481e…` |
| ahmedberatozer-v46-first-turn-microstructure | ahmedberatozer | Apache-2.0 | yes | 2 | yes | `735c370383b70d3b…` |
| ahmedberatozer-v48-clear-the-queue | ahmedberatozer | Apache-2.0 | yes | 2 | yes | `4b5402888feeb417…` |
| ahmedberatozer-v49-funded-sale-timing | ahmedberatozer | Apache-2.0 | yes | 2 | yes | `ed89be8cd96fe58e…` |
| ahmedberatozer-v50-early-yarn-commit | ahmedberatozer | Apache-2.0 | yes | 2 | yes | `044a26601be23816…` |
| **ahmedberatozer-v51-lean-flock (CHAMPION)** | ahmedberatozer | Apache-2.0 | yes | 2 | yes | `c1e3590d02e42d16…` |
| **farm_2945_original** | thomastschinkel | Apache-2.0 | yes | 2 | yes | `bfee70e9daaebeae…` |
| barnyard_v7 | romanrozen | **NONE STATED** | yes | **1** | yes | `997e6bfc5234534e…` |
| v16_rc5 | boatlee | stated in source | yes | **1** | yes | `f029fa0cb66a9eb5…` |
| v38_feed | ahmedberatozer | stated in source | yes | 2 | yes | `a2047ebd8ca57202…` |
| shop_router | yhay81 | Apache-2.0 | yes | 2 | **NO** | `d6d74997dc5b483d…` |

Lineages: 4 (seven agents are one author's incremental v27→v51 series).

### Withheld, with reasons recorded in the manifest

| agent | reason |
|---|---|
| shop_router | **NOT_SELF_CONTAINED** — `FileNotFoundError: actions.json` on turn 1; that file is not in the public notebook. Was also a phantom $3,000 victim. → `opponents/unlicensed/` |
| barnyard_v7 | **UNKNOWN_LICENSE** — no licence declared. Retained for analysis only; excluded from competitive use |
| thomas_2944 | **NOT_SELF_CONTAINED** — `RuntimeError` at import, needs `\kaggle\input` |
| three-day shop router (native) | **PLATFORM** — `agent.so` is Linux/macOS only; `WinError 193` on this host; unevaluable |

## Attribution correction

The agent previously labelled `multi_route_v43` and attributed to *flexonafft* is
byte-identical (`919fc1d61050cd96…`) to `ahmedberatozer-v43-recovering-lost-harvests`.
It is ahmedberatozer's v43. The donor-pack provenance is authoritative; the
earlier attribution was wrong. The digest-addressed store merged it
automatically rather than counting one agent twice.

## Counterfactual artifacts

| file | sha256 | purpose |
|---|---|---|
| `counterfactuals/barnyard_v7_pricefixed.py` | see `git hash-object` | CARROT/TOMATO/EGG `log`/`linear` → `hinge`. Result: **$74,991 → $74,991**, identical. The patched table is unreachable code |

## Harness

| file | role |
|---|---|
| `benchmark/agent_loader.py` | **the single correct agent loader**; signature adaptation + `probe_playable()` |
| `benchmark/meta.py` | paired both-seat harness, self-play guard, self-describing result envelopes, non-player guard |
| `benchmark/validate_artifact.py` | exact-artifact gate (corrected to `env.run`) |
| `benchmark/collect_results.py` | builds the results CSV from real run JSON; refuses non-self-describing envelopes |
| `benchmark/league_table.py` | definitive aggregation, digest-keyed identity, Wilson on everything, BT-or-why-not |
| `benchmark/league_manifest.py` | `opponents/meta/MANIFEST.csv` provenance record |
| `benchmark/build_splits.py` | audited, sealed seed splits |
| `benchmark/opponent_store.py` | digest-addressed store |
| `benchmark/sync_league.py` | derives `opponents/meta` from `MANIFEST.csv` |
| `benchmark/stats.py` | re-export of `simcomp.stats` (one implementation) |
| `benchmark/action_economy.py` | signature-adapted; action taxonomy forensics |
| `simcomp/` | reusable framework (registry, seeds, league, stats, parity, selftest) |
| `tools/probe_observations.py` | runtime parity probe |
| `tools/locate_divergence.py` | pins the delivered-vs-persisted divergence |
| `tools/verify_both_seats.py` | proves the verbatim artifact runs both seats |

## Seed splits (sealed before evaluation)

| file | n | sha256 |
|---|---|---|
| `seeds/REAL_dev.txt` | 12 | `92bc611ee24bf1db…` |
| `seeds/REAL_holdout.txt` | 12 | `8c1341e4dbfacb57…` |
| `seeds/REAL_final.txt` | 12 | `f4057aa5ed7490a4…` |

Source: public replay database `xishengfeng/kaggriculture-replay-db` — 88,281
episodes, 0 duplicate ids, 24,548 with both players rated ≥2900, all sampled
games on the stock configuration. Splits assigned by SHA256 of the seed, so
they are reproducible and not cherry-picked. Disjointness asserted by the
regression suite.
