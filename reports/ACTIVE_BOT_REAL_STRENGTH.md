# ACTIVE BOT REAL STRENGTH (ladder measurement)

**Source:** 14 real ladder episodes (7 per bot) from 2026-10-01, replays
downloaded, seats verified by action-matching our exact submitted bytes
(40-vs-0 confidence on every episode). Full rows in
`data/final_evaluation_episodes.csv`.

**Ratings at measurement:** sunrise-v5 = 250.0, sunrise-v4 = 153.0
(leader ~3052).

## sunrise-v5: 4W-3L in 7 sampled games

| opponent bucket | games | W-L | win rate | Wilson 95% | our median $ | opp median $ |
|---|---|---|---|---|---|---|
| 0-3000 (passive) | 1 | 1-0 | 1.00 | [0.21, 1.00] | 6205 | 2845 |
| 3001-6000 (weak) | 3 | 3-0 | 1.00 | [0.44, 1.00] | 6690 | 5116 |
| 10001-15000 (strong) | 2 | 0-2 | 0.00 | [0.00, 0.66] | 7587 | 11265 |
| 15001+ (very strong) | 1 | 0-1 | 0.00 | [0.00, 0.79] | 5201 | 19895 |

Seats: 2W-2L as seat 0, 2W-1L as seat 1 (no seat effect visible).

**50%-win point: ~$8,000-10,000 opponent final cash.** Below that v5 wins
reliably; above $10k it has lost every game. A $10k opponent is roughly a
1200-1500-rated agent (beats starter-level play, loses to any real economy).

## sunrise-v4: 3W-4L in 7 sampled games

| opponent bucket | games | W-L | win rate | Wilson 95% | our median $ | opp median $ |
|---|---|---|---|---|---|---|
| 0-3000 (passive) | 6 | 3-3 | 0.50 | [0.19, 0.81] | 2750 | 3000 |
| 6001-10000 (mid) | 1 | 0-1 | 0.00 | [0.00, 0.79] | 905 | 7795 |

Seats: 1W-2L as seat 0, 2W-2L as seat 1.

**v4 cannot reliably beat agents that do nothing.** Three losses to opponents
finishing at exactly $3000 (starting cash, zero economic activity), including
two total collapses ($82 and $220 final cash). Its 50%-win point is below the
passive level — consistent with its 153.0 rating.

## Interpretation

- Neither bot is competitive above the ~1000-rating level. The meta agents in
  `opponents/meta/` finish at $60k-180k locally; our bots finish at $5-9k on a
  good day. That is a **10-30× economic gap**, not a tuning gap.
- v5's ceiling (~$9k wins) vs the recovery champion's floor (~$60k+): there is
  no overlap. No matchup noise bridges this.
- Opponent team names in the sample (Tesfahun Feleke, T Vamsi Krishna,
  ArtlexYang, chestnut, etc.) are mid/low-ladder teams; even there we are 7-7
  combined.

## Caveats

- 7 games per bot is a small sample; Wilson intervals are wide. But the
  *level* conclusion (50% point near $8-10k for v5, below passive for v4) is
  robust because the cash gap to the next tier is an order of magnitude.
- Opponent strength is proxied by final cash, not rating (replays expose team
  names, not ratings). Cash is the more direct measure of game strength.
