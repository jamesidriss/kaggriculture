"""Are v51 and The 2945 Farm genuinely different lineages?

The previous report justified the PRIMARY/HEDGE pair as "two different
strategic lineages" on the basis of different author names and different order
counts. The fresh trace contradicts the order counts almost exactly:

    metric        v51      Farm 2945
    SELL          1760     2035
    BUY_SEED       930      928
    BUY_ANIMAL      61       60
    HIRE          1327     1328
    BUY_LAND        10       10

Two agents written by different people do not normally agree to three
significant figures on HIRE and BUY_LAND. This measures the overlap directly,
at the level of the source, so the hedge is chosen on evidence.
"""
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "benchmark"))
from agent_loader import load_agent  # noqa: E402

A = os.path.join(ROOT, "opponents", "meta", "ahmedberatozer-v51-lean-flock.py")
B = os.path.join(ROOT, "opponents", "meta", "farm_2945_original.py")

STOP = set("""def return if else elif for while in not and or is None True False
import from class pass break continue lambda try except finally with as
global nonlocal yield raise assert del print range len int float str list dict
set tuple bool sum max min abs sorted enumerate zip map filter open
""".split())


def tokens(path):
    src = open(path, encoding="utf-8", errors="replace").read()
    # Ignore comments and docstrings, which differ by authorship style.
    src = re.sub(r"#[^\n]*", " ", src)
    src = re.sub(r'("""|\'\'\')(?:.|\n)*?\1', " ", src)
    return [t for t in re.findall(r"[A-Za-z_][A-Za-z_0-9]*", src)
            if t not in STOP and len(t) > 2]


def main():
    ta, tb = tokens(A), tokens(B)
    sa, sb = set(ta), set(tb)
    inter = sa & sb
    jac = len(inter) / len(sa | sb)
    cont = len(sa & sb) / min(len(sa), len(sb))

    def longest_common_run(x, y):
        """Longest shared contiguous token run, a proxy for copied blocks."""
        yset = {}
        for i, t in enumerate(y):
            yset.setdefault(t, []).append(i)
        best = 0
        for i, t in enumerate(x):
            for j in yset.get(t, ()):
                k = 0
                while i + k < len(x) and j + k < len(y) and x[i + k] == y[j + k]:
                    k += 1
                best = max(best, k)
        return best

    run = longest_common_run(ta, tb)
    print("SOURCE-LEVEL LINEAGE COMPARISON")
    print(f"  v51        tokens {len(ta):,}  unique {len(sa):,}")
    print(f"  Farm 2945  tokens {len(tb):,}  unique {len(sb):,}")
    print(f"  shared unique identifiers : {len(inter):,}")
    print(f"  Jaccard similarity        : {jac:.4f}")
    print(f"  containment (min side)    : {cont:.4f}")
    print(f"  longest identical token run: {run} tokens")
    print()
    # Attribution strings
    for name, p in (("v51", A), ("Farm 2945", B)):
        src = open(p, encoding="utf-8", errors="replace").read()[:4000]
        creds = [w for w in ("Ozer", "Berat", "ahmedberatozer", "thomastschinkel",
                             "yhay81", "destbreso", "aurax7", "tetsutani",
                             "prvsiyan", "Gluzdov") if w in src]
        print(f"  {name:<10} credits in header: {creds}")
    print()
    verdict = ("NEAR-DUPLICATE lineage - not a genuine hedge"
               if cont > 0.6 else
               "SHARED ancestry but independently evolved"
               if cont > 0.35 else
               "DISTINCT lineages")
    print(f"  VERDICT: {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
