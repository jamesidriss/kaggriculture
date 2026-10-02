# OPTIMAL FINAL PAIR — parity-safe revision

Supersedes the previous version, which was written before the runtime-parity
audit and before the league was strengthened. Both of those changed the answer.

Kaggle submissions remain closed (`400 FAILED_PRECONDITION`), so this records
the decision that should have been made, not an action taken.

## PRIMARY

**`ahmedberatozer-v51-lean-flock`**

- **Artifact:** `postmortem_champion_000/main.py`
- **SHA256:** `c1e3590d02e42d16091c5377e87a3db16496e5a462d558dc2925887f835f9891`
  (461,739 bytes)
- **Licence:** Apache-2.0
- **Source:** Kaggle dataset `destbreso/kaggriculture-donor-agents-20260902`,
  `agents/ahmedberatozer-v51-lean-flock.py`; agent authored by ahmedberatozer
- **Modifications:** none — byte-identical to the published artifact
- **Evidence:** 742-50 across 792 parity-correct games (dev 248-16, holdout
  238-26, sealed final 256-8), 11 opponents, both seats, 0 errors. Local BT
  beta 57.667, the highest in the league. Artifact gate: 2,880 calls, 0 schema
  violations, max 33.1 ms of a 1000 ms `actTimeout`.

## HEDGE

**`farm_2945_original`** (The 2945 Farm v9/3)

- **Artifact:** `opponents/meta/farm_2945_original.py`
- **SHA256:** `bfee70e9daaebeae0737a880f1df8f1c60d0783c59af620136cc0d28ef482bc7`
  (856,428 bytes)
- **Licence:** Apache-2.0, full upstream attribution retained in-file
- **Source:** https://www.kaggle.com/code/thomastschinkel/the-2945-farm-96-vs-the-top-10-public-bots
- **Modifications:** none — the **verbatim** artifact. The previous session's
  seat patch (`c936e5a7…`) was built on a retracted claim and is retained as
  `challengers/challenger_001_farm2945_seatsafe.py` only.
- **Evidence:** the only agent besides v51 that beats v51 at all
  (38-34 to v51 across 72 games). Local BT beta 24.212, second.

### Why this is a genuine hedge, not a near-duplicate

Different lineage and a genuinely different portfolio:

| | v51 | farm_2945 |
|---|---|---|
| end-of-season farm | lean flock | 17 sheep + 6 cows, strawberry belt |
| market orders / 4 games | 3,618 | 11,526 |
| HIRE orders | 1,064 | 3,195 |
| SELL orders | 1,450 | 5,073 |
| cash per field action | $5.64 | $5.58 |

They differ on labour cadence, sale volume and portfolio, and they beat each
other at a coin-flip rate. That is what makes v51 the pick and farm_2945 a real
second slot rather than a copy.

## Rejected

| candidate | reason |
|---|---|
| sunrise-v5 / v4 | 4-3 / 3-4 on real ladder games; **$0.19** cash per field action vs **$5.64**; 63% of actions spent moving |
| Barnyard V7 | **no licence declared**; 0-72 vs farm_2945; and the hinge-patch counterfactual moved it 0 games |
| ahmedberatozer v49 / v50 | lose 22-2, 18-6, 24-0 to v51; also mutually identical (24/24 ties) — one lineage, not two |
| ahmedberatozer v43/v44/v46/v48 | 24-0 to v51 on all three pools |
| three-day shop router (native) | byte-verified against the author's manifest, but `agent.so` is Linux/mac only; `WinError 193` on this host, so unevaluable |
| thomas_2944 | raises `RuntimeError` at import; needs `\kaggle/input` |

## What changed from the previous recommendation

| | previous | now |
|---|---|---|
| primary | farm_2945 (seat-patched) | **v51-lean-flock (verbatim)** |
| hedge | multi_route_v43 | **farm_2945 (verbatim)** |
| basis | 300-0 vs 5 weak agents | 742-50 vs 11 strong agents, 3 sealed pools |

Two reasons: the strengthened league showed farm_2945 was **not** dominant
(loses 8-16 on final, 10-14 on holdout), and the runtime-parity audit showed the
seat patch was unnecessary — so the verbatim public artifact is the correct
canonical reproduction.

## Counterfactual placement — calibrated

Not claiming #1 of 10,246.

- Our active pair (241.5 / 158.4) sat ~1500-2600 points below the leader
  (3052.1) and below the ~$8-10k opponent cash at which sunrise's win rate
  crosses 50%.
- This pair finishes at **$95k-183k** median on real ladder worlds, matching the
  band observed for 2900+ rated agents in the public replay index (elite games
  end at $64k-158k).
- Therefore: **competitive with 2800-3000-level agents**, and above every other
  agent we can legally reproduce. Whether that is #1 is **not established** —
  our league contains two credible top lineages, and the elite public field has
  almost no extractable artifacts.
- Known cost avoided: the previous recommendation's primary would have carried
  an unneeded 30-site patch.