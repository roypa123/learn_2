# bounce.py - a mechanical switch bounces for a few milliseconds; count the false presses, then debounce
import random

random.seed(7)
SAMPLE_US = 100             # read the pin every 100 microseconds (10,000 times a second)


def bouncing_press(press_at_ms, bounce_ms=4.0):
    """A list of (time_ms, state) changes: the contact chatters before settling closed (0 = pressed, pull-up)."""
    changes = [(0.0, 1)]
    t = press_at_ms
    state = 0
    while t < press_at_ms + bounce_ms:
        changes.append((t, state))
        t += random.uniform(0.05, 0.6) * (1 - (t - press_at_ms) / bounce_ms) + 0.02   # gaps grow shorter... then stop
        state = 1 - state
    changes.append((t, 0))
    return changes


def level_at(changes, t_ms):
    s = changes[0][1]
    for when, state in changes:
        if when <= t_ms:
            s = state
    return s


changes = bouncing_press(press_at_ms=2.0)
samples = [level_at(changes, k * SAMPLE_US / 1000) for k in range(int(12 / (SAMPLE_US / 1000)))]

falls = sum(1 for a, b in zip(samples, samples[1:]) if a == 1 and b == 0)
print(f"one press of the button, sampled every {SAMPLE_US} us for 12 ms")
print(f"the pin went from HIGH to LOW {falls} times: a naive counter would see {falls} presses")

# debounce: accept a new state only after it has stayed the same for STABLE_MS
STABLE_MS = 5.0
need = int(STABLE_MS * 1000 / SAMPLE_US)
accepted, run, last, presses = 1, 0, 1, 0
for s in samples:
    run = run + 1 if s == last else 1
    last = s
    if run >= need and s != accepted:
        accepted = s
        if s == 0:
            presses += 1
print(f"after debouncing (state must be steady for {STABLE_MS:.0f} ms): {presses} press")
