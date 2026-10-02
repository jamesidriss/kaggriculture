"""Connected round robin so a Bradley-Terry fit becomes identifiable.

Why this exists
---------------
The previous measurement graph was a two-hub star: `v51` and `farm_2945` were
each played against every other agent, and the bottom tier played nobody except
those two hubs. Every bottom-tier agent therefore lost 100% of its games, its
maximum-likelihood strength is unbounded below, and no finite BT solution
exists. Publishing betas anyway produced six different agents sharing the
identical value -9.788, which was the visible symptom of an unconverged loop.

The fix is measurement, not modelling: play the missing cross-tier matches so
every agent both wins and loses, which is the necessary condition for a finite
MLE.

Usage:
    python benchmark/round_robin.py --agents a,b,c --seeds 6 --out ...
"""
import argparse
import csv
import hashlib
import itertools
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))

from tournament import play, resolve, digest_of, validate_game, FIELDS  # noqa: E402
from stats import win_interval, bt_identifiability, bradley_tery, bt_implied_p  # noqa: E402

META = os.path.join(ROOT, "opponents", "meta")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--agents", required=True,
                    help="comma-separated league names")
    ap.add_argument("--seeds", type=int, default=6)
    ap.add_argument("--seeds-file", default=None)
    ap.add_argument("--out", default="experiments/round_robin.csv")
    ap.add_argument("--shard", type=int, default=0)
    ap.add_argument("--num-shards", type=int, default=1)
    args = ap.parse_args()

    names = [a.strip() for a in args.agents.split(",") if a.strip()]
    paths = {n: resolve(n)[1] for n in names}
    digests = {n: digest_of(p) for n, p in paths.items()}
    for a, b in itertools.combinations(names, 2):
        if digests[a] == digests[b]:
            print(f"ABORT: {a} and {b} share content {digests[a][:16]}")
            return 2

    if args.seeds_file:
        seeds = [int(x) for x in open(args.seeds_file, encoding="utf-8")
                 if x.strip().isdigit()][: args.seeds]
    else:
        seeds = [int(x) for x in open(os.path.join(ROOT, "seeds", "REAL_dev.txt"),
                                      encoding="utf-8") if x.strip().isdigit()][: args.seeds]

    from importlib.metadata import version
    envver = f"kaggle-environments {version('kaggle-environments')}"
    pairs = list(itertools.combinations(names, 2))
    # Shard on PAIRS, not agents: sharding the agent list leaves most shards
    # with a single agent, hence zero pairs, hence no output.
    pairs = [p for i, p in enumerate(pairs) if i % args.num_shards == args.shard]
    total = len(pairs) * len(seeds) * 2
    print(f"round robin shard {args.shard}/{args.num_shards}: "
          f"{len(names)} agents, {len(pairs)} pairs, "
          f"{len(seeds)} seeds x 2 seats = {total} games")

    out_path = os.path.join(ROOT, args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    run_id = hashlib.sha256(
        ("|".join(sorted(digests.values()))
         + (args.seeds_file or "REAL_dev")).encode()
    ).hexdigest()[:16]

    fh = open(out_path, "w", newline="", encoding="utf-8")
    w = csv.DictWriter(fh, fieldnames=FIELDS)
    w.writeheader()

    t0 = time.time()
    n = 0
    for a, b in pairs:
        for seed in seeds:
            for seat in (0, 1):
                # A occupies `seat`; the pair is always played from both seats.
                r = play(paths[a], paths[b], seed, seat)
                reasons = validate_game(r, a, b)
                w.writerow({
                    "run_id": run_id, "timestamp": ts,
                    "environment_version": envver,
                    "candidate_name": a, "candidate_sha": digests[a],
                    "opponent_name": b, "opponent_sha": digests[b],
                    "seed": seed, "seat": seat, "valid": int(not reasons),
                    "invalid_reason": "; ".join(reasons),
                    **{k: r[k] for k in (
                        "candidate_cash", "opponent_cash", "win", "loss", "tie",
                        "candidate_status", "opponent_status", "candidate_calls",
                        "opponent_calls", "candidate_actions",
                        "opponent_actions", "candidate_runtime_max",
                        "opponent_runtime_max")},
                })
                n += 1
        if n % 40 == 0 or n == total:
            fh.flush()
            print(f"  {n}/{total}  {(time.time()-t0)/60:.1f} min")
    fh.close()

    rows = list(csv.DictReader(open(out_path, encoding="utf-8")))
    valid = [r for r in rows if r["valid"] == "1"]
    inv = len(rows) - len(valid)
    agg = {}
    for r in valid:
        k = tuple(sorted((r["candidate_name"], r["opponent_name"])))
        e = agg.setdefault(k, [0, 0, 0, 0])
        e[0] += int(r["win"]); e[1] += int(r["loss"]); e[2] += int(r["tie"])
        e[3] += 1
    print(f"\nvalid {len(valid)}/{len(rows)}  invalid {inv}")
    print(f"\n{'A':<34} {'B':<34} {'W-L-T':>12} {'n':>4}  Wilson 95%")
    for (a, b), (wa, lb, t, g) in sorted(agg.items(), key=lambda kv: -kv[1][0] / max(1, kv[1][3])):
        first, second = (a, b) if a < b else (b, a)
        w2 = wa if first == a else lb
        iv = win_interval(w2, g - w2 - t, t)
        print(f"{first[:34]:<34} {second[:34]:<34} {f'{w2}-{g-w2-t}-{t}':>12} "
              f"{g:>4}  [{iv['wilson_lo']:.3f}, {iv['wilson_hi']:.3f}]")

    bt = {}
    for (a, b), (wa, lb, t, g) in agg.items():
        if t == g:
            continue                      # all ties: same agent
        first, second = (a, b) if a < b else (b, a)
        w2 = wa if first == a else lb
        if w2 == 0 or w2 == g:
            continue                      # still complete separation
        bt[(first, second)] = (w2, g - w2 - t)
    ident = bt_identifiability(bt)
    print(f"\n=== BT IDENTIFIABILITY ===\n  {ident}")
    if ident["ok"]:
        beta = bradley_tery(bt)
        print(f"\n  {'agent':<44} {'beta':>9}")
        for t_, v in sorted(beta.items(), key=lambda kv: -kv[1]):
            print(f"  {t_[:44]:<44} {v:9.3f}")
        print("\n  implied head-to-heads:")
        order = sorted(beta, key=lambda k: -beta[k])
        for i, x in enumerate(order):
            for y in order[i + 1:]:
                k = (x, y) if (x, y) in bt else (y, x)
                if k in bt:
                    print(f"    P({x} > {y}) = {bt_implied_p(beta,x,y):.3f}  "
                          f"observed {bt[k][0]}-{bt[k][1]}")
    else:
        print("\n  BT still not identifiable. The pairs that remain fully")
        print("  separated are listed above; those need more games or are")
        print("  genuinely one-sided. Betas are NOT published.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
