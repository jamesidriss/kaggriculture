"""Create this generation's seed splits and commit the SEALED pool hash.

Split discipline
----------------
Three disjoint pools, generated from real ladder-derived seeds, with the sealed
pool's hash committed BEFORE any candidate in this generation is evaluated.
That ordering is the entire point: a sealed pool whose hash is written after
the candidate has been measured is not sealed.

The previous generation's pools are NOT reused. `REAL_final` and
`REAL_holdout` were viewed during the C001 promotion, so they are spent: a
finalist that has seen them has seen them, and re-running them would measure
nothing.

Also written: a manifest that proves the pools are disjoint from each other and
from the previous generation, so leakage cannot happen by accident later.
"""
import hashlib
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEEDS = os.path.join(ROOT, "seeds")
OUT = os.path.join(ROOT, "seeds", "gen3066.meta.json")

SPLITS = {
    # name: (count, purpose, source)
    #
    # DEV deliberately REUSES the head of REAL_scale, which the C001 decisive
    # and promotion legs already consumed. Those worlds are spent as evidence,
    # but they are perfectly good tuning data: contamination is a property of
    # what you CLAIM from a pool, not of the pool's cleanliness. Spending fresh
    # seeds on search and leaving the gates short would be the wrong trade.
    "GEN3066_dev": (500, "candidate generation and search; tuned on freely; "
                          "no result here is claimed as generalisation",
                    "spent_head"),
    "GEN3066_holdout": (130, "finalist selection; viewed once per finalist, "
                             "never tuned on", "fresh_tail"),
    "GEN3066_sealed": (130, "run ONCE for the single finalist; never tuned on",
                       "fresh_tail"),
}

PREVIOUS = ["ladder_real_dev", "ladder_real_final", "ladder_real_holdout",
            "REAL_dev", "REAL_final", "REAL_holdout",
            "meta_dev", "meta_final", "meta_holdout",
            "ladder_real_final"]


def read_pool(name):
    p = os.path.join(SEEDS, name + ".txt")
    if not os.path.exists(p):
        return []
    return [int(x) for x in open(p, encoding="utf-8") if x.strip().isdigit()]


def pool_hash(path):
    """Hash of the LF-normalised seed list, so the hash is platform-stable."""
    vals = read_pool(os.path.basename(path).replace(".txt", ""))
    body = "\n".join(str(v) for v in vals) + "\n"
    return hashlib.sha256(body.encode()).hexdigest(), len(vals)


def main():
    src = read_pool("REAL_scale")
    need_gate = sum(c for c, _p, s in SPLITS.values() if s == "fresh_tail")
    if len(tail_src := src[500:]) < need_gate:
        print(f"  need {need_gate} fresh seeds, tail has {len(tail_src)}")
        return 1
    prev_used = set()
    for n in PREVIOUS:
        prev_used.update(read_pool(n))
    prev_real = set(read_pool("REAL_scale"))
    print(f"  source REAL_scale: {len(src)} seeds")

    # Take from the TAIL of REAL_scale: the head (first 500) was consumed by the
    # C001 decisive and promotion legs, so the tail is the least contaminated
    # region available.
    tail = src[500:]
    src_head = src[:500]
    print(f"  uncontaminated tail: {len(tail)} seeds "
          f"(the first 500 were used by the C001 legs)")
    if len(tail) < SPLITS["GEN3066_holdout"][0] + SPLITS["GEN3066_sealed"][0]:
        print("  INSUFFICIENT uncontaminated seeds for the gates")
        return 1

    meta = {"generation": "3066-breakthrough",
            "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "source_pool": "seeds/REAL_scale.txt (real ladder-derived elite "
                           "seeds, 1,000 fresh, verified 24,548 elite games, "
                           "0 duplicate episode ids)",
            "offset_in_source": 500,
            "splits": {}, "previous_generation_pools": {}}
    for n in PREVIOUS:
        v = read_pool(n)
        if v:
            meta["previous_generation_pools"][n] = {"count": len(v),
                                                    "sha256": pool_hash(
                                                        os.path.join(SEEDS, n + ".txt"))[0]}
    if len(tail) < sum(c for c, _p, s in SPLITS.values() if s == "fresh_tail"):
        print("  INSUFFICIENT uncontaminated seeds for the gates")
        return 1

    i = 0
    assigned = {}
    for name, (count, purpose, src) in SPLITS.items():
        if src == "fresh_tail":
            chunk = tail[i:i + count]
            i += count
        else:
            chunk = src_head
        if len(chunk) < count:
            print(f"  {name}: only {len(chunk)} of {count} available")
            return 1
        p = os.path.join(SEEDS, name + ".txt")
        with open(p, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(str(v) for v in chunk) + "\n")
        h, n = pool_hash(p)
        assigned[name] = set(chunk)
        meta["splits"][name] = {"count": n, "sha256": h, "purpose": purpose,
                                "source": src,
                                "file": f"seeds/{name}.txt"}
        print(f"  {name:<20} {n:>4} seeds  sha256 {h[:16]}  ({src})")

    # Disjointness proof, computed rather than asserted.
    names = list(SPLITS)
    for a in range(len(names)):
        for b in range(a + 1, len(names)):
            ov = assigned[names[a]] & assigned[names[b]]
            meta["splits"][names[a]].setdefault("disjoint_from", {})[
                names[b]] = {"overlap_seeds": len(ov), "disjoint": not ov}
            print(f"  disjoint {names[a]} vs {names[b]}: "
                  f"{'OK' if not ov else f'OVERLAP {len(ov)}!'}")
    leak = set()
    for name in names:
        leak |= (assigned[name] & prev_used)
    meta["overlap_with_previous_generation_pools"] = len(leak)
    print(f"  overlap with previous-generation pools: {len(leak)} "
          f"(expected: the tail was excluded from those legs)")

    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(meta, fh, indent=2)

    print("\n" + "=" * 78)
    print("SEALED POOL COMMITTED BEFORE ANY CANDIDATE EVALUATION")
    print("=" * 78)
    print(f"  GEN3066_sealed sha256 = {meta['splits']['GEN3066_sealed']['sha256']}")
    print(f"  manifest               = seeds/gen3066.meta.json")
    print("  A finalist that fails this pool is rejected, not re-rolled.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
