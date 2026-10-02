"""Locate extractable agent source in final-week Kaggle notebooks.

The existing extractor only matches `^def agent(` at the start of a line and
`%%writefile`. Several final-week notebooks indent the definition or embed it in
a differently-shaped cell, so a broader scan is used to decide whether a
lineage is obtainable at all before spending time on it.
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATS = [
    ("writefile", re.compile(r"%%writefile", re.I)),
    ("def agent", re.compile(r"^\s*def\s+agent\s*\(", re.M)),
    ("agent assign", re.compile(r"^\s*agent\s*=\s*", re.M)),
    ("run fn", re.compile(r"^\s*def\s+(run|act|choose_action|policy)\s*\(", re.M)),
]


def scan(path):
    nb = json.load(open(path, encoding="utf-8"))
    out = []
    for i, c in enumerate(nb.get("cells", [])):
        if c.get("cell_type") != "code":
            continue
        s = "".join(c.get("source", []))
        if not s.strip():
            continue
        kinds = [name for name, rx in PATS if rx.search(s)]
        if kinds:
            out.append((i, kinds, len(s), s))
    return out


def main():
    pats = sys.argv[1:] or [os.path.join(ROOT, "research", "public_src",
                                         "final_week", "*", "*.ipynb")]
    files = []
    for p in pats:
        files += glob.glob(p)
    for f in sorted(files):
        name = os.path.basename(os.path.dirname(f))
        try:
            hits = scan(f)
        except Exception as exc:  # noqa: BLE001
            print(f"{name[:46]:<46} ERROR {exc}")
            continue
        if not hits:
            print(f"{name[:46]:<46} NO extractable agent cell")
            continue
        for i, kinds, n, s in hits[:4]:
            print(f"{name[:36]:<36} cell {i:>3} {str(kinds):<44} {n:>7} chars")
            for line in s.split("\n"):
                if re.search(r"writefile|def\s+agent", line, re.I):
                    print(f"      | {line.strip()[:90]}")
                    break


if __name__ == "__main__":
    main()
