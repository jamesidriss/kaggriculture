"""Write real ladder-derived seed splits from elite replay-DB games."""
import subprocess
import sys

out = subprocess.run(
    [sys.executable, "benchmark/replaydb_query.py", "2900", "30"],
    capture_output=True, text=True, cwd="C:/Users/James/kaggriculture").stdout
seeds = []
for line in out.splitlines():
    if "seed=" in line:
        seeds.append(line.split("seed=")[1].split()[0])
print(f"elite seeds collected: {len(seeds)}")
# Deterministic split; FINAL untouched until the end.
dev, hold, final = seeds[:10], seeds[10:20], seeds[20:30]
open("seeds/ladder_real_dev.txt", "w").write("\n".join(dev) + "\n")
open("seeds/ladder_real_holdout.txt", "w").write("\n".join(hold) + "\n")
open("seeds/ladder_real_final.txt", "w").write("\n".join(final) + "\n")
print(f"dev={len(dev)} holdout={len(hold)} final={len(final)}")
print("dev head:", dev[:3])