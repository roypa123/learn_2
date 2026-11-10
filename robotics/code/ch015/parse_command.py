# parse_command.py - turn a radio message into a word and a number Rover can use
PI = 3.14159
WHEEL_DIAMETER_M = 0.065           # Rover's wheel (Chapter 13)

message = "  FORWARD 0.25\n"       # what arrives: extra spaces, capitals, a newline
clean = message.strip().lower()    # remove the spaces and newline, then make it small letters
word, speed_text = clean.split()   # cut at the space: two strings, two names (Chapter 14)
speed_ms = float(speed_text)       # text to number: now we can calculate with it

turns_per_s = speed_ms / (PI * WHEEL_DIAMETER_M)   # speed / circumference (Chapter 13)
rpm = turns_per_s * 60

print("received:", repr(message))  # repr shows the hidden characters
print("cleaned: ", repr(clean))
print("command: ", word.upper())
print(f"speed:    {speed_ms:.2f} m/s")
print(f"wheels:   {rpm:.1f} rpm")
