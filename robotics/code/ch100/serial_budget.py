# serial_budget.py - how many log lines per second can a serial link carry at each baud rate?
LINE_CHARS = 23                 # "4962,304,299,7408,101" plus the 2 end-of-line characters (\r\n)
WANTED = 50                     # lines per second Rover wants to send
BITS_PER_CHAR = 10              # 8 data bits + a start bit + a stop bit (Chapter 107)

print(f"one line = {LINE_CHARS} characters; Rover wants {WANTED} lines per second")
print(f"{'baud':>7s} {'chars/s':>8s} {'lines/s max':>12s} {'link busy':>10s}  verdict")
for baud in [9600, 19200, 57600, 115200]:
    chars_per_s = baud / BITS_PER_CHAR
    max_lines = chars_per_s / LINE_CHARS
    busy = WANTED * LINE_CHARS / chars_per_s * 100       # percent of the link's time used
    verdict = "falls behind" if busy > 100 else ("tight" if busy > 70 else "ok")
    print(f"{baud:7d} {chars_per_s:8.0f} {max_lines:12.1f} {busy:9.0f}%  {verdict}")
print()

binary = 2 + 5 * 2 + 1           # two start bytes, five 2-byte numbers, a checksum byte (Chapter 107)
print(f"the same 5 numbers sent as binary: {binary} bytes instead of {LINE_CHARS} characters "
      f"({LINE_CHARS / binary:.1f} x less to send)")
