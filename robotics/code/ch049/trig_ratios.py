# trig_ratios.py - the ratios of a right-angled triangle depend only on its angle
import math

print("A 30-degree triangle drawn at three sizes:")
for hyp in [1.0, 2.5, 10.0]:
    opp = hyp * math.sin(math.radians(30))
    adj = hyp * math.cos(math.radians(30))
    print(f"  hyp {hyp:5.1f}  opp {opp:6.3f}  adj {adj:6.3f}   "
          f"opp/hyp {opp / hyp:.3f}  adj/hyp {adj / hyp:.3f}  opp/adj {opp / adj:.3f}")

print()
print("angle    sin      cos      tan")
for deg in [0, 30, 45, 60, 89, 90]:
    r = math.radians(deg)
    tan_text = "too big" if deg == 90 else f"{math.tan(r):8.3f}"
    print(f"{deg:5d} {math.sin(r):8.3f} {math.cos(r):8.3f} {tan_text:>8}")
