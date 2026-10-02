"""Append retraction entries to reports/RETRACTIONS.md.

Kept as a script rather than hand-edits so each entry carries a timestamp and
the entries stay in one consistent format, and so the file can be regenerated
if it is ever lost.
"""
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "reports", "RETRACTIONS.md")

TS = "2026-10-02"

ENTRIES = f"""
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
"""


def main():
    existing = open(PATH, encoding="utf-8", errors="replace").read()
    marker = "## R8 - RETRACTED"
    if marker in existing:
        print("R8-R11 already present; nothing appended")
        return 0
    with open(PATH, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(ENTRIES)
    print(f"appended R8-R11 to {os.path.relpath(PATH, ROOT)}")
    print(f"  entries: 4   timestamp: {TS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
