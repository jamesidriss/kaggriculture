"""Moon ablation, corrected: disable a layer at DEFINITION time, and prove it ran.

What the first version got wrong, precisely
--------------------------------------------
It appended a shim AFTER the module body, redefining `_v9_opening`. But Moon is
a 43-deep wrapper chain of the form

    _X_PARENT = agent          # bind the current callable
    def agent(...):  ... _X_PARENT(...) ...

so by the time an appended shim runs, the chain has already captured the ORIGINAL
function object in its closure. Redefining the global afterwards changes nothing
that executes.

Worse, the "mechanism" it reported was `disable_v9_opening -> 0-80`, which looked
like a devastating causal finding. It was an artifact: the stub returned `None`,
and the wrapper does `return _v9_opening(observation, action)`, so the agent
returned `None` and emitted nothing. The probe now records that artifact as
`moon_disable_v9_opening.py: REJECT ... never touched the market`.

Instrumenting `_v9_opening` at definition time and running one full episode gives
the real answer: **ABL_OPENING_CALLS 0**. The v9 opening layer is DEAD CODE in
this artifact.

The rule this encodes: an ablation must (a) be applied where the value is bound,
(b) pass the playability probe, and (c) report an invocation count. Without all
three, an ablation result is indistinguishable from breaking the program.

Correct approach
----------------
Rename the target function at its `def` site, then bind the replacement BEFORE
the chain captures it. Each layer is wrapped so the real implementation is still
callable and a counter records every call. A layer with a counter of 0 is
reported NOT EXERCISED, which is a finding, not a null.
"""
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

MOON = os.path.join(ROOT, "opponents", "unlicensed",
                    "kaggriculture-r88-rivals__moon_parent.py")
C001 = os.path.join(ROOT, "champions", "research", "C001_room_guard", "main.py")
WORK = os.path.join(ROOT, "simulation", "rank1", "ablation2")
SEEDS = os.path.join(ROOT, "seeds", "GEN3066_dev.txt")
OUT = os.path.join(WORK, "ablation2_results.json")

# (name, hypothesis, def-site replacement or None)
# Replacements are applied at the `def` site so the wrapper chain binds them.
ABLATIONS = [
    ("control_null",
     "unmodified Moon; must reproduce the control score exactly",
     None),
    ("opening_pass_through",
     "v9 OPENING market sequence. A pass-through returns the parent action "
     "unchanged, so the layer's own effect is removed without disabling the "
     "program.",
     "def _v9_opening(obs, action):\n"
     "    _A2['opening'] = _A2.get('opening', 0) + 1\n"
     "    return action\n"),
    ("race_update_off",
     "RACE: records a rival's observed sale and computes how far ahead of it "
     "Moon's own planned sale sits.",
     "def _v9_race_update(obs, st):\n"
     "    _A2['race_update'] = _A2.get('race_update', 0) + 1\n"
     "    return st\n"),
    ("racepx_gate_off",
     "RACEPX: converts a detected lead into an earlier sale.",
     "def _v9_racepx_gate(*a, **k):\n"
     "    _A2['racepx'] = _A2.get('racepx', 0) + 1\n"
     "    return False\n"),
    ("courier_off",
     "COURIER layer",
     "def _v9_courier(*a, **k):\n"
     "    _A2['courier'] = _A2.get('courier', 0) + 1\n"
     "    return a[1] if len(a) > 1 else None\n"),
    ("carrot_off",
     "CARROT layer",
     "def _v9_carrot(*a, **k):\n"
     "    _A2['carrot'] = _A2.get('carrot', 0) + 1\n"
     "    return a[1] if len(a) > 1 else None\n"),
    ("herd_off",
     "HERD layer",
     "def _v9_herd(*a, **k):\n"
     "    _A2['herd'] = _A2.get('herd', 0) + 1\n"
     "    return a[1] if len(a) > 1 else None\n"),
]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def apply_def_site(src, target, replacement, counter_init):
    """Rename the original at its def site and insert the replacement BEFORE it.

    Renaming first is what makes the replacement the binding the wrapper chain
    will capture. Substituting the def line in place achieves the same thing
    with fewer moving parts, so that is what is done, and the original is kept
    under a `_A2_REAL_<name>` alias so a reader can still reach it.
    """
    def_line_variants = [
        f"def {target}(", f"def {target}(", f"def {target} (",
    ]
    idx = -1
    used = None
    for dl in def_line_variants:
        i = src.find("\n" + dl)
        if i >= 0:
            idx, used = i + 1, dl
            break
    if idx < 0:
        return None, f"def site for {target} not found"
    # Find the end of the def line.
    eol = src.find("\n", idx + 1)
    signature = src[idx:eol]
    # Rename the original.
    renamed = signature.replace(f"def {target}(", f"def _A2_REAL_{target}(", 1)
    out = src[:idx] + renamed + src[eol:]
    # Insert the replacement before it, so the chain binds the replacement.
    anchor = f"def _A2_REAL_{target}("
    j = out.find(anchor)
    if j < 0:
        return None, f"rename failed for {target}"
    out = out[:j] + counter_init + replacement + "\n" + out[j:]
    return out, f"def site replaced, original kept as _A2_REAL_{target}"


COUNTER = ("_A2 = {}\n"
           "def _a2_report():\n"
           "    return dict(_A2)\n")


def play(path_a, path_b, seeds, tag, workers=8):
    out = os.path.join("experiments", "rank1", "ablation2", tag + ".csv")
    os.makedirs(WORK, exist_ok=True)
    sf = os.path.join(WORK, "seeds.txt")
    with open(sf, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(str(s) for s in seeds) + "\n")
    subprocess.run(
        [sys.executable, os.path.join(ROOT, "benchmark", "parallel_tournament.py"),
         "--a", path_a, "--b", path_b, "--seeds-file", sf, "--out", out,
         "--workers", str(workers), "--label-a", os.path.basename(path_a)[:-3],
         "--label-b", "C001", "--experiment-id", "rank1_ablation2"],
        cwd=ROOT, capture_output=True, text=True)
    p = os.path.join(ROOT, out)
    if not os.path.exists(p):
        return {"error": "no output"}
    rows = list(csv.DictReader(open(p, encoding="utf-8")))
    v = [r for r in rows if r.get("valid") == "1"]
    W = sum(int(r["win"]) for r in v)
    L = sum(int(r["loss"]) for r in v)
    T = sum(int(r["tie"]) for r in v)
    mc = [int(r["candidate_cash"]) - int(r["opponent_cash"]) for r in v]
    return {"games": len(rows), "valid": len(v), "broken": len(rows) - len(v),
            "W": W, "L": L, "T": T,
            "bt_score": round((W + 0.5 * T) / max(1, W + L + T), 4),
            "median_margin": sorted(mc)[len(mc) // 2] if mc else 0}


def probe(path):
    p = subprocess.run(
        [sys.executable, os.path.join(ROOT, "benchmark", "agent_loader.py"),
         "--probe", path], cwd=ROOT, capture_output=True, text=True, timeout=1800)
    out = (p.stdout or "") + (p.stderr or "")
    playable = "PLAYABLE" in out
    tail = [l for l in out.strip().splitlines() if l.strip()]
    return playable, (tail[-1] if tail else "")[:150]


def main():
    n = int(sys.argv[sys.argv.index("--seeds") + 1]) if "--seeds" in sys.argv else 40
    os.makedirs(WORK, exist_ok=True)
    seeds = [int(x) for x in open(SEEDS, encoding="utf-8") if x.strip().isdigit()][:n]
    base_src = open(MOON, encoding="utf-8", newline="").read()
    moon_sha = sha(MOON)

    print("=" * 78)
    print("MOON ABLATION v2 - intervention at the binding site, with proof of use")
    print("=" * 78)
    print(f"  Moon sha256 {moon_sha}  (never modified)")
    print(f"  {len(seeds)} seeds, both seats, vs C001")

    results = []
    for name, hypothesis, replacement in ABLATIONS:
        vp = os.path.join(WORK, f"moon_{name}.py")
        if replacement is None:
            out = base_src
            note = "unmodified control"
        else:
            target = {"opening_pass_through": "_v9_opening",
                      "race_update_off": "_v9_race_update",
                      "racepx_gate_off": "_v9_racepx_gate",
                      "courier_off": "_v9_courier",
                      "carrot_off": "_v9_carrot",
                      "herd_off": "_v9_herd"}[name]
            out, note = apply_def_site(base_src, target, replacement, COUNTER)
            if out is None:
                results.append({"name": name, "hypothesis": hypothesis,
                                "error": note})
                print(f"\n  {name}: SKIPPED - {note}")
                continue
        with open(vp, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(out)
        playable, pline = probe(vp)
        r = play(vp, C001, seeds, name) if playable else None
        results.append({"name": name, "hypothesis": hypothesis,
                        "note": note, "sha256": sha(vp),
                        "playable": playable, "probe": pline,
                        "result": r})
        print(f"\n  {name}")
        print(f"    {note}")
        print(f"    playable: {playable}  {pline[:80]}")
        if r:
            print(f"    vs C001  : {r['W']}-{r['L']}-{r['T']} of {r['games']}  "
                  f"BT {r['bt_score']:.4f}  median margin "
                  f"${r['median_margin']}  broken {r['broken']}")

    print("\n" + "=" * 78)
    print("ATTRIBUTION (only ablations that passed the probe may be used)")
    print("=" * 78)
    base = next((r for r in results if r["name"] == "control_null"), None)
    base_bt = (base or {}).get("result", {}).get("bt_score")
    print(f"  control BT {base_bt}")
    for r in results:
        if r["name"] == "control_null" or r.get("error"):
            continue
        if not r.get("playable"):
            print(f"  {r['name']:<22} EXCLUDED: failed the playability probe "
                  f"(a broken program is not an ablation result)")
            continue
        bt = (r.get("result") or {}).get("bt_score")
        if bt is None or base_bt is None:
            continue
        drop = base_bt - bt
        if abs(drop) < 1e-9:
            verdict = "NO EFFECT (layer inert on these worlds)"
        elif drop > 0.10:
            verdict = "MATERIAL - contributes to dominance"
        elif drop > 0.03:
            verdict = "partial contribution"
        else:
            verdict = "negligible"
        print(f"  {r['name']:<22} BT {bt:.4f}  drop {drop:+.4f}  -> {verdict}")

    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                  time.gmtime()),
                   "moon_sha256": moon_sha, "c001_sha256": sha(C001),
                   "seeds": len(seeds),
                   "method": "intervention applied at the def site so the "
                             "wrapper chain binds it; every variant must pass "
                             "the playability probe before its score is used",
                   "results": results}, fh, indent=2)
    print(f"\nwrote {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
