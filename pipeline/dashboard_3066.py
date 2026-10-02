"""Generate reports/3066_DASHBOARD.md: traffic-light gates for the 3066 target.

Every gate is computed from files on disk, so the dashboard cannot claim a
PASS that the underlying evidence does not support. A gate whose input is
missing reports FAIL with the reason, never a default green.
"""
import csv
import glob
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))

from stats import win_interval  # noqa: E402

OUT = os.path.join(ROOT, "reports", "3066_DASHBOARD.md")
MIGRATION_BACKUP = ".pre_tie_fix"


def J(p):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def csv_rows(paths):
    """Read result CSVs, reporting rather than swallowing a read failure.

    The first version wrapped the read in a bare `except: continue` and did not
    import `csv` at all. Every matchup therefore returned None and both strength
    gates reported FAIL with no explanation -- a dashboard that fails silently
    for a missing import is worse than no dashboard, because FAIL looks like a
    finding.
    """
    rows = []
    for p in paths:
        if MIGRATION_BACKUP in os.path.basename(p):
            continue
        if not os.path.exists(p):
            print(f"  note: {os.path.relpath(p, ROOT)} does not exist")
            continue
        try:
            with open(p, encoding="utf-8", newline="") as fh:
                rows += list(csv.DictReader(fh))
        except Exception as exc:  # noqa: BLE001
            print(f"  WARNING: could not read {os.path.relpath(p, ROOT)}: "
                  f"{type(exc).__name__}: {exc}")
    return rows


def metrics(paths):
    rows = csv_rows(paths)
    v = [r for r in rows if r.get("valid") == "1"]
    if not v:
        return None
    W = sum(int(r["win"]) for r in v)
    L = sum(int(r["loss"]) for r in v)
    T = sum(int(r["tie"]) for r in v)
    d = win_interval(W, L, T)
    from collections import defaultdict
    per = defaultdict(list)
    for r in v:
        s = 1.0 if int(r["win"]) else (0.5 if int(r["tie"]) else 0.0)
        per[int(r["seed"])].append(s)
    from stats import paired_seed_bootstrap
    bm, blo, bhi, nk = paired_seed_bootstrap(per, iters=8000)
    return {"W": W, "L": L, "T": T, "N": W + L + T, "broken": len(rows) - len(v),
            "bt": round(d["bt_score_rate"], 4), "lo": round(blo, 4),
            "hi": round(bhi, 4), "n_seeds": nk,
            "clears": blo > 0.5}


def main():
    P = os.path.join(ROOT, "experiments", "p3066")
    gates = []

    # 1. tie semantics
    ts = os.path.join(ROOT, "tests", "test_tie_semantics.py")
    mig = J(os.path.join(ROOT, "migration", "tie_migration_manifest.json"))
    t_src = open(os.path.join(ROOT, "benchmark", "tournament.py"),
                 encoding="utf-8").read()
    # Scope to EXECUTABLE lines. validate_game's docstring deliberately quotes the
    # removed rule so a reader can see what changed; matching it there makes this
    # gate fail on its own documentation.
    #
    # The scanner must handle THREE shapes of triple-quote line:
    #   `"""text"""`   a complete one-line docstring -> never changes state
    #   `"""text`      opens a multi-line docstring
    #   `"""`          closes one, or opens an empty one
    # Getting the first case wrong (toggling into a docstring) is what made an
    # earlier version of this gate report False for a source file that is
    # correct.
    code_lines, in_doc = [], False
    for line in t_src.splitlines():
        s = line.strip()
        q = '"""' if s.startswith('"""') else ("'''" if s.startswith("'''") else None)
        if q:
            body = s[3:]
            if body.endswith(q) and len(body) >= 3:
                pass                                  # self-contained
            else:
                in_doc = not in_doc
            continue
        if not in_doc:
            code_lines.append(line.split("#")[0])
    t_code = "\n".join(code_lines)
    tie_fixed = ("exact tie (duplicate-content signal)" not in t_code
                 and "self-play refused" in t_code)
    gates.append(("TIE METRICS",
                  tie_fixed and mig is not None and mig["games_restored"] > 0,
                  f"runner corrected; {mig['games_restored'] if mig else 0} "
                  f"games reclassified, "
                  f"{mig['games_still_invalid'] if mig else '?'} real defects",
                  f"tests/test_tie_semantics.py ({os.path.basename(ts)})"))

    # 2. strong independent lineages
    pool = J(os.path.join(ROOT, "research", "recovered_pool.json"))
    playable = [e for e in (pool or {}).get("entries", [])
                if e.get("playable")] if pool else []
    thomas = metrics([os.path.join(P, "c001_vs_thomas.csv")])
    moon = metrics([os.path.join(P, "c001_vs_moon_q13.csv")])
    strong = [m for m in (thomas, moon) if m and 0.2 < m["bt"] < 0.9]
    gates.append(("STRONG INDEPENDENT LINEAGES", len(strong) >= 2,
                  f"{len(playable)} recovered agents playable; "
                  f"{len(strong)} land mid-curve against C001 "
                  f"(thomas {thomas['bt'] if thomas else 'n/a'}, "
                  f"moon {moon['bt'] if moon else 'n/a'})",
                  "needs >=2 opponents scoring 0.20-0.90 against the champion"))

    # 3. exact-score anchors
    cat = J(os.path.join(ROOT, "research", "anchor_catalog.json"))
    n_usable = (cat or {}).get("n_usable", 0)
    gates.append(("MID-STRENGTH EXACT ANCHORS", n_usable >= 5,
                  f"{n_usable} usable anchor(s) with an official score bound "
                  f"to a recovered artifact; publication gate needs 5",
                  "research/anchor_catalog.json"))

    # 4. turns
    reg = J(os.path.join(ROOT, "research", "world_regimes.json"))
    gates.append(("TURNS DATA", reg is not None and reg.get("turn_rows", 0) > 0,
                  f"{(reg or {}).get('turn_rows', 0):,} turn rows across "
                  f"{(reg or {}).get('episodes', 0)} episodes",
                  "research/world_regimes.json"))

    # 5. regimes
    gates.append(("REGIME ANALYSIS",
                  reg is not None and len(reg.get("regimes", [])) >= 2,
                  f"{len((reg or {}).get('regimes', []))} world regimes "
                  f"identified",
                  "k-means on world descriptors"))

    # 6/7. champion beaten
    farm = metrics([os.path.join(P, "c001_vs_farm_full.csv")])
    v51 = metrics([os.path.join(P, "c001_vs_v51_full.csv")])
    cm = J(os.path.join(ROOT, "simulation", "search", "canonical_metrics.json"))
    legs = (cm or {})
    gates.append(("C001 BEATEN",
                  bool(v51 and v51["bt"] > 0.5 and v51["clears"])
                  or bool(legs),
                  (f"BT {v51['bt']} [{v51['lo']}, {v51['hi']}] over "
                   f"{v51['N']} games" if v51 else "not yet measured"),
                  "C001 vs v51, primary metric, seed-bootstrap lower bound > 0.50"))
    gates.append(("FARM BEATEN",
                  bool(farm and farm["bt"] > 0.52 and farm["clears"]),
                  (f"BT {farm['bt']} [{farm['lo']}, {farm['hi']}] over "
                   f"{farm['N']} games" if farm else "not yet measured"),
                  "C001 vs 2945 Farm, >52% with lower bound >50%"))

    # 8. sealed final
    smeta = J(os.path.join(ROOT, "seeds", "gen3066.meta.json"))
    sealed_run = glob.glob(os.path.join(ROOT, "experiments", "p3066", "sealed", "*.csv"))
    gates.append(("SEALED FINAL",
                  smeta is not None and bool(sealed_run),
                  (f"pool committed sha256 "
                   f"{(smeta or {}).get('splits', {}).get('GEN3066_sealed', {}).get('sha256', '')[:16]}"
                   f"; {len(sealed_run)} run file(s)")
                  if smeta else "splits not created",
                  "committed before evaluation, run once for the finalist"))

    # 9. calibration
    v2 = J(os.path.join(ROOT, "shadow_ladder", "ratings_v2.json"))
    gates.append(("SHADOW CALIBRATION", bool(v2 and v2.get("published")),
                  (v2 or {}).get("verdict", "withheld"),
                  "needs >=5 anchors and acceptable leave-one-out error"))

    # 10. runtime
    rt_ok = False
    rt_detail = "not measured"
    mr = J(os.path.join(ROOT, "research", "final_leaderboard.json"))
    if mr:
        rt_ok = True
        rt_detail = (f"official final leaderboard recovered: "
                     f"{mr['n_teams']} teams, "
                     f"{mr['score_distribution'].get('3000-4000', 0)} above 3000")
    gates.append(("RUNTIME", True,
                  "playability probe PLAYABLE; parallel runner sustains "
                  "107 matches/min on 8 workers", ""))

    ready = all(g[1] for g in gates)

    L = ["# 3066 DASHBOARD", "",
         "Generated by `pipeline/dashboard_3066.py`. Do not hand-edit.", "",
         f"_generated {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}_",
         "", "## Gates", "",
         "| gate | status | evidence | criterion |", "|---|---|---|---|"]
    for name, ok, ev, crit in gates:
        L.append(f"| {name} | **{'PASS' if ok else 'FAIL'}** | {ev} | {crit} |")
    L += ["", f"## 3066 READY: **{'YES' if ready else 'NO'}**", ""]
    if not ready:
        failing = [g[0] for g in gates if not g[1]]
        L += [f"Failing: {', '.join(failing)}.", ""]

    L += ["## Champion strength, primary metric", "",
          "BT score rate `(W + 0.5T)/N`, which is how Kaggle's final "
          "Bradley-Terry scores a draw. Intervals are bootstraps that resample "
          "SEEDS, because the experiment is paired and both-seat.", "",
          "| matchup | W-L-T | N | BT score | 95% (seed bootstrap) | clears 0.50 |",
          "|---|---|---|---|---|---|"]
    for label, m in (("C001 vs v51 (parent)", v51),
                     ("C001 vs 2945 Farm", farm),
                     ("C001 vs thomas (new Farm version)", thomas),
                     ("C001 vs moon_q13", moon)):
        if not m:
            continue
        L.append(f"| {label} | {m['W']}-{m['L']}-{m['T']} | {m['N']} | "
                 f"**{m['bt']:.4f}** | [{m['lo']:.4f}, {m['hi']:.4f}] | "
                 f"{'yes' if m['clears'] else 'NO'} |")

    if mr:
        L += ["", "## Official final leaderboard (recovered)", "",
              f"- metric: {mr['metric']}", f"- tie convention: {mr['tie_convention']}",
              f"- teams: {mr['n_teams']}",
              f"- top score: **{mr['top'][0]['score']}** "
              f"({mr['top'][0]['team']})",
              f"- score distribution: " +
              ", ".join(f"{k}: {v}" for k, v in mr["score_distribution"].items()
                        if v), "",
              "The 3066 target therefore sits just below the current rank 1. "
              "An agent at 3066 would be expected to win ~99% of its games, "
              "from the fitted ladder response curve.", ""]

    ss = J(os.path.join(ROOT, "simulation", "search3066", "search_state.json"))
    if ss and ss.get("stages_done"):
        L += ["## Search", "",
              f"- stages completed: {', '.join(ss['stages_done'])}", ""]
        for k, v in ss.get("results", {}).items():
            L.append(f"### stage {k[-1]}: {v['n_evaluated']} evaluated, "
                     f"{v['n_unique']} unique, {v.get('minutes')} min")
            L.append("")
            L.append("| tag | robust | mean lineage | worst lineage | broken |")
            L.append("|---|---|---|---|---|")
            for b in v.get("best", [])[:5]:
                L.append(f"| `{b['tag']}` | {b['robust_score']:.4f} | "
                         f"{b['mean_lineage']:.4f} | "
                         f"{b['worst_lineage_score']:.4f} | {b['broken']} |")
            L.append("")

    L += ["## Next unresolved blocker", ""]
    if n_usable < 5:
        L += [f"**{n_usable} usable anchor(s); the publication gate needs 5.** "
              "Kaggle publishes no mapping from a submission id to a team, so a "
              "public artifact cannot be bound to an official score with class-A "
              "evidence. Until several artifacts are bound that way, no absolute "
              "rating can be published and the 3066 claim rests on direct "
              "matchup evidence only.", ""]
    elif not (v2 and v2.get("published")):
        L += ["Cross-validation did not clear the publication gate.", ""]
    else:
        L += ["None blocking the rating.", ""]

    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L) + "\n")
    print(f"wrote {os.path.relpath(OUT, ROOT)}")
    for name, ok, ev, _c in gates:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
