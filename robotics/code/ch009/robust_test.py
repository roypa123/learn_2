# robust_test.py - test one controller on 100 slightly different "real" Rovers
import random
random.seed(2)

setpoint = 0.3
max_speed = 0.25
dt = 0.1

for gain in [2.0, 4.0, 8.0]:
    passed = 0
    for trial in range(100):
        strength = random.uniform(0.6, 1.2)      # this Rover's motors: 60% to 120% of the promised speed
        stiction = random.uniform(0.0, 0.08)     # below this command (m/s), the wheels do not turn
        distance = 1.0
        for step in range(100):                  # 10 seconds
            measured = distance + random.uniform(-0.01, 0.01)
            command = max(0.0, min(max_speed, gain * (measured - setpoint)))
            speed = strength * command
            if command < stiction:
                speed = 0.0
            distance = distance - speed * dt
        if abs(distance - setpoint) <= 0.02:     # good enough: within 2 cm of the setpoint
            passed = passed + 1
    print("gain", gain, "| passed", passed, "of 100 Rovers")
