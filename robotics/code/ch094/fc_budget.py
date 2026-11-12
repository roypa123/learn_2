# fc_budget.py - can a chip run a drone's 8 kHz stabilising loop? Count the float maths in one loop.
LOOP_HZ = 8000                                  # the gyro is read and the motors updated 8,000 times a second
AXES, MOTORS = 3, 4                             # roll, pitch, yaw; four propellers

mul = AXES * 1 + AXES * 5 + AXES * 3 + MOTORS * AXES   # scale gyro, filter, PID, mix
add = AXES * 4 + AXES * 4 + MOTORS * AXES               # filter, PID, mix
print(f"one loop: {mul} float multiplies and {add} float adds")

CHIPS = {"Uno (AVR, 16 MHz)": (16e6, 150, 100), "STM32F4 (168 MHz)": (168e6, 1, 1)}
for chip, (clock, t_mul, t_add) in CHIPS.items():
    ticks = mul * t_mul + add * t_add
    us = ticks / clock * 1e6                      # microseconds of maths per loop
    max_hz = 0.5 * clock / ticks                  # use at most half the time for this maths
    ok = "yes" if max_hz >= LOOP_HZ else "NO"
    print(f"{chip:18s} {ticks:6,.0f} ticks = {us:6.1f} us per loop (budget {1e6 / LOOP_HZ:.0f} us);"
          f" up to {max_hz:9,.0f} Hz -> {ok}")
