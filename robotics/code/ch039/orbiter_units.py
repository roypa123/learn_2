# orbiter_units.py - a number that knows its unit, and refuses a wrong sum
LBF_S_TO_N_S = 4.448


class Quantity:
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit

    def __add__(self, other):
        if self.unit != other.unit:
            raise ValueError(f"cannot add {self.unit} to {other.unit}")
        return Quantity(self.value + other.value, self.unit)

    def __str__(self):
        return f"{self.value:.1f} {self.unit}"


firings_lbf_s = [12.0, 11.5, 12.5, 13.0]     # invented numbers for this example

total_number = sum(firings_lbf_s)
true_n_s = total_number * LBF_S_TO_N_S

print(f"number in the file      : {total_number:.1f}")
print(f"used as if in N s       : {total_number:.1f} N s")
print(f"what really happened    : {true_n_s:.1f} N s")
print(f"the effect was too small by a factor of {true_n_s / total_number:.3f}")

ground = Quantity(49.0, "N s")
spacecraft = Quantity(12.0, "lbf s")
print("same units:", ground + Quantity(1.0, "N s"))
try:
    print(ground + spacecraft)
except ValueError as error:
    print("refused:", error)
