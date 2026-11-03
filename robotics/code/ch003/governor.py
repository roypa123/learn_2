# governor.py - a steam engine with and without a speed governor (feedback, about 1788)
wanted = 100          # the speed we want (turns per minute)

speed_open = 100.0    # engine without a governor: the valve stays half open
speed_gov = 100.0     # engine with a governor: the valve opens or closes with the speed

for second in range(0, 61):
    if second < 20:
        load = 1.0    # normal work
    else:
        load = 1.5    # at second 20 the machines need more power

    valve_open = 0.5                                   # fixed valve, no feedback
    valve_gov = 0.5 + 0.02 * (wanted - speed_gov)      # slower than wanted -> open the valve more
    valve_gov = max(0.0, min(1.0, valve_gov))          # a valve cannot open less than 0 or more than 1

    if second % 10 == 0:
        print("second", second, "| load", load, "| no governor:", round(speed_open, 1),
              "| with governor:", round(speed_gov, 1), "| valve", round(valve_gov, 2))

    speed_open = speed_open + 10 * (2.0 * valve_open - load * speed_open / 100)
    speed_gov = speed_gov + 10 * (2.0 * valve_gov - load * speed_gov / 100)
