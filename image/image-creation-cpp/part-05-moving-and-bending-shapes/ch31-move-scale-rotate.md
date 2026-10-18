# Chapter 31 — Move, Scale, Rotate

> **Part 5 · Chapter 31 of 82**
> **You need:** Chapters 1–30 (especially 23, 27, 29 and 30) · **You will make:** `transform.h` (moving, scaling, mirroring and turning points and shapes, and smooth tilted ellipses), `fan.ppm`, `flower.ppm`, `compare.ppm`, `figures.ppm` and `trail.ppm`

---

## What you will learn

- Why moving a shape is the same as moving its **corner points**.
- The three basic **transformations**: **translate** (move), **scale** (make bigger or smaller) and **rotate** (turn).
- How to scale **about a centre**, how to stretch in only one direction, and how a **negative** scale makes a **mirror image**.
- The **rotation formula** (x cos θ − y sin θ, x sin θ + y cos θ), built step by step from the unit circle.
- Why turning never changes lengths.
- How to turn a shape around **any point**, not just (0, 0).
- Why the **order** of transformations matters.
- How to draw the **tilted ellipse** promised in Chapter 23, in two ways: as a polygon, and with a smooth pixel test that **undoes the turn**.
- How to find the exact box around a tilted ellipse.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **transformation** | A rule that moves every point of a picture to a new place. |
| **translate** | Move (slide) everything by the same step, without turning or stretching. |
| **scale** | Make everything bigger or smaller, measured from a centre point. |
| **uniform scale** | The same scale across and down: the shape keeps its proportions. |
| **non-uniform scale** | Different scales across and down: the shape gets stretched or squashed. |
| **mirror** (reflection) | A flip, as in a mirror: left becomes right (or top becomes bottom). |
| **rotate** | Turn everything around a centre point by an angle. |
| **origin** | The point (0, 0). |
| **pivot** | The point a shape turns (or scales) around. |
| **local coordinates** | Coordinates measured from a shape's own "home" point, not from the corner of the picture. |
| **inverse** | The transformation that undoes another one. |

---

## 31.1 Moving a shape means moving its points

📖 **New word: transformation** — a rule that takes **every** point and gives it a new place.

Look at how we describe our shapes:

- a polygon is a **list of corner points** (Chapter 25);
- a triangle is **three points** (Chapter 24);
- a line is **two points** (Chapter 20);
- a circle is a **centre** and a radius (Chapter 22).

So we never need to move pixels around. To move, grow or turn a shape, we change its **points**, and then draw it again from the new points. The drawing functions of Part 4 do the rest.

```
   the points before:            the points after a move by (6, 1):
   (1, 1) (4, 1) (4, 3) (1, 3)   (7, 2) (10, 2) (10, 4) (7, 4)

   ●────●                              
   │    │                                   ●────●
   ●────●                                   │    │
                                            ●────●
```

💡 This works for **straight** edges because each of our transformations (in this chapter) turns straight lines into straight lines. Moving the two ends of a straight edge moves the whole edge. So "transform the corners, then join them" gives exactly the transformed shape.

All our points are `Vec2` (which is the same as `PointF`, Chapter 29). Every transformation in this chapter is a small function that takes a `Vec2` and returns a new `Vec2`.

---

## 31.2 Translate: slide everything

📖 **New word: translate** — move everything by the **same** step. Nothing turns, nothing stretches.

The step is a vector t = (tx, ty) (Chapter 29: a vector is a step). Each point just takes that step:

> **translate(p) = p + t = (x + tx, y + ty)**

🔢 **Maths: translate (3, 1) by (10, 5)**

> (3 + 10, 1 + 5) = **(13, 6)**

The program prints `translate (3, 1) by (10, 5): (13, 6)`.

🔢 **Maths: translating a square**

> corners (1, 1), (4, 1), (4, 3), (1, 3), step (6, 1)
> → (7, 2), (10, 2), (10, 4), (7, 4)
> The width is still 4 − 1 = 10 − 7 = 3, and the height still 3 − 1 = 4 − 2 = 2 ✓

To **undo** a translate by t, translate by **−t**.

---

## 31.3 Scale: bigger and smaller

📖 **New word: scale** — make everything bigger or smaller.

### Scaling about the origin

📖 **New word: origin** — the point (0, 0).

The simplest scale multiplies each coordinate by a number s:

> **scale(p) = s × p = (s × x, s × y)**

🔢 **Maths: scale the square (1, 1), (4, 1), (4, 3), (1, 3) by 2**

> → (2, 2), (8, 2), (8, 6), (2, 6)
> The width doubles: 3 → 6 ✓. The height doubles: 2 → 4 ✓.
> But look: the square has also **moved** — its top-left corner went from (1, 1) to (2, 2).

Why did it move? Because each point's distance **from the origin** was doubled. The origin is the only point that stays where it is. On our screen the origin is the top-left corner of the picture, so scaling "about the origin" pushes everything away from that corner (or pulls it toward the corner, if s < 1).

### Scaling about a centre

📖 **New word: pivot** — the point that stays still while everything else scales (or turns) around it.

Usually we want a shape to grow **around its own centre** (or around its base, or one corner). Call that pivot C. The idea, in three steps:

1. Find the step **from C to the point**: p − C.
2. Scale that step: s × (p − C).
3. Take the scaled step **from C** again: C + s × (p − C).

> **scaleAbout(p) = C + s × (p − C)**

The pivot itself does not move: if p = C, then p − C = (0, 0), and the result is C.

🔢 **Maths: scale (4, 6) by 2 about (2, 2)**

> p − C = (4 − 2, 6 − 2) = (2, 4)
> × 2 = (4, 8)
> C + (4, 8) = **(6, 10)**

The program prints `scale (4, 6) by 2 about (2, 2): (6, 10)`.

🔢 **Maths: scale the square around its centre**

> The square (1, 1), (4, 1), (4, 3), (1, 3) has its centre at (2.5, 2).
> Corner (1, 1): step from the centre (−1.5, −1) → × 2 = (−3, −2) → (−0.5, 0)
> Corner (4, 3): step (1.5, 1) → × 2 = (3, 2) → (5.5, 4)
> The new square goes from (−0.5, 0) to (5.5, 4): 6 wide, 4 high, and its centre is still (2.5, 2) ✓

### Different scales across and down

📖 **New word: uniform scale** — the same number across and down. Shapes keep their **proportions** (a circle stays a circle).

📖 **New word: non-uniform scale** — different numbers: sx across, sy down. Shapes get **stretched** or **squashed**:

> **scaleAbout(p) = (Cx + sx × (x − Cx), Cy + sy × (y − Cy))**

This is how Chapter 23 made an ellipse: it took the unit circle and scaled it by a across and b down.

### Negative scales: mirrors

📖 **New word: mirror** — a flip. With sx = **−1** (and sy = 1), every point's step from the pivot is turned **backwards** across: what was 3 to the right of the pivot is now 3 to the left.

🔢 **Maths: mirror (5, 3) across the upright line x = 2**

> Use the pivot (2, 0) with sx = −1, sy = 1 (the y of the pivot does not matter, because sy = 1).
> x: 2 + (−1) × (5 − 2) = 2 − 3 = **−1**
> y: 0 + 1 × (3 − 0) = **3**
> → **(−1, 3)**: the point was 3 to the right of the line, now it is 3 to the left ✓

The program prints `mirror (5, 3) about x = 2: (-1, 3)`.

- sx = −1, sy = 1: a left–right mirror (across an **upright** line).
- sx = 1, sy = −1: an upside-down mirror (across a **level** line).
- sx = −1, sy = −1: both at once — we will see in Section 31.6 that this is the same as a **half turn**.

⚠️ A mirror turns a clockwise polygon into a counter-clockwise one (the order of its corners now goes the other way round). Our scanline fill with the non-zero rule (Chapter 25) does not care, so `fillPolygonAA` still fills it. (Chapter 24's `fillTriangle` also does not care: it swaps two corners when the area is negative.)

⚠️ A scale of **0** squashes everything onto the pivot (or onto a line, if only one of sx and sy is 0). The shape has no area left and nothing is drawn.

To **undo** a scale by s, scale by **1 / s** about the same pivot (impossible if s = 0 — squashed shapes cannot be un-squashed).

---

## 31.4 Rotate: the big formula, step by step

📖 **New word: rotate** — turn everything around a pivot by an angle θ.

We start with the pivot at the **origin**. We want a formula: given a point (x, y) and an angle θ, where does the point go?

### Step 1: turn the point (1, 0)

This is just Chapter 30. (1, 0) is the point at angle 0° on the unit circle. Turning it by θ puts it at angle θ:

> (1, 0) → **(cos θ, sin θ)**

### Step 2: turn the point (0, 1)

(0, 1) is the point at angle 90° on the unit circle. Turning it by θ puts it at angle 90° + θ:

> (0, 1) → (cos(90° + θ), sin(90° + θ))

Chapter 30 (Section 30.4) showed that this is the **perpendicular** of (cos θ, sin θ):

> (cos(90° + θ), sin(90° + θ)) = **(−sin θ, cos θ)**

That makes sense: (0, 1) is the perpendicular of (1, 0) (a quarter turn further), and after turning both by θ, the second is still a quarter turn further than the first.

🔢 **Maths: check with θ = 90°**

> (1, 0) → (cos 90°, sin 90°) = (0, 1) ✓ (right turns into down: a clockwise quarter turn on the screen)
> (0, 1) → (−sin 90°, cos 90°) = (−1, 0) ✓ (down turns into left)

### Step 3: any point is made of (1, 0) and (0, 1)

Chapter 29 taught us that a vector is a step, and steps can be added and scaled. The point (x, y) is the step "x times (1, 0), plus y times (0, 1)":

> (x, y) = **x × (1, 0) + y × (0, 1)**

For example, (3, 1) = 3 × (1, 0) + 1 × (0, 1) = (3, 0) + (0, 1) ✓.

Now imagine this "walk" — x steps to the right, then y steps down — drawn on a sheet of paper, and **turn the whole sheet** by θ. The walk does not change: it is still x steps along one direction, then y steps along the other. Only the two directions have turned:

- "right" (1, 0) has become (cos θ, sin θ),
- "down" (0, 1) has become (−sin θ, cos θ).

So the turned point is:

> x × (cos θ, sin θ) + y × (−sin θ, cos θ)

Add the two parts (x part plus x part, y part plus y part):

> **rotate(x, y) = (x cos θ − y sin θ, x sin θ + y cos θ)**

That is the rotation formula. It is one of the most used formulas in all of computer graphics, so it is worth remembering how we built it: **where does (1, 0) go, where does (0, 1) go, then mix them with x and y.** (In Chapter 32 this same idea becomes a **matrix**.)


🔢 **Maths: rotate (3, 1) by 90°**

> cos 90° = 0, sin 90° = 1
> x' = 3 × 0 − 1 × 1 = **−1**
> y' = 3 × 1 + 1 × 0 = **3**
> → **(−1, 3)**

The program prints `rotate (3, 1) by 90 degrees: (-1, 3)`. (Funny: the mirror in Section 31.3 also gave (−1, 3). Two different transformations can send one particular point to the same place. They are still different: try them on another point.)

💡 A quarter turn clockwise on the screen sends (x, y) to (−y, x). That is exactly `perpendicular` from Chapter 29 ✓.

🔢 **Maths: rotate (2, 1) by 30°**

> cos 30° = 0.8660, sin 30° = 0.5
> x' = 2 × 0.8660 − 1 × 0.5 = 1.7321 − 0.5 = **1.2321**
> y' = 2 × 0.5 + 1 × 0.8660 = 1 + 0.8660 = **1.8660**

The program prints `rotate (2, 1) by 30 degrees: (1.23205, 1.86603)`.

### In code

```cpp
inline Vec2 rotate(Vec2 p, double radians) {
    double c = std::cos(radians);
    double s = std::sin(radians);
    return Vec2{p.x * c - p.y * s, p.x * s + p.y * c};
}
```

We work out the cosine and sine **once** and keep them in `c` and `s`, then use each one twice.

---

## 31.5 Turning never changes lengths

When you turn a sheet of paper, the drawing on it does not get bigger or smaller. So rotation should keep every **length** the same. Let us check it with Pythagoras (Chapter 22).

🔢 **Maths: the length of the turned point**

> x' = x cos θ − y sin θ, y' = x sin θ + y cos θ
> x'² = x² cos²θ − 2xy sin θ cos θ + y² sin²θ
> y'² = x² sin²θ + 2xy sin θ cos θ + y² cos²θ
> Add them. The two middle parts cancel (one is minus, one is plus):
> x'² + y'² = x² (cos²θ + sin²θ) + y² (sin²θ + cos²θ)
> = x² × 1 + y² × 1 (the circle rule of Chapter 30: cos²θ + sin²θ = 1)
> = **x² + y²** ✓

The distance from the origin is the same before and after. The program checks it with (3, 4), whose length is 5, turned by 37°:

```
length of (3, 4) before and after a 37 degree turn: 5, 5
```

And because rotation turns every step between two points by the same angle, the **distance between any two points** stays the same too, and so do the **angles** between edges. A turned square is still a square of the same size.

To **undo** a rotation by θ, rotate by **−θ**.

---

## 31.6 Rotating around any pivot

Our formula turns everything around the **origin** — the top-left corner of the picture. That is almost never what we want: a spinning wheel should turn around its own **hub**.

The trick is the same as for scaling about a centre (Section 31.3):

1. Take the step from the pivot C to the point: p − C. (Now the pivot is "at the origin".)
2. Turn that step: rotate(p − C, θ).
3. Add the pivot back: C + rotate(p − C, θ).

> **rotateAbout(p) = C + rotate(p − C, θ)**

Another way to say it: **move the pivot to the origin, turn, move back.**

🔢 **Maths: rotate (5, 2) by 90° about (2, 2)**

> p − C = (3, 0)
> rotate by 90°: (3 × 0 − 0 × 1, 3 × 1 + 0 × 0) = (0, 3)
> C + (0, 3) = **(2, 5)**

The point was 3 to the **right** of the pivot; after a clockwise quarter turn on the screen it is 3 **below** the pivot ✓. The program prints `rotate (5, 2) by 90 degrees about (2, 2): (2, 5)`.

🔢 **Maths: a half turn is a double mirror**

> rotate by 180°: cos 180° = −1, sin 180° = 0
> (x cos θ − y sin θ, x sin θ + y cos θ) = (−x, −y)
> That is exactly a scale by sx = −1, sy = −1 ✓ (Section 31.3)

### Local coordinates

📖 **New word: local coordinates** — coordinates measured from a shape's own home point (its pivot), not from the corner of the picture.

A very handy way to work: describe the shape with **its pivot at (0, 0)**. Then turning it is just `rotate` (no pivot needed), and placing it in the picture is just a translate. Our program does this for the house and the star:

```
   the house in local coordinates          (0, −100) = the top of the roof
   (y is negative = above the ground):
                 ╱╲  ▐▌
               ╱    ╲▐▌
             ╱________╲
              │        │
              │        │
         (−40, 0) ●(0, 0) (40, 0)          (0, 0) = the middle of the bottom edge
```

---

## 31.7 On our screen, positive angles turn clockwise

Everything in Chapter 30 (Section 30.4) carries over. Our formula is the same one used in maths books, but our y goes **down**, so:

- a **positive** θ turns shapes **clockwise** on the screen;
- a **negative** θ turns them **counter-clockwise**.


🔢 **Maths: rotate the "up" arrow (0, −10) by +90°**

> (0 × 0 − (−10) × 1, 0 × 1 + (−10) × 0) = **(10, 0)**: it now points **right**.
> Up → right is a clockwise quarter turn ✓ (like a clock hand going from 12 to 3).

---

## 31.8 The order matters

With two transformations, does it matter which comes first? Try it with the point (1, 0), a turn of 90° (about the origin) and a move by (10, 0).

🔢 **Maths: turn first, then move**

> rotate (1, 0) by 90° → (0, 1)
> move by (10, 0) → **(10, 1)**

🔢 **Maths: move first, then turn**

> move (1, 0) by (10, 0) → (11, 0)
> rotate (11, 0) by 90° → **(0, 11)**

The program prints:

```
(1, 0): rotate 90, then move by (10, 0): (10, 1)
(1, 0): move by (10, 0), then rotate 90: (6.73556e-16, 11)
```

(6.73556e-16 is "0 with a tiny rounding error", as in Chapter 30 Section 30.3: cos 90° is not stored exactly.)

**Completely different answers!** Here is the picture in words:

- **Turn, then move:** the shape spins **in place** (around the origin, where it is), and then slides to its new place. This is what you usually want: "spin the star, then put it there".
- **Move, then turn:** the shape first slides away from the origin, and then the turn swings it **around the origin**, like a stone on a string. It ends up somewhere else entirely — here 11 pixels below the top-left corner of the picture instead of 10 pixels to the right.

🧠 **Remember:** for a shape in local coordinates, the usual order is **scale, then rotate, then translate**. Scale and rotate while the pivot is still at (0, 0); move it into place last.

Some pairs do not care about order: two moves (a + b = b + a), two turns about the same pivot (θ1 + θ2 either way), or a turn and a uniform scale about the same pivot. But in general, order matters — and Chapter 33 is all about combining transformations safely.

---

## 31.9 The tilted ellipse, way 1: transform its points

Chapter 23 drew ellipses whose axes are level and upright, and said: "A tilted ellipse needs rotation, which we learn in Chapter 31." Here it is.

Chapter 30 gave us points on an ellipse with its centre at (0, 0):

> (a cos t, b sin t), for t from 0 to 2π

(We call the moving number **t** here, because θ is now the **tilt**.) To tilt this ellipse by θ and put it at the centre C, use **local coordinates** (Section 31.6): turn, then move:

> **point(t) = C + rotate((a cos t, b sin t), θ)**

Collect, say, 100 such points into a list: that is a **polygon** with 100 corners, and Part 4 can fill it smoothly with `fillPolygonAA` (Chapter 27), or draw its outline with `drawPolylineWu` (Chapter 28).

```cpp
inline std::vector<PointF> tiltedEllipsePoints(PointF centre, double a, double b, double radians,
                                               int count) {
    std::vector<PointF> points;
    for (int i = 0; i < count; ++i) {
        double t = 2.0 * kPi * i / count;
        Vec2 p{a * std::cos(t), b * std::sin(t)};
        points.push_back(centre + rotate(p, radians));
    }
    return points;
}
```

### How many points?

A polygon only touches the true curve at its corners. Between corners, its straight sides cut a little inside. With **many** corners, nobody can see the difference.

🔢 **Maths: the area lost by the polygon**

> A polygon with n corners at t = 0, 2π/n, 4π/n, … on an ellipse has area (n / 2) × a × b × sin(2π / n). The true ellipse has area π a b (Chapter 23).
> a = 80, b = 35, n = 100: 50 × 2800 × sin(3.6°) = 50 × 2800 × 0.06279 = **8790.5**; the ellipse: π × 2800 = **8796.5**. The polygon misses only 6 pixels' worth of area, spread along the whole edge — invisible.
> n = 12: 6 × 2800 × sin 30° = **8400** — 4.5 % less, and the 12 corners are easy to see.

`compare.ppm` shows a filled 100-point polygon on the left, and on the right the smooth ellipse of Section 31.12 with a red 12-point outline on top of it, so you can see how a polygon with few corners cuts inside the curve.

---

## 31.10 The tilted ellipse, way 2: undo the turn

📖 **New word: inverse** — the transformation that **undoes** another one. The inverse of "turn by θ" is "turn by −θ"; the inverse of "move by t" is "move by −t".

Way 1 builds the outline. But for a **pixel test** (like Chapter 22's circle test or Chapter 23's ellipse test), we need to answer: "is this pixel centre **inside** the tilted ellipse?"

Here is the clever idea. Tilt your head!

- The tilted ellipse is the normal (level) ellipse turned by θ around its centre C.
- So a point p is inside the tilted ellipse **exactly when** turning p back by **−θ** around C lands it inside the normal ellipse.

```
   tilted ellipse, and a pixel ●       turn everything back by −θ:
                                        the ellipse is level again,
         ╱‾‾‾╲                          and the pixel has moved with it
        ╱  ●  ╲                              ___________
       ╱      ╱                            (     ●     )
       ╲____╱                               ‾‾‾‾‾‾‾‾‾‾‾
```

So the test is:

1. q = rotate(p − C, −θ) — the step from the centre, turned back;
2. inside if **(q.x / a)² + (q.y / b)² ≤ 1** — the normal ellipse test (Chapter 23, written with divisions).

```cpp
inline bool insideTiltedEllipse(Vec2 p, PointF centre, double a, double b, double radians) {
    Vec2 q = rotate(p - centre, -radians);
    return (q.x / a) * (q.x / a) + (q.y / b) * (q.y / b) <= 1.0;
}
```

🔢 **Maths: a = 60, b = 20, tilted 30°, centre (0, 0) — is (47, 27) inside?**

> Turn back by −30°: cos(−30°) = 0.8660, sin(−30°) = −0.5
> q.x = 47 × 0.8660 − 27 × (−0.5) = 40.70 + 13.5 = 54.20
> q.y = 47 × (−0.5) + 27 × 0.8660 = −23.5 + 23.38 = −0.12
> (54.20 / 60)² + (−0.12 / 20)² = 0.816 + 0.00004 = **0.816 ≤ 1** → inside ✓

The point (47, 27) lies almost exactly along the long, tilted axis, so it is inside even though it is 47 pixels across.

🔢 **Maths: is (55, 0) inside?**

> q.x = 55 × 0.8660 − 0 = 47.63
> q.y = 55 × (−0.5) + 0 = −27.5
> (47.63 / 60)² + (−27.5 / 20)² = 0.630 + 1.891 = **2.52 > 1** → outside ✓

A level ellipse with a = 60 would contain (55, 0). But this one is tilted by +30°, which on our screen means its long axis points **down**-right (positive angles turn clockwise). At x = 55 the long axis is already about 55 × tan 30° ≈ 32 pixels down, and the ellipse is thin, so the point (55, 0) is far above it. The program prints `is (47, 27) inside it? yes, is (55, 0)? no`.

💡 This "undo the transformation, then use the simple test" idea is one of the most powerful tricks in graphics. We will use it again and again: to rotate whole **images** (Chapter 33), to resize them (Chapter 35), and in ray tracing (Part 10).

---

## 31.11 The box around a tilted ellipse

To fill a shape with pixel tests, we only test the pixels in a **box** around it (Chapter 22). For a level ellipse, the box is easy: from cx − a to cx + a across, and cy − b to cy + b down. For a tilted one?

A lazy answer: use a square box of half-size max(a, b). It always works, but it tests many pixels for nothing — for a thin ellipse lying at 45°, about half of them (Practice 7).

A better answer, with the dot product. The across-part of a point on the tilted ellipse (from its centre) is:

> x(t) = a cos t × cos θ − b sin t × sin θ

Look closely: this is a **dot product** (Chapter 29) of two vectors:

> x(t) = (a cos θ, −b sin θ) · (cos t, sin t)

The second vector, (cos t, sin t), is a **unit** vector (length 1, Chapter 30). And a dot product with a unit vector is biggest when the unit vector points the **same way** as the other vector — and then it equals that vector's **length** (Chapter 29: a · b = |a| × |b| × cos(angle), and cos 0° = 1). So the biggest x is:

> **half width = √(a² cos²θ + b² sin²θ)**

In the same way, y(t) = a cos t × sin θ + b sin t × cos θ = (a sin θ, b cos θ) · (cos t, sin t), so:

> **half height = √(a² sin²θ + b² cos²θ)**

🔢 **Maths: a = 60, b = 20, θ = 30°**

> cos²30° = 0.75, sin²30° = 0.25
> half width = √(3600 × 0.75 + 400 × 0.25) = √(2700 + 100) = √2800 = **52.92**
> half height = √(3600 × 0.25 + 400 × 0.75) = √(900 + 300) = √1200 = **34.64**

Rounded outward to whole pixels (floor for the start, ceil for the end), the box is from (−53, −35) to (53, 35). The program prints `box of a = 60, b = 20 tilted 30 degrees: -53, -35 to 53, 35`. (The lazy square box would go from −60 to 60 both ways: 120 × 120 = 14,400 pixels instead of 106 × 70 = 7,420.)

🔢 **Maths: checks**

> θ = 0°: half width = √(a²) = a, half height = b ✓ (the level ellipse)
> θ = 90°: half width = b, half height = a ✓ (the ellipse stands upright)
> a = b = r (a circle): both are √(r²(cos²θ + sin²θ)) = r ✓ (turning a circle changes nothing)

---

## 31.12 A smooth tilted ellipse

Now we put it all together, the Chapter 27 way: for each pixel in the box, test 4 × 4 = 16 sample points, count how many are inside, and paint with that **coverage**.

One small speed-up: turning back by −θ needs cos(−θ) and sin(−θ). Because cos(−θ) = cos θ and sin(−θ) = −sin θ (the point at angle −θ on the unit circle is the mirror image of the point at angle θ, across the level line: the same x, the opposite y), we can write the turn-back with the **same** c = cos θ and s = sin θ:

> u = dx × c − dy × (−s) = **dx × c + dy × s**
> v = dx × (−s) + dy × c = **−dx × s + dy × c**

where (dx, dy) is the step from the centre to the sample. Then we test (u / a)² + (v / b)² ≤ 1. We work out c and s once per pixel, not 16 times.

`flower.ppm` uses this: eight petals, each a tilted ellipse (a = 70, b = 24). Petal i has its centre 70 pixels from the middle of the picture, at angle i × 45°, and is **tilted by the same angle**, so its long axis points straight out from the middle. Its inner tip touches the middle, and its outer tip is 140 pixels out.

---

## Code, part 1: `transform.h`

File: `common/transform.h` (new). It includes `angles.h`.

```cpp
#ifndef TRANSFORM_H
#define TRANSFORM_H

#include <cmath>
#include <vector>
#include "angles.h"

inline Vec2 translate(Vec2 p, Vec2 offset) {
    return p + offset;
}

inline Vec2 scaleAbout(Vec2 p, Vec2 centre, double sx, double sy) {
    return Vec2{centre.x + sx * (p.x - centre.x), centre.y + sy * (p.y - centre.y)};
}

inline Vec2 rotate(Vec2 p, double radians) {
    double c = std::cos(radians);
    double s = std::sin(radians);
    return Vec2{p.x * c - p.y * s, p.x * s + p.y * c};
}

inline Vec2 rotateAbout(Vec2 p, Vec2 centre, double radians) {
    return centre + rotate(p - centre, radians);
}

inline std::vector<PointF> translatePoints(const std::vector<PointF>& points, Vec2 offset) {
    std::vector<PointF> result;
    for (PointF p : points) {
        result.push_back(translate(p, offset));
    }
    return result;
}

inline std::vector<PointF> scalePoints(const std::vector<PointF>& points, Vec2 centre, double sx,
                                       double sy) {
    std::vector<PointF> result;
    for (PointF p : points) {
        result.push_back(scaleAbout(p, centre, sx, sy));
    }
    return result;
}

inline std::vector<PointF> rotatePoints(const std::vector<PointF>& points, Vec2 centre,
                                        double radians) {
    std::vector<PointF> result;
    for (PointF p : points) {
        result.push_back(rotateAbout(p, centre, radians));
    }
    return result;
}

inline std::vector<PointF> tiltedEllipsePoints(PointF centre, double a, double b, double radians,
                                               int count) {
    std::vector<PointF> points;
    for (int i = 0; i < count; ++i) {
        double t = 2.0 * kPi * i / count;
        Vec2 p{a * std::cos(t), b * std::sin(t)};
        points.push_back(centre + rotate(p, radians));
    }
    return points;
}

inline bool insideTiltedEllipse(Vec2 p, PointF centre, double a, double b, double radians) {
    Vec2 q = rotate(p - centre, -radians);
    return (q.x / a) * (q.x / a) + (q.y / b) * (q.y / b) <= 1.0;
}

inline double tiltedEllipseCoverage(PointF centre, double a, double b, double radians, int x, int y,
                                    int n) {
    double c = std::cos(radians);
    double s = std::sin(radians);
    int inside = 0;
    for (int j = 0; j < n; ++j) {
        for (int i = 0; i < n; ++i) {
            double dx = x + sampleOffset(i, n) - centre.x;
            double dy = y + sampleOffset(j, n) - centre.y;
            double u = dx * c + dy * s;
            double v = -dx * s + dy * c;
            if ((u / a) * (u / a) + (v / b) * (v / b) <= 1.0) {
                ++inside;
            }
        }
    }
    return static_cast<double>(inside) / (n * n);
}

inline Rect tiltedEllipseBox(PointF centre, double a, double b, double radians) {
    double c = std::cos(radians);
    double s = std::sin(radians);
    double halfWidth = std::sqrt(a * a * c * c + b * b * s * s);
    double halfHeight = std::sqrt(a * a * s * s + b * b * c * c);
    int x0 = static_cast<int>(std::floor(centre.x - halfWidth));
    int y0 = static_cast<int>(std::floor(centre.y - halfHeight));
    int x1 = static_cast<int>(std::ceil(centre.x + halfWidth));
    int y1 = static_cast<int>(std::ceil(centre.y + halfHeight));
    return Rect{x0, y0, x1, y1};
}

inline void fillTiltedEllipseAA(Image& image, PointF centre, double a, double b, double radians,
                                Colour c, int n = 4) {
    if (a <= 0.0 || b <= 0.0 || n < 1) {
        return;
    }
    Rect box = clipToImage(tiltedEllipseBox(centre, a, b, radians), image);
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            paintCoverage(image, x, y, c, tiltedEllipseCoverage(centre, a, b, radians, x, y, n));
        }
    }
}

#endif
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef TRANSFORM_H` / `#define TRANSFORM_H` | Include guard. |
| 4–5 | `#include <cmath>` / `#include <vector>` | `std::cos`, `std::sin`, `std::sqrt`, `std::floor`, `std::ceil`; lists of points. |
| 6 | `#include "angles.h"` | `kPi`, `Vec2` and its operators, and the whole drawing library. |
| 8–10 | `inline Vec2 translate(Vec2 p, Vec2 offset) { return p + offset; }` | Move a point by a step (Section 31.2). |
| 12–14 | `inline Vec2 scaleAbout(Vec2 p, Vec2 centre, double sx, double sy) { return Vec2{centre.x + sx * (p.x - centre.x), centre.y + sy * (p.y - centre.y)}; }` | C + s × (p − C), with separate scales across and down (Section 31.3). Use sx = sy for a uniform scale, and −1 for a mirror. |
| 16 | `inline Vec2 rotate(Vec2 p, double radians) {` | Turn a point around the **origin** (Section 31.4). The angle is in radians. |
| 17–18 | `double c = std::cos(radians);` / `double s = std::sin(radians);` | Cosine and sine, worked out once. |
| 19–20 | `return Vec2{p.x * c - p.y * s, p.x * s + p.y * c};` `}` | (x cos θ − y sin θ, x sin θ + y cos θ). |
| 22–24 | `inline Vec2 rotateAbout(Vec2 p, Vec2 centre, double radians) { return centre + rotate(p - centre, radians); }` | Move the pivot to the origin, turn, move back (Section 31.6). |
| 26 | `inline std::vector<PointF> translatePoints(const std::vector<PointF>& points, Vec2 offset) {` | Move a whole shape (a list of points). The list is passed by `const` reference: we read it without copying it, and we do not change it. |
| 27–32 | `std::vector<PointF> result; for (PointF p : points) { result.push_back(translate(p, offset)); } return result; }` | A **new** list with every point moved. The original shape stays as it was, so we can use it again (the program draws one house four times). |
| 34–41 | `inline std::vector<PointF> scalePoints(...)` | The same, with `scaleAbout`. |
| 43–50 | `inline std::vector<PointF> rotatePoints(...)` | The same, with `rotateAbout`. |
| 52–53 | `inline std::vector<PointF> tiltedEllipsePoints(PointF centre, double a, double b, double radians, int count) {` | The outline of a tilted ellipse as `count` points (Section 31.9). |
| 54–56 | `std::vector<PointF> points; for (int i = 0; i < count; ++i) { double t = 2.0 * kPi * i / count;` | Equal steps of t all around: 0, 2π/count, … The last point is just before 2π, because the fill closes the polygon by itself (Chapter 25). |
| 57 | `Vec2 p{a * std::cos(t), b * std::sin(t)};` | A point on the **level** ellipse, in local coordinates (centre at (0, 0)). |
| 58 | `points.push_back(centre + rotate(p, radians));` | Turn it (around its own centre, which is still the origin), then move it into place: **turn first, then move** (Section 31.8). |
| 59–61 | `}` `return points;` `}` | Done. |
| 63 | `inline bool insideTiltedEllipse(Vec2 p, PointF centre, double a, double b, double radians) {` | The teaching version of the pixel test (Section 31.10). |
| 64 | `Vec2 q = rotate(p - centre, -radians);` | The step from the centre, turned **back** by −θ. |
| 65–66 | `return (q.x / a) * (q.x / a) + (q.y / b) * (q.y / b) <= 1.0;` `}` | The normal ellipse test. |
| 68–69 | `inline double tiltedEllipseCoverage(PointF centre, double a, double b, double radians, int x, int y, int n) {` | How much of pixel (x, y) is inside the tilted ellipse, from 0 to 1, using n × n samples (Chapter 27). |
| 70–71 | `double c = std::cos(radians);` / `double s = std::sin(radians);` | Once per pixel. |
| 72–74 | `int inside = 0; for (int j = 0; j < n; ++j) { for (int i = 0; i < n; ++i) {` | Count the samples that are inside. |
| 75–76 | `double dx = x + sampleOffset(i, n) - centre.x;` / `double dy = ...` | The step from the centre to this sample point (sample positions from Chapter 27). |
| 77–78 | `double u = dx * c + dy * s;` / `double v = -dx * s + dy * c;` | The step turned back by −θ, written with cos θ and sin θ (Section 31.12). |
| 79–81 | `if ((u / a) * (u / a) + (v / b) * (v / b) <= 1.0) { ++inside; }` | The level ellipse test. |
| 82–85 | `}` `}` `return static_cast<double>(inside) / (n * n);` `}` | The fraction of samples inside: the coverage. |
| 87 | `inline Rect tiltedEllipseBox(PointF centre, double a, double b, double radians) {` | The pixel box that holds the whole tilted ellipse (Section 31.11). |
| 88–89 | `double c = ...; double s = ...;` | cos θ and sin θ. |
| 90–91 | `double halfWidth = std::sqrt(a * a * c * c + b * b * s * s);` / `double halfHeight = ...` | √(a²cos²θ + b²sin²θ) and √(a²sin²θ + b²cos²θ). |
| 92–95 | `int x0 = static_cast<int>(std::floor(centre.x - halfWidth));` … | Round the edges **outward**: floor for the start, ceil for the end, so no part of the ellipse is cut off. |
| 96–97 | `return Rect{x0, y0, x1, y1};` `}` | A half-open `Rect` (Chapter 19). |
| 99–100 | `inline void fillTiltedEllipseAA(Image& image, PointF centre, double a, double b, double radians, Colour c, int n = 4) {` | Draw a smooth, filled, tilted ellipse. |
| 101–103 | `if (a <= 0.0 \|\| b <= 0.0 \|\| n < 1) { return; }` | Nothing to draw (and protects the divisions by a and b). |
| 104 | `Rect box = clipToImage(tiltedEllipseBox(centre, a, b, radians), image);` | The box, cut to the picture (Chapter 19). |
| 105–110 | `for (int y = ...) { for (int x = ...) { paintCoverage(image, x, y, c, tiltedEllipseCoverage(...)); } } }` | Every pixel in the box gets its coverage painted (Chapter 27: 0 is skipped, 1 is set, anything between is blended in linear light). |
| 112 | `#endif` | End of the include guard. |

---

## Code, part 2: fans, flowers and houses

File: `ch31/transform.cpp`

```cpp
#include <iostream>
#include <vector>
#include "transform.h"
#include "hsv.h"

void printPoint(const char* label, Vec2 p) {
    std::cout << label << " (" << p.x << ", " << p.y << ")\n";
}

std::vector<PointF> closed(std::vector<PointF> points) {
    if (!points.empty()) {
        points.push_back(points[0]);
    }
    return points;
}

int main() {
    double quarter = degreesToRadians(90.0);
    printPoint("translate (3, 1) by (10, 5):", translate(Vec2{3.0, 1.0}, Vec2{10.0, 5.0}));
    printPoint("scale (4, 6) by 2 about (2, 2):",
               scaleAbout(Vec2{4.0, 6.0}, Vec2{2.0, 2.0}, 2.0, 2.0));
    printPoint("mirror (5, 3) about x = 2:", scaleAbout(Vec2{5.0, 3.0}, Vec2{2.0, 0.0}, -1.0, 1.0));
    printPoint("rotate (3, 1) by 90 degrees:", rotate(Vec2{3.0, 1.0}, quarter));
    printPoint("rotate (2, 1) by 30 degrees:", rotate(Vec2{2.0, 1.0}, degreesToRadians(30.0)));
    printPoint("rotate (5, 2) by 90 degrees about (2, 2):",
               rotateAbout(Vec2{5.0, 2.0}, Vec2{2.0, 2.0}, quarter));
    printPoint("(1, 0): rotate 90, then move by (10, 0):",
               translate(rotate(Vec2{1.0, 0.0}, quarter), Vec2{10.0, 0.0}));
    printPoint("(1, 0): move by (10, 0), then rotate 90:",
               rotate(translate(Vec2{1.0, 0.0}, Vec2{10.0, 0.0}), quarter));
    Vec2 v{3.0, 4.0};
    std::cout << "length of (3, 4) before and after a 37 degree turn: " << length(v) << ", "
              << length(rotate(v, degreesToRadians(37.0))) << "\n";
    Rect box = tiltedEllipseBox(PointF{0.0, 0.0}, 60.0, 20.0, degreesToRadians(30.0));
    std::cout << "box of a = 60, b = 20 tilted 30 degrees: " << box.x0 << ", " << box.y0 << " to "
              << box.x1 << ", " << box.y1 << "\n";
    PointF origin{0.0, 0.0};
    double thirty = degreesToRadians(30.0);
    bool first = insideTiltedEllipse(Vec2{47.0, 27.0}, origin, 60.0, 20.0, thirty);
    bool second = insideTiltedEllipse(Vec2{55.0, 0.0}, origin, 60.0, 20.0, thirty);
    std::cout << "is (47, 27) inside it? " << (first ? "yes" : "no") << ", is (55, 0)? "
              << (second ? "yes" : "no") << "\n";

    Image fan(300, 300, colours::white);
    PointF c{150.0, 150.0};
    std::vector<PointF> square = {c, c + Vec2{100.0, 0.0}, c + Vec2{100.0, 100.0},
                                  c + Vec2{0.0, 100.0}};
    for (int i = 0; i < 12; ++i) {
        Colour col = toColour(hsvToRgb(HSV{i * 30.0, 0.8, 0.85}));
        std::vector<PointF> turned = rotatePoints(square, c, degreesToRadians(i * 30.0));
        drawPolylineWu(fan, closed(turned), col);
    }

    Image flower(300, 300, Colour{235, 245, 235});
    for (int i = 0; i < 8; ++i) {
        double angle = degreesToRadians(i * 45.0);
        PointF petal = pointOnCircle(c, 70.0, angle);
        Colour col = toColour(hsvToRgb(HSV{320.0 + i * 5.0, 0.6, 0.95}));
        fillTiltedEllipseAA(flower, petal, 70.0, 24.0, angle, col);
    }
    fillCircleAA(flower, c.x, c.y, 30.0, Colour{250, 200, 40});

    Image compare(400, 200, colours::white);
    double tilt = degreesToRadians(30.0);
    Colour blue{40, 90, 200};
    fillPolygonAA(compare, tiltedEllipsePoints(PointF{100.0, 100.0}, 80.0, 35.0, tilt, 100), blue);
    fillTiltedEllipseAA(compare, PointF{300.0, 100.0}, 80.0, 35.0, tilt, blue);
    drawPolylineWu(compare, closed(tiltedEllipsePoints(PointF{300.0, 100.0}, 80.0, 35.0, tilt, 12)),
                   colours::red);

    Image figures(600, 220, colours::white);
    std::vector<PointF> house = {PointF{-40.0, 0.0},   PointF{40.0, 0.0},    PointF{40.0, -60.0},
                                 PointF{50.0, -60.0},  PointF{35.0, -72.0},  PointF{35.0, -95.0},
                                 PointF{25.0, -95.0},  PointF{25.0, -80.0},  PointF{0.0, -100.0},
                                 PointF{-50.0, -60.0}, PointF{-40.0, -60.0}};
    PointF ground{0.0, 0.0};
    Colour houseColour{200, 90, 50};
    fillPolygonAA(figures, translatePoints(house, Vec2{80.0, 180.0}), houseColour);
    fillPolygonAA(figures, translatePoints(scalePoints(house, ground, 1.5, 1.5), Vec2{220.0, 180.0}),
                  houseColour);
    fillPolygonAA(figures, translatePoints(scalePoints(house, ground, -1.0, 1.0), Vec2{370.0, 180.0}),
                  houseColour);
    fillPolygonAA(figures, translatePoints(scalePoints(house, ground, 1.0, 0.5), Vec2{510.0, 180.0}),
                  houseColour);
    drawLine(figures, 0, 180, 599, 180, Colour{120, 120, 120});

    Image trail(600, 200, Colour{20, 20, 40});
    std::vector<PointF> star = starPoints(origin, 30.0, 12.0, 5, degreesToRadians(-90.0));
    for (int i = 0; i < 9; ++i) {
        std::vector<PointF> spun = rotatePoints(star, origin, degreesToRadians(i * 15.0));
        std::vector<PointF> placed = translatePoints(spun, Vec2{60.0 + i * 60.0, 100.0});
        Colour col = toColour(hsvToRgb(HSV{40.0 + i * 20.0, 0.7, 0.4 + i * 0.07}));
        fillPolygonAA(trail, placed, col);
    }

    bool ok = fan.savePPM("fan.ppm");
    ok = ok && flower.savePPM("flower.ppm");
    ok = ok && compare.savePPM("compare.ppm");
    ok = ok && figures.savePPM("figures.ppm");
    ok = ok && trail.savePPM("trail.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
```

Build and run (from the `code/ch31` folder):

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common transform.cpp -o transform
./transform
```

### Line by line

**Two helpers (lines 1–15)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–4 | the `#include` lines | Printing, lists, our new header, and `hsv.h` for rainbow colours. |
| 6–8 | `void printPoint(const char* label, Vec2 p) { std::cout << label << " (" << p.x << ", " << p.y << ")\n"; }` | Print a label and a point, so the many lines below stay short. |
| 10 | `std::vector<PointF> closed(std::vector<PointF> points) {` | Make a **closed** outline for `drawPolylineWu`. The list is passed **by value** (a copy), because we change the copy. |
| 11–15 | `if (!points.empty()) { points.push_back(points[0]); } return points; }` | Add the first point again at the end, so the last edge goes back to the start. (`fillPolygonAA` closes shapes by itself; a polyline does not.) |

**The numbers (lines 17–42)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 18 | `double quarter = degreesToRadians(90.0);` | A quarter turn, in radians. |
| 19 | `printPoint("translate (3, 1) by (10, 5):", translate(...));` | Section 31.2. |
| 20–21 | `printPoint("scale (4, 6) by 2 about (2, 2):", scaleAbout(...));` | Section 31.3. |
| 22 | `printPoint("mirror (5, 3) about x = 2:", scaleAbout(Vec2{5.0, 3.0}, Vec2{2.0, 0.0}, -1.0, 1.0));` | A mirror is a scale by −1 across. |
| 23–24 | the two `rotate` lines | Section 31.4. |
| 25–26 | `printPoint("rotate (5, 2) by 90 degrees about (2, 2):", rotateAbout(...));` | Section 31.6. |
| 27–30 | the two "order" lines | `translate(rotate(...))` turns first (the inner call happens first); `rotate(translate(...))` moves first (Section 31.8). |
| 31–33 | `Vec2 v{3.0, 4.0};` … `length(rotate(v, degreesToRadians(37.0)))` | Turning keeps the length (Section 31.5). |
| 34–36 | `Rect box = tiltedEllipseBox(...);` and printing | The box of Section 31.11. |
| 37–38 | `PointF origin{0.0, 0.0};` / `double thirty = degreesToRadians(30.0);` | Names for (0, 0) and the 30° tilt. |
| 39–40 | `bool first = insideTiltedEllipse(Vec2{47.0, 27.0}, ...);` / `bool second = ...` | The two tests of Section 31.10. |
| 41–42 | `std::cout << "is (47, 27) inside it? " << (first ? "yes" : "no") << ...` | Print "yes" or "no" instead of 1 or 0. |

**The fan (lines 44–52)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 44–45 | `Image fan(300, 300, colours::white);` / `PointF c{150.0, 150.0};` | A white picture and its middle. |
| 46–47 | `std::vector<PointF> square = {c, c + Vec2{100.0, 0.0}, c + Vec2{100.0, 100.0}, c + Vec2{0.0, 100.0}};` | A square of side 100 whose **top-left corner** is the middle of the picture. |
| 48–49 | `for (int i = 0; i < 12; ++i) { Colour col = toColour(hsvToRgb(HSV{i * 30.0, 0.8, 0.85}));` | Twelve copies, each with its own hue. |
| 50 | `std::vector<PointF> turned = rotatePoints(square, c, degreesToRadians(i * 30.0));` | Turn the square around its corner c, by 0°, 30°, 60°, … 330°. |
| 51–52 | `drawPolylineWu(fan, closed(turned), col);` `}` | Draw its smooth outline. The twelve squares overlap like the blades of a paper fan. |

**The flower (lines 54–61)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 54 | `Image flower(300, 300, Colour{235, 245, 235});` | A pale green picture. |
| 55–56 | `for (int i = 0; i < 8; ++i) { double angle = degreesToRadians(i * 45.0);` | Eight petals, 45° apart. |
| 57 | `PointF petal = pointOnCircle(c, 70.0, angle);` | The petal's centre, 70 pixels out from the middle (Chapter 30). |
| 58 | `Colour col = toColour(hsvToRgb(HSV{320.0 + i * 5.0, 0.6, 0.95}));` | Pinks, each petal a little different, so you can see where they overlap. |
| 59–60 | `fillTiltedEllipseAA(flower, petal, 70.0, 24.0, angle, col);` `}` | A smooth ellipse tilted by the **same** angle, so it points out from the middle. |
| 61 | `fillCircleAA(flower, c.x, c.y, 30.0, Colour{250, 200, 40});` | A yellow middle, drawn last so it covers the inner tips. |

**Polygon or pixel test? (lines 63–69)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 63–65 | `Image compare(400, 200, colours::white);` / `double tilt = ...;` / `Colour blue{40, 90, 200};` | A wide picture, a 30° tilt and a blue colour. |
| 66 | `fillPolygonAA(compare, tiltedEllipsePoints(PointF{100.0, 100.0}, 80.0, 35.0, tilt, 100), blue);` | Left: way 1, a 100-corner polygon (Section 31.9). |
| 67 | `fillTiltedEllipseAA(compare, PointF{300.0, 100.0}, 80.0, 35.0, tilt, blue);` | Right: way 2, the pixel test (Section 31.12). |
| 68–69 | `drawPolylineWu(compare, closed(tiltedEllipsePoints(PointF{300.0, 100.0}, 80.0, 35.0, tilt, 12)), colours::red);` | A red 12-corner outline on top of the right one: you can see its straight sides cut inside the curve. |

**The houses (lines 71–85)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 71 | `Image figures(600, 220, colours::white);` | A wide picture. |
| 72–75 | `std::vector<PointF> house = {...};` | A house in local coordinates (Section 31.6): 11 corners, with (0, 0) in the middle of its bottom edge and y negative going up. It has a **chimney on the right**, so you can tell when it is mirrored. |
| 76–77 | `PointF ground{0.0, 0.0};` / `Colour houseColour{200, 90, 50};` | The pivot for scaling (the middle of the bottom edge, so the houses stay standing on the ground), and a brick colour. |
| 78 | `fillPolygonAA(figures, translatePoints(house, Vec2{80.0, 180.0}), houseColour);` | House 1: just moved into place. |
| 79–80 | `translatePoints(scalePoints(house, ground, 1.5, 1.5), Vec2{220.0, 180.0})` | House 2: 1.5 times bigger, **then** moved (scale first, Section 31.8). |
| 81–82 | `scalePoints(house, ground, -1.0, 1.0)` | House 3: mirrored — the chimney is now on the left. |
| 83–84 | `scalePoints(house, ground, 1.0, 0.5)` | House 4: squashed to half height (a non-uniform scale). |
| 85 | `drawLine(figures, 0, 180, 599, 180, Colour{120, 120, 120});` | A grey ground line at y = 180, where all four houses stand. |

**The star trail (lines 87–94)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 87 | `Image trail(600, 200, Colour{20, 20, 40});` | A dark blue night sky. |
| 88 | `std::vector<PointF> star = starPoints(origin, 30.0, 12.0, 5, degreesToRadians(-90.0));` | A 5-tip star (Chapter 30) in local coordinates: centred on (0, 0), pointing up. |
| 89–90 | `for (int i = 0; i < 9; ++i) { std::vector<PointF> spun = rotatePoints(star, origin, degreesToRadians(i * 15.0));` | Nine stars; star i is turned by i × 15° **around its own centre** (still at the origin). |
| 91 | `std::vector<PointF> placed = translatePoints(spun, Vec2{60.0 + i * 60.0, 100.0});` | **Then** moved into place, 60 pixels apart. |
| 92 | `Colour col = toColour(hsvToRgb(HSV{40.0 + i * 20.0, 0.7, 0.4 + i * 0.07}));` | Each star a little brighter and a different hue (from orange to blue). |
| 93–94 | `fillPolygonAA(trail, placed, col);` `}` | Fill it smoothly. |

**Saving (lines 96–106)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 96–100 | `bool ok = fan.savePPM("fan.ppm");` … | Save the five pictures. |
| 101–106 | `if (!ok) { ... }` `return 0;` `}` | Report a problem, or finish. |

### What you should see

```
translate (3, 1) by (10, 5): (13, 6)
scale (4, 6) by 2 about (2, 2): (6, 10)
mirror (5, 3) about x = 2: (-1, 3)
rotate (3, 1) by 90 degrees: (-1, 3)
rotate (2, 1) by 30 degrees: (1.23205, 1.86603)
rotate (5, 2) by 90 degrees about (2, 2): (2, 5)
(1, 0): rotate 90, then move by (10, 0): (10, 1)
(1, 0): move by (10, 0), then rotate 90: (6.73556e-16, 11)
length of (3, 4) before and after a 37 degree turn: 5, 5
box of a = 60, b = 20 tilted 30 degrees: -53, -35 to 53, 35
is (47, 27) inside it? yes, is (55, 0)? no
```

Open the pictures:
- `fan.ppm`: twelve rainbow-coloured square outlines, all sharing one corner in the middle, spread around like a fan.
- `flower.ppm`: eight smooth pink petals pointing outward around a yellow middle.
- `compare.ppm`: two blue tilted ellipses that look the same; the right one has a red 12-sided outline whose corners touch the curve while its sides cut inside it.
- `figures.ppm`: four brick-red houses on a grey line: normal, bigger, mirrored (chimney on the other side) and squashed.
- `trail.ppm`: nine stars on a dark sky, turning a little more from left to right, and getting brighter.

---

## Small examples

### Example 1 — A 45° turn

Rotate (10, 0) by 45°:

> cos 45° = sin 45° = 0.7071
> (10 × 0.7071 − 0, 10 × 0.7071 + 0) = **(7.07, 7.07)** — down-right on the screen, still 10 from the origin (√(7.07² + 7.07²) = √100 = 10 ✓)

### Example 2 — Halving a shape around its middle

A triangle (100, 40), (160, 160), (40, 160). Its middle (the average of the corners, Chapter 26): (100, 120). Scale by 0.5 about it:

> (100, 40): step (0, −80) → (0, −40) → **(100, 80)**
> (160, 160): step (60, 40) → (30, 20) → **(130, 140)**
> (40, 160): step (−60, 40) → (−30, 20) → **(70, 140)**
> Half as wide (120 → 60) and half as high (120 → 60), with the same middle ✓

### Example 3 — Mirroring a whole picture's worth of shapes

To flip every shape in a picture 600 pixels wide left to right, mirror about the middle line x = 300:

> x' = 300 + (−1) × (x − 300) = **600 − x**
> A corner at x = 0 (the left edge) goes to 600 (the right edge), x = 100 goes to 500, and x = 300 stays ✓

### Example 4 — Spin in place, or swing around

A wheel's spoke tip is at (120, 100); the hub is at (100, 100). Turn it by 90°:

> **about the hub:** (100, 100) + rotate((20, 0), 90°) = (100, 100) + (0, 20) = **(100, 120)** — the spoke now points down ✓
> **about the origin (a mistake):** rotate((120, 100), 90°) = (−100, 120) — off the left edge of the picture!

### Example 5 — Many small turns add up

Turning by 30° twelve times gives 12 × 30° = 360°: a full turn, back to the start. That is why the fan has exactly twelve squares: the thirteenth would sit exactly on the first.

---

## Common mistakes

⚠️ **Rotating around the origin by accident.** `rotate` turns around (0, 0), the top-left corner of the picture. Use `rotateAbout` with the shape's own centre, or build the shape in local coordinates.

⚠️ **The wrong order.** Moving first and turning second swings the shape around the origin. For a shape in local coordinates: **scale, rotate, then translate**.

⚠️ **Degrees instead of radians.** `rotate` takes radians, like `std::sin` (Chapter 30). Use `degreesToRadians`.

⚠️ **Expecting counter-clockwise turns.** On our screen, y goes down, so a positive angle turns **clockwise**.

⚠️ **Forgetting the sign in the formula.** It is x cos θ **−** y sin θ, but x sin θ **+** y cos θ. Swap the minus to the other line and you turn the wrong way (by −θ). Check with (1, 0) and 90°: the answer must be (0, 1).

⚠️ **Changing c and s halfway.** In `rotate`, both new coordinates must be computed from the **old** x and y. If you write `p.x = ...` first and then use the new `p.x` to compute `p.y`, the point gets squashed. That is why `rotate` returns a new `Vec2` instead of changing `p`.

⚠️ **Using the level-ellipse box for a tilted ellipse.** The tips stick out of it and get cut off. Use `tiltedEllipseBox`.

⚠️ **Not closing an outline.** `drawPolylineWu` draws only the edges between the points you give it. Add the first point at the end (our `closed` helper).

---

## Practice

🏋️ **1.** By hand: rotate (4, 0) by 60°, and rotate (0, 2) by −90°. Which way does each one turn on the screen?

🏋️ **2.** Rotate (6, 3) by 180° about (4, 3). Then get the same answer with `scaleAbout`.

🏋️ **3.** The square from (10, 10) to (20, 20) is scaled by 3 about its own centre. Where are its new corners?

🏋️ **4.** Check, with numbers, that turning (1, 0) by 20° and then by 25° gives the same point as turning it by 45° at once.

🏋️ **5.** Write a function `skewX(Vec2 p, double k)` that returns (x + k × y, y), and use it on the house to make it lean, like italic letters. What happens to its height? (This "skew" or "shear" comes back in Chapter 32.)

🏋️ **6.** Draw a **windmill**: four long tilted ellipses around a centre (at 0°, 90°, 180° and 270°, plus a 20° turn for all of them), on top of a tower made with `fillPolygonAA`.

🏋️ **7.** Use `tiltedEllipseBox` to find the box of an ellipse with a = 50, b = 10 tilted 45°. Compare its area with the lazy square box.

🏋️ **8.** Draw a "spirograph": 36 copies of the outline of a tilted ellipse (a = 120, b = 40) all centred on the middle of the picture, each tilted 5° more than the last.

---

## Answers

**1.**
> rotate (4, 0) by 60°: (4 cos 60°, 4 sin 60°) = **(2, 3.464)** — it turned from "right" toward "down": clockwise.
> rotate (0, 2) by −90°: cos(−90°) = 0, sin(−90°) = −1 → (0 × 0 − 2 × (−1), 0 × (−1) + 2 × 0) = **(2, 0)** — from "down" to "right": counter-clockwise ✓ (negative angle).

**2.**
> p − C = (2, 0) → rotate by 180° → (−2, 0) → C + (−2, 0) = **(2, 3)**
> scaleAbout((6, 3), (4, 3), −1, −1) = (4 − 2, 3 − 0) = **(2, 3)** ✓ (a half turn is a double mirror, Section 31.6)

**3.**
> The centre is (15, 15). Corner (10, 10): step (−5, −5) → (−15, −15) → **(0, 0)**. Corner (20, 20): step (5, 5) → (15, 15) → **(30, 30)**. The others: **(30, 0)** and **(0, 30)**. A square 30 wide, with the same centre ✓

**4.**
> by 20°: (cos 20°, sin 20°) = (0.9397, 0.3420)
> then by 25° (cos 25° = 0.9063, sin 25° = 0.4226):
> x = 0.9397 × 0.9063 − 0.3420 × 0.4226 = 0.8517 − 0.1445 = **0.7071**
> y = 0.9397 × 0.4226 + 0.3420 × 0.9063 = 0.3971 + 0.3100 = **0.7071**
> (cos 45°, sin 45°) = (0.7071, 0.7071) ✓ — turns about the same pivot simply add up.

**5.**

```cpp
Vec2 skewX(Vec2 p, double k) {
    return Vec2{p.x + k * p.y, p.y};
}

std::vector<PointF> leaning;
for (PointF p : house) {
    leaning.push_back(skewX(p, -0.4));
}
fillPolygonAA(figures, translatePoints(leaning, Vec2{300.0, 180.0}), houseColour);
```

The house's points have y ≤ 0 (above the ground), so with k = −0.4 the higher points move **right** (−0.4 × −100 = +40 at the top of the roof): the house leans to the right. The bottom edge (y = 0) does not move, and every point keeps its y, so the **height stays the same**. Unlike a rotation, a skew changes angles: the walls are no longer upright, but level lines (like the floor) stay level.

**6.**

```cpp
Image mill(300, 300, Colour{170, 210, 240});
PointF hub{150.0, 120.0};
std::vector<PointF> tower = {PointF{135.0, 120.0}, PointF{165.0, 120.0}, PointF{185.0, 299.0},
                             PointF{115.0, 299.0}};
fillPolygonAA(mill, tower, Colour{150, 110, 80});
for (int i = 0; i < 4; ++i) {
    double angle = degreesToRadians(20.0 + i * 90.0);
    PointF blade = pointOnCircle(hub, 55.0, angle);
    fillTiltedEllipseAA(mill, blade, 55.0, 14.0, angle, colours::white);
}
fillCircleAA(mill, hub.x, hub.y, 8.0, Colour{80, 60, 50});
```

Change the 20.0 to make the windmill turn — in Chapter 80 we will do exactly that, frame by frame, to make it spin.

**7.**
> cos²45° = sin²45° = 0.5
> half width = half height = √(2500 × 0.5 + 100 × 0.5) = √1300 ≈ **36.06**
> The box is about 72 × 72 ≈ 5,200 pixels. The lazy square box is 100 × 100 = **10,000**: almost twice as many pixels to test.

**8.**

```cpp
Image spiro(300, 300, colours::white);
PointF mid{150.0, 150.0};
for (int i = 0; i < 36; ++i) {
    double tilt = degreesToRadians(i * 5.0);
    Colour col = toColour(hsvToRgb(HSV{i * 10.0, 0.7, 0.8}));
    drawPolylineWu(spiro, closed(tiltedEllipsePoints(mid, 120.0, 40.0, tilt, 120)), col);
}
```

36 × 5° = 180°, and an ellipse looks the same after a half turn, so 36 copies go exactly once around the pattern.

---

## Summary

🧠 A shape is its points. **Transform the points, then draw again.**

🧠 **Translate:** p + t. **Scale about C:** C + s(p − C) (sx and sy may differ; −1 mirrors). **Rotate about the origin:** (x cos θ − y sin θ, x sin θ + y cos θ). **Rotate about C:** C + rotate(p − C, θ).

🧠 The rotation formula comes from: (1, 0) → (cos θ, sin θ), (0, 1) → (−sin θ, cos θ), and p = x(1, 0) + y(0, 1).

🧠 Rotation keeps lengths and angles. A half turn equals a scale by (−1, −1).

🧠 On the screen, positive θ turns **clockwise**.

🧠 **Order matters.** In local coordinates: scale, rotate, **then** translate.

🧠 Every transformation here has an **inverse**: move by −t, scale by 1/s, turn by −θ.

🧠 A **tilted ellipse**: as a polygon of points C + rotate((a cos t, b sin t), θ), or with a pixel test that **turns the pixel back** by −θ and uses the level-ellipse test. Its box: half width √(a²cos²θ + b²sin²θ), half height √(a²sin²θ + b²cos²θ).

---

## Next chapter

We now have three separate functions — `translate`, `scaleAbout` and `rotate` — and long chains of them get messy (and easy to get in the wrong order). In Chapter 32 we pack the "where does (1, 0) go, where does (0, 1) go" idea of Section 31.4 into a small table of numbers called a **matrix**. With one more trick — **homogeneous coordinates**, adding a third number 1 to every point — even moving becomes a matrix, and **any** mix of moves, scales, turns and skews fits in a single 3 × 3 table.
