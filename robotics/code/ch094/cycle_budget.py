# cycle_budget.py - how much work fits in one control loop? (rough clock-tick costs of common operations)
CHIPS = {
    # name: (clock in Hz, {operation: rough clock ticks it takes})
    "Uno (AVR, 16 MHz)": (16_000_000, {"int add": 2, "int multiply": 10, "float add": 100,
                                       "float multiply": 150, "float divide": 500, "sin()": 1700}),
    "STM32F4 (168 MHz)": (168_000_000, {"int add": 1, "int multiply": 1, "float add": 1,
                                        "float multiply": 1, "float divide": 14, "sin()": 80}),
}
LOOP_HZ = 1000                       # a control loop that runs 1,000 times per second

print(f"one loop at {LOOP_HZ} Hz lasts {1000 / LOOP_HZ:g} ms")
for chip, (clock, cost) in CHIPS.items():
    ticks = clock // LOOP_HZ                      # clock ticks available in one loop
    print()
    print(f"{chip}: {ticks:,} ticks per loop, one tick = {1e9 / clock:.1f} ns")
    for op, c in cost.items():
        print(f"  {op:15s} {c:5d} ticks  ->  at most {ticks // c:7,} per loop")
