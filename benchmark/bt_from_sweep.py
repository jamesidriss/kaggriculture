"""Bradley-Terry model from champion-vs-league sweeps (parity-safe games only).

Input: one or more --result JSON files emitted by `benchmark/meta.py`, each
containing per_opponent rows (W/L/T against the candidate). Self-play rows and
error rows are dropped.

Ties contribute 0.5 to each side. Output is an OFFLINE estimate, not an
official Kaggle ranking.
"""
import argparse
import json
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bradley_tery import fit, p_win  # noqa: E402


def load(files):
    """pairwise {(candidate, opponent): (wins_cand, wins_opp)}

    The candidate is named explicitly via --candidate; inferring it from the
    first 'vs <name>' row previously mislabelled the whole model, because that
    row is an OPPONENT, not the candidate.
    """
    pw = {}
    cand = os.environ.get("BT_CANDIDATE") or None
    for f in files:
        with open(f, encoding="utf-8") as fh:
            data = json.load(fh)
        if cand is None:
            for key in ("cand", "candidate"):
                if data.get(key):
                    cand = os.path.basename(str(data[key]))
                    break
        if cand is None:
            continue
        for row in data.get("per_opponent", []):
            lbl = row.get("label", "")
            if not lbl.startswith("vs ") or "skipped" in row:
                continue
            opp = lbl[3:]
            if opp == cand or row.get("errors"):
                continue
            if row.get("games", 0) == 0:
                continue
            w, l, t = row.get("W", 0), row.get("L", 0), row.get("T", 0)
            key = (cand, opp)
            prev = pw.get(key, (0.0, 0.0))
            pw[key] = (prev[0] + w + 0.5 * t, prev[1] + l + 0.5 * t)
    return pw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--candidate", required=True,
                    help="the agent whose sweeps are being analysed")
    args = ap.parse_args()
    os.environ["BT_CANDIDATE"] = args.candidate
    pw = load(args.files)
    if not pw:
        print("no usable results")
        return 1
    teams = sorted({t for p in pw for t in p})
    beta = fit(pw, teams)
    order = sorted(beta.items(), key=lambda kv: -kv[1])
    print(f"{'agent':<44} {'beta':>8} {'P(vs avg)':>10}")
    for t, v in order:
        print(f"{t[:44]:<44} {v:8.3f} {math.exp(v)/(1+math.exp(v)):10.3f}")
    print("\npairwise implied probabilities:")
    for i, a in enumerate(order):
        for b in order[i + 1:]:
            obs = pw.get((a, b)) or pw.get((b, a))
            o = ""
            if obs:
                tot = sum(obs)
                o = f"  observed {obs[0]:.1f}/{tot:.0f}"
            print(f"  P({a} beats {b}) = {p_win(beta, a, b):.3f}{o}")
    return 0


if __name__ == "__main__":
    sys.exit(main())