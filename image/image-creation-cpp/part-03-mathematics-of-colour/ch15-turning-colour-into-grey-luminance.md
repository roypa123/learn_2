# Chapter 15 — Turning Colour into Grey: Luminance

> **Part 3 · Chapter 15 of 82**
> **You need:** Chapters 1–14 · **You will make:** `grey.h` (grey conversion and PGM saving), `bars.ppm`, `bars_average.ppm`, `bars_luma.pgm` and `desaturate.ppm`

---

## What you will learn

- Why the **plain average** (R + G + B) ÷ 3 makes a bad grey picture.
- Why our eyes see **green as bright** and **blue as dark**, even at the same power.
- The **luma** formula: **0.2126 R + 0.7152 G + 0.0722 B**, and where the numbers come from.
- The difference between **luminance** and **luma** (and why Chapter 17 matters).
- How to turn a whole image into grey and save it as a real **PGM** file.
- How to make a colour **less colourful** step by step (**desaturation**).

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **brightness** (perceived) | How bright a colour **looks** to a person. |
| **sensitivity** | How strongly the eye reacts to light of one colour. |
| **weight** | A number that says how much one part counts in a total. |
| **weighted average** | An average where some parts count more than others. |
| **luminance** | The true amount of light a colour gives, measured the way the eye feels it. |
| **luma** | A quick version of luminance, computed straight from normal RGB bytes. |
| **saturation** | How strong or "pure" a colour is. Grey has no saturation. |
| **desaturate** | To make a colour less strong, moving it toward grey. |

---

## 15.1 A first try: the plain average

To turn a colour into grey, we need **one** number for each pixel (Chapter 10, PGM). The first idea that comes to mind is the average of the three channels:

> grey = (R + G + B) ÷ 3

🔢 **Maths: the plain average of red, green and blue**

> red (255, 0, 0): (255 + 0 + 0) ÷ 3 = **85**
> green (0, 255, 0): (0 + 255 + 0) ÷ 3 = **85**
> blue (0, 0, 255): (0 + 0 + 255) ÷ 3 = **85**

All three become the **same grey**. But look at them on a screen:

```
 ┌────────┬────────┬────────┐
 │  RED   │ GREEN  │  BLUE  │
 │ medium │ BRIGHT │  dark  │   ← how they LOOK to you
 └────────┴────────┴────────┘
```

Pure green looks **very bright**. Pure blue looks **dark**. Red is in between. The plain average says they are equal. So a grey picture made with the average looks wrong: green leaves turn too dark, the blue sky turns too bright.

📖 **New word: brightness** (perceived) — how bright a colour **looks** to a person, not how much power the lamp uses.

---

## 15.2 Why the eye sees green as brighter

📖 **New word: sensitivity** — how strongly the eye reacts to light of one colour.

Remember Chapter 2: the eye has three kinds of cone cells — L ("red"), M ("green") and S ("blue"). They are **not** equal:

- The **green** and **red** cones are many, and their sensitivity curves **overlap** in the green-yellow part of the spectrum. Green light excites **both** of them strongly.
- The **blue** cones are **few** (only a small part of all cones), and they react weakly.

If you measure how bright each wavelength **looks** (at the same power), you get a curve with its peak at about **555 nm** — yellow-green:

```
how bright it looks
     ▲
 1.0 │              ▄█▄
     │            ▄█████▄
     │          ▄█████████▄
 0.5 │        ▄█████████████▄
     │     ▄▄███████████████████▄
     │▄▄▄████████████████████████████▄▄▄
   0 └──┬──────┬──────┬──────┬──────┬──► wavelength (nm)
       400    450    500    555    600    650    700
       blue                green          red
```

So equal **power** does not mean equal **brightness**. For our three screen lights:

| Light | How bright it looks (roughly) |
|---|---|
| green | about **72%** of white |
| red | about **21%** of white |
| blue | only about **7%** of white |

These numbers come from measurements of many people's eyes, made by scientists in the 1920s and 1930s, and are now part of international standards for screens and video.

---

## 15.3 A weighted average

📖 **New word: weight** — a number that says how much one part counts.

📖 **New word: weighted average** — an average where some parts count more than others.

A plain average gives each channel a weight of **1/3** (0.333):

> grey = 0.333 × R + 0.333 × G + 0.333 × B

A **weighted** average uses the eye's real sensitivities as the weights:

> **grey = 0.2126 × R + 0.7152 × G + 0.0722 × B**

🔢 **Maths: the weights add up to 1**

> 0.2126 + 0.7152 + 0.0722 = **1.0000**

This is important. It means **white stays white**:

> white (1, 1, 1): 0.2126 + 0.7152 + 0.0722 = 1.0 → 255 ✓

and **black stays black** (0 × anything = 0). And any grey stays the same grey:

> (0.5, 0.5, 0.5): 0.5 × (0.2126 + 0.7152 + 0.0722) = 0.5 × 1 = 0.5 ✓

A weighted average with weights that add up to 1 is like a lerp with more than two values. It always lands somewhere between the smallest and the biggest input.

🔢 **Maths: the three primaries, with weights** (using 0.0–1.0 values, then × 255)

> red (1, 0, 0): 0.2126 × 1 = 0.2126 → 0.2126 × 255 = 54.2 → **54**
> green (0, 1, 0): 0.7152 → 182.4 → **182**
> blue (0, 0, 1): 0.0722 → 18.4 → **18**

Now green is a light grey, red a dark grey, and blue almost black. That matches what our eyes see.

🔢 **Maths: orange (255, 128, 0)**

> as 0–1: (1.0, 0.502, 0.0)
> 0.2126 × 1.0 = 0.2126
> 0.7152 × 0.502 = 0.3590
> 0.0722 × 0.0 = 0
> sum = 0.5716 → × 255 = 145.8 → **146**

With the plain average: (255 + 128 + 0) ÷ 3 = 127.7 → 128. So orange looks a bit **brighter** than the average says, because it has a lot of green in it.

🧠 **Remember:** **grey = 0.2126 R + 0.7152 G + 0.0722 B.** Green counts most, blue least. The weights add up to 1.

---

## 15.4 Another set of weights you will see

You may also find this older formula in books and on the internet:

> grey = 0.299 × R + 0.587 × G + 0.114 × B

These weights come from the standard for old **TV** colour (called **Rec. 601**, from 1982). Our weights come from the standard for **HD** video and today's computer screens (called **Rec. 709**, from 1990, which uses the same colours as sRGB — Chapter 17).

| Standard | Red | Green | Blue | Used for |
|---|---|---|---|---|
| Rec. 601 | 0.299 | 0.587 | 0.114 | old TV, JPEG files |
| **Rec. 709** | **0.2126** | **0.7152** | **0.0722** | HD video, sRGB screens — **we use this** |

Both add up to 1. Both give much better results than the plain average. They differ because the **red, green and blue lights** of old TVs were slightly different colours from the lights of today's screens.

🔢 **Maths: orange with Rec. 601**

> 0.299 × 1.0 + 0.587 × 0.502 + 0.114 × 0 = 0.299 + 0.2947 = 0.5937 → × 255 = 151.4 → **151**

151 (Rec. 601) vs. 146 (Rec. 709). Close, but not the same.

---

## 15.5 Luminance and luma

📖 **New word: luminance** — the true amount of light a colour gives, measured the way the eye feels it.

📖 **New word: luma** — a quick version of luminance, computed straight from normal RGB bytes.

There is one more detail. Remember Chapter 5, Section 5.5: the byte value 128 does **not** give half as much light as 255. It gives only about **22%**. The bytes in an image file are **not** proportional to the amount of light. They are "gamma encoded" — Chapter 17 explains exactly how and why.

So there are two ways to use the weights:

| Name | How | Result |
|---|---|---|
| **luma** | apply the weights **directly** to the bytes (0–1 values) | fast, simple, a little inaccurate |
| **luminance** | first turn each byte into the **real** amount of light, **then** apply the weights | correct |

In this chapter we compute **luma**, and we name our function `luma` to be honest about it. It is what most programs do, and it looks good. In Chapter 17, after we learn about gamma, we will compute **true luminance** and compare the two.

⚠️ **Careful:** Many books and programs call the quick version "luminance" too. Now you know the difference.

---

## 15.6 Turning a whole image into grey

For each pixel:

1. Read the colour.
2. Turn it into a `ColourF` (0–1 values, Chapter 14).
3. Compute luma with the weights.
4. Turn it back into a byte (clamp, × 255, round — `toByte` from Chapter 14).

Then we have **one byte per pixel**. We can store it in two ways:

| Way | Result | File size for 360 × 80 |
|---|---|---|
| put it into R, G and B (R = G = B) and save as **PPM** | a colour file that only has greys | 360 × 80 × 3 + header |
| store **one** byte per pixel and save as **PGM P5** (Chapter 10) | a real grey file | 360 × 80 + header |

🔢 **Maths: the two file sizes**

> PPM: header `P6\n360 80\n255\n` = 3 + 7 + 4 = 14 → 14 + 86,400 = **86,414 bytes**
> PGM: header `P5\n360 80\n255\n` = 14 → 14 + 28,800 = **28,814 bytes**

The PGM is **3 times smaller** and holds exactly the same picture. Our new `saveGreyPGM` function does the conversion and saves a PGM in one step. `toGrey` does the R = G = B version, for when you want to keep working on an `Image`.

---

## 15.7 Saturation and desaturation

📖 **New word: saturation** — how strong or "pure" a colour is.

- Pure red (255, 0, 0) has **full** saturation.
- Pink (255, 192, 203) has **less**: it is red mixed with a lot of white.
- Grey has **no** saturation at all.

📖 **New word: desaturate** — to make a colour less strong, by moving it toward grey.

We do **not** have to jump straight from colour to grey. We can go **part of the way**, with a lerp (Chapter 13) between the colour and its own grey:

> grey version = (Y, Y, Y), where Y = luma of the colour
> result = lerp(colour, grey version, amount)

| amount | result |
|---|---|
| 0 | the original colour |
| 0.5 | half way to grey (a soft, "washed-out" colour) |
| 1 | completely grey |

Why lerp toward **its own** grey, and not toward a fixed grey like (128, 128, 128)? Because the colour's own grey has the **same brightness**. So the picture gets less colourful, but not darker or lighter. That is what photo programs do when you move a "saturation" slider down.

🔢 **Maths: orange, half desaturated**

> orange = (1.0, 0.502, 0.0), Y = 0.5716 (Section 15.3)
> grey version = (0.5716, 0.5716, 0.5716)
> R: 1.0 + (0.5716 − 1.0) × 0.5 = 1.0 − 0.2142 = 0.7858 → × 255 = 200.4 → **200**
> G: 0.502 + (0.5716 − 0.502) × 0.5 = 0.502 + 0.0348 = 0.5368 → 136.9 → **137**
> B: 0.0 + (0.5716 − 0.0) × 0.5 = 0.2858 → 72.9 → **73**
> result = **(200, 137, 73)** — a soft, light brown-orange

🔢 **Maths: check the brightness stayed the same**

> luma of the result = 0.2126 × 0.7858 + 0.7152 × 0.5368 + 0.0722 × 0.2858
> = 0.1671 + 0.3839 + 0.0206 = **0.5716** ✓ — exactly the luma of orange

Why does it stay the same? Luma is a **weighted sum**, and a lerp of two colours with the **same** luma has that same luma at every step. The colour moves "sideways" in the RGB cube, toward the grey line, at a constant brightness.

### Going the other way

An amount **below 0** moves **away** from grey — it makes colours **more** saturated. For example, amount −0.5:

> R: 1.0 + (0.5716 − 1.0) × (−0.5) = 1.0 + 0.2142 = 1.2142 → clamped to **255**
> G: 0.502 + 0.0696 × (−0.5) = 0.4672 → **119**
> B: 0.0 + 0.5716 × (−0.5) = −0.2858 → clamped to **0**

This is extrapolation (Chapter 13, Section 13.3). The clamping in `toColour` (Chapter 14) keeps it safe.

---

## Code, part 1: `grey.h`

File: `common/grey.h` (new). It includes `colourf.h`, which includes `image.h` (Chapter 14, Section 14.8).

```cpp
#ifndef GREY_H
#define GREY_H

#include <cstdint>
#include <fstream>
#include <string>
#include <vector>
#include "colourf.h"

inline double luma(ColourF c) {
    return 0.2126 * c.r + 0.7152 * c.g + 0.0722 * c.b;
}

inline double plainAverage(ColourF c) {
    return (c.r + c.g + c.b) / 3.0;
}

inline std::uint8_t greyByte(Colour c) {
    return toByte(luma(toColourF(c)));
}

inline Colour toGrey(Colour c) {
    std::uint8_t v = greyByte(c);
    return Colour{v, v, v};
}

inline Colour desaturate(Colour c, double amount) {
    ColourF f = toColourF(c);
    double y = luma(f);
    ColourF grey{y, y, y};
    return toColour(f + (grey - f) * amount);
}

inline bool saveGreyPGM(const Image& image, const std::string& fileName) {
    std::ofstream file(fileName, std::ios::binary);
    if (!file) {
        return false;
    }
    std::vector<std::uint8_t> grey(image.width() * image.height());
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            grey[y * image.width() + x] = greyByte(image.getPixel(x, y));
        }
    }
    file << "P5\n" << image.width() << " " << image.height() << "\n255\n";
    file.write(reinterpret_cast<const char*>(grey.data()),
               static_cast<std::streamsize>(grey.size()));
    return static_cast<bool>(file);
}

#endif
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef GREY_H` / `#define GREY_H` | The include guard for this header. |
| 4–7 | `#include <cstdint>` … `<vector>` | Bytes, file writing, file names, and the grey buffer. |
| 8 | `#include "colourf.h"` | `ColourF`, `toColourF`, `toByte` and `toColour` (Chapter 14) — and, through it, `image.h`. |
| 10 | `inline double luma(ColourF c) {` | The weighted average of a colour (Section 15.3). Input: 0–1 values. Output: one 0–1 value. |
| 11 | `return 0.2126 * c.r + 0.7152 * c.g + 0.0722 * c.b;` | The Rec. 709 weights (Section 15.4). |
| 12 | `}` | End of `luma`. |
| 14 | `inline double plainAverage(ColourF c) {` | The plain average, so we can **compare** (Section 15.1). |
| 15 | `return (c.r + c.g + c.b) / 3.0;` | Each channel has the weight 1/3. `3.0` keeps it a `double` division. |
| 16 | `}` | End. |
| 18 | `inline std::uint8_t greyByte(Colour c) {` | One colour in, one grey byte out. |
| 19 | `return toByte(luma(toColourF(c)));` | Three steps, read from the inside out: bytes → 0–1 values → luma → byte (clamped and rounded). |
| 20 | `}` | End. |
| 22 | `inline Colour toGrey(Colour c) {` | The grey version of a colour, as a `Colour` with R = G = B. |
| 23 | `std::uint8_t v = greyByte(c);` | The grey value. |
| 24 | `return Colour{v, v, v};` | Put it into all three channels. |
| 25 | `}` | End. |
| 27 | `inline Colour desaturate(Colour c, double amount) {` | Move a colour part of the way toward its own grey (Section 15.7). |
| 28 | `ColourF f = toColourF(c);` | The colour as 0–1 values. |
| 29 | `double y = luma(f);` | Its brightness. We call it `y`, the usual letter for luma in video standards. |
| 30 | `ColourF grey{y, y, y};` | Its own grey: the same brightness, no colour. |
| 31 | `return toColour(f + (grey - f) * amount);` | A lerp from the colour to its grey (Chapter 13), written with the `ColourF` operators (Chapter 14). `toColour` clamps, so amounts outside 0–1 are safe. |
| 32 | `}` | End. |
| 34 | `inline bool saveGreyPGM(const Image& image, const std::string& fileName) {` | Turn an image into grey and save it as **PGM P5**, all in one go. The image is not changed (`const Image&`). |
| 35–38 | `std::ofstream file(fileName, std::ios::binary); if (!file) { return false; }` | Open in binary mode (Chapter 9); stop if it fails. |
| 39 | `std::vector<std::uint8_t> grey(image.width() * image.height());` | A grey buffer: **one** byte per pixel (Chapter 10). A `std::vector` made with a size starts with all zeros. |
| 40–41 | `for (int y ...) { for (int x ...) {` | Every pixel. |
| 42 | `grey[y * image.width() + x] = greyByte(image.getPixel(x, y));` | Compute the grey and store it. The index has **no** `× 3` (Chapter 10, Section 10.2). |
| 43–44 | `}` `}` | End of the loops. |
| 45 | `file << "P5\n" << image.width() << " " << image.height() << "\n255\n";` | The PGM header, with exactly one `\n` after 255. |
| 46–47 | `file.write(reinterpret_cast<const char*>(grey.data()), ...);` | Write all the grey bytes in one call. |
| 48 | `return static_cast<bool>(file);` | `true` if it all worked. |
| 49 | `}` | End of `saveGreyPGM`. |
| 51 | `#endif` | End of the include guard. |

---

## Code, part 2: comparing the two greys

File: `ch15/to_grey.cpp`

```cpp
#include <iostream>
#include <string>
#include "grey.h"

void printRow(const std::string& name, Colour c) {
    ColourF f = toColourF(c);
    std::cout << name << ": average " << static_cast<int>(toByte(plainAverage(f)))
              << ", luma " << static_cast<int>(greyByte(c)) << "\n";
}

int main() {
    const Colour barColours[6] = {colours::red, colours::green, colours::blue,
                                  colours::yellow, colours::cyan, colours::magenta};
    const std::string names[6] = {"red    ", "green  ", "blue   ",
                                  "yellow ", "cyan   ", "magenta"};
    for (int i = 0; i < 6; ++i) {
        printRow(names[i], barColours[i]);
    }
    printRow("white  ", colours::white);

    Image bars(360, 80);
    for (int y = 0; y < bars.height(); ++y) {
        for (int x = 0; x < bars.width(); ++x) {
            bars.setPixel(x, y, barColours[x / 60]);
        }
    }

    Image averaged = bars;
    for (int y = 0; y < averaged.height(); ++y) {
        for (int x = 0; x < averaged.width(); ++x) {
            ColourF f = toColourF(averaged.getPixel(x, y));
            std::uint8_t v = toByte(plainAverage(f));
            averaged.setPixel(x, y, Colour{v, v, v});
        }
    }

    const Colour orange{255, 128, 0};
    Image steps(250, 50);
    for (int y = 0; y < steps.height(); ++y) {
        for (int x = 0; x < steps.width(); ++x) {
            double amount = (x / 50) * 0.25;
            steps.setPixel(x, y, desaturate(orange, amount));
        }
    }

    bool ok = bars.savePPM("bars.ppm");
    ok = ok && averaged.savePPM("bars_average.ppm");
    ok = ok && saveGreyPGM(bars, "bars_luma.pgm");
    ok = ok && steps.savePPM("desaturate.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }

    Colour half = desaturate(orange, 0.5);
    Colour full = desaturate(orange, 1.0);
    std::cout << "\norange half grey = (" << static_cast<int>(half.r) << ", "
              << static_cast<int>(half.g) << ", " << static_cast<int>(half.b) << ")\n";
    std::cout << "orange full grey = (" << static_cast<int>(full.r) << ", "
              << static_cast<int>(full.g) << ", " << static_cast<int>(full.b) << ")\n";
    return 0;
}
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#include <iostream>` / `<string>` | Printing and names. |
| 3 | `#include "grey.h"` | Our new header — and through it `colourf.h` and `image.h`. |
| 5 | `void printRow(const std::string& name, Colour c) {` | Print one line: a colour's name, its plain average, and its luma. |
| 6 | `ColourF f = toColourF(c);` | The colour as 0–1 values. |
| 7 | `std::cout << name << ": average " << static_cast<int>(toByte(plainAverage(f)))` | The plain average, turned into a byte, printed as a number. |
| 8 | `<< ", luma " << static_cast<int>(greyByte(c)) << "\n";` | The luma, as a byte. |
| 9 | `}` | End. |
| 11 | `int main() {` | The program starts here. |
| 12–13 | `const Colour barColours[6] = {colours::red, ...};` | The 6 colours of the test bars: the 3 primaries and the 3 secondaries (Chapter 5). |
| 14–15 | `const std::string names[6] = {"red    ", ...};` | Their names, padded with spaces to the same length so the output lines up. |
| 16–18 | `for (int i = 0; i < 6; ++i) { printRow(names[i], barColours[i]); }` | Print the comparison for each colour. |
| 19 | `printRow("white  ", colours::white);` | And for white, to check that it stays 255. |
| 21 | `Image bars(360, 80);` | 6 bars, each 60 pixels wide: 6 × 60 = 360. |
| 22–23 | `for (int y ...) { for (int x ...) {` | Every pixel. |
| 24 | `bars.setPixel(x, y, barColours[x / 60]);` | `x / 60` is the bar number: 0 for x = 0–59, 1 for 60–119, … 5 for 300–359. |
| 25–26 | `}` `}` | End of the loops. |
| 28 | `Image averaged = bars;` | A **copy** of the bars (Chapter 11, Example 3). We change the copy, not the original. |
| 29–30 | `for (int y ...) { for (int x ...) {` | Every pixel of the copy. |
| 31 | `ColourF f = toColourF(averaged.getPixel(x, y));` | Read the colour, as 0–1 values. |
| 32 | `std::uint8_t v = toByte(plainAverage(f));` | The **plain average**, as a byte. |
| 33 | `averaged.setPixel(x, y, Colour{v, v, v});` | Store it as a grey (R = G = B). |
| 34–35 | `}` `}` | End of the loops. |
| 37 | `const Colour orange{255, 128, 0};` | The colour we will desaturate. |
| 38 | `Image steps(250, 50);` | 5 steps, each 50 pixels wide. |
| 39–40 | `for (int y ...) { for (int x ...) {` | Every pixel. |
| 41 | `double amount = (x / 50) * 0.25;` | `x / 50` is the step number 0–4 (**integer** division, on purpose). Times 0.25 gives the amounts 0, 0.25, 0.5, 0.75, 1. |
| 42 | `steps.setPixel(x, y, desaturate(orange, amount));` | Orange, made that much greyer. |
| 43–44 | `}` `}` | End of the loops. |
| 46 | `bool ok = bars.savePPM("bars.ppm");` | The colour bars. |
| 47 | `ok = ok && averaged.savePPM("bars_average.ppm");` | The bars, grey by **plain average** (as PPM). |
| 48 | `ok = ok && saveGreyPGM(bars, "bars_luma.pgm");` | The bars, grey by **luma**, as a real **PGM**. We pass the **colour** image; `saveGreyPGM` converts it. |
| 49 | `ok = ok && steps.savePPM("desaturate.ppm");` | The five desaturation steps. |
| 50–53 | `if (!ok) { ...; return 1; }` | Stop if anything failed. |
| 55 | `Colour half = desaturate(orange, 0.5);` | Section 15.7's example. |
| 56 | `Colour full = desaturate(orange, 1.0);` | Fully grey: it must equal the luma of orange. |
| 57–60 | `std::cout << ...` | Print both colours. |
| 61 | `return 0;` | The program finished with no problem. |
| 62 | `}` | End of `main`. |

Compile:

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common to_grey.cpp -o to_grey
```

### What you should see

```
red    : average 85, luma 54
green  : average 85, luma 182
blue   : average 85, luma 18
yellow : average 170, luma 237
cyan   : average 170, luma 201
magenta: average 170, luma 73
white  : average 255, luma 255

orange half grey = (200, 137, 73)
orange full grey = (146, 146, 146)
```

🔢 **Maths: check yellow**

> yellow = (1, 1, 0)
> average: (1 + 1 + 0) ÷ 3 = 0.667 → × 255 = 170
> luma: 0.2126 + 0.7152 + 0 = 0.9278 → × 255 = 236.6 → **237**

Yellow is almost as bright as white, because it contains red **and** green. Blue adds very little.

🔢 **Maths: check that red + green + blue ≈ white**

> 54 + 182 + 18 = 254

Almost 255 (the small difference comes from rounding each one). Red, green and blue light together **make** white, so their brightnesses should add up to white's brightness. They do. The plain average gives 85 + 85 + 85 = 255 too, but it puts the brightness in the wrong places.

Open the images side by side:
- `bars.ppm`: six bright colour bars.
- `bars_average.ppm`: three equal greys (85), then three equal lighter greys (170). You **cannot** tell red, green and blue apart. Yellow, cyan and magenta also look identical.
- `bars_luma.pgm`: every bar has its own grey. Green is light, blue is almost black, yellow is almost white. It matches how the colour bars **feel** to your eye.
- `desaturate.ppm`: five orange squares, from strong orange to plain grey. All five look **equally bright**.

---

## Small examples

### Example 1 — Turn any photo into grey

With Chapter 12's `loadPPM`:

```cpp
Image photo(1, 1);
if (loadPPM("photo.ppm", photo)) {
    saveGreyPGM(photo, "photo_grey.pgm");
}
```

Two lines of real work. The PGM file is a third of the size of the PPM.

### Example 2 — Is this colour "light" or "dark"?

A common use of luma: choose **black or white text** on a coloured button, so the text is easy to read.

```cpp
Colour textColourFor(Colour background) {
    return greyByte(background) > 128 ? colours::black : colours::white;
}
```

> yellow background: luma 237 > 128 → **black** text
> blue background: luma 18 → **white** text
> green background: luma 182 → **black** text
> red background: luma 54 → **white** text

With the plain average, green (85) would wrongly get white text, which is hard to read on bright green.

### Example 3 — A grey image with colour in one place

Keep only the **red** parts of a picture in colour, and make everything else grey — a well-known photo effect.

```cpp
Colour c = img.getPixel(x, y);
bool reddish = c.r > 150 && c.g < 100 && c.b < 100;
img.setPixel(x, y, reddish ? c : toGrey(c));
```

> (200, 40, 30): r > 150, g < 100, b < 100 → kept red.
> (200, 180, 30): g is not < 100 → turned grey.

### Example 4 — Equal-brightness colours

Two colours with the same luma look equally bright, even if they are very different.

> pure red (255, 0, 0): luma 54
> the brightest pure blue (0, 0, 255): luma only 18

To be as bright as red, a pure blue would need about 3 times more light (54 ÷ 18 = 3) — but 255 is the limit. So **no** pure blue on a screen is as bright as pure red. A **grey** of (54, 54, 54), on the other hand, is exactly as bright as red. Designers use luma to check that a picture still "reads" well for people who cannot see some colours: if two important colours have almost the same luma, they may look the same to them.

---

## Common mistakes

⚠️ **Using the plain average.** Red, green and blue all become the same grey. Use the weights.

⚠️ **Weights that do not add up to 1.** If you type 0.2126, 0.7152, 0.722 (one zero missing), white becomes 1.65 → clamped to 255, and **every** light colour is too bright. Check the sum.

⚠️ **Using bytes with the weights without ÷ 255.** 0.2126 × 255 + … is fine **if** you also skip the × 255 at the end. Mixing the two scales gives nonsense. Our code always works in 0–1 (`ColourF`).

⚠️ **`× 3` in a grey buffer index.** A PGM has **one** byte per pixel.

⚠️ **Desaturating toward a fixed grey.** Lerping toward (128, 128, 128) makes bright colours darker and dark colours brighter. Lerp toward the colour's **own** grey.

⚠️ **Calling luma "luminance".** True luminance needs the gamma step first (Chapter 17).

---

## Practice

🏋️ **1.** Compute the luma of (100, 150, 200). Show every step with 0–1 values.

🏋️ **2.** Compute the plain average and the luma of cyan (0, 255, 255). Which is bigger? Why?

🏋️ **3.** Compute the Rec. 601 grey of green (0, 255, 0). Compare it with the Rec. 709 value (182).

🏋️ **4.** A 640 × 480 colour image is saved with `saveGreyPGM`. How big is the file?

🏋️ **5.** Desaturate (0, 0, 255) by 0.5. (Hint: its luma is 0.0722.)

🏋️ **6.** Write a program that makes a 256-wide image where the **top half** is the rainbow from Chapter 13 and the **bottom half** is the luma of the rainbow. Where is the rainbow brightest?

🏋️ **7.** Change `textColourFor` from Example 2 to use the plain average. Which of the six bar colours gets a different text colour?

---

## Answers

**1.**
> (100, 150, 200) ÷ 255 = (0.392, 0.588, 0.784)
> 0.2126 × 0.392 = 0.0834
> 0.7152 × 0.588 = 0.4206
> 0.0722 × 0.784 = 0.0566
> sum = 0.5606 → × 255 = 142.9 → **143**

**2.**
> average: (0 + 255 + 255) ÷ 3 = 170
> luma: 0.7152 + 0.0722 = 0.7874 → × 255 = 200.8 → **201**
> The luma is **bigger**, because cyan contains full **green**, which counts for 0.7152 — more than two-thirds of all brightness.

**3.**
> 0.587 × 255 = 149.7 → **150**
> Rec. 709 gives 182. Old TV green was a slightly different colour from modern screen green, so the weights differ.

**4.**
> header `P5\n640 480\n255\n` = 3 + 8 + 4 = 15
> pixels = 640 × 480 = 307,200
> total = **307,215 bytes** (the same as Chapter 10, Practice 2)

**5.**
> grey version = (0.0722, 0.0722, 0.0722)
> R: 0 + (0.0722 − 0) × 0.5 = 0.0361 → × 255 = 9.2 → **9**
> G: the same → **9**
> B: 1 + (0.0722 − 1) × 0.5 = 1 − 0.4639 = 0.5361 → 136.7 → **137**
> result = **(9, 9, 137)** — a dark, greyish blue. It is dark because blue's own brightness is low.

**6.** Use `multiStop` from Chapter 13 for the top half, and `toGrey(multiStop(stops, t))` for the bottom half. The grey band is **brightest at yellow** (luma 237) and at **cyan** (201), and **darkest at blue** (18). The rainbow does **not** look equally bright all the way, and the grey band shows exactly where it is bright and where it is dark.

**7.** With the plain average: red, green and blue all have 85 (< 128) → white text. Yellow, cyan and magenta all have 170 (> 128) → black text.

Compared with luma:
- **green** changes: luma 182 → black text, average 85 → white text.
- **magenta** changes: luma 73 → white text, average 170 → black text.

The luma choices are the easy-to-read ones.

---

## Summary

🧠 The plain average (R + G + B) ÷ 3 makes red, green and blue the **same** grey. That looks wrong.

🧠 The eye is most sensitive to **green**, less to **red**, and least to **blue**.

🧠 **Luma = 0.2126 R + 0.7152 G + 0.0722 B** (Rec. 709). The weights add up to 1, so white stays white.

🧠 The older Rec. 601 weights are 0.299, 0.587, 0.114.

🧠 **Luma** uses the bytes directly. True **luminance** first undoes gamma (Chapter 17).

🧠 `saveGreyPGM` turns an image into grey and saves it as a PGM: one byte per pixel, three times smaller.

🧠 **Desaturate** = lerp toward the colour's **own** grey. The brightness stays the same.

---

## Next chapter

RGB says how much red, green and blue light to mix. But people do not think like that. We say "a **darker** blue", "a **more yellow** green", "a **paler** pink". In Chapter 16 we learn **HSV and HSL**: colour as **hue** (which colour), **saturation** (how strong) and **value** or **lightness** (how bright) — and the maths to change between them and RGB.
