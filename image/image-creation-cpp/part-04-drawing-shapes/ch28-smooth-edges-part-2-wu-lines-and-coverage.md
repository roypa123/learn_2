# Chapter 28 — Smooth Edges, Part 2: Wu's Lines and Coverage

> **Part 4 · Chapter 28 of 82**
> **You need:** Chapters 1–27 (especially 20, 21 and 27) · **You will make:** `wu.h` (Wu's smooth lines, smooth polylines, smooth circle outlines), `wu_spokes.ppm`, `wu_rings.ppm` and `graph.ppm`

---

## What you will learn

- How to compute the coverage of a thin line **directly**, without any samples.
- **Wu's line algorithm**: in each column, split the line's brightness between the **two** nearest pixels.
- Why this split **is** a coverage, and how it relates to Bresenham's choice.
- How to handle steep lines and line ends.
- Why Wu's diagonal lines look a little **lighter** than horizontal ones.
- How the same idea draws smooth **circle outlines**.
- Which smooth-drawing method to choose when — a summary of all of Part 4.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **Wu's algorithm** | A fast way to draw smooth lines, published by Xiaolin Wu in 1991. |
| **analytic** | Computed exactly with a formula, instead of estimated with samples. |
| **gradient** | Here: the slope of the line, how much y changes for one step of x (Chapter 20). |
| **fraction part** | The part of a number after the point: the fraction part of 3.75 is 0.75. |
| **split** | Dividing an amount between two places: 0.75 here, 0.25 there. |
| **polyline** | A chain of straight lines, each one starting where the last one ended. |
| **box filter** | Measuring coverage with a simple square or rectangle "window". |

---

## 28.1 A faster idea for lines

In Chapter 27, a smooth line was a thin rectangle, and every edge pixel was tested with 16 samples. That works, but lines are by far the most common thing we draw — graphs, outlines, drawings, maps, text underlines. A line 500 pixels long touches about 1000 edge pixels: 16,000 sample tests.

In 1991, Xiaolin Wu published a much simpler idea. Think about a **shallow** line (it goes more across than down, Chapter 20). In each **column**, the line passes at some exact height. That height is usually **between** two pixel centres. So:

- give the pixel **just above** the line some of the colour,
- give the pixel **just below** the line the rest,
- and the closer the line is to a pixel, the **more** colour that pixel gets.

No samples. Just one multiplication and one subtraction per column.

📖 **New word: Wu's algorithm** — this method.

📖 **New word: analytic** — computed exactly with a formula, instead of estimated by counting samples.

---

## 28.2 Where is the line in each column?

📖 **New word: gradient** — the slope of the line: g = (y1 − y0) / (x1 − x0), how much y changes for one step of x (Chapter 20).

Our line goes from A = (x0, y0) to B = (x1, y1), with **fractional** coordinates (`PointF`). As always, we use pixel **centres**: column x has its centre at x + 0.5. At that x, the line is at height:

> **yc = y0 + g × ((x + 0.5) − x0)**

(This is the line equation of Chapter 20.)

🔢 **Maths: the line from A = (0.5, 0.5) to B = (8.5, 3.5)**

> g = (3.5 − 0.5) / (8.5 − 0.5) = 3 / 8 = **0.375**
> column 0 (centre 0.5): yc = 0.5 + 0.375 × 0 = 0.5
> column 1 (centre 1.5): yc = 0.5 + 0.375 × 1 = 0.875
> column 2 (centre 2.5): yc = 0.5 + 0.375 × 2 = 1.25
> column 4 (centre 4.5): yc = 0.5 + 0.375 × 4 = 2.0

(We chose A and B at pixel centres, so this is the "same" line as Bresenham from pixel (0, 0) to pixel (8, 3).)

---

## 28.3 Splitting between two rows

📖 **New word: fraction part** — the part after the point: the fraction part of 3.75 is 0.75. We get it with t − floor(t).

📖 **New word: split** — divide an amount between two places.

The pixel centres in a column are at heights 0.5, 1.5, 2.5, … The line at height yc lies between two of them. Which two? Move everything up by 0.5, so the centres are at whole numbers:

> **t = yc − 0.5**
> **row = floor(t)** — the pixel just above (or exactly on) the line
> **f = t − row** — the fraction part, from 0 up to (not including) 1: how far below that pixel's centre the line passes

Then:

> pixel (x, row) gets coverage **1 − f**
> pixel (x, row + 1) gets coverage **f**

🔢 **Maths: column 1 of our line**

> yc = 0.875 → t = 0.375 → row = 0, f = 0.375
> pixel (1, 0) gets 1 − 0.375 = **0.625**
> pixel (1, 1) gets **0.375**

The line passes 0.375 below the centre of row 0 and 0.625 above the centre of row 1 — it is **closer** to row 0, so row 0 gets **more**. ✓

🔢 **Maths: column 4**

> yc = 2.0 → t = 1.5 → row = 1, f = 0.5
> pixel (4, 1) gets **0.5**, pixel (4, 2) gets **0.5** — exactly halfway, an even split

Our program prints all the pixels of this line:

```
Wu line from (0.5, 0.5) to (8.5, 3.5):
  (0, 0) 1
  (1, 0) 0.625
  (1, 1) 0.375
  (2, 0) 0.25
  (2, 1) 0.75
  (3, 1) 0.875
  (3, 2) 0.125
  (4, 1) 0.5
  (4, 2) 0.5
  (5, 1) 0.125
  (5, 2) 0.875
  (6, 2) 0.75
  (6, 3) 0.25
  (7, 2) 0.375
  (7, 3) 0.625
```

(Column 0 has f = 0: its second pixel gets 0, so the program does not print it.) In every column, the two coverages add up to **exactly 1**.

### Why is this a coverage?

Imagine the line as a short **vertical** stick in each column, exactly 1 pixel tall, centred at yc. It reaches from yc − 0.5 to yc + 0.5, which is from **row + f** to **row + 1 + f**.

```
  row:      ┌────────┐ ← top of pixel (x, row) is at height row
            │        │
            │▓▓▓▓▓▓▓▓│ ← the stick starts at row + f
  row + 1:  ├────────┤
            │▓▓▓▓▓▓▓▓│ ← the stick ends at row + 1 + f
            │        │
            └────────┘
```

- The stick covers pixel (x, row) from row + f to row + 1: a height of **1 − f**.
- It covers pixel (x, row + 1) from row + 1 to row + 1 + f: a height of **f**.

So Wu's numbers are exactly the **coverage** of each pixel by this stick.

📖 **New word: box filter** — measuring coverage with a simple box shape, like our stick. Wu's line is a line drawn with a "1-pixel-tall box" in every column.

### Wu and Bresenham

The program also prints the line as digits (9 = full coverage), next to Bresenham's line between the same pixels:

```
the same, as digits (9 = full):          Bresenham from (0, 0) to (8, 3):
  962......                                ##.......
  .37851...                                ..##.....
  ...15873.                                ....###..
  ......26.                                .......#.
  .........                                .........
```

In every column, Bresenham's pixel is the one where Wu puts **more** colour (and where Wu splits exactly 0.5 / 0.5, in column 4, Bresenham had to pick one). So Bresenham is Wu's line **rounded** to the nearer pixel, and Wu's line is Bresenham with the rounding taken out.

---

## 28.4 Steep lines

For a **steep** line (more down than across), stepping along x would leave gaps — the same problem as Chapter 20. The fix is the same: swap the roles of x and y.

1. If |y1 − y0| > |x1 − x0|, the line is steep: **swap x and y** in both end points. Now it is shallow.
2. Do Wu's algorithm as before, column by column.
3. When storing each pixel, **swap back**: the "column" is really a row, and the "row" is really a column.

🔢 **Maths: the steep line from (0.5, 0.5) to (3.5, 8.5)**

> steep: |8| > |3| → swap → from (0.5, 0.5) to (8.5, 3.5) — our shallow line from before!
> its pixel (1, 0) with 0.625 becomes pixel **(0, 1)** with 0.625, and so on

So a steep line is the mirror image (across the diagonal) of a shallow one, and gets exactly the same coverage numbers.

We also make sure the line goes **left to right** (swap A and B if needed), so the loop over columns can count upwards.

---

## 28.5 The ends of the line

Which columns do we draw? Those whose centres lie between the two end points. As everywhere in this book, we use a **half-open** range:

> columns from **ceil(x0 − 0.5)** up to, but not including, **ceil(x1 − 0.5)**

(the same rule as Chapter 19: the column x is used if x0 ≤ x + 0.5 < x1).

🔢 **Maths: from x0 = 0.5 to x1 = 8.5**

> first column = ceil(0.5 − 0.5) = 0, stop before ceil(8.5 − 0.5) = 8 → **columns 0 … 7**

So the end column (8) is **left out** — like `drawLine(…, includeLast = false)` in Chapter 21.

📖 **New word: polyline** — a chain of lines, each starting where the last ended.

The half-open range is what we want for a polyline: the joint column belongs to the **next** line only, so it is not painted twice (which would make the joints darker — conflation again, Chapter 27). This works perfectly when all the lines in the chain go left to right and are shallow, like most graphs. At a joint where the chain turns from shallow to steep, a pixel can still get paint twice — a small, usually invisible, darker dot.

💡 Wu's original algorithm also handles **fractional** end points more carefully: the first and last columns get only part of the brightness, depending on how much of the column the line really covers. Our simpler version is enough for drawing, and keeps the code short.

---

## 28.6 Diagonal lines look lighter

In every column, Wu's two coverages add up to exactly **1**. That sounds right — but is it?

Think of a line that is truly 1 pixel **thick** (measured at a right angle to the line, as in Chapter 27). For a horizontal line, one column of it has an area of 1 × 1 = **1**. For a 45° line, the band is 1 pixel thick at a right angle, but in a single **column** it is taller: the vertical height of a band of thickness 1 at 45° is:

> height = 1 / cos(45°) = √2 ≈ **1.414**

(You can see it with Pythagoras: going along the band's thickness by 1 at 45° means going 0.707 across and 0.707 up; to stay in one column, the band's vertical cut is 0.707 + 0.707 = 1.414.)

So a true 1-pixel line at 45° has **1.414** units of light per column — but Wu gives only **1**. Wu's diagonal lines look about 30 % lighter (1 / 1.414 ≈ 0.71) than horizontal ones. The same is true for Bresenham lines (Chapter 20, Example 4: one pixel per column, whatever the angle).

The program measures the light in one column of a 45° line, by adding up the **linear** light of the pixels (white on black, so the linear value of each pixel is its coverage):

```
light in column 15 of a 45-degree line: Wu 1, supersampled band 1.24701
```

- **Wu**: exactly 1, as expected.
- **The supersampled band** of Chapter 27 (`fillThickLineAA`, thickness 1): 1.247 — more than Wu, but less than the true 1.414. Why not 1.414? This is the "weak spot" of regular sample grids from Chapter 27, Section 27.4. At exactly 45°, the 4 × 4 samples of every pixel lie on diagonal lines 0.25 apart, all parallel to our band. A band 1.414 wide contains exactly **5** of these diagonals, so the samples "see" 5 × 0.25 = **1.25** — and rounding the colours to bytes makes it 1.247.

💡 Is Wu "wrong"? Not really: it is a different, simpler idea of thickness (1 pixel measured **vertically**). For most drawings, nobody notices. If you need lines that look equally strong at every angle, use the thick-band method of Chapter 27 (with more samples), or make Wu's coverage bigger for steep angles: multiply it by √(1 + g²) (Practice 6).

---

## 28.7 Blend in linear light (again)

Wu's coverages are coverages like any others, so we blend them with `paintCoverage` from Chapter 27 — in **linear light**.

🔢 **Maths: column 4 of our line, black on white**

> each of the two pixels gets coverage 0.5 of black: light = 0.5 → file number about **188**
> if we blended the file numbers instead: 255 × 0.5 = 128 — much too dark

With file-number blending, the line would look much darker and "beaded" where it splits 50 / 50 (two dark grey pixels in a column look darker than one black pixel), and thinner where it falls on one pixel. In linear light, the total light of every column is the same, and the line looks even.

---

## 28.8 Smooth circle outlines

The same idea works for any curve, as long as we can find **where** the curve crosses each column (or row). For a circle with centre (cx, cy) and radius r, the circle crosses column x at:

> dx = (x + 0.5) − cx → **y = cy ± √(r² − dx²)** (the top and the bottom of the circle)

and crosses row y at:

> dy = (y + 0.5) − cy → **x = cx ± √(r² − dy²)** (the left and the right side)

Remember Chapter 22: to avoid gaps, step along the direction that changes the most. The circle is **shallow** (step columns) near its top and bottom, and **steep** (step rows) near its left and right sides. They meet at the four 45° points, where:

> |dx| = |dy| = r / √2 (Pythagoras: dx² + dy² = r² and dx = dy → 2dx² = r²)

So `drawCircleWu` has two loops:

1. **Columns** with |dx| ≤ r/√2: find the top and bottom crossing, and split each between two **rows** (`plotSplitRow`).
2. **Rows** with |dy| < r/√2: find the left and right crossing, and split each between two **columns** (`plotSplitColumn`).

🔢 **Maths: r = 10, centre (300.5, 100.5), the column through the centre**

> dx = 0 → y = 100.5 ± 10 → 90.5 and 110.5
> top: t = 90.5 − 0.5 = 90 → row 90 gets 1, row 91 gets 0 → a single full pixel, exactly on the circle

> the column one step right: dx = 1 → √(100 − 1) = 9.950 → top at y = 100.5 − 9.950 = 90.550
> t = 90.05 → row 90 gets 0.95, row 91 gets 0.05

⚠️ **Near the 45° points**, the last column of loop 1 and the last row of loop 2 can touch the same pixel. We counted it: for some radii (like 10, 26, 58 and 74), exactly **4** pixels get paint from both loops — one at each 45° point — and for others (42, 90), none. Those few pixels are a little darker. Practice 7 asks you to think about a fix.

`wu_rings.ppm` shows six circles drawn with `drawCircle` (Chapter 22) on the left, and the same six with `drawCircleWu` on the right. The right ones look round and smooth, without the little steps.

---

## 28.9 Which method when?

Part 4 is now complete. Here are all our ways to draw shapes and lines:

| method | chapter | edges | speed | best for |
|---|---|---|---|---|
| `fillRect`, `fillCircle`, `fillEllipse`, `fillTriangle`, `fillPolygon` | 19, 22–25 | hard (yes/no) | fastest | pixel art, masks, very small or very big shapes where the edge does not matter |
| `drawLine` (Bresenham), `drawCircle`, `drawEllipse` | 21–23 | hard, 1 pixel | fastest | pixel art, exact pixel work, flood-fill outlines |
| `drawLineWu`, `drawCircleWu` | 28 | smooth, 2 pixels per step | very fast | graphs, thin outlines, drawings with many lines |
| `fillCircleAA`, `fillEllipseAA`, `fillPolygonAA`, `fillThickLineAA` | 27 | smooth, any shape | slower (16 samples per edge pixel) | filled shapes, thick lines, text, anything with even-looking edges |
| draw big, then `shrinkAverage` | 27 | smooth | slowest, uses most memory | when you already have only yes/no drawing functions |

🧠 **Remember the one big idea of Part 4:** a pixel is a small square, not a point. Hard edges ask "is the centre inside?"; smooth edges ask "**how much** of the square is inside?" — and then blend in linear light.

---

## Code, part 1: `wu.h`

File: `common/wu.h` (new). It includes `antialias.h` (for `paintCoverage`, and through it everything before).

```cpp
#ifndef WU_H
#define WU_H

#include <algorithm>
#include <cmath>
#include <vector>
#include "antialias.h"

struct CoveragePixel {
    int x = 0;
    int y = 0;
    double coverage = 0.0;
};

inline std::vector<CoveragePixel> wuLinePixels(PointF a, PointF b) {
    std::vector<CoveragePixel> pixels;
    bool steep = std::fabs(b.y - a.y) > std::fabs(b.x - a.x);
    if (steep) {
        std::swap(a.x, a.y);
        std::swap(b.x, b.y);
    }
    if (a.x > b.x) {
        std::swap(a, b);
    }
    double dx = b.x - a.x;
    if (dx == 0.0) {
        return pixels;
    }
    double gradient = (b.y - a.y) / dx;
    int xStart = static_cast<int>(std::ceil(a.x - 0.5));
    int xEnd = static_cast<int>(std::ceil(b.x - 0.5));
    for (int x = xStart; x < xEnd; ++x) {
        double yc = a.y + gradient * ((x + 0.5) - a.x);
        double t = yc - 0.5;
        int row = static_cast<int>(std::floor(t));
        double f = t - row;
        if (steep) {
            pixels.push_back(CoveragePixel{row, x, 1.0 - f});
            pixels.push_back(CoveragePixel{row + 1, x, f});
        } else {
            pixels.push_back(CoveragePixel{x, row, 1.0 - f});
            pixels.push_back(CoveragePixel{x, row + 1, f});
        }
    }
    return pixels;
}

inline void drawLineWu(Image& image, PointF a, PointF b, Colour c) {
    for (const CoveragePixel& p : wuLinePixels(a, b)) {
        paintCoverage(image, p.x, p.y, c, p.coverage);
    }
}

inline void drawPolylineWu(Image& image, const std::vector<PointF>& points, Colour c) {
    const int n = static_cast<int>(points.size());
    for (int i = 0; i + 1 < n; ++i) {
        drawLineWu(image, points[i], points[i + 1], c);
    }
}

inline void plotSplitRow(Image& image, int x, double yc, Colour c) {
    double t = yc - 0.5;
    int row = static_cast<int>(std::floor(t));
    double f = t - row;
    paintCoverage(image, x, row, c, 1.0 - f);
    paintCoverage(image, x, row + 1, c, f);
}

inline void plotSplitColumn(Image& image, double xc, int y, Colour c) {
    double t = xc - 0.5;
    int column = static_cast<int>(std::floor(t));
    double f = t - column;
    paintCoverage(image, column, y, c, 1.0 - f);
    paintCoverage(image, column + 1, y, c, f);
}

inline void drawCircleWu(Image& image, double cx, double cy, double r, Colour c) {
    if (r <= 0.0) {
        return;
    }
    const double limit = r / std::sqrt(2.0);
    int first = static_cast<int>(std::floor(cx - limit - 0.5));
    int last = static_cast<int>(std::ceil(cx + limit));
    for (int x = first; x <= last; ++x) {
        double dx = (x + 0.5) - cx;
        if (std::fabs(dx) > limit) {
            continue;
        }
        double h = std::sqrt(r * r - dx * dx);
        plotSplitRow(image, x, cy - h, c);
        plotSplitRow(image, x, cy + h, c);
    }
    first = static_cast<int>(std::floor(cy - limit - 0.5));
    last = static_cast<int>(std::ceil(cy + limit));
    for (int y = first; y <= last; ++y) {
        double dy = (y + 0.5) - cy;
        if (std::fabs(dy) >= limit) {
            continue;
        }
        double w = std::sqrt(r * r - dy * dy);
        plotSplitColumn(image, cx - w, y, c);
        plotSplitColumn(image, cx + w, y, c);
    }
}

#endif
```

### Line by line

**The start (lines 1–13)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef WU_H` / `#define WU_H` | Include guard. |
| 4–6 | `#include <algorithm>` / `<cmath>` / `<vector>` | `std::swap`; `std::fabs`, `std::floor`, `std::ceil`, `std::sqrt`; vectors. |
| 7 | `#include "antialias.h"` | `paintCoverage` (Chapter 27) and everything before. |
| 9–13 | `struct CoveragePixel { int x = 0; int y = 0; double coverage = 0.0; };` | One pixel and how much of it the line covers. We collect these in a list, so the program can print them before painting. |

**The pixels of a Wu line (lines 15–46)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 15 | `inline std::vector<CoveragePixel> wuLinePixels(PointF a, PointF b) {` | Compute (but do not paint) all the pixels of the smooth line from a to b. |
| 16 | `std::vector<CoveragePixel> pixels;` | The answer, empty at first. |
| 17 | `bool steep = std::fabs(b.y - a.y) > std::fabs(b.x - a.x);` | More down than across? (Section 28.4) `std::fabs` is the size of a `double` without its sign. |
| 18–21 | `if (steep) { std::swap(a.x, a.y); std::swap(b.x, b.y); }` | For a steep line, swap x and y in both points: now the line is shallow. |
| 22–24 | `if (a.x > b.x) { std::swap(a, b); }` | Make the line go left to right. |
| 25–28 | `double dx = b.x - a.x; if (dx == 0.0) { return pixels; }` | dx is 0 only if a and b are the same point (after the swap, |dx| is the bigger size): no line. This also protects the division below. |
| 29 | `double gradient = (b.y - a.y) / dx;` | The slope g (Section 28.2), between −1 and 1. |
| 30–31 | `int xStart = static_cast<int>(std::ceil(a.x - 0.5));` / `int xEnd = ...ceil(b.x - 0.5)...;` | The half-open range of columns whose centres lie from a.x up to b.x (Section 28.5). |
| 32 | `for (int x = xStart; x < xEnd; ++x) {` | Every column. |
| 33 | `double yc = a.y + gradient * ((x + 0.5) - a.x);` | The line's height at the column centre. |
| 34–36 | `double t = yc - 0.5;` / `int row = static_cast<int>(std::floor(t));` / `double f = t - row;` | The pixel just above the line (`row`) and the fraction part f (Section 28.3). |
| 37–39 | `if (steep) { pixels.push_back(CoveragePixel{row, x, 1.0 - f}); pixels.push_back(CoveragePixel{row + 1, x, f}); }` | For a steep line, swap back: `x` is really the row, and `row` is really the column. |
| 40–43 | `} else { pixels.push_back(CoveragePixel{x, row, 1.0 - f}); pixels.push_back(CoveragePixel{x, row + 1, f}); }` | For a shallow line: the two pixels of this column, with coverage 1 − f and f. |
| 44–46 | `}` `return pixels;` `}` | Done. |

**Drawing lines (lines 48–59)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 48 | `inline void drawLineWu(Image& image, PointF a, PointF b, Colour c) {` | Draw a smooth line. |
| 49–51 | `for (const CoveragePixel& p : wuLinePixels(a, b)) { paintCoverage(image, p.x, p.y, c, p.coverage); }` | Paint every pixel of the list with its coverage, in linear light. (A coverage of 0 is skipped inside `paintCoverage`; pixels outside the image are ignored by `setPixel` and `blendPixel`.) |
| 54 | `inline void drawPolylineWu(Image& image, const std::vector<PointF>& points, Colour c) {` | Draw a chain of smooth lines (Section 28.5). |
| 55–58 | `const int n = ...; for (int i = 0; i + 1 < n; ++i) { drawLineWu(image, points[i], points[i + 1], c); }` | One line from each point to the next. |

**Splitting between two pixels (lines 61–75)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 61 | `inline void plotSplitRow(Image& image, int x, double yc, Colour c) {` | In column x, split one unit of colour between the two rows nearest to the height yc. |
| 62–64 | `double t = yc - 0.5;` … `double f = t - row;` | The same three lines as in `wuLinePixels`. |
| 65–66 | `paintCoverage(image, x, row, c, 1.0 - f);` / `paintCoverage(image, x, row + 1, c, f);` | Paint both pixels. |
| 69–75 | `inline void plotSplitColumn(Image& image, double xc, int y, Colour c) { ... }` | The same idea turned sideways: in row y, split between the two **columns** nearest to xc. |

**A smooth circle outline (lines 77–104)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 77–80 | `inline void drawCircleWu(Image& image, double cx, double cy, double r, Colour c) { if (r <= 0.0) { return; }` | A smooth circle outline with any centre and radius (Section 28.8). |
| 81 | `const double limit = r / std::sqrt(2.0);` | The distance of the 45° points from the centre lines: r/√2. |
| 82–83 | `int first = ...floor(cx - limit - 0.5)...;` / `int last = ...ceil(cx + limit)...;` | A range of columns a little wider than needed; the exact test is inside the loop. |
| 84–88 | `for (int x = first; x <= last; ++x) { double dx = (x + 0.5) - cx; if (std::fabs(dx) > limit) { continue; }` | Loop 1: every column whose centre is within the shallow part. |
| 89 | `double h = std::sqrt(r * r - dx * dx);` | How far above and below the centre the circle crosses this column. (dx² ≤ r²/2 here, so the square root is never of a negative number.) |
| 90–91 | `plotSplitRow(image, x, cy - h, c);` / `plotSplitRow(image, x, cy + h, c);` | The top crossing and the bottom crossing. |
| 92 | `}` | End of loop 1. |
| 93–94 | `first = ...floor(cy - limit - 0.5)...;` / `last = ...ceil(cy + limit)...;` | The range of rows, reusing the two variables. |
| 95–99 | `for (int y = first; y <= last; ++y) { double dy = (y + 0.5) - cy; if (std::fabs(dy) >= limit) { continue; }` | Loop 2: every row strictly inside the steep part. (`>=` here and `>` in loop 1, so a crossing exactly at 45° is drawn only once.) |
| 100–102 | `double w = std::sqrt(r * r - dy * dy);` … `plotSplitColumn(image, cx + w, y, c);` | The left and right crossings, split between columns. |
| 103–104 | `}` `}` | End. |
| 106 | `#endif` | End of the include guard. |

---

## Code, part 2: Wu lines, rings and a graph

File: `ch28/wu.cpp`

```cpp
#include <iostream>
#include <string>
#include <vector>
#include "wu.h"

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

void printCoverageGrid(const std::string& title, const std::vector<CoveragePixel>& pixels,
                       int width, int height) {
    std::vector<double> grid(width * height, 0.0);
    for (const CoveragePixel& p : pixels) {
        if (p.x >= 0 && p.x < width && p.y >= 0 && p.y < height) {
            grid[p.y * width + p.x] += p.coverage;
        }
    }
    std::cout << title << ":\n";
    for (int y = 0; y < height; ++y) {
        std::cout << "  ";
        for (int x = 0; x < width; ++x) {
            int digit = static_cast<int>(grid[y * width + x] * 9.0 + 0.5);
            if (digit == 0) {
                std::cout << '.';
            } else {
                std::cout << digit;
            }
        }
        std::cout << "\n";
    }
}

double columnLight(const Image& img, int x) {
    double sum = 0.0;
    for (int y = 0; y < img.height(); ++y) {
        sum += toLinear(img.getPixel(x, y)).r;
    }
    return sum;
}

int main() {
    std::vector<CoveragePixel> wu = wuLinePixels(PointF{0.5, 0.5}, PointF{8.5, 3.5});
    std::cout << "Wu line from (0.5, 0.5) to (8.5, 3.5):\n";
    for (const CoveragePixel& p : wu) {
        if (p.coverage > 0.0) {
            std::cout << "  (" << p.x << ", " << p.y << ") " << p.coverage << "\n";
        }
    }
    printCoverageGrid("the same, as digits (9 = full)", wu, 9, 5);
    Image bresenham(9, 5);
    drawLine(bresenham, 0, 0, 8, 3, colours::white, false);
    printGrid("Bresenham from (0, 0) to (8, 3), last pixel left out", bresenham);

    Image wuDiagonal(30, 30);
    drawLineWu(wuDiagonal, PointF{2.0, 2.0}, PointF{28.0, 28.0}, colours::white);
    Image bandDiagonal(30, 30);
    fillThickLineAA(bandDiagonal, PointF{2.0, 2.0}, PointF{28.0, 28.0}, 1.0, colours::white);
    std::cout << "light in column 15 of a 45-degree line: Wu " << columnLight(wuDiagonal, 15)
              << ", supersampled band " << columnLight(bandDiagonal, 15) << "\n";

    Image spokes(600, 200, colours::white);
    for (int k = 0; k < 10; ++k) {
        int ex = 10 + 20 * k;
        drawLine(spokes, 100, 100, ex, 10, colours::black);
        drawLine(spokes, 100, 100, ex, 190, colours::black);
        drawLineWu(spokes, PointF{300.5, 100.5}, PointF{ex + 200.5, 10.5}, colours::black);
        drawLineWu(spokes, PointF{300.5, 100.5}, PointF{ex + 200.5, 190.5}, colours::black);
        fillThickLineAA(spokes, PointF{500.5, 100.5}, PointF{ex + 400.5, 10.5}, 1.0,
                        colours::black);
        fillThickLineAA(spokes, PointF{500.5, 100.5}, PointF{ex + 400.5, 190.5}, 1.0,
                        colours::black);
    }

    Image rings(400, 200, colours::white);
    for (int r = 10; r <= 90; r += 16) {
        drawCircle(rings, 100, 100, r, Colour{30, 60, 160});
        drawCircleWu(rings, 300.5, 100.5, r, Colour{30, 60, 160});
    }

    Image graph(400, 300, colours::white);
    drawLine(graph, 20, 150, 380, 150, Colour{180, 180, 180});
    drawLine(graph, 200, 10, 200, 290, Colour{180, 180, 180});
    std::vector<PointF> parabola;
    std::vector<PointF> cubic;
    for (int x = 20; x <= 380; x += 5) {
        double u = x - 200.0;
        parabola.push_back(PointF{x + 0.5, 280.0 - u * u / 150.0});
        cubic.push_back(PointF{x + 0.5, 150.0 + u * u * u / 40000.0});
    }
    drawPolylineWu(graph, parabola, Colour{30, 60, 200});
    drawPolylineWu(graph, cubic, Colour{200, 40, 40});

    bool ok = spokes.savePPM("wu_spokes.ppm");
    ok = ok && rings.savePPM("wu_rings.ppm");
    ok = ok && graph.savePPM("graph.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
```

Build and run (from the `code/ch28` folder):

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common wu.cpp -o wu
./wu
```

### Line by line

**Helpers (lines 1–48)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–4 | the `#include` lines | Printing, text, vectors, and our new header. |
| 6–17 | `printGrid` | The same as in earlier chapters. |
| 19–20 | `void printCoverageGrid(const std::string& title, const std::vector<CoveragePixel>& pixels, int width, int height) {` | Print a list of coverage pixels as a grid of digits. |
| 21 | `std::vector<double> grid(width * height, 0.0);` | A grid of coverages, all 0, stored row by row (index y × width + x, Chapter 6). |
| 22–26 | `for (const CoveragePixel& p : pixels) { if (...inside the grid...) { grid[p.y * width + p.x] += p.coverage; } }` | Add every pixel's coverage into the grid (`+=`, in case a pixel appears twice). |
| 27–39 | the printing loops with `int digit = static_cast<int>(grid[...] * 9.0 + 0.5);` | Print 0 … 9 (rounded), with `.` for 0 — the same as Chapter 27's coverage map. |
| 42–48 | `double columnLight(const Image& img, int x) { ... sum += toLinear(img.getPixel(x, y)).r; ... }` | Add up the **linear** red light of one column (Section 28.6). For white on black, each pixel's linear value is its coverage. |

**The text output (lines 50–68)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 51 | `std::vector<CoveragePixel> wu = wuLinePixels(PointF{0.5, 0.5}, PointF{8.5, 3.5});` | The line of Sections 28.2 and 28.3. |
| 52–57 | `std::cout << "Wu line ..."; for (...) { if (p.coverage > 0.0) { std::cout << ... } }` | Print each pixel with a coverage above 0. |
| 58 | `printCoverageGrid("the same, as digits (9 = full)", wu, 9, 5);` | The same as a picture of digits. |
| 59–61 | `Image bresenham(9, 5);` / `drawLine(bresenham, 0, 0, 8, 3, colours::white, false);` / `printGrid(...)` | Bresenham between the same pixels, last pixel left out to match Wu's half-open columns. |
| 63–64 | `Image wuDiagonal(30, 30);` / `drawLineWu(wuDiagonal, PointF{2.0, 2.0}, PointF{28.0, 28.0}, colours::white);` | A 45° Wu line, white on black. |
| 65–66 | `Image bandDiagonal(30, 30);` / `fillThickLineAA(bandDiagonal, ..., 1.0, colours::white);` | The same line as a supersampled band, 1 pixel thick (Chapter 27). |
| 67–68 | `std::cout << "light in column 15 ..."` | Compare the light in one column (Section 28.6). |

**The pictures (lines 70–110)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 70 | `Image spokes(600, 200, colours::white);` | Three panels, 200 pixels wide each. |
| 71–72 | `for (int k = 0; k < 10; ++k) { int ex = 10 + 20 * k;` | The same 20 spokes as Chapter 27. |
| 73–74 | two `drawLine` calls | Left panel: Bresenham. |
| 75–76 | two `drawLineWu` calls | Middle panel: Wu. The `.5` makes the end points pixel **centres**, so the line goes from the centre of pixel (300, 100) to the centre of an edge pixel. |
| 77–80 | two `fillThickLineAA` calls | Right panel: the supersampled band, thickness 1. |
| 83–87 | `Image rings(400, 200, colours::white);` and the loop | Six circles (radius 10, 26, 42, 58, 74, 90), with `drawCircle` on the left and `drawCircleWu` on the right. |
| 89–91 | `Image graph(400, 300, colours::white);` and two grey `drawLine` calls | A graph with two axes. |
| 92–93 | `std::vector<PointF> parabola;` / `std::vector<PointF> cubic;` | Two lists of points. |
| 94–98 | `for (int x = 20; x <= 380; x += 5) { double u = x - 200.0; parabola.push_back(...); cubic.push_back(...); }` | Every 5 pixels, a point of each curve. u is the distance from the middle. The parabola is y = 280 − u² / 150 (a "U" shape, lowest at the middle — remember y goes down, so a bigger y is lower on the screen). The cubic is y = 150 + u³ / 40000 (an "S"-like curve through the middle of the graph). |
| 99–100 | two `drawPolylineWu` calls | Draw both curves as smooth chains of short lines: blue and red. |
| 102–110 | saving | `wu_spokes.ppm`, `wu_rings.ppm`, `graph.ppm`. |

### What you should see

The program prints the line's pixels (Section 28.3), the digit grid and the Bresenham grid (Section 28.3), and:

```
light in column 15 of a 45-degree line: Wu 1, supersampled band 1.24701
```

Open the pictures:
- `wu_spokes.ppm`: three fans of 20 lines. Left (Bresenham): jagged. Middle (Wu): smooth. Right (supersampled band): also smooth; the diagonal spokes look a little darker than Wu's, as Section 28.6 predicts.
- `wu_rings.ppm`: six blue rings twice. The right ones (Wu) look smooth and round.
- `graph.ppm`: a grey cross of axes, a smooth blue "U" curve and a smooth red "S" curve. (This is the smooth version of the graph of y = x² from Chapter 13, finally without gaps.)

---

## Small examples

### Example 1 — One column by hand

A line from (2.0, 5.0) to (12.0, 9.0), column 6:

> g = 4 / 10 = 0.4
> yc = 5.0 + 0.4 × (6.5 − 2.0) = 5.0 + 1.8 = 6.8
> t = 6.3 → row 6, f = 0.3 → pixel (6, 6) gets **0.7**, pixel (6, 7) gets **0.3**

### Example 2 — A horizontal line on a pixel border

From (0, 4.0) to (10, 4.0): every column has yc = 4.0 → t = 3.5 → row 3, f = 0.5. Every column is split **0.5 / 0.5** between rows 3 and 4: a soft, 2-pixel-wide grey line. From (0, 4.5) to (10, 4.5): t = 4 → f = 0 → row 4 gets **1**: a crisp, solid 1-pixel line.

🧠 For crisp horizontal and vertical lines, put them on pixel **centres** (y = k + 0.5).

### Example 3 — The steep swap

A line from (3.5, 0.5) to (5.5, 10.5) is steep (|10| > |2|). After the swap: (0.5, 3.5) to (10.5, 5.5), g = 0.2. Column 5 of the swapped line: yc = 3.5 + 0.2 × 5 = 4.5 → t = 4 → row 4 gets 1. Swapped back: pixel **(4, 5)** gets 1 — in row 5, the line is exactly on the centre of column 4.

### Example 4 — How many pixels does a Wu line paint?

A shallow line 100 columns wide paints **2 pixels per column**: 200 pixels (some with coverage 0). A Bresenham line paints 100. A supersampled band of thickness 1 paints about 200–300 pixels, and tests 16 samples in most of them.

### Example 5 — Coverage that adds up

In any column of a shallow Wu line: (1 − f) + f = **1**. In any row of the steep part of a Wu circle: also 1 per crossing. So the total "ink" of a Wu line is exactly its number of columns — easy to predict.

---

## Common mistakes

⚠️ **Forgetting the − 0.5.** If you split around yc instead of yc − 0.5, every line is shifted half a pixel down, and a line exactly on a pixel centre gets split 50 / 50 instead of being solid.

⚠️ **Not swapping for steep lines.** Steep lines then have big gaps (only one pair of pixels per column) — the same problem as Chapter 20.

⚠️ **Swapping x and y but forgetting to swap back** when storing the pixels. The line appears mirrored across the diagonal.

⚠️ **Blending file numbers.** 50 / 50 columns look too dark and the line looks "beaded". Blend in linear light (`paintCoverage`).

⚠️ **Using `int` points.** Wu's line is defined for fractional coordinates; converting the ends to `int` throws away exactly the information that makes it smooth.

⚠️ **Expecting equal brightness at all angles.** Wu's diagonals are about 30 % lighter than true 1-pixel lines.

---

## Practice

🏋️ **1.** Compute the two pixels and their coverages for column 3 of the line from (1.0, 2.0) to (9.0, 6.0).

🏋️ **2.** Which pixels does the Wu line from (0.5, 2.5) to (4.5, 2.5) paint, and with what coverage? And the line from (0.5, 2.0) to (4.5, 2.0)?

🏋️ **3.** For the steep line from (2.5, 1.5) to (4.5, 9.5), find the pixels of row 5.

🏋️ **4.** Draw a smooth triangle outline with three `drawLineWu` calls. Look at the corners: what happens there?

🏋️ **5.** Use `drawPolylineWu` to draw a smooth "zig-zag" of 10 segments across a 300 × 100 picture.

🏋️ **6.** Make `drawLineWu` lines look equally strong at all angles by multiplying each coverage by √(1 + g²) (and clamping it at 1). What factor do you get for g = 0, g = 0.5 and g = 1?

🏋️ **7.** (Thinking) In `drawCircleWu`, up to 4 pixels near the 45° points are painted by both loops. Suggest a way to avoid it.

🏋️ **8.** Draw a smooth **ellipse** outline in the Wu style. Where are the "45° points" of an ellipse? (Hint: Chapter 23, Section 23.6.)

---

## Answers

**1.**
> g = (6 − 2) / (9 − 1) = 0.5
> yc = 2.0 + 0.5 × (3.5 − 1.0) = 2.0 + 1.25 = 3.25
> t = 2.75 → row 2, f = 0.75 → pixel (3, 2) gets **0.25**, pixel (3, 3) gets **0.75**

(The line at 3.25 is closer to the centre of row 3 (3.5) than to the centre of row 2 (2.5) ✓.)

**2.**
> From (0.5, 2.5) to (4.5, 2.5): columns 0 … 3, yc = 2.5 → t = 2 → f = 0 → pixels (0, 2), (1, 2), (2, 2), (3, 2) with coverage **1** each (and row 3 with 0). A crisp line.
> From (0.5, 2.0) to (4.5, 2.0): yc = 2.0 → t = 1.5 → f = 0.5 → each column: rows 1 and 2 with **0.5** each. A soft 2-pixel line.

**3.**
> steep (|8| > |2|) → swap → (1.5, 2.5) to (9.5, 4.5), g = 2 / 8 = 0.25
> "column" 5 of the swapped line: yc = 2.5 + 0.25 × (5.5 − 1.5) = 2.5 + 1.0 = 3.5 → t = 3 → row 3, f = 0
> swapped back: pixel **(3, 5)** gets coverage **1** (and (4, 5) gets 0)

**4.**

```cpp
PointF a{20.5, 80.5};
PointF b{150.5, 20.5};
PointF c{180.5, 140.5};
drawLineWu(img, a, b, colours::black);
drawLineWu(img, b, c, colours::black);
drawLineWu(img, c, a, colours::black);
```

At the corners, the lines' half-open ranges do not always fit together, because the three lines go in different directions (after the left-to-right swap, a line may start where the previous one ended **or** end there). So a corner pixel can get paint from two lines (a little darker), or a corner can look slightly cut short. For thin outlines this is hard to see.

**5.**

```cpp
std::vector<PointF> zigzag;
for (int i = 0; i <= 10; ++i) {
    double x = 10.5 + i * 28.0;
    double y = (i % 2 == 0) ? 80.5 : 20.5;
    zigzag.push_back(PointF{x, y});
}
drawPolylineWu(img, zigzag, colours::black);
```

Each segment goes 28 across and 60 up or down: steep (|60| > |28|), so `wuLinePixels` swaps x and y for each one.

**6.**
> g = 0: √1 = **1** (horizontal lines stay the same)
> g = 0.5: √1.25 ≈ **1.118**
> g = 1: √2 ≈ **1.414** (45° lines get 41 % more coverage)

√(1 + g²) is exactly the length of the line in one column (one step across and g steps down — Pythagoras), which is why it fixes the brightness. With the factor, a 50 / 50 split at 45° becomes 0.707 / 0.707; but a split of 0.9 / 0.1 would become 1.27 / 0.14, so we must clamp at 1, losing a little.

**7.** One way: let loop 2 skip the **pixels** (not only the rows) that loop 1 has already painted. Loop 1 ends at the column with |dx| just below r/√2; for rows near the 45° points, check whether the column that `plotSplitColumn` would paint is one that loop 1 covered (|column + 0.5 − cx| ≤ r/√2), and paint only the other one. Another way: collect all coverages in a grid first (like `printCoverageGrid` does), take the **larger** value where two loops meet, and paint once.

**8.** For an ellipse, the "45° points" are where the slope is −1: b²|x| = a²|y| (Chapter 23, Section 23.6). So loop 1 (columns, crossings y = cy ± b√(1 − (dx/a)²)) runs while b²|dx| ≤ a²|y-offset|, and loop 2 (rows, crossings x = cx ± a√(1 − (dy/b)²)) runs for the other rows. For a = 6, b = 3, the switch is at about x = 5.37, y = 1.34 (Chapter 23). Instead of the circle's single limit r/√2, there are two limits:

> column limit: |dx| ≤ a² / √(a² + b²)
> row limit: |dy| < b² / √(a² + b²)

(For a = b = r, both become r² / (r√2) = r / √2 ✓.)

---

## Summary

🧠 **Wu's line**: in each column, find the exact height yc of the line; split one unit of colour between the two nearest pixels: t = yc − 0.5, row = floor(t), f = t − row → **(1 − f)** and **f**.

🧠 The split **is** a coverage: a 1-pixel-tall "box" centred on the line.

🧠 Bresenham is Wu **rounded**: it picks the pixel with the bigger share.

🧠 Steep lines: swap x and y, compute, swap back. Columns: half-open, ceil(x0 − 0.5) to ceil(x1 − 0.5).

🧠 Every column gets total coverage 1, so Wu's diagonal lines are about **30 % lighter** than true 1-pixel lines.

🧠 Blend Wu's coverage in **linear light**.

🧠 **Wu circles**: step columns where the circle is shallow and rows where it is steep; switch at **r/√2**.

🧠 **Part 4's big idea**: a pixel is a little square. Hard edges test its centre; smooth edges measure **how much** of it is inside.

---

## Next chapter

Part 4 is finished: we can draw every basic shape, hard or smooth. But all our shapes have been standing still, in fixed positions. In **Part 5** we learn to **move, turn and bend** them. It starts with Chapter 29: **2D vectors** — the arrows that describe positions, directions and movements, and the "dot" and "cross" products that we have already secretly used (the edge function of Chapter 24 is one of them!).
