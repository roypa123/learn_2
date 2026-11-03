# pick_place_wrong.py - the same steps as pick_place.py, but "close" comes before "move down"
z = 10
gripper = "open"
holding = False
print("start:          height", z, "| gripper", gripper, "| holding", holding)

gripper = "closed"           # 2. close the gripper (too early!)
holding = z == 0
print("2. close:       height", z, "| gripper", gripper, "| holding", holding)
z = 0                        # 1. move down to the block
print("1. move down:   height", z, "| gripper", gripper, "| holding", holding)
z = 10                       # 3. lift
print("3. lift:        height", z, "| gripper", gripper, "| holding", holding)
