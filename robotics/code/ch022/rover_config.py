# rover_config.py - all of Rover's settings in one dictionary
PI = 3.14159

config = {
    "name": "Rover",
    "wheel_diameter_m": 0.06589,      # from the calibration in Chapter 16
    "ticks_per_turn": 540,
    "max_speed_ms": 0.5,
    "battery_wh": 11.52,
    "power_w": 3.78,
}

for key, value in config.items():     # every setting, name and value
    print(f"{key:<18} {value}")

circumference_m = PI * config["wheel_diameter_m"]
metres_per_tick = circumference_m / config["ticks_per_turn"]
hours = config["battery_wh"] / config["power_w"]
camera_on = config.get("camera", False)     # not in the dictionary: use the default

print(f"one tick = {metres_per_tick * 1000:.3f} mm")
print(f"running time = {hours:.2f} h")
print("camera fitted:", camera_on)
