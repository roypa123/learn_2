# tilt.py - find a robot's tilt from a still accelerometer, which feels gravity as 9.81 m/s^2 "up"
import math
import random

G = 9.81
random.seed(3)


def accel_reading(pitch_deg, noise=0.0):
    """What a still accelerometer reads (x forwards, z up through the robot) when tilted nose-up by pitch."""
    p = math.radians(pitch_deg)
    ax = G * math.sin(p) + random.gauss(0, noise)
    az = G * math.cos(p) + random.gauss(0, noise)
    return ax, az


def pitch_from(ax, az):
    return math.degrees(math.atan2(ax, az))


for true_pitch in [0, 5, 15, 30, -10]:
    ax, az = accel_reading(true_pitch)
    print(f"true pitch {true_pitch:4d} deg: reads ax {ax:+5.2f}, az {az:5.2f} -> pitch {pitch_from(ax, az):+6.1f} deg")

print("with noise of 0.2 m/s^2, true pitch 15 deg:")
one = [pitch_from(*accel_reading(15, 0.2)) for k in range(5)]
print("  single readings:", [round(x, 1) for x in one])
many = [pitch_from(*accel_reading(15, 0.2)) for k in range(100)]
print(f"  average of 100 readings: {sum(many) / len(many):.2f} deg")
