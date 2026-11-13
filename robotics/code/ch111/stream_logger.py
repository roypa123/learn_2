# stream_logger.py - read the Arduino's CSV lines with pyserial, check each one, and save them to a file
# usage: python stream_logger.py COM3        (or /dev/ttyACM0 on Linux and the Raspberry Pi)
import csv
import sys
import time

import serial                                    # pyserial: pip install pyserial

PORT = sys.argv[1] if len(sys.argv) > 1 else "COM3"
WAIT_FOR_RESET = "--no-wait" not in sys.argv

rows = []
skipped = []
with serial.Serial(PORT, 115200, timeout=1) as ser:   # opening the port resets the Uno (Chapter 95)
    if WAIT_FOR_RESET:
        time.sleep(2)                            # let the bootloader finish and the sketch start
        ser.reset_input_buffer()                 # throw away anything that arrived meanwhile
    start = time.monotonic()
    while time.monotonic() - start < 3.0:        # log for 3 seconds
        raw = ser.readline()                     # bytes up to and including b"\n", or b"" after the timeout
        if not raw:
            continue
        text = raw.decode("ascii", errors="replace").strip()
        parts = text.split(",")
        try:
            t_ms = int(parts[0])
            angle = float(parts[1])
        except (ValueError, IndexError):         # a header, a broken line, or noise
            skipped.append(text)
            continue
        rows.append((t_ms, angle))

with open("joint_log.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["time_ms", "angle_deg"])
    writer.writerows(rows)

print(f"{len(rows)} readings saved to joint_log.csv; {len(skipped)} line(s) skipped: {skipped}")
print(f"first: {rows[0]}, last: {rows[-1]}")
angles = [a for _, a in rows]
print(f"angle from {min(angles):.1f} to {max(angles):.1f} degrees")
gaps = [b[0] - a[0] for a, b in zip(rows, rows[1:])]
print(f"time between readings: {min(gaps)} to {max(gaps)} ms")
