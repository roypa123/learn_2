# pullup_choice.py - how big should a pull-up resistor be? Two limits pull in opposite directions
V = 5.0
LEAK_A = 1e-6               # the most current a pin plus a long dusty wire may leak (datasheet: up to 1 uA)
HIGH_MIN = 3.0              # the pin must stay above this when the switch is open
PIN_C = 50e-12              # the pin plus 30 cm of wire store about 50 pF (Chapter 84)

print(f"{'pull-up':>9s} {'current when pressed':>21s} {'power':>8s} {'open-switch voltage':>20s} {'rise time':>10s}")
for r in [470, 1e3, 4.7e3, 10e3, 47e3, 100e3, 1e6, 4.7e6]:
    pressed_ma = V / r * 1000                 # the switch connects the resistor straight to ground
    power_mw = V ** 2 / r * 1000
    open_v = V - LEAK_A * r                   # leakage pulls the pin down a little through R
    rise_us = 2.2 * r * PIN_C * 1e6           # time to go from 10% to 90% after release (Chapter 84)
    ok = "ok" if open_v >= HIGH_MIN + 1.0 and pressed_ma <= 1.0 else ""
    print(f"{r / 1000:7.2f} k {pressed_ma:15.3f} mA {power_mw:6.2f} mW {open_v:15.2f} V {rise_us:8.2f} us  {ok}")
print()
print("small R: wastes current while pressed. Huge R: leakage and noise can pull the pin below HIGH, and it is slow.")
print("10 kohm (or the Arduino's built-in 20-50 kohm) sits comfortably in the middle")
