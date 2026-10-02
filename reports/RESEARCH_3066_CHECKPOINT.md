# RESEARCH 3066 CHECKPOINT

Branch `research/3066-breakthrough`. Main at entry: `0d22b5dd`.

## Phase
**12 of 24 — exhaustive search stage A complete, stage B running.**
Stage B (64 survivors vs the discriminating opponents) is in flight.

## Resume procedure
```
cd C:\Users\James\kaggriculture
git checkout research/3066-breakthrough
git fetch origin && git status
Get-Content simulation\search3066_B.log -Tail 20
.venv\Scripts\python.exe policy\search\racing_search.py --stage B --workers 8
.venv\Scripts\python.exe policy\search\racing_search.py --stage C --workers 8
.venv\Scripts\python.exe pipeline\dashboard_3066.py
.venv\Scripts\python.exe tests\test_gate_3066.py
.venv\Scripts\python.exe tests\test_research_gate.py
```
Both stages checkpoint every 16 configurations into
`simulation/search3066/search_state.json`, and the match cache is keyed on
digests, so restarting costs at most 16 evaluations and completed games are free.

## Stage A result (complete)
All 512 boolean configurations enumerated. 4,104 matches, 86 min, **0 broken**.
C001 baseline scores 0.8750 and ranks first. No candidate beat it.

**The screen could not have detected a difference anyway, and that is the
finding**: at 8 matches the ceiling is 0.875, the first four dev worlds have a
ZERO tie rate where the full 992-game measurement gives 21.8% ties, and a large
number of configurations sit on the ceiling. At 8 games the score rewards
*differing* from v51 — including by breaking tie-equality — rather than being
stronger. Stage A selects for divergence. Stage B is the discriminator.

## Completed
| # | item | state |
|---|---|---|
| 1 | repo safety, branch pushed | done |
| 2 | exact-tie validity bug fixed | done, 24/24 regression |
| 3 | BT score metric + intervals | done, 46/46 selftest |
| 4 | historical results migrated | 498 games restored, 0 real defects |
| 5 | +275 claim retracted | R8 |
| 6 | shadow ladder math repaired | v2, one shift, gate in code |
| 7 | anchors recovered | official leaderboard: 745 teams; 1 class-B anchor |
| 8 | strong independent lineages | 3 new agents; `thomas` is mid-curve |
| 9 | turns populated | PENDING |
| 10 | world regimes | PENDING |
| 11 | parallel official simulation | 107 matches/min, 8 workers |
| 12 | boolean search infra | **stage A done**: all 512 enumerated, 0 broken; stage B running |
| 13 | numeric search | inventory: 0 numeric keys in the live literal; numeric reach via module constants left OPEN |
| 14 | counterfactual/close-game | NOT RUN — no budget left after the search |
| 15 | selector/value model | NOT RUN — see the imitation gate reasoning in the conclusion |
| 16 | finalist evaluation | pending stage B/C |
| 17 | sealed final | pool COMMITTED (sha 3d9869bb…), not run: no finalist beat C001 |
| 18 | shadow recalibration | WITHHELD: 1 usable anchor, gate needs 5 |
| 19 | champion freeze | C001 unchanged and immutable |
| 20 | submission_ready | frozen, digest-verified against CURRENT.json |
| 21 | tests | tie 24/24, stats 46/46, 3066 gate 116/116, research gate 112/112 |
| 22 | merge/push | pending |
| 23 | remote verify | pending |
| 24 | final report | **done** — reports/3066_RESEARCH_CONCLUSION.md |

## Key measurements (all primary metric = BT score rate (W+0.5T)/N)

| matchup | W-L-T | N | BT | 95% seed bootstrap | clears 0.50 |
|---|---|---|---|---|---|
| C001 vs v51 (parent) | — | 2000 | 0.7520 | [0.7218, 0.7812] | yes |
| C001 vs 2945 Farm | 1101-897-2 | 2000 | **0.5510** | **[0.5200, 0.5815]** | **yes** |
| C001 vs thomas.py | 290-210-0 | 500 | 0.5800 | — | — |
| C001 vs moon_q13 | 27-473-0 | 500 | 0.0540 | — | — |
| C001 vs moon_parent | 27-473-0 | 500 | 0.0540 | — | — |

Seat balance on the Farm leg: P0 552/447, P1 549/450. Mean margin $83.5.
Tie rate 0.0010.

## The three corrections this generation made
1. An exact cash tie was an INVALID game. It is now a real game; content
   duplication is decided by digest BEFORE the match.
2. "80.91% win rate" was a decided-only rate over a record 18% draws. The match
   score is (W+0.5T)/N.
3. "+275 ladder points" was inferred from curve saturation. Retracted: a flat
   curve means the observation cannot be inverted, not that the gap is large.

## R11 RESOLVED, not reinterpreted
The 992-game Farm leg gave a lower bound of 0.4990. At 2000 games the seed
bootstrap is [0.5200, 0.5815] and the pre-declared promotion criterion
(>52% with lower bound >50%) is met. The earlier null was sample size.

## Official leaderboard (recovered)
745 teams, 1914.4 to **3069.5** (rank 1, "M & M & P & Q"). Metric is final
Bradley-Terry with a draw worth 0.5. The 3066 target therefore sits just under
the current leader. Rank 2 3025.7, rank 3 "DSM" 2945.4.

## Blockers
1. **Anchor binding.** Kaggle exposes no submission-id-to-team mapping, so a
   public artifact cannot be tied to an official score with class-A evidence.
   1 usable class-B anchor exists; the publication gate needs 5. No rating can
   be published.
2. **No fast simulator.** 107 matches/min on 8 official workers bounds the
   search. The other 511 boolean configurations cannot all be evaluated at
   promotion-grade sample size.
3. **`thomas.py` is unlicensed.** Usable as an analytical opponent, never as a
   submission candidate.

## Next commands
```
.venv\Scripts\python.exe policy\search\racing_search.py --stage A   # running
.venv\Scripts\python.exe policy\search\racing_search.py --stage B
.venv\Scripts\python.exe research\turns_and_regimes.py --seeds 24
.venv\Scripts\python.exe pipeline\dashboard_3066.py
.venv\Scripts\python.exe tests\test_research_gate.py
```
