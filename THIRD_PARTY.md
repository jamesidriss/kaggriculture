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
---

## Audit-era additions (branch `audit/kaggle-runtime-parity`, merged to main)

### 2. ahmedberatozer v43 / v44 / v46 / v48 / v49 / v50 / v51 â€” `postmortem_champion_000`

- **Author:** ahmedberatozer
- **Source:** Kaggle dataset `destbreso/kaggriculture-donor-agents-20260902`,
  files `agents/ahmedberatozer-v{43,44,46,48,49,50,51}-*.py`
- **Licence:** **Apache-2.0**, declared per agent in the dataset's
  `donors.csv` provenance table
- **Extraction method:** `kaggle datasets download ... --unzip`. Files were
  copied byte-for-byte; no notebook code was executed and no agent was modified.
- **Reference champion:** `ahmedberatozer-v51-lean-flock`,
  SHA256 `c1e3590d02e42d16091c5377e87a3db16496e5a462d558dc2925887f835f9891`,
  stored verbatim at `postmortem_champion_000/main.py`.
- **Modifications:** **none.**
- **Notices:** retained under Apache-2.0. The dataset README states the pack
  contains community agents "exactly as published by their authors, with
  provenance, license".

> **Apache-2.0 attribution notice, retained as required:**
> Copyright (c) ahmedberatozer and the Kaggriculture community contributors whose
> agents are redistributed in `destbreso/kaggriculture-donor-agents-20260902`.
> Licensed under the Apache License, Version 2.0. Each artifact retains its own
> header notices unmodified.

### 3. Agents analysed but NOT eligible for competitive use

| agent | author | licence | why not eligible |
|---|---|---|---|
| barnyard_v7 | romanrozen | **none stated** | `UNKNOWN_LICENSE` â€” no licence declared, so redistribution and competitive use are not permitted. Retained for forensic analysis only, in `opponents/unlicensed/`. |
| shop_router | yhay81 | Apache-2.0 | `NOT_SELF_CONTAINED` â€” raises `FileNotFoundError` for `actions.json` on turn 1; that file is not in the public notebook. Not a legal single-file submission artifact. |
| thomas_2944 | statma | unknown | `NOT_SELF_CONTAINED` â€” `RuntimeError` at import; requires `\kaggle\input`. |
| three-day shop router (native) | yhay81 | Apache-2.0 | `PLATFORM` â€” `agent.so` is Linux/macOS only (`WinError 193` on this host). Digest verified against the author's published manifest; unevaluable, so not used. |

### 4. Attribution correction

The artifact previously recorded in this file as "Multi-Route V43" and
attributed to *flexonafft* is **byte-identical**
(SHA256 `919fc1d61050cd96f799979e49177ae3ac7bce98ec9835724238bea73f4a08ed`) to
`ahmedberatozer-v43-recovering-lost-harvests`. It is ahmedberatozer's v43. The
earlier attribution to a different author was wrong and is corrected here; the
donor-pack provenance is authoritative. The digest-addressed store merged the
duplicate automatically rather than counting one agent twice.

### 5. Data sources

| dataset | use |
|---|---|
| `xishengfeng/kaggriculture-replay-db` | 88,281 public episodes; the source of the real ladder seeds in `seeds/REAL_*.txt`. Index audited: 0 duplicate episode ids, 24,548 games with both players rated >= 2900. |
| `destbreso/kaggriculture-donor-agents-20260902` | 121 community agents with per-agent provenance; 7 of them are in the competitive league. |

### 6. No private material

At no point were private sources, leaked code, competitor credentials, or
non-public notebooks used. Behavioural analysis of **public** replays was
performed and is reported in `reports/`, but no agent source was reconstructed
from observed behaviour. Submission gating was never circumvented.



---

## 7. Final-pass additions (branch 
inal/meta-resolution)

### Postmortem HEDGE

- **Artifact:** postmortem_hedge/main.py
- **Agent:** The 2945 Farm v9/3, by thomastschinkel
- **Source:** https://www.kaggle.com/code/thomastschinkel/the-2945-farm-96-vs-the-top-10-public-bots
- **Licence:** Apache-2.0, upstream attribution retained in-file
- **SHA256:** fee70e9daaebeae0737a880f1df8f1c60d0783c59af620136cc0d28ef482bc7
- **Modifications:** **none**, byte-identical to the notebook cell.
- **Not a diversifying hedge.** Measured by enchmark/lineage_check.py: the
  PRIMARY and this artifact share 1,205 identifiers, have containment 0.818,
  and contain one contiguous identical run of **3,352 tokens**, with an
  identical nine-author credit list. They are the same lineage.

### Digest convention (changed this pass)

core.autocrlf=true had been rewriting every artifact to CRLF in the working
tree while all recorded digests described the LF blob, so **no** recorded
SHA256 matched the file on disk. Fixed by marking every artifact directory
-text in .gitattributes and normalising 50 files to LF.

**Canonical digest definition from now on: SHA256 over the bytes as committed
to Git (LF line endings)**, which is what git cat-file returns and what any
Linux checkout reproduces. Two store keys changed as a result:

| agent | old (CRLF) digest | canonical (LF) digest |
|---|---|---|
| v43 recovering-lost-harvests | 919fc1d61050cd96… | 3abe0ca715ba1864… |
| v44 same-turn-sale-race | 797d9bca309d481e… | 
e370bd8a9d0f377… |

enchmark/normalize_artifacts.py --check is a release gate that compares every
tracked artifact against its Git blob, and enchmark/build_catalog.py
regenerates 
esearch/FINAL_PUBLIC_AGENT_CATALOG.csv with **recomputed**
digests — the previous hand-maintained catalog contained placeholder values
that described nothing.

### Final-week search (NO_GO, recorded for provenance)

Pulled from public Kaggle Code and examined: statma/kaggriculture-herd-safe-sale-window-submit,
haideptry/the-shepherds-ledger, hanifnoerrofiq/pioneers-of-kaggle-town,
wzhengbiao/kaggriculture-hybu-submit, yasutakababa/kaggriculture-late-purchase-v16-submit,
sunyuxiang136/kaggriculture-opening-stock-v8. None yielded a legally reusable,
self-contained, licensed agent artifact. Where a licence could not be
determined, no licence is asserted. See
reports/RETRACTIONS.md.


---

## RANK1 generation additions

### moon_parent, moon_q13_mg — Kaggle dataset kksky9k/kaggriculture-r88-rivals

**Verdict: LICENCE UNKNOWN. ANALYTICAL OPPONENT ONLY. NOT A SUBMISSION CANDIDATE.**

An Apache-2.0 licence body appears inside each file. **A licence body is not a
grant.** Four independent blockers, each sufficient on its own:

1. **The derivation chain is broken.** The header states
   *"Derived from queue_compact.py"*, and that file is **not distributed**.
   An Apache-2.6 derivative chain must be traceable to a root Work.
2. The header states the artifact is *"unproven and is not an official Kaggle
   score claim"* — it was never presented as a submitted artifact.
3. The header marks it *"FOR LOCAL DISCOVERY ONLY"* — a statement about intended
   use, not a licence.
4. **The distributing dataset declares no LICENSE or NOTICE file of its own.**

Permitted use: adversarial benchmark and analysis. **No Moon source may be
transcribed into any artifact this project submits.** Any mechanism used is
reimplemented from scratch against the public action interface, and its parameters
are swept rather than copied.

Attribution as declared in the artifact: thomastschinkel, yhay81, destbreso,
aurax7, tetsutani, prvsiyan, Dmitrii Gluzdov.

**Correction to our own catalog:** Moon was previously labelled an *independent
lineage*. That is **wrong**. Its header derives it from *Kaggriculture submission
v9/3, public V39* — the same root as our Farm hedge — and identifier Jaccard
against C001 is **0.7192**, higher than the Farm's own 0.6098.

### kaggriculture-simulation - external Rust simulator (NOT a submission dependency)

| field | value |
|---|---|
| repository | github.com/debmalyaroy/kaggriculture-simulation |
| commit | 953ac86c462ba1dbdcb897f6020fd7bdacf27720 |
| licence | Apache-2.0, LICENSE + NOTICE present |

Upstream, unchanged: a Rust port of the Kaggriculture environment pinned to
kaggle-environments release **1.32.7**. Its declared pin for
envs/kaggriculture/kaggriculture.py is
c8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e, and our own
installed 1.32.7 file hashes **identically**, as does kaggriculture.json
(82c89c1a2315b93f39775d8e025471a01b738647c9772658368ee6b1b6f4867).

**Research use: NO_GO — parity is NOT verified.** The two engines disagree on
market purchase settlement. See 
eports/RUST_PARITY.md for the minimal
reproducer. The divergence is **unresolved** and is deliberately **not**
attributed to the upstream engine, because our own tape encoder is an
unvalidated part of the harness. kaggle-environments itself is not redistributed.
