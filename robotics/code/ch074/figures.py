# Figures for Chapter 74 - Voltage, current and resistance.
# Run:  python figures.py      (saves PNG files in ../../images/ch074/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.ticker
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch074")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Figure 1: the water picture - tower height = voltage, flow = current, narrow pipe = resistance
fig, ax = plt.subplots(figsize=(11, 5.2))
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.5, 12); ax.set_ylim(-0.8, 6.2)
ax.add_patch(plt.Rectangle((0, 3.5), 2.2, 2.0, color=L_BLUE, ec=BLACK, lw=2))
ax.text(1.1, 4.5, "water\ntank", ha="center", va="center", fontsize=11)
ax.plot([1.1, 1.1], [0, 3.5], color=BLACK, lw=2); ax.plot([0.6, 1.6], [0, 0], color=BLACK, lw=3)
ax.annotate("", xy=(2.9, 4.5), xytext=(2.9, 0.4), arrowprops=dict(arrowstyle="<->", lw=2, color=BLUE))
ax.text(3.1, 2.5, "height = VOLTAGE\n(energy each litre has)", color=BLUE, fontsize=11, va="center")
# pipe going right and down
ax.plot([2.2, 6.0], [3.7, 3.7], color=BLACK, lw=2); ax.plot([2.2, 6.0], [4.1, 4.1], color=BLACK, lw=2)
ax.plot([6.0, 6.0], [4.1, 1.2], color=BLACK, lw=2); ax.plot([6.4, 6.4], [3.7, 1.2], color=BLACK, lw=2)
# narrow part
ax.plot([6.0, 6.15], [1.2, 1.0], color=BLACK, lw=2); ax.plot([6.4, 6.25], [1.2, 1.0], color=BLACK, lw=2)
ax.plot([6.15, 6.15], [1.0, 0.2], color=RED, lw=2.5); ax.plot([6.25, 6.25], [1.0, 0.2], color=RED, lw=2.5)
ax.text(6.7, 0.6, "narrow pipe = RESISTANCE\n(slows the flow)", color=RED, fontsize=11, va="center")
for x in [3.0, 4.2, 5.4]:
    ax.annotate("", xy=(x + 0.7, 3.9), xytext=(x, 3.9), arrowprops=dict(arrowstyle="-|>", lw=2, color=GREEN))
ax.text(4.9, 4.7, "flow = CURRENT (litres each second)", color=GREEN, fontsize=11, ha="center")
# a pump bringing water back up
ax.annotate("", xy=(6.2, -0.1), xytext=(6.2, 0.1), arrowprops=dict(arrowstyle="-", lw=0))
ax.plot([6.2, 6.2, 9.0, 9.0], [0.2, -0.4, -0.4, 5.6], color=GREY, lw=2, ls="--")
ax.plot([9.0, 1.1], [5.6, 5.6], color=GREY, lw=2, ls="--")
ax.add_patch(plt.Circle((9.0, 2.6), 0.55, color=ORANGE, ec=BLACK)); ax.text(9.0, 2.6, "pump", ha="center", va="center", fontsize=10)
ax.text(9.8, 2.6, "= the BATTERY:\nlifts the water back\nup to the tank", fontsize=10.5, va="center")
save(fig, "fig01-water-picture.png")

# Figure 2: voltage is between two points; ground is the reference
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1, 10.5); ax.set_ylim(-1.2, 8.6)
levels = [("battery +", 7.2, ORANGE), ("regulator out", 5.0, BLUE), ("sensor signal", 3.3, GREEN), ("ground (0 V)", 0.0, BLACK)]
for name, v, c in levels:
    ax.plot([0, 6], [v, v], color=c, lw=3)
    ax.text(6.2, v, f"{name}: {v:.1f} V", va="center", fontsize=11.5, color=c)
ax.annotate("", xy=(1.0, 7.2), xytext=(1.0, 0.0), arrowprops=dict(arrowstyle="<->", lw=2, color=ORANGE))
ax.text(1.15, 1.8, "7.2 V\nabove\nground", color=ORANGE, fontsize=10.5, va="center")
ax.annotate("", xy=(3.0, 7.2), xytext=(3.0, 5.0), arrowprops=dict(arrowstyle="<->", lw=2, color=RED))
ax.text(3.15, 6.1, "2.2 V between\nthese two", color=RED, fontsize=10.5, va="center")
ax.annotate("", xy=(5.0, 5.0), xytext=(5.0, 3.3), arrowprops=dict(arrowstyle="<->", lw=2, color=RED))
ax.text(4.0, 4.15, "1.7 V", color=RED, fontsize=10.5, va="center", ha="right")
ax.text(3, -0.9, "voltage is always BETWEEN two points; 'ground' is the point we call 0 V", ha="center", fontsize=11.5)
save(fig, "fig02-voltage-between.png")

# Figure 3: cells in series add their voltages
fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
for ax, (title, n, vcell, col) in zip(axes, [("Rover: 6 NiMH cells, 1.2 V each", 6, 1.2, ORANGE), ("drone: 4 lithium cells (4S), 3.7 V each", 4, 3.7, BLUE)]):
    ax.set_xlim(-0.6, n * 1.6 + 1.5); ax.set_ylim(-0.5, n * vcell + 2.2); ax.axis("off")
    total = 0
    for k in range(n):
        ax.add_patch(plt.Rectangle((k * 1.6, 0), 1.2, 1.0, color=col, ec=BLACK))
        ax.text(k * 1.6 + 0.6, 0.5, f"{vcell} V", ha="center", va="center", fontsize=9)
        if k < n - 1:
            ax.plot([k * 1.6 + 1.2, (k + 1) * 1.6], [0.5, 0.5], color=BLACK, lw=2)
        total += vcell
        ax.bar(k * 1.6 + 0.6, total, width=0.5, bottom=1.4, color=L_GREY, edgecolor=BLACK)
        ax.text(k * 1.6 + 0.6, total + 1.55, f"{total:.1f} V", ha="center", fontsize=9.5)
    ax.text(-0.5, 0.5, "-", fontsize=16, va="center", fontweight="bold"); ax.text(n * 1.6 - 0.2, 0.5, "+", fontsize=14, va="center", fontweight="bold")
    ax.set_title(title, fontsize=11.5)
fig.suptitle("cells in a row (in series): the voltages add up, each cell lifts the charge a bit higher", fontsize=12, y=0.0)
save(fig, "fig03-cells-in-series.png")

# Figure 4: resistance of copper wire vs length and vs area
fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
L = np.linspace(0, 10, 50)
for area, col in [(0.5, RED), (1.0, ORANGE), (2.0, BLUE), (4.0, GREEN)]:
    axes[0].plot(L, 1.68e-8 * L / (area * 1e-6) * 1000, color=col, lw=2.5, label=f"{area} mm2")
axes[0].set_xlabel("length of copper wire (m)"); axes[0].set_ylabel("resistance (milliohms)"); axes[0].grid(alpha=0.3)
axes[0].legend(title="area", fontsize=10); axes[0].set_title("longer = more resistance (straight line)", fontsize=11)
A = np.linspace(0.2, 4, 100)
axes[1].plot(A, 1.68e-8 * 1.0 / (A * 1e-6) * 1000, color=BLUE, lw=2.5)
for a in [0.5, 1.0, 2.0, 4.0]:
    r = 1.68e-8 / (a * 1e-6) * 1000
    axes[1].plot(a, r, "o", color=ORANGE, mec=BLACK, ms=8); axes[1].text(a + 0.1, r + 3, f"{r:.1f}", fontsize=10)
axes[1].set_xlabel("cross-section area (mm2)"); axes[1].set_ylabel("resistance of 1 m (milliohms)"); axes[1].grid(alpha=0.3)
axes[1].set_title("thicker = less resistance (halve the area, double R)", fontsize=11)
save(fig, "fig04-wire-resistance.png")

# Figure 5: thermistor curve
T = np.linspace(-10, 100, 200)
R = 10000 * np.exp(3950 * (1 / (T + 273.15) - 1 / 298.15))
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.semilogy(T, R, color=BLUE, lw=2.5)
for t in [0, 25, 50, 80]:
    r = 10000 * math.exp(3950 * (1 / (t + 273.15) - 1 / 298.15))
    ax.plot(t, r, "o", color=ORANGE, mec=BLACK, ms=8); ax.text(t + 2, r * 1.25, f"{t} C: {r:,.0f} ohms", fontsize=10.5)
ax.axvspan(70, 85, color=L_ORANGE); ax.axvspan(85, 100, color="#F5C6B0")
ax.text(77.5, 40000, "warn", ha="center", fontsize=10.5); ax.text(92.5, 40000, "stop", ha="center", fontsize=10.5)
ax.set_xlabel("temperature (degrees C)"); ax.set_ylabel("resistance (ohms, log scale)"); ax.grid(alpha=0.3, which="both")
ax.set_yticks([1000, 10000, 100000]); ax.set_yticklabels(["1,000", "10,000", "100,000"])
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_title("an NTC thermistor: resistance falls as it gets hotter", fontsize=12)
save(fig, "fig05-thermistor.png")

# Figure 6: the three quantities on one circuit, with the resistor symbol
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.5, 9.5); ax.set_ylim(-1.2, 4.6)
# battery symbol
ax.plot([-0.45, 0.45], [1.85, 1.85], color=BLACK, lw=3); ax.plot([-0.22, 0.22], [1.45, 1.45], color=BLACK, lw=3)
ax.plot([0, 0], [1.85, 3.5], color=BLACK, lw=2); ax.plot([0, 0], [-0.3, 1.45], color=BLACK, lw=2)
ax.plot([0.0, 6.0], [3.5, 3.5], color=BLACK, lw=2); ax.plot([0.0, 6.0], [-0.3, -0.3], color=BLACK, lw=2)
ax.text(0.6, 2.0, "+", fontsize=14, fontweight="bold"); ax.text(0.6, 0.9, "-", fontsize=16, fontweight="bold")
ax.text(-1.4, 1.6, "V\n7.2 V\n(the push:\njoules per\ncoulomb)", color=ORANGE, fontsize=10.5, ha="center", va="center")
# resistor zigzag on the right
zx = [6.0, 6.0, 6.2, 5.8, 6.2, 5.8, 6.2, 5.8, 6.0, 6.0]
zy = [3.5, 2.4, 2.2, 1.9, 1.6, 1.3, 1.0, 0.7, 0.5, -0.3]
ax.plot(zx, zy, color=BLACK, lw=2.5)
ax.text(6.6, 1.6, "R\nresistance\n(ohms):\nhow much the\nflow is slowed", color=RED, fontsize=10.5, va="center")
for x in [1.5, 3.5]:
    ax.annotate("", xy=(x + 0.8, 3.5), xytext=(x, 3.5), arrowprops=dict(arrowstyle="-|>", lw=2.5, color=GREEN))
ax.text(3.0, 3.9, "I  current (amps): coulombs per second, the same all round the loop", color=GREEN, fontsize=10.5, ha="center")
for x in [4.3, 2.3]:
    ax.annotate("", xy=(x - 0.8, -0.3), xytext=(x, -0.3), arrowprops=dict(arrowstyle="-|>", lw=2.5, color=GREEN))
ax.text(3.0, -0.85, "Chapter 75 ties the three together: V = I x R", ha="center", fontsize=11)
save(fig, "fig06-three-quantities.png")
print("saved 6 figures")
