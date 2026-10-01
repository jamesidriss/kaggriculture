"""Query the public replay DB for elite games, teams, and ladder seeds."""
import sys

import pyarrow.parquet as pq
import pandas as pd

DB = "data/replay_db"


def load():
    t = pq.read_table(f"{DB}/index/episodes_index.parquet").to_pandas()
    teams = pq.read_table(f"{DB}/index/teams.parquet").to_pandas()
    return t, dict(zip(teams.team_id, teams.team_name))


def top_teams(n=20):
    t, tn = load()
    a = t[["team_id_0", "score_0"]].rename(columns={"team_id_0": "team", "score_0": "score"})
    b = t[["team_id_1", "score_1"]].rename(columns={"team_id_1": "team", "score_1": "score"})
    best = pd.concat([a, b]).groupby("team")["score"].max().sort_values(ascending=False).head(n)
    for tm, sc in best.items():
        name = str(tn.get(tm, "?")).encode("ascii", "replace").decode()
        print(f"{tm} {name[:36]:38s} {sc:.1f}")


def elite_seeds(min_score=2900, n=24):
    """Episode IDs + seeds from games where BOTH players >= min_score."""
    import glob, json
    import zstandard as zstd
    t, _ = load()
    e = t[(t.score_0 >= min_score) & (t.score_1 >= min_score)]
    e = e.sort_values("create_time", ascending=False).head(n * 3)
    print(f"elite games both>={min_score}: {len(t[(t.score_0>=min_score)&(t.score_1>=min_score)])}, "
          f"sampling {len(e)} recent")
    loc = {}
    for s in sorted(glob.glob(f"{DB}/shards/ep_*.parquet")):
        for eid in pq.read_table(s, columns=["episode_id"]).column(0).to_pylist():
            loc[eid] = s
    out = []
    for _, r in e.iterrows():
        s = loc.get(r["episode_id"])
        if not s:
            continue
        row = pq.read_table(s, filters=[("episode_id", "=", r["episode_id"])]).to_pylist()[0]
        out.append((r["episode_id"], row["seed"], r["score_0"], r["score_1"],
                    r["reward_0"], r["reward_1"]))
        if len(out) >= n:
            break
    for o in out:
        print(f"{o[0]} seed={o[1]} scores={o[2]:.0f}/{o[3]:.0f} cash={o[4]:.0f}/{o[5]:.0f}")
    return out


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "teams":
        top_teams(int(sys.argv[2]) if len(sys.argv) > 2 else 20)
    else:
        elite_seeds(float(sys.argv[1]) if len(sys.argv) > 1 else 2900,
                    int(sys.argv[2]) if len(sys.argv) > 2 else 24)