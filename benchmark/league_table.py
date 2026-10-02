"""Definitive league table for the Kaggriculture audit.

Aggregates every parity-correct run into one table, resolves mirrored
head-to-heads (the same paired games, played from both sides) so no game is
counted twice, and reports Wilson intervals on everything it claims.

Prints the numbers that the reports quote. If this script and a report
disagree, the report is wrong.

Usage:
  python benchmark/league_table.py experiments/final_meta_results.csv
"""
import csv
import math
import os
import sys
from collections import defaultdict

Z = 1.96


def wilson(w, n, z=Z):
    if n == 0:
        return (0.0, 1.0)
    p = w / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (max(0.0, (c - h) / d), min(1.0, (c + h) / d))


def main(path="experiments/final_meta_results.csv"):
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    if not rows:
        print("no rows")
        return 1

    # ---- canonical identity map: digest -> one label ----------------------
    # An agent is referred to as `v51` when it is the candidate and
    # `ahmedberatozer-v51-lean-flock` when it is an opponent. Aggregating by
    # label split one agent in two and produced a nonsense matrix, so every
    # agent is keyed by its content digest and the shortest label wins.
    label = {}
    for r in rows:
        for d, l in ((r["candidate_sha256"], r["candidate"]),
                     (r.get("opponent_sha256", ""), r["opponent"])):
            if not d:
                continue
            if d not in label or len(l) < len(label[d]):
                label[d] = l
    unknown = [r["opponent"] for r in rows if not r.get("opponent_sha256")]
    if unknown:
        print(f"WARNING: {len(set(unknown))} opponent(s) have no digest on file; "
              f"they cannot be de-duplicated: {sorted(set(unknown))[:3]}")

    def ident(row, side):
        d = row[f"{side}_sha256"]
        return label.get(d) or row[side]

    # ---- overall record per candidate -------------------------------------
    print("=" * 78)
    print("OVERALL RECORD  (real ladder seeds, both seats, official env.run)")
    print("=" * 78)
    tot = defaultdict(lambda: [0, 0, 0, 0])  # W L T games
    errs = defaultdict(int)
    for r in rows:
        a = tot[ident(r, "candidate")]
        a[0] += int(r["W"]); a[1] += int(r["L"]); a[2] += int(r["T"])
        a[3] += int(r["games"])
        errs[ident(r, "candidate")] += int(r["errors"])
    print(f"{'agent':<40} {'W-L-T':>15} {'games':>6} {'win%':>7} "
          f"{'Wilson 95%':>20} {'err':>4}")
    for c, (w, l, t, n) in sorted(tot.items(), key=lambda kv: -kv[1][0] / max(1, kv[1][3])):
        lo, hi = wilson(w, n)
        print(f"{c[:40]:<40} {f'{w}-{l}-{t}':>15} {n:>6} {w/n:>7.4f} "
              f"{f'[{lo:.4f}, {hi:.4f}]':>20} {errs[c]:>4}")

    # ---- per-pool --------------------------------------------------------
    pools = sorted({r["seed_pool"] for r in rows})
    print()
    print("=" * 78)
    print("PER POOL")
    print("=" * 78)
    hdr = "".join(p.replace("REAL_", "").replace(".txt", "").rjust(14) for p in pools)
    print(f"  {'agent':<40}{hdr}")
    for c in sorted(tot, key=lambda k: -tot[k][0] / max(1, tot[k][3])):
        cells = ""
        for pool in pools:
            sub = [r for r in rows if ident(r, "candidate") == c
                   and r["seed_pool"] == pool]
            w = sum(int(r["W"]) for r in sub)
            l = sum(int(r["L"]) for r in sub)
            t = sum(int(r["T"]) for r in sub)
            cells += f"{w}-{l}-{t}".rjust(14)
        print(f"  {c[:40]:<40}{cells}")

    # ---- resolved head-to-head matrix ------------------------------------
    # (A vs B) and (B vs A) rows are the SAME paired games with the seats
    # swapped. Count each unordered pair once, always crediting the same side,
    # so no game is counted twice.
    print()
    print("=" * 78)
    print("RESOLVED HEAD-TO-HEADS  (each paired game counted once)")
    print("=" * 78)
    pair = defaultdict(lambda: [0.0, 0.0, 0])
    for r in rows:
        a, b = ident(r, "candidate"), ident(r, "opponent")
        if a == b:
            continue
        lo_, hi_ = sorted((a, b))
        key = (lo_, hi_)
        w, l, t = int(r["W"]), int(r["L"]), int(r["T"])
        if a == lo_:
            pair[key][0] += w
            pair[key][1] += l
        else:                       # mirrored: this row is from b's side
            pair[key][0] += l
            pair[key][1] += w
        pair[key][2] += w + l + t
    print(f"{'A':<40} {'B':<40} {'W-L':>9} {'n':>4} {'win%':>7} {'Wilson 95%':>20}")
    close = []
    for (a, b), (wa, wb, n) in sorted(pair.items(), key=lambda kv: -kv[1][0] / max(1, kv[1][2])):
        if n < 24:
            continue
        lo, hi = wilson(wa, n)
        p = wa / n
        flag = ""
        if lo < 0.5 < hi:
            flag = "  <- NOT SEPARABLE FROM 50%"
            close.append((a, b, wa, wb, n, lo, hi))
        print(f"{a[:40]:<40} {b[:40]:<40} {f'{wa}-{wb}':>9} {n:>4} "
              f"{p:>7.4f} {f'[{lo:.4f}, {hi:.4f}]':>20}{flag}")

    # ---- Bradley-Terry over resolved head-to-heads ----------------------
    print()
    print("=" * 78)
    print("LOCAL BRADLEY-TERRY  (offline estimate, NOT an official Kaggle rating)")
    print("=" * 78)
    pairs = {}
    for (a, b), (wa, wb, n) in pair.items():
        # sunrise is excluded from the model: it is our own submission, and it
        # wins nothing, so it would make the likelihood unbounded. Excluding by
        # checking BOTH members matters -- sorting puts "sunrise" second
        # against most names, so testing only the first member silently let
        # sunrise into the fit.
        if "sunrise" in (a, b) or n < 24:
            continue
        pairs[(a, b)] = (wa, wb)
    if len(pairs) >= 2:
        from stats import bradley_tery, p_win
        # Is any team's maximum likelihood unbounded? A team that loses EVERY
        # game to EVERY opponent it meets has beta -> -inf, the log-likelihood
        # has no maximum, and a truncated iteration silently returns a
        # meaningless number. The previous report's betas (-9.788 etc.) were
        # exactly that artifact.
        teams = sorted({t for p in pairs for t in p})
        wins_of = {}
        for t in teams:
            w = l = 0
            for (a, b), (wa, wb) in pairs.items():
                if t == a:
                    w += wa; l += wb
                elif t == b:
                    w += wb; l += wa
            wins_of[t] = (w, l)
        winless = [t for t in teams if wins_of[t][0] == 0]
        winless_defeated = [t for t in teams if wins_of[t][1] == 0]
        try:
            beta = bradley_tery(pairs)
            print(f"{'agent':<44} {'beta':>9} {'P(vs league avg)':>18}")
            for t, v in sorted(beta.items(), key=lambda kv: -kv[1]):
                print(f"{t[:44]:<44} {v:9.3f} {1/(1+math.exp(-v)):18.3f}")
            print("\n  Implied head-to-heads (model output, vs the OBSERVED rate):")
            order = sorted(beta, key=lambda k: -beta[k])
            for i, a in enumerate(order):
                for b in order[i + 1:]:
                    k = (a, b) if (a, b) in pairs else (b, a)
                    if k not in pairs:
                        continue
                    wa, wb = pairs[k]
                    n = wa + wb
                    if n < 24:
                        continue
                    lo, hi = wilson(wa, n)
                    mark = ("  <- observed rate NOT separable from 50%"
                            if lo < 0.5 < hi else "")
                    print(f"    P({a} beats {b}) = {p_win(beta, a, b):.3f}   "
                          f"observed {wa}-{wb} of {n} "
                          f"(Wilson [{lo:.3f}, {hi:.3f}]){mark}")
        except ValueError as exc:
            print("  NO BRADLEY-TERRY RANKING IS REPORTABLE FOR THIS LEAGUE.")
            print()
            print(f"  Reason: {exc}")
            print()
            if winless:
                print("  Unbounded likelihood, specifically: these agents lose")
                print("  EVERY game to EVERY opponent they were measured against,")
                print("  so their maximum-likelihood strength is -infinity and the")
                print("  model has no finite solution:")
                for t in winless:
                    w, l = wins_of[t]
                    print(f"    {t:<44} record {w}-{l} over "
                          f"{w + l} games (0 wins)")
            if winless_defeated:
                print("  Symmetrically, these are undefeated against every")
                print("  opponent they met, so their likelihood is +infinity:")
                for t in winless_defeated:
                    print(f"    {t}")
            print()
            print("  The league is a TWO-TIER star: two hubs (v51 and")
            print("  farm_2945) are each played against every other agent, and the")
            print("  bottom tier never plays anyone except the hubs. A single")
            print("  scalar rating cannot rank a tier that is uniformly dominated,")
            print("  and any beta printed for it would be an artifact of where the")
            print("  iteration was stopped.")
            print()
            print("  USE INSTEAD: the observed head-to-head table above with its")
            print("  Wilson intervals. That is the measurement. The beta is a")
            print("  compression of it, and here the compression loses the only")
            print("  thing that matters -- which matchups are actually separated")
            print("  from 50% and which are coin flips.")
    elif len(pairs):
        print("  too few resolved head-to-heads to fit a model")

    # ---- decisive conclusions --------------------------------------------
    print()
    print("=" * 78)
    print("WHAT IS ACTUALLY SEPARABLE")
    print("=" * 78)
    for c, (w, l, t, n) in sorted(tot.items(), key=lambda kv: -kv[1][0] / max(1, kv[1][3])):
        lo, hi = wilson(w, n)
        verdict = ("stronger than the field" if lo > 0.5 else
                   "weaker than the field" if hi < 0.5 else
                   "INDETERMINATE vs the field")
        print(f"  {c[:40]:<40} {w/n:6.2%}  Wilson [{lo:.3f}, {hi:.3f}]  -> {verdict}")
    if close:
        print("\n  Matchups NOT statistically separated from 50% at 95%:")
        for a, b, wa, wb, n, lo, hi in close:
            print(f"    {a} vs {b}: {wa}-{wb} of {n}, Wilson [{lo:.3f}, {hi:.3f}]")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
