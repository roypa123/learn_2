# Chapter 29 — 2D Vectors

> **Part 5 · Chapter 29 of 82**
> **You need:** Chapters 1–28 (especially 3, 20, 24 and 27) · **You will make:** `vec2.h` (vector maths: add, subtract, scale, length, dot, cross, perpendicular, projection, reflection, distances; smooth round-ended lines and arrows), `add.ppm`, `field.ppm`, `bounce.ppm` and `figure.ppm`

---

## What you will learn

- What a **vector** is: an **arrow** — a movement with a direction and a length.
- The difference between a **point** (a place) and a **vector** (a step from one place to another).
- How to **add**, **subtract** and **scale** vectors, and what each one means in a picture.
- The **length** of a vector (Pythagoras again) and **unit vectors**.
- The **dot product**: one number that tells you whether two arrows point the same way, at right angles, or opposite ways.
- The **cross product** in 2D — and why it is exactly the **edge function** of Chapter 24.
- **Perpendicular** vectors, **projection** (the "shadow" of one arrow on another), and **reflection** (how a ball bounces).
- The distance from a point to a **line** and to a **segment**, and how that gives smooth lines with **round ends**.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **vector** | An arrow: a step with a direction and a length, written (x, y). |
| **component** | One of the numbers of a vector: the x-component and the y-component. |
| **scalar** | An ordinary single number (not a vector). |
| **magnitude** | Another word for the length of a vector. |
| **unit vector** | A vector with length exactly 1: a pure direction. |
| **normalise** | Make a vector's length 1, keeping its direction. |
| **dot product** | a·b = a.x·b.x + a.y·b.y: one number that measures how much two vectors point the same way. |
| **cross product** (2D) | a × b = a.x·b.y − a.y·b.x: one number that measures how much b turns away from a. |
| **projection** | The part of one vector that lies along another — its "shadow". |
| **normal** | A vector at a right angle to a surface (a wall, a floor, an edge). |
| **reflection** | Bouncing off a surface, like a ball off a wall or light off a mirror. |
| **segment** | A piece of a line with two ends. |
| **capsule** | The shape of a pill: a thick line with round ends. |
| **vector field** | A picture with an arrow at every point, showing a direction everywhere (like wind on a weather map). |

---

## 29.1 Points and arrows

Since Chapter 3 we have described **places** with two numbers: the point (6, 5) is 6 across and 5 down from the top-left corner.

Now look at a different question: "How do I get **from** (2, 1) **to** (6, 5)?" The answer is a **step**: 4 to the right and 4 down. We write that step as (4, 4) too — but it is not a place. It is an **arrow**.

📖 **New word: vector** — an arrow: a step with a **direction** and a **length**. We write it with two numbers (x, y): how far across and how far down.

📖 **New word: component** — one of the two numbers: (4, 4) has x-component 4 and y-component 4.

```
      (2, 1) ●
              ╲
               ╲   the vector (4, 4):
                ╲  "4 right, 4 down"
                 ↘
                  ● (6, 5)
```

The same arrow can start **anywhere**. The step (4, 4) from (2, 1) goes to (6, 5); from (10, 0) it goes to (14, 4). An arrow does not belong to a place — it only says "which way, and how far".

🔢 **Maths: points and vectors**

> point − point = **vector**: (6, 5) − (2, 1) = (4, 4), the step from the first point to the second
> point + vector = **point**: (2, 1) + (4, 4) = (6, 5), where you arrive
> vector + vector = **vector**: two steps in a row are one bigger step

(Adding two **points** makes no sense: what would "London + Paris" be?)

### One type for both

In code, a point and a vector are both two `double`s. Chapter 24 already has `PointF`. Instead of making a second, almost identical type, we give `PointF` a **second name**:

```cpp
using Vec2 = PointF;
```

`using` makes `Vec2` mean exactly the same type as `PointF`. We write `Vec2` when we mean an arrow and `PointF` when we mean a place — the computer does not care, but it helps the **reader**. Every function from Chapters 24–28 that takes a `PointF` also takes a `Vec2`.

---

## 29.2 Adding, subtracting and scaling

### Adding: one step after another

📖 To add two vectors, add their components:

> **a + b = (a.x + b.x, a.y + b.y)**

In a picture: put the start of b at the **tip** of a ("head to tail"). The sum is the arrow from the start of a to the tip of b.

🔢 **Maths: a = (3, 4), b = (2, −1)**

> a + b = (3 + 2, 4 + (−1)) = **(5, 3)**

Walking 3 right and 4 down, then 2 right and 1 up, takes you 5 right and 3 down in total. ✓

💡 The order does not matter: b + a = (5, 3) too. In `add.ppm`, the blue arrow a and the red arrow b (drawn at a's tip) end at the same place as the green arrow a + b. The grey lines show the other way round (b first, then a): together they make a **parallelogram**, with a + b as its diagonal.

### Subtracting: the step from one tip to another

> **a − b = (a.x − b.x, a.y − b.y)** — the step that takes you from the tip of b to the tip of a

> a − b = (3 − 2, 4 − (−1)) = **(1, 5)**

And the **negative** of a vector, −v = (−v.x, −v.y), is the same arrow turned around.

### Scaling: longer or shorter

📖 **New word: scalar** — an ordinary number (as opposed to a vector). Multiplying a vector by a scalar makes it longer or shorter:

> **s × v = (s × v.x, s × v.y)**

> 2 × (3, 4) = **(6, 8)** — twice as long, same direction
> 0.5 × (3, 4) = (1.5, 2) — half as long
> −1 × (3, 4) = (−3, −4) — same length, opposite direction

### We have used vectors all along

- Lerp (Chapter 13): lerp(A, B, t) = A + t × (B − A) — a point, plus a scaled step.
- Barycentric points (Chapter 26): λ0·A + λ1·B + λ2·C.
- The thick line (Chapter 27): A + (nx, ny) — a point plus a sideways step.

Now we can write these with real `+`, `−` and `*` in C++.

---

## 29.3 Length and unit vectors

📖 **New word: magnitude** — the length of a vector, written |v|. It is Pythagoras (Chapter 3):

> **|v| = √(v.x² + v.y²)**

> |(3, 4)| = √(9 + 16) = √25 = **5**

📖 **New word: unit vector** — a vector with length exactly 1. It is a pure **direction**.

📖 **New word: normalise** — divide a vector by its length, to make a unit vector in the same direction:

> **normalize(v) = v / |v|**
> normalize((3, 4)) = (3/5, 4/5) = **(0.6, 0.8)**
> check: √(0.36 + 0.64) = √1 = 1 ✓

⚠️ The vector (0, 0) has length 0 and **no direction**. Dividing by 0 is not allowed, so our `normalize` gives back (0, 0) in that case.

💡 Unit vectors are useful because they separate **direction** from **distance**. "Move 7 pixels toward the target" is: position + 7 × normalize(target − position).

---

## 29.4 The dot product

📖 **New word: dot product** — two vectors in, **one number** out:

> **a · b = a.x × b.x + a.y × b.y**

🔢 **Maths: a = (3, 4), b = (2, −1)**

> a · b = 3 × 2 + 4 × (−1) = 6 − 4 = **2**

What does this number mean? Try it with the arrow "right", (1, 0), and three others:

> (1, 0) · (1, 1) = 1 → **positive**: (1, 1) points partly the same way (right and down)
> (1, 0) · (0, 1) = 0 → **zero**: (0, 1) points straight down, at a **right angle** to "right"
> (1, 0) · (−1, 1) = −1 → **negative**: (−1, 1) points partly **backwards** (left and down)

🧠 **Remember:**

> a · b > 0 → the arrows point **roughly the same way** (the angle between them is less than 90°)
> a · b = 0 → they are **perpendicular** (exactly 90°)
> a · b < 0 → they point **roughly opposite ways** (more than 90°)

### Why does it work? (A look ahead)

The dot product is really:

> a · b = |a| × |b| × cos(angle between them)

where **cos** (cosine) is a number that is 1 for an angle of 0°, 0 for 90°, and −1 for 180°. We meet cosine properly in Chapter 30 — and then this formula will give us a way to **measure** angles. For now, the sign alone is already very useful.

### The dot product of a vector with itself

> v · v = v.x² + v.y² = |v|²

So the length is |v| = √(v · v). Our `length` function is written exactly like that.

---

## 29.5 Perpendicular vectors

📖 A vector **perpendicular** to v (turned by a quarter turn, 90°) is:

> **perpendicular(v) = (−v.y, v.x)** — swap the components, and change the sign of the new first one

In Chapter 27 we used this to build thick lines, and promised a proof. Here it is, with the dot product:

> v · perpendicular(v) = v.x × (−v.y) + v.y × v.x = −v.x·v.y + v.y·v.x = **0** ✓

The dot product is 0 for **every** v, so they are always at a right angle. And the lengths are the same: √((−v.y)² + v.x²) = √(v.x² + v.y²).

🔢 **Maths: v = (3, 4)**

> perpendicular = (−4, 3); dot: 3 × (−4) + 4 × 3 = −12 + 12 = **0** ✓

Which way does it turn? (1, 0) ("right") becomes (0, 1) ("down"). On our screen (y goes down), turning from right to down is **clockwise**. So `perpendicular` turns a quarter turn **clockwise** on the screen. (−perpendicular(v) turns the other way.)

---

## 29.6 The cross product — the edge function again

📖 **New word: cross product** (in 2D) — two vectors in, one number out:

> **a × b = a.x × b.y − a.y × b.x**

> (3, 4) × (2, −1) = 3 × (−1) − 4 × 2 = −3 − 8 = **−11**

Look at the edge function of Chapter 24:

> E(A, B, P) = (B.x − A.x) × (P.y − A.y) − (B.y − A.y) × (P.x − A.x)

With the vectors u = B − A and w = P − A, that is u.x × w.y − u.y × w.x:

> **E(A, B, P) = (B − A) × (P − A)**

The edge function **is** the cross product of "the edge" and "the step to P". Our program checks it with the Chapter 24 example:

```
edgeFunction = 24, cross(B - A, P - A) = 24
```

So everything we learned about the edge function is true for the cross product:

- a × b > 0 → b points to the **right** of a (clockwise on the screen)
- a × b = 0 → a and b are **parallel** (same or opposite direction)
- a × b < 0 → b points to the **left** of a
- |a × b| = the **area** of the parallelogram made by a and b (twice the triangle area)

💡 **Dot and cross are partners.** The dot product measures how much two arrows go **together**; the cross product measures how much one **turns away** from the other. With cosine and sine (Chapter 30): a · b = |a||b|·cos(angle) and a × b = |a||b|·sin(angle).

---

## 29.7 Projection: the shadow of an arrow

📖 **New word: projection** — the part of a vector v that lies **along** another vector d. Imagine the sun shining straight down onto the line of d: the shadow of v on that line is its projection.

```
            v
           ↗
          ╱ │
         ╱  │  (light shines straight down onto d's line)
        ╱   │
   ────●════●─────────→ d
        shadow = projection of v onto d
```

The formula:

> **project(v, d) = d × (v · d) / (d · d)**

(v · d) / (d · d) is a scalar: **how many d's** fit into the shadow.

🔢 **Maths: project v = (4, 0) onto d = (3, 4)**

> v · d = 4 × 3 + 0 × 4 = 12
> d · d = 9 + 16 = 25
> projection = (3, 4) × 12 / 25 = (3, 4) × 0.48 = **(1.44, 1.92)**

Check: (1.44, 1.92) points the same way as (3, 4) (it is 0.48 of it). And what is left over, v − projection = (4 − 1.44, 0 − 1.92) = (2.56, −1.92), should be perpendicular to d:

> (2.56, −1.92) · (3, 4) = 7.68 − 7.68 = **0** ✓

So the projection splits v into two parts: one **along** d, one **across** d.

---

## 29.8 Distances to lines and segments

### Distance to a line

In Chapter 24 we found that |E(A, B, P)| = length of AB × distance from P to the line. With vectors:

> **distance from P to the line AB = |(B − A) × (P − A)| / |B − A|**

🔢 **Maths: P = (4, 0), the line through (0, 0) and (3, 4)** (Chapter 24, Example 4)

> (3, 4) × (4, 0) = 3 × 0 − 4 × 4 = −16 → |−16| = 16
> |(3, 4)| = 5 → distance = 16 / 5 = **3.2** ✓ (the same as Chapter 24)

### The closest point on a segment

📖 **New word: segment** — a piece of a line, from A to B, with ends.

A line goes on forever, but a segment stops at its ends. To find the point Q of the segment closest to P:

1. Project P − A onto the segment: t = (P − A) · (B − A) / ((B − A) · (B − A)). t is "how far along" (0 at A, 1 at B).
2. If t < 0, the closest point is beyond A: use t = 0. If t > 1, it is beyond B: use t = 1. (This is **clamping**, Chapter 14.)
3. Q = A + t × (B − A) — lerp again!

🔢 **Maths: the segment from (0, 0) to (10, 0)**

| P | t = (P − A)·(10, 0) / 100 | clamped | Q | distance |
|---|---|---|---|---|
| (−3, 4) | −30 / 100 = −0.3 | 0 | (0, 0) | √(9 + 16) = **5** |
| (4, 3) | 40 / 100 = 0.4 | 0.4 | (4, 0) | **3** |
| (13, 4) | 130 / 100 = 1.3 | 1 | (10, 0) | √(9 + 16) = **5** |

Our program prints exactly these three lines.

### Smooth lines with round ends

📖 **New word: capsule** — the shape of a pill: all the points within distance r of a segment.

```
      ╭──────────────────╮
     (  A ●─────────● B   )    all points within r of the segment AB
      ╰──────────────────╯
```

With `distanceToSegment`, a capsule is easy: a point is inside when its distance to the segment is ≤ r. That is just like a circle (distance to a **point** ≤ r), so we use the same smooth-edge trick as `fillCircleAA` (Chapter 27): pixels far inside are solid, pixels far outside are skipped, and only pixels within half a diagonal (0.7071) of the edge are sampled.

The round ends make capsules perfect for **joined** lines: where two capsules meet at a point, both have a round end there, so the joint is always smooth — no gaps and no spikes. `figure.ppm` draws a stick figure with five capsules and a circle.

---

## 29.9 Reflection: how a ball bounces

📖 **New word: normal** — a vector at a right angle to a surface. The floor is horizontal, so its normal is vertical: (0, 1). A wall on the left or right is vertical, so its normal is (1, 0).

📖 **New word: reflection** — bouncing. When a ball hits a wall, the part of its velocity **along the normal** turns around, and the part **along the wall** stays the same.

With a unit normal n, the part along the normal is (v · n) × n (a projection!). Turning it around means subtracting it **twice**:

> **reflect(v, n) = v − 2 × (v · n) × n**

🔢 **Maths: a ball moving (3, −4) — right and up — hits the ceiling (normal (0, 1))**

> v · n = 3 × 0 + (−4) × 1 = −4
> reflect = (3, −4) − 2 × (−4) × (0, 1) = (3, −4) − (0, −8) = **(3, 4)**

It keeps going right (3), but now goes **down** (4). ✓

`bounce.ppm` follows a ball for 160 steps. Each step:

1. **Gravity** pulls it down a little: velocity = velocity + (0, 0.25).
2. It moves: position = position + velocity.
3. If it has gone past a wall, its velocity is reflected (with normal (1, 0) for the side walls and (0, 1) for the floor and ceiling), and it is put back just inside.

The light trail shows the path: curved arcs (parabolas, from gravity) between bounces. A ball is drawn every 16 steps, so you can see it move faster at the bottom.

---

## 29.10 A vector field

📖 **New word: vector field** — an arrow at every point. A weather map with wind arrows is a vector field.

`field.ppm` draws an arrow at every point of a 40-pixel grid. The arrow at point p is:

> v = perpendicular(p − centre) × 0.12

p − centre points **away** from the centre; perpendicular turns it a quarter turn clockwise. So every arrow points **around** the centre: the field looks like a whirlpool, turning clockwise. Arrows further out are longer (we limit them to 30 pixels) and are coloured more orange.

---

## Code, part 1: `vec2.h`

File: `common/vec2.h` (new). It includes `wu.h`, so the whole drawing library is available.

```cpp
#ifndef VEC2_H
#define VEC2_H

#include <algorithm>
#include <cmath>
#include <vector>
#include "wu.h"

using Vec2 = PointF;

inline Vec2 operator+(Vec2 a, Vec2 b) {
    return Vec2{a.x + b.x, a.y + b.y};
}

inline Vec2 operator-(Vec2 a, Vec2 b) {
    return Vec2{a.x - b.x, a.y - b.y};
}

inline Vec2 operator-(Vec2 v) {
    return Vec2{-v.x, -v.y};
}

inline Vec2 operator*(Vec2 v, double s) {
    return Vec2{v.x * s, v.y * s};
}

inline Vec2 operator*(double s, Vec2 v) {
    return Vec2{v.x * s, v.y * s};
}

inline Vec2 operator/(Vec2 v, double s) {
    return Vec2{v.x / s, v.y / s};
}

inline double dot(Vec2 a, Vec2 b) {
    return a.x * b.x + a.y * b.y;
}

inline double cross(Vec2 a, Vec2 b) {
    return a.x * b.y - a.y * b.x;
}

inline double length(Vec2 v) {
    return std::sqrt(dot(v, v));
}

inline double distance(Vec2 a, Vec2 b) {
    return length(b - a);
}

inline Vec2 normalize(Vec2 v) {
    double len = length(v);
    if (len == 0.0) {
        return Vec2{0.0, 0.0};
    }
    return v / len;
}

inline Vec2 perpendicular(Vec2 v) {
    return Vec2{-v.y, v.x};
}

inline Vec2 project(Vec2 v, Vec2 onto) {
    double d = dot(onto, onto);
    if (d == 0.0) {
        return Vec2{0.0, 0.0};
    }
    return onto * (dot(v, onto) / d);
}

inline Vec2 reflect(Vec2 v, Vec2 normal) {
    Vec2 n = normalize(normal);
    return v - n * (2.0 * dot(v, n));
}

inline double distanceToLine(Vec2 p, Vec2 a, Vec2 b) {
    double len = length(b - a);
    if (len == 0.0) {
        return length(p - a);
    }
    return std::fabs(cross(b - a, p - a)) / len;
}

inline Vec2 closestPointOnSegment(Vec2 p, Vec2 a, Vec2 b) {
    Vec2 ab = b - a;
    double d = dot(ab, ab);
    if (d == 0.0) {
        return a;
    }
    double t = std::clamp(dot(p - a, ab) / d, 0.0, 1.0);
    return a + ab * t;
}

inline double distanceToSegment(Vec2 p, Vec2 a, Vec2 b) {
    return length(p - closestPointOnSegment(p, a, b));
}

inline double capsuleCoverage(Vec2 a, Vec2 b, double radius, int x, int y, int n) {
    int inside = 0;
    for (int j = 0; j < n; ++j) {
        for (int i = 0; i < n; ++i) {
            Vec2 s{x + sampleOffset(i, n), y + sampleOffset(j, n)};
            if (distanceToSegment(s, a, b) <= radius) {
                ++inside;
            }
        }
    }
    return static_cast<double>(inside) / (n * n);
}

inline void fillCapsuleAA(Image& image, Vec2 a, Vec2 b, double radius, Colour c, int n = 4) {
    if (radius <= 0.0 || n < 1) {
        return;
    }
    const double halfDiagonal = 0.70711;
    int x0 = static_cast<int>(std::floor(std::min(a.x, b.x) - radius));
    int y0 = static_cast<int>(std::floor(std::min(a.y, b.y) - radius));
    int x1 = static_cast<int>(std::ceil(std::max(a.x, b.x) + radius));
    int y1 = static_cast<int>(std::ceil(std::max(a.y, b.y) + radius));
    Rect box = clipToImage(Rect{x0, y0, x1, y1}, image);
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            double d = distanceToSegment(Vec2{x + 0.5, y + 0.5}, a, b);
            if (d <= radius - halfDiagonal) {
                image.setPixel(x, y, c);
            } else if (d < radius + halfDiagonal) {
                paintCoverage(image, x, y, c, capsuleCoverage(a, b, radius, x, y, n));
            }
        }
    }
}

inline void drawArrowAA(Image& image, Vec2 from, Vec2 to, double thickness, Colour c) {
    Vec2 d = to - from;
    double len = length(d);
    if (len == 0.0) {
        return;
    }
    Vec2 u = d / len;
    double headLength = std::min(len, thickness * 4.0);
    Vec2 base = to - u * headLength;
    Vec2 side = perpendicular(u) * (thickness / 2.0);
    Vec2 wing = perpendicular(u) * (thickness * 2.0);
    std::vector<PointF> shaft = {from + side, base + side, base - side, from - side};
    std::vector<PointF> head = {base + wing, to, base - wing};
    fillPathsAA(image, {shaft, head}, c);
}

#endif
```

### Line by line

**The start and the arithmetic (lines 1–33)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef VEC2_H` / `#define VEC2_H` | Include guard. |
| 4–6 | `#include <algorithm>` / `<cmath>` / `<vector>` | `std::min`, `std::max`, `std::clamp`; `std::sqrt`, `std::fabs`, `std::floor`, `std::ceil`; vectors. |
| 7 | `#include "wu.h"` | The whole drawing library (Chapters 11–28). |
| 9 | `using Vec2 = PointF;` | A second name for `PointF` (Section 29.1). |
| 11–13 | `inline Vec2 operator+(Vec2 a, Vec2 b) { return Vec2{a.x + b.x, a.y + b.y}; }` | Now `a + b` works for vectors (and points): add the components. This is **operator overloading**, the same idea as `ColourF` in Chapter 14. |
| 15–17 | `inline Vec2 operator-(Vec2 a, Vec2 b) { ... }` | `a - b`: subtract the components. |
| 19–21 | `inline Vec2 operator-(Vec2 v) { return Vec2{-v.x, -v.y}; }` | `-v` (one operand): the arrow turned around. |
| 23–29 | `operator*(Vec2 v, double s)` and `operator*(double s, Vec2 v)` | `v * 2.0` and `2.0 * v` both work: scale both components. |
| 31–33 | `inline Vec2 operator/(Vec2 v, double s) { ... }` | `v / s`: divide both components. |

**Dot, cross, length (lines 35–61)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 35–37 | `inline double dot(Vec2 a, Vec2 b) { return a.x * b.x + a.y * b.y; }` | The dot product (Section 29.4). |
| 39–41 | `inline double cross(Vec2 a, Vec2 b) { return a.x * b.y - a.y * b.x; }` | The 2D cross product (Section 29.6). |
| 43–45 | `inline double length(Vec2 v) { return std::sqrt(dot(v, v)); }` | √(v · v) = √(x² + y²) (Section 29.3). (There is also a `length(ColourF)` from Chapter 14; C++ picks the right one by the type of the argument.) |
| 47–49 | `inline double distance(Vec2 a, Vec2 b) { return length(b - a); }` | The distance between two points: the length of the step between them. |
| 51–57 | `inline Vec2 normalize(Vec2 v) { double len = length(v); if (len == 0.0) { return Vec2{0.0, 0.0}; } return v / len; }` | A unit vector in the same direction, or (0, 0) for the zero vector. |
| 59–61 | `inline Vec2 perpendicular(Vec2 v) { return Vec2{-v.y, v.x}; }` | A quarter turn, clockwise on the screen (Section 29.5). |

**Projection, reflection, distances (lines 63–96)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 63–69 | `inline Vec2 project(Vec2 v, Vec2 onto) { double d = dot(onto, onto); if (d == 0.0) { return Vec2{0.0, 0.0}; } return onto * (dot(v, onto) / d); }` | The shadow of v on the direction `onto` (Section 29.7). A zero `onto` has no direction: answer (0, 0). |
| 71–74 | `inline Vec2 reflect(Vec2 v, Vec2 normal) { Vec2 n = normalize(normal); return v - n * (2.0 * dot(v, n)); }` | Bounce v off a surface with this normal (Section 29.9). We normalise first, so the caller can pass any length. |
| 76–82 | `inline double distanceToLine(Vec2 p, Vec2 a, Vec2 b) { ... return std::fabs(cross(b - a, p - a)) / len; }` | \|cross\| / length (Section 29.8). If a and b are the same point, there is no line: we return the distance to that point. |
| 84–92 | `inline Vec2 closestPointOnSegment(Vec2 p, Vec2 a, Vec2 b) { ... double t = std::clamp(dot(p - a, ab) / d, 0.0, 1.0); return a + ab * t; }` | The three steps of Section 29.8: project, clamp t to [0, 1], lerp. |
| 94–96 | `inline double distanceToSegment(Vec2 p, Vec2 a, Vec2 b) { return length(p - closestPointOnSegment(p, a, b)); }` | The distance to that closest point. |

**Smooth capsules (lines 98–131)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 98–109 | `inline double capsuleCoverage(...) { ... if (distanceToSegment(s, a, b) <= radius) { ++inside; } ... }` | Like `circleCoverage` (Chapter 27), but the test is "distance to the **segment** ≤ radius". |
| 111 | `inline void fillCapsuleAA(Image& image, Vec2 a, Vec2 b, double radius, Colour c, int n = 4) {` | A smooth line from a to b, `radius` pixels from its middle to its edge (so its thickness is 2 × radius), with round ends. |
| 112–114 | `if (radius <= 0.0 \|\| n < 1) { return; }` | Nothing to draw. |
| 115 | `const double halfDiagonal = 0.70711;` | As in `fillCircleAA`. |
| 116–120 | the bounding box | From the smaller x and y of a and b, minus the radius, to the bigger ones, plus the radius. |
| 121–123 | the loops and `double d = distanceToSegment(Vec2{x + 0.5, y + 0.5}, a, b);` | The pixel centre's distance to the segment. |
| 124–128 | `if (d <= radius - halfDiagonal) { image.setPixel(x, y, c); } else if (d < radius + halfDiagonal) { paintCoverage(...); }` | Solid inside, sampled near the edge, skipped outside — exactly the circle trick. (It works because moving a point by a distance s changes its distance to the segment by at most s.) |
| 129–131 | `}` `}` `}` | End. |

**Smooth arrows (lines 133–147)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 133 | `inline void drawArrowAA(Image& image, Vec2 from, Vec2 to, double thickness, Colour c) {` | An arrow from `from` to `to`, with a triangular head at `to`. |
| 134–138 | `Vec2 d = to - from; double len = length(d); if (len == 0.0) { return; }` | The arrow's direction and length; nothing to draw if it has no length. |
| 139 | `Vec2 u = d / len;` | The unit direction. |
| 140 | `double headLength = std::min(len, thickness * 4.0);` | The head is 4 thicknesses long — but never longer than the whole arrow. |
| 141 | `Vec2 base = to - u * headLength;` | Where the head starts: go back from the tip along the arrow. |
| 142 | `Vec2 side = perpendicular(u) * (thickness / 2.0);` | Half the shaft's thickness, sideways. |
| 143 | `Vec2 wing = perpendicular(u) * (thickness * 2.0);` | Half the head's width (4 thicknesses wide), sideways. |
| 144 | `std::vector<PointF> shaft = {from + side, base + side, base - side, from - side};` | The shaft: a thin rectangle from `from` to the head's base (like Chapter 27's thick line). |
| 145 | `std::vector<PointF> head = {base + wing, to, base - wing};` | The head: a triangle. Both shapes go round in the same direction. |
| 146 | `fillPathsAA(image, {shaft, head}, c);` | Fill both in **one** call, so no seam appears where they meet (Chapter 27, Section 27.8). |
| 147 | `}` | End. |
| 149 | `#endif` | End of the include guard. |

---

## Code, part 2: vector sums, a field, a bounce and a figure

File: `ch29/vectors.cpp`

```cpp
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
#include "vec2.h"

void show(const std::string& name, Vec2 v) {
    std::cout << name << " = (" << v.x << ", " << v.y << ")\n";
}

int main() {
    Vec2 a{3.0, 4.0};
    Vec2 b{2.0, -1.0};
    show("a + b", a + b);
    show("a - b", a - b);
    show("a * 2", a * 2.0);
    std::cout << "length of a = " << length(a) << "\n";
    show("normalize(a)", normalize(a));
    std::cout << "dot(a, b) = " << dot(a, b) << ", cross(a, b) = " << cross(a, b) << "\n";
    show("perpendicular(a)", perpendicular(a));
    std::cout << "dot(a, perpendicular(a)) = " << dot(a, perpendicular(a)) << "\n";

    Vec2 right{1.0, 0.0};
    std::cout << "dot with (1, 0): (1, 1) -> " << dot(right, Vec2{1.0, 1.0}) << ", (0, 1) -> "
              << dot(right, Vec2{0.0, 1.0}) << ", (-1, 1) -> " << dot(right, Vec2{-1.0, 1.0})
              << "\n";

    Vec2 pa{2.0, 2.0};
    Vec2 pb{10.0, 2.0};
    Vec2 pp{6.0, 5.0};
    std::cout << "edgeFunction = " << edgeFunction(pa, pb, pp)
              << ", cross(B - A, P - A) = " << cross(pb - pa, pp - pa) << "\n";

    std::cout << "distance from (4, 0) to the line (0, 0)-(3, 4) = "
              << distanceToLine(Vec2{4.0, 0.0}, Vec2{0.0, 0.0}, Vec2{3.0, 4.0}) << "\n";
    show("project (4, 0) onto (3, 4)", project(Vec2{4.0, 0.0}, Vec2{3.0, 4.0}));
    show("reflect (3, -4) on a floor with normal (0, 1)", reflect(Vec2{3.0, -4.0}, Vec2{0.0, 1.0}));

    Vec2 s0{0.0, 0.0};
    Vec2 s1{10.0, 0.0};
    const Vec2 tests[3] = {Vec2{-3.0, 4.0}, Vec2{4.0, 3.0}, Vec2{13.0, 4.0}};
    for (Vec2 p : tests) {
        Vec2 q = closestPointOnSegment(p, s0, s1);
        std::cout << "closest point to (" << p.x << ", " << p.y << ") is (" << q.x << ", " << q.y
                  << "), distance " << distanceToSegment(p, s0, s1) << "\n";
    }

    Image add(400, 300, colours::white);
    Vec2 origin{40.0, 250.0};
    Vec2 va{180.0, -60.0};
    Vec2 vb{100.0, -150.0};
    drawLineWu(add, origin + vb, origin + va + vb, Colour{200, 200, 200});
    drawLineWu(add, origin + va, origin + va + vb, Colour{200, 200, 200});
    drawLineWu(add, origin, origin + vb, Colour{200, 200, 200});
    drawArrowAA(add, origin, origin + va, 3.0, Colour{40, 80, 200});
    drawArrowAA(add, origin + va, origin + va + vb, 3.0, Colour{200, 40, 40});
    drawArrowAA(add, origin, origin + va + vb, 3.0, Colour{30, 150, 60});

    Image field(400, 400, Colour{15, 20, 35});
    Vec2 centre{200.0, 200.0};
    for (int gy = 20; gy < 400; gy += 40) {
        for (int gx = 20; gx < 400; gx += 40) {
            Vec2 p{gx + 0.5, gy + 0.5};
            Vec2 v = perpendicular(p - centre) * 0.12;
            double len = length(v);
            if (len > 30.0) {
                v = v * (30.0 / len);
            }
            double t = std::min(len / 30.0, 1.0);
            Colour col = lerpColour(Colour{80, 160, 255}, Colour{255, 120, 60}, t);
            drawArrowAA(field, p - v * 0.5, p + v * 0.5, 2.0, col);
        }
    }

    Image bounce(400, 300, colours::white);
    strokeRect(bounce, Rect{10, 10, 390, 290}, 2, Colour{120, 120, 120});
    Vec2 pos{50.0, 60.0};
    Vec2 vel{5.0, 0.0};
    const Vec2 gravity{0.0, 0.25};
    std::vector<PointF> trail;
    for (int step = 0; step < 160; ++step) {
        trail.push_back(pos);
        vel = vel + gravity;
        pos = pos + vel;
        if (pos.x < 20.0 || pos.x > 380.0) {
            vel = reflect(vel, Vec2{1.0, 0.0});
            pos.x = std::clamp(pos.x, 20.0, 380.0);
        }
        if (pos.y < 20.0 || pos.y > 280.0) {
            vel = reflect(vel, Vec2{0.0, 1.0});
            pos.y = std::clamp(pos.y, 20.0, 280.0);
        }
    }
    drawPolylineWu(bounce, trail, Colour{160, 160, 200});
    for (int i = 0; i < static_cast<int>(trail.size()); i += 16) {
        fillCircleAA(bounce, trail[i].x, trail[i].y, 7.0, Colour{230, 90, 40});
    }

    Image figure(300, 300, Colour{250, 245, 230});
    Colour ink{40, 40, 60};
    fillCircleAA(figure, 150.0, 70.0, 30.0, ink);
    fillCapsuleAA(figure, Vec2{150.0, 100.0}, Vec2{150.0, 190.0}, 8.0, ink);
    fillCapsuleAA(figure, Vec2{150.0, 120.0}, Vec2{95.0, 160.0}, 6.0, ink);
    fillCapsuleAA(figure, Vec2{150.0, 120.0}, Vec2{210.0, 95.0}, 6.0, ink);
    fillCapsuleAA(figure, Vec2{150.0, 190.0}, Vec2{110.0, 270.0}, 7.0, ink);
    fillCapsuleAA(figure, Vec2{150.0, 190.0}, Vec2{195.0, 268.0}, 7.0, ink);

    bool ok = add.savePPM("add.ppm");
    ok = ok && field.savePPM("field.ppm");
    ok = ok && bounce.savePPM("bounce.ppm");
    ok = ok && figure.savePPM("figure.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
```

Build and run (from the `code/ch29` folder):

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common vectors.cpp -o vectors
./vectors
```

### Line by line

**The numbers (lines 7–46)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 7–9 | `void show(const std::string& name, Vec2 v) { ... }` | Print a vector as "name = (x, y)". |
| 12–13 | `Vec2 a{3.0, 4.0};` / `Vec2 b{2.0, -1.0};` | The two example vectors of this chapter. |
| 14–18 | the `show` and `length` lines | a + b, a − b, a × 2, the length of a, and normalize(a) (Sections 29.2–29.3). |
| 19 | `std::cout << "dot(a, b) = " ...` | The dot and cross products (Sections 29.4 and 29.6). |
| 20–21 | `show("perpendicular(a)", ...)` / `dot(a, perpendicular(a))` | The quarter turn and its proof: the dot product is 0 (Section 29.5). |
| 23–26 | `Vec2 right{1.0, 0.0};` and the long `std::cout` | The three signs of the dot product (Section 29.4). |
| 28–32 | `Vec2 pa{2.0, 2.0};` … `cross(pb - pa, pp - pa)` | The edge function and the cross product give the same number (Section 29.6). |
| 34–37 | `distanceToLine`, `project`, `reflect` | The examples of Sections 29.7–29.9. |
| 39–46 | `Vec2 s0{0.0, 0.0};` … the `for (Vec2 p : tests)` loop | The closest points of the table in Section 29.8. `const Vec2 tests[3] = {...};` is a small array of three vectors. |

**Vector addition (lines 48–57)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 48–51 | `Image add(400, 300, colours::white);` … `Vec2 vb{100.0, -150.0};` | A start point near the bottom left, and two vectors: a goes right and a little up, b goes right and a lot up. |
| 52–54 | three grey `drawLineWu` calls | The "other way round" (b first, then a) in thin grey: the parallelogram. |
| 55 | `drawArrowAA(add, origin, origin + va, 3.0, Colour{40, 80, 200});` | Blue: a, from the start point. |
| 56 | `drawArrowAA(add, origin + va, origin + va + vb, 3.0, Colour{200, 40, 40});` | Red: b, starting at the **tip** of a (head to tail). |
| 57 | `drawArrowAA(add, origin, origin + va + vb, 3.0, Colour{30, 150, 60});` | Green: a + b, straight from the start to the end. |

**The vector field (lines 59–73)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 59–60 | `Image field(400, 400, ...);` / `Vec2 centre{200.0, 200.0};` | A dark picture and its centre. |
| 61–63 | the two loops and `Vec2 p{gx + 0.5, gy + 0.5};` | A grid point every 40 pixels. |
| 64 | `Vec2 v = perpendicular(p - centre) * 0.12;` | The whirlpool arrow (Section 29.10). |
| 65–68 | `double len = length(v); if (len > 30.0) { v = v * (30.0 / len); }` | Limit the arrow to 30 pixels: scale it down to exactly 30 if it is longer. |
| 69–70 | `double t = std::min(len / 30.0, 1.0);` / `Colour col = lerpColour(...);` | Blue for short arrows, orange for long ones (Chapter 13). |
| 71 | `drawArrowAA(field, p - v * 0.5, p + v * 0.5, 2.0, col);` | Draw the arrow **centred** on the grid point: half of it before p, half after. |

**The bouncing ball (lines 75–97)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 75–76 | `Image bounce(...);` / `strokeRect(bounce, Rect{10, 10, 390, 290}, 2, ...);` | A box with grey walls (Chapter 19). |
| 77–79 | `Vec2 pos{50.0, 60.0};` / `Vec2 vel{5.0, 0.0};` / `const Vec2 gravity{0.0, 0.25};` | The ball's position, its velocity (5 pixels right per step), and the gravity (0.25 down per step, every step). |
| 80 | `std::vector<PointF> trail;` | Every position, for drawing the path. |
| 81–84 | `for (int step = 0; ...) { trail.push_back(pos); vel = vel + gravity; pos = pos + vel;` | Each step: remember where it is, speed up downwards, move. |
| 85–88 | `if (pos.x < 20.0 \|\| pos.x > 380.0) { vel = reflect(vel, Vec2{1.0, 0.0}); pos.x = std::clamp(...); }` | Hit a side wall: bounce (normal (1, 0)), and put it back inside. (The ball's centre stays 10 pixels from the walls, a bit more than its radius 7.) |
| 89–92 | `if (pos.y < 20.0 \|\| pos.y > 280.0) { vel = reflect(vel, Vec2{0.0, 1.0}); ... }` | Hit the floor or ceiling: bounce with normal (0, 1). |
| 94 | `drawPolylineWu(bounce, trail, Colour{160, 160, 200});` | The path, as a smooth light line (Chapter 28). |
| 95–97 | `for (int i = 0; ...; i += 16) { fillCircleAA(bounce, trail[i].x, trail[i].y, 7.0, ...); }` | A smooth orange ball at every 16th position. |

**The stick figure (lines 99–106)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 99–100 | `Image figure(...);` / `Colour ink{40, 40, 60};` | A cream background and dark ink. |
| 101 | `fillCircleAA(figure, 150.0, 70.0, 30.0, ink);` | The head. |
| 102 | `fillCapsuleAA(figure, Vec2{150.0, 100.0}, Vec2{150.0, 190.0}, 8.0, ink);` | The body: a capsule 16 pixels thick. |
| 103–104 | two `fillCapsuleAA` calls from (150, 120) | The arms: one down to the left, one up to the right (waving). |
| 105–106 | two `fillCapsuleAA` calls from (150, 190) | The legs. All the joints are round, because every capsule has round ends. |

**Saving (lines 108–117)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 108–111 | `bool ok = add.savePPM("add.ppm");` … | Save the four pictures. |
| 112–117 | `if (!ok) { ... }` `return 0;` `}` | Report a problem, or finish. |

### What you should see

The program prints:

```
a + b = (5, 3)
a - b = (1, 5)
a * 2 = (6, 8)
length of a = 5
normalize(a) = (0.6, 0.8)
dot(a, b) = 2, cross(a, b) = -11
perpendicular(a) = (-4, 3)
dot(a, perpendicular(a)) = 0
dot with (1, 0): (1, 1) -> 1, (0, 1) -> 0, (-1, 1) -> -1
edgeFunction = 24, cross(B - A, P - A) = 24
distance from (4, 0) to the line (0, 0)-(3, 4) = 3.2
project (4, 0) onto (3, 4) = (1.44, 1.92)
reflect (3, -4) on a floor with normal (0, 1) = (3, 4)
closest point to (-3, 4) is (0, 0), distance 5
closest point to (4, 3) is (4, 0), distance 3
closest point to (13, 4) is (10, 0), distance 5
```

Open the pictures:
- `add.ppm`: a blue arrow and a red arrow head to tail, and a green arrow straight from start to end; thin grey lines complete the parallelogram.
- `field.ppm`: a grid of small arrows swirling clockwise around the centre, short and blue near the middle, long and orange further out.
- `bounce.ppm`: a box, a light curved path bouncing between floor and walls, and orange balls along it.
- `figure.ppm`: a smooth stick figure, waving.

---

## Small examples

### Example 1 — A step toward a target

A monster at (10, 10) moves 5 pixels per step toward the player at (40, 50):

> direction = (40, 50) − (10, 10) = (30, 40), length 50 → unit (0.6, 0.8)
> new position = (10, 10) + 5 × (0.6, 0.8) = **(13, 14)**

### Example 2 — Is the light in front of the wall?

A wall with normal n = (0, −1) (it faces up). A lamp is at L = (5, 2), and a point on the wall is W = (0, 10):

> (L − W) · n = (5, −8) · (0, −1) = 0 + 8 = 8 > 0 → the lamp is **in front of** the wall (on the side the normal points to)

We will use this test for lighting in Chapter 68.

### Example 3 — The area of a parallelogram

a = (4, 0), b = (1, 3):

> |a × b| = |4 × 3 − 0 × 1| = **12** = base 4 × height 3 ✓

### Example 4 — Splitting a velocity

A ball moving v = (6, 2) hits a floor (normal (0, 1)):

> along the normal: (v · n) n = 2 × (0, 1) = (0, 2)
> along the floor: v − (0, 2) = (6, 0)
> after the bounce: (6, 0) − (0, 2) = **(6, −2)** — the floor part stays, the normal part flips

### Example 5 — Perpendicular the other way

−perpendicular((3, 4)) = −(−4, 3) = **(4, −3)**: a quarter turn **counter-clockwise** on the screen.

---

## Common mistakes

⚠️ **Adding points.** point + point means nothing. Subtract points to get a vector; add a vector to a point to move it.

⚠️ **Normalising the zero vector.** It has no direction; dividing by 0 gives "not a number". Check the length first (our `normalize` does).

⚠️ **Mixing up dot and cross.** Dot: same direction? (0 when perpendicular.) Cross: which side? (0 when parallel.)

⚠️ **Using a normal that is not a unit vector in `reflect`.** v − 2(v·n)n only works if |n| = 1. Our `reflect` normalises the normal for you.

⚠️ **Forgetting that y goes down.** `perpendicular` turns **clockwise** on the screen, and a normal pointing "up" is (0, −1).

⚠️ **Not clamping t for a segment.** Without the clamp you get the distance to the endless **line**, and capsules would never end.

---

## Practice

🏋️ **1.** Compute (5, −2) + (−1, 7), (5, −2) − (−1, 7), and 3 × (5, −2).

🏋️ **2.** What is the length of (6, 8)? Normalise it.

🏋️ **3.** Compute (2, 3) · (4, −1) and (2, 3) × (4, −1). Are they perpendicular? Parallel? Which way does (4, −1) turn from (2, 3)?

🏋️ **4.** Project v = (5, 5) onto d = (1, 0). Then onto d = (0, 2). What do you notice?

🏋️ **5.** A ball moving (−4, 3) hits the left wall (normal (1, 0)). What is its new velocity?

🏋️ **6.** Find the closest point on the segment (2, 2)–(8, 8) to P = (8, 2), and the distance.

🏋️ **7.** Write `angleSign(Vec2 a, Vec2 b)` that returns "same", "right angle" or "opposite" by looking at the dot product, and "left", "right" or "parallel" by looking at the cross product.

🏋️ **8.** Draw a "smooth polyline" made of capsules: for a list of points, draw a capsule between every two neighbours. Why do the joints look good?

---

## Answers

**1.**
> (5 + (−1), −2 + 7) = **(4, 5)**
> (5 − (−1), −2 − 7) = **(6, −9)**
> (15, −6)

**2.**
> √(36 + 64) = √100 = **10** → normalised (0.6, 0.8)

(The same direction as (3, 4) — it is just twice as long.)

**3.**
> dot = 2 × 4 + 3 × (−1) = 8 − 3 = **5** → positive: roughly the same way, **not** perpendicular
> cross = 2 × (−1) − 3 × 4 = −2 − 12 = **−14** → not 0, so **not** parallel; negative → (4, −1) is to the **left** of (2, 3) (counter-clockwise on the screen)

**4.**
> onto (1, 0): (1, 0) × (5 × 1 + 5 × 0) / 1 = **(5, 0)**
> onto (0, 2): (0, 2) × (0 + 10) / 4 = (0, 2) × 2.5 = **(0, 5)**

The projection onto the x direction is just the x part, and onto the y direction just the y part. And the **length** of d does not matter — (0, 2) and (0, 1) give the same projection, because the formula divides by d · d.

**5.**
> n = (1, 0), v · n = −4
> reflect = (−4, 3) − 2 × (−4) × (1, 0) = (−4, 3) + (8, 0) = **(4, 3)**

It now moves right, and still down. ✓

**6.**
> AB = (6, 6), AP = (6, 0)
> t = (6 × 6 + 0 × 6) / (36 + 36) = 36 / 72 = 0.5 (between 0 and 1: no clamping)
> Q = (2, 2) + 0.5 × (6, 6) = **(5, 5)**
> distance = |(8, 2) − (5, 5)| = |(3, −3)| = √18 ≈ **4.24**

**7.**

```cpp
#include <string>

std::string angleSign(Vec2 a, Vec2 b) {
    double d = dot(a, b);
    double c = cross(a, b);
    std::string first = (d > 0.0) ? "same" : (d < 0.0) ? "opposite" : "right angle";
    std::string second = (c > 0.0) ? "right" : (c < 0.0) ? "left" : "parallel";
    return first + ", " + second;
}
```

> angleSign((1, 0), (0, 1)) → "right angle, right" (down is a clockwise quarter turn from right)

**8.**

```cpp
void drawSmoothPath(Image& image, const std::vector<Vec2>& points, double radius, Colour c) {
    for (int i = 0; i + 1 < static_cast<int>(points.size()); ++i) {
        fillCapsuleAA(image, points[i], points[i + 1], radius, c);
    }
}
```

Every capsule ends in a **half circle** around its end point, and the next capsule starts with a half circle around the **same** point. Together they cover the whole circle around the joint, whatever the angle between the segments — so there are no gaps or spikes. (The only small flaw: edge pixels where two capsules overlap are blended twice — conflation, Chapter 27. With solid colours and a dark ink this is hard to see.)

---

## Summary

🧠 A **vector** is an arrow (x, y): a direction and a length. A point is a place. **point − point = vector**, **point + vector = point**.

🧠 Add, subtract and scale **component by component**. Adding = one step after another.

🧠 **Length** |v| = √(x² + y²). **Unit vector** = v / |v|.

🧠 **Dot** a·b = a.x·b.x + a.y·b.y: > 0 same way, 0 perpendicular, < 0 opposite.

🧠 **Cross** a×b = a.x·b.y − a.y·b.x: the edge function of Chapter 24. > 0 right (clockwise), 0 parallel, < 0 left; |a×b| = parallelogram area.

🧠 **perpendicular(v) = (−v.y, v.x)**: a clockwise quarter turn on the screen.

🧠 **Projection** onto d: d × (v·d)/(d·d). **Reflection**: v − 2(v·n)n with a unit normal n.

🧠 Distance to a **line**: |cross| / length. To a **segment**: clamp t to [0, 1] first. **Capsules** = smooth lines with round ends.

---

## Next chapter

We have been talking about directions without ever measuring an **angle**. In Chapter 30 we learn to measure angles in degrees and in **radians**, and meet **sine** and **cosine**: the two numbers that turn an angle into a direction. With them we can finally put points on a circle at any angle, draw regular polygons and stars without tables of numbers, make clocks and spirals — and see why the dot product is |a||b|·cos(angle).
