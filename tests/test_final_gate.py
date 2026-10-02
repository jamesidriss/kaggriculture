"""Release gate for the Kaggriculture audit.

Every check here exists because its absence previously let a wrong conclusion
through. Run before every commit that touches a result:

    python tests/test_final_gate.py

Groups:
  A  official environment and call convention
  B  canonical statistics (Wilson, exact tests, BT identifiability)
  C  artifact integrity (digest == Git blob, registry self-consistency)
  D  provenance and licence gate
  E  seed splits
  F  competitive-result schema and hygiene
  G  the two frozen artifacts
  H  playability
"""
import csv
import hashlib
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))

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


def git(*a, binary=False):
    r = subprocess.run(["git"] + list(a), cwd=ROOT, capture_output=True)
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


# ---------------------------------------------------------------- A
def t_env_and_call_convention():
    print("\n-- A  official environment and call convention")
    check(os.path.exists(os.path.join(ROOT, "benchmark",
                                      "kaggle_call_convention.json")),
          "call-convention snapshot exists")
    import json
    p = os.path.join(ROOT, "benchmark", "kaggle_call_convention.json")
    snap = json.load(open(p, encoding="utf-8"))
    check(snap["both_arities_supported"] is True,
          "recorded evidence: Kaggle supports agent(obs) AND agent(obs, config)")
    check("co_argcount" in snap["official_evidence"]["Agent.act_arg_truncation"],
          "official source quote records the arity truncation")
    for r in snap["empirical"]:
        check(r["worked"] and r["invoked_times"] > 0,
              f"empirical: {r['label']} (co_argcount={r['co_argcount']}) invoked")

    # Step parity across a full episode, both seats.
    from kaggle_environments import make
    rec = {0: [], 1: []}

    def mk(seat):
        def _a(obs, configuration=None):
            rec[seat].append((obs.get("step"), obs.get("day"), obs.get("hour")))
            return {"farmer": ["PASS"], "hands": [], "market": []}
        return _a

    env = make("kaggriculture", configuration={"seed": 31337, "episodeSteps": 720})
    env.reset()
    env.run([mk(0), mk(1)])
    n = min(len(rec[0]), len(rec[1]))
    check(n > 700, f"both seats received {n} observations")
    check(all(s is not None for s, _, _ in rec[0] + rec[1]),
          "observation['step'] delivered to BOTH seats over a full episode")
    check(all(s == d * 24 + h for s, d, h in rec[0] + rec[1]),
          "step == day*24 + hour for every sampled turn, both seats")
    check([r[0] for r in rec[0][:n]] == [r[0] for r in rec[1][:n]],
          "P0.step == P1.step at corresponding turns")
    f = env.steps[-1]
    check(f[1].observation.get("step", "MISSING") == "MISSING",
          "persisted seat-1 snapshot still lacks 'step' (the documented trap)")
    check(f[0].observation.get("step", "MISSING") != "MISSING",
          "persisted seat-0 snapshot has 'step'")

    # The current environment constants snapshot must exist and be current.
    import kaggle_environments
    check(os.path.exists(os.path.join(ROOT, "benchmark",
                                      "current_env_snapshot.json")),
          "current-environment constant snapshot exists")
    snap2 = json.load(open(os.path.join(ROOT, "benchmark",
                                         "current_env_snapshot.json"),
                           encoding="utf-8"))
    d = snap2["env_config_defaults"]

    def val(k):
        v = d.get(k)
        # kaggriculture.json declares each key as a JSON-schema object whose
        # operative value is under "default".
        if isinstance(v, dict):
            return v.get("default")
        return v

    check(val("turnsPerDay") == 24 and val("episodeSteps") == 720,
          "snapshot records turnsPerDay=24 and episodeSteps=720",
          f"{val('turnsPerDay')}/{val('episodeSteps')}")
    check(val("boardSize") == 10 and val("startingMoney") == 3000,
          "snapshot records boardSize=10 and startingMoney=3000")
    check(val("maxMarketOrdersPerTurn") == 10
          and val("townShopUnlockInterval") == 3
          and val("townShopSellInterval") == 4
          and val("shedCapacity") == 100,
          "snapshot records the shop/market/shed constants")


# ---------------------------------------------------------------- B
def t_statistics():
    print("\n-- B  canonical statistics")
    import stats as S
    for w, n, elo, ehi in ((0, 10, 0.0, 0.2775), (10, 10, 0.7225, 1.0),
                           (5, 10, 0.2366, 0.7634), (76, 144, 0.4466, 0.6075),
                           (670, 720, 0.9096, 0.9469),
                           (596, 720, 0.7985, 0.8536),
                           (0, 792, 0.0, 0.0048)):
        lo, hi = S.wilson(w, n)
        check(abs(lo - elo) < 5e-4 and abs(hi - ehi) < 5e-4,
              f"wilson({w},{n}) == [{elo:.4f}, {ehi:.4f}]", f"[{lo:.4f},{hi:.4f}]")
    worst = 0.0
    for n in (1, 10, 144, 720, 1984):
        for w in {0, 1, n // 2, n - 1, n}:
            a = S.wilson(w, n); b = S.wilson_reference(w, n)
            worst = max(worst, abs(a[0] - b[0]), abs(a[1] - b[1]))
    check(worst < 1e-12, "two independent Wilson formulations agree",
          f"max diff {worst:.2e}")
    check(S.wilson(0, 0) == (0.0, 1.0), "wilson(0,0) is the unit interval")
    r = S.win_interval(76, 68, 0)
    check(abs(r["win_rate"] - 76 / 144) < 1e-12
          and abs(r["wilson_lo"] - S.wilson(76, 144)[0]) < 1e-15,
          "win_interval rate and interval come from the same counts")
    p, _ = S.mcnemar_exact(522, 517)
    check(0.05 < p < 1.0, "McNemar on n=1039 does not overflow and is valid",
          f"p={p:.4f}")
    check(S.binom_two_sided(1039, 1984) < 0.05,
          "exact binomial on 1039/1984 is significant",
          f"p={S.binom_two_sided(1039,1984):.4f}")
    hub = {("hub", x): (72, 0) for x in "bcde"}
    check(not S.bt_identifiability(hub)["ok"],
          "BT identifiability gate rejects an unbounded result set")
    try:
        S.bradley_tery(hub)
        check(False, "BT refuses to print an unbounded fit")
    except ValueError:
        check(True, "BT refuses to print an unbounded fit")
    reg = S.bradley_tery_regularized(hub)
    check(all(abs(v) < 10 for v in reg.values()),
          "REGULARIZED BT returns a finite ranking on the same unbounded data",
          str({k: round(v, 2) for k, v in reg.items()}))


# ---------------------------------------------------------------- C
def t_artifact_integrity():
    print("\n-- C  artifact integrity")
    targets = [
        ("postmortem_champion/main.py",
         "c1e3590d02e42d16091c5377e87a3db16496e5a462d558dc2925887f835f9891"),
        ("postmortem_hedge/main.py",
         "bfee70e9daaebeae0737a880f1df8f1c60d0783c59af620136cc0d28ef482bc7"),
    ]
    for rel, want in targets:
        p = os.path.join(ROOT, rel)
        check(os.path.exists(p), f"{rel} exists")
        if not os.path.exists(p):
            continue
        got = sha(p)
        check(got == want, f"{rel} sha256 == registry", got[:16])
        blob = git("cat-file", "blob", f"HEAD:{rel}", binary=True)
        if blob:
            check(hashlib.sha256(blob).hexdigest() == got,
                  f"{rel} on disk == Git blob (no line-ending drift)")
    for d in ("opponents", "champions", "challengers", "counterfactuals",
              "postmortem_champion", "postmortem_hedge", "postmortem_champion_000"):
        dr = os.path.join(ROOT, d)
        if not os.path.isdir(dr):
            continue
        bad = []
        for base, _, files in os.walk(dr):
            for f in files:
                if os.path.splitext(f)[1] not in (".py", ".txt"):
                    continue
                fp = os.path.join(base, f)
                if b"\r\n" in open(fp, "rb").read():
                    bad.append(os.path.relpath(fp, ROOT))
        check(not bad, f"{d}/ has no CRLF in content-addressed files", str(bad[:3]))
    # Registry self-consistency.
    man = list(csv.DictReader(open(os.path.join(ROOT, "opponents", "meta",
                                               "MANIFEST.csv"), encoding="utf-8")))
    dig = [r["sha256"] for r in man]
    check(len(dig) == len(set(dig)), "no duplicate digest in the league manifest")
    bad = []
    for r in man:
        f = os.path.join(ROOT, "opponents", "meta", r["name"] + ".py")
        if not os.path.exists(f) or sha(f) != r["sha256"]:
            bad.append(r["name"])
    check(not bad, "every league file matches its manifest digest", str(bad))
    store = os.path.join(ROOT, "opponents", "store")
    for d in os.listdir(store) if os.path.isdir(store) else []:
        f = os.path.join(store, d, "main.py")
        if os.path.isfile(f) and len(d) == 64:
            check(sha(f).startswith(d), f"store key {d[:12]} addresses its content")


# ---------------------------------------------------------------- D
def t_provenance_and_licence():
    print("\n-- D  provenance and licence gate")
    man = list(csv.DictReader(open(os.path.join(ROOT, "opponents", "meta",
                                               "MANIFEST.csv"), encoding="utf-8")))
    for r in man:
        if r["league_eligible"] == "yes":
            check(bool(r["license"].strip()) and r["license"] != "NONE-STATED",
                  f"eligible agent declares a licence: {r['name'][:32]}",
                  r["license"])
            check(bool(r["author"].strip()) and bool(r["source"].strip()),
                  f"eligible agent has author+source: {r['name'][:32]}")
    inelig = [r for r in man if r["league_eligible"] != "yes"]
    for r in inelig:
        check(bool(r["reason"].strip()),
              f"ineligible agent records a reason: {r['name'][:32]}", r["reason"][:48])
    tp = os.path.join(ROOT, "THIRD_PARTY.md")
    check(os.path.exists(tp) and "Apache-2.0" in open(tp, encoding="utf-8").read(),
          "THIRD_PARTY.md records the Apache-2.0 attributions")
    cat = list(csv.DictReader(open(os.path.join(ROOT, "research",
                                                "FINAL_PUBLIC_AGENT_CATALOG.csv"),
                                  encoding="utf-8")))
    bad = [r["agent_name"] for r in cat
           if len(r["sha256"]) != 64
           or sha(os.path.join(ROOT, r["path"])) != r["sha256"]]
    check(not bad, "catalog digests are recomputed and correct", str(bad))


# ---------------------------------------------------------------- E
def t_seeds():
    print("\n-- E  seed splits")
    pools = {}
    for n in ("REAL_dev", "REAL_holdout", "REAL_final", "REAL_scale"):
        p = os.path.join(ROOT, "seeds", n + ".txt")
        check(os.path.exists(p), f"seeds/{n}.txt exists")
        if os.path.exists(p):
            s = [int(x) for x in open(p, encoding="utf-8") if x.strip().isdigit()]
            pools[n] = s
            check(len(s) == len(set(s)), f"{n}: no duplicate seeds ({len(s)})")
    names = list(pools)
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            ov = set(pools[names[i]]) & set(pools[names[j]])
            check(not ov, f"{names[i]} and {names[j]} disjoint", str(sorted(ov)[:3]))
    check(os.path.exists(os.path.join(ROOT, "seeds", "MANIFEST.md")),
          "seeds/MANIFEST.md exists")
    check(os.path.exists(os.path.join(ROOT, "seeds", "REAL_scale.meta.json")),
          "scale pool provenance recorded")


# ---------------------------------------------------------------- F
def t_result_schema():
    print("\n-- F  competitive-result schema and hygiene")
    p = os.path.join(ROOT, "experiments", "final_meta_results.csv")
    check(os.path.exists(p), "experiments/final_meta_results.csv exists")
    if not os.path.exists(p):
        return
    rows = list(csv.DictReader(open(p, encoding="utf-8")))
    required = ["run_id", "timestamp", "environment_version", "candidate_name",
                "candidate_sha", "opponent_name", "opponent_sha", "seed", "seat",
                "candidate_cash", "opponent_cash", "win", "loss", "tie",
                "candidate_status", "opponent_status", "candidate_calls",
                "opponent_calls", "valid"]
    check(all(c in rows[0] for c in required), "all required schema fields present",
          str([c for c in required if c not in rows[0]]))
    valid = [r for r in rows if r["valid"] == "1"]
    check(len(valid) > 2000, f"valid game count {len(valid)}")
    sp = [r for r in valid if r["candidate_sha"] == r["opponent_sha"]]
    check(not sp, "NO self-play among valid competitive rows", str(len(sp)))
    check(min(int(r["candidate_calls"]) for r in valid) >= 714,
          "every valid row records ~719 candidate calls",
          str(min(int(r["candidate_calls"]) for r in valid)))
    check(min(int(r["opponent_calls"]) for r in valid) >= 714,
          "every valid row records ~719 opponent calls",
          str(min(int(r["opponent_calls"]) for r in valid)))
    check(all(r["candidate_status"] == "DONE" and r["opponent_status"] == "DONE"
              for r in valid), "every valid row is DONE/DONE")
    seats = {r["seat"] for r in valid}
    check(seats == {"0", "1"}, "both seats present", str(sorted(seats)))
    frozen = [int(r["candidate_cash"]) for r in valid]
    check(frozen.count(3000) < len(frozen) * 0.01,
          "no agent is frozen at the starting bank in scored games",
          f"{frozen.count(3000)} rows at $3000")
    ties = [r for r in valid if r["tie"] == "1"]
    check(not ties, "no exact ties among valid rows (duplicate-content signal)",
          str(len(ties)))
    envs = {r["environment_version"] for r in rows}
    check(len(envs) == 1, "one environment version across all results", str(envs))
    digests = {r["candidate_sha"] for r in rows} | {r["opponent_sha"] for r in rows}
    check(all(len(d) == 64 for d in digests), "every row carries a full digest")
    check(len(digests) >= 8, f"{len(digests)} distinct agents in the results")


# ---------------------------------------------------------------- G
def t_frozen_artifacts():
    print("\n-- G  frozen artifacts")
    for d in ("postmortem_champion", "postmortem_hedge"):
        p = os.path.join(ROOT, d)
        check(os.path.exists(os.path.join(p, "main.py")), f"{d}/main.py")
        m = os.path.join(p, "METADATA.txt")
        check(os.path.exists(m), f"{d}/METADATA.txt")
        if os.path.exists(m):
            txt = open(m, encoding="utf-8").read()
            for key in ("name:", "author:", "source:", "license:", "sha256:",
                        "environment_version:", "MODIFICATIONS", "NOT_SUBMITTED",
                        "LINEAGE NOTE"):
                check(key in txt, f"{d}/METADATA.txt records {key!r}")
            dig = re.search(r"sha256:\s*([0-9a-f]{64})", txt)
            if dig:
                check(dig.group(1) == sha(os.path.join(p, "main.py")),
                      f"{d}/METADATA sha256 matches main.py")
            check("NONE" in txt.split("MODIFICATIONS")[1][:80]
                  if "MODIFICATIONS" in txt else False,
                  f"{d} declares no modifications to the public artifact")
    # The retracted seat patch must not be the frozen artifact.
    ch = os.path.join(ROOT, "postmortem_hedge", "main.py")
    if os.path.exists(ch):
        check(sha(ch) != "c936e5a71ba40e1700ca1ab3a3271132407446bbb8b7523ced2cf4450ed8463f",
              "hedge is the VERBATIM artifact, not the retracted seat patch")


# ---------------------------------------------------------------- H
def t_playability():
    print("\n-- H  playability of the two frozen artifacts")
    from agent_loader import probe
    for rel in ("postmortem_champion/main.py", "postmortem_hedge/main.py"):
        r = probe(os.path.join(ROOT, rel))
        check(r["playable"], f"{rel} passes the playability probe",
              r.get("reason", "")[:80])
        if r.get("seat0"):
            check(r["seat0"]["status"] == "DONE" and r["seat1"]["status"] == "DONE",
                  f"{rel} DONE in both seats")
            check(r["seat0"]["active"] > 0 and r["seat1"]["active"] > 0,
                  f"{rel} emits a non-trivial action trace in both seats")
            check(r["seat0"]["market"] > 0 and r["seat1"]["market"] > 0,
                  f"{rel} participates in the market in both seats")


# ---------------------------------------------------------------- I
def t_no_secrets():
    print("\n-- I  secret scan")
    # Patterns must match an ACTUAL secret, not the vocabulary. A scanner that
    # fires on the word "token" in prose about where to store a token, or on a
    # base64 blob inside a third-party agent, reports noise and gets ignored.
    pats = [
        re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
        re.compile(r"KAGGLE_(?:KEY|USERNAME)\s*[=:]\s*[\"'][^\"'\s]{16,}[\"']"),
        re.compile(r"[\"']key[\"']\s*:\s*[\"'][A-Za-z0-9]{32,}[\"']"),
        re.compile(r"[\"']api[_-]?key[\"']\s*[:=]\s*[\"'][^\"'\s]{16,}[\"']"),
        re.compile(r"[\"']access[_-]?token[\"']\s*[:=]\s*[\"'][^\"'\s]{16,}[\"']"),
        re.compile(r"Authorization:\s*Bearer\s+[A-Za-z0-9._-]{20,}", re.I),
        re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    ]
    self_scan = {os.path.abspath(__file__)}
    # Vendored third-party artifacts are not our files; a pattern firing inside
    # them is reported but does not fail the gate on its own.
    VENDOR = ("research/public_src", "data/donor_agents", "opponents/")
    hits, vendor_hits = [], []
    for d in ("benchmark", "reports", "simcomp", "tests", "research", "seeds",
              "opponents", "postmortem_champion", "postmortem_hedge",
              "postmortem_champion_000", "challengers", "experiments"):
        dp = os.path.join(ROOT, d)
        if not os.path.isdir(dp):
            continue
        for base, _, files in os.walk(dp):
            for f in files:
                if not f.endswith((".py", ".md", ".csv", ".json", ".txt", ".cfg")):
                    continue
                fp = os.path.join(base, f)
                if os.path.abspath(fp) in self_scan:
                    continue
                try:
                    txt = open(fp, encoding="utf-8", errors="ignore").read()
                except OSError:
                    continue
                rel = os.path.relpath(fp, ROOT).replace("\\", "/")
                for i, line in enumerate(txt.split("\n"), 1):
                    if any(p.search(line) for p in pats):
                        (vendor_hits if rel.startswith(VENDOR) else hits).append(
                            f"{rel}:{i}")
    check(not hits, "no real credential material in repository source",
          str(hits[:4]))
    if vendor_hits:
        print(f"  note  {len(vendor_hits)} pattern hit(s) inside vendored "
              f"third-party artifacts (not ours): {vendor_hits[:2]}")
    for bad in ("kaggle.json", ".env", "id_rsa", "id_ed25519", "credentials.json"):
        found = []
        for base, dirs, files in os.walk(ROOT):
            dirs[:] = [x for x in dirs
                       if x not in (".git", ".venv", "data", "__pycache__")]
            found += [f for f in files if f == bad]
        check(not found, f"no {bad} anywhere in the repository", str(found))


REQUIRED_REPORTS = [
    "FINAL_RESEARCH_CONCLUSION.md", "TOP_META_TABLE.md",
    "HARNESS_SIGNATURE_AUDIT.md", "KAGGLE_RUNTIME_PARITY.md", "RETRACTIONS.md",
    "V51_VS_FARM.md", "LIVESTOCK_ECONOMICS.md", "BARNYARD_INVERSION.md",
    "SUNRISE_FINAL_AUTOPSY.md", "OPTIMAL_FINAL_PAIR.md",
    "COMPETITION_LESSONS.md", "FINAL_RUN_CHECKPOINT.md",
]


def t_reports_present():
    print("\n-- J  required deliverables present")
    for r in REQUIRED_REPORTS:
        p = os.path.join(ROOT, "reports", r)
        check(os.path.exists(p) and os.path.getsize(p) > 400,
              f"reports/{r} present and non-trivial",
              f"{os.path.getsize(p) if os.path.exists(p) else 0} bytes")


def main():
    print("KAGGRICULTURE FINAL RELEASE GATE")
    for fn in (t_env_and_call_convention, t_statistics, t_artifact_integrity,
               t_provenance_and_licence, t_seeds, t_result_schema,
               t_frozen_artifacts, t_playability, t_no_secrets,
               t_reports_present):
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
    print("FINAL GATE PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
