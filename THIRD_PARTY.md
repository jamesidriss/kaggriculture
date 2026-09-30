# Third-Party Code and Licences

## Public agent artifacts reused in this repository

All entries below were recovered from **public Kaggle notebooks** using
`research/extract_nb.py`, which extracts `%%writefile main.py` cells verbatim
**without executing any notebook code**. No private data, leaked source, or
competitor credentials were used at any point.

### 1. The 2945 Farm v9/3 — `RECOVERY_CHAMPION_0`

- **Author:** thomastschinkel
- **Source:** https://www.kaggle.com/code/thomastschinkel/the-2945-farm-96-vs-the-top-10-public-bots
- **Published score:** 2945 (per notebook title)
- **Licence:** **Apache-2.0**, stated in the artifact's own header
- **Files:** `champions/public_champion_001/main.py`,
  `submissions/recovery_champion_0_exact/main.py`,
  `opponents/meta/farm_2945.py`,
  `research/public_src/the-2945-farm-96-vs-the-top-10-public-bots/`
- **Modifications:** **none.** Byte-identical to the notebook cell
  (SHA256 `bfee70e9daaebeae0737a880f1df8f1c60d0783c59af620136cc0d28ef482bc7`).
- **Notices:** the artifact's header already carries its full upstream
  attribution chain (thomastschinkel, yhay81, destbreso, aurax7, tetsutani,
  prvsiyan, Dmitrii Gluzdov, Ahmed Berat Ozer) and its retained Apache-2.0
  notices. These are preserved verbatim and unmodified.

> **Apache-2.0 attribution notice, retained as required:**
> Copyright the respective authors of The 2945 Farm v9/3 and its upstream
> contributors. Licensed under the Apache License, Version 2.0. The complete
> upstream notice block is preserved at the head of
> `submissions/recovery_champion_0_exact/main.py`.

### 2. [STRONG] Barnyard Economist V7

- **Author:** Roman Rozen
- **Source:** https://www.kaggle.com/code/romanrozen/strong-barnyard-economist
- **Published score:** 3034.8 (per the task brief; not independently confirmed
  on the leaderboard)
- **Licence:** **NONE STATED.** No Apache-2.0, MIT, or other licence appears in
  the notebook metadata or the source.
- **Files:** `champions/public_champion_000/main.py`,
  `submissions/barnyard_v7_exact/main.py`, `opponents/meta/barnyard_v7.py`,
  `research/public_src/barnyard/`
- **Modifications:** none (SHA256
  `997e6bfc5234534e246e945bc61c87858ebf997ab85b0a5c9427dd4ed710f1b6`).
- **Status:** retained for **evaluation and study only**. Because no licence is
  declared, it is **NOT cleared as a submission candidate** and must not be
  resubmitted by this project. If the author states a licence it can be
  reconsidered.

### 3. Other public agents used as opponents

| file | author | notebook | licence |
|---|---|---|---|
| `opponents/meta/v38_feed.py` | ahmedberatozer | kaggriculture-v38-smarter-feed-stronger-margins | stated in source |
| `opponents/meta/v16_rc5.py` | boatlee | v16-rc5-high-score-8c-4s-premium-market-lead | stated in source |
| `opponents/meta/shop_router.py` | yhay81 | shop-router-0909 | Apache-2.0 (per downstream attribution) |

Extracted verbatim, unmodified, for local evaluation only.

### 4. Excluded

`statma/kaggriculture-thomas-2944-candidate` was extracted but **rejected**: it
raises `RuntimeError` at import because it requires notebook-local inputs under
`\kaggle\input`, so it is not self-contained and could not be a legal
submission artifact. Preserved as
`opponents/meta/thomas_2944.NONSELF-CONTAINED.txt` with the reason.

## Environment

- **`kaggle-environments`** — https://github.com/Kaggle/kaggle-environments
- **Licence:** Apache-2.0. Version 1.32.7, used **unmodified** as the reference
  simulator for all evaluation.
- The only upstream constants re-declared inside this repository's agents are
  game data values (crop/animal tables, `MARKET_PARAMS`, `LAND_PRICES`, the
  `_shape` price functions), re-declared so an agent can compute sale prices
  locally without importing the environment. Values are reproduced verbatim.

## Competition documentation

`research/README.md` and `research/AGENTS.md` are the official Kaggriculture
documentation as distributed with the competition. They are byte-identical to the
copies inside `kaggle-environments` 1.32.7.

## Original work in this repository

`main.py` / `champions/champion_00*` (the "sunrise" series),
`benchmark/*.py`, `opponents/league.py` (the regression league), and all
reports. The sunrise series is retained for the record but is **not** competitive
and has been superseded; see `reports/SUNRISE_AUTOPSY.md`.