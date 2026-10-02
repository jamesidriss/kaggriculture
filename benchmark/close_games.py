"""Mine close games and locate the first decision divergence.

Filters results by |cash margin| and re-simulates both agents turn by turn to
find where their trajectories separate by more than a threshold.

Usage:
  python benchmark/close_games.py <a.py> <b.py> --seeds 8 --margin 5000 [--trace]
"""
import argparse
import importlib.util

from kaggle_environments import make
from kaggle_environments.envs.kaggriculture import kaggriculture as KG

BUILTIN = {"starter": KG.starter_agent, "random": KG.random_agent, "pass": KG.pass_agent}

ELITE_SEEDS = [335464115, 846389409, 1184506355, 955895442, 725584983,
               146290260, 1437887509, 1975378019, 1254813745, 943761968]


def load(p):
    if p in BUILTIN:
        return BUILTIN[p]
    s = importlib.util.spec_from_file_location("c_" + str(abs(hash(p))), p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m.agent


def count(obs, seat):
    f = obs["farms"][seat]
    c = {"plant": 0, "animal": 0, "weed": 0, "empty": 0,
         "money": f["money"], "quads": len(f["unlocked_quadrants"])}
    for row in f["tiles"]:
        for t in row:
            if t is None:
                c["empty"] += 1
            elif t == "LOCKED":
                continue
            elif t.get("kind") == "PLANT":
                c["plant"] += 1
            elif t.get("kind") == "WEED":
                c["weed"] += 1
            elif t.get("animal"):
                c["animal"] += 1
    c["shed"] = sum(v for v in obs["private"]["shed"].values() if isinstance(v, int))
    return c


def play(agent0, agent1, seed):
    """One full game; returns (cash0, cash1, traj0, traj1).

    Each agent receives the framework's genuine observation object.
    """
    env = make("kaggriculture", configuration={"seed": seed, "episodeSteps": 720})
    env.reset()
    t0, t1 = [], []

    def wrap(idx, agent, sink):
        """Capture the observation the framework DELIVERS, not the persisted
        snapshot. env.steps[i][1].observation omits shared fields (e.g. `step`),
        which manufactured a false 'seat 1 has no step' failure earlier."""
        def _a(obs, configuration=None):
            if len(sink) < 719:
                sink.append(count(obs, idx))
            return agent(obs, configuration)
        return _a

    env.run([wrap(0, agent0, t0), wrap(1, agent1, t1)])
    f = env.steps[-1]
    cash = [int(f[i].observation.farms[i]["money"]) for i in range(2)]
    return cash, t0, t1


def first_divergence(t0, t1, money_thr=3000, tiles_thr=6):
    for i, (x, y) in enumerate(zip(t0, t1)):
        if abs(x["money"] - y["money"]) > money_thr:
            return i, "money", int(x["money"] - y["money"])
        if abs(x["plant"] - y["plant"]) > tiles_thr:
            return i, "plant_tiles", x["plant"] - y["plant"]
        if abs(x["animal"] - y["animal"]) > tiles_thr:
            return i, "animal_tiles", x["animal"] - y["animal"]
        if abs(x["shed"] - y["shed"]) > 20:
            return i, "shed", x["shed"] - y["shed"]
    return None, None, None


def print_full(traj, label, upto=24):
    print(f"  {label} step  money  land plant animal weed  shed")
    for i in range(min(upto, len(traj))):
        t = traj[i]
        print(f"  {label} {i:4d} {int(t['money']):8d} {t['quads']:5d} "
              f"{t['plant']:5d} {t['animal']:6d} {t['weed']:5d} {t['shed']:5d}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("a")
    ap.add_argument("b")
    ap.add_argument("--seeds", type=int, default=8)
    ap.add_argument("--margin", type=int, default=5000)
    ap.add_argument("--trace", action="store_true")
    args = ap.parse_args()

    seeds = ELITE_SEEDS[: args.seeds]
    a, b = load(args.a), load(args.b)
    print(f"{'seed':>11} {'seat':>4} {'A$':>9} {'B$':>9} {'margin':>9}  W/L  divergence")
    rows = []
    for sd in seeds:
        # seat 0: A is player 0.  seat 1: A is player 1 (engine order swapped).
        cash, ta, tb = play(a, b, sd)
        ca, cb = cash
        i, kind, val = first_divergence(ta, tb)
        rows.append((sd, 0, ca, cb, ca - cb, "W" if ca > cb else "L", i, kind, val, ta, tb))
        print(f"{sd:>11} {0:>4} {ca:9d} {cb:9d} {ca - cb:9d}  "
              f"{'W' if ca > cb else 'L'}  {f'{kind}@step{i} ({val:+})' if i is not None else 'none'}")

        cash, tb2, ta2 = play(b, a, sd)   # A now in seat 1
        ca1, cb1 = cash[1], cash[0]
        i, kind, val = first_divergence(ta2, tb2)
        rows.append((sd, 1, ca1, cb1, ca1 - cb1, "W" if ca1 > cb1 else "L",
                     i, kind, val, ta2, tb2))
        print(f"{sd:>11} {1:>4} {ca1:9d} {cb1:9d} {ca1 - cb1:9d}  "
              f"{'W' if ca1 > cb1 else 'L'}  {f'{kind}@step{i} ({val:+})' if i is not None else 'none'}")

    close = [r for r in rows if abs(r[4]) < args.margin]
    print(f"\nclose games (|margin| < ${args.margin:,}): {len(close)}/{len(rows)}")
    losses = sorted([r for r in rows if r[5] == "L"], key=lambda r: abs(r[4]))
    if losses:
        r = losses[0]
        print(f"closest loss: seed {r[0]} seat {r[1]} margin {r[4]} "
              f"({r[2]} vs {r[3]})  divergence {r[7]}@step{r[6]} ({r[8]:+})")
    margins = sorted(abs(r[4]) for r in rows)
    for thr in (50, 100, 500, 1000, 5000):
        k = sum(1 for m in margins if m < thr)
        print(f"  decided by <${thr}: {k}/{len(margins)} ({k / len(margins):.0%})")
    if args.trace:
        print()
        print_full(rows[0][9], "A")
        print_full(rows[0][10], "B")


if __name__ == "__main__":
    main()