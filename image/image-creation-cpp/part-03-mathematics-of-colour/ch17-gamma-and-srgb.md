# Chapter 17 — Gamma and sRGB: Why 128 Is Not Half Bright

> **Part 3 · Chapter 17 of 82**
> **You need:** Chapters 1–16 · **You will make:** `srgb.h` (converting between bytes and real light), `checks.ppm`, `blends.ppm` and `steps.ppm`

---

## What you will learn

- How our eyes judge brightness: by **ratios**, not by differences.
- Why storing the **real amount of light** in a byte would waste most of its 256 levels.
- What **gamma encoding** is, and what a **power** like x^2.2 means.
- The exact **sRGB** formulas, both ways, with worked numbers.
- Why byte **128** gives only about **22%** of the light of 255 — and which byte gives **50%**.
- When to do colour maths in **linear light**, and what goes wrong if you do not.
- True **luminance** (finally), and how it differs from luma.
- How a **lookup table** makes the conversion fast.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **linear light** | Numbers that are exactly proportional to the amount of light. Twice the number = twice the light. |
| **perceived brightness** | How bright something **looks** to us (it is not proportional to the light). |
| **ratio** | How many times bigger one number is than another. 200 ÷ 100 = a ratio of 2. |
| **power** (exponent) | xⁿ: x multiplied by itself n times. x^2.2 is "x to the power 2.2". |
| **gamma** | The power used to change between linear light and stored values. Usually about 2.2. |
| **encode** | Change linear light into stored values (bytes). |
| **decode** | Change stored values back into linear light. |
| **sRGB** | The standard colour space for screens, the web and almost all image files. |
| **banding** | Visible steps (stripes) in what should be a smooth gradient. |
| **lookup table** | A list of answers computed in advance, so we can look them up instead of computing them again. |

---

## 17.1 The question we keep meeting

Three times already, this book has said: "**128 is not half as bright as 255**".

- Chapter 5, Section 5.5: (128, 128, 128) gives only about 22% of the light of white.
- Chapter 13: our gradients were made by lerping **bytes**.
- Chapter 15, Section 15.5: we computed **luma**, not true luminance, because the bytes are not proportional to light.

In this chapter we find out **why**, and how to do it correctly.

📖 **New word: linear light** — numbers that are exactly proportional to the amount of light. If the number doubles, the light doubles.

The bytes in an image file are **not** linear light. They are something else — and there is a very good reason for it.

---

## 17.2 How the eye judges brightness

📖 **New word: perceived brightness** — how bright something **looks** to us.

📖 **New word: ratio** — how many times bigger one number is than another.

Imagine a dark room with **1 candle**. You light a **second** candle. The room looks **much** brighter: the light **doubled**.

Now imagine a room with **100 candles**. You light **one more**. You do not notice any change. The light went up by only 1%.

In both cases you added **the same amount of light** (one candle). But the eye does not care about the amount added. It cares about the **ratio**:

> 2 ÷ 1 = 2 → a big change
> 101 ÷ 100 = 1.01 → no visible change

🧠 **Remember:** The eye judges brightness by **ratios**. In the dark, small changes of light are easy to see. In bright light, the same change is invisible.

This is why a dimmer switch seems to change the room a lot near "off" and very little near "full".

---

## 17.3 What if bytes stored linear light?

Suppose byte value v meant "v ÷ 255 of the full light" — linear light. Let us look at the **ratios** between neighbouring bytes:

🔢 **Maths: steps at the dark end**

> byte 1 → byte 2: ratio 2 ÷ 1 = 2.0 → light **doubles** (a huge, very visible jump)
> byte 10 → byte 11: ratio 1.1 → 10% more light (still visible)

🔢 **Maths: steps at the bright end**

> byte 200 → byte 201: ratio 1.005 → 0.5% more light (invisible)
> byte 254 → byte 255: ratio 1.004 → 0.4% more (invisible)

📖 **New word: banding** — visible steps (stripes) in what should be a smooth gradient.

So with linear bytes:
- In the **dark** part, the steps are too **big**: a dark gradient shows **bands**.
- In the **bright** part, the steps are so small that many of them look **identical**: those levels are **wasted**.

Most of the 256 levels would be spent where our eyes cannot use them, and too few would be left for the dark tones, where our eyes are most sensitive.

The solution: store the bytes so that **each step looks about the same size to the eye**. Spend more levels on the darks and fewer on the brights. That is **gamma encoding**.

---

## 17.4 Powers and gamma

📖 **New word: power** (exponent) — xⁿ means x multiplied by itself n times.

> 0.5² = 0.5 × 0.5 = 0.25
> 0.5³ = 0.5 × 0.5 × 0.5 = 0.125

The power can also be a **decimal**, like 2.2. You cannot "multiply 2.2 times" by hand, but the idea is the same: 0.5^2.2 is a little smaller than 0.5² = 0.25.

> 0.5^2.2 ≈ **0.218**

In C++, `std::pow(x, n)` from `<cmath>` computes xⁿ for any `double` n.

For x between 0 and 1, powers have two useful properties:

| Property | Example |
|---|---|
| 0 and 1 do not change | 0^2.2 = 0, 1^2.2 = 1 |
| a power above 1 makes values **smaller** | 0.5^2.2 ≈ 0.218 |
| a power below 1 makes values **bigger** | 0.5^(1/2.2) = 0.5^0.4545 ≈ 0.730 |

And the two powers **undo each other**:

> (0.5^(1/2.2))^2.2 = 0.5^((1/2.2) × 2.2) = 0.5^1 = 0.5

📖 **New word: gamma** — the power used between linear light and stored values. For screens, it is about **2.2**.

📖 **New word: encode** — linear light → stored value: **stored = light^(1/2.2)**.

📖 **New word: decode** — stored value → linear light: **light = stored^2.2**.

```
 linear light                         stored value (byte ÷ 255)
     1.0 ┤                     ●          1.0 ┤             ●●●●●●●●
         │                   ●                │        ●●●●
         │                 ●                  │     ●●●
     0.5 ┤               ●     decode:        │   ●●       encode:
         │            ●●       stored^2.2     │  ●         light^(1/2.2)
         │         ●●                         │ ●
         │    ●●●●                            │●
     0.0 ●●●●─────────────────── stored       ●──────────────────── light
         0              1                     0              1
```

The **encode** curve rises quickly at first. So a small amount of light (the darks) gets a **big** range of byte values. That is exactly the "more levels for the darks" we wanted in Section 17.3.

### A little history

Old TV and computer screens (with glass tubes, called CRTs) **naturally** turned their input signal into light with a power of about 2.2 to 2.5. By luck, this is close to the inverse of how our eyes judge brightness. So engineers stored the signal "pre-encoded" with the opposite power, and the screen's own curve decoded it. Modern flat screens do not have this natural curve, but they **imitate** it on purpose, so that all the world's images still look right.

---

## 17.5 The exact sRGB curve

📖 **New word: sRGB** — the standard colour space for screens, the web, and almost all image files (PPM, BMP, PNG, JPEG). It was published in 1996.

sRGB does not use a pure power of 2.2. Near black, a pure power curve is **very** steep, which causes problems with tiny numbers. So sRGB uses a **straight line** for the very darkest values, and a power of **2.4** (with an offset) for the rest. Together, the curve is very close to a 2.2 power overall.

Let **v** be the stored value (byte ÷ 255), and **L** the linear light. Both are from 0 to 1.

### Decode: stored → linear

> **if v ≤ 0.04045: L = v ÷ 12.92**
> **otherwise: L = ((v + 0.055) ÷ 1.055)^2.4**

### Encode: linear → stored

> **if L ≤ 0.0031308: v = 12.92 × L**
> **otherwise: v = 1.055 × L^(1/2.4) − 0.055**

(0.0031308 is exactly where the linear part ends: 0.0031308 × 12.92 = 0.04045.)

🔢 **Maths: decode byte 128**

> v = 128 ÷ 255 = 0.50196
> 0.50196 > 0.04045, so use the power part:
> (0.50196 + 0.055) ÷ 1.055 = 0.55696 ÷ 1.055 = 0.52793
> 0.52793^2.4 ≈ **0.2159**

So byte 128 gives **21.6%** of full light — the "about 22%" from Chapter 5 ✓.

🔢 **Maths: decode byte 10** (a very dark value)

> v = 10 ÷ 255 = 0.0392
> 0.0392 ≤ 0.04045, so use the straight-line part:
> L = 0.0392 ÷ 12.92 = **0.00304**

🔢 **Maths: which byte gives exactly half the light?**

> L = 0.5
> 0.5 > 0.0031308, so use the power part:
> 0.5^(1/2.4) = 0.5^0.41667 ≈ 0.74915
> v = 1.055 × 0.74915 − 0.055 = 0.79036 − 0.055 = 0.73536
> byte = 0.73536 × 255 = 187.5 → **188**

So **byte 188** is half the light of 255 — not 128!

| Byte | v | Linear light | |
|---|---|---|---|
| 0 | 0 | 0 | black |
| 64 | 0.251 | 0.0513 | 5% of white's light |
| 128 | 0.502 | 0.2159 | 22% |
| 188 | 0.737 | 0.5029 | **50%** |
| 255 | 1 | 1 | full |

🧠 **Remember:** In sRGB, **byte 128 ≈ 22% of the light**, and **byte 188 ≈ 50%**. Bytes are **not** linear light.

### Why 128 still **looks** like a middle grey

If 128 is only 22% of the light, why does (128, 128, 128) look like a "middle" grey? Because of Section 17.2: the eye judges by ratios. **22% of the light looks about half as bright** to us. That is the whole point of the encoding: **equal byte steps look like equal brightness steps**. The bytes are spaced for the **eye**, not for physics.

---

## 17.6 The simple gamma 2.2 version

Many programs use the simple power instead of the exact sRGB curve:

> decode: L = v^2.2
> encode: v = L^(1/2.2)

🔢 **Maths: byte 128 with plain gamma 2.2**

> 0.50196^2.2 ≈ **0.2195**

The exact sRGB value is 0.2159. The difference is less than 2% of the light — invisible in most pictures. The big difference is near **black**:

> byte 2 (v = 0.00784):
> sRGB: 0.00784 ÷ 12.92 = 0.000607
> gamma 2.2: 0.00784^2.2 ≈ 0.0000229 — about 26 times smaller!

In this book we use the **exact** sRGB formulas. They are only a few lines longer.

---

## 17.7 When to work in linear light

Here is the rule:

> **Physics happens in linear light. Storage happens in sRGB bytes.**

Whenever a calculation is about **amounts of light**, convert to linear first, do the maths, and convert back:

```
bytes ──decode──► linear light ──(add, average, scale, blend)──► linear light ──encode──► bytes
```

| Task | Linear light? |
|---|---|
| adding two lights (Chapter 14's lamps) | **yes** |
| averaging pixels: smooth edges, blur, resizing (Chapters 27, 35, 50) | **yes** |
| lighting and shading (Parts 9 and 10) | **yes** |
| mixing two colours "physically" | **yes** |
| true luminance (Section 17.8) | **yes** |
| storing and loading files | no — files are sRGB |
| a gradient that should **look** evenly spaced to a person | often no (bytes are already "eye-spaced") |

### The famous dark middle

What colour is halfway between red and green?

🔢 **Maths: lerping the bytes** (Chapter 13)

> lerp((255, 0, 0), (0, 255, 0), 0.5) = **(128, 128, 0)**

Decode it: each 128 gives 0.216 of the light. The **total** light is 0.216 + 0.216 = 0.43 — **less than either pure red or pure green alone** (each is 1.0 in its channel). That is why the middle of a byte-lerped red→green gradient looks **dark and muddy**.

🔢 **Maths: lerping in linear light**

> decode: red = (1, 0, 0), green = (0, 1, 0) (0 and 255 decode to 0 and 1)
> lerp at 0.5: (0.5, 0.5, 0) — half of each light, like two half-strength lamps
> encode: 0.5 → 188 (Section 17.5)
> result = **(188, 188, 0)**

This is what you would really see if you shone a half-strength red lamp and a half-strength green lamp on a white wall. It is a clean, bright yellow-olive, with no dark middle. Our `blends.ppm` shows both versions, one above the other.

### The checkerboard test

A pattern of alternating black and white pixels, seen from far away (or squinting), blurs into one grey. That grey has **half** the light: (0 + 1) ÷ 2 = 0.5 in linear light. So it should look like byte **188**, not byte 128.

Our `checks.ppm` puts three squares side by side: the checkerboard, solid 128, and solid 188. Step back from the screen (or squint). The checkerboard matches **188**, not 128.

⚠️ **Careful:** This test only works when the image is shown at **exactly 100%** zoom. If your viewer shrinks or enlarges the image, it mixes the pixels (often in byte space!) and the test is spoiled.

---

## 17.8 True luminance

In Chapter 15 we computed **luma**: the weights applied directly to the bytes (÷ 255). Now we can compute true **luminance**: decode first, then apply the weights.

> luminance = 0.2126 × L_r + 0.7152 × L_g + 0.0722 × L_b (with linear L values)

The result is **linear** light too. To show it as a grey pixel, we **encode** it back.

🔢 **Maths: orange (255, 128, 0)**

> decode: (1.0, 0.2159, 0.0)
> luminance = 0.2126 × 1.0 + 0.7152 × 0.2159 + 0.0722 × 0
> = 0.2126 + 0.1544 = **0.3670**
> encode: 1.055 × 0.3670^(1/2.4) − 0.055 ≈ 0.6398 → × 255 = 163.2 → **163**

| Method | Grey byte for orange |
|---|---|
| plain average (Chapter 15) | 128 |
| luma (Chapter 15) | 146 |
| **true luminance** | **163** |

Luma came out **too dark** for orange. In general, luma is close to luminance for greys and pale colours, but it makes strong, saturated colours look too dark in grey. For most photos, the difference is small, which is why luma is still widely used. When accuracy matters, use luminance.

---

## 17.9 A lookup table for speed

📖 **New word: lookup table** — a list of answers computed in advance.

`std::pow` is slow compared with + and ×. A 1920 × 1080 image has 6.2 million channel values (Chapter 4). Computing `std::pow` for each one takes noticeable time.

But a **byte** has only **256** possible values. So we can compute the decoded value for all 256 bytes **once**, put them in a list, and afterwards just **look them up**:

```
index (byte):  0     1        2        …   128      …   255
value:         0.0   0.000304 0.000607 …   0.2159   …   1.0
```

In C++ we use `std::array<double, 256>` (from `<array>`, on our list from Chapter 1). To build it **only once** — the first time it is needed — we use a `static` variable inside a function:

```cpp
inline const std::array<double, 256>& linearTable() {
    static const std::array<double, 256> table = makeLinearTable();
    return table;
}
```

- A `static` local variable is created the **first** time the function runs, and then **kept** for the rest of the program.
- Every later call returns the same table, with no work.
- Because the function is `inline`, all `.cpp` files of a program share **one** table.

Encoding (linear → bytes) has no such shortcut: linear values are `double`s with endless possible values. We just call `linearToSrgb`.

---

## Code, part 1: `srgb.h`

File: `common/srgb.h` (new). It includes `colourf.h`.

```cpp
#ifndef SRGB_H
#define SRGB_H

#include <algorithm>
#include <array>
#include <cmath>
#include "colourf.h"

inline double srgbToLinear(double v) {
    if (v <= 0.04045) {
        return v / 12.92;
    }
    return std::pow((v + 0.055) / 1.055, 2.4);
}

inline double linearToSrgb(double l) {
    l = std::clamp(l, 0.0, 1.0);
    if (l <= 0.0031308) {
        return 12.92 * l;
    }
    return 1.055 * std::pow(l, 1.0 / 2.4) - 0.055;
}

inline std::array<double, 256> makeLinearTable() {
    std::array<double, 256> table{};
    for (int i = 0; i < 256; ++i) {
        table[i] = srgbToLinear(i / 255.0);
    }
    return table;
}

inline const std::array<double, 256>& linearTable() {
    static const std::array<double, 256> table = makeLinearTable();
    return table;
}

inline ColourF toLinear(Colour c) {
    const std::array<double, 256>& t = linearTable();
    return ColourF{t[c.r], t[c.g], t[c.b]};
}

inline Colour fromLinear(ColourF l) {
    return toColour(ColourF{linearToSrgb(l.r), linearToSrgb(l.g), linearToSrgb(l.b)});
}

inline Colour lerpLinear(Colour a, Colour b, double t) {
    ColourF la = toLinear(a);
    ColourF lb = toLinear(b);
    return fromLinear(la + (lb - la) * t);
}

inline double luminance(Colour c) {
    ColourF l = toLinear(c);
    return 0.2126 * l.r + 0.7152 * l.g + 0.0722 * l.b;
}

#endif
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef SRGB_H` / `#define SRGB_H` | Include guard. |
| 4 | `#include <algorithm>` | `std::clamp`. |
| 5 | `#include <array>` | `std::array`, for the lookup table. |
| 6 | `#include <cmath>` | `std::pow`. |
| 7 | `#include "colourf.h"` | `ColourF`, `toColour` and the operators (Chapter 14). |
| 9 | `inline double srgbToLinear(double v) {` | **Decode**: a stored value (0–1) → linear light (0–1). |
| 10–12 | `if (v <= 0.04045) { return v / 12.92; }` | The straight-line part, for the very darkest values (Section 17.5). |
| 13 | `return std::pow((v + 0.055) / 1.055, 2.4);` | The power part, for everything else. |
| 14 | `}` | End. |
| 16 | `inline double linearToSrgb(double l) {` | **Encode**: linear light → a stored value. |
| 17 | `l = std::clamp(l, 0.0, 1.0);` | Linear light from our maths might go below 0 or above 1. Clamp first. (Also, `std::pow` of a **negative** number with a decimal power gives "not a number".) |
| 18–20 | `if (l <= 0.0031308) { return 12.92 * l; }` | The straight-line part. |
| 21 | `return 1.055 * std::pow(l, 1.0 / 2.4) - 0.055;` | The power part. `1.0 / 2.4` (not `1 / 2.4`) keeps it a `double`. |
| 22 | `}` | End. |
| 24 | `inline std::array<double, 256> makeLinearTable() {` | Build the lookup table (Section 17.9). |
| 25 | `std::array<double, 256> table{};` | 256 `double`s. The `{}` sets them all to 0 to start. |
| 26–28 | `for (int i = 0; i < 256; ++i) { table[i] = srgbToLinear(i / 255.0); }` | For every possible byte, store its decoded value. |
| 29–30 | `return table;` `}` | Give back the finished table. |
| 32 | `inline const std::array<double, 256>& linearTable() {` | Give access to **one** shared table. Returns a `const` reference: no copy, no changes. |
| 33 | `static const std::array<double, 256> table = makeLinearTable();` | `static`: made the **first** time this line runs, then kept forever. Later calls skip this line's work. |
| 34–35 | `return table;` `}` | Give back the table. |
| 37 | `inline ColourF toLinear(Colour c) {` | Decode a whole byte colour into linear light. |
| 38 | `const std::array<double, 256>& t = linearTable();` | Get the table. |
| 39 | `return ColourF{t[c.r], t[c.g], t[c.b]};` | Look up each channel. A byte (0–255) is always a valid index. No `std::pow` here at all. |
| 40 | `}` | End. |
| 42 | `inline Colour fromLinear(ColourF l) {` | Encode linear light back into a byte colour. |
| 43 | `return toColour(ColourF{linearToSrgb(l.r), linearToSrgb(l.g), linearToSrgb(l.b)});` | Encode each channel (0–1), then `toColour` (Chapter 14) turns them into rounded, clamped bytes. |
| 44 | `}` | End. |
| 46 | `inline Colour lerpLinear(Colour a, Colour b, double t) {` | Lerp two colours **in linear light** (Section 17.7). |
| 47–48 | `ColourF la = toLinear(a);` / `ColourF lb = toLinear(b);` | Decode both. |
| 49 | `return fromLinear(la + (lb - la) * t);` | Lerp with the `ColourF` operators, then encode. |
| 50 | `}` | End. |
| 52 | `inline double luminance(Colour c) {` | True luminance (Section 17.8). Returns **linear** light, 0–1. |
| 53 | `ColourF l = toLinear(c);` | Decode first… |
| 54 | `return 0.2126 * l.r + 0.7152 * l.g + 0.0722 * l.b;` | …then the Rec. 709 weights from Chapter 15. |
| 55 | `}` | End. |
| 57 | `#endif` | End of the include guard. |

---

## Code, part 2: seeing gamma

File: `ch17/gamma.cpp`

```cpp
#include <cmath>
#include <iostream>
#include <string>
#include "grey.h"
#include "srgb.h"

double roundTo(double v, double factor) {
    return std::floor(v * factor + 0.5) / factor;
}

void printColour(const std::string& label, Colour c) {
    std::cout << label << " = (" << static_cast<int>(c.r) << ", "
              << static_cast<int>(c.g) << ", " << static_cast<int>(c.b) << ")\n";
}

int main() {
    const int bytes[5] = {0, 64, 128, 188, 255};
    for (int b : bytes) {
        std::cout << "byte " << b << " gives " << roundTo(srgbToLinear(b / 255.0), 10000)
                  << " of full light\n";
    }
    std::cout << "half the light needs byte "
              << static_cast<int>(toByte(linearToSrgb(0.5))) << "\n";
    std::cout << "gamma 2.2 guess for byte 128: "
              << roundTo(std::pow(128 / 255.0, 2.2), 10000) << "\n\n";

    printColour("red-green middle, byte lerp  ", lerpColour(colours::red, colours::green, 0.5));
    printColour("red-green middle, linear lerp", lerpLinear(colours::red, colours::green, 0.5));

    const Colour orange{255, 128, 0};
    double lum = luminance(orange);
    std::cout << "orange: luma byte " << static_cast<int>(greyByte(orange))
              << ", luminance " << roundTo(lum, 1000)
              << ", as a grey byte " << static_cast<int>(toByte(linearToSrgb(lum))) << "\n";

    Image checks(300, 100);
    for (int y = 0; y < checks.height(); ++y) {
        for (int x = 0; x < checks.width(); ++x) {
            Colour c;
            if (x < 100) {
                c = ((x + y) % 2 == 0) ? colours::black : colours::white;
            } else if (x < 200) {
                c = Colour{128, 128, 128};
            } else {
                c = Colour{188, 188, 188};
            }
            checks.setPixel(x, y, c);
        }
    }

    Image blends(300, 100);
    for (int y = 0; y < blends.height(); ++y) {
        for (int x = 0; x < blends.width(); ++x) {
            double t = static_cast<double>(x) / (blends.width() - 1);
            Colour c = (y < 50) ? lerpColour(colours::red, colours::green, t)
                                : lerpLinear(colours::red, colours::green, t);
            blends.setPixel(x, y, c);
        }
    }

    Image steps(320, 100);
    for (int y = 0; y < steps.height(); ++y) {
        for (int x = 0; x < steps.width(); ++x) {
            int band = x / 20;
            std::uint8_t v = 0;
            if (y < 50) {
                v = static_cast<std::uint8_t>(band * 17);
            } else {
                v = toByte(linearToSrgb(band / 15.0));
            }
            steps.setPixel(x, y, Colour{v, v, v});
        }
    }

    bool ok = checks.savePPM("checks.ppm");
    ok = ok && blends.savePPM("blends.ppm");
    ok = ok && steps.savePPM("steps.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
```

### Line by line

**Numbers (lines 1–34)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–3 | `#include <cmath>` / `<iostream>` / `<string>` | `std::floor` and `std::pow`, printing, labels. |
| 4 | `#include "grey.h"` | For `greyByte` (luma, Chapter 15), to compare with luminance. |
| 5 | `#include "srgb.h"` | Our new header. Both headers include `colourf.h`; the include guards make sure it is read only once. |
| 7–9 | `double roundTo(double v, double factor) { ... }` | Round to some decimal places (Chapter 16). |
| 11–14 | `void printColour(...) { ... }` | Print a colour as numbers. |
| 16 | `int main() {` | The program starts here. |
| 17 | `const int bytes[5] = {0, 64, 128, 188, 255};` | Five byte values to decode. |
| 18–21 | `for (int b : bytes) { std::cout << ... srgbToLinear(b / 255.0) ... }` | Print how much light each byte really gives (the table in Section 17.5). |
| 22–23 | `std::cout << "half the light needs byte " << static_cast<int>(toByte(linearToSrgb(0.5))) << "\n";` | Encode 0.5 linear light, then turn it into a byte with `toByte` (× 255 and round). Expect 188. |
| 24–25 | `std::cout << "gamma 2.2 guess for byte 128: " << roundTo(std::pow(128 / 255.0, 2.2), 10000) ...` | The simple gamma 2.2 version, for comparison (Section 17.6). |
| 27 | `printColour("red-green middle, byte lerp  ", lerpColour(colours::red, colours::green, 0.5));` | Chapter 13's byte lerp: expect (128, 128, 0). |
| 28 | `printColour("red-green middle, linear lerp", lerpLinear(colours::red, colours::green, 0.5));` | Lerp in linear light: expect (188, 188, 0). |
| 30 | `const Colour orange{255, 128, 0};` | The colour from Section 17.8. |
| 31 | `double lum = luminance(orange);` | True luminance, as linear light. |
| 32–34 | `std::cout << "orange: luma byte " << ... greyByte(orange) ... luminance ... toByte(linearToSrgb(lum)) ...` | Print luma (as a byte), luminance (as linear light), and luminance encoded as a grey byte. |

**Three test images (lines 36–83)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 36 | `Image checks(300, 100);` | Three squares of 100 × 100. |
| 37–38 | `for (int y ...) { for (int x ...) {` | Every pixel. |
| 39 | `Colour c;` | The colour for this pixel (black by default). |
| 40–41 | `if (x < 100) { c = ((x + y) % 2 == 0) ? colours::black : colours::white; }` | Left square: a 1-pixel checkerboard of black and white (Chapter 10). |
| 42–43 | `else if (x < 200) { c = Colour{128, 128, 128}; }` | Middle square: byte 128. |
| 44–46 | `else { c = Colour{188, 188, 188}; }` | Right square: byte 188, which is half the light. |
| 47 | `checks.setPixel(x, y, c);` | Store it. |
| 48–49 | `}` `}` | End of the loops. |
| 51 | `Image blends(300, 100);` | Two gradients, one above the other. |
| 52–53 | `for (int y ...) { for (int x ...) {` | Every pixel. |
| 54 | `double t = static_cast<double>(x) / (blends.width() - 1);` | t from 0 to 1 (Chapter 13). |
| 55–56 | `Colour c = (y < 50) ? lerpColour(...) : lerpLinear(...);` | Top half: lerp the **bytes**. Bottom half: lerp in **linear light**. |
| 57 | `blends.setPixel(x, y, c);` | Store it. |
| 58–59 | `}` `}` | End of the loops. |
| 61 | `Image steps(320, 100);` | 16 grey bands of 20 pixels each. |
| 62–63 | `for (int y ...) { for (int x ...) {` | Every pixel. |
| 64 | `int band = x / 20;` | Band number 0 to 15. |
| 65 | `std::uint8_t v = 0;` | The grey byte. |
| 66–67 | `if (y < 50) { v = static_cast<std::uint8_t>(band * 17); }` | Top half: **equal byte steps**: 0, 17, 34, … 255 (15 × 17 = 255). |
| 68–70 | `} else { v = toByte(linearToSrgb(band / 15.0)); }` | Bottom half: **equal light steps**: 0, 1/15, 2/15, … 1 of the light, encoded into bytes. |
| 71 | `steps.setPixel(x, y, Colour{v, v, v});` | A grey pixel. |
| 72–73 | `}` `}` | End of the loops. |
| 75–81 | `bool ok = checks.savePPM(...); ... if (!ok) { ...; return 1; }` | Save the three images. |
| 82 | `return 0;` | The program finished with no problem. |
| 83 | `}` | End of `main`. |

Compile:

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common gamma.cpp -o gamma
```

### What you should see

```
byte 0 gives 0 of full light
byte 64 gives 0.0513 of full light
byte 128 gives 0.2159 of full light
byte 188 gives 0.5029 of full light
byte 255 gives 1 of full light
half the light needs byte 188
gamma 2.2 guess for byte 128: 0.2195

red-green middle, byte lerp   = (128, 128, 0)
red-green middle, linear lerp = (188, 188, 0)
orange: luma byte 146, luminance 0.367, as a grey byte 163
```

Every number matches the worked maths in Sections 17.5 to 17.8.

Open the images **at 100% zoom**:
- `checks.ppm`: step back or squint. The checkerboard on the left blends into a grey that matches the **right** square (188), not the middle one (128).
- `blends.ppm`: the top gradient (byte lerp) has a **dark, brownish middle**. The bottom one (linear lerp) stays bright all the way, through a clean yellow.
- `steps.ppm`: the top row (equal **byte** steps) looks evenly spaced to your eye. The bottom row (equal **light** steps) jumps from black to a dark grey (byte 73) in one step, and then most of the bands look very similar and light. This is Section 17.3 in a picture: linear steps waste levels on the brights and are too coarse in the darks.

🔢 **Maths: the first two bottom bands**

> band 0: 0 ÷ 15 = 0 → byte 0
> band 1: 1 ÷ 15 = 0.0667 → 1.055 × 0.0667^(1/2.4) − 0.055 = 1.055 × 0.3236 − 0.055 = 0.2864 → × 255 = **73**

One linear step of only 6.7% of the light jumps all the way to byte 73.

---

## Small examples

### Example 1 — Average two pixels correctly

The average of black and white (Chapter 14, Section 14.9):

> in bytes: (0 + 255) ÷ 2 = 127.5 → **128** (too dark)
> in linear light: (0 + 1) ÷ 2 = 0.5 → encode → **188** (correct)

When we make smooth edges (Chapter 27) and shrink images (Chapter 35), we will average in **linear light**, so that thin white lines on black do not get too dark.

### Example 2 — Two lamps, done right

In Chapter 14 we added lamp colours as 0–1 values made straight from bytes. That is correct only for 0 and 255 (which decode to 0 and 1). For a dimmer lamp like (128, 0, 0) plus (128, 0, 0):

> bytes as 0–1: 0.502 + 0.502 = 1.004 → clamped → 255 (wrong: twice "22% light" is not "full light")
> linear: 0.2159 + 0.2159 = 0.4318 → encode → 0.6885 → × 255 = 175.6 → **176**

The correct result is (176, 0, 0): brighter than one lamp, but far from full.

### Example 3 — Darken by half the light

"Half as much light" is **not** "half the byte":

> byte 200 → linear 0.5776 → × 0.5 = 0.2888 → encode → 0.5738 → × 255 = 146.3 → **146**
> (Halving the byte would give 100, which is only about 13% of the light — much too dark.)

### Example 4 — How fast is the lookup table?

For a 1920 × 1080 image, `toLinear` for every pixel means:

> without the table: 1920 × 1080 × 3 = 6,220,800 calls to `std::pow`
> with the table: 256 calls to `std::pow` (once), then 6,220,800 simple array reads

---

## Common mistakes

⚠️ **Doing light maths on bytes.** Averages, blends and added lights come out too dark. Decode first.

⚠️ **Forgetting to encode at the end.** If you store linear values as bytes, the picture looks much too dark and harsh (byte 54 instead of 128 for "22% light").

⚠️ **Decoding twice.** Decoding a value that is already linear makes it even darker. Keep track of which numbers are linear and which are sRGB. (A good habit: name linear variables `l…` or `lin…`.)

⚠️ **`std::pow` of a negative number.** `std::pow(-0.1, 1.0 / 2.4)` is NaN ("not a number"). Clamp before encoding.

⚠️ **`1 / 2.4`.** With an `int` 1, this is fine in C++ (2.4 is a `double`), but `1 / 2` would be 0. Write `1.0 / 2.4` to be safe and clear.

⚠️ **Testing at the wrong zoom.** The checkerboard test needs 100% zoom.

---

## Practice

🏋️ **1.** Decode byte 200 to linear light with the sRGB formula. Show every step.

🏋️ **2.** Which byte gives 25% of the light? (Encode 0.25.)

🏋️ **3.** Decode byte 5. Which part of the formula do you use?

🏋️ **4.** Compute the halfway colour between blue (0, 0, 255) and white (255, 255, 255), both in bytes and in linear light.

🏋️ **5.** Compute the luma and the true luminance (as a grey byte) of pure green (0, 255, 0). Why are they so different?

🏋️ **6.** Change the `checks` test to use a pattern of **one white pixel and three black pixels** (in each 2 × 2 block). What linear light does it have? Which byte should it match?

🏋️ **7.** Add a function `Colour averageLinear(Colour a, Colour b)` to a program and use it to average (255, 0, 0) and (0, 0, 255).

---

## Answers

**1.**
> v = 200 ÷ 255 = 0.7843
> 0.7843 > 0.04045 → power part
> (0.7843 + 0.055) ÷ 1.055 = 0.8393 ÷ 1.055 = 0.7956
> 0.7956^2.4 ≈ **0.578** — about 58% of the light

**2.**
> L = 0.25 → 0.25^(1/2.4) = 0.25^0.41667 ≈ 0.5612
> v = 1.055 × 0.5612 − 0.055 = 0.5921 − 0.055 = 0.5371
> byte = 0.5371 × 255 = 136.96 → **137**

**3.**
> v = 5 ÷ 255 = 0.0196
> 0.0196 ≤ 0.04045 → the **straight-line** part
> L = 0.0196 ÷ 12.92 = **0.00152**

**4.**
> bytes: lerp at 0.5 → (127.5, 127.5, 255) → **(128, 128, 255)**
> linear: blue = (0, 0, 1), white = (1, 1, 1) → middle (0.5, 0.5, 1) → encode → **(188, 188, 255)**

The linear version is a lighter, cleaner sky blue. The byte version looks a bit dull and too dark.

**5.**
> luma: 0.7152 × 1.0 = 0.7152 → × 255 = **182**
> luminance: decode (0, 1, 0) → 0.7152 × 1 = 0.7152 (linear) → encode: 1.055 × 0.7152^(1/2.4) − 0.055 = 1.055 × 0.8695 − 0.055 = 0.8623 → × 255 = **220**

They differ because luminance is **linear** light (0.7152 = 71.5% of the light), and 71.5% of the light, encoded, is byte 220. Luma uses the weight directly on the byte scale, which treats 0.7152 as if it were already a byte fraction.

**6.**
> one white (1) and three black (0) in each block → average light = 1 ÷ 4 = **0.25**
> encode 0.25 → byte **137** (Practice 2)

Change line 41 to `c = (x % 2 == 0 && y % 2 == 0) ? colours::white : colours::black;` and the right square to `Colour{137, 137, 137}`.

**7.**

```cpp
Colour averageLinear(Colour a, Colour b) {
    ColourF la = toLinear(a);
    ColourF lb = toLinear(b);
    return fromLinear((la + lb) / 2.0);
}
```

> (1, 0, 0) and (0, 0, 1) → (0.5, 0, 0.5) → encode → **(188, 0, 188)**

(In bytes, it would be (128, 0, 128), a darker purple.)

---

## Summary

🧠 The eye judges brightness by **ratios**. Dark tones need more levels than bright ones.

🧠 So image bytes are **gamma encoded**: bytes are **not** linear light.

🧠 sRGB decode: v ≤ 0.04045 → v ÷ 12.92, else ((v + 0.055) ÷ 1.055)^2.4. Encode is the opposite.

🧠 **Byte 128 ≈ 22% of the light. Byte 188 ≈ 50%.** 128 only **looks** middle grey.

🧠 Plain gamma 2.2 is a close approximation, except very near black.

🧠 **Physics in linear light, storage in sRGB**: decode → add/average/blend → encode.

🧠 True **luminance** = the weights on **linear** values. Luma makes saturated colours too dark.

🧠 A 256-entry **lookup table** makes decoding fast.

---

## Next chapter

In Chapter 18, the last chapter of Part 3, we make colours **see-through**. We add a fourth channel, **alpha**, and learn how to place one image **over** another, how transparent colours mix, and why "premultiplied" alpha makes the maths cleaner.
