# Chapter 33 — Combining Transforms

> **Part 5 · Chapter 33 of 82**
> **You need:** Chapters 1–32 (especially 31 and 32) · **You will make:** `combine.h` (turning and scaling around any pivot with one matrix, the inverse matrix, the box around a transformed picture, and drawing a whole picture through a matrix), `arm.ppm`, `solar.ppm`, `moved.ppm` and `holes.ppm`

---

## What you will learn

- How to turn or scale around **any pivot** with a **single** matrix.
- The general recipe for placing a shape: **local → world**.
- How to build **hierarchies**: a hand that moves with the forearm, which moves with the upper arm; a moon that goes round a planet, which goes round the Sun.
- What the **inverse** of a matrix is, how to find it, and when it does not exist.
- How to **turn, scale and skew a whole picture**, pixel by pixel.
- Why going **forwards** (from the old picture to the new one) leaves **holes**, and why going **backwards** does not.
- How to find the box that a transformed picture covers.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **pivot matrix** | A matrix that turns or scales around a chosen point, not around (0, 0). |
| **world coordinates** | The coordinates of the final picture (the "real" pixels). |
| **hierarchy** | A family tree of parts: each part is attached to a **parent** and moves with it. |
| **parent** / **child** | In a hierarchy: the part something is attached to / the part attached to it. |
| **joint** | The place where a child part is attached to its parent, and can turn. |
| **inverse matrix** | The matrix that undoes another one: M × M⁻¹ = identity. |
| **invertible** | Has an inverse (its determinant is not 0). |
| **forward mapping** | Making a new picture by sending each **old** pixel to its new place. |
| **inverse mapping** (backward mapping) | Making a new picture by asking, for each **new** pixel, where it came from. |
| **source** / **destination** | The picture we copy **from** / the picture we copy **into**. |
| **nearest neighbour** | Taking the colour of the one source pixel the position falls in. |

---

## 33.1 Turning around a pivot, as one matrix

In Chapter 31, turning around a pivot C took three steps: move C to the origin, turn, move back. In Chapter 32 we learned that a chain of steps can be packed into **one** matrix, read **right to left**. Put the two ideas together:

> **rotationAbout(C, θ) = translation(C) × rotation(θ) × translation(−C)**

Read right to left: first translation(−C) (the pivot goes to the origin), then rotation(θ), then translation(C) (back again). This is exactly Chapter 32, Practice 5.

📖 **New word: pivot matrix** — a matrix that turns (or scales) around a chosen point.

The same trick works for scaling:

> **scalingAbout(C, sx, sy) = translation(C) × scaling(sx, sy) × translation(−C)**

🔢 **Maths: scalingAbout((2, 2), 2, 2) by multiplying**

> scaling(2, 2) × translation(−2, −2): the moving part becomes 2 × (−2, −2) = (−4, −4) (Chapter 32 Section 32.10: the scale also scales the move)
> translation(2, 2) × that: adds (2, 2) to the moving part → (−2, −2)

```
[ 2  0  −2 ]
[ 0  2  −2 ]
[ 0  0   1 ]
```

> Check on (4, 6): (2 × 4 − 2, 2 × 6 − 2) = **(6, 10)** ✓ — the same as `scaleAbout` in Chapter 31.
> Check on the pivot (2, 2): (4 − 2, 4 − 2) = (2, 2) ✓ — it stays put.

The program prints this matrix, and also:

```
rotationAbout (2, 2) by 90 degrees sends (5, 2) to (2, 5)
```

— the same as Chapter 31, Section 31.6 ✓.

💡 Look at the matrix: it is "scale by 2" plus a move of (−2, −2). **Every** pivot matrix is just an ordinary scale or turn plus a move. The move is exactly what is needed to keep the pivot still: C − 2C = −C = (−2, −2).

---

## 33.2 Local to world

📖 **New word: world coordinates** — the coordinates of the final picture: real pixel positions.

In Chapters 31 and 32 we built shapes in **local coordinates** (around their own (0, 0)) and then placed them. With matrices, placing a shape is always:

> **world = translation(where) × rotation(how much turned) × scaling(how big) × local**

Right to left: scale it while its home point is at (0, 0), turn it while its home point is still at (0, 0), and finally move it to where it belongs.

We call this one matrix the shape's **placement**. Everything in this chapter is built from placements.

---

## 33.3 Hierarchies: parts attached to parts

📖 **New word: hierarchy** — a family tree of parts. Each part is attached to a **parent**, and when the parent moves, the part moves with it.

📖 **New words: parent and child** — the part something is attached to, and the part attached to it.

📖 **New word: joint** — the place where a child is attached to its parent, and where it can turn.

Think of your arm:

```
   body ── shoulder ── upper arm ── elbow ── forearm ── wrist ── hand
   (parent of)        (parent of)          (parent of)
```

When you turn your shoulder, the upper arm turns — and the forearm and hand **go with it**, without you thinking about them. When you bend your elbow, only the forearm and hand move.

### The rule

Give each part its own **local** coordinates, with (0, 0) at its joint, and its length along the x-axis. Then:

> **child's world matrix = parent's world matrix × (where the joint is on the parent) × (the joint's turn)**

For our robot arm (upper arm 100 long, forearm 80 long):

```cpp
Mat3 upper = base * rotation(shoulder);
Mat3 fore = upper * translation(100.0, 0.0) * rotation(elbow);
Mat3 hand = fore * translation(80.0, 0.0) * rotation(wrist);
```

Read `fore` right to left, as a story about a point on the forearm:

1. `rotation(elbow)`: turn it at the elbow joint (the forearm's own (0, 0)).
2. `translation(100.0, 0.0)`: move it to the end of the upper arm (in the **upper arm's** local coordinates — that is where the elbow is).
3. `upper`: now it is a point of the upper arm, so do everything the upper arm does (turn at the shoulder, move to the body).

🔢 **Maths: where is the elbow?**

> The elbow is the forearm's (0, 0). fore × (0, 0) = upper × translation(100, 0) × (0, 0) = upper × (100, 0).
> With shoulder = −60° and the base at (200, 250): rotation(−60°) × (100, 0) = (100 cos(−60°), 100 sin(−60°)) = (50, −86.6) → + (200, 250) = **(250, 163.4)**
> Up and to the right of the shoulder ✓ (−60° turns counter-clockwise on the screen, Chapter 30)

🔢 **Maths: where is the wrist?**

> hand × (0, 0) = fore × (80, 0). The forearm's world direction is shoulder + elbow = −60° + 40° = **−20°** (turns about joints simply add along the chain).
> (250, 163.4) + 80 × (cos(−20°), sin(−20°)) = (250 + 75.2, 163.4 − 27.4) = **(325.2, 136.0)**

`arm.ppm` draws the same arm in three poses, from pale to dark. Only three angles change between poses, but every part moves correctly, because each matrix is built from its parent's.

### A sun, a planet and a moon

The same idea makes a little solar system:

```cpp
Mat3 planet = sunPlace * rotation(t) * translation(130.0, 0.0);
Mat3 moon = planet * rotation(13.0 * t) * translation(35.0, 0.0);
```

- The **planet** is 130 pixels out from the Sun, and that arm turns by t.
- The **moon** is 35 pixels out from the **planet** (in the planet's own coordinates), and that arm turns 13 times faster.

As t goes once round (0 to 2π), the program records where the planet and the moon are (720 steps), and draws both paths. The planet's path is a circle. The moon's path is a wobbly ring with **13 little loops** — the moon goes round the planet 13 times while the planet goes round the Sun once. We never wrote a formula for that curly path: it simply comes out of multiplying the matrices.

🔢 **Maths: why loops?**

> The moon's arm is turned by t (from the planet's matrix) plus 13t (its own): **14t** in all. So around the planet the moon moves 35 × 14 = **490** pixels for each 1 that t grows, while the planet carries it forward only **130**.
> When the moon is on the **inside** of its little circle, it moves backwards faster than the planet carries it forwards, so its path doubles back: a loop. Relative to the planet's arm it goes round 13 times, so there are 13 loops.

---

## 33.4 The inverse: undoing a matrix

📖 **New word: inverse matrix** — the matrix that **undoes** M. We write it **M⁻¹** ("M inverse"). Doing M and then M⁻¹ (or the other way round) changes nothing:

> **M × M⁻¹ = M⁻¹ × M = identity**

For simple matrices we already know the inverse (Chapter 31): translation(t) is undone by translation(−t), rotation(θ) by rotation(−θ), scaling(s) by scaling(1/s). But what about a matrix made of a long chain, like a placement?

### Undoing a chain

If M = A × B (B first, then A), then to undo it we must undo **A first**, then undo B — like taking off your shoes before your socks:

> **(A × B)⁻¹ = B⁻¹ × A⁻¹**

That is one way. But there is a neat formula that works for **any** of our matrices directly.

### The 2 × 2 part

Take the a, b, c, d part. Try multiplying it by the matrix you get by **swapping a and d** and putting **minus signs on b and c**:

```
[ a  b ]   [  d  −b ]     [ a d − b c      −a b + b a ]     [ a d − b c      0     ]
[ c  d ] × [ −c   a ]  =  [ c d − d c      −c b + d a ]  =  [     0      a d − b c ]
```

The result is the identity times **a d − b c** — which is the **determinant** (Chapter 32, Section 32.12)! So divide by it, and we get exactly the identity:

> **inverse of [a b; c d] = (1 / det) × [d −b; −c a]**, where det = a d − b c

### The moving part

M first does the a, b, c, d part (call it A), then adds the move t. To undo it: first **take away** the move, then undo A:

> M⁻¹ × p = A⁻¹ × (p − t) = A⁻¹ × p − A⁻¹ × t

So the inverse has A⁻¹ as its 2 × 2 part, and **−A⁻¹ × t** as its moving part.

🔢 **Maths: the inverse of M = translation(10, 5) × scaling(2, 4)**

```
M = [ 2  0  10 ]        det = 2 × 4 − 0 × 0 = 8
    [ 0  4   5 ]
    [ 0  0   1 ]
```

> A⁻¹ = (1/8) × [4 0; 0 2] = [0.5 0; 0 0.25] — scale by a half across and a quarter down ✓
> moving part: −A⁻¹ × (10, 5) = −(0.5 × 10, 0.25 × 5) = **(−5, −1.25)**

```
M⁻¹ = [ 0.5   0     −5    ]
      [ 0     0.25  −1.25 ]
      [ 0     0      1    ]
```

> Check on M's result for (1, 1): M × (1, 1) = (12, 9). M⁻¹ × (12, 9) = (6 − 5, 2.25 − 1.25) = **(1, 1)** ✓

The program prints M, M⁻¹ and M × M⁻¹, which comes out as the identity.

And for a harder one — a 30° turn about (50, 50) after a scale by 1.5:

```
(7, 3) goes to (38.542, -9.15416) and comes back to (7, 3)
```

### When there is no inverse

📖 **New word: invertible** — a matrix that has an inverse.

If det = 0 we would divide by zero. That happens when the matrix **squashes** everything flat: scaling(1, 0) squashes every point onto the level line y = 0. Then (3, 5) and (3, 7) both land on (3, 0) — and from (3, 0) there is no way to know which one it was. Nothing can undo it. The program prints:

```
can scaling(1, 0) be undone? no
```

Our `inverse` function returns `false` in that case (and leaves the result alone). Because `double` arithmetic has tiny rounding errors (Chapter 30), we treat any |det| smaller than 10⁻¹² (written `1e-12`) as 0.

### A note about −0

When the program printed the inverse, a few entries were computed as `-b / det` with b = 0. In `double` arithmetic, −0 / 8 is **−0** — a real value in the `double` type, equal to 0 in every comparison, but printed as `-0`. To keep the printout tidy, our `printMatrix` passes each entry through `clean`, which turns −0 into 0. (`v == 0.0` is true for both 0 and −0, so `clean` returns a plain 0.0 for both.)

---

## 33.5 Transforming a whole picture

So far we have transformed **shapes**: lists of points. Now we want to turn a whole **picture** — every pixel of it — by 30°.

📖 **New words: source and destination** — the picture we copy **from**, and the picture we copy **into**.

### The first idea: forward mapping (and why it fails)

📖 **New word: forward mapping** — for each **source** pixel, find where its centre goes with M, and paint that destination pixel.

It sounds right. But look at what happens when we make a picture **2.5 times bigger**: the source has 120 × 90 = 10,800 pixels, and the enlarged picture covers 300 × 225 = 67,500 pixels. Each source pixel paints just **one** destination pixel, so only 10,800 of the 67,500 are painted — about 1 in 6. The rest are **holes**: the background shows through in a grid of gaps.

```
   forward:  source pixels      destination (2.5×)
             ■■■                ■ · ■ · · ■ · ■
             ■■■        →       · · · · · · · ·
                                ■ · ■ · · ■ · ■     ← most pixels never get painted
```

Turning has the same problem in a sneakier way: neighbouring source pixels land on destination pixels in a pattern that sometimes **skips** one, leaving scattered holes along diagonal lines, and sometimes hits the same pixel **twice**.

### The good idea: inverse mapping

📖 **New word: inverse mapping** (or backward mapping) — for each **destination** pixel, ask: **where did you come from?** Apply **M⁻¹** to its centre, and copy the colour of the source pixel found there.

This is the "undo the transformation" trick of Chapter 31, Section 31.10 — now for pictures. Every destination pixel asks once, so every destination pixel gets exactly one answer: **no holes, no doubles**.

```
   for each destination pixel (x, y):
       s = M⁻¹ × (x + 0.5, y + 0.5)        ← where its centre came from
       if s is inside the source picture:
           copy source pixel (floor(s.x), floor(s.y))
```

📖 **New word: nearest neighbour** — `floor(s.x), floor(s.y)` picks the **one** source pixel that the point s falls in (pixel k covers k ≤ x < k + 1, Chapter 19). Its colour is copied exactly. This gives blocky edges when enlarging — each source pixel becomes a little square of 2 or 3 destination pixels. In Chapter 35 we will **blend** the four nearest source pixels instead (bilinear sampling) to make it smooth.

🔢 **Maths: one destination pixel, scaled 2.5 times**

> M = translation(300, 15) × scaling(2.5, 2.5). M⁻¹ = scaling(0.4, 0.4) × translation(−300, −15).
> Destination pixel (312, 40): centre (312.5, 40.5) → minus (300, 15) → (12.5, 25.5) → × 0.4 → **(5, 10.2)**
> floor → source pixel **(5, 10)**

`holes.ppm` shows the same picture enlarged 2.5 times both ways: forward mapping on the left (a dotted, full-of-holes mess), inverse mapping on the right (solid, if blocky).

---

## 33.6 Which pixels to visit: the box

Inverse mapping visits destination pixels. Which ones? Visiting all of them works (pixels whose source position is outside the source are just skipped), but it is slow when the picture is small and the destination is big. Better: visit only the **box** the transformed picture covers.

The source picture is the rectangle from (0, 0) to (width, height). Its four corners go to four points under M, and because straight edges stay straight (Chapter 31), the whole transformed picture is **inside** those four points. So:

1. transform the four corners;
2. take the smallest and biggest x and y;
3. round outward (floor and ceil), as in Chapter 31, Section 31.11.

🔢 **Maths: the 120 × 90 test picture, centred at (100, 110) and turned 30°**

> M = translation(100, 110) × rotation(30°) × translation(−60, −45) (move the picture's middle to (0, 0), turn, move to (100, 110))
> corner (0, 0) → step from the middle (−60, −45) → turned: (−60 × 0.866 + 45 × 0.5, −60 × 0.5 − 45 × 0.866) = (−29.5, −69.0) → **(70.5, 41.0)**
> corner (120, 0) → (60, −45) → (52 + 22.5, 30 − 39) = (74.5, −9) → **(174.5, 101.0)**
> corner (120, 90) → (60, 45) → (52 − 22.5, 30 + 39) = (29.5, 69) → **(129.5, 179.0)**
> corner (0, 90) → (−60, 45) → (−52 − 22.5, −30 + 39) = (−74.5, 9) → **(25.5, 119.0)**
> x from 25.5 to 174.5, y from 41.0 to 179.0 → box **(25, 41) to (175, 179)**

The program prints `box of the turned picture: 25, 41 to 175, 179`. That is 150 × 138 pixels to visit — about 20,700 — and roughly 10,800 of them get painted (a turned picture still has its 120 × 90 area: the determinant of a turn is 1, Chapter 32).

`moved.ppm` shows the test picture three times: turned by 30°, enlarged 1.6 times, and skewed — each about its own middle.

---

## Code, part 1: `combine.h`

File: `common/combine.h` (new). It includes `matrix.h`.

```cpp
#ifndef COMBINE_H
#define COMBINE_H

#include <algorithm>
#include <cmath>
#include "matrix.h"

inline Mat3 rotationAbout(PointF centre, double radians) {
    return translation(centre.x, centre.y) * rotation(radians) * translation(-centre.x, -centre.y);
}

inline Mat3 scalingAbout(PointF centre, double sx, double sy) {
    return translation(centre.x, centre.y) * scaling(sx, sy) * translation(-centre.x, -centre.y);
}

inline bool inverse(const Mat3& t, Mat3& result) {
    double det = determinant(t);
    if (std::fabs(det) < 1e-12) {
        return false;
    }
    double a = t.m[0][0];
    double b = t.m[0][1];
    double c = t.m[1][0];
    double d = t.m[1][1];
    Mat3 r;
    r.m[0][0] = d / det;
    r.m[0][1] = -b / det;
    r.m[1][0] = -c / det;
    r.m[1][1] = a / det;
    double tx = t.m[0][2];
    double ty = t.m[1][2];
    r.m[0][2] = -(r.m[0][0] * tx + r.m[0][1] * ty);
    r.m[1][2] = -(r.m[1][0] * tx + r.m[1][1] * ty);
    result = r;
    return true;
}

inline Rect transformedBox(const Mat3& t, int width, int height) {
    PointF corners[4] = {PointF{0.0, 0.0}, PointF{static_cast<double>(width), 0.0},
                         PointF{static_cast<double>(width), static_cast<double>(height)},
                         PointF{0.0, static_cast<double>(height)}};
    PointF first = applyToPoint(t, corners[0]);
    double minX = first.x;
    double maxX = first.x;
    double minY = first.y;
    double maxY = first.y;
    for (int i = 1; i < 4; ++i) {
        PointF p = applyToPoint(t, corners[i]);
        minX = std::min(minX, p.x);
        maxX = std::max(maxX, p.x);
        minY = std::min(minY, p.y);
        maxY = std::max(maxY, p.y);
    }
    return Rect{static_cast<int>(std::floor(minX)), static_cast<int>(std::floor(minY)),
                static_cast<int>(std::ceil(maxX)), static_cast<int>(std::ceil(maxY))};
}

inline void drawImageForward(Image& dest, const Image& source, const Mat3& t) {
    for (int y = 0; y < source.height(); ++y) {
        for (int x = 0; x < source.width(); ++x) {
            PointF p = applyToPoint(t, PointF{x + 0.5, y + 0.5});
            int dx = static_cast<int>(std::floor(p.x));
            int dy = static_cast<int>(std::floor(p.y));
            dest.setPixel(dx, dy, source.getPixel(x, y));
        }
    }
}

inline void drawImageTransformed(Image& dest, const Image& source, const Mat3& t) {
    Mat3 back;
    if (!inverse(t, back)) {
        return;
    }
    Rect box = clipToImage(transformedBox(t, source.width(), source.height()), dest);
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            PointF s = applyToPoint(back, PointF{x + 0.5, y + 0.5});
            int sx = static_cast<int>(std::floor(s.x));
            int sy = static_cast<int>(std::floor(s.y));
            if (source.isInside(sx, sy)) {
                dest.setPixel(x, y, source.getPixel(sx, sy));
            }
        }
    }
}

#endif
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef COMBINE_H` / `#define COMBINE_H` | Include guard. |
| 4–6 | `#include <algorithm>` / `<cmath>` / `"matrix.h"` | `std::min` and `std::max`; `std::fabs`, `std::floor`, `std::ceil`; and `Mat3` with everything before it. |
| 8–10 | `inline Mat3 rotationAbout(PointF centre, double radians) { return translation(centre.x, centre.y) * rotation(radians) * translation(-centre.x, -centre.y); }` | Turn around a pivot (Section 33.1). Right to left: pivot to origin, turn, back. |
| 12–14 | `inline Mat3 scalingAbout(PointF centre, double sx, double sy) { ... }` | The same with a scale. |
| 16 | `inline bool inverse(const Mat3& t, Mat3& result) {` | Find the inverse of t (Section 33.4). It returns **two** things: `true`/`false` (does an inverse exist?), and the inverse itself, written into `result` (passed by reference, so the function can fill it in). |
| 17–20 | `double det = determinant(t); if (std::fabs(det) < 1e-12) { return false; }` | `std::fabs` is the size of a `double` without its sign. A determinant of (nearly) 0 means "squashed flat": no inverse. `result` is not touched. |
| 21–24 | `double a = t.m[0][0];` … `double d = t.m[1][1];` | Short names for the 2 × 2 part, so the formula below reads like the maths. |
| 25–29 | `Mat3 r; r.m[0][0] = d / det; r.m[0][1] = -b / det; r.m[1][0] = -c / det; r.m[1][1] = a / det;` | (1/det) × [d −b; −c a]. `r` starts as the identity, so its bottom row is already (0, 0, 1). |
| 30–31 | `double tx = t.m[0][2];` / `double ty = t.m[1][2];` | The moving part of t. |
| 32–33 | `r.m[0][2] = -(r.m[0][0] * tx + r.m[0][1] * ty);` / `r.m[1][2] = ...` | The new moving part: −A⁻¹ × t. |
| 34–36 | `result = r;` `return true;` `}` | Hand back the inverse, and say "it worked". |
| 38 | `inline Rect transformedBox(const Mat3& t, int width, int height) {` | The pixel box a width × height picture covers after t (Section 33.6). |
| 39–41 | `PointF corners[4] = {...};` | The four corners of the picture: (0, 0), (width, 0), (width, height), (0, height). (The **corners** of the picture, not pixel centres: the picture covers the whole area up to x = width.) The `static_cast<double>` turns the `int` sizes into `double`s for `PointF`. |
| 42–46 | `PointF first = applyToPoint(t, corners[0]); double minX = first.x;` … | Start the smallest and biggest values at the first corner. |
| 47–53 | `for (int i = 1; i < 4; ++i) { PointF p = applyToPoint(t, corners[i]); minX = std::min(minX, p.x); ... }` | Look at the other three corners and keep the extremes. |
| 54–56 | `return Rect{static_cast<int>(std::floor(minX)), ..., static_cast<int>(std::ceil(maxY))};` `}` | Round outward, and make a half-open `Rect` (Chapter 19). |
| 58 | `inline void drawImageForward(Image& dest, const Image& source, const Mat3& t) {` | **The wrong way**, kept so we can see its holes (Section 33.5). |
| 59–60 | `for (int y = 0; y < source.height(); ++y) { for (int x = 0; x < source.width(); ++x) {` | Visit every **source** pixel. |
| 61 | `PointF p = applyToPoint(t, PointF{x + 0.5, y + 0.5});` | Where its centre goes. |
| 62–64 | `int dx = static_cast<int>(std::floor(p.x));` … `dest.setPixel(dx, dy, source.getPixel(x, y));` | Paint the destination pixel it lands in. (`setPixel` ignores pixels outside the picture, Chapter 11.) |
| 65–67 | `}` `}` `}` | End of the loops and the function. |
| 69 | `inline void drawImageTransformed(Image& dest, const Image& source, const Mat3& t) {` | **The right way**: inverse mapping with nearest neighbour. Only pixels covered by the transformed picture are changed; the rest of `dest` stays as it was, so we can draw several pictures into one. |
| 70–73 | `Mat3 back; if (!inverse(t, back)) { return; }` | We need M⁻¹. A squashed-flat matrix draws nothing (the picture would have no area anyway). |
| 74 | `Rect box = clipToImage(transformedBox(t, source.width(), source.height()), dest);` | Only visit the box, cut to the destination (Chapter 19). |
| 75–76 | `for (int y = box.y0; y < box.y1; ++y) { for (int x = box.x0; x < box.x1; ++x) {` | Visit every **destination** pixel in the box. |
| 77 | `PointF s = applyToPoint(back, PointF{x + 0.5, y + 0.5});` | Where did this pixel's centre come from? |
| 78–79 | `int sx = static_cast<int>(std::floor(s.x));` / `int sy = ...` | The source pixel that position falls in: nearest neighbour. |
| 80–82 | `if (source.isInside(sx, sy)) { dest.setPixel(x, y, source.getPixel(sx, sy)); }` | Corners of the box lie outside the turned picture; their source position is outside the source, so we leave those pixels alone. |
| 83–85 | `}` `}` `}` | End of the loops and the function. |
| 87 | `#endif` | End of the include guard. |

---

## Code, part 2: an arm, a solar system, and moving pictures

File: `ch33/combine.cpp`

```cpp
#include <iostream>
#include <vector>
#include "combine.h"

double clean(double v) {
    return (v == 0.0) ? 0.0 : v;
}

void printMatrix(const char* label, const Mat3& t) {
    std::cout << label << "\n";
    for (int row = 0; row < 3; ++row) {
        std::cout << "  " << clean(t.m[row][0]) << "  " << clean(t.m[row][1]) << "  "
                  << clean(t.m[row][2]) << "\n";
    }
}

Image makeTestPicture() {
    Image pic(120, 90, colours::white);
    for (int y = 0; y < 90; ++y) {
        for (int x = 0; x < 120; ++x) {
            if ((x / 15 + y / 15) % 2 == 0) {
                pic.setPixel(x, y, Colour{200, 215, 240});
            }
        }
    }
    drawArrowAA(pic, PointF{60.0, 78.0}, PointF{60.0, 12.0}, 10.0, colours::red);
    fillCircleAA(pic, 15.0, 15.0, 8.0, Colour{0, 150, 0});
    return pic;
}

void drawArm(Image& image, const Mat3& base, double shoulder, double elbow, double wrist,
             Colour col) {
    PointF origin{0.0, 0.0};
    Mat3 upper = base * rotation(degreesToRadians(shoulder));
    fillCapsuleAA(image, applyToPoint(upper, origin), applyToPoint(upper, PointF{100.0, 0.0}), 9.0,
                  col);
    Mat3 fore = upper * translation(100.0, 0.0) * rotation(degreesToRadians(elbow));
    fillCapsuleAA(image, applyToPoint(fore, origin), applyToPoint(fore, PointF{80.0, 0.0}), 7.0, col);
    Mat3 hand = fore * translation(80.0, 0.0) * rotation(degreesToRadians(wrist));
    PointF wristPoint = applyToPoint(hand, origin);
    fillCapsuleAA(image, wristPoint, applyToPoint(hand, PointF{20.0, -10.0}), 3.0, col);
    fillCapsuleAA(image, wristPoint, applyToPoint(hand, PointF{20.0, 10.0}), 3.0, col);
    PointF elbowPoint = applyToPoint(fore, origin);
    fillCircleAA(image, elbowPoint.x, elbowPoint.y, 9.0, Colour{60, 60, 70});
}

int main() {
    Vec2 turned = applyToPoint(rotationAbout(PointF{2.0, 2.0}, degreesToRadians(90.0)),
                               Vec2{5.0, 2.0});
    std::cout << "rotationAbout (2, 2) by 90 degrees sends (5, 2) to (" << turned.x << ", "
              << turned.y << ")\n";
    printMatrix("scalingAbout((2, 2), 2, 2):", scalingAbout(PointF{2.0, 2.0}, 2.0, 2.0));

    Mat3 m = translation(10.0, 5.0) * scaling(2.0, 4.0);
    Mat3 back;
    inverse(m, back);
    printMatrix("M = translation(10, 5) * scaling(2, 4):", m);
    printMatrix("inverse of M:", back);
    printMatrix("M * inverse:", m * back);

    Mat3 spin = rotationAbout(PointF{50.0, 50.0}, degreesToRadians(30.0)) * scaling(1.5, 1.5);
    Mat3 unspin;
    inverse(spin, unspin);
    Vec2 there = applyToPoint(spin, Vec2{7.0, 3.0});
    Vec2 home = applyToPoint(unspin, there);
    std::cout << "(7, 3) goes to (" << there.x << ", " << there.y << ") and comes back to ("
              << home.x << ", " << home.y << ")\n";
    Mat3 flat;
    std::cout << "can scaling(1, 0) be undone? " << (inverse(scaling(1.0, 0.0), flat) ? "yes" : "no")
              << "\n";

    Image pic = makeTestPicture();
    Mat3 placeRotated = translation(100.0, 110.0) * rotation(degreesToRadians(30.0)) *
                        translation(-60.0, -45.0);
    Rect box = transformedBox(placeRotated, pic.width(), pic.height());
    std::cout << "box of the turned picture: " << box.x0 << ", " << box.y0 << " to " << box.x1
              << ", " << box.y1 << "\n";

    Image arm(400, 300, Colour{240, 240, 235});
    fillRect(arm, Rect{170, 250, 230, 300}, Colour{90, 90, 100});
    Mat3 shoulderPlace = translation(200.0, 250.0);
    drawArm(arm, shoulderPlace, -140.0, 60.0, 30.0, Colour{190, 200, 230});
    drawArm(arm, shoulderPlace, -100.0, 30.0, -20.0, Colour{120, 140, 210});
    drawArm(arm, shoulderPlace, -60.0, 40.0, 20.0, Colour{40, 70, 180});

    Image solar(400, 400, Colour{5, 5, 20});
    Mat3 sunPlace = translation(200.0, 200.0);
    std::vector<PointF> planetPath;
    std::vector<PointF> moonPath;
    PointF origin{0.0, 0.0};
    for (int i = 0; i <= 720; ++i) {
        double t = 2.0 * kPi * i / 720.0;
        Mat3 planet = sunPlace * rotation(t) * translation(130.0, 0.0);
        Mat3 moon = planet * rotation(13.0 * t) * translation(35.0, 0.0);
        planetPath.push_back(applyToPoint(planet, origin));
        moonPath.push_back(applyToPoint(moon, origin));
    }
    drawPolylineWu(solar, planetPath, Colour{70, 70, 100});
    drawPolylineWu(solar, moonPath, Colour{60, 160, 170});
    fillCircleAA(solar, 200.0, 200.0, 25.0, colours::yellow);
    double now = degreesToRadians(40.0);
    Mat3 planetNow = sunPlace * rotation(now) * translation(130.0, 0.0);
    Mat3 moonNow = planetNow * rotation(13.0 * now) * translation(35.0, 0.0);
    PointF p = applyToPoint(planetNow, origin);
    PointF q = applyToPoint(moonNow, origin);
    fillCircleAA(solar, p.x, p.y, 10.0, Colour{60, 120, 255});
    fillCircleAA(solar, q.x, q.y, 4.0, colours::white);

    Image moved(600, 220, Colour{230, 230, 230});
    drawImageTransformed(moved, pic, placeRotated);
    drawImageTransformed(moved, pic, translation(300.0, 110.0) * scaling(1.6, 1.6) *
                                         translation(-60.0, -45.0));
    drawImageTransformed(moved, pic, translation(500.0, 110.0) * skew(0.5, 0.0) *
                                         translation(-60.0, -45.0));

    Image holes(600, 255, Colour{230, 230, 230});
    drawImageForward(holes, pic, translation(0.0, 15.0) * scaling(2.5, 2.5));
    drawImageTransformed(holes, pic, translation(300.0, 15.0) * scaling(2.5, 2.5));

    bool ok = arm.savePPM("arm.ppm");
    ok = ok && solar.savePPM("solar.ppm");
    ok = ok && moved.savePPM("moved.ppm");
    ok = ok && holes.savePPM("holes.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
```

Build and run (from the `code/ch33` folder):

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common combine.cpp -o combine
./combine
```

### Line by line

**Helpers (lines 1–45)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–3 | the `#include` lines | Printing, lists, and the new header. |
| 5–7 | `double clean(double v) { return (v == 0.0) ? 0.0 : v; }` | Turn −0 into 0 for printing (Section 33.4). |
| 9–15 | `void printMatrix(const char* label, const Mat3& t) { ... }` | Chapter 32's printer, with `clean` on every entry. |
| 17–18 | `Image makeTestPicture() { Image pic(120, 90, colours::white);` | A small picture to turn and stretch. It **returns** a whole `Image`. |
| 19–25 | `for (int y = 0; y < 90; ++y) { for (int x = 0; x < 120; ++x) { if ((x / 15 + y / 15) % 2 == 0) { pic.setPixel(x, y, Colour{200, 215, 240}); } } }` | A checkerboard of 15-pixel squares: `x / 15` and `y / 15` are integer divisions — the square's column and row number. When their sum is even, the square is light blue. |
| 26 | `drawArrowAA(pic, PointF{60.0, 78.0}, PointF{60.0, 12.0}, 10.0, colours::red);` | A red arrow pointing **up** (Chapter 29), so you can see which way the picture has turned. |
| 27–29 | `fillCircleAA(pic, 15.0, 15.0, 8.0, Colour{0, 150, 0});` `return pic;` `}` | A green dot in the top-left corner, so you can see mirrors and corners. |
| 31–32 | `void drawArm(Image& image, const Mat3& base, double shoulder, double elbow, double wrist, Colour col) {` | Draw a robot arm in one pose (Section 33.3). The three angles are in degrees. |
| 33 | `PointF origin{0.0, 0.0};` | Every part's joint is at its own (0, 0). |
| 34 | `Mat3 upper = base * rotation(degreesToRadians(shoulder));` | The upper arm: turned at the shoulder, then placed by `base`. |
| 35–36 | `fillCapsuleAA(image, applyToPoint(upper, origin), applyToPoint(upper, PointF{100.0, 0.0}), 9.0, col);` | Draw it as a capsule (Chapter 29) from its joint (0, 0) to its end (100, 0), both in local coordinates, made world by `upper`. |
| 37 | `Mat3 fore = upper * translation(100.0, 0.0) * rotation(degreesToRadians(elbow));` | The forearm: turned at the elbow, moved to the end of the upper arm, then everything the upper arm does. |
| 38 | `fillCapsuleAA(... PointF{80.0, 0.0}), 7.0, col);` | The forearm is 80 long and a little thinner. |
| 39 | `Mat3 hand = fore * translation(80.0, 0.0) * rotation(degreesToRadians(wrist));` | The hand, at the end of the forearm. |
| 40–42 | `PointF wristPoint = applyToPoint(hand, origin);` and two `fillCapsuleAA` calls | Two short "fingers" from the wrist, to (20, −10) and (20, 10) in the hand's coordinates: a little claw that turns with the hand. |
| 43–45 | `PointF elbowPoint = applyToPoint(fore, origin); fillCircleAA(image, elbowPoint.x, elbowPoint.y, 9.0, Colour{60, 60, 70});` `}` | A dark disk on the elbow joint. |

**The numbers (lines 47–77)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 48–51 | `Vec2 turned = applyToPoint(rotationAbout(PointF{2.0, 2.0}, degreesToRadians(90.0)), Vec2{5.0, 2.0});` … | The pivot matrix gives the same answer as Chapter 31 (Section 33.1). |
| 52 | `printMatrix("scalingAbout((2, 2), 2, 2):", ...);` | The matrix of Section 33.1. |
| 54–59 | `Mat3 m = translation(10.0, 5.0) * scaling(2.0, 4.0); Mat3 back; inverse(m, back);` and three `printMatrix` calls | M, its inverse, and their product (Section 33.4). We know M can be undone, so we do not check the `bool` here. |
| 61–67 | `Mat3 spin = ...; Mat3 unspin; inverse(spin, unspin);` … | A point goes there and back again. |
| 68–70 | `Mat3 flat; std::cout << ... (inverse(scaling(1.0, 0.0), flat) ? "yes" : "no")` | A matrix that cannot be undone. |
| 72 | `Image pic = makeTestPicture();` | Make the test picture. |
| 73–74 | `Mat3 placeRotated = translation(100.0, 110.0) * rotation(degreesToRadians(30.0)) * translation(-60.0, -45.0);` | The picture's middle (60, 45) to the origin, turn, then to (100, 110) (Section 33.6). |
| 75–77 | `Rect box = transformedBox(placeRotated, pic.width(), pic.height());` and printing | The box worked out in Section 33.6. |

**The robot arm (lines 79–84)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 79–80 | `Image arm(400, 300, ...); fillRect(arm, Rect{170, 250, 230, 300}, Colour{90, 90, 100});` | A light picture with a dark grey body block at the bottom. |
| 81 | `Mat3 shoulderPlace = translation(200.0, 250.0);` | The shoulder is on top of the body block. |
| 82–84 | three `drawArm` calls | Three poses, pale to dark: (−140°, 60°, 30°), (−100°, 30°, −20°) and (−60°, 40°, 20°). |

**The solar system (lines 86–107)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 86–90 | `Image solar(...);` `Mat3 sunPlace = translation(200.0, 200.0);` two path lists, `PointF origin{0.0, 0.0};` | A night sky, the Sun in the middle, and lists for the two paths. |
| 91–92 | `for (int i = 0; i <= 720; ++i) { double t = 2.0 * kPi * i / 720.0;` | 721 moments, t from 0 to 2π (the last equals the first, closing the paths). |
| 93 | `Mat3 planet = sunPlace * rotation(t) * translation(130.0, 0.0);` | The planet: 130 out, turned by t, around the Sun. |
| 94 | `Mat3 moon = planet * rotation(13.0 * t) * translation(35.0, 0.0);` | The moon: 35 out from the planet, turning 13 times as fast — the **child** of the planet. |
| 95–97 | `planetPath.push_back(applyToPoint(planet, origin));` … | Each body is at its own (0, 0): record where that is in the world. |
| 98–100 | two `drawPolylineWu` calls and `fillCircleAA(..., colours::yellow)` | The planet's circle, the moon's looping path, and the Sun on top. |
| 101–107 | `double now = degreesToRadians(40.0);` … two `fillCircleAA` calls | The planet (blue) and the moon (white) at one moment, t = 40°. |

**Moving pictures (lines 109–118)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 109 | `Image moved(600, 220, Colour{230, 230, 230});` | A light grey picture with room for three panels. |
| 110 | `drawImageTransformed(moved, pic, placeRotated);` | The test picture turned by 30° about its middle, centred at (100, 110). |
| 111–112 | `... translation(300.0, 110.0) * scaling(1.6, 1.6) * translation(-60.0, -45.0)` | Enlarged 1.6 times about its middle (192 × 144), centred at (300, 110). |
| 113–114 | `... translation(500.0, 110.0) * skew(0.5, 0.0) * translation(-60.0, -45.0)` | Skewed about its middle (Chapter 32), centred at (500, 110). |
| 116 | `Image holes(600, 255, Colour{230, 230, 230});` | Room for two 300 × 225 enlargements. |
| 117 | `drawImageForward(holes, pic, translation(0.0, 15.0) * scaling(2.5, 2.5));` | Left: forward mapping — full of holes. |
| 118 | `drawImageTransformed(holes, pic, translation(300.0, 15.0) * scaling(2.5, 2.5));` | Right: inverse mapping — solid. |

**Saving (lines 120–129)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 120–123 | `bool ok = arm.savePPM("arm.ppm");` … | Save the four pictures. |
| 124–129 | `if (!ok) { ... }` `return 0;` `}` | Report a problem, or finish. |

### What you should see

```
rotationAbout (2, 2) by 90 degrees sends (5, 2) to (2, 5)
scalingAbout((2, 2), 2, 2):
  2  0  -2
  0  2  -2
  0  0  1
M = translation(10, 5) * scaling(2, 4):
  2  0  10
  0  4  5
  0  0  1
inverse of M:
  0.5  0  -5
  0  0.25  -1.25
  0  0  1
M * inverse:
  1  0  0
  0  1  0
  0  0  1
(7, 3) goes to (38.542, -9.15416) and comes back to (7, 3)
can scaling(1, 0) be undone? no
box of the turned picture: 25, 41 to 175, 179
```

Open the pictures:
- `arm.ppm`: a grey body block with a robot arm in three poses, pale to dark, each with a little two-fingered claw.
- `solar.ppm`: a yellow Sun, a grey circular orbit, and a teal moon path with 13 small loops around it; a blue planet and a white moon at one moment.
- `moved.ppm`: the checkerboard-and-arrow picture turned by 30° (the arrow leans right), enlarged, and skewed.
- `holes.ppm`: on the left, the enlarged picture as a grid of separate dots with grey between them; on the right, the same enlargement filled in solidly, with blocky (nearest-neighbour) edges.

---

## Small examples

### Example 1 — A pivot matrix by hand

rotationAbout((10, 0), 90°) on the point (10, 5):

> step from the pivot: (0, 5) → turned 90°: (−5, 0) → plus the pivot: **(5, 0)**
> The point was below the pivot; after a clockwise quarter turn it is to the left ✓

### Example 2 — Undo a chain in reverse

M = translation(5, 0) × rotation(90°). Then M⁻¹ = rotation(−90°) × translation(−5, 0): first take the move away, **then** turn back.

> M × (1, 0) = (5, 1). M⁻¹ × (5, 1): minus (5, 0) → (0, 1); turn by −90° → (1, 0) ✓

### Example 3 — A skew's inverse

skew(0.5, 0) has det = 1 × 1 − 0.5 × 0 = 1. Its inverse is (1/1) × [1 −0.5; 0 1] = **skew(−0.5, 0)**: slide the cards back.

### Example 4 — The arm, all at once

With all three joints at 0°, the arm is straight along the x-axis: the elbow at base × (100, 0), the wrist at base × (180, 0). Turn **only** the shoulder by 90°, and the whole straight arm points down — the hand swings along a quarter circle of radius 180 without you touching its matrix.

### Example 5 — How many pixels does forward mapping miss?

Enlarging 120 × 90 by 2.5: 67,500 destination pixels, 10,800 painted by forward mapping. Holes: 67,500 − 10,800 = **56,700** — 84 %.

---

## Common mistakes

⚠️ **The pivot sandwich in the wrong order.** It is translation(C) × rotation × translation(**−C**). Swap the two translations and the pivot moves by 2C.

⚠️ **Parent on the wrong side.** In a hierarchy, the **parent's** matrix goes on the **left**: `child = parent * joint`. Putting it on the right makes the parent move **inside** the child's coordinates.

⚠️ **Undoing a chain in the same order.** (A × B)⁻¹ is B⁻¹ × A⁻¹, **not** A⁻¹ × B⁻¹. Shoes off before socks.

⚠️ **Using an inverse that does not exist.** Check the `bool` that `inverse` returns before you use the result.

⚠️ **Forward mapping a picture.** It leaves holes when enlarging or turning. Always go backwards: for each destination pixel, ask where it came from — with **M⁻¹**, not M.

⚠️ **Forgetting the + 0.5.** Apply M⁻¹ to the pixel **centre** (x + 0.5, y + 0.5), not to (x, y), or the whole picture shifts by half a pixel (and a turned picture turns around the wrong point).

⚠️ **Boxing pixel centres instead of corners.** The picture covers 0 ≤ x < width, so transform the corners (0, 0) and (width, height), not (0.5, 0.5) and (width − 0.5, height − 0.5), or the box may cut off the edge pixels.

---

## Practice

🏋️ **1.** Write the matrix scalingAbout((10, 20), 3, 3) as numbers. Check that (10, 20) stays put.

🏋️ **2.** Find the inverse of [2 1; 1 1] (with no move) using the formula. Multiply to check.

🏋️ **3.** Find the inverse of translation(4, −2) × skew(1, 0), then check it on the point (1, 1).

🏋️ **4.** In the solar system, give the moon its own tiny moon ("moonmoon"), 10 pixels out, turning 40 times as fast. Draw its path. What do you see?

🏋️ **5.** Draw the robot arm reaching toward a target: try shoulder angles from −180° to 0° in steps of 10° (elbow and wrist at 0°), and draw only the pose whose wrist is closest to the point (340, 120).

🏋️ **6.** Mirror the test picture left–right with `drawImageTransformed`. Which matrix do you need, so that it stays in the same place?

🏋️ **7.** Turn the test picture by 45° using **forward** mapping, without scaling. Count (with a loop over the destination) how many pixels inside the turned area are holes.

🏋️ **8.** Why is the inverse of a rotation matrix the same as **swapping its rows and columns** (that is, m[i][j] ↔ m[j][i])? Use the formula and det = 1.

---

## Answers

**1.**

```
[ 3  0  −20 ]       moving part: C − 3C = −2C = (−20, −40)
[ 0  3  −40 ]
[ 0  0    1 ]
```

> (10, 20) → (30 − 20, 60 − 40) = (10, 20) ✓

**2.**
> det = 2 × 1 − 1 × 1 = 1 → inverse = [1 −1; −1 2]
> [2 1; 1 1] × [1 −1; −1 2] = [2 − 1, −2 + 2; 1 − 1, −1 + 2] = [1 0; 0 1] ✓

**3.**
> M = [1 1 4; 0 1 −2; 0 0 1]. det = 1. A⁻¹ = [1 −1; 0 1]. Moving part: −A⁻¹ × (4, −2) = −(4 + 2, −2) = (−6, 2).
> M⁻¹ = [1 −1 −6; 0 1 2; 0 0 1]
> M × (1, 1) = (1 + 1 + 4, 1 − 2) = (6, −1). M⁻¹ × (6, −1) = (6 + 1 − 6, −1 + 2) = **(1, 1)** ✓

**4.**

```cpp
std::vector<PointF> tinyPath;
for (int i = 0; i <= 4000; ++i) {
    double t = 2.0 * kPi * i / 4000.0;
    Mat3 planet = sunPlace * rotation(t) * translation(130.0, 0.0);
    Mat3 moon = planet * rotation(13.0 * t) * translation(35.0, 0.0);
    Mat3 tiny = moon * rotation(40.0 * t) * translation(10.0, 0.0);
    tinyPath.push_back(applyToPoint(tiny, origin));
}
drawPolylineWu(solar, tinyPath, Colour{230, 120, 200});
```

> Small loops on top of the moon's loops: a "spirograph" of loops-within-loops. (It needs more steps — 4000 — because it changes direction so often.)

**5.**

```cpp
PointF target{340.0, 120.0};
double best = 0.0;
double bestDistance = 1e9;
for (int a = -180; a <= 0; a += 10) {
    Mat3 upper = shoulderPlace * rotation(degreesToRadians(a));
    PointF wristPoint = applyToPoint(upper, PointF{180.0, 0.0});
    double dd = distance(wristPoint, target);
    if (dd < bestDistance) {
        bestDistance = dd;
        best = a;
    }
}
drawArm(arm, shoulderPlace, best, 0.0, 0.0, colours::red);
```

> With straight joints, the wrist is 180 from the shoulder (200, 250). The target is (140, −130) away: a distance of √(140² + 130²) ≈ 191, in the direction atan2(−130, 140) ≈ −42.9° (Chapter 30). The nearest 10° step is **−40°**, and its wrist is about 14.5 pixels from the target. (To reach it exactly, the elbow would have to bend — or the arm would need to be longer.)

**6.**
> The mirror must happen about the picture's middle: translation(x, y) × scaling(−1, 1) × translation(−60, −45). For example, for the panel centred at (100, 110): `drawImageTransformed(moved, pic, translation(100.0, 110.0) * scaling(-1.0, 1.0) * translation(-60.0, -45.0));` The green dot moves to the top-**right**. (The inverse exists: det = −1, not 0.)

**7.**
> Use `drawImageForward` with M = translation(100, 110) × rotation(45°) × translation(−60, −45) into a fresh picture. To know which destination pixels are **inside** the turned rectangle, use the inverse: a pixel is inside when M⁻¹ × (x + 0.5, y + 0.5) has 0 ≤ s.x < 120 and 0 ≤ s.y < 90. To find the holes, fill the fresh picture with a colour that the test picture never uses (for example magenta), and count the inside pixels that are still magenta.
> There are about 10,700 inside pixels, and about **1,800** of them are holes — 1 in 6 — in neat diagonal rows. About the same number of pixels were painted **twice** (the 10,800 source pixels have to go somewhere).

**8.**
> rotation(θ) = [cos θ, −sin θ; sin θ, cos θ], det = cos²θ + sin²θ = 1.
> Inverse = (1/1) × [cos θ, sin θ; −sin θ, cos θ] (swap a and d — both cos θ — and change the signs of b and c).
> That is exactly the rows and columns swapped ✓ — and it is rotation(−θ), as it must be: cos(−θ) = cos θ, sin(−θ) = −sin θ.

---

## Summary

🧠 A turn or scale **about a pivot C** is one matrix: **translation(C) × rotation × translation(−C)**.

🧠 Placing a shape: **world = translation × rotation × scaling × local**.

🧠 Hierarchies: **child = parent × translation(where the joint is) × rotation(joint angle)**. Move the parent and all the children follow.

🧠 The **inverse** M⁻¹ undoes M. 2 × 2 part: **(1/det) × [d −b; −c a]**. Moving part: **−A⁻¹ t**. det = 0 → no inverse. (A × B)⁻¹ = B⁻¹ × A⁻¹.

🧠 To transform a **picture**, use **inverse mapping**: for each destination pixel centre, s = M⁻¹ × (x + 0.5, y + 0.5), and copy source pixel (floor(s.x), floor(s.y)). Forward mapping leaves **holes**.

🧠 Only visit the **box** made by transforming the picture's four corners.

---

## Next chapter

So far, all our curves have come from circles and ellipses. In Chapter 34 we meet the curves that designers use every day — in fonts, logos, drawing programs and SVG files: **Bézier curves**. They are built from nothing more than **lerp** (Chapter 13) used again and again on a few "control points", and we will draw them as smooth polylines, fill shapes made from them, and join them into long smooth paths.
