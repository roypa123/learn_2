# Figures for Chapter 96 - C++ for Arduino part 1: setup, loop, variables, types.
# Run:  python figures.py      (saves PNG files in ../../images/ch096/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch, Wedge
from matplotlib.ticker import NullFormatter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch096")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6CBB5"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, fc, ec=BLACK, fs=11, weight="normal", r=0.12):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.02,rounding_size={r}", fc=fc, ec=ec, lw=1.5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, weight=weight)


def arrow(ax, x1, y1, x2, y2, color=BLACK, lw=1.8, style="-|>"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=16, color=color, lw=lw))


# Figure 1: the same program in Python and in C++
py = ["# count up and blink", "count = 0", "", "", "while True:", "    count = count + 1",
      "    print(count)", "    led_on()", "    time.sleep(0.5)", ""]
cpp = ["// count up and blink", "int count = 0;", "", "void loop() {", "", "  count = count + 1;",
       "  Serial.println(count);", "  digitalWrite(13, HIGH);", "  delay(500);", "}"]
fig, axes = plt.subplots(1, 2, figsize=(13, 5.6))
for ax, lines, title, col in [(axes[0], py, "Python (Part 2)", L_BLUE), (axes[1], cpp, "C++ on the Arduino", L_ORANGE)]:
    ax.add_patch(Rectangle((0, 0), 10, 10.5, fc=col, ec=BLACK))
    ax.text(5, 10.9, title, ha="center", fontsize=13, weight="bold")
    for k, line in enumerate(lines):
        ax.text(0.3, 9.8 - k * 0.95, line, fontsize=12, family="monospace", va="center")
    ax.set_xlim(-0.2, 10.4); ax.set_ylim(-2.0, 11.8); ax.axis("off")
for y_line, x_char, y_text, text in [(9.8, 0.4, 11.2, "comments start with //"), (8.85, 0.65, 9.9, "a new variable needs a TYPE: int"),
                                     (8.85, 3.35, 8.6, "every statement ends with ;"), (6.95, 3.15, 6.95, "{ starts a block ..."),
                                     (1.25, 0.4, 1.25, "... } ends it")]:
    axes[1].annotate(text, xy=(x_char, y_line - 0.25), xytext=(11.0, y_text),
                     fontsize=11, color=RED, va="center", arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.2))
axes[1].set_xlim(-0.2, 17.5)
axes[0].text(5, -1.0, "indentation decides the block", ha="center", fontsize=11, color=BLUE)
axes[1].text(5, -1.0, "indentation is only for people; the compiler ignores it", ha="center", fontsize=10.5, color=GREY)
save(fig, "fig01-python-vs-cpp.png")

# Figure 2: the hidden main() that calls setup() and loop()
fig, ax = plt.subplots(figsize=(11, 5.4))
box(ax, 0.2, 3.6, 2.6, 1.0, "power on\nor reset", L_GREY)
box(ax, 3.6, 3.6, 2.8, 1.0, "init()\nArduino starts its timers", L_GREY, fs=10)
box(ax, 7.2, 3.6, 2.6, 1.0, "setup()\nYOUR code, once", L_GREEN, weight="bold")
box(ax, 7.2, 1.2, 2.6, 1.0, "loop()\nYOUR code", L_ORANGE, weight="bold")
box(ax, 3.6, 1.2, 2.8, 1.0, "small jobs of the\nArduino (serialEvent)", L_GREY, fs=10)
arrow(ax, 2.85, 4.1, 3.55, 4.1); arrow(ax, 6.45, 4.1, 7.15, 4.1); arrow(ax, 8.5, 3.55, 8.5, 2.25)
arrow(ax, 7.15, 1.7, 6.45, 1.7)
ax.annotate("", xy=(8.5, 1.15), xytext=(5.0, 1.15), arrowprops=dict(arrowstyle="-|>", color=BLACK, lw=1.8,
            connectionstyle="arc3,rad=0.5"))
ax.text(6.8, -0.45, "for ever: until the power goes off", ha="center", fontsize=11)
ax.text(5.0, 5.3, "hidden main() inside the Arduino software", ha="center", fontsize=12, color=BLUE)
ax.set_xlim(0, 10); ax.set_ylim(-0.8, 5.7); ax.axis("off")
save(fig, "fig02-hidden-main.png")

# Figure 3: the types as boxes of bytes
types = [("bool", 1, "true or false", L_GREY), ("char", 1, "-128 to 127 (a letter)", L_GREY),
         ("byte", 1, "0 to 255", L_GREEN), ("int", 2, "-32,768 to 32,767", L_BLUE),
         ("unsigned int", 2, "0 to 65,535", L_BLUE), ("long", 4, "about -2.1 to +2.1 billion", L_ORANGE),
         ("unsigned long", 4, "0 to about 4.29 billion", L_ORANGE), ("float", 4, "about 7 digits, up to 3.4 x 10^38", L_RED)]
fig, ax = plt.subplots(figsize=(12, 5.8))
for k, (name, n, rng, col) in enumerate(types):
    y = 7 - k
    ax.text(2.2, y + 0.4, name, ha="right", va="center", fontsize=12, family="monospace")
    for j in range(n):
        ax.add_patch(Rectangle((2.5 + j * 1.0, y + 0.05), 0.95, 0.7, fc=col, ec=BLACK))
        ax.text(2.97 + j * 1.0, y + 0.4, "8 bits", ha="center", va="center", fontsize=8.5)
    ax.text(6.8, y + 0.4, rng, va="center", fontsize=11.5)
ax.text(4.5, 8.2, "bytes of SRAM (each box = 1 byte)", ha="center", fontsize=11)
ax.set_xlim(0, 12); ax.set_ylim(-0.3, 8.6); ax.axis("off")
save(fig, "fig03-type-sizes.png")

# Figure 4: int overflow as a circle of numbers
fig, ax = plt.subplots(figsize=(7.5, 7.5))
ax.add_patch(Wedge((0, 0), 1.0, 90, 270, width=0.18, fc=L_RED, ec=BLACK))
ax.add_patch(Wedge((0, 0), 1.0, -90, 90, width=0.18, fc=L_BLUE, ec=BLACK))
for value, ang, lab_ang, ha in [(0, 89, 80, "left"), (16384, 0, 0, "left"), (32767, -89, -80, "left"),
                                (-32768, -91, -100, "right"), (-16384, 180, 180, "right"), (-1, 91, 100, "right")]:
    a, la = math.radians(ang), math.radians(lab_ang)
    ax.plot([0.82 * math.cos(a), 1.0 * math.cos(a)], [0.82 * math.sin(a), 1.0 * math.sin(a)], color=BLACK, lw=1.5)
    ax.text(1.1 * math.cos(la), 1.1 * math.sin(la), f"{value:,}", ha=ha, va="center", fontsize=12)
ax.annotate("", xy=(-0.12, -0.72), xytext=(0.12, -0.72), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2.5))
ax.text(0, -0.55, "+1", ha="center", fontsize=13, color=RED, weight="bold")
ax.text(0.45, 0.05, "positive\nnumbers", ha="center", fontsize=12, color=BLUE)
ax.text(-0.45, 0.05, "negative\nnumbers", ha="center", fontsize=12, color=RED)
ax.annotate("", xy=(0.66, 0.66), xytext=(0.75, -0.55), arrowprops=dict(arrowstyle="<|-", color=GREY, lw=1.5,
            connectionstyle="arc3,rad=0.35"))
ax.text(0.0, 1.45, "an int on the Uno: 65,536 numbers on a circle", ha="center", fontsize=12)
ax.text(0.0, -1.45, "counting up past 32,767 jumps to -32,768", ha="center", fontsize=12, color=RED)
ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.6, 1.6); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig04-int-circle.png")

# Figure 5: the 300 * 200 bug, step by step
fig, ax = plt.subplots(figsize=(12, 4.6))
box(ax, 0.0, 2.6, 1.6, 0.9, "rpm\nint 300", L_BLUE)
box(ax, 0.0, 1.1, 1.6, 0.9, "seconds\nint 200", L_BLUE)
box(ax, 2.6, 1.8, 2.2, 1.0, "int * int\nis done in int", L_BLUE)
box(ax, 5.8, 1.8, 2.4, 1.0, "60,000 does not fit:\nit becomes -5,536", L_RED)
box(ax, 9.2, 1.8, 2.2, 1.0, "long turns\n= -5,536", L_ORANGE)
arrow(ax, 1.65, 3.0, 2.55, 2.5); arrow(ax, 1.65, 1.55, 2.55, 2.1); arrow(ax, 4.85, 2.3, 5.75, 2.3); arrow(ax, 8.25, 2.3, 9.15, 2.3)
ax.text(5.7, 0.55, "Fix: (long)rpm * seconds  -  one side is a long BEFORE multiplying, so the sum is done in long: 60,000",
        ha="center", fontsize=11, color=GREEN)
ax.text(5.7, 3.7, "The type of the answer is decided by the numbers going IN, not by the box it goes into", ha="center",
        fontsize=11.5)
ax.set_xlim(-0.2, 11.6); ax.set_ylim(0.2, 4.1); ax.axis("off")
save(fig, "fig05-multiply-bug.png")

# Figure 6: division and remainder on a number line, C++ against Python
fig, axes = plt.subplots(2, 1, figsize=(11, 4.8))
for ax, title, vals in [(axes[0], "7 / 2 and 7 % 2: both languages agree", [(7, 3, 1, 3, 1)]),
                        (axes[1], "-7 / 2: C++ gives -3 remainder -1;  Python's // gives -4 remainder 1", [(-7, -3, -1, -4, 1)])]:
    ax.axhline(0, color=BLACK, lw=1)
    for x in range(-9, 10):
        ax.plot([x, x], [-0.08, 0.08], color=BLACK, lw=1)
        ax.text(x, -0.3, str(x), ha="center", fontsize=10)
    n, q_c, r_c, q_p, r_p = vals[0]
    ax.plot([n], [0], "o", color=RED, ms=10)
    ax.annotate("", xy=(2 * q_c, 0.35), xytext=(0, 0.35), arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2.5))
    ax.text(q_c, 0.55, f"C++: {q_c} x 2 = {2 * q_c}, remainder {r_c}", ha="center", fontsize=10.5, color=ORANGE)
    if q_p != q_c:
        ax.annotate("", xy=(2 * q_p, -0.55), xytext=(0, -0.55), arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2.5))
        ax.text(q_p, -0.85, f"Python: {q_p} x 2 = {2 * q_p}, remainder {r_p}", ha="center", fontsize=10.5, color=BLUE)
    ax.set_title(title, fontsize=12)
    ax.set_xlim(-9.5, 9.5); ax.set_ylim(-1.1, 0.9); ax.axis("off")
fig.tight_layout()
save(fig, "fig06-division.png")

# Figure 7: Rover's distance: from the tick count, or added up tick by tick (float32, the same as the Uno)
step = np.float32(0.207) / np.float32(540)
n_total = 1_000_000
marks = np.unique(np.round(np.logspace(2, 6, 60)).astype(int))
added = np.float32(0.0)
errs, xs = [], []
k = 0
for n in range(1, n_total + 1):
    added = np.float32(added + step)
    if n == marks[k]:
        true = float(np.float32(n) * step)
        xs.append(true); errs.append((float(added) - true) * 100)       # cm
        k += 1
        if k == len(marks):
            break
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(xs, errs, color=RED, lw=2.5, label="added up tick by tick (float)")
ax.axhline(0, color=GREEN, lw=2.5, ls="--", label="computed from a long tick count")
ax.set_xscale("log"); ax.set_xticks([0.1, 1, 10, 100, 1000]); ax.set_xticklabels(["0.1", "1", "10", "100", "1,000"])
ax.xaxis.set_minor_formatter(NullFormatter())
ax.set_xlabel("distance Rover has driven (m, log scale)"); ax.set_ylabel("error in the distance (cm)")
ax.legend(loc="upper left", fontsize=11); ax.grid(alpha=0.3)
save(fig, "fig07-odometry-error.png")

# Figure 8: the timer bug (numbers from timer_bug.ino on the PC test bench)
t = [5, 10, 15, 20, 25, 30, 35, 40]
bad = [49, 50, 51, 50, 50, 49, 366692, 832791]
good = [49, 51, 50, 50, 50, 49, 51, 50]
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.bar([x - 0.9 for x in t], bad, width=1.7, color=RED, label="last time kept in an int")
ax.bar([x + 0.9 for x in t], good, width=1.7, color=BLUE, hatch="//", ec="white", label="last time kept in an unsigned long")
ax.axvline(32.767, color=BLACK, ls="--"); ax.text(32.2, 2e5, "32.767 s", ha="right", fontsize=11)
ax.set_yscale("log"); ax.set_yticks([10, 100, 1000, 10000, 100000, 1000000])
ax.set_yticklabels(["10", "100", "1,000", "10,000", "100,000", "1,000,000"]); ax.yaxis.set_minor_formatter(NullFormatter())
ax.set_xlabel("time since power-on (s)"); ax.set_ylabel("runs of the 100 ms job\nin each 5 s (log scale)")
ax.set_xticks(t); ax.legend(loc="upper left", fontsize=11); ax.grid(axis="y", alpha=0.3)
save(fig, "fig08-timer-bug.png")
print("figures saved in", os.path.abspath(OUT))
