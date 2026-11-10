# homing.py - move a robot arm joint until it touches its limit switch
STEP_DEG = 0.5                     # how far one motor step moves the joint
MAX_STEPS = 400                    # 200 degrees: the joint cannot honestly travel further
SWITCH_AT_DEG = -37.0              # the simulated switch (the program only sees "pressed")

angle_deg = 0.0                    # where the joint starts (the program does not really know)
steps = 0
homed = False

while steps < MAX_STEPS:
    switch_pressed = angle_deg <= SWITCH_AT_DEG     # read the switch
    if switch_pressed:
        homed = True
        break
    angle_deg -= STEP_DEG          # one small step towards the switch
    steps += 1

if homed:
    print(f"homed after {steps} steps: the joint is at its zero position")
else:
    print(f"FAULT: no switch after {steps} steps. Motor off, call a person.")
