# Chapter 25 — Filling Shapes: Scanline Fill and Flood Fill

> **Part 4 · Chapter 25 of 82**
> **You need:** Chapters 1–24 · **You will make:** `fill.h` (scanline polygon fill with two fill rules, shapes with holes, masks, flood fill), `stars.ppm`, `holes.ppm` and `venn.ppm`

---

## What you will learn

- Why the triangle fan of Chapter 24 fails for shapes with **dents**.
- The **ray test**: count how many times a line from a point crosses the edges.
- **Scanline filling**: fill any polygon row by row.
- How to treat corners that lie exactly on a row, so nothing is counted twice.
- Two **fill rules** — **even-odd** and **non-zero** — and why a star looks different with each.
- Shapes with **holes** (a frame, a letter "O"), and why the direction of the inner edge matters.
- **Masks**: a yes/no grid that remembers which pixels belong to a region.
- **Flood fill**, the "paint bucket": 4-way and 8-way, and why 8-way can **leak**.
- Why flood fill should **not** use recursion, and how a **stack** solves it.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **scanline** | One row of pixels. "Scanline fill" fills a shape one row at a time. |
| **ray** | A straight line that starts at a point and goes on forever in one direction. |
| **crossing** | A place where a row (or a ray) cuts through an edge of the shape. |
| **fill rule** | The rule that decides which parts of a shape count as "inside" when edges cross each other. |
| **even-odd rule** | Inside if a ray crosses the edges an **odd** number of times. |
| **winding number** | How many times the edges wind around a point (going round one way counts +1, the other way −1). |
| **non-zero rule** | Inside if the winding number is **not 0**. |
| **path** | One closed chain of points. A shape can have several paths (for example, an outside and a hole). |
| **mask** | A grid of yes/no values, one for each pixel, saying which pixels belong to something. |
| **flood fill** | Filling a connected area of one colour, by spreading from a starting pixel to its neighbours. |
| **seed** | The starting pixel of a flood fill. |
| **leak** | When a flood fill escapes through a gap in an outline. |
| **recursion** | A function that calls itself. |
| **stack** | A list where you always add to the end and take from the end ("last in, first out"). |
| **stack overflow** | A crash that happens when a program uses up its call stack memory. |

---

## 25.1 Shapes with dents

In Chapter 24 we filled convex polygons with a **fan** of triangles. Practice 7 of that chapter showed the problem: the arrow-head (0, 0), (10, 5), (0, 10), (3, 5) has a **dent**, and the fan from the first corner fills the dent in.

Real shapes have dents all the time: stars, letters like "C", "E" and "L", outlines of countries, a cartoon cloud. We want **one** method that fills any polygon correctly.

The idea is very old and very simple. Look at one **row** of pixels at a time.

📖 **New word: scanline** — one row of pixels (from old TV screens, which drew the picture row by row, "scanning" across).

```
  row y:   ......#####.......#######.....
                 ↑    ↑      ↑      ↑
               enter leave  enter  leave
```

As we walk along a row from left to right, we **enter** the shape when we cross an edge, and **leave** it when we cross the next edge. So:

1. Find every place where the row crosses an edge.
2. Sort these places from left to right.
3. Fill between the 1st and 2nd, between the 3rd and 4th, and so on.

That is scanline filling. It does not care about dents, and it works for any number of edges.

---

## 25.2 The ray test

Why does "fill between pairs" work? Here is the idea behind it.

📖 **New word: ray** — a straight line that starts at a point and goes on forever in one direction.

📖 **New word: crossing** — a place where the ray cuts through an edge.

Stand at a point P and shoot a ray to the **left** (to x = −∞). Count the crossings.

- Every time the ray crosses an edge, it goes from inside to outside, or from outside to inside.
- Far away to the left, it is definitely **outside**.
- So, coming back from far away: 0 crossings = outside, 1 crossing = inside, 2 = outside again, 3 = inside, …

🧠 **Remember:** P is inside if its ray crosses the edges an **odd** number of times (1, 3, 5, …).

```
     ┌──────────┐
     │   ┌──┐   │        point ●:  ray to the left crosses 1 edge   → inside
  ←──┼─● │  │   │        point ○:  ray to the left crosses 2 edges  → outside
     │   └──┘   │
     └──────────┘
```

Scanline filling uses this test for a whole row at once. The pixels after the 1st crossing have 1 crossing to their left (inside). After the 2nd crossing they have 2 (outside), and so on. That is why we fill between the 1st and 2nd crossings, the 3rd and 4th, …

---

## 25.3 Where does a row cross an edge?

We test the row at the height of the **pixel centres**: for row y, that is **sy = y + 0.5** (the same pixel-centre rule as always).

An edge goes from A to B. It crosses the row if sy is between A.y and B.y. Where? We use **lerp** (Chapter 13) along the edge:

> t = (sy − A.y) / (B.y − A.y) — how far along the edge (from 0 to 1) the row is
> **x = A.x + t × (B.x − A.x)** — the crossing point

🔢 **Maths: an edge from A = (2, 1) to B = (8, 13), row y = 6**

> sy = 6.5
> t = (6.5 − 1) / (13 − 1) = 5.5 / 12 = 0.458
> x = 2 + 0.458 × 6 = 2 + 2.75 = **4.75**

### From a crossing to pixels

The row crosses at x = xa (entering) and x = xb (leaving). Which pixels do we fill? The pixels whose **centre** x + 0.5 is between them: xa ≤ x + 0.5 < xb. That gives (with the rule from Chapter 19):

> first pixel = ceil(xa − 0.5), and stop **before** ceil(xb − 0.5)

🔢 **Maths: crossings at 2.49 and 7.90**

> first = ceil(2.49 − 0.5) = ceil(1.99) = **2**
> stop = ceil(7.90 − 0.5) = ceil(7.40) = **8**
> → pixels 2, 3, 4, 5, 6, 7 (centres 2.5 to 7.5, all between 2.49 and 7.90 ✓)

### Horizontal edges

If A.y = B.y, the edge is flat. A flat row never "crosses" a flat edge (it either misses it or lies on top of it), so we simply **skip** horizontal edges. The edges next to it take care of the shape.

---

## 25.4 Corners exactly on a row

What if the row goes **exactly through a corner** of the polygon? Two edges meet there. Should we count 1 crossing, or 2?

Look at this diamond, with corners on pixel-centre rows:

> (5, 0.5) top, (9, 4.5) right, (5, 8.5) bottom, (1, 4.5) left

```
           ● (5, 0.5)
         ╱   ╲
       ╱       ╲
     ● (1, 4.5)  ● (9, 4.5)     ← row 4 (sy = 4.5) goes through two corners
       ╲       ╱
         ╲   ╱
           ● (5, 8.5)
```

Row 4 (sy = 4.5) touches the left corner and the right corner. If we count each corner **twice** (once for each edge), we get 4 crossings: 1, 1, 9, 9. We fill [1, 1) — nothing — and [9, 9) — nothing. The widest row of the diamond would be **empty**!

The fix is the **half-open** idea again (Chapter 19). Each edge covers the rows from its top **up to, but not including,** its bottom:

> **an edge counts for the row if top ≤ sy < bottom**

At the right corner (9, 4.5):
- The upper edge (5, 0.5) → (9, 4.5) covers 0.5 ≤ sy < 4.5. Row 4.5 is **not** included.
- The lower edge (9, 4.5) → (5, 8.5) covers 4.5 ≤ sy < 8.5. Row 4.5 **is** included.

So the corner is counted exactly **once**. Row 4 gets 2 crossings, at 1 and 9, and is filled from pixel 1 to pixel 8 — the widest row. ✓

At the **top** corner (5, 0.5), both edges start there (it is the top of both), so both include row 0.5: 2 crossings, both at x = 5. We fill [5, 5): nothing. That is correct: the shape is just a point there. At the bottom corner (5, 8.5), both edges end there, so neither counts: 0 crossings. Also correct.

🧠 **Remember:** with "top ≤ sy < bottom", every row crosses a closed shape an **even** number of times, so the crossings always pair up.

💡 This is the same idea as the **top-left rule** of Chapter 24: top included, bottom not; left included (ceil(xa − 0.5)), right not. Because the rules are the same, `fillPolygon` and `fillTriangle` give the same pixels for a triangle. Our program checks one triangle, and we tested 2000 random triangles with whole and half-number corners: all the same.

---

## 25.5 When edges cross each other: two fill rules

A polygon's edges can **cross each other**. The classic example is a **star** drawn with one line, without lifting the pen: you visit the five points of a pentagon, always skipping one.

```
              0
             ╱ ╲
     4 ─────╳───╳───── 1          order: 0 → 2 → 4 → 1 → 3 → back to 0
        ╲  ╱     ╲  ╱
         ╳         ╳
        ╱  ╲     ╱  ╲
       3     ╲ ╱     2
```

The lines cross each other and make a small **pentagon** in the middle. Is that middle part inside the star or not? There are two common answers.

📖 **New word: fill rule** — the rule that decides this.

### Rule 1: even-odd

📖 **New word: even-odd rule** — inside if the ray crosses the edges an **odd** number of times (Section 25.2).

From the middle pentagon, a ray to the left crosses **2** edges (the two star lines in the way). 2 is even → **outside**. So the even-odd rule draws the star with an **empty middle**.

### Rule 2: non-zero

This rule also looks at the **direction** of each edge.

📖 **New word: winding number** — walk along the path. Each edge going **down** the screen counts **+1** when the ray crosses it; each edge going **up** counts **−1**. Add them up.

📖 **New word: non-zero rule** — inside if the winding number is **not 0**.

From the middle pentagon, the two edges that the ray crosses both go **up** (−1 and −1): the winding number is **−2**. Not 0 → **inside**. So the non-zero rule fills the middle: a solid star.

🔢 **Maths: one row of our small star, row 8 (sy = 8.5)**

Our program's star has its centre at (10.5, 10.5) and radius 10. Row 8 crosses four edges:

| crossing x | edge goes | running winding | even-odd (count so far) | pixels until the next crossing |
|---|---|---|---|---|
| 2.489 | up (−1) | −1 | 1 → inside | 2 … 7 |
| 7.901 | up (−1) | −2 | 2 → outside | 8 … 12 |
| 13.099 | down (+1) | −1 | 3 → inside | 13 … 18 |
| 18.511 | down (+1) | 0 | 4 → outside | — |

> even-odd fills pixels 2–7 and 13–18: `..######.....######..`
> non-zero fills 2–7, 8–12 **and** 13–18: `..#################..`

The program prints both stars:

```
star, even-odd rule:              star, non-zero rule:
  .....................             .....................
  ..........#..........             ..........#..........
  ..........#..........             ..........#..........
  ..........#..........             ..........#..........
  .........###.........             .........###.........
  .........###.........             .........###.........
  .........###.........             .........###.........
  .#######.....#######.             .###################.
  ..######.....######..             ..#################..
  ....####.....####....             ....#############....
  .....##.......##.....             .....###########.....
  .....................             .......#######.......
  .......#.....#.......             .......#######.......
  ......###...###......             ......#########......
  ......####.####......             ......####.####......
  ......###...###......             ......###...###......
  .....##.......##.....             .....##.......##.....
  .....#.........#.....             .....#.........#.....
  .....................             .....................
  .....................             .....................
```

(The program prints them one below the other; here they are side by side.) Even-odd: **78** pixels. Non-zero: **115** pixels. The difference, 37 pixels, is the middle pentagon. (In such a tiny star, the thin points look broken; in `stars.ppm` with radius 100, they are smooth.)

### The star's corners, without sine and cosine

The five corners of a star sit on a circle, at equal angles. To compute them we normally use **sine** and **cosine**, which we learn in Chapter 30. For now, we just use the numbers. For a circle of radius 1, the five points (starting at the top and going clockwise) are:

| corner | x | y |
|---|---|---|
| 0 (top) | 0 | −1 |
| 1 | 0.9511 | −0.3090 |
| 2 | 0.5878 | 0.8090 |
| 3 | −0.5878 | 0.8090 |
| 4 | −0.9511 | −0.3090 |

For a star with centre (cx, cy) and radius r: corner = (cx + r × x, cy + r × y). We visit them in the order **0, 2, 4, 1, 3**.

🔢 **Maths: check that corner 1 is on the circle of radius 1**

> 0.9511² + 0.3090² = 0.9046 + 0.0955 = 1.0001 ≈ 1 ✓ (the tiny difference is from rounding to 4 digits)

---

## 25.6 Shapes with holes

📖 **New word: path** — one closed chain of points. A **frame** (a square with a square hole) needs **two** paths: the outside square and the inside square.

Our `fillPaths` function takes **several** paths and collects the crossings of **all** of them for each row. Then it applies the fill rule as before.

### With even-odd: holes just work

Inside the hole, a ray to the left crosses the inner square once and the outer square once: 2 crossings → even → outside. **A hole.** ✓

### With non-zero: the direction matters

If both squares go round the **same** way (both clockwise), the two edges the ray crosses go the same direction: −1 and −1 → winding −2 → **inside**. No hole! The inner square is simply painted over.

If the inner square goes round the **other** way, its edge counts +1 instead: −1 + 1 = 0 → **outside**. A hole. ✓

🧠 **Remember:** with the non-zero rule, a hole must go round the **opposite** way to the outside. Fonts and drawing programs (SVG, for example) store their letters exactly like this: the inside of the "O" goes round the other way.

🔢 **Maths: the frame in our program**

> outside: the square from (1, 1) to (11, 11) → 10 × 10 = 100 pixels
> inside: the square from (4, 4) to (8, 8) → 4 × 4 = 16 pixels
> non-zero, both the same way: **100** pixels (no hole)
> non-zero, inner reversed: 100 − 16 = **84** pixels
> even-odd: **84** pixels

The program prints the reversed version:

```
  ............
  .##########.
  .##########.
  .##########.
  .###....###.
  .###....###.
  .###....###.
  .###....###.
  .##########.
  .##########.
  .##########.
  ............
```

To reverse a path, we just list its points backwards. Our program has a tiny helper `reversed` for that.

---

## 25.7 Masks

Now we leave polygons and turn to a different kind of filling. First we need a small tool.

📖 **New word: mask** — a grid of yes/no values, one for each pixel. "Yes" means "this pixel belongs to the region".

```
  image:              mask (the red region):
  . . R R . .          0 0 1 1 0 0
  . R R R R .          0 1 1 1 1 0
  . . R R . .          0 0 1 1 0 0
```

A mask is like a **stencil**: you can first decide **where** to paint, and then paint later — solid, see-through, or with any colour. Masks are everywhere in image programs: "select this area", then "fill it", "blur it", "delete it". In Chapter 27 we will use many small masks to make smooth edges.

We store a mask exactly like an image (Chapter 6): one value per pixel, row by row, at index **y × width + x**. Each value is one byte: 1 for yes, 0 for no.

---

## 25.8 Flood fill: the paint bucket

Every paint program has a **paint bucket**. You click inside an area, and the whole area changes colour — but only up to its outline.

📖 **New word: flood fill** — fill the connected area that has the same colour as the starting pixel.

📖 **New word: seed** — the starting pixel (where you click).

The idea is like water flooding a field:

1. Remember the colour of the seed: the **target** colour.
2. Mark the seed.
3. Look at its **neighbours** (Chapter 3). Every neighbour that has the target colour, and is not marked yet, gets marked too.
4. Repeat for the new pixels, until no new pixel can be reached.
5. Paint all the marked pixels.

The marks are a **mask** (Section 25.7). The mask also guarantees that we never visit a pixel twice.

### A small example

```
  # # # # #          the seed is S, the target colour is "."
  # . . S #
  # . # . #          step 1: S is marked
  # . . . #          step 2: its 4 neighbours: left (.) → mark, right (#) no,
  # # # # #                  up (#) no, down (.) → mark
                     step 3, 4, …: keep spreading from the new marks
                     at the end: S and all 7 "." pixels are marked —
                     8 pixels (the # in the middle stays)
```

### 4-way and 8-way

Remember the neighbours from Chapter 3:

- **4 neighbours**: left, right, up, down.
- **8 neighbours**: also the 4 diagonal ones.

A **4-way** flood fill spreads only through the 4 neighbours; an **8-way** flood fill also through the diagonals. Does it matter? Very much!

### The leak

📖 **New word: leak** — when the fill escapes through a gap.

Our program draws a diamond with four Bresenham lines. Diagonal lines are made of pixels that touch only at their **corners**. Then it flood-fills from the centre, 4-way and 8-way:

```
4-way flood fill from (6, 6):     8-way flood fill from (6, 6):
  ......#......                     oooooo#oooooo
  .....#o#.....                     ooooo#o#ooooo
  ....#ooo#....                     oooo#ooo#oooo
  ...#ooooo#...                     ooo#ooooo#ooo
  ..#ooooooo#..                     oo#ooooooo#oo
  .#ooooooooo#.                     o#ooooooooo#o
  #ooooooooooo#                     #ooooooooooo#
  .#ooooooooo#.                     o#ooooooooo#o
  ..#ooooooo#..                     oo#ooooooo#oo
  ...#ooooo#...                     ooo#ooooo#ooo
  ....#ooo#....                     oooo#ooo#oooo
  .....#o#.....                     ooooo#o#ooooo
  ......#......                     oooooo#oooooo
```

(`#` = the outline, `o` = filled, `.` = not filled.)

The **4-way** fill stays inside: **61** pixels. The **8-way** fill **leaks**: it slips diagonally between two outline pixels that touch only at a corner, and floods the outside as well: **145** pixels (all 169 pixels except the 24 outline pixels).

🧠 **Remember the pairing:**

> outlines drawn with **diagonal steps** (8-connected, like Bresenham lines and midpoint circles) need a **4-way** fill.
> 8-way fills need outlines without diagonal steps (4-connected, "thick" outlines).

Our `floodFill` is 4-way by default.

---

## 25.9 Why not recursion?

📖 **New word: recursion** — a function that calls itself.

Flood fill looks perfect for recursion:

```cpp
// a tempting but dangerous version (not in our library!)
void floodRecursive(Image& image, int x, int y, Colour target, Colour c) {
    if (!image.isInside(x, y) || !sameColour(image.getPixel(x, y), target)) {
        return;
    }
    image.setPixel(x, y, c);
    floodRecursive(image, x + 1, y, target, c);
    floodRecursive(image, x - 1, y, target, c);
    floodRecursive(image, x, y + 1, target, c);
    floodRecursive(image, x, y - 1, target, c);
}
```

Short and clear. But it has a hidden danger.

Every function call that has not finished yet is remembered on the **call stack**, a small area of memory (often only 1 to 8 megabytes). Each waiting call needs some bytes there (its parameters, its return address, …). When we fill a large area, the fill can wander very far before any call finishes. For a 1000 × 1000 area, it can be up to **a million** calls deep.

🔢 **Maths: how much call stack would that need?**

> say 64 bytes per waiting call (a typical small amount)
> 1,000,000 calls × 64 bytes = 64,000,000 bytes = **64 megabytes**
> but the call stack is often only 1 to 8 megabytes → **crash**

📖 **New word: stack overflow** — this crash. The program simply dies.

(There is also a second problem: this version breaks if c is the same as target — it would never stop. Our mask version does not have this problem: a marked pixel is never visited again.)

### The fix: our own stack

📖 **New word: stack** — a list where you always add at the end and take from the end. The last thing you put in is the first thing you take out, like a stack of plates.

Instead of letting C++ remember the "pixels still to visit" on the small call stack, we keep them in our **own** list: a `std::vector<Point>`. A vector stores its items in the big main memory (the **heap**), which has gigabytes of room.

```
stack = [seed]
while the stack is not empty:
    take the last point p out of the stack
    if p is outside the image, or already marked, or not the target colour: skip it
    mark p
    put all its neighbours on the stack
```

`push_back` adds to the end, `back` reads the end, and `pop_back` removes the end — exactly a stack.

🔢 **Maths: how big can our stack get?**

> each marked pixel pushes 4 neighbours
> a 1000 × 1000 area: at most 4,000,000 points × 8 bytes (two `int`s) = 32 megabytes, in the heap — no problem

💡 There are faster flood fills. The most famous is the **scanline flood fill**: instead of single pixels, it fills a whole horizontal run at once, and only pushes the runs above and below. Practice 8 asks you to think about it.

---

## Code, part 1: `fill.h`

File: `common/fill.h` (new). It includes `triangles.h` (for `PointF`, `Point`, and everything before).

```cpp
#ifndef FILL_H
#define FILL_H

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <vector>
#include "triangles.h"

enum class FillRule { EvenOdd, NonZero };

struct Crossing {
    double x = 0.0;
    int direction = 0;
};

inline bool crossingIsLeft(const Crossing& p, const Crossing& q) {
    return p.x < q.x;
}

inline void findCrossings(const std::vector<PointF>& path, double sy,
                          std::vector<Crossing>& crossings) {
    const int n = static_cast<int>(path.size());
    for (int i = 0; i < n; ++i) {
        PointF a = path[i];
        PointF b = path[(i + 1) % n];
        if (a.y == b.y) {
            continue;
        }
        double top = std::min(a.y, b.y);
        double bottom = std::max(a.y, b.y);
        if (sy >= top && sy < bottom) {
            double t = (sy - a.y) / (b.y - a.y);
            int direction = (b.y > a.y) ? 1 : -1;
            crossings.push_back(Crossing{a.x + t * (b.x - a.x), direction});
        }
    }
}

inline void fillPaths(Image& image, const std::vector<std::vector<PointF>>& paths, Colour col,
                      FillRule rule = FillRule::NonZero, double alpha = 1.0) {
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
    int y0 = std::max(0, static_cast<int>(std::floor(minY)));
    int y1 = std::min(image.height(), static_cast<int>(std::ceil(maxY)));
    std::vector<Crossing> crossings;
    for (int y = y0; y < y1; ++y) {
        double sy = y + 0.5;
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
            int xa = std::max(0, static_cast<int>(std::ceil(crossings[k].x - 0.5)));
            int xb = std::min(image.width(), static_cast<int>(std::ceil(crossings[k + 1].x - 0.5)));
            for (int x = xa; x < xb; ++x) {
                if (alpha >= 1.0) {
                    image.setPixel(x, y, col);
                } else {
                    blendPixel(image, x, y, col, alpha);
                }
            }
        }
    }
}

inline void fillPolygon(Image& image, const std::vector<PointF>& points, Colour col,
                        FillRule rule = FillRule::NonZero, double alpha = 1.0) {
    std::vector<std::vector<PointF>> paths;
    paths.push_back(points);
    fillPaths(image, paths, col, rule, alpha);
}

struct Mask {
    int width = 0;
    int height = 0;
    std::vector<std::uint8_t> on;
};

inline Mask makeMask(int width, int height) {
    Mask mask;
    mask.width = width;
    mask.height = height;
    mask.on.assign(width * height, 0);
    return mask;
}

inline bool maskGet(const Mask& mask, int x, int y) {
    if (x < 0 || y < 0 || x >= mask.width || y >= mask.height) {
        return false;
    }
    return mask.on[y * mask.width + x] != 0;
}

inline void maskSet(Mask& mask, int x, int y, bool value) {
    if (x < 0 || y < 0 || x >= mask.width || y >= mask.height) {
        return;
    }
    mask.on[y * mask.width + x] = value ? 1 : 0;
}

inline int maskCount(const Mask& mask) {
    int count = 0;
    for (std::uint8_t v : mask.on) {
        if (v != 0) {
            ++count;
        }
    }
    return count;
}

inline bool sameColour(Colour p, Colour q) {
    return p.r == q.r && p.g == q.g && p.b == q.b;
}

inline Mask floodMask(const Image& image, int x, int y, bool eightWay = false) {
    Mask mask = makeMask(image.width(), image.height());
    if (!image.isInside(x, y)) {
        return mask;
    }
    const Colour target = image.getPixel(x, y);
    const int stepX[8] = {1, -1, 0, 0, 1, 1, -1, -1};
    const int stepY[8] = {0, 0, 1, -1, 1, -1, 1, -1};
    const int steps = eightWay ? 8 : 4;
    std::vector<Point> stack;
    stack.push_back(Point{x, y});
    while (!stack.empty()) {
        Point p = stack.back();
        stack.pop_back();
        if (!image.isInside(p.x, p.y) || maskGet(mask, p.x, p.y)) {
            continue;
        }
        if (!sameColour(image.getPixel(p.x, p.y), target)) {
            continue;
        }
        maskSet(mask, p.x, p.y, true);
        for (int i = 0; i < steps; ++i) {
            stack.push_back(Point{p.x + stepX[i], p.y + stepY[i]});
        }
    }
    return mask;
}

inline void paintMask(Image& image, const Mask& mask, Colour c, double alpha = 1.0) {
    for (int y = 0; y < mask.height; ++y) {
        for (int x = 0; x < mask.width; ++x) {
            if (!maskGet(mask, x, y)) {
                continue;
            }
            if (alpha >= 1.0) {
                image.setPixel(x, y, c);
            } else {
                blendPixel(image, x, y, c, alpha);
            }
        }
    }
}

inline int floodFill(Image& image, int x, int y, Colour c, bool eightWay = false,
                     double alpha = 1.0) {
    Mask mask = floodMask(image, x, y, eightWay);
    paintMask(image, mask, c, alpha);
    return maskCount(mask);
}

#endif
```

### Line by line

**The start (lines 1–19)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef FILL_H` / `#define FILL_H` | Include guard. |
| 4–7 | `#include <algorithm>` … `#include <vector>` | `std::min`, `std::max`, `std::sort`; `std::floor`, `std::ceil`; `std::uint8_t` (Chapter 4); `std::vector`. |
| 8 | `#include "triangles.h"` | `PointF` (Chapter 24), `Point` (Chapter 21), and everything before. |
| 10 | `enum class FillRule { EvenOdd, NonZero };` | The two fill rules of Section 25.5, as named values. |
| 12–15 | `struct Crossing { double x = 0.0; int direction = 0; };` | One crossing of a row with an edge: **where** (x) and **which way** the edge goes (+1 down, −1 up). |
| 17–19 | `inline bool crossingIsLeft(const Crossing& p, const Crossing& q) { return p.x < q.x; }` | "Is p further left than q?" `std::sort` uses this to put the crossings in order from left to right. |

**Finding the crossings of one path with one row (lines 21–38)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 21–22 | `inline void findCrossings(const std::vector<PointF>& path, double sy, std::vector<Crossing>& crossings) {` | Add to `crossings` every place where the row at height sy crosses an edge of this path. |
| 23 | `const int n = static_cast<int>(path.size());` | The number of corners (and of edges: a closed path has as many edges as corners). |
| 24 | `for (int i = 0; i < n; ++i) {` | Every edge. |
| 25–26 | `PointF a = path[i];` / `PointF b = path[(i + 1) % n];` | The edge from corner i to corner i + 1. For the last corner, `% n` gives 0: the edge back to the start closes the path. |
| 27–29 | `if (a.y == b.y) { continue; }` | Skip horizontal edges (Section 25.3). This also protects the division below from dividing by 0. |
| 30–31 | `double top = std::min(a.y, b.y);` / `double bottom = std::max(a.y, b.y);` | The highest and lowest y of the edge (remember: smaller y is higher on the screen). |
| 32 | `if (sy >= top && sy < bottom) {` | The half-open test of Section 25.4: the top end counts, the bottom end does not. |
| 33 | `double t = (sy - a.y) / (b.y - a.y);` | How far along the edge the row is (0 at a, 1 at b). |
| 34 | `int direction = (b.y > a.y) ? 1 : -1;` | Going down the screen: +1. Going up: −1. (For the non-zero rule.) |
| 35 | `crossings.push_back(Crossing{a.x + t * (b.x - a.x), direction});` | The crossing point by lerp (Section 25.3), and its direction. |
| 36–38 | `}` `}` `}` | End. |

**Scanline filling (lines 40–89)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 40–41 | `inline void fillPaths(Image& image, const std::vector<std::vector<PointF>>& paths, Colour col, FillRule rule = FillRule::NonZero, double alpha = 1.0) {` | Fill a shape made of one or more paths (holes are extra paths). Non-zero is the default rule, and solid paint is the default. |
| 42–44 | `bool any = false;` / `double minY = 0.0;` / `double maxY = 0.0;` | We look for the top and bottom of the whole shape. `any` says if we have seen a point yet. |
| 45–56 | the two `for` loops with `if (!any) { ... } else { ... }` | For every point of every path: the first point sets minY and maxY; later points can only make them smaller or bigger. |
| 57–59 | `if (!any) { return; }` | No points at all: nothing to fill. |
| 60–61 | `int y0 = std::max(0, ...floor(minY)...);` / `int y1 = std::min(image.height(), ...ceil(maxY)...);` | The rows to visit: from the top to the bottom of the shape, clipped to the image. |
| 62 | `std::vector<Crossing> crossings;` | The crossings of the current row. We make the vector once and reuse it for every row. |
| 63 | `for (int y = y0; y < y1; ++y) {` | Every row. |
| 64 | `double sy = y + 0.5;` | The height of the pixel centres in this row. |
| 65 | `crossings.clear();` | Forget the crossings of the previous row. |
| 66–68 | `for (const std::vector<PointF>& path : paths) { findCrossings(path, sy, crossings); }` | Collect the crossings of **all** paths together. That is what makes holes work. |
| 69 | `std::sort(crossings.begin(), crossings.end(), crossingIsLeft);` | Put the crossings in order from left to right. |
| 70 | `int winding = 0;` | The winding number, starting far away on the left (outside). |
| 71 | `const int count = static_cast<int>(crossings.size());` | How many crossings this row has (always an even number). |
| 72 | `for (int k = 0; k + 1 < count; ++k) {` | Every gap between crossing k and crossing k + 1. |
| 73 | `winding += crossings[k].direction;` | Passing crossing k changes the winding number by its direction. |
| 74 | `bool inside = (rule == FillRule::EvenOdd) ? (k % 2 == 0) : (winding != 0);` | Even-odd: after k + 1 crossings, inside if k + 1 is odd, which means k is even. Non-zero: inside if the winding number is not 0. |
| 75–77 | `if (!inside) { continue; }` | Outside: skip this gap. |
| 78–79 | `int xa = ...ceil(crossings[k].x - 0.5)...;` / `int xb = ...ceil(crossings[k + 1].x - 0.5)...;` | The pixels whose centres lie between the two crossings (Section 25.3), clipped to the image. |
| 80–86 | `for (int x = xa; x < xb; ++x) { ... setPixel ... blendPixel ... }` | Paint them, solid or see-through. |
| 87–89 | `}` `}` `}` | End of the gap loop, the row loop, and the function. |

**One polygon (lines 91–96)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 91–92 | `inline void fillPolygon(Image& image, const std::vector<PointF>& points, Colour col, FillRule rule = FillRule::NonZero, double alpha = 1.0) {` | The common case: a shape with just one path. |
| 93–94 | `std::vector<std::vector<PointF>> paths;` / `paths.push_back(points);` | Make a list of paths with one path in it. |
| 95–96 | `fillPaths(image, paths, col, rule, alpha);` `}` | Fill it. |

**The mask (lines 98–134)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 98–102 | `struct Mask { int width = 0; int height = 0; std::vector<std::uint8_t> on; };` | A yes/no grid (Section 25.7): its size, and one byte per pixel (1 = yes, 0 = no). |
| 104–110 | `inline Mask makeMask(int width, int height) { ... mask.on.assign(width * height, 0); return mask; }` | A new mask of the given size, all "no". `assign(n, 0)` makes the vector n bytes long, all 0. |
| 112–117 | `inline bool maskGet(const Mask& mask, int x, int y) { if (...outside...) { return false; } return mask.on[y * mask.width + x] != 0; }` | Read one value. Outside the mask counts as "no", like `getPixel` returns black outside the image. |
| 119–124 | `inline void maskSet(Mask& mask, int x, int y, bool value) { if (...outside...) { return; } mask.on[...] = value ? 1 : 0; }` | Write one value. Outside the mask is ignored. |
| 126–134 | `inline int maskCount(const Mask& mask) { ... for (std::uint8_t v : mask.on) { if (v != 0) { ++count; } } return count; }` | How many pixels are "yes". |

**Flood fill (lines 136–188)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 136–138 | `inline bool sameColour(Colour p, Colour q) { return p.r == q.r && p.g == q.g && p.b == q.b; }` | Are two colours exactly the same? |
| 140 | `inline Mask floodMask(const Image& image, int x, int y, bool eightWay = false) {` | Find (but do not paint) the region a flood fill from (x, y) would reach. The image is `const`: it is not changed. |
| 141 | `Mask mask = makeMask(image.width(), image.height());` | The marks, all "no" at first. |
| 142–144 | `if (!image.isInside(x, y)) { return mask; }` | A seed outside the image reaches nothing. |
| 145 | `const Colour target = image.getPixel(x, y);` | The colour we flood through: the seed's colour. |
| 146–147 | `const int stepX[8] = {1, -1, 0, 0, 1, 1, -1, -1};` / `const int stepY[8] = {...};` | The steps to the neighbours, like Chapter 3: the first 4 are right, left, down, up; the last 4 are the diagonals. |
| 148 | `const int steps = eightWay ? 8 : 4;` | Use 4 or all 8 of them. |
| 149–150 | `std::vector<Point> stack;` / `stack.push_back(Point{x, y});` | Our own stack (Section 25.9), with the seed in it. |
| 151 | `while (!stack.empty()) {` | Until there is nothing left to visit. |
| 152–153 | `Point p = stack.back();` / `stack.pop_back();` | Take the last point out. |
| 154–156 | `if (!image.isInside(p.x, p.y) \|\| maskGet(mask, p.x, p.y)) { continue; }` | Outside the image, or already marked: skip it. |
| 157–159 | `if (!sameColour(image.getPixel(p.x, p.y), target)) { continue; }` | Not the target colour (for example, the outline): skip it. |
| 160 | `maskSet(mask, p.x, p.y, true);` | It belongs to the region: mark it. |
| 161–163 | `for (int i = 0; i < steps; ++i) { stack.push_back(Point{p.x + stepX[i], p.y + stepY[i]}); }` | Put all its neighbours on the stack. We do not check them here; they are checked when they come out (lines 154–159). |
| 164–166 | `}` `return mask;` `}` | Done: the mask holds the whole region. |
| 168 | `inline void paintMask(Image& image, const Mask& mask, Colour c, double alpha = 1.0) {` | Paint every "yes" pixel of a mask. |
| 169–181 | the loops, `if (!maskGet(...)) { continue; }`, then `setPixel` or `blendPixel` | Skip the "no" pixels; paint the others, solid or see-through. |
| 183–184 | `inline int floodFill(Image& image, int x, int y, Colour c, bool eightWay = false, double alpha = 1.0) {` | The paint bucket. |
| 185 | `Mask mask = floodMask(image, x, y, eightWay);` | First find the region… |
| 186 | `paintMask(image, mask, c, alpha);` | …then paint it. Because the finding is finished **before** the painting starts, painting with the same colour, or with see-through paint, causes no trouble. |
| 187–188 | `return maskCount(mask);` `}` | Tell the caller how many pixels were filled. |
| 190 | `#endif` | End of the include guard. |

---

## Code, part 2: stars, holes and a Venn diagram

File: `ch25/fill.cpp`

```cpp
#include <iostream>
#include <string>
#include <vector>
#include "fill.h"

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

bool samePixels(const Image& p, const Image& q) {
    if (p.width() != q.width() || p.height() != q.height()) {
        return false;
    }
    for (int y = 0; y < p.height(); ++y) {
        for (int x = 0; x < p.width(); ++x) {
            if (!sameColour(p.getPixel(x, y), q.getPixel(x, y))) {
                return false;
            }
        }
    }
    return true;
}

void printColours(const std::string& title, const Image& img) {
    std::cout << title << ":\n";
    for (int y = 0; y < img.height(); ++y) {
        std::cout << "  ";
        for (int x = 0; x < img.width(); ++x) {
            Colour c = img.getPixel(x, y);
            char ch = '?';
            if (sameColour(c, colours::black)) {
                ch = '.';
            } else if (sameColour(c, colours::white)) {
                ch = '#';
            } else if (sameColour(c, colours::red)) {
                ch = 'o';
            }
            std::cout << ch;
        }
        std::cout << "\n";
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

std::vector<PointF> square(double x0, double y0, double x1, double y1) {
    return {PointF{x0, y0}, PointF{x1, y0}, PointF{x1, y1}, PointF{x0, y1}};
}

std::vector<PointF> reversed(const std::vector<PointF>& points) {
    return std::vector<PointF>(points.rbegin(), points.rend());
}

int main() {
    Image evenOdd(21, 20);
    fillPolygon(evenOdd, star(10.5, 10.5, 10.0), colours::white, FillRule::EvenOdd);
    printGrid("star, even-odd rule", evenOdd);
    Image nonZero(21, 20);
    fillPolygon(nonZero, star(10.5, 10.5, 10.0), colours::white, FillRule::NonZero);
    printGrid("star, non-zero rule", nonZero);
    std::cout << "pixels: even-odd " << countLit(evenOdd) << ", non-zero " << countLit(nonZero)
              << "\n";

    std::vector<PointF> arrowHead = {PointF{0.0, 0.0}, PointF{10.0, 5.0}, PointF{0.0, 10.0},
                                     PointF{3.0, 5.0}};
    Image arrow(11, 11);
    fillPolygon(arrow, arrowHead, colours::white);
    printGrid("arrow-head (a shape with a dent)", arrow);

    std::vector<PointF> tri = {PointF{1.0, 1.0}, PointF{12.0, 4.0}, PointF{4.0, 10.0}};
    Image byScan(14, 12);
    Image byEdges(14, 12);
    fillPolygon(byScan, tri, colours::white);
    fillTriangle(byEdges, tri[0], tri[1], tri[2], colours::white);
    std::cout << "scanline fill and fillTriangle give the same pixels: "
              << (samePixels(byScan, byEdges) ? "yes" : "no") << "\n";

    std::vector<PointF> outer = square(1.0, 1.0, 11.0, 11.0);
    std::vector<PointF> inner = square(4.0, 4.0, 8.0, 8.0);
    Image sameWay(12, 12);
    Image otherWay(12, 12);
    Image evenOddFrame(12, 12);
    fillPaths(sameWay, {outer, inner}, colours::white, FillRule::NonZero);
    fillPaths(otherWay, {outer, reversed(inner)}, colours::white, FillRule::NonZero);
    fillPaths(evenOddFrame, {outer, inner}, colours::white, FillRule::EvenOdd);
    printGrid("frame, non-zero rule, inner square reversed", otherWay);
    std::cout << "pixels: non-zero same way " << countLit(sameWay) << ", non-zero reversed "
              << countLit(otherWay) << ", even-odd " << countLit(evenOddFrame) << "\n";

    Image diamond(13, 13);
    drawLine(diamond, 6, 0, 12, 6, colours::white);
    drawLine(diamond, 12, 6, 6, 12, colours::white);
    drawLine(diamond, 6, 12, 0, 6, colours::white);
    drawLine(diamond, 0, 6, 6, 0, colours::white);
    Image four = diamond;
    int filled4 = floodFill(four, 6, 6, colours::red);
    printColours("4-way flood fill from (6, 6)", four);
    Image eight = diamond;
    int filled8 = floodFill(eight, 6, 6, colours::red, true);
    printColours("8-way flood fill from (6, 6)", eight);
    std::cout << "filled pixels: 4-way " << filled4 << ", 8-way " << filled8 << "\n";

    Image stars(420, 220, Colour{20, 30, 70});
    Colour gold{255, 200, 40};
    fillPolygon(stars, star(110.5, 115.5, 100.0), gold, FillRule::EvenOdd);
    fillPolygon(stars, star(310.5, 115.5, 100.0), gold, FillRule::NonZero);

    Image holes(320, 180, colours::white);
    for (int x = 0; x < 320; x += 20) {
        fillRect(holes, Rect{x, 0, x + 10, 180}, Colour{190, 210, 230});
    }
    std::vector<PointF> letterC = {PointF{40.0, 20.0}, PointF{140.0, 20.0}, PointF{140.0, 50.0},
                                   PointF{70.0, 50.0}, PointF{70.0, 130.0}, PointF{140.0, 130.0},
                                   PointF{140.0, 160.0}, PointF{40.0, 160.0}};
    fillPolygon(holes, letterC, Colour{200, 40, 60});
    fillPaths(holes,
              {square(170.0, 20.0, 290.0, 160.0), reversed(square(200.0, 50.0, 260.0, 130.0))},
              Colour{40, 120, 60});

    Image venn(300, 200, colours::white);
    drawCircle(venn, 110, 100, 70, colours::black);
    drawCircle(venn, 190, 100, 70, colours::black);
    floodFill(venn, 5, 5, Colour{255, 250, 210});
    floodFill(venn, 70, 100, Colour{250, 120, 120});
    floodFill(venn, 150, 100, Colour{180, 110, 200});
    floodFill(venn, 230, 100, Colour{110, 150, 250});

    bool ok = stars.savePPM("stars.ppm");
    ok = ok && holes.savePPM("holes.ppm");
    ok = ok && venn.savePPM("venn.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
```

Build and run (from the `code/ch25` folder):

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common fill.cpp -o fill
./fill
```

### Line by line

**Helpers (lines 1–84)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–4 | the `#include` lines | Printing, text, vectors, and our new header. |
| 6–30 | `printGrid`, `countLit` | The same as in the last chapters. |
| 32–44 | `bool samePixels(const Image& p, const Image& q) { ... }` | The same as Chapter 24, but shorter: it uses `sameColour` from `fill.h`. |
| 46 | `void printColours(const std::string& title, const Image& img) {` | Like `printGrid`, but with **three** symbols, so we can tell the outline from the fill. |
| 52 | `char ch = '?';` | Any colour we do not expect prints as `?`. |
| 53–59 | `if (sameColour(c, colours::black)) { ch = '.'; } else if (... white ...) { ch = '#'; } else if (... red ...) { ch = 'o'; }` | Black (empty) → `.`, white (outline) → `#`, red (flooded) → `o`. |
| 66 | `std::vector<PointF> star(double cx, double cy, double r) {` | The five corners of a star, in drawing order (Section 25.5). |
| 67–68 | `const double ux[5] = {...};` / `const double uy[5] = {...};` | The five points of a pentagon on a circle of radius 1 (from the table in Section 25.5). |
| 69 | `const int order[5] = {0, 2, 4, 1, 3};` | Skip one corner each time: this makes the star. |
| 70–75 | `std::vector<PointF> points; for (...) { int k = order[i]; points.push_back(PointF{cx + r * ux[k], cy + r * uy[k]}); } return points;` | Scale by r, move to the centre, and collect the points in star order. |
| 78–80 | `std::vector<PointF> square(double x0, double y0, double x1, double y1) { return {...}; }` | The four corners of a rectangle: top-left, top-right, bottom-right, bottom-left. On the screen, that goes **clockwise**. |
| 82–84 | `std::vector<PointF> reversed(const std::vector<PointF>& points) { return std::vector<PointF>(points.rbegin(), points.rend()); }` | The same points backwards (Section 25.6). `rbegin()` and `rend()` walk through a vector from its end to its start ("r" for "reverse"); the new vector is built from that walk. |

**The text output (lines 86–133)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 87–94 | `Image evenOdd(21, 20);` … `countLit(nonZero)` | The same star, filled with each rule, printed, and counted (Section 25.5). |
| 96–100 | `std::vector<PointF> arrowHead = {...};` … `printGrid(...)` | The arrow-head that broke the fan in Chapter 24. Scanline filling keeps the dent. |
| 102–108 | `std::vector<PointF> tri = {...};` … `samePixels(byScan, byEdges)` | Fill the Chapter 24 triangle both ways and compare (Section 25.4). |
| 110–120 | `outer`, `inner`, the three `fillPaths` calls, the printing | The frame of Section 25.6 with three choices: non-zero with the inner square the same way, non-zero with it reversed, and even-odd. The `{outer, inner}` with curly brackets makes a list of two paths on the spot. |
| 122–126 | `Image diamond(13, 13);` and four `drawLine` calls | A diamond outline made of four diagonal Bresenham lines (Chapter 21). |
| 127 | `Image four = diamond;` | A **copy** of the image (copying an `Image` copies all its pixels). |
| 128–129 | `int filled4 = floodFill(four, 6, 6, colours::red);` / `printColours(...)` | 4-way flood fill from the centre (the default). |
| 130–132 | `Image eight = diamond;` … `floodFill(eight, 6, 6, colours::red, true);` … | 8-way flood fill on a fresh copy: it leaks (Section 25.8). |
| 133 | `std::cout << "filled pixels: ..."` | Print both counts. |

**The pictures (lines 135–168)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 135–136 | `Image stars(420, 220, Colour{20, 30, 70});` / `Colour gold{255, 200, 40};` | A night-blue picture and a gold colour. |
| 137 | `fillPolygon(stars, star(110.5, 115.5, 100.0), gold, FillRule::EvenOdd);` | The left star with even-odd: a hollow middle. (The centre is lower than the middle of the picture, because a star's points reach further up, 100, than down, 81.) |
| 138 | `fillPolygon(stars, star(310.5, 115.5, 100.0), gold, FillRule::NonZero);` | The right star with non-zero: solid. |
| 140–143 | `Image holes(320, 180, colours::white);` and the stripes loop | Light blue stripes, so we can see the background through the holes. |
| 144–146 | `std::vector<PointF> letterC = {...};` | A blocky letter "C": 8 corners, with a deep dent on the right side. |
| 147 | `fillPolygon(holes, letterC, Colour{200, 40, 60});` | Red "C". The dent stays empty. |
| 148–150 | `fillPaths(holes, {square(...), reversed(square(...))}, Colour{40, 120, 60});` | A green frame: an outer square and a **reversed** inner square, with the default non-zero rule: the stripes show through the hole. |
| 152 | `Image venn(300, 200, colours::white);` | A white picture. |
| 153–154 | `drawCircle(venn, 110, 100, 70, colours::black);` / `drawCircle(venn, 190, 100, 70, ...);` | Two black circles that overlap: a **Venn diagram** (a picture that shows two groups and what they share). The outlines split the picture into 4 areas: outside, left only, both, right only. |
| 155 | `floodFill(venn, 5, 5, Colour{255, 250, 210});` | The outside (seed in the top-left corner): pale yellow. |
| 156 | `floodFill(venn, 70, 100, Colour{250, 120, 120});` | Left only: red. (70 is 40 from the left centre, inside its radius 70, but 120 from the right centre.) |
| 157 | `floodFill(venn, 150, 100, Colour{180, 110, 200});` | The overlap: purple (red and blue mixed). |
| 158 | `floodFill(venn, 230, 100, Colour{110, 150, 250});` | Right only: blue. The midpoint circles have diagonal steps, so the 4-way default is the right choice: no leaks. |
| 160–168 | saving | Save `stars.ppm`, `holes.ppm` and `venn.ppm`. |

### What you should see

The program prints the two stars (Section 25.5), then:

```
pixels: even-odd 78, non-zero 115
arrow-head (a shape with a dent):
  #..........
  .##........
  .####......
  ..#####....
  ...######..
  ...######..
  ..#####....
  .####......
  .##........
  #..........
  ...........
scanline fill and fillTriangle give the same pixels: yes
frame, non-zero rule, inner square reversed:
  ...  (the frame of Section 25.6)
pixels: non-zero same way 100, non-zero reversed 84, even-odd 84
4-way flood fill from (6, 6):
  ...  (the diamond of Section 25.8)
8-way flood fill from (6, 6):
  ...
filled pixels: 4-way 61, 8-way 145
```

Look at the arrow-head: the rows on the left get shorter toward the middle (rows 4 and 5 start at column 3). That is the **dent**, kept empty.

Open the pictures:
- `stars.ppm`: two gold stars. The left one has a dark pentagon in its middle; the right one is solid.
- `holes.ppm`: a red blocky "C" and a green square frame, with blue stripes showing through the hole.
- `venn.ppm`: two overlapping circles, filled red, purple and blue, on a pale yellow background, with black outlines.

---

## Small examples

### Example 1 — Crossings of a triangle

Triangle (2, 1), (8, 13), (14, 1). Row 6 (sy = 6.5):

> edge (2, 1) → (8, 13): t = 5.5 / 12 = 0.458 → x = 2 + 0.458 × 6 = 4.75
> edge (8, 13) → (14, 1): t = (6.5 − 13) / (1 − 13) = 0.542 → x = 8 + 0.542 × 6 = 11.25
> edge (14, 1) → (2, 1): horizontal → skipped
> crossings 4.75 and 11.25 → pixels ceil(4.25) = 5 to ceil(10.75) = 11, not including 11 → **5 … 10**

### Example 2 — Even-odd with a ray

A square frame: outer (0, 0)–(10, 10), inner (3, 3)–(7, 7). The point (5, 5), ray to the left:

> it crosses the inner square's left edge at x = 3, and the outer square's left edge at x = 0
> 2 crossings → even → **outside** (the hole) ✓

The point (1, 5): 1 crossing (x = 0) → odd → **inside** (the frame) ✓

### Example 3 — The winding number of a doubled square

Draw a square twice around (the path goes round the same 4 corners two times — 8 points). A point inside:

> even-odd: 2 crossings to the left → **outside**! The square is empty.
> non-zero: winding −2 → **inside**. The square is filled.

So with even-odd, "going round twice" cancels out. That is why most drawing programs prefer non-zero as the default.

### Example 4 — Using a mask for see-through paint

```cpp
Mask region = floodMask(img, 50, 50);
paintMask(img, region, colours::blue, 0.3);
```

This tints the whole region at (50, 50) with 30 % blue, without changing its shape. A paint bucket with see-through paint!

### Example 5 — How many pixels does the stack hold?

In the small example of Section 25.8, each of the 8 marked pixels pushes 4 neighbours: 32 pushes, plus the seed, makes 33. Most of them are skipped when they come out (walls, or already marked). So the stack never holds more than 33 points for this example.

---

## Common mistakes

⚠️ **Counting a corner twice.** Use "top ≤ sy < bottom" for every edge. Otherwise some rows get an odd number of crossings, and whole rows are filled wrongly.

⚠️ **Not sorting the crossings.** The edges are in path order, not left-to-right order. Without sorting, the pairs are nonsense.

⚠️ **Forgetting horizontal edges in the division.** (b.y − a.y) is 0 for them: skip them first.

⚠️ **A hole going round the same way, with non-zero.** No hole appears. Reverse the inner path, or use even-odd.

⚠️ **8-way flood fill on a thin diagonal outline.** It leaks out. Use 4-way.

⚠️ **Recursive flood fill.** Fine for tiny pictures, a crash for big ones. Use your own stack.

⚠️ **Flood fill with the same colour as the target, without a mask.** The simple version never knows it is finished. Our version marks pixels in a mask, so it always stops.

---

## Practice

🏋️ **1.** For the triangle (2, 1), (8, 13), (14, 1), find the crossings of row 10 and the pixels that are filled.

🏋️ **2.** A polygon has the corners (0, 0.5), (6, 4.5), (0, 8.5), (2, 4.5) (an arrow-head with a corner exactly on row 4). How many crossings does row 4 (sy = 4.5) have, and where? Which pixels are filled?

🏋️ **3.** Draw a "plus" sign (+) as one polygon with 12 corners and fill it.

🏋️ **4.** Make a letter "O": an outer square 100 × 140 and an inner square 50 × 90, centred. Fill it with the non-zero rule. What must you do with the inner square?

🏋️ **5.** In the star with even-odd, a point in one of the five **points** (arms) of the star: how many crossings does its ray to the left have? And a point in the middle pentagon?

🏋️ **6.** Use `floodMask` and `maskCount` to measure the area of the overlap in `venn.ppm`. Estimate it first: two circles of radius 70 whose centres are 80 apart.

🏋️ **7.** Write `outlineMask`: given a mask, make a new mask with only the pixels that are "yes" and have at least one 4-neighbour that is "no". Paint it to draw the **border** of a flood-filled region.

🏋️ **8.** (Thinking) In the scanline flood fill, you fill a whole horizontal run at once. Explain why this needs far fewer stack pushes than our pixel-by-pixel version.

---

## Answers

**1.**
> sy = 10.5
> edge (2, 1) → (8, 13): t = 9.5 / 12 = 0.792 → x = 2 + 0.792 × 6 = **6.75**
> edge (8, 13) → (14, 1): t = (10.5 − 13) / (−12) = 0.208 → x = 8 + 0.208 × 6 = **9.25**
> pixels from ceil(6.25) = 7 up to (not including) ceil(8.75) = 9 → **7 and 8**

(Check: the triangle gets narrower toward its bottom point (8, 13), and pixel centres 7.5 and 8.5 are between 6.75 and 9.25 ✓.)

**2.**
> Edges: (0, 0.5) → (6, 4.5) covers 0.5 ≤ sy < 4.5: **not** row 4.5.
> (6, 4.5) → (0, 8.5) covers 4.5 ≤ sy < 8.5: **yes**, crossing at x = 6.
> (0, 8.5) → (2, 4.5): top 4.5, bottom 8.5: **yes**, crossing at x = 2.
> (2, 4.5) → (0, 0.5): top 0.5, bottom 4.5: **not** row 4.5.
> 2 crossings: 2 and 6 → pixels ceil(1.5) = 2 to ceil(5.5) = 6, not including 6 → **2, 3, 4, 5** ✓

Each of the two corners on the row is counted exactly once.

**3.** A plus with arms 20 wide, from 0 to 60:

```cpp
std::vector<PointF> plus = {
    PointF{20, 0}, PointF{40, 0}, PointF{40, 20}, PointF{60, 20},
    PointF{60, 40}, PointF{40, 40}, PointF{40, 60}, PointF{20, 60},
    PointF{20, 40}, PointF{0, 40}, PointF{0, 20}, PointF{20, 20}};
fillPolygon(img, plus, colours::red);
```

It has 4 dents (the inside corners), and scanline filling handles all of them.

Area: the plus is a 60 × 60 square with the 4 corner squares (20 × 20 each) cut away:

> 3600 − 4 × 400 = 3600 − 1600 = **2000** pixels

Check another way: the plus is 5 squares of 20 × 20 (the middle and the four arms): 5 × 400 = 2000 ✓

**4.** The inner square must go round the **other** way: use `reversed(inner)` (or list its corners counter-clockwise). With the image centre at (cx, cy):

```cpp
std::vector<PointF> outerO = square(cx - 50, cy - 70, cx + 50, cy + 70);
std::vector<PointF> innerO = square(cx - 25, cy - 45, cx + 25, cy + 45);
fillPaths(img, {outerO, reversed(innerO)}, colours::black);
```

Area: 100 × 140 − 50 × 90 = 14,000 − 4500 = **9500** pixels.

**5.** Look at row 8 in Section 25.5. It has crossings at 2.489, 7.901, 13.099 and 18.511.

> a point in the **left** arm, x = 5: one crossing (2.489) is on its left → **1** → odd → inside
> a point in the **right** arm, x = 16: three crossings are on its left → **3** → odd → inside
> a point in the **middle**, x = 10: two crossings are on its left → **2** → even → outside (with even-odd)

**6.**

```cpp
Mask overlap = floodMask(venn, 150, 100);   // run this before filling the overlap
std::cout << maskCount(overlap) << "\n";
```

Estimate: the overlap is a "lens". Its width is 2 × 70 − 80 = 60 (from x = 120 to x = 180), and its height is 2 × √(70² − 40²) = 2 × √3300 ≈ 2 × 57.4 = 115. Its box has 60 × 115 = 6900 pixels. A lens is fatter than a diamond (which fills ½ of its box) and thinner than an ellipse (which fills π/4 ≈ 79 %). Guess about 70 %: 0.7 × 6900 ≈ **4800** pixels.

The exact area (with a formula we do not need here) is about **4837**. The program prints **4723**: a little less, because the black outline pixels are not part of the region.

**7.**

```cpp
inline Mask outlineMask(const Mask& m) {
    Mask out = makeMask(m.width, m.height);
    for (int y = 0; y < m.height; ++y) {
        for (int x = 0; x < m.width; ++x) {
            if (!maskGet(m, x, y)) {
                continue;
            }
            bool edge = !maskGet(m, x + 1, y) || !maskGet(m, x - 1, y) ||
                        !maskGet(m, x, y + 1) || !maskGet(m, x, y - 1);
            maskSet(out, x, y, edge);
        }
    }
    return out;
}
```

Because `maskGet` returns "no" outside the mask, pixels at the image border count as border pixels too.

**8.** Our version pushes 4 neighbours for **every** pixel: for a run of 100 pixels in a row, that is 400 pushes, and most of them are pixels in the same row that we reach anyway. The scanline version fills the whole run of 100 with a simple loop (no pushes at all), and then pushes only **one** point for each separate run it finds in the row above and the row below — often just 2 pushes. So the stack stays tiny, and the program does much less work.

---

## Summary

🧠 **Scanline fill**: for each row at sy = y + 0.5, find the **crossings** with every edge, **sort** them, and fill between pairs.

🧠 An edge counts for a row if **top ≤ sy < bottom** (half-open). Skip horizontal edges. Every row then has an **even** number of crossings.

🧠 Pixels between crossings xa and xb: from **ceil(xa − 0.5)** up to (not including) **ceil(xb − 0.5)**.

🧠 **Even-odd**: inside if an odd number of crossings is on the left. **Non-zero**: inside if the winding number (+1 down, −1 up) is not 0.

🧠 **Holes**: extra paths. With non-zero, the hole must go round the **opposite** way.

🧠 A **mask** is a yes/no grid, one byte per pixel at y × width + x.

🧠 **Flood fill**: spread from the seed to neighbours of the same colour; mark them in a mask; paint the mask. **4-way** for thin diagonal outlines (8-way **leaks**).

🧠 Use your **own stack** (`std::vector`), never deep **recursion**.

---

## Next chapter

So far every shape has had **one** colour. In Chapter 26 we give each corner of a triangle its **own** colour and blend smoothly between them. The key is a set of three numbers we already met in Chapter 24 — w0, w1 and w2 — which become the **barycentric coordinates** of a point: "how much" of each corner the point has.
