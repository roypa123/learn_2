# corridor_trip.py - distance travelled and displacement for a robot in a corridor
positions_m = [0.0, 2.0, 5.0, 5.0, 3.0, 1.5, 4.0]   # position after each move

distance_m = 0.0
for i in range(1, len(positions_m)):
    step_m = positions_m[i] - positions_m[i - 1]
    distance_m = distance_m + abs(step_m)
    print(f"move {i}: from {positions_m[i - 1]:4.1f} to {positions_m[i]:4.1f}   step {step_m:+5.1f} m")

displacement_m = positions_m[-1] - positions_m[0]
print(f"distance travelled: {distance_m:.1f} m")
print(f"displacement:       {displacement_m:+.1f} m")
