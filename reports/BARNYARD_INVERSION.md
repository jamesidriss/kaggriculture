# BARNYARD INVERSION — how much is staleness, how much is strategy

Supersedes the previous version, whose counterfactual was executed while
Barnyard was not actually playing (see `reports/HARNESS_SIGNATURE_AUDIT.md`).
Everything below is re-measured on the corrected harness.

## The inversion> **Correction (final pass).** This report originally rested on a
> counterfactual executed while Barnyard was believed not to be playing. That
> belief was wrong (`reports/RETRACTIONS.md` R1): Barnyard always played, and the
> 0-144 record below is genuine. The counterfactual has been re-run on the
> canonical harness and the conclusion is unchanged — the patched agent
> finishes at **$74,991, identical to the dollar across 24 games** — but it is
> now measured rather than carried forward. Barnyard is also ineligible as a
> redistributable champion because the author declared no licence.



Barnyard V7 carries the highest *published* score of any Kaggriculture agent
(3034.8). Under the current environment it is the weakest serious agent in the
league, and it genuinely plays.

## Verified matchup (corrected harness, both seats, real ladder seeds)

Verbatim Barnyard V7 (`997e6bfc5234534e…`), 719 turns per game, 0 errors:

| pool | opponent | barnyard W-L | barnyard mean cash | opponent mean cash |
|---|---|---|---|---|
| REAL_dev | v51 | 0-24 | $74,453 | $97,412 |
| REAL_dev | farm_2945 | 0-24 | $74,991 | $122,165 |
| all pools | v51 | **0-72** | ~$74k | ~$99k |
| all pools | farm_2945 | **0-72** | ~$74k | ~$110k |

Combined **0-144**, observed win rate 0%, Wilson 95% [0.0000, 0.0265].

The inversion is real. Barnyard ends the season with roughly **$74,000** while
the top agents finish near **$99,000-$122,000**.

## Decomposition: is the stale price model the cause?

### The intervention

`research/patch_hinge.py` rewrites the three pre-`hinge` scarcity curves and
nothing else — CARROT `log`→`hinge`, TOMATO `linear`→`hinge`, EGG
`linear`→`hinge`. 27,244 bytes in, 27,244 bytes out; three string literals.

Artifact: `counterfactuals/barnyard_v7_pricefixed.py`.

### The result

| variant | vs farm_2945 (REAL_dev) | mean cash |
|---|---|---|
| verbatim | 0-24 | $74,991 |
| price model repaired | **0-24** | **$74,991** |

**Identical to the dollar, across all 24 games.**

### Why the patch changes nothing: the table is dead code

`opponents/meta/barnyard_v7.py` lines 250 and 266-267:

```python
prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
...
base_price = float(_MARKET_PARAMS[item][0])
current_price = float(_get(prices, item, 0) or 0)
```

The agent reads the **live** price out of `observation.market.prices`. The
`_MARKET_PARAMS` table — the thing the previous session identified as the cause
of the collapse — is consulted only as a fallback for a field the environment
always supplies. It is never reached in any of the 144 games.

So the previous causal claim was doubly wrong:

1. It was measured against an agent that was not playing.
2. Even if it had been playing, the table it patched is unreachable.

## What actually explains the gap

Action-economy forensics (`benchmark/action_economy.py`, 4 paired games,
corrected harness). These were re-measured after the signature fix:

| metric | champion (v51) | farm_2945 | Barnyard V7 |
|---|---|---|---|
| total field actions | 29,955 | 29,976 | 29,488 |
| production | 10.1% | 10.1% | **7.7%** |
| maintenance | 31.8% | 31.8% | 26.7% |
| movement | 38.4% | 38.2% | 39.9% |
| PASS | 15.1% | 15.4% | **22.8%** |
| **productive / total** | **41.9%** | **41.9%** | **34.4%** |
| **cash per field action** | **$5.64** | $5.58 | $5.48 |
| SELL orders (4 games) | 1,450 | 5,073 | 2,944 |
| HIRE orders | 1,064 | 3,195 | **4,208** |
| hands mean / max | 8.6 / 12 | 8.6 / 12 | 9.5 / 14 |
| production share, days 24-29 | 13% | 13% | **10%** |

Barnyard's **cash per field action is $5.48 against the champion's $5.64** — a
2.8% deficit, not a collapse. It is not catastrophically inefficient. It is
*marginally* behind, and the margin compounds over 720 turns:

- production share 7.7% vs 10.1%
- PASS rate 22.8% vs 15.1%
- productive share 34.4% vs 41.9%
- endgame production share 10% vs 13%

Its one large structural difference is labour churn: **4,208 HIRE orders**
against the champion's 1,064 — 4× as many, reaching 14 hands against 12. A
`HIRE` is a market order, so that is a farm-hand ladder being repeatedly rebuilt
rather than retained, each rebuild spending cash that does not reach the field.

## Verdict

```
Is the inversion real?                                    YES - 0-144, both seats
Is the stale price model the cause?                       NO - it is unreachable code
                                                          and patching it moved the
                                                          result by exactly 0 games
                                                          and $0
What is the cause?                                        a compounding ~2-3% action
                                                          efficiency deficit plus 4x
                                                          hire churn, concentrated in
                                                          production share, PASS rate
                                                          and the endgame
```

The `hinge` change is a real environment fact and remains documented in
`reports/ENVIRONMENT_CHANGELOG.md`; a stale price model is a genuine hazard in
general. But in Barnyard's case it is not the binding constraint and never was.
The binding constraint is that it does slightly less with each of the same
~29,500 actions, and it spends four times as much rebuilding its labour force.

## Correction to the earlier attribution

`reports/ENVIRONMENT_CHANGELOG.md` and the earlier root-cause write-up
attributed the inversion to the price model, citing a table of theoretical
prices (scarce carrot: environment $9,259 vs the agent's $44) without running a
counterfactual. The price measurements themselves are correct. The causal claim
is superseded by this report.
