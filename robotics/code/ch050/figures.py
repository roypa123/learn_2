# Figures for Chapter 50 - Trigonometry part 2: the unit circle, atan2, wrapping angles.
# Run:  python figures.py      (saves PNG files in ../../images/ch050/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Arc, FancyArrowPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch050")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=2.6):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, color=colour, lw=lw, shrinkA=0, shrinkB=0, zorder=4))


def wrap(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


# Figure 1: the unit circle
fig, ax = plt.subplots(figsize=(7.5, 7.5))
ax.add_patch(Circle((0, 0), 1, fill=False, ec=BLACK, lw=2))
ax.axhline(0, color=GREY, lw=1); ax.axvline(0, color=GREY, lw=1)
t = math.radians(140)
px, py = math.cos(t), math.sin(t)
arrow(ax, (0, 0), (px, py), ORANGE, 3)
ax.plot([px, px], [0, py], color=BLUE, lw=3); ax.plot([0, px], [0, 0], color=GREEN, lw=4)
ax.plot([px], [py], "o", color=BLACK, ms=10, zorder=5)
ax.text(px - 0.1, py + 0.12, "(cos 140, sin 140)\n= (-0.766, 0.643)", ha="center", fontsize=12, bbox=dict(fc="white", ec="none", pad=1))
ax.text(px / 2, -0.12, "cos 140 = -0.766", ha="center", fontsize=12, color=GREEN)
ax.text(px - 0.04, py / 2, "sin 140\n= 0.643", ha="right", fontsize=12, color=BLUE)
ax.add_patch(Arc((0, 0), 0.5, 0.5, theta1=0, theta2=140, color=RED, lw=2.5)); ax.text(0.2, 0.25, "140", fontsize=12, color=RED)
for lab, (x, y) in [("I", (0.6, 0.6)), ("II", (-0.6, -0.55)), ("III", (-0.6, -0.75)), ("IV", (0.6, -0.6))]:
    pass
ax.text(0.25, 0.55, "I: cos +, sin +", fontsize=11, color="#555555"); ax.text(-0.75, -0.55, "III: cos -, sin -", fontsize=11, color="#555555")
ax.text(0.2, -0.55, "IV: cos +, sin -", fontsize=11, color="#555555"); ax.text(-0.55, 0.68, "II: cos -, sin +", fontsize=11, color="#555555", bbox=dict(fc="white", ec="none", pad=1))
ax.text(1.03, 0.03, "1", fontsize=12); ax.text(0.03, 1.03, "1", fontsize=12)
ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig01-unit-circle.png")

# Figure 2: sin and cos waves
a = np.linspace(-90, 720, 800)
fig, ax = plt.subplots(figsize=(12, 4.6))
ax.plot(a, np.sin(np.radians(a)), color=BLUE, lw=3, label="sin")
ax.plot(a, np.cos(np.radians(a)), color=GREEN, lw=3, ls="--", label="cos")
ax.axhline(0, color=BLACK, lw=1)
ax.axvspan(360, 720, color=L_GREY, alpha=0.5); ax.text(540, 1.4, "the same again: period 360 degrees (2 pi)", ha="center", fontsize=12)
ax.set_xticks(range(-90, 721, 90)); ax.set_xlabel("angle (degrees)"); ax.set_ylim(-1.3, 1.75); ax.grid(alpha=0.3); ax.legend(loc="upper left", ncol=2)
save(fig, "fig02-waves.png")

# Figure 3: atan versus atan2
fig, ax = plt.subplots(figsize=(7.5, 7.5))
ax.axhline(0, color=BLACK, lw=1); ax.axvline(0, color=BLACK, lw=1)
for (x, y), col in [((1, 1), BLUE), ((-1, -1), RED)]:
    arrow(ax, (0, 0), (x, y), col, 3)
ax.text(1.05, 1.05, "(1, 1)\natan2: 45", fontsize=12.5, color=BLUE)
ax.text(-1.45, -1.3, "(-1, -1)\natan2: -135", fontsize=12.5, color=RED)
ax.text(-1.45, 0.75, "atan(y/x) gives 45\nfor BOTH, because\n1/1 = (-1)/(-1) = 1", fontsize=12.5)
ax.add_patch(Arc((0, 0), 0.6, 0.6, theta1=0, theta2=45, color=BLUE, lw=2.5))
ax.add_patch(Arc((0, 0), 0.9, 0.9, theta1=-135, theta2=0, color=RED, lw=2.5))
ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.6, 1.6); ax.set_aspect("equal"); ax.grid(alpha=0.3)
save(fig, "fig03-atan2.png")

# Figure 4: go to goal path
goal = (-2.0, -1.0)
x, y, h = 0.0, 0.0, math.radians(30)
xs, ys = [x], [y]
for _ in range(200):
    dx, dy = goal[0] - x, goal[1] - y
    if math.hypot(dx, dy) < 0.05:
        break
    e = wrap(math.atan2(dy, dx) - h)
    h = wrap(h + 2.0 * e * 0.1)
    x += 0.3 * math.cos(h) * 0.1; y += 0.3 * math.sin(h) * 0.1
    xs.append(x); ys.append(y)
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(xs, ys, color=BLUE, lw=3, label="path driven")
ax.plot([0], [0], "s", color=ORANGE, mec=BLACK, ms=13, label="start, facing 30 degrees")
arrow(ax, (0, 0), (0.4 * math.cos(math.radians(30)), 0.4 * math.sin(math.radians(30))), ORANGE, 2.5)
ax.plot([goal[0]], [goal[1]], "*", color=BLACK, ms=20, label="goal (-2, -1)")
ax.plot([0, goal[0]], [0, goal[1]], color=BLACK, ls="--", lw=1.5)
ax.text(-1.35, -0.95, "goal direction: atan2(-1, -2) = -153.4 deg", fontsize=12, rotation=26)
ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)"); ax.grid(alpha=0.3); ax.legend(loc="upper left"); ax.set_aspect("equal")
ax.set_xlim(-2.5, 0.8); ax.set_ylim(-1.5, 0.8)
save(fig, "fig04-go-to-goal.png")

# Figure 5: averaging headings as arrows
r = [350, 355, 2, 8, 5, 352]
fig, ax = plt.subplots(figsize=(7, 7))
ax.add_patch(Circle((0, 0), 1, fill=False, ec=GREY, lw=1.5))
for d in r:
    t = math.radians(90 - d)
    arrow(ax, (0, 0), (math.cos(t), math.sin(t)), GREY, 1.6)
t = math.radians(90 - 358.7)
arrow(ax, (0, 0), (1.2 * math.cos(t), 1.2 * math.sin(t)), GREEN, 4); ax.text(-0.05, 1.27, "vector mean 358.7", fontsize=12.5, color=GREEN, ha="center")
t = math.radians(90 - 178.7)
arrow(ax, (0, 0), (math.cos(t), math.sin(t)), RED, 3); ax.text(0.05, -1.15, "plain average 178.7: points SOUTH!", fontsize=12.5, color=RED, ha="center")
ax.text(0, 1.45, "N", ha="center", fontsize=14, weight="bold")
ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.6); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig05-average.png")

# Figure 6: unwrapping
raw = [2.8, 3.0, -3.1, -2.9, -2.7, 3.1, 2.9]
un = [raw[0]]
for v in raw[1:]:
    un.append(un[-1] + wrap(v - un[-1]))
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(range(7), raw, "s--", color=RED, lw=2, ms=8, label="raw readings (jump at the edge)")
ax.plot(range(7), un, "o-", color=BLUE, lw=3, ms=8, label="unwrapped (smooth)")
ax.axhline(math.pi, color=GREY, ls=":", lw=1.5); ax.axhline(-math.pi, color=GREY, ls=":", lw=1.5)
ax.text(6.3, math.pi - 0.1, "pi", fontsize=12); ax.text(6.3, -math.pi - 0.1, "-pi", fontsize=12)
ax.set_xlabel("reading number"); ax.set_ylabel("angle (rad)"); ax.grid(alpha=0.3); ax.legend(loc="center left")
ax.set_ylim(-3.6, 4.2); ax.set_xlim(-0.3, 6.7)
save(fig, "fig06-unwrap.png")

# Figure 7: three motor phases 120 degrees apart
a = np.linspace(0, 720, 800)
fig, ax = plt.subplots(figsize=(11, 4.4))
for shift, col, st, lab in [(0, BLUE, "-", "phase A"), (120, GREEN, "--", "phase B: 120 later"), (240, ORANGE, ":", "phase C: 240 later")]:
    ax.plot(a, np.sin(np.radians(a - shift)), color=col, ls=st, lw=2.8, label=lab)
ax.axhline(0, color=BLACK, lw=1)
ax.set_xticks(range(0, 721, 120)); ax.set_xlabel("electrical angle (degrees)"); ax.set_ylabel("share of full current"); ax.grid(alpha=0.3)
ax.legend(loc="upper center", ncol=3, fontsize=11); ax.set_ylim(-1.2, 1.5)
save(fig, "fig07-three-phases.png")
print("figures saved in", os.path.abspath(OUT))
