# Chapter 50 — Blur: Box Blur and Gaussian Blur

> **Part 7 · Chapter 50 of 82**
> **You need:** Chapters 1–49 (especially 17, 30, 35 and 49) · **You will make:** `blur.h` (Gaussian weights, separable blurring across and down, a fast box blur with a running sum), and `blur.png`: one scene at five strengths of blur, plus one blurred in the wrong light

---

## What you will learn

- Why the **box** blur looks a bit crude, and what makes the **Gaussian** blur smooth.
- The bell curve e^(−x² / 2σ²), and what the number **σ** (sigma) means.
- How to make big blurs fast: **separable** kernels (across, then down).
- The **running sum**: a box blur whose cost does not grow with its size.
- Why three box blurs in a row look like one Gaussian.
- Why blurring belongs in **linear light**, and why you should blur **before** shrinking a picture.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **Gaussian** | The smooth "bell curve" shape e^(−x² / 2σ²), named after Carl Friedrich Gauss. |
| **sigma (σ)** | The width of the bell curve: bigger σ, wider blur. |
| **normalise** | Divide all weights by their sum, so that they add up to 1. |
| **separable** | A 2D kernel that can be done as one pass across and one pass down. |
| **running sum** | A sum that is updated by adding the new value and subtracting the old one. |
| **aliasing** | False patterns that appear when fine detail is sampled too coarsely. |

---

## 50.1 What is wrong with the box?

Chapter 49's box kernel gives the same weight to every pixel in a square. Two things look wrong:

- A pixel at the **corner** of the square counts as much as the centre pixel, although it is further away.
- At the **edge** of the square, weights jump from 1/n to 0. A bright dot becomes a bright **square** — you can see the shape of the kernel in the picture.

Real blur (a camera out of focus, a misty window) is softer: near pixels count a lot, far pixels a little, and the weight fades away smoothly. That shape is a **bell curve**.

---

## 50.2 The bell curve

📖 **New word: Gaussian** — the function

> **g(x) = e^(−x² / (2σ²))**

named after the mathematician Carl Friedrich Gauss. e is the number 2.71828… (`std::exp(v)` in `<cmath>` computes e^v; Chapter 30 mentioned it). Its graph is the famous bell:

```
     g(x)
    1.0 ┤        ▄█▄
        │       █████
    0.6 ┤      ███████              x = 0: g = 1 (the top)
        │     █████████             x = ±σ: g = 0.61
        │    ███████████            x = ±2σ: g = 0.14
    0.1 ┤  ▄█████████████▄          x = ±3σ: g = 0.011 (almost nothing)
      0 ┼▄▄█████████████████▄▄─── x
         −3σ   −σ  0  σ   3σ
```

📖 **New word: sigma (σ)** — the Greek letter that sets the **width** of the bell. σ = 1: most of the weight is within 1–2 pixels. σ = 5: a wide, strong blur.

🔢 **Maths: why −x², and why 2σ²?**

> −x²: the weight is biggest at x = 0, the same on both sides (x² does not care about the sign), and falls quickly as x grows.
> dividing by 2σ²: makes the curve wider when σ is bigger. At x = σ, the exponent is always −1/2, so g(σ) = e^(−0.5) = 0.6065 for every σ.

Beyond 3σ, the weights are so small (under 1.1 % of the centre) that we can leave them out. So a Gaussian kernel has radius **r = ⌈3σ⌉** (rounded up).

---

## 50.3 Gaussian weights

To make a kernel: compute g(x) for x = −r … r, then make the weights add up to 1 (Chapter 49: weights adding up to 1 keep the brightness).

📖 **New word: normalise** — divide every weight by the sum of all weights. Then they add up to exactly 1 (apart from tiny rounding).

🔢 **Maths: σ = 1** (radius ⌈3⌉ = 3, so 7 weights)

> g(0) = e^0 = **1**
> g(±1) = e^(−1/2) = **0.6065**
> g(±2) = e^(−4/2) = e^(−2) = **0.1353**
> g(±3) = e^(−9/2) = e^(−4.5) = **0.0111**
> sum = 1 + 2 × (0.6065 + 0.1353 + 0.0111) = **2.5059**
> normalised: 1 / 2.5059 = **0.3991**, 0.6065 / 2.5059 = **0.2420**, 0.1353 / 2.5059 = **0.0540**, 0.0111 / 2.5059 = **0.0044**

```
Gaussian weights, sigma 0.5: 0.0003 0.1065 0.7866 0.1065 0.0003  (sum 1)
Gaussian weights, sigma 1: 0.0044 0.0540 0.2420 0.3991 0.2420 0.0540 0.0044  (sum 1)
```

With σ = 0.5, the centre keeps 79 % of its own value: a very gentle blur. With σ = 1, only 40 %.

---

## 50.4 From one dimension to two: separable kernels

Those are **1D** weights — for a row. A 2D blur needs a square kernel. For the Gaussian, there is a beautiful shortcut.

🔢 **Maths: the 2D Gaussian splits in two**

> the 2D bell: G(x, y) = e^(−(x² + y²) / 2σ²)
> and since e^(a + b) = e^a × e^b:
> G(x, y) = e^(−x² / 2σ²) × e^(−y² / 2σ²) = **g(x) × g(y)**

So the 2D weight in column i, row j is just w[i] × w[j]. `kernelFromWeights` builds such a square kernel. But more importantly:

📖 **New word: separable** — a 2D kernel whose weights are w[j] × w[i] can be done as **two 1D passes**: first blur every **row** with w (across), then blur every **column** of the result with w (down). The result is the same as the full 2D convolution.

🔢 **Maths: why two passes give the same sum**

> 2D: new(x, y) = Σⱼ Σᵢ w[j] w[i] × old(x + i − r, y + j − r)
> = Σⱼ w[j] × ( Σᵢ w[i] × old(x + i − r, y + j − r) )
> the bracket is the **row pass** at row y + j − r; the outer sum is the **column pass** on its results

The program checks it on a test picture (a checkerboard with a white square), with σ = 1.5:

```
sigma 1.5: 11 x 11 kernel vs separable: 0 of 18432 values differ, by at most 0
```

Identical. (In general, a value can now and then differ by 1, because the two methods add their numbers in a different order, and `double` rounding depends on order. Here, none did.)

🔢 **Maths: the saving**

> σ = 5: r = 15, so n = 31 weights
> 2D: 31 × 31 = **961** multiplications per value
> separable: 31 + 31 = **62** — more than 15 times less work

```
sigma 5: kernel 31 x 31, multiplications per value: 2D 961, separable 62
```

The box kernel is separable too (all weights equal: w[i] × w[j] = 1/n × 1/n).

⚠️ Between the two passes we keep the values as `double`s (`PixelsF`), not bytes. Rounding to bytes in the middle would add an error — and in linear light, dark values would lose a lot of precision.

---

## 50.5 The running sum: a box blur in constant time

For the **box**, there is an even better trick. Moving along a row, the window of 2r + 1 pixels changes by only two pixels: one **enters** on the right, one **leaves** on the left.

```
   window for x:     [ a  b  c  d  e ]
   window for x + 1:    [ b  c  d  e  f ]      sum(x + 1) = sum(x) + f − a
```

📖 **New word: running sum** — keep the sum of the window; for each step, **add** the entering pixel and **subtract** the leaving one. Each step costs one addition and one subtraction, **whatever the radius**. A box blur of radius 50 costs the same as one of radius 1.

🔢 **Maths: the row 10 20 30 40 50, radius 1, clamp**

> start: window for x = 0 is (clamp −1 → 10) 10 + 10 + 20 = **40** → 40 / 3 = 13.3
> x = 1: + 30 (entering, x + 2) − 10 (leaving, x − 1 = −1 → 10) → 60 → 20
> x = 2: + 40 − 10 → 90 → 30
> x = 3: + 50 − 20 → 120 → 40
> x = 4: + 50 (x + 2 = 5 → clamp 4) − 30 → 140 → 46.7

`boxRowsFast` does this for every row. For the columns, we **transpose** the picture (swap x and y, so columns become rows), run the same function, and transpose back. Checked against the separable box blur:

```
box radius 3: separable vs running sum: 0 of 18432 values differ, by at most 0
```

⚠️ A running sum collects tiny `double` errors as it goes (each add and subtract rounds). For pictures of normal size, that is far below one byte step.

---

## 50.6 Three boxes make a bell

Blur a single bright pixel with a small box three times, and compare it with one Gaussian:

```
spike, three box blurs (radius 1): 0 0 0 0 9 28 57 66 57 28 9 0 0 0 0
spike, one Gaussian (sigma 1.41):   0 0 0 1 8 26 56 72 56 26 8 1 0 0 0
```

Almost the same shape! Each box pass spreads the spike out a little, and the passes pile up into a bell. (Mathematicians know this as the **central limit theorem**: adding up many small random steps always gives a bell curve.)

🔢 **Maths: why σ = 1.41?**

> a box of radius 1 averages the offsets −1, 0, 1: the "spread" (variance) is (1 + 0 + 1) / 3 = 2/3
> three passes add their variances: 3 × 2/3 = 2
> σ is the square root of the variance: √2 = **1.41**

So three fast box blurs (with running sums) give a cheap, good Gaussian of any size. Many programs blur exactly like that.

---

## 50.7 Blur in linear light

Blurring is mixing, and mixing colours belongs in **linear light** (Chapter 17). Our functions do it by default (`linearLight = true`).

🔢 **Maths: red next to green**

> the row red red green green, box radius 1, pixel 1 mixes (red + red + green) / 3
> in sRGB values: red channel (255 + 255 + 0) / 3 = **170**, green (0 + 0 + 255) / 3 = **85**
> in linear light: red (1 + 1 + 0) / 3 = 0.667 → sRGB **213**; green 1/3 = 0.333 → sRGB **156**

```
red red green green, pixel 1 blurred: sRGB values 170 85 0, linear light 213 156 0
```

(170, 85, 0) is a dark, muddy brown; (213, 156, 0) a bright orange. Real light from a red and a green lamp mixes to a bright yellow-orange, not brown. In `blur.png`, compare "Gaussian sigma 3" with "sigma 3, sRGB values": in the sRGB version, the edge between the bright sun and the blue sky gets a **dark rim**.

---

## 50.8 Blur before you shrink

Chapter 35 shrank pictures with nearest neighbour and noticed that fine detail can turn into strange patterns. Chapter 35 promised a fix: blur first. Here is why.

📖 **New word: aliasing** — when a picture has detail **finer** than the new pixel size, sampling picks up the detail at "random" places, and **false patterns** appear.

🔢 **Maths: stripes, shrunk 3 times**

> the picture: 2 white pixels, 2 black, 2 white, … (a stripe pattern that repeats every **4** pixels)
> shrinking 48 → 16 with nearest neighbour picks source x = ⌊(x + 0.5) × 3⌋ = 1, 4, 7, 10, 13, 16, …
> x mod 4 of those: 1, 0, 3, 2, 1, 0, 3, 2 … → white, white, black, black, …

```
stripes shrunk 3 times:           255 255 0 0 255 255 0 0 255 255 0 0 255 255 0 0
```

The small picture shows **wide** stripes, repeating every 4 **new** pixels — 12 old pixels. That pattern is not in the original at all! It is aliasing (you may have seen it as strange waves on photos of shirts or screens, called **moiré**).

Blur first, with σ about half the shrink factor:

```
blurred (sigma 1.5), then shrunk: 215 193 182 182 193 193 182 182 193 193 182 182 193 193 182 154
```

Now the small picture is almost even grey, around **188** — which is exactly right: half white and half black light is 0.5 in linear light, and 0.5 linear is sRGB **188** (Chapter 17). The remaining ripple (182 / 193) is small; a bigger σ would smooth it more but blur real detail too. (The first and last values differ because of the picture's edges.)

🧠 **Remember:** before shrinking a picture, blur away the detail that the smaller picture cannot hold. Chapter 35's box shrink (`resizeBox`) does a version of this automatically.

---

## 50.9 Edges, once more

Our blurs use **Clamp** edges by default (Chapter 49). With a big σ, the edge mode matters more: σ = 8 reaches 24 pixels outside the picture. Clamp repeats the border pixels, which looks natural for skies and walls. Zero would add a dark frame; Wrap would mix the sky into the ground. (Chapter 35 promised to show this choice; Practice 5 lets you see all four.)

---

## Code, part 1: `blur.h`

File: `common/blur.h` (new). It includes `convolve.h` (kernels, edge modes and `readPixel`/`writePixel`, Chapter 49).

```cpp
#ifndef BLUR_H
#define BLUR_H

#include <cmath>
#include <vector>
#include "convolve.h"

struct PixelsF {
    int width = 0;
    int height = 0;
    std::vector<ColourF> data;
};

inline PixelsF toPixelsF(const Image& image, bool linearLight) {
    PixelsF p{image.width(), image.height(), {}};
    p.data.reserve(image.width() * image.height());
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            const Colour c = image.getPixel(x, y);
            p.data.push_back(linearLight ? toLinear(c) : toColourF(c));
        }
    }
    return p;
}

inline Image fromPixelsF(const PixelsF& p, bool linearLight) {
    Image image(p.width, p.height);
    for (int y = 0; y < p.height; ++y) {
        for (int x = 0; x < p.width; ++x) {
            image.setPixel(x, y, writePixel(p.data[y * p.width + x], linearLight));
        }
    }
    return image;
}

inline std::vector<double> gaussianWeights(double sigma) {
    const int r = static_cast<int>(std::ceil(3.0 * sigma));
    std::vector<double> w(2 * r + 1);
    double sum = 0.0;
    for (int i = 0; i <= 2 * r; ++i) {
        const double d = i - r;
        w[i] = std::exp(-(d * d) / (2.0 * sigma * sigma));
        sum += w[i];
    }
    for (double& v : w) {
        v /= sum;
    }
    return w;
}

inline std::vector<double> boxWeights(int radius) {
    return std::vector<double>(2 * radius + 1, 1.0 / (2 * radius + 1));
}

inline Kernel kernelFromWeights(const std::vector<double>& w) {
    const int n = static_cast<int>(w.size());
    Kernel k{n, std::vector<double>(n * n)};
    for (int j = 0; j < n; ++j) {
        for (int i = 0; i < n; ++i) {
            k.weights[j * n + i] = w[j] * w[i];
        }
    }
    return k;
}

inline PixelsF blurRows(const PixelsF& src, const std::vector<double>& w, EdgeMode mode) {
    const int r = static_cast<int>(w.size()) / 2;
    PixelsF out{src.width, src.height, std::vector<ColourF>(src.data.size())};
    for (int y = 0; y < src.height; ++y) {
        for (int x = 0; x < src.width; ++x) {
            ColourF sum{0.0, 0.0, 0.0};
            for (int k = 0; k < static_cast<int>(w.size()); ++k) {
                const int sx = edgeIndex(x + k - r, src.width, mode);
                if (sx >= 0) {
                    sum = sum + src.data[y * src.width + sx] * w[k];
                }
            }
            out.data[y * src.width + x] = sum;
        }
    }
    return out;
}

inline PixelsF blurColumns(const PixelsF& src, const std::vector<double>& w, EdgeMode mode) {
    const int r = static_cast<int>(w.size()) / 2;
    PixelsF out{src.width, src.height, std::vector<ColourF>(src.data.size())};
    for (int y = 0; y < src.height; ++y) {
        for (int x = 0; x < src.width; ++x) {
            ColourF sum{0.0, 0.0, 0.0};
            for (int k = 0; k < static_cast<int>(w.size()); ++k) {
                const int sy = edgeIndex(y + k - r, src.height, mode);
                if (sy >= 0) {
                    sum = sum + src.data[sy * src.width + x] * w[k];
                }
            }
            out.data[y * src.width + x] = sum;
        }
    }
    return out;
}

inline Image separableBlur(const Image& image, const std::vector<double>& w,
                           EdgeMode mode = EdgeMode::Clamp, bool linearLight = true) {
    const PixelsF across = blurRows(toPixelsF(image, linearLight), w, mode);
    return fromPixelsF(blurColumns(across, w, mode), linearLight);
}

inline Image gaussianBlur(const Image& image, double sigma, EdgeMode mode = EdgeMode::Clamp,
                          bool linearLight = true) {
    if (sigma <= 0.0) {
        return image;
    }
    return separableBlur(image, gaussianWeights(sigma), mode, linearLight);
}

inline PixelsF boxRowsFast(const PixelsF& src, int r) {
    PixelsF out{src.width, src.height, std::vector<ColourF>(src.data.size())};
    const double scale = 1.0 / (2 * r + 1);
    for (int y = 0; y < src.height; ++y) {
        const ColourF* row = &src.data[y * src.width];
        ColourF sum{0.0, 0.0, 0.0};
        for (int k = -r; k <= r; ++k) {
            sum = sum + row[edgeIndex(k, src.width, EdgeMode::Clamp)];
        }
        for (int x = 0; x < src.width; ++x) {
            out.data[y * src.width + x] = sum * scale;
            const ColourF entering = row[edgeIndex(x + r + 1, src.width, EdgeMode::Clamp)];
            const ColourF leaving = row[edgeIndex(x - r, src.width, EdgeMode::Clamp)];
            sum = sum + entering - leaving;
        }
    }
    return out;
}

inline PixelsF transposed(const PixelsF& src) {
    PixelsF out{src.height, src.width, std::vector<ColourF>(src.data.size())};
    for (int y = 0; y < src.height; ++y) {
        for (int x = 0; x < src.width; ++x) {
            out.data[x * src.height + y] = src.data[y * src.width + x];
        }
    }
    return out;
}

inline Image boxBlurFast(const Image& image, int radius, bool linearLight = true) {
    const PixelsF across = boxRowsFast(toPixelsF(image, linearLight), radius);
    const PixelsF down = boxRowsFast(transposed(across), radius);
    return fromPixelsF(transposed(down), linearLight);
}

#endif
```

### Line by line

**Floating-point pictures (lines 1–34)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–6 | include guard and `#include` lines | `std::exp`, `std::ceil`, lists, and Chapter 49's header. |
| 8–12 | `struct PixelsF { int width = 0; int height = 0; std::vector<ColourF> data; };` | A picture made of `ColourF`s (doubles), for the values between the two passes (Section 50.4). Same order as `Image`: index y × width + x. |
| 14–24 | `inline PixelsF toPixelsF(const Image& image, bool linearLight) { PixelsF p{image.width(), image.height(), {}}; p.data.reserve(...); for (...) { ... p.data.push_back(linearLight ? toLinear(c) : toColourF(c)); } return p; }` | Turn a picture into doubles: linear light or plain sRGB values / 255. `reserve` gets the memory once instead of many times. |
| 26–34 | `inline Image fromPixelsF(const PixelsF& p, bool linearLight) { ... image.setPixel(x, y, writePixel(p.data[y * p.width + x], linearLight)); ... }` | And back to bytes, clamped and rounded (Chapter 49's `writePixel`). |

**Weights (lines 36–64)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 36–38 | `inline std::vector<double> gaussianWeights(double sigma) { const int r = static_cast<int>(std::ceil(3.0 * sigma)); std::vector<double> w(2 * r + 1);` | Radius ⌈3σ⌉ (Section 50.2), so 2r + 1 weights. |
| 39–44 | `double sum = 0.0; for (int i = 0; i <= 2 * r; ++i) { const double d = i - r; w[i] = std::exp(-(d * d) / (2.0 * sigma * sigma)); sum += w[i]; }` | The bell value for each distance d = −r … r, and their sum. |
| 45–49 | `for (double& v : w) { v /= sum; } return w;` `}` | Normalise (Section 50.3). `double& v` changes the weights in the list itself. |
| 51–53 | `inline std::vector<double> boxWeights(int radius) { return std::vector<double>(2 * radius + 1, 1.0 / (2 * radius + 1)); }` | The 1D box: 2r + 1 equal weights. |
| 55–64 | `inline Kernel kernelFromWeights(const std::vector<double>& w) { const int n = ...; Kernel k{n, std::vector<double>(n * n)}; for (...) { for (...) { k.weights[j * n + i] = w[j] * w[i]; } } return k; }` | The full 2D kernel w[j] × w[i] (Section 50.4) — for checking, and for Chapter 49's `convolve`. |

**The two passes (lines 66–114)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 66–68 | `inline PixelsF blurRows(const PixelsF& src, const std::vector<double>& w, EdgeMode mode) { const int r = ...w.size()... / 2; PixelsF out{src.width, src.height, std::vector<ColourF>(src.data.size())};` | Blur across. A new `out`, never in place (Chapter 49). |
| 69–76 | `for (y) { for (x) { ColourF sum{0.0, 0.0, 0.0}; for (int k = 0; ...) { const int sx = edgeIndex(x + k - r, src.width, mode); if (sx >= 0) { sum = sum + src.data[y * src.width + sx] * w[k]; } }` | The 1D convolution along the row, with Chapter 49's edge modes (−1 means Zero: add nothing). |
| 77–82 | `out.data[y * src.width + x] = sum; } } return out; }` | Keep the result as doubles. |
| 84–100 | `inline PixelsF blurColumns(...) { ... const int sy = edgeIndex(y + k - r, src.height, mode); ... src.data[sy * src.width + x] ... }` | The same, down each column. |
| 102–106 | `inline Image separableBlur(const Image& image, const std::vector<double>& w, EdgeMode mode = EdgeMode::Clamp, bool linearLight = true) { const PixelsF across = blurRows(toPixelsF(image, linearLight), w, mode); return fromPixelsF(blurColumns(across, w, mode), linearLight); }` | Any separable blur: to doubles, across, down, back to bytes. Linear light by default (Section 50.7). |
| 108–114 | `inline Image gaussianBlur(const Image& image, double sigma, ...) { if (sigma <= 0.0) { return image; } return separableBlur(image, gaussianWeights(sigma), mode, linearLight); }` | The Gaussian blur. σ of 0 or less means "no blur" (and avoids dividing by 0). |

**The fast box blur (lines 116–149)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 116–118 | `inline PixelsF boxRowsFast(const PixelsF& src, int r) { PixelsF out{...}; const double scale = 1.0 / (2 * r + 1);` | A box blur across, with a running sum (Section 50.5). Multiplying by `scale` is the same as dividing by the window size. |
| 119–124 | `for (y) { const ColourF* row = &src.data[y * src.width]; ColourF sum{0.0, 0.0, 0.0}; for (int k = -r; k <= r; ++k) { sum = sum + row[edgeIndex(k, src.width, EdgeMode::Clamp)]; }` | `row` points at the first pixel of row y, so `row[x]` is pixel x. The first window (for x = 0) is added up the slow way, once. |
| 125–130 | `for (int x = 0; x < src.width; ++x) { out.data[y * src.width + x] = sum * scale; const ColourF entering = row[edgeIndex(x + r + 1, ...)]; const ColourF leaving = row[edgeIndex(x - r, ...)]; sum = sum + entering - leaving; }` | Write the average, then move the window one step: add the pixel at x + r + 1, subtract the one at x − r. Clamp edges only (a running sum with Zero or Wrap would work too, but we keep it simple). |
| 131–133 | `}` `return out;` `}` | |
| 135–143 | `inline PixelsF transposed(const PixelsF& src) { PixelsF out{src.height, src.width, ...}; ... out.data[x * src.height + y] = src.data[y * src.width + x]; ... }` | Swap rows and columns: pixel (x, y) moves to (y, x), and width and height swap. |
| 145–149 | `inline Image boxBlurFast(const Image& image, int radius, bool linearLight = true) { const PixelsF across = boxRowsFast(toPixelsF(image, linearLight), radius); const PixelsF down = boxRowsFast(transposed(across), radius); return fromPixelsF(transposed(down), linearLight); }` | Across; then transpose, so the columns become rows, blur those "rows", and transpose back. |
| 151 | `#endif` | End of the include guard. |

---

## Code, part 2: blurs compared

File: `ch50/blur.cpp`

```cpp
#include <cmath>
#include <iostream>
#include <string>
#include <vector>
#include "blur.h"
#include "deflate.h"

std::string fourDecimals(double v) {
    const long long n = std::llround(v * 10000.0);
    std::string digits = std::to_string(n % 10000);
    while (digits.size() < 4) {
        digits = "0" + digits;
    }
    return std::to_string(n / 10000) + "." + digits;
}

void printRow(const std::string& label, const Image& image) {
    std::cout << label;
    for (int x = 0; x < image.width(); ++x) {
        std::cout << " " << static_cast<int>(image.getPixel(x, 0).r);
    }
    std::cout << "\n";
}

std::string colourText(Colour c) {
    return std::to_string(c.r) + " " + std::to_string(c.g) + " " + std::to_string(c.b);
}

Image makeTest() {
    Image test(96, 64);
    for (int y = 0; y < 64; ++y) {
        for (int x = 0; x < 96; ++x) {
            const std::uint8_t v = ((x / 8 + y / 8) % 2 == 0) ? 40 : 200;
            Colour c{v, static_cast<std::uint8_t>(v / 2), static_cast<std::uint8_t>(255 - v)};
            if (x >= 60 && x < 80 && y >= 20 && y < 40) {
                c = colours::white;
            }
            test.setPixel(x, y, c);
        }
    }
    return test;
}

void compare(const std::string& label, const Image& a, const Image& b) {
    int different = 0;
    int largest = 0;
    for (int y = 0; y < a.height(); ++y) {
        for (int x = 0; x < a.width(); ++x) {
            const Colour p = a.getPixel(x, y);
            const Colour q = b.getPixel(x, y);
            const int d[3] = {std::abs(p.r - q.r), std::abs(p.g - q.g), std::abs(p.b - q.b)};
            for (int v : d) {
                different += (v > 0) ? 1 : 0;
                largest = std::max(largest, v);
            }
        }
    }
    std::cout << label << ": " << different << " of " << a.width() * a.height() * 3
              << " values differ, by at most " << largest << "\n";
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
    const double sigmas[2] = {0.5, 1.0};
    for (double s : sigmas) {
        const std::vector<double> w = gaussianWeights(s);
        std::cout << "Gaussian weights, sigma " << s << ":";
        double sum = 0.0;
        for (double v : w) {
            std::cout << " " << fourDecimals(v);
            sum += v;
        }
        std::cout << "  (sum " << sum << ")\n";
    }

    const Image test = makeTest();
    compare("sigma 1.5: 11 x 11 kernel vs separable",
            convolve(test, kernelFromWeights(gaussianWeights(1.5)), EdgeMode::Clamp, false),
            gaussianBlur(test, 1.5, EdgeMode::Clamp, false));
    compare("box radius 3: separable vs running sum", separableBlur(test, boxWeights(3)),
            boxBlurFast(test, 3));
    const int n = static_cast<int>(gaussianWeights(5.0).size());
    std::cout << "sigma 5: kernel " << n << " x " << n << ", multiplications per value: 2D " << n * n
              << ", separable " << 2 * n << "\n";

    Image spike(15, 1);
    spike.setPixel(7, 0, colours::white);
    Image boxed = spike;
    for (int pass = 0; pass < 3; ++pass) {
        boxed = separableBlur(boxed, boxWeights(1), EdgeMode::Clamp, false);
    }
    printRow("\nspike, three box blurs (radius 1):", boxed);
    printRow("spike, one Gaussian (sigma 1.41):  ",
             gaussianBlur(spike, std::sqrt(2.0), EdgeMode::Clamp, false));

    Image redGreen(4, 1);
    redGreen.setPixel(0, 0, colours::red);
    redGreen.setPixel(1, 0, colours::red);
    redGreen.setPixel(2, 0, colours::green);
    redGreen.setPixel(3, 0, colours::green);
    const Image blurredSrgb = separableBlur(redGreen, boxWeights(1), EdgeMode::Clamp, false);
    const Image blurredLinear = separableBlur(redGreen, boxWeights(1), EdgeMode::Clamp, true);
    std::cout << "\nred red green green, pixel 1 blurred: sRGB values "
              << colourText(blurredSrgb.getPixel(1, 0)) << ", linear light "
              << colourText(blurredLinear.getPixel(1, 0)) << "\n";

    Image stripes(48, 4);
    for (int y = 0; y < 4; ++y) {
        for (int x = 0; x < 48; ++x) {
            stripes.setPixel(x, y, (x % 4 < 2) ? colours::white : colours::black);
        }
    }
    printRow("\nstripes shrunk 3 times:          ", resizeNearest(stripes, 16, 1));
    printRow("blurred (sigma 1.5), then shrunk:",
             resizeNearest(gaussianBlur(stripes, 1.5), 16, 1));

    const Image scene = makeScene();
    const Image tiles[6] = {scene,
                            gaussianBlur(scene, 1.0),
                            gaussianBlur(scene, 3.0),
                            gaussianBlur(scene, 8.0),
                            boxBlurFast(scene, 8),
                            gaussianBlur(scene, 3.0, EdgeMode::Clamp, false)};
    const std::string names[6] = {"original",    "Gaussian sigma 1", "Gaussian sigma 3",
                                  "Gaussian sigma 8", "box radius 8", "sigma 3, sRGB values"};
    Image sheet(3 * 170 + 10, 2 * 134 + 10, colours::white);
    for (int i = 0; i < 6; ++i) {
        const int left = 10 + (i % 3) * 170;
        const int top = 10 + (i / 3) * 134;
        for (int y = 0; y < 110; ++y) {
            for (int x = 0; x < 160; ++x) {
                sheet.setPixel(left + x, top + y, tiles[i].getPixel(x, y));
            }
        }
        drawText(sheet, left, top + 114, names[i], colours::black);
    }
    if (!savePNGCompressed(sheet, "blur.png")) {
        std::cout << "could not write blur.png\n";
        return 1;
    }
    std::cout << "wrote blur.png\n";
    return 0;
}
```

Build and run it from the `code/ch50` folder:

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common blur.cpp -o blur
./blur
```

### Line by line

**Helpers (lines 1–76)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–6 | the `#include` lines | `<cmath>` for `std::llround`, `std::sqrt` and `std::abs`, printing, strings, lists, the new header, and `deflate.h`. |
| 8–15 | `std::string fourDecimals(double v) { const long long n = std::llround(v * 10000.0); std::string digits = std::to_string(n % 10000); while (digits.size() < 4) { digits = "0" + digits; } return std::to_string(n / 10000) + "." + digits; }` | Exactly four digits after the point: 0.0044 → n = 44 → "0" + "." + "0044". The leading zeros of the fraction must be added by hand. |
| 17–23 | `void printRow(const std::string& label, const Image& image) { ... }` | Print row 0 of a picture (the red values). |
| 25–27 | `std::string colourText(Colour c) { return std::to_string(c.r) + " " + ... ; }` | A colour as three numbers. |
| 29–42 | `Image makeTest() { ... const std::uint8_t v = ((x / 8 + y / 8) % 2 == 0) ? 40 : 200; Colour c{v, ...v / 2..., ...255 - v...}; if (x >= 60 && x < 80 && y >= 20 && y < 40) { c = colours::white; } ... }` | A test picture made only of whole-number rules: a coloured checkerboard of 8-pixel squares with a white rectangle. |
| 44–60 | `void compare(const std::string& label, const Image& a, const Image& b) { ... const int d[3] = {std::abs(p.r - q.r), ...}; for (int v : d) { different += (v > 0) ? 1 : 0; largest = std::max(largest, v); } ... }` | How many channel values differ between two pictures, and by how much at most. |
| 62–76 | `Image makeScene() { ... }` | Chapter 47's scene. |

**Weights and checks (lines 79–99)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 79–89 | `const double sigmas[2] = {0.5, 1.0}; for (double s : sigmas) { const std::vector<double> w = gaussianWeights(s); ... fourDecimals(v) ... sum += v; ... }` | The weights of Section 50.3, and their sum. |
| 91–94 | `compare("sigma 1.5: 11 x 11 kernel vs separable", convolve(test, kernelFromWeights(gaussianWeights(1.5)), EdgeMode::Clamp, false), gaussianBlur(test, 1.5, EdgeMode::Clamp, false));` | The full 2D kernel (Chapter 49's `convolve`) against the two passes, both in sRGB values (Section 50.4). |
| 95–96 | `compare("box radius 3: separable vs running sum", separableBlur(test, boxWeights(3)), boxBlurFast(test, 3));` | The two box blurs, both in linear light (Section 50.5). |
| 97–99 | `const int n = ...gaussianWeights(5.0).size()...; std::cout << ... n * n << ... 2 * n << ...` | The work for σ = 5. |

**Small rows (lines 101–130)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 101–109 | `Image spike(15, 1); spike.setPixel(7, 0, colours::white); Image boxed = spike; for (int pass = 0; pass < 3; ++pass) { boxed = separableBlur(boxed, boxWeights(1), EdgeMode::Clamp, false); } printRow(...); printRow(..., gaussianBlur(spike, std::sqrt(2.0), EdgeMode::Clamp, false));` | Three box blurs against one Gaussian with σ = √2 (Section 50.6). |
| 111–120 | `Image redGreen(4, 1); ... const Image blurredSrgb = separableBlur(redGreen, boxWeights(1), EdgeMode::Clamp, false); const Image blurredLinear = ...true...; std::cout << ...colourText(blurredSrgb.getPixel(1, 0))...` | The same blur in sRGB values and in linear light (Section 50.7). |
| 122–130 | `Image stripes(48, 4); ... (x % 4 < 2) ? colours::white : colours::black ... printRow(..., resizeNearest(stripes, 16, 1)); printRow(..., resizeNearest(gaussianBlur(stripes, 1.5), 16, 1));` | Shrinking 3 times without and with a blur first (Section 50.8; `resizeNearest` is Chapter 35's). |

**The picture (lines 132–158)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 132–138 | `const Image scene = makeScene(); const Image tiles[6] = {scene, gaussianBlur(scene, 1.0), gaussianBlur(scene, 3.0), gaussianBlur(scene, 8.0), boxBlurFast(scene, 8), gaussianBlur(scene, 3.0, EdgeMode::Clamp, false)};` | Six versions of the scene. |
| 139–151 | `const std::string names[6] = {...}; Image sheet(...); for (...) { ... sheet.setPixel(left + x, top + y, tiles[i].getPixel(x, y)); ... drawText(...); }` | A 3 × 2 grid with names. |
| 152–158 | `if (!savePNGCompressed(sheet, "blur.png")) { ... }` … `return 0;` `}` | Save it. |

### What you should see

```
Gaussian weights, sigma 0.5: 0.0003 0.1065 0.7866 0.1065 0.0003  (sum 1)
Gaussian weights, sigma 1: 0.0044 0.0540 0.2420 0.3991 0.2420 0.0540 0.0044  (sum 1)
sigma 1.5: 11 x 11 kernel vs separable: 0 of 18432 values differ, by at most 0
box radius 3: separable vs running sum: 0 of 18432 values differ, by at most 0
sigma 5: kernel 31 x 31, multiplications per value: 2D 961, separable 62

spike, three box blurs (radius 1): 0 0 0 0 9 28 57 66 57 28 9 0 0 0 0
spike, one Gaussian (sigma 1.41):   0 0 0 1 8 26 56 72 56 26 8 1 0 0 0

red red green green, pixel 1 blurred: sRGB values 170 85 0, linear light 213 156 0

stripes shrunk 3 times:           255 255 0 0 255 255 0 0 255 255 0 0 255 255 0 0
blurred (sigma 1.5), then shrunk: 215 193 182 182 193 193 182 182 193 193 182 182 193 193 182 154
wrote blur.png
```

In `blur.png`, look at the sun. With the box (radius 8), its glow has a squarish outline and a fairly hard end; with the Gaussians, the glow is round and fades out softly. (A box of radius 8 blurs about as much as a Gaussian with σ ≈ 4.9: its variance is 8 × 9 / 3 = 24, and √24 ≈ 4.9.)

---

## Small examples

### Example 1 — The radius for σ = 2.2

r = ⌈3 × 2.2⌉ = ⌈6.6⌉ = **7**: a kernel of 15 weights.

### Example 2 — g(2σ)

At x = 2σ: e^(−4σ² / 2σ²) = e^(−2) = **0.135** — for every σ.

### Example 3 — A blur of a flat area

Any blur of a flat colour gives the same colour: Σ w × v = v × Σ w = v, because the weights are normalised.

### Example 4 — The cost of a 101-pixel box

Radius 50: 2D 101 × 101 = 10,201 per value; separable 202; running sum about **4** (one add, one subtract, one multiply, one write).

### Example 5 — Four times smaller

Shrinking by 4: blur with σ ≈ 2 first, then take every 4th pixel (or use Chapter 35's `resizeBox`).

---

## Common mistakes

⚠️ **Weights that do not add up to 1** — forgetting to normalise makes the picture darker (or brighter).

⚠️ **A radius that is too small** — r = σ cuts off the bell's sides: the blur looks like a box again. Use r = ⌈3σ⌉.

⚠️ **Rounding to bytes between the passes** — keep doubles in between.

⚠️ **Blurring in sRGB values** — dark rims around bright objects. Use linear light.

⚠️ **Shrinking without blurring** — false patterns (aliasing).

⚠️ **Blurring in place** — Chapter 49's warning applies to each pass.

---

## Practice

🏋️ **1.** Compute the normalised Gaussian weights for σ = 0.5 by hand (radius 2), and check them against the program.

🏋️ **2.** Run the running sum of Section 50.5 by hand for the row 0 0 90 0 0 with radius 1 (clamp).

🏋️ **3.** Write `Image gaussianBlurFast(const Image& image, double sigma)` using three `boxBlurFast` passes. Which box radius gives about the right σ? (Hint: a box of radius r has variance r(r + 1)/3; three passes have three times that.)

🏋️ **4.** Blur only **across** (rows), not down: a "motion blur", as if the camera moved sideways. Write it with `blurRows` and a box of radius 10.

🏋️ **5.** Blur the scene with σ = 8 using all four edge modes and compare the borders.

🏋️ **6.** Make a "glow": blur a copy of the scene strongly (σ = 6), then mix it with the original — for each channel, new = original + 0.5 × blurred, clamped.

🏋️ **7.** Make a "tilt-shift" effect: blur only the top and bottom thirds of a picture, keep the middle sharp.

🏋️ **8.** Why is the separable trick impossible for most kernels? Give a 3 × 3 kernel that is **not** separable.

---

## Answers

**1.**
> g(0) = 1; g(±1) = e^(−1 / 0.5) = e^(−2) = 0.1353; g(±2) = e^(−4 / 0.5) = e^(−8) = 0.000335.
> sum = 1 + 2 × (0.1353 + 0.000335) = 1.2713 → **0.7866**, **0.1065**, **0.0003** ✓.

**2.**
> start (x = 0): clamp(−1) = 0, so 0 + 0 + 0 = 0 → 0.
> x = 1: + 90 (x + 1 = 2) − 0 → 90 → **30**; x = 2: + 0 (3) − 0 (0) → 90 → **30**; x = 3: + 0 (4) − 0 (1) → 90 → **30**; x = 4: + 0 (5 → 4) − 90 (2) → 0 → **0**.
> Result: 0 30 30 30 0 — the same as Chapter 49's box.

**3.**

```cpp
Image gaussianBlurFast(const Image& image, double sigma) {
    const int r = std::max(1, static_cast<int>(std::lround((std::sqrt(4.0 * sigma * sigma + 1.0) - 1.0) / 2.0)));
    return boxBlurFast(boxBlurFast(boxBlurFast(image, r), r), r);
}
```

> We want 3 × r(r + 1)/3 = r(r + 1) = σ², so r ≈ (√(4σ² + 1) − 1) / 2. For σ = 3: r ≈ 2.54 → **3** (σ ≈ 3.46). Whole-number radii only come close; that is the price of speed. (Rounding between the three passes also adds a little error.)

**4.**

```cpp
Image motionBlur(const Image& image) {
    return fromPixelsF(blurRows(toPixelsF(image, true), boxWeights(10), EdgeMode::Clamp), true);
}
```

**5.**
> Clamp: the borders look natural. Zero: a dark frame, about 2σ = 16 pixels wide, fading inwards. Mirror: very like clamp, slightly different in the corners. Wrap: the green hills appear at the top of the sky and the sky colour at the bottom; the left and right edges mix.

**6.**

```cpp
Image glow = scene;
const Image soft = gaussianBlur(scene, 6.0);
for (int y = 0; y < scene.height(); ++y) {
    for (int x = 0; x < scene.width(); ++x) {
        const Colour a = scene.getPixel(x, y);
        const Colour b = soft.getPixel(x, y);
        glow.setPixel(x, y, Colour{clampByte(a.r + 0.5 * b.r), clampByte(a.g + 0.5 * b.g),
                                   clampByte(a.b + 0.5 * b.b)});
    }
}
```

> (Even better in linear light: add `toLinear` values and convert back.)

**7.**
> Make `blurred = gaussianBlur(picture, 4.0)`. Copy the rows y < height / 3 and y ≥ 2 × height / 3 from `blurred` into a copy of the picture, and keep the middle rows from the original. For a smoother look, mix the two with a weight that changes gradually near the borders of the middle third (Chapter 13's `lerpColour`).

**8.**
> A separable kernel must have weights w[j] × w[i]: every row is a multiple of the same row. The Laplacian `0 1 0 / 1 −4 1 / 0 1 0` (Chapter 49, Practice 3) is not: its first row (0 1 0) and middle row (1 −4 1) are not multiples of each other. So it must be done as a full 2D convolution (it is small, so that is cheap).

---

## Summary

🧠 The **Gaussian** weights e^(−x² / 2σ²) fade smoothly; **σ** sets the width; a radius of ⌈3σ⌉ keeps almost all of the bell. **Normalise** so the weights add up to 1.

🧠 The 2D Gaussian (and the box) is **separable**: blur across, then down — 2n instead of n² multiplications. Keep doubles between the passes.

🧠 A **running sum** makes the box blur cost the same at any radius; three box passes give a good Gaussian (σ² adds up).

🧠 Blur in **linear light**; otherwise bright edges get dark rims.

🧠 **Blur before shrinking** to prevent aliasing (false patterns).

---

## Next chapter

Blurring removes fine detail. Can we do the **opposite**? In Chapter 51 we **sharpen**: subtract a blurred copy to find the detail, then add it back stronger (the "unsharp mask"). And we find **edges** with the **Sobel** kernels: two small kernels that measure how fast the brightness changes across and down, combined with Pythagoras (Chapter 29) into an edge strength — and, with `atan2` (Chapter 30), an edge **direction**.
