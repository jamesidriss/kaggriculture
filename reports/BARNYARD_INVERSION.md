# BARNYARD INVERSION — how much is staleness, how much is strategy?

## The inversion

Barnyard V7 carries the highest *published* score of any Kaggriculture agent
(3034.8). Under the current environment it is the weakest serious agent in the
league.

## Verified matchup (parity-safe, both seats, real ladder seeds)

Verbatim Barnyard V7 (sha256 `997e6bfc5234534e…`) vs verbatim The 2945 Farm
(sha256 `bfee70e9daaebeae…`), 24 paired games per pool:

| pool | barnyard W-L | win rate | Wilson 95% |
|---|---|---|---|
| REAL_dev | 0-24 | 0% | [0.00, 0.138] |
| REAL_holdout | 0-24 | 0% | [0.00, 0.138] |
| **combined** | **0-72** | **0%** | [0.00, 0.051] |

The previously reported 0-22 reproduces and extends. Observed 0%; the Wilson
lower bound on any true win probability here is 0% and the upper bound is 5.1%.

## Decomposing the loss: staleness vs strategy

Two interventions, each measured against farm_2945 on `REAL_dev`, both seats.

### Intervention 1 — repair the stale price model only

`research/patch_hinge.py` rewrites the three pre-`hinge` scarcity curves and
nothing else: CARROT `log`→`hinge`, TOMATO `linear`→`hinge`, EGG
`linear`→`hinge`. 27,244 bytes in, 27,244 bytes out (three string literals).

| barnyard variant | vs farm_2945 | delta |
|---|---|---|
| verbatim (stale price model) | 0-10 | — |
| price model repaired | **0-10** | **none** |

**Repairing the price model changed nothing.** The score was already 0.

This is the most important finding in the audit. The earlier report presented the
`hinge` mispricing as *the* cause of Barnyard's decline, on the strength of a
table of theoretical prices ($44 vs $9,259 on scarce carrot). The prices were
computed correctly; the causal claim was not tested. Once measured, it is false.

### Intervention 2 — measure the strategy directly

Action-economy forensics, 4 paired games against Multi-Route v43
(`benchmark/action_economy.py`):

| metric | Barnyard (repaired) | farm_2945 |
|---|---|---|
| total field actions | 29,488 | 29,976 |
| production | 7.7% | 10.1% |
| maintenance | 26.7% | 31.8% |
| movement | 39.9% | 38.2% |
| PASS | 22.8% | 15.4% |
| productive/total | **34.4%** | **41.9%** |
| cash per field action | **$5.48** | **$5.58** |
| market orders issued | 10,480 | 3,842 |
| HIRE orders | 4,208 | 1,065 |

Barnyard's **cash per field action is essentially the same** ($5.48 vs $5.58).
It is not failing because it wastes actions. It fails on the small residual:
7.7% vs 10.1% production, 22.8% vs 15.4% PASS, and 34.4% vs 41.9% productive
share. Over 720 turns that is a compounding few-percent disadvantage, and it
never inverts.

Its one clear structural difference is market behaviour: it issues **2.7× more
market orders** (10,480 vs 3,842) and **4× more hires** (4,208 vs 1,065). A
`HIRE` is a market order, so a farm-hand ladder of 4,208 hires across 30 days
means repeatedly rebuilding labour. farm_2945 hires ~1,000 times total.

## Verdict

```
How much of Barnyard's loss is stale price modelling?    ~none measurable
How much is strategy / scheduling / action economy?       the whole of it
```

The `hinge` change is real and still documented
(`research/ENVIRONMENT_CHANGELOG.md`), and a stale price model is a genuine
hazard — but **in Barnyard's case it is not the binding constraint**. Patching
it moved the record by zero games. The binding constraints are its lower
production share, higher PASS rate, and an order-of-magnitude larger hire churn.

## Correction to the previous report

`reports/ENVIRONMENT_CHANGELOG.md` and the earlier `BARNYARD_ROOT_CAUSE.md`
attributed the inversion primarily to the price model, citing price-divergence
tables without running the counterfactual. The counterfactual has now been run
and it refutes that attribution. The changelog's price-divergence measurements
stand; its causal claim is superseded by this report.