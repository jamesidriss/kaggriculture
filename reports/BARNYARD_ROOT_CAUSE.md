# WHY BARNYARD V7 LOSES — root cause, measured

## Hypothesis

Barnyard V7's embedded `_MARKET_PARAMS` predate a Kaggriculture environment
change that replaced the **scarcity side** (`below_func`) of CARROT, TOMATO and
EGG with a `hinge` shape. The recovery champion (The 2945 Farm v9/3) already
embeds the post-change values. If that is the whole story, Barnyard should be
systematically mispricing sales into scarcity.

## Confirmed

Recovery champion's embedded params match the current environment **exactly**:

```python
_R37_MARKET_PARAMS = {
  'CARROT': {..., 'below_func': 'hinge', 'below_target': 1.0, ...},
  'TOMATO': {..., 'below_func': 'hinge', 'below_target': 0.4, ...},
  'EGG':    {..., 'below_func': 'hinge', 'below_target': 0.4, ...},
}
```

Barnyard V7's, from August, do not:

```python
"CARROT": (35, 10000, 450, "log",    0.2, "sqrt", 0.7)
"TOMATO": (60, 10000, 200, "linear", 0.4, "sqrt", 0.6)
"EGG":    (50, 10000, 332, "linear", 0.4, "log",  0.2)
```

## Measured price divergence (scarcity side, inventory below I0=10000)

Computed with the official `market_price` versus Barnyard's embedded model:

### CARROT — catastrophic

| inventory | official env | Barnyard V7 | error |
|---|---|---|---|
| 9900 | $43 | $40 | -7% |
| 9600 | $66 | $42 | **-36%** |
| 9400 | $113 | $42 | **-63%** |
| 9100 | $385 | $43 | **-89%** |
| 8500 | $1,676 | $43 | **-97%** |
| 7000 | $9,259 | $44 | **-99.5% (210×)** |

### TOMATO — catastrophic

| inventory | official env | Barnyard V7 | error |
|---|---|---|---|
| 9700 | $144 | $96 | -33% |
| 9400 | $900 | $132 | -85% |
| 8500 | $8,352 | $240 | **-97% (35×)** |
| 7000 | $38,052 | $420 | **-99% (91×)** |

### EGG — severe

| inventory | official env | Barnyard V7 | error |
|---|---|---|---|
| 9600 | $81 | $74 | -9% |
| 9400 | $190 | $86 | -55% |
| 8500 | $2,121 | $140 | **-93% (15×)** |
| 7000 | $10,563 | $231 | **-98% (46×)** |

## Mechanism

`hinge` is linear below `x = T` and quadratic above:

```
f_hinge(x) = x/T + 8 * max(0, x/T - 1)^2
```

So as a product is consumed below `I0 - T` the price goes **vertical**. Barnyard
models CARROT scarcity as `log`, which is nearly flat — it believes a deeply
scarce carrot is still worth $43 when it is actually worth $9,259.

Consequence for play: a `hinge`-aware agent correctly recognises that dumping
scarce product into a drained market is enormously profitable, and does it
early and aggressively. Barnyard sees almost no price signal, so it neither
tim nor sizes those sales correctly. This is not a small edge — it is a
misread of the single most valuable state in the game.

## Head-to-head evidence

| matchup | games | W | L | win rate | Wilson 95% CI | median cash A | median cash B |
|---|---|---|---|---|---|---|---|
| farm_2945 vs barnyard_v7 (holdout) | 6 | 6 | 0 | **100%** | [0.61, 1.00] | 94,049 | 127,421 |
| barnyard_v7 vs farm_2945 (meta_dev) | 16 | 0 | 16 | **0%** | [0.00, 0.194] | 77,866 | 120,200 |

Combined **0-22 across both seed pools.** The 95% CI upper bound of 19.4% means
even the most Barnyard-favourable reading is a decisive loss.

## Consequence for our choice

This is the single most important finding of the emergency session:

- The **published** scores (Barnyard 3034.8, 2945 Farm 2945) rank Barnyard
  first. That ranking reflects the environment **as it was in August**, when
  Barnyard's `log` model was correct and the recovery champion's `hinge` model
  was not.
- In the **current** environment the ranking **inverts**: the 2945 Farm wins 22
  of 22 local games.
- Trusting published leaderboard scores without verifying against the current
  environment would have led us to deploy the *weaker* agent. This is the
  concrete justification for the "environment is the source of truth" rule.

Barnyard V7 additionally declares **no licence**, so it was not a legal
submission candidate regardless.

## Caveat

Barnyard's higher median cash in the 22 games (127,421 vs 94,049) shows once
more that **cash and win rate diverge** in this game. Barnyard accumulates more
money and loses every match. Promotion criteria must remain win-rate based.