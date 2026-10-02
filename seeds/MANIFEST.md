# Real ladder seed splits — provenance manifest

Source dataset: Kaggle dataset `xishengfeng/kaggriculture-replay-db`
(public replay database, lastUpdated 2026-09-26).

## Index audit

- **rows**: 88281
- **unique_episode_ids**: 88281
- **date_min**: 2026-09-07T10:56:20.414041500Z
- **date_max**: 2026-09-25T05:10:09.395092900Z
- **duplicate_episode_ids**: 0
- **elite_games**: 24548
- **min_score_filter**: 2900.0
- **public_episodes**: 87808

## Filter criteria

- `score_0 >= 2900.0` AND `score_1 >= 2900.0` — **both** players rated 2900+
- `type == EPISODE_TYPE_PUBLIC` (excludes validation episodes)
- episode must have a downloaded shard so the seed is recoverable
- duplicate seeds discarded; assignment to split by SHA256 of the seed (stable and not cherry-picked)

## Splits

### REAL_dev.txt
- count: 12
- sha256: `92bc611ee24bf1db1686a93642f6e5ecf28e1978ff395a399fba4742ceec95f1`

### REAL_holdout.txt
- count: 12
- sha256: `8c1341e4dbfacb57afc4980b212f90f19bd899bd6c9ff6322cd31cacabf7734c`

### REAL_final.txt
- count: 12
- sha256: `f4057aa5ed7490a411b267cddfd034c0b7bf7297e37ab07657ab95f23bdbddce`

## Coverage note

- Index covers 2026-09-07T10:56:20.414041500Z → 2026-09-25T05:10:09.395092900Z.
- The competition deadline was 2026-09-30 and evaluation continued after;
  this snapshot therefore misses the final ~5 days of ladder play.
- Scores in the index are `updatedScore` at crawl time, i.e. the rating
  **after** the episode, not the rating at which it was matched.
- Config overrides observed: <stock>

## Seal

`REAL_final.txt` is committed before evaluation and must be run exactly once.
It is listed in `.gitignore` results-wise only insofar as `meta_final` was; the seed file itself IS committed here to prevent post-hoc selection.
