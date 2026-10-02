# RANK1 CHECKPOINT

Canonical recovery point. Updated before and after every expensive phase.

| field | value |
|---|---|
| **phase** | COMPLETE — generation closed, RANK-1 READY: **NO** |
| **branch** | `research/rank1-offensive` (merged to `main`) |
| **base commit** | `9e8a7e130817e2e36cbe183f6db7806d33719633` |
| **current champion** | `C001_room_guard` |
| **champion SHA** | `a52ba1bfe9df9dc1d504550af46744ef8d474797cdba7af2412dc40a3ebdf3b8` |
| **champion parent** | v51 `c1e3590d02e42d16091c5377e87a3db16496e5a462d558dc2925887f835f9891` |
| **current best challenger** | none — all 8 transplant candidates failed the Moon gate |
| **long-running process** | none |
| **shadow rating** | **WITHHELD** (0 class-A anchors) |
| **RANK-1 READY** | **NO** |

## Last completed item

Full generation executed and closed: Moon licence audit, Moon full-field payoff,
Moon ablation by intervention, turn-0 transplant sweep, Rust provenance and
parity gate, anchor status, all reports written, tests, merge, push, remote
verify.

## Outputs produced

```
reports/MOON_AUTOPSY.md            mechanism, licence, lineage, field payoff
reports/MOON_DIFF.md               layer inventory with measured live/dead status
reports/RUST_PARITY.md             NO_GO with minimal reproducer
reports/ANCHOR_BINDING.md          not recovered; blocker stands
reports/SHADOW_LADDER_V3.md        WITHHELD
reports/RANK1_DASHBOARD.md         all gates
reports/RANK1_RESEARCH_CONCLUSION.md  30 numbered answers
experiments/rank1_results.csv      29 rows, consolidated
research/moon_provenance.json      licence + lineage + payoff
simulation/rank1/ablation2/        ablation records
simulation/rust/day_alignment.json parity evidence
policy/rank1/moon_ablation.py      v1 (documented as invalid)
policy/rank1/moon_ablation2.py     v2, def-site intervention
policy/rank1/transplant.py         C002 candidate sweep
simulation/rust/parity.py          parity harness
simulation/rust/day_alignment.py   sampling-convention test
```

## Resume command

```
git checkout research/rank1-offensive
git pull
.venv\Scripts\python.exe -m pytest tests\ -q
```

## Remaining gates

1. **Moon ≥ 0.45.** Currently 0.054. Naive transplant peaks at 0.125.
   Measured blocker: an opening that **collides with C001's own wheat plan**
   consumes the cash or market-order capacity its step-2 `BUY_PRODUCT WHEAT 30`,
   5 hires and 2 livestock purchases need, and those orders vanish.
   Survival requires a non-negative net outlay **or** a non-colliding product —
   plain "cash-neutrality" was refuted by the surviving `q20_s15_MILK` net buy.
2. **≥5 class-A anchors.** 0 today. Needs Kaggle kernel-version enumeration and
   exact-version output retrieval. See `reports/ANCHOR_BINDING.md`.
3. **Rust parity.** Resolve the purchase-settlement divergence, or abandon.
4. **Turn data at scale.** Still 8,640 rows / 6 episodes.

## Known traps in this codebase

Recorded because each one cost a run:

- **Appending a shim to a 43-deep wrapper chain does nothing.** Intervene at the
  `def` site. This produced a published "MECHANISM, drop 0.9000" that was a
  broken agent scoring 0-80.
- **A stub returning `None` breaks the agent and reports as a causal finding.**
  Disabled layers must pass through, and every variant must pass the playability
  probe before its score is used.
- **`episode` vs `serve`:** `kagg episode`'s `m` field is a hashed money value
  with offset steps; `kagg serve`'s `GENGAME` returns integer money.
- **Day boundaries differ in sampling instant** between engines; compare by
  `day`, never by list index.
- **Final-bank agreement is not parity.** 100/100 agreed while 75/100 tapes
  diverged in intermediate state.

## Last commit

See `git log -1`. Merge to `main` uses `--no-ff`; never force-push, never
rewrite history. Historical champions are immutable.