"""Run a native (ctypes/CDLL) public agent from its own bundle directory.

Some strong public agents ship a Python `main.py` that loads a compiled
`agent.so`/`agent.dylib` sibling via ctypes. The library path is resolved
relative to the *Python source file's* directory, so the agent must be loaded
from its bundle directory rather than copied into a flat league folder.

Usage:
  python benchmark/native_agent.py <bundle_dir> <main_py> [seed ...]
"""
import importlib.util
import sys


def load_native(bundle_dir, main_name="main.py"):
    import os
    path = os.path.abspath(os.path.join(bundle_dir, main_name))
    spec = importlib.util.spec_from_file_location("native_agent_" + str(abs(hash(path))), path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.agent.__kag_src__ = os.path.basename(bundle_dir)
    return mod.agent


if __name__ == "__main__":
    sys.path.insert(0, __file__.rsplit("\\", 1)[0])
    from meta import play, summarise, wilson
    import json
    bundle, main_name = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else "main.py")
    seeds = [int(x) for x in sys.argv[3:]] or [335464115, 846389409]
    agent = load_native(bundle, main_name)
    rows = []
    for s in seeds:
        for seat in (0, 1):
            rows.append(play(agent, agent, s, seat))
    print(json.dumps(summarise(rows, f"{bundle} self-play"), indent=1))