# Figures for Chapter 4 — Kinds of robots.
# Run:  python figures.py      (saves PNG files in ../../images/ch004/)
import os
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle, Polygon

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch004")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, face, size=11):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size)


def arrow(ax, p, q, colour=GREY, lw=1.5):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=14, color=colour, lw=lw))


# ---------- Figure 1: the robot family ----------
fig, ax = plt.subplots(figsize=(14, 7.5))
box(ax, 5.6, 6.3, 2.8, 0.8, "ROBOTS", L_GREY, 14)
groups = [
    ("FIXED\n(stay in one place)", 0.3, L_ORANGE, ["arms: articulated,\nSCARA, delta, gantry", "cobots (work\nnext to people)"]),
    ("ON THE GROUND", 3.8, L_BLUE, ["wheeled", "tracked", "legged", "humanoid"]),
    ("IN THE AIR", 7.3, L_GREEN, ["multirotor\n(drones)", "fixed-wing", "VTOL"]),
    ("IN WATER", 10.8, L_BLUE, ["remotely operated\n(ROV)", "autonomous\n(AUV)", "boats"]),
]
for title, x, face, items in groups:
    box(ax, x, 4.7, 2.9, 0.9, title, face, 12)
    arrow(ax, (7.0, 6.3), (x + 1.45, 5.6))
    for k, item in enumerate(items):
        box(ax, x + 0.2, 3.6 - k * 1.0, 2.5, 0.8, item, "white", 11)
box(ax, 0.3, -1.2, 13.4, 1.1, "SPECIAL KINDS (can mix with the above):\nsoft robots  •  mobile manipulators (arm on a base)  •  "
    "snake robots  •  exoskeletons  •  swarms  •  tiny robots", L_GREY, 12)
ax.set_xlim(0, 14); ax.set_ylim(-1.4, 7.3); ax.axis("off")
save(fig, "fig01-robot-family.png")

# ---------- Figure 2: four kinds of robot arm (stick drawings) ----------
fig, axs = plt.subplots(1, 4, figsize=(16, 5))
# (a) articulated arm, side view
ax = axs[0]
pts = [(0, 0), (0, 1.0)]
a1, a2 = math.radians(50), math.radians(-40)
p2 = (pts[1][0] + 1.4 * math.cos(a1), pts[1][1] + 1.4 * math.sin(a1)); pts.append(p2)
p3 = (p2[0] + 1.2 * math.cos(a1 + a2), p2[1] + 1.2 * math.sin(a1 + a2)); pts.append(p3)
ax.add_patch(Rectangle((-0.4, -0.2), 0.8, 0.2, fc=GREY))
xs, ys = zip(*pts); ax.plot(xs, ys, "-", color=ORANGE, lw=8, solid_capstyle="round")
ax.plot(xs[1:], ys[1:], "o", color=BLACK, ms=10)
ax.text(-0.1, 1.15, "shoulder", ha="right"); ax.text(p2[0], p2[1] + 0.2, "elbow", ha="center"); ax.text(p3[0] + 0.15, p3[1], "wrist + tool")
ax.set_title("(a) articulated arm\n(side view, like a human arm)")
ax.set_xlim(-1.2, 3.4); ax.set_ylim(-0.4, 3.2)
# (b) SCARA, top view
ax = axs[1]
b1, b2 = math.radians(30), math.radians(70)
q1 = (1.4 * math.cos(b1), 1.4 * math.sin(b1)); q2 = (q1[0] + 1.2 * math.cos(b1 + b2), q1[1] + 1.2 * math.sin(b1 + b2))
ax.add_patch(Circle((0, 0), 0.3, fc=GREY))
ax.plot([0, q1[0], q2[0]], [0, q1[1], q2[1]], "-", color=ORANGE, lw=8, solid_capstyle="round")
ax.plot([0, q1[0], q2[0]], [0, q1[1], q2[1]], "o", color=BLACK, ms=10)
ax.text(q2[0], q2[1] + 0.25, "tool moves\nup and down here", ha="center", fontsize=10.5)
ax.set_title("(b) SCARA\n(top view: swings flat, fast)")
ax.set_xlim(-1.0, 2.6); ax.set_ylim(-0.8, 2.8)
# (c) gantry / cartesian
ax = axs[2]
ax.add_patch(Rectangle((0, 0), 3.0, 2.2, fc="none", ec=GREY, lw=4))
ax.plot([1.6, 1.6], [0, 2.2], color=ORANGE, lw=7)
ax.add_patch(Rectangle((1.4, 1.1), 0.4, 0.4, fc=ORANGE, ec=BLACK))
arrow(ax, (0.5, -0.35), (2.5, -0.35), BLACK); ax.text(1.5, -0.65, "x", ha="center")
arrow(ax, (3.3, 0.3), (3.3, 1.9), BLACK); ax.text(3.45, 1.1, "y")
ax.text(1.6, 2.45, "tool also moves up/down (z)", ha="center", fontsize=10.5)
ax.set_title("(c) gantry / cartesian\n(top view: straight lines, like a 3D printer)")
ax.set_xlim(-0.5, 3.9); ax.set_ylim(-0.9, 2.9)
# (d) delta, side view
ax = axs[3]
ax.add_patch(Polygon([[0.2, 2.6], [2.8, 2.6], [2.5, 2.3], [0.5, 2.3]], fc=GREY))
for top, elbow in [((0.6, 2.3), (0.1, 1.5)), ((2.4, 2.3), (2.9, 1.5)), ((1.5, 2.3), (1.5, 1.6))]:
    ax.plot([top[0], elbow[0]], [top[1], elbow[1]], color=ORANGE, lw=6)
    ax.plot([elbow[0], 1.5 + (elbow[0] - 1.5) * 0.15], [elbow[1], 0.4], color=ORANGE, lw=3)
ax.add_patch(Rectangle((1.3, 0.25), 0.4, 0.15, fc=ORANGE, ec=BLACK))
ax.text(1.5, 0.0, "light tool plate:\nvery fast picking", ha="center", va="top", fontsize=10.5)
ax.set_title("(d) delta\n(side view: three arms from above)")
ax.set_xlim(-0.4, 3.4); ax.set_ylim(-0.7, 2.9)
for ax in axs:
    ax.set_aspect("equal"); ax.axis("off")
fig.tight_layout()
save(fig, "fig02-arm-types.png")

# ---------- Figure 3: four kinds of wheeled / tracked bases (top view) ----------
fig, axs = plt.subplots(1, 4, figsize=(16, 5))
def body(ax, w=1.6, h=2.0):
    ax.add_patch(Rectangle((-w / 2, -h / 2), w, h, fc=ORANGE, ec=BLACK, alpha=0.8))
def wheel(ax, x, y, w=0.25, h=0.6, angle=0):
    r = Rectangle((x - w / 2, y - h / 2), w, h, fc=BLACK)
    if angle:
        import matplotlib.transforms as mt
        r.set_transform(mt.Affine2D().rotate_deg_around(x, y, angle) + ax.transData)
    ax.add_patch(r)
# (a) differential drive
ax = axs[0]; ax.add_patch(Circle((0, 0), 1.0, fc=ORANGE, ec=BLACK, alpha=0.8))
wheel(ax, -0.9, 0); wheel(ax, 0.9, 0); ax.add_patch(Circle((0, -0.75), 0.12, fc=GREY, ec=BLACK))
arrow(ax, (0, 0.2), (0, 1.5), BLUE, 2.5); ax.text(0.1, 1.55, "forward", color=BLUE)
ax.add_patch(FancyArrowPatch((0.6, 1.2), (-0.6, 1.2), connectionstyle="arc3,rad=0.4", arrowstyle="-|>",
                             mutation_scale=14, color=GREEN, lw=2))
ax.text(0, -1.45, "turns on the spot\n(2 motors)", ha="center")
ax.set_title("(a) differential drive\n(Rover, robot vacuum)")
# (b) car-like (Ackermann)
ax = axs[1]; body(ax)
wheel(ax, -0.85, -0.7); wheel(ax, 0.85, -0.7); wheel(ax, -0.85, 0.7, angle=20); wheel(ax, 0.85, 0.7, angle=20)
ax.add_patch(FancyArrowPatch((0, 1.1), (-0.8, 1.7), connectionstyle="arc3,rad=0.2", arrowstyle="-|>",
                             mutation_scale=14, color=BLUE, lw=2.5))
ax.text(0, -1.45, "must drive to turn,\ncannot turn on the spot", ha="center")
ax.set_title("(b) car-like (Ackermann)\n(Racer, self-driving cars)")
# (c) mecanum
ax = axs[2]; body(ax)
for x, y, s in [(-0.85, 0.7, 1), (0.85, 0.7, -1), (-0.85, -0.7, -1), (0.85, -0.7, 1)]:
    wheel(ax, x, y, w=0.3)
    for k in (-0.2, 0, 0.2):
        ax.plot([x - 0.12, x + 0.12], [y + k - 0.1 * s, y + k + 0.1 * s], color="white", lw=1.5)
arrow(ax, (0.2, 0), (1.6, 0), BLUE, 2.5); ax.text(1.2, 0.15, "sideways!", color=BLUE)
ax.text(0, -1.45, "moves in any direction\n(4 motors)", ha="center")
ax.set_title("(c) mecanum wheels\n(Glide, factory platforms)")
# (d) tracked
ax = axs[3]; body(ax, 1.2)
for x in (-0.85, 0.85):
    ax.add_patch(Rectangle((x - 0.2, -1.1), 0.4, 2.2, fc=GREY, ec=BLACK))
    for k in range(-5, 6):
        ax.plot([x - 0.2, x + 0.2], [k * 0.2, k * 0.2], color=BLACK, lw=1)
ax.text(0, -1.45, "grips rough ground,\nskids when it turns", ha="center")
ax.set_title("(d) tracked / skid-steer\n(rescue robots, diggers)")
for ax in axs:
    ax.set_xlim(-1.9, 1.9); ax.set_ylim(-1.9, 2.0); ax.set_aspect("equal"); ax.axis("off")
fig.tight_layout()
save(fig, "fig03-wheeled-types.png")

# ---------- Figure 4: feet on the ground and balance (support polygons) ----------
fig, axs = plt.subplots(1, 3, figsize=(15, 5))
cases = [("2 legs (humanoid)\none foot lifted", [(-0.15, 0.2), (0.15, 0.2), (0.15, -0.2), (-0.15, -0.2)], (0.45, 0.0), False),
         ("4 legs (Quad)\nback-right leg lifted, body shifted away", [(-0.8, 0.8), (0.8, 0.8), (-0.8, -0.8)], (-0.3, 0.25), True),
         ("6 legs (insect-like)\nthree legs lifted", [(-0.8, 0.9), (0.9, 0.0), (-0.8, -0.9)], (0.0, 0.0), True)]
for ax, (title, feet, com, stable) in zip(axs, cases):
    ax.add_patch(Polygon(feet, fc=L_GREEN if stable else L_ORANGE, ec=BLACK, lw=1.5, alpha=0.8))
    for f in feet:
        ax.scatter(*f, s=120, color=BLACK, zorder=3)
    ax.scatter(*com, s=220, color=RED, marker="X", zorder=4)
    ax.text(com[0] + 0.12, com[1] + 0.12, "centre of mass", color=RED, fontsize=11)
    ax.set_title(title + ("\nSTABLE: the red X is inside" if stable else "\nfalls unless it keeps moving:\nthe red X is outside"),
                 fontsize=12)
    ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3); ax.set_aspect("equal"); ax.axis("off")
fig.tight_layout()
save(fig, "fig04-support-polygons.png")

# ---------- Figure 5: same battery, three kinds of robot (from robot_range.py) ----------
kinds = ["wheeled", "legged", "flying"]
power = [10, 40, 150]; speed = [1.0, 1.0, 10.0]
minutes = [50 / p * 60 for p in power]
km = [v * 50 / p * 3600 / 1000 for v, p in zip(speed, power)]
fig, axs = plt.subplots(1, 2, figsize=(12, 4.8))
for ax, values, label, fmt in [(axs[0], minutes, "time on one 50 Wh battery (minutes)", "{:.0f} min"),
                               (axs[1], km, "distance on one 50 Wh battery (km)", "{:.1f} km")]:
    bars = ax.bar(kinds, values, color=[BLUE, GREEN, ORANGE], edgecolor=BLACK)
    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, v * 1.02, fmt.format(v), ha="center", fontsize=12)
    ax.set_ylabel(label); ax.grid(axis="y", alpha=0.3); ax.set_ylim(0, max(values) * 1.18)
fig.tight_layout()
save(fig, "fig05-battery-time-range.png")

# ---------- Figure 6: the decision scores (from choose_robot.py) ----------
scores = [[5, 1, 2, 4, 5, 5, 4, 5], [4, 2, 4, 3, 4, 4, 5, 4], [4, 5, 5, 2, 2, 1, 2, 3], [5, 5, 5, 5, 1, 3, 1, 1]]
jobs = [("warehouse\ntransport", [5, 0, 0, 3, 5, 4, 5, 4]), ("plant with\nstairs", [2, 5, 3, 1, 3, 1, 1, 3]),
        ("survey a big\nfarm field", [1, 0, 3, 5, 3, 3, 0, 1])]
names = ["wheeled", "tracked", "legged", "flying"]
table = [[sum(s * w for s, w in zip(scores[k], wts)) for _, wts in jobs] for k in range(4)]
fig, ax = plt.subplots(figsize=(9, 5.5))
im = ax.imshow(table, cmap="Blues", vmin=30, vmax=130)
ax.set_xticks(range(3)); ax.set_xticklabels([j for j, _ in jobs])
ax.set_yticks(range(4)); ax.set_yticklabels(names)
for k in range(4):
    for j in range(3):
        best = table[k][j] == max(table[r][j] for r in range(4))
        ax.text(j, k, str(table[k][j]) + (" ★" if best else ""), ha="center", va="center", fontsize=13,
                color="white" if table[k][j] > 95 else BLACK, weight="bold" if best else "normal")
ax.set_title("weighted score (higher = better fit, ★ = best for that job)")
fig.colorbar(im, ax=ax, shrink=0.8)
save(fig, "fig06-decision-scores.png")

# ---------- Figure 7: how many motors do the robots in this course have? ----------
robots = ["Rover", "Racer", "Scribe", "Hover", "Glide", "Six", "Quad", "Buddy"]
motors = [2, 2, 3, 4, 4, 6, 12, 18]
colours = [BLUE, BLUE, ORANGE, GREEN, BLUE, ORANGE, RED, RED]
fig, ax = plt.subplots(figsize=(11, 4.8))
bars = ax.bar(robots, motors, color=colours, edgecolor=BLACK)
for b, m in zip(bars, motors):
    ax.text(b.get_x() + b.get_width() / 2, m + 0.3, str(m), ha="center", fontsize=12)
ax.set_ylabel("number of motors (actuators)"); ax.set_ylim(0, 21); ax.grid(axis="y", alpha=0.3)
ax.set_yticks(range(0, 21, 2))
handles = [Rectangle((0, 0), 1, 1, fc=c, ec=BLACK) for c in (BLUE, ORANGE, GREEN, RED)]
ax.legend(handles, ["wheeled", "arm", "flying", "legged / humanoid"], loc="upper left")
save(fig, "fig07-motor-counts.png")

print("saved 7 figures in", os.path.normpath(OUT))
