# Chapter 35 — Resizing Images: Nearest and Bilinear

> **Part 5 · Chapter 35 of 82**
> **You need:** Chapters 1–34 (especially 13, 17, 27 and 33) · **You will make:** `resize.h` (nearest-neighbour, bilinear and box resizing, a bilinear sampler, and smooth picture transforms), `zoom.ppm`, `blend.ppm`, `rings.ppm`, `small.ppm` and `turned.ppm`

---

## What you will learn

- That resizing is just the **inverse mapping** of Chapter 33, with a scale.
- The exact formula that sends a new pixel back to the old picture — and why it needs a **+ 0.5**.
- **Nearest-neighbour** resizing: simple, sharp and blocky.
- **Bilinear** resizing: blending the four nearest pixels for smooth results.
- What to do at the **edges** of the picture.
- Why blending must happen in **linear light** (Chapter 17) — and what goes wrong if it does not.
- Why **shrinking** is different: skipping pixels causes **aliasing**, and **averaging** fixes it.
- How to make Chapter 33's turned pictures **smooth**.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **resize** (or **rescale**) | Make a picture bigger or smaller: more or fewer pixels. |
| **enlarge** (upscale) | Make a picture bigger. |
| **shrink** (downscale) | Make a picture smaller. |
| **sample** | Read a colour from a picture at some position (which may be between pixel centres). |
| **nearest neighbour** | Take the colour of the one pixel the position falls in. |
| **bilinear** | Blend the four pixel centres around the position: lerp across, then down. |
| **clamp to edge** | Outside the picture, use the nearest edge pixel instead. |
| **aliasing** | Wrong patterns that appear when fine detail is sampled too sparsely. |
| **moiré** (say "mwah-RAY") | Wavy false patterns caused by aliasing, like on a TV showing a striped shirt. |
| **box filter** | Shrinking by averaging all the old pixels under each new pixel. |
| **pixel art** | Small pictures drawn pixel by pixel, like old video game characters. |

---

## 35.1 Resizing is inverse mapping

📖 **New words: resize, enlarge, shrink** — change the number of pixels: more (enlarge) or fewer (shrink).

Chapter 33 taught us how to make a new picture from an old one with any matrix: for each **new** pixel, ask "where did you come from?", using the inverse matrix. Resizing is the special case where the matrix is a **scale**.

To turn a picture W pixels wide into one w pixels wide, the scale across is w / W. Going **back** (the inverse) divides by it, which means multiplying by:

> **scaleX = W / w** (old width / new width)

and the same for heights. So:

> **source position = ((x + 0.5) × W / w, (y + 0.5) × H / h)**

Why the **+ 0.5**? Because, as always in this book, we map **pixel centres** (Chapter 22): new pixel x has its centre at x + 0.5. The picture covers the area from 0 to W, and from 0 to w in the new one; these two areas must line up exactly, edge to edge.

### What goes wrong without the + 0.5

🔢 **Maths: enlarging 3 pixels to 7**

> scaleX = 3 / 7 = 0.4286
> with + 0.5: x = 0 → 0.21, 1 → 0.64, 2 → 1.07, 3 → 1.50, 4 → 1.93, 5 → 2.36, 6 → 2.79
> floor: **0, 0, 1, 1, 1, 2, 2**
> without + 0.5: x × 0.4286 = 0, 0.43, 0.86, 1.29, 1.71, 2.14, 2.57 → floor: **0, 0, 0, 1, 1, 2, 2**

The program prints both:

```
3 to 7 pixels, source pixel for each new pixel: 0 0 1 1 1 2 2
without the + 0.5: 0 0 0 1 1 2 2
```

With + 0.5, the three old pixels get 2, 3 and 2 new pixels: fair, and symmetric (the middle pixel is in the middle). Without it, the first old pixel gets 3 and the others 2 each: the whole picture is pushed **half a pixel** to the right. Half a pixel sounds small, but resize a picture several times and the shifts add up — and with bilinear blending (below) the shift is plainly visible.

---

## 35.2 Nearest neighbour

📖 **New word: sample** — read a colour from a picture at some position. The position can be anywhere, also between pixel centres.

📖 **New word: nearest neighbour** — the simplest way to sample: take the pixel the position falls **in** (floor of both coordinates, Chapter 33). That pixel's centre is the nearest centre to the position, hence the name.

```cpp
int sx = static_cast<int>(std::floor((x + 0.5) * scaleX));
int sy = static_cast<int>(std::floor((y + 0.5) * scaleY));
result.setPixel(x, y, source.getPixel(sx, sy));
```

This is what Chapter 27's `pasteEnlarged` did by hand, and what Chapter 33's `drawImageTransformed` does with any matrix.

When **enlarging** by a whole number (×16, say), every old pixel becomes a neat 16 × 16 square of copies: the picture looks **blocky**. That is exactly right for:

📖 **New word: pixel art** — small pictures drawn pixel by pixel, where every pixel was placed on purpose (old video games, icons). Enlarging pixel art with nearest neighbour keeps it crisp and true.

For photos, the blocks look ugly. And when enlarging by an **uneven** amount (like 3 → 7), some old pixels become 2 new pixels wide and others 3, which makes lines look uneven.

---

## 35.3 Where do the colours live?

To do better than nearest neighbour, we need a new way to think about a picture.

Think of each pixel's colour as being **exactly at its centre**: pixel (0, 0)'s colour is at (0.5, 0.5), pixel (1, 0)'s at (1.5, 0.5), and so on. Between the centres, we do not know the colour — we have to **guess**. Nearest neighbour guesses "the same as the nearest centre", which makes jumps halfway between centres. A smoother guess is to **blend** between the centres around the position.

```
   pixel centres (●) and a sample position (×) between them:

      ●───────────●         (x0, y0)       (x0+1, y0)
      │     ×     │
      │           │
      ●───────────●         (x0, y0+1)     (x0+1, y0+1)
```

---

## 35.4 Bilinear sampling

📖 **New word: bilinear** — "lerp in two directions": blend the four pixel centres around the position, first across, then down. (Chapter 26, Section 26.9 met the same idea for four corners.)

Here is the recipe for a position p:

1. **Shift by half a pixel**: gx = p.x − 0.5, gy = p.y − 0.5. Now pixel (i, j)'s centre is at exactly (i, j) — whole numbers.
2. **Find the top-left one of the four centres**: x0 = floor(gx), y0 = floor(gy).
3. **How far past it are we?** fx = gx − x0 and fy = gy − y0, each from 0 to just under 1.
4. **Lerp across**, along the top pair and the bottom pair:
   > top = lerp(c(x0, y0), c(x0 + 1, y0), fx)
   > bottom = lerp(c(x0, y0 + 1), c(x0 + 1, y0 + 1), fx)
5. **Lerp down** between them:
   > colour = lerp(top, bottom, fy)

🔢 **Maths: the weights**

> Expand the three lerps, and each corner gets a weight:
> c(x0, y0): (1 − fx)(1 − fy)    c(x0 + 1, y0): fx (1 − fy)
> c(x0, y0 + 1): (1 − fx) fy     c(x0 + 1, y0 + 1): fx fy
> They add up to (1 − fx + fx)(1 − fy + fy) = 1 × 1 = **1** ✓ — a weighted mix again, like Bézier weights (Chapter 34) and barycentric weights (Chapter 26).
> Each weight is the **area** of the rectangle **opposite** that corner, inside the unit square. The closer the position is to a corner, the bigger that corner's opposite rectangle, and the more its colour counts.

🔢 **Maths: sample at (1.2, 0.9)**

> gx = 0.7, gy = 0.4 → x0 = 0, y0 = 0, fx = 0.7, fy = 0.4
> weights: pixel (0, 0): 0.3 × 0.6 = 0.18; pixel (1, 0): 0.7 × 0.6 = 0.42; pixel (0, 1): 0.3 × 0.4 = 0.12; pixel (1, 1): 0.7 × 0.4 = 0.28
> total 0.18 + 0.42 + 0.12 + 0.28 = 1 ✓. Pixel (1, 0) — whose centre (1.5, 0.5) is closest — counts most.

### At the edges: clamp

📖 **New word: clamp to edge** — near the edge of the picture, some of the four centres are **outside** it. Chapter 11's `getPixel` returns **black** outside, which would give every enlarged picture a dark fringe. Instead, we **clamp** the coordinates into the picture (Chapter 14's `std::clamp`): x = −1 becomes 0, x = W becomes W − 1. Outside the picture, we pretend the edge pixels go on for ever.

```cpp
inline Colour getPixelClamped(const Image& image, int x, int y) {
    x = std::clamp(x, 0, image.width() - 1);
    y = std::clamp(y, 0, image.height() - 1);
    return image.getPixel(x, y);
}
```

(Chapter 50 will meet this choice again, together with others, for blurring.)

---

## 35.5 Blend in linear light

Every time we have mixed colours in this book, we have done it in **linear light** (Chapter 17): turn the sRGB bytes into amounts of light, mix, and turn back. Bilinear sampling is mixing, so the same rule applies. Our `sampleBilinear` has a `linearLight` switch, so we can see what happens if we break the rule.

🔢 **Maths: enlarge black, white (2 pixels) to 4**

> new pixel centres 0.5, 1.5, 2.5, 3.5 → × 2/4 → source positions 0.25, 0.75, 1.25, 1.75
> gx = −0.25, 0.25, 0.75, 1.25
> x = 0: x0 = −1, fx = 0.75 — pixels −1 and 0, both black after clamping → **black**
> x = 1: x0 = 0, fx = 0.25 → 25 % of the way from black to white
> x = 2: x0 = 0, fx = 0.75 → 75 % of the way
> x = 3: x0 = 1, fx = 0.25 — pixels 1 and 2, both white after clamping → **white**
> In linear light: 0.25 of white's light → sRGB 0.537 → byte **137**; 0.75 → 0.881 → byte **225**
> Mixing the bytes directly: 0.25 × 255 = **64**, 0.75 × 255 = **191**

The program prints:

```
black, white to 4, nearest: 0 0 255 255
black, white to 4, bilinear (linear light): 0 137 225 255
black, white to 4, bilinear (sRGB bytes): 0 64 191 255
```

The byte version is **too dark** in the middle: byte 64 is only about 5 % of white's light, not 25 % (Chapter 17).

It gets worse with colours. `blend.ppm` enlarges a 2-pixel picture — red, green — to 400 × 40, mixing bytes on the top half and linear light on the bottom half:

```
middle of red to green: linear light (187, 188, 0), sRGB bytes (127, 128, 0)
```

The byte mix (127, 128, 0) is a dark, muddy olive; the linear mix (187, 188, 0) is a bright yellow-ish blend, which is what you see when you shine a red and a green light together. Mixing bytes makes a **dark band** wherever two bright colours meet.

---

## 35.6 Nearest or bilinear?

`zoom.ppm` enlarges an 8 × 8 pixel-art smiley 16 times, both ways:

- **nearest** (left): crisp 16 × 16 blocks — perfect for pixel art.
- **bilinear** (right): soft and blurry; each block melts into its neighbours. Inside every 16 × 16 block, the colour slides smoothly toward the next block's colour.

Neither is "right": nearest keeps hard edges but shows the blocks, bilinear hides the blocks but blurs the edges. For photos, bilinear (or better methods that use more than four pixels) looks much more natural. For pixel art, use nearest.

---

## 35.7 Shrinking: the trouble with skipping

📖 **New word: aliasing** — when fine detail is sampled too sparsely, it does not just disappear: it turns into **wrong** patterns. (We met a cousin of this in Chapter 27: jagged edges.)

When **shrinking**, nearest neighbour and bilinear both look at only one (or four) old pixels for each new pixel. Everything in between is **skipped**.

🔢 **Maths: shrink black, white, black, white (4 pixels) to 2**

> new centres 0.5 and 1.5 → × 4/2 → source positions **1.0** and **3.0**
> nearest: floor(1.0) = 1 and floor(3.0) = 3 → pixels 1 and 3 — both **white**!

```
black, white, black, white to 2, nearest: 255 255
```

Half the picture was black, but the shrunk picture is all white. With a slightly different size, the same stripes could come out all black, or as slow, wide stripes that were never there.

📖 **New word: moiré** — those wavy false patterns. `rings.ppm` is a test picture made for showing them: rings that get thinner and thinner toward the edges (grey = 0.5 + 0.5 cos(r² / 150), where r is the distance from the middle). `small.ppm` shrinks it to a third, three ways:

- **nearest** (left): the thin outer rings turn into **new** sets of rings, centred in the corners — patterns that are not in the original at all.
- **bilinear** (middle): almost as bad. Each new pixel sits over 3 × 3 = 9 old pixels, but bilinear looks at only 4 of them, so most are still skipped.
- **box** (right): the outer rings fade to smooth grey, which is the honest answer — they are too thin to show at this size.

🔢 **Maths: where does the trouble start?**

> The rings' "wiggle speed" grows with r: from one pixel to the next, the cosine's angle changes by about 2r / 150 radians.
> A pattern can only be shown if it changes by at most half a wave per pixel (π radians) — otherwise light–dark–light falls between two pixels and is lost.
> In the shrunk picture, each new pixel is 3 old pixels wide, so the change per new pixel is 3 × 2r / 150 = r / 25. That reaches π at r ≈ **78** old pixels (26 new pixels) from the middle. Outside that circle, nearest and bilinear make moiré.

### The fix: average everything underneath

📖 **New word: box filter** — each new pixel covers a rectangle of the old picture. Instead of picking one point in it, **average all** the old pixels whose centres are inside that rectangle (in linear light, of course). That is exactly what Chapter 27's `shrinkAverage` did for whole-number factors; our `resizeBox` works for any size.

New pixel x covers old x from x × scaleX to (x + 1) × scaleX. Which old pixel centres k + 0.5 are inside? Using the **half-open** rule from Chapter 19 (the left edge in, the right edge out):

> **first pixel = ceil(left − 0.5)**, and stop before ceil(right − 0.5)

(That is `firstCentreAtOrAfter` in the code.) When enlarging, the rectangle can be so small that **no** centre is inside — then we take at least one pixel.

```
black, white, black, white to 2, box: 188 188
```

Each new pixel averages one black and one white: half of white's light, which in sRGB is byte **188** (Chapter 17) — an even grey, the true look of fine stripes seen from far away ✓.

💡 The box filter is not perfect: thin patterns right at the edge of what fits can still leave faint ghosts. Better averaging weights (like the **Gaussian** blur of Chapter 50) reduce them further. But box is simple, fast, and much better than skipping.

---

## 35.8 Smooth turned pictures

Chapter 33's `drawImageTransformed` used nearest neighbour. With `sampleBilinear` we can make a smooth version: the same box, the same inverse matrix, but instead of copying pixel (floor(s.x), floor(s.y)), we sample bilinearly at s.

`turned.ppm` turns the smiley by 30° and enlarges it 10 times, with nearest (left) and bilinear (right). On the left, each pixel of the smiley is a turned square with jagged, stair-step edges. On the right, the colours inside flow smoothly.

⚠️ The **outer** edge of the turned picture is still jagged on the right too: each destination pixel is either inside the source rectangle or not. To smooth that edge as well, we would need coverage (Chapter 27): test several samples per pixel, and blend with the background. That is Practice 7.

---

## Code, part 1: `resize.h`

File: `common/resize.h` (new). It includes `bezier.h`.

```cpp
#ifndef RESIZE_H
#define RESIZE_H

#include <algorithm>
#include <cmath>
#include "bezier.h"

inline Image resizeNearest(const Image& source, int width, int height) {
    Image result(width, height);
    if (source.width() == 0 || source.height() == 0) {
        return result;
    }
    double scaleX = static_cast<double>(source.width()) / width;
    double scaleY = static_cast<double>(source.height()) / height;
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            int sx = static_cast<int>(std::floor((x + 0.5) * scaleX));
            int sy = static_cast<int>(std::floor((y + 0.5) * scaleY));
            result.setPixel(x, y, source.getPixel(sx, sy));
        }
    }
    return result;
}

inline Colour getPixelClamped(const Image& image, int x, int y) {
    x = std::clamp(x, 0, image.width() - 1);
    y = std::clamp(y, 0, image.height() - 1);
    return image.getPixel(x, y);
}

inline ColourF pixelAsF(const Image& image, int x, int y, bool linearLight) {
    Colour c = getPixelClamped(image, x, y);
    return linearLight ? toLinear(c) : toColourF(c);
}

inline Colour sampleBilinear(const Image& image, PointF p, bool linearLight = true) {
    double gx = p.x - 0.5;
    double gy = p.y - 0.5;
    int x0 = static_cast<int>(std::floor(gx));
    int y0 = static_cast<int>(std::floor(gy));
    double fx = gx - x0;
    double fy = gy - y0;
    ColourF c00 = pixelAsF(image, x0, y0, linearLight);
    ColourF c10 = pixelAsF(image, x0 + 1, y0, linearLight);
    ColourF c01 = pixelAsF(image, x0, y0 + 1, linearLight);
    ColourF c11 = pixelAsF(image, x0 + 1, y0 + 1, linearLight);
    ColourF top = c00 * (1.0 - fx) + c10 * fx;
    ColourF bottom = c01 * (1.0 - fx) + c11 * fx;
    ColourF mixed = top * (1.0 - fy) + bottom * fy;
    return linearLight ? fromLinear(mixed) : toColour(mixed);
}

inline Image resizeBilinear(const Image& source, int width, int height, bool linearLight = true) {
    Image result(width, height);
    if (source.width() == 0 || source.height() == 0) {
        return result;
    }
    double scaleX = static_cast<double>(source.width()) / width;
    double scaleY = static_cast<double>(source.height()) / height;
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            PointF p{(x + 0.5) * scaleX, (y + 0.5) * scaleY};
            result.setPixel(x, y, sampleBilinear(source, p, linearLight));
        }
    }
    return result;
}

inline int firstCentreAtOrAfter(double edge) {
    return static_cast<int>(std::ceil(edge - 0.5));
}

inline Image resizeBox(const Image& source, int width, int height) {
    Image result(width, height);
    if (source.width() == 0 || source.height() == 0) {
        return result;
    }
    double scaleX = static_cast<double>(source.width()) / width;
    double scaleY = static_cast<double>(source.height()) / height;
    for (int y = 0; y < height; ++y) {
        int sy0 = firstCentreAtOrAfter(y * scaleY);
        int sy1 = std::max(firstCentreAtOrAfter((y + 1) * scaleY), sy0 + 1);
        for (int x = 0; x < width; ++x) {
            int sx0 = firstCentreAtOrAfter(x * scaleX);
            int sx1 = std::max(firstCentreAtOrAfter((x + 1) * scaleX), sx0 + 1);
            ColourF sum{0.0, 0.0, 0.0};
            for (int sy = sy0; sy < sy1; ++sy) {
                for (int sx = sx0; sx < sx1; ++sx) {
                    sum = sum + toLinear(getPixelClamped(source, sx, sy));
                }
            }
            int count = (sx1 - sx0) * (sy1 - sy0);
            result.setPixel(x, y, fromLinear(sum / count));
        }
    }
    return result;
}

inline void drawImageTransformedSmooth(Image& dest, const Image& source, const Mat3& t) {
    Mat3 back;
    if (!inverse(t, back)) {
        return;
    }
    Rect box = clipToImage(transformedBox(t, source.width(), source.height()), dest);
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            PointF s = applyToPoint(back, PointF{x + 0.5, y + 0.5});
            if (s.x >= 0.0 && s.x < source.width() && s.y >= 0.0 && s.y < source.height()) {
                dest.setPixel(x, y, sampleBilinear(source, s));
            }
        }
    }
}

#endif
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef RESIZE_H` / `#define RESIZE_H` | Include guard. |
| 4–6 | `#include <algorithm>` / `<cmath>` / `"bezier.h"` | `std::clamp` and `std::max`; `std::floor` and `std::ceil`; and the whole library so far (including `toLinear` and `fromLinear` from Chapter 17, and Chapter 33's `inverse` and `transformedBox`). |
| 8 | `inline Image resizeNearest(const Image& source, int width, int height) {` | A new picture of the given size, by nearest neighbour (Section 35.2). |
| 9–12 | `Image result(width, height); if (source.width() == 0 \|\| source.height() == 0) { return result; }` | An empty source has nothing to copy: return a black picture. |
| 13–14 | `double scaleX = static_cast<double>(source.width()) / width;` / `double scaleY = ...` | Old size / new size (Section 35.1). The `static_cast` avoids integer division. |
| 15–16 | `for (int y = 0; y < height; ++y) { for (int x = 0; x < width; ++x) {` | Every **new** pixel (inverse mapping). |
| 17–18 | `int sx = static_cast<int>(std::floor((x + 0.5) * scaleX));` / `int sy = ...` | The old pixel this new pixel's centre falls in. |
| 19–23 | `result.setPixel(x, y, source.getPixel(sx, sy));` … `return result; }` | Copy its colour. |
| 25–29 | `inline Colour getPixelClamped(const Image& image, int x, int y) { x = std::clamp(x, 0, image.width() - 1); y = ...; return image.getPixel(x, y); }` | Outside the picture, use the nearest edge pixel (Section 35.4). |
| 31–34 | `inline ColourF pixelAsF(const Image& image, int x, int y, bool linearLight) { Colour c = getPixelClamped(image, x, y); return linearLight ? toLinear(c) : toColourF(c); }` | Read a pixel as a `ColourF`: in linear light (Chapter 17) or as plain bytes / 255 (Chapter 14). |
| 36 | `inline Colour sampleBilinear(const Image& image, PointF p, bool linearLight = true) {` | The colour at any position p (Section 35.4). Linear light unless asked otherwise. |
| 37–38 | `double gx = p.x - 0.5;` / `double gy = p.y - 0.5;` | Step 1: shift so pixel centres are at whole numbers. |
| 39–40 | `int x0 = static_cast<int>(std::floor(gx));` / `int y0 = ...` | Step 2: the top-left of the four centres. |
| 41–42 | `double fx = gx - x0;` / `double fy = gy - y0;` | Step 3: how far past it, from 0 to under 1. |
| 43–46 | `ColourF c00 = pixelAsF(image, x0, y0, linearLight);` … `ColourF c11 = ...` | The four colours. The names say which: c10 is "one across, zero down". |
| 47–48 | `ColourF top = c00 * (1.0 - fx) + c10 * fx;` / `ColourF bottom = c01 * (1.0 - fx) + c11 * fx;` | Step 4: lerp across, top and bottom. |
| 49 | `ColourF mixed = top * (1.0 - fy) + bottom * fy;` | Step 5: lerp down. |
| 50–51 | `return linearLight ? fromLinear(mixed) : toColour(mixed);` `}` | Back to bytes the same way we came. |
| 53–67 | `inline Image resizeBilinear(const Image& source, int width, int height, bool linearLight = true) { ... PointF p{(x + 0.5) * scaleX, (y + 0.5) * scaleY}; result.setPixel(x, y, sampleBilinear(source, p, linearLight)); ... }` | The same as `resizeNearest`, but each new pixel is **sampled** at its source position instead of copied from one pixel. |
| 69–71 | `inline int firstCentreAtOrAfter(double edge) { return static_cast<int>(std::ceil(edge - 0.5)); }` | The first pixel k whose centre k + 0.5 is at or after `edge` (Section 35.7). |
| 73 | `inline Image resizeBox(const Image& source, int width, int height) {` | Shrink (or enlarge) by averaging (Section 35.7). |
| 74–79 | the empty check and the two scales | As before. |
| 80–82 | `for (int y = 0; ...) { int sy0 = firstCentreAtOrAfter(y * scaleY); int sy1 = std::max(firstCentreAtOrAfter((y + 1) * scaleY), sy0 + 1);` | The rows of old pixels under this new row: from the top edge y × scaleY up to (not including) the bottom edge. At least one row. These only depend on y, so we work them out once per row. |
| 83–85 | `for (int x = 0; ...) { int sx0 = ...; int sx1 = std::max(..., sx0 + 1);` | The same across. |
| 86–91 | `ColourF sum{0.0, 0.0, 0.0}; for (int sy = sy0; sy < sy1; ++sy) { for (int sx = sx0; sx < sx1; ++sx) { sum = sum + toLinear(getPixelClamped(source, sx, sy)); } }` | Add up the light of all those pixels. (`getPixelClamped` protects us if rounding ever reaches one pixel past the edge.) |
| 92–93 | `int count = (sx1 - sx0) * (sy1 - sy0); result.setPixel(x, y, fromLinear(sum / count));` | The average, back to sRGB bytes. |
| 94–97 | `}` `}` `return result;` `}` | Done. |
| 99 | `inline void drawImageTransformedSmooth(Image& dest, const Image& source, const Mat3& t) {` | Chapter 33's `drawImageTransformed`, with bilinear sampling (Section 35.8). |
| 100–104 | `Mat3 back; if (!inverse(t, back)) { return; } Rect box = clipToImage(transformedBox(...), dest);` | Exactly as in Chapter 33. |
| 105–107 | the two loops and `PointF s = applyToPoint(back, PointF{x + 0.5, y + 0.5});` | Where each destination pixel centre came from. |
| 108–110 | `if (s.x >= 0.0 && s.x < source.width() && s.y >= 0.0 && s.y < source.height()) { dest.setPixel(x, y, sampleBilinear(source, s)); }` | Inside the source rectangle? Then sample there. (This is the same "inside" test as Chapter 33's, written with the position instead of the pixel numbers.) |
| 111–113 | `}` `}` `}` | End of the loops and the function. |
| 115 | `#endif` | End of the include guard. |

---

## Code, part 2: zooms, blends, rings and a turned smiley

File: `ch35/resize.cpp`

```cpp
#include <cmath>
#include <iostream>
#include <string>
#include "resize.h"

void paste(Image& dest, const Image& source, int ox, int oy) {
    for (int y = 0; y < source.height(); ++y) {
        for (int x = 0; x < source.width(); ++x) {
            dest.setPixel(ox + x, oy + y, source.getPixel(x, y));
        }
    }
}

Image makeSprite() {
    const std::string rows[8] = {"  ####  ", " #yyyy# ", "#y#yy#y#", "#yyyyyy#",
                                 "#y#yy#y#", "#yy##yy#", " #yyyy# ", "  ####  "};
    Image sprite(8, 8);
    for (int y = 0; y < 8; ++y) {
        for (int x = 0; x < 8; ++x) {
            char ch = rows[y][x];
            Colour c{120, 180, 240};
            if (ch == '#') {
                c = Colour{40, 40, 60};
            } else if (ch == 'y') {
                c = Colour{250, 210, 60};
            }
            sprite.setPixel(x, y, c);
        }
    }
    return sprite;
}

void printRow(const char* label, const Image& image) {
    std::cout << label;
    for (int x = 0; x < image.width(); ++x) {
        std::cout << " " << static_cast<int>(image.getPixel(x, 0).r);
    }
    std::cout << "\n";
}

int main() {
    std::cout << "3 to 7 pixels, source pixel for each new pixel:";
    for (int x = 0; x < 7; ++x) {
        std::cout << " " << static_cast<int>(std::floor((x + 0.5) * 3.0 / 7.0));
    }
    std::cout << "\nwithout the + 0.5:";
    for (int x = 0; x < 7; ++x) {
        std::cout << " " << static_cast<int>(std::floor(x * 3.0 / 7.0));
    }
    std::cout << "\n";

    Image strip(2, 1);
    strip.setPixel(0, 0, colours::black);
    strip.setPixel(1, 0, colours::white);
    printRow("black, white to 4, nearest:", resizeNearest(strip, 4, 1));
    printRow("black, white to 4, bilinear (linear light):", resizeBilinear(strip, 4, 1));
    printRow("black, white to 4, bilinear (sRGB bytes):", resizeBilinear(strip, 4, 1, false));

    Image stripes(4, 1);
    for (int x = 0; x < 4; ++x) {
        stripes.setPixel(x, 0, (x % 2 == 0) ? colours::black : colours::white);
    }
    printRow("black, white, black, white to 2, nearest:", resizeNearest(stripes, 2, 1));
    printRow("black, white, black, white to 2, box:", resizeBox(stripes, 2, 1));

    Image redGreen(2, 1);
    redGreen.setPixel(0, 0, colours::red);
    redGreen.setPixel(1, 0, colours::green);
    Image blendLinear = resizeBilinear(redGreen, 400, 40);
    Image blendBytes = resizeBilinear(redGreen, 400, 40, false);
    Colour m1 = blendLinear.getPixel(200, 0);
    Colour m2 = blendBytes.getPixel(200, 0);
    std::cout << "middle of red to green: linear light (" << static_cast<int>(m1.r) << ", "
              << static_cast<int>(m1.g) << ", " << static_cast<int>(m1.b) << "), sRGB bytes ("
              << static_cast<int>(m2.r) << ", " << static_cast<int>(m2.g) << ", "
              << static_cast<int>(m2.b) << ")\n";

    Image sprite = makeSprite();
    Image zoom(266, 128, colours::white);
    paste(zoom, resizeNearest(sprite, 128, 128), 0, 0);
    paste(zoom, resizeBilinear(sprite, 128, 128), 138, 0);

    Image blend(400, 80);
    paste(blend, blendBytes, 0, 0);
    paste(blend, blendLinear, 0, 40);

    Image rings(300, 300);
    for (int y = 0; y < 300; ++y) {
        for (int x = 0; x < 300; ++x) {
            double dx = x + 0.5 - 150.0;
            double dy = y + 0.5 - 150.0;
            double v = 0.5 + 0.5 * std::cos((dx * dx + dy * dy) / 150.0);
            std::uint8_t g = toByte(v);
            rings.setPixel(x, y, Colour{g, g, g});
        }
    }
    Image small(320, 100, colours::white);
    paste(small, resizeNearest(rings, 100, 100), 0, 0);
    paste(small, resizeBilinear(rings, 100, 100), 110, 0);
    paste(small, resizeBox(rings, 100, 100), 220, 0);

    Image turned(400, 200, colours::white);
    Mat3 place = rotation(degreesToRadians(30.0)) * scaling(10.0, 10.0) * translation(-4.0, -4.0);
    drawImageTransformed(turned, sprite, translation(100.0, 100.0) * place);
    drawImageTransformedSmooth(turned, sprite, translation(300.0, 100.0) * place);

    bool ok = zoom.savePPM("zoom.ppm");
    ok = ok && blend.savePPM("blend.ppm");
    ok = ok && rings.savePPM("rings.ppm");
    ok = ok && small.savePPM("small.ppm");
    ok = ok && turned.savePPM("turned.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
```

Build and run (from the `code/ch35` folder):

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common resize.cpp -o resize
./resize
```

### Line by line

**Helpers (lines 1–39)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–4 | the `#include` lines | `std::floor` and `std::cos`; printing; `std::string`; the new header. |
| 6–12 | `void paste(Image& dest, const Image& source, int ox, int oy) { ... dest.setPixel(ox + x, oy + y, source.getPixel(x, y)); ... }` | Copy a whole picture into another, with its top-left corner at (ox, oy). Used to put several results side by side. |
| 14–16 | `Image makeSprite() { const std::string rows[8] = {...};` | An 8 × 8 smiley as eight strings: `#` is dark outline, `y` is yellow face, a space is sky blue. Drawing pixel art as text is easy to read and to change. |
| 17–29 | `Image sprite(8, 8); for (...) { for (...) { char ch = rows[y][x]; Colour c{120, 180, 240}; if (ch == '#') { ... } else if (ch == 'y') { ... } sprite.setPixel(x, y, c); } }` | Turn each character into a colour. Sky blue is the default. |
| 30–31 | `return sprite;` `}` | Done. |
| 33–39 | `void printRow(const char* label, const Image& image) { ... static_cast<int>(image.getPixel(x, 0).r) ... }` | Print the red value of every pixel in the top row. (For greys, red = green = blue. The `static_cast<int>` prints a number instead of a character, Chapter 4.) |

**The numbers (lines 41–76)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 42–50 | two loops printing `std::floor((x + 0.5) * 3.0 / 7.0)` and `std::floor(x * 3.0 / 7.0)` | The 3 → 7 table of Section 35.1, with and without + 0.5. |
| 52–54 | `Image strip(2, 1); strip.setPixel(0, 0, colours::black); strip.setPixel(1, 0, colours::white);` | A tiny 2-pixel picture. |
| 55–57 | three `printRow` calls | Enlarged to 4: nearest, bilinear in linear light, bilinear with bytes (Section 35.5). |
| 59–62 | `Image stripes(4, 1); for (...) { stripes.setPixel(x, 0, (x % 2 == 0) ? colours::black : colours::white); }` | Black, white, black, white. |
| 63–64 | two `printRow` calls | Shrunk to 2: nearest (all white!) and box (even grey) (Section 35.7). |
| 66–70 | `Image redGreen(2, 1); ...; Image blendLinear = resizeBilinear(redGreen, 400, 40); Image blendBytes = resizeBilinear(redGreen, 400, 40, false);` | Red and green, stretched to 400 × 40 both ways. |
| 71–76 | `Colour m1 = blendLinear.getPixel(200, 0);` … printing | The colour halfway along each. |

**The pictures (lines 78–105)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 78 | `Image sprite = makeSprite();` | The smiley. |
| 79–81 | `Image zoom(266, 128, colours::white); paste(zoom, resizeNearest(sprite, 128, 128), 0, 0); paste(zoom, resizeBilinear(sprite, 128, 128), 138, 0);` | 16 times bigger, nearest on the left, bilinear on the right, with a 10-pixel white gap (Section 35.6). |
| 83–85 | `Image blend(400, 80); paste(blend, blendBytes, 0, 0); paste(blend, blendLinear, 0, 40);` | The byte blend on top, the linear blend below. |
| 87–96 | `Image rings(300, 300); for (...) { for (...) { double dx = ...; double dy = ...; double v = 0.5 + 0.5 * std::cos((dx * dx + dy * dy) / 150.0); std::uint8_t g = toByte(v); rings.setPixel(x, y, Colour{g, g, g}); } }` | The ring test picture (Section 35.7). r² = dx² + dy², so the cosine's angle grows faster and faster outward. `toByte` (Chapter 14) turns 0…1 into a byte. |
| 97–100 | `Image small(320, 100, colours::white);` and three `paste` calls | The rings shrunk to 100 × 100: nearest, bilinear and box, side by side. |
| 102–103 | `Image turned(400, 200, colours::white); Mat3 place = rotation(degreesToRadians(30.0)) * scaling(10.0, 10.0) * translation(-4.0, -4.0);` | Right to left: move the smiley's middle (4, 4) to the origin, enlarge 10 times, turn 30°. |
| 104–105 | `drawImageTransformed(turned, sprite, translation(100.0, 100.0) * place);` / `drawImageTransformedSmooth(turned, sprite, translation(300.0, 100.0) * place);` | Then move it to (100, 100) — nearest — or (300, 100) — bilinear (Section 35.8). |

**Saving (lines 107–117)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 107–111 | `bool ok = zoom.savePPM("zoom.ppm");` … | Save the five pictures. |
| 112–117 | `if (!ok) { ... }` `return 0;` `}` | Report a problem, or finish. |

### What you should see

```
3 to 7 pixels, source pixel for each new pixel: 0 0 1 1 1 2 2
without the + 0.5: 0 0 0 1 1 2 2
black, white to 4, nearest: 0 0 255 255
black, white to 4, bilinear (linear light): 0 137 225 255
black, white to 4, bilinear (sRGB bytes): 0 64 191 255
black, white, black, white to 2, nearest: 255 255
black, white, black, white to 2, box: 188 188
middle of red to green: linear light (187, 188, 0), sRGB bytes (127, 128, 0)
```

Open the pictures:
- `zoom.ppm`: a blocky smiley on the left, a soft, blurry one on the right.
- `blend.ppm`: red fading into green twice; the top band has a dark muddy middle, the bottom one stays bright.
- `rings.ppm`: the test picture — rings getting thinner toward the edges.
- `small.ppm`: the rings shrunk three ways; the left two show false ring patterns in the corners, the right one fades smoothly to grey.
- `turned.ppm`: the smiley turned and enlarged, blocky on the left, smooth on the right.

---

## Small examples

### Example 1 — Where does a new pixel come from?

Shrink 640 pixels wide to 200: scaleX = 3.2. New pixel 10: (10.5) × 3.2 = **33.6** → nearest: old pixel **33**.

### Example 2 — Bilinear by hand

A 2 × 2 grey picture: top row 0 and 100, bottom row 100 and 200 (pretend these are already amounts of light). Sample at the very middle, (1, 1):

> gx = gy = 0.5 → x0 = y0 = 0, fx = fy = 0.5
> top = 50, bottom = 150, colour = **100** — the average of all four, as it should be at the middle.

### Example 3 — Clamping at the corner

Sample the same picture at (0.2, 0.2): gx = gy = −0.3 → x0 = y0 = −1, fx = fy = 0.7. Pixels (−1, −1), (0, −1) and (−1, 0) are all clamped to pixel (0, 0). So all four "neighbours" are really pixel (0, 0) (with weights 0.09 + 0.21 + 0.21 + 0.49 = 1) → exactly pixel (0, 0)'s colour ✓. Near the edge, the colour stays flat.

### Example 4 — How many pixels does the box average?

Shrink 9 → 2: scaleX = 4.5. New pixel 0 covers 0 to 4.5: first = ceil(−0.5) = 0, stop = ceil(4.0) = 4 → old pixels 0, 1, 2, 3. New pixel 1 covers 4.5 to 9: first = ceil(4.0) = 4, stop = ceil(8.5) = 9 → pixels 4 … 8. The middle pixel 4 (centre 4.5, exactly on the boundary) goes to the **right** — the half-open rule — so every old pixel is used exactly once.

### Example 5 — Shrinking then enlarging

Shrink a photo to a quarter and enlarge it back: the detail is gone for good. Resizing can never **add** detail: bilinear can only guess smoothly between the pixels it has.

---

## Common mistakes

⚠️ **Forgetting the + 0.5.** It shifts the whole picture by half a pixel (Section 35.1).

⚠️ **Forgetting the − 0.5 in bilinear.** Then the four centres are chosen wrongly, and the result is shifted the other way.

⚠️ **Reading outside the picture.** Clamp to the edge, or the borders go dark.

⚠️ **Blending sRGB bytes.** Dark bands between bright colours. Blend in linear light.

⚠️ **Shrinking with nearest or bilinear.** Fine detail turns into false patterns. Use the box filter (or blur first, Chapter 50).

⚠️ **Integer division in the scale.** `source.width() / width` with `int`s is 0 when enlarging. Use `static_cast<double>`.

⚠️ **Using bilinear for pixel art.** It blurs the crisp pixels that the artist placed one by one. Use nearest.

---

## Practice

🏋️ **1.** Enlarging 4 pixels to 10: which old pixel does each new pixel use (nearest)? How many new pixels does each old pixel get?

🏋️ **2.** Compute the bilinear weights for the sample position (2.9, 1.6).

🏋️ **3.** Enlarge the smiley to 100 × 60 (a different scale across and down) with both methods. What happens to its shape?

🏋️ **4.** Write `Image resizeKeepShape(const Image& source, int maxWidth, int maxHeight)` that makes the picture as big as possible inside the given box **without** stretching it.

🏋️ **5.** Shrink `rings.ppm` to 100 × 100 with `resizeBox`, and then enlarge the result back to 300 × 300 with `resizeBilinear`. Compare with the original. Where is the difference biggest?

🏋️ **6.** Make a "mosaic" effect: shrink a picture to 1/10 with `resizeBox`, then enlarge it back with `resizeNearest`.

🏋️ **7.** Make the outer edge of `drawImageTransformedSmooth` smooth: for each destination pixel, test 4 × 4 sample positions (Chapter 27's `sampleOffset`), count how many fall inside the source rectangle, and blend the sampled colour with `paintCoverage`.

🏋️ **8.** Why does enlarging by **exactly 2** with bilinear never use the colours of pixels exactly — each new pixel is a 25 % / 75 % mix? (Hint: work out fx for new pixels 0, 1, 2, 3.)

---

## Answers

**1.**
> scaleX = 0.4: (x + 0.5) × 0.4 = 0.2, 0.6, 1.0, 1.4, 1.8, 2.2, 2.6, 3.0, 3.4, 3.8
> floor: **0, 0, 1, 1, 1, 2, 2, 3, 3, 3** → the old pixels get 2, 3, 2 and 3 new pixels — not quite even, because 10 / 4 = 2.5 is not a whole number.

**2.**
> gx = 2.4, gy = 1.1 → x0 = 2, y0 = 1, fx = 0.4, fy = 0.1
> (2, 1): 0.6 × 0.9 = **0.54**; (3, 1): 0.4 × 0.9 = **0.36**; (2, 2): 0.6 × 0.1 = **0.06**; (3, 2): 0.4 × 0.1 = **0.04** (total 1 ✓)

**3.**
> `resizeNearest(sprite, 100, 60)` and `resizeBilinear(sprite, 100, 60)`: the smiley is stretched wide and squashed (scale 12.5 across, 7.5 down). With nearest, the blocks are uneven — some columns 12 pixels wide, some 13; some rows 7, some 8.

**4.**

```cpp
Image resizeKeepShape(const Image& source, int maxWidth, int maxHeight) {
    double sx = static_cast<double>(maxWidth) / source.width();
    double sy = static_cast<double>(maxHeight) / source.height();
    double s = std::min(sx, sy);
    int w = std::max(1, static_cast<int>(source.width() * s));
    int h = std::max(1, static_cast<int>(source.height() * s));
    return (s < 1.0) ? resizeBox(source, w, h) : resizeBilinear(source, w, h);
}
```

> Use the **smaller** of the two scales, so both sides fit. Shrink with the box filter, enlarge with bilinear.

**5.**
> In the middle (thick rings) the result looks almost like the original. Near the edges the original has thin rings, but the round trip gives smooth grey: the detail was averaged away when shrinking, and enlarging cannot bring it back (Example 5).

**6.**

```cpp
Image mosaic = resizeNearest(resizeBox(photo, photo.width() / 10, photo.height() / 10),
                             photo.width(), photo.height());
```

> Each 10 × 10 block becomes one flat square of its average colour — the "pixelated" look used to hide faces on TV.

**7.**

```cpp
int inside = 0;
for (int j = 0; j < 4; ++j) {
    for (int i = 0; i < 4; ++i) {
        PointF q = applyToPoint(back, PointF{x + sampleOffset(i, 4), y + sampleOffset(j, 4)});
        if (q.x >= 0.0 && q.x < source.width() && q.y >= 0.0 && q.y < source.height()) {
            ++inside;
        }
    }
}
PointF s = applyToPoint(back, PointF{x + 0.5, y + 0.5});
paintCoverage(dest, x, y, sampleBilinear(source, s), inside / 16.0);
```

> (Inside the loops over the box. Pixels whose centre is just outside the source still get a colour — `sampleBilinear` clamps to the edge — and partial coverage.)

**8.**
> scaleX = 0.5: source positions 0.25, 0.75, 1.25, 1.75, … → gx = −0.25, 0.25, 0.75, 1.25 → fx = 0.75, 0.25, 0.75, 0.25, … Every new pixel centre lies a quarter of the way between two old centres, never on one. So every new pixel is a 25/75 mix (or 75/25) — except at the edges, where clamping makes both neighbours the same pixel.

---

## Summary

🧠 Resizing is **inverse mapping** with a scale: **source = (x + 0.5) × old / new**. Never forget the + 0.5.

🧠 **Nearest neighbour**: floor of the source position. Sharp, blocky — right for pixel art.

🧠 **Bilinear**: subtract 0.5, take the four centres around the position, lerp across, then down. Weights (1 − fx)(1 − fy), fx(1 − fy), (1 − fx)fy, fx·fy add up to 1.

🧠 **Clamp to the edge** instead of reading black outside the picture.

🧠 Blend in **linear light**: mixing sRGB bytes makes dark bands.

🧠 **Shrinking** by skipping pixels causes **aliasing** and **moiré**. **Average** everything underneath (box filter) instead.

🧠 The same bilinear sampler makes Chapter 33's turned pictures smooth.

---

## Next chapter

That is the end of Part 5. We can now move, turn, bend and resize shapes and pictures. But all our pictures are still saved as PPM files, which many programs cannot open. **Part 6** is about real file formats. Chapter 36 begins with the simplest one that every computer understands: **BMP**. We will take a BMP file apart byte by byte: its two headers, its **little-endian** numbers (Chapter 4), its **upside-down** rows, its **BGR** colour order, and the strange **padding** at the end of each row.
