# balance.py - which x makes 3x + 2 equal to 14?
def left_side(x):
    return 3 * x + 2


RIGHT_SIDE = 14

for x in range(0, 8):
    value = left_side(x)
    if value < RIGHT_SIDE:
        result = "left side too light"
    elif value > RIGHT_SIDE:
        result = "left side too heavy"
    else:
        result = "balanced"
    print(f"x = {x}:  3x + 2 = {value:2d}   {result}")
