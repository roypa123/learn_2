# Figures for Chapter 64 - Turning: angle, angular speed, angular acceleration.
# Run:  python figures.py      (saves PNG files in ../../images/ch064/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch064")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, x0, y0, x1, y1, col, lw=3):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", color=col, lw=lw, mutation_scale=18))


# Figure 1: a spinning bar - outer points move faster
fig, ax = plt.subplots(figsize=(8, 7))
th = math.radians(35)
ax.plot([0, 2.2 * math.cos(th)], [0, 2.2 * math.sin(th)], color=ORANGE, lw=10, solid_capstyle="round")
ax.plot([0], [0], "o", color=BLACK, ms=12)
for r, col in [(0.7, GREEN), (1.4, BLUE), (2.1, RED)]:
    x, y = r * math.cos(th), r * math.sin(th)
    ax.plot([x], [y], "o", color=col, ms=11, zorder=5)
    v = 0.6 * r
    arrow(ax, x, y, x - v * math.sin(th), y + v * math.cos(th), col)
    ax.text(x + 0.12, y - 0.25, f"r = {r / 7 * 0.1 * 10:.1f} m: v = {r / 7 * 0.1 * 10 * 2:.1f} m/s", fontsize=11, color=col)
t = np.linspace(0, 2 * math.pi, 200)
for r in [0.7, 1.4, 2.1]:
    ax.plot(r * np.cos(t), r * np.sin(t), color=GREY, lw=0.8, ls=":")
ax.annotate("", xy=(0.45 * math.cos(th + 0.9), 0.45 * math.sin(th + 0.9)), xytext=(0.45, 0.0),
            arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=0.4", lw=1.5))
ax.text(-2.4, 2.2, "the whole bar turns at omega = 2 rad/s\nspeed of a point: v = omega x r", fontsize=12)
ax.set_xlim(-2.5, 2.8); ax.set_ylim(-1.0, 2.6); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig01-spinning-bar.png")

# Figure 2: turntable speeding up - omega and theta against time
tt = np.linspace(0, 3, 300)
alpha = math.pi
om = np.minimum(alpha * tt, 2 * math.pi)
thv = np.where(tt < 2, 0.5 * alpha * tt ** 2, 2 * math.pi + 2 * math.pi * (tt - 2))
fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
a1.plot(tt, om, color=BLUE, lw=3)
a1.fill_between(tt[tt <= 2], 0, om[tt <= 2], color=L_BLUE)
a1.text(1.3, 1.5, "area = 1/2 x 2 x 6.28\n= 6.28 rad (one turn)", fontsize=11.5)
a1.text(0.2, 4.6, "slope = alpha = 3.14 rad/s^2", fontsize=11.5, color=GREEN)
a1.set_ylabel("omega (rad/s)"); a1.grid(alpha=0.3); a1.set_ylim(0, 7.5)
a2.plot(tt, thv, color=RED, lw=3)
a2.axhline(2 * math.pi, color=GREY, ls="--", lw=1.5); a2.text(0.1, 2 * math.pi + 0.5, "one turn = 6.28 rad", fontsize=11.5)
a2.set_ylabel("angle theta (rad)"); a2.set_xlabel("time (s)"); a2.grid(alpha=0.3)
save(fig, "fig02-omega-theta.png")

# Figure 3: moving in a circle - velocity along, acceleration inwards
fig, ax = plt.subplots(figsize=(7.5, 7))
R = 2.0
ax.plot(R * np.cos(t), R * np.sin(t), color=GREY, lw=2, ls="--")
ax.plot([0], [0], "+", color=BLACK, ms=14)
for ang in [0.3, 1.9, 3.6, 5.0]:
    x, y = R * math.cos(ang), R * math.sin(ang)
    ax.add_patch(plt.Circle((x, y), 0.17, color=ORANGE, ec=BLACK, zorder=5))
    arrow(ax, x, y, x - 1.0 * math.sin(ang), y + 1.0 * math.cos(ang), BLUE)
    arrow(ax, x, y, x - 0.8 * math.cos(ang), y - 0.8 * math.sin(ang), RED)
ax.plot([], [], color=BLUE, lw=3, label="velocity: along the circle")
ax.plot([], [], color=RED, lw=3, label="acceleration v^2 / r: towards the centre")
ax.text(0.1, -0.35, "centre", fontsize=11)
ax.set_xlim(-3.4, 3.4); ax.set_ylim(-3.2, 3.6); ax.set_aspect("equal"); ax.axis("off")
ax.legend(loc="upper center", fontsize=11)
save(fig, "fig03-circle.png")

# Figure 4: differential drive turning geometry (robot heading up, turning left)
fig, ax = plt.subplots(figsize=(9, 7))
Rc = 1.2
T = 0.6
ax.plot([0], [0], "+", color=BLACK, ms=14); ax.text(-0.1, -0.25, "centre of the turn", fontsize=11, ha="center")
arc = np.linspace(-0.25, 1.1, 100)
for r, col, ls, lw in [(Rc - T / 2, GREEN, "-", 2.5), (Rc, GREY, "--", 1.2), (Rc + T / 2, RED, "-", 2.5)]:
    ax.plot(r * np.cos(arc), r * np.sin(arc), color=col, lw=lw, ls=ls)
ax.add_patch(plt.Rectangle((Rc - T / 2, -0.25), T, 0.5, color=ORANGE, ec=BLACK, alpha=0.9, zorder=4))
for xw, col, v in [(Rc - T / 2, GREEN, 0.6), (Rc + T / 2, RED, 1.0)]:
    ax.add_patch(plt.Rectangle((xw - 0.05, -0.18), 0.1, 0.36, color=BLACK, zorder=5))
    arrow(ax, xw, 0, xw, v, col)
arrow(ax, Rc, 0, Rc, 0.8, BLUE)
ax.text(Rc - T / 2 - 0.3, 0.5, "v_L", color=GREEN, fontsize=12)
ax.text(Rc + T / 2 + 0.08, 0.9, "v_R", color=RED, fontsize=12)
ax.text(Rc + 0.05, 0.85, "v", color=BLUE, fontsize=12)
ax.annotate("", xy=(Rc, -0.45), xytext=(0, -0.45), arrowprops=dict(arrowstyle="<->", lw=1.5))
ax.text(Rc / 2, -0.68, "radius R = v / omega", ha="center", fontsize=12)
ax.annotate("", xy=(Rc + T / 2, -0.95), xytext=(Rc - T / 2, -0.95), arrowprops=dict(arrowstyle="<->", lw=1.5))
ax.text(Rc, -1.18, "track T", ha="center", fontsize=12)
ax.text(-1.0, 1.75, "omega = (v_R - v_L) / T\nv = (v_L + v_R) / 2", fontsize=13)
ax.text(-1.0, 1.35, "Rover drives up the page and turns left.", fontsize=11)
ax.set_xlim(-1.1, 2.1); ax.set_ylim(-1.3, 2.2); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig04-diff-drive.png")

# Figure 5: safe cornering speed against radius
rr = np.linspace(0.1, 4, 200)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(rr, np.sqrt(0.8 * 9.81 * rr), color=GREEN, lw=3, label="wheels slide sideways, dry concrete (mu 0.8)")
ax.plot(rr, np.sqrt(0.3 * 9.81 * rr), color=BLUE, lw=3, label="wheels slide sideways, wet tiles (mu 0.3)")
ax.plot(rr, np.sqrt(0.2 * 9.81 * rr), color=RED, lw=3, label="tote slides (mu 0.2)")
ax.plot(rr, np.sqrt(0.2 * 9.81 / 1.5 * rr), color=BLACK, lw=2, ls="--", label="safe speed (tote limit / 1.5)")
ax.set_xlabel("radius of the corner (m)"); ax.set_ylabel("speed (m/s)"); ax.grid(alpha=0.3)
ax.legend(loc="upper left", fontsize=10.5); ax.set_ylim(0, 6.5)
ax.set_title("v = square root of (a_max x r): tight corners need low speeds", fontsize=12.5)
save(fig, "fig05-cornering.png")
print("saved 5 figures")
