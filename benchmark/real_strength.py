"""Real-strength analysis of the active bots from ladder episodes.

Buckets opponents by final cash (directly measured game strength; opponent
ratings are not exposed in replay JSON, only team names). Reports W/L/T, win
rate with Wilson 95% CI, median cash and margin per bucket.
"""
import csv
import math
import statistics
import sys

BUCKETS = [(0, 3000, "0-3000 (passive/broken)"),
           (3001, 6000, "3001-6000 (weak)"),
           (6001, 10000, "6001-10000 (mid)"),
           (10001, 15000, "10001-15000 (strong)"),
           (15001, 10**12, "15001+ (very strong)")]


def wilson(w, n, z=1.96):
    """Rounded to 3dp for this report; canonical definition in stats.py."""
    from stats import wilson as _w
    lo, hi = _w(w, n, z)
    return (round(lo, 3), round(hi, 3))


def main(path="data/final_evaluation_episodes.csv"):
    rows = [r for r in csv.DictReader(open(path, encoding="utf-8"))]
    bots = sorted({r["our_submission"] for r in rows})
    md = []
    for bot in bots:
        br = [r for r in rows if r["our_submission"] == bot]
        n = len(br)
        w = sum(1 for r in br if r["result"] == "W")
        md.append(f"## {bot}: {w}W-{n-w}L in {n} sampled ladder games")
        md.append("")
        md.append("| opponent bucket | games | W-L | win rate | Wilson 95% | our median $ | opp median $ | median margin |")
        md.append("|---|---|---|---|---|---|---|---|")
        for lo, hi, label in BUCKETS:
            b = [r for r in br if lo <= float(r["opponent_cash"]) <= hi]
            if not b:
                md.append(f"| {label} | 0 | - | - | - | - | - | - |")
                continue
            bw = sum(1 for r in b if r["result"] == "W")
            oc = [float(r["our_cash"]) for r in b]
            op = [float(r["opponent_cash"]) for r in b]
            mg = [float(r["our_cash"]) - float(r["opponent_cash"]) for r in b]
            wl, wh = wilson(bw, len(b))
            md.append(f"| {label} | {len(b)} | {bw}-{len(b)-bw} | {bw/len(b):.2f} | "
                      f"[{wl}, {wh}] | {statistics.median(oc):.0f} | "
                      f"{statistics.median(op):.0f} | {statistics.median(mg):+.0f} |")
        md.append("")
        s0 = [r for r in br if r["our_seat"] == "0"]
        s1 = [r for r in br if r["our_seat"] == "1"]
        for s, nm in ((s0, "seat 0"), (s1, "seat 1")):
            sw = sum(1 for r in s if r["result"] == "W")
            md.append(f"- {nm}: {sw}W-{len(s)-sw}L in {len(s)}")
        md.append("")
    sys.stdout.write("\n".join(md) + "\n")


if __name__ == "__main__":
    main(*sys.argv[1:])