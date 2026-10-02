# CHALLENGER RESULTS — NONE PROMOTED

## Outcome

**No challenger is promoted. The references stand.**

## What was built

The reference agent declares `DEFAULT_SETTINGS` with most layers enabled, but
it is actually constructed as

```python
_IMPL = make_agent(_ROUTES, router=_router, **_SETTINGS)      # line 968
```

and `Planner.__init__` does `self.cfg = dict(DEFAULT_SETTINGS)` then
`self.cfg.update(settings)`. **`_SETTINGS` wins.** The live configuration is a
reduced one:

```
hand_align True   weed_repair True   sell_lead True
budget_guard False   room_guard False   clamp_sells False
dead_stock False     terminal_liquidation False   front_run False
```

The first attempt edited `DEFAULT_SETTINGS`. All four "challengers" then
produced **byte-identical cash and action traces to the parent**, which is the
only reason the error was caught: a challenger that behaves exactly like its
parent is a no-op, and reporting it as a tie would have been nonsense.

Three real single-variable challengers were then built by editing `_SETTINGS`,
each verified to occur exactly once:

| tag | change | sha256 | cash vs starter | market orders | verdict |
|---|---|---|---|---|---|
| parent | — | `c1e3590d…` | $182,861 | 905 | reference |
| challenger_001 | `sell_lead` True→False | `2d5d98c9…` | **$182,746** | 911 | worse |
| challenger_002 | `terminal_liquidation` False→True | `f5c254f9…` | **$182,861** | 905 | **no-op** |
| challenger_003 | `clamp_sells` False→True | `259fb772…` | **$182,627** | 870 | worse |

## Findings

1. **The agent is already at a local optimum on its own levers.** Two of the
   three single-variable changes reduce final cash; none increases it. The
   layers it runs (`hand_align`, `weed_repair`, `sell_lead`) are the ones that
   pay, and the three it has switched off are not free wins waiting to be taken.

2. **`terminal_liquidation` is inert.** Enabling it changes nothing at all:
   identical cash, identical action trace, identical market-order count. The
   flag is present in the configuration and the code path is written, but it
   never fires. This is the same failure shape as Barnyard's price table — a
   documented mechanism that is not on the executed path. The end-of-season
   liquidation hypothesis is therefore **NO_GO on this agent**, not because it
   was tested and failed, but because the mechanism does not exist at runtime.

3. **The screening sample was far too small, and that is the real finding.**
   The paired screen produced **12 valid games** across six matchups. At a 2-point
   true effect, detecting it needs on the order of a thousand games, as the
   v51-vs-Farm experiment itself demonstrates: 144 games produced a "tie" and
   1,984 produced p = 0.0368. Twelve games cannot distinguish a challenger from
   its parent, and no promotion is claimed on that basis.

## Why no promotion is defensible either way

The promotion gate requires improvement against **both** top agents. With 12
games the intervals are roughly [0.00, 0.66] — uninformative. Granting a
promotion on that evidence, or refusing one, would both be arbitrary. The
honest state is **inconclusive by sample size**, with the one exception of
challenger_002, which is not a challenger at all because it is a no-op.

The cash figures in the table above come from a single 720-turn game each
against `starter` and are reported as a *direction*, not as a result.

## What a real challenger would require

The remaining margin is about two points of win rate and $28 of mean cash
difference. Three things would be needed to attack it, none of which is a
one-line edit to a 460 KB published artifact:

1. **A market-order model.** `sell_lead` is a one-turn lead. The environment
   has a shared market with scarcity-driven prices, and the winning move is
   almost certainly to model the joint sell queue rather than to lead or trail
   it. That is a new subsystem, not a flag.
2. **A genuine opponent model.** `front_run` has a hook for the opponent's
   planned actions and the hook is unpopulated. Populating it from the public
   observation is a real, evidence-backed idea (3.1% of worlds flip with the
   seat, so the world matters), but it is a feature, not a flag flip.
3. **A 1,000+ game paired evaluation per candidate.** At this effect size,
   screening is not measurement.

The honest summary is in `reports/FINAL_RESEARCH_CONCLUSION.md` §10: the
strongest reproducible public agent is v51, and no evidence gathered here shows
a better one is reachable by surgical modification.

## Artifacts

- `challengers/challengers.json` — machine-readable index
- `challengers/challenger_00{1,2,3}.md` — one file per hypothesis, with the
  measured result
- `challengers/challenger_00*_*.py` — the exact single-variable artifacts
- `experiments/chal/*.csv` — the (small) screening rows
- `benchmark/build_challengers.py` — reproducible construction, with the parent
  digest asserted before any edit
