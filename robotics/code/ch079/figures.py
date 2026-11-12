# Figures for Chapter 79 - Voltage dividers.
# Run:  python figures.py      (saves PNG files in ../../images/ch079/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch079")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def resistor(ax, x0, y0, x1, y1, color=BLACK):
    n = 6
    xs, ys = [x0], [y0]
    dx, dy = (x1 - x0), (y1 - y0)
    L = math.hypot(dx, dy); px, py = -dy / L, dx / L
    for k in range(1, 2 * n):
        f = k / (2 * n); s = 0.15 if k % 2 else -0.15
        xs.append(x0 + dx * f + px * s); ys.append(y0 + dy * f + py * s)
    xs.append(x1); ys.append(y1)
    ax.plot(xs, ys, color=color, lw=2)


# Figure 1: the divider, with its 'heights'
fig, axes = plt.subplots(1, 2, figsize=(11, 5), gridspec_kw=dict(width_ratios=[1, 1.1]))
ax = axes[0]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-2.5, 4.5); ax.set_ylim(-0.8, 6.6)
ax.plot([1, 1], [6.0, 5.2], color=BLACK, lw=2); resistor(ax, 1, 5.2, 1, 3.4); ax.plot([1, 1], [3.4, 2.6], color=BLACK, lw=2)
resistor(ax, 1, 2.6, 1, 0.8); ax.plot([1, 1], [0.8, 0.0], color=BLACK, lw=2); ax.plot([0.5, 1.5], [0, 0], color=BLACK, lw=3)
ax.plot(1, 3.0, "o", color=BLACK, ms=7); ax.plot([1, 3.0], [3.0, 3.0], color=BLUE, lw=2); ax.plot(3.0, 3.0, "o", color=BLUE, ms=7)
ax.text(1, 6.25, "Vin = 12 V", ha="center", fontsize=11.5, color=ORANGE)
ax.text(1.45, 4.3, "R1 = 2 kohm", fontsize=11, color=RED); ax.text(1.45, 1.7, "R2 = 1 kohm", fontsize=11, color=RED)
ax.text(3.2, 3.0, "Vout\n4 V", fontsize=11.5, color=BLUE, va="center")
ax.text(1, -0.5, "ground, 0 V", ha="center", fontsize=10.5)
ax.annotate("", xy=(-0.4, 0.8), xytext=(-0.4, 5.2), arrowprops=dict(arrowstyle="-|>", lw=2, color=GREEN)); ax.text(-0.6, 3.0, "I = 12 / 3000\n= 4 mA", ha="right", va="center", fontsize=10.5, color=GREEN)
ax = axes[1]
ax.bar([0], [12], width=0.5, color=L_GREY, edgecolor=BLACK); ax.bar([1], [8], bottom=4, width=0.5, color=L_ORANGE, edgecolor=BLACK); ax.bar([1], [4], width=0.5, color=L_BLUE, edgecolor=BLACK)
ax.text(0, 12.3, "12 V", ha="center"); ax.text(1, 8, "R1 drops\n8 V\n(2 of 3 parts)", ha="center", va="center", fontsize=10.5)
ax.text(1, 2, "R2 drops\n4 V\n(1 of 3)", ha="center", va="center", fontsize=10.5)
ax.set_xticks([0, 1]); ax.set_xticklabels(["supply", "the two\nresistors"]); ax.set_ylabel("volts"); ax.set_ylim(0, 13.5); ax.grid(alpha=0.3, axis="y")
ax.set_title("each resistor takes its share: R / (R1 + R2)", fontsize=11.5)
save(fig, "fig01-divider.png")

# Figure 2: loading - output against load resistance for three divider sizes
fig, ax = plt.subplots(figsize=(10, 5))
RL = np.logspace(2, 7, 300)
for r, col in [(1000, GREEN), (10000, BLUE), (100000, RED)]:
    rp = r * RL / (r + RL)
    ax.semilogx(RL, 5 * rp / (r + rp), color=col, lw=2.5, label=f"R1 = R2 = {r:,} ohm")
ax.axhline(2.5, color=BLACK, ls="--", lw=1.5, label="unloaded: 2.5 V")
ax.axvline(10000, color=GREY, ls=":"); ax.text(11000, 0.2, "a 10 kohm load", fontsize=10.5)
ax.set_xlabel("load resistance connected across R2 (ohm)"); ax.set_ylabel("divider output (V)"); ax.grid(alpha=0.3, which="both")
ax.set_xticks([100, 1000, 10000, 100000, 1000000, 10000000]); ax.set_xticklabels(["100", "1 k", "10 k", "100 k", "1 M", "10 M"])
ax.set_ylim(0, 2.8); ax.legend(loc="lower right", fontsize=10.5)
ax.set_title("a load pulls the output down unless it is much bigger than R1 || R2", fontsize=11.5)
save(fig, "fig02-loading.png")

# Figure 3: a potentiometer
fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
ax = axes[0]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.5, 4.5); ax.set_ylim(-0.8, 5.4)
ax.add_patch(plt.Rectangle((0.7, 0.6), 0.6, 4.0, color=L_GREY, ec=BLACK, lw=2))
ax.plot([1, 1], [4.6, 5.0], color=BLACK, lw=2); ax.plot([1, 1], [0.2, 0.6], color=BLACK, lw=2)
ax.text(1, 5.15, "5 V", ha="center", color=ORANGE); ax.text(1, -0.15, "0 V", ha="center")
ax.annotate("", xy=(1.35, 3.2), xytext=(2.6, 3.2), arrowprops=dict(arrowstyle="-|>", lw=2.5, color=BLUE))
ax.text(2.7, 3.2, "wiper: Vout", va="center", color=BLUE, fontsize=11)
ax.text(-0.1, 4.0, "top part\n= R1", ha="right", fontsize=10.5, color=RED); ax.text(-0.1, 1.6, "bottom part\n= R2", ha="right", fontsize=10.5, color=RED)
ax.set_title("a potentiometer: a resistor with a sliding contact", fontsize=11.5)
ax = axes[1]
pos = np.linspace(0, 270, 50)
ax.plot(pos, 5 * pos / 270, color=BLUE, lw=2.5)
ax.plot(135, 2.5, "o", color=BLACK, ms=8); ax.text(140, 2.2, "half-way: 2.5 V", fontsize=10.5)
ax.set_xlabel("knob angle (degrees)"); ax.set_ylabel("wiper voltage (V)"); ax.grid(alpha=0.3)
ax.set_title("the output follows the angle in a straight line", fontsize=11.5)
save(fig, "fig03-potentiometer.png")

# Figure 4: LDR divider output against light for several fixed resistors
fig, ax = plt.subplots(figsize=(10, 5))
lux = np.logspace(0, 4, 300)
ldr = 20000 * (lux / 10) ** -0.7
for r, col, ls in [(1000, GREY, ":"), (4700, BLUE, "-"), (47000, RED, "--")]:
    ax.semilogx(lux, 5 * r / (ldr + r), color=col, lw=2.5, ls=ls, label=f"fixed {r:,} ohm")
ax.axvspan(10, 1000, color=L_GREEN, alpha=0.6); ax.text(100, 0.25, "the range the robot must tell apart", ha="center", fontsize=10.5)
ax.set_xlabel("light (lux, log scale)"); ax.set_ylabel("divider output (V)"); ax.grid(alpha=0.3, which="both")
ax.set_xticks([1, 10, 100, 1000, 10000]); ax.set_xticklabels(["1", "10", "100", "1,000", "10,000"])
ax.legend(loc="upper left", fontsize=10.5); ax.set_ylim(0, 5.2)
ax.set_title("4.7 kohm (close to the best, 4.0 kohm) gives the biggest swing between 10 and 1,000 lux", fontsize=11)
save(fig, "fig04-light-sensor.png")

# Figure 5: thermistor divider - ADC count against temperature
fig, ax = plt.subplots(figsize=(10, 4.8))
T = np.linspace(-10, 110, 200)
Rt = 10000 * np.exp(3950 * (1 / (T + 273.15) - 1 / 298.15))
count = 1023 * Rt / (10000 + Rt)
ax.plot(T, count, color=BLUE, lw=2.5)
for t in [0, 25, 50, 85]:
    r = 10000 * math.exp(3950 * (1 / (t + 273.15) - 1 / 298.15)); c = 1023 * r / (10000 + r)
    ax.plot(t, c, "o", color=ORANGE, mec=BLACK, ms=8); ax.text(t + 3, c + 25, f"{t} C: {c:.0f}", fontsize=10.5)
ax.set_xlabel("temperature (C)"); ax.set_ylabel("Arduino ADC count (0-1023)"); ax.grid(alpha=0.3)
ax.set_title("thermistor below a 10 kohm resistor: steep (fine steps) near 25 C, flatter when hot", fontsize=11.5)
save(fig, "fig05-thermistor-count.png")

# Figure 6: battery monitor - ADC voltage against battery voltage
fig, ax = plt.subplots(figsize=(10, 4.8))
vb = np.linspace(0, 20, 100)
ratio = 4700 / (22000 + 4700)
ax.plot(vb, vb * ratio, color=BLUE, lw=2.5, label="22 kohm over 4.7 kohm")
ax.axhline(3.3, color=RED, ls="--", lw=2, label="ADC limit 3.3 V")
ax.axvspan(13.2, 16.8, color=L_GREEN, alpha=0.7)
ax.text(15.0, 0.6, "4S pack in use\n13.2 to 16.8 V", ha="center", fontsize=10.5)
for v in [13.2, 16.8]:
    ax.plot(v, v * ratio, "o", color=BLACK, ms=7); ax.text(v - 0.2, v * ratio + 0.15, f"{v * ratio:.2f} V", ha="right", fontsize=10.5)
ax.set_xlabel("battery voltage (V)"); ax.set_ylabel("voltage at the ADC pin (V)"); ax.grid(alpha=0.3)
ax.legend(loc="upper left", fontsize=10.5); ax.set_ylim(0, 3.8)
ax.set_title("the divider scales 16.8 V down to 2.96 V, safely under 3.3 V even with a spike", fontsize=11.5)
save(fig, "fig06-battery-monitor.png")
print("saved 6 figures")
