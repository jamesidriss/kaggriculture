"""Collect per-model results of the Kaggle benchmark task from `kaggle benchmarks tasks log` output.
python collect_results.py [--task farm-economy-benchmark] -> results/results.json, results/results.md, results/rationales.md"""
import os, re, json, subprocess, argparse, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
K = os.path.join(ROOT, ".venv", "bin", "kaggle")
FAM = {"hire_math": "sanity", "feed_or_lose": "sanity", "fertilizer_melon": "sanity", "melon_dump": "exact", "melon_race_timing": "exact",
       "wool_lot": "exact", "milk_front_run": "exact", "crop_choice": "exact", "opening": "sim", "sheep_yarn": "sim", "sheep_no_yarn": "sim",
       "se_quadrant": "sim", "max_hands": "sim", "terminal_tomato": "sim", "terminal_carrot": "sim"}
TASKS = list(FAM)

ap = argparse.ArgumentParser(); ap.add_argument("--task", default="farm-economy-benchmark"); a = ap.parse_args()
out = subprocess.run([K, "benchmarks", "tasks", "log", a.task], capture_output=True, text=True).stdout
runs = re.split(r"\n═══ Logs for ", out)[1:]
results = {}; allruns = {}
for chunk in runs:
    head = chunk.split("\n", 1)[0]
    m = re.match(r"(\S+) \(Run (\d+)\) \[(\w+)\]", head)
    if not m: continue
    model, run_id, state = m.group(1), m.group(2), m.group(3)
    per = {}; rat = {}; flags = None; score = None
    for line in chunk.splitlines():
        t = re.match(r"^\s*([a-z_]+)\s+(sanity|exact|sim)\s+(.*?)\s+(\S+)\s+(\S+)\s+(\S+)\s+(.*?)\s+(\d\.\d\d)\s*$", line)
        if t and t.group(1) in FAM:
            per[t.group(1)] = dict(choice=t.group(3).strip(), value=t.group(4), naive=t.group(5), best=t.group(6), best_choice=t.group(7).strip(), score=float(t.group(8)))
        r = re.match(r"^\[([a-z_]+)\] \(score (\d\.\d\d)\) (.*)$", line)
        if r and r.group(1) in FAM:
            rat[r.group(1)] = r.group(3)
        if line.startswith("rationale flags:"):
            flags = json.loads(line.split(":", 1)[1].replace("'", '"'))
        if line.startswith("FARMBENCH SCORE:"):
            try: score = float(line.split(":")[1])
            except ValueError: score = None
    allruns.setdefault(model, {})[run_id] = dict(run_id=run_id, state=state, score=score, flags=flags, per_task=per, rationales=rat)
    if model not in results or int(results[model]["run_id"]) < int(run_id):   # latest run per model for the tables
        results[model] = allruns[model][run_id]

os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
json.dump(results, open(os.path.join(HERE, "results", "results.json"), "w"), indent=1)
json.dump(allruns, open(os.path.join(HERE, "results", "results_all_runs.json"), "w"), indent=1)
# test-retest: choice agreement between the two most recent runs of each model
rr = ["", "| model | runs compared | same choice | score run A | score run B |", "|---|---|---|---|---|"]
for m, d in sorted(allruns.items()):
    ids = sorted(d, key=int)
    if len(ids) < 2: continue
    a, b = d[ids[-2]], d[ids[-1]]
    same = sum(1 for t in TASKS if a["per_task"].get(t, {}).get("choice") == b["per_task"].get(t, {}).get("choice"))
    both = sum(1 for t in TASKS if t in a["per_task"] and t in b["per_task"])
    fa = f"{a['score']:.3f}" if a["score"] is not None else "n/a"; fb = f"{b['score']:.3f}" if b["score"] is not None else "n/a"
    rr.append(f"| {m} | {ids[-2]} vs {ids[-1]} | {same}/{both} | {fa} | {fb} |")
open(os.path.join(HERE, "results", "retest.md"), "w").write("\n".join(rr) + "\n")
print("\n".join(rr))
done = {m: r for m, r in results.items() if r["score"] is not None}
order = sorted(done, key=lambda m: -done[m]["score"])
def fam_mean(r, f):
    v = [x["score"] for t, x in r["per_task"].items() if FAM[t] == f]
    return sum(v) / len(v) if v else float("nan")
lines = ["| model | score | sanity (3) | exact (5) | sim (7) | flags pool / SE / fib / refill |", "|---|---|---|---|---|---|"]
for m in order:
    r = done[m]; f = r["flags"] or {}
    lines.append(f"| {m} | {r['score']:.3f} | {fam_mean(r,'sanity'):.2f} | {fam_mean(r,'exact'):.2f} | {fam_mean(r,'sim'):.2f} | {f.get('pool','-')} / {f.get('se_trap','-')} / {f.get('fibonacci','-')} / {f.get('refill','-')} |")
lines += ["", "| task | " + " | ".join(order) + " |", "|---|" + "---|" * len(order)]
for t in TASKS:
    lines.append(f"| {t} | " + " | ".join(f"{done[m]['per_task'].get(t, {}).get('score', float('nan')):.2f}" for m in order) + " |")
lines += ["", "| task | " + " | ".join(order) + " |", "|---|" + "---|" * len(order)]
for t in TASKS:
    lines.append(f"| {t} (choice) | " + " | ".join(done[m]["per_task"].get(t, {}).get("choice", "-")[:22] for m in order) + " |")
open(os.path.join(HERE, "results", "results.md"), "w").write("\n".join(lines) + "\n")
with open(os.path.join(HERE, "results", "rationales.md"), "w") as fh:
    for t in TASKS:
        fh.write(f"\n## {t}\n")
        for m in order:
            fh.write(f"- **{m}** ({done[m]['per_task'].get(t, {}).get('score', float('nan')):.2f}, chose {done[m]['per_task'].get(t, {}).get('choice', '-')[:30]}): {done[m]['rationales'].get(t, '')}\n")
print("\n".join(lines[:len(order) + 2]))
print(f"\nmodels with results: {len(done)}; errored/pending: {[m for m in results if m not in done]}")
