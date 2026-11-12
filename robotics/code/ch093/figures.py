# Figures for Chapter 93 - Project: Moth, a light-seeking robot made only with transistors.
# Run:  python figures.py      (saves PNG files in ../../images/ch093/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch, Polygon
from matplotlib.ticker import NullFormatter
import numpy as np
from moth_channel import channel, I_START, I_MAX, THETA
import moth_sim

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch093")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN = "#BFE3F5", "#FBE3B3", "#BDEBDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def line(ax, xs, ys, color=BLACK, lw=2, **kw):
    ax.plot(xs, ys, color=color, lw=lw, **kw)


# Figure 1: the idea, seen from above: crossed and straight wiring
fig, axes = plt.subplots(1, 2, figsize=(11, 5.4))
for ax, crossed, title in [(axes[0], True, "CROSSED: turns towards the light (Moth)"), (axes[1], False, "STRAIGHT: turns away from the light")]:
    ax.set_xlim(-3, 3); ax.set_ylim(-3.2, 3.6); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(FancyBboxPatch((-1.4, -2.0), 2.8, 3.4, boxstyle="round,pad=0.1", fc="#EEEEEE", ec=BLACK))
    for sx in (-1, 1):
        ax.add_patch(Rectangle((sx * 1.55 - 0.25, -1.8), 0.5, 1.2, fc=GREY, ec=BLACK))
        ax.add_patch(Circle((sx * 0.8, 1.55), 0.28, fc="#FFF3B0", ec=BLACK))
    ax.text(-0.8, 2.05, "left eye", ha="center", fontsize=10); ax.text(0.8, 2.05, "right eye", ha="center", fontsize=10)
    ax.text(-2.4, -1.2, "left\nwheel", ha="center", fontsize=10); ax.text(2.4, -1.2, "right\nwheel", ha="center", fontsize=10)
    ax.add_patch(Circle((-2.3, 3.0), 0.35, fc="#FFD400", ec=BLACK)); ax.text(-2.3, 2.35, "lamp", ha="center", fontsize=10)
    for k in range(5):
        a = math.radians(-60 + k * 10)
        ax.plot([-2.3 + 0.4 * math.cos(a), -2.3 + 0.8 * math.cos(a)], [3.0 + 0.4 * math.sin(a), 3.0 + 0.8 * math.sin(a)], color=ORANGE, lw=1.5)
    if crossed:
        ax.annotate("", xy=(1.4, -1.2), xytext=(-0.8, 1.25), arrowprops=dict(arrowstyle="->", color=RED, lw=3))
        ax.annotate("", xy=(-1.4, -1.2), xytext=(0.8, 1.25), arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2))
        ax.text(0, -2.75, "bright left eye -> fast RIGHT wheel -> turns LEFT", ha="center", fontsize=10.5, color=RED)
    else:
        ax.annotate("", xy=(-1.4, -1.2), xytext=(-0.8, 1.25), arrowprops=dict(arrowstyle="->", color=RED, lw=3))
        ax.annotate("", xy=(1.4, -1.2), xytext=(0.8, 1.25), arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2))
        ax.text(0, -2.75, "bright left eye -> fast LEFT wheel -> turns RIGHT", ha="center", fontsize=10.5, color=RED)
    ax.set_title(title, fontsize=11.5)
save(fig, "fig01-crossed-wiring.png")

# Figure 2: one channel's circuit
fig, ax = plt.subplots(figsize=(9.5, 6.4))
ax.set_xlim(-0.5, 10); ax.set_ylim(-0.6, 7.2); ax.set_aspect("equal"); ax.axis("off")
line(ax, [0.5, 9.0], [6.5, 6.5]); ax.text(0.5, 6.75, "+6 V (4 x AA, switch, 100 uF)", fontsize=11)
line(ax, [0.5, 9.0], [0.3, 0.3]); ax.text(0.5, -0.15, "0 V", fontsize=11)
# LDR
line(ax, [2, 2], [6.5, 5.6]); ax.add_patch(Rectangle((1.7, 4.3), 0.6, 1.3, fill=False, ec=BLACK, lw=2))
ax.text(2.5, 4.95, "LDR (eye)", fontsize=11); ax.annotate("", xy=(1.75, 5.0), xytext=(0.9, 5.7), arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.5))
line(ax, [2, 2], [4.3, 3.4])
ax.add_patch(Circle((2, 3.4), 0.07, color=BLACK))
line(ax, [2, 2], [3.4, 2.6]); ax.add_patch(Rectangle((1.7, 1.3), 0.6, 1.3, fill=False, ec=BLACK, lw=2)); ax.text(2.5, 1.85, "R_B 4.7 k", fontsize=11, color=RED); line(ax, [2, 2], [1.3, 0.3])
line(ax, [2, 5.2], [3.4, 3.4]); ax.text(3.0, 3.6, "base", fontsize=10)
# transistor
ax.add_patch(Circle((5.8, 3.4), 0.75, fill=False, ec=BLACK, lw=2))
line(ax, [5.2, 5.5], [3.4, 3.4]); line(ax, [5.5, 5.5], [2.9, 3.9], lw=3)
line(ax, [5.5, 6.2], [3.65, 4.1]); line(ax, [6.2, 6.2], [4.1, 4.4])
line(ax, [5.5, 6.2], [3.15, 2.7]); line(ax, [6.2, 6.2], [2.7, 0.3])
ax.annotate("", xy=(6.15, 2.72), xytext=(5.8, 2.95), arrowprops=dict(arrowstyle="->", color=BLACK, lw=1.5))
ax.text(6.7, 3.3, "BD139\n(NPN)", fontsize=10.5)
# motor and diode
line(ax, [6.2, 6.2], [4.4, 4.7]); ax.add_patch(Circle((6.2, 5.2), 0.5, fill=False, ec=BLACK, lw=2)); ax.text(6.2, 5.2, "M", ha="center", va="center", fontsize=13)
line(ax, [6.2, 6.2], [5.7, 6.5]); ax.text(5.55, 5.75, "OTHER side's\nmotor", fontsize=10.5, color=BLUE, ha="right", va="center")
line(ax, [6.2, 8.3], [4.55, 4.55]); line(ax, [6.2, 8.3], [6.0, 6.0]); line(ax, [8.3, 8.3], [4.55, 4.95]); line(ax, [8.3, 8.3], [5.6, 6.0])
ax.add_patch(Polygon([[8.0, 4.95], [8.6, 4.95], [8.3, 5.5]], closed=True, fc="white", ec=BLACK, lw=1.5)); line(ax, [8.0, 8.6], [5.55, 5.55])
ax.text(8.75, 5.1, "1N4001\nflyback", fontsize=10)
save(fig, "fig02-channel-circuit.png")

# Figure 3: motor current and transistor heat against light
lux = np.logspace(0.5, 3, 300)
fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6))
for r_b, col, ls in [(1000, ORANGE, "--"), (4700, BLUE, "-"), (22000, GREEN, ":")]:
    axes[0].plot(lux, [channel(l, r_b)[1] * 1000 for l in lux], color=col, ls=ls, lw=2.3, label=f"R_B = {r_b / 1000:g} k")
axes[0].axhline(I_START * 1000, color=RED, ls=":", lw=1.2); axes[0].text(3.5, I_START * 1000 + 8, "motor starts: 80 mA", fontsize=10, color=RED)
axes[0].axhline(I_MAX * 1000, color=BLACK, ls=":", lw=1.2); axes[0].text(3.5, I_MAX * 1000 - 25, "fully on: 387 mA", fontsize=10)
axes[1].plot(lux, [channel(l)[2] * THETA for l in lux], color=RED, lw=2.3)
axes[1].set_ylabel("BD139 temperature rise (C)")
for ax in axes:
    ax.set_xscale("log"); ax.set_xticks([3, 10, 30, 100, 300, 1000]); ax.set_xticklabels(["3", "10", "30", "100", "300", "1000"])
    ax.xaxis.set_minor_formatter(NullFormatter()); ax.set_xlabel("light on the eye (lux)"); ax.grid(alpha=0.3)
axes[0].set_ylabel("motor current (mA)"); axes[0].legend(loc="center left", fontsize=10)
axes[0].set_title("one channel: more light, more current", fontsize=11.5)
axes[1].set_title("heat: worst when the transistor is half on", fontsize=11.5)
save(fig, "fig04-channel-curves.png")

# Figure 4: simulated paths
LAMP = (1.5, 1.0)
fig, ax = plt.subplots(figsize=(10, 6))
for crossed, heading, bias, col, lab in [(True, 0.0, 0.0, BLUE, "crossed (Moth): reaches the lamp in 11.0 s"),
                                         (False, 0.0, 0.0, RED, "straight: turns away, stops in the dark after 4.0 s"),
                                         (True, math.pi, 30.0, GREEN, "crossed + 30 lux bias, lamp behind: circles, finds it in 35.2 s")]:
    path, res = moth_sim.simulate(crossed, LAMP, heading=heading, bias=bias)
    xs, ys = zip(*path)
    ax.plot(xs, ys, color=col, lw=2.3, label=lab)
    ax.plot(xs[-1], ys[-1], "o", color=col, ms=7)
ax.plot(0, 0, "s", color=BLACK, ms=9); ax.text(0.04, -0.12, "start", fontsize=10.5)
ax.add_patch(Circle(LAMP, 0.06, fc="#FFD400", ec=BLACK, zorder=5)); ax.text(LAMP[0] + 0.08, LAMP[1] + 0.06, "lamp", fontsize=11)
ax.set_aspect("equal"); ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)"); ax.grid(alpha=0.3)
ax.legend(loc="lower right", fontsize=10); ax.set_xlim(-0.6, 2.1); ax.set_ylim(-0.9, 1.4)
save(fig, "fig05-paths.png")

# Figure 5: the build, seen from above
fig, ax = plt.subplots(figsize=(8.5, 7))
ax.set_xlim(-5, 5); ax.set_ylim(-5.2, 5.4); ax.set_aspect("equal"); ax.axis("off")
ax.add_patch(FancyBboxPatch((-3.5, -4.2), 7, 8.2, boxstyle="round,pad=0.2", fc="#F3E3C3", ec=BLACK, lw=1.5)); ax.text(0, -4.85, "base: stiff card, plastic or a CD (about 10 x 12 cm)", ha="center", fontsize=10.5)
for sx in (-1, 1):
    ax.add_patch(Rectangle((sx * 3.5 - (0.6 if sx > 0 else -0.6) - 0.45, -2.6), 0.9, 2.4, fc="#333333"))
    ax.add_patch(Rectangle((sx * 2.0 - 0.8, -2.2), 1.6, 1.4, fc=GREY, ec=BLACK)); ax.text(sx * 2.0, -1.5, "motor\n+gear", ha="center", va="center", fontsize=9, color="white")
    ax.add_patch(Rectangle((sx * 1.5 - 0.35, 3.0), 0.7, 1.2, fc=BLACK)); ax.add_patch(Circle((sx * 1.5, 4.2), 0.3, fc="#FFF3B0", ec=BLACK))
    ax.text(sx * 2.6, 3.5, "eye in\na tube", ha="center", fontsize=9.5)
ax.add_patch(Rectangle((-2.0, -0.3), 4.0, 1.8, fc=L_BLUE, ec=BLACK)); ax.text(0, 0.6, "4 x AA battery box\n(with switch)", ha="center", va="center", fontsize=10)
ax.add_patch(Rectangle((-1.6, 1.8), 3.2, 1.0, fc="#C9A26B", ec=BLACK)); ax.text(0, 2.3, "stripboard: 2 channels", ha="center", va="center", fontsize=9.5)
ax.add_patch(Circle((0, -3.5), 0.4, fc="white", ec=BLACK)); ax.text(0.6, -3.6, "ball castor", fontsize=9.5)
ax.annotate("", xy=(0, 5.3), xytext=(0, 4.6), arrowprops=dict(arrowstyle="->", lw=2)); ax.text(0.25, 4.85, "front", fontsize=10)
ax.text(-4.5, -1.2, "wheel", rotation=90, fontsize=10, va="center"); ax.text(4.3, -1.2, "wheel", rotation=90, fontsize=10, va="center")
save(fig, "fig03-build.png")

# Figure 6: Part 5 inside Moth
fig, ax = plt.subplots(figsize=(11, 6))
ax.set_xlim(0, 11); ax.set_ylim(0, 6.2); ax.axis("off")
boxes = [(0.2, 4.6, "Battery 6 V\n(Ch 74, 89)"), (2.4, 4.6, "Switch, 100 uF\n(Ch 83, 84)"), (4.6, 4.6, "LDR divider\n(Ch 79)"),
         (6.8, 4.6, "BD139 gain\n(Ch 87)"), (9.0, 4.6, "Motor\n(Ch 85)"),
         (0.2, 2.6, "Ohm's law\n(Ch 75)"), (2.4, 2.6, "Heat 0.6 W\n(Ch 76)"), (4.6, 2.6, "Series, parallel\n(Ch 77, 78)"),
         (6.8, 2.6, "Flyback diode\n(Ch 86)"), (9.0, 2.6, "Analog control\n(Ch 91)"),
         (2.4, 0.6, "Multimeter tests\n(Ch 81)"), (4.6, 0.6, "Breadboard first\n(Ch 80)"), (6.8, 0.6, "Soldered board\n(Ch 92)")]
for x, y, t in boxes:
    ax.add_patch(FancyBboxPatch((x, y), 1.8, 1.1, boxstyle="round,pad=0.08", fc=L_GREEN if y > 4 else (L_ORANGE if y > 2 else L_BLUE), ec=BLACK))
    ax.text(x + 0.9, y + 0.55, t, ha="center", va="center", fontsize=9.5)
for x in [2.0, 4.2, 6.4, 8.6]:
    ax.annotate("", xy=(x + 0.4, 5.15), xytext=(x, 5.15), arrowprops=dict(arrowstyle="->", lw=1.8))
ax.text(5.5, 6.0, "the energy and signal path (green), the ideas that size it (orange), how it is built (blue)", ha="center", fontsize=10.5)
save(fig, "fig06-part5-in-moth.png")
print("saved 6 figures")
