"""Real challengers: single-flag edits of the reference's live settings.

Finding that made this possible
-------------------------------
The reference declares `DEFAULT_SETTINGS` (line 263) with almost everything
enabled, but the agent is actually constructed as

    _IMPL = make_agent(_ROUTES, router=_router, **_SETTINGS)      # line 968

and `Planner.__init__` does `self.cfg = dict(DEFAULT_SETTINGS)` followed by
`self.cfg.update(settings)`. So `_SETTINGS` WINS. Editing DEFAULT_SETTINGS is a
no-op, which is exactly what the first attempt did: all four "challengers"
produced byte-identical cash and action traces to the parent, proving they
changed nothing. The live configuration is a *reduced* one:

    _SETTINGS = {'hand_align': True, 'weed_reap': True, 'sell_lead': True,
                 'budget_guard': False, 'room_guard': False,
                 'clamp_sells': False, 'dead_stock': False,
                 'terminal_liquidation': False, 'front_run': False}

so the real single-variable experiments are: switch `sell_lead` off, and switch
each of the four disabled layers on. Each edit is a targeted single-occurrence
replacement in `_SETTINGS`, verified to fire exactly once and to change the
observed behaviour (a challenger that produces byte-identical cash to the
parent is a no-op and is rejected, not reported as a tie).

Promotion requires paired evidence against BOTH top agents, and a 2-point
baseline cannot be resolved by a screening sample, so the two-stage protocol
below is mandatory rather than optional.
"""
import hashlib
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHAL = os.path.join(ROOT, "challengers")
PARENT = os.path.join(ROOT, "opponents", "meta",
                      "ahmedberatozer-v51-lean-flock.py")
PARENT_SHA = "c1e3590d02e42d16091c5377e87a3db16496e5a462d558dc2925887f835f9891"

# (tag, flag, from, to, why it is worth testing)
ABLATIONS = [
    ("challenger_001", "sell_lead", "True", "False",
     "H1 sale timing, primary lever. sell_lead is the only market layer the "
     "agent actually runs. If switching it OFF helps, the agent is leading its "
     "own sales into its own competition and the missing piece is a proper "
     "market-order model rather than a one-turn lead."),
    ("challenger_002", "terminal_liquidation", "False", "True",
     "H1 sale timing, endgame lever. Off in the live config. If switching it ON "
     "helps, unsold shed stock is worth more converted at step >= 718, which is "
     "precisely where 59% of top-two games are decided."),
    ("challenger_003", "clamp_sells", "False", "True",
     "H1 sale sizing. Off in the live config. If clamping helps, the agent is "
     "overselling into a thin market and losing price on volume."),
    ("challenger_004", "front_run", "False", "True",
     "H2 opponent-conditioned selling. Off in the live config, and the hook "
     "exists. If enabling it helps, the opponent's revealed plan is "
     "exploitable, which is the one genuinely new source of information "
     "available."),
]


def main():
    src = open(PARENT, encoding="utf-8", newline="").read()
    got = hashlib.sha256(src.encode()).hexdigest()
    assert got == PARENT_SHA, (
        f"parent digest drift: {got[:16]} != {PARENT_SHA[:16]}")
    if "'sell_lead': True" not in src:
        print("ABORT: the live _SETTINGS block no longer has the expected shape")
        return 2
    os.makedirs(CHAL, exist_ok=True)
    print(f"parent verified: {got[:16]}  ({len(src)} bytes)")
    print(f"live _SETTINGS occurrences of 'sell_lead': True = "
          f"{src.count(chr(39) + 'sell_lead' + chr(39) + ': True')}")

    made = []
    for tag, flag, frm, to, why in ABLATIONS:
        needle = f"'{flag}': {frm},"
        n = src.count(needle)
        if n != 1:
            print(f"  SKIP {tag}: {needle!r} occurs {n} times, expected 1")
            continue
        out = src.replace(needle, f"'{flag}': {to},")
        name = f"{tag}_{flag}_{frm.lower()}_to_{to.lower()}.py"
        path = os.path.join(CHAL, name)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(out)
        d = hashlib.sha256(out.encode()).hexdigest()
        made.append((tag, name, flag, d, path, frm, to, why))
        with open(os.path.join(CHAL, f"{tag}.md"), "w", encoding="utf-8",
                  newline="\n") as fh:
            fh.write(
                f"# {tag} — `{flag}` {frm} → {to}\n\n{why}\n\n"
                f"- parent: `ahmedberatozer-v51-lean-flock` `{PARENT_SHA}`\n"
                f"- change: **one** value in the live `_SETTINGS` dict, "
                f"verified to occur exactly once\n"
                f"- challenger sha256: `{d}`\n"
                f"- screening: `experiments/challenger_screen.csv`\n"
                f"- promotion: requires improvement against BOTH v51 and the "
                f"2945 Farm on a large paired sample. A screening sample cannot "
                f"resolve a 2-point effect, so no promotion is granted on "
                f"screening alone.\n")
        print(f"  {tag}  {name:<46} {d[:16]}")

    with open(os.path.join(CHAL, "challengers.json"), "w", encoding="utf-8",
              newline="\n") as fh:
        json.dump({"parent_sha256": PARENT_SHA, "parent": PARENT,
                   "challengers": [
                       {"tag": t, "file": n, "flag": f, "from": fr, "to": to,
                        "sha256": d,
                        "path": os.path.relpath(p, ROOT).replace("\\", "/"),
                        "hypothesis": w}
                       for t, n, f, d, p, fr, to, w in made]}, fh, indent=2)
    print(f"\n{len(made)} single-variable challengers built.")
    return 0 if made else 1


if __name__ == "__main__":
    sys.exit(main())
