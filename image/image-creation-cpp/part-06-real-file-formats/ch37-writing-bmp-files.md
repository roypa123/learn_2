# Chapter 37 — Writing BMP Files

> **Part 6 · Chapter 37 of 82**
> **You need:** Chapters 1–36 (especially 7, 11 and 36) · **You will make:** `bmp.h` (`writeBytes`, a size check, `makeBmpBytes` and `saveBMP`), `pattern.bmp`, and four pictures from earlier chapters saved as both BMP and PPM: `gradient`, `rainbow`, `heart` and `flower`

---

## What you will learn

- How to turn Chapter 36's hand-built file into a function that works for **any** picture.
- How to write a list of bytes to a file, safely.
- Which picture sizes a BMP can hold, and how to refuse the ones it cannot.
- How to **test** a file writer by reading the bytes back and comparing every pixel.
- Why testing **every padding case** matters.
- How big BMP files are, compared with PPM.
- How to open your pictures in any ordinary picture viewer — no special program needed any more.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **writer** | Code that turns a picture into the bytes of a file. |
| **reader** | Code that turns the bytes of a file back into a picture (Chapter 38). |
| **round trip** | Writing something and reading it back, to check nothing changed. |
| **self-test** | A program that checks its own results and reports "match" or "mismatch". |
| **edge case** | An unusual input at the limits, where bugs like to hide (width 1, width 0, …). |
| **overflow** | A number getting too big for its type, so it wraps around to a wrong value (Chapter 4). |
| **reserve** | Tell a `std::vector` how big it will get, so it can get the memory once. |

---

## 37.1 From one file to any picture

📖 **New word: writer** — code that turns a picture into the bytes of a file. `savePPM` (Chapter 11) is a writer.

Chapter 36 built one BMP file by hand, for one 3 × 2 picture. Almost every line used fixed numbers: 3, 2, 12, 24, 78. To make a writer for **any** picture, we replace each of them with the formula behind it:

| Chapter 36 | formula | in the code |
|---|---|---|
| width 3, height 2 | from the picture | `image.width()`, `image.height()` |
| row size 12 | (3 × width + 3) / 4 × 4 | `bmpRowSize(width)` |
| pixel array 24 | row size × height | `pixelBytes` |
| file size 78 | 54 + pixel array | `kBmpHeaderSize + pixelBytes` |
| pixel offset 54 | 14 + 40 | `kBmpHeaderSize` |

Everything else — "BM", 40, 1, 24, 0, 2835 — stays the same for every 24-bit BMP.

```cpp
const int kBmpHeaderSize = 14 + 40;
```

A named constant (the `k` again means "constant", Chapter 30) is clearer than writing 54 in five places, and it explains **where** the number comes from.

---

## 37.2 Building the bytes, then writing them

We split the job into two parts:

1. **`makeBmpBytes(image)`** builds the whole file as a `Bytes` list, in memory.
2. **`writeBytes(fileName, bytes)`** writes any list of bytes to a file.

Why not write straight to the file, byte by byte? Splitting makes both parts simpler, and it makes **testing** easy: we can check the bytes of `makeBmpBytes` without touching the disk at all (Section 37.5). And `writeBytes` will be used again for TGA, PNG and GIF files.

### Writing bytes to a file

This is Chapter 7's recipe, and the same as the end of Chapter 11's `savePPM`:

```cpp
inline bool writeBytes(const std::string& fileName, const Bytes& bytes) {
    std::ofstream file(fileName, std::ios::binary);
    if (!file) {
        return false;
    }
    file.write(reinterpret_cast<const char*>(bytes.data()),
               static_cast<std::streamsize>(bytes.size()));
    return static_cast<bool>(file);
}
```

- `std::ios::binary`: write the bytes exactly as they are. Without it, Windows would turn every byte 0x0A ("new line") into the two bytes 0x0D 0x0A — and a BMP is full of 0x0A bytes that are really colours or sizes (Chapter 7).
- `bytes.data()` points at the first byte; `write` sends all `bytes.size()` bytes in one go.
- The last line reports whether everything worked (a full disk, for example, makes it fail).

### Reserving memory

📖 **New word: reserve** — a `std::vector` grows as we `push_back`. Each time it runs out of room it gets a bigger piece of memory and copies everything across. If we know the final size, `reserve` gets the right amount of memory **once**:

```cpp
file.reserve(kBmpHeaderSize + pixelBytes);
```

It does not change what the program does — only how fast it does it. (For a 300 × 300 picture that is 270,054 bytes; without `reserve`, the list would move about 20 times as it grew.)

---

## 37.3 Which sizes can a BMP hold?

📖 **New word: edge case** — an unusual input at the limits, where bugs like to hide.

Two edge cases need thought:

**A picture with no pixels.** `Image empty(0, 0)` is allowed in our library (Chapter 11). But a BMP with width 0 is not a real picture, and many programs refuse to open one. Our writer refuses too: `saveBMP` returns `false` and writes nothing.

**A picture that is too big.**

📖 **New word: overflow** — when a number gets too big for its type, it wraps around to a wrong value (Chapter 4, Section 4.9).

The file size field is 4 bytes, and many BMP readers treat it as a **signed** number, so the biggest safe file is 2,147,483,647 bytes (2³¹ − 1, about 2 gigabytes). Our sizes are `int`s too, with the same limit. For a huge picture, row size × height would overflow an `int` and give a nonsense (even negative) size.

So before computing anything, we check — in `long long`, which holds numbers far bigger than any picture:

```cpp
long long rowSize = (3LL * width + 3) / 4 * 4;
return kBmpHeaderSize + rowSize * height <= 2147483647LL;
```

(`3LL` is the number 3 as a `long long`. Because it comes first, the whole calculation is done in `long long` — just as `2.0 * x` makes a calculation `double`, Chapter 30.)

🔢 **Maths: the biggest square picture**

> rowSize × height ≈ 3 × w × w ≤ 2,147,483,647 → w² ≤ 715,827,882 → w ≤ **26,754**
> A square BMP can be up to about 26,700 pixels on each side — far bigger than any picture in this book.

If the size is not OK, `makeBmpBytes` returns an **empty** list, and `saveBMP` turns that into `false`.

---

## 37.4 `makeBmpBytes`, step by step

The function is Chapter 36's program, with the fixed numbers replaced:

1. Check the size (Section 37.3).
2. Work out `rowSize` and `pixelBytes`; reserve the memory.
3. The **file header**: "BM", file size, two zeros, pixel offset (Chapter 36, Section 36.3).
4. The **info header**: 40, width, height, 1, 24, 0, pixel array size, 2835, 2835, 0, 0 (Section 36.4).
5. The **pixels**: rows bottom-up, each pixel as B, G, R, each row padded with zeros to `rowSize`.
6. Return the list.

Then `saveBMP` is just:

```cpp
inline bool saveBMP(const Image& image, const std::string& fileName) {
    Bytes file = makeBmpBytes(image);
    if (file.empty()) {
        return false;
    }
    return writeBytes(fileName, file);
}
```

💡 Notice that `saveBMP` is a free function, not a member of `Image` like `savePPM`. That keeps `image.h` small: the picture class does not need to know about every file format. (`loadPPM`, from Chapter 12, is a free function too.)

---

## 37.5 Testing a writer: the round trip

📖 **New words: round trip and self-test** — write something, read it back, and check that nothing changed. A program that does this and reports the result is a **self-test**.

How do we know our writer is right? Opening the file in a viewer is a good check, but it is easy to miss one wrong pixel, and impossible to check 90,000 by eye. So the program reads the bytes back **exactly as a reader would** — using only what the file says (pixel offset, width, height) — and compares every pixel with the original picture:

> at = offset + (height − 1 − y) × rowSize + 3x (Chapter 36, Section 36.9)
> match if file[at] = blue, file[at + 1] = green, file[at + 2] = red

`checkBmp` returns the number of matching pixels, or −1 if the header itself is wrong (or a pixel would be outside the file). If the answer equals width × height, every pixel made the round trip.

⚠️ A round trip only finds bugs where the writer and the checker **disagree**. If both made the same mistake (say, both forgot the padding), they would agree perfectly — and the file would still be broken. That is why `checkBmp` uses the file's own fields and the Chapter 36 formula, which we checked by hand, byte by byte. And why we still open the files in a real viewer.

### Every padding case

Padding is 0, 1, 2 or 3 bytes, depending on the width (Chapter 36). A bug in the padding only shows up for some widths — and the most common test sizes (64, 100, 256, 640) are all multiples of 4, where the padding is 0 and the bug hides. So the program tests widths **1 to 7**, which covers every padding case twice over:

```
width, file size, expected size, pixels matching:
  1, 66, 66, 3 of 3
  2, 78, 78, 6 of 6
  3, 90, 90, 9 of 9
  4, 90, 90, 12 of 12
  5, 102, 102, 15 of 15
  6, 114, 114, 18 of 18
  7, 126, 126, 21 of 21
```

🔢 **Maths: width 5, height 3**

> colour bytes per row 15 → row size (15 + 3) / 4 × 4 = 16 → pixel array 16 × 3 = 48 → file 54 + 48 = **102** ✓

(Widths 3 and 4 give the same file size, 90: a 3-wide row is 9 colour bytes + 3 padding, a 4-wide row is 12 colour bytes + 0 padding — both 12.)

The test pattern gives every pixel a different colour (red grows across, green grows down, blue shrinks across), so a pixel in the wrong place would not match by accident.

And the empty picture:

```
saving a 0 x 0 picture: refused
```

---

## 37.6 Real pictures, in a real viewer

The program now rebuilds four pictures from earlier chapters and saves each one twice — as BMP and as PPM:

| picture | from | size | why it is a good test |
|---|---|---|---|
| `gradient` | Chapter 13 | 256 × 64 | smooth colours; width a multiple of 4 (no padding) |
| `rainbow` | Chapter 16 | 301 × 101 | odd width: 903 colour bytes per row, so 1 byte of padding |
| `heart` | Chapter 34 | 300 × 300 | Bézier curves, smooth edges |
| `flower` | Chapter 31 | 300 × 300 | tilted ellipses, blended petals |

Now **open the BMP files** — double-click them. Windows Photos, macOS Preview, any web browser (drag the file onto the window), any phone: they all show BMP. For the first time since Chapter 8, you do not need a special PPM viewer. The pictures should look exactly like the PPM versions. If one is upside down, or red and blue are swapped, or the picture is slanted, Chapter 36's Common mistakes tell you what went wrong.

### How big are the files?

```
gradient 256 x 64: BMP 49206 bytes, PPM 49166 bytes, read back: 16384 of 16384 pixels match
rainbow 301 x 101: BMP 91358 bytes, PPM 91218 bytes, read back: 30401 of 30401 pixels match
heart 300 x 300: BMP 270054 bytes, PPM 270015 bytes, read back: 90000 of 90000 pixels match
flower 300 x 300: BMP 270054 bytes, PPM 270015 bytes, read back: 90000 of 90000 pixels match
```

🔢 **Maths: where do the sizes come from?**

> BMP = 54 + rowSize × height; PPM = its text header + 3 × width × height (Chapter 9)
> gradient: BMP 54 + 768 × 64 = **49,206**; PPM header "P6\n256 64\n255\n" is 14 bytes → 14 + 49,152 = **49,166**
> rainbow: rowSize = (903 + 3) / 4 × 4 = 904 → BMP 54 + 904 × 101 = **91,358**; PPM 15 + 91,203 = **91,218**
> heart: BMP 54 + 900 × 300 = **270,054**; PPM 15 + 270,000 = **270,015**

Both formats store the colours with **no compression**, so they are almost exactly the same size: 3 bytes per pixel, plus a small header (and a little padding for BMP). A 1920 × 1080 photo is about 6 MB either way. In Chapters 40–45 we will make PNG files, which are **compressed** — often 3 to 10 times smaller for pictures like ours, with no loss of quality.

---

## Code, part 1: `bmp.h`

File: `common/bmp.h` (new). It includes `bytes.h`.

```cpp
#ifndef BMP_H
#define BMP_H

#include <cstdint>
#include <fstream>
#include <string>
#include "bytes.h"

const int kBmpHeaderSize = 14 + 40;

inline bool writeBytes(const std::string& fileName, const Bytes& bytes) {
    std::ofstream file(fileName, std::ios::binary);
    if (!file) {
        return false;
    }
    file.write(reinterpret_cast<const char*>(bytes.data()),
               static_cast<std::streamsize>(bytes.size()));
    return static_cast<bool>(file);
}

inline bool bmpSizeIsOk(int width, int height) {
    if (width <= 0 || height <= 0) {
        return false;
    }
    long long rowSize = (3LL * width + 3) / 4 * 4;
    return kBmpHeaderSize + rowSize * height <= 2147483647LL;
}

inline Bytes makeBmpBytes(const Image& image) {
    Bytes file;
    const int width = image.width();
    const int height = image.height();
    if (!bmpSizeIsOk(width, height)) {
        return file;
    }
    const int rowSize = bmpRowSize(width);
    const int pixelBytes = rowSize * height;
    file.reserve(kBmpHeaderSize + pixelBytes);

    file.push_back('B');
    file.push_back('M');
    putU32(file, kBmpHeaderSize + pixelBytes);
    putU16(file, 0);
    putU16(file, 0);
    putU32(file, kBmpHeaderSize);

    putU32(file, 40);
    putS32(file, width);
    putS32(file, height);
    putU16(file, 1);
    putU16(file, 24);
    putU32(file, 0);
    putU32(file, pixelBytes);
    putS32(file, 2835);
    putS32(file, 2835);
    putU32(file, 0);
    putU32(file, 0);

    for (int y = height - 1; y >= 0; --y) {
        for (int x = 0; x < width; ++x) {
            Colour c = image.getPixel(x, y);
            file.push_back(c.b);
            file.push_back(c.g);
            file.push_back(c.r);
        }
        for (int p = width * 3; p < rowSize; ++p) {
            file.push_back(0);
        }
    }
    return file;
}

inline bool saveBMP(const Image& image, const std::string& fileName) {
    Bytes file = makeBmpBytes(image);
    if (file.empty()) {
        return false;
    }
    return writeBytes(fileName, file);
}

#endif
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef BMP_H` / `#define BMP_H` | Include guard. |
| 4–7 | `#include <cstdint>` / `<fstream>` / `<string>` / `"bytes.h"` | Exact-size integers; files; file names; and `Bytes`, `putU32`, `bmpRowSize` (Chapter 36). |
| 9 | `const int kBmpHeaderSize = 14 + 40;` | The two headers together: 54 bytes (Section 37.1). |
| 11 | `inline bool writeBytes(const std::string& fileName, const Bytes& bytes) {` | Write any list of bytes to a file (Section 37.2). |
| 12–15 | `std::ofstream file(fileName, std::ios::binary); if (!file) { return false; }` | Open the file for writing, in binary mode. If it cannot be opened (a bad folder name, no permission), give up. |
| 16–17 | `file.write(reinterpret_cast<const char*>(bytes.data()), static_cast<std::streamsize>(bytes.size()));` | Write all the bytes at once. `write` wants a `char` pointer and a `std::streamsize` count, so we convert (exactly as in `savePPM`, Chapter 11). |
| 18–19 | `return static_cast<bool>(file);` `}` | `true` if every byte was written. |
| 21–24 | `inline bool bmpSizeIsOk(int width, int height) { if (width <= 0 \|\| height <= 0) { return false; }` | Can this picture be a BMP? Not with no pixels (Section 37.3). |
| 25 | `long long rowSize = (3LL * width + 3) / 4 * 4;` | The row size, worked out in `long long` so it cannot overflow. |
| 26–27 | `return kBmpHeaderSize + rowSize * height <= 2147483647LL;` `}` | The whole file must fit in 2³¹ − 1 bytes. |
| 29–32 | `inline Bytes makeBmpBytes(const Image& image) { Bytes file; const int width = image.width(); const int height = image.height();` | Build the bytes of a BMP file for `image` (Section 37.4). |
| 33–35 | `if (!bmpSizeIsOk(width, height)) { return file; }` | A size we cannot store: return the still-empty list. |
| 36–38 | `const int rowSize = bmpRowSize(width); const int pixelBytes = rowSize * height; file.reserve(kBmpHeaderSize + pixelBytes);` | The sizes (safe now, because we checked), and the memory for the whole file. |
| 40–45 | `file.push_back('B'); file.push_back('M'); putU32(file, kBmpHeaderSize + pixelBytes); putU16(file, 0); putU16(file, 0); putU32(file, kBmpHeaderSize);` | The 14-byte file header: signature, file size, reserved, reserved, pixel offset. |
| 47–57 | `putU32(file, 40);` … `putU32(file, 0);` | The 40-byte info header: header size, width, height (signed), planes, bits per pixel, compression, pixel array size, two "pixels per metre", colours used, important colours. |
| 59 | `for (int y = height - 1; y >= 0; --y) {` | Rows bottom-up. |
| 60–65 | `for (int x = 0; x < width; ++x) { Colour c = image.getPixel(x, y); file.push_back(c.b); file.push_back(c.g); file.push_back(c.r); }` | Each pixel as B, G, R. |
| 66–69 | `for (int p = width * 3; p < rowSize; ++p) { file.push_back(0); }` `}` | Pad the row with zeros up to `rowSize`. |
| 70–71 | `return file;` `}` | The whole file. |
| 73–79 | `inline bool saveBMP(const Image& image, const std::string& fileName) { Bytes file = makeBmpBytes(image); if (file.empty()) { return false; } return writeBytes(fileName, file); }` | Build, refuse if empty, write (Section 37.4). Note the order of the arguments: picture first, then the file name. |
| 81 | `#endif` | End of the include guard. |

---

## Code, part 2: testing, and saving real pictures

File: `ch37/write_bmp.cpp`

```cpp
#include <iostream>
#include <string>
#include "bmp.h"
#include "bezier.h"
#include "hsv.h"

int checkBmp(const Image& image, const Bytes& file) {
    if (!hasBytes(file, 0, kBmpHeaderSize) || file[0] != 'B' || file[1] != 'M') {
        return -1;
    }
    int offset = static_cast<int>(getU32(file, 10));
    int width = getS32(file, 18);
    int height = getS32(file, 22);
    if (width != image.width() || height != image.height() || getU16(file, 28) != 24) {
        return -1;
    }
    int rowSize = bmpRowSize(width);
    int matches = 0;
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            int at = offset + (height - 1 - y) * rowSize + x * 3;
            if (!hasBytes(file, at, 3)) {
                return -1;
            }
            Colour c = image.getPixel(x, y);
            if (file[at] == c.b && file[at + 1] == c.g && file[at + 2] == c.r) {
                ++matches;
            }
        }
    }
    return matches;
}

long long fileSizeOf(const std::string& fileName) {
    Bytes bytes;
    if (!readFileBytes(fileName, bytes)) {
        return -1;
    }
    return static_cast<long long>(bytes.size());
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

int main() {
    std::cout << "width, file size, expected size, pixels matching:\n";
    for (int w = 1; w <= 7; ++w) {
        Image test = makeTestPattern(w, 3);
        Bytes file = makeBmpBytes(test);
        int expected = kBmpHeaderSize + bmpRowSize(w) * 3;
        std::cout << "  " << w << ", " << file.size() << ", " << expected << ", "
                  << checkBmp(test, file) << " of " << w * 3 << "\n";
    }
    Image empty(0, 0);
    std::cout << "saving a 0 x 0 picture: " << (saveBMP(empty, "empty.bmp") ? "saved" : "refused")
              << "\n";

    Image gradient(256, 64);
    for (int x = 0; x < 256; ++x) {
        Colour c = lerpColour(colours::blue, colours::yellow, x / 255.0);
        for (int y = 0; y < 64; ++y) {
            gradient.setPixel(x, y, c);
        }
    }

    Image rainbow(301, 101);
    for (int x = 0; x < 301; ++x) {
        Colour c = toColour(hsvToRgb(HSV{x * 360.0 / 301.0, 1.0, 1.0}));
        for (int y = 0; y < 101; ++y) {
            rainbow.setPixel(x, y, c);
        }
    }

    Image heart(300, 300, Colour{255, 240, 245});
    std::vector<PointF> outline;
    appendCubic(outline, PointF{150.0, 260.0}, PointF{40.0, 180.0}, PointF{50.0, 40.0},
                PointF{150.0, 95.0});
    appendCubic(outline, PointF{150.0, 95.0}, PointF{250.0, 40.0}, PointF{260.0, 180.0},
                PointF{150.0, 260.0});
    fillPolygonAA(heart, outline, Colour{220, 30, 70});

    Image flower(300, 300, Colour{235, 245, 235});
    PointF middle{150.0, 150.0};
    for (int i = 0; i < 8; ++i) {
        double angle = degreesToRadians(i * 45.0);
        Colour col = toColour(hsvToRgb(HSV{320.0 + i * 5.0, 0.6, 0.95}));
        fillTiltedEllipseAA(flower, pointOnCircle(middle, 70.0, angle), 70.0, 24.0, angle, col);
    }
    fillCircleAA(flower, middle.x, middle.y, 30.0, Colour{250, 200, 40});

    const Image* pictures[4] = {&gradient, &rainbow, &heart, &flower};
    const std::string names[4] = {"gradient", "rainbow", "heart", "flower"};
    for (int i = 0; i < 4; ++i) {
        const Image& picture = *pictures[i];
        std::string bmpName = names[i] + ".bmp";
        std::string ppmName = names[i] + ".ppm";
        if (!saveBMP(picture, bmpName) || !picture.savePPM(ppmName)) {
            std::cout << "could not write " << names[i] << "\n";
            return 1;
        }
        Bytes back;
        int matches = readFileBytes(bmpName, back) ? checkBmp(picture, back) : -1;
        std::cout << names[i] << " " << picture.width() << " x " << picture.height() << ": BMP "
                  << fileSizeOf(bmpName) << " bytes, PPM " << fileSizeOf(ppmName)
                  << " bytes, read back: " << matches << " of "
                  << picture.width() * picture.height() << " pixels match\n";
    }
    if (!saveBMP(makeTestPattern(7, 3), "pattern.bmp")) {
        std::cout << "could not write pattern.bmp\n";
        return 1;
    }
    return 0;
}
```

Build and run (from the `code/ch37` folder):

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common write_bmp.cpp -o write_bmp
./write_bmp
```

### Line by line

**Checking a BMP (lines 1–32)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–5 | the `#include` lines | Printing, strings, the new header, and — for the pictures — `bezier.h` (which brings the whole drawing library) and `hsv.h`. The two header families can be used together. |
| 7–10 | `int checkBmp(const Image& image, const Bytes& file) { if (!hasBytes(file, 0, kBmpHeaderSize) \|\| file[0] != 'B' \|\| file[1] != 'M') { return -1; }` | The round-trip check (Section 37.5). First: are the headers there, and is it a BMP? |
| 11–13 | `int offset = static_cast<int>(getU32(file, 10)); int width = getS32(file, 18); int height = getS32(file, 22);` | Read the three fields a reader needs — from the **file**, not from the picture. |
| 14–16 | `if (width != image.width() \|\| height != image.height() \|\| getU16(file, 28) != 24) { return -1; }` | The size must match the picture, and the pixels must be 24-bit. |
| 17–18 | `int rowSize = bmpRowSize(width); int matches = 0;` | The row size, and a counter. |
| 19–21 | `for (int y = 0; ...) { for (int x = 0; ...) { int at = offset + (height - 1 - y) * rowSize + x * 3;` | For every pixel, where its bytes should be (Chapter 36, Section 36.9). |
| 22–24 | `if (!hasBytes(file, at, 3)) { return -1; }` | The file is too short: something is badly wrong. |
| 25–28 | `Colour c = image.getPixel(x, y); if (file[at] == c.b && file[at + 1] == c.g && file[at + 2] == c.r) { ++matches; }` | Compare B, G, R with the picture's colour. |
| 29–32 | `}` `}` `return matches;` `}` | How many pixels matched. |
| 34–40 | `long long fileSizeOf(const std::string& fileName) { Bytes bytes; if (!readFileBytes(fileName, bytes)) { return -1; } return static_cast<long long>(bytes.size()); }` | The size of a file on disk, using Chapter 12's `readFileBytes` (simple, if not the fastest way: it reads the whole file). |
| 42–52 | `Image makeTestPattern(int width, int height) { ... Colour{static_cast<std::uint8_t>(40 * x + 10), static_cast<std::uint8_t>(80 * y + 20), static_cast<std::uint8_t>(255 - 30 * x)} ... }` | A picture where every pixel has its own colour. For widths up to 7 and heights up to 3, all values stay between 0 and 255 (the biggest: 40 × 6 + 10 = 250, 80 × 2 + 20 = 180). |

**The tests (lines 54–65)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 55–62 | `for (int w = 1; w <= 7; ++w) { Image test = makeTestPattern(w, 3); Bytes file = makeBmpBytes(test); int expected = kBmpHeaderSize + bmpRowSize(w) * 3; std::cout << ... checkBmp(test, file) ... }` | Every padding case (Section 37.5): the size of the bytes, the size it should be, and the round trip — all in memory, no files yet. |
| 63–65 | `Image empty(0, 0); std::cout << ... (saveBMP(empty, "empty.bmp") ? "saved" : "refused") ...` | The empty edge case: it must be refused, and no `empty.bmp` is created. |

**Four pictures (lines 67–98)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 67–73 | `Image gradient(256, 64); for (int x = 0; x < 256; ++x) { Colour c = lerpColour(colours::blue, colours::yellow, x / 255.0); ... }` | Chapter 13's gradient: blue to yellow, one colour per column. |
| 75–81 | `Image rainbow(301, 101); ... toColour(hsvToRgb(HSV{x * 360.0 / 301.0, 1.0, 1.0})) ...` | Chapter 16's hue rainbow, deliberately 301 wide (1 byte of padding per row). |
| 83–89 | `Image heart(300, 300, ...); std::vector<PointF> outline; appendCubic(...); appendCubic(...); fillPolygonAA(...);` | Chapter 34's heart. |
| 91–98 | `Image flower(300, 300, ...); ... fillTiltedEllipseAA(flower, pointOnCircle(middle, 70.0, angle), 70.0, 24.0, angle, col); ... fillCircleAA(...);` | Chapter 31's flower. |

**Saving and checking them (lines 100–122)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 100–101 | `const Image* pictures[4] = {&gradient, &rainbow, &heart, &flower}; const std::string names[4] = {...};` | A list of **pointers** to the four pictures (so they are not copied), and their names. |
| 102–105 | `for (int i = 0; i < 4; ++i) { const Image& picture = *pictures[i]; std::string bmpName = names[i] + ".bmp"; std::string ppmName = names[i] + ".ppm";` | For each picture: a short name for it, and its two file names. |
| 106–109 | `if (!saveBMP(picture, bmpName) \|\| !picture.savePPM(ppmName)) { ... return 1; }` | Save it both ways. |
| 110–111 | `Bytes back; int matches = readFileBytes(bmpName, back) ? checkBmp(picture, back) : -1;` | Read the BMP back **from disk** and check every pixel. This also tests `writeBytes`. |
| 112–116 | `std::cout << names[i] << ... fileSizeOf(bmpName) << ... fileSizeOf(ppmName) << ...` | Print the sizes and the round-trip result (Section 37.6). |
| 117–122 | `if (!saveBMP(makeTestPattern(7, 3), "pattern.bmp")) { ... }` `return 0;` `}` | Save a tiny 7 × 3 test pattern too — zoom in on it in a viewer to see its 21 different colours. |

### What you should see

```
width, file size, expected size, pixels matching:
  1, 66, 66, 3 of 3
  2, 78, 78, 6 of 6
  3, 90, 90, 9 of 9
  4, 90, 90, 12 of 12
  5, 102, 102, 15 of 15
  6, 114, 114, 18 of 18
  7, 126, 126, 21 of 21
saving a 0 x 0 picture: refused
gradient 256 x 64: BMP 49206 bytes, PPM 49166 bytes, read back: 16384 of 16384 pixels match
rainbow 301 x 101: BMP 91358 bytes, PPM 91218 bytes, read back: 30401 of 30401 pixels match
heart 300 x 300: BMP 270054 bytes, PPM 270015 bytes, read back: 90000 of 90000 pixels match
flower 300 x 300: BMP 270054 bytes, PPM 270015 bytes, read back: 90000 of 90000 pixels match
```

And in the folder: `gradient.bmp`, `rainbow.bmp`, `heart.bmp`, `flower.bmp` and `pattern.bmp` (plus the four PPM files). Double-click a BMP: it opens in your normal picture viewer.

---

## Small examples

### Example 1 — The file size of a 1 × 1 BMP

Row size 4 (3 colour bytes + 1 padding) → 54 + 4 = **58** bytes, to store just 3 bytes of colour.

### Example 2 — Which widths need no padding?

Padding is 0 when 3 × width is a multiple of 4. Since 3 and 4 share no factor, that happens exactly when **width** is a multiple of 4: 4, 8, 12, …, 640, 1920.

### Example 3 — An HD picture

1920 × 1080: row size 5760 → pixel array 5760 × 1080 = 6,220,800 → file **6,220,854** bytes (about 6 MB).

### Example 4 — Too big

40,000 × 40,000: 3 × 40,000 × 40,000 = 4,800,000,000 bytes — more than 2,147,483,647. `bmpSizeIsOk` says no, and `saveBMP` returns `false` instead of writing a broken file.

### Example 5 — What a round-trip failure looks like

If `makeBmpBytes` forgot the padding (but still wrote the right sizes into the header), the width-1 test would print `1, 63, 66, -1 of 3`. The file is 1 byte short per row, 3 bytes in all. The bottom row (the first in the file) is still in the right place; the next row starts 1 byte too early, so its pixel does not match; and the top row, where the checker looks at bytes 62 to 64, runs past the end of the 63-byte file — so `checkBmp` gives up with −1.

---

## Common mistakes

⚠️ **Forgetting `std::ios::binary`.** On Windows, every 0x0A byte gains a 0x0D in front of it, and the file is ruined.

⚠️ **Testing only "nice" widths.** 100 × 100, 256 × 256, 640 × 480 all have no padding. Always test widths 1, 2, 3 and 5 too.

⚠️ **Writing a file for an empty picture.** Return `false` instead: a 0-wide BMP is not a picture.

⚠️ **Computing big sizes in `int`.** Check in `long long` first.

⚠️ **Trusting a round trip completely.** Writer and checker could share the same mistake. Also check one small file by hand (Chapter 36's hex dump) and open the files in a real viewer.

⚠️ **Arguments in the wrong order.** It is `saveBMP(image, "name.bmp")`. (Our `writeBytes` has the file name first: read each function's first line before using it.)

---

## Practice

🏋️ **1.** What is the file size of a 13 × 7 BMP? Check it with `makeBmpBytes(Image(13, 7)).size()`.

🏋️ **2.** Save the Chapter 26 colour triangle (or any of your favourite pictures) as BMP and open it in your normal viewer.

🏋️ **3.** Change `checkBmp` so it also checks that every **padding** byte is 0.

🏋️ **4.** Write `saveBMPTopDown`, which writes the rows top-down with a **negative** height (Chapter 36, Section 36.7). Do your viewers still show it the right way up?

🏋️ **5.** Write a 32-bit BMP: 4 bytes per pixel (B, G, R, and a fourth byte 255). What is the row size now — is any padding needed? Which header fields change?

🏋️ **6.** Change the "pixels per metre" fields to 11811 (300 dots per inch). Print a picture (or look at the file's properties in your system). Does the printed size change?

🏋️ **7.** Make a 2 × 2 BMP whose four pixels are red, green, blue and white, and write its hex dump by hand — then check it with Chapter 36's dump loop.

🏋️ **8.** How many bytes of padding does the 301 × 101 rainbow file contain in total? What fraction of the file is that?

---

## Answers

**1.**
> 13 × 3 = 39 → row size (39 + 3) / 4 × 4 = **40** → pixel array 40 × 7 = 280 → file **334** bytes.

**2.**
> `saveBMP(picture, "triangle.bmp");` — that is all. (Build the picture as in Chapter 26.)

**3.**

```cpp
for (int y = 0; y < height; ++y) {
    int rowStart = offset + (height - 1 - y) * rowSize;
    for (int p = width * 3; p < rowSize; ++p) {
        if (!hasBytes(file, rowStart + p, 1) || file[rowStart + p] != 0) {
            return -1;
        }
    }
}
```

**4.**
> Copy `makeBmpBytes`, change `putS32(file, height)` to `putS32(file, -height)`, and loop `for (int y = 0; y < height; ++y)`. Modern viewers (Windows Photos, browsers) show it the right way up. A few very old programs show it upside down, or refuse it — which is why the normal writer stays bottom-up.

**5.**
> Row size = 4 × width — always a multiple of 4, so **no padding** ever. Changes: bits per pixel **32**, and the sizes (pixel array = 4 × width × height, file size = 54 + that). Many programs ignore the fourth byte, and some treat it as alpha (Chapter 18's warning: support is poor). PNG (Chapter 42) is the proper way to store transparency.

**6.**
> Viewers on screen show it the same size (screens ignore the field). Some print dialogs and the "properties" of the file show a smaller physical size: 300 pixels at 300 dots per inch is 1 inch (2.54 cm) instead of about 4.2 inches at 72.

**7.**
> Row size 8 (6 + 2 padding), pixel array 16, file 70 = 0x46. The pixel bytes, bottom row first (blue, white), then top row (red, green):
> `FF 00 00  FF FF FF  00 00` · `00 00 FF  00 FF 00  00 00`

**8.**
> 1 byte per row × 101 rows = **101** bytes of padding, out of 91,358: about **0.11 %** of the file.

---

## Summary

🧠 `makeBmpBytes` = Chapter 36 with formulas: row size = **bmpRowSize(width)**, pixel array = row size × height, file size = **54** + pixel array.

🧠 Build the bytes in memory, then `writeBytes` them in **binary** mode. `saveBMP(image, fileName)` does both.

🧠 Refuse empty pictures and files over 2³¹ − 1 bytes (check sizes in **long long**).

🧠 Test with a **round trip**, and test **widths 1 to 7** to cover every padding case.

🧠 BMP and PPM are almost exactly the same size: 3 bytes per pixel, no compression. But **every** computer can open a BMP.

---

## Next chapter

We can write BMP files; now we read them. In Chapter 38 we write `loadBMP`, which opens a BMP made by **any** program — not just ours. That means being careful: checking the signature, the header size, the bits per pixel and the compression, making sure every size and offset stays **inside** the file, handling **top-down** files with a negative height, and skipping the padding. A reader must never trust a file.
