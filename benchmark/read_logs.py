"""Summarise a Kaggle agent log file for a validation episode."""
import json
import statistics
import sys

path = sys.argv[1]
d = json.load(open(path, encoding="utf-8"))
print("entries:", len(d))
print("shape of first entry:", type(d[0]), (d[0] if not isinstance(d[0], list) else d[0][:2]))


def flatten(obj):
    if isinstance(obj, dict):
        return [obj]
    if isinstance(obj, list):
        out = []
        for x in obj:
            out.extend(flatten(x))
        return out
    return []


entries = flatten(d)
print("flattened entries:", len(entries))
if entries:
    print("keys:", sorted(entries[0].keys()))

durs = [e.get("duration") for e in entries if isinstance(e.get("duration"), (int, float))]
if durs:
    ds = sorted(durs)
    print("agent call duration: median %.4fs p95 %.4fs max %.4fs"
          % (statistics.median(ds), ds[int(len(ds) * 0.95)], ds[-1]))

errs = [e for e in entries if (e.get("stderr") or "").strip()]
outs = [e for e in entries if (e.get("stdout") or "").strip()]
print("entries with stderr:", len(errs))
print("entries with stdout:", len(outs))
for e in errs[:6]:
    print("--- stderr ---")
    print(e["stderr"][:600])
for e in outs[:6]:
    print("--- stdout ---")
    print(e["stdout"][:600])