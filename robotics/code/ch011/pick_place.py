# pick_place.py - a robot arm picks up a block: the steps must come in the right order
z = 10                       # gripper height above the table, in cm (the block is on the table, at 0 cm)
gripper = "open"
holding = False
print("start:          height", z, "| gripper", gripper, "| holding", holding)

z = 0                        # 1. move down to the block
print("1. move down:   height", z, "| gripper", gripper, "| holding", holding)
gripper = "closed"           # 2. close the gripper
holding = z == 0             #    it only catches the block if it is down at the block (height 0)
print("2. close:       height", z, "| gripper", gripper, "| holding", holding)
z = 10                       # 3. lift
print("3. lift:        height", z, "| gripper", gripper, "| holding", holding)
