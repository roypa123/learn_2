# Figures for Chapter 110 - Libraries and how they work inside.
# Run:  python figures.py      (saves PNG files in ../../images/ch110/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch110")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6CBB5"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, fc, fs=11, family=None):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=BLACK))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, family=family)


def arrow(ax, a, b, col=BLACK):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=13, lw=1.6, color=col))


# Figure 1: the folders and files of a library
fig, ax = plt.subplots(figsize=(11, 4.8))
lines = [(0, "RoverLib/", "the library's folder (its name)", BLACK),
         (1, "library.properties", "name, version, author, a one-line description", GREY),
         (1, "src/", "the code", BLACK),
         (2, "RoverLib.h", "#include this one: it includes the others", BLUE),
         (2, "Debouncer.h", "the class's description (the 'menu')", BLUE),
         (2, "Debouncer.cpp", "how its functions work (the 'kitchen')", GREEN),
         (2, "BatteryMonitor.h", "", BLUE),
         (2, "BatteryMonitor.cpp", "", GREEN),
         (1, "examples/", "sketches that show how to use it", BLACK),
         (2, "BumpersAndBattery/BumpersAndBattery.ino", "", ORANGE)]
for k, (depth, name, note, col) in enumerate(lines):
    y = 9.3 - k
    ax.text(0.3 + depth * 0.8, y, name, fontsize=12, family="monospace", color=col, va="center")
    if note:
        ax.text(6.3, y, note, fontsize=10.5, va="center", color=GREY if col == GREY else BLACK)
    if depth:
        ax.plot([0.15 + (depth - 1) * 0.8 + 0.2, 0.15 + depth * 0.8], [y, y], color=GREY, lw=1)
ax.set_xlim(0, 12); ax.set_ylim(-0.5, 10); ax.axis("off")
save(fig, "fig01-library-folder.png")

# Figure 2: compile each .cpp separately, then link
fig, ax = plt.subplots(figsize=(12, 4.6))
srcs = [("BumpersAndBattery.ino", L_ORANGE, 3.2), ("Debouncer.cpp", L_GREEN, 1.9), ("BatteryMonitor.cpp", L_GREEN, 0.6)]
for name, col, y in srcs:
    box(ax, 0.0, y, 3.0, 0.9, name, col, 10.5, "monospace")
    arrow(ax, (3.05, y + 0.45), (4.4, y + 0.45))
    box(ax, 4.45, y, 2.2, 0.9, "compiler", L_GREY, 10.5)
    arrow(ax, (6.7, y + 0.45), (7.9, y + 0.45))
    box(ax, 7.95, y, 1.8, 0.9, "machine\ncode", "white", 10)
    arrow(ax, (9.8, y + 0.45), (10.4, 2.35))
box(ax, 10.45, 1.9, 1.5, 0.9, "linker", L_GREY, 10.5)
arrow(ax, (12.0, 2.35), (12.6, 2.35))
box(ax, 12.65, 1.75, 1.6, 1.2, "one\nprogram\n(.hex)", L_BLUE, 10.5)
box(ax, 0.6, 4.55, 4.6, 0.75, "Debouncer.h and BatteryMonitor.h", L_BLUE, 10, "monospace")
ax.text(5.4, 4.92, "#included by all three, so each knows the classes' shape", fontsize=10, va="center")
ax.set_xlim(-0.2, 14.4); ax.set_ylim(0.4, 5.5); ax.axis("off")
save(fig, "fig02-compile-link.png")

# Figure 3: one class, several objects
fig, ax = plt.subplots(figsize=(12, 4.4))
box(ax, 0.2, 1.0, 3.4, 2.8, "", L_BLUE)
ax.text(1.9, 3.45, "class Debouncer", ha="center", fontsize=12, family="monospace")
ax.text(0.45, 2.65, "data:\n  _pin, _stable, _last,\n  _changedAt, _presses", fontsize=10, va="center", family="monospace")
ax.text(0.45, 1.5, "functions:\n  begin(), update(),\n  isPressed(), presses()", fontsize=10, va="center", family="monospace")
for k, (name, pin, presses) in enumerate([("leftBumper", 4, 2), ("rightBumper", 5, 1)]):
    y = 2.6 - k * 1.7
    box(ax, 6.0, y, 4.4, 1.3, "", L_GREEN)
    ax.text(8.2, y + 1.0, f"object {name}", ha="center", fontsize=11, family="monospace")
    ax.text(6.2, y + 0.45, f"_pin = {pin}   _presses = {presses}\n_stable = HIGH  ...", fontsize=10, va="center", family="monospace")
    arrow(ax, (3.65, 2.4), (5.95, y + 0.65))
ax.text(4.8, 3.35, "made from", ha="center", fontsize=10)
ax.text(10.6, 2.0, "same functions,\nseparate data:\neach remembers\nits own button", fontsize=10.5, va="center")
ax.set_xlim(0, 12.6); ax.set_ylim(0.6, 4.1); ax.axis("off")
save(fig, "fig03-class-objects.png")

# Figure 4: naive timing drifts; planned timing does not ('R' = 0x52 at 19200 baud)
bits = [0] + [(0x52 >> k) & 1 for k in range(8)] + [1]
T = 1e6 / 19200
fig, axes = plt.subplots(2, 1, figsize=(12, 5.0), sharex=True)
for ax, per, title in [(axes[0], 56.0, "simple version: each bit = delayMicroseconds(52) + digitalWrite (4 us) = 56 us"),
                       (axes[1], T, "fixed version: each bit starts at its planned time (k x 52 us)")]:
    xs, ys = [-40, 0], [1, 1]
    for k, b in enumerate(bits):
        xs += [k * per, (k + 1) * per]; ys += [b, b]
    xs += [12 * T]; ys += [1]
    ax.step(xs, ys, where="post", color=BLUE, lw=2)
    for k in range(9):
        t = (k + 1.5) * T
        sent = int(t // per)
        ok = sent == k + 1
        ax.plot([t], [0.5], "o", color=GREEN if ok else RED, ms=9)
    ax.set_title(title, fontsize=10.5); ax.set_yticks([0, 1]); ax.set_yticklabels(["LOW", "HIGH"]); ax.set_ylim(-0.25, 1.3)
axes[1].set_xlabel("time (us); dots: where a 19,200 baud receiver reads (red = it reads the wrong bit)")
save(fig, "fig04-bit-timing.png")

# Figure 5: interrupts paused for a whole character: a fast encoder (3,000 pulses per second) loses pulses
fig, ax = plt.subplots(figsize=(12, 3.8))
windows = [(0.2, 0.2 + 1.0417), (1.4, 1.4 + 1.0417)]
for k, (a, b) in enumerate(windows):
    ax.add_patch(Rectangle((a, 1.6), b - a, 0.6, fc=L_RED, ec=RED))
    ax.text((a + b) / 2, 1.9, "one character at 9600 baud:\ninterrupts paused 1.04 ms" if k == 0 else "the next character",
            ha="center", va="center", fontsize=10)
pulses = np.arange(0.05, 2.6, 1 / 3.0)
waiting = set()
for p in pulses:
    win = [w for w in windows if w[0] <= p < w[1]]
    if not win:
        col = GREEN
    elif win[0] not in waiting:
        col = ORANGE
        waiting.add(win[0])
    else:
        col = RED
    ax.plot([p, p], [0.6, 1.2], color=col, lw=2.5)
ax.text(0.0, 0.3, "encoder pulses, 3,000 per second:  green = counted at once;  orange = waits until the character ends;"
        "  red = lost", fontsize=9.5)
ax.set_xlim(-0.05, 2.7); ax.set_ylim(0.1, 2.5); ax.set_yticks([]); ax.set_xlabel("time (ms)")
for s in ["left", "right", "top"]:
    ax.spines[s].set_visible(False)
save(fig, "fig05-interrupts-off.png")

# Figure 6: RoverLib's example on the PC test bench: two bouncing bumpers, three presses detected
t = np.linspace(0, 1200, 24001)


def bouncy(presses, ms):
    edges = [0.0, 0.08, 0.15, 0.35, 0.45, 0.70, 0.85]
    out = np.ones_like(ms)
    for d, u in presses:
        for i, x in enumerate(ms):
            if d <= x < u:
                f = (x - d) / 3.0
                k = sum(1 for e in edges if e <= f) if f < 1 else 1
                out[i] = 0 if (f >= 1 or k % 2 == 1) else 1
    return out


fig, ax = plt.subplots(figsize=(11, 3.8))
ax.plot(t, bouncy([(200, 400), (900, 1100)], t) + 1.6, color=BLUE, lw=1.5, drawstyle="steps-post")
ax.plot(t, bouncy([(600, 700)], t), color=ORANGE, lw=1.5, drawstyle="steps-post")
for x, y in [(207, 1.6), (907, 1.6), (607, 0.0)]:
    ax.plot([x], [y + 0.5], "v", color=RED, ms=10)
ax.text(1150, 2.1, "left (pin 4)", ha="right", color=BLUE, fontsize=10.5)
ax.text(1150, 0.5, "right (pin 5)", ha="right", color=ORANGE, fontsize=10.5)
ax.set_yticks([]); ax.set_xlabel("time (ms); red marks: \"pressed\" reported, 7 ms after each press began")
save(fig, "fig06-example-run.png")
print("figures saved in", os.path.abspath(OUT))
