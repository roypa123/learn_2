# euler_fall.py - Euler's method: simulate a falling ball in small steps, and check it against the exact answer
G = 9.81
T_END = 2.0


def simulate(dt):
    """Step a dropped ball forward in time; return its fall distance after T_END seconds."""
    t, x, v = 0.0, 0.0, 0.0           # time, distance fallen, speed (down is positive)
    for step in range(round(T_END / dt)):
        a = G                          # 1) work out the acceleration from the forces now
        x = x + v * dt                 # 2) move, using the speed at the START of the step
        v = v + a * dt                 # 3) change the speed
        t = t + dt
    return x


exact = 0.5 * G * T_END ** 2
print(f"exact: 1/2 g t^2 = {exact:.4f} m")
for dt in [0.5, 0.1, 0.01, 0.001]:
    x = simulate(dt)
    print(f"dt = {dt:5.3f} s: {round(T_END / dt):5d} steps, Euler gives {x:8.4f} m, error {x - exact:+8.4f} m")
