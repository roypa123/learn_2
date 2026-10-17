# Chapter 21 — Lines, Part 2: Bresenham's Algorithm

> **Part 4 · Chapter 21 of 82**
> **You need:** Chapters 1–20 · **You will make:** Bresenham lines in `lines.h` (with thick and dashed lines), `fan_bresenham.ppm` and `styles.ppm`

---

## What you will learn

- The key idea of Bresenham's algorithm: at each step, make a **yes/no decision**.
- How to keep track of the **error**: how far the true line is from the pixel we chose.
- How to turn all the fractions into **whole numbers**, by multiplying by **2 × dx**.
- A full, worked table of the algorithm for a real line.
- The **general version** that works in **all eight directions** with one loop.
- What happens at **ties** (exactly halfway), and why different methods can choose differently.
- How to **skip the last pixel**, so joined lines do not draw corners twice.
- How to draw **thick** lines and **dashed** lines.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **algorithm** | A list of exact steps that solves a problem. (First met in Chapter 1.) |
| **decision** | A choice between two options, made with one test. |
| **error** (in drawing) | How far the true line is from the pixel we actually drew. |
| **error term** | A number that the algorithm keeps updated to remember the error. |
| **integer** | A whole number: …, −2, −1, 0, 1, 2, … (an `int` in C++). |
| **floating-point** | A number with a fractional part, like 0.4 (a `double` in C++). |
| **octant** | One of the 8 "directions" a line can go in, each covering 45°. |
| **tie** | A case where both choices are exactly equally good. |
| **brush** | The small shape we stamp at every point of a line to give it thickness. |
| **dash** | One visible piece of a dashed line. |

---

## 21.1 Why another line algorithm?

DDA (Chapter 20) gives good lines. But look at what it does for **every** pixel:

| Work per pixel | DDA |
|---|---|
| multiplications | 2 (`xStep * i`, `yStep * i`) |
| additions | 4 (two in the formula, two inside the rounding) |
| `std::floor` calls | 2 |
| conversions from `double` to `int` | 2 |

📖 **New word: integer** — a whole number.

📖 **New word: floating-point** — a number with a fractional part.

In 1962, **Jack Bresenham**, an engineer at IBM, needed to drive a pen plotter — a machine that draws on paper with a pen moved by motors. The computers of that time were very slow at floating-point maths. He found a way to draw exactly the same kind of line using only:

- **integer additions and subtractions**, and
- **one comparison** per pixel.

No multiplications in the loop, no fractions, no rounding. His method is still one of the most famous algorithms in computer graphics, and it is still used today in many places (for example, in printers and in simple graphics chips).

Even on today's fast computers, it is worth learning: the idea of **"keep a running error and make a small decision each step"** comes back in circles (Chapter 22), ellipses (Chapter 23), and dithering (Chapter 52).

---

## 21.2 The decision

To keep things simple, we first look at **one kind** of line:

> going **right** (x1 > x0) and **down** (y1 ≥ y0), and **shallow**: 0 ≤ slope ≤ 1

(Section 21.5 handles all the other directions.)

For a shallow line, we draw one pixel in **every column** (Chapter 20). As we go from one column to the next, the true line goes down by `slope`, which is **less than 1**. So from one column to the next, there are only **two** possible choices for the row:

```
 column x        column x + 1

   ■ ─────────── ? stay in the same row (y)
                 
                 ? or move down one row (y + 1)
```

📖 **New word: decision** — a choice between two options, made with one test.

So the **whole** algorithm is a sequence of tiny yes/no decisions: "**down or not?**". The only question is how to decide.

---

## 21.3 Keeping track of the error

📖 **New word: error** (in drawing) — how far the true line is from the row we drew.

Think about the true line's y in each column, and the row we drew. Let **e** be the difference:

> e = (true y) − (row we drew)

At the start, we are exactly on the line: **e = 0**.

Each step to the right, the true line goes down by `slope`, so **e grows by slope**.

When should we move down a row? When the true line is **closer to the next row** than to the current row — that is, when **e > 0.5**. After moving down a row, the row we drew is 1 bigger, so **e shrinks by 1**.

🔢 **Maths: the line from (0, 0) to (5, 2)**, slope = 0.4

| column x | row drawn | e (before moving to next column) | then: e + 0.4 | e > 0.5? | next row |
|---|---|---|---|---|---|
| 0 | 0 | 0.0 | 0.4 | no | 0 |
| 1 | 0 | 0.4 | 0.8 | **yes** → e = 0.8 − 1 = −0.2 | 1 |
| 2 | 1 | −0.2 | 0.2 | no | 1 |
| 3 | 1 | 0.2 | 0.6 | **yes** → e = 0.6 − 1 = −0.4 | 2 |
| 4 | 2 | −0.4 | 0.0 | no | 2 |
| 5 | 2 | 0.0 | | | |

Pixels: (0, 0), (1, 0), (2, 1), (3, 1), (4, 2), (5, 2) — **exactly** the same as DDA (Chapter 20, Section 20.4).

Check the meaning: in column 2, the true y is 0.8 and we drew row 1, so e = 0.8 − 1 = −0.2 ✓. In column 3, the true y is 1.2 and we drew row 1, so e = 0.2 ✓.

### A cleaner test

Comparing with 0.5 is a little awkward. Let us **shift** the error by 0.5 and call it **e′**:

> e′ = e − 0.5

Then:
- the start is **e′ = −0.5**,
- the test "e > 0.5" becomes "**e′ > 0**",
- each step: **e′ += slope**,
- after moving down: **e′ −= 1**.

The test "is it bigger than zero?" is the simplest test there is. We still have fractions (slope = 0.4, start −0.5). The next section removes them.

---

## 21.4 Removing the fractions

📖 **New word: error term** — the number the algorithm keeps updated to remember the error.

All the fractions come from **slope = dy ÷ dx** and from the **0.5**. If we multiply **everything** by **2 × dx**, every fraction disappears:

| What | Before (× 1) | After (× 2·dx) |
|---|---|---|
| start | e′ = −0.5 | d = −0.5 × 2·dx = **−dx** |
| each step | e′ += dy ÷ dx | d += (dy ÷ dx) × 2·dx = **2·dy** |
| after moving down | e′ −= 1 | d −= 1 × 2·dx = **2·dx** |
| test | e′ > 0 | **d > 0** |

Why can we multiply? Because 2·dx is a **positive** number (the line goes right, so dx > 0). Multiplying both sides of "e′ > 0" by a positive number does not change whether it is true. So **d > 0** gives exactly the same decisions as **e′ > 0**.

And now every number is an **integer**: dx and dy are whole numbers (the endpoints are pixels), so −dx, 2·dy and 2·dx are whole numbers too.

🧠 **Remember — Bresenham for shallow lines going right and down:**

```
d = −dx
y = y0
for x = x0 … x1:
    plot (x, y)
    d = d + 2·dy
    if d > 0:
        y = y + 1
        d = d − 2·dx
```

🔢 **Maths: the line from (0, 0) to (5, 2) with whole numbers**

> dx = 5, dy = 2 → start d = −5, step +4, move −10

| x | plot | d + 4 | d > 0? | then d | y for the next column |
|---|---|---|---|---|---|
| 0 | (0, 0) | −5 + 4 = −1 | no | −1 | 0 |
| 1 | (1, 0) | −1 + 4 = 3 | **yes** | 3 − 10 = −7 | 1 |
| 2 | (2, 1) | −7 + 4 = −3 | no | −3 | 1 |
| 3 | (3, 1) | −3 + 4 = 1 | **yes** | 1 − 10 = −9 | 2 |
| 4 | (4, 2) | −9 + 4 = −5 | no | −5 | 2 |
| 5 | (5, 2) | (the line ends here) | | | |

The same pixels as Section 21.3. And look: every d is exactly **10 × e′** (10 = 2·dx). For example, in column 1, e′ was 0.8 − 0.5 = 0.3, and d = 3 ✓.

Per pixel, the work is now: one addition (`d + 2·dy`), one comparison (`d > 0`), and sometimes one subtraction and one `y + 1`. No `double`, no rounding. (`2·dy` and `2·dx` are computed once; in the loop they are just numbers.)

---

## 21.5 All directions with one loop

📖 **New word: octant** — one of the 8 "directions" a line can go in.

The version above only works for 1 of 8 kinds of line:

```
            steep, up-left │ steep, up-right
                     ╲     │     ╱
        shallow,       ╲   │   ╱      shallow,
        up-left          ╲ │ ╱        up-right
       ─────────────────── ● ───────────────────
        shallow,         ╱ │ ╲        shallow,
        down-left      ╱   │   ╲      down-right  ← Section 21.4
                     ╱     │     ╲
          steep, down-left │ steep, down-right
```

We could write 8 loops, or swap x and y for steep lines and swap the endpoints for lines going left. But there is a neater version that handles **all eight** at once. It is the one most programmers use, and it is our `drawLine`:

```
dx  =  |x1 − x0|          (always ≥ 0)
dy  = −|y1 − y0|          (always ≤ 0 — note the minus!)
sx  = +1 if x0 < x1, else −1     (which way to step in x)
sy  = +1 if y0 < y1, else −1     (which way to step in y)
err = dx + dy

repeat until we reach (x1, y1):
    plot (x0, y0)
    e2 = 2 · err
    if e2 ≥ dy:  err += dy, x0 += sx      (a step in x is good)
    if e2 ≤ dx:  err += dx, y0 += sy      (a step in y is good)
plot (x1, y1)
```

How to understand it:

- **sx** and **sy** take care of the direction: left or right, up or down. Everything else works with **distances** (dx, and −dy, which are never negative), so the maths is the same in every direction.
- **err** is the same kind of error term as d, but it watches **both** directions at once. It measures how far the **diagonal** neighbour is from the true line (scaled to whole numbers, like d).
- Each round makes **two** small decisions: "should I step in x?" and "should I step in y?". If **both** are yes, we step **diagonally**. A shallow line mostly says yes to x and only sometimes to y. A steep line mostly says yes to y and only sometimes to x.
- Each step adds `dy` (a negative number) when we move in x, and `dx` (a positive number) when we move in y. These keep err balanced near zero, just like `+ 2·dy` and `− 2·dx` kept d balanced in Section 21.4.

🔢 **Maths: drawLine from (0, 0) to (2, 6)** (a steep line)

> dx = 2, dy = −6, sx = +1, sy = +1, err = 2 + (−6) = −4

| plot | e2 = 2·err | e2 ≥ −6? (step x) | e2 ≤ 2? (step y) | new err | next point |
|---|---|---|---|---|---|
| (0, 0) | −8 | no | yes: err + 2 | −2 | (0, 1) |
| (0, 1) | −4 | yes: err − 6 = −8 | yes: −8 + 2 | −6 | (1, 2) |
| (1, 2) | −12 | no | yes | −4 | (1, 3) |
| (1, 3) | −8 | no | yes | −2 | (1, 4) |
| (1, 4) | −4 | yes: −8 | yes: −6 | −6 | (2, 5) |
| (2, 5) | −12 | no | yes | −4 | (2, 6) |
| (2, 6) | — end — | | | | |

Pixels: (0, 0), (0, 1), (1, 2), (1, 3), (1, 4), (2, 5), (2, 6) — **the same** 7 pixels as DDA in Chapter 20, Section 20.6.

Notice that **e2 ≤ dx** was true in every round: a steep line steps in y every time, and only sometimes also in x.

🔢 **Maths: drawLine from (0, 0) to (5, 2)** (the shallow line again)

> dx = 5, dy = −2, err = 3

| plot | e2 | step x? (e2 ≥ −2) | step y? (e2 ≤ 5) | new err |
|---|---|---|---|---|
| (0, 0) | 6 | yes: 3 − 2 = 1 | no | 1 |
| (1, 0) | 2 | yes: −1 | yes: −1 + 5 = 4 | 4 |
| (2, 1) | 8 | yes: 2 | no | 2 |
| (3, 1) | 4 | yes: 0 | yes: 5 | 5 |
| (4, 2) | 10 | yes: 3 | no | 3 |
| (5, 2) | — end — | | | |

The same pixels again. Here **e2 ≥ dy** was always true: a shallow line steps in x every time.

🧠 **Remember:** The general Bresenham uses **dx = |Δx|**, **dy = −|Δy|**, step signs **sx, sy**, and **err = dx + dy**. Each round: **e2 = 2·err**; if e2 ≥ dy step x; if e2 ≤ dx step y.

---

## 21.6 Ties

📖 **New word: tie** — a case where both choices are exactly equally good.

Look at the line from (0, 0) to (2, 1). Its slope is 0.5. In column 1, the true y is **exactly 0.5** — exactly halfway between row 0 and row 1. Neither row is closer. Which one should we choose?

| Method | Rule at a tie | Pixel in column 1 |
|---|---|---|
| DDA (Chapter 20) | rounds 0.5 **up**: floor(0.5 + 0.5) = 1 | (1, **1**) |
| shallow Bresenham (Section 21.4) | moves down only when d **> 0**; at a tie d = 0 | (1, **0**) |
| general Bresenham (`drawLine`) | at a tie both tests are true → diagonal step | (1, **1**) |

🔢 **Maths: the shallow version at the tie**

> dx = 2, dy = 1 → d = −2
> x = 0: plot (0, 0); d = −2 + 2 = 0; 0 > 0? **no** → stay in row 0
> x = 1: plot (1, **0**); d = 0 + 2 = 2 > 0 → row 1, d = 2 − 4 = −2
> x = 2: plot (2, 1)

All three answers are **correct**. A tie has no "right" answer. But it explains two things you may notice:

1. Different programs can draw the same line with **slightly different** pixels.
2. Drawing a line **from A to B** and **from B to A** can give slightly different pixels at the ties, because "round up" means a different thing in the other direction.

If you need lines that are **exactly** the same in both directions (for example, when you draw over a line again to erase it), always draw from the endpoint with the smaller y (or smaller x) first.

---

## 21.7 Skipping the last pixel

In Chapter 20 (Section 20.6), we saw that joined lines draw their shared corner **twice**. With solid colours it does not matter. With alpha, or with the "invert" drawing mode some programs use, the corner looks wrong.

The fix is simple: give `drawLine` an option to **not** draw its last pixel:

```cpp
drawLine(image, x0, y0, x1, y1, colour, false);   // false = do not plot (x1, y1)
```

Then a closed shape made of n lines, each skipping its last pixel, draws **every corner exactly once**: each corner is the **first** pixel of the next line.

🔢 **Maths: a square outline of side 60**

> 4 lines, each with 61 pixels (60 + 1, Chapter 20)
> with the last pixel: 4 × 61 = 244 pixels drawn, but only 240 different pixels (4 corners drawn twice)
> without the last pixel: 4 × 60 = **240** pixels drawn — each one once ✓

In C++ we do this with a **default argument**: `bool includeLast = true`. If you leave the argument out, it is `true` and the line is drawn as usual.

---

## 21.8 Thick lines

📖 **New word: brush** — the small shape we stamp at every point of a line.

A Bresenham line is always **1 pixel wide**. To make a thicker line, a simple method is: at every point of the line, draw a small **square** (a brush) instead of a single pixel.

```
a 1-pixel line:   ■■■            with a 3 × 3 brush:   ■■■■■
                     ■■■                               ■■■■■■■■
                        ■■■                            ■■■■■■■■■■■
                                                          ■■■■■■■■■
                                                             ■■■■■
```

For a brush of width w, the square around point (x, y) starts at (x − r, y − r) with r = w ÷ 2:

🔢 **Maths: a brush of width 5 at (100, 40)**

> r = 5 ÷ 2 = 2 (integer division)
> square = makeRect(100 − 2, 40 − 2, 5, 5) = [98, 103) × [38, 43)
> it covers x = 98, 99, **100**, 101, 102 — centred on 100 ✓

To stamp a square at every point, we first need the **list** of points. So we add a function `linePoints` that runs the same Bresenham loop, but **stores** each point in a `std::vector<Point>` instead of plotting it. Then `drawThickLine` loops over the points and calls `fillRect` (Chapter 19) for each.

⚠️ **Careful:** This simple method has two weaknesses:
- Neighbouring squares **overlap** a lot, so many pixels are painted many times. With solid colours it does not matter. With alpha it would.
- A **diagonal** line comes out a little **thicker** than a horizontal one with the same brush, because a square is wider across its diagonal (√2 ≈ 1.41 times wider, Chapter 3).

Better thick lines are drawn as **filled shapes** (a long, thin rectangle turned to the line's direction). We can do that after we learn triangles (Chapter 24) and rotation (Chapter 31).

---

## 21.9 Dashed lines

📖 **New word: dash** — one visible piece of a dashed line.

A dashed line draws some points and skips others. With the list of points, this is easy: count the points, and draw a point only if it falls in the "dash" part of the pattern.

🔢 **Maths: dashes of 10 and gaps of 6**

> pattern length = 10 + 6 = 16
> point i is drawn if **i % 16 < 10**
> i = 0–9: drawn (9 % 16 = 9 < 10)
> i = 10–15: skipped (10 % 16 = 10, not < 10)
> i = 16–25: drawn again (16 % 16 = 0 < 10)

We count **points**, not distance. So, like thick lines, dashes on a diagonal line look slightly **longer** than on a horizontal one (diagonal points are 1.41 pixels apart, Chapter 20, Example 4).

⚠️ If `dash + gap` is 0, `i % 0` would be a division by zero, which crashes the program. Our function checks `dash <= 0` first and simply draws nothing.

---

## Code, part 1: the new part of `lines.h`

Add this code at the **end** of `common/lines.h`, after `drawLineDDA` and **before** `#endif`. The line numbers are the real ones in the finished file.

```cpp
#include <vector>

struct Point {
    int x = 0;
    int y = 0;
};

inline void drawLineShallow(Image& image, int x0, int y0, int x1, int y1, Colour c) {
    int dx = x1 - x0;
    int dy = y1 - y0;
    int d = -dx;
    int y = y0;
    for (int x = x0; x <= x1; ++x) {
        image.setPixel(x, y, c);
        d += 2 * dy;
        if (d > 0) {
            y += 1;
            d -= 2 * dx;
        }
    }
}

inline void drawLine(Image& image, int x0, int y0, int x1, int y1, Colour c,
                     bool includeLast = true) {
    int dx = std::abs(x1 - x0);
    int dy = -std::abs(y1 - y0);
    int sx = (x0 < x1) ? 1 : -1;
    int sy = (y0 < y1) ? 1 : -1;
    int err = dx + dy;
    while (x0 != x1 || y0 != y1) {
        image.setPixel(x0, y0, c);
        int e2 = 2 * err;
        if (e2 >= dy) {
            err += dy;
            x0 += sx;
        }
        if (e2 <= dx) {
            err += dx;
            y0 += sy;
        }
    }
    if (includeLast) {
        image.setPixel(x1, y1, c);
    }
}

inline std::vector<Point> linePoints(int x0, int y0, int x1, int y1) {
    std::vector<Point> points;
    int dx = std::abs(x1 - x0);
    int dy = -std::abs(y1 - y0);
    int sx = (x0 < x1) ? 1 : -1;
    int sy = (y0 < y1) ? 1 : -1;
    int err = dx + dy;
    while (x0 != x1 || y0 != y1) {
        points.push_back(Point{x0, y0});
        int e2 = 2 * err;
        if (e2 >= dy) {
            err += dy;
            x0 += sx;
        }
        if (e2 <= dx) {
            err += dx;
            y0 += sy;
        }
    }
    points.push_back(Point{x1, y1});
    return points;
}

inline void drawThickLine(Image& image, int x0, int y0, int x1, int y1, int width, Colour c) {
    int r = width / 2;
    for (const Point& p : linePoints(x0, y0, x1, y1)) {
        fillRect(image, makeRect(p.x - r, p.y - r, width, width), c);
    }
}

inline void drawDashedLine(Image& image, int x0, int y0, int x1, int y1,
                           int dash, int gap, Colour c) {
    if (dash <= 0 || gap < 0) {
        return;
    }
    std::vector<Point> points = linePoints(x0, y0, x1, y1);
    for (int i = 0; i < static_cast<int>(points.size()); ++i) {
        if (i % (dash + gap) < dash) {
            image.setPixel(points[i].x, points[i].y, c);
        }
    }
}
```

### Line by line

**A point type, and the teaching version (lines 43–63)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 43 | `#include <vector>` | `std::vector`, for `linePoints`. We include it **here**, next to the new code, so the earlier line numbers of this file (Chapter 20) stay the same. An `#include` may appear anywhere outside a function. (`image.h` already includes `<vector>`, but a header should include what **it** uses.) |
| 45–48 | `struct Point { int x = 0; int y = 0; };` | A pixel position (x, y). |
| 50 | `inline void drawLineShallow(Image& image, int x0, int y0, int x1, int y1, Colour c) {` | The teaching version from Section 21.4. **Only** for lines going right and down with slope 0 to 1. |
| 51–52 | `int dx = x1 - x0;` / `int dy = y1 - y0;` | The run and the rise. For this kind of line, both are ≥ 0, and dy ≤ dx. |
| 53 | `int d = -dx;` | The error term, starting at −0.5 × 2·dx = −dx. |
| 54 | `int y = y0;` | The row we are drawing on. |
| 55 | `for (int x = x0; x <= x1; ++x) {` | One pixel per column, both endpoints included. |
| 56 | `image.setPixel(x, y, c);` | Plot the pixel. |
| 57 | `d += 2 * dy;` | The true line moved down by "slope" (here: 2·dy, in whole numbers). |
| 58–61 | `if (d > 0) { y += 1; d -= 2 * dx; }` | The decision: if the line is now closer to the next row, move down, and reduce the error by "one row" (2·dx). |
| 62–63 | `}` `}` | End. |

**The general version (lines 65–87)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 65–66 | `inline void drawLine(Image& image, int x0, int y0, int x1, int y1, Colour c, bool includeLast = true) {` | Bresenham for **every** direction (Section 21.5). `includeLast` has a **default** of `true`: you may leave it out. |
| 67 | `int dx = std::abs(x1 - x0);` | The distance across, never negative. |
| 68 | `int dy = -std::abs(y1 - y0);` | The distance down, made **negative** on purpose. This sign trick lets one formula (`err = dx + dy`) and two simple tests handle both shallow and steep lines. |
| 69 | `int sx = (x0 < x1) ? 1 : -1;` | Step right (+1) or left (−1). |
| 70 | `int sy = (y0 < y1) ? 1 : -1;` | Step down (+1) or up (−1). |
| 71 | `int err = dx + dy;` | The starting error term. |
| 72 | `while (x0 != x1 \|\| y0 != y1) {` | Keep going until we reach the end point. (We move `x0` and `y0` themselves: they are copies, so the caller's values are not changed.) |
| 73 | `image.setPixel(x0, y0, c);` | Plot the current point. |
| 74 | `int e2 = 2 * err;` | Twice the error, for the two tests. |
| 75–78 | `if (e2 >= dy) { err += dy; x0 += sx; }` | Is a step in x good? Then take it, and update the error (adding the negative dy). |
| 79–82 | `if (e2 <= dx) { err += dx; y0 += sy; }` | Is a step in y good? Then take it too. If both happened, it was a diagonal step. |
| 83 | `}` | End of the loop. We are now **at** (x1, y1), but have not plotted it yet. |
| 84–86 | `if (includeLast) { image.setPixel(x1, y1, c); }` | Plot the last point — unless asked not to (Section 21.7). |
| 87 | `}` | End. |

**A list of points (lines 89–110)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 89 | `inline std::vector<Point> linePoints(int x0, int y0, int x1, int y1) {` | The same algorithm as `drawLine`, but it **returns** the points instead of plotting them. |
| 90 | `std::vector<Point> points;` | Starts empty. |
| 91–95 | `int dx = ...; int dy = ...; int sx = ...; int sy = ...; int err = dx + dy;` | Exactly as in `drawLine`. |
| 96–107 | `while (...) { points.push_back(Point{x0, y0}); ... }` | The same loop, with `push_back` instead of `setPixel`. |
| 108 | `points.push_back(Point{x1, y1});` | Always add the last point. |
| 109–110 | `return points;` `}` | Give back the list. |

Why not let `drawLine` use `linePoints`? Because building a `std::vector` costs time and memory. `drawLine` is used for almost every line in the book, so it plots directly, as fast as possible. `linePoints` is for the special effects below, where we need the list.

**Thick and dashed lines (lines 112–130)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 112 | `inline void drawThickLine(Image& image, int x0, int y0, int x1, int y1, int width, Colour c) {` | A line drawn with a square brush (Section 21.8). |
| 113 | `int r = width / 2;` | How far the brush reaches to each side of the centre. |
| 114 | `for (const Point& p : linePoints(x0, y0, x1, y1)) {` | For each point of the line… |
| 115 | `fillRect(image, makeRect(p.x - r, p.y - r, width, width), c);` | …stamp a `width × width` square around it. `fillRect` clips it to the image (Chapter 19). |
| 116–117 | `}` `}` | End. |
| 119–120 | `inline void drawDashedLine(Image& image, int x0, int y0, int x1, int y1, int dash, int gap, Colour c) {` | A dashed line (Section 21.9). |
| 121–123 | `if (dash <= 0 \|\| gap < 0) { return; }` | Bad values: draw nothing, and never divide by zero. |
| 124 | `std::vector<Point> points = linePoints(x0, y0, x1, y1);` | Get the list of points. |
| 125 | `for (int i = 0; i < static_cast<int>(points.size()); ++i) {` | For each point, with its number `i`… |
| 126–128 | `if (i % (dash + gap) < dash) { image.setPixel(points[i].x, points[i].y, c); }` | …draw it only if it is inside a dash. |
| 129–130 | `}` `}` | End. |

`#endif` is now on line 132.

---

## Code, part 2: testing and using Bresenham

File: `ch21/bresenham.cpp`

```cpp
#include <iostream>
#include <string>
#include <vector>
#include "hsv.h"
#include "lines.h"

void printGrid(const std::string& title, const Image& img) {
    std::cout << title << ":\n";
    for (int y = 0; y < img.height(); ++y) {
        std::cout << "  ";
        for (int x = 0; x < img.width(); ++x) {
            Colour c = img.getPixel(x, y);
            bool on = c.r != 0 || c.g != 0 || c.b != 0;
            std::cout << (on ? '#' : '.');
        }
        std::cout << "\n";
    }
}

int main() {
    Image a(6, 3);
    drawLineShallow(a, 0, 0, 5, 2, colours::white);
    printGrid("shallow Bresenham (0, 0) to (5, 2)", a);

    Image b(3, 7);
    drawLine(b, 0, 0, 2, 6, colours::white);
    printGrid("drawLine (0, 0) to (2, 6)", b);

    Image tieDDA(3, 2);
    drawLineDDA(tieDDA, 0, 0, 2, 1, colours::white);
    printGrid("DDA (0, 0) to (2, 1)", tieDDA);

    Image tieShallow(3, 2);
    drawLineShallow(tieShallow, 0, 0, 2, 1, colours::white);
    printGrid("shallow Bresenham (0, 0) to (2, 1)", tieShallow);

    Image tieGeneral(3, 2);
    drawLine(tieGeneral, 0, 0, 2, 1, colours::white);
    printGrid("drawLine (0, 0) to (2, 1)", tieGeneral);

    std::vector<Point> pts = linePoints(10, 10, 70, 10);
    std::cout << "points on (10, 10) to (70, 10): " << pts.size() << "\n";

    Image fan(200, 200, colours::white);
    for (int i = 0; i < 200; i += 10) {
        Colour c = toColour(hsvToRgb(HSV{i * 1.8, 0.9, 0.8}));
        drawLine(fan, 100, 100, i, 0, c);
        drawLine(fan, 100, 100, 199, i, c);
        drawLine(fan, 100, 100, 199 - i, 199, c);
        drawLine(fan, 100, 100, 0, 199 - i, c);
    }

    Image styles(300, 200, colours::white);
    drawLine(styles, 20, 30, 280, 60, colours::black);
    drawThickLine(styles, 20, 80, 280, 110, 5, colours::blue);
    drawDashedLine(styles, 20, 130, 280, 160, 10, 6, colours::red);
    const int xs[5] = {40, 120, 200, 160, 60};
    const int ys[5] = {190, 170, 190, 140, 140};
    for (int i = 0; i < 5; ++i) {
        int j = (i + 1) % 5;
        drawLine(styles, xs[i], ys[i], xs[j], ys[j], Colour{0, 140, 0}, false);
    }

    bool ok = fan.savePPM("fan_bresenham.ppm");
    ok = ok && styles.savePPM("styles.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–3 | `#include <iostream>` / `<string>` / `<vector>` | Printing, titles, and the list of points. |
| 4–5 | `#include "hsv.h"` / `#include "lines.h"` | Hue colours for the fan (Chapter 16), and our line functions. |
| 7–18 | `void printGrid(const std::string& title, const Image& img) { ... }` | Print a title, then a tiny image as `#` and `.` (as in Chapter 20). |
| 20 | `int main() {` | The program starts here. |
| 21–23 | `Image a(6, 3); drawLineShallow(a, 0, 0, 5, 2, ...); printGrid(...);` | The table of Section 21.4, drawn. |
| 25–27 | `Image b(3, 7); drawLine(b, 0, 0, 2, 6, ...); printGrid(...);` | The steep table of Section 21.5. |
| 29–31 | `Image tieDDA(3, 2); drawLineDDA(...); printGrid(...);` | The tie line (Section 21.6) with DDA. |
| 33–35 | `Image tieShallow(3, 2); drawLineShallow(...); printGrid(...);` | …with the shallow Bresenham. |
| 37–39 | `Image tieGeneral(3, 2); drawLine(...); printGrid(...);` | …with the general Bresenham. |
| 41 | `std::vector<Point> pts = linePoints(10, 10, 70, 10);` | The list of points of a horizontal line 60 long. |
| 42 | `std::cout << "points on (10, 10) to (70, 10): " << pts.size() << "\n";` | Expect 61 (60 steps + 1). |
| 44–51 | `Image fan(...); for (...) { ... drawLine(...) × 4 ... }` | The Chapter 20 fan, now with Bresenham. |
| 53 | `Image styles(300, 200, colours::white);` | A picture of line styles. |
| 54 | `drawLine(styles, 20, 30, 280, 60, colours::black);` | A plain 1-pixel line. |
| 55 | `drawThickLine(styles, 20, 80, 280, 110, 5, colours::blue);` | The same direction, 5 pixels thick. |
| 56 | `drawDashedLine(styles, 20, 130, 280, 160, 10, 6, colours::red);` | Dashes of 10 points, gaps of 6. |
| 57–58 | `const int xs[5] = {...};` / `const int ys[5] = {...};` | The 5 corners of a closed shape (a polygon). |
| 59 | `for (int i = 0; i < 5; ++i) {` | For each corner… |
| 60 | `int j = (i + 1) % 5;` | …the **next** corner. For the last one (i = 4), `% 5` wraps back to corner 0, which closes the shape. |
| 61 | `drawLine(styles, xs[i], ys[i], xs[j], ys[j], Colour{0, 140, 0}, false);` | A green line, **without** its last pixel, so every corner is drawn exactly once (Section 21.7). |
| 62 | `}` | End of the polygon. |
| 64–69 | `bool ok = fan.savePPM(...); ... if (!ok) { ...; return 1; }` | Save both pictures. |
| 70 | `return 0;` | The program finished with no problem. |
| 71 | `}` | End of `main`. |

Compile:

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common bresenham.cpp -o bresenham
```

### What you should see

```
shallow Bresenham (0, 0) to (5, 2):
  ##....
  ..##..
  ....##
drawLine (0, 0) to (2, 6):
  #..
  #..
  .#.
  .#.
  .#.
  ..#
  ..#
DDA (0, 0) to (2, 1):
  #..
  .##
shallow Bresenham (0, 0) to (2, 1):
  ##.
  ..#
drawLine (0, 0) to (2, 1):
  #..
  .##
points on (10, 10) to (70, 10): 61
```

The first two grids are exactly the DDA results of Chapter 20. The three tie grids show Section 21.6: the shallow version keeps column 1 in row 0; DDA and `drawLine` move it to row 1.

Open the pictures:
- `fan_bresenham.ppm`: it looks just like Chapter 20's fan. (If you compare the two files pixel by pixel, a few pixels differ at ties. Your eye will not see it.)
- `styles.ppm`: a thin black line, a thick blue line, a dashed red line, and a green five-sided shape at the bottom.

---

## Small examples

### Example 1 — The shallow algorithm for (0, 0) to (6, 4)

> dx = 6, dy = 4: start d = −6, step +8, move −12

| x | plot | d + 8 | > 0? | then d |
|---|---|---|---|---|
| 0 | (0, 0) | 2 | yes → y = 1 | −10 |
| 1 | (1, 1) | −2 | no | −2 |
| 2 | (2, 1) | 6 | yes → y = 2 | −6 |
| 3 | (3, 2) | 2 | yes → y = 3 | −10 |
| 4 | (4, 3) | −2 | no | −2 |
| 5 | (5, 3) | 6 | yes → y = 4 | −6 |
| 6 | (6, 4) | end | | |

Check with the true line (y = x × 4 ÷ 6 = 0.667x): at x = 4, the true y is 2.67 → closest row 3 ✓. At x = 1, the true y is 0.67 → row 1 ✓.

### Example 2 — A line going left and up

drawLine from (4, 3) to (0, 1):

> dx = 4, dy = −2, sx = −1, sy = −1, err = 2

> (4, 3): e2 = 4 ≥ −2 → x = 3, err = 0; 4 ≤ 4 → y = 2, err = 4
> (3, 2): e2 = 8 ≥ −2 → x = 2, err = 2; 8 ≤ 4? no
> (2, 2): e2 = 4 → x = 1, err = 0; 4 ≤ 4 → y = 1, err = 4
> (1, 1): e2 = 8 → x = 0, err = 2; no
> (0, 1): end

Pixels: (4, 3), (3, 2), (2, 2), (1, 1), (0, 1). The signs sx and sy did all the work.

### Example 3 — A grid of dashed lines

```cpp
for (int x = 0; x < img.width(); x += 40) {
    drawDashedLine(img, x, 0, x, img.height() - 1, 4, 4, Colour{180, 180, 180});
}
```

Light grey dashed lines every 40 pixels — like the guide lines on graph paper.

### Example 4 — How much work does a thick line do?

A line of 260 steps with a brush of width 5:

> points = 261
> pixels painted = 261 × 25 = 6,525
> but the line only **covers** about 261 × 5 ≈ 1,300 different pixels

So each pixel is painted about 5 times. That is the price of the simple brush method (Section 21.8).

---

## Common mistakes

⚠️ **Using `drawLineShallow` for other directions.** It only works for lines going right and down with slope 0 to 1. Use `drawLine` for everything else.

⚠️ **Forgetting the minus sign in `dy = -std::abs(...)`.** The tests then go wrong, and lines go in the wrong direction or never end.

⚠️ **Using `e2 > dy` instead of `e2 >= dy`.** Small changes in the tests change the pixels at ties, or can even make a line miss its end point and run forever.

⚠️ **Plotting the last pixel twice in closed shapes.** Use `includeLast = false` when lines are joined, if it matters (alpha).

⚠️ **`i % (dash + gap)` with dash + gap = 0.** A crash. Check the values first.

⚠️ **Expecting thick lines to be equally thick in all directions.** With a square brush, diagonal lines come out thicker.

---

## Practice

🏋️ **1.** Run the shallow algorithm by hand for (0, 0) to (4, 1). List d after each step and every pixel.

🏋️ **2.** Why do we multiply by **2·dx** and not just by **dx**?

🏋️ **3.** Run `drawLine` by hand for (0, 0) to (3, 3). What kind of step does it take each time?

🏋️ **4.** Run `drawLine` by hand for (2, 0) to (2, 4) (a vertical line). Which test is true each round?

🏋️ **5.** A closed triangle has corners (10, 10), (50, 10), (30, 40). Draw it with `includeLast = false`. How many pixels are painted in total? (Hint: count the points of each line minus 1.)

🏋️ **6.** Make a dashed line pattern "dash 1, gap 1" — a dotted line. What does i % 2 < 1 mean?

🏋️ **7.** Write `drawThickLineAlpha` that uses `fillRectAlpha` instead of `fillRect`. What goes wrong with the overlap? (Try it with alpha 0.2.)

---

## Answers

**1.**
> dx = 4, dy = 1: d = −4, step +2, move −8
> x = 0: plot (0, 0); d = −2 → no
> x = 1: plot (1, 0); d = −2 + 2 = 0 → 0 > 0 is **false** → stay in row 0
> x = 2: plot (2, 0); d = 2 → yes → y = 1, d = −6
> x = 3: plot (3, 1); d = −4 → no
> x = 4: plot (4, 1)
> Pixels: (0, 0), (1, 0), (2, 0), (3, 1), (4, 1).

d = 0 is a **tie**: at x = 2 the true y is 2 × 0.25 = 0.5, exactly halfway between rows 0 and 1, and this version stays in row 0 (Section 21.6).

**2.** The 0.5 in the start value (e′ = −0.5) would become −0.5 × dx, which is **not** a whole number when dx is odd (for dx = 5: −2.5). Multiplying by **2**·dx turns 0.5 into dx, which is always whole.

**3.**
> dx = 3, dy = −3, err = 0
> each round: e2 = 0; 0 ≥ −3 (yes, step x) and 0 ≤ 3 (yes, step y) → err = 0 − 3 + 3 = 0
> Every step is **diagonal**: (0, 0), (1, 1), (2, 2), (3, 3).

**4.**
> dx = 0, dy = −4, sx = −1 (x0 is not < x1, so −1 — but it is never used), sy = +1, err = −4
> round 1: e2 = −8; −8 ≥ −4? **no**; −8 ≤ 0? **yes** → y = 1, err = −4
> the same every round
> Only the "step y" test is ever true. Pixels: (2, 0), (2, 1), (2, 2), (2, 3), (2, 4). x never changes, so the unused sx does not matter.

**5.**
> line 1: (10, 10) → (50, 10): steps = 40 → 41 points → 40 drawn
> line 2: (50, 10) → (30, 40): steps = max(20, 30) = 30 → 31 points → 30 drawn
> line 3: (30, 40) → (10, 10): steps = 30 → 30 drawn
> total = 40 + 30 + 30 = **100 pixels**, each corner exactly once

**6.** `i % 2` is 0 for even i and 1 for odd i. `i % 2 < 1` is true only for **even** i. So every **second** point is drawn: a dotted line.

**7.**

```cpp
inline void drawThickLineAlpha(Image& image, int x0, int y0, int x1, int y1,
                               int width, Colour c, double alpha) {
    int r = width / 2;
    for (const Point& p : linePoints(x0, y0, x1, y1)) {
        fillRectAlpha(image, makeRect(p.x - r, p.y - r, width, width), c, alpha);
    }
}
```

Because neighbouring squares overlap (Example 4), the pixels in the **middle** of the line are blended about 5 times, and the ones at the **edges** fewer times. With α = 0.2, the middle becomes much darker than 0.2 (about 1 − 0.8⁵ ≈ 0.67, Chapter 18), and the line looks like it has dark and light **stripes**. The right fix is to first **collect** all the pixels the line covers (a mask, Chapter 10), and then blend each pixel **once**.

---

## Summary

🧠 Bresenham's algorithm draws lines with **integers only**: additions, subtractions and comparisons.

🧠 For a shallow line, each column is a **decision**: stay in the row, or move down one.

🧠 The **error term** remembers how far the true line is from the chosen row. Shift by 0.5 and multiply by **2·dx** to make every number whole.

🧠 Shallow version: **d = −dx; each column: plot, d += 2·dy; if d > 0: y += 1, d −= 2·dx**.

🧠 General version: **dx = |Δx|, dy = −|Δy|, sx, sy, err = dx + dy**; each round **e2 = 2·err**, step x if e2 ≥ dy, step y if e2 ≤ dx.

🧠 At **ties**, different methods can choose different pixels. Both are correct.

🧠 `includeLast = false` stops joined lines from drawing corners twice.

🧠 Thick lines = a square **brush** at every point. Dashed lines = draw point i only if **i % (dash + gap) < dash**.

---

## Next chapter

Lines are done. In Chapter 22 we draw **circles**: first with the **equation of a circle** (x² + y² = r², which is Pythagoras again), and then with the **midpoint circle algorithm** — Bresenham's idea of "running error and small decisions", bent into a curve, using the circle's **eight-way symmetry**.
