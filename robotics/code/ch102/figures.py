# Figures for Chapter 102 - PWM: "fake" analog output.
# Run:  python figures.py      (saves PNG files in ../../images/ch102/)
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "images", "ch102")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.size": 12, "text.parse_math": False})
BLUE, ORANGE, GREEN, RED, GREY, BLACK = "#0072B2", "#E69F00", "#009E73", "#D55E00", "#999999", "#000000"
L_BLUE, L_ORANGE, L_GREEN, L_GREY, L_RED = "#BFE3F5", "#FBE3B3", "#BDEBDD", "#DDDDDD", "#F6CBB5"


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight")
    plt.close(fig)


def pwm_wave(t, freq, duty):
    return np.where((t * freq) % 1.0 < duty, 5.0, 0.0)


# Figure 1: three duty cycles and their averages
t = np.linspace(0, 3 / 490, 3000)
fig, axes = plt.subplots(3, 1, figsize=(11, 6.6), sharex=True)
for ax, value in zip(axes, [64, 128, 191]):
    duty = value / 255
    ax.plot(t * 1000, pwm_wave(t, 490, duty), color=BLUE, lw=2)
    ax.axhline(5 * duty, color=RED, ls="--", lw=2)
    ax.text(6.2, 5 * duty + 0.45, f"average {5 * duty:.2f} V", va="center", fontsize=11, color=RED)
    ax.set_ylabel("V"); ax.set_ylim(-0.5, 5.8); ax.set_yticks([0, 5])
    ax.set_title(f"analogWrite(pin, {value}): HIGH for {duty * 100:.0f}% of each 2.04 ms period", fontsize=11)
    ax.grid(alpha=0.3)
axes[2].set_xlabel("time (ms)"); axes[2].set_xlim(0, 7.6)
fig.tight_layout()
save(fig, "fig01-duty-cycles.png")

# Figure 2: equal PWM steps do not look like equal brightness steps
levels = np.arange(0, 11)
linear = levels * 255 // 10
corrected = np.floor(255 * (levels / 10) ** 2.2 + 0.5)
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(levels * 10, linear, "o-", color=GREY, lw=2, label="equal PWM steps (looks uneven)")
ax.plot(levels * 10, corrected, "s-", color=BLUE, lw=2.5, label="gamma-corrected (looks even)")
ax.set_xlabel("brightness you want to SEE (%)"); ax.set_ylabel("analogWrite value")
ax.legend(loc="upper left", fontsize=11); ax.grid(alpha=0.3)
for x, y in zip(levels[1:4] * 10, corrected[1:4]):
    ax.annotate(f"{int(y)}", xy=(x, y), xytext=(x + 1, y + 18), fontsize=10, color=BLUE)
save(fig, "fig02-gamma.png")

# Figure 3: motor current under PWM at 490 Hz and at 20 kHz (the model of pwm_motor.py)
R, L, V = 15.0, 0.002, 6.0
fig, axes = plt.subplots(2, 1, figsize=(11, 6), sharex=True)
for ax, freq, col in [(axes[0], 490, RED), (axes[1], 20000, BLUE)]:
    dt = 1e-6
    n = int(0.008 / dt)
    i, ts, cur = 0.0, [], []
    for k in range(n):
        tt = k * dt
        v = V if (tt * freq) % 1.0 < 0.5 else 0.0
        i += (v - R * i) / L * dt
        ts.append(tt * 1000); cur.append(i * 1000)
    ax.plot(ts, cur, color=col, lw=1.6)
    ax.axhline(200, color=BLACK, ls="--", lw=1.2)
    ax.set_ylabel("current (mA)"); ax.set_ylim(-20, 430); ax.grid(alpha=0.3)
    ax.set_title(f"PWM at {freq:,} Hz, 50% duty (dashed: the 200 mA average)", fontsize=11)
axes[1].set_xlabel("time (ms)")

fig.tight_layout()
save(fig, "fig03-motor-ripple.png")

# Figure 4: an RC filter turns PWM into a steady voltage
fig, ax = plt.subplots(figsize=(11, 4.8))
for r, c, col, ls in [(1000, 1e-6, GREY, "-"), (10000, 1e-6, ORANGE, "--"), (10000, 10e-6, BLUE, "-")]:
    tau = r * c
    dt = 1 / 490 / 200
    v, ts, vs = 0.0, [], []
    for k in range(int(0.4 / dt)):
        tt = k * dt
        vin = 5.0 if (tt * 490) % 1.0 < 128 / 255 else 0.0
        v += (vin - v) / tau * dt
        ts.append(tt * 1000); vs.append(v)
    ax.plot(ts, vs, color=col, ls=ls, lw=1.5, label=f"R = {r // 1000} k, C = {c * 1e6:.0f} uF (tau {tau * 1000:.0f} ms)")
ax.axhline(2.51, color=BLACK, ls=":", lw=1.2); ax.text(402, 2.51, "2.51 V", va="center", fontsize=10.5)
ax.set_xlabel("time (ms)"); ax.set_ylabel("filtered voltage (V)"); ax.set_xlim(0, 430); ax.set_ylim(0, 5.2)
ax.legend(loc="upper right", fontsize=10); ax.grid(alpha=0.3)
save(fig, "fig04-rc-filter.png")

# Figure 5: the knob-to-motor mapping with a dead zone (motor_speed.ino)
knob = np.arange(0, 1024)
pwm = knob * 255 // 1023
pwm = np.where(pwm < 50, 0, pwm)
fig, ax = plt.subplots(figsize=(10, 4.8))
ax.plot(knob, pwm, color=BLUE, lw=2.5, label="PWM sent to the motor")
ax.axvspan(0, 200, color=L_GREY); ax.text(100, 150, "dead zone:\nmotor off", ha="center", fontsize=11)
for k, p in [(0, 0), (163, 0), (409, 101), (716, 178), (1023, 255)]:
    ax.plot(k, p, "o", color=RED, ms=8)
ax.plot([], [], "o", color=RED, label="PC test bench readings")
ax.set_xlabel("knob reading (analogRead)"); ax.set_ylabel("analogWrite value"); ax.legend(loc="upper left", fontsize=11)
ax.grid(alpha=0.3)
save(fig, "fig05-knob-to-motor.png")

# Figure 6: PWM as power and PWM as a message
fig, axes = plt.subplots(2, 1, figsize=(11, 5.6), sharex=True)
t = np.linspace(0, 0.06, 6000)
axes[0].plot(t * 1000, pwm_wave(t, 490, 0.6), color=BLUE, lw=1)
axes[0].set_title("PWM as POWER: 490 Hz, the share of ON time sets the motor's average voltage", fontsize=11)
pulse = np.where((t * 50) % 1.0 < 0.0015 * 50, 5.0, 0.0)
axes[1].plot(t * 1000, pulse, color=GREEN, lw=2)
axes[1].set_title("PWM as a MESSAGE: 50 Hz, a 1.0-2.0 ms pulse tells a servo or ESC a position or throttle (1.5 ms here)", fontsize=11)
for ax in axes:
    ax.set_ylim(-0.5, 5.8); ax.set_yticks([0, 5]); ax.set_ylabel("V")
axes[1].set_xlabel("time (ms)")
fig.tight_layout()
save(fig, "fig06-power-or-message.png")
print("figures saved in", os.path.abspath(OUT))
