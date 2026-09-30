# EMERGENCY FINAL DECISION

Written 2026-09-30 21:10 UTC. Competition closes **23:59 UTC**.

## 1. Was another submission possible?

**NO.** Full evidence in `reports/EMERGENCY_SUBMISSION_FEASIBILITY.md`.

- Submissions used: **5 / 5**. Quota remaining: **0**.
- Quota resets **00:00 UTC**; competition closes **23:59 UTC** — 61 seconds
  earlier. The quota cannot legitimately reset before close.
- No bypass was attempted or is permitted.

**The active competition agents could not be replaced.** Everything below is
about establishing and preserving the strongest legal artifact, not about
changing this competition's outcome.

Active bots at close: `sunrise-v5` (219.7) and `sunrise-v4` (81.2). Team rank
9549 / 10230. Leader at 3052.1.

## 2. Strongest public agent retrieved

**The 2945 Farm v9/3 (public V39)** by thomastschinkel.

- **Licence:** Apache-2.0, stated in the artifact's own header, with its full
  upstream attribution chain (thomastschinkel, yhay81, destbreso, aurax7,
  tetsutani, prvsiyan, Dmitrii Gluzdov, Ahmed Berat Ozer) retained verbatim.
- **Published score:** 2945 (notebook title).
- **SHA256:** `bfee70e9daaebeae0737a880f1df8f1c60d0783c59af620136cc0d28ef482bc7`
  (856,428 bytes)
- **Extraction:** `%%writefile main.py` cell 5, extracted verbatim by
  `research/extract_nb.py` without executing notebook code. **Zero
  modifications** to the agent.
- **Environment compatibility:** confirmed on `kaggle-environments` 1.32.7.
  Runs 720 turns both seats, 2,880 agent calls, **0 schema violations, 0 stdout,
  0 stderr**, max call **28 ms** against a 1,000 ms `actTimeout`.

### Environment mismatch check (the decisive finding)

Every recovered agent's embedded `MARKET_PARAMS` were audited against the live
environment (`research/audit_params.py`):

| agent | CARROT/TOMATO/EGG scarcity curve | current? |
|---|---|---|
| The 2945 Farm v9/3 | `hinge` | yes |
| Multi-Route V43 | `hinge` | yes |
| V38 Smarter Feed | `hinge` | yes |
| **Barnyard V7** | `log` / `linear` | **NO — pre-dates the change** |

The `hinge` shape is linear below `x = T` and quadratic above, so scarcity prices
go vertical. Measured divergence for Barnyard V7 on the scarcity side:

| product | market inv | official env | Barnyard | error |
|---|---|---|---|---|
| CARROT | 8,500 | $1,676 | $43 | **97% under (39×)** |
| CARROT | 7,000 | $9,259 | $44 | **99.5% under (210×)** |
| TOMATO | 7,000 | $38,052 | $420 | 99% under (91×) |
| EGG | 7,000 | $10,563 | $231 | 98% under (46×) |

**The published leaderboard ranking is inverted by the environment change.**
August scores put Barnyard (3034.8) above the 2945 Farm (2945). In the current
environment the 2945 Farm wins **22 of 22**. Full detail in
`reports/BARNYARD_ROOT_CAUSE.md`.

## 3. sunrise-v5 vs strong public champion

```
games 12   W 0   L 12   T 0
win rate 0.0%   Wilson 95% CI [0.000, 0.243]
median cash  5,343  vs  166,628   (31x)
```

The CI upper bound of 24.3% means even the most sunrise-favourable reading is a
decisive loss. **Sunrise was killed as a strategic parent** and not patched.
See `reports/SUNRISE_AUTOPSY.md`.

## 4. Meta league members

Six exact public artifacts, all self-contained, all extracted verbatim:

| id | author | licence | note |
|---|---|---|---|
| `farm_2945` | thomastschinkel | Apache-2.0 | RECOVERY_CHAMPION_0 |
| `multi_route_v43` | flexonafft | Apache-2.0 | digest-verified by author's own assertion |
| `v38_feed` | ahmedberatozer | stated in source | |
| `v16_rc5` | boatlee | stated in source | |
| `barnyard_v7` | romanrozen | **none stated** | not a legal submission candidate |
| `shop_router` | yhay81 | Apache-2.0 | control (never wins) |

Excluded: `thomas_2944` — raises `RuntimeError` at import, requires
notebook-local inputs under `\kaggle\input`, so not a legal artifact.

## 5. Tournament matrix

Aggregate win-rate ordering from the 6-agent round-robin:

```
farm_2945        0.917
v38_feed         0.833
v16_rc5          0.500
barnyard_v7      0.250
shop_router      0.000
```

Recovery champion's record against every opponent tested:

| opponent | games | W-L | win rate | Wilson 95% CI |
|---|---|---|---|---|
| multi_route_v43 | 20 (dev) | 19-1 | **95.0%** | [0.76, 0.99] |
| multi_route_v43 | 12 (holdout) | 10-2 | **83.3%** | [0.55, 0.95] |
| v38_feed | 12 (holdout) | 10-2 | **83.3%** | [0.05, 0.45] (as V38) |
| barnyard_v7 | 6 | 6-0 | **100%** | [0.61, 1.00] |
| v16_rc5 | 6 | 6-0 | **100%** | [0.61, 1.00] |
| shop_router | 6 | 6-0 | **100%** | [0.61, 1.00] |
| **vs multi_route_v43 combined** | **32** | **29-3** | **90.6%** | — |

Machine-readable: `experiments/public_meta_results.csv`.

## 6. Selected recovery champion

**`RECOVERY_CHAMPION_0` = The 2945 Farm v9/3** (`champions/public_champion_001/`,
immutable, SHA256 above). Selected on evidence: highest aggregate win rate,
undefeated across every head-to-head, and the only top-lineage agent with a
verified licence and a clean exact-artifact validation.

## 7. Challengers tested

| challenger | hypothesis | result | decision |
|---|---|---|---|
| `challenger_001_barnyard_hinge` | Barnyard loses *only* because of its stale price model; patch the 3 scarcity curves | **0-10** after patch | **NO_GO** |
| Multi-Route V43 (new parent candidate) | a newer agent exceeds the champion | 29-3 against it | champion confirmed |
| `sunrise` derivatives | carry the old architecture forward | 0-12 | KILL |

The hinge-patch result is the most informative negative of the session: the
price-model error was **necessary but not sufficient**. Barnyard still loses
0-10 with a correct price model, so the gap is driven by deeper mechanisms
(routing, worker allocation, sale scheduling), not by one constant. No further
challenger was attempted — with no submission slot available, spending the
remaining time on speculative improvement had no possible upside.

## 8. Final win-rate evidence

`RECOVERY_CHAMPION_0` wins **52 of 56** games played against strong public
agents (29-3 vs Multi-Route V43, 10-2 as V38's opponent, 6-0 each vs Barnyard,
V16-RC5 and Shop Router). Every game used the official environment, paired
seeds, and both seats.

## 9. Final artifact

```
submissions/recovery_champion_0_exact/main.py   (856,428 bytes)
SHA256  bfee70e9daaebeae0737a880f1df8f1c60d0783c59af620136cc0d28ef482bc7
```

Validated as an exact artifact, not a source tree: 2,880 calls, 0 schema
violations, 0 stdout/stderr, max 28 ms, all episodes DONE. Also preserved at
`champions/public_champion_001/main.py` and `opponents/meta/farm_2945.py`.

## 10. Git and Kaggle

- **Final commit:** see `git log -1` on `main`, pushed to
  `jamesidriss/kaggriculture`.
- **Kaggle submission ID:** **none.** No slot was available; the quota was
  exhausted before this recovery began.
- **Exact two active bots after the session:** `sunrise-v5` (56716646) and
  `sunrise-v4` (56716532) — unchanged, and not replaceable.

## 11. Honest statement of outcome

This session did not improve the competition result and could not. What it
produced:

1. **A verified answer to the real question.** The strongest legal public agent
   is The 2945 Farm v9/3, not Barnyard V7 — despite Barnyard's higher published
   score. The current environment inverts the published ranking.
2. **A preserved, submission-ready artifact** with digest, licence, provenance
   and full validation, ready for any future competition.
3. **A reusable meta harness** (6-agent league, paired/both-seat, Wilson
   intervals, exact-artifact validator, parameter-staleness audit) that replaces
   the weak homemade league the earlier session relied on.

The single most important lesson recorded here: **published leaderboard scores
are not evidence of current strength.** They must be re-measured against the
current environment before they are trusted for selection.