# Figures for Chapter 69 - Wheels and rolling.
# Run:  python figures.py      (saves PNG files in ../../images/ch069/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch069")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"
G = 9.81


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, x0, y0, x1, y1, col, lw=3):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", color=col, lw=lw, mutation_scale=18))


# Figure 1: velocities on a rolling wheel
fig, ax = plt.subplots(figsize=(9, 6))
R = 1.0
ax.fill_between([-2.5, 3.5], -0.3, 0, color=L_GREY)
ax.add_patch(plt.Circle((0, R), R, fill=False, ec=BLACK, lw=3))
ax.plot([0], [R], "o", color=BLACK, ms=8)
k = 0.9
arrow(ax, 0, 2 * R, 2 * k, 2 * R, RED); ax.text(2 * k + 0.1, 2 * R - 0.05, "top: 2v", fontsize=12, color=RED)
arrow(ax, 0, R, k, R, BLUE); ax.text(k + 0.1, R - 0.05, "centre: v", fontsize=12, color=BLUE)
ax.plot([0], [0], "o", color=GREEN, ms=10); ax.text(-0.15, 0.12, "bottom: 0\n(touching the ground)", fontsize=12, color=GREEN, ha="right")
arrow(ax, R, R, R + k, R - k, GREY, 2); ax.text(R + k + 0.1, R - k + 0.25, "front: v x 1.41", fontsize=11, color=GREY)
ax.plot([0, 2 * k], [0, 2 * R], color=BLACK, ls=":", lw=1.2)
ax.text(-2.3, 2.3, "the wheel turns about the contact point:\nspeed grows with the height above the ground", fontsize=12)
ax.set_xlim(-2.5, 3.6); ax.set_ylim(-0.3, 2.8); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig01-rolling-velocities.png")

# Figure 2: the cycloid traced by a point on the rim
Rw, V = 0.05, 0.5
om = V / Rw
t = np.linspace(0, 2 * 2 * math.pi / om, 400)
fig, ax = plt.subplots(figsize=(11, 3.8))
ax.plot(V * t - Rw * np.sin(om * t), Rw - Rw * np.cos(om * t), color=RED, lw=3, label="path of one point on the rim (a cycloid)")
ax.plot(V * t, np.full_like(t, Rw), color=BLUE, lw=2, ls="--", label="path of the centre (a straight line)")
for xc in [0.0, 0.1571, 0.3142, 0.4712, 0.6283]:
    ax.add_patch(plt.Circle((xc, Rw), Rw, fill=False, ec=GREY, lw=1))
ax.axhline(0, color=BLACK, lw=1.5)
ax.set_aspect("equal"); ax.set_xlim(-0.06, 0.70); ax.set_ylim(-0.01, 0.13)
ax.set_xlabel("distance along the floor (m)"); ax.set_ylabel("height (m)"); ax.legend(loc="upper right", fontsize=10.5)
save(fig, "fig02-cycloid.png")

# Figure 3: the rolling race
ang = math.radians(10)
fig, ax = plt.subplots(figsize=(10, 5))
for name, kk, col in [("sliding block (no friction)", 0.0, GREY), ("solid ball", 0.4, GREEN), ("solid disc", 0.5, BLUE), ("thin ring", 1.0, RED)]:
    a = G * math.sin(ang) / (1 + kk)
    T = math.sqrt(4 / a)
    tt = np.linspace(0, 2.3, 300)
    ax.plot(tt, np.minimum(0.5 * a * tt ** 2, 2.0), color=col, lw=3, label=f"{name}: {T:.2f} s")
ax.axhline(2.0, color=BLACK, ls="--", lw=1.2); ax.text(0.05, 2.05, "bottom of the 2 m slope", fontsize=11)
ax.set_xlabel("time (s)"); ax.set_ylabel("distance down the slope (m)"); ax.set_ylim(0, 2.3); ax.grid(alpha=0.3)
ax.legend(loc="lower right", fontsize=11)
ax.set_title("a 10 deg slope: the more mass near the rim, the slower it rolls", fontsize=12.5)
save(fig, "fig03-roll-race.png")

# Figure 4: kinds of wheels (schematic, from above)
fig, axes = plt.subplots(1, 4, figsize=(15, 4.2))
ax = axes[0]
ax.add_patch(plt.Rectangle((-0.25, -0.6), 0.5, 1.2, color=BLACK)); ax.set_title("fixed wheel:\nrolls forwards only", fontsize=12)
ax = axes[1]
ax.add_patch(plt.Rectangle((-0.2, -0.45), 0.4, 0.9, color=BLACK)); ax.plot([0, 0], [0.45, 0.85], color=GREY, lw=3); ax.plot([0], [0.85], "o", color=GREY, ms=10)
ax.set_title("caster: swivels freely\n(Rover's front wheel)", fontsize=12)
ax = axes[2]
ax.add_patch(plt.Circle((0, 0), 0.6, fill=False, ec=BLACK, lw=6))
for k in range(8):
    a = 2 * math.pi * k / 8
    cx, cy = 0.6 * math.cos(a), 0.6 * math.sin(a)
    ax.add_patch(plt.Polygon([(cx - 0.12 * math.sin(a) - 0.06 * math.cos(a), cy + 0.12 * math.cos(a) - 0.06 * math.sin(a)),
                              (cx + 0.12 * math.sin(a) - 0.06 * math.cos(a), cy - 0.12 * math.cos(a) - 0.06 * math.sin(a)),
                              (cx + 0.12 * math.sin(a) + 0.06 * math.cos(a), cy - 0.12 * math.cos(a) + 0.06 * math.sin(a)),
                              (cx - 0.12 * math.sin(a) + 0.06 * math.cos(a), cy + 0.12 * math.cos(a) + 0.06 * math.sin(a))], color=ORANGE, ec=BLACK))
ax.set_title("omni wheel (side view): small rollers\nlet it slide sideways", fontsize=12)
ax = axes[3]
ax.add_patch(plt.Rectangle((-0.3, -0.6), 0.6, 1.2, color=L_GREY, ec=BLACK))
for y in np.linspace(-0.3, 0.3, 4):
    ax.plot([-0.3, 0.3], [y - 0.3, y + 0.3], color=ORANGE, lw=5)
ax.set_title("mecanum wheel (from above):\nrollers at 45 deg", fontsize=12)
for ax in axes:
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1.1); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig04-wheel-kinds.png")

# Figure 5: rolling resistance against wheel diameter, on different ground
D = np.linspace(0.04, 0.40, 200)
fig, ax = plt.subplots(figsize=(10, 5))
for name, c10, col in [("hard floor", 0.010, GREEN), ("carpet", 0.04, ORANGE), ("short grass", 0.08, BLUE), ("soft sand", 0.20, RED)]:
    ax.plot(D * 100, c10 * np.sqrt(0.10 / D), color=col, lw=3, label=name)
ax.set_xlabel("wheel diameter (cm)"); ax.set_ylabel("rolling resistance coefficient C_rr"); ax.grid(alpha=0.3)
ax.legend(loc="upper right", fontsize=11); ax.set_ylim(0, 0.35)
ax.set_title("bigger wheels roll more easily, especially on soft ground (rough guide)", fontsize=12.5)
save(fig, "fig05-rolling-resistance.png")
print("saved 5 figures")
