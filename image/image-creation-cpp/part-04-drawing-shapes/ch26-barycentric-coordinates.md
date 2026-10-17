# Chapter 26 — Barycentric Coordinates: Colouring Inside a Triangle

> **Part 4 · Chapter 26 of 82**
> **You need:** Chapters 1–25 (especially 13, 17 and 24) · **You will make:** `barycentric.h` (barycentric weights, points from weights, triangles with a colour at each corner), `rgb.ppm`, `quad.ppm` and `pattern.ppm`

---

## What you will learn

- How to describe a point by **"how much"** of each corner of a triangle it has.
- These three numbers — the **barycentric coordinates** — come straight from the edge functions of Chapter 24.
- Why they always **add up to 1**.
- What they mean: corners, edges, the centre, and **areas**.
- How to go **back** from the three numbers to the point.
- How to give each corner of a triangle its **own colour** and blend smoothly between them.
- Why the blending should happen in **linear light** (Chapter 17).
- Why a square made of two coloured triangles shows a **crease**, and how it differs from **bilinear** blending.
- How barycentric coordinates let a **pattern** stick to a triangle.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **weight** | A number that says how much one thing counts in a mix. |
| **weighted average** | A mix where each part has its own weight, and the weights add up to 1. |
| **barycentric coordinates** | Three weights (λ0, λ1, λ2) that describe a point by how much of each triangle corner it has. |
| **λ (lambda)** | A Greek letter, often used for weights. We write it `l` in code: `l0`, `l1`, `l2`. |
| **centroid** | The centre of a triangle: the average of its three corners. Its weights are ⅓, ⅓, ⅓. |
| **interpolation** | Finding in-between values from known values (Chapter 13 did it on a line; here we do it on a triangle). |
| **Gouraud shading** | Giving each corner a colour and blending across the triangle (named after Henri Gouraud, 1971). |
| **quad** | A shape with four corners (short for "quadrilateral"). |
| **crease** | A visible line, like the fold in a piece of paper. |
| **bilinear** | Blending in two directions, one after the other: first along x, then along y. |

---

## 26.1 One colour per corner

All the triangles so far had **one** colour. But look at a real ball in sunlight: it is bright on one side and dark on the other, with every shade in between. 3D programs make this kind of smooth change with a very simple trick:

1. Give each **corner** of a triangle its own colour.
2. For each pixel inside, **mix** the three corner colours.
3. A pixel close to a corner gets mostly that corner's colour; a pixel in the middle gets an even mix.

📖 **New word: Gouraud shading** — this trick, named after Henri Gouraud, who described it in 1971. It is still used in every graphics card.

The question is: **how much** of each corner does a pixel get? We need three numbers — one per corner — that say "how close" the pixel is to each corner, in a way that blends smoothly.

In Chapter 13 we solved this on a **line**: from A to B, the point at t has (1 − t) of A and t of B. Now we do the same thing on a **triangle**.

---

## 26.2 Weights from the edge functions

📖 **New word: weight** — a number that says how much something counts.

📖 **New word: weighted average** — a mix where each part has a weight, and the weights add up to 1. For example, a drink of 70 % water and 30 % juice: weights 0.7 and 0.3.

Remember Chapter 24, Section 24.5: for a point P and a triangle A, B, C,

> w0 = E(B, C, P), w1 = E(C, A, P), w2 = E(A, B, P)

and, for **every** P:

> **w0 + w1 + w2 = E(A, B, C)** (twice the area of the whole triangle)

Divide all three by E(A, B, C):

> **λ0 = w0 / E(A, B, C)**
> **λ1 = w1 / E(A, B, C)**
> **λ2 = w2 / E(A, B, C)**

📖 **New word: λ (lambda)** — a Greek letter, the usual name for these weights. In code we write `l0`, `l1`, `l2`.

Now they add up to exactly **1**:

> λ0 + λ1 + λ2 = (w0 + w1 + w2) / E(A, B, C) = E(A, B, C) / E(A, B, C) = **1**

📖 **New word: barycentric coordinates** — these three weights (λ0, λ1, λ2). ("Barycentre" is an old word for "centre of weight": the point where a shape would balance on your finger.)

🔢 **Maths: P = (3.5, 3.5) in the triangle A = (0, 0), B = (10, 0), C = (0, 10)**

From Chapter 24, Section 24.5:

> w0 = 30, w1 = 35, w2 = 35, E(A, B, C) = 100
> λ0 = 30 / 100 = **0.3**, λ1 = 35 / 100 = **0.35**, λ2 = 35 / 100 = **0.35**
> sum: 0.3 + 0.35 + 0.35 = **1** ✓

So P is "30 % A, 35 % B, 35 % C". Our program prints exactly these numbers.

---

## 26.3 What the weights mean

### Each weight is a share of the area

Remember that each w is twice the area of a small triangle: P together with one edge (Chapter 24, Section 24.5). So:

> λ0 = (area of the small triangle P, B, C) / (area of the whole triangle)

```
          A ●───────────────● B
             ╲ ╲    λ2    ╱ ╱
              ╲   ╲     ╱  ╱       λ0 = the share of P–B–C (opposite A)
               ╲ λ1 ● P   ╱        λ1 = the share of P–C–A (opposite B)
                ╲   │ λ0 ╱         λ2 = the share of P–A–B (opposite C)
                 ╲  │   ╱
                  ╲ │  ╱
                   ╲│ ╱
                    ●
                    C
```

The closer P comes to corner A, the **bigger** the small triangle opposite A gets — so λ0 grows. When P reaches A, that triangle is the whole triangle, and λ0 = 1.

### Special places

| where P is | λ0, λ1, λ2 | why |
|---|---|---|
| at corner A | 1, 0, 0 | the triangle opposite A is the whole triangle; the other two are flat |
| at corner B | 0, 1, 0 | |
| at corner C | 0, 0, 1 | |
| on the edge BC | 0, something, something | P is on the line BC, so E(B, C, P) = 0 |
| in the middle of BC | 0, ½, ½ | halfway between B and C |
| at the **centroid** | ⅓, ⅓, ⅓ | the three small triangles have the same area |

📖 **New word: centroid** — the centre of a triangle: the average of the three corners,

> centroid = ((A.x + B.x + C.x) / 3, (A.y + B.y + C.y) / 3)

It is the balance point: if you cut the triangle out of cardboard, it balances on a pin at its centroid.

🔢 **Maths: the centroid of A = (0, 0), B = (10, 0), C = (0, 10)**

> centroid = (10/3, 10/3) = (3.333…, 3.333…)
> w0 = E(B, C, P) = (0 − 10)(3.333 − 0) − (10 − 0)(3.333 − 10) = −33.33 + 66.67 = 33.33
> λ0 = 33.33 / 100 = **0.3333** = ⅓ ✓ (and the same for λ1 and λ2)

---

## 26.4 From the weights back to the point

The weights **describe** the point completely. If you know λ0, λ1, λ2, you can find P again:

> **P = λ0 × A + λ1 × B + λ2 × C**

which means, for each coordinate:

> P.x = λ0 × A.x + λ1 × B.x + λ2 × C.x
> P.y = λ0 × A.y + λ1 × B.y + λ2 × C.y

🔢 **Maths: back from (0.3, 0.35, 0.35)**

> P.x = 0.3 × 0 + 0.35 × 10 + 0.35 × 0 = **3.5**
> P.y = 0.3 × 0 + 0.35 × 0 + 0.35 × 10 = **3.5** ✓

This is exactly like Chapter 13's lerp, but with three points instead of two. In fact, on the edge from B to C (λ0 = 0), it **is** lerp: λ1 = 1 − t and λ2 = t give P = (1 − t) × B + t × C.

💡 This is why the weights must add up to 1. If they added up to 2, the "average" of the corners would land twice as far from (0, 0) as it should — not inside the triangle at all.

---

## 26.5 Outside the triangle

A point **outside** still has barycentric coordinates, and they still add up to 1 — but at least one of them is **negative**.

🔢 **Maths: P = (8, 8), outside our triangle**

> w0 = E(B, C, P) = (−10)(8) − (10)(8 − 10) = −80 + 20 = −60 → λ0 = **−0.6**
> w1 = E(C, A, P) = (0)(8 − 10) − (−10)(8) = 80 → λ1 = **0.8**
> w2 = E(A, B, P) = (10)(8) − (0)(8) = 80 → λ2 = **0.8**
> sum: −0.6 + 0.8 + 0.8 = **1** ✓

P is on the far side of the edge BC — "more than 100 % of B and C, and a negative amount of A".

🧠 **Remember:** P is inside the triangle exactly when **all three weights are ≥ 0**. (That is the same test as Chapter 24, just divided by the area.)

---

## 26.6 The corner order does not matter

In Chapter 24 we had to **swap** two corners when the triangle was counter-clockwise, because otherwise all the w's were negative inside.

With barycentric coordinates there is no such problem. If the triangle is counter-clockwise, all the w's are negative inside — but so is E(A, B, C)! A negative divided by a negative is positive:

🔢 **Maths: the same point, the corners in the order A, C, B**

> E(A, C, B) = (0 − 0)(0 − 0) − (10 − 0)(10 − 0) = **−100**
> λ for A: E(C, B, P) / −100 = (10 − 0)(3.5 − 10) − (0 − 10)(3.5 − 0) = (−65 + 35) = −30 → −30 / −100 = **0.3** ✓
> and the weights of C and B are 0.35 each, as before

The program shows it with the line "other order": the same three numbers. Each corner keeps its own weight, whatever order you give the corners in.

---

## 26.7 Mixing three colours

📖 **New word: interpolation** — finding in-between values from known values.

Now the main idea of the chapter. Give each corner a colour: cA, cB and cC. For a pixel with weights λ0, λ1, λ2:

> **colour = λ0 × cA + λ1 × cB + λ2 × cC**

for each channel (red, green, blue) separately — using `ColourF` and its `+` and `*` from Chapter 14.

🔢 **Maths: a red, green and blue triangle, at the point (0.3, 0.35, 0.35)**

> cA = red = (1, 0, 0), cB = green = (0, 1, 0), cC = blue = (0, 0, 1) (as `ColourF`, from 0 to 1)
> colour = 0.3 × (1, 0, 0) + 0.35 × (0, 1, 0) + 0.35 × (0, 0, 1) = **(0.3, 0.35, 0.35)**

At corner A, the weights are (1, 0, 0), so the colour is exactly cA. Along the edge from A to B, it is the Chapter 13 gradient from cA to cB. Inside, it is a smooth mix of all three.

### In sRGB or in linear light?

Chapter 17 taught us that the numbers in a picture file are **gamma-encoded** (sRGB): 128 is not half the light of 255. If we mix the **file numbers** directly, the mixes come out too **dark**. To mix **light** correctly, we:

1. convert the corner colours to **linear light** (`toLinear`),
2. mix them,
3. convert the result back (`fromLinear`).

🔢 **Maths: the centroid of the red–green–blue triangle**

> weights (⅓, ⅓, ⅓)
> mixing the file numbers: (255/3, 255/3, 255/3) = **(85, 85, 85)** — a dark grey
> mixing in linear light: each channel is ⅓ of full light → linearToSrgb(⅓) ≈ 0.613 → × 255 ≈ **(156, 156, 156)** — a medium grey

The linear mix is **much** lighter, and it is the correct one: one third of red light, one third of green and one third of blue really do add up to one third of white light. (With the formulas of Chapter 17: the file number for one third of white's light is about 156, not 85.)

Our `rgb.ppm` shows both triangles side by side. In the left one (file numbers), the middle has a dark, muddy band. In the right one (linear light), the colours stay bright and the middle is a clean, light grey.

Our `fillTriangleColours` has a last parameter `linearLight`, true by default.

---

## 26.8 The weights change in equal steps

In Chapter 24, Section 24.8, we saw that an edge function changes by a **fixed amount** from one pixel to the next. The weights are just the edge functions divided by a fixed number (E(A, B, C)), so they also change by fixed amounts:

> one step right: λ0 changes by −(C.y − B.y) / E(A, B, C)
> one step down: λ0 changes by +(C.x − B.x) / E(A, B, C)

(and the same for λ1 with the edge C→A, and λ2 with the edge A→B).

🔢 **Maths: the triangle A = (0, 0), B = (20, 0), C = (0, 10)**

> E(A, B, C) = (20)(10) − (0)(0) = 200
> one step right: λ0 changes by −(10 − 0) / 200 = **−0.05**
> one step down: λ0 changes by +(0 − 20) / 200 = **−0.1**

So λ0 goes down by 0.05 for each step to the right, and by 0.1 for each step down. Our program prints λ0 × 10 (rounded down) for every pixel of this triangle:

```
weight of corner A (l0), times 10:
  9887766554433221100.
  87766554433221100...
  766554433221100.....
  6554433221100.......
  54433221100.........
  433221100...........
  3221100.............
  21100...............
  100.................
  0...................
```

Read along the first row: 9, 8, 8, 7, 7, 6, … — it drops by 1 every **two** pixels (0.05 × 10 = 0.5 per pixel). Read down the first column: 9, 8, 7, 6, … — it drops by 1 every pixel (0.1 × 10 = 1). The pattern of equal "contour lines" shows that λ0 is a **flat slope** across the triangle, highest at A (top-left) and 0 along the far edge BC.

Because the weights change in equal steps, the **colours** change in equal steps too. That is why the colour mix looks so smooth: there are no bumps anywhere inside the triangle.

---

## 26.9 A square from two triangles: the crease

📖 **New word: quad** — a shape with four corners.

3D models are made of triangles, so a square with a colour at each of its four corners is drawn as **two** triangles. Let us try. Our `quad.ppm` uses:

> top-left: red, top-right: yellow, bottom-right: blue, bottom-left: yellow

and cuts the square along the diagonal from top-left to bottom-right.

Look at the **diagonal**. It belongs to both triangles, and on it, the colour only mixes the two diagonal corners: red and blue. The two yellow corners have **no** influence there at all (their weight is 0 on the diagonal). So a purple line runs right across the yellow-orange square.

📖 **New word: crease** — a visible line, like the fold in paper. This is a famous problem of colour-per-corner triangles.

🔢 **Maths: the colour at the centre of the square**

> two triangles: the centre is the middle of the diagonal → ½ red + ½ blue, in linear light → (0.5, 0, 0.5) → about **(188, 0, 188)**, purple
> but the "fair" answer would use all four corners equally: ¼ red + ½ yellow + ¼ blue = (0.75, 0.5, 0.25) in linear light → about **(225, 188, 137)**, a light orange

### Bilinear blending

📖 **New word: bilinear** — blending in two directions, one after the other.

The right half of `quad.ppm` is drawn differently, pixel by pixel, without triangles:

1. Find u (how far across, 0 to 1) and v (how far down, 0 to 1).
2. Blend along the **top** edge: top = lerp(top-left, top-right, u).
3. Blend along the **bottom** edge: bottom = lerp(bottom-left, bottom-right, u).
4. Blend **between** them: colour = lerp(top, bottom, v).

All four corners take part everywhere, so there is no crease: the centre is the light orange (225, 188, 137). We meet bilinear blending again in Chapter 35, where it makes resized pictures smooth.

💡 So why do graphics cards use triangles at all? Because a triangle is always flat, simple and fast (Chapter 24), and the crease becomes invisible when the triangles are small. Real 3D models use thousands of small triangles, not two big ones.

---

## 26.10 Coordinates that stick: patterns

Barycentric coordinates are not only for colours. **Any** value can be given to the corners and blended: a brightness, a depth, a position in a picture.

Here is a nice experiment. We use λ1 and λ2 as **coordinates inside the triangle**, and draw a checkerboard with them:

> u = floor(λ1 × 8), v = floor(λ2 × 8)
> if u + v is even → first colour, else → second colour

🔢 **Maths: two pixels in the black-and-white triangle**

> at the corner A (λ1 = 0, λ2 = 0): u = 0, v = 0 → 0 is even → black
> a pixel with λ1 = 0.2, λ2 = 0.1: u = floor(1.6) = 1, v = floor(0.8) = 0 → 1 is odd → white

In `pattern.ppm`, the left triangle is a right-angled triangle, and the checkerboard looks like ordinary squares cut by the slanted edge. The right triangle is tilted and stretched — and the checkerboard **tilts and stretches with it**. The pattern **sticks** to the triangle, like a printed sticker stuck on a piece of rubber.

This is the main idea of **texture mapping** (Chapter 70): every corner of a 3D triangle gets a position in a picture (a "texture"), and barycentric coordinates find the position for every pixel in between. That is how a game puts a brick picture on a wall, or a face on a character.

---

## Code, part 1: `barycentric.h`

File: `common/barycentric.h` (new). It includes `fill.h` (and through it `triangles.h`, `srgb.h`, `colourf.h` and everything else).

```cpp
#ifndef BARYCENTRIC_H
#define BARYCENTRIC_H

#include <algorithm>
#include <cmath>
#include "fill.h"

struct Barycentric {
    double l0 = 0.0;
    double l1 = 0.0;
    double l2 = 0.0;
};

inline Barycentric barycentric(PointF a, PointF b, PointF c, PointF p) {
    double area2 = edgeFunction(a, b, c);
    if (area2 == 0.0) {
        return Barycentric{-1.0, -1.0, -1.0};
    }
    Barycentric w;
    w.l0 = edgeFunction(b, c, p) / area2;
    w.l1 = edgeFunction(c, a, p) / area2;
    w.l2 = edgeFunction(a, b, p) / area2;
    return w;
}

inline PointF fromBarycentric(PointF a, PointF b, PointF c, Barycentric w) {
    return PointF{w.l0 * a.x + w.l1 * b.x + w.l2 * c.x,
                  w.l0 * a.y + w.l1 * b.y + w.l2 * c.y};
}

inline bool allPositive(Barycentric w) {
    return w.l0 >= 0.0 && w.l1 >= 0.0 && w.l2 >= 0.0;
}

inline ColourF mixThree(ColourF ca, ColourF cb, ColourF cc, Barycentric w) {
    return ca * w.l0 + cb * w.l1 + cc * w.l2;
}

inline void fillTriangleColours(Image& image, PointF a, PointF b, PointF c,
                                Colour ca, Colour cb, Colour cc, bool linearLight = true) {
    double area2 = edgeFunction(a, b, c);
    if (area2 == 0.0) {
        return;
    }
    if (area2 < 0.0) {
        std::swap(b, c);
        std::swap(cb, cc);
        area2 = -area2;
    }
    ColourF fa = linearLight ? toLinear(ca) : toColourF(ca);
    ColourF fb = linearLight ? toLinear(cb) : toColourF(cb);
    ColourF fc = linearLight ? toLinear(cc) : toColourF(cc);
    int x0 = static_cast<int>(std::floor(std::min({a.x, b.x, c.x})));
    int y0 = static_cast<int>(std::floor(std::min({a.y, b.y, c.y})));
    int x1 = static_cast<int>(std::ceil(std::max({a.x, b.x, c.x})));
    int y1 = static_cast<int>(std::ceil(std::max({a.y, b.y, c.y})));
    Rect box = clipToImage(Rect{x0, y0, x1, y1}, image);
    bool topLeft0 = isTopLeft(b, c);
    bool topLeft1 = isTopLeft(c, a);
    bool topLeft2 = isTopLeft(a, b);
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            PointF p{x + 0.5, y + 0.5};
            double w0 = edgeFunction(b, c, p);
            double w1 = edgeFunction(c, a, p);
            double w2 = edgeFunction(a, b, p);
            if (edgeCovers(w0, topLeft0) && edgeCovers(w1, topLeft1) &&
                edgeCovers(w2, topLeft2)) {
                Barycentric w{w0 / area2, w1 / area2, w2 / area2};
                ColourF mixed = mixThree(fa, fb, fc, w);
                image.setPixel(x, y, linearLight ? fromLinear(mixed) : toColour(mixed));
            }
        }
    }
}

#endif
```

### Line by line

**The start and the weights (lines 1–24)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef BARYCENTRIC_H` / `#define BARYCENTRIC_H` | Include guard. |
| 4–5 | `#include <algorithm>` / `#include <cmath>` | `std::min`, `std::max`, `std::swap`; `std::floor`, `std::ceil`. |
| 6 | `#include "fill.h"` | Everything before: `PointF`, `edgeFunction`, `isTopLeft`, `edgeCovers`, `ColourF`, `toLinear`, `fromLinear`, … |
| 8–12 | `struct Barycentric { double l0 = 0.0; double l1 = 0.0; double l2 = 0.0; };` | The three weights λ0, λ1, λ2 (for the corners a, b, c). |
| 14 | `inline Barycentric barycentric(PointF a, PointF b, PointF c, PointF p) {` | The barycentric coordinates of p in the triangle a, b, c (Section 26.2). |
| 15 | `double area2 = edgeFunction(a, b, c);` | Twice the signed area of the triangle. |
| 16–18 | `if (area2 == 0.0) { return Barycentric{-1.0, -1.0, -1.0}; }` | A flat triangle has no area, and we cannot divide by 0. We return −1, −1, −1: negative weights, so `allPositive` says "outside" for every point. (If we returned 0, 0, 0, every point would count as **inside**, and a flat triangle would paint the whole image!) |
| 19 | `Barycentric w;` | The answer, filled in below. |
| 20–22 | `w.l0 = edgeFunction(b, c, p) / area2;` … `w.l2 = edgeFunction(a, b, p) / area2;` | λ0 = w0 / E, λ1 = w1 / E, λ2 = w2 / E. Dividing by the **signed** area makes the order of the corners unimportant (Section 26.6). |
| 23–24 | `return w;` `}` | Done. |

**Back to a point, the inside test, and mixing (lines 26–37)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 26–29 | `inline PointF fromBarycentric(PointF a, PointF b, PointF c, Barycentric w) { return PointF{w.l0 * a.x + w.l1 * b.x + w.l2 * c.x, w.l0 * a.y + ...}; }` | P = λ0·A + λ1·B + λ2·C (Section 26.4), for x and for y. |
| 31–33 | `inline bool allPositive(Barycentric w) { return w.l0 >= 0.0 && w.l1 >= 0.0 && w.l2 >= 0.0; }` | Inside (or on an edge) when no weight is negative (Section 26.5). (The name says "positive"; 0 also counts.) |
| 35–37 | `inline ColourF mixThree(ColourF ca, ColourF cb, ColourF cc, Barycentric w) { return ca * w.l0 + cb * w.l1 + cc * w.l2; }` | The weighted average of three colours (Section 26.7). It uses `*` (colour times number) and `+` (colour plus colour) from Chapter 14. |

**A triangle with three colours (lines 39–75)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 39–40 | `inline void fillTriangleColours(Image& image, PointF a, PointF b, PointF c, Colour ca, Colour cb, Colour cc, bool linearLight = true) {` | Fill the triangle; corner a has colour ca, b has cb, c has cc. Mix in linear light unless told otherwise. |
| 41–44 | `double area2 = edgeFunction(a, b, c);` / `if (area2 == 0.0) { return; }` | As in `fillTriangle`: a flat triangle draws nothing. |
| 45–49 | `if (area2 < 0.0) { std::swap(b, c); std::swap(cb, cc); area2 = -area2; }` | Make it clockwise, for the top-left rule. When we swap two **corners**, we must also swap their **colours**, so each colour stays with its corner. The area changes sign too. |
| 50–52 | `ColourF fa = linearLight ? toLinear(ca) : toColourF(ca);` … | Turn the three corner colours into numbers from 0 to 1 — in linear light (Chapter 17), or just divided by 255 (Chapter 14). We do this **once**, not for every pixel. |
| 53–57 | the bounding box and `clipToImage` | The same as `fillTriangle` (Chapter 24). |
| 58–60 | `bool topLeft0 = isTopLeft(b, c);` … | The top-left rule, as in Chapter 24. |
| 61–66 | the loops, `PointF p{x + 0.5, y + 0.5};`, `w0`, `w1`, `w2` | Every pixel centre in the box, and its three edge values. |
| 67–68 | `if (edgeCovers(w0, topLeft0) && ... ) {` | Inside? Exactly the same test as `fillTriangle`, so the shape is exactly the same. |
| 69 | `Barycentric w{w0 / area2, w1 / area2, w2 / area2};` | The weights. We already have the edge values, so we just divide (we do not call `barycentric`, which would compute them again). |
| 70 | `ColourF mixed = mixThree(fa, fb, fc, w);` | Mix the three colours. |
| 71 | `image.setPixel(x, y, linearLight ? fromLinear(mixed) : toColour(mixed));` | Turn the mix back into a `Colour` — from linear light, or just × 255 — and set the pixel. |
| 72–75 | `}` `}` `}` `}` | End. |
| 77 | `#endif` | End of the include guard. |

---

## Code, part 2: weights, an RGB triangle, a crease, and patterns

File: `ch26/barycentric.cpp`

```cpp
#include <cmath>
#include <iostream>
#include <string>
#include "barycentric.h"

void printWeights(const std::string& name, PointF a, PointF b, PointF c, PointF p) {
    Barycentric w = barycentric(a, b, c, p);
    PointF back = fromBarycentric(a, b, c, w);
    std::cout << name << " (" << p.x << ", " << p.y << "): " << w.l0 << ", " << w.l1 << ", "
              << w.l2 << "  sum " << (w.l0 + w.l1 + w.l2)
              << (allPositive(w) ? "  inside" : "  outside") << "  back to (" << back.x << ", "
              << back.y << ")\n";
}

void printWeightMap(PointF a, PointF b, PointF c, int width, int height) {
    std::cout << "weight of corner A (l0), times 10:\n";
    for (int y = 0; y < height; ++y) {
        std::cout << "  ";
        for (int x = 0; x < width; ++x) {
            Barycentric w = barycentric(a, b, c, PointF{x + 0.5, y + 0.5});
            if (!allPositive(w)) {
                std::cout << '.';
                continue;
            }
            int digit = static_cast<int>(w.l0 * 10.0);
            if (digit > 9) {
                digit = 9;
            }
            std::cout << digit;
        }
        std::cout << "\n";
    }
}

void fillTriangleChecker(Image& image, PointF a, PointF b, PointF c, int squares,
                         Colour first, Colour second) {
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            Barycentric w = barycentric(a, b, c, PointF{x + 0.5, y + 0.5});
            if (!allPositive(w)) {
                continue;
            }
            int u = static_cast<int>(std::floor(w.l1 * squares));
            int v = static_cast<int>(std::floor(w.l2 * squares));
            image.setPixel(x, y, ((u + v) % 2 == 0) ? first : second);
        }
    }
}

int main() {
    PointF a{0.0, 0.0};
    PointF b{10.0, 0.0};
    PointF c{0.0, 10.0};
    PointF centre{(a.x + b.x + c.x) / 3.0, (a.y + b.y + c.y) / 3.0};
    std::cout << "triangle A (0, 0), B (10, 0), C (0, 10); weights l0, l1, l2:\n";
    printWeights("a point", a, b, c, PointF{3.5, 3.5});
    printWeights("the centre", a, b, c, centre);
    printWeights("corner A", a, b, c, a);
    printWeights("middle of BC", a, b, c, PointF{5.0, 5.0});
    printWeights("outside", a, b, c, PointF{8.0, 8.0});
    printWeights("other order", a, c, b, PointF{3.5, 3.5});

    printWeightMap(PointF{0.0, 0.0}, PointF{20.0, 0.0}, PointF{0.0, 10.0}, 20, 10);

    Image rgb(420, 200, colours::white);
    fillTriangleColours(rgb, PointF{110.0, 15.0}, PointF{200.0, 185.0}, PointF{20.0, 185.0},
                        colours::red, colours::green, colours::blue, false);
    fillTriangleColours(rgb, PointF{320.0, 15.0}, PointF{410.0, 185.0}, PointF{230.0, 185.0},
                        colours::red, colours::green, colours::blue, true);

    Image quad(420, 200, colours::white);
    const Colour topLeft = colours::red;
    const Colour topRight = colours::yellow;
    const Colour bottomRight = colours::blue;
    const Colour bottomLeft = colours::yellow;
    PointF p0{20.0, 10.0};
    PointF p1{200.0, 10.0};
    PointF p2{200.0, 190.0};
    PointF p3{20.0, 190.0};
    fillTriangleColours(quad, p0, p1, p2, topLeft, topRight, bottomRight);
    fillTriangleColours(quad, p0, p2, p3, topLeft, bottomRight, bottomLeft);
    for (int y = 10; y < 190; ++y) {
        for (int x = 220; x < 400; ++x) {
            double u = (x + 0.5 - 220.0) / 180.0;
            double v = (y + 0.5 - 10.0) / 180.0;
            Colour top = lerpLinear(topLeft, topRight, u);
            Colour bottom = lerpLinear(bottomLeft, bottomRight, u);
            quad.setPixel(x, y, lerpLinear(top, bottom, v));
        }
    }

    Image pattern(420, 200, Colour{230, 230, 230});
    fillTriangleChecker(pattern, PointF{20.0, 180.0}, PointF{190.0, 180.0}, PointF{20.0, 20.0}, 8,
                        colours::black, colours::white);
    fillTriangleChecker(pattern, PointF{230.0, 150.0}, PointF{400.0, 190.0}, PointF{330.0, 10.0}, 8,
                        Colour{200, 30, 30}, Colour{250, 220, 60});

    bool ok = rgb.savePPM("rgb.ppm");
    ok = ok && quad.savePPM("quad.ppm");
    ok = ok && pattern.savePPM("pattern.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
```

Build and run (from the `code/ch26` folder):

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common barycentric.cpp -o barycentric
./barycentric
```

### Line by line

**Printing the weights (lines 6–13)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 6 | `void printWeights(const std::string& name, PointF a, PointF b, PointF c, PointF p) {` | Print the barycentric coordinates of p, with a name. |
| 7 | `Barycentric w = barycentric(a, b, c, p);` | The three weights. |
| 8 | `PointF back = fromBarycentric(a, b, c, w);` | Rebuild the point from the weights (Section 26.4), as a check. |
| 9–12 | the long `std::cout` line | Print: the point, the three weights, their sum, inside or outside, and the rebuilt point. `std::cout` prints a `double` with up to 6 digits, so ⅓ shows as 0.333333. |
| 13 | `}` | End. |

**The weight map (lines 15–33)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 15 | `void printWeightMap(PointF a, PointF b, PointF c, int width, int height) {` | Print λ0 for every pixel of a small grid (Section 26.8). |
| 17–19 | the row loop, `"  "`, the column loop | Every pixel. |
| 20 | `Barycentric w = barycentric(a, b, c, PointF{x + 0.5, y + 0.5});` | The weights at the pixel centre. |
| 21–24 | `if (!allPositive(w)) { std::cout << '.'; continue; }` | Outside: print a dot. |
| 25–28 | `int digit = static_cast<int>(w.l0 * 10.0); if (digit > 9) { digit = 9; }` | λ0 is between 0 and 1. Times 10 and cut off: a digit from 0 to 9. (Only exactly 1.0 would give 10, so we keep it at 9.) |
| 29 | `std::cout << digit;` | Print it. |
| 30–33 | `}` … `}` | End of the loops and the function. |

**A checkerboard that sticks (lines 35–48)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 35–36 | `void fillTriangleChecker(Image& image, PointF a, PointF b, PointF c, int squares, Colour first, Colour second) {` | A triangle filled with a checkerboard pattern made from its barycentric coordinates (Section 26.10). |
| 37–38 | the loops | Every pixel of the image. (Simple, not fast: fine for one picture.) |
| 39–42 | `Barycentric w = ...; if (!allPositive(w)) { continue; }` | Skip pixels outside the triangle. |
| 43–44 | `int u = static_cast<int>(std::floor(w.l1 * squares));` / `int v = ...(w.l2 * squares)...;` | Which "square" we are in, counting along λ1 and along λ2. |
| 45 | `image.setPixel(x, y, ((u + v) % 2 == 0) ? first : second);` | Even → first colour, odd → second: the checkerboard rule. |
| 46–48 | `}` `}` `}` | End. |

**The text output (lines 50–63)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 51–53 | `PointF a{0.0, 0.0};` … `PointF c{0.0, 10.0};` | The triangle of Sections 26.2–26.6. |
| 54 | `PointF centre{(a.x + b.x + c.x) / 3.0, (a.y + b.y + c.y) / 3.0};` | Its centroid (Section 26.3). |
| 56–60 | five `printWeights` calls | A point inside, the centroid, a corner, the middle of an edge, and a point outside. |
| 61 | `printWeights("other order", a, c, b, PointF{3.5, 3.5});` | The same point with the corners in the order A, C, B (Section 26.6). Now the second number is C's weight and the third is B's. |
| 63 | `printWeightMap(PointF{0.0, 0.0}, PointF{20.0, 0.0}, PointF{0.0, 10.0}, 20, 10);` | The weight map of Section 26.8. |

**The RGB triangles (lines 65–69)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 65 | `Image rgb(420, 200, colours::white);` | A white picture. |
| 66–67 | `fillTriangleColours(rgb, ..., colours::red, colours::green, colours::blue, false);` | Left: red at the top, green at the bottom right, blue at the bottom left, mixed with the **file numbers** (`false`). |
| 68–69 | `fillTriangleColours(rgb, ..., true);` | Right: the same triangle, 210 pixels further right, mixed in **linear light**. |

**The quad (lines 71–90)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 71 | `Image quad(420, 200, colours::white);` | A white picture. |
| 72–75 | `const Colour topLeft = colours::red;` … `const Colour bottomLeft = colours::yellow;` | The four corner colours of Section 26.9. |
| 76–79 | `PointF p0{20.0, 10.0};` … `PointF p3{20.0, 190.0};` | The corners of the left square (180 × 180), clockwise from the top-left. |
| 80 | `fillTriangleColours(quad, p0, p1, p2, topLeft, topRight, bottomRight);` | The upper-right triangle. |
| 81 | `fillTriangleColours(quad, p0, p2, p3, topLeft, bottomRight, bottomLeft);` | The lower-left triangle. They share the diagonal p0–p2. |
| 82–83 | `for (int y = 10; y < 190; ++y) { for (int x = 220; x < 400; ++x) {` | Every pixel of the right square (also 180 × 180). |
| 84–85 | `double u = (x + 0.5 - 220.0) / 180.0;` / `double v = (y + 0.5 - 10.0) / 180.0;` | How far across (u) and down (v) the pixel centre is, from 0 to 1. |
| 86–87 | `Colour top = lerpLinear(topLeft, topRight, u);` / `Colour bottom = lerpLinear(bottomLeft, bottomRight, u);` | Blend along the top edge and along the bottom edge (Chapter 17's lerp in linear light). |
| 88 | `quad.setPixel(x, y, lerpLinear(top, bottom, v));` | Blend between the two: bilinear (Section 26.9). |
| 89–90 | `}` `}` | End. |

**The patterns (lines 92–96)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 92 | `Image pattern(420, 200, Colour{230, 230, 230});` | A light grey picture. |
| 93–94 | `fillTriangleChecker(pattern, PointF{20.0, 180.0}, PointF{190.0, 180.0}, PointF{20.0, 20.0}, 8, colours::black, colours::white);` | A right-angled triangle with an 8-step black-and-white checkerboard. |
| 95–96 | `fillTriangleChecker(pattern, PointF{230.0, 150.0}, PointF{400.0, 190.0}, PointF{330.0, 10.0}, 8, ...);` | A tilted, stretched triangle with a red-and-yellow checkerboard. The pattern follows the triangle's shape. |

**Saving (lines 98–106)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 98–100 | `bool ok = rgb.savePPM("rgb.ppm");` … | Save the three pictures. |
| 101–106 | `if (!ok) { ... }` `return 0;` `}` | Report a problem, or finish. |

### What you should see

The program prints:

```
triangle A (0, 0), B (10, 0), C (0, 10); weights l0, l1, l2:
a point (3.5, 3.5): 0.3, 0.35, 0.35  sum 1  inside  back to (3.5, 3.5)
the centre (3.33333, 3.33333): 0.333333, 0.333333, 0.333333  sum 1  inside  back to (3.33333, 3.33333)
corner A (0, 0): 1, 0, 0  sum 1  inside  back to (0, 0)
middle of BC (5, 5): 0, 0.5, 0.5  sum 1  inside  back to (5, 5)
outside (8, 8): -0.6, 0.8, 0.8  sum 1  outside  back to (8, 8)
other order (3.5, 3.5): 0.3, 0.35, 0.35  sum 1  inside  back to (3.5, 3.5)
weight of corner A (l0), times 10:
  9887766554433221100.
  ...  (the weight map of Section 26.8)
```

Every sum is 1, and every point comes back exactly. ✓

Open the pictures:
- `rgb.ppm`: two triangles with red, green and blue corners. The left one has a darker, muddy middle; the right one (linear light) is brighter, with a light grey centre.
- `quad.ppm`: two squares with the same four corner colours. The left one (two triangles) has a purple line along its diagonal — the crease. The right one (bilinear) blends smoothly, with a light orange centre.
- `pattern.ppm`: a black-and-white checkerboard triangle, and a red-and-yellow one whose squares are tilted and stretched to follow the triangle.

---

## Small examples

### Example 1 — Weights of a corner point of a different triangle

Triangle A = (2, 1), B = (12, 4), C = (4, 10). P = B:

> λ1 is 1 and the others are 0 — without computing anything! (Every corner has weight 1 for itself.)

### Example 2 — Weights halfway along an edge

Triangle A = (0, 0), B = (10, 0), C = (0, 10). P = (5, 0), the middle of AB:

> w0 = E(B, C, P) = (−10)(0) − (10)(5 − 10) = 50 → λ0 = 0.5
> w1 = E(C, A, P) = (0)(0 − 10) − (−10)(5) = 50 → λ1 = 0.5
> w2 = E(A, B, P) = 10 × 0 − 0 = 0 → λ2 = **0** (it is on the edge AB, opposite C)

### Example 3 — The colour at one pixel

Corner colours: A = white (255, 255, 255), B = black (0, 0, 0), C = black. A pixel with weights (0.5, 0.25, 0.25), mixing **file numbers**:

> 0.5 × 255 + 0.25 × 0 + 0.25 × 0 = 127.5 → about (128, 128, 128)

Mixing in **linear light**: 0.5 × 1 = 0.5 of white light → linearToSrgb(0.5) ≈ 0.735 → about **(188, 188, 188)**. (Chapter 17 again: half the light is 188, not 128.)

### Example 4 — Any value can be blended

Give each corner a **brightness**: A = 1.0 (in the light), B = 0.2, C = 0.2 (in shadow). At the centroid:

> ⅓ × 1.0 + ⅓ × 0.2 + ⅓ × 0.2 = 0.4667

Multiply the triangle's colour by this number (Chapter 14, colour × number). This is how simple 3D lighting works: compute the light only at the corners, and blend it across (Chapter 68).

### Example 5 — Does the crease go away with the other diagonal?

Cut the square along the **other** diagonal (top-right to bottom-left). Now the diagonal mixes only yellow and yellow: the crease is **yellow**, and the red and blue corners stay separate. A different crease, but still a crease. Only bilinear blending (or many small triangles) avoids it.

---

## Common mistakes

⚠️ **Forgetting to divide by E(A, B, C).** The edge values w0, w1, w2 add up to twice the area, not to 1. Mixing colours with them gives colours far too bright (or negative).

⚠️ **Swapping corners without swapping their colours.** If you swap b and c for the top-left rule, swap cb and cc too — otherwise the colours move to the wrong corners.

⚠️ **Mixing file numbers instead of light.** The middle comes out too dark (Chapter 17). Mix in linear light.

⚠️ **Mixing up which weight belongs to which corner.** λ0 comes from the edge **opposite** A (B→C), not from an edge that touches A.

⚠️ **Dividing by a zero area.** A flat triangle (all corners on one line) has E(A, B, C) = 0. Check first.

⚠️ **Expecting a quad of two coloured triangles to look like bilinear blending.** It has a crease along the diagonal.

---

## Practice

🏋️ **1.** Find the barycentric coordinates of P = (2, 6) in the triangle A = (0, 0), B = (10, 0), C = (0, 10). Is P inside?

🏋️ **2.** In the same triangle, which point has the weights (0.5, 0.2, 0.3)?

🏋️ **3.** Corner colours red, green and blue, mixing file numbers. What is the colour at the weights (0.5, 0.5, 0)? And at (0.2, 0.3, 0.5)?

🏋️ **4.** For the triangle A = (0, 0), B = (20, 0), C = (0, 10), how much does λ1 (B's weight) change for one step right, and for one step down? Check against the shape of the weight map.

🏋️ **5.** Write `fillTriangleValues`, which takes a brightness (0 to 1) for each corner, and paints each pixel with `base` colour × the blended brightness (Example 4).

🏋️ **6.** Draw a "colour wheel" like Chapter 24's, but with **one** colour per slice corner: the centre white, and each outer corner a different hue. Do the slices meet smoothly?

🏋️ **7.** In `quad.ppm`, what colour is the pixel exactly in the centre of the left square, roughly? And in the right square? (Use Section 26.9.)

🏋️ **8.** (Thinking) Why is the centroid of a triangle at ⅓, ⅓, ⅓, and not somewhere else? Use the areas.

---

## Answers

**1.**
> E(A, B, C) = 100
> w0 = E(B, C, P) = (0 − 10)(6 − 0) − (10 − 0)(2 − 10) = −60 + 80 = 20 → λ0 = **0.2**
> w1 = E(C, A, P) = (0 − 0)(6 − 10) − (0 − 10)(2 − 0) = 0 + 20 = 20 → λ1 = **0.2**
> w2 = E(A, B, P) = (10)(6) − (0)(2) = 60 → λ2 = **0.6**
> sum = 1 ✓, all ≥ 0 → **inside**
> check: 0.2 × (0, 0) + 0.2 × (10, 0) + 0.6 × (0, 10) = (2, 6) ✓

**2.**
> P = 0.5 × (0, 0) + 0.2 × (10, 0) + 0.3 × (0, 10) = (0 + 2 + 0, 0 + 0 + 3) = **(2, 3)**

**3.**
> (0.5, 0.5, 0): 0.5 × (255, 0, 0) + 0.5 × (0, 255, 0) = (127.5, 127.5, 0) → about **(128, 128, 0)**, a dark yellow (olive). It is on the edge AB, so it is the Chapter 13 gradient from red to green.
> (0.2, 0.3, 0.5): (0.2 × 255, 0.3 × 255, 0.5 × 255) = (51, 76.5, 127.5) → about **(51, 77, 128)**, a greyish blue.

**4.**
> λ1 comes from the edge C → A: C = (0, 10), A = (0, 0), E(A, B, C) = 200
> one step right: −(A.y − C.y) / 200 = −(0 − 10) / 200 = **+0.05**
> one step down: +(A.x − C.x) / 200 = (0 − 0) / 200 = **0**

So B's weight grows to the right and does not change at all going down. That makes sense: B = (20, 0) is far to the right, and the edge opposite B (the left edge, x = 0) is vertical — moving down keeps the same distance from it. In the weight map, λ0 + λ1 + λ2 = 1 and λ2 grows going down, so λ0 must shrink both ways — as we saw.

**5.**

```cpp
inline void fillTriangleValues(Image& image, PointF a, PointF b, PointF c,
                               double va, double vb, double vc, Colour base) {
    ColourF baseF = toLinear(base);
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            Barycentric w = barycentric(a, b, c, PointF{x + 0.5, y + 0.5});
            if (!allPositive(w)) {
                continue;
            }
            double v = w.l0 * va + w.l1 * vb + w.l2 * vc;
            image.setPixel(x, y, fromLinear(baseF * v));
        }
    }
}
```

(The brightness is light, so we multiply in linear light. For speed, you would add a bounding box, as in `fillTriangle`.)

**6.**

```cpp
Image wheel(200, 200, colours::white);
PointF centre{100.0, 100.0};
std::vector<PointF> corners = hexagon(100.0, 100.0, 90.0);   // from Chapter 24
for (int i = 0; i < 6; ++i) {
    Colour ci = toColour(hsvToRgb(HSV{i * 60.0, 1.0, 1.0}));
    Colour cj = toColour(hsvToRgb(HSV{((i + 1) % 6) * 60.0, 1.0, 1.0}));
    fillTriangleColours(wheel, centre, corners[i], corners[(i + 1) % 6],
                        colours::white, ci, cj);
}
```

Yes, they meet smoothly: two neighbouring slices share an edge (centre → corner), and on that edge both slices blend **the same two colours** (white and that corner's hue) with the same weights. So the colours match exactly along every shared edge. (The colour **changes direction** at each edge, though, so you may see faint "spokes" — the same kind of crease as Section 26.9.)

**7.**
> left (two triangles): the centre is on the diagonal, halfway between red and blue → about **(188, 0, 188)**, purple
> right (bilinear): about **(225, 188, 137)**, light orange

**8.** At the centroid, the three small triangles (P with each edge) all have the **same area**: each is exactly ⅓ of the whole. (Each small triangle has one edge of the big triangle as its base, and the centroid is ⅓ of the way up from every edge — a known fact about centroids.) Since each weight is "the share of the area", each weight is ⅓.

---

## Summary

🧠 **Barycentric coordinates**: λ0 = E(B, C, P) / E(A, B, C), λ1 = E(C, A, P) / E(A, B, C), λ2 = E(A, B, P) / E(A, B, C).

🧠 They always **add up to 1**. Each one is the **share of the area** of the small triangle opposite its corner.

🧠 Corner A → (1, 0, 0). Edge BC → λ0 = 0. Centroid → (⅓, ⅓, ⅓). **Inside** → all ≥ 0.

🧠 Back to the point: **P = λ0·A + λ1·B + λ2·C** — lerp with three points.

🧠 The corner order does not matter: the signs cancel.

🧠 **Colour per corner**: colour = λ0·cA + λ1·cB + λ2·cC, mixed in **linear light**.

🧠 The weights change in **equal steps** from pixel to pixel: the blend is perfectly smooth.

🧠 A coloured quad made of two triangles has a **crease**; **bilinear** blending does not.

🧠 Barycentric coordinates make **patterns stick** to triangles — the idea behind texture mapping.

---

## Next chapter

Look closely at the edges of any shape we have drawn: they are **jagged**, like little stairs. Each pixel is either fully in or fully out. In Chapter 27 we learn **supersampling**: test many points inside each pixel, and use the **fraction** that is inside to blend the edge smoothly — the first real cure for "the jaggies".
