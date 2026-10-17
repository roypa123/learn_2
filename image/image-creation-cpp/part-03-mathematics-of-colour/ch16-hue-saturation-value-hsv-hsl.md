# Chapter 16 — Hue, Saturation, Value (HSV and HSL)

> **Part 3 · Chapter 16 of 82**
> **You need:** Chapters 1–15 · **You will make:** `hsv.h` (conversions between RGB, HSV and HSL), `hue_strip.ppm`, `picker.ppm` (a colour-picker square), `lightness.ppm` and `bars_shifted.ppm`

---

## What you will learn

- Why people find RGB hard to use, and what they want instead.
- **Hue**: the "kind" of colour, measured as an angle on a **colour wheel**.
- **HSV**: hue, **saturation**, **value**. How to compute it from RGB, and back.
- **HSL**: hue, saturation, **lightness**. How it differs from HSV.
- The ideas of **chroma** and **sector** that make the conversions work.
- How to **shift the hue** of a whole picture.
- What HSV and HSL **cannot** do well.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **colour model** | A way to describe a colour with numbers. RGB is one; HSV and HSL are others. |
| **hue** | The "kind" of colour: red, orange, yellow, green… |
| **colour wheel** | The hues arranged in a circle, so that red comes back after magenta. |
| **degree (°)** | A unit for parts of a turn. A full turn is 360°. |
| **saturation** | How strong the colour is, from grey (0) to pure (1). (First met in Chapter 15.) |
| **value** | In HSV: how bright the strongest channel is, from black (0) to full (1). |
| **lightness** | In HSL: how light a colour is, from black (0) through the pure colour (0.5) to white (1). |
| **chroma** | How far a colour is from grey: the strongest channel minus the weakest. |
| **sector** | One of the six 60° slices of the colour wheel. |
| **hue shift** | Turning every hue in a picture by the same angle. |

---

## 16.1 Why another colour model?

📖 **New word: colour model** — a way to describe a colour with numbers.

Try to answer this with RGB: "I have (200, 120, 40), a brown-orange. Make it **a bit more yellow** and **a little paler**."

Which numbers do you change? Green up? Blue up too? By how much? It is hard. RGB says **how much of each light to mix**, which is perfect for a screen. But it is not how **people** think about colour.

People describe colour with three different ideas:

| Question | Name |
|---|---|
| Which colour is it? Red? Orange? Blue? | **hue** |
| How strong is it? Bright and pure, or greyish and dull? | **saturation** |
| How light or dark is it? | **value** (HSV) or **lightness** (HSL) |

HSV and HSL are two colour models built on exactly these ideas. They were made in the 1970s for computer paint programs, and nearly every colour picker you have ever used is built on one of them.

💡 **Tip:** HSV and HSL do not add any new colours. Every HSV or HSL colour **is** an RGB colour. They are only a different way to **name** the same colours — like describing a place by "3 km north-east" instead of by (x, y).

---

## 16.2 Hue: the colour wheel

📖 **New word: hue** — the "kind" of colour.

Look at the six colours of the rainbow from Chapter 13: red, yellow, green, cyan, blue, magenta. After magenta, if we keep going, we come **back to red** (magenta is between blue and red). So the hues do not form a line — they form a **circle**.

📖 **New word: colour wheel** — the hues arranged in a circle.

📖 **New word: degree (°)** — a unit for parts of a turn. A full turn is **360°**, a half turn is 180°, a quarter turn is 90°. (Chapter 30 teaches angles fully. Here we only need degrees as a way to say "how far round the circle".)

```
                    0° red
                     ●
        300°  ●             ●  60°
      magenta                  yellow

        240°  ●             ●  120°
         blue                  green
                     ●
                 180° cyan
```

The six corner colours sit **60° apart**:

| Hue | Colour | RGB (0–1) |
|---|---|---|
| 0° | red | (1, 0, 0) |
| 60° | yellow | (1, 1, 0) |
| 120° | green | (0, 1, 0) |
| 180° | cyan | (0, 1, 1) |
| 240° | blue | (0, 0, 1) |
| 300° | magenta | (1, 0, 1) |
| 360° | red again | (1, 0, 0) |

Every hue between them is a mix of the two neighbours. Orange is at about 30° (between red and yellow). Violet is at about 270° (between blue and magenta).

### Wrapping the hue

Because it is a circle, **360° is the same as 0°**, 370° is the same as 10°, and −30° is the same as 330°. We **wrap** any angle into the range 0 to 360:

🔢 **Maths: wrapping**

> 370 → 370 − 360 = **10**
> 725 → 725 − 360 − 360 = **5**
> −30 → −30 + 360 = **330**

In C++, `std::fmod(h, 360.0)` gives the **remainder** of h ÷ 360 for `double`s (like `%` for `int`s, Chapter 6). But for negative numbers, `fmod` gives a negative remainder (`fmod(-30, 360)` is −30), so we add 360 when the result is below 0. That is our `wrapHue` function.

---

## 16.3 Saturation and value (HSV)

📖 **New word: value** — in HSV: how bright the **strongest** channel is.

📖 **New word: saturation** — how strong the colour is (Chapter 15). In HSV: how far the **weakest** channel is from the strongest.

For a colour (r, g, b) with values from 0 to 1, let:

> max = the biggest of r, g, b
> min = the smallest of r, g, b

Then:

> **V = max**
> **S = (max − min) ÷ max** (and S = 0 when max = 0, to avoid dividing by zero)

🔢 **Maths: four colours**

| Colour | (r, g, b) | max | min | V | S |
|---|---|---|---|---|---|
| red | (1, 0, 0) | 1 | 0 | 1 | (1 − 0) ÷ 1 = **1** |
| dark red | (0.5, 0, 0) | 0.5 | 0 | 0.5 | 0.5 ÷ 0.5 = **1** |
| pink | (1, 0.753, 0.796) | 1 | 0.753 | 1 | 0.247 ÷ 1 = **0.247** |
| grey | (0.5, 0.5, 0.5) | 0.5 | 0.5 | 0.5 | 0 ÷ 0.5 = **0** |

- **Dark red** still has S = 1: it is a **pure** red, just not bright. Only V went down.
- **Pink** has a low S: its weakest channel (green 0.753) is close to its strongest (red 1). There is a lot of "white" mixed in.
- **Grey** has S = 0: all channels are equal, there is no colour at all.

### A picture of HSV

Imagine a **cone** standing on its point:

```
     pure colours (S = 1, V = 1) all round the rim
        ●───────────●───────────●
         ╲        white        ╱     ← top: V = 1. White is in the centre of the top.
          ╲         │         ╱
           ╲      greys      ╱       V goes up: from the point (black) to the top
            ╲   down the    ╱        S goes out: from the centre line (grey) to the rim (pure)
             ╲    axis     ╱         H goes round the centre line
              ╲     │     ╱
               ╲    │    ╱
                ╲   │   ╱
                 ╲  │  ╱
                  ╲ │ ╱
                    ●  black (V = 0)
```

- **V** is the height: black at the bottom point, bright at the top.
- **S** is the distance from the centre line: grey in the middle, pure colour at the edge.
- **H** is the angle around the centre.

---

## 16.4 Finding the hue

📖 **New word: chroma** — how far a colour is from grey: **chroma = max − min**.

The hue depends on **which channel is the biggest**. Each case covers 120° of the wheel:

| Biggest channel | Hue range | Formula |
|---|---|---|
| red | from −60° to 60° (around 0°) | H = 60 × (g − b) ÷ chroma |
| green | from 60° to 180° (around 120°) | H = 60 × ((b − r) ÷ chroma + 2) |
| blue | from 180° to 300° (around 240°) | H = 60 × ((r − g) ÷ chroma + 4) |

Then **wrap** the result into 0–360. If chroma = 0 (a grey), there is **no** hue; we use 0.

Why does this work? Take the "red is biggest" case. If green is bigger than blue, the colour leans toward **yellow** (60°), so the hue is positive. If blue is bigger, it leans toward **magenta** (300° = −60°), so the hue is negative. The `(g − b) ÷ chroma` part is a number from −1 to 1 that says **how far** it leans. The `+ 2` and `+ 4` in the other cases move the middle of the range to 120° and 240°.

🔢 **Maths: orange (1.0, 0.502, 0.0)**

> max = 1.0 (red), min = 0.0, chroma = 1.0
> red is biggest: H = 60 × (0.502 − 0.0) ÷ 1.0 = 60 × 0.502 = **30.1°**
> V = 1.0, S = 1.0 ÷ 1.0 = 1.0
> **HSV = (30.1°, 1, 1)** — halfway between red (0°) and yellow (60°) ✓

🔢 **Maths: a leafy green (100, 200, 50) = (0.392, 0.784, 0.196)**

> max = 0.784 (green), min = 0.196, chroma = 0.588
> green is biggest: H = 60 × ((0.196 − 0.392) ÷ 0.588 + 2)
> = 60 × (−0.333 + 2) = 60 × 1.667 = **100°**
> V = 0.784, S = 0.588 ÷ 0.784 = **0.75**
> **HSV = (100°, 0.75, 0.784)**

100° is between yellow (60°) and green (120°), closer to green. A yellowish green ✓.

🔢 **Maths: pink (1.0, 0.753, 0.796)**

> max = 1.0 (red), min = 0.753, chroma = 0.247
> red is biggest: H = 60 × (0.753 − 0.796) ÷ 0.247 = 60 × (−0.043 ÷ 0.247) = 60 × (−0.175) = **−10.5°**
> wrap: −10.5 + 360 = **349.5°**
> **HSV = (349.5°, 0.247, 1)** — a red that leans slightly toward magenta

---

## 16.5 From HSV back to RGB

📖 **New word: sector** — one of the six 60° slices of the wheel.

Going back has four steps.

**Step 1: chroma.** From S = (max − min) ÷ max and V = max:

> C = V × S (this is max − min)

**Step 2: which sector, and the "middle" channel.** Divide the hue by 60 to get a number from 0 to 6: `hp = H ÷ 60`. Its whole part (0–5) is the **sector**. In each sector, one channel is the biggest (= C), one is the smallest (= 0), and the third one is somewhere in between:

> X = C × (1 − |hp mod 2 − 1|)

The bars `| |` mean "drop the minus sign" (Chapter 3). X goes up from 0 to C and back down, like a tent, every two sectors.

| Sector | hp | (r, g, b) before step 4 | Why |
|---|---|---|---|
| 0 | 0–1 | (C, X, 0) | red to yellow: green rising |
| 1 | 1–2 | (X, C, 0) | yellow to green: red falling |
| 2 | 2–3 | (0, C, X) | green to cyan: blue rising |
| 3 | 3–4 | (0, X, C) | cyan to blue: green falling |
| 4 | 4–5 | (X, 0, C) | blue to magenta: red rising |
| 5 | 5–6 | (C, 0, X) | magenta to red: blue falling |

**Step 3: m.** So far, the smallest channel is 0. But it should be `min`:

> m = V − C (this is max − (max − min) = min)

**Step 4: add m** to all three channels.

🔢 **Maths: HSV (100°, 0.75, 0.784) → RGB** (the leafy green, back again)

> 1. C = 0.784 × 0.75 = 0.588
> 2. hp = 100 ÷ 60 = 1.667 → sector 1
>    hp mod 2 = 1.667, minus 1 = 0.667, |0.667| = 0.667
>    X = 0.588 × (1 − 0.667) = 0.588 × 0.333 = 0.196
>    sector 1 → (X, C, 0) = (0.196, 0.588, 0)
> 3. m = 0.784 − 0.588 = 0.196
> 4. (0.196 + 0.196, 0.588 + 0.196, 0 + 0.196) = **(0.392, 0.784, 0.196)** ✓

That is (100, 200, 50) again. The round trip works.

🔢 **Maths: HSV (240°, 0.5, 1)**

> C = 1 × 0.5 = 0.5
> hp = 4 → sector 4 → (X, 0, C)
> hp mod 2 = 0 → |0 − 1| = 1 → X = 0.5 × (1 − 1) = 0
> (0, 0, 0.5)
> m = 1 − 0.5 = 0.5
> result = (0.5, 0.5, 1.0) → **(128, 128, 255)**, a light blue

🧠 **Remember:** HSV → RGB: **C = V × S**, find the sector from **H ÷ 60**, **X** is the middle channel, then add **m = V − C** to everything.

---

## 16.6 HSL: lightness instead of value

📖 **New word: lightness** — in HSL: how light a colour is, from black (0), through the **pure** colour (0.5), to **white** (1).

HSV has one odd feature: **white** and **pure red** both have V = 1. "Value 1" does not mean "very light". HSL fixes this with a different third number:

> **L = (max + min) ÷ 2** — the middle point between the strongest and weakest channel

And saturation is measured **relative to how much room there is** at that lightness:

> **S = chroma ÷ (1 − |2L − 1|)** (and S = 0 when chroma = 0)

| L | 1 − \|2L − 1\| | Meaning |
|---|---|---|
| 0 (black) | 0 | no room for any colour |
| 0.25 | 0.5 | |
| 0.5 | 1 | the most room: pure colours live here |
| 0.75 | 0.5 | |
| 1 (white) | 0 | no room for any colour |

A picture of HSL is a **double cone**: black at the bottom point, white at the top point, and the pure colours around the wide middle.

```
                   ● white (L = 1)
                  ╱ ╲
                 ╱   ╲
                ╱     ╲
  pure colours ●───────● (L = 0.5, S = 1)
                ╲     ╱
                 ╲   ╱
                  ╲ ╱
                   ● black (L = 0)
```

🔢 **Maths: orange (1.0, 0.502, 0.0) in HSL**

> max = 1, min = 0
> L = (1 + 0) ÷ 2 = **0.5**
> chroma = 1 → S = 1 ÷ (1 − |1 − 1|) = 1 ÷ 1 = **1**
> H = 30.1° (the hue is computed the same way)
> **HSL = (30.1°, 1, 0.5)** — a pure orange, at the middle lightness

🔢 **Maths: pink (1.0, 0.753, 0.796) in HSL**

> L = (1 + 0.753) ÷ 2 = **0.876**
> |2L − 1| = |1.753 − 1| = 0.753 → 1 − 0.753 = 0.247
> chroma = 0.247 → S = 0.247 ÷ 0.247 = **1**
> **HSL = (349.5°, 1, 0.876)**

Look at this! In **HSV**, pink has S = 0.247 ("weak colour"). In **HSL**, pink has S = 1 ("as colourful as it can be **at this lightness**"). Both are true — they measure saturation differently. Pink is very light, and at that lightness there is very little room for colour, and pink uses all of it.

### From HSL back to RGB

The same four steps as HSV, with a different C and m:

> C = (1 − |2L − 1|) × S
> m = L − C ÷ 2

🔢 **Maths: HSL (240°, 1, 0.75)**

> C = (1 − |1.5 − 1|) × 1 = (1 − 0.5) × 1 = 0.5
> sector 4, X = 0 → (0, 0, 0.5)
> m = 0.75 − 0.25 = 0.5
> result = (0.5, 0.5, 1.0) → **(128, 128, 255)**

It is the **same** light blue as HSV (240°, 0.5, 1) in Section 16.5 — one colour, two different names.

### Which one to use?

| Model | Good for | Example |
|---|---|---|
| **HSV** | "the colour, then how dark" | colour pickers in paint programs; making a colour darker by lowering V |
| **HSL** | "the colour, then how light or dark around it" | web design (CSS has `hsl()`); making tints (toward white) and shades (toward black) with one slider |

---

## 16.7 Shifting the hue

📖 **New word: hue shift** — turning every hue in a picture by the same angle.

With HSV, some changes that are hard in RGB become **one line**:

| Change | In HSV |
|---|---|
| shift every colour round the wheel | H = H + angle (then wrap) |
| make colours more grey | S = S × 0.5 |
| make the image darker | V = V × 0.7 |

🔢 **Maths: shift red by 120°**

> red: HSV (0°, 1, 1)
> H = 0 + 120 = 120°
> HSV (120°, 1, 1) → green (0, 1, 0)

So a +120° shift turns: red → green, green → blue, blue → red, yellow → cyan, cyan → magenta, magenta → yellow (300 + 120 = 420 → wrap → 60). Our `bars_shifted.ppm` shows it.

---

## 16.8 What HSV and HSL cannot do

HSV and HSL are useful, but they are **simple maths on RGB**, not models of the eye. In Chapter 15 we learned that the eye sees green as much brighter than blue. HSV and HSL ignore this:

> yellow HSV (60°, 1, 1): luma 237
> blue HSV (240°, 1, 1): luma 18

Both have V = 1, but yellow looks **13 times** brighter. The same is true for HSL: pure yellow and pure blue both have L = 0.5.

So "same V" or "same L" does **not** mean "looks equally bright". There are better colour models built from eye measurements (often called **perceptual colour spaces**), but they need more maths than this book has room for. For picking and changing colours by hand, HSV and HSL are good enough, and that is how they are used.

⚠️ **Careful:** Do not use "V" or "L" to make a grey image. Use luma (Chapter 15).

---

## Code, part 1: `hsv.h`

File: `common/hsv.h` (new). It includes `colourf.h`.

```cpp
#ifndef HSV_H
#define HSV_H

#include <algorithm>
#include <cmath>
#include "colourf.h"

struct HSV {
    double h = 0.0;
    double s = 0.0;
    double v = 0.0;
};

struct HSL {
    double h = 0.0;
    double s = 0.0;
    double l = 0.0;
};

inline double wrapHue(double h) {
    h = std::fmod(h, 360.0);
    if (h < 0.0) {
        h += 360.0;
    }
    return h;
}

inline double hueOf(ColourF c) {
    double maxC = std::max({c.r, c.g, c.b});
    double minC = std::min({c.r, c.g, c.b});
    double delta = maxC - minC;
    if (delta == 0.0) {
        return 0.0;
    }
    double h = 0.0;
    if (maxC == c.r) {
        h = 60.0 * ((c.g - c.b) / delta);
    } else if (maxC == c.g) {
        h = 60.0 * ((c.b - c.r) / delta + 2.0);
    } else {
        h = 60.0 * ((c.r - c.g) / delta + 4.0);
    }
    return wrapHue(h);
}

inline HSV rgbToHsv(ColourF c) {
    double maxC = std::max({c.r, c.g, c.b});
    double minC = std::min({c.r, c.g, c.b});
    HSV result;
    result.h = hueOf(c);
    result.v = maxC;
    result.s = (maxC == 0.0) ? 0.0 : (maxC - minC) / maxC;
    return result;
}

inline HSL rgbToHsl(ColourF c) {
    double maxC = std::max({c.r, c.g, c.b});
    double minC = std::min({c.r, c.g, c.b});
    double delta = maxC - minC;
    HSL result;
    result.h = hueOf(c);
    result.l = (maxC + minC) / 2.0;
    result.s = (delta == 0.0) ? 0.0 : delta / (1.0 - std::fabs(2.0 * result.l - 1.0));
    return result;
}

inline ColourF hueToRgb(double h, double c) {
    double hp = wrapHue(h) / 60.0;
    double x = c * (1.0 - std::fabs(std::fmod(hp, 2.0) - 1.0));
    if (hp < 1.0) {
        return ColourF{c, x, 0.0};
    }
    if (hp < 2.0) {
        return ColourF{x, c, 0.0};
    }
    if (hp < 3.0) {
        return ColourF{0.0, c, x};
    }
    if (hp < 4.0) {
        return ColourF{0.0, x, c};
    }
    if (hp < 5.0) {
        return ColourF{x, 0.0, c};
    }
    return ColourF{c, 0.0, x};
}

inline ColourF hsvToRgb(HSV hsv) {
    double c = hsv.v * hsv.s;
    double m = hsv.v - c;
    return hueToRgb(hsv.h, c) + ColourF{m, m, m};
}

inline ColourF hslToRgb(HSL hsl) {
    double c = (1.0 - std::fabs(2.0 * hsl.l - 1.0)) * hsl.s;
    double m = hsl.l - c / 2.0;
    return hueToRgb(hsl.h, c) + ColourF{m, m, m};
}

inline Colour shiftHue(Colour c, double degrees) {
    HSV hsv = rgbToHsv(toColourF(c));
    hsv.h = wrapHue(hsv.h + degrees);
    return toColour(hsvToRgb(hsv));
}

#endif
```

### Line by line

**Types and wrapping (lines 1–26)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef HSV_H` / `#define HSV_H` | Include guard. |
| 4 | `#include <algorithm>` | `std::max` and `std::min`. |
| 5 | `#include <cmath>` | `std::fmod` (remainder for `double`) and `std::fabs` (drop the minus sign of a `double`). |
| 6 | `#include "colourf.h"` | `ColourF` and its operators (Chapter 14). |
| 8–12 | `struct HSV { double h = 0.0; double s = 0.0; double v = 0.0; };` | A colour in HSV. h is in degrees (0–360), s and v from 0 to 1. |
| 14–18 | `struct HSL { double h = 0.0; double s = 0.0; double l = 0.0; };` | A colour in HSL. Same idea, with lightness l. |
| 20 | `inline double wrapHue(double h) {` | Put any angle into 0–360 (Section 16.2). |
| 21 | `h = std::fmod(h, 360.0);` | The remainder after dividing by 360. For 370 → 10. For −30 → −30 (still negative!). |
| 22–24 | `if (h < 0.0) { h += 360.0; }` | Fix negative remainders: −30 → 330. |
| 25 | `return h;` | Now 0 ≤ h < 360. |
| 26 | `}` | End. |

**Finding the hue (lines 28–44)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 28 | `inline double hueOf(ColourF c) {` | The hue of a colour, in degrees (Section 16.4). Both HSV and HSL use it. |
| 29 | `double maxC = std::max({c.r, c.g, c.b});` | The biggest channel. The `{ }` braces let `std::max` compare **three** values at once. |
| 30 | `double minC = std::min({c.r, c.g, c.b});` | The smallest channel. |
| 31 | `double delta = maxC - minC;` | The chroma (Section 16.4). |
| 32–34 | `if (delta == 0.0) { return 0.0; }` | A grey has no hue. Return 0 (and avoid dividing by zero below). |
| 35 | `double h = 0.0;` | The hue we will compute. |
| 36–37 | `if (maxC == c.r) { h = 60.0 * ((c.g - c.b) / delta); }` | Red is biggest: the hue is near 0°, leaning toward yellow or magenta. |
| 38–39 | `} else if (maxC == c.g) { h = 60.0 * ((c.b - c.r) / delta + 2.0); }` | Green is biggest: the hue is near 120°. |
| 40–42 | `} else { h = 60.0 * ((c.r - c.g) / delta + 4.0); }` | Blue is biggest: the hue is near 240°. |
| 43 | `return wrapHue(h);` | The red case can be negative (like −10.5 for pink), so wrap it. |
| 44 | `}` | End. |

Comparing two `double`s with `==` is usually risky (Chapter 13's tiny rounding errors). Here it is safe: `maxC` is not computed — it **is** one of the three values, copied exactly.

**RGB → HSV and HSL (lines 46–65)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 46 | `inline HSV rgbToHsv(ColourF c) {` | Convert RGB (0–1) to HSV. |
| 47–48 | `double maxC = ...; double minC = ...;` | Biggest and smallest channel. |
| 49 | `HSV result;` | Starts as (0, 0, 0). |
| 50 | `result.h = hueOf(c);` | The hue. |
| 51 | `result.v = maxC;` | V = max (Section 16.3). |
| 52 | `result.s = (maxC == 0.0) ? 0.0 : (maxC - minC) / maxC;` | S = (max − min) ÷ max. For black (max = 0) we use 0, to avoid dividing by zero. |
| 53–54 | `return result;` `}` | Done. |
| 56 | `inline HSL rgbToHsl(ColourF c) {` | Convert RGB to HSL (Section 16.6). |
| 57–59 | `double maxC = ...; double minC = ...; double delta = maxC - minC;` | Biggest, smallest, chroma. |
| 60 | `HSL result;` | Starts as (0, 0, 0). |
| 61 | `result.h = hueOf(c);` | Same hue as HSV. |
| 62 | `result.l = (maxC + minC) / 2.0;` | L = the middle of max and min. |
| 63 | `result.s = (delta == 0.0) ? 0.0 : delta / (1.0 - std::fabs(2.0 * result.l - 1.0));` | S = chroma ÷ the room available at this lightness. For greys (chroma 0) we use 0. When chroma is not 0, L is never exactly 0 or 1, so the room is never 0. |
| 64–65 | `return result;` `}` | Done. |

**HSV and HSL → RGB (lines 67–98)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 67 | `inline ColourF hueToRgb(double h, double c) {` | Steps 2 of Section 16.5: a hue and a chroma → (r, g, b) with the smallest channel at 0. Both HSV and HSL use it. |
| 68 | `double hp = wrapHue(h) / 60.0;` | The hue in "sectors": 0 to 6. |
| 69 | `double x = c * (1.0 - std::fabs(std::fmod(hp, 2.0) - 1.0));` | The middle channel X: the "tent" formula. |
| 70–72 | `if (hp < 1.0) { return ColourF{c, x, 0.0}; }` | Sector 0: red to yellow. |
| 73–75 | `if (hp < 2.0) { return ColourF{x, c, 0.0}; }` | Sector 1: yellow to green. |
| 76–78 | `if (hp < 3.0) { return ColourF{0.0, c, x}; }` | Sector 2: green to cyan. |
| 79–81 | `if (hp < 4.0) { return ColourF{0.0, x, c}; }` | Sector 3: cyan to blue. |
| 82–84 | `if (hp < 5.0) { return ColourF{x, 0.0, c}; }` | Sector 4: blue to magenta. |
| 85 | `return ColourF{c, 0.0, x};` | Sector 5: magenta to red. |
| 86 | `}` | End. |
| 88 | `inline ColourF hsvToRgb(HSV hsv) {` | HSV → RGB. |
| 89 | `double c = hsv.v * hsv.s;` | Step 1: chroma = V × S. |
| 90 | `double m = hsv.v - c;` | Step 3: m = V − C. |
| 91 | `return hueToRgb(hsv.h, c) + ColourF{m, m, m};` | Steps 2 and 4: the sector colour, plus m on every channel. |
| 92 | `}` | End. |
| 94 | `inline ColourF hslToRgb(HSL hsl) {` | HSL → RGB. |
| 95 | `double c = (1.0 - std::fabs(2.0 * hsl.l - 1.0)) * hsl.s;` | Chroma = room × S. |
| 96 | `double m = hsl.l - c / 2.0;` | m = L − C ÷ 2. |
| 97 | `return hueToRgb(hsl.h, c) + ColourF{m, m, m};` | The same steps 2 and 4. |
| 98 | `}` | End. |

**Hue shift (lines 100–106)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 100 | `inline Colour shiftHue(Colour c, double degrees) {` | Turn a colour round the wheel (Section 16.7). |
| 101 | `HSV hsv = rgbToHsv(toColourF(c));` | Bytes → 0–1 → HSV. |
| 102 | `hsv.h = wrapHue(hsv.h + degrees);` | Add the angle, and wrap. |
| 103 | `return toColour(hsvToRgb(hsv));` | HSV → 0–1 → bytes (with clamping and rounding). |
| 104 | `}` | End. |
| 106 | `#endif` | End of the include guard. |

---

## Code, part 2: colour pickers and hue shifts

File: `ch16/hsv_hsl.cpp`

```cpp
#include <cmath>
#include <iostream>
#include <string>
#include "hsv.h"

double roundTo(double v, double factor) {
    return std::floor(v * factor + 0.5) / factor;
}

void describe(const std::string& name, Colour c) {
    HSV hsv = rgbToHsv(toColourF(c));
    HSL hsl = rgbToHsl(toColourF(c));
    std::cout << name << ": HSV (" << roundTo(hsv.h, 10) << ", " << roundTo(hsv.s, 1000)
              << ", " << roundTo(hsv.v, 1000) << ")   HSL (" << roundTo(hsl.h, 10) << ", "
              << roundTo(hsl.s, 1000) << ", " << roundTo(hsl.l, 1000) << ")\n";
}

void printColour(const std::string& label, Colour c) {
    std::cout << label << " = (" << static_cast<int>(c.r) << ", "
              << static_cast<int>(c.g) << ", " << static_cast<int>(c.b) << ")\n";
}

int main() {
    describe("orange", Colour{255, 128, 0});
    describe("pink  ", Colour{255, 192, 203});
    describe("grey  ", Colour{128, 128, 128});
    printColour("HSV (120, 1, 1)  ", toColour(hsvToRgb(HSV{120.0, 1.0, 1.0})));
    printColour("HSV (240, 0.5, 1)", toColour(hsvToRgb(HSV{240.0, 0.5, 1.0})));
    printColour("HSL (240, 1, 0.75)", toColour(hslToRgb(HSL{240.0, 1.0, 0.75})));
    printColour("red shifted by 120", shiftHue(colours::red, 120.0));

    Image strip(360, 40);
    for (int y = 0; y < strip.height(); ++y) {
        for (int x = 0; x < strip.width(); ++x) {
            strip.setPixel(x, y, toColour(hsvToRgb(HSV{static_cast<double>(x), 1.0, 1.0})));
        }
    }

    Image picker(256, 256);
    for (int y = 0; y < picker.height(); ++y) {
        for (int x = 0; x < picker.width(); ++x) {
            double s = x / 255.0;
            double v = 1.0 - y / 255.0;
            picker.setPixel(x, y, toColour(hsvToRgb(HSV{210.0, s, v})));
        }
    }

    Image lightness(360, 120);
    for (int y = 0; y < lightness.height(); ++y) {
        double l = 0.25 * (y / 40 + 1);
        for (int x = 0; x < lightness.width(); ++x) {
            HSL hsl{static_cast<double>(x), 1.0, l};
            lightness.setPixel(x, y, toColour(hslToRgb(hsl)));
        }
    }

    const Colour barColours[6] = {colours::red, colours::green, colours::blue,
                                  colours::yellow, colours::cyan, colours::magenta};
    Image shifted(360, 80);
    for (int y = 0; y < shifted.height(); ++y) {
        for (int x = 0; x < shifted.width(); ++x) {
            shifted.setPixel(x, y, shiftHue(barColours[x / 60], 120.0));
        }
    }

    bool ok = strip.savePPM("hue_strip.ppm");
    ok = ok && picker.savePPM("picker.ppm");
    ok = ok && lightness.savePPM("lightness.ppm");
    ok = ok && shifted.savePPM("bars_shifted.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    return 0;
}
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–3 | `#include <cmath>` / `<iostream>` / `<string>` | `std::floor`, printing, and names. |
| 4 | `#include "hsv.h"` | Our new header (and through it `colourf.h` and `image.h`). |
| 6 | `double roundTo(double v, double factor) {` | Round to a number of decimal places, so the output is short. `factor` 10 → 1 decimal place, 1000 → 3 places. |
| 7 | `return std::floor(v * factor + 0.5) / factor;` | 30.1176 × 10 = 301.176 → + 0.5 → floor → 301 → ÷ 10 → 30.1. The Chapter 13 rounding, shifted by a factor. |
| 8 | `}` | End. |
| 10 | `void describe(const std::string& name, Colour c) {` | Print a colour in both HSV and HSL. |
| 11–12 | `HSV hsv = rgbToHsv(toColourF(c));` / `HSL hsl = rgbToHsl(toColourF(c));` | Convert it both ways. |
| 13–15 | `std::cout << name << ": HSV (" << roundTo(hsv.h, 10) ...` | Print h with 1 decimal place, s, v and l with 3. |
| 16 | `}` | End. |
| 18–21 | `void printColour(...) { ... }` | Print an RGB colour as numbers (as in earlier chapters). |
| 23 | `int main() {` | The program starts here. |
| 24–26 | `describe("orange", ...); describe("pink  ", ...); describe("grey  ", ...);` | The worked examples from Sections 16.4 and 16.6, and a grey. |
| 27 | `printColour("HSV (120, 1, 1)  ", toColour(hsvToRgb(HSV{120.0, 1.0, 1.0})));` | Hue 120°, full S and V: expect pure green. |
| 28 | `printColour("HSV (240, 0.5, 1)", ...);` | Section 16.5's light blue. |
| 29 | `printColour("HSL (240, 1, 0.75)", ...);` | Section 16.6: the same light blue, named in HSL. |
| 30 | `printColour("red shifted by 120", shiftHue(colours::red, 120.0));` | Section 16.7: expect green. |
| 32 | `Image strip(360, 40);` | One column per degree of hue. |
| 33–34 | `for (int y ...) { for (int x ...) {` | Every pixel. |
| 35 | `strip.setPixel(x, y, toColour(hsvToRgb(HSV{static_cast<double>(x), 1.0, 1.0})));` | Hue = x degrees, full saturation and value: the whole colour wheel, unrolled. |
| 36–37 | `}` `}` | End of the loops. |
| 39 | `Image picker(256, 256);` | A colour-picker square, like in paint programs. |
| 40–41 | `for (int y ...) { for (int x ...) {` | Every pixel. |
| 42 | `double s = x / 255.0;` | Saturation grows to the **right**: 0 on the left, 1 on the right. |
| 43 | `double v = 1.0 - y / 255.0;` | Value grows **upward**: 1 at the top, 0 at the bottom (a flip, like Chapter 3's "maths y"). |
| 44 | `picker.setPixel(x, y, toColour(hsvToRgb(HSV{210.0, s, v})));` | One fixed hue (210°, a sky blue) with every S and V. |
| 45–46 | `}` `}` | End of the loops. |
| 48 | `Image lightness(360, 120);` | Three bands of 40 rows. |
| 49 | `for (int y = 0; y < lightness.height(); ++y) {` | For each row… |
| 50 | `double l = 0.25 * (y / 40 + 1);` | `y / 40` is the band number 0, 1, 2 (integer division). So L = 0.25, 0.5, 0.75. |
| 51 | `for (int x = 0; x < lightness.width(); ++x) {` | Across the row… |
| 52 | `HSL hsl{static_cast<double>(x), 1.0, l};` | hue = x, full saturation, this band's lightness. |
| 53 | `lightness.setPixel(x, y, toColour(hslToRgb(hsl)));` | Convert and store. |
| 54–55 | `}` `}` | End of the loops. |
| 57–58 | `const Colour barColours[6] = {...};` | The six test bars from Chapter 15. |
| 59 | `Image shifted(360, 80);` | The same size as Chapter 15's bars. |
| 60–61 | `for (int y ...) { for (int x ...) {` | Every pixel. |
| 62 | `shifted.setPixel(x, y, shiftHue(barColours[x / 60], 120.0));` | Each bar's colour, turned 120° round the wheel. |
| 63–64 | `}` `}` | End of the loops. |
| 66–73 | `bool ok = strip.savePPM(...); ... if (!ok) { ...; return 1; }` | Save the four images. |
| 74 | `return 0;` | The program finished with no problem. |
| 75 | `}` | End of `main`. |

Compile:

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common hsv_hsl.cpp -o hsv_hsl
```

### What you should see

```
orange: HSV (30.1, 1, 1)   HSL (30.1, 1, 0.5)
pink  : HSV (349.5, 0.247, 1)   HSL (349.5, 1, 0.876)
grey  : HSV (0, 0, 0.502)   HSL (0, 0, 0.502)
HSV (120, 1, 1)   = (0, 255, 0)
HSV (240, 0.5, 1) = (128, 128, 255)
HSL (240, 1, 0.75) = (128, 128, 255)
red shifted by 120 = (0, 255, 0)
```

These match Sections 16.4 to 16.7. The grey has hue 0 and saturation 0 in both models: with no colour, the hue does not matter.

Open the images:
- `hue_strip.ppm`: the full wheel, from red through yellow, green, cyan, blue, magenta, and **back to red** at the right edge. (Compare with Chapter 13's rainbow, which **stopped** at magenta.)
- `picker.ppm`: white at the top-left, pure sky blue (0, 128, 255) at the top-right, and black along the whole bottom. This is the square you see in almost every colour picker.
- `lightness.ppm`: three hue strips — dark (L = 0.25), pure (L = 0.5) and pale (L = 0.75).
- `bars_shifted.ppm`: green, blue, red, cyan, magenta, yellow — every bar of Chapter 15 turned 120°.

---

## Small examples

### Example 1 — The question from Section 16.1

"(200, 120, 40): make it a bit more yellow and a little paler."

> (200, 120, 40) = (0.784, 0.471, 0.157)
> max = 0.784 (red), min = 0.157, chroma = 0.627
> H = 60 × (0.471 − 0.157) ÷ 0.627 = 60 × 0.5 = **30°**
> HSL: L = (0.784 + 0.157) ÷ 2 = 0.471, S = 0.627 ÷ (1 − |0.941 − 1|) = 0.627 ÷ 0.941 = 0.667

"More yellow" → H = 40°. "Paler" → L = 0.6. Then convert back:

> C = (1 − |1.2 − 1|) × 0.667 = 0.8 × 0.667 = 0.533
> hp = 40 ÷ 60 = 0.667 → sector 0 → (C, X, 0)
> X = 0.533 × (1 − |0.667 − 1|) = 0.533 × 0.667 = 0.356
> m = 0.6 − 0.533 ÷ 2 = 0.6 − 0.267 = 0.333
> RGB = (0.533 + 0.333, 0.356 + 0.333, 0 + 0.333) = (0.867, 0.689, 0.333) → **(221, 176, 85)**

Two simple changes in HSL. Doing the same in RGB would have been guesswork.

### Example 2 — Evenly spaced colours

To get 5 clearly different colours (for example, for 5 lines on a chart), space the hues evenly:

```cpp
for (int i = 0; i < 5; ++i) {
    double h = i * 360.0 / 5;     // 0, 72, 144, 216, 288
    Colour c = toColour(hsvToRgb(HSV{h, 0.8, 0.9}));
}
```

> 360 ÷ 5 = 72° apart: red (0°), yellow-green (72°), green (144°), light blue (216°), purple (288°).

### Example 3 — Tints and shades with HSL

A **tint** is a colour mixed with white. A **shade** is a colour mixed with black. With HSL, both are the same slider:

> pure blue: HSL (240°, 1, 0.5)
> shade: L = 0.25 → (0, 0, 128) navy
> tint: L = 0.75 → (128, 128, 255) light blue

### Example 4 — Darken without changing the hue

To make a picture 30% darker but keep every hue and saturation: V = V × 0.7.

> orange HSV (30.1°, 1, 1) → (30.1°, 1, 0.7)
> C = 0.7, X = 0.7 × 0.502 = 0.351, m = 0
> (0.7, 0.351, 0) → **(179, 90, 0)**

This is the same as multiplying the RGB by 0.7 (Chapter 14). For **V**, HSV and plain scaling agree — but for hue and saturation changes, HSV is much easier.

---

## Common mistakes

⚠️ **Forgetting to wrap the hue.** A hue of −10.5 or 420 gives nonsense in `hueToRgb` (it would pick no sector, or the wrong one). Always wrap.

⚠️ **`fmod` with negative numbers.** `std::fmod(-30, 360)` is −30, not 330. Add 360 when the result is negative.

⚠️ **Dividing by zero for greys and black.** chroma = 0 or max = 0 must be handled first.

⚠️ **Mixing HSV saturation and HSL saturation.** Pink has S = 0.247 in HSV and S = 1 in HSL. Know which model you are in.

⚠️ **Hue in 0–1 instead of 0–360.** Some programs store hue as 0–1 (a fraction of a turn). Ours uses degrees. Multiply by 360 if you get a 0–1 hue from somewhere else.

⚠️ **Thinking same V means same brightness.** Yellow and blue at V = 1 look very different. Use luma for brightness.

---

## Practice

🏋️ **1.** What is the hue (in degrees) of: cyan, (255, 0, 128), and (64, 64, 64)?

🏋️ **2.** Wrap these hues: 400°, −90°, 720°, 359°.

🏋️ **3.** Convert (0, 128, 255) to HSV. Show every step.

🏋️ **4.** Convert HSV (300°, 1, 0.5) to RGB bytes.

🏋️ **5.** Convert (255, 255, 128) to HSL. Then convert HSL (60°, 1, 0.75) back to RGB. Do you get the same colour?

🏋️ **6.** Shift the hue of orange (255, 128, 0) by 180°. What colour do you get? Compare it with the complement from Chapter 5, (0, 127, 255).

🏋️ **7.** Make a picker image for HSL instead of HSV: x → S from 0 to 1, y → L from 1 (top) to 0 (bottom), hue 30°. What do the top edge and bottom edge look like?

---

## Answers

**1.**
> cyan (0, 1, 1): max = 1 (green and blue are equal; the code checks red first, then green, so green "wins") → H = 60 × ((1 − 0) ÷ 1 + 2) = 60 × 3 = **180°** ✓
> (255, 0, 128) = (1, 0, 0.502): red biggest → H = 60 × (0 − 0.502) ÷ 1 = −30.1 → wrap → **329.9°** (a pink-red, near magenta)
> (64, 64, 64): chroma = 0 → **no hue** (0)

**2.**
> 400 → **40**
> −90 → −90 + 360 = **270**
> 720 → **0**
> 359 → **359**

**3.**
> (0, 128, 255) = (0, 0.502, 1)
> max = 1 (blue), min = 0, chroma = 1
> H = 60 × ((0 − 0.502) ÷ 1 + 4) = 60 × 3.498 = **209.9°**
> V = **1**, S = 1 ÷ 1 = **1**
> HSV = **(209.9°, 1, 1)** — the top-right corner of our picker (hue 210°) ✓

**4.**
> C = 0.5 × 1 = 0.5
> hp = 5 → sector 5 → (C, 0, X), X = 0.5 × (1 − |5 mod 2 − 1|) = 0.5 × (1 − 0) = 0.5
> (0.5, 0, 0.5), m = 0.5 − 0.5 = 0
> → **(128, 0, 128)**, a purple (dark magenta)

**5.**
> (1, 1, 0.502): max = 1, min = 0.502, chroma = 0.498
> red and green are equal; red is checked first → H = 60 × (1 − 0.502) ÷ 0.498 = 60 × 1 = **60°**
> L = (1 + 0.502) ÷ 2 = **0.751**, S = 0.498 ÷ (1 − |1.502 − 1|) = 0.498 ÷ 0.498 = **1**
> back from (60°, 1, 0.75): C = 0.5 × 1 = 0.5, hp = 1 → sector 1 → (X, C, 0), X = 0.5 × (1 − |1 − 1|) = 0.5
> (0.5, 0.5, 0), m = 0.75 − 0.25 = 0.5 → (1, 1, 0.5) → **(255, 255, 128)** ✓ the same colour (L 0.751 vs 0.75 is a rounding difference that disappears in the bytes)

**6.**
> orange HSV (30.1°, 1, 1) → H = 210.1°
> C = 1, hp = 3.502 → sector 3 → (0, X, C), X = 1 × (1 − |1.502 − 1|) = 0.498
> → (0, 0.498, 1) → **(0, 127, 255)**

It is **exactly** the complement from Chapter 5! For pure colours (S = 1, V = 1), the opposite side of the wheel and the complement (255 − each channel) are the same thing.

**7.**

```cpp
Image hslPicker(256, 256);
for (int y = 0; y < 256; ++y) {
    for (int x = 0; x < 256; ++x) {
        HSL hsl{30.0, x / 255.0, 1.0 - y / 255.0};
        hslPicker.setPixel(x, y, toColour(hslToRgb(hsl)));
    }
}
```

The **top edge** (L = 1) is all **white**, and the **bottom edge** (L = 0) is all **black**, for every saturation. The pure orange is in the **middle** of the right edge (L = 0.5, S = 1). This is the "double cone" of Section 16.6, cut in half.

---

## Summary

🧠 People think in **hue**, **saturation** and **brightness**. HSV and HSL give us those as numbers.

🧠 **Hue** is an angle on the colour wheel, 0–360°: red 0°, yellow 60°, green 120°, cyan 180°, blue 240°, magenta 300°. Always **wrap** it.

🧠 **HSV**: V = max, S = (max − min) ÷ max. Hue from which channel is biggest.

🧠 HSV → RGB: C = V × S, sector = H ÷ 60, X = the middle channel, then add m = V − C.

🧠 **HSL**: L = (max + min) ÷ 2, S = chroma ÷ (1 − |2L − 1|). Black at L = 0, pure colours at 0.5, white at 1.

🧠 **Hue shift**: H + angle. A 180° shift of a pure colour gives its complement.

🧠 HSV and HSL ignore the eye's sensitivity. Same V or L does **not** mean the same brightness.

---

## Next chapter

We have said it three times now: "128 is not half as bright as 255". In Chapter 17 we finally find out why. We learn about **gamma** and the **sRGB** standard: how screens turn bytes into light, why images are stored this way, and how to do colour maths **correctly** in "linear light" — including true **luminance**.
