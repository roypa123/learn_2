# swap_motors.py - crossed motor wires? Swap two variables instead of re-soldering
left_pin = 5                  # the pin the program sends the LEFT motor speed to
right_pin = 6                 # the pin the program sends the RIGHT motor speed to
left_speed = 0.1              # to turn left: left wheel slow ...
right_speed = 0.3             # ... and right wheel fast
print("before:       pin", left_pin, "gets", left_speed, "| pin", right_pin, "gets", right_speed)

# the test drive showed the wires are crossed: swap the pins, using a spare box
temp = left_pin               # 1. keep a copy of the left pin
left_pin = right_pin          # 2. left gets the right pin (the old value is safe in temp)
right_pin = temp              # 3. right gets the copy
print("after swap 1: pin", left_pin, "gets", left_speed, "| pin", right_pin, "gets", right_speed)

# Python's short way does the same in one line (here it swaps them back again)
left_pin, right_pin = right_pin, left_pin
print("after swap 2: pin", left_pin, "gets", left_speed, "| pin", right_pin, "gets", right_speed)
