"""Real public meta league for Kaggriculture.

Every member is an exact agent artifact recovered from a public Kaggle notebook
(see research/PUBLIC_META_AGENTS.csv and THIRD_PARTY.md for provenance and
licence). The earlier homemade league is kept separately as `league.py` and is
used only as a REGRESSION suite -- it is not evidence of competitiveness.

Usage:
  python benchmark/meta.py --cand main.py --opp barnyard_v7 --games 8
  python benchmark/meta.py --roundrobin --games 4
"""
import argparse
import hashlib
import importlib.util
import json
import math
import os
import statistics
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from kaggle_environments import make  # noqa: E402
from kaggle_environments.envs.kaggriculture import kaggriculture as KG  # noqa: E402

META_DIR = os.path.join(ROOT, "opponents", "meta")

# Real ladder-derived worlds where obtainable, plus deterministic pools.
META_DEV = [70117, 30341, 29450, 29113, 28777, 26001, 24002, 20003,
            19004, 18005, 16006, 15007, 12008, 11009, 10010, 9011]
META_HOLDOUT = [58001, 58002, 58003, 58004, 58005, 58006, 58007, 58008]
META_FINAL = [99991, 99992, 99993, 99994, 99995, 99996, 99997, 99998]

_cache = {}


def load(path):
    path = os.path.abspath(path)
    if path not in _cache:
        spec = importlib.util.spec_from_file_location("m_" + str(abs(hash(path))), path)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as exc:  # noqa: BLE001
            # An agent that needs notebook-local assets is not self-contained and
            # therefore not a legal submission artifact. Record why and skip it
            # rather than silently dropping it from the league.
            raise RuntimeError(f"{os.path.basename(path)} not self-contained: "
                               f"{repr(exc)[:160]}") from exc
        # Tag each agent with its own file path and content digest so the
        # self-play guard can detect two "different" names holding the same file.
        mod.agent.__kag_src__ = os.path.basename(path)
        mod.agent.__kag_sha__ = hashlib.sha256(open(path, "rb").read()).hexdigest()
        _cache[path] = mod.agent
    return _cache[path]


def meta_names():
    if not os.path.isdir(META_DIR):
        return []
    return sorted(f[:-3] for f in os.listdir(META_DIR) if f.endswith(".py"))


def play(agent_a, agent_b, seed, a_seat):
    """agent_a is the candidate; a_seat is its seat index."""
    # Guard against the same artifact being compared with itself. A duplicate
    # file produces a mirror match that always ties, which silently corrupts an
    # aggregate win rate if it is mistaken for a real result.
    sha_a = getattr(agent_a, "__kag_sha__", None)
    sha_b = getattr(agent_b, "__kag_sha__", None)
    if sha_a is not None and sha_a == sha_b:
        raise RuntimeError(
            f"SELF-PLAY GUARD: '{getattr(agent_a, '__kag_src__', '?')}' and "
            f"'{getattr(agent_b, '__kag_src__', '?')}' have identical content "
            f"(sha256 {sha_a[:16]}); the result would be a meaningless mirror match")
    a0 = agent_a if a_seat == 0 else agent_b
    a1 = agent_b if a_seat == 0 else agent_a
    env = make("kaggriculture", configuration={"seed": seed, "episodeSteps": 720})
    t0 = time.time()
    try:
        env.reset()
        env.run([a0, a1])
        f = env.steps[-1]
        money = [int(f[i].observation.farms[i]["money"]) for i in range(2)]
        st = [f[i].status for i in range(2)]
    except Exception as exc:  # noqa: BLE001
        return {"error": repr(exc)[:180], "seed": seed, "seat": a_seat,
                "runtime_s": round(time.time() - t0, 2)}
    c, o = money[a_seat], money[1 - a_seat]
    return {"seed": seed, "seat": a_seat, "cash": c, "opp_cash": o,
            "margin": c - o, "win": c > o, "loss": c < o, "tie": c == o,
            "status": st[a_seat], "opp_status": st[1 - a_seat],
            "runtime_s": round(time.time() - t0, 2)}


def wilson(w, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = w / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    s = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (round((c - s) / d, 4), round((c + s) / d, 4))


def summarise(rows, label):
    ok = [r for r in rows if "error" not in r]
    errs = [r for r in rows if "error" in r]
    n = len(ok)
    w = sum(1 for r in ok if r["win"])
    l = sum(1 for r in ok if r["loss"])
    t = sum(1 for r in ok if r["tie"])
    lo, hi = wilson(w, n)
    out = {"label": label, "games": n, "errors": len(errs),
           "W": w, "L": l, "T": t,
           "win_rate": round(w / n, 4) if n else 0.0,
           "score_rate": round((w + 0.5 * t) / n, 4) if n else 0.0,
           "wilson95": [lo, hi]}
    if ok:
        c = sorted(r["cash"] for r in ok)
        out["median_cash"] = int(statistics.median(c))
        out["mean_cash"] = int(statistics.mean(c))
        out["mean_opp"] = int(statistics.mean(r["opp_cash"] for r in ok))
        out["p10"] = c[max(0, int(n * 0.1))]
        out["p90"] = c[min(n - 1, int(n * 0.9))]
        out["max_runtime_s"] = max(r["runtime_s"] for r in ok)
        out["seat0_W"] = sum(1 for r in ok if r["seat"] == 0 and r["win"])
        out["seat1_W"] = sum(1 for r in ok if r["seat"] == 1 and r["win"])
        bad = [r for r in ok if r["status"] != "DONE" or r["opp_status"] != "DONE"]
        out["non_done"] = len(bad)
    if errs:
        out["error_samples"] = [e["error"] for e in errs[:3]]
    return out


def head_to_head(cand_path, opp_name, seeds):
    opp_path = os.path.join(META_DIR, opp_name + ".py")
    rows = []
    for s in seeds:
        for seat in (0, 1):
            rows.append(play(load(cand_path), load(opp_path), s, seat))
    return summarise(rows, f"vs {opp_name}")


def bradley_tery(results):
    """results: {(a,b): (wins_a, wins_b)} -> strength ordering."""
    teams = sorted({t for pair in results for t in pair})
    wins = {t: 0.0 for t in teams}
    plays = {t: 0 for t in teams}
    for (a, b), (wa, wb) in results.items():
        plays[a] += wa + wb
        plays[b] += wa + wb
        # 1 point per win, 0.5 per draw-equivalent omitted (round robin here)
        wins[a] += wa
        wins[b] += wb
    rates = {t: (wins[t] / plays[t] if plays[t] else 0.5) for t in teams}
    return rates


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cand", default="main.py")
    ap.add_argument("--opp", default="")
    ap.add_argument("--games", type=int, default=8)
    ap.add_argument("--stage", default="meta_dev",
                    choices=["meta_dev", "meta_holdout", "meta_final"])
    ap.add_argument("--roundrobin", action="store_true")
    ap.add_argument("--json", default="")
    args = ap.parse_args()

    seeds = {"meta_dev": META_DEV, "meta_holdout": META_HOLDOUT,
             "meta_final": META_FINAL}[args.stage][: max(1, args.games)]

    names = meta_names()
    print(f"meta league ({len(names)}): {', '.join(names)}")
    print(f"cand={args.cand}  stage={args.stage}  seeds={seeds}\n")

    if args.roundrobin:
        matrix = {}
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                rows = []
                pa, pb = os.path.join(META_DIR, a + ".py"), os.path.join(META_DIR, b + ".py")
                for s in seeds:
                    # Both directions, and both seats for the first-named agent.
                    # Passing seat=1 here is what actually moves `a` to seat 1;
                    # swapping the arguments instead would pin both agents.
                    rows.append(play(load(pa), load(pb), s, 0))
                    rows.append(play(load(pa), load(pb), s, 1))
                r = summarise(rows, f"{a} vs {b}")
                wa = sum(1 for x in rows if x.get("win"))
                wb = sum(1 for x in rows if "error" not in x and x.get("loss"))
                matrix[(a, b)] = (wa, wb)
                print(json.dumps(r))
        rates = bradley_tery(matrix)
        print("\nraw win-rate ordering:")
        for t, v in sorted(rates.items(), key=lambda kv: -kv[1]):
            print(f"  {t:16s} {v:.3f}")
        if args.json:
            json.dump({f"{a}|{b}": v for (a, b), v in matrix.items()},
                      open(args.json, "w"), indent=2)
        return

    opps = [args.opp] if args.opp else names
    cand_sha = hashlib.sha256(open(os.path.abspath(args.cand), "rb").read()).hexdigest()
    allrows = []
    for o in opps:
        opp_path = os.path.join(META_DIR, o + ".py")
        if os.path.exists(opp_path) and \
                hashlib.sha256(open(opp_path, "rb").read()).hexdigest() == cand_sha:
            # Same bytes as the candidate: a mirror match, not evidence.
            print(json.dumps({"label": f"vs {o}", "skipped": "identical to candidate"}))
            continue
        try:
            r = head_to_head(args.cand, o, seeds)
        except Exception as exc:  # noqa: BLE001
            r = {"label": f"vs {o}", "games": 0, "errors": 1,
                 "error_samples": [repr(exc)[:180]], "win_rate": 0.0}
        allrows.append(r)
        print(json.dumps(r))
    g = sum(r["games"] for r in allrows)
    w = sum(r["W"] for r in allrows)
    l = sum(r["L"] for r in allrows)
    t = sum(r["T"] for r in allrows)
    lo, hi = wilson(w, g)
    overall = {"label": "OVERALL", "games": g, "W": w, "L": l, "T": t,
               "opponents_scored": len(allrows),
               "win_rate": round(w / g, 4) if g else 0.0,
               "score_rate": round((w + 0.5 * t) / g, 4) if g else 0.0,
               "wilson95": [lo, hi],
               "errors": sum(r.get("errors", 0) for r in allrows)}
    print(json.dumps(overall, indent=2))
    if args.json:
        json.dump({"per_opponent": allrows, "overall": overall},
                  open(args.json, "w"), indent=2)


if __name__ == "__main__":
    main()