# Progress

Read `MASTER_PLAN.md` first. Then continue from **Next up**.

## Next up

**Part 4, Chapter 21 — Lines, part 2: Bresenham's algorithm.**
File: `part-04-drawing-shapes/ch21-lines-part-2-bresenham.md`, code in `code/ch21/`. Append the new functions
to the END of `common/lines.h` (before `#endif`; lines.h is the line-drawing topic header, 43 lines now).
It should cover: the decision idea (at each column, stay on the row or step one row), the error term
(distance of the true line from the pixel centre), removing fractions by multiplying by dx (and by 2 for
the 0.5 test), the integer recurrences err += 2·dy, err −= 2·dx, a full worked table for (0,0)→(5,2) and
(0,0)→(2,6), handling all 8 octants with sx/sy = ±1 and the "both axes" form (err = dx − dy) that works
in every direction with one loop, comparing pixels with DDA (identical or differing at .5 ties), skipping
the last pixel for polylines (Ch 20 §20.6 promise), thick lines by drawing a small square per pixel,
dashed lines (count steps), and a speed note. Images: the Ch 20 fan with Bresenham, dashed/thick lines.

## Chapters done

| Ch | File | Words | Code |
|---|---|---|---|
| 1 | part-01-what-is-an-image/ch01-how-to-use-this-book.md | 3,739 | code/ch01/check.cpp |
| 2 | part-01-what-is-an-image/ch02-light-eyes-and-pixels.md | 3,771 | code/ch02/number_picture.cpp |
| 3 | part-01-what-is-an-image/ch03-grids-and-coordinates.md | 4,809 | code/ch03/grid.cpp |
| 4 | part-01-what-is-an-image/ch04-bits-bytes-and-hex.md | 5,094 | code/ch04/bytes.cpp |
| 5 | part-01-what-is-an-image/ch05-how-colour-works-rgb.md | 4,606 | code/ch05/colours.cpp |
| 6 | part-01-what-is-an-image/ch06-an-image-inside-memory.md | 4,920 | code/ch06/buffer.cpp |
| 7 | part-02-first-image-files/ch07-writing-files-byte-by-byte.md | 5,123 | code/ch07/bytes_file.cpp |
| 8 | part-02-first-image-files/ch08-the-ppm-text-format-p3.md | 5,345 | code/ch08/ppm_p3.cpp |
| 9 | part-02-first-image-files/ch09-the-ppm-binary-format-p6.md | 4,758 | code/ch09/ppm_p6.cpp |
| 10 | part-02-first-image-files/ch10-grey-and-black-white-pgm-pbm.md | 5,399 | code/ch10/pgm_pbm.cpp |
| 11 | part-02-first-image-files/ch11-building-an-image-class.md | 5,029 | code/common/image.h (lines 1–89), code/ch11/use_image.cpp |
| 12 | part-02-first-image-files/ch12-reading-a-ppm-file.md | 6,544 | code/common/image.h (lines 91–213), code/ch12/read_ppm.cpp |
| 13 | part-03-mathematics-of-colour/ch13-gradients-and-linear-interpolation.md | 6,571 | code/common/image.h (lines 215–232), code/ch13/gradients.cpp |
| 14 | part-03-mathematics-of-colour/ch14-colours-as-vectors.md | 6,270 | code/common/colourf.h (new, 55 lines), code/ch14/colour_maths.cpp |
| 15 | part-03-mathematics-of-colour/ch15-turning-colour-into-grey-luminance.md | 5,186 | code/common/grey.h (new, 51 lines), code/ch15/to_grey.cpp |
| 16 | part-03-mathematics-of-colour/ch16-hue-saturation-value-hsv-hsl.md | 7,210 | code/common/hsv.h (new, 106 lines), code/ch16/hsv_hsl.cpp |
| 17 | part-03-mathematics-of-colour/ch17-gamma-and-srgb.md | 5,827 | code/common/srgb.h (new, 57 lines), code/ch17/gamma.cpp |
| 18 | part-03-mathematics-of-colour/ch18-transparency-alpha-and-blending.md | 5,802 | code/common/alpha.h (new, 60 lines), code/ch18/alpha.cpp |

**Parts 1, 2 and 3 complete.** Part 4 in progress. Total so far: ~108,000 words.

## The shared library: `code/common/image.h`

It grows over the book. Each chapter that adds to it says where to add the code, and gives the **real line
numbers** in the finished file. Before you add anything, run `cat -n code/common/image.h` so the new line
numbers are right. Free functions must be `inline`. Current contents:

- lines 1–89 (Ch 11): include guard, `struct Colour` (defaults 0), `namespace colours` (8 corner colours),
  `class Image` (width, height, isInside, setPixel, getPixel [black outside], clear, data, savePPM [P6], private index)
- lines 91–213 (Ch 12): `readFileBytes`, `isSpace`, `skipSpaceAndComments`, `readNumber`, `scaleToByte`, `loadPPM` (P3 + P6, maxval ≤ 255)
- lines 215–232 (Ch 13): `lerp`, `lerpByte` (clamps, rounds), `lerpColour`
- line 234: `#endif`

`code/common/colourf.h` (Ch 14, includes `image.h`): `struct ColourF` (doubles 0..1), operators `+ - * /`
(scalar both sides, and colour×colour), `toColourF`, `toByte` (std::clamp + round), `toColour`, `length`.
**Rule from Ch 14 on:** each new topic gets its own header that includes the previous ones, so existing
line numbers never move. Append to the end of a header only when the topic really belongs there.

`code/common/grey.h` (Ch 15, includes `colourf.h`): `luma` (Rec. 709 weights on gamma-encoded values —
deliberately called *luma*, true luminance comes in Ch 17), `plainAverage`, `greyByte`, `toGrey`,
`desaturate` (lerp toward own grey), `saveGreyPGM` (P5).

`code/common/hsv.h` (Ch 16, includes `colourf.h`): `struct HSV {h,s,v}`, `struct HSL {h,s,l}` (h in
degrees 0–360), `wrapHue`, `hueOf`, `rgbToHsv`, `rgbToHsl`, `hueToRgb`, `hsvToRgb`, `hslToRgb`, `shiftHue`.

`code/common/srgb.h` (Ch 17, includes `colourf.h`): `srgbToLinear`, `linearToSrgb` (clamps), `makeLinearTable`,
`linearTable` (static 256-entry table), `toLinear(Colour)`, `fromLinear(ColourF)`, `lerpLinear`, `luminance` (true, linear).

`code/common/alpha.h` (Ch 18, includes `srgb.h`): `struct ColourFA {r,g,b,a}`, `withAlpha`, `overStraight`,
`premultiply`, `unpremultiply`, `overPremultiplied`, `blendOver(dst, src, alpha)` (linear light, dst first!),
`blendPixel(Image&, x, y, src, alpha)`.

`code/common/draw.h` (Ch 19, includes `alpha.h`): `struct Rect {x0,y0,x1,y1}` (half-open), `fromCorners`,
`makeRect`, `rectWidth`, `rectHeight`, `isEmpty`, `contains`, `intersect`, `clipToImage`, `fillRect`,
`fillRectAlpha`, `strokeRect` (inside, corners once; overlaps if 2t > side — Ch 19 P7 fix).

`code/common/lines.h` (Ch 20, includes `draw.h`): `roundToInt` (floor(v+0.5)), `drawLineNaive`, `drawLineDDA`
(both endpoints included).

Header include chain so far: image.h ← colourf.h ← {grey.h, hsv.h, srgb.h ← alpha.h ← draw.h ← lines.h}.
Note: programs that need HSV colours include `hsv.h` as well (it is not in the draw chain).

Chapter programs from Ch 11 on use `#include "image.h"` and are built with `g++ -std=c++17 -Wall -Wextra -O2 -I ../common`.

## Ideas and promises already made to the reader (keep them!)

Earlier chapters point forward to these. The later chapters must deliver them:

- (Ch 13 and 14 delivered: rounding with floor, graphs, any-width gradients, clamping, overflow.)
- Ch 20: line drawing fills the gaps in the Ch 13 graph of y = x².
- Ch 27 / 35 / 50: averages of many colours (Ch 14 §14.9) — do them in **linear light** (Ch 17 Ex 1) and with premultiplied alpha (Ch 18 §18.6); alpha = coverage (Ch 18 §18.2).
- Ch 42: PNG with RGBA to really store transparency (Ch 18 §18.8). Ch 67: painter's algorithm (Ch 18 §18.4). Ch 80: fades (Ch 18 Ex 3).
- Ch 47: invert via remap backwards (Ch 13 Ex 4); Ch 68/73: lighting = colour × colour (Ch 14 §14.5).
- Ch 15: turning colour into grey (PGM output).
- Ch 17: why (128,128,128) is only ~22 % of white's light (gamma).
- Ch 19+: drawing. Ch 22: circles using √(dx² + dy²) and pixel centres (Ch 10 already drew a disk with them).
- Ch 25: flood fill with 4/8 neighbours; masks.
- Ch 27: many small masks for smooth edges.
- Ch 35: "nearest neighbour" (viewers that blur when zooming).
- Ch 36: BMP bottom-up rows, **BGR** order (Ch 12 P5 swaps R and B), rows padded to a multiple of 4,
  little-endian (Ch 4 P8 `78 56 34 12`, Ch 9 §9.8).
- Ch 47: invert (`255 − v`); Ch 12 already does a negative.
- Ch 50: better choices than black for pixels outside the edge (getPixel returns black).
- Ch 52: colour distance in the RGB cube for dithering.
- Ch 54: our own random numbers (we never use `<random>`).
- The allowed header list is in Ch 1 §1.2 (`<climits>` was also used in Ch 1).

## Notes

- No compiler was installed on the authoring machine (as of Ch 12), so the code was checked by hand, not compiled.
  The code blocks inside the chapters were diffed against the files in `code/`. Compile everything in `code/`
  with `g++ -std=c++17 -Wall -Wextra` when a compiler is available.
- Watch for line-number drift in the tables: write the code file first, run `cat -n`, then write the table.
