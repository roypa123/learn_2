# bits.py - the bit operators on one 8-bit register, step by step, the way Chapter 106's sketches use them
# (Python has the same operators as C++: | & ~ ^ << >>)
def show(code, value):
    print(f"{code:<38s} {value & 0xFF:08b}  ({value & 0xFF})")


reg = 0b00000011                          # TCCR1B as the Arduino core leaves it: prescaler 64
show("start", reg)
reg = 0
show("reg = 0", reg)
reg |= (1 << 3)                           # set bit 3 (WGM12: CTC mode)
show("reg |= (1 << 3)", reg)
reg |= (1 << 1) | (1 << 0)                # set bits 1 and 0 together (CS11, CS10: prescaler 64)
show("reg |= (1 << 1) | (1 << 0)", reg)
print(f"{'is bit 3 set?  reg & (1 << 3)':<38s} {'yes' if reg & (1 << 3) else 'no'}")
reg &= ~(1 << 3)                          # clear bit 3 (~ turns every 0 into 1 and every 1 into 0)
show("reg &= ~(1 << 3)", reg)
print(f"{'is bit 3 set?  reg & (1 << 3)':<38s} {'yes' if reg & (1 << 3) else 'no'}")
reg ^= (1 << 5)                           # toggle bit 5
show("reg ^= (1 << 5)", reg)
reg ^= (1 << 5)                           # toggle it again
show("reg ^= (1 << 5)", reg)
show("reg & 0b00000111   (keep bits 0-2)", reg & 0b00000111)
reg = (reg & 0b11111000) | 0b001          # change only bits 0-2: prescaler 1
show("reg = (reg & 0b11111000) | 0b001", reg)
