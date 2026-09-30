# Kaggriculture — Submission State

Last updated 2026-09-30 22:05 UTC. Deadline **2026-09-30 23:59**.

Daily quota: 5 submissions. **2 remaining.**

## ACTIVE BOT SAFETY ANALYSIS

```
ACTIVE BOT 1: 56716337  sunrise-v2   score 600.0   (bulk-seed fix)
ACTIVE BOT 2: 56716289  sunrise-v1   score 491.1   (superseded, weaker)
NEW CANDIDATE: 56716446  sunrise-v3  (bulk seeds + $1-floor liquidation)

SUNRISE-V3 WOULD RETIRE: 56716289 (sunrise-v1, the weaker of the two)

SAFE?  YES
  - v1 scores 491.1, v2 scores 600.0, v3 is a strict superset of v2's changes
    and beats v2's exact source on the paired dev seeds (8-0).
  - Only the strictly weaker bot is displaced; the current best stays active.
  - Local evidence: v3 vs starter 12-0 dev / 9-1 holdout; 12-0 vs random;
    8-0 vs pass. Zero errors across 40+ simulated episodes.
```

## SUBMISSION TABLE

| SUBMISSION_ID | TIMESTAMP (UTC) | VERSION | STATUS | RATING | EPISODES | ACTIVE? | KEEP? |
|---|---|---|---|---|---|---|---|
| 56716289 | 2026-09-30 18:52 | sunrise-v1 | COMPLETE | 491.1 | 1 validation | yes | no — superseded |
| 56716337 | 2026-09-30 18:54 | sunrise-v2 | COMPLETE | 600.0 | 1 validation | yes | yes |
| 56716446 | 2026-09-30 19:00 | sunrise-v3 | PENDING | — | — | pending | yes |

## Notes

- All three submissions are the single-file `main.py` agent. No archive, no
  external dependency, no network access, no model download.
- Validation score of 600.0 is the Kaggle default for a completed validation
  episode; the meaningful number is the ladder rating, which needs real matches.
- Leaderboard top at time of writing is ~3053 (`M & M & P & Q`).
- **Emergency reserve: 2 submissions held in hand.**