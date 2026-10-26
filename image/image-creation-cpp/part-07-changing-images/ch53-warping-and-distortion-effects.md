# Chapter 53 — Warping and Distortion Effects

> **Part 7 · Chapter 53 of 82**
> **You need:** Chapters 1–52 (especially 29, 30, 31, 33 and 35) · **You will make:** `warp.h` (wave, ripple, swirl, bulge and pinch, all worked backwards with bilinear sampling, and a forwards version to show its holes), and `warp.png`: a scene and a grid, bent five ways

---

## What you will learn

- What **warping** is: moving pixels to new places, each by a different amount.
- Why we work **backwards** again: for each new pixel, where did it come **from**?
- Four classic effects as small formulas: **wave**, **ripple**, **swirl**, **bulge** and **pinch**.
- How **polar coordinates** (distance and angle from a centre) make round effects easy.
- What to do when a new pixel comes from **outside** the old picture.
- How many **holes** the forwards way leaves.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **warp** | Bend a picture by moving its pixels, each by its own amount. |
| **source point** | The place in the old picture that a new pixel reads its colour from. |
| **wavelength** | The distance after which a wave repeats. |
| **polar coordinates** | Describing a point by its distance r and angle θ from a centre, instead of x and y. |
| **ripple** | Rings that push points in and out, like a stone dropped in water. |
| **swirl** | A twist: points turn around a centre, more near the centre than far away. |
| **bulge / pinch** | Making the middle look bigger (like a magnifying glass) or smaller. |

---

## 53.1 Moving pixels

So far in Part 7, we changed pixels **where they were**:

- point operations (Chapters 47–48) changed each value on its own;
- convolution (Chapters 49–51) mixed each pixel with its neighbours;
- dithering (Chapter 52) chose new colours.

Now we **move** them.

📖 **New word: warp** — make a new picture in which each pixel's colour comes from some **other** place in the old picture. Think of the picture printed on a rubber sheet that you stretch, twist and push.

Chapter 33 already moved whole pictures through a **matrix**: turning, scaling, moving. A matrix treats every point the same way — straight lines stay straight. A warp can move every point differently. It is any rule of the form:

> **new(x, y) = old(source(x, y))**

where `source` is a function that takes a point and gives back a point — and it can be anything we like.

---

## 53.2 Backwards, again

Chapter 33 (Section 33.5) showed that going **forwards** — taking each old pixel and putting it somewhere new — leaves **holes** (and paints some pixels twice). The cure was to go **backwards**: for each **new** pixel, ask where it came from. Every new pixel asks exactly once, so there are no holes.

Warps work the same way. That is why our functions are all called `...Source`: they answer the question "**this** new point — **which** old point does it show?"

📖 **New word: source point** — the answer to that question.

🔢 **The recipe for one new pixel (x, y):**

> 1. Take its centre: p = (x + 0.5, y + 0.5) (Chapter 22's pixel centres).
> 2. Ask the warp: from = source(p).
> 3. If `from` is inside the old picture: read the colour there with Chapter 35's `sampleBilinear` (`from` is almost never exactly on a pixel centre, so we mix the 4 nearest pixels, in linear light).
> 4. If it is outside: use a chosen colour (we use black).

💡 Writing the warp backwards is often **easier** than forwards too. We never need to "undo" a formula; we just write the backwards formula directly.

The simplest warp moves nothing:

```
none:   the new point (105.00, 55.00) reads from (105.00, 55.00)
```

---

## 53.3 The wave

Slide each **row** sideways, by an amount that goes up and down like a wave:

> **source x = x + A × sin(2π × y / L)**, source y = y

- **A** (the `amount`) is how far the rows slide, at most: A pixels left or right.
- **L** (the `size`) is the **wavelength**.

📖 **New word: wavelength** — the distance after which the wave repeats. sin goes through one full wave while its angle goes from 0 to 2π (Chapter 30), and 2π × y / L does that while y goes from 0 to L.

🔢 **Maths: A = 6, L = 40**

> row y = 10: 2π × 10 / 40 = π/2, and sin(π/2) = **1** → source x = 50 + 6 = **56**
> row y = 30: 2π × 30 / 40 = 3π/2, and sin(3π/2) = **−1** → source x = 50 − 6 = **44**
> row y = 20: 2π × 20 / 40 = π, and sin(π) = 0 → no slide

```
wave:   the new point (50.00, 10.00) reads from (56.00, 10.00)
        the new point (50.00, 30.00) reads from (44.00, 30.00)
```

⚠️ **Which way does the picture move?** The new point at x = 50 shows what **was** at x = 56. So the picture has moved 6 pixels to the **left** in row 10. Backwards formulas always feel "the wrong way round" at first — just like Chapter 49's shift kernel, where a weight on the left neighbour moved the picture right.

Straight vertical lines become wavy, horizontal lines stay straight. Near the left and right sides, some rows read from x < 0 or x ≥ 160 — outside the picture — and get black: thin black slivers along the sides.

---

## 53.4 Polar coordinates

The other four effects are **round**: they happen around a centre point c. For round effects there is a better way to describe a point.

📖 **New word: polar coordinates** — instead of "x across, y down", say "**r** away from the centre, in the direction **θ**":

> d = p − c (the step from the centre to the point, a vector — Chapter 29)
> r = length(d) = √(dx² + dy²)
> θ = atan2(dy, dx) (Chapter 30)

Round effects change **only r** (push points inwards or outwards) or **only θ** (turn them around the centre).

🔢 **Maths: changing only r**

> To move a point to a new distance r′ in the same direction, scale its step: c + d × (r′ / r).
> (d / r has length 1 and points the same way; times r′ makes the length r′.)

⚠️ When r = 0 (the point is the centre itself), r′ / r divides by 0. The centre must be handled on its own — it simply stays where it is.

🔢 **Maths: changing only θ**

> To turn a point by an angle a around c: c + rotate(d, a) — Chapter 31's `rotate`.

All our round effects use the centre (80, 55) — the middle of the 160 × 110 test pictures.

---

## 53.5 The ripple

📖 **New word: ripple** — rings around the centre, like the waves when a stone drops into a pond:

> **r′ = r + A × sin(2π × r / L)**

It is the wave of Section 53.3, but going **outwards** from the centre instead of down the picture: points at some distances read from further out, at others from further in.

🔢 **Maths: A = 3, L = 20, the point (85, 55)**

> d = (85 − 80, 55 − 55) = (5, 0), so r = **5**
> 2π × 5 / 20 = π/2 → sin = 1 → r′ = 5 + 3 = **8**
> source = (80, 55) + (5, 0) × 8 / 5 = (80, 55) + (8, 0) = **(88, 55)**

```
ripple: the new point (85.00, 55.00) reads from (88.00, 55.00)
```

On the grid picture, the squares bend into rings of ripples. The ripple has no outer limit, so far from the centre, near the corners, some points read from outside the picture and turn black.

---

## 53.6 The swirl

📖 **New word: swirl** — turn every point around the centre, by an angle that is biggest at the centre and fades to 0 at the radius R:

> **angle = amount × (1 − r / R)**, for r < R (outside R, nothing changes)

At r = 0 the angle is the full `amount`; at r = R it is 0. So the swirl joins the unchanged picture smoothly at its edge — no seam.

🔢 **Maths: amount = π/2 (90°), R = 50, the point (105, 55)**

> d = (25, 0), r = **25** → angle = π/2 × (1 − 25/50) = π/2 × 0.5 = **π/4** (45°)
> rotate((25, 0), 45°) = (25 × cos 45°, 25 × sin 45°) = (25 × 0.7071, 25 × 0.7071) = **(17.68, 17.68)**
> source = (80 + 17.68, 55 + 17.68) = **(97.68, 72.68)**

```
swirl:  the new point (105.00, 55.00) reads from (97.68, 72.68)
        the new point (80.00, 55.00) reads from (80.00, 55.00)
```

The centre itself turns too — but turning a point around itself does not move it.

⚠️ **Which way does it turn?** In pictures, y goes down, so a positive angle turns **clockwise** on the screen (Chapter 31, Section 31.7). The new point at 0° reads from 45° clockwise. So what you **see** has turned the other way: **anticlockwise** by 45°.

---

## 53.7 Bulge and pinch

📖 **New words: bulge / pinch** — make the area around the centre look **bigger** (as through a magnifying glass or a "fish-eye" lens) or **smaller**, inside a radius R:

> **r′ = R × (r / R)^k**, for r < R

- r / R goes from 0 (centre) to 1 (edge). Raising it to the power k keeps 0 at 0 and 1 at 1, so the edge does not move: no seam.
- **k > 1**: (r / R)^k is **smaller** than r / R, so points read from **nearer** the centre: the middle is stretched out — a **bulge**.
- **k < 1**: points read from **further out**: the middle is squeezed — a **pinch**.
- k = 1: nothing changes.

In the code, the scale for the step d is r′ / r = (r / R)^k × R / r = **(r / R)^(k − 1)**.

🔢 **Maths: R = 50, the point (105, 55), r = 25, r / R = 0.5**

> bulge, k = 2: 0.5^(2 − 1) = **0.5** → source = (80, 55) + (25, 0) × 0.5 = **(92.5, 55)**
> pinch, k = 0.5: 0.5^(0.5 − 1) = 0.5^(−0.5) = 1 / √0.5 = **1.4142** → (80, 55) + (35.36, 0) = **(115.36, 55)**

```
bulge:  the new point (105.00, 55.00) reads from (92.50, 55.00)
pinch:  the new point (105.00, 55.00) reads from (115.36, 55.00)
```

With the bulge, what was 12.5 pixels from the centre now shows 25 pixels from it — **twice** as far: magnified. Very close to the centre, the magnification grows even more (with k = 2, r′ = r² / R, so a point 1 pixel out reads from only 0.02 pixels out): a tiny spot in the middle is blown up into a soft blob.

---

## 53.8 Forwards leaves holes — counted

To see why we go backwards, `warpForward` does it the wrong way: it uses the same formula as if it said where each **old** pixel **goes**, and paints the old pixel's colour there. Pixels that nobody paints stay red:

```
swirl done forwards: 1472 of 17600 pixels never painted
```

That is **8.4 %** of the picture: a sprinkle of red holes along curved lines in the swirled area (and some pixels painted twice, which you cannot see). The backwards `warpImage` has none, by construction.

(Because it uses the formula in the other direction, the forwards picture swirls the **opposite** way. That does not matter for counting holes.)

---

## Code, part 1: `warp.h`

File: `common/warp.h` (new). It includes `dither.h` (and through it everything from Chapters 1–52: `PointF`, `rotate`, `sampleBilinear`, `kPi`).

```cpp
#ifndef WARP_H
#define WARP_H

#include <cmath>
#include <vector>
#include "dither.h"

enum class WarpKind { None, Wave, Ripple, Swirl, Bulge };

struct Warp {
    WarpKind kind = WarpKind::None;
    PointF centre{0.0, 0.0};
    double amount = 0.0;
    double size = 1.0;
};

inline PointF waveSource(PointF p, const Warp& w) {
    return PointF{p.x + w.amount * std::sin(2.0 * kPi * p.y / w.size), p.y};
}

inline PointF rippleSource(PointF p, const Warp& w) {
    const Vec2 d = p - w.centre;
    const double r = length(d);
    if (r == 0.0) {
        return p;
    }
    const double push = w.amount * std::sin(2.0 * kPi * r / w.size);
    return w.centre + d * ((r + push) / r);
}

inline PointF swirlSource(PointF p, const Warp& w) {
    const Vec2 d = p - w.centre;
    const double r = length(d);
    if (r >= w.size) {
        return p;
    }
    const double angle = w.amount * (1.0 - r / w.size);
    return w.centre + rotate(d, angle);
}

inline PointF bulgeSource(PointF p, const Warp& w) {
    const Vec2 d = p - w.centre;
    const double r = length(d);
    if (r == 0.0 || r >= w.size) {
        return p;
    }
    return w.centre + d * std::pow(r / w.size, w.amount - 1.0);
}

inline PointF warpSource(PointF p, const Warp& w) {
    if (w.kind == WarpKind::Wave) {
        return waveSource(p, w);
    }
    if (w.kind == WarpKind::Ripple) {
        return rippleSource(p, w);
    }
    if (w.kind == WarpKind::Swirl) {
        return swirlSource(p, w);
    }
    if (w.kind == WarpKind::Bulge) {
        return bulgeSource(p, w);
    }
    return p;
}

inline bool insideImage(const Image& image, PointF p) {
    return p.x >= 0.0 && p.x < image.width() && p.y >= 0.0 && p.y < image.height();
}

inline Image warpImage(const Image& source, const Warp& w, Colour outside,
                       bool linearLight = true) {
    Image result(source.width(), source.height());
    for (int y = 0; y < source.height(); ++y) {
        for (int x = 0; x < source.width(); ++x) {
            const PointF from = warpSource(PointF{x + 0.5, y + 0.5}, w);
            if (insideImage(source, from)) {
                result.setPixel(x, y, sampleBilinear(source, from, linearLight));
            } else {
                result.setPixel(x, y, outside);
            }
        }
    }
    return result;
}

inline Image warpForward(const Image& source, const Warp& w, Colour background, int& holes) {
    Image result(source.width(), source.height(), background);
    std::vector<bool> painted(source.width() * source.height(), false);
    for (int y = 0; y < source.height(); ++y) {
        for (int x = 0; x < source.width(); ++x) {
            const PointF to = warpSource(PointF{x + 0.5, y + 0.5}, w);
            const int tx = static_cast<int>(std::floor(to.x));
            const int ty = static_cast<int>(std::floor(to.y));
            if (tx >= 0 && tx < source.width() && ty >= 0 && ty < source.height()) {
                result.setPixel(tx, ty, source.getPixel(x, y));
                painted[ty * source.width() + tx] = true;
            }
        }
    }
    holes = 0;
    for (bool p : painted) {
        holes += p ? 0 : 1;
    }
    return result;
}

#endif
```

### Line by line

**Describing a warp (lines 1–15)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–6 | include guard and `#include` lines | `std::sin`, `std::pow`, `std::floor`, lists, and Chapter 52's header. |
| 8 | `enum class WarpKind { None, Wave, Ripple, Swirl, Bulge };` | The kinds of warp. Pinch is a bulge with k < 1. |
| 10–15 | `struct Warp { WarpKind kind = WarpKind::None; PointF centre{0.0, 0.0}; double amount = 0.0; double size = 1.0; };` | Everything one warp needs. `amount` is A (pixels) for the wave and ripple, the angle (radians) for the swirl, and k for the bulge. `size` is the wavelength L or the radius R. |

**The source formulas (lines 17–64)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 17–19 | `inline PointF waveSource(PointF p, const Warp& w) { return PointF{p.x + w.amount * std::sin(2.0 * kPi * p.y / w.size), p.y}; }` | Section 53.3. |
| 21–26 | `inline PointF rippleSource(PointF p, const Warp& w) { const Vec2 d = p - w.centre; const double r = length(d); if (r == 0.0) { return p; }` | The step from the centre and its length (Section 53.4). The centre stays put. |
| 27–29 | `const double push = w.amount * std::sin(2.0 * kPi * r / w.size); return w.centre + d * ((r + push) / r); }` | r′ = r + push, then scale the step by r′ / r (Section 53.5). |
| 31–36 | `inline PointF swirlSource(PointF p, const Warp& w) { const Vec2 d = p - w.centre; const double r = length(d); if (r >= w.size) { return p; }` | Outside the radius, nothing changes. |
| 37–39 | `const double angle = w.amount * (1.0 - r / w.size); return w.centre + rotate(d, angle); }` | Turn the step by an angle that fades to 0 at the radius (Section 53.6). |
| 41–48 | `inline PointF bulgeSource(PointF p, const Warp& w) { ... if (r == 0.0 \|\| r >= w.size) { return p; } return w.centre + d * std::pow(r / w.size, w.amount - 1.0); }` | Scale the step by (r / R)^(k − 1) (Section 53.7). The centre is skipped because 0 to a negative power (for a pinch) would be infinite. |
| 50–64 | `inline PointF warpSource(PointF p, const Warp& w) { if (w.kind == WarpKind::Wave) { return waveSource(p, w); } ... return p; }` | Choose the formula by `kind`. `None` (and anything unknown) returns the point itself. |

**Making the new picture (lines 66–84)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 66–68 | `inline bool insideImage(const Image& image, PointF p) { return p.x >= 0.0 && p.x < image.width() && p.y >= 0.0 && p.y < image.height(); }` | Is a point on the picture? (The picture covers 0 … width across and 0 … height down.) |
| 70–75 | `inline Image warpImage(const Image& source, const Warp& w, Colour outside, bool linearLight = true) { Image result(...); for (y) { for (x) { const PointF from = warpSource(PointF{x + 0.5, y + 0.5}, w);` | Backwards: for each new pixel centre, its source point (Section 53.2). |
| 76–84 | `if (insideImage(source, from)) { result.setPixel(x, y, sampleBilinear(source, from, linearLight)); } else { result.setPixel(x, y, outside); }` … `return result; }` | Read with Chapter 35's bilinear sampling, or use the `outside` colour. |

**The wrong way, for counting (lines 86–107)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 86–88 | `inline Image warpForward(const Image& source, const Warp& w, Colour background, int& holes) { Image result(source.width(), source.height(), background); std::vector<bool> painted(source.width() * source.height(), false);` | A picture filled with the background colour, and a list that remembers which pixels were painted. `int& holes` is a reference, so the function can hand back a second answer. |
| 89–99 | `for (y) { for (x) { const PointF to = warpSource(PointF{x + 0.5, y + 0.5}, w); const int tx = ...std::floor(to.x)...; const int ty = ...; if (tx >= 0 && ...) { result.setPixel(tx, ty, source.getPixel(x, y)); painted[ty * source.width() + tx] = true; } } }` | Forwards: each **old** pixel is sent to the pixel that contains `to`. |
| 100–105 | `holes = 0; for (bool p : painted) { holes += p ? 0 : 1; } return result; }` | Count the pixels nobody painted (Section 53.8). |
| 107 | `#endif` | End of the include guard. |

---

## Code, part 2: five warps

File: `ch53/warp.cpp`

```cpp
#include <cmath>
#include <iostream>
#include <string>
#include <vector>
#include "warp.h"
#include "deflate.h"

std::string twoDecimals(double v) {
    const long long n = std::llround(v * 100.0);
    const std::string digits = std::to_string(n % 100);
    return std::to_string(n / 100) + "." + ((digits.size() < 2) ? "0" + digits : digits);
}

std::string pointText(PointF p) {
    return "(" + twoDecimals(p.x) + ", " + twoDecimals(p.y) + ")";
}

void showSource(const std::string& label, const Warp& w, PointF p) {
    std::cout << label << pointText(p) << " reads from " << pointText(warpSource(p, w)) << "\n";
}

Image makeGrid() {
    Image grid(160, 110);
    for (int y = 0; y < 110; ++y) {
        for (int x = 0; x < 160; ++x) {
            const bool light = (x / 10 + y / 10) % 2 == 0;
            grid.setPixel(x, y, light ? Colour{230, 230, 230} : Colour{40, 40, 40});
        }
    }
    return grid;
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
    const PointF middle{80.0, 55.0};
    const Warp none{};
    const Warp wave{WarpKind::Wave, middle, 6.0, 40.0};
    const Warp ripple{WarpKind::Ripple, middle, 3.0, 20.0};
    const Warp swirl{WarpKind::Swirl, middle, kPi / 2.0, 50.0};
    const Warp bulge{WarpKind::Bulge, middle, 2.0, 50.0};
    const Warp pinch{WarpKind::Bulge, middle, 0.5, 50.0};

    showSource("none:   the new point ", none, PointF{105.0, 55.0});
    showSource("wave:   the new point ", wave, PointF{50.0, 10.0});
    showSource("        the new point ", wave, PointF{50.0, 30.0});
    showSource("ripple: the new point ", ripple, PointF{85.0, 55.0});
    showSource("swirl:  the new point ", swirl, PointF{105.0, 55.0});
    showSource("        the new point ", swirl, PointF{80.0, 55.0});
    showSource("bulge:  the new point ", bulge, PointF{105.0, 55.0});
    showSource("pinch:  the new point ", pinch, PointF{105.0, 55.0});

    const Image grid = makeGrid();
    int holes = 0;
    const Image forward = warpForward(grid, swirl, colours::red, holes);
    std::cout << "\nswirl done forwards: " << holes << " of " << grid.width() * grid.height()
              << " pixels never painted\n";

    const Image scene = makeScene();
    const Colour black = colours::black;
    const Image tiles[8] = {scene,
                            warpImage(scene, wave, black),
                            warpImage(scene, swirl, black),
                            warpImage(scene, bulge, black),
                            grid,
                            warpImage(grid, ripple, black),
                            warpImage(grid, pinch, black),
                            forward};
    const std::string names[8] = {"original", "wave",  "swirl",          "bulge",
                                  "grid",     "ripple", "pinch",         "swirl, forwards"};
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
    if (!savePNGCompressed(sheet, "warp.png")) {
        std::cout << "could not write warp.png\n";
        return 1;
    }
    std::cout << "wrote warp.png\n";
    return 0;
}
```

Build and run it from the `code/ch53` folder:

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common warp.cpp -o warp
./warp
```

### Line by line

**Helpers (lines 1–47)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–6 | the `#include` lines | `std::llround`, printing, strings, lists, the new header, and `deflate.h`. |
| 8–12 | `std::string twoDecimals(double v) { const long long n = std::llround(v * 100.0); const std::string digits = std::to_string(n % 100); return std::to_string(n / 100) + "." + ((digits.size() < 2) ? "0" + digits : digits); }` | Exactly two digits after the point: 92.5 → n = 9250 → "92" + "." + "50"; 56.0 → n = 5600 → "56" + "." + "0" made into "00". (For values that are not negative.) |
| 14–16 | `std::string pointText(PointF p) { return "(" + twoDecimals(p.x) + ", " + twoDecimals(p.y) + ")"; }` | A point as "(x, y)". |
| 18–20 | `void showSource(const std::string& label, const Warp& w, PointF p) { std::cout << label << pointText(p) << " reads from " << pointText(warpSource(p, w)) << "\n"; }` | One line of the worked examples. |
| 22–31 | `Image makeGrid() { ... const bool light = (x / 10 + y / 10) % 2 == 0; grid.setPixel(x, y, light ? Colour{230, 230, 230} : Colour{40, 40, 40}); ... }` | A checkerboard of 10-pixel squares: bending is easiest to see on straight lines. |
| 33–47 | `Image makeScene() { ... }` | Chapter 47's scene. |

**The warps and the worked points (lines 50–65)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 50–51 | `const PointF middle{80.0, 55.0}; const Warp none{};` | The centre of the test pictures, and a warp with all the default values (kind `None`). |
| 52–56 | `const Warp wave{WarpKind::Wave, middle, 6.0, 40.0}; const Warp ripple{WarpKind::Ripple, middle, 3.0, 20.0}; const Warp swirl{WarpKind::Swirl, middle, kPi / 2.0, 50.0}; const Warp bulge{WarpKind::Bulge, middle, 2.0, 50.0}; const Warp pinch{WarpKind::Bulge, middle, 0.5, 50.0};` | The five warps of Sections 53.3–53.7. The values in `{}` fill the struct's members in order: kind, centre, amount, size. |
| 58–65 | `showSource("none:   the new point ", none, PointF{105.0, 55.0}); ...` | The worked numbers, one line each. |

**Holes and the picture (lines 67–102)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 67–71 | `const Image grid = makeGrid(); int holes = 0; const Image forward = warpForward(grid, swirl, colours::red, holes); std::cout << ... holes << ...` | The swirl done forwards on the grid, with red holes (Section 53.8). |
| 73–82 | `const Image scene = makeScene(); const Colour black = colours::black; const Image tiles[8] = {scene, warpImage(scene, wave, black), warpImage(scene, swirl, black), warpImage(scene, bulge, black), grid, warpImage(grid, ripple, black), warpImage(grid, pinch, black), forward};` | Eight pictures: the scene and three warps of it; the grid, two warps of it, and the forwards swirl. |
| 83–102 | `const std::string names[8] = {...}; Image sheet(...); for (...) { ... drawText(...); } if (!savePNGCompressed(sheet, "warp.png")) { ... }` … `return 0;` `}` | The 4 × 2 sheet, as in Chapters 51 and 52. |

### What you should see

```
none:   the new point (105.00, 55.00) reads from (105.00, 55.00)
wave:   the new point (50.00, 10.00) reads from (56.00, 10.00)
        the new point (50.00, 30.00) reads from (44.00, 30.00)
ripple: the new point (85.00, 55.00) reads from (88.00, 55.00)
swirl:  the new point (105.00, 55.00) reads from (97.68, 72.68)
        the new point (80.00, 55.00) reads from (80.00, 55.00)
bulge:  the new point (105.00, 55.00) reads from (92.50, 55.00)
pinch:  the new point (105.00, 55.00) reads from (115.36, 55.00)

swirl done forwards: 1472 of 17600 pixels never painted
wrote warp.png
```

In `warp.png`:

- **wave**: the house walls, the sun's sides and the hills' outlines wobble from side to side, as if seen through rippled glass. Thin black slivers along the left and right sides.
- **swirl**: the middle of the scene is twisted round like water going down a drain. The corners are untouched.
- **bulge**: the middle is magnified, as through a glass ball.
- **grid** and **ripple**: the straight squares bend into rings, in and out.
- **pinch**: the squares near the centre are squeezed small; the grid lines curve inwards.
- **swirl, forwards**: a twisted grid sprinkled with red holes.

---

## Small examples

### Example 1 — A row that does not move

Wave with L = 40, row y = 40: 2π × 40 / 40 = 2π, sin(2π) = 0 → no slide. Rows 0, 20, 40, 60 … all stay put.

### Example 2 — A ripple point that reads from nearer in

A = 3, L = 20, r = 15: 2π × 15 / 20 = 3π/2, sin = −1 → r′ = 15 − 3 = **12**.

### Example 3 — The edge of the swirl

R = 50, r = 50: r ≥ R → unchanged. Just inside, at r = 49: angle = π/2 × (1 − 49/50) = π/2 × 0.02 ≈ **1.8°** — almost nothing.

### Example 4 — k = 1

(r / R)^(1 − 1) = (r / R)^0 = **1**: every step stays the same. A "bulge" with k = 1 does nothing.

### Example 5 — Reading between pixels

The wave's source point (56.00, 10.00) lies exactly on the line between pixel 55 (centre 55.5) and pixel 56 (centre 56.5) — halfway. `sampleBilinear` mixes the two 50/50 (and the same for the rows 9 and 10 above and below, since 10.00 is halfway between centres 9.5 and 10.5).

---

## Common mistakes

⚠️ **Writing the formula forwards** — and getting holes. Ask "where does this new pixel come **from**?"

⚠️ **Surprised by the direction** — a backwards formula that reads from +6 moves the picture by −6.

⚠️ **Dividing by r at the centre** — r = 0. Treat the centre on its own.

⚠️ **Forgetting the pixel centre** — use (x + 0.5, y + 0.5), or the whole warp is shifted by half a pixel.

⚠️ **Reading outside the picture** without deciding what that means — choose a colour (or Chapter 49's edge modes).

⚠️ **Warping in place** — the same trap as Chapter 49: later pixels would read already-warped colours. Always into a new picture.

---

## Practice

🏋️ **1.** Make a **vertical** wave: slide each **column** up and down by A × sin(2π × x / L). Write `PointF waveDownSource(PointF p, const Warp& w)`.

🏋️ **2.** Combine two warps: first swirl, then wave (the wave applied to the swirled picture). In which order must the two source formulas be called for one new point?

🏋️ **3.** Make the ripple **fade out** with distance, so that it stops at the radius R = 70.

🏋️ **4.** Where does the new point (80, 105) read from in the swirl? And (80, 70)?

🏋️ **5.** Make a **mirror**: the right half of the picture shows the left half, flipped. Write its source formula.

🏋️ **6.** For the pinch with R = 50 and k = 0.5, where does the new point at r = 1 read from? What does that do to the middle of the picture?

🏋️ **7.** Strong pinches squeeze a big area of the old picture into a few new pixels — and Chapter 50 warned about shrinking without averaging. Write `warpImageSmooth`, which averages 4 × 4 source samples per new pixel (Chapter 27's `sampleOffset`).

🏋️ **8.** Why not just do the warp forwards and fill each hole with the colour of a neighbour?

---

## Answers

**1.**

```cpp
PointF waveDownSource(PointF p, const Warp& w) {
    return PointF{p.x, p.y + w.amount * std::sin(2.0 * kPi * p.x / w.size)};
}
```

> Horizontal lines become wavy, vertical lines stay straight.

**2.**
> The new picture is wave(swirl(old)). Backwards, the **last** step is undone **first**: the new point asks the wave where it came from (a point of the swirled picture), and that point asks the swirl where **it** came from (a point of the old picture):
> `const PointF from = swirlSource(waveSource(p, wave), swirl);`

**3.**

```cpp
PointF rippleFadingSource(PointF p, const Warp& w, double radius) {
    const Vec2 d = p - w.centre;
    const double r = length(d);
    if (r == 0.0 || r >= radius) {
        return p;
    }
    const double push = w.amount * (1.0 - r / radius) * std::sin(2.0 * kPi * r / w.size);
    return w.centre + d * ((r + push) / r);
}
```

**4.**
> (80, 105): d = (0, 50), r = 50 ≥ R → **unchanged**, (80, 105).
> (80, 70): d = (0, 15), r = 15 → angle = π/2 × (1 − 0.3) = 0.35π (63°). rotate((0, 15), 63°) = (0 × cos − 15 × sin, 0 × sin + 15 × cos) = (−15 × 0.891, 15 × 0.454) = (−13.37, 6.81) → **(66.63, 61.81)**.

**5.**

```cpp
PointF mirrorSource(PointF p, double width) {
    if (p.x < width / 2.0) {
        return p;
    }
    return PointF{width - p.x, p.y};
}
```

> A new point at x reads from width − x. (It also works through `warpImage` if you add a `Mirror` kind to the enum and the `if` chain.)

**6.**
> r / R = 0.02 → 0.02^(−0.5) = 1 / √0.02 ≈ 7.07 → reads from r′ ≈ **7.07**. The points between the centre and 1 pixel out show what was within 7 pixels: the middle is squeezed about 7 times — a strong shrink, so it can shimmer (Practice 7 fixes that).

**7.**

```cpp
Image warpImageSmooth(const Image& source, const Warp& w, Colour outside) {
    Image result(source.width(), source.height());
    for (int y = 0; y < source.height(); ++y) {
        for (int x = 0; x < source.width(); ++x) {
            ColourF sum{0.0, 0.0, 0.0};
            for (int j = 0; j < 4; ++j) {
                for (int i = 0; i < 4; ++i) {
                    const PointF p{x + sampleOffset(i, 4), y + sampleOffset(j, 4)};
                    const PointF from = warpSource(p, w);
                    const Colour c = insideImage(source, from) ? sampleBilinear(source, from) : outside;
                    sum = sum + toLinear(c);
                }
            }
            result.setPixel(x, y, fromLinear(sum / 16.0));
        }
    }
    return result;
}
```

> Sixteen times slower, but areas that are squeezed hard no longer shimmer. (Adding up `toLinear` values averages in linear light, as Chapter 50 asked.)

**8.**
> Forwards also paints some pixels **twice**, and the hole-filling has to **guess** — the guess is wrong wherever the warp stretches the picture a lot (the holes get big, and "nearest neighbour" fills them with blocks). Backwards needs no guess: every new pixel gets its colour from exactly the right place, mixed properly by bilinear sampling.

---

## Summary

🧠 A **warp** makes new(x, y) = old(source(x, y)), with any source function. We always write it **backwards**: "where does this new pixel come from?" — no holes.

🧠 Read the old picture with **bilinear** sampling at the source point; choose a colour for points **outside**.

🧠 **Wave**: x + A sin(2π y / L). Round effects use **polar coordinates** around a centre: **ripple** r + A sin(2π r / L); **swirl** turn by amount × (1 − r / R); **bulge/pinch** r′ = R (r / R)^k.

🧠 Make effects fade to "no change" at their radius, so that there is no seam. Handle **r = 0** on its own.

🧠 Forwards, the swirl left **1472** holes (8.4 %).

---

## Next chapter

Part 7 is complete: we can change pictures in every way — values, neighbours, colours and places. Part 8 makes pictures from **nothing but maths**. Its first tool: **random numbers**. Our C++ does not use `<random>` (Chapter 1 promised that), so in Chapter 54 we build our own — starting from the little formula Chapter 39 used for its noisy test picture, finding out why it is not good enough, and making a better one. Then we use them for noise, scattered stars, and the jittered sample positions that Chapter 27 promised.
