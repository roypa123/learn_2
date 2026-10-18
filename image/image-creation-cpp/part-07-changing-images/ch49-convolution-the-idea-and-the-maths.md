# Chapter 49 — Convolution: the Idea and the Maths

> **Part 7 · Chapter 49 of 82**
> **You need:** Chapters 1–48 (especially 6, 14, 17, 35 and 47) · **You will make:** `convolve.h` (kernels, four ways to handle the picture's edges, and the convolution itself), and `kernels.png`: one picture through six different kernels

---

## What you will learn

- Why blurring, sharpening and edge finding need a pixel's **neighbours**.
- What a **kernel** is: a small grid of weights.
- The convolution sum — "neighbour × weight, add them up" — worked slowly with numbers.
- What different weights do: copy, average, move, compare.
- Why the **sum of the weights** matters.
- Four ways to deal with pixels near the **edge** of the picture.
- Why the result must go into a **new** picture.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **neighbourhood** | A pixel and the pixels around it. |
| **kernel** | A small grid of numbers (weights) that says how much each neighbour counts. |
| **weight** | How much one neighbour counts in the sum. |
| **convolution** | Sliding a kernel over a picture and computing "neighbour × weight, added up" at every pixel. |
| **radius** | How far a kernel reaches from its centre: 1 for 3 × 3, 2 for 5 × 5. |
| **edge mode** | The rule for pixels that would lie outside the picture. |
| **in place** | Writing the results into the same picture you are reading from. |

---

## 49.1 Looking at neighbours

Chapter 47's point operations look at one pixel at a time. Its Practice 8 asked: why can't a point operation **blur** a picture? Because blurring means "make each pixel more like the pixels **around** it". You cannot do that without looking at them.

📖 **New word: neighbourhood** — a pixel together with the pixels around it. For a 3 × 3 neighbourhood, that is the pixel itself and its 8 neighbours:

```
   (x−1, y−1)  (x, y−1)  (x+1, y−1)
   (x−1, y)    (x, y)    (x+1, y)
   (x−1, y+1)  (x, y+1)  (x+1, y+1)
```

Blurring, sharpening and edge detection all do the same thing with a neighbourhood: they take the neighbours' values, multiply each by a number, and add up the results. Only the numbers differ. That one method is called **convolution**.

---

## 49.2 Kernels and weights

📖 **New words: kernel and weight** — a **kernel** is a small grid of numbers, the same shape as the neighbourhood. Each number is a **weight**: how much that neighbour counts.

```
   a 3 × 3 kernel            means
   ┌─────┬─────┬─────┐
   │ 1/9 │ 1/9 │ 1/9 │       new pixel = 1/9 × (each of the 9 pixels), added up
   ├─────┼─────┼─────┤                 = the average of the neighbourhood
   │ 1/9 │ 1/9 │ 1/9 │
   ├─────┼─────┼─────┤
   │ 1/9 │ 1/9 │ 1/9 │
   └─────┴─────┴─────┘
```

Kernels have an **odd** size — 3 × 3, 5 × 5, 7 × 7 — so that they have a **centre**, which sits on the pixel being computed.

📖 **New word: radius** — how far the kernel reaches from its centre: r = size / 2 (in whole numbers). 3 × 3 → r = 1; 5 × 5 → r = 2; 9 × 9 → r = 4.

In our code, a kernel is its size and a list of size × size weights, row by row (the same "y × width + x" order as pixels, Chapter 6):

```cpp
struct Kernel {
    int size = 1;
    std::vector<double> weights;
};
```

---

## 49.3 The convolution sum

📖 **New word: convolution** — put the kernel's centre on a pixel, multiply every weight by the pixel under it, add up all the products: that is the new value of the centre pixel. Then move to the next pixel and do it again — for every pixel of the picture.

🔢 **Maths: the formula**

> new(x, y) = Σ over j = 0 … size − 1, i = 0 … size − 1 of **w[j][i] × old(x + i − r, y + j − r)**

(Σ, the Greek letter "sigma", means "add up all of these".) The weight in column i, row j of the kernel meets the pixel i − r across and j − r down from the centre. For a 3 × 3 kernel (r = 1), i − r and j − r go from −1 to +1.

🔢 **Maths: a dot, averaged**

The program's first grid is 5 × 5, all 0 except one pixel of 90 in the middle. We use the 3 × 3 averaging kernel (all weights 1/9).

> at the centre (2, 2): the 9 pixels are 0, 0, 0, 0, 90, 0, 0, 0, 0 → 90 / 9 = **10**
> at (1, 1): its neighbourhood (0 … 2, 0 … 2) contains the dot at its bottom-right corner → 90 / 9 = **10**
> at (0, 0): its neighbourhood does not reach (2, 2) → **0**

```
a dot:                          3 x 3 box (average):
     0   0   0   0   0               0   0   0   0   0
     0   0   0   0   0               0  10  10  10   0
     0   0  90   0   0               0  10  10  10   0
     0   0   0   0   0               0  10  10  10   0
     0   0   0   0   0               0   0   0   0   0
```

The dot has **spread out** into a 3 × 3 square, nine times fainter. That is blurring. And the total stays the same: 9 × 10 = 90.

🔢 **Maths: an edge, averaged**

The second grid has a sharp edge: columns 0 … 1 are 0, columns 2 … 4 are 90.

> column 1: it reads columns 0, 1, 2 → each row gives 0 + 0 + 90 = 90; three rows: 270 / 9 = **30**
> column 2: it reads columns 1, 2, 3 → each row gives 0 + 90 + 90 = 180; three rows: 540 / 9 = **60**
> column 3: all 90 → **90**

```
an edge:                        3 x 3 box:
     0   0  90  90  90               0  30  60  90  90
     ...                             ...
```

The hard step 0 → 90 has become a soft ramp 0, 30, 60, 90. That is what a blurred edge looks like.

---

## 49.4 What the weights do

Different weights, different effects. The program tries a few on the edge grid.

### The identity kernel

```
   0 0 0
   0 1 0
   0 0 0
```

Only the centre counts, with weight 1: every pixel stays the same. It is the "do nothing" kernel, like Chapter 47's identity table.

### The shift kernel

```
   0 0 0
   1 0 0          weight 1 on the LEFT neighbour
   0 0 0
```

new(x, y) = old(x − 1, y): every pixel takes the value of its **left** neighbour — so the **picture moves one pixel to the right**:

```
shift kernel (weight 1 on the left neighbour):
     0   0   0  90  90
```

The edge was between columns 1 and 2; now it is between 2 and 3. (Column 0 copies the pixel left of the picture — see Section 49.6.)

⚠️ A weight on the **left** moves the picture to the **right**. This surprises everyone the first time. Think of it as "each pixel **looks** left and copies what it sees".

### The difference kernel

```
   0  0  0
  −1  0  1        right neighbour minus left neighbour
   0  0  0
```

new(x, y) = old(x + 1, y) − old(x − 1, y). Where the picture is flat, both neighbours are equal and the result is **0**. Where it changes from left to right, the result is big:

```
difference kernel (right - left):
     0  90  90   0   0
```

Only columns 1 and 2 — the two pixels beside the edge — light up. This is the start of **edge detection** (Chapter 51).

### The sum of the weights

```
weights add up to: box 1, identity 1, difference 0
```

🧠 **Remember:**

> weights add up to **1** → a flat area keeps its value: the picture keeps its **brightness** (blur, sharpen, shift)
> weights add up to **0** → a flat area becomes **0**: only **changes** remain (edge kernels)
> weights add up to 2 → everything twice as bright; ½ → half as bright

🔢 **Maths: why**

> on a flat area where every pixel is v: new = Σ w × v = v × (Σ w)

---

## 49.5 Convolution or correlation?

A small honesty note. Mathematicians define **convolution** with the kernel **flipped**: the weight at the top-left multiplies the pixel at the **bottom-right**. What we compute (without the flip) is properly called **correlation**.

For **symmetric** kernels — the box, the identity, the blurs of Chapter 50 — flipping changes nothing, so the two are the same. For the shift kernel, flipping would move the picture the other way. Image-processing programs nearly always do what we do and call it "convolution" anyway; just remember that a kernel's **direction** depends on this choice.

---

## 49.6 The edges of the picture

At pixel (0, 0), a 3 × 3 kernel wants pixel (−1, −1), which does not exist. What do we use instead?

📖 **New word: edge mode** — the rule for positions outside the picture. Our `edgeIndex(i, n, mode)` turns a position i (in a row or column of n pixels) into a real position, or −1 for "use black":

| mode | i = −1 | i = −2 | i = n (one past the end) | idea |
|---|---|---|---|---|
| **Zero** | black | black | black | the world outside is black |
| **Clamp** | 0 | 0 | n − 1 | repeat the edge pixel (Chapter 35's `getPixelClamped`) |
| **Mirror** | 0 | 1 | n − 1 | the picture continues as its mirror image |
| **Wrap** | n − 1 | n − 2 | 0 | the picture repeats like a tile |

🔢 **Maths: the row 100 80 60 40 20, averaged across**

We use a kernel that averages only **across** (weights 1/3, 1/3, 1/3 in its middle row), on a 5 × 1 picture.

> pixel 0 needs the pixel at −1:
> **zero**: (0 + 100 + 80) / 3 = **60**
> **clamp**: (100 + 100 + 80) / 3 = 93.3 → **93**
> **mirror**: −1 → 0, the same as clamp → **93**
> **wrap**: −1 → 4, the pixel 20: (20 + 100 + 80) / 3 = 66.7 → **67**
> pixel 4 needs the pixel at 5: zero → **20**, clamp and mirror → (40 + 20 + 20) / 3 = **27**, wrap → (40 + 20 + 100) / 3 = **53**

```
the row 100 80 60 40 20, averaged across:
  zero      60  80  60  40  20
  clamp     93  80  60  40  27
  mirror    93  80  60  40  27
  wrap      67  80  60  40  53
  index -2 with mirror: 1, with clamp: 0, with wrap: 3
```

The middle pixels do not care. At the ends:

- **Zero** makes the border **darker** — a dark frame appears around a blurred picture.
- **Wrap** mixes the **other side** in: here the left end got some of the dark right end. Good only for pictures that really repeat (textures, Part 8).
- **Clamp** and **Mirror** keep the edges natural. With a 3 × 3 kernel they are the same; with bigger kernels they differ: at −2, clamp still repeats the edge pixel, but mirror uses pixel **1**.

We use **Clamp** as the default. (Chapter 35 promised this choice for blurring; Chapter 50 uses it.)

🔢 **Maths: the mirror rule for any position**

> the mirrored picture repeats every 2n pixels: … 4 3 2 1 0 | 0 1 2 3 4 | 4 3 2 1 0 | 0 1 …
> m = i mod 2n (made positive); if m < n → m, else → 2n − 1 − m
> i = −2, n = 5: −2 mod 10 = 8 → 8 ≥ 5 → 2 × 5 − 1 − 8 = **1** ✓

---

## 49.7 Always into a new picture

📖 **New word: in place** — writing each result back into the picture you are still reading from.

It is tempting: no second picture, less memory. But it is **wrong**: when we compute pixel x, pixel x − 1 has **already** been changed, and the kernel reads the **new** value instead of the old one.

🔢 **Maths: the row 0 0 90 0 0 0 0, averaged across**

> correct (a new picture): x = 1: (0 + 0 + 90) / 3 = 30; x = 2: 30; x = 3: 30 → `0 30 30 30 0 0 0`
> in place: x = 1 → 30 (written back); x = 2: (**30** + 90 + 0) / 3 = **40**; x = 3: (**40** + 0 + 0) / 3 = **13**; x = 4: 13 / 3 = **4** …

```
the row 0 0 90 0 0 0 0, averaged into a new picture:
     0  30  30  30   0   0   0
averaged in place (wrong):
     0  30  40  13   4   1   0
```

The in-place result is lopsided: it smears to the **right**, the direction we walked. That is why `convolve` always makes a new picture `out` and only reads from `src`.

---

## 49.8 Colours, rounding and light

**Colours.** We convolve red, green and blue separately, with the same kernel. `convolvePixel` adds up `ColourF` values (Chapter 14), so all three channels are done at once.

**Rounding and clamping.** The sum is a `double`. It can be fractional (93.33) or outside the range: a difference kernel can give −90, a sharpening kernel 300. `writePixel` clamps to 0 … 1 and rounds (Chapter 14's `toColour`). Negative edge values therefore become 0 — Chapter 51 will show how to keep them.

**Light.** Averaging is mixing, and Chapter 17 taught that mixing should happen in **linear light**. `convolve` has a `linearLight` choice: `false` (the default) works directly on the sRGB bytes, as the worked numbers in this chapter do; `true` turns each pixel into linear light first (`toLinear`) and back afterwards (`fromLinear`). For blurring, linear light is more correct — a blurred bright light stays bright instead of turning muddy; Chapter 50 compares the two.

---

## 49.9 How much work?

Each output value needs size × size multiplications.

🔢 **Maths: a photo**

> 1920 × 1080 pixels × 3 channels = 6,220,800 values
> 3 × 3 kernel: × 9 = **55,987,200** multiplications
> 15 × 15 kernel: × 225 = **1,399,680,000** — about 1.4 billion

```
multiplications for a 1920 x 1080 photo: 3 x 3 kernel 55987200, 15 x 15 kernel 1399680000
```

A modern computer does that in a second or two, but big blurs get slow fast: the work grows with the **square** of the size. Chapter 50 shows two tricks that make big blurs almost as fast as small ones.

---

## 49.10 Six kernels on a picture

The program applies six kernels to Chapter 47's scene and saves them side by side in `kernels.png`:

| kernel | weights | what you see |
|---|---|---|
| identity | centre 1 | the scene, unchanged |
| box 3 × 3 | nine × 1/9 | slightly soft |
| box 9 × 9 | 81 × 1/81 | very blurred; the edges are wide ramps |
| sharpen | centre 5, four neighbours −1 | edges look crisper (Chapter 51 explains why) |
| edges (x) | −1 0 1 / −2 0 2 / −1 0 1 | black, with bright lines where the colour **rises** from left to right |
| shift | left neighbour 1 | the scene moved one pixel right |

The sharpen kernel's weights add up to 5 − 4 = 1 (brightness stays); the edge kernel's add up to 0 (flat areas turn black).

---

## Code, part 1: `convolve.h`

File: `common/convolve.h` (new). It includes `histogram.h` — the end of the drawing chain (Chapters 47–48), which brings in colours, linear light and drawing.

```cpp
#ifndef CONVOLVE_H
#define CONVOLVE_H

#include <algorithm>
#include <vector>
#include "histogram.h"

struct Kernel {
    int size = 1;
    std::vector<double> weights;
};

enum class EdgeMode { Zero, Clamp, Mirror, Wrap };

inline double kernelSum(const Kernel& k) {
    double sum = 0.0;
    for (double w : k.weights) {
        sum += w;
    }
    return sum;
}

inline Kernel identityKernel() {
    return Kernel{3, {0, 0, 0, 0, 1, 0, 0, 0, 0}};
}

inline Kernel boxKernel(int size) {
    return Kernel{size, std::vector<double>(size * size, 1.0 / (size * size))};
}

inline int edgeIndex(int i, int n, EdgeMode mode) {
    if (i >= 0 && i < n) {
        return i;
    }
    if (mode == EdgeMode::Zero) {
        return -1;
    }
    if (mode == EdgeMode::Clamp) {
        return std::clamp(i, 0, n - 1);
    }
    if (mode == EdgeMode::Mirror) {
        const int period = 2 * n;
        int m = i % period;
        if (m < 0) {
            m += period;
        }
        return (m < n) ? m : period - 1 - m;
    }
    int m = i % n;
    if (m < 0) {
        m += n;
    }
    return m;
}

inline ColourF readPixel(const Image& src, int x, int y, EdgeMode mode, bool linearLight) {
    const int ex = edgeIndex(x, src.width(), mode);
    const int ey = edgeIndex(y, src.height(), mode);
    if (ex < 0 || ey < 0) {
        return ColourF{0.0, 0.0, 0.0};
    }
    const Colour c = src.getPixel(ex, ey);
    return linearLight ? toLinear(c) : toColourF(c);
}

inline Colour writePixel(ColourF value, bool linearLight) {
    return linearLight ? fromLinear(value) : toColour(value);
}

inline Colour convolvePixel(const Image& src, int x, int y, const Kernel& k, EdgeMode mode,
                            bool linearLight) {
    const int r = k.size / 2;
    ColourF sum{0.0, 0.0, 0.0};
    for (int j = 0; j < k.size; ++j) {
        for (int i = 0; i < k.size; ++i) {
            const double w = k.weights[j * k.size + i];
            if (w != 0.0) {
                sum = sum + readPixel(src, x + i - r, y + j - r, mode, linearLight) * w;
            }
        }
    }
    return writePixel(sum, linearLight);
}

inline Image convolve(const Image& src, const Kernel& k, EdgeMode mode = EdgeMode::Clamp,
                      bool linearLight = false) {
    Image out(src.width(), src.height());
    for (int y = 0; y < src.height(); ++y) {
        for (int x = 0; x < src.width(); ++x) {
            out.setPixel(x, y, convolvePixel(src, x, y, k, mode, linearLight));
        }
    }
    return out;
}

#endif
```

### Line by line

**Kernels (lines 1–29)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–6 | include guard and `#include` lines | `std::clamp`, lists, and everything up to Chapter 48. |
| 8–11 | `struct Kernel { int size = 1; std::vector<double> weights; };` | A kernel: its size (odd) and size × size weights, row by row (Section 49.2). |
| 13 | `enum class EdgeMode { Zero, Clamp, Mirror, Wrap };` | The four edge modes of Section 49.6, as named choices (Chapter 25's `FillRule` used the same idea). |
| 15–21 | `inline double kernelSum(const Kernel& k) { double sum = 0.0; for (double w : k.weights) { sum += w; } return sum; }` | The sum of the weights (Section 49.4). |
| 23–25 | `inline Kernel identityKernel() { return Kernel{3, {0, 0, 0, 0, 1, 0, 0, 0, 0}}; }` | The "do nothing" kernel. |
| 27–29 | `inline Kernel boxKernel(int size) { return Kernel{size, std::vector<double>(size * size, 1.0 / (size * size))}; }` | The averaging kernel: size × size equal weights that add up to 1. `std::vector<double>(count, value)` makes a list of `count` copies of `value`. |

**Edges (lines 31–54)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 31–34 | `inline int edgeIndex(int i, int n, EdgeMode mode) { if (i >= 0 && i < n) { return i; }` | A position inside the picture is used as it is, whatever the mode. |
| 35–37 | `if (mode == EdgeMode::Zero) { return -1; }` | −1 means "outside: use black". |
| 38–40 | `if (mode == EdgeMode::Clamp) { return std::clamp(i, 0, n - 1); }` | The nearest edge pixel. |
| 41–48 | `if (mode == EdgeMode::Mirror) { const int period = 2 * n; int m = i % period; if (m < 0) { m += period; } return (m < n) ? m : period - 1 - m; }` | The mirror rule of Section 49.6. In C++, `%` of a negative number is negative or 0 (−2 % 10 = −2), so we add the period to make it positive. |
| 49–54 | `int m = i % n; if (m < 0) { m += n; } return m;` `}` | Wrap: the position "mod n", made positive. |

**Reading and writing (lines 56–68)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 56–61 | `inline ColourF readPixel(const Image& src, int x, int y, EdgeMode mode, bool linearLight) { const int ex = edgeIndex(x, src.width(), mode); const int ey = edgeIndex(y, src.height(), mode); if (ex < 0 \|\| ey < 0) { return ColourF{0.0, 0.0, 0.0}; }` | Turn (x, y) into a real pixel by the edge mode, or black. |
| 62–64 | `const Colour c = src.getPixel(ex, ey); return linearLight ? toLinear(c) : toColourF(c);` `}` | The pixel as 0 … 1 numbers: linear light (Chapter 17) or the plain sRGB values / 255 (Chapter 14). |
| 66–68 | `inline Colour writePixel(ColourF value, bool linearLight) { return linearLight ? fromLinear(value) : toColour(value); }` | Back to bytes. Both clamp to 0 … 1 and round (Section 49.8). |

**The convolution (lines 70–96)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 70–73 | `inline Colour convolvePixel(const Image& src, int x, int y, const Kernel& k, EdgeMode mode, bool linearLight) { const int r = k.size / 2; ColourF sum{0.0, 0.0, 0.0};` | One output pixel. `r` is the radius. |
| 74–76 | `for (int j = 0; j < k.size; ++j) { for (int i = 0; i < k.size; ++i) { const double w = k.weights[j * k.size + i];` | Every weight: row j, column i. |
| 77–81 | `if (w != 0.0) { sum = sum + readPixel(src, x + i - r, y + j - r, mode, linearLight) * w; } } }` | Add neighbour × weight (Section 49.3). Weights of 0 are skipped: they add nothing, and reading costs time. |
| 82–83 | `return writePixel(sum, linearLight);` `}` | The result as a colour. |
| 85–87 | `inline Image convolve(const Image& src, const Kernel& k, EdgeMode mode = EdgeMode::Clamp, bool linearLight = false) { Image out(src.width(), src.height());` | A **new** picture of the same size (Section 49.7). Clamp edges and sRGB values unless asked otherwise. |
| 88–94 | `for (...) { for (...) { out.setPixel(x, y, convolvePixel(src, x, y, k, mode, linearLight)); } } return out; }` | Every pixel: read only from `src`, write only to `out`. |
| 96 | `#endif` | End of the include guard. |

---

## Code, part 2: kernels at work

File: `ch49/convolve.cpp`

```cpp
#include <iostream>
#include <string>
#include <vector>
#include "convolve.h"
#include "deflate.h"

std::string padLeft(const std::string& text, int width) {
    std::string s = text;
    while (static_cast<int>(s.size()) < width) {
        s = " " + s;
    }
    return s;
}

Image greyGrid(int width, int height, const std::vector<int>& values) {
    Image grid(width, height);
    for (int i = 0; i < width * height; ++i) {
        const std::uint8_t g = static_cast<std::uint8_t>(values[i]);
        grid.setPixel(i % width, i / width, Colour{g, g, g});
    }
    return grid;
}

void printGrid(const std::string& title, const Image& grid) {
    std::cout << title << "\n";
    for (int y = 0; y < grid.height(); ++y) {
        std::cout << "  ";
        for (int x = 0; x < grid.width(); ++x) {
            std::cout << padLeft(std::to_string(grid.getPixel(x, y).r), 4);
        }
        std::cout << "\n";
    }
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
    const Image dot = greyGrid(5, 5, {0, 0, 0,  0, 0,
                                      0, 0, 0,  0, 0,
                                      0, 0, 90, 0, 0,
                                      0, 0, 0,  0, 0,
                                      0, 0, 0,  0, 0});
    printGrid("a dot:", dot);
    printGrid("3 x 3 box (average):", convolve(dot, boxKernel(3)));

    const Image edge = greyGrid(5, 5, {0, 0, 90, 90, 90,
                                       0, 0, 90, 90, 90,
                                       0, 0, 90, 90, 90,
                                       0, 0, 90, 90, 90,
                                       0, 0, 90, 90, 90});
    printGrid("an edge:", edge);
    printGrid("3 x 3 box:", convolve(edge, boxKernel(3)));
    const Kernel shiftRight{3, {0, 0, 0, 1, 0, 0, 0, 0, 0}};
    printGrid("shift kernel (weight 1 on the left neighbour):", convolve(edge, shiftRight));
    const Kernel difference{3, {0, 0, 0, -1, 0, 1, 0, 0, 0}};
    printGrid("difference kernel (right - left):", convolve(edge, difference));
    std::cout << "weights add up to: box " << kernelSum(boxKernel(3)) << ", identity "
              << kernelSum(identityKernel()) << ", difference " << kernelSum(difference) << "\n";

    const Image row = greyGrid(5, 1, {100, 80, 60, 40, 20});
    const Kernel across{3, {0, 0, 0, 1.0 / 3, 1.0 / 3, 1.0 / 3, 0, 0, 0}};
    const EdgeMode modes[4] = {EdgeMode::Zero, EdgeMode::Clamp, EdgeMode::Mirror, EdgeMode::Wrap};
    const std::string modeNames[4] = {"zero", "clamp", "mirror", "wrap"};
    std::cout << "\nthe row 100 80 60 40 20, averaged across:\n";
    for (int m = 0; m < 4; ++m) {
        const Image result = convolve(row, across, modes[m]);
        std::cout << "  " << modeNames[m] << std::string(8 - modeNames[m].size(), ' ');
        for (int x = 0; x < 5; ++x) {
            std::cout << padLeft(std::to_string(result.getPixel(x, 0).r), 4);
        }
        std::cout << "\n";
    }
    std::cout << "  index -2 with mirror: " << edgeIndex(-2, 5, EdgeMode::Mirror) << ", with clamp: "
              << edgeIndex(-2, 5, EdgeMode::Clamp) << ", with wrap: " << edgeIndex(-2, 5, EdgeMode::Wrap)
              << "\n";

    const Image spike = greyGrid(7, 1, {0, 0, 90, 0, 0, 0, 0});
    Image inPlace = spike;
    for (int x = 0; x < 7; ++x) {
        inPlace.setPixel(x, 0, convolvePixel(inPlace, x, 0, across, EdgeMode::Clamp, false));
    }
    printGrid("\nthe row 0 0 90 0 0 0 0, averaged into a new picture:", convolve(spike, across));
    printGrid("averaged in place (wrong):", inPlace);

    const Image scene = makeScene();
    const Kernel kernels[6] = {identityKernel(), boxKernel(3), boxKernel(9),
                               Kernel{3, {0, -1, 0, -1, 5, -1, 0, -1, 0}},
                               Kernel{3, {-1, 0, 1, -2, 0, 2, -1, 0, 1}}, shiftRight};
    const std::string names[6] = {"identity", "box 3 x 3", "box 9 x 9", "sharpen", "edges (x)", "shift"};
    Image sheet(3 * 170 + 10, 2 * 134 + 10, colours::white);
    for (int i = 0; i < 6; ++i) {
        const Image result = convolve(scene, kernels[i]);
        const int left = 10 + (i % 3) * 170;
        const int top = 10 + (i / 3) * 134;
        for (int y = 0; y < result.height(); ++y) {
            for (int x = 0; x < result.width(); ++x) {
                sheet.setPixel(left + x, top + y, result.getPixel(x, y));
            }
        }
        drawText(sheet, left, top + 114, names[i], colours::black);
    }
    if (!savePNGCompressed(sheet, "kernels.png")) {
        std::cout << "could not write kernels.png\n";
        return 1;
    }
    const long long photo = 1920LL * 1080 * 3;
    std::cout << "\nmultiplications for a 1920 x 1080 photo: 3 x 3 kernel " << photo * 9
              << ", 15 x 15 kernel " << photo * 225 << "\n";
    std::cout << "wrote kernels.png\n";
    return 0;
}
```

Build and run it from the `code/ch49` folder:

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common convolve.cpp -o convolve
./convolve
```

### Line by line

**Helpers (lines 1–49)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–5 | the `#include` lines | Printing, strings, lists, the new header and `deflate.h` for saving. |
| 7–13 | `std::string padLeft(...)` | Columns. |
| 15–22 | `Image greyGrid(int width, int height, const std::vector<int>& values) { ... grid.setPixel(i % width, i / width, Colour{g, g, g}); ... }` | A small grey picture from a list of numbers, row by row. |
| 24–33 | `void printGrid(const std::string& title, const Image& grid) { ... grid.getPixel(x, y).r ... }` | Print a grey picture as a grid of numbers (the red value; all three are equal). |
| 35–49 | `Image makeScene() { ... }` | Chapter 47's scene. |

**Small grids (lines 52–72)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 52–58 | `const Image dot = greyGrid(5, 5, {...}); printGrid("a dot:", dot); printGrid("3 x 3 box (average):", convolve(dot, boxKernel(3)));` | Section 49.3's dot. The numbers are written in a 5 × 5 layout so you can see the picture in the code. |
| 60–66 | `const Image edge = greyGrid(5, 5, {...}); ... convolve(edge, boxKernel(3)) ...` | Section 49.3's edge. |
| 67–70 | `const Kernel shiftRight{3, {0, 0, 0, 1, 0, 0, 0, 0, 0}}; ... const Kernel difference{3, {0, 0, 0, -1, 0, 1, 0, 0, 0}}; ...` | The shift and difference kernels of Section 49.4. |
| 71–72 | `std::cout << "weights add up to: box " << kernelSum(boxKernel(3)) << ...` | Section 49.4's sums. |

**Edge modes and the in-place bug (lines 74–97)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 74–77 | `const Image row = greyGrid(5, 1, {100, 80, 60, 40, 20}); const Kernel across{3, {0, 0, 0, 1.0 / 3, 1.0 / 3, 1.0 / 3, 0, 0, 0}}; const EdgeMode modes[4] = {...}; const std::string modeNames[4] = {...};` | A one-row picture and a kernel that averages across only. |
| 78–86 | `for (int m = 0; m < 4; ++m) { const Image result = convolve(row, across, modes[m]); ... }` | One line per edge mode (Section 49.6). |
| 87–89 | `std::cout << "  index -2 with mirror: " << edgeIndex(-2, 5, EdgeMode::Mirror) << ...` | Where position −2 lands in each mode. |
| 91–95 | `const Image spike = greyGrid(7, 1, {...}); Image inPlace = spike; for (int x = 0; x < 7; ++x) { inPlace.setPixel(x, 0, convolvePixel(inPlace, x, 0, across, EdgeMode::Clamp, false)); }` | The **wrong** way on purpose: read from and write to the same picture (Section 49.7). |
| 96–97 | `printGrid(..., convolve(spike, across)); printGrid("averaged in place (wrong):", inPlace);` | The right result and the wrong one. |

**The picture (lines 99–125)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 99–103 | `const Image scene = makeScene(); const Kernel kernels[6] = {identityKernel(), boxKernel(3), boxKernel(9), Kernel{3, {0, -1, 0, -1, 5, -1, 0, -1, 0}}, Kernel{3, {-1, 0, 1, -2, 0, 2, -1, 0, 1}}, shiftRight}; const std::string names[6] = {...};` | The six kernels of Section 49.10. |
| 104–115 | `Image sheet(...); for (int i = 0; i < 6; ++i) { const Image result = convolve(scene, kernels[i]); ... sheet.setPixel(left + x, top + y, result.getPixel(x, y)); ... drawText(...); }` | Each result in a 3 × 2 grid with its name. |
| 116–119 | `if (!savePNGCompressed(sheet, "kernels.png")) { ... }` | Save it. |
| 120–125 | `const long long photo = 1920LL * 1080 * 3; std::cout << ... photo * 9 << ... photo * 225 << ...` … `}` | Section 49.9's numbers, in `long long` (1.4 billion does not fit in an `int`). |

### What you should see

```
a dot:
     0   0   0   0   0
     0   0   0   0   0
     0   0  90   0   0
     0   0   0   0   0
     0   0   0   0   0
3 x 3 box (average):
     0   0   0   0   0
     0  10  10  10   0
     0  10  10  10   0
     0  10  10  10   0
     0   0   0   0   0
an edge:
     0   0  90  90  90
     0   0  90  90  90
     0   0  90  90  90
     0   0  90  90  90
     0   0  90  90  90
3 x 3 box:
     0  30  60  90  90
     0  30  60  90  90
     0  30  60  90  90
     0  30  60  90  90
     0  30  60  90  90
shift kernel (weight 1 on the left neighbour):
     0   0   0  90  90
     0   0   0  90  90
     0   0   0  90  90
     0   0   0  90  90
     0   0   0  90  90
difference kernel (right - left):
     0  90  90   0   0
     0  90  90   0   0
     0  90  90   0   0
     0  90  90   0   0
     0  90  90   0   0
weights add up to: box 1, identity 1, difference 0

the row 100 80 60 40 20, averaged across:
  zero      60  80  60  40  20
  clamp     93  80  60  40  27
  mirror    93  80  60  40  27
  wrap      67  80  60  40  53
  index -2 with mirror: 1, with clamp: 0, with wrap: 3

the row 0 0 90 0 0 0 0, averaged into a new picture:
     0  30  30  30   0   0   0
averaged in place (wrong):
     0  30  40  13   4   1   0

multiplications for a 1920 x 1080 photo: 3 x 3 kernel 55987200, 15 x 15 kernel 1399680000
wrote kernels.png
```

---

## Small examples

### Example 1 — A 3 × 3 box on a checkerboard

A pixel of 255 with four 0 neighbours (left, right, up, down) and four 255 diagonal neighbours: (5 × 255 + 4 × 0) / 9 = 141.7 → **142**. A fine checkerboard becomes almost flat grey: blur removes fine patterns.

### Example 2 — Shifting down

Weight 1 at the **top** middle (row 0, column 1): new(x, y) = old(x, y − 1). The picture moves one pixel **down**.

### Example 3 — A kernel that brightens

All weights 0 except the centre, 1.5: a point operation in disguise ("× 1.5"). Its weights add up to 1.5: every flat area becomes 1.5 times brighter.

### Example 4 — The radius of a 7 × 7 kernel

r = 7 / 2 = **3**: it reads pixels from x − 3 to x + 3.

### Example 5 — Mirror at the far end

n = 5, i = 6: 6 mod 10 = 6 ≥ 5 → 9 − 6 = **3**. (The mirror continues 4, 3, 2, … after the last pixel 4: position 5 is 4, position 6 is 3.)

---

## Common mistakes

⚠️ **Convolving in place** — results smear in the direction of the loop. Always write into a new picture.

⚠️ **Reading outside the picture** — every position must go through the edge mode. `getPixel` would return black (Chapter 11), which is the Zero mode whether you want it or not.

⚠️ **Weights that do not add up to 1** — the picture gets brighter or darker. Check `kernelSum` (unless you want 0, for edges).

⚠️ **Rounding inside the sum** — add up in `double` and round once at the end.

⚠️ **An even kernel size** — 4 × 4 has no centre, and the picture shifts by half a pixel.

⚠️ **Mixing up the direction** — a weight on the left neighbour moves the picture right (Section 49.4).

---

## Practice

🏋️ **1.** Convolve the 3 × 3 grey patch `10 20 30 / 40 50 60 / 70 80 90` with the box kernel at its centre. Then with the difference kernel.

🏋️ **2.** Write the kernel that moves a picture one pixel **up and to the left** (diagonally).

🏋️ **3.** What do the weights `0 1 0 / 1 −4 1 / 0 1 0` add up to? Apply them to the dot grid of Section 49.3 at the centre and at (1, 2). What kind of kernel is it?

🏋️ **4.** Convolve the edge grid with the 3 × 3 box **twice**. What are the new values in the middle row? Is it the same as one 5 × 5 box?

🏋️ **5.** Write `Kernel crossKernel()`: the average of the centre and its 4 direct neighbours (5 weights of 1/5). Compare its blur with the 3 × 3 box.

🏋️ **6.** Try `convolve(scene, boxKernel(9), EdgeMode::Zero)` and `EdgeMode::Wrap`. Describe what happens at the borders.

🏋️ **7.** A 1-row picture `0 0 0 255 0 0 0` and the kernel with weights 1/4, 1/2, 1/4 across. What comes out? What do the weights add up to?

🏋️ **8.** Why does `convolvePixel` skip weights that are exactly 0? Would the result change if it did not skip them?

---

## Answers

**1.**
> Box: (10 + 20 + … + 90) / 9 = 450 / 9 = **50**.
> Difference (right − left in the middle row): 60 − 40 = **20**.

**2.**
> Each pixel must copy its neighbour **below and to the right**: weight 1 at row 2, column 2 (the bottom-right corner): `0 0 0 / 0 0 0 / 0 0 1`.

**3.**
> 1 + 1 + 1 + 1 − 4 = **0**: flat areas become 0 — an edge (or "change") kernel, called the **Laplacian**.
> Centre: 4 × 0 − 4 × 90 = −360 → clamped to **0**. At (1, 2) (left of the dot): its right neighbour is 90 → **90**.
> It finds places that differ from the average of their neighbours. The negative value at the dot itself is lost to clamping — Chapter 51 handles that.

**4.**
> After one box: `0 30 60 90 90`. Second box, middle row: column 0 (clamp: 0, 0, 30) → 10; column 1: (0 + 30 + 60) / 3 = **30**; column 2: (30 + 60 + 90) / 3 = **60**; column 3: (60 + 90 + 90) / 3 = **80**; column 4: **90** → `10 30 60 80 90`. (All rows are the same, so the vertical part changes nothing.) Not the same as a 5 × 5 box: two boxes weight the centre **more** than the sides — the start of the bell shape of Chapter 50.

**5.**

```cpp
Kernel crossKernel() {
    const double f = 1.0 / 5;
    return Kernel{3, {0, f, 0, f, f, f, 0, f, 0}};
}
```

> It blurs a little less than the 3 × 3 box, and slightly more along the axes than along the diagonals.

**6.**
> **Zero**: a dark frame about 4 pixels wide appears around the picture (black pixels from outside are averaged in). **Wrap**: the top rows get some of the green hills from the bottom, and the bottom rows some of the blue sky from the top; the left and right sides mix too.

**7.**
> x = 2: 1/4 × 255 = 63.75 → **64**; x = 3: 1/2 × 255 = 127.5 → **128**; x = 4: **64** → `0 0 64 128 64 0 0`. The weights add up to 1/4 + 1/2 + 1/4 = **1**. This little kernel is the smallest **Gaussian**-like blur (Chapter 50).

**8.**
> A weight of 0 adds 0 × (pixel) = 0, so the result is exactly the same either way. Skipping just saves time — the shift and difference kernels are mostly zeros.

---

## Summary

🧠 **Convolution**: for every pixel, put the **kernel** on it, multiply each **weight** by the pixel under it, and add up. Kernels have odd sizes; the **radius** is size / 2.

🧠 Weights decide everything: the identity copies, the box **averages** (blurs), a single off-centre 1 **moves** the picture, a difference **finds changes**.

🧠 Weights that add up to **1** keep the brightness; to **0**, they keep only the changes.

🧠 Positions outside the picture need an **edge mode**: Zero (dark border), **Clamp** (our default), Mirror, Wrap.

🧠 Always write into a **new** picture; add up in `double`, then clamp and round once.

🧠 The work grows with size × size — big kernels are slow (Chapter 50 fixes that).

---

## Next chapter

The box kernel blurs, but it is a bit crude: it treats the far corners of the neighbourhood the same as the centre. In Chapter 50 we build the **Gaussian blur**, whose weights follow the smooth bell curve e^(−x²/2σ²), and two tricks that make big blurs fast: **separable** kernels (blur across, then down) and the **running sum** for box blurs. We will also see why blurring before shrinking a picture (Chapter 35) prevents ugly patterns.
