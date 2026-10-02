"""Did the ORIGINAL benchmark path actually break 1-arg agents?

The previous session concluded that barnyard_v7, v16_rc5 and sunrise-v5 were
"never invoked" because Kaggle requires two arguments. That reason is now
retracted: `Agent.act` truncates the argument list to `co_argcount`, so a raw
one-argument callable passed to `env.run` works.

But the DATA changed when the adapter was added, so something must have
differed. This script isolates it by running each one-argument agent three
ways against the identical seed:

  A. raw callable straight into env.run   (what the original meta.py did)
  B. two-argument wrapper into env.run    (what the current adapter does)
  C. direct invocation fn(obs, config)    (what simcomp's first cut did)

If A works, the original results were sound and the previous session's
"correction" was solving a different bug. If A is inert, this script shows why.
"""
import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

SEED = 62857979
STEPS = 720
AGENTS = [
    ("opponents/meta/v16_rc5.py", "v16_rc5"),
    ("opponents/meta/barnyard_v7.py", "barnyard_v7"),
    ("main.py", "sunrise-v5"),
    ("opponents/meta/ahmedberatozer-v51-lean-flock.py", "v51 (control)"),
    ("opponents/meta/farm_2945_original.py", "farm_2945 (control)"),
]


def raw_agent(path):
    spec = importlib.util.spec_from_file_location("raw_" + os.path.basename(path)[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.agent


def arity(fn):
    code = getattr(fn, "__code__", None)
    return getattr(code, "co_argcount", None)


def run(label, a0, a1, calls):
    from kaggle_environments import make
    env = make("kaggriculture", configuration={"seed": SEED, "episodeSteps": STEPS})
    env.reset()
    env.run([a0, a1])
    f = env.steps[-1]
    return {
        "path": label,
        "cash": [int(f[i].observation.farms[i]["money"]) for i in range(2)],
        "status": [f[i].status for i in range(2)],
        "calls": calls["n"],
    }


def main():
    from kaggle_environments.envs.kaggriculture import kaggriculture as KG
    rows = []
    for path, name in AGENTS:
        fn = raw_agent(path)
        n = arity(fn)

        # A. raw callable into env.run
        ca = {"n": 0}
        fn_a = fn
        if n == 1:
            def fn_a(obs):  # keep genuine 1-arg shape
                ca["n"] += 1
                return fn(obs)
        else:
            def fn_a(obs, configuration=None):
                ca["n"] += 1
                return fn(obs, configuration)
        a = run("A raw->env.run", fn_a, KG.starter_agent, ca)

        # B. 2-arg wrapper into env.run
        cb = {"n": 0}
        def fn_b(obs, configuration=None):
            cb["n"] += 1
            return fn(obs) if n == 1 else fn(obs, configuration)
        b = run("B wrapper->env.run", fn_b, KG.starter_agent, cb)

        # C. direct 2-arg invocation (no env.run dispatch)
        cc = {"n": 0}
        err = []
        def fn_c(obs, configuration=None):
            cc["n"] += 1
            try:
                return fn(obs, configuration) if n >= 2 else fn(obs)
            except TypeError as exc:
                err.append(str(exc))
                return {"farmer": ["PASS"], "hands": [], "market": []}
        c = run("C direct", fn_c, KG.starter_agent, cc)

        rows.append((name, n, a, b, c))
        print(f"{name:<22} co_argcount={n}")
        for lbl, r in (("A raw -> env.run", a), ("B wrapper -> env.run", b),
                       ("C direct call", c)):
            print(f"    {lbl:<22} calls={r['calls']:<5} cash={r['cash'][0]:<9} "
                  f"status={r['status'][0]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
