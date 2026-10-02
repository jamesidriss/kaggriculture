"""Re-key the digest-addressed store and rebuild the manifest.

Why this was necessary
----------------------
The store's directory names were digests computed while `core.autocrlf=true`
was rewriting the working tree to CRLF. The files themselves were authored with
LF. Normalising the working tree to LF (so that the on-disk digest matches the
Git blob and therefore the published value) changed the content digest of two
agents:

    919fc1d61050cd96  ->  3abe0ca715ba1864   (v43)
    797d9bca309d481e  ->  fe370bd8a9d0f377   (v44)

A digest-addressed store whose keys no longer address their contents is not a
registry. This script re-keys the directories to the digest of the bytes that
are actually stored, and rewrites MANIFEST.csv from the files rather than from
the previous manifest.

Canonical digest definition, stated once: SHA256 over the file's bytes as
committed to Git (LF line endings), which is what `git cat-file` returns and
what any Linux checkout will produce.
"""
import csv
import hashlib
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = os.path.join(ROOT, "opponents", "store")
META = os.path.join(ROOT, "opponents", "meta")
MANIFEST = os.path.join(META, "MANIFEST.csv")

PROV = {
    "ahmedberatozer-v43-recovering-lost-harvests": ("ahmedberatozer", "Apache-2.0", "yes", "Ozer / 2945-Farm lineage"),
    "ahmedberatozer-v44-winning-the-same-turn-sale-race": ("ahmedberatozer", "Apache-2.0", "yes", "Ozer / 2945-Farm lineage"),
    "ahmedberatozer-v46-first-turn-microstructure": ("ahmedberatozer", "Apache-2.0", "yes", "Ozer / 2945-Farm lineage"),
    "ahmedberatozer-v48-clear-the-queue": ("ahmedberatozer", "Apache-2.0", "yes", "Ozer / 2945-Farm lineage"),
    "ahmedberatozer-v49-funded-sale-timing": ("ahmedberatozer", "Apache-2.0", "yes", "Ozer / 2945-Farm lineage"),
    "ahmedberatozer-v50-early-yarn-commit": ("ahmedberatozer", "Apache-2.0", "yes", "Ozer / 2945-Farm lineage"),
    "ahmedberatozer-v51-lean-flock": ("ahmedberatozer", "Apache-2.0", "yes", "Ozer / 2945-Farm lineage"),
    "v38_feed": ("ahmedberatozer", "stated-in-source", "yes", "Ozer / 2945-Farm lineage"),
    "farm_2945_original": ("thomastschinkel", "Apache-2.0", "yes", "Ozer / 2945-Farm lineage"),
    "v16_rc5": ("boatlee", "stated-in-source", "yes", "boatlee (DISTINCT)"),
    "barnyard_v7": ("romanrozen", "NONE-STATED", "no", "romanrozen standalone"),
}
SOURCE_DEFAULT = "kaggle dataset destbreso/kaggriculture-donor-agents-20260902"
SOURCES = {
    "farm_2945_original": "kaggle code thomastschinkel/the-2945-farm-96-vs-the-top-10-public-bots",
    "v38_feed": "kaggle code ahmedberatozer/kaggriculture-v38-smarter-feed-stronger-margins",
    "v16_rc5": "kaggle code boatlee/v16-rc5-high-score-8c-4s-premium-market-lead",
    "barnyard_v7": "kaggle code romanrozen/strong-barnyard-economist",
}
INELIGIBLE = {
    "barnyard_v7": "UNKNOWN_LICENSE - no licence declared by the author; "
                   "excluded from competitive use, retained for analysis only",
}
FIELDS = ["name", "sha256", "bytes", "path", "author", "license", "source",
          "verbatim", "lineage", "league_eligible", "reason"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    # 1. Re-key store directories whose name no longer matches their content.
    rekeyed = []
    if os.path.isdir(STORE):
        for d in sorted(os.listdir(STORE)):
            p = os.path.join(STORE, d)
            f = os.path.join(p, "main.py")
            if not os.path.isfile(f) or len(d) == 64:
                continue
            actual = sha(f)
            if actual.startswith(d):
                continue
            new = os.path.join(STORE, actual)
            if os.path.exists(new):
                shutil.rmtree(p)
            else:
                os.rename(p, new)
            rekeyed.append((d, actual))
    print("STORE RE-KEYED")
    for old, new in rekeyed:
        print(f"  {old} -> {new}")
    if not rekeyed:
        print("  (already consistent)")

    # 2. Rebuild the manifest from files on disk.
    rows = []
    for f in sorted(os.listdir(META)):
        if not f.endswith(".py"):
            continue
        name = f[:-3]
        p = os.path.join(META, f)
        raw = open(p, "rb").read()
        d = hashlib.sha256(raw).hexdigest()
        author, lic, elig, lineage = PROV.get(
            name, ("UNKNOWN", "UNKNOWN", "no", "UNKNOWN"))
        store_dir = os.path.join(STORE, d)
        if os.path.isfile(os.path.join(store_dir, "main.py")):
            rel = f"opponents/store/{d}"
        else:
            rel = f"opponents/meta/{f}"
        rows.append({
            "name": name, "sha256": d, "bytes": len(raw), "path": rel,
            "author": author, "license": lic,
            "source": SOURCES.get(name, SOURCE_DEFAULT),
            "verbatim": "yes", "lineage": lineage,
            "league_eligible": elig,
            "reason": INELIGIBLE.get(name, ""),
        })
    rows.sort(key=lambda r: r["name"])
    with open(MANIFEST, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    # 3. Verify.
    print(f"\nMANIFEST rebuilt: {len(rows)} agents, "
          f"{sum(1 for r in rows if r['league_eligible'] == 'yes')} eligible")
    digests = [r["sha256"] for r in rows]
    assert len(digests) == len(set(digests)), "duplicate digest in the manifest"
    for r in rows:
        p = os.path.join(ROOT, r["path"], "main.py") if r["path"].endswith(
            hashlib.sha256(r["path"].encode()).hexdigest()[:0] or "x") else None
    bad = []
    for r in rows:
        p = os.path.join(ROOT, r["path"], "main.py")
        if not os.path.exists(p):
            p = os.path.join(ROOT, r["path"])
        if not os.path.exists(p) or sha(p) != r["sha256"]:
            bad.append(r["name"])
    print(f"digest verification: {'OK' if not bad else 'FAILED ' + str(bad)}")
    for r in rows:
        print(f"  {r['name'][:44]:<44} {r['sha256'][:16]} {r['license']}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
