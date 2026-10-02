"""Materialise opponents/meta from the digest-addressed store.

Single source of truth: opponents/store/MANIFEST.csv. Copying is derived, never
hand-written, so a league file can never drift from a registered digest.
"""
import csv
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = os.path.join(ROOT, "opponents", "store", "MANIFEST.csv")
OUT = os.path.join(ROOT, "opponents", "meta")

# Deliberately excludes anything whose digest equals the champion's; those are
# the champion's own twins and must never enter a league.
EXCLUDE = {"farm_2945_SEATSAFE", "farm_2945_ORIG", "tdr_native"}


def main():
    rows = list(csv.DictReader(open(MAN, encoding="utf-8")))
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for r in rows:
        if r["name"] in EXCLUDE:
            continue
        src = os.path.join(ROOT, r["path"], "main.py")
        dst = os.path.join(OUT, r["name"] + ".py")
        if not os.path.exists(src):
            print(f"  MISSING {r['name']}: {src}")
            continue
        shutil.copy2(src, dst)
        n += 1
    print(f"materialised {n} league files into opponents/meta")
    print("excluded (champion twins / unevaluable):", ", ".join(sorted(EXCLUDE)))
    # Report digests for the record.
    import hashlib
    for f in sorted(os.listdir(OUT)):
        if f.endswith(".py"):
            h = hashlib.sha256(open(os.path.join(OUT, f), "rb").read()).hexdigest()[:16]
            print(f"  {f[:-3]:<40} {h}")


if __name__ == "__main__":
    sys.exit(main())