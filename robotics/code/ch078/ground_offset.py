# ground_offset.py - a sensor and a motor share one ground wire: the voltage law shows the error it causes
WIRE_OHM = 0.02            # the shared ground wire from the board to the battery
SENSOR_V = 2.50            # what the sensor really outputs, measured from its own ground
ADC_STEP = 5.0 / 1024

print(f"{'motor current':>14s} {'ground lifted by':>17s} {'Arduino reads':>14s} {'error in ADC steps':>19s}")
for motor_a in [0.0, 0.5, 1.5, 3.0]:
    lift = motor_a * WIRE_OHM                  # V = I x R along the shared ground wire
    # the loop: Arduino ground -> battery ground -> up the shared wire to the sensor's ground -> sensor output
    seen = SENSOR_V + lift                     # the sensor's ground sits 'lift' volts above the Arduino's ground
    print(f"{motor_a:11.1f} A {lift * 1000:13.1f} mV {seen:12.3f} V {lift / ADC_STEP:16.1f}")

print()
print("fix: give the sensor its own ground wire back to the Arduino (a 'star' ground), so no motor current flows in it")
