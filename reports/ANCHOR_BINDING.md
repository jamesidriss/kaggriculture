# ANCHOR BINDING REPORT

## Verdict

**NOT RECOVERED. The prior blocker stands unchanged.**

This generation recovered **zero** new exact-version score anchors. The
`reports/3075_RESEARCH_CONCLUSION.md` blocker — *no public artifact can be bound
to an official score with class-A evidence* — is **not** resolved by anything in
this generation.

Recording that plainly is more useful than a table of near-misses. The eight
candidate anchors in the research brief were **not attempted**: no Kaggle
notebook-version enumeration was run this generation. That is unfinished work,
recorded as unfinished, not silently dropped.

## Current anchor inventory

| # | artifact | score | class | binding | note |
|---|---|---|---|---|---|
| 1 | `farm_2945` (postmortem_hedge) | ~2945.4 | **B** | **inferred** | team-name binding inferred from the leaderboard, not from a submission id |

Count: **1**. Class A: **0**. Required for a ShadowRating publication: **5**.

## Why Class A remains structurally blocked

A class-A anchor needs all four of:

1. a Kaggle notebook/script **version id**,
2. the **Public Score displayed for that exact version**,
3. the **exact output artifact** retrieved from that version,
4. a **verified digest** tying (3) to (2).

Kaggle exposes no submission-id → team mapping through any public API surface
available here. Without that, an artifact retrieved from a notebook version
cannot be *proven* to be the file that produced the displayed score. Matching by
title, by best-score, or by "latest version" is exactly the forbidden
substitution — it attaches one version's score to another version's bytes.

## The trap this project has already fallen into twice

Recorded so it is not fallen into a third time:

- **"Best Score" must never be bound to the current version.** A notebook family
  whose latest version scores ~1500 and whose Best Score is 2767.3 (V59) yields
  a valid anchor only as *V59 artifact ↔ 2767.3*.
- **A turn-variable file is not a score anchor** unless the version id is pinned
  alongside the digest.

## What would actually unblock it

1. Run Kaggle's kernel-version enumeration for the eight named candidates, and
   retrieve **exact version outputs**, not `latest`.
2. For each, hash the artifact and record `scriptVersionId` + displayed score in
   the same row.
3. Require ≥5 class-A anchors spanning ≥250 points and ≥2 independent lineages
   before `shadow_ladder/score_candidate_v2.py` will publish anything.

Until then the publication gate stays closed, and the correct output is
**WITHHELD** — not a softened gate and not an estimated number.

## Licence note on one candidate

`Ray Kretzschmar / Rank Your Agent V11` (reported 2990.4) was flagged in the
brief for licence verification. It was **not retrieved this generation**, so its
licence is **unverified**. It is treated as `UNKNOWN` — analytical only — by
default, exactly as Moon is.