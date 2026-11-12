# meter_loading.py - a voltmeter is a big resistor: how much does it disturb what it measures?
def parallel(a, b):
    return a * b / (a + b)


V_IN = 10.0
print("measuring the tap of an R-over-R divider on 10 V (true value 5.000 V)")
print(f"{'R1 = R2':>10s} {'10 Mohm meter':>14s} {'1 Mohm meter':>13s} {'20 kohm/V analog on 10 V range':>31s}")
for r in [1e3, 1e4, 1e5, 1e6]:
    readings = []
    for meter in [10e6, 1e6, 20000 * 10]:              # an old analog meter: 20 kohm per volt of range
        bottom = parallel(r, meter)                    # the meter sits across R2
        readings.append(V_IN * bottom / (r + bottom))
    print(f"{r:10.0f} " + " ".join(f"{v:9.3f} V ({(v - 5) / 5:+.1%})" for v in readings))

print()
print("rule: the meter's input resistance should be at least 100 x the circuit's output resistance (R1 || R2)")
