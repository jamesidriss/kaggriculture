# MOON DIFF — structural comparison, ranked by measured causal importance

Companion to `reports/MOON_AUTOPSY.md`. The autopsy measures *what* Moon does;
this file records *how it differs structurally* from our champion, and — critically
— marks which differences are **dead** in the runtime configuration.

## Structural facts

Moon is a **43-deep wrapper chain**. Every layer binds the previous callable:

```python
_X_PARENT = agent          # bind current
def agent(obs, cfg=None):  # and extend it
    ...
    return _X_PARENT(obs, cfg)
```

A chain this deep has a property that cost this project a full run and a
published wrong answer: **appending a redefinition after the module body changes
nothing that executes.** The chain already captured the original function object.
Any ablation written that way measures nothing, and if it happens to break the
program it will report as a dramatic result. `policy/rank1/moon_ablation2.py`
intervenes at the `def` site instead.

## Layer inventory and measured status

Identified from the v9 header and the wrapper chain; **status is from
intervention, not from reading**:

| layer | identifier | measured effect on BT vs C001 | status |
|---|---|---|---|
| **v9 OPENING** | `_v9_opening` | 0.8667 → **0.0000** | **LIVE — the mechanism** |
| COURIER | `_V9_COURIER_PARENT` | 0.8667 → 0.8000 | live, partial (−0.067) |
| RACE | `_v9_race_update` | 0.8667 → 0.8667 | **INERT** |
| RACE tape search | `_v9_planned_sells` | 0.8667 → 0.8667 | **INERT** |
| RACEPX | `_V9_RACEPX_PARENT` | — | **INERT** (no reachable def site) |
| CARROT | `_V9_CARROT_PARENT` | 0.8667 → 0.8667 | **INERT** |
| HERD | `_V9_HERD_PARENT` | 0.8667 → 0.8667 | **INERT** |

**Five of seven named layers are dead code in this artifact.** The header
advertises RACEPX, RACE, COURIER, CARROT and HERD; four of them do nothing.

## The one live mechanism

```python
V9_OPENING_STEP0 = (("BUY_PRODUCT", "WHEAT", 20), ("SELL", "WHEAT", 15))
```

At **turn 0 only**, prepended to Moon's own market orders. Market orders settle
**index by index in lockstep within a step**, so the `SELL` observes the
post-`BUY` state, and at turn 0 no rival has acted and none can interleave. It is
a one-sided flash round-trip on a shared market, committed before any
observation.

## Why identifier analysis alone could not have found this

| method | verdict on OPENING | why |
|---|---|---|
| identifier Jaccard | "Moon is 72% the same as C001" | measures shared vocabulary, not behaviour |
| code size / layer count | "43 layers, enormously complex" | five layers are inert |
| header claims | "RACEPX + RACE + COURIER + CARROT + HERD" | four of the five are dead |
| **intervention** | **OPENING, and nothing else** | the only method that can |

This is the third time in this project's history that code inspection produced a
confident wrong answer and only an intervention produced a right one.

## C001 differences that matter

C001's `_SETTINGS` literal is **9 booleans and 0 numeric keys**; numeric tunables
exist only in dead `DEFAULT_SETTINGS`. C001 therefore has **no route-table,
market-timing, or numeric-parameter layer** comparable to Moon's machinery. The
structural gap is not "Moon has better constants" — it is that **C001 has no
market-microstructure layer at all**.

That is the gap the transplant experiment probed, and it failed for a specific
and instructive reason: see `reports/RANK1_RESEARCH_CONCLUSION.md` §7.