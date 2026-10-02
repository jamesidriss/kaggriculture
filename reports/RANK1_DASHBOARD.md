# RANK-1 DASHBOARD

## RANK-1 READY: **NO**

Two independent legs fail, and neither is softenable.

## Gates

| gate | required | measured | verdict |
|---|---|---|---|
| **RUST PARITY** | 0 unexplained divergences | intermediate state diverges on 75/100 tapes; purchase settlement unreconciled | **NO_GO** |
| **ANCHORS ≥5 (class A)** | 5 | **0** | **FAIL** |
| **ANCHOR SPAN ≥250** | 250 pts | **0 pts** | **FAIL** |
| **INDEPENDENT LINEAGES** | ≥2 | 0 class-A | **FAIL** |
| **MOON COUNTER** | C001 ≥ 0.45 vs Moon | **0.054** | **FAIL** |
| **C001 MATCHUP** | >0.50, lower 95% >0.50 | 0.7520 / 0.7530 (replicated) | pass |
| **FARM MATCHUP** | >0.50, lower 95% >0.50 | **0.5510** [0.5200, 0.5815], N=2000 | pass |
| **WORLD COVERAGE** | diverse regimes | 4 regimes / 6 worlds | weak |
| **SHADOW CALIBRATION** | accepted | **WITHHELD** | **FAIL** |
| **SEALED FINAL** | run once | not run — no finalist | n/a |
| **RUNTIME** | p99 < 100 ms | inherited from C001 | pass |
| **LICENSE** | declared | Moon **UNKNOWN** → analytical only; champion Apache-2.0 lineage | pass (analytical) |
| **SUBMISSION ARTIFACT** | submission-ready | `submission_ready/` points at C001 | pass |

## The two failing legs

**Leg 1 — Moon.** C001 scores **0.054** against a publicly obtainable artifact
(27-473-0, N=500). A rank-1 agent cannot carry a known catastrophic matchup. The
mechanism is now understood (`reports/MOON_AUTOPSY.md`) but **not closed**: the
8-candidate transplant sweep peaked at **0.125**, and 4 of 8 candidates
actively destroyed C001's Farm matchup (0.5510 → 0.0000).

**Leg 2 — Calibration.** Zero class-A anchors. No rating may be expressed at any
confidence, so `>3069.5` is untestable. `reports/SHADOW_LADDER_V3.md` is
**WITHHELD**.

## Measured state of the league

| matchup | N | BT score | note |
|---|---|---|---|
| moon_parent vs C001 | 240 | **0.9208** | Moon dominant |
| moon_parent vs v51 | 240 | 0.9417 | |
| moon_parent vs Farm | 240 | **0.9833** | Moon beats Farm hardest |
| moon_q13_mg vs C001 | 240 | 0.9208 | byte-distinct, behaviourally identical to moon_parent |
| C001 vs Farm 2945 | 2000 | 0.5510 | [0.5200, 0.5815] |
| C001 vs v51 | 2000 | 0.7520 / 0.7530 | replicated on independent seed pools |

## The uncomfortable summary

Moon is **not** an independent lineage — identifier Jaccard vs C001 is **0.7192**,
*higher* than the Farm's own 0.6098, and its header derives it from the same
v9/3 root as our Farm hedge. It is our own family's strongest offshoot, it beats
us 0.92 to 0.05, **and it cannot be submitted** because its licence is UNKNOWN.

So the best strategy we can legally obtain is the one we just watched dismantle
our champion, and understanding it did not translate into beating it.

## Champion

**Unchanged.** `C001_room_guard`
sha256 `a52ba1bfe9df9dc1d504550af46744ef8d474797cdba7af2412dc40a3ebdf3b8`
parent v51 `c1e3590d02e42d16091c5377e87a3db16496e5a462d558dc2925887f835f9891`

No challenger was promoted. C001 remains immutable and is **not** a rank-1 agent.

## Throughput

Official Python engine, 8 workers, ~107 matches/min. Unchanged. The Rust engine
that would have lifted this was gated to NO_GO on an unresolved divergence.