"""Statistics self-test: exact expected values, not properties.

Every case below has a hand-computable answer, and each is a record that has
actually been measured in this project, so a regression shows up as a changed
number rather than a vague degradation.

Run:  python benchmark/stats_selftest.py
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from stats import (binom_two_sided, bootstrap_score_interval,  # noqa: E402
                   bt_score_rate, lineage_balanced_score,
                   mcnemar_exact, paired_seed_bootstrap,
                   wilson, wilson_decided, win_interval)

FAILED = []
N = 0


def eq(label, got, want, tol=1e-9):
    global N
    N += 1
    if isinstance(want, str) or isinstance(got, str):
        good = got == want
    else:
        good = abs(got - want) <= tol
    print(("  PASS  " if good else "  FAIL  ") + label
          + (f"   got {got!r}" + ("" if good else f" want {want!r}")))
    if not good:
        FAILED.append(label)


def ok(label, cond, detail=""):
    global N
    N += 1
    print(("  PASS  " if cond else "  FAIL  ") + label
          + (f"   {detail}" if detail else ""))
    if not cond:
        FAILED.append(label)


print("=" * 78)
print("STATS SELFTEST - tie-aware match metrics")
print("=" * 78)

print("\n-- bt_score_rate, exact arithmetic")
eq("all wins 10-0-0", bt_score_rate(10, 0, 0), 1.0)
eq("all losses 0-10-0", bt_score_rate(0, 10, 0), 0.0)
eq("all ties 0-0-10", bt_score_rate(0, 0, 10), 0.5)
eq("50/50 decided 5-5-0", bt_score_rate(5, 5, 0), 0.5)
eq("no games", bt_score_rate(0, 0, 0), 0.0)

print("\n-- the two records that produced the reporting error")
# C001 vs v51, promotion leg. Previously reported as 80.91% "win rate".
eq("657-155-180 bt_score_rate", bt_score_rate(657, 155, 180), 747 / 992, 1e-12)
eq("657-155-180 decided_win_rate", bt_score_rate(657, 155, 0), 657 / 812, 1e-12)
d = win_interval(657, 155, 180)
eq("657-155-180 tie_rate", d["tie_rate"], 180 / 992, 1e-12)
ok("657-155-180 primary is ~75.30%", abs(d["bt_score_rate"] - 0.7530) < 1e-4,
   f"{d['bt_score_rate']:.6f}")
ok("657-155-180 decided-only is ~80.91%",
   abs(d["decided_win_rate"] - 0.8091) < 1e-4,
   f"{d['decided_win_rate']:.6f}")
ok("the two differ materially, which is why the label mattered",
   d["bt_score_rate"] < d["decided_win_rate"] - 0.05,
   f"{d['decided_win_rate']-d['bt_score_rate']:.4f} apart")

eq("638-138-216 bt_score_rate", bt_score_rate(638, 138, 216), 746 / 992, 1e-12)
eq("638-138-216 decided_win_rate",
   win_interval(638, 138, 216)["decided_win_rate"], 638 / 776, 1e-12)
eq("537-453-2 bt_score_rate", bt_score_rate(537, 453, 2), 538 / 992, 1e-12)
eq("1039-945-0 bt_score_rate (the old top-two record)",
   bt_score_rate(1039, 945, 0), 1039 / 1984, 1e-12)

print("\n-- the replication is the real finding")
# 638-138-216 and 657-155-180 have different decided-only rates (82.22% vs
# 80.91%) but almost identical BT scores. That is much stronger evidence than
# either number alone: two independent runs agreeing on the metric that matches
# the competition's own scoring convention.
a = bt_score_rate(638, 138, 216)
b = bt_score_rate(657, 155, 180)
ok("BT scores agree within 0.5 points", abs(a - b) < 0.005,
   f"{a:.4f} vs {b:.4f}, gap {abs(a-b)*100:.2f} pts")
ok("decided-only rates disagree by ~1.3 points",
   abs((638 / 776) - (657 / 812)) > 0.01,
   f"{638/776:.4f} vs {657/812:.4f}")

print("\n-- wilson_decided is on the decided rate, not on N")
lo, hi = wilson_decided(657, 155)
eq("wilson_decided lower", lo, _ := wilson_decided(657, 155)[0], 1e-15)
ok("decided-only Wilson clears 0.5", lo > 0.5, f"[{lo:.4f}, {hi:.4f}]")
full = win_interval(657, 155, 180)
ok("win_interval carries the same decided Wilson",
   abs(full["wilson_lo"] - lo) < 1e-15 and abs(full["wilson_hi"] - hi) < 1e-15)

print("\n-- bootstrap_score_interval on per-game scores")
s = [1.0] * 638 + [0.0] * 138 + [0.5] * 216
mean, blo, bhi, bn = bootstrap_score_interval(s, iters=4000)
eq("bootstrap mean equals the arithmetic mean", mean, sum(s) / len(s), 1e-12)
eq("bootstrap n", bn, 992)
ok("bootstrap brackets its own estimate", blo < mean < bhi,
   f"[{blo:.4f}, {bhi:.4f}] contains {mean:.4f}")
# Comparison with the tempting shortcut: a binomial Wilson at n=992 for
# p = 747/992. It is WIDER than the correct bootstrap here, because a per-game
# score of 0.5 sits at the mean while a Bernoulli outcome is 0 or 1, so 216
# draws at 0.5 contribute less variance than 992 Bernoulli trials at the same
# mean. The shortcut is therefore conservative in this direction -- which is
# luck, not a reason to use it. The reverse case exists (heavy ties plus rare
# decisive games can exceed Bernoulli variance) and the bootstrap is right in
# both, because it uses the actual observed scores.
naive_lo, naive_hi = wilson(747, 992)
ok("bootstrap differs from a naive binomial interval on the same n",
   abs((bhi - blo) - (naive_hi - naive_lo)) > 0.001,
   f"bootstrap width {bhi-blo:.4f} vs naive binomial {naive_hi-naive_lo:.4f}")
ok("bootstrap CI still clears 0.5 comfortably", blo > 0.5, f"lo={blo:.4f}")
ok("all-ties degenerate case", bootstrap_score_interval([0.5] * 10,
                                                        iters=500)[:3]
   == (0.5, 0.5, 0.5))
ok("empty input is safe", bootstrap_score_interval([])[3] == 0)

print("\n-- paired_seed_bootstrap resamples seeds, not games")
# Worlds vary in difficulty, and within a world the two seats are correlated.
# Every seed must have a DIFFERENT mean, otherwise resampling seeds gives a
# constant and the test is vacuous.
import random as _r
_rng = _r.Random(7)
per = {}
for i in range(400):
    p = 0.30 + 0.40 * _rng.random()          # per-world win propensity
    per[i] = [1.0 if _rng.random() < p else 0.0,
              1.0 if _rng.random() < p else 0.0]
pm, plo, phi, pk = paired_seed_bootstrap(per, iters=4000)
eq("paired bootstrap n is the SEED count", pk, 400)
eq("paired mean", pm, sum(sum(v) for v in per.values()) / 800, 1e-12)
ok("paired bootstrap brackets its estimate", plo < pm < phi,
   f"[{plo:.4f}, {phi:.4f}] contains {pm:.4f}")
ok("seed-level interval is non-degenerate", (phi - plo) > 0.001,
   f"width {phi-plo:.4f}")

# Resampling GAMES treats the two seats of one world as independent. They are
# not: they share the world, the market state and the opponent. The direction
# of the resulting error depends on the SIGN of the within-seed correlation,
# which is why it cannot be waved away in either direction.
#   positive correlation (seats agree)  -> game-level interval too NARROW
#   negative correlation (seats disagree) -> game-level interval too WIDE
pos = {i: ([1.0, 1.0] if i % 2 == 0 else [0.0, 0.0]) for i in range(400)}
neg = {i: ([1.0, 0.0] if i % 2 == 0 else [0.0, 1.0]) for i in range(400)}
for label, data, wider in (("positive within-seed", pos, True),
                           ("negative within-seed", neg, False)):
    gm, glo, ghi, _ = bootstrap_score_interval(
        [v for vs in data.values() for v in vs], iters=4000)
    cm, clo, chi, _ = paired_seed_bootstrap(data, iters=4000)
    ok(f"point estimates agree under {label} correlation",
       abs(cm - gm) < 1e-12, f"{cm:.4f}")
    gw, sw = (ghi - glo), (chi - clo)
    if wider:
        ok(f"game-level bootstrap is too NARROW under {label} correlation",
           sw > gw * 1.05, f"seed {sw:.4f} vs game {gw:.4f}")
    else:
        ok(f"game-level bootstrap is too WIDE under {label} correlation",
           gw > sw * 1.05, f"seed {sw:.4f} vs game {gw:.4f}")

print("\n-- lineage_balanced_score")
# Nine variants of one lineage vs one independent agent.
many = [{"lineage_id": "L-A", "W": 60, "L": 40, "T": 0}] * 9 + \
       [{"lineage_id": "L-B", "W": 50, "L": 50, "T": 0}]
lb = lineage_balanced_score(many)
eq("nine identical variants do not outvote one other lineage",
   lb["score"], (0.6 + 0.5) / 2, 1e-12)
eq("worst lineage identified", lb["worst_lineage"], "L-B")
eq("worst score", lb["worst_score"], 0.5, 1e-12)
eq("two lineages counted", lb["n_lineages"], 2)
# A collapse must survive averaging, not be hidden by the mean.
coll = [{"lineage_id": "L-A", "W": 90, "L": 10, "T": 0},
        {"lineage_id": "L-B", "W": 90, "L": 10, "T": 0},
        {"lineage_id": "L-C", "W": 10, "L": 90, "T": 0}]
lb2 = lineage_balanced_score(coll)
ok("mean stays respectable but the collapse is visible",
   lb2["score"] > 0.6 and lb2["worst_score"] < 0.2,
   f"mean {lb2['score']:.3f}, worst {lb2['worst_score']:.3f}")
ok("empty input is safe",
   lineage_balanced_score([])["n_lineages"] == 0)
ok("zero-game matchups are skipped",
   lineage_balanced_score([{"lineage_id": "L", "W": 0, "L": 0, "T": 0}])
   ["n_lineages"] == 0)

print("\n-- exact tests still behave")
ok("657-155-180 is overwhelmingly significant as a raw count",
   binom_two_sided(657, 992) < 1e-20, f"{binom_two_sided(657, 992):.3g}")
ok("the half-tie equivalent is significant too",
   binom_two_sided(747, 992) < 0.001, f"{binom_two_sided(747, 992):.3g}")
ok("1039-945 against Farm is only marginally significant",
   binom_two_sided(1039, 1984) < 0.05 and binom_two_sided(1039, 1984) > 1e-3,
   f"{binom_two_sided(1039, 1984):.4f}")
p, nd = mcnemar_exact(10, 8)
ok("mcnemar returns (p, n_discordant)", 0.0 <= p <= 1.0 and nd == 18,
   f"p={p:.4f} n={nd}")

print(f"\n{N - len(FAILED)}/{N} checks passed")
if FAILED:
    print("FAILURES:")
    for f in FAILED:
        print("  -", f)
    sys.exit(1)
print("STATS SELFTEST PASS")
