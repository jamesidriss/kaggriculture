"""Bradley-Terry strength model from pairwise results.

Offline estimate only -- NOT an official Kaggle ranking. Ties contribute 0.5
to each side. MLE via iterative MM algorithm with optional bootstrap CI.

Usage:
  python benchmark/bradley_tery.py experiments/final_meta_results.csv
  python benchmark/bradley_tery.py results.json --seedfile seeds/ladder_real_holdout.txt
"""
import argparse
import csv
import json
import math
import random
import sys


def fit(pairwise, teams=None, iters=400):
    """pairwise: {(a,b): (wins_a, wins_b)} -> {team: beta} with mean 0."""
    teams = teams or sorted({t for p in pairwise for t in p})
    n = {t: 0.0 for t in teams}          # wins (with ties halved)
    c = {t: 0.0 for t in teams}          # games
    for (a, b), (wa, wb) in pairwise.items():
        n[a] += wa
        n[b] += wb
        c[a] += wa + wb
        c[b] += wa + wb
    beta = {t: 0.0 for t in teams}
    for _ in range(iters):
        new = {}
        for t in teams:
            if c[t] == 0:
                new[t] = 0.0
                continue
            num = 0.0
            for (a, b), (wa, wb) in pairwise.items():
                for s, w, l in ((a, wa, wb), (b, wb, wa)):
                    if s != t:
                        continue
                    tot = w + l
                    if tot:
                        num += w / (1.0 + math.exp(-(beta[a] - beta[b]))) * tot
            p = beta[t]
            new[t] = num / c[t]
        mean = sum(new.values()) / len(new)
        beta = {t: v - mean for t, v in new.items()}
    return beta


def p_win(beta, a, b):
    return 1.0 / (1.0 + math.exp(-(beta[a] - beta[b])))


def bootstrap(pairwise, teams, n=400, rng_seed=7):
    rng = random.Random(rng_seed)
    keys = list(pairwise)
    out = {t: [] for t in teams}
    for _ in range(n):
        sample = {}
        for k in keys:
            wa, wb = pairwise[k]
            resample = [1] * wa + [0] * wb
            rng.shuffle(resample)
            sample[k] = (sum(resample), len(resample) - sum(resample))
        b = fit(sample, teams)
        for t in teams:
            out[t].append(b[t])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--boot", type=int, default=200)
    args = ap.parse_args()

    if args.path.endswith(".json"):
        data = json.load(open(args.path, encoding="utf-8"))
        pairwise = {tuple(k.split("|")): tuple(v) for k, v in data.items()}
        meta = []
    else:
        pairwise = {}
        meta = []
        for r in csv.DictReader(open(args.path, encoding="utf-8")):
            label = r.get("matchup", "")
            if " vs " not in label:
                continue
            a, b = [x.strip() for x in label.split(" vs ")]
            pairwise[(a, b)] = (int(r["W"]), int(r["L"]))
            meta.append(r)
    teams = sorted({t for p in pairwise for t in p})
    if len(teams) < 2:
        print("not enough matchups")
        return
    beta = fit(pairwise, teams)
    print(f"{'team':28s} {'beta':>8s} {'p(vs avg)':>10s}")
    for t, v in sorted(beta.items(), key=lambda kv: -kv[1]):
        print(f"{t[:28]:28s} {v:8.3f} {math.exp(v)/(1+math.exp(v)):10.3f}")
    print()
    for i, a in enumerate(teams):
        for b in teams[i + 1:]:
            print(f"P({a} beats {b}) = {p_win(beta, a, b):.3f}   observed "
                  f"{pairwise.get((a, b), (0, 0))[0]}/{sum(pairwise.get((a, b), (0, 0)))}")


if __name__ == "__main__":
    main()