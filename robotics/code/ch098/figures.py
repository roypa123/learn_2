# Figures for Chapter 98 - Blink: digital output.
# Run:  python figures.py      (saves PNG files in ../../images/ch098/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch, Polygon, Circle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch098")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6CBB5"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, fc, fs=11, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=fc, ec=BLACK, lw=1.5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, weight=weight)


def wire(ax, pts, color=BLACK, lw=2):
    ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, lw=lw, solid_capstyle="round")


def resistor_v(ax, x, y0, y1, label):
    """A zigzag resistor drawn vertically from y0 (top) to y1 (bottom)."""
    n = 6
    ys = np.linspace(y0 - 0.15, y1 + 0.15, 2 * n + 1)
    xs = [x] + [x + (0.15 if k % 2 else -0.15) for k in range(1, 2 * n)] + [x]
    wire(ax, [(x, y0), (x, y0 - 0.15)]); wire(ax, list(zip(xs, ys))); wire(ax, [(x, y1 + 0.15), (x, y1)])
    ax.text(x + 0.3, (y0 + y1) / 2, label, va="center", fontsize=11)


def led_v(ax, x, y_top, y_bot, label, lit=False):
    """An LED pointing down (current flows from top to bottom)."""
    mid = (y_top + y_bot) / 2
    wire(ax, [(x, y_top), (x, mid + 0.2)]); wire(ax, [(x, mid - 0.2), (x, y_bot)])
    ax.add_patch(Polygon([(x - 0.22, mid + 0.2), (x + 0.22, mid + 0.2), (x, mid - 0.2)], fc=RED if lit else "white", ec=BLACK, lw=1.5))
    wire(ax, [(x - 0.22, mid - 0.2), (x + 0.22, mid - 0.2)])
    for dy in (0.05, -0.12):
        ax.add_patch(FancyArrowPatch((x + 0.28, mid + dy), (x + 0.55, mid + dy + 0.18), arrowstyle="-|>", mutation_scale=9, color=ORANGE if lit else GREY))
    ax.text(x - 0.35, mid, label, ha="right", va="center", fontsize=11)


def ground(ax, x, y):
    for k, w in enumerate([0.3, 0.2, 0.1]):
        wire(ax, [(x - w, y - k * 0.1), (x + w, y - k * 0.1)], lw=1.8)


# Figure 1: inside an output pin
fig, axes = plt.subplots(1, 3, figsize=(13, 5.4))
for ax, title, top_on, bot_on in [(axes[0], "OUTPUT, HIGH", True, False), (axes[1], "OUTPUT, LOW", False, True),
                                   (axes[2], "INPUT: both switches open", False, False)]:
    wire(ax, [(1, 4.6), (3, 4.6)]); ax.text(2, 4.8, "5 V", ha="center", fontsize=11)
    wire(ax, [(1, 0.4), (3, 0.4)]); ax.text(2, 0.1, "0 V (GND)", ha="center", fontsize=11)
    for y0, y1, on, name in [(4.6, 3.0, top_on, "upper\ntransistor"), (2.0, 0.4, bot_on, "lower\ntransistor")]:
        wire(ax, [(2, y0), (2, y0 - 0.45)])
        if on:
            wire(ax, [(2, y0 - 0.45), (2, y1 + 0.45)], color=GREEN, lw=4)
        else:
            wire(ax, [(2, y0 - 0.45), (2.45, y1 + 0.6)], color=GREY, lw=3)
        wire(ax, [(2, y1 + 0.45), (2, y1)])
        ax.text(0.3, (y0 + y1) / 2, name + ("\nON" if on else "\noff"), fontsize=10, va="center", color=GREEN if on else GREY)
    wire(ax, [(2, 3.0), (2, 2.0)]); wire(ax, [(2, 2.5), (3.6, 2.5)])
    ax.add_patch(Rectangle((3.6, 2.25), 0.5, 0.5, fc=GREY, ec=BLACK)); ax.text(4.25, 2.5, "pin", va="center", fontsize=11)
    if top_on:
        ax.text(2.2, 3.4, "current flows OUT\n(the pin 'sources')", fontsize=10, color=RED)
    if bot_on:
        ax.text(2.2, 1.4, "current flows IN\n(the pin 'sinks')", fontsize=10, color=RED)
    if not top_on and not bot_on:
        ax.text(2.25, 3.4, "the pin only listens:\nalmost no current", fontsize=10, color=BLUE)
    ax.set_title(title, fontsize=12)
    ax.set_xlim(0, 5.2); ax.set_ylim(-0.1, 5.2); ax.axis("off")
save(fig, "fig01-pin-inside.png")

# Figure 2: an LED driven by sourcing and by sinking
fig, axes = plt.subplots(1, 2, figsize=(11, 5.6))
ax = axes[0]
ax.add_patch(Rectangle((0.4, 4.0), 1.0, 0.6, fc=GREY, ec=BLACK)); ax.text(0.9, 4.3, "pin 8", ha="center", va="center", fontsize=10)
wire(ax, [(1.4, 4.3), (2.5, 4.3), (2.5, 4.0)]); resistor_v(ax, 2.5, 4.0, 2.8, "220 ohm"); led_v(ax, 2.5, 2.8, 1.2, "LED", lit=True)
ground(ax, 2.5, 1.2)
ax.set_title("sourcing: HIGH turns the LED on", fontsize=12); ax.set_xlim(0, 4.5); ax.set_ylim(0.5, 5.2); ax.axis("off")
ax = axes[1]
wire(ax, [(2.5, 4.8), (2.5, 4.0)]); ax.text(2.5, 4.95, "5 V", ha="center", fontsize=11)
resistor_v(ax, 2.5, 4.0, 2.8, "220 ohm"); led_v(ax, 2.5, 2.8, 1.6, "LED", lit=True)
wire(ax, [(2.5, 1.6), (2.5, 1.3), (1.4, 1.3)])
ax.add_patch(Rectangle((0.4, 1.0), 1.0, 0.6, fc=GREY, ec=BLACK)); ax.text(0.9, 1.3, "pin 8", ha="center", va="center", fontsize=10)
ax.set_title("sinking: LOW turns the LED on", fontsize=12); ax.set_xlim(0, 4.5); ax.set_ylim(0.5, 5.2); ax.axis("off")
save(fig, "fig02-source-sink.png")

# Figure 3: LED current against the resistor (the model of led_current.py)
r = np.linspace(0, 1000, 400)
fig, ax = plt.subplots(figsize=(10, 5))
for name, vf, col, ls in [("red LED (2.0 V)", 2.0, RED, "-"), ("blue LED (3.0 V)", 3.0, BLUE, "--")]:
    ax.plot(r, (5 - vf) / (r + 25) * 1000, color=col, ls=ls, lw=2.5, label=name)
ax.axhline(20, color=BLACK, ls="--", lw=1.2); ax.text(700, 21.5, "20 mA: the most a pin should give", fontsize=10.5)
ax.axhline(40, color=RED, ls=":", lw=1.5); ax.text(700, 41.5, "40 mA: damage", fontsize=10.5, color=RED)
for rv in (220, 330):
    ax.axvline(rv, color=GREY, lw=1); ax.text(rv + 8, 75, f"{rv} ohm", fontsize=10, color=GREY)
ax.set_ylim(0, 90); ax.set_xlim(0, 1000)
ax.set_xlabel("series resistor (ohm)"); ax.set_ylabel("LED current (mA)")
ax.legend(loc="upper right", fontsize=11); ax.grid(alpha=0.3)
save(fig, "fig04-led-current.png")

# Figure 4: the pin's voltage sags as it gives more current
i = np.linspace(0, 40, 100)
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.plot(i, 5 - i / 1000 * 25, color=BLUE, lw=2.5, label="HIGH pin: about 5 V - 25 ohm x current")
ax.plot(i, i / 1000 * 22, color=ORANGE, lw=2.5, ls="--", label="LOW pin: about 22 ohm x current")
ax.axvspan(20, 40, color=L_RED); ax.text(30, 2.6, "above 20 mA:\navoid", ha="center", fontsize=11, color=RED)
ax.axhline(4.2, color=GREY, ls=":", lw=1.3); ax.text(1, 3.75, "V_OH promised: at least 4.2 V (Chapter 91)", fontsize=10, color=GREY)
ax.set_xlabel("current through the pin (mA)"); ax.set_ylabel("pin voltage (V)")
ax.set_xlim(0, 40); ax.set_ylim(0, 5.3); ax.legend(loc="center left", fontsize=10.5); ax.grid(alpha=0.3)
save(fig, "fig03-pin-sag.png")

# Figure 5: SOS on pin 8 (times from pc_tests/test_sos.cpp)
edges = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.6, 2.2, 2.4, 3.0, 3.2, 3.8, 4.4, 4.6, 4.8, 5.0, 5.2, 5.4, 6.8]
fig, ax = plt.subplots(figsize=(12, 3.6))
ts, vs, lv = [0.0], [0], 0
for e in edges:
    ts += [e, e]; vs += [lv, 1 - lv]; lv = 1 - lv
ts.append(7.2); vs.append(lv)
ax.plot(ts, vs, color=BLUE, lw=2.5)
for x0, x1, t in [(0, 1.0, "S: dot dot dot"), (1.6, 3.8, "O: dash dash dash"), (4.4, 5.4, "S: dot dot dot")]:
    ax.annotate("", xy=(x0, 1.25), xytext=(x1, 1.25), arrowprops=dict(arrowstyle="<->", color=GREEN))
    ax.text((x0 + x1) / 2, 1.33, t, ha="center", fontsize=11, color=GREEN)
ax.annotate("", xy=(5.4, -0.25), xytext=(6.8, -0.25), arrowprops=dict(arrowstyle="<->", color=RED))
ax.text(6.1, -0.45, "word gap: 7 units", ha="center", fontsize=10.5, color=RED)
ax.annotate("", xy=(1.0, -0.25), xytext=(1.6, -0.25), arrowprops=dict(arrowstyle="<->", color=ORANGE))
ax.text(1.3, -0.45, "letter gap: 3", ha="center", fontsize=10.5, color=ORANGE)
ax.set_yticks([0, 1]); ax.set_yticklabels(["LOW", "HIGH"]); ax.set_ylim(-0.6, 1.5); ax.set_xlim(-0.1, 7.2)
ax.set_xlabel("time (s); 1 unit = 0.2 s"); ax.grid(axis="x", alpha=0.3)
save(fig, "fig06-sos.png")

# Figure 6: switching a 300 mA headlight with a BJT and with a MOSFET
fig, axes = plt.subplots(1, 2, figsize=(12, 6))
for ax, kind in [(axes[0], "BJT"), (axes[1], "MOSFET")]:
    wire(ax, [(3, 5.6), (3, 5.0)]); ax.text(3, 5.75, "5 V", ha="center", fontsize=11)
    box(ax, 2.3, 4.0, 1.4, 1.0, "headlight\n300 mA", L_ORANGE, fs=10)
    wire(ax, [(3, 4.0), (3, 3.3)])
    ax.add_patch(Circle((3, 2.8), 0.5, fc="white", ec=BLACK, lw=1.5))
    ax.text(3, 2.8, "NPN\n2N2222" if kind == "BJT" else "N-MOSFET\nAO3400", ha="center", va="center", fontsize=8.5)
    wire(ax, [(3, 2.3), (3, 1.4)]); ground(ax, 3, 1.4)
    ax.add_patch(Rectangle((0.0, 2.55), 0.8, 0.5, fc=GREY, ec=BLACK)); ax.text(0.4, 2.8, "pin 9", ha="center", va="center", fontsize=10)
    wire(ax, [(0.8, 2.8), (1.0, 2.8)])
    xs = np.linspace(1.0, 2.0, 13)
    wire(ax, list(zip(xs, [2.8 + (0.12 if k % 2 else -0.12) * (0 < k < 12) for k in range(13)])))
    wire(ax, [(2.0, 2.8), (2.5, 2.8)])
    ax.text(1.5, 3.1, "270 ohm" if kind == "BJT" else "220 ohm", ha="center", fontsize=10.5)
    if kind == "MOSFET":
        wire(ax, [(2.2, 2.8), (2.2, 1.6)]); ground(ax, 2.2, 1.6); ax.text(2.05, 2.15, "100 k to GND:\nkeeps it off while\nthe pin floats", ha="right", fontsize=9.5)
        ax.text(0.2, 0.6, "gate: almost no steady current\nheat when on: 3.6 mW", fontsize=10.5, color=GREEN)
    else:
        ax.text(0.2, 0.6, "base: 15.9 mA from the pin\nheat when on: about 90 mW", fontsize=10.5, color=ORANGE)
    ax.set_title(f"{kind} switch", fontsize=12)
    ax.set_xlim(-0.2, 5); ax.set_ylim(0.3, 6.1); ax.axis("off")
save(fig, "fig05-switches.png")

# Figure 7: Rover's battery lights (times from pc_tests/test_status_leds.cpp)
fig, ax = plt.subplots(figsize=(11, 3.8))
segs = {"green (pin 10)": [(0.0001, 2.0003)], "yellow (pin 11)": [(2.0003, 4.0005)],
        "red (pin 12)": [(4.0005 + 0.2 * k, 4.1005 + 0.2 * k) for k in range(5)]}
for row, (name, spans) in enumerate(segs.items()):
    col = [GREEN, ORANGE, RED][row]
    for a, b in spans:
        ax.add_patch(Rectangle((a, 2 - row), b - a, 0.6, fc=col, ec=BLACK))
    ax.text(-0.1, 2 - row + 0.3, name, ha="right", va="center", fontsize=11)
for k, v in enumerate([8.2, 7.5, 7.0, 6.7, 6.3]):
    ax.axvline(k, color=GREY, ls=":", lw=1); ax.text(k + 0.05, 2.75, f"{v} V", fontsize=10.5)
ax.set_xlim(-0.05, 5.2); ax.set_ylim(-0.2, 3.05); ax.set_yticks([]); ax.set_xlabel("time (s)")
save(fig, "fig07-battery-lights.png")

# Figure 8: charlieplexing - 3 pins drive 6 LEDs
fig, ax = plt.subplots(figsize=(12, 5))
pins = {"A": 0.8, "B": 2.6, "C": 4.4}
for name, y in pins.items():
    ax.add_patch(Rectangle((0.0, y - 0.3), 0.9, 0.6, fc=GREY, ec=BLACK)); ax.text(0.45, y, f"pin {name}", ha="center", va="center", fontsize=10)
    wire(ax, [(0.9, y), (9.4, y)], lw=1.5)
pairs = [("A", "B"), ("B", "A"), ("B", "C"), ("C", "B"), ("A", "C"), ("C", "A")]
for k, (hi, lo) in enumerate(pairs):
    x = 1.6 + k * 1.3
    y1, y2 = pins[hi], pins[lo]
    lit = k == 2
    ax.plot([x, x], [y1, y2], color=BLACK, lw=1.2)
    ax.plot([x], [y1], "ko", ms=4); ax.plot([x], [y2], "ko", ms=4)
    mid = (y1 + y2) / 2 if abs(y1 - y2) < 2 else 1.7      # A-C LEDs sit between A and B, crossing B without touching it
    if abs(y1 - y2) > 2:
        ax.add_patch(Rectangle((x - 0.12, pins["B"] - 0.12), 0.24, 0.24, fc="white", ec="white", zorder=2))
        ax.plot([x, x], [pins["B"] - 0.14, pins["B"] + 0.14], color=BLACK, lw=1.2, zorder=2)
    d = -0.22 if y2 < y1 else 0.22
    ax.add_patch(Polygon([(x - 0.2, mid - d), (x + 0.2, mid - d), (x, mid + d)], fc=RED if lit else "white", ec=BLACK, zorder=3))
    ax.text(x, -0.25, f"LED {k + 1}\n{hi} HIGH\n{lo} LOW", ha="center", va="top", fontsize=9.5, color=RED if lit else BLACK)
ax.text(9.6, 2.6, "the third pin is\nset to INPUT:\nit takes no part", va="center", fontsize=11, color=BLUE)
ax.set_xlim(-0.1, 11.5); ax.set_ylim(-1.6, 5.0); ax.axis("off")
save(fig, "fig08-charlieplexing.png")
print("figures saved in", os.path.abspath(OUT))
