# sequences.py - arithmetic and geometric sequences: terms and sums, by loop and by formula
a, d, n = 2, 3, 10              # arithmetic: start 2, add 3 each time, 10 terms
terms = [a + k * d for k in range(n)]
print("arithmetic terms:", terms)
print("  sum by loop   :", sum(terms))
print("  sum by formula:", n * (2 * a + (n - 1) * d) // 2)

a, r, n = 1, 0.5, 10            # geometric: start 1, multiply by 0.5 each time
terms = [a * r ** k for k in range(n)]
print("geometric terms :", [round(t, 4) for t in terms])
print("  sum by loop   :", sum(terms))
print("  sum by formula:", a * (1 - r ** n) / (1 - r))
print("  if it never ended, the sum would be", a / (1 - r))
