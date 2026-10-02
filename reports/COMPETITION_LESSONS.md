# COMPETITION LESSONS — what actually cost us the run

Ordered by measured cost, not by how embarrassing they were.

## 1. Optimising against a league that could not discriminate

**Cost: the entire result.** Sunrise scored 100% against our homemade league
(`opponents/league.py`) and finished at **241.5** on the real ladder.

When the league was replaced with 11 genuine public agents, the agent we had
declared champion (The 2945 Farm) went from an apparent 360-0 to **216-48** — and
lost to three opponents it had never been tested against.

The lesson is not "test against more opponents". It is that **a sweep is a
measurement failure, not a result**. Every time an agent won everything, the
correct response was to ask whether the league could lose, not to celebrate.

## 2. Declaring a winner before the league existed

The previous session wrote "RECOVERY_CHAMPION_0 selected by evidence" and a
300-0 record while the league contained five weak agents and one unlicensed
artifact. Selection was declared against opponents chosen by the same person
who wrote the agent.

## 3. A harness bug that manufactured a false conclusion

**Cost: a wrong headline finding and an unnecessary patch.**

The claim "The 2945 Farm crashes in seat 1" was produced by feeding agents from
`env.steps[i][seat].observation`. The framework copies shared fields into the
observation it *delivers* but not into the snapshot it *persists*, so seat-1
snapshots lack `step` and produced a `KeyError` that cannot occur on Kaggle.

The artifact was correct. We patched it anyway, shipped the patch as the
champion, and wrote the retraction nowhere. This is now proven and retracted in
`reports/KAGGLE_RUNTIME_PARITY.md`, and `tests/test_audit_regressions.py` fails
if any gating script feeds agents from snapshots again.

**Lesson: a harness bug and a product bug look identical from the inside.
Prove which one you have before you patch the product.**

## 4. Treating a theoretical price table as a causal claim

**Cost: a wrong postmortem.** We computed that Barnyard's pre-`hinge` model
mismeasures scarce carrot by 210× and concluded that explained its decline.

The counterfactual was never run. When it was: patching the price model moved
the record by **zero games** (0-10 before, 0-10 after). Barnyard's
cash-per-field-action is $5.48 against the champion's $5.64 — it is not
inefficient, it is marginally behind on production share and PASS rate.

**Lesson: a mechanism that explains a number is not evidence it explains an
outcome. Run the intervention.**

## 5. Deriving strategy from the price function alone

**Cost: abandoning a profitable strategy on false grounds.** We concluded
"animals are a trap" from MILK flooring at ~75 units and WOOL at ~59. The
winning agent's largest single revenue line is **WOOL**, and it runs a
17-sheep/6-cow pasture block.

**Lesson: isolated base-price arithmetic does not model a season. Realised
revenue includes by-products, shop demand, scale and timing.**

## 6. Confusing cash with outcome

The champion frequently ends games with *lower* cash than the agent it beats.
Every matchup here was decided by margin as small as **$506**, and 60% of
farm_2945-vs-v50 games were decided by under $1,000. Optimising margin would have
optimised the wrong thing.

## 7. Synthesising seeds and calling them ladder worlds

**Cost: unmeasurable overfitting risk.** Early evaluation used locally chosen
seeds. Real ladder seeds only arrived in the final session, from an 88,281-row
public replay index, with the split sealed and committed before evaluation.

## 8. The self-play contamination

An opponent file was overwritten by the champion, producing a fake 29-3 that
looked like a result. Caught only because identical cash *and* identical tile
layouts repeated — an impossible outcome between two different agents.

Fixed structurally: digest-addressed store, manifest verification, a
content-digest guard that raises rather than skips, and a derived league
directory (`benchmark/sync_league.py`) so no human copies an agent into a league
path.

## 9. Consuming the submission quota before meta validation

Five submissions went to agents benchmarked only against `starter`. By the time
the real meta was understood, the quota was gone. The active bots score 241.5 and
158.4.

**Lesson: the first submission of any kind is a placeholder. The quota is the
scarce resource, not the code.**

## 10. Not testing both seats systematically

Seat 1 was untested until the final audit, which is how the false crash
belief survived. Every evaluation since runs both seats, and a regression test
now asserts it.

---

## The reusable loop

```
CURRENT ENVIRONMENT (probe the runtime, don't read the schema)
  ↓
PUBLIC META       (digest-addressed, licence-checked, 11+ agents)
  ↓
REAL LADDER WORLDS (sealed dev/holdout/final, committed before use)
  ↓
PAIRED BOTH-SEAT  (env.run only; never persisted snapshots)
  ↓
INVARIANT GATE    (self-play, digests, licences, snapshot-feeding)
  ↓
ARTIFACT GATE     (exact bytes, full 720 turns, both seats)
  ↓
SEQUENTIAL TESTING (stop at 20 paired games when the effect is overwhelming)
```

The two rules that would have changed this run:

1. **A sweep means the league is broken.** Stop and fix the league.
2. **Never patch the product to fix a symptom you have not localised.** Prove
   which layer is wrong first.

Both are now enforced by tests, not by discipline.