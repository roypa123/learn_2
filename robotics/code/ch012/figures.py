# Figures for Chapter 12 — Running Python: the shell and script files.
# Run:  python figures.py      (saves PNG files in ../../images/ch012/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Polygon

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch012")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"
TERM_BG, TERM_FG, PROMPT, OUTC = "#1E1E1E", "#F0F0F0", "#7EC8E3", "#B5E8B0"
MONO = "DejaVu Sans Mono"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, face, size=11):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size)


def arrow(ax, p, q, colour=GREY, lw=2.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=15, color=colour, lw=lw))


def panel(ax, x, y, w, h, title, lines, bg=TERM_BG, title_bg="#3C3C3C", fg=TERM_FG, size=11):
    ax.add_patch(Rectangle((x, y), w, h, fc=bg, ec=BLACK))
    ax.add_patch(Rectangle((x, y + h - 0.45), w, 0.45, fc=title_bg, ec=BLACK))
    ax.text(x + 0.15, y + h - 0.22, title, va="center", color=fg if bg == TERM_BG else BLACK, fontsize=10.5)
    for i, (t, c) in enumerate(lines):
        ax.text(x + 0.2, y + h - 0.8 - i * 0.42, t, family=MONO, fontsize=size, color=c, va="center")


# ---------- Figure 1: the shell and a script ----------
fig, ax = plt.subplots(figsize=(14, 6.4))
panel(ax, 0.0, 0.6, 6.4, 4.6, "THE SHELL: a conversation", [
    (">>> 0.5 * 0.02", TERM_FG), ("0.01", OUTC), (">>> speed = 0.5", TERM_FG), (">>> speed * 2", TERM_FG),
    ("1.0", OUTC), (">>> round(3.0476, 2)", TERM_FG), ("3.05", OUTC), (">>> |", TERM_FG)])
panel(ax, 7.6, 0.6, 6.4, 4.6, "A SCRIPT FILE: robot_calc.py", [
    ("speed = 0.5", BLACK), ("loop_time = 0.02", BLACK), ('print("blind distance:",', BLACK),
    ("      speed * loop_time, \"m\")", BLACK), ("", BLACK), ("... more lines ...", GREY)],
    bg="white", title_bg=L_BLUE)
ax.text(3.2, 0.2, "type one line -> Python answers at once\nnothing is saved when you close it", ha="center", va="top", fontsize=11.5)
ax.text(10.8, 0.2, "write many lines -> run them all together\nsaved on disk: run again any time", ha="center", va="top", fontsize=11.5)
ax.text(7.0, 5.75, "Two ways to talk to Python", ha="center", fontsize=14, weight="bold")
ax.set_xlim(-0.2, 14.2); ax.set_ylim(-0.9, 6.1); ax.axis("off")
save(fig, "fig01-shell-and-script.png")

# ---------- Figure 2: an annotated shell session ----------
fig, ax = plt.subplots(figsize=(14, 6.6))
lines = [("Python 3.14.7 ... on win32", GREY), ('Type "help", "copyright", "credits" or "license" ...', GREY),
         (">>> 0.8 * 14.4 / 3.78", TERM_FG), ("3.0476190476190483", OUTC), (">>> _ * 60", TERM_FG),
         ("182.8571428571429", OUTC), (">>> battery = 14.4", TERM_FG), (">>> battery", TERM_FG), ("14.4", OUTC),
         (">>> exit()", TERM_FG)]
panel(ax, 0.0, 0.0, 8.6, 5.2, "Terminal: python", lines)
notes = [(0, "<- the version and a welcome", GREY), (2, "<- you type after >>> and press Enter", BLUE),
         (3, "<- Python answers at once (no print needed)", GREEN), (4, "<- _ means 'the last answer'", BLUE),
         (6, "<- storing a value shows nothing...", BLACK), (7, "<- ...asking for it shows it", BLACK),
         (9, "<- leave the shell (or Ctrl+Z then Enter on", RED), (9.5, "    Windows, Ctrl+D on macOS / Linux)", RED)]
for i, t, c in notes:
    ax.text(8.75, 5.2 - 0.8 - i * 0.42, t, fontsize=11, color=c, va="center")
ax.set_xlim(-0.1, 14.3); ax.set_ylim(-0.1, 5.3); ax.axis("off")
save(fig, "fig02-shell-session.png")

# ---------- Figure 3: shell or script? ----------
fig, ax = plt.subplots(figsize=(13, 6.6))


def diamond(ax, cx, cy, w, h, text):
    ax.add_patch(Polygon([(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)], closed=True,
                         fc=L_ORANGE, ec=BLACK, lw=1.3))
    ax.text(cx, cy, text, ha="center", va="center", fontsize=11)


diamond(ax, 2.5, 5.0, 4.2, 1.6, "Will I need it\nagain later?")
diamond(ax, 2.5, 2.2, 4.2, 1.6, "More than 2 or 3\nlines?")
box(ax, 7.2, 4.4, 4.6, 1.2, "SCRIPT FILE\n(save it in my-code/chNNN/)", L_BLUE, 12)
box(ax, 7.2, 1.6, 4.6, 1.2, "SHELL\n(quick try, then forget it)", L_GREEN, 12)
arrow(ax, (4.6, 5.0), (7.2, 5.0), BLACK); ax.text(5.9, 5.2, "yes", fontsize=11.5, weight="bold")
arrow(ax, (2.5, 4.2), (2.5, 3.0), BLACK); ax.text(2.7, 3.55, "no", fontsize=11.5, weight="bold")
arrow(ax, (4.6, 2.2), (7.2, 4.6), BLACK); ax.text(5.6, 3.6, "yes", fontsize=11.5, weight="bold")
arrow(ax, (2.5, 1.4), (2.5, 0.6), BLACK); ax.plot([2.5, 9.5], [0.6, 0.6], color=BLACK, lw=2)
arrow(ax, (9.5, 0.6), (9.5, 1.6), BLACK); ax.text(2.7, 0.85, "no", fontsize=11.5, weight="bold")
ax.text(6.5, 6.4, "Shell or script? Two questions decide", ha="center", fontsize=13.5, weight="bold")
ax.set_xlim(0, 12.2); ax.set_ylim(0.2, 6.8); ax.axis("off")
save(fig, "fig03-shell-or-script.png")

# ---------- Figure 4: python -i ----------
fig, ax = plt.subplots(figsize=(14, 6.0))
panel(ax, 0.0, 0.5, 6.2, 4.4, "1. the script runs, top to bottom", [
    ("distance = 1.0", BLACK), ("speed = 0.25", BLACK), ("step_time = 0.5", BLACK), ("for step in range(4):", BLACK),
    ("    distance = distance - ...", BLACK), ('print("done")', BLACK)], bg="white", title_bg=L_BLUE)
panel(ax, 7.8, 0.5, 6.2, 4.4, "2. then the shell opens, variables kept", [
    ("done", OUTC), (">>> distance", TERM_FG), ("0.5", OUTC), (">>> step", TERM_FG), ("3", OUTC),
    (">>> speed * step_time", TERM_FG), ("0.125", OUTC)])
arrow(ax, (6.3, 2.7), (7.7, 2.7), RED, 3)
ax.text(7.0, 3.0, "python -i", ha="center", fontsize=12, family=MONO, color=RED, weight="bold")
ax.text(7.0, 5.45, "python -i wall_check.py : run the file, then stay to look inside", ha="center", fontsize=13.5, weight="bold")
ax.text(7.0, 0.1, "Like opening the robot after a test drive to read its memory", ha="center", fontsize=11.5, style="italic")
ax.set_xlim(-0.2, 14.2); ax.set_ylim(-0.2, 5.8); ax.axis("off")
save(fig, "fig04-python-i.png")
print("figures saved in", os.path.abspath(OUT))
