# make_packet.py - build and check Rover's link packets, as the Raspberry Pi side does (Chapter 111 sends them)
# packet: START (0xAA), LEN, TYPE, LEN payload bytes, CHECKSUM = (LEN + TYPE + payload) & 0xFF
START = 0xAA


def packet(ptype, payload):
    body = [len(payload), ptype] + list(payload)
    return bytes([START] + body + [sum(body) & 0xFF])


def int16_bytes(v):
    v &= 0xFFFF                                   # two's complement, 16 bits (Chapter 96)
    return [v & 0xFF, v >> 8]                     # low byte first: the order the Uno uses


def motor(left, right):
    return packet(ord("M"), int16_bytes(left) + int16_bytes(right))


def check(p):
    """True if p is a complete packet whose checksum is right."""
    if len(p) < 4 or p[0] != START or len(p) != p[1] + 4:
        return False
    return sum(p[1:-1]) & 0xFF == p[-1]


for left, right in [(120, 120), (200, -80)]:
    p = motor(left, right)
    print(f"M {left:4d} {right:4d}  ->  {p.hex(' ').upper()}   checksum right: {check(p)}")
bad = bytearray(motor(50, 50))
print(f"M   50   50  ->  {bytes(bad).hex(' ').upper()}   checksum right: {check(bad)}")
bad[3] ^= 0b00000100                              # noise flips one bit of the payload
print(f"one bit flipped: {bytes(bad).hex(' ').upper()}   checksum right: {check(bad)}")
