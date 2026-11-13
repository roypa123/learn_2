# nmea.py - check and read a GPS module's NMEA sentences, the text a GPS sends over its UART at 9600 baud
# A sentence: $ ... * two hex digits. The digits are the XOR of every character between $ and *.
def checksum_ok(line):
    if not line.startswith("$") or "*" not in line:
        return False
    body, given = line[1:].split("*", 1)
    x = 0
    for ch in body:
        x ^= ord(ch)                              # XOR (Chapter 106): each bit flips when a character has a 1 there
    return f"{x:02X}" == given.strip().upper()


def degrees(value, hemisphere):
    """NMEA gives ddmm.mmmm (degrees and minutes); turn it into decimal degrees."""
    dot = value.index(".")
    d = float(value[:dot - 2])
    m = float(value[dot - 2:])
    sign = -1 if hemisphere in "SW" else 1
    return sign * (d + m / 60)


def read_gga(line):
    f = line.split("*")[0].split(",")
    return {"time": f[1], "lat": degrees(f[2], f[3]), "lon": degrees(f[4], f[5]),
            "fix": int(f[6]), "satellites": int(f[7]), "altitude_m": float(f[9])}


lines = [
    "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47",
    "$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47".replace("4807", "4817"),
    "$GPGGA,123520,4807.0",                       # cut short: the rest was lost
]
for line in lines:
    if checksum_ok(line):
        g = read_gga(line)
        print(f"OK   {g['time']}: {g['lat']:.5f}, {g['lon']:.5f}, fix {g['fix']}, "
              f"{g['satellites']} satellites, {g['altitude_m']} m")
    else:
        print(f"BAD  ignored: {line[:40]}...")
