# Chapter 34 — Bézier Curves

> **Part 5 · Chapter 34 of 82**
> **You need:** Chapters 1–33 (especially 13, 27, 28, 29 and 32) · **You will make:** `bezier.h` (lerping points, quadratic and cubic Bézier curves, their formula and direction, turning curves into polylines, smooth paths through points, and a circle made of curves), `steps.ppm`, `curves.ppm`, `heart.ppm` and `path.ppm`

---

## What you will learn

- What a **Bézier curve** is, and why designers love them.
- How to build one from nothing but **lerp** (Chapter 13), used again and again: **de Casteljau's method**.
- **Quadratic** curves (3 points) and **cubic** curves (4 points).
- The **formula** for a cubic curve, and the "1, 3, 3, 1" pattern hidden inside it.
- Four useful facts: where the curve starts and ends, which way it leaves, where it can never go, and how to transform it.
- The curve's **direction** at any moment.
- How to draw a curve as a **polyline**, and how many pieces to use.
- How to **fill** shapes made of curves, **join** curves smoothly, and draw a smooth path through any list of points.
- How four cubic curves make an almost perfect **circle**.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **Bézier curve** (say "BEZ-ee-ay") | A smooth curve controlled by a few points, built by lerping again and again. |
| **control point** | One of the points that shape a Bézier curve. |
| **end point** | The first or last control point: the curve starts and ends exactly there. |
| **handle** | A control point in the middle (not an end point): it pulls the curve toward it. |
| **control polygon** | The control points joined by straight lines, in order. |
| **quadratic** | Using squares (t²): a Bézier curve with 3 control points. |
| **cubic** | Using cubes (t³): a Bézier curve with 4 control points. |
| **de Casteljau's method** | Finding a point on a Bézier curve by lerping between neighbours until one point is left. |
| **tangent** | The direction a curve is going at one point. |
| **convex hull** | The shape you get by stretching a rubber band around a set of points. |
| **flattening** | Turning a curve into many short straight lines. |
| **smooth join** | Two curves meeting without a corner. |

---

## 34.1 Curves you can steer

So far our curves came from formulas: circles, ellipses, sine waves, spirals. They are beautiful, but you cannot easily **steer** them. A designer drawing the letter S, the outline of a car, or a logo wants to say "start here, end there, and **bend like this**".

In the 1960s, two engineers working for French car makers — **Pierre Bézier** at Renault and **Paul de Casteljau** at Citroën — found the same answer: describe a curve by a few **control points**, and build it with simple lerps. Today these curves are everywhere: every letter you are reading was drawn with them, and so is every curve in drawing programs and SVG files.

📖 **New words: control point, end point and handle** — a Bézier curve is controlled by a short list of points. The curve **starts** at the first and **ends** at the last (the **end points**). The ones in between (the **handles**) pull the curve toward them, like magnets, but the curve usually does not touch them.

📖 **New word: control polygon** — the control points joined in order by straight lines. It is like a rough sketch of the curve.

---

## 34.2 Lerping points

Chapter 13 gave us **lerp** for numbers: lerp(a, b, t) = a + (b − a) × t, which slides from a (t = 0) to b (t = 1). With the vector operators of Chapter 29, it works for **points** too:

> **lerpPoint(A, B, t) = A + (B − A) × t**

It slides along the straight line from A to B: t = 0 gives A, t = 1 gives B, t = 0.5 the middle, t = 0.25 a quarter of the way.

🔢 **Maths: lerpPoint((0, 0), (0, 100), 0.25)**

> (0, 0) + ((0, 100) − (0, 0)) × 0.25 = **(0, 25)**

With **two** control points, this **is** the simplest Bézier curve: a straight line. As t goes from 0 to 1, the point travels from A to B. Things get interesting when we add more points.

---

## 34.3 Quadratic curves: three points

📖 **New word: quadratic** — with **three** control points P0, P1, P2. To find the point at "time" t:

1. lerp along the first side: **a = lerp(P0, P1, t)**
2. lerp along the second side: **b = lerp(P1, P2, t)**
3. lerp between those two: **point = lerp(a, b, t)**

```
                 P1
                 ●
               ╱   ╲
          a  ●───────●  b        a and b slide along the two sides;
           ╱    ●      ╲         the curve point slides along a–b
         ╱   (the point) ╲
     P0 ●                 ● P2
```

As t goes from 0 to 1, a slides from P0 to P1, b slides from P1 to P2, and the point between them traces a smooth arch.

🔢 **Maths: P0 = (0, 0), P1 = (50, 100), P2 = (100, 0), at t = 0.5**

> a = lerp((0, 0), (50, 100), 0.5) = (25, 50)
> b = lerp((50, 100), (100, 0), 0.5) = (75, 50)
> point = lerp((25, 50), (75, 50), 0.5) = **(50, 50)**

The program prints `quadratic (0, 0), (50, 100), (100, 0) at t = 0.5: (50, 50)`.

Notice: the handle P1 is 100 below the line from P0 to P2 (remember y goes down), but the curve only gets **halfway** there, to y = 50. Handles pull, but they do not drag the curve all the way to them.

💡 Quadratic curves are used in TrueType fonts. They are simple, but they can only bend in **one** direction — they can never make an S.

---

## 34.4 Cubic curves: four points

📖 **New word: cubic** — with **four** control points P0, P1, P2, P3. Same idea, one more level:

1. Three lerps along the three sides: **q0** = lerp(P0, P1, t), **q1** = lerp(P1, P2, t), **q2** = lerp(P2, P3, t)
2. Two lerps between those: **r0** = lerp(q0, q1, t), **r1** = lerp(q1, q2, t)
3. One last lerp: **point** = lerp(r0, r1, t)

📖 **New word: de Casteljau's method** — this "lerp between neighbours until only one point is left" recipe. 4 points → 3 → 2 → 1.

Look at step 2 and 3: they are exactly a **quadratic** curve with control points q0, q1, q2. So our code can say:

```cpp
inline PointF cubicPoint(PointF p0, PointF p1, PointF p2, PointF p3, double t) {
    PointF a = lerpPoint(p0, p1, t);
    PointF b = lerpPoint(p1, p2, t);
    PointF c = lerpPoint(p2, p3, t);
    return quadraticPoint(a, b, c, t);
}
```

### Seeing it: `steps.ppm`

`steps.ppm` shows every step at **t = 0.4** for the control points P0 = (40, 260), P1 = (80, 40), P2 = (300, 30), P3 = (360, 250): the grey control polygon, the three **green** points and their two lines, the two **blue** points and their line, the **red** point on the black curve.

🔢 **Maths: the steps at t = 0.4**

> q0 = (40, 260) + ((80, 40) − (40, 260)) × 0.4 = (40 + 16, 260 − 88) = **(56, 172)**
> q1 = (80, 40) + (220, −10) × 0.4 = **(168, 36)**
> q2 = (300, 30) + (60, 220) × 0.4 = **(324, 118)**
> r0 = (56, 172) + (112, −136) × 0.4 = **(100.8, 117.6)**
> r1 = (168, 36) + (156, 82) × 0.4 = **(230.4, 68.8)**
> point = (100.8, 117.6) + (129.6, −48.8) × 0.4 = **(152.64, 98.08)**

The red dot sits exactly on the black curve, and the blue line r0–r1 just **touches** the curve there (Section 34.7).

💡 Cubic curves are the ones in drawing programs, PDF and SVG files, and most fonts. With two handles they can make arches, S-shapes, and even loops.

---

## 34.5 The formula, and the 1–3–3–1 pattern

De Casteljau's method is easy to understand. But we can also **expand** all those lerps into one formula. Write u = 1 − t (so lerp(A, B, t) = u × A + t × B).

For a **quadratic**:

> a = u P0 + t P1, b = u P1 + t P2
> point = u a + t b = u (u P0 + t P1) + t (u P1 + t P2)
> = **u² P0 + 2 u t P1 + t² P2**

For a **cubic**, one more level gives:

> **point = u³ P0 + 3 u² t P1 + 3 u t² P2 + t³ P3**

The numbers in front — **1, 2, 1** for quadratic and **1, 3, 3, 1** for cubic — are rows of **Pascal's triangle**:

```
          1   1          (a line: u, t)
        1   2   1        (quadratic)
      1   3   3   1      (cubic)
```

(Each number is the sum of the two above it. They count how many different "paths" through the lerps lead to each control point.)

### The weights always add up to 1

The four numbers u³, 3u²t, 3ut², t³ are **weights**: how much each control point counts. They are never negative (for t from 0 to 1), and they always add up to **1**, because they are what you get when you multiply out (u + t)³, and u + t = 1:

> (u + t)³ = u³ + 3u²t + 3ut² + t³ = 1³ = 1

So a point on a Bézier curve is a **weighted mix** of the control points — like mixing colours (Chapter 14), or like the barycentric weights of a triangle (Chapter 26).

🔢 **Maths: the cubic (0, 0), (0, 100), (100, 100), (100, 0) at t = 0.5**

> u = t = 0.5: weights 0.125, 0.375, 0.375, 0.125 (that is 1/8, 3/8, 3/8, 1/8)
> x = 0.125 × 0 + 0.375 × 0 + 0.375 × 100 + 0.125 × 100 = 37.5 + 12.5 = **50**
> y = 0.125 × 0 + 0.375 × 100 + 0.375 × 100 + 0.125 × 0 = **75**

🔢 **Maths: at t = 0.25**

> u = 0.75: weights 0.421875, 0.421875, 0.140625, 0.015625
> x = 0.140625 × 100 + 0.015625 × 100 = **15.625**
> y = 0.421875 × 100 + 0.140625 × 100 = **56.25**

The program computes both ways and gets the same answers:

```
cubic at t = 0.25: (15.625, 56.25), formula (15.625, 56.25)
cubic at t = 0.5: (50, 75), formula (50, 75)
cubic at t = 0.75: (84.375, 56.25), formula (84.375, 56.25)
```

(The curve is symmetric, so t = 0.75 is the mirror image of t = 0.25.)

---

## 34.6 Four useful facts

**1. It starts at P0 and ends at P3.** At t = 0 the weights are 1, 0, 0, 0; at t = 1 they are 0, 0, 0, 1. The curve passes **exactly** through its end points, and (usually) not through its handles.

**2. It leaves P0 heading toward P1, and arrives at P3 coming from P2.** (Section 34.7 proves it.) So the handles set the **direction** at each end — that is what a designer drags in a drawing program.

**3. It never goes outside the rubber band.**

📖 **New word: convex hull** — stretch a rubber band around the control points and let it snap tight. The shape inside is the convex hull.

Because every point of the curve is a mix of the control points with weights that are never negative and add up to 1, it can never go outside their convex hull. That is handy: the **box** around the control points is always a box around the curve (Chapter 33 used boxes to decide which pixels to visit).

**4. To transform the curve, transform the control points.** Moving, turning, scaling and skewing (Chapters 31–32) all keep lerps working: transforming a lerped point gives the same answer as lerping the transformed points, M × (A + (B − A) t) = M × A + (M × B − M × A) t. So the transformed curve is the Bézier curve of the transformed control points. To turn a letter, turn its few control points — not thousands of curve points. (This is only true for the transformations of Chapters 31–33. The perspective of Part 9 needs more care.)

---

## 34.7 The direction of the curve

📖 **New word: tangent** — the direction the curve is going at a point. If the curve were a road, it is the way your car points.

How fast does the point move as t grows? For a cubic, the answer (it comes from a branch of maths called **calculus**, which we will not need) is:

> **direction(t) = 3u² (P1 − P0) + 6ut (P2 − P1) + 3t² (P3 − P2)**

Look at its shape: it is a mix of the three **sides** of the control polygon, with weights 3u², 6ut, 3t².

- At t = 0 (u = 1): direction = **3 (P1 − P0)** — pointing from P0 toward P1 (fact 2) ✓
- At t = 1 (u = 0): direction = **3 (P3 − P2)** — pointing from P2 toward P3 ✓

🔢 **Maths: the curve (0, 0), (0, 100), (100, 100), (100, 0)**

> t = 0: 3 × ((0, 100) − (0, 0)) = **(0, 300)** — straight down, toward P1
> t = 0.5: 0.75 × (0, 100) + 1.5 × (100, 0) + 0.75 × (0, −100) = **(150, 0)** — level, at the bottom of the arch

The program prints `tangent at t = 0: (0, 300)` and `tangent at t = 0.5: (150, 0)`. Only the **direction** matters for drawing; `normalize` (Chapter 29) gives it length 1. (The tangent's perpendicular is how you would draw a thick Bézier "ribbon" or place arrows along a curve.)

💡 There is a nice picture of this in `steps.ppm`: the blue line r0–r1 **is** the tangent at t = 0.4. The curve point is on that line, and the curve just touches it.

---

## 34.8 Drawing a curve: flattening

📖 **New word: flattening** — turning a curve into many short straight lines.

Our drawing tools draw straight lines and polygons. So we pick n + 1 values of t — 0, 1/n, 2/n, …, 1 — compute the points, and join them with Wu lines (Chapter 28). If the pieces are short enough, nobody can see the corners.

### How many pieces?

Too few, and the corners show. Too many wastes time. A good rule:

- The curve is **never longer** than its control polygon (the rubber band again: going around the handles is the long way).
- So if we use **controlLength / 4** pieces, each piece of the curve is **at most** about 4 pixels long — so short that the straight line and the curve differ by much less than a pixel.

> **segments = ceil((|P0P1| + |P1P2| + |P2P3|) / 4)**, at least 1

🔢 **Maths: the curve (0, 0), (0, 100), (100, 100), (100, 0)**

> control length = 100 + 100 + 100 = 300 → 300 / 4 = **75 segments** → **76 points** (75 pieces need 76 points: one more than the pieces, like fence posts)

The program prints `points used for this curve: 76`.

### Building long paths

Many curves are joined end to end (a letter, a heart, a path). Our `appendCubic` **adds** a curve's points to a list. It only adds the start point if the list is empty: otherwise the start of this curve is the end of the last one, which is already there. So several `appendCubic` calls build one long path with no repeated points.

---

## 34.9 A gallery of cubics

`curves.ppm` shows four cubic curves, each with its handles drawn as grey lines from the end points (black dots) to the handles (orange dots):

| panel | handles | shape |
|---|---|---|
| 1 | one pulls up, the other pulls down | an **S** — the curve bends one way, then the other |
| 2 | both pull up, near the ends | an **arch**, like a bridge |
| 3 | the handles **cross** (the left handle is far right, the right handle far left) | a **loop** — the curve crosses itself |
| 4 | both handles at the **same** point | a tall, round-topped **peak** |

Try moving the handles in the program and look again. This is the best way to get a feeling for Bézier curves.

---

## 34.10 Filling curved shapes

A closed shape made of Bézier curves is, after flattening, just a polygon with many corners — and Chapter 25's scanline fill (in its smooth Chapter 27 form, `fillPolygonAA`) fills any polygon.

`heart.ppm` is two cubic curves:

```
   left half:   from the bottom tip (150, 260), handles (40, 180) and (50, 40), to the top dip (150, 95)
   right half:  from the top dip (150, 95),  handles (250, 40) and (260, 180), to the bottom tip (150, 260)
```

The right half is the mirror image of the left half across the line x = 150 (each x becomes 300 − x), and runs in the opposite direction so the outline goes round in one loop. Both curves are appended to one list, and `fillPolygonAA` fills it.

💡 This is how letters are drawn: each letter in a font is a few closed paths of Bézier curves (with holes as extra paths, like the inside of an O — Chapter 25's `fillPaths`). A good-looking letter is just well-placed control points.

---

## 34.11 Joining curves smoothly

📖 **New word: smooth join** — two curves meet without a corner.

At a joint, curve 1 arrives coming from its last handle, and curve 2 leaves heading toward its first handle (fact 2). The join is smooth exactly when those two directions are the **same**: when the last handle of curve 1, the joint, and the first handle of curve 2 lie on **one straight line**, with the joint between them.

```
   corner:                       smooth:
     handle                         handle ●
         ●                                  ╲
          ╲   ● handle                       ● joint
           ● joint                            ╲
                                               ● handle
```

### A smooth path through any points

Suppose we want a smooth path through the stops S0, S1, S2, …. Each pair of neighbouring stops gets one cubic. The question is: where do the handles go?

A popular answer (it is called a **Catmull–Rom spline**, after two computer scientists) is: at each stop, make the path go **parallel to the line from the previous stop to the next stop**:

> from S(i) to S(i+1):
> **handle 1 = S(i) + (S(i+1) − S(i−1)) / 6**
> **handle 2 = S(i+1) − (S(i+2) − S(i)) / 6**

At stop S(i+1), the curve that arrives has its handle 2 at S(i+1) − (S(i+2) − S(i)) / 6, and the curve that leaves has its handle 1 at S(i+1) + (S(i+2) − S(i)) / 6. Those two handles are on opposite sides of the stop, along the **same** direction (S(i+2) − S(i)) — exactly the smooth-join rule ✓.

At the two ends there is no "previous" or "next" stop, so we use the end stop itself in its place.

`path.ppm` shows six stops (black dots), joined by straight grey lines, and the smooth red Catmull–Rom path through them.

💡 Why divide by 6? It makes the path move through each stop at the same speed it would have if the stops were evenly spaced on a straight line. Try 3 (a loopier path) or 12 (a tighter, more cornery one).

---

## 34.12 A circle made of four curves

Can a Bézier curve make a circle? Not **exactly** — a circle needs sines and cosines, and a Bézier curve is only made of t, t², t³. But it can come amazingly close. Use four cubics, one for each quarter.

For the quarter from (r, 0) to (0, r) (centre at (0, 0)): the curve must leave (r, 0) going straight down, and arrive at (0, r) going straight left (fact 2). So the handles are:

> P0 = (r, 0), **P1 = (r, k r)**, **P2 = (k r, r)**, P3 = (0, r)

for some number k. Which k? Make the **middle** of the curve (t = 0.5) land exactly on the circle. The 45° point of the circle is (0.70711 r, 0.70711 r) (Chapter 30). With the weights 1/8, 3/8, 3/8, 1/8:

> x at t = 0.5 = (1/8) r + (3/8) r + (3/8) k r + (1/8) × 0 = r × (4 + 3k) / 8
> we want: (4 + 3k) / 8 = 0.70711
> 4 + 3k = 5.65685 → 3k = 1.65685 → **k ≈ 0.55228**

(The exact value is k = 4(√2 − 1) / 3 = 0.5522847…)

How good is it? The program builds a Bézier circle of radius 100 and measures every point's distance from the centre:

```
Bezier circle of radius 100: 177 points, largest error 0.0272076 pixels
```

At most **0.027 pixels** off — less than a thirtieth of a pixel. Nobody can see that. Drawing programs and PDF files draw almost all their circles this way. (177 points: 44 pieces per quarter × 4 quarters = 176 pieces, plus the first point.) `path.ppm` has a small blue Bézier circle in its top-left corner.

---

## Code, part 1: `bezier.h`

File: `common/bezier.h` (new). It includes `combine.h`.

```cpp
#ifndef BEZIER_H
#define BEZIER_H

#include <algorithm>
#include <cmath>
#include <vector>
#include "combine.h"

inline PointF lerpPoint(PointF a, PointF b, double t) {
    return a + (b - a) * t;
}

inline PointF quadraticPoint(PointF p0, PointF p1, PointF p2, double t) {
    PointF a = lerpPoint(p0, p1, t);
    PointF b = lerpPoint(p1, p2, t);
    return lerpPoint(a, b, t);
}

inline PointF cubicPoint(PointF p0, PointF p1, PointF p2, PointF p3, double t) {
    PointF a = lerpPoint(p0, p1, t);
    PointF b = lerpPoint(p1, p2, t);
    PointF c = lerpPoint(p2, p3, t);
    return quadraticPoint(a, b, c, t);
}

inline PointF cubicPointFormula(PointF p0, PointF p1, PointF p2, PointF p3, double t) {
    double u = 1.0 - t;
    return p0 * (u * u * u) + p1 * (3.0 * u * u * t) + p2 * (3.0 * u * t * t) + p3 * (t * t * t);
}

inline Vec2 cubicTangent(PointF p0, PointF p1, PointF p2, PointF p3, double t) {
    double u = 1.0 - t;
    return (p1 - p0) * (3.0 * u * u) + (p2 - p1) * (6.0 * u * t) + (p3 - p2) * (3.0 * t * t);
}

inline int segmentsFor(double controlLength) {
    return std::max(1, static_cast<int>(std::ceil(controlLength / 4.0)));
}

inline void appendQuadratic(std::vector<PointF>& path, PointF p0, PointF p1, PointF p2) {
    int n = segmentsFor(distance(p0, p1) + distance(p1, p2));
    if (path.empty()) {
        path.push_back(p0);
    }
    for (int i = 1; i <= n; ++i) {
        path.push_back(quadraticPoint(p0, p1, p2, static_cast<double>(i) / n));
    }
}

inline void appendCubic(std::vector<PointF>& path, PointF p0, PointF p1, PointF p2, PointF p3) {
    int n = segmentsFor(distance(p0, p1) + distance(p1, p2) + distance(p2, p3));
    if (path.empty()) {
        path.push_back(p0);
    }
    for (int i = 1; i <= n; ++i) {
        path.push_back(cubicPoint(p0, p1, p2, p3, static_cast<double>(i) / n));
    }
}

inline void drawCubic(Image& image, PointF p0, PointF p1, PointF p2, PointF p3, Colour c) {
    std::vector<PointF> path;
    appendCubic(path, p0, p1, p2, p3);
    drawPolylineWu(image, path, c);
}

inline std::vector<PointF> smoothPath(const std::vector<PointF>& points) {
    std::vector<PointF> path;
    int n = static_cast<int>(points.size());
    if (n < 2) {
        return points;
    }
    for (int i = 0; i + 1 < n; ++i) {
        PointF before = points[std::max(i - 1, 0)];
        PointF from = points[i];
        PointF to = points[i + 1];
        PointF after = points[std::min(i + 2, n - 1)];
        PointF handle1 = from + (to - before) / 6.0;
        PointF handle2 = to - (after - from) / 6.0;
        appendCubic(path, from, handle1, handle2, to);
    }
    return path;
}

inline std::vector<PointF> bezierCircle(PointF centre, double r) {
    const double k = 0.5522847498;
    double h = k * r;
    PointF right = centre + Vec2{r, 0.0};
    PointF bottom = centre + Vec2{0.0, r};
    PointF left = centre + Vec2{-r, 0.0};
    PointF top = centre + Vec2{0.0, -r};
    std::vector<PointF> path;
    appendCubic(path, right, right + Vec2{0.0, h}, bottom + Vec2{h, 0.0}, bottom);
    appendCubic(path, bottom, bottom + Vec2{-h, 0.0}, left + Vec2{0.0, h}, left);
    appendCubic(path, left, left + Vec2{0.0, -h}, top + Vec2{-h, 0.0}, top);
    appendCubic(path, top, top + Vec2{h, 0.0}, right + Vec2{0.0, -h}, right);
    return path;
}

#endif
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef BEZIER_H` / `#define BEZIER_H` | Include guard. |
| 4–7 | `#include <algorithm>` / `<cmath>` / `<vector>` / `"combine.h"` | `std::max` and `std::min`; `std::ceil`; lists of points; and everything from Parts 4 and 5. |
| 9–11 | `inline PointF lerpPoint(PointF a, PointF b, double t) { return a + (b - a) * t; }` | Slide from a to b (Section 34.2). Written with the vector operators of Chapter 29. |
| 13–17 | `inline PointF quadraticPoint(PointF p0, PointF p1, PointF p2, double t) { PointF a = ...; PointF b = ...; return lerpPoint(a, b, t); }` | A quadratic curve by de Casteljau: two lerps, then one (Section 34.3). |
| 19–24 | `inline PointF cubicPoint(...) { PointF a = lerpPoint(p0, p1, t); PointF b = ...; PointF c = ...; return quadraticPoint(a, b, c, t); }` | A cubic: three lerps, and the rest is a quadratic (Section 34.4). |
| 26–29 | `inline PointF cubicPointFormula(...) { double u = 1.0 - t; return p0 * (u * u * u) + p1 * (3.0 * u * u * t) + p2 * (3.0 * u * t * t) + p3 * (t * t * t); }` | The same point with the 1–3–3–1 formula (Section 34.5). |
| 31–34 | `inline Vec2 cubicTangent(...) { double u = 1.0 - t; return (p1 - p0) * (3.0 * u * u) + (p2 - p1) * (6.0 * u * t) + (p3 - p2) * (3.0 * t * t); }` | The direction of the curve at t (Section 34.7). It returns a `Vec2`, a direction, not a place. |
| 36–38 | `inline int segmentsFor(double controlLength) { return std::max(1, static_cast<int>(std::ceil(controlLength / 4.0))); }` | How many pieces: control length / 4, rounded up, and never fewer than 1 (Section 34.8). |
| 40–41 | `inline void appendQuadratic(std::vector<PointF>& path, PointF p0, PointF p1, PointF p2) { int n = segmentsFor(distance(p0, p1) + distance(p1, p2));` | Add a flattened quadratic curve to `path` (passed by reference, so we add to the caller's list). |
| 42–44 | `if (path.empty()) { path.push_back(p0); }` | Only the very first curve adds its start point; later curves start where the last one ended. |
| 45–48 | `for (int i = 1; i <= n; ++i) { path.push_back(quadraticPoint(p0, p1, p2, static_cast<double>(i) / n)); } }` | t = 1/n, 2/n, …, 1. The `static_cast<double>` stops `i / n` from being an integer division (which would be 0 until i = n). |
| 50–58 | `inline void appendCubic(...)` | The same for a cubic, with three sides in the control length. |
| 60–64 | `inline void drawCubic(Image& image, ..., Colour c) { std::vector<PointF> path; appendCubic(path, p0, p1, p2, p3); drawPolylineWu(image, path, c); }` | Flatten one cubic and draw it smoothly (Chapter 28). |
| 66 | `inline std::vector<PointF> smoothPath(const std::vector<PointF>& points) {` | A smooth Catmull–Rom path through the stops (Section 34.11). |
| 67–71 | `std::vector<PointF> path; int n = static_cast<int>(points.size()); if (n < 2) { return points; }` | With 0 or 1 stops there is nothing to join: hand them back as they are. (`size()` is an unsigned number; we turn it into an `int` so `i - 1` below can safely be −1.) |
| 72 | `for (int i = 0; i + 1 < n; ++i) {` | One cubic from stop i to stop i + 1. |
| 73 | `PointF before = points[std::max(i - 1, 0)];` | The previous stop — or this stop itself at the start. |
| 74–75 | `PointF from = points[i];` / `PointF to = points[i + 1];` | The two stops this curve joins. |
| 76 | `PointF after = points[std::min(i + 2, n - 1)];` | The stop after `to` — or `to` itself at the end. |
| 77–78 | `PointF handle1 = from + (to - before) / 6.0;` / `PointF handle2 = to - (after - from) / 6.0;` | The Catmull–Rom handles. |
| 79–82 | `appendCubic(path, from, handle1, handle2, to);` `}` `return path;` `}` | Add each curve to the one long path. |
| 84 | `inline std::vector<PointF> bezierCircle(PointF centre, double r) {` | A circle from four cubics (Section 34.12). |
| 85–86 | `const double k = 0.5522847498;` / `double h = k * r;` | The magic number, and the handle length for this radius. |
| 87–90 | `PointF right = centre + Vec2{r, 0.0};` … `PointF top = ...` | The four points where the quarters meet. |
| 91 | `std::vector<PointF> path;` | The whole circle goes into one list. |
| 92 | `appendCubic(path, right, right + Vec2{0.0, h}, bottom + Vec2{h, 0.0}, bottom);` | Right → bottom: leave going down, arrive going left. |
| 93–95 | the other three `appendCubic` calls | Bottom → left, left → top, top → right, each with its handles along the circle's direction at its ends. The last one ends at `right`, closing the circle. |
| 96–97 | `return path;` `}` | Done. |
| 99 | `#endif` | End of the include guard. |

---

## Code, part 2: steps, curves, a heart and a path

File: `ch34/bezier.cpp`

```cpp
#include <cmath>
#include <iostream>
#include <vector>
#include "bezier.h"

void printPoint(const char* label, PointF p) {
    std::cout << label << " (" << p.x << ", " << p.y << ")\n";
}

void drawDot(Image& image, PointF p, double r, Colour c) {
    fillCircleAA(image, p.x, p.y, r, c);
}

void drawHandles(Image& image, PointF p0, PointF p1, PointF p2, PointF p3) {
    Colour grey{170, 170, 180};
    drawLineWu(image, p0, p1, grey);
    drawLineWu(image, p2, p3, grey);
    drawDot(image, p0, 3.0, colours::black);
    drawDot(image, p3, 3.0, colours::black);
    drawDot(image, p1, 3.0, Colour{230, 120, 0});
    drawDot(image, p2, 3.0, Colour{230, 120, 0});
}

int main() {
    printPoint("quadratic (0, 0), (50, 100), (100, 0) at t = 0.5:",
               quadraticPoint(PointF{0.0, 0.0}, PointF{50.0, 100.0}, PointF{100.0, 0.0}, 0.5));
    PointF a{0.0, 0.0};
    PointF b{0.0, 100.0};
    PointF c{100.0, 100.0};
    PointF d{100.0, 0.0};
    const double times[3] = {0.25, 0.5, 0.75};
    for (double t : times) {
        PointF p = cubicPoint(a, b, c, d, t);
        PointF q = cubicPointFormula(a, b, c, d, t);
        std::cout << "cubic at t = " << t << ": (" << p.x << ", " << p.y << "), formula ("
                  << q.x << ", " << q.y << ")\n";
    }
    printPoint("tangent at t = 0:", cubicTangent(a, b, c, d, 0.0));
    printPoint("tangent at t = 0.5:", cubicTangent(a, b, c, d, 0.5));
    std::vector<PointF> counted;
    appendCubic(counted, a, b, c, d);
    std::cout << "points used for this curve: " << counted.size() << "\n";

    std::vector<PointF> ring = bezierCircle(PointF{0.0, 0.0}, 100.0);
    double worst = 0.0;
    for (PointF p : ring) {
        worst = std::max(worst, std::fabs(length(p) - 100.0));
    }
    std::cout << "Bezier circle of radius 100: " << ring.size() << " points, largest error "
              << worst << " pixels\n";

    Image steps(400, 300, colours::white);
    PointF p0{40.0, 260.0};
    PointF p1{80.0, 40.0};
    PointF p2{300.0, 30.0};
    PointF p3{360.0, 250.0};
    double t = 0.4;
    PointF q0 = lerpPoint(p0, p1, t);
    PointF q1 = lerpPoint(p1, p2, t);
    PointF q2 = lerpPoint(p2, p3, t);
    PointF r0 = lerpPoint(q0, q1, t);
    PointF r1 = lerpPoint(q1, q2, t);
    PointF s = lerpPoint(r0, r1, t);
    drawPolylineWu(steps, {p0, p1, p2, p3}, Colour{170, 170, 180});
    drawPolylineWu(steps, {q0, q1, q2}, Colour{80, 160, 80});
    drawLineWu(steps, r0, r1, Colour{60, 90, 220});
    drawCubic(steps, p0, p1, p2, p3, colours::black);
    for (PointF p : {p0, p1, p2, p3}) {
        drawDot(steps, p, 4.0, Colour{120, 120, 130});
    }
    for (PointF p : {q0, q1, q2}) {
        drawDot(steps, p, 4.0, Colour{80, 160, 80});
    }
    drawDot(steps, r0, 4.0, Colour{60, 90, 220});
    drawDot(steps, r1, 4.0, Colour{60, 90, 220});
    drawDot(steps, s, 5.0, colours::red);

    Image curves(800, 200, colours::white);
    const PointF shapes[4][4] = {
        {PointF{20.0, 160.0}, PointF{80.0, 20.0}, PointF{120.0, 180.0}, PointF{180.0, 40.0}},
        {PointF{220.0, 170.0}, PointF{230.0, 20.0}, PointF{370.0, 20.0}, PointF{380.0, 170.0}},
        {PointF{420.0, 170.0}, PointF{600.0, 30.0}, PointF{400.0, 30.0}, PointF{580.0, 170.0}},
        {PointF{620.0, 170.0}, PointF{700.0, 20.0}, PointF{700.0, 20.0}, PointF{780.0, 170.0}}};
    for (int i = 0; i < 4; ++i) {
        drawHandles(curves, shapes[i][0], shapes[i][1], shapes[i][2], shapes[i][3]);
        drawCubic(curves, shapes[i][0], shapes[i][1], shapes[i][2], shapes[i][3],
                  Colour{30, 60, 200});
    }

    Image heart(300, 300, Colour{255, 240, 245});
    std::vector<PointF> outline;
    appendCubic(outline, PointF{150.0, 260.0}, PointF{40.0, 180.0}, PointF{50.0, 40.0},
                PointF{150.0, 95.0});
    appendCubic(outline, PointF{150.0, 95.0}, PointF{250.0, 40.0}, PointF{260.0, 180.0},
                PointF{150.0, 260.0});
    fillPolygonAA(heart, outline, Colour{220, 30, 70});

    Image path(500, 300, colours::white);
    std::vector<PointF> stops = {PointF{30.0, 250.0}, PointF{110.0, 80.0}, PointF{200.0, 200.0},
                                 PointF{280.0, 60.0}, PointF{380.0, 220.0}, PointF{470.0, 90.0}};
    drawPolylineWu(path, stops, Colour{200, 200, 210});
    drawPolylineWu(path, smoothPath(stops), Colour{200, 40, 40});
    for (PointF p : stops) {
        drawDot(path, p, 4.0, colours::black);
    }
    std::vector<PointF> circle = bezierCircle(PointF{50.0, 50.0}, 35.0);
    drawPolylineWu(path, circle, Colour{30, 60, 200});

    bool ok = steps.savePPM("steps.ppm");
    ok = ok && curves.savePPM("curves.ppm");
    ok = ok && heart.savePPM("heart.ppm");
    ok = ok && path.savePPM("path.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
```

Build and run (from the `code/ch34` folder):

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common bezier.cpp -o bezier
./bezier
```

### Line by line

**Helpers (lines 1–22)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–4 | the `#include` lines | `std::fabs`, printing, lists, and the new header. |
| 6–8 | `void printPoint(const char* label, PointF p) { ... }` | Print a label and a point (as in Chapter 31). |
| 10–12 | `void drawDot(Image& image, PointF p, double r, Colour c) { fillCircleAA(image, p.x, p.y, r, c); }` | A smooth dot at a point — shorter to write than `fillCircleAA` with `p.x, p.y`. |
| 14 | `void drawHandles(Image& image, PointF p0, PointF p1, PointF p2, PointF p3) {` | Draw a cubic's handles, the way drawing programs show them. |
| 15–17 | `Colour grey{170, 170, 180};` / `drawLineWu(image, p0, p1, grey);` / `drawLineWu(image, p2, p3, grey);` | A grey line from each end point to its handle. |
| 18–22 | four `drawDot` calls, `}` | Black dots on the end points, orange dots on the handles. |

**The numbers (lines 24–50)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 25–26 | `printPoint("quadratic ...", quadraticPoint(PointF{0.0, 0.0}, PointF{50.0, 100.0}, PointF{100.0, 0.0}, 0.5));` | Section 34.3. |
| 27–30 | `PointF a{0.0, 0.0};` … `PointF d{100.0, 0.0};` | An arch-shaped cubic for the next tests. |
| 31–37 | `const double times[3] = {0.25, 0.5, 0.75}; for (double t : times) { PointF p = cubicPoint(...); PointF q = cubicPointFormula(...); std::cout << ...; }` | De Casteljau and the formula give the same points (Section 34.5). |
| 38–39 | two `printPoint` calls with `cubicTangent` | The directions at t = 0 and t = 0.5 (Section 34.7). (`printPoint` takes a `PointF`; a `Vec2` is the same type, Chapter 29.) |
| 40–42 | `std::vector<PointF> counted; appendCubic(counted, a, b, c, d); std::cout << ... counted.size() ...` | How many points the flattening uses (Section 34.8). |
| 44 | `std::vector<PointF> ring = bezierCircle(PointF{0.0, 0.0}, 100.0);` | A Bézier circle around (0, 0), radius 100. |
| 45–48 | `double worst = 0.0; for (PointF p : ring) { worst = std::max(worst, std::fabs(length(p) - 100.0)); }` | Each point's distance from the centre is `length(p)`; how far is that from 100? Keep the biggest difference. |
| 49–50 | `std::cout << "Bezier circle of radius 100: " << ring.size() << ...` | Print the count and the worst error (Section 34.12). (Plain "Bezier", because the é might not print well in every terminal.) |

**The steps picture (lines 52–76)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 52–56 | `Image steps(400, 300, colours::white);` and `p0` … `p3` | A white picture and four control points. |
| 57–63 | `double t = 0.4;` … `PointF s = lerpPoint(r0, r1, t);` | De Casteljau by hand, keeping every middle point so we can draw it (Section 34.4). |
| 64 | `drawPolylineWu(steps, {p0, p1, p2, p3}, Colour{170, 170, 180});` | The grey control polygon. `{p0, p1, p2, p3}` makes a `std::vector<PointF>` on the spot. |
| 65–66 | `drawPolylineWu(steps, {q0, q1, q2}, ...);` / `drawLineWu(steps, r0, r1, ...);` | The green lines (level 1) and the blue line (level 2). |
| 67 | `drawCubic(steps, p0, p1, p2, p3, colours::black);` | The curve itself. |
| 68–76 | `for (PointF p : {p0, p1, p2, p3}) { drawDot(...); }` … `drawDot(steps, s, 5.0, colours::red);` | Dots on all the points, drawn last so they sit on top. A `for` loop can walk through a `{...}` list directly. |

**The gallery (lines 78–88)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 78 | `Image curves(800, 200, colours::white);` | A wide picture with room for four curves. |
| 79–83 | `const PointF shapes[4][4] = {...};` | Four curves, four control points each: an S, an arch, a loop and a peak (Section 34.9). |
| 84–88 | `for (int i = 0; i < 4; ++i) { drawHandles(...); drawCubic(..., Colour{30, 60, 200}); }` | Handles first, then the blue curve on top. |

**The heart (lines 90–96)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 90–91 | `Image heart(300, 300, Colour{255, 240, 245});` / `std::vector<PointF> outline;` | A pale pink picture and an empty outline. |
| 92–95 | two `appendCubic` calls | The left half (up from the tip), then the right half (back down to the tip) — one closed loop (Section 34.10). |
| 96 | `fillPolygonAA(heart, outline, Colour{220, 30, 70});` | Fill it smoothly in red. |

**The smooth path (lines 98–107)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 98–100 | `Image path(500, 300, colours::white);` / `std::vector<PointF> stops = {...};` | Six stops that zigzag across the picture. |
| 101 | `drawPolylineWu(path, stops, Colour{200, 200, 210});` | The stops joined by straight lines, in light grey — for comparison. |
| 102 | `drawPolylineWu(path, smoothPath(stops), Colour{200, 40, 40});` | The smooth red Catmull–Rom path (Section 34.11). |
| 103–105 | `for (PointF p : stops) { drawDot(path, p, 4.0, colours::black); }` | Black dots on the stops: the red path goes through every one. |
| 106–107 | `std::vector<PointF> circle = bezierCircle(PointF{50.0, 50.0}, 35.0);` / `drawPolylineWu(...)` | A small blue Bézier circle in the top-left corner. |

**Saving (lines 109–118)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 109–112 | `bool ok = steps.savePPM("steps.ppm");` … | Save the four pictures. |
| 113–118 | `if (!ok) { ... }` `return 0;` `}` | Report a problem, or finish. |

### What you should see

```
quadratic (0, 0), (50, 100), (100, 0) at t = 0.5: (50, 50)
cubic at t = 0.25: (15.625, 56.25), formula (15.625, 56.25)
cubic at t = 0.5: (50, 75), formula (50, 75)
cubic at t = 0.75: (84.375, 56.25), formula (84.375, 56.25)
tangent at t = 0: (0, 300)
tangent at t = 0.5: (150, 0)
points used for this curve: 76
Bezier circle of radius 100: 177 points, largest error 0.0272076 pixels
```

Open the pictures:
- `steps.ppm`: a black curve with its grey control polygon, the green and blue construction lines for t = 0.4, and a red dot on the curve where the blue line touches it.
- `curves.ppm`: four blue curves with grey handle lines: an S, an arch, a loop, and a round-topped peak.
- `heart.ppm`: a smooth red heart on pale pink.
- `path.ppm`: a grey zigzag, the smooth red path through the same six stops, and a small blue circle.

---

## Small examples

### Example 1 — A quadratic by hand

P0 = (0, 0), P1 = (100, 0), P2 = (100, 100), t = 0.5:

> a = (50, 0), b = (100, 50), point = **(75, 25)**
> With the formula: 0.25 × (0, 0) + 0.5 × (100, 0) + 0.25 × (100, 100) = (75, 25) ✓

### Example 2 — A straight "curve"

If all four control points are on one line, evenly spaced — (0, 0), (10, 0), (20, 0), (30, 0) — every lerp stays on that line, and the curve is a straight segment: at t = 0.5 the point is (0 × 1/8 + 10 × 3/8 + 20 × 3/8 + 30 × 1/8, 0) = **(15, 0)**, the middle ✓.

### Example 3 — Handles set the direction

Curve (0, 0), (50, 0), (100, 50), (100, 100). It leaves (0, 0) going **right** (toward (50, 0)) and arrives at (100, 100) going **down** (from (100, 50)) — a smooth quarter-turn, like a road bending.

### Example 4 — Turning a curve

Turn the curve (0, 0), (0, 100), (100, 100), (100, 0) by 90° about (0, 0): its control points become (0, 0), (−100, 0), (−100, 100), (0, 100). The arch that opened upward now opens to the right. And its point at t = 0.5, (50, 75), turned by 90°, gives (−75, 50) — which is exactly the new curve's point at t = 0.5: (0/8 − 300/8 − 300/8 + 0, 0 + 0 + 300/8 + 100/8) = (−75, 50) ✓ (fact 4).

### Example 5 — Pieces for a big curve

Control points (0, 0), (300, 0), (300, 400), (0, 400): control length 300 + 400 + 300 = 1000 → **250** pieces.

---

## Common mistakes

⚠️ **Expecting the curve to go through the handles.** It goes through the **end points** only. The handles pull.

⚠️ **The wrong order of control points.** P0, P1, P2, P3 — ends at the outside, handles in the middle. Swap P1 and P3 and you get a completely different curve.

⚠️ **Integer division for t.** `i / n` with `int`s is 0 until i = n. Use `static_cast<double>(i) / n`.

⚠️ **Too few pieces.** A curve flattened into 5 pieces has visible corners. Use the control length rule.

⚠️ **Repeating joint points.** When appending curves into one path, do not add each curve's start point again (our `appendCubic` takes care of it). A repeated point makes a zero-length edge — harmless for filling, but it can upset code that divides by edge lengths.

⚠️ **Corners at joins.** For a smooth join, the handle before the joint, the joint and the handle after it must be on one straight line.

⚠️ **Thinking a Bézier circle is exact.** It is off by up to 0.027 % of the radius: invisible in a picture, but do not use it to measure things.

---

## Practice

🏋️ **1.** By hand, find the point at t = 0.5 on the quadratic curve (0, 100), (100, 0), (200, 100).

🏋️ **2.** Find the cubic weights u³, 3u²t, 3ut², t³ at t = 0.2 and check that they add up to 1.

🏋️ **3.** Draw a quadratic curve with `appendQuadratic` and `drawPolylineWu`, and draw its control polygon in grey. Move the handle around.

🏋️ **4.** Draw a "wave" of 6 cubic curves joined smoothly, each going from (100i, 100) to (100(i + 1), 100), with handles alternately above and below. Where must the handles be for the joins to be smooth?

🏋️ **5.** Draw the letter **S** as one thick smooth line: two cubics, drawn with many small `fillCapsuleAA` capsules along the flattened path. (Hint: all pieces at once in one `fillPathsAA` call would be better — why do separate capsules look slightly blotchy where they overlap?)

🏋️ **6.** Turn the heart by 20° about its centre (150, 170) using `applyToPoints` and `rotationAbout` (Chapter 33) — on the **control points** before appending, or on the **flattened outline** after. Do both give the same picture?

🏋️ **7.** Change the divide-by-6 in `smoothPath` to a divide-by-3, and to a divide-by-12. Describe the paths.

🏋️ **8.** Use `cubicTangent` to put 10 small arrows (Chapter 29's `drawArrowAA`) along the S curve of `curves.ppm`, each pointing the way the curve goes.

---

## Answers

**1.**
> a = lerp((0, 100), (100, 0), 0.5) = (50, 50); b = lerp((100, 0), (200, 100), 0.5) = (150, 50); point = **(100, 50)** — halfway up toward the handle at y = 0.

**2.**
> u = 0.8: u³ = 0.512, 3u²t = 3 × 0.64 × 0.2 = 0.384, 3ut² = 3 × 0.8 × 0.04 = 0.096, t³ = 0.008
> 0.512 + 0.384 + 0.096 + 0.008 = **1** ✓

**3.**

```cpp
PointF a{50.0, 250.0};
PointF h{200.0, 30.0};
PointF b{350.0, 250.0};
std::vector<PointF> curve;
appendQuadratic(curve, a, h, b);
drawPolylineWu(img, {a, h, b}, Colour{170, 170, 180});
drawPolylineWu(img, curve, colours::black);
```

**4.**

```cpp
std::vector<PointF> wave;
for (int i = 0; i < 6; ++i) {
    double x0 = 100.0 * i;
    double up = (i % 2 == 0) ? -60.0 : 60.0;
    appendCubic(wave, PointF{x0, 100.0}, PointF{x0 + 33.0, 100.0 + up},
                PointF{x0 + 67.0, 100.0 + up}, PointF{x0 + 100.0, 100.0});
}
drawPolylineWu(img, wave, colours::blue);
```

> This wave is already **smooth**. At the joint x = 100, the handle before it is (67, 40) and the handle after it is (133, 160): mirror images of each other through the joint (100, 100), so all three are on one straight line. Because `up` changes sign from one curve to the next, this happens at every joint.
> If you gave every curve the **same** handles (say `up` = −60 every time), the wave would become a row of bumps with a sharp **corner** at each joint: one curve would arrive going down-right and the next would leave going up-right.

**5.**
> Draw each piece of the flattened path with `fillCapsuleAA(img, path[i], path[i + 1], 4.0, col)`. Where two capsules overlap (at every joint), the edge pixels get blended **twice** — the smooth edge is a little darker there, which looks blotchy. One `fillPathsAA` call for the whole outline of the thick line paints each pixel once (Chapter 27's "conflation" problem).

**6.**
> Both give the same picture (up to tiny differences in where the flattening points fall), because of fact 4: transforming the control points transforms the curve. Transforming the 4 + 4 control points is much less work than transforming the whole flattened outline.

**7.**
> Divide by 3: the handles are twice as long, so the path swings wide past each stop and can make little loops when stops are close together. Divide by 12: the handles are short, the path hugs the grey zigzag and turns sharply at the stops, almost like corners.

**8.**

```cpp
PointF s0{20.0, 160.0};
PointF s1{80.0, 20.0};
PointF s2{120.0, 180.0};
PointF s3{180.0, 40.0};
for (int i = 0; i < 10; ++i) {
    double t = (i + 0.5) / 10.0;
    PointF p = cubicPoint(s0, s1, s2, s3, t);
    Vec2 dir = normalize(cubicTangent(s0, s1, s2, s3, t));
    drawArrowAA(curves, p - dir * 6.0, p + dir * 6.0, 2.0, colours::red);
}
```

---

## Summary

🧠 A **Bézier curve** is controlled by a few points. It starts at the first, ends at the last, and is pulled toward the **handles** in between.

🧠 **De Casteljau:** lerp between neighbours, again and again, until one point is left. 3 points → **quadratic**, 4 points → **cubic**.

🧠 Cubic formula: **u³ P0 + 3u²t P1 + 3ut² P2 + t³ P3** (u = 1 − t). The weights (1–3–3–1) add up to 1.

🧠 The curve leaves P0 toward P1 and arrives at P3 from P2. It stays inside the **convex hull**. To transform it, transform the control points.

🧠 Direction: **3u²(P1 − P0) + 6ut(P2 − P1) + 3t²(P3 − P2)**.

🧠 **Flatten** with about (control length / 4) pieces, then draw with Wu lines or fill with `fillPolygonAA`.

🧠 **Smooth joins**: handle, joint, handle on one straight line. **Catmull–Rom**: handles = stop ± (next − previous) / 6.

🧠 A circle ≈ four cubics with handles **0.5523 r** long — off by only 0.027 %.

---

## Next chapter

Until now we have changed **shapes**. In Chapter 35 — the last chapter of Part 5 — we change the size of whole **pictures**: making them bigger and smaller. We will meet **nearest-neighbour** resizing properly (the blocky enlargement of Chapter 33, and the `pasteEnlarged` of Chapter 27), then **bilinear** resizing, which blends the four nearest pixels for a smooth result — the same idea as the inverse mapping of Chapter 33, with a better way of picking the colour.
