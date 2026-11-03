# robot_range.py - how long and how far can different kinds of robot go on the same battery?
battery = 50                     # battery energy in watt-hours (Wh)

kinds = ["wheeled", "legged", "flying"]
power = [10, 40, 150]            # watts used while moving (example values for a robot of about 1 kg)
speed = [1.0, 1.0, 10.0]         # metres per second while moving

for i in range(3):
    hours = battery / power[i]                 # time = energy / power
    seconds = hours * 3600                     # 1 hour = 3600 seconds
    distance_km = speed[i] * seconds / 1000    # d = v x t, then metres -> kilometres
    print(kinds[i], "| time:", round(hours * 60), "minutes | distance:", round(distance_km, 1), "km")
