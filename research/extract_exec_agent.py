"""Materialise an exact agent that self-writes its main.py, verifying its digest.

The Multi-Route notebook cell defines SOURCE_BYTES plus an EXPECTED_MAIN_SHA256
assertion, then writes main.py to a notebook-local WORKDIR. Executing it under a
temporary WORKDIR reproduces the author's own integrity check, so the recovered
bytes are verified by the artifact itself rather than by our parsing.
"""
import hashlib
import os
import sys
import tempfile
from pathlib import Path


def main(nb_path, out_path, cell=2):
    import json
    nb = json.load(open(nb_path, encoding="utf-8"))
    src = "".join(nb["cells"][cell]["source"])

    import re
    m = re.search(r"EXPECTED_MAIN_SHA256\s*=\s*'([0-9a-f]{64})'", src)
    expected = m.group(1) if m else None

    with tempfile.TemporaryDirectory() as td:
        wd = Path(td)
        g = {"WORKDIR": wd, "__name__": "multi_route_extract", "__file__": str(wd / "cell.py")}
        exec(compile(src, "<notebook-cell>", "exec"), g)
        target = wd / "main.py"
        if not target.exists():
            cand = list(wd.glob("**/*.py"))
            print(f"no main.py written; files present: {[c.name for c in cand][:10]}")
            return 1
        data = target.read_bytes()
        got = hashlib.sha256(data).hexdigest()
        out_path = os.path.abspath(out_path)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(data)
        print(f"wrote {len(data)} bytes -> {out_path}")
        print(f"  expected sha256 {expected}")
        print(f"  actual   sha256 {got}")
        print(f"  SELF-ASSERTION MATCH: {expected == got}")
        print(f"  agent callable: {callable(g.get('agent'))}")
        return 0 if expected == got else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))