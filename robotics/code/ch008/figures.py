# Figures for Chapter 8 — Setting up your computer: Python, a code editor, folders.
# Run:  python figures.py      (saves PNG files in ../../images/ch008/)
import os
import shutil
import subprocess
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch008")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"
TERM_BG, TERM_FG = "#1E1E1E", "#E8E8E8"
MONO = "DejaVu Sans Mono"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, face, size=11):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size)


def arrow(ax, p, q, colour=GREY, lw=2.0, label=None, lpos=None):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=15, color=colour, lw=lw))
    if label:
        x, y = lpos if lpos else ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2 + 0.25)
        ax.text(x, y, label, ha="center", fontsize=11, style="italic")


# ---------- Figure 1: from your fingers to the output ----------
fig, ax = plt.subplots(figsize=(14, 4.6))
box(ax, 0.0, 1.0, 2.0, 1.4, "YOU\ntype the\ninstructions", L_ORANGE)
box(ax, 3.0, 1.0, 2.4, 1.4, "CODE EDITOR\n(VS Code or\nThonny)", L_BLUE)
box(ax, 6.4, 1.0, 2.2, 1.4, "FILE\nhello_robot.py\n(saved on disk)", "white")
box(ax, 9.6, 1.0, 2.2, 1.4, "PYTHON\nreads the file,\nline by line", L_GREEN)
box(ax, 12.8, 1.0, 2.2, 1.4, "OUTPUT\nin the terminal\n(or a plot)", L_GREY)
arrow(ax, (2.0, 1.7), (3.0, 1.7), label="keys")
arrow(ax, (5.4, 1.7), (6.4, 1.7), label="save")
arrow(ax, (8.6, 1.7), (9.6, 1.7), label="run")
arrow(ax, (11.8, 1.7), (12.8, 1.7), label="print")
ax.add_patch(FancyArrowPatch((13.9, 1.0), (1.0, 1.0), arrowstyle="-|>", mutation_scale=15, color=RED, lw=1.8,
                             connectionstyle="arc3,rad=-0.2"))
ax.text(7.5, -0.95, "read the output (or the error message), change the code, run again", ha="center",
        fontsize=11.5, color=RED, style="italic")
ax.set_xlim(-0.2, 15.2); ax.set_ylim(-1.3, 2.8); ax.axis("off")
save(fig, "fig01-from-keys-to-output.png")

# ---------- Figure 2: the folder tree ----------
fig, ax = plt.subplots(figsize=(11, 6.4))
rows = [
    (0, "Documents/", "a place you can find easily", GREY),
    (1, "robotics/", "everything for this course", BLACK),
    (2, "my-code/", "YOUR programs (you type these)", BLUE),
    (3, "ch001/", "", BLACK),
    (3, "...", "", GREY),
    (3, "ch008/", "this chapter's folder", BLACK),
    (4, "hello_robot.py", "a file: name + . + extension", GREEN),
    (4, "check_setup.py", "", GREEN),
    (4, "plot_catch.py", "", GREEN),
    (4, "catch_plot.png", "made by plot_catch.py", ORANGE),
    (3, "ch009/", "", BLACK),
    (2, "notebook-photos/", "optional: photos of your paper notes", BLACK),
]
for i, (lvl, name, note, colour) in enumerate(rows):
    y = len(rows) - i
    x = 0.4 + lvl * 0.9
    if lvl > 0:
        ax.plot([x - 0.6, x - 0.6, x - 0.1], [y + 0.55, y, y], color=GREY, lw=1.2)
    is_folder = name.endswith("/")
    ax.text(x, y, ("[folder] " if is_folder else "") + name, va="center", fontsize=12.5, family=MONO, color=colour,
            weight="bold" if is_folder else "normal")
    if note:
        ax.text(6.3, y, "<- " + note, va="center", fontsize=11, color="#444444")
ax.set_xlim(0, 11); ax.set_ylim(0.3, len(rows) + 0.7); ax.axis("off")
ax.set_title("Folders inside folders: your robotics workspace", fontsize=13)
save(fig, "fig02-folder-tree.png")


# ---------- Figure 3: a terminal session ----------
def terminal(ax, lines, title):
    ax.add_patch(Rectangle((0, 0), 1, 1, transform=ax.transAxes, fc=TERM_BG, ec=BLACK))
    ax.add_patch(Rectangle((0, 0.92), 1, 0.08, transform=ax.transAxes, fc="#3C3C3C", ec=BLACK))
    ax.text(0.02, 0.96, title, transform=ax.transAxes, va="center", color=TERM_FG, fontsize=10.5)
    n = len(lines)
    for i, (txt, colour) in enumerate(lines):
        ax.text(0.02, 0.86 - i * (0.82 / max(n, 1)), txt, transform=ax.transAxes, va="top", family=MONO,
                fontsize=11, color=colour)
    ax.axis("off")


fig, ax = plt.subplots(figsize=(13, 6.2))
P, C, O = "#7EC8E3", "#F5F5F5", "#B5E8B0"     # prompt, command, output colours
terminal(ax, [
    ("PS C:\\Users\\Sam>  cd Documents\\robotics\\my-code", C),
    ("PS C:\\Users\\Sam\\Documents\\robotics\\my-code>  mkdir ch008", C),
    ("PS C:\\Users\\Sam\\Documents\\robotics\\my-code>  cd ch008", C),
    ("PS C:\\...\\my-code\\ch008>  dir", C),
    ("    hello_robot.py", O),
    ("PS C:\\...\\my-code\\ch008>  python hello_robot.py", C),
    ("Hello! I am Rover.", O),
    ("I drive at 0.3 m/s.", O),
    ("In 10 seconds I drive 3.0 m.", O),
    ("PS C:\\...\\my-code\\ch008>  _", C),
], "Terminal (Windows PowerShell). On macOS / Linux: ls instead of dir, python3 instead of python")
ax.text(1.01, 0.86, "<- go into a folder", transform=ax.transAxes, va="top", fontsize=11)
ax.text(1.01, 0.78, "<- make a new folder", transform=ax.transAxes, va="top", fontsize=11)
ax.text(1.01, 0.70, "<- go into it", transform=ax.transAxes, va="top", fontsize=11)
ax.text(1.01, 0.61, "<- list what is inside", transform=ax.transAxes, va="top", fontsize=11)
ax.text(1.01, 0.45, "<- run the program", transform=ax.transAxes, va="top", fontsize=11, color=BLUE, weight="bold")
ax.text(1.01, 0.37, "<- its output", transform=ax.transAxes, va="top", fontsize=11, color=GREEN)
ax.text(1.01, 0.12, "<- waiting for the\n    next command", transform=ax.transAxes, va="top", fontsize=11)
save(fig, "fig03-terminal-session.png")

# ---------- Figure 4: anatomy of an error message ----------
fig, ax = plt.subplots(figsize=(13, 5.6))
terminal(ax, [
    ("Hello! I am Rover.", O),
    ("Traceback (most recent call last):", "#FFB3B3"),
    ('  File "...\\ch008\\hello_error.py", line 4, in <module>', "#FFB3B3"),
    ('    prnt("I drive at", speed, "m/s.")', C),
    ("    ^^^^", "#FFD24D"),
    ("NameError: name 'prnt' is not defined. Did you mean: 'print'?", "#FFB3B3"),
], "Terminal: python hello_error.py")
notes = [(0.86, "1. line 2 worked: its output is here", GREEN),
         (0.72, "2. 'something went wrong, here is where'", BLACK),
         (0.59, "3. WHICH FILE and WHICH LINE (line 4)", BLUE),
         (0.45, "4. the line itself", BLACK),
         (0.32, "5. the ^^^^ points at the problem", ORANGE),
         (0.18, "6. WHAT went wrong: read this first!", RED)]
for y, t, c in notes:
    ax.text(1.01, y, "<- " + t, transform=ax.transAxes, va="top", fontsize=11, color=c, weight="bold")
save(fig, "fig04-error-message.png")

# ---------- Figure 5: the plot made by plot_catch.py (the reader's real output) ----------
env = dict(os.environ, MPLBACKEND="Agg")
subprocess.run([sys.executable, "plot_catch.py"], cwd=HERE, env=env, check=True, capture_output=True)
shutil.move(os.path.join(HERE, "catch_plot.png"), os.path.join(OUT, "fig05-catch-plot.png"))

# ---------- Figure 6: the parts of a code editor window ----------
fig, ax = plt.subplots(figsize=(13, 7.5))
ax.add_patch(Rectangle((0, 0), 13, 8, fc="#F3F3F3", ec=BLACK, lw=1.5))
ax.add_patch(Rectangle((0, 7.5), 13, 0.5, fc="#DDDDDD", ec=BLACK))
ax.text(0.2, 7.75, "File  Edit  View  Run  Terminal  Help", va="center", fontsize=11)
ax.add_patch(Rectangle((12.2, 7.55), 0.6, 0.4, fc=GREEN, ec=BLACK)); ax.text(12.5, 7.75, ">", ha="center", va="center", fontsize=13, color="white", weight="bold")
ax.add_patch(Rectangle((0, 2.6), 3.0, 4.9, fc=L_BLUE, ec=BLACK))
for i, t in enumerate(["my-code", "  ch007", "  ch008", "    hello_robot.py", "    check_setup.py", "    plot_catch.py"]):
    ax.text(0.15, 7.1 - i * 0.45, t, fontsize=10.5, family=MONO)
ax.add_patch(Rectangle((3.0, 2.6), 10.0, 4.9, fc="white", ec=BLACK))
code = ['# hello_robot.py - my first program', 'print("Hello! I am Rover.")', "speed = 0.3",
        'print("I drive at", speed, "m/s.")', 'print("In 10 seconds I drive", speed * 10, "m.")']
for i, t in enumerate(code):
    ax.text(3.2, 7.1 - i * 0.45, f"{i + 1:>2}", fontsize=10.5, family=MONO, color=GREY)
    ax.text(3.7, 7.1 - i * 0.45, t, fontsize=10.5, family=MONO, color=GREEN if t.startswith("#") else BLACK)
ax.add_patch(Rectangle((0, 0), 13, 2.6, fc=TERM_BG, ec=BLACK))
for i, t in enumerate(["> python hello_robot.py", "Hello! I am Rover.", "I drive at 0.3 m/s.", "In 10 seconds I drive 3.0 m."]):
    ax.text(0.2, 2.2 - i * 0.45, t, fontsize=10.5, family=MONO, color=TERM_FG)
labels = [((1.5, 4.0), "A  FILES\n(your folders)"), ((9.5, 4.2), "B  EDITOR\n(you type here)"),
          ((10.0, 1.0), "C  TERMINAL\n(output appears here)"), ((10.6, 6.6), "D  RUN button")]
ax.annotate("", xy=(12.3, 7.55), xytext=(11.4, 6.85), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
for (x, y), t in labels:
    ax.text(x, y, t, ha="center", va="center", fontsize=12, color=RED, weight="bold",
            bbox=dict(fc="white", ec=RED, boxstyle="round,pad=0.3"))
ax.set_xlim(-0.1, 13.1); ax.set_ylim(-0.1, 8.1); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig06-editor-window.png")
print("figures saved in", os.path.abspath(OUT))
