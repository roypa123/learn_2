# spi_ring.py - SPI is two 8-bit shift registers joined in a ring: at each clock pulse, each side
# sends its top bit to the other and takes the other's top bit in at its bottom.
# After 8 pulses the two bytes have swapped places: data goes both ways at the same time.
controller = 0xA5                                 # the byte the Uno sends   (10100101)
target = 0x3C                                     # the byte the chip sends  (00111100)
print(f"clock  controller  target")
print(f"start  {controller:08b}    {target:08b}")
for pulse in range(1, 9):
    out_c = (controller >> 7) & 1                 # on MOSI: the controller's highest bit
    out_t = (target >> 7) & 1                     # on MISO: the target's highest bit
    controller = ((controller << 1) & 0xFF) | out_t
    target = ((target << 1) & 0xFF) | out_c
    print(f"{pulse:5d}  {controller:08b}    {target:08b}")
print(f"the controller now holds 0x{controller:02X}, the target 0x{target:02X}")
