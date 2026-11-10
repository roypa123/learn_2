# Figures for Chapter 15 — Text: strings.
# Run:  python figures.py      (saves PNG files in ../../images/ch015/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "images", "ch015")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6C9B0"
MONO = "DejaVu Sans Mono"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def arrow(ax, p, q, colour=GREY, lw=2.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=16, color=colour, lw=lw))


def rbox(ax, x, y, w, h, text, face, size=12, family=MONO, weight="normal", edge=BLACK):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=face, ec=edge, lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, family=family, weight=weight)


def cells(ax, text, y=0.0, face=L_BLUE, size=17, highlight=()):
    for i, ch in enumerate(text):
        ax.add_patch(Rectangle((i, y), 1, 1, fc=L_ORANGE if i in highlight else face, ec=BLACK, lw=1.5))
        ax.text(i + 0.5, y + 0.5, ch, ha="center", va="center", fontsize=size, family=MONO, weight="bold")


# ---------- Figure 1: numbers and text ----------
fig, ax = plt.subplots(figsize=(13, 5.2))
rows = [("5 + 1", "6", L_GREEN, "numbers: Python adds them"),
        ('"5" + "1"', "'51'", L_BLUE, "text: Python joins the characters"),
        ('"5" + 1', "TypeError", L_RED, "text + number: Python refuses"),
        ('float("5") + 1', "6.0", L_GREEN, "turn the text into a number first")]
ax.text(2.2, 5.0, "You type", ha="center", fontsize=13.5, weight="bold")
ax.text(6.9, 5.0, "Python gives", ha="center", fontsize=13.5, weight="bold")
ax.text(11.0, 5.0, "Why", ha="center", fontsize=13.5, weight="bold")
for i, (code, res, c, why) in enumerate(rows):
    y = 3.75 - i * 1.2
    rbox(ax, 0.2, y, 4.0, 0.85, code, "white", 15, weight="bold")
    arrow(ax, (4.3, y + 0.42), (5.3, y + 0.42), GREY, 2.5)
    rbox(ax, 5.4, y, 3.0, 0.85, res, c, 15, weight="bold")
    ax.text(8.8, y + 0.42, why, va="center", fontsize=12)
ax.set_xlim(0, 13.2); ax.set_ylim(0.0, 5.4); ax.axis("off")
save(fig, "fig01-numbers-and-text.png")

# ---------- Figure 2: index numbers ----------
fig, ax = plt.subplots(figsize=(13, 4.2))
text = "DIST:0.42"
cells(ax, text)
for i in range(len(text)):
    ax.text(i + 0.5, 1.28, str(i), ha="center", va="center", fontsize=14, color=BLUE, weight="bold", family=MONO)
    ax.text(i + 0.5, -0.32, str(i - len(text)), ha="center", va="center", fontsize=13, color=RED, weight="bold", family=MONO)
ax.text(-0.25, 1.28, "from the start", ha="right", va="center", fontsize=12, color=BLUE)
ax.text(-0.25, -0.32, "from the end", ha="right", va="center", fontsize=12, color=RED)
ax.text(4.5, 2.1, 's = "DIST:0.42"     s[0] is D     s[4] is :     s[-1] is 2', ha="center", fontsize=14, family=MONO)
ax.text(4.5, -1.0, "9 characters: len(s) is 9, so the last index is 8. s[9] is an IndexError.", ha="center", fontsize=12.5,
        style="italic")
ax.set_xlim(-2.6, 9.4); ax.set_ylim(-1.3, 2.5); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig02-index-numbers.png")

# ---------- Figure 3: slices cut between the characters ----------
fig, ax = plt.subplots(figsize=(13, 5.2))
cells(ax, text, y=1.2, highlight=(0, 1, 2, 3))
for i in range(5, 9):
    ax.add_patch(Rectangle((i, 1.2), 1, 1, fc=L_GREEN, ec=BLACK, lw=1.5))
    ax.text(i + 0.5, 1.7, text[i], ha="center", va="center", fontsize=17, family=MONO, weight="bold")
for i in range(len(text) + 1):
    ax.plot([i, i], [0.95, 2.45], color=RED, lw=2.2, ls="--")
    ax.text(i, 2.72, str(i), ha="center", va="center", fontsize=14, color=RED, weight="bold", family=MONO)
ax.text(-0.3, 2.72, "cuts", ha="right", va="center", fontsize=12, color=RED)
ax.plot([0, 0, 4, 4], [0.85, 0.65, 0.65, 0.85], color=ORANGE, lw=2.5)
ax.plot([5, 5, 9, 9], [0.85, 0.65, 0.65, 0.85], color=GREEN, lw=2.5)
ax.text(2, 0.2, "s[0:4] or s[:4]\n'DIST'", ha="center", va="center", fontsize=14, family=MONO, weight="bold")
ax.text(7, 0.2, "s[5:9] or s[5:]\n'0.42'", ha="center", va="center", fontsize=14, family=MONO, weight="bold")
ax.text(4.5, 3.4, "A slice s[a:b] takes what lies between cut a and cut b", ha="center", fontsize=14, weight="bold")
ax.text(4.5, -0.6, "the character after cut b is NOT included; the length of the slice is b - a", ha="center", fontsize=12.5,
        style="italic")
ax.set_xlim(-1.2, 9.4); ax.set_ylim(-0.9, 3.7); ax.set_aspect("equal"); ax.axis("off")
save(fig, "fig03-slices-are-cuts.png")

# ---------- Figure 4: the parsing pipeline ----------
fig, ax = plt.subplots(figsize=(13.5, 7.0))
steps = [("the radio gives", "'  FORWARD 0.25\\n'", L_RED, "extra spaces, capitals, a hidden newline"),
         (".strip()", "'FORWARD 0.25'", L_ORANGE, "the spaces and newline at both ends are gone"),
         (".lower()", "'forward 0.25'", L_ORANGE, "now all small letters"),
         (".split()", "'forward'     '0.25'", L_BLUE, "cut at the space: two strings"),
         ("float(...)", "'forward'      0.25", L_GREEN, "the second one is now a NUMBER (no quotes)")]
for i, (op, val, c, why) in enumerate(steps):
    y = 5.6 - i * 1.4
    ax.text(2.0, y + 0.42, op, ha="right", va="center", fontsize=13, family=MONO, weight="bold", color=RED if i else BLACK)
    rbox(ax, 2.3, y, 5.4, 0.85, val, c, 15, weight="bold")
    ax.text(8.0, y + 0.42, why, va="center", fontsize=12)
    if i < len(steps) - 1:
        arrow(ax, (5.0, y - 0.03), (5.0, y - 0.52), BLACK, 2.2)
ax.set_xlim(0, 13.6); ax.set_ylim(-0.15, 6.7); ax.axis("off")
save(fig, "fig04-parsing-pipeline.png")

# ---------- Figure 5: anatomy of an f-string ----------
fig, ax = plt.subplots(figsize=(13.5, 5.6))
parts = [("f", 0.6, L_RED), ('"', 0.6, "white"), ("speed: ", 2.4, "white"), ("{", 0.6, L_ORANGE), ("speed_ms", 2.9, L_BLUE),
         (":", 0.6, L_ORANGE), ("6", 0.6, L_GREEN), (".2", 1.0, L_GREEN), ("f", 0.6, L_GREEN), ("}", 0.6, L_ORANGE),
         (" m/s", 1.6, "white"), ('"', 0.6, "white")]
x = 0.4
centres = []
for t, w, c in parts:
    ax.add_patch(Rectangle((x, 2.6), w, 1.0, fc=c, ec=BLACK, lw=1.2))
    ax.text(x + w / 2, 3.1, t, ha="center", va="center", fontsize=17, family=MONO, weight="bold")
    centres.append(x + w / 2)
    x += w
notes_up = [(0, "f = this string has\n{ } holes to fill", 0.0), (4, "the value to put in the hole:\na name, or a calculation", 5.1),
            (10, "plain text\nis copied as it is", 10.9)]
for idx, txt, tx in notes_up:
    ax.text(tx, 4.35, txt, ha="left", va="bottom", fontsize=11.5)
    ax.plot([centres[idx], centres[idx]], [3.62, 4.28], color=GREY, lw=1.5)
notes_down = [(6, "width: use at least\n6 characters", 5.5), (7, "2 digits after\nthe point", 8.5), (8, "f = show as a\ndecimal number", 11.0)]
for idx, txt, tx in notes_down:
    ax.text(tx, 1.75, txt, ha="left" if idx == 8 else "center", va="top", fontsize=11.5)
ax.plot([centres[6], 6.0], [2.58, 1.82], color=GREY, lw=1.5)
ax.plot([centres[7], 8.8], [2.58, 1.82], color=GREY, lw=1.5)
ax.plot([centres[8], 11.3], [2.58, 1.82], color=GREY, lw=1.5)
ax.text(0.4, 0.45, "with speed_ms = 0.25 this makes:", fontsize=13)
ax.text(6.6, 0.45, "speed:   0.25 m/s", fontsize=17, family=MONO, weight="bold", color=BLUE)
ax.set_xlim(0, 13.9); ax.set_ylim(0.1, 5.3); ax.axis("off")
save(fig, "fig05-fstring-anatomy.png")

# ---------- Figure 6: a GPS sentence, field by field ----------
fig, ax = plt.subplots(figsize=(14, 6.2))
fields = [("$GPGGA", 1.45, L_GREY, "0", "sentence\nname"), ("123519", 1.45, L_BLUE, "1", "time\n12:35:19"),
          ("4807.038", 1.85, L_GREEN, "2", "latitude\n48 deg\n7.038 min"), ("N", 0.6, L_GREEN, "3", "north"),
          ("01131.000", 2.05, L_ORANGE, "4", "longitude\n011 deg\n31.000 min"), ("E", 0.6, L_ORANGE, "5", "east"),
          ("1", 0.6, L_GREY, "6", "fix"), ("08", 0.7, L_BLUE, "7", "satel-\nlites"), ("0.9", 0.8, L_GREY, "8", ""),
          ("545.4", 1.25, L_RED, "9", "height\n(metres)"), ("...", 0.8, "white", "", "")]
x = 0.2
for i, (t, w, c, idx, note) in enumerate(fields):
    ax.add_patch(Rectangle((x, 3.0), w, 0.95, fc=c, ec=BLACK, lw=1.3))
    ax.text(x + w / 2, 3.47, t, ha="center", va="center", fontsize=13.5, family=MONO, weight="bold")
    ax.text(x + w / 2, 4.2, idx, ha="center", va="center", fontsize=13, color=RED, weight="bold", family=MONO)
    if note:
        ax.text(x + w / 2, 2.8, note, ha="center", va="top", fontsize=10.5)
    x += w
ax.text(6.3, 5.1, 'line.strip().split(",") cuts the sentence at every comma', ha="center", fontsize=14, weight="bold")
ax.text(6.3, 4.65, "the red numbers are the positions: fields[0], fields[1], ...", ha="center", fontsize=12, color=RED)
ax.text(6.3, 1.45, "lat_text[:2] = '48'     lat_text[2:] = '07.038'     48 + 7.038 / 60 = 48.11730 degrees", ha="center",
        fontsize=13, family=MONO)
ax.text(6.3, 0.95, "60 minutes make 1 degree, the same idea as 60 minutes in 1 hour", ha="center", fontsize=12, style="italic")
ax.set_xlim(0, 12.8); ax.set_ylim(0.7, 5.4); ax.axis("off")
save(fig, "fig06-gps-sentence.png")
print("figures saved in", os.path.abspath(OUT))
