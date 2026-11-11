# drag_fall.py - a drone falls from 30 m with air drag, and opens a parachute after 1.5 s
import math

G = 9.81
MASS = 1.6                 # kg
RHO = 1.2                  # kg/m^3, density of air
CD_A_DRONE = 0.05          # drag coefficient x area of the drone, m^2
CD_A_CHUTE = 1.2           # drag coefficient x area with the parachute open, m^2
OPEN_AT = 1.5              # s after the motors stop
DT = 0.001

t, h, v = 0.0, 30.0, 0.0   # v is the downward speed
report = 0.0
while h > 0:
    cd_a = CD_A_CHUTE if t >= OPEN_AT else CD_A_DRONE
    drag = 0.5 * RHO * cd_a * v * v            # grows with speed squared, pushes up
    a = (MASS * G - drag) / MASS               # Newton's second law, down positive
    h = h - v * DT
    v = v + a * DT
    t = t + DT
    if t >= report:
        print(f"t = {t:4.2f} s   height {h:6.2f} m   speed {v:5.2f} m/s   drag {drag:6.2f} N")
        report = report + 0.5
print(f"lands after {t:.2f} s at {v:.2f} m/s")
print(f"terminal speed with the parachute: {math.sqrt(2 * MASS * G / (RHO * CD_A_CHUTE)):.2f} m/s")
print(f"terminal speed without it:         {math.sqrt(2 * MASS * G / (RHO * CD_A_DRONE)):.2f} m/s")
