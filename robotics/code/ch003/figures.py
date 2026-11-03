# Figures for Chapter 3 — A short history of robots.
# Run:  python figures.py      (saves PNG files in ../../images/ch003/)
import os
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle, Polygon

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch003")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"
KIND = {"S": (BLUE, "new way to SENSE"), "T": (ORANGE, "new way to THINK"), "A": (GREEN, "new way to ACT")}


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, face, size=11):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size)


# ---------- Figure 1: timeline in three panels ----------
panels = [
    # (year, text, kind, level, shift): level = which row the label sits in (+ above, - below),
    # shift = move the label sideways (in years) so labels do not overlap
    ("Long ago: water, weights and gears", -300, 1820, [
        (-250, "Ctesibius: water clock\nwith a float regulator", "T", 1, 0),
        (60, "Hero: a cart programmed\nwith ropes", "T", -1, 0),
        (1206, "Al-Jazari: book of\nautomata, camshafts", "A", 1, 0),
        (1495, "Leonardo: a mechanical\nknight (design)", "A", -1, -120),
        (1774, "Jaquet-Droz:\n'The Writer'", "T", 2, -230),
        (1788, "Watt: speed governor\n(feedback)", "S", -2, 0),
        (1804, "Jacquard: loom with\npunched cards", "T", 1, 60)]),
    ("1820–1960: electricity, the word 'robot', control theory", 1820, 1965, [
        (1868, "Maxwell: maths of\ngovernors (stability)", "T", 1, 0),
        (1921, "R.U.R.: the word\n'robot' on stage", "T", -1, 0),
        (1942, "Asimov: three laws\n(in a story)", "T", 1, -4),
        (1949, "Grey Walter's\ntortoises: light sensors", "S", -2, -8),
        (1960, "Kalman filter", "S", 2, 0),
        (1961, "Unimate: first factory\nrobot arm at work", "A", -1, 6)]),
    ("1960–today: computers, AI, robots everywhere", 1960, 2026, [
        (1966, "Shakey: a robot\nthat plans (A*)", "T", 1, 0),
        (1973, "WABOT-1: humanoid\nthat walks a little", "A", -1, 0),
        (1997, "Sojourner on Mars", "S", 1, -4),
        (2000, "ASIMO walks; surgical\nrobot approved (US)", "A", -1, -4),
        (2002, "Robot vacuums\nin homes", "S", 2, 0),
        (2005, "Robot cars finish a\n212 km desert race", "T", -2, 3),
        (2010, "ROS: shared\nrobot software", "T", 1, 4),
        (2021, "A helicopter flies\non Mars", "A", -1, 0)]),
]
fig, axes = plt.subplots(3, 1, figsize=(15, 15))
for ax, (title, a, b, events) in zip(axes, panels):
    ax.plot([a, b], [0, 0], color=BLACK, lw=2)
    for year, text, kind, level, shift in events:
        colour = KIND[kind][0]
        up = 1 if level > 0 else -1
        y_text = up * (0.45 + 1.25 * (abs(level) - 1))
        ax.plot([year, year + shift], [0, y_text], color=colour, lw=2)
        ax.scatter(year, 0, s=80, color=colour, edgecolor=BLACK, zorder=3)
        label = f"{abs(year)} BC" if year < 0 else str(year)
        if year == -250: label = "about 250 BC"
        if year == 60: label = "about 60 AD"
        ax.text(year + shift, y_text, f"{label}\n{text}", ha="center", va="bottom" if up > 0 else "top",
                fontsize=10.5, bbox=dict(fc="white", ec=colour, lw=1.2, boxstyle="round,pad=0.3"))
    ax.set_xlim(a - (b - a) * 0.08, b + (b - a) * 0.08); ax.set_ylim(-2.9, 2.9)
    ax.set_title(title, fontsize=13, loc="left"); ax.axis("off")
handles = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=c, markeredgecolor=BLACK, markersize=11, label=t)
           for c, t in KIND.values()]
fig.legend(handles=handles, loc="upper right", fontsize=12)
fig.tight_layout()
save(fig, "fig01-timeline.png")

# ---------- Figure 2: the float regulator (Ctesibius) ----------
fig, ax = plt.subplots(figsize=(10, 6.5))
ax.add_patch(Rectangle((0, 3.2), 3.0, 1.6, fc=L_BLUE, ec=BLACK, lw=1.5))                  # supply tank
ax.text(1.5, 4.95, "supply tank (water level changes)", ha="center")
ax.add_patch(Rectangle((1.3, 2.4), 0.4, 0.8, fc=L_BLUE, ec=BLACK))                        # pipe down
ax.add_patch(Rectangle((0.2, 0.0), 3.0, 2.2, fc="white", ec=BLACK, lw=1.5))               # regulating vessel
ax.add_patch(Rectangle((0.2, 0.0), 3.0, 1.3, fc=L_BLUE, ec="none"))
ax.add_patch(Polygon([[1.25, 2.4], [1.75, 2.4], [1.5, 1.85]], fc=ORANGE, ec=BLACK))        # cone valve on the float
ax.add_patch(Rectangle((1.1, 1.1), 0.8, 0.35, fc=ORANGE, ec=BLACK))                       # float
ax.plot([1.5, 1.5], [1.45, 1.85], color=BLACK, lw=2)
ax.annotate("float with a\ncone on top", xy=(1.1, 1.3), xytext=(-2.6, 1.6), fontsize=11,
            arrowprops=dict(arrowstyle="->"))
ax.add_patch(Rectangle((3.2, 0.25), 1.2, 0.25, fc=L_BLUE, ec=BLACK))                      # outflow
ax.add_patch(Rectangle((4.6, -1.2), 1.6, 3.0, fc="white", ec=BLACK, lw=1.5))              # clock vessel
ax.add_patch(Rectangle((4.6, -1.2), 1.6, 1.2, fc=L_BLUE, ec="none"))
ax.text(5.4, 1.95, "clock vessel:\nwater rises at a\nsteady speed = time", ha="center", va="bottom", fontsize=11)
ax.text(1.7, -0.25, "regulating vessel:\nlevel stays the same", ha="center", va="top", fontsize=11)
for t, yy in [("level too LOW → float drops → valve opens → more water in", 6.6),
              ("level too HIGH → float rises → cone closes the pipe → less water in", 6.1),
              ("so the level stays steady, and the clock runs at a steady speed", 5.6)]:
    ax.text(7.0, yy - 1.7, t, fontsize=11)
ax.set_xlim(-2.8, 15.5); ax.set_ylim(-1.5, 5.4); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig02-float-regulator.png")

# ---------- Figure 3: the governor as a sense-think-act loop ----------
fig, ax = plt.subplots(figsize=(11, 5.5))
box(ax, 0.0, 2.4, 3.0, 1.2, "ENGINE\nturns faster or slower", L_GREY, 12)
box(ax, 4.2, 2.4, 3.0, 1.2, "SENSE + THINK\nspinning balls fly out\nwhen it turns fast", L_BLUE, 12)
box(ax, 8.4, 2.4, 3.0, 1.2, "ACT\nsteam valve closes\na little", L_GREEN, 12)
for p, q in [((3.0, 3.0), (4.2, 3.0)), ((7.2, 3.0), (8.4, 3.0))]:
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, color=GREY, lw=2))
ax.add_patch(FancyArrowPatch((9.9, 2.4), (1.5, 2.4), arrowstyle="-|>", mutation_scale=16, color=GREY, lw=2,
                             connectionstyle="arc3,rad=0.45"))
ax.text(5.7, 0.35, "less steam → the engine slows down again", ha="center", fontsize=12, style="italic")
ax.text(5.7, 4.2, "too fast → balls out → less steam → slower      too slow → balls in → more steam → faster",
        ha="center", fontsize=11.5, color=BLUE)
ax.set_xlim(-0.3, 11.7); ax.set_ylim(-0.1, 4.6); ax.axis("off")
save(fig, "fig03-governor-loop.png")

# ---------- Figure 4: governor simulation (same model as governor.py) ----------
wanted = 100
so, sg = 100.0, 100.0
t, s_open, s_gov = [], [], []
for second in range(0, 61):
    load = 1.0 if second < 20 else 1.5
    vg = max(0.0, min(1.0, 0.5 + 0.02 * (wanted - sg)))
    t.append(second); s_open.append(so); s_gov.append(sg)
    so = so + 10 * (2.0 * 0.5 - load * so / 100)
    sg = sg + 10 * (2.0 * vg - load * sg / 100)
fig, ax = plt.subplots(figsize=(10, 5.2))
ax.axhline(wanted, color=BLACK, ls="--", lw=2, label="wanted speed: 100 turns per minute")
ax.plot(t, s_open, color=GREY, ls=":", lw=3, label="no governor (open loop)")
ax.plot(t, s_gov, color=BLUE, lw=2.5, label="with governor (closed loop)")
ax.axvline(20, color=GREY, lw=1)
ax.annotate("second 20: the machines\nneed 50% more power", xy=(20, 85), xytext=(26, 78), arrowprops=dict(arrowstyle="->"))
ax.annotate("about 91: a small gap stays\n(Chapter 211 explains why)", xy=(55, 90.9), xytext=(36, 95.5),
            arrowprops=dict(arrowstyle="->"))
ax.annotate("about 67: a third slower", xy=(55, 66.8), xytext=(38, 71), arrowprops=dict(arrowstyle="->"))
ax.set_xlabel("time (seconds)"); ax.set_ylabel("engine speed (turns per minute)")
ax.set_ylim(60, 105); ax.grid(alpha=0.3); ax.legend(loc="lower left", fontsize=11)
save(fig, "fig04-governor-run.png")

# ---------- Figure 5: the light-seeking tortoise (same model as tortoise.py) ----------
def bright(px, py): return 1 / (1 + px ** 2 + py ** 2)
def run(x, y, heading):
    xs, ys = [x], [y]
    for _ in range(200):
        la, ra = math.radians(heading + 30), math.radians(heading - 30)
        left = bright(x + 0.2 * math.cos(la), y + 0.2 * math.sin(la))
        right = bright(x + 0.2 * math.cos(ra), y + 0.2 * math.sin(ra))
        if bright(x, y) > 0.9: break
        heading += 400 * (left - right)
        x += 0.1 * math.cos(math.radians(heading)); y += 0.1 * math.sin(math.radians(heading))
        xs.append(x); ys.append(y)
    return xs, ys
fig, ax = plt.subplots(figsize=(8, 7))
for r in [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]:
    ax.add_patch(Circle((0, 0), r, fc="none", ec=ORANGE, alpha=0.35, lw=1))
ax.scatter(0, 0, s=500, color="#F0E442", edgecolor=BLACK, zorder=3, marker="*")
ax.text(0.15, 0.2, "lamp", fontsize=12)
starts = [(-3.0, -2.0, 0.0, "start A (facing east)"), (2.5, -2.5, 90.0, "start B (facing north)"),
          (-2.0, 2.5, 180.0, "start C (facing west)")]
for (x0, y0, h0, lab), ls in zip(starts, ["-", "--", ":"]):
    xs, ys = run(x0, y0, h0)
    found = math.hypot(xs[-1], ys[-1]) < 0.4
    result = f"reaches the lamp in {len(xs) - 1} steps" if found else f"LOST: no lamp after {len(xs) - 1} steps"
    ax.plot(xs, ys, color=BLUE, ls=ls, lw=2.5, label=f"{lab}: {result}")
    ax.scatter(x0, y0, s=90, color=ORANGE, edgecolor=BLACK, zorder=3)
ax.set_xlabel("x (metres)"); ax.set_ylabel("y (metres)")
ax.set_xlim(-3.6, 3.6); ax.set_ylim(-3.6, 3.6); ax.set_aspect("equal"); ax.grid(alpha=0.3)
ax.legend(loc="upper right", fontsize=10.5)
save(fig, "fig05-tortoise-paths.png")

# ---------- Figure 6: what was new in each era ----------
rows = ["Ancient and\nmedieval", "1700s–1800s", "1900–1960", "1960–2000", "2000–today"]
cols = ["SENSE", "THINK", "ACT"]
cells = [
    ["floats feel\nthe water level", "fixed programs:\nropes, cams", "water, falling\nweights, gears"],
    ["spinning balls\nfeel speed", "punched cards;\nmaths of stability", "steam engines"],
    ["light cells,\nradar", "electronics,\nfirst computers", "electric motors,\nhydraulics"],
    ["cameras, sonar,\nlaser scanners", "planning (A*),\nmicrochips", "precise arm\nmotors, walking legs"],
    ["cheap IMUs, GPS,\nLiDAR, depth cameras", "SLAM, deep learning,\nROS", "brushless motors,\nnew batteries"],
]
fig, ax = plt.subplots(figsize=(12, 7))
face = [L_BLUE, L_ORANGE, L_GREEN]
for j, c in enumerate(cols):
    box(ax, 2.4 + j * 3.2, 5.2, 3.0, 0.7, c, face[j], 13)
for i, r in enumerate(rows):
    y = 4.2 - i * 1.0
    box(ax, 0, y, 2.2, 0.85, r, L_GREY, 11)
    for j in range(3):
        box(ax, 2.4 + j * 3.2, y, 3.0, 0.85, cells[i][j], "white", 11)
ax.set_xlim(-0.2, 12.2); ax.set_ylim(-0.1, 6.1); ax.axis("off")
save(fig, "fig06-eras-sense-think-act.png")

print("saved 6 figures in", os.path.normpath(OUT))
