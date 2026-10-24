# Chapter 51 — Sharpen and Edge Detection (Sobel)

> **Part 7 · Chapter 51 of 82**
> **You need:** Chapters 1–50 (especially 15, 16, 29, 30, 47, 49 and 50) · **You will make:** `edges.h` (a grey picture made of doubles, sharpening, the unsharp mask, the Sobel and Laplacian kernels, edge strength and direction), and `edges.png`: one scene sharpened, over-sharpened, and turned into five kinds of edge picture

---

## What you will learn

- How to **sharpen** a picture: find the detail (original − blurred) and add it back, stronger.
- Why the sharpen kernel `0 −1 0 / −1 5 −1 / 0 −1 0` works, and why sharpening makes **halos**.
- The **unsharp mask**, the sharpening tool in every photo program.
- How to find **edges** with the two **Sobel** kernels, and why we must keep **negative** numbers.
- The edge **strength** (Pythagoras) and the edge **direction** (atan2), and how to draw both.
- Why you should **blur before** looking for edges, and what the **Laplacian** finds.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **sharpen** | Make edges and small details stand out more. |
| **detail** | What a blur takes away: original − blurred. |
| **halo** | A light or dark rim beside an edge, made by sharpening. |
| **unsharp mask** | Sharpening by adding back (original − blurred) × amount. |
| **gradient** | How fast, and in which direction, the brightness changes at a pixel. |
| **Sobel kernels** | Two 3 × 3 kernels that measure the change across (Gx) and down (Gy). |
| **edge strength** | How big the change is: √(gx² + gy²). |
| **edge map** | A black-and-white picture: white where the edge strength is big. |
| **Laplacian** | A kernel that compares a pixel with the average of its neighbours. |

---

## 51.1 The opposite of blur

Chapter 50 blurred pictures: each pixel became an average of its neighbourhood, and fine detail went away. Can we go the other way?

Look at what the blur **took away**:

> **detail = original − blurred**

On a flat area, the blur changes nothing, so the detail is 0. Next to an edge, the blur changes a lot, so the detail is big. The detail is "the part of the picture that is not smooth".

Now add the detail back, more strongly:

> **sharpened = original + amount × detail = original + amount × (original − blurred)**

📖 **New word: sharpen** — make edges and small details stand out more. A sharpened picture is not more **correct** (lost detail cannot really come back); it only **looks** crisper, because our eyes judge sharpness by how strong the edges are.

🔢 **Maths: a row with an edge**

> The row: **100 100 100 160 160 160** (a step from dark grey to lighter grey).
> Blur with a 3-pixel box (Chapter 49), at the two pixels beside the step:
> x = 2: (100 + 100 + 160) / 3 = **120** → detail = 100 − 120 = **−20**
> x = 3: (100 + 160 + 160) / 3 = **140** → detail = 160 − 140 = **+20**
> Everywhere else, the detail is 0.
> Sharpened, amount 1: x = 2: 100 + (−20) = **80**; x = 3: 160 + 20 = **180**.

```
original:   100 100 100 160 160 160
sharpened:  100 100  80 180 160 160
```

The dark side of the step got **darker**, the bright side got **brighter**. The step is now 100 (80 → 180) instead of 60 (100 → 160): it looks sharper.

---

## 51.2 The sharpen kernel

The idea of Section 51.1 fits into one 3 × 3 kernel:

```
    0  −1   0
   −1   5  −1
    0  −1   0
```

🔢 **Maths: why 5 and −1?**

> new = 5c − (up + down + left + right)
> = c + 4c − (up + down + left + right)
> = c + 4 × (c − (up + down + left + right) / 4)
> = **original + 4 × (original − average of the 4 neighbours)**

It is exactly Section 51.1, with "blurred" = the average of the four neighbours and amount = 4.

🧠 **Check the sum:** 5 − 1 − 1 − 1 − 1 = **1**. The weights add up to 1, so flat areas keep their brightness (Chapter 49's rule).

🔢 **Maths: the row again**

The program's row is only 1 pixel high, so "up" and "down" (clamped, Chapter 49) are the pixel itself: new = 5c − c − c − left − right = 3c − left − right.

> x = 1: 300 − 100 − 100 = **100** (flat: no change)
> x = 2: 300 − 100 − 160 = **40**
> x = 3: 480 − 100 − 160 = **220**
> x = 4: 480 − 160 − 160 = **160**

```
edge 100 -> 160, sharpen kernel:   100 100 40 220 160 160
```

📖 **New word: halo** — the dip to 40 and the bump to 220 are thin dark and light rims along the edge. A little halo looks crisp. Too much looks like a glowing outline — the typical sign of an over-sharpened photo.

⚠️ **Clamping.** With a stronger edge the rims leave the 0 … 255 range:

> row 50 50 50 200 200 200: x = 2: 150 − 50 − 200 = **−100** → 0; x = 3: 600 − 50 − 200 = **350** → 255

```
edge 50 -> 200, sharpen kernel:    50 50 0 255 200 200
```

The halos are now pure black and pure white. Clamping cannot be avoided in the final picture — but it is one more reason to sharpen gently.

💡 The sharpen kernel is also "identity minus Laplacian": `0 0 0 / 0 1 0 / 0 0 0` − `0 1 0 / 1 −4 1 / 0 1 0` = `0 −1 0 / −1 5 −1 / 0 −1 0`. We meet the Laplacian properly in Section 51.10.

---

## 51.3 The unsharp mask

The sharpen kernel is fixed: its "blur" is always the 4 neighbours, and its amount is always 4. Photo programs give you three controls instead.

📖 **New word: unsharp mask** — sharpened = original + amount × (original − **Gaussian blur**(original)). The strange name comes from old photo darkrooms: a slightly **unsharp** (blurred) copy of the negative was used as a **mask** to make the print look sharper.

| Control | What it does |
|---|---|
| **radius** (σ of the blur) | How wide the halos are. Small σ (0.5–1) sharpens fine detail; big σ (5–20) adds "punch" to big shapes. |
| **amount** | How strong the halos are. 0.5 to 1.5 is usual; 0 means no change. |
| threshold (optional) | Only sharpen where the detail is bigger than this, so that smooth skin or sky is left alone (Practice 4). |

🔢 **Maths: σ = 1, amount 1, on our row**

The Gaussian with σ = 1 (Chapter 50) reaches 3 pixels on each side, so the blurred row is a soft ramp: about 100.3 103.5 118.0 142.0 156.5 159.7. Then 2 × original − blurred:

> x = 1: 200 − 103.5 = 96.5 → **96**; x = 2: 200 − 118.0 = **82**; x = 3: 320 − 142.0 = **178**; x = 4: 320 − 156.5 = 163.5 → **164**

```
unsharp mask, sigma 1, amount 1:   100 96 82 178 164 160
```

The halos are wider and softer than the kernel's (40 and 220): they fade over two pixels. That usually looks more natural.

### Sharpen in sRGB values or in linear light?

Chapter 50 said: **blur** in linear light. Is it the same for sharpening? The program tries both:

```
unsharp mask, sigma 1, amount 1:   100 96 82 178 164 160
the same in linear light:          100 95 69 173 163 160
```

In sRGB values the halos are **balanced**: 18 below the dark side (100 → 82) and 18 above the bright side (160 → 178). In linear light they are not: 31 below, only 13 above. The dark rim is much heavier, and dark halos are the ugliest kind.

Why the difference? Blurring is **mixing light**, and light mixes in linear light. Sharpening is not mixing anything: it makes **differences that we see** bigger. sRGB values are spaced roughly the way our eyes see brightness (Chapter 17), so equal steps in sRGB look equal. That is why `unsharpMask` works on **sRGB values by default** (`linearLight = false`), and most photo programs do the same.

---

## 51.4 Sharpening sharpens everything

The unsharp mask cannot tell a real edge from **noise** — little random speckles in a photo (or grain, or the blocks of a badly compressed file). Noise is also "detail that is not smooth", so it gets stronger too.

That is why:

- **sharpen last**, after other changes (and after shrinking: shrinking itself averages noise away);
- keep the **amount small** on noisy pictures;
- the **threshold** control exists: tiny differences (noise) are left alone, big ones (edges) are sharpened.

---

## 51.5 Edges: where the brightness changes

Now a different question. Not "make edges stronger" but "**where are** the edges?" A program that finds edges can trace outlines, find objects, or make a drawing out of a photo.

An edge is a place where the brightness **changes quickly**. Chapter 20 measured change with the **slope**: how much y changes for one step in x. Here: how much the brightness changes for one step across the picture.

Chapter 49 already had a kernel for that — the **difference** kernel, right − left:

```
difference kernel (right - left):
     0  90  90   0   0
```

It lights up beside the edge and is 0 on flat areas (its weights add up to 0). But it looks at only **one** row, so a single noisy pixel in that row fools it completely.

📖 **New word: Sobel kernels** — Irwin Sobel's improvement (1968): take the difference across, but in **three rows**, and give the middle row twice the weight:

```
Gx (change across):        Gy (change down):
   −1   0   1                 −1  −2  −1
   −2   0   2                  0   0   0
   −1   0   1                  1   2   1
```

🔢 **Maths: Sobel is "difference × small blur"**

> Gx = the column (1, 2, 1) times the row (−1, 0, 1):
> row 1: 1 × (−1 0 1) = −1 0 1
> row 2: 2 × (−1 0 1) = −2 0 2
> row 3: 1 × (−1 0 1) = −1 0 1
> So Gx is **separable** (Chapter 50): a difference across, and a little blur (1 2 1) down. The blur part calms the noise; the difference part finds the change. Gy is the same, turned by 90°.

All the weights of Gx add up to 0 (−1 − 2 − 1 + 1 + 2 + 1), so a flat area gives exactly 0.

🔢 **Maths: Gx on the edge grid**

The grid of Chapter 49: columns 0 and 1 are 0, columns 2, 3 and 4 are 90. At (1, 2), the left column is column 0 (all 0) and the right column is column 2 (all 90):

> gx = (−1 × 0 + 1 × 90) + (−2 × 0 + 2 × 90) + (−1 × 0 + 1 × 90) = 90 + 180 + 90 = **360**
> At (2, 2): left column 1 (0), right column 3 (90) → also **360**
> At (3, 2): left and right are both 90 → **0**

```
edge grid, Sobel x:        0 360 360 0 0
edge grid, Sobel y:        0 0 0 0 0
```

Gy is 0 everywhere: nothing changes going **down** this grid. Gx gives 360 = 4 × 90 because its positive weights add up to 4 (1 + 2 + 1).

🧠 **The biggest possible value:** a jump from 0 to 255 gives gx = 4 × 255 = **1020**. So edge values are not bytes — they need a bigger range.

---

## 51.6 Keep the negative numbers

Turn the edge round: bright on the left, dark on the right. Now right − left is **negative**:

```
flipped edge, Sobel x:     0 -360 -360 0 0
the same, kept as bytes:   0 0 0 0 0
```

If we stored the result as bytes (as Chapter 49's `convolve` does), −360 would be clamped to **0** — and the edge would vanish completely. Chapter 49 (Section 49.8) promised to fix this, and here is how: we do edge maths on a picture made of **doubles**, not bytes.

`GreyF` is that picture: a width, a height, and one `double` per pixel. Two decisions:

- **Grey, not colour.** An edge is a change in brightness, so one number per pixel is enough. `toGreyF` uses Chapter 15's `luma`.
- **The scale 0 … 255.** We keep grey values in the same range as bytes (luma × 255), so that the worked numbers stay easy: a 0 → 90 step gives 360, not 1.41.

The values in a `GreyF` can be anything: −360, 1020, 0.5. Only at the very end, when we want to **look** at them, do we turn them into a picture (Section 51.8).

💡 Why sRGB values again, not linear light? For the same reason as sharpening (Section 51.3): an edge is a difference **we see**, and sRGB values are spaced the way we see.

---

## 51.7 Edge strength and edge direction

At each pixel we now have two numbers: **gx** (the change across) and **gy** (the change down). Together they are an arrow — a 2D vector (Chapter 29) — pointing the way the brightness grows fastest.

📖 **New word: gradient** — that arrow (gx, gy). Its length says **how strong** the edge is; its angle says **which way** it faces.

📖 **New word: edge strength** — the length of the arrow, by Pythagoras (Chapter 29):

> **strength = √(gx² + gy²)**

🔢 **Maths: a diagonal edge**

The program's fourth grid has 90 where x + y ≥ 5, and 0 elsewhere — a staircase going diagonally. Around the centre (2, 2):

```
           x = 1   x = 2   x = 3
  y = 1:     0       0       0
  y = 2:     0       0      90
  y = 3:     0      90      90
```

> gx = (−1 × 0 + 1 × 0) + (−2 × 0 + 2 × 90) + (−1 × 0 + 1 × 90) = 180 + 90 = **270**
> gy = (−1 × 0 − 2 × 0 − 1 × 0) + (1 × 0 + 2 × 90 + 1 × 90) = 180 + 90 = **270**
> strength = √(270² + 270²) = √145,800 = **381.8**

Neither gx nor gy alone is the whole story: each is only 270, but together the edge is as strong as 381.8.

🔢 **Maths: the direction**

> **direction = atan2(gy, gx)** (Chapter 30) = atan2(270, 270) = **45°**

```
diagonal edge, centre: gx 270, gy 270, strength 381.8, direction 45 degrees
directions: edge grid 0, flipped 180
```

⚠️ **y goes down.** In a picture, y grows downwards (Chapter 3), so 45° means **down and to the right** — towards the bright corner. 90° means "brighter below". The arrow always points from dark to bright, and it is at a **right angle** to the edge line itself: the staircase runs from bottom-left to top-right, the arrow points bottom-right.

The edge grid (dark left, bright right) gives 0°: pointing right. The flipped grid gives 180°: pointing left. That is exactly the information the clamped bytes threw away.

`directionDegrees` uses `wrapHue` (Chapter 16) to turn atan2's −180° … 180° into 0° … 360°. Why a hue function? Because we will show directions **as hues**.

---

## 51.8 Looking at edge numbers

Edge numbers are not colours. To see them, we choose how to turn them into bytes. `greyFToImage(g, scale, offset)` makes each value into the grey byte **offset + scale × value** (clamped).

| What we show | How | Looks like |
|---|---|---|
| **gx** (signed) | offset 128, scale 0.25: 0 → mid grey, +1020 → white, −1020 → black | a grey picture whose edges look raised or sunk, like a stamp |
| **strength** | scale 255 / largest strength: the strongest edge → white | white outlines on black |
| **edge map** | white where strength ≥ a level, black elsewhere | a black-and-white drawing |
| **direction** | hue = direction, brightness = strength | coloured outlines |

📖 **New word: edge map** — Chapter 47's **threshold**, applied to the edge strength. The program uses a level of 0.25 × the largest strength: anything at least a quarter as strong as the strongest edge counts as an edge.

**Direction as colour.** `directionColours` makes an HSV colour (Chapter 16): hue = the direction in degrees, saturation 1, value = strength / largest. So:

| Direction | Means | Hue |
|---|---|---|
| 0° | brighter to the right | red |
| 90° | brighter below | yellow-green |
| 180° | brighter to the left | cyan |
| 270° | brighter above | blue-violet |

Flat areas have strength 0, so their value is 0: black. The two sides of the sun come out in opposite colours — the left rim faces one way, the right rim the other way.

---

## 51.9 Blur first

Real pictures have noise, and Sobel is a difference: it reacts to every speckle. The program makes a 64 × 64 test picture: left half 80, right half 160 (a real edge, 2 columns wide in Sobel's eyes: 2 × 64 = 128 pixels), plus a fixed pattern of noise from −18 to +18.

```
noisy edge, pixels with strength >= 100: 920 without blur, 192 after a blur (the real edge: 2 x 64 = 128)
```

Without a blur, 920 pixels look like edges — most of them are noise. After a Gaussian blur with σ = 1 (Chapter 50), the noise is averaged down and only **192** pixels pass: three full columns, all of them along the real edge. (The blur also made the edge itself a bit wider: 3 columns instead of 2. You cannot have everything: more blur, less noise, but softer edges.)

🧠 **The usual recipe:** grey → small blur → Sobel → strength → threshold. (Famous edge detectors, like John Canny's, add one more step: **thinning** the edge to 1 pixel. Practice 8 tries it.)

---

## 51.10 The Laplacian

Sobel measures the **slope** of the brightness. The **Laplacian** of Chapter 49 (Practice 3) measures something else:

```
    0   1   0
    1  −4   1
    0   1   0
```

📖 **New word: Laplacian** — up + down + left + right − 4 × centre = 4 × (average of the 4 neighbours − centre). It is 0 on a flat area **and** on a smooth ramp (on a straight slope, the left neighbour is as much below as the right one is above). It only reacts where the slope **changes** — mathematicians call this the **second derivative**, "the change of the change".

Kept as doubles, the negative values survive this time:

```
dot grid, Laplacian:       0 90 -360 90 0
edge grid, Laplacian:      0 90 -90 0 0
```

> the dot: at the centre 4 × 0 − 4 × 90 = **−360**; beside it, one neighbour is 90 → **90**
> the edge: at column 1, the right neighbour is 90 → **+90**; at column 2, the left neighbour is 0 and the other three are 90 → 90 + 90 + 90 + 0 − 360 = **−90**

At the edge, the Laplacian goes from **+90 to −90**. The edge itself is where it **crosses zero** — between columns 1 and 2, exactly where the step is. A zero-crossing gives a thin, precise edge position, but the Laplacian is even more sensitive to noise than Sobel (no blur built in), so it is almost always used after a Gaussian blur ("Laplacian of Gaussian").

The program shows it like gx: 128 + value, so zero is mid grey and both signs are visible.

---

## Code, part 1: `edges.h`

File: `common/edges.h` (new). It includes `blur.h` (kernels, `PixelsF` and the Gaussian, Chapters 49 and 50) and `hsv.h` (hues, Chapter 16).

```cpp
#ifndef EDGES_H
#define EDGES_H

#include <algorithm>
#include <cmath>
#include <vector>
#include "blur.h"
#include "hsv.h"

struct GreyF {
    int width = 0;
    int height = 0;
    std::vector<double> data;
};

inline GreyF makeGreyF(int width, int height) {
    return GreyF{width, height, std::vector<double>(width * height, 0.0)};
}

inline double greyAt(const GreyF& g, int x, int y) {
    const int cx = std::clamp(x, 0, g.width - 1);
    const int cy = std::clamp(y, 0, g.height - 1);
    return g.data[cy * g.width + cx];
}

inline GreyF toGreyF(const Image& image) {
    GreyF g = makeGreyF(image.width(), image.height());
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            g.data[y * g.width + x] = 255.0 * luma(toColourF(image.getPixel(x, y)));
        }
    }
    return g;
}

inline GreyF convolveGrey(const GreyF& src, const Kernel& k) {
    const int r = k.size / 2;
    GreyF out = makeGreyF(src.width, src.height);
    for (int y = 0; y < src.height; ++y) {
        for (int x = 0; x < src.width; ++x) {
            double sum = 0.0;
            for (int j = 0; j < k.size; ++j) {
                for (int i = 0; i < k.size; ++i) {
                    sum += k.weights[j * k.size + i] * greyAt(src, x + i - r, y + j - r);
                }
            }
            out.data[y * src.width + x] = sum;
        }
    }
    return out;
}

inline Kernel sharpenKernel() {
    return Kernel{3, {0, -1, 0, -1, 5, -1, 0, -1, 0}};
}

inline Kernel laplacianKernel() {
    return Kernel{3, {0, 1, 0, 1, -4, 1, 0, 1, 0}};
}

inline Kernel sobelX() {
    return Kernel{3, {-1, 0, 1, -2, 0, 2, -1, 0, 1}};
}

inline Kernel sobelY() {
    return Kernel{3, {-1, -2, -1, 0, 0, 0, 1, 2, 1}};
}

inline GreyF magnitudeOf(const GreyF& gx, const GreyF& gy) {
    GreyF m = makeGreyF(gx.width, gx.height);
    for (int i = 0; i < static_cast<int>(m.data.size()); ++i) {
        m.data[i] = std::sqrt(gx.data[i] * gx.data[i] + gy.data[i] * gy.data[i]);
    }
    return m;
}

inline GreyF sobelMagnitude(const GreyF& g) {
    return magnitudeOf(convolveGrey(g, sobelX()), convolveGrey(g, sobelY()));
}

inline double directionDegrees(double gx, double gy) {
    return wrapHue(radiansToDegrees(std::atan2(gy, gx)));
}

inline double largestValue(const GreyF& g) {
    double largest = 0.0;
    for (double v : g.data) {
        largest = std::max(largest, std::fabs(v));
    }
    return largest;
}

inline Image greyFToImage(const GreyF& g, double scale, double offset = 0.0) {
    Image image(g.width, g.height);
    for (int y = 0; y < g.height; ++y) {
        for (int x = 0; x < g.width; ++x) {
            const std::uint8_t v = clampByte(offset + scale * g.data[y * g.width + x]);
            image.setPixel(x, y, Colour{v, v, v});
        }
    }
    return image;
}

inline Image edgeMap(const GreyF& magnitude, double level) {
    Image image(magnitude.width, magnitude.height);
    for (int y = 0; y < magnitude.height; ++y) {
        for (int x = 0; x < magnitude.width; ++x) {
            const bool edge = magnitude.data[y * magnitude.width + x] >= level;
            image.setPixel(x, y, edge ? colours::white : colours::black);
        }
    }
    return image;
}

inline Image directionColours(const GreyF& gx, const GreyF& gy, double largest) {
    Image image(gx.width, gx.height);
    for (int y = 0; y < gx.height; ++y) {
        for (int x = 0; x < gx.width; ++x) {
            const double a = gx.data[y * gx.width + x];
            const double b = gy.data[y * gx.width + x];
            const double strength = std::min(1.0, std::sqrt(a * a + b * b) / largest);
            image.setPixel(x, y, toColour(hsvToRgb(HSV{directionDegrees(a, b), 1.0, strength})));
        }
    }
    return image;
}

inline Image unsharpMask(const Image& image, double sigma, double amount, bool linearLight = false) {
    const std::vector<double> w = gaussianWeights(sigma);
    const PixelsF sharp = toPixelsF(image, linearLight);
    const PixelsF soft = blurColumns(blurRows(sharp, w, EdgeMode::Clamp), w, EdgeMode::Clamp);
    PixelsF out = sharp;
    for (int i = 0; i < static_cast<int>(out.data.size()); ++i) {
        out.data[i] = sharp.data[i] + (sharp.data[i] - soft.data[i]) * amount;
    }
    return fromPixelsF(out, linearLight);
}

#endif
```

### Line by line

**A grey picture of doubles (lines 1–51)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–8 | include guard and `#include` lines | `std::clamp`/`std::max`, `std::sqrt`/`std::atan2`, lists, the blur header, and the HSV header. |
| 10–14 | `struct GreyF { int width = 0; int height = 0; std::vector<double> data; };` | One `double` per pixel, row by row (index y × width + x), so values can be negative or bigger than 255 (Section 51.6). |
| 16–18 | `inline GreyF makeGreyF(int width, int height) { return GreyF{width, height, std::vector<double>(width * height, 0.0)}; }` | A new grey picture, all 0. |
| 20–24 | `inline double greyAt(const GreyF& g, int x, int y) { const int cx = std::clamp(x, 0, g.width - 1); const int cy = std::clamp(y, 0, g.height - 1); return g.data[cy * g.width + cx]; }` | Read a value; outside the picture, use the nearest edge pixel (Clamp, Chapter 49). |
| 26–34 | `inline GreyF toGreyF(const Image& image) { ... g.data[y * g.width + x] = 255.0 * luma(toColourF(image.getPixel(x, y))); ... }` | Colour → grey, with Chapter 15's `luma`, on the scale 0 … 255. |
| 36–41 | `inline GreyF convolveGrey(const GreyF& src, const Kernel& k) { const int r = k.size / 2; GreyF out = makeGreyF(src.width, src.height); for (y) { for (x) { double sum = 0.0;` | Chapter 49's convolution, for grey doubles. A new picture `out` (never in place). |
| 42–46 | `for (int j = 0; j < k.size; ++j) { for (int i = 0; i < k.size; ++i) { sum += k.weights[j * k.size + i] * greyAt(src, x + i - r, y + j - r); } }` | The sum of weight × value over the kernel (Chapter 49's formula). |
| 47–51 | `out.data[y * src.width + x] = sum;` … `return out;` `}` | Store the sum **as it is**: no rounding, no clamping. |

**The kernels (lines 53–67)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 53–55 | `inline Kernel sharpenKernel() { return Kernel{3, {0, -1, 0, -1, 5, -1, 0, -1, 0}}; }` | Section 51.2. Weights add up to 1. |
| 57–59 | `inline Kernel laplacianKernel() { return Kernel{3, {0, 1, 0, 1, -4, 1, 0, 1, 0}}; }` | Section 51.10. Weights add up to 0. |
| 61–63 | `inline Kernel sobelX() { return Kernel{3, {-1, 0, 1, -2, 0, 2, -1, 0, 1}}; }` | Section 51.5: right − left, middle row counted twice. |
| 65–67 | `inline Kernel sobelY() { return Kernel{3, {-1, -2, -1, 0, 0, 0, 1, 2, 1}}; }` | Below − above. |

**Strength and direction (lines 69–91)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 69–75 | `inline GreyF magnitudeOf(const GreyF& gx, const GreyF& gy) { GreyF m = ...; for (int i = 0; i < static_cast<int>(m.data.size()); ++i) { m.data[i] = std::sqrt(gx.data[i] * gx.data[i] + gy.data[i] * gy.data[i]); } return m; }` | The strength √(gx² + gy²) of every pixel (Section 51.7). Both pictures have the same size, so one index `i` walks through all three. |
| 77–79 | `inline GreyF sobelMagnitude(const GreyF& g) { return magnitudeOf(convolveGrey(g, sobelX()), convolveGrey(g, sobelY())); }` | Everything in one call: Gx, Gy, strength. |
| 81–83 | `inline double directionDegrees(double gx, double gy) { return wrapHue(radiansToDegrees(std::atan2(gy, gx))); }` | atan2 gives −180° … 180° (in radians); Chapter 30's `radiansToDegrees` and Chapter 16's `wrapHue` make it 0° … 360°. Note the order: **gy first**. |
| 85–91 | `inline double largestValue(const GreyF& g) { double largest = 0.0; for (double v : g.data) { largest = std::max(largest, std::fabs(v)); } return largest; }` | The biggest value, ignoring the sign (`std::fabs` = absolute value of a double). |

**Turning numbers into pictures (lines 93–126)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 93–102 | `inline Image greyFToImage(const GreyF& g, double scale, double offset = 0.0) { ... const std::uint8_t v = clampByte(offset + scale * g.data[y * g.width + x]); image.setPixel(x, y, Colour{v, v, v}); ... }` | offset + scale × value, clamped and rounded by Chapter 47's `clampByte`. Offset 128 shows signed values (Section 51.8). |
| 104–113 | `inline Image edgeMap(const GreyF& magnitude, double level) { ... const bool edge = magnitude.data[y * magnitude.width + x] >= level; image.setPixel(x, y, edge ? colours::white : colours::black); ... }` | The threshold of Chapter 47: white for edges, black for the rest. |
| 115–121 | `inline Image directionColours(const GreyF& gx, const GreyF& gy, double largest) { ... const double a = gx.data[...]; const double b = gy.data[...]; const double strength = std::min(1.0, std::sqrt(a * a + b * b) / largest);` | For each pixel: its gx and gy, and its strength as a part of the largest (0 … 1). |
| 122–126 | `image.setPixel(x, y, toColour(hsvToRgb(HSV{directionDegrees(a, b), 1.0, strength})));` … `return image; }` | Hue = direction, full saturation, value = strength (Chapter 16's `hsvToRgb`). |

**The unsharp mask (lines 128–139)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 128–131 | `inline Image unsharpMask(const Image& image, double sigma, double amount, bool linearLight = false) { const std::vector<double> w = gaussianWeights(sigma); const PixelsF sharp = toPixelsF(image, linearLight); const PixelsF soft = blurColumns(blurRows(sharp, w, EdgeMode::Clamp), w, EdgeMode::Clamp);` | The original as doubles (`sharp`) and its Gaussian blur (`soft`), with Chapter 50's two passes. sRGB values by default (Section 51.3). |
| 132–135 | `PixelsF out = sharp; for (int i = 0; ...; ++i) { out.data[i] = sharp.data[i] + (sharp.data[i] - soft.data[i]) * amount; }` | original + amount × (original − blurred), for all three channels at once (Chapter 14's `ColourF` operators). |
| 136–137 | `return fromPixelsF(out, linearLight);` `}` | Back to bytes; this is where the halos may be clamped. |
| 139 | `#endif` | End of the include guard. |

---

## Code, part 2: sharpening and edges

File: `ch51/edges.cpp`

```cpp
#include <cmath>
#include <iostream>
#include <string>
#include <vector>
#include "edges.h"
#include "deflate.h"

std::string oneDecimal(double v) {
    const long long n = std::llround(v * 10.0);
    return std::to_string(n / 10) + "." + std::to_string(n % 10);
}

void printRow(const std::string& label, const Image& image) {
    std::cout << label;
    for (int x = 0; x < image.width(); ++x) {
        std::cout << " " << static_cast<int>(image.getPixel(x, 0).r);
    }
    std::cout << "\n";
}

void printGreyRow(const std::string& label, const GreyF& g, int y) {
    std::cout << label;
    for (int x = 0; x < g.width; ++x) {
        std::cout << " " << std::llround(g.data[y * g.width + x]);
    }
    std::cout << "\n";
}

Image makeRow(const std::vector<int>& values) {
    Image row(static_cast<int>(values.size()), 1);
    for (int x = 0; x < row.width(); ++x) {
        const std::uint8_t v = static_cast<std::uint8_t>(values[x]);
        row.setPixel(x, 0, Colour{v, v, v});
    }
    return row;
}

double gridValue(const std::string& kind, int x, int y) {
    if (kind == "dot") {
        return (x == 2 && y == 2) ? 90.0 : 0.0;
    }
    if (kind == "edge") {
        return (x >= 2) ? 90.0 : 0.0;
    }
    if (kind == "flipped") {
        return (x >= 2) ? 0.0 : 90.0;
    }
    return (x + y >= 5) ? 90.0 : 0.0;
}

GreyF makeGrid(const std::string& kind) {
    GreyF g = makeGreyF(5, 5);
    for (int y = 0; y < 5; ++y) {
        for (int x = 0; x < 5; ++x) {
            g.data[y * 5 + x] = gridValue(kind, x, y);
        }
    }
    return g;
}

Image makeNoisy() {
    Image noisy(64, 64);
    for (int y = 0; y < 64; ++y) {
        for (int x = 0; x < 64; ++x) {
            const int base = (x < 32) ? 80 : 160;
            const int noise = ((x * 37 + y * 53 + x * y) % 7 - 3) * 6;
            const std::uint8_t v = static_cast<std::uint8_t>(base + noise);
            noisy.setPixel(x, y, Colour{v, v, v});
        }
    }
    return noisy;
}

int countAtLeast(const GreyF& g, double level) {
    int count = 0;
    for (double v : g.data) {
        count += (v >= level) ? 1 : 0;
    }
    return count;
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
    std::cout << "weights add up to: sharpen " << kernelSum(sharpenKernel()) << ", Laplacian "
              << kernelSum(laplacianKernel()) << ", Sobel x " << kernelSum(sobelX()) << "\n";

    const Image gentle = makeRow({100, 100, 100, 160, 160, 160});
    printRow("\nedge 100 -> 160, sharpen kernel:  ", convolve(gentle, sharpenKernel()));
    printRow("unsharp mask, sigma 1, amount 1:  ", unsharpMask(gentle, 1.0, 1.0));
    printRow("the same in linear light:         ", unsharpMask(gentle, 1.0, 1.0, true));
    const Image strong = makeRow({50, 50, 50, 200, 200, 200});
    printRow("edge 50 -> 200, sharpen kernel:   ", convolve(strong, sharpenKernel()));

    const GreyF edge = makeGrid("edge");
    const GreyF flipped = makeGrid("flipped");
    printGreyRow("\nedge grid, Sobel x:       ", convolveGrey(edge, sobelX()), 2);
    printGreyRow("edge grid, Sobel y:       ", convolveGrey(edge, sobelY()), 2);
    printGreyRow("flipped edge, Sobel x:    ", convolveGrey(flipped, sobelX()), 2);
    printRow("the same, kept as bytes:  ", greyFToImage(convolveGrey(flipped, sobelX()), 1.0));

    const GreyF diagonal = makeGrid("diagonal");
    const double gx = convolveGrey(diagonal, sobelX()).data[2 * 5 + 2];
    const double gy = convolveGrey(diagonal, sobelY()).data[2 * 5 + 2];
    std::cout << "diagonal edge, centre: gx " << gx << ", gy " << gy << ", strength "
              << oneDecimal(std::sqrt(gx * gx + gy * gy)) << ", direction "
              << directionDegrees(gx, gy) << " degrees\n";
    std::cout << "directions: edge grid " << directionDegrees(360.0, 0.0) << ", flipped "
              << directionDegrees(-360.0, 0.0) << "\n";

    printGreyRow("\ndot grid, Laplacian:      ", convolveGrey(makeGrid("dot"), laplacianKernel()), 2);
    printGreyRow("edge grid, Laplacian:     ", convolveGrey(edge, laplacianKernel()), 2);

    const Image noisy = makeNoisy();
    const int plain = countAtLeast(sobelMagnitude(toGreyF(noisy)), 100.0);
    const Image smooth = gaussianBlur(noisy, 1.0, EdgeMode::Clamp, false);
    const int blurred = countAtLeast(sobelMagnitude(toGreyF(smooth)), 100.0);
    std::cout << "\nnoisy edge, pixels with strength >= 100: " << plain << " without blur, "
              << blurred << " after a blur (the real edge: 2 x 64 = 128)\n";

    const Image scene = makeScene();
    const GreyF grey = toGreyF(scene);
    const GreyF sx = convolveGrey(grey, sobelX());
    const GreyF sy = convolveGrey(grey, sobelY());
    const GreyF strength = magnitudeOf(sx, sy);
    const double largest = largestValue(strength);
    const Image tiles[8] = {scene,
                            unsharpMask(scene, 1.0, 1.5),
                            unsharpMask(scene, 2.0, 5.0),
                            greyFToImage(sx, 0.25, 128.0),
                            greyFToImage(strength, 255.0 / largest),
                            edgeMap(strength, 0.25 * largest),
                            directionColours(sx, sy, largest),
                            greyFToImage(convolveGrey(grey, laplacianKernel()), 1.0, 128.0)};
    const std::string names[8] = {"original",   "sharpened",  "far too sharp", "Sobel x",
                                  "strength",   "edge map",   "direction",     "Laplacian"};
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
    if (!savePNGCompressed(sheet, "edges.png")) {
        std::cout << "could not write edges.png\n";
        return 1;
    }
    std::cout << "wrote edges.png\n";
    return 0;
}
```

Build and run it from the `code/ch51` folder:

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common edges.cpp -o edges
./edges
```

### Line by line

**Helpers (lines 1–96)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–6 | the `#include` lines | `std::llround` and `std::sqrt`, printing, strings, lists, the new header, and `deflate.h` for the PNG. |
| 8–11 | `std::string oneDecimal(double v) { const long long n = std::llround(v * 10.0); return std::to_string(n / 10) + "." + std::to_string(n % 10); }` | 381.838 → n = 3818 → "381" + "." + "8". (Only for values that are not negative.) |
| 13–19 | `void printRow(const std::string& label, const Image& image) { ... image.getPixel(x, 0).r ... }` | Print row 0 of a picture (the red values; our test rows are grey). |
| 21–27 | `void printGreyRow(const std::string& label, const GreyF& g, int y) { ... std::llround(g.data[y * g.width + x]) ... }` | Print one row of a grey picture, rounded to whole numbers — **with** their signs. |
| 29–36 | `Image makeRow(const std::vector<int>& values) { Image row(static_cast<int>(values.size()), 1); ... row.setPixel(x, 0, Colour{v, v, v}); ... }` | A grey picture 1 pixel high, from a list of numbers. |
| 38–49 | `double gridValue(const std::string& kind, int x, int y) { if (kind == "dot") { return (x == 2 && y == 2) ? 90.0 : 0.0; } if (kind == "edge") { ... } if (kind == "flipped") { ... } return (x + y >= 5) ? 90.0 : 0.0; }` | The value of one cell in one of four little test grids: Chapter 49's dot and edge, the flipped edge, and the diagonal. |
| 51–59 | `GreyF makeGrid(const std::string& kind) { GreyF g = makeGreyF(5, 5); ... g.data[y * 5 + x] = gridValue(kind, x, y); ... }` | Build a 5 × 5 grid of that kind. |
| 61–72 | `Image makeNoisy() { ... const int base = (x < 32) ? 80 : 160; const int noise = ((x * 37 + y * 53 + x * y) % 7 - 3) * 6; ...` | The noisy edge of Section 51.9. The noise is a fixed pattern (we have no random numbers until Chapter 54): x × 37 + y × 53 + x × y, remainder after dividing by 7 (0 … 6), minus 3 (−3 … 3), times 6 (−18 … 18). |
| 74–80 | `int countAtLeast(const GreyF& g, double level) { int count = 0; for (double v : g.data) { count += (v >= level) ? 1 : 0; } return count; }` | How many values are at least `level`. |
| 82–96 | `Image makeScene() { ... }` | Chapter 47's scene. |

**Sharpening (lines 99–107)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 99–100 | `std::cout << "weights add up to: sharpen " << kernelSum(sharpenKernel()) << ...` | Chapter 49's `kernelSum`: 1, 0 and 0. |
| 102–105 | `const Image gentle = makeRow({100, 100, 100, 160, 160, 160}); printRow(..., convolve(gentle, sharpenKernel())); printRow(..., unsharpMask(gentle, 1.0, 1.0)); printRow(..., unsharpMask(gentle, 1.0, 1.0, true));` | The row of Sections 51.2 and 51.3: kernel, unsharp mask, and unsharp mask in linear light. Chapter 49's `convolve` is fine here because sharpened values are wanted as bytes. |
| 106–107 | `const Image strong = makeRow({50, 50, 50, 200, 200, 200}); printRow(..., convolve(strong, sharpenKernel()));` | The stronger edge, with clamped halos. |

**Sobel and the Laplacian (lines 109–126)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 109–113 | `const GreyF edge = makeGrid("edge"); const GreyF flipped = makeGrid("flipped"); printGreyRow(..., convolveGrey(edge, sobelX()), 2); ...` | Gx and Gy on the edge, and Gx on the flipped edge — middle row (y = 2) only; the other rows are the same. |
| 114 | `printRow("the same, kept as bytes:  ", greyFToImage(convolveGrey(flipped, sobelX()), 1.0));` | What would happen with bytes: −360 → 0 (Section 51.6). |
| 116–121 | `const GreyF diagonal = makeGrid("diagonal"); const double gx = convolveGrey(diagonal, sobelX()).data[2 * 5 + 2]; const double gy = ...; std::cout << ... oneDecimal(std::sqrt(gx * gx + gy * gy)) << ... directionDegrees(gx, gy) ...` | The centre pixel (2, 2) of the diagonal: index 2 × 5 + 2 = 12. Strength and direction (Section 51.7). |
| 122–123 | `std::cout << "directions: edge grid " << directionDegrees(360.0, 0.0) << ", flipped " << directionDegrees(-360.0, 0.0) << "\n";` | The directions of the two straight edges, from their gx (360 and −360) and gy (0). |
| 125–126 | `printGreyRow(..., convolveGrey(makeGrid("dot"), laplacianKernel()), 2); printGreyRow(..., convolveGrey(edge, laplacianKernel()), 2);` | The Laplacian, negative values kept (Section 51.10). |

**Noise (lines 128–133)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 128–131 | `const Image noisy = makeNoisy(); const int plain = countAtLeast(sobelMagnitude(toGreyF(noisy)), 100.0); const Image smooth = gaussianBlur(noisy, 1.0, EdgeMode::Clamp, false); const int blurred = countAtLeast(sobelMagnitude(toGreyF(smooth)), 100.0);` | Edge pixels (strength ≥ 100) without and with a blur first (Section 51.9). The blur works on sRGB values, like the rest of the edge maths. |
| 132–133 | `std::cout << ... plain << ... blurred << ...` | Print both counts. |

**The picture (lines 135–168)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 135–140 | `const Image scene = makeScene(); const GreyF grey = toGreyF(scene); const GreyF sx = convolveGrey(grey, sobelX()); const GreyF sy = ...; const GreyF strength = magnitudeOf(sx, sy); const double largest = largestValue(strength);` | The scene's grey version, Gx, Gy, strength, and the strongest edge. |
| 141–148 | `const Image tiles[8] = {scene, unsharpMask(scene, 1.0, 1.5), unsharpMask(scene, 2.0, 5.0), greyFToImage(sx, 0.25, 128.0), greyFToImage(strength, 255.0 / largest), edgeMap(strength, 0.25 * largest), directionColours(sx, sy, largest), greyFToImage(convolveGrey(grey, laplacianKernel()), 1.0, 128.0)};` | Eight pictures: original; sharpened gently; sharpened far too much (σ 2, amount 5); signed Gx; strength; edge map; directions as hues; signed Laplacian. |
| 149–161 | `const std::string names[8] = {...}; Image sheet(4 * 170 + 10, 2 * 134 + 10, colours::white); for (int i = 0; i < 8; ++i) { ... drawText(sheet, left, top + 114, names[i], colours::black); }` | A 4 × 2 sheet with names (the same layout as Chapter 50). |
| 162–168 | `if (!savePNGCompressed(sheet, "edges.png")) { ... }` … `return 0;` `}` | Save it. |

### What you should see

```
weights add up to: sharpen 1, Laplacian 0, Sobel x 0

edge 100 -> 160, sharpen kernel:   100 100 40 220 160 160
unsharp mask, sigma 1, amount 1:   100 96 82 178 164 160
the same in linear light:          100 95 69 173 163 160
edge 50 -> 200, sharpen kernel:    50 50 0 255 200 200

edge grid, Sobel x:        0 360 360 0 0
edge grid, Sobel y:        0 0 0 0 0
flipped edge, Sobel x:     0 -360 -360 0 0
the same, kept as bytes:   0 0 0 0 0
diagonal edge, centre: gx 270, gy 270, strength 381.8, direction 45 degrees
directions: edge grid 0, flipped 180

dot grid, Laplacian:       0 90 -360 90 0
edge grid, Laplacian:      0 90 -90 0 0

noisy edge, pixels with strength >= 100: 920 without blur, 192 after a blur (the real edge: 2 x 64 = 128)
wrote edges.png
```

In `edges.png`:

- **sharpened**: the house, the roof and the hills look crisper. **far too sharp**: thick bright and dark rims around everything.
- **Sobel x**: mid grey, with the left rim of the sun light (going right, it gets brighter: gx > 0) and its right rim dark (gx < 0) — like a stamp lit from the side. The horizon lines are almost invisible here, because they are mostly horizontal: gx hardly sees them.
- **strength**: white outlines of everything, on black. The sky is black, because its gradient is so gentle.
- **edge map**: the same outlines, now pure black and white.
- **direction**: coloured outlines; the top and bottom of the sun and the left and right of the house have different hues.
- **Laplacian**: mid grey with thin light and dark double lines along every edge.

---

## Small examples

### Example 1 — Sharpening a flat area

All neighbours are v: 5v − v − v − v − v = **v**. Flat areas never change (the weights add up to 1).

### Example 2 — The strongest possible Sobel value

A jump from 0 to 255 under the whole kernel: gx = (1 + 2 + 1) × 255 = **1020**. If gx and gy are both 1020: √(1020² + 1020²) ≈ **1442.5**.

### Example 3 — A 3-4-5 edge

gx = 30, gy = 40: strength = √(900 + 1600) = √2500 = **50**; direction = atan2(40, 30) ≈ **53.1°** (down and to the right, more down than right).

### Example 4 — A horizontal edge

Dark above, bright below: gx = 0, gy = +360 → strength 360, direction atan2(360, 0) = **90°**: "brighter below".

### Example 5 — Amount 0 and a negative amount

Amount 0: original + 0 × detail = the **original**. Amount −0.5: original − 0.5 × detail — the edges get **softer**, a mild blur.

---

## Common mistakes

⚠️ **Storing edge values as bytes** — negative values become 0 and half the edges vanish. Use doubles (`GreyF`) until the end.

⚠️ **atan2(gx, gy)** instead of **atan2(gy, gx)** — the y value comes first. The wrong order mirrors every direction.

⚠️ **Forgetting that y goes down** — 90° means "brighter below", not above.

⚠️ **Dividing by the largest strength when there is none** — a picture with no edges at all has largest = 0. Check for 0 before dividing (`directionColours` and the "strength" tile assume there is at least one edge).

⚠️ **Sharpening too much** — glowing halos. Keep the amount around 0.5–1.5.

⚠️ **Sharpening a noisy picture** — the noise is sharpened too. Blur a little (or use a threshold) first.

⚠️ **Looking for edges without a blur** — noise makes hundreds of false edges.

---

## Practice

🏋️ **1.** Apply the sharpen kernel by hand to the 1-pixel-high row 0 0 90 0 0. What are the real values, and what do the bytes become?

🏋️ **2.** Make a horizontal edge grid (rows 0 and 1 are 0, rows 2 … 4 are 90). Work out Gy in column 2, going down, and Gx.

🏋️ **3.** The **Prewitt** kernels are like Sobel, but without the 2: `−1 0 1 / −1 0 1 / −1 0 1`. Compute gx, gy, strength and direction at the centre of the diagonal grid.

🏋️ **4.** Add a **threshold** to the unsharp mask: change a channel only where |original − blurred| is bigger than `threshold` (in 0 … 1 units). Write `unsharpMaskThreshold`.

🏋️ **5.** On the edge grid, Sobel's edge is **2** pixels wide (columns 1 and 2). Why two, and not one?

🏋️ **6.** Make an **emboss** effect: every pixel becomes the grey 128 + gx / 4 + gy / 4. Write it with the functions of this chapter.

🏋️ **7.** What colour does `directionColours` give to an edge whose bright side is **above**?

🏋️ **8.** Make edges **thin**: keep a pixel of the strength picture only if it is at least as strong as both neighbours **along its direction** (rounded to 0°, 45°, 90° or 135°); otherwise set it to 0. Write `GreyF thinEdges(const GreyF& strength, const GreyF& gx, const GreyF& gy)`.

---

## Answers

**1.**
> 1 pixel high, so new = 3c − left − right (Section 51.2):
> x = 0: 0 − 0 − 0 = 0; x = 1: 0 − 0 − 90 = **−90**; x = 2: 270 − 0 − 0 = **270**; x = 3: **−90**; x = 4: 0.
> Real values: 0 −90 270 −90 0. As bytes: **0 0 255 0 0** — the dark halos are lost (they cannot go below black) and the top is clamped.

**2.**
> Gy at column 2: row 0: above is row 0 (clamped), below is row 1 → 0 − 0 = **0**; row 1: above row 0 (0), below row 2 (90) → (1 + 2 + 1) × 90 = **360**; row 2: above row 1 (0), below row 3 (90) → **360**; rows 3 and 4: **0**.
> Down column 2: 0 360 360 0 0. Gx is 0 everywhere (nothing changes across).

**3.**
> gx = (0 − 0) + (90 − 0) + (90 − 0) = **180**; gy = (0 + 90 + 90) − (0 + 0 + 0) = **180**.
> strength = √(180² + 180²) ≈ **254.6**; direction = atan2(180, 180) = **45°**. Same direction, smaller numbers (the positive weights add up to 3, not 4).

**4.**

```cpp
Image unsharpMaskThreshold(const Image& image, double sigma, double amount, double threshold) {
    const std::vector<double> w = gaussianWeights(sigma);
    const PixelsF sharp = toPixelsF(image, false);
    const PixelsF soft = blurColumns(blurRows(sharp, w, EdgeMode::Clamp), w, EdgeMode::Clamp);
    PixelsF out = sharp;
    for (int i = 0; i < static_cast<int>(out.data.size()); ++i) {
        const ColourF detail = sharp.data[i] - soft.data[i];
        if (std::fabs(detail.r) > threshold) {
            out.data[i].r += detail.r * amount;
        }
        if (std::fabs(detail.g) > threshold) {
            out.data[i].g += detail.g * amount;
        }
        if (std::fabs(detail.b) > threshold) {
            out.data[i].b += detail.b * amount;
        }
    }
    return fromPixelsF(out, false);
}
```

> A threshold of 0.02 (about 5 in byte units) leaves gentle gradients and fine noise alone.

**5.**
> The step lies **between** pixels 1 and 2. Pixel 1 sees 0 on its left and 90 on its right; pixel 2 sees the same (its left is column 1, 0; its right is column 3, 90). Both straddle the step, so both light up. Thinning (Practice 8) or the Laplacian's zero-crossing (Section 51.10) can put the edge in one place.

**6.**

```cpp
Image emboss(const Image& image) {
    const GreyF g = toGreyF(image);
    const GreyF gx = convolveGrey(g, sobelX());
    const GreyF gy = convolveGrey(g, sobelY());
    GreyF sum = makeGreyF(g.width, g.height);
    for (int i = 0; i < static_cast<int>(sum.data.size()); ++i) {
        sum.data[i] = gx.data[i] + gy.data[i];
    }
    return greyFToImage(sum, 0.25, 128.0);
}
```

> It looks as if the picture were pressed into metal and lit from the top-left.

**7.**
> Bright above means gy is **negative** (below − above < 0) and gx = 0: atan2(−360, 0) = −90°, and `wrapHue` makes it **270°**: a blue-violet hue.

**8.**

```cpp
GreyF thinEdges(const GreyF& strength, const GreyF& gx, const GreyF& gy) {
    const int stepX[4] = {1, 1, 0, -1};
    const int stepY[4] = {0, 1, 1, 1};
    GreyF out = makeGreyF(strength.width, strength.height);
    for (int y = 0; y < strength.height; ++y) {
        for (int x = 0; x < strength.width; ++x) {
            const int i = y * strength.width + x;
            const double angle = std::fmod(directionDegrees(gx.data[i], gy.data[i]), 180.0);
            const int d = static_cast<int>(std::floor(angle / 45.0 + 0.5)) % 4;
            const double ahead = greyAt(strength, x + stepX[d], y + stepY[d]);
            const double behind = greyAt(strength, x - stepX[d], y - stepY[d]);
            if (strength.data[i] >= ahead && strength.data[i] >= behind) {
                out.data[i] = strength.data[i];
            }
        }
    }
    return out;
}
```

> A direction and its opposite (say 20° and 200°) look along the same line, so we reduce the angle to 0 … 180° with `std::fmod`. Then 0°, 45°, 90°, 135° become d = 0, 1, 2, 3 (and 180° wraps to 0 with `% 4`). On the edge grid, columns 1 and 2 are both 360 — equal, so both survive (`>=`); with real, slightly uneven pictures, only the ridge is kept. This is the "non-maximum suppression" step of the Canny edge detector.

---

## Summary

🧠 **Sharpen** = original + amount × (original − blurred). The kernel `0 −1 0 / −1 5 −1 / 0 −1 0` is this with a tiny blur and amount 4; the **unsharp mask** uses a Gaussian blur, a radius and an amount.

🧠 Sharpening makes **halos**; too much looks bad and gets clamped. Sharpen in **sRGB values**, where equal steps look equal — and remember that noise gets sharpened too.

🧠 **Sobel** Gx and Gy measure the change across and down (a difference times a small blur). Keep their **negative** values: work in doubles (`GreyF`).

🧠 Edge **strength** = √(gx² + gy²); edge **direction** = atan2(gy, gx), pointing from dark to bright (y goes down). Show them as grey, as a threshold edge map, or as hues.

🧠 **Blur first** to stop noise from making false edges. The **Laplacian** finds edges where it crosses zero.

---

## Next chapter

Chapter 47's threshold turned a grey picture into black and white — and lost all the shading. In Chapter 52 we keep it: **dithering** mixes black and white dots so that, from a distance, they look grey. We build the ordered **Bayer** pattern and the clever **Floyd–Steinberg** method that passes each pixel's mistake on to its neighbours, then dither in colour, choosing the **nearest colour** in the RGB cube (Chapter 5 promised this).
