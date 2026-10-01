# FINAL PUBLIC AGENT CATALOG

All artifacts recovered from **public Kaggle notebooks**, extracted verbatim by
`research/extract_nb.py` (never reimplemented from prose). Every competitive
agent is digest-addressed under `opponents/store/<sha16>/main.py` and registered
in `opponents/store/MANIFEST.csv`.

Verify before any tournament:

```
python benchmark/opponent_store.py verify      # unique digests + licences
python tests/test_invariants.py                # 15 harness invariants
python research/compat_linter.py               # stale-environment scan
```

| agent | author | version | date | licence | hist. score | current-env compatible | sha256 | lineage | strategy | reproduced | runtime-safe |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **farm_2945_SEATSAFE** | thomastschinkel | v9/3 (V39) | 2026-09-19 | Apache-2.0 | 2945 | yes (seat-patched) | `c936e5a71ba40e17` | thomastschinkel + yhay81 + destbreso + aurax7 + tetsutani + prvsiyan + Gluzdov + Ozer | 17 sheep + 6 cows pasture block, strawberry belt, shop-conditioned routing, 4-quadrant land, 12 hands | **yes** | yes (max 28.9ms) |
| multi_route_v43 | flexonafft | V43 | 2026-09-24 | Apache-2.0 | unknown | yes | `919fc1d61050cd96` | thomastschinkel V39 base + EXP-257/260 layers | opening funding guard, reservation (RACE), COURIER, CARROT, HERD | yes | yes |
| v38_feed | ahmedberatozer | v38 | 2026-09-12 | stated in source | unknown | yes | `a2047ebd8ca57202` | v31/v28 EXP-154/157 | smarter feed + stronger margins, v39 price model | yes | yes |
| v16_rc5 | boatlee | v16-rc5 | 2026-08-12 | stated in source | unknown | yes | `f029fa0cb66a9eb5` | — | 8 cows / 4 sheep premium market lead | yes | yes |
| shop_router | yhay81 | 0909 | 2026-09-09 | Apache-2.0 | unknown | yes | `d6d74997dc5b483d` | — | shop-pair production routing (control: never wins) | yes | yes |
| tdr_native | yhay81 | r5 (native) | 2026-10 | Apache-2.0 | unknown | **linux/mac only** | `23b0d0c93bcf3dfe` | ShopForge three-day frontier router | ctypes `agent.so` tape policy | yes | **n/a on Windows** (`WinError 193`) |
| farm_2945_ORIG | thomastschinkel | v9/3 | 2026-09-19 | Apache-2.0 | 2945 | **NO — crashes in seat 1** | `bfee70e9daaebeae` | as above | verbatim public artifact | yes | yes (seat 0 only) |
| barnyard_v7 | romanrozen | adaptive-preempt-3x2x1 | 2026-08-08 | **NONE STATED** | 3034.8 | **stale price model** | `997e6bfc5234534e` | standalone | actor-local weed repair, demand-aware SELL slots, near-clone preemption | yes | yes |
| thomas_2944 | statma | unknown | 2026-09-23 | unknown | 2944 | **no** | `dd297f8c90431e43` | standalone | — | **no** | n/a |

## Excluded and why

- **barnyard_v7** — moved to `opponents/unlicensed/`. No licence is declared
  anywhere in the notebook or source, so it cannot be redistributed or
  submitted. Retained for study only.
- **thomas_2944** — raises `RuntimeError` at import; requires notebook-local
  inputs under `\kaggle/input`. Not a legal, self-contained artifact.
- **tdr_native** — verified byte-identical to the author's manifest
  (`agent.so` sha `d3b4e19d…`, `main.py` sha `23b0d0c9…`), but the compiled
  `.so` cannot load on Windows. It is the strongest *unmeasured* candidate and
  should be evaluated on a Linux host before the next competition.

## Compatibility findings (`research/compat_linter.py`)

| agent | verdict |
|---|---|
| barnyard_v7 | **STALE_PRICE_MODEL** ×3 — CARROT below_func `log`, TOMATO/EGG `linear`; current env uses `hinge` |
| farm_2945_SEATSAFE | clean (`hinge` present, no stale tables) |
| multi_route_v43, v38_feed, v16_rc5, shop_router | no stale data detected |
| tdr_native | NATIVE_AGENT — not statically auditable |

## Seat-compatibility (the decisive finding)

The official observation schema does **not** declare `step`. The interpreter
sets `state[0].observation.step` only — player 1's observation has no `step`
key (verified directly in a downloaded Kaggle replay: P0 obs has `step`, P1 obs
does not).

`farm_2945` reads `observation["step"]` at 30 sites and therefore
**raises `KeyError` at step 0 whenever it plays seat 1** — both locally and on
Kaggle. The public artifact as published cannot fill both seats.

`research/seat_safe_patch.py` rewrites those reads to the agent's own
`_step_of()` helper (`day*24 + hour`, numerically identical because
`turnsPerDay = 24`). Verified:
- seat-0 final cash byte-identical pre/post patch on 3 seeds;
- seat 1 goes from immediate crash to normal play (wins, $190,035 / $167,698).

## Coverage gap

Six usable agents, of which **two** (`farm_2945_SEATSAFE`, `multi_route_v43`) are
credible top-meta lineages. The elite public field (top-20 ladder teams, 3050-3300)
has almost no extractable artifacts among the notebooks retrieved. A stronger
league needs Linux-hosted evaluation of the native agents and additional
notebook retrieval.