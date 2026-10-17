# Chapter 19 — Pixels and Rectangles

> **Part 4 · Chapter 19 of 82**
> **You need:** Chapters 1–18 · **You will make:** `draw.h` (rectangles: fill, outline, clip, alpha) and `house.ppm` (a small scene built only from rectangles)

---

## What you will learn

- Two ways to describe a rectangle: **position + size**, or **two corners**.
- **Half-open ranges** — "from x0 up to, but not including, x1" — and why they stop off-by-one bugs.
- How to **normalise** a rectangle given in any order.
- **Empty** rectangles, and how to test for them.
- How to find where two rectangles **overlap** (intersection).
- How to **clip** a rectangle to the image, so we never loop over pixels that do not exist.
- How to draw **outlines** of any thickness, without painting any pixel twice.
- Which pixels belong to a rectangle whose corners are **not whole numbers**.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **plot** | To set one pixel to a colour. |
| **rectangle** | A shape with four straight sides and four square corners. Ours always have sides parallel to the image edges. |
| **half-open range** | A range that **includes** its start but **not** its end: [x0, x1). |
| **inclusive range** | A range that includes both ends: [x0, x1]. |
| **off-by-one error** | A bug where a count or position is wrong by exactly 1. |
| **normalise** | To put values into a standard form, like "the smaller corner first". |
| **intersection** | The part where two shapes overlap. |
| **clip** | To cut a shape so only the part inside an area (like the image) is left. |
| **fill** | To colour the whole inside of a shape. |
| **stroke** (outline) | To colour only the border of a shape. |
| **ceiling** | The smallest whole number that is not smaller than a number: ceil(2.3) = 3. |

---

## 19.1 The smallest shape: one pixel

📖 **New word: plot** — to set one pixel to a colour.

We have plotted pixels since Chapter 6: `image.setPixel(x, y, colour)`. Every shape in Part 4 — rectangles, lines, circles, triangles — is drawn by plotting the **right set of pixels**. The real question of each chapter is: **which pixels belong to the shape?**

For a rectangle, the answer is easy. That makes it a good place to learn the **rules** we will use for every shape: how to describe it, which edge pixels count, and how to stay inside the image.

---

## 19.2 Describing a rectangle

📖 **New word: rectangle** — a shape with four straight sides and four square corners. In this chapter, the sides are always **parallel to the image edges** (no tilted rectangles; those need triangles, Chapter 24).

There are two common ways to describe one:

**1. Position and size:** the top-left corner (x, y), plus a width w and a height h.

```
(x, y) ●─────────── w ───────────┐
       │                         │
       h                         │
       │                         │
       └─────────────────────────┘
```

**2. Two corners:** the top-left corner (x0, y0) and the bottom-right corner (x1, y1).

> x1 = x + w
> y1 = y + h

🔢 **Maths: a rectangle at (10, 20) with size 30 × 40**

> x0 = 10, y0 = 20
> x1 = 10 + 30 = **40**
> y1 = 20 + 40 = **60**

Inside our code, we always store the **two-corner** form, in a small struct:

```cpp
struct Rect {
    int x0 = 0;
    int y0 = 0;
    int x1 = 0;
    int y1 = 0;
};
```

Why corners? Because overlaps and clipping (Sections 19.6 and 19.7) are very simple with corners, and awkward with sizes.

---

## 19.3 Half-open ranges

Here is a question that sounds silly but causes many bugs. The rectangle goes from x0 = 10 to x1 = 40. **Is column 40 part of it?**

📖 **New word: half-open range** — a range that **includes its start** but **not its end**. We write it **[x0, x1)**: the square bracket `[` means "included", the round bracket `)` means "not included".

📖 **New word: inclusive range** — a range that includes both ends: [x0, x1].

In this book, rectangles are **half-open**: columns x0, x0 + 1, …, x1 − 1. Column x1 is **not** included.

```
column:  8   9  10  11  12  …  38  39  40  41
              │                      │   │
              ● ━━━━━━━━━━━━━━━━━━━━ ●   ○
              x0 (included)    x1 − 1    x1 (not included)
```

🔢 **Maths: how many columns?**

> half-open [10, 40): 40 − 10 = **30** columns ✓ (exactly the width)
> inclusive [10, 40]: 40 − 10 + 1 = **31** columns (one more!)

With half-open ranges, **width = x1 − x0**, with no "+ 1". The same rule you already use in C++:

```cpp
for (int x = x0; x < x1; ++x)   // half-open: x1 is not visited
```

and the same rule as `std::vector`: indexes go from 0 to `size()`, not including `size()` (Chapter 3).

### Why half-open ranges are better

📖 **New word: off-by-one error** — a bug where a count or position is wrong by exactly 1.

Put two rectangles **side by side**: [0, 10) and [10, 20).

> left covers columns 0–9
> right covers columns 10–19
> together: 0–19 — **every** column exactly **once**. No gap, no overlap.

Now try inclusive ranges: [0, 10] and [10, 20].

> left covers 0–10, right covers 10–20
> column **10 is painted twice** (an overlap)

And if you "fix" it with [0, 9] and [10, 20], the left one is 10 wide but the right one is 11 wide. Inclusive ranges always make you think about "+ 1" and "− 1". Half-open ranges make it automatic:

| Fact | Half-open | Inclusive |
|---|---|---|
| width | x1 − x0 | x1 − x0 + 1 |
| two rectangles touch exactly when | a.x1 = b.x0 | a.x1 + 1 = b.x0 |
| empty when | x1 ≤ x0 | x1 < x0 |
| split [0, 20) in the middle | [0, 10) + [10, 20) | [0, 9] + [10, 19] |

Painting a pixel **twice** looks harmless with solid colours. But with **alpha** (Chapter 18), a pixel painted twice at 50% becomes 75% (Chapter 18, Example 2). Overlaps then show up as darker lines. Half-open ranges stop this.

🧠 **Remember:** A `Rect` covers columns **x0 ≤ x < x1** and rows **y0 ≤ y < y1**. Width = x1 − x0. Height = y1 − y0.

---

## 19.4 Normalising a rectangle

📖 **New word: normalise** — to put values into a standard form.

What if someone gives us the two corners in the "wrong" order — bottom-right first? Or a negative width?

```
fromCorners(50, 30, 20, 10)   // (50, 30) and (20, 10): which is top-left?
makeRect(100, 50, -30, 20)    // a width of −30
```

A negative width can be read as "the rectangle goes 30 pixels to the **left** of x". To handle every case the same way, we **normalise**: always put the **smaller** x into x0 and the **bigger** into x1, and the same for y.

🔢 **Maths: fromCorners(50, 30, 20, 10)**

> x0 = min(50, 20) = **20**, x1 = max(50, 20) = **50**
> y0 = min(30, 10) = **10**, y1 = max(30, 10) = **30**
> → [20, 50) × [10, 30), size 30 × 20

🔢 **Maths: makeRect(100, 50, −30, 20)**

> corners: (100, 50) and (100 − 30, 50 + 20) = (70, 70)
> normalised: x0 = 70, x1 = 100, y0 = 50, y1 = 70
> → [70, 100) × [50, 70), size 30 × 20

Our `makeRect` simply computes the two corners and calls `fromCorners`, so it is normalised too.

---

## 19.5 Empty rectangles

A rectangle with width 0 or height 0 has **no pixels**. After normalising, a rectangle is empty when:

> **x1 ≤ x0 or y1 ≤ y0**

| Rect | Empty? | Why |
|---|---|---|
| [5, 5) × [0, 10) | yes | width 0 |
| [0, 10) × [3, 4) | no | 10 × 1 — one row |
| [0, 10) × [7, 2) | yes | y1 < y0 (only happens if we did not normalise, or after an intersection — next section) |

Drawing an empty rectangle does **nothing**, and our loops handle that naturally: `for (x = x0; x < x1; …)` runs zero times when x1 ≤ x0.

---

## 19.6 Where do two rectangles overlap?

📖 **New word: intersection** — the part where two shapes overlap.

Take A = [0, 100) × [0, 100) and B = [60, 160) × [70, 170).

```
 0         60       100      160
 ┌──────────┬────────┐                  0
 │    A     │        │
 │          │ overlap│                  70
 │          ├────────┼────────┐
 │          │        │        │
 └──────────┼────────┘        │         100
            │      B          │
            └─────────────────┘         170
```

Look at the x direction only. The overlap **starts** where the **later** of the two starts is, and **ends** where the **earlier** of the two ends is:

> **x0 = max(A.x0, B.x0)**
> **x1 = min(A.x1, B.x1)**

And the same for y.

🔢 **Maths: A ∩ B** (∩ means "intersection")

> x0 = max(0, 60) = 60
> x1 = min(100, 160) = 100
> y0 = max(0, 70) = 70
> y1 = min(100, 170) = 100
> → [60, 100) × [70, 100), size **40 × 30**

### When they do not overlap

A = [0, 10) × [0, 10), B = [20, 30) × [0, 10):

> x0 = max(0, 20) = 20
> x1 = min(10, 30) = 10
> x1 ≤ x0 → **empty** — no overlap ✓

The same formula tells us **both** "where" and "whether". If the result is empty, the rectangles do not overlap. In our code, an empty result is always returned as the plain `Rect{}` = [0, 0) × [0, 0), so it is easy to recognise.

🧠 **Remember:** Intersection = **max of the starts, min of the ends**. Empty means no overlap.

---

## 19.7 Clipping to the image

📖 **New word: clip** — to cut a shape so only the part inside an area is left.

The image itself is a rectangle: **[0, width) × [0, height)**. So clipping a shape to the image is just an **intersection** with that rectangle.

🔢 **Maths: a ground rectangle that is too big**

> ground = makeRect(−50, 200, 400, 100) = [−50, 350) × [200, 300)
> image (320 × 240) = [0, 320) × [0, 240)
> x0 = max(−50, 0) = 0, x1 = min(350, 320) = 320
> y0 = max(200, 0) = 200, y1 = min(300, 240) = 240
> → [0, 320) × [200, 240), size **320 × 40**

### Why clip? `setPixel` already ignores outside pixels!

Yes — so clipping is not needed for **safety**. It is needed for **speed**.

🔢 **Maths: filling a huge rectangle without clipping**

> Imagine a rectangle [−1,000,000, 1,000,000) × [−1,000,000, 1,000,000).
> That is 2,000,000 × 2,000,000 = 4,000,000,000,000 (four trillion) pixels to try.
> Even at a billion pixels per second, that takes over an hour — for a 320 × 240 picture!
> With clipping: only 320 × 240 = 76,800 pixels.

Shapes can easily end up huge or far outside: a zoomed-in drawing, a moving object in an animation, a mistake in a calculation. Clipping **first** makes the work depend on the **image** size, not on the shape size.

After clipping, every pixel we visit is inside the image, so `setPixel`'s own check always says "yes". That costs a little time, but it keeps the code safe and simple.

---

## 19.8 Filling and outlining

📖 **New word: fill** — to colour the whole inside of a shape.

📖 **New word: stroke** (or **outline**) — to colour only the border.

**Filling** is two loops over the clipped rectangle:

```cpp
for (int y = clipped.y0; y < clipped.y1; ++y)
    for (int x = clipped.x0; x < clipped.x1; ++x)
        image.setPixel(x, y, c);
```

**Outlining** with thickness t: the border is made of **four strips**, all **inside** the rectangle. The trick is to cut the strips so that the corners are **not painted twice**:

```
 ┌───────────────────────────┐
 │           top             │  ← full width, t rows
 ├────┬─────────────────┬────┤
 │    │                 │    │
 │left│    (not drawn)  │right  ← only the rows BETWEEN top and bottom
 │    │                 │    │
 ├────┴─────────────────┴────┤
 │          bottom           │  ← full width, t rows
 └───────────────────────────┘
```

| Strip | x range | y range |
|---|---|---|
| top | [x0, x1) | [y0, y0 + t) |
| bottom | [x0, x1) | [y1 − t, y1) |
| left | [x0, x0 + t) | [y0 + t, y1 − t) |
| right | [x1 − t, x1) | [y0 + t, y1 − t) |

🔢 **Maths: a 10 × 6 rectangle with thickness 2**

> top: 10 × 2 = 20 pixels
> bottom: 10 × 2 = 20 pixels
> left: 2 × (6 − 4) = 2 × 2 = 4 pixels
> right: 4 pixels
> total: 20 + 20 + 4 + 4 = **48**
> check: all pixels 10 × 6 = 60, inside hole (10 − 4) × (6 − 4) = 6 × 2 = 12, 60 − 12 = **48** ✓

Each border pixel is painted **exactly once** — important for alpha.

### A thickness that is too big

If t is bigger than the width or the height, the strips would reach outside the rectangle. So our code first limits t to the smaller of the width and height.

But there is a smaller problem when t is more than **half** the width or height:

> a rectangle 6 rows high, with t = 4:
> top strip: rows [0, 4), bottom strip: rows [6 − 4, 6) = [2, 6)
> rows 2 and 3 are in **both** strips → painted twice

(The side strips are then empty, because [0 + 4, 6 − 4) = [4, 2) is empty.)

For a solid colour this does not matter: painting the same colour twice gives the same result. For an outline drawn with alpha it would. Practice 7 shows the small change that fixes it: when 2t reaches the width or height, simply fill the whole rectangle.

---

## 19.9 Rectangles with alpha

With Chapter 18's `blendPixel`, a see-through rectangle is the same double loop, calling `blendPixel` instead of `setPixel`. We use it in our scene for a soft white "cloud panel" in the sky.

Because the loops visit each pixel **once**, the alpha is applied exactly once everywhere. (If you draw **two** see-through rectangles that overlap, the overlap **is** blended twice — that is correct: two layers of glass.)

---

## 19.10 Rectangles with non-whole corners

📖 **New word: ceiling** — the smallest whole number that is **not smaller** than a number. ceil(2.3) = 3, ceil(5.0) = 5, ceil(−1.5) = −1. In C++: `std::ceil` from `<cmath>`.

Later, shapes will have corners like x = 2.3 (for example, after rotating or scaling, Part 5). Which pixels belong to a rectangle from x = 2.3 to x = 5.6?

We use the **pixel-centre rule** (Chapter 3, Section 3.9):

> **A pixel belongs to the shape if its centre (x + 0.5, y + 0.5) is inside the shape.**

🔢 **Maths: columns for [2.3, 5.6)**

| Column | Centre | 2.3 ≤ centre < 5.6? |
|---|---|---|
| 1 | 1.5 | no |
| 2 | 2.5 | **yes** |
| 3 | 3.5 | **yes** |
| 4 | 4.5 | **yes** |
| 5 | 5.5 | **yes** |
| 6 | 6.5 | no |

So columns 2 to 5 → the whole-number range **[2, 6)**.

There is a neat formula for this:

> **first column = ceil(a − 0.5)**, **end column = ceil(b − 0.5)**

> ceil(2.3 − 0.5) = ceil(1.8) = **2**
> ceil(5.6 − 0.5) = ceil(5.1) = **6**
> → [2, 6) ✓

Why does it work? A column c is inside when a ≤ c + 0.5, which means c ≥ a − 0.5; the first whole number that is ≥ a − 0.5 is ceil(a − 0.5). The same reasoning gives the end.

This rule is important because it means two shapes that **touch** at x = 5.6 still share no pixels and leave no gaps — the half-open idea again, now for non-whole numbers. We use it for triangles in Chapter 24.

---

## Code, part 1: `draw.h`

File: `common/draw.h` (new). It includes `alpha.h`, so shapes can be drawn with transparency.

```cpp
#ifndef DRAW_H
#define DRAW_H

#include <algorithm>
#include "alpha.h"

struct Rect {
    int x0 = 0;
    int y0 = 0;
    int x1 = 0;
    int y1 = 0;
};

inline Rect fromCorners(int ax, int ay, int bx, int by) {
    return Rect{std::min(ax, bx), std::min(ay, by), std::max(ax, bx), std::max(ay, by)};
}

inline Rect makeRect(int x, int y, int width, int height) {
    return fromCorners(x, y, x + width, y + height);
}

inline int rectWidth(Rect r) {
    return r.x1 - r.x0;
}

inline int rectHeight(Rect r) {
    return r.y1 - r.y0;
}

inline bool isEmpty(Rect r) {
    return r.x1 <= r.x0 || r.y1 <= r.y0;
}

inline bool contains(Rect r, int x, int y) {
    return x >= r.x0 && x < r.x1 && y >= r.y0 && y < r.y1;
}

inline Rect intersect(Rect a, Rect b) {
    Rect r{std::max(a.x0, b.x0), std::max(a.y0, b.y0),
           std::min(a.x1, b.x1), std::min(a.y1, b.y1)};
    if (isEmpty(r)) {
        return Rect{};
    }
    return r;
}

inline Rect clipToImage(Rect r, const Image& image) {
    return intersect(r, Rect{0, 0, image.width(), image.height()});
}

inline void fillRect(Image& image, Rect r, Colour c) {
    Rect clipped = clipToImage(r, image);
    for (int y = clipped.y0; y < clipped.y1; ++y) {
        for (int x = clipped.x0; x < clipped.x1; ++x) {
            image.setPixel(x, y, c);
        }
    }
}

inline void fillRectAlpha(Image& image, Rect r, Colour c, double alpha) {
    Rect clipped = clipToImage(r, image);
    for (int y = clipped.y0; y < clipped.y1; ++y) {
        for (int x = clipped.x0; x < clipped.x1; ++x) {
            blendPixel(image, x, y, c, alpha);
        }
    }
}

inline void strokeRect(Image& image, Rect r, int thickness, Colour c) {
    if (isEmpty(r) || thickness <= 0) {
        return;
    }
    int t = std::min(thickness, std::min(rectWidth(r), rectHeight(r)));
    fillRect(image, Rect{r.x0, r.y0, r.x1, r.y0 + t}, c);
    fillRect(image, Rect{r.x0, r.y1 - t, r.x1, r.y1}, c);
    fillRect(image, Rect{r.x0, r.y0 + t, r.x0 + t, r.y1 - t}, c);
    fillRect(image, Rect{r.x1 - t, r.y0 + t, r.x1, r.y1 - t}, c);
}

#endif
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef DRAW_H` / `#define DRAW_H` | Include guard. |
| 4 | `#include <algorithm>` | `std::min` and `std::max`. |
| 5 | `#include "alpha.h"` | `blendPixel` (Chapter 18), and through it everything else. |
| 7–12 | `struct Rect { int x0 = 0; int y0 = 0; int x1 = 0; int y1 = 0; };` | A rectangle as two corners. It covers **x0 ≤ x < x1** and **y0 ≤ y < y1** (half-open, Section 19.3). The default is the empty rectangle. |
| 14 | `inline Rect fromCorners(int ax, int ay, int bx, int by) {` | Make a rectangle from any two opposite corners. |
| 15 | `return Rect{std::min(ax, bx), std::min(ay, by), std::max(ax, bx), std::max(ay, by)};` | **Normalise**: smaller values into x0/y0, bigger into x1/y1 (Section 19.4). |
| 16 | `}` | End. |
| 18 | `inline Rect makeRect(int x, int y, int width, int height) {` | Make a rectangle from position + size (Section 19.2). |
| 19 | `return fromCorners(x, y, x + width, y + height);` | Turn it into two corners, then normalise. Negative sizes work too. |
| 20 | `}` | End. |
| 22–24 | `inline int rectWidth(Rect r) { return r.x1 - r.x0; }` | Width = x1 − x0. No "+ 1", because the range is half-open. |
| 26–28 | `inline int rectHeight(Rect r) { return r.y1 - r.y0; }` | Height = y1 − y0. |
| 30–32 | `inline bool isEmpty(Rect r) { return r.x1 <= r.x0 \|\| r.y1 <= r.y0; }` | No pixels when the width or height is zero or less (Section 19.5). |
| 34–36 | `inline bool contains(Rect r, int x, int y) { return x >= r.x0 && x < r.x1 && y >= r.y0 && y < r.y1; }` | Is pixel (x, y) inside? Note `>=` for the start and `<` for the end: half-open. This is the same test as `isInside` from Chapter 3, which is just `contains` for the rectangle [0, width) × [0, height). |
| 38 | `inline Rect intersect(Rect a, Rect b) {` | Where do two rectangles overlap? (Section 19.6.) |
| 39–40 | `Rect r{std::max(a.x0, b.x0), std::max(a.y0, b.y0), std::min(a.x1, b.x1), std::min(a.y1, b.y1)};` | Max of the starts, min of the ends. |
| 41–43 | `if (isEmpty(r)) { return Rect{}; }` | No overlap: give back the standard empty rectangle, so odd values like [20, 10) never escape. |
| 44–45 | `return r;` `}` | Otherwise, the overlap. |
| 47 | `inline Rect clipToImage(Rect r, const Image& image) {` | Cut a rectangle to the image (Section 19.7). |
| 48–49 | `return intersect(r, Rect{0, 0, image.width(), image.height()});` `}` | The image is the rectangle [0, width) × [0, height). |
| 51 | `inline void fillRect(Image& image, Rect r, Colour c) {` | Fill a rectangle with a solid colour. |
| 52 | `Rect clipped = clipToImage(r, image);` | Clip **first**, so we never loop over pixels outside the image. |
| 53–54 | `for (int y = clipped.y0; y < clipped.y1; ++y) { for (int x = clipped.x0; x < clipped.x1; ++x) {` | Every pixel of the clipped rectangle, with half-open loops. |
| 55 | `image.setPixel(x, y, c);` | Plot it. |
| 56–58 | `}` `}` `}` | End. |
| 60–67 | `inline void fillRectAlpha(Image& image, Rect r, Colour c, double alpha) { ... blendPixel(image, x, y, c, alpha); ... }` | The same, but **blending** each pixel with alpha (Section 19.9). |
| 69 | `inline void strokeRect(Image& image, Rect r, int thickness, Colour c) {` | Draw the outline of a rectangle, inside its edges (Section 19.8). |
| 70–72 | `if (isEmpty(r) \|\| thickness <= 0) { return; }` | Nothing to draw. |
| 73 | `int t = std::min(thickness, std::min(rectWidth(r), rectHeight(r)));` | Never thicker than the rectangle itself. |
| 74 | `fillRect(image, Rect{r.x0, r.y0, r.x1, r.y0 + t}, c);` | The top strip: full width, t rows. |
| 75 | `fillRect(image, Rect{r.x0, r.y1 - t, r.x1, r.y1}, c);` | The bottom strip: full width, the last t rows. |
| 76 | `fillRect(image, Rect{r.x0, r.y0 + t, r.x0 + t, r.y1 - t}, c);` | The left strip: t columns, only **between** the top and bottom strips, so the corners are not painted twice. |
| 77 | `fillRect(image, Rect{r.x1 - t, r.y0 + t, r.x1, r.y1 - t}, c);` | The right strip, the same way. |
| 78 | `}` | End. |
| 80 | `#endif` | End of the include guard. |

---

## Code, part 2: a house made of rectangles

File: `ch19/rectangles.cpp`

```cpp
#include <iostream>
#include <string>
#include "draw.h"

void printRect(const std::string& label, Rect r) {
    std::cout << label << ": (" << r.x0 << ", " << r.y0 << ") to (" << r.x1 << ", " << r.y1
              << "), " << rectWidth(r) << " x " << rectHeight(r);
    if (isEmpty(r)) {
        std::cout << " (empty)";
    }
    std::cout << "\n";
}

int main() {
    printRect("makeRect(10, 20, 30, 40)", makeRect(10, 20, 30, 40));
    printRect("fromCorners(50, 30, 20, 10)", fromCorners(50, 30, 20, 10));
    printRect("overlap", intersect(makeRect(0, 0, 100, 100), makeRect(60, 70, 100, 100)));
    printRect("no overlap", intersect(makeRect(0, 0, 10, 10), makeRect(20, 0, 10, 10)));

    Image scene(320, 240);
    for (int y = 0; y < scene.height(); ++y) {
        double t = static_cast<double>(y) / (scene.height() - 1);
        Colour sky = lerpLinear(Colour{60, 120, 220}, Colour{200, 230, 255}, t);
        fillRect(scene, Rect{0, y, scene.width(), y + 1}, sky);
    }
    printRect("ground, clipped", clipToImage(makeRect(-50, 200, 400, 100), scene));
    fillRect(scene, makeRect(-50, 200, 400, 100), Colour{70, 140, 60});

    const Rect house = makeRect(90, 110, 140, 90);
    fillRect(scene, house, Colour{230, 200, 150});
    strokeRect(scene, house, 3, Colour{90, 60, 40});
    for (int step = 0; step < 5; ++step) {
        fillRect(scene, makeRect(80 + step * 16, 110 - (step + 1) * 10, 160 - step * 32, 10),
                 Colour{170, 50, 40});
    }
    fillRect(scene, makeRect(145, 150, 30, 50), Colour{110, 70, 40});
    for (int i = 0; i < 2; ++i) {
        Rect window = makeRect(105 + i * 85, 125, 30, 25);
        fillRect(scene, window, Colour{250, 240, 170});
        strokeRect(scene, window, 2, colours::white);
    }
    fillRectAlpha(scene, makeRect(200, 20, 160, 45), colours::white, 0.6);

    int count = 0;
    Rect left = makeRect(0, 0, 10, 1);
    Rect right = makeRect(10, 0, 10, 1);
    for (int x = 0; x < 20; ++x) {
        if (contains(left, x, 0)) {
            ++count;
        }
        if (contains(right, x, 0)) {
            ++count;
        }
    }
    std::cout << "touching rectangles cover " << count << " pixels of 20\n";

    if (!scene.savePPM("house.ppm")) {
        std::cout << "could not write house.ppm\n";
        return 1;
    }
    return 0;
}
```

### Line by line

**Printing and the four tests (lines 1–18)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#include <iostream>` / `<string>` | Printing and labels. |
| 3 | `#include "draw.h"` | Our new header — it brings in everything from earlier chapters too. |
| 5 | `void printRect(const std::string& label, Rect r) {` | Print a rectangle's corners and size. |
| 6–7 | `std::cout << label << ": (" << r.x0 << ... << rectHeight(r);` | "label: (x0, y0) to (x1, y1), w x h". |
| 8–10 | `if (isEmpty(r)) { std::cout << " (empty)"; }` | Mark empty rectangles. |
| 11–12 | `std::cout << "\n";` `}` | End of the line, end of the function. |
| 14 | `int main() {` | The program starts here. |
| 15 | `printRect("makeRect(10, 20, 30, 40)", makeRect(10, 20, 30, 40));` | Section 19.2: expect (10, 20) to (40, 60), 30 × 40. |
| 16 | `printRect("fromCorners(50, 30, 20, 10)", fromCorners(50, 30, 20, 10));` | Section 19.4: expect (20, 10) to (50, 30). |
| 17 | `printRect("overlap", intersect(makeRect(0, 0, 100, 100), makeRect(60, 70, 100, 100)));` | Section 19.6: expect (60, 70) to (100, 100), 40 × 30. |
| 18 | `printRect("no overlap", intersect(makeRect(0, 0, 10, 10), makeRect(20, 0, 10, 10)));` | Two rectangles far apart: expect the empty rectangle. |

**The scene (lines 20–42)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 20 | `Image scene(320, 240);` | Our picture. |
| 21 | `for (int y = 0; y < scene.height(); ++y) {` | For each row of the sky… |
| 22 | `double t = static_cast<double>(y) / (scene.height() - 1);` | t from 0 (top) to 1 (bottom) (Chapter 13). |
| 23 | `Colour sky = lerpLinear(Colour{60, 120, 220}, Colour{200, 230, 255}, t);` | A blue sky that gets paler toward the horizon, mixed in linear light (Chapter 17). |
| 24 | `fillRect(scene, Rect{0, y, scene.width(), y + 1}, sky);` | A rectangle **one row high**: [y, y + 1). A row is just a very thin rectangle. |
| 25 | `}` | End of the sky. |
| 26 | `printRect("ground, clipped", clipToImage(makeRect(-50, 200, 400, 100), scene));` | Show the clipping of Section 19.7: expect (0, 200) to (320, 240). |
| 27 | `fillRect(scene, makeRect(-50, 200, 400, 100), Colour{70, 140, 60});` | The green ground. It sticks out on three sides; `fillRect` clips it. |
| 29 | `const Rect house = makeRect(90, 110, 140, 90);` | The house wall: [90, 230) × [110, 200). It ends exactly where the ground starts (y = 200): touching, no gap, no overlap. |
| 30 | `fillRect(scene, house, Colour{230, 200, 150});` | Fill the wall with a sand colour. |
| 31 | `strokeRect(scene, house, 3, Colour{90, 60, 40});` | A dark brown outline, 3 pixels thick, **inside** the wall. |
| 32 | `for (int step = 0; step < 5; ++step) {` | The roof is made of 5 steps (true triangles come in Chapter 24). |
| 33 | `fillRect(scene, makeRect(80 + step * 16, 110 - (step + 1) * 10, 160 - step * 32, 10),` | Each step is 10 rows high, 32 pixels narrower than the one below (16 on each side), and 10 rows higher. Step 0 sits right on top of the wall (rows 100–109) and is 160 wide — wider than the wall, like real eaves. |
| 34 | `Colour{170, 50, 40});` | A tile red. |
| 35 | `}` | End of the roof. |
| 36 | `fillRect(scene, makeRect(145, 150, 30, 50), Colour{110, 70, 40});` | The door: [145, 175) × [150, 200), in the middle of the wall (the wall's middle is (90 + 230) ÷ 2 = 160, and the door's middle is (145 + 175) ÷ 2 = 160 ✓). |
| 37 | `for (int i = 0; i < 2; ++i) {` | Two windows. |
| 38 | `Rect window = makeRect(105 + i * 85, 125, 30, 25);` | Left window at x = 105, right window at x = 190. |
| 39 | `fillRect(scene, window, Colour{250, 240, 170});` | A warm light-yellow glass. |
| 40 | `strokeRect(scene, window, 2, colours::white);` | A white frame, 2 pixels thick. |
| 41 | `}` | End of the windows. |
| 42 | `fillRectAlpha(scene, makeRect(200, 20, 160, 45), colours::white, 0.6);` | A see-through white "cloud" panel, 60% opaque. It sticks out on the right; it is clipped. |

**The touching test and saving (lines 44–62)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 44 | `int count = 0;` | How many times any column is covered. |
| 45–46 | `Rect left = makeRect(0, 0, 10, 1);` / `Rect right = makeRect(10, 0, 10, 1);` | [0, 10) and [10, 20): two rectangles that touch (Section 19.3). |
| 47 | `for (int x = 0; x < 20; ++x) {` | Look at columns 0 to 19. |
| 48–53 | `if (contains(left, x, 0)) { ++count; }` and the same for `right` | Count each rectangle that covers this column. |
| 54 | `}` | End of the loop. |
| 55 | `std::cout << "touching rectangles cover " << count << " pixels of 20\n";` | With half-open ranges: exactly 20 — no column missed, none counted twice. |
| 57–60 | `if (!scene.savePPM("house.ppm")) { ...; return 1; }` | Save the picture. |
| 61 | `return 0;` | The program finished with no problem. |
| 62 | `}` | End of `main`. |

Compile:

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common rectangles.cpp -o rectangles
```

### What you should see

```
makeRect(10, 20, 30, 40): (10, 20) to (40, 60), 30 x 40
fromCorners(50, 30, 20, 10): (20, 10) to (50, 30), 30 x 20
overlap: (60, 70) to (100, 100), 40 x 30
no overlap: (0, 0) to (0, 0), 0 x 0 (empty)
ground, clipped: (0, 200) to (320, 240), 320 x 40
touching rectangles cover 20 pixels of 20
```

Open `house.ppm`: a blue sky that gets lighter near the ground, green grass, a sand-coloured house with a brown outline, a stepped red roof, a brown door in the middle, two yellow windows with white frames, and a soft white panel in the top-right corner through which you can still see the sky.

---

## Small examples

### Example 1 — A bar chart

```cpp
const int values[5] = {40, 90, 60, 120, 75};
Image chart(260, 150, colours::white);
for (int i = 0; i < 5; ++i) {
    Rect bar = makeRect(20 + i * 48, 140 - values[i], 32, values[i]);
    fillRect(chart, bar, Colour{70, 130, 200});
}
```

> bar 3: makeRect(20 + 144, 140 − 120, 32, 120) = [164, 196) × [20, 140)

Every bar ends at y = 140 (its **bottom** edge), because images count y **downward** (Chapter 3). A taller bar starts **higher** — at a **smaller** y.

### Example 2 — A grid of tiles with gaps

```cpp
for (int row = 0; row < 4; ++row) {
    for (int col = 0; col < 6; ++col) {
        fillRect(img, makeRect(col * 50 + 5, row * 50 + 5, 40, 40), colours::cyan);
    }
}
```

> each tile is 40 × 40, and tiles are 50 apart → a 10-pixel gap between them (5 on each side)
> tile (col 2, row 1): [105, 145) × [55, 95)

### Example 3 — The intersection of three rectangles

Intersection can be done step by step:

> A = [0, 100) × [0, 100), B = [50, 150) × [20, 80), C = [70, 90) × [0, 200)
> A ∩ B = [50, 100) × [20, 80)
> (A ∩ B) ∩ C = [max(50, 70), min(100, 90)) × [max(20, 0), min(80, 200)) = **[70, 90) × [20, 80)**

### Example 4 — Columns for a rectangle from 0.4 to 3.5

> first = ceil(0.4 − 0.5) = ceil(−0.1) = **0**
> end = ceil(3.5 − 0.5) = ceil(3.0) = **3**
> → columns 0, 1, 2

Check with centres: 0.5 (inside, since 0.4 ≤ 0.5 < 3.5), 1.5, 2.5 (inside), 3.5 (**not** inside, because 3.5 < 3.5 is false) ✓.

---

## Common mistakes

⚠️ **Using `<=` with the end.** `for (x = x0; x <= x1; ...)` draws one column too many. Half-open: `x < x1`.

⚠️ **Width + 1.** With half-open ranges, width = x1 − x0. Adding 1 is an inclusive-range habit.

⚠️ **Not normalising.** A rectangle with x1 < x0 is "empty" to our loops, even though the user meant a real rectangle. Use `fromCorners` or `makeRect`.

⚠️ **Not clipping before looping.** It works, but a huge or far-away shape can take forever.

⚠️ **Outlines that paint corners twice.** With alpha, the corners come out darker. Cut the side strips between the top and bottom strips.

⚠️ **Forgetting that y grows downward.** A bar of height h that stands on y = 140 starts at y = 140 − h, not 140 + h.

---

## Practice

🏋️ **1.** Write the corners of makeRect(5, 8, 12, 3). How many pixels does it have?

🏋️ **2.** Normalise fromCorners(30, 5, 10, 25) and makeRect(40, 40, −10, −20).

🏋️ **3.** Intersect [10, 50) × [10, 50) with [40, 80) × [0, 20). Is it empty?

🏋️ **4.** Clip makeRect(300, −30, 100, 100) to a 320 × 240 image.

🏋️ **5.** How many pixels does strokeRect paint for a 20 × 20 rectangle with thickness 3?

🏋️ **6.** Which columns belong to a rectangle from x = 1.6 to x = 4.4? Use the ceiling formula, then check with centres.

🏋️ **7.** Change `strokeRect` so that a thickness above half the smaller side simply **fills** the rectangle (so strips never overlap, even with alpha). (Hint: compare `2 * thickness` with the width and height.)

🏋️ **8.** Draw a **chessboard**: 8 × 8 squares of 30 pixels, using only `fillRect`.

---

## Answers

**1.**
> x0 = 5, y0 = 8, x1 = 5 + 12 = 17, y1 = 8 + 3 = 11
> [5, 17) × [8, 11) → 12 × 3 = **36 pixels**

**2.**
> fromCorners(30, 5, 10, 25) → x0 = 10, x1 = 30, y0 = 5, y1 = 25 → **[10, 30) × [5, 25)**
> makeRect(40, 40, −10, −20): corners (40, 40) and (30, 20) → **[30, 40) × [20, 40)**

**3.**
> x0 = max(10, 40) = 40, x1 = min(50, 80) = 50
> y0 = max(10, 0) = 10, y1 = min(50, 20) = 20
> → **[40, 50) × [10, 20)**, 10 × 10. Not empty.

**4.**
> rect = [300, 400) × [−30, 70)
> x0 = max(300, 0) = 300, x1 = min(400, 320) = 320
> y0 = max(−30, 0) = 0, y1 = min(70, 240) = 70
> → **[300, 320) × [0, 70)**, 20 × 70

**5.**
> all = 20 × 20 = 400
> hole = (20 − 6) × (20 − 6) = 14 × 14 = 196
> outline = 400 − 196 = **204 pixels**

**6.**
> first = ceil(1.6 − 0.5) = ceil(1.1) = **2**
> end = ceil(4.4 − 0.5) = ceil(3.9) = **4**
> → columns **2 and 3**
> centres: 1.5 (no: 1.5 < 1.6), 2.5 (yes), 3.5 (yes), 4.5 (no: 4.5 ≥ 4.4) ✓

**7.**

```cpp
inline void strokeRect(Image& image, Rect r, int thickness, Colour c) {
    if (isEmpty(r) || thickness <= 0) {
        return;
    }
    if (2 * thickness >= rectWidth(r) || 2 * thickness >= rectHeight(r)) {
        fillRect(image, r, c);
        return;
    }
    int t = thickness;
    // ... the four strips, as before
}
```

When 2t is at least the width (or height), the strips from both sides would meet or overlap, so the outline **is** the whole rectangle.

**8.**

```cpp
Image board(240, 240);
for (int row = 0; row < 8; ++row) {
    for (int col = 0; col < 8; ++col) {
        Colour c = ((row + col) % 2 == 0) ? Colour{240, 220, 180} : Colour{120, 80, 50};
        fillRect(board, makeRect(col * 30, row * 30, 30, 30), c);
    }
}
board.savePPM("chess.ppm");
```

> 8 × 30 = 240, so the board fills the image exactly. Each square is [col × 30, col × 30 + 30) — touching squares, no gaps, thanks to half-open ranges.

---

## Summary

🧠 Every shape is drawn by plotting the **right set of pixels**.

🧠 We store rectangles as **two corners**. `makeRect(x, y, w, h)` and `fromCorners` both **normalise**.

🧠 Rectangles are **half-open**: **x0 ≤ x < x1**. Width = x1 − x0. Touching rectangles share no pixels and leave no gaps.

🧠 Empty: **x1 ≤ x0 or y1 ≤ y0**.

🧠 Intersection = **max of the starts, min of the ends**.

🧠 **Clip** to [0, width) × [0, height) **before** looping — for speed.

🧠 Outlines: four strips **inside** the rectangle, side strips cut between top and bottom so no pixel is painted twice.

🧠 Non-whole corners: a pixel belongs if its **centre** is inside: columns **[ceil(a − 0.5), ceil(b − 0.5))**.

---

## Next chapter

Rectangles only need straight up-and-down and side-to-side edges. In Chapter 20 we draw **lines** in **any** direction. We learn what the **slope** of a line is, and the simplest way to draw one: the **DDA** method, which takes small steps along the line and rounds each point to a pixel.
