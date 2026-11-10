# battery_bar.py - draw a battery gauge out of characters
BAR_WIDTH = 20                     # the bar is 20 characters long

percent = int(input("Battery percent (0-100): "))
filled = percent * BAR_WIDTH // 100          # how many characters to fill
bar = "#" * filled + "-" * (BAR_WIDTH - filled)
print(f"[{bar}] {percent:3d}%")
