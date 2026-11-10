# spec_sheet.py - from a mixed-unit data sheet to the motor speed we must order
import math

MPH_TO_MS = 0.44704
INCH_TO_M = 0.0254

top_speed_mph = 3.0
wheel_diameter_in = 8.0
gear_ratio = 30

speed_ms = top_speed_mph * MPH_TO_MS
diameter_m = wheel_diameter_in * INCH_TO_M
wheel_circle_m = math.pi * diameter_m
wheel_turns_per_s = speed_ms / wheel_circle_m
wheel_rpm = wheel_turns_per_s * 60
motor_rpm = wheel_rpm * gear_ratio

print(f"top speed     : {speed_ms:.3f} m/s")
print(f"wheel diameter: {diameter_m:.4f} m")
print(f"one wheel turn: {wheel_circle_m:.4f} m")
print(f"wheel speed   : {wheel_turns_per_s:.3f} turns/s = {wheel_rpm:.1f} rpm")
print(f"motor speed   : {motor_rpm:.0f} rpm")
