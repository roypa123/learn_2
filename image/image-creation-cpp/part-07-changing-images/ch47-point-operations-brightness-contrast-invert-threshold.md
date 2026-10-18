# Chapter 47 — Point Operations: Brightness, Contrast, Invert, Threshold

> **Part 7 · Chapter 47 of 82**
> **You need:** Chapters 1–46 (especially 4, 13, 15, 17 and 46) · **You will make:** `pointops.h` (lookup tables for brightness, contrast, invert, threshold, gamma, exposure and levels; applying and combining them; drawing them as curves), `operations.png` (one picture, nine ways) and `curves.png` (the eight curves)

---

## What you will learn

- What a **point operation** is: a change that looks at one value at a time.
- How to see any point operation as a **curve** from "old value" to "new value".
- Why a **lookup table** of 256 entries makes them fast and simple.
- Brightness, contrast, invert, threshold, gamma, exposure and levels — each with its maths.
- Why **clamping** (not wrap-around) is right for pictures, and how operations **lose** information.
- Why the **order** of two operations matters.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **image processing** | Changing a picture that already exists. |
| **point operation** | A change where each new value depends only on the same pixel's old value. |
| **transfer curve** | The graph of a point operation: old value across, new value up. |
| **lookup table** | A list of 256 answers, one for every possible old value. |
| **contrast** | How far apart the dark and light parts of a picture are. |
| **threshold** | A level: values below it become black, values above it white. |
| **clipping** | Many different values all ending as 0 or 255, so the difference between them is lost. |

---

## 47.1 Changing pictures

Parts 4 and 5 **made** pictures. Part 7 **changes** them.

📖 **New word: image processing** — taking a picture that exists (a drawing, a loaded PNG, a photo) and changing it: lighter, sharper, softer, black-and-white…

We start with the simplest kind of change.

📖 **New word: point operation** — a change where the **new** value of a pixel depends **only** on the **old** value of the **same** pixel. Not on its neighbours, not on its position.

```
   old picture             new picture
   ┌─────────────┐         ┌─────────────┐
   │      v      │  ───▶   │    f(v)     │      the same rule f for every pixel
   └─────────────┘         └─────────────┘
```

We apply the rule to each colour channel separately: red, green and blue each go through the rule. (Chapter 49 will start using neighbours.)

---

## 47.2 Point operations as curves

A point operation is a **function**: a rule that turns each number 0–255 into another number 0–255. Like any function, we can draw its **graph**.

📖 **New word: transfer curve** — the graph of a point operation: the **old** value along the bottom (0 to 255), the **new** value up the side (0 to 255).

```
   new                         new                         new
   255 ┤        ╱              255 ┤    ╱───               255 ┤╲
       │      ╱                    │   ╱                       │  ╲
       │    ╱                      │  ╱                        │    ╲
       │  ╱                        │ ╱                         │      ╲
     0 ┼╱──────── old            0 ┼╱──────── old            0 ┼────────╲ old
       0       255                 0       255                 0       255
     "do nothing"              "brighter" (clamped)          "invert"
```

- The diagonal **new = old** changes nothing. We call it the **identity**.
- A curve **above** the diagonal makes the picture **lighter**; **below** makes it **darker**.
- A **steep** curve stretches small differences into big ones: **more contrast**. A **flat** curve squeezes them: **less contrast**.
- A curve that goes **down** reverses light and dark.

🧠 **Remember:** if you can draw the curve, you understand the operation. The program draws all eight curves of this chapter into `curves.png`.

---

## 47.3 Lookup tables

A byte has only **256** possible values. So instead of computing the rule for every pixel, we compute it **once for each possible value**, and keep the answers in a list.

📖 **New word: lookup table** — a list of 256 answers: entry v is the new value for the old value v.

```cpp
using LookupTable = std::array<std::uint8_t, 256>;
```

To apply it, each pixel just **looks up** its answer:

> new red = table[old red], new green = table[old green], new blue = table[old blue]

🔢 **Maths: how much work does a table save?**

> a 1920 × 1080 photo: 1920 × 1080 × 3 = **6,220,800** channel values
> gamma without a table: 6,220,800 calls of `std::pow`
> gamma with a table: **256** calls of `std::pow`, then 6,220,800 quick lookups

Tables have two more good points: every operation, however complicated, is applied the **same** way (`applyTable`), and two tables can be **combined** into one (Section 47.10).

💡 You have used this idea before: Chapter 17's `linearTable` holds the 256 linear values of the sRGB bytes.

---

## 47.4 Brightness

The simplest change: add the same amount to every value.

> **new = old + amount**, then **clamp** to 0 … 255

🔢 **Maths: brightness +40**

> 0 → **40**, 50 → **90**, 100 → **140**, 200 → **240**
> 230 → 270 → too big → **255**; and every value from 215 up gives 255

The curve is the diagonal moved **up** by 40, flattened at the top where it hits 255.

### Clamping, not wrap-around

Chapter 4 warned that a byte **wraps around**: 230 + 40 stored in a byte gives 270 − 256 = **14** — a very bright pixel would suddenly become almost black. For pictures, that is always wrong. So we do the sum in a `double`, then **clamp** it (Chapter 13):

```
230 + 40 with clamping: 255, with wrap-around: 14
```

Our helper `clampByte(v)` clamps to 0 … 255 and rounds to the nearest whole number.

📖 **New word: clipping** — after brightness +40, the values 215, 216, … 255 **all** become 255. They were 41 different values; now they are one. The details in the brightest parts of the picture (a cloud's shape, say) are **gone**, and darkening the picture again will not bring them back. This loss is called **clipping**. Every operation whose curve has a flat part clips.

---

## 47.5 Contrast

📖 **New word: contrast** — how far apart the dark and the light parts of a picture are. Low contrast looks grey and foggy; high contrast looks bold.

To raise the contrast, push every value **away from the middle**:

> **new = (old − 128) × factor + 128**, then clamp

- factor > 1: values move away from 128 → **more** contrast (a steeper curve)
- factor < 1: values move towards 128 → **less** contrast (a flatter curve)
- 128 itself never moves: it is the **centre** of the change

🔢 **Maths: contrast × 1.5**

> 50: (50 − 128) × 1.5 + 128 = −117 + 128 = **11**
> 100: (100 − 128) × 1.5 + 128 = −42 + 128 = **86**
> 128: 0 × 1.5 + 128 = **128**
> 200: 72 × 1.5 + 128 = **236**
> 0: −192 + 128 = −64 → clamp → **0** (clipped); 255: 318.5 → **255** (clipped)

💡 For a picture that is mostly dark, 128 is a poor centre: everything moves **down**. `contrastTable` lets you choose the centre — for example, the average value of the picture (Chapter 48 shows how to find it).

---

## 47.6 Invert

> **new = 255 − old**

Black becomes white, white becomes black, and every colour becomes its **opposite** (Chapter 5): red (255, 0, 0) becomes cyan (0, 255, 255). This is the "negative" that Chapter 12 already made, and Chapter 13's Example 4 noticed that it is a **remap backwards**: the value runs from 255 down to 0 as the old value runs up.

🔢 **Maths: invert twice**

> 255 − (255 − v) = v

Inverting twice gives the picture back **exactly**: no clipping, nothing lost. The program checks this by combining the table with itself (Section 47.10):

```
invert twice is the identity: yes
```

---

## 47.7 Threshold

📖 **New word: threshold** — a level. Every value **below** it becomes 0, every value **at or above** it becomes 255:

> **new = 255 if old ≥ level, otherwise 0**

The curve is a **step**: flat at 0, a jump at the level, flat at 255. Only 2 values are left, so a threshold clips almost everything — on purpose. It turns a picture into pure black and white, like a stamp or a stencil.

⚠️ On a **colour** picture, a threshold works on each channel separately, so every pixel becomes one of the 8 corner colours of the RGB cube (Chapter 5): a poster-like effect. For black and white, first make the picture **grey** (Chapter 15's `toGrey`), then threshold. The program does exactly that for its "threshold 128" picture.

🔢 **Maths: a threshold at 128**

> 0, 50, 100 → **0**; 128, 200, 255 → **255**

💡 Chapter 52 (dithering) will make black-and-white pictures that keep the **shading** too — a threshold alone cannot.

---

## 47.8 Gamma and exposure

Brightness **adds**. That lifts black (0 becomes 40), which makes the darks look grey and washed out. Often we want to brighten the picture while keeping black **black** and white **white**. Two better tools:

### Gamma

> **new = 255 × (old / 255) ^ γ**

Divide by 255 to get a number from 0 to 1. Raise it to the power γ (the Greek letter "gamma"). Multiply by 255 again. Since 0^γ = 0 and 1^γ = 1, black and white **stay where they are**; only the middle bends.

- γ < 1: the curve bulges **up**: lighter, especially the darks
- γ > 1: the curve sags **down**: darker

🔢 **Maths: gamma 0.5 and 2.0**

> γ = 0.5 (the square root): 100 → 255 × √(100 / 255) = 255 × 0.6262 = 159.7 → **160**
> γ = 2.0 (the square): 100 → 255 × (0.3922)² = 255 × 0.1538 = 39.2 → **39**
> 128 → **181** (γ = 0.5) and 64.25 → **64** (γ = 2.0)

This is the same kind of curve as Chapter 17's sRGB gamma — that was a "standard" gamma for storing light; here we use it as a **tool**.

### Exposure

Chapter 17 taught that sRGB bytes are not amounts of **light**. To make a picture really "twice as bright", like a camera that lets in twice the light, we should **multiply the light**:

> 1. turn the byte into linear light (Chapter 17's `srgbToLinear`)
> 2. multiply by the factor
> 3. turn it back into a byte (`linearToSrgb`, which also clamps)

Photographers call this **exposure**; doubling the light is "one stop" brighter.

🔢 **Maths: exposure × 2 for the value 50**

> 50 / 255 = 0.196 → linear light **0.0319** (Chapter 17)
> × 2 = **0.0638**
> back to sRGB: 1.055 × 0.0638^(1 / 2.4) − 0.055 = **0.280** → × 255 = 71.5 → **71**

So doubling the light turns 50 into 71, not 100. In linear light, "twice as bright" is a much gentler change for dark values than "add 50". Black stays 0 (0 × 2 = 0), but exposure **clips** the top: every value from **188** up becomes 255.

---

## 47.9 Levels

Many photos never use the full range: their darkest pixel is maybe 50, their brightest 200. **Levels** stretches a chosen range to the full 0 … 255:

> **new = (old − low) × 255 / (high − low)**, then clamp

🔢 **Maths: levels 50 … 200**

> 50 → **0**; 200 → **255**; 100 → 50 × 255 / 150 = **85**; 128 → 78 × 1.7 = 132.6 → **133**
> below 50 → 0, above 200 → 255 (clipped — but if the picture had no values there, nothing is lost)

Levels is a contrast change whose centre and factor are chosen from **two values of the picture**. Chapter 48 will choose them automatically from the picture's histogram.

---

## 47.10 Combining operations

Applying table A and then table B is the same as applying **one** combined table:

> combined[v] = B[A[v]]

So a whole chain of point operations costs **one** lookup per value. But be careful:

⚠️ **The order matters.** "Brighter, then more contrast" is not "more contrast, then brighter":

🔢 **Maths: the value 100**

> brightness +40, then contrast × 1.5: 100 → 140 → (140 − 128) × 1.5 + 128 = **146**
> contrast × 1.5, then brightness +40: 100 → 86 → 86 + 40 = **126**

```
100: brightness then contrast = 146, contrast then brightness = 126
```

In maths words: function composition is not commutative — like the matrices of Chapter 33, where "rotate then move" was not "move then rotate".

And clipping adds up: once a value has been clipped to 255, no later operation can tell it apart from its neighbours again.

---

## 47.11 The table of all eight operations

The program prints what each table does to six input values, and the **average** of each table (the average output for a picture that uses all 256 values equally):

```
input:              0   50  100  128  200  255   average
brightness +40     40   90  140  168  240  255   164.297
contrast x1.5       0   11   86  128  236  255   127.5
invert            255  205  155  127   55    0   127.5
threshold 128       0    0    0  255  255  255   127.5
gamma 0.5           0  113  160  181  226  255   169.805
gamma 2.0           0   10   39   64  157  255   85.1484
exposure x2         0   71  138  176  255  255   162.766
levels 50-200       0    0   85  133  255  255   130.02
```

Read it like this: contrast, invert and threshold keep the average at 127.5 (they move values symmetrically around the middle); brightness, gamma 0.5 and exposure raise it; gamma 2.0 lowers it.

🔢 **Maths: how many values survive?**

> invert: all **256** different outputs (nothing lost)
> brightness +40: 216 (215 … 255 merge into one)
> contrast × 1.5: 172
> levels 50–200: 151
> threshold: **2**

---

## Code, part 1: `pointops.h`

File: `common/pointops.h` (new). It includes `font.h` (the end of the drawing chain, Chapter 46) and `grey.h` (Chapter 15, which is not in that chain).

```cpp
#ifndef POINTOPS_H
#define POINTOPS_H

#include <array>
#include <cmath>
#include <cstdint>
#include "font.h"
#include "grey.h"

using LookupTable = std::array<std::uint8_t, 256>;

inline std::uint8_t clampByte(double v) {
    if (v <= 0.0) {
        return 0;
    }
    if (v >= 255.0) {
        return 255;
    }
    return static_cast<std::uint8_t>(v + 0.5);
}

inline LookupTable identityTable() {
    LookupTable t{};
    for (int v = 0; v < 256; ++v) {
        t[v] = static_cast<std::uint8_t>(v);
    }
    return t;
}

inline LookupTable brightnessTable(int amount) {
    LookupTable t{};
    for (int v = 0; v < 256; ++v) {
        t[v] = clampByte(v + amount);
    }
    return t;
}

inline LookupTable contrastTable(double factor, double centre = 128.0) {
    LookupTable t{};
    for (int v = 0; v < 256; ++v) {
        t[v] = clampByte((v - centre) * factor + centre);
    }
    return t;
}

inline LookupTable invertTable() {
    LookupTable t{};
    for (int v = 0; v < 256; ++v) {
        t[v] = static_cast<std::uint8_t>(255 - v);
    }
    return t;
}

inline LookupTable thresholdTable(int level) {
    LookupTable t{};
    for (int v = 0; v < 256; ++v) {
        t[v] = (v >= level) ? 255 : 0;
    }
    return t;
}

inline LookupTable gammaTable(double gamma) {
    LookupTable t{};
    for (int v = 0; v < 256; ++v) {
        t[v] = clampByte(255.0 * std::pow(v / 255.0, gamma));
    }
    return t;
}

inline LookupTable exposureTable(double factor) {
    LookupTable t{};
    for (int v = 0; v < 256; ++v) {
        t[v] = clampByte(255.0 * linearToSrgb(srgbToLinear(v / 255.0) * factor));
    }
    return t;
}

inline LookupTable levelsTable(int low, int high) {
    if (high <= low) {
        high = low + 1;
    }
    LookupTable t{};
    for (int v = 0; v < 256; ++v) {
        t[v] = clampByte((v - low) * 255.0 / (high - low));
    }
    return t;
}

inline LookupTable combineTables(const LookupTable& first, const LookupTable& second) {
    LookupTable t{};
    for (int v = 0; v < 256; ++v) {
        t[v] = second[first[v]];
    }
    return t;
}

inline void applyTables(Image& image, const LookupTable& red, const LookupTable& green,
                        const LookupTable& blue) {
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            const Colour c = image.getPixel(x, y);
            image.setPixel(x, y, Colour{red[c.r], green[c.g], blue[c.b]});
        }
    }
}

inline void applyTable(Image& image, const LookupTable& t) {
    applyTables(image, t, t, t);
}

inline void makeGrey(Image& image) {
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            image.setPixel(x, y, toGrey(image.getPixel(x, y)));
        }
    }
}

inline double tableAverage(const LookupTable& t) {
    double sum = 0.0;
    for (std::uint8_t v : t) {
        sum += v;
    }
    return sum / 256.0;
}

inline void drawCurve(Image& image, int x, int y, int size, const LookupTable& t, Colour c) {
    strokeRect(image, makeRect(x, y, size + 1, size + 1), 1, Colour{170, 170, 170});
    drawLine(image, x, y + size, x + size, y, Colour{225, 225, 225});
    for (int v = 0; v < 255; ++v) {
        const int x0 = x + v * size / 255;
        const int y0 = y + size - t[v] * size / 255;
        const int x1 = x + (v + 1) * size / 255;
        const int y1 = y + size - t[v + 1] * size / 255;
        drawLine(image, x0, y0, x1, y1, c);
    }
}

#endif
```

### Line by line

**Tables and clamping (lines 1–28)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–8 | include guard and `#include` lines | `std::array`, `std::pow`, exact-size integers, the drawing library with fonts, and the grey functions. |
| 10 | `using LookupTable = std::array<std::uint8_t, 256>;` | A short name for "256 bytes" (Section 47.3). `using` gives a type a new name, like `Bytes` in Chapter 36. |
| 12–20 | `inline std::uint8_t clampByte(double v) { if (v <= 0.0) { return 0; } if (v >= 255.0) { return 255; } return static_cast<std::uint8_t>(v + 0.5); }` | Clamp to 0 … 255 and round to the nearest whole number (Section 47.4). |
| 22–28 | `inline LookupTable identityTable() { LookupTable t{}; for (int v = 0; v < 256; ++v) { t[v] = static_cast<std::uint8_t>(v); } return t; }` | The "do nothing" table: entry v is v. `LookupTable t{};` starts with all zeros. |

**The operations (lines 30–87)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 30–36 | `inline LookupTable brightnessTable(int amount) { ... t[v] = clampByte(v + amount); ... }` | Section 47.4. The sum is an `int`, then turned into a `double` for `clampByte` — no wrap-around. |
| 38–44 | `inline LookupTable contrastTable(double factor, double centre = 128.0) { ... t[v] = clampByte((v - centre) * factor + centre); ... }` | Section 47.5, with a centre you may choose. |
| 46–52 | `inline LookupTable invertTable() { ... t[v] = static_cast<std::uint8_t>(255 - v); ... }` | Section 47.6. Never outside 0 … 255, so no clamp is needed. |
| 54–60 | `inline LookupTable thresholdTable(int level) { ... t[v] = (v >= level) ? 255 : 0; ... }` | Section 47.7. |
| 62–68 | `inline LookupTable gammaTable(double gamma) { ... t[v] = clampByte(255.0 * std::pow(v / 255.0, gamma)); ... }` | Section 47.8. `v / 255.0` is a `double` division (the `.0` matters: `v / 255` would be 0 for every v below 255). |
| 70–76 | `inline LookupTable exposureTable(double factor) { ... t[v] = clampByte(255.0 * linearToSrgb(srgbToLinear(v / 255.0) * factor)); ... }` | Section 47.8: to linear light, multiply, back to sRGB (Chapter 17). |
| 78–87 | `inline LookupTable levelsTable(int low, int high) { if (high <= low) { high = low + 1; } ... t[v] = clampByte((v - low) * 255.0 / (high - low)); ... }` | Section 47.9. If `high` is not above `low`, we make it `low + 1` — a very steep levels, like a threshold — instead of dividing by 0. |

**Using tables (lines 89–125)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 89–95 | `inline LookupTable combineTables(const LookupTable& first, const LookupTable& second) { ... t[v] = second[first[v]]; ... }` | One table that does `first`, then `second` (Section 47.10). |
| 97–105 | `inline void applyTables(Image& image, const LookupTable& red, const LookupTable& green, const LookupTable& blue) { ... image.setPixel(x, y, Colour{red[c.r], green[c.g], blue[c.b]}); ... }` | A different table for each channel — useful for tinting (Practice 5). The channel value is the index. |
| 107–109 | `inline void applyTable(Image& image, const LookupTable& t) { applyTables(image, t, t, t); }` | The same table for all three channels. |
| 111–117 | `inline void makeGrey(Image& image) { ... image.setPixel(x, y, toGrey(image.getPixel(x, y))); ... }` | The whole picture in grey (Chapter 15) — before a threshold. |
| 119–125 | `inline double tableAverage(const LookupTable& t) { double sum = 0.0; for (std::uint8_t v : t) { sum += v; } return sum / 256.0; }` | The average of the 256 answers (Section 47.11). |

**Drawing a curve (lines 127–139)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 127–129 | `inline void drawCurve(Image& image, int x, int y, int size, const LookupTable& t, Colour c) { strokeRect(image, makeRect(x, y, size + 1, size + 1), 1, Colour{170, 170, 170}); drawLine(image, x, y + size, x + size, y, Colour{225, 225, 225});` | A grey frame (Chapter 19) and the light grey identity diagonal, from bottom-left to top-right. The graph is `size + 1` pixels so that both 0 and `size` fit. |
| 130–134 | `for (int v = 0; v < 255; ++v) { const int x0 = x + v * size / 255; const int y0 = y + size - t[v] * size / 255; ... }` | Map value v to a position across and its answer to a position **up** — our y goes down, so we subtract from the bottom edge (Chapter 3). |
| 135–139 | `drawLine(image, x0, y0, x1, y1, c); }` `}` `#endif` | Join neighbouring points with Bresenham lines (Chapter 21). A jump (the threshold) becomes a vertical line. |

---

## Code, part 2: one picture, nine ways

File: `ch47/pointops.cpp`

```cpp
#include <iostream>
#include <string>
#include <vector>
#include "pointops.h"
#include "deflate.h"

std::string padLeft(const std::string& text, int width) {
    std::string s = text;
    while (static_cast<int>(s.size()) < width) {
        s = " " + s;
    }
    return s;
}

Image makeScene() {
    Image scene(160, 110);
    for (int y = 0; y < 110; ++y) {
        const Colour c = lerpColour(Colour{70, 120, 190}, Colour{235, 190, 140}, y / 109.0);
        fillRect(scene, makeRect(0, y, 160, 1), c);
    }
    fillCircleAA(scene, 118.0, 38.0, 16.0, Colour{255, 230, 120});
    const std::vector<PointF> hills = {{0.0, 80.0},    {30.0, 62.0},   {65.0, 78.0}, {100.0, 58.0},
                                       {160.0, 84.0},  {160.0, 110.0}, {0.0, 110.0}};
    fillPolygonAA(scene, hills, Colour{60, 110, 60});
    fillRect(scene, makeRect(28, 70, 26, 22), Colour{200, 80, 60});
    fillPolygonAA(scene, {{24.0, 71.0}, {41.0, 56.0}, {58.0, 71.0}}, Colour{110, 50, 40});
    fillRect(scene, makeRect(37, 80, 8, 12), Colour{70, 45, 30});
    return scene;
}

void paste(Image& dest, const Image& src, int left, int top) {
    for (int y = 0; y < src.height(); ++y) {
        for (int x = 0; x < src.width(); ++x) {
            dest.setPixel(left + x, top + y, src.getPixel(x, y));
        }
    }
}

int main() {
    const std::string names[8] = {"brightness +40", "contrast x1.5", "invert",    "threshold 128",
                                  "gamma 0.5",      "gamma 2.0",     "exposure x2", "levels 50-200"};
    const LookupTable tables[8] = {brightnessTable(40), contrastTable(1.5), invertTable(),
                                   thresholdTable(128), gammaTable(0.5),     gammaTable(2.0),
                                   exposureTable(2.0),  levelsTable(50, 200)};
    const int samples[6] = {0, 50, 100, 128, 200, 255};

    std::cout << "input:          ";
    for (int v : samples) {
        std::cout << padLeft(std::to_string(v), 5);
    }
    std::cout << "   average\n";
    for (int i = 0; i < 8; ++i) {
        std::cout << names[i] << std::string(16 - names[i].size(), ' ');
        for (int v : samples) {
            std::cout << padLeft(std::to_string(tables[i][v]), 5);
        }
        std::cout << "   " << tableAverage(tables[i]) << "\n";
    }

    const int v = 230;
    std::cout << "\n230 + 40 with clamping: " << static_cast<int>(clampByte(v + 40))
              << ", with wrap-around: " << static_cast<int>(static_cast<std::uint8_t>(v + 40)) << "\n";
    const LookupTable brightThenContrast = combineTables(tables[0], tables[1]);
    const LookupTable contrastThenBright = combineTables(tables[1], tables[0]);
    std::cout << "100: brightness then contrast = " << static_cast<int>(brightThenContrast[100])
              << ", contrast then brightness = " << static_cast<int>(contrastThenBright[100]) << "\n";
    const LookupTable twice = combineTables(invertTable(), invertTable());
    std::cout << "invert twice is the identity: " << (twice == identityTable() ? "yes" : "no") << "\n";

    const Image scene = makeScene();
    Image sheet(3 * 170 + 10, 3 * 134 + 10, colours::white);
    for (int i = 0; i < 9; ++i) {
        Image tile = scene;
        std::string label = "original";
        if (i > 0) {
            if (i == 4) {
                makeGrey(tile);
            }
            applyTable(tile, tables[i - 1]);
            label = names[i - 1];
        }
        const int left = 10 + (i % 3) * 170;
        const int top = 10 + (i / 3) * 134;
        paste(sheet, tile, left, top);
        drawText(sheet, left, top + 114, label, colours::black);
    }

    Image curves(4 * 150 + 10, 2 * 160 + 10, colours::white);
    for (int i = 0; i < 8; ++i) {
        const int left = 20 + (i % 4) * 150;
        const int top = 10 + (i / 4) * 160;
        drawCurve(curves, left, top, 120, tables[i], Colour{200, 40, 40});
        drawText(curves, left, top + 128, names[i], colours::black);
    }

    if (!savePNGCompressed(sheet, "operations.png") || !savePNGCompressed(curves, "curves.png")) {
        std::cout << "could not write the files\n";
        return 1;
    }
    std::cout << "wrote operations.png and curves.png\n";
    return 0;
}
```

Build and run it from the `code/ch47` folder:

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common pointops.cpp -o pointops
./pointops
```

### Line by line

**Helpers (lines 1–37)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–5 | the `#include` lines | Printing, strings, lists, the new header, and `deflate.h` for `savePNGCompressed`. |
| 7–13 | `std::string padLeft(const std::string& text, int width) { ... }` | Spaces in front, for columns (Chapter 43). |
| 15–20 | `Image makeScene() { Image scene(160, 110); for (...) { ... lerpColour(...y / 109.0); fillRect(scene, makeRect(0, y, 160, 1), c); }` | A small test picture: a sky gradient, one row at a time. |
| 21–28 | `fillCircleAA(...)`, `fillPolygonAA(scene, hills, ...)`, `fillRect(...)` for the house, `fillPolygonAA(...)` for the roof, `fillRect(...)` for the door | A sun, green hills, and a house with a roof and a door — smooth edges from Chapter 27. |
| 31–37 | `void paste(Image& dest, const Image& src, int left, int top) { ... }` | Copy one picture into another at (left, top). |

**The table of values (lines 40–58)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 40–44 | `const std::string names[8] = {...}; const LookupTable tables[8] = {brightnessTable(40), ...};` | The eight operations, built once. |
| 45 | `const int samples[6] = {0, 50, 100, 128, 200, 255};` | The input values to show. |
| 47–51 | print the heading | |
| 52–58 | `for (...) { std::cout << names[i] << std::string(16 - names[i].size(), ' '); for (int v : samples) { ... tables[i][v] ... } std::cout << "   " << tableAverage(tables[i]) << "\n"; }` | One line per operation: its answers and its average (Section 47.11). |

**Clamping, order and invert (lines 60–68)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 60–62 | `const int v = 230; ... clampByte(v + 40) ... static_cast<std::uint8_t>(v + 40) ...` | Clamping gives 255; storing 270 in a byte wraps to 14 (Section 47.4). |
| 63–66 | `combineTables(tables[0], tables[1])` and `combineTables(tables[1], tables[0])` | Both orders of brightness and contrast (Section 47.10). |
| 67–68 | `const LookupTable twice = combineTables(invertTable(), invertTable()); ... (twice == identityTable() ? "yes" : "no") ...` | Two `std::array`s can be compared with `==`: all 256 entries must be equal. |

**The pictures (lines 70–102)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 70–71 | `const Image scene = makeScene(); Image sheet(3 * 170 + 10, 3 * 134 + 10, colours::white);` | A 3 × 3 grid of tiles: each 170 wide and 134 tall (110 for the picture, 24 for its label and a gap). |
| 72–81 | `for (int i = 0; i < 9; ++i) { Image tile = scene; std::string label = "original"; if (i > 0) { if (i == 4) { makeGrey(tile); } applyTable(tile, tables[i - 1]); label = names[i - 1]; } ...` | Tile 0 is the original; tiles 1–8 each use one table on a **copy** of the scene. The threshold tile (i = 4) is made grey first (Section 47.7). |
| 82–86 | `const int left = 10 + (i % 3) * 170; const int top = 10 + (i / 3) * 134; paste(sheet, tile, left, top); drawText(sheet, left, top + 114, label, colours::black);` | Put the tile in its place and write its name under it (Chapter 46). |
| 88–94 | `Image curves(4 * 150 + 10, 2 * 160 + 10, colours::white); for (...) { ... drawCurve(curves, left, top, 120, tables[i], Colour{200, 40, 40}); drawText(...); }` | The eight curves, 120 pixels big, each with its name. |
| 96–102 | `if (!savePNGCompressed(sheet, "operations.png") \|\| ...) { ... }` … `return 0;` `}` | Save both pictures as small PNG files (Chapter 45). |

### What you should see

```
input:              0   50  100  128  200  255   average
brightness +40     40   90  140  168  240  255   164.297
contrast x1.5       0   11   86  128  236  255   127.5
invert            255  205  155  127   55    0   127.5
threshold 128       0    0    0  255  255  255   127.5
gamma 0.5           0  113  160  181  226  255   169.805
gamma 2.0           0   10   39   64  157  255   85.1484
exposure x2         0   71  138  176  255  255   162.766
levels 50-200       0    0   85  133  255  255   130.02

230 + 40 with clamping: 255, with wrap-around: 14
100: brightness then contrast = 146, contrast then brightness = 126
invert twice is the identity: yes
wrote operations.png and curves.png
```

Open `operations.png` and compare the tiles: "brightness +40" looks washed out (black is gone); "gamma 0.5" and "exposure x2" are lighter but keep black; "exposure x2" clips the bright sky and sun to white; "threshold 128" is a black-and-white stencil. Then look at `curves.png` and match each curve to its tile.

---

## Small examples

### Example 1 — Darker

Brightness −60: 50 → **0** (clipped), 100 → **40**, 255 → **195**. Now the **top** is lost: nothing can be brighter than 195.

### Example 2 — Less contrast

Contrast × 0.5: 0 → (−128) × 0.5 + 128 = **64**; 255 → 127.5 × 0.5 + 128 = 191.75 → **192**. The picture becomes a grey, foggy version of itself.

### Example 3 — A threshold at 200

Only very bright values survive as white: 199 → **0**, 200 → **255**. Good for finding the sun or lights in a picture.

### Example 4 — Gamma undoes gamma

Gamma 2.0 after gamma 0.5: (x^0.5)² = x. Apart from rounding, the picture comes back: 100 → 160 → 255 × (160 / 255)² = 100.4 → **100**.

### Example 5 — A tint with three tables

`applyTables(image, brightnessTable(30), identityTable(), brightnessTable(-30))`: red up, blue down — a warm, "sunset" tint.

---

## Common mistakes

⚠️ **Doing the maths in a byte** — 230 + 40 wraps to 14. Use `int` or `double`, then clamp.

⚠️ **Integer division** — `v / 255` is 0 for every v below 255. Write `v / 255.0`.

⚠️ **Forgetting to round** — a plain cast cuts 159.7 down to 159. `clampByte` adds 0.5 first.

⚠️ **Thresholding a colour picture** — you get 8 poster colours, not black and white. Make it grey first.

⚠️ **The wrong order** — brightness then contrast is not contrast then brightness.

⚠️ **Too many steps** — each step may clip and round. Combine the tables first, or apply strong changes once.

---

## Practice

🏋️ **1.** Work out by hand what contrast × 2 does to 0, 64, 100, 128, 160 and 255. Which values are clipped?

🏋️ **2.** Write `posterizeTable(int levels)`, which keeps only `levels` different values (for example 4: 0, 85, 170, 255). Hint: `round(v × (levels − 1) / 255) × 255 / (levels − 1)`.

🏋️ **3.** Write `solarizeTable()`: values below 128 stay; values from 128 up are inverted. Draw its curve. (Photographers got this effect by flashing light on film while developing it.)

🏋️ **4.** Make a table with **two** thresholds: below 85 → 0, 85–169 → 128, from 170 → 255. Apply it to a grey picture.

🏋️ **5.** Use `applyTables` to turn a grey picture into a **sepia** (old brown photo) picture: red gets lighter, blue darker.

🏋️ **6.** Check Example 4 for **all** 256 values: how many come back exactly after gamma 0.5 then gamma 2.0? Which do not, and why?

🏋️ **7.** Load any PNG with `loadPNGFull` (Chapter 45), apply `exposureTable(0.5)` (one stop darker), and save it. Compare with `brightnessTable(-60)`.

🏋️ **8.** A point operation cannot blur a picture or find its edges. Why not?

---

## Answers

**1.**
> 0 → −128 → **0** (clipped); 64 → (−64) × 2 + 128 = **0** (exactly 0, not clipped); 100 → −56 + 128 = **72**; 128 → **128**; 160 → 64 + 128 = **192**; 255 → 382 → **255** (clipped). Everything below 64 becomes 0, and everything from 192 up becomes 255 (192 → 256 → clipped; 191 → 254 still fits).

**2.**

```cpp
LookupTable posterizeTable(int levels) {
    LookupTable t{};
    for (int v = 0; v < 256; ++v) {
        const double step = std::round(v * (levels - 1) / 255.0);
        t[v] = clampByte(step * 255.0 / (levels - 1));
    }
    return t;
}
```

**3.**

```cpp
LookupTable solarizeTable() {
    LookupTable t{};
    for (int v = 0; v < 256; ++v) {
        t[v] = static_cast<std::uint8_t>((v < 128) ? v : 255 - v);
    }
    return t;
}
```

> The curve goes up along the diagonal to 127, then jumps to 127 and comes down to 0: a roof shape.

**4.**

```cpp
LookupTable t{};
for (int v = 0; v < 256; ++v) {
    t[v] = (v < 85) ? 0 : (v < 170) ? 128 : 255;
}
```

**5.**
> For example `applyTables(picture, brightnessTable(40), brightnessTable(10), brightnessTable(-30))` on a grey picture: each grey value v becomes (v + 40, v + 10, v − 30), a warm brown. (Real sepia formulas mix the channels, which needs more than three tables — Chapter 14's colour maths.)

**6.**

```cpp
const LookupTable roundTrip = combineTables(gammaTable(0.5), gammaTable(2.0));
int same = 0;
for (int v = 0; v < 256; ++v) {
    same += (roundTrip[v] == v) ? 1 : 0;
}
```

> **192** of the 256 values come back; 64 do not (the first is 72). Gamma 0.5 **stretches** the dark values (0–50 spread over 0–113) but **squeezes** everything above 64, where its curve is flatter than the diagonal: there, neighbouring inputs round to the **same** output (the gamma 0.5 table has only 192 different answers). Once two values have merged, gamma 2.0 cannot split them again.

**7.**

```cpp
Image photo(0, 0);
if (loadPNGFull("photo.png", photo)) {
    Image darker = photo;
    applyTable(darker, exposureTable(0.5));
    savePNGCompressed(darker, "darker.png");
}
```

> Exposure × 0.5 keeps the dark parts readable (it halves the **light**); brightness −60 crushes everything below 60 into black.

**8.**
> Blurring mixes a pixel with its **neighbours**; finding an edge **compares** neighbours. A point operation only ever sees one value, so it cannot know anything about the pixels around it. That needs **convolution** — Chapter 49.

---

## Summary

🧠 A **point operation** changes each value using only that value. Its **transfer curve** shows everything it does: above the diagonal = lighter, steep = more contrast, flat = clipped.

🧠 A **lookup table** of 256 answers makes any point operation fast, and two tables combine into one: combined[v] = B[A[v]].

🧠 **Brightness** adds, **contrast** stretches around a centre, **invert** is 255 − v, **threshold** is a step, **gamma** bends the middle, **exposure** multiplies linear light, **levels** stretches a range to 0 … 255.

🧠 Always **clamp** (never wrap), and remember that clipping **loses** information for good.

🧠 The **order** of operations matters.

---

## Next chapter

How do we know which operation a picture needs? We **count**. In Chapter 48 we build a **histogram**: how many pixels have each value from 0 to 255, drawn as a bar chart with labels. It shows at a glance whether a picture is too dark, too bright or too grey. Then we use it to choose levels **automatically**, and meet **histogram equalisation**, which spreads the values out so that every brightness is used about equally.
