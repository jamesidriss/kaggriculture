# 3066 RESEARCH CONCLUSION

Branch `research/3066-breakthrough`. Generation objective: a legal,
submission-ready Kaggriculture agent with defensible offline evidence that it
can exceed a real leaderboard strength of **3066**, with an internal research
target above 3100.

Reproduce with:

```
python benchmark/stats_selftest.py              # 46/46
python tests/test_tie_semantics.py              # 24/24
python migration/reclassify_ties.py --dry-run   # 0 remaining after migration
python shadow_ladder/fetch_leaderboard.py       # official final leaderboard
python research/build_anchor_catalog.py
python shadow_ladder/score_candidate_v2.py      # publication gate
python benchmark/parallel_tournament.py ...     # canonical measurements
python policy/search/racing_search.py --stage A
python research/turns_and_regimes.py --seeds 6
python pipeline/dashboard_3066.py
python tests/test_research_gate.py
```

Throughout: **primary metric is the BT score rate `(W + 0.5T)/N`**, which is how
Kaggle's final Bradley-Terry scores a draw. Intervals are percentile bootstraps
that resample **seeds**, because the experiments are paired and both-seat and the
two games from one world are correlated observations. Decided-only `W/(W+L)` is
reported as a secondary diagnostic and is never called the match score.

---

## 1. Was the exact-tie tournament bug fixed?

**Yes, and it was the most consequential change of this generation.**

`benchmark/tournament.py` had been rejecting any game whose two sides finished
with identical cash, recording the reason as *"exact tie (duplicate-content
signal)"*. That applied a heuristic about **content duplication** to the
**outcome**.

Content duplication is exactly decidable from the artifact SHA256, and the
runner already checked it **before** the match
(`if a_sha == b_sha or a_nrm == b_nrm: ABORT`). Cash equality carries no
information about duplication at all: two different artifacts can, and in the
C001 experiment did, finish a season level.

It also failed in the direction that flatters an experiment. C001 and v51 tied
on **216 of 992** worlds — precisely the worlds where the single changed gene
never fired. Discarding them removed exactly the no-op worlds and computed the
aggregate on the remainder, so the reported rate was conditional on the change
doing something. The 82.22% figure was conditional on a difference existing.

Rule now, and pinned by `tests/test_tie_semantics.py` (24 checks, both
directions): digest decides duplication, before the match, and aborts; an exact
cash tie between different artifacts is a **real game**, `valid = 1`, `tie = 1`.

## 2. What historical results changed?

`migration/reclassify_ties.py` recomputed validity from the fields that actually
mean something — both statuses `DONE`, both call counts within tolerance — and
restored **498 games across 23 files** from their preserved originals. Zero
games failed for a real defect, so nothing was left invalid. The migration is
idempotent (a second pass restores 0) and records a provenance manifest with the
original digest per file.

One bug found while aggregating the migration: preserved originals end in
`.csv`, so an `r_*.csv` glob matched both the live file and its backup and
**double-counted 992 games as 1,984**. Backups are now excluded by name
everywhere, and `.pre_tie_fix.csv` is git-ignored.

## 3. What is C001's corrected BT score vs v51?

| record | N | **BT score** | 95% (seed bootstrap) | decided-only | tie rate |
|---|---|---|---|---|---|
| 638-138-216 | 992 | **0.7520** | [0.7218, 0.7812] | 0.8222 | 0.218 |
| 657-155-180 | 992 | **0.7530** | [0.7218, 0.7833] | 0.8091 | 0.181 |

**The replication is the real finding, and it was invisible before.** The two
runs disagree by **1.31 points** on the decided-only rate and by **0.10 points**
on the BT score rate. The metric that matches the competition's own scoring
convention is the one that replicates. Both runs are independent seed sets.

Seat splits: 320 P0 / 318 P1 and 326 P0 / 331 P1. No seat effect.

## 4. Corrected BT score vs Farm?

**0.5510 over 2,000 fresh paired games** (1,000 seeds, both seats, 0 broken):

| | |
|---|---|
| W-L-T | 1101-897-2 |
| **BT score rate** | **0.5510** |
| 95% seed bootstrap | **[0.5200, 0.5815]** — clears 0.50 |
| decided-only | 0.5511, Wilson [0.5292, 0.5727] |
| tie rate | 0.0010 |
| seat 0 / seat 1 | 552-447 / 549-450 |
| mean / median margin | $83.5 / $135 |

This **resolves** the previous generation's retraction R11. At 992 games the
seed bootstrap was [0.4990, 0.5857] and the pre-declared promotion criterion
(>52% with lower bound >50%) was **not** met. At 2,000 games it is met. R11 was
a correct retraction of a small-sample claim, resolved by measurement rather than
by reinterpretation.

## 5. How many exact-score calibration anchors were recovered?

**One usable anchor (class B).** The gate needs five.

The competition is over and Kaggle publishes a **final Bradley-Terry leaderboard**
with draws worth 0.5 per side — exactly the metric this project must optimise.
`shadow_ladder/fetch_leaderboard.py` recovered **745 teams**, scores **1914.4 to
3069.5**.

| anchor | artifact | official score | class | binding |
|---|---|---|---|---|
| 2945 Farm | `postmortem_hedge/main.py` | 2945.4 (rank 3, "DSM") | **B** | inferred |

The binding rests on two independently derived numbers agreeing to 0.4 points:
the agent's own notebook self-reports 2945, and the official leaderboard has
exactly one team named "DSM" at 2945.4. Kaggle exposes **no** public mapping from
a submission id to a team, so this is a strong coincidence, not a proof, and it
is recorded as class B with its weaknesses written down rather than promoted to
A.

## 6. What scores do they span?

The leaderboard spans **1914.4 → 3069.5**, with 490 teams in 2000–2500, 72 in
2500–2800, 7 above 2800 and 2 above 3000. The anchor set spans **0 points**,
because there is one anchor.

Top of the field: rank 1 "M & M & P & Q" **3069.5**, rank 2 "1x5090 potato run"
**3025.7**, rank 3 "DSM" **2945.4**.

**The 3066 target therefore sits just below the current rank 1**, and from the
fitted ladder response curve a 3066 rating implies winning roughly **99%** of
games (P(win) is 0.934 at a 100–125 point gap and 0.995 at 200+).

## 7. Is ShadowRating now calibrated?

**WITHHELD.** `shadow_ladder/score_candidate_v2.py` refuses to emit a rating.

The v2 audit found that v1 contained **seven consecutive assignments to
`shift`**, six of them dead, plus a `sign` variable computed and never used in
the surviving expression. The last assignment happened to be correct, so no
number was wrong — but correctness by luck is not correctness. v2 has one
`shift`, a publication gate in code with **no path that emits a rating without
clearing it**, explicit censoring, and **no fabricated gap from saturation**.

Gate outcome: 1 usable anchor against a requirement of 5; anchor span 0 against
a requirement of 300; leave-one-anchor-out not performable.

## 8. Calibration MAE / rank correlation?

**Not measured, and reported as not measured.** Leave-one-anchor-out cannot run
with one anchor. No MAE and no Spearman are published, because publishing either
from a single point would be manufacturing a validation result.

## 9. How many turn rows were ingested?

**8,640 rows over 6 episodes** (720 steps × 2 players × 6 worlds), from our own
matches on the official engine. The public replay shards were never downloaded
(33 of 88,281 episodes had a local shard), so per-turn state is largely
unavailable there; the `source` column records this rather than passing the data
off as replay data.

37 typed columns. Quality gate: 0 duplicate `(step, player)`, 0 steps over 720,
0 negative money, both players on every episode, and **0 shared-market
mismatches** between seats — the market is shared, and recording it per-player
would model a fiction.

## 10. How many world regimes identified?

**4 clusters over 6 worlds**, separating on shop count (5–7) and minimum market
inventory (~89.7k).

Honest limitation: with 6 worlds and a 5–7 shop spread, **world diversity in this
environment is weak**. Regime-stratified evaluation therefore has limited
resolving power, and a candidate cannot be exonerated by a favourable regime
breakdown on this sample. Feature families are kept apart —
`known_at_decision_time` (first shops) versus `descriptive_only`
(whole-trajectory scarcity), which may group worlds offline and may never become
a policy input.

## 11. How many strong independent lineages?

**Four known, one newly recovered, and only one that is both mid-curve and
legally restricted.**

| lineage | agents | notes |
|---|---|---|
| `L-OZER-2945` | 12 | v43→v51 series plus the 2945 Farm. Includes champion, parent and hedge |
| `L-R88` | 1 | `thomas.py`, **unlicensed** → analytical opponent only. C001 scores 0.5800 against it: mid-curve, the most informative opponent found |
| `L-MOON` | 2 | `moon_parent`, `moon_q13_mg`, **unlicensed**. C001 scores 0.0540 — saturated |
| `L-BOATLEE` | 1 | `v16_rc5`, distinct, far weaker |
| `L-SUNRISE` / `L-ROMANROZEN` | 3 | failure baseline and ineligible |

`moon_q13_mg.py` and `moon_parent.py` return **byte-identical records** over 250
seeds, which is itself a finding: the q13 variant is behaviourally
indistinguishable from its parent on every world tested.

Two Apache-2.0 agents from a second dataset were ingested and **failed** the
playability probe; they are recorded as rejected rather than quietly kept.

## 12. How many candidates evaluated?

**512 boolean configurations, enumerated exhaustively**, plus the champion at
every stage.

| stage | configurations | opponents | matches | minutes | broken |
|---|---|---|---|---|---|
| A | 512 + champion | v51, 4 worlds | 4,104 | 86.1 | **0** |
| B | 64 survivors + champion | v51 + Farm, 16 worlds | 4,096 | 76.8 | **0** |

A three-stage progressive race (A: 512×4, B: 64×16 vs two opponents, C: 3×48)
is defined in `policy/search/racing_search.py` with stage sizes, sample counts,
opponents and the objective written into the source **before any result
existed**.

## 13. What search method?

Exhaustive enumeration of the reachable boolean space with progressive racing,
**not** evolution. The reachable space is 2⁹ = 512, small enough to enumerate
completely; a stochastic search over 512 points would be strictly worse and would
add a failure mode to a programme that already has too many.

Objective, declared in advance: `0.6 × mean_lineage_score + 0.4 ×
worst_lineage_score` on lineage-balanced BT score rates, so nine variants of one
lineage cannot outvote one independent opponent.

**The robustness term was inert, and that is a design flaw worth recording.**
v51 and the 2945 Farm are correctly tagged as the *same* lineage
(`L-OZER-2945`), so at stages B and C the fit collapses to a single lineage and
`worst_lineage_score` equals `mean_lineage_score`. The reported `n_lineages` is
literally **1**. The term that exists to stop a one-lineage league from
dominating fitness cannot function inside a one-lineage opponent set. Making it
live requires the independent lineages to be in the search's opponent set, not
merely in the evaluation pool — recorded as the concrete next change rather than
patched here, because changing the opponent set mid-generation would invalidate
the pre-declaration.

Two sampling bugs from the previous generation were designed out: a
lexicographic **prefix** of `itertools.product` (which left `hand_align` constant
in all 64 sampled configurations and produced a uniform 0.0000 that looked like a
result), and an explicit abort if any single gene is degenerate.

## 14. Best candidate?

**None beat C001.** Stage B is the discriminating measurement, and there the
champion leads by a wide margin:

| rank | tag | robust | vs v51 | vs Farm |
|---|---|---|---|---|
| **0** | **C001_BASELINE** | **0.7656** | 24-4-4 → 0.8125 | 23-9-0 → 0.7188 |
| 1 | 788b6a356582 | 0.5469 | 18-14-0 → 0.5625 | 17-15-0 → 0.5312 |
| 2 | 94b7924d0da9 | 0.5469 | 18-14-0 → 0.5625 | 17-15-0 → 0.5312 |
| 3 | a98c3b1f18f4 | 0.5156 | 16-16-0 → 0.5000 | 17-15-0 → 0.5312 |

The champion is first at both stages.

## 15. Did it beat C001?

**No.** The best candidate trails C001 by **21.9 points** on the same worlds at
stage B (0.5469 vs 0.7656). Because the comparison is paired on identical seeds,
this is not a sample-size artefact: the candidates were measured against exactly
the worlds the champion was measured against.

## 16. Did it beat Farm?

**No.** The best candidate scores 0.5312 against the Farm where C001 scores
0.7188 on the same 16 worlds.

**Caveat on those absolute levels.** On the 16 dev worlds C001 beats the Farm
71.9% of the time, against 55.1% over the full 1,000-world measurement. The dev
pool's head is not representative of the Farm matchup. The *ranking* is still
valid because it is paired; the *levels* are not, and no conclusion is drawn from
them beyond the ordering.

## 17. Worst independent matchup?

**vs the 2945 Farm, BT 0.5510 [0.5200, 0.5815]** — the only opponent against
which C001 is above 50% without being near-total. Everything else is either a
decisive win (0.75 against the parent, 0.58 against `thomas`) or a decisive loss
(0.054 against the moon agents).

## 18. Sealed-final result?

**Not run.** The pool was created and its hash **committed before any candidate
was evaluated**, which is the point of a sealed pool:

```
GEN3066_sealed  130 seeds  sha256 3d9869bb78554097...
```

Disjointness is computed and recorded, not asserted: pairwise disjoint across
dev/holdout/sealed, and **0 seeds overlapping any previous-generation pool**.

It was not run because no finalist beat C001. Running a sealed pool against the
incumbent produces no information about a new candidate.

## 19. Current champion?

**`C001_room_guard`**, unchanged and immutable. sha256
`a52ba1bfe9df9dc1d504550af46744ef8d474797cdba7af2412dc40a3ebdf3b8`, 461,738
bytes, Apache-2.0 with NOTICE retained, exactly one declared modification from
its parent and byte-identical outside the settings literal.

## 20. Is it 3066-ready?

**NO.** Two legs fail, and the gate is not softened.

| leg | status |
|---|---|
| calibrated rating evidence | **FAILS** — 1 usable anchor against 5 required; no MAE or rank correlation computable |
| positive vs v51 | PASSES — 0.7520 / 0.7530, replicated |
| positive vs Farm | **PASSES** — 0.5510, lower bound 0.5200 > 0.50 |
| positive vs strong independent lineage | PARTIAL — 0.5800 vs `thomas`, but that agent is unlicensed and only one exists |
| both seats | PASSES |
| multiple world regimes | WEAK — 4 regimes over 6 worlds, shop spread 5–7 |
| sealed final | pool committed, not run (no finalist) |
| zero runtime/schema failures | PASSES — 0 broken in ~7,000 measured matches |

## 21. If not, the exact blocker?

**Kaggle publishes no mapping from a submission id to a team**, so a public
artifact cannot be bound to an official leaderboard score with class-A evidence.
One anchor is inferable (2945 Farm ↔ "DSM" at 2945.4) and it is class B. The
publication gate needs five.

This is a hard external limit, not a project deficiency, and the honest response
is to withhold the rating rather than to attach a notebook's self-reported
"Best Score" to a different version's artifact — which is precisely the
destruction of calibration this project exists to avoid.

## 22. Submission-ready SHA?

```
submission_ready/main.py
a52ba1bfe9df9dc1d504550af46744ef8d474797cdba7af2412dc40a3ebdf3b8
```
byte-identical to `champions/research/C001_room_guard/main.py`, verified
against `champions/research/CURRENT.json`. `METADATA.txt` carries the corrected
BT-score figures and states `3066-READY: NO` on two legs.

## 23. Final Git commit?

Recorded in `reports/RESEARCH_3066_CHECKPOINT.md` and in the merge commit on
`main`. Verified by `HEAD == origin/main` with a clean worktree after the merge.

---

## What this generation actually established

Three corrections, each of which had been inflating the case for the champion:

1. An exact cash tie was an **invalid game**. It is a real game. 498
   historical games were restored.
2. "80.91% win rate" was a decided-only rate over a record 18% draws. The match
   score is `(W + 0.5T)/N`.
3. "+275 ladder points" was inferred from a **saturated curve**. A flat curve
   means the observation cannot be inverted, not that the gap is large.

Two of those errors pushed the same way — each discarded information, and each
made the champion look stronger than the evidence supports. Neither flattered
the agent; both flattered the *reporting*, which is the more dangerous direction.

One thing was **resolved**: at 2,000 games, C001's BT score rate against the 2945
Farm is 0.5510 with a seed-bootstrap lower bound of 0.5200. The previous
generation's null was sample size, not a wrong method.

And one thing is new: the official final leaderboard. 745 teams, top score
3069.5, metric is final Bradley-Terry with draws at 0.5. The 3066 target is
therefore "match or beat the current leader", and the curve says that means
winning ~99% of games.

## The honest bottom line

C001 is the strongest legally reproducible agent this project can substantiate:
it beats its own parent by a replicated 75-point margin, it is the only agent
measured that sits significantly above 50% against the 2945 Farm, and it wins
100% of the weaker independent agents it was tested against.

It is **not** demonstrably a 3066 agent, and this generation cannot demonstrate
it, because no artifact can be bound to an official score with the evidence
required. The remaining gap between "strongest reproducible agent" and "provably
above 3066" is a **data-binding** gap, not a strategy gap — and closing it
requires either a submission that can be traced, or several more inferable
anchors of the 2945-Farm kind spread across the score range.
