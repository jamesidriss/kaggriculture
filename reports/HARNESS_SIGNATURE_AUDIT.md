# HARNESS SIGNATURE AUDIT — corrected

**The v1 conclusion published here was wrong about Kaggle and has been
retracted. See `reports/RETRACTIONS.md` R1 for the full correction. This file is
the corrected version and the correction is kept, not buried.**

## The claim that was retracted

> "Kaggle invokes agents as `agent(obs, configuration)`. Many public agents
> define `def agent(obs)`, so passing the raw function raises `TypeError` on
> every turn, the agent is marked `INVALID`, it never acts, and it finishes on
> the starting $3,000."

The Kaggle half of that is **false**.

## What the official runtime actually does

`kaggle_environments/agent.py`, `Agent.act` (kaggle-environments 1.32.7):

```python
args = [structify(observation), structify(self.configuration)]

if hasattr(self.agent, "__code__") and hasattr(self.agent.__code__, "co_argcount"):
    args = args[: self.agent.__code__.co_argcount]
...
action = self.agent(*args)
```

and `build_agent` passes a callable through untouched:

```python
# Already callable.
if callable(raw):
    return raw, False
```

So the argument list is truncated to the callable's own positional arity.
**Both `agent(obs)` and `agent(obs, configuration)` are valid**, and an
agent object with `__call__` is passed through as well.

Machine-readable snapshot: `benchmark/kaggle_call_convention.json`.

## Proof by execution

`benchmark/call_convention.py` runs a real `env.run([raw_callable, starter])`:

| agent | `co_argcount` | invoked | seat status | worked |
|---|---|---|---|---|
| `def agent(obs)` | 1 | 29 | DONE | yes |
| `def agent(obs, configuration=None)` | 2 | 29 | DONE | yes |
| `def agent(obs, configuration)` | 2 | 29 | DONE | yes |

## The real root cause

**Our own diagnostic scripts invoked agents directly**, bypassing the
framework's dispatcher:

```python
# wrong, and this is what produced the TypeError
action = agent_fn(obs, configuration)
```

Files that did this: `benchmark/close_games.py`, `benchmark/endgame.py`,
`benchmark/forensic.py`, and the first cut of `simcomp/league.py`. They are
diagnostics; none of them decides a competitive result.

The competitive harness `benchmark/meta.py` passed the **raw callable** to
`env.run`, which is the correct path, and was therefore never affected.

## Verification that no competitive number was wrong

`benchmark/isolate_signature_bug.py` runs four matchups three ways — raw
callable into `env.run`, a 2-argument wrapper into `env.run`, and direct
invocation — and separately replays the **pre-fix** `benchmark/meta.py` from
commit `c8fb403`:

| matchup, seed 62857979 | old `meta.py` (raw) | current (adapter) | |
|---|---|---|---|
| sunrise vs v16_rc5 | 6400 vs 112314 | 6400 vs 112314 | identical |
| v51 vs v16_rc5 | 93336 vs 69182 | 93336 vs 69182 | identical |
| v51 vs barnyard_v7 | 113694 vs 78471 | 113694 vs 78471 | identical |
| v51 vs farm_2945 | 85013 vs 84461 | 85013 vs 84461 | identical |

All three invocation paths agree. The "silent agent failure" class of bug is
real and worth guarding against, but it did not affect the competitive results
of this project.

## Which agent actually was inert

One: **`shop_router`** (yhay81). It is **not self-contained** —

```
FileNotFoundError: [Errno 2] No such file or directory: '...actions.json'
```

— on its first turn, and that data file is not present in the public notebook.
It is withheld to `opponents/unlicensed/` and recorded as `NOT_SELF_CONTAINED`
in the manifest. Before the playability probe existed it sat at $3,000 and was
scored as a 24-0 victim, which is the failure mode the probe now prevents.

## The canonical loader

`benchmark/agent_loader.py` is the single loader. It:

- adapts the signature so diagnostics can call uniformly **without diverging
  from the official runner**;
- never alters strategy — the action is forwarded unchanged;
- preserves `__wrapped__`, `__kag_path__`, `__kag_sha__` and the source name;
- is used by `benchmark/tournament.py`, `benchmark/round_robin.py`,
  `benchmark/forensics_final.py` and `benchmark/agent_loader.py --probe-all`.

## The playability probe

`benchmark/agent_loader.py --probe-all` must pass before an agent may enter a
league. It deliberately does **not** use "final cash > 3000" as the test,
because an agent can legitimately lose money. The evidence is behavioural:

| criterion | why |
|---|---|
| module imports, `agent` is callable | catches a broken artifact |
| invoked ~719 times per episode | catches a non-playing seat |
| seat status `DONE` (never INVALID/ERROR/TIMEOUT) | catches framework rejection |
| a non-trivial action trace, not 719 `PASS` | catches an idle agent |
| market orders issued > 0 | catches an agent that never enters the economy |
| works from **both** seats | catches seat-dependent code |
| final cash changes over the episode | catches a frozen farm |

Current result: **11/11 league agents playable**, e.g.

```
v51                       two_arg=True   turns=719  active=357  mkt=905  $182,861
barnyard_v7               two_arg=False  turns=719  active=319  mkt=635  $167,711
v16_rc5                   two_arg=False  turns=719  active=436  mkt=626  $138,247
```

Note `two_arg=False` is fine and is now understood: it only means the agent
declares one parameter, which Kaggle handles by truncation.

## Why this matters beyond one report

The generalisable lesson is not "one-arg agents are special". It is:

> A harness bug and a product bug look identical from the inside, and both
> look like a *result*. The only defence is to assert on the side effects the
> agent produces — invocations, exceptions, status, action trace, final bank —
> rather than on the absence of an error code.

That is now enforced by `benchmark/agent_loader.py --probe-all` and by
`tests/test_audit_regressions.py`.
