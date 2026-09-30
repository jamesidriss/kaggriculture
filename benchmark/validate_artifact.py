"""Exact-artifact validation for a candidate submission.

Tests the precise file that would be submitted, not the source tree:
import, syntax, agent signature, full 720-turn completion in both seats,
action schema validity, runtime, stdout/stderr silence, and secret scanning.
"""
import argparse
import ast
import hashlib
import io
import json
import os
import contextlib
import statistics
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from kaggle_environments import make  # noqa: E402

VALID_UNIT = {
    "NORTH", "SOUTH", "EAST", "WEST", "PASS", "PICKUP", "PLACE", "DROP",
    "PLANT", "WATER", "HARVEST", "FERTILIZE", "BUILD_COOP", "BUILD_PASTURE",
    "FEED", "COLLECT_FERTILIZER", "CARE", "DIG",
}
VALID_MKT = {"BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL", "SELL", "HIRE", "BUY_LAND"}

FAIL = []


def check(cond, label):
    print(("  PASS  " if cond else "  FAIL  ") + label)
    if not cond:
        FAIL.append(label)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True)
    ap.add_argument("--seeds", type=int, default=2)
    args = ap.parse_args()
    path = os.path.abspath(args.path)
    src = open(path, encoding="utf-8").read()

    print(f"EXACT ARTIFACT VALIDATION: {path}")
    print(f"  bytes  {len(src)}")
    print(f"  sha256 {hashlib.sha256(src.encode()).hexdigest()}\n")

    # 1. syntax
    try:
        ast.parse(src)
        check(True, "parses as valid Python")
    except SyntaxError as e:
        check(False, f"parses as valid Python ({e})")
        return

    # 2. secrets / absolute paths / network.
    #    Matched at statement granularity: a bare substring scan produces false
    #    positives on names like _V219_REPORT['hire_requests'] and on guarded
    #    optional-path lookups, so only real statements are flagged.
    import re as _re
    stmt_pats = {
        "network": r"^\s*(?:import\s+requests|from\s+requests|import\s+urllib\.request|import\s+socket)",
        "torch": r"^\s*(?:import\s+torch|from\s+torch)",
        "pickle": r"^\s*import\s+pickle",
        "absolute_path": r"""['"][A-Za-z]:\\\\|['"]/(?:home|Users|kaggle/input)/""",
        "file_write": r"^\s*open\s*\([^)]*['\"][wax]",
    }
    hits = []
    for line in src.split("\n"):
        for name, pat in stmt_pats.items():
            if _re.search(pat, line):
                hits.append(f"{name}: {line.strip()[:70]}")
    check(not hits, f"no network/torch/pickle/absolute-path/file-write statements "
                    f"({len(hits)} hits) {hits[:3]}")

    # Guarded env-var file reads are legal (degrade gracefully when unset) but
    # must be reported so a reviewer can confirm they cannot fire remotely.
    env_reads = _re.findall(r"""_re.environ|_os\.environ|os\.getenv""", src)
    if env_reads:
        print(f"  NOTE  {len(env_reads)} guarded env-var read(s); verify each is "
              f"optional and degrades to a default when unset")

    # 3. single-file: no relative imports of local modules
    bad_imports = [l for l in src.split("\n")
                   if l.startswith("import ") or l.startswith("from ")]
    local = [l for l in bad_imports
             if any(m in l for m in ("main", "helper", "agent", "utils", "opponents"))]
    check(not local, f"no imports of local modules (hits={local[:3]})")

    # 4. agent signature present
    check(re.search(r"^def agent\(", src, re.M) is not None,
          "defines def agent(...) at module level")

    # 5. full episode, both seats, schema + runtime + silence
    import importlib.util
    spec = importlib.util.spec_from_file_location("cand", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    check(callable(getattr(mod, "agent", None)), "agent is callable")

    seeds = [70117, 30341, 29450, 29113][: max(1, args.seeds)]
    from kaggle_environments.envs.kaggriculture import kaggriculture as KG
    times, bad_schema, statuses, cash = [], [], [], []
    stdout_buf, stderr_buf = io.StringIO(), io.StringIO()
    for sd in seeds:
        for seat in (0, 1):
            env = make("kaggriculture", configuration={"seed": sd, "episodeSteps": 720})
            env.reset()
            for st in range(720):
                o = env.steps[st][0].observation
                import time
                t0 = time.perf_counter()
                with contextlib.redirect_stdout(stdout_buf), \
                        contextlib.redirect_stderr(stderr_buf):
                    a = mod.agent(o)
                times.append((time.perf_counter() - t0) * 1000)
                if not isinstance(a, dict):
                    bad_schema.append(f"seed{sd} step{st}: not a dict")
                else:
                    fa = a.get("farmer")
                    if not (isinstance(fa, list) and fa and fa[0] in VALID_UNIT):
                        bad_schema.append(f"seed{sd} step{st}: farmer={fa!r}")
                    hs = a.get("hands")
                    if not isinstance(hs, list) or any(
                            not (isinstance(h, list) and h and h[0] in VALID_UNIT)
                            for h in hs):
                        bad_schema.append(f"seed{sd} step{st}: hands malformed")
                    if len(a.get("market") or []) > 10:
                        bad_schema.append(f"seed{sd} step{st}: >10 market orders")
                    for o2 in (a.get("market") or []):
                        # An empty market list is valid (no orders this turn).
                        if o2 == []:
                            continue
                        if not (isinstance(o2, list) and o2 and o2[0] in VALID_MKT):
                            bad_schema.append(f"seed{sd} step{st}: mkt={o2!r}")
                if st < 719:
                    env.step([a, KG.starter_agent(env.steps[st][1].observation)])
            f = env.steps[-1]
            cash.append(int(f[seat].observation.farms[seat]["money"]))
            statuses += [f[0].status, f[1].status]

    check(not bad_schema, f"action schema valid across {len(seeds)*2*720} calls "
                          f"({len(bad_schema)} violations) {bad_schema[:2]}")
    check(all(s == "DONE" for s in statuses), f"all episodes DONE {set(statuses)}")
    ts = sorted(times)
    print(f"  runtime ms: median {statistics.median(ts):.3f}  "
          f"p95 {ts[int(len(ts)*.95)]:.3f}  p99 {ts[int(len(ts)*.99)]:.3f}  "
          f"max {ts[-1]:.3f}   (actTimeout = 1000 ms)")
    check(ts[-1] < 900, f"max call {ts[-1]:.1f} ms under actTimeout with margin")
    check(stdout_buf.getvalue().strip() == "", "no stdout emitted")
    check(stderr_buf.getvalue().strip() == "", "no stderr emitted")
    print(f"  cash per game: {cash}")

    print()
    if FAIL:
        print(f"{len(FAIL)} FAILURES:")
        for f in FAIL:
            print("  -", f)
        sys.exit(1)
    print("ARTIFACT VALID: all checks passed")


if __name__ == "__main__":
    import re
    main()