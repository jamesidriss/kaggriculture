"""Make a public Kaggriculture agent seat-safe by removing hard `step` reads.

The official observation schema does NOT declare `step`. The interpreter only
sets it on player 0, so any agent that does `int(observation["step"])` raises
KeyError when it plays seat 1 and dies immediately.

This rewrites every such read to the agent's own safe accessor when one exists,
otherwise to a day*24+hour reconstruction (which is numerically identical to
`step` because turnsPerDay is 24).

Usage:
  python research/seat_safe_patch.py <in.py> <out.py> --dry
"""
import argparse
import re
import sys

# Preferred safe accessors, in order, if the file defines them.
SAFE = ["_step_of(observation)", "_step(observation)"]
RECON = "(int(observation.get('day', 0)) * 24 + int(observation.get('hour', 0)))"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst", nargs="?")
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    src = open(args.src, encoding="utf-8").read()
    safe = next((s for s in SAFE if re.search(r"def " + s.split("(")[0] + r"\(", src)), None)

    # Matches int(observation["step"]), observation['step'], observation.get("step")
    pats = [
        (r'int\(\s*observation\s*\[\s*["\']step["\']\s*\]\s*\)', f"int({safe or RECON})"),
        (r'observation\s*\[\s*["\']step["\']\s*\]', f"({safe or RECON})"),
        (r'int\(\s*observation\.get\(\s*["\']step["\']\s*,\s*0\s*\)\s*\)',
         f"int({safe or RECON})"),
    ]
    out = src
    total = 0
    for p, rep in pats:
        out, n = re.subn(p, rep, out)
        total += n
    # Observation[ "step" ] forms with spaces are covered above; also handle
    # `_get(observation, "step")` which is already safe (no change).
    print(f"rewrote {total} hard step read(s); safe accessor = {safe or 'day*24+hour'}")
    if args.dry:
        return
    open(args.dst or args.src, "w", encoding="utf-8", newline="").write(out)
    print(f"wrote {args.dst or args.src}")


if __name__ == "__main__":
    main()