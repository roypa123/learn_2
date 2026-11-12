# Figures for Chapter 84 - Capacitors.
# Run:  python figures.py      (saves PNG files in ../../images/ch084/)
import math
import os
import random
import matplotlib
matplotlib.use("Agg")
import matplotlib.ticker
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch084")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


# Figure 1: inside a capacitor, and the symbols
fig, axes = plt.subplots(1, 2, figsize=(11, 4.8), gridspec_kw=dict(width_ratios=[1.3, 1]))
ax = axes[0]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-1, 9); ax.set_ylim(-2.0, 5)
ax.add_patch(plt.Rectangle((2.6, 0), 0.3, 4, color=GREY, ec=BLACK)); ax.add_patch(plt.Rectangle((5.1, 0), 0.3, 4, color=GREY, ec=BLACK))
ax.add_patch(plt.Rectangle((2.9, 0), 2.2, 4, color=L_BLUE, alpha=0.6))
ax.text(4.0, 4.3, "insulator", ha="center", fontsize=10.5)
for y in np.linspace(0.4, 3.6, 6):
    ax.text(2.75, y, "+", ha="center", va="center", fontsize=11, color=RED, fontweight="bold")
    ax.text(5.25, y, "-", ha="center", va="center", fontsize=13, color=BLUE, fontweight="bold")
ax.plot([0.5, 2.6], [2, 2], color=BLACK, lw=2); ax.plot([5.4, 7.5], [2, 2], color=BLACK, lw=2)
ax.text(0.4, 2.3, "to +", fontsize=10.5); ax.text(6.9, 2.3, "to -", fontsize=10.5)
ax.text(4.0, -1.1, "two metal plates; charge piles up on them,\nbut cannot cross the gap", ha="center", fontsize=10.5)
ax.set_title("inside: plates and an insulator", fontsize=11.5)
ax = axes[1]; ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-0.5, 6), ax.set_ylim(-1, 5)
ax.plot([0, 1.3], [3.5, 3.5], color=BLACK, lw=2); ax.plot([1.3, 1.3], [3.0, 4.0], color=BLACK, lw=3); ax.plot([1.6, 1.6], [3.0, 4.0], color=BLACK, lw=3); ax.plot([1.6, 2.9], [3.5, 3.5], color=BLACK, lw=2)
ax.text(3.2, 3.5, "ceramic or film:\neither way round", va="center", fontsize=10.5)
ax.plot([0, 1.3], [1.0, 1.0], color=BLACK, lw=2); ax.plot([1.3, 1.3], [0.5, 1.5], color=BLACK, lw=3)
ax.add_patch(matplotlib.patches.Arc((2.2, 1.0), 1.2, 1.4, theta1=145, theta2=215, color=BLACK, lw=3)); ax.plot([1.65, 2.9], [1.0, 1.0], color=BLACK, lw=2)
ax.text(1.0, 1.6, "+", fontsize=13, fontweight="bold"); ax.text(3.2, 1.0, "electrolytic:\n+ must go to +", va="center", fontsize=10.5)
ax.set_title("symbols", fontsize=11.5)
save(fig, "fig01-capacitor.png")

# Figure 2: charging and discharging curves
fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
t = np.linspace(0, 5, 300)
axes[0].plot(t, 5 * (1 - np.exp(-t)), color=BLUE, lw=2.5); axes[0].axhline(5, color=BLACK, ls="--", lw=1.5)
for n in [1, 2, 3, 5]:
    v = 5 * (1 - math.exp(-n)); axes[0].plot(n, v, "o", color=ORANGE, mec=BLACK, ms=8); axes[0].text(n + 0.08, v - 0.45, f"{v / 5:.0%}", fontsize=10.5)
axes[0].set_xlabel("time (in units of RC)"); axes[0].set_ylabel("capacitor voltage (V)"); axes[0].set_title("charging from 5 V", fontsize=11.5); axes[0].grid(alpha=0.3); axes[0].set_ylim(0, 5.5)
axes[1].plot(t, 5 * np.exp(-t), color=RED, lw=2.5)
for n in [1, 2, 3, 5]:
    v = 5 * math.exp(-n); axes[1].plot(n, v, "o", color=ORANGE, mec=BLACK, ms=8); axes[1].text(n + 0.08, v + 0.2, f"{v / 5:.1%}", fontsize=10.5)
axes[1].set_xlabel("time (in units of RC)"); axes[1].set_ylabel("capacitor voltage (V)"); axes[1].set_title("discharging from 5 V", fontsize=11.5); axes[1].grid(alpha=0.3); axes[1].set_ylim(0, 5.5)
fig.suptitle("after one time constant RC: 63% of the way; after five: practically there", fontsize=12, y=1.02)
save(fig, "fig02-rc-curves.png")

# Figure 3: energy in different capacitors (log bar)
fig, ax = plt.subplots(figsize=(10, 4.6))
names = ["decoupling\n100 nF, 5 V", "Rover bulk\n470 uF, 7.2 V", "drone ESC\n1000 uF, 25 V", "flash\n120 uF, 330 V", "supercap\n10 F, 2.7 V"]
energy = [0.5 * 100e-9 * 25, 0.5 * 470e-6 * 7.2 ** 2, 0.5 * 1e-3 * 25.2 ** 2, 0.5 * 120e-6 * 330 ** 2, 0.5 * 10 * 2.7 ** 2]
ax.bar(range(5), energy, color=[GREY, BLUE, BLUE, RED, GREEN], edgecolor=BLACK); ax.set_yscale("log")
for k, e in enumerate(energy):
    ax.text(k, e * 1.6, f"{e:.3g} J", ha="center", fontsize=10.5)
ax.set_xticks(range(5)); ax.set_xticklabels(names, fontsize=10); ax.set_ylabel("energy stored (J, log scale)")
ax.set_ylim(1e-7, 1e3); ax.grid(alpha=0.3, axis="y", which="both")
ax.set_yticks([1e-6, 1e-4, 1e-2, 1, 100]); ax.set_yticklabels(["0.000001", "0.0001", "0.01", "1", "100"])
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
ax.set_title("energy = 1/2 C V^2: voltage counts twice, so the 330 V flash capacitor is the dangerous one", fontsize=11)
save(fig, "fig03-energy.png")

# Figure 4: brown-out
fig, ax = plt.subplots(figsize=(10, 4.8))
for c_uf, col in [(1000, RED), (2200, ORANGE), (4700, GREEN)]:
    c = c_uf * 1e-6; v, tt = 5.0, 0.0; ts, vs = [], []
    while tt < 0.012:
        load = 0.19 + (1.3 if 0.001 <= tt < 0.007 else 0.0)
        supply = min(1.0, load + (5.0 - v) * 50)
        v = min(max(v + (supply - load) / c * 1e-6, 0.0), 5.0)
        if int(tt * 1e6) % 20 == 0:
            ts.append(tt * 1000); vs.append(v)
        tt += 1e-6
    ax.plot(ts, vs, color=col, lw=2.5, label=f"{c_uf} uF on the 5 V rail")
ax.axhline(4.3, color=BLACK, ls="--", lw=1.5); ax.text(11.8, 4.12, "Arduino may reset below 4.3 V", ha="right", fontsize=10.5)
ax.axvspan(1, 7, color=L_GREY, alpha=0.6); ax.text(4, 1.6, "servo starting:\n1.49 A wanted,\nregulator gives 1.0 A", ha="center", fontsize=10.5)
ax.set_xlabel("time (ms)"); ax.set_ylabel("5 V rail (V)"); ax.set_ylim(1.5, 5.4); ax.grid(alpha=0.3); ax.legend(loc="lower right", fontsize=10.5)
ax.set_title("the capacitor supplies the missing 0.49 A; a bigger one sags less", fontsize=11.5)
save(fig, "fig04-brownout.png")

# Figure 5: RC filter on a noisy sensor signal
random.seed(3)
fig, ax = plt.subplots(figsize=(10, 4.8))
tau, dt = 0.01, 1e-5
vc, tt = 0.0, 0.0; ts, raw, fil, tru = [], [], [], []
while tt < 0.15:
    tr = 1.0 if tt < 0.05 else 2.0
    r = tr + 0.4 * math.sin(2 * math.pi * 2000 * tt) + random.uniform(-0.1, 0.1)
    vc += (r - vc) / tau * dt; tt += dt
    if int(tt / dt) % 5 == 0:
        ts.append(tt * 1000); raw.append(r); fil.append(vc); tru.append(tr)
ax.plot(ts, raw, color=L_GREY, lw=0.8, label="sensor wire with motor noise")
ax.plot(ts, tru, color=BLACK, ls="--", lw=1.5, label="true sensor output")
ax.plot(ts, fil, color=BLUE, lw=2.5, label="after a 10 kohm, 1 uF filter (RC = 10 ms)")
ax.set_xlabel("time (ms)"); ax.set_ylabel("volts"); ax.grid(alpha=0.3); ax.legend(loc="upper left", fontsize=10); ax.set_ylim(0, 3)
ax.set_title("the filter removes the fast noise but follows the real step with a delay", fontsize=11.5)
save(fig, "fig05-rc-filter.png")

# Figure 6: RC debounce with thresholds
random.seed(7)
changes = [(0.0, 1)]; t0 = 2.0; tt = t0; st = 0
while tt < t0 + 4.0:
    changes.append((tt, st)); tt += random.uniform(0.05, 0.6) * (1 - (tt - t0) / 4.0) + 0.02; st = 1 - st
changes.append((tt, 0))
fig, ax = plt.subplots(figsize=(10, 4.6))
ts = np.arange(0, 20, 0.01); raw = []
for x in ts:
    s = 1
    for when, state in changes:
        if when <= x:
            s = state
    raw.append(5.0 * s)
vc = 5.0; out = []
for r in raw:
    rr = 10e3 if r > vc else 1e3        # charges through 10 k (pull-up), discharges through 1 k (button path)
    vc += (r - vc) / (rr * 1e-6) * 1e-5
    out.append(vc)
ax.step(ts, raw, where="post", color=GREY, lw=1.2, label="switch contacts (bouncing)")
ax.plot(ts, out, color=BLUE, lw=2.5, label="capacitor voltage (1 uF)")
ax.axhline(1.5, color=BLACK, ls=":"); ax.axhline(3.0, color=BLACK, ls=":"); ax.text(19.8, 3.1, "reads 1 above", ha="right", fontsize=10); ax.text(19.8, 1.6, "reads 0 below", ha="right", fontsize=10)
ax.set_xlabel("time (ms)"); ax.set_ylabel("volts"); ax.grid(alpha=0.3); ax.legend(loc="upper right", fontsize=10); ax.set_ylim(-0.3, 5.6)
ax.set_title("a capacitor smooths the bounce: the pin crosses each threshold only once", fontsize=11.5)
save(fig, "fig06-rc-debounce.png")
print("saved 6 figures")
