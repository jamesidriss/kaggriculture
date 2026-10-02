"""Machine-readable snapshot of the CURRENT official environment, hashed.

Every constant an analysis depends on is read from the installed package, never
from a public agent's embedded copy. An agent carrying a stale constant is the
reason the previous project's market analysis was wrong twice.

The snapshot is hashed and the hash is committed, so a report can state exactly
which rules produced its numbers.
"""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_DIR = os.path.join(ROOT, "simulation", "official")
OUT = os.path.join(OUT_DIR, "environment_snapshot.json")

ACTION_UNITS = ["MOVE", "PLANT", "WATER", "HARVEST", "DIG", "BUILD", "FEED",
                "CARE", "COLLECT_FERTILIZER", "PICKUP", "DROP", "PASS"]


def snapshot():
    import kaggle_environments
    from importlib.metadata import version
    pkg = os.path.dirname(kaggle_environments.__file__)
    j = os.path.join(pkg, "envs", "kaggriculture", "kaggriculture.json")
    raw = json.load(open(j, encoding="utf-8"))

    def val(k):
        v = raw.get("configuration", {}).get(k)
        return v.get("default") if isinstance(v, dict) else v

    from kaggle_environments.envs.kaggriculture import kaggriculture as KG
    consts = {}
    for name in dir(KG):
        if not name.isupper():
            continue
        v = getattr(KG, name)
        if isinstance(v, (int, float, bool, str)):
            consts[name] = v
        elif isinstance(v, (dict, list, tuple)) and 0 < len(v) <= 64:
            try:
                consts[name] = json.loads(json.dumps(v, default=str))
            except Exception:
                consts[name] = str(v)[:400]

    return {
        "kaggle_environments_version": version("kaggle-environments"),
        "package_path": pkg,
        "env_json": os.path.relpath(j, ROOT).replace("\\", "/"),
        "env_name": raw.get("name"),
        "env_version_field": raw.get("version"),
        "python": sys.version.split()[0],
        "configuration": {k: val(k) for k in (
            "episodeSteps", "turnsPerDay", "boardSize", "startingMoney",
            "maxMarketOrdersPerTurn", "shedCapacity", "weedSpawnChance",
            "townShopUnlockInterval", "townShopSellInterval",
            "townCenterSellInterval", "farmHandCostMult", "actTimeout",
            "runTimeout")},
        "module_constants": consts,
        "action_units": ACTION_UNITS,
        "provenance": {
            "source": "read from the installed kaggle_environments package",
            "never_from": "a public agent's embedded constants",
            "why": "an agent carrying a stale constant produced two wrong "
                   "market analyses in this project",
        },
    }


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    s = snapshot()
    body = json.dumps(s, indent=2, sort_keys=True, default=str)
    h = hashlib.sha256(body.encode()).hexdigest()
    s["snapshot_sha256"] = h
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(s, fh, indent=2, sort_keys=True, default=str)
    print("ENVIRONMENT SNAPSHOT")
    print(f"  kaggle-environments : {s['kaggle_environments_version']}")
    print(f"  python              : {s['python']}")
    c = s["configuration"]
    for k in ("episodeSteps", "turnsPerDay", "boardSize", "startingMoney",
              "maxMarketOrdersPerTurn", "shedCapacity", "weedSpawnChance",
              "townShopUnlockInterval", "townShopSellInterval",
              "farmHandCostMult", "actTimeout"):
        print(f"    {k:<26} {c.get(k)}")
    print(f"  module constants    : {len(s['module_constants'])}")
    print(f"  snapshot sha256     : {h}")
    print(f"  wrote {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
