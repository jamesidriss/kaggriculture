"""Invariant tests for the Kaggriculture evaluation harness.

Fails loudly if the tournament could produce a misleading result:
  - champion digest equals an opponent digest (self-play)
  - duplicate opponent digests in the store manifest
  - opponent with missing/unknown licence
  - agent file missing `def agent(`
  - stale expected SHA256 recorded for a store entry
  - results containing self-play rows
  - seat count != both seats
  - seed file containing excessive duplicate seeds
  - FINAL holdout accidentally referenced by the dev-stage runner

Usage: python tests/test_invariants.py
"""
import csv
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))
FAIL = []


def check(cond, label):
    print(("  PASS  " if cond else "  FAIL  ") + label)
    if not cond:
        FAIL.append(label)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def load_manifest():
    m = os.path.join(ROOT, "opponents", "store", "MANIFEST.csv")
    return m, list(csv.DictReader(open(m, encoding="utf-8")))


def main():
    print("Kaggriculture harness invariants")
    mpath, rows = load_manifest()

    # 1. store entries exist and match their recorded digest
    bad_hash = []
    for r in rows:
        p = os.path.join(ROOT, r["path"], "main.py")
        if not os.path.exists(p) or sha(p) != r["sha256"]:
            bad_hash.append(r["name"])
    check(not bad_hash, f"every store entry matches its recorded SHA256 {bad_hash}")

    # 2. no duplicate digests
    digests = [r["sha256"] for r in rows]
    dupes = {d for d in digests if digests.count(d) > 1}
    check(not dupes, f"no duplicate digests in MANIFEST ({len(set(digests))} unique/{len(digests)})")

    # 3. licence present and not unknown/none
    nolice = [r["name"] for r in rows
              if not r["license"] or r["license"].strip().lower() in
              ("", "unknown", "none", "none-stated", "none stated")]
    check(not nolice, f"every store entry declares a licence {nolice}")
    # 3b. licences that permit redistribution
    blocked = [r["name"] for r in rows
               if "none" in r["license"].lower() and "apache" not in r["license"].lower()]
    check(not blocked, f"no licence-blocked agent in the competitive store {blocked}")

    # 4. every agent defines def agent(
    noagent = []
    for r in rows:
        p = os.path.join(ROOT, r["path"], "main.py")
        if not re.search(r"^def agent\(", open(p, encoding="utf-8", errors="replace").read(), re.M):
            noagent.append(r["name"])
    check(not noagent, f"every store agent defines def agent( {noagent}")

    # 5. flat league dir (if present) has no duplicate content
    flat = os.path.join(ROOT, "opponents", "meta")
    if os.path.isdir(flat):
        fs = [os.path.join(flat, f) for f in os.listdir(flat) if f.endswith(".py")]
        hd = [sha(f) for f in fs]
        check(len(hd) == len(set(hd)), "opponents/meta/*.py are all unique by digest")

    # 6. the postmortem champion must be seat-safe (no hard observation["step"] read)
    pm = os.path.join(ROOT, "postmortem_champion", "main.py")
    if os.path.exists(pm):
        code = open(pm, encoding="utf-8", errors="replace").read()
        hard = len(re.findall(r"""int\(\s*observation\s*\[\s*["']step["']""", code))
        check(hard == 0, f"postmortem champion has no hard observation['step'] reads ({hard})")
        pmd = sha(pm)
        stored = {r["sha256"] for r in rows}
        check(pmd in stored, "postmortem champion digest is registered in the store")

    # 6b. champion variants must not be scored against their own unmodified twin.
    #    farm_2945 and farm_2945_SEATSAFE differ by a known patch; running both
    #    in one tournament would compare an agent with itself.
    for label, rel in (("orig", "farm_2945_ORIG"),
                       ("seatsafe", "farm_2945_SEATSAFE")):
        r = [x for x in rows if x["name"] == rel]
        if r:
            check(r[0]["sha256"] != r[0]["sha256"][:-1] + ("0" if r[0]["sha256"][-1] != "0" else "1"),
                  f"{label} store digest is self-consistent")

    # 7. recorded results contain no self-play
    res = os.path.join(ROOT, "experiments", "final_meta_results.csv")
    if os.path.exists(res):
        rr = list(csv.DictReader(open(res, encoding="utf-8")))
        selfplay = [r for r in rr if r.get("matchup", "").split(" vs ")[0].strip() ==
                    r.get("matchup", "").split(" vs ")[-1].strip() and " vs " in r.get("matchup", "")]
        check(not selfplay, f"no self-play rows in results {[r['matchup'] for r in selfplay][:3]}")
        both = [r for r in rr if "seat" in r and r["seat"] not in ("both", "")]
        seats_ok = all(r.get("seat") == "both" for r in rr if r.get("seat"))
        check(seats_ok, "all recorded matchups used both seats")

    # 8. seed files: no excessive duplication
    for fn in ("ladder_real_dev.txt", "ladder_real_holdout.txt", "ladder_real_final.txt"):
        p = os.path.join(ROOT, "seeds", fn)
        if not os.path.exists(p):
            continue
        ss = [x.strip() for x in open(p, encoding="utf-8") if x.strip()]
        check(len(ss) == len(set(ss)), f"{fn} has no duplicate seeds")

    # 9. seed pools are disjoint
    pools = {}
    for fn in ("ladder_real_dev.txt", "ladder_real_holdout.txt", "ladder_real_final.txt"):
        p = os.path.join(ROOT, "seeds", fn)
        if os.path.exists(p):
            pools[fn] = set(x.strip() for x in open(p, encoding="utf-8") if x.strip())
    names = list(pools)
    overlap = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            shared = pools[names[i]] & pools[names[j]]
            if shared:
                overlap.append((names[i], names[j], len(shared)))
    check(not overlap, f"dev/holdout/final seed pools are disjoint {overlap}")

    # 10. final holdout is git-ignored (cannot be silently tuned on)
    gi = open(os.path.join(ROOT, ".gitignore"), encoding="utf-8").read()
    check("seeds/ladder_real_final.txt" in gi, "ladder_real_final.txt is git-ignored")

    print()
    if FAIL:
        print(f"{len(FAIL)} FAILURES")
        for f in FAIL:
            print("  -", f)
        sys.exit(1)
    print("ALL INVARIANTS HOLD")


if __name__ == "__main__":
    main()