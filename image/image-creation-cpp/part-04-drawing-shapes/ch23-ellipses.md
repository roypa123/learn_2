# Chapter 23 — Ellipses

> **Part 4 · Chapter 23 of 82**
> **You need:** Chapters 1–22 · **You will make:** `ellipses.h` (filled ellipses, ellipse outlines with the midpoint method), `eye.ppm`, `egg.ppm` and `orbits.ppm`

---

## What you will learn

- What an **ellipse** is: a circle that has been **stretched** (or squashed).
- Its two sizes: the **horizontal radius a** and the **vertical radius b**.
- The **equation of an ellipse**, (x/a)² + (y/b)² = 1, and where it comes from.
- The **integer form**, b²x² + a²y² = a²b², which needs no division.
- How to draw a **filled** ellipse with the pixel-centre test and a bounding box (just like `fillCircle`).
- Why an ellipse has only **four-way** symmetry, not eight.
- The **midpoint ellipse algorithm**, which needs **two regions**: one where we step along x, and one where we step along y.
- How to make every number a whole number with a "**multiply by 4**" trick.
- Why we need **`long long`** for big ellipses.
- That a **circle is just an ellipse with a = b**.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **ellipse** | A stretched circle: a smooth, closed, oval curve. |
| **oval** | An everyday word for an egg-like or ellipse-like shape. |
| **horizontal radius** (a) | How far the ellipse reaches to the left and right of its centre. |
| **vertical radius** (b) | How far the ellipse reaches up and down from its centre. |
| **axis** (plural: **axes**) | Here: the line through the centre along the longest or shortest direction of the ellipse. |
| **major axis** | The **long** axis (length 2 × the bigger radius). |
| **minor axis** | The **short** axis (length 2 × the smaller radius). |
| **stretch** | Make something longer in one direction by multiplying its positions by a number. |
| **region** | A part of something. Here: a part of the ellipse where one rule is used. |
| **tangent** | A straight line that just touches a curve at one point, going the same way as the curve there. |
| **focus** (plural: **foci**) | One of two special points inside an ellipse (Section 23.13). |
| **overflow** | When a number becomes too big for its type and turns into nonsense (Chapter 4). |

---

## 23.1 What is an ellipse?

📖 **New word: ellipse** — a circle that has been **stretched** in one direction. You see ellipses everywhere:

- A round plate, seen from the side, looks like an ellipse.
- The top of a glass of water, seen from an angle, is an ellipse.
- A rugby ball, seen from the side, looks like an ellipse.
- The paths of the planets around the Sun are ellipses.

📖 **New word: oval** — the everyday word for shapes like this.

A circle has **one** radius, r: the same distance in every direction. An ellipse has **two**:

📖 **New word: horizontal radius (a)** — the distance from the centre to the left or right edge.

📖 **New word: vertical radius (b)** — the distance from the centre to the top or bottom edge.

```
                 b
          ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
      ▄▀▀        │        ▀▀▄
     █           │           █
     █    a      ●───────────█     ● = centre
     █                       █
      ▀▄▄                 ▄▄▀
          ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
```

- If **a > b**, the ellipse is **wide** (like a lying-down egg).
- If **a < b**, the ellipse is **tall** (like a standing-up egg).
- If **a = b**, it is a **circle**, with r = a = b.

📖 **New word: axis** — a line through the centre. The ellipse has two important axes:

📖 **New word: major axis** — the **long** one. Its length is 2 × (the bigger radius).

📖 **New word: minor axis** — the **short** one. Its length is 2 × (the smaller radius).

🔢 **Maths: an ellipse with a = 6 and b = 3**

> It reaches 6 pixels left and right of the centre, and 3 pixels up and down.
> width = 2 × 6 = 12 (the major axis, horizontal)
> height = 2 × 3 = 6 (the minor axis, vertical)
> It is **twice as wide as it is tall**.

💡 **In this chapter, the axes of our ellipses are always horizontal and vertical** (lined up with the pixel grid). A **tilted** ellipse needs rotation, which we learn in Chapter 31.

---

## 23.2 The equation: a stretched circle

We already know the circle very well (Chapter 22). Let us **build** the ellipse from it.

### Step 1: the unit circle

Take a circle with centre (0, 0) and radius **1**. (A circle with radius 1 is called the **unit circle**.) Its equation is:

> u² + v² = 1

(We call the positions u and v here, so we do not mix them up with x and y later.)

### Step 2: stretch it

📖 **New word: stretch** — multiply every position by a number. Stretching by 6 in the horizontal direction means: every x-position becomes 6 times bigger.

Now stretch the unit circle:
- horizontally by **a**: x = a × u
- vertically by **b**: y = b × v

🔢 **Maths: stretching four points of the unit circle (a = 6, b = 3)**

| point on the unit circle (u, v) | x = 6u | y = 3v | new point (x, y) |
|---|---|---|---|
| (1, 0) right | 6 | 0 | (6, 0) |
| (0, 1) bottom | 0 | 3 | (0, 3) |
| (−1, 0) left | −6 | 0 | (−6, 0) |
| (0, −1) top | 0 | −3 | (0, −3) |

The circle has become **12 wide and 6 tall**: our ellipse.

### Step 3: turn it round

We want a test for (x, y), not for (u, v). From x = a·u we get u = x / a. From y = b·v we get v = y / b. Put these into u² + v² = 1:

> **(x / a)² + (y / b)² = 1**

This is the **equation of an ellipse** with centre (0, 0).

🧠 **Remember:** dividing x by a "un-stretches" it. After un-stretching, the point is on the unit circle, and the unit-circle test is easy.

### With any centre

If the centre is (cx, cy), we measure from the centre first (just like the circle in Chapter 22):

> **((x − cx) / a)² + ((y − cy) / b)² = 1**

### Inside, on, outside

| value of (x/a)² + (y/b)² | the point is… |
|---|---|
| less than 1 | **inside** the ellipse |
| exactly 1 | **on** the ellipse |
| more than 1 | **outside** the ellipse |

🔢 **Maths: four points and the ellipse a = 6, b = 3 (centre (0, 0))**

> (6, 0): (6/6)² + (0/3)² = 1 + 0 = **1** → on
> (0, 3): (0/6)² + (3/3)² = 0 + 1 = **1** → on
> (3, 2): (3/6)² + (2/3)² = 0.25 + 0.444 = **0.694** → inside
> (5, 2): (5/6)² + (2/3)² = 0.694 + 0.444 = **1.139** → outside

💡 Look at (3, 2) and (5, 2). They are in the same row, but one is inside and one is outside. Going right, the value grows, and at some x between 3 and 5 it crosses 1. That crossing is the edge of the ellipse in that row.

### Check: is the circle a special case?

Put a = b = r:

> (x / r)² + (y / r)² = 1
> multiply both sides by r²: x² + y² = r²

That is exactly the circle equation from Chapter 22. ✓

---

## 23.3 The integer form: no division

Division is slow, and with whole numbers it is dangerous (in C++, `5 / 6` is **0** for `int`s!). We can remove the division completely.

Multiply both sides of (x/a)² + (y/b)² = 1 by **a²b²**:

> (x² / a²) × a²b² + (y² / b²) × a²b² = 1 × a²b²
> the a² cancels in the first part, the b² cancels in the second part:
> **b²x² + a²y² = a²b²**

This is the **integer form**. If a, b, x and y are whole numbers, every part is a whole number.

🔢 **Maths: the same four points with the integer form (a = 6, b = 3)**

> a² = 36, b² = 9, a²b² = 36 × 9 = **324**
> (6, 0): 9 × 36 + 36 × 0 = 324 → **= 324** → on
> (0, 3): 9 × 0 + 36 × 9 = 324 → **= 324** → on
> (3, 2): 9 × 9 + 36 × 4 = 81 + 144 = 225 → **< 324** → inside
> (5, 2): 9 × 25 + 36 × 4 = 225 + 144 = 369 → **> 324** → outside

Same answers as Section 23.2. Multiplying both sides by a positive number never changes "less than" into "more than", so the test stays correct.

🧠 **Remember:**

> inside or on: **b²·dx² + a²·dy² ≤ a²·b²**, where dx = x − cx and dy = y − cy

⚠️ Watch the letters: the **x** part is multiplied by **b²**, and the **y** part by **a²**. They are "crossed over". If you mix them up, you get the tall ellipse instead of the wide one.

---

## 23.4 Filled ellipses

A filled ellipse works exactly like `fillCircle` (Chapter 22, Section 22.2):

1. Find the **bounding box**.
2. Clip it to the image.
3. For every pixel in the box, test its **centre** (x + 0.5, y + 0.5).

### The bounding box

The ellipse reaches a to the left and right, and b up and down. So its box is:

> from (cx − a, cy − b) to (cx + a, cy + b)

As in Chapter 22, we round the start **down** (floor) and the end **up** (ceil), and use a half-open rectangle.

🔢 **Maths: the box of an ellipse with centre (6.5, 3.5), a = 6, b = 3**

> x0 = floor(6.5 − 6) = floor(0.5) = 0, x1 = ceil(6.5 + 6) = ceil(12.5) = 13
> y0 = floor(3.5 − 3) = floor(0.5) = 0, y1 = ceil(3.5 + 3) = ceil(6.5) = 7
> box = [0, 13) × [0, 7) → **13 × 7** pixels

### The test for each pixel

> dx = (x + 0.5) − cx
> dy = (y + 0.5) − cy
> colour the pixel if b²·dx² + a²·dy² ≤ a²·b²

🔢 **Maths: two pixels of this ellipse**

> pixel (1, 2): dx = 1.5 − 6.5 = −5, dy = 2.5 − 3.5 = −1
> 9 × 25 + 36 × 1 = 225 + 36 = 261 ≤ 324 → **inside** ✓
>
> pixel (1, 1): dx = −5, dy = 1.5 − 3.5 = −2
> 9 × 25 + 36 × 4 = 225 + 144 = 369 > 324 → **outside**

Our program prints the whole filled ellipse:

```
  ......#......
  ..#########..
  .###########.
  #############
  .###########.
  ..#########..
  ......#......
```

It is **55 pixels**. Do you see the four single pixels at the ends: the top, the bottom, the far left and the far right? These are the "**spikes**" from Chapter 22 again. Those four pixel centres lie **exactly on** the ellipse (for example pixel (12, 3): dx = 6, dy = 0, and 9 × 36 + 0 = 324, exactly a²b²), and our test uses ≤, so they are coloured. For radii that are not whole numbers, the spikes usually disappear: with a = 5.9 and b = 2.9, the four end pixels are outside, and the ellipse has 51 pixels with a smooth edge.

### Checking with the area

The area of an ellipse is like the area of a circle, πr², but with r × r replaced by a × b:

> **area = π × a × b**

🔢 **Maths: the area of our ellipse**

> π × 6 × 3 = 3.14159 × 18 ≈ **56.5**
> Our pixel count: **55**. Close. ✓

💡 Why π·a·b? Stretching a shape by a in one direction makes its area a times bigger, and stretching by b in the other direction makes it b times bigger again. The unit circle has area π × 1² = π. So the ellipse has area π × a × b.

---

## 23.5 Four-way symmetry (not eight)

A circle has **eight-way** symmetry (Chapter 22, Section 22.4). We used it to compute only 1/8 of the circle. Does an ellipse have it too?

Some of the symmetry is still there. If (x, y) is on the ellipse, then so are:

> (x, y), (−x, y), (−x, −y), (x, −y)

because squaring removes the minus signs: (−x)² = x². These are the four **mirror images**:
- flip left–right (the vertical axis is a mirror),
- flip up–down (the horizontal axis is a mirror),
- and both.

But the other four copies of the circle **swap** x and y: (y, x), (−y, x) and so on. Is that allowed for an ellipse?

🔢 **Maths: swap the point (6, 0) on the ellipse a = 6, b = 3**

> (6, 0) is on the ellipse: 9 × 36 + 36 × 0 = 324 ✓
> swapped: (0, 6): 9 × 0 + 36 × 36 = 1296 → **not** 324 → **not on** the ellipse ✗

Swapping x and y turns a **wide** ellipse into a **tall** one. It only works when a = b (a circle). So an ellipse has only **four-way symmetry**: we must compute **one quarter** of it, not one eighth.

Which quarter? We use offsets (x, y) with x ≥ 0 and y ≥ 0. Because y goes **down** (Chapter 3), that is the **bottom-right** quarter of the picture: from the bottom point (0, b) to the right point (a, 0).

```
          ▄▄▄▄▄▄▄▄▄
      ▄▀▀    │    ▀▀▄
     █       │       █
     █───────●───────█ (a, 0)
     █       │      ░█   ← we compute this quarter,
      ▀▄▄    │   ░░▄▀      from (0, b) to (a, 0),
          ▀▀▀▀░░░░         then mirror it 4 ways
           (0, b)
```

---

## 23.6 Why one region is not enough

In the circle (Chapter 22), our octant went from (r, 0) to the 45° point. In that octant, the circle is **steep**: every step goes one row (y + 1), and the only question was "does x stay, or go one left?".

For an ellipse quarter, from the bottom point (0, b) to the side point (a, 0), the curve **changes** how steep it is:

- Near the **bottom point** (0, b), the curve is almost **flat** (horizontal). It goes right a lot, and up only a little.
- Near the **side point** (a, 0), the curve is almost **vertical**. It goes up a lot, and right only a little.

```
                        ● (a, 0)
                        █     ← steep here: step y, sometimes x
                        █
                      ▄▀
                  ▄▄▀▀
  (0, b) ●▄▄▄▄▄▄▀▀            ← flat here: step x, sometimes y
```

Remember the lesson of lines (Chapter 20): to avoid gaps, we must step along the direction that **changes the most**.
- Where the curve is flat, x changes most: **step x by 1** every time, and decide about y.
- Where the curve is steep, y changes most: **step y by 1** every time, and decide about x.

📖 **New word: region** — a part of the curve where one rule is used. We split the quarter into **two regions**:

| | Region 1 | Region 2 |
|---|---|---|
| where | from the bottom point (0, b) to the "45° point" | from the 45° point to the side point (a, 0) |
| the curve is | flat (it moves less than 1 row per column) | steep (it moves less than 1 column per row) |
| every step | x = x + 1 | y = y − 1 |
| the question | does y stay, or go one up (y − 1)? | does x stay, or go one right (x + 1)? |

(In a circle, Region 1 is one octant and Region 2 is the next octant. Four quadrants × two regions = eight octants. The circle's eight-way trick is just this, plus the swap.)

### Where does Region 1 end?

📖 **New word: tangent** — the straight line that just touches a curve at one point, going in the same direction as the curve there. "How steep the curve is" means "how steep its tangent is".

Region 1 ends where the tangent has slope exactly −1 (it goes 1 down for every 1 across, a 45° line). We can find this point **without** any new maths, with a "balance" idea.

### The balance idea

Stand on the ellipse at (x, y). The value b²x² + a²y² is exactly a²b² there. Now move a little:

- One step right, x → x + 1, makes b²x² bigger by about **2b²x** (because (x + 1)² = x² + 2x + 1, and 2x is the big part).
- One step in y, toward the centre (y → y − 1), makes a²y² smaller by about **2a²y**.

To stay **on** the ellipse after stepping right, the total must stay a²b², so y must move toward the centre to remove the extra 2b²x. Each full step of y removes about 2a²y. So:

> how far y must move for one step of x ≈ **2b²x / 2a²y**

- If 2b²x < 2a²y, this is **less than 1**: the curve moves less than one row per column → **flat** → Region 1.
- If 2b²x ≥ 2a²y, this is **1 or more** → **steep** → Region 2.

🧠 **Remember:** stay in Region 1 while **b²x < a²y**. (We dropped the 2 on both sides — it does not change the comparison.)

🔢 **Maths: where is the switch for a = 6, b = 3?**

> b²x = a²y → 9x = 36y → **x = 4y**
> Which point on the ellipse has x = 4y?
> 9 × (4y)² + 36 × y² = 324 → 144y² + 36y² = 324 → 180y² = 324 → y² = 1.8 → y ≈ 1.34
> x = 4 × 1.34 ≈ 5.37
> So Region 1 is from (0, 3) to about (5.37, 1.34), and Region 2 is from there to (6, 0).

🔢 **Maths: check the balance idea with real numbers (a = 6, b = 3)**

> Near the bottom point, at x = 1: the true y is 3 × √(1 − 1/36) = 2.958. At x = 2: 3 × √(1 − 4/36) = 2.828.
> y changed by only 0.13 for one step of x → **flat** ✓
> The balance idea, halfway between, at x = 1.5 (where y = 2.905): 2b²x / 2a²y = 27 / 209 ≈ **0.13** ✓ — the same!
> Near the side point, at y = 1: the true x is 6 × √(1 − 1/9) = 5.657. At y = 0: x = 6.
> x changed by only 0.34 for one step of y → **steep** ✓

💡 A circle is the special case: b² = a², so "b²x < a²y" becomes **x < y** — exactly the 45° line, where the circle's octant ended in Chapter 22. ✓

---

## 23.7 Region 1: the midpoint decision

We use the **midpoint idea** from Chapter 22, Section 22.5.

📖 Write **f(x, y) = b²x² + a²y² − a²b²**. Then:
- f < 0: the point is **inside**,
- f = 0: **on** the ellipse,
- f > 0: **outside**.

### The choice

In Region 1, we are at pixel (x, y) and the next column is x + 1. The ellipse in the next column is either still in row y, or one row up in row y − 1:

```
  row y − 1:  ·        ●  (x + 1, y − 1)   ← "go up" choice
                       ×  the midpoint (x + 1, y − 0.5)
  row y:      ●        ●  (x + 1, y)       ← "stay" choice
           (x, y)
```

We test the **midpoint** between the two choices: (x + 1, y − 0.5).

Remember that we are in the bottom-right quarter, so row y is **further from the centre** than row y − 1.

- If the midpoint is **inside** (f < 0): the true edge is further out than the midpoint, so it is nearer to row y → **stay in row y**.
- If the midpoint is **outside** (f ≥ 0): the true edge is nearer to the centre than the midpoint, so it is nearer to row y − 1 → **go to row y − 1**.

🧠 **Remember (Region 1):** midpoint (x + 1, y − 0.5). Inside → keep y. Outside or on → y − 1.

### The "multiply by 4" trick

The midpoint has a "− 0.5" in it, so f has fractions (0.25 and 0.5). In Chapter 22, we dropped a 0.25. Here that trick does not work so simply, because the fraction is a² / 4, and a² / 4 can be 0, 0.25, 0.5 or 0.75 depending on a.

So we use a different trick: **multiply everything by 4**.

> **d = 4 × f(midpoint)**

Multiplying by 4 (a positive number) never changes the sign: if f is negative, 4f is negative; if f is positive, 4f is positive. So "d < 0" gives the same decision as "f < 0". And 4 × 0.25 = 1, 4 × 0.5 = 2: all the fractions become whole numbers.

### The start

We start at the bottom point of the quarter: **(x, y) = (0, b)**. The first midpoint is (1, b − 0.5):

> f(1, b − 0.5) = b² × 1² + a² × (b − 0.5)² − a²b²
> = b² + a²(b² − b + 0.25) − a²b²
> = b² + a²b² − a²b + 0.25a² − a²b²
> = b² − a²b + 0.25a²
>
> **d = 4f = 4b² − 4a²b + a²**

🔢 **Maths: the start for a = 6, b = 3**

> d = 4 × 9 − 4 × 36 × 3 + 36 = 36 − 432 + 36 = **−360**

### When we keep y (d < 0)

The next midpoint is (x + 2, y − 0.5) instead of (x + 1, y − 0.5). Only the x part changes:

> change in f = b²(x + 2)² − b²(x + 1)²
> = b²[(x² + 4x + 4) − (x² + 2x + 1)]
> = b²(2x + 3)

In the code, we first do `++x`, so the "new x" is X = x + 1. Then 2x + 3 = 2(X − 1) + 3 = 2X + 1:

> change in f = b²(2X + 1)
> change in d = 4 × that = **4b²(2X + 1)**

### When we go up (d ≥ 0)

The next midpoint is (x + 2, y − 1.5). The x part changes as above, **and** the y part changes:

> change in the y part = a²(y − 1.5)² − a²(y − 0.5)²
> = a²[(y² − 3y + 2.25) − (y² − y + 0.25)]
> = a²(−2y + 2)

In the code we do `--y` first, so the "new y" is Y = y − 1, and −2y + 2 = −2(Y + 1) + 2 = −2Y:

> change in the y part of f = −2a²Y
> change in d (× 4) = **−8a²Y**
> total change in d = **4b²(2X + 1) − 8a²Y**

🧠 **Remember — Region 1:**

```
x = 0, y = b
d = 4b² − 4a²b + a²
while b²·x < a²·y:
    plot the 4 copies of (x, y)
    x = x + 1
    if d < 0:
        d = d + 4b²·(2x + 1)
    else:
        y = y − 1
        d = d + 4b²·(2x + 1) − 8a²·y
```

---

## 23.8 Region 2: the midpoint decision

When Region 1 stops, we are at some pixel (x, y), **not yet plotted**. From now on, every step goes **one row up** (y − 1), toward the side point (a, 0). The question is whether x stays or moves one right:

```
  row y − 1:  ● (x, y − 1)   ×   ● (x + 1, y − 1)
                     the midpoint (x + 0.5, y − 1)
  row y:      ● (x, y)
```

We test the midpoint (x + 0.5, y − 1):

- If it is **outside** (d > 0): the edge is to the **left** of the midpoint (closer to the centre) → **keep x**.
- If it is **inside or on** (d ≤ 0): the edge is to the right → **x + 1**.

🧠 **Remember (Region 2):** midpoint (x + 0.5, y − 1). Outside → keep x. Inside or on → x + 1.

### The start of Region 2

> f(x + 0.5, y − 1) = b²(x + 0.5)² + a²(y − 1)² − a²b²
> multiply by 4, and use 4(x + 0.5)² = (2x + 1)²:
> **d = b²(2x + 1)² + 4a²(y − 1)² − 4a²b²**

All whole numbers. ✓ In the code we call u = 2x + 1 and v = y − 1, so d = b²·u·u + 4·a²·v·v − 4·a²·b².

### When we keep x (d > 0)

The next midpoint is (x + 0.5, y − 2) instead of (x + 0.5, y − 1):

> change in the y part = a²(y − 2)² − a²(y − 1)²
> = a²[(y² − 4y + 4) − (y² − 2y + 1)]
> = a²(−2y + 3)

With the new Y = y − 1 (the code does `--y` first): −2y + 3 = −2(Y + 1) + 3 = 1 − 2Y.

> change in d (× 4) = **4a²(1 − 2Y)**

### When we move right (d ≤ 0)

Now the x part changes too: from (x + 0.5) to (x + 1.5):

> change in the x part = b²(x + 1.5)² − b²(x + 0.5)²
> = b²[(x² + 3x + 2.25) − (x² + x + 0.25)]
> = b²(2x + 2)

With the new X = x + 1: 2x + 2 = 2X.

> change in the x part of d (× 4) = **8b²X**
> total change in d = **4a²(1 − 2Y) + 8b²X**

🧠 **Remember — Region 2:**

```
d = b²·(2x + 1)² + 4a²·(y − 1)² − 4a²b²
while y ≥ 0:
    plot the 4 copies of (x, y)
    y = y − 1
    if d > 0:
        d = d + 4a²·(1 − 2y)
    else:
        x = x + 1
        d = d + 4a²·(1 − 2y) + 8b²·x
```

The loop stops when y goes below 0: we have reached the horizontal axis, and the mirror images do the rest.

---

## 23.9 A full worked example: a = 6, b = 3

> a² = 36, b² = 9
> start: x = 0, y = 3, d = −360 (Section 23.7)

### Region 1

| plot (x, y) | still Region 1? b²x < a²y | d < 0? | new x, y | change in d | new d |
|---|---|---|---|---|---|
| (0, 3) | 0 < 108 yes | yes (−360) | 1, 3 | 4·9·(2·1 + 1) = 108 | −252 |
| (1, 3) | 9 < 108 yes | yes (−252) | 2, 3 | 36·5 = 180 | −72 |
| (2, 3) | 18 < 108 yes | yes (−72) | 3, 3 | 36·7 = 252 | 180 |
| (3, 3) | 27 < 108 yes | no (180) | 4, 2 | 36·9 − 8·36·2 = 324 − 576 = −252 | −72 |
| (4, 2) | 36 < 72 yes | yes (−72) | 5, 2 | 36·11 = 396 | 324 |
| (5, 2) | 45 < 72 yes | no (324) | 6, 1 | 36·13 − 8·36·1 = 468 − 288 = 180 | 504 |
| — | 54 < 36? **no** → Region 1 ends at (6, 1), not plotted yet | | | | |

### Region 2

> u = 2 × 6 + 1 = 13, v = 1 − 1 = 0
> d = 9 × 13 × 13 + 4 × 36 × 0 × 0 − 4 × 36 × 9 = 1521 + 0 − 1296 = **225**

| plot (x, y) | new y | d > 0? | x | change in d | new d |
|---|---|---|---|---|---|
| (6, 1) | 0 | yes (225) | 6 | 4·36·(1 − 0) = 144 | 369 |
| (6, 0) | −1 | yes (369) | 6 | 4·36·(1 + 2) = 432 | 801 |
| stop: y = −1 < 0 | | | | | |

So our quarter has the points:

> (0, 3), (1, 3), (2, 3), (3, 3), (4, 2), (5, 2), (6, 1), (6, 0)

### Check against the true ellipse

The true y for each column: y = b × √(1 − (x/a)²).

> x = 3: y = 3 × √(1 − 9/36) = 3 × 0.866 = 2.60 → closest whole number 3 ✓
> x = 4: y = 3 × √(1 − 16/36) = 3 × 0.745 = 2.24 → 2 ✓
> x = 5: y = 3 × √(1 − 25/36) = 3 × 0.553 = 1.66 → 2 ✓
> (and in Region 2, the true x for each row: x = a × √(1 − (y/b)²))
> y = 1: x = 6 × √(1 − 1/9) = 6 × 0.943 = 5.66 → 6 ✓

### The whole ellipse

The four mirror images of these points give (centre at (6, 3) in a 13 × 7 image):

```
  ...#######...
  .##.......##.
  #...........#
  #...........#
  #...........#
  .##.......##.
  ...#######...
```

**28 pixels, no gaps.**

🔢 **Maths: why 28?**

> 8 quarter points × 4 copies = 32 plots
> (0, 3) is on the vertical axis: (0, 3) and (−0, 3) are the same pixel. Its 4 copies give only **2** different pixels.
> (6, 0) is on the horizontal axis: its 4 copies also give only **2**.
> The other 6 points give 4 each.
> 6 × 4 + 2 + 2 = 24 + 4 = **28** ✓

🔢 **Maths: a check with the length around the ellipse**

There is no simple exact formula for the length around an ellipse (it is a famously hard problem!). A very good approximation was found by the Indian mathematician Ramanujan:

> length ≈ π × [3(a + b) − √((3a + b)(a + 3b))]
> = π × [3 × 9 − √(21 × 15)]
> = π × [27 − √315] = π × [27 − 17.75] = π × 9.25 ≈ **29.1**

28 pixels for a length of about 29 — as with circles (Chapter 22), a little less than the length, because diagonal parts use fewer pixels.

---

## 23.10 Very flat ellipses: the missing tips

There is one more problem. Look at a very flat ellipse: a = 10, b = 1. If we only use Region 1 and Region 2:

> Region 1 runs while b²x < a²y, that is x < 100 × 1. It plots (0, 1), (1, 1), … (8, 1), and then moves to (9, 0).
> Now y = 0, so the test is 9 < 0 → no. Region 1 ends.
> Region 2 plots (9, 0), then y becomes −1 and the loop stops.
> **The tips (10, 0) and (−10, 0) are never drawn!**

The ellipse is too flat: Region 2 reaches the row y = 0 before x reaches a. This happens only for very flat ellipses (b of 3 or less — we tested every a and b from 0 to 79).

The fix is simple. After Region 2, if x has not yet reached a, finish the row y = 0:

```
while x ≤ a:
    plot the 4 copies of (x, 0)
    x = x + 1
```

For normal ellipses, this loop does nothing harmful: it just plots (a, 0) a second time, or nothing at all. Our program prints the fixed flat ellipse:

```
  ..#################..
  ##.................##
  ..#################..
```

Both tips are there. ✓

The same fix also handles **b = 0**: an ellipse with no height at all is a horizontal line of length 2a + 1, and the extra loop draws exactly that line. (And a = 0 gives a vertical line: Region 2 keeps x = 0 all the way, because d stays positive.)

---

## 23.11 A circle is an ellipse with a = b

When a = b = r:
- the equation becomes x² + y² = r² (Section 23.2),
- the Region 1 test becomes x < y (Section 23.6).

So `drawEllipse(image, cx, cy, r, r, c)` should draw a circle. But is it **exactly** the same circle as `drawCircle` from Chapter 22? The two methods start at different places (the circle starts at (r, 0), the ellipse at (0, r)) and make their decisions with different numbers.

Our program checks radius 5 and prints:

```
ellipse with a = b = 5 is the same as the circle: yes
```

In fact, we tested every radius from 0 to 79: the pixels are **always the same**. Both methods make the same kind of choice again and again — "which of these two pixels is nearer to the true curve?" — so it is not a big surprise that they agree. But it is always good to **check** a belief like this with a program.

---

## 23.12 Big ellipses and `long long`

The numbers in the ellipse algorithm get **big**. Look at the start value:

> d = 4b² − 4a²b + a²

🔢 **Maths: the start value for a = b = 1000**

> 4 × a² × b = 4 × 1,000,000 × 1000 = **4,000,000,000**
> the biggest `int`: **2,147,483,647** (about 2.1 billion, Chapter 4)
> 4,000,000,000 is bigger → an `int` would **overflow**

📖 **New word: overflow** — when a number becomes too big for its type (Chapter 4). For signed whole numbers like `int`, the C++ rules say the result is **undefined**: anything can happen. Usually the number "wraps around" and becomes negative, and our ellipse would turn into a mess.

And 4a²b² (in Region 2) is even bigger: 4 × 10⁶ × 10⁶ = 4 × 10¹².

So we use **`long long`** (Chapter 12): a 64-bit whole number, up to about **9.2 × 10¹⁸**.

🔢 **Maths: how big can the ellipse be now?**

> The biggest values in d are about 8 × a² × b².
> 8 × a² × b² < 9.2 × 10¹⁸ → a × b < about 1.07 × 10⁹
> For a = b: a < about **32,000**

An image 64,000 pixels wide is far bigger than anything in this book. ✓

⚠️ **The type of each part matters.** `a * a` with two `int`s is computed in `int`, and can overflow **before** it is put into a `long long`. That is why the code writes:

```cpp
const long long a2 = static_cast<long long>(a) * a;
```

The `static_cast` makes the first `a` a `long long`, so the multiplication is done in `long long`. After that, every calculation that uses `a2` or `b2` is `long long` too. In the same way, `2LL * x` uses `2LL`, which is the number 2 as a `long long`.

---

## 23.13 Extra: the gardener's ellipse (foci)

Here is a famous way to draw an ellipse with **no maths at all**, used by gardeners to make oval flower beds:

1. Push two pins into the ground.
2. Tie a loop of string around them (looser than the distance between the pins).
3. Put a stick in the loop, pull it tight, and walk around. The stick draws an ellipse!

📖 **New word: focus** (plural **foci**) — each of the two pins. For every point on the ellipse, the two distances to the foci **add up to the same number**: **2a** (the width of the ellipse).

The foci are on the major axis, at distance **c** from the centre, where:

> **c² = a² − b²** (when a > b)

🔢 **Maths: an ellipse with a = 5, b = 3**

> c² = 25 − 9 = 16 → c = 4. The foci are at (−4, 0) and (4, 0).
> Point (5, 0) on the ellipse: distances 9 and 1 → 9 + 1 = **10** = 2a ✓
> Point (0, 3) on the ellipse: each distance is √(4² + 3²) = √25 = 5 → 5 + 5 = **10** ✓

💡 **The planets.** About 400 years ago, Johannes Kepler discovered that each planet goes around the Sun on an ellipse, with the Sun at one **focus** — not at the centre. Our `orbits.ppm` puts the Sun at the centre to keep things simple; Practice 8 moves it to a focus.

---

## Code, part 1: `ellipses.h`

File: `common/ellipses.h` (new). It includes `circles.h` (and through it `lines.h`, `draw.h` and everything before).

```cpp
#ifndef ELLIPSES_H
#define ELLIPSES_H

#include <cmath>
#include "circles.h"

inline void fillEllipse(Image& image, double cx, double cy, double a, double b, Colour c,
                        double alpha = 1.0) {
    if (a <= 0.0 || b <= 0.0) {
        return;
    }
    int x0 = static_cast<int>(std::floor(cx - a));
    int y0 = static_cast<int>(std::floor(cy - b));
    int x1 = static_cast<int>(std::ceil(cx + a));
    int y1 = static_cast<int>(std::ceil(cy + b));
    Rect box = clipToImage(Rect{x0, y0, x1, y1}, image);
    double a2 = a * a;
    double b2 = b * b;
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            double dx = (x + 0.5) - cx;
            double dy = (y + 0.5) - cy;
            if (b2 * dx * dx + a2 * dy * dy <= a2 * b2) {
                if (alpha >= 1.0) {
                    image.setPixel(x, y, c);
                } else {
                    blendPixel(image, x, y, c, alpha);
                }
            }
        }
    }
}

inline void plotFour(Image& image, int cx, int cy, int x, int y, Colour c) {
    image.setPixel(cx + x, cy + y, c);
    image.setPixel(cx - x, cy + y, c);
    image.setPixel(cx - x, cy - y, c);
    image.setPixel(cx + x, cy - y, c);
}

inline void drawEllipse(Image& image, int cx, int cy, int a, int b, Colour c) {
    if (a < 0 || b < 0) {
        return;
    }
    const long long a2 = static_cast<long long>(a) * a;
    const long long b2 = static_cast<long long>(b) * b;
    int x = 0;
    int y = b;
    long long d = 4 * b2 - 4 * a2 * b + a2;
    while (b2 * x < a2 * y) {
        plotFour(image, cx, cy, x, y, c);
        ++x;
        if (d < 0) {
            d += 4 * b2 * (2 * x + 1);
        } else {
            --y;
            d += 4 * b2 * (2 * x + 1) - 8 * a2 * y;
        }
    }
    const long long u = 2LL * x + 1;
    const long long v = y - 1LL;
    d = b2 * u * u + 4 * a2 * v * v - 4 * a2 * b2;
    while (y >= 0) {
        plotFour(image, cx, cy, x, y, c);
        --y;
        if (d > 0) {
            d += 4 * a2 * (1 - 2 * y);
        } else {
            ++x;
            d += 4 * a2 * (1 - 2 * y) + 8 * b2 * x;
        }
    }
    while (x <= a) {
        plotFour(image, cx, cy, x, 0, c);
        ++x;
    }
}

#endif
```

### Line by line

**The start (lines 1–5)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef ELLIPSES_H` / `#define ELLIPSES_H` | Include guard. |
| 4 | `#include <cmath>` | `std::floor` and `std::ceil`. |
| 5 | `#include "circles.h"` | Everything before: `Image`, `Rect`, `clipToImage`, `blendPixel`, and `drawCircle` (used by the program to compare). |

**The filled ellipse (lines 7–32)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 7–8 | `inline void fillEllipse(Image& image, double cx, double cy, double a, double b, Colour c, double alpha = 1.0) {` | A filled ellipse with any centre (cx, cy) and radii a (left–right) and b (up–down). `alpha` is optional: solid by default, like `fillCircle`. |
| 9–11 | `if (a <= 0.0 \|\| b <= 0.0) { return; }` | No size in one direction: nothing to fill. (This also protects against strange negative radii.) |
| 12–13 | `int x0 = static_cast<int>(std::floor(cx - a));` / `int y0 = ...(cy - b)...;` | The top-left of the bounding box, rounded **down** (Section 23.4). Note: **a** for x, **b** for y. |
| 14–15 | `int x1 = static_cast<int>(std::ceil(cx + a));` / `int y1 = ...(cy + b)...;` | The bottom-right, rounded **up**. Half-open: [x0, x1). |
| 16 | `Rect box = clipToImage(Rect{x0, y0, x1, y1}, image);` | Keep only the part of the box that is inside the image (Chapter 19). |
| 17–18 | `double a2 = a * a;` / `double b2 = b * b;` | a² and b², computed once, before the loops. |
| 19–20 | `for (int y = box.y0; y < box.y1; ++y) { for (int x = box.x0; x < box.x1; ++x) {` | Every pixel in the box, row by row. |
| 21–22 | `double dx = (x + 0.5) - cx;` / `double dy = (y + 0.5) - cy;` | From the ellipse centre to the **pixel centre**. |
| 23 | `if (b2 * dx * dx + a2 * dy * dy <= a2 * b2) {` | The integer form of the test (Section 23.3): b²dx² + a²dy² ≤ a²b². No division. The letters are crossed: **b²** with dx, **a²** with dy. |
| 24–28 | `if (alpha >= 1.0) { image.setPixel(x, y, c); } else { blendPixel(image, x, y, c, alpha); }` | Solid paint, or see-through paint (Chapter 18). |
| 29–32 | `}` `}` `}` `}` | End of the ifs, the loops and the function. |

**Four copies (lines 34–39)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 34 | `inline void plotFour(Image& image, int cx, int cy, int x, int y, Colour c) {` | Plot the four mirror images of the offset (x, y) around the centre (Section 23.5). |
| 35 | `image.setPixel(cx + x, cy + y, c);` | The original point (bottom-right quarter). |
| 36 | `image.setPixel(cx - x, cy + y, c);` | Mirrored left–right (bottom-left). |
| 37 | `image.setPixel(cx - x, cy - y, c);` | Mirrored both ways (top-left). |
| 38 | `image.setPixel(cx + x, cy - y, c);` | Mirrored up–down (top-right). |
| 39 | `}` | End. There is **no** swap of x and y: that would only be right for a circle. |

**The midpoint ellipse: setting up (lines 41–49)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 41 | `inline void drawEllipse(Image& image, int cx, int cy, int a, int b, Colour c) {` | The outline of an ellipse, centred on pixel (cx, cy). Whole numbers only. Its width is 2a + 1 pixels, its height 2b + 1. |
| 42–44 | `if (a < 0 \|\| b < 0) { return; }` | Negative radii make no sense: draw nothing. (a = 0 or b = 0 gives a straight line; a = b = 0 gives one pixel.) |
| 45 | `const long long a2 = static_cast<long long>(a) * a;` | a², as a `long long` (Section 23.12). The cast comes **before** the multiplication, so it cannot overflow. |
| 46 | `const long long b2 = static_cast<long long>(b) * b;` | b², the same way. |
| 47–48 | `int x = 0;` / `int y = b;` | Start at the offset (0, b): the bottom point, straight below the centre. |
| 49 | `long long d = 4 * b2 - 4 * a2 * b + a2;` | The first decision value: 4 × f(1, b − 0.5) (Section 23.7). Because `b2` and `a2` are `long long`, the whole calculation is `long long`. |

**Region 1 (lines 50–59)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 50 | `while (b2 * x < a2 * y) {` | Stay in Region 1 while the curve is flat: b²x < a²y (Section 23.6). |
| 51 | `plotFour(image, cx, cy, x, y, c);` | Plot this point in all four quarters. |
| 52 | `++x;` | In Region 1, x always moves one step. |
| 53–54 | `if (d < 0) { d += 4 * b2 * (2 * x + 1); }` | The midpoint was **inside**: keep y. Update d by 4b²(2x + 1), with the new x. |
| 55–57 | `} else { --y; d += 4 * b2 * (2 * x + 1) - 8 * a2 * y; }` | The midpoint was **outside** (or on): move one row toward the centre. Update d with the new x **and** the new y. |
| 58–59 | `}` `}` | End of the if and of the Region 1 loop. |

**Region 2 (lines 60–72)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 60 | `const long long u = 2LL * x + 1;` | u = 2x + 1, which is 2 × (x + 0.5): the midpoint's x, doubled so there is no fraction. `2LL` makes it a `long long`. |
| 61 | `const long long v = y - 1LL;` | v = y − 1: the midpoint's y. |
| 62 | `d = b2 * u * u + 4 * a2 * v * v - 4 * a2 * b2;` | The first Region 2 decision value: 4 × f(x + 0.5, y − 1) (Section 23.8). |
| 63 | `while (y >= 0) {` | Keep going until we pass the horizontal axis (the row of the centre). |
| 64 | `plotFour(image, cx, cy, x, y, c);` | Plot this point in all four quarters. (The first time, this is the point where Region 1 stopped.) |
| 65 | `--y;` | In Region 2, y always moves one step (toward the axis). |
| 66–67 | `if (d > 0) { d += 4 * a2 * (1 - 2 * y); }` | The midpoint was **outside**: keep x. Update d with the new y. |
| 68–70 | `} else { ++x; d += 4 * a2 * (1 - 2 * y) + 8 * b2 * x; }` | The midpoint was **inside** (or on): move one column outward. Update d with the new y **and** the new x. |
| 71–72 | `}` `}` | End of the if and of the Region 2 loop. |

**The flat-ellipse fix (lines 73–79)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 73 | `while (x <= a) {` | If x has not yet reached the tip a (only for very flat ellipses, Section 23.10)… |
| 74 | `plotFour(image, cx, cy, x, 0, c);` | …draw the rest of the row y = 0, on both sides. |
| 75 | `++x;` | Next column. |
| 76–77 | `}` `}` | End of the loop and the function. |
| 79 | `#endif` | End of the include guard. |

---

## Code, part 2: an eye, an egg and orbits

File: `ch23/ellipses.cpp`

```cpp
#include <climits>
#include <cmath>
#include <iostream>
#include <string>
#include "ellipses.h"

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

void fillEgg(Image& image, double cx, double cy, double a, double bTop, double bBottom,
             Colour c) {
    int x0 = static_cast<int>(std::floor(cx - a));
    int y0 = static_cast<int>(std::floor(cy - bTop));
    int x1 = static_cast<int>(std::ceil(cx + a));
    int y1 = static_cast<int>(std::ceil(cy + bBottom));
    Rect box = clipToImage(Rect{x0, y0, x1, y1}, image);
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            double dx = (x + 0.5) - cx;
            double dy = (y + 0.5) - cy;
            double b = (dy < 0.0) ? bTop : bBottom;
            double u = dx / a;
            double v = dy / b;
            if (u * u + v * v <= 1.0) {
                image.setPixel(x, y, c);
            }
        }
    }
}

double orbitY(double a, double b, double x) {
    double t = 1.0 - (x / a) * (x / a);
    if (t < 0.0) {
        return 0.0;
    }
    return b * std::sqrt(t);
}

int main() {
    Image outline(13, 7);
    drawEllipse(outline, 6, 3, 6, 3, colours::white);
    printGrid("ellipse outline, a = 6, b = 3", outline);
    std::cout << "pixels in the outline: " << countLit(outline) << "\n";

    Image filled(13, 7);
    fillEllipse(filled, 6.5, 3.5, 6.0, 3.0, colours::white);
    printGrid("filled ellipse, centre (6.5, 3.5), a = 6, b = 3", filled);
    std::cout << "pixels in the filled ellipse: " << countLit(filled) << "\n";

    Image flat(21, 3);
    drawEllipse(flat, 10, 1, 10, 1, colours::white);
    printGrid("flat ellipse, a = 10, b = 1", flat);

    Image asEllipse(11, 11);
    Image asCircle(11, 11);
    drawEllipse(asEllipse, 5, 5, 5, 5, colours::white);
    drawCircle(asCircle, 5, 5, 5, colours::white);
    std::cout << "ellipse with a = b = 5 is the same as the circle: "
              << (samePixels(asEllipse, asCircle) ? "yes" : "no") << "\n";

    long long big = 4LL * 1000 * 1000 * 1000;
    std::cout << "4 * a * a * b for a = b = 1000: " << big << "\n";
    std::cout << "the biggest int:                " << INT_MAX << "\n";

    Image eye(300, 160, Colour{235, 190, 160});
    fillEllipse(eye, 150.5, 80.5, 120.0, 55.0, colours::white);
    fillCircle(eye, 150.5, 80.5, 42.0, Colour{60, 120, 200});
    fillCircle(eye, 150.5, 80.5, 18.0, colours::black);
    fillCircle(eye, 165.5, 65.5, 8.0, colours::white, 0.8);
    drawEllipse(eye, 150, 80, 120, 55, Colour{90, 50, 40});

    Image egg(200, 240, Colour{200, 225, 245});
    fillEllipse(egg, 100.5, 200.5, 62.0, 12.0, colours::black, 0.25);
    fillEgg(egg, 100.5, 120.5, 60.0, 90.0, 70.0, Colour{250, 240, 215});

    Image orbits(400, 260, Colour{5, 5, 20});
    const int sunX = 200;
    const int sunY = 130;
    const int orbitA[4] = {50, 90, 130, 175};
    const int orbitB[4] = {30, 55, 80, 110};
    const double planetX[4] = {30.0, -60.0, 100.0, -150.0};
    const Colour planetColour[4] = {colours::red, colours::cyan, colours::green, colours::magenta};
    for (int i = 0; i < 4; ++i) {
        drawEllipse(orbits, sunX, sunY, orbitA[i], orbitB[i], Colour{80, 80, 110});
    }
    fillCircle(orbits, sunX + 0.5, sunY + 0.5, 18.0, colours::yellow);
    for (int i = 0; i < 4; ++i) {
        double side = (i % 2 == 0) ? -1.0 : 1.0;
        double planetY = side * orbitY(orbitA[i], orbitB[i], planetX[i]);
        fillCircle(orbits, sunX + planetX[i] + 0.5, sunY + planetY + 0.5, 6.0, planetColour[i]);
    }

    bool ok = eye.savePPM("eye.ppm");
    ok = ok && egg.savePPM("egg.ppm");
    ok = ok && orbits.savePPM("orbits.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
```

Build and run (from the `code/ch23` folder):

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common ellipses.cpp -o ellipses
./ellipses
```

### Line by line

**Includes and helpers (lines 1–47)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1 | `#include <climits>` | `INT_MAX`, the biggest `int` (Chapter 1). |
| 2 | `#include <cmath>` | `std::floor`, `std::ceil`, `std::sqrt`. |
| 3–4 | `#include <iostream>` / `#include <string>` | Printing and text. |
| 5 | `#include "ellipses.h"` | Our new header (and everything before it). |
| 7–31 | `printGrid` and `countLit` | The same two helpers as Chapter 22: print an image as `#` and `.`, and count the pixels that are not black. |
| 33 | `bool samePixels(const Image& p, const Image& q) {` | Answer "do these two images have exactly the same pixels?". |
| 34–36 | `if (p.width() != q.width() \|\| p.height() != q.height()) { return false; }` | Different sizes can never be the same. |
| 37–38 | `for (int y = 0; ...) { for (int x = 0; ...) {` | Every pixel. |
| 39–40 | `Colour s = p.getPixel(x, y);` / `Colour t = q.getPixel(x, y);` | The pixel at the same place in both images. |
| 41–43 | `if (s.r != t.r \|\| s.g != t.g \|\| s.b != t.b) { return false; }` | One channel different → not the same. We can stop at once. |
| 44–47 | `}` `}` `return true;` `}` | We checked every pixel and found no difference. |

**The egg (lines 49–68)**

An egg is not an ellipse. But an egg is **almost** two half-ellipses glued together: a taller half on top (the pointed end) and a shorter half below (the round end). Both halves have the same width a, so they fit together smoothly in the middle.

| Line | Code | What it does, in simple words |
|---|---|---|
| 49–50 | `void fillEgg(Image& image, double cx, double cy, double a, double bTop, double bBottom, Colour c) {` | A filled egg: width radius a, height bTop above the centre and bBottom below it. |
| 51–54 | `int x0 = ...floor(cx - a)...;` … `int y1 = ...ceil(cy + bBottom)...;` | The bounding box. The top uses **bTop**, the bottom uses **bBottom**. |
| 55 | `Rect box = clipToImage(Rect{x0, y0, x1, y1}, image);` | Clip to the image. |
| 56–57 | the two `for` loops | Every pixel in the box. |
| 58–59 | `double dx = (x + 0.5) - cx;` / `double dy = (y + 0.5) - cy;` | From the centre to the pixel centre. |
| 60 | `double b = (dy < 0.0) ? bTop : bBottom;` | Above the centre (dy is negative, because y goes down), use the top height. Below, use the bottom height. |
| 61–62 | `double u = dx / a;` / `double v = dy / b;` | "Un-stretch" the point (Section 23.2). These are `double`s, so the division is exact (not the `int` division that gives 0). |
| 63–65 | `if (u * u + v * v <= 1.0) { image.setPixel(x, y, c); }` | The unit-circle test: inside → colour it. (Here we use the division form, to show it. Both forms give the same answer.) |
| 66–68 | `}` `}` `}` | End. |

**A point on an orbit (lines 70–76)**

We want to put each planet **exactly on** its orbit. We do not know sine and cosine yet (Chapter 30), but we can use the equation: for a chosen x, solve (x/a)² + (y/b)² = 1 for y:

> (y/b)² = 1 − (x/a)² → y = b × √(1 − (x/a)²)

| Line | Code | What it does, in simple words |
|---|---|---|
| 70 | `double orbitY(double a, double b, double x) {` | Give the y-offset of the ellipse at the x-offset x (the lower half; use a minus for the upper half). |
| 71 | `double t = 1.0 - (x / a) * (x / a);` | t = 1 − (x/a)². |
| 72–74 | `if (t < 0.0) { return 0.0; }` | If x is further out than a, there is no point on the ellipse there. √ of a negative number is not allowed, so we return 0 instead. |
| 75 | `return b * std::sqrt(t);` | y = b√t. |
| 76 | `}` | End. |

🔢 **Maths: the first planet** (a = 50, b = 30, x = 30)

> t = 1 − (30/50)² = 1 − 0.36 = 0.64
> y = 30 × √0.64 = 30 × 0.8 = **24**
> check: (30/50)² + (24/30)² = 0.36 + 0.64 = 1 ✓

**The text output (lines 78–102)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 79–82 | `Image outline(13, 7);` … `countLit(outline)` | The outline from Section 23.9: a = 6, b = 3, centred on pixel (6, 3). Width 2 × 6 + 1 = 13, height 2 × 3 + 1 = 7: it fills the image exactly. |
| 84–87 | `Image filled(13, 7);` … `countLit(filled)` | The filled ellipse from Section 23.4, centre (6.5, 3.5): the centre of pixel (6, 3). |
| 89–91 | `Image flat(21, 3);` … `printGrid(...)` | The very flat ellipse from Section 23.10, to show that the tips are drawn. |
| 93–98 | `Image asEllipse(11, 11);` … `samePixels(...)` | Draw a radius-5 shape both ways — as an ellipse with a = b = 5 and with `drawCircle` — and compare (Section 23.11). |
| 100 | `long long big = 4LL * 1000 * 1000 * 1000;` | 4 × a² × b for a = b = 1000. `4LL` makes the first number a `long long`, so all the multiplications are done in `long long` (Section 23.12). |
| 101–102 | the two `std::cout` lines | Print it next to `INT_MAX`, to see that it would not fit into an `int`. |

**The eye (lines 104–109)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 104 | `Image eye(300, 160, Colour{235, 190, 160});` | A skin-coloured background. |
| 105 | `fillEllipse(eye, 150.5, 80.5, 120.0, 55.0, colours::white);` | The white of the eye: a wide ellipse, 240 × 110 pixels. |
| 106 | `fillCircle(eye, 150.5, 80.5, 42.0, Colour{60, 120, 200});` | The blue **iris**: a circle. Its radius 42 is less than b = 55, so it fits inside the white. |
| 107 | `fillCircle(eye, 150.5, 80.5, 18.0, colours::black);` | The black **pupil** in the middle. |
| 108 | `fillCircle(eye, 165.5, 65.5, 8.0, colours::white, 0.8);` | A small, slightly see-through highlight: the light reflected in the eye. It makes the eye look wet and alive. |
| 109 | `drawEllipse(eye, 150, 80, 120, 55, Colour{90, 50, 40});` | A dark brown outline around the eye. Centre (150, 80) as whole numbers matches the fill centre (150.5, 80.5) — the same rule as circles (Chapter 22, Section 22.8). |

**The egg (lines 111–113)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 111 | `Image egg(200, 240, Colour{200, 225, 245});` | A light blue background. |
| 112 | `fillEllipse(egg, 100.5, 200.5, 62.0, 12.0, colours::black, 0.25);` | A **shadow** first: a very flat, 25 % black ellipse under the egg. Shadows on the ground look like flat ellipses, because we see the ground from an angle. |
| 113 | `fillEgg(egg, 100.5, 120.5, 60.0, 90.0, 70.0, Colour{250, 240, 215});` | The cream-coloured egg on top: 120 wide, 90 above the centre and 70 below it. |

**The orbits (lines 115–130)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 115 | `Image orbits(400, 260, Colour{5, 5, 20});` | A very dark blue sky. |
| 116–117 | `const int sunX = 200;` / `const int sunY = 130;` | The centre of all the orbits. |
| 118–119 | `const int orbitA[4] = {50, 90, 130, 175};` / `const int orbitB[4] = {30, 55, 80, 110};` | The radii of four orbits. The biggest one reaches from x = 25 to 375 and from y = 20 to 240: it fits. |
| 120 | `const double planetX[4] = {30.0, -60.0, 100.0, -150.0};` | Where (left or right of the Sun) each planet is. |
| 121 | `const Colour planetColour[4] = {...};` | A colour for each planet. |
| 122–124 | `for (...) { drawEllipse(orbits, sunX, sunY, orbitA[i], orbitB[i], Colour{80, 80, 110}); }` | Draw the four orbit lines in grey-blue. |
| 125 | `fillCircle(orbits, sunX + 0.5, sunY + 0.5, 18.0, colours::yellow);` | The Sun, drawn **after** the orbits, so it covers them. |
| 126 | `for (int i = 0; i < 4; ++i) {` | For each planet: |
| 127 | `double side = (i % 2 == 0) ? -1.0 : 1.0;` | Planets 0 and 2 go on the upper half (−1: up), planets 1 and 3 on the lower half (+1: down). |
| 128 | `double planetY = side * orbitY(orbitA[i], orbitB[i], planetX[i]);` | The y-offset that puts the planet exactly on its orbit. |
| 129 | `fillCircle(orbits, sunX + planetX[i] + 0.5, sunY + planetY + 0.5, 6.0, planetColour[i]);` | The planet: a small disc. The + 0.5 matches the pixel-centred orbit line. |
| 130 | `}` | End of the planet loop. |

**Saving (lines 132–140)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 132–134 | `bool ok = eye.savePPM("eye.ppm");` … | Save the three pictures. `&&` skips the later saves if one fails (Chapter 11). |
| 135–138 | `if (!ok) { ... return 1; }` | Tell the user if a file could not be written. |
| 139–140 | `return 0;` `}` | Success. |

### What you should see

The program prints:

```
ellipse outline, a = 6, b = 3:
  ...#######...
  .##.......##.
  #...........#
  #...........#
  #...........#
  .##.......##.
  ...#######...
pixels in the outline: 28
filled ellipse, centre (6.5, 3.5), a = 6, b = 3:
  ......#......
  ..#########..
  .###########.
  #############
  .###########.
  ..#########..
  ......#......
pixels in the filled ellipse: 55
flat ellipse, a = 10, b = 1:
  ..#################..
  ##.................##
  ..#################..
ellipse with a = b = 5 is the same as the circle: yes
4 * a * a * b for a = b = 1000: 4000000000
the biggest int:                2147483647
```

Open the pictures:
- `eye.ppm`: a big white almond shape with a blue iris, a black pupil, a small shine, and a brown outline.
- `egg.ppm`: a cream egg, pointed at the top and round at the bottom, standing on its soft grey shadow.
- `orbits.ppm`: a yellow Sun with four oval orbits around it, and a coloured planet sitting exactly on each orbit.

---

## Small examples

### Example 1 — Inside or outside? (integer form)

An ellipse with centre (20, 10), a = 8, b = 4. Is the point (26, 12) inside?

> dx = 6, dy = 2
> a² = 64, b² = 16, a²b² = 1024
> b²dx² + a²dy² = 16 × 36 + 64 × 4 = 576 + 256 = 832
> 832 ≤ 1024 → **inside**

### Example 2 — An ellipse from its box

Often we know the **box** we want the ellipse in, not its centre and radii. For the half-open box [20, 80) × [10, 50):

> cx = (20 + 80) / 2 = 50, a = (80 − 20) / 2 = 30
> cy = (10 + 50) / 2 = 30, b = (50 − 10) / 2 = 20
> `fillEllipse(img, 50.0, 30.0, 30.0, 20.0, c);`

The ellipse touches all four sides of the box. (Because the box is half-open and we use pixel centres, this is exactly right: the box is 60 pixels wide, and so is the ellipse.)

### Example 3 — The area of the eye

> π × 120 × 55 = 3.14159 × 6600 ≈ **20,735** white pixels (before the iris covers some of them)
> The box has 240 × 110 = 26,400 pixels. The ellipse fills π/4 ≈ 78.5 % of its box — for **every** ellipse, just like a circle fills 78.5 % of its square.

### Example 4 — A filled ellipse from the midpoint method

Like Chapter 22, Example 2: instead of `plotFour`, fill each row between the left and right points. In both loops of `drawEllipse`, replace `plotFour(image, cx, cy, x, y, c);` with:

```cpp
fillRect(image, Rect{cx - x, cy + y, cx + x + 1, cy + y + 1}, c);
fillRect(image, Rect{cx - x, cy - y, cx + x + 1, cy - y + 1}, c);
```

The first `fillRect` is the row below the centre, the second the row above it. In Region 1, many points share the same row, so that row is filled several times, each time a little longer. That is some wasted work, but for solid colours the picture is right: the last, longest fill covers all the earlier ones.

### Example 5 — Tall or wide?

> `drawEllipse(img, 50, 50, 30, 10, c)` → a = 30 > b = 10 → **wide**: 61 × 21 pixels
> `drawEllipse(img, 50, 50, 10, 30, c)` → a = 10 < b = 30 → **tall**: 21 × 61 pixels

---

## Common mistakes

⚠️ **Mixing up a and b.** a is left–right, b is up–down. In the integer form they cross over: b² goes with dx², a² goes with dy².

⚠️ **Using eight copies.** Swapping x and y is only right for circles. With an ellipse, it draws a wide **and** a tall ellipse on top of each other — a strange flower shape.

⚠️ **Forgetting Region 2.** Region 1 alone draws only the flat top and bottom; the steep sides have big **gaps** (like the naive circle in Chapter 22).

⚠️ **Forgetting the flat-ellipse fix.** Very flat ellipses lose their tips.

⚠️ **`int` division.** If x and a are `int`s, `x / a` is 0 for every x smaller than a. Use the integer form (no division), or `double`s.

⚠️ **`int` overflow.** For big ellipses, a²b² does not fit into an `int`. Use `long long`, and cast **before** multiplying.

⚠️ **Wrong signs for the midpoint tests.** Region 1: d < 0 → **keep** y. Region 2: d > 0 → **keep** x. They look opposite, because in Region 1 "stay" means staying far from the centre, and in Region 2 "stay" means staying close to it. Follow the derivation, not your feelings!

---

## Practice

🏋️ **1.** Is the point (4, 2) inside, on, or outside the ellipse with centre (0, 0), a = 5, b = 3? Use the integer form.

🏋️ **2.** What is the bounding box (half-open) of `fillEllipse(img, 50.5, 20.5, 10.2, 4.7, c)`? Clip it to a 55 × 24 image.

🏋️ **3.** Write the four copies of the offset (5, 2) around the centre (20, 10).

🏋️ **4.** Run the midpoint ellipse algorithm by hand for a **tall** ellipse: a = 3, b = 5. Write both tables. How many pixels?

🏋️ **5.** Run it for a = b = 4. Do you get the same pixels as the radius-4 circle from Chapter 22, Practice 4?

🏋️ **6.** For a = 300 and b = 200, compute 4a²b². Would it fit into an `int`?

🏋️ **7.** Write `strokeEllipse(Image&, double cx, double cy, double a, double b, double thickness, Colour)`, which colours the pixels inside the ellipse (a + t/2, b + t/2) but **not** inside the ellipse (a − t/2, b − t/2), where t is the thickness.

🏋️ **8.** An orbit has a = 150 and b = 90. Where are its foci? Draw it centred at (200, 130) in a 400 × 260 image, with the Sun at the right focus.

---

## Answers

**1.**
> a² = 25, b² = 9, a²b² = 225
> 9 × 4² + 25 × 2² = 9 × 16 + 25 × 4 = 144 + 100 = 244
> 244 > 225 → **outside** (just a little)

**2.**
> x0 = floor(50.5 − 10.2) = floor(40.3) = 40, x1 = ceil(50.5 + 10.2) = ceil(60.7) = 61
> y0 = floor(20.5 − 4.7) = floor(15.8) = 15, y1 = ceil(20.5 + 4.7) = ceil(25.2) = 26
> box = [40, 61) × [15, 26)
> clipped to [0, 55) × [0, 24): **[40, 55) × [15, 24)**

**3.**
> (25, 12), (15, 12), (15, 8), (25, 8)

**4.**
> a² = 9, b² = 25
> start: x = 0, y = 5, d = 4 × 25 − 4 × 9 × 5 + 9 = 100 − 180 + 9 = **−71**

Region 1:

| plot (x, y) | b²x < a²y? | d < 0? | new x, y | change | new d |
|---|---|---|---|---|---|
| (0, 5) | 0 < 45 yes | yes (−71) | 1, 5 | 4·25·3 = 300 | 229 |
| (1, 5) | 25 < 45 yes | no (229) | 2, 4 | 4·25·5 − 8·9·4 = 500 − 288 = 212 | 441 |
| — | 50 < 36? **no** → Region 2 starts at (2, 4) | | | | |

Region 2:
> u = 5, v = 3 → d = 25 × 25 + 4 × 9 × 9 − 4 × 9 × 25 = 625 + 324 − 900 = **49**

| plot (x, y) | new y | d > 0? | x | change | new d |
|---|---|---|---|---|---|
| (2, 4) | 3 | yes (49) | 2 | 36·(1 − 6) = −180 | −131 |
| (2, 3) | 2 | no (−131) | 3 | 36·(1 − 4) + 8·25·3 = −108 + 600 = 492 | 361 |
| (3, 2) | 1 | yes (361) | 3 | 36·(1 − 2) = −36 | 325 |
| (3, 1) | 0 | yes (325) | 3 | 36·(1 − 0) = 36 | 361 |
| (3, 0) | −1 | yes (361) | 3 | 36·3 = 108 | 469 |
| stop | | | | | |

> Quarter points: (0, 5), (1, 5), (2, 4), (2, 3), (3, 2), (3, 1), (3, 0)
> (0, 5) and (3, 0) are on the axes → 2 pixels each. The other 5 → 4 each.
> Pixels: 2 + 5 × 4 + 2 = **24**

```
  ..###..
  .#...#.
  .#...#.
  #.....#
  #.....#
  #.....#
  #.....#
  #.....#
  .#...#.
  .#...#.
  ..###..
```

Notice: for a tall ellipse, Region 1 (the flat part at the top) is very short — only 2 points — and Region 2 does most of the work.

**5.**
> a² = b² = 16, d = 64 − 256 + 16 = −176
> Region 1: (0, 4) → d = −176 + 192 = 16; (1, 4) → x = 2, y = 3, d = 16 + 320 − 384 = −48; (2, 3) → x = 3, d = −48 + 448 = 400; then 16·3 < 16·3? no → stop at (3, 3).
> Region 2: d = 16 × 49 + 64 × 4 − 1024 = 784 + 256 − 1024 = 16
> (3, 3) → y = 2, d = 16 − 192 = −176; (3, 2) → y = 1, x = 4, d = −176 − 64 + 512 = 272; (4, 1) → y = 0, d = 272 + 64 = 336; (4, 0) → y = −1, stop.
> Quarter points: (0, 4), (1, 4), (2, 3), (3, 3), (3, 2), (4, 1), (4, 0)

The circle's octant in Chapter 22 was (4, 0), (4, 1), (3, 2), (3, 3). Its swapped copies are (0, 4), (1, 4), (2, 3), (3, 3). Together: exactly our seven quarter points. **The same 24 pixels.** ✓

**6.**
> a² = 90,000, b² = 40,000
> a²b² = 3,600,000,000, so 4a²b² = **14,400,000,000** (1.44 × 10¹⁰)
> The biggest `int` is 2,147,483,647 (about 2.1 × 10⁹) → it does **not** fit. Even a²b² alone does not fit. That is why we use `long long`.

**7.**

```cpp
inline void strokeEllipse(Image& image, double cx, double cy, double a, double b,
                          double thickness, Colour c) {
    double ao = a + thickness / 2.0;
    double bo = b + thickness / 2.0;
    double ai = a - thickness / 2.0;
    double bi = b - thickness / 2.0;
    if (ao <= 0.0 || bo <= 0.0) {
        return;
    }
    Rect box = clipToImage(Rect{static_cast<int>(std::floor(cx - ao)),
                                static_cast<int>(std::floor(cy - bo)),
                                static_cast<int>(std::ceil(cx + ao)),
                                static_cast<int>(std::ceil(cy + bo))}, image);
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            double dx = (x + 0.5) - cx;
            double dy = (y + 0.5) - cy;
            bool insideOuter = (dx / ao) * (dx / ao) + (dy / bo) * (dy / bo) <= 1.0;
            bool insideInner = ai > 0.0 && bi > 0.0 &&
                               (dx / ai) * (dx / ai) + (dy / bi) * (dy / bi) < 1.0;
            if (insideOuter && !insideInner) {
                image.setPixel(x, y, c);
            }
        }
    }
}
```

If the inner radii are 0 or less, there is no hole, and the whole outer ellipse is filled (`insideInner` is false). The `&&` checks `ai > 0.0` **first**, so we never divide by 0.

💡 The band between two ellipses is **not** exactly the same thickness everywhere: it is a little thinner near the ends of the long axis when a and b are very different. (The exact "same thickness everywhere" curve around an ellipse is not an ellipse at all!) For normal thicknesses, nobody can see the difference.

**8.**
> c² = a² − b² = 22,500 − 8,100 = 14,400 → c = **120**
> The foci are at (200 − 120, 130) = **(80, 130)** and (200 + 120, 130) = **(320, 130)**

```cpp
Image kepler(400, 260, Colour{5, 5, 20});
drawEllipse(kepler, 200, 130, 150, 90, Colour{80, 80, 110});
fillCircle(kepler, 320.5, 130.5, 12.0, colours::yellow);
```

Now the Sun is near the right end of the orbit. A planet on this orbit is close to the Sun at the right end (distance 150 − 120 = 30) and far away at the left end (distance 150 + 120 = 270). Real planets move **faster** when they are close to the Sun — another of Kepler's discoveries.

---

## Summary

🧠 An **ellipse** is a stretched circle, with a **horizontal radius a** and a **vertical radius b**.

🧠 Equation: **(x/a)² + (y/b)² = 1**. Integer form (no division): **b²x² + a²y² = a²b²**. Inside: ≤.

🧠 **Filled ellipse**: test the pixel **centre** inside the clipped **bounding box** [cx − a, cx + a) × [cy − b, cy + b).

🧠 Area = **π·a·b**. A circle is the special case **a = b**.

🧠 Only **four-way symmetry**: (±x, ±y). Never swap x and y.

🧠 **Two regions**: Region 1 (flat, b²x < a²y) steps x; Region 2 (steep) steps y.

🧠 **Multiply by 4** to make the midpoint values whole numbers. Use **`long long`**, and cast before multiplying.

🧠 After Region 2, **finish the row y = 0** for very flat ellipses.

---

## Next chapter

Rectangles, lines, circles and ellipses are all "one formula" shapes. The most important shape in computer graphics is even simpler: the **triangle**. Every 3D game draws millions of them every second. In Chapter 24 we learn the **edge function**, a tiny formula that tells us which side of a line a point is on — and with three of them, whether a point is inside a triangle.
