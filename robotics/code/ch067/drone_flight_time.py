# drone_flight_time.py - how long can a delivery drone fly on one battery?
G = 9.81
BATTERY_WH = 74.0              # 4-cell LiPo, 14.8 V x 5.0 Ah
USABLE = 0.80                  # never empty a LiPo completely (Chapter 89)
HOVER_POWER_W = 180.0          # measured on a test stand with the drone at 1.6 kg
ELECTRONICS_W = 6.0            # flight controller, GPS, radio, camera
MASS_KG = 1.6
CLIMB_EFFICIENCY = 0.5         # only half the extra electrical power ends up as height

usable_j = BATTERY_WH * USABLE * 3600
print(f"usable energy: {BATTERY_WH * USABLE:.1f} Wh = {usable_j:,.0f} J")

hover_s = usable_j / (HOVER_POWER_W + ELECTRONICS_W)
print(f"hovering only: {hover_s / 60:.1f} minutes")

climb_j = MASS_KG * G * 60 / CLIMB_EFFICIENCY      # climbing to 60 m, and back down for free
print(f"climbing to 60 m costs {climb_j:.0f} J, the same as {climb_j / (HOVER_POWER_W + ELECTRONICS_W):.1f} s of hovering")

parcel_kg = 0.5
heavier_power = HOVER_POWER_W * ((MASS_KG + parcel_kg) / MASS_KG) ** 1.5   # hover power grows faster than mass
loaded_s = usable_j / (heavier_power + ELECTRONICS_W)
print(f"with a {parcel_kg} kg parcel: hover power {heavier_power:.0f} W, flight time {loaded_s / 60:.1f} minutes")
