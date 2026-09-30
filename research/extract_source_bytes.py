"""Rebuild an exact main.py from a SOURCE_BYTES b''.join((b'...'), ...) literal.

Some public Kaggriculture agents ship their submission file as a byte literal so
the shipped digest is verifiable. This reconstructs the exact bytes (preserving
CRLF) and checks the author's pinned SHA256.
"""
import ast
import hashlib
import re
import sys


def extract(path, out):
    src = open(path, encoding="utf-8").read()
    m = re.search(r"EXPECTED_MAIN_SHA256\s*=\s*'([0-9a-f]{64})'", src)
    expected = m.group(1) if m else None
    i = src.find("SOURCE_BYTES")
    if i < 0:
        raise SystemExit("no SOURCE_BYTES literal found")
    start = src.index("(", i)
    # Balance parentheses to find the end of the b''.join(( ... )) call.
    depth = 0
    j = start
    while True:
        c = src[j]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                break
        j += 1
    expr = src[start:j + 1]
    tree = ast.parse(expr, mode="eval")
    data = ast.literal_eval(tree.body)
    if isinstance(data, bytes):
        data = data
    else:
        data = bytes(data)
    open(out, "wb").write(data)
    got = hashlib.sha256(data).hexdigest()
    print(f"extracted {len(data)} bytes -> {out}")
    print(f"  expected sha256 {expected}")
    print(f"  actual   sha256 {got}")
    print(f"  MATCH: {expected == got}")
    return expected == got


if __name__ == "__main__":
    ok = extract(sys.argv[1], sys.argv[2])
    sys.exit(0 if ok else 1)