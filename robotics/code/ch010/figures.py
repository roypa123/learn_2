# Figures for Chapter 10 — Your first robot on paper: designing a tiny cleaning robot.
# Run:  python figures.py      (saves PNG files in ../../images/ch010/)
import math
import os
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Wedge, Arc

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch010")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
PURPLE, SKY = "#CC79A7", "#56B4E9"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, face, size=11):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size)


def arrow(ax, p, q, colour=GREY, lw=2.0, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=15, color=colour, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}"))


def line(ax, pts, colour=BLACK, lw=3.0, ls="-"):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=colour, lw=lw, ls=ls, solid_capstyle="round")


# ---------- Figure 1: the design loop ----------
fig, ax = plt.subplots(figsize=(13, 6.5))
steps = [(0.0, 4.2, "1. REQUIREMENTS\nwhat must it do?\n(with numbers)", L_ORANGE),
         (4.4, 4.2, "2. IDEAS\nseveral ways\nto do it", L_GREY),
         (8.8, 4.2, "3. CHOOSE\ncompare ideas\n(score table, Ch 4)", L_GREY),
         (8.8, 0.6, "4. DETAILS\nparts, block diagram,\npower, behaviour, safety", L_BLUE),
         (4.4, 0.6, "5. CHECK\ncalculate + simulate:\ndoes it meet 1?", L_GREEN),
         (0.0, 0.6, "6. IMPROVE\nfix what failed,\nthen check again", L_RED)]
for x, y, t, c in steps:
    box(ax, x, y, 3.4, 1.7, t, c, 11.5)
arrow(ax, (3.4, 5.05), (4.4, 5.05)); arrow(ax, (7.8, 5.05), (8.8, 5.05))
arrow(ax, (10.5, 4.2), (10.5, 2.3)); arrow(ax, (8.8, 1.45), (7.8, 1.45)); arrow(ax, (4.4, 1.45), (3.4, 1.45))
arrow(ax, (1.7, 2.3), (1.7, 4.2), RED, 2.5)
ax.text(1.85, 3.25, "go round again", color=RED, fontsize=11, style="italic")
ax.text(6.1, 3.25, "all PASS -> build it\n(or, in this chapter: done on paper)", ha="center", fontsize=11, color=GREEN, weight="bold")
ax.text(6.1, 6.5, "The engineering design loop: it is a control loop for designs", ha="center", fontsize=13.5, weight="bold")
ax.set_xlim(-0.2, 12.4); ax.set_ylim(0.3, 6.9); ax.axis("off")
save(fig, "fig01-design-loop.png")

# ---------- Figure 2: top view of the robot ----------
fig, ax = plt.subplots(figsize=(10, 10))
ax.add_patch(Circle((0, 0), 10, fc=L_ORANGE, ec=BLACK, lw=2))                      # body (orange = robot)
ax.add_patch(Wedge((0, 0), 10.6, 15, 165, width=0.6, fc=GREY, ec=BLACK))             # bumper, front half
for sx in (-1, 1):
    ax.add_patch(Rectangle((sx * 8.2 - 1.0, -2.5), 2.0, 5.0, fc=BLACK))              # wheels on the centre line
ax.plot([-7.2, 7.2], [0, 0], color=GREY, ls="--", lw=1)
ax.add_patch(Circle((0, 6.8), 1.0, fc=GREY, ec=BLACK))                                # caster in front
ax.add_patch(Rectangle((-5.5, -6.2), 11, 2.0, fc=L_BLUE, ec=BLACK, hatch="///"))     # brush behind the wheels
ax.add_patch(Rectangle((-4.5, -9.2), 9, 2.6, fc="white", ec=BLACK))                 # dust bin
ax.add_patch(Rectangle((-3.5, 1.0), 7, 2.8, fc=L_GREEN, ec=BLACK))                  # battery
ax.add_patch(Circle((0, -2.0), 1.3, fc=RED, ec=BLACK, lw=1.5))                       # stop button
for px, py in [(-4.5, 7.6), (4.5, 7.6), (-8.0, 3.8), (8.0, 3.8)]:
    ax.add_patch(Circle((px, py), 0.55, fc=PURPLE, ec=BLACK))                         # cliff sensors
ax.plot(0, 0.9, marker="+", color=BLACK, ms=14, mew=2)
notes = [((0, 10.6), (6.5, 13.0), "bumper (front half, 2 switches)"),
         ((4.5, 7.6), (9.5, 10.2), "cliff sensor (4: purple dots)"),
         ((-1.0, 6.8), (-17.5, 11.5), "caster ball"),
         ((8.2, -2.5), (11.5, -6.0), "drive wheel (2), on the\ncentre line: turns on the spot"),
         ((-5.5, -5.2), (-20.5, -8.5), "brush (16 cm wide)"),
         ((0, -8.0), (5.5, -13.0), "dust bin"),
         ((-3.5, 2.4), (-20.5, 5.0), "battery: 4 x AA NiMH"),
         ((-1.3, -2.0), (-20.5, -3.0), "red STOP button on top"),
         ((0, 0.9), (11.0, 1.5), "centre of mass (+)")]
for xy, xt, t in notes:
    ax.annotate(t, xy=xy, xytext=xt, fontsize=11, arrowprops=dict(arrowstyle="->", color=BLACK, lw=1))
ax.annotate("", xy=(0, 14.5), xytext=(0, 11.5), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.5))
ax.text(0.6, 13.2, "forward", color=BLUE, fontsize=12, weight="bold")
ax.annotate("", xy=(-10, -11.2), xytext=(10, -11.2), arrowprops=dict(arrowstyle="<->", color=BLACK))
ax.text(0, -12.3, "20 cm", ha="center", fontsize=11)
ax.set_xlim(-21, 18); ax.set_ylim(-14, 15.5); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("Tiny cleaner, seen from above (8 cm tall)", fontsize=13)
save(fig, "fig02-top-view.png")

# ---------- Figure 3: block diagram ----------
fig, ax = plt.subplots(figsize=(14, 7.5))
box(ax, 0.0, 3.4, 1.9, 1.2, "BATTERY\n4 x AA NiMH\n4.8 V", L_GREEN, 10.5)
box(ax, 2.5, 3.5, 1.9, 1.0, "SWITCH +\n3 A FUSE", "white", 10.5)
box(ax, 5.2, 5.3, 2.0, 1.0, "5 V\nREGULATOR", L_GREY, 10.5)
box(ax, 8.2, 5.0, 2.4, 1.6, "BRAIN\nArduino Nano", L_ORANGE, 11)
box(ax, 5.2, 1.4, 2.0, 1.0, "STOP\nbutton", L_RED, 10.5)
box(ax, 8.2, 1.2, 2.4, 1.4, "MOTOR DRIVER\nTB6612 + MOSFET", L_GREEN, 10.5)
box(ax, 11.6, 2.2, 2.0, 0.9, "2 DRIVE\nMOTORS", L_GREEN, 10.5)
box(ax, 11.6, 0.6, 2.0, 0.9, "BRUSH\nMOTOR", L_GREEN, 10.5)
box(ax, 11.6, 6.3, 2.2, 0.8, "2 BUMPERS", L_BLUE, 10.5)
box(ax, 11.6, 5.2, 2.2, 0.8, "4 CLIFF\nSENSORS", L_BLUE, 10.5)
box(ax, 11.6, 4.1, 2.2, 0.8, "2 ENCODERS", L_BLUE, 10.5)
box(ax, 8.6, 7.1, 1.6, 0.6, "BUZZER", L_GREY, 10)
line(ax, [(1.9, 4.0), (2.5, 4.0)]); line(ax, [(4.4, 4.0), (4.8, 4.0), (4.8, 5.8), (5.2, 5.8)])
line(ax, [(7.2, 5.8), (8.2, 5.8)])
line(ax, [(4.8, 4.0), (4.8, 1.9), (5.2, 1.9)], GREEN); line(ax, [(7.2, 1.9), (8.2, 1.9)], GREEN)
line(ax, [(10.6, 1.9), (11.1, 1.9), (11.1, 2.65), (11.6, 2.65)], GREEN); line(ax, [(11.1, 1.9), (11.1, 1.05), (11.6, 1.05)], GREEN)
for yy in (6.7, 5.6, 4.5):
    arrow(ax, (11.6, yy), (10.6, min(max(yy, 5.2), 6.4)), BLUE, 1.8)
arrow(ax, (9.4, 5.0), (9.4, 2.6), BLUE, 1.8); ax.text(9.5, 3.7, "speed and\ndirection", color=BLUE, fontsize=10)
arrow(ax, (9.4, 6.6), (9.4, 7.1), BLUE, 1.8)
ax.plot([6.2, 6.2, 7.9, 7.9, 8.2], [2.4, 3.3, 3.3, 5.4, 5.4], color=BLUE, lw=1.8, ls="--")
ax.text(6.3, 3.45, "'stop pressed'", color=BLUE, fontsize=10)
ax.text(0.0, 8.2, "Thick black = power for the electronics.  Green = motor power (the STOP button cuts it).  Blue = signals.",
        fontsize=11.5)
ax.set_xlim(-0.2, 14.2); ax.set_ylim(0.3, 8.6); ax.axis("off")
save(fig, "fig03-block-diagram.png")

# ---------- Figure 4: behaviours with priorities ----------
fig, ax = plt.subplots(figsize=(13, 6.8))
beh = [("1. CLIFF!", "a cliff sensor sees no floor", "stop, reverse 5 cm, turn away", RED),
       ("2. BUMP", "a bumper is pressed", "reverse 3 cm, turn a random angle", ORANGE),
       ("3. BATTERY LOW", "battery below 4.4 V", "stop the brush, beep, stop", PURPLE),
       ("4. CLEAN", "always (if nothing above)", "brush on, drive forward 0.2 m/s", GREEN)]
for i, (name, when, does, col) in enumerate(beh):
    y = 5.0 - i * 1.45
    ax.add_patch(FancyBboxPatch((0.0, y), 2.8, 1.05, boxstyle="round,pad=0.02", fc=col, ec=BLACK, alpha=0.85))
    ax.text(1.4, y + 0.52, name, ha="center", va="center", fontsize=12.5, weight="bold", color="white")
    ax.text(3.1, y + 0.72, "WHEN: " + when, fontsize=11.5, va="center")
    ax.text(3.1, y + 0.3, "DOES: " + does, fontsize=11.5, va="center")
    arrow(ax, (8.3, y + 0.52), (9.4, 3.1), GREY, 1.5)
box(ax, 9.4, 2.5, 2.4, 1.2, "MOTORS\n+ BRUSH", L_GREEN, 12)
ax.annotate("", xy=(-0.4, 6.1), xytext=(-0.4, 0.75), arrowprops=dict(arrowstyle="-|>", color=BLACK, lw=2))
ax.text(-0.6, 3.4, "more important", rotation=90, ha="right", va="center", fontsize=11.5)
ax.text(5.5, 6.55, "Every loop (50 per second): the highest behaviour whose WHEN is true gets the motors", ha="center",
        fontsize=12.5, weight="bold")
ax.set_xlim(-1.3, 12.1); ax.set_ylim(0.5, 6.9); ax.axis("off")
save(fig, "fig04-behaviours.png")

# ---------- simulations (same models as clean_sim.py and lawnmower.py) ----------
W, H, CELL = 4.0, 3.0, 0.05
COLS, ROWS = int(W / CELL), int(H / CELL)


def sweep(clean, x, y, br=0.08):
    n = 0
    for r in range(int((y - br) / CELL), int((y + br) / CELL) + 1):
        for c in range(int((x - br) / CELL), int((x + br) / CELL) + 1):
            cx, cy = (c + 0.5) * CELL, (r + 0.5) * CELL
            if (cx - x) ** 2 + (cy - y) ** 2 <= br ** 2 and not clean[r][c]:
                clean[r][c] = True
                n += 1
    return n


random.seed(3)
clean_r = [[False] * COLS for _ in range(ROWS)]
x, y, hd, cnt = 0.5, 0.5, 30.0, 0
path_r, cov_r = [(x, y)], []
for step in range(18001):
    nx = x + 0.02 * math.cos(math.radians(hd)); ny = y + 0.02 * math.sin(math.radians(hd))
    if nx < 0.1 or nx > W - 0.1 or ny < 0.1 or ny > H - 0.1:
        hd += random.uniform(90, 270)
    else:
        x, y = nx, ny
    cnt += sweep(clean_r, x, y)
    path_r.append((x, y)); cov_r.append(100 * cnt / (COLS * ROWS))


def mower(fix):
    plan, yr, right = [], 0.1, True
    while yr <= H - 0.1:
        plan += [(0.1, yr), (W - 0.1, yr)] if right else [(W - 0.1, yr), (0.1, yr)]
        right = not right; yr += 0.15
    if fix and plan[-1][1] < H - 0.1:
        plan += [(0.1, H - 0.1), (W - 0.1, H - 0.1)] if right else [(W - 0.1, H - 0.1), (0.1, H - 0.1)]
    clean = [[False] * COLS for _ in range(ROWS)]
    x, y = plan[0]; tgt, cnt, cov, path = 1, 0, [], [(x, y)]
    while tgt < len(plan):
        tx, ty = plan[tgt]; d = math.hypot(tx - x, ty - y)
        if d <= 0.02:
            x, y = tx, ty; tgt += 1
        else:
            x += 0.02 * (tx - x) / d; y += 0.02 * (ty - y) / d
        cnt += sweep(clean, x, y)
        cov.append(100 * cnt / (COLS * ROWS)); path.append((x, y))
    return clean, cov, path


clean_m, cov_m, path_m = mower(False)
clean_f, cov_f, path_f = mower(True)


def show_map(ax, clean, path, title, lw=0.4, col=BLUE):
    ax.imshow([[1 if v else 0 for v in row] for row in clean], origin="lower", extent=(0, W, 0, H),
              cmap=matplotlib.colors.ListedColormap(["#8C6D46", "#F4F1E8"]), vmin=0, vmax=1)
    ax.plot([p[0] for p in path], [p[1] for p in path], color=col, lw=lw, alpha=0.6)
    ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect("equal")
    ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)"); ax.set_title(title)


# ---------- Figure 5: random bounce map ----------
fig, axes = plt.subplots(1, 2, figsize=(15, 5.6))
idx5 = 5 * 600
c5 = [[False] * COLS for _ in range(ROWS)]
for (px, py) in path_r[1:idx5 + 2]:
    sweep(c5, px, py)
show_map(axes[0], c5, path_r[:idx5 + 2], f"After 5 minutes: {cov_r[idx5]:.1f}% clean")
show_map(axes[1], clean_r, path_r, f"After 30 minutes: {cov_r[-1]:.1f}% clean", lw=0.15)
axes[0].plot(0.5, 0.5, marker="s", color=ORANGE, ms=10); axes[0].text(0.6, 0.25, "dock (start)", color=BLACK, fontsize=10)
save(fig, "fig05-random-map.png")

# ---------- Figure 6: lawnmower maps ----------
fig, axes = plt.subplots(1, 2, figsize=(15, 5.6))
show_map(axes[0], clean_m, path_m, f"Rows as planned: {cov_m[-1]:.1f}% clean in {len(cov_m) / 600:.1f} min", lw=1.0)
axes[0].annotate("a dirty strip: the plan\nstopped one row too early", xy=(2.0, 2.95), xytext=(1.0, 1.9), fontsize=11,
                 color=RED, weight="bold", bbox=dict(fc="white", ec=RED), arrowprops=dict(arrowstyle="->", color=RED, lw=2))
show_map(axes[1], clean_f, path_f, f"With one extra row at the wall: {cov_f[-1]:.1f}% in {len(cov_f) / 600:.1f} min", lw=1.0)
save(fig, "fig06-lawnmower-map.png")

# ---------- Figure 7: coverage over time ----------
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot([i / 600 for i in range(len(cov_r))], cov_r, color=ORANGE, lw=2.5, label="bump and turn (random)")
ax.plot([i / 600 for i in range(len(cov_m))], cov_m, color=BLUE, lw=2.5, label="rows (lawnmower), as planned")
ax.plot([i / 600 for i in range(len(cov_f))], cov_f, color=GREEN, lw=2.0, ls="--", label="rows, with the extra row")
ax.axhline(90, color=BLACK, ls="--", lw=1.5, label="requirement: 90% in 30 min")
ax.axvline(30, color=GREY, ls=":", lw=1.5)
ax.set_xlabel("time (minutes)"); ax.set_ylabel("floor cleaned (%)")
ax.set_xlim(0, 31); ax.set_ylim(0, 102); ax.grid(alpha=0.3); ax.legend(loc="lower right", fontsize=11)
ax.set_title("How fast does each strategy clean the room?")
save(fig, "fig07-coverage-vs-time.png")

# ---------- Figure 8: Part 1 in one picture ----------
fig, ax = plt.subplots(figsize=(14, 8))
nodes = [(6.0, 7.2, "Ch 1: how to learn\n(notebook, folders, rules)", L_GREY),
         (1.2, 5.5, "Ch 2: what is a robot\nsense-think-act, loops", L_ORANGE),
         (6.0, 5.5, "Ch 3: history\n(ideas keep coming back)", L_GREY),
         (10.8, 5.5, "Ch 4: kinds of robots\nDOF, stability, energy", L_ORANGE),
         (1.2, 3.1, "Ch 5: parts\nbody, sensors, brain,\nactuators, power", L_BLUE),
         (6.0, 3.1, "Ch 6: control loop\nerror, gain, delay", L_BLUE),
         (10.8, 3.1, "Ch 7: safety\nfuse, e-stop, watchdog,\nlayers", L_RED),
         (1.2, 0.7, "Ch 8: your computer\nPython, terminal, errors", L_GREEN),
         (10.8, 0.7, "Ch 9: simulation or\nhardware, reality gap,\nbudget", L_GREEN)]
for x, y, t, c in nodes:
    box(ax, x - 1.7, y - 0.6, 3.4, 1.2, t, c, 10.5)
ax.add_patch(Circle((6.0, 0.9), 1.05, fc=ORANGE, ec=BLACK, lw=2))
ax.text(6.0, 0.9, "Ch 10\nTINY\nCLEANER", ha="center", va="center", fontsize=11.5, weight="bold")
for x, y, _, _ in nodes:
    if (x, y) != (6.0, 7.2):
        ax.plot([x, 6.0], [y - 0.6 if y > 1 else y, 1.95 if y > 1 else 0.9], color=GREY, lw=1.2, ls="--", zorder=0)
ax.text(6.0, 8.3, "Part 1 in one picture: every chapter feeds the design of the tiny cleaner", ha="center",
        fontsize=13.5, weight="bold")
ax.set_xlim(-0.8, 12.8); ax.set_ylim(-0.4, 8.7); ax.axis("off")
save(fig, "fig08-part1-map.png")
print("figures saved in", os.path.abspath(OUT))
