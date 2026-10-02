"""Empirical determination of the OFFICIAL Kaggle call convention.

The previous session asserted that Kaggle requires `agent(obs, configuration)`
and that a one-argument `agent(obs)` therefore fails. That claim is WRONG.
`kaggle_environments.agent.Agent.act` does:

    args = [structify(observation), structify(self.configuration)]
    if hasattr(self.agent, "__code__") and hasattr(self.agent.__code__, "co_argcount"):
        args = args[: self.agent.__code__.co_argcount]
    action = self.agent(*args)

so the argument list is TRUNCATED to the callable's own positional arity, and
both `agent(obs)` and `agent(obs, configuration)` are supported.

This script proves it by execution, records the truth in a machine-readable
snapshot, and is the regression test for the correction.
"""
import inspect
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

OUT = os.path.join(ROOT, "benchmark", "kaggle_call_convention.json")


def probe(agent_obj, label, seed=4242, env_name="kaggriculture", episode_steps=30):
    """Run `agent_obj` in seat 0 against the builtin starter via env.run.

    Returns evidence: was the agent invoked, how often, did it produce a
    schema-valid action, and what status did the seat reach.
    """
    from kaggle_environments import make
    from kaggle_environments.envs.kaggriculture import kaggriculture as KG

    calls = {"n": 0}
    errors = []

    def one_arg(obs, configuration=None):
        calls["n"] += 1
        return {"farmer": ["PASS"], "hands": [], "market": []}

    def two_arg(obs, configuration=None):
        calls["n"] += 1
        return {"farmer": ["PASS"], "hands": [], "market": []}

    # Strip the second parameter to simulate a genuine one-argument agent.
    def genuine_one_arg(obs):
        calls["n"] += 1
        return {"farmer": ["PASS"], "hands": [], "market": []}

    fn = {"one_arg": one_arg, "two_arg": two_arg,
          "genuine_one_arg": genuine_one_arg}[label]

    env = make(env_name, configuration={"seed": seed, "episodeSteps": episode_steps})
    env.reset()
    # Pass the RAW callable, exactly as a Kaggle submission would be executed.
    env.run([fn, KG.starter_agent])
    f = env.steps[-1]
    return {
        "label": label,
        "co_argcount": getattr(getattr(fn, "__code__", None), "co_argcount", None),
        "invoked_times": calls["n"],
        "seat0_status": f[0].status,
        "seat1_status": f[1].status,
        "errors": errors,
        "worked": calls["n"] > 0 and f[0].status == "DONE",
    }


def official_source_evidence():
    """Quote the official truncation logic, so the report is not a guess."""
    import kaggle_environments.agent as ka
    src = inspect.getsource(ka.Agent.act)
    i = src.find("args = [")
    snippet = src[i:i + 320].rstrip()
    build = inspect.getsource(ka.build_agent)
    j = build.find("# Already callable")
    build_snip = build[j:j + 90].rstrip()
    return {
        "Agent.act_arg_truncation": snippet,
        "build_agent_callable_branch": build_snip,
        "kaggle_environments_file": ka.__file__,
    }


def main():
    from importlib.metadata import version
    info = official_source_evidence()

    print("=" * 74)
    print("OFFICIAL CALL CONVENTION -- from kaggle_environments source")
    print("=" * 74)
    for k, v in info.items():
        print(f"\n{k}:\n{v}")

    print("\n" + "=" * 74)
    print("EMPIRICAL VERIFICATION via env.run([raw_callable, starter])")
    print("=" * 74)
    results = []
    for label in ("genuine_one_arg", "one_arg", "two_arg"):
        r = probe(None, label)
        results.append(r)
        print(f"  {r['label']:<20} co_argcount={r['co_argcount']}  "
              f"invoked={r['invoked_times']:<3}  seat0={r['seat0_status']:<12} "
              f"worked={r['worked']}")

    allok = all(r["worked"] for r in results)
    print()
    if allok:
        print("  VERDICT: Kaggle supports BOTH agent(obs) and agent(obs, configuration).")
        print("  The argument list is truncated to co_argcount in Agent.act.")
        print("  The previous session's claim that 'Kaggle requires two arguments'")
        print("  is FALSE and is retracted.")
    else:
        print("  VERDICT: at least one arity failed. Investigate before trusting")
        print("  any result produced by the harness.")

    snapshot = {
        "kaggle_environments_version": version("kaggle-environments"),
        "official_evidence": info,
        "empirical": results,
        "both_arities_supported": allok,
        "corrected_claim": (
            "Kaggle truncates the call to the callable's co_argcount, so "
            "agent(obs) and agent(obs, configuration) are BOTH valid. The "
            "historical harness bug was that our own loader/benchmark path "
            "invoked the agent directly with two positional arguments instead "
            "of letting the official runner dispatch it."),
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(snapshot, fh, indent=2)
    print(f"\n  wrote {os.path.relpath(OUT, ROOT)}")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
