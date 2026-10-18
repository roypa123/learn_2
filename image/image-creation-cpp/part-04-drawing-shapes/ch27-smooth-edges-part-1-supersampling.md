# Chapter 27 — Smooth Edges, Part 1: Supersampling

> **Part 4 · Chapter 27 of 82**
> **You need:** Chapters 1–26 (especially 17, 18, 22 and 25) · **You will make:** `antialias.h` (coverage by sampling, smooth circles, ellipses, polygons and thick lines, "draw big and shrink"), `zoom.ppm`, `stars_aa.ppm` and `spokes.ppm`

---

## What you will learn

- Why the edges of our shapes look like **stairs** ("the jaggies"), and what **aliasing** means.
- What **coverage** is: how much of a pixel a shape really covers.
- How to **estimate** coverage by testing many small **sample** points inside each pixel.
- How many samples we need, and what each extra sample **costs**.
- Why the edge colour must be blended in **linear light**.
- A trick that tests only the pixels on the **edge**, not every pixel.
- How to make **smooth polygons** with the scanline method of Chapter 25.
- Why two smooth triangles side by side can still show a **seam**, and how to avoid it.
- How to draw a smooth **thick line** as a thin polygon.
- The "**draw big, then shrink**" method, and why it gives exactly the same result.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **jaggies** | The stair-step look of a sloped or curved edge made of whole pixels. |
| **aliasing** | When small details are too fine for the pixel grid and turn into wrong, blocky patterns. |
| **anti-aliasing** | Any method that makes edges smooth by using in-between colours. Often written **AA**. |
| **coverage** | The fraction of a pixel's area that is inside a shape: 0 (none) to 1 (all). |
| **sample** | One test point. "Sampling" = testing at many points. |
| **supersampling** | Testing **several** points inside each pixel, instead of only the centre. |
| **subpixel** | A position inside a pixel, between whole pixel positions. |
| **sub-row** | A row of sample points inside a pixel row. |
| **conflation** | Mixing two partial coverages as if they were see-through paint; it makes faint seams. |
| **perpendicular** | At a right angle (90°) to something. |
| **SSAA** | "Supersample anti-aliasing": draw the picture bigger, then shrink it by averaging. |

---

## 27.1 The jaggies

Zoom into any shape we have drawn so far. The edge of a circle looks like a staircase:

```
  .......########......
  .....############....
  ...################..      ← the edge goes in steps:
  ..##################.        each pixel is either fully in
  .####################        or fully out
```

📖 **New word: jaggies** — this stair-step look.

The reason: every pixel asks **one** question — "is my centre inside?" — and gets a yes or a no. A pixel whose centre is just inside becomes fully coloured; its neighbour, just outside, stays fully background. But the true edge passes **through** these pixels. Some of them are half covered, some a quarter, some three quarters. Our yes/no answer throws that away.

📖 **New word: aliasing** — the general name for this problem: the pixel grid is too coarse for the fine detail of the edge, so the detail "pretends" to be something else (stairs). The word comes from "alias", a false name.

📖 **New word: anti-aliasing (AA)** — the cure: give edge pixels **in-between** colours.

---

## 27.2 Coverage

📖 **New word: coverage** — the fraction of the pixel's area (a 1 × 1 square) that is inside the shape.

```
  ┌────────┐      ┌────────┐      ┌────────┐
  │        │      │████    │      │████████│
  │        │      │████    │      │████████│
  │        │      │████    │      │████████│
  └────────┘      └────────┘      └────────┘
  coverage 0     coverage 0.5     coverage 1
```

If we knew the coverage of every pixel, the right colour would be easy. Think of the pixel as a tiny lamp. If half of it shows the shape and half shows the background, the light it sends out is **half** shape-light and **half** background-light. That is exactly an "over" blend with alpha = coverage (Chapter 18):

> **pixel = shape colour × coverage + background × (1 − coverage)** (in linear light)

Chapter 18 already said it: **alpha is coverage**. Our `blendPixel` does this blend.

---

## 27.3 Estimating coverage with samples

Finding the **exact** area of a circle inside a little square needs difficult maths. But there is an easy way to get very close: test **many points** inside the pixel and count how many are inside the shape.

📖 **New word: sample** — one test point.

📖 **New word: supersampling** — testing several sample points in each pixel instead of one.

We use an **n × n grid** of sample points, evenly spread inside the pixel:

> sample (i, j) of pixel (x, y) is at **(x + (i + 0.5) / n, y + (j + 0.5) / n)** for i, j = 0 … n − 1

📖 **New word: subpixel** — a position inside a pixel, like x + 0.375.

🔢 **Maths: the 4 × 4 sample positions inside pixel (9, 2)**

> (i + 0.5) / 4 for i = 0, 1, 2, 3 → **0.125, 0.375, 0.625, 0.875**
> so the x positions are 9.125, 9.375, 9.625, 9.875, and the y positions 2.125, 2.375, 2.625, 2.875

Each sample sits in the **centre** of its own little sub-square — the same pixel-centre idea, one level smaller.

```
   pixel (9, 2), split into 16 sub-squares:
   ┌──┬──┬──┬──┐
   │• │• │• │• │   each • is a sample point
   ├──┼──┼──┼──┤
   │• │• │• │• │
   ├──┼──┼──┼──┤
   │• │• │• │• │
   ├──┼──┼──┼──┤
   │• │• │• │• │
   └──┴──┴──┴──┘
```

> **coverage ≈ (number of samples inside) / n²**

🔢 **Maths: pixel (9, 2) and the circle with centre (5.5, 5.5), radius 5** (the disc of Chapter 22)

The program tests all 16 samples and prints which ones are inside (`#`):

```
samples in pixel (9, 2):
  #...
  ##..
  ##..
  ###.
  coverage 8 / 16
```

The circle's edge cuts diagonally through this pixel (it is in the top-right part of the circle). 8 of 16 samples are inside: coverage ≈ **0.5**.

Check one sample by hand, the top-left one (i = 0, j = 0):

> position (9.125, 2.125)
> dx = 9.125 − 5.5 = 3.625, dy = 2.125 − 5.5 = −3.375
> dx² + dy² = 13.14 + 11.39 = 24.53 ≤ 25 → **inside** ✓ (the `#` in the top-left corner)

And the top-right one (i = 3, j = 0):

> position (9.875, 2.125): dx = 4.375, dy = −3.375 → 19.14 + 11.39 = 30.53 > 25 → **outside** ✓

### How good is the estimate?

We can measure the true coverage of this pixel with a huge number of samples (1000 × 1000 = one million). Here is how the estimate improves:

| samples (n × n) | coverage |
|---|---|
| 1 × 1 (only the centre — what we did before) | 1.0 |
| 2 × 2 | 0.5 |
| 4 × 4 | 0.5 |
| 8 × 8 | 0.484 |
| 16 × 16 | 0.480 |
| 1000 × 1000 (the "true" value) | **0.484** |

With one sample, the pixel is "fully in" — badly wrong. With 16 samples, it is already within 2 % of the truth.

---

## 27.4 How many samples?

With n × n samples, the coverage can only be one of **n² + 1** values: 0/n², 1/n², …, n²/n².

| n | samples per pixel | coverage levels | cost (times more tests) |
|---|---|---|---|
| 1 | 1 | 2 (in or out) | 1 |
| 2 | 4 | 5 | 4 |
| 4 | **16** | **17** | **16** |
| 8 | 64 | 65 | 64 |
| 16 | 256 | 257 | 256 |

More samples = smoother edges, but more work. **n = 4** (16 samples) is a good balance, and it is the default in our functions. You can always pass a bigger n.

⚠️ **A weak spot: nearly horizontal edges.** Look at an edge that is almost flat, going through a row of pixels. Inside one pixel, all the samples in one **row** of the 4 × 4 grid are at the same height, so they are usually all in or all out together. So along such an edge, the coverage only takes **n + 1** = 5 different values (0, 4, 8, 12 or 16 samples), not 17. You can sometimes see faint steps on nearly-horizontal (and nearly-vertical) edges. Better sample patterns — a slightly **rotated** grid, or randomly **jittered** points — fix this. We will make our own random numbers in Chapter 54.

---

## 27.5 Blend in linear light

The coverage tells us how much **light** of each colour the pixel sends out. Light adds up in **linear** values, not in sRGB file numbers (Chapter 17). So we must blend in linear light — and `blendPixel` already does (Chapter 18).

🔢 **Maths: white on black, the 17 levels of a 4 × 4 coverage**

Blending white over black with coverage k / 16, in linear light, gives these file numbers:

| k (samples inside) | 0 | 1 | 2 | 4 | 8 | 12 | 16 |
|---|---|---|---|---|---|---|---|
| coverage | 0 | 0.06 | 0.13 | 0.25 | 0.5 | 0.75 | 1 |
| file number | 0 | 71 | 99 | 137 | **188** | 225 | 255 |

Half coverage gives **188**, not 128. If we blended the file numbers (128 for half), the edges would look too thin and dark on a light shape, and too thick on a dark shape. That is a very common mistake in real programs — and you can see it: text drawn with it looks slightly "bold" or "thin" depending on its colour.

---

## 27.6 Only the edge pixels need samples

Testing 16 samples for every pixel of a big circle is a lot of work — and wasted, because most pixels are **fully** inside or fully outside. Only pixels near the **edge** have partial coverage.

How do we know a pixel is far from the edge? The pixel is a 1 × 1 square. The point inside it that is farthest from its centre is a **corner**, at distance:

> √(0.5² + 0.5²) = √0.5 ≈ **0.7071** (half a diagonal — Pythagoras, Chapter 3)

So, with d = the distance from the circle's centre to the pixel's centre:

- If **d ≤ r − 0.7071**, every point of the pixel is inside the circle (even its farthest corner): coverage = 1. No sampling!
- If **d ≥ r + 0.7071**, every point of the pixel is outside: coverage = 0. No sampling!
- Only in between — a thin ring about 1.4 pixels wide — do we sample.

🔢 **Maths: how many pixels need sampling? (r = 100)**

> the ring is about 2 × 0.7071 ≈ 1.41 pixels wide, and 2π × 100 ≈ 628 pixels long
> ring area ≈ 1.41 × 628 ≈ **890** pixels (sampled, 16 tests each)
> the whole disc has π × 100² ≈ 31,416 pixels
> so only about 3 % of the pixels need sampling

Our `fillCircleAA` uses 0.70711, a tiny bit more than √0.5, to be safe from rounding.

### The coverage of a small disc

The program prints the coverage of every pixel of the Chapter 22 disc (centre (5.5, 5.5), radius 5) as a digit from 0 to 9 (9 = fully covered, `.` = 0):

```
coverage of each pixel, from 0 to 9:
  ...13531...
  ..5999995..
  .599999995.
  19999999991
  39999999993
  59999999995
  39999999993
  19999999991
  .599999995.
  ..5999995..
  ...13531...
```

Compare it with the yes/no disc of Chapter 22: the old "spikes" (single pixels at the top, bottom, left and right) have become soft 5s (half covered) with 3s and 1s next to them. The edge now fades out smoothly instead of stopping in steps.

---

## 27.7 Smooth polygons with sub-rows

For polygons, we use the scanline method of Chapter 25, but with **n sub-rows** in every pixel row.

📖 **New word: sub-row** — one row of sample points: for pixel row y, the sub-rows are at sy = y + (j + 0.5) / n.

For each pixel row:

1. Set a counter to 0 for every pixel in the row.
2. For each of the n sub-rows: find the crossings (exactly as in Chapter 25), sort them, and apply the fill rule. For each inside span [xa, xb), count the samples sx = x + (i + 0.5) / n with xa ≤ sx < xb, and add them to the pixel's counter.
3. After all n sub-rows, each counter holds the number of samples inside (0 to n²). Paint each pixel with coverage = counter / n².

🔢 **Maths: one sub-row crosses a pixel**

> pixel 7, sub-row with an inside span from xa = 7.3 to xb = 12.0
> samples in pixel 7: 7.125, 7.375, 7.625, 7.875
> 7.125 < 7.3 → no; 7.375, 7.625, 7.875 → yes → **3** samples counted for pixel 7 in this sub-row
> pixels 8 to 11: all 4 samples inside → 4 each; pixel 12: 12.125 ≥ 12.0 → none

Everything else — even-odd and non-zero rules, holes, stars — works exactly as before, because each sub-row is just an ordinary scanline.

`stars_aa.ppm` shows the Chapter 25 star twice: on the left with `fillPolygon` (jagged), on the right with `fillPolygonAA` (smooth). The long thin points of the star show the difference best.

---

## 27.8 The seam comes back

In Chapter 24 we solved the seam problem with the **top-left rule**: a pixel on a shared edge belongs to exactly one triangle. With anti-aliasing, a new kind of seam appears. Our program draws an 8 × 8 white square on black in two ways:

- as **two** triangles (cut along the diagonal), each drawn with `fillPolygonAA`,
- as **one** square polygon with `fillPolygonAA`.

It prints:

```
pixel (3, 3): two triangles 227, one polygon 255
pixels that are not white: two triangles 8, one polygon 0
```

The diagonal pixels are **not white** with two triangles. Why?

🔢 **Maths: pixel (3, 3) on the diagonal**

> The diagonal cuts the pixel in half. Each sample belongs to exactly one triangle (the sub-row spans are half-open, like the top-left rule). The upper-right triangle gets 10 of the 16 samples (the ones on the diagonal and above it); the lower-left triangle gets the other 6.
> Triangle 1: coverage 10/16 = 0.625 of white over black → linear 0.625 → file number **207**
> Triangle 2: coverage 6/16 = 0.375 of white over that pixel:
> linear = 0.375 × 1 + 0.625 × (1 − 0.375) = 0.375 + 0.390625 = **0.766** → file number **227**, not 255

The problem: the second blend treats its 0.375 as see-through paint over the **whole** pixel, including the part that triangle 1 already covered. It does not know that its samples are exactly the **other** samples.

📖 **New word: conflation** — this mistake: mixing partial coverages as if they were independent see-through layers.

### The fix: count the samples of the whole shape first

If we fill the square as **one** polygon, every sample of pixel (3, 3) is counted for the same shape: 16 of 16 → coverage 1 → **255**. No seam.

🧠 **Remember:** to draw a shape made of many pieces smoothly, collect the samples of **all** the pieces first (one call of `fillPathsAA` with all the paths), and blend **once**. Think of each pixel's samples as a tiny 4 × 4 **mask** (Chapter 25): combining pieces means combining their masks, not blending their colours.

(Graphics cards solve this with "multisample anti-aliasing": they keep the samples of each pixel separately in memory until the whole picture is finished, and only then average them.)

---

## 27.9 Smooth thick lines

A line with thickness t is really a long, thin **rectangle**. If we know its four corners, `fillPolygonAA` draws it smoothly.

📖 **New word: perpendicular** — at a right angle (90°).

From A to B, the direction is (dx, dy) = (B.x − A.x, B.y − A.y). A direction **perpendicular** to it is:

> **(−dy, dx)** — swap the two numbers, and change the sign of the first

🔢 **Maths: the line from (0, 0) to (3, 4)**

> direction (3, 4); perpendicular (−4, 3)
> check: walking 3 right and 4 down, and then turning to (−4, 3) — 4 left and 3 down — is a quarter turn. (Chapter 29 will prove it with the "dot product": 3 × (−4) + 4 × 3 = 0.)
> length of (−4, 3) = √(16 + 9) = 5, the same as the line's length

We want to move **half the thickness** to each side, so we make the perpendicular exactly t/2 long: divide by the length, multiply by t/2:

> (nx, ny) = (−dy, dx) / length × t / 2

For t = 2: (−4, 3) / 5 × 1 = **(−0.8, 0.6)**. The four corners are:

> A + (nx, ny), B + (nx, ny), B − (nx, ny), A − (nx, ny)
> = (−0.8, 0.6), (2.2, 4.6), (3.8, 3.4), (0.8, −0.6)

`spokes.ppm` has 20 black lines from a centre to the top and bottom edges: on the left with `drawLine` (Chapter 21, jagged), on the right with `fillThickLineAA` (thickness 1, smooth). The smooth lines look thinner and much cleaner, especially the nearly horizontal ones.

---

## 27.10 Draw big, then shrink

📖 **New word: SSAA** — "supersample anti-aliasing". The simplest anti-aliasing of all:

1. Draw the whole picture **n times bigger** (n times wider and n times taller), with ordinary yes/no drawing.
2. **Shrink** it back: every n × n block of big pixels becomes one small pixel, the **average** of the block (in linear light).

This is exactly supersampling! A big pixel (X, Y) has its centre at (X + 0.5, Y + 0.5). In the small picture, that is at ((X + 0.5) / n, (Y + 0.5) / n). With X = n·x + i:

> (n·x + i + 0.5) / n = **x + (i + 0.5) / n**

— exactly our sample positions. And averaging k shape pixels and (n² − k) background pixels in linear light is exactly the coverage blend with coverage k / n².

Our program checks it: a circle with radius 17.3 drawn with `fillCircleAA` in a 50 × 50 picture, and the same circle drawn with plain `fillCircle` 4 times bigger (radius 69.2 in 200 × 200), then shrunk with `shrinkAverage`. It prints:

```
largest difference, fillCircleAA vs draw big and shrink: 0
```

**Identical.** Two very different-looking methods, one idea.

So why not always draw big and shrink? Because it needs **n² times the memory** (a 1000 × 1000 picture at n = 4 is a 4000 × 4000 picture: 48 million bytes instead of 3 million) and n² times the work for **every** pixel, not just the edges. Our coverage functions only do the extra work where it matters.

---

## Code, part 1: `antialias.h`

File: `common/antialias.h` (new). It includes `barycentric.h` (and through it `fill.h` and everything before).

```cpp
#ifndef ANTIALIAS_H
#define ANTIALIAS_H

#include <algorithm>
#include <cmath>
#include <vector>
#include "barycentric.h"

inline double sampleOffset(int i, int n) {
    return (i + 0.5) / n;
}

inline void paintCoverage(Image& image, int x, int y, Colour c, double coverage) {
    if (coverage <= 0.0) {
        return;
    }
    if (coverage >= 1.0) {
        image.setPixel(x, y, c);
        return;
    }
    blendPixel(image, x, y, c, coverage);
}

inline double circleCoverage(double cx, double cy, double r, int x, int y, int n) {
    double r2 = r * r;
    int inside = 0;
    for (int j = 0; j < n; ++j) {
        for (int i = 0; i < n; ++i) {
            double dx = x + sampleOffset(i, n) - cx;
            double dy = y + sampleOffset(j, n) - cy;
            if (dx * dx + dy * dy <= r2) {
                ++inside;
            }
        }
    }
    return static_cast<double>(inside) / (n * n);
}

inline void fillCircleAA(Image& image, double cx, double cy, double r, Colour c, int n = 4) {
    if (r <= 0.0 || n < 1) {
        return;
    }
    const double halfDiagonal = 0.70711;
    int x0 = static_cast<int>(std::floor(cx - r));
    int y0 = static_cast<int>(std::floor(cy - r));
    int x1 = static_cast<int>(std::ceil(cx + r));
    int y1 = static_cast<int>(std::ceil(cy + r));
    Rect box = clipToImage(Rect{x0, y0, x1, y1}, image);
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            double dx = (x + 0.5) - cx;
            double dy = (y + 0.5) - cy;
            double d = std::sqrt(dx * dx + dy * dy);
            if (d <= r - halfDiagonal) {
                image.setPixel(x, y, c);
            } else if (d < r + halfDiagonal) {
                paintCoverage(image, x, y, c, circleCoverage(cx, cy, r, x, y, n));
            }
        }
    }
}

inline double ellipseCoverage(double cx, double cy, double a, double b, int x, int y, int n) {
    double a2 = a * a;
    double b2 = b * b;
    int inside = 0;
    for (int j = 0; j < n; ++j) {
        for (int i = 0; i < n; ++i) {
            double dx = x + sampleOffset(i, n) - cx;
            double dy = y + sampleOffset(j, n) - cy;
            if (b2 * dx * dx + a2 * dy * dy <= a2 * b2) {
                ++inside;
            }
        }
    }
    return static_cast<double>(inside) / (n * n);
}

inline void fillEllipseAA(Image& image, double cx, double cy, double a, double b, Colour c,
                          int n = 4) {
    if (a <= 0.0 || b <= 0.0 || n < 1) {
        return;
    }
    int x0 = static_cast<int>(std::floor(cx - a));
    int y0 = static_cast<int>(std::floor(cy - b));
    int x1 = static_cast<int>(std::ceil(cx + a));
    int y1 = static_cast<int>(std::ceil(cy + b));
    Rect box = clipToImage(Rect{x0, y0, x1, y1}, image);
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            paintCoverage(image, x, y, c, ellipseCoverage(cx, cy, a, b, x, y, n));
        }
    }
}

inline void fillPathsAA(Image& image, const std::vector<std::vector<PointF>>& paths, Colour col,
                        FillRule rule = FillRule::NonZero, int n = 4) {
    if (n < 1) {
        return;
    }
    bool any = false;
    double minY = 0.0;
    double maxY = 0.0;
    for (const std::vector<PointF>& path : paths) {
        for (PointF p : path) {
            if (!any) {
                minY = p.y;
                maxY = p.y;
                any = true;
            } else {
                minY = std::min(minY, p.y);
                maxY = std::max(maxY, p.y);
            }
        }
    }
    if (!any) {
        return;
    }
    const int width = image.width();
    int y0 = std::max(0, static_cast<int>(std::floor(minY)));
    int y1 = std::min(image.height(), static_cast<int>(std::ceil(maxY)));
    std::vector<int> counts(width, 0);
    std::vector<Crossing> crossings;
    for (int y = y0; y < y1; ++y) {
        std::fill(counts.begin(), counts.end(), 0);
        for (int j = 0; j < n; ++j) {
            double sy = y + sampleOffset(j, n);
            crossings.clear();
            for (const std::vector<PointF>& path : paths) {
                findCrossings(path, sy, crossings);
            }
            std::sort(crossings.begin(), crossings.end(), crossingIsLeft);
            int winding = 0;
            const int count = static_cast<int>(crossings.size());
            for (int k = 0; k + 1 < count; ++k) {
                winding += crossings[k].direction;
                bool inside = (rule == FillRule::EvenOdd) ? (k % 2 == 0) : (winding != 0);
                if (!inside) {
                    continue;
                }
                double xa = crossings[k].x;
                double xb = crossings[k + 1].x;
                int first = std::max(0, static_cast<int>(std::floor(xa)));
                int last = std::min(width - 1, static_cast<int>(std::floor(xb)));
                for (int x = first; x <= last; ++x) {
                    for (int i = 0; i < n; ++i) {
                        double sx = x + sampleOffset(i, n);
                        if (sx >= xa && sx < xb) {
                            ++counts[x];
                        }
                    }
                }
            }
        }
        for (int x = 0; x < width; ++x) {
            if (counts[x] > 0) {
                paintCoverage(image, x, y, col, static_cast<double>(counts[x]) / (n * n));
            }
        }
    }
}

inline void fillPolygonAA(Image& image, const std::vector<PointF>& points, Colour col,
                          FillRule rule = FillRule::NonZero, int n = 4) {
    std::vector<std::vector<PointF>> paths;
    paths.push_back(points);
    fillPathsAA(image, paths, col, rule, n);
}

inline void fillThickLineAA(Image& image, PointF a, PointF b, double thickness, Colour col,
                            int n = 4) {
    double dx = b.x - a.x;
    double dy = b.y - a.y;
    double length = std::sqrt(dx * dx + dy * dy);
    if (length == 0.0) {
        return;
    }
    double half = thickness / 2.0;
    double nx = -dy / length * half;
    double ny = dx / length * half;
    std::vector<PointF> band = {PointF{a.x + nx, a.y + ny}, PointF{b.x + nx, b.y + ny},
                                PointF{b.x - nx, b.y - ny}, PointF{a.x - nx, a.y - ny}};
    fillPolygonAA(image, band, col, FillRule::NonZero, n);
}

inline Image shrinkAverage(const Image& big, int factor) {
    const int w = big.width() / factor;
    const int h = big.height() / factor;
    Image small(w, h);
    for (int y = 0; y < h; ++y) {
        for (int x = 0; x < w; ++x) {
            ColourF sum{0.0, 0.0, 0.0};
            for (int j = 0; j < factor; ++j) {
                for (int i = 0; i < factor; ++i) {
                    sum = sum + toLinear(big.getPixel(x * factor + i, y * factor + j));
                }
            }
            small.setPixel(x, y, fromLinear(sum / (factor * factor)));
        }
    }
    return small;
}

#endif
```

### Line by line

**The start and two small helpers (lines 1–22)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef ANTIALIAS_H` / `#define ANTIALIAS_H` | Include guard. |
| 4–6 | `#include <algorithm>` / `<cmath>` / `<vector>` | `std::min`, `std::max`, `std::sort`, `std::fill`; `std::floor`, `std::ceil`, `std::sqrt`; vectors. |
| 7 | `#include "barycentric.h"` | Everything before, including `fill.h` (crossings, fill rules) and `blendPixel`. |
| 9–11 | `inline double sampleOffset(int i, int n) { return (i + 0.5) / n; }` | Where sample number i sits inside a pixel, from 0 to 1 (Section 27.3). For n = 4: 0.125, 0.375, 0.625, 0.875. |
| 13 | `inline void paintCoverage(Image& image, int x, int y, Colour c, double coverage) {` | Paint one pixel with a given coverage (Section 27.2). |
| 14–16 | `if (coverage <= 0.0) { return; }` | Not covered at all: leave the pixel alone. |
| 17–20 | `if (coverage >= 1.0) { image.setPixel(x, y, c); return; }` | Fully covered: just set it (faster than blending, and exact). |
| 21–22 | `blendPixel(image, x, y, c, coverage);` `}` | Partly covered: blend in linear light with alpha = coverage (Chapters 18 and 27.5). |

**Smooth circles (lines 24–61)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 24 | `inline double circleCoverage(double cx, double cy, double r, int x, int y, int n) {` | The coverage of pixel (x, y) by the circle, estimated with n × n samples. |
| 25–26 | `double r2 = r * r;` / `int inside = 0;` | r² once; a counter. |
| 27–28 | `for (int j = 0; j < n; ++j) { for (int i = 0; i < n; ++i) {` | Every sample: j is the sub-row, i the sub-column. |
| 29–30 | `double dx = x + sampleOffset(i, n) - cx;` / `double dy = y + sampleOffset(j, n) - cy;` | From the circle's centre to the sample. |
| 31–33 | `if (dx * dx + dy * dy <= r2) { ++inside; }` | The circle test of Chapter 22, for this sample. |
| 36–37 | `return static_cast<double>(inside) / (n * n);` `}` | Samples inside ÷ all samples. The cast makes it a `double` division (otherwise 8 / 16 would be 0). |
| 39 | `inline void fillCircleAA(Image& image, double cx, double cy, double r, Colour c, int n = 4) {` | A smooth filled circle. n = 4 by default. |
| 40–42 | `if (r <= 0.0 \|\| n < 1) { return; }` | Nothing to draw. |
| 43 | `const double halfDiagonal = 0.70711;` | Half a pixel's diagonal, √0.5, rounded up (Section 27.6). |
| 44–48 | the bounding box and `clipToImage` | As in `fillCircle` (Chapter 22). |
| 49–53 | the loops, `dx`, `dy`, `double d = std::sqrt(dx * dx + dy * dy);` | The distance from the circle's centre to the pixel centre. |
| 54–55 | `if (d <= r - halfDiagonal) { image.setPixel(x, y, c); }` | The whole pixel is inside: solid, no sampling. |
| 56–57 | `} else if (d < r + halfDiagonal) { paintCoverage(..., circleCoverage(cx, cy, r, x, y, n)); }` | Near the edge: sample it. (Pixels further out are skipped: fully outside.) |
| 58–61 | `}` `}` `}` `}` | End. |

**Smooth ellipses (lines 63–94)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 63–77 | `inline double ellipseCoverage(...) { ... }` | The same as `circleCoverage`, with the ellipse test of Chapter 23 (b²dx² + a²dy² ≤ a²b²). |
| 79–80 | `inline void fillEllipseAA(Image& image, double cx, double cy, double a, double b, Colour c, int n = 4) {` | A smooth filled ellipse. |
| 81–83 | `if (a <= 0.0 \|\| b <= 0.0 \|\| n < 1) { return; }` | Nothing to draw. |
| 84–88 | the bounding box | As in `fillEllipse`. |
| 89–94 | the loops with `paintCoverage(image, x, y, c, ellipseCoverage(...));` | Sample **every** pixel in the box. (Simpler than the circle: no shortcut. Practice 5 adds one.) |

**Smooth polygons (lines 96–161)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 96–97 | `inline void fillPathsAA(Image& image, const std::vector<std::vector<PointF>>& paths, Colour col, FillRule rule = FillRule::NonZero, int n = 4) {` | Like `fillPaths` (Chapter 25), but smooth (Section 27.7). |
| 98–100 | `if (n < 1) { return; }` | At least one sample is needed. |
| 101–118 | `any`, `minY`, `maxY`, the loops | Find the top and bottom of the shape — the same as `fillPaths`. |
| 119 | `const int width = image.width();` | The image width, used often below. |
| 120–121 | `int y0 = ...;` / `int y1 = ...;` | The pixel rows to visit, clipped to the image. |
| 122 | `std::vector<int> counts(width, 0);` | One sample counter per pixel of the current row. |
| 123 | `std::vector<Crossing> crossings;` | The crossings of one sub-row. |
| 124 | `for (int y = y0; y < y1; ++y) {` | Every pixel row. |
| 125 | `std::fill(counts.begin(), counts.end(), 0);` | Reset all counters to 0 for this row. `std::fill` sets every element to the same value. |
| 126–127 | `for (int j = 0; j < n; ++j) { double sy = y + sampleOffset(j, n);` | The n sub-rows of this pixel row. |
| 128–136 | `crossings.clear();` … `winding += crossings[k].direction;` | Exactly the scanline steps of Chapter 25, at the height sy. |
| 137–140 | `bool inside = ...; if (!inside) { continue; }` | The fill rule, as before. |
| 141–142 | `double xa = crossings[k].x;` / `double xb = crossings[k + 1].x;` | An inside span of this sub-row, from xa to xb. |
| 143–144 | `int first = std::max(0, ...floor(xa)...);` / `int last = std::min(width - 1, ...floor(xb)...);` | The pixels the span touches: from the pixel that contains xa to the pixel that contains xb, clipped to the image. |
| 145–148 | `for (int x = first; x <= last; ++x) { for (int i = 0; i < n; ++i) { double sx = x + sampleOffset(i, n); if (sx >= xa && sx < xb) {` | For each sample of this sub-row in these pixels: is it inside the span? (Half-open: xa included, xb not — like Chapter 25.) |
| 149 | `++counts[x];` | One more sample inside for pixel x. |
| 150–154 | `}` … `}` | End of the span, gap and sub-row loops. |
| 155–158 | `for (int x = 0; x < width; ++x) { if (counts[x] > 0) { paintCoverage(..., static_cast<double>(counts[x]) / (n * n)); } }` | All sub-rows done: paint every pixel of the row with its coverage. |
| 159–161 | `}` `}` `}` | End. |
| 163–168 | `inline void fillPolygonAA(...) { ... fillPathsAA(image, paths, col, rule, n); }` | One path, like `fillPolygon`. |

**Smooth thick lines (lines 170–184)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 170–171 | `inline void fillThickLineAA(Image& image, PointF a, PointF b, double thickness, Colour col, int n = 4) {` | A smooth line from a to b, `thickness` pixels wide (Section 27.9). |
| 172–174 | `double dx = b.x - a.x;` / `double dy = b.y - a.y;` / `double length = std::sqrt(dx * dx + dy * dy);` | The direction and the length of the line (Pythagoras). |
| 175–177 | `if (length == 0.0) { return; }` | A line of length 0 has no direction: draw nothing (and do not divide by 0). |
| 178 | `double half = thickness / 2.0;` | Half the thickness goes to each side. |
| 179–180 | `double nx = -dy / length * half;` / `double ny = dx / length * half;` | The perpendicular (−dy, dx), made exactly `half` long. |
| 181–182 | `std::vector<PointF> band = {PointF{a.x + nx, a.y + ny}, ...};` | The four corners of the thin rectangle, going around it in order. |
| 183–184 | `fillPolygonAA(image, band, col, FillRule::NonZero, n);` `}` | Fill it smoothly. |

**Draw big, then shrink (lines 186–204)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 186 | `inline Image shrinkAverage(const Image& big, int factor) {` | Make a picture `factor` times smaller, averaging each block (Section 27.10). |
| 187–189 | `const int w = big.width() / factor;` … `Image small(w, h);` | The small picture's size. |
| 190–191 | `for (int y = 0; y < h; ++y) { for (int x = 0; x < w; ++x) {` | Every small pixel. |
| 192 | `ColourF sum{0.0, 0.0, 0.0};` | The sum of the block's light. |
| 193–197 | `for (int j = 0; ...) { for (int i = 0; ...) { sum = sum + toLinear(big.getPixel(x * factor + i, y * factor + j)); } }` | Add up the **linear** light of the factor × factor big pixels that make this small pixel. |
| 198 | `small.setPixel(x, y, fromLinear(sum / (factor * factor)));` | The average, turned back into a file colour. |
| 199–202 | `}` `}` `return small;` `}` | Done. |
| 204 | `#endif` | End of the include guard. |

---

## Code, part 2: zoom, stars and spokes

File: `ch27/antialias.cpp`

```cpp
#include <iostream>
#include <string>
#include <vector>
#include "antialias.h"

void printSampleMask(double cx, double cy, double r, int x, int y, int n) {
    std::cout << "samples in pixel (" << x << ", " << y << "):\n";
    int inside = 0;
    for (int j = 0; j < n; ++j) {
        std::cout << "  ";
        for (int i = 0; i < n; ++i) {
            double dx = x + sampleOffset(i, n) - cx;
            double dy = y + sampleOffset(j, n) - cy;
            bool in = dx * dx + dy * dy <= r * r;
            if (in) {
                ++inside;
            }
            std::cout << (in ? '#' : '.');
        }
        std::cout << "\n";
    }
    std::cout << "  coverage " << inside << " / " << n * n << "\n";
}

void printCoverageMap(double cx, double cy, double r, int width, int height, int n) {
    std::cout << "coverage of each pixel, from 0 to 9:\n";
    for (int y = 0; y < height; ++y) {
        std::cout << "  ";
        for (int x = 0; x < width; ++x) {
            double coverage = circleCoverage(cx, cy, r, x, y, n);
            int digit = static_cast<int>(coverage * 9.0 + 0.5);
            if (digit == 0) {
                std::cout << '.';
            } else {
                std::cout << digit;
            }
        }
        std::cout << "\n";
    }
}

int channelDifference(int a, int b) {
    return (a > b) ? a - b : b - a;
}

int largestDifference(const Image& p, const Image& q) {
    int largest = 0;
    for (int y = 0; y < p.height(); ++y) {
        for (int x = 0; x < p.width(); ++x) {
            Colour s = p.getPixel(x, y);
            Colour t = q.getPixel(x, y);
            largest = std::max(largest, channelDifference(s.r, t.r));
            largest = std::max(largest, channelDifference(s.g, t.g));
            largest = std::max(largest, channelDifference(s.b, t.b));
        }
    }
    return largest;
}

int countNotWhite(const Image& img) {
    int count = 0;
    for (int y = 0; y < img.height(); ++y) {
        for (int x = 0; x < img.width(); ++x) {
            if (!sameColour(img.getPixel(x, y), colours::white)) {
                ++count;
            }
        }
    }
    return count;
}

void pasteEnlarged(Image& dst, const Image& src, int ox, int oy, int factor) {
    for (int y = 0; y < src.height() * factor; ++y) {
        for (int x = 0; x < src.width() * factor; ++x) {
            dst.setPixel(ox + x, oy + y, src.getPixel(x / factor, y / factor));
        }
    }
}

std::vector<PointF> star(double cx, double cy, double r) {
    const double ux[5] = {0.0, 0.9511, 0.5878, -0.5878, -0.9511};
    const double uy[5] = {-1.0, -0.3090, 0.8090, 0.8090, -0.3090};
    const int order[5] = {0, 2, 4, 1, 3};
    std::vector<PointF> points;
    for (int i = 0; i < 5; ++i) {
        int k = order[i];
        points.push_back(PointF{cx + r * ux[k], cy + r * uy[k]});
    }
    return points;
}

int main() {
    printSampleMask(5.5, 5.5, 5.0, 9, 2, 4);
    printCoverageMap(5.5, 5.5, 5.0, 11, 11, 4);

    Image smooth(50, 50);
    fillCircleAA(smooth, 25.0, 25.0, 17.3, colours::white);
    Image big(200, 200);
    fillCircle(big, 100.0, 100.0, 4 * 17.3, colours::white);
    Image shrunk = shrinkAverage(big, 4);
    std::cout << "largest difference, fillCircleAA vs draw big and shrink: "
              << largestDifference(smooth, shrunk) << "\n";

    Image twoTriangles(8, 8);
    fillPolygonAA(twoTriangles, {PointF{0.0, 0.0}, PointF{8.0, 0.0}, PointF{8.0, 8.0}},
                  colours::white);
    fillPolygonAA(twoTriangles, {PointF{0.0, 0.0}, PointF{8.0, 8.0}, PointF{0.0, 8.0}},
                  colours::white);
    Image onePolygon(8, 8);
    fillPolygonAA(onePolygon,
                  {PointF{0.0, 0.0}, PointF{8.0, 0.0}, PointF{8.0, 8.0}, PointF{0.0, 8.0}},
                  colours::white);
    std::cout << "pixel (3, 3): two triangles " << static_cast<int>(twoTriangles.getPixel(3, 3).r)
              << ", one polygon " << static_cast<int>(onePolygon.getPixel(3, 3).r) << "\n";
    std::cout << "pixels that are not white: two triangles " << countNotWhite(twoTriangles)
              << ", one polygon " << countNotWhite(onePolygon) << "\n";

    Image jagged(40, 40, colours::white);
    fillCircle(jagged, 20.0, 20.0, 15.0, Colour{30, 60, 160});
    Image soft(40, 40, colours::white);
    fillCircleAA(soft, 20.0, 20.0, 15.0, Colour{30, 60, 160});
    Image zoom(490, 240, colours::white);
    pasteEnlarged(zoom, jagged, 0, 0, 6);
    pasteEnlarged(zoom, soft, 250, 0, 6);

    Image stars(420, 220, Colour{20, 30, 70});
    Colour gold{255, 200, 40};
    fillPolygon(stars, star(110.5, 115.5, 100.0), gold);
    fillPolygonAA(stars, star(310.5, 115.5, 100.0), gold);

    Image spokes(400, 200, colours::white);
    for (int k = 0; k < 10; ++k) {
        int ex = 10 + 20 * k;
        drawLine(spokes, 100, 100, ex, 10, colours::black);
        drawLine(spokes, 100, 100, ex, 190, colours::black);
        PointF centre{300.0, 100.0};
        fillThickLineAA(spokes, centre, PointF{ex + 200.0, 10.0}, 1.0, colours::black);
        fillThickLineAA(spokes, centre, PointF{ex + 200.0, 190.0}, 1.0, colours::black);
    }

    bool ok = zoom.savePPM("zoom.ppm");
    ok = ok && stars.savePPM("stars_aa.ppm");
    ok = ok && spokes.savePPM("spokes.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
```

Build and run (from the `code/ch27` folder):

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common antialias.cpp -o antialias
./antialias
```

### Line by line

**Printing helpers (lines 6–40)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 6 | `void printSampleMask(double cx, double cy, double r, int x, int y, int n) {` | Show which of the n × n samples of one pixel are inside a circle (Section 27.3). |
| 9–21 | the two loops, `dx`, `dy`, `bool in = dx * dx + dy * dy <= r * r;`, printing `#` or `.` | The same test as `circleCoverage`, but printing each sample. |
| 22 | `std::cout << "  coverage " << inside << " / " << n * n << "\n";` | How many were inside, out of how many. |
| 25 | `void printCoverageMap(double cx, double cy, double r, int width, int height, int n) {` | Print the coverage of every pixel as a digit (Section 27.6). |
| 30 | `double coverage = circleCoverage(cx, cy, r, x, y, n);` | The coverage, 0 to 1. |
| 31 | `int digit = static_cast<int>(coverage * 9.0 + 0.5);` | Turn it into 0 … 9, rounded (Chapter 13's rounding trick). |
| 32–36 | `if (digit == 0) { std::cout << '.'; } else { std::cout << digit; }` | Print a dot for 0, so the shape is easy to see. |

**Comparing pictures (lines 42–70)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 42–44 | `int channelDifference(int a, int b) { return (a > b) ? a - b : b - a; }` | The distance between two numbers, always positive. (Our own small "absolute value", so we need no extra header.) |
| 46–58 | `int largestDifference(const Image& p, const Image& q) { ... }` | The biggest difference in any channel of any pixel. 0 means the pictures are identical. |
| 60–70 | `int countNotWhite(const Image& img) { ... }` | How many pixels are not exactly white (to find seams, Section 27.8). |

**Zooming and the star (lines 72–90)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 72 | `void pasteEnlarged(Image& dst, const Image& src, int ox, int oy, int factor) {` | Copy `src` into `dst` at (ox, oy), with every pixel made into a `factor` × `factor` block, so we can see the pixels. |
| 73–74 | `for (int y = 0; y < src.height() * factor; ++y) { for (int x = 0; x < src.width() * factor; ++x) {` | Every pixel of the enlarged copy. |
| 75 | `dst.setPixel(ox + x, oy + y, src.getPixel(x / factor, y / factor));` | Whole-number division picks the source pixel: x = 0 … 5 all come from source pixel 0 when factor is 6. (This is "nearest neighbour" enlarging — Chapter 35.) |
| 80–90 | `std::vector<PointF> star(...) { ... }` | The star of Chapter 25. |

**The text output (lines 92–116)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 93–94 | `printSampleMask(5.5, 5.5, 5.0, 9, 2, 4);` / `printCoverageMap(5.5, 5.5, 5.0, 11, 11, 4);` | The pixel of Section 27.3 and the coverage map of Section 27.6, for the Chapter 22 disc. |
| 96–97 | `Image smooth(50, 50);` / `fillCircleAA(smooth, 25.0, 25.0, 17.3, colours::white);` | A smooth circle. |
| 98–99 | `Image big(200, 200);` / `fillCircle(big, 100.0, 100.0, 4 * 17.3, colours::white);` | The same circle, 4 times bigger, with ordinary yes/no drawing. `4 * 17.3` keeps it exactly 4 times the small radius. |
| 100–102 | `Image shrunk = shrinkAverage(big, 4);` … `largestDifference(smooth, shrunk)` | Shrink it and compare (Section 27.10). |
| 104–108 | `Image twoTriangles(8, 8);` and two `fillPolygonAA` calls | The square as two smooth triangles (Section 27.8). The `{PointF{...}, ...}` makes a list of points on the spot. |
| 109–112 | `Image onePolygon(8, 8);` and one `fillPolygonAA` call | The same square as one polygon. |
| 113–116 | the two `std::cout` lines | Print pixel (3, 3) of both, and how many pixels are not white. `static_cast<int>` prints the byte as a number, not as a letter. |

**The pictures (lines 118–149)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 118–121 | `Image jagged(40, 40, ...);` … `fillCircleAA(soft, 20.0, 20.0, 15.0, Colour{30, 60, 160});` | A blue circle twice: yes/no and smooth. |
| 122–124 | `Image zoom(490, 240, colours::white);` and two `pasteEnlarged` calls | Both, 6 times bigger, side by side with a 10-pixel gap. |
| 126–129 | `Image stars(...);` … `fillPolygonAA(stars, star(310.5, 115.5, 100.0), gold);` | The star of Chapter 25, jagged on the left, smooth on the right. |
| 131 | `Image spokes(400, 200, colours::white);` | A white picture. |
| 132–133 | `for (int k = 0; k < 10; ++k) { int ex = 10 + 20 * k;` | Ten end positions along the top and bottom edges: x = 10, 30, …, 190. |
| 134–135 | `drawLine(spokes, 100, 100, ex, 10, colours::black);` / `drawLine(..., ex, 190, ...);` | Left half: jagged Bresenham lines from (100, 100). |
| 136–138 | `PointF centre{300.0, 100.0};` and two `fillThickLineAA` calls | Right half: the same lines, 200 pixels to the right, smooth and 1 pixel thick. |
| 139 | `}` | End of the loop. |
| 141–149 | saving | `zoom.ppm`, `stars_aa.ppm`, `spokes.ppm`. |

### What you should see

The program prints the sample mask and the coverage map (Sections 27.3 and 27.6), then:

```
largest difference, fillCircleAA vs draw big and shrink: 0
pixel (3, 3): two triangles 227, one polygon 255
pixels that are not white: two triangles 8, one polygon 0
```

Open the pictures:
- `zoom.ppm`: two big blue circles made of visible blocks. The left one has hard stair-steps. The right one has soft, light-blue blocks along its edge, and from a distance it looks perfectly round.
- `stars_aa.ppm`: two gold stars. Look at the thin points: the right star's edges are smooth.
- `spokes.ppm`: two fans of black lines. The left lines are jagged and look uneven; the right lines are smooth grey-and-black and look thin and straight.

---

## Small examples

### Example 1 — Which samples of a pixel are inside a half-plane?

The shape "everything left of x = 10.6". Pixel 10, n = 4: samples at 10.125, 10.375, 10.625, 10.875.

> inside: 10.125 and 10.375 → 2 of each row of 4 → coverage 2/4 = **0.5**
> the true coverage is 0.6 (from 10 to 10.6). A 4 × 4 grid can only say 0, 0.25, 0.5, 0.75 or 1 for a vertical edge (Section 27.4).

### Example 2 — Coverage of a pixel crossed by a diagonal

The shape "below the line y = x" (that is, y > x), pixel (3, 3), n = 4. A sample is inside when its j-offset is bigger than its i-offset:

> j = 1: i = 0 → 1 sample; j = 2: i = 0, 1 → 2; j = 3: i = 0, 1, 2 → 3 → total **6** of 16 = 0.375

(The diagonal samples, i = j, are exactly on the line and not counted — the same 6 as triangle 2 in Section 27.8.)

### Example 3 — The cost of a smooth circle

> r = 100: the box has 200 × 200 = 40,000 pixels, and each one gets **one** distance test
> about 890 of them are edge pixels and get 16 sample tests more: 890 × 16 ≈ 14,000
> total ≈ 54,000 tests
> a plain `fillCircle` also does one test per box pixel: 40,000 tests
> so the smooth circle costs only about **a third more** — not 16 times more.

### Example 4 — Thick line corners

A horizontal line from (10, 20) to (30, 20), thickness 4:

> direction (20, 0), length 20; perpendicular (−0, 20) / 20 × 2 = (0, 2)
> corners: (10, 22), (30, 22), (30, 18), (10, 18) → a 20 × 4 rectangle ✓

### Example 5 — Smooth text?

A letter of a font is a set of paths (with holes for "o", "e", "a" …). With `fillPathsAA` and all the paths of the letter in **one** call, letters come out smooth and without seams. This is how real font programs draw text.

---

## Common mistakes

⚠️ **Blending coverage in sRGB numbers.** Half coverage would give 128 instead of 188: edges look too dark or too light. Blend in linear light.

⚠️ **Integer division for the coverage.** `inside / (n * n)` with `int`s is 0 (or 1). Cast to `double` first.

⚠️ **Sample positions at pixel corners** (x + i / n instead of x + (i + 0.5) / n). The samples are no longer evenly spread: the shape shifts by a fraction of a pixel.

⚠️ **Drawing a shape in pieces, each with its own coverage blend.** Faint seams where the pieces meet (Section 27.8). Collect all paths into one `fillPathsAA` call.

⚠️ **Using the circle shortcut with the wrong distance.** It must be half the **diagonal** (0.7071), not half the side (0.5): a pixel whose centre is 0.6 inside the circle can still have a corner outside it.

⚠️ **Expecting smooth edges from too few samples.** n = 2 gives only 5 levels; you will still see small steps.

---

## Practice

🏋️ **1.** For the circle with centre (5.5, 5.5) and radius 5, test the 4 samples of pixel (9, 2) with n = 2 by hand. Do you get 0.5, as in the table of Section 27.3?

🏋️ **2.** How many coverage levels does n = 3 give? And n = 6?

🏋️ **3.** Blend black over white with coverage 0.25, in linear light. What file number do you get? (Hint: the light is 0.75 of white.)

🏋️ **4.** Write `fillRingAA(image, cx, cy, inner, outer, colour, n)`: a smooth ring (a thick circle outline), with its own coverage function. A sample is inside when inner² ≤ dx² + dy² ≤ outer².

🏋️ **5.** Add an "only the edge" shortcut to `fillEllipseAA`. Hint: test the pixel's four **corners** with the ellipse test. If all four are inside, what is the coverage? And if all four are outside — can the pixel still be partly covered?

🏋️ **6.** Draw the two-triangle square of Section 27.8, but in **one** call: `fillPathsAA(img, {triangle1, triangle2}, colours::white)`. What do you get for pixel (3, 3)? Why?

🏋️ **7.** Use `fillThickLineAA` to draw a smooth outline of a triangle: three thick lines, thickness 3. What happens at the corners?

🏋️ **8.** Draw the `spokes.ppm` picture with "draw big, then shrink": draw the jagged lines in a 1600 × 800 picture with `drawThickLine` (Chapter 21, thickness 4), then shrink by 4. Compare with the right half of `spokes.ppm`.

---

## Answers

**1.**
> n = 2: offsets 0.25 and 0.75 → samples (9.25, 2.25), (9.75, 2.25), (9.25, 2.75), (9.75, 2.75)
> (9.25, 2.25): dx = 3.75, dy = −3.25 → 14.06 + 10.56 = 24.63 ≤ 25 → inside
> (9.75, 2.25): dx = 4.25 → 18.06 + 10.56 = 28.63 → outside
> (9.25, 2.75): dy = −2.75 → 14.06 + 7.56 = 21.63 → inside
> (9.75, 2.75): 18.06 + 7.56 = 25.63 → outside
> 2 of 4 → **0.5** ✓

**2.** n = 3: 9 samples → **10** levels. n = 6: 36 samples → **37** levels.

**3.** Black over white with alpha 0.25: light = 0.25 × 0 + 0.75 × 1 = 0.75 → file number about **225** (from the table in Section 27.5: coverage 0.75 of white gives 225).

**4.**

```cpp
inline double ringCoverage(double cx, double cy, double inner, double outer,
                           int x, int y, int n) {
    int inside = 0;
    for (int j = 0; j < n; ++j) {
        for (int i = 0; i < n; ++i) {
            double dx = x + sampleOffset(i, n) - cx;
            double dy = y + sampleOffset(j, n) - cy;
            double d2 = dx * dx + dy * dy;
            if (d2 >= inner * inner && d2 <= outer * outer) {
                ++inside;
            }
        }
    }
    return static_cast<double>(inside) / (n * n);
}

inline void fillRingAA(Image& image, double cx, double cy, double inner, double outer,
                       Colour c, int n = 4) {
    Rect box = clipToImage(Rect{static_cast<int>(std::floor(cx - outer)),
                                static_cast<int>(std::floor(cy - outer)),
                                static_cast<int>(std::ceil(cx + outer)),
                                static_cast<int>(std::ceil(cy + outer))}, image);
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            paintCoverage(image, x, y, c, ringCoverage(cx, cy, inner, outer, x, y, n));
        }
    }
}
```

This is the smooth version of Chapter 22's `strokeCircle`.

**5.** Yes, it can! A very thin ellipse (say b = 0.3) can pass through the middle of a pixel without touching any of its corners. So "all four corners outside" does **not** prove coverage 0. A safe shortcut: test the four corners; if **all four are inside**, the coverage is 1 (an ellipse is convex, so the whole square between the corners is inside too). In every other case, sample.

```cpp
bool cornerInside(double px, double py) {   // the ellipse test for one point
    double dx = px - cx;
    double dy = py - cy;
    return b2 * dx * dx + a2 * dy * dy <= a2 * b2;
}
// in the loop:
if (cornerInside(x, y) && cornerInside(x + 1, y) &&
    cornerInside(x, y + 1) && cornerInside(x + 1, y + 1)) {
    image.setPixel(x, y, c);
} else {
    paintCoverage(image, x, y, c, ellipseCoverage(cx, cy, a, b, x, y, n));
}
```

(Write `cornerInside` as a small helper that takes cx, cy, a2 and b2 as parameters.)

**6.** Pixel (3, 3) is **255**. With both paths in one call, each sub-row finds the crossings of **both** triangles together. With the non-zero rule, the two diagonal crossings cancel out (one goes down, one goes up), so the whole sub-row from 0 to 8 is inside: all 16 samples are counted for one shape, and the pixel is blended **once** with coverage 1.

**7.** At each corner, two thick lines overlap, and the overlapping part is blended **twice** (conflation again). With black lines on white, the corners look a little darker. Also, the outer corner is cut off (the lines end square at the corner point). To get clean corners, draw the outline as **one** shape: the outer triangle and a smaller inner triangle as two paths (a hole), with one `fillPathsAA` call — like the frame in Chapter 25.

**8.**

```cpp
Image big(1600, 800, colours::white);
for (int k = 0; k < 10; ++k) {
    int ex = 10 + 20 * k;
    drawThickLine(big, 1200, 400, (ex + 200) * 4, 40, 4, colours::black);
    drawThickLine(big, 1200, 400, (ex + 200) * 4, 760, 4, colours::black);
}
Image small = shrinkAverage(big, 4);
```

It looks very similar to the right half of `spokes.ppm`. It is not identical, because `drawThickLine` uses a square brush on a Bresenham line (Chapter 21), which is a slightly different shape from our exact thin rectangle.

---

## Summary

🧠 **Jaggies** come from yes/no pixels. The cure is to colour each pixel by its **coverage** (0 to 1).

🧠 Coverage = **alpha**: blend the shape over the background with alpha = coverage, in **linear light**.

🧠 Estimate coverage with an **n × n grid of samples** at (x + (i + 0.5)/n, y + (j + 0.5)/n): coverage ≈ inside / n².

🧠 n × n samples give **n² + 1** levels and cost **n² times** as many tests. n = 4 is a good default.

🧠 Only pixels within **half a diagonal (0.7071)** of the edge need sampling.

🧠 Smooth polygons: the Chapter 25 scanline method on **n sub-rows**, counting samples per pixel.

🧠 Pieces blended separately give **seams** (conflation): draw a shape in **one** call.

🧠 A thick line is a thin rectangle: corners A ± (nx, ny), B ± (nx, ny), with (nx, ny) = (−dy, dx) / length × t/2.

🧠 **Draw big, then shrink** gives exactly the same result as supersampling — but costs much more memory.

---

## Next chapter

Supersampling is simple and works for every shape, but it does 16 tests per edge pixel. For the most common shape of all — a thin **line** — there is a famous faster method. In Chapter 28 we learn **Wu's line algorithm**, which computes the coverage of a line's two nearest pixels **directly**, with no samples at all, and we compare it with what we built here.
