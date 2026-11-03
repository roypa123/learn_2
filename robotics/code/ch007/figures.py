# Figures for Chapter 7 — Safety first: electricity, moving parts, batteries, tools.
# Run:  python figures.py      (saves PNG files in ../../images/ch007/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Ellipse

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch007")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
PURPLE, SKY, YELLOW = "#CC79A7", "#56B4E9", "#F0E442"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, face, size=11, ec=BLACK, lw=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=ec, lw=lw))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size)


def arrow(ax, p, q, colour=GREY, lw=2.0, rad=0.0, label=None, lpos=None, lcol=BLACK, size=11):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=15, color=colour, lw=lw,
                                 connectionstyle=f"arc3,rad={rad}"))
    if label:
        x, y = lpos if lpos else ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + 0.2)
        ax.text(x, y, label, ha="center", fontsize=size, color=lcol, style="italic")


def line(ax, pts, colour=BLACK, lw=3.0, ls="-"):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    ax.plot(xs, ys, color=colour, lw=lw, ls=ls, solid_capstyle="round")


# ---------- Figure 1: risk = how likely x how bad ----------
fig, ax = plt.subplots(figsize=(11, 7.5))
colours = [["#BDEBDD", "#BDEBDD", "#FBE3B3"],
           ["#BDEBDD", "#FBE3B3", "#F6C9B0"],
           ["#FBE3B3", "#F6C9B0", "#F6C9B0"]]
words = [["low", "low", "medium"], ["low", "medium", "high"], ["medium", "high", "high"]]
for row in range(3):          # row = how likely (0 rare, 2 often)
    for col in range(3):      # col = how bad (0 small, 2 serious)
        ax.add_patch(Rectangle((col, row), 1, 1, fc=colours[row][col], ec="white", lw=3))
        ax.text(col + 0.95, row + 0.06, words[row][col] + " risk", ha="right", va="bottom", fontsize=10, color="#444444")
examples = [
    (0.5, 0.62, "AA battery\nin a toy"),
    (0.5, 2.62, "small scratch\nfrom a wire end"),
    (1.5, 1.62, "touching a\nhot soldering iron"),
    (2.5, 0.62, "lithium battery\nfire while charging"),
    (2.5, 2.62, "fingers in drone\npropellers (props on!)"),
    (1.5, 2.62, "robot arm pinches\na finger"),
    (0.5, 1.62, "small robot\nbumps your foot"),
    (1.5, 0.62, "wire gets hot in\na short circuit"),
    (2.5, 1.62, "something in\nyour eye (no glasses)"),
]
for x, y, t in examples:
    ax.text(x, y, t, ha="center", va="center", fontsize=10.5)
ax.set_xticks([0.5, 1.5, 2.5]); ax.set_xticklabels(["small\n(a plaster helps)", "medium\n(it really hurts)", "serious\n(hospital, fire)"])
ax.set_yticks([0.5, 1.5, 2.5]); ax.set_yticklabels(["rare", "sometimes", "often"])
ax.set_xlabel("HOW BAD is it if it happens?", fontsize=13, weight="bold")
ax.set_ylabel("HOW LIKELY is it to happen?", fontsize=13, weight="bold")
ax.set_xlim(0, 3); ax.set_ylim(0, 3)
ax.set_title("Risk = how likely x how bad: we work hardest on the red corner", fontsize=13)
for s in ax.spines.values():
    s.set_visible(False)
ax.tick_params(length=0)
save(fig, "fig01-risk-matrix.png")

# ---------- Figure 2: normal circuit vs short circuit, with a fuse ----------
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
for k, ax in enumerate(axes):
    # battery on the left
    ax.add_patch(Rectangle((0.0, 1.2), 1.0, 2.2, fc=L_ORANGE, ec=BLACK, lw=1.5))
    ax.text(0.5, 2.3, "BATTERY", ha="center", va="center", fontsize=11, rotation=90, weight="bold")
    ax.text(0.5, 3.55, "+", ha="center", fontsize=16, weight="bold"); ax.text(0.5, 0.75, "−", ha="center", fontsize=18, weight="bold")
    # fuse on the top wire
    ax.add_patch(Rectangle((2.0, 3.75), 1.2, 0.5, fc="white", ec=BLACK, lw=1.5))
    ax.text(2.6, 4.45, "FUSE", ha="center", fontsize=11, weight="bold")
    # motor on the right
    ax.add_patch(plt.Circle((6.0, 2.3), 0.6, fc=L_GREEN, ec=BLACK, lw=1.5))
    ax.text(6.0, 2.3, "M", ha="center", va="center", fontsize=16, weight="bold")
    ax.text(6.0, 1.35, "motor", ha="center", fontsize=11)
    if k == 0:
        c = BLUE
        line(ax, [(0.5, 3.4), (0.5, 4.0), (2.0, 4.0)], c); ax.plot([2.0, 3.2], [4.0, 4.0], color=c, lw=1.5)
        line(ax, [(3.2, 4.0), (6.0, 4.0), (6.0, 2.9)], c)
        line(ax, [(6.0, 1.7), (6.0, 0.4), (0.5, 0.4), (0.5, 1.2)], c)
        arrow(ax, (3.8, 4.0), (4.8, 4.0), c, lw=0)
        ax.text(3.5, 5.0, "NORMAL: the electricity must go\nthrough the motor, which uses it", ha="center", fontsize=12.5, color=BLUE, weight="bold")
        ax.text(3.3, -0.35, "a normal amount flows; wires stay cool", ha="center", fontsize=11.5)
    else:
        c = RED
        line(ax, [(0.5, 3.4), (0.5, 4.0), (2.0, 4.0)], c, lw=5)
        ax.plot([2.0, 2.45], [4.0, 4.0], color=c, lw=1.5); ax.plot([2.75, 3.2], [4.0, 4.0], color=c, lw=1.5)
        ax.text(2.6, 3.88, "X", ha="center", va="center", fontsize=16, color=RED, weight="bold")
        line(ax, [(3.2, 4.0), (6.0, 4.0), (6.0, 2.9)], GREY)
        line(ax, [(6.0, 1.7), (6.0, 0.4), (0.5, 0.4), (0.5, 1.2)], GREY)
        line(ax, [(4.0, 4.0), (4.0, 0.4)], RED, lw=5)
        ax.add_patch(Ellipse((4.0, 2.3), 0.6, 0.5, fc=YELLOW, ec=RED, lw=2))
        ax.text(2.45, 2.3, "loose wire or\ndropped\nscrewdriver\ntouches\nboth sides", ha="center", va="center", fontsize=10.5, color=RED)
        arrow(ax, (3.2, 2.3), (3.65, 2.3), RED, lw=1.5)
        ax.text(3.5, 5.0, "SHORT CIRCUIT: a shortcut with almost\nnothing in the way", ha="center", fontsize=12.5, color=RED, weight="bold")
        ax.text(3.3, -0.35, "a HUGE amount flows; wires get hot in seconds\n-> the fuse melts first and breaks the circuit", ha="center", fontsize=11.5)
    ax.set_xlim(-0.6, 7.2); ax.set_ylim(-1.0, 5.7); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig02-short-circuit.png")

# ---------- Figure 3: thermal runaway, a "bad loop" ----------
fig, ax = plt.subplots(figsize=(12, 7))
box(ax, 0.0, 5.2, 3.6, 1.2, "START\ndamage, overcharge,\nshort circuit, heat", L_GREY, 11)
box(ax, 4.6, 4.4, 3.0, 1.2, "the cell gets\nWARMER", L_ORANGE, 12)
box(ax, 8.8, 2.4, 3.0, 1.2, "chemicals inside\nreact FASTER", L_RED, 12)
box(ax, 4.6, 0.4, 3.0, 1.2, "the reaction makes\nMORE HEAT", L_RED, 12)
box(ax, 0.4, 2.4, 3.0, 1.2, "the cell next to it\ngets hot too", L_ORANGE, 11)
arrow(ax, (3.6, 5.6), (4.6, 5.1), BLACK)
arrow(ax, (7.6, 5.0), (9.6, 3.6), RED, lw=3, rad=-0.25)
arrow(ax, (9.6, 2.4), (7.6, 1.0), RED, lw=3, rad=-0.25)
arrow(ax, (5.9, 1.6), (5.9, 4.4), RED, lw=3)
arrow(ax, (4.6, 1.0), (2.4, 2.4), GREY, lw=2, rad=-0.25)
ax.text(6.25, 3.0, "the loop\nfeeds itself", ha="left", fontsize=12, color=RED, weight="bold")
ax.text(6.0, 6.75, "Thermal runaway: a feedback loop that makes things WORSE", ha="center", fontsize=14, weight="bold")
ax.text(6.0, -0.35, "End: poisonous smoke, fire, flying sparks. It is very hard to put out: get out and call for help.\n"
        "Prevent it: the right charger, never charge unattended, never use a damaged or swollen battery.",
        ha="center", va="top", fontsize=11)
ax.set_xlim(-0.3, 12.2); ax.set_ylim(-1.3, 7.1); ax.axis("off")
save(fig, "fig03-thermal-runaway.png")

# ---------- Figure 4: Rover's power path with the emergency stop ----------
fig, ax = plt.subplots(figsize=(14, 6.5))
box(ax, 0.0, 2.6, 1.8, 1.3, "BATTERY\n7.2 V", L_ORANGE)
box(ax, 2.4, 2.75, 1.3, 1.0, "FUSE", "white")
box(ax, 4.3, 2.75, 1.7, 1.0, "MAIN\nSWITCH", "white")
box(ax, 7.0, 4.2, 2.0, 1.1, "5 V\nREGULATOR", L_GREY)
box(ax, 10.0, 4.2, 2.2, 1.1, "BRAIN\n(Arduino)", L_ORANGE)
ax.add_patch(plt.Circle((8.0, 1.5), 0.62, fc=RED, ec=BLACK, lw=2))
ax.add_patch(plt.Circle((8.0, 1.5), 0.82, fc="none", ec=YELLOW, lw=8))
ax.text(8.0, 1.5, "STOP", ha="center", va="center", fontsize=12, color="white", weight="bold")
ax.text(8.0, 0.25, "E-STOP\n(press = motor power OFF)", ha="center", va="top", fontsize=11, weight="bold")
box(ax, 10.0, 0.95, 2.2, 1.1, "MOTOR\nDRIVER", L_GREEN)
box(ax, 13.0, 0.95, 1.6, 1.1, "MOTORS", L_GREEN)
line(ax, [(1.8, 3.25), (2.4, 3.25)]); line(ax, [(3.7, 3.25), (4.3, 3.25)])
line(ax, [(6.0, 3.25), (6.5, 3.25), (6.5, 4.75), (7.0, 4.75)])
line(ax, [(6.5, 3.25), (6.5, 1.5), (7.18, 1.5)], GREEN)
line(ax, [(8.82, 1.5), (10.0, 1.5)], GREEN)
line(ax, [(12.2, 1.5), (13.0, 1.5)], GREEN)
line(ax, [(9.0, 4.75), (10.0, 4.75)])
ax.plot([11.1, 11.1], [4.2, 2.05], color=BLUE, lw=2)
ax.text(11.25, 3.1, "signal:\nspeed", color=BLUE, fontsize=10.5)
ax.plot([8.6, 9.2, 9.2, 10.0], [2.2, 2.2, 4.45, 4.45], color=BLUE, lw=2, ls="--")
ax.text(9.3, 3.35, "signal:\n'e-stop\npressed'", color=BLUE, fontsize=10)
ax.text(0.0, 5.9, "The e-stop cuts the MOTOR power with a real switch. The brain stays on, sees that the e-stop is pressed, "
        "and refuses to restart\nby itself. Even if the program has a bug, the motors cannot move.", fontsize=11.5)
ax.text(0.0, 0.1, "black = power for everything\ngreen = motor power\nblue = signals", fontsize=10.5)
ax.set_xlim(-0.2, 14.8); ax.set_ylim(-0.6, 6.6); ax.axis("off")
save(fig, "fig04-e-stop-power-path.png")

# ---------- Figure 5: e-stop stopping distance, stacked bars ----------
labels = ["robot's own\nsensor (Ch 2)", "person: hand\non the button", "person: surprised,\nbutton close", "person: must walk\nto a button"]
first = [0.225, 0.375, 1.5, 4.5]         # distance before the circuit acts (sense+think, or the person)
circuit = [0.0, 0.03, 0.03, 0.03]
brake = [1.13, 1.13, 1.13, 1.13]
fig, ax = plt.subplots(figsize=(12, 6.5))
y = range(4)
ax.barh(y, first, color=SKY, ec=BLACK, label="before anything happens (robot's loop, or the person reacting)")
ax.barh(y, circuit, left=first, color=PURPLE, ec=BLACK, label="e-stop circuit (0.02 s)")
left2 = [first[i] + circuit[i] for i in range(4)]
ax.barh(y, brake, left=left2, color=GREY, ec=BLACK, label="braking (1.13 m at 1.5 m/s)")
for i in range(4):
    total = first[i] + circuit[i] + brake[i]
    ax.text(total + 0.08, i, ["1.355 m", "1.535 m", "2.66 m", "5.66 m"][i], va="center", fontsize=12, weight="bold")
ax.set_yticks(list(y)); ax.set_yticklabels(labels)
ax.invert_yaxis()
ax.set_xlabel("distance the robot moves before it stands still (m)")
ax.set_title("Warehouse robot at 1.5 m/s: who stops it, and how far does it go?")
ax.set_xlim(0, 6.6)
ax.legend(loc="upper right", fontsize=10.5)
ax.grid(axis="x", alpha=0.3)
save(fig, "fig05-stopping-distance.png")

# ---------- Figure 6: the watchdog ----------
dt = 0.1
ts = [i * dt for i in range(51)]
pos_off, pos_on = [], []
p_off = p_on = 0.0; sp_on = 0.0; silent = 0
for step in range(51):
    pos_off.append(p_off); pos_on.append(p_on)
    if step < 20:
        sp_on = 0.5; silent = 0
    else:
        silent += 1
    if silent >= 3:
        sp_on = 0.0
    p_off += 0.5 * dt
    p_on += sp_on * dt
fig, ax = plt.subplots(figsize=(11.5, 6))
ax.axvspan(2.0, 5.0, color=L_GREY, alpha=0.6)
ax.text(3.5, 0.15, "no messages arrive (radio link lost)", ha="center", fontsize=11.5)
ax.plot(ts, pos_off, color=RED, lw=2.5, label="no watchdog: keeps the last command and drives on")
ax.plot(ts, pos_on, color=BLUE, lw=2.5, label="with watchdog: stops after 3 silent loops")
ax.axvline(2.0, color=BLACK, ls="--", lw=1.2)
ax.annotate("link breaks\n(t = 2.0 s, 1.0 m)", xy=(2.0, 1.0), xytext=(0.4, 1.6), fontsize=11,
            arrowprops=dict(arrowstyle="->", color=BLACK))
ax.annotate("STOP at t = 2.2 s\n(only 0.1 m more)", xy=(2.2, 1.1), xytext=(2.6, 0.55), fontsize=11, color=BLUE,
            arrowprops=dict(arrowstyle="->", color=BLUE))
ax.annotate("1.55 m more\nand still going", xy=(5.0, 2.55), xytext=(3.6, 2.25), fontsize=11, color=RED,
            arrowprops=dict(arrowstyle="->", color=RED))
ax.set_xlabel("time (s)"); ax.set_ylabel("position (m)")
ax.set_title("A watchdog: 'if I hear nothing, I stop'")
ax.set_xlim(0, 5.2); ax.set_ylim(0, 2.8)
ax.legend(loc="upper left", fontsize=10.5)
ax.grid(alpha=0.3)
save(fig, "fig06-watchdog.png")

# ---------- Figure 7: propeller tip speed ----------
names = ["toy drone\n4 cm, 30,000 rpm", "racing drone\n12.7 cm, 30,000 rpm", "camera drone\n24 cm, 7,000 rpm", "farm drone\n76 cm, 3,000 rpm"]
tips = [62.8, 199.5, 88.0, 119.4]
fig, ax = plt.subplots(figsize=(12, 6.5))
ax.bar(range(4), tips, color=ORANGE, ec=BLACK, width=0.6)
for i, v in enumerate(tips):
    ax.text(i, v + 4, f"{v:.0f} m/s\n({v * 3.6:.0f} km/h)", ha="center", fontsize=11, weight="bold")
ax.axhline(33, color=GREY, ls="--", lw=1.5)
ax.text(3.4, 29, "car on a motorway\n(33 m/s)", ha="left", va="top", fontsize=10.5, color="#555555")
ax.axhline(55, color=BLACK, ls=":", lw=1.5)
ax.text(3.4, 59, "table-saw blade tip\n(about 55 m/s)", ha="left", va="bottom", fontsize=10.5)
ax.set_xticks(range(4)); ax.set_xticklabels(names)
ax.set_ylabel("speed of the propeller tip (m/s)")
ax.set_title("Propeller tips move faster than a saw blade: never touch a spinning propeller")
ax.set_ylim(0, 240); ax.set_xlim(-0.5, 4.3)
ax.grid(axis="y", alpha=0.3)
save(fig, "fig07-prop-tip-speed.png")

# ---------- Figure 8: layers of safety ----------
fig, ax = plt.subplots(figsize=(13, 6.2))
layers = [("1. SAFE DESIGN", "slow, light, rounded,\nlow voltage, guards", L_GREEN),
          ("2. SOFTWARE", "speed limits,\nwatchdog, checks", L_BLUE),
          ("3. SENSORS", "bumpers, distance,\ncurrent limits", L_BLUE),
          ("4. HARDWARE", "fuse, e-stop that\ncuts motor power", L_ORANGE),
          ("5. PEOPLE", "habits, checklist,\nglasses, tidy desk", L_GREY)]
holes = [[2.3, 4.0], [1.0, 2.3], [3.6, 1.2], [3.9, 1.8], [0.9, 2.7]]
for i, (title, text, face) in enumerate(layers):
    x = 1.2 + i * 2.3
    ax.add_patch(Rectangle((x, 0.3), 0.55, 4.6, fc=face, ec=BLACK, lw=1.3))
    for h in holes[i]:
        ax.add_patch(Ellipse((x + 0.275, h), 0.32, 0.5, fc="white", ec=BLACK, lw=1))
    ax.text(x + 0.275, 5.25, title, ha="center", fontsize=11, weight="bold")
    ax.text(x + 0.275, -0.05, text, ha="center", va="top", fontsize=10)
ax.text(0.0, 3.1, "a\ndanger", ha="center", va="center", fontsize=12, color=RED, weight="bold")
ax.annotate("", xy=(5.8, 2.3), xytext=(0.4, 2.3), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.5))
ax.text(6.5, 2.3, "stopped\nby layer 3",fontsize=11.5, color=RED, weight="bold", va="center", ha="left",
        bbox=dict(fc="white", ec="none", pad=0.1))
ax.text(6.0, 6.0, "No layer is perfect (each has holes). Many layers together stop the danger.", ha="center", fontsize=13, weight="bold")
ax.set_xlim(-0.5, 12.6); ax.set_ylim(-1.2, 6.4); ax.axis("off")
save(fig, "fig08-safety-layers.png")
print("figures saved in", os.path.abspath(OUT))
