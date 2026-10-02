# COMPETITION LESSONS — what actually cost us the run

Ordered by measured cost, not by how embarrassing they were. Items 1-3 are new
and are the expensive ones.

## 1. A harness bug that fabricated results about three agents

**Cost: a wrong headline finding, a wrong champion justification, and a wrong
postmortem — all published.**

Kaggle calls `agent(obs, configuration)`. `barnyard_v7`, `v16_rc5` and **our
own `sunrise-v5`** define `def agent(obs)`. Passing the raw function to
`env.run()` raises `TypeError` on every turn, the framework marks the agent
`INVALID`, it never acts, it finishes on the starting $3,000, and the opponent
is recorded as a decisive 72-0 winner.

So we reported:

- Barnyard V7 "collapsing" — it was never playing;
- v16_rc5 as a 0-72 pushover — it actually reaches $138,247 against `starter`;
- sunrise-v5 with 72 wins and a 8.3% win rate — it had **0 wins in 792 games**
  once it was really running, and it had never been running at all.

Full detail in `reports/HARNESS_SIGNATURE_AUDIT.md`.

**Why no guard caught it.** A non-player is the easiest possible opponent, so
the record looked *too good*. `errors: 0` — the framework had already absorbed
the exception. The self-play guard did not fire (content differed). The Wilson
interval cheerfully reported `[0.862, 1.000]` for 24-0 against a corpse. The
`mean_opp: 3000` field was in the JSON the whole time and nobody read it.

**Lesson: a green result is not a validated result. Assert on side effects —
invocations, exceptions, final bank — not on the absence of an error code.**

## 2. A harness bug that invented a product defect

**Cost: a patched artifact shipped as the champion, plus a false headline.**

We concluded "The 2945 Farm crashes in seat 1 because `observation['step']`
only exists for player 0." It runs in both seats, unmodified. The probes that
"proved" it were reading `env.steps[i][seat].observation` — the **persisted**
snapshot, which omits shared fields for seat 1 — instead of the observation
Kaggle actually **delivers**, which includes them. Proven and retracted in
`reports/KAGGLE_RUNTIME_PARITY.md`.

We then shipped the "fix" as the reference champion and wrote the retraction
nowhere.

**Lesson: a harness bug and a product bug look identical from the inside. Prove
which layer is broken before you patch the artifact.** Two separate harness bugs
in one audit, both producing confident false conclusions, both invisible to
every existing guard.

## 3. Publishing a fitted ranking from an unconverged model

**Cost: a report whose central table was meaningless.**

We published Bradley-Terry betas of `17.758 / 5.424 / -2.576 / -9.788` and an
ordering built on them. The fit never converged — the league is a two-tier star
in which four agents lose every game to every opponent they meet, so their
maximum-likelihood strength is **−∞** and no finite optimum exists. The
identical value `-9.788` printed for six different agents was the visible
symptom, and it was written off as "the bottom of the scale is degenerate"
rather than "this number is an artifact of where the loop stopped".

**Lesson: if your model will not converge, the answer is that the model does not
apply. Do not print the last iterate.** Model code must raise, and it must be
tested against data generated from known parameters.

## 4. Optimising against a league that could not discriminate

**Cost: the previous champion selection.** When the league was five weak agents,
farm_2945 recorded 360-0 and was declared champion. Against ten real public
agents it is 596-124 (82.78%) and **ties** the eventual winner.

**A sweep is a measurement failure, not a result.** The correct response to an
undefeated record is to ask whether the league can lose.

## 5. A theoretical price table presented as a causal claim

**Cost: a wrong postmortem.** We computed that Barnyard's pre-`hinge` model
mismeasures scarce carrot by 210× and concluded that explained its decline. The
counterfactual was never run. When it was: the patched agent finished at
**$74,991 — identical to the dollar, across all 24 games.**

The reason is better than the correction: the agent reads live prices from
`observation.market.prices`, and the table we patched is a **fallback for a
field the environment always supplies**. It is unreachable code.

**Lesson: a mechanism that explains a number is not evidence it explains an
outcome. Run the intervention — and when it moves nothing, find out *why*
nothing.**

## 6. Deriving strategy from the price function alone

**Cost: abandoning a profitable strategy on false grounds.** "Animals are a
trap" came from MILK flooring at ~75 and WOOL at ~59. The winning strategy's
**largest single revenue line is WOOL** ($96,684), behind 17 sheep and 6 cows.

A price-curve ceiling is not a revenue cap. By-product fertiliser ($24,872),
shop demand, scale and timing all sit outside the base price.

## 7. Confusing cash with outcome

The champion often ends games with *lower* cash than the agent it beats. The
v51-vs-farm_2945 margin is often a few hundred dollars on ~$100,000 banks.
Optimising margin would have optimised the wrong thing, and at this margin size
the sign of the difference is not even statistically resolved.

## 8. Synthesising seeds and calling them ladder worlds

Early evaluation used locally chosen seeds, so overfitting risk was
unmeasurable. Real ladder seeds arrived only in the final session, from an
88,281-row public replay index, split by SHA256 of the seed and committed before
evaluation. Even then the index stops at 2026-09-25 and misses the last five
days of ladder play.

## 9. Accidental self-play

An opponent file was overwritten by the champion, producing a fake 29-3. Caught
only because identical cash *and* identical tile layouts repeated — impossible
between two different agents. Fixed structurally: digest-addressed store,
manifest verification, a guard that raises rather than skips, and a derived
league directory (`benchmark/sync_league.py`) so no human copies an agent into a
league path.

## 10. Consuming the submission quota before meta validation

Five submissions went out against agents benchmarked only versus `starter`. By
the time the real meta was understood the quota was gone. Final scores: 348.1,
322.0, 316.8, 252.6, 138.5.

**The first submission of any kind is a placeholder. The quota is the scarce
resource, not the code.**

## 11. Not testing both seats systematically

Seat 1 went untested until the final audit, which is how the false crash belief
survived two sessions. Both seats are now mandatory and asserted.

---

## The reusable loop

```
PROBE THE RUNTIME      real env.run(), never the schema, never a snapshot
  ↓
ADAPT THE CALL         inspect agent's arity; wrap to (obs, configuration)
  ↓
VERIFY IT PLAYS        719 turns, cash != 3000, zero exceptions
  ↓
PUBLIC META            digest-addressed, licence-gated, lineage-diverse
  ↓
SEALED REAL WORLDS     dev/holdout/final committed before evaluation
  ↓
PAIRED BOTH-SEAT      official env.run only
  ↓
INVARIANT GATE         self-play, digests, licences, phantom opponents
  ↓
ARTIFACT GATE          exact bytes, 720 turns, both seats, silent
  ↓
MEASURE WITH INTERVALS Wilson on everything; report ties as ties
  ↓
SEQUENTIAL             stop at 20 paired games when the effect is overwhelming
```

The four rules that would have changed this run:

1. **A sweep means the league is broken.** Stop and fix the league.
2. **Never patch the product to fix a symptom you have not localised.** Prove
   which layer is wrong first.
3. **Assert on side effects, not error codes.** An agent that raises inside
   `env.run()` produces a perfectly green result.
4. **A model that will not converge has told you the model does not apply.**
   Do not print the last iterate.

All four are now enforced by code — `simcomp/` and
`tests/test_audit_regressions.py` (26/26) — rather than by discipline.
