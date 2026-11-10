# Figures for Chapter 36 — Project: GridBot.
# Run:  python figures.py      (runs the project and saves PNG files in ../../images/ch036/)
import os
import shutil
import subprocess
import sys
import tempfile
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch036")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"
MONO = "DejaVu Sans Mono"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=2.2):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=15, color=colour, lw=lw, zorder=3))


def rbox(ax, x, y, w, h, text, face, size=11.5, family=None, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, family=family, weight=weight)


# run the real program in a temporary folder, so that no output files land in code/
with tempfile.TemporaryDirectory() as d:
    for name in ("gridbot.py", "run_gridbot.py"):
        shutil.copy(os.path.join(HERE, name), d)
    shutil.copytree(os.path.join(HERE, "worlds"), os.path.join(d, "worlds"))
    subprocess.run([sys.executable, "run_gridbot.py"], cwd=d, check=True, env=dict(os.environ, MPLBACKEND="Agg"), stdout=subprocess.DEVNULL)
    shutil.copy(os.path.join(d, "gridbot_result.png"), os.path.join(OUT, "gridbot_result.png"))

# ---------- Figure 1: the parts of the project ----------
fig, ax = plt.subplots(figsize=(13.5, 6.4))
rbox(ax, 0.3, 4.6, 3.3, 1.2, "worlds/maze.txt\nthe map, as text\n(Ch 27 files)", L_GREY)
rbox(ax, 5.0, 4.0, 4.0, 2.2, "gridbot.py\nWorld and GridBot classes (Ch 28)\nsensors, moves, battery\nfollow_right_wall, shortest_path\ndraw", L_GREEN)
rbox(ax, 10.4, 4.6, 2.9, 1.2, "test_gridbot.py\n10 checks\n(Ch 25)", L_ORANGE)
rbox(ax, 2.2, 0.9, 4.0, 1.8, "run_gridbot.py\nruns everything\nCSV log (Ch 27)\nNumPy + picture (Ch 33, 34)", L_BLUE)
rbox(ax, 7.8, 0.9, 4.0, 1.8, "noisy_gridbot.py\ninherits from GridBot (Ch 29)\nsensors that lie (Ch 31)\nMonte Carlo", L_BLUE)
arrow(ax, (3.65, 5.2), (4.95, 5.2)); ax.text(4.3, 5.4, "reads", ha="center", fontsize=11)
arrow(ax, (10.35, 5.2), (9.05, 5.2)); ax.text(9.7, 5.4, "imports", ha="center", fontsize=11)
arrow(ax, (4.2, 2.75), (6.0, 3.95)); ax.text(4.6, 3.4, "imports", fontsize=11, ha="right")
arrow(ax, (9.8, 2.75), (8.0, 3.95)); ax.text(9.4, 3.4, "imports", fontsize=11, ha="left")
ax.set_xlim(0, 13.6); ax.set_ylim(0.6, 6.5); ax.axis("off")
save(fig, "fig01-project-parts.png")

# ---------- Figure 2: the right-hand rule ----------
fig, axes = plt.subplots(1, 3, figsize=(14, 5.0))


def scene(ax, walls, title, note, arrow_to, turn=None):
    for x in range(3):
        for y in range(3):
            ax.add_patch(Rectangle((x, y), 1, 1, fc=(GREY if (x, y) in walls else "white"), ec=L_GREY))
    ax.add_patch(Polygon([(1.5, 1.8), (1.25, 1.25), (1.75, 1.25)], closed=True, fc=ORANGE, ec=BLACK, zorder=4))
    if arrow_to:
        arrow(ax, arrow_to[0], arrow_to[1], BLUE, 3.5)
    ax.set_title(title, fontsize=13.5, weight="bold")
    ax.text(1.5, -0.45, note, ha="center", va="center", fontsize=12)
    ax.set_xlim(-0.1, 3.1); ax.set_ylim(-0.8, 3.1); ax.set_aspect("equal"); ax.axis("off")


scene(axes[0], {(0, 2), (1, 2), (2, 2), (0, 1), (0, 0)}, "1. No wall on the right", "turn right, then step forward", ((1.7, 1.5), (2.75, 1.5)))
scene(axes[1], {(2, 2), (2, 1), (2, 0), (0, 1), (0, 0)}, "2. Wall on the right, front clear", "step forward", ((1.5, 1.85), (1.5, 2.8)))
scene(axes[2], {(0, 2), (1, 2), (2, 2), (2, 1), (2, 0)}, "3. Wall right and in front", "turn left", ((1.3, 1.5), (0.25, 1.5)))
save(fig, "fig02-right-hand-rule.png")

# ---------- Figure 3: noise against success ----------
err = [0, 1, 5, 10, 20]
win = [100, 100, 84, 55, 23]
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(err, win, "o-", color=BLUE, lw=2.5, ms=9)
for e, w in zip(err, win):
    ax.annotate(f"{w}%", xy=(e, w), xytext=(e - 0.25, w - 9) if e == 0 else (e + 0.4, w + 3), fontsize=12)
ax.set_xlabel("chance that one sensor reading is wrong (%)"); ax.set_ylabel("runs reaching the goal (%)")
ax.set_xlim(-1, 22); ax.set_ylim(0, 112); ax.grid(alpha=0.3)
save(fig, "fig03-sensor-errors.png")
print("figures saved in", os.path.abspath(OUT))
