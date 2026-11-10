# sensor_stream.py - survive damaged lines from an Arduino, and count them
def parse_line(line):
    """Return (time_s, distance_m, battery_v), or None if the line is damaged."""
    try:
        t_part, d_part, v_part = line.strip().split(";")
        return float(t_part[2:]), float(d_part[2:]), float(v_part[2:])
    except ValueError:
        return None


stream = [
    "t=12.40;d=0.42;v=7.13\n",
    "t=12.50;d=0.4",               # cut short
    "t=12.60;d=0.4#;v=7.12\n",     # a damaged character
    "\n",                          # an empty line
    "t=12.70;d=0.44;v=7.11\n",
]

good = 0
bad = 0
for line in stream:
    result = parse_line(line)
    if result is None:
        bad += 1
        print("skipped:", repr(line))
    else:
        good += 1
        time_s, distance_m, battery_v = result
        print(f"t={time_s:.2f}  d={distance_m:.2f}  v={battery_v:.2f}")

print(f"good {good}, bad {bad}, loss {bad / (good + bad):.0%}")
