# budget.py - how much does the hardware for Rover (stage 3) cost?
parts = ["Arduino Uno (compatible)", "TB6612 motor driver", "2WD chassis + 2 gearmotors with encoders",
         "6 x AA NiMH cells + holder", "NiMH charger", "switch, fuse holder, 4 A slow fuses",
         "e-stop button", "5 V regulator", "line sensor", "distance sensor (time of flight)",
         "2 bumper switches", "wires, screws, tape"]
low = [12, 4, 15, 12, 12, 4, 5, 3, 4, 5, 2, 5]      # dollars, cheapest typical price
high = [25, 8, 25, 20, 20, 7, 10, 6, 8, 10, 4, 10]  # dollars, more expensive typical price

total_low = 0
total_high = 0
for i in range(len(parts)):
    total_low = total_low + low[i]
    total_high = total_high + high[i]
    print(parts[i], "|", low[i], "to", high[i], "dollars")
print("TOTAL |", total_low, "to", total_high, "dollars")
print("Average guess:", (total_low + total_high) / 2, "dollars")
