# Figures for Chapter 101 - Analog input: the ADC.
# Run:  python figures.py      (saves PNG files in ../../images/ch101/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch101")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6CBB5"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def box(ax, x, y, w, h, text, fc, fs=10.5):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.1", fc=fc, ec=BLACK, lw=1.5))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs)


def arrow(ax, x1, y1, x2, y2, color=BLACK):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=15, color=color, lw=1.8))


# Figure 1: inside the ADC
fig, ax = plt.subplots(figsize=(13, 5))
for k in range(6):
    ax.text(0.3, 4.2 - k * 0.6, f"A{k}", fontsize=11, va="center")
    arrow(ax, 0.7, 4.2 - k * 0.6, 1.6, 4.2 - k * 0.6)
ax.add_patch(Polygon([(1.6, 4.6), (2.6, 3.9), (2.6, 1.6), (1.6, 0.9)], fc=L_GREY, ec=BLACK, lw=1.5))
ax.text(2.1, 2.75, "multi-\nplexer:\nchooses\none pin", ha="center", va="center", fontsize=9.5)
arrow(ax, 2.6, 2.75, 3.3, 2.75)
box(ax, 3.3, 2.15, 2.2, 1.2, "sample and hold:\na 14 pF capacitor\nholds the voltage", L_BLUE)
arrow(ax, 5.5, 2.75, 6.2, 2.75)
box(ax, 6.2, 2.15, 2.4, 1.2, "comparator +\n10 guesses, one\nbit at a time", L_ORANGE)
arrow(ax, 8.6, 2.75, 9.3, 2.75)
box(ax, 9.3, 2.15, 2.4, 1.2, "result: 0 - 1023\n(analogRead\nreturns it)", L_GREEN)
box(ax, 6.2, 0.2, 2.4, 1.1, "reference: 5 V rail,\n1.1 V inside,\nor the AREF pin", L_RED)
arrow(ax, 7.4, 1.3, 7.4, 2.15)
ax.text(7.4, 4.0, "about 104 us for one reading (13 ADC clock ticks at 125 kHz)", ha="center", fontsize=11)
ax.set_xlim(0, 12); ax.set_ylim(0, 4.8); ax.axis("off")
save(fig, "fig01-adc-inside.png")

# Figure 2: successive approximation for 3.10 V (sar.py)
trials = [512, 768, 640, 576, 608, 624, 632, 636, 634, 635]
keeps = [True, False, False, True, True, True, True, False, True, False]
counts = [512, 512, 512, 576, 608, 624, 632, 632, 634, 634]
fig, ax = plt.subplots(figsize=(11, 4.8))
x = np.arange(10)
ax.plot(x, [t * 5 / 1024 for t in trials], "o", color=GREY, ms=9, label="the guess tried")
for k in range(10):
    ax.plot(k, trials[k] * 5 / 1024, "o", color=GREEN if keeps[k] else RED, ms=9)
ax.step(x, [c * 5 / 1024 for c in counts], where="post", color=BLUE, lw=2.5, label="the count so far")
ax.axhline(3.10, color=BLACK, ls="--", lw=1.5); ax.text(9.3, 3.14, "3.10 V", fontsize=11)
ax.set_xticks(x); ax.set_xticklabels([f"bit {9 - k}" for k in range(10)], fontsize=10)
ax.set_ylabel("volts"); ax.set_ylim(2.3, 3.9); ax.grid(alpha=0.3)
ax.legend(loc="upper right", fontsize=10.5)
ax.set_title("green = 'keep this bit' (the input is at least that big), red = 'too big'", fontsize=11)
save(fig, "fig02-sar.png")

# Figure 3: the ADC's staircase near zero
v = np.linspace(0, 0.03, 600)
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.plot(v * 1000, np.floor(v / 5 * 1024), color=BLUE, lw=2.5, drawstyle="steps-post", label="analogRead count")
ax.plot(v * 1000, v / 5 * 1024, color=GREY, ls="--", lw=1.5, label="the true voltage, in steps")
for k in range(1, 7):
    ax.axvline(k * 4.8828, color=L_GREY, lw=1)
ax.annotate("", xy=(4.88, 0.5), xytext=(9.77, 0.5), arrowprops=dict(arrowstyle="<->", color=RED))
ax.text(7.3, 0.6, "one step:\n4.88 mV", ha="center", fontsize=10.5, color=RED)
ax.set_xlabel("voltage on the pin (mV)"); ax.set_ylabel("count"); ax.set_xlim(0, 30); ax.set_ylim(0, 6.5)
ax.legend(loc="upper left", fontsize=10.5); ax.grid(alpha=0.3)
save(fig, "fig03-staircase.png")

# Figure 4: aliasing - a 50 Hz hum sampled 45 times a second
t = np.linspace(0, 0.4, 4000)
fig, ax = plt.subplots(figsize=(11, 4.4))
ax.plot(t, np.sin(2 * np.pi * 50 * t), color=GREY, lw=1, label="the real 50 Hz hum")
ts = np.arange(0, 0.4, 1 / 45)
ax.plot(ts, np.sin(2 * np.pi * 50 * ts), "o", color=RED, ms=7, label="samples taken 45 times a second")
ax.plot(t, np.sin(2 * np.pi * 5 * t), color=RED, ls="--", lw=2, label="what the samples seem to show: 5 Hz")
ax.set_xlabel("time (s)"); ax.set_ylabel("value"); ax.set_ylim(-1.5, 1.9)
ax.legend(loc="upper right", fontsize=10, ncol=3); ax.grid(alpha=0.3)
save(fig, "fig04-aliasing.png")

# Figure 5: Rover's battery reading with the 5 V reference and with the 1.1 V reference
vb = np.linspace(8.4, 6.0, 200)
rail = np.minimum(5.0, vb - 1.9)
default_read = np.floor(vb * 0.5 / rail * 1024) * 5.0 / 1024 / 0.5           # Chapter 95: 10 k / 10 k, 5 V reference
internal_read = np.floor(vb * 10 / 78 / 1.1 * 1024) * 1.1 / 1024 / (10 / 78)  # this chapter: 68 k / 10 k, 1.1 V
uncal = np.floor(vb * 10 / 78 / 1.083 * 1024) * 1.1 / 1024 / (10 / 78)        # a chip whose reference is really 1.083 V
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(vb, vb, color=BLACK, ls="--", lw=1.5, label="the truth")
ax.plot(vb, default_read, color=RED, lw=2.5, label="5 V reference, Uno through VIN (Chapter 95)")
ax.plot(vb, internal_read, color=GREEN, lw=2.5, label="1.1 V internal reference")
ax.plot(vb, uncal, color=ORANGE, lw=2, ls=":", label="1.1 V reference, chip not calibrated (really 1.083 V)")
ax.invert_xaxis(); ax.set_xlabel("true battery voltage (V)  - the battery runs down to the right")
ax.set_ylabel("what the sketch reads (V)"); ax.legend(loc="upper right", fontsize=9.5); ax.grid(alpha=0.3)
save(fig, "fig05-battery-reference.png")

# Figure 6: thermistor counts against temperature for two fixed resistors
T = np.linspace(20, 100, 300)
R = 10000 * np.exp(3950 * (1 / (T + 273.15) - 1 / 298.15))
fig, ax = plt.subplots(figsize=(10, 5))
for rf, col, ls in [(10000, GREY, "--"), (1500, BLUE, "-")]:
    ax.plot(T, R / (rf + R) * 1024, color=col, ls=ls, lw=2.5, label=f"fixed resistor {rf:,} ohm")
ax.axvspan(70, 85, color=L_ORANGE); ax.text(77.5, 950, "70-85 C:\nwhere it\nmatters", ha="center", fontsize=10.5)
bench_t = [25.1, 33.1, 41.1, 49.0, 57.0, 65.1, 73.0, 81.1, 89.0, 97.1]
true_t = [25 + 8 * k for k in range(10)]
Rb = 10000 * np.exp(3950 * (1 / (np.array(true_t) + 273.15) - 1 / 298.15))
ax.plot(true_t, Rb / (1500 + Rb) * 1024, "o", color=RED, ms=7, label="PC test bench readings (1.5 k)")
ax.set_xlabel("temperature (C)"); ax.set_ylabel("analogRead count"); ax.set_ylim(0, 1050)
ax.legend(loc="lower left", fontsize=10.5); ax.grid(alpha=0.3)
save(fig, "fig06-thermistor.png")
print("figures saved in", os.path.abspath(OUT))
