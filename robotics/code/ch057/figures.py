# Figures for Chapter 57 - Speed and velocity.
# Run:  python figures.py      (saves PNG files in ../../images/ch057/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch057")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Figure 1: three robots on one position-time graph
t = np.array([0, 10])
fig, ax = plt.subplots(figsize=(10, 5.2))
ax.plot(t, 0.5 * t, color=BLUE, lw=3, label="robot A: +0.5 m/s")
ax.plot(t, 0.2 * t + 1, color=GREEN, lw=3, label="robot B: +0.2 m/s (starts at 1 m)")
ax.plot(t, 6 - 0.4 * t, color=RED, lw=3, label="robot C: -0.4 m/s (drives back)")
ax.plot(t, [3, 3], color=GREY, lw=3, label="robot D: 0 m/s (parked at 3 m)")
ax.plot([2, 6], [1, 1], color=BLACK, lw=1.2, ls=":"); ax.plot([6, 6], [1, 3], color=BLACK, lw=1.2, ls=":")
ax.text(4, 0.55, "run = 4 s", ha="center", fontsize=11.5)
ax.text(6.15, 1.9, "rise = 2 m", fontsize=11.5)
ax.text(5.2, 0.25, "slope of A = rise / run = 2 m / 4 s = 0.5 m/s", fontsize=11.5, color=BLUE)
ax.set_xlabel("time t (s)"); ax.set_ylabel("position x (m)"); ax.set_xlim(0, 10); ax.set_ylim(0, 6.5)
ax.grid(alpha=0.3); ax.legend(loc="upper right", fontsize=10.5)
save(fig, "fig01-slopes.png")

# Figure 2: average velocity (chord) against instant velocity (tangent)
tt = np.linspace(0, 6, 300)
x = 0.15 * tt ** 2
fig, ax = plt.subplots(figsize=(10, 5.2))
ax.plot(tt, x, color=BLUE, lw=3, label="position of a robot that is speeding up")
ax.plot([1, 5], [0.15, 3.75], "o--", color=GREEN, lw=2.5, ms=8, label="average velocity from 1 s to 5 s: 0.90 m/s")
v3 = 0.3 * 3
ax.plot([1.2, 4.8], [1.35 + v3 * (1.2 - 3), 1.35 + v3 * (4.8 - 3)], color=RED, lw=2.5, label="tangent at 3 s: instant velocity 0.90 m/s")
ax.plot([4], [2.4], "o", color=RED, ms=0)
ax.plot([3], [1.35], "o", color=RED, ms=9)
v5 = 0.3 * 5
ax.plot([4.0, 6.0], [3.75 - v5, 3.75 + v5], color=ORANGE, lw=2.5, label="tangent at 5 s: instant velocity 1.50 m/s")
ax.plot([5], [3.75], "o", color=ORANGE, ms=9)
ax.set_xlabel("time t (s)"); ax.set_ylabel("position x (m)"); ax.set_xlim(0, 6.2); ax.set_ylim(-0.3, 5.6)
ax.grid(alpha=0.3); ax.legend(loc="upper left", fontsize=10.5)
save(fig, "fig02-tangent.png")

# Figure 3: velocity-time graph, area is displacement
tv = [0, 2, 2, 5, 5, 7, 7, 9, 9, 10, 10, 12]
vv = [1, 1, 1, 1, 0, 0, -1, -1, -1.5, -1.5, 1.25, 1.25]
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(tv, vv, color=BLUE, lw=3)
segs = [(0, 5, 1.0), (7, 9, -1.0), (9, 10, -1.5), (10, 12, 1.25)]
for a, b, v in segs:
    ax.fill_between([a, b], [0, 0], [v, v], color=L_GREEN if v > 0 else L_ORANGE, alpha=0.9)
    ax.text((a + b) / 2, v / 2, f"{v * (b - a):+.1f} m", ha="center", va="center", fontsize=10.5)
ax.axhline(0, color=BLACK, lw=1)
ax.text(0.2, -1.95, "green area above the axis: forwards.   orange area below: backwards.", fontsize=11.5)
ax.text(0.2, 1.62, "sum of areas = 5 + 0 - 2 - 1.5 + 2.5 = +4.0 m (displacement)", fontsize=12, color=RED)
ax.set_xlabel("time t (s)"); ax.set_ylabel("velocity v (m/s)"); ax.set_xticks(range(0, 13))
ax.set_ylim(-2.2, 1.9); ax.grid(alpha=0.3)
save(fig, "fig03-area.png")

# Figure 4: speed estimates from an encoder, one-loop against ten-loop
TICK = math.pi * 0.065 / 360
DT = 0.01


def counts_for(v, n=100):
    out, last = [], 0
    for k in range(1, n + 1):
        tot = math.floor(v * k * DT / TICK)
        out.append(tot - last); last = tot
    return out


fig, axes = plt.subplots(1, 2, figsize=(13, 5))
for ax, v in zip(axes, [0.5, 0.05]):
    c = counts_for(v)
    tl = np.arange(1, 101) * DT
    one = np.array(c) * TICK / DT
    ten = [sum(c[i - 10:i]) * TICK / (10 * DT) for i in range(10, 101)]
    ax.plot(tl, one, ".-", color=GREY, lw=1, ms=6, label="one-loop estimate")
    ax.plot(tl[9:], ten, color=BLUE, lw=3, label="ten-loop estimate")
    ax.axhline(v, color=BLACK, ls="--", lw=2, label=f"true speed {v} m/s")
    ax.set_xlabel("time (s)"); ax.set_ylabel("speed (m/s)"); ax.grid(alpha=0.3)
    ax.set_title(f"wheel at {v} m/s", fontsize=13)
axes[0].set_ylim(0.40, 0.56); axes[0].legend(loc="lower right", fontsize=10.5)
axes[1].set_ylim(-0.005, 0.075); axes[1].legend(loc="center right", fontsize=10.5)
save(fig, "fig04-encoder-speed.png")

# Figure 5: route parts, length and time
names = ["pavement", "crossing", "market\nstreet", "pavement", "lobby"]
lens = [400, 15, 120, 250, 30]
spd = [1.6, 1.0, 0.6, 1.6, 0.4]
times = [l / s for l, s in zip(lens, spd)]
fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
cols = [BLUE, GREY, RED, BLUE, ORANGE]
axes[0].bar(range(5), lens, color=cols, edgecolor=BLACK)
axes[1].bar(range(5), times, color=cols, edgecolor=BLACK)
for ax, vals, unit in [(axes[0], lens, "m"), (axes[1], times, "s")]:
    ax.set_xticks(range(5)); ax.set_xticklabels(names, fontsize=11)
    for i, v in enumerate(vals):
        ax.text(i, v + max(vals) * 0.02, f"{v:.0f} {unit}", ha="center", fontsize=11)
    ax.grid(axis="y", alpha=0.3)
axes[0].set_title("length of each part (815 m in total)", fontsize=12.5); axes[0].set_ylabel("metres")
axes[1].set_title("time for each part (696 s in total)", fontsize=12.5); axes[1].set_ylabel("seconds")
axes[0].set_ylim(0, 450); axes[1].set_ylim(0, 290)
save(fig, "fig05-route.png")

# Figure 6: adding velocities - a drone in a wind
fig, ax = plt.subplots(figsize=(7, 7))
ax.annotate("", xy=(0, 10), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=3.5))
ax.annotate("", xy=(3, 10), xytext=(0, 10), arrowprops=dict(arrowstyle="-|>", color=GREY, lw=3.5))
ax.annotate("", xy=(3, 10), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=RED, lw=3.5))
ax.text(-0.35, 5, "drone through the air\n10 m/s north", ha="right", va="center", fontsize=12, color=BLUE)
ax.text(1.5, 10.35, "wind 3 m/s east", ha="center", fontsize=12, color=GREY)
ax.text(1.85, 4.6, "over the ground\n10.44 m/s\nbearing 16.7 deg", fontsize=12, color=RED)
ax.plot([0], [0], "o", color=ORANGE, mec=BLACK, ms=14)
ax.set_aspect("equal"); ax.set_xlim(-5.5, 6); ax.set_ylim(-1, 11.5)
ax.set_xlabel("east (m/s)"); ax.set_ylabel("north (m/s)"); ax.grid(alpha=0.3)
save(fig, "fig06-wind.png")
print("saved 6 figures")
