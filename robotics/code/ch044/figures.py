# Figures for Chapter 44 - Functions and graphs.
# Run:  python figures.py      (saves PNG files in ../../images/ch044/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch044")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=2.4):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=18, color=colour, lw=lw, shrinkA=0, shrinkB=0))


def box(ax, x, y, w, h, text, face, size=14):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.15", fc=face, ec=BLACK, lw=1.4))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size)


# Figure 1: function machines in a chain
fig, ax = plt.subplots(figsize=(13, 3.6))
ax.text(0.5, 1.5, "x = 3", fontsize=17, ha="center", va="center", weight="bold")
arrow(ax, (1.1, 1.5), (2.0, 1.5))
box(ax, 2.0, 0.8, 2.6, 1.4, "f\ndouble, add 1", L_BLUE)
arrow(ax, (4.6, 1.5), (5.6, 1.5)); ax.text(5.1, 1.75, "7", fontsize=16, ha="center", weight="bold")
box(ax, 5.6, 0.8, 2.6, 1.4, "g\nsquare it", L_GREEN)
arrow(ax, (8.2, 1.5), (9.2, 1.5))
ax.text(9.9, 1.5, "49", fontsize=17, ha="center", va="center", weight="bold")
ax.text(5.1, 0.25, "g(f(3)) = g(7) = 49      one input in, exactly one output out of each machine", fontsize=12.5, ha="center")
ax.set_xlim(0, 10.6); ax.set_ylim(0, 2.6); ax.axis("off")
save(fig, "fig01-machines.png")

# Figure 2: gallery of shapes
fig, axes = plt.subplots(2, 3, figsize=(13, 7.6))
x = np.linspace(-3, 3, 400)
panels = [("y = 2x + 1  (straight line)", x, 2 * x + 1),
          ("y = x squared  (parabola, Ch 45)", x, x ** 2),
          ("y = 1/x  (not defined at 0)", None, None),
          ("y = square root of x  (x >= 0 only)", np.linspace(0, 3, 200), np.sqrt(np.linspace(0, 3, 200))),
          ("y = |x|  (absolute value)", x, np.abs(x)),
          ("step: 0 below 1, then 1", None, None)]
for ax, (title, xs, ys) in zip(axes.flat, panels):
    ax.axhline(0, color=BLACK, lw=1); ax.axvline(0, color=BLACK, lw=1); ax.grid(alpha=0.3)
    ax.set_title(title, fontsize=12.5); ax.set_xlim(-3, 3); ax.set_ylim(-3, 4)
    if xs is not None:
        ax.plot(xs, ys, color=BLUE, lw=3)
xl = np.linspace(-3, -0.25, 100); xr = np.linspace(0.25, 3, 100)
axes[0, 2].plot(xl, 1 / xl, color=BLUE, lw=3); axes[0, 2].plot(xr, 1 / xr, color=BLUE, lw=3)
axes[1, 2].plot([-3, 1], [0, 0], color=BLUE, lw=3); axes[1, 2].plot([1, 3], [1, 1], color=BLUE, lw=3)
axes[1, 2].plot([1], [0], "o", mfc="white", mec=BLUE, ms=9, mew=2); axes[1, 2].plot([1], [1], "o", color=BLUE, ms=9)
save(fig, "fig02-shapes.png")

# Figure 3: deadband and saturate
s = np.arange(-130, 131)
dead = np.where(np.abs(s) < 5, 0, s)
both = np.clip(dead, -80, 80)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(s, s, color=BLACK, ls="--", lw=1.8, label="no change: output = stick")
ax.plot(s, both, color=GREEN, lw=3, label="speed_command = saturate(deadband(stick))")
ax.axvspan(-5, 5, color=L_ORANGE); ax.text(0, -110, "deadband\n-5 to 5", ha="center", fontsize=11.5)
ax.axhline(80, color=RED, ls=":", lw=2); ax.axhline(-80, color=RED, ls=":", lw=2)
ax.text(-125, 88, "limit +80", color=RED, fontsize=11.5); ax.text(85, -95, "limit -80", color=RED, fontsize=11.5)
ax.set_xlabel("joystick input"); ax.set_ylabel("speed command"); ax.grid(alpha=0.3); ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.8), fontsize=11)
ax.set_xlim(-130, 130); ax.set_ylim(-135, 135)
save(fig, "fig03-piecewise.png")

# Figure 4: IR sensor table
T = [(10, 2.30), (15, 1.65), (20, 1.30), (30, 0.92), (40, 0.74), (50, 0.60), (60, 0.50), (80, 0.40)]
fig, ax = plt.subplots(figsize=(10, 5))
dd = np.linspace(10, 80, 300)
ax.plot([t[0] for t in T], [t[1] for t in T], "o-", color=BLUE, lw=2.2, ms=8, label="table points joined by straight pieces")
ax.plot([27.9], [1.00], "s", color=ORANGE, mec=BLACK, ms=11, zorder=5)
ax.plot([0, 27.9, 27.9], [1.0, 1.0, 0], color=ORANGE, ls="--", lw=2)
ax.text(29, 1.05, "1.00 V means about 27.9 cm", fontsize=12.5)
ax.set_xlabel("distance (cm)"); ax.set_ylabel("sensor output (V)"); ax.grid(alpha=0.3); ax.legend(fontsize=11)
ax.set_xlim(0, 85); ax.set_ylim(0, 2.6)
save(fig, "fig04-ir-table.png")

# Figure 5: bisection
f = lambda v: v * 0.3 + v ** 2 / 3
fig, ax = plt.subplots(figsize=(10, 5.2))
v = np.linspace(0, 5, 300)
ax.plot(v, f(v), color=BLUE, lw=3, label="stopping distance s(v)")
ax.axhline(2.0, color=BLACK, ls="--", lw=2, label="free space: 2 m")
lo, hi = 0.0, 5.0
for i in range(5):
    y = -0.4 - i * 0.45
    ax.plot([lo, hi], [y, y], color=GREEN, lw=5, solid_capstyle="butt")
    ax.text(5.1, y, f"step {i}", va="center", fontsize=11)
    mid = (lo + hi) / 2
    if f(mid) < 2:
        lo = mid
    else:
        hi = mid
ax.plot([2.0405], [2.0], "o", color=ORANGE, mec=BLACK, ms=12, zorder=5)
ax.annotate("answer: 2.0405 m/s", (2.0405, 2.0), xytext=(2.6, 3.4), fontsize=12.5, arrowprops=dict(arrowstyle="-|>"))
ax.set_xlabel("speed (m/s)"); ax.set_ylabel("distance (m)"); ax.grid(alpha=0.3); ax.legend(loc="upper left")
ax.set_xlim(0, 5.8); ax.set_ylim(-2.5, 10)
save(fig, "fig05-bisection.png")

# Figure 6: expo curves
x = np.linspace(-1, 1, 200)
fig, ax = plt.subplots(figsize=(8, 6))
for k, col, st in [(0, BLACK, "--"), (0.4, BLUE, "-"), (0.8, GREEN, ":")]:
    ax.plot(x, (1 - k) * x + k * x ** 3, color=col, ls=st, lw=3, label=f"k = {k}")
ax.axhline(0, color=BLACK, lw=1); ax.axvline(0, color=BLACK, lw=1)
ax.set_xlabel("stick position (-1 to 1)"); ax.set_ylabel("command sent to the drone"); ax.grid(alpha=0.3); ax.legend(title="expo")
ax.set_xticks([-1, -0.5, 0, 0.5, 1]); ax.set_aspect("equal")
save(fig, "fig06-expo.png")
print("figures saved in", os.path.abspath(OUT))
