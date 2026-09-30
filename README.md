# Kaggriculture

Competitive engineering workspace for the Kaggle **Kaggriculture** agent competition.

- **Competition:** https://www.kaggle.com/competitions/kaggriculture
- **Repository:** https://github.com/jamesidriss/kaggriculture
- **Local:** `C:\Users\James\kaggriculture`

## Current status

**`RECOVERY_CHAMPION_0` = The 2945 Farm v9/3** by thomastschinkel
(Apache-2.0). Undefeated on the held-out seed pool: **60-0** across five distinct
strong public agents, both seats.

```
submissions/recovery_champion_0_exact/main.py
sha256 bfee70e9daaebeae0737a880f1df8f1c60d0783c59af620136cc0d28ef482bc7
```

Validated as an exact artifact: 0 schema violations, 0 stdout/stderr, max call
28 ms against a 1,000 ms `actTimeout`. Read
`reports/EMERGENCY_FINAL_DECISION.md` before using any of this.

### Two findings that matter most

1. **Published leaderboard scores are not evidence of current strength.** In the
   current environment the ranking *inverts*: the agent with the higher published
   score (Barnyard V7, 3034.8) loses 0-22 locally to a lower-published agent
   (The 2945 Farm, 2945). The cause is a `hinge` change to the market scarcity
   curve that Barnyard's embedded price model predates — a 210× mispricing on
   deep carrot scarcity. See `reports/BARNYARD_ROOT_CAUSE.md`.
2. **Cash and win rate diverge in this game.** The champion often ends with
   *lower* cash than the agent it beats. Cash is a diagnostic only; promotion
   decisions are win-rate based.

## Layout

```
main.py                    original sunrise agent (KILLED, kept for the record)
champions/
  champion_000/            sunrise-v4  (immutable)
  champion_001/            sunrise-v5  (immutable)
  public_champion_000/     Barnyard V7      (no licence - NOT submittable)
  public_champion_001/     The 2945 Farm   <- RECOVERY_CHAMPION_0
opponents/
  league.py                REGRESSION suite only; NOT evidence of competitiveness
  meta/                    exact public meta agents (6 distinct artifacts)
benchmark/
  meta.py                  paired/both-seat meta harness + self-play guard
  validate_artifact.py     exact-artifact validation
  evaluate.py, trace.py    sunrise-era harness
research/
  CURRENT_RULES.md, META_MAP.md, PUBLIC_META_AGENTS.csv, public_src/
reports/                   feasibility, autopsy, tournament, final decision
experiments/               EXPERIMENTS.csv, public_meta_results.csv
seeds/                     meta_dev / meta_holdout / meta_final (disjoint)
submissions/               submission-ready artifacts
tests/                     submission gate
```

## Workflow

```bash
.venv\Scripts\python.exe benchmark\meta.py --cand champions\public_champion_001\main.py \
    --games 6 --stage meta_final
.venv\Scripts\python.exe benchmark\validate_artifact.py \
    --path submissions\recovery_champion_0_exact\main.py
.venv\Scripts\python.exe tests\test_submission.py
```

Seed pools are disjoint: never tune on `meta_final`.

## Rules

Never commit Kaggle credentials, tokens, cookies, or env secret files.
Public agent artifacts are reused only under their declared licences — see
`THIRD_PARTY.md`.