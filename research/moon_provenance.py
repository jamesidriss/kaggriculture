"""Moon provenance audit and full-field payoff.

Why this runs before any counter research
-----------------------------------------
C001 loses 94.6% of its games to two artifacts whose headers say they are
*derived from the 2945 Farm submission v9/3*, which is C001's own lineage. If
that is true then Moon is not an independent opponent, the "independent lineage"
label in the catalog is wrong, and 0.054 is a family argument rather than a
cross-lineage catastrophe. That changes what the right response is: a
cross-lineage weakness needs a genuinely different strategy, while a
within-lineage argument may be closable by transplanting the specific layer
that won.

Two questions, answered separately:
  1. LICENCE: is the Work actually distributed under Apache-2.0, or does an
     Apache body merely appear in the file? A licence body is not a grant.
  2. LINEAGE: is Moon outside C001's lineage, and what is its actual payoff
     across the whole field?
"""
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))

MOON = {
    "moon_parent": os.path.join(ROOT, "opponents", "unlicensed",
                                "kaggriculture-r88-rivals__moon_parent.py"),
    "moon_q13_mg": os.path.join(ROOT, "opponents", "unlicensed",
                                "kaggriculture-r88-rivals__moon_q13_mg.py"),
}
FARM = os.path.join(ROOT, "postmortem_hedge", "main.py")
V51 = os.path.join(ROOT, "postmortem_champion", "main.py")
C001 = os.path.join(ROOT, "champions", "research", "C001_room_guard", "main.py")
OUT = os.path.join(ROOT, "research", "moon_provenance.json")
WORK = os.path.join(ROOT, "experiments", "rank1")

# Attribution strings that appear in the artifact headers.
CLAIM_PATTERNS = {
    "derived_from_2945_farm_v9_3": r"submission v9/3|public V39",
    "derived_from_queue_compact": r"queue_compact",
    "modified_by": r"^#\s*MODIFIED by ([^\n:]+)",
    "for_local_discovery_only": r"LOCAL DISCOVERY ONLY",
    "not_an_official_score_claim": r"not an official Kaggle score claim",
    "unproven": r"unproven",
    "apache_body_present": r"Apache License",
}
AUTHORS = ("thomastschinkel", "yhay81", "destbreso", "aurax7", "tetsutani",
           "prvsiyan", "ahmed", "ozer", "gluzdov", "dmitrii", "kksky9k")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


# ---------------------------------------------------------------- licence
def audit_licence(name, path):
    src = open(path, encoding="utf-8", errors="ignore").read()
    head = "\n".join(src.splitlines()[:60])
    claims = {}
    for k, pat in CLAIM_PATTERNS.items():
        m = re.search(pat, head, re.M | re.I)
        claims[k] = (m.group(0).strip() if m else None)
    mod_by = re.search(r"^#\s*MODIFIED by ([^\n:]+)", head, re.M)
    present = [a for a in AUTHORS if a in head]

    # The decisive question: is the chain of Works complete?
    missing = []
    for ref in re.findall(r"Derived from ([A-Za-z0-9_./-]+\.py)", head):
        if not os.path.exists(os.path.join(ROOT, "data", "pool",
                                           "kaggriculture-r88-rivals", ref)):
            missing.append(ref)

    # A dataset-level licence, as opposed to a licence body inside one file.
    ds = os.path.join(ROOT, "data", "pool", "kaggriculture-r88-rivals")
    ds_licence = [f for f in os.listdir(ds)
                  if "licen" in f.lower() or "notice" in f.lower()] \
        if os.path.isdir(ds) else []

    blockers = []
    if missing:
        blockers.append(
            f"the immediate parent Work ({', '.join(missing)}) is NOT distributed, "
            f"so the Apache-2.0 derivation chain is incomplete and the licence "
            f"grant cannot be traced to the root Work")
    if claims.get("for_local_discovery_only"):
        blockers.append(
            "the artifact's own header marks it 'FOR LOCAL DISCOVERY ONLY', "
            "which is a statement about intended use, not a licence grant")
    if claims.get("not_an_official_score_claim"):
        blockers.append(
            "the header explicitly disclaims any official Kaggle score claim, "
            "so it was never presented as a submitted artifact")
    if not ds_licence:
        blockers.append(
            "the distributing dataset declares no LICENSE or NOTICE file of its "
            "own; an Apache body inside one file is not a dataset-level grant")

    if blockers:
        verdict = "UNKNOWN"
    else:
        verdict = "LICENSED"

    return {
        "artifact": name,
        "sha256": sha(path),
        "bytes": os.path.getsize(path),
        "source_dataset": "kaggle datasets kksky9k/kaggriculture-r88-rivals",
        "dataset_licence_files": ds_licence,
        "apache_body_in_file": bool(claims.get("apache_body_present")),
        "attributed_authors": present,
        "modified_by": mod_by.group(1).strip() if mod_by else None,
        "header_claims": claims,
        "missing_parent_works": missing,
        "blockers_to_reuse": blockers,
        "licence_verdict": verdict,
        "permitted_use": ("analytical opponent and adversarial benchmark only; "
                          "NOT a submission candidate, NOT to be transcribed "
                          "into any artifact we submit"
                          if verdict != "LICENSED" else
                          "reusable under Apache-2.0 with notices retained"),
    }


# ---------------------------------------------------------------- lineage
def token_profile(path):
    """Behavioural fingerprint proxy: the set of module-level identifiers."""
    src = open(path, encoding="utf-8", errors="ignore").read()
    ids = set(re.findall(r"^\s*(?:def|class)\s+([A-Za-z_][A-Za-z0-9_]*)", src,
                         re.M))
    ids |= set(re.findall(r"^([A-Z][A-Z0-9_]{3,})\s*=", src, re.M))
    return ids


def lineage_evidence(path):
    src = open(path, encoding="utf-8", errors="ignore").read()
    heads = "\n".join(src.splitlines()[:80])
    ev = {}
    ev["claims_v9_3_base"] = bool(re.search(r"submission v9/3", heads))
    ev["claims_v39_public"] = bool(re.search(r"public V39", heads))
    ev["names_thomastschinkel"] = "thomastschinkel" in src
    ev["names_ahmed_oz er".replace(" ", "")] = bool(
        re.search(r"Ahmed Berat O?z?e?r", src))
    return ev


# ---------------------------------------------------------------- payoff
OPPONENTS = [
    ("C001", C001, "L-OZER-2945"),
    ("v51", V51, "L-OZER-2945"),
    ("farm_2945", FARM, "L-OZER-2945"),
]


def play(a_path, b_path, seeds, tag, workers=8):
    out = os.path.join("experiments", "rank1", tag + ".csv")
    sf = os.path.join(WORK, f"seeds_{len(seeds)}.txt")
    os.makedirs(WORK, exist_ok=True)
    with open(sf, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(str(s) for s in seeds) + "\n")
    subprocess.run(
        [sys.executable, os.path.join(ROOT, "benchmark", "parallel_tournament.py"),
         "--a", a_path, "--b", b_path, "--seeds-file", sf, "--out", out,
         "--workers", str(workers), "--label-a", os.path.basename(a_path)[:-3],
         "--label-b", os.path.basename(b_path)[:-3], "--experiment-id", "rank1"],
        cwd=ROOT, capture_output=True, text=True)
    import csv
    p = os.path.join(ROOT, out)
    if not os.path.exists(p):
        return None
    rows = list(csv.DictReader(open(p, encoding="utf-8")))
    v = [r for r in rows if r.get("valid") == "1"]
    if not v:
        return None
    W = sum(int(r["win"]) for r in v)
    L = sum(int(r["loss"]) for r in v)
    T = sum(int(r["tie"]) for r in v)
    return {"W": W, "L": L, "T": T, "N": W + L + T,
            "broken": len(rows) - len(v),
            "bt_score": round((W + 0.5 * T) / max(1, W + L + T), 4)}


def main():
    n = int(sys.argv[sys.argv.index("--seeds") + 1]) if "--seeds" in sys.argv else 120
    os.makedirs(WORK, exist_ok=True)
    seeds = [int(x) for x in open(os.path.join(ROOT, "seeds",
                                               "GEN3066_dev.txt"), encoding="utf-8")
             if x.strip().isdigit()][:n]

    print("=" * 78)
    print("MOON PROVENANCE AND FULL-FIELD PAYOFF")
    print("=" * 78)

    lic = {name: audit_licence(name, p) for name, p in MOON.items()}
    for name, r in lic.items():
        print(f"\n-- LICENCE: {name}")
        print(f"   verdict              : {r['licence_verdict']}")
        print(f"   apache body in file  : {r['apache_body_in_file']}")
        print(f"   dataset licence files: {r['dataset_licence_files'] or 'NONE'}")
        print(f"   modified by          : {r['modified_by']}")
        print(f"   attributed authors   : {len(r['attributed_authors'])} "
              f"{r['attributed_authors'][:6]}")
        print(f"   missing parent Works : {r['missing_parent_works']}")
        for b in r["blockers_to_reuse"]:
            print(f"     BLOCKER: {b[:104]}")

    print("\n" + "=" * 78)
    print("LINEAGE: is Moon actually independent of C001?")
    print("=" * 78)
    lin = {}
    for name, p in list(MOON.items()) + [("C001", C001), ("v51", V51),
                                        ("farm_2945", FARM)]:
        e = lineage_evidence(p)
        tp = token_profile(p)
        lin[name] = {**e, "n_identifiers": len(tp), "_ids": tp}
        print(f"  {name:<12} v9/3 base={e['claims_v9_3_base']!s:<5} "
              f"V39={e['claims_v39_public']!s:<5} "
              f"thomastschinkel={e['names_thomastschinkel']!s:<5} "
              f"idents={len(tp)}")
    print("\n  identifier overlap with C001 (Jaccard):")
    c001 = lin["C001"]["_ids"]
    for name in ("moon_parent", "moon_q13_mg", "v51", "farm_2945"):
        t = lin[name]["_ids"]
        print(f"    {name:<14} {len(c001 & t) / max(1, len(c001 | t)):.4f}")

    print("\n" + "=" * 78)
    print(f"PAYOFF: Moon against the whole league ({n} seeds, both seats)")
    print("=" * 78)
    payoff = {}
    for mname, mpath in MOON.items():
        payoff[mname] = {}
        for oname, opath, _lin in OPPONENTS:
            r = play(mpath, opath, seeds, f"moon_{mname}_vs_{oname}")
            payoff[mname][oname] = r
            if r:
                print(f"  {mname:<12} vs {oname:<12} {r['W']:>4}-{r['L']:<4}-"
                      f"{r['T']:<3} of {r['N']:<5} BT {r['bt_score']:.4f} "
                      f"broken {r['broken']}")
            else:
                print(f"  {mname:<12} vs {oname:<12} NO DATA")
        print()

    out = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "licence_audit": lic,
           "lineage": {k: {kk: vv for kk, vv in v.items() if kk != "_ids"}
                       for k, v in lin.items()},
           "payoff": payoff, "seeds": len(seeds)}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, indent=2)
    print(f"wrote {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
