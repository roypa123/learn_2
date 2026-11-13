# Figures for Chapter 113 - Project: a traffic light and a reaction-time game.
# Run:  python figures.py      (saves PNG files in ../../images/ch113/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch113")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6CBB5"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, fc, fs=10.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=fc, ec=BLACK))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)


def arrow(ax, a, b, text="", col=BLACK, rad=0.0, fs=9):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=13, lw=1.5, color=col,
                                 connectionstyle=f"arc3,rad={rad}"))
    if text:
        ax.text((a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + 0.18, text, ha="center", fontsize=fs)


# Figure 1: the crossing's state machine
fig, ax = plt.subplots(figsize=(12.5, 4.8))
st = [("CARS_GO\ncars green", 0.0, 2.6, L_GREEN), ("CARS_SLOW\nyellow", 3.0, 2.6, L_ORANGE), ("ALL_STOP\nall red", 6.0, 2.6, L_RED),
      ("WALK\nwalk green", 9.0, 2.6, L_GREEN), ("WALK_ENDING\nwalk flashes", 9.0, 0.2, L_ORANGE),
      ("CLEAR\nall red", 6.0, 0.2, L_RED), ("CARS_READY\nred + yellow", 3.0, 0.2, L_ORANGE)]
for name, x, y, col in st:
    box(ax, x, y, 2.3, 1.1, name, col)
arrow(ax, (2.35, 3.15), (2.95, 3.15)); ax.text(2.65, 3.95, "request and\n8 s of green", ha="center", fontsize=8.5)
arrow(ax, (5.35, 3.15), (5.95, 3.15), "3 s")
arrow(ax, (8.35, 3.15), (8.95, 3.15), "1 s")
arrow(ax, (10.15, 2.55), (10.15, 1.35)); ax.text(10.3, 1.95, "6 s", fontsize=9)
arrow(ax, (8.95, 0.75), (8.35, 0.75), "4 s")
arrow(ax, (5.95, 0.75), (5.35, 0.75), "2 s")
arrow(ax, (2.95, 0.75), (1.15, 2.55), "1.5 s", rad=-0.3)
ax.text(-0.1, 4.75, "the button only sets a flag (requested); the state machine decides when to act on it",
        fontsize=10, color=BLUE)
ax.set_xlim(-0.3, 11.6); ax.set_ylim(-0.1, 5.0); ax.axis("off")
save(fig, "fig01-traffic-states.png")

# Figure 2: 50 s of the crossing on the PC test bench
changes = [(0, "CARS_GO"), (8000, "CARS_SLOW"), (11000, "ALL_STOP"), (12000, "WALK"), (18000, "WALK_ENDING"),
           (22000, "CLEAR"), (24000, "CARS_READY"), (25500, "CARS_GO"), (33500, "CARS_SLOW"), (36500, "ALL_STOP"),
           (37500, "WALK"), (43500, "WALK_ENDING"), (47500, "CLEAR"), (49500, "CARS_READY"), (50000, None)]
car = {"CARS_GO": GREEN, "CARS_SLOW": ORANGE, "ALL_STOP": RED, "WALK": RED, "WALK_ENDING": RED, "CLEAR": RED, "CARS_READY": ORANGE}
walk = {"CARS_GO": RED, "CARS_SLOW": RED, "ALL_STOP": RED, "WALK": GREEN, "WALK_ENDING": "flash", "CLEAR": RED, "CARS_READY": RED}
fig, ax = plt.subplots(figsize=(12, 3.4))
for (t0, s), (t1, _) in zip(changes, changes[1:]):
    ax.add_patch(Rectangle((t0 / 1000, 1.2), (t1 - t0) / 1000, 0.6, fc=car[s], ec="white"))
    if walk[s] == "flash":
        for k in range(int((t1 - t0) / 500)):
            ax.add_patch(Rectangle((t0 / 1000 + k * 0.5, 0.2), 0.25, 0.6, fc=GREEN, ec="white"))
    else:
        ax.add_patch(Rectangle((t0 / 1000, 0.2), (t1 - t0) / 1000, 0.6, fc=walk[s], ec="white"))
for t, txt in [(3.0, "2 presses"), (4.0, ""), (13.0, "press"), (30.0, "press")]:
    ax.annotate(txt, xy=(t, 1.85), xytext=(t, 2.45), ha="center", fontsize=9, arrowprops=dict(arrowstyle="-|>"))
ax.text(-0.5, 1.5, "cars", ha="right", va="center"); ax.text(-0.5, 0.5, "walkers", ha="right", va="center")
ax.set_xlim(-0.2, 50.2); ax.set_ylim(0, 2.8); ax.set_yticks([]); ax.set_xlabel("time (s)")
for s in ["left", "right", "top"]:
    ax.spines[s].set_visible(False)
save(fig, "fig02-traffic-run.png")

# Figure 3: the reaction game's state machine
fig, ax = plt.subplots(figsize=(12, 4.0))
box(ax, 0.0, 1.5, 2.6, 1.1, "WAITING\ndim glow,\nrandom 1.5-4 s", L_BLUE)
box(ax, 4.2, 1.5, 2.6, 1.1, "GO\nfull light + beep,\nnote micros()", L_GREEN)
box(ax, 8.4, 1.5, 2.6, 1.1, "RESULT\nprint, pause 1 s", L_ORANGE)
box(ax, 8.4, -0.4, 2.6, 0.9, "DONE\nprint best, average", L_GREY)
arrow(ax, (2.65, 2.05), (4.15, 2.05), "time is up")
arrow(ax, (6.85, 2.05), (8.35, 2.05), "pressed (or 1.5 s)")
arrow(ax, (1.3, 2.65), (9.7, 2.65), col=RED, rad=-0.25); ax.text(5.5, 3.95, "pressed too early: false start", ha="center", fontsize=9.5, color=RED)
arrow(ax, (9.0, 1.45), (1.3, 1.45), rad=-0.3); ax.text(5.5, 0.25, "next round", ha="center", fontsize=9)
arrow(ax, (9.7, 1.45), (9.7, 0.55)); ax.text(9.8, 1.0, "after round 5", fontsize=9)
ax.set_xlim(-0.2, 11.4); ax.set_ylim(-0.6, 4.2); ax.axis("off")
save(fig, "fig03-game-states.png")

# Figure 4: why the interrupt makes the game fair
fig, ax = plt.subplots(figsize=(12, 3.8))
t = np.linspace(225, 245, 4001)
go = 0.0
press = 231.4
edges = [0.0, 0.08, 0.15, 0.35, 0.45, 0.70, 0.85]


def pin(x):
    if x < press:
        return 1
    f = (x - press) / 3.0
    if f >= 1:
        return 0
    k = sum(1 for e in edges if e <= f)
    return 0 if k % 2 == 1 else 1


ax.plot(t, [pin(x) + 1.4 for x in t], color=BLUE, lw=2)
ax.text(225.2, 2.55, "button pin (pressed = LOW), with bounce", fontsize=10, color=BLUE)
ax.axvline(press, color=GREEN, lw=2); ax.text(press + 0.2, 0.9, "ISR: micros() at the\nfirst edge: 231.4 ms", fontsize=10, color=GREEN)
polls = np.arange(225, 246, 10.0) + 3.0
for p in polls:
    ax.plot([p, p], [0.1, 0.6], color=RED, lw=2)
ax.text(238.5, 0.25, "a loop polling every 10 ms\nwould see it up to 10 ms late", fontsize=10, color=RED, va="bottom")
ax.set_xlim(225, 245); ax.set_ylim(0, 2.8); ax.set_yticks([]); ax.set_xlabel("ms after GO")
save(fig, "fig04-fair-timing.png")

# Figure 5: the scores collected by scores.py
rounds = [1, 2, 3, 4, 5]
ms = [231.4, 198.0, None, 264.7, 187.3]
fig, ax = plt.subplots(figsize=(9, 4.0))
for r, v in zip(rounds, ms):
    if v is None:
        ax.bar(r, 20, color=RED); ax.text(r, 30, "false\nstart", ha="center", fontsize=10, color=RED)
    else:
        ax.bar(r, v, color=BLUE); ax.text(r, v + 5, f"{v}", ha="center", fontsize=10)
ax.axhline(220.35, color=GREEN, ls="--"); ax.text(5.45, 223, "average\n220.35", fontsize=9.5, color=GREEN)
ax.set_xticks(rounds); ax.set_xlabel("round"); ax.set_ylabel("reaction time (ms)"); ax.set_ylim(0, 300)
save(fig, "fig05-scores.png")

# Figure 6: Part 6 inside the project
fig, ax = plt.subplots(figsize=(12.5, 5.2))
rows = [("traffic light", L_GREEN, [("lights, pins", "98"), ("button +\ndebounce", "99, 110"), ("state machine", "104"),
                                    ("millis() timing", "103"), ("Serial log", "100")]),
        ("reaction game", L_BLUE, [("interrupt pin 2", "105"), ("volatile, copy", "105"), ("PWM glow", "102"),
                                   ("tone() buzzer", "102, 106"), ("random wait", "96, 101")]),
        ("scores on the PC", L_ORANGE, [("pyserial", "111"), ("CSV lines", "100, 111"), ("floats", "96"),
                                        ("one Uno, 5 V", "94, 95"), ("Rover link next", "107, 112")])]
for r, (title, col, cells) in enumerate(rows):
    y = 3.4 - r * 1.5
    box(ax, 0.0, y, 2.2, 1.0, title, col, 11)
    for k, (what, ch) in enumerate(cells):
        box(ax, 2.6 + k * 2.0, y, 1.85, 1.0, f"{what}\nCh {ch}", "white", 9.5)
ax.set_xlim(-0.2, 12.6); ax.set_ylim(0.2, 4.6); ax.axis("off")
save(fig, "fig06-part6-in-project.png")
print("figures saved in", os.path.abspath(OUT))
