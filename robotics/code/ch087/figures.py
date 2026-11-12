# Figures for Chapter 87 - Transistors as switches (BJT).
# Run:  python figures.py      (saves PNG files in ../../images/ch087/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch087")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def line(ax, xs, ys, color=BLACK, lw=2):
    ax.plot(xs, ys, color=color, lw=lw)


def npn(ax, x, y, r=0.6, labels=True):
    ax.add_patch(plt.Circle((x, y), r, fill=False, ec=BLACK, lw=2))
    line(ax, [x - 0.25, x - 0.25], [y - 0.35, y + 0.35], lw=3)
    line(ax, [x - 1.0, x - 0.25], [y, y])
    line(ax, [x - 0.25, x + 0.25], [y + 0.12, y + 0.4]); line(ax, [x + 0.25, x + 0.25], [y + 0.4, y + 1.0])
    line(ax, [x - 0.25, x + 0.25], [y - 0.12, y - 0.4]); line(ax, [x + 0.25, x + 0.25], [y - 0.4, y - 1.0])
    ax.annotate("", xy=(x + 0.25, y - 0.4), xytext=(x, y - 0.26), arrowprops=dict(arrowstyle="-|>", lw=1.5, color=BLACK))
    if labels:
        ax.text(x - 1.05, y + 0.15, "B", fontsize=11); ax.text(x + 0.35, y + 0.75, "C", fontsize=11); ax.text(x + 0.35, y - 0.85, "E", fontsize=11)


# Figure 1: the NPN symbol and the tap picture
fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
ax = axes[0]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-3, 3); ax.set_ylim(-2.2, 2.2)
npn(ax, 0.5, 0)
ax.text(-2.8, 1.4, "base (B): the small\ncontrol current goes in", fontsize=10.5)
ax.text(1.3, 1.4, "collector (C):\nthe big current\ncomes in", fontsize=10.5)
ax.text(1.3, -1.7, "emitter (E):\nboth leave here", fontsize=10.5)
ax.set_title("an NPN transistor", fontsize=11.5)
ax = axes[1]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.5, 7); ax.set_ylim(-1, 5)
ax.add_patch(plt.Rectangle((2.5, 0), 1.5, 4.5, color=L_BLUE, ec=BLACK)); ax.add_patch(plt.Rectangle((2.5, 1.8), 1.5, 0.6, color=GREY, ec=BLACK))
ax.annotate("", xy=(3.25, 0.2), xytext=(3.25, 4.3), arrowprops=dict(arrowstyle="-|>", lw=5, color=BLUE))
ax.plot([4.0, 5.2], [2.1, 2.1], color=ORANGE, lw=2); ax.add_patch(plt.Circle((5.4, 2.1), 0.25, color=ORANGE))
ax.text(5.7, 2.1, "a small hand\non the tap", va="center", fontsize=10.5)
ax.text(1.2, 4.0, "big flow\n(collector)", ha="center", fontsize=10.5, color=BLUE)
ax.set_title("like a tap: a small effort controls a big flow", fontsize=11.5)
save(fig, "fig01-npn.png")

# Figure 2: collector current against base current for the 12 V lamp
fig, ax = plt.subplots(figsize=(10, 4.8))
ib = np.linspace(0, 8, 300)
ic = np.minimum(100 * ib, (12 - 0.2) / 40 * 1000)
ax.plot(ib, ic, color=BLUE, lw=2.5)
ax.axvspan(0, 2.95, color=L_ORANGE, alpha=0.6); ax.axvspan(2.95, 8, color=L_GREEN, alpha=0.6)
ax.text(1.4, 150, "ACTIVE:\nIc = 100 x Ib\n(half on)", ha="center", fontsize=11)
ax.text(5.5, 150, "SATURATED:\nfully on; the lamp\nsets the current", ha="center", fontsize=11)
ax.axvline(15 / 1, color=GREEN, ls=":")
ax.set_xlabel("base current (mA)"); ax.set_ylabel("collector current (mA)"); ax.grid(alpha=0.3); ax.set_xlim(0, 8); ax.set_ylim(0, 330)
ax.set_title("more base current, more collector current, until the load allows no more", fontsize=11.5)
save(fig, "fig02-regions.png")

# Figure 3: the low-side switch circuit
fig, ax = plt.subplots(figsize=(10, 5.4))
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-4, 7); ax.set_ylim(-1.6, 6.3)
npn(ax, 2.0, 1.2, labels=False)
line(ax, [2.25, 2.25], [2.2, 3.0])
for k in range(4):
    ax.add_patch(matplotlib.patches.Arc((2.25, 3.2 + k * 0.4), 0.5, 0.4, theta1=-90, theta2=90, color=ORANGE, lw=2.5))
line(ax, [2.25, 2.25], [4.6, 5.6]); ax.text(2.25, 5.8, "+5 V (or +12 V)", ha="center", color=RED, fontsize=11)
ax.text(1.6, 3.8, "relay\ncoil", ha="right", fontsize=10.5)
line(ax, [2.25, 3.6], [5.2, 5.2]); line(ax, [3.6, 3.6], [5.2, 4.3]); line(ax, [3.6, 3.6], [3.5, 2.6]); line(ax, [3.6, 2.25], [2.6, 2.6])
ax.add_patch(plt.Polygon([(3.25, 3.5), (3.95, 3.5), (3.6, 4.2)], color=GREEN)); line(ax, [3.25, 3.95], [4.25, 4.25], color=GREEN, lw=3)
ax.text(4.1, 3.9, "flyback diode\n(Chapter 86)", fontsize=10, color=GREEN)
line(ax, [2.25, 2.25], [0.2, -0.6]); line(ax, [1.85, 2.65], [-0.6, -0.6], lw=3); ax.text(2.25, -1.0, "ground", ha="center", fontsize=10)
line(ax, [-3.2, -2.4], [1.2, 1.2]); ax.add_patch(plt.Rectangle((-2.4, 1.0), 1.0, 0.4, fill=False, ec=BLACK, lw=2)); line(ax, [-1.4, 1.0], [1.2, 1.2])
ax.text(-3.3, 1.2, "Arduino\npin", ha="right", va="center", fontsize=10.5); ax.text(-1.9, 1.6, "Rb 1 k", ha="center", fontsize=10.5, color=RED)
line(ax, [-0.5, -0.5], [1.2, 0.6]); ax.add_patch(plt.Rectangle((-0.7, -0.4), 0.4, 1.0, fill=False, ec=BLACK, lw=2)); line(ax, [-0.5, -0.5], [-0.4, -0.6]); line(ax, [-0.5, 2.25], [-0.6, -0.6])
ax.text(-0.1, 0.1, "10 k\n(keeps it off\nat start-up)", fontsize=9.5)
ax.text(5.2, 1.2, "the load sits ABOVE the\ntransistor: a 'low-side' switch", fontsize=10.5, va="center")
save(fig, "fig03-low-side.png")

# Figure 4: heat in the transistor against base current
fig, ax = plt.subplots(figsize=(10, 4.6))
p = []
for x in ib:
    c = min(100 * x / 1000, (12 - 0.2) / 40)
    p.append(c * (12 - c * 40))
ax.plot(ib, np.array(p) * 1000, color=RED, lw=2.5)
ax.axhline(625, color=BLACK, ls="--"); ax.text(7.9, 650, "a small TO-92 transistor can shed about 0.6 W", ha="right", fontsize=10.5)
ax.annotate("fully on: 59 mW", xy=(5, 59), xytext=(5.5, 250), arrowprops=dict(arrowstyle="->"), fontsize=10.5)
ax.annotate("half on: up to 900 mW", xy=(1.5, 900), xytext=(3.5, 820), arrowprops=dict(arrowstyle="->"), fontsize=10.5)
ax.set_xlabel("base current (mA)"); ax.set_ylabel("heat in the transistor (mW)"); ax.grid(alpha=0.3); ax.set_xlim(0, 8); ax.set_ylim(0, 1000)
ax.set_title("a switch must be fully off or fully on: half way it gets hot", fontsize=11.5)
save(fig, "fig04-heat.png")

# Figure 5: light-controlled motor: single transistor vs Darlington
fig, ax = plt.subplots(figsize=(10, 4.6))
lux = np.logspace(0, 4, 300)
imax = (6 - 0.2) / 15 * 1000
single = np.minimum(150 * lux * 0.5e-6 * 1000, imax)
dar = np.minimum(22500 * lux * 0.5e-6 * 1000, imax)
ax.semilogx(lux, single, color=BLUE, lw=2.5, label="phototransistor + one transistor (gain 150)")
ax.semilogx(lux, dar, color=ORANGE, lw=2.5, ls="--", label="phototransistor + Darlington pair (gain 22,500)")
ax.axhline(80, color=GREY, ls=":"); ax.text(1.2, 90, "motor starts at 80 mA", fontsize=10)
ax.axvspan(200, 500, color=L_GREY, alpha=0.6); ax.text(320, 200, "a room", ha="center", fontsize=10.5)
ax.set_xlabel("light on the sensor (lux, log scale)"); ax.set_ylabel("motor current (mA)"); ax.grid(alpha=0.3, which="both"); ax.legend(loc="center left", fontsize=10)
ax.set_xticks([1, 10, 100, 1000, 10000]); ax.set_xticklabels(["1", "10", "100", "1,000", "10,000"])
ax.set_title("light in, motor current out: no code, just gain", fontsize=11.5)
save(fig, "fig05-light-motor.png")

# Figure 6: an optocoupler
fig, ax = plt.subplots(figsize=(10, 4.4))
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1, 11); ax.set_ylim(-1, 4.5)
ax.add_patch(plt.Rectangle((3.5, 0), 3.0, 3.6, fill=False, ec=BLACK, lw=2, ls="--"))
ax.add_patch(plt.Polygon([(4.0, 2.2), (4.6, 2.2), (4.3, 1.6)], color=RED)); line(ax, [3.95, 4.65], [1.55, 1.55], color=RED, lw=3)
line(ax, [4.3, 4.3], [2.2, 3.0]); line(ax, [4.3, 4.3], [1.55, 0.6]); line(ax, [0.5, 4.3], [3.0, 3.0]); line(ax, [0.5, 4.3], [0.6, 0.6])
for d in [0, 0.5]:
    ax.annotate("", xy=(5.4, 2.1 - d), xytext=(4.8, 2.1 - d), arrowprops=dict(arrowstyle="-|>", lw=1.5, color=ORANGE))
npn(ax, 6.0, 1.8, r=0.5, labels=False)
line(ax, [6.25, 6.25], [2.8, 3.0]); line(ax, [6.25, 9.5], [3.0, 3.0]); line(ax, [6.25, 6.25], [0.8, 0.6]); line(ax, [6.25, 9.5], [0.6, 0.6])
ax.text(0.4, 3.0, "24 V factory\nsensor signal", ha="right", va="center", fontsize=10.5)
ax.text(9.6, 3.0, "to the 3.3 V\nmicrocontroller", va="center", fontsize=10.5)
ax.text(5.0, 3.9, "light crosses the gap: no wire joins the two sides", ha="center", fontsize=10.5)
ax.text(2.0, -0.5, "LED side", ha="center", fontsize=10.5, color=RED); ax.text(8.0, -0.5, "phototransistor side", ha="center", fontsize=10.5, color=BLUE)
save(fig, "fig06-optocoupler.png")
print("saved 6 figures")
