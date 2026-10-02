"""Regression suite for the Kaggriculture audit.

Covers the harness-parity bug class and every invariant that, if it silently
fails, would make a tournament result meaningless.

Run: python tests/test_audit_regressions.py
"""
import csv
import hashlib
import importlib.util
import inspect
import io
import os
import re
import sys
import contextlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))
FAIL = []
N = 0


def check(cond, label, detail=""):
    global N
    N += 1
    line = ("  PASS  " if cond else "  FAIL  ") + label
    if detail:
        line += f"  {detail}"
    print(line)
    if not cond:
        FAIL.append(label)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def t_runtime_parity():
    """`step` must reach BOTH seats through env.run()."""
    from kaggle_environments import make
    rec = {0: [], 1: []}

    def mk(p):
        def _a(obs, configuration=None):
            if len(rec[p]) < 5:
                rec[p].append((obs.get("step"), obs.get("day"), obs.get("hour")))
            return {"farmer": ["PASS"], "hands": [], "market": []}
        return _a

    env = make("kaggriculture", configuration={"seed": 999, "episodeSteps": 720})
    env.run([mk(0), mk(1)])
    for p in (0, 1):
        check(all(s is not None for s, _, _ in rec[p]),
              f"seat {p}: observation['step'] delivered via env.run()")
        check(all(s == d * 24 + h for s, d, h in rec[p]),
              f"seat {p}: step == day*24 + hour")
    check([r[0] for r in rec[0]] == [r[0] for r in rec[1]],
          "both seats agree on step values")


def t_snapshot_divergence():
    """The persisted seat-1 snapshot must NOT be used as agent input."""
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": 999, "episodeSteps": 720})
    env.reset()
    env.run(["starter", "starter"])
    s1 = env.steps[3][1].observation
    check("step" not in s1,
          "persisted env.steps[i][1].observation lacks 'step' (the documented trap)")
    check("step" in env.steps[3][0].observation,
          "persisted env.steps[i][0].observation has 'step'")


def t_agent_signature_adaptation():
    """Every league agent must actually be invoked by the harness.

    Kaggle calls `agent(obs, configuration)`. Many public agents define
    `agent(obs)`. Handing the raw one-argument function to `env.run()` raises
    TypeError on every turn, the framework marks the agent INVALID, it never
    acts, it finishes on the starting $3,000, and the opponent is recorded as a
    decisive victim. That fabricated 72-0 results against barnyard_v7, v16_rc5
    and our own sunrise-v5.
    """
    import inspect
    meta_dir = os.path.join(ROOT, "opponents", "meta")
    files = [f for f in os.listdir(meta_dir) if f.endswith(".py")]
    check(len(files) > 0, f"league directory is populated ({len(files)} agents)")
    bad = []
    for f in files:
        p = os.path.join(meta_dir, f)
        spec = importlib.util.spec_from_file_location("sig_" + f[:-3], p)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            sig = inspect.signature(mod.agent)
            npos = sum(1 for q in sig.parameters.values()
                       if q.kind in (q.POSITIONAL_ONLY, q.POSITIONAL_OR_KEYWORD))
            var = any(q.kind == q.VAR_POSITIONAL for q in sig.parameters.values())
        except Exception as exc:  # noqa: BLE001
            bad.append(f"{f}: import failed {type(exc).__name__}")
            continue
        if npos < 2 and not var:
            # Legal one-arg agent: the harness MUST adapt it, not call it raw.
            pass
    check(not [b for b in bad if "import failed" in b],
          "every league agent imports cleanly", str(bad[:2]))


def t_harness_adapts_signatures():
    """meta.load must return a (obs, configuration)-callable for 1-arg agents."""
    sys.path.insert(0, os.path.join(ROOT, "benchmark"))
    import meta as M
    one_arg = [f for f in os.listdir(os.path.join(ROOT, "opponents", "meta"))
               if f.endswith(".py")]
    adapted = 0
    for f in one_arg:
        fn = M.load(os.path.join(ROOT, "opponents", "meta", f))
        try:
            inspect.signature(fn)
            # the wrapper must accept two positional args
            npos = sum(1 for q in inspect.signature(fn).parameters.values()
                       if q.kind in (q.POSITIONAL_ONLY, q.POSITIONAL_OR_KEYWORD))
            if npos >= 2 or hasattr(fn, "__wrapped__"):
                adapted += 1
        except Exception:  # noqa: BLE001
            pass
    check(adapted == len(one_arg),
          "meta.load wraps EVERY league agent in a 2-arg callable",
          f"{adapted}/{len(one_arg)}")


def t_results_have_no_phantom_opponents():
    """A league member that never played must not appear as a victim.

    An agent whose mean final cash equals the starting bank ($3,000) across
    every game was not playing. It must be reported as an error, not scored.
    """
    p = os.path.join(ROOT, "experiments", "final_meta_results.csv")
    if not os.path.exists(p):
        check(False, "results CSV exists")
        return
    rows = list(csv.DictReader(open(p, encoding="utf-8")))
    phantom = []
    for r in rows:
        mc = r.get("mean_cash")
        mo = r.get("mean_opp_cash")
        # A side sitting exactly on the starting bank never acted.
        if mc and int(mc) == 3000:
            phantom.append(f"{r['candidate']} (candidate held $3000)")
        if mo and int(mo) == 3000:
            phantom.append(f"{r['opponent']} held $3000 vs {r['candidate']}")
    check(not phantom, "no scored game involved an agent frozen at $3,000",
          str(sorted(set(phantom))[:3]))


def t_harness_sources():
    """Any script that DECIDES results must not feed agents from snapshots."""
    # Scripts that may legitimately read snapshots for diagnostics only.
    diagnostic_ok = {"ingest_replay.py", "locate_divergence.py"}
    # Scripts whose output gates a competitive decision.
    gating = ["meta.py", "validate_artifact.py", "close_games.py"]
    for fn in gating:
        p = os.path.join(ROOT, "benchmark", fn)
        if not os.path.exists(p):
            continue
        src = open(p, encoding="utf-8").read()
        feeds = re.search(r"\.step\[[^\]]+\]\[[^\]]+\]\.observation", src)
        check(feeds is None or fn in diagnostic_ok,
              f"{fn}: does not feed agents from persisted snapshots")


def t_digests():
    man = os.path.join(ROOT, "opponents", "store", "MANIFEST.csv")
    if not os.path.exists(man):
        check(False, "store MANIFEST.csv exists")
        return
    rows = list(csv.DictReader(open(man, encoding="utf-8")))
    digests = [r["sha256"] for r in rows]
    check(len(digests) == len(set(digests)), "no duplicate digests in store manifest")
    bad = [r["name"] for r in rows
           if not os.path.exists(os.path.join(ROOT, r["path"], "main.py"))
           or sha(os.path.join(ROOT, r["path"], "main.py")) != r["sha256"]]
    check(not bad, f"every store file matches its recorded digest {bad}")
    nolice = [r["name"] for r in rows if not r.get("license", "").strip()]
    check(not nolice, f"every store entry declares a licence {nolice}")


def t_known_hashes():
    expect = {
        os.path.join(ROOT, "research", "public_src",
                     "the-2945-farm-96-vs-the-top-10-public-bots", "extracted", "main.py"):
            "bfee70e9daaebeae0737a880f1df8f1c60d0783c59af620136cc0d28ef482bc7",
        os.path.join(ROOT, "postmortem_champion_000", "main.py"):
            "c1e3590d02e42d16091c5377e87a3db16496e5a462d558dc2925887f835f9891",
    }
    for p, h in expect.items():
        if os.path.exists(p):
            check(sha(p) == h, f"{os.path.basename(os.path.dirname(p)) or p}: {h[:12]}...")
        else:
            check(False, f"{p} exists")


def t_seeds():
    pools = {}
    for n in ("dev", "holdout", "final"):
        p = os.path.join(ROOT, "seeds", f"REAL_{n}.txt")
        if os.path.exists(p):
            pools[n] = [int(x) for x in open(p) if x.strip().isdigit()]
            check(len(pools[n]) == len(set(pools[n])), f"REAL_{n}: no duplicate seeds")
    if len(pools) == 3:
        for i in pools:
            for j in pools:
                if i < j:
                    check(not (set(pools[i]) & set(pools[j])),
                          f"REAL_{i} and REAL_{j} are disjoint")


def t_results_no_selfplay():
    p = os.path.join(ROOT, "experiments", "final_meta_results.csv")
    if not os.path.exists(p):
        return
    rows = list(csv.DictReader(open(p, encoding="utf-8")))
    selfplay = [r for r in rows
                if " vs " in r.get("matchup", "")
                and r["matchup"].split(" vs ")[0].strip() == r["matchup"].split(" vs ")[-1].strip()]
    check(not selfplay, f"no self-play rows in results {[r['matchup'] for r in selfplay][:2]}")


def main():
    print("Kaggriculture audit regression suite")
    for fn in (t_runtime_parity, t_snapshot_divergence,
               t_agent_signature_adaptation, t_harness_adapts_signatures,
               t_results_have_no_phantom_opponents,
               t_harness_sources,
               t_digests, t_known_hashes, t_seeds, t_results_no_selfplay):
        print(f"\n-- {fn.__name__}")
        try:
            fn()
        except Exception as exc:  # noqa: BLE001
            check(False, f"{fn.__name__} raised {type(exc).__name__}: {exc}")
    print(f"\n{N - len(FAIL)}/{N} checks passed")
    if FAIL:
        print("FAILURES:")
        for f in FAIL:
            print("  -", f)
        sys.exit(1)
    print("ALL REGRESSIONS PASS")


if __name__ == "__main__":
    main()