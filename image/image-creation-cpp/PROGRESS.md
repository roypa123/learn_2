# Progress

Read `MASTER_PLAN.md` first. Then continue from **Next up**.

## Next up

**Part 2, Chapter 7 — Writing files byte by byte.**
File: `part-02-first-image-files/ch07-writing-files-byte-by-byte.md`, code in `code/ch07/`.
It should cover: `std::ofstream` with `std::ios::binary`, `put`/`write`, `reinterpret_cast<const char*>`,
text vs binary mode (the `\n` → `\r\n` problem on Windows), checking that a file opened, file size,
and a small program that reads the bytes back and prints them in hex (reuse `toHex` from Ch 4).
Chapter 8 then writes the first real image: a 3 × 2 P3 PPM (red, green, blue / yellow, white, black),
using the pixel buffer and `index = y × width + x` from Ch 6.

## Chapters done

| Ch | File | Words | Code |
|---|---|---|---|
| 1 | part-01-what-is-an-image/ch01-how-to-use-this-book.md | 3,739 | code/ch01/check.cpp |
| 2 | part-01-what-is-an-image/ch02-light-eyes-and-pixels.md | 3,771 | code/ch02/number_picture.cpp |
| 3 | part-01-what-is-an-image/ch03-grids-and-coordinates.md | 4,809 | code/ch03/grid.cpp |
| 4 | part-01-what-is-an-image/ch04-bits-bytes-and-hex.md | 5,094 | code/ch04/bytes.cpp |
| 5 | part-01-what-is-an-image/ch05-how-colour-works-rgb.md | 4,606 | code/ch05/colours.cpp |
| 6 | part-01-what-is-an-image/ch06-an-image-inside-memory.md | 4,920 | code/ch06/buffer.cpp |

**Part 1 complete.** Total so far: ~26,900 words.

## Ideas and promises already made to the reader (keep them!)

Earlier chapters point forward to these. The later chapters must deliver them:

- Ch 13: exact rounding, including negative numbers; graphing with "maths y" flipped.
- Ch 14: clamping to stop wrap-around; `std::clamp`; overflow.
- Ch 17: why (128,128,128) is only ~22 % of white's light (gamma).
- Ch 22: circles using √(dx² + dy²) and pixel centres (x + 0.5, y + 0.5).
- Ch 25: flood fill with 4/8 neighbours.
- Ch 35: "nearest neighbour" (viewers that blur when zooming).
- Ch 36: BMP bottom-up rows, BGR order, rows padded to a multiple of 4, little-endian (Ch 4 practice 8 showed `78 56 34 12`).
- Ch 47: invert (`255 − v`), photo negative.
- Ch 52: colour distance in the RGB cube for dithering.
- Ch 54: our own random numbers (we never use `<random>`).
- The allowed header list is in Ch 1 §1.2 (`<climits>` was also used in Ch 1).

## Shared helpers so far

- `toHex(std::uint8_t)` — Ch 4 (reused in 5, 6)
- `isInside(x, y, width, height)` — Ch 3 (reused in 6)
- `struct Colour { std::uint8_t r, g, b; }` — Ch 5
- `setPixel(pixels, width, height, x, y, r, g, b)` with bounds check — Ch 6

## Notes

- No compiler was installed on the authoring machine when Part 1 was written, so the code was checked by hand,
  not compiled. Compile everything in `code/` with `g++ -std=c++17 -Wall -Wextra` when a compiler is available.
