# Figures for Chapter 104 - State machines.
# Run:  python figures.py      (saves PNG files in ../../images/ch104/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle, FancyBboxPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch104")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED, L_YEL = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6CBB5", "#FFF3B0"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def state(ax, x, y, name, fc, r=0.75, fs=11, sub=None):
    ax.add_patch(Circle((x, y), r, fc=fc, ec=BLACK, lw=2))
    ax.text(x, y + (0.12 if sub else 0), name, ha="center", va="center", fontsize=fs, weight="bold")
    if sub:
        ax.text(x, y - 0.25, sub, ha="center", va="center", fontsize=9)


def trans(ax, p1, p2, label, rad=0.25, color=BLACK, r=0.78, lx=0, ly=0, fs=10):
    (x1, y1), (x2, y2) = p1, p2
    d = math.hypot(x2 - x1, y2 - y1)
    ux, uy = (x2 - x1) / d, (y2 - y1) / d
    a = FancyArrowPatch((x1 + ux * r, y1 + uy * r), (x2 - ux * r, y2 - uy * r), connectionstyle=f"arc3,rad={rad}",
                        arrowstyle="-|>", mutation_scale=16, color=color, lw=1.8)
    ax.add_patch(a)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    nx, ny = uy, -ux                       # the side matplotlib's arc3 bends towards
    ax.text(mx + nx * rad * d * 0.5 + lx, my + ny * rad * d * 0.5 + ly, label, ha="center", va="center", fontsize=fs, color=color,
            bbox=dict(fc="white", ec="none", pad=1))


# Figure 1: the traffic light as a state machine
fig, ax = plt.subplots(figsize=(9, 6))
P = {"RED": (0, 2.2), "GREEN": (3.2, -0.6), "YELLOW": (-3.2, -0.6)}
state(ax, *P["RED"], "RED", L_RED, sub="red lamp on")
state(ax, *P["GREEN"], "GREEN", L_GREEN, sub="green lamp on")
state(ax, *P["YELLOW"], "YELLOW", L_YEL, sub="yellow lamp on")
trans(ax, P["RED"], P["GREEN"], "after 3 s", rad=-0.25)
trans(ax, P["GREEN"], P["YELLOW"], "after 2.5 s", rad=-0.25)
trans(ax, P["YELLOW"], P["RED"], "after 1 s", rad=-0.25)
ax.annotate("start", xy=(0, 2.95), xytext=(0, 3.8), ha="center", fontsize=11, arrowprops=dict(arrowstyle="-|>", lw=1.8))
ax.set_xlim(-4.5, 4.5); ax.set_ylim(-2, 4.1); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig01-traffic-light.png")

# Figure 2: the parts of a state machine
fig, ax = plt.subplots(figsize=(11, 4.6))
state(ax, 1.2, 1.2, "DRIVE", L_GREEN, r=0.9, sub="motors forward")
state(ax, 7.0, 1.2, "BACK_UP", L_ORANGE, r=0.9, sub="motors backward")
trans(ax, (1.2, 1.2), (7.0, 1.2), "event: a bumper is pressed", rad=-0.18, r=0.95)
ax.annotate("a STATE: what the robot\nis doing now", xy=(1.2, 2.1), xytext=(1.2, 3.4), ha="center", fontsize=10.5,
            arrowprops=dict(arrowstyle="-|>", color=BLUE), color=BLUE)
ax.annotate("a TRANSITION: the rule\nfor moving to another state", xy=(4.1, 1.75), xytext=(4.1, 3.4), ha="center", fontsize=10.5,
            arrowprops=dict(arrowstyle="-|>", color=BLUE), color=BLUE)
ax.annotate("an ENTRY ACTION: done once,\non arriving (start the motors)", xy=(7.0, 0.85), xytext=(9.6, -0.5), ha="center",
            fontsize=10.5, arrowprops=dict(arrowstyle="-|>", color=BLUE), color=BLUE)
ax.set_xlim(-0.2, 11.5); ax.set_ylim(-1.1, 4.0); ax.axis("off")
save(fig, "fig02-parts.png")

# Figure 3: Rover's behaviour
fig, ax = plt.subplots(figsize=(12, 7.2))
P = {"WAIT_START": (0, 2.5), "DRIVE": (3.6, 2.5), "BACK_UP": (7.2, 2.5), "TURN_LEFT": (10.8, 5.0), "TURN_RIGHT": (10.8, 2.5),
     "TURN_AROUND": (10.8, 0.0)}
cols = {"WAIT_START": L_GREY, "DRIVE": L_GREEN, "BACK_UP": L_ORANGE, "TURN_LEFT": L_BLUE, "TURN_RIGHT": L_BLUE, "TURN_AROUND": L_BLUE}
subs = {"WAIT_START": "stop", "DRIVE": "forward", "BACK_UP": "backward", "TURN_LEFT": "spin left", "TURN_RIGHT": "spin right",
        "TURN_AROUND": "spin right"}
for name, (x, y) in P.items():
    state(ax, x, y, name.replace("_", "_\n") if len(name) > 8 else name, cols[name], r=0.85, fs=10, sub=None)
    ax.text(x, y - 1.05, "motors: " + subs[name], ha="center", fontsize=9.5, color=GREY)
trans(ax, P["WAIT_START"], P["DRIVE"], "start\npressed", rad=0.0, r=0.9, ly=0.4)
trans(ax, P["DRIVE"], P["BACK_UP"], "a bumper\npressed", rad=0.0, r=0.9, ly=0.4)
trans(ax, P["BACK_UP"], P["TURN_LEFT"], "after 0.5 s:\nright only", rad=0.0, r=0.9, lx=-0.6, ly=0.35)
trans(ax, P["BACK_UP"], P["TURN_RIGHT"], "after 0.5 s:\nleft only", rad=0.0, r=0.9, ly=0.4)
trans(ax, P["BACK_UP"], P["TURN_AROUND"], "after 0.5 s:\nboth", rad=0.0, r=0.9, lx=-0.6, ly=-0.35)
for name, t in [("TURN_LEFT", "0.4 s"), ("TURN_RIGHT", "0.4 s"), ("TURN_AROUND", "0.8 s")]:
    x, y = P[name]
    ax.add_patch(FancyArrowPatch((x + 0.88, y), (x + 1.7, y), arrowstyle="-|>", mutation_scale=16, lw=1.8))
    ax.text(x + 1.8, y, f"after {t}:\nback to\nDRIVE", va="center", fontsize=10)
ax.text(3.6, 5.6, "from ANY moving state: start pressed -> WAIT_START (motors stop)", ha="center", fontsize=11, color=RED)
ax.set_xlim(-1.2, 13.6); ax.set_ylim(-1.5, 6.1); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig03-rover-states.png")

# Figure 4: the Rover test as a timeline (from pc_tests/test_rover_behaviour.cpp)
events = [(0, "WAIT_START"), (507, "DRIVE"), (2007, "BACK_UP"), (2507, "TURN_RIGHT"), (2907, "DRIVE"), (4007, "BACK_UP"),
          (4507, "TURN_AROUND"), (5307, "DRIVE"), (7007, "WAIT_START"), (8000, None)]
colmap = {"WAIT_START": L_GREY, "DRIVE": L_GREEN, "BACK_UP": L_ORANGE, "TURN_RIGHT": L_BLUE, "TURN_AROUND": L_BLUE}
fig, ax = plt.subplots(figsize=(13, 4.2))
for (t0, name), (t1, _) in zip(events[:-1], events[1:]):
    ax.add_patch(Rectangle((t0, 2.0), t1 - t0, 0.8, fc=colmap[name], ec=BLACK))
    ax.text((t0 + t1) / 2, 2.4, name.replace("TURN_", "TURN\n"), ha="center", va="center", fontsize=8.5)
for row, (label, spans) in enumerate([("start", [(500, 700), (7000, 7200)]), ("left bumper", [(2000, 2200), (4000, 4300)]),
                                       ("right bumper", [(4010, 4300)])]):
    y = 1.3 - row * 0.55
    for a, b in spans:
        ax.add_patch(Rectangle((a, y), b - a, 0.35, fc=RED, ec="none"))
    ax.text(-80, y + 0.17, label, ha="right", va="center", fontsize=10)
ax.text(-80, 2.4, "state", ha="right", va="center", fontsize=10)
ax.set_xlim(0, 8000); ax.set_ylim(-0.1, 3.0); ax.set_yticks([]); ax.set_xlabel("time (ms)")
save(fig, "fig04-rover-timeline.png")

# Figure 5: debounce as a state machine
fig, ax = plt.subplots(figsize=(10, 7))
P = {"UP": (0, 3), "MAYBE_DOWN": (4.4, 3), "DOWN": (4.4, -0.6), "MAYBE_UP": (0, -0.6)}
for name, fc in [("UP", L_GREY), ("MAYBE_DOWN", L_YEL), ("DOWN", L_GREEN), ("MAYBE_UP", L_YEL)]:
    state(ax, *P[name], name.replace("_", "_\n"), fc, r=0.95, fs=10.5)
trans(ax, P["UP"], P["MAYBE_DOWN"], "pin LOW:\nstart timing", rad=-0.25, r=1.0)
trans(ax, P["MAYBE_DOWN"], P["UP"], "pin HIGH again:\na bounce", rad=-0.25, r=1.0)
trans(ax, P["MAYBE_DOWN"], P["DOWN"], "LOW for 5 ms:\nPRESS (count it)", rad=-0.2, r=1.0, lx=0.4, color=GREEN)
trans(ax, P["DOWN"], P["MAYBE_UP"], "pin HIGH:\nstart timing", rad=-0.25, r=1.0)
trans(ax, P["MAYBE_UP"], P["DOWN"], "pin LOW again:\na bounce", rad=-0.25, r=1.0)
trans(ax, P["MAYBE_UP"], P["UP"], "HIGH for 5 ms:\nreleased", rad=-0.2, r=1.0, lx=-0.4)
ax.set_xlim(-2.2, 6.6); ax.set_ylim(-2.2, 4.6); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig05-debounce-fsm.png")
print("figures saved in", os.path.abspath(OUT))
