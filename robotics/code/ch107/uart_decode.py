# uart_decode.py - a receiver reads each bit in its middle, timed by ITS OWN clock.
# What happens when the sender's clock is a few percent fast or slow?
def frame(byte):
    return [0] + [(byte >> k) & 1 for k in range(8)] + [1]


def sender(text, error):
    """The line level at time t (in the receiver's bit-times), for a sender whose clock is off by error."""
    bits = []
    for ch in text:
        bits += frame(ord(ch))                    # characters sent back to back, with no gap
    def line(t):
        k = int(t * (1 + error))                  # which of the sender's bits is on the line at time t
        return bits[k] if k < len(bits) else 1    # after the last stop bit the line rests HIGH
    return line


def receive_first(line):
    # the start bit's falling edge is at t = 0: data bit k is read at k + 1.5, the stop bit at 9.5
    value = 0
    for k in range(8):
        value |= line(k + 1.5) << k
    return value, line(9.5) == 1


print("sender's clock   first byte read   stop bit")
for error in [0.0, 0.02, 0.04, 0.05, 0.06, -0.04, -0.06]:
    value, stop_ok = receive_first(sender("AB", error))
    verdict = "right" if value == ord("A") else "WRONG"
    print(f"{error * 100:+6.0f} %         0x{value:02X} ({verdict})      {'OK' if stop_ok else 'missing: framing error'}")
