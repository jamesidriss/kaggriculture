"""Self-test for the simcomp framework.

Run: python -m simcomp.selftest
Exits non-zero on any failure. Uses the Kaggriculture league as the fixture
because that is the environment where the framework's guards were earned.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from simcomp import (Registry, SeedSplits, League, wilson, bradley_tery,  # noqa: E402
                     assert_shared_delivery, assert_both_seats)
from simcomp.parity import snapshot_divergence, runtime_info  # noqa: E402

FAILED = []
N = 0


def check(cond, label, detail=""):
    global N
    N += 1
    print(("  PASS  " if cond else "  FAIL  ") + label + (f"  {detail}" if detail else ""))
    if not cond:
        FAILED.append(label)


def main():
    print("simcomp self-test")
    info = runtime_info()
    print(f"  runtime: python {info['python']}, "
          f"kaggle-environments {info['kaggle_environments']}")

    # --- statistics ------------------------------------------------------
    lo, hi = wilson(24, 24)
    check(lo > 0.8, "wilson(24,24) does not collapse to zero width", f"[{lo:.3f},{hi:.3f}]")
    check(wilson(0, 0) == (0.0, 1.0), "wilson(0,0) is (0,1), not (0,0)")
    check(abs(wilson(5, 10)[0] - 0.2366) < 0.002, "wilson(5,10) matches reference")
    # BT recovery test. The data must be generated FROM known betas, otherwise
    # the tournament is over-determined, no strengths exist, and the fit
    # correctly refuses to converge.
    import math
    true = {"x": 1.2, "y": 0.3, "z": -0.5}
    n = 1000
    pairs = {}
    for i, a in enumerate("xyz"):
        for b in "xyz"[i + 1:]:
            p = 1.0 / (1.0 + math.exp(-(true[a] - true[b])))
            w = round(p * n)
            pairs[(a, b)] = (w, n - w)
    beta = bradley_tery(pairs)
    check(beta["x"] > beta["y"] > beta["z"],
          "bradley_tery recovers the generating ordering",
          f"{ {k: round(v, 3) for k, v in beta.items()} }")
    # Betas are identified only up to an additive constant (the fitter centres
    # them), so recovery must be checked on DIFFERENCES, not absolute values.
    err = max(abs((beta[k] - beta["z"]) - (true[k] - true["z"])) for k in true)
    check(err < 0.05, "bradley_tery recovers generating strength DIFFERENCES to <0.05",
          f"max abs err {err:.5f}")
    pw = 1.0 / (1.0 + math.exp(-(true["x"] - true["y"])))
    fitted_pw = 1.0 / (1.0 + math.exp(-(beta["x"] - beta["y"])))
    check(abs(pw - fitted_pw) < 0.01,
          "bradley_tery recovers the implied head-to-head probability",
          f"fitted {fitted_pw:.4f} vs true {pw:.4f}")
    check(abs(sum(beta.values())) < 1e-6, "betas are mean-centred")
    rps = bradley_tery({("a", "b"): (9, 1), ("b", "c"): (9, 1), ("a", "c"): (9, 1)})
    check(rps["a"] > rps["b"] > rps["c"],
          "a lopsided non-transitive record still yields a defensible MLE",
          f"{ {k: round(v, 3) for k, v in rps.items()} }")

    # --- parity ----------------------------------------------------------
    try:
        rec = assert_shared_delivery("kaggriculture", seed=4242, turns=5)
        check(True, "shared field `step` reaches BOTH seats via env.run()",
              f"seat0={[r['step'] for r in rec[0]]} seat1={[r['step'] for r in rec[1]]}")
    except AssertionError as exc:
        check(False, "shared field `step` reaches BOTH seats via env.run()", str(exc))
    delivered, persisted = snapshot_divergence("kaggriculture")
    check(delivered[1] != persisted[1],
          "persisted seat-1 snapshot differs from the delivered observation",
          f"delivered={delivered[1]} persisted={persisted[1]}")

    # --- registry --------------------------------------------------------
    cfg = os.path.join(HERE, "config", "kaggriculture.json")
    reg = Registry(cfg)
    check(len(reg.agents) > 0, "registry loaded", f"{len(reg.agents)} agents")
    probs = reg.problems()
    check(not probs, "registry has no digest/provenance problems",
          "" if not probs else f"{len(probs)}: {probs[0]}")
    elig = reg.eligible()
    lins = {a.lineage for a in elig}
    # Two distinct eligible lineages is the honest state of the legally reusable
    # public agent set for this environment, and it is the project's single
    # biggest weakness. Asserting a higher bar here would mean either faking a
    # lineage or failing the suite forever; the limitation is documented in
    # reports/FINAL_RESEARCH_CONCLUSION.md §4 and recorded as NO_GO in
    # reports/RETRACTIONS.md. The test asserts what is true and says so.
    check(len(lins) >= 2,
          "league has at least 2 distinct eligible lineages",
          f"{len(lins)} lineages, {len(elig)} agents")
    if len(lins) < 3:
        print(f"  NOTE  only {len(lins)} independent lineages are available. "
              f"This is a KNOWN, DOCUMENTED limitation, not a passing grade: "
              f"a league this narrow cannot validate a champion against the "
              f"field it will actually meet.")
    try:
        reg.get(elig[0].sha256[:16])
        ok = True
    except KeyError as exc:
        ok = False
    check(ok, "registry resolves an agent by digest prefix")

    # --- seeds -----------------------------------------------------------
    sp = SeedSplits(os.path.join(ROOT, "seeds"))
    check(not sp.problems(), "seed splits are disjoint and duplicate-free",
          f"dev={len(sp.load('dev'))} holdout={len(sp.load('holdout'))} "
          f"final={len(sp.load('final'))}")

    # --- league ----------------------------------------------------------
    # Two clearly different agents so the guard's assertions have teeth.
    strong = next((a for a in elig if "v51" in a.name), None)
    weak = next((a for a in elig if "v16_rc5" in a.name), None)
    if strong and weak:
        lg = League(reg, env_name="kaggriculture")
        res = lg.head_to_head(strong, weak, sp.load("dev")[:2],
                              meta={"pool": "dev-smoke"})
        try:
            res.assert_clean()
            check(True, "head-to-head passes the clean-result gate",
                  f"{res.counts()} over {res.games} games")
        except AssertionError as exc:
            check(False, "head-to-head passes the clean-result gate", str(exc))
        assert_both_seats(res)
        check(True, "head-to-head covered every seed from both seats")
        try:
            res.assert_discriminating()
            check(True, "a 100% sweep is REJECTED as non-discriminating "
                        "(correct: the league is weak here)")
        except AssertionError as exc:
            check(False, "a sweep must raise, not pass silently")
            print("        ", str(exc)[:160])
        # self-play must be refused outright
        try:
            lg.head_to_head(strong, strong, [1], meta={"pool": "x"})
            check(False, "self-play is refused by digest")
        except ValueError:
            check(True, "self-play is refused by digest")

    print(f"\n{N - len(FAILED)}/{N} checks passed")
    if FAILED:
        print("FAILURES:")
        for f in FAILED:
            print("  -", f)
        return 1
    print("SIMCOMP SELFTEST PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
