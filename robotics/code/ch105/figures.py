# Figures for Chapter 105 - Interrupts.
# Run:  python figures.py      (saves PNG files in ../../images/ch105/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch105")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6CBB5"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Figure 1: what happens when an interrupt arrives
fig, ax = plt.subplots(figsize=(12, 4.4))
ax.add_patch(Rectangle((0, 2.0), 4.0, 0.8, fc=L_BLUE, ec=BLACK)); ax.text(2.0, 2.4, "loop(): your program", ha="center", va="center")
ax.add_patch(Rectangle((4.0, 2.0), 0.4, 0.8, fc=L_GREY, ec=BLACK))
ax.add_patch(Rectangle((4.4, 0.6), 1.4, 0.8, fc=L_ORANGE, ec=BLACK)); ax.text(5.1, 1.0, "ISR\n(a few us)", ha="center", va="center", fontsize=10)
ax.add_patch(Rectangle((5.8, 2.0), 0.4, 0.8, fc=L_GREY, ec=BLACK))
ax.add_patch(Rectangle((6.2, 2.0), 4.8, 0.8, fc=L_BLUE, ec=BLACK)); ax.text(8.6, 2.4, "loop() carries on exactly where it was", ha="center", va="center")
ax.add_patch(FancyArrowPatch((4.2, 2.0), (4.6, 1.45), arrowstyle="-|>", mutation_scale=14, lw=1.6))
ax.add_patch(FancyArrowPatch((5.6, 1.45), (6.0, 2.0), arrowstyle="-|>", mutation_scale=14, lw=1.6))
ax.plot([0, 4.0, 4.0, 11], [3.6, 3.6, 4.2, 4.2], color=RED, lw=2.5)
ax.text(0.1, 3.85, "pin 2", fontsize=10, color=RED)
ax.annotate("the edge", xy=(4.0, 3.9), xytext=(2.6, 4.6), fontsize=10.5, color=RED, arrowprops=dict(arrowstyle="-|>", color=RED))
ax.text(4.2, 3.1, "save", ha="center", fontsize=9.5); ax.text(6.0, 3.1, "restore", ha="center", fontsize=9.5)
ax.set_xlim(-0.2, 11.2); ax.set_ylim(0.3, 4.9); ax.axis("off")
save(fig, "fig01-interrupt.png")

# Figure 3: polling with a busy loop against an interrupt (encoder at 1,305 Hz)
t = np.linspace(0, 0.01, 20000)
wave = ((1305 * t) % 1.0) >= 0.5
fig, ax = plt.subplots(figsize=(12, 4.2))
ax.plot(t * 1000, wave * 1.0 + 2.2, color=BLUE, lw=1.5, drawstyle="steps-post")
ax.text(-0.2, 2.7, "encoder A", ha="right", fontsize=10.5)
pass_ms = 0.8 + 0.006
k = 0.0
while k < 10:
    ax.plot([k, k], [1.2, 1.9], color=GREY, lw=1.2)
    k += pass_ms
ax.text(-0.2, 1.55, "polling:\nreads", ha="right", fontsize=10.5)
rises = [(n + 0.5) / 1305 * 1000 for n in range(14)]
for r in rises:
    ax.plot([r, r], [0.2, 0.9], color=GREEN, lw=2.5)
ax.text(-0.2, 0.55, "interrupt:\nruns", ha="right", fontsize=10.5)
ax.set_xlim(0, 10); ax.set_ylim(0, 3.6); ax.set_yticks([]); ax.set_xlabel("time (ms)")
ax.set_title("polling reads once per 0.8 ms pass and often misses the short HIGH; the interrupt runs at every rising edge", fontsize=10.5)
save(fig, "fig03-poll-vs-isr.png")

# Figure 5: counts per second (PC test bench)
fig, ax = plt.subplots(figsize=(9, 4.4))
ax.bar(["polling\n(0.8 ms loop)", "interrupt\n(same loop)", "true pulses"], [66, 1306, 1305], color=[RED, GREEN, GREY])
for k, v in enumerate([66, 1306, 1305]):
    ax.text(k, v + 25, str(v), ha="center", fontsize=12)
ax.set_ylabel("pulses counted in the first second"); ax.set_ylim(0, 1500)
save(fig, "fig05-counts.png")

# Figure 4: quadrature: B tells the direction
t = np.linspace(0, 4, 2000)
fig, axes = plt.subplots(1, 2, figsize=(12, 3.8))
for ax, sign, title in [(axes[0], 1, "forwards: at A's rising edge, B is LOW: +1"), (axes[1], -1, "backwards: at A's rising edge, B is HIGH: -1")]:
    ph = sign * t
    a = ((ph % 1.0) >= 0.5) * 1.0
    b = (((ph - 0.25) % 1.0) >= 0.5) * 1.0
    ax.plot(t, a + 1.5, color=BLUE, lw=2, drawstyle="steps-post"); ax.text(-0.1, 2.0, "A", ha="right")
    ax.plot(t, b, color=ORANGE, lw=2, drawstyle="steps-post"); ax.text(-0.1, 0.5, "B", ha="right")
    for k in range(1, len(t)):
        if a[k] > a[k - 1]:
            ax.axvline(t[k], color=GREEN, ls=":", lw=1.5)
    ax.set_title(title, fontsize=10.5); ax.set_yticks([]); ax.set_xticks([]); ax.set_ylim(-0.3, 2.8)
save(fig, "fig04-quadrature.png")

# Figure 2: the torn read
fig, ax = plt.subplots(figsize=(11, 3.6))
for k, (t, txt, col) in enumerate([("1", "read low byte:\n0xFF (255)", L_BLUE), ("2", "ISR: count 255 -> 256\n(0x00FF -> 0x0100)", L_ORANGE),
                                   ("3", "read high byte: 0x01", L_BLUE), ("4", "result: 0x01FF = 511\n(neither 255 nor 256!)", L_RED)]):
    ax.add_patch(FancyBboxPatch((k * 2.8, 0.5), 2.4, 1.3, boxstyle="round,pad=0.02,rounding_size=0.1", fc=col, ec=BLACK))
    ax.text(k * 2.8 + 1.2, 1.15, txt, ha="center", va="center", fontsize=10.5)
    if k:
        ax.add_patch(FancyArrowPatch((k * 2.8 - 0.38, 1.15), (k * 2.8 - 0.02, 1.15), arrowstyle="-|>", mutation_scale=14, lw=1.6))
ax.set_xlim(-0.2, 11.2); ax.set_ylim(0.2, 2.1); ax.axis("off")
save(fig, "fig02-torn-read.png")

# Figure 6: the ultrasonic distance readings over time (PC test bench)
tt = [65, 125, 185, 244, 304, 364, 423, 483, 543, 602, 662]
dd = [94.5, 88.5, 82.4, 76.4, 70.4, 64.3, 58.3, 52.3, 46.3, 40.2, 40.2]
fig, ax = plt.subplots(figsize=(10, 4.4))
x = np.linspace(0, 700, 300)
ax.plot(x, np.where(x < 600, 100 - x / 10, 40), color=GREY, ls="--", lw=2, label="true distance to the wall")
ax.plot(tt, dd, "o", color=BLUE, ms=8, label="measured (interrupt on the echo pin)")
ax.set_xlabel("time (ms)"); ax.set_ylabel("distance (cm)"); ax.legend(fontsize=10.5); ax.grid(alpha=0.3)
save(fig, "fig06-ultrasonic.png")
print("figures saved in", os.path.abspath(OUT))
