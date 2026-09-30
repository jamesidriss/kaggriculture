# Kaggriculture — CURRENT META MAP

Compiled 2026-09-30 from the official environment source, the competition
README/AGENTS docs shipped inside `kaggle-environments` 1.32.7, and the live
leaderboard. Search-by-recency caveat: the competition is 6 weeks old and the
public discussion surface was thin at sprint time, so the meta below is derived
primarily from the **price function design**, which is where the competition
actually is.

## Leaderboard snapshot (2026-09-30 19:07 UTC)

| Rank | Team | Score |
|---|---|---|
| 1 | M & M & P & Q | 3053.1 |
| 2 | Victor @ Tufa Labs | 2969.9 |
| 3 | DECEM | 2951.9 |
| 4 | DSM | 2918.4 |
| 5 | CDE | 2890.3 |
| 6 | Unknown Mother-Goose | 2878.8 |
| 7 | Vadim Vasilenko | 2854.7 |
| 8 | Gemini IS ALL YOU NEED | 2853.9 |
| 9 | TKNP | 2844.9 |

10222 teams entered. The top ten sit within ~210 points, which is a very tight
band — consistent with a game where one clean economic insight separates agents
and everything after that is noise.

## The dominant insight: glut curves are the whole game

Every product has an asymmetric price curve around `I0 = 10,000`, and the shape
function differs **per side** of equilibrium. Measured with the agent's exact
replica of the official function:

| Product | glut curve | behaviour under volume |
|---|---|---|
| WHEAT | `log`, target 0.20 | **$19 after 2,000 units dumped.** Effectively unlimited. |
| EGG | `log`, target 0.20 | **$39 after 500 units.** Effectively unlimited. |
| FERTILIZER | `linear`, target 0.40 | gentle, two-sided |
| CARROT | `sqrt`, target 0.70 | floors around 900 units |
| TOMATO | `sqrt`, target 0.60 | floors around 500 units |
| STRAWBERRY | `linear`, target 1.60 | floors around 60 units |
| MILK | `linear`, target 1.60 | floors around **75 units** |
| WOOL | `sq`, target 3.20 | floors around **59 units** |
| MELON | `sq`, target 3.60 | floors around **160 units** |

Two conclusions drive every serious agent:

1. **Wheat is the only truly scalable crop.** It is the correct backbone because
   volume does not destroy its price. Every strong farm is a wheat treadmill.
2. **The premium goods are finite pots, not scalable products.** Melon's *entire
   season* is worth about **$24.4k** — the integral of its price curve. Selling
   it all at once yields roughly half that. The skill that separates agents is
   **selling in tranches that hold the unit price up**, which requires modelling
   the price function locally rather than dumping on a schedule.

Town demand matters here: the town centre drains 1 of every product daily and
shops drain more every 4 turns, so price partially recovers and waiting has real
option value — but only for goods with a town sink.

## Notable structural traps

- **MELON has no shop demand.** No shop in `SHOPS` consumes melon, so its only
  town sink is the flat 1/day at the centre. Melon volume beyond ~160 units is
  near-worthless. It is a high-margin, low-volume crop, not a scale crop, and
  treating it as one is the most common way to waste a season.
- **MILK and WOOL have tiny season pots** (75 and 59 units). Each cow is $400 and
  eats a tile plus a daily FEED action to contribute to a few-thousand-dollar
  ceiling. Large cow/sheep herds are almost certainly a losing allocation.
- **Fertilizer is a trap.** It sells at a fixed $100 and buying drains inventory
  (price rises above $100). The yield bonus on a 4-day wheat cycle is worth about
  $38 of extra product. Net negative, plus it burns a field action.
- **Shed capacity is 100 with no overflow holding area.** Overflow at end-of-day
  drop is destroyed outright, and unit inventories do *not* bypass the cap. An
  agent that harvests faster than it sells loses production silently.

## Action economy

Only field actions cost a worker turn; market orders are free up to 10/turn. A
wheat tile needs ~1.5 actions/day (plant, water, bonus waterings, harvest), so 25
tiles need ~2 workers and 100 tiles need ~7. The `fib(n)` hand ladder
(1,1,2,3,5,8,13,21,34,55,89,144...) makes 12 hands cost $376/day and 14 hands
$987/day — cheap early, ruinous late. The binding constraint on a strong farm is
**action throughput and cash discipline, not land**.

## Winning agent shape (inferred)

1. Wheat treadmill on every workable tile, watered on the bonus window.
2. Melon tranche programme on ~14 tiles, sold to hold price.
3. Land bought only out of surplus ($1k/$2k/$4k, payback ~2 days per quadrant,
   but only if there are hands to work it).
4. Hands scaled to land, never to cash.
5. Geese if and only if the action budget has slack — $50/egg on a `log` curve is
   genuinely scalable in a way milk and wool are not.
6. Zero stranded inventory at step 720.

## Sources

- Official rules: `research/README.md`, `research/AGENTS.md` (byte-identical to
  the copies in `kaggle-environments` 1.32.7).
- Environment mechanics and all price parameters:
  `.venv/.../envs/kaggriculture/kaggriculture.py`.
- Live leaderboard: `kaggle competitions leaderboard kaggriculture -s`.
- Local verification of every price claim above: `benchmark/` harness.