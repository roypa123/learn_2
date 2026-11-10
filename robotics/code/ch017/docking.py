# docking.py - has the robot reached its charger? "Close enough" with tolerances
TARGET_X_M, TARGET_Y_M = 2.0, 1.5  # where the charger is
TARGET_HEADING_DEG = 0             # the robot must face north
POSITION_TOL_M = 0.02              # within 2 cm is good enough
HEADING_TOL_DEG = 2.0              # within 2 degrees is good enough

x_m, y_m = 2.012, 1.491            # where the robot says it is
heading_deg = 359                  # just left of north

dx_m = x_m - TARGET_X_M
dy_m = y_m - TARGET_Y_M
position_error_m = (dx_m ** 2 + dy_m ** 2) ** 0.5           # Pythagoras
heading_error_deg = (heading_deg - TARGET_HEADING_DEG + 180) % 360 - 180   # -180 to 179

position_ok = position_error_m <= POSITION_TOL_M
heading_ok = abs(heading_error_deg) <= HEADING_TOL_DEG
docked = position_ok and heading_ok

naive_ok = abs(heading_deg - TARGET_HEADING_DEG) <= HEADING_TOL_DEG   # the wrong way

print(f"position error: {position_error_m:.3f} m -> {position_ok}")
print(f"heading error:  {heading_error_deg} degrees -> {heading_ok}")
print("DOCKED:", docked)
print("exact test x == 2.0:", x_m == TARGET_X_M)
print("heading test without wrapping:", naive_ok)
