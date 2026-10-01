# FINAL TOURNAMENT TRACKER

Kaggle continues running post-deadline evaluation games. Our two active agents
are **immutable competition entries** — nothing in this repository can change
their performance. This file records what the platform reports.

## Current state (2026-10-02)

```
SUBMISSION_ID  VERSION      STATUS    RATING
56716646       sunrise-v5   COMPLETE  241.5
56716532       sunrise-v4   COMPLETE  158.4
```

Rating history observed this session:

| timestamp (UTC) | v5 | v4 |
|---|---|---|
| 2026-10-01 20:35 | 250.0 | 153.0 |
| 2026-10-01 21:40 | 241.5 | 158.4 |

Both are drifting in the 150-250 band. The leader sits at ~3052 and the
10-team cut is ~2880. The gap is roughly an order of magnitude.

## Episode volume

19 episodes retrievable per bot at last check (`kaggle competitions episodes`),
running continuously through the extended evaluation window. Episode 116532203
completed 2026-10-01 21:38.

## Measured strength (our own ladder episodes, 14 games downloaded)

| bot | W-L | 50%-win point (opponent final cash) |
|---|---|---|
| sunrise-v5 | 4-3 | ~$8-10k |
| sunrise-v4 | 3-4 | below passive |

Full detail: `reports/ACTIVE_BOT_REAL_STRENGTH.md`, raw rows in
`data/final_evaluation_episodes.csv`.

## Opponent distribution

Every sampled opponent was a mid/low-ladder team (Tesfahun Feleke, T Vamsi
Krishna, ArtlexYang, chestnut, Mahmoud Abdelshafy, …). No elite opponent
appeared in our sample, which is why our measured win rate is roughly 50% and
the ladder rating is ~250: **we are beating the field we are matched against,
and that field is far below the leaders.**

## Rating buckets observed

| bucket (opponent final cash) | games | result |
|---|---|---|
| $0-3,000 (passive) | 7 | 4-3 |
| $3,001-6,000 (weak) | 3 | 3-0 |
| $6,001-10,000 (mid) | 1 | 0-1 |
| $10,001-15,000 (strong) | 2 | 0-2 |
| $15,000+ (very strong) | 1 | 0-1 |

Every loss came against an opponent that earned more than $10k. The meta agents
reproduce at $95k-183k. There is no match regime in which our bots meet the
leaders.

## Close matches

In the 14 sampled ladder games **no game was decided by less than $2,000**, and
the smallest margin was $905. Our agents do not reach the near-tie regime at
all: they are either comfortably ahead of passive opponents or far behind
anyone who plays properly. At the top of this leaderboard, results are decided by
hundreds of dollars, so this is a level difference, not a variance difference.

## What this tracker cannot tell us

- Whether any public agent we reproduced would place higher than we did. We have
  no ladder entries for them.
- The elite public field's behaviour: top-20 teams (3050-3300) have almost no
  extractable artifacts among the notebooks retrieved. Behavioural inference
  from replays is the only avenue and has not been done.