"""Build an immutable, digest-addressed opponent store.

Prevents the class of bug where a league file is silently overwritten by a
different agent. Every agent is written to
    opponents/store/<sha256[:16]>/main.py   (+ sibling bundle files)
and recorded in opponents/store/MANIFEST.csv.

A duplicate digest can never create a second directory, so a "different"
opponent that is byte-identical to another cannot be registered.

Usage:
  python benchmark/opponent_store.py add <name> <file> --source URL --license L --score S
  python benchmark/opponent_store.py verify
  python benchmark/opponent_store.py list
"""
import argparse
import csv
import hashlib
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STORE = os.path.join(ROOT, "opponents", "store")
MANIFEST = os.path.join(STORE, "MANIFEST.csv")
COLS = ["name", "sha256", "source", "license", "score", "path", "notes"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def add(name, src, source="", license_="", score="", notes="", siblings=None):
    os.makedirs(STORE, exist_ok=True)
    h = sha(src)
    dest_dir = os.path.join(STORE, h[:16])
    os.makedirs(dest_dir, exist_ok=True)
    shutil.copy2(src, os.path.join(dest_dir, "main.py"))
    for s in (siblings or []):
        shutil.copy2(s, os.path.join(dest_dir, os.path.basename(s)))
    rel = os.path.relpath(dest_dir, ROOT).replace("\\", "/")
    rows = []
    if os.path.exists(MANIFEST):
        rows = list(csv.DictReader(open(MANIFEST, encoding="utf-8")))
    rows = [r for r in rows if r["sha256"] != h]
    rows.append({"name": name, "sha256": h, "source": source,
                 "license": license_, "score": score, "path": rel, "notes": notes})
    rows.sort(key=lambda r: -int(r["sha256"][:8], 16))
    with open(MANIFEST, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    print(f"registered {name} sha={h[:16]} path={rel}")
    return h


def verify():
    if not os.path.exists(MANIFEST):
        print("no manifest")
        return 1
    rows = list(csv.DictReader(open(MANIFEST, encoding="utf-8")))
    digests = {}
    bad = 0
    print(f"{'name':26s} {'sha256':18s} unique license")
    for r in rows:
        p = os.path.join(ROOT, r["path"], "main.py")
        ok = os.path.exists(p) and sha(p) == r["sha256"]
        uniq = r["sha256"] not in digests
        digests.setdefault(r["sha256"], r["name"])
        lic = "yes" if r["license"] and r["license"].lower() not in ("", "unknown", "none") else "NO"
        print(f"{r['name'][:26]:26s} {r['sha256'][:16]:18s} {'yes ' if uniq else 'DUP '}    {lic}")
        if not ok or not uniq:
            bad += 1
    print(f"\n{len(rows)} agents, {len(digests)} unique digests, {bad} problem(s)")
    return 1 if bad else 0


def listing():
    if not os.path.exists(MANIFEST):
        return
    for r in csv.DictReader(open(MANIFEST, encoding="utf-8")):
        print(f"{r['name']:26s} {r['sha256'][:16]} {r['license'][:18]:20s} {r['path']}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("name"); a.add_argument("file")
    a.add_argument("--source", default=""); a.add_argument("--license", default="")
    a.add_argument("--score", default=""); a.add_argument("--notes", default="")
    a.add_argument("--sibling", action="append", default=[])
    sub.add_parser("verify")
    sub.add_parser("list")
    args = ap.parse_args()
    if args.cmd == "add":
        add(args.name, args.file, args.source, args.license, args.score,
            args.notes, args.sibling)
    elif args.cmd == "verify":
        sys.exit(verify())
    else:
        listing()