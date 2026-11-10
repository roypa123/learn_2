# steady_loop.py - a loop that keeps a steady beat by aiming at fixed moments
import time

PERIOD_S = 0.02                     # 50 loops per second
LOOPS = 50

start = time.perf_counter()
next_time = start + PERIOD_S        # the moment the next loop should begin
periods_ms = []
overruns = 0
previous = start

for i in range(LOOPS):
    time.sleep(0.005)               # pretend this is 5 ms of real work

    remaining = next_time - time.perf_counter()
    if remaining > 0:
        time.sleep(remaining)       # wait only for what is left
    else:
        overruns += 1               # the work took too long: we are late

    now = time.perf_counter()
    periods_ms.append((now - previous) * 1000)
    previous = now
    next_time += PERIOD_S           # add to the schedule, not to the clock

elapsed = time.perf_counter() - start
print(f"wanted:  {LOOPS * PERIOD_S:.3f} s")
print(f"got:     {elapsed:.3f} s")
print(f"period:  min {min(periods_ms):.2f}  max {max(periods_ms):.2f}  average {sum(periods_ms) / LOOPS:.2f} ms")
print(f"overruns: {overruns}")
