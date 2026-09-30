"""Inspect a Kaggle notebook: metadata, cell sizes, license hints, embedded agents.

Deliberately prints summaries only -- full notebooks are 150-250KB and dumping
them into the conversation is pure waste.
"""
import json
import sys
import re


def summarize(path):
    nb = json.load(open(path, encoding="utf-8"))
    cells = nb.get("cells", [])
    print(f"=== {path}")
    print(f"  cells: {len(cells)}  nbformat: {nb.get('nbformat')}")
    km = nb.get("metadata", {})
    print(f"  kernelspec: {km.get('kernelspec', {}).get('name')}")
    lang = km.get("language_info", {})
    print(f"  language: {lang.get('name')} {lang.get('version')}")
    lic = km.get("license", km.get("kaggle", {}).get("license"))
    if lic:
        print(f"  LICENSE METADATA: {lic}")

    total = 0
    for i, c in enumerate(cells):
        src = "".join(c.get("source", []))
        total += len(src)
        head = src.strip().split("\n")[0][:110] if src.strip() else "(empty)"
        outs = c.get("outputs", [])
        otxt = 0
        for o in outs:
            otxt += len(json.dumps(o.get("text", o.get("data", {}))))
        flag = ""
        if re.search(r"base85|b85decode|zlib|import base64", src):
            flag += " [ENCODED]"
        if re.search(r"def agent\(", src):
            flag += " [HAS agent()]"
        if "output_files" in json.dumps(outs)[:2000]:
            flag += " [HAS FILES]"
        print(f"  cell {i:3d} {c['cell_type'][:4]:4s} src={len(src):7d} out={otxt:8d}{flag}  {head}")
    print(f"  TOTAL SOURCE CHARS: {total}")
    return nb


if __name__ == "__main__":
    for p in sys.argv[1:]:
        summarize(p)
        print()