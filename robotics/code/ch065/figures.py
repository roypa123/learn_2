# Figures for Chapter 65 - Torque and levers.
# Run:  python figures.py      (saves PNG files in ../../images/ch065/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch065")
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


# Figure 1: a door seen from above, pushed at three distances
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot([0, 0.85], [0, 0], color=ORANGE, lw=12, solid_capstyle="butt")
ax.plot([0], [0], "o", color=BLACK, ms=14)
ax.text(-0.03, -0.12, "hinge", ha="center", fontsize=12)
for r, col in [(0.05, GREY), (0.40, BLUE), (0.80, RED)]:
    arrow(ax, r, 0.35, r, 0.05, col)
    ax.text(r, 0.40, f"20 N at {r:.2f} m\ntorque {20 * r:.2f} N m", ha="center", fontsize=11, color=col)
ax.text(0.42, -0.2, "door, seen from above", ha="center", fontsize=11.5)
ax.set_xlim(-0.15, 1.0); ax.set_ylim(-0.3, 0.6); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig01-door.png")

# Figure 2: lever arm - the same force at different angles
fig, ax = plt.subplots(figsize=(9, 6))
ax.plot([0, 2.0], [0, 0], color=ORANGE, lw=10, solid_capstyle="butt")
ax.plot([0], [0], "o", color=BLACK, ms=14)
th = math.radians(30)
px, py = 2.0, 0.0
fx, fy = -1.2 * math.cos(th), 1.2 * math.sin(th)
arrow(ax, px, py, px + fx * -1 * 0 + fx, py + fy, RED)
ax.text(1.55, 0.5, "force F,\n30 deg to the bar", fontsize=11.5, color=RED)
ax.plot([px - 2.6 * math.cos(th), px + 0.6 * math.cos(th)], [py + 2.6 * math.sin(th), py - 0.6 * math.sin(th)], color=GREY, ls=":", lw=1.5)
d = 2.0 * math.sin(th)
fxp, fyp = d * math.sin(th), d * math.cos(th)
ax.plot([0, fxp], [0, fyp], color=GREEN, lw=2.5)
ax.text(-0.55, 0.45, "lever arm\nd = r sin(30)\n= 1.0 m", fontsize=11.5, color=GREEN)
ax.text(1.0, -0.3, "r = 2.0 m", ha="center", fontsize=11.5)
ax.text(-0.4, 1.75, "torque = F x d = F x r x sin(angle)", fontsize=12.5)
ax.set_xlim(-0.6, 2.8); ax.set_ylim(-0.5, 2.0); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig02-lever-arm.png")

# Figure 3: a balanced seesaw
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.plot([-2.2, 2.2], [0, 0], color=ORANGE, lw=10)
ax.fill([-0.25, 0.25, 0], [-0.8, -0.8, -0.05], color=GREY)
ax.add_patch(plt.Rectangle((-1.75, 0.08), 0.5, 0.5, color=BLUE)); ax.text(-1.5, 0.7, "30 kg", ha="center", fontsize=12)
ax.add_patch(plt.Rectangle((0.7, 0.08), 0.6, 0.65, color=RED)); ax.text(1.0, 0.85, "45 kg", ha="center", fontsize=12)
arrow(ax, -1.5, 0.08, -1.5, -0.7, BLUE); arrow(ax, 1.0, 0.08, 1.0, -0.9, RED)
ax.annotate("", xy=(-1.5, -1.1), xytext=(0, -1.1), arrowprops=dict(arrowstyle="<->", lw=1.5)); ax.text(-0.75, -1.35, "1.5 m", ha="center", fontsize=12)
ax.annotate("", xy=(1.0, -1.1), xytext=(0, -1.1), arrowprops=dict(arrowstyle="<->", lw=1.5)); ax.text(0.5, -1.35, "1.0 m", ha="center", fontsize=12)
ax.text(-2.2, 1.3, "30 x 9.81 x 1.5 = 441 N m (anticlockwise)  =  45 x 9.81 x 1.0 = 441 N m (clockwise)", fontsize=11.5)
ax.set_xlim(-2.4, 2.4); ax.set_ylim(-1.6, 1.6); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig03-seesaw.png")

# Figure 4: the three classes of lever
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
setups = [("class 1: pivot in the middle\n(seesaw, scissors, pliers)", 0.3, -1.0, 2.0),
          ("class 2: load in the middle\n(wheelbarrow, nutcracker)", -1.0, 0.5, 2.0),
          ("class 3: effort in the middle\n(your forearm, tweezers, many robot arms)", -1.0, 2.0, 0.5)]
for ax, (title, pivot, load, effort) in zip(axes, setups):
    ax.plot([-1.2, 2.2], [0, 0], color=ORANGE, lw=8)
    ax.fill([pivot - 0.15, pivot + 0.15, pivot], [-0.45, -0.45, -0.04], color=BLACK)
    arrow(ax, load, 0.05, load, -0.75, BLUE); ax.text(load, -0.95, "load", ha="center", fontsize=11, color=BLUE)
    if pivot < min(load, effort):          # pivot at one end: the effort must lift
        arrow(ax, effort, 0.06, effort, 0.8, RED)
    else:                                  # pivot in the middle: the effort pushes down on the other side
        arrow(ax, effort, 0.8, effort, 0.06, RED)
    ax.text(effort, 0.9, "effort", ha="center", fontsize=11, color=RED)
    ax.text(pivot, -0.65, "pivot", ha="center", fontsize=10.5) if pivot != load else None
    ax.set_title(title, fontsize=11.5); ax.set_xlim(-1.4, 2.4); ax.set_ylim(-1.2, 1.2); ax.axis("off")
save(fig, "fig04-lever-classes.png")

# Figure 5: holding torque against arm angle
ang = np.linspace(-90, 90, 300)
arm = 0.40 * G * 0.25 * np.cos(np.radians(ang))
pay = 0.25 * G * 0.50 * np.cos(np.radians(ang))
fig, ax = plt.subplots(figsize=(10, 5))
ax.fill_between(ang, 0, arm, color=L_ORANGE, label="the arm's own weight (0.40 kg at 0.25 m)")
ax.fill_between(ang, arm, arm + pay, color=L_BLUE, label="the payload (0.25 kg at 0.50 m)")
ax.plot(ang, arm + pay, color=BLUE, lw=3, label="total holding torque")
ax.axhline(3.0, color=RED, ls="--", lw=2, label="motor limit 3.0 N m")
ax.set_xticks([-90, -60, -30, 0, 30, 60, 90])
ax.set_xlabel("arm angle above the horizontal (deg)"); ax.set_ylabel("torque (N m)"); ax.set_ylim(0, 4.4)
ax.grid(alpha=0.3); ax.legend(loc="upper center", ncol=2, fontsize=10.5)
ax.set_title("the arm is hardest to hold straight out (0 deg)", fontsize=12.5)
save(fig, "fig05-arm-torque.png")

# Figure 6: a wheel meeting a rug edge
r, h = 0.025, 0.010
fig, ax = plt.subplots(figsize=(8, 6))
cx, cy = 0.0, r
edge_x = -math.sqrt(r ** 2 - (r - h) ** 2) + cx + 2 * math.sqrt(r ** 2 - (r - h) ** 2)
ex, ey = cx + math.sqrt(r ** 2 - (r - h) ** 2), h
ax.fill_between([-0.05, ex], -0.005, 0, color=L_GREY)
ax.fill_between([ex, 0.06], -0.005, h, color=L_ORANGE)
ax.text(0.05, 0.003, "rug", fontsize=11)
ax.add_patch(plt.Circle((cx, cy), r, fill=False, ec=BLACK, lw=2.5))
ax.plot([cx], [cy], "o", color=BLACK, ms=6)
ax.plot([ex], [ey], "o", color=RED, ms=9)
ax.annotate("edge: the wheel\nturns about here", (ex, ey), xytext=(0.03, 0.035), fontsize=10.5, color=RED, arrowprops=dict(arrowstyle="-|>", color=RED))
arrow(ax, cx, cy, cx, cy - 0.022, BLUE); ax.text(cx - 0.002, cy - 0.016, "load W", ha="right", fontsize=11, color=BLUE)
arrow(ax, cx - 0.03, cy, cx - 0.003, cy, GREEN); ax.text(cx - 0.031, cy + 0.003, "push P", fontsize=11, color=GREEN)
ax.plot([cx, ex], [h, h], color=BLUE, lw=1.5, ls=":"); ax.text((cx + ex) / 2, h - 0.004, "d", ha="center", fontsize=12, color=BLUE)
ax.plot([ex, ex], [h, cy], color=GREEN, lw=1.5, ls=":"); ax.text(ex + 0.001, (h + cy) / 2, "r - h", fontsize=12, color=GREEN)
ax.text(-0.045, 0.058, "rolls over when  P x (r - h) > W x d", fontsize=12.5)
ax.set_xlim(-0.05, 0.06); ax.set_ylim(-0.006, 0.064); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig06-rug-edge.png")
print("saved 6 figures")
