# Chapter 24 — Triangles and Edge Functions

> **Part 4 · Chapter 24 of 82**
> **You need:** Chapters 1–23 · **You will make:** `triangles.h` (the edge function, filled triangles, triangle outlines, convex polygons), `mountains.ppm`, `seams.ppm` and `wheel.ppm`

---

## What you will learn

- Why the **triangle** is the most important shape in computer graphics.
- The **edge function**: one short formula that tells you which **side** of a line a point is on.
- Why that formula works, and why it is also **twice the area** of a triangle.
- How **three** edge functions tell you if a point is **inside** a triangle.
- **Clockwise** and **counter-clockwise** triangles, and how to handle both.
- How to fill a triangle with a bounding box and the pixel-centre test.
- How the edge function changes by a **fixed amount** from one pixel to the next.
- The problem of **shared edges** (pixels painted twice, or never), and the **top-left rule** that solves it.
- How to fill any **convex polygon** by cutting it into triangles.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **triangle** | A shape with three straight sides and three corners. |
| **vertex** (plural: **vertices**) | A corner point of a shape. |
| **edge** | One straight side of a shape, from one vertex to the next. |
| **edge function** | A formula that gives a positive number on one side of a line, a negative number on the other side, and 0 on the line. |
| **orientation** | The direction in which we go around the corners: clockwise or counter-clockwise. |
| **clockwise** | Turning the same way as the hands of a clock. |
| **counter-clockwise** | Turning the other way. |
| **signed area** | An area with a + or − sign. The sign tells the orientation. |
| **seam** | A visible line where two pieces meet, like the line where two pieces of cloth are sewn together. |
| **polygon** | A closed shape made of straight edges (a triangle, a square, a hexagon, …). |
| **convex** | A shape with no "dents": every inside angle is less than 180°. |
| **triangulation** | Cutting a shape into triangles. |
| **fan** | A triangulation where all the triangles share one corner, like the folds of a hand fan. |
| **hexagon** | A polygon with six edges. |

---

## 24.1 Why triangles?

📖 **New word: triangle** — a shape with three straight sides.

📖 **New word: vertex** (plural **vertices**) — a corner point. A triangle has 3 vertices. We usually call them **A**, **B** and **C**.

📖 **New word: edge** — one straight side, from one vertex to the next. A triangle has 3 edges: A→B, B→C and C→A.

Triangles are the "atoms" of computer graphics, for three reasons:

1. **Any flat shape with straight edges can be cut into triangles.** A square is 2 triangles. A hexagon is 4 (or 6). A map of a country can be thousands.
2. **A triangle is always flat and simple.** It never has dents, never crosses itself, and has no holes. So one simple test works for every triangle.
3. **Three points are enough.** In 3D, every surface of a game character — a face, a car, a tree — is made of small triangles. Your graphics card draws **millions** of them every second, using exactly the method of this chapter.

```
   A square = 2 triangles
   ┌─────────┐
   │╲        │
   │  ╲      │
   │    ╲    │
   │      ╲  │
   │        ╲│
   └─────────┘
```

---

## 24.2 The outline of a triangle

The easy part first. The outline is just three lines (Chapter 21):

> line from A to B, line from B to C, line from C to A

We draw each line **without its last pixel** (`includeLast = false`, Chapter 21). Each line ends where the next one starts, so every corner pixel is drawn exactly once. (With solid colours this does not matter, but with see-through colours, a corner painted twice would look darker.)

The hard part is **filling** the triangle: which pixels are inside? For that we need a new tool.

---

## 24.3 Which side of a line? The edge function

Stand on a straight road, and look along it. Every house is either on your **left** or on your **right** (or exactly on the road). We want a formula that tells us which.

📖 **New word: edge function** — for a line through A and B, and any point P:

> **E(A, B, P) = (B.x − A.x) × (P.y − A.y) − (B.y − A.y) × (P.x − A.x)**

- E = 0: P is **on** the line.
- E > 0: P is on one side.
- E < 0: P is on the other side.

🔢 **Maths: the edge from A = (2, 2) to B = (10, 2)**

> B.x − A.x = 8, B.y − A.y = 0
> So E(A, B, P) = 8 × (P.y − 2) − 0 × (P.x − 2) = 8 × (P.y − 2)
>
> P = (6, 5): E = 8 × 3 = **24** (positive)
> P = (6, 0): E = 8 × (−2) = **−16** (negative)
> P = (6, 2): E = 8 × 0 = **0** (on the line)

Our program prints exactly these three numbers.

### Which side is "positive"?

Walk from A to B. In the example, you walk to the **right** across the screen. The point (6, 5) is **below** the line on the screen (remember: y goes **down**, Chapter 3). If you walk to the right, your right hand points **down** the screen. So (6, 5) is on your **right**, and its E is positive.

🧠 **Remember (on the screen, with y going down):**

> E > 0 → P is on the **right** of the line, when you walk from A to B
> E < 0 → P is on the **left**
> E = 0 → P is **on** the line

```
         A ●━━━━━━━━━━━━━━━━→● B        walking this way
                  · (6, 5)              ← on your right: E > 0
```

💡 In maths books, the y-axis usually goes **up**, and then everything is mirrored: positive means **left**. Do not be confused if you read other books. On our screen with y going down, positive means **right**.

### A slanted edge

🔢 **Maths: the edge from A = (0, 0) to B = (4, 4)** (going down-right on the screen)

> B.x − A.x = 4, B.y − A.y = 4
> E(A, B, P) = 4 × P.y − 4 × P.x
>
> P = (1, 3): E = 12 − 4 = **8** → right side
> P = (3, 1): E = 4 − 12 = **−8** → left side
> P = (2, 2): E = 8 − 8 = **0** → on the line ✓ (it is on the diagonal)

Check with a picture: you walk down-right from (0, 0). Your right hand points down-left, toward (1, 3). ✓

---

## 24.4 Why does the formula work?

### Part 1: why E = 0 on the line

A point P is on the line through A and B when going from A to P is "the same direction" as going from A to B. Same direction means the same **slope** (Chapter 20):

> (P.y − A.y) / (P.x − A.x) = (B.y − A.y) / (B.x − A.x)

Divisions are dangerous (what if P.x − A.x is 0?), so we **cross-multiply** — multiply both sides by (P.x − A.x) and by (B.x − A.x):

> (B.x − A.x) × (P.y − A.y) = (B.y − A.y) × (P.x − A.x)

Move everything to one side:

> (B.x − A.x) × (P.y − A.y) − (B.y − A.y) × (P.x − A.x) = 0

That is exactly **E(A, B, P) = 0**. ✓ And because there is no division, this works for every line, even a vertical one.

### Part 2: why the sign changes from side to side

E is a "straight" (linear) formula in P.x and P.y: there are no squares and no square roots. If you walk with P across the line, E grows (or shrinks) **steadily**, like a ruler. It is 0 on the line, so it must be positive on one side and negative on the other.

In fact, E measures **how far** P is from the line:

> **E = (length of AB) × (signed distance from P to the line)**

🔢 **Maths: check with A = (2, 2), B = (10, 2), P = (6, 5)**

> length of AB = 8
> distance from P to the line y = 2 is 5 − 2 = 3
> 8 × 3 = 24 ✓ (the program prints 24)

### Part 3: E is twice the area of a triangle

The area of a triangle is ½ × base × height. Take A, B and P as a triangle. The base is AB, and the height is the distance from P to the line AB. So:

> area of triangle ABP = ½ × (length of AB) × (distance) = ½ × |E|
>
> **|E(A, B, P)| = 2 × area of triangle ABP**

(|E| means "E without its sign": |−12| = 12 and |12| = 12.)

🔢 **Maths: the triangle A = (0, 0), B = (4, 0), P = (0, 3)**

> E = (4 − 0)(3 − 0) − (0 − 0)(0 − 0) = 12
> The triangle has a right angle at A: base 4, height 3 → area = ½ × 4 × 3 = 6
> 2 × 6 = 12 ✓

📖 **New word: signed area** — E / 2, **with** its sign. The size tells the area, and the sign tells the orientation (Section 24.6).

💡 You will meet this formula again in Chapter 29, where it is called the **cross product** of two 2D vectors: the vector from A to B, and the vector from A to P.

---

## 24.5 Inside a triangle: three edge functions

A triangle has three edges. Walk around it: A → B → C → A. If the triangle is on your **right** the whole time, then a point P is **inside** when it is on the right of **all three** edges:

> **inside ⇔ E(A, B, P) ≥ 0 and E(B, C, P) ≥ 0 and E(C, A, P) ≥ 0**

(The ⇔ sign means "exactly when".)

```
              A ●───────────→● B
                 ╲  inside  ╱
                  ╲   ·P   ╱      walking A → B → C → A,
                   ╲      ╱       the inside is always
                    ╲    ╱        on your right
                     ╲  ╱
                      ●
                      C
```

We give the three values short names, which we will use a lot (also in Chapter 26):

> w0 = E(B, C, P) — for the edge **opposite** A
> w1 = E(C, A, P) — for the edge opposite B
> w2 = E(A, B, P) — for the edge opposite C

🔢 **Maths: is P = (3.5, 3.5) inside A = (0, 0), B = (10, 0), C = (0, 10)?**

> w0 = E(B, C, P) = (0 − 10)(3.5 − 0) − (10 − 0)(3.5 − 10) = −35 + 65 = 30
> w1 = E(C, A, P) = (0 − 0)(3.5 − 10) − (0 − 10)(3.5 − 0) = 0 + 35 = 35
> w2 = E(A, B, P) = (10 − 0)(3.5 − 0) − (0 − 0)(3.5 − 0) = 35
> All three ≥ 0 → **inside** ✓

### A beautiful fact: the three values add up to the same number

> w0 + w1 + w2 = 30 + 35 + 35 = **100**

And E(A, B, C), twice the area of the whole triangle, is (10)(10) − (0)(0) = **100**. The same!

This is true for **every** point P. Each w is twice the area of a small triangle (P with one edge), and the three small triangles together make the whole triangle:

```
          A ●───────────────● B
             ╲ ╲    w2    ╱ ╱
              ╲   ╲     ╱  ╱       the three small triangles
               ╲ w1 ● P   ╱        around P fill the big one:
                ╲   │ w0 ╱         w2 = P with edge AB,
                 ╲  │   ╱          w0 = P with edge BC,
                  ╲ │  ╱           w1 = P with edge CA
                   ╲│ ╱
                    ●
                    C
```

🧠 **Remember:** w0 + w1 + w2 = E(A, B, C) = 2 × area. Chapter 26 turns this fact into a way to **mix colours** across a triangle.

---

## 24.6 Clockwise or counter-clockwise?

📖 **New word: orientation** — the direction in which we go around the corners.

📖 **New words: clockwise** (the way a clock's hands turn) and **counter-clockwise** (the other way).

The rule "inside is on the right" only works if we walk around the triangle **clockwise** (as seen on the screen). If someone gives us the corners in the other order, the inside is on our **left**, and all three w's are **negative** inside.

How can we know the orientation? Use the edge function on the corners themselves:

> **E(A, B, C) > 0** → C is on the right of A→B → **clockwise** on the screen
> **E(A, B, C) < 0** → **counter-clockwise**
> **E(A, B, C) = 0** → A, B, C are on **one line**: the "triangle" is flat and has no area

🔢 **Maths: two orders of the same triangle**

> A = (0, 0), B = (10, 0), C = (0, 10):
> E(A, B, C) = 10 × 10 − 0 × 0 = **100** → clockwise ✓
> (On the screen: top-left → top-right → bottom-left. Draw it: that turns like a clock.)
>
> A = (0, 0), B = (0, 10), C = (10, 0) (B and C swapped):
> E(A, B, C) = 0 × 0 − 10 × 10 = **−100** → counter-clockwise

The fix is simple: if E(A, B, C) < 0, **swap B and C**. Now the order is clockwise, and our test works. If E(A, B, C) = 0, there is nothing to fill.

Our program fills the triangle (1, 1), (12, 4), (4, 10), and then the same corners in the other order. It prints:

```
the other order gives the same pixels: yes
```

---

## 24.7 Filling a triangle

Now we have everything:

1. Check the orientation; swap B and C if needed; stop if the area is 0.
2. Find the **bounding box**: the smallest and largest x and y of the three corners. Round down / up, and clip to the image (like circles, Chapter 22).
3. For every pixel in the box, test its **centre** (x + 0.5, y + 0.5) with the three edge functions.

🔢 **Maths: the bounding box of (1, 1), (12, 4), (4, 10)**

> smallest x = 1, largest x = 12 → columns [1, 12)
> smallest y = 1, largest y = 10 → rows [1, 10)

(A pixel in column 12 has its centre at 12.5, which is further right than every corner, so it can never be inside. The half-open box is right.)

🔢 **Maths: two pixels of this triangle**

> E(A, B, C) = (12 − 1)(10 − 1) − (4 − 1)(4 − 1) = 99 − 9 = **90** → clockwise, no swap
>
> pixel (2, 1), centre P = (2.5, 1.5):
> w2 = E(A, B, P) = 11 × 0.5 − 3 × 1.5 = 5.5 − 4.5 = **1**
> w0 = E(B, C, P) = (4 − 12)(1.5 − 4) − (10 − 4)(2.5 − 12) = 20 + 57 = **77**
> w1 = E(C, A, P) = (1 − 4)(1.5 − 10) − (1 − 10)(2.5 − 4) = 25.5 − 13.5 = **12**
> all positive → **inside**. (Check: 1 + 77 + 12 = 90 ✓)
>
> pixel (3, 1), centre P = (3.5, 1.5):
> w2 = 11 × 0.5 − 3 × 2.5 = 5.5 − 7.5 = **−2** → **outside** (we can stop at the first negative value)

The program prints the whole triangle:

```
  ..............
  .##...........
  .#####........
  ..########....
  ..#########...
  ..########....
  ...######.....
  ...####.......
  ...###........
  ....#.........
  ..............
  ..............
```

**46 pixels.** The true area is 90 / 2 = **45**. Close, as always. ✓

---

## 24.8 Stepping from pixel to pixel

The edge function is "straight" (linear), so it changes by the **same amount** every time we move one pixel. Look at E(A, B, P) when P moves one step right (P.x + 1):

> E(A, B, P) = (B.x − A.x) × (P.y − A.y) − (B.y − A.y) × (P.x − A.x)
> only the last part changes: (P.x − A.x) becomes (P.x − A.x + 1)
> so E changes by **−(B.y − A.y)**

And one step down (P.y + 1):

> only the first part changes → E changes by **+(B.x − A.x)**

🔢 **Maths: the edge A = (1, 1) to B = (12, 4)**

> one step right: E changes by −(4 − 1) = **−3**
> one step down: E changes by +(12 − 1) = **+11**
> At pixel (2, 1) we had w2 = 1. One step right, at pixel (3, 1): 1 − 3 = **−2** ✓ (the same as Section 24.7, without multiplying!)

So a fast triangle filler computes the three w's **once** at the start of each row, and then just **adds** a fixed number for each pixel. Graphics cards work this way. Our `fillTriangle` computes the edge functions fully at every pixel, because it is easier to read; Practice 5 makes the fast version.

---

## 24.9 Shared edges: painted twice, or never?

Here is a problem you only notice when you draw **many** triangles next to each other — which is exactly what we want to do (a square is two triangles, a hexagon is four, a 3D model is millions).

Take a square from (0, 0) to (8, 8), and cut it along the diagonal into two triangles:

> triangle 1: (0, 0), (8, 0), (8, 8) — the upper-right half
> triangle 2: (0, 0), (8, 8), (0, 8) — the lower-left half

The diagonal is a **shared edge**. Now look at the pixels (0, 0), (1, 1), …, (7, 7). Their centres (0.5, 0.5), (1.5, 1.5), … lie **exactly on** the diagonal: their edge value is exactly 0.

**Rule 1: "E ≥ 0 counts as inside".** Then those 8 pixels are inside **both** triangles. Our program counts how often each pixel is painted:

```
shared edge, rule E >= 0:
  21111111
  12111111
  11211111
  11121111
  11112111
  11111211
  11111121
  11111112
  painted twice: 8, never painted: 0
```

With solid colours, painting twice is harmless. But with **see-through** colours (Chapter 18), a pixel blended twice is darker than its neighbours. You see a thin dark line — a **seam** — exactly where the triangles meet.

📖 **New word: seam** — a visible line where two pieces meet.

**Rule 2: "E > 0 counts as inside" (0 does not count).** Then those 8 pixels are inside **neither** triangle:

```
shared edge, rule E > 0:
  .1111111
  1.111111
  11.11111
  111.1111
  1111.111
  11111.11
  111111.1
  1111111.
  painted twice: 0, never painted: 8
```

Now there is a line of **holes**: you see the background through the square. That is even worse.

We need a rule where a pixel exactly on a shared edge belongs to **exactly one** of the two triangles.

---

## 24.10 The top-left rule

Graphics cards use a rule called the **top-left rule**:

> A pixel whose centre lies **exactly on** an edge belongs to the triangle only if that edge is a **top** edge or a **left** edge of the triangle.

What are top and left edges? Our triangles are always clockwise (Section 24.6), so the inside is on the right of every edge.

| kind of edge | what it looks like | in numbers (ex = B.x − A.x, ey = B.y − A.y) |
|---|---|---|
| **top** edge | exactly horizontal, with the inside **below** it | ey = 0 and ex > 0 (walking right; your right hand points down, to the inside) |
| **left** edge | going **up** the screen, with the inside on its right | ey < 0 |
| other edges (right and bottom edges) | going down, or horizontal with the inside above | ey > 0, or ey = 0 and ex < 0 |

```
             top edge (→)
          A ●━━━━━━━━━━━━━━● B
            ┃            ╱
            ┃  inside  ╱
  left edge ┃       ╱    right edge
     (↑)    ┃    ╱        (going down)
            ┃ ╱
            ● C
```

(In this picture the triangle A → B → C → A goes: right along the top, down-left along the slanted side, and up the left side. The slanted side goes **down** (ey > 0), so it is a right edge, even though it is not straight up and down.)

### Why does it always work?

Think about a shared edge between two triangles. Both triangles are clockwise, so they walk along the shared edge in **opposite directions** — one from P to Q, the other from Q to P:

- If the edge is not horizontal, one triangle walks it **up** (ey < 0: a left edge, it takes the pixel) and the other walks it **down** (ey > 0: it does not take the pixel).
- If the edge is horizontal, one triangle walks it to the **right** (a top edge, it takes the pixel), the other to the **left** (it does not).

So **exactly one** of the two triangles takes every pixel on the shared edge. No seams, no holes! The program shows it:

```
shared edge, top-left rule:
  11111111
  11111111
  11111111
  11111111
  11111111
  11111111
  11111111
  11111111
  painted twice: 0, never painted: 0
```

🔢 **Maths: who takes the diagonal pixels?**

> Triangle 1 is (0, 0), (8, 0), (8, 8). Its edge C → A goes from (8, 8) to (0, 0): ey = −8 < 0 → a **left** edge → triangle 1 takes the diagonal pixels.
> Triangle 2 is (0, 0), (8, 8), (0, 8). Its edge A → B goes from (0, 0) to (8, 8): ey = +8 > 0 → **not** top-left → triangle 2 does not take them.

### Putting it into code

For each edge, we decide **once** (before the pixel loop) whether it is top-left. Then, for a pixel with edge value e:

> e > 0 → inside this edge (clearly on the inside)
> e = 0 → inside only if this edge is top-left
> e < 0 → outside

💡 **When is e exactly 0?** Only when a pixel centre lies exactly on an edge. This happens often when the corners are whole numbers or halves — which is common! A `double` stores whole numbers, halves and quarters **exactly** (as long as they are not huge), and adding, subtracting and multiplying them gives exact results too. So "e == 0.0" is a safe test here. Real graphics cards go one step further: they round every corner to a fine grid (often 1/256 of a pixel) and then use only whole numbers, so the test is exact for **every** triangle.

---

## 24.11 Polygons made of triangles

📖 **New word: polygon** — a closed shape made of straight edges: triangle (3), square (4), pentagon (5), **hexagon** (6), …

📖 **New word: convex** — a shape with no dents. Two ways to say it:
- every inside angle is less than 180°, or
- the straight line between any two points inside the shape stays inside the shape.

```
  convex:           not convex (a dent):
   ┌───────┐           ┌───────┐
   │       │           │   ┌───┘
   │       │           │   └───┐
   └───────┘           └───────┘
```

📖 **New word: triangulation** — cutting a shape into triangles.

📖 **New word: fan** — the easiest triangulation of a convex polygon: take the first corner P0, and make triangles with every pair of neighbouring corners after it:

> (P0, P1, P2), (P0, P2, P3), (P0, P3, P4), …

Like the folds of a hand fan, all the triangles share the corner P0.

🔢 **Maths: how many triangles?**

> A polygon with n corners gives **n − 2** triangles.
> square: 4 − 2 = 2, hexagon: 6 − 2 = 4

If every triangle uses the top-left rule, the inner edges of the fan have **no seams**, even with see-through colours.

⚠️ The fan only works for **convex** polygons. For a shape with a dent, some fan triangles go **outside** the shape (Practice 7). Chapter 25 fills any polygon with a different method.

### The corners of a hexagon

A regular hexagon (all sides the same length) is made of **six equilateral triangles** (triangles with all three sides the same), meeting in the centre. If the hexagon's "radius" (centre to corner) is r, every side is also r.

The two corners on the left and right are at (cx ± r, cy). The other four are half a side across and one triangle-height up or down. The height h of an equilateral triangle with side r is found with Pythagoras (Chapter 3):

> h² + (r/2)² = r² → h² = r² − r²/4 = ¾ r² → **h = r × √3 / 2**

🔢 **Maths: r = 60**

> h = 60 × 1.732 / 2 = **51.96**
> corners: (cx + 60, cy), (cx + 30, cy + 51.96), (cx − 30, cy + 51.96), (cx − 60, cy), (cx − 30, cy − 51.96), (cx + 30, cy − 51.96)
> area = 6 equilateral triangles = 6 × ½ × 60 × 51.96 ≈ **9353**

Our see-through hexagon (made with the top-left rule) has **9298** pixels. Close. ✓

---

## 24.12 Similar triangles: snow on the mountains

Our `mountains.ppm` has snow on each peak. The snow is a smaller triangle at the top of the mountain, with corners found by **lerp** (Chapter 13): a quarter of the way from the peak toward each base corner.

> snow left corner = lerp(peak, left corner, 0.25)
> snow right corner = lerp(peak, right corner, 0.25)

The snow triangle has the **same shape** as the mountain, just smaller: each side is ¼ as long. Triangles with the same shape are called **similar** triangles. Its area is ¼ × ¼ = **1/16** of the mountain's area (both the base and the height shrink to ¼).

🔢 **Maths: the front mountain** — left (−30, 170), peak (90, 30), right (210, 170)

> snow left = (90 + 0.25 × (−30 − 90), 30 + 0.25 × (170 − 30)) = (90 − 30, 30 + 35) = **(60, 65)**
> snow right = (90 + 0.25 × (210 − 90), 30 + 35) = (90 + 30, 65) = **(120, 65)**
> mountain: base 240, height 140 → area 16,800. Snow: base 60, height 35 → area 1050 = 16,800 / 16 ✓

Notice the left corner (−30, 170) is **outside** the image. That is no problem: the bounding box is clipped to the image, so we simply never visit those pixels.

---

## Code, part 1: `triangles.h`

File: `common/triangles.h` (new). It includes `ellipses.h` (and through it everything before).

```cpp
#ifndef TRIANGLES_H
#define TRIANGLES_H

#include <algorithm>
#include <cmath>
#include "ellipses.h"

struct PointF {
    double x = 0.0;
    double y = 0.0;
};

inline double edgeFunction(PointF a, PointF b, PointF p) {
    return (b.x - a.x) * (p.y - a.y) - (b.y - a.y) * (p.x - a.x);
}

inline double triangleArea(PointF a, PointF b, PointF c) {
    return std::fabs(edgeFunction(a, b, c)) / 2.0;
}

inline bool isTopLeft(PointF from, PointF to) {
    double ex = to.x - from.x;
    double ey = to.y - from.y;
    return (ey == 0.0 && ex > 0.0) || ey < 0.0;
}

inline bool edgeCovers(double e, bool topLeft) {
    return e > 0.0 || (e == 0.0 && topLeft);
}

inline void fillTriangle(Image& image, PointF a, PointF b, PointF c, Colour col,
                         double alpha = 1.0) {
    double area2 = edgeFunction(a, b, c);
    if (area2 == 0.0) {
        return;
    }
    if (area2 < 0.0) {
        std::swap(b, c);
    }
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
                if (alpha >= 1.0) {
                    image.setPixel(x, y, col);
                } else {
                    blendPixel(image, x, y, col, alpha);
                }
            }
        }
    }
}

inline void drawTriangle(Image& image, Point a, Point b, Point c, Colour col) {
    drawLine(image, a.x, a.y, b.x, b.y, col, false);
    drawLine(image, b.x, b.y, c.x, c.y, col, false);
    drawLine(image, c.x, c.y, a.x, a.y, col, false);
}

inline void fillConvexPolygon(Image& image, const std::vector<PointF>& points, Colour col,
                              double alpha = 1.0) {
    const int n = static_cast<int>(points.size());
    for (int i = 1; i + 1 < n; ++i) {
        fillTriangle(image, points[0], points[i], points[i + 1], col, alpha);
    }
}

#endif
```

### Line by line

**The start and a point type (lines 1–11)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef TRIANGLES_H` / `#define TRIANGLES_H` | Include guard. |
| 4 | `#include <algorithm>` | `std::min`, `std::max` and `std::swap`. |
| 5 | `#include <cmath>` | `std::floor`, `std::ceil`, `std::fabs`. |
| 6 | `#include "ellipses.h"` | Everything before (images, rectangles, blending, lines, circles, ellipses). |
| 8–11 | `struct PointF { double x = 0.0; double y = 0.0; };` | A point with **fractional** coordinates (F for "floating point"). The `Point` from Chapter 21 has `int`s; triangle corners can be anywhere, like (12.25, 4.5). |

**The edge function and the area (lines 13–19)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 13 | `inline double edgeFunction(PointF a, PointF b, PointF p) {` | Which side of the line A→B is P on? (Section 24.3) |
| 14 | `return (b.x - a.x) * (p.y - a.y) - (b.y - a.y) * (p.x - a.x);` | The formula: positive on the right (on the screen), negative on the left, 0 on the line. It is also twice the signed area of the triangle A, B, P. |
| 15 | `}` | End. |
| 17 | `inline double triangleArea(PointF a, PointF b, PointF c) {` | The area of a triangle. |
| 18 | `return std::fabs(edgeFunction(a, b, c)) / 2.0;` | Half of \|E(A, B, C)\| (Section 24.4). `std::fabs` removes the sign of a `double`. |
| 19 | `}` | End. |

**Top-left edges (lines 21–29)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 21 | `inline bool isTopLeft(PointF from, PointF to) {` | Is the edge from `from` to `to` a top or a left edge? (For a clockwise triangle, Section 24.10.) |
| 22–23 | `double ex = to.x - from.x;` / `double ey = to.y - from.y;` | The direction of the edge: how far across, how far down. |
| 24 | `return (ey == 0.0 && ex > 0.0) \|\| ey < 0.0;` | Top edge: horizontal and going right. Left edge: going up. |
| 25 | `}` | End. |
| 27 | `inline bool edgeCovers(double e, bool topLeft) {` | Does this one edge "allow" the pixel, given its edge value e? |
| 28 | `return e > 0.0 \|\| (e == 0.0 && topLeft);` | Clearly inside (e > 0), or exactly on the edge **and** the edge is top-left. |
| 29 | `}` | End. |

**The filled triangle (lines 31–64)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 31–32 | `inline void fillTriangle(Image& image, PointF a, PointF b, PointF c, Colour col, double alpha = 1.0) {` | Fill the triangle A, B, C. The corners may be in any order. `alpha` is optional (solid by default), like `fillCircle`. |
| 33 | `double area2 = edgeFunction(a, b, c);` | Twice the signed area. Its sign tells the orientation (Section 24.6). |
| 34–36 | `if (area2 == 0.0) { return; }` | The three corners are on one line: there is nothing to fill. |
| 37–39 | `if (area2 < 0.0) { std::swap(b, c); }` | Counter-clockwise? Swap two corners to make it clockwise. (`a`, `b`, `c` are copies, so this does not change the caller's points.) |
| 40–41 | `int x0 = static_cast<int>(std::floor(std::min({a.x, b.x, c.x})));` / `int y0 = ...;` | The top-left of the bounding box: the smallest x and y, rounded down. `std::min({ ... })` with curly brackets finds the smallest of **several** numbers. |
| 42–43 | `int x1 = static_cast<int>(std::ceil(std::max({a.x, b.x, c.x})));` / `int y1 = ...;` | The bottom-right: the largest x and y, rounded up. |
| 44 | `Rect box = clipToImage(Rect{x0, y0, x1, y1}, image);` | Clip to the image (Chapter 19). Corners outside the image are fine. |
| 45–47 | `bool topLeft0 = isTopLeft(b, c);` … `bool topLeft2 = isTopLeft(a, b);` | For each edge, decide once whether it is top-left. Edge 0 is B→C (opposite A), edge 1 is C→A, edge 2 is A→B. |
| 48–49 | `for (int y = box.y0; ...) { for (int x = box.x0; ...) {` | Every pixel in the box. |
| 50 | `PointF p{x + 0.5, y + 0.5};` | The pixel **centre**. |
| 51–53 | `double w0 = edgeFunction(b, c, p);` … `double w2 = edgeFunction(a, b, p);` | The three edge values (Section 24.5). |
| 54–55 | `if (edgeCovers(w0, topLeft0) && edgeCovers(w1, topLeft1) && edgeCovers(w2, topLeft2)) {` | Inside all three edges, using the top-left rule for pixels exactly on an edge. `&&` stops at the first "no". |
| 56–60 | `if (alpha >= 1.0) { image.setPixel(x, y, col); } else { blendPixel(image, x, y, col, alpha); }` | Solid or see-through paint. |
| 61–64 | `}` `}` `}` `}` | End of the if, the two loops, and the function. |

**The outline (lines 66–70)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 66 | `inline void drawTriangle(Image& image, Point a, Point b, Point c, Colour col) {` | The outline of a triangle with **whole-number** corners (`Point`, Chapter 21). |
| 67–69 | `drawLine(image, a.x, a.y, b.x, b.y, col, false);` … | The three edges, each without its last pixel, so every corner is drawn exactly once (Section 24.2). |
| 70 | `}` | End. |

**Convex polygons (lines 72–78)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 72–73 | `inline void fillConvexPolygon(Image& image, const std::vector<PointF>& points, Colour col, double alpha = 1.0) {` | Fill a convex polygon, given its corners in order around the edge (Section 24.11). |
| 74 | `const int n = static_cast<int>(points.size());` | The number of corners, as an `int`. |
| 75 | `for (int i = 1; i + 1 < n; ++i) {` | i = 1, 2, …, n − 2: one triangle for each. With fewer than 3 corners, the loop does nothing. |
| 76 | `fillTriangle(image, points[0], points[i], points[i + 1], col, alpha);` | The fan triangle (P0, Pi, Pi+1). Thanks to the top-left rule, the shared edges have no seams. |
| 77–78 | `}` `}` | End. |
| 80 | `#endif` | End of the include guard. |

---

## Code, part 2: mountains, seams and a colour wheel

File: `ch24/triangles.cpp`

```cpp
#include <cmath>
#include <iostream>
#include <string>
#include <vector>
#include "hsv.h"
#include "triangles.h"

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
            Colour s = p.getPixel(x, y);
            Colour t = q.getPixel(x, y);
            if (s.r != t.r || s.g != t.g || s.b != t.b) {
                return false;
            }
        }
    }
    return true;
}

enum class EdgeRule { Include, Exclude, TopLeft };

bool coversWithRule(double e, bool topLeft, EdgeRule rule) {
    if (rule == EdgeRule::Include) {
        return e >= 0.0;
    }
    if (rule == EdgeRule::Exclude) {
        return e > 0.0;
    }
    return edgeCovers(e, topLeft);
}

void paintTriangle(Image& image, PointF a, PointF b, PointF c, Colour col, double alpha,
                   EdgeRule rule) {
    if (edgeFunction(a, b, c) < 0.0) {
        std::swap(b, c);
    }
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            PointF p{x + 0.5, y + 0.5};
            bool inside = coversWithRule(edgeFunction(b, c, p), isTopLeft(b, c), rule) &&
                          coversWithRule(edgeFunction(c, a, p), isTopLeft(c, a), rule) &&
                          coversWithRule(edgeFunction(a, b, p), isTopLeft(a, b), rule);
            if (inside) {
                if (alpha >= 1.0) {
                    image.setPixel(x, y, col);
                } else {
                    blendPixel(image, x, y, col, alpha);
                }
            }
        }
    }
}

void showSharedEdge(const std::string& title, EdgeRule rule) {
    PointF p0{0.0, 0.0};
    PointF p1{8.0, 0.0};
    PointF p2{8.0, 8.0};
    PointF p3{0.0, 8.0};
    Image first(8, 8);
    Image second(8, 8);
    paintTriangle(first, p0, p1, p2, colours::white, 1.0, rule);
    paintTriangle(second, p0, p2, p3, colours::white, 1.0, rule);
    int twice = 0;
    int never = 0;
    std::cout << title << ":\n";
    for (int y = 0; y < 8; ++y) {
        std::cout << "  ";
        for (int x = 0; x < 8; ++x) {
            int count = 0;
            if (first.getPixel(x, y).r != 0) {
                ++count;
            }
            if (second.getPixel(x, y).r != 0) {
                ++count;
            }
            if (count == 0) {
                ++never;
                std::cout << '.';
            } else {
                if (count == 2) {
                    ++twice;
                }
                std::cout << count;
            }
        }
        std::cout << "\n";
    }
    std::cout << "  painted twice: " << twice << ", never painted: " << never << "\n";
}

PointF lerpPoint(PointF p, PointF q, double t) {
    return PointF{lerp(p.x, q.x, t), lerp(p.y, q.y, t)};
}

void drawMountain(Image& image, PointF left, PointF peak, PointF right, Colour col) {
    fillTriangle(image, left, peak, right, col);
    PointF capLeft = lerpPoint(peak, left, 0.25);
    PointF capRight = lerpPoint(peak, right, 0.25);
    fillTriangle(image, capLeft, peak, capRight, colours::white);
}

std::vector<PointF> hexagon(double cx, double cy, double r) {
    double h = r * std::sqrt(3.0) / 2.0;
    return {PointF{cx + r, cy}, PointF{cx + r / 2.0, cy + h}, PointF{cx - r / 2.0, cy + h},
            PointF{cx - r, cy}, PointF{cx - r / 2.0, cy - h}, PointF{cx + r / 2.0, cy - h}};
}

int main() {
    PointF a{2.0, 2.0};
    PointF b{10.0, 2.0};
    std::cout << "edge from (2, 2) to (10, 2):\n";
    std::cout << "  E at (6, 5) = " << edgeFunction(a, b, PointF{6.0, 5.0}) << "\n";
    std::cout << "  E at (6, 0) = " << edgeFunction(a, b, PointF{6.0, 0.0}) << "\n";
    std::cout << "  E at (6, 2) = " << edgeFunction(a, b, PointF{6.0, 2.0}) << "\n";

    PointF t0{1.0, 1.0};
    PointF t1{12.0, 4.0};
    PointF t2{4.0, 10.0};
    Image small(14, 12);
    fillTriangle(small, t0, t1, t2, colours::white);
    printGrid("filled triangle (1, 1), (12, 4), (4, 10)", small);
    std::cout << "pixels: " << countLit(small) << ", area: " << triangleArea(t0, t1, t2) << "\n";

    Image swapped(14, 12);
    fillTriangle(swapped, t0, t2, t1, colours::white);
    std::cout << "the other order gives the same pixels: "
              << (samePixels(small, swapped) ? "yes" : "no") << "\n";

    showSharedEdge("shared edge, rule E >= 0", EdgeRule::Include);
    showSharedEdge("shared edge, rule E > 0", EdgeRule::Exclude);
    showSharedEdge("shared edge, top-left rule", EdgeRule::TopLeft);

    Image land(320, 200);
    for (int y = 0; y < 200; ++y) {
        double t = y / 199.0;
        Colour sky = lerpColour(Colour{30, 60, 140}, Colour{250, 180, 120}, t);
        fillRect(land, Rect{0, y, 320, y + 1}, sky);
    }
    fillCircle(land, 280.5, 45.5, 20.0, Colour{255, 230, 150});
    drawMountain(land, PointF{120.0, 170.0}, PointF{230.0, 45.0}, PointF{340.0, 170.0},
                 Colour{120, 110, 150});
    drawMountain(land, PointF{-30.0, 170.0}, PointF{90.0, 30.0}, PointF{210.0, 170.0},
                 Colour{80, 70, 110});
    fillRect(land, Rect{0, 170, 320, 200}, Colour{40, 90, 50});

    Image seams(320, 160, colours::white);
    for (int x = 0; x < 320; x += 40) {
        fillRect(seams, Rect{x, 0, x + 20, 160}, Colour{200, 200, 200});
    }
    std::vector<PointF> left = hexagon(80.5, 80.5, 60.0);
    for (int i = 1; i + 1 < 6; ++i) {
        paintTriangle(seams, left[0], left[i], left[i + 1], Colour{230, 80, 30}, 0.5,
                      EdgeRule::Include);
    }
    fillConvexPolygon(seams, hexagon(240.5, 80.5, 60.0), Colour{230, 80, 30}, 0.5);

    Image wheel(200, 200, colours::white);
    PointF centre{100.0, 100.0};
    std::vector<PointF> corners = hexagon(100.0, 100.0, 90.0);
    for (int i = 0; i < 6; ++i) {
        PointF p = corners[i];
        PointF q = corners[(i + 1) % 6];
        Colour col = toColour(hsvToRgb(HSV{i * 60.0, 0.8, 1.0}));
        fillTriangle(wheel, centre, p, q, col);
        drawTriangle(wheel, Point{100, 100}, Point{roundToInt(p.x), roundToInt(p.y)},
                     Point{roundToInt(q.x), roundToInt(q.y)}, colours::black);
    }

    bool ok = land.savePPM("mountains.ppm");
    ok = ok && seams.savePPM("seams.ppm");
    ok = ok && wheel.savePPM("wheel.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
```

Build and run (from the `code/ch24` folder):

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common triangles.cpp -o triangles
./triangles
```

### Line by line

**Includes and helpers (lines 1–48)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1 | `#include <cmath>` | `std::sqrt` for the hexagon. |
| 2–4 | `#include <iostream>` / `<string>` / `<vector>` | Printing, text, and lists of points. |
| 5 | `#include "hsv.h"` | `hsvToRgb` for the rainbow colours (Chapter 16). It is not in the drawing chain, so we include it as well. |
| 6 | `#include "triangles.h"` | Our new header. |
| 8–48 | `printGrid`, `countLit`, `samePixels` | The same helpers as Chapter 23. |

**Three rules for comparison (lines 50–82)**

To **see** the shared-edge problem, we need triangle fillers with the two "wrong" rules. These live only in this program; the library always uses the top-left rule.

| Line | Code | What it does, in simple words |
|---|---|---|
| 50 | `enum class EdgeRule { Include, Exclude, TopLeft };` | A small type with three named values: "E ≥ 0", "E > 0", and the top-left rule. |
| 52 | `bool coversWithRule(double e, bool topLeft, EdgeRule rule) {` | Like `edgeCovers`, but with a choice of rule. |
| 53–55 | `if (rule == EdgeRule::Include) { return e >= 0.0; }` | Rule 1: on the edge counts as inside. |
| 56–58 | `if (rule == EdgeRule::Exclude) { return e > 0.0; }` | Rule 2: on the edge counts as outside. |
| 59–60 | `return edgeCovers(e, topLeft);` `}` | Otherwise: the top-left rule from the library. |
| 62–63 | `void paintTriangle(Image& image, PointF a, PointF b, PointF c, Colour col, double alpha, EdgeRule rule) {` | A simple triangle filler with a chosen rule. |
| 64–66 | `if (edgeFunction(a, b, c) < 0.0) { std::swap(b, c); }` | Make the triangle clockwise. |
| 67–68 | `for (int y = 0; ...) { for (int x = 0; ...) {` | Every pixel of the image. (No bounding box: these images are small, and the code stays short.) |
| 69 | `PointF p{x + 0.5, y + 0.5};` | The pixel centre. |
| 70–72 | `bool inside = coversWithRule(edgeFunction(b, c, p), isTopLeft(b, c), rule) && ...;` | The same three tests as `fillTriangle`, with the chosen rule. |
| 73–79 | `if (inside) { if (alpha >= 1.0) { ... } else { ... } }` | Paint the pixel, solid or see-through. |
| 80–82 | `}` `}` `}` | End. |

**Counting the paint on a shared edge (lines 84–119)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 84 | `void showSharedEdge(const std::string& title, EdgeRule rule) {` | The experiment of Section 24.9, with one rule. |
| 85–88 | `PointF p0{0.0, 0.0};` … `PointF p3{0.0, 8.0};` | The four corners of an 8 × 8 square. |
| 89–90 | `Image first(8, 8);` / `Image second(8, 8);` | One black image per triangle, so we can see which triangle painted which pixel. |
| 91 | `paintTriangle(first, p0, p1, p2, colours::white, 1.0, rule);` | Triangle 1: the upper-right half. |
| 92 | `paintTriangle(second, p0, p2, p3, colours::white, 1.0, rule);` | Triangle 2: the lower-left half. They share the diagonal p0–p2. |
| 93–94 | `int twice = 0;` / `int never = 0;` | Counters for the problems. |
| 96–98 | the two `for` loops | Every pixel. |
| 99–105 | `int count = 0; if (first.getPixel(x, y).r != 0) { ++count; } if (second...) { ++count; }` | How many of the two triangles painted this pixel: 0, 1 or 2. (White has r = 255, black has r = 0.) |
| 106–108 | `if (count == 0) { ++never; std::cout << '.'; }` | Never painted: a hole. Print a dot. |
| 109–114 | `} else { if (count == 2) { ++twice; } std::cout << count; }` | Painted once or twice: print the number. |
| 116–119 | `std::cout << "\n";` … `std::cout << "  painted twice: " ...` | End of a row; at the end, print the two counters. |

**Mountains (lines 121–130)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 121–123 | `PointF lerpPoint(PointF p, PointF q, double t) { return PointF{lerp(p.x, q.x, t), lerp(p.y, q.y, t)}; }` | The point a fraction t of the way from p to q: lerp the x's and the y's (Chapter 13). |
| 125 | `void drawMountain(Image& image, PointF left, PointF peak, PointF right, Colour col) {` | A mountain with snow on top. |
| 126 | `fillTriangle(image, left, peak, right, col);` | The mountain itself. |
| 127–128 | `PointF capLeft = lerpPoint(peak, left, 0.25);` / `PointF capRight = ...;` | A quarter of the way down each side (Section 24.12). |
| 129 | `fillTriangle(image, capLeft, peak, capRight, colours::white);` | The white snow cap: a similar triangle, ¼ of the size. |
| 130 | `}` | End. |

**The hexagon's corners (lines 132–136)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 132 | `std::vector<PointF> hexagon(double cx, double cy, double r) {` | The six corners of a regular hexagon with centre (cx, cy) and radius r. |
| 133 | `double h = r * std::sqrt(3.0) / 2.0;` | The height of each equilateral triangle: r√3 / 2 (Section 24.11). |
| 134–135 | `return {PointF{cx + r, cy}, ...};` | The corners in order: right, lower right, lower left, left, upper left, upper right. On the screen (y down), that goes **clockwise**. |
| 136 | `}` | End. |

**The text output (lines 138–161)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 139–144 | `PointF a{2.0, 2.0};` … `edgeFunction(a, b, PointF{6.0, 2.0})` | The three edge values from Section 24.3: 24, −16, 0. |
| 146–152 | `PointF t0{1.0, 1.0};` … `triangleArea(t0, t1, t2)` | Fill the small triangle of Section 24.7, print it, and print its pixel count and true area. |
| 154–157 | `Image swapped(14, 12);` … `samePixels(small, swapped)` | Fill it again with the corners in the other order (t0, t2, t1), and compare (Section 24.6). |
| 159–161 | the three `showSharedEdge` calls | The experiment of Sections 24.9 and 24.10, once with each rule. |

**The mountain picture (lines 163–174)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 163 | `Image land(320, 200);` | The picture. |
| 164–168 | `for (int y = 0; y < 200; ++y) { ... lerpColour(...) ... fillRect(land, Rect{0, y, 320, y + 1}, sky); }` | The sky: a gradient from dark blue at the top to warm orange at the bottom (Chapter 13), one row at a time. |
| 169 | `fillCircle(land, 280.5, 45.5, 20.0, Colour{255, 230, 150});` | A pale sun, high on the right, in the open sky. |
| 170–171 | `drawMountain(land, PointF{120.0, 170.0}, PointF{230.0, 45.0}, PointF{340.0, 170.0}, Colour{120, 110, 150});` | The **back** mountain, in a light, misty purple. Its right corner (340) is outside the image: that is fine. |
| 172–173 | `drawMountain(land, PointF{-30.0, 170.0}, PointF{90.0, 30.0}, PointF{210.0, 170.0}, Colour{80, 70, 110});` | The **front** mountain, darker, drawn **after** the back one, so it covers it (the painter's order). |
| 174 | `fillRect(land, Rect{0, 170, 320, 200}, Colour{40, 90, 50});` | Green ground along the bottom. |

**The seams picture (lines 176–185)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 176 | `Image seams(320, 160, colours::white);` | A white picture. |
| 177–179 | `for (int x = 0; x < 320; x += 40) { fillRect(seams, Rect{x, 0, x + 20, 160}, Colour{200, 200, 200}); }` | Grey stripes, 20 pixels wide, so we can see through the see-through hexagons. |
| 180 | `std::vector<PointF> left = hexagon(80.5, 80.5, 60.0);` | The left hexagon's corners. Its centre is a **pixel centre**, so the line from the right corner to the left corner runs exactly through a row of pixel centres (row 80). |
| 181–184 | `for (int i = 1; i + 1 < 6; ++i) { paintTriangle(seams, left[0], left[i], left[i + 1], ..., 0.5, EdgeRule::Include); }` | A fan of 4 half-transparent triangles with the **"E ≥ 0"** rule: the shared edges are painted twice. |
| 185 | `fillConvexPolygon(seams, hexagon(240.5, 80.5, 60.0), Colour{230, 80, 30}, 0.5);` | The same hexagon on the right, with the library (top-left rule). |

**The colour wheel (lines 187–197)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 187 | `Image wheel(200, 200, colours::white);` | A white picture. |
| 188 | `PointF centre{100.0, 100.0};` | The centre of the wheel. |
| 189 | `std::vector<PointF> corners = hexagon(100.0, 100.0, 90.0);` | Six corners, 90 pixels from the centre. |
| 190 | `for (int i = 0; i < 6; ++i) {` | Six slices. |
| 191–192 | `PointF p = corners[i];` / `PointF q = corners[(i + 1) % 6];` | Two neighbouring corners. `% 6` makes the last slice use corner 5 and corner **0**, closing the wheel. |
| 193 | `Colour col = toColour(hsvToRgb(HSV{i * 60.0, 0.8, 1.0}));` | Hues 0°, 60°, 120°, …: red, yellow, green, cyan, blue, magenta (Chapter 16). |
| 194 | `fillTriangle(wheel, centre, p, q, col);` | The slice. |
| 195–196 | `drawTriangle(wheel, Point{100, 100}, Point{roundToInt(p.x), roundToInt(p.y)}, Point{roundToInt(q.x), roundToInt(q.y)}, colours::black);` | A black outline. `drawTriangle` needs whole numbers, so we round the corners (Chapter 20). |
| 197 | `}` | End of the loop. |

**Saving (lines 199–207)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 199–201 | `bool ok = land.savePPM("mountains.ppm");` … | Save the three pictures. |
| 202–207 | `if (!ok) { ... return 1; }` `return 0;` `}` | Report a problem, or finish. |

### What you should see

The program prints:

```
edge from (2, 2) to (10, 2):
  E at (6, 5) = 24
  E at (6, 0) = -16
  E at (6, 2) = 0
filled triangle (1, 1), (12, 4), (4, 10):
  ..............
  .##...........
  .#####........
  ..########....
  ..#########...
  ..########....
  ...######.....
  ...####.......
  ...###........
  ....#.........
  ..............
  ..............
pixels: 46, area: 45
the other order gives the same pixels: yes
shared edge, rule E >= 0:
  21111111
  12111111
  11211111
  11121111
  11112111
  11111211
  11111121
  11111112
  painted twice: 8, never painted: 0
shared edge, rule E > 0:
  .1111111
  1.111111
  11.11111
  111.1111
  1111.111
  11111.11
  111111.1
  1111111.
  painted twice: 0, never painted: 8
shared edge, top-left rule:
  11111111
  11111111
  11111111
  11111111
  11111111
  11111111
  11111111
  11111111
  painted twice: 0, never painted: 0
```

Open the pictures:
- `mountains.ppm`: an evening sky, a pale sun, two purple mountains with white snow caps (the dark one in front), and green ground.
- `seams.ppm`: two orange see-through hexagons over grey stripes. The **left** one has a thin, darker orange line straight across its middle: 121 pixels were blended more than once (the shared edge from the right corner to the left corner). The **right** one, made with the top-left rule, is perfectly even.
- `wheel.ppm`: a hexagon cut into six rainbow slices, each with a black outline.

---

## Small examples

### Example 1 — Which side?

Edge from (2, 1) to (8, 5). Where is P = (8, 1)?

> E = (8 − 2)(1 − 1) − (5 − 1)(8 − 2) = 0 − 24 = **−24** → on the **left**

Check: walking from (2, 1) down-right to (8, 5), your left hand points up-right — toward (8, 1). ✓

### Example 2 — The area of a triangle in one line

Triangle (0, 0), (6, 0), (0, 4):

> E = (6 − 0)(4 − 0) − (0 − 0)(0 − 0) = 24 → area = 24 / 2 = **12**
> Check: right angle at (0, 0), base 6, height 4 → ½ × 6 × 4 = 12 ✓

### Example 3 — Orientation of a hexagon

Our hexagon starts at the right corner (r, 0), then goes to the lower right (r/2, h), then the lower left (−r/2, h), all measured from the centre. With r = 60, h = 51.96:

> E(P0, P1, P2) = (30 − 60)(51.96 − 0) − (51.96 − 0)(−30 − 60)
> = −30 × 51.96 + 51.96 × 90 = 51.96 × 60 = **3118** > 0 → **clockwise** ✓

### Example 4 — The edge function as a ruler

Edge A = (0, 0) → B = (3, 4). Its length is √(9 + 16) = 5. For P = (4, 0):

> E = 3 × 0 − 4 × 4 = −16
> distance from P to the line = |E| / length = 16 / 5 = **3.2** pixels

### Example 5 — A square from two triangles

```cpp
fillTriangle(img, PointF{10, 10}, PointF{50, 10}, PointF{50, 40}, c, 0.5);
fillTriangle(img, PointF{10, 10}, PointF{50, 40}, PointF{10, 40}, c, 0.5);
```

Even with alpha 0.5, the square is perfectly even: the diagonal pixels belong to exactly one triangle. (The result is the same as `fillRectAlpha` from Chapter 19.)

---

## Common mistakes

⚠️ **Forgetting the orientation check.** Without it, a triangle given counter-clockwise has all its w's negative, and **nothing** is drawn. Half of your triangles vanish!

⚠️ **Testing the pixel corner (x, y) instead of the centre (x + 0.5, y + 0.5).** The triangle shifts by half a pixel.

⚠️ **Using "E ≥ 0" for every edge.** Seams where see-through triangles meet.

⚠️ **Using "E > 0" for every edge.** Holes where triangles meet.

⚠️ **Mixing up the edge order in `isTopLeft`.** The edge B→C and the edge C→B are opposite directions: one is "left", the other is not. Use the same order as the edge functions (B→C, C→A, A→B).

⚠️ **Using the fan on a shape with a dent.** Some triangles cover pixels outside the shape (Practice 7).

⚠️ **Testing every pixel of the image.** Use the bounding box of the three corners.

---

## Practice

🏋️ **1.** Compute E for the edge (2, 1) → (8, 5) at P = (4, 6). Which side is P on?

🏋️ **2.** Is pixel (5, 2) inside the triangle (1, 1), (12, 4), (4, 10)? Compute w0, w1 and w2 at its centre. Check your answer against the printed grid.

🏋️ **3.** For the triangle A = (0, 0), B = (10, 0), C = (5, 8): is it clockwise? Which of its edges are top edges, and which are left edges?

🏋️ **4.** What is the area of the triangle (2, 3), (10, 5), (4, 9)?

🏋️ **5.** Write `fillTriangleFast`, which computes w0, w1 and w2 once at the start of each row, and then only **adds** fixed steps for each pixel (Section 24.8).

🏋️ **6.** Fill a "diamond" with corners (cx, cy − h), (cx + w, cy), (cx, cy + h), (cx − w, cy) using `fillConvexPolygon`. How many triangles does it use? What is its area?

🏋️ **7.** The arrow-head shape (0, 0), (10, 5), (0, 10), (3, 5) has a dent at (3, 5). What goes wrong with the fan from the first corner? Which corner should the fan start from instead?

🏋️ **8.** With the top-left rule, how many pixels of the 8 × 8 square does triangle 1 (upper right) paint, and how many does triangle 2 paint?

---

## Answers

**1.**
> E = (8 − 2)(6 − 1) − (5 − 1)(4 − 2) = 6 × 5 − 4 × 2 = 30 − 8 = **22** > 0 → on the **right**
> (Walking down-right from (2, 1), your right hand points down-left — toward (4, 6). ✓)

**2.**
> P = (5.5, 2.5), A = (1, 1), B = (12, 4), C = (4, 10)
> w0 = E(B, C, P) = (4 − 12)(2.5 − 4) − (10 − 4)(5.5 − 12) = 12 + 39 = **51**
> w1 = E(C, A, P) = (1 − 4)(2.5 − 10) − (1 − 10)(5.5 − 4) = 22.5 + 13.5 = **36**
> w2 = E(A, B, P) = (12 − 1)(2.5 − 1) − (4 − 1)(5.5 − 1) = 16.5 − 13.5 = **3**
> All positive → **inside**. (Check: 51 + 36 + 3 = 90 ✓.) In the grid, row 2 is `.#####........`: columns 1 to 5 are lit, so column 5 is inside ✓.

**3.**
> E(A, B, C) = (10)(8) − (0)(5) = 80 > 0 → **clockwise** ✓
> A → B: (0, 0) → (10, 0): ey = 0, ex = 10 > 0 → **top** edge
> B → C: (10, 0) → (5, 8): ey = 8 > 0 → not top-left (a right edge)
> C → A: (5, 8) → (0, 0): ey = −8 < 0 → **left** edge

On the screen: the horizontal side at the top, and the slanted side on the left, as the names say.

**4.**
> E = (10 − 2)(9 − 3) − (5 − 3)(4 − 2) = 8 × 6 − 2 × 2 = 48 − 4 = 44 → area = **22**

**5.**

```cpp
inline void fillTriangleFast(Image& image, PointF a, PointF b, PointF c, Colour col) {
    double area2 = edgeFunction(a, b, c);
    if (area2 == 0.0) {
        return;
    }
    if (area2 < 0.0) {
        std::swap(b, c);
    }
    int x0 = static_cast<int>(std::floor(std::min({a.x, b.x, c.x})));
    int y0 = static_cast<int>(std::floor(std::min({a.y, b.y, c.y})));
    int x1 = static_cast<int>(std::ceil(std::max({a.x, b.x, c.x})));
    int y1 = static_cast<int>(std::ceil(std::max({a.y, b.y, c.y})));
    Rect box = clipToImage(Rect{x0, y0, x1, y1}, image);
    bool topLeft0 = isTopLeft(b, c);
    bool topLeft1 = isTopLeft(c, a);
    bool topLeft2 = isTopLeft(a, b);
    double step0 = -(c.y - b.y);
    double step1 = -(a.y - c.y);
    double step2 = -(b.y - a.y);
    for (int y = box.y0; y < box.y1; ++y) {
        PointF p{box.x0 + 0.5, y + 0.5};
        double w0 = edgeFunction(b, c, p);
        double w1 = edgeFunction(c, a, p);
        double w2 = edgeFunction(a, b, p);
        for (int x = box.x0; x < box.x1; ++x) {
            if (edgeCovers(w0, topLeft0) && edgeCovers(w1, topLeft1) &&
                edgeCovers(w2, topLeft2)) {
                image.setPixel(x, y, col);
            }
            w0 += step0;
            w1 += step1;
            w2 += step2;
        }
    }
}
```

Each step is the "one step right" change from Section 24.8: −(end.y − start.y) for each edge. With whole-number or half-number corners, the additions are exact, so you get exactly the same pixels as `fillTriangle`. (With strange fractions like 0.1, tiny rounding errors can add up over a long row. That is why the code starts each row fresh.)

**6.** 4 corners → 4 − 2 = **2** triangles. The diamond is two triangles with base 2w (the horizontal middle line) and height h each:

> area = 2 × ½ × 2w × h = **2wh**

(Check: the diamond fits in a box 2w × 2h = 4wh, and fills exactly half of it.)

**7.** The fan from P0 = (0, 0) makes (P0, P1, P2) = (0, 0), (10, 5), (0, 10) — the **whole** big triangle, including the dent — and (P0, P2, P3) = (0, 0), (0, 10), (3, 5), which is exactly the dent. Both are painted, so the dent is filled in: the arrow-head becomes a plain triangle.

Start the fan from the dent corner P3 = (3, 5) instead: (P3, P0, P1) and (P3, P1, P2). Both triangles are inside the arrow-head, and together they cover it exactly. (In general, a shape with dents needs a better method — Chapter 25.)

**8.** Triangle 1 takes the diagonal (Section 24.10), so it paints every pixel with x ≥ y:

> row 0: 8, row 1: 7, …, row 7: 1 → 8 + 7 + … + 1 = **36**

Triangle 2 paints the pixels with x < y: 64 − 36 = **28**. Together: 64, each once. ✓

---

## Summary

🧠 The **edge function** E(A, B, P) = (B.x − A.x)(P.y − A.y) − (B.y − A.y)(P.x − A.x). On the screen: **> 0 right**, **< 0 left**, **= 0 on the line**.

🧠 |E(A, B, P)| = **2 × area** of triangle ABP = length of AB × distance from P to the line.

🧠 **E(A, B, C) > 0** → clockwise on the screen. If it is negative, **swap B and C**. If it is 0, the triangle is flat.

🧠 **Inside** a clockwise triangle: w0 = E(B, C, P), w1 = E(C, A, P), w2 = E(A, B, P) are all ≥ 0. And **w0 + w1 + w2 = E(A, B, C)**.

🧠 Fill: bounding box of the corners, pixel **centres**, three tests.

🧠 E changes by a **fixed step** per pixel: −(B.y − A.y) to the right, +(B.x − A.x) down.

🧠 **Top-left rule**: a pixel exactly on an edge belongs to the triangle only if the edge is a **top** edge (horizontal, going right) or a **left** edge (going up). Shared edges: no seams, no holes.

🧠 A **convex** polygon with n corners = a **fan** of n − 2 triangles.

---

## Next chapter

The fan only works for convex shapes. What about a star, the letter "C", or a shape drawn by the user with the mouse? In Chapter 25 we learn **scanline filling**, which fills any polygon row by row, and **flood fill**, the "paint bucket" of every paint program, which fills an area by spreading from one pixel to its neighbours.
