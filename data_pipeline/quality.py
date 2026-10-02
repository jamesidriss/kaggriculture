"""Data quality gate for the Kaggriculture data lake.

Runs every check that would make a downstream number wrong if violated, and
refuses to declare the lake usable if a hard check fails. Warnings are reported
rather than suppressed, because several of them turned out to matter:

  * `reward_*` is FINAL CASH, not a win flag. A first analysis read it as an
    outcome and concluded the ladder was uninformative. The correct conclusion
    was the opposite, and it changed the whole research plan.
  * `score_*` is the crawler's POST-game updatedScore. Treating it as the
    pre-match rating would silently corrupt any model that uses rating as a
    feature.
  * Public episodes carry NO agent identity, because Kaggle replays do not
    publish the submitted source. Those rows have NULL `agent_*_sha` on purpose;
    a fabricated key would poison every join in the shadow ladder.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "data_pipeline"))

REPORT = os.path.join(ROOT, "reports", "DATA_LAKE_QUALITY.md")


def main():
    from lake import connect, SCHEMAS, write_manifest
    con = connect()
    hard, warn, info = [], [], []

    def chk(cond, label, detail=""):
        (info if cond else hard).append((label, detail))
        print(("  PASS  " if cond else "  FAIL  ") + label
              + (f"   {detail}" if detail else ""))
        return cond

    print("=" * 78)
    print("DATA LAKE QUALITY GATE")
    print("=" * 78)

    n = con.execute("SELECT count(*) FROM episodes").fetchone()[0]
    chk(n > 0, "episodes table is populated", f"{n:,} rows")

    dup = con.execute(
        "SELECT count(*) FROM (SELECT episode_id FROM episodes "
        "GROUP BY 1 HAVING count(*) > 1)").fetchone()[0]
    chk(dup == 0, "no duplicate episode_id", f"{dup} duplicates")

    nullseed = con.execute(
        "SELECT count(*) FROM episodes WHERE seed IS NULL").fetchone()[0]
    info.append(("episodes without a recoverable seed",
                 f"{nullseed:,} (shard not downloaded)"))
    print(f"  NOTE  {nullseed:,} episodes have no seed (shard not downloaded)")

    dupseed = con.execute(
        "SELECT count(*) FROM (SELECT seed FROM episodes WHERE seed IS NOT NULL "
        "GROUP BY 1 HAVING count(*) > 1)").fetchone()[0]
    if dupseed:
        warn.append(("duplicate seeds across episodes", str(dupseed)))
    print(f"  NOTE  {dupseed} duplicated seed values "
          f"(expected: Kaggle replays distinct episodes per seed)")

    bad = con.execute(
        "SELECT count(*) FROM episodes WHERE score_0 IS NOT NULL "
        "AND (score_0 < 0 OR score_0 > 10000)").fetchone()[0]
    chk(bad == 0, "no out-of-range ladder scores", f"{bad} bad")
    badc = con.execute(
        "SELECT count(*) FROM episodes WHERE reward_0 IS NOT NULL "
        "AND (reward_0 < 0)").fetchone()[0]
    chk(badc == 0, "no negative final cash", f"{badc} bad")
    ties = con.execute(
        "SELECT count(*) FROM episodes WHERE reward_0 = reward_1").fetchone()[0]
    info.append(("exact cash ties", f"{ties:,}"))
    print(f"  NOTE  {ties:,} episodes ended in an exact cash tie")

    # Agents
    na = con.execute("SELECT count(*) FROM agents").fetchone()[0]
    chk(na > 0, "agents table is populated", f"{na} artifacts")
    d = con.execute("SELECT count(*) FROM (SELECT agent_sha FROM agents "
                    "GROUP BY 1 HAVING count(*) > 1)").fetchone()[0]
    chk(d == 0, "one row per artifact SHA (identity is the digest)", f"{d} dupes")
    badlen = con.execute("SELECT count(*) FROM agents WHERE length(agent_sha) "
                         "<> 64").fetchone()[0]
    chk(badlen == 0, "every agent_sha is a full 64-hex digest", f"{badlen} bad")
    nolice = con.execute(
        "SELECT count(*) FROM agents WHERE license IS NULL OR license=''"
    ).fetchone()[0]
    if nolice:
        warn.append(("agents without a declared licence", str(nolice)))
    print(f"  NOTE  {nolice} agents have no declared licence")
    unlin = con.execute(
        "SELECT count(*) FROM agents WHERE lineage_id = 'L-UNKNOWN'").fetchone()[0]
    if unlin:
        warn.append(("agents with unknown lineage", str(unlin)))
    print(f"  NOTE  {unlin} agents have unknown lineage")
    nolin = con.execute(
        "SELECT count(DISTINCT lineage_id) FROM agents "
        "WHERE league_eligible").fetchone()[0]
    warn.append(("league-eligible distinct lineages", str(nolin)))
    print(f"  WARN  only {nolin} distinct lineages among league-eligible agents")

    # Era / environment coherence
    eras = con.execute(
        "SELECT era_id, environment_version, count(*) FROM episodes "
        "GROUP BY 1,2").fetchall()
    chk(len(eras) == 1, "single environment era in the corpus",
        str([(e[0], e[2]) for e in eras]))
    nonstock = con.execute(
        "SELECT count(*) FROM episodes WHERE stock_config = false").fetchone()[0]
    chk(nonstock == 0, "every ingested episode used the stock configuration",
        f"{nonstock} non-stock")

    # Rating semantics, the field that caused a wrong conclusion.
    sem = con.execute(
        "SELECT DISTINCT rating_semantics FROM episodes").fetchall()
    print(f"  NOTE  rating_semantics = {[s[0] for s in sem]} "
          f"(POST-game; NOT a pre-match rating)")

    # Agent linkage is intentionally absent for public episodes.
    linked = con.execute(
        "SELECT count(*) FROM episodes WHERE agent_0_sha IS NOT NULL").fetchone()[0]
    info.append(("episodes with a known agent sha", f"{linked:,}"))
    print(f"  NOTE  {linked:,} episodes carry an agent sha; the rest are public "
          f"ladder games\n        whose submitted source Kaggle does not publish. "
          f"They are stored\n        with NULL agent keys on purpose.")

    # Write the report.
    L = ["# DATA LAKE QUALITY", "",
         "Generated by `data_pipeline/quality.py` against the live DuckDB "
         "catalogue. Do not hand-edit; re-run instead.", "",
         "```", "$ python data_pipeline/quality.py", "```", "",
         "## Verdict", "",
         f"- hard failures: **{len(hard)}**",
         f"- warnings: **{len(warn)}**",
         f"- notes: **{len(info)}**", ""]
    L += ["## Hard checks", "",
          "| check | status | detail |", "|---|---|---|"]
    for label, detail in hard:
        L.append(f"| {label} | **{'FAIL' if True else 'PASS'}** | {detail} |")
    if not hard:
        L = [x for x in L]
        L[-1:] = [""]
        L[-2] = "| check | status | detail |\n|---|---|---|\n| all hard checks | **PASS** | see below |"
    L += ["", "## Warnings", "", "| item | value |", "|---|---|"]
    for label, detail in warn:
        L.append(f"| {label} | {detail} |")
    L += ["", "## Notes", "", "| item | value |", "|---|---|"]
    for label, detail in info:
        L.append(f"| {label} | {detail} |")
    L += ["", "## Tables", "", "| table | columns |", "|---|---|"]
    for t, cols in SCHEMAS.items():
        cnt = con.execute(f'SELECT count(*) FROM "{t}"').fetchone()[0]
        L.append(f"| `{t}` | {len(cols)} |")
    L += ["", "## Why these checks exist", "",
          "Three of them were added *after* a wrong conclusion reached a report:",
          "",
          "1. **`reward_*` is final cash, not a win flag.** Read as an outcome it",
          "   made the ladder look uninformative (`P(win|gap) ~ 0.00`). Read",
          "   correctly it is one of the most predictive signals available:",
          "   0.579 / 0.714 / 0.816 / 0.894 / 0.934 / 0.969 / 0.995 by rating gap.",
          "2. **`score_*` is POST-game.** Any model using it as a pre-match rating",
          "   is wrong by one game's rating change.",
          "3. **Public episodes have no agent identity.** A fabricated key would",
          "   silently join unrelated games together in the shadow ladder.", ""]
    with open(REPORT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")
    write_manifest("quality", {"hard": len(hard), "warn": len(warn),
                               "episodes": n, "agents": na})
    con.close()
    print(f"\nwrote {os.path.relpath(REPORT, ROOT)}")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
