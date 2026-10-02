# HARNESS SIGNATURE AUDIT — the second harness bug, and the worst of the run

This is the most damaging finding of the audit. It invalidated results that had
already been written up, including a headline postmortem.

## The bug

Kaggle invokes an agent as:

```python
agent(observation, configuration)
```

A large share of public Kaggriculture agents define the one-argument form:

```python
def agent(obs):
    ...
```

`benchmark/meta.py` passed the raw module attribute straight to `env.run()`:

```python
spec.loader.exec_module(mod)
_cache[path] = mod.agent          # raw, unadapted
...
env.run([a0, a1])                 # Kaggle calls it with TWO positional args
```

For a one-argument agent that is a `TypeError` on **every single turn**:

```
TypeError: agent() takes 1 positional argument but 2 were given
```

Kaggle catches the exception, marks the agent `INVALID`, and the game continues
with that seat inert. The agent never acts. It ends the 720-turn season on the
starting bank: **exactly $3,000, every game.**

## Why it was invisible

A non-playing agent is the *easiest possible opponent*. It loses 100% of games
with a huge cash margin. The harness dutifully recorded:

```
{"label": "vs barnyard_v7", "games": 24, "errors": 0, "W": 24, "L": 0}
```

- `errors: 0` — because no exception propagated out of `env.run()`; the
  framework had already absorbed it.
- `W: 24` — the candidate beat a seat that never moved.
- The `mean_opp: 3000` field was present in the JSON and nobody read it.

The self-play guard did not fire (the content differed), the digest guard did
not fire (the content differed), the Wilson interval dutifully reported
`[0.862, 1.000]` for a 24-0 against a corpse, and the invariant suite passed.

## Who was actually never playing

| agent | signature | real strength | recorded as |
|---|---|---|---|
| `barnyard_v7` | `agent(obs)` | ~$74k final cash, plays 719 turns | 0-72 victim, "score inversion" |
| `v16_rc5` | `agent(obs)` | **$138,247** vs `starter` | 0-72 victim |
| `main.py` = **sunrise-v5** | `agent(obs)` | our own submission | 0-264 per pool |
| 9 other league agents | `agent(obs, config)` | fine | fine |

Detection, in one line per agent:

```
v16_rc5                     two_arg=False
barnyard_v7                 two_arg=False
shop_router                 two_arg=True
ahmedberatozer-v51-lean-flock  two_arg=True
```

`main.py`, `champions/champion_000/main.py` (sunrise-v4) and
`champions/champion_001/main.py` (sunrise-v5) are all one-argument.

**Our own submitted agents were never evaluated.** Every sunrise number in the
pre-existing reports — the 72-792 record, and the 792-game aggregate — was a
measurement of a non-player.

## The fix

`benchmark/meta.py::load` now introspects the signature and returns a uniform
wrapper:

```python
sig = inspect.signature(fn)
npos = sum(1 for p in sig.parameters.values()
           if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD))
has_var = any(p.kind == p.VAR_POSITIONAL for p in sig.parameters.values())
two_arg = has_var or npos >= 2

def wrapper(obs, configuration=None, _fn=fn, _two=two_arg, _src=...):
    st = _stats.setdefault(_src, {"calls": 0, "errors": []})
    st["calls"] += 1
    try:
        return _fn(obs, configuration) if _two else _fn(obs)
    except Exception as exc:
        st["errors"].append(f"turn {st['calls']}: {type(exc).__name__}: {exc}")
        raise
```

and `head_to_head` refuses to score a game in which either side did not
actually play:

```python
if st["calls"] == 0 and "error" not in r:
    r["error"] = f"{src} was never invoked (0 turns) -- the result would be a fabrication"
elif st["errors"] and "error" not in r:
    r["error"] = f"{src} raised: {st['errors'][0][:140]}"
```

Every result row now carries `candidate_turns` and `opponent_turns`, so a
non-player is visible in the data rather than inferred. All 720 recorded games
show 719/719.

The same bug existed in the new `simcomp` framework and was caught by its own
self-test within minutes of being written — which is the argument for having
the guard at all.

## What the guard then caught

`shop_router` (yhay81) raises on its first turn:

```
FileNotFoundError: [Errno 2] No such file or directory:
  'opponents\meta\actions.json'
```

It needs a data file that is not present in the public notebook. It is **not a
self-contained artifact** and therefore not a legal single-file submission. It
had also been sitting at $3,000 and being recorded as a 72-0 victim. It is
withheld to `opponents/unlicensed/` and the reason is recorded in
`opponents/meta/MANIFEST.csv`.

## Corrected records

All re-run on the corrected harness: real ladder seeds, 12 per pool, both seats,
official `Environment.run`, 0 errors.

| agent | W-L-T | games | win% | Wilson 95% |
|---|---|---|---|---|
| `ahmedberatozer-v51-lean-flock` | **670-50-0** | 720 | 93.06% | [0.9096, 0.9469] |
| `farm_2945_original` | 596-124-0 | 720 | 82.78% | [0.7985, 0.8536] |
| `sunrise` (v5) | **0-792-0** | 792 | 0.00% | [0.0000, 0.0048] |

Per pool:

| agent | dev | holdout | final (sealed) |
|---|---|---|---|
| v51 | 224-16 | 214-26 | 232-8 |
| farm_2945 | 194-46 | 210-30 | 192-48 |
| sunrise-v5 | 0-264 | 0-264 | 0-264 |

Head-to-heads that survive correction, with intervals:

| matchup | record | n | win% | Wilson 95% | verdict |
|---|---|---|---|---|---|
| v51 vs farm_2945 | 76-68 | 144 | 52.78% | [0.3925, 0.5534] | **not separable from 50%** |
| v49 vs farm_2945 | 38-34 | 72 | 52.78% | [0.4140, 0.6387] | not separable from 50% |
| v50 vs farm_2945 | 38-34 | 72 | 52.78% | [0.4140, 0.6387] | not separable from 50% |
| v51 vs v49/v50 | 64-8 | 72 | 88.89% | [0.7958, 0.9494] | decisive |
| v51 vs v43/v44/v46/v48 | 72-0 | 72 | 100% | [0.9493, 1.0000] | decisive |
| v51 vs barnyard_v7 | 72-0 | 72 | 100% | [0.9493, 1.0000] | decisive |
| v51 vs v16_rc5 | 72-0 | 72 | 100% | [0.9493, 1.0000] | decisive |
| anyone vs sunrise | 792-0 | 792 | 100% | [0.0000, 0.0048] | decisive |

## Conclusions that changed

**Sunrise's failure is real and worse than reported.** 0 for 792, Wilson upper
bound 0.48%. It is not merely weak; it never beat any of ten distinct public
agents in either seat on any real ladder world.

**The Barnyard score inversion is real, but its explanation was void.**
Barnyard genuinely loses 0-72 to v51 and 0-72 to farm_2945 while scoring ~$74k.
But the previous report's causal test — patch the stale `hinge` price table,
re-run, observe no change — was executed while Barnyard was not playing. It has
been redone; see `reports/BARNYARD_INVERSION.md`.

**`v16_rc5` is a genuine agent, not a corpse.** It reaches $138,247 against
`starter` and ~$81k against the top agents. It loses, but it is a real opponent
and its 0-72 is informative.

**`v51` over `farm_2945` is NOT established.** 76-68 over 144 paired games,
Wilson [0.3925, 0.5534]. v51 is the better pick on aggregate (93.06% vs 82.78%
and a decisive 64-8 over v49/v50 where farm is 38-34), but the head-to-head is
a coin flip and must not be reported as a win.

## Regression coverage

`tests/test_audit_regressions.py` — 26/26 pass, including three new checks:

- every league agent imports and is wrapped in a 2-arg callable (`11/11`)
- no scored game has a side frozen at $3,000
- `meta.py`, `validate_artifact.py`, `close_games.py` never feed agents from
  persisted snapshots

## The lesson

Two separate harness bugs in one audit, both producing confident false
conclusions, both invisible to every existing guard:

| bug | false conclusion | why no guard caught it |
|---|---|---|
| feeding agents `env.steps[i][1].observation` | "the agent crashes in seat 1" | the `KeyError` looked like a product bug |
| passing a 1-arg `agent` to `env.run` | "the opponent is 0-72" | the exception was absorbed by the framework |

Both were found by **asking what the harness actually did** rather than what it
reported. The durable protections are: drive agents through the environment's
own entry point, adapt the call signature, and assert on the *side effects*
(invocations, exceptions, final bank) rather than on the absence of an error
code.
