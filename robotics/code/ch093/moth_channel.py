# moth_channel.py - one of Moth's two "nerves": an LDR divider drives a power transistor that drives a motor
V = 6.0                       # 4 x AA cells
R_AT_10_LUX, GAMMA = 20000.0, 0.7   # the LDR from Chapter 79
R_B = 4700.0                  # the divider's lower resistor: base to ground (Chapter 79's best value)
BETA = 150                    # BD139-16 power transistor gain (Chapter 87)
V_BE = 0.7
R_MOTOR = 15.0                # the small toy motor from Chapter 87
V_CE_SAT = 0.2
I_START = 0.08                # the motor needs about 80 mA to start
THETA = 100.0                 # BD139 (TO-126 case) in free air, C per W (Chapter 76)
I_MAX = (V - V_CE_SAT) / R_MOTOR


def ldr(lux):
    return R_AT_10_LUX * (lux / 10) ** (-GAMMA)


def channel(lux, r_b=R_B):
    """Return base current, motor current and transistor heat for this much light."""
    r_ldr = ldr(lux)
    v_th = V * r_b / (r_ldr + r_b)              # the divider's open-circuit voltage (Chapter 79)
    r_th = r_ldr * r_b / (r_ldr + r_b)          # what the base "sees": LDR and R_B in parallel
    i_b = max(0.0, (v_th - V_BE) / r_th)        # the base pulls the divider down to 0.7 V
    i_c = min(BETA * i_b, I_MAX)                # gain, until the transistor is fully on
    v_ce = V - i_c * R_MOTOR
    heat = v_ce * i_c                           # power in the transistor (Chapter 76)
    return i_b, i_c, heat


if __name__ == "__main__":
    print(f"motor current when fully on: {I_MAX * 1000:.0f} mA")
    print(f"{'lux':>6s} {'LDR':>8s} {'base':>8s} {'motor':>7s} {'heat':>8s} {'temp rise':>9s}  motor")
    for lux in [5, 10, 20, 40, 70, 100, 150, 200, 300, 500]:
        i_b, i_c, heat = channel(lux)
        state = "stopped" if i_c < I_START else ("full speed" if i_c >= I_MAX - 1e-9 else "turning")
        print(f"{lux:6d} {ldr(lux):6.0f} ohm {i_b * 1000:5.2f} mA {i_c * 1000:4.0f} mA {heat * 1000:5.0f} mW {heat * THETA:7.0f} C  {state}")
    worst = max(channel(l / 10)[2] for l in range(10, 10000))
    print()
    print(f"worst transistor heat: {worst * 1000:.0f} mW -> {worst * THETA:.0f} C above the room in a BD139")
    print(f"the same in a 2N2222 (TO-92, 200 C/W): {worst * 200:.0f} C above the room -> too hot")
