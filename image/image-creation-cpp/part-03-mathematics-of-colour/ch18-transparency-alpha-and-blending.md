# Chapter 18 — Transparency: Alpha and Blending

> **Part 3 · Chapter 18 of 82**
> **You need:** Chapters 1–17 · **You will make:** `alpha.h` (see-through colours and the "over" operation), `glass.ppm` (three coloured glass discs over a checkerboard) and `fade.ppm` (a fade-in, done two ways)

---

## What you will learn

- What **transparency** means for a pixel, and the **alpha** channel that stores it.
- How to paint a see-through colour **over** a picture: **src × α + dst × (1 − α)**.
- Why the **order** of layers matters.
- The full **"over"** formula, for when **both** layers are see-through.
- What **premultiplied alpha** is, and why it makes the maths simpler and more correct.
- Why blending should happen in **linear light** (Chapter 17).
- How editors **show** transparency with a checkerboard, and which file formats can **store** it.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **transparent** | You can see through it completely. |
| **opaque** | You cannot see through it at all. |
| **translucent** | Partly see-through, like coloured glass or tracing paper. |
| **alpha (α)** | A fourth number for a pixel: how opaque it is, from 0 (invisible) to 1 (solid). |
| **RGBA** | A colour with four channels: red, green, blue and alpha. |
| **coverage** | How much of a pixel's area a shape covers. Alpha can mean coverage. |
| **source (src)** | The new colour we are painting. |
| **destination (dst)** | The colour that is already there, under the new one. |
| **compositing** | Putting several image layers together into one picture. |
| **straight alpha** | Storing the colour and the alpha separately. |
| **premultiplied alpha** | Storing the colour already **multiplied** by its alpha. |
| **layer** | One picture in a stack of pictures that are put together. |

---

## 18.1 What is transparency?

Look through a window: you see the world behind it. That glass is **transparent**.

Look at a wall: you see only the wall. It is **opaque**.

Look through red glass, or a thin curtain: you see the world behind, but **mixed** with the glass's own colour. It is **translucent** — partly see-through.

📖 **New word: transparent** — completely see-through.

📖 **New word: opaque** — not see-through at all.

📖 **New word: translucent** — partly see-through.

On a screen, every pixel is just a colour (Chapter 5). There is no real glass. To make something **look** see-through, we compute the colour you **would see** through it: a mix of the glass colour and the colour behind it.

---

## 18.2 The alpha channel

📖 **New word: alpha (α)** — a fourth number for a pixel: how **opaque** it is.

| α | Meaning |
|---|---|
| 0 | fully transparent (invisible — you see only what is behind) |
| 0.25 | mostly see-through |
| 0.5 | half see-through |
| 1 | fully opaque (solid — you see only this colour) |

α is the Greek letter **alpha**. In bytes, α is stored like any other channel: 0 to 255 (0 = transparent, 255 = opaque).

📖 **New word: RGBA** — a colour with four channels: (R, G, B, A). In bytes, one RGBA pixel is **4 bytes**.

📖 **New word: coverage** — how much of a pixel's area a shape covers.

There are two ways to think about α, and both lead to the same maths:

1. **Glass**: the pixel is covered by a material that lets (1 − α) of the light behind it through.
2. **Coverage**: a fraction α of the pixel is covered by a solid shape, and (1 − α) is not.

The second view is very important in Chapters 27 and 28 (smooth edges). There, a pixel on the edge of a circle may be **40% covered** by the circle. We will paint it with α = 0.4.

---

## 18.3 Painting a see-through colour over a picture

📖 **New word: source (src)** — the new colour we paint.

📖 **New word: destination (dst)** — the colour already there.

Take the most common case: the picture underneath is **opaque** (like our `Image` — every pixel is solid). We paint a colour **src** with alpha **α** on top.

The light we see is:
- **α** of the source's light (the glass's own colour), **plus**
- **(1 − α)** of the destination's light (what shines through).

> **result = src × α + dst × (1 − α)**

🔢 **Maths: 50% red over solid blue** (in linear light — Section 18.7)

> src = red = (1, 0, 0), α = 0.5
> dst = blue = (0, 0, 1)
> result = (1, 0, 0) × 0.5 + (0, 0, 1) × (1 − 0.5)
> = (0.5, 0, 0) + (0, 0, 0.5)
> = **(0.5, 0, 0.5)** in linear light → encode (Chapter 17) → **(188, 0, 188)**, a purple

Look closely at the formula. It is our old friend **lerp** (Chapter 13):

> lerp(dst, src, α) = dst + (src − dst) × α = dst × (1 − α) + src × α ✓

So "paint with alpha α" is exactly "lerp from what is there to the new colour, by α". When α = 0, the result is dst (nothing painted). When α = 1, the result is src (solid paint).

🧠 **Remember:** Over an opaque picture: **result = src × α + dst × (1 − α)** — a lerp from dst to src by α.

---

## 18.4 The order of layers matters

📖 **New word: layer** — one picture in a stack of pictures.

📖 **New word: compositing** — putting several layers together into one picture.

Painting is **not** the same in both orders.

🔢 **Maths: 80% red over solid blue, and 80% blue over solid red**

> red over blue: (1, 0, 0) × 0.8 + (0, 0, 1) × 0.2 = **(0.8, 0, 0.2)** → mostly red → bytes **(231, 0, 124)**
> blue over red: (0, 0, 1) × 0.8 + (1, 0, 0) × 0.2 = **(0.2, 0, 0.8)** → mostly blue → bytes **(124, 0, 231)**

The colour on **top** wins more. This matches real life: red glass on a blue table looks reddish; blue glass on a red table looks bluish.

So when we put layers together, we must go from the **back** to the **front**:

```
   step 1: start with the background (opaque)
   step 2: paint layer 1 over it
   step 3: paint layer 2 over the result
   …
```

This back-to-front order is called the **painter's algorithm**, because a painter paints the sky first, then the mountains, then the trees in front. We meet it again in 3D (Chapter 67).

---

## 18.5 When both layers are see-through

So far the destination was solid. But sometimes the destination is see-through too — for example, when we put two translucent layers together **before** placing them on a background. Then the result is also see-through, and we need its alpha too.

Think in terms of **how much light gets through**:

- The source blocks a fraction **α_s** of what is behind it.
- The destination blocks **α_d** of what is behind **it**.
- Of the light that passes the source, (1 − α_s), the destination then blocks α_d.

🔢 **Maths: the total alpha**

> α_out = α_s + α_d × (1 − α_s)

> 50% over 50%: α_out = 0.5 + 0.5 × 0.5 = 0.5 + 0.25 = **0.75**

Two half-see-through sheets together let only **25%** of the light through (0.5 × 0.5), so they are **75% opaque**. ✓

🔢 **Maths: the colour**

The colour is the **weighted average** of the two colours, weighted by how much each one is **seen**:

- the source is seen by α_s,
- the destination is seen by α_d × (1 − α_s).

> colour_out = (src × α_s + dst × α_d × (1 − α_s)) ÷ α_out

We divide by α_out because the weights add up to α_out, not to 1 (Chapter 15: a weighted average divides by the total weight).

🔢 **Maths: 50% red over 50% blue**

> α_out = 0.75 (above)
> weight of red = 0.5
> weight of blue = 0.5 × (1 − 0.5) = 0.25
> R = (1 × 0.5 + 0 × 0.25) ÷ 0.75 = 0.5 ÷ 0.75 = **0.667**
> G = 0
> B = (0 × 0.5 + 1 × 0.25) ÷ 0.75 = 0.25 ÷ 0.75 = **0.333**
> result = **(0.667, 0, 0.333)** with **α = 0.75**

Two-thirds red and one-third blue, because red is on top. This is the famous **"over"** operation, published by Thomas Porter and Tom Duff in 1984. It is used in nearly every graphics program.

⚠️ **Careful:** If α_out = 0 (both layers fully transparent), we would divide by zero. The result is simply "nothing": (0, 0, 0) with α = 0.

### A check: an opaque destination

If α_d = 1:

> α_out = α_s + 1 × (1 − α_s) = 1
> colour_out = (src × α_s + dst × (1 − α_s)) ÷ 1

That is exactly Section 18.3 ✓. The simple formula is a special case of the full one.

---

## 18.6 Premultiplied alpha

📖 **New word: straight alpha** — storing the colour and the alpha **separately**, as we did above: (R, G, B, α).

📖 **New word: premultiplied alpha** — storing the colour **already multiplied by its alpha**: (R × α, G × α, B × α, α).

🔢 **Maths: 50% red, both ways**

> straight: (1, 0, 0, 0.5)
> premultiplied: (1 × 0.5, 0 × 0.5, 0 × 0.5, 0.5) = **(0.5, 0, 0, 0.5)**

What does premultiplied (0.5, 0, 0) mean? It is the **light this pixel adds** — half of full red. That is a very natural quantity.

### "Over" becomes very simple

With premultiplied colours (written with a ′ mark), "over" is the **same formula for all four channels**, with **no division**:

> **out′ = src′ + dst′ × (1 − α_s)** (for R′, G′, B′ and α alike)

🔢 **Maths: 50% red over 50% blue, premultiplied**

> src′ = (0.5, 0, 0, 0.5), dst′ = (0, 0, 0.5, 0.5)
> 1 − α_s = 0.5
> R′ = 0.5 + 0 × 0.5 = **0.5**
> G′ = 0 + 0 × 0.5 = **0**
> B′ = 0 + 0.5 × 0.5 = **0.25**
> α = 0.5 + 0.5 × 0.5 = **0.75**
> out′ = **(0.5, 0, 0.25, 0.75)**

To get back the straight colour, divide by α:

> (0.5 ÷ 0.75, 0, 0.25 ÷ 0.75) = **(0.667, 0, 0.333)** with α = 0.75 ✓ — the same as Section 18.5

### Why premultiplied alpha is better

| Reason | Explanation |
|---|---|
| simpler | One formula, the same for all channels. No special case. |
| no division | Faster, and no danger of dividing by zero during compositing. |
| invisible pixels are clean | A fully transparent pixel is always (0, 0, 0, 0). In straight alpha, an invisible pixel can still carry a colour, like (1, 0, 0, 0) — "invisible red" — and that hidden colour can leak out. |
| correct averaging | When we **blur** or **shrink** an image with transparency (Chapters 35, 50), we average neighbouring pixels. With straight alpha, an invisible black pixel next to a white one pulls the average toward **black**, and edges get dark "fringes". With premultiplied alpha, the invisible pixel adds (0, 0, 0, 0) — no light and no weight — so there is no fringe. |

🔢 **Maths: averaging a solid white pixel with an invisible pixel**

> straight: white (1, 1, 1, 1) and invisible black (0, 0, 0, 0)
> average: (0.5, 0.5, 0.5, 0.5) → a **half-transparent grey** — a dark fringe!

> premultiplied: (1, 1, 1, 1) and (0, 0, 0, 0)
> average: (0.5, 0.5, 0.5, 0.5) → un-premultiply: (0.5 ÷ 0.5, …) = (1, 1, 1) with α = 0.5 → **half-transparent white** ✓

The numbers looked the same, but they **mean** different things. In premultiplied form, (0.5, 0.5, 0.5, 0.5) is "half-covered by white". That is correct.

🧠 **Remember:** **Premultiplied**: store (R·α, G·α, B·α, α). Then **out = src + dst × (1 − α_src)**, the same for every channel.

---

## 18.7 Blend in linear light

Blending is **mixing light** — so, as Chapter 17 taught, it should happen in **linear light**.

🔢 **Maths: 50% white over black**

> in bytes: lerp(0, 255, 0.5) = 127.5 → **128** (only 22% of the light — too dark)
> in linear light: 1 × 0.5 + 0 × 0.5 = 0.5 → encode → **188** (half the light — correct)

Our `blendOver` function decodes both colours, blends, and encodes the result. Our `fade.ppm` shows both methods: a red that fades in over a grey checkerboard. In the byte version (top), the half-faded area looks too dark and muddy. In the linear version (bottom), it looks like real red glass getting gradually thicker.

⚠️ **Careful:** Many programs (and many web browsers) blend in byte space, for speed and for historical reasons. So you will often see the "too dark" version. Both are common; linear is the physically correct one.

---

## 18.8 Showing and storing transparency

### Showing it: the checkerboard

A screen cannot show "nothing". So paint programs show transparent areas as a **grey-and-white checkerboard**. Wherever you see the checkerboard through a picture, that part of the picture is see-through. Our `glass.ppm` uses the same idea: three coloured glass discs over a checkerboard, so you can see the pattern through them.

### Storing it: file formats

| Format | Can store alpha? |
|---|---|
| PPM, PGM, PBM (Chapters 8–10) | **no** — only colour or grey |
| PAM ("P7", another Netpbm format) | yes, but few viewers open it |
| BMP (Chapter 36) | sometimes (32-bit BMP), but support is poor |
| TGA (Chapter 39) | yes |
| **PNG** (Chapters 40–43) | **yes** — the most common way to store transparency |

Our `Image` class stores only RGB, so in this chapter we always blend **onto** an opaque image. When we write PNG in Part 6, we will be able to save real transparent images.

---

## Code, part 1: `alpha.h`

File: `common/alpha.h` (new). It includes `srgb.h`, so blending happens in linear light.

```cpp
#ifndef ALPHA_H
#define ALPHA_H

#include <algorithm>
#include "srgb.h"

struct ColourFA {
    double r = 0.0;
    double g = 0.0;
    double b = 0.0;
    double a = 0.0;
};

inline ColourFA withAlpha(ColourF c, double a) {
    return ColourFA{c.r, c.g, c.b, a};
}

inline ColourFA overStraight(ColourFA src, ColourFA dst) {
    double outA = src.a + dst.a * (1.0 - src.a);
    if (outA <= 0.0) {
        return ColourFA{};
    }
    double k = dst.a * (1.0 - src.a);
    return ColourFA{(src.r * src.a + dst.r * k) / outA,
                    (src.g * src.a + dst.g * k) / outA,
                    (src.b * src.a + dst.b * k) / outA,
                    outA};
}

inline ColourFA premultiply(ColourFA c) {
    return ColourFA{c.r * c.a, c.g * c.a, c.b * c.a, c.a};
}

inline ColourFA unpremultiply(ColourFA c) {
    if (c.a <= 0.0) {
        return ColourFA{};
    }
    return ColourFA{c.r / c.a, c.g / c.a, c.b / c.a, c.a};
}

inline ColourFA overPremultiplied(ColourFA src, ColourFA dst) {
    double k = 1.0 - src.a;
    return ColourFA{src.r + dst.r * k, src.g + dst.g * k, src.b + dst.b * k, src.a + dst.a * k};
}

inline Colour blendOver(Colour dst, Colour src, double alpha) {
    alpha = std::clamp(alpha, 0.0, 1.0);
    ColourF ld = toLinear(dst);
    ColourF ls = toLinear(src);
    return fromLinear(ls * alpha + ld * (1.0 - alpha));
}

inline void blendPixel(Image& image, int x, int y, Colour src, double alpha) {
    if (!image.isInside(x, y)) {
        return;
    }
    image.setPixel(x, y, blendOver(image.getPixel(x, y), src, alpha));
}

#endif
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef ALPHA_H` / `#define ALPHA_H` | Include guard. |
| 4 | `#include <algorithm>` | `std::clamp`. |
| 5 | `#include "srgb.h"` | `toLinear` and `fromLinear` (Chapter 17), and through it `colourf.h` and `image.h`. |
| 7–12 | `struct ColourFA { double r = 0.0; ... double a = 0.0; };` | A maths colour **with alpha**: four `double`s. The default is (0, 0, 0, 0): fully transparent. We use **linear** values for r, g, b. |
| 14 | `inline ColourFA withAlpha(ColourF c, double a) {` | A small helper: add an alpha to a `ColourF`. |
| 15–16 | `return ColourFA{c.r, c.g, c.b, a};` `}` | Copy the three channels and add `a`. |
| 18 | `inline ColourFA overStraight(ColourFA src, ColourFA dst) {` | The full "over" for **straight** alpha (Section 18.5): `src` on top of `dst`. |
| 19 | `double outA = src.a + dst.a * (1.0 - src.a);` | The total alpha. |
| 20–22 | `if (outA <= 0.0) { return ColourFA{}; }` | Both fully transparent: the result is "nothing". This also stops a divide by zero. |
| 23 | `double k = dst.a * (1.0 - src.a);` | How much the destination is **seen** through the source. |
| 24–27 | `return ColourFA{(src.r * src.a + dst.r * k) / outA, ..., outA};` | Each colour channel: the weighted average of src (weight α_s) and dst (weight k), divided by the total weight. The alpha is `outA`. |
| 28 | `}` | End. |
| 30 | `inline ColourFA premultiply(ColourFA c) {` | Straight → premultiplied (Section 18.6). |
| 31–32 | `return ColourFA{c.r * c.a, c.g * c.a, c.b * c.a, c.a};` `}` | Multiply each colour channel by alpha. Alpha stays the same. |
| 34 | `inline ColourFA unpremultiply(ColourFA c) {` | Premultiplied → straight. |
| 35–37 | `if (c.a <= 0.0) { return ColourFA{}; }` | An invisible pixel has no colour to recover. Avoid dividing by zero. |
| 38–39 | `return ColourFA{c.r / c.a, c.g / c.a, c.b / c.a, c.a};` `}` | Divide each colour channel by alpha. |
| 41 | `inline ColourFA overPremultiplied(ColourFA src, ColourFA dst) {` | "Over" for **premultiplied** alpha. |
| 42 | `double k = 1.0 - src.a;` | How much of the destination shows through the source. |
| 43–44 | `return ColourFA{src.r + dst.r * k, src.g + dst.g * k, src.b + dst.b * k, src.a + dst.a * k};` `}` | The same simple formula for all four channels. No division. |
| 46 | `inline Colour blendOver(Colour dst, Colour src, double alpha) {` | The everyday case (Section 18.3): paint `src` with `alpha` over an **opaque** `dst`. Byte colours in, byte colour out. |
| 47 | `alpha = std::clamp(alpha, 0.0, 1.0);` | Alpha must be from 0 to 1. |
| 48–49 | `ColourF ld = toLinear(dst);` / `ColourF ls = toLinear(src);` | Decode both colours to linear light (Chapter 17). |
| 50 | `return fromLinear(ls * alpha + ld * (1.0 - alpha));` | src × α + dst × (1 − α), then encode back to bytes. |
| 51 | `}` | End. |
| 53 | `inline void blendPixel(Image& image, int x, int y, Colour src, double alpha) {` | Paint one see-through pixel **into an image**. |
| 54–56 | `if (!image.isInside(x, y)) { return; }` | Outside the image: do nothing. (Otherwise `getPixel` would return black, and `setPixel` would ignore the result anyway — but this is clearer and faster.) |
| 57 | `image.setPixel(x, y, blendOver(image.getPixel(x, y), src, alpha));` | Read what is there (dst), blend the new colour over it, and write the result back. |
| 58 | `}` | End. |
| 60 | `#endif` | End of the include guard. |

---

## Code, part 2: glass discs and a fade

File: `ch18/alpha.cpp`

```cpp
#include <cmath>
#include <iostream>
#include <string>
#include "alpha.h"

double roundTo(double v, double factor) {
    return std::floor(v * factor + 0.5) / factor;
}

void printColour(const std::string& label, Colour c) {
    std::cout << label << " = (" << static_cast<int>(c.r) << ", "
              << static_cast<int>(c.g) << ", " << static_cast<int>(c.b) << ")\n";
}

void printFA(const std::string& label, ColourFA c) {
    std::cout << label << " = (" << roundTo(c.r, 1000) << ", " << roundTo(c.g, 1000) << ", "
              << roundTo(c.b, 1000) << ", alpha " << roundTo(c.a, 1000) << ")\n";
}

bool insideCircle(int x, int y, double cx, double cy, double radius) {
    double dx = (x + 0.5) - cx;
    double dy = (y + 0.5) - cy;
    return dx * dx + dy * dy <= radius * radius;
}

Colour checker(int x, int y) {
    bool light = ((x / 20) + (y / 20)) % 2 == 0;
    return light ? Colour{230, 230, 230} : Colour{150, 150, 150};
}

int main() {
    const ColourF red = toLinear(colours::red);
    const ColourF blue = toLinear(colours::blue);

    ColourFA a = overStraight(withAlpha(red, 0.5), withAlpha(blue, 1.0));
    printColour("50% red over solid blue  ", fromLinear(ColourF{a.r, a.g, a.b}));
    printFA("50% red over 50% blue    ", overStraight(withAlpha(red, 0.5), withAlpha(blue, 0.5)));
    ColourFA p = overPremultiplied(premultiply(withAlpha(red, 0.5)),
                                   premultiply(withAlpha(blue, 0.5)));
    printFA("same, premultiplied      ", p);
    printFA("premultiplied, undone    ", unpremultiply(p));

    printColour("80% red over solid blue  ", blendOver(colours::blue, colours::red, 0.8));
    printColour("80% blue over solid red  ", blendOver(colours::red, colours::blue, 0.8));
    printColour("50% white over black, bytes ", lerpColour(colours::black, colours::white, 0.5));
    printColour("50% white over black, linear", blendOver(colours::black, colours::white, 0.5));

    Image glass(300, 200);
    for (int y = 0; y < glass.height(); ++y) {
        for (int x = 0; x < glass.width(); ++x) {
            glass.setPixel(x, y, checker(x, y));
        }
    }
    const double cxs[3] = {120.0, 180.0, 150.0};
    const double cys[3] = {80.0, 80.0, 130.0};
    const Colour inks[3] = {colours::red, colours::green, colours::blue};
    for (int i = 0; i < 3; ++i) {
        for (int y = 0; y < glass.height(); ++y) {
            for (int x = 0; x < glass.width(); ++x) {
                if (insideCircle(x, y, cxs[i], cys[i], 55.0)) {
                    blendPixel(glass, x, y, inks[i], 0.6);
                }
            }
        }
    }

    Image fade(300, 80);
    for (int y = 0; y < fade.height(); ++y) {
        for (int x = 0; x < fade.width(); ++x) {
            double alpha = static_cast<double>(x) / (fade.width() - 1);
            Colour back = checker(x, y);
            Colour c = (y < 40) ? lerpColour(back, colours::red, alpha)
                                : blendOver(back, colours::red, alpha);
            fade.setPixel(x, y, c);
        }
    }

    bool ok = glass.savePPM("glass.ppm");
    ok = ok && fade.savePPM("fade.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
```

### Line by line

**Helpers (lines 1–29)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–3 | `#include <cmath>` / `<iostream>` / `<string>` | `std::floor`, printing, labels. |
| 4 | `#include "alpha.h"` | Our new header (and everything it includes). |
| 6–8 | `double roundTo(...) { ... }` | Round to some decimal places (Chapter 16). |
| 10–13 | `void printColour(...) { ... }` | Print a byte colour. |
| 15–18 | `void printFA(const std::string& label, ColourFA c) { ... }` | Print a colour with alpha, as four numbers rounded to 3 places. |
| 20–24 | `bool insideCircle(...) { ... }` | Is a pixel's centre inside a circle? (Chapter 14.) |
| 26 | `Colour checker(int x, int y) {` | The colour of the "transparency" checkerboard at (x, y) (Section 18.8). |
| 27 | `bool light = ((x / 20) + (y / 20)) % 2 == 0;` | Squares of 20 × 20 pixels, alternating (Chapter 11, Example 1). |
| 28 | `return light ? Colour{230, 230, 230} : Colour{150, 150, 150};` | Light grey or darker grey. |
| 29 | `}` | End. |

**The worked examples (lines 31–46)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 31 | `int main() {` | The program starts here. |
| 32–33 | `const ColourF red = toLinear(colours::red);` / `... blue ...` | Red and blue in linear light. |
| 35 | `ColourFA a = overStraight(withAlpha(red, 0.5), withAlpha(blue, 1.0));` | 50% red over **solid** blue, using the full formula. |
| 36 | `printColour("50% red over solid blue  ", fromLinear(ColourF{a.r, a.g, a.b}));` | Encode its colour into bytes and print it. Expect (188, 0, 188) (Section 18.3). |
| 37 | `printFA("50% red over 50% blue    ", overStraight(withAlpha(red, 0.5), withAlpha(blue, 0.5)));` | Both see-through (Section 18.5). Expect (0.667, 0, 0.333) with α 0.75. |
| 38–39 | `ColourFA p = overPremultiplied(premultiply(withAlpha(red, 0.5)), premultiply(withAlpha(blue, 0.5)));` | The same, with premultiplied alpha (Section 18.6). |
| 40 | `printFA("same, premultiplied      ", p);` | Expect (0.5, 0, 0.25) with α 0.75. |
| 41 | `printFA("premultiplied, undone    ", unpremultiply(p));` | Back to straight: it must equal line 37's result. |
| 43–44 | `printColour("80% red over solid blue  ", blendOver(colours::blue, colours::red, 0.8));` and the reverse | The order matters (Section 18.4). Note `blendOver` takes the **destination first**. |
| 45 | `printColour("50% white over black, bytes ", lerpColour(colours::black, colours::white, 0.5));` | A byte-space blend (Chapter 13's lerp): expect 128. |
| 46 | `printColour("50% white over black, linear", blendOver(colours::black, colours::white, 0.5));` | A linear-light blend: expect 188 (Section 18.7). |

**Glass discs (lines 48–65)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 48 | `Image glass(300, 200);` | The picture. |
| 49–53 | `for (...) { for (...) { glass.setPixel(x, y, checker(x, y)); } }` | Fill it with the checkerboard: our opaque background. |
| 54–55 | `const double cxs[3] = {120.0, 180.0, 150.0};` / `const double cys[3] = {80.0, 80.0, 130.0};` | The centres of three discs, in a triangle. |
| 56 | `const Colour inks[3] = {colours::red, colours::green, colours::blue};` | Their colours. |
| 57 | `for (int i = 0; i < 3; ++i) {` | Paint the discs **one after another** — back to front (Section 18.4). |
| 58–59 | `for (int y ...) { for (int x ...) {` | Every pixel. |
| 60 | `if (insideCircle(x, y, cxs[i], cys[i], 55.0)) {` | Is this pixel inside disc `i`? |
| 61 | `blendPixel(glass, x, y, inks[i], 0.6);` | Paint the disc's colour with α = 0.6 over whatever is there already — the checkerboard, or an earlier disc. |
| 62–65 | `}` `}` `}` `}` | End of the `if` and the loops. |

**The fade (lines 67–76)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 67 | `Image fade(300, 80);` | Two bands of 40 rows. |
| 68–69 | `for (int y ...) { for (int x ...) {` | Every pixel. |
| 70 | `double alpha = static_cast<double>(x) / (fade.width() - 1);` | Alpha goes from 0 (left) to 1 (right) — like Chapter 13's t. |
| 71 | `Colour back = checker(x, y);` | The background colour here. |
| 72–73 | `Colour c = (y < 40) ? lerpColour(back, colours::red, alpha) : blendOver(back, colours::red, alpha);` | Top band: blend in **bytes**. Bottom band: blend in **linear light**. |
| 74 | `fade.setPixel(x, y, c);` | Store it. |
| 75–76 | `}` `}` | End of the loops. |

**Save (lines 78–85)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 78–83 | `bool ok = glass.savePPM(...); ... if (!ok) { ...; return 1; }` | Save both images. |
| 84 | `return 0;` | The program finished with no problem. |
| 85 | `}` | End of `main`. |

Compile:

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common alpha.cpp -o alpha
```

### What you should see

```
50% red over solid blue   = (188, 0, 188)
50% red over 50% blue     = (0.667, 0, 0.333, alpha 0.75)
same, premultiplied       = (0.5, 0, 0.25, alpha 0.75)
premultiplied, undone     = (0.667, 0, 0.333, alpha 0.75)
80% red over solid blue   = (231, 0, 124)
80% blue over solid red   = (124, 0, 231)
50% white over black, bytes  = (128, 128, 128)
50% white over black, linear = (188, 188, 188)
```

🔢 **Maths: check "80% red over solid blue"**

> linear result: (0.8, 0, 0.2) (Section 18.4)
> encode 0.8: 1.055 × 0.8^(1/2.4) − 0.055 = 1.055 × 0.9112 − 0.055 = 0.9063 → × 255 = 231.1 → **231**
> encode 0.2: 1.055 × 0.2^(1/2.4) − 0.055 = 1.055 × 0.5114 − 0.055 = 0.4845 → × 255 = 123.6 → **124**

Open the images:
- `glass.ppm`: three discs of coloured glass. You can **see the checkerboard through them**. Where two discs overlap, the colours **mix** — but the disc painted **later** is stronger in the mix. Compare with Chapter 14's `lights.ppm`, where lights **added** up to white. Glass does not add up: each new disc **replaces** 60% of what is behind it with its own colour, so overlaps become mixtures, never white.
- `fade.ppm`: red fading in from the left. In the top band (bytes), the middle looks darker and dirtier. In the bottom band (linear), the red comes in smoothly, like real glass getting thicker.

---

## Small examples

### Example 1 — A see-through rectangle

```cpp
for (int y = 40; y < 100; ++y) {
    for (int x = 50; x < 250; ++x) {
        blendPixel(img, x, y, colours::black, 0.5);
    }
}
```

A half-transparent black box: a "shadow" or a dark panel behind text, like the subtitles in videos. Everything under it gets darker, but stays visible.

> white under it: linear 1 × 0.5 + 0 × 0.5 = 0.5 → **188**
> mid grey 188 (linear 0.5) under it: 0.5 × 0.5 = 0.25 → **137**

### Example 2 — Painting the same colour twice

Painting 50% red **twice** over white:

> after the first: 0.5 red + 0.5 white → linear (1, 0.5, 0.5)
> after the second: 0.5 red + 0.5 × (1, 0.5, 0.5) → (1, 0.25, 0.25)

The total effect is like **one** coat with α = 0.75 (because 1 − 0.5 × 0.5 = 0.75):

> 0.75 red + 0.25 white → (1, 0.25, 0.25) ✓

This is the α_out rule from Section 18.5. Each coat lets half of the "white" through, so two coats let a quarter through.

### Example 3 — A fade to black for an animation

Fading a whole picture to black over 10 frames:

```cpp
for (int frame = 0; frame <= 10; ++frame) {
    double alpha = frame / 10.0;
    // for every pixel: blendPixel(img, x, y, colours::black, alpha) on a copy
}
```

> frame 0: α = 0 → the picture as it is
> frame 5: α = 0.5 → half the light
> frame 10: α = 1 → black

We make real animations in Chapter 80.

### Example 4 — Why straight alpha needs the division

Try the colour formula from Section 18.5 **without** dividing by α_out:

> 50% red over 50% blue: R = 1 × 0.5 = 0.5, B = 1 × 0.25 = 0.25, α = 0.75

Interpreted as a straight colour, (0.5, 0, 0.25) is a **dark** purple. But both layers were full-strength red and blue! It is too dark because we forgot to divide by the total weight. Interpreted as a **premultiplied** colour, (0.5, 0, 0.25, 0.75) is exactly right (Section 18.6). The two systems give the same numbers in a different meaning — mixing them up is a classic bug.

---

## Common mistakes

⚠️ **Painting layers in the wrong order.** The top layer must be painted **last**.

⚠️ **Swapping src and dst.** `blendOver(dst, src, alpha)` — the destination comes first in our function. Swapping them changes the result (Section 18.4).

⚠️ **Mixing straight and premultiplied colours.** Using a premultiplied colour in a straight formula (or the opposite) makes colours too dark or too bright. Know which one you have.

⚠️ **Dividing by zero when un-premultiplying.** A pixel with α = 0 has no colour. Return (0, 0, 0, 0).

⚠️ **Blending bytes.** Half-transparent white over black gives 128 instead of 188. Blend in linear light.

⚠️ **Expecting PPM to keep transparency.** PPM has no alpha channel. Save PNG (Part 6) for transparent images.

---

## Practice

🏋️ **1.** Paint 25% green (0, 1, 0) over solid white (1, 1, 1), in linear light. What is the linear result? What are the bytes?

🏋️ **2.** What is α_out when you put a 30% layer over a 60% layer? How much light gets through both?

🏋️ **3.** Premultiply (0.8, 0.4, 0.2) with α = 0.5. Then un-premultiply the result. Do you get the original back?

🏋️ **4.** Compute 50% blue over 50% red with the straight formula, and compare with "50% red over 50% blue" from Section 18.5.

🏋️ **5.** In Example 2, what single alpha equals **three** coats of 50%?

🏋️ **6.** Change `glass.ppm` so that the **blue** disc is painted first and the **red** disc last. Which overlaps change colour?

🏋️ **7.** Write a function `blendImage(Image& dst, const Image& src, double alpha)` that blends a whole image over another of the same size.

---

## Answers

**1.**
> result = (0, 1, 0) × 0.25 + (1, 1, 1) × 0.75 = (0, 0.25, 0) + (0.75, 0.75, 0.75) = **(0.75, 1.0, 0.75)** (linear)
> encode 0.75: 1.055 × 0.75^(1/2.4) − 0.055 = 1.055 × 0.8870 − 0.055 = 0.8808 → × 255 = 224.6 → **225**
> bytes = **(225, 255, 225)**, a very pale green

**2.**
> α_out = 0.3 + 0.6 × (1 − 0.3) = 0.3 + 0.42 = **0.72**
> light through = 1 − 0.72 = **0.28** (check: 0.7 × 0.4 = 0.28 ✓)

**3.**
> premultiplied: (0.8 × 0.5, 0.4 × 0.5, 0.2 × 0.5, 0.5) = **(0.4, 0.2, 0.1, 0.5)**
> un-premultiplied: (0.4 ÷ 0.5, 0.2 ÷ 0.5, 0.1 ÷ 0.5) = **(0.8, 0.4, 0.2)** ✓ yes

(With bytes, the trip is not always exact: dividing small rounded numbers loses precision. That is one reason why we do this maths with `double`s.)

**4.**
> α_out = 0.75 (the same)
> weight of blue (top) = 0.5, weight of red (below) = 0.25
> R = 0.25 ÷ 0.75 = 0.333, B = 0.5 ÷ 0.75 = 0.667
> **(0.333, 0, 0.667)** with α 0.75 — now blue is stronger, because it is on top.

**5.**
> light through one coat = 0.5
> through three coats = 0.5 × 0.5 × 0.5 = 0.125
> α = 1 − 0.125 = **0.875**

**6.** Change the arrays so the loop paints blue first: for example `inks[3] = {colours::blue, colours::green, colours::red}` with the matching centres reordered. Every overlap where red is involved now looks **redder**, because red is on top. The red–green overlap leans to red instead of green, and the red–blue overlap leans to red instead of blue.

**7.**

```cpp
void blendImage(Image& dst, const Image& src, double alpha) {
    for (int y = 0; y < dst.height(); ++y) {
        for (int x = 0; x < dst.width(); ++x) {
            blendPixel(dst, x, y, src.getPixel(x, y), alpha);
        }
    }
}
```

If `src` is smaller, `getPixel` returns black outside it (Chapter 11), so the edge would be blended with black. A full version would only loop over the area both images share.

---

## Summary

🧠 **Alpha** (0–1) says how opaque a pixel is. RGBA = 4 channels.

🧠 Over an opaque picture: **result = src × α + dst × (1 − α)** — a lerp from dst to src.

🧠 The **order** matters: paint layers **back to front**. The top one wins more.

🧠 Both see-through: **α_out = α_s + α_d (1 − α_s)**, and the colour is the weighted average ÷ α_out.

🧠 **Premultiplied**: store colour × α. Then **out = src + dst × (1 − α_s)** for every channel — simpler, and correct when averaging.

🧠 Blend in **linear light**. 50% white over black = 188, not 128.

🧠 PPM cannot store alpha. **PNG** can (Part 6).

---

## Next chapter

**Part 3 is complete!** We know how colour works: interpolation, vectors, grey, HSV, gamma and transparency. In **Part 4** we start **drawing shapes**. Chapter 19 begins with the simplest ones: single pixels and **rectangles**, filled and outlined, with careful rules for where exactly their edges go.
