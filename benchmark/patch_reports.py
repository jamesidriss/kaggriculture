"""One-off: append the final-pass corrections to two reports.

Kept as a script rather than a hand edit so the text that goes into the reports
is reviewable and the operation is repeatable.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SUNRISE_NOTE = """## 1b. Reconfirmation on the corrected harness

Because a harness bug previously produced a false 72-win record for this very
agent, the 0-792 result was re-verified rather than assumed. Sunrise is a
one-argument agent, and the retracted explanation ("Kaggle requires two
arguments") was false; what is true is that our own diagnostics invoked agents
directly. Re-run through the canonical runner with the behavioural playability
probe: **719 invocations, seat status DONE in both seats, a non-trivial action
trace, and real market activity.** Sunrise genuinely plays, and genuinely loses.
See `reports/RETRACTIONS.md` R1.

"""

BARNYARD_NOTE = """> **Correction (final pass).** This report originally rested on a
> counterfactual executed while Barnyard was believed not to be playing. That
> belief was wrong (`reports/RETRACTIONS.md` R1): Barnyard always played, and the
> 0-144 record below is genuine. The counterfactual has been re-run on the
> canonical harness and the conclusion is unchanged — the patched agent
> finishes at **$74,991, identical to the dollar across 24 games** — but it is
> now measured rather than carried forward. Barnyard is also ineligible as a
> redistributable champion because the author declared no licence.

"""


def patch(path, anchor, note, before=True):
    p = os.path.join(ROOT, path)
    s = open(p, encoding="utf-8").read()
    if note.strip()[:60] in s:
        print(f"  already patched: {path}")
        return
    if anchor not in s:
        print(f"  ANCHOR MISSING in {path}: {anchor!r}")
        return
    s = s.replace(anchor, (note + anchor) if before else (anchor + note), 1)
    with open(p, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(s)
    print(f"  patched {path}")


def main():
    patch("reports/SUNRISE_FINAL_AUTOPSY.md", "## 2. Corrected local record",
          SUNRISE_NOTE)
    patch("reports/BARNYARD_INVERSION.md", "## The inversion", BARNYARD_NOTE,
          before=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
