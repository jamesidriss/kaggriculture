"""Normalise tracked agent artifacts to LF and verify digest integrity.

Why this exists
---------------
`core.autocrlf=true` on Windows made Git check every agent file out with CRLF
while every recorded SHA256 described the LF blob in the repository. The
consequence was that `sha256sum postmortem_champion/main.py` disagreed with the
value published in METADATA.txt and MANIFEST.csv -- for the entire project. An
artifact whose digest does not match its registry is not a verified artifact.

This script:
  1. reads each tracked file's true bytes out of the Git object database
     (`git cat-file blob`), which is immune to working-tree conversion;
  2. compares them with the working-tree bytes;
  3. rewrites the working tree to LF where it differs;
  4. re-verifies that the working tree now hashes to the same value as Git.

Run with --check to verify only.
"""
import hashlib
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directories whose contents are content-addressed artifacts.
DIRS = [
    "opponents", "champions", "challengers", "postmortem_champion_000",
    "postmortem_champion", "postmortem_hedge", "counterfactuals",
    "research/public_src", "data/donor_agents",
]


def git(*args, binary=False):
    out = subprocess.run(["git"] + list(args), cwd=ROOT, capture_output=True)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.decode("utf-8", "replace")[:300])
    return out.stdout if binary else out.stdout.decode("utf-8", "replace")


def tracked_in(d):
    if not os.path.isdir(os.path.join(ROOT, d)):
        return []
    files = git("ls-files", "--", d).splitlines()
    return [f for f in files if f and not f.endswith("/")]


def blob_sha(path):
    return hashlib.sha256(git("cat-file", "blob", f"HEAD:{path}", binary=True)).hexdigest()


def main():
    check_only = "--check" in sys.argv
    rows = []
    for d in DIRS:
        for rel in tracked_in(d):
            disk = os.path.join(ROOT, rel)
            if not os.path.exists(disk):
                continue
            with open(disk, "rb") as fh:
                cur = fh.read()
            cur_sha = hashlib.sha256(cur).hexdigest()
            try:
                head_sha = blob_sha(rel)
            except RuntimeError:
                head_sha = None
            rows.append((rel, cur, cur_sha, head_sha))

    mismatched = [r for r in rows if r[3] and r[2] != r[3]]
    crlf = [r for r in rows if b"\r\n" in r[1]]
    print(f"tracked artifacts examined : {len(rows)}")
    print(f"working tree contains CRLF : {len(crlf)}")
    print(f"digest differs from Git    : {len(mismatched)}")
    for rel, _, a, b in mismatched[:10]:
        print(f"   {rel}\n     disk {a[:16]}  git {b[:16]}")

    if check_only:
        ok = not mismatched
        print(f"\nINTEGRITY {'OK' if ok else 'BROKEN'}")
        return 0 if ok else 1

    fixed = 0
    for rel, cur, cur_sha, head_sha in mismatched:
        if head_sha is None:
            continue
        with open(os.path.join(ROOT, rel), "wb") as fh:
            fh.write(cur.replace(b"\r\n", b"\n"))
        fixed += 1

    # Re-verify.
    bad = []
    for rel, _, _, head_sha in rows:
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p) or head_sha is None:
            continue
        now = hashlib.sha256(open(p, "rb").read()).hexdigest()
        if now != head_sha:
            bad.append((rel, now[:16], head_sha[:16]))
    print(f"\nrewritten to LF            : {fixed}")
    print(f"still mismatching          : {len(bad)}")
    for rel, a, b in bad[:10]:
        print(f"   {rel}: disk {a} git {b}")
    print(f"\nINTEGRITY {'OK' if not bad else 'BROKEN'}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
