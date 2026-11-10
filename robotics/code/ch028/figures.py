# Figures for Chapter 28 — Classes and objects part 1: a Robot class.
# Run:  python figures.py      (saves PNG files in ../../images/ch028/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Polygon

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch028")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"
MONO = "DejaVu Sans Mono"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=2.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=15, color=colour, lw=lw))


def card(ax, x, y, w, h, title, lines, face, tsize=13):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.4))
    ax.text(x + w / 2, y + h - 0.32, title, ha="center", va="center", fontsize=tsize, weight="bold", family=MONO)
    ax.plot([x + 0.1, x + w - 0.1], [y + h - 0.62, y + h - 0.62], color=BLACK, lw=1)
    for i, t in enumerate(lines):
        ax.text(x + 0.2, y + h - 0.95 - i * 0.42, t, va="center", fontsize=11.5, family=MONO)


# ---------- Figure 1: class and objects ----------
fig, ax = plt.subplots(figsize=(13.5, 6.0))
card(ax, 0.2, 0.75, 4.5, 4.75, "class Robot", ["data each robot has:", "  name, x_m, y_m,", "  heading_deg,", "  battery_wh", "", "what each robot can do:", "  drive()", "  turn()", "  status()"], L_GREY)
ax.text(2.45, 0.42, "the BLUEPRINT: it is not a robot yet", ha="center", fontsize=12.5, style="italic")
card(ax, 7.3, 3.2, 5.6, 2.3, 'rover = Robot("rover")', ["name = 'rover'", "x_m = 1.5   y_m = 2.0", "heading_deg = 90"], L_BLUE, 12)
card(ax, 7.3, 0.4, 5.6, 2.3, 'cart = Robot("cart", x_m=5.0)', ["name = 'cart'", "x_m = 5.0   y_m = -1.0", "heading_deg = 180"], L_ORANGE, 12)
arrow(ax, (4.8, 3.9), (7.2, 4.4), GREY, 3); arrow(ax, (4.8, 2.6), (7.2, 1.6), GREY, 3)
ax.text(6.0, 3.0, "makes", ha="center", fontsize=13, weight="bold", color=GREY)
ax.set_xlim(0, 13.1); ax.set_ylim(0.15, 5.7); ax.axis("off")
save(fig, "fig01-class-and-objects.png")

# ---------- Figure 2: what self means ----------
fig, ax = plt.subplots(figsize=(13.5, 4.6))
ax.text(0.3, 3.6, "rover.drive(2.0)", family=MONO, fontsize=18, weight="bold", va="center")
ax.text(0.3, 1.35, "def drive(self, distance_m):", family=MONO, fontsize=18, weight="bold", va="center")
arrow(ax, (1.0, 3.25), (3.0, 1.72), BLUE, 3)
arrow(ax, (2.9, 3.25), (5.2, 1.72), GREEN, 3)
ax.text(0.1, 2.45, "the object\nbefore the dot\nbecomes self", fontsize=12.5, color=BLUE, weight="bold", ha="left", va="center")
ax.text(5.0, 2.75, "the argument in the brackets\nbecomes distance_m", fontsize=13, color=GREEN, weight="bold", ha="left", va="center")
ax.text(0.3, 0.45, "Inside drive, self.x_m means THIS robot's x_m.", fontsize=14, style="italic")
ax.set_xlim(0, 12.5); ax.set_ylim(0.1, 4.1); ax.axis("off")
save(fig, "fig02-what-self-means.png")

# ---------- Figure 3: two robots on a floor ----------
fig, ax = plt.subplots(figsize=(9.5, 7.0))
for g in range(0, 7):
    ax.plot([g, g], [-1.5, 2.8], color=L_GREY, lw=1, zorder=0)
for g in range(-1, 3):
    ax.plot([-0.5, 6.5], [g, g], color=L_GREY, lw=1, zorder=0)


def bot(ax, x, y, h, c):
    s = 0.17
    if h == 0:
        pts = [(x, y + 0.28), (x - s, y), (x - s, y - s), (x + s, y - s), (x + s, y)]
    elif h == 90:
        pts = [(x + 0.28, y), (x, y + s), (x - s, y + s), (x - s, y - s), (x, y - s)]
    else:
        pts = [(x, y - 0.28), (x - s, y), (x - s, y + s), (x + s, y + s), (x + s, y)]
    ax.add_patch(Polygon(pts, closed=True, fc=c, ec=BLACK, lw=1.3, zorder=3))


ax.plot([0, 0, 1.5], [0, 2, 2], color=BLUE, lw=2.5, ls="--", zorder=1)
ax.plot([5, 5], [0, -1], color=RED, lw=2.5, ls="--", zorder=1)
bot(ax, 1.5, 2, 90, ORANGE); bot(ax, 5, -1, 180, L_ORANGE)
ax.plot(0, 0, "o", color=GREY, ms=9, zorder=2); ax.plot(5, 0, "o", color=GREY, ms=9, zorder=2)
ax.text(0.1, -0.35, "rover starts", fontsize=11.5, ha="left"); ax.text(4.85, 0.18, "cart starts", fontsize=11.5, ha="right")
ax.text(2.0, 2.3, "rover: (1.50, 2.00), facing 90", fontsize=12.5, weight="bold", color=BLUE)
ax.text(4.85, -1.35, "cart: (5.00, -1.00), facing 180", fontsize=12.5, weight="bold", color=RED, ha="right")
ax.set_xlim(-0.7, 6.6); ax.set_ylim(-1.7, 3.0); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig03-two-robots.png")

# ---------- Figure 4: a filter object remembers ----------
fig, ax = plt.subplots(figsize=(13.5, 5.2))
ax.text(0.3, 5.0, "front = MovingAverage(3)", family=MONO, fontsize=13.5, weight="bold", color=BLUE)
ax.text(0.3, 2.45, "left = MovingAverage(5)", family=MONO, fontsize=13.5, weight="bold", color=ORANGE)
for i, v in enumerate([11, 30, 10]):
    ax.add_patch(Rectangle((0.5 + i * 1.1, 3.6), 1.1, 0.9, fc=L_BLUE, ec=BLACK))
    ax.text(1.05 + i * 1.1, 4.05, str(v), ha="center", va="center", fontsize=14, family=MONO, weight="bold")
for i, v in enumerate([52, 51, 49, 50, 48]):
    ax.add_patch(Rectangle((0.5 + i * 1.1, 1.05), 1.1, 0.9, fc=L_ORANGE, ec=BLACK))
    ax.text(1.05 + i * 1.1, 1.5, str(v), ha="center", va="center", fontsize=14, family=MONO, weight="bold")
ax.text(4.2, 4.05, "self.history: only the last 3 readings", fontsize=12.5, va="center")
ax.text(6.4, 1.5, "self.history: only the last 5 readings", fontsize=12.5, va="center")
arrow(ax, (0.5, 3.35), (2.5, 3.35), GREY, 1.8); ax.text(1.5, 3.08, "older     newer", fontsize=11, ha="center", color=GREY)
ax.text(6.6, 0.45, "two objects, two separate memories, one piece of code", ha="center", fontsize=13, style="italic")
ax.set_xlim(0, 13.3); ax.set_ylim(0.2, 5.4); ax.axis("off")
save(fig, "fig04-objects-remember.png")
print("figures saved in", os.path.abspath(OUT))
