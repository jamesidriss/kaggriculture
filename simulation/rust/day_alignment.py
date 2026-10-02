"""Is the Rust/Python day-boundary mismatch a RULE divergence or a SAMPLING convention?

The first parity harness reported a divergence at day 1: Python showed market
CARROT=9998 and Rust showed 9999. That comparison was unfair, and saying so is
the whole point of this script.

What actually happened
---------------------
`kagg serve`'s GENGAME emits a day record AT the day roll. The Python harness
took the LAST observation seen within each day. Those are different instants:
step 24 (start of day 1) versus step 47 (end of day 1). A market restock that
fires once per roll will legitimately have been drawn once at the start of a day
and twice by its end, so a start/end mismatch manufactures a divergence out of
correct behaviour.

The decisive test
-----------------
Project Python at BOTH conventions -- first observation in each day, and last
observation in each day -- and compare each against Rust. Whichever convention
matches identifies the engines' shared sampling point, and simultaneously proves
whether the underlying rules agree. If NEITHER matches, it is a real divergence
and the engine is NO_GO for research use.

This is also why the 100/100 final-bank agreement is not sufficient on its own:
identical terminal cash can hide a mid-game divergence that cancels out. It is
reported as a necessary condition, not a sufficient one.
"""
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))
sys.path.insert(0, os.path.join(ROOT, "simulation", "rust"))

import parity as P  # noqa: E402

WORK = os.path.join(ROOT, "simulation", "rust")
OUT = os.path.join(WORK, "day_alignment.json")


def py_days_both_conventions(tape, seed):
    """Per-day records under both sampling conventions, from one Python run.

    first[d] : the earliest observation in day d  (should match Rust's roll)
    last[d]  : the latest observation in day d
    """
    from kaggle_environments import make
    env = make("kaggriculture",
               configuration={"seed": int(seed), "episodeSteps": 720})
    env.reset()

    def proj():
        o = None
        money = []
        for p in (0, 1):
            oo = env.steps[-1][p].observation
            try:
                d = oo.to_dict()
            except Exception:
                d = {k: v for k, v in vars(oo).items() if not k.startswith("_")}
            money.append(int((d.get("farms") or [{}, {}])[p].get("money", 0)))
            if p == 0:
                o = d
        inv = (o.get("market") or {}).get("inventory") or {}
        return {"day": int(o.get("day", 0)), "step": int(o.get("step", 0)),
                "money": money,
                "inventory": {k: int(v) for k, v in sorted(inv.items())}}

    first, last = {}, {}
    for seats in tape:
        cur = proj()
        d = cur["day"]
        if d not in first:
            first[d] = cur
        last[d] = cur
        env.step(seats)
    fin = proj()
    last[fin["day"]] = fin
    return first, last, fin


def main():
    n = int(sys.argv[sys.argv.index("--trajectories") + 1]) \
        if "--trajectories" in sys.argv else 20
    exe = sys.argv[sys.argv.index("--exe") + 1] if "--exe" in sys.argv else ""
    os.makedirs(WORK, exist_ok=True)
    if not exe or not os.path.exists(exe):
        print("  Rust CLI not found. Set --exe.")
        return 1

    kinds = ["legal", "empty_pos", "chaos", "noop"]
    tally = {"first": 0, "last": 0, "neither": 0, "error": 0}
    detail = []
    t0 = time.time()
    for kind in kinds:
        kt = {"first": 0, "last": 0, "neither": 0, "error": 0}
        for i in range(n):
            seed = 300000 + i
            tape = P.make_tape(seed, kind)
            tp = os.path.join(WORK, f"align_{kind}_{seed}.txt")
            P.write_tape(tape, seed, tp)
            first, last, fin = py_days_both_conventions(tape, seed)
            rs, err = P.rust_projection(exe, tp, seed)
            os.remove(tp)
            if rs is None:
                tally["error"] += 1
                kt["error"] += 1
                detail.append({"kind": kind, "seed": seed, "verdict": "ERROR",
                               "detail": err[:200]})
                continue
            rsm = {r["day"]: r for r in rs if not r.get("_final")}

            def same(rec):
                return (rec["money"] == rsm[rec["day"]]["money"]
                        and rec["inventory"] == rsm[rec["day"]]["inventory"])

            days = sorted(set(first) & set(rsm))
            if days and all(same(first[d]) for d in days):
                verdict = "first"
            elif days and all(same(last[d]) for d in days):
                verdict = "last"
            else:
                verdict = "neither"
            tally[verdict] += 1
            kt[verdict] += 1
            rec = {"kind": kind, "seed": seed, "verdict": verdict,
                   "days_common": len(days), "days_python": len(first),
                   "days_rust": len(rsm),
                   "banks_agree": fin["money"] == (rs[-1]["money"] if rs else None)}
            if verdict == "neither" and days:
                for d in days:
                    if not same(first[d]):
                        rec["first_bad_day"] = d
                        rec["py_first"] = first[d]
                        rec["py_last"] = last[d]
                        rec["rust"] = rsm[d]
                        break
            detail.append(rec)
        print(f"  {kind:<11} first={kt['first']:>3} last={kt['last']:>3} "
              f"neither={kt['neither']:>3} error={kt['error']:>3}")

    dur = time.time() - t0
    total = sum(tally.values())
    if tally["first"] == total:
        verdict = ("PARITY_VERIFIED_AT_ROLL -- Rust and Python agree exactly at "
                   "the day roll, the shared sampling point")
    elif tally["last"] == total:
        verdict = ("PARITY_VERIFIED_AT_DAY_END -- agree at day end, not at the "
                   "roll; still a shared sampling point, but report which")
    else:
        verdict = "NO_GO -- neither sampling convention reproduces the other"

    print("\n" + "=" * 78)
    print(f"  {total} trajectories, {dur:.0f}s")
    print(f"  matched FIRST-in-day (roll): {tally['first']}")
    print(f"  matched LAST-in-day  (end) : {tally['last']}")
    print(f"  matched neither            : {tally['neither']}")
    print(f"  rust errors                : {tally['error']}")
    banks = sum(1 for d in detail if d.get("banks_agree"))
    print(f"  final banks agree          : {banks}/{total}")
    print(f"\n  VERDICT: {verdict}")

    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"verdict": verdict, "tally": tally, "trajectories": total,
                   "seconds": round(dur, 1), "banks_agree": banks,
                   "detail": detail}, fh, indent=2)
    print(f"wrote {os.path.relpath(OUT, ROOT)}")
    return 0 if tally["neither"] == 0 and tally["error"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
