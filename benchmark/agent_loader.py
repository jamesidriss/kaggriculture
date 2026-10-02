"""The single correct way to turn an agent file into something env.run accepts.

Two harness bugs in this project both came from writing this by hand:

  1. `mod.agent` returned raw and handed to `env.run()`. Kaggle calls
     `agent(obs, configuration)`; an agent defining `def agent(obs)` then raises
     TypeError on every turn, is marked INVALID, never acts, and finishes on the
     starting $3,000 -- a free 72-0 for the opponent.

  2. `env.steps[i][seat].observation` used as agent input. The framework copies
     shared fields (including `step`) into the observation it DELIVERS but not
     into the snapshot it PERSISTS, so seat 1 appears to lack `step` and agents
     crash with a KeyError that cannot happen on Kaggle.

Every harness in this repository must load agents through `load_agent()`.
"""
import importlib.util
import inspect
import os


def _adapt(fn, src=""):
    """Uniform (obs, configuration) callable + provenance tags."""
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
    """Import an agent file and return a uniform callable."""
    path = os.path.abspath(path)
    name = module_name or ("kag_agent_" + str(abs(hash(path))))
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "agent"):
        raise AttributeError(f"{path} defines no agent(obs) function")
    return _adapt(mod.agent, os.path.basename(path))


def probe_playable(path, env_name="kaggriculture", seed=62857979, verbose=True):
    """Confirm an agent really acts, before trusting any number from it.

    Runs one game against `starter` and reports final cash. An agent frozen on
    the starting bank never played. Returns a dict of evidence.
    """
    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as KG
    calls = {"n": 0}
    fn = load_agent(path)

    def spy(obs, configuration=None):
        calls["n"] += 1
        return fn(obs, configuration)

    env = make(env_name, configuration={"seed": seed, "episodeSteps": 720})
    env.reset()
    env.run([spy, KG.starter_agent])
    f = env.steps[-1]
    cash = [int(f[i].observation.farms[i]["money"]) for i in range(2)]
    out = {"path": path, "src": os.path.basename(path), "turns": calls["n"],
           "cash": cash, "played": calls["n"] > 0 and cash[0] != 3000,
           "two_arg": getattr(fn, "__kag_two_arg__", None)}
    if verbose:
        flag = "OK " if out["played"] else "DEAD"
        print(f"  {flag}  {out['src']:<48} two_arg={out['two_arg']!s:<5} "
              f"turns={out['turns']:<4} cash={cash[0]}")
    return out
