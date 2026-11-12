# divider.py - the voltage divider: Vout = Vin x R2 / (R1 + R2), and what happens when you load it
def divider(v_in, r1, r2):
    """Output voltage of an unloaded divider: R1 on top, R2 to ground."""
    return v_in * r2 / (r1 + r2)


def parallel(a, b):
    return a * b / (a + b)


print("unloaded dividers from 5 V:")
for r1, r2 in [(1000, 1000), (2000, 1000), (1000, 2000), (10000, 10000), (100000, 100000)]:
    print(f"  R1 = {r1:6d}, R2 = {r2:6d}: Vout = {divider(5.0, r1, r2):.3f} V, "
          f"current {5.0 / (r1 + r2) * 1000:.3f} mA, wasted {5.0 ** 2 / (r1 + r2) * 1000:.3f} mW")

print()
print("the same 1:1 dividers with a 10 kohm load across R2:")
for r in [1000, 10000, 100000]:
    loaded = divider(5.0, r, parallel(r, 10000))       # the load is in parallel with R2
    print(f"  R1 = R2 = {r:6d}: unloaded 2.500 V, loaded {loaded:.3f} V  ({(loaded - 2.5) / 2.5:+.1%})")

print()
print("the divider's output acts like a source of Vout with a resistance R1 || R2 in series:")
for r in [1000, 10000, 100000]:
    r_out = parallel(r, r)
    print(f"  R1 = R2 = {r:6d}: output resistance {r_out:8.0f} ohm; with 10 kohm load: "
          f"{2.5 * 10000 / (r_out + 10000):.3f} V")
