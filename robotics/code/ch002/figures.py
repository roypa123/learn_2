# Figures for Chapter 2 — What is a robot? Sense, think, act.
# Run:  python figures.py      (saves PNG files in ../../images/ch002/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Wedge

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch002")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, face, size=12):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.3))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size)


def arrow(ax, p, q, colour=GREY, text=None, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, color=colour, lw=2,
                                 connectionstyle=f"arc3,rad={rad}"))
    if text:
        ax.text((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + 0.18, text, ha="center", fontsize=11, style="italic")


# ---------- Figure 1: the sense–think–act loop ----------
fig, ax = plt.subplots(figsize=(11, 6))
box(ax, 0.0, 2.2, 2.8, 1.4, "SENSE\n(sensors)\ncamera, distance,\nbump, encoders", L_BLUE)
box(ax, 4.1, 2.2, 2.8, 1.4, "THINK\n(controller)\nrules, maths,\nprograms", L_ORANGE)
box(ax, 8.2, 2.2, 2.8, 1.4, "ACT\n(actuators)\nmotors, wheels,\ngripper, lights", L_GREEN)
box(ax, 3.6, -0.6, 3.8, 1.1, "THE WORLD\nwalls, people, floor, objects", L_GREY)
arrow(ax, (2.8, 2.9), (4.1, 2.9), text="numbers")
arrow(ax, (6.9, 2.9), (8.2, 2.9), text="commands")
arrow(ax, (9.6, 2.2), (7.4, 0.0), text=None, rad=-0.2)
arrow(ax, (3.6, 0.0), (1.4, 2.2), text=None, rad=-0.2)
ax.text(9.3, 0.7, "the robot\nchanges the world", ha="center", fontsize=11, style="italic")
ax.text(1.7, 0.7, "the world is\nmeasured", ha="center", fontsize=11, style="italic")
ax.text(5.5, 4.2, "repeat many times every second", ha="center", fontsize=13, weight="bold", color=BLUE)
ax.set_xlim(-0.3, 11.3); ax.set_ylim(-0.9, 4.6); ax.axis("off")
save(fig, "fig01-sense-think-act.png")

# ---------- Figure 2: tool, automatic machine or robot? ----------
fig, ax = plt.subplots(figsize=(12, 5.6))
cols = [("TOOL\nno sensing, no deciding", L_GREY,
         ["hammer", "bicycle", "electric drill\n(person holds it)"]),
        ("AUTOMATIC MACHINE\nfixed steps, little sensing", L_BLUE,
         ["toaster with a timer", "washing machine", "traffic light\nwith a timer"]),
        ("ROBOT\nsenses, decides,\nacts by itself", L_GREEN,
         ["robot vacuum", "self-driving car", "planetary rover"])]
for i, (title, face, items) in enumerate(cols):
    x = i * 4.1
    ax.add_patch(Rectangle((x, 0), 3.8, 4.6, fc=face, ec=BLACK, alpha=0.6))
    ax.text(x + 1.9, 4.15, title, ha="center", va="center", fontsize=12, weight="bold")
    for k, item in enumerate(items):
        box(ax, x + 0.3, 2.7 - k * 1.15, 3.2, 0.85, item, "white", size=12)
arrow(ax, (0.2, -0.4), (12.1, -0.4), colour=BLACK)
ax.text(6.15, -0.85, "more sensing and more deciding by itself  →", ha="center", fontsize=12)
ax.set_xlim(-0.2, 12.4); ax.set_ylim(-1.1, 4.8); ax.axis("off")
save(fig, "fig02-tool-machine-robot.png")

# ---------- Figure 3: the wall_stop.py run ----------
distance, speed, step_time, stop_distance = 1.0, 0.25, 0.5, 0.3
steps, readings = [], []
step, moving = 0, True
while moving:
    steps.append(step); readings.append(distance)
    if distance > stop_distance:
        distance -= speed * step_time
    else:
        moving = False
    step += 1
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(steps, readings, "o-", color=BLUE, lw=2.5, ms=8, label="distance to the wall (sensor)")
ax.axhline(stop_distance, color=BLACK, ls="--", lw=2, label="stop distance 0.3 m (what we want)")
ax.fill_between([-0.5, 6.5], 0, 0.3, color=RED, alpha=0.08)
ax.annotate("stops here: 0.25 m\n5 cm closer than we wanted", xy=(6, 0.25), xytext=(3.2, 0.08),
            arrowprops=dict(arrowstyle="->"))
ax.set_xlabel("loop number (one loop every 0.5 s)"); ax.set_ylabel("distance to the wall (metres)")
ax.set_xlim(-0.5, 6.5); ax.set_ylim(0, 1.1); ax.grid(alpha=0.3); ax.legend(loc="upper right")
save(fig, "fig03-wall-stop-run.png")

# ---------- Figure 4: open loop (timer) vs closed loop (thermostat) ----------
minutes = list(range(0, 181))
def outside(m): return 10.0 if m < 60 else 0.0          # it gets colder at minute 60
T_open, T_closed = [15.0], [15.0]
for m in minutes[1:]:
    o = outside(m - 1)
    T_open.append(T_open[-1] + 0.5 - 0.05 * (T_open[-1] - o))          # heater always at half power
    heat = 1.5 if T_closed[-1] < 20 else 0.0                           # thermostat: on below 20 °C
    T_closed.append(T_closed[-1] + heat - 0.05 * (T_closed[-1] - o))
fig, ax = plt.subplots(figsize=(10, 5.2))
ax.axhline(20, color=BLACK, ls="--", lw=2, label="setpoint: 20 °C (what we want)")
ax.plot(minutes, T_open, color=GREY, ls=":", lw=3, label="OPEN loop: heater on a fixed setting")
ax.plot(minutes, T_closed, color=BLUE, lw=2.5, label="CLOSED loop: thermostat measures and decides")
ax.axvline(60, color=GREY, lw=1)
ax.annotate("minute 60: outside\ngets 10 °C colder", xy=(60, 17.0), xytext=(85, 16.2), fontsize=11,
            arrowprops=dict(arrowstyle="->"))
ax.set_xlabel("time (minutes)"); ax.set_ylabel("room temperature (°C)")
ax.set_ylim(8, 23); ax.grid(alpha=0.3); ax.legend(loc="lower left", fontsize=11)
save(fig, "fig04-open-vs-closed-loop.png")

# ---------- Figure 5: a robot vacuum from above, with its sensors ----------
fig, ax = plt.subplots(figsize=(8.5, 7))
ax.add_patch(Circle((0, 0), 1.0, fc=ORANGE, ec=BLACK, lw=1.5, alpha=0.85))
ax.add_patch(Wedge((0, 0), 1.08, 20, 160, width=0.08, fc=GREY, ec=BLACK))             # front bumper
for x in (-0.75, 0.75):
    ax.add_patch(Rectangle((x - 0.08, -0.25), 0.16, 0.5, fc=BLACK))                   # wheels
for (x, y) in [(-0.55, 0.72), (0.0, 0.88), (0.55, 0.72), (-0.6, -0.65), (0.6, -0.65)]:
    ax.add_patch(Circle((x, y), 0.06, fc=BLUE, ec=BLACK))                              # cliff sensors
ax.add_patch(Circle((0, 0.2), 0.22, fc="white", ec=BLACK, lw=1.5))                    # LiDAR on top
ax.annotate("", xy=(0, 1.55), xytext=(0, 1.15), arrowprops=dict(arrowstyle="-|>", lw=2))
ax.text(0.08, 1.45, "forward", fontsize=11)
labels = [((0.9, 0.55), (1.6, 1.15), "bumper: SENSE a touch"),
          ((0.55, 0.72), (1.45, 0.45), "cliff sensors (blue): SENSE\na drop, like stairs"),
          ((0.0, 0.2), (1.45, -0.25), "LiDAR: SENSE walls\nall around (Part 7)"),
          ((0.75, -0.2), (1.45, -0.95), "wheels + motors: ACT,\nencoders: SENSE turning"),
          ((-0.3, -0.3), (-2.6, -1.3), "inside: a small computer\nTHINKS (Part 6)")]
for xy, xytext, text in labels:
    ax.annotate(text, xy=xy, xytext=xytext, fontsize=11, arrowprops=dict(arrowstyle="->"))
ax.set_xlim(-2.8, 3.3); ax.set_ylim(-1.6, 1.7); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig05-vacuum-sensors.png")

# ---------- Figure 6: how often different robots run their loop ----------
names = ["room\nthermostat", "robot\nvacuum", "warehouse\nrobot", "factory arm\n(joint motors)", "drone\n(tilt control)"]
rates = [0.2, 50, 100, 1000, 2000]
fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.bar(names, rates, color=[GREY, ORANGE, BLUE, GREEN, RED], edgecolor=BLACK)
ax.set_yscale("log"); ax.set_ylim(0.05, 20000)
for b, r in zip(bars, rates):
    label = "1 every 5 s" if r < 1 else f"about {r:,}"
    ax.text(b.get_x() + b.get_width() / 2, r * 1.4, label, ha="center", fontsize=11)
ax.set_yticks([0.1, 1, 10, 100, 1000, 10000])
ax.set_yticklabels(["0.1", "1", "10", "100", "1,000", "10,000"])
ax.set_ylabel("loops per second (log scale)")
ax.grid(axis="y", alpha=0.3)
save(fig, "fig06-loop-rates.png")

print("saved 6 figures in", os.path.normpath(OUT))
