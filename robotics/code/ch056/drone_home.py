# drone_home.py - add up a drone's legs, then find the straight way home
import math

# each leg: (metres east, metres north) flown during that leg
legs = [(120.0, 0.0), (0.0, 90.0), (-150.0, 30.0), (-40.0, -160.0), (80.0, -10.0)]

east_m, north_m = 0.0, 0.0
flown_m = 0.0
for n, (de, dn) in enumerate(legs, start=1):
    east_m = east_m + de
    north_m = north_m + dn
    flown_m = flown_m + math.hypot(de, dn)
    print(f"after leg {n}: east {east_m:7.1f} m, north {north_m:7.1f} m, flown {flown_m:6.1f} m")

home_m = math.hypot(east_m, north_m)
home_bearing = math.degrees(math.atan2(-east_m, -north_m)) % 360
print(f"displacement from home: ({east_m:+.1f}, {north_m:+.1f}) m, {home_m:.1f} m away")
print(f"fly {home_m:.1f} m on compass bearing {home_bearing:.1f} deg to get home")
print(f"the way home is {home_m / flown_m:.0%} of the distance already flown")
