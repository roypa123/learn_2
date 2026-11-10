# Figures for Chapter 29 — Classes and objects part 2: methods and inheritance.
# Run:  python figures.py      (saves PNG files in ../../images/ch029/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch029")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"
MONO = "DejaVu Sans Mono"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=2.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, color=colour, lw=lw))


def card(ax, x, y, w, h, title, lines, face, tsize=13):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.4))
    ax.text(x + w / 2, y + h - 0.3, title, ha="center", va="center", fontsize=tsize, weight="bold", family=MONO)
    ax.plot([x + 0.1, x + w - 0.1], [y + h - 0.58, y + h - 0.58], color=BLACK, lw=1)
    for i, (t, c) in enumerate(lines):
        ax.text(x + 0.2, y + h - 0.9 - i * 0.4, t, va="center", fontsize=11.5, family=MONO, color=c)


# ---------- Figure 1: inheritance ----------
fig, ax = plt.subplots(figsize=(13.5, 6.4))
card(ax, 4.0, 3.7, 5.4, 2.6, "Robot", [("name, battery_wh", BLACK), ("move(), endurance_min()", BLACK), ("__str__()", BLACK), ("power_w(): 5.0", BLACK)], L_GREY)
card(ax, 0.3, 0.05, 5.3, 2.45, "Rover(Robot)", [("inherits everything", GREY), ("power_w(): 3.78", RED)], L_BLUE)
card(ax, 7.8, 0.05, 5.3, 2.45, "Drone(Robot)", [("inherits everything", GREY), ("mass_kg, altitude_m", GREEN), ("power_w(): depends on mass", RED), ("climb()", GREEN)], L_ORANGE)
arrow(ax, (3.0, 2.6), (5.1, 3.65), BLACK, 2.5); arrow(ax, (10.4, 2.6), (8.3, 3.65), BLACK, 2.5)
ax.text(3.2, 3.3, "is a", fontsize=13, weight="bold", ha="right"); ax.text(10.2, 3.3, "is a", fontsize=13, weight="bold")
ax.text(6.7, 1.75, "red: replaced\n(override)", ha="center", fontsize=12, color=RED, weight="bold")
ax.text(6.7, 0.75, "green: added", ha="center", fontsize=12, color=GREEN, weight="bold")
ax.set_xlim(0, 13.4); ax.set_ylim(-0.1, 6.5); ax.axis("off")
save(fig, "fig01-inheritance.png")

# ---------- Figure 2: one call, different results ----------
fig, ax = plt.subplots(figsize=(13.5, 5.0))
ax.text(1.9, 2.5, "for robot in fleet:\n    robot.power_w()", family=MONO, fontsize=14, weight="bold", va="center", ha="center")
rows = [("Rover", "3.78 W", L_BLUE, 3.9), ("Drone", "150.0 W", L_ORANGE, 2.2), ("Robot", "5.0 W", L_GREY, 0.5)]
for name, res, c, y in rows:
    arrow(ax, (4.2, 2.5), (6.0, y + 0.5), GREY, 2.2)
    ax.add_patch(FancyBboxPatch((6.1, y), 3.1, 1.0, boxstyle="round,pad=0.02,rounding_size=0.1", fc=c, ec=BLACK, lw=1.3))
    ax.text(7.65, y + 0.5, name, ha="center", va="center", fontsize=14, family=MONO, weight="bold")
    arrow(ax, (9.3, y + 0.5), (10.4, y + 0.5), GREEN, 2.5)
    ax.text(10.55, y + 0.5, res, va="center", fontsize=16, family=MONO, weight="bold", color=GREEN)
ax.set_xlim(0, 13); ax.set_ylim(0.2, 5.1); ax.axis("off")
save(fig, "fig02-one-call-different-results.png")

# ---------- Figure 3: composition ----------
fig, ax = plt.subplots(figsize=(13.5, 5.8))
ax.add_patch(FancyBboxPatch((0.3, 0.4), 12.6, 4.9, boxstyle="round,pad=0.02,rounding_size=0.15", fc=L_GREY, ec=BLACK, lw=1.6))
ax.text(6.6, 4.85, "rover = Rover()", ha="center", fontsize=15, family=MONO, weight="bold")
card(ax, 0.8, 1.0, 3.6, 3.0, "self.battery", [("Battery", GREY), ("level_wh", BLACK), ("use()", BLACK), ("percent", BLACK)], L_GREEN)
card(ax, 4.85, 1.0, 3.6, 3.0, "self.left", [("Motor", GREY), ("speed_ms", BLACK), ("(clamped)", BLACK)], L_BLUE)
card(ax, 8.9, 1.0, 3.6, 3.0, "self.right", [("Motor", GREY), ("speed_ms", BLACK), ("(clamped)", BLACK)], L_BLUE)
ax.text(6.6, 0.1, "A Rover HAS a battery and HAS two motors. That is composition, not inheritance.", ha="center", fontsize=13, style="italic")
ax.set_xlim(0, 13.2); ax.set_ylim(-0.1, 5.5); ax.axis("off")
save(fig, "fig03-composition.png")
print("figures saved in", os.path.abspath(OUT))
