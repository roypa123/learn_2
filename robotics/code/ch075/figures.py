# Figures for Chapter 75 - Ohm's law with many worked examples.
# Run:  python figures.py      (saves PNG files in ../../images/ch075/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch075")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Figure 1: I against V for three resistors - straight lines through the origin
fig, ax = plt.subplots(figsize=(10, 5))
V = np.linspace(0, 10, 50)
for r, col in [(5, RED), (10, ORANGE), (20, BLUE)]:
    ax.plot(V, V / r, color=col, lw=2.5, label=f"{r} ohms: I = V / {r}")
ax.plot([6, 6], [0, 6 / 10], color=GREY, ls="--"); ax.plot([0, 6], [0.6, 0.6], color=GREY, ls="--")
ax.plot(6, 0.6, "o", color=BLACK, ms=8); ax.text(6.15, 0.68, "6 V across 10 ohms: 0.6 A", fontsize=10.5)
ax.set_xlabel("voltage across the resistor (V)"); ax.set_ylabel("current through it (A)"); ax.grid(alpha=0.3)
ax.legend(loc="upper left", fontsize=11); ax.set_ylim(0, 2.1)
ax.set_title("a resistor: double the voltage, double the current (a straight line)", fontsize=12)
save(fig, "fig01-iv-lines.png")

# Figure 2: the Ohm's law triangle
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.5, 10.5); ax.set_ylim(-0.5, 4.2)
tri = plt.Polygon([(0, 0), (4, 0), (2, 3.6)], fill=True, color=L_GREY, ec=BLACK, lw=2)
ax.add_patch(tri); ax.plot([0.7, 3.3], [1.3, 1.3], color=BLACK, lw=2); ax.plot([2, 2], [0, 1.3], color=BLACK, lw=2)
ax.text(2, 2.1, "V", ha="center", va="center", fontsize=24, fontweight="bold", color=ORANGE)
ax.text(1.3, 0.6, "I", ha="center", va="center", fontsize=24, fontweight="bold", color=GREEN)
ax.text(2.7, 0.6, "R", ha="center", va="center", fontsize=24, fontweight="bold", color=RED)
ax.text(2, -0.4, "cover the one you want; what is left is the formula", ha="center", fontsize=10.5)
ax.text(5.0, 3.3, "cover V:   V = I x R      (volts = amps x ohms)", fontsize=12.5, color=ORANGE)
ax.text(5.0, 2.2, "cover I:   I = V / R      (amps = volts / ohms)", fontsize=12.5, color=GREEN)
ax.text(5.0, 1.1, "cover R:   R = V / I      (ohms = volts / amps)", fontsize=12.5, color=RED)
ax.text(5.0, 0.2, "one law, three ways to write it", fontsize=11.5)
save(fig, "fig02-triangle.png")

# Figure 3: voltage along the loop - the 'height' falls a little in each wire and a lot in the motor
fig, ax = plt.subplots(figsize=(10, 5))
I = 3.1; r_wire = 0.01008 * 0.5 * 1 / 1  # 0.3 m one way (half of the 0.6 m round trip)
r_wire = 1.68e-8 * 0.3 / 0.5e-6
v_wire = I * r_wire
points = ["battery +", "driver in", "driver out\n(motor +)", "motor -", "battery -"]
heights = [7.2, 7.2 - v_wire, 7.2 - v_wire, 7.2 - v_wire - (7.2 - 2 * v_wire), 0]
x = np.arange(5)
ax.step(x, heights, where="post", color=BLUE, lw=3)
ax.plot(x, heights, "o", color=ORANGE, mec=BLACK, ms=9, zorder=5)
for xi, h in zip(x, heights):
    ax.text(xi, h + 0.25, f"{h:.3f} V", ha="center", fontsize=10.5)
ax.annotate("", xy=(1.5, heights[1]), xytext=(1.5, 7.2), arrowprops=dict(arrowstyle="<->", color=RED, lw=1.5))
ax.text(1.6, 7.05, f"wire loses {v_wire * 1000:.0f} mV\n(3.1 A x 10 mohm)", fontsize=10, color=RED, va="top")
ax.annotate("", xy=(2.5, heights[3]), xytext=(2.5, heights[2]), arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.5))
ax.text(2.6, 3.6, f"the motor gets\n{heights[2] - heights[3]:.3f} V", fontsize=10.5, color=GREEN, va="center")
ax.set_xticks(x); ax.set_xticklabels(points); ax.set_ylabel("volts above ground"); ax.set_ylim(-0.5, 8.2); ax.grid(alpha=0.3, axis="y")
ax.set_title("Rover at 3.1 A: the 'height' falls a few millivolts in each wire and 7.1 V in the motor", fontsize=11.5)
save(fig, "fig03-voltage-drop.png")

# Figure 4: current against resistance (log-log), with the fuse line
fig, ax = plt.subplots(figsize=(10, 5))
R = np.logspace(-3, 2, 200)
ax.loglog(R, 7.2 / R, color=GREY, lw=2, ls="--", label="perfect battery: I = 7.2 / R")
ax.loglog(R, 7.2 / (R + 0.15), color=BLUE, lw=2.5, label="real battery (0.15 ohm inside)")
ax.axhline(4.0, color=RED, lw=2, ls=":", label="Rover's 4 A fuse")
ax.axhline(48, color=ORANGE, lw=1.5, ls="-.", label="limit set by the battery: 48 A")
for r, lab in [(3, "motor 3 ohms"), (0.05, "a stray wire\n0.05 ohms")]:
    i = 7.2 / (r + 0.15)
    ax.plot(r, i, "o", color=BLACK, ms=8); ax.text(r * 1.3, i * 1.3, f"{lab}: {i:.1f} A", fontsize=10.5)
ax.set_xlabel("resistance of the load (ohms)"); ax.set_ylabel("current (A)")
ax.set_xticks([0.001, 0.01, 0.1, 1, 10, 100]); ax.set_xticklabels(["0.001", "0.01", "0.1", "1", "10", "100"])
ax.set_yticks([0.1, 1, 10, 100, 1000]); ax.set_yticklabels(["0.1", "1", "10", "100", "1,000"])
ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter()); ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.grid(alpha=0.3, which="both"); ax.legend(loc="lower left", fontsize=10)
ax.set_title("smaller resistance, bigger current: a short circuit is the far left", fontsize=12)
save(fig, "fig04-short-circuit.png")

# Figure 5: ohmic and non-ohmic parts
fig, ax = plt.subplots(figsize=(10, 5))
V = np.linspace(0, 5, 200)
ax.plot(V, V / 10, color=BLUE, lw=2.5, label="10 ohm resistor: straight line (obeys Ohm's law)")
led = np.where(V > 1.8, (V - 1.8) / 2.0, 0.0) * np.exp(np.clip((V - 1.8) * 1.2, 0, 5)) / 6
led = np.clip(led, 0, 0.6)
ax.plot(V, led, color=RED, lw=2.5, label="LED: nothing until about 1.8 V, then a steep rise")
lamp = 0.5 * np.sqrt(V / 5)
ax.plot(V, lamp, color=ORANGE, lw=2.5, label="small lamp: bends over as the filament gets hot")
ax.set_xlabel("voltage across the part (V)"); ax.set_ylabel("current through it (A)"); ax.grid(alpha=0.3)
ax.set_ylim(0, 0.65); ax.legend(loc="upper left", fontsize=10.5)
ax.set_title("only the resistor is a straight line; for the others, R = V / I changes with V", fontsize=11.5)
save(fig, "fig05-ohmic-or-not.png")

# Figure 6: a shunt resistor: voltage at the shunt vs voltage lost
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
shunts = [0.01, 0.05, 0.1, 0.5, 1.0]
labels = [f"{r} ohm" for r in shunts]
axes[0].bar(range(5), [1.5 * r * 1000 for r in shunts], color=GREEN, edgecolor=BLACK)
axes[0].axhline(4.88, color=RED, ls="--"); axes[0].text(2.0, 7, "one ADC step: 4.9 mV", color=RED, fontsize=10.5)
axes[0].set_xticks(range(5)); axes[0].set_xticklabels(labels); axes[0].set_ylabel("millivolts at 1.5 A (stall)")
axes[0].set_yscale("log"); axes[0].set_yticks([1, 10, 100, 1000]); axes[0].set_yticklabels(["1", "10", "100", "1,000"])
axes[0].yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
axes[0].set_title("signal: how much voltage a stall makes", fontsize=11); axes[0].grid(alpha=0.3, axis="y", which="both")
axes[1].bar(range(5), [1.5 * r / 7.2 * 100 for r in shunts], color=RED, edgecolor=BLACK)
axes[1].axhline(5, color=BLACK, ls="--"); axes[1].text(0.0, 5.6, "keep under 5%", fontsize=10.5)
axes[1].set_xticks(range(5)); axes[1].set_xticklabels(labels); axes[1].set_ylabel("% of 7.2 V eaten at stall")
axes[1].set_title("cost: voltage taken from the motor", fontsize=11); axes[1].grid(alpha=0.3, axis="y")
fig.suptitle("choosing a current-sense (shunt) resistor: 0.1 ohm is the compromise", fontsize=12, y=1.02)
save(fig, "fig06-shunt.png")
print("saved 6 figures")
