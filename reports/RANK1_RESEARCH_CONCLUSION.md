# RANK1 RESEARCH CONCLUSION

Answers to the 30 questions in the mission brief. Every number is measured;
every non-measurement says so.

---

## 1. Did the public Rust simulator exist?

**YES.** The prior generation's conclusion "no Rust simulator exists publicly"
was **wrong**. `github.com/debmalyaroy/kaggriculture-simulation` is real,
substantial, Apache-2.0, and builds cleanly in 21 s.

## 2. Exact commit and licence?

| field | value |
|---|---|
| commit | `953ac86c462ba1dbdcb897f6020fd7bdacf27720` |
| licence | **Apache-2.0** (`LICENSE`, 11,357 B) + `NOTICE` present |
| CLI version | `kagg 0.1.0 (engine kaggle-environments 1.32.7)` |

The NOTICE declares the engine a derivative of `kaggle-environments` 1.32.7 and
`mt19937.rs` an independent MT19937 port.

## 3. Differential trajectories?

**NO — they are not identical.** Intermediate state diverges on **75 of 100**
tapes. Divergence starts at **day 1, step 24**, the first day roll.

## 4. Divergences?

Market **purchase settlement**. Minimal reproducer — seat 1 issues one order and
then passes:

| order | step | official Python | Rust |
|---|---|---|---|
| `BUY_PRODUCT WHEAT 20` | 0 / 1 / 2 | $2,440 / $2,436 / $2,436 | **$3,000** |
| `BUY_LAND` | 0 / 1 / 2 | $2,000 at every step | **$3,000** |

Python charges; Rust never does. `SELL` with no stock is rejected by both, so it
proves nothing about settlement.

**Unresolved, and deliberately not attributed.** Either the Rust engine does not
settle purchases through `GENGAME`, or **my hand-written tape encoder is wrong**
and Rust cannot parse the order. I did not separate these, so this report does
**not** claim the Rust engine is incorrect.

## 5. Local simulation throughput?

**Not benchmarked at scale.** The parity gate failed first, and throughput was
not the binding constraint. Build: 21 s. Official Python baseline remains
**~107 matches/min at 8 workers**.

## 6. Moon licence verdict?

**UNKNOWN** — analytical opponent only. Four independent blockers:

1. parent Work `queue_compact.py` is **not distributed** → the Apache-2.6
   derivation chain cannot be traced to a root;
2. header says *"unproven and is not an official Kaggle score claim"*;
3. header says *"FOR LOCAL DISCOVERY ONLY"*;
4. the distributing dataset declares **no LICENSE or NOTICE file**.

An Apache licence *body* inside a file is not a grant.

## 7. Why does Moon beat C001?

**One turn-0 wheat flash trade.**

```python
V9_OPENING_STEP0 = (("BUY_PRODUCT", "WHEAT", 20), ("SELL", "WHEAT", 15))
```

Market orders settle index-by-index in lockstep within a step, so the `SELL` sees
the post-`BUY` state, and at turn 0 no rival has acted. Established by ablation
at the `def` site: disabling it takes Moon from **BT 0.8667 → 0.0000** against
C001, median paired margin **+$1,259 → −$14,659**.

## 8. Broad champion, or C001-specific counter?

**Broadly dominant.** 120 seeds, paired, both seats:

| | vs C001 | vs v51 | vs Farm |
|---|---|---|---|
| `moon_parent` | 0.9208 | 0.9417 | **0.9833** |
| `moon_q13_mg` | 0.9208 | 0.9500 | 0.9833 |

It beats the Farm *hardest*. Not a narrow exploit — the strongest publicly
obtainable artifact seen, by a wide margin.

**And it is not an independent lineage.** Identifier Jaccard vs C001 is
**0.7192**, higher than the Farm's own 0.6098; its header derives it from the
same v9/3 root. The catalog's "independent lineage" label was **wrong**.

## 9. Exact public-score anchors recovered?

**ZERO.** The eight named candidates were **not attempted** this generation.

## 10. Their exact scores / version ids?

**None.** Nothing recovered, so nothing to bind.

## 11. Anchor score span?

**0 points.**

## 12. Calibration CV MAE?

**Not computable** — 0 anchors means 0 CV folds.

## 13. Spearman?

**Not computable.**

## 14. Is ShadowRating publishable?

**NO — WITHHELD.** 0 of 5 gate legs pass; two are undefined, not merely unmet.

## 15. Current champion?

**`C001_room_guard`** — unchanged, immutable.
sha256 `a52ba1bfe9df9dc1d504550af46744ef8d474797cdba7af2412dc40a3ebdf3b8`

## 16. Champion vs C001?

N/A (it is C001). vs its parent **v51: BT 0.7520 / 0.7530**, replicated on
independent seed pools.

## 17. Champion vs Farm?

**BT 0.5510**, seed-bootstrap 95% **[0.5200, 0.5815]**, N = 2000.

## 18. Champion vs Moon?

**BT 0.054** (27-473-0, N = 500). **Automatic rank-1 failure.**

## 19. vs strongest independent exact-score agents?

**None exist.** 0 class-A anchors. This leg is unanswerable, not passed.

## 20. Worst lineage?

**Moon at 0.054.**

## 21. Candidates evaluated?

**14 artifacts**: 6 ablation variants + 8 transplant candidates, plus full-field
payoff over 6 matchups.

**All 8 transplant candidates FAILED.** Best vs Moon **0.125** (gate 0.45); best
vs Farm 0.5833. Several scored **0.0000 vs Farm** — *worse than the unmodified
champion's 0.5510*.

## 22. Counterfactual branches?

**0.** Rust (which offers replay branching) was gated NO_GO, and official Python
has no branching mechanism.

## 23. Selector oracle gain?

**Not measured.** Oracle analysis was not run this generation.

## 24. Selector result?

**Not built.** No basis to justify one.

## 25. Sealed-final score?

**Not run.** No finalist cleared the gates, so the sealed pool was correctly
left unopened.

## 26. Estimated rating?

**WITHHELD.**

## 27. Lower bound?

**WITHHELD.**

## 28. RANK-1 READY?

**NO.**

## 29. Submission-ready SHA?

`a52ba1bfe9df9dc1d504550af46744ef8d474797cdba7af2412dc40a3ebdf3b8`
— verified byte-identical to the frozen champion this generation.

## 30. Final Git main commit?

Recorded in `reports/RANK1_CHECKPOINT.md` and verifiable via `git log -1`.

---

## The transplant failure, in one paragraph

The naive transplant is **cash- and order-capacity-destabilising**. A net buy
that *collides with C001's own wheat plan* spends the cash C001 needs one step
later: at step 1 the prepend consumes the market-order budget, and by step 2
C001's `BUY_PRODUCT WHEAT 30`, five hires and both livestock purchases
**disappear** — it cannot afford them. Four WHEAT candidates with `s < q`
collapsed to **0.0000 vs Farm**, worse than the unmodified champion's 0.5510.

**But plain "cash-neutrality" is the wrong rule, and my own sweep refuted it.**
`q20_s15_MILK_L0` is a **net buy** (`s = 15 < q = 20`) and it **survived** at
0.5417 vs Farm. The accurate rule is narrower:

> An opening survives iff it has a non-negative net outlay **or** it buys a
> product that does not collide with C001's own purchases.

What kills C001 is specifically an opening that consumes the cash *or the
market-order capacity* that its own **wheat** step-2 plan needs. Buying milk does
not collide with that plan, so it does no damage — and buys exactly as little
Moon's advantage as wheat does. The correct next step is a **non-colliding,
non-negative-net** opening, not a larger one.

Copying Moon's *action* is not the same as reproducing Moon's *cash profile*. The
mechanism is real; it is not portable by transcription.

## Honest summary

This generation produced three findings and no promotion.

1. **A mechanism**: Moon's entire advantage is one turn-0 flash trade, confirmed
   by intervention rather than inspection.
2. **A correction**: Moon is our own lineage's offshoot, not an independent
   opponent — and it is legally unsubmittable.
3. **A refutation**: the public Rust simulator exists, but parity is **not**
   established, and 100/100 final-bank agreement would have been a **false pass**.

The champion is unchanged and **is not a rank-1 agent**. No rating is claimed.