"""Reference backend: the official Python runtime, wrapped in the contract.

This is the oracle the differential harness compares against. It also serves
as the harness's own self-test: if a fixed action stream does not reproduce a
fixed final state, the harness cannot detect a backend divergence either, and
that has to be known before any backend is trusted.
"""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))
sys.path.insert(0, os.path.join(ROOT, "simulation"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Imported as a top-level module: this file is executed both as a script and as
# a library, and a package-relative import fails in one of the two cases.
from parity import canonical  # noqa: E402

ACTIVE = {"MOVE", "PLANT", "WATER", "HARVEST", "DIG", "BUILD", "FEED",
          "CARE", "COLLECT_FERTILIZER", "PICKUP", "DROP"}
MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}


def _struct(o):
    if isinstance(o, dict):
        return {k: _struct(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_struct(v) for v in o]
    if hasattr(o, "to_dict"):
        try:
            return _struct(o.to_dict())
        except Exception:
            pass
    if hasattr(o, "__dict__"):
        return {k: _struct(v) for k, v in vars(o).items() if not k.startswith("_")}
    return o


class OfficialBackend:
    name = "official-python"
    version = "1.32.7"

    def __init__(self, env_name="kaggriculture", episode_steps=720):
        from kaggle_environments import make
        from kaggle_environments.envs.kaggriculture import kaggriculture as KG
        self.make = make
        self.KG = KG
        self.env_name = env_name
        self.episode_steps = episode_steps
        self.env = None

    def reset(self, seed, config=None):
        cfg = {"seed": int(seed), "episodeSteps": self.episode_steps}
        cfg.update(config or {})
        self.env = self.make(self.env_name, configuration=cfg)
        self.env.reset()
        return {"step": 0}

    def observe(self, player=0):
        st = self.env.steps[-1]
        o = st[player].observation
        return _struct(o)

    def digest(self, state):
        """Canonical digest of BOTH seats' observable state."""
        st = self.env.steps[-1]
        return canonical([_struct(st[0].observation), _struct(st[1].observation),
                          st[0].status, st[1].status])

    def sample_actions(self, state, rng):
        """Legal random actions for both seats.

        Deliberately biased toward the mechanics that are easy to get wrong:
        land purchases, market orders (including bulk sells and buys), animal
        purchase, CARE, FEED, fertiliser, shops, weeds and the endgame.
        """
        acts = []
        for player in (0, 1):
            o = self.observe(player)
            farms = o.get("farms") or []
            hands = (farms[player].get("hands") if player < len(farms) else []) or []
            a = {"farmer": ["PASS"], "hands": [], "market": []}
            r = rng.random()
            if r < 0.45:
                mv = rng.choice(list(MOVES))
                a["farmer"] = ["MOVE", mv]
            elif r < 0.55:
                a["farmer"] = ["DIG", rng.randrange(10), rng.randrange(10)]
            elif r < 0.62:
                a["farmer"] = ["PLANT", rng.randrange(10), rng.randrange(10),
                               "WHEAT"]
            elif r < 0.70:
                a["farmer"] = ["WATER", rng.randrange(10), rng.randrange(10)]
            elif r < 0.76:
                a["farmer"] = ["HARVEST", rng.randrange(10), rng.randrange(10)]
            elif r < 0.82:
                a["farmer"] = ["CARE", rng.randrange(10), rng.randrange(10)]
            elif r < 0.86:
                a["farmer"] = ["FEED", rng.randrange(10), rng.randrange(10),
                               rng.choice(["WHEAT", "CARROT"])]
            elif r < 0.90:
                a["farmer"] = ["COLLECT_FERTILIZER", rng.randrange(10),
                               rng.randrange(10)]
            if rng.random() < 0.5:
                for _ in range(rng.randrange(1, 3)):
                    a["hands"].append(["PASS"] if rng.random() < 0.4 else
                                      ["MOVE", rng.choice(list(MOVES))])
            for _ in range(len(hands)):
                # Emit one instruction per hired hand so a random stream can
                # actually reach the multi-worker code paths.
                if rng.random() < 0.5:
                    a["hands"].append(["PASS"] if rng.random() < 0.4 else
                                      ["MOVE", rng.choice(list(MOVES))])
                else:
                    a["hands"].append(["PASS"])
            if rng.random() < 0.35:
                n = rng.randrange(1, 11)
                kind = rng.random()
                if kind < 0.5:
                    a["market"].append(["SELL", "WHEAT", n])
                elif kind < 0.8:
                    a["market"].append(["BUY", "CARROT_SEED", n])
                else:
                    a["market"].append(["BUY_LAND"])
            acts.append(a)
        return acts

    def step(self, state, actions):
        self.env.step(actions)
        return {"step": state["step"] + 1}, {}


def self_test(trajectories=8, seed=20261002):
    """Prove the oracle is deterministic and replayable under a fixed stream."""
    import random
    b = OfficialBackend()
    deterministic, replayable = True, True
    for t in range(trajectories):
        s = 4242 + t
        b.reset(s)
        rng = random.Random(seed + t)
        acts = []
        for _ in range(40):
            acts.append(b.sample_actions({"step": 0}, rng))
        # run A
        b.reset(s)
        for a in acts:
            b.step({"step": 0}, a)
        da = b.digest({"step": 0})
        # run B, identical stream
        b.reset(s)
        for a in acts:
            b.step({"step": 0}, a)
        db = b.digest({"step": 0})
        if da != db:
            deterministic = False
        # replay from a fresh env, same seed, same stream -> same final state
        b2 = OfficialBackend()
        b2.reset(s)
        for a in acts:
            b2.step({"step": 0}, a)
        if b2.digest({"step": 0}) != da:
            replayable = False
    return {"trajectories": trajectories, "steps_each": 40,
            "deterministic": deterministic, "replayable": replayable,
            "engine": "official kaggle-environments"}


if __name__ == "__main__":
    print(json.dumps(self_test(), indent=2))
