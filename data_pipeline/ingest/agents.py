"""Load the agent registry into the lake, keyed strictly by artifact SHA256.

Identity is the digest. A name is an attribute. Two artifacts with identical
content collapse to one row; two names for one artifact are both recorded as
aliases, never as two agents.

Sources of truth, in order:
  1. `opponents/meta/MANIFEST.csv`      - the league, licence-gated
  2. `research/FINAL_PUBLIC_AGENT_CATALOG.csv` - the wider public catalog
  3. `postmortem_champion` / `postmortem_hedge` - the frozen references
  4. `challengers/challengers.json`     - research candidates

Lineage is a first-class column. `lineage_id` groups agents that share
strategy ancestry, and `lineage_method` records HOW we know that:
  - `provenance`  - the author or the source artifact states the ancestry
  - `code`        - measured code similarity (benchmark/lineage_check.py)
  - `behaviour`   - a behavioural fingerprint from public replays only
  - `declared`    - a naming convention with no independent evidence

The distinction matters: a behavioural grouping is a hypothesis about strategy
and must never be presented as proof of code ancestry.
"""
import csv
import hashlib
import json
import os
import sys

# This file lives at data_pipeline/ingest/agents.py, so the repository root is
# two directories up, not one. Getting this wrong silently resolves every
# artifact path to nothing and ingests zero agents without an error.
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "data_pipeline"))

from lake import connect, create_tables, write_manifest, _utc  # noqa: E402

MANIFEST = os.path.join(ROOT, "opponents", "meta", "MANIFEST.csv")
CATALOG = os.path.join(ROOT, "research", "FINAL_PUBLIC_AGENT_CATALOG.csv")
CHAMP = os.path.join(ROOT, "postmortem_champion", "main.py")
HEDGE = os.path.join(ROOT, "postmortem_hedge", "main.py")
CHALL = os.path.join(ROOT, "challengers", "challengers.json")

# Lineage assignment, with the evidence for each. The Ozer/2945 group is
# measured, not assumed: benchmark/lineage_check.py found 1,205 shared
# identifiers, containment 0.818 and one contiguous identical run of 3,352
# tokens between v51 and the 2945 Farm, with an identical nine-author credit
# list. Everything downstream inherits that ancestry.
LINEAGE_OF = {
    "ahmedberatozer-v51-lean-flock": ("L-OZER-2945", 0.95, "code+provenance"),
    "farm_2945_original": ("L-OZER-2945", 0.95, "code+provenance"),
    "ahmedberatozer-v49-funded-sale-timing": ("L-OZER-2945", 0.9, "provenance"),
    "ahmedberatozer-v50-early-yarn-commit": ("L-OZER-2945", 0.9, "provenance"),
    "ahmedberatozer-v48-clear-the-queue": ("L-OZER-2945", 0.9, "provenance"),
    "ahmedberatozer-v46-first-turn-microstructure": ("L-OZER-2945", 0.9, "provenance"),
    "ahmedberatozer-v44-winning-the-same-turn-sale-race": ("L-OZER-2945", 0.9, "provenance"),
    "ahmedberatozer-v43-recovering-lost-harvests": ("L-OZER-2945", 0.9, "provenance"),
    "v38_feed": ("L-OZER-2945", 0.85, "provenance"),
    "v16_rc5": ("L-BOATLEE", 0.95, "code+provenance"),
    "barnyard_v7": ("L-ROMANROZEN", 0.9, "provenance"),
    "sunrise_v5": ("L-SUNRISE", 0.99, "provenance"),
    "sunrise_v4": ("L-SUNRISE", 0.99, "provenance"),
    "shop_router": ("L-YHAY81", 0.9, "provenance"),
    "thomas_2944": ("L-STATMA", 0.7, "declared"),
    "three_day_router_native": ("L-YHAY81", 0.7, "declared"),
}
DEFAULT_LINEAGE = ("L-UNKNOWN", 0.0, "none")


def sha256(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def resolve_path(rel):
    if os.path.isabs(rel):
        return rel
    p = os.path.join(ROOT, rel)
    if os.path.isdir(p):
        p = os.path.join(p, "main.py")
    return p


def collect():
    """Return {sha: {...}} from every known source, digests recomputed."""
    agents = {}

    def put(sha, **kw):
        rec = agents.setdefault(sha, {})
        rec.update({k: v for k, v in kw.items() if v not in (None, "")})
        aliases = rec.setdefault("aliases", [])
        n = kw.get("canonical_name")
        if n and n not in aliases:
            aliases.append(n)

    if os.path.exists(MANIFEST):
        for r in csv.DictReader(open(MANIFEST, encoding="utf-8")):
            p = resolve_path(r["path"])
            if not os.path.exists(p):
                continue
            sha = sha256(p)
            lin, conf, meth = LINEAGE_OF.get(r["name"], DEFAULT_LINEAGE)
            put(sha, canonical_name=r["name"], author=r.get("author", ""),
                license=r.get("license", ""), source_url=r.get("source", ""),
                lineage_id=lin, lineage_confidence=conf, lineage_method=meth,
                playable=True, runtime_safe=True,
                league_eligible=(r.get("league_eligible") == "yes"),
                path=os.path.relpath(p, ROOT).replace("\\", "/"),
                notes=r.get("reason", ""))

    if os.path.exists(CATALOG):
        for r in csv.DictReader(open(CATALOG, encoding="utf-8")):
            p = resolve_path(r.get("path", ""))
            if not os.path.exists(p):
                continue
            sha = sha256(p)
            lin, conf, meth = LINEAGE_OF.get(r["agent_name"], DEFAULT_LINEAGE)
            put(sha, canonical_name=r["agent_name"], author=r.get("author", ""),
                license=r.get("license", ""), lineage_id=lin,
                lineage_confidence=conf, lineage_method=meth,
                playable=(r.get("playable") == "yes"),
                league_eligible=(r.get("league_eligible") == "yes"),
                path=os.path.relpath(p, ROOT).replace("\\", "/"),
                notes=r.get("notes", ""))

    for p, name in ((CHAMP, "ahmedberatozer-v51-lean-flock"),
                    (HEDGE, "farm_2945_original")):
        if os.path.exists(p):
            lin, conf, meth = LINEAGE_OF[name]
            put(sha256(p), canonical_name=name, lineage_id=lin,
                lineage_confidence=conf, lineage_method=meth, playable=True,
                league_eligible=True, path=os.path.relpath(p, ROOT).replace("\\", "/"),
                author=("ahmedberatozer" if "v51" in name else "thomastschinkel"),
                license="Apache-2.0", notes="frozen postmortem reference")

    if os.path.exists(CHALL):
        for c in json.load(open(CHALL, encoding="utf-8"))["challengers"]:
            p = os.path.join(ROOT, c["path"])
            if not os.path.exists(p):
                continue
            put(sha256(p), canonical_name=c["tag"], lineage_id="L-OZER-2945",
                lineage_confidence=0.99, lineage_method="code+provenance",
                playable=True, league_eligible=False,
                path=c["path"], notes=f"challenger: {c['hypothesis'][:80]}")
    return agents


def load(verbose=True):
    con = connect()
    create_tables(con)
    have = {r[0] for r in con.execute("SELECT agent_sha FROM agents").fetchall()}
    data = collect()
    rows = []
    for sha, r in data.items():
        if sha in have:
            continue
        lin = r.get("lineage_id", DEFAULT_LINEAGE[0])
        rows.append((
            sha, r.get("canonical_name", sha[:12]),
            r.get("author", ""), lin, r.get("source_url", ""),
            r.get("license", ""), r.get("historical_public_score"),
            r.get("publication_date", ""), r.get("environment_version",
                                                  "kaggle-environments 1.32.7"),
            bool(r.get("playable", False)), bool(r.get("runtime_safe", False)),
            bool(r.get("league_eligible", False)),
            r.get("lineage_confidence", DEFAULT_LINEAGE[1]),
            r.get("lineage_method", DEFAULT_LINEAGE[2]),
            r.get("notes", ""), _utc(),
        ))
    if rows:
        ph = ", ".join(["?"] * len(rows[0]))
        con.executemany(f"INSERT INTO agents VALUES ({ph})", rows)

    total = con.execute("SELECT count(*) FROM agents").fetchone()[0]
    lin = con.execute(
        "SELECT lineage_id, count(*) n, sum(CASE WHEN league_eligible "
        "THEN 1 ELSE 0 END) elig FROM agents GROUP BY 1 ORDER BY n DESC"
    ).fetchall()
    stats = {"unique_agents": total, "inserted_now": len(rows),
             "lineages": [{"lineage_id": a, "agents": b, "eligible": c}
                          for a, b, c in lin]}
    write_manifest("ingest_agents", stats)
    if verbose:
        print(f"  unique artifacts : {total}")
        print(f"  inserted now     : {len(rows)}")
        for r in lin:
            print(f"    {r[0]:<16} agents={r[1]:<3} eligible={r[2]}")
    con.close()
    return stats


if __name__ == "__main__":
    print("INGEST: agent registry")
    load()
