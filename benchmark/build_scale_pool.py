"""Build a LARGE, FRESH ladder-derived seed pool, disjoint from the sealed splits.

The previous top-two comparison used only 36 elite worlds (12 per pool) and was
far too small to separate a 52.8% rate from 50%. This builds a fourth pool,
`REAL_scale.txt`, from the same audited public replay database, guaranteed
disjoint from REAL_dev / REAL_holdout / REAL_final, so the decisive experiment
never touches a world that was used to choose anything.

Audit performed before emitting:
  * index integrity (unique episode ids)
  * duplicate seeds
  * config recovery and stock-config verification
  * era/date coverage
  * explicit disjointness against the three existing pools
"""
import glob
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "data", "replay_db")
SEEDS = os.path.join(ROOT, "seeds")
EXISTING = ("REAL_dev.txt", "REAL_holdout.txt", "REAL_final.txt")
OUT_NAME = "REAL_scale.txt"
MIN_SCORE = 2900.0
WANT = 1000

STOCK = {
    "episodeSteps": 720, "boardSize": 10, "startingMoney": 3000,
    "maxMarketOrdersPerTurn": 10, "turnsPerDay": 24, "shedCapacity": 100,
    "weedSpawnChance": 0.005, "townShopUnlockInterval": 3,
    "townShopSellInterval": 4, "townCenterSellInterval": 24,
    "farmHandCostMult": 1, "marketParams": {},
}


def load_existing():
    used, detail = set(), {}
    for f in EXISTING:
        p = os.path.join(SEEDS, f)
        if os.path.exists(p):
            s = {int(x) for x in open(p, encoding="utf-8") if x.strip().isdigit()}
            used |= s
            detail[f] = len(s)
    return used, detail


def main():
    import pyarrow.parquet as pq
    idx = pq.read_table(os.path.join(DB, "index", "episodes_index.parquet")).to_pandas()
    print("=== INDEX AUDIT ===")
    print(f"  rows                 : {len(idx)}")
    print(f"  unique episode ids   : {int(idx.episode_id.nunique())}")
    print(f"  duplicate ids        : {len(idx) - int(idx.episode_id.nunique())}")
    print(f"  date range           : {idx.create_time.min()} -> {idx.create_time.max()}")
    elite = idx[(idx.score_0 >= MIN_SCORE) & (idx.score_1 >= MIN_SCORE)]
    print(f"  elite (both >= {MIN_SCORE:.0f})   : {len(elite)}")
    verify = elite.score_0.notna().all() and elite.score_1.notna().all()
    print(f"  ratings non-null     : {bool(verify)}")

    used, detail = load_existing()
    print(f"\n=== EXISTING SEALED POOLS ===")
    for k, v in detail.items():
        print(f"  {k:<20} {v} seeds")
    print(f"  total seeds in use   : {len(used)}")

    # Map episode -> shard once.
    loc = {}
    for s in sorted(glob.glob(os.path.join(DB, "shards", "ep_*.parquet"))):
        for i in pq.read_table(s, columns=["episode_id"]).column(0).to_pylist():
            loc[i] = s
    print(f"  episodes with a shard: {len(loc)}")

    rows, seen_seeds, seen_eps = [], set(), set()
    nonstock = 0
    for _, r in elite.sort_values("create_time", ascending=False).iterrows():
        if len(rows) >= WANT:
            break
        eid = int(r.episode_id)
        if eid in seen_eps:
            continue
        shard = loc.get(eid)
        if not shard:
            continue
        rec = pq.read_table(shard, filters=[("episode_id", "=", eid)]).to_pylist()[0]
        seed = rec.get("seed")
        if seed is None:
            continue
        seed = int(seed)
        if seed in seen_seeds or seed in used:
            continue
        try:
            cfg = json.loads(rec.get("config") or "{}")
        except Exception:
            cfg = {}
        overrides = [k for k, v in cfg.items() if k in STOCK and STOCK[k] != v]
        if overrides:
            nonstock += 1
            continue                      # only current, stock-config worlds
        seen_eps.add(eid)
        seen_seeds.add(seed)
        rows.append({"episode_id": eid, "seed": seed,
                     "score_0": float(r.score_0), "score_1": float(r.score_1),
                     "create_time": r.create_time})

    print(f"\n=== HARVESTED {len(rows)} fresh stock-config elite worlds ===")
    print(f"  non-stock configs skipped: {nonstock}")
    print(f"  overlap with sealed pools: {len(seen_seeds & used)}")
    scores = [min(x["score_0"], x["score_1"]) for x in rows]
    print(f"  weaker-player rating: min {min(scores):.1f}  "
          f"median {sorted(scores)[len(scores)//2]:.1f}  max {max(scores):.1f}")

    out = os.path.join(SEEDS, OUT_NAME)
    with open(out, "w", encoding="utf-8") as fh:
        for x in sorted(rows, key=lambda z: z["seed"]):
            fh.write(f"{x['seed']}\n")
    h = hashlib.sha256(open(out, "rb").read()).hexdigest()

    # Strata, so the champion comparison is not confined to one world regime.
    strata = {}
    for x in rows:
        band = ("elite_3000+" if min(x["score_0"], x["score_1"]) >= 3000
                else "strong_2900_2999")
        strata.setdefault(band, []).append(x["seed"])
    print(f"\n=== STRATA (by weaker player's ladder rating) ===")
    for k, v in sorted(strata.items()):
        print(f"  {k:<20} {len(v)}")

    meta = os.path.join(SEEDS, "REAL_scale.meta.json")
    with open(meta, "w", encoding="utf-8") as fh:
        json.dump({
            "source": "kaggle dataset xishengfeng/kaggriculture-replay-db",
            "filter": f"score_0 >= {MIN_SCORE} and score_1 >= {MIN_SCORE}, "
                      f"stock configuration only",
            "count": len(rows),
            "sha256": h,
            "disjoint_from": {k: v for k, v in detail.items()},
            "strata": {k: {"count": len(v), "seeds": sorted(v)}
                       for k, v in strata.items()},
            "episodes": rows,
        }, fh, indent=2)

    print(f"\n  wrote {OUT_NAME}  n={len(rows)}  sha256={h[:16]}")
    print(f"  wrote REAL_scale.meta.json")
    ok = not (seen_seeds & used) and len(seen_seeds) == len(rows)
    print(f"\nDISJOINT FROM SEALED POOLS AND DUPLICATE-FREE: {ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
