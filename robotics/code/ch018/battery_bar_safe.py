# battery_bar_safe.py - the Chapter 16 gauge, now refusing impossible values
BAR_WIDTH = 20

percent = int(input("Battery percent (0-100): "))

if percent < 0 or percent > 100:
    print("That is not a battery percentage.")
else:
    filled = percent * BAR_WIDTH // 100
    bar = "#" * filled + "-" * (BAR_WIDTH - filled)
    if percent <= 20:
        warning = "  LOW!"
    else:
        warning = ""
    print(f"[{bar}] {percent:3d}%{warning}")
