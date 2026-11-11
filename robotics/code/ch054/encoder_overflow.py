# encoder_overflow.py - a 16-bit tick counter wraps round; differences still work
TICKS_PER_METRE = 2600


def as_int16(n):
    return (n + 32768) % 65536 - 32768


def tick_change(new, old):
    return as_int16(new - old)


true_ticks = 0
stored = 0
position_naive = 0.0
position_safe = 0.0
last_stored = 0

print("  true ticks   stored (16-bit)   naive metres   safe metres")
for _ in range(10):
    true_ticks += 5200                      # 2 m forward each period
    stored = as_int16(true_ticks)
    position_naive = stored / TICKS_PER_METRE
    position_safe += tick_change(stored, last_stored) / TICKS_PER_METRE
    last_stored = stored
    print(f"{true_ticks:12d} {stored:17d} {position_naive:14.2f} {position_safe:13.2f}")
