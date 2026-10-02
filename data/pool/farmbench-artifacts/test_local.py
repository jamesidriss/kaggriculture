"""Local checks: (1) exact optima via the graders (prefix of farmbench.py executed without the task cells),
(2) the whole notebook source with the naive stub (expect 0.0) and the best stub (expect 1.0)."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
PY = os.path.join(ROOT, ".venv", "bin", "python")
src = open(os.path.join(HERE, "farmbench.py")).read()
prefix = src.split("# %% [markdown]\n# ## 5. Tasks")[0]
ns = {}; exec(compile(prefix, "farmbench_prefix", "exec"), ns)
best = {}
g = ns["grade_melon_dump"](ns["SellNow"](0, "")); best["melon_dump"] = {"sell_now": g["best_choice"]}; print("melon_dump", g)
g = ns["grade_melon_race"](ns["HarvestDay"](10, "")); best["melon_race_timing"] = {"harvest_day": g["best_choice"]}; print("melon_race", g)
g = ns["grade_wool_lot"](ns["ThreeDayPlan"](30, 0, 0, "")); p = g["best_choice"]; best["wool_lot"] = dict(day27=p[0], day28=p[1], day29=p[2]); print("wool", g)
g = ns["grade_milk_front_run"](ns["HourlyPlan"]([24] + [0] * 23, "")); best["milk_front_run"] = {"units_per_hour": g["best_choice"]}; print("milk", g)
g = ns["grade_crop_choice"](ns["CropChoice"]("NONE", "")); best["crop_choice"] = {"crop": g["best_choice"]}; print("crop", g)
best["hire_math"] = {"hire_more": 1, "extra_cost": 8}; best["feed_or_lose"] = {"feed": ["A", "B", "C"]}
best["fertilizer_melon"] = {"units_with_fertilizer": 6, "units_without_fertilizer": 6, "age_first_full_with_fertilizer": 8}
T = ns["TABLES"]
def arm_val(task, arm):
    import re
    m = re.search(r"(-?\d+)$", arm); return int(m.group(1)) if m else None
if T:
    best["opening"] = {"option": T["opening"]["best"]}
    best["se_quadrant"] = {"option": T["se_quadrant"]["best"]}
    for t in ("sheep_yarn", "sheep_no_yarn", "max_hands", "terminal_tomato", "terminal_carrot"):
        b = T[t]["best"]; best[t] = {"value": -1 if b in ("never", "off") else arm_val(t, b)}
json.dump(best, open(os.path.join(HERE, "stub_answers_best.json"), "w"), indent=1)
print("\nbest answers written:", json.dumps(best)[:400], "...")
import glob, shutil
scores = {}
for mode in ("naive", "best"):
    for f in glob.glob(os.path.join(HERE, "*.run.json")) + glob.glob(os.path.join(HERE, "*.task.json")): os.remove(f)
    shutil.rmtree(os.path.join(HERE, ".cache"), ignore_errors=True)
    env = dict(os.environ, FARMBENCH_STUB=mode, KBENCH_UI_MODE="none", PYTHONPATH=HERE)
    r = subprocess.run([PY, os.path.join(HERE, "farmbench.py")], env=env, capture_output=True, text=True, cwd=HERE)
    tail = [l for l in r.stdout.splitlines() if l.strip()][-30:]
    print(f"\n===== stub {mode} (rc {r.returncode}) =====\n" + "\n".join(tail))
    if r.returncode: print(r.stderr[-1500:])
    m = [l for l in r.stdout.splitlines() if l.startswith("FARMBENCH SCORE:")]
    scores[mode] = float(m[-1].split(":")[1]) if m else None
for f in glob.glob(os.path.join(HERE, "*.run.json")) + glob.glob(os.path.join(HERE, "*.task.json")): os.remove(f)
shutil.rmtree(os.path.join(HERE, ".cache"), ignore_errors=True)
print("SCORES", scores)
# naive: 2 trap tasks where doing nothing IS best (sheep_no_yarn, se_quadrant) + 1/3 of fertilizer_melon = 2.3333/15
exp_naive = (sum(1 for t in T.values() if t["naive"] == t["best"] and t is not T.get("land_ne_timing")) + 1/3) / 15
ok = scores.get("best") == 1.0 and scores.get("naive") is not None and abs(scores["naive"] - exp_naive) < 1e-6
print("expected naive", round(exp_naive, 4))
print("LOCAL TEST", "PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
