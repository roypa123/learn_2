# sci_notation.py - how long does a sensor signal take to come back from 1 metre?
SPEED_OF_LIGHT = 3e8        # metres per second
SPEED_OF_SOUND = 343        # metres per second, in air at about 20 degrees C

distance_m = 1.0

laser_time_s = 2 * distance_m / SPEED_OF_LIGHT
sound_time_s = 2 * distance_m / SPEED_OF_SOUND

print(f"laser: {laser_time_s:.3e} s = {laser_time_s * 1e9:.2f} ns")
print(f"sound: {sound_time_s:.3e} s = {sound_time_s * 1e3:.2f} ms")
print(f"sound takes {sound_time_s / laser_time_s:.2e} times longer")
