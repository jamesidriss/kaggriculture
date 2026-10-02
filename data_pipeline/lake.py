"""Kaggriculture data lake: DuckDB + Parquet, local, zero server.

Design
------
Physical storage is Parquet partitioned by dataset. DuckDB is the query layer
and the catalogue. Large files are git-ignored; schemas, manifests, checksums
and small fixtures are committed, so the lake is reproducible from public
sources without bloating Git.

Identity rule, enforced by `lake.agents`: **the artifact SHA256 is the agent
identity.** Filenames and labels are attributes, never keys. This is the single
most important invariant in the project; every previous contamination incident
came from violating it.

Layout
------
    data_lake/
      lake.duckdb          catalogue + views (git-ignored)
      parquet/
        agents/            one row per unique artifact
        episodes/          one row per public episode
        turns/             per player per step
        experiments/       experiment registry
        matches/           per-game rows
      manifests/           committed: source + checksums + row counts
      _tmp/                staging, git-ignored
"""
import glob
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LAKE = os.path.join(ROOT, "data_lake")
PARQUET = os.path.join(LAKE, "parquet")
MANIFESTS = os.path.join(LAKE, "manifests")
TMP = os.path.join(LAKE, "_tmp")
DB = os.path.join(LAKE, "lake.duckdb")

# ---------------------------------------------------------------- schemas
# Every column is typed. `agent_sha` is a 64-hex string and is the ONLY agent
# key anywhere in the lake.
SCHEMAS = {
    "agents": [
        ("agent_sha", "VARCHAR"), ("canonical_name", "VARCHAR"),
        ("author", "VARCHAR"), ("lineage_id", "VARCHAR"),
        ("source_url", "VARCHAR"), ("license", "VARCHAR"),
        ("historical_public_score", "DOUBLE"),
        ("publication_date", "VARCHAR"),
        ("environment_version", "VARCHAR"), ("playable", "BOOLEAN"),
        ("runtime_safe", "BOOLEAN"), ("league_eligible", "BOOLEAN"),
        ("lineage_confidence", "DOUBLE"), ("lineage_method", "VARCHAR"),
        ("notes", "VARCHAR"), ("first_seen_utc", "TIMESTAMP"),
    ],
    "episodes": [
        ("episode_id", "BIGINT"), ("seed", "BIGINT"),
        ("create_time", "TIMESTAMP"), ("era_id", "VARCHAR"),
        ("environment_version", "VARCHAR"),
        ("agent_0_sha", "VARCHAR"), ("agent_1_sha", "VARCHAR"),
        ("pre_rating_0", "DOUBLE"), ("pre_rating_1", "DOUBLE"),
        ("post_rating_0", "DOUBLE"), ("post_rating_1", "DOUBLE"),
        ("rating_semantics", "VARCHAR"),
        ("score_0", "DOUBLE"), ("score_1", "DOUBLE"),
        ("cash_0", "BIGINT"), ("cash_1", "BIGINT"),
        ("winner", "VARCHAR"), ("reward_0", "DOUBLE"), ("reward_1", "DOUBLE"),
        ("source_dataset", "VARCHAR"), ("replay_available", "BOOLEAN"),
        ("stock_config", "BOOLEAN"), ("ingested_utc", "TIMESTAMP"),
    ],
    "turns": [
        ("episode_id", "BIGINT"), ("step", "INTEGER"), ("player", "INTEGER"),
        ("agent_sha", "VARCHAR"), ("day", "INTEGER"), ("hour", "INTEGER"),
        ("money", "BIGINT"), ("land_count", "INTEGER"),
        ("hands_count", "INTEGER"),
        ("n_sheep", "INTEGER"), ("n_cow", "INTEGER"), ("n_goose", "INTEGER"),
        ("n_structures", "INTEGER"),
        ("crop_wheat", "INTEGER"), ("crop_carrot", "INTEGER"),
        ("crop_tomato", "INTEGER"), ("crop_strawberry", "INTEGER"),
        ("crop_melon", "INTEGER"),
        ("shed_total", "INTEGER"), ("inv_total", "INTEGER"),
        ("market_inv_total", "INTEGER"),
        ("farmer_x", "INTEGER"), ("farmer_y", "INTEGER"),
        ("actions_json", "VARCHAR"),
    ],
    "experiments": [
        ("experiment_id", "VARCHAR"), ("created_utc", "TIMESTAMP"),
        ("parent_sha", "VARCHAR"), ("candidate_sha", "VARCHAR"),
        ("hypothesis", "VARCHAR"), ("seed_split", "VARCHAR"),
        ("opponent_population", "VARCHAR"), ("games", "INTEGER"),
        ("wins", "INTEGER"), ("losses", "INTEGER"), ("ties", "INTEGER"),
        ("win_rate", "DOUBLE"), ("wilson_lo", "DOUBLE"),
        ("wilson_hi", "DOUBLE"), ("runtime_max_ms", "DOUBLE"),
        ("decision", "VARCHAR"), ("notes", "VARCHAR"),
    ],
    "matches": [
        ("experiment_id", "VARCHAR"), ("run_id", "VARCHAR"),
        ("environment_version", "VARCHAR"),
        ("candidate_sha", "VARCHAR"), ("candidate_name", "VARCHAR"),
        ("opponent_sha", "VARCHAR"), ("opponent_name", "VARCHAR"),
        ("seed", "BIGINT"), ("seat", "INTEGER"),
        ("candidate_cash", "BIGINT"), ("opponent_cash", "BIGINT"),
        ("win", "INTEGER"), ("loss", "INTEGER"), ("tie", "INTEGER"),
        ("candidate_status", "VARCHAR"), ("opponent_status", "VARCHAR"),
        ("candidate_calls", "INTEGER"), ("opponent_calls", "INTEGER"),
        ("valid", "INTEGER"), ("invalid_reason", "VARCHAR"),
    ],
    "ratings": [
        ("agent_sha", "VARCHAR"), ("agent_name", "VARCHAR"),
        ("shadow_rating", "DOUBLE"), ("lo95", "DOUBLE"), ("hi95", "DOUBLE"),
        ("games", "INTEGER"), ("opponents", "INTEGER"),
        ("lineage_coverage", "DOUBLE"), ("seat_balance", "DOUBLE"),
        ("regime_coverage", "DOUBLE"), ("method", "VARCHAR"),
        ("computed_utc", "TIMESTAMP"),
    ],
    "counterfactuals": [
        ("cf_id", "VARCHAR"), ("episode_id", "BIGINT"), ("step", "INTEGER"),
        ("player", "INTEGER"), ("agent_sha", "VARCHAR"),
        ("macro_action", "VARCHAR"), ("branch_seed", "BIGINT"),
        ("final_cash", "BIGINT"), ("baseline_cash", "BIGINT"),
        ("delta_cash", "BIGINT"), ("outcome", "VARCHAR"),
        ("opponent_sha", "VARCHAR"), ("seed", "BIGINT"),
        ("created_utc", "TIMESTAMP"),
    ],
    "champion_history": [
        ("champion_id", "VARCHAR"), ("agent_sha", "VARCHAR"),
        ("agent_name", "VARCHAR"), ("parent_sha", "VARCHAR"),
        ("promoted_utc", "TIMESTAMP"), ("shadow_rating", "DOUBLE"),
        ("top_meta_record", "VARCHAR"), ("lineage_record", "VARCHAR"),
        ("sealed_result", "VARCHAR"), ("git_commit", "VARCHAR"),
    ],
}

DUCK_TYPES = {
    "VARCHAR": "VARCHAR", "BIGINT": "BIGINT", "INTEGER": "INTEGER",
    "DOUBLE": "DOUBLE", "BOOLEAN": "BOOLEAN", "TIMESTAMP": "TIMESTAMP",
}


def connect(read_only=False):
    import duckdb
    os.makedirs(LAKE, exist_ok=True)
    con = duckdb.connect(DB, read_only=read_only)
    return con


def ensure_dirs():
    for d in (LAKE, PARQUET, MANIFESTS, TMP):
        os.makedirs(d, exist_ok=True)
    for t in SCHEMAS:
        os.makedirs(os.path.join(PARQUET, t), exist_ok=True)


def create_tables(con):
    ensure_dirs()
    for table, cols in SCHEMAS.items():
        ddl = ", ".join(f'"{n}" {DUCK_TYPES[t]}' for n, t in cols)
        con.execute(f'CREATE TABLE IF NOT EXISTS "{table}" ({ddl})')
    # Views over the Parquet layer, so a query written once works against the
    # lake regardless of whether the DuckDB table has been refreshed. A view
    # cannot be created over a glob matching nothing, so an empty placeholder
    # view is installed until the first Parquet file exists.
    for table in SCHEMAS:
        p = os.path.join(PARQUET, table, "*.parquet").replace("\\", "/")
        if glob.glob(p):
            con.execute(
                f"CREATE OR REPLACE VIEW v_{table} AS "
                f"SELECT * FROM read_parquet('{p}', union_by_name=true)")
        else:
            cols = ", ".join(f'CAST(NULL AS {DUCK_TYPES[t]}) AS "{n}"'
                             for n, t in SCHEMAS[table])
            con.execute(
                f"CREATE OR REPLACE VIEW v_{table} AS "
                f'SELECT {cols} FROM "{table}" WHERE FALSE')
    con.execute(
        "CREATE OR REPLACE VIEW v_agent_episode_pairs AS "
        "SELECT e.episode_id, e.seed, e.create_time, e.environment_version, "
        "       e.source_dataset, "
        "       a0.canonical_name AS name_0, a0.agent_sha AS sha_0, "
        "       a1.canonical_name AS name_1, a1.agent_sha AS sha_1, "
        "       e.score_0, e.score_1, e.cash_0, e.cash_1, e.winner, "
        "       a0.lineage_id AS lineage_0, a1.lineage_id AS lineage_1 "
        "FROM v_episodes e "
        "LEFT JOIN v_agents a0 ON a0.agent_sha = e.agent_0_sha "
        "LEFT JOIN v_agents a1 ON a1.agent_sha = e.agent_1_sha")


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def row_count(con, table):
    try:
        return con.execute(f'SELECT count(*) FROM "{table}"').fetchone()[0]
    except Exception:
        return 0


def write_manifest(name, payload):
    ensure_dirs()
    p = os.path.join(MANIFESTS, f"{name}.json")
    payload = dict(payload)
    payload["written_utc"] = payload.get("written_utc") or _utc()
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(payload, fh, indent=2, sort_keys=True, default=str)
    return p


def _utc():
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)


def summarize(con):
    out = {}
    for t in SCHEMAS:
        pq = os.path.join(PARQUET, t)
        files = [f for f in os.listdir(pq)] if os.path.isdir(pq) else []
        out[t] = {"duckdb_rows": row_count(con, t), "parquet_files": len(files),
                  "columns": [c for c, _ in SCHEMAS[t]]}
    return out


def main():
    con = connect()
    create_tables(con)
    ensure_dirs()
    s = summarize(con)
    print("DATA LAKE INITIALISED")
    print(f"  db    : {os.path.relpath(DB, ROOT)}")
    print(f"  parquet: {os.path.relpath(PARQUET, ROOT)}")
    for t, v in s.items():
        print(f"  {t:<16} {v['duckdb_rows']:>8} rows  {len(v['columns']):>2} cols")
    write_manifest("lake_init", {"tables": s, "root": "data_lake"})
    print(f"\n  manifest -> data_lake/manifests/lake_init.json")
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
