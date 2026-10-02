"""Ingest the public replay corpus into the lake, idempotently.

Sources, in priority order:
  1. `data/replay_db/index/episodes_index.parquet` - the episode index
  2. `data/replay_db/shards/ep_*.parquet`        - per-episode rows with seed,
                                                  config and (optionally) the
                                                  full step trace

Idempotency contract
--------------------
Re-running must not duplicate rows. The primary key is `episode_id`, and the
loader filters on what is already present. A second run over the same source
reports 0 inserted and leaves the table unchanged; the test suite asserts it.

Rating semantics
----------------
The index carries one rating column per player. It is the crawler's
`updatedScore`, i.e. the rating AFTER the episode, so it is stored as
`post_rating_*` with `rating_semantics = 'post_crawl'` and `pre_rating_*` left
NULL. Storing it as a pre-game rating would silently corrupt any model that
treats rating as a predictor. Nothing in the lake pretends to know the
pre-match rating.
"""
import glob
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "data_pipeline"))

from lake import (PARQUET, connect, create_tables, write_manifest,  # noqa: E402
                  _utc, row_count, summarize)

SRC = os.path.join(ROOT, "data", "replay_db")
INDEX = os.path.join(SRC, "index", "episodes_index.parquet")
SHARDS = os.path.join(SRC, "shards", "ep_*.parquet")
SOURCE_DATASET = "xishengfeng/kaggriculture-replay-db"

STOCK = {
    "episodeSteps": 720, "boardSize": 10, "startingMoney": 3000,
    "maxMarketOrdersPerTurn": 10, "turnsPerDay": 24, "shedCapacity": 100,
    "weedSpawnChance": 0.005, "townShopUnlockInterval": 3,
    "townShopSellInterval": 4, "townCenterSellInterval": 24,
    "farmHandCostMult": 1, "marketParams": {},
}
ENV_VERSION = "kaggle-environments 1.32.7"
# The index predates the 2026-09-30 deadline, so every episode it contains was
# produced under the same rules. That single-version assumption is what makes
# calibration possible at all, and it is recorded as `era_id`.
ERA_ID = "kag-1327-2026-09"


def _cfg_stock(cfg):
    if not isinstance(cfg, dict):
        return False
    for k, v in STOCK.items():
        if k in cfg and cfg[k] != v:
            return False
    return True


def load_episodes(limit_shards=None, verbose=True):
    import pyarrow.parquet as pq
    import pyarrow as pa
    import datetime

    if not os.path.exists(INDEX):
        print(f"  index missing at {INDEX}")
        return 0, {}

    con = connect()
    create_tables(con)
    have = {r[0] for r in con.execute("SELECT episode_id FROM episodes").fetchall()}

    idx = pq.read_table(INDEX).to_pylist()
    loc = {}
    shards = sorted(glob.glob(SHARDS))
    if limit_shards:
        shards = shards[:limit_shards]
    for s in shards:
        for i in pq.read_table(s, columns=["episode_id"]).column(0).to_pylist():
            loc[int(i)] = s

    rows, missing, nonstock, dup = [], 0, 0, 0
    seen = set()
    for r in idx:
        eid = int(r["episode_id"])
        if eid in have or eid in seen:
            dup += 1
            continue
        seen.add(eid)
        shard = loc.get(eid)
        cfg, seed, replay = {}, None, False
        if shard:
            rec = pq.read_table(shard, filters=[("episode_id", "=", eid)]).to_pylist()[0]
            seed = rec.get("seed")
            try:
                cfg = json.loads(rec.get("config") or "{}")
            except Exception:
                cfg = {}
            replay = any(k in rec for k in ("steps", "moves", "observations"))
        else:
            missing += 1

        stock = _cfg_stock(cfg)
        if not stock:
            nonstock += 1

        def ts(v):
            if v is None:
                return None
            s = str(v).replace("Z", "+00:00")
            try:
                d = datetime.datetime.fromisoformat(s)
                return d.replace(tzinfo=None)
            except Exception:
                return None

        cash0 = cash1 = None
        winner = None
        if r.get("reward_0") is not None and r.get("reward_1") is not None:
            # The index's reward is a normalised outcome, not cash.
            winner = ("0" if r["reward_0"] > r["reward_1"]
                      else "1" if r["reward_1"] > r["reward_0"] else "tie")
        rows.append((
            eid, int(seed) if seed is not None else None,
            ts(r.get("create_time")), ERA_ID, ENV_VERSION,
            None, None,                      # agent shas: unknown from the index
            None, None,
            r.get("score_0"), r.get("score_1"),
            "post_crawl",                     # crawler's updatedScore, POST-game
            r.get("score_0"), r.get("score_1"),
            cash0, cash1, winner,
            r.get("reward_0"), r.get("reward_1"),
            SOURCE_DATASET, bool(replay), stock, _utc(),
        ))

    if rows:
        # `agent_0_sha` is unknown for public episodes: Kaggle replays do not
        # publish the submitted source. Storing the episode's outcome with a
        # NULL agent key is honest; fabricating a key would poison the ladder.
        # Outcome statistics are consumed through the score columns, and the
        # shadow ladder joins only on episodes where both sides are known.
        placeholders = ", ".join(["?"] * len(rows[0]))
        con.executemany(f"INSERT INTO episodes VALUES ({placeholders})", rows)

    n = row_count(con, "episodes")
    stats = {
        "source": SOURCE_DATASET,
        "index_rows": len(idx), "shards_available": len(loc),
        "inserted": len(rows), "already_present": dup,
        "shard_missing": missing, "non_stock_config": nonstock,
        "episodes_total": n, "era_id": ERA_ID,
        "environment_version": ENV_VERSION,
        "rating_semantics": "post_crawl (updatedScore at crawl time, POST-game)",
        "agent_keys_present": False,
    }
    con.execute(
        "CREATE OR REPLACE TABLE ingest_episodes AS SELECT * FROM episodes")
    write_manifest("ingest_episodes", stats)
    if verbose:
        print(f"  index rows        : {len(idx):,}")
        print(f"  shard-mapped      : {len(loc):,}")
        print(f"  already present   : {dup:,}")
        print(f"  inserted          : {len(rows):,}")
        print(f"  shard missing     : {missing:,}")
        print(f"  non-stock config  : {nonstock:,}")
        print(f"  episodes total    : {n:,}")
    con.close()
    return len(rows), stats


if __name__ == "__main__":
    lim = None
    if "--limit-shards" in sys.argv:
        lim = int(sys.argv[sys.argv.index("--limit-shards") + 1])
    print("INGEST: public replay episodes")
    load_episodes(limit_shards=lim)
