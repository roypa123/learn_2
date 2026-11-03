# Figures for Chapter 9 — Simulation or real hardware: what you need (and what is optional).
# Run:  python figures.py      (saves PNG files in ../../images/ch009/)
import os
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch009")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})   # "$" means dollars here, not maths
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
PURPLE, SKY = "#CC79A7", "#56B4E9"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, face, size=11):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size)


def arrow(ax, p, q, colour=GREY, lw=2.0, label=None, lpos=None, lcol=BLACK):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=15, color=colour, lw=lw))
    if label:
        ax.text(lpos[0], lpos[1], label, ha="center", fontsize=11, style="italic", color=lcol)


# ---------- Figure 1: one controller, two worlds ----------
fig, ax = plt.subplots(figsize=(13, 6.5))
box(ax, 0.0, 2.4, 3.2, 1.6, "YOUR CONTROLLER\n(the 'think' part)\ncommand = gain x error", L_ORANGE, 11.5)
box(ax, 5.2, 4.2, 4.4, 1.9, "SIMULATED WORLD (computer)\nPython model, Wokwi, Gazebo,\nWebots, MuJoCo, Isaac Sim", L_BLUE, 11)
box(ax, 5.2, 0.3, 4.4, 1.9, "REAL WORLD (hardware)\nArduino, motors, sensors,\nbattery, floor, walls", L_GREEN, 11)
arrow(ax, (3.2, 3.4), (5.2, 5.0), ORANGE, label="commands", lpos=(3.9, 4.55), lcol=ORANGE)
arrow(ax, (5.2, 4.6), (3.2, 3.1), BLUE, label="simulated\nmeasurements", lpos=(4.6, 3.45), lcol=BLUE)
arrow(ax, (3.2, 3.0), (5.2, 1.6), ORANGE)
arrow(ax, (5.2, 1.0), (3.2, 2.5), GREEN, label="real\nmeasurements", lpos=(3.75, 1.2), lcol=GREEN)
ax.text(10.0, 5.6, "+ free, fast, safe\n+ repeat exactly, try 1,000 times\n+ see hidden values\n- only as true as the model",
        fontsize=11, va="top", color=BLUE)
ax.text(10.0, 1.8, "+ the truth: noise, friction,\n   weak batteries, loose wires\n- costs money, slow, can break\n- can hurt (Chapter 7)",
        fontsize=11, va="top", color=GREEN)
ax.text(6.5, 6.7, "The SAME controller can drive a simulated robot or a real one", ha="center", fontsize=13.5, weight="bold")
ax.set_xlim(-0.2, 13.6); ax.set_ylim(0.0, 7.1); ax.axis("off")
save(fig, "fig01-one-controller-two-worlds.png")

# ---------- Figure 2: perfect vs real world (same model as sim_vs_real.py) ----------
random.seed(1)
traces = {}
for world in ["perfect", "real"]:
    distance = 1.0; ds = []
    for step in range(61):
        ds.append(distance)
        measured = distance
        if world == "real":
            measured = distance + random.uniform(-0.01, 0.01)
        command = max(0.0, min(0.25, 2.0 * (measured - 0.3)))
        speed = command
        if world == "real":
            speed = 0.85 * command
            if command < 0.05:
                speed = 0.0
        distance = distance - speed * 0.1
    ds.append(distance)
    traces[world] = ds
t = [i * 0.1 for i in range(62)]
fig, axes = plt.subplots(1, 2, figsize=(14, 5.6))
for ax, (lo, hi) in zip(axes, [(0.2, 1.05), (0.28, 0.36)]):
    ax.axhline(0.3, color=BLACK, ls="--", lw=2, label="setpoint 0.3 m")
    ax.plot(t, traces["perfect"], color=GREY, lw=2.5, label="perfect simulation")
    ax.plot(t, traces["real"], color=BLUE, lw=2.5, label="'real' Rover (noise, weak motors, friction)")
    ax.set_xlabel("time (s)"); ax.set_ylabel("distance to the wall (m)")
    ax.set_ylim(lo, hi); ax.grid(alpha=0.3)
axes[0].set_title("The whole run"); axes[0].legend(fontsize=10.5, loc="upper right")
axes[1].set_title("Zoom on the end (note the scale)")
axes[1].annotate("stuck at 0.315 m:\nthe command became\ntoo small to beat friction", xy=(5.0, traces["real"][50]),
                 xytext=(3.65, 0.338), fontsize=11, color=BLUE, arrowprops=dict(arrowstyle="->", color=BLUE))
save(fig, "fig02-perfect-vs-real.png")

# ---------- Figure 3: 100 different Rovers (same model as robust_test.py) ----------
random.seed(2)
results = {}
for gain in [2.0, 4.0, 8.0]:
    pts = []
    for trial in range(100):
        strength = random.uniform(0.6, 1.2)
        stiction = random.uniform(0.0, 0.08)
        distance = 1.0
        for step in range(100):
            measured = distance + random.uniform(-0.01, 0.01)
            command = max(0.0, min(0.25, gain * (measured - 0.3)))
            speed = strength * command
            if command < stiction:
                speed = 0.0
            distance = distance - speed * 0.1
        pts.append((stiction, distance - 0.3))
    results[gain] = pts
fig, ax = plt.subplots(figsize=(11.5, 6.2))
ax.axhspan(-0.02, 0.02, color=L_GREEN, alpha=0.7, label="good enough: within 2 cm")
for gain, colour, mk in [(2.0, RED, "o"), (4.0, BLUE, "s"), (8.0, GREEN, "^")]:
    xs = [p[0] for p in results[gain]]; ys = [p[1] * 100 / 100 for p in results[gain]]
    n = sum(1 for p in results[gain] if abs(p[1]) <= 0.02)
    ax.scatter(xs, ys, color=colour, marker=mk, s=28, alpha=0.8, label=f"gain {gain:.0f}: {n} of 100 pass")
ax.axhline(0, color=BLACK, ls="--", lw=1.5)
ax.set_xlabel("this Rover's friction: the smallest command that makes the wheels turn (m/s)")
ax.set_ylabel("final error: distance - setpoint (m)")
ax.set_title("One controller tested on 100 slightly different Rovers")
ax.legend(loc="upper left", fontsize=10.5); ax.grid(alpha=0.3)
save(fig, "fig03-hundred-rovers.png")

# ---------- Figure 4: Rover's parts budget ----------
parts = ["Arduino Uno (compatible)", "TB6612 motor driver", "2WD chassis + 2 gearmotors\nwith encoders",
         "6 x AA NiMH cells + holder", "NiMH charger", "switch, fuse holder,\n4 A slow fuses",
         "e-stop button", "5 V regulator", "line sensor", "distance sensor (ToF)",
         "2 bumper switches", "wires, screws, tape"]
low = [12, 4, 15, 12, 12, 4, 5, 3, 4, 5, 2, 5]
high = [25, 8, 25, 20, 20, 7, 10, 6, 8, 10, 4, 10]
fig, ax = plt.subplots(figsize=(11.5, 7.2))
y = list(range(len(parts)))[::-1]
ax.barh(y, low, color=ORANGE, ec=BLACK, label="cheapest typical price")
ax.barh(y, [h - l for h, l in zip(high, low)], left=low, color=L_ORANGE, ec=BLACK, label="up to (more expensive)")
for yi, l, h in zip(y, low, high):
    ax.text(h + 0.4, yi, f"${l}-{h}", va="center", fontsize=10.5)
ax.set_yticks(y); ax.set_yticklabels(parts, fontsize=10.5)
ax.set_xlabel("price (US dollars, 2026, rough)")
ax.set_title(f"Rover stage 3: total ${sum(low)} to ${sum(high)}")
ax.set_xlim(0, 30); ax.legend(loc="lower right", fontsize=10.5); ax.grid(axis="x", alpha=0.3)
save(fig, "fig04-rover-budget.png")

# ---------- Figure 5: when you need to buy what (cumulative) ----------
items = [(81, 30, "multimeter +\nsoldering iron"), (94, 40, "Arduino\nstarter kit"), (114, 20, "sensors"),
         (143, 20, "servos"), (152, 50, "Rover base"), (447, 85, "LiDAR"), (498, 105, "Pi + camera"),
         (527, 20, "ESP32 + CAN"), (614, 225, "drone kit"), (667, 90, "Quad servos"), (691, 185, "Buddy kit")]
fig, ax = plt.subplots(figsize=(13, 6.2))
xs, ys, total = [0], [0], 0
for ch, cost, name in items:
    xs += [ch, ch]; ys += [total, total + cost]; total += cost
xs.append(749); ys.append(total)
ax.plot(xs, ys, color=ORANGE, lw=3)
ax.fill_between(xs, ys, color=L_ORANGE, alpha=0.5)
running = 0
key = []
for i, (ch, cost, name) in enumerate(items):
    running += cost
    ax.text(ch, running + 15, str(i + 1), ha="center", va="bottom", fontsize=10.5, weight="bold",
            bbox=dict(fc="white", ec=ORANGE, boxstyle="circle,pad=0.2"))
    key.append(f"{i + 1:>2}. Ch {ch}: {name.replace(chr(10), ' ')} (+${cost})")
ax.text(170, total * 1.08, "\n".join(key), va="top", fontsize=10.5, family="DejaVu Sans Mono",
        bbox=dict(fc="white", ec=GREY))
ax.axvspan(0, 36, color=L_BLUE, alpha=0.6)
ax.text(18, total * 0.55, "Parts 1-2:\n$0", ha="center", fontsize=11, color=BLUE, weight="bold")
ax.set_xlabel("chapter"); ax.set_ylabel("money spent so far (US dollars, middle of each price range)")
ax.set_title(f"Full hardware track, bought only when needed: about ${total} over the whole course")
ax.set_xlim(0, 760); ax.set_ylim(0, total * 1.15); ax.grid(alpha=0.3)
save(fig, "fig05-cost-over-the-course.png")

# ---------- Figure 6: choose your path ----------
fig, ax = plt.subplots(figsize=(13.5, 7))
box(ax, 4.6, 5.6, 4.4, 1.1, "Can you spend money on parts now?", L_GREY, 12)
box(ax, 0.0, 2.6, 4.0, 2.0, "PATH A\nSimulation only\n$0\nevery chapter's\nsimulation track", L_BLUE, 11.5)
box(ax, 4.8, 2.6, 4.0, 2.0, "PATH B\nStarter hardware\nabout $100-200\nstarter kit + tools\n+ Rover base", L_GREEN, 11.5)
box(ax, 9.6, 2.6, 4.0, 2.0, "PATH C\nFull hardware\nbuy each kit\nwhen its part starts\n(Figure 9.3)", L_ORANGE, 11.5)
arrow(ax, (5.6, 5.6), (2.0, 4.6), GREY, label="no", lpos=(3.4, 5.25))
arrow(ax, (6.8, 5.6), (6.8, 4.6), GREY, label="a little", lpos=(7.55, 5.05))
arrow(ax, (8.0, 5.6), (11.6, 4.6), GREY, label="yes", lpos=(10.2, 5.25))
for x, t in [(2.0, "You learn all the ideas.\nSwitch to B any time:\nyour code stays useful."),
             (6.8, "Real robot experience\nfor the core: sensors,\nmotors, control, Rover."),
             (11.6, "Drone, Quad, Buddy\nonly with an adult and\nthe safety rules (Ch 7).")]:
    ax.text(x, 2.35, t, ha="center", va="top", fontsize=10.5)
ax.text(6.8, 0.25, "Every path uses the same chapters. You can change path at any time.", ha="center", fontsize=12.5, weight="bold")
ax.set_xlim(-0.2, 13.8); ax.set_ylim(0, 7.0); ax.axis("off")
save(fig, "fig06-choose-your-path.png")
print("figures saved in", os.path.abspath(OUT))
