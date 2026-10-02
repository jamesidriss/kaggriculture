"""Validation of the canonical statistics module.

Run: python benchmark/stats_selftest.py

The point of this file is that the previous session published an interval that
did not belong to the win rate printed beside it, and nothing caught it. Every
interval that appears in a report must be reproducible from these checks.
"""
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "benchmark"))

from stats import (wilson, wilson_reference, win_interval, mcnemar_exact,   # noqa: E402
                   binom_two_sided, bt_identifiability, bradley_tery, Z95)

FAILED = []
N = 0


def check(cond, label, detail=""):
    global N
    N += 1
    line = ("  PASS  " if cond else "  FAIL  ") + label
    if detail:
        line += f"   {detail}"
    print(line)
    if not cond:
        FAILED.append(label)


def main():
    print("CANONICAL STATISTICS VALIDATION")
    print(f"  z(95%) = {Z95}")
    print()

    # ---- 1. reference agreement over a wide grid ------------------------
    print("-- wilson vs independent quadratic-formula implementation")
    worst = 0.0
    for n in (1, 5, 10, 24, 50, 72, 100, 144, 250, 500, 720, 792, 1000, 2000):
        for w in {0, 1, n // 4, n // 3, n // 2, (2 * n) // 3, n - 1, n}:
            if w < 0 or w > n:
                continue
            a = wilson(w, n)
            b = wilson_reference(w, n)
            worst = max(worst, abs(a[0] - b[0]), abs(a[1] - b[1]))
    check(worst < 1e-12, "two independent formulations agree to 1e-12",
          f"max abs diff {worst:.2e}")

    # ---- 2. closed-form expected values ---------------------------------
    # Computed by hand from the definition, not copied from a previous report.
    print("\n-- closed-form spot checks")
    cases = [
        (0, 10), (10, 10), (5, 10), (76, 144), (670, 720), (596, 720), (0, 792),
    ]
    print(f"  {'w/n':>10} {'observed':>9} {'wilson lo':>10} {'wilson hi':>10}")
    for w, n in cases:
        lo, hi = wilson(w, n)
        print(f"  {str(w) + '/' + str(n):>10} {w/n:>9.4f} {lo:>10.4f} {hi:>10.4f}")

    # 76/144 = 0.527778; the correct 95% Wilson interval is ~[0.4466, 0.6075].
    lo, hi = wilson(76, 144)
    check(abs(wilson(76, 144)[0] - 0.4466) < 5e-4 and abs(hi - 0.6075) < 5e-4,
          "wilson(76,144) == [0.4466, 0.6075]",
          f"[{lo:.4f}, {hi:.4f}]")
    # The previously published [0.3925, 0.5534] is the interval for 68/144.
    lo68, hi68 = wilson(68, 144)
    check(abs(lo68 - 0.3925) < 5e-4 and abs(hi68 - 0.5534) < 5e-4,
          "wilson(68,144) == [0.3925, 0.5534]  <- the mislabelled pair",
          f"[{lo68:.4f}, {hi68:.4f}]")
    check(not (abs(lo - 0.3925) < 1e-3),
          "76/144 does NOT reproduce the previously published lower bound",
          "so the old report mixed 76 wins with the interval for 68")

    lo, hi = wilson(0, 10)
    check(lo == 0.0 and 0.25 < hi < 0.32,
          "wilson(0,10) upper bound is finite and non-trivial", f"[{lo:.4f},{hi:.4f}]")
    lo, hi = wilson(10, 10)
    check(abs(hi - 1.0) < 1e-12 and 0.70 < lo < 0.75,
          "wilson(10,10) lower bound is finite and non-trivial", f"[{lo:.4f},{hi:.4f}]")
    lo, hi = wilson(5, 10)
    check(abs(lo - 0.2366) < 2e-3 and abs(hi - 0.7634) < 2e-3,
          "wilson(5,10) == [0.2366, 0.7634]", f"[{lo:.4f},{hi:.4f}]")
    lo, hi = wilson(670, 720)
    check(abs(lo - 0.9096) < 2e-3 and abs(hi - 0.9468) < 2e-3,
          "wilson(670,720) == [0.9096, 0.9468]", f"[{lo:.4f},{hi:.4f}]")
    lo, hi = wilson(596, 720)
    check(abs(lo - 0.7985) < 2e-3 and abs(hi - 0.8535) < 2e-3,
          "wilson(596,720) == [0.7985, 0.8535]", f"[{lo:.4f},{hi:.4f}]")
    lo, hi = wilson(0, 792)
    check(lo == 0.0 and abs(hi - 0.0048) < 2e-4,
          "wilson(0,792) == [0.0000, 0.0048]", f"[{lo:.4f},{hi:.4f}]")
    check(wilson(0, 0) == (0.0, 1.0),
          "wilson(0,0) is the whole unit interval, not a zero-width point")

    # ---- 3. symmetry ----------------------------------------------------
    print("\n-- invariants")
    for w, n in cases:
        a = wilson(w, n)
        b = wilson(n - w, n)
        check(abs((a[0] + b[1]) - 1.0) < 1e-12 and abs((a[1] + b[0]) - 1.0) < 1e-12,
              f"symmetry holds for {w}/{n}")
    for w in range(0, 21):
        lo, hi = wilson(w, 20)
        check(0.0 <= lo <= hi <= 1.0, f"ordering holds for {w}/20")

    # ---- 4. record helper cannot disagree with itself -------------------
    print("\n-- win_interval consistency")
    r = win_interval(76, 68, 0)
    check(abs(r["win_rate"] - 76 / 144) < 1e-12 and r["decided"] == 144,
          "win_interval rate matches its own counts", f"{r['win_rate']:.4f}")
    check(abs(r["wilson_lo"] - wilson(76, 144)[0]) < 1e-15,
          "win_interval interval is wilson() on the same counts")
    r2 = win_interval(10, 10, 5)
    check(r2["decided"] == 20 and r2["games"] == 25,
          "ties are excluded from the rate but retained in the game count",
          f"decided={r2['decided']} games={r2['games']}")

    # ---- 5. exact tests -------------------------------------------------
    print("\n-- exact tests")
    p, n = mcnemar_exact(45, 55)
    # Two-sided exact McNemar = 2 * P(X <= 45), X ~ Bin(100, 0.5) = 0.3682.
    # "Not significant" means p > 0.05, not p == 1.
    check(p > 0.05 and n == 100, "McNemar 45/55 is not significant", f"p={p:.4f}")
    p, n = mcnemar_exact(70, 30)
    check(p < 0.001 and n == 100, "McNemar 70/30 is significant", f"p={p:.2e}")
    check(abs(binom_two_sided(5, 10) - 1.0) < 1e-9,
          "exact binomial 5/10 is not significant")
    check(binom_two_sided(76, 144) < 0.7,
          "exact binomial on 76/144 is not significant", f"p={binom_two_sided(76,144):.4f}")

    # ---- 6. BT identifiability gate -------------------------------------
    print("\n-- Bradley-Terry identifiability")
    star = {}
    for opp in ("b", "c", "d", "e"):
        # Only the hub's own rows. The hub wins every game it plays, so its
        # likelihood is +infinity and no finite MLE exists.
        star[("hub", opp)] = (72, 0)
    idn = bt_identifiability(star)
    check(not idn["ok"] and set(idn["zero_loss"]) == {"hub"},
          "a hub that never loses is detected as unbounded", str(idn["zero_loss"]))
    try:
        bradley_tery(star)
        check(False, "BT refuses an unbounded result set")
    except ValueError as exc:
        check("not identifiable" in str(exc),
              "BT refuses an unbounded result set with a reason")

    connected = {}
    names = "abcde"
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            # One entry per unordered pair. An even split is the BT equilibrium,
            # so the correct answer is all-zero betas. Storing both directions
            # would double-count the same games and invent a gradient.
            connected[(a, b)] = (50, 50)
    check(bt_identifiability(connected)["ok"],
          "a connected, all-decided set is identifiable")
    beta = bradley_tery(connected)
    check(all(abs(v) < 1e-6 for v in beta.values()),
          "an evenly split round robin yields all-zero betas",
          str({k: round(v, 6) for k, v in beta.items()}))

    # recovery test from known parameters
    true = {"p": 0.9, "q": 0.0, "r": -0.9}
    n = 1000
    rec = {}
    for i, a in enumerate("pqr"):
        for b in "pqr"[i + 1:]:
            pr = 1 / (1 + math.exp(-(true[a] - true[b])))
            w = round(pr * n)
            rec[(a, b)] = (w, n - w)
    b2 = bradley_tery(rec)
    check(b2["p"] > b2["q"] > b2["r"],
          "BT recovers the generating ordering from synthetic data",
          str({k: round(v, 3) for k, v in b2.items()}))

    print(f"\n{N - len(FAILED)}/{N} checks passed")
    if FAILED:
        print("FAILURES:")
        for f in FAILED:
            print("  -", f)
        return 1
    print("STATISTICS VALIDATION PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
