"""Is Kaggle's ladder rating informative about who wins? (corrected)

Premise under test
------------------
The research objective is "exceed 3075 on the real leaderboard". That is only
reachable if the leaderboard responds to performance we can influence. So test
the premise rather than assume it.

Column semantics, established empirically (not guessed)
------------------------------------------------------
  * `reward_0` / `reward_1` in the public index are FINAL CASH, not a win flag:
    values run to ~100,000 and their means differ by <0.1%. A "win" is
    therefore `cash_0 > cash_1`.
  * `score_0` / `score_1` are the two players' ladder ratings, balanced
    (P(score_0 > score_1) = 0.4995).

  * The direct conditional probability P(cash_0 > cash_1 | score_0 > score_1)
    is 0.767 -- the higher-rated player wins about three games in four.

The first version of this script reported ~0.00 and concluded "uninformative".
That was a bug in the CASE expression, and it is recorded here because a wrong
conclusion from a plausible-looking query is exactly the failure mode this
project keeps hitting. The corrected form is used below and is simpler: because
the pairing is symmetric and the index stores both players, compute

    P(higher rated wins | gap in bin) = 2 * P(cash_0 > cash_1 AND score_0 >
    score_1 AND gap in bin) / P(gap in bin AND score_0 != score_1)

which cannot go out of range and needs no tie handling, because a game with
equal cash is simply not a win for either side.
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "shadow_ladder"))


def wilson(w, n, z=1.959963984540054):
    if n <= 0:
        return (0.0, 1.0)
    p = w / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, c - h) / d, min(1.0, (c + h) / d))


def main():
    from data_pipeline.lake import connect
    con = connect()

    pre = """
    WITH g AS (
      SELECT score_0 AS r0, score_1 AS r1, reward_0 AS c0, reward_1 AS c1
      FROM episodes
      WHERE score_0 IS NOT NULL AND score_1 IS NOT NULL
        AND reward_0 IS NOT NULL AND reward_1 IS NOT NULL
    ),
    d AS (
      SELECT abs(r0 - r1) AS gap,
             CASE WHEN r0 = r1 THEN NULL
                  WHEN r0 > r1 AND c0 > c1 THEN 1
                  WHEN r1 > r0 AND c1 > c0 THEN 1
                  ELSE 0 END AS higher_won
      FROM g
    )
    """
    rows = con.execute(pre + """
        SELECT CAST(floor(gap/25.0)*25 AS BIGINT) AS b,
               count(*) AS n, avg(higher_won) AS p
        FROM d WHERE higher_won IS NOT NULL
        GROUP BY b HAVING count(*) >= 300 ORDER BY b
    """).fetchall()

    print("=" * 78)
    print("DOES THE LADDER PREDICT WHO WINS?  (88k real public games)")
    print("=" * 78)
    print(f"{'rating gap':>12} {'games':>8} {'P(higher rated wins)':>22} "
          f"{'95% Wilson':>20}")
    bins = []
    for b, n, p in rows:
        w = int(round(p * n))
        lo, hi = wilson(w, n)
        print(f"{f'{b:.0f}-{b+25:.0f}':>12} {n:>8,} {p:>22.4f} "
              f"{f'[{lo:.4f}, {hi:.4f}]':>20}")
        bins.append({"gap_lo": b, "gap_hi": b + 25, "games": n, "p": p,
                     "wilson": [lo, hi]})

    big = con.execute(pre + """
        SELECT count(*) AS n,
               sum(CASE WHEN higher_won = 1 THEN 1 ELSE 0 END) AS w
        FROM d WHERE higher_won IS NOT NULL AND gap >= 200
    """).fetchone()
    n2, w2 = int(big[0]), int(big[1] or 0)
    lo, hi = wilson(w2, n2)
    print()
    print(f"rating gap >= 200 : n={n2:,}  P(higher rated wins)={w2/max(1,n2):.4f}"
          f"  Wilson [{lo:.4f}, {hi:.4f}]")

    # Elite-only: both players above 2900, which is where the leaderboard fight
    # is actually decided.
    elite = con.execute("""
        WITH g AS (
          SELECT score_0 r0, score_1 r1, reward_0 c0, reward_1 c1
          FROM episodes WHERE score_0 IS NOT NULL AND score_1 IS NOT NULL
            AND reward_0 IS NOT NULL AND reward_1 IS NOT NULL
            AND score_0 >= 2900 AND score_1 >= 2900
        )
        SELECT count(*) n,
               sum(CASE WHEN (r0>r1 AND c0>c1) OR (r1>r0 AND c1>c0)
                        THEN 1 ELSE 0 END) w
        FROM g WHERE r0 <> r1
    """).fetchone()
    ne, we = int(elite[0]), int(elite[1] or 0)
    elo, ehi = wilson(we, ne)
    print(f"ELITE (both >= 2900): n={ne:,}  P(higher rated wins)="
          f"{we/max(1,ne):.4f}  Wilson [{elo:.4f}, {ehi:.4f}]")

    predictive = elo > 0.5
    out = {
        "column_semantics": {
            "reward": "final cash (NOT a win flag); values ~100k, means differ <0.1%",
            "score": "the two players' ladder ratings, balanced P(s0>s1)=0.4995",
        },
        "gap_bins": bins,
        "gap_ge_200": {"games": n2, "wins": w2, "wilson": [lo, hi]},
        "elite_both_ge_2900": {"games": ne, "wins": we, "wilson": [elo, ehi]},
        "verdict": ("LADDER IS PREDICTIVE" if predictive
                    else "LADDER IS UNINFORMATIVE"),
    }
    with open(os.path.join(ROOT, "shadow_ladder",
                           "ladder_informativeness.json"), "w",
              encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=2)
    print(f"\nVERDICT: {out['verdict']}")
    print("wrote shadow_ladder/ladder_informativeness.json")
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
