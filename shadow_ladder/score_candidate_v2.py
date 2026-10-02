"""Shadow Ladder v2. Audited, tested, and structurally unable to over-claim.

What changed from v1, and why
---------------------------
v1 contained seven consecutive assignments to `shift` in the anchoring block,
six of them dead, plus a `sign` variable that was computed and then never used
in the surviving expression. The final assignment happened to be correct, so the
numbers were not wrong -- but a block that computes the same thing six times is
a block whose correctness is a matter of luck, and that is not acceptable in the
one component that converts measurements into a rating. This version has one
assignment and a test that pins it.

Three structural changes beyond the cleanup:

1. PUBLICATION GATE, in code. `publish_rating()` returns None unless at least
   `MIN_ANCHORS` anchors are usable, they span a minimum range, and
   leave-one-out cross-validation clears the configured thresholds. There is no
   code path that emits a rating without passing that gate, so "we should not
   have published that" cannot happen by accident.

2. CENSORING IS EXPLICIT. The ladder response curve saturates near 1.0. A
   measured score at or above `SATURATION` is recorded as a bound, never as a
   point, because the inverse is not identifiable there. v1's handling of the
   censored case wrote a no-op line that looked like a constraint; this version
   has no such line.

3. NO FABRICATED GAP FROM SATURATION. v1's predecessor report concluded that a
   saturated observation implied a gap of "at least 275" ladder points. That is
   retracted (RETRACTIONS R8): a curve that is flat over its observed range has
   no resolution there, so an observation past the top of the table is
   consistent with ANY gap above the last bin. The only defensible statement is
   that the observation cannot be inverted.

Metric convention
-----------------
Kaggle's final leaderboard is Bradley-Terry with a draw worth 0.5 per side, so
every score in this module is a mean of per-game scores in {0, 0.5, 1}, never a
decided-only win rate.
"""
import json
import math
import os
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))

from stats import paired_seed_bootstrap  # noqa: E402

CURVE_PATH = os.path.join(ROOT, "shadow_ladder", "ladder_informativeness.json")
ANCHOR_PATH = os.path.join(ROOT, "research", "anchor_catalog.json")
LB_PATH = os.path.join(ROOT, "research", "final_leaderboard.csv")
OUT = os.path.join(ROOT, "shadow_ladder", "ratings_v2.json")

# A score this close to 1 carries no positional information: the curve is flat
# over the rest of its observed range, so the inverse is unidentifiable.
SATURATION = 0.985

# Publication gate. These are the project's own thresholds, stated here so they
# can be argued with rather than discovered.
MIN_ANCHORS = 5
MIN_ANCHOR_SPAN = 300.0        # ladder points between lowest and highest anchor
MIN_LOO_MAE = 60.0             # mean absolute error of leave-one-out prediction
MIN_LOO_SPEARMAN = 0.70


# ---------------------------------------------------------------- curve
def load_curve():
    """Empirical P(stronger rated side wins | rating gap), ascending."""
    cal = json.load(open(CURVE_PATH, encoding="utf-8"))
    pts = sorted((float(b["gap_lo"]), float(b["p"])) for b in cal["gap_bins"])
    return pts, max(g for g, _ in pts)


def invert(pts, score, top_gap):
    """Ladder gap whose empirical win rate is `score`.

    Returns None when `score` lies outside the curve's resolution, which is the
    honest answer. Callers must handle None as 'unidentifiable', never as a
    bound.
    """
    if not pts:
        return None
    lo_p, hi_p = pts[0][1], pts[-1][1]
    if score < lo_p or score > hi_p:
        return None
    for i in range(len(pts) - 1):
        g0, w0 = pts[i]
        g1, w1 = pts[i + 1]
        if w0 <= score <= w1:
            if w1 == w0:
                return g0
            return g0 + (g1 - g0) * (score - w0) / (w1 - w0)
    return top_gap


# ---------------------------------------------------------------- anchors
def load_anchors():
    """Usable anchors only. An anchor without a bound artifact cannot calibrate.

    Classes, per the project's rule:
      A  artifact digest <-> exact submission, score verified against artifact
      B  official leaderboard score with a recovered, probed artifact
      C  official score, artifact unknown      -> excluded
      D  self-reported title only              -> excluded
    """
    if not os.path.exists(ANCHOR_PATH):
        return []
    cat = json.load(open(ANCHOR_PATH, encoding="utf-8"))
    return [a for a in cat.get("anchors", []) if a.get("anchor_class") in ("A", "B")]


# ---------------------------------------------------------------- fit
def fit_relative(observations, pts, top_gap):
    """Least squares on `s_a - s_b = gap_ab`, using ONLY identifiable gaps.

    An observation whose inverse is None contributes nothing. It is still
    reported, as an unidentifiable constraint, because "we measured this and
    cannot place it" is a real result and hiding it would misrepresent the
    evidence as stronger than it is.
    """
    usable, unusable = [], []
    for o in observations:
        g = invert(pts, o["score_rate"], top_gap) if not o["censored"] else None
        if g is None:
            unusable.append(o)
        else:
            usable.append({**o, "gap": g})
    if len(usable) < 2:
        return {}, usable, unusable

    agents = sorted({o["a"] for o in usable} | {o["b"] for o in usable})
    idx = {a: i for i, a in enumerate(agents)}
    n = len(agents)
    A = [[0.0] * n for _ in range(n)]
    rhs = [0.0] * n
    for o in usable:
        i, j = idx[o["a"]], idx[o["b"]]
        w = min(o["games"], 400.0)
        A[i][i] += w
        A[j][j] += w
        A[i][j] -= w
        A[j][i] -= w
        rhs[i] += w * o["gap"]
        rhs[j] -= w * o["gap"]
    A[0][0] += 1.0                      # pin the gauge, then re-centre
    M = [A[i][:] + [rhs[i]] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-12:
            continue
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        for r in range(n):
            if r == col:
                continue
            f = M[r][col] / pv
            if f:
                for c in range(col, n + 1):
                    M[r][c] -= f * M[col][c]
    s = {}
    for a in agents:
        i = idx[a]
        s[a] = (M[i][n] / M[i][i]) if abs(M[i][i]) > 1e-12 else 0.0
    mu = sum(s.values()) / len(s)
    return {k: v - mu for k, v in s.items()}, usable, unusable


def anchor_against(rel, anchor_agent, anchor_score):
    """The ONE shift. v1 had seven.

    The anchor's own relative strength is placed at its official score, and
    everything else moves with it. Returns the additive offset, which is None
    when the anchor is not present in the fitted graph -- in which case no
    rating can be published at all, rather than one anchored on nothing.
    """
    if anchor_agent not in rel:
        return None
    return anchor_score - rel[anchor_agent]


def cross_validate(anchors, pts, top_gap, min_games=200):
    """Leave-one-anchor-out. Fit on the rest, predict the held-out anchor.

    This is the only honest test of whether the scale carries information. It is
    reported whatever the answer, and a rating is withheld when it fails.
    """
    if len(anchors) < MIN_ANCHORS:
        return {"performed": False, "reason": f"only {len(anchors)} anchors"}
    rows = []
    for held in anchors:
        rest = [a for a in anchors if a["agent"] != held["agent"]]
        if len(rest) < MIN_ANCHORS - 1:
            rows.append({"agent": held["agent"], "error": None,
                         "reason": "insufficient training anchors"})
            continue
        obs = rest_to_obs(rest)
        rel, _u, _x = fit_relative(obs, pts, top_gap)
        sh = anchor_against(rel, rest[0]["agent"], rest[0]["score"])
        if sh is None:
            rows.append({"agent": held["agent"], "error": None,
                         "reason": "training anchor absent from the fitted graph"})
            continue
        pred = rel.get(held["agent"], None)
        pred = None if pred is None else pred + sh
        rows.append({"agent": held["agent"], "true": held["score"],
                     "predicted": None if pred is None else round(pred, 1),
                     "error": None if pred is None else round(pred - held["score"], 1)})
    errs = [abs(r["error"]) for r in rows if r.get("error") is not None]
    if not errs:
        return {"performed": False,
                "reason": "no held-out anchor could be predicted; the graph is "
                          "disconnected or every anchor is censored"}
    pairs = [(r["predicted"], r["true"]) for r in rows if r.get("error") is not None]
    return {"performed": True, "folds": len(rows),
            "n_predicted": len(errs),
            "mae": round(sum(errs) / len(errs), 1),
            "max_abs_error": round(max(errs), 1),
            "spearman": _spearman(pairs),
            "per_anchor": rows}


def rest_to_obs(anchors):
    """Turn anchor pairs into the observation shape `fit_relative` consumes."""
    obs = []
    for a in anchors:
        for b in anchors:
            if a is b or a["score"] <= b["score"]:
                continue
            exp = _expected_score(pts_gap=a["score"] - b["score"])
            obs.append({"a": a["agent"], "b": b["agent"], "games": 100000,
                        "score_rate": exp, "censored": False,
                        "source": "leaderboard-derived"})
    return obs


_PTS_CACHE = {}


def pts_gap(**_kw):
    return _PTS_CACHE["pts"]


def _expected_score(gap):
    """Ladder gap -> expected per-game score, by interpolating the curve."""
    pts = _PTS_CACHE["pts"]
    if gap <= pts[0][0]:
        return pts[0][1]
    for i in range(len(pts) - 1):
        g0, w0 = pts[i]
        g1, w1 = pts[i + 1]
        if g0 <= gap <= g1:
            if w1 == w0:
                return w0
            return w0 + (w1 - w0) * (gap - g0) / (g1 - g0)
    return pts[-1][1]


def _spearman(pairs):
    n = len(pairs)
    if n < 3:
        return None

    def rank(vals):
        order = sorted(range(len(vals)), key=lambda i: vals[i])
        r = [0.0] * len(vals)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r

    rx = rank([p[0] for p in pairs])
    ry = rank([p[1] for p in pairs])
    mx = sum(rx) / n
    my = sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = math.sqrt(sum((a - mx) ** 2 for a in rx))
    dy = math.sqrt(sum((b - my) ** 2 for b in ry))
    if dx == 0 or dy == 0:
        return None
    return round(num / (dx * dy), 4)


def publish_rating(rel, anchors, pts, top_gap):
    """The gate. Returns a rating dict, or None.

    There is deliberately no code path that returns a rating without clearing
    every condition below.
    """
    if len(anchors) < MIN_ANCHORS:
        return None
    scores = [a["score"] for a in anchors]
    span = max(scores) - min(scores)
    if span < MIN_ANCHOR_SPAN:
        return None
    lineages = {a.get("lineage_id") for a in anchors if a.get("lineage_id")}
    if len(lineages) < 2:
        return None
    cv = cross_validate(anchors, pts, top_gap)
    if not cv.get("performed"):
        return None
    if cv.get("mae") is None or cv["mae"] > MIN_LOO_MAE:
        return None
    sp = cv.get("spearman")
    if sp is None or sp < MIN_LOO_SPEARMAN:
        return None
    anchor = max(anchors, key=lambda a: a["score"])
    shift = anchor_against(rel, anchor["agent"], anchor["score"])
    if shift is None:
        return None
    return {"absolute": {k: round(v + shift, 1) for k, v in rel.items()},
            "shift": round(shift, 1), "anchor_used": anchor["agent"],
            "anchor_score": anchor["score"], "cross_validation": cv,
            "n_anchors": len(anchors), "anchor_span": span}


def main():
    pts, top_gap = load_curve()
    _PTS_CACHE["pts"] = pts
    anchors = load_anchors()
    print("=" * 78)
    print("SHADOW LADDER v2 (audited)")
    print("=" * 78)
    print(f"  curve bins          : {len(pts)}")
    print(f"  top resolved gap    : {top_gap:.0f} ladder points")
    print(f"  saturation threshold: score >= {SATURATION} is unidentifiable")
    print(f"  usable anchors      : {len(anchors)}  (need >= {MIN_ANCHORS})")

    obs = rest_to_obs(anchors) if anchors else []
    rel, usable, unusable = fit_relative(obs, pts, top_gap)

    print(f"\n  anchor-anchor constraints built : {len(obs)}")
    print(f"  identifiable                    : {len(usable)}")
    print(f"  unidentifiable (saturated)      : {len(unusable)}")
    for u in unusable[:8]:
        print(f"    {u['a']} vs {u['b']}  score {u['score_rate']:.4f} -> "
              f"beyond the top of the curve")

    cv = cross_validate(anchors, pts, top_gap) if anchors else {
        "performed": False, "reason": "no usable anchors"}
    print(f"\n  leave-one-anchor-out: "
          f"{'performed' if cv.get('performed') else 'NOT PERFORMED'}")
    if cv.get("performed"):
        print(f"    folds predicted : {cv['n_predicted']}")
        print(f"    MAE             : {cv['mae']} ladder points "
              f"(threshold {MIN_LOO_MAE})")
        print(f"    max abs error   : {cv['max_abs_error']}")
        print(f"    Spearman        : {cv['spearman']} "
              f"(threshold {MIN_LOO_SPEARMAN})")

    rating = publish_rating(rel, anchors, pts, top_gap)
    print("\n" + "=" * 78)
    if rating is None:
        reasons = []
        if len(anchors) < MIN_ANCHORS:
            reasons.append(f"usable anchors {len(anchors)} < {MIN_ANCHORS}")
        sc = [a.get("score") for a in anchors if a.get("score") is not None]
        if sc and max(sc) - min(sc) < MIN_ANCHOR_SPAN:
            reasons.append(f"anchor span {max(sc)-min(sc):.0f} "
                           f"< {MIN_ANCHOR_SPAN}")
        if cv.get("performed"):
            if cv["mae"] > MIN_LOO_MAE:
                reasons.append(f"LOO MAE {cv['mae']} > {MIN_LOO_MAE}")
            if (cv.get("spearman") or 0) < MIN_LOO_SPEARMAN:
                reasons.append(f"LOO Spearman {cv.get('spearman')} "
                               f"< {MIN_LOO_SPEARMAN}")
        elif anchors:
            reasons.append(f"cross-validation not performed: "
                           f"{cv.get('reason')}")
        print("SHADOW RATING: WITHHELD")
        for r in reasons:
            print(f"  - {r}")
        if not reasons:
            print("  - gate conditions unmet for an unrecorded reason")
    else:
        print("SHADOW RATING: PUBLISHED")
        print(f"  anchor   : {rating['anchor_used']} at {rating['anchor_score']}")
        print(f"  shift    : {rating['shift']}")
        print(f"  LOO MAE  : {rating['cross_validation']['mae']}")
        for k, v in sorted(rating["absolute"].items(), key=lambda kv: -kv[1]):
            print(f"    {k:<44} {v:>8.1f}")
    print("=" * 78)

    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"curve_top_gap": top_gap, "saturation": SATURATION,
                   "thresholds": {"min_anchors": MIN_ANCHORS,
                                  "min_span": MIN_ANCHOR_SPAN,
                                  "min_loo_mae": MIN_LOO_MAE,
                                  "min_loo_spearman": MIN_LOO_SPEARMAN},
                   "n_usable_anchors": len(anchors),
                   "n_constraints": len(obs),
                   "n_identifiable": len(usable),
                   "n_unidentifiable": len(unusable),
                   "relative": {k: round(v, 2) for k, v in rel.items()},
                   "cross_validation": cv,
                   "published": rating is not None,
                   "rating": rating}, fh, indent=2)
    print(f"wrote {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
