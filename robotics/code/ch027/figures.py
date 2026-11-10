# Figures for Chapter 27 — Files: saving and reading data.
# Run:  python figures.py      (saves PNG files in ../../images/ch027/)
import csv
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "..", "images", "ch027")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"
MONO = "DejaVu Sans Mono"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=BLACK, lw=2.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=15, color=colour, lw=lw))


def page(ax, x, y, lines, face, w=2.4, h=1.7, hi=None):
    ax.add_patch(Rectangle((x, y), w, h, fc=face, ec=BLACK, lw=1.4))
    for i, t in enumerate(lines):
        ax.text(x + 0.2, y + h - 0.35 - i * 0.42, t, fontsize=12.5, family=MONO, va="center", weight="bold" if hi == i else "normal",
                color=GREEN if hi == i else BLACK)


# ---------- Figure 1: the three modes ----------
fig, ax = plt.subplots(figsize=(13.5, 6.6))
rows = [('open(p)  or  "r"', "READ: the file must exist; nothing changes", ["first", "second"], ["first", "second"], None),
        ('open(p, "w")', "WRITE: the old contents are ERASED at once", ["first", "second"], ["new"], 0),
        ('open(p, "a")', "APPEND: new text goes at the end", ["first", "second"], ["first", "second", "new"], 2)]
ax.text(5.3, 6.55, "before", ha="center", fontsize=13, weight="bold")
ax.text(9.6, 6.55, "after", ha="center", fontsize=13, weight="bold")
for r, (code, note, a, b, hi) in enumerate(rows):
    y = 4.5 - r * 2.2
    ax.text(0.1, y + 0.85, code, fontsize=13, family=MONO, weight="bold", va="center")
    page(ax, 4.1, y, a, "white")
    arrow(ax, (6.65, y + 0.85), (8.25, y + 0.85), GREY, 2.5)
    page(ax, 8.4, y, b, L_RED if r == 1 else (L_GREEN if r == 2 else "white"), hi=hi)
    ax.text(0.1, y + 0.2, note, fontsize=10.5, va="center", color=RED if r == 1 else BLACK, wrap=True)
ax.set_xlim(0, 11.2); ax.set_ylim(-0.1, 6.9); ax.axis("off")
save(fig, "fig01-file-modes.png")

# ---------- Figure 2: CSV is a table written as text ----------
fig, ax = plt.subplots(figsize=(13.5, 4.8))
text_rows = ["time_s,distance_m,speed_ms", "0.5,0.875,0.25", "1.0,0.75,0.25", "1.5,0.625,0.25"]
ax.add_patch(Rectangle((0.2, 0.8), 5.6, 3.1, fc="#1E1E1E", ec=BLACK))
ax.text(0.45, 3.6, "trip_log.csv: plain text", color="#7EC8E3", fontsize=11.5, va="center")
for i, t in enumerate(text_rows):
    ax.text(0.45, 3.0 - i * 0.55, t, family=MONO, color="#F0F0F0", fontsize=13, va="center")
arrow(ax, (6.0, 2.3), (7.1, 2.3), ORANGE, 3)
cols = [("time_s", 1.6), ("distance_m", 2.0), ("speed_ms", 1.7)]
y0 = 3.3
x = 7.3
for name, w in cols:
    ax.add_patch(Rectangle((x, y0), w, 0.55, fc=L_GREY, ec=BLACK))
    ax.text(x + w / 2, y0 + 0.27, name, ha="center", va="center", family=MONO, fontsize=11.5, weight="bold")
    x += w
for r, row in enumerate(text_rows[1:]):
    x = 7.3
    for (name, w), v in zip(cols, row.split(",")):
        ax.add_patch(Rectangle((x, y0 - 0.55 * (r + 1)), w, 0.55, fc="white", ec=BLACK))
        ax.text(x + w / 2, y0 - 0.55 * (r + 1) + 0.27, v, ha="center", va="center", family=MONO, fontsize=12)
        x += w
ax.text(9.95, 0.9, "the same data in a spreadsheet", ha="center", fontsize=12.5, style="italic")
ax.set_xlim(0, 13.3); ax.set_ylim(0.5, 4.1); ax.axis("off")
save(fig, "fig02-csv-as-a-table.png")

# ---------- Figure 3: the drive log ----------
t, s, v, b = [], [], [], []
with open(os.path.join(HERE, "drive_log.csv"), newline="") as f:
    for r in csv.DictReader(f):
        t.append(float(r["time_s"])); s.append(float(r["speed_ms"])); v.append(float(r["battery_v"])); b.append(int(r["bumper"]))
fig, axes = plt.subplots(2, 1, figsize=(13, 6.6), sharex=True)
ax = axes[0]
ax.plot(t, s, "o-", color=GREEN, lw=2.5, label="speed command")
ax.axvspan(4.5, 6.5, color=L_RED, label="bumper pressed")
ax.set_ylabel("speed (m/s)"); ax.set_ylim(-0.02, 0.36); ax.grid(alpha=0.3); ax.legend(loc="upper right", framealpha=1)
ax = axes[1]
ax.plot(t, v, "o-", color=BLUE, lw=2.5, label="battery voltage")
ax.axvspan(4.5, 6.5, color=L_RED)
ax.annotate("voltage sags under load,\nand recovers when stopped", xy=(6, 7.08), xytext=(7.1, 7.14), fontsize=12, arrowprops=dict(arrowstyle="-|>"))
ax.annotate("lowest: 6.81 V", xy=(10, 6.81), xytext=(7.5, 6.83), fontsize=12, arrowprops=dict(arrowstyle="-|>"))
ax.set_xlabel("time (s)"); ax.set_ylabel("battery (V)"); ax.grid(alpha=0.3); ax.legend(loc="upper center", framealpha=1)
save(fig, "fig03-drive-log.png")


# ---------- Figure 4: a safe save ----------
def rbox(ax, x, y, w, h, text, face, size=12):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=BLACK, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size)


fig, ax = plt.subplots(figsize=(13.5, 5.0))
ax.text(3.0, 4.75, "Simple save", ha="center", fontsize=14, weight="bold", color=RED)
rbox(ax, 0.7, 3.3, 4.6, 0.95, "open(path, \"w\"): the old file is gone", L_RED, 12)
rbox(ax, 0.7, 2.0, 4.6, 0.95, "POWER CUT while writing", L_ORANGE, 12)
rbox(ax, 0.7, 0.7, 4.6, 0.95, "half a file: settings are ruined", L_RED, 12)
arrow(ax, (3.0, 3.28), (3.0, 3.0)); arrow(ax, (3.0, 1.98), (3.0, 1.7))
ax.text(10.0, 4.75, "Safe save", ha="center", fontsize=14, weight="bold", color=GREEN)
rbox(ax, 7.2, 3.3, 5.6, 0.95, "write everything to settings.json.tmp", L_GREEN, 12)
rbox(ax, 7.2, 2.0, 5.6, 0.95, "POWER CUT here? the real file is still intact", L_ORANGE, 12)
rbox(ax, 7.2, 0.7, 5.6, 0.95, "os.replace: the new file takes over in one step", L_GREEN, 12)
arrow(ax, (10.0, 3.28), (10.0, 3.0)); arrow(ax, (10.0, 1.98), (10.0, 1.7))
ax.set_xlim(0.3, 13.2); ax.set_ylim(0.4, 5.1); ax.axis("off")
save(fig, "fig04-safe-save.png")
print("figures saved in", os.path.abspath(OUT))
