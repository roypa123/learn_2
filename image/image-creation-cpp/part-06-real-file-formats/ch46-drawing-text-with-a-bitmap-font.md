# Chapter 46 — Drawing Text with a Bitmap Font

> **Part 6 · Chapter 46 of 82**
> **You need:** Chapters 1–45 (especially 4, 19, 27, 35 and 45) · **You will make:** `font.h` (a complete 5 × 8 pixel font for all 95 printable ASCII characters, `drawText`, `drawTextCentred`, `textBox` and `drawTextSmooth`), and three PNG files: `font.png` (every character), `sizes.png` (smooth text at five sizes) and `label.png` (a picture with a title and a caption)

---

## What you will learn

- What a **font** and a **glyph** are, and the difference between **bitmap** and **outline** fonts.
- How to store a whole font in 760 bytes, one bit per pixel.
- How to find a character's glyph from its **ASCII** code.
- How to lay out text: character spacing, line spacing, width and height.
- How to draw text **bigger**, in blocks, and at **any size** with smooth edges.
- How to make text easy to read on a busy picture: shadows and boxes.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **font** | A set of shapes for letters, digits and signs, all in one style. |
| **glyph** | The shape of one character in a font. |
| **bitmap font** | A font whose glyphs are small grids of on/off pixels. |
| **outline font** | A font whose glyphs are curves (Bézier curves, Chapter 34). |
| **ASCII** | The standard numbering of characters: 'A' = 65, '0' = 48, space = 32. |
| **advance** | How far the pen moves after one character. |
| **monospaced** | Every character has the same advance. |
| **descender** | The part of a letter below the line, as in g, j, p, q and y. |

---

## 46.1 Letters are pictures

Every letter you see on a screen is drawn with pixels, just like our circles and triangles. There is no magic "letter" pixel.

📖 **New words: font and glyph** — a **font** is a set of shapes for characters, all in one style. The shape of one character is its **glyph**. "A" is a character; the particular drawing of "A" in a particular font is a glyph.

There are two main kinds of fonts:

📖 **New words: bitmap font and outline font**

- A **bitmap font** stores each glyph as a small **grid of pixels**, on or off. Simple and fast — but it has one natural size. Old computers, calculators and many small displays use them.
- An **outline font** stores each glyph as **curves** — usually the quadratic and cubic **Bézier curves** of Chapter 34. It can be drawn at any size and filled with smooth edges (Chapter 27). The fonts in your phone and browser are outline fonts.

We build a **bitmap font**. It needs no curves, it fits in a few hundred bytes, and in Section 46.7 we will still draw it at any size with smooth edges.

---

## 46.2 A glyph in eight bytes

Our glyphs are **5 pixels wide and 8 pixels tall**. Capital letters and digits use the top 7 rows. The 8th row is for **descenders**.

📖 **New word: descender** — the part of a letter that hangs below the line: the tails of g, j, p, q and y.

Each row of a glyph has 5 pixels: 5 bits. We store each row in one byte, using the **lowest 5 bits**. Bit 4 (value 16) is the **left** column, bit 0 (value 1) the **right** one:

```
   column:   0  1  2  3  4
   bit:      4  3  2  1  0
   value:   16  8  4  2  1
```

🔢 **Maths: the letter A** (the program prints it)

```
'A': 0E 11 11 1F 11 11 11 00
    .###.        0 + 8 + 4 + 2 + 0  = 14 = 0x0E
    #...#       16 + 0 + 0 + 0 + 1  = 17 = 0x11
    #...#                             17 = 0x11
    #####       16 + 8 + 4 + 2 + 1  = 31 = 0x1F
    #...#                             17 = 0x11
    #...#                             17 = 0x11
    #...#                             17 = 0x11
    .....                              0 = 0x00
```

Eight bytes for one letter. And a letter with a descender:

```
'g': 00 00 0F 11 11 0F 01 0E
    .....
    .....
    .####
    #...#
    #...#
    .####
    ....#
    .###.        ← row 7: the descender
```

🔢 **Maths: the size of the whole font**

> 95 characters × 8 bytes = **760 bytes**

Our font table, `kFont`, is a list of 95 glyphs, each a list of 8 bytes. In the header, each glyph is one line, with a comment naming its character:

```cpp
    {{0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11, 0x00}},  // 65 A
```

💡 Designing a font is real work: every glyph must be readable, and all of them must look like one family. Ours follows the style of classic 5 × 7 screen fonts. You can change any glyph you do not like — just draw it on squared paper and work out the bytes.

---

## 46.3 Finding a glyph: ASCII

How does the program know which glyph belongs to the character 'A'?

📖 **New word: ASCII** — the standard numbering of characters, from 1963. In C++, a `char` holds such a number. Some codes:

| characters | codes |
|---|---|
| space | 32 |
| `!` `"` `#` … `/` | 33–47 |
| `0`–`9` | 48–57 |
| `A`–`Z` | 65–90 |
| `a`–`z` | 97–122 |
| `~` | 126 |

Codes **32 to 126** are the **printable** characters: 95 of them. (0–31 and 127 are control codes like "new line" and "tab".) Our table has them in order, so:

> **glyph number = code − 32**
> 'A': 65 − 32 = **33** → the 34th line of the table (counting from 1)

⚠️ **Characters outside 32–126** — a tab, a new line in the wrong place, or letters like é and ü (which are not ASCII) — would give a glyph number outside the table. Reading `kFont[200]` would read memory that is not ours. So `glyphIndex` draws them as **'?'**:

```
a character outside the font is drawn as '?': glyph 31 = glyph 31
```

⚠️ A `char` may be **negative** in C++ (on many computers, `char` is signed, so é's bytes come out as negative numbers). We first convert it with `static_cast<unsigned char>`, which gives 0–255 (Chapter 4), and only then compare.

---

## 46.4 Reading one pixel of a glyph

Is pixel (x, y) of a glyph "on"? Take row y, shift the wanted bit down to position 0, and mask it (Chapter 4):

> bit number = 4 − x (column 0 is bit 4)
> on = (row >> (4 − x)) & 1

🔢 **Maths: 'A', pixel (1, 0)**

> row 0 = 0x0E = 0000 1110
> x = 1 → bit 3 → 0x0E >> 3 = 0000 0001 → & 1 = **1** → on ✓ (`.###.` has column 1 on)

`glyphPixel` also answers "off" for any (x, y) **outside** the 5 × 8 grid. That makes the smooth drawing of Section 46.7 simpler: it may ask about neighbouring cells without checking first.

---

## 46.5 Laying out text

To write a word, we draw its glyphs one after another, moving a **pen** to the right.

📖 **New words: advance and monospaced** — the **advance** is how far the pen moves after each character. Ours is **6** pixels: 5 for the glyph, 1 for a gap. Every character has the same advance, so our font is **monospaced** (like the font of an old typewriter or a code editor).

For a new line (the character `'\n'`), the pen goes back to the left edge and down by the **line advance**: **10** pixels (8 for the glyph, 2 for a gap).

```
   H . . . . . e . . . . . l ...         each glyph starts 6 pixels after the last
   <-- 5 --> 1 <-- 5 --> 1
```

🔢 **Maths: the size of a text**

> width = (characters in the longest line × 6 − 1) × scale   (no gap after the last character)
> height = (number of lines × 10 − 2) × scale   (no gap after the last line)
> "Hello, world!": 13 characters → 13 × 6 − 1 = **77**; 1 line → 10 − 2 = **8**: 77 × 8 pixels
> at scale 3: 231 × 24
> "Line one\nand two": the longest line has 8 characters → 47; 2 lines → 18: 47 × 18

The program draws "Hello, world!" into a 77 × 8 picture and prints it as text:

```
#   #        ##    ##                                        ##       #   #  
#   #         #     #                                         #       #   #  
#   #  ###    #     #    ###              #   #  ###  # ##    #    ## #   #  
##### #   #   #     #   #   #             #   # #   # ##  #   #   #  ##   #  
#   # #####   #     #   #   #             # # # #   # #       #   #   #   #  
#   # #       #     #   #   #  ##         # # # #   # #       #   #   #      
#   #  ###   ###   ###   ###    #          # #   ###  #      ###   ####   #  
                               #                                             
```

Look at the comma: its tail uses row 7, the descender row.

💡 Knowing the size **before** drawing is useful: to centre a text, start at centre − width / 2 (`drawTextCentred`); to put a box behind it, make the box the text's size plus a margin (`textBox`).

---

## 46.6 Bigger text: scaling up

At scale 1, each font pixel is one image pixel. Text that small is hard to read on a big picture. `drawText` has a **scale**: each "on" font pixel becomes a **scale × scale square**, drawn with `fillRect` (Chapter 19).

🔢 **Maths: where does a font pixel go?**

> pen at (penX, penY), font pixel (gx, gy), scale s
> square: from (penX + gx × s, penY + gy × s), size s × s
> 'A' at (10, 20), scale 3: font pixel (1, 0) → square at (13, 20), 3 × 3 pixels

This is exactly the **nearest-neighbour** enlarging of Chapter 35: the glyph gets bigger, but its stairs get bigger too. The program draws all 95 characters at scale 3 into `font.png`:

```
font sheet: 300 x 192, 10080 dark pixels
```

🔢 **Maths: the dark pixels**

> the 95 glyphs have 1,120 "on" pixels together; each becomes 3 × 3 = 9 image pixels → 1,120 × 9 = **10,080**

Whole-number scales keep the text **sharp** — good for pixel-art style. But we cannot make it 2.5 times bigger, and it never looks smooth.

---

## 46.7 Any size, with smooth edges

Now think of each "on" font pixel as a **small square** of size `size` × `size`, where `size` may be any number — 1.5, 2.5, 4.5 … These squares do not line up with the image pixels any more. An image pixel may be partly covered.

We know what to do with partial cover: Chapter 27's **coverage**. The coverage of an image pixel is the part of its area that is inside the shape — and here we can compute it **exactly**, without samples, because the shape is made of squares:

> coverage = sum, over all "on" font squares that touch the pixel, of (overlap width × overlap height)

🔢 **Maths: the overlap of two intervals**

> overlap of [a0, a1] and [b0, b1] = max(0, min(a1, b1) − max(a0, b0))
> [2, 3] and [2.8, 5.3]: min(3, 5.3) − max(2, 2.8) = 3 − 2.8 = **0.2**
> [2, 3] and [5.3, 7.8]: min(3, 7.8) − max(2, 5.3) = 3 − 5.3 < 0 → **0** (no overlap)

The overlap of two **squares** is (overlap in x) × (overlap in y). The font squares never overlap each other, so we can simply add their pieces.

🔢 **Maths: 'I' at (0.3, 0.0), size 2.5** (the program prints this)

> 'I' row 0 = `.###.` — columns 1, 2, 3 are on; row 1 = `..#..`
> font column 0 covers x from 0.3 to 2.8; column 1 from 2.8 to 5.3; row 0 covers y from 0 to 2.5; row 1 from 2.5 to 5
> **pixel (2, 0)** (x 2–3, y 0–1): column 0 (off) and column 1 (on, overlap 0.2), row 0 (overlap 1) → 0.2 × 1 = **0.2**
> **pixel (2, 2)** (x 2–3, y 2–3): column 1 in row 0 (on: 0.2 × 0.5) and in row 1 (off) → **0.1**
> **pixel (3, 0)** (x 3–4): entirely inside column 1, row 0 → **1**

```
'I' at (0.3, 0.0), size 2.5: coverage of pixel (2, 0) = 0.2, of pixel (2, 2) = 0.1, of pixel (3, 0) = 1
```

Which font squares can touch pixel px? Font column gx covers x from left + gx × size to left + (gx + 1) × size. So the columns that touch [px, px + 1] are from ⌊(px − left) / size⌋ to ⌊(px + 1 − left) / size⌋ — usually one or two of them (more when size < 1). The same for rows.

Then `paintCoverage` (Chapter 27) blends the text colour into the pixel by its coverage, in linear light (Chapter 18). `drawTextSmooth` does this for every pixel in each glyph's box.

```
   size 1.0   — the same as drawText at scale 1, when x and y are whole numbers
   size 1.5   — readable, with soft grey edges
   size 2.5, 3.0, 4.5 …   — any size, any position (even between pixels)
```

Open `sizes.png` to see five sizes. The edges are smooth, but at large sizes you can still see the font's **steps**: they belong to the glyph's design, not to the drawing. Removing them needs an outline font.

⚠️ At sizes **below 1**, one image pixel can touch two neighbouring characters (the 1-pixel gap becomes thinner than a pixel). Each character is blended separately, so such a pixel gets the colour twice — the "conflation" of Chapter 27. Text that small is unreadable anyway.

---

## 46.8 Text people can read

White text on a light sky disappears; black text on a dark sky too. Two simple tricks:

**1. A shadow.** Draw the text first in a dark colour, moved 2 pixels right and down, then in the real colour on top:

```cpp
drawTextCentred(label, 152, 22, title, Colour{20, 30, 60}, 4);   // shadow
drawTextCentred(label, 150, 20, title, colours::white, 4);        // text
```

**2. A box.** Darken a rectangle behind the text with `fillRectAlpha` (Chapter 19), then draw the text on top:

🔢 **Maths: the caption box**

> caption "300 x 200 pixels\nsaved as a PNG", scale 2, at (20, 150), margin 6
> width: the longest line has 16 characters → (16 × 6 − 1) × 2 = **190**; height: (2 × 10 − 2) × 2 = **36**
> box: from (20 − 6, 150 − 6) = **(14, 144)**, size (190 + 12) × (36 + 12) = 202 × 48 → to **(216, 192)**

```
caption box: 14, 144 to 216, 192
```

With alpha 0.5, the sky still shows through the box, but the white text stands out clearly. Open `label.png`.

---

## 46.9 The end of Part 6

Part 6 started with a BMP header and ends with a complete toolbox for files:

| format | write | read |
|---|---|---|
| PPM (Chapters 8, 9 and 12) | ✓ | ✓ |
| PGM / PBM (Chapter 10) | ✓ | — |
| BMP (Chapters 36–38) | ✓ | ✓ |
| TGA, with RLE and alpha (Chapter 39) | ✓ | ✓ |
| PNG, with filters and Deflate (Chapters 40–45) | ✓ | ✓ (8-bit RGB/RGBA) |

And now our pictures can carry **text**: titles, labels, numbers. In Part 7 we stop drawing shapes and start **changing pictures**: brightness, contrast, histograms, blur, sharpening, edges and dithering — and we can load real photos to try them on.

---

## Code, part 1: `font.h`

File: `common/font.h` (new). It belongs to the drawing family: it includes `resize.h`, the last header of the drawing chain (Chapter 35), which brings in `fillRect`, `makeRect`, `paintCoverage` and everything else we need.

```cpp
#ifndef FONT_H
#define FONT_H

#include <algorithm>
#include <array>
#include <cmath>
#include <cstdint>
#include <string>
#include "resize.h"

const int kGlyphWidth = 5;
const int kGlyphHeight = 8;
const int kCharAdvance = 6;
const int kLineAdvance = 10;
const int kFirstChar = 32;
const int kLastChar = 126;

const std::array<std::array<std::uint8_t, 8>, 95> kFont = {{
    {{0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}},  // 32 space
    {{0x04, 0x04, 0x04, 0x04, 0x04, 0x00, 0x04, 0x00}},  // 33 !
    {{0x0A, 0x0A, 0x0A, 0x00, 0x00, 0x00, 0x00, 0x00}},  // 34 "
    {{0x0A, 0x0A, 0x1F, 0x0A, 0x1F, 0x0A, 0x0A, 0x00}},  // 35 #
    {{0x04, 0x0F, 0x14, 0x0E, 0x05, 0x1E, 0x04, 0x00}},  // 36 $
    {{0x18, 0x19, 0x02, 0x04, 0x08, 0x13, 0x03, 0x00}},  // 37 %
    {{0x0C, 0x12, 0x14, 0x08, 0x15, 0x12, 0x0D, 0x00}},  // 38 &
    {{0x04, 0x04, 0x08, 0x00, 0x00, 0x00, 0x00, 0x00}},  // 39 '
    {{0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02, 0x00}},  // 40 (
    {{0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08, 0x00}},  // 41 )
    {{0x00, 0x04, 0x15, 0x0E, 0x15, 0x04, 0x00, 0x00}},  // 42 *
    {{0x00, 0x04, 0x04, 0x1F, 0x04, 0x04, 0x00, 0x00}},  // 43 +
    {{0x00, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x04, 0x08}},  // 44 ,
    {{0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00, 0x00}},  // 45 -
    {{0x00, 0x00, 0x00, 0x00, 0x00, 0x0C, 0x0C, 0x00}},  // 46 .
    {{0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x00, 0x00}},  // 47 /
    {{0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E, 0x00}},  // 48 0
    {{0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E, 0x00}},  // 49 1
    {{0x0E, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1F, 0x00}},  // 50 2
    {{0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E, 0x00}},  // 51 3
    {{0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02, 0x00}},  // 52 4
    {{0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E, 0x00}},  // 53 5
    {{0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E, 0x00}},  // 54 6
    {{0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08, 0x00}},  // 55 7
    {{0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E, 0x00}},  // 56 8
    {{0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C, 0x00}},  // 57 9
    {{0x00, 0x0C, 0x0C, 0x00, 0x0C, 0x0C, 0x00, 0x00}},  // 58 :
    {{0x00, 0x0C, 0x0C, 0x00, 0x0C, 0x04, 0x08, 0x00}},  // 59 ;
    {{0x02, 0x04, 0x08, 0x10, 0x08, 0x04, 0x02, 0x00}},  // 60 <
    {{0x00, 0x00, 0x1F, 0x00, 0x1F, 0x00, 0x00, 0x00}},  // 61 =
    {{0x08, 0x04, 0x02, 0x01, 0x02, 0x04, 0x08, 0x00}},  // 62 >
    {{0x0E, 0x11, 0x01, 0x02, 0x04, 0x00, 0x04, 0x00}},  // 63 ?
    {{0x0E, 0x11, 0x01, 0x0D, 0x15, 0x15, 0x0E, 0x00}},  // 64 @
    {{0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11, 0x00}},  // 65 A
    {{0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E, 0x00}},  // 66 B
    {{0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E, 0x00}},  // 67 C
    {{0x1C, 0x12, 0x11, 0x11, 0x11, 0x12, 0x1C, 0x00}},  // 68 D
    {{0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F, 0x00}},  // 69 E
    {{0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10, 0x00}},  // 70 F
    {{0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F, 0x00}},  // 71 G
    {{0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11, 0x00}},  // 72 H
    {{0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E, 0x00}},  // 73 I
    {{0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C, 0x00}},  // 74 J
    {{0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11, 0x00}},  // 75 K
    {{0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F, 0x00}},  // 76 L
    {{0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11, 0x00}},  // 77 M
    {{0x11, 0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x00}},  // 78 N
    {{0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E, 0x00}},  // 79 O
    {{0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10, 0x00}},  // 80 P
    {{0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D, 0x00}},  // 81 Q
    {{0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11, 0x00}},  // 82 R
    {{0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E, 0x00}},  // 83 S
    {{0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x00}},  // 84 T
    {{0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E, 0x00}},  // 85 U
    {{0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04, 0x00}},  // 86 V
    {{0x11, 0x11, 0x11, 0x15, 0x15, 0x15, 0x0A, 0x00}},  // 87 W
    {{0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11, 0x00}},  // 88 X
    {{0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04, 0x00}},  // 89 Y
    {{0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F, 0x00}},  // 90 Z
    {{0x0E, 0x08, 0x08, 0x08, 0x08, 0x08, 0x0E, 0x00}},  // 91 [
    {{0x00, 0x10, 0x08, 0x04, 0x02, 0x01, 0x00, 0x00}},  // 92 backslash
    {{0x0E, 0x02, 0x02, 0x02, 0x02, 0x02, 0x0E, 0x00}},  // 93 ]
    {{0x04, 0x0A, 0x11, 0x00, 0x00, 0x00, 0x00, 0x00}},  // 94 ^
    {{0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F, 0x00}},  // 95 _
    {{0x08, 0x04, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00}},  // 96 `
    {{0x00, 0x00, 0x0E, 0x01, 0x0F, 0x11, 0x0F, 0x00}},  // 97 a
    {{0x10, 0x10, 0x16, 0x19, 0x11, 0x11, 0x1E, 0x00}},  // 98 b
    {{0x00, 0x00, 0x0E, 0x10, 0x10, 0x11, 0x0E, 0x00}},  // 99 c
    {{0x01, 0x01, 0x0D, 0x13, 0x11, 0x11, 0x0F, 0x00}},  // 100 d
    {{0x00, 0x00, 0x0E, 0x11, 0x1F, 0x10, 0x0E, 0x00}},  // 101 e
    {{0x06, 0x09, 0x08, 0x1C, 0x08, 0x08, 0x08, 0x00}},  // 102 f
    {{0x00, 0x00, 0x0F, 0x11, 0x11, 0x0F, 0x01, 0x0E}},  // 103 g
    {{0x10, 0x10, 0x16, 0x19, 0x11, 0x11, 0x11, 0x00}},  // 104 h
    {{0x04, 0x00, 0x0C, 0x04, 0x04, 0x04, 0x0E, 0x00}},  // 105 i
    {{0x02, 0x00, 0x06, 0x02, 0x02, 0x02, 0x12, 0x0C}},  // 106 j
    {{0x10, 0x10, 0x12, 0x14, 0x18, 0x14, 0x12, 0x00}},  // 107 k
    {{0x0C, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E, 0x00}},  // 108 l
    {{0x00, 0x00, 0x1A, 0x15, 0x15, 0x11, 0x11, 0x00}},  // 109 m
    {{0x00, 0x00, 0x16, 0x19, 0x11, 0x11, 0x11, 0x00}},  // 110 n
    {{0x00, 0x00, 0x0E, 0x11, 0x11, 0x11, 0x0E, 0x00}},  // 111 o
    {{0x00, 0x00, 0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10}},  // 112 p
    {{0x00, 0x00, 0x0F, 0x11, 0x11, 0x0F, 0x01, 0x01}},  // 113 q
    {{0x00, 0x00, 0x16, 0x19, 0x10, 0x10, 0x10, 0x00}},  // 114 r
    {{0x00, 0x00, 0x0E, 0x10, 0x0E, 0x01, 0x1E, 0x00}},  // 115 s
    {{0x08, 0x08, 0x1C, 0x08, 0x08, 0x09, 0x06, 0x00}},  // 116 t
    {{0x00, 0x00, 0x11, 0x11, 0x11, 0x13, 0x0D, 0x00}},  // 117 u
    {{0x00, 0x00, 0x11, 0x11, 0x11, 0x0A, 0x04, 0x00}},  // 118 v
    {{0x00, 0x00, 0x11, 0x11, 0x15, 0x15, 0x0A, 0x00}},  // 119 w
    {{0x00, 0x00, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x00}},  // 120 x
    {{0x00, 0x00, 0x11, 0x11, 0x11, 0x0F, 0x01, 0x0E}},  // 121 y
    {{0x00, 0x00, 0x1F, 0x02, 0x04, 0x08, 0x1F, 0x00}},  // 122 z
    {{0x02, 0x04, 0x04, 0x08, 0x04, 0x04, 0x02, 0x00}},  // 123 {
    {{0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x00}},  // 124 |
    {{0x08, 0x04, 0x04, 0x02, 0x04, 0x04, 0x08, 0x00}},  // 125 }
    {{0x00, 0x00, 0x08, 0x15, 0x02, 0x00, 0x00, 0x00}},  // 126 ~
}};

inline int glyphIndex(char c) {
    const int code = static_cast<unsigned char>(c);
    if (code < kFirstChar || code > kLastChar) {
        return '?' - kFirstChar;
    }
    return code - kFirstChar;
}

inline bool glyphPixel(char c, int x, int y) {
    if (x < 0 || x >= kGlyphWidth || y < 0 || y >= kGlyphHeight) {
        return false;
    }
    const std::uint8_t row = kFont[glyphIndex(c)][y];
    return ((row >> (kGlyphWidth - 1 - x)) & 1) != 0;
}

inline int lineCount(const std::string& text) {
    return 1 + static_cast<int>(std::count(text.begin(), text.end(), '\n'));
}

inline int longestLine(const std::string& text) {
    int longest = 0;
    int current = 0;
    for (char c : text) {
        if (c == '\n') {
            current = 0;
        } else {
            ++current;
            longest = std::max(longest, current);
        }
    }
    return longest;
}

inline int textWidth(const std::string& text, int scale) {
    const int chars = longestLine(text);
    return (chars == 0) ? 0 : (chars * kCharAdvance - 1) * scale;
}

inline int textHeight(const std::string& text, int scale) {
    return (lineCount(text) * kLineAdvance - 2) * scale;
}

inline void drawText(Image& image, int x, int y, const std::string& text, Colour c, int scale = 1) {
    int penX = x;
    int penY = y;
    for (char ch : text) {
        if (ch == '\n') {
            penX = x;
            penY += kLineAdvance * scale;
            continue;
        }
        for (int gy = 0; gy < kGlyphHeight; ++gy) {
            for (int gx = 0; gx < kGlyphWidth; ++gx) {
                if (glyphPixel(ch, gx, gy)) {
                    fillRect(image, makeRect(penX + gx * scale, penY + gy * scale, scale, scale), c);
                }
            }
        }
        penX += kCharAdvance * scale;
    }
}

inline void drawTextCentred(Image& image, int centreX, int y, const std::string& text, Colour c,
                            int scale = 1) {
    drawText(image, centreX - textWidth(text, scale) / 2, y, text, c, scale);
}

inline Rect textBox(int x, int y, const std::string& text, int scale, int padding) {
    return makeRect(x - padding, y - padding, textWidth(text, scale) + 2 * padding,
                    textHeight(text, scale) + 2 * padding);
}

inline double overlapLength(double a0, double a1, double b0, double b1) {
    return std::max(0.0, std::min(a1, b1) - std::max(a0, b0));
}

inline double glyphCoverage(char ch, double left, double top, double size, int px, int py) {
    const int gx0 = static_cast<int>(std::floor((px - left) / size));
    const int gx1 = static_cast<int>(std::floor((px + 1 - left) / size));
    const int gy0 = static_cast<int>(std::floor((py - top) / size));
    const int gy1 = static_cast<int>(std::floor((py + 1 - top) / size));
    double area = 0.0;
    for (int gy = gy0; gy <= gy1; ++gy) {
        for (int gx = gx0; gx <= gx1; ++gx) {
            if (glyphPixel(ch, gx, gy)) {
                const double w = overlapLength(px, px + 1.0, left + gx * size, left + (gx + 1) * size);
                const double h = overlapLength(py, py + 1.0, top + gy * size, top + (gy + 1) * size);
                area += w * h;
            }
        }
    }
    return std::min(area, 1.0);
}

inline void drawTextSmooth(Image& image, double x, double y, const std::string& text, Colour c,
                           double size) {
    if (size <= 0.0) {
        return;
    }
    double penX = x;
    double penY = y;
    for (char ch : text) {
        if (ch == '\n') {
            penX = x;
            penY += kLineAdvance * size;
            continue;
        }
        const int x0 = static_cast<int>(std::floor(penX));
        const int x1 = static_cast<int>(std::ceil(penX + kGlyphWidth * size));
        const int y0 = static_cast<int>(std::floor(penY));
        const int y1 = static_cast<int>(std::ceil(penY + kGlyphHeight * size));
        for (int py = y0; py < y1; ++py) {
            for (int px = x0; px < x1; ++px) {
                if (image.isInside(px, py)) {
                    paintCoverage(image, px, py, c, glyphCoverage(ch, penX, penY, size, px, py));
                }
            }
        }
        penX += kCharAdvance * size;
    }
}

#endif
```

### Line by line

**The font (lines 1–114)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–9 | include guard and `#include` lines | `std::count`, `std::max`, `std::min`, `std::array`, `std::floor`, `std::ceil`, exact-size integers, strings, and the drawing library. |
| 11–12 | `const int kGlyphWidth = 5; const int kGlyphHeight = 8;` | The glyph grid (Section 46.2). |
| 13–14 | `const int kCharAdvance = 6; const int kLineAdvance = 10;` | The pen moves (Section 46.5). |
| 15–16 | `const int kFirstChar = 32; const int kLastChar = 126;` | The printable ASCII characters (Section 46.3). |
| 18 | `const std::array<std::array<std::uint8_t, 8>, 95> kFont = {{` | 95 glyphs, each 8 bytes. The double braces `{{` are the way to fill a `std::array` (which holds a plain array inside) completely and without warnings. |
| 19–113 | `{{0x00, 0x00, ...}},  // 32 space` … `// 126 ~` | One glyph per line, in ASCII order, with a comment naming it. Each glyph is itself a `std::array`, so it gets double braces too. Line 19 + (code − 32) holds the glyph for that code: 'A' (65) is on line 52, 'g' (103) on line 90. |
| 114 | `}};` | End of the table. |

**Reading the font (lines 116–130)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 116–117 | `inline int glyphIndex(char c) { const int code = static_cast<unsigned char>(c);` | The character's code, 0–255 (Section 46.3, ⚠️). |
| 118–120 | `if (code < kFirstChar \|\| code > kLastChar) { return '?' - kFirstChar; }` | Anything outside the font becomes '?' (63 − 32 = 31). |
| 121–122 | `return code - kFirstChar;` `}` | The glyph number. |
| 124–127 | `inline bool glyphPixel(char c, int x, int y) { if (x < 0 \|\| x >= kGlyphWidth \|\| y < 0 \|\| y >= kGlyphHeight) { return false; }` | Outside the grid: always off (Section 46.4). |
| 128–130 | `const std::uint8_t row = kFont[glyphIndex(c)][y]; return ((row >> (kGlyphWidth - 1 - x)) & 1) != 0;` `}` | Take the row's byte, shift bit (4 − x) down, and mask it. |

**Measuring text (lines 132–157)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 132–134 | `inline int lineCount(const std::string& text) { return 1 + static_cast<int>(std::count(text.begin(), text.end(), '\n')); }` | Lines = new-line characters + 1. `std::count` counts how often a value appears. |
| 136–148 | `inline int longestLine(const std::string& text) { int longest = 0; int current = 0; for (char c : text) { if (c == '\n') { current = 0; } else { ++current; longest = std::max(longest, current); } } return longest; }` | The number of characters in the longest line: count up, start again at each new line, remember the biggest count. |
| 150–153 | `inline int textWidth(const std::string& text, int scale) { const int chars = longestLine(text); return (chars == 0) ? 0 : (chars * kCharAdvance - 1) * scale; }` | Section 46.5's width. An empty text is 0 wide (not −1). |
| 155–157 | `inline int textHeight(const std::string& text, int scale) { return (lineCount(text) * kLineAdvance - 2) * scale; }` | Section 46.5's height. |

**Drawing in blocks (lines 159–187)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 159–161 | `inline void drawText(Image& image, int x, int y, const std::string& text, Colour c, int scale = 1) { int penX = x; int penY = y;` | (x, y) is the **top-left** corner of the first character. The pen starts there. |
| 162–167 | `for (char ch : text) { if (ch == '\n') { penX = x; penY += kLineAdvance * scale; continue; }` | A new line: back to the left edge, one line down. |
| 168–174 | `for (int gy = 0; ...) { for (int gx = 0; ...) { if (glyphPixel(ch, gx, gy)) { fillRect(image, makeRect(penX + gx * scale, penY + gy * scale, scale, scale), c); } } }` | Every "on" font pixel becomes a scale × scale square (Section 46.6). `fillRect` clips at the picture's edges (Chapter 19), so text may run off the picture safely. |
| 175–177 | `penX += kCharAdvance * scale;` `}` `}` | Move the pen to the next character. |
| 179–182 | `inline void drawTextCentred(Image& image, int centreX, int y, const std::string& text, Colour c, int scale = 1) { drawText(image, centreX - textWidth(text, scale) / 2, y, text, c, scale); }` | Start half a text-width left of the centre. |
| 184–187 | `inline Rect textBox(int x, int y, const std::string& text, int scale, int padding) { return makeRect(x - padding, y - padding, textWidth(text, scale) + 2 * padding, textHeight(text, scale) + 2 * padding); }` | The rectangle around a text, with a margin on every side (Section 46.8). |

**Drawing smoothly (lines 189–239)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 189–191 | `inline double overlapLength(double a0, double a1, double b0, double b1) { return std::max(0.0, std::min(a1, b1) - std::max(a0, b0)); }` | How long two intervals overlap; 0 if they do not (Section 46.7). |
| 193–197 | `inline double glyphCoverage(char ch, double left, double top, double size, int px, int py) { const int gx0 = static_cast<int>(std::floor((px - left) / size)); ... gy1 = ...;` | The font columns and rows that can touch pixel (px, py). `std::floor` (not a plain cast) rounds negative numbers down too. |
| 198–207 | `double area = 0.0; for (gy ...) { for (gx ...) { if (glyphPixel(ch, gx, gy)) { const double w = overlapLength(px, px + 1.0, left + gx * size, left + (gx + 1) * size); const double h = ...; area += w * h; } } }` | Add the overlap area of every "on" font square. Cells outside the grid are off (Section 46.4). |
| 208–209 | `return std::min(area, 1.0);` `}` | Never more than the whole pixel (tiny rounding errors could make it 1.0000001). |
| 211–215 | `inline void drawTextSmooth(Image& image, double x, double y, const std::string& text, Colour c, double size) { if (size <= 0.0) { return; }` | Smooth text: `size` is the size of one font pixel. A size of 0 or less draws nothing (and avoids dividing by 0). |
| 216–223 | `double penX = x; double penY = y; for (char ch : text) { if (ch == '\n') { ... } ` | The pen and new lines, as in `drawText`, but with `double`s. |
| 224–227 | `const int x0 = static_cast<int>(std::floor(penX)); const int x1 = static_cast<int>(std::ceil(penX + kGlyphWidth * size)); ...` | The box of image pixels that this glyph can touch. |
| 228–234 | `for (int py = y0; py < y1; ++py) { for (int px = x0; px < x1; ++px) { if (image.isInside(px, py)) { paintCoverage(image, px, py, c, glyphCoverage(ch, penX, penY, size, px, py)); } } }` | Paint each pixel by its coverage (Chapter 27: 0 = skip, 1 = set, between = blend). |
| 235–239 | `penX += kCharAdvance * size;` `}` `}` `#endif` | Next character; end of the header. |

---

## Code, part 2: text on pictures

File: `ch46/text.cpp`

```cpp
#include <iostream>
#include <string>
#include "font.h"
#include "deflate.h"

void printGlyph(char c) {
    std::cout << "'" << c << "':";
    for (int y = 0; y < kGlyphHeight; ++y) {
        std::cout << " " << hexByte(kFont[glyphIndex(c)][y]);
    }
    std::cout << "\n";
    for (int y = 0; y < kGlyphHeight; ++y) {
        std::cout << "    ";
        for (int x = 0; x < kGlyphWidth; ++x) {
            std::cout << (glyphPixel(c, x, y) ? '#' : '.');
        }
        std::cout << "\n";
    }
}

void printText(const std::string& text) {
    Image picture(textWidth(text, 1), textHeight(text, 1), colours::white);
    drawText(picture, 0, 0, text, colours::black);
    for (int y = 0; y < picture.height(); ++y) {
        for (int x = 0; x < picture.width(); ++x) {
            std::cout << (picture.getPixel(x, y).r == 0 ? '#' : ' ');
        }
        std::cout << "\n";
    }
}

int countDark(const Image& picture) {
    int count = 0;
    for (int y = 0; y < picture.height(); ++y) {
        for (int x = 0; x < picture.width(); ++x) {
            count += (picture.getPixel(x, y).r < 128) ? 1 : 0;
        }
    }
    return count;
}

int main() {
    printGlyph('A');
    printGlyph('g');
    printText("Hello, world!");

    const std::string two = "Line one\nand two";
    std::cout << "\"Hello, world!\": " << textWidth("Hello, world!", 1) << " x "
              << textHeight("Hello, world!", 1) << " pixels; at scale 3: "
              << textWidth("Hello, world!", 3) << " x " << textHeight("Hello, world!", 3) << "\n";
    std::cout << "two lines: " << lineCount(two) << " lines, " << textWidth(two, 1) << " x "
              << textHeight(two, 1) << " pixels\n";
    std::cout << "a character outside the font is drawn as '?': glyph " << glyphIndex('\t')
              << " = glyph " << glyphIndex('?') << "\n";

    std::cout << "'I' at (0.3, 0.0), size 2.5: coverage of pixel (2, 0) = "
              << glyphCoverage('I', 0.3, 0.0, 2.5, 2, 0) << ", of pixel (2, 2) = "
              << glyphCoverage('I', 0.3, 0.0, 2.5, 2, 2) << ", of pixel (3, 0) = "
              << glyphCoverage('I', 0.3, 0.0, 2.5, 3, 0) << "\n";

    Image sheet(16 * kCharAdvance * 3 + 12, 6 * kLineAdvance * 3 + 12, colours::white);
    for (int code = kFirstChar; code <= kLastChar; ++code) {
        const int i = code - kFirstChar;
        drawText(sheet, 6 + (i % 16) * kCharAdvance * 3, 6 + (i / 16) * kLineAdvance * 3,
                 std::string(1, static_cast<char>(code)), colours::black, 3);
    }
    std::cout << "font sheet: " << sheet.width() << " x " << sheet.height() << ", "
              << countDark(sheet) << " dark pixels\n";

    Image sizes(300, 125, colours::white);
    const double steps[5] = {1.0, 1.5, 2.0, 3.0, 4.5};
    double y = 6.0;
    for (double s : steps) {
        drawTextSmooth(sizes, 6.0, y, "Smooth " + std::to_string(s).substr(0, 3), colours::black, s);
        y += kLineAdvance * s;
    }

    Image label(300, 200);
    for (int py = 0; py < 200; ++py) {
        const Colour c = lerpColour(Colour{40, 90, 200}, Colour{250, 200, 120}, py / 199.0);
        for (int px = 0; px < 300; ++px) {
            label.setPixel(px, py, c);
        }
    }
    const std::string title = "Evening sky";
    drawTextCentred(label, 152, 22, title, Colour{20, 30, 60}, 4);
    drawTextCentred(label, 150, 20, title, colours::white, 4);
    const std::string caption = "300 x 200 pixels\nsaved as a PNG";
    const Rect box = textBox(20, 150, caption, 2, 6);
    fillRectAlpha(label, box, colours::black, 0.5);
    drawText(label, 20, 150, caption, colours::white, 2);
    std::cout << "caption box: " << box.x0 << ", " << box.y0 << " to " << box.x1 << ", " << box.y1
              << "\n";

    if (!savePNGCompressed(sheet, "font.png") || !savePNGCompressed(sizes, "sizes.png") ||
        !savePNGCompressed(label, "label.png")) {
        std::cout << "could not write the files\n";
        return 1;
    }
    std::cout << "wrote font.png, sizes.png and label.png\n";
    return 0;
}
```

Build and run it from the `code/ch46` folder:

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common text.cpp -o text
./text
```

### Line by line

**Helpers (lines 1–40)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–4 | the `#include` lines | Printing, strings, the font (with the drawing library) and `deflate.h` (with the file formats) for `savePNGCompressed`. The two families of headers work side by side, as since Chapter 39. |
| 6–19 | `void printGlyph(char c) { ... hexByte(kFont[glyphIndex(c)][y]) ... (glyphPixel(c, x, y) ? '#' : '.') ... }` | Print a glyph's 8 bytes in hex, then the glyph as a little picture (Section 46.2). |
| 21–30 | `void printText(const std::string& text) { Image picture(textWidth(text, 1), textHeight(text, 1), colours::white); drawText(picture, 0, 0, text, colours::black); ... }` | Draw a text into a picture of exactly its size, then print the picture: `#` for black, a space for white. |
| 32–40 | `int countDark(const Image& picture) { ... (picture.getPixel(x, y).r < 128) ? 1 : 0 ... }` | Count the dark pixels (red below 128). |

**Glyphs, sizes and coverage (lines 43–59)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 43–45 | `printGlyph('A'); printGlyph('g'); printText("Hello, world!");` | Sections 46.2 and 46.5. |
| 47–52 | `const std::string two = "Line one\nand two"; std::cout << ... textWidth("Hello, world!", 1) ... textHeight(two, 1) ...` | The sizes of Section 46.5. `\n` inside the string is the new-line character. |
| 53–54 | `std::cout << ... glyphIndex('\t') << " = glyph " << glyphIndex('?') << "\n";` | A tab (code 9) gets the '?' glyph (Section 46.3). |
| 56–59 | `std::cout << "'I' at (0.3, 0.0), size 2.5: coverage of pixel (2, 0) = " << glyphCoverage('I', 0.3, 0.0, 2.5, 2, 0) << ...` | The worked example of Section 46.7. |

**The three pictures (lines 61–102)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 61 | `Image sheet(16 * kCharAdvance * 3 + 12, 6 * kLineAdvance * 3 + 12, colours::white);` | Room for 16 characters × 6 rows at scale 3, plus a 6-pixel margin on each side: 300 × 192. |
| 62–66 | `for (int code = kFirstChar; code <= kLastChar; ++code) { const int i = code - kFirstChar; drawText(sheet, 6 + (i % 16) * kCharAdvance * 3, 6 + (i / 16) * kLineAdvance * 3, std::string(1, static_cast<char>(code)), colours::black, 3); }` | Each character in its own cell: column i % 16, row i / 16 (Chapter 6's index, backwards). `std::string(1, c)` is a text of one character. |
| 67–68 | `std::cout << "font sheet: " << ... countDark(sheet) << " dark pixels\n";` | 10,080 (Section 46.6). |
| 70–76 | `Image sizes(300, 125, colours::white); const double steps[5] = {1.0, 1.5, 2.0, 3.0, 4.5}; double y = 6.0; for (double s : steps) { drawTextSmooth(sizes, 6.0, y, "Smooth " + std::to_string(s).substr(0, 3), colours::black, s); y += kLineAdvance * s; }` | Five lines of smooth text, each at its own size. `std::to_string(1.5)` gives "1.500000"; `substr(0, 3)` keeps "1.5". Each line moves down by its own line advance. |
| 78–84 | `Image label(300, 200); for (...) { const Colour c = lerpColour(...py / 199.0); for (...) { label.setPixel(px, py, c); } }` | Chapter 39's sky gradient as the background. |
| 85–87 | `const std::string title = "Evening sky"; drawTextCentred(label, 152, 22, title, Colour{20, 30, 60}, 4); drawTextCentred(label, 150, 20, title, colours::white, 4);` | A title with a shadow (Section 46.8). Scale 4: 260 pixels wide, centred at x = 150. |
| 88–91 | `const std::string caption = "300 x 200 pixels\nsaved as a PNG"; const Rect box = textBox(20, 150, caption, 2, 6); fillRectAlpha(label, box, colours::black, 0.5); drawText(label, 20, 150, caption, colours::white, 2);` | A two-line caption on a half-transparent dark box. |
| 92–93 | `std::cout << "caption box: " << box.x0 << ... << box.y1 << "\n";` | The box of Section 46.8. |
| 95–99 | `if (!savePNGCompressed(sheet, "font.png") \|\| ... ) { ... return 1; }` | Save all three as compressed PNG files (Chapter 45). |
| 100–102 | `std::cout << "wrote font.png, sizes.png and label.png\n";` `return 0;` `}` | Done. |

### What you should see

```
'A': 0E 11 11 1F 11 11 11 00
    .###.
    #...#
    #...#
    #####
    #...#
    #...#
    #...#
    .....
'g': 00 00 0F 11 11 0F 01 0E
    .....
    .....
    .####
    #...#
    #...#
    .####
    ....#
    .###.
#   #        ##    ##                                        ##       #   #  
#   #         #     #                                         #       #   #  
#   #  ###    #     #    ###              #   #  ###  # ##    #    ## #   #  
##### #   #   #     #   #   #             #   # #   # ##  #   #   #  ##   #  
#   # #####   #     #   #   #             # # # #   # #       #   #   #   #  
#   # #       #     #   #   #  ##         # # # #   # #       #   #   #      
#   #  ###   ###   ###   ###    #          # #   ###  #      ###   ####   #  
                               #                                             
"Hello, world!": 77 x 8 pixels; at scale 3: 231 x 24
two lines: 2 lines, 47 x 18 pixels
a character outside the font is drawn as '?': glyph 31 = glyph 31
'I' at (0.3, 0.0), size 2.5: coverage of pixel (2, 0) = 0.2, of pixel (2, 2) = 0.1, of pixel (3, 0) = 1
font sheet: 300 x 192, 10080 dark pixels
caption box: 14, 144 to 216, 192
wrote font.png, sizes.png and label.png
```

`font.png` shows all 95 characters:

```
     ! " # $ % & ' ( ) * + , - . /
   0 1 2 3 4 5 6 7 8 9 : ; < = > ?
   @ A B C D E F G H I J K L M N O
   P Q R S T U V W X Y Z [ \ ] ^ _
   ` a b c d e f g h i j k l m n o
   p q r s t u v w x y z { | } ~
```

---

## Small examples

### Example 1 — The bytes of 'T'

```
   #####   0x1F
   ..#..   0x04   (and five more rows of 0x04)
   .....   0x00
```

'T' = `1F 04 04 04 04 04 04 00`.

### Example 2 — Which glyph is '0'?

'0' has code 48 → glyph 48 − 32 = **16**: the first glyph of the second row in `font.png`.

### Example 3 — Is pixel (4, 3) of 'A' on?

Row 3 = 0x1F = 1 1111; x = 4 → bit 0 → 0x1F & 1 = **1** → on.

### Example 4 — The width of a number

"2024" at scale 2: (4 × 6 − 1) × 2 = **46** pixels wide, (10 − 2) × 2 = **16** tall.

### Example 5 — Coverage on a half-pixel

A glyph at (0.5, 0.0) with size 1: font column 0 covers x 0.5–1.5. Image pixel 0 gets half of it (**0.5**), pixel 1 the other half. A whole-pixel position gives sharp text; a half-pixel position gives grey, blurry edges. Draw small text at whole-number positions.

---

## Common mistakes

⚠️ **Reading outside the table** — characters below 32 or above 126 (and negative `char`s). Always go through `glyphIndex`.

⚠️ **Bit order** — column 0 is the **highest** of the 5 bits (bit 4), not bit 0. Mixing this up mirrors every letter.

⚠️ **No gap between characters** — with an advance of 5, the letters touch. The advance must be the glyph width **plus** the gap.

⚠️ **Forgetting the descender in the height** — the text box must include row 7, or the tails of g, p and y stick out.

⚠️ **Drawing small smooth text at half-pixel positions** — it looks blurred (Example 5).

⚠️ **White text on a light picture** — use a shadow or a box (Section 46.8).

---

## Practice

🏋️ **1.** Work out the 8 bytes of 'L' and of 'H' by hand. Check them against the table.

🏋️ **2.** What are `textWidth` and `textHeight` of "OK" at scale 2? And of "a\nbb\nccc" at scale 1?

🏋️ **3.** Write `drawTextRight(image, rightX, y, text, c, scale)`, which ends the text at `rightX` (useful for columns of numbers).

🏋️ **4.** Make **outlined** text: draw the text in black at the 8 positions around (x, y) (one pixel away, scale 1), then in white at (x, y).

🏋️ **5.** Make **bold** text: draw each character twice, the second time one pixel to the right. What happens to the gap between characters? How would you fix it?

🏋️ **6.** Draw a bar chart: five bars with heights 40, 75, 60, 90, 30, each with its value written above it with `drawTextCentred`.

🏋️ **7.** Show that `drawTextSmooth` with size 1.0 at a whole-number position gives exactly the same pixels as `drawText` with scale 1.

🏋️ **8.** Design your own glyph for '£' (not in ASCII). How would you add it to the font without changing the 95 glyphs?

---

## Answers

**1.**
> 'L': `10 10 10 10 10 10 1F 00` (five rows with only column 0 = 16 = 0x10, then the full bottom row 0x1F).
> 'H': `11 11 11 1F 11 11 11 00`.

**2.**
> "OK", scale 2: (2 × 6 − 1) × 2 = **22** wide, (10 − 2) × 2 = **16** tall.
> "a\nbb\nccc": the longest line has 3 characters → 3 × 6 − 1 = **17**; 3 lines → 3 × 10 − 2 = **28**.

**3.**

```cpp
void drawTextRight(Image& image, int rightX, int y, const std::string& text, Colour c, int scale) {
    drawText(image, rightX - textWidth(text, scale), y, text, c, scale);
}
```

> (For several lines, each line would need its own width; this version right-aligns the longest line.)

**4.**

```cpp
for (int dy = -1; dy <= 1; ++dy) {
    for (int dx = -1; dx <= 1; ++dx) {
        if (dx != 0 || dy != 0) {
            drawText(image, x + dx, y + dy, text, colours::black);
        }
    }
}
drawText(image, x, y, text, colours::white);
```

**5.**
> Each glyph becomes 6 pixels wide, so the 1-pixel gap is filled and the letters touch. Fix it with a bigger advance (7) for bold text — for example, draw character by character with your own pen that moves 7 pixels.

**6.**

```cpp
const int values[5] = {40, 75, 60, 90, 30};
for (int i = 0; i < 5; ++i) {
    const int left = 20 + i * 50;
    const int top = 180 - values[i];
    fillRect(chart, makeRect(left, top, 30, values[i]), Colour{70, 130, 200});
    drawTextCentred(chart, left + 15, top - 12, std::to_string(values[i]), colours::black);
}
```

> (For a 280 × 200 white picture `chart`. The text goes 12 pixels above the bar: 8 for the glyph, 4 for a gap.)

**7.**
> With size 1 and a whole-number pen position, every font square **is** exactly one image pixel. Its coverage is 1 where the font pixel is on and 0 everywhere else, and `paintCoverage` sets coverage-1 pixels to the colour without blending — just like `fillRect` with a 1 × 1 rectangle. (You can check it with `samePictures` from Chapter 39.)

**8.**
> For example `.##.. / #..#. / #.... / ###.. / #.... / #...# / #####` (+ an empty row) = `0C 12 10 1C 10 11 1F 00`. Since '£' has no ASCII code, use one of the unused codes, for example 127: add a 96th glyph to `kFont` (size 96), and change `kLastChar` to 127. Then write `std::string(1, static_cast<char>(127))` wherever you want a '£'.

---

## Summary

🧠 A **glyph** is the shape of one character; a **bitmap font** stores glyphs as grids of on/off pixels; an **outline font** stores curves.

🧠 Our font: **5 × 8** pixels per glyph, one byte per row (bit 4 = left), 95 glyphs for ASCII **32–126** = **760 bytes**. Anything else is drawn as '?'.

🧠 Layout: advance **6** across, **10** down. Width = (chars × 6 − 1) × scale, height = (lines × 10 − 2) × scale.

🧠 `drawText` draws each "on" font pixel as a scale × scale square: sharp, whole-number sizes only.

🧠 `drawTextSmooth` treats each font pixel as a square of any size and paints the **exact overlap area** as coverage: smooth text at any size and position.

🧠 Shadows and half-transparent boxes keep text readable on any picture.

---

## Next chapter

Part 7 begins: **image processing**. Until now we made pictures; now we change them. In Chapter 47 we meet **point operations** — changes that look at one pixel at a time: brightness, contrast, invert, and threshold (black or white). We will see them as **curves** that map each old value to a new one, build them as fast 256-entry tables, and try them on our pictures and on any PNG we can now load.
