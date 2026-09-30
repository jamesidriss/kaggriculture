"""Audit an agent's embedded market-parameter tables against the live environment.

An agent that embeds a stale scarcity curve misprices sales badly, which was
the root cause of Barnyard V7's 0-22 loss. This finds every embedded
CARROT/TOMATO/EGG below_func declaration and flags any that predate the
current `hinge` shape.
"""
import re
import sys
from collections import Counter

CURRENT = {"CARROT": "hinge", "TOMATO": "hinge", "EGG": "hinge"}
STALE_OK = {"CARROT": {"log"}, "TOMATO": {"linear"}, "EGG": {"linear"}}


def main(path):
    src = open(path, encoding="utf-8").read()
    print(f"AUDIT {path}")
    total_stale = 0
    for item, want in CURRENT.items():
        found = re.findall(
            r"['\"]" + item + r"['\"]\s*:\s*\{[^{}]*?below_func['\"]\s*:\s*['\"](\w+)['\"]",
            src)
        if not found:
            print(f"  {item:11s} no embedded below_func found")
            continue
        c = Counter(found)
        stale = sum(v for k, v in c.items() if k != want)
        total_stale += stale
        flag = "  <-- STALE PRESENT" if stale else "  all current"
        print(f"  {item:11s} blocks={len(found):3d}  {dict(c)}{flag}")
    print(f"  TOTAL STALE BLOCKS: {total_stale}")
    return total_stale


if __name__ == "__main__":
    bad = 0
    for p in sys.argv[1:]:
        bad += main(p)
        print()
    sys.exit(1 if bad else 0)