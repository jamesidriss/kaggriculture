"""Regression tests for the exact-tie / self-play confusion.

This project's worst historical error was fake self-play: two content-identical
files scored against each other produced a number that looked like a real
result. The fix that followed over-corrected. `benchmark/tournament.py` began
treating ANY exact cash tie as an invalid game with the reason "duplicate-content
signal", which silently discarded 216 of 992 real games in the C001 experiment
and reported 82.22% where the honest figure over all games was 64.31%.

Two rules follow, and this file pins both permanently:

  RULE 1  Content duplication is decided by the artifact digest, BEFORE the
          match. Identical SHA or identical normalised digest -> abort.

  RULE 2  An exact cash tie between two DIFFERENT artifacts is a REAL GAME.
          valid = 1, tie = 1, and it enters every aggregate.

The fixture agents below are built so that the two fixtures finish a season on
exactly the same cash while having completely different content. That is the
case the old rule destroyed.

Run:  python tests/test_tie_semantics.py
"""
import csv
import hashlib
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))

FAILED = []
N = 0


def check(label, cond, detail=""):
    global N
    N += 1
    print(("  PASS  " if cond else "  FAIL  ") + label
          + (f"   {detail}" if detail else ""))
    if not cond:
        FAILED.append(label)


# ---------------------------------------------------------------------------
# Fixture agents.
#
# `_IDLE` is a well-formed Kaggriculture agent that passes every turn. The two
# fixtures are byte-different (different names and a differing comment) but
# behaviourally identical, so they MUST finish level. Any divergence would be a
# harness bug, which the fixture deliberately makes obvious rather than subtle.
IDLE_TEMPLATE = '''
"""Fixture agent: {name}.

Deliberately behaviourally inert. Exists to pin the tie semantics, not to play.
"""
_AGENT_NAME = "{name}"


def _noop(observation):
    # A valid, if useless, action set for every step.
    return {{"farmer": ["PASS"], "hands": [], "market": []}}


def agent(observation):
    try:
        a = _noop(observation)
        _ = _AGENT_NAME
        return a
    except Exception:
        return {{"farmer": ["PASS"], "hands": [], "market": []}}


def act(observation):
    return agent(observation)
'''


def write_fixture(directory, name):
    p = os.path.join(directory, name + ".py")
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(IDLE_TEMPLATE.format(name=name))
    return p


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run_tournament(a, b, seeds_file, out, extra=()):
    cmd = [sys.executable, os.path.join(ROOT, "benchmark", "tournament.py"),
           "--a", a, "--b", b, "--seeds-file", seeds_file, "--out", out,
           "--label-a", "fixtureA"] + list(extra)
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)


def main():
    print("=" * 78)
    print("TIE SEMANTICS REGRESSION")
    print("=" * 78)
    tmp = tempfile.mkdtemp(prefix="kg_tie_")
    seeds = os.path.join(tmp, "seeds.txt")
    with open(seeds, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("4242\n")

    # ---------------------------------------------------------------- fixtures
    fa = write_fixture(tmp, "fixture_alpha")
    fb = write_fixture(tmp, "fixture_beta")
    dup_a = write_fixture(tmp, "fixture_dup")
    dup_b = os.path.join(tmp, "copy_of_dup.py")
    with open(dup_a, "rb") as src, open(dup_b, "wb") as dst:
        dst.write(src.read())

    print("\n-- fixture construction")
    check("two fixtures have different content", sha(fa) != sha(fb),
          f"{sha(fa)[:12]} vs {sha(fb)[:12]}")
    check("byte-identical copy has an identical digest",
          sha(dup_a) == sha(dup_b), sha(dup_a)[:12])

    # ------------------------------------------------- RULE 1: self-play abort
    print("\n-- RULE 1: identical content aborts BEFORE any match")
    out = os.path.join(tmp, "selfplay.csv")
    r = run_tournament(dup_a, dup_b, seeds, out)
    check("runner exits non-zero", r.returncode != 0, f"rc={r.returncode}")
    check("abort is announced", "self-play refused" in r.stdout,
          r.stdout.strip().splitlines()[-1][:80] if r.stdout.strip() else "")
    wrote = os.path.exists(out) and os.path.getsize(out) > 0
    check("no result file was produced for a self-play match", not wrote)

    # ------------------------------------------------ RULE 2: a real tie is valid
    print("\n-- RULE 2: an exact cash tie between DIFFERENT artifacts is valid")
    out = os.path.join(tmp, "realtie.csv")
    r = run_tournament(fa, fb, seeds, out)
    check("runner exits zero", r.returncode == 0,
          r.stdout.strip().splitlines()[-1][:90] if r.stdout.strip() else "")
    rows = list(csv.DictReader(open(out, encoding="utf-8")))
    check("games were recorded", len(rows) >= 2, f"{len(rows)} rows")
    if not rows:
        print("  (no rows; cannot continue)")
    for row in rows:
        s = int(row["seed"])
        check(f"seed {s}: cash levels", row["candidate_cash"] == row["opponent_cash"],
              f"{row['candidate_cash']} vs {row['opponent_cash']}")
        check(f"seed {s}: tie flag set", row["tie"] == "1", row["tie"])
        check(f"seed {s}: VALID, not invalid", row["valid"] == "1",
              row["invalid_reason"] or "no reason recorded")
        check(f"seed {s}: no duplicate-content reason",
              "duplicate" not in (row["invalid_reason"] or "").lower(),
              row["invalid_reason"] or "-")
        check(f"seed {s}: neither win nor loss",
              row["win"] == "0" and row["loss"] == "0",
              f"win={row['win']} loss={row['loss']}")
    both_seats = {int(x["seat"]) for x in rows}
    check("both seats were played", both_seats == {0, 1}, str(sorted(both_seats)))

    # -------------------------------------------- the metric consequence
    print("\n-- the metric consequence, which is the whole point")
    from stats import bt_score_rate, win_interval
    W = sum(int(x["win"]) for x in rows)
    L = sum(int(x["loss"]) for x in rows)
    T = sum(int(x["tie"]) for x in rows)
    d = win_interval(W, L, T)
    check("all-ties record scores 0.5, not 0",
          abs(d["bt_score_rate"] - 0.5) < 1e-12, f"{d['bt_score_rate']}")
    check("all-ties record has no decided games", d["decided"] == 0)
    check("decided-only rate is reported as undefined-safe 0",
          d["decided_win_rate"] == 0.0)
    check("tie rate is 1.0", abs(d["tie_rate"] - 1.0) < 1e-12)
    print(f"    record W-L-T = {W}-{L}-{T} over {W+L+T} games")
    print(f"    bt_score_rate  = {d['bt_score_rate']:.4f}   <- PRIMARY")
    print(f"    decided_win    = {d['decided_win_rate']:.4f}   <- secondary")

    # ------------------------------------------- old behaviour is unreachable
    print("\n-- the old rule is gone from the runner")
    src = open(os.path.join(ROOT, "benchmark", "tournament.py"),
               encoding="utf-8").read()
    # Scope the search to EXECUTABLE lines of validate_game. The function's
    # docstring deliberately quotes the old rule so a future reader understands
    # what was removed; matching it there would make this test fail on its own
    # documentation.
    start = src.index("def validate_game")
    end = src.index("\ndef ", start + 10)
    vg = src[start:end]
    code = []
    in_doc = False
    for line in vg.splitlines():
        s = line.strip()
        if s.startswith(('"""', "'''")):
            q = s[:3]
            if not (in_doc and s.endswith(q) and len(s) > 5):
                in_doc = not in_doc
            continue
        if in_doc:
            continue
        code.append(line.split("#")[0])
    vg_code = "\n".join(code)
    check("validate_game contains no cash-equality or tie test",
          'r["tie"]' not in vg_code and "candidate_cash" not in vg_code,
          "no outcome-derived validity test")
    whole = "\n".join(l.split("#")[0] for l in src.splitlines())
    check("the self-play digest check still exists",
          "self-play refused" in whole and "a_sha == b_sha" in whole)

    print(f"\n{N - len(FAILED)}/{N} checks passed")
    if FAILED:
        print("FAILURES:")
        for f in FAILED:
            print("  -", f)
        return 1
    print("TIE SEMANTICS REGRESSION PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
