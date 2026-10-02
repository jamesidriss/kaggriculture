# RESEARCH 3075 CHECKPOINT

Branch `research/3075-pipeline`. Main at entry: `73a3844`.

## Phase
**6 — shadow ladder built; calibration measured and found inadequate.**
Next: fast simulation (Rust differential) so search can run at scale.

## Done
- P0 git safety, branch pushed
- P1 **data lake**: DuckDB + Parquet, 8 typed tables, views, manifests
- P2 **ingestion**: 88,281 episodes (idempotent, verified 0 dup on re-run),
      16 unique agents keyed by SHA, lineage recorded with evidence
- P3 lineage catalog: 4 lineages, 2 league-eligible
- P4 **ladder calibration curve** from 88,280 real games (the key artifact)
- P5 **shadow ladder v1**: honest, refuses to publish a point rating

## The two findings that change the plan
1. **The ladder IS predictive.** P(higher-rated wins) by rating gap:
   0.579 / 0.714 / 0.816 / 0.894 / 0.934 / 0.969 / 0.995. Elite (both >=2900,
   n=24,548) = 0.708. So a 3075 rating means winning ~99% of games.
   => To reach 3075 the agent must be near-untouchable, not merely better.
2. **Calibration is INADEQUATE here.** Only 2 of 41 matchups are informative
   (not saturated): v51 vs farm 0.4763 over 3968 games -> gap 0, and v51 vs
   v49 0.9464 over 392 games -> gap 109. Everything else is a near-total win,
   and a saturated curve cannot invert a saturated observation.
   => Direct paired win rate vs the top meta is the PRIMARY gate. No point
      ShadowRating is published.

## Champion / hedge (unchanged, both frozen and immutable)
- PRIMARY `ahmedberatozer-v51-lean-flock`
  `c1e3590d02e42d16091c5377e87a3db16496e5a462d558dc2925887f835f9891`
- HEDGE `farm_2945_original`
  `bfee70e9daaebeae0737a880f1df8f1c60d0783c59af620136cc0d28ef482bc7`
- Relative strength measured: v51 is **+109 ladder points** over v49 and within
  ~25 points of the 2945 Farm. That v51-vs-farm comparison is the ONLY
  informative signal available for improvement work.

## Last benchmark
v51 vs farm: 1039-945 / 1984 (52.37%, Wilson [0.5017, 0.5456], p=0.0368)
Extended to 3968 games across all experiments: farm 47.63%.

## Next commands
```
python simulation/differential/parity.py --trajectories 10000
python policy/search/run_search.py --budget 200
python pipeline/run_research.py --stage smoke
```

## Blockers
- No strong independent opponent exists in the legally reusable public set
  (NO_GO recorded in reports/RETRACTIONS.md). Improvement can only be measured
  against the v51-vs-farm signal, so effect sizes below ~2 points are invisible.
- Ladder calibration has 2 informative observations. Nothing more can be
  extracted without a mid-strength agent whose public score is known.

## Uncommitted work
(none at last commit)
