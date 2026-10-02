"""Ingest a public agent pool: digest, probe for playability, measure strength.

Purpose
-------
The research programme needs opponents spread across a RANGE of strengths. The
ladder response curve only has resolution where the win rate is mid-range, and
every matchup this project could previously measure was saturated (0% or 100%).
That is the actual reason calibration failed, and it is an opponent-selection
problem, not a statistics problem.

So: ingest everything legally obtainable, keep what plays, and MEASURE the
spread. If the recovered pool spans a useful range of win rates against C001,
the curve can be inverted and a position estimated. If it does not, that is
recorded as the finding.

Identity and licence discipline, unchanged
------------------------------------------
  * the SHA256 of the file is the agent's identity, never the filename;
  * an agent with no declared licence is stored under `unlicensed/` and may be
    used as an ANALYTICAL OPPONENT only. It is never a submission candidate and
    never redistributed as one;
  * a candidate that produces byte-identical behaviour to an existing artifact
    is collapsed, not stored twice.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))

POOL = os.path.join(ROOT, "opponents", "pool")
UNLICENSED = os.path.join(ROOT, "opponents", "unlicensed")
STORE = os.path.join(ROOT, "opponents", "store")
CATALOG = os.path.join(ROOT, "research", "recovered_pool.json")

# Sources, with the licence each one declares. Absence of a licence is recorded
# as absence, never assumed permissive.
SOURCES = [
    ("kaggriculture-r88-rivals", "data/pool/kaggriculture-r88-rivals",
     "dataset:kksky9k/kaggriculture-r88-rivals",
     {"moon_parent.py", "moon_q13_mg.py", "r30.py", "thomas.py"}, "UNDECLARED"),
    ("two-policy-last-dance", "data/pool/kaggriculture-two-policy-source",
     "dataset:mqingcs/kaggriculture-two-policy-source",
     {"last_dance_56720309.py"}, "Apache-2.0"),
    ("two-policy-observed", "data/pool/kaggriculture-two-policy-source",
     "dataset:mqingcs/kaggriculture-two-policy-source",
     {"observed_56713902.py"}, "Apache-2.0"),
    ("two-policy-observed-009", "data/pool/kaggriculture-two-policy-source",
     "dataset:mqingcs/kaggriculture-two-policy-source",
     {"observed_56713902_009.py"}, "Apache-2.0"),
    ("farmbench", "data/pool/farmbench-artifacts",
     "dataset:manjunadhpadarthi/farmbench-artifacts",
     {"farmbench.py"}, "UNDECLARED"),
]

# An agent must define one of these to be a playable submission candidate.
AGENT_MARKERS = ("def agent(", "def act(")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def probe(path):
    """Run the canonical playability probe. Never a hand-rolled check."""
    p = subprocess.run(
        [sys.executable, os.path.join(ROOT, "benchmark", "agent_loader.py"),
         "--probe", path],
        cwd=ROOT, capture_output=True, text=True, timeout=1200)
    out = (p.stdout or "") + (p.stderr or "")
    last = [l for l in out.strip().splitlines() if l.strip()]
    return (("PLAYABLE" in out), (last[-1] if last else "no output")[:160])


def main():
    print("=" * 78)
    print("POOL INGESTION - digest, licence gate, playability probe")
    print("=" * 78)
    os.makedirs(POOL, exist_ok=True)
    os.makedirs(UNLICENSED, exist_ok=True)

    existing = {}
    for d in (POOL, os.path.join(ROOT, "opponents", "meta"), UNLICENSED):
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if f.endswith(".py"):
                existing[sha(os.path.join(d, f))] = os.path.join(d, f)

    catalog = []
    for name, rel, source, files, licence in SOURCES:
        base = os.path.join(ROOT, rel)
        if not os.path.isdir(base):
            print(f"  {name}: source missing, skipped")
            continue
        for f in sorted(files):
            src = os.path.join(base, f)
            if not os.path.exists(src):
                # Datasets nest files in subdirectories, so look for the
                # basename anywhere under the source before giving up.
                found = None
                for dirpath, _dirs, fnames in os.walk(base):
                    if f in fnames:
                        found = os.path.join(dirpath, f)
                        break
                if not found:
                    print(f"  {name}/{f}: not found anywhere in the dataset")
                    catalog.append({"name": name, "file": f, "source": source,
                                    "declared_license": licence,
                                    "status": "NOT FOUND", "playable": None})
                    continue
                src = found
            text = open(src, encoding="utf-8", errors="ignore").read()
            has_agent = any(m in text for m in AGENT_MARKERS)
            digest = sha(src)
            rec = {"name": name, "file": f, "source": source,
                   "declared_license": licence, "bytes": os.path.getsize(src),
                   "sha256": digest, "defines_agent": has_agent}
            if digest in existing:
                rec["status"] = "DUPLICATE of " + os.path.relpath(
                    existing[digest], ROOT).replace("\\", "/")
                rec["playable"] = None
                catalog.append(rec)
                print(f"  {f:<34} duplicate of "
                      f"{os.path.basename(existing[digest])}")
                continue
            if not has_agent:
                rec["status"] = "NO agent() or act() - module, not an agent"
                rec["playable"] = None
                catalog.append(rec)
                print(f"  {f:<34} not an agent (no agent/act)")
                continue
            dest_dir = UNLICENSED if licence == "UNDECLARED" else POOL
            dest = os.path.join(dest_dir, f"{name}__{f}")
            shutil.copy2(src, dest)
            rec["path"] = os.path.relpath(dest, ROOT).replace("\\", "/")
            ok, note = probe(dest)
            rec["playable"] = ok
            rec["probe"] = note
            rec["usable_as"] = ("analytical_opponent_only" if licence == "UNDECLARED"
                                else "opponent_and_candidate")
            rec["status"] = "PLAYABLE" if ok else "REJECTED"
            catalog.append(rec)
            existing[digest] = dest
            print(f"  {f:<34} {rec['status']:<9} {note[:74]}")

    os.makedirs(os.path.dirname(CATALOG), exist_ok=True)
    with open(CATALOG, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ",
                                                  time.gmtime()),
                   "principles": {
                       "identity": "SHA256 of the file, never the filename",
                       "licence_gate": "an agent with no declared licence is an "
                                       "analytical opponent only and is never a "
                                       "submission candidate",
                       "probe": "benchmark/agent_loader.py --probe, canonical"},
                   "entries": catalog}, fh, indent=2)
    n_ok = sum(1 for c in catalog if c.get("playable"))
    print(f"\n  ingested {len(catalog)} entries, {n_ok} playable")
    print(f"  wrote {os.path.relpath(CATALOG, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
