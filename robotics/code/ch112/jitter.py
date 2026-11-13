# jitter.py - how steady is a timed loop on a computer with an operating system (Windows, Linux, macOS)?
# usage: python jitter.py [period in ms]      (default 10 ms, like Rover's control loop in Chapter 106)
import statistics
import sys
import time

PERIOD = (float(sys.argv[1]) if len(sys.argv) > 1 else 10.0) / 1000.0   # seconds
N = 500

gaps = []
next_t = time.perf_counter()
last = None
for i in range(N + 1):
    next_t += PERIOD                             # plan each step from the start (Chapter 30), never "sleep a period"
    remaining = next_t - time.perf_counter()
    if remaining > 0:
        time.sleep(remaining)
    now = time.perf_counter()
    if last is not None:
        gaps.append((now - last) * 1e6)          # microseconds
    last = now

with open(f"jitter_gaps_{PERIOD * 1000:g}ms.txt", "w") as f:   # for the chapter's figure
    f.write("\n".join(f"{g:.1f}" for g in gaps))
s = sorted(gaps)
target = PERIOD * 1e6
print(f"target {target:.0f} us, {len(gaps)} gaps measured")
print(f"smallest {s[0]:.0f} us, median {statistics.median(s):.0f} us, largest {s[-1]:.0f} us")
print(f"99 % of the gaps were under {s[int(0.99 * len(s))]:.0f} us")
print(f"gaps more than 10 % late: {sum(g > 1.1 * target for g in gaps)} of {len(gaps)}")
