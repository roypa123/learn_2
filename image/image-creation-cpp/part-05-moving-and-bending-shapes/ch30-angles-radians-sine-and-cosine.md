# Chapter 30 — Angles, Radians, Sine and Cosine

> **Part 5 · Chapter 30 of 82**
> **You need:** Chapters 1–29 (especially 22, 23 and 29) · **You will make:** `angles.h` (π, degrees and radians, directions from angles, points on circles and ellipses, angles of vectors, regular polygons and stars), `clock.ppm`, `shapes.ppm`, `waves.ppm`, `spiral.ppm` and `orbits.ppm`

---

## What you will learn

- What an **angle** is, and two ways to measure it: **degrees** and **radians**.
- What the number **π** (pi) has to do with radians.
- What **cosine** and **sine** are: the x and y of a point on a circle.
- The most important values (0°, 30°, 45°, 60°, 90°, …), and how to check them with Pythagoras.
- Why, on our screen, **angles turn clockwise**.
- How to put a point on a circle — or an ellipse — at any angle.
- How to find the angle of a vector (**atan2**), and the angle between two vectors (the dot product again).
- How to draw clocks, regular polygons, stars, waves and spirals.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **angle** | How much something turns, or how far apart two directions are. |
| **degree** (°) | A unit of angle: a full turn is 360°. |
| **radian** | A unit of angle based on the circle: a full turn is 2π radians (about 6.28). |
| **arc** | A piece of a circle's edge. |
| **unit circle** | The circle with radius 1 around (0, 0) (Chapter 23). |
| **cosine** (cos) | For an angle: the x-coordinate of the point at that angle on the unit circle. |
| **sine** (sin) | For an angle: the y-coordinate of that point. |
| **trigonometry** | The maths of angles, sines and cosines (from Greek: "measuring triangles"). |
| **atan2** | A function that gives the angle of a direction (x, y). |
| **parametric** | Describing a curve by a "moving" number t: as t changes, the point moves along the curve. |
| **regular polygon** | A polygon with all sides the same length and all corners the same angle. |
| **period** | How long a repeating pattern takes before it starts again. |
| **amplitude** | How far a wave goes up and down from its middle. |

---

## 30.1 What is an angle?

📖 **New word: angle** — how much something **turns**. If you stand facing east and turn to face south, you have turned by an angle. It is also the size of the "opening" between two directions.

📖 **New word: degree** (°) — the everyday unit. A full turn is **360°**:

| turn | degrees |
|---|---|
| no turn | 0° |
| a quarter turn (a right angle, like the corner of a page) | 90° |
| a half turn (facing backwards) | 180° |
| three quarters | 270° |
| a full turn (back where you started) | 360° |

The number 360 is very old (it comes from ancient Babylon, about 4000 years ago). It is handy because it divides nicely: by 2, 3, 4, 5, 6, 8, 9, 10, 12, …

---

## 30.2 Radians and π

Degrees are easy for people, but the maths functions in C++ (`std::sin`, `std::cos`) use a different unit.

📖 **New word: arc** — a piece of the edge of a circle.

📖 **New word: radian** — the angle at which the **arc** is exactly as long as the **radius**.

```
            ●  ← arc of length r
          ╱  ╲
     r  ╱  1   ╲          an angle of 1 radian:
      ╱ radian  ╲         the curved edge is as long as
     ●───────────●        each of the two straight sides
          r
```

How many radians are in a full turn? The whole circumference is 2πr (Chapter 22). Each radian uses up an arc of length r. So a full turn is:

> 2πr / r = **2π radians** ≈ 6.283

📖 **New word: π** — remember it from Chapter 22: π ≈ 3.14159, the circumference divided by the diameter. We store it as a constant:

```cpp
const double kPi = 3.14159265358979323846;
```

(The `k` at the start is a common way of saying "this is a constant". The digits go further than a `double` can hold, which is fine: it keeps the closest possible value.)

### Converting

> 360° = 2π radians, so **180° = π radians**
> **radians = degrees × π / 180**
> **degrees = radians × 180 / π**

🔢 **Maths: some angles in radians**

| degrees | radians (exact) | radians (number) |
|---|---|---|
| 0° | 0 | 0 |
| 30° | π/6 | 0.5236 |
| 45° | π/4 | 0.7854 |
| 60° | π/3 | 1.0472 |
| 90° | π/2 | 1.5708 |
| 180° | π | 3.1416 |
| 360° | 2π | 6.2832 |

> 1 radian = 180 / π ≈ **57.3°**

⚠️ **The most common mistake in all of graphics:** giving degrees to `std::sin` or `std::cos`. `std::sin(90)` is **not** 1 — it is the sine of 90 **radians** (about 14 full turns plus a bit), which is 0.894. Always convert first: `std::sin(degreesToRadians(90.0))`.

---

## 30.3 Cosine and sine: a point on the circle

📖 **New word: unit circle** — the circle with radius 1 around (0, 0).

Start at the point (1, 0) on the unit circle and **walk around the circle** by an angle θ. (θ, "theta", is the Greek letter usually used for angles.) You arrive at some point (x, y).

📖 **New word: cosine** — the **x** of that point: **cos θ**.

📖 **New word: sine** — the **y** of that point: **sin θ**.

> **the point at angle θ on the unit circle = (cos θ, sin θ)**

That is the whole definition. Everything else follows from it.

📖 **New word: trigonometry** — the maths of angles, sines and cosines.

### The important values

| θ | point (cos θ, sin θ) | why |
|---|---|---|
| 0° | (1, 0) | we have not moved |
| 90° | (0, 1) | a quarter turn |
| 180° | (−1, 0) | half way round, on the other side |
| 270° | (0, −1) | three quarters |
| 360° | (1, 0) | back at the start |
| 45° | (0.7071, 0.7071) | halfway between (1, 0) and (0, 1): x = y |
| 60° | (0.5, 0.8660) | |
| 30° | (0.8660, 0.5) | the mirror image of 60° (x and y swapped) |

🔢 **Maths: why is the 45° point (0.7071, 0.7071)?**

> At 45°, x = y (the point is on the diagonal).
> The point is on the unit circle: x² + y² = 1 (Pythagoras, Chapter 23).
> x² + x² = 1 → 2x² = 1 → x² = 0.5 → x = √0.5 ≈ **0.7071** ✓
> (This is the "half diagonal" of Chapter 27!)

🔢 **Maths: why is the 60° point (0.5, 0.866)?**

> Join (0, 0), (1, 0) and the 60° point: all three sides have length 1 (two are radii, and the angle between them is 60°). It is an **equilateral** triangle (Chapter 24).
> So the 60° point is right above the middle of the base: x = **0.5**.
> Pythagoras: y = √(1 − 0.25) = √0.75 ≈ **0.866** ✓ (that is √3/2, the hexagon height of Chapter 24)

### The circle rule

Because every point (cos θ, sin θ) is on the unit circle:

> **cos²θ + sin²θ = 1** for every angle

Our program checks it at 37°: it prints exactly 1.

### What our program prints

```
degrees, radians, cos, sin:
  0, 0, 1, 0
  30, 0.523599, 0.866025, 0.5
  45, 0.785398, 0.707107, 0.707107
  60, 1.0472, 0.5, 0.866025
  90, 1.5708, 6.12323e-17, 1
  180, 3.14159, -1, 1.22465e-16
  360, 6.28319, 1, -2.44929e-16
```

What is **6.12323e-17**? It means 6.12323 × 10⁻¹⁷ = 0.0000000000000000612323. The true cos 90° is exactly 0, but π cannot be stored exactly in a `double`, so the angle is a tiny bit off, and so is the answer. For drawing, a number this small **is** 0. (Never test `std::cos(x) == 0.0`; test if it is very small instead.)

---

## 30.4 On our screen, angles turn clockwise

In maths books, y goes **up**, and the angle 90° points **up**: angles turn **counter-clockwise**.

On our screen, y goes **down** (Chapter 3). The formulas do not change — (cos 90°, sin 90°) is still (0, 1) — but (0, 1) now means **down**:

```
                 270° (−90°)
                   (0, −1)
                     ↑
                     │
   180° (−1, 0) ←────●────→ (1, 0)  0°
                     │
                     ↓
                   (0, 1)
                    90°
```

🧠 **Remember:** on the screen, 0° points **right**, 90° points **down**, 180° **left**, and 270° (or −90°) **up**. Increasing the angle turns **clockwise**.

This matches what we found in Chapter 29: `perpendicular` turns (1, 0) into (0, 1), a clockwise quarter turn. And `perpendicular(fromAngle(θ))` is exactly `fromAngle(θ + 90°)`:

> perpendicular((cos θ, sin θ)) = (−sin θ, cos θ) = (cos(θ + 90°), sin(θ + 90°)) ✓

💡 To start at the **top** (like the 12 on a clock, or the top point of a star), start at **−90°**.

---

## 30.5 Points on circles and ellipses

### Any circle

For a circle with centre C and radius r: scale the unit circle by r, and move it to C (vectors, Chapter 29):

> **point = C + r × (cos θ, sin θ)**

🔢 **Maths: the 2 o'clock mark on a clock with centre (150, 150), radius 120**

> 2 o'clock is 2 × 30° = 60° after 12 o'clock; 12 o'clock is at −90°: θ = 60° − 90° = **−30°**
> cos(−30°) = 0.866, sin(−30°) = −0.5
> point = (150 + 120 × 0.866, 150 + 120 × (−0.5)) = **(253.9, 90)** — to the right and above the centre ✓

### Ellipses: the parametric form

📖 **New word: parametric** — a curve described by a "moving" number. As θ goes from 0 to 2π, the point moves once around the curve.

In Chapter 23 we built an ellipse by **stretching** the unit circle: x by a, y by b. So:

> **point on the ellipse = (cx + a × cos θ, cy + b × sin θ)**

In Chapter 23 we placed planets with y = b√(1 − (x/a)²) — choosing x and solving for y. Now we can simply choose an **angle**. `orbits.ppm` draws each orbit as a smooth polyline of 121 points (θ = 0, 3°, 6°, …, 360° — the last point is the same as the first, closing the loop), and puts each planet at its own angle.

⚠️ For an ellipse, θ is **not** the real angle of the point as seen from the centre (except at 0°, 90°, 180° and 270°). It is the angle on the circle **before** stretching. For orbits and drawings, that is fine.

---

## 30.6 The angle of a vector: atan2

The opposite question: given a direction (x, y), what is its angle?

📖 **New word: atan2** — the function `std::atan2(y, x)` gives the angle of the direction (x, y), in radians, between −π and π (−180° to 180°).

⚠️ Note the order: **y first**, then x.

🔢 **Maths: the program prints**

```
angleOf in degrees: (1, 1) 45, (0, 1) 90, (-1, 0) 180, (0, -1) -90
```

> (1, 1): down-right on the screen → 45° ✓
> (0, 1): straight down → 90° ✓
> (−1, 0): left → 180° ✓
> (0, −1): straight up → −90° (the same direction as 270°) ✓

💡 Why not just atan(y / x)? Because y / x loses information: (1, 1) and (−1, −1) both give y / x = 1, but they point in opposite directions. And x = 0 would divide by zero. `atan2` looks at the signs of x and y separately and always gives the right direction.

---

## 30.7 The angle between two vectors

Chapter 29 promised it: the dot product is

> **a · b = |a| × |b| × cos(angle between a and b)**

So:

> cos(angle) = (a · b) / (|a| × |b|) → **angle = acos((a · b) / (|a| × |b|))**

`std::acos` ("arc cosine") is the reverse of cosine: it gives the angle (from 0° to 180°) whose cosine is the given number.

🔢 **Maths: (1, 0) and (1, 1)**

> a · b = 1, |a| = 1, |b| = √2 ≈ 1.4142
> cos(angle) = 1 / 1.4142 = 0.7071 → angle = acos(0.7071) = **45°** ✓

🔢 **Maths: (3, 4) and (−4, 3)**

> a · b = −12 + 12 = 0 → cos(angle) = 0 → angle = **90°** ✓ (perpendicular, Chapter 29)

The program prints: `angleBetween in degrees: (1, 0) and (1, 1) 45, (3, 4) and (-4, 3) 90`.

⚠️ Because of tiny rounding errors, (a · b) / (|a| × |b|) can come out as 1.0000000001, and `acos` of a number bigger than 1 is "not a number". Our `angleBetween` **clamps** it to [−1, 1] first (Chapter 14).

💡 And the cross product (Chapter 29): a × b = |a| × |b| × **sin**(angle). Its sign tells you which way the angle turns.

---

## 30.8 Regular polygons and stars

📖 **New word: regular polygon** — all sides equal and all corners equal: an equilateral triangle, a square, a regular pentagon, hexagon, …

Its corners sit on a circle, at **equal angles**. For n corners, the angle between neighbours is 360° / n:

> corner i = C + r × (cos θi, sin θi), with **θi = start + i × 360° / n**

🔢 **Maths: a regular hexagon, start 0°**

> 360° / 6 = 60°: the corners are at 0°, 60°, 120°, 180°, 240°, 300°
> corner 1: (cos 60°, sin 60°) = (0.5, 0.866) → with r = 60: (30, 51.96) from the centre
> — exactly the (r/2, r√3/2) of Chapter 24 ✓

### The star of Chapter 25

In Chapter 25 we drew a star with a table of five numbers and promised to explain them. The five points are a regular pentagon, starting at the top (−90°), 72° apart (360° / 5 = 72°):

```
the five star corners of Chapter 25:
  0: (6.12323e-17, -1)
  1: (0.951057, -0.309017)
  2: (0.587785, 0.809017)
  3: (-0.587785, 0.809017)
  4: (-0.951057, -0.309017)
```

These are exactly the numbers of Chapter 25 (0, −1), (0.9511, −0.3090), … — now with more digits. (The first x, 6e-17, is "0 with a rounding error", Section 30.3.)

### Stars without crossings

The Chapter 25 star had crossing edges, which is why the fill rule mattered. Here is another way to make a star: go around the circle with **2n** points, alternating between an **outer** radius (the tips) and an **inner** radius (the dips between tips), with half the polygon angle between them:

> point i at angle start + i × 180° / n, radius = outer if i is even, inner if i is odd

This outline never crosses itself, so any fill rule fills it completely. `shapes.ppm` shows regular polygons with 3 to 8 sides on the top row, and stars with 3 to 8 tips below them, all starting at −90° so they point **up**.

---

## 30.9 Waves

📖 **New word: period** — the length after which a repeating pattern starts again. Sine and cosine repeat every 360° (2π): sin(θ + 360°) = sin θ.

📖 **New word: amplitude** — how far a wave goes from its middle.

To draw a sine **wave** across the screen, turn x into an angle:

> angle = 2π × x / period (one full wave every `period` pixels)
> y = middle − amplitude × sin(angle)

The **minus** makes the wave go **up** first, as in a maths book (on the screen, up is smaller y).

🔢 **Maths: period 200, amplitude 60, middle 100**

> x = 0: angle 0 → sin = 0 → y = 100 (the middle)
> x = 50: angle π/2 (90°) → sin = 1 → y = 100 − 60 = **40** (the top)
> x = 100: angle π → sin ≈ 0 → y = 100
> x = 150: angle 3π/2 (270°) → sin = −1 → y = **160** (the bottom)

`waves.ppm` draws the sine wave in blue and the cosine wave in red. Cosine is the same wave **shifted** by a quarter period: cos θ = sin(θ + 90°). (Look at the unit circle: x at angle θ is the same as y at angle θ + 90°.)

---

## 30.10 A spiral

If the radius **grows** as the angle grows, the point spirals outward. The simplest spiral (an "Archimedean spiral", after the Greek scientist Archimedes) has:

> r = k × θ

`spiral.ppm` uses k = 4, and θ from 0.05 to 32 radians (about 5 turns, since 32 / 6.28 ≈ 5.1), in 640 small steps. Each tiny step is a Wu line (Chapter 28), and its colour comes from the angle as a **hue** (Chapter 16) — so the colour goes round the rainbow once per turn.

🔢 **Maths: how far apart are the arms?**

> one full turn adds 2π to θ, so it adds k × 2π = 4 × 6.283 ≈ **25 pixels** to the radius — the arms are evenly spaced, 25 pixels apart

---

## 30.11 A clock

`clock.ppm` puts everything together:

- **60 minute marks** at angles i × 6° − 90° (360° / 60 = 6°, starting at the top): every 5th is a thick tick (a capsule from radius 104 to 120), the others small dots.
- **The minute hand** at 10 minutes: 10 × 6° − 90° = **−30°** (pointing at the 2).
- **The hour hand** at 10:10: the hour hand moves 30° per hour (360° / 12), and also moves **between** the numbers as the minutes pass: (10 + 10/60) × 30° − 90° = 305° − 90° = **215°**.

🔢 **Maths: where does the hour hand point?**

> 215°: cos 215° ≈ −0.819, sin 215° ≈ −0.574 → left and **up** (y is negative) → toward the 10 ✓ (and a sixth of the way to the 11)

---

## Code, part 1: `angles.h`

File: `common/angles.h` (new). It includes `vec2.h`.

```cpp
#ifndef ANGLES_H
#define ANGLES_H

#include <algorithm>
#include <cmath>
#include <vector>
#include "vec2.h"

const double kPi = 3.14159265358979323846;

inline double degreesToRadians(double degrees) {
    return degrees * kPi / 180.0;
}

inline double radiansToDegrees(double radians) {
    return radians * 180.0 / kPi;
}

inline Vec2 fromAngle(double radians) {
    return Vec2{std::cos(radians), std::sin(radians)};
}

inline PointF pointOnCircle(PointF centre, double r, double radians) {
    return centre + fromAngle(radians) * r;
}

inline PointF pointOnEllipse(PointF centre, double a, double b, double radians) {
    return PointF{centre.x + a * std::cos(radians), centre.y + b * std::sin(radians)};
}

inline double angleOf(Vec2 v) {
    return std::atan2(v.y, v.x);
}

inline double angleBetween(Vec2 a, Vec2 b) {
    double la = length(a);
    double lb = length(b);
    if (la == 0.0 || lb == 0.0) {
        return 0.0;
    }
    double c = std::clamp(dot(a, b) / (la * lb), -1.0, 1.0);
    return std::acos(c);
}

inline std::vector<PointF> regularPolygon(PointF centre, double r, int sides,
                                          double startRadians) {
    std::vector<PointF> points;
    for (int i = 0; i < sides; ++i) {
        double angle = startRadians + 2.0 * kPi * i / sides;
        points.push_back(pointOnCircle(centre, r, angle));
    }
    return points;
}

inline std::vector<PointF> starPoints(PointF centre, double outer, double inner, int tips,
                                      double startRadians) {
    std::vector<PointF> points;
    for (int i = 0; i < 2 * tips; ++i) {
        double angle = startRadians + kPi * i / tips;
        double r = (i % 2 == 0) ? outer : inner;
        points.push_back(pointOnCircle(centre, r, angle));
    }
    return points;
}

#endif
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef ANGLES_H` / `#define ANGLES_H` | Include guard. |
| 4–6 | `#include <algorithm>` / `<cmath>` / `<vector>` | `std::clamp`; `std::sin`, `std::cos`, `std::atan2`, `std::acos`; vectors. |
| 7 | `#include "vec2.h"` | `Vec2`, `dot`, `length`, and the whole drawing library. |
| 9 | `const double kPi = 3.14159265358979323846;` | π (Section 30.2). A `const` at the top of a header is allowed: each file that includes it gets its own copy of this one number. |
| 11–13 | `inline double degreesToRadians(double degrees) { return degrees * kPi / 180.0; }` | × π / 180. |
| 15–17 | `inline double radiansToDegrees(double radians) { return radians * 180.0 / kPi; }` | × 180 / π. |
| 19–21 | `inline Vec2 fromAngle(double radians) { return Vec2{std::cos(radians), std::sin(radians)}; }` | The unit vector pointing at this angle: the point on the unit circle (Section 30.3). |
| 23–25 | `inline PointF pointOnCircle(PointF centre, double r, double radians) { return centre + fromAngle(radians) * r; }` | C + r × (cos θ, sin θ) (Section 30.5) — written with the vector operators of Chapter 29. |
| 27–29 | `inline PointF pointOnEllipse(PointF centre, double a, double b, double radians) { return PointF{centre.x + a * std::cos(radians), centre.y + b * std::sin(radians)}; }` | The parametric ellipse: the circle stretched by a across and b down. |
| 31–33 | `inline double angleOf(Vec2 v) { return std::atan2(v.y, v.x); }` | The angle of a direction, from −π to π (Section 30.6). y first! |
| 35 | `inline double angleBetween(Vec2 a, Vec2 b) {` | The angle between two vectors, from 0 to π (Section 30.7). |
| 36–40 | `double la = length(a); double lb = length(b); if (la == 0.0 \|\| lb == 0.0) { return 0.0; }` | A zero vector has no direction, so there is no angle: we return 0. |
| 41 | `double c = std::clamp(dot(a, b) / (la * lb), -1.0, 1.0);` | The cosine of the angle, kept safely between −1 and 1. |
| 42–43 | `return std::acos(c);` `}` | Turn the cosine back into an angle. |
| 45–46 | `inline std::vector<PointF> regularPolygon(PointF centre, double r, int sides, double startRadians) {` | The corners of a regular polygon (Section 30.8). |
| 47–52 | `for (int i = 0; i < sides; ++i) { double angle = startRadians + 2.0 * kPi * i / sides; points.push_back(pointOnCircle(centre, r, angle)); }` | Equal steps of 2π / sides. (`2.0 * kPi * i` is a `double`, so the division by `sides` is not an integer division.) |
| 53 | `return points;` `}` | Done. |
| 55–56 | `inline std::vector<PointF> starPoints(PointF centre, double outer, double inner, int tips, double startRadians) {` | A star outline with no crossings (Section 30.8). |
| 58 | `for (int i = 0; i < 2 * tips; ++i) {` | Twice as many points as tips: tip, dip, tip, dip, … |
| 59 | `double angle = startRadians + kPi * i / tips;` | Steps of π / tips = 180° / tips: half the polygon step. |
| 60 | `double r = (i % 2 == 0) ? outer : inner;` | Even points are tips (outer radius), odd points are dips (inner radius). |
| 61–64 | `points.push_back(pointOnCircle(centre, r, angle));` `}` `return points;` `}` | Collect them. |
| 66 | `#endif` | End of the include guard. |

---

## Code, part 2: a clock, shapes, waves, a spiral and orbits

File: `ch30/angles.cpp`

```cpp
#include <cmath>
#include <iostream>
#include <vector>
#include "angles.h"
#include "hsv.h"

int main() {
    const double table[7] = {0.0, 30.0, 45.0, 60.0, 90.0, 180.0, 360.0};
    std::cout << "degrees, radians, cos, sin:\n";
    for (double d : table) {
        double r = degreesToRadians(d);
        std::cout << "  " << d << ", " << r << ", " << std::cos(r) << ", " << std::sin(r) << "\n";
    }
    double t = degreesToRadians(37.0);
    std::cout << "cos^2 + sin^2 at 37 degrees = "
              << std::cos(t) * std::cos(t) + std::sin(t) * std::sin(t) << "\n";

    std::cout << "the five star corners of Chapter 25:\n";
    for (int k = 0; k < 5; ++k) {
        Vec2 v = fromAngle(degreesToRadians(-90.0 + 72.0 * k));
        std::cout << "  " << k << ": (" << v.x << ", " << v.y << ")\n";
    }

    std::cout << "angleOf in degrees: (1, 1) " << radiansToDegrees(angleOf(Vec2{1.0, 1.0}))
              << ", (0, 1) " << radiansToDegrees(angleOf(Vec2{0.0, 1.0})) << ", (-1, 0) "
              << radiansToDegrees(angleOf(Vec2{-1.0, 0.0})) << ", (0, -1) "
              << radiansToDegrees(angleOf(Vec2{0.0, -1.0})) << "\n";
    std::cout << "angleBetween in degrees: (1, 0) and (1, 1) "
              << radiansToDegrees(angleBetween(Vec2{1.0, 0.0}, Vec2{1.0, 1.0}))
              << ", (3, 4) and (-4, 3) "
              << radiansToDegrees(angleBetween(Vec2{3.0, 4.0}, Vec2{-4.0, 3.0})) << "\n";

    Image clock(300, 300, Colour{225, 228, 235});
    PointF c{150.0, 150.0};
    Colour dark{40, 40, 55};
    fillCircleAA(clock, c.x, c.y, 130.0, colours::white);
    drawCircleWu(clock, c.x, c.y, 130.0, dark);
    for (int i = 0; i < 60; ++i) {
        double angle = degreesToRadians(i * 6.0 - 90.0);
        if (i % 5 == 0) {
            fillCapsuleAA(clock, pointOnCircle(c, 104.0, angle), pointOnCircle(c, 120.0, angle),
                          3.0, dark);
        } else {
            PointF dotCentre = pointOnCircle(c, 118.0, angle);
            fillCircleAA(clock, dotCentre.x, dotCentre.y, 1.5, Colour{140, 140, 150});
        }
    }
    double minutes = 10.0;
    double hours = 10.0 + minutes / 60.0;
    double hourAngle = degreesToRadians(hours * 30.0 - 90.0);
    double minuteAngle = degreesToRadians(minutes * 6.0 - 90.0);
    fillCapsuleAA(clock, c, pointOnCircle(c, 65.0, hourAngle), 5.0, dark);
    fillCapsuleAA(clock, c, pointOnCircle(c, 100.0, minuteAngle), 3.5, dark);
    fillCircleAA(clock, c.x, c.y, 6.0, Colour{200, 40, 40});

    Image shapes(600, 220, colours::white);
    for (int sides = 3; sides <= 8; ++sides) {
        double x = 50.0 + (sides - 3) * 100.0;
        Colour col = toColour(hsvToRgb(HSV{(sides - 3) * 60.0, 0.7, 0.9}));
        double up = degreesToRadians(-90.0);
        fillPolygonAA(shapes, regularPolygon(PointF{x, 60.0}, 40.0, sides, up), col);
        fillPolygonAA(shapes, starPoints(PointF{x, 165.0}, 45.0, 20.0, sides, up), col);
    }

    Image waves(400, 200, colours::white);
    drawLine(waves, 0, 100, 399, 100, Colour{190, 190, 190});
    std::vector<PointF> sine;
    std::vector<PointF> cosine;
    for (int x = 0; x <= 400; x += 2) {
        double angle = 2.0 * kPi * x / 200.0;
        sine.push_back(PointF{x + 0.5, 100.0 - 60.0 * std::sin(angle)});
        cosine.push_back(PointF{x + 0.5, 100.0 - 60.0 * std::cos(angle)});
    }
    drawPolylineWu(waves, sine, Colour{30, 60, 200});
    drawPolylineWu(waves, cosine, Colour{200, 40, 40});

    Image spiral(300, 300, colours::white);
    PointF previous = c;
    for (int i = 1; i <= 640; ++i) {
        double angle = i * 0.05;
        PointF p = pointOnCircle(c, 4.0 * angle, angle);
        Colour col = toColour(hsvToRgb(HSV{radiansToDegrees(angle), 0.8, 0.85}));
        drawLineWu(spiral, previous, p, col);
        previous = p;
    }

    Image orbits(400, 260, Colour{5, 5, 20});
    const double orbitA[4] = {50.0, 90.0, 130.0, 175.0};
    const double orbitB[4] = {30.0, 55.0, 80.0, 110.0};
    const double planetAngle[4] = {30.0, 150.0, 250.0, 320.0};
    const Colour planetColour[4] = {colours::red, colours::cyan, colours::green, colours::magenta};
    PointF sun{200.0, 130.0};
    for (int k = 0; k < 4; ++k) {
        std::vector<PointF> path;
        for (int i = 0; i <= 120; ++i) {
            path.push_back(pointOnEllipse(sun, orbitA[k], orbitB[k], 2.0 * kPi * i / 120.0));
        }
        drawPolylineWu(orbits, path, Colour{80, 80, 110});
    }
    fillCircleAA(orbits, sun.x, sun.y, 18.0, colours::yellow);
    for (int k = 0; k < 4; ++k) {
        PointF p = pointOnEllipse(sun, orbitA[k], orbitB[k], degreesToRadians(planetAngle[k]));
        fillCircleAA(orbits, p.x, p.y, 6.0, planetColour[k]);
    }

    bool ok = clock.savePPM("clock.ppm");
    ok = ok && shapes.savePPM("shapes.ppm");
    ok = ok && waves.savePPM("waves.ppm");
    ok = ok && spiral.savePPM("spiral.ppm");
    ok = ok && orbits.savePPM("orbits.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
```

Build and run (from the `code/ch30` folder):

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common angles.cpp -o angles
./angles
```

### Line by line

**The numbers (lines 1–31)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–5 | the `#include` lines | `std::sin` and `std::cos`, printing, vectors, our new header, and `hsv.h` for rainbow colours. |
| 8 | `const double table[7] = {0.0, 30.0, 45.0, 60.0, 90.0, 180.0, 360.0};` | The angles of the table in Section 30.3. |
| 10–13 | `for (double d : table) { double r = degreesToRadians(d); std::cout << ... }` | Print each angle in degrees and radians, with its cosine and sine. |
| 14–16 | `double t = degreesToRadians(37.0);` … | Check cos² + sin² = 1 at an "ordinary" angle. |
| 18–22 | `for (int k = 0; k < 5; ++k) { Vec2 v = fromAngle(degreesToRadians(-90.0 + 72.0 * k)); ... }` | The five corners of the Chapter 25 star: start at the top (−90°), steps of 72°. |
| 24–27 | the `angleOf` printing | Four directions and their angles (Section 30.6). |
| 28–31 | the `angleBetween` printing | Two angles between vectors (Section 30.7). |

**The clock (lines 33–54)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 33–35 | `Image clock(...);` / `PointF c{150.0, 150.0};` / `Colour dark{40, 40, 55};` | A light grey picture, its centre, and a dark ink colour. |
| 36–37 | `fillCircleAA(clock, c.x, c.y, 130.0, colours::white);` / `drawCircleWu(...)` | A smooth white face with a smooth outline. |
| 38–39 | `for (int i = 0; i < 60; ++i) { double angle = degreesToRadians(i * 6.0 - 90.0);` | 60 marks, 6° apart, starting at the top. |
| 40–42 | `if (i % 5 == 0) { fillCapsuleAA(clock, pointOnCircle(c, 104.0, angle), pointOnCircle(c, 120.0, angle), 3.0, dark); }` | Every 5th mark (the hours): a short thick capsule pointing to the centre. |
| 43–46 | `} else { PointF dotCentre = pointOnCircle(c, 118.0, angle); fillCircleAA(..., 1.5, ...); }` | The other marks: a small grey dot. |
| 48–51 | `double minutes = 10.0;` … `double minuteAngle = degreesToRadians(minutes * 6.0 - 90.0);` | The time 10:10 and the angles of the two hands (Section 30.11). |
| 52–53 | two `fillCapsuleAA` calls | The hour hand (short and thick) and the minute hand (long and thinner), from the centre. |
| 54 | `fillCircleAA(clock, c.x, c.y, 6.0, Colour{200, 40, 40});` | A red cap over the centre where the hands meet. |

**Polygons and stars (lines 56–63)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 56 | `Image shapes(600, 220, colours::white);` | A wide white picture. |
| 57–58 | `for (int sides = 3; sides <= 8; ++sides) { double x = 50.0 + (sides - 3) * 100.0;` | Six columns, 100 pixels apart. |
| 59 | `Colour col = toColour(hsvToRgb(HSV{(sides - 3) * 60.0, 0.7, 0.9}));` | A different hue for each column. |
| 60 | `double up = degreesToRadians(-90.0);` | Start at the top, so the shapes stand up straight. |
| 61 | `fillPolygonAA(shapes, regularPolygon(PointF{x, 60.0}, 40.0, sides, up), col);` | Top row: a regular polygon with this many sides. |
| 62 | `fillPolygonAA(shapes, starPoints(PointF{x, 165.0}, 45.0, 20.0, sides, up), col);` | Bottom row: a star with this many tips (outer radius 45, inner 20). |

**Waves (lines 65–75)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 65–66 | `Image waves(400, 200, colours::white);` / `drawLine(waves, 0, 100, 399, 100, ...);` | A white picture with a grey middle line. |
| 67–68 | `std::vector<PointF> sine;` / `std::vector<PointF> cosine;` | Two lists of points. |
| 69–70 | `for (int x = 0; x <= 400; x += 2) { double angle = 2.0 * kPi * x / 200.0;` | A point every 2 pixels; one full wave (2π) every 200 pixels. |
| 71–72 | `sine.push_back(PointF{x + 0.5, 100.0 - 60.0 * std::sin(angle)});` / `cosine...` | The wave heights (Section 30.9). The minus turns "maths up" into "screen up". |
| 74–75 | two `drawPolylineWu` calls | Blue sine, red cosine. |

**The spiral (lines 77–85)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 77–78 | `Image spiral(...);` / `PointF previous = c;` | The spiral starts at the centre of the picture (we reuse `c`, which is also (150, 150)). |
| 79–80 | `for (int i = 1; i <= 640; ++i) { double angle = i * 0.05;` | 640 small steps of 0.05 radians (about 3°). |
| 81 | `PointF p = pointOnCircle(c, 4.0 * angle, angle);` | The radius grows with the angle: r = 4θ (Section 30.10). |
| 82 | `Colour col = toColour(hsvToRgb(HSV{radiansToDegrees(angle), 0.8, 0.85}));` | The angle in degrees as the hue. Hues above 360 wrap around (`wrapHue`, Chapter 16), so the rainbow repeats every turn. |
| 83–84 | `drawLineWu(spiral, previous, p, col);` / `previous = p;` | A short smooth line from the last point to this one. |

**The orbits (lines 87–104)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 87–92 | `Image orbits(...);` … `PointF sun{200.0, 130.0};` | The same four orbits and colours as Chapter 23, and an angle for each planet. |
| 93–99 | `for (int k = 0; k < 4; ++k) { std::vector<PointF> path; for (int i = 0; i <= 120; ++i) { path.push_back(pointOnEllipse(...)); } drawPolylineWu(...); }` | Each orbit as 121 points on the parametric ellipse (Section 30.5), drawn as a smooth closed polyline. |
| 100 | `fillCircleAA(orbits, sun.x, sun.y, 18.0, colours::yellow);` | The Sun. |
| 101–104 | `for (int k = 0; k < 4; ++k) { PointF p = pointOnEllipse(sun, orbitA[k], orbitB[k], degreesToRadians(planetAngle[k])); fillCircleAA(...); }` | Each planet at its own angle on its orbit — no square roots needed this time. |

**Saving (lines 106–116)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 106–110 | `bool ok = clock.savePPM("clock.ppm");` … | Save the five pictures. |
| 111–116 | `if (!ok) { ... }` `return 0;` `}` | Report a problem, or finish. |

### What you should see

The program prints the table of Section 30.3, then:

```
cos^2 + sin^2 at 37 degrees = 1
the five star corners of Chapter 25:
  0: (6.12323e-17, -1)
  1: (0.951057, -0.309017)
  2: (0.587785, 0.809017)
  3: (-0.587785, 0.809017)
  4: (-0.951057, -0.309017)
angleOf in degrees: (1, 1) 45, (0, 1) 90, (-1, 0) 180, (0, -1) -90
angleBetween in degrees: (1, 0) and (1, 1) 45, (3, 4) and (-4, 3) 90
```

Open the pictures:
- `clock.ppm`: a smooth clock face showing ten past ten.
- `shapes.ppm`: a triangle, square, pentagon, hexagon, heptagon and octagon in rainbow colours, and below them stars with 3 to 8 tips.
- `waves.ppm`: a blue sine wave and a red cosine wave, each with two full waves, crossing the grey middle line.
- `spiral.ppm`: a rainbow spiral with five evenly spaced turns.
- `orbits.ppm`: smooth elliptical orbits around a yellow Sun, with four coloured planets.

---

## Small examples

### Example 1 — Degrees to radians

> 120° × π / 180 = 2π/3 ≈ **2.094** rad
> 2.5 rad × 180 / π ≈ **143.2°**

### Example 2 — A point on a circle

Centre (100, 100), radius 50, angle 135°:

> cos 135° = −0.7071, sin 135° = 0.7071
> point = (100 − 35.36, 100 + 35.36) = **(64.6, 135.4)** — to the left and **down** (remember: positive angles turn clockwise on the screen)

### Example 3 — The angle of a step

From (10, 10) to (10, 40): the step (0, 30) → atan2(30, 0) = **90°** (straight down).
From (10, 10) to (−20, 10): the step (−30, 0) → atan2(0, −30) = **180°** (left).

### Example 4 — How many sides look like a circle?

A regular polygon with radius 100 and n sides: the biggest gap between a side and the true circle is r × (1 − cos(180° / n)).

> n = 6: 100 × (1 − cos 30°) = 100 × 0.134 = 13.4 pixels — clearly not round
> n = 64: 100 × (1 − cos 2.8°) = 100 × 0.0012 = **0.12** pixels — less than a pixel: it looks like a perfect circle

### Example 5 — Turning a direction

The direction at 20° is (cos 20°, sin 20°) = (0.940, 0.342). Turning it 90° further (clockwise on the screen) gives the direction at 110°: (cos 110°, sin 110°) = (−0.342, 0.940) — exactly `perpendicular` of the first (Chapter 29) ✓

---

## Common mistakes

⚠️ **Giving degrees to `std::sin` / `std::cos`.** They want radians. Convert with `degreesToRadians`.

⚠️ **Forgetting that the screen's y goes down.** 90° points down, angles turn clockwise, and "up" is −90°.

⚠️ **Swapping the arguments of `atan2`.** It is `std::atan2(y, x)` — y first.

⚠️ **Testing a sine or cosine for exactly 0.** Rounding gives numbers like 6e-17. Compare with a small tolerance.

⚠️ **Calling `acos` on a number slightly above 1.** Clamp to [−1, 1] first.

⚠️ **Integer division in angle formulas.** `2 * 3 / 4` with `int`s is 1. Use `2.0 * kPi * i / sides`, where the first number is a `double`.

---

## Practice

🏋️ **1.** Convert 15°, 270° and 720° to radians, and π/12 and 3 radians to degrees.

🏋️ **2.** Without a computer, find cos and sin of 120° and of 300°. (Hint: use the mirror images of 60°.)

🏋️ **3.** Where is the 7 o'clock mark on a clock with centre (150, 150) and radius 120?

🏋️ **4.** Find the angle of the direction (−3, 3) with atan2, and the angle between (2, 0) and (−3, 3).

🏋️ **5.** Draw a "sunburst": 24 capsules from radius 40 to radius 120 around a centre, every 15°, alternating two colours.

🏋️ **6.** Draw a sine wave whose amplitude **shrinks** from 80 at the left to 0 at the right (a "damped" wave, like a guitar string getting quiet).

🏋️ **7.** Draw a **rose curve**: r = 100 × cos(4θ) for θ from 0 to 2π, as a polyline. How many petals does it have?

🏋️ **8.** At what time between 3:00 and 4:00 do the hour hand and the minute hand point in exactly the same direction?

---

## Answers

**1.**
> 15° = π/12 ≈ **0.2618**; 270° = 3π/2 ≈ **4.712**; 720° = 4π ≈ **12.566** (two full turns)
> π/12 rad = **15°**; 3 rad ≈ **171.9°**

**2.**
> 120° is 60° past 90°: the point is the mirror image of the 60° point across the vertical axis: (−0.5, 0.866). So cos 120° = **−0.5**, sin 120° = **0.866**.
> 300° = 360° − 60°: the mirror image of 60° across the horizontal axis: (0.5, −0.866). cos 300° = **0.5**, sin 300° = **−0.866**.

**3.**
> 7 o'clock: 7 × 30° − 90° = **120°**
> (150 + 120 × cos 120°, 150 + 120 × sin 120°) = (150 − 60, 150 + 103.9) = **(90, 253.9)** — left and below the centre ✓

**4.**
> atan2(3, −3) = **135°** (down-left on the screen)
> angle between (2, 0) and (−3, 3): dot = −6, lengths 2 and 4.243 → cos = −6 / 8.485 = −0.7071 → **135°** ✓ (the same, because (2, 0) points at 0°)

**5.**

```cpp
Image sun(300, 300, colours::white);
PointF c{150.0, 150.0};
for (int i = 0; i < 24; ++i) {
    double angle = degreesToRadians(i * 15.0);
    Colour col = (i % 2 == 0) ? Colour{250, 180, 30} : Colour{240, 100, 30};
    fillCapsuleAA(sun, pointOnCircle(c, 40.0, angle), pointOnCircle(c, 120.0, angle), 5.0, col);
}
fillCircleAA(sun, c.x, c.y, 35.0, Colour{250, 200, 40});
```

**6.**

```cpp
std::vector<PointF> damped;
for (int x = 0; x <= 400; x += 2) {
    double amplitude = 80.0 * (1.0 - x / 400.0);
    double angle = 2.0 * kPi * x / 50.0;
    damped.push_back(PointF{x + 0.5, 100.0 - amplitude * std::sin(angle)});
}
drawPolylineWu(img, damped, colours::black);
```

The amplitude goes down in a straight line from 80 to 0 (lerp, Chapter 13). (A real string fades faster at first and then slower — that needs the "exponential" curve, which we do not use yet.)

**7.**

```cpp
std::vector<PointF> rose;
for (int i = 0; i <= 720; ++i) {
    double angle = 2.0 * kPi * i / 720.0;
    double r = 100.0 * std::cos(4.0 * angle);
    rose.push_back(pointOnCircle(PointF{150.0, 150.0}, r, angle));
}
drawPolylineWu(img, rose, Colour{200, 40, 120});
```

It has **8** petals. (When r is negative, `pointOnCircle` puts the point on the opposite side of the centre, which draws extra petals. For r = cos(kθ): k odd gives k petals, k even gives 2k petals.)

**8.** At m minutes after 3:00, the minute hand is at 6m degrees (after 12), and the hour hand at 90 + 0.5m degrees (it moves 30° per 60 minutes, so 0.5° per minute). They meet when:

> 6m = 90 + 0.5m → 5.5m = 90 → m = 90 / 5.5 ≈ **16.36** minutes → about **3:16:22**

---

## Summary

🧠 A full turn is **360°** or **2π radians**. **radians = degrees × π / 180**. `std::sin` and `std::cos` use **radians**.

🧠 The point at angle θ on the unit circle is **(cos θ, sin θ)**. Always: **cos²θ + sin²θ = 1**.

🧠 Key values: cos 0 = 1, cos 90° = 0, cos 60° = 0.5, cos 45° = sin 45° = 0.7071, sin 60° = cos 30° = 0.866.

🧠 On the screen (y down), 0° is right, **90° is down**: angles turn **clockwise**. Start at **−90°** for "up".

🧠 Circle: **C + r(cos θ, sin θ)**. Ellipse: **(cx + a cos θ, cy + b sin θ)**.

🧠 The angle of a vector: **atan2(y, x)**. The angle between two vectors: **acos(a·b / (|a||b|))** (clamped).

🧠 Regular polygon: corners every **360°/n**. A star without crossings: 2n points, alternating outer and inner radius, every 180°/n.

🧠 Wave: y = middle − amplitude × sin(2π x / period).

---

## Next chapter

We can now place points anywhere with angles. The next step is to **move whole shapes**: shift them, make them bigger or smaller, and **turn** them around a point. In Chapter 31 we learn the three basic **transformations** — translate, scale and rotate — and the rotation formula (x cos θ − y sin θ, x sin θ + y cos θ), which we will build from the unit circle. And at last we will draw the **tilted** ellipse promised in Chapter 23.
