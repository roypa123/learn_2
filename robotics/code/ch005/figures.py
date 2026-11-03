# Figures for Chapter 5 — The parts of a robot.
# Run:  python figures.py      (saves PNG files in ../../images/ch005/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle, Polygon

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch005")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6D0BF"
POWER = "#000000"   # thick black lines = power wires in this chapter's diagrams


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, face, size=11):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size)


def arrow(ax, p, q, colour=BLUE, lw=2.0, style="-|>"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=15, color=colour, lw=lw))


# ---------- Figure 1: five parts of a robot, and the same parts in a person ----------
fig, ax = plt.subplots(figsize=(12, 6.5))
rows = [("BODY", "frame, wheels, joints,\ncovers, mounts", "skeleton, skin", L_GREY),
        ("SENSORS", "camera, distance,\nbump, encoders, IMU", "eyes, ears, skin,\nbalance organs", L_BLUE),
        ("BRAIN (controller)", "microcontroller,\nsmall computer, program", "brain, nerves", L_ORANGE),
        ("ACTUATORS", "motors + motor drivers,\ngripper, speaker", "muscles", L_GREEN),
        ("POWER", "battery, switch, fuse,\nregulators, wires", "food, heart, blood", L_RED)]
ax.text(2.6, 5.55, "PART", ha="center", weight="bold"); ax.text(6.4, 5.55, "IN A ROBOT", ha="center", weight="bold")
ax.text(10.2, 5.55, "IN A PERSON", ha="center", weight="bold")
for i, (part, robot, person, face) in enumerate(rows):
    y = 4.4 - i * 1.1
    box(ax, 1.2, y, 2.8, 0.9, part, face, 12)
    box(ax, 4.6, y, 3.6, 0.9, robot, "white", 11)
    box(ax, 8.8, y, 2.8, 0.9, person, "white", 11)
    arrow(ax, (4.0, y + 0.45), (4.6, y + 0.45), GREY, 1.5); arrow(ax, (8.2, y + 0.45), (8.8, y + 0.45), GREY, 1.5, "<|-|>")
ax.set_xlim(1.0, 11.8); ax.set_ylim(-0.1, 5.8); ax.axis("off")
save(fig, "fig01-five-parts.png")

# ---------- Figure 2: Rover's block diagram (stage 3) ----------
fig, ax = plt.subplots(figsize=(14, 8))
box(ax, 0.2, 5.6, 2.6, 1.0, "BATTERY\n6 × AA, 7.2 V", L_RED, 12)
box(ax, 3.4, 5.6, 2.0, 1.0, "SWITCH\n+ FUSE", L_RED, 12)
box(ax, 6.0, 5.6, 2.6, 1.0, "5 V REGULATOR", L_RED, 12)
box(ax, 5.6, 2.9, 3.4, 1.6, "BRAIN\nArduino board\n(runs the loop)", L_ORANGE, 13)
box(ax, 10.4, 5.6, 3.0, 1.0, "MOTOR DRIVER\n(TB6612)", L_GREEN, 12)
box(ax, 10.4, 3.2, 1.4, 1.0, "LEFT\nMOTOR", L_GREEN, 11)
box(ax, 12.0, 3.2, 1.4, 1.0, "RIGHT\nMOTOR", L_GREEN, 11)
box(ax, 10.4, 1.4, 1.4, 1.0, "left\nencoder", L_BLUE, 11)
box(ax, 12.0, 1.4, 1.4, 1.0, "right\nencoder", L_BLUE, 11)
box(ax, 0.2, 3.6, 2.6, 0.9, "bumpers", L_BLUE, 12)
box(ax, 0.2, 2.4, 2.6, 0.9, "line sensor", L_BLUE, 12)
box(ax, 0.2, 1.2, 2.6, 0.9, "distance sensor", L_BLUE, 12)
# power (thick black)
for p, q in [((2.8, 6.1), (3.4, 6.1)), ((5.4, 6.1), (6.0, 6.1)), ((8.6, 6.1), (10.4, 6.1)), ((7.3, 5.6), (7.3, 4.5))]:
    ax.plot([p[0], q[0]], [p[1], q[1]], color=POWER, lw=4)
ax.plot([9.2, 9.2, 10.4], [6.1, 6.9, 6.9], color=POWER, lw=4)
ax.text(9.25, 7.0, "7.2 V straight to the driver\n(motors need the big power)", fontsize=10.5)
ax.text(7.4, 5.0, "5 V", fontsize=11)
ax.plot([6.4, 6.4, 1.5, 1.5], [5.6, 5.2, 5.2, 4.5], color=POWER, lw=2.5)
ax.text(1.6, 5.25, "5 V to sensors (from the regulator)", fontsize=10.5)
# signals (blue arrows)
for y in (4.05, 2.85, 1.65):
    arrow(ax, (2.8, y), (5.6, 3.7))
arrow(ax, (9.0, 4.3), (10.6, 5.6)); ax.text(9.1, 3.25, "commands →\n(speed,\ndirection)", fontsize=10.5, color=BLUE)
arrow(ax, (11.1, 5.6), (11.1, 4.2), GREEN, 3); arrow(ax, (12.7, 5.6), (12.7, 4.2), GREEN, 3)
ax.text(13.45, 4.9, "motor\npower", fontsize=10.5, color=GREEN)
arrow(ax, (11.1, 3.2), (11.1, 2.4), GREY, 1.5, "-"); arrow(ax, (12.7, 3.2), (12.7, 2.4), GREY, 1.5, "-")
ax.plot([11.1, 11.1, 9.6], [1.4, 0.95, 0.95], color=BLUE, lw=2)
ax.plot([12.7, 12.7, 11.1], [1.4, 0.95, 0.95], color=BLUE, lw=2)
arrow(ax, (9.6, 0.95), (8.4, 2.9))
ax.text(9.7, 0.6, "wheel counts (encoders)", fontsize=10.5, color=BLUE)
# legend
ax.plot([0.3, 1.1], [0.35, 0.35], color=POWER, lw=4); ax.text(1.25, 0.35, "power", va="center")
arrow(ax, (3.0, 0.35), (3.8, 0.35)); ax.text(3.95, 0.35, "signal (information)", va="center")
arrow(ax, (7.3, 0.35), (8.1, 0.35), GREEN, 3); ax.text(8.25, 0.35, "big power to motors", va="center")
ax.set_xlim(0, 14.2); ax.set_ylim(0, 7.6); ax.axis("off")
save(fig, "fig02-rover-block-diagram.png")

# ---------- Figure 3: three kinds of signal ----------
fig, axs = plt.subplots(3, 1, figsize=(10, 7.5), sharex=True)
t = [i / 100 for i in range(0, 401)]
digital = [5 if (1.0 <= x < 2.2 or x >= 3.1) else 0 for x in t]
analog = [2.5 + 1.8 * __import__("math").sin(2 * 3.14159 * x / 4.0) for x in t]
pwm = [5 if (x % 0.5) < 0.5 * (0.2 + 0.18 * x) else 0 for x in t]
for ax, y, title, colour in [(axs[0], digital, "DIGITAL: only two values, ON (5 V) or OFF (0 V) — e.g. a bump switch", BLUE),
                             (axs[1], analog, "ANALOG: any value in a range — e.g. a light sensor or a temperature sensor", BLUE),
                             (axs[2], pwm, "PWM: switched ON and OFF very fast; the ON part grows → the motor gets more power", GREEN)]:
    ax.plot(t, y, color=colour, lw=2.2); ax.set_ylim(-0.6, 5.8); ax.set_ylabel("volts")
    ax.set_title(title, fontsize=12, loc="left"); ax.grid(alpha=0.3)
axs[2].set_xlabel("time (seconds)")
fig.tight_layout()
save(fig, "fig03-signal-kinds.png")

# ---------- Figure 4: power budgets of Rover stage 3 and stage 7 ----------
parts = ["Arduino board", "motor driver", "2 drive motors", "line sensor", "distance sensor", "Raspberry Pi", "camera"]
stage3 = [0.25, 0.3, 3.0, 0.15, 0.08, 0, 0]
stage7 = [0.25, 0.3, 3.0, 0.15, 0.08, 4.0, 1.0]
colours = [ORANGE, GREEN, "#56B4E9", BLUE, "#CC79A7", RED, GREY]
fig, ax = plt.subplots(figsize=(10, 5.5))
for label, values, x in [("stage 3:\nRover feels", stage3, 0), ("stage 7:\nRover sees", stage7, 1)]:
    bottom = 0
    for v, c, name in zip(values, colours, parts):
        if v > 0:
            ax.bar(x, v, bottom=bottom, color=c, edgecolor=BLACK, width=0.5, label=name if x == 1 else None)
            bottom += v
    hours = 14.4 * 0.8 / bottom
    ax.text(x, bottom + 0.2, f"{bottom:.2f} W\n→ about {hours * 60:.0f} min", ha="center", fontsize=12)
ax.set_xticks([0, 1]); ax.set_xticklabels(["stage 3: Rover feels", "stage 7: Rover sees"])
ax.set_ylabel("power while driving (watts)"); ax.set_ylim(0, 11); ax.set_xlim(-0.6, 2.2)
ax.legend(loc="upper right", fontsize=10.5); ax.grid(axis="y", alpha=0.3)
save(fig, "fig04-power-budget.png")

# ---------- Figure 5: Rover from the side, centre of mass for two battery places ----------
fig, axs = plt.subplots(2, 1, figsize=(10, 6.5))
for ax, bat_x, com, title, ok in [(axs[0], 5, 0.82, "design A: battery in the FRONT", False),
                                  (axs[1], -5, -2.23, "design B: battery in the BACK", True)]:
    ax.plot([-14, 12], [0, 0], color=GREY, lw=2)                                 # floor
    ax.add_patch(Rectangle((-11, 3.2), 21, 2.0, fc=ORANGE, ec=BLACK, alpha=0.7))   # chassis plate
    ax.add_patch(Circle((0, 3.2), 3.2, fc=BLACK))                                 # big wheel at the axle (x = 0)
    ax.add_patch(Circle((-9, 1.0), 1.0, fc=GREY, ec=BLACK))                        # caster
    ax.plot([-9, -9], [2.0, 3.2], color=BLACK, lw=2)
    ax.add_patch(Rectangle((bat_x - 3, 5.2), 6, 2.2, fc=L_RED, ec=BLACK)); ax.text(bat_x, 6.3, "battery", ha="center")
    ax.add_patch(Rectangle((6, 2.2), 2.0, 1.0, fc=L_BLUE, ec=BLACK))             # sensors, under the front edge
    ax.text(7.0, 1.6, "sensors", ha="center", va="center", fontsize=10)
    ax.add_patch(Rectangle((-7.5, 2.2), 4, 1.0, fc=L_ORANGE, ec=BLACK))          # Arduino, under the plate
    ax.text(-5.5, 2.7, "Arduino", ha="center", va="center", fontsize=10)
    ax.fill_between([-9, 0], -0.6, -0.1, color=L_GREEN if ok else L_GREEN, alpha=0.9)
    ax.text(-4.5, -1.4, "support: from caster (−9 cm) to wheel axle (0 cm)", ha="center", fontsize=10.5)
    ax.plot([com, com], [-0.4, 8.6], color=RED, ls="--", lw=2)
    ax.scatter(com, 8.6, s=160, color=RED, marker="v", zorder=4)
    ax.text(com + 0.4, 8.4, f"centre of mass: {com:+.2f} cm", color=RED, fontsize=11)
    ax.set_title(title + ("  →  STABLE" if ok else "  →  tips forward onto its nose"), fontsize=12, loc="left")
    ax.set_xlim(-14, 13); ax.set_ylim(-2.2, 9.6); ax.set_aspect("equal"); ax.axis("off")
fig.tight_layout()
save(fig, "fig05-centre-of-mass.png")

# ---------- Figure 6: one trip around the loop, inside Rover (time line) ----------
steps = [("read sensors", 0.0, 2.0, L_BLUE), ("decide (program)", 2.0, 1.0, L_ORANGE),
         ("send commands to driver", 3.0, 0.5, L_ORANGE), ("motors respond", 3.5, 15.0, L_GREEN),
         ("wait for next loop", 3.5, 16.5, L_GREY)]
fig, ax = plt.subplots(figsize=(11, 3.8))
for k, (name, start, length, face) in enumerate(steps):
    ax.barh(len(steps) - 1 - k, length, left=start, color=face, edgecolor=BLACK)
    ax.text(start + length + 0.3, len(steps) - 1 - k, f"{name} ({length:g} ms)", va="center", fontsize=11)
ax.axvline(20, color=BLACK, ls="--"); ax.text(20.2, 4.3, "next loop starts\nat 20 ms", fontsize=11)
ax.set_yticks([]); ax.set_xlabel("time (milliseconds, ms) — one loop = 20 ms = 50 loops per second")
ax.set_xlim(0, 34); ax.grid(axis="x", alpha=0.3)
save(fig, "fig06-one-loop-timeline.png")

print("saved 6 figures in", os.path.normpath(OUT))
