# rover_commands.py - Rover chooses what to do from one typed command
MAX_SPEED_MS = 0.5                 # safety limit (Chapter 7)

message = input("command> ").strip().lower()
parts = message.split()            # "forward 0.25" becomes two pieces

if len(parts) == 0:                # the guard comes first: nothing was typed
    print("nothing typed: staying stopped")
elif parts[0] == "stop":
    print("stopping: speed 0.0 m/s")
elif parts[0] == "forward" or parts[0] == "back":
    if len(parts) != 2:            # these two commands need a speed
        print("please give one speed, for example: forward 0.25")
    else:
        speed_ms = float(parts[1])
        if speed_ms > MAX_SPEED_MS:        # never go past the limit
            speed_ms = MAX_SPEED_MS
            print("speed limited")
        if parts[0] == "back":
            speed_ms = -speed_ms           # backwards is a negative speed
        print(f"driving at {speed_ms:.2f} m/s")
else:
    print("unknown command:", parts[0])
