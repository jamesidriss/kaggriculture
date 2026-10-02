"""RANK1 generation release gate.

Mostly NEGATIVE-result guards. The value of this file is that it makes the
generation's failures impossible to forget. If a later run "fixes" the Rust parity
result by loosening a tolerance, promotes a candidate that actually scores 0.054
against Moon, or relabels Moon as an independent lineage, these checks fail.

Every assertion reads a committed artifact. None re-run a simulation, because a
gate that depends on a 60-minute run is a gate that will be skipped.

Run:  python tests/test_gate_rank1.py
"""
import csv
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILED = []
N = 0


def check(label, cond, detail=""):
    global N
    N += 1
    print(("  PASS  " if cond else "  FAIL  ") + label
          + (f"   {detail}" if detail else ""))
    if not cond:
        FAILED.append(label)


def P(*a):
    return os.path.join(ROOT, *a)


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def J(*a):
    with open(P(*a), encoding="utf-8") as fh:
        return json.load(fh)


def main():
    print("=" * 78)
    print("RANK1 GATE")
    print("=" * 78)

    # ------------------------------------------------------------ champion
    print("\n-- champion --")
    # NOTE: the key is `agent_sha`, not `sha256`. Guessing the field name here
    # is exactly the recurring failure class this project keeps hitting.
    cur = J("champions", "research", "CURRENT.json")
    check("champion pointer names the frozen artifact",
          cur["champion_id"] == "C001_room_guard")
    check("champion digest matches frozen bytes",
          sha(P("champions", "research", "C001_room_guard", "main.py"))
          == cur["agent_sha"])
    check("submission_ready is byte-identical to the champion",
          sha(P("submission_ready", "main.py"))
          == sha(P("champions", "research", "C001_room_guard", "main.py")))
    check("champion is still the immutable C001",
          sha(P("submission_ready", "main.py"))
          == "a52ba1bfe9df9dc1d504550af46744ef8d474797cdba7af2412"
             "dc40a3ebdf3b8",
          "champions are immutable")

    # ------------------------------------------------------------ moon
    print("\n-- moon licence and lineage --")
    prov = J("research", "moon_provenance.json")
    lic = prov["licence_audit"]
    check("moon licence audit is present", bool(lic))
    check("moon licence verdict is UNKNOWN",
          all(r["licence_verdict"] == "UNKNOWN" for r in lic.values()),
          "an Apache body is not a grant; re-audit before any reuse")
    check("audit premise: an Apache body IS present in the files",
          all(r["apache_body_in_file"] for r in lic.values()))
    check("at least 4 licence blockers recorded per artifact",
          all(len(r["blockers_to_reuse"]) >= 4 for r in lic.values()),
          "provenance was re-opened without a decision")
    check("broken derivation chain is named",
          all("queue_compact.py" in r["missing_parent_works"]
              for r in lic.values()))

    with open(P("research", "FINAL_PUBLIC_AGENT_CATALOG.csv"),
              encoding="utf-8") as fh:
        cat = [r for r in csv.DictReader(fh) if r["agent_name"].startswith("moon")]
    check("both moon artifacts are catalogued", len(cat) == 2, f"{len(cat)} rows")
    check("catalogued moon licence is UNKNOWN",
          all(r["license"] == "UNKNOWN" for r in cat))
    check("catalogued moon is NOT league eligible",
          all(r["league_eligible"] == "no" for r in cat))
    check("moon lineage recorded as NOT independent",
          all("not independent" in r["lineage"].lower() for r in cat),
          "identifier Jaccard 0.719 vs C001; it descends from the v9/3 root")
    check("moon lineage cites the v9/3 root",
          all("v9/3" in r["lineage"] for r in cat))

    with open(P("opponents", "meta", "MANIFEST.csv"), encoding="utf-8") as fh:
        man = [r for r in csv.DictReader(fh) if r["name"].startswith("moon")]
    check("manifest excludes moon from the league",
          bool(man) and all(r["league_eligible"] == "no" for r in man))

    print("\n-- moon field payoff --")
    pay = prov["payoff"]["moon_parent"]
    check("moon is broadly dominant, not a narrow counter",
          all(pay[o]["bt_score"] > 0.85 for o in ("C001", "v51", "farm_2945")),
          " ".join(f"{o} {pay[o]['bt_score']}" for o in ("C001", "v51",
                                                        "farm_2945")))
    check("no broken games in the payoff run",
          all(pay[o]["broken"] == 0 for o in pay if pay[o]))

    # ------------------------------------------------------------ ablation
    print("\n-- ablation method and result --")
    abl = J("simulation", "rank1", "ablation2", "ablation2_results.json")
    res = abl["results"]
    # A SKIPPED ablation (no reachable def site) has no score and no probe
    # result. It must be excluded, not counted as a failure -- but it must also
    # not be silently forgotten, so its existence is checked separately.
    skipped = [r["name"] for r in res if r.get("error")]
    ran = [r for r in res if not r.get("error")]
    check("ablation SKIPs are labelled, not silently dropped",
          all(r.get("error") for r in res if r.get("playable") is None),
          f"skipped: {skipped}")
    check("every ablation that ran was applied at the binding site",
          all("def site replaced" in r.get("note", "") for r in ran
              if r.get("note") != "unmodified control"),
          "appending a shim into a 43-deep wrapper chain measures nothing")
    check("every ablation that ran passed the playability probe",
          all(r.get("playable") is True for r in ran),
          "a broken agent scored 0-80 and once reported as a mechanism")
    by = {r["name"]: (r.get("result") or {}).get("bt_score") for r in res}
    base = by["control_null"]
    check("control reproduced", base is not None, f"BT {base}")
    check("v9 OPENING is material",
          by["opening_pass_through"] < base - 0.5,
          f"{base} -> {by['opening_pass_through']}")
    for inert in ("race_update_off", "carrot_off", "herd_off"):
        check(f"{inert} remains inert", abs(by[inert] - base) < 1e-9,
              "these layers are dead code; do not resurrect them by name")

    # ------------------------------------------------------------ transplant
    print("\n-- transplant negative result --")
    tr = J("simulation", "rank1", "transplant",
           "transplant_results.json")["results"]
    scored = [r for r in tr if r.get("vs_moon") and r.get("vs_farm")]
    check("all transplant candidates were scored", len(scored) == len(tr),
          f"{len(scored)}/{len(tr)}")
    best_moon = max(r["vs_moon"]["bt"] for r in scored)
    check("no transplant candidate reaches the 0.45 Moon gate",
          best_moon < 0.45, f"best {best_moon}")
    check("no transplant candidate clears both pre-declared gates",
          not any(r["vs_moon"]["bt"] >= 0.45 and r["vs_farm"]["bt"] >= 0.52
                  for r in scored))
    check("no broken games in the sweep",
          all(r["vs_moon"]["broken"] == 0 and r["vs_farm"]["broken"] == 0
              for r in scored))
    destroyed = [r["name"] for r in scored if r["vs_farm"]["bt"] < 0.10]
    check("net-buy variants destroyed the Farm matchup", bool(destroyed),
          f"{len(destroyed)} candidates collapsed to 0.0000")
    survivors = [r for r in scored if r["vs_farm"]["bt"] >= 0.50]
    collapsed = [r for r in scored if r["vs_farm"]["bt"] < 0.10]

    # The accurate rule is NOT "cash-neutrality". A net buy of MILK survived.
    # What kills C001 is an opening that consumes the cash OR the market-order
    # capacity that C001's own WHEAT plan needs at step 2 (BUY_PRODUCT WHEAT 30,
    # five hires, two livestock purchases). So survival requires either a
    # non-negative net outlay, OR a product that does not collide with C001's
    # own purchases. The first version of this gate asserted plain cash-neutrality
    # and was refuted by the MILK candidate.
    def survivable(r):
        c = r["config"]
        return c["s"] >= c["q"] or c["product"] != "WHEAT"

    check("every collapsed candidate violates the cash/order-collision rule",
          all(not survivable(r) for r in collapsed),
          f"{len(collapsed)} collapsed")
    check("every surviving candidate satisfies it",
          all(survivable(r) for r in survivors),
          f"{len(survivors)} survivors")
    check("a net buy of a NON-colliding product survives",
          any(r["config"]["s"] < r["config"]["q"]
              and r["config"]["product"] != "WHEAT" for r in survivors),
          "MILK refutes plain cash-neutrality; keep the gate honest")
    check("no collapsed candidate used a non-colliding product",
          all(r["config"]["product"] == "WHEAT" for r in collapsed))

    # ------------------------------------------------------------ rust
    print("\n-- rust parity gate --")
    par = J("simulation", "rust", "parity_results.json")
    check("rust parity is NOT verified", par["status"] != "PARITY_VERIFIED",
          par["status"])
    check("rust divergences recorded", par.get("divergences", 0) > 0)
    da = J("simulation", "rust", "day_alignment.json")
    check("day alignment reports NO_GO", da["verdict"].startswith("NO_GO"),
          da["verdict"])
    check("final banks agree on every tape",
          da["banks_agree"] == da["trajectories"],
          f"{da['banks_agree']}/{da['trajectories']}")
    neither = sum(1 for x in da["detail"] if x["verdict"] == "neither")
    check("intermediate state still diverges despite bank agreement",
          neither > 0,
          f"{neither} tapes; final-bank agreement alone would be a FALSE PASS")
    check("rust has zero harness errors",
          sum(1 for x in da["detail"] if x["verdict"] == "ERROR") == 0)
    try:
        import kaggle_environments as K
        pyf = os.path.join(os.path.dirname(K.__file__), "envs", "kaggriculture",
                           "kaggriculture.py")
        check("installed environment matches the tool's pin",
              sha(pyf) == "bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463"
                         "f23bccee653e",
              "a version drift would explain the divergence away")
    except Exception as e:
        check("installed environment matches the tool's pin", False, str(e))

    # ------------------------------------------------------------ calibration
    print("\n-- calibration gate --")
    with open(P("research", "EXACT_SCORE_ANCHORS.csv"), encoding="utf-8") as fh:
        anchors = list(csv.DictReader(fh))
    check("anchor ledger is non-empty", bool(anchors))
    check("no class-A anchors exist",
          all(r["binding_class"] != "A" for r in anchors),
          f"{sum(1 for r in anchors if r['binding_class'] == 'A')} class A")
    md = open(P("reports", "SHADOW_LADDER_V3.md"), encoding="utf-8").read()
    check("shadow rating is WITHHELD", "WITHHELD" in md)
    check("the 3125 target is shown as untestable, not claimed",
          "3125" in md and "UNTESTABLE" in md.upper())

    print("\n-- forbidden claims --")
    bad = []
    for name in sorted(os.listdir(P("reports"))):
        if not name.endswith(".md"):
            continue
        text = open(P("reports", name), encoding="utf-8",
                    errors="ignore").read()
        for m in re.finditer(r"(will be #1|will be rank-1|guaranteed rank|"
                             r"beat the entire field|stronger than every public)",
                             text, re.I):
            bad.append(f"{name}: {m.group(0)}")
    check("no unsupported rank-1 claim in any report", not bad, "; ".join(bad))
    check("RANK-1 READY is stated as NO",
          "RANK-1 READY" in open(P("reports", "RANK1_DASHBOARD.md"),
                                 encoding="utf-8").read()
          and "**NO**" in open(P("reports", "RANK1_DASHBOARD.md"),
                               encoding="utf-8").read())

    # ------------------------------------------------------------ ledger
    print("\n-- consolidated ledger --")
    with open(P("experiments", "rank1_results.csv"), encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh) if r["bt_score"]]
    check("ledger has scored rows", bool(rows), f"{len(rows)} rows")
    bad = []
    for r in rows:
        W, L, T = int(r["W"]), int(r["L"]), int(r["T"])
        Nn = W + L + T
        # Round BEFORE comparing. The ledger stores a 4dp value, so comparing it
        # against the unrounded quotient fails on every single row. The first
        # version of this check did exactly that and reported three phantom
        # corruptions in a ledger that was correct.
        want = round((W + 0.5 * T) / Nn, 4)
        if Nn != int(r["valid"]):
            bad.append(f"{r['candidate']}: W+L+T != valid")
        elif abs(want - float(r["bt_score"])) > 1e-9:
            bad.append(f"{r['candidate']}: bt != (W+0.5T)/N")
    check("every ledger bt_score == (W + 0.5T)/N", not bad, "; ".join(bad[:3]))
    check("ledger covers all three experiment families",
          len({r["experiment"] for r in rows}) >= 3,
          ", ".join(sorted({r["experiment"] for r in rows})))

    print("\n" + "=" * 78)
    print(f"{N - len(FAILED)}/{N} checks passed")
    if FAILED:
        print("FAILURES:")
        for f in FAILED:
            print("  -", f)
        return 1
    print("RANK1 GATE PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())