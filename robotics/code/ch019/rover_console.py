# rover_console.py - keep taking commands until the person types "quit"
x_m = 0.0                          # STATE: position
moves = 0                          # STATE: a counter

print("Commands: forward <m>, back <m>, where, quit")

while True:                        # keep going until a break
    parts = input("rover> ").strip().lower().split()

    if len(parts) == 0:            # an empty line: ask again
        continue
    word = parts[0]

    if word == "quit":
        break                      # leave the loop

    if word == "where":
        print(f"  x = {x_m:.2f} m after {moves} moves")
        continue                   # back to the top

    if word != "forward" and word != "back":
        print("  unknown command:", word)
        continue

    if len(parts) != 2:
        print("  please give a distance")
        continue

    distance_m = float(parts[1])
    if word == "back":
        distance_m = -distance_m
    x_m += distance_m
    moves += 1
    print(f"  moved {distance_m:+.2f} m")

print("Goodbye. Final position:", round(x_m, 2), "m")
