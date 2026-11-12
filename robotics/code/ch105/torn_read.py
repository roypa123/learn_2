# torn_read.py - why reading a 2-byte count while an interrupt changes it can give nonsense
# The Uno's CPU works on one byte at a time (Chapter 94), so it reads a 16-bit count in two steps:
# first the low byte, then the high byte. Here an interrupt adds 1 to the count BETWEEN the two steps.
def torn_read(count):
    low = count & 0xFF                 # step 1: read the low byte (the last 8 bits)
    count = count + 1                  # ... the interrupt runs here and adds one pulse ...
    high = count >> 8                  # step 2: read the high byte (the first 8 bits)
    return high * 256 + low, count     # what the main program believes, and the true count now


print(f"{'true before':>11s} {'true after':>10s} {'program reads':>14s}")
for before in [100, 254, 255, 511, 1023, 32767]:
    seen, after = torn_read(before)
    flag = "" if seen in (before, after) else "   <- WRONG"
    print(f"{before:11d} {after:10d} {seen:14d}{flag}")
