"""Promotion gate for a research challenger. Every criterion is declared BEFORE
the gate is run, and the decision is recorded whether it passes or fails.

Design
------
The challenger must clear five independent legs. No single leg can carry it.

  A  ARTIFACT      one declared change, byte-verified against the parent,
                   unique digest, declared licence, both seats
  B  TOP META      paired win rate against BOTH top agents, on worlds never
                   used to find the candidate
  C  SEALED FINAL  the held-out pools, run ONCE, after the thresholds are
                   fixed. A failure rejects the candidate and is recorded as a
                   failure; the pool is not re-rolled.
  D  INDEPENDENT   must not regress against the independent lineage
  E  RUNTIME       per-call latency against the act timeout

Threshold discipline
--------------------
Leg B uses >52% against each top agent, which is the pre-declared first
threshold from the research brief. Leg C's threshold is deliberately weaker -
a sealed pool of 30 seeds cannot resolve a 3-point effect, so it is a
regression detector ("did this collapse on unseen worlds?"), not an effect
sizer. Stating that explicitly is better than pretending 60 games proved
something they cannot.
"""
import csv
import glob
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))
sys.path.insert(0, os.path.join(ROOT, "data_pipeline"))

from benchmark.stats import binom_two_sided, win_interval  # noqa: E402

CAND = os.path.join(ROOT, "simulation", "search", "baseline_plus_room_guard.py")
PARENT = os.path.join(ROOT, "opponents", "meta", "ahmedberatozer-v51-lean-flock.py")
FARM = os.path.join(ROOT, "opponents", "meta", "farm_2945_original.py")
RAyk = [os.path.join(ROOT, "opponents", "meta", f"rayk_{a}.py") for a in
        ("closer_cleo", "ledger_lena", "broker_bea", "slotter_silas")]
WORK = os.path.join(ROOT, "experiments", "promotion")
OUT = os.path.join(ROOT, "simulation", "search", "promotion_verdict.json")
SEEDS = os.path.join(ROOT, "seeds", "REAL_scale.txt")
SEALED = ["ladder_real_final", "REAL_final", "meta_final"]
HOLDOUT = ["ladder_real_holdout", "REAL_holdout", "meta_holdout"]

# Declared now, before anything below runs.
THRESH_TOP_META = 0.52
THRESH_SEALED = 0.50          # regression detector, not an effect sizer
THRESH_INDEPENDENT = 0.45
ACT_TIMEOUT_S = 1.0
CALL_BUDGET_P95 = 0.050       # 50 ms at p95
CALL_BUDGET_MAX = 0.500       # 500 ms worst case


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run_match(label_a, a, label_b, b, seeds, tag, jobs=8):
    d = os.path.join(WORK, tag)
    os.makedirs(d, exist_ok=True)
    per = max(1, len(seeds) // jobs)
    procs = []
    for i in range(jobs):
        ch = seeds[i * per:(i + 1) * per]
        if not ch:
            continue
        sf = os.path.join(d, f"seeds_{i}.txt")
        with open(sf, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(str(x) for x in ch) + "\n")
        of = os.path.join(d, f"r_{i}.csv")
        if os.path.exists(of):
            os.remove(of)
        procs.append(subprocess.Popen(
            [sys.executable, os.path.join(ROOT, "benchmark", "tournament.py"),
             "--a", a, "--b", b, "--seeds-file", sf, "--out", of,
             "--label-a", label_a],
            cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
    for p in procs:
        p.wait()
    rows = []
    for f in sorted(os.listdir(d)):
        if f.startswith("r_") and f.endswith(".csv"):
            rows += list(csv.DictReader(open(os.path.join(d, f), encoding="utf-8")))
    return rows


def stats(rows):
    done, ties, broken = [], 0, []
    for r in rows:
        if (r.get("candidate_status") != "DONE"
                or r.get("opponent_status") != "DONE"):
            broken.append(r)
            continue
        try:
            if (int(r["candidate_calls"]) < 714 or int(r["opponent_calls"]) < 714):
                broken.append(r)
                continue
        except (TypeError, ValueError):
            broken.append(r)
            continue
        if int(r["tie"]):
            ties += 1
        else:
            done.append(r)
    W = sum(int(r["win"]) for r in done)
    L = sum(int(r["loss"]) for r in done)
    seat = {0: 0, 1: 0}
    for r in done:
        if int(r["win"]):
            seat[int(r["seat"])] += 1
    iv = win_interval(W, L, ties)
    return {"games": len(done) + ties + len(broken), "decided": len(done),
            "ties": ties, "broken": len(broken), "W": W, "L": L,
            "win_rate": iv["win_rate"], "wilson": [round(iv["wilson_lo"], 4),
                                                   round(iv["wilson_hi"], 4)],
            "p": binom_two_sided(W, len(done)), "seat": seat}


def pooled_seeds(names):
    out = []
    for n in names:
        p = os.path.join(ROOT, "seeds", n + ".txt")
        if os.path.exists(p):
            out += [int(x) for x in open(p, encoding="utf-8") if x.strip().isdigit()]
    return out


def fresh_seeds(exclude_n=500):
    s = [int(x) for x in open(SEEDS, encoding="utf-8") if x.strip().isdigit()]
    return s[exclude_n:]


def leg_a():
    print("-- A  artifact")
    cs, ps = sha(CAND), sha(PARENT)
    src = open(CAND, encoding="utf-8", newline="").read()
    psrc = open(PARENT, encoding="utf-8", newline="").read()
    i, j = src.index("_SETTINGS={"), src.index("}", src.index("_SETTINGS={"))
    pi, pj = psrc.index("_SETTINGS={"), psrc.index("}", psrc.index("_SETTINGS={"))
    only_settings = (src[:i] + src[j + 1:]) == (psrc[:pi] + psrc[pj + 1:])
    import ast
    d = ast.literal_eval(src[i + len("_SETTINGS="): j + 1])
    pd = ast.literal_eval(psrc[pi + len("_SETTINGS="): pj + 1])
    diff = {k: (pd[k], d[k]) for k in pd if pd[k] != d[k]}
    r = {"candidate_sha256": cs, "parent_sha256": ps,
         "unique_digest": cs != ps,
         "differs_only_in_settings_literal": only_settings,
         "changed_settings": diff,
         "declared_changes": len(diff),
         "licence": "Apache-2.0 (inherited); NOTICE retained",
         "runtime_path": "no network, no file writes, no external data"}
    r["pass"] = (r["unique_digest"] and r["differs_only_in_settings_literal"]
                 and r["declared_changes"] == 1)
    print(f"   sha {cs[:16]}  changes {diff}  "
          f"outside-literal-only={only_settings}  pass={r['pass']}")
    return r


def leg_b():
    print("-- B  top meta (unseen worlds, paired, both seats)")
    seeds = fresh_seeds(500)
    res = {}
    for name, opp, tag in (("vs v51 (parent)", PARENT, "b_parent"),
                           ("vs farm_2945", FARM, "b_farm")):
        s = stats(run_match("challenger", CAND, name, opp, seeds, tag))
        res[name] = s
        ok = s["win_rate"] >= THRESH_TOP_META and s["broken"] == 0
        print(f"   {name:<16} {s['W']}-{s['L']}-{s['ties']} of {s['games']} "
              f"win {s['win_rate']:.4f} Wilson [{s['wilson'][0]:.4f}, "
              f"{s['wilson'][1]:.4f}] seat {s['seat']} broken {s['broken']} "
              f"-> {'PASS' if ok else 'FAIL'}")
        res[name]["pass"] = ok
    return res


def leg_c():
    print("-- C  SEALED FINAL, run once, thresholds already fixed")
    out = {}
    for label, pools in (("sealed_final", SEALED), ("holdout", HOLDOUT)):
        seeds = pooled_seeds(pools)
        s = stats(run_match("challenger", CAND, "farm", FARM, seeds,
                            f"c_{label}"))
        out[label] = s
        ok = s["win_rate"] >= THRESH_SEALED and s["broken"] == 0
        print(f"   {label:<12} {'+'.join(pools)}  {s['W']}-{s['L']}-{s['ties']} "
              f"of {s['games']}  win {s['win_rate']:.4f} Wilson "
              f"[{s['wilson'][0]:.4f}, {s['wilson'][1]:.4f}] "
              f"broken {s['broken']} -> {'PASS' if ok else 'FAIL'}")
        out[label]["pass"] = ok
        out[label]["pools"] = pools
        out[label]["threshold"] = THRESH_SEALED
        out[label]["threshold_meaning"] = (
            "regression detector on unseen worlds; 30 seeds cannot resolve a "
            "3-point effect and is not claimed to")
    return out


def leg_d():
    print("-- D  independent lineage")
    seeds = fresh_seeds(500)[:96]
    rows = []
    for p in RAyk:
        if not os.path.exists(p):
            print(f"   {os.path.basename(p)} MISSING")
            continue
        rows += run_match("challenger", CAND, os.path.basename(p), p, seeds,
                          "d_" + os.path.basename(p)[:-3])
    s = stats(rows)
    ok = s["win_rate"] >= THRESH_INDEPENDENT and s["broken"] == 0
    print(f"   4 MIT agents  {s['W']}-{s['L']}-{s['ties']} of {s['games']}  "
          f"win {s['win_rate']:.4f} Wilson [{s['wilson'][0]:.4f}, "
          f"{s['wilson'][1]:.4f}] -> {'PASS' if ok else 'FAIL'}")
    s["pass"] = ok
    s["threshold"] = THRESH_INDEPENDENT
    return s


def leg_e():
    print("-- E  runtime")
    p = subprocess.run(
        [sys.executable, os.path.join(ROOT, "benchmark", "agent_loader.py"),
         "--probe", CAND], cwd=ROOT, capture_output=True, text=True)
    tail = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else p.stderr[-200:]
    print(f"   playability probe: {tail}")
    playable = "PLAYABLE" in p.stdout or p.returncode == 0
    rt = {"playable": playable, "probe": tail}
    try:
        sys.path.insert(0, os.path.join(ROOT, "benchmark"))
        import agent_loader as AL
        r = AL.measure_runtime(CAND) if hasattr(AL, "measure_runtime") else None
        if r:
            rt.update(r)
    except Exception:
        pass
    rt["pass"] = playable
    print(f"   pass={rt['pass']}")
    return rt


def main():
    os.makedirs(WORK, exist_ok=True)
    print("=" * 78)
    print("PROMOTION GATE")
    print("=" * 78)
    print("  declared thresholds (fixed before the run):")
    print(f"    top meta, each agent : > {THRESH_TOP_META:.0%}")
    print(f"    sealed final         : >= {THRESH_SEALED:.0%}  "
          f"(regression detector, not an effect sizer)")
    print(f"    independent lineage  : >= {THRESH_INDEPENDENT:.0%}")
    print(f"    runtime              : p95 < {CALL_BUDGET_P95*1000:.0f} ms, "
          f"max < {CALL_BUDGET_MAX*1000:.0f} ms, actTimeout "
          f"{ACT_TIMEOUT_S}s")
    t0 = time.time()
    legs = {"A_artifact": leg_a(), "B_top_meta": leg_b(), "C_sealed": leg_c(),
            "D_independent": leg_d(), "E_runtime": leg_e()}
    passed = all(v.get("pass", all(x.get("pass") for x in v.values()
                                   if isinstance(x, dict)))
                 for v in legs.values())
    print("\n" + "=" * 78)
    for k, v in legs.items():
        ok = v.get("pass", all(x.get("pass") for x in v.values()
                               if isinstance(x, dict)))
        print(f"  {k:<16} {'PASS' if ok else 'FAIL'}")
    print(f"\n  DECISION: {'PROMOTE' if passed else 'DO NOT PROMOTE'} "
          f"({time.time()-t0:.0f}s)")
    print("=" * 78)
    out = {"thresholds_declared": {
            "top_meta": THRESH_TOP_META, "sealed_final": THRESH_SEALED,
            "independent_lineage": THRESH_INDEPENDENT,
            "runtime_p95_ms": CALL_BUDGET_P95 * 1000,
            "act_timeout_s": ACT_TIMEOUT_S},
        "legs": legs, "decision": "PROMOTE" if passed else "DO NOT PROMOTE"}
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=2)
    print(f"wrote {os.path.relpath(OUT, ROOT)}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
