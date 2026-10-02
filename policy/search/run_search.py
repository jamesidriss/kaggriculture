"""Exhaustive search over the reference agent's own layer stack.

Why exhaustive rather than evolutionary
---------------------------------------
The reference exposes a genuine, documented configuration surface: nine
boolean layer switches plus two numeric tunables, of which six layers are
switched OFF in the shipped configuration. The reachable set of layer
combinations is 2^9 = 512, which is small enough to enumerate COMPLETELY.

An evolutionary search over 512 points would be strictly worse than simply
evaluating all of them, and would add a stochastic failure mode to a research
programme that already has enough of them. So this is a grid search, with early
stopping applied to the evaluation budget rather than to correctness.

Fitness
-------
Never mean cash alone. The reference and the 2945 Farm are near-clones whose
banks differ by <0.5% while their head-to-head win rate is 52.4%, so cash is
close to a constant on this matchup and carries almost no signal. The primary
fitness is therefore the paired WIN RATE against the discriminating opponent,
with cash margin as a secondary tie-break.

Budget protocol
---------------
  stage 1  SMOKE   8 paired games   - reject crashes and non-players only
  stage 2  EARLY   32 paired games  - keep the top decile
  stage 3  SERIOUS 400+ paired games on the survivors, both seats

Seeds are drawn from `REAL_scale` and never from the sealed final pool.
"""
import hashlib
import itertools
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))

from benchmark.stats import win_interval, wilson  # noqa: E402

PARENT = os.path.join(ROOT, "opponents", "meta",
                      "ahmedberatozer-v51-lean-flock.py")
PARENT_SHA = "c1e3590d02e42d16091c5377e87a3db16496e5a462d558dc2925887f835f9891"
WORK = os.path.join(ROOT, "simulation", "search")
GENES = ["hand_align", "weed_repair", "sell_lead", "front_run", "budget_guard",
         "room_guard", "clamp_sells", "dead_stock", "terminal_liquidation"]
TUNABLES = {"min_sell_price": [1, 2, 3, 4], "block_turns": [48, 60, 72, 96]}

SEED_FILE = os.path.join(ROOT, "seeds", "REAL_scale.txt")
RESULTS = os.path.join(ROOT, "simulation", "search", "results.json")
OPPONENT = os.path.join(ROOT, "opponents", "meta", "farm_2945_original.py")


def settings_literal(flags, tunables=None):
    parts = [f"'{k}': {bool(flags[k])}" for k in GENES]
    for k, v in (tunables or {}).items():
        parts.append(f"'{k}': {v}")
    return "{" + ", ".join(parts) + "}"


def build(flags, tunables, path):
    src = open(PARENT, encoding="utf-8", newline="").read()
    assert hashlib.sha256(src.encode()).hexdigest() == PARENT_SHA, \
        "parent digest drift: refusing to derive candidates from it"
    lit = settings_literal(flags, tunables)
    # Replace the live settings dict. `DEFAULT_SETTINGS` is NOT the live
    # configuration: the agent is constructed with `**_SETTINGS`, which
    # overrides it. Editing DEFAULT_SETTINGS is a silent no-op.
    out, n = src.replace("_SETTINGS=", f"_SETTINGS_SEARCH={lit} + dict(_SETTINGS", 0) \
        if False else (src, 0)
    marker = "_SETTINGS={"
    i = src.index(marker)
    j = src.index("}", i)
    out = src[:i] + f"_SETTINGS={lit}" + src[j + 1:]
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(out)
    return hashlib.sha256(out.encode()).hexdigest()


def evaluate(cand_path, opponent_path, seeds, tag, jobs=8):
    """Run one candidate against the opponent, paired, both seats."""
    per = max(1, len(seeds) // jobs)
    chunks = [seeds[i * per:(i + 1) * per] for i in range(jobs)]
    chunks = [c for c in chunks if c]
    procs = []
    outdir = os.path.join(WORK, "runs", tag)
    os.makedirs(outdir, exist_ok=True)
    for i, ch in enumerate(chunks):
        sf = os.path.join(outdir, f"seeds_{i}.txt")
        with open(sf, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(str(s) for s in ch) + "\n")
        of = os.path.join(outdir, f"r_{i}.csv")
        if os.path.exists(of):
            os.remove(of)
        procs.append(subprocess.Popen(
            [sys.executable, os.path.join(ROOT, "benchmark", "tournament.py"),
             "--a", cand_path, "--b", opponent_path, "--seeds-file", sf,
             "--out", of, "--label-a", "cand"],
            cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
    for p in procs:
        p.wait()
    import csv
    rows = []
    for f in sorted(os.listdir(outdir)):
        if f.startswith("r_") and f.endswith(".csv"):
            rows += list(csv.DictReader(open(os.path.join(outdir, f),
                                            encoding="utf-8")))
    valid = [r for r in rows if r["valid"] == "1"]
    w = sum(int(r["win"]) for r in valid)
    l = sum(int(r["loss"]) for r in valid)
    t = sum(int(r["tie"]) for r in valid)
    mc = [int(r["candidate_cash"]) for r in valid]
    mo = [int(r["opponent_cash"]) for r in valid]
    iv = win_interval(w, l, t)
    return {"tag": tag, "games": len(valid), "invalid": len(rows) - len(valid),
            "W": w, "L": l, "T": t, "win_rate": iv["win_rate"],
            "wilson": [round(iv["wilson_lo"], 4), round(iv["wilson_hi"], 4)],
            "median_cash": sorted(mc)[len(mc) // 2] if mc else 0,
            "median_opp": sorted(mo)[len(mo) // 2] if mo else 0,
            "margin": (sorted(mc)[len(mc) // 2] - sorted(mo)[len(mo) // 2])
            if mc else 0}


def main():
    budget = int(sys.argv[sys.argv.index("--budget") + 1]) \
        if "--budget" in sys.argv else 64
    os.makedirs(WORK, exist_ok=True)
    seeds = [int(x) for x in open(SEED_FILE, encoding="utf-8")
             if x.strip().isdigit()]
    smoke_seeds = seeds[:8]
    early_seeds = seeds[:32]

    # The shipped configuration, as the baseline every candidate must beat.
    base_flags = {g: (g in ("hand_align", "weed_repair", "sell_lead")) for g in GENES}
    print("=" * 78)
    print("EXHAUSTIVE LAYER-STACK SEARCH over the reference's own genes")
    print("=" * 78)
    print(f"  genes     : {len(GENES)} booleans -> {2**len(GENES)} stacks")
    print(f"  baseline  : {settings_literal(base_flags)}")
    print(f"  opponent  : farm_2945_original (the only discriminating matchup)")
    print(f"  budget    : {budget} candidates")

    combos = []
    for bits in itertools.product([False, True], repeat=len(GENES)):
        flags = dict(zip(GENES, bits))
        if flags == base_flags:
            continue
        combos.append(flags)
    # Sample EVENLY across the enumeration, never take a prefix.
    # `itertools.product([False, True], ...)` emits lexicographically, so the
    # first N configurations all share the first gene's value: a prefix of 64
    # out of 512 is 64 configurations with hand_align=False and nothing else.
    # Every one of them scored 0.0000, which looked like a result and was in
    # fact a sampling bug. Even spacing over the index set guarantees each gene
    # takes both values.
    total = len(combos)
    if budget < total:
        step = total / budget
        idx = sorted({int(i * step) for i in range(budget)})
        combos = [combos[i] for i in idx]
    # Fail loudly if the sample is degenerate on any single gene.
    for g in GENES:
        vals = {c[g] for c in combos}
        if len(vals) < 2:
            print(f"  ABORT: sample is degenerate on gene {g!r} "
                  f"(only {vals}); the search would be meaningless.")
            return 2
    print(f"  sampling {len(combos)} of {total} stacks, evenly spaced")
    for g in GENES:
        print(f"    {g:<24} on in {sum(1 for c in combos if c[g]):>3}/{len(combos)}")
    print()

    results = []
    t0 = time.time()
    for i, flags in enumerate(combos):
        tag = "c" + hashlib.sha256(settings_literal(flags).encode()).hexdigest()[:10]
        path = os.path.join(WORK, f"{tag}.py")
        sha = build(flags, None, path)
        # STAGE 1 SMOKE: reject crashes and non-players, do not rank.
        r = evaluate(path, OPPONENT, smoke_seeds, tag + "_smoke", jobs=8)
        if r["games"] < 8 or r["invalid"] > 0:
            results.append({**r, "flags": flags, "sha256": sha,
                            "stage": "smoke", "verdict": "KILL"})
            if (i + 1) % 8 == 0:
                print(f"  {i+1}/{len(combos)} smoke  "
                      f"{(time.time()-t0)/60:.1f} min")
            continue
        results.append({**r, "flags": flags, "sha256": sha,
                        "stage": "smoke", "verdict": "keep"})
        if (i + 1) % 8 == 0:
            print(f"  {i+1}/{len(combos)} smoke  {(time.time()-t0)/60:.1f} min")

    alive = [r for r in results if r["verdict"] == "keep"]
    alive.sort(key=lambda r: -r["win_rate"])
    survivors = alive[: max(4, len(alive) // 8)]
    print(f"\n  smoke: {len(alive)}/{len(combos)} alive; "
          f"{len(survivors)} advance to EARLY")

    early = []
    for r in survivors:
        tag = "e" + r["sha256"][:10]
        path = os.path.join(WORK, f"{tag}.py")
        build(r["flags"], None, path)
        e = evaluate(path, OPPONENT, early_seeds, tag, jobs=8)
        e.update({"flags": r["flags"], "sha256": r["sha256"], "stage": "early"})
        early.append(e)
        print(f"  early {tag}: {e['W']}-{e['L']} of {e['games']}  "
              f"{e['win_rate']:.4f}")
    early.sort(key=lambda r: -r["win_rate"])

    with open(RESULTS, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"parent_sha256": PARENT_SHA, "genes": GENES,
                   "baseline_flags": base_flags,
                   "opponent": "farm_2945_original",
                   "smoke": results, "early": early,
                   "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
                  fh, indent=2)
    print(f"\nwrote {os.path.relpath(RESULTS, ROOT)}")
    print("STAGE 3 (SERIOUS, 400+ games) is run by pipeline/run_research.py on "
          "the top survivors, not here, so the budget is not spent on losers.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
