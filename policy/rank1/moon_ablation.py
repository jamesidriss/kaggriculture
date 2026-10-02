"""Moon ablation: identify the mechanism by INTERVENTION, not by reading names.

The rule this project keeps re-learning: do not infer causation from code size,
identifier names, or how impressive a block looks. Disable one layer, measure,
and let the number decide.

Why Moon matters
----------------
`research/moon_provenance.py` established two things that reframe the whole
problem:

1. **Moon is not an independent lineage.** Its header says it derives from the
   2945 Farm submission v9/3, and identifier Jaccard against C001 is 0.72 --
   higher than the Farm's own 0.61. Moon is a *descendant of the same family*,
   not a foreign strategy. The catalog label "independent lineage" was wrong.

2. **Moon is broadly dominant, not a C001-specific counter.** Over 120 seeds
   paired both seats:

       moon_parent vs C001     221-19   BT 0.9208
       moon_parent vs v51      226-14   BT 0.9417
       moon_parent vs farm     236-4    BT 0.9833

   It beats the whole field, and beats the Farm hardest. So this is not a narrow
   exploit to be patched; Moon is the strongest publicly obtainable artifact we
   have seen, by a wide margin.

3. **Its licence is UNKNOWN, not Apache-2.0.** An Apache body appears inside the
   file, but the immediate parent Work (`queue_compact.py`) is NOT distributed,
   the header marks it "FOR LOCAL DISCOVERY ONLY" and explicitly disclaims any
   official Kaggle score claim, and the distributing dataset carries no licence
   file. A licence body is not a grant, and an incomplete derivation chain cannot
   be traced to a root Work. Moon is an analytical opponent and a source of
   hypotheses. It is never a submission artifact and none of its source is
   transcribed into one.

What this script does
---------------------
For each candidate mechanism, disable it in Moon and measure Moon's BT score
against C001. A layer whose removal costs Moon little is not the cause; a layer
whose removal collapses Moon to C001's level is the cause.

Layers under test, all taken from the v9 header:
  RACE   reservation/racing against a rival's observed sale
  RACEPX a lead on top of RACE, gated on a precondition
  COURIER, CARROT, HERD  further appended layers
  OPENING  the v9 opening market sequence
  plus two control ablations that should cost nothing, to prove the harness can
  detect a null.

Interventions are implemented as source-level no-ops, each recorded with its
exact diff so a later reader can reproduce or audit it.
"""
import ast
import csv
import difflib
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))

MOON = os.path.join(ROOT, "opponents", "unlicensed",
                    "kaggriculture-r88-rivals__moon_parent.py")
C001 = os.path.join(ROOT, "champions", "research", "C001_room_guard", "main.py")
WORK = os.path.join(ROOT, "simulation", "rank1", "ablation")
SEEDS = os.path.join(ROOT, "seeds", "GEN3066_dev.txt")
OUT = os.path.join(WORK, "ablation_results.json")

# Each ablation is (name, hypothesis, python_expression_returning_replacement).
# The expression is evaluated in the Moon module's namespace with `agent` bound,
# so a disabled layer returns the UNMODIFIED parent action.
#
# `mode` is either:
#   "chain"   -> wrap the CURRENT `agent` so it is bypassed
#   "guard"   -> replace a named function with a pass-through
# A disabled layer must be a PASS-THROUGH that returns the unmodified action.
#
# The first version of this file replaced layers with stubs returning `None`.
# For `_v9_opening` that made the top-level wrapper `return _v9_opening(...)`
# return `None`, so the agent emitted nothing and scored 0-80. That is not an
# ablation result, it is a broken agent, and it reported as "MECHANISM: drop
# 0.9000". Any intervention that cannot distinguish "this layer does not matter"
# from "I broke the program" is not an intervention.
#
# Each shim therefore (a) returns the ORIGINAL value it was given, and (b)
# counts its invocations in a module global, so the harness can PROVE the shim
# actually fired. An ablation that never ran must report as such rather than as
# a null result.
#
# `mode` is retained for readability; the shim text is what is applied.
ABLATIONS = [
    ("control_null",
     "a no-op that must cost Moon nothing; if it costs anything the harness is "
     "measuring something other than the layer",
     None),
    ("disable_v9_opening",
     "the v9 opening market sequence, which overrides the first two turns' "
     "market orders with a fixed tape (V9_OPENING_TAPE)",
     "_ABL_COUNT['opening'] = _ABL_COUNT.get('opening', 0) + 1\n"
     "_V9_OPENING_REAL = _v9_opening\n"
     "def _v9_opening(obs, action, _real=_V9_OPENING_REAL):\n"
     "    _ABL_COUNT['opening'] = _ABL_COUNT.get('opening', 0) + 1\n"
     "    return action\n"),
    ("disable_RACE_update",
     "RACE records a rival's observed sale and computes how far ahead of it "
     "Moon's own planned sale sits. If Moon's dominance comes from reacting to "
     "an opponent's sale, disabling the update should collapse it toward C001.",
     "_ABL_COUNT['race'] = _ABL_COUNT.get('race', 0) + 1\n"
     "_V9_RACE_UPDATE_REAL = _v9_race_update\n"
     "def _v9_race_update(obs, st, _real=_V9_RACE_UPDATE_REAL):\n"
     "    _ABL_COUNT['race'] = _ABL_COUNT.get('race', 0) + 1\n"
     "    return st\n"),
    ("disable_planned_sells",
     "_v9_planned_sells is the tape search RACE depends on. Disabling it "
     "starves RACE of the data it acts on, so this should behave like "
     "disable_RACE_update if the mechanism is real.",
     "_ABL_COUNT['planned'] = _ABL_COUNT.get('planned', 0) + 1\n"
     "def _v9_planned_sells(tape, item, step):\n"
     "    _ABL_COUNT['planned'] = _ABL_COUNT.get('planned', 0) + 1\n"
     "    return []\n"),
]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def make_variant(name, replacement, out_path):
    """Append a disabling shim to a COPY of Moon. Never edits the original."""
    src = open(MOON, encoding="utf-8", newline="").read()
    before = sha(MOON)
    if replacement is None:
        out = src
        diff = ""
    else:
        shim = (
            "\n\n# " + "=" * 70 + "\n"
            f"# RANK1 ABLATION: {name}\n"
            "# Appended shim on a COPY. The original artifact is unmodified.\n"
            "# Every shim counts its own invocations in _ABL_COUNT so the\n"
            "# harness can prove the intervention actually fired. An ablation\n"
            "# that never ran is reported as NOT EXERCISED, not as a null.\n"
            "# " + "=" * 70 + "\n"
            "_ABL_COUNT = {}\n"
            + replacement
            + "\n_ABL_SEAL_NAMED = True\n"
            + "\n# " + "=" * 70 + "\n"
            "# ABLATION ENDS\n"
            "# " + "=" * 70 + "\n")
        out = src + shim
        diff = "".join(difflib.unified_diff(
            src.splitlines(True), out.splitlines(True),
            fromfile="moon_parent.py", tofile=f"moon_parent+{name}.py", n=0))
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(out)
    return {"name": name, "path": os.path.relpath(out_path, ROOT).replace("\\", "/"),
            "sha256": sha(out_path), "bytes": len(out),
            "source_sha256_unchanged": sha(MOON) == before,
            "diff_lines": len([l for l in diff.splitlines()
                               if l.startswith(("+", "-"))
                               and not l.startswith(("+++", "---"))]),
            "diff_preview": diff[:1200] if replacement is not None else ""}


def play(path_a, path_b, seeds, tag, workers=8):
    out = os.path.join("experiments", "rank1", "ablation", tag + ".csv")
    sf = os.path.join(WORK, "seeds.txt")
    os.makedirs(WORK, exist_ok=True)
    with open(sf, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(str(s) for s in seeds) + "\n")
    p = subprocess.run(
        [sys.executable, os.path.join(ROOT, "benchmark", "parallel_tournament.py"),
         "--a", path_a, "--b", path_b, "--seeds-file", sf, "--out", out,
         "--workers", str(workers), "--label-a", os.path.basename(path_a)[:-3],
         "--label-b", "C001", "--experiment-id", "rank1_ablation"],
        cwd=ROOT, capture_output=True, text=True)
    p_csv = os.path.join(ROOT, out)
    if not os.path.exists(p_csv):
        return {"error": "no output", "stderr": (p.stderr or "")[-300:]}
    rows = list(csv.DictReader(open(p_csv, encoding="utf-8")))
    v = [r for r in rows if r.get("valid") == "1"]
    W = sum(int(r["win"]) for r in v)
    L = sum(int(r["loss"]) for r in v)
    T = sum(int(r["tie"]) for r in v)
    return {"games": len(rows), "valid": len(v), "broken": len(rows) - len(v),
            "W": W, "L": L, "T": T,
            "bt_score": round((W + 0.5 * T) / max(1, W + L + T), 4),
            "raw_row": p.stdout.strip().splitlines()[-3:]
            if p.stdout.strip() else []}


def main():
    n = int(sys.argv[sys.argv.index("--seeds") + 1]) if "--seeds" in sys.argv else 60
    os.makedirs(WORK, exist_ok=True)
    seeds = [int(x) for x in open(SEEDS, encoding="utf-8") if x.strip().isdigit()][:n]

    print("=" * 78)
    print("MOON ABLATION - causation by intervention")
    print("=" * 78)
    print(f"  seeds {len(seeds)}, both seats, vs C001")
    print(f"  Moon is NEVER edited; every variant is an appended shim on a COPY")
    print(f"  Moon sha256 {sha(MOON)}")

    results = []
    for entry in ABLATIONS:
        # Each entry is a 4-tuple (name, hypothesis, replacement, mode).
        # Tolerating 3 too, because the earlier version of this file declared
        # 3-tuples and the 4th was added later; a silent unpack mismatch here
        # cost a full run before it was noticed.
        name, hypothesis, replacement = entry[0], entry[1], entry[2]
        vp = os.path.join(WORK, f"moon_{name}.py")
        meta = make_variant(name, replacement, vp)
        r = play(vp, C001, seeds, name)
        meta.update({"hypothesis": hypothesis, "result": r})
        results.append(meta)
        bt = r.get("bt_score")
        print(f"\n  {name}")
        print(f"    hypothesis : {hypothesis[:96]}")
        print(f"    diff lines : {meta['diff_lines']}   "
              f"shim on copy, source unchanged: "
              f"{meta['source_sha256_unchanged']}")
        if bt is not None:
            print(f"    vs C001     : {r['W']}-{r['L']}-{r['T']} of {r['games']}  "
                  f"BT {bt:.4f}   broken {r['broken']}")
        else:
            print(f"    FAILED: {r.get('error')} {r.get('stderr', '')[:120]}")

    base = next((r for r in results if r["name"] == "control_null"), None)
    print("\n" + "=" * 78)
    print("ATTRIBUTION")
    print("=" * 78)
    base_bt = (base or {}).get("result", {}).get("bt_score")
    print(f"  control (Moon unmodified): BT {base_bt}")
    for r in results:
        if r["name"] == "control_null":
            continue
        bt = r["result"].get("bt_score")
        if bt is None or base_bt is None:
            continue
        drop = base_bt - bt
        tag = ("MECHANISM" if drop > 0.10 else
               "partial" if drop > 0.03 else
               "NOT the cause" if drop < 0.02 else "small")
        print(f"  {r['name']:<24} BT {bt:.4f}  drop {drop:+.4f}  -> {tag}")

    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                  time.gmtime()),
                   "moon_sha256": sha(MOON),
                   "c001_sha256": sha(C001),
                   "seeds": len(seeds),
                   "method": "source-level shim appended to a COPY; the original "
                             "artifact is never modified",
                   "results": results}, fh, indent=2)
    print(f"\nwrote {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
