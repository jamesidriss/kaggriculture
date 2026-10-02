# KAGGLE RUNTIME OBSERVATION PARITY

## Question

**Is `observation["step"]` available to player 1?**

## Answer

**YES.** The previous session's claim to the contrary is **RETRACTED**.

The artifact that would have been submitted, The 2945 Farm v9/3, runs in **both
seats** under the real Kaggle execution path, unmodified.

---

## Phase A evidence

Environment under test:

```
python                 3.11.9
kaggle-environments    1.32.7
location               C:\Users\James\kaggriculture\.venv\Lib\site-packages\kaggle_environments
Kaggriculture env      kaggriculture (episodeSteps 720, turnsPerDay 24)
```

### Probe 1 — real `env.run()` with two instrumented agents

`tools/probe_observations.py`. Two probe agents record only `player`, `step`,
`day`, `hour` and the delivered keys, for 6 turns of a real game.

```
delivered observation keys, first turn
  seat 0: step_present=True  keys=[day, farms, hour, market, player, private,
                                   remainingOverageTime, step, town]
  seat 1: step_present=True  keys=[day, farms, hour, market, player, private,
                                   remainingOverageTime, step, town]

   seat  turn   step  day  hour  day*24+hour  match
      0     0      0    0     0            0   True
      0     1      1    0     0            1   True
      ...
      1     0      0    0     0            0   True
      1     1      1    0     0            1   True
      ...
      1     5      5    0     0            5   True

RESULT: PASS -- `step` is delivered to BOTH seats and is self-consistent
        (step == day*24+hour, and both seats agree)
```

Both seats receive `step`, the values agree across seats, and
`step == day*24 + hour` holds for every sampled turn.

### Probe 2 — locating the divergence

`tools/locate_divergence.py` measures all three observation-delivery paths in
one environment:

| path | seat 0 | seat 1 | verdict |
|---|---|---|---|
| **A.** `env.run([a0,a1])` — framework calls the agents | `[0,1,2,3,4]` | `[0,1,2,3,4]` | **OK** |
| **C.** `env.steps[i][seat].observation` — persisted snapshot | `[0,1,2,3,4]` | `['<MISSING>' ×5]` | **FAIL** |
| **B.** manual `env.step([callable, callable])` | `[0,1,2,3,4]` | `[0,1,2,3,4]` | **OK** |

### Root cause of the previous false conclusion

The framework's **delivered** observation and the **persisted per-seat snapshot**
differ.

`kaggle_environments/core.py` copies shared observation state with
`__get_shared_state(position)` when it builds the object handed to the agent, so
`step` reaches seat 1 at runtime. The `env.steps[i][1]` entry that the harness
retains for the match log does **not** go through that shared-state copy, so the
stored seat-1 snapshot lacks `step`.

The previous session's ad-hoc probes read the **stored snapshot** (path C) and
concluded the agent lacked `step` in seat 1. That was a **harness bug, not a
Kaggle bug**.

Note that `observation.step` is not declared in
`kaggriculture.json`'s own observation block, which is what made the snapshot
discrepancy look like an environment quirk. The generic
`kaggle_environments/schemas.json` also carries `step: null` in this
installation, so the schema alone cannot settle the question — only the runtime
probe can, which is why probes were used.

## Phase A conclusion

```
IS observation.step available to player 1?   YES
Evidence: real env.run() probe, both seats, step == day*24+hour, cross-seat equal
```

## Retracted conclusion

**Previous claim:**
> "The 2945 Farm verbatim crashes in seat 1 because observation['step'] only
> exists for player 0."

**Correction:**
> False. The local harness read persisted per-seat snapshots instead of the
> observations the framework actually delivers. Feeding an agent from
> `env.steps[i][seat].observation` omits shared fields for seat 1 and
> manufactures a `KeyError` that cannot occur under Kaggle's runner.

## Consequence for artifacts

`tools/verify_both_seats.py`, real `env.run()`, verbatim artifact
(sha256 `bfee70e9daaebeae0737a880f1df8f1c60d0783c59af620136cc0d28ef482bc7`):

```
seed 335464115 seat0: cash=[142723, 3700]  DONE/DONE
seed 335464115 seat1: cash=[3700, 142723]  DONE/DONE
seed  846389409 seat0: cash=[167853, 3546]  DONE/DONE
seed  846389409 seat1: cash=[3546, 167853]  DONE/DONE
crashes: 0
```

**The verbatim artifact is fully functional in both seats.** The seat patch was
built on a false premise.

Patch equivalence in seat 0 (must be identical, and is):

```
seed 335464115: orig=142723 patched=142723 identical=True
seed  846389409: orig=167853 patched=167853 identical=True
```

That equivalence is expected and not evidence of necessity: `step` is always
equal to `day*24 + hour` (`turnsPerDay = 24`), so the patch substitutes a
value-identical expression. It is behaviourally neutral **when `step` is
present**, and harmless when it is not.

### Artifact gate, corrected and rerun

`benchmark/validate_artifact.py` previously drove `env.step()` manually and fed
the candidate `env.steps[st][0].observation`. It now wraps the candidate in a
callable and uses `env.run([...])`, so it exercises the real delivery path in
both seats:

```
EXACT ARTIFACT VALIDATION (verbatim original)
  sha256 bfee70e9daaebeae0737a880f1df8f1c60d0783c59af620136cc0d28ef482bc7
  PASS  action schema valid across 2880 calls (0 violations)
  PASS  all episodes DONE
  runtime ms: median 0.371  p95 1.501  p99 3.433  max 44.312
  PASS  no stdout emitted / no stderr emitted
ARTIFACT VALID: all checks passed
```

## Harness inventory after correction

| script | delivery path | status |
|---|---|---|
| `benchmark/meta.py` | `env.run([a0,a1])` | already correct — tournament results stand |
| `benchmark/evaluate.py` | `env.run(...)` | correct |
| `benchmark/validate_artifact.py` | **now `env.run(...)`** | **corrected this session** |
| `benchmark/action_economy.py` | `env.run` | correct |
| `tools/probe_observations.py` | `env.run` | new, parity proof |
| `tools/locate_divergence.py` | all three paths | new, divergence locator |
| `tools/verify_both_seats.py` | `env.run` | new, artifact proof |
| `benchmark/forensic.py`, `endgame.py`, `close_games.py`, `audit.py`, `econ.py`, `trace.py` | manual `env.step` with `env.steps[...].observation` | **still snapshot-fed; diagnostics only, must not gate conclusions** |

The remaining snapshot-fed scripts are analysis/forensics tools that never
decide a competitive result; `benchmark/meta.py`, which does, was already on the
correct path. Their outputs are re-derived where they support a claim.

## Limitations

- The probe covers the local 1.32.7 runtime. Kaggle's server-side runner is not
  directly observable. Agreement between path A (the framework's own delivery)
  and the fact that every working public agent in this competition reads
  `observation["step"]` is strong indirect evidence that the server behaves the
  same.
- Two Kaggle replay files were examined earlier: player-1 stored observations
  lack `step`, consistent with path C above and therefore **not** evidence
  about runtime delivery.

## A SECOND harness defect, found later in the same audit

This report establishes that the observation *contents* reached both seats. It
did not catch that some agents were never asked to act at all, because the
harness handed Kaggle the agent's raw function.

Kaggle's runner invokes `agent(observation, configuration)`. Three league
members — `barnyard_v7`, `v16_rc5` and **our own `sunrise-v5`** — define
`def agent(obs)`. The `TypeError` is absorbed by the framework, the agent is
marked `INVALID`, it never acts, and it finishes on the starting $3,000.

So "both seats receive a correct observation" was true and still not sufficient:
three seats were receiving a correct observation that a broken agent was
ignoring.

The rule that follows: **parity of the observation is not parity of the
harness.** Both the delivered *contents* and the *call convention* have to be
right, and the only proof of the second is an agent that demonstrably acts.
`benchmark/agent_loader.py::probe_playable` now asserts 719 turns and a final
bank above the starting value for every league member before any number from it
is used.

Full detail, including which published conclusions it invalidated, in
`reports/HARNESS_SIGNATURE_AUDIT.md`.