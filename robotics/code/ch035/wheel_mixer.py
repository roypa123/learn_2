# wheel_mixer.py - from wheel speeds to robot motion, and back, with a matrix
import numpy as np

TRACK_M = 0.15                        # the distance between Rover's two wheels

# [forward speed, turn rate] = A @ [left wheel speed, right wheel speed]
A = np.array([[0.5,            0.5],
              [-1 / TRACK_M,   1 / TRACK_M]])

wheels = np.array([0.20, 0.30])
motion = A @ wheels
print(f"wheels {wheels} m/s -> forward {motion[0]:.3f} m/s, turn {motion[1]:.3f} rad/s")

wanted = np.array([0.25, 0.5])        # we want this motion: what must the wheels do?
needed = np.linalg.solve(A, wanted)
print(f"wanted {wanted} -> wheels {needed.round(4)} m/s")

print("A inverse:")
print(np.linalg.inv(A).round(4))
print("check:", (A @ needed).round(4))
