# Figures for Chapter 80 - Breadboards, wires and reading circuit diagrams.
# Run:  python figures.py      (saves PNG files in ../../images/ch080/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch080")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def zigzag(ax, x0, y0, x1, y1, color=BLACK, lw=2, amp=0.12):
    n = 6
    xs, ys = [x0], [y0]
    dx, dy = (x1 - x0), (y1 - y0)
    L = math.hypot(dx, dy); px, py = -dy / L, dx / L
    for k in range(1, 2 * n):
        f = k / (2 * n); s = amp if k % 2 else -amp
        xs.append(x0 + dx * f + px * s); ys.append(y0 + dy * f + py * s)
    xs.append(x1); ys.append(y1)
    ax.plot(xs, ys, color=color, lw=lw)


def line(ax, xs, ys, color=BLACK, lw=2):
    ax.plot(xs, ys, color=color, lw=lw)


# Figure 1: the symbols
fig, ax = plt.subplots(figsize=(12, 7.4))
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.2, 16.2); ax.set_ylim(-0.6, 10.2)


def cell(ax, x, y):
    line(ax, [x, x + 0.8], [y, y]); line(ax, [x + 0.8, x + 0.8], [y - 0.35, y + 0.35], lw=3)
    line(ax, [x + 1.0, x + 1.0], [y - 0.18, y + 0.18], lw=3); line(ax, [x + 1.0, x + 1.8], [y, y])
    ax.text(x + 0.6, y + 0.4, "+", fontsize=11)


slots = []
for row in range(4):
    for col in range(4):
        slots.append((0.3 + col * 4.0, 9.0 - row * 2.6))
labels = []
# 1 cell / battery
x, y = slots[0]; cell(ax, x, y); labels.append("cell or battery\n(long line = +)")
# 2 resistor
x, y = slots[1]; line(ax, [x, x + 0.4], [y, y]); zigzag(ax, x + 0.4, y, x + 1.6, y); line(ax, [x + 1.6, x + 2.0], [y, y])
ax.add_patch(plt.Rectangle((x + 2.3, y - 0.18), 0.9, 0.36, fill=False, ec=BLACK, lw=2)); line(ax, [x + 2.1, x + 2.3], [y, y]); line(ax, [x + 3.2, x + 3.4], [y, y])
labels.append("resistor (US zigzag,\nor European box)")
# 3 potentiometer
x, y = slots[2]; line(ax, [x, x + 0.4], [y, y]); zigzag(ax, x + 0.4, y, x + 1.6, y); line(ax, [x + 1.6, x + 2.0], [y, y])
ax.annotate("", xy=(x + 1.0, y + 0.15), xytext=(x + 1.0, y + 0.8), arrowprops=dict(arrowstyle="-|>", lw=2, color=BLACK))
labels.append("potentiometer\n(arrow = wiper)")
# 4 switch
x, y = slots[3]; line(ax, [x, x + 0.7], [y, y]); ax.plot(x + 0.7, y, "o", color=BLACK, ms=5); line(ax, [x + 0.7, x + 1.5], [y, y + 0.45])
ax.plot(x + 1.6, y, "o", color=BLACK, ms=5); line(ax, [x + 1.6, x + 2.3], [y, y]); labels.append("switch (open)")
# 5 push button
x, y = slots[4]; line(ax, [x, x + 0.7], [y, y]); line(ax, [x + 1.6, x + 2.3], [y, y]); ax.plot([x + 0.7, x + 1.6], [y, y], "o", color=BLACK, ms=5)
line(ax, [x + 0.6, x + 1.7], [y + 0.35, y + 0.35]); line(ax, [x + 1.15, x + 1.15], [y + 0.35, y + 0.75]); labels.append("push button\n(closed while pressed)")
# 6 lamp
x, y = slots[5]; line(ax, [x, x + 0.6], [y, y]); ax.add_patch(plt.Circle((x + 1.0, y), 0.4, fill=False, ec=BLACK, lw=2))
line(ax, [x + 0.72, x + 1.28], [y - 0.28, y + 0.28]); line(ax, [x + 0.72, x + 1.28], [y + 0.28, y - 0.28]); line(ax, [x + 1.4, x + 2.0], [y, y]); labels.append("lamp")
# 7 diode
x, y = slots[6]; line(ax, [x, x + 0.7], [y, y]); ax.add_patch(plt.Polygon([(x + 0.7, y - 0.3), (x + 0.7, y + 0.3), (x + 1.2, y)], color=BLACK))
line(ax, [x + 1.2, x + 1.2], [y - 0.3, y + 0.3], lw=3); line(ax, [x + 1.2, x + 1.9], [y, y]); labels.append("diode (current flows\nthe way the arrow points)")
# 8 LED
x, y = slots[7]; line(ax, [x, x + 0.7], [y, y]); ax.add_patch(plt.Polygon([(x + 0.7, y - 0.3), (x + 0.7, y + 0.3), (x + 1.2, y)], color=BLACK))
line(ax, [x + 1.2, x + 1.2], [y - 0.3, y + 0.3], lw=3); line(ax, [x + 1.2, x + 1.9], [y, y])
for d in [0, 0.3]:
    ax.annotate("", xy=(x + 1.5 + d, y + 0.75), xytext=(x + 1.0 + d, y + 0.35), arrowprops=dict(arrowstyle="-|>", lw=1.5, color=BLACK))
labels.append("LED (arrows = light out)")
# 9 capacitor
x, y = slots[8]; line(ax, [x, x + 0.85], [y, y]); line(ax, [x + 0.85, x + 0.85], [y - 0.35, y + 0.35], lw=3); line(ax, [x + 1.1, x + 1.1], [y - 0.35, y + 0.35], lw=3)
line(ax, [x + 1.1, x + 1.95], [y, y]); labels.append("capacitor (Chapter 84)")
# 10 fuse
x, y = slots[9]; line(ax, [x, x + 0.5], [y, y]); ax.add_patch(plt.Rectangle((x + 0.5, y - 0.18), 1.0, 0.36, fill=False, ec=BLACK, lw=2)); line(ax, [x + 0.5, x + 1.5], [y, y], lw=1.5)
line(ax, [x + 1.5, x + 2.0], [y, y]); labels.append("fuse")
# 11 motor
x, y = slots[10]; line(ax, [x, x + 0.6], [y, y]); ax.add_patch(plt.Circle((x + 1.0, y), 0.4, fill=False, ec=BLACK, lw=2)); ax.text(x + 1.0, y, "M", ha="center", va="center", fontsize=13, fontweight="bold")
line(ax, [x + 1.4, x + 2.0], [y, y]); labels.append("motor")
# 12 ground
x, y = slots[11]; line(ax, [x + 1.0, x + 1.0], [y + 0.5, y]);
for k, w in enumerate([0.5, 0.33, 0.16]):
    line(ax, [x + 1.0 - w, x + 1.0 + w], [y - k * 0.15, y - k * 0.15])
labels.append("ground (0 V)")
# 13 joined wires
x, y = slots[12]; line(ax, [x, x + 2.0], [y, y]); line(ax, [x + 1.0, x + 1.0], [y, y + 0.7]); ax.plot(x + 1.0, y, "o", color=BLACK, ms=8); labels.append("wires JOINED\n(dot at the joint)")
# 14 crossing wires
x, y = slots[13]; line(ax, [x, x + 2.0], [y, y]); line(ax, [x + 1.0, x + 1.0], [y - 0.6, y + 0.6]); labels.append("wires CROSSING\n(no dot: not joined)")
# 15 supply rail
x, y = slots[14]; line(ax, [x + 1.0, x + 1.0], [y - 0.4, y + 0.3]); line(ax, [x + 0.6, x + 1.4], [y + 0.3, y + 0.3]); ax.text(x + 1.0, y + 0.45, "+5V", ha="center", fontsize=11)
labels.append("supply rail\n(joins every '+5V')")
# 16 transistor placeholder (Chapter 87)
x, y = slots[15]; ax.add_patch(plt.Circle((x + 1.0, y), 0.5, fill=False, ec=BLACK, lw=2)); line(ax, [x + 0.2, x + 0.8], [y, y]); line(ax, [x + 0.8, x + 0.8], [y - 0.3, y + 0.3], lw=3)
line(ax, [x + 0.8, x + 1.3], [y + 0.12, y + 0.45]); line(ax, [x + 0.8, x + 1.3], [y - 0.12, y - 0.45])
ax.annotate("", xy=(x + 1.3, y - 0.45), xytext=(x + 1.0, y - 0.25), arrowprops=dict(arrowstyle="-|>", lw=1.5, color=BLACK)); labels.append("transistor (Chapter 87)")
for (x, y), lab in zip(slots, labels):
    ax.text(x + 1.0, y - 0.95, lab, ha="center", va="top", fontsize=10)
save(fig, "fig01-symbols.png")

# Figure 2: inside a breadboard
fig, ax = plt.subplots(figsize=(12, 5.6))
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.5, 16.5); ax.set_ylim(-1.8, 8.6)
ax.add_patch(plt.Rectangle((-0.6, -1.4), 16.4, 9.6, color="#F5F5F0", ec=BLACK))
cols = "abcdefghij"
for r in range(15):
    for k, c in enumerate(cols):
        yy = 0.5 + k * 0.55 + (0.6 if k >= 5 else 0)
        ax.plot(r + 0.5, yy, "s", color=GREY, ms=5)
ax.add_patch(plt.Rectangle((-0.2, 3.05), 15.6, 0.55, color=L_GREY))
ax.text(15.6, 3.32, "centre gap", fontsize=10, va="center")
# highlight strips
ax.add_patch(plt.Rectangle((3.3, 0.3), 0.4, 2.6, color=GREEN, alpha=0.4))
ax.add_patch(plt.Rectangle((7.3, 3.7), 0.4, 2.6, color=BLUE, alpha=0.4))
ax.text(3.5, -0.35, "row 4: holes a-e joined", ha="center", fontsize=10, color=GREEN)
ax.text(7.5, 6.65, "row 8: holes f-j joined\n(not joined to a-e!)", ha="center", fontsize=10, color=BLUE)
for k, c in enumerate(cols):
    yy = 0.5 + k * 0.55 + (0.6 if k >= 5 else 0)
    ax.text(-0.35, yy, c, ha="center", va="center", fontsize=9)
# rails
for yy, sign, col in [(7.3, "+", RED), (7.75, "-", BLUE), (-0.85, "+", RED), (-1.15, "-", BLUE)]:
    pass
ax.plot([0, 15], [7.4, 7.4], color=RED, lw=2); ax.plot([0, 15], [7.85, 7.85], color=BLUE, lw=2)
ax.text(15.3, 7.4, "+ rail", color=RED, fontsize=10, va="center"); ax.text(15.3, 7.85, "- rail", color=BLUE, fontsize=10, va="center")
for r in range(15):
    ax.plot(r + 0.5, 7.4, "s", color=GREY, ms=4); ax.plot(r + 0.5, 7.85, "s", color=GREY, ms=4)
ax.text(7.5, 8.35, "rails run the whole length (on some long boards they break in the middle)", ha="center", fontsize=10)
save(fig, "fig02-breadboard-inside.png")

# Figure 3: a diagram and the same circuit on a breadboard
fig, axes = plt.subplots(1, 2, figsize=(12, 5.2), gridspec_kw=dict(width_ratios=[1, 1.4]))
ax = axes[0]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1.5, 5.5); ax.set_ylim(-1.0, 6.2)
line(ax, [0, 0], [5.6, 5.0]); ax.text(0, 5.75, "+5V", ha="center", fontsize=11, color=RED)
zigzag(ax, 0, 5.0, 0, 3.6); line(ax, [0, 0], [3.6, 3.0]); zigzag(ax, 0, 3.0, 0, 1.6); line(ax, [0, 0], [1.6, 0.3])
ax.plot(0, 3.3, "o", color=BLACK, ms=7); line(ax, [0, 2.5], [3.3, 3.3]); line(ax, [2.5, 2.5], [3.3, 2.9]); zigzag(ax, 2.5, 2.9, 2.5, 1.5); line(ax, [2.5, 2.5], [1.5, 0.3])
line(ax, [0, 2.5], [0.3, 0.3]); ax.plot(1.25, 0.3, "o", color=BLACK, ms=7)
line(ax, [1.25, 1.25], [0.3, -0.1]);
for k, w in enumerate([0.4, 0.26, 0.12]):
    line(ax, [1.25 - w, 1.25 + w], [-0.1 - k * 0.13, -0.1 - k * 0.13])
ax.text(0.3, 4.3, "R1 10k", fontsize=10.5, color=RED); ax.text(0.3, 2.3, "R2 10k", fontsize=10.5, color=RED); ax.text(2.8, 2.2, "R3 1k", fontsize=10.5, color=RED)
ax.text(0.3, 3.55, "tap", fontsize=10, color=BLUE)
ax.set_title("the circuit diagram", fontsize=11.5)
ax = axes[1]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1, 23); ax.set_ylim(-1.5, 8.2)
ax.add_patch(plt.Rectangle((-0.6, -1.0), 22, 8.9, color="#F5F5F0", ec=BLACK))
for r in range(21):
    for k in range(10):
        yy = 0.3 + k * 0.55 + (0.6 if k >= 5 else 0)
        ax.plot(r + 0.5, yy, "s", color=L_GREY, ms=4)
ax.plot([0, 21], [6.9, 6.9], color=RED, lw=2); ax.plot([0, 21], [7.4, 7.4], color=BLUE, lw=2)
ax.text(21.4, 6.9, "+", color=RED, fontsize=12, va="center"); ax.text(21.4, 7.4, "-", color=BLUE, fontsize=12, va="center")


def hole(r, c):
    k = "abcdefghij".index(c)
    return r - 0.5, 0.3 + k * 0.55 + (0.6 if k >= 5 else 0)


def part(ax, h1, h2, label, color):
    (x1, y1), (x2, y2) = hole(*h1), hole(*h2)
    ax.plot([x1, x2], [y1, y2], color=color, lw=5, solid_capstyle="round")
    ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.35, label, ha="center", fontsize=9.5)


part(ax, (5, "a"), (10, "a"), "R1", ORANGE); part(ax, (10, "b"), (15, "b"), "R2", ORANGE); part(ax, (10, "c"), (20, "c"), "R3", ORANGE)
for (r, c), yr, col in [((5, "e"), 6.9, RED), ((15, "e"), 7.4, BLUE), ((20, "e"), 7.4, BLUE)]:
    x, y = hole(r, c); ax.plot([x, x + 0.3], [y, yr], color=col, lw=2.5)
x, y = hole(10, "d"); ax.text(x, y + 0.25, "tap", ha="center", fontsize=9.5, color=BLUE)
ax.set_title("the same circuit on a breadboard (rows 5, 10, 15, 20)", fontsize=11.5)
save(fig, "fig03-diagram-to-board.png")

# Figure 4: four common breadboard mistakes
fig, axes = plt.subplots(1, 4, figsize=(13, 3.6))
titles = ["both legs in one row:\nthe part is shorted out", "across rows on the same\nside of the gap: fine",
          "a chip must straddle\nthe centre gap", "rails split in the middle\nof a long board"]
for k, (ax, title) in enumerate(zip(axes, titles)):
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.5, 6.5); ax.set_ylim(-0.5, 6.5)
    ax.add_patch(plt.Rectangle((-0.3, -0.3), 6.6, 6.6, color="#F5F5F0", ec=BLACK))
    for r in range(6):
        for c in range(5):
            ax.plot(r + 0.5, c * 0.55 + 0.4, "s", color=L_GREY, ms=4)
            ax.plot(r + 0.5, c * 0.55 + 3.6, "s", color=L_GREY, ms=4)
    ax.set_title(title, fontsize=10)
axes[0].plot([2.5, 2.5], [0.4, 2.6], color=RED, lw=5); axes[0].add_patch(plt.Rectangle((2.25, 0.2), 0.5, 2.6, color=GREEN, alpha=0.25))
axes[1].plot([1.5, 4.5], [1.5, 1.5], color=ORANGE, lw=5)
axes[2].add_patch(plt.Rectangle((1.2, 2.4), 3.6, 1.6, color=BLACK)); axes[2].text(3.0, 3.2, "chip", color="white", ha="center", va="center")
for r in range(4):
    axes[2].plot([1.5 + r, 1.5 + r], [2.0, 2.4], color=GREY, lw=3); axes[2].plot([1.5 + r, 1.5 + r], [4.0, 4.4], color=GREY, lw=3)
ax = axes[3]; ax.plot([0, 2.8], [6.0, 6.0], color=RED, lw=3); ax.plot([3.2, 6.0], [6.0, 6.0], color=RED, lw=3); ax.text(3.0, 5.5, "gap", ha="center", fontsize=10)
ax.plot([2.6, 3.4], [6.25, 6.25], color=GREEN, lw=2); ax.text(3.0, 6.45, "bridge wire", ha="center", fontsize=9, color=GREEN)
save(fig, "fig04-mistakes.png")

# Figure 5: wire gauge - area and safe current
fig, ax = plt.subplots(figsize=(10, 4.8))
g = np.arange(30, 9, -2)
d = 0.127 * 92 ** ((36 - g) / 39); area = math.pi * (d / 2) ** 2
safe = np.sqrt(5.0 / (1.68e-8 / (area * 1e-6)))
ax.bar(range(len(g)), safe, color=BLUE, edgecolor=BLACK)
for k, (s, a) in enumerate(zip(safe, area)):
    ax.text(k, s + 0.6, f"{a:.2f}\nmm2", ha="center", fontsize=8.5)
ax.set_xticks(range(len(g))); ax.set_xticklabels([str(x) for x in g]); ax.set_xlabel("AWG (smaller number = thicker wire)")
ax.set_ylabel("current for 5 W of heat per metre (A)"); ax.grid(alpha=0.3, axis="y"); ax.set_ylim(0, 46)
ax.set_title("thicker wire, more current: the area doubles every 3 gauge numbers", fontsize=11.5)
save(fig, "fig05-wire-gauge.png")

# Figure 6: voltage lost through a breadboard
fig, ax = plt.subplots(figsize=(10, 4.6))
I = np.linspace(0, 3.2, 100)
ax.plot(I, I * 0.26, color=RED, lw=2.5, label="through a breadboard and two jumpers (0.26 ohm)")
ax.plot(I, I * 0.02, color=GREEN, lw=2.5, label="screw terminals and 20 AWG wire (0.02 ohm)")
ax.axvline(1.0, color=GREY, ls="--"); ax.text(1.05, 0.5, "breadboard\nrating 1 A", fontsize=10)
ax.axvline(3.1, color=BLACK, ls=":"); ax.text(3.05, 0.45, "Rover's\nmotor start", fontsize=10, ha="right")
ax.set_xlabel("current (A)"); ax.set_ylabel("volts lost in the connections (V)"); ax.grid(alpha=0.3); ax.legend(fontsize=10, loc="upper left")
ax.set_title("breadboards are for signals and small currents, not motors", fontsize=11.5)
save(fig, "fig06-breadboard-loss.png")
print("saved 6 figures")
