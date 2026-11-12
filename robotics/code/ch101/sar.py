# sar.py - how the Uno's ADC finds the number for a voltage: 10 guesses, one bit at a time
V_IN = 3.10                     # the voltage on the pin
V_REF = 5.0                     # the ADC's reference: the voltage that would give 1024
BITS = 10

count = 0
for bit in range(BITS - 1, -1, -1):          # from the biggest bit (512) down to the smallest (1)
    trial = count + 2 ** bit                 # try switching this bit on
    trial_v = trial * V_REF / 2 ** BITS      # the voltage that trial number stands for
    keep = V_IN >= trial_v                   # the comparator: is the input at least that big?
    if keep:
        count = trial
    print(f"bit {bit}: try {trial:4d} = {trial_v:.4f} V -> {'keep' if keep else 'too big'}   count = {count}")
print(f"result: {count}, which means {count * V_REF / 2 ** BITS:.4f} V (one step = {V_REF / 2 ** BITS * 1000:.2f} mV)")
