# truth_table.py - check a rule for all four cases of two True/False values
print("  a       b      a and b  a or b   not a")

a, b = True, True
print(f"{a!s:<7} {b!s:<7} {a and b!s:<8} {a or b!s:<8} {not a!s}")

a, b = True, False
print(f"{a!s:<7} {b!s:<7} {a and b!s:<8} {a or b!s:<8} {not a!s}")

a, b = False, True
print(f"{a!s:<7} {b!s:<7} {a and b!s:<8} {a or b!s:<8} {not a!s}")

a, b = False, False
print(f"{a!s:<7} {b!s:<7} {a and b!s:<8} {a or b!s:<8} {not a!s}")
