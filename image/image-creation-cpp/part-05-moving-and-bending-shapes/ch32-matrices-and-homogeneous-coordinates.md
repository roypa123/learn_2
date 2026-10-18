# Chapter 32 — Matrices and Homogeneous Coordinates

> **Part 5 · Chapter 32 of 82**
> **You need:** Chapters 1–31 (especially 29, 30 and 31) · **You will make:** `matrix.h` (a 3 × 3 matrix type, the matrices for moving, scaling, turning and skewing, matrix multiplication, applying a matrix to points and directions, and the determinant), `grids.ppm`, `letters.ppm` and `squares.ppm`

---

## What you will learn

- What a **matrix** is: a small table of numbers.
- How to multiply a matrix by a point, and why it is just two **dot products**.
- The big secret: the **columns** of a matrix tell you where (1, 0) and (0, 1) go.
- The matrices for **scale**, **mirror**, **rotate** and a new one, **skew**.
- Why moving cannot be done with a 2 × 2 matrix, and how a third number 1 — **homogeneous coordinates** — fixes it.
- The difference between a **point** and a **direction** (w = 1 and w = 0).
- How to **multiply two matrices**, so that many transformations become **one**.
- Why the order is read **right to left**.
- What the **determinant** tells you: how much areas grow, and whether there is a mirror.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **matrix** (plural: **matrices**) | A rectangle of numbers in rows and columns. |
| **row** | A line of numbers going **across** a matrix. |
| **column** | A line of numbers going **down** a matrix. |
| **entry** | One number inside a matrix. |
| **2 × 2**, **3 × 3** | The size of a matrix: rows × columns. |
| **skew** (or **shear**) | A slant: each point slides sideways by an amount that depends on its height (like italic letters). |
| **homogeneous coordinates** | Writing a point (x, y) with a third number: (x, y, 1). |
| **identity matrix** | The matrix that changes nothing (1s on the diagonal, 0s elsewhere). |
| **diagonal** | The entries from the top-left to the bottom-right corner of a matrix. |
| **matrix product** | Two matrices multiplied together: one matrix that does both transformations. |
| **determinant** | One number from a matrix that tells how much it scales areas (and whether it mirrors). |

---

## 32.1 Why do we need a new tool?

In Chapter 31 we wrote shapes like this:

```cpp
translatePoints(rotatePoints(scalePoints(house, ground, 1.5, 1.5), ground, angle), Vec2{220.0, 180.0})
```

It works, but:

- It is long, and easy to write in the wrong order.
- The whole chain runs again for every point: a `std::cos` and a `std::sin` for **every** corner.
- We cannot **store** "this whole chain" in one variable, pass it to a function, or combine it with another chain.

What we want is **one small object** that holds "move this much, turn this much, scale this much" — any mix of them — and can be applied to a point quickly. That object is a **matrix**.

---

## 32.2 What is a matrix?

📖 **New word: matrix** — a rectangle of numbers, arranged in **rows** and **columns**.

📖 **New words: row and column** — a **row** goes across, a **column** goes down. (Like the rows and columns of an image, Chapter 3.)

📖 **New word: entry** — one number in the matrix.

Here is a **2 × 2** matrix ("two by two": 2 rows, 2 columns):

```
         column 0   column 1
row 0  [    a          b    ]
row 1  [    c          d    ]
```

We name entries by **row first, then column**: `m[0][1]` is row 0, column 1 (that is b above). This is the same order as `m[y][x]`, but be careful: for an image we usually write (x, y) — column first. For matrices, it is always **row first**.

In C++, a 3 × 3 table of numbers is a two-dimensional array:

```cpp
struct Mat3 {
    double m[3][3] = {{1.0, 0.0, 0.0}, {0.0, 1.0, 0.0}, {0.0, 0.0, 1.0}};
};
```

(We will see in Section 32.7 why we use 3 × 3 and not 2 × 2, and in Section 32.10 why the starting values are 1s on the diagonal.)

---

## 32.3 A matrix times a point

To apply a 2 × 2 matrix to a point (x, y), we multiply. The rule:

```
[ a  b ]   [ x ]     [ a × x + b × y ]
[ c  d ] × [ y ]  =  [ c × x + d × y ]
```

> **new x = a x + b y**
> **new y = c x + d y**

Each new coordinate is a **row** of the matrix, "dotted" with the point: row 0 · (x, y) gives the new x, and row 1 · (x, y) gives the new y. (A dot product, Chapter 29: multiply matching numbers and add.)

🔢 **Maths: multiply**

```
[ 2  1 ]   [ 3 ]     [ 2 × 3 + 1 × 4 ]     [ 10 ]
[ 0  3 ] × [ 4 ]  =  [ 0 × 3 + 3 × 4 ]  =  [ 12 ]
```

💡 We write points **standing up** (as a column) next to a matrix, because then the rule "row times column" lines up nicely. It is still just the point (3, 4).

---

## 32.4 The columns tell the story

Here is the most important idea of this chapter. Multiply a matrix by **(1, 0)**:

```
[ a  b ]   [ 1 ]     [ a ]
[ c  d ] × [ 0 ]  =  [ c ]      ← column 0!
```

And by **(0, 1)**:

```
[ a  b ]   [ 0 ]     [ b ]
[ c  d ] × [ 1 ]  =  [ d ]      ← column 1!
```

🧠 **Remember:** **column 0 is where (1, 0) goes. Column 1 is where (0, 1) goes.**

And because every point is x × (1, 0) + y × (0, 1) (Chapter 31, Section 31.4), the matrix sends it to x × (column 0) + y × (column 1). That is exactly the multiplication rule, read the other way:

> a x + b y, c x + d y = x × (a, c) + y × (b, d) ✓

So to **build** a matrix for any transformation, we only have to answer two questions: **where does (1, 0) go? where does (0, 1) go?** — and write the answers down as the two columns.

### Scale

Scaling by sx across and sy down sends (1, 0) to (sx, 0), and (0, 1) to (0, sy):

```
[ sx   0 ]
[  0  sy ]
```

### Mirror

A left–right mirror sends (1, 0) to (−1, 0) and keeps (0, 1):

```
[ −1  0 ]
[  0  1 ]
```

(It is a scale with sx = −1, as in Chapter 31.)

### Rotate

Chapter 31 found: (1, 0) goes to (cos θ, sin θ), and (0, 1) goes to (−sin θ, cos θ). Write them down as columns:

```
[ cos θ   −sin θ ]
[ sin θ    cos θ ]
```

🔢 **Maths: check against Chapter 31**

> new x = cos θ × x − sin θ × y, new y = sin θ × x + cos θ × y ✓ — the rotation formula
> θ = 30°: cos = 0.866, sin = 0.5:

```
[ 0.866  −0.5   ]   [ 2 ]     [ 0.866 × 2 − 0.5 × 1 ]     [ 1.232 ]
[ 0.5     0.866 ] × [ 1 ]  =  [ 0.5 × 2 + 0.866 × 1 ]  =  [ 1.866 ]
```

> the same (1.23205, 1.86603) as Chapter 31 ✓

### Seeing it: `grids.ppm`

`grids.ppm` has four panels. Each one draws a square grid (7 lines each way, 20 pixels apart) **through** a matrix, plus two arrows: a **red** arrow showing where (40, 0) goes, and a **green** arrow showing where (0, 40) goes. The arrows **are** the two columns (times 40):

| panel | matrix | red arrow (column 0 × 40) | green arrow (column 1 × 40) | the grid |
|---|---|---|---|---|
| 1 | the identity (Section 32.10) | (40, 0): right | (0, 40): down | unchanged |
| 2 | rotation by 30° | (34.6, 20): turned clockwise | (−20, 34.6) | turned |
| 3 | scale (1.5, 0.6) | (60, 0): longer | (0, 24): shorter | wide and flat |
| 4 | skew (0.5, 0) | (40, 0): unchanged | (20, 40): leaning | slanted |

---

## 32.5 A new transformation: skew

📖 **New word: skew** (also called **shear**) — every point slides sideways by an amount that grows with its height:

> **new x = x + kx × y**, new y = y

Where does (1, 0) go? (1 + kx × 0, 0) = (1, 0): nowhere. Where does (0, 1) go? (kx, 1): it leans over. So the matrix is:

```
[ 1  kx ]
[ 0   1 ]
```

You can also skew the other way: new y = ky × x + y (things lean up or down as you go across). Our `skew(kx, ky)` does both:

```
[  1  kx ]
[ ky   1 ]
```

💡 Imagine a stack of playing cards. Push the top of the stack sideways: each card slides a bit more than the one below it. The stack becomes a slanted box, but each card stays level and keeps its size. That is a skew. Italic letters are skewed letters.

🔢 **Maths: skew the point (10, −20) with kx = −0.3**

> new x = 10 + (−0.3) × (−20) = 10 + 6 = **16**, new y = **−20**
> The point is above the baseline (y negative), so it slides **right**: our letters lean to the right, like italics ✓

---

## 32.6 The trouble with moving

Now the bad news. Try to build a **translate** matrix — "move everything by (10, 5)". Whatever a, b, c and d are:

```
[ a  b ]   [ 0 ]     [ 0 ]
[ c  d ] × [ 0 ]  =  [ 0 ]
```

The point (0, 0) **always** stays at (0, 0)! A 2 × 2 matrix can stretch, turn, mirror and skew around the origin, but it can never **slide** things away. Moving is not "where do (1, 0) and (0, 1) go" — moving does not change directions at all; it adds a fixed step.

---

## 32.7 The trick: homogeneous coordinates

📖 **New word: homogeneous coordinates** — write every point with an **extra third number, 1**:

> (x, y) → **(x, y, 1)**

Now use a **3 × 3** matrix. Here is the moving matrix:

```
[ 1  0  tx ]   [ x ]     [ 1 × x + 0 × y + tx × 1 ]     [ x + tx ]
[ 0  1  ty ] × [ y ]  =  [ 0 × x + 1 × y + ty × 1 ]  =  [ y + ty ]
[ 0  0   1 ]   [ 1 ]     [ 0 × x + 0 × y +  1 × 1 ]     [   1    ]
```

The extra 1 at the bottom of the point gets multiplied by tx and ty, and **adds** them. Moving works!

And the bottom row (0, 0, 1) makes the third number come out as 1 again, ready for the next matrix.

🔢 **Maths: move (3, 1) by (10, 5)**

> new x = 1 × 3 + 0 × 1 + 10 × 1 = **13**
> new y = 0 × 3 + 1 × 1 + 5 × 1 = **6** ✓ (Chapter 31)

### All our matrices in 3 × 3 form

The 2 × 2 matrices go into the **top-left corner**, with 0s for "no move" and the same bottom row:

```
  translate            scale               rotate                     skew
[ 1  0  tx ]      [ sx  0  0 ]      [ cos θ  −sin θ  0 ]      [  1  kx  0 ]
[ 0  1  ty ]      [  0 sy  0 ]      [ sin θ   cos θ  0 ]      [ ky   1  0 ]
[ 0  0   1 ]      [  0  0  1 ]      [   0       0    1 ]      [  0   0  1 ]
```

🧠 **Remember the layout:**

```
[ a  b  tx ]      a, b, c, d: the stretching, turning and skewing part
[ c  d  ty ]      tx, ty:     the moving part
[ 0  0   1 ]      0, 0, 1:    always the same (for now)
```

💡 The word "homogeneous" (say "hom-oh-JEE-nee-us") means "of the same kind". With the extra 1, all four kinds of transformation become the same kind of thing: a 3 × 3 matrix. In Part 9 (3D) we will use a bigger 4 × 4 version of the same trick, and there the bottom row will **not** always be all 0s and a 1 — that is how **perspective** (far things look smaller) is done. In this part of the book, the bottom row never changes.

### In code

Because the bottom row is always (0, 0, 1) and the third number of a point is always 1, we do not need to compute the third result (it would always be 1). So applying a matrix to a point is:

```cpp
inline Vec2 applyToPoint(const Mat3& t, Vec2 p) {
    return Vec2{t.m[0][0] * p.x + t.m[0][1] * p.y + t.m[0][2],
                t.m[1][0] * p.x + t.m[1][1] * p.y + t.m[1][2]};
}
```

That is 4 multiplications and 4 additions per point — and no `std::cos`, no `std::sin`. The cosine and sine were worked out **once**, when the matrix was built.

---

## 32.8 Points and directions

A **point** is a place. A **direction** (or a step — a vector, Chapter 29) is "which way, and how far". If you move a whole drawing 10 pixels right:

- every **place** moves 10 pixels right;
- but a **direction** — like "the arrow points up-right" — does **not** change. The arrow moved, but it still points the same way.

Homogeneous coordinates show this beautifully. Write a direction with a third number **0** instead of 1:

> point: (x, y, **1**)    direction: (x, y, **0**)

```
[ 1  0  tx ]   [ x ]     [ x + tx × 0 ]     [ x ]
[ 0  1  ty ] × [ y ]  =  [ y + ty × 0 ]  =  [ y ]
[ 0  0   1 ]   [ 0 ]     [     0      ]     [ 0 ]
```

The moving part is multiplied by 0: a direction is not moved, but it **is** still turned, scaled and skewed by the a, b, c, d part. Our `applyToDirection` does exactly this (it leaves out tx and ty).

The program prints:

```
move by (10, 5): the point (3, 1) goes to (13, 6), the direction (3, 1) stays (3, 1)
```

💡 There is even a little rule hidden here: point − point = direction (1 − 1 = 0), point + direction = point (1 + 0 = 1), and point + point = nonsense (1 + 1 = 2). Chapter 29 said the same thing in words.

⚠️ Later, for lighting (Part 9), the directions that stick out of surfaces ("normals") need yet another rule when the matrix has a non-uniform scale. We will deal with that when we get there.

---

## 32.9 Multiplying two matrices

Now the real power. Suppose we want to **scale** by (2, 3) and **then** move by (10, 5). We could apply two matrices to every point, one after the other. Or we could first combine them into **one** matrix that does both.

📖 **New word: matrix product** — the matrix A × B (also written A · B or just AB). Applying it to a point gives the same result as applying **B first, then A**:

> **(A × B) × p = A × (B × p)**

### Building the product, the column way

What should the columns of A × B be? Use Section 32.4: column 0 must be "where (1, 0) ends up". First B sends (1, 0) to **column 0 of B**. Then A sends that to **A × (column 0 of B)**. So:

> **column j of (A × B) = A × (column j of B)**

### The rule: row times column

Working that out for every entry gives the usual rule:

> **entry (row i, column j) of A × B = (row i of A) · (column j of B)**

— the dot product of a row of A with a column of B. For 3 × 3 matrices, each entry is the sum of 3 products:

> (A × B)[i][j] = A[i][0] × B[0][j] + A[i][1] × B[1][j] + A[i][2] × B[2][j]

That is three loops in C++: over the rows, the columns, and the three products to add.

🔢 **Maths: translation(10, 5) × scaling(2, 3)**

```
[ 1  0  10 ]   [ 2  0  0 ]
[ 0  1   5 ] × [ 0  3  0 ]
[ 0  0   1 ]   [ 0  0  1 ]
```

> row 0 · column 0 = 1 × 2 + 0 × 0 + 10 × 0 = **2**
> row 0 · column 1 = 1 × 0 + 0 × 3 + 10 × 0 = **0**
> row 0 · column 2 = 1 × 0 + 0 × 0 + 10 × 1 = **10**
> row 1 · column 0 = 0 × 2 + 1 × 0 + 5 × 0 = **0**
> row 1 · column 1 = 0 × 0 + 1 × 3 + 5 × 0 = **3**
> row 1 · column 2 = 0 × 0 + 1 × 0 + 5 × 1 = **5**
> row 2 gives (0, 0, 1) as always

```
[ 2  0  10 ]
[ 0  3   5 ]
[ 0  0   1 ]
```

Read it with the layout of Section 32.7: "scale by (2, 3), and move by (10, 5)" ✓. Try it on (1, 1): (2 × 1 + 10, 3 × 1 + 5) = **(12, 8)**. By hand: scale (1, 1) → (2, 3), then move → (12, 8) ✓.

---

## 32.10 Order: read from right to left

🔢 **Maths: the other order, scaling(2, 3) × translation(10, 5)**

> This means: move **first**, then scale.

The program prints both:

```
translation(10, 5) * scaling(2, 3):
  2  0  10
  0  3  5
  0  0  1
scaling(2, 3) * translation(10, 5):
  2  0  20
  0  3  15
  0  0  1
```

Different! In the second one, the move happens first, and then the scale **also scales the move**: 10 × 2 = 20 and 5 × 3 = 15. Try (1, 1): move → (11, 6), scale → **(22, 18)** — and the matrix gives (2 + 20, 3 + 15) = (22, 18) ✓.

🧠 **Remember:** in **A × B × C**, the matrix **nearest the point** acts first. So C acts first, then B, then A. **Read right to left.**

This matches Chapter 31, Section 31.8. The program repeats that example with matrices:

```
(1, 0) with translation * rotation: (10, 1)
(1, 0) with rotation * translation: (6.73556e-16, 11)
```

- translation × rotation: **turn first**, then move → (10, 1).
- rotation × translation: **move first**, then turn → (0, 11).

So "scale, then rotate, then translate" (Chapter 31's usual order for a shape in local coordinates) is written as:

> **M = translation × rotation × scaling**

⚠️ For ordinary numbers, 2 × 3 = 3 × 2. For matrices, **A × B is usually not B × A**. That is the maths way of saying "order matters".

But one thing does work like ordinary numbers: (A × B) × C = A × (B × C). So we can combine a long chain of matrices in any **grouping** we like, as long as we keep the **order**.

### The identity matrix

📖 **New word: identity matrix** — the matrix that changes nothing:

```
[ 1  0  0 ]
[ 0  1  0 ]
[ 0  0  1 ]
```

(1, 0) goes to (1, 0), (0, 1) goes to (0, 1), and nothing moves. It works like the number 1 for multiplication: I × A = A × I = A.

📖 **New word: diagonal** — the entries from the top-left to the bottom-right: m[0][0], m[1][1], m[2][2]. The identity has 1s on the diagonal and 0s everywhere else.

That is why a new `Mat3` starts as the identity: then `translation`, `scaling`, `rotation` and `skew` only need to change a few entries.

### Two turns make one turn

The program also multiplies rotation(20°) × rotation(25°):

```
rotation(20) * rotation(25):
  0.707107  -0.707107  0
  0.707107  0.707107  0
  0  0  1
```

That is exactly rotation(45°): cos 45° = sin 45° = 0.707107 ✓. Turns about the same point add up (Chapter 31, Practice 4) — and the matrix product does the adding for us.

---

## 32.11 One matrix for the whole job

Once a chain is multiplied into one matrix, applying it to a point costs the same 4 multiplications and 4 additions, no matter how long the chain was. For a shape with 1000 corners and a chain of 5 steps, we do 4 matrix products (a few dozen multiplications, once) and then 1000 cheap point applications — instead of 5000 function calls with sines and cosines.

### The letters: `letters.ppm`

The program draws a capital **F** (10 corners, in local coordinates with (0, 0) at the middle of its bottom edge) five times. Each copy is placed with **one** matrix:

> place = translation(60 + 120 i, 130) × shape i

| i | shape | what you see |
|---|---|---|
| 0 | identity | a normal F |
| 1 | skew(−0.3, 0) | an *italic* F, leaning right |
| 2 | rotation(20°) | an F turned clockwise around its bottom middle |
| 3 | scaling(−1, 1) | a mirrored F (its arms point left) |
| 4 | skew(−0.3, 0) × scaling(−1, 1) | mirrored **first**, then made italic — a mirrored F that still leans right |

Why an F? Because it has no mirror symmetry and no turning symmetry, so every transformation shows clearly.

### Doing it again and again: `squares.ppm`

Here is something only a matrix can do so neatly. Make a small step:

> step = rotation(10°) × scaling(0.93, 0.93) — "shrink a little, then turn a little"

and keep a matrix `current`, starting as the identity. Each time round the loop, draw a square through `current`, then do:

> current = step × current

After k times round, current = step × step × … × step (k times): shrunk by 0.93 k times and turned by 10° k times.

🔢 **Maths: the last square (k = 29)**

> it is turned by 29 × 10° = **290°**
> it is scaled by 0.93²⁹ ≈ **0.122**: the 200-pixel square is now about **24** pixels across

The 30 squares spiral inward, each a little smaller and a little more turned, in rainbow colours. (The final translation(150, 150) is multiplied on the **left**, so it happens **last**: the squares are shrunk and turned around their own middle, then moved to the middle of the picture.)

---

## 32.12 The determinant: how much does area change?

📖 **New word: determinant** — for the a, b, c, d part of a matrix:

> **determinant = a × d − b × c**

(With the bottom row (0, 0, 1), this is also the determinant of the whole 3 × 3 matrix.)

What does it mean? Think about the unit square, with corners (0, 0), (1, 0), (1, 1), (0, 1) — area 1. The matrix sends (1, 0) to column 0 = (a, c), and (0, 1) to column 1 = (b, d). So the square becomes a **parallelogram** with those two sides. Its area is the cross product of the two sides (Chapter 29: the cross product is the area of the parallelogram):

> cross((a, c), (b, d)) = a × d − c × b ✓

🧠 **Remember:** the determinant is **how many times bigger every area gets**. And if it is **negative**, the matrix contains a **mirror** (the order of the corners is flipped, Chapter 31).

🔢 **Maths: four determinants**

> rotation: cos θ × cos θ − (−sin θ) × sin θ = cos²θ + sin²θ = **1** — turning does not change areas ✓
> scaling(2, 3): 2 × 3 − 0 × 0 = **6** — 2 times wider, 3 times taller, 6 times the area ✓
> scaling(−1, 1) (a mirror): −1 × 1 − 0 = **−1** — same area, but mirrored ✓
> skew(0.5, 0): 1 × 1 − 0.5 × 0 = **1** — the playing cards slide, but the stack has the same area ✓

The program prints `determinants: rotation 1, scaling(2, 3) 6, mirror -1, skew 1`.

And the spiral's step: rotation × scaling(0.93, 0.93) has determinant 1 × 0.93² = **0.8649** — each square has about 86 % of the area of the one before.

💡 Determinants multiply: the determinant of A × B is det(A) × det(B). (Doubling the area twice makes it 4 times bigger.) If it is ever **0**, the matrix squashes everything flat onto a line or a point, and nothing can undo it. In Chapter 33 we will use the determinant to **undo** a matrix.

---

## Code, part 1: `matrix.h`

File: `common/matrix.h` (new). It includes `transform.h`.

```cpp
#ifndef MATRIX_H
#define MATRIX_H

#include <cmath>
#include <vector>
#include "transform.h"

struct Mat3 {
    double m[3][3] = {{1.0, 0.0, 0.0}, {0.0, 1.0, 0.0}, {0.0, 0.0, 1.0}};
};

inline Mat3 identity() {
    return Mat3{};
}

inline Mat3 translation(double tx, double ty) {
    Mat3 r;
    r.m[0][2] = tx;
    r.m[1][2] = ty;
    return r;
}

inline Mat3 scaling(double sx, double sy) {
    Mat3 r;
    r.m[0][0] = sx;
    r.m[1][1] = sy;
    return r;
}

inline Mat3 rotation(double radians) {
    double c = std::cos(radians);
    double s = std::sin(radians);
    Mat3 r;
    r.m[0][0] = c;
    r.m[0][1] = -s;
    r.m[1][0] = s;
    r.m[1][1] = c;
    return r;
}

inline Mat3 skew(double kx, double ky) {
    Mat3 r;
    r.m[0][1] = kx;
    r.m[1][0] = ky;
    return r;
}

inline Mat3 operator*(const Mat3& a, const Mat3& b) {
    Mat3 r;
    for (int row = 0; row < 3; ++row) {
        for (int col = 0; col < 3; ++col) {
            double sum = 0.0;
            for (int k = 0; k < 3; ++k) {
                sum += a.m[row][k] * b.m[k][col];
            }
            r.m[row][col] = sum;
        }
    }
    return r;
}

inline Vec2 applyToPoint(const Mat3& t, Vec2 p) {
    return Vec2{t.m[0][0] * p.x + t.m[0][1] * p.y + t.m[0][2],
                t.m[1][0] * p.x + t.m[1][1] * p.y + t.m[1][2]};
}

inline Vec2 applyToDirection(const Mat3& t, Vec2 v) {
    return Vec2{t.m[0][0] * v.x + t.m[0][1] * v.y, t.m[1][0] * v.x + t.m[1][1] * v.y};
}

inline std::vector<PointF> applyToPoints(const Mat3& t, const std::vector<PointF>& points) {
    std::vector<PointF> result;
    for (PointF p : points) {
        result.push_back(applyToPoint(t, p));
    }
    return result;
}

inline double determinant(const Mat3& t) {
    return t.m[0][0] * t.m[1][1] - t.m[0][1] * t.m[1][0];
}

#endif
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef MATRIX_H` / `#define MATRIX_H` | Include guard. |
| 4–6 | `#include <cmath>` / `<vector>` / `"transform.h"` | `std::cos` and `std::sin`; lists of points; and everything before (Chapter 31's functions, `Vec2`, the drawing library). |
| 8–10 | `struct Mat3 { double m[3][3] = {{1.0, 0.0, 0.0}, {0.0, 1.0, 0.0}, {0.0, 0.0, 1.0}}; };` | A 3 × 3 matrix: 3 rows of 3 numbers. `m[row][col]`. It starts as the **identity** (Section 32.10). |
| 12–14 | `inline Mat3 identity() { return Mat3{}; }` | A fresh `Mat3` is already the identity. The function just gives it a clear name. |
| 16–21 | `inline Mat3 translation(double tx, double ty) { Mat3 r; r.m[0][2] = tx; r.m[1][2] = ty; return r; }` | Start from the identity and fill in the moving part: the last column (Section 32.7). |
| 23–28 | `inline Mat3 scaling(double sx, double sy) { Mat3 r; r.m[0][0] = sx; r.m[1][1] = sy; return r; }` | The scales go on the diagonal (Section 32.4). |
| 30–32 | `inline Mat3 rotation(double radians) { double c = std::cos(radians); double s = std::sin(radians);` | Cosine and sine, once. |
| 33–39 | `Mat3 r; r.m[0][0] = c; r.m[0][1] = -s; r.m[1][0] = s; r.m[1][1] = c; return r; }` | Column 0 is (cos θ, sin θ), column 1 is (−sin θ, cos θ). Notice where the minus goes: **top right**. |
| 41–46 | `inline Mat3 skew(double kx, double ky) { Mat3 r; r.m[0][1] = kx; r.m[1][0] = ky; return r; }` | The skew amounts go in the two corners off the diagonal (Section 32.5). |
| 48 | `inline Mat3 operator*(const Mat3& a, const Mat3& b) {` | So we can write `a * b` for the matrix product (Section 32.9). The matrices are passed by `const` reference: 9 numbers each, read but not changed. |
| 49 | `Mat3 r;` | The result. (Every entry is set below, so its starting values do not matter.) |
| 50–51 | `for (int row = 0; row < 3; ++row) { for (int col = 0; col < 3; ++col) {` | Every entry of the result. |
| 52–55 | `double sum = 0.0; for (int k = 0; k < 3; ++k) { sum += a.m[row][k] * b.m[k][col]; }` | Row `row` of a, dotted with column `col` of b: walk **across** a's row and **down** b's column together. |
| 56–60 | `r.m[row][col] = sum;` … `return r; }` | Store each entry, and return the product. |
| 62–65 | `inline Vec2 applyToPoint(const Mat3& t, Vec2 p) { return Vec2{t.m[0][0] * p.x + t.m[0][1] * p.y + t.m[0][2], t.m[1][0] * p.x + t.m[1][1] * p.y + t.m[1][2]}; }` | Matrix × (x, y, 1). The third number of the result is always 1, so we skip it (Section 32.7). |
| 67–69 | `inline Vec2 applyToDirection(const Mat3& t, Vec2 v) { return Vec2{t.m[0][0] * v.x + t.m[0][1] * v.y, t.m[1][0] * v.x + t.m[1][1] * v.y}; }` | Matrix × (x, y, 0): the same, without the moving part (Section 32.8). |
| 71–77 | `inline std::vector<PointF> applyToPoints(const Mat3& t, const std::vector<PointF>& points) { ... }` | A new list with every point transformed — like Chapter 31's `translatePoints`, but for **any** matrix. |
| 79–81 | `inline double determinant(const Mat3& t) { return t.m[0][0] * t.m[1][1] - t.m[0][1] * t.m[1][0]; }` | a d − b c: the area factor (Section 32.12). |
| 83 | `#endif` | End of the include guard. |

---

## Code, part 2: grids, letters and squares

File: `ch32/matrices.cpp`

```cpp
#include <iostream>
#include <vector>
#include "matrix.h"
#include "hsv.h"

void printMatrix(const char* label, const Mat3& t) {
    std::cout << label << "\n";
    for (int row = 0; row < 3; ++row) {
        std::cout << "  " << t.m[row][0] << "  " << t.m[row][1] << "  " << t.m[row][2] << "\n";
    }
}

std::vector<PointF> closed(std::vector<PointF> points) {
    if (!points.empty()) {
        points.push_back(points[0]);
    }
    return points;
}

void drawGridPanel(Image& image, const Mat3& t, PointF centre) {
    Mat3 place = translation(centre.x, centre.y) * t;
    for (int i = -3; i <= 3; ++i) {
        double k = i * 20.0;
        Colour col = (i == 0) ? Colour{100, 100, 110} : Colour{195, 195, 205};
        drawLineWu(image, applyToPoint(place, Vec2{k, -60.0}), applyToPoint(place, Vec2{k, 60.0}), col);
        drawLineWu(image, applyToPoint(place, Vec2{-60.0, k}), applyToPoint(place, Vec2{60.0, k}), col);
    }
    PointF o = applyToPoint(place, Vec2{0.0, 0.0});
    drawArrowAA(image, o, applyToPoint(place, Vec2{40.0, 0.0}), 3.0, colours::red);
    drawArrowAA(image, o, applyToPoint(place, Vec2{0.0, 40.0}), 3.0, Colour{0, 150, 0});
}

int main() {
    printMatrix("rotation by 30 degrees:", rotation(degreesToRadians(30.0)));
    Mat3 move = translation(10.0, 5.0);
    Vec2 p = applyToPoint(move, Vec2{3.0, 1.0});
    Vec2 d = applyToDirection(move, Vec2{3.0, 1.0});
    std::cout << "move by (10, 5): the point (3, 1) goes to (" << p.x << ", " << p.y
              << "), the direction (3, 1) stays (" << d.x << ", " << d.y << ")\n";

    printMatrix("translation(10, 5) * scaling(2, 3):", translation(10.0, 5.0) * scaling(2.0, 3.0));
    printMatrix("scaling(2, 3) * translation(10, 5):", scaling(2.0, 3.0) * translation(10.0, 5.0));

    double quarter = degreesToRadians(90.0);
    Vec2 a = applyToPoint(translation(10.0, 0.0) * rotation(quarter), Vec2{1.0, 0.0});
    Vec2 b = applyToPoint(rotation(quarter) * translation(10.0, 0.0), Vec2{1.0, 0.0});
    std::cout << "(1, 0) with translation * rotation: (" << a.x << ", " << a.y << ")\n";
    std::cout << "(1, 0) with rotation * translation: (" << b.x << ", " << b.y << ")\n";

    printMatrix("rotation(20) * rotation(25):",
                rotation(degreesToRadians(20.0)) * rotation(degreesToRadians(25.0)));
    std::cout << "determinants: rotation " << determinant(rotation(degreesToRadians(30.0)))
              << ", scaling(2, 3) " << determinant(scaling(2.0, 3.0)) << ", mirror "
              << determinant(scaling(-1.0, 1.0)) << ", skew " << determinant(skew(0.5, 0.0)) << "\n";

    Image grids(880, 220, colours::white);
    drawGridPanel(grids, identity(), PointF{110.0, 110.0});
    drawGridPanel(grids, rotation(degreesToRadians(30.0)), PointF{330.0, 110.0});
    drawGridPanel(grids, scaling(1.5, 0.6), PointF{550.0, 110.0});
    drawGridPanel(grids, skew(0.5, 0.0), PointF{770.0, 110.0});

    Image letters(600, 160, colours::white);
    std::vector<PointF> letterF = {PointF{-30.0, 0.0},  PointF{-30.0, -100.0}, PointF{30.0, -100.0},
                                   PointF{30.0, -80.0}, PointF{-10.0, -80.0},  PointF{-10.0, -60.0},
                                   PointF{20.0, -60.0}, PointF{20.0, -40.0},   PointF{-10.0, -40.0},
                                   PointF{-10.0, 0.0}};
    const Mat3 shapes[5] = {identity(), skew(-0.3, 0.0), rotation(degreesToRadians(20.0)),
                            scaling(-1.0, 1.0), skew(-0.3, 0.0) * scaling(-1.0, 1.0)};
    for (int i = 0; i < 5; ++i) {
        Mat3 place = translation(60.0 + i * 120.0, 130.0) * shapes[i];
        fillPolygonAA(letters, applyToPoints(place, letterF), Colour{40, 60, 140});
    }

    Image squares(300, 300, colours::white);
    std::vector<PointF> square = {PointF{-100.0, -100.0}, PointF{100.0, -100.0},
                                  PointF{100.0, 100.0}, PointF{-100.0, 100.0}};
    Mat3 step = rotation(degreesToRadians(10.0)) * scaling(0.93, 0.93);
    Mat3 current = identity();
    for (int k = 0; k < 30; ++k) {
        Colour col = toColour(hsvToRgb(HSV{k * 12.0, 0.8, 0.8}));
        std::vector<PointF> corners = applyToPoints(translation(150.0, 150.0) * current, square);
        drawPolylineWu(squares, closed(corners), col);
        current = step * current;
    }

    bool ok = grids.savePPM("grids.ppm");
    ok = ok && letters.savePPM("letters.ppm");
    ok = ok && squares.savePPM("squares.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
```

Build and run (from the `code/ch32` folder):

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common matrices.cpp -o matrices
./matrices
```

### Line by line

**Helpers (lines 1–31)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–4 | the `#include` lines | Printing, lists, the new header, and `hsv.h` for rainbow colours. |
| 6–7 | `void printMatrix(const char* label, const Mat3& t) { std::cout << label << "\n";` | Print a label, then the matrix. |
| 8–11 | `for (int row = 0; row < 3; ++row) { std::cout << "  " << t.m[row][0] << "  " << t.m[row][1] << "  " << t.m[row][2] << "\n"; } }` | One line per row, entries separated by two spaces. |
| 13–18 | `std::vector<PointF> closed(std::vector<PointF> points) { ... }` | The same helper as Chapter 31: repeat the first point at the end, to close an outline. |
| 20 | `void drawGridPanel(Image& image, const Mat3& t, PointF centre) {` | Draw a grid and two arrows through the matrix t, in a panel around `centre` (Section 32.4). |
| 21 | `Mat3 place = translation(centre.x, centre.y) * t;` | First t (the grid is built around (0, 0)), **then** move to the panel's centre. Right to left! |
| 22–24 | `for (int i = -3; i <= 3; ++i) { double k = i * 20.0; Colour col = (i == 0) ? ... : ...;` | Seven lines each way, at −60, −40, … 60. The two lines through (0, 0) are darker. |
| 25 | `drawLineWu(image, applyToPoint(place, Vec2{k, -60.0}), applyToPoint(place, Vec2{k, 60.0}), col);` | An upright grid line, from its top end to its bottom end, both transformed. (Straight lines stay straight, Chapter 31 Section 31.1, so the two ends are enough.) |
| 26 | `drawLineWu(image, applyToPoint(place, Vec2{-60.0, k}), applyToPoint(place, Vec2{60.0, k}), col);` | A level grid line. |
| 27 | `}` | End of the loop. |
| 28 | `PointF o = applyToPoint(place, Vec2{0.0, 0.0});` | Where the grid's middle ends up (the panel centre). |
| 29 | `drawArrowAA(image, o, applyToPoint(place, Vec2{40.0, 0.0}), 3.0, colours::red);` | Red arrow: where (40, 0) goes — 40 × column 0 (Chapter 29's arrow). |
| 30–31 | `drawArrowAA(image, o, applyToPoint(place, Vec2{0.0, 40.0}), 3.0, Colour{0, 150, 0});` `}` | Green arrow: where (0, 40) goes — 40 × column 1. |

**The numbers (lines 33–54)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 34 | `printMatrix("rotation by 30 degrees:", rotation(degreesToRadians(30.0)));` | The rotation matrix of Section 32.4. |
| 35–39 | `Mat3 move = translation(10.0, 5.0);` … | A point moves, a direction does not (Section 32.8). |
| 41–42 | the two `printMatrix` lines | The two orders of Section 32.10. |
| 44–48 | `double quarter = ...;` `Vec2 a = applyToPoint(translation(10.0, 0.0) * rotation(quarter), Vec2{1.0, 0.0});` … | Chapter 31's order example, now with matrix products. |
| 50–51 | `printMatrix("rotation(20) * rotation(25):", ...);` | Two turns make one (Section 32.10). |
| 52–54 | `std::cout << "determinants: rotation " << determinant(...) ...` | The four determinants of Section 32.12. |

**The grid panels (lines 56–60)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 56 | `Image grids(880, 220, colours::white);` | Four panels of 220 × 220, side by side. |
| 57–60 | four `drawGridPanel` calls | The identity, a 30° turn, a scale (1.5, 0.6) and a skew (0.5, 0), with panel centres 220 pixels apart. |

**The letters (lines 62–72)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 62 | `Image letters(600, 160, colours::white);` | A wide picture. |
| 63–66 | `std::vector<PointF> letterF = {...};` | A capital F with 10 corners: (0, 0) is the middle of its foot, and it is 60 wide and 100 tall (y from 0 up to −100). |
| 67–68 | `const Mat3 shapes[5] = {identity(), skew(-0.3, 0.0), rotation(degreesToRadians(20.0)), scaling(-1.0, 1.0), skew(-0.3, 0.0) * scaling(-1.0, 1.0)};` | The five shape matrices of Section 32.11. An array of matrices: each one is a whole transformation, stored like any other value. |
| 69–70 | `for (int i = 0; i < 5; ++i) { Mat3 place = translation(60.0 + i * 120.0, 130.0) * shapes[i];` | Shape first, then move to its place on the baseline y = 130. |
| 71–72 | `fillPolygonAA(letters, applyToPoints(place, letterF), Colour{40, 60, 140});` `}` | Transform all 10 corners with one matrix, and fill smoothly. |

**The spiral of squares (lines 74–84)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 74–76 | `Image squares(300, 300, colours::white);` / `std::vector<PointF> square = {...};` | A square 200 pixels wide, centred on (0, 0). |
| 77 | `Mat3 step = rotation(degreesToRadians(10.0)) * scaling(0.93, 0.93);` | Shrink to 93 %, then turn 10° (right to left). |
| 78 | `Mat3 current = identity();` | Before the first step: no change. |
| 79–80 | `for (int k = 0; k < 30; ++k) { Colour col = toColour(hsvToRgb(HSV{k * 12.0, 0.8, 0.8}));` | Thirty squares, the hue moving 12° each time. |
| 81 | `std::vector<PointF> corners = applyToPoints(translation(150.0, 150.0) * current, square);` | Apply `current`, then move to the middle of the picture. |
| 82 | `drawPolylineWu(squares, closed(corners), col);` | A smooth outline. |
| 83–84 | `current = step * current;` `}` | One more step for the next square. `step` is on the **left**: it happens after everything already in `current`. (Here both orders give the same result, because turns and uniform scales about the same point do not care about order — Chapter 31 Section 31.8. But putting the new step on the left is the safe habit.) |

**Saving (lines 86–94)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 86–88 | `bool ok = grids.savePPM("grids.ppm");` … | Save the three pictures. |
| 89–94 | `if (!ok) { ... }` `return 0;` `}` | Report a problem, or finish. |

### What you should see

```
rotation by 30 degrees:
  0.866025  -0.5  0
  0.5  0.866025  0
  0  0  1
move by (10, 5): the point (3, 1) goes to (13, 6), the direction (3, 1) stays (3, 1)
translation(10, 5) * scaling(2, 3):
  2  0  10
  0  3  5
  0  0  1
scaling(2, 3) * translation(10, 5):
  2  0  20
  0  3  15
  0  0  1
(1, 0) with translation * rotation: (10, 1)
(1, 0) with rotation * translation: (6.73556e-16, 11)
rotation(20) * rotation(25):
  0.707107  -0.707107  0
  0.707107  0.707107  0
  0  0  1
determinants: rotation 1, scaling(2, 3) 6, mirror -1, skew 1
```

Open the pictures:
- `grids.ppm`: four grids with a red and a green arrow each — a plain square grid, a turned one, a wide flat one, and a slanted one. In every panel, the arrows show the matrix's two columns.
- `letters.ppm`: five blue F's: normal, italic, turned, mirrored, and mirrored-and-italic.
- `squares.ppm`: thirty rainbow square outlines spiralling inward to the middle.

---

## Small examples

### Example 1 — Reading a matrix

```
[ 0  −1  50 ]
[ 1   0  20 ]
[ 0   0   1 ]
```

> Column 0 = (0, 1): (1, 0) goes to (0, 1) — right turns into down.
> Column 1 = (−1, 0): down turns into left.
> That is a clockwise quarter turn on the screen (rotation by 90°), followed by a move by (50, 20).
> Check on (10, 0): (0 × 10 − 1 × 0 + 50, 1 × 10 + 0 + 20) = **(50, 30)** ✓ (turn → (0, 10), move → (50, 30))

### Example 2 — Building a matrix from the columns

We want a matrix that sends (1, 0) to (2, 1) and (0, 1) to (−1, 2), with no move:

```
[ 2  −1  0 ]
[ 1   2  0 ]
[ 0   0  1 ]
```

> Its determinant: 2 × 2 − (−1) × 1 = 5. The columns are perpendicular and both have length √5, so it is a turn (by atan2(1, 2) ≈ 26.6°, Chapter 30) and a scale by √5 ≈ 2.236 — and √5 × √5 = 5 ✓.

### Example 3 — A direction under a matrix

The direction (1, 0) under translation(100, 0) × scaling(3, 3): applyToDirection gives **(3, 0)** — scaled, but not moved. The point (1, 0) under the same matrix: **(103, 0)**.

### Example 4 — The identity does nothing

identity × (7, −2, 1) = (1 × 7 + 0 + 0, 0 + 1 × (−2) + 0, 1) = **(7, −2)** ✓

### Example 5 — Undoing by hand

translation(10, 5) × translation(−10, −5) = translation(0, 0) = the **identity**: moving there and back is no move at all. In the same way, rotation(θ) × rotation(−θ) = identity, and scaling(2, 2) × scaling(0.5, 0.5) = identity. (Chapter 33 finds the undo matrix for **any** matrix.)

---

## Common mistakes

⚠️ **Column first instead of row first.** In `m[row][col]`, the **row** comes first. The moving part is the **last column**: `m[0][2]` and `m[1][2]`.

⚠️ **Multiplying in the wrong order.** In A × B, **B acts first**. "Scale, then turn, then move" is `translation * rotation * scaling`.

⚠️ **The minus sign in the wrong corner.** The rotation matrix has −sin θ at the **top right**. Check: column 0 must be (cos θ, sin θ), where (1, 0) goes.

⚠️ **Moving directions.** A direction (an arrow, a step, a speed) must not be moved by translations. Use `applyToDirection`, not `applyToPoint`.

⚠️ **Forgetting to add up all three products.** Each entry of a matrix product is a sum of three products: row of a · column of b. Leaving one out gives a nearly-right matrix that is very hard to debug.

⚠️ **Changing a matrix while multiplying it.** Writing `a = a * b` is fine (the product is built in a new `Mat3 r` first). But a hand-written "in place" multiplication that overwrites `a.m[0][0]` before it has been used for every entry gives wrong answers.

---

## Practice

🏋️ **1.** Multiply by hand:

```
[ 3  1 ]   [ 2 ]
[ 0  2 ] × [ 5 ]
```

🏋️ **2.** Write the 3 × 3 matrix that mirrors upside down (across the level line y = 0), and then moves down by 100.

🏋️ **3.** What transformation does this matrix do? Find where (1, 0) and (0, 1) go, and its determinant.

```
[ 0  1  0 ]
[ 1  0  0 ]
[ 0  0  1 ]
```

🏋️ **4.** Multiply rotation(90°) × scaling(2, 1) by hand (use cos 90° = 0, sin 90° = 1). Then multiply scaling(2, 1) × rotation(90°). Are they the same? Apply both to (1, 0).

🏋️ **5.** Write a function `Mat3 rotationAbout(PointF c, double radians)` using three matrices. (Chapter 31: move the pivot to the origin, turn, move back.) Which order do the three go in?

🏋️ **6.** Draw a **clock** with matrices: build each hour mark once as a small rectangle (four points) in local coordinates, and place it 12 times with translation(c) × rotation(i × 30°) × translation(0, −110).

🏋️ **7.** The skew(0.5, 0) panel: what are the four corners of the grid (±60, ±60) after the skew? What is the area of the slanted grid, and does it agree with the determinant?

🏋️ **8.** In `squares.ppm`, how many steps does it take for a square to be smaller than 10 pixels across? (0.93ᵏ × 200 < 10.)

---

## Answers

**1.**
> (3 × 2 + 1 × 5, 0 × 2 + 2 × 5) = **(11, 10)**

**2.**
> Mirror upside down: (1, 0) stays, (0, 1) goes to (0, −1). Then move by (0, 100). Mirror first, so translation × scaling(1, −1):

```
[ 1   0    0 ]
[ 0  −1  100 ]
[ 0   0    1 ]
```

> Check: (5, 20) → (5, −20 + 100) = (5, 80). A point near the top goes near the bottom (of a 100-pixel-high area) ✓

**3.**
> (1, 0) → (0, 1), and (0, 1) → (1, 0): it **swaps x and y**. That is a mirror across the diagonal line y = x. Determinant: 0 × 0 − 1 × 1 = **−1** — a mirror ✓

**4.**
> rotation(90°) × scaling(2, 1): the rotation has columns (0, 1) and (−1, 0); the scale has columns (2, 0) and (0, 1).

```
rotation × scaling            scaling × rotation
[ 0  −1  0 ]                  [ 0  −2  0 ]
[ 2   0  0 ]                  [ 1   0  0 ]
[ 0   0  1 ]                  [ 0   0  1 ]
```

> Not the same. On (1, 0): the first gives **(0, 2)** (stretch to (2, 0), then turn to (0, 2)); the second gives **(0, 1)** (turn to (0, 1), then the across-stretch does nothing to it).

**5.**

```cpp
Mat3 rotationAbout(PointF c, double radians) {
    return translation(c.x, c.y) * rotation(radians) * translation(-c.x, -c.y);
}
```

> Right to left: **first** move the pivot to the origin (translation by −c), then turn, then move back (translation by +c). Chapter 33 builds on exactly this.

**6.**

```cpp
Image dial(300, 300, colours::white);
std::vector<PointF> mark = {PointF{-3.0, -15.0}, PointF{3.0, -15.0}, PointF{3.0, 15.0},
                            PointF{-3.0, 15.0}};
for (int i = 0; i < 12; ++i) {
    Mat3 place = translation(150.0, 150.0) * rotation(degreesToRadians(i * 30.0)) *
                 translation(0.0, -110.0);
    fillPolygonAA(dial, applyToPoints(place, mark), colours::black);
}
```

> Right to left: move the mark **up** 110 (to the 12 o'clock place), then turn it around (0, 0) — it swings around like a clock hand and stays pointing at the middle — then move the whole dial to (150, 150).

**7.**
> new x = x + 0.5 y: (−60, −60) → **(−90, −60)**, (60, −60) → **(30, −60)**, (60, 60) → **(90, 60)**, (−60, 60) → **(−30, 60)**
> A parallelogram: each level side is still 120 long, and the height is still 120: area **120 × 120 = 14,400** — the same as the square. Determinant 1 ✓

**8.**
> 0.93ᵏ < 10 / 200 = 0.05. Try: 0.93⁴⁰ ≈ 0.055, 0.93⁴¹ ≈ 0.051, 0.93⁴² ≈ 0.047. So after **42** steps. (Our loop stops at 29, at about 24 pixels.)

---

## Summary

🧠 A **matrix** is a table of numbers. Matrix × point: each **row** · the point gives one new coordinate.

🧠 **Column 0 = where (1, 0) goes; column 1 = where (0, 1) goes.** That is how to build any matrix, and how to read one.

🧠 Scale: diagonal (sx, sy). Rotate: columns (cos θ, sin θ) and (−sin θ, cos θ). Skew: kx and ky off the diagonal. Mirror: a −1 on the diagonal.

🧠 **Homogeneous coordinates**: points are (x, y, 1). A 3 × 3 matrix with (tx, ty) in the last column **moves** points. Directions are (x, y, 0): they turn and stretch, but never move.

🧠 **Matrix product**: entry = row of A · column of B. **(A × B)p = A(Bp): the right-hand matrix acts first.** A × B ≠ B × A.

🧠 "Scale, then rotate, then move" = **translation × rotation × scaling**. The **identity** changes nothing.

🧠 **Determinant** a d − b c: the area factor. Negative means a mirror; 0 means everything is squashed flat.

---

## Next chapter

We can now build transformations as matrices and multiply them together. In Chapter 33 we use them for real: turning and scaling **around any pivot** with one matrix, building **hierarchies** (a hand that moves with the arm that moves with the body), finding the **inverse** matrix that undoes a transformation — and using that inverse to do something new: **rotating, scaling and skewing a whole image**, pixel by pixel, with the "undo the transformation" trick from Chapter 31.
