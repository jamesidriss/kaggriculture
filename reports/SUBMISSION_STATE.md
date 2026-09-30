# Kaggriculture — Submission State

Last updated 2026-09-30 21:13 UTC. Deadline **2026-09-30 23:59**.

Daily quota: 5 submissions. **0 remaining today.** The quota is spent; the two
active slots are locked and no further changes can be made before the deadline.

## SUBMISSION TABLE

| SUBMISSION_ID | TIMESTAMP (UTC) | VERSION | COMMIT | STATUS | RATING | ACTIVE? | KEEP? |
|---|---|---|---|---|---|---|---|
| 56716289 | 18:52 | sunrise-v1 | `fd4c370` | COMPLETE | 348.1 | no | no — retired |
| 56716337 | 18:54 | sunrise-v2 | `fd4c370` | COMPLETE | 322.0 | no | no — retired |
| 56716446 | 19:00 | sunrise-v3 | `f4f58a6` | COMPLETE | 506.8 | no | no — retired by v5 |
| 56716532 | 19:06 | sunrise-v4 | `d6f79ce` | COMPLETE | **600.0** | **yes** | **yes** |
| **56716646** | **19:12** | **sunrise-v5 (FINAL)** | `8919b23` | PENDING | — | **yes** | **yes** |

## ACTIVE BOT SAFETY ANALYSIS (final submission)

```
ACTIVE BOT 1:  56716532  sunrise-v4  rating 600.0
ACTIVE BOT 2:  56716446  sunrise-v3  rating 506.8
NEW CANDIDATE: 56716646  sunrise-v5  (= champion_001)

SUNRISE-V5 WOULD RETIRE: 56716446 (sunrise-v3, rating 506.8)

SAFE?  YES
  - v5 is a strict superset of v4's source: it changes only the melon tile quota
    from land/2 to land/5 and adds a comment. Every other mechanism is identical.
  - Local evidence strictly improved, on both seed pools:
        holdout vs starter   mean cash  $4,757 -> $7,520   win rate 9-1 -> 8-0
        league dev           20-0, 0 errors
        league holdout       20-0, 0 errors
  - The bot being retired (v3, 506.8) was ALREADY the weaker of the two active
    pair at the time of the swap (600.0 vs 506.8), so the strongest active bot
    (v4, 600.0) is preserved untouched.
  - v4 remains in the repo as champions/champion_000, restorable in seconds.
```

## Notes

- All submissions are the single-file `main.py` agent: no archive, no external
  dependency, no network access, no model download, no absolute paths.
- Validation ratings (322-600) are the Kaggle default for a completed validation
  episode and are **not** ladder performance. The leaderboard top is ~3053, so
  none of these numbers indicate real ladder strength; they only confirm the
  agent executed cleanly on Kaggle's side.
- `champions/champion_000` (v4) and `champions/champion_001` (v5) are both
  frozen locally and on GitHub with SHA256 and commit hashes.
- Submission gate `tests/test_submission.py`: **13/13 passing**.