# rover_driver.py - the Raspberry Pi side of Rover's link (Chapter 107): send motor packets, read status packets
# usage: python rover_driver.py COM3          (the Arduino runs ch107/rover_link/rover_link.ino)
import struct
import sys
import time

import serial                                    # pyserial: pip install pyserial

PORT = sys.argv[1] if len(sys.argv) > 1 else "COM3"
WAIT_FOR_RESET = "--no-wait" not in sys.argv
START = 0xAA


def packet(ptype, payload):
    body = bytes([len(payload), ptype]) + payload
    return bytes([START]) + body + bytes([sum(body) & 0xFF])


def motor(left, right):
    return packet(ord("M"), struct.pack("<hh", left, right))   # two int16, low byte first


class PacketReader:
    """Collects bytes and gives back each complete packet whose checksum is right (Chapter 107)."""

    def __init__(self):
        self.buf = bytearray()

    def feed(self, data):
        self.buf += data
        found = []
        while True:
            k = self.buf.find(bytes([START]))
            if k < 0:
                self.buf.clear()
                return found
            del self.buf[:k]                     # skip anything before a start byte
            if len(self.buf) < 2 or len(self.buf) < self.buf[1] + 4:
                return found                     # not complete yet: wait for more bytes
            n = self.buf[1]
            p = bytes(self.buf[:n + 4])
            if sum(p[1:-1]) & 0xFF == p[-1]:
                found.append((chr(p[2]), p[3:-1]))
                del self.buf[:n + 4]
            else:
                del self.buf[:1]                 # a false start or a damaged packet: look further on


plan = [(0, 0), (60, 60), (120, 120), (180, 180), (200, 200), (200, 120), (200, 60), (150, 150)]
reader = PacketReader()
with serial.Serial(PORT, 115200, timeout=0.1) as ser:
    if WAIT_FOR_RESET:
        time.sleep(2)
        ser.reset_input_buffer()
    start = time.monotonic()

    def report():
        for ptype, payload in reader.feed(ser.read(ser.in_waiting)):
            left, right, good, bad = struct.unpack("<hhBB", payload)
            print(f"{(time.monotonic() - start) * 1000:7.1f} ms  status: left {left:4d} right {right:4d}  good {good} bad {bad}")

    for left, right in plan:                     # one command every 100 ms
        ser.write(motor(left, right))
        print(f"{(time.monotonic() - start) * 1000:7.1f} ms  sent M {left:4d} {right:4d}")
        time.sleep(0.1)
        report()
    print("... the Pi stops sending (as if its program had crashed) ...")
    for _ in range(8):
        time.sleep(0.1)
        report()
