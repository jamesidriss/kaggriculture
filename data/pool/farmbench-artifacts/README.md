# FarmBench — can a language model run a farm?

A Kaggle Benchmark (DEV × Kaggle Benchmarking Challenge, Sep–Oct 2026) that grades LLM **economic decisions** with a
real game engine: [Kaggriculture](https://www.kaggle.com/competitions/kaggriculture) (`kaggle-environments` 1.32.7),
Kaggle's two-player, 30-day farming economy with finite product pools, non-linear price curves, a town that refills
demand, Fibonacci-priced labour and $1k/$2k/$4k land.

* Kaggle notebook / task: `manjunadhpadarthi/farm-economy-benchmark` (`farmbench.ipynb`, built from `farmbench.py`)
* Main task: `farm_economy_benchmark(llm) -> float` = mean captured gain over 15 decisions (0–1). Sub-task
  `farm_decision(llm, task_id) -> dict` runs one decision. No LLM judge anywhere; every grade is reproducible.
* Model access only inside the Kaggle notebook (`kbench.llm`); locally the notebook runs against a stub
  (`FARMBENCH_STUB=naive|best python farmbench.py`, see `test_local.py`).

## Files

| file | role |
|---|---|
| `farmbench.py` | notebook source (`# %%` cells). Sections: engine market functions (verbatim), rules digest, embedded tables, task specs, tasks, run |
| `farmbench.ipynb` | built by `build_notebook.py` (adds the `%choose farm_economy_benchmark` cell last) |
| `kernel-metadata.json` | Kaggle kernel metadata (id `manjunadhpadarthi/farm-economy-benchmark`, internet off, no data sources) |
| `build_tables.py` | offline simulation of every menu arm of the sim tasks (3 workers, ~470 games, ~8 min) → `tables/games.jsonl`, `tables/farmbench_tables.json`, `states/<task>.json` |
| `embed_tables.py` | inlines the tables and the decision-state texts into `farmbench.py` between the `# --- BEGIN TABLES` / `# --- END STATES` markers |
| `stub_llm.py`, `stub_answers_best.json`, `test_local.py` | local proof of the grader: the best stub must score 1.0 and the naive stub 0.1556 (two trap tasks where doing nothing is right, plus one partial-credit field) |
| `DRAFT_POST.md` | the DEV post (template of the challenge) |
| `NOTES.md` | worklog and design decisions |

## Scoring

Per task: `score = clip((value(choice) − value(naive)) / (value(best) − value(naive)), 0, 1)` — the share of the available gain the
decision captured, where *naive* is the do-nothing / obvious answer and *best* the engine's optimum. Sanity tasks score 0 / 0.5 / 1
per correct field. Benchmark score = unweighted mean over the 15 tasks; a task with no parseable decision counts 0. Each decision
also asserts `score >= 0.5` (recorded, not required) and the main task asserts that all 15 decisions were graded.

Structured output: `ask()` calls `llm.prompt(..., schema=dataclass)` (with `max_tokens=6000` on the OpenAI backend so the model
proxy's cost reservation stays small); if the reply cannot be parsed (Gemma 4 echoes the JSON schema, DeepSeek-R1 answers in prose)
it re-prompts once with "reply with ONLY a JSON object with exactly these fields", then records the error and scores 0.

Every prompt = the same rules digest (generated from the engine's own `market_price`, so the numbers cannot drift from the code)
+ a situation + one structured decision (`schema=` dataclass) + a free-text `rationale`. Rationales are regex-scanned for four
ideas (pool saturation, the SE quadrant, Fibonacci hand cost, refill/demand) and the counts are printed; they are not scored.

## The 15 tasks and how each is graded

### Sanity (rules arithmetic; unambiguous)

| id | decision | correct | grading |
|---|---|---|---|
| `hire_math` | day 12 h18, 6 hours left, farmer + 5 hands, 40 plants must be watered today: how many more hands, what do they cost? | 1 hand, $8 (6th hire of the day = fib(5)) | 0.5 per correct field |
| `feed_or_lose` | 3 wheat, 5 cows, A and B unfed yesterday: who gets fed? | A and B (+ any one more) | 1 / 0.5 / 0 |
| `fertilizer_melon` | melon watered daily; fertilize at age 6? units at age 10 with / without, first age at 6 units | 6 / 6 / age 8 (fertilizer buys time, not units) | 1/3 per correct field |

### Exact (graded in the notebook with the engine's price function and per-unit lockstep market)

| id | decision | naive → best | why it is interesting |
|---|---|---|---|
| `melon_dump` | day 10, 72 melons, opponent dumps 72 this hour: sell how many now? (rest tomorrow) | hold all $9,525 → sell all $13,126 | no shop buys melons; the pool never recovers; lockstep sharing |
| `melon_race_timing` | harvest 12 melons at age 9 (60 units, sell alone) or age 10 (72 units, lockstep with the opponent's 72)? | age 10 $13,240 → age 9 $14,301 | a smaller lot sold first beats a bigger lot sold together |
| `wool_lot` | day 27, 30 wool at I0+40 (price $107), one yarn store (13 units/day refill): split over days 27/28/29 | dump now $1,130 → hold to day 29 $4,457 | for a lone seller in this engine, waiting always dominates spreading (the town refills 26 units in two days) |
| `milk_front_run` | day 29, 24 milk at I0+20, opponent sells 4/hour at hours 0–5: hourly plan | wait to hour 23 $1,700 → sell 20 at h0 + 4 at h1 $2,086 | the opposite of `wool_lot`: with an opponent selling, front-run them (DP with lockstep) |
| `crop_choice` | day 12, 25 fresh tiles, given market offsets and the shops' daily drains: one planting of which crop? | nothing $0 → STRAWBERRY $24,462 (TOMATO $8,118, WHEAT $3,980, CARROT $2,732, MELON −$964) | reading a scarcity curve + refill rate; melon looks premium but its pool is already crashed |

Implementation: `sell_run` (one seller, one hour), `lockstep_sell` (both players, same hour, the engine's alternating unit loop),
`schedule_value` / `best_schedule` (DP over period × units left × inventory), `lockstep_schedule_value` / `best_lockstep_schedule`
(same with an opponent schedule), `crop_value` (harvest calendar × drains × price curve, minus seeds).

### Simulation (menus; every arm played offline by the engine — `tables/farmbench_tables.json`)

Executor = our knob-driven policy bot `kaggriculture/submissions_v32_main.py` (hand-written routing/market policy with a `P` dict of
strategy knobs); opponent = Thomas Tschinkel's public "95-5 win rate via replay routing" shop-router bot (the league2 gate
opponent); `variants/late/fixtown.py` applied so the town's shop sequence is a function of the seed; both seats; towns chosen for
the task (yarn-store towns, pet-cafe towns, ...). Value of an arm = mean final coins of the executor over its games. The prompt's
situation is the executor's real observation at the decision step of the naive arm on the first seed, rendered as text.

| id | day | arms (knob / injection) | seeds × seats | naive | best (mean coins) |
|---|---|---|---|---|---|
| `opening` | 0 | 8 day-0 shopping lists (`cows_day0`, `sheep_day0`, `geese_day0`, `melon_tiles`, `wheat_day0`, `straw_day0`, `land_day0`) | 6 × 2 | cautious 67,713 | goose_farm 72,419 (strawberry_rush 55,700 worst) |
| `sheep_yarn` | 6 | max sheep 0/2/4/6/8 (`demand_aware=False, max_sheep=n`), yarn store open by day 6 | 4 × 2 | 0 sheep 74,725 | 8 sheep 96,818 |
| `sheep_no_yarn` | 6 | same arms, towns with no yarn store all season | 4 × 2 | 0 sheep 95,277 (best) | 8 sheep 84,478 (worst) |
| `se_quadrant` | 12 | never / BUY_LAND injected hourly from day 12, 16, 20 until 4 quadrants | 6 × 2 | never 68,484 (best) | buy day 12 67,140 |
| `max_hands` | 0 | `max_hands` 2/4/6/8/10/12/14 | 6 × 2 | 2 hands 33,539 | 12 hands 68,484 (14 hands 61,972) |
| `terminal_tomato` | 16 | `term_tomato_days=(d,)` d = 16/18/20/22, min price 0, or off | 4 × 2 | off 61,225 | day 18 66,669 (day 20 59,850) |
| `terminal_carrot` | 24 | `term_carrot_days=(d,)` d = 24/25/26/27, or off | 4 × 2 | off 74,277 | day 24 75,010 (day 27 73,341) |

Free-form numeric answers are snapped to the nearest arm; option keys are matched by name. A dropped task, `land_ne_timing`
(buy NE on day 2/4/6/8/10/never), is still in the tables: with $36 cash on day 2 every "buy on day D" arm collapses into "buy when
the melon money arrives" (all within 0.5k), so it only measured "expand at all" (+18k) — not a decision worth a slot.

Known issues (kept in this version, disclosed in the post; to fix next): the `max_hands` question includes the hint "roughly 2-3
actions per tile per day", which anchors every model to 8 hands while the executor's optimum is 12 (its workload includes walking,
shed trips and animal care) — the hint is itself an economic claim and should be removed; `opening`'s ground truth is executor-
dependent (the real top-10 opening `meta_a` scores 0 because the executor does not play the meta's follow-up).

Caveats, stated plainly: the executor is a mid-ladder bot (Tschinkel's bot wins most of these games); the tables measure the
effect of a decision *under that continuation policy*, and a few arms are executor-specific (the top-10 "meta A" opening scores
below the executor's default because the executor does not play the meta's follow-up). Rankings are what the tasks use, not the
absolute coins. Six to twelve games per arm; differences under ~1k are noise (`terminal_carrot` is a small-stakes task).

## Reproduce

```sh
PY=../../.venv/bin/python
$PY build_tables.py --workers 3          # ~8 min on a laptop; resumable; writes tables/ and states/
$PY embed_tables.py                      # inline tables + states into farmbench.py
$PY test_local.py                        # exact optima + stub runs: best must be 1.0, naive 0.1556
$PY build_notebook.py                    # farmbench.ipynb with the %choose cell (for the web import path)
```

### Results — `results/` (`collect_results.py` rebuilds them from `kaggle b t log`; the log keeps one run per model)

| file | content |
|---|---|
| `results/results.md`, `results.json`, `rationales.md` | **version 5** (26–27 Sep 2026, 21 models, one clean run each): summary table, per-task scores and choices, every rationale — the numbers in the post |
| `results/v3_results.md` | version-3 run (26 Sep, 15 scored models, with the `max_hands` hint): saved by hand; used for the hint experiment and the test–retest |
| `results/retest_v3_v4.md` | v3 vs v4 choice agreement, 20 min apart: 93/131 decisions unchanged at temperature 0 |
| `results/v5_runs.log`, `rerun_when_quota.sh` | how the v5 runs were scheduled (cheap models first, the 11 quota-blocked models retried every 8 h until clean) |

v5 scores (19 scored): Gemini 3.7 Flash 0.90, GPT-6 Astra 0.86, Gemma 4 31B 0.86, Claude Opus 5 0.86, Gemini 3.8 Flash 0.84,
Claude Sonnet 5 0.84, Gemini 2.5 Flash 0.81, GLM-5 0.81, GPT-5.5 0.80, Gemini 2.5 Pro 0.79, Claude Opus 4.8 0.74, Grok 4.20 R 0.73,
gpt-oss-20b 0.72, Claude Sonnet 4.5 0.71, GPT-5.4 mini 0.65, Gemini 3.1 Flash-Lite 0.55, gpt-oss-120b 0.52, GPT-5.4 nano 0.40,
Claude Haiku 4.5 0.40. DeepSeek-R1: every answer fails the structured parse even after the JSON-only re-prompt. Grok 4.6: HTTP 404
on the proxy. v3 → v5 on the nine unchanged menu tasks: 96/135 decisions unchanged (29% moved, same as v3 → v4).

Known weak spots, disclosed in the post: `terminal_carrot`'s best-to-worst spread is $733, under the $1,000 noise line of the
simulation tables (day 26 sits $226 below "off"), so its zeros are not trusted; `hands_10` vs `hands_12` is a $510 tie; the
`opening` menu's `meta_a` arm is executor-specific.

### Publishing: use the CLI's benchmark commands, not `kernels push`

A notebook pushed with `kaggle kernels push` runs in the standard Kaggle image, which has no `kaggle_benchmarks` and no
model proxy (version 1 of `manjunadhpadarthi/farm-economy-benchmark` failed at `import kaggle_benchmarks`). The benchmark
runtime is provisioned only for benchmark tasks. Kaggle CLI 2.2.4 drives those directly from the `.py` source:

```sh
K=../../.venv/bin/kaggle
$K benchmarks tasks push farm_economy_benchmark -f farmbench.py --wait   # converts # %% cells itself; runs the default model
$K benchmarks tasks status farm-economy-benchmark                        # creation state + per-model runs
$K benchmarks tasks models                                                # slugs of the ~40 available models
$K benchmarks tasks run farm-economy-benchmark -m gemini-2.5-flash -m claude-sonnet-4-5-20250929 --wait
$K benchmarks tasks log farm-economy-benchmark -m <model>                # notebook stdout: per-task table + rationales
$K benchmarks tasks download farm-economy-benchmark -o out/              # run outputs
$K benchmarks tasks publish farm-economy-benchmark                       # make the task (and backing notebook) public
```

Task page: https://www.kaggle.com/benchmarks/tasks/manjunadhpadarthi/farm-economy-benchmark (model comparison:
`?compare=true`). The web alternative (kaggle.com/benchmarks/tasks/new, import `farmbench.ipynb`, Save Version,
"Evaluate More Models") does the same thing in the browser; `kernel-metadata.json` is kept only for that notebook's id.
