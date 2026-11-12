# Figures for Chapter 91 - Digital and analog signals, logic levels.
# Run:  python figures.py      (saves PNG files in ../../images/ch091/)
import math
import os
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch091")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def line(ax, xs, ys, color=BLACK, lw=2):
    ax.plot(xs, ys, color=color, lw=lw)


# Figure 1: analog vs digital
fig, axes = plt.subplots(2, 1, figsize=(10, 5.2), sharex=True)
t = np.linspace(0, 1, 500)
axes[0].plot(t, 2.5 + 1.8 * np.sin(2 * np.pi * 1.5 * t) * np.exp(-0.5 * t), color=BLUE, lw=2.5)
axes[0].set_ylabel("volts"); axes[0].set_ylim(0, 5.2); axes[0].grid(alpha=0.3)
axes[0].set_title("ANALOG: any voltage, and the exact value carries the information (a thermistor, a microphone)", fontsize=11)
bits = [1, 0, 1, 1, 0, 0, 1, 0, 1, 1]
tb = np.repeat(np.arange(len(bits) + 1) / len(bits), 2)[1:-1]
vb = np.repeat(np.array(bits) * 5.0, 2)
axes[1].plot(tb, vb, color=GREEN, lw=2.5)
for k, b in enumerate(bits):
    axes[1].text((k + 0.5) / len(bits), 5.3 if b else 0.35, str(b), ha="center", fontsize=12)
axes[1].set_ylabel("volts"); axes[1].set_ylim(-0.3, 6.0); axes[1].set_xlabel("time (s)"); axes[1].grid(alpha=0.3)
axes[1].set_title("DIGITAL: only HIGH or LOW; the pattern carries the information (a button, a serial message)", fontsize=11)
save(fig, "fig01-analog-digital.png")

# Figure 2: logic levels and noise margins, 5 V and 3.3 V
fig, axes = plt.subplots(1, 2, figsize=(11, 5.4))
for ax, (name, vdd, voh, vol, vih, vil) in zip(axes, [("5 V Arduino Uno", 5.0, 4.2, 0.9, 3.0, 1.5), ("3.3 V ESP32 / Raspberry Pi", 3.3, 2.9, 0.4, 2.5, 0.8)]):
    ax.set_xlim(0, 4); ax.set_ylim(0, 5.4)
    ax.add_patch(plt.Rectangle((0.3, voh), 1.2, vdd - voh, color=L_GREEN, ec=BLACK)); ax.text(0.9, (voh + vdd) / 2, "output\nHIGH", ha="center", va="center", fontsize=10)
    ax.add_patch(plt.Rectangle((0.3, 0), 1.2, vol, color=L_GREEN, ec=BLACK)); ax.text(0.9, vol / 2, "output LOW", ha="center", va="center", fontsize=9)
    ax.add_patch(plt.Rectangle((2.5, vih), 1.2, vdd - vih, color=L_BLUE, ec=BLACK)); ax.text(3.1, (vih + vdd) / 2, "read as\nHIGH", ha="center", va="center", fontsize=10)
    ax.add_patch(plt.Rectangle((2.5, 0), 1.2, vil, color=L_BLUE, ec=BLACK)); ax.text(3.1, vil / 2, "read as\nLOW", ha="center", va="center", fontsize=10)
    ax.add_patch(plt.Rectangle((2.5, vil), 1.2, vih - vil, color="#F5C6B0", ec=BLACK)); ax.text(3.1, (vil + vih) / 2, "undefined", ha="center", va="center", fontsize=10)
    ax.annotate("", xy=(1.75, vih), xytext=(1.75, voh), arrowprops=dict(arrowstyle="<->", color=RED, lw=1.5)); ax.text(1.82, (voh + vih) / 2, f"margin\n{voh - vih:.1f} V", fontsize=9, color=RED, va="center")
    ax.annotate("", xy=(1.75, vil), xytext=(1.75, vol), arrowprops=dict(arrowstyle="<->", color=RED, lw=1.5)); ax.text(1.82, (vol + vil) / 2, f"margin\n{vil - vol:.1f} V", fontsize=9, color=RED, va="center")
    ax.set_xticks([0.9, 3.1]); ax.set_xticklabels(["what an output\npromises", "what an input\nneeds"]); ax.set_ylabel("volts"); ax.set_title(name, fontsize=11.5)
save(fig, "fig02-logic-levels.png")

# Figure 3: noise on an analog and a digital signal
random.seed(5)
fig, axes = plt.subplots(2, 1, figsize=(10, 5.2), sharex=True)
t = np.linspace(0, 1, 400)
noise = np.array([random.gauss(0, 0.4) for _ in t])
axes[0].plot(t, np.full_like(t, 3.1) + noise, color=BLUE, lw=1.2, label="received"); axes[0].axhline(3.1, color=BLACK, ls="--", label="sent: 3.10 V")
axes[0].set_ylabel("volts"); axes[0].legend(loc="upper right", fontsize=10); axes[0].set_ylim(0, 5.5); axes[0].grid(alpha=0.3)
axes[0].set_title("analog with 0.4 V of noise: every reading is a little wrong", fontsize=11)
bits = [1, 0, 0, 1, 1, 1, 1, 0]
tb = (np.arange(400) // 50).astype(int)
sent = np.array([bits[k] * 5.0 for k in tb])
axes[1].plot(t, sent + noise, color=GREEN, lw=1.2, label="received"); axes[1].axhline(2.5, color=RED, ls=":", label="decision: 2.5 V")
axes[1].set_ylabel("volts"); axes[1].legend(loc="upper right", fontsize=10); axes[1].grid(alpha=0.3); axes[1].set_xlabel("time")
axes[1].set_title("digital with the same noise: every bit is still clearly above or below 2.5 V", fontsize=11)
save(fig, "fig03-noise.png")

# Figure 4: Schmitt trigger
random.seed(2)
fig, axes = plt.subplots(2, 1, figsize=(10, 5.6), sharex=True)
t = np.arange(0, 0.02, 1e-5)
v = 5.0 / (1 + np.exp(-(t - 0.01) / 0.0015)) + np.array([random.gauss(0, 0.25) for _ in t])
plain = (v > 2.5).astype(float)
sch, out = 0, []
for x in v:
    if sch == 0 and x > 3.0:
        sch = 1
    elif sch == 1 and x < 2.0:
        sch = 0
    out.append(sch)
axes[0].plot(t * 1000, v, color=GREY, lw=1); axes[0].axhline(2.5, color=RED, ls=":"); axes[0].axhline(3.0, color=GREEN, ls="--"); axes[0].axhline(2.0, color=GREEN, ls="--")
axes[0].text(0.3, 3.15, "Schmitt: up at 3.0 V", color=GREEN, fontsize=10); axes[0].text(0.3, 1.6, "Schmitt: down at 2.0 V", color=GREEN, fontsize=10); axes[0].text(14, 2.6, "plain: 2.5 V", color=RED, fontsize=10)
axes[0].set_ylabel("input (V)"); axes[0].grid(alpha=0.3); axes[0].set_title("a slow, noisy edge (a line sensor crossing a black line)", fontsize=11)
axes[1].step(t * 1000, plain + 1.4, where="post", color=RED, lw=1.5, label="plain input: 29 changes")
axes[1].step(t * 1000, np.array(out), where="post", color=GREEN, lw=2.5, label="Schmitt input: 1 change")
axes[1].set_yticks([]); axes[1].set_xlabel("time (ms)"); axes[1].set_ylim(-0.2, 3.3); axes[1].legend(loc="upper left", fontsize=10)
save(fig, "fig04-schmitt.png")

# Figure 5: level shifters
fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
for ax in axes:
    ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.5, 7); ax.set_ylim(-1, 5)
ax = axes[0]
line(ax, [0, 2.5], [3.5, 3.5]); ax.text(0, 3.8, "5 V output", fontsize=10.5)
ax.add_patch(plt.Rectangle((2.5, 3.3), 1.0, 0.4, fill=False, ec=BLACK, lw=2)); ax.text(3.0, 3.9, "1 k", ha="center", fontsize=10, color=RED)
line(ax, [3.5, 6.5], [3.5, 3.5]); ax.text(5.0, 3.8, "to 3.3 V input: 3.33 V", fontsize=10.5, color=BLUE)
line(ax, [4.5, 4.5], [3.5, 2.8]); ax.add_patch(plt.Rectangle((4.3, 1.4), 0.4, 1.4, fill=False, ec=BLACK, lw=2)); ax.text(4.85, 2.1, "2 k", fontsize=10, color=RED); line(ax, [4.5, 4.5], [1.4, 0.6])
line(ax, [4.2, 4.8], [0.6, 0.6], lw=3); ax.text(3.5, -0.4, "a divider (Chapter 79): one way only, 5 V down to 3.3 V", ha="center", fontsize=10)
ax.set_title("simple: two resistors", fontsize=11)
ax = axes[1]
ax.add_patch(plt.Rectangle((2.6, 2.2), 1.6, 1.2, color=L_BLUE, ec=BLACK)); ax.text(3.4, 2.8, "N-MOSFET\n(BSS138)", ha="center", va="center", fontsize=9.5)
line(ax, [0, 2.6], [2.8, 2.8]); line(ax, [4.2, 6.5], [2.8, 2.8]); ax.text(0, 2.3, "3.3 V side", fontsize=10.5); ax.text(5.0, 2.3, "5 V side", fontsize=10.5)
line(ax, [3.4, 3.4], [3.4, 4.2]); ax.text(3.4, 4.35, "gate to 3.3 V", ha="center", fontsize=10)
for x, lab in [(1.0, "10 k up to 3.3 V"), (5.6, "10 k up to 5 V")]:
    ax.add_patch(plt.Rectangle((x - 0.2, 2.8), 0.4, 1.0, fill=False, ec=BLACK, lw=2)); line(ax, [x, x], [3.8, 4.2]); ax.text(x, 4.35, lab, ha="center", fontsize=9.5)
ax.text(3.4, 1.0, "works both ways: used for I2C buses (Chapter 108)", ha="center", fontsize=10)
ax.set_title("bidirectional: one MOSFET, two pull-ups", fontsize=11)
save(fig, "fig05-level-shifters.png")

# Figure 6: quantization staircase
fig, ax = plt.subplots(figsize=(10, 4.8))
v = np.linspace(0, 5, 1000)
for bits, col, ls in [(3, RED, "-"), (5, ORANGE, "--")]:
    steps = 2 ** bits
    ax.plot(v, np.floor(v / (5 / steps)) * (5 / steps), color=col, lw=2, ls=ls, label=f"{bits}-bit ADC: {steps} steps of {5 / steps * 1000:.0f} mV")
ax.plot(v, v, color=BLACK, ls=":", lw=1.5, label="the true voltage")
ax.set_xlabel("true voltage (V)"); ax.set_ylabel("voltage the number stands for (V)"); ax.grid(alpha=0.3); ax.legend(loc="upper left", fontsize=10.5)
ax.set_title("an ADC turns a smooth voltage into a staircase; more bits, finer steps", fontsize=11.5)
save(fig, "fig06-quantization.png")
print("saved 6 figures")
