# Figures for Chapter 14 — Variables: boxes with names.
# Run:  python figures.py      (saves PNG files in ../../images/ch014/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Polygon

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch014")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"
MONO = "DejaVu Sans Mono"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=GREY, lw=2.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, color=colour, lw=lw))


def var_box(ax, x, y, name, value, face=L_BLUE, w=2.4, h=1.1, size=14, crossed=None):
    # a variable drawn as a box with its value inside and a name label on the front
    ax.add_patch(Rectangle((x, y), w, h, fc=face, ec=BLACK, lw=1.5))
    ax.text(x + w / 2, y + h / 2 + 0.08, value, ha="center", va="center", fontsize=size, family=MONO, weight="bold")
    if crossed is not None:
        ax.text(x + w * 0.18, y + h - 0.22, crossed, ha="center", va="center", fontsize=11, family=MONO, color=GREY)
        ax.plot([x + w * 0.18 - 0.2, x + w * 0.18 + 0.2], [y + h - 0.36, y + h - 0.08], color=RED, lw=2)
    ax.add_patch(FancyBboxPatch((x + 0.2, y - 0.38), w - 0.4, 0.42, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc="white", ec=BLACK, lw=1.2))
    ax.text(x + w / 2, y - 0.17, name, ha="center", va="center", fontsize=11.5, family=MONO)


# ---------- Figure 1: variables are boxes with names ----------
fig, ax = plt.subplots(figsize=(13.5, 5.2))
for i, (n, v) in enumerate([("speed_ms", "0.5"), ("battery_wh", "11.52"), ("ticks", "2000"), ("heading_deg", "90")]):
    var_box(ax, 0.3 + i * 3.3, 2.2, n, v)
ax.text(6.8, 4.15, "Four variables: each is a name (the label) and a value (inside the box)", ha="center",
        fontsize=13.5, weight="bold")
ax.text(1.6, 0.75, "speed_ms = 0.5", fontsize=16, family=MONO, weight="bold", ha="center")
ax.annotate("", xy=(0.25, 0.4), xytext=(3.0, 0.4), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.5))
ax.text(4.0, 0.95, "1. Python works out the RIGHT side first (0.5)", fontsize=12, color=RED)
ax.text(4.0, 0.45, "2. then puts the value in the box named on the LEFT", fontsize=12, color=RED)
ax.text(4.0, -0.05, "'=' means 'store', not 'is equal to'", fontsize=12, color=BLACK, style="italic")
ax.set_xlim(0, 13.6); ax.set_ylim(-0.4, 4.5); ax.axis("off")
save(fig, "fig01-variables-are-boxes.png")

# ---------- Figure 2: ticks = ticks + 1 in three steps ----------
fig, ax = plt.subplots(figsize=(13.5, 4.8))
var_box(ax, 0.3, 1.4, "ticks", "4")
ax.text(1.5, 3.0, "1. READ the box", ha="center", fontsize=12.5, weight="bold", color=BLUE)
arrow(ax, (2.9, 1.95), (4.6, 1.95), BLUE, 2.5)
ax.add_patch(FancyBboxPatch((4.7, 1.45), 2.8, 1.0, boxstyle="round,pad=0.02,rounding_size=0.1", fc=L_ORANGE, ec=BLACK))
ax.text(6.1, 1.95, "4 + 1 = 5", ha="center", va="center", fontsize=15, family=MONO, weight="bold")
ax.text(6.1, 3.0, "2. COMPUTE the right side", ha="center", fontsize=12.5, weight="bold", color=ORANGE)
arrow(ax, (7.6, 1.95), (9.3, 1.95), GREEN, 2.5)
var_box(ax, 9.4, 1.4, "ticks", "5", face=L_GREEN, crossed="4")
ax.text(10.6, 3.0, "3. STORE the new value", ha="center", fontsize=12.5, weight="bold", color=GREEN)
ax.text(6.8, 0.25, "ticks = ticks + 1        (short way:  ticks += 1)", ha="center", fontsize=15, family=MONO)
ax.text(6.8, -0.35, "the old value 4 is gone: a box holds only ONE value", ha="center", fontsize=12, style="italic")
ax.set_xlim(0, 13.4); ax.set_ylim(-0.6, 3.4); ax.axis("off")
save(fig, "fig02-update-in-three-steps.png")

# ---------- Figure 3: naming rules ----------
fig, ax = plt.subplots(figsize=(13.5, 6.4))
good = [("battery_wh", "letters, digits and _"), ("motor2_speed", "a digit, but not first"),
        ("_count", "may start with _"), ("MAX_SPEED_MS", "capitals: a constant"), ("heading_deg", "the unit in the name")]
bad = [("2nd_motor", "starts with a digit"), ("motor-speed", "'-' means minus"), ("max speed", "no spaces allowed"),
       ("class", "a keyword"), ("speed$", "only letters, digits, _")]
ax.text(3.3, 6.0, "ALLOWED", ha="center", fontsize=15, weight="bold", color=GREEN)
ax.text(10.1, 6.0, "NOT ALLOWED (SyntaxError)", ha="center", fontsize=15, weight="bold", color=RED)
for i, (n, why) in enumerate(good):
    y = 5.0 - i * 1.0
    ax.add_patch(FancyBboxPatch((0.2, y - 0.32), 6.2, 0.64, boxstyle="round,pad=0.02,rounding_size=0.1", fc=L_GREEN, ec=GREEN))
    ax.text(0.45, y, n, va="center", fontsize=13.5, family=MONO, weight="bold")
    ax.text(3.45, y, why, va="center", fontsize=11.5)
for i, (n, why) in enumerate(bad):
    y = 5.0 - i * 1.0
    ax.add_patch(FancyBboxPatch((7.0, y - 0.32), 6.2, 0.64, boxstyle="round,pad=0.02,rounding_size=0.1", fc=L_RED, ec=RED))
    ax.text(7.25, y, n, va="center", fontsize=13.5, family=MONO, weight="bold")
    ax.text(10.15, y, why, va="center", fontsize=11.5)
ax.text(6.7, -0.15, "And: Speed, speed and SPEED are THREE different names (Python is case-sensitive)", ha="center",
        fontsize=12.5, style="italic")
ax.set_xlim(0, 13.4); ax.set_ylim(-0.5, 6.4); ax.axis("off")
save(fig, "fig03-naming-rules.png")

# ---------- Figure 4: Rover's state after each leg ----------
fig, ax = plt.subplots(figsize=(13, 7.2))
for gx in range(0, 4):
    ax.plot([gx, gx], [-0.5, 2.5], color=L_GREY, lw=1, zorder=0)
for gy in range(0, 3):
    ax.plot([-0.5, 3.5], [gy, gy], color=L_GREY, lw=1, zorder=0)
ax.plot([0, 2, 2], [0, 0, 1.5], color=BLUE, lw=2.5, ls="--", zorder=1)


def rover(ax, x, y, heading):
    # a simple Rover seen from above: orange body with a pointed front; heading in compass degrees
    a = math.radians(90 - heading)
    fx, fy = math.cos(a), math.sin(a)
    sx, sy = -fy, fx
    s = 0.17
    pts = [(x + fx * s * 1.6, y + fy * s * 1.6), (x + fx * s * 0.4 + sx * s, y + fy * s * 0.4 + sy * s),
           (x - fx * s + sx * s, y - fy * s + sy * s), (x - fx * s - sx * s, y - fy * s - sy * s),
           (x + fx * s * 0.4 - sx * s, y + fy * s * 0.4 - sy * s)]
    ax.add_patch(Polygon(pts, closed=True, fc=ORANGE, ec=BLACK, lw=1.3, zorder=3))


for (x, y, h) in [(0, 0, 90), (2, 0, 90), (2, 1.5, 0)]:
    rover(ax, x, y, h)
states = [(-0.45, -1.95, "start", "x_m = 0.0   y_m = 0.0\nheading_deg = 90\nbattery_wh = 11.52\nodometer_m = 0.0"),
          (2.0, -1.95, "after leg 1 (2 m east)", "x_m = 2.0   y_m = 0.0\nheading_deg = 90\nbattery_wh = 11.5116\nodometer_m = 2.0"),
          (2.6, 1.0, "after leg 2 (turn left, 1.5 m north)", "x_m = 2.0   y_m = 1.5\nheading_deg = 0\nbattery_wh = 11.5053\nodometer_m = 3.5")]
for (bx, by, title, txt) in states:
    ax.text(bx, by + 0.85, title, fontsize=11.5, weight="bold")
    ax.text(bx, by, txt, fontsize=11, family=MONO, bbox=dict(boxstyle="round,pad=0.4", fc=L_BLUE, ec=BLACK))
ax.text(-0.45, 2.85, "Rover's STATE = the values of its state variables at one moment", fontsize=13.5, weight="bold")
ax.text(3.55, -0.05, "x (m)", fontsize=11, color=GREY)
ax.text(-0.45, 2.45, "y (m)", fontsize=11, color=GREY)
ax.set_xlim(-0.6, 5.9); ax.set_ylim(-2.2, 3.1); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig04-rover-state.png")

# ---------- Figure 5: the swap puzzle ----------
fig, axes = plt.subplots(1, 2, figsize=(14.5, 6.4), gridspec_kw={"width_ratios": [1, 2.0]})
ax = axes[0]
ax.text(2.4, 6.1, "WRONG: two steps", ha="center", fontsize=14, weight="bold", color=RED)
rows = [("start", "5", "6"), ("left_pin = right_pin", "6", "6"), ("right_pin = left_pin", "6", "6")]
for i, (code, a, b) in enumerate(rows):
    y = 4.3 - i * 1.9
    var_box(ax, 0.2, y, "left_pin", a, w=1.9, h=0.9, size=13)
    var_box(ax, 2.6, y, "right_pin", b, w=1.9, h=0.9, size=13)
    ax.text(2.4, y + 1.1, code, ha="center", fontsize=11, family=MONO, color=BLACK)
ax.text(2.4, -0.55, "the 5 is lost in step 1!", ha="center", fontsize=12, color=RED, weight="bold")
ax.set_xlim(0, 4.8); ax.set_ylim(-0.9, 6.5); ax.axis("off")
ax = axes[1]
ax.text(4.9, 6.1, "RIGHT: a spare box called temp", ha="center", fontsize=14, weight="bold", color=GREEN)
rows = [("start", "5", "6", ""), ("1. temp = left_pin", "5", "6", "5"), ("2. left_pin = right_pin", "6", "6", "5"),
        ("3. right_pin = temp", "6", "5", "5")]
for i, (code, a, b, t) in enumerate(rows):
    y = 4.75 - i * 1.55
    var_box(ax, 0.2, y, "left_pin", a, w=1.9, h=0.8, size=13)
    var_box(ax, 2.6, y, "right_pin", b, w=1.9, h=0.8, size=13)
    var_box(ax, 5.0, y, "temp", t, face=L_ORANGE, w=1.6, h=0.8, size=13)
    ax.text(6.9, y + 0.4, code, va="center", fontsize=11.5, family=MONO)
ax.text(4.9, -0.55, "Python's short way:  left_pin, right_pin = right_pin, left_pin", ha="center", fontsize=12,
        family=MONO, color=GREEN, weight="bold")
ax.set_xlim(0, 10.2); ax.set_ylim(-0.9, 6.5); ax.axis("off")
save(fig, "fig05-swap-puzzle.png")

# ---------- Figure 6: names are labels on values ----------
fig, axes = plt.subplots(1, 3, figsize=(14, 4.6))
steps = [("a = 5", [("a", 5)]), ("b = a", [("a", 5), ("b", 5)]), ("a = 7", [("a", 7), ("b", 5)])]
for ax, (code, tags) in zip(axes, steps):
    ax.text(2.0, 3.6, code, ha="center", fontsize=16, family=MONO, weight="bold")
    vals = sorted(set(v for _, v in tags))
    pos = {v: (1.0 + i * 2.0, 1.0) for i, v in enumerate(vals)}
    for v, (vx, vy) in pos.items():
        ax.add_patch(FancyBboxPatch((vx - 0.45, vy - 0.4), 0.9, 0.8, boxstyle="round,pad=0.02,rounding_size=0.15",
                                    fc=L_BLUE, ec=BLACK, lw=1.4))
        ax.text(vx, vy, str(v), ha="center", va="center", fontsize=16, family=MONO, weight="bold")
    used = {}
    for name, v in tags:
        vx, vy = pos[v]
        k = used.get(v, 0)
        used[v] = k + 1
        tx = vx - 0.55 + k * 1.1 if len([t for t in tags if t[1] == v]) > 1 else vx
        ax.add_patch(FancyBboxPatch((tx - 0.3, 2.35), 0.6, 0.5, boxstyle="round,pad=0.02,rounding_size=0.1",
                                    fc=L_ORANGE, ec=BLACK))
        ax.text(tx, 2.6, name, ha="center", va="center", fontsize=14, family=MONO, weight="bold")
        ax.plot([tx, vx], [2.35, vy + 0.42], color=ORANGE, lw=2)
    ax.set_xlim(-0.2, 4.2); ax.set_ylim(0.2, 4.0); ax.axis("off")
fig.text(0.5, -0.04, "A name is a label tied to a value. 'b = a' ties b to the SAME value as a. "
         "Moving the label a later does not move b.", ha="center", fontsize=12.5, style="italic")
save(fig, "fig06-names-are-labels.png")
print("figures saved in", os.path.abspath(OUT))
