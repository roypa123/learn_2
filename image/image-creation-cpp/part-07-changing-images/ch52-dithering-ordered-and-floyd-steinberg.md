# Chapter 52 — Dithering: Ordered and Floyd–Steinberg

> **Part 7 · Chapter 52 of 82**
> **You need:** Chapters 1–51 (especially 5, 17, 47 and 50) · **You will make:** `dither.h` (posterising, ordered dithering with the Bayer matrix, colour palettes, the nearest colour, Floyd–Steinberg error diffusion, the average colour), and `dither.png`: a scene in 8 colours and in black and white, without and with dithering

---

## What you will learn

- Why a picture with only a few colours loses its shading, and how **dithering** brings it back.
- How our eyes **average** tiny dots, and why 50 % white dots look like grey 188, not 128.
- **Ordered dithering**: a threshold that changes from pixel to pixel, using the **Bayer matrix**.
- **Error diffusion**: the **Floyd–Steinberg** method, which passes each pixel's mistake on to its neighbours.
- How to find the **nearest colour** in a palette with the distance in the RGB cube.
- Why dithering, too, belongs in **linear light**.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **palette** | The list of colours a picture is allowed to use. |
| **posterise** | Replace each colour by the nearest allowed one, with no dithering. |
| **dithering** | Mixing allowed colours in a fine pattern, so that from far away they look like the missing colours. |
| **ordered dithering** | Dithering with a fixed pattern of thresholds. |
| **Bayer matrix** | The famous grid of threshold numbers for ordered dithering. |
| **error diffusion** | Dithering by passing each pixel's rounding mistake on to pixels not done yet. |
| **Floyd–Steinberg** | The most famous error diffusion method (1976). |

---

## 52.1 Too few colours

Our pictures have 256 levels in each channel: more than 16 million colours. Many devices and formats cannot show that many:

- an **e-ink** reader or a receipt printer: black and white only;
- a **GIF** file: at most 256 colours;
- old computers and game consoles: 2, 4, 16 or 256 colours;
- a **printer**: a dot of ink is there or it is not.

📖 **New word: palette** — the list of colours we are allowed to use.

The simplest way to use a small palette is to replace each colour by the **nearest** allowed one.

📖 **New word: posterise** — that replacement, with nothing else. (Old posters were printed with a few flat inks, hence the name.) For black and white, it is Chapter 47's **threshold**.

Chapter 47 already showed what goes wrong: all the shading disappears. A smooth grey ramp becomes one black half and one white half. And a whole area of grey 128 becomes pure **white** (128 is a little more than half of 255):

```
  threshold:                256 of 256 white, looks like grey 255
```

Chapter 47 promised a way to keep the shading. Here it is.

---

## 52.2 The eye averages

Look at a newspaper photo through a magnifying glass: it is made of black dots of different sizes on white paper. From a normal distance you cannot see the dots — you see grey. Your eye **averages** the light of a small area, a little like Chapter 50's blur.

📖 **New word: dithering** — mixing the allowed colours in a fine pattern, so that the **average** in each small area is the colour we wanted.

🔢 **Maths: how many white dots?**

> If a fraction p of the dots is white and the rest black, the area sends out **p × (the light of white)**.
> So for a grey that has 30 % of white's light, about 30 % of the dots should be white.

⚠️ **Light, not sRGB values.** Chapter 17 showed that grey 128 has only about **22 %** of white's light (srgbToLinear(128 / 255) = 0.216). So:

> grey 128 needs about **22 %** white dots, not 50 %!
> 50 % white dots send out 0.5 of white's light, and the grey with that light is linearToSrgb(0.5) × 255 = **188**.

The program checks this on a 16 × 16 patch of grey 128. "Looks like" is the patch's average **light**, turned back into a grey value (`averageColour`, at the end of this chapter's header):

```
  the grey itself:          0 of 256 white, looks like grey 128
  ordered, sRGB values:     128 of 256 white, looks like grey 188
  ordered, linear light:    48 of 256 white, looks like grey 120
```

Half the dots white looks like 188 — far too bright. About a fifth of them white looks close to 128. Keep this in mind for every method in this chapter: **count the light**.

---

## 52.3 Ordered dithering

The threshold of Chapter 47 asks the same question at every pixel: "is the value above 0.5?" The trick of ordered dithering: ask with a **different** threshold at each pixel, from a fixed pattern.

📖 **New word: ordered dithering** — white if value > threshold(x, y), where the thresholds come from a small grid that repeats across the picture like tiles.

If the 16 thresholds in a 4 × 4 tile are spread evenly between 0 and 1, then a flat area with value v gets white wherever the threshold is below v: about **v × 16** of every 16 pixels. That is exactly the fraction we want.

📖 **New word: Bayer matrix** — the best-known threshold grid, from Bryce Bayer (who also invented the colour filter inside almost every camera):

```
Bayer 4 x 4:
     0  8  2 10
    12  4 14  6
     3 11  1  9
    15  7 13  5
thresholds of the top row: 0.03125 0.53125 0.15625 0.65625
```

🔢 **Maths: from numbers to thresholds**

> The grid holds the numbers 0 … 15, each once. Threshold = (number + 0.5) / 16:
> 0 → 0.5 / 16 = **0.03125**; 8 → 8.5 / 16 = **0.53125**; 15 → 15.5 / 16 = 0.96875.
> The + 0.5 puts each threshold in the **middle** of its sixteenth, so that 0 stays all black and 1 all white.

**Why this order?** Imagine raising the grey slowly. The pixel with number 0 turns white first, then 1, then 2, and so on. Look where they are: 0 is at the top-left, 1 is in the middle (2, 2) — as far from 0 as possible in the tile —, 2 and 3 fill the remaining gaps... Each new white dot lands as far as possible from the dots that are already white. So the dots are always spread evenly, never in clumps.

🔢 **Maths: how the grid is built**

The 2 × 2 Bayer matrix is:

```
   0  2
   3  1
```

(0 and 1 on one diagonal, 2 and 3 on the other.) The 4 × 4 one is four copies of 4 × (the 2 × 2), with 0, 2, 3 and 1 added to the copies in that same pattern:

> top-left: 4 × (0 2 / 3 1) + 0 = **0 8 / 12 4**; top-right: + 2 = **2 10 / 14 6**
> bottom-left: + 3 = **3 11 / 15 7**; bottom-right: + 1 = **1 9 / 13 5**

The same rule makes 8 × 8 from 4 × 4, and so on (Practice 3).

🔢 **Maths: grey 128 in linear light**

> The light of grey 128 is **0.2159**. Thresholds below it: 0.03125 (number 0), 0.09375 (1), 0.15625 (2). The next one, 0.21875 (number 3), is just above.
> So **3 of every 16** pixels are white: 3 × 16 = **48** of 256.

```
ordered, linear light, top rows:
    #.#.#.#.#.#.#.#.
    ................
    ..#...#...#...#.
    ................
```

Number 0 is at (0, 0), number 2 at (2, 0), number 1 at (2, 2): exactly the `#` positions above, repeated every 4 pixels. The light is 3/16 = 0.1875, which looks like grey **120** — a bit darker than 128, because a 4 × 4 tile can only make **17** shades (0 … 16 white dots). An 8 × 8 matrix makes 65.

### More than two levels

With more levels per channel (say 4 levels: 0, 85, 170, 255), we do the same thing **between the two nearest levels**:

> value 100: it lies between the levels 85 and 170, at the fraction f = (100 − 85) / 85 = 0.18 of the way.
> Then: the higher level (170) if f > threshold, else the lower one (85). About 18 % of the pixels become 170.

`orderedChannel` does exactly this, one channel at a time. With `linearLight`, it measures the fraction in **light** instead: f = (L(v) − L(low)) / (L(high) − L(low)), where L is `srgbToLinear`. For two levels (0 and 1) that is simply f = L(v), as in the worked example.

---

## 52.4 Error diffusion: the idea

Ordered dithering decides each pixel on its own. **Error diffusion** does something cleverer: it **remembers** its mistakes.

📖 **New word: error diffusion** — round each pixel to the nearest allowed colour, and **add the rounding error** to the pixels that have not been done yet. "Diffusion" means spreading out.

🔢 **Maths: one row of grey 0.4**

Work along a row where every value is 0.4 (black = 0, white = 1). The error = what we wanted − what we drew, and all of it goes to the next pixel:

| Pixel | Value + error from before | Drawn | Error passed on |
|---|---|---|---|
| 1 | 0.4 | black (0) | 0.4 − 0 = **+0.4** |
| 2 | 0.4 + 0.4 = 0.8 | white (1) | 0.8 − 1 = **−0.2** |
| 3 | 0.4 − 0.2 = 0.2 | black | **+0.2** |
| 4 | 0.4 + 0.2 = 0.6 | white | **−0.4** |
| 5 | 0.4 − 0.4 = 0.0 | black | **0** |
| 6 | 0.4 (the same as pixel 1 — it repeats) | black | +0.4 |

Black, white, black, white, black — and repeat: **2 of every 5** pixels are white = 0.4. ✓ Without any pattern table, the right number of white dots came out by itself. Each mistake was paid back by the next pixels.

🧠 **Why it works:** the total of all the errors never grows. Whatever was "too dark" a moment ago is made up by being "too bright" soon after. So over any stretch, the average of the drawn values is the average of the wanted values.

---

## 52.5 Floyd–Steinberg

In a picture, the error can go to more than one neighbour. Robert Floyd and Louis Steinberg (1976) spread it over **four** pixels that are not done yet — one to the right in this row, three in the row below:

```
              current    7/16
     3/16      5/16      1/16
```

📖 **New word: Floyd–Steinberg** — error diffusion with these four weights. They add up to 16/16 = 1, so all of the error is passed on (except at the picture's edges, where some of it falls outside and is lost).

⚠️ **Only forwards.** We go through the picture row by row, left to right. The four neighbours are exactly the ones we have **not** drawn yet. The pixel to the left and the row above are already finished — sending error to them would change nothing.

🔢 **Maths: the first pixel of grey 128, in sRGB values**

> value 128 / 255 = 0.502 → nearest of 0 and 1 is **1** (white); error = 0.502 − 1 = **−0.498**
> right neighbour: 0.502 + (−0.498) × 7/16 = 0.502 − 0.218 = **0.284** → black, error +0.284 …
> below: 0.502 − 0.498 × 5/16 = 0.346, and so on.

In sRGB values this gives a perfect checkerboard: 128 of 256 white. But we know (Section 52.2) that this looks like 188. In **linear light** (value 0.2159):

```
  Floyd-Steinberg, sRGB:    128 of 256 white, looks like grey 188
  Floyd-Steinberg, linear:  52 of 256 white, looks like grey 124
Floyd-Steinberg, linear light, top rows:
    ................
    .#.#.#.#.#.#.#..
    ...............#
    .#..#..#..#..#..
```

0.2159 × 256 = 55.3, so we hoped for about 55 white dots; we got 52. The difference is the error that fell off the right and bottom edges of this small 16 × 16 patch (and what was still "owed" at the end). On a big picture, it hardly matters.

💡 Look at the dots: they are not on a regular grid like the ordered ones. Error diffusion makes an irregular, "organic" pattern. Each pixel's decision depends on all the pixels before it.

---

## 52.6 Colours: the nearest colour in the RGB cube

With colour, the palette is a list of colours, and "round to the nearest" means: find the palette colour that is **closest** to the colour we want.

Chapter 5 promised this: colours are points in the **RGB cube** (red across, green up, blue in depth), and the distance between two colours is Pythagoras in three directions (Chapter 29):

> **distance = √((r₁ − r₂)² + (g₁ − g₂)² + (b₁ − b₂)²)**

🔢 **Maths: orange against the 8 corners**

The 8 corners of the cube are the colours with every channel 0 or 255: black, blue, green, cyan, red, magenta, yellow, white. For orange (200, 100, 50):

> red (255, 0, 0): 55² + 100² + 50² = 3,025 + 10,000 + 2,500 = **15,525** → √ = **124.6**
> yellow (255, 255, 0): 3,025 + 24,025 + 2,500 = 29,550 → 171.9
> black (0, 0, 0): 40,000 + 10,000 + 2,500 = 52,500 → 229.1
> white (255, 255, 255): 3,025 + 24,025 + 42,025 = 69,075 → 262.8

```
nearest of the 8 corner colours to 200 100 50: 255 0 0, distance 124.6
```

💡 To find the nearest, we do not need the square root: if a² < b², then a < b. So `nearestIndex` compares **squared** distances (`distanceSquared`) — faster, and the same answer.

`cubePalette(levels)` makes a palette of evenly spaced levels in each channel: 2 levels → 2³ = **8** colours (the corners); 4 levels → 64; 6 levels → 216 (the old "web-safe" palette). For such a palette, the nearest colour is simply the nearest level in each channel — which is what `posterise` does.

**Floyd–Steinberg in colour** works exactly as in grey, with three numbers instead of one: the error is a `ColourF` (wanted − drawn, for red, green and blue), and it is spread with the same four weights.

### Does the colour come out right?

The program makes a 64 × 16 ramp from orange (200, 100, 50) to sky blue (40, 160, 220) and measures its average colour — the colour you would see from far away:

```
colour ramp, average colour seen from far away:
  original:               131 131 146
  nearest corner colour:  179 195 195
  ordered, 8 colours:     132 131 146
  Floyd-Steinberg, 8:     129 131 145
```

Posterised, the ramp becomes just two flat blocks: red on the left half, cyan on the right (all three channels cross the halfway point near the middle). The average is far off (179 195 195). Both dithered versions use the **same** 8 colours, yet their average is within 2 of the original. That is the whole point of dithering.

💡 `floydSteinberg` measures the distance in the same units as the error: linear light by default. The error **must** be in linear light (it is light that adds up), but distances in linear light do not match our eyes very well — two dark colours look more different than their small linear distance suggests. Better "perceptual" colour distances exist; for small palettes like ours, the simple one is fine.

---

## 52.7 Ordered or error diffusion?

| | Ordered (Bayer) | Error diffusion (Floyd–Steinberg) |
|---|---|---|
| **Pattern** | regular cross-hatch, the same tile everywhere | irregular, organic dots |
| **Detail** | good | better: edges and fine lines survive |
| **Each pixel** | decided alone (can be done in any order, or all at once) | depends on every pixel before it |
| **Change one pixel** | only that pixel changes | the dots after it can all change |
| **Animation** | calm: still areas stay still | flickers: dots dance from frame to frame |
| **Known problems** | the tile pattern can be visible | "worms": short wiggly chains of dots in smooth areas |

Both are still used. Ordered dithering is popular in games and animation. Error diffusion is popular for still pictures, printers and GIF files.

💡 Dithering is even used **without** a small palette. A smooth sky gradient in 8 bits can show faint steps (bands). Adding a tiny ordered dither before rounding to bytes hides them — the same trick, with 256 levels.

---

## Code, part 1: `dither.h`

File: `common/dither.h` (new). It includes `edges.h` (and through it `blur.h`, for `PixelsF`, Chapter 50).

```cpp
#ifndef DITHER_H
#define DITHER_H

#include <algorithm>
#include <cmath>
#include <vector>
#include "edges.h"

const int kBayer4[16] = {0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5};

inline double bayerThreshold(int x, int y) {
    return (kBayer4[(y % 4) * 4 + (x % 4)] + 0.5) / 16.0;
}

inline double nearestLevel(double v, int levels) {
    const double steps = levels - 1;
    return std::floor(std::clamp(v, 0.0, 1.0) * steps + 0.5) / steps;
}

inline Image posterise(const Image& image, int levels) {
    Image out(image.width(), image.height());
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            const ColourF c = toColourF(image.getPixel(x, y));
            const ColourF q{nearestLevel(c.r, levels), nearestLevel(c.g, levels),
                            nearestLevel(c.b, levels)};
            out.setPixel(x, y, toColour(q));
        }
    }
    return out;
}

inline double orderedChannel(double v, double t, int levels, bool linearLight) {
    const double steps = levels - 1;
    const double low = std::floor(v * steps) / steps;
    if (low >= 1.0) {
        return 1.0;
    }
    const double high = low + 1.0 / steps;
    double f = (v - low) * steps;
    if (linearLight) {
        f = (srgbToLinear(v) - srgbToLinear(low)) / (srgbToLinear(high) - srgbToLinear(low));
    }
    return (f > t) ? high : low;
}

inline Image orderedDither(const Image& image, int levels, bool linearLight = true) {
    Image out(image.width(), image.height());
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            const ColourF c = toColourF(image.getPixel(x, y));
            const double t = bayerThreshold(x, y);
            const ColourF q{orderedChannel(c.r, t, levels, linearLight),
                            orderedChannel(c.g, t, levels, linearLight),
                            orderedChannel(c.b, t, levels, linearLight)};
            out.setPixel(x, y, toColour(q));
        }
    }
    return out;
}

inline std::vector<Colour> cubePalette(int levels) {
    std::vector<Colour> palette;
    for (int r = 0; r < levels; ++r) {
        for (int g = 0; g < levels; ++g) {
            for (int b = 0; b < levels; ++b) {
                const double s = 1.0 / (levels - 1);
                palette.push_back(toColour(ColourF{r * s, g * s, b * s}));
            }
        }
    }
    return palette;
}

inline double distanceSquared(ColourF a, ColourF b) {
    const ColourF d = a - b;
    return d.r * d.r + d.g * d.g + d.b * d.b;
}

inline int nearestIndex(ColourF c, const std::vector<ColourF>& palette) {
    int best = 0;
    for (int i = 1; i < static_cast<int>(palette.size()); ++i) {
        if (distanceSquared(c, palette[i]) < distanceSquared(c, palette[best])) {
            best = i;
        }
    }
    return best;
}

inline void addError(PixelsF& p, int x, int y, ColourF error, double weight) {
    if (x >= 0 && x < p.width && y >= 0 && y < p.height) {
        p.data[y * p.width + x] = p.data[y * p.width + x] + error * weight;
    }
}

inline Image floydSteinberg(const Image& image, const std::vector<Colour>& palette,
                            bool linearLight = true) {
    PixelsF work = toPixelsF(image, linearLight);
    std::vector<ColourF> values;
    for (Colour c : palette) {
        values.push_back(linearLight ? toLinear(c) : toColourF(c));
    }
    Image out(image.width(), image.height());
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            const ColourF old = work.data[y * work.width + x];
            const int k = nearestIndex(old, values);
            out.setPixel(x, y, palette[k]);
            const ColourF error = old - values[k];
            addError(work, x + 1, y, error, 7.0 / 16.0);
            addError(work, x - 1, y + 1, error, 3.0 / 16.0);
            addError(work, x, y + 1, error, 5.0 / 16.0);
            addError(work, x + 1, y + 1, error, 1.0 / 16.0);
        }
    }
    return out;
}

inline Colour averageColour(const Image& image) {
    ColourF sum{0.0, 0.0, 0.0};
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            sum = sum + toLinear(image.getPixel(x, y));
        }
    }
    return fromLinear(sum / (image.width() * image.height()));
}

#endif
```

### Line by line

**The Bayer matrix and posterising (lines 1–31)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–7 | include guard and `#include` lines | `std::clamp`, `std::floor`, lists, and Chapter 51's header. |
| 9 | `const int kBayer4[16] = {0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5};` | The 4 × 4 Bayer matrix, row by row (Section 52.3). |
| 11–13 | `inline double bayerThreshold(int x, int y) { return (kBayer4[(y % 4) * 4 + (x % 4)] + 0.5) / 16.0; }` | The threshold for pixel (x, y). `% 4` repeats the tile across the whole picture. |
| 15–18 | `inline double nearestLevel(double v, int levels) { const double steps = levels - 1; return std::floor(std::clamp(v, 0.0, 1.0) * steps + 0.5) / steps; }` | Round v (0 … 1) to the nearest of `levels` evenly spaced levels. With 2 levels: v < 0.5 → 0, else 1. |
| 20–31 | `inline Image posterise(const Image& image, int levels) { ... const ColourF q{nearestLevel(c.r, levels), nearestLevel(c.g, levels), nearestLevel(c.b, levels)}; out.setPixel(x, y, toColour(q)); ... }` | Every channel to its nearest level, with no dithering (Section 52.1). |

**Ordered dithering (lines 33–60)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 33–37 | `inline double orderedChannel(double v, double t, int levels, bool linearLight) { const double steps = levels - 1; const double low = std::floor(v * steps) / steps; if (low >= 1.0) { return 1.0; }` | The level just below v. If v is already the top level (1), there is nothing to choose. |
| 38–42 | `const double high = low + 1.0 / steps; double f = (v - low) * steps; if (linearLight) { f = (srgbToLinear(v) - srgbToLinear(low)) / (srgbToLinear(high) - srgbToLinear(low)); }` | The level just above, and how far v is from `low` to `high`, as a fraction f (0 … 1) — in sRGB values or in light (Section 52.3). |
| 43–45 | `return (f > t) ? high : low;` `}` | The ordered-dither decision. |
| 47–60 | `inline Image orderedDither(const Image& image, int levels, bool linearLight = true) { ... const double t = bayerThreshold(x, y); const ColourF q{orderedChannel(c.r, t, levels, linearLight), ...}; out.setPixel(x, y, toColour(q)); ... }` | For every pixel: its threshold, then each channel's decision with the same threshold. Linear light by default. |

**Palettes and the nearest colour (lines 62–88)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 62–73 | `inline std::vector<Colour> cubePalette(int levels) { std::vector<Colour> palette; for (r) { for (g) { for (b) { const double s = 1.0 / (levels - 1); palette.push_back(toColour(ColourF{r * s, g * s, b * s})); } } } return palette; }` | All combinations of the levels: levels³ colours. For 2 levels: black, blue, green, cyan, red, magenta, yellow, white (in that order). |
| 75–78 | `inline double distanceSquared(ColourF a, ColourF b) { const ColourF d = a - b; return d.r * d.r + d.g * d.g + d.b * d.b; }` | The squared distance in the RGB cube (Section 52.6). |
| 80–88 | `inline int nearestIndex(ColourF c, const std::vector<ColourF>& palette) { int best = 0; for (int i = 1; ...; ++i) { if (distanceSquared(c, palette[i]) < distanceSquared(c, palette[best])) { best = i; } } return best; }` | Try every palette colour; keep the closest. On a tie, the earlier one wins (`<`, not `<=`). |

**Floyd–Steinberg (lines 90–117)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 90–94 | `inline void addError(PixelsF& p, int x, int y, ColourF error, double weight) { if (x >= 0 && x < p.width && y >= 0 && y < p.height) { p.data[y * p.width + x] = p.data[y * p.width + x] + error * weight; } }` | Add a share of the error to one pixel — only if it is inside the picture. Outside, the error is lost. |
| 96–101 | `inline Image floydSteinberg(const Image& image, const std::vector<Colour>& palette, bool linearLight = true) { PixelsF work = toPixelsF(image, linearLight); std::vector<ColourF> values; for (Colour c : palette) { values.push_back(linearLight ? toLinear(c) : toColourF(c)); }` | `work` is a copy of the picture as doubles, which collects the errors. `values` is the palette in the same units (light or sRGB values). |
| 102–106 | `Image out(...); for (y) { for (x) { const ColourF old = work.data[y * work.width + x]; const int k = nearestIndex(old, values); out.setPixel(x, y, palette[k]);` | Row by row, left to right: the wanted colour (with the errors so far), its nearest palette colour, and draw it. |
| 107–112 | `const ColourF error = old - values[k]; addError(work, x + 1, y, error, 7.0 / 16.0); addError(work, x - 1, y + 1, error, 3.0 / 16.0); addError(work, x, y + 1, error, 5.0 / 16.0); addError(work, x + 1, y + 1, error, 1.0 / 16.0);` | The error, shared out with the four weights of Section 52.5. Write `7.0 / 16.0`, not `7 / 16` — whole-number division would give 0. |
| 113–117 | `}` `}` `return out;` `}` | |

**Average colour (lines 119–129)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 119–127 | `inline Colour averageColour(const Image& image) { ColourF sum{0.0, 0.0, 0.0}; for (...) { sum = sum + toLinear(image.getPixel(x, y)); } return fromLinear(sum / (image.width() * image.height())); }` | The average **light** of the whole picture, as a colour: what you see from far away (Section 52.2). |
| 129 | `#endif` | End of the include guard. |

---

## Code, part 2: dithering compared

File: `ch52/dither.cpp`

```cpp
#include <cmath>
#include <iostream>
#include <string>
#include <vector>
#include "dither.h"
#include "deflate.h"

std::string oneDecimal(double v) {
    const long long n = std::llround(v * 10.0);
    return std::to_string(n / 10) + "." + std::to_string(n % 10);
}

std::string colourText(Colour c) {
    return std::to_string(c.r) + " " + std::to_string(c.g) + " " + std::to_string(c.b);
}

int countWhite(const Image& image) {
    int count = 0;
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            count += (image.getPixel(x, y).r == 255) ? 1 : 0;
        }
    }
    return count;
}

void report(const std::string& label, const Image& image) {
    std::cout << label << " " << countWhite(image) << " of " << image.width() * image.height()
              << " white, looks like grey " << static_cast<int>(averageColour(image).r) << "\n";
}

void printDots(const std::string& label, const Image& image, int rows) {
    std::cout << label << "\n";
    for (int y = 0; y < rows; ++y) {
        std::cout << "    ";
        for (int x = 0; x < image.width(); ++x) {
            std::cout << ((image.getPixel(x, y).r == 255) ? "#" : ".");
        }
        std::cout << "\n";
    }
}

Image makeColourRamp() {
    Image ramp(64, 16);
    for (int x = 0; x < 64; ++x) {
        const Colour c = lerpColour(Colour{200, 100, 50}, Colour{40, 160, 220}, x / 63.0);
        fillRect(ramp, makeRect(x, 0, 1, 16), c);
    }
    return ramp;
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

int main() {
    std::cout << "Bayer 4 x 4:\n";
    for (int y = 0; y < 4; ++y) {
        std::cout << "   ";
        for (int x = 0; x < 4; ++x) {
            const int v = kBayer4[y * 4 + x];
            std::cout << ((v < 10) ? "  " : " ") << v;
        }
        std::cout << "\n";
    }
    std::cout << "thresholds of the top row: " << bayerThreshold(0, 0) << " " << bayerThreshold(1, 0)
              << " " << bayerThreshold(2, 0) << " " << bayerThreshold(3, 0) << "\n";

    const Image grey(16, 16, Colour{128, 128, 128});
    const std::vector<Colour> blackWhite = {colours::black, colours::white};
    const Image orderedLinear = orderedDither(grey, 2, true);
    const Image diffusedLinear = floydSteinberg(grey, blackWhite, true);
    std::cout << "\ngrey 128 as black and white dots:\n";
    report("  the grey itself:         ", grey);
    report("  threshold:               ", posterise(grey, 2));
    report("  ordered, sRGB values:    ", orderedDither(grey, 2, false));
    report("  ordered, linear light:   ", orderedLinear);
    report("  Floyd-Steinberg, sRGB:   ", floydSteinberg(grey, blackWhite, false));
    report("  Floyd-Steinberg, linear: ", diffusedLinear);
    printDots("ordered, linear light, top rows:", orderedLinear, 4);
    printDots("Floyd-Steinberg, linear light, top rows:", diffusedLinear, 4);

    const std::vector<Colour> corners = cubePalette(2);
    const ColourF orange = toColourF(Colour{200, 100, 50});
    std::vector<ColourF> cornerValues;
    for (Colour c : corners) {
        cornerValues.push_back(toColourF(c));
    }
    const int k = nearestIndex(orange, cornerValues);
    std::cout << "\nnearest of the 8 corner colours to 200 100 50: " << colourText(corners[k])
              << ", distance " << oneDecimal(255.0 * std::sqrt(distanceSquared(orange, cornerValues[k])))
              << "\n";

    const Image ramp = makeColourRamp();
    std::cout << "\ncolour ramp, average colour seen from far away:\n";
    std::cout << "  original:               " << colourText(averageColour(ramp)) << "\n";
    std::cout << "  nearest corner colour:  " << colourText(averageColour(posterise(ramp, 2))) << "\n";
    std::cout << "  ordered, 8 colours:     " << colourText(averageColour(orderedDither(ramp, 2)))
              << "\n";
    std::cout << "  Floyd-Steinberg, 8:     "
              << colourText(averageColour(floydSteinberg(ramp, corners))) << "\n";

    const Image scene = makeScene();
    Image greyScene = scene;
    makeGrey(greyScene);
    const Image tiles[8] = {scene,
                            posterise(scene, 2),
                            orderedDither(scene, 2),
                            floydSteinberg(scene, corners),
                            greyScene,
                            posterise(greyScene, 2),
                            orderedDither(greyScene, 2),
                            floydSteinberg(greyScene, blackWhite)};
    const std::string names[8] = {"original",   "8 colours",   "ordered, 8",  "Floyd-St., 8",
                                  "grey",       "threshold",   "ordered, b/w", "Floyd-St., b/w"};
    Image sheet(4 * 170 + 10, 2 * 134 + 10, colours::white);
    for (int i = 0; i < 8; ++i) {
        const int left = 10 + (i % 4) * 170;
        const int top = 10 + (i / 4) * 134;
        for (int y = 0; y < 110; ++y) {
            for (int x = 0; x < 160; ++x) {
                sheet.setPixel(left + x, top + y, tiles[i].getPixel(x, y));
            }
        }
        drawText(sheet, left, top + 114, names[i], colours::black);
    }
    if (!savePNGCompressed(sheet, "dither.png")) {
        std::cout << "could not write dither.png\n";
        return 1;
    }
    std::cout << "wrote dither.png\n";
    return 0;
}
```

Build and run it from the `code/ch52` folder:

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common dither.cpp -o dither
./dither
```

### Line by line

**Helpers (lines 1–66)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–6 | the `#include` lines | `std::llround` and `std::sqrt`, printing, strings, lists, the new header, and `deflate.h`. |
| 8–11 | `std::string oneDecimal(double v) { ... }` | One digit after the point (as in Chapter 51). |
| 13–15 | `std::string colourText(Colour c) { ... }` | A colour as three numbers (as in Chapter 50). |
| 17–25 | `int countWhite(const Image& image) { ... count += (image.getPixel(x, y).r == 255) ? 1 : 0; ... }` | How many pixels are white. (Our black-and-white pictures have only 0 and 255.) |
| 27–30 | `void report(const std::string& label, const Image& image) { std::cout << label << " " << countWhite(image) << " of " << ... << " white, looks like grey " << static_cast<int>(averageColour(image).r) << "\n"; }` | One line of the grey-128 test: white dots, and the grey with the same average light. |
| 32–41 | `void printDots(const std::string& label, const Image& image, int rows) { ... std::cout << ((image.getPixel(x, y).r == 255) ? "#" : "."); ... }` | Draw the first few rows as text: `#` for white, `.` for black. |
| 43–50 | `Image makeColourRamp() { Image ramp(64, 16); for (int x = 0; x < 64; ++x) { const Colour c = lerpColour(Colour{200, 100, 50}, Colour{40, 160, 220}, x / 63.0); fillRect(ramp, makeRect(x, 0, 1, 16), c); } return ramp; }` | The orange-to-blue ramp of Section 52.6: one column at a time (Chapter 13's `lerpColour`, Chapter 19's `fillRect`). |
| 52–66 | `Image makeScene() { ... }` | Chapter 47's scene. |

**The Bayer matrix and grey 128 (lines 69–93)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 69–77 | `std::cout << "Bayer 4 x 4:\n"; for (y) { std::cout << "   "; for (x) { const int v = kBayer4[y * 4 + x]; std::cout << ((v < 10) ? "  " : " ") << v; } ... }` | Print the matrix; one-digit numbers get an extra space so the columns line up. |
| 78–79 | `std::cout << "thresholds of the top row: " << bayerThreshold(0, 0) << ...` | The first four thresholds. |
| 81–84 | `const Image grey(16, 16, Colour{128, 128, 128}); const std::vector<Colour> blackWhite = {colours::black, colours::white}; const Image orderedLinear = orderedDither(grey, 2, true); const Image diffusedLinear = floydSteinberg(grey, blackWhite, true);` | A patch of grey 128, a black-and-white palette, and the two linear-light results (kept, because we print them twice). |
| 85–91 | `report("  the grey itself:         ", grey); report(..., posterise(grey, 2)); report(..., orderedDither(grey, 2, false)); ...` | The six lines of Sections 52.2–52.5. |
| 92–93 | `printDots("ordered, linear light, top rows:", orderedLinear, 4); printDots(..., diffusedLinear, 4);` | The two dot patterns. |

**The nearest colour and the ramp (lines 95–113)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 95–100 | `const std::vector<Colour> corners = cubePalette(2); const ColourF orange = toColourF(Colour{200, 100, 50}); std::vector<ColourF> cornerValues; for (Colour c : corners) { cornerValues.push_back(toColourF(c)); }` | The 8 corners, and the same colours as `ColourF` (0 … 1) for `nearestIndex`. |
| 101–104 | `const int k = nearestIndex(orange, cornerValues); std::cout << ... colourText(corners[k]) << ", distance " << oneDecimal(255.0 * std::sqrt(distanceSquared(orange, cornerValues[k]))) << "\n";` | The nearest corner and its distance — times 255 to get back to byte units (Section 52.6). |
| 106–113 | `const Image ramp = makeColourRamp(); std::cout << ... colourText(averageColour(ramp)) ... averageColour(posterise(ramp, 2)) ... averageColour(orderedDither(ramp, 2)) ... averageColour(floydSteinberg(ramp, corners)) ...` | The average colour of the ramp: original, posterised, and the two dithers. |

**The picture (lines 115–145)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 115–117 | `const Image scene = makeScene(); Image greyScene = scene; makeGrey(greyScene);` | The scene, and a grey copy (Chapter 47's `makeGrey`). |
| 118–125 | `const Image tiles[8] = {scene, posterise(scene, 2), orderedDither(scene, 2), floydSteinberg(scene, corners), greyScene, posterise(greyScene, 2), orderedDither(greyScene, 2), floydSteinberg(greyScene, blackWhite)};` | Top row: colour, then 8 colours without dithering, ordered, and Floyd–Steinberg. Bottom row: the same in black and white. |
| 126–138 | `const std::string names[8] = {...}; Image sheet(4 * 170 + 10, 2 * 134 + 10, colours::white); for (...) { ... drawText(...); }` | The 4 × 2 sheet, as in Chapter 51. |
| 139–145 | `if (!savePNGCompressed(sheet, "dither.png")) { ... }` … `return 0;` `}` | Save it. |

### What you should see

```
Bayer 4 x 4:
     0  8  2 10
    12  4 14  6
     3 11  1  9
    15  7 13  5
thresholds of the top row: 0.03125 0.53125 0.15625 0.65625

grey 128 as black and white dots:
  the grey itself:          0 of 256 white, looks like grey 128
  threshold:                256 of 256 white, looks like grey 255
  ordered, sRGB values:     128 of 256 white, looks like grey 188
  ordered, linear light:    48 of 256 white, looks like grey 120
  Floyd-Steinberg, sRGB:    128 of 256 white, looks like grey 188
  Floyd-Steinberg, linear:  52 of 256 white, looks like grey 124
ordered, linear light, top rows:
    #.#.#.#.#.#.#.#.
    ................
    ..#...#...#...#.
    ................
Floyd-Steinberg, linear light, top rows:
    ................
    .#.#.#.#.#.#.#..
    ...............#
    .#..#..#..#..#..

nearest of the 8 corner colours to 200 100 50: 255 0 0, distance 124.6

colour ramp, average colour seen from far away:
  original:               131 131 146
  nearest corner colour:  179 195 195
  ordered, 8 colours:     132 131 146
  Floyd-Steinberg, 8:     129 131 145
wrote dither.png
```

In `dither.png`, hold the page a little away from you (or squint):

- **8 colours** (posterised): the sky is three flat bands of blue, cyan and white; the house is flat red and the sun yellow. The hills and the roof turn **black**: their green and red values (110 and less) are below the halfway point 128. All the soft shading has gone.
- **ordered, 8**: the hills come back as a mix of green and black dots; the sky is a fine cross-hatch of blue, cyan and white dots that, from a distance, gives back the smooth gradient. You can see the regular 4 × 4 pattern close up.
- **Floyd-St., 8**: the same colours, scattered irregularly. Edges (the roof, the sun) look a little crisper.
- **threshold**: the grey scene in pure black and white — big black and white blobs.
- **ordered, b/w** and **Floyd-St., b/w**: the shading is back, made only of black and white dots, like a newspaper photo.

---

## Small examples

### Example 1 — How many shades from a 4 × 4 tile?

0, 1, 2 … 16 white dots out of 16: **17** shades. An 8 × 8 tile: 65.

### Example 2 — White dots for grey 64

The light of grey 64: srgbToLinear(64 / 255) ≈ **0.051**. So about 5 % white dots: 0.051 × 256 ≈ **13** of 256.

### Example 3 — Sharing an error

The wanted value is 0.7 and we draw white (1): error = 0.7 − 1 = **−0.3**. The right neighbour gets −0.3 × 7/16 ≈ **−0.131**, the one below −0.3 × 5/16 ≈ −0.094.

### Example 4 — Palette sizes

`cubePalette(4)`: 4³ = **64** colours (levels 0, 85, 170, 255). `cubePalette(6)`: 6³ = **216** colours (0, 51, 102, 153, 204, 255).

### Example 5 — The longest distance in the cube

From black (0, 0, 0) to white (255, 255, 255): √(3 × 255²) = 255 × √3 ≈ **441.7**.

---

## Common mistakes

⚠️ **Counting sRGB values instead of light** — 50 % white dots for grey 128 makes it look like 188. Dither in linear light.

⚠️ **`7 / 16` instead of `7.0 / 16.0`** — whole-number division gives 0, and no error is spread at all.

⚠️ **Sending error backwards** — to pixels already drawn. It changes nothing (and the error is lost).

⚠️ **Rounding the work picture to bytes** — the small errors get lost. Keep the work picture in doubles (`PixelsF`).

⚠️ **Forgetting the edge check** — `x − 1` at x = 0, or `y + 1` on the last row, is outside the picture.

⚠️ **Dithering and then resizing** — shrinking or blurring a dithered picture mixes the dots into mud (or makes new patterns). Dither **last**, at the final size.

---

## Practice

🏋️ **1.** Use the 2 × 2 Bayer matrix (0 2 / 3 1) on a flat area of 0.6 (sRGB values, no linear light). What are the four thresholds, and which pixels are white?

🏋️ **2.** Do one-row error diffusion (all of the error to the right, as in Section 52.4) by hand for the value 0.6. What pattern comes out?

🏋️ **3.** Write `int bayer8(int x, int y)` that gives the 8 × 8 Bayer number for a pixel, using the rule of Section 52.3 and `kBayer4`.

🏋️ **4.** **Serpentine** Floyd–Steinberg: go left to right on even rows and right to left on odd rows (with the error weights mirrored). This breaks up the "worms". Change the loops of `floydSteinberg`.

🏋️ **5.** Dither a grey ramp (0 … 255 across 256 pixels) with `orderedDither(ramp, 4)`. Which byte values appear in the result?

🏋️ **6.** Make a palette of four greens like an old hand-held game console — (15, 56, 15), (48, 98, 48), (139, 172, 15), (155, 188, 15) — and dither the grey scene with it.

🏋️ **7.** Why can the ordered dither of one pixel be computed without looking at any other pixel, but Floyd–Steinberg cannot?

🏋️ **8.** **Atkinson dithering** (used on the first Apple Macintosh): it gives 1/8 of the error to each of six pixels — (x + 1, y), (x + 2, y), (x − 1, y + 1), (x, y + 1), (x + 1, y + 1), (x, y + 2) — so only 6/8 of the error is passed on. Change the four `addError` lines. What happens to the shading?

---

## Answers

**1.**
> Thresholds (number + 0.5) / 4: **0.125 0.625 / 0.875 0.375**.
> White where 0.6 > threshold: the two pixels with 0.125 and 0.375 — the top-left and bottom-right of each 2 × 2 tile: a checkerboard, 2 of 4 white (0.5, the closest the 2 × 2 tile can get to 0.6: it has only 5 shades).

**2.**
> 0.6 → white, error −0.4; 0.2 → black, +0.2; 0.8 → white, −0.2; 0.4 → black, +0.4; 1.0 → white, 0; then it repeats.
> White, black, white, black, white: **3 of 5** white = 0.6 ✓.

**3.**

```cpp
int bayer8(int x, int y) {
    const int offset[4] = {0, 2, 3, 1};
    const int small = kBayer4[(y % 4) * 4 + (x % 4)];
    const int quarter = ((y % 8) / 4) * 2 + (x % 8) / 4;
    return 4 * small + offset[quarter];
}
```

> Four copies of 4 × the 4 × 4 matrix, with 0, 2, 3, 1 added to the top-left, top-right, bottom-left and bottom-right copies. The threshold is then (number + 0.5) / 64.

**4.**

```cpp
for (int y = 0; y < image.height(); ++y) {
    const bool leftToRight = (y % 2 == 0);
    const int step = leftToRight ? 1 : -1;
    for (int n = 0; n < image.width(); ++n) {
        const int x = leftToRight ? n : image.width() - 1 - n;
        const ColourF old = work.data[y * work.width + x];
        const int k = nearestIndex(old, values);
        out.setPixel(x, y, palette[k]);
        const ColourF error = old - values[k];
        addError(work, x + step, y, error, 7.0 / 16.0);
        addError(work, x - step, y + 1, error, 3.0 / 16.0);
        addError(work, x, y + 1, error, 5.0 / 16.0);
        addError(work, x + step, y + 1, error, 1.0 / 16.0);
    }
}
```

> "Ahead" is now +1 or −1 depending on the direction: `step`.

**5.**
> Only the four levels **0, 85, 170 and 255**. Between two levels the pixels are a mix of the lower and the higher one, so from a distance the ramp is smooth.

**6.**

```cpp
const std::vector<Colour> greens = {Colour{15, 56, 15}, Colour{48, 98, 48}, Colour{139, 172, 15},
                                    Colour{155, 188, 15}};
const Image handheld = floydSteinberg(greyScene, greens);
```

> The picture becomes green, and its brightness is made from the four greens — dark scene parts from the two dark ones, the sky from the light ones. (Two of the greens are close together, so the very light parts look a little flat.)

**7.**
> Ordered dithering needs only the pixel's own value and its threshold, which depends only on (x, y). Floyd–Steinberg's value at a pixel includes errors from pixels before it — which include errors from pixels before **them**, and so on. So the pixels must be done in order, one after another.

**8.**

```cpp
addError(work, x + 1, y, error, 1.0 / 8.0);
addError(work, x + 2, y, error, 1.0 / 8.0);
addError(work, x - 1, y + 1, error, 1.0 / 8.0);
addError(work, x, y + 1, error, 1.0 / 8.0);
addError(work, x + 1, y + 1, error, 1.0 / 8.0);
addError(work, x, y + 2, error, 1.0 / 8.0);
```

> A quarter of every error is thrown away, so very light areas become pure white and very dark areas pure black: more contrast, cleaner-looking, but some shading is lost near both ends.

---

## Summary

🧠 With few colours, **posterising** (nearest colour) loses the shading. **Dithering** mixes allowed colours in fine patterns so that the **average** looks right.

🧠 The eye averages **light**: dither in linear light. Grey 128 needs about 22 % white dots, not 50 %.

🧠 **Ordered dithering** uses a different threshold at each pixel, from the **Bayer matrix**: each pixel is decided alone, in a regular pattern.

🧠 **Error diffusion** passes each pixel's rounding error on; **Floyd–Steinberg** gives 7/16, 3/16, 5/16 and 1/16 to the four pixels ahead. Irregular dots, more detail.

🧠 The **nearest colour** is the one with the smallest distance √(dr² + dg² + db²) in the RGB cube; compare squared distances.

---

## Next chapter

So far, every change kept each pixel where it was. In Chapter 53 we **move** pixels: **warping** bends a picture like a rubber sheet — swirls, waves, ripples, a fish-eye lens. The trick is Chapter 31's "work backwards": for each pixel of the new picture, ask where it came **from** in the old one, and read the colour there with Chapter 35's bilinear sampling.
