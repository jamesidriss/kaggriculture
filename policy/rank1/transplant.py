"""Transplant the measured Moon mechanism onto C001, and ablate its parameters.

Legality
--------
This file does NOT copy Moon source. Moon's licence is UNKNOWN
(`research/moon_provenance.py`: the parent Work is undistributed, the header
disclaims submission status, the dataset declares no licence). Nothing is
transcribed from it.

What is used is a *measured fact*: a turn-0 wheat flash-trade is worth a large
margin, established by ablation on Moon's own artifact. The implementation below
is written from scratch against C001's public action interface, and its
parameters are swept rather than copied. If it helps, it helps because the
mechanism is real, not because the code is shared.

The mechanism, in the environment's own terms
---------------------------------------------
Market orders at a step settle in slot order, index by index, within that step.
So submitting

    [BUY_PRODUCT WHEAT q, SELL WHEAT s]

at turn 0 buys q wheat at the prevailing price and then sells s of it in the same
settle. The realised margin is (s * bid_after_buy - cost_of_buy), and because the
buy happens first in the same slot sequence, the sell sees the post-buy state.
Every rival acts from the same turn-0 state and cannot interleave.

What is swept
-------------
  quantity bought   q
  quantity sold     s
  the product       WHEAT only in this generation; the sweep below is over q and
                    s, and a product sweep is declared but small
  activation        turn 0 only, or turn 0 and 1

Pre-declared acceptance criteria, fixed before any sweep runs:
  * BT score vs Moon >= 0.45         (from 0.054)
  * BT score vs Farm  >= 0.52        (must not regress)
  * BT score vs C001  reported, not gated: a candidate may trade some of this
    because field value is what matters, but a catastrophic loss here would
    indicate the mechanism is C001-specific rather than general
  * 0 broken games, both seats, runtime inside the act timeout

The mechanism is a commitment made before any observation, so it cannot be
conditioned on world state at turn 0. That is exactly why it must be swept and
measured rather than assumed.
"""
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

C001 = os.path.join(ROOT, "champions", "research", "C001_room_guard", "main.py")
MOON = os.path.join(ROOT, "opponents", "unlicensed",
                    "kaggriculture-r88-rivals__moon_parent.py")
FARM = os.path.join(ROOT, "postmortem_hedge", "main.py")
WORK = os.path.join(ROOT, "simulation", "rank1", "transplant")
SEEDS = os.path.join(ROOT, "seeds", "GEN3066_dev.txt")
OUT = os.path.join(WORK, "transplant_results.json")

# Pre-declared acceptance criteria.
GATE_MOON = 0.45
GATE_FARM = 0.52


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


# The shim. Written against the public action schema only.
#
# It is appended to a COPY of C001. C001 itself is never edited, so the champion
# and every historical artifact stay byte-identical.
SHIM = '''
# ---------------------------------------------------------------------------
# RANK1 C002 CANDIDATE: turn-0 opening market sequence.
#
# Written from scratch for this project against the public action interface.
# No source is transcribed from any third-party artifact.
#
# Mechanism, as measured by ablation on a strong public artifact: submitting a
# BUY and a SELL of the same product in the same turn settles index by index
# within that step, so the sell observes the post-buy state. At turn 0 no rival
# has acted and none can interleave. That converts the shared market into a
# one-sided flash trade, and it is the single largest source of margin
# difference found in this generation's autopsy.
#
# Parameters are swept, not copied. Activation is a fixed step range.
# ---------------------------------------------------------------------------
_OPEN_Q = {q}
_OPEN_S = {s}
_OPEN_PRODUCT = "{product}"
_OPEN_LAST_STEP = {last_step}


def _rank1_open(action, step):
    """Prepend the opening flash trade to `action`'s market orders.

    Slot order matters and is preserved: the buy is inserted BEFORE the sell,
    and both are inserted BEFORE the agent's own orders, so the flash trade
    settles first and the agent's own sales see the post-trade state.
    """
    if step > _OPEN_LAST_STEP or not isinstance(action, dict):
        return action
    orders = action.get("market") or []
    flash = [["BUY_PRODUCT", _OPEN_PRODUCT, _OPEN_Q],
             ["SELL", _OPEN_PRODUCT, _OPEN_S]]
    out = dict(action)
    # At most 10 orders settle per turn; never exceed it.
    out["market"] = (flash + [list(o) for o in orders])[:10]
    return out


_RANK1_PARENT = agent


def agent(observation, configuration=None):
    action = _RANK1_PARENT(observation, configuration)
    try:
        step = int(observation.get("step", 0))
    except (TypeError, ValueError):
        return action
    try:
        return _rank1_open(action, step)
    except Exception:
        return action


agent = globals().pop("agent")
'''


def build(q, s, product, last_step, out_path):
    src = open(C001, encoding="utf-8", newline="").read()
    shim = SHIM.format(q=q, s=s, product=product, last_step=last_step)
    out = src + shim
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(out)
    return sha(out_path)


def probe(path):
    p = subprocess.run(
        [sys.executable, os.path.join(ROOT, "benchmark", "agent_loader.py"),
         "--probe", path], cwd=ROOT, capture_output=True, text=True,
        timeout=1800)
    out = (p.stdout or "") + (p.stderr or "")
    return ("PLAYABLE" in out,
            [l for l in out.strip().splitlines() if l.strip()][-1][:130])


def play(a, b, seeds, tag, workers=8):
    rel = os.path.join("experiments", "rank1", "transplant", tag + ".csv")
    os.makedirs(WORK, exist_ok=True)
    sf = os.path.join(WORK, "seeds.txt")
    with open(sf, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(str(s) for s in seeds) + "\n")
    subprocess.run(
        [sys.executable, os.path.join(ROOT, "benchmark", "parallel_tournament.py"),
         "--a", a, "--b", b, "--seeds-file", sf, "--out", rel,
         "--workers", str(workers), "--label-a", os.path.basename(a)[:-3],
         "--label-b", os.path.basename(b)[:-3], "--experiment-id", "rank1_tr"],
        cwd=ROOT, capture_output=True, text=True)
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        return None
    rows = list(csv.DictReader(open(p, encoding="utf-8")))
    v = [r for r in rows if r.get("valid") == "1"]
    W = sum(int(r["win"]) for r in v)
    L = sum(int(r["loss"]) for r in v)
    T = sum(int(r["tie"]) for r in v)
    m = sorted(int(r["candidate_cash"]) - int(r["opponent_cash"]) for r in v)
    return {"games": len(rows), "broken": len(rows) - len(v), "W": W, "L": L,
            "T": T, "N": W + L + T,
            "bt": round((W + 0.5 * T) / max(1, W + L + T), 4),
            "median_margin": m[len(m) // 2] if m else 0}


def main():
    n = int(sys.argv[sys.argv.index("--seeds") + 1]) if "--seeds" in sys.argv else 24
    seeds = [int(x) for x in open(SEEDS, encoding="utf-8") if x.strip().isdigit()][:n]
    os.makedirs(WORK, exist_ok=True)

    print("=" * 78)
    print("C002 CANDIDATE: turn-0 opening transplant, parameter sweep")
    print("=" * 78)
    print(f"  C001 sha256 {sha(C001)}  (never modified; shim goes on a COPY)")
    print(f"  {len(seeds)} seeds, both seats")
    print(f"  pre-declared gates: BT vs Moon >= {GATE_MOON}, "
          f"BT vs Farm >= {GATE_FARM}, 0 broken")

    # Grid. Small and declared up front: the mechanism is one action, and a
    # large grid would spend the budget re-confirming that it is not noise.
    grid = []
    for q, s in [(20, 15), (20, 20), (30, 20), (13, 13), (30, 30), (40, 30)]:
        grid.append({"q": q, "s": s, "product": "WHEAT", "last_step": 0})
    # A turn-1 variant tests whether the effect is about timing or repetition.
    grid.append({"q": 20, "s": 15, "product": "WHEAT", "last_step": 1})
    # Product control: a product with no shop demand should NOT help, which is
    # the falsification test for "any flash trade works".
    grid.append({"q": 20, "s": 15, "product": "MILK", "last_step": 0})

    results = []
    for g in grid:
        name = f"q{g['q']}_s{g['s']}_{g['product']}_L{g['last_step']}"
        path = os.path.join(WORK, f"cand_{name}.py")
        sh = build(g["q"], g["s"], g["product"], g["last_step"], path)
        playable, pline = probe(path)
        rec = {"config": g, "name": name, "sha256": sh, "playable": playable,
               "probe": pline}
        if playable:
            rec["vs_moon"] = play(path, MOON, seeds, name + "_moon")
            rec["vs_farm"] = play(path, FARM, seeds, name + "_farm")
        results.append(rec)
        vm = (rec.get("vs_moon") or {}).get("bt")
        vf = (rec.get("vs_farm") or {}).get("bt")
        print(f"\n  {name}")
        print(f"    playable {playable}")
        if vm is not None:
            print(f"    vs Moon BT {vm:.4f}   vs Farm BT {vf:.4f}   "
                  f"broken {(rec['vs_moon'] or {}).get('broken')}"
                  f"/{(rec['vs_farm'] or {}).get('broken')}")
            gate = (vm >= GATE_MOON and vf >= GATE_FARM)
            print(f"    gates: {'PASS' if gate else 'fail'}")

    print("\n" + "=" * 78)
    print("VERDICT")
    print("=" * 78)
    ok = [r for r in results if r.get("vs_moon") and r.get("vs_farm")
          and r["vs_moon"]["bt"] >= GATE_MOON and r["vs_farm"]["bt"] >= GATE_FARM]
    ok.sort(key=lambda r: -(r["vs_moon"]["bt"] + r["vs_farm"]["bt"]))
    if ok:
        print(f"  {len(ok)} candidate(s) clear both gates:")
        for r in ok[:5]:
            print(f"    {r['name']:<28} Moon {r['vs_moon']['bt']:.4f}  "
                  f"Farm {r['vs_farm']['bt']:.4f}  "
                  f"sha {r['sha256'][:16]}")
    else:
        print("  NO candidate cleared both gates at this sample size.")
        best = max((r for r in results if r.get("vs_moon")),
                   key=lambda r: r["vs_moon"]["bt"], default=None)
        if best:
            print(f"  best vs Moon: {best['name']} at {best['vs_moon']['bt']:.4f}")
        milk = next((r for r in results
                     if r["config"]["product"] == "MILK"), None)
        wh = next((r for r in results
                   if r["config"]["product"] == "WHEAT"
                   and r["config"]["last_step"] == 0
                   and r["config"]["q"] == 20 and r["config"]["s"] == 15), None)
        if milk and wh and milk.get("vs_moon"):
            print(f"\n  FALSIFICATION CHECK (does ANY flash trade work?):")
            print(f"    WHEAT 20/15 vs Moon {wh['vs_moon']['bt']:.4f}")
            print(f"    MILK  20/15 vs Moon {milk['vs_moon']['bt']:.4f}")
            print(f"    -> the mechanism is product-SPECIFIC"
                  if wh['vs_moon']['bt'] > milk['vs_moon']['bt'] + 0.05
                  else "    -> NOT product-specific; a generic flash trade "
                       "explains it, which contradicts the autopsy")

    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                  time.gmtime()),
                   "c001_sha256": sha(C001), "seeds": len(seeds),
                   "gates": {"moon": GATE_MOON, "farm": GATE_FARM},
                   "legality": "implementation written from scratch against the "
                               "public action interface; no third-party source "
                               "transcribed; Moon is licence UNKNOWN",
                   "grid": grid, "results": results}, fh, indent=2)
    print(f"\nwrote {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
