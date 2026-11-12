# led_current.py - an LED on an Uno pin: how much current flows, and is the pin safe?
# The pin's output acts like a 5 V source with about 25 ohms inside it (its output transistor, Chapter 88).
V_PIN = 5.0
R_PIN = 25.0                      # ohms inside the pin when it drives HIGH (rough, from the datasheet's curves)
V_LED = {"red": 2.0, "yellow": 2.1, "green": 2.2, "blue": 3.0}   # LED forward voltages (Chapter 82)
PIN_SAFE, PIN_MAX = 20.0, 40.0    # mA: recommended and absolute maximum for one pin

print(f"{'LED':7s} {'resistor':>9s} {'current':>8s} {'pin volts':>10s}  verdict")
for colour in ["red", "blue"]:
    for r in [0, 100, 220, 330, 1000]:
        i = (V_PIN - V_LED[colour]) / (r + R_PIN)          # Ohm's law round the loop (Chapter 75)
        ma = i * 1000
        v_out = V_PIN - i * R_PIN                          # the pin's own voltage sags as current flows
        verdict = "DAMAGE" if ma > PIN_MAX else ("too much" if ma > PIN_SAFE else "ok")
        print(f"{colour:7s} {r:6d} ohm {ma:6.1f} mA {v_out:8.2f} V  {verdict}")
print()

leds = [("green", 220), ("yellow", 220), ("red", 220), ("blue", 330), ("board L", 1000)]
total = 0.0
for colour, r in leds:
    v = V_LED.get(colour, 2.0)
    total += (V_PIN - v) / (r + R_PIN) * 1000
print(f"Rover's 5 status LEDs all on: {total:.1f} mA (the whole chip may give at most 200 mA)")
