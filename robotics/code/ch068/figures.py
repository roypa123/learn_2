# Figures for Chapter 68 - Gears, pulleys and belts.
# Run:  python figures.py      (saves PNG files in ../../images/ch068/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch068")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def gear(ax, cx, cy, teeth, module, col, phase=0.0):
    r = module * teeth / 2
    pts = []
    for k in range(teeth):
        a0 = 2 * math.pi * k / teeth + phase
        for frac, rr in [(0.0, r - module), (0.15, r + module * 0.9), (0.35, r + module * 0.9), (0.5, r - module)]:
            a = a0 + frac * 2 * math.pi / teeth
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    ax.add_patch(plt.Polygon(pts, color=col, ec=BLACK, lw=1))
    ax.add_patch(plt.Circle((cx, cy), module * 1.2, color="white", ec=BLACK))
    return r


def arrow(ax, x0, y0, x1, y1, col, lw=3):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0), arrowprops=dict(arrowstyle="-|>", color=col, lw=lw, mutation_scale=18))


# Figure 1: a small gear driving a big gear
fig, ax = plt.subplots(figsize=(10, 6))
m = 0.1
r1 = gear(ax, 0, 0, 12, m, ORANGE, phase=0.0)
cx2 = r1 + 0.1 * 36 / 2
r2 = gear(ax, cx2, 0, 36, m, BLUE, phase=math.pi / 36)
ax.text(-0.4, -r1 - 0.9, "12 teeth (driving)\nfast, weak", ha="center", fontsize=11.5)
ax.text(cx2, -r2 - 0.45, "36 teeth (driven)\nslow, strong", ha="center", fontsize=11.5)
arrow(ax, r1, 1.0, r1, 0.1, RED)
ax.text(r1 - 0.25, 1.3, "the same tooth force F\nacts on both gears", fontsize=11, color=RED, ha="right")
for cx, rr, sign in [(0, r1, 1), (cx2, r2, -1)]:
    t = np.linspace(0.4, 1.4, 40)
    ax.plot(cx + (rr + 0.35) * np.cos(t), (rr + 0.35) * np.sin(t), color=BLACK, lw=1.5)
    end = 1.4 if sign > 0 else 0.4
    start = 1.3 if sign > 0 else 0.5
    ax.annotate("", xy=(cx + (rr + 0.35) * math.cos(end), (rr + 0.35) * math.sin(end)),
                xytext=(cx + (rr + 0.35) * math.cos(start), (rr + 0.35) * math.sin(start)), arrowprops=dict(arrowstyle="-|>", lw=1.5))
ax.text(-1.8, 2.3, "ratio 36 : 12 = 3 : 1\nspeed divided by 3, torque multiplied by 3\nthe two gears turn opposite ways", fontsize=12)
ax.set_xlim(-2.0, 5.0); ax.set_ylim(-2.6, 3.0); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig01-gear-pair.png")

# Figure 2: speed and torque through a three-stage gearbox
labels = ["motor", "stage 1\n(5:1)", "stage 2\n(3:1)", "stage 3\n(4:1)"]
rpm = [6000, 1200, 400, 100]
tq = [0.05, 0.2375, 0.6769, 2.5721]
pw = [31.42, 29.85, 28.35, 26.94]
fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
axes[0].bar(range(4), rpm, color=BLUE, edgecolor=BLACK); axes[0].set_title("speed (rpm)", fontsize=12.5)
axes[1].bar(range(4), tq, color=RED, edgecolor=BLACK); axes[1].set_title("torque (N m)", fontsize=12.5)
axes[2].bar(range(4), pw, color=GREEN, edgecolor=BLACK); axes[2].set_title("power (W): almost the same", fontsize=12.5)
axes[2].set_ylim(0, 36)
for ax, vals, fmt in [(axes[0], rpm, "{:.0f}"), (axes[1], tq, "{:.2f}"), (axes[2], pw, "{:.1f}")]:
    ax.set_xticks(range(4)); ax.set_xticklabels(labels, fontsize=9.5)
    for i, v in enumerate(vals):
        ax.text(i, v * 1.02 + (0.5 if ax is axes[2] else 0), fmt.format(v), ha="center", fontsize=10.5)
    ax.grid(axis="y", alpha=0.3)
save(fig, "fig02-gearbox-stages.png")

# Figure 3: some kinds of gears (schematic)
fig, axes = plt.subplots(1, 3, figsize=(15, 4.8))
ax = axes[0]
r = gear(ax, 0, 0.9, 12, 0.1, ORANGE)
xs = np.arange(-1.8, 1.9, 0.314)
for x in xs:
    ax.add_patch(plt.Polygon([(x, 0.0), (x + 0.08, 0.2), (x + 0.16, 0.2), (x + 0.24, 0.0)], color=BLUE, ec=BLACK))
ax.add_patch(plt.Rectangle((-1.8, -0.3), 3.7, 0.3, color=BLUE, ec=BLACK))
arrow(ax, 0.3, -0.6, 1.3, -0.6, BLACK, 2)
ax.set_title("rack and pinion:\nturning becomes straight motion", fontsize=12)
ax.set_xlim(-2, 2); ax.set_ylim(-0.9, 2.2); ax.set_aspect("equal"); ax.axis("off")
ax = axes[1]
gear(ax, 0, 0, 36, 0.06, L_GREY)
ax.add_patch(plt.Circle((0, 0), 0.86, color="white"))
gear(ax, 0, 0, 12, 0.06, ORANGE)
for k in range(3):
    a = 2 * math.pi * k / 3 + 0.5
    gear(ax, 0.72 * math.cos(a), 0.72 * math.sin(a), 12, 0.06, BLUE, phase=a)
ax.set_title("planetary: sun (orange), planets (blue)\nand ring (grey), compact and strong", fontsize=12)
ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4); ax.set_aspect("equal"); ax.axis("off")
ax = axes[2]
gear(ax, 0, 0.75, 30, 0.06, BLUE)
for k in range(7):
    y = -0.3
    x = -1.0 + k * 0.3
    ax.add_patch(plt.Polygon([(x, y - 0.15), (x + 0.15, y + 0.15), (x + 0.25, y + 0.15), (x + 0.1, y - 0.15)], color=ORANGE, ec=BLACK))
ax.add_patch(plt.Rectangle((-1.3, -0.33), 2.6, 0.06, color=GREY))
ax.set_title("worm and wheel: big ratio in one step,\nthe wheel cannot turn the worm back", fontsize=12)
ax.set_xlim(-1.5, 1.5); ax.set_ylim(-0.8, 1.9); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig03-gear-types.png")

# Figure 4: push against speed for several ratios
G = 9.81
v = np.linspace(0, 1.5, 300)
wf = 12000 * 2 * math.pi / 60
fig, ax = plt.subplots(figsize=(10, 5.5))
for N, col in [(10, GREY), (20, ORANGE), (30, BLUE), (50, GREEN), (80, RED)]:
    mt = 0.010 * np.clip(1 - v / 0.033 * N / wf, 0, None)
    ax.plot(v, 2 * mt * N * 0.8 / 0.033, color=col, lw=3, label=f"{N}:1")
ramp = 4 * G * math.sin(math.atan(0.2)) + 0.015 * 4 * G
ax.axhline(ramp, color=BLACK, ls="--", lw=1.5); ax.text(1.0, ramp + 0.4, "20% ramp needs 8.28 N", fontsize=11.5)
ax.plot([0.2], [ramp], "o", color=BLACK, ms=8)
ax.axvline(0.6, color=BLACK, ls=":", lw=1.5); ax.text(0.62, 22, "flat: need\n0.6 m/s", fontsize=11.5)
ax.set_xlabel("robot speed (m/s)"); ax.set_ylabel("push from both wheels (N)"); ax.set_ylim(0, 26); ax.set_xlim(0, 1.5)
ax.grid(alpha=0.3); ax.legend(title="gear ratio", loc="upper right", fontsize=11)
ax.set_title("each ratio's line: a high ratio pushes hard but is slow", fontsize=12.5)
save(fig, "fig04-choose-ratio.png")

# Figure 5: a belt and two pulleys, and a pulley block
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
ax = axes[0]
for cx, rr, col, lab in [(0, 0.4, ORANGE, "20 teeth\non the motor"), (3, 1.0, BLUE, "50 teeth")]:
    ax.add_patch(plt.Circle((cx, 0), rr, color=col, ec=BLACK))
    ax.add_patch(plt.Circle((cx, 0), 0.08, color="white", ec=BLACK))
    ax.text(cx, -rr - 0.45, lab, ha="center", fontsize=11.5)
ang = math.asin((1.0 - 0.4) / 3)
for s in (1, -1):
    ax.plot([0 - 0.4 * math.sin(ang), 3 - 1.0 * math.sin(ang)], [s * 0.4 * math.cos(ang), s * 1.0 * math.cos(ang)], color=BLACK, lw=3)
ax.text(1.5, 1.05, "toothed belt", ha="center", fontsize=11.5)
ax.text(-0.6, 1.9, "ratio 50 : 20 = 2.5 : 1", fontsize=12.5)
ax.set_xlim(-1.0, 4.4); ax.set_ylim(-1.8, 2.2); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("belt drive: same direction, ratio = teeth ratio", fontsize=12.5)
ax = axes[1]
ax.plot([-1.5, 1.5], [2.0, 2.0], color=BLACK, lw=4)
ax.add_patch(plt.Circle((0, 1.6), 0.3, color=GREY, ec=BLACK))
ax.add_patch(plt.Circle((0, 0.4), 0.3, color=GREY, ec=BLACK))
ax.plot([0, 0], [2.0, 1.6], color=BLACK, lw=2)
ax.plot([-0.3, -0.3], [1.6, 0.4], color=BLUE, lw=2); ax.plot([0.3, 0.3], [1.6, 0.4], color=BLUE, lw=2)
ax.plot([-0.3, -0.3, -0.9], [1.6, 1.6, -0.6], color=BLUE, lw=2)
ax.add_patch(plt.Rectangle((-0.35, -0.6), 0.7, 0.6, color=ORANGE, ec=BLACK)); ax.plot([0, 0], [0.1, 0.0], color=BLACK, lw=2)
ax.text(0, -0.35, "200 N", ha="center", fontsize=11.5)
arrow(ax, -0.9, -0.4, -0.9, -1.0, RED); ax.text(-1.0, -1.2, "pull 100 N", fontsize=11.5, color=RED, ha="right")
ax.text(0.45, 1.0, "2 rope sections hold\nthe load: each\ncarries 100 N", fontsize=11.5)
ax.set_xlim(-2, 2.5); ax.set_ylim(-1.6, 2.4); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("pulley block: half the pull, twice the rope", fontsize=12.5)
save(fig, "fig05-belt-pulley.png")

# Figure 6: reflected inertia and acceleration against gear ratio
N = np.linspace(2, 120, 400)
I_rotor = 1e-6
I_load = 2.0 * 0.033 ** 2              # half of Rover's 4 kg, as seen by one wheel: (m/2) r^2
tau = 0.010
alpha_load = tau * N / (I_load + I_rotor * N ** 2)
best = math.sqrt(I_load / I_rotor)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(N, alpha_load * 0.033, color=BLUE, lw=3)
ax.axvline(best, color=RED, ls="--", lw=2); ax.text(best + 3, 1.0, f"best ratio\nsqrt(I_load / I_rotor)\n= {best:.0f}:1", fontsize=11.5, color=RED)
ax.set_xlabel("gear ratio N"); ax.set_ylabel("Rover's best acceleration (m/s^2)"); ax.grid(alpha=0.3)
ax.set_title("too low: weak motor torque.  too high: the rotor's inertia x N^2 takes over", fontsize=12)
save(fig, "fig06-best-ratio.png")
print("saved 6 figures")
