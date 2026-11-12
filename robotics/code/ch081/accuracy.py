# accuracy.py - what does '+/-(0.5% + 2 digits)' mean on a 2000-count meter?
RANGES = [0.2, 2.0, 20.0, 200.0]        # the DC volt ranges of a cheap 2000-count meter (full scale 1999 counts)
PERCENT = 0.005                          # 0.5% of the reading
DIGITS = 2                               # plus 2 counts of the last digit


def measure(true_v, full_scale):
    step = full_scale / 2000             # one count: the smallest change the display can show
    if true_v >= full_scale:
        return None, None, step          # the display shows '1' or 'OL': over the range
    shown = round(true_v / step) * step
    error = PERCENT * true_v + DIGITS * step
    return shown, error, step


for true_v in [1.234, 7.2, 16.8]:
    print(f"true voltage {true_v} V:")
    for fs in RANGES:
        shown, err, step = measure(true_v, fs)
        if shown is None:
            print(f"  {fs:6.1f} V range: OL (over the range)")
        else:
            print(f"  {fs:6.1f} V range: shows {shown:.4g} V, step {step * 1000:g} mV, could be off by +/-{err * 1000:.1f} mV ({err / true_v:.2%})")
print()
print("choose the smallest range that does not overflow: it gives the finest step and the smallest error")
