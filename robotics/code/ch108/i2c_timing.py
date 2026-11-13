# i2c_timing.py - how long do Rover's I2C transactions take at 100 kHz and 400 kHz?
# Each byte on the bus is 9 clock pulses (8 bits + the acknowledge bit); add about 1 for the start
# and 1 for the stop. A register read is a write (address + register number) and then a read.
def bits(nbytes):
    return 1 + 9 * nbytes + 1                     # start + bytes + stop


jobs = [
    ("scanner: is anyone at this address?", bits(1)),
    ("expander: read 8 pins", bits(1 + 1)),
    ("expander: write 8 pins", bits(1 + 1)),
    ("IMU: read 6 acceleration bytes", bits(1 + 1) + bits(1 + 6)),
    ("IMU: read all 14 bytes", bits(1 + 1) + bits(1 + 14)),
]
print(f"{'transaction':<38s} {'bits':>5s} {'100 kHz':>9s} {'400 kHz':>9s}")
for name, n in jobs:
    print(f"{name:<38s} {n:5d} {n / 100:7.2f} ms {n / 400:7.2f} ms")
n14 = jobs[-1][1]
print(f"most complete IMU readings per second: {100_000 // n14} at 100 kHz, {400_000 // n14} at 400 kHz")
