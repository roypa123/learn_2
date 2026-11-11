# Figures for Chapter 70 - Centre of mass and balance.
# Run:  python figures.py      (saves PNG files in ../../images/ch070/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch070")
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


# Figure 1: a light bar with masses balances at the centre of mass
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot([0, 1.0], [0, 0], color=GREY, lw=6)
masses = [(0.1, 3, BLUE), (0.5, 1, GREEN), (0.9, 2, RED)]
for x, m, col in masses:
    ax.add_patch(plt.Rectangle((x - 0.03 * m ** 0.5, 0.03), 0.06 * m ** 0.5, 0.06 * m ** 0.5 + 0.04, color=col, ec=BLACK))
    ax.text(x, 0.2 + 0.06 * m ** 0.5, f"{m} kg\nat {x} m", ha="center", fontsize=11.5)
com = sum(x * m for x, m, c in masses) / sum(m for x, m, c in masses)
ax.fill([com - 0.04, com + 0.04, com], [-0.15, -0.15, -0.02], color=BLACK)
ax.text(com, -0.25, f"balances at {com:.3f} m\n(3 x 0.1 + 1 x 0.5 + 2 x 0.9) / 6", ha="center", fontsize=11.5)
ax.set_xlim(-0.1, 1.1); ax.set_ylim(-0.42, 0.5); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig01-balance-point.png")

# Figure 2: the support polygon of Rover seen from above
fig, ax = plt.subplots(figsize=(8, 6.5))
tri = [(0.0, 0.075), (0.0, -0.075), (-0.09, 0.0)]
ax.fill([p[0] for p in tri], [p[1] for p in tri], color=L_GREEN, ec=GREEN, lw=2)
for (x, y), lab in [((0.0, 0.075), "left wheel"), ((0.0, -0.075), "right wheel"), ((-0.09, 0.0), "caster")]:
    ax.plot([x], [y], "o", color=BLACK, ms=12)
    ax.text(x + 0.008, y + (0.012 if y >= 0 else -0.02), lab, fontsize=11.5)
ax.plot([0.0082], [0], "X", color=RED, ms=14); ax.text(0.012, -0.012, "design A:\ncentre of mass\noutside: tips forward", fontsize=11, color=RED)
ax.plot([-0.0223], [0], "P", color=BLUE, ms=14); ax.text(-0.075, -0.045, "design B:\ninside: stable", fontsize=11, color=BLUE)
ax.text(-0.1, 0.1, "Rover from above (forward = right). The green triangle\nis its support polygon.", fontsize=11.5)
ax.set_xlim(-0.11, 0.07); ax.set_ylim(-0.1, 0.12); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig02-support-polygon.png")

# Figure 3: tipping on a side slope
fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))
for ax, ang_deg, title in [(axes[0], 10, "10 deg: weight line inside the wheels, stable"), (axes[1], 20, "20 deg: weight line outside, tips over")]:
    th = math.radians(ang_deg)
    c, s = math.cos(th), math.sin(th)
    ax.fill([-1.2, 1.2, 1.2, -1.2], [-1.2 * math.tan(th), 1.2 * math.tan(th), -0.7, -0.7], color=L_GREY)
    ax.plot([-1.2, 1.2], [-1.2 * math.tan(th), 1.2 * math.tan(th)], color=BLACK, lw=2)
    W, H = 0.4, 0.7
    body = [(-W / 2, 0), (W / 2, 0), (W / 2, 0.85), (-W / 2, 0.85)]
    ax.add_patch(plt.Polygon([(c * x - s * y, s * x + c * y) for x, y in body], color=ORANGE, ec=BLACK, alpha=0.85))
    for wx in (-W / 2, W / 2):
        ax.plot([c * wx], [s * wx], "o", color=BLACK, ms=12)
    cx, cy = c * 0 - s * H, s * 0 + c * H
    ax.plot([cx], [cy], "o", color=RED, ms=12, zorder=6)
    ax.plot([cx, cx], [cy, -0.7], color=RED, ls="--", lw=2)
    ax.text(cx + 0.04, cy + 0.03, "centre of mass", fontsize=11, color=RED)
    ax.set_title(title, fontsize=12); ax.set_xlim(-1.0, 1.0); ax.set_ylim(-0.6, 1.1); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig03-side-slope.png")

# Figure 4: tipping angle against centre-of-mass height, compared with sliding
h = np.linspace(0.05, 1.2, 300)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(h, np.degrees(np.arctan(0.20 / h)), color=RED, lw=3, label="tips over: atan(half-track / height), half-track 0.20 m")
for mu, col in [(0.6, BLUE), (0.3, GREEN)]:
    ax.axhline(math.degrees(math.atan(mu)), color=col, ls="--", lw=2, label=f"slides: atan(mu) with mu = {mu}")
ax.plot([0.70], [math.degrees(math.atan(0.2 / 0.7))], "o", color=BLACK, ms=9)
ax.annotate("tray robot: 0.70 m high,\ntips at 15.9 deg", (0.70, 15.9), xytext=(0.78, 40), fontsize=11.5, arrowprops=dict(arrowstyle="-|>"))
ax.set_xlabel("height of the centre of mass (m)"); ax.set_ylabel("slope angle (deg)"); ax.set_ylim(0, 80); ax.grid(alpha=0.3)
ax.legend(loc="upper right", fontsize=10.5)
ax.set_title("a low robot slides before it tips; a tall robot tips before it slides", fontsize=12.5)
save(fig, "fig04-tip-or-slide.png")

# Figure 5: braking - the forces that tip a robot forwards
fig, ax = plt.subplots(figsize=(9, 6))
ax.fill_between([-1.2, 1.2], -0.1, 0, color=L_GREY)
ax.add_patch(plt.Rectangle((-0.35, 0.05), 0.6, 1.0, color=ORANGE, ec=BLACK, alpha=0.85))
ax.plot([-0.3, 0.18], [0.02, 0.02], "o", color=BLACK, ms=12)
cx, cy = 0.0, 0.7
ax.plot([cx], [cy], "o", color=RED, ms=12, zorder=6)
arrow(ax, cx, cy, cx, cy - 0.55, BLUE); ax.text(cx + 0.03, cy - 0.5, "weight m g", fontsize=11.5, color=BLUE)
arrow(ax, cx, cy, cx + 0.55, cy, RED); ax.text(cx + 0.58, cy - 0.02, "m a (the body\nwants to keep going)", fontsize=11.5, color=RED)
ax.plot([0.18], [0.0], "o", color=GREEN, ms=8)
ax.text(0.22, -0.2, "front wheel: the robot\ntips about this point", fontsize=11.5, color=GREEN)
ax.annotate("", xy=(0.18, 0.75 + 0.15), xytext=(cx, 0.75 + 0.15), arrowprops=dict(arrowstyle="<->", lw=1.5)); ax.text(0.09, 0.95, "d", ha="center", fontsize=12)
ax.annotate("", xy=(-0.5, cy), xytext=(-0.5, 0.0), arrowprops=dict(arrowstyle="<->", lw=1.5)); ax.text(-0.55, cy / 2, "h", ha="right", fontsize=12)
ax.text(-1.15, 1.25, "tips forward if  m a x h  >  m g x d,   so if  a > g x d / h", fontsize=12.5)
ax.set_xlim(-1.2, 1.5); ax.set_ylim(-0.35, 1.4); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig05-braking-tip.png")

# Figure 6: forklift braking limit against fork height
lift = np.linspace(0, 3.5, 200)
fig, ax = plt.subplots(figsize=(10, 5))
for load, col in [(150, GREEN), (300, BLUE), (400, RED)]:
    gm = 400 * G * 0.5 - load * G * 0.4
    a = gm / (400 * 0.45 + load * (lift + 0.3))
    ax.plot(lift, a, color=col, lw=3, label=f"{load} kg load")
ax.axhline(1.0, color=BLACK, ls="--", lw=1.5); ax.text(2.6, 1.07, "normal braking 1.0 m/s^2", fontsize=11)
ax.set_xlabel("fork height (m)"); ax.set_ylabel("braking that tips it forward (m/s^2)"); ax.set_ylim(0, 4.5); ax.grid(alpha=0.3)
ax.legend(loc="upper right", fontsize=11)
ax.set_title("the higher and heavier the load, the gentler the forklift must brake", fontsize=12.5)
save(fig, "fig06-forklift.png")
print("saved 6 figures")
