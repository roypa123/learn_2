# Figures for Chapter 56 - Position, distance and displacement.
# Run:  python figures.py      (saves PNG files in ../../images/ch056/)
import math
import os
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch056")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def robot(ax, x, y, w=0.6, h=0.35, label=None):
    ax.add_patch(plt.Rectangle((x - w / 2, y - h / 2), w, h, color=ORANGE, ec=BLACK, zorder=5))
    for dx in (-w / 3, w / 3):
        ax.add_patch(plt.Circle((x + dx, y - h / 2), 0.09, color=BLACK, zorder=6))
    if label:
        ax.text(x, y + h / 2 + 0.12, label, ha="center", fontsize=12)


# Figure 1: position on a number line along a corridor
fig, ax = plt.subplots(figsize=(11, 3.2))
ax.add_patch(plt.Rectangle((-3.5, -0.55), 10.0, 1.3, color=L_GREY, zorder=0))
ax.axhline(-0.55, color=BLACK, lw=1)
for x in range(-3, 7):
    ax.plot([x, x], [-0.62, -0.48], color=BLACK, lw=1.5)
    ax.text(x, -0.9, f"{x}", ha="center", fontsize=12)
ax.annotate("", xy=(6.6, -0.55), xytext=(-3.5, -0.55), arrowprops=dict(arrowstyle="-|>", lw=1.5))
ax.plot([0], [-0.55], "o", color=BLACK, ms=10, zorder=7)
ax.text(0, -1.35, "origin (charging dock)", ha="center", fontsize=12)
robot(ax, 3.0, -0.3, label="Rover at x = +3 m")
ax.add_patch(plt.Rectangle((-2.2, -0.55), 0.4, 1.0, color=GREY, zorder=4))
ax.text(-2.0, 0.6, "door at x = -2 m", ha="center", fontsize=12)
ax.text(6.6, -0.9, "x (m)", ha="left", fontsize=12)
ax.text(4.6, 0.5, "positive direction  -->", fontsize=12, color=BLUE)
ax.set_xlim(-3.7, 7.2); ax.set_ylim(-1.6, 1.0); ax.axis("off")
save(fig, "fig01-number-line.png")

# Figure 2: the corridor trip, distance against displacement
pos = [0.0, 2.0, 5.0, 5.0, 3.0, 1.5, 4.0]
fig, ax = plt.subplots(figsize=(11, 5))
row = 0
for i in range(1, len(pos)):
    a, b = pos[i - 1], pos[i]
    y = 6 - row
    if a == b:
        ax.plot([a], [y], "o", color=BLUE, ms=8)
        ax.text(a + 0.15, y + 0.12, f"move {i}: waits (0 m)", fontsize=11.5)
    else:
        ax.annotate("", xy=(b, y), xytext=(a, y), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.5))
        ax.text(max(a, b) + 0.15, y - 0.1, f"move {i}: {b - a:+.1f} m", fontsize=11.5)
    row += 1
ax.annotate("", xy=(4.0, -0.4), xytext=(0.0, -0.4), arrowprops=dict(arrowstyle="-|>", color=RED, lw=3.5))
ax.text(0.0, -0.95, "displacement = 4.0 - 0.0 = +4.0 m (one red arrow from start to end)", fontsize=12, color=RED)
ax.text(0.0, 7.55, "distance = 2 + 3 + 0 + 2 + 1.5 + 2.5 = 11.0 m (all blue arrows, signs ignored)", fontsize=12, color=BLUE)
for x in range(0, 7):
    ax.axvline(x, color=GREY, lw=0.6, alpha=0.6, zorder=0)
ax.set_xlim(-0.3, 8.0); ax.set_ylim(-1.3, 8.0)
ax.set_yticks([]); ax.set_xlabel("position x along the corridor (m)")
for s in ["left", "right", "top"]:
    ax.spines[s].set_visible(False)
save(fig, "fig02-distance-vs-displacement.png")

# Figure 3: a 2D path through waypoints and its displacement arrow
wp = [(0, 0), (4, 0), (4, 3), (1, 3), (1, 5)]
fig, ax = plt.subplots(figsize=(7.5, 7))
xs, ys = zip(*wp)
ax.plot(xs, ys, "-", color=BLUE, lw=3, label="path driven: 4 + 3 + 3 + 2 = 12.0 m")
ax.plot(xs, ys, "o", color=BLUE, ms=9)
for n, (x, y) in enumerate(wp):
    ax.text(x + 0.12, y + 0.12, f"W{n} ({x}, {y})", fontsize=11.5)
ax.annotate("", xy=(1, 5), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=3.5))
ax.plot([], [], color=RED, lw=3.5, label="displacement (+1, +5): 5.10 m at 78.7 deg")
ax.plot([0, 1], [0, 0], color=GREY, ls=":", lw=2); ax.plot([1, 1], [0, 5], color=GREY, ls=":", lw=2)
ax.text(0.35, -0.38, "dx = 1", fontsize=11.5, color=GREY)
ax.text(1.08, 1.4, "dy = 5", fontsize=11.5, color=GREY)
ax.set_aspect("equal"); ax.set_xlim(-0.8, 5.6); ax.set_ylim(-0.8, 6.8)
ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)"); ax.grid(alpha=0.3); ax.legend(loc="upper right", fontsize=11)
save(fig, "fig03-path-2d.png")

# Figure 4: position-time graph and odometer for the warehouse robot
M_PER_TICK = math.pi * 0.20 / 1024
ticks = [1630, 3260, 3260, 1630, 0, 0, -1630, -3260, -1630, 0, 1630, 1630]
t, p, o = [0], [0.0], [0.0]
for k, n in enumerate(ticks, start=1):
    t.append(k); p.append(p[-1] + n * M_PER_TICK); o.append(o[-1] + abs(n * M_PER_TICK))
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(t, o, "s--", color=GREY, lw=2, ms=6, label="odometer: distance travelled (never goes down)")
ax.plot(t, p, "o-", color=BLUE, lw=3, ms=7, label="position x along the aisle")
ax.axvspan(4, 6, color=L_GREEN, alpha=0.6, zorder=0)
ax.text(5, 0.6, "flat:\nstopped", ha="center", fontsize=11.5)
ax.axvspan(6, 9, color=L_ORANGE, alpha=0.6, zorder=0)
ax.text(7.5, 0.6, "going down:\ndriving backwards", ha="center", fontsize=11.5)
ax.annotate("", xy=(12, 4.0), xytext=(12, 0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=3))
ax.text(11.85, 1.6, "displacement\n+4.0 m", ha="right", fontsize=11.5, color=RED)
ax.set_xlabel("time t (s)"); ax.set_ylabel("metres"); ax.set_xticks(range(0, 13))
ax.grid(alpha=0.3); ax.legend(loc="upper left", fontsize=11)
save(fig, "fig04-position-time.png")

# Figure 5: the drone's legs and the way home
legs = [(120, 0), (0, 90), (-150, 30), (-40, -160), (80, -10)]
e, n = [0], [0]
for de, dn in legs:
    e.append(e[-1] + de); n.append(n[-1] + dn)
fig, ax = plt.subplots(figsize=(8, 7))
for k in range(len(legs)):
    ax.annotate("", xy=(e[k + 1], n[k + 1]), xytext=(e[k], n[k]), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.5))
    mx, my = (e[k] + e[k + 1]) / 2, (n[k] + n[k + 1]) / 2
    ax.text(mx + 4, my + 4, f"leg {k + 1}", fontsize=11.5, color=BLUE)
ax.annotate("", xy=(0, 0), xytext=(e[-1], n[-1]), arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=3.5, ls="--"))
ax.text(14, -24, "way home:\n51.0 m on\nbearing 348.7 deg", fontsize=11.5, color=GREEN)
ax.plot([0], [0], "s", color=BLACK, ms=12)
ax.text(-8, 8, "home", ha="right", fontsize=12)
ax.plot([e[-1]], [n[-1]], "o", color=ORANGE, mec=BLACK, ms=14, zorder=6)
ax.text(e[-1] + 10, n[-1] - 18, "drone now (+10, -50)", fontsize=11.5)
ax.annotate("N", xy=(150, 150), xytext=(150, 115), ha="center", fontsize=13, arrowprops=dict(arrowstyle="-|>", lw=2))
ax.set_aspect("equal"); ax.set_xlim(-100, 175); ax.set_ylim(-85, 160)
ax.set_xlabel("east (m)"); ax.set_ylabel("north (m)"); ax.grid(alpha=0.3)
ax.set_title("flown 608.5 m, but only 51.0 m from home", fontsize=13)
save(fig, "fig05-drone-home.png")

# Figure 6: random walk - distance grows steadily, displacement does not
random.seed(7)
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
for run, col in zip(range(3), [BLUE, GREEN, RED]):
    x = y = 0.0
    xs, ys, d, s = [0.0], [0.0], [0.0], [0.0]
    for step in range(400):
        a = random.uniform(0, 2 * math.pi)
        x += 0.1 * math.cos(a); y += 0.1 * math.sin(a)
        xs.append(x); ys.append(y); d.append(math.hypot(x, y)); s.append(0.1 * (step + 1))
    axes[0].plot(xs, ys, color=col, lw=1.2)
    axes[0].plot([xs[-1]], [ys[-1]], "o", color=col, ms=8)
    axes[1].plot(s, d, color=col, lw=2, label=f"robot {run + 1}: displacement size")
axes[1].plot(s, s, color=GREY, ls="--", lw=2, label="distance travelled")
axes[0].plot([0], [0], "s", color=BLACK, ms=9)
axes[0].set_aspect("equal"); axes[0].grid(alpha=0.3); axes[0].set_xlabel("x (m)"); axes[0].set_ylabel("y (m)")
axes[0].set_title("three random walks, 400 steps of 0.1 m", fontsize=12.5)
axes[1].set_xlabel("distance travelled (m)"); axes[1].set_ylabel("metres"); axes[1].grid(alpha=0.3)
axes[1].legend(loc="upper left", fontsize=10.5); axes[1].set_title("distance against displacement", fontsize=12.5)
save(fig, "fig06-random-walk.png")
print("saved 6 figures")
