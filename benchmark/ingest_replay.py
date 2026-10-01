"""Ingest a Kaggle ladder replay into the episode database.

Identifies OUR seat by feeding recorded observations to our exact submitted
agent and comparing outputs to recorded actions (no env stepping needed).
Extracts seed, teams, rewards, shops, and any marketParams overrides.

Usage:
  python benchmark/ingest_replay.py <replay.json> <our_agent.py> <our_submission_id> [our_label]
Appends to data/final_evaluation_episodes.csv and prints the row as JSON.
"""
import csv
import hashlib
import importlib.util
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(ROOT, "data", "final_evaluation_episodes.csv")
COLS = ["episode_id", "timestamp", "our_submission", "our_seat", "opponent_team",
        "opponent_cash", "our_cash", "result", "seed", "market_params_override",
        "final_shops", "replay_file"]


def load_agent(path):
    spec = importlib.util.spec_from_file_location("our_agent", os.path.abspath(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.agent


def norm(action):
    """Normalize an action for comparison (order-insensitive market list)."""
    if not isinstance(action, dict):
        return None
    try:
        mkt = action.get("market", [])
        return (json.dumps(action.get("farmer"), sort_keys=True),
                json.dumps(action.get("hands"), sort_keys=True),
                json.dumps(sorted([json.dumps(o, sort_keys=True) for o in mkt])))
    except Exception:
        return None


def main():
    replay_path, agent_path, our_sub = sys.argv[1], sys.argv[2], sys.argv[3]
    label = sys.argv[4] if len(sys.argv) > 4 else our_sub
    d = json.load(open(replay_path, encoding="utf-8"))
    agent = load_agent(agent_path)

    info = d.get("info", {})
    seed = info.get("seed")
    teams = info.get("TeamNames", ["?", "?"])
    rewards = d.get("rewards", [None, None])
    steps = d.get("steps", [])
    cfg = d.get("configuration", {})
    ts = None
    ep_id = info.get("EpisodeId") or os.path.basename(replay_path)

    # Seat identification: match our agent's outputs against recorded actions.
    # Replay layout: steps[t]['action'] is the action computed FROM the
    # observation at steps[t-1] (action lags observation by one step).
    scores = [0, 0]
    tested = 0
    for st in range(min(40, len(steps) - 1)):
        for seat in (0, 1):
            try:
                obs = steps[st][seat]["observation"]
                rec = steps[st + 1][seat]["action"]
            except (KeyError, IndexError, TypeError):
                continue
            try:
                out = agent(obs)
            except Exception:
                continue
            if norm(out) == norm(rec):
                scores[seat] += 1
            tested += 1
    total = scores[0] + scores[1]
    our_seat = 0 if scores[0] >= scores[1] else 1
    conf = (max(scores) / 40.0) if tested else 0.0

    our_cash = rewards[our_seat]
    opp_cash = rewards[1 - our_seat]
    result = "W" if our_cash > opp_cash else ("L" if our_cash < opp_cash else "T")

    # Final shops from last step observation.
    try:
        final_shops = steps[-1][our_seat]["observation"]["town"]["unlocked_shops"]
    except (KeyError, IndexError):
        final_shops = []
    mp = cfg.get("marketParams") or cfg.get("marketparams")

    row = {
        "episode_id": ep_id, "timestamp": "",
        "our_submission": label, "our_seat": our_seat,
        "opponent_team": teams[1 - our_seat],
        "opponent_cash": opp_cash, "our_cash": our_cash, "result": result,
        "seed": seed, "market_params_override": json.dumps(mp) if mp else "",
        "final_shops": json.dumps(sorted(final_shops)),
        "replay_file": os.path.basename(replay_path),
    }
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    new = not os.path.exists(DB)
    with open(DB, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        if new:
            w.writeheader()
        w.writerow(row)
    row["_seat_match"] = f"{scores[0]}-vs-{scores[1]} conf={conf:.2f}"
    print(json.dumps(row, indent=1))


if __name__ == "__main__":
    main()