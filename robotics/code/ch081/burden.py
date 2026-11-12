# burden.py - an ammeter is a small resistor in the loop: how much does it change the current?
SHUNTS = {"mA socket (200 mA range)": 1.0, "10 A socket": 0.01}     # typical resistances inside a cheap meter

circuits = [
    # name, supply volts, circuit resistance in ohms (without the meter)
    ("LED and 150 ohm resistor on 5 V (LED drop removed: 3 V across 150 ohm)", 3.0, 150.0),
    ("a 100 ohm sensor on 5 V", 5.0, 100.0),
    ("Rover's stalled motor on 7.2 V (4.8 ohm + 0.15 inside)", 7.2, 4.95),
]
for name, v, r in circuits:
    true_i = v / r
    print(f"{name}: true current {true_i * 1000:.1f} mA")
    for socket, shunt in SHUNTS.items():
        measured = v / (r + shunt)                   # the shunt is in series with everything
        burden = measured * shunt                    # the voltage the meter itself takes
        print(f"  {socket:26s}: reads {measured * 1000:8.1f} mA ({(measured - true_i) / true_i:+.1%}), meter takes {burden * 1000:6.1f} mV")
print()
print("the stalled motor's 1.45 A is far above the 200 mA range: on the mA socket the meter's fuse would blow")
