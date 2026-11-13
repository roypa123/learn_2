# baud_error.py - which baud rates can a 16 MHz Uno make exactly?
# The UART divides the clock by 16 x (UBRR + 1), or by 8 x (UBRR + 1) in "double speed" mode (U2X),
# and UBRR must be a whole number, so most baud rates come out slightly wrong.
CLOCK = 16_000_000


def actual(baud, divider):
    ubrr = round(CLOCK / (divider * baud)) - 1
    real = CLOCK / (divider * (ubrr + 1))
    return ubrr, real, (real - baud) / baud * 100


print(f"{'baud':>8s} | {'normal: UBRR, real, error':>28s} | {'double speed: UBRR, real, error':>32s}")
for baud in [9600, 19200, 57600, 115200, 250000, 500000, 1000000]:
    n = actual(baud, 16)
    d = actual(baud, 8)
    print(f"{baud:8d} | {n[0]:4d}, {n[1]:9.0f}, {n[2]:+5.1f} %   | {d[0]:4d}, {d[1]:9.0f}, {d[2]:+5.1f} %")
