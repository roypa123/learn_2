# naive_loop.py - why "do the work, then sleep" drifts behind
import time

PERIOD_S = 0.02                     # we want 50 loops per second
LOOPS = 50

start = time.perf_counter()
for i in range(LOOPS):
    time.sleep(0.005)               # pretend this is 5 ms of real work
    time.sleep(PERIOD_S)            # then wait for "one period"
elapsed = time.perf_counter() - start

print(f"wanted:  {LOOPS * PERIOD_S:.3f} s")
print(f"got:     {elapsed:.3f} s")
print(f"average period: {elapsed / LOOPS * 1000:.1f} ms")
