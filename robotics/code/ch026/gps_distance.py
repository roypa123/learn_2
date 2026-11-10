# gps_distance.py - how far apart are two GPS points? (good for short distances)
import math

EARTH_RADIUS_M = 6371000.0


def gps_offset(lat1, lon1, lat2, lon2):
    """Return (east_m, north_m) from point 1 to point 2. Angles in degrees."""
    north_m = math.radians(lat2 - lat1) * EARTH_RADIUS_M
    mean_lat = math.radians((lat1 + lat2) / 2)
    east_m = math.radians(lon2 - lon1) * EARTH_RADIUS_M * math.cos(mean_lat)
    return east_m, north_m


home = (48.11730, 11.51667)           # the GPS fix from Chapter 15
field_corner = (48.11810, 11.51900)

east_m, north_m = gps_offset(home[0], home[1], field_corner[0], field_corner[1])
print(f"east {east_m:.1f} m, north {north_m:.1f} m")
print(f"distance {math.hypot(east_m, north_m):.1f} m")
print(f"bearing {math.degrees(math.atan2(east_m, north_m)) % 360:.1f} degrees")
