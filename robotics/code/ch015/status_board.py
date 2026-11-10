# status_board.py - a tidy table of robots, lined up with f-strings
print(f"{'ROBOT':<10}{'X (m)':>8}{'BATTERY':>10}")
print("-" * 28)

name, x_m, battery_pct = "rover", 2.0, 87.5
print(f"{name.upper():<10}{x_m:>8.2f}{battery_pct:>9.1f}%")

name, x_m, battery_pct = "cleaner", 12.345, 9.0
print(f"{name.upper():<10}{x_m:>8.2f}{battery_pct:>9.1f}%")

name, x_m, battery_pct = "arm", 0.5, 100.0
print(f"{name.upper():<10}{x_m:>8.2f}{battery_pct:>9.1f}%")
