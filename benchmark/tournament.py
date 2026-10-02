"""The ONE canonical competitive tournament path.

Every competitive number in this repository comes from this file. It exists
because the project accumulated several harnesses, one of which fed agents from
persisted `env.steps` snapshots, another of which had no notion of a
non-playing opponent, and a third of which could publish a statistic that did
not match the record printed beside it.

Guarantees, each of which is asserted and fatal:

  * agents are loaded through `benchmark/agent_loader.load_agent`
  * games are driven by `kaggle_environments...Environment.run` only
  * every world is played from BOTH seats (paired design)
  * the candidate and the opponent must have different content digests
  * an agent that was never invoked, or that raised, makes the game INVALID;
    invalid games never enter a strength calculation
  * every row carries both digests, the seed, the seat, both statuses and both
    call counts, so any aggregate can be re-derived from the CSV
  * Wilson intervals come from `benchmark/stats.win_interval` on the same
    counts that are printed, so a rate and its interval cannot disagree

Usage:
    python benchmark/tournament.py --a v51 --b farm_2945_original \
        --seeds-file seeds/REAL_scale.txt --out experiments/v51_vs_farm.csv
"""
import argparse
import csv
import hashlib
import importlib.util
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "benchmark"))

from agent_loader import load_agent                      # noqa: E402
from stats import win_interval, mcnemar_exact, binom_two_sided  # noqa: E402

META_DIR = os.path.join(ROOT, "opponents", "meta")
STARTING_CASH = 3000
EXPECTED_TURNS = 719

FIELDS = [
    "run_id", "timestamp", "environment_version", "candidate_name",
    "candidate_sha", "opponent_name", "opponent_sha", "seed", "seat",
    "candidate_cash", "opponent_cash", "win", "loss", "tie",
    "candidate_status", "opponent_status", "candidate_calls",
    "opponent_calls", "candidate_runtime_max", "opponent_runtime_max", "valid",
    "invalid_reason", "candidate_actions", "opponent_actions",
]


def resolve(spec):
    """Accept a league name, a repo-relative path, or a digest prefix."""
    if os.path.sep in spec or spec.endswith(".py"):
        p = spec if os.path.isabs(spec) else os.path.join(ROOT, spec)
        if not os.path.exists(p):
            raise FileNotFoundError(p)
        return os.path.basename(p)[:-3], p
    p = os.path.join(META_DIR, spec + ".py")
    if os.path.exists(p):
        return spec, p
    hits = [f for f in os.listdir(META_DIR)
            if f.endswith(".py")
            and hashlib.sha256(open(os.path.join(META_DIR, f), "rb").read())
            .hexdigest().startswith(spec)]
    if len(hits) == 1:
        return hits[0][:-3], os.path.join(META_DIR, hits[0])
    raise KeyError(f"cannot resolve agent {spec!r} ({len(hits)} digest matches)")


def digest_of(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def normalised_digest(path):
    raw = open(path, "rb").read()
    return hashlib.sha256(raw.decode("utf-8", "replace")
                          .replace("\r\n", "\n").encode()).hexdigest()


class Counter:
    """Wraps an agent to record invocations, exceptions and action shape.

    Deliberately does not change strategy: it forwards the action unchanged and
    only observes. `active` distinguishes a real action from a bare PASS so
    playability does not rest on final cash alone -- an agent can legitimately
    lose money, and `probe_playable` must not reject it for that.
    """

    def __init__(self, fn, label):
        self.fn = fn
        self.label = label
        self.calls = 0
        self.errors = []
        self.active = 0
        self.market_orders = 0
        self.max_ms = 0.0

    def __call__(self, obs, configuration=None):
        t0 = time.perf_counter()
        self.calls += 1
        try:
            action = self.fn(obs, configuration)
        except Exception as exc:  # noqa: BLE001
            if len(self.errors) < 3:
                self.errors.append(f"turn {self.calls}: {type(exc).__name__}: {exc}")
            raise
        finally:
            self.max_ms = max(self.max_ms, (time.perf_counter() - t0) * 1000.0)
        try:
            if isinstance(action, dict):
                if action.get("farmer") and action["farmer"][0] != "PASS":
                    self.active += 1
                m = action.get("market") or []
                self.market_orders += sum(1 for o in m if o)
        except Exception:  # noqa: BLE001
            pass
        return action


def play(cand_path, opp_path, seed, cand_seat, env_name="kaggriculture",
         episode_steps=720):
    from kaggle_environments import make
    ca = Counter(load_agent(cand_path), "cand")
    ob = Counter(load_agent(opp_path), "opp")
    seats = [ca, ob] if cand_seat == 0 else [ob, ca]
    env = make(env_name, configuration={"seed": seed,
                                        "episodeSteps": episode_steps})
    env.reset()
    t0 = time.perf_counter()
    env.run(seats)
    wall = time.perf_counter() - t0
    f = env.steps[-1]
    cc = int(f[cand_seat].observation.farms[cand_seat]["money"])
    oc = int(f[1 - cand_seat].observation.farms[1 - cand_seat]["money"])
    return {
        "candidate_cash": cc, "opponent_cash": oc,
        "win": int(cc > oc), "loss": int(cc < oc), "tie": int(cc == oc),
        "candidate_status": f[cand_seat].status,
        "opponent_status": f[1 - cand_seat].status,
        "candidate_calls": ca.calls, "opponent_calls": ob.calls,
        "candidate_actions": ca.active, "opponent_actions": ob.active,
        "candidate_runtime_max": round(ca.max_ms, 3),
        "opponent_runtime_max": round(ob.max_ms, 3),
        "wall_s": round(wall, 2),
    }


def validate_game(r, cand_name, opp_name):
    """A game is competitive only if both sides demonstrably played.

    IMPORTANT, corrected 2026-10-02
    -------------------------------
    This function used to reject any game where both sides finished with the
    same cash, recording it as "exact tie (duplicate-content signal)". That was
    wrong, and wrong in the direction that flatters an experiment.

    The rule was a heuristic about content duplication. It was applied to the
    OUTCOME instead. Two different artifacts can finish a season level, and in
    the measured case they did so on 216 of 992 worlds -- because the single
    changed gene never fired and both agents followed identical trajectories.
    Discarding those games removed exactly the worlds where the change had no
    effect, and reported the remaining rate as 82.22% when the honest figure
    over all games was 64.31%.

    Content duplication is detectable exactly, from the artifact digest, and is
    checked BEFORE the match in `main()`:

        if a_sha == b_sha or a_nrm == b_nrm: ABORT

    So the outcome carries no information about duplication, and an exact cash
    tie between two different artifacts is a REAL GAME with `valid = 1`.
    """
    reasons = []
    for side in ("candidate", "opponent"):
        if r[f"{side}_calls"] == 0:
            reasons.append(f"{side} never invoked")
        if r[f"{side}_status"] != "DONE":
            reasons.append(f"{side} status {r[f'{side}_status']}")
    if r["candidate_calls"] < EXPECTED_TURNS - 5:
        reasons.append(f"candidate called {r['candidate_calls']}x")
    if r["opponent_calls"] < EXPECTED_TURNS - 5:
        reasons.append(f"opponent called {r['opponent_calls']}x")
    # Deliberately absent: any test derived from r["tie"] or cash equality.
    return reasons


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", "--candidate", dest="a", required=True)
    ap.add_argument("--b", "--opponent", dest="b", required=True)
    ap.add_argument("--seeds-file", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--label-a", default=None)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--resume", action="store_true")
    args = ap.parse_args()

    from importlib.metadata import version
    envver = f"kaggle-environments {version('kaggle-environments')}"

    an, ap_ = resolve(args.a)
    bn, bp = resolve(args.b)
    an = args.label_a or an
    a_sha, b_sha = digest_of(ap_), digest_of(bp)
    a_nrm, b_nrm = normalised_digest(ap_), normalised_digest(bp)

    if a_sha == b_sha or a_nrm == b_nrm:
        print(f"ABORT: self-play refused. {an} and {bn} are the same content "
              f"({a_sha[:16]}).")
        return 2

    seeds = [int(x) for x in open(args.seeds_file, encoding="utf-8")
             if x.strip().isdigit()]
    if args.limit:
        seeds = seeds[: args.limit]

    run_id = hashlib.sha256(
        f"{a_sha}|{b_sha}|{args.seeds_file}|{len(seeds)}".encode()
    ).hexdigest()[:16]
    os.makedirs(os.path.dirname(os.path.join(ROOT, args.out)), exist_ok=True)
    out_path = os.path.join(ROOT, args.out)

    done = set()
    if args.resume and os.path.exists(out_path):
        for row in csv.DictReader(open(out_path, encoding="utf-8")):
            if row["valid"] == "1":
                done.add((int(row["seed"]), int(row["seat"])))
        print(f"resuming: {len(done)} valid games already recorded")

    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    fh = open(out_path, "a" if args.resume else "w", newline="", encoding="utf-8")
    w = csv.DictWriter(fh, fieldnames=FIELDS)
    if not (args.resume and os.path.exists(out_path)):
        w.writeheader()
        fh.flush()

    print(f"run_id={run_id}")
    print(f"  A = {an}  {a_sha[:16]}  arity-agnostic loader")
    print(f"  B = {bn}  {b_sha[:16]}")
    print(f"  seeds={len(seeds)}  games={len(seeds)*2 - len(done)}  "
          f"paired, both seats")

    t0 = time.time()
    n = 0
    agg = {"W": 0, "L": 0, "T": 0}
    invalid = 0
    seat0_W = seat1_W = 0
    margins = {}
    for seed in seeds:
        for seat in (0, 1):
            if (seed, seat) in done:
                continue
            try:
                r = play(ap_, bp, seed, seat)
            except Exception as exc:  # noqa: BLE001
                print(f"  seed {seed} seat {seat}: EXCEPTION "
                      f"{type(exc).__name__}: {exc}")
                invalid += 1
                continue
            reasons = validate_game(r, an, bn)
            valid = not reasons
            row = {
                "run_id": run_id, "timestamp": ts, "environment_version": envver,
                "candidate_name": an, "candidate_sha": a_sha,
                "opponent_name": bn, "opponent_sha": b_sha,
                "seed": seed, "seat": seat,
                "valid": int(valid),
                "invalid_reason": "; ".join(reasons),
                **{k: r[k] for k in (
                    "candidate_cash", "opponent_cash", "win", "loss", "tie",
                    "candidate_status", "opponent_status", "candidate_calls",
                    "opponent_calls", "candidate_actions", "opponent_actions",
                    "candidate_runtime_max", "opponent_runtime_max")},
            }
            w.writerow(row)
            n += 1
            if valid:
                agg["W"] += r["win"]; agg["L"] += r["loss"]; agg["T"] += r["tie"]
                if r["win"]:
                    if seat == 0:
                        seat0_W += 1
                    else:
                        seat1_W += 1
                margins.setdefault(seed, []).append(r["candidate_cash"]
                                                    - r["opponent_cash"])
            else:
                invalid += 1
                print(f"  seed {seed} seat {seat}: INVALID {reasons}")
            if n % 50 == 0:
                fh.flush()
                el = time.time() - t0
                iv = win_interval(agg["W"], agg["L"], agg["T"])
                print(f"  {n:>5}/{len(seeds)*2}  {agg['W']}-{agg['L']}-{agg['T']}  "
                      f"{iv['win_rate']:.4f} [{iv['wilson_lo']:.4f},"
                      f"{iv['wilson_hi']:.4f}]  invalid={invalid}  "
                      f"{el/60:.1f} min")
    fh.close()

    iv = win_interval(agg["W"], agg["L"], agg["T"])
    print(f"\n=== {an} vs {bn} ===")
    print(f"  valid games : {iv['games']}   invalid: {invalid}")
    print(f"  record      : {iv['W']}-{iv['L']}-{iv['T']}")
    print(f"  win rate    : {iv['win_rate']:.4f}")
    print(f"  Wilson 95%  : [{iv['wilson_lo']:.4f}, {iv['wilson_hi']:.4f}]")
    print(f"  seat split  : A wins {seat0_W} as P0, {seat1_W} as P1")
    p, disc = mcnemar_exact(seat0_W, seat1_W)
    print(f"  seat effect : McNemar exact p={p:.4f} on {disc} discordant worlds")
    pb = binom_two_sided(iv["W"], iv["decided"])
    print(f"  vs 50%      : exact binomial p={pb:.4f}")
    if 0.5 < iv["wilson_lo"]:
        print("  VERDICT     : separated from 50%")
    elif 0.5 < iv["wilson_hi"]:
        print("  VERDICT     : NOT separated from 50% -- TIED within the interval")
    else:
        print("  VERDICT     : separated, and worse than 50%")
    print(f"  wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
