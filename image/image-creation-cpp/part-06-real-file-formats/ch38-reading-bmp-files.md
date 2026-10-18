# Chapter 38 — Reading BMP Files

> **Part 6 · Chapter 38 of 82**
> **You need:** Chapters 1–37 (especially 12, 36 and 37) · **You will make:** `bmpload.h` (`bmpProblem`, `decodeBMP` and `loadBMP`), a program that tests the reader with good, top-down, 32-bit and **broken** files, and `heart-small.bmp` and `heart-flipped.bmp` — made by loading a BMP, changing it, and saving it again

---

## What you will learn

- Why a **reader** is harder than a writer: it must handle files made by **other** programs, and broken files too.
- The golden rule: **never trust a file**.
- Every check a BMP reader needs, and the order to do them in.
- How to check that sizes and offsets stay **inside** the file, without overflow.
- How to read **bottom-up** and **top-down** files, **24-bit** and **32-bit** pixels, and skip the padding.
- How to test a reader with deliberately **broken** files.
- How to load a picture, change it, and save it again — a complete picture-editing pipeline.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **reader** (decoder) | Code that turns the bytes of a file into a picture. |
| **validate** | Check that data follows the rules before using it. |
| **malformed** | Broken: not following the format's rules (by accident or on purpose). |
| **untrusted data** | Data from outside the program — a file, a download — that might be wrong. |
| **out of bounds** | Reading before the start or past the end of a list. |
| **error message** | A short text saying what went wrong. |
| **pipeline** | A chain of steps: load → change → save. |

---

## 38.1 Readers must be careful

📖 **New word: reader** (or **decoder**) — code that turns a file's bytes into a picture. `loadPPM` (Chapter 12) is a reader.

A writer only has to produce **one** correct kind of file. A reader has a harder job:

- It must read files made by **other** programs, which may use options we never write (top-down rows, 32-bit pixels, bigger headers).
- It must survive **broken** files: cut short by a failed download, damaged on a disk, or made wrong by a buggy program — or made wrong **on purpose** by someone trying to crash it.

📖 **New words: untrusted data and malformed** — anything that comes from outside the program is **untrusted**: it might be **malformed** (broken). Chapter 12 already said it: never trust a file.

What happens if a reader trusts a bad file? Suppose a file says "width 100000, height 100000" but is only 200 bytes long. A careless reader would read **past the end** of its list of bytes.

📖 **New word: out of bounds** — reading before the start or after the end of a list. In C++, `bytes[i]` with a bad `i` does not stop the program with a nice message: it reads whatever memory happens to be there, or crashes. Bugs like this in real picture readers have been used to break into computers. So our reader checks **everything** before it reads a single pixel.

---

## 38.2 The checks, in order

📖 **New word: validate** — check that data follows the rules before using it.

Our reader validates in this order. Each check only uses things that earlier checks have made safe.

| # | check | why |
|---|---|---|
| 1 | the file is at most 2,147,483,647 bytes | so every position fits in an `int` |
| 2 | at least 54 bytes | so we can read both headers without going out of bounds |
| 3 | starts with `B` `M` | is it a BMP at all? |
| 4 | info header size ≥ 40 | older BMPs have a 12-byte header with different fields; newer ones have 108 or 124 bytes, but **start** with the same 40 |
| 5 | planes = 1 | the only legal value |
| 6 | bits per pixel = 24 or 32 | the two kinds we can read (Section 38.5) |
| 7 | compression = 0 | we cannot uncompress BMP's special formats |
| 8 | width > 0, height ≠ 0 (and not absurdly negative) | a picture needs pixels; a negative height means top-down |
| 9 | width × rows ≤ 100,000,000 | refuse giant pictures that would use gigabytes of memory (the same limit as `loadPPM`) |
| 10 | pixel offset ≥ 54, and offset + row size × rows ≤ file size | **all** the pixels are inside the file |

Only after **all ten** pass do we create the picture and read pixels.

💡 Notice what we do **not** check: the file size field (bytes 2–5) and the image size field (bytes 34–37). Many programs write them wrongly (some write 0 for the image size, which is allowed when there is no compression). The real file size and our own calculation are what matter.

### Error messages

📖 **New word: error message** — a short text saying what went wrong.

`loadPPM` simply returned `false` for every problem. That is fine for a program, but not for a person trying to understand why a file will not open. So the checks live in a function that returns a **reason**:

```cpp
inline std::string bmpProblem(const Bytes& file) {
```

It returns an empty string `""` if the file is fine, or a message like `"no BM signature"`. Then `decodeBMP` just asks:

```cpp
if (!bmpProblem(file).empty()) {
    return false;
}
```

---

## 38.3 Staying inside the file, without overflow

Check 10 is the most important one, and the easiest to get wrong. The pixels take **row size × rows** bytes, starting at the pixel offset. They are all inside the file if:

> **offset + rowSize × rows ≤ file size**

But every one of those numbers comes from the **file** — they could be anything. The offset is a 4-byte unsigned number, up to 4,294,967,295. Width and height can be up to about 2 billion each. Multiplied together in `int`, they overflow (Chapter 37, Section 37.3) and can wrap around to a **small** number — and then the check would wrongly pass!

So `bmpProblem` does this arithmetic in **`long long`**, after check 9 has already limited width × rows to 100 million:

> rowSize ≤ (4 × width + 3), rows ≤ 100,000,000 / width → rowSize × rows ≤ about 400 million — no overflow

🔢 **Maths: a file cut short**

> Our 7 × 3 test file: offset 54, row size 24, 3 rows → the pixels need 54 + 72 = **126** bytes.
> Cut off the last 10 bytes: the file has 116 → 126 > 116 → **refused** ✓

🔢 **Maths: a pixel offset far outside**

> offset = 0xFFFFFFF0 = 4,294,967,280 → 4,294,967,280 + 72 > 126 → **refused** ✓
> (In `int`, 0xFFFFFFF0 would be −16: a careless reader might then read 16 bytes **before** the start of the list.)

🔢 **Maths: a giant height**

> height = 2,147,483,647, width 7 → width × rows ≈ 15 billion > 100 million → **refused** at check 9, before any multiplication could overflow ✓

---

## 38.4 Reading the rows

Once the file passed every check, reading is Chapter 36's pixel formula, the other way round:

1. **Which way up?** If the height is **negative**, the rows are **top-down** (Chapter 36, Section 36.7): file row 0 is our row 0. Otherwise they are **bottom-up**: file row 0 is our **last** row.

   > **y = topDown ? row : height − 1 − row**

2. **Where does the row start?** Every row takes `rowSize` bytes (padding included), so file row `row` starts at:

   > **rowStart = offset + row × rowSize**

   This **skips the padding** automatically: we never read the padding bytes, we just jump over them to the next row.

3. **Each pixel**: at rowStart + x × bytesPerPixel, the bytes are **B, G, R** — so the colour is `Colour{file[at + 2], file[at + 1], file[at]}`.

🔢 **Maths: the 7 × 3 test file, pixel (6, 0) (top-right)**

> bottom-up: our row y = 0 is file row 3 − 1 − 0 = **2**
> rowStart = 54 + 2 × 24 = 102; at = 102 + 6 × 3 = **120** (the same as Chapter 36, Practice 4 ✓)

---

## 38.5 32-bit pixels

Some programs save BMP files with **32 bits** per pixel: four bytes, **B, G, R** and a fourth byte (often alpha, Chapter 18, or just unused). We can read those easily:

- bytes per pixel = 32 / 8 = **4**;
- row size = (4 × width + 3) / 4 × 4 = 4 × width — always a multiple of 4, so **no padding**;
- the colour is still in the first three bytes, B, G, R. We ignore the fourth (our `Image` has no alpha).

The same row formula works for both: `bytesPerPixel` is 3 or 4.

⚠️ Strictly, many 32-bit BMPs use compression **3** ("bit fields"), which adds masks saying where each colour is inside the 4 bytes. Our reader only accepts compression 0, where the order is always B, G, R, unused. That covers the simplest 32-bit files; a full reader would read the masks too (Practice 7).

---

## 38.6 Testing a reader

A reader needs two kinds of tests:

**1. Good files are read correctly.** The program:

- writes test patterns of widths 1 to 7 with `makeBmpBytes` (Chapter 37) and decodes them back — every padding case;
- turns one into a **top-down** file (negative height, rows in the other order) by hand, and decodes it;
- builds a **32-bit** version by hand, and decodes it;
- saves the Chapter 34 heart to disk with `saveBMP`, and loads it back with `loadBMP`.

Each time, `countSame` compares the decoded picture with the original, pixel by pixel.

```
round trips in memory (pixels the same): 3 6 9 12 15 18 21
top-down file: 21 of 21 the same, 32-bit file: 21 of 21 the same
heart.bmp from disk: 90000 of 90000 pixels the same
```

**2. Broken files are refused.** The program takes the good 7 × 3 file and breaks it in eight different ways — each one aimed at one check:

```
broken files:
  the good file: accepted
  empty: refused (too short for the two headers)
  signature BX: refused (no BM signature)
  16 bits per pixel: refused (only 24 and 32 bits per pixel are supported)
  compressed: refused (compressed BMP files are not supported)
  width 0: refused (bad width or height)
  last 10 bytes missing: refused (the pixels are not inside the file)
  pixel offset far outside: refused (the pixels are not inside the file)
  height 2147483647: refused (picture too big)
```

💡 Making broken inputs on purpose is called **fuzzing** when a program does it automatically, millions of times, with random changes. Picture readers in web browsers are fuzzed all the time, because a browser opens pictures from anywhere on the internet.

---

## 38.7 Load, change, save

📖 **New word: pipeline** — a chain of steps. Now that we can **read** a real format, our programs can work on pictures made by **anything**: a paint program, a screenshot tool, a camera app that saves BMP.

The program ends with a tiny pipeline:

1. **load** `heart.bmp` from disk;
2. **shrink** it to 100 × 100 with Chapter 35's `resizeBox`;
3. **save** it as `heart-small.bmp`;
4. **flip** it upside down (row y comes from row 99 − y) and save `heart-flipped.bmp`;
5. **load** `heart-small.bmp` again, to check it.

```
heart-small.bmp: loaded, 100 x 100
```

Try it with your own pictures: save a screenshot or a drawing as 24-bit BMP from any paint program, and load it with `loadBMP`. Everything in Parts 4, 5 and (soon) 7 can now be used on real pictures.

---

## Code, part 1: `bmpload.h`

File: `common/bmpload.h` (new). It includes `bmp.h`. (A separate header keeps the line numbers of `bmp.h` in Chapter 37 correct, and lets a program that only writes BMP files leave the reader out.)

```cpp
#ifndef BMPLOAD_H
#define BMPLOAD_H

#include <cstdint>
#include <string>
#include "bmp.h"

inline std::string bmpProblem(const Bytes& file) {
    if (file.size() > 2147483647u) {
        return "file too big";
    }
    if (!hasBytes(file, 0, kBmpHeaderSize)) {
        return "too short for the two headers";
    }
    if (file[0] != 'B' || file[1] != 'M') {
        return "no BM signature";
    }
    const std::uint32_t headerSize = getU32(file, 14);
    const std::int32_t width = getS32(file, 18);
    const std::int32_t height = getS32(file, 22);
    const std::uint16_t bits = getU16(file, 28);
    if (headerSize < 40) {
        return "unknown (old) info header";
    }
    if (getU16(file, 26) != 1) {
        return "planes is not 1";
    }
    if (bits != 24 && bits != 32) {
        return "only 24 and 32 bits per pixel are supported";
    }
    if (getU32(file, 30) != 0) {
        return "compressed BMP files are not supported";
    }
    if (width <= 0 || height == 0 || height < -100000000) {
        return "bad width or height";
    }
    const long long rows = (height < 0) ? -static_cast<long long>(height) : height;
    if (static_cast<long long>(width) * rows > 100000000LL) {
        return "picture too big";
    }
    const long long rowSize = (static_cast<long long>(width) * (bits / 8) + 3) / 4 * 4;
    const long long offset = getU32(file, 10);
    if (offset < kBmpHeaderSize || offset + rowSize * rows > static_cast<long long>(file.size())) {
        return "the pixels are not inside the file";
    }
    return "";
}

inline bool decodeBMP(const Bytes& file, Image& image) {
    if (!bmpProblem(file).empty()) {
        return false;
    }
    const int width = getS32(file, 18);
    const int rawHeight = getS32(file, 22);
    const bool topDown = rawHeight < 0;
    const int height = topDown ? -rawHeight : rawHeight;
    const int bytesPerPixel = getU16(file, 28) / 8;
    const int rowSize = (width * bytesPerPixel + 3) / 4 * 4;
    const int offset = static_cast<int>(getU32(file, 10));

    Image result(width, height);
    for (int row = 0; row < height; ++row) {
        const int y = topDown ? row : height - 1 - row;
        const int rowStart = offset + row * rowSize;
        for (int x = 0; x < width; ++x) {
            const int at = rowStart + x * bytesPerPixel;
            result.setPixel(x, y, Colour{file[at + 2], file[at + 1], file[at]});
        }
    }
    image = result;
    return true;
}

inline bool loadBMP(const std::string& fileName, Image& image) {
    Bytes file;
    if (!readFileBytes(fileName, file)) {
        return false;
    }
    return decodeBMP(file, image);
}

#endif
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef BMPLOAD_H` / `#define BMPLOAD_H` | Include guard. |
| 4–6 | `#include <cstdint>` / `<string>` / `"bmp.h"` | Exact-size integers; strings for the messages; and `Bytes`, the get functions and `kBmpHeaderSize`. |
| 8 | `inline std::string bmpProblem(const Bytes& file) {` | All ten checks (Section 38.2). Returns `""` if the file is fine. |
| 9–11 | `if (file.size() > 2147483647u) { return "file too big"; }` | Check 1. (The `u` makes 2147483647 unsigned, like `file.size()`, so the comparison does not mix signed and unsigned numbers.) |
| 12–14 | `if (!hasBytes(file, 0, kBmpHeaderSize)) { return "too short for the two headers"; }` | Check 2. From now on, reading any header field is safe. |
| 15–17 | `if (file[0] != 'B' \|\| file[1] != 'M') { return "no BM signature"; }` | Check 3. |
| 18–21 | `const std::uint32_t headerSize = getU32(file, 14);` … `const std::uint16_t bits = getU16(file, 28);` | Read the fields we need, once. Width and height are **signed** (Chapter 36, Section 36.6). |
| 22–24 | `if (headerSize < 40) { return "unknown (old) info header"; }` | Check 4. Bigger headers are fine: their first 40 bytes are the same fields. |
| 25–27 | `if (getU16(file, 26) != 1) { return "planes is not 1"; }` | Check 5. |
| 28–30 | `if (bits != 24 && bits != 32) { return "only 24 and 32 bits per pixel are supported"; }` | Check 6. |
| 31–33 | `if (getU32(file, 30) != 0) { return "compressed BMP files are not supported"; }` | Check 7. |
| 34–36 | `if (width <= 0 \|\| height == 0 \|\| height < -100000000) { return "bad width or height"; }` | Check 8. The last part refuses absurd negative heights — and protects `-rawHeight` in `decodeBMP`: −2,147,483,648 cannot be turned positive in an `int`. |
| 37 | `const long long rows = (height < 0) ? -static_cast<long long>(height) : height;` | The number of rows, whichever way up. |
| 38–40 | `if (static_cast<long long>(width) * rows > 100000000LL) { return "picture too big"; }` | Check 9, in `long long`. |
| 41 | `const long long rowSize = (static_cast<long long>(width) * (bits / 8) + 3) / 4 * 4;` | The row size for 3 or 4 bytes per pixel. |
| 42–45 | `const long long offset = getU32(file, 10); if (offset < kBmpHeaderSize \|\| offset + rowSize * rows > static_cast<long long>(file.size())) { return "the pixels are not inside the file"; }` | Check 10 (Section 38.3). Pixels must not overlap the headers, and must end inside the file. |
| 46–47 | `return "";` `}` | All checks passed. |
| 49–52 | `inline bool decodeBMP(const Bytes& file, Image& image) { if (!bmpProblem(file).empty()) { return false; }` | Turn the bytes of a BMP into a picture. Refuse anything with a problem. |
| 53–56 | `const int width = getS32(file, 18); const int rawHeight = getS32(file, 22); const bool topDown = rawHeight < 0; const int height = topDown ? -rawHeight : rawHeight;` | The size, and which way up (Section 38.4). These are safe as `int`s now, because of checks 8–10. |
| 57–59 | `const int bytesPerPixel = getU16(file, 28) / 8; const int rowSize = (width * bytesPerPixel + 3) / 4 * 4; const int offset = static_cast<int>(getU32(file, 10));` | 3 or 4 bytes per pixel; the row size; where the pixels start. |
| 61 | `Image result(width, height);` | A new picture, built aside: `image` is only changed if everything works (as in `loadPPM`). |
| 62–64 | `for (int row = 0; row < height; ++row) { const int y = topDown ? row : height - 1 - row; const int rowStart = offset + row * rowSize;` | Go through the file's rows in order; work out which picture row each one is, and where it starts (skipping the padding). |
| 65–68 | `for (int x = 0; x < width; ++x) { const int at = rowStart + x * bytesPerPixel; result.setPixel(x, y, Colour{file[at + 2], file[at + 1], file[at]}); }` | Each pixel: B, G, R turned around into R, G, B. For 32-bit files, the fourth byte is simply not read. |
| 69–72 | `}` `image = result;` `return true;` `}` | Hand the finished picture back. |
| 74–80 | `inline bool loadBMP(const std::string& fileName, Image& image) { Bytes file; if (!readFileBytes(fileName, file)) { return false; } return decodeBMP(file, image); }` | Read the whole file (Chapter 12), then decode it. The same shape as `loadPPM(fileName, image)`. |
| 82 | `#endif` | End of the include guard. |

---

## Code, part 2: testing the reader

File: `ch38/read_bmp.cpp`

```cpp
#include <iostream>
#include <string>
#include "bmpload.h"
#include "resize.h"

int countSame(const Image& a, const Image& b) {
    if (a.width() != b.width() || a.height() != b.height()) {
        return -1;
    }
    int same = 0;
    for (int y = 0; y < a.height(); ++y) {
        for (int x = 0; x < a.width(); ++x) {
            Colour p = a.getPixel(x, y);
            Colour q = b.getPixel(x, y);
            if (p.r == q.r && p.g == q.g && p.b == q.b) {
                ++same;
            }
        }
    }
    return same;
}

void setU32(Bytes& file, int pos, std::uint32_t v) {
    Bytes four;
    putU32(four, v);
    for (int i = 0; i < 4; ++i) {
        file[pos + i] = four[i];
    }
}

Bytes makeTopDown(const Bytes& bottomUp, int width, int height) {
    Bytes file(bottomUp.begin(), bottomUp.begin() + kBmpHeaderSize);
    setU32(file, 22, static_cast<std::uint32_t>(-height));
    int rowSize = bmpRowSize(width);
    for (int row = height - 1; row >= 0; --row) {
        int start = kBmpHeaderSize + row * rowSize;
        file.insert(file.end(), bottomUp.begin() + start, bottomUp.begin() + start + rowSize);
    }
    return file;
}

Bytes make32Bit(const Image& image) {
    Bytes file = makeBmpBytes(image);
    file.resize(kBmpHeaderSize);
    int pixelBytes = 4 * image.width() * image.height();
    setU32(file, 2, kBmpHeaderSize + pixelBytes);
    file[28] = 32;
    setU32(file, 34, pixelBytes);
    for (int y = image.height() - 1; y >= 0; --y) {
        for (int x = 0; x < image.width(); ++x) {
            Colour c = image.getPixel(x, y);
            file.push_back(c.b);
            file.push_back(c.g);
            file.push_back(c.r);
            file.push_back(255);
        }
    }
    return file;
}

Image makeTestPattern(int width, int height) {
    Image pattern(width, height);
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            pattern.setPixel(x, y, Colour{static_cast<std::uint8_t>(40 * x + 10),
                                          static_cast<std::uint8_t>(80 * y + 20),
                                          static_cast<std::uint8_t>(255 - 30 * x)});
        }
    }
    return pattern;
}

void report(const char* label, const Bytes& file) {
    std::string problem = bmpProblem(file);
    std::cout << "  " << label << ": " << (problem.empty() ? "accepted" : "refused (" + problem + ")")
              << "\n";
}

int main() {
    std::cout << "round trips in memory (pixels the same):";
    for (int w = 1; w <= 7; ++w) {
        Image original = makeTestPattern(w, 3);
        Image back(0, 0);
        bool ok = decodeBMP(makeBmpBytes(original), back);
        std::cout << " " << (ok ? countSame(original, back) : -1);
    }
    std::cout << "\n";

    Image pattern = makeTestPattern(7, 3);
    Bytes bottomUp = makeBmpBytes(pattern);
    Image fromTopDown(0, 0);
    decodeBMP(makeTopDown(bottomUp, 7, 3), fromTopDown);
    Image from32(0, 0);
    decodeBMP(make32Bit(pattern), from32);
    std::cout << "top-down file: " << countSame(pattern, fromTopDown) << " of 21 the same, "
              << "32-bit file: " << countSame(pattern, from32) << " of 21 the same\n";

    std::cout << "broken files:\n";
    report("the good file", bottomUp);
    report("empty", Bytes{});
    Bytes wrong = bottomUp;
    wrong[1] = 'X';
    report("signature BX", wrong);
    wrong = bottomUp;
    wrong[28] = 16;
    report("16 bits per pixel", wrong);
    wrong = bottomUp;
    setU32(wrong, 30, 1);
    report("compressed", wrong);
    wrong = bottomUp;
    setU32(wrong, 18, 0);
    report("width 0", wrong);
    wrong = bottomUp;
    wrong.resize(wrong.size() - 10);
    report("last 10 bytes missing", wrong);
    wrong = bottomUp;
    setU32(wrong, 10, 0xFFFFFFF0u);
    report("pixel offset far outside", wrong);
    wrong = bottomUp;
    setU32(wrong, 22, 0x7FFFFFFFu);
    report("height 2147483647", wrong);

    Image heart(300, 300, Colour{255, 240, 245});
    std::vector<PointF> outline;
    appendCubic(outline, PointF{150.0, 260.0}, PointF{40.0, 180.0}, PointF{50.0, 40.0},
                PointF{150.0, 95.0});
    appendCubic(outline, PointF{150.0, 95.0}, PointF{250.0, 40.0}, PointF{260.0, 180.0},
                PointF{150.0, 260.0});
    fillPolygonAA(heart, outline, Colour{220, 30, 70});
    Image loaded(0, 0);
    if (!saveBMP(heart, "heart.bmp") || !loadBMP("heart.bmp", loaded)) {
        std::cout << "could not save and load heart.bmp\n";
        return 1;
    }
    std::cout << "heart.bmp from disk: " << countSame(heart, loaded) << " of "
              << heart.width() * heart.height() << " pixels the same\n";

    Image small = resizeBox(loaded, 100, 100);
    Image flipped(100, 100);
    for (int y = 0; y < 100; ++y) {
        for (int x = 0; x < 100; ++x) {
            flipped.setPixel(x, y, small.getPixel(x, 99 - y));
        }
    }
    if (!saveBMP(small, "heart-small.bmp") || !saveBMP(flipped, "heart-flipped.bmp")) {
        std::cout << "could not write the small hearts\n";
        return 1;
    }
    Image check(0, 0);
    bool reloaded = loadBMP("heart-small.bmp", check);
    std::cout << "heart-small.bmp: " << (reloaded ? "loaded" : "failed") << ", " << check.width()
              << " x " << check.height() << "\n";
    return 0;
}
```

Build and run (from the `code/ch38` folder):

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common read_bmp.cpp -o read_bmp
./read_bmp
```

### Line by line

**Helpers (lines 1–77)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–4 | the `#include` lines | Printing, strings, the new reader, and `resize.h` (for `resizeBox`, and through it the drawing library for the heart). |
| 6–21 | `int countSame(const Image& a, const Image& b) { ... }` | How many pixels of two pictures are exactly the same, or −1 if their sizes differ. |
| 23–29 | `void setU32(Bytes& file, int pos, std::uint32_t v) { Bytes four; putU32(four, v); for (...) { file[pos + i] = four[i]; } }` | **Change** a 4-byte field that is already in the file (`putU32` can only **add** bytes at the end). We use it to break files on purpose. |
| 31 | `Bytes makeTopDown(const Bytes& bottomUp, int width, int height) {` | Turn one of our bottom-up files into a top-down one, by hand (Section 38.6). |
| 32 | `Bytes file(bottomUp.begin(), bottomUp.begin() + kBmpHeaderSize);` | A new list holding a copy of the first 54 bytes: the two headers. |
| 33 | `setU32(file, 22, static_cast<std::uint32_t>(-height));` | Make the height negative (two's complement, Chapter 36). |
| 34–38 | `int rowSize = bmpRowSize(width); for (int row = height - 1; row >= 0; --row) { int start = kBmpHeaderSize + row * rowSize; file.insert(file.end(), bottomUp.begin() + start, bottomUp.begin() + start + rowSize); }` | Copy the rows in the **other** order: the old last row first. `insert` at `file.end()` adds a whole slice of another list (padding included). |
| 39–40 | `return file;` `}` | The top-down file. |
| 42–44 | `Bytes make32Bit(const Image& image) { Bytes file = makeBmpBytes(image); file.resize(kBmpHeaderSize);` | A 32-bit BMP by hand: start from our 24-bit headers and throw away their pixels. |
| 45–48 | `int pixelBytes = 4 * image.width() * image.height(); setU32(file, 2, kBmpHeaderSize + pixelBytes); file[28] = 32; setU32(file, 34, pixelBytes);` | Fix the file size, bits per pixel and image size fields. (`file[28]` is the low byte of the 2-byte bits field; the high byte stays 0.) |
| 49–59 | the row loops with four `push_back` calls | Bottom-up rows, 4 bytes per pixel: B, G, R, 255. No padding is needed (Section 38.5). |
| 61–71 | `Image makeTestPattern(int width, int height) { ... }` | Chapter 37's test pattern: every pixel a different colour. |
| 73–77 | `void report(const char* label, const Bytes& file) { std::string problem = bmpProblem(file); std::cout << ... (problem.empty() ? "accepted" : "refused (" + problem + ")") ... }` | Print whether a file is accepted, or why it is refused. `"refused (" + problem + ")"` joins text with `+`, giving a `std::string`. |

**Good files (lines 79–96)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 80–87 | `for (int w = 1; w <= 7; ++w) { Image original = makeTestPattern(w, 3); Image back(0, 0); bool ok = decodeBMP(makeBmpBytes(original), back); std::cout << ... countSame(original, back) ...; }` | Write and read back every padding case, in memory. `Image back(0, 0)` is an empty picture for the reader to fill in. |
| 89–90 | `Image pattern = makeTestPattern(7, 3); Bytes bottomUp = makeBmpBytes(pattern);` | The good 7 × 3 file, used for the next tests. |
| 91–94 | `decodeBMP(makeTopDown(bottomUp, 7, 3), fromTopDown);` / `decodeBMP(make32Bit(pattern), from32);` | Read a top-down file and a 32-bit file. |
| 95–96 | `std::cout << "top-down file: " << countSame(pattern, fromTopDown) << ...` | Both must give back the same picture. |

**Broken files (lines 98–121)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 99–100 | `report("the good file", bottomUp); report("empty", Bytes{});` | The good file must be accepted; an empty list (`Bytes{}`) refused. |
| 101–103 | `Bytes wrong = bottomUp; wrong[1] = 'X'; report("signature BX", wrong);` | Each test starts from a **fresh copy** of the good file and breaks **one** thing. |
| 104–112 | `wrong[28] = 16;` / `setU32(wrong, 30, 1);` / `setU32(wrong, 18, 0);` | 16 bits per pixel; compression 1; width 0. |
| 113–115 | `wrong.resize(wrong.size() - 10);` | Cut the last 10 bytes off (Section 38.3). |
| 116–121 | `setU32(wrong, 10, 0xFFFFFFF0u);` / `setU32(wrong, 22, 0x7FFFFFFFu);` | A pixel offset far outside the file; a giant height. |

**The heart (lines 123–136)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 123–129 | `Image heart(300, 300, ...); ... fillPolygonAA(heart, outline, Colour{220, 30, 70});` | Chapter 34's heart again. |
| 130–134 | `Image loaded(0, 0); if (!saveBMP(heart, "heart.bmp") \|\| !loadBMP("heart.bmp", loaded)) { ... return 1; }` | Save it to disk, and load it back with the new reader. |
| 135–136 | `std::cout << "heart.bmp from disk: " << countSame(heart, loaded) << ...` | All 90,000 pixels must be the same. |

**The pipeline (lines 138–154)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 138 | `Image small = resizeBox(loaded, 100, 100);` | Shrink the **loaded** picture (Chapter 35). |
| 139–144 | `Image flipped(100, 100); for (...) { for (...) { flipped.setPixel(x, y, small.getPixel(x, 99 - y)); } }` | Turn it upside down: row y gets row 99 − y. |
| 145–148 | `if (!saveBMP(small, "heart-small.bmp") \|\| !saveBMP(flipped, "heart-flipped.bmp")) { ... }` | Save both. |
| 149–154 | `Image check(0, 0); bool reloaded = loadBMP("heart-small.bmp", check); std::cout << ...` `return 0;` `}` | Load the small one back, and print its size. |

### What you should see

```
round trips in memory (pixels the same): 3 6 9 12 15 18 21
top-down file: 21 of 21 the same, 32-bit file: 21 of 21 the same
broken files:
  the good file: accepted
  empty: refused (too short for the two headers)
  signature BX: refused (no BM signature)
  16 bits per pixel: refused (only 24 and 32 bits per pixel are supported)
  compressed: refused (compressed BMP files are not supported)
  width 0: refused (bad width or height)
  last 10 bytes missing: refused (the pixels are not inside the file)
  pixel offset far outside: refused (the pixels are not inside the file)
  height 2147483647: refused (picture too big)
heart.bmp from disk: 90000 of 90000 pixels the same
heart-small.bmp: loaded, 100 x 100
```

And three files: `heart.bmp`, `heart-small.bmp` (a smooth little heart) and `heart-flipped.bmp` (the same, upside down). Open them in any viewer.

---

## Small examples

### Example 1 — Which check fails?

A file of 40 bytes: check 2 ("too short for the two headers") — we never even look at the signature, because reading byte 28 would be out of bounds.

### Example 2 — A PNG renamed to .bmp

The first two bytes of a PNG file are 0x89 0x50 — not "BM". Check 3 refuses it. (The file **name** says nothing; only the bytes count.)

### Example 3 — A top-down file

Height bytes `FD FF FF FF` = −3. rows = 3, topDown = true: file row 0 is our row 0 (the top), and so on.

### Example 4 — A 32-bit pixel

The four bytes `20 40 80 FF` at a pixel's position: blue 0x20 = 32, green 0x40 = 64, red 0x80 = 128 → `Colour{128, 64, 32}`, a brown. The 0xFF is ignored.

### Example 5 — The bytes we never read

In a 7 × 3, 24-bit file: 3 rows × 3 padding bytes = 9 bytes the reader jumps over. In a 32-bit file: none — but one byte per pixel (the fourth) is never read: 21 bytes.

---

## Common mistakes

⚠️ **Trusting the header.** Every number in a file can be wrong. Check sizes against the **real** file size before reading pixels.

⚠️ **Checking in `int`.** offset + rowSize × rows can overflow and wrap to a small number, so the check passes when it should fail. Use `long long`, and limit the picture size first.

⚠️ **Reading the header before checking the length.** `getU32(file, 18)` on a 10-byte file reads out of bounds. Check `hasBytes` first.

⚠️ **Assuming pixels start at byte 54.** Use the pixel offset field.

⚠️ **Ignoring negative heights.** Top-down files would come out upside down — or, if the height is used as a size, the reader would refuse them or crash.

⚠️ **Forgetting the padding.** Rows start at offset + row × **rowSize**, not offset + row × 3 × width.

⚠️ **Changing the output picture before all checks pass.** Build the result aside, and only copy it into `image` at the end.

---

## Practice

🏋️ **1.** Which check refuses each of these files? (a) 54 bytes, all zero. (b) A good file with planes = 2. (c) A good 24-bit file whose header says 8 bits per pixel.

🏋️ **2.** Make a BMP with your favourite paint program (save as "24-bit bitmap"), load it with `loadBMP`, and print its width, height and the colour of its top-left pixel.

🏋️ **3.** Write a program that loads any BMP and saves it as PPM — a **converter**. Then write the opposite: PPM → BMP.

🏋️ **4.** Change `bmpProblem` to also refuse files whose pixel offset is **smaller than 14 + header size** (pixels overlapping the info header). Which of our test files would that affect?

🏋️ **5.** Write `loadAndCheck(fileName)`, which prints either the picture's size or the reason from `bmpProblem`.

🏋️ **6.** Load a BMP, make it grey with Chapter 15's `toGrey`, and save it as `grey.bmp`.

🏋️ **7.** (Harder) Support 32-bit files with compression 3: read the three 4-byte **masks** at offsets 54, 58 and 62 (red, green, blue), and check that they are 0x00FF0000, 0x0000FF00 and 0x000000FF — the B, G, R, unused layout. Accept the file only then.

🏋️ **8.** Break the good 7 × 3 file by setting its width to 1,000,000. Which message do you get, and why that one?

---

## Answers

**1.**
> (a) check 3: "no BM signature" (the length is fine, but the first byte is 0, not 'B').
> (b) check 5: "planes is not 1".
> (c) check 6: "only 24 and 32 bits per pixel are supported".

**2.**

```cpp
Image picture(0, 0);
if (loadBMP("drawing.bmp", picture)) {
    Colour c = picture.getPixel(0, 0);
    std::cout << picture.width() << " x " << picture.height() << ", top-left ("
              << static_cast<int>(c.r) << ", " << static_cast<int>(c.g) << ", "
              << static_cast<int>(c.b) << ")\n";
}
```

**3.**

```cpp
Image picture(0, 0);
if (loadBMP("in.bmp", picture) && picture.savePPM("out.ppm")) {
    std::cout << "converted\n";
}
Image other(0, 0);
if (loadPPM("in.ppm", other) && saveBMP(other, "out.bmp")) {
    std::cout << "converted back\n";
}
```

> Converting BMP → PPM → BMP gives back exactly the same pixels: both formats store the colours exactly.

**4.**

```cpp
if (offset < 14 + static_cast<long long>(headerSize)) {
    return "the pixels overlap the info header";
}
```

> None of our tests: all of them have offset 54 = 14 + 40, except "pixel offset far outside", which is refused anyway.

**5.**

```cpp
void loadAndCheck(const std::string& fileName) {
    Bytes file;
    if (!readFileBytes(fileName, file)) {
        std::cout << fileName << ": cannot open\n";
        return;
    }
    std::string problem = bmpProblem(file);
    Image picture(0, 0);
    if (!problem.empty() || !decodeBMP(file, picture)) {
        std::cout << fileName << ": " << problem << "\n";
        return;
    }
    std::cout << fileName << ": " << picture.width() << " x " << picture.height() << "\n";
}
```

**6.**
```cpp
Image picture(0, 0);
if (loadBMP("in.bmp", picture)) {
    for (int y = 0; y < picture.height(); ++y) {
        for (int x = 0; x < picture.width(); ++x) {
            picture.setPixel(x, y, toGrey(picture.getPixel(x, y)));
        }
    }
    saveBMP(picture, "grey.bmp");
}
```

> Chapter 15's `toGrey` turns one `Colour` into its grey (include `grey.h`), so we apply it to every pixel.

**7.**

```cpp
bool masksAreBGR(const Bytes& file) {
    return hasBytes(file, 54, 12) && getU32(file, 54) == 0x00FF0000u &&
           getU32(file, 58) == 0x0000FF00u && getU32(file, 62) == 0x000000FFu;
}
```

> In `bmpProblem`, allow compression 3 when bits = 32 and `masksAreBGR(file)` is true. (With the 40-byte header, the masks come right after it, and the pixel offset is then 66 or more.)

**8.**
> "the pixels are not inside the file": width 1,000,000 × 3 rows = 3,000,000 ≤ 100,000,000, so check 9 passes; but the pixels would need 54 + 3,000,000 × 3 = 9,000,054 bytes, and the file has 126.

---

## Summary

🧠 A reader must **never trust a file**: check everything before reading pixels.

🧠 The checks: size ≤ 2³¹ − 1, ≥ 54 bytes, "BM", header ≥ 40, planes 1, 24 or 32 bits, no compression, sensible width and height, not too big, and **offset + rowSize × rows ≤ file size** (in `long long`).

🧠 Return a **reason** (`bmpProblem`) so people can see what is wrong.

🧠 Rows: **y = topDown ? row : height − 1 − row**, starting at **offset + row × rowSize** — which skips the padding. Pixels are B, G, R (and an ignored fourth byte for 32-bit).

🧠 Test with good files (every width, top-down, 32-bit) **and** broken files (one problem each).

🧠 Load → change → save: our library now works on real pictures from any program.

---

## Next chapter

BMP is done. In Chapter 39 we meet another simple, uncompressed format, popular in games and 3D programs: **TGA** (Targa). It has a small 18-byte header, can store pixels **bottom-up or top-down**, and — unlike BMP — properly supports **alpha** (transparency, Chapter 18). It also has a simple kind of compression called **run-length encoding**, our very first compression method.
