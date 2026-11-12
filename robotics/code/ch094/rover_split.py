# rover_split.py - which of Rover's jobs fit on the Arduino Uno, and which need the Raspberry Pi?
import math

CLOCK = 16_000_000                         # Uno clock ticks per second
SRAM = 2048                                # Uno working memory, bytes
WHEEL = math.pi * 0.06589                  # Rover's wheel goes 0.207 m per turn (Chapter 16)
ENCODER = 540                              # encoder ticks per wheel turn (Chapter 47)
SPEED = 0.5                                # m/s

pulses = 2 * SPEED / WHEEL * ENCODER       # both wheels' encoder pulses per second

jobs = [
    # (job, times per second, clock ticks each time - rough estimates)
    ("count encoder pulses", pulses, 80),
    ("wheel speed control x2", 100, 3_000),
    ("read 5 sensors (analog)", 100, 5 * 1_800),
    ("ultrasonic distance", 20, 95_000),
    ("send status to the Pi", 50, 30 * 100),
]
total = 0.0
print(f"{'job':26s} {'per s':>7s} {'ticks':>7s} {'CPU':>7s}")
for name, rate, ticks in jobs:
    load = rate * ticks / CLOCK * 100         # percent of all the Uno's clock ticks
    total += load
    print(f"{name:26s} {rate:7.0f} {ticks:7,} {load:6.1f}%")
print(f"{'total':42s} {total:6.1f}%")
print()

w, h, fps = 320, 240, 30                     # a small colour camera picture, 30 times per second
frame = w * h * 3                            # 3 bytes per pixel: red, green, blue
vision = w * h * fps * 10 / CLOCK * 100      # about 10 ticks per pixel for the simplest colour test
print(f"camera: one {w}x{h} picture = {frame:,} bytes = {frame / SRAM:.0f} x the Uno's SRAM")
print(f"camera: looking at every pixel {fps} times a second = {vision:.0f}% of the Uno's ticks")
