# c_rating.py - what does '5000 mAh 25C' promise? Current limit, sag and heat for a drone pack
from lipo_model import ocv

CAPACITY_AH = 5.0
C_RATING = 25
CELLS = 4
R_CELL = 0.005            # 5 milliohms per cell when new

max_a = CAPACITY_AH * C_RATING
r_pack = CELLS * R_CELL
print(f"{CAPACITY_AH * 1000:.0f} mAh, {C_RATING}C: up to {max_a:.0f} A continuous; pack resistance {r_pack * 1000:.0f} milliohms")
print(f"{'situation':22s} {'amps':>6s} {'C':>6s} {'pack voltage':>13s} {'sag':>7s} {'heat in pack':>13s}")
for name, amps in [("hover", 25), ("climbing", 60), ("full throttle", 120), ("short burst", 150)]:
    v = CELLS * ocv(0.5) - amps * r_pack            # half-charged pack under load
    heat = amps ** 2 * r_pack
    flag = "  (over the rating!)" if amps > max_a else ""
    print(f"{name:22s} {amps:6d} {amps / CAPACITY_AH:5.0f}C {v:10.2f} V {amps * r_pack:5.2f} V {heat:10.0f} W{flag}")
print()
print("hover time from the C rate: 1 / 5C = 0.2 h = 12 min for the whole pack; with the 80% rule, about 9.6 min")
