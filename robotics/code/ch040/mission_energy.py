# mission_energy.py - E = P_d * d / v + P_w * t_w, for a delivery robot
JOULES_PER_WH = 3600


def trip_energy_wh(drive_w, wait_w, distance_m, speed_ms, wait_s):
    drive_time_s = distance_m / speed_ms
    energy_j = drive_w * drive_time_s + wait_w * wait_s
    return energy_j / JOULES_PER_WH


BATTERY_WH = 200
RESERVE = 0.20
usable_wh = BATTERY_WH * (1 - RESERVE)

print("wait (min)  energy (Wh)  whole trips")
for wait_min in [0, 5, 10, 20, 40]:
    energy = trip_energy_wh(60, 15, 800, 1.2, wait_min * 60)
    trips = int(usable_wh // energy)
    print(f"{wait_min:10d} {energy:12.1f} {trips:12d}")
