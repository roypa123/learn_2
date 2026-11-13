# timer_calc.py - choose a prescaler and TOP for a timer interrupt frequency (CTC mode)
# frequency = 16,000,000 / (prescaler x (TOP + 1)); TOP must fit in the timer: 65,535 (Timer1) or 255 (Timer2)
CLOCK = 16_000_000
TIMER1 = (16, [1, 8, 64, 256, 1024])
TIMER2 = (8, [1, 8, 32, 64, 128, 256, 1024])


def choose(freq, timer):
    bits, prescalers = timer
    limit = 2 ** bits - 1
    for n in prescalers:                  # the smallest prescaler that fits gives the finest steps
        top = round(CLOCK / (n * freq)) - 1
        if 0 <= top <= limit:
            actual = CLOCK / (n * (top + 1))
            return n, top, actual
    return None                           # too slow even with the biggest prescaler


print(f"{'wanted':>11s} | {'Timer1: prescaler, TOP, actual':>32s} | {'Timer2: prescaler, TOP, actual':>32s}")
for f in [0.2, 1, 2, 100, 250, 1000, 20000, 38000]:
    cells = []
    for timer in (TIMER1, TIMER2):
        c = choose(f, timer)
        cells.append("does not fit" if c is None else f"{c[0]:5d}, {c[1]:5d}, {c[2]:10.3f} Hz")
    print(f"{f:8g} Hz | {cells[0]:>32s} | {cells[1]:>32s}")
