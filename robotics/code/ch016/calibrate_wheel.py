# calibrate_wheel.py - find Rover's true wheel diameter from one measured drive
PI = 3.14159
TICKS_PER_TURN = 540
NOMINAL_DIAMETER_M = 0.065         # what the wheel's data sheet says

ticks = int(input("Encoder ticks counted: "))
tape_m = float(input("Distance on the tape (m): "))

turns = ticks / TICKS_PER_TURN
thought_m = turns * PI * NOMINAL_DIAMETER_M        # what Rover believes it drove
true_diameter_m = tape_m / (turns * PI)            # distance = turns x pi x diameter
error_pct = (thought_m - tape_m) / tape_m * 100

print(f"Rover thought: {thought_m:.3f} m")
print(f"Tape says:     {tape_m:.3f} m")
print(f"Error:         {error_pct:+.2f} %")
print(f"Use WHEEL_DIAMETER_M = {true_diameter_m:.5f}")
print(ticks, tape_m, round(true_diameter_m, 5), sep=",")
