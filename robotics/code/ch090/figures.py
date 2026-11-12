# Figures for Chapter 90 - Voltage regulators and power supplies.
# Run:  python figures.py      (saves PNG files in ../../images/ch090/)
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch090")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def line(ax, xs, ys, color=BLACK, lw=2):
    ax.plot(xs, ys, color=color, lw=lw)


# Figure 1: the linear regulator as a self-adjusting resistor
fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw=dict(width_ratios=[1, 1.2]))
ax = axes[0]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1, 7), ax.set_ylim(-1, 5)
ax.add_patch(plt.Rectangle((2.2, 2.6), 1.6, 1.2, color=L_ORANGE, ec=BLACK, lw=2)); ax.text(3.0, 3.2, "regulator", ha="center", va="center", fontsize=10)
ax.annotate("", xy=(3.4, 3.9), xytext=(2.6, 2.5), arrowprops=dict(arrowstyle="-|>", lw=1.5, color=RED))
line(ax, [0, 2.2], [3.2, 3.2]); line(ax, [3.8, 6], [3.2, 3.2]); ax.text(0, 3.5, "battery\n6-8.4 V", fontsize=10.5); ax.text(4.6, 3.5, "steady 5 V", fontsize=10.5, color=BLUE)
line(ax, [3.0, 3.0], [2.6, 0.8]); ax.text(3.2, 1.6, "ground", fontsize=10)
ax.text(3.0, 0.0, "it adjusts its own resistance so that\nwhatever is extra is dropped across it", ha="center", fontsize=10)
ax.set_title("a linear regulator", fontsize=11.5)
ax = axes[1]
vin = np.linspace(5.3, 12, 100)
ax.plot(vin, (vin - 5) * 0.19 * 1000, color=RED, lw=2.5, label="heat at 190 mA (mW)")
ax2 = ax.twinx(); ax2.plot(vin, 5 / vin * 100, color=BLUE, lw=2.5, ls="--", label="efficiency (%)")
ax.set_xlabel("input voltage (V)"); ax.set_ylabel("heat (mW)", color=RED); ax2.set_ylabel("efficiency (%)", color=BLUE); ax2.set_ylim(0, 100)
ax.grid(alpha=0.3); ax.set_title("the more extra voltage, the more heat", fontsize=11.5)
save(fig, "fig01-linear.png")

# Figure 2: efficiency against input voltage, linear vs buck
fig, ax = plt.subplots(figsize=(10, 4.6))
vin = np.linspace(5.5, 25, 200)
ax.plot(vin, 5 / vin * 100, color=RED, lw=2.5, label="linear regulator: 5 V / input")
ax.plot(vin, 90 - 0.15 * (vin - 5.5), color=GREEN, lw=2.5, label="buck converter: about 85-90%")
for v, lab in [(7.2, "Rover\n7.2 V"), (14.8, "4S drone\n14.8 V"), (22.2, "6S drone\n22.2 V")]:
    ax.axvline(v, color=GREY, ls=":"); ax.text(v + 0.2, 15, lab, fontsize=10)
ax.set_xlabel("input voltage (V)"); ax.set_ylabel("efficiency making 5 V (%)"); ax.set_ylim(0, 100); ax.grid(alpha=0.3); ax.legend(loc="center right", fontsize=10.5)
ax.set_title("from a drone pack, a linear regulator wastes most of the energy as heat", fontsize=11.5)
save(fig, "fig02-efficiency.png")

# Figure 3: buck converter circuit
fig, ax = plt.subplots(figsize=(10, 4.6))
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1, 11), ax.set_ylim(-1.2, 4.2)
line(ax, [0, 2.0], [3, 3]); ax.text(0, 3.3, "8.4 V in", fontsize=10.5, color=RED)
ax.add_patch(plt.Rectangle((2.0, 2.6), 1.4, 0.8, color=L_BLUE, ec=BLACK)); ax.text(2.7, 3.0, "MOSFET\nswitch", ha="center", va="center", fontsize=9)
line(ax, [3.4, 4.2], [3, 3]); ax.plot(4.2, 3, "o", color=BLACK, ms=6)
for k in range(4):
    ax.add_patch(matplotlib.patches.Arc((4.6 + k * 0.4, 3.0), 0.4, 0.5, theta1=0, theta2=180, color=ORANGE, lw=2.5))
line(ax, [6.0, 7.5], [3, 3]); ax.text(5.2, 3.5, "inductor L", ha="center", fontsize=10, color=ORANGE)
line(ax, [4.2, 4.2], [3, 2.0]); ax.add_patch(plt.Polygon([(3.9, 1.3), (4.5, 1.3), (4.2, 1.9)], color=GREEN)); line(ax, [3.9, 4.5], [1.95, 1.95], color=GREEN, lw=3)
line(ax, [4.2, 4.2], [1.3, 0]); ax.text(3.0, 1.5, "diode", fontsize=10, color=GREEN)
line(ax, [7.5, 7.5], [3, 2.0]); line(ax, [7.1, 7.9], [2.0, 2.0], lw=3); line(ax, [7.1, 7.9], [1.75, 1.75], lw=3); line(ax, [7.5, 7.5], [1.75, 0]); ax.text(7.9, 1.6, "C", fontsize=11)
line(ax, [7.5, 9.5], [3, 3]); ax.text(9.6, 3.0, "5 V out", fontsize=10.5, color=BLUE, va="center")
line(ax, [0, 9.5], [0, 0]); ax.text(0, -0.4, "ground", fontsize=10)
ax.text(5.0, -1.0, "switch on: the battery pushes current into L; switch off: L keeps it flowing through the diode", ha="center", fontsize=10.5)
save(fig, "fig03-buck-circuit.png")

# Figure 4: buck simulation waveforms (one steady stretch)
V_IN, L, C, R, F, VD, DT = 8.4, 22e-6, 100e-6, 2.5, 200_000, 0.4, 20e-9
duty = (5 + VD) / (V_IN + VD); period = 1 / F
il, vo, t = 0.0, 0.0, 0.0
ts, ils, vos, sw = [], [], [], []
while t < 0.00802:
    on = (t % period) < duty * period
    vn = V_IN if on else -VD
    if not on and il <= 0:
        vn = vo
    il = max(il + (vn - vo) / L * DT, 0.0); vo += (il - vo / R) / C * DT; t += DT
    if t > 0.008:
        ts.append((t - 0.008) * 1e6); ils.append(il); vos.append(vo); sw.append(1 if on else 0)
fig, axes = plt.subplots(3, 1, figsize=(10, 6.2), sharex=True)
axes[0].step(ts, np.array(sw) * V_IN, where="post", color=GREY, lw=1.5); axes[0].set_ylabel("switch\nnode (V)"); axes[0].set_ylim(-1, 9.5)
axes[0].set_title("a buck converter in steady state: 200 kHz switching, 5 V out at 2 A", fontsize=11.5)
axes[1].plot(ts, ils, color=ORANGE, lw=2); axes[1].set_ylabel("inductor\ncurrent (A)"); axes[1].grid(alpha=0.3)
axes[2].plot(ts, vos, color=BLUE, lw=2); axes[2].set_ylabel("output (V)"); axes[2].grid(alpha=0.3); axes[2].set_xlabel("time (microseconds)")
save(fig, "fig04-buck-waves.png")

# Figure 5: Rover's power tree at stage 7
fig, ax = plt.subplots(figsize=(11, 5))
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.5, 12.5), ax.set_ylim(-0.5, 6)


def box(x, y, w, h, text, col):
    ax.add_patch(plt.Rectangle((x, y), w, h, color=col, ec=BLACK)); ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9.5)


box(0, 2.4, 2.2, 1.2, "battery\n6 x NiMH\n6.0-8.4 V", L_ORANGE)
box(2.8, 2.4, 1.8, 1.2, "fuse 4 A +\nreverse\nprotection", L_GREY)
box(5.4, 4.4, 2.3, 1.1, "LDO 5 V, 1 A\n(linear)", L_BLUE); box(8.6, 4.4, 3.4, 1.1, "Arduino, sensors,\nLEDs, bumpers: 0.19 A", "white")
box(5.4, 2.45, 2.3, 1.1, "buck 5 V, 3 A\n(switching)", L_GREEN); box(8.6, 2.45, 3.4, 1.1, "Raspberry Pi +\ncamera: 0.8-3 A", "white")
box(5.4, 0.5, 2.3, 1.1, "e-stop ->\nmotor driver", L_GREY); box(8.6, 0.5, 3.4, 1.1, "two motors:\nbattery voltage", "white")
for y in [4.95, 3.0, 1.05]:
    line(ax, [4.6, 5.0, 5.0, 5.4], [3.0, 3.0, y, y])
for y in [4.95, 3.0, 1.05]:
    line(ax, [7.7, 8.6], [y, y])
line(ax, [2.2, 2.8], [3.0, 3.0])
ax.text(6.25, 5.75, "one ground for everything (Chapter 78)", ha="center", fontsize=10)
save(fig, "fig05-power-tree.png")

# Figure 6: battery voltage over a run vs regulator needs
fig, ax = plt.subplots(figsize=(10, 4.6))
t = np.linspace(0, 100, 200)
vb = 8.2 - 0.9 * t / 100 - 1.3 * (t / 100) ** 6
ax.plot(t, vb, color=ORANGE, lw=2.5, label="Rover's battery under load")
ax.axhline(7.0, color=RED, ls="--", lw=2, label="7805 needs at least 7.0 V")
ax.axhline(5.3, color=GREEN, ls="--", lw=2, label="LDO needs at least 5.3 V")
cross = t[np.argmax(vb < 7.0)]
ax.axvspan(cross, 100, color="#F5C6B0", alpha=0.6); ax.text((cross + 100) / 2, 7.6, "7805\ndrops out", ha="center", fontsize=10.5)
ax.set_xlabel("time through the run (%)"); ax.set_ylabel("volts"); ax.set_ylim(4.5, 9); ax.grid(alpha=0.3); ax.legend(loc="center left", fontsize=10.5)
ax.set_title("a low-dropout regulator keeps 5 V to the very end of the battery", fontsize=11.5)
save(fig, "fig06-dropout.png")
print("saved 6 figures")
