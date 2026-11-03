# e_stop_distance.py - how far does a warehouse robot move after a person sees danger?
speed = 1.5             # the robot drives at 1.5 m/s
brake_distance = 1.13   # metres to stand still at 1.5 m/s, measured by the maker (Chapter 2)
circuit_delay = 0.02    # the e-stop circuit needs 0.02 s to cut the motor power

situations = ["hand on the button", "surprised, button close", "must walk to a button"]
human_times = [0.25, 1.0, 3.0]   # seconds from "danger!" until the button is pressed

for i in range(3):
    human = speed * human_times[i]        # distance driven while the person reacts
    circuit = speed * circuit_delay       # distance driven while the circuit works
    total = human + circuit + brake_distance
    print(situations[i], "| person", round(human, 3), "m | circuit", round(circuit, 3),
          "m | braking", brake_distance, "m | total", round(total, 3), "m")
