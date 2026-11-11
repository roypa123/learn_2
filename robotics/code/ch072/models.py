# models.py - four models of the cart on the ramp, from simplest to fullest, checked against the video
import math
from ramp_data import FPS, RAMP_MARKS, CART_MASS_KG, WHEEL_MASS_KG, RAMP_LENGTH_M, RAMP_RISE_M

G = 9.81
SIN = RAMP_RISE_M / RAMP_LENGTH_M
COS = math.sqrt(1 - SIN ** 2)
K = 4 * 0.5 * WHEEL_MASS_KG / CART_MASS_KG      # spinning wheels (Chapter 69)
C_RR = 0.0220                                   # from coast_down.py
CD_A = 0.004                                    # drag coefficient x front area, m^2: a box about 6 cm x 5 cm
RHO = 1.2
DT = 0.0005


def acceleration(v, wheels, rolling, drag):
    """Acceleration down the ramp at speed v, with the chosen effects switched on."""
    force = CART_MASS_KG * G * SIN                                  # gravity along the ramp (Chapter 61)
    if rolling:
        force -= C_RR * CART_MASS_KG * G * COS                      # rolling resistance (Chapter 63)
    if drag:
        force -= 0.5 * RHO * CD_A * v * v                           # air drag (Chapter 71)
    mass = CART_MASS_KG * (1 + K) if wheels else CART_MASS_KG       # spinning wheels feel heavier
    return force / mass


def times_at_marks(wheels, rolling, drag):
    """Simulate with semi-implicit Euler; return the time the cart passes each mark."""
    t, x, v = 0.0, 0.0, 0.0
    result = []
    for s, frame in RAMP_MARKS:
        while x < s:
            v = v + acceleration(v, wheels, rolling, drag) * DT
            x = x + v * DT
            t = t + DT
        result.append(t)
    return result, v


if __name__ == "__main__":
    measured = [frame / FPS for s, frame in RAMP_MARKS]
    models = [("1: sliding, nothing else", False, False, False),
              ("2: + spinning wheels", True, False, False),
              ("3: + rolling resistance", True, True, False),
              ("4: + air drag", True, True, True)]
    print("model                       time at 1.2 m   speed at 1.2 m   RMS error (frames)")
    print(f"{'measured by video':26s}  {measured[-1]:10.3f} s")
    for name, wheels, rolling, drag in models:
        sim, v_end = times_at_marks(wheels, rolling, drag)
        rms = math.sqrt(sum((a - b) ** 2 for a, b in zip(sim, measured)) / len(sim)) * FPS
        print(f"{name:26s}  {sim[-1]:10.3f} s   {v_end:10.3f} m/s   {rms:12.2f}")
