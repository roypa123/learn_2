# speed_and_temperature.py - conversions a robot meets every day
import math


def kmh_to_ms(kmh):
    return kmh * 1000 / 3600


def wheel_speed_ms(rpm, diameter_m):
    turns_per_second = rpm / 60
    return turns_per_second * math.pi * diameter_m


def celsius_to_kelvin(celsius):
    return celsius + 273.15


def celsius_to_fahrenheit(celsius):
    return celsius * 9 / 5 + 32


print(f"6 km/h is {kmh_to_ms(6):.3f} m/s")
print(f"Rover at 120 rpm: {wheel_speed_ms(120, 0.06589):.3f} m/s")
print(f"25 C is {celsius_to_kelvin(25):.2f} K")
print(f"25 C is {celsius_to_fahrenheit(25):.1f} F")
