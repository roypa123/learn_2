# Figures for Chapter 78 - Kirchhoff's laws.
# Run:  python figures.py      (saves PNG files in ../../images/ch078/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from nodal import solve

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch078")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def resistor(ax, x0, y0, x1, y1, label="", color=BLACK, lx=0.3):
    n = 6
    xs, ys = [x0], [y0]
    dx, dy = (x1 - x0), (y1 - y0)
    L = math.hypot(dx, dy); px, py = -dy / L, dx / L
    for k in range(1, 2 * n):
        f = k / (2 * n); s = 0.15 if k % 2 else -0.15
        xs.append(x0 + dx * f + px * s); ys.append(y0 + dy * f + py * s)
    xs.append(x1); ys.append(y1)
    ax.plot(xs, ys, color=color, lw=2)
    if label:
        if abs(dx) < 1e-9:
            ax.text(x0 + lx, (y0 + y1) / 2, label, ha="left", va="center", fontsize=10.5, color=RED)
        else:
            ax.text((x0 + x1) / 2, (y0 + y1) / 2 + 0.4, label, ha="center", va="center", fontsize=10.5, color=RED)


def battery(ax, x, y, label, lx=-0.5):
    ax.plot([x - 0.35, x + 0.35], [y + 0.12, y + 0.12], color=BLACK, lw=3)
    ax.plot([x - 0.18, x + 0.18], [y - 0.12, y - 0.12], color=BLACK, lw=3)
    ax.text(x + lx, y, label, ha="right", va="center", fontsize=10.5, color=ORANGE)


# Figure 1: the current law at a node
fig, ax = plt.subplots(figsize=(9, 5))
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-4, 4); ax.set_ylim(-2.8, 2.8)
ax.plot(0, 0, "o", color=BLACK, ms=14)
for ang, cur, inward in [(160, "2 A", True), (215, "1 A", True), (30, "1.5 A", False), (-40, "1 A", False), (90, "0.5 A", False)]:
    a = math.radians(ang); x, y = 2.4 * math.cos(a), 2.4 * math.sin(a)
    ax.plot([0, x], [0, y], color=BLACK, lw=2)
    xm, ym = 1.3 * math.cos(a), 1.3 * math.sin(a)
    if inward:
        ax.annotate("", xy=(0.5 * math.cos(a), 0.5 * math.sin(a)), xytext=(xm + 0.4 * math.cos(a), ym + 0.4 * math.sin(a)),
                    arrowprops=dict(arrowstyle="-|>", lw=2.5, color=GREEN))
    else:
        ax.annotate("", xy=(xm + 0.4 * math.cos(a), ym + 0.4 * math.sin(a)), xytext=(0.5 * math.cos(a), 0.5 * math.sin(a)),
                    arrowprops=dict(arrowstyle="-|>", lw=2.5, color=RED))
    ax.text(2.75 * math.cos(a), 2.75 * math.sin(a), cur, ha="center", va="center", fontsize=12, color=GREEN if inward else RED)
ax.text(0, -2.6, "in: 2 + 1 = 3 A      out: 1.5 + 1 + 0.5 = 3 A", ha="center", fontsize=12)
save(fig, "fig01-current-law.png")

# Figure 2: the voltage law - the 'height' round a loop comes back to where it started
fig, ax = plt.subplots(figsize=(10, 4.8))
pts = ["start\n(battery -)", "battery +", "after R1", "after R2", "after R4\n(back to start)"]
h = [0, 12, 12 - 4.444, 12 - 4.444 - 5.333, 0]
ax.plot(range(5), h, "o-", color=BLUE, lw=3, ms=9, mec=BLACK, mfc=ORANGE)
labels = ["+12.000 V (battery lifts)", "-4.444 V (R1)", "-5.333 V (R2)", "-2.222 V (R4)"]
for k, lab in enumerate(labels):
    ax.text(k + 0.6, (h[k] + h[k + 1]) / 2 + (0 if k == 0 else 1.0), lab, ha="left", fontsize=10.5, color=GREEN if k == 0 else RED)
ax.set_xticks(range(5)); ax.set_xticklabels(pts); ax.set_ylabel("volts above the start"); ax.grid(alpha=0.3, axis="y")
ax.set_ylim(-1, 14); ax.set_title("round any closed loop the rises and drops add up to zero: 12 - 4.444 - 5.333 - 2.222 = 0", fontsize=11.5)
save(fig, "fig02-voltage-law.png")

# Figure 3: the charging dock circuit
fig, ax = plt.subplots(figsize=(11, 4.8))
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.5, 11); ax.set_ylim(-1.4, 4.3)
ax.plot([0, 9], [3.5, 3.5], color=BLACK, lw=2); ax.plot([0, 9], [-0.5, -0.5], color=BLACK, lw=2)
for x in [0, 4.5, 9]:
    ax.plot(x, 3.5, "o", color=BLACK, ms=6); ax.plot(x, -0.5, "o", color=BLACK, ms=6)
# charger branch
resistor(ax, 0, 3.5, 0, 2.0, "0.5 ohm\n(wires, contacts)", lx=0.3); ax.plot([0, 0], [2.0, 1.6], color=BLACK, lw=2)
battery(ax, 0, 1.45, "dock charger\n8.4 V"); ax.plot([0, 0], [1.3, -0.5], color=BLACK, lw=2)
# battery branch
resistor(ax, 4.5, 3.5, 4.5, 2.0, "0.15 ohm\n(inside)", lx=0.3); ax.plot([4.5, 4.5], [2.0, 1.6], color=BLACK, lw=2)
battery(ax, 4.5, 1.45, "Rover battery\n7.2 V"); ax.plot([4.5, 4.5], [1.3, -0.5], color=BLACK, lw=2)
# load
resistor(ax, 9, 3.5, 9, -0.5, "Rover's\nelectronics\n13.6 ohm", lx=0.3)
ax.text(4.5, 3.95, "rail: 7.414 V", ha="center", fontsize=11.5, color=BLUE)
ax.annotate("", xy=(2.2, 3.75), xytext=(0.6, 3.75), arrowprops=dict(arrowstyle="-|>", lw=2, color=GREEN)); ax.text(1.4, 4.0, "1.972 A", ha="center", color=GREEN, fontsize=10.5)
ax.annotate("", xy=(4.15, 2.6), xytext=(4.15, 3.3), arrowprops=dict(arrowstyle="-|>", lw=2, color=GREEN)); ax.text(4.0, 2.95, "1.427 A\ninto the battery", color=GREEN, fontsize=10, ha="right", va="center")
ax.annotate("", xy=(8.5, 3.75), xytext=(6.9, 3.75), arrowprops=dict(arrowstyle="-|>", lw=2, color=GREEN)); ax.text(7.7, 4.0, "0.545 A", ha="center", color=GREEN, fontsize=10.5)
ax.text(4.5, -1.1, "one node (the rail): 1.972 A in = 1.427 A + 0.545 A out", ha="center", fontsize=11)
save(fig, "fig03-dock.png")

# Figure 4: charging current as the battery fills
fig, ax = plt.subplots(figsize=(10, 4.8))
bv = np.linspace(6.4, 8.4, 100)
cur = []
for b in bv:
    rail = solve(1, [(1, 0, 13.6)], [(1, 0, 8.4, 0.5), (1, 0, b, 0.15)])[1]
    cur.append((rail - b) / 0.15)
ax.plot(bv, cur, color=BLUE, lw=2.5)
ax.axhline(0, color=BLACK, lw=1)
ax.fill_between(bv, cur, 0, where=np.array(cur) < 0, color="#F5C6B0")
b0 = bv[np.argmin(np.abs(cur))]
ax.plot(b0, 0, "o", color=BLACK, ms=8); ax.text(b0 - 0.08, -0.3, f"stops charging at {b0:.2f} V", ha="right", fontsize=10.5)
ax.text(8.25, -0.35, "battery\nhelps the\ncharger", ha="center", fontsize=10, color=RED)
ax.set_xlabel("battery voltage (V)"); ax.set_ylabel("current into the battery (A)"); ax.grid(alpha=0.3)
ax.set_title("a simple dock: the charging current falls as the battery fills, and stops before it is full", fontsize=11.5)
save(fig, "fig04-charging-current.png")

# Figure 5: the Wheatstone bridge and its output
fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), gridspec_kw=dict(width_ratios=[1, 1.2]))
ax = axes[0]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-2.2, 4.2); ax.set_ylim(-1.0, 5.0)
top, bot = (1, 4.3), (1, -0.3)
for (x0, y0, x1, y1, lab) in [(1, 4.3, -0.5, 2.0, "350"), (1, 4.3, 2.5, 2.0, "350"), (-0.5, 2.0, 1, -0.3, "gauge"), (2.5, 2.0, 1, -0.3, "350")]:
    resistor(ax, x0, y0, x1, y1, color=RED if lab == "gauge" else BLACK)
    ax.text((x0 + x1) / 2 + (-0.6 if x1 < x0 or x0 < 1 else 0.6), (y0 + y1) / 2, lab, ha="center", fontsize=10.5, color=RED)
ax.plot(-0.5, 2.0, "o", color=BLACK, ms=6); ax.plot(2.5, 2.0, "o", color=BLACK, ms=6)
ax.text(1, 4.65, "+5 V", ha="center", fontsize=11, color=ORANGE); ax.text(1, -0.75, "0 V", ha="center", fontsize=11)
ax.annotate("", xy=(2.3, 2.0), xytext=(-0.3, 2.0), arrowprops=dict(arrowstyle="<->", lw=1.5, color=BLUE)); ax.text(1, 2.25, "output", ha="center", color=BLUE, fontsize=10.5)
ax.set_title("the bridge", fontsize=11.5)
ax = axes[1]
micro = np.linspace(0, 2000, 50)
outs = []
for m in micro:
    g = 350 * (1 + 2 * m * 1e-6)
    v = solve(3, [(1, 2, 350), (2, 0, g), (1, 3, 350), (3, 0, 350)], [(1, 0, 5.0, 1e-9)])
    outs.append((v[2] - v[3]) * 1000)
ax.plot(micro, outs, color=BLUE, lw=2.5, label="bridge output")
ax.axhline(4.88, color=RED, ls="--", label="one Arduino ADC step (4.88 mV)")
ax.set_xlabel("strain (microstrain)"); ax.set_ylabel("output (mV)"); ax.grid(alpha=0.3); ax.legend(fontsize=10, loc="upper left")
ax.set_title("1.25 mV at 500 microstrain: it must be amplified", fontsize=11.5)
save(fig, "fig05-bridge.png")

# Figure 6: shared ground wire vs star ground
fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
for ax, star in zip(axes, [False, True]):
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.5, 10); ax.set_ylim(-2.4, 4.2)
    for x, y, lab, col in [(0, 2.5, "battery", ORANGE), (4.0, 3.0, "Arduino", BLUE), (8.0, 3.0, "sensor", GREEN), (8.0, 0.8, "motor\n3 A", RED)]:
        ax.add_patch(plt.Rectangle((x, y), 1.6, 1.0, color=col, alpha=0.35, ec=BLACK))
        ax.text(x + 0.8, y + 0.5, lab, ha="center", va="center", fontsize=10.5)
    if not star:
        ax.plot([0.8, 0.8, 8.8], [2.5, -0.8, -0.8], color=BLACK, lw=2.5)
        ax.plot([8.8, 8.8], [-0.8, 0.8], color=BLACK, lw=2.5)
        ax.plot([8.4, 8.4], [3.0, 1.9], color=BLACK, lw=1.5, ls=":")
        ax.plot([8.4, 9.9, 9.9, 8.8], [1.9, 1.9, -0.8, -0.8], color=BLACK, lw=1.5)
        ax.plot([4.8, 4.8], [3.0, -0.8], color=BLACK, lw=1.5)
        ax.text(6.8, -1.25, "shared wire: 3 A x 0.02 ohm = 60 mV", ha="center", fontsize=10.5, color=RED)
        ax.set_title("shared ground: the sensor's 0 V is lifted by 60 mV", fontsize=11.5)
    else:
        ax.plot(0.8, -0.8, "o", color=BLACK, ms=8)
        ax.plot([0.8, 0.8], [2.5, -0.8], color=BLACK, lw=2.5)
        ax.plot([0.8, 8.8, 8.8], [-0.8, -0.8, 0.8], color=BLACK, lw=2.5)
        ax.plot([0.8, 4.8, 4.8], [-0.5, -0.5, 3.0], color=BLUE, lw=1.5)
        ax.plot([4.8, 4.8], [2.6, 2.6], color=BLUE)
        ax.plot([5.6, 8.4, 8.4], [2.6, 2.6, 3.0], color=GREEN, lw=1.5)
        ax.plot([5.6, 5.6], [3.0, 2.6], color=GREEN, lw=1.5)
        ax.text(5.0, -1.8, "star: the motor current has its own wire; the sensor's ground\ngoes to the Arduino and carries almost no current", ha="center", fontsize=10)
        ax.set_title("star ground: no motor current in the sensor's ground", fontsize=11.5)
save(fig, "fig06-ground.png")
print("saved 6 figures")
