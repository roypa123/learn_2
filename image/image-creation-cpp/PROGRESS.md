# Progress

Read `MASTER_PLAN.md` first. Then continue from **Next up**.

## Next up

**Part 3, Chapter 17 — Gamma and sRGB: why 128 is not half bright.**
File: `part-03-mathematics-of-colour/ch17-gamma-and-srgb.md`, code in `code/ch17/` and a new `common/srgb.h`.
It should cover: the eye's non-linear response (Weber-like: we notice ratios), why storing bytes "gamma
encoded" uses the 256 levels better, the exact sRGB formulas (decode: v ≤ 0.04045 ? v/12.92 :
((v+0.055)/1.055)^2.4 ; encode: l ≤ 0.0031308 ? 12.92 l : 1.055 l^(1/2.4) − 0.055) with worked numbers
(128 → 0.2158 ≈ 22 %, promised in Ch 5 §5.5 and Ch 15 §15.5), the simple gamma 2.2 approximation,
`std::pow` from <cmath>, a 256-entry lookup table for speed, **linear-light** blending (lerp in linear
space vs. byte space: the dark band in the middle of a red→green gradient), true **luminance** vs luma
(Ch 15 promised), and a test image: a checkerboard of 0/255 next to solid 128 and solid 188 (which matches
when viewed from afar). Functions: `srgbToLinear(double)`, `linearToSrgb(double)`, `toLinear(ColourF)`,
`fromLinear(ColourF)`, `lerpLinear`, `luminance(Colour)`.

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

**Parts 1 and 2 complete.** Part 3 in progress. Total so far: ~84,300 words.

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

Chapter programs from Ch 11 on use `#include "image.h"` and are built with `g++ -std=c++17 -Wall -Wextra -O2 -I ../common`.

## Ideas and promises already made to the reader (keep them!)

Earlier chapters point forward to these. The later chapters must deliver them:

- (Ch 13 and 14 delivered: rounding with floor, graphs, any-width gradients, clamping, overflow.)
- Ch 20: line drawing fills the gaps in the Ch 13 graph of y = x².
- Ch 27 / 50: averages of many colours (Ch 14 §14.9).
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
