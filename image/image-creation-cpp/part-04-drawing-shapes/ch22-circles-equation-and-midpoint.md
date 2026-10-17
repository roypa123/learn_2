# Chapter 22 — Circles: the Equation and the Midpoint Method

> **Part 4 · Chapter 22 of 82**
> **You need:** Chapters 1–21 · **You will make:** `circles.h` (filled circles, circle outlines with the midpoint method), `target.ppm` (rings) and `bubbles.ppm` (see-through bubbles)

---

## What you will learn

- What a circle is in maths: **all points at distance r from the centre**.
- The **equation of a circle**, (x − cx)² + (y − cy)² = r² — Pythagoras again.
- How to draw a **filled** circle with the pixel-centre test, quickly, using a bounding box.
- Why the simple outline method leaves **gaps** (the same problem as steep lines).
- The circle's **eight-way symmetry**: compute 1/8 of the circle, get the rest for free.
- The **midpoint circle algorithm**: Bresenham's idea of a running error, for curves, with **integers only**.
- The difference between a circle centred **on** a pixel and one centred **between** pixels.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **circle** | All the points that are exactly the same distance from one point, the centre. |
| **radius** (r) | The distance from the centre to the circle. |
| **diameter** | The distance across the circle through the centre: 2 × r. |
| **disc** | A filled circle: the circle **and** everything inside it. |
| **circumference** | The length all the way around a circle: 2 × π × r. |
| **π (pi)** | The number 3.14159…: the circumference divided by the diameter, for every circle. |
| **bounding box** | The smallest rectangle that contains a shape. |
| **symmetry** | When a shape looks the same after it is flipped or turned. |
| **octant** | One eighth of a circle (45°). (First met in Chapter 21, for line directions.) |
| **midpoint** | The point exactly halfway between two other points. |

---

## 22.1 What is a circle?

📖 **New word: circle** — all the points that are exactly the same distance from one point, the **centre**.

📖 **New word: radius** — that distance, called **r**.

📖 **New word: diameter** — the distance across, through the centre: **2r**.

Take a centre (cx, cy) and any point (x, y). In Chapter 3 we learned the distance between two points, with Pythagoras:

> distance = √((x − cx)² + (y − cy)²)

The point is **on** the circle when this distance is exactly r. Squaring both sides (so there is no square root):

> **(x − cx)² + (y − cy)² = r²**

This is the **equation of a circle**.

🔢 **Maths: is (8, 9) on the circle with centre (5, 5) and radius 5?**

> (8 − 5)² + (9 − 5)² = 3² + 4² = 9 + 16 = 25
> r² = 5² = 25
> 25 = 25 → **yes**, it is exactly on the circle

📖 **New word: disc** — a filled circle: the points **on** or **inside** the circle.

> inside or on: (x − cx)² + (y − cy)² **≤** r²
> outside: (x − cx)² + (y − cy)² **>** r²

📖 **New word: π (pi)** — the number 3.14159…, the same for every circle.

📖 **New word: circumference** — the length around the circle: **2πr**.

Two facts we will use to check our pictures:

> circumference = 2 × π × r
> area of a disc = π × r²

---

## 22.2 Filled circles

We have already drawn filled circles twice: in Chapter 10 (`disk.pbm`) and Chapter 14 (the coloured lights). Now we make it a proper library function.

For each pixel, test its **centre** (Chapter 3, Section 3.9):

> dx = (x + 0.5) − cx
> dy = (y + 0.5) − cy
> colour the pixel if dx² + dy² ≤ r²

### Only test the pixels that could be inside

📖 **New word: bounding box** — the smallest rectangle that contains a shape.

A circle with centre (cx, cy) and radius r fits inside the square from (cx − r, cy − r) to (cx + r, cy + r). Pixels outside this square can **never** be inside the circle, so we do not test them.

```
 cx − r            cx + r
   ┌─────────────────┐  cy − r
   │     ▄▄███▄▄     │
   │   ▄█████████▄   │
   │  ████████████   │
   │   ▀█████████▀   │
   │     ▀▀███▀▀     │
   └─────────────────┘  cy + r
```

🔢 **Maths: how much work does the box save?**

> a circle of radius 10 in a 1000 × 1000 image
> testing every pixel: 1,000,000 tests
> testing only the box: about 20 × 20 = 400 tests

We turn the box into whole pixel numbers with `std::floor` (round down) for the start and `std::ceil` (round up, Chapter 19) for the end, so the box is never too small. Then we **clip** it to the image (Chapter 19), so a circle that sticks out of the image is no problem.

🔢 **Maths: the box of a circle at (5.5, 5.5) with radius 5**

> x0 = floor(5.5 − 5) = floor(0.5) = 0
> x1 = ceil(5.5 + 5) = ceil(10.5) = 11
> → columns [0, 11), the same for rows → an 11 × 11 box

### Checking with the area

The filled disc with centre (5.5, 5.5) and radius 5 has **81** pixels (our program counts them). The true area is:

> π × 5² = 3.14159 × 25 ≈ **78.5**

81 is close to 78.5. A disc made of whole pixels can never have exactly the right area, but it is always close — and the bigger the circle, the closer.

### A small surprise: "spikes"

Look at the disc our program prints:

```
  .....#.....
  ..#######..
  .#########.
  .#########.
  .#########.
  ###########
  .#########.
  .#########.
  .#########.
  ..#######..
  .....#.....
```

There is a single pixel sticking out at the top, bottom, left and right. Why?

> pixel (5, 0): centre (5.5, 0.5) → dx = 0, dy = −5 → dx² + dy² = 25 = r² → **exactly on the edge** → inside (≤)

With a whole-number radius and a centre in the middle of a pixel, four pixels lie **exactly** on the circle and get included. They look like little spikes. Two easy fixes:

- use a radius that is not a whole number, like **4.9** or **5.5**, or
- use `<` instead of `≤`.

Neither is "wrong". For big circles, the spikes are too small to see.

---

## 22.3 Outlines: the simple way, and its gaps

For an outline (a ring that is 1 pixel wide), we could solve the circle equation for y:

> (x − cx)² + (y − cy)² = r²
> (y − cy)² = r² − (x − cx)²
> y − cy = ±√(r² − (x − cx)²)

For each column x, there are **two** points: one on the top half (minus) and one on the bottom half (plus).

🔢 **Maths: centre (5, 5), radius 5**

| x − cx | √(25 − (x − cx)²) | rounded |
|---|---|---|
| 0 | √25 = 5 | 5 |
| ±1 | √24 ≈ 4.90 | 5 |
| ±2 | √21 ≈ 4.58 | 5 |
| ±3 | √16 = 4 | 4 |
| ±4 | √9 = 3 | 3 |
| ±5 | √0 = 0 | 0 |

```
  ...#####...
  ..#.....#..
  .#.......#.
  ...........     ← gaps!
  ...........
  #.........#
  ...........
  ...........
  .#.......#.
  ..#.....#..
  ...#####...
```

Only **20** pixels, with big gaps on the left and right sides. It is **exactly** the problem of steep lines in Chapter 20: near the left and right, the circle is **steep** (it goes mostly up and down), and one pixel per column is not enough.

We could fix it the same way as DDA: switch to "one pixel per row" where the circle is steep. There is an even nicer way.

---

## 22.4 Eight-way symmetry

📖 **New word: symmetry** — when a shape looks the same after it is flipped or turned.

A circle has a lot of symmetry. If (x, y) is a point on a circle centred at (0, 0), then so are all of these:

> (x, y), (y, x), (−y, x), (−x, y), (−x, −y), (−y, −x), (y, −x), (x, −y)

Why? Changing the sign of x or y does not change x² or y². And swapping x and y does not change x² + y². So all eight have the same distance from the centre.

```
                (−y, −x) │ (y, −x)
                    ●    │    ●
          (−x, −y) ●     │     ● (x, −y)
                  ───────┼───────
          (−x, y)  ●     │     ● (x, y)
                    ●    │    ●
                (−y, x)  │  (y, x)
```

📖 **New word: octant** — one eighth of a circle (45°).

So we only need to compute **one octant** — 1/8 of the circle — and then plot every point **eight** times, once in each octant. We choose the octant that starts at the **right** side of the circle, (r, 0), and goes **down** to the 45° point, where x = y.

🔢 **Maths: the eight copies of (5, 2), around centre (100, 50)**

| Copy | Point |
|---|---|
| (x, y) | (105, 52) |
| (y, x) | (102, 55) |
| (−y, x) | (98, 55) |
| (−x, y) | (95, 52) |
| (−x, −y) | (95, 48) |
| (−y, −x) | (98, 45) |
| (y, −x) | (102, 45) |
| (x, −y) | (105, 48) |

Our function `plotEight` does exactly this.

In our octant, the circle goes from **straight down** (at (r, 0), the circle is vertical) to the **45°** point (where it is diagonal). So, in this octant, the circle is always **steep or diagonal**: y changes by 1 every step, and x changes by 0 or 1. That is exactly the kind of yes/no decision Bresenham used (Chapter 21)!

🧠 **Remember:** Compute **one octant** (from (r, 0) down to x = y), and plot **eight** copies of each point.

---

## 22.5 The midpoint method: the decision

📖 **New word: midpoint** — the point exactly halfway between two other points.

In our octant, we go **down** one row at a time: y = 0, 1, 2, … At each step, we are at some point (x, y), and for the next row, y + 1, there are only two choices:

> keep x: (x, y + 1)
> or move one column left: (x − 1, y + 1)

```
            x − 1    x
   row y             ■      ← we are here
   row y + 1   ?  ·  ?      ← the next point is one of these two
                  ↑
               midpoint (x − 0.5, y + 1)
```

Which one is closer to the circle? Look at the **midpoint** between them: (x − 0.5, y + 1).

- If the midpoint is **inside** the circle, the circle passes to the **right** of it, closer to x. → **keep x**.
- If the midpoint is **outside**, the circle passes to the **left** of it, closer to x − 1. → **move to x − 1**.

To test "inside or outside", we use the circle equation as a **test function**:

> **f(x, y) = x² + y² − r²**

| f | Meaning |
|---|---|
| f < 0 | inside the circle |
| f = 0 | exactly on the circle |
| f > 0 | outside the circle |

So the decision value is **d = f(x − 0.5, y + 1)**:
- d < 0 (midpoint inside) → keep x
- d ≥ 0 (midpoint outside or on) → x − 1

---

## 22.6 The midpoint method: updating d without squares

Computing (x − 0.5)² + (y + 1)² − r² at every step would need multiplications and fractions. Like Bresenham, we find how d **changes** from one step to the next, and just add that change.

### The start

We start at (r, 0). The first midpoint is (r − 0.5, 1):

> d = (r − 0.5)² + 1² − r²
> = r² − r + 0.25 + 1 − r²
> = **1.25 − r**

That has a fraction (0.25). But look: r is a whole number, and later changes (below) are whole numbers too. So d is always "a whole number + 0.25". For the sign test, the 0.25 never changes the answer:

> If the whole part is −1 or less, d = (whole part) + 0.25 is still negative.
> If the whole part is 0 or more, d is positive.

So we can **drop the 0.25** and start with **d = 1 − r**, and the test "d < 0" gives exactly the same decisions.

### When we keep x (d < 0)

The next midpoint is (x − 0.5, y + 2) instead of (x − 0.5, y + 1). Only the y part changes:

> change = (y + 2)² − (y + 1)²
> = (y² + 4y + 4) − (y² + 2y + 1)
> = 2y + 3

In the code, we first do `++y`, so the "new y" is y + 1. In terms of the new y (call it Y = y + 1): 2y + 3 = 2(Y − 1) + 3 = **2Y + 1**.

### When we move x left (d ≥ 0)

Now both parts change: the next midpoint is (x − 1.5, y + 2):

> change in the x part = (x − 1.5)² − (x − 0.5)² = (x² − 3x + 2.25) − (x² − x + 0.25) = −2x + 2
> change in the y part = 2y + 3 (as above)
> total change = 2y − 2x + 5

In terms of the new values Y = y + 1 and X = x − 1: 2(Y − 1) − 2(X + 1) + 5 = **2(Y − X) + 1**.

🧠 **Remember — the midpoint circle algorithm:**

```
x = r, y = 0, d = 1 − r
while x ≥ y:
    plot the 8 copies of (x, y)
    y = y + 1
    if d < 0:
        d = d + 2·y + 1
    else:
        x = x − 1
        d = d + 2·(y − x) + 1
```

Every number is a whole number. Each step is an addition or two — no square roots, no `double`.

---

## 22.7 A full worked example: radius 5

> start: x = 5, y = 0, d = 1 − 5 = −4

| plot (x, y) | then y | d < 0? | x | change | new d |
|---|---|---|---|---|---|
| (5, 0) | 1 | yes (−4) | 5 | 2·1 + 1 = 3 | −1 |
| (5, 1) | 2 | yes (−1) | 5 | 2·2 + 1 = 5 | 4 |
| (5, 2) | 3 | no (4) | 4 | 2·(3 − 4) + 1 = −1 | 3 |
| (4, 3) | 4 | no (3) | 3 | 2·(4 − 3) + 1 = 3 | 6 |
| stop: x = 3 < y = 4 | | | | | |

So the octant has the points **(5, 0), (5, 1), (5, 2), (4, 3)**.

Check against the true circle:
> at y = 1: true x = √(25 − 1) = 4.90 → closest 5 ✓
> at y = 2: true x = √21 = 4.58 → closest 5 ✓
> at y = 3: true x = √16 = 4 ✓

With eight-way symmetry, these 4 points become the whole circle:

```
  ...#####...
  ..#.....#..
  .#.......#.
  #.........#
  #.........#
  #.........#
  #.........#
  #.........#
  .#.......#.
  ..#.....#..
  ...#####...
```

**28 pixels, no gaps.** Compare with the 20 pixels and the gaps of Section 22.3.

🔢 **Maths: why 28?**

> 4 octant points × 8 copies = 32 plots
> but (5, 0) and its copies lie **on** the axes, where some copies are the same point: (x, y) = (5, 0) and (x, −y) = (5, −0) are identical, and so on. Its 8 copies give only 4 different pixels.
> So: 3 points × 8 + 4 = 24 + 4 = **28**

🔢 **Maths: a check with the circumference**

> 2 × π × 5 ≈ 31.4
> 28 pixels for a length of about 31 — the diagonal parts use fewer pixels per length (Chapter 20, Example 4), so a little less than the circumference is expected. For any radius, the midpoint circle has about 5.66 × r pixels (5.66 × 5 ≈ 28 ✓).

---

## 22.8 Centred on a pixel, or between pixels?

Our two circle functions have a small but important difference:

| Function | Centre | Parameters |
|---|---|---|
| `drawCircle` (midpoint) | a **pixel**: (cx, cy) are whole numbers | the circle goes through pixel (cx + r, cy) |
| `fillCircle` | **any point**: (cx, cy) and r are `double`s | pixels are tested by their **centres** |

A midpoint circle with centre pixel (5, 5) and radius 5 spans columns 0 to 10: **11 pixels wide**. Its width is always **2r + 1**, an odd number, because the centre pixel is in the middle.

The **geometric** centre of pixel (5, 5) is (5.5, 5.5) (Chapter 3). So to fill the inside of `drawCircle(img, 5, 5, 5, …)`, use `fillCircle(img, 5.5, 5.5, 5.0, …)`. That is exactly what our program does.

⚠️ **Careful:** If you fill with centre (5, 5) instead of (5.5, 5.5), the filled disc is shifted half a pixel up and to the left of the outline. On big circles you will see a thin gap on one side and an overlap on the other.

---

## 22.9 See-through circles

Like `fillRectAlpha` (Chapter 19), a filled circle can be blended. Our `fillCircle` takes an extra parameter `alpha`, with the default value **1.0** (solid). When alpha is below 1, it uses `blendPixel` (Chapter 18) instead of `setPixel`.

The `bubbles.ppm` picture uses alpha 0.5: where bubbles overlap, you see both colours mixed, and you can see the dark background through them. Each bubble also gets a thin white outline with `drawCircle`.

---

## Code, part 1: `circles.h`

File: `common/circles.h` (new). It includes `lines.h` (for `roundToInt`, and through it `draw.h` and everything before).

```cpp
#ifndef CIRCLES_H
#define CIRCLES_H

#include <cmath>
#include "lines.h"

inline void drawCircleNaive(Image& image, int cx, int cy, int r, Colour c) {
    for (int x = -r; x <= r; ++x) {
        int y = roundToInt(std::sqrt(static_cast<double>(r * r - x * x)));
        image.setPixel(cx + x, cy + y, c);
        image.setPixel(cx + x, cy - y, c);
    }
}

inline void plotEight(Image& image, int cx, int cy, int x, int y, Colour c) {
    image.setPixel(cx + x, cy + y, c);
    image.setPixel(cx + y, cy + x, c);
    image.setPixel(cx - y, cy + x, c);
    image.setPixel(cx - x, cy + y, c);
    image.setPixel(cx - x, cy - y, c);
    image.setPixel(cx - y, cy - x, c);
    image.setPixel(cx + y, cy - x, c);
    image.setPixel(cx + x, cy - y, c);
}

inline void drawCircle(Image& image, int cx, int cy, int r, Colour c) {
    if (r < 0) {
        return;
    }
    int x = r;
    int y = 0;
    int d = 1 - r;
    while (x >= y) {
        plotEight(image, cx, cy, x, y, c);
        ++y;
        if (d < 0) {
            d += 2 * y + 1;
        } else {
            --x;
            d += 2 * (y - x) + 1;
        }
    }
}

inline void fillCircle(Image& image, double cx, double cy, double radius, Colour c,
                       double alpha = 1.0) {
    int x0 = static_cast<int>(std::floor(cx - radius));
    int y0 = static_cast<int>(std::floor(cy - radius));
    int x1 = static_cast<int>(std::ceil(cx + radius));
    int y1 = static_cast<int>(std::ceil(cy + radius));
    Rect box = clipToImage(Rect{x0, y0, x1, y1}, image);
    double r2 = radius * radius;
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            double dx = (x + 0.5) - cx;
            double dy = (y + 0.5) - cy;
            if (dx * dx + dy * dy <= r2) {
                if (alpha >= 1.0) {
                    image.setPixel(x, y, c);
                } else {
                    blendPixel(image, x, y, c, alpha);
                }
            }
        }
    }
}

#endif
```

### Line by line

**The simple outline (lines 1–13)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef CIRCLES_H` / `#define CIRCLES_H` | Include guard. |
| 4 | `#include <cmath>` | `std::sqrt`, `std::floor`, `std::ceil`. |
| 5 | `#include "lines.h"` | `roundToInt` (Chapter 20), and `draw.h` for `Rect` and clipping. |
| 7 | `inline void drawCircleNaive(Image& image, int cx, int cy, int r, Colour c) {` | The simple "one pixel per column" outline (Section 22.3). Only for comparison. |
| 8 | `for (int x = -r; x <= r; ++x) {` | Every column from the left edge of the circle to the right edge, as an offset from the centre. |
| 9 | `int y = roundToInt(std::sqrt(static_cast<double>(r * r - x * x)));` | Solve the circle equation for y: √(r² − x²). It is never negative here, because |x| ≤ r. |
| 10–11 | `image.setPixel(cx + x, cy + y, c);` / `image.setPixel(cx + x, cy - y, c);` | One point on the bottom half and one on the top half. |
| 12–13 | `}` `}` | End. |

**Eight copies (lines 15–24)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 15 | `inline void plotEight(Image& image, int cx, int cy, int x, int y, Colour c) {` | Plot the eight symmetric copies of the offset (x, y) around the centre (Section 22.4). |
| 16–23 | `image.setPixel(cx + x, cy + y, c);` … `image.setPixel(cx + x, cy - y, c);` | The eight copies, going round the circle: (x, y), (y, x), (−y, x), (−x, y), (−x, −y), (−y, −x), (y, −x), (x, −y). |
| 24 | `}` | End. |

**The midpoint circle (lines 26–43)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 26 | `inline void drawCircle(Image& image, int cx, int cy, int r, Colour c) {` | The midpoint circle (Sections 22.5–22.7). Centre on pixel (cx, cy). |
| 27–29 | `if (r < 0) { return; }` | A negative radius makes no sense: draw nothing. (r = 0 draws one pixel: the centre.) |
| 30–31 | `int x = r;` / `int y = 0;` | Start at the right side of the circle: offset (r, 0). |
| 32 | `int d = 1 - r;` | The decision value for the first midpoint, without the 0.25 (Section 22.6). |
| 33 | `while (x >= y) {` | Stay in our octant: it ends at the 45° point, where x and y meet. |
| 34 | `plotEight(image, cx, cy, x, y, c);` | Plot this point in all eight octants. |
| 35 | `++y;` | Every step moves one row (in our octant, y always changes). |
| 36–37 | `if (d < 0) { d += 2 * y + 1; }` | The midpoint was **inside**: keep x. Update d for the next midpoint. |
| 38–41 | `} else { --x; d += 2 * (y - x) + 1; }` | The midpoint was **outside** (or on): move one column in. Update d. |
| 42–43 | `}` `}` | End. |

**The filled circle (lines 45–66)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 45–46 | `inline void fillCircle(Image& image, double cx, double cy, double radius, Colour c, double alpha = 1.0) {` | A filled circle with any centre and radius (Section 22.2). `alpha` is optional: solid by default. |
| 47–48 | `int x0 = static_cast<int>(std::floor(cx - radius));` / `int y0 = ...;` | The top-left of the bounding box, rounded **down**. |
| 49–50 | `int x1 = static_cast<int>(std::ceil(cx + radius));` / `int y1 = ...;` | The bottom-right, rounded **up**. Half-open: [x0, x1). |
| 51 | `Rect box = clipToImage(Rect{x0, y0, x1, y1}, image);` | Clip the box to the image (Chapter 19). |
| 52 | `double r2 = radius * radius;` | r², computed once. |
| 53–54 | `for (int y = box.y0; y < box.y1; ++y) { for (int x = box.x0; x < box.x1; ++x) {` | Every pixel in the box. |
| 55–56 | `double dx = (x + 0.5) - cx;` / `double dy = (y + 0.5) - cy;` | From the circle centre to the **pixel centre**. |
| 57 | `if (dx * dx + dy * dy <= r2) {` | Inside or on the circle? |
| 58–62 | `if (alpha >= 1.0) { image.setPixel(x, y, c); } else { blendPixel(image, x, y, c, alpha); }` | Solid paint, or see-through paint (Section 22.9). |
| 63–66 | `}` `}` `}` `}` | End. |
| 68 | `#endif` | End of the include guard. |

---

## Code, part 2: rings and bubbles

File: `ch22/circles.cpp`

```cpp
#include <iostream>
#include <string>
#include "circles.h"
#include "hsv.h"

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

int countLit(const Image& img) {
    int count = 0;
    for (int y = 0; y < img.height(); ++y) {
        for (int x = 0; x < img.width(); ++x) {
            Colour c = img.getPixel(x, y);
            if (c.r != 0 || c.g != 0 || c.b != 0) {
                ++count;
            }
        }
    }
    return count;
}

int main() {
    Image naive(11, 11);
    drawCircleNaive(naive, 5, 5, 5, colours::white);
    printGrid("naive circle, radius 5", naive);

    Image midpoint(11, 11);
    drawCircle(midpoint, 5, 5, 5, colours::white);
    printGrid("midpoint circle, radius 5", midpoint);
    std::cout << "pixels in the midpoint circle: " << countLit(midpoint) << "\n";

    Image disc(11, 11);
    fillCircle(disc, 5.5, 5.5, 5.0, colours::white);
    printGrid("filled disc, centre (5.5, 5.5), radius 5", disc);
    std::cout << "pixels in the filled disc: " << countLit(disc) << "\n";

    Image target(220, 220, colours::white);
    for (int r = 10; r <= 100; r += 10) {
        Colour c = (r % 20 == 0) ? colours::red : colours::blue;
        drawCircle(target, 110, 110, r, c);
    }

    Image bubbles(300, 200, Colour{20, 30, 60});
    for (int i = 0; i < 12; ++i) {
        double cx = 25.0 + i * 23.0;
        double cy = 100.0 + ((i % 3) - 1) * 45.0;
        double radius = 15.0 + (i % 4) * 8.0;
        Colour c = toColour(hsvToRgb(HSV{i * 30.0, 0.7, 1.0}));
        fillCircle(bubbles, cx, cy, radius, c, 0.5);
        drawCircle(bubbles, roundToInt(cx), roundToInt(cy), roundToInt(radius), colours::white);
    }

    bool ok = target.savePPM("target.ppm");
    ok = ok && bubbles.savePPM("bubbles.ppm");
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
| 1–2 | `#include <iostream>` / `<string>` | Printing and titles. |
| 3–4 | `#include "circles.h"` / `#include "hsv.h"` | Our new header, and hue colours (Chapter 16). |
| 6–17 | `void printGrid(...) { ... }` | Print a tiny image as `#` and `.` (as in Chapter 21). |
| 19 | `int countLit(const Image& img) {` | Count the pixels that are not black. |
| 20–29 | `int count = 0; for (...) { for (...) { ... if (not black) ++count; } }` | Look at every pixel and count. |
| 30 | `}` | End. |
| 32 | `int main() {` | The program starts here. |
| 33–35 | `Image naive(11, 11); drawCircleNaive(naive, 5, 5, 5, ...); printGrid(...);` | The simple outline: expect gaps (Section 22.3). |
| 37–40 | `Image midpoint(11, 11); drawCircle(midpoint, 5, 5, 5, ...); printGrid(...); ... countLit(midpoint)` | The midpoint circle: expect no gaps and 28 pixels (Section 22.7). |
| 42–45 | `Image disc(11, 11); fillCircle(disc, 5.5, 5.5, 5.0, ...); ... countLit(disc)` | The filled disc with the same geometric centre (Section 22.8): expect 81 pixels and four "spikes" (Section 22.2). |
| 47 | `Image target(220, 220, colours::white);` | A white image for rings. |
| 48 | `for (int r = 10; r <= 100; r += 10) {` | Ten radii: 10, 20, … 100. |
| 49 | `Colour c = (r % 20 == 0) ? colours::red : colours::blue;` | Red for 20, 40, 60, 80, 100; blue for the others. |
| 50 | `drawCircle(target, 110, 110, r, c);` | A ring around the centre. |
| 51 | `}` | End of the rings. |
| 53 | `Image bubbles(300, 200, Colour{20, 30, 60});` | A dark blue background. |
| 54 | `for (int i = 0; i < 12; ++i) {` | Twelve bubbles. |
| 55 | `double cx = 25.0 + i * 23.0;` | Spread across the image, 23 pixels apart. |
| 56 | `double cy = 100.0 + ((i % 3) - 1) * 45.0;` | `(i % 3) − 1` is −1, 0 or 1, so the bubbles go up and down in a wave: y = 55, 100 or 145. |
| 57 | `double radius = 15.0 + (i % 4) * 8.0;` | Four sizes: 15, 23, 31, 39. |
| 58 | `Colour c = toColour(hsvToRgb(HSV{i * 30.0, 0.7, 1.0}));` | Each bubble gets its own hue, 30° apart. |
| 59 | `fillCircle(bubbles, cx, cy, radius, c, 0.5);` | A half-transparent filled circle. |
| 60 | `drawCircle(bubbles, roundToInt(cx), roundToInt(cy), roundToInt(radius), colours::white);` | A thin white outline. `drawCircle` needs whole numbers, so we round. |
| 61 | `}` | End of the bubbles. |
| 63–68 | `bool ok = target.savePPM(...); ... if (!ok) { ...; return 1; }` | Save both pictures. |
| 69 | `return 0;` | The program finished with no problem. |
| 70 | `}` | End of `main`. |

Compile:

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common circles.cpp -o circles
```

### What you should see

```
naive circle, radius 5:
  ...#####...
  ..#.....#..
  .#.......#.
  ...........
  ...........
  #.........#
  ...........
  ...........
  .#.......#.
  ..#.....#..
  ...#####...
midpoint circle, radius 5:
  ...#####...
  ..#.....#..
  .#.......#.
  #.........#
  #.........#
  #.........#
  #.........#
  #.........#
  .#.......#.
  ..#.....#..
  ...#####...
pixels in the midpoint circle: 28
filled disc, centre (5.5, 5.5), radius 5:
  .....#.....
  ..#######..
  .#########.
  .#########.
  .#########.
  ###########
  .#########.
  .#########.
  .#########.
  ..#######..
  .....#.....
pixels in the filled disc: 81
```

Open the pictures:
- `target.ppm`: ten rings, alternating blue and red, like a shooting target. Every ring is closed and round.
- `bubbles.ppm`: twelve coloured bubbles in a wave, see-through where they overlap, each with a white edge.

---

## Small examples

### Example 1 — The midpoint table for radius 3

> x = 3, y = 0, d = 1 − 3 = −2

| plot | y | d < 0? | x | new d |
|---|---|---|---|---|
| (3, 0) | 1 | yes | 3 | −2 + 3 = 1 |
| (3, 1) | 2 | no | 2 | 1 + 2·(2 − 2) + 1 = 2 |
| (2, 2) | 3 | no | 1 | (stop: 1 < 3) |

Octant points: (3, 0), (3, 1), (2, 2). Pixels: 4 + 8 + 4 = **16**. ((2, 2) lies on the diagonal, where (x, y) and (y, x) are the same point, so it gives only 4 different pixels.)

### Example 2 — A filled circle from the midpoint method

The midpoint points tell us, for each row, how far the circle goes left and right. Filling between them gives a disc with **exactly** the same edge as `drawCircle`:

```cpp
// inside the midpoint loop, instead of plotEight:
fillRect(img, Rect{cx - x, cy + y, cx + x + 1, cy + y + 1}, c);
fillRect(img, Rect{cx - x, cy - y, cx + x + 1, cy - y + 1}, c);
fillRect(img, Rect{cx - y, cy + x, cx + y + 1, cy + x + 1}, c);
fillRect(img, Rect{cx - y, cy - x, cx + y + 1, cy - x + 1}, c);
```

Each `Rect` is one row from the left edge to the right edge (+ 1, because the rectangle is half-open and we want to include the right edge pixel). Rows can be filled more than once, which is fine for solid colours.

### Example 3 — Is a point inside a ring?

A ring (a thick circle) between radius 20 and radius 30 around (100, 100). Is (120, 115) inside it?

> dx = 20, dy = 15 → dx² + dy² = 400 + 225 = 625 → distance = 25
> 20 ≤ 25 ≤ 30 → **yes**

(This is the same test as Chapter 10, Practice 6.)

### Example 4 — How many pixels does a big circle have?

> radius 100: about 5.66 × 100 ≈ **566** outline pixels
> circumference: 2 × π × 100 ≈ 628

The filled disc of radius 100: about π × 100² ≈ **31,416** pixels.

---

## Common mistakes

⚠️ **Testing every pixel of the image for a small circle.** Use the bounding box.

⚠️ **Forgetting the pixel centre (+ 0.5).** The disc is shifted by half a pixel.

⚠️ **One pixel per column for outlines.** Gaps on the left and right sides.

⚠️ **Mixing up the eight copies.** If you write (x, y) and (y, −x) but forget (−y, x), one octant is missing and the circle has a gap. Check that all eight sign/swap combinations are there.

⚠️ **Using `drawCircle` with a centre like 5.5.** It takes whole numbers. Round first, or use `fillCircle` for exact positions.

⚠️ **Expecting exact areas.** A pixel disc is close to πr², never exactly equal.

---

## Practice

🏋️ **1.** Is (13, 2) inside, on, or outside the circle with centre (10, 6) and radius 5?

🏋️ **2.** What is the bounding box (half-open) of a circle with centre (40.5, 20.5) and radius 7.2? Clip it to a 45 × 30 image.

🏋️ **3.** Write the eight copies of the offset (7, 3) around the centre (50, 50).

🏋️ **4.** Run the midpoint algorithm by hand for radius 4. List the octant points and the number of pixels.

🏋️ **5.** Draw a disc with radius 4.9 instead of 5 at (5.5, 5.5). Are there still spikes? How many pixels?

🏋️ **6.** Draw the Olympic-style picture: five rings of radius 30 in two rows, each ring drawn 3 times (radius 29, 30, 31) to make it thicker.

🏋️ **7.** Write `strokeCircle(Image&, double cx, double cy, double r, double thickness, Colour)`: colour the pixels whose centre distance is between r − thickness/2 and r + thickness/2.

---

## Answers

**1.**
> (13 − 10)² + (2 − 6)² = 9 + 16 = 25 = 5² → **on** the circle

**2.**
> x0 = floor(40.5 − 7.2) = floor(33.3) = 33, x1 = ceil(40.5 + 7.2) = ceil(47.7) = 48
> y0 = floor(20.5 − 7.2) = floor(13.3) = 13, y1 = ceil(27.7) = 28
> box = [33, 48) × [13, 28)
> clipped to [0, 45) × [0, 30): **[33, 45) × [13, 28)**

**3.**
> (57, 53), (53, 57), (47, 57), (43, 53), (43, 47), (47, 43), (53, 43), (57, 47)

**4.**
> x = 4, y = 0, d = 1 − 4 = −3

| plot | then y | d < 0? | x | new d |
|---|---|---|---|---|
| (4, 0) | 1 | yes (−3) | 4 | −3 + 2·1 + 1 = 0 |
| (4, 1) | 2 | no (0) | 3 | 0 + 2·(2 − 3) + 1 = −1 |
| (3, 2) | 3 | yes (−1) | 3 | −1 + 2·3 + 1 = 6 |
| (3, 3) | 4 | no (6) | 2 | (stop: x = 2 < y = 4) |

> Octant points: (4, 0), (4, 1), (3, 2), (3, 3).
> (4, 0) is on an axis → 4 different pixels. (3, 3) is on the diagonal → 4 different pixels. (4, 1) and (3, 2) → 8 each.
> Pixels: 4 + 8 + 8 + 4 = **24**

**5.**
> r² = 4.9² = 24.01
> The pixels that were **exactly on** the radius-5 circle have dx² + dy² = 25. With r = 4.9 they are now **outside** (25 > 24.01).
> Which pixels are they? With the centre at (5.5, 5.5), dx and dy are whole numbers, and dx² + dy² = 25 has 12 solutions: (0, ±5), (±5, 0), (±3, ±4) and (±4, ±3).
> So **12** pixels are lost: 81 − 12 = **69 pixels**.
> The 4 spikes are among them, so **no more spikes**. The disc now has a smooth, even edge.

**6.**

```cpp
Image rings(330, 200, colours::white);
const int cxs[5] = {70, 165, 260, 117, 212};
const int cys[5] = {70, 70, 70, 110, 110};
const Colour cols[5] = {colours::blue, colours::black, colours::red, colours::yellow, colours::green};
for (int i = 0; i < 5; ++i) {
    for (int r = 29; r <= 31; ++r) {
        drawCircle(rings, cxs[i], cys[i], r, cols[i]);
    }
}
```

(Drawing circles with radius 29, 30 and 31 next to each other can leave a few single-pixel holes between them, because neighbouring midpoint circles do not always touch. Practice 7 gives a gap-free way.)

**7.**

```cpp
inline void strokeCircle(Image& image, double cx, double cy, double r,
                         double thickness, Colour c) {
    double inner = r - thickness / 2.0;
    double outer = r + thickness / 2.0;
    if (inner < 0.0) {
        inner = 0.0;
    }
    Rect box = clipToImage(Rect{static_cast<int>(std::floor(cx - outer)),
                                static_cast<int>(std::floor(cy - outer)),
                                static_cast<int>(std::ceil(cx + outer)),
                                static_cast<int>(std::ceil(cy + outer))}, image);
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            double dx = (x + 0.5) - cx;
            double dy = (y + 0.5) - cy;
            double d2 = dx * dx + dy * dy;
            if (d2 >= inner * inner && d2 <= outer * outer) {
                image.setPixel(x, y, c);
            }
        }
    }
}
```

This is a **ring**: a disc with a smaller disc removed. It works for any thickness, has no holes, and every pixel is painted once.

---

## Summary

🧠 A circle is all points at distance r from the centre: **(x − cx)² + (y − cy)² = r²**.

🧠 **Filled circle**: test each pixel **centre** with dx² + dy² ≤ r², only inside the clipped **bounding box**.

🧠 One pixel per column leaves **gaps** where the circle is steep.

🧠 **Eight-way symmetry**: compute one octant (from (r, 0) to x = y), plot 8 copies.

🧠 **Midpoint method**: test the midpoint (x − 0.5, y + 1) with f = x² + y² − r²; inside → keep x, outside → x − 1.

🧠 Start with **d = 1 − r**; then **d += 2y + 1** (keep x) or **d += 2(y − x) + 1** (x − 1). Integers only.

🧠 `drawCircle` is centred **on a pixel** (width 2r + 1). `fillCircle` takes any centre; use (cx + 0.5, cy + 0.5) to match.

---

## Next chapter

A circle is round in every direction. An **ellipse** is a "stretched" circle — wider than it is tall, or taller than it is wide. In Chapter 23 we learn its equation, draw filled ellipses, and extend the midpoint idea to ellipses, which have only **four-way** symmetry and need **two** regions instead of one.
