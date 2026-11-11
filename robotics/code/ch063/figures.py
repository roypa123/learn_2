# Figures for Chapter 63 - Friction and grip (traction).
# Run:  python figures.py      (saves PNG files in ../../images/ch063/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch063")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"
G = 9.81


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, x0, y0, x1, y1, col, lw=3):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", color=col, lw=lw, mutation_scale=20))


# Figure 1: friction force against the push
push = np.linspace(0, 14, 300)
lim, slide = 9.81, 7.85
fr = np.where(push <= lim, push, slide)
fig, ax = plt.subplots(figsize=(10, 5.2))
ax.plot(push, fr, color=RED, lw=3, label="friction force")
ax.plot(push, push, color=GREY, ls=":", lw=1.5, label="push (if friction matched it exactly)")
ax.axhline(lim, color=BLACK, ls="--", lw=1.5); ax.text(0.3, lim + 0.25, "static limit mu_s N = 9.81 N", fontsize=11.5)
ax.axhline(slide, color=BLUE, ls="--", lw=1.5); ax.text(10.3, slide - 1.6, "sliding friction\nmu_k N = 7.85 N", fontsize=11.5, color=BLUE)
ax.axvspan(0, lim, color=L_GREEN, alpha=0.5); ax.text(4.5, 1.0, "stuck: friction matches the push", ha="center", fontsize=11.5)
ax.axvspan(lim, 14, color=L_ORANGE, alpha=0.5); ax.text(11.9, 1.0, "sliding", ha="center", fontsize=11.5)
ax.set_xlabel("push on the block (N)"); ax.set_ylabel("friction force (N)"); ax.set_xlim(0, 14); ax.set_ylim(0, 12)
ax.grid(alpha=0.3); ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.8), fontsize=10.5)
ax.set_title("a 2 kg block: mu_s = 0.5, mu_k = 0.4", fontsize=12.5)
save(fig, "fig01-friction-vs-push.png")

# Figure 2: the tilt test
th = math.radians(26.6)
fig, ax = plt.subplots(figsize=(9, 5.5))
L = 6
ax.fill([0, L, L], [0, 0, L * math.tan(th)], color=L_GREY)
ax.plot([0, L], [0, L * math.tan(th)], color=BLACK, lw=2)
c, s = math.cos(th), math.sin(th)
bx, by = 3.6, 3.6 * math.tan(th)
pts = [(-0.5, 0), (0.5, 0), (0.5, 0.6), (-0.5, 0.6)]
ax.add_patch(plt.Polygon([(bx + c * x - s * y, by + s * x + c * y) for x, y in pts], color=ORANGE, ec=BLACK))
mx, my = bx - 0.3 * s, by + 0.3 * c
arrow(ax, mx, my, mx - 1.6 * s * c, my - 1.6 * s * s, RED)
ax.text(mx - 1.6 * s * c - 0.1, my - 1.6 * s * s + 0.15, "m g sin(angle)\n(down the ramp)", ha="right", fontsize=11.5, color=RED)
arrow(ax, bx + 0.5 * c, by + 0.5 * s, bx + 0.5 * c + 1.4 * c, by + 0.5 * s + 1.4 * s, GREEN)
ax.text(bx + 2.0 * c, by + 2.0 * s + 0.3, "friction, up to\nmu x m g cos(angle)", fontsize=11.5, color=GREEN)
t = np.linspace(0, th, 30)
ax.plot(1.4 * np.cos(t), 1.4 * np.sin(t), color=BLACK, lw=1.5)
ax.text(1.55, 0.25, "26.6 deg", fontsize=11.5)
ax.text(0.2, 3.4, "raise the board slowly.\nthe block starts to slide when\ntan(angle) = mu.   tan(26.6) = 0.50", fontsize=12)
ax.set_xlim(-0.2, 6.4); ax.set_ylim(-0.3, 4.3); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig02-tilt-test.png")

# Figure 3: wheel limit and tote limit on different floors
floors = ["dry concrete\nmu 0.8", "dusty floor\nmu 0.5", "wet tiles\nmu 0.3", "icy floor\nmu 0.1"]
mus = [0.8, 0.5, 0.3, 0.1]
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(range(4), [m * G for m in mus], color=[GREEN, ORANGE, BLUE, GREY], edgecolor=BLACK, label="wheels slip above this (mu x g)")
ax.axhline(0.2 * G, color=RED, ls="--", lw=2.5, label="tote slides above 1.96 m/s^2 (mu 0.2)")
for i, m in enumerate(mus):
    ax.text(i, m * G + 0.15, f"{m * G:.2f}", ha="center", fontsize=11.5)
ax.set_xticks(range(4)); ax.set_xticklabels(floors, fontsize=11)
ax.set_ylabel("largest acceleration or braking (m/s^2)"); ax.set_ylim(0, 9); ax.grid(axis="y", alpha=0.3)
ax.legend(loc="upper right", fontsize=11)
save(fig, "fig03-grip-limits.png")

# Figure 4: a two-finger gripper
fig, ax = plt.subplots(figsize=(8, 6.5))
ax.add_patch(plt.Rectangle((-0.6, -1.0), 1.2, 2.0, color=GREY, ec=BLACK))
ax.text(0, 0, "part\nmass m", ha="center", va="center", fontsize=12)
ax.add_patch(plt.Rectangle((-1.5, -0.6), 0.9, 1.2, color=ORANGE, ec=BLACK))
ax.add_patch(plt.Rectangle((0.6, -0.6), 0.9, 1.2, color=ORANGE, ec=BLACK))
arrow(ax, -2.6, 0, -1.55, 0, BLUE); ax.text(-2.6, 0.2, "squeeze F", fontsize=11.5, color=BLUE)
arrow(ax, 2.6, 0, 1.55, 0, BLUE); ax.text(1.8, 0.2, "squeeze F", fontsize=11.5, color=BLUE)
arrow(ax, -0.7, -0.4, -0.7, 0.9, GREEN); ax.text(-1.2, 1.15, "friction\nup to mu F", ha="center", fontsize=11.5, color=GREEN)
arrow(ax, 0.7, -0.4, 0.7, 0.9, GREEN); ax.text(1.2, 1.15, "friction\nup to mu F", ha="center", fontsize=11.5, color=GREEN)
arrow(ax, 0, -1.0, 0, -2.3, RED); ax.text(0.1, -2.2, "weight m g", fontsize=11.5, color=RED)
ax.text(-2.9, -2.9, "holds if  2 x mu x F >= m g,   so   F >= m g / (2 mu)", fontsize=12.5)
ax.set_xlim(-3.0, 3.0); ax.set_ylim(-3.2, 2.0); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig04-gripper.png")

# Figure 5: squeeze force against mu
mu = np.linspace(0.08, 1.0, 300)
fig, ax = plt.subplots(figsize=(10, 5))
for m, col in [(0.2, GREEN), (0.8, BLUE), (2.0, RED)]:
    ax.plot(mu, m * G / (2 * mu), color=col, lw=3, label=f"part of {m} kg (holding still)")
ax.axhline(40, color=BLACK, ls="--", lw=2); ax.text(0.55, 42, "most this gripper can squeeze: 40 N", fontsize=11.5)
ax.set_xlabel("friction coefficient mu between pads and part"); ax.set_ylabel("squeeze per finger (N)")
ax.set_ylim(0, 100); ax.grid(alpha=0.3); ax.legend(loc="upper right", fontsize=11)
ax.set_title("slippery parts (small mu) need much more squeeze", fontsize=12.5)
save(fig, "fig05-squeeze-vs-mu.png")

# Figure 6: braking distance on each floor at 1.5 m/s
fig, ax = plt.subplots(figsize=(10, 4.8))
labels = ["dry concrete", "dusty floor", "wet tiles", "icy floor"]
br = [1.5 ** 2 / (2 * m * G) for m in mus]
ax.barh(range(4), [0.45] * 4, color=L_ORANGE, edgecolor=BLACK, label="reaction 0.3 s x 1.5 m/s = 0.45 m")
ax.barh(range(4), br, left=[0.45] * 4, color=BLUE, edgecolor=BLACK, label="braking v^2 / (2 mu g)")
for i, b in enumerate(br):
    ax.text(0.45 + b + 0.03, i, f"{0.45 + b:.2f} m", va="center", fontsize=11.5)
ax.set_yticks(range(4)); ax.set_yticklabels(labels); ax.invert_yaxis()
ax.set_xlabel("stopping distance at 1.5 m/s (m)"); ax.set_xlim(0, 1.9); ax.grid(axis="x", alpha=0.3)
ax.legend(loc="upper right", fontsize=10.5)
save(fig, "fig06-braking-floors.png")
print("saved 6 figures")
