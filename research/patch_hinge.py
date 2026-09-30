"""Patch an embedded MARKET_PARAMS table from a pre-hinge to the current shape.

Experiment E-001. Barnyard V7 embeds CARROT/TOMATO/EGG scarcity curves that
predate the environment's switch to `hinge`. This rewrites only those three
entries' below_func to the current value, leaving every other byte untouched, so
the effect of the price-model correction can be measured in isolation.
"""
import re
import sys

PATCH = {"CARROT": ("log", "hinge"),
         "TOMATO": ("linear", "hinge"),
         "EGG": ("linear", "hinge")}


def main(src_path, out_path):
    src = open(src_path, encoding="utf-8").read()
    orig = src
    changes = []
    for item, (old_fn, new_fn) in PATCH.items():
        pat = re.compile(
            r'("%s"\s*:\s*\(\s*[\d.]+\s*,\s*[\d]+\s*,\s*[\d]+\s*,\s*)"%s"' % (item, old_fn))
        src, n = pat.subn(lambda m: m.group(1) + '"%s"' % new_fn, src)
        if n:
            changes.append(f"{item} {old_fn}->{new_fn} x{n}")
    if not changes:
        print("no pre-hinge entries found; nothing patched")
        return 1
    open(out_path, "w", encoding="utf-8", newline="").write(src)
    print(f"patched {len(changes)} group(s): {'; '.join(changes)}")
    print(f"bytes {len(orig)} -> {len(src)} (delta {len(src)-len(orig)})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))