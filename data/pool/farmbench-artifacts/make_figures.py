"""Figures for the DEV post: cover (1000x420), arithmetic-vs-strategy dumbbell, SE-quadrant waffle.

    ../../.venv/bin/python make_figures.py      -> images/*.png
Reads results/results.md (version 5) and the engine price function embedded in farmbench.py.
"""
import os, re, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "images"); os.makedirs(OUT, exist_ok=True)

for f in ("/System/Library/Fonts/Avenir Next.ttc", "/System/Library/Fonts/Palatino.ttc", "/System/Library/Fonts/Menlo.ttc"):
    if os.path.exists(f): fm.fontManager.addfont(f)
BODY, DISPLAY, MONO = "Avenir Next", "Palatino", "Menlo"

# palette: cool field-green neutrals, two validated series hues (dataviz reference slots 1-2)
GROUND = "#f2f5f0"; INK = "#16221b"; INK2 = "#4d5a52"; MUTED = "#8a968e"; RULE = "#d5ddd6"
EXACT = "#2a78d6"; STRAT = "#eb6834"

NAMES = {
    "gemini-3.7-flash": "Gemini 3.7 Flash", "gpt-6-astra": "GPT-6 Astra", "gemma-4-31b-it": "Gemma 4 31B",
    "claude-opus-5-default": "Claude Opus 5", "gemini-3.8-flash": "Gemini 3.8 Flash",
    "claude-sonnet-5-default": "Claude Sonnet 5", "gemini-2.5-flash": "Gemini 2.5 Flash", "glm-5": "GLM-5",
    "gpt-5.5-2026-04-23": "GPT-5.5", "gemini-2.5-pro": "Gemini 2.5 Pro", "claude-opus-4-8-default": "Claude Opus 4.8",
    "grok-4.20-0309-reasoning": "Grok 4.20 Reasoning", "gpt-oss-20b": "gpt-oss-20b",
    "claude-sonnet-4-5-20250929": "Claude Sonnet 4.5", "gpt-5.4-mini-2026-03-17": "GPT-5.4 mini",
    "gemini-3.1-flash-lite-preview": "Gemini 3.1 Flash-Lite", "gpt-oss-120b": "gpt-oss-120b",
    "gpt-5.4-nano-2026-03-17": "GPT-5.4 nano", "claude-haiku-4-5-20251001": "Claude Haiku 4.5",
}
NEWEST = {"GPT-6 Astra", "Claude Opus 5", "Claude Sonnet 5", "Gemini 3.8 Flash"}


def load_scores():
    rows = []
    for line in open(os.path.join(HERE, "results", "results.md")):
        m = re.match(r"\| (\S+) \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \| ([\d.]+) \|", line)
        if m and m.group(1) in NAMES and float(m.group(2)) > 0:
            rows.append((NAMES[m.group(1)], float(m.group(2)), float(m.group(4)), float(m.group(5))))
        if line.startswith("| task |"): break
    return rows


def style(ax):
    ax.set_facecolor(GROUND)
    for s in ax.spines.values(): s.set_visible(False)
    ax.tick_params(colors=INK2, length=0)


def dumbbell(rows):
    rows = sorted(rows, key=lambda r: r[1])          # lowest at the bottom
    fig = plt.figure(figsize=(10, 9.2), dpi=200, facecolor=GROUND)
    ax = fig.add_axes([0.25, 0.07, 0.70, 0.76]); style(ax)
    ys = range(len(rows))
    for x in (0, 0.25, 0.5, 0.75, 1.0):
        ax.axvline(x, color=RULE, lw=0.8, zorder=0)
    for y, (name, total, ex, st) in zip(ys, rows):
        ax.plot([ex, st], [y, y], color=MUTED, lw=2, solid_capstyle="round", zorder=1)
        dy = 0.14 if abs(ex - st) < 0.03 else 0.0          # coincident scores: stack the two dots
        ax.scatter([ex], [y + dy], s=90, color=EXACT, edgecolor=GROUND, linewidth=2, zorder=3)
        ax.scatter([st], [y - dy], s=90, color=STRAT, edgecolor=GROUND, linewidth=2, zorder=3)
        ax.text(1.08, y, f"{total:.2f}", va="center", ha="left", fontsize=10.5, family=MONO, color=INK2)
    ax.set_yticks(list(ys))
    ax.set_yticklabels([r[0] for r in rows], fontsize=11.5, family=BODY)
    for lab, r in zip(ax.get_yticklabels(), rows):
        lab.set_color(INK); lab.set_fontweight("bold" if r[0] in NEWEST else "normal")
    ax.set_xlim(-0.03, 1.2); ax.set_ylim(-0.8, len(rows) - 0.3)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0]); ax.set_xticklabels(["0", "0.25", "0.50", "0.75", "1.0"], family=MONO, fontsize=10)
    ax.text(1.08, len(rows) - 0.1, "overall", fontsize=10, family=BODY, color=MUTED, ha="left", va="bottom")
    fig.text(0.04, 0.955, "Perfect at the arithmetic, not at the strategy", fontsize=21, family=DISPLAY, color=INK, weight="bold")
    fig.text(0.04, 0.918, "FarmBench score per model: the 5 exact market tasks (engine price curve, brute-force optimum) vs the",
             fontsize=11, family=BODY, color=INK2)
    fig.text(0.04, 0.895, "7 strategy tasks (menus played out in 472 offline games). 1.0 = engine-optimal. Bold = newest frontier models.",
             fontsize=11, family=BODY, color=INK2)
    # legend with swatches
    lx = 0.25
    for col, lab in ((EXACT, "exact market (5 tasks)"), (STRAT, "strategy (7 tasks)")):
        fig.patches.append(matplotlib.patches.Circle((lx, 0.862), 0.006, color=col, transform=fig.transFigure, figure=fig))
        fig.text(lx + 0.014, 0.856, lab, fontsize=10.5, family=BODY, color=INK)
        lx += 0.24
    fig.text(0.04, 0.02, "Kaggle model proxy, temperature 0, task version 5, 26-27 Sep 2026, one run per model. Differences under ~0.05 are noise.",
             fontsize=9, family=BODY, color=MUTED)
    p = os.path.join(OUT, "arithmetic_vs_strategy.png"); fig.savefig(p, facecolor=GROUND); plt.close(fig); return p


def melon_curve():
    """Melon price vs units sold into the market from neutral inventory, with the engine's own function."""
    src = open(os.path.join(HERE, "farmbench.py")).read()
    ns = {}
    # execute only the engine block (constants + market_price), which is plain data and arithmetic
    block = "import math\n" + src[src.index("MARKET_I0 = 10000"): src.index("def sell_run")]
    exec(compile(block, "farmbench_engine", "exec"), ns)
    I0 = ns["MARKET_I0"]
    xs = list(range(0, 181)); ys = [ns["market_price"]("MELON", I0 + x) for x in xs]
    return xs, ys


def cover(rows):
    xs, ys = melon_curve()
    floor_at = next(x for x, y in zip(xs, ys) if y <= 1)
    fig = plt.figure(figsize=(10, 4.2), dpi=200, facecolor=GROUND)
    ax = fig.add_axes([0.60, 0.20, 0.36, 0.60]); style(ax)
    ax.fill_between(xs, ys, 0, color=STRAT, alpha=0.12, lw=0)
    ax.plot(xs, ys, color=STRAT, lw=2.2, solid_capstyle="round")
    ax.scatter([0, floor_at], [ys[0], 1], s=60, color=STRAT, edgecolor=GROUND, linewidth=2, zorder=3)
    ax.axhline(0, color=RULE, lw=1)
    ax.set_xlim(-6, 185); ax.set_ylim(-12, 285)
    ax.set_xticks([0, 50, 100, 150]); ax.set_yticks([0, 100, 200])
    ax.set_xticklabels(["0", "50", "100", "150"], family=MONO, fontsize=9)
    ax.set_yticklabels(["$0", "$100", "$200"], family=MONO, fontsize=9)
    ax.text(4, ys[0] + 10, f"${ys[0]}", family=MONO, fontsize=10, color=INK)
    ax.text(floor_at - 6, 22, f"$1 after {floor_at} units", family=MONO, fontsize=10, color=INK, ha="right")
    ax.text(0, -58, "melon price vs units sold into a shared market (engine function)", family=BODY, fontsize=9, color=INK2)
    fig.text(0.05, 0.70, "Can a Language Model", family=DISPLAY, fontsize=34, color=INK, weight="bold")
    fig.text(0.05, 0.56, "Run a Farm?", family=DISPLAY, fontsize=34, color=INK, weight="bold")
    fig.text(0.05, 0.40, "15 economic decisions from Kaggriculture,", family=BODY, fontsize=14, color=INK2)
    fig.text(0.05, 0.33, "21 models, graded by the game engine.", family=BODY, fontsize=14, color=INK2)
    fig.text(0.05, 0.14, "FarmBench  ·  Kaggle Benchmarks  ·  DEV × Kaggle Benchmarking Challenge", family=BODY, fontsize=10.5, color=MUTED)
    p = os.path.join(OUT, "cover.png"); fig.savefig(p, facecolor=GROUND); plt.close(fig); return p


def se_waffle():
    """16 of 19 models bought the SE quadrant; the top-10 teams bought it in 0 of 160 games."""
    bought = ["Gemini 3.7 Flash", "GPT-6 Astra", "Gemma 4 31B", "Claude Opus 5", "Gemini 3.8 Flash", "Claude Sonnet 5",
              "Gemini 2.5 Flash", "GLM-5", "GPT-5.5", "Gemini 2.5 Pro", "Grok 4.20 Reasoning", "gpt-oss-20b",
              "GPT-5.4 mini", "gpt-oss-120b", "GPT-5.4 nano", "Claude Haiku 4.5"]
    declined = ["Claude Opus 4.8", "Claude Sonnet 4.5", "Gemini 3.1 Flash-Lite"]
    fig = plt.figure(figsize=(10, 4.6), dpi=200, facecolor=GROUND)
    ax = fig.add_axes([0.04, 0.17, 0.92, 0.56]); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 2.2)
    cells = [(n, True) for n in bought] + [(n, False) for n in declined]
    for i, (n, b) in enumerate(cells):
        cx, cy = (i % 10) * 1.0 + 0.05, 1.15 if i < 10 else 0.05
        box = FancyBboxPatch((cx, cy), 0.9, 0.9, boxstyle="round,pad=0,rounding_size=0.08",
                             facecolor=STRAT if b else GROUND, edgecolor=STRAT if b else INK2, linewidth=0 if b else 1.4)
        ax.add_patch(box)
        lines = [""]
        for w in n.split(" "):
            lines[-1] = (lines[-1] + " " + w).strip() if len(lines[-1]) + len(w) < 11 else lines[-1]
            if w not in lines[-1].split(" "): lines.append(w)
        lines = [l for l in lines if l][:2] + [""]
        ax.text(cx + 0.45, cy + 0.52, lines[0], ha="center", va="center", fontsize=8.2, family=BODY,
                color="#ffffff" if b else INK, weight="bold")
        if lines[1]:
            ax.text(cx + 0.45, cy + 0.32, lines[1], ha="center", va="center", fontsize=8.2, family=BODY,
                    color="#ffffff" if b else INK, weight="bold")
    ax.text(9.5, 0.5, "", fontsize=1)
    fig.text(0.04, 0.90, "16 of 19 models bought the $4,000 quadrant", family=DISPLAY, fontsize=21, color=INK, weight="bold")
    fig.text(0.04, 0.83, "Day 12, $11,573 cash, 4 empty tiles. Filled = bought, outlined = declined. The engine prefers never buying in 11 of 12",
             family=BODY, fontsize=10.5, color=INK2)
    fig.text(0.04, 0.785, "simulated games, and the real top-10 teams bought it in 0 of 160.", family=BODY, fontsize=10.5, color=INK2)
    fig.text(0.04, 0.07, "The three that declined reasoned about the time left to recoup $4,000; the buyers reasoned about capacity.",
             family=BODY, fontsize=10.5, color=INK2)
    p = os.path.join(OUT, "se_quadrant.png"); fig.savefig(p, facecolor=GROUND); plt.close(fig); return p


if __name__ == "__main__":
    rows = load_scores()
    assert len(rows) == 19, len(rows)
    for p in (cover(rows), dumbbell(rows), se_waffle()):
        print("wrote", os.path.relpath(p, HERE))
