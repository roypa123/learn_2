# Figures for Chapter 61 - Forces and Newton's three laws.
# Run:  python figures.py      (saves PNG files in ../../images/ch061/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch061")
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


def rover(ax, x, y, w=2.0, h=0.8, ang=0.0):
    c, s = math.cos(ang), math.sin(ang)
    pts = [(-w / 2, 0), (w / 2, 0), (w / 2, h), (-w / 2, h)]
    xy = [(x + c * px - s * py, y + s * px + c * py) for px, py in pts]
    ax.add_patch(plt.Polygon(xy, color=ORANGE, ec=BLACK, zorder=4))
    for px in (-w / 3, w / 3):
        ax.add_patch(plt.Circle((x + c * px, y + s * px), 0.22, color=BLACK, zorder=5))


# Figure 1: free-body diagram of Rover speeding up
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot([-4, 4], [-0.22, -0.22], color=BLACK, lw=2)
ax.fill_between([-4, 4], -0.6, -0.22, color=L_GREY)
rover(ax, 0, 0)
arrow(ax, 0, 0.4, 0, -2.0, BLUE)
ax.text(0.15, -1.7, "weight 39.2 N\n(gravity pulls down)", fontsize=11.5, color=BLUE)
arrow(ax, 0, 0.4, 0, 2.8, GREEN)
ax.text(0.15, 2.3, "ground pushes up 39.2 N", fontsize=11.5, color=GREEN)
arrow(ax, 1.0, 0.4, 2.6, 0.4, RED)
ax.text(2.7, 0.3, "motors push\nforwards 3.0 N", fontsize=11.5, color=RED)
arrow(ax, -1.0, 0.4, -1.6, 0.4, GREY)
ax.text(-1.7, 0.9, "rolling resistance\nand air 0.7 N", fontsize=11.5, color=GREY, ha="right")
ax.text(-3.9, 3.3, "up and down: 39.2 - 39.2 = 0 (balanced)\nalong the floor: 3.0 - 0.7 = 2.3 N forwards (not balanced)", fontsize=12)
ax.set_xlim(-4, 4.6); ax.set_ylim(-2.2, 4.0); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig01-free-body.png")

# Figure 2: F = m a, acceleration against force for several masses
F = np.linspace(0, 10, 100)
fig, ax = plt.subplots(figsize=(10, 5.2))
for m, col in [(2, RED), (4, BLUE), (8, GREEN), (25, GREY)]:
    ax.plot(F, F / m, color=col, lw=3, label=f"mass {m} kg: slope 1/{m}")
ax.plot([2], [0.5], "o", color=BLUE, ms=9)
ax.annotate("Rover: 2 N gives 0.5 m/s^2", (2, 0.5), xytext=(3.2, 0.25), fontsize=11.5, arrowprops=dict(arrowstyle="-|>"))
ax.set_xlabel("net force F (N)"); ax.set_ylabel("acceleration a (m/s^2)"); ax.set_ylim(0, 3); ax.grid(alpha=0.3)
ax.legend(loc="upper left", fontsize=11)
save(fig, "fig02-f-equals-ma.png")

# Figure 3: Newton's third law pairs
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
ax = axes[0]
ax.fill_between([-2.5, 2.5], -0.8, 0, color=L_GREY)
ax.add_patch(plt.Circle((0, 0.8), 0.8, color=BLACK, zorder=3))
ax.add_patch(plt.Circle((0, 0.8), 0.3, color=GREY, zorder=4))
arrow(ax, 0.0, 0.03, -1.6, 0.03, RED)
ax.text(-1.0, 0.18, "tyre pushes\nground backwards", ha="center", fontsize=11.5, color=RED)
arrow(ax, 0.0, -0.3, 1.6, -0.3, GREEN)
ax.text(0.85, -0.72, "ground pushes tyre forwards", ha="center", fontsize=11.5, color=GREEN)
ax.text(0, 1.9, "turning wheel", ha="center", fontsize=12)
ax.annotate("", xy=(0.7, 1.55), xytext=(-0.7, 1.55), arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3,rad=-0.5", lw=1.5))
ax.set_xlim(-2.5, 2.5); ax.set_ylim(-0.9, 2.2); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("a wheel on the ground", fontsize=12.5)
ax = axes[1]
ax.add_patch(plt.Rectangle((-1.2, 0.0), 2.4, 0.3, color=ORANGE, ec=BLACK, zorder=3))
ax.plot([-1.0, 1.0], [0.42, 0.42], color=BLACK, lw=4)
arrow(ax, 0, -0.1, 0, -1.6, RED)
ax.text(0.15, -1.3, "propeller pushes\nair down", fontsize=11.5, color=RED)
arrow(ax, 0, 0.6, 0, 2.0, GREEN)
ax.text(0.15, 1.6, "air pushes\npropeller up (thrust)", fontsize=11.5, color=GREEN)
for xx in (-0.95, -0.65, -0.35):
    ax.annotate("", xy=(xx, -1.4), xytext=(xx, -0.3), arrowprops=dict(arrowstyle="->", color=L_BLUE, lw=2))
ax.set_xlim(-2.2, 2.2); ax.set_ylim(-1.8, 2.2); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("a drone motor and propeller", fontsize=12.5)
save(fig, "fig03-third-law.png")

# Figure 4: forces on a ramp
th = math.radians(20)
fig, ax = plt.subplots(figsize=(10, 7))
L = 8.0
ax.fill([0, L, L], [0, 0, L * math.tan(th)], color=L_GREY, zorder=0)
ax.plot([0, L], [0, L * math.tan(th)], color=BLACK, lw=2, zorder=1)
cx = 4.5
cy = cx * math.tan(th)
rover(ax, cx, cy, w=1.6, h=0.7, ang=th)
mx, my = cx - 0.35 * math.sin(th), cy + 0.35 * math.cos(th)


def zarrow(x0, y0, x1, y1, col):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), zorder=7,
                arrowprops=dict(arrowstyle="-|>", color=col, lw=3, mutation_scale=20))


W = 2.6
zarrow(mx, my, mx, my - W, BLUE)
ax.text(mx - 0.1, my - W - 0.05, "weight m g", fontsize=12, color=BLUE, va="top", ha="right")
al = W * math.sin(th)
zarrow(mx, my, mx - al * math.cos(th), my - al * math.sin(th), RED)
ax.text(mx - al * math.cos(th) - 0.15, my - al * math.sin(th) + 0.1, "along the ramp:\nm g sin(angle)", fontsize=12, color=RED, ha="right")
pe = W * math.cos(th)
zarrow(mx, my, mx + pe * math.sin(th), my - pe * math.cos(th), GREEN)
ax.text(mx + pe * math.sin(th) + 0.15, my - pe * math.cos(th) - 0.1, "into the ramp:\nm g cos(angle)", fontsize=12, color=GREEN)
ax.plot([mx - al * math.cos(th), mx], [my - al * math.sin(th), my - W], color=GREY, ls=":", lw=1.5, zorder=6)
ax.plot([mx + pe * math.sin(th), mx], [my - pe * math.cos(th), my - W], color=GREY, ls=":", lw=1.5, zorder=6)
t = np.linspace(0, th, 30)
ax.plot(1.6 * np.cos(t), 1.6 * np.sin(t), color=BLACK, lw=1.5)
ax.text(1.75, 0.18, "angle", fontsize=12)
ax.set_xlim(-0.3, 8.4); ax.set_ylim(-1.3, 3.3); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig04-ramp-forces.png")

# Figure 5: drone thrust needed
labels = ["hover", "climb\n+2 m/s^2", "climb\n+5 m/s^2", "descend\n-2 m/s^2"]
acc = [0, 2, 5, -2]
thr = [1.2 * (G + a) for a in acc]
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(range(4), thr, color=[GREY, GREEN, GREEN, BLUE], edgecolor=BLACK)
ax.axhline(1.2 * G, color=BLACK, ls="--", lw=2, label="weight 11.77 N")
ax.axhline(24, color=RED, ls="--", lw=2, label="most the 4 motors can give: 24 N")
for i, v in enumerate(thr):
    ax.text(i, v + 0.4, f"{v:.2f} N", ha="center", fontsize=11.5)
ax.set_xticks(range(4)); ax.set_xticklabels(labels); ax.set_ylabel("total thrust (N)"); ax.set_ylim(0, 27)
ax.grid(axis="y", alpha=0.3); ax.legend(loc="upper right", fontsize=11)
save(fig, "fig05-drone-thrust.png")

# Figure 6: ground force during a landing, stiff against bent knees
t = np.linspace(-0.05, 0.35, 800)
m = 30.0


def pulse(t, T):
    a = 2.0 / T
    return np.where((t >= 0) & (t <= T), m * (G + a), m * G)


fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(t, pulse(t, 0.05), color=RED, lw=3, label="stiff legs: stops in 0.05 s, peak 1494 N")
ax.plot(t, pulse(t, 0.2), color=GREEN, lw=3, label="bent knees: stops in 0.2 s, peak 594 N")
ax.axhline(m * G, color=BLACK, ls="--", lw=1.5)
ax.text(0.22, m * G + 40, "standing still: weight 294 N", fontsize=11.5)
ax.set_xlabel("time since the feet touched the ground (s)"); ax.set_ylabel("force from the ground (N)")
ax.set_ylim(0, 1700); ax.grid(alpha=0.3); ax.legend(loc="upper right", fontsize=11)
ax.set_title("a 30 kg robot landing at 2 m/s: the same change of speed, spread over a longer time", fontsize=12)
save(fig, "fig06-landing.png")
print("saved 6 figures")
