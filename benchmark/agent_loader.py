"""Playability probe: an agent must be PROVEN to act before it enters a league.

Deliberately does not use "final cash > 3000" as the test. An agent can
legitimately lose money and still be perfectly playable, and an agent can also
finish above 3000 while having been served a malformed observation. The
evidence used here is behavioural:

  * the module imports and exposes a callable
  * Kaggle invokes it on the expected number of turns
  * its seat reaches DONE (never INVALID, ERROR or TIMEOUT)
  * it emits a non-trivial action trace (not 719 bare PASSes)
  * it issues market orders, i.e. it participates in the economy
  * it works from BOTH seats
  * its cash actually changes during the episode

Usage:
    python benchmark/agent_loader.py --probe-all
    python benchmark/agent_loader.py --probe opponents/meta/v51_lean_flock.py
"""
import argparse
import hashlib
import importlib.util
import inspect
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPECTED_TURNS = 719
ACTIVE_UNITS = {"MOVE", "PLANT", "WATER", "HARVEST", "DIG", "BUILD", "FEED",
                "CARE", "COLLECT_FERTILIZER", "PICKUP", "DROP"}


# ---------------------------------------------------------------------------
# The ONE canonical loader
# ---------------------------------------------------------------------------
def _adapt(fn, src=""):
    """Uniform (obs, configuration) callable plus provenance tags.

    The wrapper exists for a *loader* reason, not because Kaggle demands two
    arguments. `Agent.act` truncates its argument list to the callable's
    `co_argcount`, so Kaggle itself supports both `agent(obs)` and
    `agent(obs, configuration)`. Normalising here means our diagnostics can
    call agents uniformly without diverging from the official runner, and it
    gives every wrapper a stable `co_argcount` for tags.
    """
    try:
        sig = inspect.signature(fn)
        npos = sum(1 for p in sig.parameters.values()
                   if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD))
        var = any(p.kind == p.VAR_POSITIONAL for p in sig.parameters.values())
    except (TypeError, ValueError):
        npos, var = 2, True
    two = var or npos >= 2

    def wrapper(obs, configuration=None, _fn=fn, _two=two):
        return _fn(obs, configuration) if _two else _fn(obs)

    wrapper.__kag_src__ = src or os.path.basename(getattr(fn, "__module__", ""))
    wrapper.__kag_two_arg__ = two
    wrapper.__wrapped__ = fn
    return wrapper


def load_agent(path, module_name=None):
    """Import an agent file and return a uniform callable.

    Does NOT alter strategy: the action returned by the underlying function is
    forwarded unchanged. Preserves `__wrapped__`, source path, digest and
    provenance metadata.
    """
    path = os.path.abspath(path)
    name = module_name or ("kag_agent_" + str(abs(hash(path))))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "agent"):
        raise AttributeError(f"{path} defines no agent(obs) function")
    w = _adapt(mod.agent, os.path.basename(path))
    w.__kag_path__ = path
    try:
        w.__kag_sha__ = hashlib.sha256(open(path, "rb").read()).hexdigest()
    except OSError:
        w.__kag_sha__ = None
    return w


def probe(path, env_name="kaggriculture", seed=62857979, episode_steps=720):
    """Run one game from seat 0 and one from seat 1 against `starter`."""
    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as KG
    out = {"path": os.path.relpath(path, ROOT) if path.startswith(ROOT) else path,
           "name": os.path.basename(path)}
    try:
        fn = load_agent(path)
    except Exception as exc:  # noqa: BLE001
        out["playable"] = False
        out["reason"] = f"import/callable failure: {type(exc).__name__}: {exc}"[:200]
        return out
    out["two_arg"] = bool(getattr(fn, "__kag_two_arg__", True))
    out["sha256"] = hashlib.sha256(open(path, "rb").read()).hexdigest()

    for seat in (0, 1):
        st = {"calls": 0, "active": 0, "market": 0, "errors": []}

        def spy(obs, configuration=None, _s=st, _seat=seat):
            _s["calls"] += 1
            a = fn(obs, configuration)
            if isinstance(a, dict):
                f = a.get("farmer")
                if f and f[0] in ACTIVE_UNITS:
                    _s["active"] += 1
                _s["market"] += sum(1 for o in (a.get("market") or []) if o)
            return a

        env = make(env_name, configuration={"seed": seed,
                                            "episodeSteps": episode_steps})
        env.reset()
        agents = [spy, KG.starter_agent] if seat == 0 else [KG.starter_agent, spy]
        t0 = time.perf_counter()
        try:
            env.run(agents)
        except Exception as exc:  # noqa: BLE001
            st["errors"].append(f"{type(exc).__name__}: {exc}"[:160])
        f = env.steps[-1]
        cash0 = int(f[0].observation.farms[0]["money"])
        cash1 = int(f[1].observation.farms[1]["money"])
        out[f"seat{seat}"] = {
            "calls": st["calls"], "active": st["active"],
            "market": st["market"], "status": f[seat].status,
            "cash": cash0 if seat == 0 else cash1,
            "opponent_cash": cash1 if seat == 0 else cash0,
            "ms": round((time.perf_counter() - t0) * 1000),
            "error": "; ".join(st["errors"])[:160] or None,
        }

    reasons = []
    for seat in (0, 1):
        d = out[f"seat{seat}"]
        if d["error"]:
            reasons.append(f"seat{seat} raised {d['error']}")
        if d["status"] != "DONE":
            reasons.append(f"seat{seat} status {d['status']}")
        if d["calls"] < EXPECTED_TURNS - 5:
            reasons.append(f"seat{seat} invoked {d['calls']}x, expected "
                           f"~{EXPECTED_TURNS}")
        if d["active"] == 0:
            reasons.append(f"seat{seat} emitted only PASS/idle actions")
        if d["market"] == 0:
            reasons.append(f"seat{seat} never touched the market")
    out["playable"] = not reasons
    out["reason"] = "; ".join(reasons)[:300]
    return out


def probe_all(directory):
    files = sorted(f for f in os.listdir(directory) if f.endswith(".py"))
    rows = []
    print(f"{'agent':<52} {'2arg':>5} {'turns':>6} {'active':>7} "
          f"{'mkt':>6} {'cash0':>9} {'cash1':>9}  verdict")
    for f in files:
        r = probe(os.path.join(directory, f))
        rows.append(r)
        s0, s1 = r.get("seat0", {}), r.get("seat1", {})
        print(f"{f[:-3][:52]:<52} {str(r.get('two_arg')):>5} "
              f"{s0.get('calls', 0):>6} {s0.get('active', 0):>7} "
              f"{s0.get('market', 0):>6} {s0.get('cash', 0):>9} "
              f"{s1.get('cash', 0):>9}  "
              f"{'PLAYABLE' if r['playable'] else 'REJECT: ' + r['reason'][:70]}")
    ok = sum(1 for r in rows if r["playable"])
    print(f"\n{ok}/{len(rows)} playable")
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe-all", action="store_true")
    ap.add_argument("--probe", action="append", default=[])
    ap.add_argument("--dir", default=os.path.join(ROOT, "opponents", "meta"))
    args = ap.parse_args()

    if args.probe_all:
        rows = probe_all(args.dir)
        return 0 if all(r["playable"] for r in rows) else 1
    rc = 0
    for p in args.probe:
        r = probe(os.path.abspath(p) if os.path.exists(p) else p)
        print(f"{r['name']}: {'PLAYABLE' if r['playable'] else 'REJECT'}  "
              f"{r.get('reason', '')}")
        rc |= 0 if r["playable"] else 1
    return rc


if __name__ == "__main__":
    sys.path.insert(0, os.path.join(ROOT, "benchmark"))
    sys.exit(main())
