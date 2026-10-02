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
