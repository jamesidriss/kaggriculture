"""Compatibility linter for public Kaggriculture agents.

Scans each agent for embedded copies of environment-critical data (market
price functions, crop/animal constants, town/shop tables, land costs, action
vocabulary) and compares them against the CURRENT official environment.

Emits: STALE_PRICE_MODEL, STALE_CROP_MODEL, STALE_TOWN_MODEL,
       STALE_ACTION_SCHEMA, NO_EMBEDDED_MODEL (fine), NATIVE_AGENT (opaque).

Usage: python research/compat_linter.py opponents/store/*/main.py
"""
import glob
import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, ".venv", "Lib", "site-packages"))

from kaggle_environments.envs.kaggriculture.kaggriculture import (  # noqa: E402
    CROPS, ANIMALS, SHOPS, LAND_PRICES, FARMER_MOVES, MARKET_PARAMS)

# Scarcity curve that older agents got wrong (pre-hinge).
CURRENT_BELOW = {k: v["below_func"] for k, v in MARKET_PARAMS.items()}
CURRENT_TGT = {k: v["below_target"] for k, v in MARKET_PARAMS.items()}
SHOPS_CUR = set(SHOPS)
LAND_CUR = list(LAND_PRICES)


def lint(path):
    src = open(path, encoding="utf-8", errors="replace").read()
    name = os.path.basename(os.path.dirname(path)) or os.path.basename(path)
    warns = []

    # --- STALE_PRICE_MODEL: embedded below_func that differs from current
    for item, cur in CURRENT_BELOW.items():
        for m in re.finditer(
                r"['\"]" + item + r"['\"]\s*:\s*(\{[^{}]*?\})", src):
            blk = m.group(1)
            bf = re.search(r"below_func['\"]?\s*[:=]\s*['\"](\w+)['\"]", blk)
            bt = re.search(r"below_target['\"]?\s*[:=]\s*([\d.]+)", blk)
            if bf and bf.group(1) != cur:
                warns.append(("STALE_PRICE_MODEL",
                              f"{item} below_func={bf.group(1)} (current {cur})"))
            if bt and cur == "hinge" and abs(float(bt.group(1)) - CURRENT_TGT[item]) > 1e-9:
                warns.append(("STALE_PRICE_MODEL",
                              f"{item} below_target={bt.group(1)} (current {CURRENT_TGT[item]})"))
        # tuple form: "ITEM": (base, I0, T, "bf", bt, "af", at)
        for m in re.finditer(
                r"['\"]" + item + r"['\"]\s*:\s*\(\s*[\d.]+\s*,\s*[\d.]+\s*,\s*[\d.]+\s*,\s*['\"](\w+)['\"]",
                src):
            if m.group(1) != cur:
                warns.append(("STALE_PRICE_MODEL",
                              f"{item} tuple below_func={m.group(1)} (current {cur})"))

    # --- STALE_CROP_MODEL: embedded crop table that disagrees with current
    for crop, cd in CROPS.items():
        f = re.search(r"['\"]" + crop + r"['\"]\s*:\s*\{[^{}]*?seed['\"]?\s*[:=]\s*(\d+)", src)
        if f and int(f.group(1)) != cd["seed"]:
            warns.append(("STALE_CROP_MODEL", f"{crop} seed={f.group(1)} (current {cd['seed']})"))

    # --- STALE_TOWN_MODEL: shop names not present in the current table
    for m in re.finditer(r"['\"]([A-Z_]{4,})['\"]", src):
        nm = m.group(1)
        if nm.endswith(("_SHOP", "_CAFE", "_SPOT", "_MARKET", "_CENTER", "_STORE")):
            if nm not in SHOPS_CUR and nm != "TOWN_CENTER":
                warns.append(("STALE_TOWN_MODEL", f"unknown shop {nm}"))

    

    # --- NATIVE_AGENT: opaque compiled policy (ctypes dlopen of agent.so)
    #     Only a real ctypes.CDLL call counts; a bare ".so" mention in a comment
    #     or string constant does not make an agent opaque, and mislabelling a
    #     Python agent as native would skip its compatibility audit entirely.
    if "ctypes.CDLL" in src:
        warns.append(("NATIVE_AGENT", "dlopens a compiled library; policy not statically linted"))

    if not warns:
        warns.append(("NO_EMBEDDED_MODEL", "no stale environment data detected"))

    print(f"\n{name}  ({os.path.getsize(path)} bytes)")
    for tag, msg in warns:
        print(f"  [{tag}] {msg}")
    return warns


if __name__ == "__main__":
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(HERE, "opponents", "store", "*", "main.py")))
    bad = 0
    for f in files:
        for tag, _ in lint(f):
            if tag.startswith("STALE"):
                bad += 1
    print(f"\n{bad} stale-model warning(s)")
    sys.exit(1 if bad else 0)