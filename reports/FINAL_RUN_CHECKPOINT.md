# FINAL RUN CHECKPOINT

Canonical resume point. Read this file and `git status`; do not reread history.

- **Branch:** `final/meta-resolution` (from `main` @ `ba4a6ef`)
- **Repo:** C:\Users\James\kaggriculture
- **Remote:** https://github.com/jamesidriss/kaggriculture

## Phase status

| # | Phase | State |
|---|---|---|
| 0 | git safety, branch, push | DONE |
| 1 | correct Kaggle call-convention claim | DONE |
| 2 | correct Wilson / canonical stats | DONE |
| 3 | canonical loader + playability probe | DONE |
| 4 | seed audit + fresh pools | DONE |
| 5 | league expansion (independent lineages) | DONE |
| 6 | v51 vs Farm large paired test | DONE |
| 7 | connected round robin + BT identifiability | DONE |
| 8 | forensics, close-game mining, challenges | DONE |
| 9 | freeze PRIMARY + HEDGE, reports, tests | DONE |
| 10 | commit, merge, push, remote verify | DONE |

All phases complete. See `reports/FINAL_RESEARCH_CONCLUSION.md`.

## Champion / hedge

- **PRIMARY** `ahmedberatozer-v51-lean-flock`
  sha256 `c1e3590d02e42d16091c5377e87a3db16496e5a462d558dc2925887f835f9891`, Apache-2.0
  → `postmortem_champion/main.py`
- **HEDGE** `farm_2945_original` (The 2945 Farm v9/3)
  sha256 `bfee70e9daaebeae0737a880f1df8f1c60d0783c59af620136cc0d28ef482bc7`, Apache-2.0
  → `postmortem_hedge/main.py`

## Two corrections made this pass (both material)

1. **Kaggle call convention.** The claim "Kaggle calls `agent(obs, configuration)`
   so one-argument agents crash" is **FALSE**. `Agent.act` truncates the
   argument list to `co_argcount`, so both arities are supported. Proof and
   source quote in `benchmark/kaggle_call_convention.json` and
   `reports/HARNESS_SIGNATURE_AUDIT.md`. The historical defect was in *our*
   diagnostic scripts, which invoked agents directly; the competitive harness
   `benchmark/meta.py` was verified byte-equivalent before and after the
   "fix" and was never broken.
2. **Wilson interval.** The previously published interval for `76/144` was the
   interval for `68/144`. Correct value is **[0.4466, 0.6075]**. The label and
   the interval came from different win counts. All reports regenerated from
   `benchmark/stats.py`, validated against an independent implementation
   (`benchmark/stats_selftest.py`, 51/51).

## Top-two verdict

144-pair evidence did not separate v51 from Farm. A larger fresh paired
experiment was run to resolve it. Result and interval in
`reports/V51_VS_FARM.md` and `reports/TOP_META_TABLE.md`.

## Key numbers

See `reports/LEAGUE_TABLE.txt` (regenerate: `python benchmark/league_table.py`).

## Gates

- `python benchmark/stats_selftest.py` — 51/51
- `python tests/test_audit_regressions.py` — 26/26
- `python -m simcomp.selftest` — 19/19
- `python benchmark/call_convention.py` — both arities supported
- `python benchmark/agent_loader.py --probe-all` — all league agents play
- `python benchmark/validate_artifact.py --path postmortem_champion/main.py`

## Never repeat

- Do not re-litigate the call convention; it is settled by source + execution.
- Do not re-run the dev/holdout/final sweeps; validity unchanged.
- Do not publish BT betas unless `bt_identifiability()` returns `ok`.
