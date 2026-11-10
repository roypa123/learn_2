# safe_console.py - a Rover console that bad input can no longer crash
def parse_command(text):
    """Return (word, number). Raise ValueError if the text makes no sense."""
    parts = text.strip().lower().split()
    if len(parts) != 2:
        raise ValueError("please type a word and a number")
    word = parts[0]
    if word != "forward" and word != "back":
        raise ValueError(f"unknown command: {word}")
    return word, float(parts[1])          # float can raise ValueError too


x_m = 0.0
while True:
    text = input("rover> ")
    if text.strip().lower() == "quit":
        break
    try:
        word, distance_m = parse_command(text)
    except ValueError as error:
        print("  not understood:", error)
        continue                          # back to the top: x_m is untouched
    if word == "back":
        distance_m = -distance_m
    x_m += distance_m
    print(f"  x = {x_m:.2f} m")

print("Goodbye")
