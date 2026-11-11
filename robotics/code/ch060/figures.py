# Figures for Chapter 60 - Motion in two directions (first look at vectors).
# Run:  python figures.py      (saves PNG files in ../../images/ch060/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch060")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"
G = 9.81


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, x0, y0, x1, y1, col, lw=3, ls="-"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", color=col, lw=lw, ls=ls))


# Figure 1: a vector and its two parts
fig, ax = plt.subplots(figsize=(7, 6))
arrow(ax, 0, 0, 2.4, 4.0, BLUE, 3.5)
arrow(ax, 0, 0, 2.4, 0, RED, 2.5)
arrow(ax, 2.4, 0, 2.4, 4.0, GREEN, 2.5)
ax.text(0.65, 2.4, "the throw:\n4.66 m/s\nat 59 deg", fontsize=12, color=BLUE, ha="right")
ax.text(1.2, -0.35, "across part: 4.66 cos 59 = 2.4 m/s", ha="center", fontsize=11.5, color=RED)
ax.text(2.5, 2.0, "up part:\n4.66 sin 59\n= 4.0 m/s", fontsize=11.5, color=GREEN)
t = np.linspace(0, math.radians(59.04), 50)
ax.plot(0.7 * np.cos(t), 0.7 * np.sin(t), color=BLACK, lw=1.5)
ax.text(0.78, 0.35, "59 deg", fontsize=11.5)
ax.set_aspect("equal"); ax.set_xlim(-1.4, 4.0); ax.set_ylim(-0.8, 4.5)
ax.set_xlabel("across (m/s)"); ax.set_ylabel("up (m/s)"); ax.grid(alpha=0.3)
save(fig, "fig01-components.png")

# Figure 2: adding two vectors tip to tail, and subtracting positions
fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
ax = axes[0]
arrow(ax, 0, 0, 3, 1, BLUE); arrow(ax, 3, 1, 4, 3.5, GREEN); arrow(ax, 0, 0, 4, 3.5, RED, 3.5)
ax.text(1.9, 0.12, "p = (3, 1)", color=BLUE, fontsize=12, ha="center")
ax.text(3.6, 2.0, "q = (1, 2.5)", color=GREEN, fontsize=12)
ax.text(0.2, 2.6, "p + q = (4, 3.5)", color=RED, fontsize=12)
ax.set_title("adding: put q at the tip of p", fontsize=12.5)
ax.set_aspect("equal"); ax.set_xlim(-0.5, 5.5); ax.set_ylim(-0.5, 4.2); ax.grid(alpha=0.3)
ax = axes[1]
ax.plot([1], [2], "s", color=ORANGE, mec=BLACK, ms=14); ax.text(1.1, 1.55, "robot (1, 2)", fontsize=12)
ax.plot([4], [6], "o", color=BLUE, ms=12); ax.text(4.15, 5.9, "ball (4, 6)", fontsize=12)
arrow(ax, 1, 2, 4, 6, RED, 3.5)
arrow(ax, 0, 0, 1, 2, GREY, 2, "--"); arrow(ax, 0, 0, 4, 6, GREY, 2, "--")
ax.text(3.0, 2.3, "ball - robot\n= (3, 4)\n5.0 m", color=RED, fontsize=12)
ax.plot([0], [0], "k+", ms=12); ax.text(0.1, -0.35, "origin", fontsize=11.5)
ax.set_title("subtracting: the arrow from robot to ball", fontsize=12.5)
ax.set_aspect("equal"); ax.set_xlim(-0.5, 6.5); ax.set_ylim(-0.7, 7); ax.grid(alpha=0.3)
save(fig, "fig02-add-subtract.png")

# Figure 3: dropped and thrown balls fall together
fig, ax = plt.subplots(figsize=(10, 6))
for k in range(0, 9):
    tk = k * 0.1
    yk = 3.0 - 0.5 * G * tk ** 2
    if yk < 0:
        break
    ax.plot([0], [yk], "o", color=GREY, ms=12)
    ax.plot([2.0 * tk], [yk], "o", color=BLUE, ms=12)
    ax.plot([-0.4, 2.0 * tk + 0.3], [yk, yk], color=GREY, lw=0.6, ls=":")
    if k != 1:
        ax.text(-0.5, yk, f"{tk:.1f} s", ha="right", va="center", fontsize=10.5)
tt = np.linspace(0, math.sqrt(6 / G), 100)
ax.plot(2.0 * tt, 3.0 - 0.5 * G * tt ** 2, color=BLUE, lw=1.5)
ax.text(0.0, 3.2, "dropped", color=GREY, fontsize=12, ha="center")
ax.text(0.45, 3.2, "thrown sideways at 2.0 m/s", color=BLUE, fontsize=12)
ax.set_xlabel("across (m)"); ax.set_ylabel("height (m)"); ax.set_xlim(-1.1, 2.0); ax.set_ylim(-0.1, 3.5)
ax.set_title("a photo every 0.1 s: both balls are always at the same height", fontsize=12.5)
save(fig, "fig03-drop-and-throw.png")

# Figure 4: the parcel throw of Chapter 45, with velocity arrows
ux, uy, h0 = 2.4, 4.0, 0.5
T = 0.863
tt = np.linspace(0, T, 200)
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(ux * tt, h0 + uy * tt - 0.5 * G * tt ** 2, color=ORANGE, lw=3)
for tk in [0.0, 0.2, 0.408, 0.6, 0.8]:
    x = ux * tk; y = h0 + uy * tk - 0.5 * G * tk ** 2; vy = round(uy - G * tk, 1) + 0.0
    k = 0.12
    arrow(ax, x, y, x + k * ux, y, RED, 2)
    arrow(ax, x, y, x, y + k * vy, GREEN, 2)
    ax.plot([x], [y], "o", color=ORANGE, mec=BLACK, ms=9)
    ax.text(x + 0.05 if vy > -3 else x - 0.05, y + 0.06 if vy > -1 else y - 0.25, f"vy = {vy:+.1f}", fontsize=10.5, color=GREEN, ha="left" if vy > -3 else "right")
ax.add_patch(plt.Rectangle((1.85, 0), 0.3, 0.3, color=GREY, zorder=0))
ax.text(2.0, 0.08, "bin", ha="center", fontsize=11)
ax.plot([], [], color=RED, lw=2, label="across part: always 2.4 m/s")
ax.plot([], [], color=GREEN, lw=2, label="up part: falls by 9.81 m/s every second")
ax.set_aspect("equal"); ax.set_xlim(-0.2, 2.6); ax.set_ylim(0, 1.75)
ax.set_xlabel("across (m)"); ax.set_ylabel("height (m)"); ax.grid(alpha=0.3); ax.legend(loc="upper right", fontsize=10.5)
save(fig, "fig04-parcel-throw.png")

# Figure 5: the same speed at different angles
fig, ax = plt.subplots(figsize=(10, 5.2))
cols = {15: GREY, 30: GREEN, 45: RED, 60: BLUE, 75: ORANGE}
for ang, col in cols.items():
    u = 5.0
    ux_, uy_ = u * math.cos(math.radians(ang)), u * math.sin(math.radians(ang))
    T_ = 2 * uy_ / G
    tt = np.linspace(0, T_, 200)
    ax.plot(ux_ * tt, uy_ * tt - 0.5 * G * tt ** 2, color=col, lw=3 if ang == 45 else 2.2,
            label=f"{ang} deg: lands at {ux_ * T_:.2f} m")
ax.set_xlabel("across (m)"); ax.set_ylabel("height (m)"); ax.set_aspect("equal")
ax.set_xlim(0, 2.8); ax.set_ylim(0, 1.3); ax.grid(alpha=0.3); ax.legend(loc="upper right", fontsize=10.5)
ax.set_title("5 m/s thrown from the ground: 30 and 60 deg land at the same place", fontsize=12.5)
save(fig, "fig05-angles.png")

# Figure 6: a drone drops a parcel
H, V = 20.0, 8.0
Tf = math.sqrt(2 * H / G)
rel = 100 - V * Tf
fig, ax = plt.subplots(figsize=(10, 5.5))
tt = np.linspace(0, Tf, 200)
ax.plot(rel + V * tt, H - 0.5 * G * tt ** 2, color=ORANGE, lw=3, label="the parcel's path (a parabola)")
ax.plot([rel - 20, 100 + 6], [H, H], color=GREY, lw=2, ls="--", label="the drone's path at 8 m/s")
for k in range(0, 9):
    tk = k * 0.25
    ax.plot([rel + V * tk], [H], "s", color=BLUE, ms=6)
    yk = H - 0.5 * G * tk ** 2
    if yk > 0:
        ax.plot([rel + V * tk], [yk], "o", color=ORANGE, mec=BLACK, ms=7)
ax.annotate("release here\n83.85 m east", (rel, H), xytext=(rel - 18, H - 7), fontsize=11.5, arrowprops=dict(arrowstyle="-|>"))
ax.plot([100], [0], "v", color=RED, ms=14)
ax.text(100, 1.2, "target\n100 m", ha="center", fontsize=11.5, color=RED)
ax.annotate("", xy=(100, -2.2), xytext=(rel, -2.2), arrowprops=dict(arrowstyle="<->", lw=1.5))
ax.text((rel + 100) / 2, -4.2, "16.15 m = 8 m/s x 2.02 s", ha="center", fontsize=11.5)
ax.set_xlim(rel - 22, 108); ax.set_ylim(-5.5, 24)
ax.set_xlabel("east (m)"); ax.set_ylabel("height (m)"); ax.grid(alpha=0.3); ax.legend(loc="lower left", fontsize=10.5)
ax.set_title("squares: the drone every 0.25 s.  dots: the parcel. Each dot is right under its square.", fontsize=11.5)
save(fig, "fig06-drone-drop.png")
print("saved 6 figures")
