# RESEARCH 3075 CHECKPOINT

Branch `research/3075-pipeline`. Main at entry: `73a3844`.

## Phase
**COMPLETE — champion promoted, submission artifact re-frozen, gate 111/111.**

## Champion
`C001_room_guard` — `ahmedberatozer-v51-lean-flock` + `room_guard: True`
sha256 `a52ba1bfe9df9dc1d504550af46744ef8d474797cdba7af2412dc40a3ebdf3b8`
461,738 bytes, Apache-2.0, exactly one declared modification, verified
byte-for-byte outside the settings literal.

Predecessor preserved: `C000_v51` /
`c1e3590d02e42d16091c5377e87a3db16496e5a462d558dc2925887f835f9891`
Hedge unchanged: `postmortem_hedge/main.py`
`bfee70e9daaebeae0737a880f1df8f1c60d0783c59af620136cc0d28ef482bc7`
(same lineage as both — documented, not glossed)

## Headline evidence
| matchup | record | n | win rate | Wilson |
|---|---|---|---|---|
| C001 vs v51 | 657-155-180 | 992 | 80.91% | [0.7807, 0.8347] |
| C001 vs 2945 Farm | 537-453-2 | 992 | 54.24% | [0.5113, 0.5732] |
| v51 vs 2945 Farm | 506-486-0 | 992 | 51.01% | [0.4790, 0.5411] |
| sealed final (once) | 34-14-0 | 48 | 70.83% | [0.5682, 0.8176] |
| holdout | 30-18-0 | 48 | 62.50% | [0.4836, 0.7478] |
| independent lineage | 768-0-0 | 768 | 100.00% | [0.9950, 1.0000] |

Net effect on the top matchup: **+3.23 points** on identical worlds; mean cash
margin flips from −$26.9 to +$33.8. 0 broken games in ~3,800 paired games.

Replicated: a second independent run of the head-to-head gave 82.22%
(638-138-216 of 992).

## Deliverables complete
- A data lake: 88,281 episodes, idempotent, quality gate green
- B ingestion: agents keyed by SHA, 5 lineages
- C agent/episode linkage + honest NULLs where Kaggle publishes no identity
- D independent lineage: found `raykkretzschmar` (MIT, 10 agents), 4 in league
- E Rust simulator audit: NO_GO, none exists publicly
- F differential harness: contract + observable state + 2,000-trajectory self-test
- G Shadow Ladder v1: calibration curve fitted, point ratings WITHHELD
- H parameter search: exhaustive over 512 layer stacks, sampling bug found+fixed
- I one real automated candidate search → the promoted champion
- J champion decision: PROMOTE, five legs, thresholds declared in advance
- K submission_ready frozen and digest-verified against `CURRENT.json`
- L GitHub push

## Known defects left open
1. `benchmark/tournament.py` flags any exact cash tie as an invalid game. It is
   a fake-self-play heuristic and it misfires here: it removed exactly the
   216/992 worlds where the change had no effect, flattering the result.
   Corrected in `policy/search/room_guard_verdict.py`; **the runner itself is
   unchanged**, so all future experiments inherit the bias. Fix first.
2. No fast simulator → search resolution bounded near 100 candidates per phase.
   The other five off-layers in the same 2⁹ space remain untested at
   trustworthy resolution.
3. `turns` table empty → no feature store, no regime analysis, no imitation data.

## 3075-readiness
**NO.** Passes vs v51, vs Farm, vs independent lineages, both seats, sealed
final, runtime, frozen artifact. **Fails** the calibrated-rating leg (2
informative observations of 41; the ladder curve saturates, so no point rating
can be published) and world-regime coverage is not established.

The strongest defensible quantitative claim: 80.91% over the previous champion
is past the top of the fitted ladder curve, so the gap is **at least 275 ladder
points**. A bound, not a point estimate.

## Next commands
```
python pipeline/run_research.py --stage quality --stage rate --stage freeze
python tests/test_research_gate.py
```
Highest-value next work, in order:
1. fix the exact-tie validity rule in `benchmark/tournament.py`
2. commit the `turns` table so regime analysis and imitation become possible
3. re-run the grid search over the remaining five off-layers at higher resolution
4. find a mid-strength agent with a published `publicScore` to un-censor the
   ladder calibration

## Submission status
Kaggle submissions are closed (`CreateSubmission` → HTTP 400). Nothing has been
submitted and nothing in this repository can affect a live result.
