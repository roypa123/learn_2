# Chapter 13 — Gradients and Linear Interpolation

> **Part 3 · Chapter 13 of 82**
> **You need:** Chapters 1–12 · **You will make:** `across.ppm`, `sky.ppm`, `rainbow.ppm` and `graph.ppm`, and three new functions in `image.h`: `lerp`, `lerpByte`, `lerpColour`

---

## What you will learn

- What "part of the way between two numbers" means, exactly.
- The formula for **linear interpolation** (lerp): **a + (b − a) × t**.
- What the number **t** means, and what happens when t is below 0 or above 1.
- How to lerp **colours**, one channel at a time.
- How to get t from a pixel position: **t = x ÷ (width − 1)**, and why it is `width − 1`.
- How to make gradients of **any** size and direction, and with **many colours**.
- How to **round correctly**, even for **negative** numbers.
- **Inverse lerp** and **remap**: changing a number from one range into another.
- How to draw the **graph of a function**, using "maths y" (Chapter 3).

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **interpolation** | Finding a value **between** two known values. |
| **linear** | Changing at a steady speed, like a straight line. |
| **lerp** | Short for "linear interpolation". Also the name of our function. |
| **parameter t** | A number that says **how far** we are from the start (0) to the end (1). |
| **extrapolation** | Going **past** the ends: t below 0 or above 1. |
| **gradient** | A smooth change from one colour to another across an image. |
| **colour stop** | One fixed colour in a gradient that has several colours. |
| **inverse lerp** | The opposite of lerp: given a value, find its t. |
| **remap** | Moving a number from one range into another range. |
| **floor** | The biggest whole number that is **not bigger** than a number. |

---

## 13.1 Part of the way between two numbers

Look at a number line from 10 to 20:

```
10    12.5    15    17.5    20
 |-----|-------|-------|-----|
 0%   25%     50%     75%  100%
```

- **0%** of the way from 10 to 20 is **10** (we have not moved yet).
- **100%** of the way is **20** (we have arrived).
- **50%** of the way — halfway — is **15**.
- **25%** of the way is **12.5**.

How did we get 12.5? The whole distance is 20 − 10 = **10**. A quarter of that is 10 × 0.25 = **2.5**. Start at 10, and move 2.5: **12.5**.

📖 **New word: interpolation** — finding a value between two known values.

📖 **New word: linear** — changing at a steady speed. If you draw it, you get a straight line.

---

## 13.2 The lerp formula

📖 **New word: lerp** — short for **l**inear int**erp**olation.

📖 **New word: parameter t** — a number that says how far we are, from **0** (at the start) to **1** (at the end).

The steps from Section 13.1 become one formula:

> **lerp(a, b, t) = a + (b − a) × t**

| Part | Meaning |
|---|---|
| `a` | the start value |
| `b` | the end value |
| `b − a` | the whole distance from start to end |
| `(b − a) × t` | the part of the distance we move |
| `a + …` | start at `a`, then move that part |

🔢 **Maths: four examples**

> lerp(10, 20, 0.25) = 10 + (20 − 10) × 0.25 = 10 + 10 × 0.25 = 10 + 2.5 = **12.5**
> lerp(10, 20, 0) = 10 + 10 × 0 = **10** (t = 0 gives the start)
> lerp(10, 20, 1) = 10 + 10 × 1 = **20** (t = 1 gives the end)
> lerp(255, 0, 0.25) = 255 + (0 − 255) × 0.25 = 255 − 63.75 = **191.25**

The last one goes **down**: when `b` is smaller than `a`, `b − a` is negative, and we move backwards. The same formula works both ways.

### Another way to write it

You may also see lerp written like this:

> lerp(a, b, t) = (1 − t) × a + t × b

It is the **same** formula, rearranged. Check:

> (1 − t) × a + t × b
> = a − t × a + t × b
> = a + t × (b − a) ✓

This form shows lerp as a **mix**: "take (1 − t) parts of a and t parts of b". At t = 0.25, it is 75% of a and 25% of b.

> (1 − 0.25) × 10 + 0.25 × 20 = 0.75 × 10 + 0.25 × 20 = 7.5 + 5 = **12.5** ✓

🧠 **Remember:** **lerp(a, b, t) = a + (b − a) × t.** t = 0 gives a, t = 1 gives b, t = 0.5 gives the middle.

---

## 13.3 When t is outside 0 to 1

📖 **New word: extrapolation** — using t below 0 or above 1, so we go **past** the ends.

The formula still works:

> lerp(10, 20, 1.5) = 10 + 10 × 1.5 = 10 + 15 = **25** (past the end)
> lerp(10, 20, −0.5) = 10 + 10 × (−0.5) = 10 − 5 = **5** (before the start)

```
  5      10      15      20      25
  |-------|-------|-------|-------|
t=−0.5   t=0    t=0.5    t=1    t=1.5
```

For colours, this is dangerous. With a = 0 and b = 255:

> lerp(0, 255, 1.2) = 0 + 255 × 1.2 = **306** — too big for a byte!

If we stored 306 in a byte, it would **wrap around** to 306 − 256 = 50 (Chapter 4). So our colour lerp **limits** the result to 0–255 before storing it. This limiting is called **clamping**, and Chapter 14 explains it fully.

---

## 13.4 Lerping colours

A colour has three channels (Chapter 5). To lerp between two colours, **lerp each channel on its own**, with the **same** t.

🔢 **Maths: red to blue at t = 0.25**

> red = (255, 0, 0), blue = (0, 0, 255)
> R: lerp(255, 0, 0.25) = 255 + (0 − 255) × 0.25 = 255 − 63.75 = 191.25 → **191**
> G: lerp(0, 0, 0.25) = 0 + 0 × 0.25 = **0**
> B: lerp(0, 255, 0.25) = 0 + 255 × 0.25 = 63.75 → **64**
> result = **(191, 0, 64)** — a red with a little blue

In the RGB cube (Chapter 5, Section 5.6), this is a point **on the straight line** from the red corner to the blue corner, a quarter of the way along. That is why it is called **linear** interpolation.

🔢 **Maths: why round, not cut?**

> 63.75 cut → 63
> 63.75 rounded → 64

63.75 is much closer to 64. Cutting would make every gradient a tiny bit too dark. So we **round** (add 0.5, then cut — Chapter 5, Section 5.9).

### Our new functions for `image.h`

```cpp
inline double lerp(double a, double b, double t) {
    return a + (b - a) * t;
}
```

`lerpByte` does lerp for **one** channel: lerp, then clamp to 0–255, then round.

`lerpColour` calls `lerpByte` three times, once for R, G and B.

The full code and its line-by-line table are in the **Code** section.

---

## 13.5 Getting t from a pixel position

📖 **New word: gradient** — a smooth change from one colour to another across an image.

To make a gradient across an image, each pixel needs its own t:
- The **first** column (x = 0) should get **t = 0** (the start colour).
- The **last** column (x = width − 1) should get **t = 1** (the end colour).

> **t = x ÷ (width − 1)**

🔢 **Maths: width = 5**

| x | x ÷ (5 − 1) | t |
|---|---|---|
| 0 | 0 ÷ 4 | 0.00 |
| 1 | 1 ÷ 4 | 0.25 |
| 2 | 2 ÷ 4 | 0.50 |
| 3 | 3 ÷ 4 | 0.75 |
| 4 | 4 ÷ 4 | 1.00 |

Five pixels, perfectly spread from 0 to 1.

### Why `width − 1`, not `width`?

Try `t = x ÷ width` with width = 5:

> x = 4 (the last pixel): 4 ÷ 5 = **0.8**

The last pixel only gets t = 0.8. The end colour **never appears**! The last column of a red-to-blue gradient would be (51, 0, 204), not pure blue.

The reason: 5 pixels have only **4 gaps** between them.

```
pixel:  0     1     2     3     4
        ●─────●─────●─────●─────●
          gap   gap   gap   gap      ← 4 gaps for 5 pixels
```

t must go from 0 to 1 across the **gaps**, so we divide by the number of gaps: `width − 1`. (This is the same "n + 1 places" idea as Chapter 3, Section 3.1.)

⚠️ **Careful: integer division.** `x / (width - 1)` with two `int`s gives **0** for every pixel except the last (Chapter 5)! Make one side a `double`:

```cpp
double t = static_cast<double>(x) / (width - 1);
```

⚠️ **Careful: width 1.** If the image is only 1 pixel wide, `width − 1` is 0, and we divide by zero. Our code in this chapter always uses widths above 1. A full library would treat width 1 as a special case.

### Gradients of any size

In Chapter 8 our gradient had to be **256** wide, so that x could be used as a byte directly. In Chapter 9, Practice 7, a 512-wide gradient needed `x / 2`. Now we can do **any** width:

> width 300: t = x ÷ 299, then lerp from 0 to 255.
> x = 299 → t = 1 → 255 ✓
> x = 150 → t = 150 ÷ 299 ≈ 0.5017 → 0 + 255 × 0.5017 = 127.93 → **128**

🧠 **Remember:** **t = x ÷ (width − 1)**, computed as `double`. Then `lerpColour(start, end, t)`.

---

## 13.6 Directions

The direction of a gradient depends on **what t is made from**.

| Direction | t |
|---|---|
| left → right | x ÷ (width − 1) |
| top → bottom | y ÷ (height − 1) |
| right → left | 1 − x ÷ (width − 1) |
| diagonal, top-left → bottom-right | (x + y) ÷ ((width − 1) + (height − 1)) |

🔢 **Maths: the diagonal t at the corners of a 5 × 3 image**

> (width − 1) + (height − 1) = 4 + 2 = 6
> top-left (0, 0): (0 + 0) ÷ 6 = **0**
> bottom-right (4, 2): (4 + 2) ÷ 6 = **1**
> top-right (4, 0): 4 ÷ 6 ≈ **0.67**
> bottom-left (0, 2): 2 ÷ 6 ≈ **0.33**

### A speed trick for vertical gradients

In a top-to-bottom gradient, **every pixel in a row has the same colour**. So we compute the colour **once per row**, not once per pixel. Our `sky` image does this: 300 lerps instead of 60,000.

---

## 13.7 Gradients with many colours

📖 **New word: colour stop** — one fixed colour in a gradient that has several colours.

A rainbow has **6 stops**: red, yellow, green, cyan, blue, magenta. Between each pair of neighbouring stops, we lerp. That gives **5 parts**.

```
t:      0      0.2     0.4     0.6     0.8     1.0
        red ── yellow ── green ── cyan ── blue ── magenta
        part 0  part 1   part 2   part 3   part 4
```

For a t from 0 to 1, we must find:
1. **Which part** we are in.
2. **How far** we are inside that part (a "local" t, from 0 to 1).

🔢 **Maths: the steps**

> parts = stops − 1 = 6 − 1 = 5
> scaled = t × parts           (now from 0 to 5)
> i = whole part of scaled     (the part number: 0, 1, 2, 3 or 4)
> local = scaled − i           (from 0 to 1, inside the part)
> colour = lerp(stops[i], stops[i + 1], local)

🔢 **Maths: t = 0.5**

> scaled = 0.5 × 5 = 2.5
> i = 2 (part 2: green → cyan)
> local = 2.5 − 2 = 0.5 (halfway between green and cyan)
> green = (0, 255, 0), cyan = (0, 255, 255)
> colour = (0, 255, lerp(0, 255, 0.5)) = (0, 255, 127.5 → **128**)

🔢 **Maths: t = 0.13**

> scaled = 0.13 × 5 = 0.65
> i = 0 (red → yellow), local = 0.65
> R: lerp(255, 255, 0.65) = 255
> G: lerp(0, 255, 0.65) = 165.75 → 166
> B: 0
> colour = **(255, 166, 0)** — an orange

### The ends

At t = 1: scaled = 5, i = 5, and `stops[i + 1]` = `stops[6]` does **not exist** (only 0 to 5)! So we handle the ends first: t ≤ 0 → the first stop, t ≥ 1 → the last stop.

---

## 13.8 Rounding correctly — even for negative numbers

In Chapter 5 we learned to round by adding 0.5 and cutting with `static_cast<int>`. For colours (always 0 or more) this is fine. But later we round **negative** numbers too: positions to the left of or above the image (Chapter 20 lines), maths coordinates (this chapter's graph), and more.

`static_cast<int>` cuts **toward zero**: it drops the decimals, so −1.9 becomes −1, not −2.

🔢 **Maths: rounding −2.4 with "add 0.5, then cut"**

> −2.4 + 0.5 = −1.9
> cut toward zero → **−1** ✗ (wrong! −2.4 is closest to −2)

📖 **New word: floor** — the biggest whole number that is **not bigger** than the number. The floor always goes **down** the number line, even for negative numbers.

```
   −3      −2      −1       0       1       2       3
    |-------|-------|-------|-------|-------|-------|
             ↑ −1.9                    ↑ 1.9
   floor(−1.9) = −2               floor(1.9) = 1
```

| x | `static_cast<int>(x)` (cut toward zero) | `std::floor(x)` (always down) |
|---|---|---|
| 1.9 | 1 | 1 |
| −1.9 | −1 | **−2** |
| −2.1 | −2 | **−3** |
| 3.0 | 3 | 3 |

So the correct rounding rule is:

> **round(x) = floor(x + 0.5)**

🔢 **Maths: check four numbers**

> 2.4: floor(2.9) = **2** ✓
> 2.5: floor(3.0) = **3** ✓ (halfway rounds up)
> −2.4: floor(−1.9) = **−2** ✓
> −2.6: floor(−2.1) = **−3** ✓

`std::floor` comes from `<cmath>` (on our allowed list in Chapter 1). In this chapter's program, `roundToInt` does exactly this.

💡 **Tip:** `<cmath>` also has `std::round`. It rounds halves **away from zero** (−2.5 → −3), which is slightly different from floor(x + 0.5) (−2.5 → −2). Both are fine for images. We use `floor(x + 0.5)` because you can see exactly what it does.

🧠 **Remember:** For numbers that can be negative, round with **`std::floor(x + 0.5)`**, not `static_cast<int>(x + 0.5)`.

---

## 13.9 Inverse lerp and remap

📖 **New word: inverse lerp** — the opposite of lerp. Lerp turns **t into a value**. Inverse lerp turns **a value into t**.

> lerp: a, b, t → value
> inverse lerp: a, b, value → t

> **inverseLerp(a, b, v) = (v − a) ÷ (b − a)**

🔢 **Maths: where is 12.5 between 10 and 20?**

> (12.5 − 10) ÷ (20 − 10) = 2.5 ÷ 10 = **0.25** ✓ (the opposite of Section 13.1)

Look: `t = x ÷ (width − 1)` from Section 13.5 **is** an inverse lerp, with a = 0 and b = width − 1:

> inverseLerp(0, width − 1, x) = (x − 0) ÷ (width − 1 − 0) = x ÷ (width − 1) ✓

📖 **New word: remap** — moving a number from one range into another.

Remap = inverse lerp (find t in the first range), then lerp (use t in the second range):

> **remap(v, inMin, inMax, outMin, outMax) = lerp(outMin, outMax, inverseLerp(inMin, inMax, v))**

🔢 **Maths: a temperature of 25 °C, from the range 0–40, into a colour value 0–255**

> t = (25 − 0) ÷ (40 − 0) = 0.625
> value = 0 + (255 − 0) × 0.625 = 159.375 → **159**

🔢 **Maths: pixel column 150 in a 201-wide image, into maths x from −1 to 1**

> t = 150 ÷ 200 = 0.75
> maths x = −1 + (1 − (−1)) × 0.75 = −1 + 2 × 0.75 = −1 + 1.5 = **0.5**

Remap is how we connect **pixels** with **maths**. We use it for graphs (next section), fractals (Chapter 60), and cameras (Chapter 65).

---

## 13.10 Drawing the graph of a function

Let us draw the graph of **y = x²** for x from −1 to 1. It is a U-shaped curve called a **parabola**.

The problem: pixels and maths use **different coordinates**.

| | Pixels | Maths |
|---|---|---|
| across | column 0 to 200 | x from −1 to 1 |
| up/down | row 0 (top) to 200 (bottom), **y down** | y from −1 to 1, **y up** |

So for each pixel column:

1. **Remap** the column into maths x.
2. Compute maths y = x².
3. **Remap** maths y into a "maths-style row" (0 at the bottom, 200 at the top).
4. **Flip** it into an image row with **(h − 1) − row** (Chapter 3, Section 3.4).
5. **Round** with `floor(v + 0.5)` and set the pixel.

🔢 **Maths: column 150**

> 1. maths x = remap(150, 0, 200, −1, 1) = **0.5** (Section 13.9)
> 2. maths y = 0.5 × 0.5 = **0.25**
> 3. row = remap(0.25, −1, 1, 0, 200): t = (0.25 + 1) ÷ 2 = 0.625 → 0 + 200 × 0.625 = **125**
> 4. image row = (201 − 1) − 125 = **75**
> 5. set pixel (150, 75)

🔢 **Maths: column 100 (the middle)**

> maths x = remap(100, 0, 200, −1, 1) = −1 + 2 × 0.5 = **0**
> maths y = 0
> row = remap(0, −1, 1, 0, 200) = **100**
> image row = 200 − 100 = **100** → pixel (100, 100), the centre ✓

We use an image **201** wide (not 200) on purpose: then maths 0 lands **exactly** on column 100 and row 100, where we draw the grey axes.

⚠️ **Careful:** We set **one** pixel per column. Where the curve is steep (near the left and right edges), the points are far apart vertically, and you see **gaps**. Chapter 20 teaches line drawing, which fills them.

---

## Code, part 1: the new part of `image.h`

Add this code to `common/image.h`, **after** `loadPPM` and **before** the final `#endif`. The line numbers are the real ones in the finished file.

```cpp
inline double lerp(double a, double b, double t) {
    return a + (b - a) * t;
}

inline std::uint8_t lerpByte(std::uint8_t a, std::uint8_t b, double t) {
    double v = lerp(a, b, t);
    if (v < 0.0) {
        v = 0.0;
    }
    if (v > 255.0) {
        v = 255.0;
    }
    return static_cast<std::uint8_t>(v + 0.5);
}

inline Colour lerpColour(Colour a, Colour b, double t) {
    return Colour{lerpByte(a.r, b.r, t), lerpByte(a.g, b.g, t), lerpByte(a.b, b.b, t)};
}
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 215 | `inline double lerp(double a, double b, double t) {` | Linear interpolation of two numbers. `inline`, because it is a free function in a header (Chapter 12, Section 12.9). |
| 216 | `return a + (b - a) * t;` | The formula from Section 13.2. |
| 217 | `}` | End of `lerp`. |
| 219 | `inline std::uint8_t lerpByte(std::uint8_t a, std::uint8_t b, double t) {` | Lerp for one colour channel: two bytes in, one byte out. |
| 220 | `double v = lerp(a, b, t);` | Do the lerp in `double`. The bytes `a` and `b` are turned into `double` automatically. |
| 221–223 | `if (v < 0.0) { v = 0.0; }` | If t was below 0, v could be negative. Limit it to 0 (Section 13.3). |
| 224–226 | `if (v > 255.0) { v = 255.0; }` | If t was above 1, v could be above 255. Limit it to 255. |
| 227 | `return static_cast<std::uint8_t>(v + 0.5);` | Round and store as a byte. Here v is never negative, so "add 0.5 and cut" is correct (Section 13.8). |
| 228 | `}` | End of `lerpByte`. |
| 230 | `inline Colour lerpColour(Colour a, Colour b, double t) {` | Lerp between two colours. |
| 231 | `return Colour{lerpByte(a.r, b.r, t), lerpByte(a.g, b.g, t), lerpByte(a.b, b.b, t)};` | Lerp each channel with the **same** t (Section 13.4), and build the new colour. |
| 232 | `}` | End of `lerpColour`. |

The final `#endif` is now on line 234.

⚠️ **Careful:** C++20 added a function called `std::lerp` in `<cmath>`. It lives inside `std::`, so it does **not** clash with our `lerp`. But if you ever write `using namespace std;`, the two names collide. This is one more reason why this book never writes `using namespace std;`.

---

## Code, part 2: four gradients

File: `ch13/gradients.cpp`

```cpp
#include <cmath>
#include <iostream>
#include <vector>
#include "image.h"

double inverseLerp(double a, double b, double v) {
    return (v - a) / (b - a);
}

double remap(double v, double inMin, double inMax, double outMin, double outMax) {
    return lerp(outMin, outMax, inverseLerp(inMin, inMax, v));
}

int roundToInt(double v) {
    return static_cast<int>(std::floor(v + 0.5));
}

Colour multiStop(const std::vector<Colour>& stops, double t) {
    if (t <= 0.0) {
        return stops.front();
    }
    if (t >= 1.0) {
        return stops.back();
    }
    double scaled = t * static_cast<double>(stops.size() - 1);
    int i = static_cast<int>(scaled);
    double local = scaled - i;
    return lerpColour(stops[i], stops[i + 1], local);
}

void printColour(const std::string& label, Colour c) {
    std::cout << label << " = (" << static_cast<int>(c.r) << ", "
              << static_cast<int>(c.g) << ", " << static_cast<int>(c.b) << ")\n";
}

int main() {
    Image across(300, 60);
    for (int y = 0; y < across.height(); ++y) {
        for (int x = 0; x < across.width(); ++x) {
            double t = static_cast<double>(x) / (across.width() - 1);
            across.setPixel(x, y, lerpColour(colours::red, colours::blue, t));
        }
    }

    Image sky(200, 300);
    const Colour night{10, 20, 80};
    const Colour sunset{255, 150, 50};
    for (int y = 0; y < sky.height(); ++y) {
        double t = static_cast<double>(y) / (sky.height() - 1);
        Colour c = lerpColour(night, sunset, t);
        for (int x = 0; x < sky.width(); ++x) {
            sky.setPixel(x, y, c);
        }
    }

    Image rainbow(360, 40);
    const std::vector<Colour> stops = {colours::red, colours::yellow, colours::green,
                                       colours::cyan, colours::blue, colours::magenta};
    for (int y = 0; y < rainbow.height(); ++y) {
        for (int x = 0; x < rainbow.width(); ++x) {
            double t = static_cast<double>(x) / (rainbow.width() - 1);
            rainbow.setPixel(x, y, multiStop(stops, t));
        }
    }

    Image graph(201, 201, colours::white);
    const Colour grey{200, 200, 200};
    for (int i = 0; i < 201; ++i) {
        graph.setPixel(i, 100, grey);
        graph.setPixel(100, i, grey);
    }
    for (int px = 0; px < graph.width(); ++px) {
        double mathsX = remap(px, 0, graph.width() - 1, -1.0, 1.0);
        double mathsY = mathsX * mathsX;
        double row = remap(mathsY, -1.0, 1.0, 0, graph.height() - 1);
        int py = (graph.height() - 1) - roundToInt(row);
        graph.setPixel(px, py, colours::red);
    }

    bool ok = across.savePPM("across.ppm");
    ok = ok && sky.savePPM("sky.ppm");
    ok = ok && rainbow.savePPM("rainbow.ppm");
    ok = ok && graph.savePPM("graph.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }

    printColour("red to blue at t = 0.25", lerpColour(colours::red, colours::blue, 0.25));
    printColour("across (150, 0)", across.getPixel(150, 0));
    printColour("rainbow (359, 0)", rainbow.getPixel(359, 0));
    std::cout << "graph: maths x = 0.5 is drawn at row "
              << (graph.height() - 1) - roundToInt(remap(0.25, -1.0, 1.0, 0, 200)) << "\n";

    const double tests[] = {2.4, 2.5, -2.4, -2.6};
    for (double v : tests) {
        std::cout << v << ": cut gives " << static_cast<int>(v + 0.5)
                  << ", floor gives " << roundToInt(v) << "\n";
    }
    return 0;
}
```

### Line by line

**Helper functions (lines 1–34)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1 | `#include <cmath>` | For `std::floor` (Section 13.8). |
| 2 | `#include <iostream>` | Printing. |
| 3 | `#include <vector>` | A list of colour stops. |
| 4 | `#include "image.h"` | Our library, now with `lerp` and `lerpColour`. |
| 6 | `double inverseLerp(double a, double b, double v) {` | Given a value `v` between `a` and `b`, find its t (Section 13.9). |
| 7 | `return (v - a) / (b - a);` | How far `v` is from `a`, divided by the whole distance. |
| 8 | `}` | End of `inverseLerp`. |
| 10 | `double remap(double v, double inMin, double inMax, double outMin, double outMax) {` | Move `v` from the range inMin–inMax into the range outMin–outMax. |
| 11 | `return lerp(outMin, outMax, inverseLerp(inMin, inMax, v));` | First find t in the old range, then use t in the new range. |
| 12 | `}` | End of `remap`. |
| 14 | `int roundToInt(double v) {` | Round to the nearest whole number — correct for negative numbers too. |
| 15 | `return static_cast<int>(std::floor(v + 0.5));` | Add 0.5, then go **down** to a whole number (Section 13.8). `std::floor` gives a `double` like −2.0, so we still cast it to `int`; that cast is now safe, because there are no decimals left to cut. |
| 16 | `}` | End of `roundToInt`. |
| 18 | `Colour multiStop(const std::vector<Colour>& stops, double t) {` | A gradient with many colour stops (Section 13.7). |
| 19–21 | `if (t <= 0.0) { return stops.front(); }` | At (or before) the start: the first stop. |
| 22–24 | `if (t >= 1.0) { return stops.back(); }` | At (or after) the end: the last stop. This also stops us from reading `stops[i + 1]` past the end. |
| 25 | `double scaled = t * static_cast<double>(stops.size() - 1);` | Stretch t from 0–1 to 0–(number of parts). With 6 stops: 0 to 5. |
| 26 | `int i = static_cast<int>(scaled);` | The part number: the whole-number part of `scaled`. Here `scaled` is never negative, so cutting is fine. |
| 27 | `double local = scaled - i;` | How far we are inside this part, from 0 to 1. |
| 28 | `return lerpColour(stops[i], stops[i + 1], local);` | Lerp between the two stops around us. |
| 29 | `}` | End of `multiStop`. |
| 31–34 | `void printColour(...) { ... }` | Print a label and a colour as numbers (as in Chapter 11). |

**Four images (lines 36–78)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 36 | `int main() {` | The program starts here. |
| 37 | `Image across(300, 60);` | A 300 × 60 image. 300 is **not** 256 — that is the point. |
| 38–39 | `for (int y ...) { for (int x ...) {` | Every pixel. |
| 40 | `double t = static_cast<double>(x) / (across.width() - 1);` | t from 0 (left) to 1 (right), with `width − 1` and a `double` division (Section 13.5). |
| 41 | `across.setPixel(x, y, lerpColour(colours::red, colours::blue, t));` | Lerp from red to blue. |
| 42–43 | `}` `}` | End of the loops. |
| 45 | `Image sky(200, 300);` | A tall image for a vertical gradient. |
| 46 | `const Colour night{10, 20, 80};` | A dark night blue for the top. |
| 47 | `const Colour sunset{255, 150, 50};` | A warm orange for the bottom. |
| 48 | `for (int y = 0; y < sky.height(); ++y) {` | For each row… |
| 49 | `double t = static_cast<double>(y) / (sky.height() - 1);` | …t from 0 (top) to 1 (bottom), using **y** and **height**. |
| 50 | `Colour c = lerpColour(night, sunset, t);` | One colour for the whole row: computed **once** (Section 13.6). |
| 51–53 | `for (int x ...) { sky.setPixel(x, y, c); }` | Paint the whole row with it. |
| 54 | `}` | End of the rows. |
| 56 | `Image rainbow(360, 40);` | A wide, short image. |
| 57–58 | `const std::vector<Colour> stops = {colours::red, ...};` | The 6 colour stops of the rainbow. |
| 59–60 | `for (int y ...) { for (int x ...) {` | Every pixel. |
| 61 | `double t = static_cast<double>(x) / (rainbow.width() - 1);` | t from left to right. |
| 62 | `rainbow.setPixel(x, y, multiStop(stops, t));` | The multi-stop colour at t. |
| 63–64 | `}` `}` | End of the loops. |
| 66 | `Image graph(201, 201, colours::white);` | A white 201 × 201 image for the graph (Section 13.10). |
| 67 | `const Colour grey{200, 200, 200};` | A light grey for the axes. |
| 68 | `for (int i = 0; i < 201; ++i) {` | 201 steps, one for each pixel along an axis. |
| 69 | `graph.setPixel(i, 100, grey);` | The x axis: row 100, where maths y = 0. |
| 70 | `graph.setPixel(100, i, grey);` | The y axis: column 100, where maths x = 0. |
| 71 | `}` | End of the axes. |
| 72 | `for (int px = 0; px < graph.width(); ++px) {` | For each pixel column… |
| 73 | `double mathsX = remap(px, 0, graph.width() - 1, -1.0, 1.0);` | …step 1: column → maths x. |
| 74 | `double mathsY = mathsX * mathsX;` | Step 2: the function y = x². |
| 75 | `double row = remap(mathsY, -1.0, 1.0, 0, graph.height() - 1);` | Step 3: maths y → a "maths-style" row, 0 at the bottom. |
| 76 | `int py = (graph.height() - 1) - roundToInt(row);` | Steps 4 and 5: round, then **flip** so up is up (Chapter 3). |
| 77 | `graph.setPixel(px, py, colours::red);` | Draw the point. If it were outside, `setPixel` would ignore it. |
| 78 | `}` | End of the columns. |

**Saving and checking (lines 80–101)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 80–87 | `bool ok = across.savePPM(...); ... if (!ok) { ... return 1; }` | Save all four images, and stop if any save fails. |
| 89 | `printColour("red to blue at t = 0.25", lerpColour(...));` | Check Section 13.4: should be (191, 0, 64). |
| 90 | `printColour("across (150, 0)", across.getPixel(150, 0));` | A pixel in the middle of the 300-wide gradient. |
| 91 | `printColour("rainbow (359, 0)", rainbow.getPixel(359, 0));` | The last rainbow pixel: t = 1, so the last stop, magenta. |
| 92–93 | `std::cout << "graph: maths x = 0.5 is drawn at row " << ...` | Repeat the Section 13.10 calculation for x = 0.5 (y = 0.25): it should be row 75. |
| 95 | `const double tests[] = {2.4, 2.5, -2.4, -2.6};` | Four numbers to round (Section 13.8). |
| 96 | `for (double v : tests) {` | For each one… |
| 97–98 | `std::cout << v << ": cut gives " << static_cast<int>(v + 0.5) << ", floor gives " << roundToInt(v) << "\n";` | …print the result of both rounding methods, side by side. |
| 99 | `}` | End of the loop. |
| 100 | `return 0;` | The program finished with no problem. |
| 101 | `}` | End of `main`. |

### What you should see

```
red to blue at t = 0.25 = (191, 0, 64)
across (150, 0) = (127, 0, 128)
rainbow (359, 0) = (255, 0, 255)
graph: maths x = 0.5 is drawn at row 75
2.4: cut gives 2, floor gives 2
2.5: cut gives 3, floor gives 3
-2.4: cut gives -1, floor gives -2
-2.6: cut gives -2, floor gives -3
```

🔢 **Maths: check `across (150, 0)`**

> t = 150 ÷ 299 ≈ 0.50167
> R: 255 + (0 − 255) × 0.50167 = 255 − 127.93 = 127.07 → **127**
> B: 0 + 255 × 0.50167 = 127.93 → **128**

So the middle is (127, 0, 128). Not exactly (127.5, 0, 127.5), because 300 pixels have no single middle pixel: pixel 150 is a little **past** the middle (the middle is 149.5).

The last two lines show the rounding bug from Section 13.8: "cut" gives −1 and −2, which are **wrong**. "floor" gives −2 and −3, which are right.

Open the images:
- `across.ppm`: red on the left, through purple, to blue on the right.
- `sky.ppm`: dark night blue at the top, fading into orange at the bottom, like a sunset.
- `rainbow.ppm`: red, yellow, green, cyan, blue, magenta, all smoothly joined.
- `graph.ppm`: white, with grey axes and a red U-shaped curve. It touches the centre, and reaches the top corners. Near the corners you see gaps (Section 13.10).

---

## Small examples

### Example 1 — A three-colour flag gradient

Use `multiStop` with 3 stops: `{colours::red, colours::white, colours::blue}`.

> parts = 2. t = 0.25 → scaled = 0.5 → i = 0, local = 0.5 → halfway red→white = (255, 128, 128), a pink.
> t = 0.75 → scaled = 1.5 → i = 1, local = 0.5 → halfway white→blue = (128, 128, 255), a light blue.

### Example 2 — A diagonal gradient

```cpp
Image diag(200, 100);
for (int y = 0; y < diag.height(); ++y) {
    for (int x = 0; x < diag.width(); ++x) {
        double t = static_cast<double>(x + y) / ((diag.width() - 1) + (diag.height() - 1));
        diag.setPixel(x, y, lerpColour(colours::yellow, colours::magenta, t));
    }
}
```

> (width − 1) + (height − 1) = 199 + 99 = 298
> pixel (100, 50): t = 150 ÷ 298 ≈ 0.503 → about halfway → R 255, G lerp(255, 0, 0.503) = 126.7 → 127, B lerp(0, 255, 0.503) = 128.3 → 128 → **(255, 127, 128)**.

### Example 3 — A middle row of the sky

> y = 150, t = 150 ÷ 299 ≈ 0.5017
> R: 10 + (255 − 10) × 0.5017 = 10 + 122.9 = 132.9 → **133**
> G: 20 + (150 − 20) × 0.5017 = 20 + 65.2 = 85.2 → **85**
> B: 80 + (50 − 80) × 0.5017 = 80 − 15.05 = 64.95 → **65**

Blue goes **down** from 80 to 50, because `b − a` is negative for that channel. Each channel can go up or down on its own.

### Example 4 — Remap backwards

Remap also works when the output range is "backwards":

> remap(0.25, 0, 1, 255, 0) = lerp(255, 0, 0.25) = 255 − 63.75 = **191.25**

So "0 to 1" became "255 to 0". This is how we will **invert** brightness in Chapter 47.

---

## Common mistakes

⚠️ **`t = x / width`.** The last pixel never reaches t = 1. Use `width − 1`.

⚠️ **Integer division.** `x / (width - 1)` with two `int`s is 0 for almost every pixel. Cast to `double` first.

⚠️ **Cutting instead of rounding.** Gradients get slightly too dark. Use + 0.5 (for positive values) or `floor(v + 0.5)` (for any value).

⚠️ **Rounding negatives with a cast.** `static_cast<int>(-2.4 + 0.5)` is −1, not −2. Use `std::floor`.

⚠️ **Reading `stops[i + 1]` at t = 1.** It is one past the end. Handle the ends first.

⚠️ **Forgetting the y flip in graphs.** The curve comes out upside down: a ∩ instead of a U.

⚠️ **Writing `using namespace std;`.** Our `lerp` would clash with C++20's `std::lerp`.

---

## Practice

🏋️ **1.** Work out lerp(40, 100, 0.3) and lerp(100, 40, 0.3). Are they the same?

🏋️ **2.** Lerp the colours (0, 0, 0) and (200, 100, 50) at t = 0.6. Round each channel.

🏋️ **3.** An image is 11 pixels wide. What is t for x = 0, 5 and 10? What would it be for x = 10 if you used `width` instead of `width − 1`?

🏋️ **4.** Work out inverseLerp(50, 250, 100) and remap(100, 50, 250, 0, 1000).

🏋️ **5.** Round these with floor(x + 0.5): 7.49, 7.5, −0.4, −0.5, −0.6.

🏋️ **6.** In the rainbow (6 stops), which part and which local t belong to t = 0.9? What colour is it?

🏋️ **7.** Make a **radial** gradient: a 200 × 200 image where t is the distance from the centre (100, 100) divided by 100, going from white in the middle to dark blue at the edge. (Hint: Chapter 3 distance, `std::sqrt`; if t > 1, `lerpColour` clamps it.)

🏋️ **8.** Change the graph to draw **y = x³** instead of x². Which way does it go?

---

## Answers

**1.**
> lerp(40, 100, 0.3) = 40 + 60 × 0.3 = 40 + 18 = **58**
> lerp(100, 40, 0.3) = 100 + (−60) × 0.3 = 100 − 18 = **82**

They are **not** the same. Swapping a and b is the same as using 1 − t: lerp(40, 100, 0.7) = 40 + 42 = 82 ✓.

**2.**
> R: 0 + 200 × 0.6 = **120**
> G: 0 + 100 × 0.6 = **60**
> B: 0 + 50 × 0.6 = **30**
> result **(120, 60, 30)** — lerping from black is the same as "darker" from Chapter 5, Section 5.7.

**3.**
> width − 1 = 10
> x = 0: 0 ÷ 10 = **0**
> x = 5: 5 ÷ 10 = **0.5** (with an odd width, there **is** a middle pixel)
> x = 10: 10 ÷ 10 = **1**
> with `width`: 10 ÷ 11 ≈ **0.909** — the end colour never appears.

**4.**
> inverseLerp(50, 250, 100) = (100 − 50) ÷ (250 − 50) = 50 ÷ 200 = **0.25**
> remap(100, 50, 250, 0, 1000) = lerp(0, 1000, 0.25) = **250**

**5.**
> 7.49 → floor(7.99) = **7**
> 7.5 → floor(8.0) = **8**
> −0.4 → floor(0.1) = **0**
> −0.5 → floor(0.0) = **0**
> −0.6 → floor(−0.1) = **−1**

**6.**
> scaled = 0.9 × 5 = 4.5
> i = 4 (blue → magenta), local = 0.5
> blue = (0, 0, 255), magenta = (255, 0, 255)
> R: lerp(0, 255, 0.5) = 127.5 → 128
> colour = **(128, 0, 255)** — a violet

**7.**

```cpp
Image radial(200, 200);
const Colour darkBlue{0, 0, 60};
for (int y = 0; y < radial.height(); ++y) {
    for (int x = 0; x < radial.width(); ++x) {
        double dx = (x + 0.5) - 100.0;
        double dy = (y + 0.5) - 100.0;
        double t = std::sqrt(dx * dx + dy * dy) / 100.0;
        radial.setPixel(x, y, lerpColour(colours::white, darkBlue, t));
    }
}
radial.savePPM("radial.ppm");
```

We use pixel **centres** (Chapter 3). In the corners, the distance is about 141 (√(100² + 100²)), so t ≈ 1.41. `lerpByte` clamps each channel, and the corners are exactly dark blue. You see a soft glowing white circle.

**8.** Change line 74 to:

```cpp
double mathsY = mathsX * mathsX * mathsX;
```

> x = −1 → y = −1 (bottom-left), x = 0 → y = 0 (centre), x = 1 → y = 1 (top-right)
> x = 0.5 → y = 0.125, x = −0.5 → y = −0.125

The curve goes from the **bottom-left**, flattens through the centre, and rises to the **top-right**: an "S" lying on its side. (Without the y flip, it would go from top-left to bottom-right instead.)

---

## Summary

🧠 **lerp(a, b, t) = a + (b − a) × t.** t = 0 → a, t = 1 → b. t outside 0–1 goes past the ends.

🧠 Lerp colours **channel by channel**, with the same t. Then clamp to 0–255 and **round**.

🧠 For pixel x: **t = x ÷ (width − 1)**, as a `double`. 5 pixels have 4 gaps.

🧠 The **direction** of a gradient is set by what t is made from: x, y, x + y, distance…

🧠 Many stops: scaled = t × (stops − 1), i = whole part, local = scaled − i. Handle the ends first.

🧠 Round with **`std::floor(x + 0.5)`** when x can be negative.

🧠 **inverseLerp(a, b, v) = (v − a) ÷ (b − a).** **remap = lerp(out range, inverseLerp(in range, v))**.

🧠 Graphs: remap pixel → maths, compute, remap maths → row, **flip y**, round.

---

## Next chapter

`lerpByte` quietly **clamped** values to 0–255. In Chapter 14 we look at colours as **vectors**: we add, subtract and scale them, see what goes wrong when the numbers get too big (overflow), and learn to **clamp** properly with `std::clamp`.
