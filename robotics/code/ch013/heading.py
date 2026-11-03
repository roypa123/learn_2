# heading.py - keep a compass heading between 0 and 359 degrees with %
heading = 350                          # degrees: almost north (0 = north, 90 = east)
heading = (heading + 30) % 360         # turn 30 degrees to the right
print("after turning right 30:", heading)
heading = (heading - 50) % 360         # turn 50 degrees to the left
print("after turning left 50: ", heading)
heading = (heading + 725) % 360        # spin two full turns and 5 degrees more
print("after spinning 725:    ", heading)
