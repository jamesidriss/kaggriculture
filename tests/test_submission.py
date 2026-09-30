"""Tests that must pass before any submission.

Run: python tests/test_submission.py
Exits non-zero on failure so it can gate a release.
"""

import hashlib
import importlib.util
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN = os.path.join(ROOT, "main.py")

FAILURES = []
CHECKS = 0


def check(cond, label):
    global CHECKS
    CHECKS += 1
    if not cond:
        FAILURES.append(label)
    print(("  PASS  " if cond else "  FAIL  ") + label)


def test_agent_signature():
    spec = importlib.util.spec_from_file_location("m", MAIN)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    check(callable(getattr(m, "agent", None)), "main.py exposes a callable agent()")
    return m


def test_schema_on_synthetic_obs(m):
    """A malformed action must never escape the agent."""
    farms = []
    for i in range(2):
        tiles = [[None] * 10 for _ in range(10)]
        for y in range(5):
            for x in range(5):
                tiles[y][x] = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 0,
                               "watered_today": False, "consecutive_unwatered": 1,
                               "yield_units": 2, "max_lifespan_step": 120,
                               "fertilized_until_day": -1}
        farms.append({"money": 1000.0, "tiles": tiles, "farmer": [4, 4],
                      "hands": [[5, 4]], "unlocked_quadrants": ["NW"],
                      "hires_today": 0})
    obs = {
        "player": 0, "step": 40, "day": 1, "hour": 16, "farms": farms,
        "private": {"shed": {"WHEAT": 5}, "seeds": {"WHEAT": 3},
                    "inventories": [{}, {}]},
        "market": {"inventory": {"WHEAT": 10000}, "prices": {"WHEAT": 25}},
        "town": {"unlocked_shops": []},
    }
    out = m.agent(obs)
    ok = isinstance(out, dict) and set(out) >= {"farmer", "hands", "market"}
    check(ok, "returns farmer/hands/market keys")
    check(isinstance(out["farmer"], list) and out["farmer"][0] in m.VALID_UNIT_OPS,
          "farmer action is a list with a valid op")
    check(len(out["hands"]) == 1, "hands length matches farm hands")
    check(all(isinstance(h, list) and h[0] in m.VALID_UNIT_OPS for h in out["hands"]),
          "every hand action is a valid list")
    check(all(isinstance(o, list) and o[0] in m.VALID_MARKET_OPS
              for o in out["market"]), "every market order is a valid list")
    check(len(out["market"]) <= 10, "market orders within maxMarketOrdersPerTurn")


def test_survives_hostile_obs(m):
    junk = [None, {}, {"farms": []}, {"farms": [None]}, {"player": 9},
            {"farms": [{}], "player": 0}]
    ok = True
    for obs in junk:
        try:
            out = m.agent(obs)
            if not (isinstance(out.get("farmer"), list)):
                ok = False
        except Exception:
            ok = False
    check(ok, "survives malformed/empty observations without raising")


def test_no_network_or_paths():
    src = open(MAIN, encoding="utf-8").read()
    banned = ["requests", "urllib", "socket", "http", "open(", "C:\\", "/home/",
              "os.environ", "__file__", "pickle", "torch", "numpy"]
    hits = [b for b in banned if b in src]
    check(not hits, f"no network/IO/absolute-path/dependency imports (hits={hits})")
    check("import math" in src, "only stdlib math is imported")


def test_no_secrets():
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True,
                             text=True).stdout.split()
    bad = [f for f in tracked if any(
        s in f.lower() for s in ("kaggle.json", "access_token", ".env", "credential",
                                 "cookie", "secret"))]
    check(not bad, f"no credential files tracked in git (hits={bad})")


def test_hash_recorded():
    h = hashlib.sha256(open(MAIN, "rb").read()).hexdigest()
    meta = os.path.join(ROOT, "champions", "champion_000", "METADATA.txt")
    if os.path.exists(meta):
        check(h in open(meta, encoding="utf-8").read(),
              "champion METADATA.txt SHA256 matches current main.py")
    else:
        check(False, "champions/champion_000/METADATA.txt exists")


def main():
    print("Submission gate for Kaggriculture")
    m = test_agent_signature()
    test_schema_on_synthetic_obs(m)
    test_survives_hostile_obs(m)
    test_no_network_or_paths()
    test_no_secrets()
    test_hash_recorded()
    print(f"\n{CHECKS - len(FAILURES)}/{CHECKS} checks passed")
    if FAILURES:
        print("FAILURES:")
        for f in FAILURES:
            print("  -", f)
        sys.exit(1)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    main()