# cornering.py - how fast may a robot take a corner before its wheels or its load slide sideways?
import math

G = 9.81
FLOOR_MU = {"dry concrete": 0.8, "wet tiles": 0.3}
TOTE_MU = 0.2
SAFETY = 1.5

print("radius   floor          wheels slide above   tote slides above   safe speed")
for radius in [0.5, 1.0, 2.0, 4.0]:
    for floor, mu in FLOOR_MU.items():
        v_wheels = math.sqrt(mu * G * radius)                # mu g = v^2 / r
        v_tote = math.sqrt(TOTE_MU * G * radius)
        v_safe = math.sqrt(min(mu, TOTE_MU) * G / SAFETY * radius)
        print(f"{radius:5.1f} m  {floor:13s}  {v_wheels:10.2f} m/s   {v_tote:12.2f} m/s   {v_safe:8.2f} m/s")
