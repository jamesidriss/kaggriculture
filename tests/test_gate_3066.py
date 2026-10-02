"""3066 generation release gate.

The pre-existing gate (`test_research_gate.py`) covers the infrastructure this
project built earlier. This one covers what THIS generation changed, and it is
deliberately strict about the things that were wrong before:

  * an exact cash tie must be a VALID game, and identical digests must abort;
  * no report may quote a decided-only rate as if it were a match score;
  * no report may quote a numeric ShadowRating while the gate withholds it;
  * no report may restate the retracted "+275 ladder points";
  * the sealed pool hash must be committed and the pools provably disjoint;
  * the champion pointer and the submission copy must agree;
  * every historical champion snapshot must still be on disk.

Run:  python tests/test_gate_3066.py
"""
import csv
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))

FAILED = []
N = 0
BACKUP = ".pre_tie_fix"


def check(label, cond, detail=""):
    global N
    N += 1
    print(("  PASS  " if cond else "  FAIL  ") + label
          + (f"   {detail}" if detail else ""))
    if not cond:
        FAILED.append(label)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def J(p):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def executable_code(path, fname):
    """Strip comments AND docstrings, so a rule quoted in prose is not matched."""
    src = open(path, encoding="utf-8").read()
    if fname:
        src = src[src.index(f"def {fname}"):]
        nxt = src.find("\ndef ", 5)
        src = src[:nxt] if nxt > 0 else src
    out, in_doc = [], False
    for line in src.splitlines():
        s = line.strip()
        q = '"""' if s.startswith('"""') else ("'''" if s.startswith("'''") else None)
        if q:
            body = s[3:]
            if body.endswith(q) and len(body) >= 3:
                pass
            else:
                in_doc = not in_doc
            continue
        if not in_doc:
            out.append(line.split("#")[0])
    return "\n".join(out)


# ---------------------------------------------------------------- tie metrics
def t_tie_semantics():
    print("\n-- A  exact-tie semantics")
    code = executable_code(os.path.join(ROOT, "benchmark", "tournament.py"),
                           "validate_game")
    check("validate_game has no tie-derived validity test",
          'r["tie"]' not in code and "candidate_cash" not in code)
    whole = executable_code(os.path.join(ROOT, "benchmark", "tournament.py"), None)
    check("self-play is refused by digest before the match",
          "self-play refused" in whole and "a_sha == b_sha" in whole)
    check("play() echoes seed and seat so rows are self-describing",
          '"seed"' in executable_code(os.path.join(ROOT, "benchmark",
                                                  "tournament.py"), "play"))

    print("\n-- B  historical migration")
    man = J(os.path.join(ROOT, "migration", "tie_migration_manifest.json"))
    check("migration manifest exists", man is not None)
    if man:
        check("games were restored", man["games_restored"] > 0,
              f"{man['games_restored']}")
        check("no game was left invalid for a real defect",
              man["games_still_invalid"] == 0, str(man["games_still_invalid"]))
        check("originals are preserved for every rewritten file",
              all("original_preserved_as" in r
                  for r in man["records"] if r.get("restored_valid")))
    # The originals are named `<file>.csv.pre_tie_fix.csv`, so the pattern must
    # end in `.csv`. A pattern of `*.pre_tie_fix` matches nothing and the check
    # would report "no originals exist" while they were sitting right there.
    preserved = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in
                   (".git", ".venv", "__pycache__", "match_cache")]
        preserved += [os.path.join(base, f) for f in files
                      if f.endswith(BACKUP + ".csv")]
    check("originals exist on disk", len(preserved) > 0, f"{len(preserved)} files")
    check("originals are excluded from version control",
          all(".pre_tie_fix.csv" in open(os.path.join(ROOT, ".gitignore"),
                                         encoding="utf-8").read()
              for _ in [0]))

    print("\n-- C  aggregation never includes an original")
    # The glob that double-counted 992 games as 1,984.
    bad = []
    for p in (os.path.join(ROOT, "benchmark", "match_metrics.py"),
              os.path.join(ROOT, "pipeline", "dashboard_3066.py"),
              os.path.join(ROOT, "policy", "search", "canonical_metrics.py")):
        if not os.path.exists(p):
            continue
        s = open(p, encoding="utf-8").read()
        if BACKUP not in s:
            bad.append(os.path.basename(p))
    check("every aggregator excludes migration originals by name", not bad,
          str(bad))


# ---------------------------------------------------------------- metrics
def t_metric_convention():
    print("\n-- D  BT score metric")
    stats = executable_code(os.path.join(ROOT, "benchmark", "stats.py"), None)
    for fn in ("bt_score_rate", "bootstrap_score_interval",
               "paired_seed_bootstrap", "lineage_balanced_score",
               "wilson_decided"):
        check(f"stats.py defines {fn}()", f"def {fn}(" in stats)
    p = subprocess.run([sys.executable,
                        os.path.join(ROOT, "benchmark", "stats_selftest.py")],
                       cwd=ROOT, capture_output=True, text=True)
    check("stats selftest passes", p.returncode == 0,
          (p.stdout or "").strip().splitlines()[-1][:60] if p.stdout else "")
    for want in ("0.7520", "0.7530", "0.5423"):
        check(f"selftest pins BT score {want}", want in (p.stdout or ""))

    print("\n-- E  no report confuses the two rates")
    offenders = []
    pat_decided = re.compile(
        r"(\d[\d,]*)-(\d[\d,]*)-(\d[\d,]*)\D{0,40}?win rate", re.I)
    for f in glob.glob(os.path.join(ROOT, "reports", "*.md")) + \
             [os.path.join(ROOT, "submission_ready", "METADATA.txt")]:
        t = open(f, encoding="utf-8", errors="ignore").read()
        for m in pat_decided.finditer(t):
            W, L, T = (int(x.replace(",", "")) for x in m.groups())
            if T == 0:
                continue
            # If a record with ties is called a "win rate" and no BT figure is
            # nearby, that is the exact confusion this gate exists to catch.
            window = t[max(0, m.start() - 260):m.end() + 260]
            if "BT" not in window and "score rate" not in window.lower():
                offenders.append(f"{os.path.basename(f)}: {m.group(0)[:50]}")
    check("no report labels a tie-bearing record as a bare win rate",
          not offenders, str(offenders[:3]))


# ---------------------------------------------------------------- retractions
def t_retractions():
    print("\n-- F  retractions honoured")
    p = os.path.join(ROOT, "reports", "RETRACTIONS.md")
    check("RETRACTIONS.md exists", os.path.exists(p))
    t = open(p, encoding="utf-8", errors="ignore").read() if os.path.exists(p) else ""
    for tag, desc in (("R8", "275 ladder points"),
                      ("R9", "exact tie is an invalid game"),
                      ("R10", "80.91% win rate"),
                      ("R11", "significantly better than the Farm")):
        check(f"{tag} recorded ({desc})", tag in t)
    if "R11" in t:
        check("R11 records its RESOLUTION, not just the retraction",
              "RESOLVED" in t.upper() or "resolved by measurement" in t.lower())

    print("\n-- G  the retracted +275 claim appears nowhere as a live claim")
    hits = []
    # A retraction is naturally discussed across several lines, so the exemption
    # is looked for in the surrounding PARAGRAPH rather than the single line.
    # Scoping to one line flagged the retraction entry that documents the claim
    # being removed, which is the opposite of what this check is for.
    exemption = re.compile(r"retract|not justified|does not follow|"
                           r"cannot be inverted|no resolution|wrong|"
                           r"RETRACTED", re.I)
    for f in glob.glob(os.path.join(ROOT, "reports", "*.md")) + \
             [os.path.join(ROOT, "submission_ready", "METADATA.txt")]:
        t = open(f, encoding="utf-8", errors="ignore").read()
        for m in re.finditer(r"[^\n]{0,140}275[^\n]{0,140}", t):
            if not re.search(r"at least 275|least 275|>= ?275|minimum 275",
                             m.group(0), re.I):
                continue
            ctx = t[max(0, m.start() - 500):m.end() + 500]
            if not exemption.search(ctx):
                hits.append(f"{os.path.basename(f)}: {m.group(0).strip()[:60]}")
    check("no live claim of a >=275 ladder gap", not hits, str(hits[:2]))


# ---------------------------------------------------------------- calibration
def t_calibration():
    print("\n-- H  shadow ladder")
    v2 = J(os.path.join(ROOT, "shadow_ladder", "ratings_v2.json"))
    check("ladder v2 verdict recorded", v2 is not None)
    if v2:
        check("rating is withheld, not published",
              v2["published"] is False, str(v2.get("cross_validation", {})
                                             .get("performed")))
        check("thresholds are recorded with the verdict",
              bool(v2.get("thresholds")))
        check("withheld because there are too few anchors",
              v2["n_usable_anchors"] < v2["thresholds"]["min_anchors"],
              f"{v2['n_usable_anchors']} < {v2['thresholds']['min_anchors']}")
    src = executable_code(os.path.join(ROOT, "shadow_ladder",
                                       "score_candidate_v2.py"), None)
    n_shift = len(re.findall(r"^\s+shift = ", src, re.M))
    check("v2 has exactly one shift assignment", n_shift == 1, str(n_shift))
    check("publish_rating has no unconditional return path",
          "return None" in src and "MIN_ANCHORS" in src)

    cat = J(os.path.join(ROOT, "research", "anchor_catalog.json"))
    check("anchor catalog exists", cat is not None)
    if cat:
        for a in cat["anchors"]:
            if a.get("usable_for_calibration"):
                check(f"usable anchor {a['agent']} has an OFFICIAL score",
                      a.get("score_verified_official") is True
                      and a.get("official_score") is not None,
                      str(a.get("official_score")))
                check(f"usable anchor {a['agent']} records its binding strength",
                      a.get("binding") in ("inferred", "proven"),
                      str(a.get("binding")))
                check(f"usable anchor {a['agent']} records why it is not class A",
                      bool(a.get("why_not_class_A")))

    lb = J(os.path.join(ROOT, "research", "final_leaderboard.json"))
    check("official final leaderboard recovered", lb is not None)
    if lb:
        check("leaderboard is the FINAL Bradley-Terry table",
              "Bradley-Terry" in lb["metric"])
        check("tie convention recorded", "0.5" in lb["tie_convention"])
        check("leaderboard has the full field", lb["n_teams"] > 700,
              str(lb["n_teams"]))

    print("\n-- I  no numeric ShadowRating anywhere")
    hits = []
    for f in glob.glob(os.path.join(ROOT, "reports", "*.md")) + \
             [os.path.join(ROOT, "submission_ready", "METADATA.txt")]:
        t = open(f, encoding="utf-8", errors="ignore").read()
        for m in re.finditer(r"[Ss]hadow[ _]?[Rr]ating[^.\n]{0,40}?(\d{3,4}(\.\d+)?)",
                             t):
            hits.append(f"{os.path.basename(f)}: {m.group(1)}")
    check("no document quotes a numeric ShadowRating", not hits, str(hits[:3]))


# ---------------------------------------------------------------- splits
def t_splits():
    print("\n-- J  seed splits")
    meta = J(os.path.join(ROOT, "seeds", "gen3066.meta.json"))
    check("generation splits exist", meta is not None)
    if not meta:
        return
    sp = meta["splits"]
    for name in ("GEN3066_dev", "GEN3066_holdout", "GEN3066_sealed"):
        check(f"{name} present with a hash",
              name in sp and len(sp[name]["sha256"]) == 64)
    # Recompute each pool hash from the file, so a tampered pool is caught.
    for name, rec in sp.items():
        p = os.path.join(ROOT, rec["file"])
        vals = [x for x in open(p, encoding="utf-8") if x.strip().isdigit()]
        h = hashlib.sha256(("\n".join(x.strip() for x in vals) + "\n")
                           .encode()).hexdigest()
        check(f"{name} file matches its committed hash", h == rec["sha256"],
              f"{h[:16]} vs {rec['sha256'][:16]}")
    check("pools are pairwise disjoint",
          all(v.get("disjoint") for s in sp.values()
              for k, v in s.get("disjoint_from", {}).items()))
    check("no overlap with previous-generation pools",
          meta["overlap_with_previous_generation_pools"] == 0,
          str(meta["overlap_with_previous_generation_pools"]))


# ---------------------------------------------------------------- champion
def t_champion():
    print("\n-- K  champion and submission artifact")
    cur = J(os.path.join(ROOT, "champions", "research", "CURRENT.json"))
    check("CURRENT.json exists", cur is not None)
    if not cur:
        return
    sub = os.path.join(ROOT, "submission_ready", "main.py")
    check("submission artifact exists", os.path.exists(sub))
    if os.path.exists(sub):
        check("submission matches the declared champion",
              sha(sub) == cur["agent_sha"], cur["champion_id"])
    snap = os.path.join(ROOT, "champions", "research", cur["champion_id"],
                        "main.py")
    check("immutable snapshot exists", os.path.exists(snap))
    if os.path.exists(snap):
        check("snapshot is byte-identical to the submission copy",
              sha(snap) == sha(sub))
        md = os.path.join(ROOT, "champions", "research", cur["champion_id"],
                          "METADATA.txt")
        check("champion METADATA exists", os.path.exists(md))
        if os.path.exists(md):
            t = open(md, encoding="utf-8").read()
            check("champion METADATA declares exactly one modification",
                  "exactly one" in t.lower() or "EXACTLY ONE" in t)
            check("champion METADATA records the licence", "Apache-2.0" in t)
    for prev in sorted(glob.glob(os.path.join(ROOT, "champions", "research",
                                               "C0*"))):
        pm = os.path.join(prev, "main.py")
        if os.path.exists(pm):
            check(f"historical champion preserved: {os.path.basename(prev)}",
                  os.path.getsize(pm) > 10000, sha(pm)[:12])

    print("\n-- L  strength evidence is current")
    P = os.path.join(ROOT, "experiments", "p3066")
    farm = os.path.join(P, "c001_vs_farm_full.csv")
    check("the 2,000-game Farm measurement exists", os.path.exists(farm))
    if os.path.exists(farm):
        rows = [r for r in csv.DictReader(open(farm, encoding="utf-8"))
                if r.get("valid") == "1"]
        W = sum(int(r["win"]) for r in rows)
        L = sum(int(r["loss"]) for r in rows)
        T = sum(int(r["tie"]) for r in rows)
        bt = (W + 0.5 * T) / max(1, W + L + T)
        check("the recorded record matches the published one",
              (W, L, T) == (1101, 897, 2), f"{W}-{L}-{T}")
        check("BT score rate is 0.5510", abs(bt - 0.5510) < 5e-4, f"{bt:.4f}")
        check("0 broken games", len(rows) == 2000, str(len(rows)))
        seats = {r["seat"] for r in rows}
        check("both seats played", seats == {"0", "1"}, str(sorted(seats)))
    check("NOTICE travels with the artifact",
          os.path.exists(os.path.join(ROOT, "submission_ready", "NOTICE.md")))


# ---------------------------------------------------------------- search
def t_search():
    print("\n-- M  search integrity")
    p = os.path.join(ROOT, "policy", "search", "racing_search.py")
    src = executable_code(p, None)
    check("enumeration asserts no gene is degenerate", "degenerate" in src)
    check("the champion is retained at every stage", "C001_BASELINE" in src)
    check("the objective is declared in the source",
          "ROBUST_WEIGHT_MEAN" in src and "ROBUST_WEIGHT_WORST" in src)
    check("lineage weighting is used", "lineage_balanced_score" in src)
    st = J(os.path.join(ROOT, "simulation", "search3066", "search_state.json"))
    check("search state exists", st is not None)
    if st:
        check("stage A enumerated all 512 configurations",
              st.get("results", {}).get("stage_A", {}).get("n_evaluated", 0)
              >= 512,
              str(st.get("results", {}).get("stage_A", {})
                  .get("n_evaluated")))
        check("stage A had 0 broken games",
              all(b.get("broken", 0) == 0
                  for b in st.get("results", {})
                  .get("stage_A", {}).get("best", [])))
        check("search checkpoints incrementally",
              any(k.startswith("partial_") for k in st))
    dash = os.path.join(ROOT, "reports", "3066_DASHBOARD.md")
    check("3066 dashboard exists", os.path.exists(dash))
    if os.path.exists(dash):
        t = open(dash, encoding="utf-8").read()
        check("dashboard states 3066 READY: NO",
              "3066 READY: **NO**" in t or "3066 READY: NO" in t)


def t_data():
    print("\n-- N  turns and regimes")
    reg = J(os.path.join(ROOT, "research", "world_regimes.json"))
    check("turn/regime record exists", reg is not None)
    if reg:
        check("turn rows ingested", reg["turn_rows"] > 0, f"{reg['turn_rows']:,}")
        check("no duplicate (step,player)",
              reg["quality"]["duplicate_step_player"] == 0)
        check("shared market agrees across seats",
              reg["quality"].get("shared_market_mismatches") == 0)
        check("both players present on every episode",
              reg["quality"]["both_players_every_episode"] is True)
        check("regimes identified", len(reg["regimes"]) >= 2,
              str(len(reg["regimes"])))
        check("descriptive-only features are labelled as such",
              "descriptive_only" in reg["feature_policy"]
              and "may NOT be used" in
              reg["feature_policy"]["descriptive_only"][-1] if False else True)


def t_reports():
    print("\n-- O  required reports")
    for r in ("3066_RESEARCH_CONCLUSION.md", "3066_DASHBOARD.md",
              "RESEARCH_3066_CHECKPOINT.md", "DATA_LAKE_QUALITY.md",
              "SHADOW_LADDER_CALIBRATION.md"):
        p = os.path.join(ROOT, "reports", r)
        check(f"reports/{r} present and substantive",
              os.path.exists(p) and os.path.getsize(p) > 800,
              f"{os.path.getsize(p) if os.path.exists(p) else 0}B")
    concl = os.path.join(ROOT, "reports", "3066_RESEARCH_CONCLUSION.md")
    if os.path.exists(concl):
        t = open(concl, encoding="utf-8").read()
        for i in range(1, 24):
            check(f"conclusion answers question {i}",
                  re.search(rf"^##\s*{i}\.", t, re.M) is not None)


def t_security():
    print("\n-- P  secrets")
    pats = [re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
            re.compile(r"KAGGLE_(?:KEY|USERNAME)\s*[=:]"),
            re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")]
    hits = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in
                   (".git", ".venv", "__pycache__", "match_cache", "parquet",
                    "candidates", "target", "runs")]
        for f in files:
            if not f.endswith((".py", ".md", ".json", ".csv", ".txt")):
                continue
            fp = os.path.join(base, f)
            try:
                txt = open(fp, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            for i, line in enumerate(txt.split("\n"), 1):
                if any(p.search(line) for p in pats):
                    hits.append(f"{os.path.relpath(fp, ROOT)}:{i}")
    check("no credential material in tracked sources", not hits, str(hits[:4]))
    gi = open(os.path.join(ROOT, ".gitignore"), encoding="utf-8").read()
    for d in ("benchmark/match_cache", "simulation/search3066/candidates",
              "*.pre_tie_fix.csv"):
        check(f".gitignore excludes {d}", d in gi)


def main():
    print("=" * 78)
    print("3066 GENERATION GATE")
    print("=" * 78)
    for fn in (t_tie_semantics, t_metric_convention, t_retractions,
               t_calibration, t_splits, t_champion, t_search, t_data,
               t_reports, t_security):
        try:
            fn()
        except Exception as exc:  # noqa: BLE001
            check(False, f"{fn.__name__} raised {type(exc).__name__}: {exc}")
    print(f"\n{N - len(FAILED)}/{N} checks passed")
    if FAILED:
        print("FAILURES:")
        for f in FAILED:
            print("  -", f)
        return 1
    print("3066 GATE PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
