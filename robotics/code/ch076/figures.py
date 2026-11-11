# Figures for Chapter 76 - Power in circuits (P = V x I) and heat.
# Run:  python figures.py      (saves PNG files in ../../images/ch076/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch076")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Figure 1: power as the area of a rectangle V x I, on the I-V line of a resistor
fig, ax = plt.subplots(figsize=(10, 5))
V = np.linspace(0, 10, 50)
ax.plot(V, V / 4.8, color=BLUE, lw=2.5, label="Rover's stalled motor: 4.8 ohms")
for v, col, lab in [(7.2, ORANGE, "7.2 V x 1.5 A = 10.8 W"), (3.6, GREEN, "3.6 V x 0.75 A = 2.7 W")]:
    i = v / 4.8
    ax.add_patch(plt.Rectangle((0, 0), v, i, color=col, alpha=0.35))
    ax.plot(v, i, "o", color=BLACK, ms=8); ax.text(v + 0.15, i + 0.04, lab, fontsize=10.5)
ax.set_xlabel("voltage across the motor (V)"); ax.set_ylabel("current through it (A)"); ax.grid(alpha=0.3)
ax.set_xlim(0, 10); ax.set_ylim(0, 2.1); ax.legend(loc="upper left", fontsize=11)
ax.set_title("power = the area of the rectangle V x I: half the voltage gives a quarter of the power", fontsize=11.5)
save(fig, "fig01-power-rectangle.png")

# Figure 2: heat per metre against current for several wire sizes
fig, ax = plt.subplots(figsize=(10, 5))
I = np.linspace(0, 50, 200)
for a, col in [(0.5, RED), (1.0, ORANGE), (2.0, GREEN), (4.0, BLUE)]:
    ax.plot(I, I ** 2 * 1.68e-8 / (a * 1e-6), color=col, lw=2.5, label=f"{a} mm2")
ax.axvline(40, color=GREY, ls="--"); ax.text(40.5, 60, "drone at 40 A", fontsize=10.5)
for a, y in [(1.0, 26.9), (4.0, 6.7)]:
    ax.plot(40, y, "o", color=BLACK, ms=7); ax.text(41, y + 1.5, f"{y} W/m", fontsize=10.5)
ax.set_xlabel("current (A)"); ax.set_ylabel("heat in each metre of wire (W)"); ax.grid(alpha=0.3)
ax.set_ylim(0, 80); ax.legend(title="wire area", fontsize=10.5)
ax.set_title("heat grows with the current SQUARED: double the amps, four times the heat", fontsize=11.5)
save(fig, "fig02-wire-heat.png")

# Figure 3: the heat ladder - like voltages, temperature rises add up along the path to the air
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.5, 12.5); ax.set_ylim(-1.6, 4.2)
boxes = [("chip\n(junction)", RED), ("case", ORANGE), ("heat sink", GREEN), ("air", L_BLUE)]
for k, (name, col) in enumerate(boxes):
    ax.add_patch(plt.Rectangle((k * 3.2, 1.0), 2.2, 2.0, color=col, ec=BLACK))
    ax.text(k * 3.2 + 1.1, 2.0, name, ha="center", va="center", fontsize=11)
for k, (theta, p) in enumerate([("5 C/W", 2.25), ("2 C/W", 2.25), ("18 C/W", 2.25)]):
    ax.annotate("", xy=((k + 1) * 3.2, 2.0), xytext=(k * 3.2 + 2.2, 2.0), arrowprops=dict(arrowstyle="-|>", lw=2.5, color=BLACK))
    ax.text(k * 3.2 + 2.7, 2.35, theta, ha="center", fontsize=10.5)
    ax.text(k * 3.2 + 2.7, 1.5, f"{p} W", ha="center", fontsize=10, color=RED)
temps = [25 + 2.25 * 25, 25 + 2.25 * 20, 25 + 2.25 * 18, 25]
for k, t in enumerate(temps):
    ax.text(k * 3.2 + 1.1, 0.4, f"{t:.0f} C", ha="center", fontsize=11.5, fontweight="bold")
ax.text(6, 3.7, "2.25 W of heat flows out through each stage; each stage adds its own temperature rise (W x C/W)", ha="center", fontsize=10.5)
ax.text(6, -0.6, "total 5 + 2 + 18 = 25 C/W, so the chip sits 2.25 x 25 = 56 C above the air: the same adding-up as voltages in series",
        ha="center", fontsize=10.5)
save(fig, "fig03-heat-ladder.png")

# Figure 4: resistor power ratings
fig, ax = plt.subplots(figsize=(10, 4.2))
ratings = [("1/8 W", 0.125), ("1/4 W", 0.25), ("1/2 W", 0.5), ("1 W", 1.0), ("2 W", 2.0), ("5 W", 5.0)]
ax.bar(range(6), [r for _, r in ratings], color=[GREY, ORANGE, GREEN, BLUE, BLUE, BLUE], edgecolor=BLACK)
ax.axhline(0.225, color=RED, ls="--", lw=2); ax.text(1.0, 0.75, "the 0.1 ohm shunt at stall: 0.225 W", color=RED, fontsize=10.5, ha="center")
ax.axhline(0.0, color=BLACK, lw=0.5)
ax.set_xticks(range(6)); ax.set_xticklabels([n for n, _ in ratings]); ax.set_ylabel("rated power (W)")
ax.set_ylim(0, 5.5); ax.grid(alpha=0.3, axis="y")
ax.set_title("resistor sizes: the 1/4 W kind is barely enough for the shunt; use 1/2 W or more", fontsize=11.5)
save(fig, "fig04-resistor-ratings.png")

# Figure 5: the motor winding heating up (exponential approach) with the 100 C limit
fig, ax = plt.subplots(figsize=(10, 5))
t = np.linspace(0, 40 * 60, 500)
watts, theta, C, room = 20 ** 2 * 0.3, 1.5, 450.0, 20.0
steady = room + watts * theta; tau = C * theta
T = steady - (steady - room) * np.exp(-t / tau)
ax.plot(t / 60, T, color=BLUE, lw=2.5, label="winding temperature")
ax.axhline(100, color=RED, ls="--", lw=2, label="insulation limit 100 C")
ax.axhline(steady, color=GREY, ls=":", lw=2, label=f"would settle at {steady:.0f} C")
t_hit = -tau * math.log(1 - 80 / (steady - room))
ax.plot(t_hit / 60, 100, "o", color=BLACK, ms=8); ax.text(t_hit / 60 + 0.5, 92, f"{t_hit / 60:.1f} min", fontsize=11)
ax.set_xlabel("time holding the pose (min)"); ax.set_ylabel("temperature (C)"); ax.grid(alpha=0.3)
ax.legend(loc="lower right", fontsize=10.5)
ax.set_title("120 W of I^2 R heat in a leg motor: the same curve as Chapter 52, going up", fontsize=11.5)
save(fig, "fig05-motor-heating.png")

# Figure 6: Rover's motor driver temperature during a stall, bare and with a heat sink
fig, ax = plt.subplots(figsize=(10, 5))
for theta, col, lab in [(60.0, RED, "no heat sink"), (25.0, GREEN, "small heat sink")]:
    temp, tt, temps, times = 25.0, 0.0, [], []
    while tt < 300:
        temps.append(temp); times.append(tt)
        temp = temp + (2.25 - (temp - 25.0) / theta) / 1.5 * 0.1
        tt += 0.1
    ax.plot(times, temps, color=col, lw=2.5, label=lab)
ax.axhline(150, color=BLACK, ls="--", lw=1.5); ax.text(150, 154, "chip limit 150 C", fontsize=10.5)
ax.set_xlabel("time with both motors stalled (s)"); ax.set_ylabel("chip temperature (C)"); ax.grid(alpha=0.3)
ax.set_ylim(0, 180); ax.legend(loc="lower right", fontsize=11)
ax.set_title("Rover's driver at 2.25 W: bare, it passes 150 C after about 4 minutes", fontsize=11.5)
save(fig, "fig06-driver-stall.png")
print("saved 6 figures")
