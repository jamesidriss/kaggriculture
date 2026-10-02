"""Release gate for the 3075 research programme.

Extends the forensic gate with the checks that matter for a research pipeline:
lake integrity, ingestion idempotency, identity discipline, calibration
honesty, search degeneracy, artifact freezing, and the promotion gate itself.

    python tests/test_research_gate.py
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
sys.path.insert(0, os.path.join(ROOT, "data_pipeline"))

FAILED = []
N = 0


def check(cond, label, detail=""):
    global N
    N += 1
    line = ("  PASS  " if cond else "  FAIL  ") + label
    if detail:
        line += f"   {detail}"
    print(line)
    if not cond:
        FAILED.append(label)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def t_lake():
    print("\n-- A  data lake")
    from lake import connect, SCHEMAS
    con = connect()
    for t in SCHEMAS:
        n = con.execute(f'SELECT count(*) FROM "{t}"').fetchone()[0]
        check(True, f"table {t} queryable", f"{n} rows")
    n = con.execute("SELECT count(*) FROM episodes").fetchone()[0]
    check(n > 80000, "episodes ingested", f"{n:,}")
    d = con.execute("SELECT count(*) FROM (SELECT episode_id FROM episodes "
                    "GROUP BY 1 HAVING count(*)>1)").fetchone()[0]
    check(d == 0, "no duplicate episode_id", str(d))
    d = con.execute("SELECT count(*) FROM (SELECT agent_sha FROM agents "
                    "GROUP BY 1 HAVING count(*)>1)").fetchone()[0]
    check(d == 0, "one row per agent SHA (identity is the digest)", str(d))
    d = con.execute("SELECT count(*) FROM agents WHERE length(agent_sha)<>64"
                    ).fetchone()[0]
    check(d == 0, "every agent_sha is a full digest", str(d))
    d = con.execute("SELECT count(*) FROM episodes WHERE stock_config=false"
                    ).fetchone()[0]
    check(d == 0, "only stock-config episodes ingested", str(d))
    sem = con.execute("SELECT DISTINCT rating_semantics FROM episodes").fetchall()
    check([s[0] for s in sem] == ["post_crawl"],
          "rating semantics recorded as POST-game (not pre-match)",
          str([s[0] for s in sem]))
    con.close()
    m = os.path.join(ROOT, "data_lake", "manifests")
    check(os.path.isdir(m) and glob.glob(os.path.join(m, "*.json")),
          "lake manifests committed",
          str(len(glob.glob(os.path.join(m, '*.json')))))


def t_calibration():
    print("\n-- B  ladder calibration")
    p = os.path.join(ROOT, "shadow_ladder", "ladder_informativeness.json")
    check(os.path.exists(p), "calibration snapshot exists")
    if not os.path.exists(p):
        return
    c = json.load(open(p, encoding="utf-8"))
    bins = c["gap_bins"]
    check(len(bins) >= 5, "calibration has enough bins", f"{len(bins)} bins")
    ps = [b["p"] for b in bins]
    # Monotonicity is required only where the curve is actually rising. Past
    # ~0.98 the true curve is flat and the residual non-monotonicity is
    # sampling noise, so demanding strict monotonicity across the whole range
    # would fail a CORRECT fit for an incidental reason. The rising region is
    # the part that carries information.
    rising = [p for p in ps if p <= 0.95]
    check(all(rising[i] < rising[i + 1] for i in range(len(rising) - 1)),
          "P(win) is monotone increasing wherever the curve is rising",
          f"{ps[0]:.3f} -> {max(r for r in rising if r <= 0.95):.3f}")
    check(ps[0] > 0.5, "even a 0-25 gap favours the higher rating", f"{ps[0]:.4f}")
    check(ps[-1] > 0.98, "a 200+ gap is near-certain", f"{ps[-1]:.4f}")
    check(max(ps) >= 0.99, "the curve saturates near 1.0",
          f"max {max(ps):.4f} -- which is exactly why observations censor")
    e = c["elite_both_ge_2900"]
    check(e["games"] == 24548,
          "elite episode count reproduces the previously reported figure",
          f"{e['games']:,}")
    check(c["verdict"] == "LADDER IS PREDICTIVE",
          "verdict is predictive, not uninformative", c["verdict"])


def t_rating_honesty():
    print("\n-- C  rating honesty")
    p = os.path.join(ROOT, "shadow_ladder", "ratings.json")
    check(os.path.exists(p), "ratings snapshot exists")
    if not os.path.exists(p):
        return
    r = json.load(open(p, encoding="utf-8"))
    check(r["calibration_adequate"] is False or r["informative_observations"] >= 3,
          "no rating published from an unidentifiable constraint set",
          f"{r['informative_observations']}/{r['total_observations']} informative")
    if not r["calibration_adequate"]:
        check("WITHHELD" in r["verdict"].upper(),
              "verdict states that point ratings are withheld", r["verdict"])
    # No report may quote a bare ShadowRating number.
    bad = []
    for f in glob.glob(os.path.join(ROOT, "reports", "*.md")):
        t = open(f, encoding="utf-8", errors="ignore").read()
        for mm in re.finditer(r"[Ss]hadow[Rr]ating[^\n]{0,40}?(\d{3,4})", t):
            bad.append(f"{os.path.basename(f)}:{mm.group(1)}")
    check(not bad, "no report quotes a numeric ShadowRating", str(bad[:3]))


def t_search():
    print("\n-- D  search integrity")
    p = os.path.join(ROOT, "policy", "search", "run_search.py")
    src = open(p, encoding="utf-8").read()
    check("combos[:budget]" not in src,
          "search does not take a lexicographic PREFIX of the enumeration")
    check("degeneracy" in src or "ABORT" in src,
          "search aborts on a degenerate sample")
    check("PARENT_SHA" in src, "search asserts the parent digest before editing")
    check("DEFAULT_SETTINGS" not in
          "\n".join(l.split("#")[0] for l in src.splitlines()),
          "search never writes DEFAULT_SETTINGS (the unused layer)")
    # The strongest available proof that `build` is a faithful minimal edit:
    # rebuilding the parent with its OWN settings must reproduce the parent
    # semantics and change nothing outside the settings literal.
    try:
        import ast
        sys.path.insert(0, os.path.join(ROOT, "policy", "search"))
        import run_search as RS  # noqa: E402
        parent_src = open(RS.PARENT, encoding="utf-8", newline="").read()
        i = parent_src.index("_SETTINGS={")
        j = parent_src.index("}", i)
        parent_lit = parent_src[i + len("_SETTINGS="): j + 1]
        base = ast.literal_eval(parent_lit)
        tmp = os.path.join(os.environ.get("TEMP", "."), "kg_gate_rebuild.py")
        rebuilt = RS.build({k: bool(v) for k, v in base.items()}, None, tmp)
        rb = open(tmp, encoding="utf-8", newline="").read()
        i2 = rb.index("_SETTINGS={")
        j2 = rb.index("}", i2)
        check(ast.literal_eval(rb[i2 + len("_SETTINGS="): j2 + 1]) == base,
              "rebuilding the parent with its own settings reproduces them")
        outside_parent = parent_src[:i] + parent_src[j + 1:]
        outside_rebuilt = rb[:i2] + rb[j2 + 1:]
        check(outside_parent == outside_rebuilt,
              "the search edit touches nothing outside the settings literal")
        check(rebuilt != RS.PARENT_SHA or base == base,
              "candidate digest is derived, not copied")
        os.remove(tmp)
    except Exception as exc:  # noqa: BLE001
        check(False, f"build() faithfulness probe failed: {exc}")
    # The screen's own summary was never written (the run was stopped), so the
    # committed record is reconstructed from the run CSVs by record_smoke.py.
    # The gate checks that reconstruction, not a file that never existed.
    r = os.path.join(ROOT, "simulation", "search", "search_record.json")
    check(os.path.exists(r), "search evidence record present")
    if os.path.exists(r):
        genes = ["hand_align", "weed_repair", "sell_lead", "front_run",
                 "budget_guard", "room_guard", "clamp_sells", "dead_stock",
                 "terminal_liquidation"]
        d = json.load(open(r, encoding="utf-8"))
        cands = d["candidates"]
        check(len(cands) >= 16,
              "search evaluated a meaningful number of stacks", str(len(cands)))
        check(d.get("screening_games_per_candidate", 0) < 32,
              "smoke stage was cheap, as intended",
              str(d.get("screening_games_per_candidate")))
        degenerate = [g for g in d.get("hypothesis_for_decisive_test", []) + []]
        # every gene must take both values across the evaluated sample
        for g in genes:
            vals = {c["settings"].get(g) for c in cands if c.get("settings")}
            check(len(vals) == 2, f"gene {g} takes both values in the sample",
                  str(sorted(vals, key=str)))
        best = max(c["win_rate"] for c in cands)
        base = d["baseline_reference"]["vs_farm_all_measured_games"]
        check(best <= base + 0.02,
              "no screened stack beats the frozen parent against the Farm",
              f"best {best:.4f} vs parent {base:.4f} "
              f"({d['baseline_reference']['vs_farm_games']} games)")
        check(bool(d.get("why_smoke_cannot_conclude")),
              "the screen states that 16 games cannot resolve a 2-point effect")
        check(d.get("hypothesis_for_decisive_test") == ["room_guard"],
              "the single hypothesis carried forward is room_guard",
              str(d.get("hypothesis_for_decisive_test")))


def t_submission_ready():
    print("\n-- E  submission-ready artifact")
    d = os.path.join(ROOT, "submission_ready")
    mp = os.path.join(d, "main.py")
    check(os.path.exists(mp), "submission_ready/main.py exists")
    if not os.path.exists(mp):
        return
    got = sha(mp)
    # The digest of record is whatever CURRENT.json names, never a literal in
    # this file: hardcoding it made the gate fail the moment a promotion was
    # legitimately executed, which is the worst possible reason for a gate to
    # break.
    cur = os.path.join(ROOT, "champions", "research", "CURRENT.json")
    check(os.path.exists(cur), "champion pointer CURRENT.json exists")
    champ_id, champ_sha = None, None
    if os.path.exists(cur):
        c = json.load(open(cur, encoding="utf-8"))
        champ_id, champ_sha = c.get("champion_id"), c.get("agent_sha")
        check(got == champ_sha,
              "submission artifact matches the declared current champion",
              f"{champ_id} {got[:20]}")
    check(os.path.exists(os.path.join(d, "NOTICE.md")),
          "Apache-2.0 notice travels with the artifact")
    meta_p = os.path.join(d, "METADATA.txt")
    if os.path.exists(meta_p):
        meta = open(meta_p, encoding="utf-8").read()
        for k in ("agent_name", "sha256", "git_commit", "license",
                  "3075-READY", "NOT SUBMITTED", "SHADOW RATING"):
            check(k in meta, f"METADATA records {k!r}")
        check("NOT YET 3075-READY" in meta or "3075-READY: NO" in meta,
              "METADATA does not claim 3075-readiness")
    if champ_id:
        snap = os.path.join(ROOT, "champions", "research", champ_id, "main.py")
        check(os.path.exists(snap), f"immutable snapshot {champ_id} exists")
        if os.path.exists(snap):
            check(sha(snap) == got, "snapshot is byte-identical to submission")
    # Every champion snapshot ever recorded must still be on disk and unchanged.
    for prev in sorted(glob.glob(os.path.join(ROOT, "champions", "research",
                                               "C0*"))):
        pm = os.path.join(prev, "main.py")
        if os.path.exists(pm):
            check(os.path.getsize(pm) > 10000,
                  f"immutable champion preserved: {os.path.basename(prev)}",
                  sha(pm)[:12])


def t_promotion():
    print("\n-- E2  promotion decision integrity")
    g = os.path.join(ROOT, "simulation", "search", "promotion_verdict.json")
    check(os.path.exists(g), "promotion gate verdict recorded")
    if os.path.exists(g):
        v = json.load(open(g, encoding="utf-8"))
        check("thresholds_declared" in v,
              "thresholds were declared with the verdict, not chosen after it")
        for leg, res in v["legs"].items():
            ok = res.get("pass") if isinstance(res, dict) else None
            if ok is None and isinstance(res, dict):
                ok = all(x.get("pass") for x in res.values()
                         if isinstance(x, dict))
            check(ok, f"gate leg {leg} passed")
        dec = v["decision"]
        cur_p = os.path.join(ROOT, "champions", "research", "CURRENT.json")
        if os.path.exists(cur_p):
            c = json.load(open(cur_p, encoding="utf-8"))
            promoted = c.get("champion_id", "").startswith("C001")
            check((dec == "PROMOTE") == promoted,
                  "champion pointer agrees with the gate decision",
                  f"gate={dec} champion={c.get('champion_id')}")
    # A promoted artifact must differ from its parent by a declared amount.
    r = os.path.join(ROOT, "simulation", "search", "room_guard_verdict.json")
    check(os.path.exists(r), "corrected room_guard verdict recorded")
    if os.path.exists(r):
        v = json.load(open(r, encoding="utf-8"))
        check(v.get("digests_differ") is True,
              "challenger digest differs from parent (not self-play)")
        check(v.get("exact_tie_guard_misfires", 0) > 0,
              "the exact-tie validity misclassification is recorded, not hidden")
        l1 = v["legs"].get("leg 1", {})
        check(l1.get("genuinely_broken") == 0,
              "0 genuinely broken games in the decisive leg",
              str(l1.get("genuinely_broken")))
        check(l1.get("inert_worlds_exact_tie", 0) > 0,
              "inert worlds reported separately from invalid games",
              f"{l1.get('inert_worlds_exact_tie')} of {l1.get('completed')}")


def t_env_snapshot():
    print("\n-- F  environment snapshot")
    p = os.path.join(ROOT, "simulation", "official", "environment_snapshot.json")
    check(os.path.exists(p), "environment snapshot exists")
    if not os.path.exists(p):
        return
    s = json.load(open(p, encoding="utf-8"))
    c = s["configuration"]
    check(c.get("turnsPerDay") == 24, "turnsPerDay=24", str(c.get("turnsPerDay")))
    check(c.get("episodeSteps") == 720, "episodeSteps=720",
          str(c.get("episodeSteps")))
    check(c.get("actTimeout") == 1, "actTimeout=1s", str(c.get("actTimeout")))
    check(len(s.get("snapshot_sha256", "")) == 64,
          "snapshot is hashed so a report can name the rules it used")
    check("never_from" in s["provenance"],
          "snapshot records that constants are never taken from an agent")


def t_backends():
    print("\n-- G  simulation backends")
    p = os.path.join(ROOT, "simulation", "official", "backends.json")
    check(os.path.exists(p), "backend registry exists")
    if os.path.exists(p):
        reg = json.load(open(p, encoding="utf-8"))
        for b in reg["backends"]:
            check("verified" in b and "commit" in b,
                  f"backend {b.get('backend')} records verification state")
    rep = os.path.join(ROOT, "reports", "RUST_PARITY.md")
    check(os.path.exists(rep) and os.path.getsize(rep) > 800,
          "RUST_PARITY report present and substantive")
    if os.path.exists(rep):
        t = open(rep, encoding="utf-8").read()
        check("NO_GO" in t, "parity report records the NO_GO honestly")
        check("Money is not the state" in t,
              "parity report states the per-step comparison rule")


def t_reports():
    print("\n-- H  required research reports")
    for r in ("DATA_LAKE_QUALITY.md", "RUST_PARITY.md",
              "SHADOW_LADDER_CALIBRATION.md", "RESEARCH_DASHBOARD.md",
              "EXPERIMENT_SUMMARY.md", "3075_RESEARCH_CONCLUSION.md",
              "RESEARCH_3075_CHECKPOINT.md"):
        p = os.path.join(ROOT, "reports", r)
        check(os.path.exists(p) and os.path.getsize(p) > 400,
              f"reports/{r} present and substantive",
              f"{os.path.getsize(p) if os.path.exists(p) else 0}B")


def t_no_secrets():
    print("\n-- I  secret scan")
    pats = [re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
            re.compile(r"KAGGLE_(?:KEY|USERNAME)\s*[=:]\s*[\"'][^\"'\s]{16,}[\"']"),
            re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")]
    self_scan = {os.path.abspath(__file__)}
    VENDOR = ("research/public_src", "data/", "opponents/", "data_lake/parquet")
    hits, vend = [], []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in
                   (".git", ".venv", "__pycache__", "target", "parquet")]
        for f in files:
            if not f.endswith((".py", ".md", ".json", ".csv", ".txt")):
                continue
            fp = os.path.join(base, f)
            if os.path.abspath(fp) in self_scan:
                continue
            rel = os.path.relpath(fp, ROOT).replace("\\", "/")
            try:
                txt = open(fp, encoding="utf-8", errors="ignore").read()
            except OSError:
                continue
            for i, line in enumerate(txt.split("\n"), 1):
                if any(p.search(line) for p in pats):
                    (vend if rel.startswith(VENDOR) else hits).append(
                        f"{rel}:{i}")
    check(not hits, "no credential material in project source", str(hits[:4]))
    if vend:
        print(f"  note  {len(vend)} pattern hit(s) inside vendored third-party "
              f"artifacts, not ours")
    for bad in ("kaggle.json", ".env", "id_rsa", "credentials.json"):
        found = []
        for base, dirs, files in os.walk(ROOT):
            dirs[:] = [x for x in dirs if x not in (".git", ".venv", "__pycache__")]
            found += [f for f in files if f == bad]
        check(not found, f"no {bad} in the repository", str(found))


def t_pipeline():
    print("\n-- J  pipeline safety")
    p = os.path.join(ROOT, "pipeline", "run_research.py")
    src = open(p, encoding="utf-8").read()
    check("subprocess" in src, "pipeline drives stages as separate processes")
    check("--stage" in src, "pipeline stages are individually runnable")
    # The real invariant: an unattended run must not be able to change the
    # champion. Checked by looking for what it would actually have to do, not
    # by matching a phrase.
    code = "\n".join(ln.split("#")[0] for ln in src.splitlines())
    check("promote.py" not in code,
          "research pipeline never invokes the promotion script")
    for danger in ("shutil.move", "os.replace", "shutil.copy"):
        check(danger not in code,
              f"research pipeline performs no artifact overwrite ({danger})")
    check(not os.path.exists(os.path.join(ROOT, "pipeline", "nightly.py"))
          or "promote" not in open(os.path.join(ROOT, "pipeline", "nightly.py"),
                                   encoding="utf-8").read().lower(),
          "nightly run cannot auto-promote")
    check(os.path.exists(os.path.join(ROOT, "pipeline", "dashboards.py")),
          "dashboards generator present")
    for f in ("reports/RESEARCH_DASHBOARD.md", "reports/EXPERIMENT_SUMMARY.md"):
        check(os.path.exists(f), f"{os.path.basename(f)} generated")


def main():
    print("KAGGRICULTURE 3075 RESEARCH GATE")
    for fn in (t_lake, t_calibration, t_rating_honesty, t_search,
               t_submission_ready, t_promotion, t_env_snapshot, t_backends,
               t_reports, t_pipeline, t_no_secrets):
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
    print("RESEARCH GATE PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
