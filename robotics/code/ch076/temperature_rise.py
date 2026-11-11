# temperature_rise.py - how hot does a part get? rise = power x thermal resistance
ROOM_C = 25.0

parts = [
    # name, watts of heat, thermal resistance in degrees C per watt, maximum allowed temperature
    ("1/4 W resistor used as a 0.1 ohm shunt at stall", 0.225, 400, 155),
    ("1 W resistor as the same shunt", 0.225, 100, 155),
    ("motor driver chip, no heat sink, motors driving", 0.25, 60, 150),
    ("motor driver chip, no heat sink, both motors stalled", 2.25, 60, 150),
    ("motor driver chip with a small heat sink, stalled", 2.25, 25, 150),
    ("5 V regulator making 1 A from 7.2 V, no heat sink", 2.2, 50, 125),
]
print(f"{'part':54s} {'watts':>6s} {'C/W':>5s} {'rise':>7s} {'temp':>7s} {'ok?':>4s}")
for name, watts, c_per_w, limit in parts:
    rise = watts * c_per_w
    temp = ROOM_C + rise
    ok = "yes" if temp <= limit else "NO"
    print(f"{name:54s} {watts:6.3f} {c_per_w:5d} {rise:6.0f} C {temp:5.0f} C {ok:>4s}")
