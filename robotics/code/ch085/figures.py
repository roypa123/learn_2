# Figures for Chapter 85 - Inductors and coils (why motors make voltage spikes).
# Run:  python figures.py      (saves PNG files in ../../images/ch085/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch085")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Figure 1: magnetic field around a wire and through a coil
fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
ax = axes[0]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-3, 3); ax.set_ylim(-3, 3)
ax.add_patch(plt.Circle((0, 0), 0.25, color=ORANGE, ec=BLACK)); ax.text(0, 0, "x", ha="center", va="center", fontsize=12, fontweight="bold")
for r in [0.8, 1.4, 2.0, 2.6]:
    ax.add_patch(plt.Circle((0, 0), r, fill=False, ec=BLUE, lw=1.5))
    ax.annotate("", xy=(r * math.cos(1.0), r * math.sin(1.0)), xytext=(r * math.cos(1.15), r * math.sin(1.15)), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.5))
ax.set_title("current into the page: circles of magnetic field\n(weaker further away)", fontsize=11)
ax = axes[1]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-4, 4); ax.set_ylim(-3, 3)
for k in range(7):
    x = -2.1 + k * 0.7
    ax.add_patch(matplotlib.patches.Ellipse((x, 0), 0.35, 2.0, fill=False, ec=ORANGE, lw=3))
for y in [-0.4, 0, 0.4]:
    ax.annotate("", xy=(3.6, y), xytext=(-3.6, y), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2))
for sgn in [1, -1]:
    ax.add_patch(matplotlib.patches.Arc((0, sgn * 0.9), 7.6, 3.4, theta1=0 if sgn > 0 else 180, theta2=180 if sgn > 0 else 360, color=BLUE, lw=1.5, ls="--"))
ax.text(-3.4, 0.7, "S", fontsize=14, fontweight="bold"); ax.text(3.2, 0.7, "N", fontsize=14, fontweight="bold")
ax.set_title("a coil: the circles add up into a strong field\nthrough the middle, like a bar magnet", fontsize=11)
save(fig, "fig01-field.png")

# Figure 2: current rising in a coil
fig, ax = plt.subplots(figsize=(10, 4.6))
t = np.linspace(0, 12, 300)
tau = 0.15 / 70 * 1000
ax.plot(t, 5 / 70 * (1 - np.exp(-t / tau)) * 1000, color=BLUE, lw=2.5, label="relay coil current (L = 0.15 H, R = 70 ohm)")
ax.axhline(71.4, color=BLACK, ls="--", lw=1.5); ax.text(11.8, 73, "final 71.4 mA = 5 V / 70 ohm", ha="right", fontsize=10.5)
ax.axhline(50, color=GREEN, ls=":", lw=2); ax.text(11.8, 45, "relay pulls in at about 50 mA", ha="right", fontsize=10.5, color=GREEN)
tp = -tau * math.log(1 - 50 / 71.4); ax.plot(tp, 50, "o", color=BLACK, ms=8); ax.text(tp + 0.25, 44, f"{tp:.1f} ms", fontsize=10.5)
ax.axvline(tau, color=GREY, ls=":"); ax.text(tau + 0.1, 5, f"L/R = {tau:.2f} ms", fontsize=10.5)
ax.set_xlabel("time after switch-on (ms)"); ax.set_ylabel("current (mA)"); ax.grid(alpha=0.3); ax.set_ylim(0, 80); ax.legend(loc="lower right", fontsize=10)
ax.set_title("a coil's current cannot jump: it rises with time constant L / R", fontsize=11.5)
save(fig, "fig02-rl-rise.png")

# Figure 3: the switch-off spike with different escape paths
fig, ax = plt.subplots(figsize=(10, 4.8))
names = ["nothing\n(1 us switch-off)", "10 kohm\nacross the coil", "1 kohm", "100 ohm", "diode\n(Chapter 86)"]
I0 = 5 / 70
vals = [0.15 * I0 / 1e-6, 5 + I0 * 10000, 5 + I0 * 1000, 5 + I0 * 100, 5.7]
ax.bar(range(5), vals, color=[RED, ORANGE, ORANGE, GREEN, GREEN], edgecolor=BLACK); ax.set_yscale("log")
for k, v in enumerate(vals):
    ax.text(k, v * 1.3, f"{v:,.0f} V" if v >= 10 else f"{v:.1f} V", ha="center", fontsize=11)
ax.axhline(40, color=BLACK, ls="--"); ax.text(4.45, 46, "a small transistor's limit: about 40 V", ha="right", fontsize=10.5)
ax.set_xticks(range(5)); ax.set_xticklabels(names, fontsize=10); ax.set_ylabel("voltage across the switch (V, log scale)")
ax.set_yticks([1, 10, 100, 1000, 10000]); ax.set_yticklabels(["1", "10", "100", "1,000", "10,000"])
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter()); ax.set_ylim(1, 1e5); ax.grid(alpha=0.3, axis="y")
ax.set_title("switching off a 71 mA relay coil: give the current somewhere to go", fontsize=11.5)
save(fig, "fig03-spike.png")

# Figure 4: motor current against speed
fig, ax = plt.subplots(figsize=(10, 4.6))
K = (7.2 - 0.1 * 4.8) / (12000 * 2 * math.pi / 60)
rpm = np.linspace(0, 18000, 200)
back = K * rpm * 2 * math.pi / 60
cur = (7.2 - back) / 4.8
ax.plot(rpm, cur, color=BLUE, lw=2.5, label="current = (7.2 V - back voltage) / 4.8 ohm")
ax.axhline(0, color=BLACK, lw=1); ax.fill_between(rpm, cur, 0, where=cur < 0, color="#F5C6B0")
ax.plot(0, 1.5, "o", color=RED, ms=9); ax.text(300, 1.52, "stalled: 1.5 A", fontsize=10.5)
ax.plot(12000, 0.1, "o", color=GREEN, ms=9); ax.text(12200, 0.17, "free speed: 0.1 A", fontsize=10.5)
ax.text(15800, 0.35, "pushed faster:\ncurrent flows back\n(a generator)", ha="center", fontsize=10.5, color=RED)
ax.set_xlabel("motor speed (rpm)"); ax.set_ylabel("current (A)"); ax.grid(alpha=0.3); ax.legend(loc="upper right", fontsize=10.5)
ax.set_title("Rover's motor: the faster it spins, the more its back voltage cuts the current", fontsize=11.5)
save(fig, "fig04-motor-current.png")

# Figure 5: back voltage against speed, compared with the battery
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.plot(rpm, back, color=ORANGE, lw=2.5, label="back voltage made by the motor")
ax.axhline(7.2, color=BLACK, ls="--", lw=1.5, label="battery 7.2 V")
ax.axvline(12000, color=GREY, ls=":")
ax.set_xlabel("motor speed (rpm)"); ax.set_ylabel("volts"); ax.grid(alpha=0.3); ax.legend(loc="upper left", fontsize=10.5)
ax.set_title("the back voltage grows in a straight line with speed: 0.56 mV per rpm", fontsize=11.5)
save(fig, "fig05-back-voltage.png")

# Figure 6: a relay
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1, 11); ax.set_ylim(-1.2, 6)
for k in range(8):
    ax.add_patch(matplotlib.patches.Ellipse((1.0 + k * 0.35, 2.0), 0.3, 1.8, fill=False, ec=ORANGE, lw=2.5))
ax.add_patch(plt.Rectangle((0.7, 1.75), 3.0, 0.5, color=GREY, alpha=0.6))
ax.text(2.2, 0.1, "coil (electromagnet)\n5 V, 70 ohm", ha="center", fontsize=10.5)
ax.plot([0.5, 4.0], [3.3, 3.6], color=BLACK, lw=5); ax.plot(0.5, 3.3, "o", color=BLACK, ms=8)
ax.text(0.2, 3.9, "hinged iron armature,\npulled down by the coil", fontsize=10)
ax.plot([4.0, 6.0], [3.6, 3.6], color=GREY, lw=3); ax.plot(6.2, 3.6, "s", color=ORANGE, ms=10)
ax.plot([6.2, 9.0], [4.4, 4.4], color=BLACK, lw=2); ax.plot([6.2, 9.0], [2.8, 2.8], color=BLACK, lw=2)
ax.plot(6.2, 4.4, "o", color=BLACK, ms=7); ax.plot(6.2, 2.8, "o", color=BLACK, ms=7)
ax.text(9.2, 4.4, "NC contact", va="center", fontsize=10.5); ax.text(9.2, 2.8, "NO contact", va="center", fontsize=10.5)
ax.text(7.6, 3.5, "moving contact (COM)", fontsize=10, ha="center", va="center")
ax.text(5.0, 5.4, "a small current in the coil switches a big, separate circuit", ha="center", fontsize=11)
save(fig, "fig06-relay.png")
print("saved 6 figures")
