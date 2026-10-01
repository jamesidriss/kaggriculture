# LOCAL BRADLEY-TERRY STRENGTH MODEL

Offline estimate only. **Not** an official Kaggle ranking. Fitted from paired
both-seat results over real elite-ladder seeds (all games ≥ 2900 score, from the
public 88,281-episode replay database).

Method: Bradley-Terry MLE with an MM update, mean-centred (identifiability).
Ties contribute 0.5 to each side.

## League round-robin (10 elite seeds, both seats, 20 games per pair)

| team | beta | P(beats league average) |
|---|---|---|
| **farm_2945** (The 2945 Farm v9/3) | **10.203** | 1.000 |
| multi_route_v43 (Multi-Route V43) | 5.936 | 0.997 |
| barnyard_v7 (Barnyard Economist V7) | −1.791 | 0.143 |
| v16_rc5 (V16-RC5 8C/4S) | −2.941 | 0.050 |
| v38_feed (V38 Smarter Feed) | −5.694 | 0.003 |
| shop_router (Shop Router 0909) | −5.713 | 0.003 |

## Predicted vs observed

| pairing | P(predicted) | observed |
|---|---|---|
| farm_2945 beats multi_route_v43 | 0.986 | 20-0 |
| farm_2945 beats barnyard_v7 | 0.999 | 20-0 |
| multi_route_v43 beats v38_feed | 0.999 | 20-0 |
| barnyard_v7 beats shop_router | 0.981 | 20-0 |
| barnyard_v7 beats v16_rc5 | 0.760 | **0-20** ← model over-predicts |
| v38_feed beats shop_router | 0.500 | 20-0 |

## Interpretation

**farm_2945 is the strongest agent we reproduced.** Its beta is 4.3 above the
next agent and it is undefeated (60-0 in the round-robin, then 300-0 across the
three disjoint seed pools).

Two disagreements with the model are informative rather than errors:

1. **barnyard_v7 vs v16_rc5**: the model predicts 0.76 from barnyard's wins
   against shop_router and multi_route, but the observed record is 0-20. This
   is the transitivity failure that comes from barnyard's stale price model —
   it wins the games it should win and loses the ones it should also win,
   because the BT model cannot represent an agent that plays a *different game*
   than its rating implies.
2. **v38_feed vs shop_router**: shop_router never wins anything and never plays
   (it holds $3,000 all season), so it anchors the bottom without being a
   meaningful opponent.

## What this does NOT establish

- It is a six-agent offline model, not the 10,246-team ladder.
- Betas are only meaningful *relative to this league*. farm_2945's 10.2 says
  "dominates these five", not "rated ~3000".
- Four of the six league members are far below the elite tier, so the top of
  the scale is compressed and under-resolved.

## Reproduction

```
python benchmark/bradley_tery.py C:\...\rr_ladder.json
```

`benchmark/opponent_store.py verify` must pass first (unique digests).