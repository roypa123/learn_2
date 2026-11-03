# Figures for Chapter 1 — How to use this book.
# Run:  python figures.py      (saves PNG files in ../../images/ch001/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch001")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12})

# Colour-blind safe colours (Okabe–Ito), used the same way in the whole course.
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
LIGHT = {"Beginner": "#BFE3F5", "Middle": "#FBE3B3", "Advanced": "#BDEBDD"}


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, face, size=10, edge=BLACK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=face, ec=edge, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, wrap=True)


# ---------- Figure 1: the course map (33 parts) ----------
parts = [
    "Welcome", "Python", "School\nmaths", "Physics", "Electronics", "Arduino", "Sensors", "Motors",
    "Linear\nalgebra", "Calculus", "Probability",
    "Control 1\nPID", "Control 2\nclassical", "Control 3\nLQR, MPC", "Mobile\nrobots", "Frames",
    "Arms: FK", "Arms: IK", "Dynamics", "Trajectories",
    "Estimation", "Maps,\nSLAM", "Planning", "Vision", "Machine\nlearning", "Real-time,\nCAN", "Linux,\nROS 2",
    "Simulators", "ROS 2 in\npractice", "Drones", "Legged\nrobots", "Humanoids", "Final\nprojects",
]
level = ["Beginner"] * 11 + ["Middle"] * 9 + ["Advanced"] * 13
fig, ax = plt.subplots(figsize=(14, 7.2))
per_row, w, h = 11, 1.05, 0.8
centres = []
for i, (name, lv) in enumerate(zip(parts, level)):
    row, col = divmod(i, per_row)
    if row % 2 == 1:
        col = per_row - 1 - col          # snake: every second row goes right to left
    x, y = col * 1.25, -row * 1.6
    box(ax, x, y, w, h, f"{i + 1}\n{name}", LIGHT[lv], size=9)
    centres.append((x + w / 2, y + h / 2))
for (x1, y1), (x2, y2) in zip(centres, centres[1:]):
    if abs(y1 - y2) < 0.1:
        sx = 1 if x2 > x1 else -1
        a = FancyArrowPatch((x1 + sx * w / 2, y1), (x2 - sx * w / 2, y2), arrowstyle="-|>", mutation_scale=12, color=GREY)
    else:
        a = FancyArrowPatch((x1, y1 - h / 2), (x2, y2 + h / 2), arrowstyle="-|>", mutation_scale=12, color=GREY)
    ax.add_patch(a)
for k, lv in enumerate(LIGHT):
    ax.add_patch(FancyBboxPatch((k * 3.2, 1.2), 0.5, 0.4, boxstyle="round,pad=0.02", fc=LIGHT[lv], ec=BLACK))
    ax.text(k * 3.2 + 0.65, 1.4, lv, va="center", fontsize=12)
ax.text(0, 2.0, "START here (Part 1)", fontsize=12, color=BLUE, weight="bold")
ax.set_xlim(-0.3, 13.7); ax.set_ylim(-4.0, 2.4); ax.axis("off")
save(fig, "fig01-course-map.png")

# ---------- Figure 2: the parts of every chapter ----------
sections = [
    ("Title, 'You need', 'You will make'", "Start"),
    ("What you will learn", "Start"),
    ("New words", "Start"),
    ("Theory sections: example → picture → maths → small example", "Theory"),
    ("Code + line-by-line table + output", "Theory"),
    ("Small examples (at least 5)", "Theory"),
    ("Real robot applications", "Use"),
    ("Hands-on lab (simulation / hardware)", "Use"),
    ("Experiments (core parts)", "Use"),
    ("Common mistakes", "Check"),
    ("Practice + Answers", "Check"),
    ("Summary + Next chapter", "End"),
]
colour = {"Start": "#DDDDDD", "Theory": LIGHT["Beginner"], "Use": LIGHT["Middle"], "Check": LIGHT["Advanced"], "End": "#DDDDDD"}
fig, ax = plt.subplots(figsize=(9, 8))
for i, (txt, grp) in enumerate(sections):
    y = -i * 0.75
    box(ax, 0, y, 7.4, 0.6, txt, colour[grp], size=11)
    if i:
        ax.add_patch(FancyArrowPatch((3.7, y + 0.75), (3.7, y + 0.6), arrowstyle="-|>", mutation_scale=10, color=GREY))
groups = [("START", 0, 2), ("THEORY\n(learn it)", 3, 5), ("USE IT\n(apply + build)", 6, 8), ("CHECK\nyourself", 9, 10), ("END", 11, 11)]
for label, a, b in groups:
    top, bottom = -a * 0.75 + 0.6, -b * 0.75
    ax.plot([7.7, 7.8, 7.8, 7.7], [top, top, bottom, bottom], color=BLACK)
    ax.text(7.95, (top + bottom) / 2, label, va="center", fontsize=12, weight="bold")
ax.set_xlim(-0.2, 10.2); ax.set_ylim(-8.6, 0.9); ax.axis("off")
save(fig, "fig02-chapter-parts.png")

# ---------- Figure 3: how a plot is read (a robot drives, stops, drives again) ----------
t = [i / 10 for i in range(0, 111)]
def distance(s):
    if s <= 5: return 0.2 * s                 # 0.2 m every second for 5 s
    if s <= 8: return 1.0                      # stopped for 3 s
    return 1.0 + 0.4 * (s - 8)                 # 0.4 m every second for 3 s
d = [distance(s) for s in t]
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(t, d, color=BLUE, lw=2.5, label="robot position")
ax.set_xlabel("time (seconds)"); ax.set_ylabel("distance from start (metres)")
ax.grid(alpha=0.3); ax.set_xlim(0, 11); ax.set_ylim(0, 2.4)
ax.annotate("A: driving slowly\n(0.2 m each second)", xy=(2.5, 0.5), xytext=(0.3, 1.5), arrowprops=dict(arrowstyle="->"))
ax.annotate("B: stopped\n(flat line)", xy=(6.5, 1.0), xytext=(5.2, 0.3), arrowprops=dict(arrowstyle="->"))
ax.annotate("C: driving faster\n(steeper line)", xy=(9.5, 1.6), xytext=(8.0, 2.1), arrowprops=dict(arrowstyle="->"))
ax.legend(loc="lower right")
save(fig, "fig03-read-a-plot.png")

# ---------- Figure 4: the two tracks of every lab ----------
fig, ax = plt.subplots(figsize=(11, 5))
box(ax, 3.6, 3.6, 3.8, 0.9, "The idea of the chapter", "#DDDDDD", size=13)
box(ax, 0, 1.6, 4.6, 1.3, "SIMULATION track (always)\nPython, Wokwi, simulators\nfree, safe, on any computer", LIGHT["Beginner"], size=12)
box(ax, 6.4, 1.6, 4.6, 1.3, "HARDWARE track (optional)\nreal parts, wiring, building\ncosts money, needs care", LIGHT["Middle"], size=12)
box(ax, 3.6, -0.4, 3.8, 0.9, "You understand it", LIGHT["Advanced"], size=13)
for (x1, y1, x2, y2) in [(5.5, 3.6, 2.3, 2.9), (5.5, 3.6, 8.7, 2.9), (2.3, 1.6, 5.5, 0.5), (8.7, 1.6, 5.5, 0.5)]:
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=14, color=GREY, lw=1.5))
ax.text(5.5, 2.25, "same\nresult", ha="center", va="center", fontsize=11, style="italic")
ax.set_xlim(-0.3, 11.3); ax.set_ylim(-0.6, 4.7); ax.axis("off")
save(fig, "fig04-two-tracks.png")

# ---------- Figure 5: Rover grows with you ----------
stages = [("drives", 281), ("counts", 288), ("feels", 291), ("races", 294), ("navigates", 298), ("maze", 313),
          ("sees", 498), ("maps", 447), ("ROS 2", 579), ("HomeBot", 612), ("delivers", 747), ("arm", 749)]
fig, ax = plt.subplots(figsize=(13, 3.6))
ax.plot([0, 11], [0, 0], color=GREY, lw=3, zorder=0)
for i, (name, ch) in enumerate(stages):
    ax.scatter(i, 0, s=420, color=ORANGE, edgecolor=BLACK, zorder=2)
    ax.text(i, 0, str(i + 1), ha="center", va="center", fontsize=11, weight="bold", zorder=3)
    ax.text(i, 0.45 if i % 2 == 0 else -0.55, f"{name}\nCh {ch}", ha="center", va="center", fontsize=11)
ax.set_xlim(-0.7, 11.7); ax.set_ylim(-1.1, 1.0); ax.axis("off")
ax.set_title("Rover, the main robot, in 12 stages", fontsize=13)
save(fig, "fig05-rover-stages.png")

# ---------- Figure 6: how long the course takes ----------
total = 749
paces = [3, 5, 7, 10]
years = [total / p / 52 for p in paces]
fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.bar([f"{p} chapters\na week" for p in paces], years, color=[GREY, BLUE, GREEN, ORANGE], edgecolor=BLACK)
for b, y in zip(bars, years):
    ax.text(b.get_x() + b.get_width() / 2, y + 0.08, f"{y:.1f} years", ha="center", fontsize=12)
ax.set_ylabel("years to finish all 749 chapters"); ax.set_ylim(0, 5.6); ax.grid(axis="y", alpha=0.3)
save(fig, "fig06-study-pace.png")

print("saved 6 figures in", os.path.normpath(OUT))
