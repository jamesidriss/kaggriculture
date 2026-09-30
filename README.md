# Kaggriculture

Final-sprint competitive engineering workspace for the Kaggle **Kaggriculture** agent competition.

- **Competition:** https://www.kaggle.com/competitions/kaggriculture
- **Repository:** https://github.com/jamesidriss/kaggriculture
- **Local:** `C:\Users\James\kaggriculture`
- **Mode:** Deadline sprint — ~6h to final submission.

## Objective

Produce, validate, version, and submit the strongest reliable Kaggriculture agent.
Primary metric is **pairwise win rate**, not raw cash.

## Principles in force

- **Champion / challenger** — a working champion is never modified in place.
- **Paired evaluation** — same opponent, same seed, both seats.
- **Real meta league** — random/starter are smoke tests only.
- **Holdout discipline** — `HOLDOUT_SEEDS` are not tuned against.
- **One hypothesis per experiment** — no untraceable mega-changes.
- **Deployment fidelity** — benchmark the exact packaged archive.
- **NO_GO is a valid outcome** — regressions are killed fast.
- **Win rate > cash** — the competition rewards match wins.
- **Push everything important to GitHub** — GitHub is disaster recovery.

## Structure

```
main.py              # submission entry point (def agent(obs))
agent/               # champion working source
champions/           # immutable champion snapshots + metadata
opponents/           # opponent league agents
benchmark/           # paired evaluation harness
research/            # rules audit + meta map
reports/             # submission state, final decision
experiments/         # EXPERIMENTS.csv experiment log
submissions/         # packaged artifacts + metadata
tools/               # packaging / verification scripts
tests/               # smoke + integrity tests
```

## Rules acknowledgement

Never commit Kaggle credentials, tokens, cookies, or env secret files.
See `.gitignore` and `THIRD_PARTY.md`.