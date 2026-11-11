# Figures for Chapter 67 - Work, energy and power.
# Run:  python figures.py      (saves PNG files in ../../images/ch067/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch067")
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


# Figure 1: work = force x distance, and the angle
fig, axes = plt.subplots(1, 2, figsize=(13, 4.2))
for ax, ang, title in [(axes[0], 0, "force along the motion: W = F d"), (axes[1], 40, "force at an angle: W = F d cos(angle)")]:
    ax.fill_between([-0.5, 5.5], -0.3, 0, color=L_GREY)
    for x, a in [(0, 0.35), (4, 1.0)]:
        ax.add_patch(plt.Rectangle((x, 0), 0.9, 0.7, color=ORANGE, ec=BLACK, alpha=a))
    th = math.radians(ang)
    arrow(ax, 0.9, 0.35, 0.9 + 1.4 * math.cos(th), 0.35 + 1.4 * math.sin(th), RED)
    ax.text(0.95 + 1.4 * math.cos(th), 0.45 + 1.4 * math.sin(th), "F", color=RED, fontsize=13)
    if ang:
        arrow(ax, 0.9, 0.35, 0.9 + 1.4 * math.cos(th), 0.35, GREEN, 2)
        ax.text(1.2, 0.05, "F cos(angle)", color=GREEN, fontsize=11)
    ax.annotate("", xy=(4.45, -0.15), xytext=(0.45, -0.15), arrowprops=dict(arrowstyle="<->", lw=1.5))
    ax.text(2.45, -0.5, "distance d", ha="center", fontsize=12)
    ax.set_title(title, fontsize=12.5); ax.set_xlim(-0.5, 5.5); ax.set_ylim(-0.7, 1.6); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig01-work.png")

# Figure 2: kinetic energy against speed
v = np.linspace(0, 3, 200)
fig, ax = plt.subplots(figsize=(10, 5))
for m, col in [(4, GREEN), (25, BLUE), (60, RED)]:
    ax.plot(v, 0.5 * m * v ** 2, color=col, lw=3, label=f"{m} kg robot")
for vv in [1, 2]:
    ax.plot([vv], [0.5 * 25 * vv ** 2], "o", color=BLUE, ms=9)
ax.annotate("1 m/s: 12.5 J", (1, 12.5), xytext=(0.3, 60), fontsize=11.5, arrowprops=dict(arrowstyle="-|>"))
ax.annotate("2 m/s: 50 J\n(four times as much)", (2, 50), xytext=(1.2, 110), fontsize=11.5, arrowprops=dict(arrowstyle="-|>"))
ax.set_xlabel("speed (m/s)"); ax.set_ylabel("kinetic energy (J)"); ax.set_ylim(0, 280); ax.grid(alpha=0.3)
ax.legend(loc="upper left", fontsize=11)
ax.set_title("kinetic energy = 1/2 m v^2: double the speed, four times the energy", fontsize=12.5)
save(fig, "fig02-kinetic-energy.png")

# Figure 3: energy changing form - a cart rolling down a ramp and up the other side
h0 = 0.8
x = np.linspace(0, 6, 400)
y = np.where(x < 2, h0 * (1 - x / 2), np.where(x < 4, 0, h0 * (x - 4) / 2))
fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 7), gridspec_kw={"height_ratios": [1, 1.3]})
a1.fill_between(x, -0.05, y, color=L_GREY); a1.plot(x, y, color=BLACK, lw=2)
pos = [0.0, 1.0, 3.0, 5.0, 6.0]
for k, xp in enumerate(pos):
    yp = np.interp(xp, x, y)
    a1.add_patch(plt.Circle((xp, yp + 0.12), 0.1, color=ORANGE, ec=BLACK, zorder=5))
    a1.text(xp, yp + 0.3, "ABCDE"[k], ha="center", fontsize=12)
a1.set_xlim(-0.3, 6.3); a1.set_ylim(-0.1, 1.2); a1.set_aspect("equal"); a1.axis("off")
m = 2.0
pe = [m * G * np.interp(xp, x, y) for xp in pos]
total = m * G * h0
ke = [total - p for p in pe]
idx = np.arange(5)
a2.bar(idx - 0.18, pe, 0.36, color=BLUE, label="potential energy m g h")
a2.bar(idx + 0.18, ke, 0.36, color=RED, label="kinetic energy 1/2 m v^2")
a2.axhline(total, color=BLACK, ls="--", lw=1.5); a2.text(4.45, total + 0.4, f"total {total:.1f} J", ha="right", fontsize=11.5)
a2.set_xticks(idx); a2.set_xticklabels(list("ABCDE")); a2.set_ylabel("energy (J)"); a2.set_ylim(0, 21)
a2.legend(loc="upper center", fontsize=11, ncol=2); a2.grid(axis="y", alpha=0.3)
a2.set_title("a 2 kg cart with no friction: the total stays 15.7 J", fontsize=12)
save(fig, "fig03-energy-forms.png")

# Figure 4: power during a trip
t = np.linspace(0, 20, 2000)
m, crr, eff = 80, 0.015, 0.7
vel = np.where(t < 1, 1.5 * t, np.where(t < 8, 1.5, np.where(t < 14, 1.5, np.where(t < 15, 1.5 * (15 - t), 0))))
acc = np.where(t < 1, 1.5, np.where((t >= 14) & (t < 15), -1.5, 0))
slope = np.where((t >= 8) & (t < 14), math.sin(math.atan(0.05)), 0)
force = m * acc + crr * m * G * (vel > 0) + m * G * slope
power = np.maximum(force * vel, 0) / eff
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(t, power, color=BLUE, lw=2.5)
ax.axvspan(0, 1, color=L_ORANGE, alpha=0.7); ax.text(1.3, 240, "speeding up: 282 W at the peak", fontsize=10.5)
ax.axvspan(8, 14, color=L_GREEN, alpha=0.7); ax.text(11, 260, "climbing a 5% ramp", ha="center", fontsize=11)
ax.text(4.5, 40, "steady on the flat:\nonly rolling resistance", ha="center", fontsize=11)
ax.axvspan(14, 15, color=L_GREY, alpha=0.8); ax.text(16.5, 120, "braking: no power\nneeded (or energy\ngot back, Application 3)", fontsize=10.5)
ax.set_xlabel("time (s)"); ax.set_ylabel("power from the battery (W)"); ax.set_ylim(0, 300); ax.grid(alpha=0.3)
ax.set_title("an 80 kg robot: power = force x speed / efficiency", fontsize=12.5)
save(fig, "fig04-power-trip.png")

# Figure 5: drone flight time against battery size
wh = np.linspace(20, 150, 200)
fig, ax = plt.subplots(figsize=(10, 5))
for mass0, col, lab in [(1.6, BLUE, "drone alone"), (2.1, RED, "with a 0.5 kg parcel")]:
    batt_mass = wh / 150                              # about 150 Wh per kg of LiPo
    total_mass = mass0 - 74 / 150 + batt_mass
    power = 180 * (total_mass / 1.6) ** 1.5 + 6
    ax.plot(wh, wh * 0.8 * 60 / power, color=col, lw=3, label=lab)
ax.plot([74], [19.1], "o", color=BLUE, ms=9); ax.text(76, 18.0, "74 Wh: 19.1 min", fontsize=11.5)
ax.set_xlabel("battery size (Wh)"); ax.set_ylabel("hover time (minutes)"); ax.grid(alpha=0.3)
ax.legend(loc="lower right", fontsize=11)
ax.set_title("bigger batteries help less and less: they also add weight", fontsize=12.5)
save(fig, "fig05-drone-battery.png")

# Figure 6: energy budget of the warehouse robot
names = ["driving", "speeding up", "lifting", "electronics"]
vals = [121.1, 34.3, 21.8, 200.0]
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.barh(names, vals, color=[BLUE, ORANGE, GREEN, GREY], edgecolor=BLACK)
for i, v in enumerate(vals):
    ax.text(v + 3, i, f"{v:.0f} Wh ({v / sum(vals):.0%})", va="center", fontsize=11.5)
ax.invert_yaxis(); ax.set_xlabel("energy over an 8-hour shift (Wh)"); ax.set_xlim(0, 260); ax.grid(axis="x", alpha=0.3)
ax.set_title("total 377 Wh: the always-on electronics use more than the wheels", fontsize=12.5)
save(fig, "fig06-shift-budget.png")
print("saved 6 figures")
