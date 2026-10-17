# Chapter 3 — Grids and Coordinates

> **Part 1 · Chapter 3 of 82**
> **You need:** Chapters 1–2 · **You will make:** a program that prints a labelled grid, marks a pixel and its neighbours, and checks the edges

---

## What you will learn

- How two numbers, **x** and **y**, name every pixel in an image.
- Why pixel **(0, 0)** is the **top-left** corner, and why **y goes down**.
- How to change between "maths y" (up) and "image y" (down).
- How to test if a position is **inside** the image.
- What the **neighbours** of a pixel are.
- How far apart two pixels are (with **Pythagoras**).
- Where the **centre** of a pixel is, and why that matters later.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **number line** | A straight line with numbers marked on it, in order. |
| **coordinate** | A number that tells a position along one direction. |
| **axis** (plural: **axes**) | One direction we measure along: the x axis goes across, the y axis goes down. |
| **origin** | The place where x = 0 and y = 0. |
| **row** | One line of pixels going across. All pixels in a row have the same y. |
| **column** | One line of pixels going down. All pixels in a column have the same x. |
| **in bounds** | Inside the image. A position that really is a pixel. |
| **neighbour** | A pixel right next to another pixel. |
| **offset** | How far you move from one place to another, like "+1 in x". |
| **distance** | How far apart two places are. |
| **pixel centre** | The exact middle of a pixel's square. |

---

## 3.1 One number for one direction

📖 **New word: number line** — a straight line with numbers marked on it, in order.

```
 0   1   2   3   4   5   6   7
 |---|---|---|---|---|---|---|
```

If I say "go to 5", you know exactly where to stand. One number is enough when there is only **one direction**.

📖 **New word: coordinate** — a number that tells a position along one direction.

In images, we **always start counting at 0**, not at 1. This matches C++ arrays and vectors: the first element is `[0]`.

🔢 **Maths: how many places from 0 to 7?**

> Places: 0, 1, 2, 3, 4, 5, 6, 7
> Count them: 8 places.
> Rule: from 0 to n, there are n + 1 places.
> Here n = 7, so 7 + 1 = 8.

So if an image is **8 pixels wide**, its x coordinates go from **0 to 7**. The last one is `width - 1`.

🧠 **Remember:** For an image of width `w`, x goes from `0` to `w − 1`. **There is no pixel at x = w.**

---

## 3.2 Two numbers for a grid

An image is a grid. It has two directions: **across** and **down**. So we need **two** coordinates.

📖 **New word: axis** — one direction we measure along. The **x axis** goes across. The **y axis** goes down. Two of them are called **axes**.

We write a position as **(x, y)**. **x first, then y.** Always.

- **x** says how far **across** (to the right).
- **y** says how far **down**.

```
        x →
        0   1   2   3   4
      +---+---+---+---+---+
 y  0 |   |   |   |   |   |
 ↓    +---+---+---+---+---+
    1 |   |   |   | A |   |
      +---+---+---+---+---+
    2 |   | B |   |   |   |
      +---+---+---+---+---+
```

- Pixel **A** is at **(3, 1)**: 3 across, 1 down.
- Pixel **B** is at **(1, 2)**: 1 across, 2 down.

⚠️ **Careful:** (3, 1) and (1, 3) are **different** pixels. The order matters. x is always first.

📖 **New word: row** — one line of pixels going across. All pixels in one row have the **same y**.

📖 **New word: column** — one line of pixels going down. All pixels in one column have the **same x**.

| | Changes | Stays the same |
|---|---|---|
| Moving along a **row** | x | y |
| Moving down a **column** | y | x |

---

## 3.3 Why (0, 0) is the top-left

📖 **New word: origin** — the place where x = 0 and y = 0.

In images, the origin is the **top-left** pixel. And **y grows downward**.

Why? Because of how old screens worked, and how we read:

1. Old TV screens drew the picture **line by line, from the top**, like a person reading a page.
2. Each line was drawn **from left to right**.
3. So the first thing drawn was the top-left corner. It got the number 0.

```
reading a page:          drawing a screen:
  → → → → → →              → → → → → →   row 0
  → → → → → →              → → → → → →   row 1
  → → → → → →              → → → → → →   row 2
```

Almost all image file formats store pixels in this order: **row 0 first** (the top), and inside each row, **x = 0 first** (the left). We will use this order in Chapter 6 and in our first file in Chapter 8.

💡 **Tip:** One famous format, BMP, stores rows **from the bottom up**! We will handle that in Chapter 36. For now, top-left is the rule.

---

## 3.4 Maths y and image y

In school maths, y usually goes **up**:

```
 school maths              images
   y ↑                      (0,0) ──── x →
     │                        │
     │                        │
     └──── x →                ↓ y
   (0,0)
```

Both are fine. They are just different rules. But we must not mix them up.

Sometimes we want to think in "maths y" (up), for example when we draw a graph of a function in Chapter 13. Then we change it to "image y" (down) before we set the pixel.

🔢 **Maths: changing maths y into image y**

Say the image has height `h`. In maths style, `y = 0` is the **bottom** row. In image style, the bottom row is `y = h − 1`.

The rule is:

> image_y = (h − 1) − maths_y

Let us check with h = 5 (rows 0 to 4):

| maths_y | (h − 1) − maths_y | image_y | Where |
|---|---|---|---|
| 0 | 4 − 0 | 4 | bottom row ✓ |
| 1 | 4 − 1 | 3 | |
| 2 | 4 − 2 | 2 | middle row (same in both!) |
| 3 | 4 − 3 | 1 | |
| 4 | 4 − 4 | 0 | top row ✓ |

The same rule also changes image y back into maths y:

> maths_y = (h − 1) − image_y

Try it: image_y = 4 → (5 − 1) − 4 = 0. Correct, the bottom row.

🧠 **Remember:** In this book, **(0, 0) is top-left and y goes down**, unless we clearly say "maths y". To flip: `y_flipped = (h − 1) − y`.

---

## 3.5 The four corners

Let us name the corners of an image with width `w` and height `h`.

| Corner | x | y |
|---|---|---|
| top-left | 0 | 0 |
| top-right | w − 1 | 0 |
| bottom-left | 0 | h − 1 |
| bottom-right | w − 1 | h − 1 |

🔢 **Maths: corners of an 8 × 5 image**

> w = 8, h = 5
> w − 1 = 7
> h − 1 = 4

| Corner | (x, y) |
|---|---|
| top-left | (0, 0) |
| top-right | (7, 0) |
| bottom-left | (0, 4) |
| bottom-right | (7, 4) |

```
(0,0) ● · · · · · · ● (7,0)
      · · · · · · · ·
      · · · · · · · ·
      · · · · · · · ·
(0,4) ● · · · · · · ● (7,4)
```

---

## 3.6 Inside or outside?

📖 **New word: in bounds** — inside the image. A position that really is a pixel.

Later we will draw lines and circles. Sometimes they go **past the edge** of the image. If we try to write a pixel at x = 9 in an 8-wide image, we write into memory that is **not ours**. That is a serious bug.

So we need a test: **is (x, y) inside?**

🔢 **Maths: the four conditions**

A position (x, y) is inside an image of width `w` and height `h` when **all four** are true:

> x ≥ 0
> x < w      (not ≤, because the last x is w − 1)
> y ≥ 0
> y < h

Examples with w = 8, h = 5:

| (x, y) | x ≥ 0 | x < 8 | y ≥ 0 | y < 5 | Inside? |
|---|---|---|---|---|---|
| (3, 2) | yes | yes | yes | yes | **yes** |
| (7, 4) | yes | yes | yes | yes | **yes** (the last pixel) |
| (8, 4) | yes | **no** | yes | yes | **no** |
| (−1, 0) | **no** | yes | yes | yes | **no** |
| (2, 5) | yes | yes | yes | **no** | **no** |

In C++ this becomes one small function. We write it in this chapter's code and use it for the rest of the book.

⚠️ **Careful:** Writing `x <= w` is a very common mistake. It lets x = w through, which is one pixel past the edge.

---

## 3.7 Neighbours

📖 **New word: neighbour** — a pixel right next to another pixel.

📖 **New word: offset** — how far you move. For example, "+1 in x, 0 in y" means "one step right".

### The 4 neighbours

The pixels **directly** left, right, above and below:

```
        (x, y−1)
           ↑
(x−1, y) ← ● → (x+1, y)
           ↓
        (x, y+1)
```

| Direction | Offset in x | Offset in y |
|---|---|---|
| right | +1 | 0 |
| left | −1 | 0 |
| down | 0 | +1 |
| up | 0 | −1 |

⚠️ **Careful:** **Up is −1** in y, because y grows downward. This surprises many people.

### The 8 neighbours

The 4 neighbours **plus** the 4 diagonal ones:

```
(x−1,y−1) (x,y−1) (x+1,y−1)
(x−1,y)      ●    (x+1,y)
(x−1,y+1) (x,y+1) (x+1,y+1)
```

We use neighbours in **flood fill** (Chapter 25) and in **blur** and **edge detection** (Chapters 49–51).

🔢 **Maths: neighbours of (5, 2)**

> right: (5 + 1, 2) = (6, 2)
> left:  (5 − 1, 2) = (4, 2)
> down:  (5, 2 + 1) = (5, 3)
> up:    (5, 2 − 1) = (5, 1)

### Neighbours at the edge

A pixel at the edge has **fewer** neighbours inside the image. The bottom-right pixel (7, 4) of an 8 × 5 image:

> right: (8, 4) → x = 8 is not < 8 → **outside**
> left:  (6, 4) → **inside**
> down:  (7, 5) → y = 5 is not < 5 → **outside**
> up:    (7, 3) → **inside**

So it has only **2** of its 4 neighbours inside. Our code checks this.

---

## 3.8 Distance between two pixels

📖 **New word: distance** — how far apart two places are.

Take two pixels: **P = (1, 1)** and **Q = (4, 5)**.

🔢 **Maths: step 1 — the differences**

> dx = Q.x − P.x = 4 − 1 = 3
> dy = Q.y − P.y = 5 − 1 = 4

`dx` means "difference in x". `dy` means "difference in y".

### Distance by steps

If you can only walk right/left/up/down (like a rook in chess, or along city streets), the distance is:

> steps = |dx| + |dy| = 3 + 4 = 7

The bars `| |` mean "**absolute value**": drop the minus sign if there is one. |−3| = 3.

### Straight-line distance (Pythagoras)

If you can walk in a **straight line**, the path is shorter. Look at the triangle:

```
P ●
  │ \
  │   \   straight line = ?
dy=4    \
  │       \
  └─────────● Q
     dx=3
```

The famous rule of **Pythagoras** says: for a triangle with a square corner,

> (straight line)² = dx² + dy²

🔢 **Maths: the straight distance from P to Q**

> dx² = 3 × 3 = 9
> dy² = 4 × 4 = 16
> dx² + dy² = 9 + 16 = 25
> straight line = √25 = 5

So the straight distance is **5 pixels**. That is shorter than 7 steps, as it should be.

A second example: P = (0, 0), Q = (1, 1) — a diagonal neighbour.

> dx = 1, dy = 1
> dx² + dy² = 1 + 1 = 2
> distance = √2 ≈ 1.414

So a **diagonal** neighbour is about 1.41 pixels away. A straight neighbour is exactly 1 away.

💡 **Tip:** Often we only need to **compare** distances ("is this pixel closer than that one?"). Then we can skip the square root and compare dx² + dy² directly. It gives the same answer and is faster. Our code uses this trick: a pixel is a **4-neighbour** exactly when dx² + dy² = 1.

🧠 **Remember:** distance = √(dx² + dy²). This rule draws every circle in Chapter 22 and every sphere in Chapter 72.

---

## 3.9 Where is the centre of a pixel?

📖 **New word: pixel centre** — the exact middle of a pixel's square.

So far, a pixel was just a cell with two whole numbers. But a pixel is really a small **square**. Pixel (x, y) covers the area:

> from x to x + 1 across
> from y to y + 1 down

```
 x=2      x=3
  ┌────────┐ y=1
  │        │
  │   ●    │   ● = centre at (2.5, 1.5)
  │        │
  └────────┘ y=2
```

🔢 **Maths: the centre**

> centre_x = x + 0.5
> centre_y = y + 0.5

For pixel (2, 1): centre = (2 + 0.5, 1 + 0.5) = **(2.5, 1.5)**.

Why does this matter? When we ask "is this pixel inside a circle?" (Chapter 22) or "where does this ray go?" (Chapter 71), we use the **centre** of the pixel. If we use the corner instead, every shape moves by half a pixel. Small, but you can see it.

🧠 **Remember:** Pixel (x, y) has its centre at **(x + 0.5, y + 0.5)**.

---

## Code

File: `ch03/grid.cpp`

```cpp
#include <iostream>

bool isInside(int x, int y, int width, int height) {
    return x >= 0 && x < width && y >= 0 && y < height;
}

int main() {
    const int width = 8;
    const int height = 5;

    const int markX = 5;
    const int markY = 2;

    std::cout << "    ";
    for (int x = 0; x < width; ++x) {
        std::cout << x << ' ';
    }
    std::cout << "  <- x\n";

    for (int y = 0; y < height; ++y) {
        std::cout << y << " | ";
        for (int x = 0; x < width; ++x) {
            int dx = x - markX;
            int dy = y - markY;
            int distSquared = dx * dx + dy * dy;
            if (distSquared == 0) {
                std::cout << "X ";
            } else if (distSquared == 1) {
                std::cout << "o ";
            } else {
                std::cout << ". ";
            }
        }
        std::cout << "\n";
    }
    std::cout << "^\ny\n\n";

    const int cornerX = width - 1;
    const int cornerY = height - 1;
    const int stepX[4] = {1, -1, 0, 0};
    const int stepY[4] = {0, 0, 1, -1};

    std::cout << "Neighbours of (" << cornerX << ", " << cornerY << "):\n";
    for (int i = 0; i < 4; ++i) {
        int nx = cornerX + stepX[i];
        int ny = cornerY + stepY[i];
        std::cout << "  (" << nx << ", " << ny << ") ";
        if (isInside(nx, ny, width, height)) {
            std::cout << "inside\n";
        } else {
            std::cout << "outside\n";
        }
    }

    int mathsY = 0;
    int imageY = (height - 1) - mathsY;
    std::cout << "\nmaths y = " << mathsY << " is image y = " << imageY << "\n";
    return 0;
}
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1 | `#include <iostream>` | Lets us print. |
| 3 | `bool isInside(int x, int y, int width, int height) {` | A function that answers "is (x, y) a real pixel of this image?" with `true` or `false`. |
| 4 | `return x >= 0 && x < width && y >= 0 && y < height;` | The four conditions from Section 3.6. All four must be true. Note `<`, not `<=`. |
| 5 | `}` | End of the function. |
| 7 | `int main() {` | The program starts here. |
| 8 | `const int width = 8;` | The grid is 8 pixels across (x = 0 to 7). |
| 9 | `const int height = 5;` | The grid is 5 pixels down (y = 0 to 4). |
| 11 | `const int markX = 5;` | The x of the pixel we will mark. |
| 12 | `const int markY = 2;` | The y of the pixel we will mark. So we mark pixel (5, 2). |
| 14 | `std::cout << "    ";` | Four spaces, so the column numbers line up with the grid below. (Each grid row starts with 4 characters: the row number, a space, a bar and a space.) |
| 15–17 | `for (int x = 0; ...) { std::cout << x << ' '; }` | Print the column numbers 0 to 7 across the top, each followed by a space. |
| 18 | `std::cout << "  <- x\n";` | A label that says these are x values. Then a new line. |
| 20 | `for (int y = 0; y < height; ++y) {` | Go through the rows from **top (y = 0) to bottom**. |
| 21 | `std::cout << y << " | ";` | Print the row number and a bar at the start of each row. |
| 22 | `for (int x = 0; x < width; ++x) {` | Go across the row, left to right. |
| 23 | `int dx = x - markX;` | How far across this pixel is from the marked pixel. |
| 24 | `int dy = y - markY;` | How far down this pixel is from the marked pixel. |
| 25 | `int distSquared = dx * dx + dy * dy;` | The **squared** distance (Section 3.8). We skip the square root because we only compare with 0 and 1. |
| 26–27 | `if (distSquared == 0) { std::cout << "X "; }` | Distance 0 means this **is** the marked pixel. Print `X`. |
| 28–29 | `else if (distSquared == 1) { std::cout << "o "; }` | Squared distance 1 happens **only** for the 4 neighbours (one step left, right, up or down). Diagonals give 1 + 1 = 2, so they are not marked. Print `o`. |
| 30–32 | `else { std::cout << ". "; }` | Any other pixel: print a dot. |
| 33 | `}` | End of one row. |
| 34 | `std::cout << "\n";` | New line before the next row. |
| 35 | `}` | End of all rows. |
| 36 | `std::cout << "^\ny\n\n";` | An arrow and the letter y under the row numbers, to show that **y goes down**. Then an empty line. |
| 38 | `const int cornerX = width - 1;` | The x of the bottom-right corner: 8 − 1 = 7. |
| 39 | `const int cornerY = height - 1;` | The y of the bottom-right corner: 5 − 1 = 4. |
| 40 | `const int stepX[4] = {1, -1, 0, 0};` | The x offsets for right, left, down, up (Section 3.7). |
| 41 | `const int stepY[4] = {0, 0, 1, -1};` | The y offsets for right, left, down, up. Position `i` in both arrays belongs together. |
| 43 | `std::cout << "Neighbours of (" ... "):\n";` | A heading: "Neighbours of (7, 4):". |
| 44 | `for (int i = 0; i < 4; ++i) {` | Look at each of the 4 directions. |
| 45 | `int nx = cornerX + stepX[i];` | The neighbour's x. `nx` means "neighbour x". |
| 46 | `int ny = cornerY + stepY[i];` | The neighbour's y. |
| 47 | `std::cout << "  (" << nx << ", " << ny << ") ";` | Print the neighbour's position. |
| 48–52 | `if (isInside(...)) { ... "inside" } else { ... "outside" }` | Use our function to say if this neighbour is a real pixel. |
| 53 | `}` | End of the 4 directions. |
| 55 | `int mathsY = 0;` | A "maths y" of 0 means the **bottom** row (Section 3.4). |
| 56 | `int imageY = (height - 1) - mathsY;` | The flip rule. (5 − 1) − 0 = 4. |
| 57 | `std::cout << ... << "\n";` | Print the result. |
| 58 | `return 0;` | The program finished with no problem. |
| 59 | `}` | End of `main`. |

### What you should see

```
    0 1 2 3 4 5 6 7   <- x
0 | . . . . . . . . 
1 | . . . . . o . . 
2 | . . . . o X o . 
3 | . . . . . o . . 
4 | . . . . . . . . 
^
y

Neighbours of (7, 4):
  (8, 4) outside
  (6, 4) inside
  (7, 5) outside
  (7, 3) inside

maths y = 0 is image y = 4
```

Look at the grid: `X` is at column 5, row 2. The four `o` marks are its 4 neighbours. Notice that the `o` **above** the `X` is in row **1** — a **smaller** y. Up means y − 1.

---

## Small examples

### Example 1 — Mark a different pixel

Change `markX` to `0` and `markY` to `0`. Now `X` is in the top-left corner. Only **2** `o` marks appear: one to the right, one below. The other two neighbours would be at x = −1 and y = −1, which are not drawn because the loops never reach them.

### Example 2 — Show the 8 neighbours

Change line 28 to:

```cpp
} else if (distSquared <= 2) {
```

Now diagonal pixels (squared distance 1 + 1 = 2) also get an `o`. You see a 3 × 3 block with `X` in the middle:

```
1 | . . . . o o o . 
2 | . . . . o X o . 
3 | . . . . o o o . 
```

### Example 3 — Draw a small "circle" with distance

Change the tests to use a bigger distance:

```cpp
if (distSquared <= 4) {
    std::cout << "# ";
} else {
    std::cout << ". ";
}
```

This marks every pixel whose distance from (5, 2) is **2 or less** (because 2² = 4). You get a little round blob:

```
0 | . . . . . # . . 
1 | . . . . # # # . 
2 | . . . # # # # # 
3 | . . . . # # # . 
4 | . . . . . # . . 
```

You just drew a **circle** using Pythagoras! Chapter 22 does this properly.

Let us check one pixel by hand. Pixel (7, 2): dx = 7 − 5 = 2, dy = 2 − 2 = 0, so 2² + 0² = 4 ≤ 4 → `#` ✓. Pixel (7, 1): dx = 2, dy = −1, so 4 + 1 = 5 > 4 → `.` ✓.

### Example 4 — Flip every row

Print the grid **upside down** by using the flip rule in the outer loop:

```cpp
for (int row = 0; row < height; ++row) {
    int y = (height - 1) - row;
    ...
}
```

Now row 4 prints first and row 0 prints last. This is exactly what we need for BMP files in Chapter 36.

---

## Common mistakes

⚠️ **Writing (y, x) instead of (x, y).** When you **talk** about a position, it is always (x, y). But in a 2D C++ array like `picture[y][x]` (Chapter 2), y comes first. Keep these two ideas apart: the **name** is (x, y); the **2D array index** is `[y][x]`.

⚠️ **Thinking up is +1.** In images, up is **y − 1** and down is **y + 1**.

⚠️ **`x <= width` in a bounds check.** It must be `x < width`. The last pixel is `width − 1`.

⚠️ **Forgetting negative positions.** A line or a shape can start at x = −3. Check `x >= 0` too, not only the right edge.

⚠️ **Using `sqrt` to compare distances.** It works, but it is slower and can have tiny rounding errors. Compare **squared** distances when you can.

⚠️ **Using the pixel corner instead of the centre.** For exact geometry, the centre of pixel (x, y) is (x + 0.5, y + 0.5).

---

## Practice

🏋️ **1.** An image is 10 pixels wide and 6 pixels tall. Write the (x, y) of all four corners.

🏋️ **2.** In a 10 × 6 image, which of these are inside? (4, 6), (9, 0), (10, 3), (0, −1), (9, 5).

🏋️ **3.** Write the 4 neighbours of (0, 3) in a 10 × 6 image. Which ones are inside?

🏋️ **4.** What is the straight distance between (2, 3) and (8, 11)? Show every step.

🏋️ **5.** The image height is 6. Change maths y = 1 into image y. Change image y = 0 into maths y.

🏋️ **6.** What is the centre of pixel (7, 0)?

🏋️ **7.** In Example 3, we marked pixels with squared distance ≤ 4. How many `#` were there? Count them, and check one more pixel by hand: (3, 2).

🏋️ **8.** Change `grid.cpp` so it marks pixel (2, 4) with `X` and its **8** neighbours with `o`. How many `o` marks will you see? Why not 8?

---

## Answers

**1.** w = 10, h = 6, so w − 1 = 9 and h − 1 = 5.
- top-left (0, 0)
- top-right (9, 0)
- bottom-left (0, 5)
- bottom-right (9, 5)

**2.**
- (4, 6): y = 6 is not < 6 → **outside**.
- (9, 0): 9 < 10 and 0 < 6 → **inside** (the top-right corner).
- (10, 3): x = 10 is not < 10 → **outside**.
- (0, −1): y = −1 is not ≥ 0 → **outside**.
- (9, 5): **inside** (the bottom-right corner).

**3.**
- right (1, 3) → inside
- left (−1, 3) → **outside** (x < 0)
- down (0, 4) → inside
- up (0, 2) → inside

So **3** neighbours are inside.

**4.**
> dx = 8 − 2 = 6
> dy = 11 − 3 = 8
> dx² = 36, dy² = 64
> dx² + dy² = 36 + 64 = 100
> distance = √100 = **10**

**5.** h = 6, so h − 1 = 5.
> maths y = 1 → image y = 5 − 1 = **4**
> image y = 0 → maths y = 5 − 0 = **5**

**6.** (7 + 0.5, 0 + 0.5) = **(7.5, 0.5)**.

**7.** Count each row of the picture in Example 3: row 0 has 1, row 1 has 3, row 2 has 5, row 3 has 3, row 4 has 1.
> 1 + 3 + 5 + 3 + 1 = **13** `#` marks.

Pixel (3, 2): dx = 3 − 5 = −2, dy = 0. (−2)² + 0² = 4 ≤ 4 → `#` ✓. (Squaring removes the minus sign: −2 × −2 = 4.)

**8.** Set `markX = 2`, `markY = 4`, and use `distSquared <= 2` as in Example 2. You will see only **5** `o` marks. The pixel is on the **bottom row** (y = 4 is the last row). The three neighbours below it would be at y = 5, which is outside the 5-row grid, so they are never printed. The 5 you see are: (1, 3), (2, 3), (3, 3), (1, 4) and (3, 4).

---

## Summary

🧠 Every pixel has a name **(x, y)**: x across, y down. **x is always first.**

🧠 The **origin (0, 0) is the top-left**. **y grows downward**. Up is y − 1.

🧠 For width `w`, x goes from 0 to **w − 1**. For height `h`, y goes from 0 to **h − 1**.

🧠 **Inside test:** `x >= 0 && x < w && y >= 0 && y < h`.

🧠 To flip y: `y_flipped = (h − 1) − y`.

🧠 4 neighbours: right, left, down, up. 8 neighbours add the diagonals.

🧠 **Distance = √(dx² + dy²)**. To compare, use dx² + dy² without the root.

🧠 The **centre** of pixel (x, y) is **(x + 0.5, y + 0.5)**.

---

## Next chapter

Pixels hold **numbers**. But how does a computer store a number? In Chapter 4 we look at **bits, bytes and hexadecimal**, and at the exact C++ types we use to hold one byte of colour.
