# solve_3x3.py - three equations, three unknowns, by elimination (then compare with NumPy)
import numpy as np


def solve_3x3(rows):
    m = [list(row) for row in rows]          # each row: [a, b, c, right side]
    n = 3
    for col in range(n):
        best = max(range(col, n), key=lambda r: abs(m[r][col]))
        m[col], m[best] = m[best], m[col]
        if m[col][col] == 0:
            return None
        for r in range(col + 1, n):
            factor = m[r][col] / m[col][col]
            for k in range(col, n + 1):
                m[r][k] = m[r][k] - factor * m[col][k]
    answer = [0.0] * n
    for r in range(n - 1, -1, -1):
        known = sum(m[r][k] * answer[k] for k in range(r + 1, n))
        answer[r] = (m[r][n] - known) / m[r][r]
    return answer


if __name__ == "__main__":
    rows = [[1, 1, 1, 6],
            [2, -1, 1, 3],
            [1, 2, -1, 2]]
    print("by hand :", solve_3x3(rows))
    a = np.array([r[:3] for r in rows], dtype=float)
    b = np.array([r[3] for r in rows], dtype=float)
    print("by NumPy:", np.linalg.solve(a, b))
