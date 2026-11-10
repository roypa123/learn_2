# Figures for Chapter 25 — Errors and debugging.
# Run:  python figures.py      (saves PNG files in ../../images/ch025/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Polygon

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch025")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"
TERM_BG, TERM_FG, OUTC = "#1E1E1E", "#F0F0F0", "#FFB3A0"
MONO = "DejaVu Sans Mono"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=2.0, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=15, color=colour, lw=lw, connectionstyle=f"arc3,rad={rad}"))


def rbox(ax, x, y, w, h, text, face, size=12, family=None, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, family=family, weight=weight)


# ---------- Figure 1: reading a traceback ----------
fig, ax = plt.subplots(figsize=(14, 6.6))
ax.add_patch(Rectangle((0, 0.1), 9.0, 6.2, fc=TERM_BG, ec=BLACK))
lines = [("Traceback (most recent call last):", TERM_FG), ('  File "crash_demo.py", line 16, in <module>', "#7EC8E3"), ("    main()", TERM_FG),
         ('  File "crash_demo.py", line 13, in main', "#7EC8E3"), ("    report(900, 0)", TERM_FG), ('  File "crash_demo.py", line 7, in report', "#7EC8E3"),
         ("    seconds = trip_time(route_m, speed_ms)", TERM_FG), ('  File "crash_demo.py", line 3, in trip_time', "#7EC8E3"), ("    return route_m / speed_ms", TERM_FG),
         ("ZeroDivisionError: division by zero", OUTC)]
for i, (t, c) in enumerate(lines):
    ax.text(0.2, 5.9 - i * 0.59, t, family=MONO, fontsize=12, color=c, va="center", weight="bold" if i == 9 else "normal")
ax.annotate("3. first: who called what,\noldest at the top", xy=(9.0, 4.7), xytext=(9.6, 5.3), fontsize=12.5, arrowprops=dict(arrowstyle="-|>", color=GREY))
ax.annotate("2. the exact line\nthat failed", xy=(9.0, 1.2), xytext=(9.6, 2.4), fontsize=12.5, color=BLUE, weight="bold", arrowprops=dict(arrowstyle="-|>", color=BLUE))
ax.annotate("1. START HERE:\nthe kind of error\nand what went wrong", xy=(9.0, 0.6), xytext=(9.6, 0.25), fontsize=12.5, color=RED, weight="bold", arrowprops=dict(arrowstyle="-|>", color=RED))
ax.set_xlim(-0.1, 13.2); ax.set_ylim(0, 6.4); ax.axis("off")
save(fig, "fig01-reading-a-traceback.png")

# ---------- Figure 2: try / except / finally ----------
fig, ax = plt.subplots(figsize=(13.5, 6.6))
rbox(ax, 3.6, 5.6, 5.4, 1.05, "try:  lines that might fail", L_BLUE, 13.5, None, "bold")
arrow(ax, (4.8, 5.58), (2.6, 4.25), GREEN, 3); ax.text(2.8, 5.0, "no error", color=GREEN, fontsize=13, weight="bold", ha="right")
arrow(ax, (7.8, 5.58), (9.9, 4.25), RED, 3); ax.text(9.7, 5.0, "error of this kind", color=RED, fontsize=13, weight="bold", ha="left")
rbox(ax, 0.4, 3.1, 4.3, 1.1, "else:  runs only if\nnothing went wrong", L_GREEN, 12.5)
rbox(ax, 7.7, 3.1, 4.5, 1.1, "except ValueError:\nhandle the problem", L_RED, 12.5)
arrow(ax, (2.6, 3.08), (4.8, 1.75), BLACK, 2.2); arrow(ax, (9.9, 3.08), (7.8, 1.75), BLACK, 2.2)
rbox(ax, 3.6, 0.65, 5.4, 1.05, "finally:  ALWAYS runs\n(the place to stop the motors)", L_ORANGE, 12.5, None, "bold")
ax.annotate("any OTHER kind of error\nstill crashes the program\n(after finally has run)", xy=(9.0, 6.1), xytext=(10.0, 6.2), fontsize=11.5, color=GREY, va="center",
            arrowprops=dict(arrowstyle="-", color=GREY))
ax.set_xlim(0, 13.6); ax.set_ylim(0.4, 6.9); ax.axis("off")
save(fig, "fig02-try-except-finally.png")

# ---------- Figure 3: the debugging loop ----------
fig, ax = plt.subplots(figsize=(10.5, 8.2))
steps = [("1. REPRODUCE\nmake it fail on purpose", L_RED), ("2. READ\nthe last line and the line number", L_ORANGE), ("3. PREDICT\nwhat should each value be?", L_BLUE),
         ("4. LOOK\nprint(f\"{x=}\") or python -i", L_BLUE), ("5. FIX\none change only", L_GREEN), ("6. TEST\ndid it work? did anything break?", L_GREEN)]
R = 3.0
pos = []
for i, (t, c) in enumerate(steps):
    a = math.radians(90 - i * 60)
    x, y = R * math.cos(a) * 1.25, R * math.sin(a)
    pos.append((x, y))
    rbox(ax, x - 1.55, y - 0.55, 3.1, 1.1, t, c, 10.8)
for i in range(len(steps)):
    a1, a2 = math.radians(90 - i * 60), math.radians(90 - (i + 1) * 60)
    p1 = (R * 0.68 * math.cos(a1 - math.radians(22)) * 1.25, R * 0.68 * math.sin(a1 - math.radians(22)))
    p2 = (R * 0.68 * math.cos(a2 + math.radians(22)) * 1.25, R * 0.68 * math.sin(a2 + math.radians(22)))
    if i < 5:
        arrow(ax, p1, p2, BLACK, 2.2, rad=-0.15)
ax.text(0, 0.15, "Never change\nanything at random", ha="center", va="center", fontsize=13.5, weight="bold", color=RED)
ax.text(0, -1.1, "not fixed? go back to 2", ha="center", fontsize=11.5, color=GREY, style="italic")
ax.set_xlim(-5.6, 5.6); ax.set_ylim(-4.0, 4.0); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig03-debugging-loop.png")

# ---------- Figure 4: three kinds of bug ----------
fig, ax = plt.subplots(figsize=(13.5, 4.8))
cols = [("Syntax error", "The program never starts.\nPython shows it at once.", "print('a'", "SyntaxError", L_ORANGE),
        ("Runtime error", "It starts, and crashes\nwhen it reaches the line.", "total / len(value)", "NameError", L_RED),
        ("Logic error", "It runs and ends normally.\nThe answer is WRONG.", "total = v", "average 2.0 (should be 3.0)", L_BLUE)]
for i, (t, d, c, e, col) in enumerate(cols):
    x = 0.2 + i * 4.5
    ax.add_patch(FancyBboxPatch((x, 0.3), 4.1, 3.9, boxstyle="round,pad=0.02,rounding_size=0.12", fc=col, ec=BLACK, lw=1.3))
    ax.text(x + 2.05, 3.7, t, ha="center", fontsize=15, weight="bold")
    ax.text(x + 2.05, 2.8, d, ha="center", va="center", fontsize=12.5)
    ax.text(x + 2.05, 1.65, c, ha="center", fontsize=13, family=MONO, weight="bold")
    ax.text(x + 2.05, 0.8, e, ha="center", fontsize=12.5, family=MONO, color=RED, weight="bold")
ax.text(9.0, -0.15, "easiest to find  <------------------------------------------------>  hardest to find", ha="center", fontsize=12.5, style="italic")
ax.set_xlim(0, 13.7); ax.set_ylim(-0.4, 4.4); ax.axis("off")
save(fig, "fig04-three-kinds-of-bug.png")
print("figures saved in", os.path.abspath(OUT))
