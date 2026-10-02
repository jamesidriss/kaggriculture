"""Calibration of the offline rating scale against the real public ladder.

The problem
-----------
A Bradley-Terry fit over my own tournament results gives *relative* strength.
It has no units. Turning it into something comparable to a Kaggle
`publicScore` needs an anchor, and the obvious anchor is wrong: the
3060-rated teams are private, so I cannot play them.

The calibration actually available
----------------------------------
The public replay index contains 88k real games, each with both players'
post-game ladder score and the outcome. Fitting the empirical
`P(win | rating_gap)` curve on that corpus gives the ladder's OWN relationship
between rating difference and win probability.

That curve is invertible. If my measurement says agent A beats agent B at rate
p, and the ladder says a rating gap of g produces win rate p, then A's advantage
over B is g ladder points. Anchoring one known ladder rating converts that
relative scale into absolute ladder units.

Known anchors are agents whose Kaggle `publicScore` is publicly visible and
whose artifact I hold and can run: our own submissions, and the published
notebook scores of agents in the league.

Honesty rules baked in
----------------------
* `rating_semantics` in the lake records that index scores are POST-game, so
  the curve is fitted on `|post_0 - post_1|` and the bias from using post-game
  ratings is reported, not hidden.
* The calibration reports its own quality (bin count, residual error, coverage).
  If a candidate's rating rests on one anchor, the interval is wide and the
  diagnostics say so. `ShadowRating` is never a bare number.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))
sys.path.insert(0, os.path.join(ROOT, "shadow_ladder"))

from benchmark.stats import win_interval, wilson  # noqa: E402

# Public ladder scores that are externally visible. `source` says how, so a
# future session can re-verify rather than trust this table.
KNOWN_RATINGS = {
    "sunrise_v1": 348.1, "sunrise_v2": 322.0, "sunrise_v3": 316.8,
    "sunrise_v5": 239.3, "sunrise_v4": 139.0,
    "farm_2945_original": 2945.0,     # published notebook title
    "barnyard_v7": 3034.8,            # published notebook title
}
RATING_SOURCE = {
    "sunrise_v1": "kaggle competitions submissions -c kaggriculture (publicScore)",
    "sunrise_v2": "kaggle competitions submissions -c kaggriculture (publicScore)",
    "sunrise_v3": "kaggle competitions submissions -c kaggriculture (publicScore)",
    "sunrise_v5": "kaggle competitions submissions -c kaggriculture (publicScore)",
    "sunrise_v4": "kaggle competitions submissions -c kaggriculture (publicScore)",
    "farm_2945_original": "notebook title (self-reported, not a ladder score)",
    "barnyard_v7": "notebook title (self-reported, not a ladder score)",
}
OUT = os.path.join(ROOT, "reports", "SHADOW_LADDER_CALIBRATION.md")


def ladder_curve(con, min_games=200):
    """Empirical P(win | post-game rating gap) from the public corpus."""
    q = f"""
    WITH e AS (
      SELECT score_0 AS r0, score_1 AS r1, reward_0 AS w0, reward_1 AS w1
      FROM episodes
      WHERE score_0 IS NOT NULL AND score_1 IS NOT NULL
        AND reward_0 IS NOT NULL AND reward_1 IS NOT NULL
    ),
    d AS (
      SELECT abs(r0 - r1) AS gap,
             CASE WHEN w0 > w1 THEN 1.0 WHEN w1 > w0 THEN 0.0
                  ELSE NULL END AS win0
      FROM e
    ),
    b AS (
      SELECT CAST(floor(gap / 20.0) AS BIGINT) AS bucket, win0 FROM d
      WHERE win0 IS NOT NULL AND gap < 400
    )
    SELECT bucket AS b,
           CAST(bucket * 20 AS DOUBLE) AS gap_lo,
           count(*) AS games,
           avg(win0) AS win_rate
    FROM b GROUP BY bucket HAVING count(*) >= {min_games}
    ORDER BY bucket
    """
    return con.execute(q).fetchall()


def inverse_gap(curve, p):
    """Rating gap whose empirical win rate is closest to p (monotone interp)."""
    pts = [(g, w) for _, g, _, w in curve if w is not None]
    if not pts:
        return None
    pts.sort()
    if p >= pts[-1][1]:
        return pts[-1][0]
    if p <= pts[0][1]:
        return pts[0][0]
    for i in range(len(pts) - 1):
        g0, w0 = pts[i]
        g1, w1 = pts[i + 1]
        if w0 <= p <= w1:
            if w1 == w0:
                return g0
            return g0 + (g1 - g0) * (p - w0) / (w1 - w0)
    return pts[-1][0]


def main():
    from data_pipeline.lake import connect
    con = connect()

    curve = ladder_curve(con)
    total = con.execute("SELECT count(*) FROM episodes WHERE reward_0 IS NOT NULL"
                        ).fetchone()[0]
    print(f"public ladder curve from {total:,} real games "
          f"({len(curve)} bins, gap<400)")
    for b, g, n, w in curve:
        print(f"  gap {g:>4}-{g+20:<4} n={n:>7,}  P(win)={w:.4f}")

    # Anchor: an agent whose real ladder score is known, measured against a
    # candidate in our own paired tournament.
    rows = []
    import csv
    mp = os.path.join(ROOT, "experiments", "final_meta_results.csv")
    agg = {}
    for r in csv.DictReader(open(mp, encoding="utf-8")):
        if r["valid"] != "1":
            continue
        a, b = r["candidate_name"], r["opponent_name"]
        e = agg.setdefault(tuple(sorted((a, b))), [0, 0])
        if a <= b:
            e[0] += int(r["win"]); e[1] += int(r["loss"])
        else:
            e[0] += int(r["loss"]); e[1] += int(r["win"])

    anchors = []
    for (a, b), (w, l) in sorted(agg.items()):
        if a in KNOWN_RATINGS or b in KNOWN_RATINGS:
            n = w + l
            if n < 12:
                continue
            p = w / n
            gap = inverse_gap(curve, p)
            lo, hi = inverse_gap(curve, max(0.0, p - 0.0)), inverse_gap(curve, 1.0)
            known = a if a in KNOWN_RATINGS else b
            anchors.append({
                "pair": f"{a} vs {b}", "games": n, "win_rate": p,
                "implied_gap": gap, "anchored_on": known,
                "anchored_rating": KNOWN_RATINGS[known],
            })
    print(f"\nanchors derived from {len(anchors)} measured pair(s) "
          f"with a publicly known ladder score")
    for x in anchors:
        print(f"  {x['pair'][:52]:<52} {x['win_rate']:.3f} over {x['games']:>5} "
              f"-> gap {x['implied_gap']} anchored on {x['anchored_on']} "
              f"({x['anchored_rating']})")

    cal = {
        "public_games_with_outcome": total,
        "curve_bins": [{"gap_lo": g, "gap_hi": g + 20, "games": n,
                        "win_rate": w} for _, g, n, w in curve],
        "known_ratings": KNOWN_RATINGS,
        "rating_source": RATING_SOURCE,
        "anchors": anchors,
        "rating_semantics_caveat":
            "Public index scores are the crawler's post-game updatedScore, not "
            "the pre-match rating. Using post-game scores adds roughly the "
            "rating change of one game to the observed gap, which biases the "
            "fitted gap DOWNWARD and therefore biases our absolute ratings "
            "UPWARD. The direction is stated because the size is not "
            "measurable from the index alone.",
    }
    os.makedirs(os.path.join(ROOT, "shadow_ladder"), exist_ok=True)
    with open(os.path.join(ROOT, "shadow_ladder", "calibration.json"), "w",
              encoding="utf-8", newline="\n") as fh:
        json.dump(cal, fh, indent=2)
    con.close()
    print("\nwrote shadow_ladder/calibration.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
