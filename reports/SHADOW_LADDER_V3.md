# SHADOW LADDER V3

## Verdict

**WITHHELD.**

No rating is published. No point estimate, no interval, no 3125 target, no
3069.5 claim. The gate inputs were not produced this generation, so the gate
cannot open.

## Publication gate (unchanged, not softened)

| requirement | value | actual | pass |
|---|---|---|---|
| strong exact anchors (class A) | ≥ 5 | **0** | ✗ |
| score span | ≥ 250 pts | **0 pts** | ✗ |
| independent lineages | ≥ 2 | **0** | ✗ |
| leave-one-anchor-out CV | accept | **not runnable** (0 folds) | ✗ |
| no major current-env mismatch | required | **not assessable** | ✗ |

Zero of five legs pass. Two of them are not merely unmet but **undefined**: with
0 anchors there is no CV and no span to compute.

## What V3 does *not* do

This generation produced one genuinely new strategic fact — Moon's mechanism —
and it is tempting to reach for a number because we finally understand something.
That is precisely the failure mode this ladder exists to prevent.

**A mechanism finding is not a calibration finding.** Knowing *why* an agent wins
tells you nothing about where its rating sits on Kaggle's scale. There is no
mapping from "BT 0.92 vs C001 on our dev seeds" to "3069.5" that this project is
permitted to assert.

## Rating status

```
estimated final strength : WITHHELD
uncertainty              : WITHHELD
internal safety target   : 3125  — UNTESTABLE, no calibration exists
RANK-1 READY             : NO
```

## What would change the verdict

Reproduce, in order:

1. **Anchor ladder** — ≥5 class-A exact-version anchors, ≥250-point span, ≥2
   independent lineages (`reports/ANCHOR_BINDING.md`).
2. **Re-evaluate each anchor under the current environment** — a historical rating
   is contextual; anchors must be re-measored against C001, Moon, Farm and v51
   on today's engine.
3. **Leave-one-anchor-out CV** — report MAE, median absolute error, Spearman, and
   interval coverage. If prediction error is ~100+ points, then a claim of
   precision near 3069 is unavailable regardless of how many anchors exist.
4. Only then: point estimate ≥ 3125 **and** lower 95% bound > 3069.5.

If calibration never becomes adequate, the honest permanent answer is
`WITHHELD`, and the strongest defensible statement remains relative:

> stronger than all legally reproduced public references actually tested

which this generation has **not** established either — no candidate beat C001, and
C001 loses 94.6% to a publicly obtainable artifact.