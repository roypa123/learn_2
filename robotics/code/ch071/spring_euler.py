# spring_euler.py - a mass on a spring: plain Euler slowly gains energy, semi-implicit Euler does not
K = 40.0          # spring stiffness, N/m
M = 1.0           # mass, kg
DT = 0.02
STEPS = 500       # 10 seconds


def energy(x, v):
    return 0.5 * M * v * v + 0.5 * K * x * x        # kinetic + spring energy (Chapter 67)


for method in ["plain Euler", "semi-implicit Euler"]:
    x, v = 0.1, 0.0                                  # pulled 10 cm and let go
    for step in range(STEPS):
        a = -K * x / M                               # the spring pulls back towards 0
        if method == "plain Euler":
            x, v = x + v * DT, v + a * DT            # both use the OLD values of x and v
        else:
            v = v + a * DT                           # first the speed...
            x = x + v * DT                           # ...then move with the NEW speed
    print(f"{method:20s}: after 10 s, x = {x:+.4f} m, energy {energy(x, v):.4f} J (started at {energy(0.1, 0):.4f} J)")
