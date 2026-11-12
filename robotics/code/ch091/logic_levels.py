# logic_levels.py - can this output safely talk to that input? Logic levels, noise margins and damage
FAMILIES = {
    # name: (supply, V_OH min, V_OL max, V_IH min, V_IL max, absolute max input)
    "5 V Arduino Uno": (5.0, 4.2, 0.9, 3.0, 1.5, 5.5),
    "3.3 V ESP32 / Pi": (3.3, 2.9, 0.4, 2.5, 0.8, 3.6),
    "1.8 V sensor": (1.8, 1.4, 0.4, 1.2, 0.6, 2.1),
}


def check(driver, receiver):
    d = FAMILIES[driver]
    r = FAMILIES[receiver]
    v_oh, v_ol = d[1], d[2]
    v_ih, v_il, v_max = r[3], r[4], r[5]
    if d[0] > v_max:
        return "DAMAGE: the high level is above the input's absolute maximum"
    nm_high = v_oh - v_ih             # how much noise a HIGH can take before it might be misread
    nm_low = v_il - v_ol              # how much noise a LOW can take
    if nm_high < 0:
        return f"NO: a high ({v_oh} V) may not reach the input's {v_ih} V threshold"
    if nm_low < 0:
        return "NO: a low is not low enough"
    return f"ok (noise margins: high {nm_high:.1f} V, low {nm_low:.1f} V)"


for name, (vdd, voh, vol, vih, vil, vmax) in FAMILIES.items():
    print(f"{name:18s} outputs: high >= {voh} V, low <= {vol} V;  reads: high >= {vih} V, low <= {vil} V")
print()
for drv in FAMILIES:
    for rcv in FAMILIES:
        if drv != rcv:
            print(f"{drv:18s} -> {rcv:18s}: {check(drv, rcv)}")
