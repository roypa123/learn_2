# order_matters.py - the same two steps, done in two different orders
battery = 80                 # Rover's battery is 80% full
battery = battery + 20       # step 1: charge it by 20%
battery = battery / 2        # step 2: drive around the house, using half of what is left
print("charge first, then drive:", battery, "%")

battery = 80                 # start again from 80%
battery = battery / 2        # step 2 first: drive around the house
battery = battery + 20       # step 1 second: charge by 20%
print("drive first, then charge:", battery, "%")
