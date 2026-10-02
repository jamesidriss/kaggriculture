# RETRACTIONS, SUPERSEDIONS and NO_GO records

Nothing in this file is deleted history. Each entry records what was claimed,
why it was wrong, when it was corrected, and what the evidence now says.

---

## R1 — SUPERSEDED: "Kaggle calls `agent(obs, configuration)`, so one-argument agents crash"

- **Old claim** (2026-10-02, `reports/HARNESS_SIGNATURE_AUDIT.md` v1):
  > "Kaggle invokes agents as `agent(obs, configuration)`. A large share of
  > public Kaggriculture agents define the one-argument form… `TypeError` on
  > every turn, the framework marks the agent `INVALID`, it never acts, it
  > finishes on the starting $3,000."

- **Why it was wrong.** The claim about Kaggle is false.
  `kaggle_environments/agent.py`, `Agent.act`, does:

  ```python
  args = [structify(observation), structify(self.configuration)]
  if hasattr(self.agent, "__code__") and hasattr(self.agent.__code__, "co_argcount"):
      args = args[: self.agent.__code__.co_argcount]
  action = self.agent(*args)
  ```

  The argument list is **truncated to the callable's own positional arity**, so
  `agent(obs)` and `agent(obs, configuration)` are both supported.
  `build_agent` passes a callable through unchanged (`if callable(raw): return
  raw, False`), so the truncation in `Agent.act` is what applies.

  Proof by execution, `benchmark/call_convention.py`:

  | agent | `co_argcount` | invoked | seat status |
  |---|---|---|---|
  | `def agent(obs)` | 1 | 29 | DONE |
  | `def agent(obs, configuration=None)` | 2 | 29 | DONE |

- **Correct root cause.** Our *diagnostic* scripts (`close_games.py`,
  `endgame.py`, `forensic.py`, and the first cut of `simcomp/league.py`) invoked
  agents **directly** as `fn(obs, configuration)`, which does break a
  one-argument agent. The competitive harness `benchmark/meta.py` passed the raw
  callable to `env.run` and was therefore never broken.

- **Verification that the competitive data was never affected.**
  `benchmark/isolate_signature_bug.py` runs four matchups through three paths
  (raw callable into `env.run`, 2-arg wrapper into `env.run`, direct
  invocation). All three produce **identical** cash, and the pre-fix
  `benchmark/meta.py` at commit `c8fb403` reproduces the current numbers:

  | matchup (seed 62857979) | old meta.py (raw) | new meta.py (adapter) | |
  |---|---|---|---|
  | sunrise vs v16_rc5 | 6400 vs 112314 | 6400 vs 112314 | same |
  | v51 vs v16_rc5 | 93336 vs 69182 | 93336 vs 69182 | same |
  | v51 vs barnyard_v7 | 113694 vs 78471 | 113694 vs 78471 | same |
  | v51 vs farm_2945 | 85013 vs 84461 | 85013 vs 84461 | same |

- **What actually happened to the "phantom" opponents.** Only one agent was
  genuinely inert: `shop_router`, which is **not self-contained** — it raises
  `FileNotFoundError` for `actions.json` on turn 1, and that file is not in the
  public notebook. It is withheld to `opponents/unlicensed/`.

- **Corrected** 2026-10-02. The adapter is retained because it gives every
  wrapper a uniform signature and provenance tags, but its docstring now states
  the real reason and `benchmark/agent_loader.py` is the single loader.

---

## R2 — CORRECTED: the Wilson interval published beside 76/144

- **Old claim**: v51 vs Farm was 76-68 over 144 games, "52.78%,
  Wilson 95% [0.3925, 0.5534]".

- **Why it was wrong.** The rate and the interval came from **different win
  counts**. `[0.3925, 0.5534]` is the correct Wilson interval for **68/144**
  (0.4722). The correct interval for **76/144** (0.5278) is
  **[0.4466, 0.6075]**. Nothing validated the pairing, and a report printed a
  number that did not describe the quantity next to it.

- **Corrected** 2026-10-02. `benchmark/stats.py` is now the single
  implementation, validated against an independently written formulation
  (`wilson_reference`, agreeing to 1e-12 over a grid) and against closed-form
  expected values. `benchmark/stats_selftest.py`, 51/51. The record helper
  `win_interval(W, L, T)` derives the rate and the interval from one set of
  counts so they cannot disagree.

  Verification, `benchmark/stats_selftest.py`:

  | record | Wilson 95% |
  |---|---|
  | 0/10 | [0.0000, 0.2775] |
  | 10/10 | [0.7225, 1.0000] |
  | 5/10 | [0.2366, 0.7634] |
  | 76/144 | [0.4466, 0.6075] |
  | 670/720 | [0.9096, 0.9469] |
  | 596/720 | [0.7985, 0.8536] |
  | 0/792 | [0.0000, 0.0048] |

  Two further defects were fixed in the same place: `binom_two_sided` and
  `mcnemar_exact` overflowed a float for n > 1023, which is exactly where they
  matter. Both now work in log space.

---

## R3 — SUPERSEDED: the 144-game top-two comparison

- **Old claim**: "v51 and farm_2945 are statistically tied."
- **Why it was superseded**: the sample was far too small, and the published
  interval was the wrong one. The comparison was re-run on **1,000 fresh
  ladder-derived elite worlds** (both seats, 1,984 games, disjoint from the
  sealed dev/holdout/final pools).
- **New evidence**: v51 **1039-945**, 52.37%, Wilson 95% **[0.5017, 0.5456]**,
  exact binomial **p = 0.0368**. The interval excludes 50%, so v51 **is** better
  — by about two points, which is real but economically negligible (mean paired
  margin $28, 59% of games decided by under $1,000).
- See `reports/V51_VS_FARM.md`.

---

## R4 — RETRACTED: the Bradley-Terry ranking

- **Old claim** (2026-10-02, `reports/LOCAL_BRADLEY_TERRY_PARITY_SAFE.md` v1):
  betas `57.667 / 24.212 / -1.788 / -9.788` and an ordering built on them.

- **Why it was wrong**: the fit never converged and the model is not
  identifiable for this league. After a connected 9-agent round robin
  (576 games) the diagnosis is precise rather than a guess: the comparison graph
  is now strongly connected (9 of 9) but **`v49` and `v50` are undefeated within
  it (MLE = +inf) and `v16_rc5` is winless (MLE = -inf)**. The league is a strict
  linear order with complete separation, so no finite maximum likelihood exists.
  The tell was visible in the old output: six different agents printed the
  identical value `-9.788`.

- **Corrected** 2026-10-02. Plain-MLE betas are **withheld**.
  `benchmark/stats.py` raises rather than printing an unbounded fit, and the
  report publishes a clearly labelled **REGULARIZED BT** (MAP under a
  Normal(0,1) prior) whose spread is explicitly described as compressed. The
  primary evidence remains the observed pairwise records with intervals.
  See `reports/ROUND_ROBIN.md`.

---

## R5 — SUPERSEDED: "the PRIMARY and HEDGE are two different lineages"

- **Old claim** (2026-10-02, `reports/OPTIMAL_FINAL_PAIR.md` v2): v51 and the
  2945 Farm are "a genuine hedge, not a near-duplicate", justified by different
  order counts (3,618 vs 7,684 market orders) and different end-of-season farms.

- **Why it was wrong**: the order-count difference came from a measurement made
  with different `--opp` arguments. Measured identically, the two agents agree to
  three significant figures:

  | over 5 seeds vs `starter` | v51 | Farm 2945 |
  |---|---|---|
  | SELL orders | 1,760 | 2,035 |
  | BUY_SEED | 930 | 928 |
  | BUY_ANIMAL | 61 | 60 |
  | HIRE | 1,327 | 1,328 |
  | BUY_LAND | 10 | 10 |

  And at the source level (`benchmark/lineage_check.py`) they are the **same
  lineage**: 1,205 shared unique identifiers, containment 0.82, a single
  contiguous identical run of **3,352 tokens**, and an identical nine-author
  credit list in both headers. v51 descends from the 2945 Farm.

- **Corrected** 2026-10-02. The HEDGE remains the 2945 Farm because it is the
  only other agent within noise, but `postmortem_hedge/METADATA.txt` states
  explicitly that it is **not** a diversifying hedge. A genuinely diverse hedge
  does not exist in the legally reusable public set: the one distinct-lineage
  agent obtainable, `v16_rc5` (boatlee), is 0-232 to both top agents.

---

## R6 — INVALIDATED BY HARNESS BUG: "The 2945 Farm crashes in seat 1"

- **Old claim**: `observation["step"]` exists only for player 0, so the
  artifact raises `KeyError` in seat 1 and required a patch.
- **Why it was wrong**: a harness bug. The probes read
  `env.steps[i][seat].observation` — the **persisted** snapshot, which omits
  shared fields for seat 1 — instead of the observation Kaggle **delivers**,
  which includes them. The verbatim artifact runs in both seats, 0 crashes.
- **Corrected** 2026-10-02, `reports/KAGGLE_RUNTIME_PARITY.md`. The seat patch
  is retracted and retained only as `challengers/challenger_001_…`.

---

## R7 — CORRECTED: artifact digests did not match the files on disk

- **Old claim**: `opponents/meta/MANIFEST.csv` and the METADATA files record a
  SHA256 for every agent artifact.
- **Why it was wrong**: `core.autocrlf=true` made Git write every artifact to
  the working tree with CRLF while every recorded digest described the LF blob.
  `sha256sum postmortem_champion/main.py` disagreed with its own METADATA for
  the whole project.
- **Corrected** 2026-10-02. `.gitattributes` marks every artifact directory
  `-text`; `core.autocrlf=false`; `benchmark/normalize_artifacts.py` rewrote 50
  files to LF and re-verifies against the Git blob.
- **Consequence**: two store keys no longer addressed their contents and were
  re-keyed (`benchmark/rekey_store.py`):

  | old (CRLF) digest | canonical (LF) digest | agent |
  |---|---|---|
  | `919fc1d61050cd96…` | `3abe0ca715ba1864…` | v43 recovering-lost-harvests |
  | `797d9bca309d481e…` | `fe370bd8a9d0f377…` | v44 same-turn-sale-race |

  **Canonical digest definition, from now on**: SHA256 over the bytes as
  committed to Git (LF), which is what `git cat-file` returns and what any Linux
  checkout produces.

---

## NO_GO records

Recorded so the search is not repeated blindly.

| hypothesis | verdict | reason |
|---|---|---|
| More independent lineages from final-week Kaggle Code | **NO_GO** | `statma/kaggriculture-herd-safe-sale-window-submit`, `haideptry/the-shepherds-ledger` and `hanifnoerrofiq/pioneers-of-kaggle-town` contain no extractable agent cell (`research/scan_nb_agents.py`); `wzhengbiao/kaggriculture-hybu-submit` and `yasutakababa/kaggriculture-late-purchase-v16-submit` are code **generators** that print `restored main.py` rather than being artifacts; `sunyuxiang136` `export_v8.py` defines no `agent()`. |
| `shop_router` as a league member | **NO_GO** | Not self-contained: `FileNotFoundError` for `actions.json` on turn 1; the file is not in the public notebook. |
| `barnyard_v7` as a redistributable champion | **NO_GO** | The author declared **no licence**. Analysed, never redistributed as champion. |
| `v16_rc5` as the diversifying hedge | **NO_GO** | Genuinely distinct lineage, but 0-232 to both top agents, median $82k against $116k. |
| A challenger that beats the references | **NO_GO** | See `reports/FINAL_RESEARCH_CONCLUSION.md` §7. |
| Agent-callable (object with `__call__`) agents | not exercised | No candidate in the final-week search defined one; `load_agent` handles the callable-object case by wrapping `mod.agent` regardless of its type. |

---

## R8 - RETRACTED: "C001 is at least 275 ladder points above v51"

- **Old claim** (`reports/3075_RESEARCH_CONCLUSION.md` §7, and the same claim in
  `submission_ready/METADATA.txt`):
  > "an 80.91% win rate over the previous champion is far past the top of the
  > fitted curve, so the gap is at least 275 ladder points"

- **Why it was wrong.** The argument was: the fitted `P(higher rated wins)`
  curve is observed only up to a 275-point gap, where it reaches 0.995; our
  measured win rate sits beyond that; therefore the gap is >= 275.

  That does not follow. The curve being *flat* over its observed range means
  the measurement has no resolution there. Two gaps of 275 and of 900 produce
  the same predicted win rate, so an observation beyond the top of the table
  is consistent with a gap anywhere above the last bin. "At least 275" is a
  statement about where the DATA STOPS, not about the agents.

  It is the same class of error as reading a saturated table as a bound. The
  curve saturating is evidence that the observation cannot be inverted, which
  is the opposite of evidence about how large the gap is.

- **Correct interpretation.** An 80.91% decided-only win rate (75.30% BT score
  rate) against the previous champion is far outside the range where the
  ladder curve has resolution. It therefore establishes that the two agents are
  very far apart on the ladder's own scale, and it establishes **nothing
  quantitative** about how far. No lower bound on the gap is available.

- **Correct position now:** NO RELIABLE ABSOLUTE SHADOW RATING. The champion's
  ladder position is unknown, and no bound is claimed.

---

## R9 - RETRACTED: "an exact cash tie is an invalid game"

- **Old claim** (`benchmark/tournament.py`, `validate_game`):
  > `if r["tie"]: reasons.append("exact tie (duplicate-content signal)")`

- **Why it was wrong.** It applied a heuristic about CONTENT DUPLICATION to the
  OUTCOME. Content duplication is exactly decidable from the artifact SHA256,
  and the runner already checked it before the match
  (`if a_sha == b_sha or a_nrm == b_nrm: ABORT`). Cash equality carries no
  information about duplication at all: two different artifacts can, and in the
  C001 experiment did, finish a season level.

  It also failed in the flattering direction. In the C001 vs v51 experiment the
  two agents finished level on 216 of 992 worlds -- worlds where the single
  changed gene never fired. Discarding those removed exactly the worlds where
  the change had NO effect, and the aggregate was computed on the remainder
  only. The reported figure was conditional on the change doing something.

- **Correct rule**, now enforced and regression-tested in
  `tests/test_tie_semantics.py`:
  * content duplication -> decided by digest, BEFORE the match, aborts the run;
  * an exact cash tie between different artifacts -> a REAL GAME,
    `valid = 1`, `tie = 1`, and it enters every aggregate.

- **Consequence.** `migration/reclassify_ties.py` restored **498** games across
  23 files from their preserved originals. Zero games failed for a real defect,
  so nothing was left invalid.

---

## R10 - SUPERSEDED: "80.91% is C001's win rate against v51"

- **Old claim** (`reports/3075_RESEARCH_CONCLUSION.md` §8, promotion metadata):
  > "657-155-180 of 992, 80.91% win rate"

- **Why it was wrong.** 180 of the 992 games, 18.1%, were draws. Kaggle's final
  evaluation is a Bradley-Terry fit over episodes in which a draw scores 0.5
  for each side, so the per-game score is (1, 0.5, 0) and the match score is
  the mean of that, `(W + 0.5T)/N`. `W/(W+L)` answers a different question:
  "when this matchup produces a winner, how often do I win it". Both are worth
  knowing. Only the first is the match score.

- **Correct figures** (recomputed from migrated raw rows by
  `policy/search/canonical_metrics.py`):

  | record | N | BT score rate | 95% (seed bootstrap) | decided-only | tie rate |
  |---|---|---|---|---|---|
  | 638-138-216 | 992 | **0.7520** | [0.7218, 0.7812] | 0.8222 | 0.218 |
  | 657-155-180 | 992 | **0.7530** | [0.7218, 0.7833] | 0.8091 | 0.181 |
  | 537-453-2 | 992 | **0.5423** | [0.4990, 0.5857] | 0.5424 | 0.002 |
  | 506-486-0 | 992 | **0.5101** | [0.4667, 0.5534] | 0.5101 | 0.000 |

  The improvement over v51 is still enormous: 75.2-75.3% BT score rate where the
  parent scores 51.0% against the same opponent. But the replication is the
  real finding, and it was invisible before: the two runs disagree by **1.31
  points** on the decided-only rate and by **0.10 points** on the BT score rate.
  The metric that matches the competition's scoring convention is the one that
  replicates.

---

## R11 - RETRACTED: "C001 is significantly better than the 2945 Farm"

- **Old claim** (`reports/3075_RESEARCH_CONCLUSION.md` §9, promotion gate leg B):
  > "54.24%, Wilson [0.5113, 0.5732], p = 0.0083 ... positive result vs Farm"

- **Why it was wrong.** The interval quoted was a Wilson interval on the
  DECIDED-only rate, treating the 992 games as independent Bernoulli trials.
  Two things are wrong with that:

  1. the primary metric is the BT score rate, not the decided-only rate;
  2. the experiment is PAIRED and BOTH-SEAT. The two games from one world share
     the world, the market state and the opponent, so they are correlated
     observations. Resampling them independently understates the interval.

  Under the correct uncertainty method -- a bootstrap that resamples SEEDS,
  `paired_seed_bootstrap` -- the interval is [0.4990, 0.5857]. **The lower
  bound falls below 0.50.** The pre-declared promotion criterion was "score
  rate > 52% with lower confidence > 50%", and it is not met.

- **Correct position now.** C001's BT score rate against the 2945 Farm is
  **0.5423**, a real and replicated point estimate, but its lower confidence
  bound is **0.4990**. C001 is *probably* better than the Farm; this evidence
  does not establish it at the stated threshold. The honest statement is that
  this matchup is unresolved and needs a larger sample, which is why the next
  generation's first job is 3,000+ direct games on this pairing.

- **Note on the direction of the error.** Both of the mistakes in R10 and R11
  pushed the same way: each discarded or ignored information (the draws, the
  within-seed correlation), and each made the champion look stronger than the
  evidence supports. Neither was in the agent's favour; both were in the
  *reporting's* favour, which is the more dangerous direction.
