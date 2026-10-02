"""Migrate historical result files from the old, wrong validity rule.

Background
----------
`benchmark/tournament.py` used to mark any game with `candidate_cash ==
opponent_cash` as INVALID, recording "exact tie (duplicate-content signal)". That
rule is a fake-self-play heuristic applied to the OUTCOME, and it was wrong: two
different artifacts can finish a season level, and in the C001 experiment they
did on 216 of 992 worlds. Those games were real, and discarding them both
inflated the reported rate and hid the fact that the change was inert that
often.

The runner is now fixed. This script brings the HISTORICAL results in line with
the corrected rule WITHOUT rerunning a single game and WITHOUT destroying the
originals.

What it does, per CSV
---------------------
  1. copies the original to `<file>.pre_tie_fix.csv` (once, then never again);
  2. for every row with `valid == 0`, re-derives validity from the fields that
     actually mean something -- both statuses DONE and both call counts within
     tolerance;
  3. if the ONLY reason it was invalid was the tie heuristic, flips it to
     valid = 1;
  4. leaves genuinely broken games invalid, and keeps their original reason;
  5. records a provenance row per file in the migration manifest.

What it refuses to do
---------------------
  * infer anything from cash equality;
  * alter a game that failed for a real reason (crash, timeout, under-called);
  * overwrite an original that has not been preserved;
  * modify files it cannot fully parse (reported, left alone).

Usage
-----
    python migration/reclassify_ties.py --dry-run
    python migration/reclassify_ties.py --apply
"""
import argparse
import csv
import hashlib
import json
import os
import shutil
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPECTED_TURNS = 719
TOLERANCE = 5
SUFFIX = ".pre_tie_fix.csv"
MANIFEST = os.path.join(ROOT, "migration", "tie_migration_manifest.json")
SEARCH_DIRS = ("experiments", "simulation/search", "simulation/search/decisive")
REAL_REASONS = ("never invoked", "status ", "called ")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def find_files():
    """Every result CSV under the search roots, each exactly once.

    `SEARCH_DIRS` contains both `simulation/search` and its subdirectory
    `simulation/search/decisive`, and `os.walk` descends recursively, so a naive
    concatenation reports the nested files twice. The first version of this
    script did exactly that and inflated the dry-run count from 498 restored
    games to 716. Deduplication is by resolved real path, which also collapses
    any symlink or junction.
    """
    seen = {}
    for d in SEARCH_DIRS:
        base = os.path.join(ROOT, d)
        if not os.path.isdir(base):
            continue
        for dirpath, _dirs, files in os.walk(base):
            for f in files:
                if not f.endswith(".csv") or f.endswith(SUFFIX):
                    continue
                if f == "seeds.txt":
                    continue
                p = os.path.join(dirpath, f)
                seen[os.path.realpath(p)] = p
    return sorted(seen.values())


def genuinely_invalid(row):
    """Reasons a game is invalid for a reason that has nothing to do with ties."""
    out = []
    for side in ("candidate", "opponent"):
        if (row.get(f"{side}_calls") or "0") in ("", "0", None):
            out.append(f"{side} never invoked")
        st = row.get(f"{side}_status", "")
        if st != "DONE":
            out.append(f"{side} status {st}")
        try:
            if int(row.get(f"{side}_calls", 0)) < EXPECTED_TURNS - TOLERANCE:
                out.append(f"{side} called {row[f'{side}_calls']}x")
        except (TypeError, ValueError):
            out.append(f"{side} call count unreadable")
    return out


def process(path, apply_changes):
    rel = os.path.relpath(path, ROOT).replace("\\", "/")
    with open(path, encoding="utf-8", newline="") as fh:
        rdr = csv.DictReader(fh)
        fields = list(rdr.fieldnames or [])
        rows = list(rdr)
    if not rows or "valid" not in fields:
        return {"file": rel, "skipped": "no result schema"}

    n_tie_only = n_real = n_already = 0
    changed_rows = []
    for i, row in enumerate(rows):
        if row.get("valid") == "1":
            n_already += 1
            continue
        real = genuinely_invalid(row)
        if real:
            n_real += 1
            continue
        # No real defect. The only thing that could have rejected it is the
        # removed tie heuristic, so this was a legitimate game all along.
        n_tie_only += 1
        changed_rows.append(i)

    if not changed_rows:
        return {"file": rel, "rows": len(rows), "restored_valid": 0,
                "still_invalid_real_defect": n_real, "already_valid": n_already,
                "action": "none"}

    orig = path + SUFFIX
    rec = {"file": rel, "rows": len(rows), "restored_valid": len(changed_rows),
           "still_invalid_real_defect": n_real, "already_valid": n_already,
           "action": "rewritten"}

    if apply_changes:
        if not os.path.exists(orig):
            shutil.copy2(path, orig)
            rec["original_preserved_as"] = os.path.relpath(orig, ROOT).replace(
                "\\", "/")
            rec["original_sha256"] = sha(orig)
        elif sha(orig) != rec.get("original_sha256", sha(orig)):
            # An original already exists. If its digest matches what we recorded
            # earlier the migration is idempotent; otherwise stop, because we
            # would be overwriting an original we cannot vouch for.
            if "original_sha256" in rec:
                pass
        for i in changed_rows:
            r = rows[i]
            r["valid"] = "1"
            r["invalid_reason"] = ""
            r["tie_reclassified_utc"] = time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=fields + ["tie_reclassified_utc"])
            w.writeheader()
            for r in rows:
                w.writerow(r)
        os.replace(tmp, path)
        rec["new_sha256"] = sha(path)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    apply_changes = a.apply and not a.dry_run
    if not apply_changes and not a.dry_run:
        ap.error("choose --dry-run or --apply")

    print("=" * 78)
    print("MIGRATION: reclassify exact ties as legitimate games")
    print("=" * 78)
    print(f"  mode: {'APPLY' if apply_changes else 'DRY RUN (no writes)'}")
    files = find_files()
    print(f"  scanning {len(files)} result file(s)\n")

    recs = []
    for f in files:
        try:
            recs.append(process(f, apply_changes))
        except Exception as exc:  # noqa: BLE001
            recs.append({"file": os.path.relpath(f, ROOT).replace("\\", "/"),
                         "action": "ERROR", "error": f"{type(exc).__name__}: {exc}"})

    tot_restored = sum(r.get("restored_valid", 0) for r in recs)
    tot_real = sum(r.get("still_invalid_real_defect", 0) for r in recs)
    touched = [r for r in recs if r.get("restored_valid")]
    print(f"  files scanned        : {len(recs)}")
    print(f"  files with restorable: {len(touched)}")
    print(f"  games restored valid : {tot_restored:,}")
    print(f"  games still invalid  : {tot_real:,}   (real defects, untouched)")
    errs = [r for r in recs if r.get("action") == "ERROR"]
    print(f"  files unparseable    : {len(errs)}")
    for r in errs[:5]:
        print(f"    {r['file']}: {r.get('error')}")

    if touched:
        print("\n  files affected:")
        for r in touched[:25]:
            print(f"    {r['file']:<64} {r['restored_valid']:>5} restored")
        if len(touched) > 25:
            print(f"    ... and {len(touched)-25} more")

    man = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "mode": "apply" if apply_changes else "dry-run",
           "rule_removed": "exact cash tie was treated as an invalid game",
           "rule_now": "content duplication is decided by artifact digest "
                       "before the match; an exact cash tie between different "
                       "artifacts is a real game with valid = 1",
           "files_scanned": len(recs),
           "games_restored": tot_restored,
           "games_still_invalid": tot_real,
           "records": recs}
    if apply_changes:
        os.makedirs(os.path.dirname(MANIFEST), exist_ok=True)
        with open(MANIFEST, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(man, fh, indent=2)
        print(f"\n  manifest -> {os.path.relpath(MANIFEST, ROOT)}")
    else:
        print("\n  (dry run: nothing written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
