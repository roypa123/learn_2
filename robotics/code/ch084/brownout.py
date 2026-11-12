# brownout.py - a servo starts and asks for more current than the 5 V regulator can give: does the Arduino reset?
REG_V = 5.0              # the regulator's output when it is not overloaded
REG_LIMIT_A = 1.0        # the most it can supply; above this its voltage collapses
BASE_A = 0.19            # Rover's 5 V rail normally (Chapter 77)
SERVO_START_A = 1.3      # a servo's current for the first few milliseconds of a move
START_MS = 6.0
RESET_V = 4.3            # below this the Arduino may reset or misbehave
DT = 1e-6                # 1 microsecond steps


def lowest_voltage(c_farads):
    v, t, lowest = REG_V, 0.0, REG_V
    while t < 0.012:
        load = BASE_A + (SERVO_START_A if 0.001 <= t < 0.001 + START_MS / 1000 else 0.0)
        # the regulator gives what the load wants, up to its limit, and recharges the capacitor if it is low
        supply = min(REG_LIMIT_A, load + (REG_V - v) * 50)
        v = v + (supply - load) / c_farads * DT        # I = C dV/dt, turned round: dV = I dt / C
        v = min(max(v, 0.0), REG_V)                   # the rail cannot go below 0 V or above the regulator
        lowest = min(lowest, v)
        t += DT
    return lowest


print(f"servo start: {BASE_A + SERVO_START_A:.2f} A wanted, regulator gives at most {REG_LIMIT_A:.1f} A, for {START_MS:.0f} ms")
for c_uf in [100, 470, 1000, 2200, 4700]:
    low = lowest_voltage(c_uf * 1e-6)
    shortfall = BASE_A + SERVO_START_A - REG_LIMIT_A
    estimate = REG_V - shortfall * START_MS / 1000 / (c_uf * 1e-6)
    verdict = "ok" if low >= RESET_V else "RESET"
    print(f"  {c_uf:5d} uF on the rail: lowest {low:5.2f} V (simple estimate {max(estimate, 0):5.2f} V)  {verdict}")
