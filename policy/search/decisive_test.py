"""Decisive single-variable test: does `room_guard` help, hurt, or do nothing?

Why this experiment exists
--------------------------
The smoke screen (`policy/search/run_search.py`) surfaced five survivors, all
sharing exactly one gene beyond `hand_align`: `room_guard=True`, which the
shipped configuration has OFF. Everything else varied at random between them,
which is what noise selection looks like.

But a 16-game screen cannot resolve the 2-point effect that separates the
baseline from the Farm. So the survivor signal is a *hypothesis*, not a result,
and it is tested here properly:

  - exactly ONE variable changes from the frozen parent;
  - head-to-head against the parent itself, so the comparison is paired and
    world-for-world rather than two independent samples;
  - both seats, every world;
  - a large sample, because $28 mean margin on ~$100k banks means small
    effects;
  - two DISJOINT seed halves, so the parent-vs-variant leg and the vs-Farm leg
    cannot share worlds and inflate each other.

The three possible verdicts are all useful:
  * variant beats parent significantly -> `room_guard` is a real gain;
  * parent and variant are indistinguishable -> `room_guard` is a NO-OP and the
    parent is already at a local optimum on its own levers;
  * parent beats variant significantly -> `room_guard` must stay OFF.

A no-op is a publishable result. Inventing a win out of a tie is not.
"""
import ast
import csv
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))
sys.path.insert(0, os.path.join(ROOT, "policy", "search"))

from benchmark.stats import binom_two_sided, mcnemar_exact, win_interval  # noqa
from run_search import PARENT, PARENT_SHA  # noqa: E402

WORK = os.path.join(ROOT, "simulation", "search")
VARIANT = os.path.join(WORK, "baseline_plus_room_guard.py")
FARM = os.path.join(ROOT, "opponents", "meta", "farm_2945_original.py")
SEEDS = os.path.join(ROOT, "seeds", "REAL_scale.txt")
OUT = os.path.join(WORK, "room_guard_decisive.json")
GENE = "room_guard"


def parent_settings():
    src = open(PARENT, encoding="utf-8", newline="").read()
    i = src.index("_SETTINGS={")
    j = src.index("}", i)
    return src, i, j, ast.literal_eval(src[i + len("_SETTINGS="): j + 1])


def build_variant():
    """Change exactly one gene. Verify afterwards that nothing else moved."""
    src, i, j, base = parent_settings()
    assert base[GENE] is False, (
        f"{GENE} is already {base[GENE]}; this experiment would be a no-op by "
        f"construction and could not tell us anything")
    new = dict(base)
    new[GENE] = True
    parts = [f"'{k}': {new[k]}" for k in base]
    lit = "{" + ", ".join(parts) + "}"
    out = src[:i] + f"_SETTINGS={lit}" + src[j + 1:]
    # Post-conditions: exactly one gene differs, and nothing outside the
    # literal changed. Asserted, not assumed.
    rb = ast.literal_eval(out[out.index("_SETTINGS={") + len("_SETTINGS="):
                              out.index("}", out.index("_SETTINGS={")) + 1])
    diff = {k for k in base if rb[k] != base[k]}
    assert diff == {GENE}, f"more than one gene changed: {diff}"
    assert (src[:i] + src[j + 1:]) == (out[:out.index("_SETTINGS={")] +
                                       out[out.index("}", out.index("_SETTINGS={")) + 1:]), \
        "edit touched bytes outside the settings literal"
    with open(VARIANT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(out)
    return hashlib.sha256(out.encode()).hexdigest(), base, rb


def split_seeds(n_a=500, n_b=500):
    s = [int(x) for x in open(SEEDS, encoding="utf-8") if x.strip().isdigit()]
    assert len(s) >= n_a + n_b, f"need {n_a+n_b} seeds, have {len(s)}"
    return s[:n_a], s[n_a:n_a + n_b]


def run(label_a, path_a, label_b, path_b, seeds, tag, jobs=8):
    outdir = os.path.join(WORK, "decisive", tag)
    os.makedirs(outdir, exist_ok=True)
    per = max(1, len(seeds) // jobs)
    procs = []
    for i in range(jobs):
        ch = seeds[i * per:(i + 1) * per]
        if not ch:
            continue
        sf = os.path.join(outdir, f"seeds_{i}.txt")
        with open(sf, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(str(x) for x in ch) + "\n")
        of = os.path.join(outdir, f"r_{i}.csv")
        procs.append(subprocess.Popen(
            [sys.executable, os.path.join(ROOT, "benchmark", "tournament.py"),
             "--a", path_a, "--b", path_b, "--seeds-file", sf,
             "--out", of, "--label-a", label_a],
            cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
    for p in procs:
        p.wait()
    rows = []
    for f in sorted(os.listdir(outdir)):
        if f.startswith("r_") and f.endswith(".csv"):
            rows += list(csv.DictReader(open(os.path.join(outdir, f),
                                             encoding="utf-8")))
    return rows


def summarise(rows, label):
    v = [r for r in rows if r["valid"] == "1"]
    W = sum(int(r["win"]) for r in v)
    L = sum(int(r["loss"]) for r in v)
    T = sum(int(r["tie"]) for r in v)
    iv = win_interval(W, L, T)
    mc = [int(r["candidate_cash"]) - int(r["opponent_cash"]) for r in v]
    mc.sort()
    seat = {0: 0, 1: 0}
    disc = [0, 0]
    for r in v:
        w = int(r["win"])
        l = int(r["loss"])
        if w:
            seat[int(r["seat"])] += 1
        if w and not l:
            disc[0] += 1
        elif l and not w:
            disc[1] += 1
    p = binom_two_sided(W, L + T)
    return {
        "label": label, "games": len(v), "invalid": len(rows) - len(v),
        "W": W, "L": L, "T": T, "win_rate": iv["win_rate"],
        "wilson": [round(iv["wilson_lo"], 4), round(iv["wilson_hi"], 4)],
        "binomial_p_vs_50": p,
        "median_margin": mc[len(mc) // 2] if mc else 0,
        "mean_margin": round(sum(mc) / len(mc), 1) if mc else 0,
        "seat_wins": seat, "discordant": disc,
        "mcnemar_p": mcnemar_exact(disc[0], disc[1])[0],
        "mcnemar_n_discordant": sum(disc),
    }


def main():
    n = int(sys.argv[sys.argv.index("--games") + 1]) if "--games" in sys.argv else 500
    vsha, base, var = build_variant()
    a_seeds, b_seeds = split_seeds(n, n)
    print("=" * 78)
    print(f"DECISIVE SINGLE-VARIABLE TEST: +{GENE}")
    print("=" * 78)
    print(f"  parent  {PARENT_SHA}")
    print(f"  variant {vsha}")
    print(f"  parent  {GENE}={base[GENE]}   variant {GENE}={var[GENE]}")
    print(f"  post-condition: exactly one gene differs, verified after the edit")
    print(f"  seeds: {n} for the head-to-head, {n} disjoint for the vs-Farm leg")

    t0 = time.time()
    print("\n-- leg 1: variant vs parent, paired, both seats")
    r1 = run("variant", VARIANT, "parent", PARENT, a_seeds, "vh")
    s1 = summarise(r1, f"variant(+{GENE}) vs parent")
    print(f"   {s1['W']}-{s1['L']}-{s1['T']} of {s1['games']}  "
          f"win={s1['win_rate']:.4f}  Wilson [{s1['wilson'][0]:.4f}, "
          f"{s1['wilson'][1]:.4f}]  p={s1['binomial_p_vs_50']:.4f}")
    print(f"   median margin ${s1['median_margin']}, mean ${s1['mean_margin']}, "
          f"seat {s1['seat_wins']}, McNemar p={s1['mcnemar_p']:.4f}, "
          f"invalid {s1['invalid']}")

    print(f"\n-- leg 2: variant vs Farm (disjoint seeds)")
    r2 = run("variant", VARIANT, "farm", FARM, b_seeds, "vf")
    s2 = summarise(r2, f"variant(+{GENE}) vs farm")
    print(f"   {s2['W']}-{s2['L']}-{s2['T']} of {s2['games']}  "
          f"win={s2['win_rate']:.4f}  Wilson [{s2['wilson'][0]:.4f}, "
          f"{s2['wilson'][1]:.4f}]  p={s2['binomial_p_vs_50']:.4f}")

    print(f"\n-- leg 3: parent vs Farm (disjoint seeds, the reference number)")
    r3 = run("parent", PARENT, "farm", FARM, b_seeds, "pf")
    s3 = summarise(r3, "parent vs farm")
    print(f"   {s3['W']}-{s3['L']}-{s3['T']} of {s3['games']}  "
          f"win={s3['win_rate']:.4f}  Wilson [{s3['wilson'][0]:.4f}, "
          f"{s3['wilson'][1]:.4f}]  p={s3['binomial_p_vs_50']:.4f}")

    # Verdicts, stated against the pre-declared thresholds.
    v1 = ("VARIANT WINS" if s1["wilson"][0] > 0.5 else
          "PARENT WINS" if s1["wilson"][1] < 0.5 else
          "NO-OP (indistinguishable)")
    delta = s2["win_rate"] - s3["win_rate"]
    v2 = ("variant better vs Farm" if delta > 0.02 else
          "variant worse vs Farm" if delta < -0.02 else
          "variant indistinguishable vs Farm")
    print("\n" + "=" * 78)
    print(f"VERDICT leg 1: {v1}")
    print(f"VERDICT leg 2: {v2} (delta {delta:+.4f})")
    print("=" * 78)

    out = {"gene": GENE, "parent_sha256": PARENT_SHA, "variant_sha256": vsha,
           "parent_settings": base, "variant_settings": var,
           "games_per_leg": n, "seed_halves_disjoint": True,
           "leg1_variant_vs_parent": s1, "leg2_variant_vs_farm": s2,
           "leg3_parent_vs_farm": s3,
           "verdict_leg1": v1, "verdict_leg2": v2,
           "delta_vs_farm": delta,
           "minutes": round((time.time() - t0) / 60, 1)}
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=2)
    print(f"\nwrote {os.path.relpath(OUT, ROOT)}  "
          f"({out['minutes']} min)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
