# Figures for Chapter 88 - MOSFETs.
# Run:  python figures.py      (saves PNG files in ../../images/ch088/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch088")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def line(ax, xs, ys, color=BLACK, lw=2):
    ax.plot(xs, ys, color=color, lw=lw)


def nmos(ax, x, y, labels=True):
    line(ax, [x - 1.0, x - 0.35], [y, y]); line(ax, [x - 0.35, x - 0.35], [y - 0.5, y + 0.5], lw=3)
    for yy in [y + 0.35, y, y - 0.35]:
        line(ax, [x - 0.2, x - 0.2], [yy - 0.12, yy + 0.12], lw=3)
    line(ax, [x - 0.2, x + 0.3], [y + 0.35, y + 0.35]); line(ax, [x + 0.3, x + 0.3], [y + 0.35, y + 1.0])
    line(ax, [x - 0.2, x + 0.3], [y - 0.35, y - 0.35]); line(ax, [x + 0.3, x + 0.3], [y - 0.35, y - 1.0])
    line(ax, [x - 0.2, x + 0.3], [y, y]); line(ax, [x + 0.3, x + 0.3], [y, y - 0.35])
    ax.annotate("", xy=(x - 0.18, y), xytext=(x + 0.15, y), arrowprops=dict(arrowstyle="-|>", lw=1.5, color=BLACK))
    if labels:
        ax.text(x - 1.05, y + 0.12, "G", fontsize=11); ax.text(x + 0.4, y + 0.75, "D", fontsize=11); ax.text(x + 0.4, y - 0.85, "S", fontsize=11)


# Figure 1: MOSFET symbol and the gate as a capacitor
fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
ax = axes[0]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-3, 3.5); ax.set_ylim(-2, 2)
nmos(ax, 0.5, 0)
ax.text(-2.9, 1.2, "gate (G): insulated;\na VOLTAGE controls it", fontsize=10.5)
ax.text(1.2, 1.2, "drain (D):\nthe big current in", fontsize=10.5); ax.text(1.2, -1.6, "source (S):\nit leaves here", fontsize=10.5)
ax.set_title("an N-channel MOSFET", fontsize=11.5)
ax = axes[1]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.5, 8); ax.set_ylim(-1, 4.5)
ax.add_patch(plt.Rectangle((1.0, 0), 6.0, 1.2, color=L_GREY, ec=BLACK)); ax.text(4.0, 0.3, "silicon", ha="center", fontsize=10.5)
ax.add_patch(plt.Rectangle((2.5, 1.2), 3.0, 0.25, color=L_BLUE, ec=BLACK)); ax.text(5.7, 1.32, "thin glass (oxide)", fontsize=9.5, va="center")
ax.add_patch(plt.Rectangle((2.5, 1.45), 3.0, 0.5, color=GREY, ec=BLACK)); ax.text(4.0, 1.7, "gate metal", ha="center", fontsize=10, va="center")
ax.add_patch(plt.Rectangle((2.5, 0.85), 3.0, 0.35, color=L_ORANGE, alpha=0.9)); ax.text(4.0, 1.02, "channel", ha="center", fontsize=9.5, va="center")
ax.text(1.4, 0.6, "S", fontsize=12, fontweight="bold"); ax.text(6.4, 0.6, "D", fontsize=12, fontweight="bold")
ax.text(4.0, 3.0, "the gate is a tiny capacitor: charge it to a few volts and a\nconducting channel appears under the glass; no steady\ncurrent flows into the gate", ha="center", fontsize=10.5)
ax.set_title("inside: the gate never touches the silicon", fontsize=11.5)
save(fig, "fig01-mosfet.png")

# Figure 2: resistance against gate voltage
fig, ax = plt.subplots(figsize=(10, 4.8))
vg = np.linspace(0, 12, 400)


def r_on(v, v_th, r_min, v_full):
    out = np.full_like(v, np.nan)
    on = v > v_th
    out[on] = np.where(v[on] >= v_full, r_min, r_min * (v_full - v_th) / (v[on] - v_th))
    return out


ax.semilogy(vg, r_on(vg, 1.5, 0.025, 4.0), color=GREEN, lw=2.5, label="logic-level MOSFET (fully on at about 4 V)")
ax.semilogy(vg, r_on(vg, 3.0, 0.044, 10.0), color=RED, lw=2.5, ls="--", label="standard MOSFET (needs about 10 V)")
ax.axvline(5.0, color=GREY, ls=":"); ax.text(5.1, 3.0, "5 V Arduino pin", fontsize=10.5)
ax.axvline(3.3, color=GREY, ls=":"); ax.text(3.35, 0.012, "3.3 V", fontsize=10.5)
ax.set_xlabel("gate voltage (V)"); ax.set_ylabel("resistance drain to source (ohm, log)"); ax.grid(alpha=0.3, which="both"); ax.legend(fontsize=10.5)
ax.set_ylim(0.01, 10); ax.set_yticks([0.01, 0.1, 1, 10]); ax.set_yticklabels(["0.01", "0.1", "1", "10"])
import matplotlib.ticker
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_title("below the threshold it is off; above it the resistance falls to its datasheet value", fontsize=11.5)
save(fig, "fig02-ron-vs-vgs.png")

# Figure 3: low-side MOSFET switch
fig, ax = plt.subplots(figsize=(10, 5.4))
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-4, 7); ax.set_ylim(-1.6, 6.3)
nmos(ax, 2.0, 1.2, labels=False)
line(ax, [2.3, 2.3], [2.2, 3.0]); ax.add_patch(plt.Rectangle((1.9, 3.0), 0.8, 1.6, color=L_ORANGE, ec=BLACK)); ax.text(2.3, 3.8, "LED\nstrip", ha="center", va="center", fontsize=9.5)
line(ax, [2.3, 2.3], [4.6, 5.6]); ax.text(2.3, 5.8, "+12 V", ha="center", color=RED, fontsize=11)
line(ax, [2.3, 2.3], [0.2, -0.6]); line(ax, [1.9, 2.7], [-0.6, -0.6], lw=3); ax.text(2.3, -1.0, "ground", ha="center", fontsize=10)
line(ax, [-3.2, -2.4], [1.2, 1.2]); ax.add_patch(plt.Rectangle((-2.4, 1.0), 1.0, 0.4, fill=False, ec=BLACK, lw=2)); line(ax, [-1.4, 1.0], [1.2, 1.2])
ax.text(-3.3, 1.2, "Arduino\npin", ha="right", va="center", fontsize=10.5); ax.text(-1.9, 1.6, "100 ohm", ha="center", fontsize=10.5, color=RED)
line(ax, [-0.5, -0.5], [1.2, 0.6]); ax.add_patch(plt.Rectangle((-0.7, -0.4), 0.4, 1.0, fill=False, ec=BLACK, lw=2)); line(ax, [-0.5, -0.5], [-0.4, -0.6]); line(ax, [-0.5, 2.3], [-0.6, -0.6])
ax.text(-0.1, 0.0, "10 k pull-down", fontsize=9.5)
ax.text(3.5, 1.6, "logic-level N-MOSFET", fontsize=10.5)
ax.text(3.5, 0.6, "(add a flyback diode across the\nload if it is a motor or a coil)", fontsize=9.5)
save(fig, "fig03-low-side-mosfet.png")

# Figure 4: heat in a BJT vs a MOSFET switch, against load current
fig, ax = plt.subplots(figsize=(10, 4.8))
I = np.linspace(0, 10, 200)
ax.plot(I, 0.2 * I, color=BLUE, lw=2.5, label="BJT, saturated (0.2 V x I)")
ax.plot(I, 0.9 * I, color=ORANGE, lw=2.5, ls="--", label="Darlington (0.9 V x I)")
ax.plot(I, I ** 2 * 0.025, color=GREEN, lw=2.5, label="logic-level MOSFET, 25 milliohm (I^2 R)")
ax.plot(I, I ** 2 * 0.003, color=BLACK, lw=2.5, ls=":", label="modern MOSFET, 3 milliohm")
ax.set_xlabel("load current (A)"); ax.set_ylabel("heat in the switch (W)"); ax.grid(alpha=0.3); ax.legend(fontsize=10); ax.set_ylim(0, 5)
ax.set_title("a MOSFET acts like a small resistor: a good one runs coolest, and needs no base current", fontsize=11)
save(fig, "fig04-heat-compare.png")

# Figure 5: a switching transition - voltage and current overlap
fig, ax = plt.subplots(figsize=(10, 4.6))
t = np.linspace(0, 400, 800)
v = np.where(t < 100, 22.2, np.where(t < 150, 22.2 * (1 - (t - 100) / 50), np.where(t < 250, 0, np.where(t < 300, 22.2 * (t - 250) / 50, 22.2))))
i = np.where(t < 100, 0, np.where(t < 150, 30 * (t - 100) / 50, np.where(t < 250, 30, np.where(t < 300, 30 * (1 - (t - 250) / 50), 0))))
ax.plot(t, v, color=BLUE, lw=2.5, label="voltage across the MOSFET (V)")
ax.plot(t, i, color=RED, lw=2.5, label="current through it (A)")
ax.fill_between(t, 0, np.minimum(v, i) * 0 + (v * i / 30), where=(v * i > 1), color=L_ORANGE, alpha=0.8, label="V x I during the change (drawn 1/30 size): heat")
ax.set_xlabel("time (ns)"); ax.grid(alpha=0.3); ax.legend(loc="center right", fontsize=10)
ax.set_title("every switch-on and switch-off passes through 'half on' for about 50 ns", fontsize=11.5)
save(fig, "fig05-transition.png")

# Figure 6: ESC MOSFET losses against PWM frequency
fig, ax = plt.subplots(figsize=(10, 4.6))
f = np.linspace(2000, 100000, 200)
cond = np.full_like(f, 30 ** 2 * 0.002 * 0.5)
sw = 0.5 * 22.2 * 30 * 100e-9 * f
ax.stackplot(f / 1000, cond, sw, colors=[L_BLUE, L_ORANGE], labels=["conduction (I^2 R, fixed)", "switching (grows with frequency)"])
ax.axvline(24, color=BLACK, ls="--"); ax.text(25, 2.2, "24 kHz: 1.7 W", fontsize=10.5)
ax.set_xlabel("PWM frequency (kHz)"); ax.set_ylabel("heat in one MOSFET (W)"); ax.grid(alpha=0.3); ax.legend(loc="upper left", fontsize=10.5)
ax.set_title("a drone ESC MOSFET at 30 A: faster switching means more heat", fontsize=11.5)
save(fig, "fig06-esc-losses.png")
print("saved 6 figures")
