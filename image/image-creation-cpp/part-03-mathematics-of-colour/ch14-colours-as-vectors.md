# Chapter 14 — Colours as Vectors: Add, Scale, Clamp

> **Part 3 · Chapter 14 of 82**
> **You need:** Chapters 1–13 · **You will make:** `colourf.h` (a colour type for maths), `lights.ppm` (three coloured lights mixing) and `overflow.ppm` (wrap-around vs. clamping, side by side)

---

## What you will learn

- What a **vector** is, and why a colour is one.
- How to **add**, **subtract** and **scale** colours, channel by channel.
- How to **multiply two colours** — and why that is how coloured light and coloured objects work.
- Exactly what goes wrong when a value is too big: **overflow** and **wrap-around**.
- How to **clamp** with `std::min`, `std::max` and `std::clamp`.
- A new type, **`ColourF`**: colours as `double`s from 0.0 to 1.0, for all our maths.
- The **length** of a colour vector, and the distance between two colours.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **vector** | A small list of numbers that we treat as one thing, like (R, G, B) or (x, y). |
| **component** | One number inside a vector. R, G and B are the components of a colour. |
| **component-wise** | Doing the same thing to each component on its own. |
| **scalar** | A single plain number (not a vector), like 0.5. |
| **scaling** | Multiplying every component of a vector by the same scalar. |
| **overflow** | When a result is too big for its type. |
| **clamp** | To limit a value so it stays between a smallest and a biggest value. |
| **saturate** | To reach the top limit of a value (255, or 1.0) and stay there. |
| **filter** | Something that lets some light through and blocks the rest, like coloured glass. |
| **operator overloading** | Telling C++ what `+`, `−`, `*` mean for our own type. |

---

## 14.1 What is a vector?

📖 **New word: vector** — a small list of numbers that we treat as **one thing**.

📖 **New word: component** — one number inside a vector.

You have already met vectors in this book, without the name:

| Vector | Components | Chapter |
|---|---|---|
| a position (x, y) | 2 | 3 |
| a colour (R, G, B) | 3 | 5 |
| the offset of a neighbour (+1, 0) | 2 | 3 |

⚠️ **Careful:** this "vector" is a **maths** idea. It is not the same as `std::vector` in C++, which is a list of any length. A maths vector usually has 2, 3 or 4 components. (The names are related: both are "a list of numbers in order".)

In Chapter 5 we pictured a colour as a **point** in the RGB cube. We can also picture it as an **arrow** from black (0, 0, 0) to that point:

```
          blue
           ↑
           |      ● (R, G, B)
           |    ↗
           |  ↗
           |↗
 black ────●─────────→ red
          /
         ↙
     green
```

Thinking of colours as arrows lets us use simple **vector maths** on them. All the operations in this chapter work on the components one at a time.

📖 **New word: component-wise** — doing the same thing to each component on its own.

---

## 14.2 Adding colours

To add two colours, add each pair of components:

> (R₁, G₁, B₁) + (R₂, G₂, B₂) = (R₁ + R₂, G₁ + G₂, B₁ + B₂)

What does adding colours **mean**? It is **adding light** — two lamps shining on the same spot (Chapter 5, Section 5.1).

🔢 **Maths: red light + green light**

> (255, 0, 0) + (0, 255, 0) = (255 + 0, 0 + 255, 0 + 0) = **(255, 255, 0)** = yellow ✓

That is exactly the additive mixing rule from Chapter 5.

🔢 **Maths: two dim lights**

> (100, 50, 0) + (60, 60, 60) = **(160, 110, 60)**

Two lights together are brighter than either one alone.

### When the sum is too big

> (200, 100, 0) + (100, 100, 100) = **(300, 200, 100)**

300 is **bigger than 255**. A byte cannot hold it. This is the main problem of this chapter (Sections 14.6 and 14.7).

---

## 14.3 Subtracting colours

> (R₁, G₁, B₁) − (R₂, G₂, B₂) = (R₁ − R₂, G₁ − G₂, B₁ − B₂)

Subtraction gives the **difference** between two colours: "how do I get from colour 2 to colour 1?"

🔢 **Maths: orange − red**

> (255, 128, 0) − (255, 0, 0) = **(0, 128, 0)**

So orange is red **plus** 128 of green. That matches Chapter 5, Section 5.4.

🔢 **Maths: red − blue**

> (255, 0, 0) − (0, 0, 255) = **(255, 0, −255)**

A **negative** component! That is not a colour you can show. But it is a perfectly good **difference**, and we need it: in lerp, `b − a` can be negative (Chapter 13), and the distance between colours uses differences (Section 14.9).

🧠 **Remember:** A difference of two colours may be negative. We may **compute** with it, but before we **store** a colour, every component must be between 0 and 255.

---

## 14.4 Scaling a colour

📖 **New word: scalar** — a single plain number, like 0.5 or 2. (It "scales" things.)

📖 **New word: scaling** — multiplying every component by the same scalar.

> (R, G, B) × s = (R × s, G × s, B × s)

Scaling changes the **brightness** but keeps the **hue** (the "kind" of colour). In the cube, the arrow keeps its direction and only gets longer or shorter.

🔢 **Maths: orange × 0.5**

> (255, 128, 0) × 0.5 = (127.5, 64, 0) → rounded **(128, 64, 0)** — a darker orange (brown)

This is "darker" from Chapter 5, Section 5.7.

🔢 **Maths: orange × 2**

> (255, 128, 0) × 2 = **(510, 256, 0)** — too big again!

| s | Meaning |
|---|---|
| 0 | black |
| between 0 and 1 | darker |
| 1 | no change |
| above 1 | brighter — and it may go past 255 |

### Lerp is adding and scaling

Look at lerp from Chapter 13 again:

> lerp(a, b, t) = a + (b − a) × t

It is made of exactly the operations of this chapter: a **subtraction** (b − a), a **scaling** (× t) and an **addition** (a + …). This is why lerp works on colours: it is just vector maths.

---

## 14.5 Multiplying two colours

Adding is "two lights together". What is multiplying?

📖 **New word: filter** — something that lets some light through and blocks the rest, like coloured glass.

Think of **white light passing through cyan glass**. Cyan glass lets green and blue through, and blocks red. Each channel is **multiplied** by how much the glass lets through:

| | R | G | B |
|---|---|---|---|
| white light | 1.0 | 1.0 | 1.0 |
| cyan glass lets through | 0.0 | 1.0 | 1.0 |
| light that comes out | 1.0 × 0.0 = **0** | 1.0 × 1.0 = **1** | 1.0 × 1.0 = **1** |

The result is cyan light ✓.

This only works with values from **0.0 to 1.0** (Chapter 5, Section 5.9). With bytes, 255 × 255 = 65,025 — nonsense. With 0–1 values, 1.0 × 1.0 = 1.0 (full stays full) and 0.5 × 0.5 = 0.25 (dims more).

> (R₁, G₁, B₁) × (R₂, G₂, B₂) = (R₁ × R₂, G₁ × G₂, B₁ × B₂) — **component-wise**, with 0.0–1.0 values

### Why objects have colour

The same multiplication explains how **objects** look. A blue ball **reflects** blue light and absorbs red and green. Its colour (0, 0, 1) is a "filter" for the light that hits it.

🔢 **Maths: orange light on blue paint**

> orange light ≈ (1.0, 0.5, 0.0)
> blue paint = (0.0, 0.0, 1.0)
> what we see = (1.0 × 0.0, 0.5 × 0.0, 0.0 × 1.0) = **(0, 0, 0)** — black!

The orange light has **no blue** in it, and the blue paint reflects **only blue**. Nothing comes back. In real life, a blue object under an orange street light looks almost black. We use exactly this multiplication for lighting in Chapters 68 and 73.

| Multiply by | Result |
|---|---|
| white (1, 1, 1) | no change |
| black (0, 0, 0) | black |
| grey (0.5, 0.5, 0.5) | half as bright (the same as × 0.5) |

---

## 14.6 Overflow: what really happens

📖 **New word: overflow** — when a result is too big for its type.

In Chapter 4 we saw that a byte **wraps around**: 250 + 10 = 4. Let us look closer at what C++ does.

```cpp
std::uint8_t a = 200;
std::uint8_t b = 100;
int sum = a + b;
```

**Step 1: C++ makes them `int` first.** Before any arithmetic, C++ turns small types like `std::uint8_t` into `int`. This is called **integer promotion**. So `a + b` is `200 + 100` in **`int`**, which is **300**. Nothing is lost yet.

**Step 2: the damage happens when we store.** If we store 300 back into a byte, only the lowest 8 bits are kept:

🔢 **Maths: 300 into a byte**

> 300 in binary = `1 0010 1100` (9 bits: 256 + 32 + 8 + 4 = 300)
> keep the lowest 8 bits: `0010 1100` = 32 + 8 + 4 = **44**
> (same as 300 − 256 = 44)

So a bright pixel (300 should be "very bright") becomes **44** (quite dark). In a picture, this shows as **dark bands** where the image should be brightest. This chapter's `overflow.ppm` shows it.

⚠️ **Careful:** With **signed** `int`, going past 2,147,483,647 is **undefined behaviour** (Chapter 12, Section 12.5). It is not a safe wrap-around. With colours this rarely happens, because 255 + 255 = 510 is tiny for an `int`. But it can happen with big **products**, like width × height × 3 for a huge image.

🧠 **Remember:** Byte maths happens in `int`, so it is safe. The problem is **storing** a result above 255 (or below 0) back into a byte. Always limit it first.

---

## 14.7 Clamping

📖 **New word: clamp** — to limit a value so it stays between a smallest and a biggest value.

📖 **New word: saturate** — to reach the top limit and stay there. A clamped pixel at 255 is "saturated".

🔢 **Maths: the rule for clamping v between lo and hi**

> if v < lo → use lo
> if v > hi → use hi
> otherwise → use v

| v | clamp(v, 0, 255) |
|---|---|
| −20 | 0 |
| 0 | 0 |
| 128 | 128 |
| 255 | 255 |
| 300 | 255 |

```
         lo                    hi
  ───────●━━━━━━━━━━━━━━━━━━━━━●───────
  v here → moved to lo         v here → moved to hi
```

### Three ways in C++ (all from `<algorithm>`)

| Code | Meaning |
|---|---|
| `std::min(v, 255)` | the smaller of the two: stops values **above** 255 |
| `std::max(v, 0)` | the bigger of the two: stops values **below** 0 |
| `std::clamp(v, 0, 255)` | both at once (C++17) |

`std::clamp(v, lo, hi)` is the same as `std::min(std::max(v, lo), hi)`.

⚠️ **Careful:** For `std::min`, `std::max` and `std::clamp`, all the values must have the **same type**. `std::min(a + b, 255)` works, because `a + b` is an `int` and `255` is an `int`. But `std::clamp(v, 0, 1)` with a `double` v does **not** compile — write `std::clamp(v, 0.0, 1.0)`.

### Wrap or clamp: a picture

🔢 **Maths: making a gradient 100 brighter**

For each x from 0 to 255, the brighter value is x + 100.

| x | x + 100 | wrapped into a byte | clamped |
|---|---|---|---|
| 0 | 100 | 100 | 100 |
| 155 | 255 | 255 | 255 |
| 156 | 256 | **0** | 255 |
| 200 | 300 | **44** | 255 |
| 255 | 355 | **99** | 255 |

With wrap-around, the picture goes up to white at x = 155, then **jumps to black** at x = 156, and climbs again. With clamping, it goes up to white and **stays** white. The top half of `overflow.ppm` shows the wrong way; the bottom half shows the right way.

🧠 **Remember:** Before storing into a byte, **clamp** to 0–255. Before converting a 0.0–1.0 value, clamp to 0.0–1.0.

---

## 14.8 `ColourF`: a colour type for maths

Doing maths with `Colour` (bytes) is clumsy: every step needs casts, and every step risks overflow. So we add a second colour type, for **maths only**:

```cpp
struct ColourF {
    double r = 0.0;
    double g = 0.0;
    double b = 0.0;
};
```

- The `F` stands for "floating point" (`double`).
- Normal values are **0.0 to 1.0** (Chapter 5, Section 5.9).
- **During** maths, values may go above 1 or below 0. That is fine: a `double` holds them easily.
- Only at the very **end**, we convert back to a `Colour`, and **then** we clamp and round.

```
Colour ──toColourF──► ColourF ──(add, scale, multiply...)──► ColourF ──toColour──► Colour
 bytes       ÷ 255     doubles        any values                       clamp, × 255, round    bytes
```

### Operator overloading

📖 **New word: operator overloading** — telling C++ what `+`, `−`, `*`, `/` mean for our own type.

You may already know this C++ feature. If you write a function named `operator+` that takes two `ColourF`s, then `a + b` calls it:

```cpp
inline ColourF operator+(ColourF a, ColourF b) {
    return ColourF{a.r + b.r, a.g + b.g, a.b + b.b};
}
```

Now we can write colour maths that looks like the maths on paper:

```cpp
ColourF c = a + (b - a) * t;   // lerp, written with real operators
```

We define:

| Operator | Meaning | Section |
|---|---|---|
| `a + b` | add two colours | 14.2 |
| `a - b` | subtract two colours | 14.3 |
| `a * s` and `s * a` | scale by a number | 14.4 |
| `a * b` | multiply two colours (filter) | 14.5 |
| `a / s` | divide by a number (for averages) | 14.9 |

### A new header: `colourf.h`

We put `ColourF` into a **new** header file, `common/colourf.h`, which includes `image.h`. Why not add it to `image.h`?

- It needs `<algorithm>` (for `std::clamp`) at the top. Adding a line at the top of `image.h` would move **every** line number used in Chapters 11–13.
- It is also good design: **one header per topic**. A program that only saves PPM files does not need colour maths.

From now on, a program that does colour maths writes `#include "colourf.h"`. That also brings in `image.h`, because `colourf.h` includes it. (The include guards from Chapter 11 make sure nothing is included twice.)

---

## 14.9 Averages and lengths

### The average of colours

To find the **average** of several colours: add them all, then divide by how many there are.

🔢 **Maths: the average of red, green and blue (as 0–1 values)**

> sum = (1, 0, 0) + (0, 1, 0) + (0, 0, 1) = (1, 1, 1)
> average = (1, 1, 1) ÷ 3 = (0.333, 0.333, 0.333)
> as bytes: 0.333 × 255 = 85 → **(85, 85, 85)**, a dark grey

The average of two colours is the same as lerp at t = 0.5:

> (a + b) ÷ 2 = a + (b − a) × 0.5 ✓

Averages are very important later: **smooth edges** (Chapter 27) and **blur** (Chapter 50) are both "the average of many colours".

### The length of a colour vector

The **length** of the arrow (R, G, B) uses Pythagoras in 3 directions (Chapter 3, Chapter 5 Section 5.6):

> length = √(R² + G² + B²)

The **distance** between two colours is the length of their **difference**:

> distance(a, b) = length(a − b)

🔢 **Maths: red to blue, with 0–1 values**

> red − blue = (1, 0, −1)
> length = √(1 + 0 + 1) = √2 ≈ **1.414**
> In byte units: 1.414 × 255 ≈ 360.6 — the same as Chapter 5, Section 5.6 ✓

---

## Code, part 1: `colourf.h`

File: `common/colourf.h`

```cpp
#ifndef COLOURF_H
#define COLOURF_H

#include <algorithm>
#include <cmath>
#include "image.h"

struct ColourF {
    double r = 0.0;
    double g = 0.0;
    double b = 0.0;
};

inline ColourF operator+(ColourF a, ColourF b) {
    return ColourF{a.r + b.r, a.g + b.g, a.b + b.b};
}

inline ColourF operator-(ColourF a, ColourF b) {
    return ColourF{a.r - b.r, a.g - b.g, a.b - b.b};
}

inline ColourF operator*(ColourF a, double s) {
    return ColourF{a.r * s, a.g * s, a.b * s};
}

inline ColourF operator*(double s, ColourF a) {
    return a * s;
}

inline ColourF operator*(ColourF a, ColourF b) {
    return ColourF{a.r * b.r, a.g * b.g, a.b * b.b};
}

inline ColourF operator/(ColourF a, double s) {
    return ColourF{a.r / s, a.g / s, a.b / s};
}

inline ColourF toColourF(Colour c) {
    return ColourF{c.r / 255.0, c.g / 255.0, c.b / 255.0};
}

inline std::uint8_t toByte(double v) {
    double clamped = std::clamp(v, 0.0, 1.0);
    return static_cast<std::uint8_t>(clamped * 255.0 + 0.5);
}

inline Colour toColour(ColourF c) {
    return Colour{toByte(c.r), toByte(c.g), toByte(c.b)};
}

inline double length(ColourF c) {
    return std::sqrt(c.r * c.r + c.g * c.g + c.b * c.b);
}

#endif
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef COLOURF_H` / `#define COLOURF_H` | The include guard, with its own name (Chapter 11, Section 11.4). |
| 4 | `#include <algorithm>` | For `std::clamp`. |
| 5 | `#include <cmath>` | For `std::sqrt`. |
| 6 | `#include "image.h"` | For `Colour`, `Image` and the rest. A program that includes `colourf.h` gets all of `image.h` too. |
| 8 | `struct ColourF {` | A colour for maths, with `double` components (Section 14.8). |
| 9–11 | `double r = 0.0;` … | Red, green, blue. Normally 0.0 to 1.0, but any value is allowed during maths. Default: black. |
| 12 | `};` | End of `ColourF`. |
| 14 | `inline ColourF operator+(ColourF a, ColourF b) {` | What `a + b` means for two `ColourF`s. `inline` because it is in a header (Chapter 12). The colours are passed **by value**: they are tiny (3 doubles), so copying is cheap. |
| 15 | `return ColourF{a.r + b.r, a.g + b.g, a.b + b.b};` | Add component-wise (Section 14.2). |
| 16 | `}` | End. |
| 18–20 | `inline ColourF operator-(ColourF a, ColourF b) { ... }` | What `a − b` means: subtract component-wise (Section 14.3). The result may be negative. |
| 22–24 | `inline ColourF operator*(ColourF a, double s) { ... }` | What `colour * number` means: scale every component (Section 14.4). |
| 26 | `inline ColourF operator*(double s, ColourF a) {` | What `number * colour` means. C++ treats `c * 0.5` and `0.5 * c` as two different things, so we need both. |
| 27 | `return a * s;` | Just use the one above. Scaling does not care about the order. |
| 28 | `}` | End. |
| 30–32 | `inline ColourF operator*(ColourF a, ColourF b) { ... }` | What `colour * colour` means: multiply component-wise — a **filter** (Section 14.5). |
| 34–36 | `inline ColourF operator/(ColourF a, double s) { ... }` | What `colour / number` means: divide every component. Used for averages (Section 14.9). |
| 38 | `inline ColourF toColourF(Colour c) {` | Turn a byte colour into a maths colour. |
| 39 | `return ColourF{c.r / 255.0, c.g / 255.0, c.b / 255.0};` | Divide each byte by 255.0 (with `.0`, so it is a `double` division). 0 → 0.0, 255 → 1.0. |
| 40 | `}` | End. |
| 42 | `inline std::uint8_t toByte(double v) {` | Turn one 0.0–1.0 value back into a byte, safely. |
| 43 | `double clamped = std::clamp(v, 0.0, 1.0);` | First **clamp** it to 0.0–1.0 (Section 14.7). Note `0.0` and `1.0`, so all three values are `double`. |
| 44 | `return static_cast<std::uint8_t>(clamped * 255.0 + 0.5);` | Then × 255, round (the value is not negative, so + 0.5 and cut is correct), and store as a byte. The result is always 0 to 255. |
| 45 | `}` | End. |
| 47 | `inline Colour toColour(ColourF c) {` | Turn a maths colour back into a byte colour. |
| 48 | `return Colour{toByte(c.r), toByte(c.g), toByte(c.b)};` | Convert each component with `toByte`. Every value is clamped, so nothing can wrap around. |
| 49 | `}` | End. |
| 51 | `inline double length(ColourF c) {` | The length of the colour arrow (Section 14.9). |
| 52 | `return std::sqrt(c.r * c.r + c.g * c.g + c.b * c.b);` | Pythagoras in 3 directions. |
| 53 | `}` | End. |
| 55 | `#endif` | End of the include guard. |

---

## Code, part 2: lights and overflow

File: `ch14/colour_maths.cpp`

```cpp
#include <algorithm>
#include <cstdint>
#include <iostream>
#include "colourf.h"

void printColour(const std::string& label, Colour c) {
    std::cout << label << " = (" << static_cast<int>(c.r) << ", "
              << static_cast<int>(c.g) << ", " << static_cast<int>(c.b) << ")\n";
}

bool insideCircle(int x, int y, double cx, double cy, double radius) {
    double dx = (x + 0.5) - cx;
    double dy = (y + 0.5) - cy;
    return dx * dx + dy * dy <= radius * radius;
}

int main() {
    std::uint8_t a = 200;
    std::uint8_t b = 100;
    int sum = a + b;
    std::uint8_t wrapped = static_cast<std::uint8_t>(a + b);
    std::uint8_t clamped = static_cast<std::uint8_t>(std::min(a + b, 255));
    std::cout << "200 + 100 as int:  " << sum << "\n";
    std::cout << "stored in a byte:  " << static_cast<int>(wrapped) << "\n";
    std::cout << "clamped to 255:    " << static_cast<int>(clamped) << "\n";
    std::cout << "clamp(-20) = " << std::clamp(-20, 0, 255)
              << ", clamp(300) = " << std::clamp(300, 0, 255)
              << ", clamp(128) = " << std::clamp(128, 0, 255) << "\n\n";

    const ColourF red = toColourF(colours::red);
    const ColourF green = toColourF(colours::green);
    const ColourF blue = toColourF(colours::blue);
    const ColourF orange = toColourF(Colour{255, 128, 0});

    printColour("red + green", toColour(red + green));
    printColour("orange * 0.5", toColour(orange * 0.5));
    printColour("white light through cyan glass",
                toColour(toColourF(colours::white) * toColourF(colours::cyan)));
    printColour("orange light on blue paint", toColour(orange * blue));
    std::cout << "distance from red to blue = " << length(red - blue) << "\n";

    Image lights(300, 300);
    for (int y = 0; y < lights.height(); ++y) {
        for (int x = 0; x < lights.width(); ++x) {
            ColourF total;
            if (insideCircle(x, y, 150.0, 110.0, 75.0)) {
                total = total + red;
            }
            if (insideCircle(x, y, 110.0, 180.0, 75.0)) {
                total = total + green;
            }
            if (insideCircle(x, y, 190.0, 180.0, 75.0)) {
                total = total + blue;
            }
            lights.setPixel(x, y, toColour(total));
        }
    }

    Image overflow(256, 100);
    for (int y = 0; y < overflow.height(); ++y) {
        for (int x = 0; x < overflow.width(); ++x) {
            int brighter = x + 100;
            std::uint8_t v = 0;
            if (y < 50) {
                v = static_cast<std::uint8_t>(brighter);
            } else {
                v = static_cast<std::uint8_t>(std::clamp(brighter, 0, 255));
            }
            overflow.setPixel(x, y, Colour{v, v, v});
        }
    }

    bool ok = lights.savePPM("lights.ppm");
    ok = ok && overflow.savePPM("overflow.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    printColour("lights (150, 157)", lights.getPixel(150, 157));
    printColour("overflow (200, 10)", overflow.getPixel(200, 10));
    printColour("overflow (200, 60)", overflow.getPixel(200, 60));
    return 0;
}
```

### Line by line

**Helpers (lines 1–15)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1 | `#include <algorithm>` | `std::min` and `std::clamp`. (`colourf.h` includes it too, but a program should include what it uses itself.) |
| 2 | `#include <cstdint>` | `std::uint8_t`. |
| 3 | `#include <iostream>` | Printing. |
| 4 | `#include "colourf.h"` | `ColourF` and its operators — and, through it, `image.h`. |
| 6–9 | `void printColour(...) { ... }` | Print a label and a colour as numbers (as in Chapters 11 and 13). |
| 11 | `bool insideCircle(int x, int y, double cx, double cy, double radius) {` | Is pixel (x, y) inside a circle with centre (cx, cy)? |
| 12–13 | `double dx = (x + 0.5) - cx;` / `double dy = (y + 0.5) - cy;` | Distance from the circle centre to the **pixel centre** (Chapter 3, Section 3.9). |
| 14 | `return dx * dx + dy * dy <= radius * radius;` | Inside if the squared distance is at most radius² (Chapter 10, Section 10.6). |
| 15 | `}` | End. |

**Overflow and clamping with bytes (lines 17–28)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 17 | `int main() {` | The program starts here. |
| 18–19 | `std::uint8_t a = 200;` / `std::uint8_t b = 100;` | Two bytes. |
| 20 | `int sum = a + b;` | `a + b` is computed in `int` (integer promotion, Section 14.6): **300**. Stored in an `int`, so nothing is lost. |
| 21 | `std::uint8_t wrapped = static_cast<std::uint8_t>(a + b);` | Store 300 in a byte: it **wraps around** to 44. |
| 22 | `std::uint8_t clamped = static_cast<std::uint8_t>(std::min(a + b, 255));` | First take the smaller of 300 and 255 → 255. **Then** store. |
| 23–25 | `std::cout << ...` | Print all three results. |
| 26–28 | `std::cout << "clamp(-20) = " << std::clamp(-20, 0, 255) ...` | Show `std::clamp` on a value below, above, and inside the range. |

**Colour maths with `ColourF` (lines 30–40)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 30–32 | `const ColourF red = toColourF(colours::red);` … | Red, green and blue as maths colours: (1, 0, 0), (0, 1, 0), (0, 0, 1). |
| 33 | `const ColourF orange = toColourF(Colour{255, 128, 0});` | Orange: (1.0, 0.502, 0.0). |
| 35 | `printColour("red + green", toColour(red + green));` | Add two lights (Section 14.2). Expect yellow. |
| 36 | `printColour("orange * 0.5", toColour(orange * 0.5));` | Scale (Section 14.4). Expect (128, 64, 0). |
| 37–38 | `printColour("white light through cyan glass", toColour(... * ...));` | Multiply two colours (Section 14.5). Expect cyan. |
| 39 | `printColour("orange light on blue paint", toColour(orange * blue));` | Expect black. |
| 40 | `std::cout << "distance from red to blue = " << length(red - blue) << "\n";` | Subtract, then take the length (Section 14.9). Expect √2 ≈ 1.41421. |

**Three lights (lines 42–57)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 42 | `Image lights(300, 300);` | A black 300 × 300 image: a dark room. |
| 43–44 | `for (int y ...) { for (int x ...) {` | Every pixel. |
| 45 | `ColourF total;` | The light that reaches this pixel. It starts as (0, 0, 0): no light. |
| 46–48 | `if (insideCircle(x, y, 150.0, 110.0, 75.0)) { total = total + red; }` | If this pixel is in the circle of the **red** lamp (top middle), add red light. |
| 49–51 | `if (insideCircle(x, y, 110.0, 180.0, 75.0)) { total = total + green; }` | If it is in the **green** lamp's circle (bottom left), add green light. |
| 52–54 | `if (insideCircle(x, y, 190.0, 180.0, 75.0)) { total = total + blue; }` | If it is in the **blue** lamp's circle (bottom right), add blue light. |
| 55 | `lights.setPixel(x, y, toColour(total));` | Turn the total into a byte colour (with clamping) and store it. |
| 56–57 | `}` `}` | End of the loops. |

**Wrap vs. clamp (lines 59–71)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 59 | `Image overflow(256, 100);` | 256 wide, so x goes 0 to 255 (like Chapter 8's gradient). |
| 60–61 | `for (int y ...) { for (int x ...) {` | Every pixel. |
| 62 | `int brighter = x + 100;` | A grey gradient, made 100 brighter. In `int`, so values up to 355 are fine here. |
| 63 | `std::uint8_t v = 0;` | The byte we will store. |
| 64–65 | `if (y < 50) { v = static_cast<std::uint8_t>(brighter); }` | **Top half: the wrong way.** Store directly. Values above 255 wrap around. |
| 66–68 | `} else { v = static_cast<std::uint8_t>(std::clamp(brighter, 0, 255)); }` | **Bottom half: the right way.** Clamp first, then store. |
| 69 | `overflow.setPixel(x, y, Colour{v, v, v});` | A grey pixel (R = G = B). |
| 70–71 | `}` `}` | End of the loops. |

**Save and check (lines 73–83)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 73–78 | `bool ok = lights.savePPM(...); ... if (!ok) { ... return 1; }` | Save both images. |
| 79 | `printColour("lights (150, 157)", lights.getPixel(150, 157));` | A pixel where **all three** circles overlap. Expect white. |
| 80 | `printColour("overflow (200, 10)", overflow.getPixel(200, 10));` | Top half, x = 200: 300 wrapped → 44. |
| 81 | `printColour("overflow (200, 60)", overflow.getPixel(200, 60));` | Bottom half, x = 200: 300 clamped → 255. |
| 82 | `return 0;` | The program finished with no problem. |
| 83 | `}` | End of `main`. |

Compile:

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common colour_maths.cpp -o colour_maths
```

### What you should see

```
200 + 100 as int:  300
stored in a byte:  44
clamped to 255:    255
clamp(-20) = 0, clamp(300) = 255, clamp(128) = 128

red + green = (255, 255, 0)
orange * 0.5 = (128, 64, 0)
white light through cyan glass = (0, 255, 255)
orange light on blue paint = (0, 0, 0)
distance from red to blue = 1.41421
lights (150, 157) = (255, 255, 255)
overflow (200, 10) = (44, 44, 44)
overflow (200, 60) = (255, 255, 255)
```

🔢 **Maths: check that (150, 157) is inside all three circles**

The pixel centre is (150.5, 157.5). The radius² is 75 × 75 = 5,625.

> red lamp (150, 110): dx = 0.5, dy = 47.5 → 0.25 + 2,256.25 = 2,256.5 ≤ 5,625 ✓
> green lamp (110, 180): dx = 40.5, dy = −22.5 → 1,640.25 + 506.25 = 2,146.5 ≤ 5,625 ✓
> blue lamp (190, 180): dx = −39.5, dy = −22.5 → 1,560.25 + 506.25 = 2,066.5 ≤ 5,625 ✓

Inside all three → red + green + blue = **white** ✓.

Open `lights.ppm`. You see the famous picture of additive colour: three circles of red, green and blue light. Where two overlap: **yellow** (red + green), **magenta** (red + blue), **cyan** (green + blue). In the middle, where all three overlap: **white**. It is the triangle from Chapter 5, Section 5.3, made with real maths.

Open `overflow.ppm`. The **top** half rises to white, then suddenly drops to black at x = 156 and rises again. The **bottom** half rises to white and stays white. One `std::clamp` is the whole difference.

---

## Small examples

### Example 1 — Lerp with operators

With `ColourF`, lerp looks exactly like the formula:

```cpp
ColourF lerpF(ColourF a, ColourF b, double t) {
    return a + (b - a) * t;
}
```

> lerpF(red, blue, 0.25) = (1, 0, 0) + ((0, 0, 1) − (1, 0, 0)) × 0.25
> = (1, 0, 0) + (−1, 0, 1) × 0.25
> = (1, 0, 0) + (−0.25, 0, 0.25)
> = (0.75, 0, 0.25) → × 255 → (191.25, 0, 63.75) → **(191, 0, 64)** ✓ the same as Chapter 13

### Example 2 — A warm tint on a whole image

Multiply every pixel by a warm "filter" colour, like looking through orange-tinted glasses:

```cpp
const ColourF warm = toColourF(Colour{255, 220, 170});
for (int y = 0; y < img.height(); ++y) {
    for (int x = 0; x < img.width(); ++x) {
        ColourF c = toColourF(img.getPixel(x, y));
        img.setPixel(x, y, toColour(c * warm));
    }
}
```

> warm ≈ (1.0, 0.863, 0.667)
> white (1, 1, 1) × warm → (255, 220, 170), a cream colour
> blue (0, 0, 1) × warm → (0, 0, 170), a darker blue

Red stays full. Green is reduced a little, and blue more. The whole picture looks warmer.

### Example 3 — Brighten without overflow

To make an image 50% brighter: `c * 1.5`, then `toColour`.

> (200, 100, 50) → (0.784, 0.392, 0.196) × 1.5 = (1.176, 0.588, 0.294)
> toColour clamps 1.176 → 1.0
> → **(255, 150, 75)**

Red **saturates** at 255. Green and blue grow normally. No wrap-around.

### Example 4 — Average of four pixels

```cpp
ColourF sum = toColourF(Colour{255, 0, 0}) + toColourF(Colour{255, 0, 0})
            + toColourF(Colour{0, 0, 255}) + toColourF(Colour{255, 255, 255});
Colour average = toColour(sum / 4.0);
```

> sum = (1, 0, 0) + (1, 0, 0) + (0, 0, 1) + (1, 1, 1) = (3, 1, 2)
> ÷ 4 = (0.75, 0.25, 0.5)
> → **(191, 64, 128)**

The sum (3, 1, 2) is far above 1.0. That is no problem in `ColourF`: we only clamp at the very end.

---

## Common mistakes

⚠️ **Storing before clamping.** `static_cast<std::uint8_t>(300)` is 44. Clamp first.

⚠️ **Clamping in the middle of the maths.** In Example 4, if we clamped the sum (3, 1, 2) to (1, 1, 1) before dividing, the average would be wrong: (0.25, 0.25, 0.25). Clamp only at the **end**.

⚠️ **Multiplying byte colours.** 255 × 255 = 65,025. Multiply as 0.0–1.0 values (`ColourF`), never as bytes.

⚠️ **Mixing types in `std::clamp`.** `std::clamp(v, 0, 1)` with a `double` v does not compile. Use `0.0, 1.0`.

⚠️ **Forgetting `operator*(double, ColourF)`.** Then `0.5 * c` does not compile, even though `c * 0.5` does.

⚠️ **Confusing "maths vector" with `std::vector`.** A colour is a maths vector with 3 components. `std::vector` is a C++ container of any length.

---

## Practice

🏋️ **1.** Add (120, 200, 30) and (100, 80, 60). Which channels overflow? What is the clamped result?

🏋️ **2.** Work out (40, 200, 100) − (50, 100, 100). Which component is negative?

🏋️ **3.** A byte holds 30. We subtract 50 and store it back without clamping. What value does it hold? (Hint: Chapter 4, Practice 7.)

🏋️ **4.** Multiply the colours yellow (1, 1, 0) and magenta (1, 0, 1). What colour do you get? Explain it with "filters".

🏋️ **5.** Work out `std::clamp(1.3, 0.0, 1.0)`, `std::clamp(-0.2, 0.0, 1.0)` and `std::clamp(0.4, 0.0, 1.0)`.

🏋️ **6.** Change the `lights` program so each lamp has **half** strength (multiply each colour by 0.5 before adding). What colour is the middle now? What about where red and green overlap?

🏋️ **7.** What is the length of white (1, 1, 1)? Of grey (0.5, 0.5, 0.5)? Why is the second exactly half the first?

🏋️ **8.** Write a function `ColourF average(const std::vector<ColourF>& list)` that returns the average of any number of colours.

---

## Answers

**1.**
> (120 + 100, 200 + 80, 30 + 60) = (220, 280, 90)
> Green (280) overflows.
> Clamped: **(220, 255, 90)**
> (Without clamping, green would wrap to 280 − 256 = 24, and a light yellow-green would become a dark orange-brown.)

**2.**
> (40 − 50, 200 − 100, 100 − 100) = **(−10, 100, 0)**
> The **red** component is negative.

**3.**
> 30 − 50 = −20 (computed in `int`)
> Stored in a byte: −20 + 256 = **236**
> A dark pixel becomes almost white!

**4.**
> (1 × 1, 1 × 0, 0 × 1) = **(1, 0, 0)** = red
> Yellow glass lets red and green through. Magenta glass lets red and blue through. Through **both**, only the light that **both** let through survives: red.

**5.**
> clamp(1.3, 0.0, 1.0) = **1.0**
> clamp(−0.2, 0.0, 1.0) = **0.0**
> clamp(0.4, 0.0, 1.0) = **0.4**

**6.** Change lines 47, 50 and 53 to add `red * 0.5`, `green * 0.5` and `blue * 0.5`.

> middle: (0.5, 0.5, 0.5) → **(128, 128, 128)**, a middle grey
> red + green overlap: (0.5, 0.5, 0) → **(128, 128, 0)**, a dark yellow (olive)

**7.**
> white: √(1 + 1 + 1) = √3 ≈ **1.732**
> grey: √(0.25 + 0.25 + 0.25) = √0.75 ≈ **0.866**
> 0.866 = 1.732 ÷ 2. Grey is white × 0.5, and **scaling a vector by s scales its length by s** too. The arrow keeps its direction, and gets half as long (Section 14.4).

**8.**

```cpp
ColourF average(const std::vector<ColourF>& list) {
    if (list.empty()) {
        return ColourF{};
    }
    ColourF sum;
    for (const ColourF& c : list) {
        sum = sum + c;
    }
    return sum / static_cast<double>(list.size());
}
```

> We check for an empty list first: dividing by 0 would give "not a number" values.
> We add everything first, and divide **once** at the end.

---

## Summary

🧠 A **vector** is a small list of numbers treated as one thing. A colour (R, G, B) is a vector.

🧠 **Add** colours = add light. **Subtract** = the difference (may be negative). **Scale** = brighter or darker.

🧠 **Multiply** two colours (as 0.0–1.0 values) = a **filter**. This is how coloured glass, and coloured objects, work.

🧠 Byte maths happens in `int` (safe). The danger is **storing** a value outside 0–255: it **wraps around**.

🧠 **Clamp** before storing: `std::clamp(v, 0, 255)` or `std::clamp(v, 0.0, 1.0)`. Clamp only at the **end** of the maths.

🧠 **`ColourF`** (in `colourf.h`) holds `double` colours, with `+ − * /` operators. Convert with `toColourF` and `toColour`.

🧠 Average = sum ÷ count. Distance between colours = **length(a − b)**.

---

## Next chapter

How do you turn a colour photo into a **grey** one? Taking the plain average (R + G + B) ÷ 3 looks wrong — green looks too dark, and blue too bright. In Chapter 15 we learn why our eyes see some colours as brighter than others, and the **luminance** formula that fixes it. Then we save our results as real grey **PGM** files.
