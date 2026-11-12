# iron_model.py - why some joints take 2 seconds and some never melt: heat flow from a soldering iron
T_ROOM = 25.0
T_SET = 350.0                 # the iron's temperature setting, in C
T_WET = 230.0                 # lead-free solder melts at 217-220 C; the joint must be a little hotter to wet
C_TIP = 2.0                   # heat capacity of the tip: J per C (about 5 g of copper)
DT = 0.001


def solder(c_joint, g_loss, g_contact, p_max, seconds=10.0):
    """Return the time (s) for the joint to reach T_WET, and the lowest tip temperature on the way."""
    t_tip, t_joint, t = T_SET, T_ROOM, 0.0
    lowest_tip = t_tip
    while t < seconds:
        p_heater = max(0.0, min(p_max, 5.0 * (T_SET - t_tip)))   # the iron's controller: full power when the tip cools
        flow = g_contact * (t_tip - t_joint)                      # heat from tip into joint, W
        loss = g_loss * (t_joint - T_ROOM)                        # heat the joint loses into the board and wire, W
        t_tip += (p_heater - flow) / C_TIP * DT
        t_joint += (flow - loss) / c_joint * DT
        lowest_tip = min(lowest_tip, t_tip)
        t += DT
        if t_joint >= T_WET:
            return t, lowest_tip
    return None, lowest_tip


JOINTS = {
    # name: (joint heat capacity J/C, loss to surroundings W/C)
    "resistor lead on stripboard": (0.05, 0.004),
    "header pin on a ground plane": (0.4, 0.06),
    "battery wire into a connector": (1.0, 0.03),
}
IRONS = {
    # name: (contact conductance W/C, maximum heater power W)
    "small tip, 25 W iron, no solder on tip": (0.02, 25.0),
    "small tip, 25 W iron, tinned tip": (0.08, 25.0),
    "chisel tip, 60 W station, tinned": (0.30, 60.0),
}
for jname, (c_j, g_l) in JOINTS.items():
    print(jname)
    for iname, (g_c, p) in IRONS.items():
        t, low = solder(c_j, g_l, g_c, p)
        result = f"wets in {t:4.1f} s" if t is not None else "NEVER wets (cold joint)"
        print(f"   {iname:40s} {result:24s} tip dips to {low:4.0f} C")
