# uart_frame.py - the bits a UART sends for one character, and when they are sent
def frame(byte):
    bits = [0]                                    # the start bit: always 0 (LOW)
    bits += [(byte >> k) & 1 for k in range(8)]   # 8 data bits, lowest bit FIRST
    bits += [1]                                   # the stop bit: always 1 (HIGH)
    return bits


BAUD = 9600
t_bit = 1e6 / BAUD                                # microseconds per bit
names = ["start"] + [f"bit {k}" for k in range(8)] + ["stop"]
print(f"'A' = 0x41 = 0b01000001, sent at {BAUD} baud: each bit lasts {t_bit:.1f} us")
for k, (name, b) in enumerate(zip(names, frame(ord("A")))):
    level = "HIGH" if b else "LOW"
    print(f"  {name:>6s}: {b} {level:4s} from {k * t_bit:6.1f} to {(k + 1) * t_bit:6.1f} us")
for baud in (9600, 115200):
    char_us = 10 * 1e6 / baud
    print(f"at {baud:6d} baud: one character takes {char_us:7.1f} us; at most {baud // 10:5d} characters per second")
