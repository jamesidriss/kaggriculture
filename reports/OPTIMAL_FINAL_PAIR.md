# OPTIMAL FINAL PAIR — what we should have submitted

Decision as of the evidence available now. **Kaggle submissions are disabled**
(HTTP 400 `FAILED_PRECONDITION`), so this is a record of the correct decision,
not an action.

## PRIMARY

**The 2945 Farm v9/3, seat-patched.**

- **Artifact:** `postmortem_champion/main.py`
- **SHA256:** `c936e5a71ba40e1700ca1ab3a3271132407446bbb8b7523ced2cf4450ed8463f`
  (856,428 bytes)
- **Licence:** Apache-2.0, full upstream attribution retained in-file
- **Source:** https://www.kaggle.com/code/thomastschinkel/the-2945-farm-96-vs-the-top-10-public-bots
- **Evidence:** 300-0 across three disjoint elite-ladder seed pools (dev /
  holdout / final), both seats, 0 errors; Bradley-Terry beta 10.203, highest of
  six agents; median final cash $95k-183k vs sunrise-v5's $5-9k
- **Modification:** one mechanism only — 30 `observation["step"]` reads rewritten
  to the agent's own `_step_of()`. Required: the verbatim artifact crashes in
  seat 1. Seat-0 output is byte-identical before and after.

## HEDGE

**Multi-Route Farming Agent V43.**

- **Artifact:** `opponents/store/919fc1d61050cd96/main.py`
- **SHA256:** `919fc1d61050cd96f799979e49177ae3ac7bce98ec9835724238bea73f4a08ed`
- **Licence:** Apache-2.0 (SPDX headers in source)
- **Source:** https://www.kaggle.com/code/flexonafft/kaggriculture-multi-route-farming-agent
- **Evidence:** 20-0 against the primary on elite seeds (i.e. the second-strongest
  agent we could reproduce); BT beta 5.936, second of six
- **Verification:** exact bytes recovered from the notebook's `SOURCE_BYTES`
  literal; the artifact's own pinned SHA256 assertion passes
- **Why hedge:** genuinely differentiated lineage (opening funding guard, RACE
  reservation, COURIER/CARROT/HERD layers) rather than a near-duplicate of the
  primary, so it covers a different failure mode

## Rejected candidates

| candidate | reason |
|---|---|
| sunrise-v5 / v4 | 4-3 and 3-4 on real ladder games; ~$0.19 cash per field action vs $5.58 |
| Barnyard V7 | **no licence declared anywhere** — not redistributable or submittable. Also loses 0-22 locally (stale pre-`hinge` price model) |
| thomas_2944 | raises `RuntimeError` at import; depends on `\kaggle/input`; not a legal artifact |
| three-day shop router (native) | byte-verified but `agent.so` is Linux/mac only; unevaluable on this host |
| V38 Smarter Feed / V16-RC5 | legitimate but 20-0 against both primary and hedge; no reason to spend a slot |

## Why this pair

Both slots filled with the two strongest *legal, current-environment-compatible*
artifacts we could reproduce, differentiated by lineage, both verified on real
elite-ladder worlds in both seats, with the seat-1 crash fixed on the primary.

## Counterfactual placement — calibrated

I will not claim "would have won". What the evidence supports:

- Our active pair (sunrise-v5 250.0, sunrise-v4 153.0) was **roughly 1500-2000
  rating points below the leader** (3052.1), and below the ~$8-10k opponent
  cash at which sunrise-v5's win rate crosses 50%.
- The postmortem pair reproduces at **$95k-183k** final cash on elite worlds,
  matching the observed band for 2900+ rated agents in the replay database
  (elite games there end at $64k-158k).
- So: the pair would very likely have been **competitive with 2800-3000-level
  agents**, and is **indistinguishable from the strongest public agents we
  could reproduce**. Whether that is #1 of 10,246 teams is **not established** —
  our league has only two credible top-meta lineages, and the elite public field
  has almost no extractable artifacts.
- One concrete known cost: the verbatim primary (unpatched) would have failed
  every seat-1 game. The patch removes that.