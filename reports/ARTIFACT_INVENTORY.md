# ARTIFACT INVENTORY

Recalculated digests at audit time (2026-10-02). Everything is verifiable with:

```
python benchmark/opponent_store.py verify
python tests/test_audit_regressions.py
```

## Reference champions

| role | file | sha256 | immutable | notes |
|---|---|---|---|---|
| **postmortem_champion_000** | `postmortem_champion_000/main.py` | `c1e3590d02e42d16091c5377e87a3db16496e5a462d558dc2925887f835f9891` | yes | ahmedberatozer-v51-lean-flock, Apache-2.0, **verbatim**, 461,739 bytes |
| retired candidate | `postmortem_champion/main.py` | `c936e5a71ba40e1700ca1ab3a3271132407446bbb8b7523ced2cf4450ed8463f` | yes | farm_2945 + seat patch; patch now **retracted**, kept for the record |
| challenger | `challengers/challenger_001_farm2945_seatsafe.py` | `c936e5a71ba40e1700ca1ab3a3271132407446bbb8b7523ced2cf4450ed8463f` | yes | the retracted patch |

## Original (verbatim) competition submissions

| agent | path | sha256 |
|---|---|---|
| sunrise-v4 | `champions/champion_000/main.py` | `4838f8f05b44975b783653b6f69fb6bea8f01ae3a69a81d962be5d7b3ead8f13` |
| sunrise-v5 | `champions/champion_001/main.py` | `97ede93268ce2deacc1010005c1d28775c777f3b83a670f25b6c3ff6a8ffd53d` |
| sunrise-v5 (working copy) | `main.py` | `97ede93268ce2deacc1010005c1d28775c777f3b83a670f25b6c3ff6a8ffd53d` |

## Public artifacts (all Apache-2.0 except where noted)

| agent | author | license | sha256 | path |
|---|---|---|---|---|
| farm_2945_original | thomastschinkel | Apache-2.0 | `bfee70e9daaebeae0737a880f1df8f1c60d0783c59af620136cc0d28ef482bc7` | `opponents/meta/farm_2945_original.py` |
| farm_2945_seatsafe (patched) | thomastschinkel | Apache-2.0 | `c936e5a71ba40e1700ca1ab3a3271132407446bbb8b7523ced2cf4450ed8463f` | `opponents/meta/farm_2945_patched.py` |
| v43 recovering-lost-harvests | ahmedberatozer | Apache-2.0 | `919fc1d61050cd96f799979e49177ae3ac7bce98ec9835724238bea73f4a08ed` | `opponents/meta/ahmedberatozer-v43-…py` |
| v44 same-turn-sale-race | ahmedberatozer | Apache-2.0 | `797d9bca309d481e…` | `opponents/meta/…` |
| v46 first-turn-microstructure | ahmedberatozer | Apache-2.0 | `735c370383b70d3b…` | `opponents/meta/…` |
| v48 clear-the-queue | ahmedberatozer | Apache-2.0 | `4b5402888feeb417…` | `opponents/meta/…` |
| v49 funded-sale-timing | ahmedberatozer | Apache-2.0 | `ed89be8cd96fe58e…` | `opponents/meta/…` |
| v50 early-yarn-commit | ahmedberatozer | Apache-2.0 | `044a26601be23816…` | `opponents/meta/…` |
| **v51 lean-flock (CHAMPION)** | ahmedberatozer | Apache-2.0 | `c1e3590d02e42d16…` | `opponents/meta/…` |
| v38 smarter-feed | ahmedberatozer | stated | `a2047ebd8ca57202…` | `opponents/meta/v38_feed.py` |
| v16-rc5 8C/4S | boatlee | stated | `f029fa0cb66a9eb5…` | `opponents/meta/v16_rc5.py` |
| shop-router-0909 | yhay81 | Apache-2.0 | `d6d74997dc5b483d…` | `opponents/meta/shop_router.py` |
| three-day shop router (native) | yhay81 | Apache-2.0 | `23b0d0c93bcf3dfe…` | `opponents/store/23b0d0c93bcf3dfe/` |
| barnyard_v7 | romanrozen | **NONE STATED** | `997e6bfc5234534e…` | `opponents/unlicensed/` |
| thomas_2944 | statma | unknown | `dd297f8c90431e43…` | excluded: not self-contained |

**Important attribution correction.** The agent previously labelled
`multi_route_v43` and attributed to *flexonafft* is byte-identical
(sha256 `919fc1d6…`) to `ahmedberatozer-v43-recovering-lost-harvests`. It is
ahmedberatozer's v43. The donor-pack provenance is authoritative; the earlier
attribution was wrong. `opponents/store/` keys by digest, so the duplicate was
automatically merged rather than counted twice.

## Harness artifacts

| file | sha256 | role |
|---|---|---|
| `benchmark/meta.py` | `36657c9912845d558d8fe6bc974d7c2ecfb779b0423c4563be69e991bb605629` (pre-audit) | paired both-seat harness, self-play guard |
| `benchmark/validate_artifact.py` | — | exact-artifact gate (**corrected to `env.run`** this session) |
| `benchmark/opponent_store.py` | — | digest-addressed store + manifest |
| `benchmark/sync_league.py` | — | derives `opponents/meta` from the manifest |
| `benchmark/build_splits.py` | — | audited, sealed seed splits |
| `tools/probe_observations.py` | — | runtime parity probe |
| `tools/locate_divergence.py` | — | pins the snapshot-vs-delivery divergence |
| `tools/verify_both_seats.py` | — | proves verbatim artifact runs both seats |

## Seed splits (sealed before evaluation)

| file | n | sha256 |
|---|---|---|
| `seeds/REAL_dev.txt` | 12 | `92bc611ee24bf1db…` |
| `seeds/REAL_holdout.txt` | 12 | `8c1341e4dbfacb57…` |
| `seeds/REAL_final.txt` | 12 | `f4057aa5ed7490a4…` |

Source: public replay database `xishengfeng/kaggriculture-replay-db`
(88,281 episodes, 0 duplicate ids, 24,548 with both players rated ≥2900).
Disjointness asserted by `tests/test_audit_regressions.py`.