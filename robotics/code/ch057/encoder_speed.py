# encoder_speed.py - measure a wheel's speed from encoder ticks, and see why slow speeds are hard
import math

TICKS_PER_REV = 360
WHEEL_DIAMETER_M = 0.065
M_PER_TICK = math.pi * WHEEL_DIAMETER_M / TICKS_PER_REV
LOOP_DT_S = 0.01                     # the control loop runs 100 times a second


def ticks_seen(true_speed, seconds):
    """Whole ticks counted in each loop when the wheel moves at a steady true speed."""
    counts = []
    last_total = 0
    for k in range(1, round(seconds / LOOP_DT_S) + 1):
        total = math.floor(true_speed * k * LOOP_DT_S / M_PER_TICK)
        counts.append(total - last_total)
        last_total = total
    return counts


for true_speed in [0.50, 0.05]:
    counts = ticks_seen(true_speed, 1.0)
    one_loop = [c * M_PER_TICK / LOOP_DT_S for c in counts]
    window = 10
    ten_loops = [sum(counts[i - window:i]) * M_PER_TICK / (window * LOOP_DT_S) for i in range(window, len(counts) + 1)]
    print(f"true speed {true_speed:.2f} m/s")
    print(f"  ticks in the first 12 loops: {counts[:12]}")
    print(f"  one-loop estimate:  min {min(one_loop):.3f}  max {max(one_loop):.3f} m/s")
    print(f"  ten-loop estimate:  min {min(ten_loops):.3f}  max {max(ten_loops):.3f} m/s")
print(f"one tick is {M_PER_TICK * 1000:.3f} mm, so one tick per loop means {M_PER_TICK / LOOP_DT_S:.4f} m/s")
