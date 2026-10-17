# Chapter 20 — Lines, Part 1: the Slope and the DDA Method

> **Part 4 · Chapter 20 of 82**
> **You need:** Chapters 1–19 · **You will make:** `lines.h` (two ways to draw a line), `fan.ppm` (coloured lines in every direction), `naive_vs_dda.ppm` and `graph_lines.ppm` (the Chapter 13 graph, now with no gaps)

---

## What you will learn

- What a **line segment** is, and how two **endpoints** describe it.
- The **slope** of a line: "rise over run", and what its sign means when y goes down.
- The **equation of a line**: y = y0 + slope × (x − x0).
- The simplest way to draw a line — **one pixel per column** — and why it leaves **gaps**.
- The **DDA** method: take as many steps as the **longer** direction needs, so there are never gaps.
- Why we compute each point **from the start**, instead of adding a small step again and again.
- How DDA fixes the gaps in the Chapter 13 graph.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **line segment** | A straight piece of line with two ends. We usually just say "line". |
| **endpoint** | One of the two ends of a line segment. |
| **slope** | How steep a line is: how far it goes across or down for each step. |
| **rise** and **run** | Rise: how far a line goes in y. Run: how far it goes in x. |
| **steep** | A line that goes more in y than in x (slope bigger than 1 or smaller than −1). |
| **shallow** | A line that goes more in x than in y (slope between −1 and 1). |
| **major axis** | The direction (x or y) in which the line goes **further**. |
| **DDA** | "Digital Differential Analyser": a simple way to draw lines by taking equal small steps. |
| **connected** | A line is connected if each pixel touches the next one (no gaps). |
| **drift** | Small errors that grow bigger and bigger when you repeat a calculation many times. |
| **polyline** | Many line segments joined end to end. |

---

## 20.1 What is a line?

📖 **New word: line segment** — a straight piece of line with two ends.

📖 **New word: endpoint** — one of its two ends.

In maths, a "line" goes on forever in both directions. In drawing, we almost always want a **segment** from point A to point B. In this book, "line" means a segment.

A line is fully described by its two endpoints: **(x0, y0)** and **(x1, y1)**.

```
 (x0, y0) ●
            ╲
              ╲
                ╲
                  ● (x1, y1)
```

The question of this chapter: **which pixels should we colour**, so that the result looks like a straight line from A to B?

---

## 20.2 The slope

📖 **New word: rise** and **run** — the rise is how far the line goes in y; the run is how far it goes in x.

> run = dx = x1 − x0
> rise = dy = y1 − y0

📖 **New word: slope** — how steep the line is:

> **slope = rise ÷ run = dy ÷ dx**

🔢 **Maths: three lines**

> from (0, 0) to (5, 2): slope = 2 ÷ 5 = **0.4** — for each step right, it goes 0.4 down
> from (0, 0) to (2, 6): slope = 6 ÷ 2 = **3** — for each step right, it goes 3 down
> from (0, 5) to (10, 0): slope = −5 ÷ 10 = **−0.5** — for each step right, it goes 0.5 **up**

⚠️ **Careful: y goes down!** In school maths, a positive slope goes **up** to the right. In images, y grows **downward** (Chapter 3), so a **positive** slope goes **down** to the right, and a **negative** slope goes **up** to the right.

| Slope | Picture (in an image) |
|---|---|
| 0 | flat (horizontal) |
| 0.4 | gently down to the right |
| 1 | exactly diagonal, down to the right (45°) |
| 3 | steeply down |
| −0.5 | gently **up** to the right |
| "infinite" | straight down (vertical): dx = 0, so we cannot divide |

📖 **New word: steep** — a line with |slope| > 1: it goes further in y than in x.

📖 **New word: shallow** — a line with |slope| ≤ 1: it goes at least as far in x as in y.

---

## 20.3 The equation of a line

If we know one point (x0, y0) and the slope, we can find y for **any** x on the line:

> **y = y0 + slope × (x − x0)**

This says: start at y0, and for every step away from x0, add `slope` to y.

🔢 **Maths: the line from (0, 0) to (5, 2), at x = 3**

> slope = 0.4
> y = 0 + 0.4 × (3 − 0) = **1.2**

So the line passes through (3, 1.2). There is no pixel at y = 1.2. We **round** (Chapter 13) to row 1, and colour pixel (3, 1).

Look closely: this is a **lerp** (Chapter 13) in disguise. With t = (x − x0) ÷ (x1 − x0):

> y = y0 + (y1 − y0) × t = lerp(y0, y1, t) ✓

Moving along a line from A to B is lerping both x and y with the same t. We use that idea for DDA in Section 20.6.

---

## 20.4 A first try: one pixel per column

Here is the simplest idea:

1. Go through every column x from x0 to x1.
2. Compute y with the line equation.
3. Round y, and colour that pixel.

🔢 **Maths: from (0, 0) to (5, 2)**

| x | y = 0.4 × x | rounded |
|---|---|---|
| 0 | 0.0 | 0 |
| 1 | 0.4 | 0 |
| 2 | 0.8 | 1 |
| 3 | 1.2 | 1 |
| 4 | 1.6 | 2 |
| 5 | 2.0 | 2 |

```
  ##....
  ..##..
  ....##
```

That looks like a good line. 

### The problem: steep lines

🔢 **Maths: from (0, 0) to (2, 6)** (slope 3)

| x | y = 3 × x | rounded |
|---|---|---|
| 0 | 0 | 0 |
| 1 | 3 | 3 |
| 2 | 6 | 6 |

Only **3** pixels for a line that is 6 rows tall:

```
  #..
  ...
  ...
  .#.
  ...
  ...
  ..#
```

📖 **New word: connected** — each pixel of the line touches the next one (as one of its 8 neighbours, Chapter 3).

This line is **not connected**. It is three dots with big gaps. The problem: we took one pixel per **column**, but this line moves **3 rows** for every column. We need one pixel per **row** instead.

And a vertical line (dx = 0) is even worse: we cannot even compute the slope (we would divide by zero). Our naive function must treat it as a special case.

🧠 **Remember:** One pixel per column only works for **shallow** lines. A steep line needs one pixel per **row**.

---

## 20.5 Walk along the longer direction

📖 **New word: major axis** — the direction in which the line goes **further**: x if |dx| ≥ |dy|, y otherwise.

The fix is simple: take one pixel per step along the **major axis**.

- Shallow line (|dx| ≥ |dy|): one pixel per **column**. In each step, y moves **less than one** row.
- Steep line (|dy| > |dx|): one pixel per **row**. In each step, x moves **less than one** column.

Either way, each step moves **exactly 1** pixel in the major direction and **at most 1** pixel in the other. So each new pixel is always one of the 8 neighbours of the previous one: **no gaps**.

We could write two separate loops (one for shallow lines, one for steep lines). The **DDA** method does both with **one** loop.

---

## 20.6 The DDA method

📖 **New word: DDA** — "Digital Differential Analyser". The name comes from old machines that solved maths problems by adding small steps. The idea is simple: **walk from A to B in equal small steps**.

🔢 **Maths: the steps**

> dx = x1 − x0, dy = y1 − y0
> **steps = the bigger of |dx| and |dy|** (the length along the major axis)
> **xStep = dx ÷ steps**, **yStep = dy ÷ steps**
> for i = 0, 1, 2, … steps:
>     x = x0 + xStep × i
>     y = y0 + yStep × i
>     colour the pixel (round(x), round(y))

Because `steps` is the **bigger** distance, one of xStep and yStep is exactly **±1**, and the other is between −1 and 1. That is exactly the "walk along the longer direction" rule from Section 20.5 — in one loop, for **every** direction.

🔢 **Maths: from (0, 0) to (2, 6) with DDA**

> dx = 2, dy = 6, steps = max(2, 6) = **6**
> xStep = 2 ÷ 6 = 0.333, yStep = 6 ÷ 6 = **1**

| i | x = 0.333 × i | round(x) | y = i | pixel |
|---|---|---|---|---|
| 0 | 0.000 | 0 | 0 | (0, 0) |
| 1 | 0.333 | 0 | 1 | (0, 1) |
| 2 | 0.667 | 1 | 2 | (1, 2) |
| 3 | 1.000 | 1 | 3 | (1, 3) |
| 4 | 1.333 | 1 | 4 | (1, 4) |
| 5 | 1.667 | 2 | 5 | (2, 5) |
| 6 | 2.000 | 2 | 6 | (2, 6) |

```
  #..
  #..
  .#.
  .#.
  .#.
  ..#
  ..#
```

**7 pixels, all connected.** Compare with the 3 dots of Section 20.4.

🔢 **Maths: from (0, 0) to (5, 2) with DDA**

> steps = max(5, 2) = 5, xStep = 1, yStep = 0.4
> the same pixels as the naive method (Section 20.4) — for shallow lines, DDA and the naive method agree.

### How many pixels?

A DDA line has **steps + 1** pixels: the loop runs for i = 0 to steps, **including** both endpoints.

> (0, 0) to (2, 6): 6 + 1 = **7** pixels ✓
> (0, 0) to (0, 0): steps = 0 → we draw just **1** pixel (and we must not divide by zero — our code checks this case first).

### Lines include both endpoints

Remember, rectangles were **half-open** (Chapter 19): the end is **not** included. Lines are different: we include **both** endpoints. Why? Because people expect a line "from A to B" to touch **both** A and B. If you draw a line from (10, 10) to (10, 10), you expect a dot, not nothing.

The cost: when lines are **joined** (Section 20.9), the shared point is drawn **twice** — once as the end of one line, and once as the start of the next. With solid colours this is invisible. With alpha it would make a darker dot at each joint. Chapter 21 shows how to skip the last pixel when needed.

🧠 **Remember:** **DDA**: steps = max(|dx|, |dy|), then for i = 0 … steps, plot round(x0 + i·dx/steps, y0 + i·dy/steps). Every line is connected.

---

## 20.7 Why "x0 + xStep × i", not "x += xStep"?

📖 **New word: drift** — small errors that grow when a calculation is repeated many times.

A common way to write DDA is to **add** the step each time:

```cpp
double x = x0;
for (...) {
    plot(round(x), ...);
    x += xStep;      // add the step again and again
}
```

This works in maths, but not perfectly in a computer. A `double` cannot store most decimal numbers **exactly**. For example, 0.1 is stored as 0.1000000000000000055511… — a tiny bit too big.

🔢 **Maths: adding 0.1 ten times**

> In exact maths: 0.1 × 10 = 1.0
> In a `double`: 0.1 + 0.1 + … (10 times) = 0.9999999999999999

The tiny errors **pile up**. For a line of 10 steps, this is harmless. But for a line of 10,000 steps, the end can be off by enough to round to the **wrong pixel**, and the line may miss its endpoint.

Computing `x0 + xStep * i` makes **one** small rounding error per point — it never piles up. The last point is computed as x0 + (dx ÷ steps) × steps, which is dx + x0 within a tiny error that rounds away. So the line always ends at **exactly** (x1, y1).

---

## 20.8 Rounding, and lines that go outside

We round with **`std::floor(v + 0.5)`** (Chapter 13), because lines can have **negative** coordinates — for example, a line from (−20, 50) to (100, 80) that starts outside the image. `static_cast<int>(v + 0.5)` would round −2.4 to −1 instead of −2 (Chapter 13, Section 13.8), and the part of the line just inside the edge would be off by one.

Our `roundToInt` helper (in `lines.h`) does exactly this.

### Clipping

We do **not** clip lines in this chapter: we simply plot every point, and `setPixel` ignores the ones outside (Chapter 11). That is correct, but for a **very** long line that is mostly outside the image, it wastes time on millions of outside points. Cutting a line to the image is harder than cutting a rectangle, because the cut points are on slanted edges. For now, the simple way is enough.

---

## 20.9 Polylines: fixing the Chapter 13 graph

📖 **New word: polyline** — many line segments joined end to end.

In Chapter 13 we drew the graph of y = x² with **one pixel per column**. Near the edges, the curve was steep, and we got gaps — exactly the problem of Section 20.4.

The fix: compute the curve's point for every column as before, then **connect** each point to the next one with a DDA line:

```
point 0 ──line── point 1 ──line── point 2 ──line── …
```

🔢 **Maths: the two first columns of the graph**

> column 0: maths x = −1, y = 1 → row = (1 + 1) ÷ 2 × 200 = 200 → flipped: 200 − 200 = **0**
> column 1: maths x = −1 + 2 × 1 ÷ 200 = −0.99, y = 0.9801 → row = 1.9801 ÷ 2 × 200 = 198.01 → 198 → flipped: **2**
> The two points are (0, 0) and (1, 2). Before, there was a **gap** at row 1.
> DDA from (0, 0) to (1, 2): steps = 2, xStep = 0.5, yStep = 1
> i = 0: (0, 0)
> i = 1: x = 0.5 → floor(0.5 + 0.5) = **1**, y = 1 → pixel **(1, 1)**
> i = 2: (1, 2)

The new pixel (1, 1) fills the gap at row 1. The curve is a **connected** line from end to end.

---

## Code, part 1: `lines.h`

File: `common/lines.h` (new). It includes `draw.h`.

```cpp
#ifndef LINES_H
#define LINES_H

#include <algorithm>
#include <cmath>
#include "draw.h"

inline int roundToInt(double v) {
    return static_cast<int>(std::floor(v + 0.5));
}

inline void drawLineNaive(Image& image, int x0, int y0, int x1, int y1, Colour c) {
    if (x0 == x1) {
        for (int y = std::min(y0, y1); y <= std::max(y0, y1); ++y) {
            image.setPixel(x0, y, c);
        }
        return;
    }
    double slope = static_cast<double>(y1 - y0) / (x1 - x0);
    for (int x = std::min(x0, x1); x <= std::max(x0, x1); ++x) {
        double y = y0 + slope * (x - x0);
        image.setPixel(x, roundToInt(y), c);
    }
}

inline void drawLineDDA(Image& image, int x0, int y0, int x1, int y1, Colour c) {
    int dx = x1 - x0;
    int dy = y1 - y0;
    int steps = std::max(std::abs(dx), std::abs(dy));
    if (steps == 0) {
        image.setPixel(x0, y0, c);
        return;
    }
    double xStep = static_cast<double>(dx) / steps;
    double yStep = static_cast<double>(dy) / steps;
    for (int i = 0; i <= steps; ++i) {
        double x = x0 + xStep * i;
        double y = y0 + yStep * i;
        image.setPixel(roundToInt(x), roundToInt(y), c);
    }
}

#endif
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef LINES_H` / `#define LINES_H` | Include guard. |
| 4 | `#include <algorithm>` | `std::min` and `std::max`. |
| 5 | `#include <cmath>` | `std::floor`, and `std::abs` for `int`s (since C++17, `<cmath>` gives us all versions of `std::abs`). |
| 6 | `#include "draw.h"` | Rectangles and everything before them (Chapter 19). |
| 8 | `inline int roundToInt(double v) {` | Round to the nearest whole number, correctly for negative numbers too (Section 20.8, Chapter 13). |
| 9–10 | `return static_cast<int>(std::floor(v + 0.5));` `}` | Add 0.5, go down to a whole number. |
| 12 | `inline void drawLineNaive(Image& image, int x0, int y0, int x1, int y1, Colour c) {` | The simple "one pixel per column" method (Section 20.4). We keep it only to **compare**. |
| 13 | `if (x0 == x1) {` | A vertical line: dx = 0, so there is no slope. |
| 14–16 | `for (int y = std::min(y0, y1); y <= std::max(y0, y1); ++y) { image.setPixel(x0, y, c); }` | Draw every row of the column, from the top endpoint to the bottom one. `<=` includes both endpoints (Section 20.6). |
| 17–18 | `return;` `}` | Done with the vertical case. |
| 19 | `double slope = static_cast<double>(y1 - y0) / (x1 - x0);` | The slope dy ÷ dx (Section 20.2), as a `double`. |
| 20 | `for (int x = std::min(x0, x1); x <= std::max(x0, x1); ++x) {` | Every column between the endpoints, left to right, whichever endpoint is on the left. |
| 21 | `double y = y0 + slope * (x - x0);` | The line equation (Section 20.3). It works from either endpoint. |
| 22 | `image.setPixel(x, roundToInt(y), c);` | One pixel in this column. |
| 23–24 | `}` `}` | End. |
| 26 | `inline void drawLineDDA(Image& image, int x0, int y0, int x1, int y1, Colour c) {` | The DDA method (Section 20.6). Works in every direction. |
| 27–28 | `int dx = x1 - x0;` / `int dy = y1 - y0;` | How far the line goes across and down. Either can be negative. |
| 29 | `int steps = std::max(std::abs(dx), std::abs(dy));` | The length along the **major axis**: the number of steps. |
| 30–33 | `if (steps == 0) { image.setPixel(x0, y0, c); return; }` | Both endpoints are the same pixel: draw a single dot. This also stops a divide by zero. |
| 34–35 | `double xStep = static_cast<double>(dx) / steps;` / `double yStep = ...;` | How far x and y move in each step. One of them is exactly 1 or −1. |
| 36 | `for (int i = 0; i <= steps; ++i) {` | steps + 1 points: both endpoints included. |
| 37–38 | `double x = x0 + xStep * i;` / `double y = y0 + yStep * i;` | Compute each point **from the start**, so errors cannot pile up (Section 20.7). |
| 39 | `image.setPixel(roundToInt(x), roundToInt(y), c);` | Round to the nearest pixel and plot it. Outside points are ignored by `setPixel`. |
| 40–41 | `}` `}` | End. |
| 43 | `#endif` | End of the include guard. |

---

## Code, part 2: lines in every direction

File: `ch20/lines.cpp`

```cpp
#include <iostream>
#include <vector>
#include "hsv.h"
#include "lines.h"

void printGrid(const Image& img) {
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
    Image shallow(6, 3);
    drawLineDDA(shallow, 0, 0, 5, 2, colours::white);
    std::cout << "DDA from (0, 0) to (5, 2):\n";
    printGrid(shallow);

    Image steepNaive(3, 7);
    drawLineNaive(steepNaive, 0, 0, 2, 6, colours::white);
    std::cout << "naive from (0, 0) to (2, 6):\n";
    printGrid(steepNaive);

    Image steepDDA(3, 7);
    drawLineDDA(steepDDA, 0, 0, 2, 6, colours::white);
    std::cout << "DDA from (0, 0) to (2, 6):\n";
    printGrid(steepDDA);

    Image fan(200, 200, colours::white);
    for (int i = 0; i < 200; i += 10) {
        Colour c = toColour(hsvToRgb(HSV{i * 1.8, 0.9, 0.8}));
        drawLineDDA(fan, 100, 100, i, 0, c);
        drawLineDDA(fan, 100, 100, 199, i, c);
        drawLineDDA(fan, 100, 100, 199 - i, 199, c);
        drawLineDDA(fan, 100, 100, 0, 199 - i, c);
    }

    Image compare(200, 120, colours::white);
    for (int k = 0; k < 5; ++k) {
        int top = 10;
        int bottom = 110;
        drawLineNaive(compare, 10 + k * 8, top, 20 + k * 8, bottom, colours::red);
        drawLineDDA(compare, 110 + k * 8, top, 120 + k * 8, bottom, colours::blue);
    }

    Image graph(201, 201, colours::white);
    drawLineDDA(graph, 0, 100, 200, 100, Colour{200, 200, 200});
    drawLineDDA(graph, 100, 0, 100, 200, Colour{200, 200, 200});
    std::vector<int> rows;
    for (int px = 0; px < graph.width(); ++px) {
        double mathsX = -1.0 + 2.0 * px / (graph.width() - 1);
        double mathsY = mathsX * mathsX;
        double row = (mathsY + 1.0) / 2.0 * (graph.height() - 1);
        rows.push_back((graph.height() - 1) - roundToInt(row));
    }
    for (int px = 0; px + 1 < graph.width(); ++px) {
        drawLineDDA(graph, px, rows[px], px + 1, rows[px + 1], colours::red);
    }

    bool ok = fan.savePPM("fan.ppm");
    ok = ok && compare.savePPM("naive_vs_dda.ppm");
    ok = ok && graph.savePPM("graph_lines.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
```

### Line by line

**The tiny grids (lines 1–32)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#include <iostream>` / `<vector>` | Printing, and a list of graph rows. |
| 3 | `#include "hsv.h"` | For the rainbow colours of the fan (Chapter 16). |
| 4 | `#include "lines.h"` | Our new header. |
| 6 | `void printGrid(const Image& img) {` | Print a tiny image as `#` (coloured) and `.` (black) — like Chapter 3. |
| 7–8 | `for (int y ...) { std::cout << "  ";` | Each row, indented by two spaces. |
| 9–10 | `for (int x ...) { Colour c = img.getPixel(x, y);` | Each pixel. |
| 11 | `bool on = c.r != 0 \|\| c.g != 0 \|\| c.b != 0;` | Any colour that is not black counts as "on". |
| 12 | `std::cout << (on ? '#' : '.');` | Print one character. |
| 13–16 | `}` `std::cout << "\n";` `}` `}` | End of the row, end of the function. |
| 18 | `int main() {` | The program starts here. |
| 19–22 | `Image shallow(6, 3); drawLineDDA(shallow, 0, 0, 5, 2, colours::white); ... printGrid(shallow);` | A shallow line on a tiny image (Section 20.4). |
| 24–27 | `Image steepNaive(3, 7); drawLineNaive(steepNaive, 0, 0, 2, 6, ...); ...` | The steep line with the **naive** method: expect gaps. |
| 29–32 | `Image steepDDA(3, 7); drawLineDDA(steepDDA, 0, 0, 2, 6, ...); ...` | The same line with **DDA**: expect 7 connected pixels (Section 20.6). |

**The pictures (lines 34–73)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 34 | `Image fan(200, 200, colours::white);` | A white image for the fan of lines. |
| 35 | `for (int i = 0; i < 200; i += 10) {` | 20 positions along each edge: 0, 10, 20, … 190. |
| 36 | `Colour c = toColour(hsvToRgb(HSV{i * 1.8, 0.9, 0.8}));` | A colour from the hue wheel: i × 1.8 goes from 0° to 342°. |
| 37 | `drawLineDDA(fan, 100, 100, i, 0, c);` | From the centre to a point on the **top** edge (moving right as i grows). |
| 38 | `drawLineDDA(fan, 100, 100, 199, i, c);` | …to the **right** edge (moving down). |
| 39 | `drawLineDDA(fan, 100, 100, 199 - i, 199, c);` | …to the **bottom** edge (moving left). |
| 40 | `drawLineDDA(fan, 100, 100, 0, 199 - i, c);` | …to the **left** edge (moving up). Together: lines in every direction — shallow and steep, positive and negative slopes. |
| 41 | `}` | End of the fan. |
| 43 | `Image compare(200, 120, colours::white);` | Naive lines on the left half, DDA lines on the right half. |
| 44 | `for (int k = 0; k < 5; ++k) {` | Five lines of each kind, 8 pixels apart. |
| 45–46 | `int top = 10;` / `int bottom = 110;` | Every line goes from row 10 down to row 110. |
| 47 | `drawLineNaive(compare, 10 + k * 8, top, 20 + k * 8, bottom, colours::red);` | A steep red line (10 across, 100 down: slope 10) with the naive method: only 11 dots each. |
| 48 | `drawLineDDA(compare, 110 + k * 8, top, 120 + k * 8, bottom, colours::blue);` | The same line shape in blue, with DDA: 101 connected pixels each. |
| 49 | `}` | End of the comparison. |
| 51 | `Image graph(201, 201, colours::white);` | The Chapter 13 graph again. |
| 52–53 | `drawLineDDA(graph, 0, 100, 200, 100, ...);` / `drawLineDDA(graph, 100, 0, 100, 200, ...);` | The two grey axes, now drawn as lines. |
| 54 | `std::vector<int> rows;` | The image row of the curve, for each column. |
| 55 | `for (int px = 0; px < graph.width(); ++px) {` | For each column… |
| 56 | `double mathsX = -1.0 + 2.0 * px / (graph.width() - 1);` | …the maths x: a remap from 0–200 to −1–1 (Chapter 13), written out directly. |
| 57 | `double mathsY = mathsX * mathsX;` | y = x². |
| 58 | `double row = (mathsY + 1.0) / 2.0 * (graph.height() - 1);` | Remap maths y (−1 to 1) to a "maths-style" row (0 to 200). |
| 59 | `rows.push_back((graph.height() - 1) - roundToInt(row));` | Round and **flip** (Chapter 3), and remember the row. |
| 60 | `}` | End. |
| 61 | `for (int px = 0; px + 1 < graph.width(); ++px) {` | For each pair of neighbouring columns (the last column has no right neighbour, so we stop one early)… |
| 62 | `drawLineDDA(graph, px, rows[px], px + 1, rows[px + 1], colours::red);` | …connect their points with a line (Section 20.9). |
| 63 | `}` | End: a polyline of 200 short lines. |
| 65–71 | `bool ok = fan.savePPM("fan.ppm"); ... if (!ok) { ...; return 1; }` | Save the three pictures. |
| 72 | `return 0;` | The program finished with no problem. |
| 73 | `}` | End of `main`. |

Compile:

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common lines.cpp -o lines
```

### What you should see

```
DDA from (0, 0) to (5, 2):
  ##....
  ..##..
  ....##
naive from (0, 0) to (2, 6):
  #..
  ...
  ...
  .#.
  ...
  ...
  ..#
DDA from (0, 0) to (2, 6):
  #..
  #..
  .#.
  .#.
  .#.
  ..#
  ..#
```

These are exactly the tables of Sections 20.4 and 20.6.

Open the images:
- `fan.ppm`: 80 coloured lines from the centre to the edges, going round the colour wheel. Every one is connected — shallow or steep, up or down. (You may notice that lines look slightly "jagged", like little stairs. That is normal for lines made of whole pixels. Chapters 27 and 28 make them smooth.)
- `naive_vs_dda.ppm`: on the left, five red "lines" that are just columns of dots. On the right, five solid blue lines.
- `graph_lines.ppm`: the U-shaped curve, now **unbroken** all the way to the top corners.

---

## Small examples

### Example 1 — A diagonal line

From (0, 0) to (4, 4):

> steps = 4, xStep = 1, yStep = 1
> pixels: (0, 0), (1, 1), (2, 2), (3, 3), (4, 4)

A 45° line has exactly one pixel per row **and** per column.

### Example 2 — A line going up and to the left

From (6, 3) to (0, 0):

> dx = −6, dy = −3, steps = 6
> xStep = −1, yStep = −0.5
> i = 0: (6, 3)
> i = 1: (5, 2.5 → round → 3)
> i = 2: (4, 2)
> i = 3: (3, 1.5 → 2)
> i = 4: (2, 1)
> i = 5: (1, 0.5 → 1)
> i = 6: (0, 0)

Negative steps work with no special code.

⚠️ Notice: drawing this line from (0, 0) to (6, 3) gives (1, 0.5 → 1), (3, 1.5 → 2), (5, 2.5 → 3) — the same pixels here. But because .5 always rounds **up**, lines drawn in opposite directions can sometimes differ by one pixel at the "halfway" points. Chapter 21 talks about this.

### Example 3 — A triangle outline

```cpp
drawLineDDA(img, 50, 10, 90, 80, colours::black);
drawLineDDA(img, 90, 80, 10, 80, colours::black);
drawLineDDA(img, 10, 80, 50, 10, colours::black);
```

Three lines that share endpoints make a closed shape. (Filling it comes in Chapter 24.)

### Example 4 — How many pixels?

| Line | |dx| | |dy| | steps | pixels |
|---|---|---|---|---|
| (0, 0) → (100, 0) | 100 | 0 | 100 | 101 |
| (0, 0) → (100, 100) | 100 | 100 | 100 | 101 |
| (0, 0) → (30, 100) | 30 | 100 | 100 | 101 |
| (5, 5) → (5, 5) | 0 | 0 | 0 | 1 |

Interesting: the diagonal line (0, 0) → (100, 100) is about 141 pixels **long** (Pythagoras, Chapter 3), but it is drawn with only 101 pixels — the same as the horizontal one. Diagonal pixels are further apart. This is one reason why diagonal lines look a little **thinner** and lighter than horizontal ones.

---

## Common mistakes

⚠️ **One pixel per column for steep lines.** Big gaps. Use the major axis (DDA).

⚠️ **Dividing by zero.** dx = 0 breaks the slope; steps = 0 breaks DDA. Handle them first.

⚠️ **`x += xStep` for long lines.** Errors pile up (drift). Compute `x0 + xStep * i`.

⚠️ **Rounding with a cast.** Negative coordinates round the wrong way. Use `floor(v + 0.5)`.

⚠️ **`i < steps` instead of `i <= steps`.** The last endpoint is missing.

⚠️ **Forgetting that y goes down.** A positive slope goes **down** to the right.

---

## Practice

🏋️ **1.** Compute the slope of the lines (2, 3) → (10, 7), (0, 10) → (5, 0) and (4, 1) → (4, 9). Which are steep?

🏋️ **2.** Use the line equation to find y at x = 6 on the line from (2, 3) to (10, 7).

🏋️ **3.** Draw (by hand, as a grid) the DDA line from (0, 0) to (3, 5). List every pixel.

🏋️ **4.** How many pixels does the DDA line from (−10, 4) to (20, −6) have? How many of them are inside a 10 × 10 image?

🏋️ **5.** Draw a square outline with four DDA lines from (20, 20) to (80, 80). How many corner pixels are drawn twice?

🏋️ **6.** Draw a "star" shape: lines from the centre of a 200 × 200 image to 8 points: the 4 corners and the 4 middles of the edges.

🏋️ **7.** Write a function `drawPolyline(Image&, const std::vector<int>& xs, const std::vector<int>& ys, Colour)` that connects point 0 to point 1, point 1 to point 2, and so on.

---

## Answers

**1.**
> (2, 3) → (10, 7): 4 ÷ 8 = **0.5** — shallow
> (0, 10) → (5, 0): −10 ÷ 5 = **−2** — steep (going up to the right)
> (4, 1) → (4, 9): dx = 0 — **vertical** (steepest of all; no slope number)

**2.**
> slope = 0.5
> y = 3 + 0.5 × (6 − 2) = 3 + 2 = **5**

**3.**
> steps = max(3, 5) = 5, xStep = 0.6, yStep = 1

| i | x | round | y |
|---|---|---|---|
| 0 | 0.0 | 0 | 0 |
| 1 | 0.6 | 1 | 1 |
| 2 | 1.2 | 1 | 2 |
| 3 | 1.8 | 2 | 3 |
| 4 | 2.4 | 2 | 4 |
| 5 | 3.0 | 3 | 5 |

```
  #...
  .#..
  .#..
  ..#.
  ..#.
  ...#
```

**4.**
> dx = 30, dy = −10, steps = 30 → **31 pixels**
> xStep = 1, yStep = −1/3
> Inside a 10 × 10 image we need 0 ≤ x ≤ 9 and 0 ≤ y ≤ 9.
> x = −10 + i → x ≥ 0 when i ≥ 10; x ≤ 9 when i ≤ 19.
> y = 4 − i/3, rounded: at i = 10, y = 0.67 → 1; at i = 12, y = 0 → 0; at i = 13, y = −0.33 → 0; at i = 14, y = −0.67 → −1 (outside).
> So i = 10, 11, 12, 13 → **4 pixels** inside: (0, 1), (1, 0), (2, 0), (3, 0).
> (Check i = 11: y = 4 − 3.67 = 0.33 → 0. So (1, 0).)

**5.** Four lines: (20, 20)→(80, 20), (80, 20)→(80, 80), (80, 80)→(20, 80), (20, 80)→(20, 20). Each corner is the end of one line and the start of the next, so **all 4 corners** are drawn twice. (With solid colours you cannot see it; with alpha you would.)

**6.**

```cpp
Image star(200, 200, colours::white);
const int ends[8][2] = {{0, 0}, {100, 0}, {199, 0}, {199, 100},
                        {199, 199}, {100, 199}, {0, 199}, {0, 100}};
for (int i = 0; i < 8; ++i) {
    drawLineDDA(star, 100, 100, ends[i][0], ends[i][1], colours::black);
}
star.savePPM("star.ppm");
```

**7.**

```cpp
void drawPolyline(Image& image, const std::vector<int>& xs, const std::vector<int>& ys, Colour c) {
    int count = static_cast<int>(std::min(xs.size(), ys.size()));
    for (int i = 0; i + 1 < count; ++i) {
        drawLineDDA(image, xs[i], ys[i], xs[i + 1], ys[i + 1], c);
    }
}
```

> With n points, there are n − 1 lines. `i + 1 < count` makes sure `xs[i + 1]` always exists. If the two lists have different lengths, we use the shorter one.

---

## Summary

🧠 A line segment is described by two **endpoints**.

🧠 **Slope = dy ÷ dx.** In images, a positive slope goes **down** to the right. |slope| > 1 is **steep**.

🧠 **y = y0 + slope × (x − x0)** — a lerp of y along x.

🧠 One pixel per column leaves **gaps** in steep lines. Walk along the **major axis** instead.

🧠 **DDA**: steps = max(|dx|, |dy|), xStep = dx ÷ steps, yStep = dy ÷ steps, plot round(x0 + xStep·i, y0 + yStep·i) for i = 0 … steps.

🧠 Every DDA line is **connected** and includes **both** endpoints (steps + 1 pixels).

🧠 Compute each point **from the start** (no drift), and round with **floor(v + 0.5)**.

---

## Next chapter

DDA works, but every pixel needs two `double` multiplications, two additions and two roundings. In 1962, Jack Bresenham found a way to draw exactly the same kind of line using **only whole numbers**: additions, subtractions and one comparison per pixel. In Chapter 21 we derive **Bresenham's algorithm** step by step.
