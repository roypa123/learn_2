# bus_compare.py - time on the wires to read an IMU's 14 measurement bytes, I2C against SPI
# I2C: write (address + register) then read (address + 14 bytes), 9 clocks per byte, + start/stop (Chapter 108)
# SPI: 1 register byte + 14 data bytes, 8 clocks per byte, no address and no acknowledge bits
i2c_bits = (1 + 9 * 2 + 1) + (1 + 9 * 15 + 1)
spi_bits = 8 * 15
print(f"{'bus and clock':<16s} {'clock bits':>10s} {'time on the wires':>18s} {'readings per second, at most':>30s}")
for name, bits, hz in [("I2C 100 kHz", i2c_bits, 100e3), ("I2C 400 kHz", i2c_bits, 400e3),
                       ("SPI 1 MHz", spi_bits, 1e6), ("SPI 8 MHz", spi_bits, 8e6), ("SPI 20 MHz", spi_bits, 20e6)]:
    t = bits / hz
    print(f"{name:<16s} {bits:10d} {t * 1e6:15.1f} us {int(1 / t):30d}")
