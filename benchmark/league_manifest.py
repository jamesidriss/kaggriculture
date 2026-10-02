"""Emit `opponents/meta/MANIFEST.csv`: the authoritative league record.

One row per agent that may legally enter a competitive league, keyed by content
digest. The file answers, for every league member: what it is, where it came
from, who wrote it, what licence covers it, and whether it is a verbatim public
artifact or something we modified.

Written to disk and checked on every run, so a league cannot quietly gain an
agent with an unknown licence or an unrecorded edit.
"""
import csv
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META = os.path.join(ROOT, "opponents", "meta")
OUT = os.path.join(META, "MANIFEST.csv")

FIELDS = ["name", "sha256", "bytes", "path", "author", "license", "source",
          "verbatim", "lineage", "league_eligible", "reason"]

# Authoritative provenance. Populated from:
#   - Kaggle dataset destbreso/kaggriculture-donor-agents-20260902 (README
#     states the pack is "exactly as published by their authors, with
#     provenance, license")
#   - research/FINAL_PUBLIC_AGENT_CATALOG.csv
#   - reports/ARTIFACT_INVENTORY.md
PROV = {
    "ahmedberatozer-v43-recovering-lost-harvests": dict(
        author="ahmedberatozer", license="Apache-2.0", verbatim="yes",
        lineage="ahmedberatozer series v27-v51",
        source="kaggle dataset destbreso/kaggriculture-donor-agents-20260902"),
    "ahmedberatozer-v44-winning-the-same-turn-sale-race": dict(
        author="ahmedberatozer", license="Apache-2.0", verbatim="yes",
        lineage="ahmedberatozer series v27-v51",
        source="kaggle dataset destbreso/kaggriculture-donor-agents-20260902"),
    "ahmedberatozer-v46-first-turn-microstructure": dict(
        author="ahmedberatozer", license="Apache-2.0", verbatim="yes",
        lineage="ahmedberatozer series v27-v51",
        source="kaggle dataset destbreso/kaggriculture-donor-agents-20260902"),
    "ahmedberatozer-v48-clear-the-queue": dict(
        author="ahmedberatozer", license="Apache-2.0", verbatim="yes",
        lineage="ahmedberatozer series v27-v51",
        source="kaggle dataset destbreso/kaggriculture-donor-agents-20260902"),
    "ahmedberatozer-v49-funded-sale-timing": dict(
        author="ahmedberatozer", license="Apache-2.0", verbatim="yes",
        lineage="ahmedberatozer series v27-v51",
        source="kaggle dataset destbreso/kaggriculture-donor-agents-20260902"),
    "ahmedberatozer-v50-early-yarn-commit": dict(
        author="ahmedberatozer", license="Apache-2.0", verbatim="yes",
        lineage="ahmedberatozer series v27-v51",
        source="kaggle dataset destbreso/kaggriculture-donor-agents-20260902"),
    "ahmedberatozer-v51-lean-flock": dict(
        author="ahmedberatozer", license="Apache-2.0", verbatim="yes",
        lineage="ahmedberatozer series v27-v51",
        source="kaggle dataset destbreso/kaggriculture-donor-agents-20260902"),
    "v38_feed": dict(
        author="ahmedberatozer", license="stated-in-source", verbatim="yes",
        lineage="Ozer v28/v31 lineage",
        source="kaggle code ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins"),
    "farm_2945_original": dict(
        author="thomastschinkel", license="Apache-2.0", verbatim="yes",
        lineage="thomastschinkel + yhay81 + destbreso + aurax7 + tetsutani",
        source="kaggle code thomastschinkel/the-2945-farm-96-vs-the-top-10-public-bots"),
    "v16_rc5": dict(
        author="boatlee", license="stated-in-source", verbatim="yes",
        lineage="standalone",
        source="kaggle code boatlee/v16-rc5-high-score-8c-4s-premium-market-lead"),
    "shop_router": dict(
        author="yhay81", license="Apache-2.0", verbatim="yes",
        lineage="yhay81 router series",
        source="kaggle code yhay81/shop-router-0909"),
    "barnyard_v7": dict(
        author="romanrozen", license="NONE-STATED", verbatim="yes",
        lineage="standalone",
        source="kaggle code romanrozen/strong-barnyard-economist"),
}

INELIGIBLE_REASON = {
    "barnyard_v7": "UNKNOWN_LICENSE - no licence declared by the author; "
                   "excluded from competitive use",
}

# Present in research/public_src but deliberately NOT in opponents/meta, so the
# reason is recorded here rather than lost.
WITHHELD = {
    "shop_router": "NOT_SELF_CONTAINED - raises FileNotFoundError for "
                   "'actions.json' on its first turn; the file is not available "
                   "in the public notebook. Before the signature fix it silently "
                   "sat at the starting $3,000 and was recorded as a 72-0 "
                   "victim. Moved to opponents/unlicensed/.",
    "thomas_2944": "NOT_SELF_CONTAINED - RuntimeError at import; requires "
                   "\\kaggle/input",
    "three_day_router_native": "PLATFORM - agent.so is Linux/macOS only; "
                               "WinError 193 on this host, so unevaluable",
}


def main():
    files = sorted(f for f in os.listdir(META) if f.endswith(".py"))
    rows, problems = [], []
    seen = {}
    for f in files:
        name = f[:-3]
        p = os.path.join(META, f)
        raw = open(p, "rb").read()
        sha = hashlib.sha256(raw).hexdigest()
        # Normalised digest: CRLF vs LF must not create a phantom second agent.
        norm = hashlib.sha256(raw.decode("utf-8", "replace")
                              .replace("\r\n", "\n").encode()).hexdigest()
        if sha in seen:
            problems.append(f"{name}: byte-identical to {seen[sha]}")
        seen[norm] = name
        seen.setdefault(sha, name)

        prov = PROV.get(name)
        if not prov:
            problems.append(f"{name}: NO PROVENANCE RECORD - cannot enter a league")
            prov = dict(author="UNKNOWN", license="UNKNOWN", verbatim="?",
                        lineage="UNKNOWN", source="UNKNOWN")
        elig = "no" if name in INELIGIBLE_REASON else "yes"
        rows.append({
            "name": name, "sha256": sha, "bytes": len(raw),
            "path": f"opponents/meta/{f}",
            "author": prov["author"], "license": prov["license"],
            "source": prov["source"], "verbatim": prov["verbatim"],
            "lineage": prov["lineage"], "league_eligible": elig,
            "reason": INELIGIBLE_REASON.get(name, ""),
        })

    rows.sort(key=lambda r: r["name"])
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    elig = [r for r in rows if r["league_eligible"] == "yes"]
    print(f"wrote {os.path.relpath(OUT, ROOT)}: {len(rows)} agents, "
          f"{len(elig)} league-eligible")
    lic = {}
    for r in elig:
        lic.setdefault(r["license"], []).append(r["name"])
    for k, v in sorted(lic.items()):
        print(f"  {k}: {len(v)}")
    lineage = {}
    for r in elig:
        lineage.setdefault(r["lineage"], []).append(r["name"])
    print(f"\n  distinct lineages in the competitive league: {len(lineage)}")
    for k, v in sorted(lineage.items(), key=lambda kv: -len(kv[1])):
        print(f"    {len(v):>2}  {k}")
    print("\n  withheld (recorded here, absent from opponents/meta):")
    for k, v in sorted(WITHHELD.items()):
        print(f"    {k}: {v[:88]}...")

    soft = [p for p in problems if "byte-identical" in p]
    hard = [p for p in problems if p not in soft]
    for p in soft:
        print("  WARN  " + p)
    for p in hard:
        print("  FAIL  " + p)
    if not hard:
        print(f"\n  every league-eligible agent has author, licence and source")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
