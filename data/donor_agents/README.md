# Kaggriculture donor agents, snapshot 2026-09-24

121 executable community agents for offline Kaggriculture evaluation, exactly as published by their authors, with provenance, license, and a MEASURED behaviour-family classification so you know which ones are actually different opponents. 103 are a single `main.py`; 16 ship as tar.gz because their authors structured them as a loader over sibling files (policy, router, action tapes); 2 are metadata-only (avioon-apex-v7, moon_v189c: one under its author's terms, one because its notebook states no license and it is an uncredited derivative, so no redistribution right exists to exercise).

## What is in here

* `donors.csv`: one row per agent. Columns: identity, author, source URL, license, behaviour family, sha256, size, and `payload_b64`, the agent base64-encoded so a single CSV is enough to reconstruct every agent offline.
* `agents/<donor_id>.py` (or `.tar.gz` for a packaged agent): the same payloads in plain form, ready to load.

## Your agent

If you published an agent for this competition and it is not in this snapshot, say so in the comments and I will add it. All I need is the notebook URL: the file lands here byte-identical, credited to you, under the license your notebook carries.

The same goes for a correction. If a row credits you wrongly, or your notebook has moved on and the copy here is stale, tell me and I will refresh it. If you would rather not be included at all, say so and the row goes.

## Columns

| column | meaning |
|---|---|
| `donor_id` | stable identifier, also the filename under `agents/` |
| `author`, `source_url`, `license` | provenance; every agent belongs to its author |
| `published` | the day Kaggle reports for the notebook version this file came from, and the column `--since` and `--until` filter on. A field that turns over in days is a different population in every window |
| `pulled` | the day this copy was taken, which is not the same question |
| `behaviour_family`, `family_size`, `family_evidence` | measured equivalence class, see below |
| `main_py_sha256`, `size_bytes` | pins the file to the exact bytes that were measured |
| `payload_included` | False only where the license does not permit redistribution |
| `verified` | the date and the bank this agent scored against IDLE, reproduced from the CSV payload and from the original file. An agent that raises instead of playing says so here, in its own row, rather than being dropped |
| `payload_format` | `py` for a single file, `tar.gz` for a packaged agent |
| `payload_b64` | base64 of the raw bytes in that format |
| `verified` | the game-verification record of this snapshot: the reconstructed agent's bank equals the on-disk copy's |

## Use it in three steps

**1. Reconstruct an agent from the CSV alone** (verified for every included row: decoded payloads are byte-identical to the published files, and a season played from the reconstructed agent banks exactly what the original does):

```python
import base64, io, tarfile, pandas as pd
df = pd.read_csv("donors.csv")

def materialize(row, into="."):
    raw = base64.b64decode(row.payload_b64)
    if row.payload_format == "tar.gz":
        tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz").extractall(into)
    else:
        open(f"{into}/main.py", "wb").write(raw)

materialize(df[df.donor_id == "yhay81-shop-router-0909"].iloc[0])
```

For a packaged agent, put its directory on `sys.path` before loading `main.py`, exactly as the extractall above leaves it.

**2. Load it the way Kaggle does.** The runner takes the LAST callable bound at module level, whatever its name. Loading `module.agent` by name picks the wrong entry on some of these files:

```python
import importlib.util
spec = importlib.util.spec_from_file_location("donor", "main.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
entry = [v for v in vars(mod).values()
         if callable(v) and getattr(v, "__module__", "") == mod.__name__][-1]
```

**3. Play it.** Any harness that feeds observations works; the official one:

```python
from kaggle_environments import make
env = make("kaggriculture", configuration={"episodeSteps": 720, "seed": 11})
env.run([entry, entry2])
print(env.state[0].reward, env.state[1].reward)
```

Three practical notes, each learned the hard way:

* Set a headless matplotlib backend before loading (`import os; os.environ["MPLBACKEND"] = "Agg"`). One agent here calls `plt.show()` at import time, and an interactive backend blocks your process until a window is closed by hand.
* Load a FRESH module per game. These agents keep module-level state, most have no reset guard, and the ladder gives every episode a fresh process; a reused module replays the previous game's memory.
* Three agents (the xuantianfengwu pair and pilkwang's structured policy) import `kaggle_environments` at run time for the engine's constants, so that package must be importable where you play them.

## The behaviour families, and how they were computed

Byte-level hashes cannot tell you two agents PLAY the same, and names cannot tell you they play differently. Each measured agent played its games in an engine-exact simulator against two reference challengers over all 64 first-two-shop worlds and both seats, and two agents are in the same family when their full final-bank vector over those games is identical. Families measured on the arena's date over 3,180 games; agents added after that pass carry `F??` until the next one.

| family | n | members |
|---|---|---|
| F01 | 3 | ahmedberatozer-v47-reactive-market-coordination, ahmedberatozer-v48-clear-the-queue, shiiin9-beat-v48-100-0-your |
| F02 | 3 | guruprasaathas111-master-engine-v4, sunil123kumar-idle-workers, tetsutani-demand-preserving-turn-sale-timing |
| F03 | 2 | ahmedberatozer-v52-lean-flock-yarn-route, ahmedberatozer-v53-opening-signature |
| F04 | 2 | ahmedberatozer-v56-smarter-seeds-fertilizer, lynnsakurai-farmer-john-idle-seller |
| F05 | 2 | alperen5252525-ready-stock-earlier-sales, ghazarosghazaros-k0013-v46-advance6 |
| F06 | 2 | aurax7-shop-router-reactive-v7, jaxa623-2802-two-identical-agents-90 |
| F07 | 2 | dmitriigluzdov-a-smaller-market-shock, haideptry-2950-peak-farm |
| F08 | 2 | haideptry-shepherds-ledger-herd-safe-sovereign, statma-herd-safe-sale-window-submit |
| F09 | 2 | nihilisticneuralnet-population-robust-economy, wzhengbiao-v15stack-submit |
| F10 | 1 | ahmedberatozer-v49-funded-sale-timing |
| F11 | 1 | ahmedberatozer-v50-early-yarn-commit |
| F12 | 1 | ahmedberatozer-v51-lean-flock |
| F13 | 1 | ahmedberatozer-v54-productive-wheat-patient |
| F14 | 1 | ahmedberatozer-v55-one-turn-market-race |
| F15 | 1 | ahmedberatozer-v57-funding-order-invariant |
| F16 | 1 | alperen5252525-first-in-line-stock-into |
| F17 | 1 | alperen5252525-market-rhythm-sale-policy |
| F18 | 1 | anhadmahajan06-autonomous-ai-farming-agent |
| F19 | 1 | arsgorynich-herd-safe-v3-experimental-risk |
| F20 | 1 | arsgorynich-order-book-v3-response-improvement |
| F21 | 1 | dmitriigluzdov-one-more-wheat |
| F22 | 1 | goodpjw2008-melon-threshold-squeeze-2749 |
| F23 | 1 | haideptry-2965-master-hybrid-engine |
| F24 | 1 | hanifnoerrofiq-pioneers-kaggle-town |
| F25 | 1 | hanifnoerrofiq-wonderful-life |
| F26 | 1 | hosen42-m4a-metav4-sr18-2690-1 |
| F27 | 1 | jaxa623-2780-beyond-48-0-128 |
| F28 | 1 | kenanzhang9-a1-t31-guard |
| F29 | 1 | koshinm-local-best-2026-09-20 |
| F30 | 1 | koshinm-local-best-2026-09-21 |
| F31 | 1 | lynnsakurai-farmer-john-wheat-seller |
| F32 | 1 | nathanjacob-pipe15-two-layers |
| F33 | 1 | nathanjacob-pipe18-six-layers |
| F34 | 1 | shiiin9-your-market-list-is-an |
| F35 | 1 | statma-herd-safe-sale-window-race |
| F36 | 1 | statma-herd-safe-sale-window-race-ca20 |
| F37 | 1 | statma-tetsutani-demand-preserving |
| F38 | 1 | tetsutani-market-smart-farming |
| F39 | 1 | thomastschinkel-2945-farm-96-top-10 |
| F40 | 1 | wzhengbiao-hybu-submit |
| F41 | 1 | yasutakababa-late-purchase-v16-submit |
| F42 | 1 | zihengedie-best-version |
| F?? | 68 | ahmedberatozer-v27, ahmedberatozer-v31-production-and-sale-priority, ahmedberatozer-v34-observed-market-timing, ahmedberatozer-v35-reactive-sales-sheep-expansion, ahmedberatozer-v36-guarded-four-turn-sales, ahmedberatozer-v38-smarter-feed-stronger-margins, ahmedberatozer-v39-ready-before-the-rush, ahmedberatozer-v40-plans-that-fit-the-shops, ahmedberatozer-v41-review-candidate, ahmedberatozer-v42-production-that-fits-the-market, ahmedberatozer-v43-recovering-lost-harvests, ahmedberatozer-v44-winning-the-same-turn-sale-race, ahmedberatozer-v45-first-turn-wheat-round, ahmedberatozer-v46-first-turn-microstructure, aurax7-shop-router-reactive-v2, aurax7-shop-router-reactive-v4, aurax7-shop-router-reactive-v5, aurax7-shop-router-reactive-v6, avioon-apex-v7, boatlee-v16-rc5-r5a-recovery, boatlee-v20-adaptive-r1-multi-route, boatlee-v29-market-hysteresis, bruceqdu-route1, denizeryilmaz-v16-rc5, dmitriigluzdov-7-turn-rescue, dmitriigluzdov-herd-safe-sale-window-lb-2700, flexonafft-fieldbook-closeout, flexonafft-fieldbook-day9, flexonafft-multiroute, guruprasaathas111-fully-dynamic-autonomous-agent, hakdevelopment-2887-score-fieldcraft-agent, hesoponyo-pure-rl-agent-bc-ppo, hgh1024-herd-safe-v2-sale-horizon-2, hosen42-v11-hc1-h5-validation, indarkarhana-e776-latent-pasture, kaitofukami-v25-meta-reset, kenanzhang9-notebook6cc8bf1c92, leoprovorov-two-coins-at-high-noon-small-improvement, llccqq624-adaptive-counterbook, llccqq624-adaptive-shop-guard, llccqq624-premium-queue-split, llccqq624-shops-remember-the-route, lucifer19-harvest-nocturne-v2-a-lighter-start, lynnsakurai-farming-score-v4-a-better-shop, moon_v189c, municef1-lb-2448-single-file-agent, nathanjacob-beyond-v43-what-top-clusters, nathanjacob-pipe-5-terminal-boost, nathanjacob-pipe-8-clean-opening, nathanjacob-pipe7-wheat-microstructure, pilkwang-precomputed-schedule-policy, pilkwang-structured-economic-policy, prvsiyan-wheat-q45, rayk-topmeta-consensus-route, salemali7-3000-score, tschinkel-router-v5, tschinkel-router-v55, tschinkel-state-router, v21-r1-public-state-route-portfolio, xuantianfengwu-adaptive-land-allocator, xuantianfengwu-land-labor-capital-allocator, xuantianfengwu-preempt-selector, xuantianfengwu-timed-six-cow, yhay81-shop-router-0909, yhay81-shop-router-0911-simple, yhay81-shop-router-0913, yhay81-two-shop-router, zakariajoudar-rules |

121 agents, 42 measured families plus 68 awaiting a family. If you build an opponent pool from this set, one representative per family is the honest unit.

## Changes in this snapshot (2026-09-24)

* Every agent now carries a real publication date. Forty-six rows had none, so a dated window silently dropped them and the recent field read 28 agents when it holds 57.
* Three agents published on the 23rd and 24th are new here, one of them recovered from a single 524 KB bytes literal that an earlier extractor read as empty because it parsed the markdown cells alongside the code.
* arena.py now takes the entry point the Kaggle runner takes: a class defined at module level is callable and is not an agent, and 25 of these agents do not call their entry point 'agent'.
## Running the arena: `arena.py`

A set of opponents is not a measurement until you know how many DISTINCT opponents
it holds and how often you would actually meet each one. `arena.py` answers both.

    pip install kagsim-0.5.0.tar.gz          # the bit-exact C++ engine, optional
    # no network? extract both tarballs and compile the one source file directly:
    #   setup.py build_ext with include_dirs pointing at the pybind11 headers
    python arena.py --worlds 8               # the whole field against itself
    python arena.py --challenger MINE=main.py --vs-only --worlds 64
    python arena.py --worlds 64 --weights examples/weights_one_per_behaviour.json

| flag | what it is for |
|---|---|
| `--worlds N` | distinct first-two-shop worlds, taken from `worlds.json`; the shop draw is what makes two seeds different games rather than two samples of one |
| `--seats both` | the default, and it is not optional: the market settles slot by slot with player 0 first, so seat is worth real money and a one-seat table is biased in a direction you cannot sign |
| `--challenger NAME=PATH` | add your own agent; repeatable |
| `--vs-only` | your agents against the field only, which is the question when you are choosing what to submit, rather than the full all-against-all |
| `--weights FILE` | a population weight per opponent, applied at the END. The raw table weights every opponent equally, which is a panel; a ladder pays for beating whoever it matches you against. When the two orderings disagree, distrust the raw one |
| `--diverse N` | N agents spread across behaviour families and authors. Use this and not `--limit` for a small run: `--limit` takes the first N alphabetically and on this dataset those are six consecutive versions by one author, which is an opponent set of near clones |
| `--games FILE` | one row per game side: agent, opponent, seed, seat, world, both banks, margin. This is the file every cut by band, world or seat is computed from, and a pooled matrix cannot answer those questions because pooling is what threw the answer away |
| `--replay FILE` | re-report the games in a previous `--out` JSON instead of playing any. The two files in `examples/` are what this command writes, byte for byte |
| `--since YYYY-MM-DD`, `--until YYYY-MM-DD` | use only agents published inside a window: `--since` alone runs to today, `--until` alone from the beginning, both an interval, neither the whole snapshot. This is how you ask what the field looks like THIS week rather than since the competition opened |
| `--random N` | draw N agents at random from whatever the other filters leave, with the seed printed so the draw repeats. A random panel is the control for a chosen one |
| `--procs N` | play N games at once. The complete matrix over this field is a day on one core |
| `--exclude NAME` | leave one agent out; repeatable. One agent here runs a neural policy in pure Python and takes 225 SECONDS a game, which is a duel opponent and not a matrix one |
| `--probe` | report which agents IGNORE their opponent, an identical action stream against two very different rivals. It changes nothing about the games, it says what kind of field this is |
| `--limit N`, `--engine`, `--out`, `--matrix` | subset the field, force an engine, write the raw games and the per-pair-and-seat matrix |

**What a game costs, and the engine is not the answer.** Measured on one machine, one season: the
engine alone plays it in **0.73 ms**, the two observations the harness builds every turn add **32 ms**,
and one of these agents thinking on one side adds **200 to 1,800 ms**. A pairing of two large agents is
about 1.6 seconds of Python against under a millisecond of simulator. The field is the cost, not the
engine, and a faster engine buys about two percent.

What follows: use `--procs`, and choose the number of worlds to fit the time you have. Jobs run world by
world, so a run you stop early is a complete matrix over fewer worlds rather than a ragged one. Without
`kagsim` the script falls back to `kaggle_environments` automatically and says so: correct, not
approximate, and about 241 milliseconds a game on top of everything above.

**The obvious shortcut does not apply here.** An agent that ignores its opponent is a recording, and a
recording replays at the engine's speed instead of the policy's. Probed against two very different rivals
over three worlds and both seats, **3 of 83 agents played an identical stream and 80 did not**. This
field reacts, which is what makes it worth playing and what makes it expensive.

**The loading rule, which is a trap and not a detail.** The Kaggle runner takes the
LAST module-level callable, not the one named `agent`. Several agents in this dataset
keep an earlier, stale `agent` from a layer they later wrapped, and loading that one
silently drops everything after it: the agent runs, returns legal actions, and plays
a weaker game than its author wrote. `arena.py` uses the runner's rule and prints how
many agents in the field are affected.

## What to run, by what you are asking

| the question | the run |
|---|---|
| Is my agent ready to submit? | `--challenger MINE=main.py --vs-only --worlds 64 --procs 8` |
| Which of my two candidates is better? | `--challenger A=a/main.py --challenger B=b/main.py --vs-only --worlds 64` |
| What does the field look like NOW? | `--since 2026-09-13` |
| Did my ranking come from the panel I chose? | `--random 12 --worlds 16`, then again with another seed |
| What kind of opponents are these? | `--probe` |
| I already ran it and want another cut | `--replay run.json --games games.csv --matrix matrix.csv` |
| A quick check that the harness works | `--diverse 12 --worlds 6 --procs 4` |

Two of those deserve a sentence each.

**The window.** This field turns over in days, so the agents published this week are a different
population from the agents published since the competition opened, and the recent ones are the ones you
are about to meet. `--since` and `--until` cut the snapshot by the `published` column: `--since` alone
runs to today, `--until` alone from the beginning, both an interval, neither the whole thing.

**The random panel.** Ranking candidates against a panel you chose can reproduce your choice rather than
measure your agents. `--random N` draws the panel instead, prints the seed so the draw repeats, and two
draws that agree are evidence the ordering is not an artefact of the choosing.

## What is in `examples/`

* `full_matrix_20260919.csv`: a real run rather than a demonstration. 15,872 games,
  two reference challengers against all 62 loadable agents, 64 worlds, both seats,
  one row per ordered pair AND seat, with wins, losses, ties and both margins. Read
  the margin column beside the win column: in that run one pairing reads 33 % wins at
  a median of -10 dollars on banks near 100,000, which is a coin flip, and another
  reads 5 % at a median of -1,935, which is a defeat. A win rate alone cannot tell
  those two apart.
* `full_games_20260919.csv`: the same run, one row per game side: agent, opponent, seed,
  seat, world, both banks and the margin. 15,872 rows. This is the file to cut by world,
  by seat or by band of opponent strength; the matrix above is a pooled summary of it.
* Both CSVs are reproducible from the run they came from, and not by hand:

      python arena.py --replay run.json --challenger CAND= --challenger INC= \
          --games full_games.csv --matrix full_matrix.csv

* `weights_one_per_behaviour.json`: the simplest useful weighting, one vote per
  measured BEHAVIOUR rather than per file, so an agent republished under three names
  counts once. Feed it to `--weights` and compare the two columns.

## The telemetry layer

The C++ engine keeps 60 counters, maintained on every action and read with
`Game.telemetry(player)`. They answer the question a margin cannot: whether the thing
you built ever fired. `sell_zero_fill` counts market orders that sold nothing and burned
one of the ten slots anyway; `shed_discarded_units` counts production destroyed at the
shed cap of 100, which the engine does in silence; `hand_pass_turns` counts labour bought
and not used; `silent_loss_coins` and `silent_loss_units` count value lost with nothing
raised. `examples/telemetry_one_game.json` is one real game's full set.

Cost, measured with two idle agents so the engine and not Python is what is timed: never
reading, 0.61 ms a game; reading once at the end, 0.64 ms, five per cent; reading after
every one of the 719 steps, 3.22 ms, **5.3 times slower**. Take it once a game and it is
free. Take it every step and you have given back most of what the C++ engine bought you.

## When the arena refuses to rank

A run whose games nearly all end in an exact tie, or whose largest margin is under a
dollar, is an engine path that did not work rather than a field of equals. Two agents
that really play differently do not tie to the dollar. The script prints that verdict
above the table instead of letting a page of artefacts look like a result.

