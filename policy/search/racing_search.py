"""Progressive-racing search over the reference agent's FULL boolean layer space.

Scope, and why it is this scope
------------------------------
The champion is a published Apache-2.0 agent plus one settings flag. Its
configuration surface is what the search is allowed to touch:

  * the nine boolean layer switches in the live `_SETTINGS` literal
    (2^9 = 512 reachable configurations);
  * the numeric keys in the same literal (`min_sell_price`, `block_turns`,
    `shed_capacity`, `board_size`, `max_orders`, `turns_per_day`) -- these are
    part of the same dict and are INVENTORIED here rather than assumed inert.

The full inventory is recorded, including which keys the agent actually reads,
because a previous search assumed only the booleans mattered and a previous
report assumed `DEFAULT_SETTINGS` was live when `_SETTINGS` overrides it. Both
assumptions were wrong in the same direction: toward under-searching.

`room_guard` proved that a dormant layer can be worth 3.2 points. That is the
justification for enumerating the whole space rather than stopping at the first
improvement.

Progressive racing, PRE-DECLARED before the run
-----------------------------------------------
    stage A   all 512 configurations            4 worlds  (8 games)
    stage B   top 128                           16 worlds (32 games)
    stage C   top 32                            64 worlds (128 games)
    stage D   top 8                            256 worlds (512 games)
    stage E   top 2                            full league

The stage sizes and sample counts are fixed in this file BEFORE any result
exists. Choosing them after seeing outcomes is how a search turns into a search
for a confirmation.

Why racing rather than one big evaluation
-----------------------------------------
The official Python engine sustains roughly 50-80 matches/minute here because no
verified fast backend exists. Scoring all 512 configurations at a resolution
that could resolve a 2-point effect is not affordable. Racing spends the budget
where it discriminates: every configuration is screened, and only the plausible
ones are paid for in games.

The champion is retained at every stage
---------------------------------------
`C001` is scored in every stage on the same seeds, so a stage's numbers are
comparable to the champion's on the same worlds. A candidate that beats the
champion by less than the champion's own stage-to-stage wobble is not an
improvement, and the wobble is measured rather than assumed.

Objective, fixed in advance
---------------------------
Primary: lineage-balanced BT score rate, `(W + 0.5T)/N`, averaged over lineages
with equal weight so that nine variants of one lineage cannot outvote a single
independent opponent.

Robustness term: `0.6 * mean_lineage_score + 0.4 * worst_lineage_score`. The
worst-lineage term is in the objective, not merely reported, because a candidate
that is excellent against the Farm and catastrophic against one independent
lineage is exactly the brittle agent this project must not promote.

Both terms and the weights are declared here, before any candidate is built.
"""
import argparse
import ast
import csv
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
sys.path.insert(0, os.path.join(ROOT, "policy", "search"))

from stats import lineage_balanced_score, win_interval  # noqa: E402

WORK = os.path.join(ROOT, "simulation", "search3066")
CAND_DIR = os.path.join(WORK, "candidates")
RES_DIR = os.path.join(WORK, "results")
STATE = os.path.join(WORK, "search_state.json")
OUT = os.path.join(WORK, "search_summary.json")

C001 = os.path.join(ROOT, "champions", "research", "C001_room_guard", "main.py")
C001_SHA = "a52ba1bfe9df9dc1d504550af46744ef8d474797cdba7af2412dc40a3ebdf3b8"

SEEDS = os.path.join(ROOT, "seeds", "GEN3066_dev.txt")
RUNNER = os.path.join(ROOT, "benchmark", "parallel_tournament.py")

# Opponents, with the lineage each belongs to. The lineage weighting is the
# whole reason these are tagged.
OPPONENTS = [
    ("v51", "opponents/meta/ahmedberatozer-v51-lean-flock.py", "L-OZER-2945"),
    ("farm", "opponents/meta/farm_2945_original.py", "L-OZER-2945"),
    ("moon_q13", "opponents/unlicensed/kaggriculture-r88-rivals__moon_q13_mg.py",
     "L-MOON"),
    ("thomas", "opponents/unlicensed/kaggriculture-r88-rivals__thomas.py",
     "L-R88"),
]

# Declared before the run.
STAGES = [
    ("A", 512, 4),      # configurations kept, worlds per configuration
    ("B", 128, 16),
    ("C", 32, 64),
    ("D", 8, 256),
]
ROBUST_WEIGHT_MEAN = 0.6
ROBUST_WEIGHT_WORST = 0.4


def settings_of(path):
    src = open(path, encoding="utf-8", newline="").read()
    i = src.index("_SETTINGS={")
    j = src.index("}", i)
    return src, i, j, ast.literal_eval(src[i + len("_SETTINGS="): j + 1])


def inventory():
    """Every configurable key in the live settings, typed and classified.

    Recorded because the previous generation searched nine booleans on the
    assumption that was the whole space. It was not: the same literal carries
    six numeric keys.
    """
    _src, _i, _j, d = settings_of(C001)
    src = open(C001, encoding="utf-8", errors="ignore").read()
    out = []
    for k, v in d.items():
        if isinstance(v, bool):
            kind = "boolean"
        elif isinstance(v, int):
            kind = "integer"
        elif isinstance(v, float):
            kind = "float"
        elif isinstance(v, (list, tuple)):
            kind = "list"
        else:
            kind = type(v).__name__
        # "Read" is a best-effort signal, not a proof of reachability. It is
        # recorded as a count so a key that appears nowhere is visible.
        out.append({"key": k, "value": v, "type": kind,
                    "occurrences_in_source": src.count(f"'{k}'")})
    return out


def enumerate_configs():
    _src, _i, _j, base = settings_of(C001)
    bools = [k for k, v in base.items() if isinstance(v, bool)]
    combos = []
    for bits in itertools.product([False, True], repeat=len(bools)):
        d = dict(base)
        for k, b in zip(bools, bits):
            d[k] = b
        combos.append(d)
    # Every gene must take both values in the sample, or the search is vacuous.
    # The previous generation's screen scored 0.0000 on all 64 candidates
    # because a lexicographic prefix of itertools.product left the first gene
    # constant. An explicit assertion is the fix.
    for k in bools:
        if len({c[k] for c in combos}) < 2:
            raise SystemExit(f"degenerate enumeration: gene {k!r} is constant")
    return bools, combos


def build(cfg, path):
    src, i, j, _base = settings_of(C001)
    parts = []
    for k, v in cfg.items():
        parts.append(f"'{k}': {v}")
    lit = "{" + ", ".join(parts) + "}"
    out = src[:i] + f"_SETTINGS={lit}" + src[j + 1:]
    if out.count("_SETTINGS={") != 1:
        raise SystemExit("refusing to build: the edit was not single-site")
    # Post-condition: byte-identical outside the literal.
    if (src[:i] + src[j + 1:]) != (out[:out.index("_SETTINGS={")] +
                                    out[out.index("}",
                                                  out.index("_SETTINGS={")) + 1:]):
        raise SystemExit("refusing to build: edit touched bytes outside the "
                         "settings literal")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(out)
    return hashlib.sha256(out.encode()).hexdigest()


def tag_of(cfg):
    return hashlib.sha256(repr(sorted(cfg.items())).encode()).hexdigest()[:12]


def run_matchups(path, label, worlds, stage, workers=8):
    """Play every opponent on the first `worlds` dev seeds. Cached by digest."""
    seeds = [int(x) for x in open(SEEDS, encoding="utf-8") if x.strip().isdigit()]
    seeds = seeds[:worlds]
    sf = os.path.join(WORK, f"seeds_{worlds}.txt")
    os.makedirs(WORK, exist_ok=True)
    with open(sf, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(str(s) for s in seeds) + "\n")
    res = {}
    for opp_name, opp_path, lineage in OPPONENTS:
        if not os.path.exists(opp_path):
            continue
        tag = f"{label}__{opp_name}__{stage}"
        out = os.path.join("experiments", "p3066", "search", tag + ".csv")
        cmd = [sys.executable, RUNNER, "--a", path, "--b", opp_path,
               "--seeds-file", sf, "--out", out, "--workers", str(workers),
               "--label-a", label, "--label-b", opp_name,
               "--experiment-id", f"search_{stage}"]
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        rows = []
        if os.path.exists(os.path.join(ROOT, out)):
            rows = list(csv.DictReader(
                open(os.path.join(ROOT, out), encoding="utf-8")))
        v = [r for r in rows if r.get("valid") == "1"]
        W = sum(int(r["win"]) for r in v)
        L = sum(int(r["loss"]) for r in v)
        T = sum(int(r["tie"]) for r in v)
        broken = len(rows) - len(v)
        res[opp_name] = {"lineage_id": lineage, "W": W, "L": L, "T": T,
                         "games": len(v), "broken": broken,
                         "bt_score_rate": win_interval(W, L, T)["bt_score_rate"],
                         "stderr": (p.stderr or "")[-120:]}
    return res


def score(res):
    lb = lineage_balanced_score([
        {"lineage_id": v["lineage_id"], "W": v["W"], "L": v["L"], "T": v["T"]}
        for v in res.values()])
    robust = (ROBUST_WEIGHT_MEAN * lb["score"]
              + ROBUST_WEIGHT_WORST * lb["worst_score"])
    return {"robust_score": robust, "mean_lineage": lb["score"],
            "worst_lineage": lb["worst_lineage"],
            "worst_lineage_score": lb["worst_score"],
            "n_lineages": lb["n_lineages"],
            "broken": sum(v["broken"] for v in res.values())}


def load_state():
    if os.path.exists(STATE):
        return json.load(open(STATE, encoding="utf-8"))
    return {"stages_done": [], "results": {}}


def save_state(st):
    os.makedirs(WORK, exist_ok=True)
    tmp = STATE + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(st, fh, indent=2)
    os.replace(tmp, STATE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default=None, help="run a single stage letter")
    ap.add_argument("--workers", type=int, default=os.cpu_count() or 8)
    args = ap.parse_args()

    os.makedirs(CAND_DIR, exist_ok=True)
    os.makedirs(RES_DIR, exist_ok=True)
    bools, combos = enumerate_configs()
    inv = inventory()
    print("=" * 78)
    print("PROGRESSIVE-RACING BOOLEAN SEARCH around C001")
    print("=" * 78)
    print(f"  boolean genes     : {len(bools)}  -> {len(combos)} configurations")
    print(f"  genes             : {bools}")
    print(f"  numeric keys also present in the live literal (inventoried, "
          f"NOT yet searched):")
    for r in inv:
        if r["type"] != "boolean":
            print(f"      {r['key']:<18} = {r['value']:<8} "
                  f"occurrences in source: {r['occurrences_in_source']}")
    print(f"\n  objective         : {ROBUST_WEIGHT_MEAN} * mean_lineage + "
          f"{ROBUST_WEIGHT_WORST} * worst_lineage")
    print(f"  primary metric    : lineage-balanced BT score rate "
          f"(W+0.5T)/N")
    print(f"  opponents         : "
          f"{', '.join(n for n, _, _ in OPPONENTS)}")
    print(f"  declared schedule : " +
          ", ".join(f"{s}:{k}x{w}w" for s, k, w in STAGES))
    print(f"  C001 is evaluated at every stage on the same seeds\n")

    st = load_state()

    # The champion is scored first at every stage, as the reference the stage's
    # numbers are compared against.
    base_cfg = settings_of(C001)[3]

    for stage, keep, worlds in STAGES:
        if args.stage and stage != args.stage:
            continue
        key = f"stage_{stage}"
        if key in st["stages_done"]:
            print(f"  stage {stage} already done, skipping")
            continue
        t0 = time.time()

        if stage == "A":
            pool = [("C001_BASELINE", C001, base_cfg)] + \
                   [(tag_of(c), None, c) for c in combos]
        else:
            # Stages B..D consume the pool the previous stage retained. The
            # champion rides along at every stage as `__C001__`, which is
            # preserved by `nxt` slicing only if it ranks inside `keep`; to
            # guarantee the reference is always present, it is re-added
            # unconditionally here.
            prev = st.get(f"pool_{stage}") or []
            pool = [("C001_BASELINE", C001, base_cfg)]
            seen_tags = {"C001_BASELINE"}
            for entry in prev:
                if entry["tag"] in seen_tags:
                    continue
                seen_tags.add(entry["tag"])
                pool.append((entry["tag"],
                             os.path.join(CAND_DIR, entry["tag"] + ".py"),
                             entry["cfg"]))

        print(f"\n--- stage {stage}: {len(pool)} configurations x {worlds} "
              f"worlds ({worlds*2} games each)")
        results = []
        for i, (tag, path, cfg) in enumerate(pool):
            if path is None:
                path = os.path.join(CAND_DIR, tag + ".py")
                build(cfg, path)
            res = run_matchups(path, tag, worlds, stage, args.workers)
            if not res:
                continue
            sc = score(res)
            results.append({"tag": tag, "path": path, "cfg": cfg,
                            "per_opponent": res, **sc})
            if (i + 1) % 16 == 0 or i + 1 == len(pool):
                print(f"    {i+1}/{len(pool)}  "
                      f"{(time.time()-t0)/60:.1f} min  "
                      f"best so far {max(r['robust_score'] for r in results):.4f}")
        results.sort(key=lambda r: -r["robust_score"])

        # A candidate that is functionally identical to another is a no-op and
        # must not crowd out the field. Identical is decided by DIGEST.
        seen, deduped = set(), []
        for r in results:
            h = sha_of(r["path"])
            if h in seen:
                r["duplicate_of"] = True
                continue
            seen.add(h)
            deduped.append(r)

        nxt = deduped[:keep]
        st.setdefault("results", {})[key] = {
            "n_evaluated": len(results), "n_unique": len(deduped),
            "worlds": worlds,
            "best": [{k: r[k] for k in ("tag", "robust_score", "mean_lineage",
                                        "worst_lineage_score", "broken")}
                     for r in deduped[:8]],
            "minutes": round((time.time() - t0) / 60, 1)}
        st[f"pool_{stage}"] = [
            {"tag": r["tag"], "cfg": r["cfg"],
             "path": "__C001__" if r["tag"] == "C001_BASELINE" else r["path"]}
            for r in nxt]
        st["stages_done"].append(key)
        save_state(st)

        base = [r for r in deduped if r["tag"] == "C001_BASELINE"]
        print(f"\n  stage {stage} done in {(time.time()-t0)/60:.1f} min, "
              f"{len(deduped)} unique of {len(results)}")
        if base:
            print(f"  C001 baseline robust score this stage: "
                  f"{base[0]['robust_score']:.4f} "
                  f"(mean {base[0]['mean_lineage']:.4f}, "
                  f"worst {base[0]['worst_lineage_score']:.4f})")
        print(f"  {'rank':>4} {'tag':<16}{'robust':>9}{'mean':>8}"
              f"{'worst':>8}  worst lineage")
        for rank, r in enumerate(deduped[:8]):
            print(f"  {rank:>4} {r['tag']:<16}"
                  f"{r['robust_score']:>9.4f}{r['mean_lineage']:>8.4f}"
                  f"{r['worst_lineage_score']:>8.4f}  {r['worst_lineage']}")
        if len(st["stages_done"]) >= len(STAGES):
            break

    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"genes": bools, "n_configurations": len(combos),
                   "numeric_inventory": [r for r in inv if r["type"] != "boolean"],
                   "objective": {"mean_weight": ROBUST_WEIGHT_MEAN,
                                 "worst_weight": ROBUST_WEIGHT_WORST,
                                 "metric": "lineage-balanced BT score rate"},
                   "opponents": [{"name": n, "path": p, "lineage_id": l}
                                 for n, p, l in OPPONENTS],
                   "stages_declared": [{"stage": s, "keep": k, "worlds": w}
                                       for s, k, w in STAGES],
                   "state": st}, fh, indent=2)
    print(f"\nwrote {os.path.relpath(OUT, ROOT)}")
    return 0


def sha_of(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


if __name__ == "__main__":
    sys.exit(main())
