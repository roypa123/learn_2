# Figures for Chapter 39 - Units and measurement.
# Run:  python figures.py      (saves PNG files in ../../images/ch039/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle, Circle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch039")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=2.2):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, color=colour, lw=lw, shrinkA=0, shrinkB=0, zorder=3))


def box(ax, x, y, w, h, text, face, size=12):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size)


# Figure 1: multiply by one
fig, ax = plt.subplots(figsize=(12, 3.6))
ax.text(0.8, 1.5, "3 km", fontsize=20, ha="center", va="center", weight="bold")
ax.text(1.75, 1.5, "x", fontsize=18, ha="center", va="center")
ax.text(3.4, 2.1, "1000 m", fontsize=19, ha="center", va="center", color=BLUE)
ax.plot([2.4, 4.4], [1.5, 1.5], color=BLACK, lw=2)
ax.text(3.4, 0.9, "1 km", fontsize=19, ha="center", va="center", color=BLUE)
ax.plot([0.45, 1.15], [1.25, 1.75], color=RED, lw=2.5); ax.plot([2.95, 3.85], [0.65, 1.15], color=RED, lw=2.5)
ax.text(5.3, 1.5, "=", fontsize=20, ha="center", va="center")
ax.text(6.6, 1.5, "3000 m", fontsize=20, ha="center", va="center", weight="bold")
ax.text(9.8, 1.5, "The blue fraction equals 1:\n1000 m and 1 km are the same length.\nkm on top cancels km below.", fontsize=12.5, ha="center", va="center")
ax.set_xlim(0, 12); ax.set_ylim(0.4, 2.7); ax.axis("off")
save(fig, "fig01-multiply-by-one.png")

# Figure 2: ruler with cm and inch
fig, ax = plt.subplots(figsize=(12, 3.8))
ax.add_patch(Rectangle((0, 0), 15.5, 2.2, fc=L_ORANGE, ec=BLACK))
for i in range(0, 156):
    x = i / 10
    h = 0.55 if i % 10 == 0 else (0.38 if i % 5 == 0 else 0.22)
    ax.plot([x, x], [2.2, 2.2 - h], color=BLACK, lw=1)
    if i % 10 == 0:
        ax.text(x, 1.35, str(i // 10), ha="center", fontsize=11.5)
for i in range(0, 25):
    x = i * 2.54 / 4
    if x > 15.5:
        break
    h = 0.55 if i % 4 == 0 else 0.25
    ax.plot([x, x], [0, h], color=BLUE, lw=1.2)
    if i % 4 == 0:
        ax.text(x, 0.65, str(i // 4), ha="center", fontsize=11.5, color=BLUE)
ax.text(15.7, 1.6, "cm", fontsize=13, va="center"); ax.text(15.7, 0.4, "inches", fontsize=13, va="center", color=BLUE)
ax.set_xlim(-0.3, 17); ax.set_ylim(-0.2, 2.4); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig02-ruler.png")

# Figure 3: thermometer scales
fig, ax = plt.subplots(figsize=(11, 5))
xs = [1.5, 5, 8.5]
names = ["Celsius", "Kelvin", "Fahrenheit"]
marks = [("water boils", 100, 373.15, 212), ("robot motor limit", 80, 353.15, 176), ("room", 25, 298.15, 77), ("water freezes", 0, 273.15, 32), ("cold night", -40, 233.15, -40)]
for x, n in zip(xs, names):
    ax.add_patch(Rectangle((x - 0.1, -50), 0.2, 165, fc=L_GREY, ec=BLACK))
    ax.text(x, 123, n, ha="center", fontsize=13.5, weight="bold")
for name, c, k, f in marks:
    ax.plot([0.9, 9.1], [c, c], color=GREY, ls=":", lw=1.3, zorder=0)
    ax.text(0, c, name, ha="center", va="center", fontsize=11.5)
    ax.text(xs[0] + 0.25, c + 3.5, f"{c} C", fontsize=12); ax.text(xs[1] + 0.25, c + 3.5, f"{k:.2f} K", fontsize=12); ax.text(xs[2] + 0.25, c + 3.5, f"{f} F", fontsize=12)
ax.set_xlim(-1.2, 10.6); ax.set_ylim(-55, 132); ax.axis("off")
save(fig, "fig03-temperature.png")

# Figure 4: the conversion pipeline
fig, ax = plt.subplots(figsize=(13.5, 3.5))
items = [("3.0 mph\nspeed", L_GREY), ("1.341 m/s\nSI speed", L_BLUE), ("2.101 turns/s\nof the wheel", L_BLUE), ("126.1 rpm\nof the wheel", L_BLUE), ("3782 rpm\nof the motor", L_GREEN)]
labels = ["x 0.44704", "/ 0.6384 m", "x 60", "x 30"]
for i, (t, face) in enumerate(items):
    x = i * 2.75
    box(ax, x, 1.2, 2.0, 1.2, t, face)
    if i < 4:
        arrow(ax, (x + 2.05, 1.8), (x + 2.72, 1.8))
        ax.text(x + 2.38, 0.85, labels[i], ha="center", fontsize=11.5)
ax.set_xlim(-0.1, 13.2); ax.set_ylim(0.6, 2.6); ax.axis("off")
save(fig, "fig04-pipeline.png")

# Figure 5: the orbit that went too low (schematic)
fig, ax = plt.subplots(figsize=(9.5, 6.2))
ax.add_patch(Circle((0, 0), 3.0, fc=L_RED, ec=BLACK, lw=1.5)); ax.text(0, 0, "Mars", ha="center", va="center", fontsize=15)
ax.add_patch(Circle((0, 0), 3.33, fc="none", ec=GREY, ls="--", lw=1.5))
xs_p, ys_p, xs_a, ys_a = [], [], [], []
for t in [i / 100 for i in range(-160, 161)]:
    r_plan = 4.2 * (1 + 0.65) / (1 + 0.65 * math.cos(t))
    xs_p.append(r_plan * math.sin(t)); ys_p.append(r_plan * math.cos(t) * -1)
    r_act = 3.2 * (1 + 0.65) / (1 + 0.65 * math.cos(t))
    xs_a.append(r_act * math.sin(t)); ys_a.append(r_act * math.cos(t) * -1)
ax.plot(xs_p, ys_p, color=BLACK, ls="--", lw=2.5, label="planned path")
ax.plot(xs_a, ys_a, color=BLUE, lw=2.5, label="path actually flown")
ax.text(0, -3.65, "too low", color=BLUE, fontsize=12.5, ha="center", va="top", bbox=dict(fc="white", ec="none", pad=1))
ax.text(4.2, 2.3, "grey dashed circle:\nthick part of the air", fontsize=12, color="#555555")
ax.set_xlim(-7, 8); ax.set_ylim(-5.4, 6); ax.set_aspect("equal"); ax.axis("off"); ax.legend(loc="upper left")
save(fig, "fig05-orbit.png")

# Figure 6: reading between marks
fig, ax = plt.subplots(figsize=(11, 3.6))
ax.add_patch(Rectangle((2, 0), 8, 1.2, fc=L_ORANGE, ec=BLACK))
for i in range(0, 41):
    x = 2 + i * 0.2
    h = 0.55 if i % 10 == 0 else (0.38 if i % 5 == 0 else 0.22)
    ax.plot([x, x], [1.2, 1.2 - h], color=BLACK, lw=1.2)
    if i % 10 == 0:
        ax.text(x, 0.35, f"{i // 10}", ha="center", fontsize=12)
ax.add_patch(Rectangle((2, 1.2), 5.26, 0.5, fc=L_GREY, ec=BLACK)); ax.text(4.6, 1.45, "the part being measured", ha="center", va="center", fontsize=12)
ax.plot([7.26, 7.26], [0.2, 2.15], color=RED, lw=2)
ax.text(7.26, 2.25, "about 2.63 cm", color=RED, ha="center", fontsize=13)
ax.text(10.2, 0.7, "each small mark\nis 1 mm", fontsize=12, va="center")
ax.set_xlim(1.6, 12.2); ax.set_ylim(0, 2.7); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig06-reading.png")
print("figures saved in", os.path.abspath(OUT))
