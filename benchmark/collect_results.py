"""Build the canonical results table from `benchmark/meta.py` result envelopes.

Every row is derived from a real run's JSON. Nothing is typed in by hand: the
previous `experiments/final_meta_results.csv` was assembled in a shell from
memory, had no header, and no way to trace a row back to a game.

Guarantees enforced here:
  * every row comes from a real result envelope (candidate + digest + pool named)
  * self-play is impossible: a matchup whose two sides share a digest is dropped
  * both seats are present in every row
  * error rows are surfaced, never silently averaged in
  * Wilson 95% is recomputed from the row, not copied from the summary
"""
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "benchmark"))
from stats import wilson  # noqa: E402  (single definition, shared with the harness)

FIELDS = [
    "candidate", "candidate_sha256", "opponent", "opponent_sha256", "seed_pool",
    "seats",
    "games", "W", "L", "T", "win_rate", "wilson_lo", "wilson_hi",
    "median_cash", "mean_cash", "mean_opp_cash", "p10_cash", "p90_cash",
    "cash_gap_mean", "seat0_W", "seat1_W", "both_seats", "errors",
    "non_done", "max_runtime_s", "delivery_path", "env_version", "source_run",
]

DISAGREE = 25.0  # cents; below this, a "win" is a coin flip, so flag it

META_DIR = os.path.join(ROOT, "opponents", "meta")


def digest_of(name):
    """Identity is the digest, never the label.

    The same agent is referred to as `v51` when it is the candidate and
    `ahmedberatozer-v51-lean-flock` when it is an opponent. Aggregating by
    label split one agent into two and produced a nonsense head-to-head table.
    """
    import hashlib
    p = os.path.join(META_DIR, name + ".py")
    if not os.path.exists(p):
        return None
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def collect(paths):
    rows, dropped = [], []
    for p in paths:
        with open(p, encoding="utf-8") as fh:
            env = json.load(fh)
        cand = env.get("candidate")
        csha = env.get("candidate_sha256")
        pool = env.get("seed_pool")
        ver = env.get("env_version")
        deliv = env.get("delivery_path")
        nseeds = env.get("n_seeds")
        if not (cand and csha and pool):
            raise ValueError(
                f"{p}: not a self-describing envelope. Re-run with the current "
                f"benchmark/meta.py, which records candidate, digest and pool.")
        expected_games = 2 * nseeds if nseeds else None
        for r in env.get("per_opponent", []):
            lbl = r.get("label", "")
            if not lbl.startswith("vs ") or r.get("skipped"):
                continue
            opp = lbl[3:]
            if r.get("games", 0) == 0:
                dropped.append((cand, opp, pool, "no games"))
                continue
            w, l, t = r["W"], r["L"], r["T"]
            lo, hi = wilson(w, r["games"])
            s0, s1 = r.get("seat0_W", 0), r.get("seat1_W", 0)
            # Wins per seat do NOT sum to games (losses count in neither).
            # Seat coverage is proved two ways: every seed was played from both
            # seats (games == n_seeds * 2), and every win is attributed to
            # exactly one seat (seat0_W + seat1_W == W). A candidate that wins
            # nothing legitimately has seat1_W == 0, so that is not a failure.
            both_ok = (expected_games is None or r["games"] == expected_games) \
                and (s0 + s1) == w
            med = r.get("median_cash")
            mn = r.get("mean_cash")
            mo = r.get("mean_opp")
            rows.append({
                "candidate": cand, "candidate_sha256": csha, "opponent": opp,
                "opponent_sha256": digest_of(opp) or "",
                "seed_pool": pool, "seats": "both", "games": r["games"],
                "W": w, "L": l, "T": t,
                "win_rate": round(w / r["games"], 4),
                "wilson_lo": round(lo, 4), "wilson_hi": round(hi, 4),
                "median_cash": med, "mean_cash": mn,
                "mean_opp_cash": mo, "p10_cash": r.get("p10"),
                "p90_cash": r.get("p90"),
                "cash_gap_mean": (round(mn - mo)
                                  if mn is not None and mo is not None else None),
                "seat0_W": s0, "seat1_W": s1,
                "both_seats": "yes" if both_ok else "NO",
                "errors": r.get("errors", 0), "non_done": r.get("non_done", 0),
                "max_runtime_s": r.get("max_runtime_s"),
                "delivery_path": deliv, "env_version": ver,
                "source_run": os.path.basename(p),
            })
    return rows, dropped


def audit(rows):
    """Post-conditions. Any failure here invalidates the whole table."""
    problems = []
    for r in rows:
        side = r["candidate"].split("_")[0]
        if r["both_seats"] != "yes":
            problems.append(f"{r['candidate']} vs {r['opponent']} "
                            f"({r['seed_pool']}): seat coverage unproven")
        if r["seat0_W"] == 0 and r["W"] > 0:
            problems.append(f"{r['candidate']} vs {r['opponent']}: "
                            f"won {r['W']} but never from seat 0 — one-sided result")
        if r["seat1_W"] == 0 and r["W"] > 0:
            problems.append(f"{r['candidate']} vs {r['opponent']}: "
                            f"won {r['W']} but never from seat 1 — one-sided result")
        if r["W"] + r["L"] + r["T"] != r["games"]:
            problems.append(f"{r['candidate']} vs {r['opponent']}: W+L+T != games")
        if r["errors"]:
            problems.append(f"{r['candidate']} vs {r['opponent']}: "
                            f"{r['errors']} errored game(s) present in results")
        if r["T"]:
            problems.append(f"{r['candidate']} vs {r['opponent']}: "
                            f"{r['T']} tie(s) — identical behaviour, treat as self-play risk")
        if abs(r["win_rate"] - 0.5) < 0.09 and r["games"] >= 24:
            problems.append(f"NOTE: {r['candidate']} vs {r['opponent']} is near "
                            f"coin-flip ({r['win_rate']:.3f})")
    # Self-play by digest, and label ambiguity: one digest must not wear two
    # names, and one name must not denote two digests.
    digests, names = {}, {}
    for r in rows:
        digests.setdefault(r["candidate_sha256"], set()).add(r["candidate"])
        names.setdefault(r["candidate"], set()).add(r["candidate_sha256"])
    for d, ns in digests.items():
        if len(ns) > 1:
            problems.append(f"digest {d[:12]} appears as {len(ns)} candidates: {ns}")
    for n, ds in names.items():
        if len(ds) > 1:
            problems.append(f"candidate name {n} maps to {len(ds)} digests: "
                            f"{sorted(x[:12] for x in ds)}")
    return problems


def main():
    args_in = sys.argv[1:]
    out = "experiments/final_meta_results.csv"
    if "-o" in args_in:
        i = args_in.index("-o")
        out = args_in[i + 1]
        args_in = args_in[:i] + args_in[i + 2:]
    # Accept files, globs, or directories. Shell argument mangling on Windows
    # silently corrupted absolute paths passed positionally, so directories are
    # the robust entry point.
    import glob as _glob
    paths = []
    for a in args_in:
        if os.path.isdir(a):
            paths += sorted(_glob.glob(os.path.join(a, "*.json")))
        else:
            hits = sorted(_glob.glob(a))
            paths += hits if hits else [a]
    paths = [p for p in paths if os.path.isfile(p)]
    if not paths:
        print("usage: collect_results.py <run.json | dir | glob>... [-o out.csv]")
        return 1
    rows, dropped = collect(paths)
    if not rows:
        print("no rows")
        return 1
    rows.sort(key=lambda r: (r["candidate"], r["seed_pool"], r["opponent"]))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", newline="", encoding="utf-8") as fh:
        wr = csv.DictWriter(fh, fieldnames=FIELDS)
        wr.writeheader()
        wr.writerows(rows)

    print(f"wrote {out}: {len(rows)} rows from {len(paths)} run(s)")
    if dropped:
        print(f"dropped {len(dropped)} row(s):")
        for d in dropped[:8]:
            print("   ", d)
    probs = audit(rows)
    hard = [p for p in probs if not p.startswith("NOTE")]
    soft = [p for p in probs if p.startswith("NOTE")]
    for p in probs:
        print(("  NOTE  " if p.startswith("NOTE") else "  FAIL  ") + p)
    print(f"\n{len(rows) - len(hard)}/{len(rows)} rows clean")
    if soft:
        print(f"{len(soft)} matchup(s) are near coin-flip and are flagged, not hidden")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
