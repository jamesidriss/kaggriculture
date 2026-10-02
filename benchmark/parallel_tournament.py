"""Parallel, cached tournament runner. Same results as the serial runner.

Why this exists
---------------
Every measurement this project needs is a large paired tournament on the OFFICIAL
Python runtime, because no verified fast backend exists. Serial execution makes
the required sample sizes unaffordable: at 8 workers the official engine sustains
roughly 36 games/minute, so a 3,000-game leg is about 85 minutes and a 512-candidate
screen is measured in hours.

Three properties are non-negotiable, because a parallel harness that quietly
changes the numbers is worse than no harness:

  1. DETERMINISTIC PROCESS ISOLATION. Each worker builds its own environment
     and loads its own copy of each agent module. No mutable agent global state
     is ever shared across matches, because a leaked global turns a search
     result into an artefact of worker scheduling.

  2. AN EXACT MATCH CACHE. (environment, agent A digest, agent B digest, seed,
     seat) fully determines a deterministic match, so a repeated game is looked
     up instead of recomputed. The cache is keyed on DIGESTS, never filenames,
     so renaming a file cannot silently invalidate or falsely reuse an entry.

  3. IDENTICAL SEMANTICS. The cache key is orientation-aware and the row schema
     is the canonical one, so a serial run and a parallel run over the same
     seeds produce the same rows. `tests/test_parallel_equivalence.py` asserts
     it rather than assuming it.

Usage
-----
    python benchmark/parallel_tournament.py --a A.py --b B.py \\
        --seeds-file seeds/GEN3066_dev.txt --out out.csv --workers 8
"""
import argparse
import csv
import hashlib
import json
import multiprocessing as mp
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))

CACHE_DIR = os.path.join(ROOT, "benchmark", "match_cache")
FIELDS = ["experiment_id", "run_id", "environment_version", "candidate_sha",
          "candidate_name", "opponent_sha", "opponent_name", "seed", "seat",
          "candidate_cash", "opponent_cash", "win", "loss", "tie",
          "candidate_status", "opponent_status", "candidate_calls",
          "opponent_calls", "candidate_actions", "opponent_actions",
          # Runtime maxima MUST be in the schema. The first version of this file
          # omitted them, so a 2,000-game run reported median latency 0.0 ms and
          # the runtime gate would have passed on missing data rather than on
          # fast agents. A gate that passes on absent data is not a gate.
          "candidate_runtime_max", "opponent_runtime_max",
          "valid", "invalid_reason", "wall_s"]

_W = {}


def env_sha():
    """Digest of the installed environment. Part of every cache key, so an
    environment upgrade invalidates the whole cache instead of mixing results
    produced under different rules."""
    try:
        from importlib.metadata import version
        v = version("kaggle-environments")
    except Exception:
        v = "unknown"
    import kaggle_environments
    pkg = os.path.dirname(kaggle_environments.__file__)
    j = os.path.join(pkg, "envs", "kaggriculture", "kaggriculture.json")
    h = hashlib.sha256()
    h.update(v.encode())
    try:
        with open(j, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
    except OSError:
        pass
    return h.hexdigest(), v


def cache_key(env, a_sha, b_sha, seed, seat):
    """Orientation-aware and digest-based.

    Orientation matters: swapping the seats changes the observation order and
    therefore the game. Including seat in the key makes a cached seat-0 row
    unusable for seat 1.
    """
    return hashlib.sha256(
        f"{env}|{a_sha}|{b_sha}|{seed}|{seat}".encode()).hexdigest()


def _init(env_name, a_path, b_path, a_name, b_name):
    """Per-worker initialisation. Runs once, in the child, before any match."""
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")
    import tournament as T
    _W["T"] = T
    _W["env_name"] = env_name
    _W["a"] = a_path
    _W["b"] = b_path
    _W["a_name"] = a_name
    _W["b_name"] = b_name


def _one(job):
    """Play exactly one (seed, seat) match. Never raises; errors become rows."""
    seed, seat = job
    T = _W["T"]
    t0 = time.time()
    try:
        r = T.play(_W["a"], _W["b"], seed, seat, _W["env_name"])
        r["wall_s"] = round(time.time() - t0, 2)
        reasons = T.validate_game(r, _W["a_name"], _W["b_name"])
        row = dict(r)
        row["valid"] = int(not reasons)
        row["invalid_reason"] = "; ".join(reasons)
        return row
    except Exception as exc:  # noqa: BLE001
        return {"candidate_cash": 0, "opponent_cash": 0, "win": 0, "loss": 0,
                "tie": 0, "candidate_status": f"ERROR {type(exc).__name__}",
                "opponent_status": "", "candidate_calls": 0,
                "opponent_calls": 0, "candidate_actions": 0,
                "opponent_actions": 0, "candidate_runtime_max": 0.0,
                "opponent_runtime_max": 0.0, "valid": 0,
                "invalid_reason": f"runner exception: {exc}"[:200],
                "wall_s": round(time.time() - t0, 2)}


def load_cache(index_path):
    idx = {}
    if os.path.exists(index_path):
        with open(index_path, encoding="utf-8") as fh:
            for line in fh:
                parts = line.rstrip("\n").split("\t")
                if len(parts) == 3:
                    idx[parts[0]] = parts[1]
    return idx


def append_cache(index_path, key, out_path):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cf = os.path.join(CACHE_DIR, key + ".json")
    with open(cf, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out_path, fh)
    with open(index_path, "a", encoding="utf-8", newline="\n") as fh:
        fh.write(f"{key}\t{out_path}\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", "--candidate", dest="a", required=True)
    ap.add_argument("--b", "--opponent", dest="b", required=True)
    ap.add_argument("--seeds-file", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--label-a", default=None)
    ap.add_argument("--label-b", default=None)
    ap.add_argument("--workers", type=int, default=0)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--resume", action="store_true")
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--experiment-id", default="parallel")
    args = ap.parse_args()

    import tournament as T
    from importlib.metadata import version
    envver = f"kaggle-environments {version('kaggle-environments')}"
    env_hash, _v = env_sha()

    # `resolve` returns (name, path); the serial runner uses the same helper so
    # the two runners resolve league names, repo paths and digest prefixes
    # identically.
    a_name, a_path = T.resolve(args.a)
    b_name, b_path = T.resolve(args.b)
    if args.label_a:
        a_name = args.label_a
    if args.label_b:
        b_name = args.label_b
    a_sha, b_sha = T.digest_of(a_path), T.digest_of(b_path)
    a_nrm, b_nrm = T.normalised_digest(a_path), T.normalised_digest(b_path)

    # RULE 1 of the harness: refuse self-play by digest, before any match.
    if a_sha == b_sha or a_nrm == b_nrm:
        print(f"ABORT: self-play refused. {a_name} and {b_name} are the same "
              f"content ({a_sha[:16]}).")
        return 2

    seeds = [int(x) for x in open(args.seeds_file, encoding="utf-8")
             if x.strip().isdigit()]
    if args.limit:
        seeds = seeds[:args.limit]

    index_path = os.path.join(CACHE_DIR, "index.tsv")
    cache = {} if args.no_cache else load_cache(index_path)

    jobs = [(s, seat) for s in seeds for seat in (0, 1)]
    todo, rows, hits = [], [], 0
    for seed, seat in jobs:
        k = cache_key(env_hash, a_sha, b_sha, seed, seat)
        if k in cache and not args.no_cache:
            try:
                with open(cache[k], encoding="utf-8") as fh:
                    rows.append(json.load(fh))
                hits += 1
            except (OSError, ValueError):
                todo.append((seed, seat))
        else:
            todo.append((seed, seat))

    run_id = hashlib.sha256(
        f"{a_sha}|{b_sha}|{args.seeds_file}|{len(seeds)}|{env_hash}".encode()
    ).hexdigest()[:16]
    workers = args.workers or min(os.cpu_count() or 4, 8)
    print(f"run_id={run_id}  env={env_hash[:12]}  workers={workers}")
    print(f"  A = {a_name}  {a_sha[:16]}")
    print(f"  B = {b_name}  {b_sha[:16]}")
    print(f"  seeds={len(seeds)}  matches={len(jobs)}  "
          f"cache_hits={hits}  to_compute={len(todo)}")

    if args.resume and os.path.exists(args.out):
        have = set()
        for r in csv.DictReader(open(args.out, encoding="utf-8")):
            have.add((int(r["seed"]), int(r["seat"])))
        rows = [r for r in rows
                if (int(r["seed"]), int(r["seat"])) not in have]

    t0 = time.time()
    if todo:
        ctx = mp.get_context("spawn")  # spawn: fresh interpreter, no inherited
                                        # agent globals
        with ctx.Pool(workers, initializer=_init,
                      initargs=("kaggriculture", a_path, b_path,
                                a_name, b_name)) as pool:
            done = 0
            for r in pool.imap_unordered(_one, todo, chunksize=1):
                done += 1
                rows.append(r)
                if not args.no_cache and "seed" in r and "seat" in r:
                    k = cache_key(env_hash, a_sha, b_sha,
                                  int(r["seed"]), int(r["seat"]))
                    cf = os.path.join(CACHE_DIR, k + ".json")
                    os.makedirs(CACHE_DIR, exist_ok=True)
                    with open(cf, "w", encoding="utf-8", newline="\n") as fh:
                        json.dump(r, fh)
                    append_cache(index_path, k, cf)
                if done % 100 == 0:
                    el = time.time() - t0
                    rate = done / max(el, 1e-9)
                    print(f"  {done}/{len(todo)}  {rate*60:.1f} matches/min  "
                          f"eta {(len(todo)-done)/max(rate,1e-9)/60:.1f} min")
    dt = time.time() - t0

    rows.sort(key=lambda r: (int(r.get("seed", 0) or 0), int(r.get("seat", 0) or 0)))
    out_path = os.path.join(ROOT, args.out)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            r.setdefault("experiment_id", args.experiment_id)
            r.setdefault("run_id", run_id)
            r.setdefault("environment_version", envver)
            r.setdefault("candidate_sha", a_sha)
            r.setdefault("candidate_name", a_name)
            r.setdefault("opponent_sha", b_sha)
            r.setdefault("opponent_name", b_name)
            w.writerow({k: r.get(k, "") for k in FIELDS})

    # summary in the canonical metric set
    sys.path.insert(0, os.path.join(ROOT, "benchmark"))
    from stats import win_interval
    v = [r for r in rows if int(r.get("valid", 0)) == 1]
    W = sum(int(r["win"]) for r in v)
    L = sum(int(r["loss"]) for r in v)
    Tt = sum(int(r["tie"]) for r in v)
    d = win_interval(W, L, Tt)
    print(f"\n=== {a_name} vs {b_name} ===")
    print(f"  matches    : {len(rows)}   valid {len(v)}   "
          f"broken {len(rows)-len(v)}")
    print(f"  W-L-T      : {W}-{L}-{Tt}")
    print(f"  BT score   : {d['bt_score_rate']:.4f}   <- PRIMARY "
          f"(ties = 0.5)")
    print(f"  decided    : {d['decided_win_rate']:.4f}   "
          f"Wilson [{d['wilson_decided_lo']:.4f}, {d['wilson_decided_hi']:.4f}]")
    print(f"  tie rate   : {d['tie_rate']:.4f}")
    print(f"  throughput : {len(todo)/max(dt,1e-9)*60:.1f} matches/min "
          f"({workers} workers, {dt/60:.1f} min)")
    print(f"  wrote      : {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
