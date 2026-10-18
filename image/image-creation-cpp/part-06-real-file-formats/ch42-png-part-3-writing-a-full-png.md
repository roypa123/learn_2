# Chapter 42 — PNG, Part 3: Writing a Full PNG

> **Part 6 · Chapter 42 of 82**
> **You need:** Chapters 1–41 (especially 18, 27, 39, 40 and 41) · **You will make:** `pngfile.h` (`makePngRows`, `makePngBytes`, `savePNG`, `decodePNG` and `loadPNG`), and real PNG files that open in every browser: `tiny.png`, `heart.png`, a transparent `disk.png`, and `fade.png`, a rainbow that fades away

---

## What you will learn

- How all the pieces of Chapters 40 and 41 fit together into a complete PNG file.
- Every one of the 88 bytes of a tiny PNG.
- How to store **transparency**, and see it in a web browser.
- How to read our own PNG files back, with all the checks.
- Why our PNG files are (for now) a little **bigger** than BMP files.
- What the reader needs in order to open PNGs made by **other** programs (Chapters 43–45).

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **encoder** | A program part that writes a format (our `savePNG`). |
| **decoder** | A program part that reads a format (our `decodePNG`). |
| **conformant** | Following all the rules of a format, so every reader can open it. |
| **RGBA** | Red, green, blue and alpha: four bytes per pixel. |
| **premultiplied** | Colours already multiplied by their alpha (Chapter 18). PNG does **not** store them this way. |
| **unknown chunk** | A chunk type the reader has never heard of. |

---

## 42.1 Putting it together

📖 **New words: encoder and decoder** — the part of a program that **writes** a format is its **encoder**; the part that **reads** it is its **decoder**.

Our PNG encoder is just four steps, each from an earlier chapter:

```
   1. the signature                              Chapter 40   89 50 4E 47 0D 0A 1A 0A
   2. an IHDR chunk                              Chapter 40   width, height, 8, 2 or 6, 0, 0, 0
   3. an IDAT chunk holding:                     Chapter 40   (length, "IDAT", data, CRC)
        zlib (stored blocks) of                  Chapter 41   78 01, blocks, Adler-32
          the rows (a 0 byte + R G B (A) …)      Chapter 41   one row after another
   4. an IEND chunk                              Chapter 40   00 00 00 00 49 45 4E 44 AE 42 60 82
```

In code:

```cpp
appendPngSignature(file);
appendChunk(file, "IHDR", makeIhdr(width, height, alpha != nullptr));
appendChunk(file, "IDAT", zlibStore(makePngRows(image, alpha)));
appendChunk(file, "IEND", Bytes{});
```

📖 **New word: conformant** — a file that follows **all** the rules of its format, so **every** reader can open it. Our PNGs use only the simplest options (8-bit, no filters, stored blocks), but they are fully conformant: Chrome, Firefox, Safari, Windows Photos, macOS Preview, phones, paint programs — all open them.

---

## 42.2 A complete PNG, all 88 bytes

The 3 × 2 picture of Chapter 41 (red, green, blue on top; white, black, yellow below):

```
tiny.png, 88 bytes:
  00: 89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52
  10: 00 00 00 03 00 00 00 02 08 02 00 00 00 12 16 F1
  20: 4D 00 00 00 1F 49 44 41 54 78 01 01 14 00 EB FF
  30: 00 FF 00 00 00 FF 00 00 00 FF 00 FF FF FF 00 00
  40: 00 FF FF 00 49 CA 07 F9 33 EB 21 7D 00 00 00 00
  50: 49 45 4E 44 AE 42 60 82
```

| offset (hex) | bytes | meaning |
|---|---|---|
| 00 | 89 50 4E 47 0D 0A 1A 0A | signature |
| 08 | 00 00 00 0D · 49 48 44 52 | IHDR: 13 bytes of data |
| 10 | 00 00 00 03 · 00 00 00 02 · 08 02 00 00 00 | width 3, height 2, 8 bits, RGB, 0, 0, 0 |
| 1D | 12 16 F1 4D | IHDR's CRC |
| 21 | 00 00 00 1F · 49 44 41 54 | IDAT: 0x1F = **31** bytes of data |
| 29 | 78 01 | zlib header |
| 2B | 01 · 14 00 · EB FF | stored block: final; LEN 20; NLEN |
| 30 | 00 FF 00 00 00 FF 00 00 00 FF | row 0: filter 0, red, green, blue |
| 3A | 00 FF FF FF 00 00 00 FF FF 00 | row 1: filter 0, white, black, yellow |
| 44 | 49 CA 07 F9 | Adler-32 of the 20 row bytes |
| 48 | 33 EB 21 7D | IDAT's CRC |
| 4C | 00 00 00 00 · 49 45 4E 44 · AE 42 60 82 | IEND |

🔢 **Maths: the size**

> 8 (signature) + 25 (IHDR) + 12 + 31 (IDAT) + 12 (IEND) = **88** bytes ✓

Save it, double-click `tiny.png`, and zoom in: six coloured squares. (Viewers usually blur tiny pictures when enlarging; Chapter 35 explains why. Most have a "nearest neighbour" or "pixelated" option.)

---

## 42.3 Transparency

📖 **New word: RGBA** — with colour type **6**, each pixel has **four** bytes: **R, G, B, A**. A is alpha (Chapter 18): 0 = invisible, 255 = solid.

As in Chapter 39, our `Image` has no alpha, so `makePngRows` takes a separate list with one alpha byte per pixel (index y × width + x). If the list is missing or the wrong size, `makePngBytes` simply writes an ordinary RGB picture.

> **RGBA scanline = 1 + 4 × width bytes**

The program makes two transparent pictures:

- **`disk.png`**: the orange disk of Chapter 39 — alpha = the coverage of a circle of radius 80, so its edge is **smooth** against any background.
- **`fade.png`**: Chapter 37's rainbow, with alpha going from 255 at the top to 0 at the bottom: `255 − y × 255 / 100`.

Open them in a **web browser** (drag the files onto a browser window). The page behind shows through: the disk's square corners disappear, and the rainbow fades into the page colour. Try a dark-mode browser too: the same files look right on a dark background — that is what alpha is for.

📖 **New word: premultiplied** — Chapter 18 explained that colours can be stored "premultiplied" by their alpha. PNG does **not** do that: it stores the plain ("straight") colour and the alpha separately. That is why `disk.png` can keep the full orange colour even in the pixels whose alpha is 0 — the viewer multiplies by alpha when it draws.

---

## 42.4 How big are our PNGs?

```
heart: PNG 270388 bytes, BMP 270054 bytes
disk.png is 160278 bytes, fade.png is 121778 bytes
```

Our PNG is **bigger** than the BMP!

🔢 **Maths: where do the bytes go?**

> heart, 300 × 300 RGB: rows = 300 × (1 + 900) = 270,300 bytes (one filter byte per row)
> zlib = 270,300 + 2 + 5 × 5 + 4 = 270,331 (5 stored blocks, Chapter 41)
> PNG = 8 + 25 + (12 + 270,331) + 12 = **270,388**
> BMP = 54 + 900 × 300 = **270,054** (300 is a multiple of 4: no padding)

The extra 334 bytes are the filter bytes, the zlib and block headers, two checksums and three chunk headers. Stored blocks do no compression at all, so PNG can only be **bigger** than a plain format.

🔢 **Maths: the RGBA pictures**

> disk: 200 × (1 + 800) = 160,200 → 3 blocks → zlib 160,221 → PNG 8 + 25 + 12 + 160,221 + 12 = **160,278**
> fade: 101 × (1 + 1204) = 121,705 → 2 blocks → zlib 121,721 → PNG **121,778**

💡 The same heart saved by a paint program would be many times smaller: it is mostly two flat colours. Chapters 43 (filters), 44 (Huffman coding) and 45 (Deflate) close that gap — and the same `savePNG` will just call a better `zlib` function.

---

## 42.5 Reading our PNGs back

`decodePNG` reads PNG files — as long as they use only what we write. It checks, in order:

| # | check | message |
|---|---|---|
| 1 | the chunk walk of Chapter 40 (signature, every length inside the file) | e.g. "no PNG signature" |
| 2 | the first chunk is a 13-byte IHDR | "the first chunk must be a 13-byte IHDR" |
| 3 | the last chunk is IEND | "there is no IEND chunk" |
| 4 | every chunk's CRC is right | "the … chunk has a wrong CRC" |
| 5 | no **critical** chunk we do not know | "unknown critical chunk …" |
| 6 | width and height are 1 or more, at most 100 million pixels | "bad width or height" |
| 7 | 8-bit, colour type 2 or 6 | "only 8-bit RGB and RGBA pictures are supported" |
| 8 | compression, filter and interlace methods are 0 | "unknown compression, filter or interlace method" |
| 9 | the zlib data unpacks (Chapter 41's checks) | "IDAT: …" |
| 10 | exactly height × (1 + bytes per pixel × width) bytes | "wrong amount of pixel data" |
| 11 | every row's filter byte is 0 | "row filters are not supported yet" |

### Several IDAT chunks

📖 A PNG may split its zlib data over **several** IDAT chunks (many programs use chunks of 8 KB or 64 KB). The split can be anywhere — even in the middle of a block. So the decoder first **joins** the data of all IDAT chunks, in order, and only then unpacks the zlib data.

### Unknown chunks

📖 **New word: unknown chunk** — other programs add chunks we never write: `sRGB`, `gAMA`, `pHYs`, `tEXt`, `tIME`, … Chapter 40's rule: an **ancillary** chunk (small first letter) can be **skipped** safely, and our decoder simply ignores it. A **critical** chunk (capital first letter) that we do not know means the picture cannot be shown correctly, so we refuse it. (`PLTE`, the palette, is critical but only needed for colour type 3; for RGB pictures it is just a suggestion, and we ignore it.)

### Tests

```
read back: all loaded, heart same, disk same, fade same
broken PNG files:
  the good file: accepted
  width changed: refused (the IHDR chunk has a wrong CRC)
  colour type 3: refused (only 8-bit RGB and RGBA pictures are supported)
  16 bits per channel: refused (only 8-bit RGB and RGBA pictures are supported)
  row 1 uses filter 1: refused (row filters are not supported yet)
  one row missing: refused (wrong amount of pixel data)
  no IEND: refused (there is no IEND chunk)
```

The broken files are made two ways: by changing one byte of a good file (so the CRC catches it), or by building a whole new file with `pngFromParts`, which writes **correct** CRCs around wrong contents — to reach the checks **behind** the CRC check.

---

## 42.6 What about PNGs from other programs?

Try loading a PNG made by a paint program or a screenshot tool: `loadPNG` will almost certainly refuse it, with "IDAT: compressed blocks are not supported yet". Real PNGs are **compressed**, and most of their rows use **filters**. Here is what our decoder still needs, and where it comes:

| missing | chapter |
|---|---|
| row filters 1–4 (Sub, Up, Average, Paeth) | 43 |
| Huffman codes | 44 |
| Deflate's compressed blocks (types 1 and 2) | 45 |
| grey, palette and 16-bit pictures, interlacing | not in this book (a Practice idea) |

But our **encoder** is already complete: every PNG it writes is a real PNG.

---

## Code, part 1: `pngfile.h`

File: `common/pngfile.h` (new). It includes `zlib.h`.

```cpp
#ifndef PNGFILE_H
#define PNGFILE_H

#include <cstdint>
#include <string>
#include <vector>
#include "zlib.h"

inline Bytes makePngRows(const Image& image, const std::vector<std::uint8_t>* alpha) {
    Bytes rows;
    const int width = image.width();
    const bool withAlpha = alpha != nullptr;
    for (int y = 0; y < image.height(); ++y) {
        rows.push_back(0);
        for (int x = 0; x < width; ++x) {
            Colour c = image.getPixel(x, y);
            rows.push_back(c.r);
            rows.push_back(c.g);
            rows.push_back(c.b);
            if (withAlpha) {
                rows.push_back((*alpha)[y * width + x]);
            }
        }
    }
    return rows;
}

inline Bytes makePngBytes(const Image& image, const std::vector<std::uint8_t>* alpha = nullptr) {
    Bytes file;
    const int width = image.width();
    const int height = image.height();
    if (width <= 0 || height <= 0) {
        return file;
    }
    if (alpha != nullptr && static_cast<int>(alpha->size()) != width * height) {
        alpha = nullptr;
    }
    const int bytesPerPixel = (alpha != nullptr) ? 4 : 3;
    if ((1LL + bytesPerPixel * static_cast<long long>(width)) * height > 1000000000LL) {
        return file;
    }
    appendPngSignature(file);
    appendChunk(file, "IHDR", makeIhdr(width, height, alpha != nullptr));
    appendChunk(file, "IDAT", zlibStore(makePngRows(image, alpha)));
    appendChunk(file, "IEND", Bytes{});
    return file;
}

inline bool savePNG(const Image& image, const std::string& fileName,
                    const std::vector<std::uint8_t>* alpha = nullptr) {
    Bytes file = makePngBytes(image, alpha);
    if (file.empty()) {
        return false;
    }
    return writeBytes(fileName, file);
}

inline bool isKnownChunk(const std::string& type) {
    return type == "IHDR" || type == "IDAT" || type == "IEND" || type == "PLTE";
}

inline std::string decodePNG(const Bytes& file, Image& image,
                             std::vector<std::uint8_t>* alpha = nullptr) {
    std::vector<PngChunk> chunks;
    const std::string problem = listChunks(file, chunks);
    if (!problem.empty()) {
        return problem;
    }
    if (chunks.empty() || chunks[0].type != "IHDR" || chunks[0].length != 13) {
        return "the first chunk must be a 13-byte IHDR";
    }
    if (chunks.back().type != "IEND") {
        return "there is no IEND chunk";
    }
    Bytes zdata;
    for (const PngChunk& c : chunks) {
        if (!c.crcOk) {
            return "the " + c.type + " chunk has a wrong CRC";
        }
        const bool critical = c.type[0] >= 'A' && c.type[0] <= 'Z';
        if (critical && !isKnownChunk(c.type)) {
            return "unknown critical chunk " + c.type;
        }
        if (c.type == "IDAT") {
            zdata.insert(zdata.end(), file.begin() + c.dataStart,
                         file.begin() + c.dataStart + c.length);
        }
    }

    const int d = chunks[0].dataStart;
    const std::uint32_t width = getU32BE(file, d);
    const std::uint32_t height = getU32BE(file, d + 4);
    const int bitDepth = file[d + 8];
    const int colourType = file[d + 9];
    if (width == 0 || height == 0 || static_cast<long long>(width) * height > 100000000LL) {
        return "bad width or height";
    }
    if (bitDepth != 8 || (colourType != 2 && colourType != 6)) {
        return "only 8-bit RGB and RGBA pictures are supported";
    }
    if (file[d + 10] != 0 || file[d + 11] != 0 || file[d + 12] != 0) {
        return "unknown compression, filter or interlace method";
    }

    Bytes rows;
    const std::string zproblem = zlibUnstore(zdata, rows);
    if (!zproblem.empty()) {
        return "IDAT: " + zproblem;
    }
    const int w = static_cast<int>(width);
    const int h = static_cast<int>(height);
    const int bytesPerPixel = (colourType == 6) ? 4 : 3;
    const long long rowBytes = 1 + static_cast<long long>(bytesPerPixel) * w;
    if (static_cast<long long>(rows.size()) != rowBytes * h) {
        return "wrong amount of pixel data";
    }

    Image result(w, h);
    std::vector<std::uint8_t> alphaResult(w * h, 255);
    for (int y = 0; y < h; ++y) {
        const int start = static_cast<int>(y * rowBytes);
        if (rows[start] != 0) {
            return "row filters are not supported yet";
        }
        for (int x = 0; x < w; ++x) {
            const int at = start + 1 + x * bytesPerPixel;
            result.setPixel(x, y, Colour{rows[at], rows[at + 1], rows[at + 2]});
            if (bytesPerPixel == 4) {
                alphaResult[y * w + x] = rows[at + 3];
            }
        }
    }
    image = result;
    if (alpha != nullptr) {
        *alpha = alphaResult;
    }
    return "";
}

inline bool loadPNG(const std::string& fileName, Image& image,
                    std::vector<std::uint8_t>* alpha = nullptr) {
    Bytes file;
    if (!readFileBytes(fileName, file)) {
        return false;
    }
    return decodePNG(file, image, alpha).empty();
}

#endif
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–7 | include guard and `#include` lines | Exact-size integers, strings, lists, and everything from Chapters 36–41. |
| 9–12 | `inline Bytes makePngRows(const Image& image, const std::vector<std::uint8_t>* alpha) { Bytes rows; const int width = image.width(); const bool withAlpha = alpha != nullptr;` | The PNG row bytes (Section 42.3). The caller has already made sure the alpha list has the right size. |
| 13–14 | `for (int y = 0; y < image.height(); ++y) { rows.push_back(0);` | Rows top-down; each starts with filter byte 0. |
| 15–23 | `for (int x = 0; ...) { Colour c = image.getPixel(x, y); rows.push_back(c.r); rows.push_back(c.g); rows.push_back(c.b); if (withAlpha) { rows.push_back((*alpha)[y * width + x]); } }` | R, G, B (and A) for every pixel — the normal order, no padding. |
| 24–26 | `}` `return rows;` `}` | Done. |
| 28–34 | `inline Bytes makePngBytes(const Image& image, const std::vector<std::uint8_t>* alpha = nullptr) { ... if (width <= 0 \|\| height <= 0) { return file; }` | Build a complete PNG. An empty picture cannot be a PNG (IHDR needs width and height ≥ 1). |
| 35–37 | `if (alpha != nullptr && static_cast<int>(alpha->size()) != width * height) { alpha = nullptr; }` | A wrong-sized alpha list is ignored: write plain RGB. (`alpha` is our own copy of the pointer, so we may change it.) |
| 38–41 | `const int bytesPerPixel = ...; if ((1LL + bytesPerPixel * static_cast<long long>(width)) * height > 1000000000LL) { return file; }` | Refuse pictures whose rows would be over a billion bytes (computed in `long long`). |
| 42–47 | the four `append…` lines, `return file;` `}` | Signature, IHDR (colour type 6 if there is alpha), IDAT and IEND (Section 42.1). |
| 49–56 | `inline bool savePNG(const Image& image, const std::string& fileName, const std::vector<std::uint8_t>* alpha = nullptr) { ... }` | Build and write. The same shape as `saveBMP` and `saveTGA`. |
| 58–60 | `inline bool isKnownChunk(const std::string& type) { return type == "IHDR" \|\| ... \|\| type == "PLTE"; }` | The critical chunks we accept. |
| 62–68 | `inline std::string decodePNG(const Bytes& file, Image& image, std::vector<std::uint8_t>* alpha = nullptr) { std::vector<PngChunk> chunks; const std::string problem = listChunks(file, chunks); if (!problem.empty()) { return problem; }` | Read a PNG (Section 42.5). Check 1: walk the chunks. |
| 69–74 | the IHDR and IEND checks | Checks 2 and 3. |
| 75–88 | `Bytes zdata; for (const PngChunk& c : chunks) { if (!c.crcOk) { ... } const bool critical = c.type[0] >= 'A' && c.type[0] <= 'Z'; if (critical && !isKnownChunk(c.type)) { ... } if (c.type == "IDAT") { zdata.insert(...); } }` | Checks 4 and 5, and join the data of all IDAT chunks in order. A capital first letter means critical. |
| 90–94 | `const int d = chunks[0].dataStart; const std::uint32_t width = getU32BE(file, d); ... const int colourType = file[d + 9];` | Read the IHDR fields (Chapter 40, Section 40.5). |
| 95–103 | three checks | Checks 6, 7 and 8. |
| 105–109 | `Bytes rows; const std::string zproblem = zlibUnstore(zdata, rows); if (!zproblem.empty()) { return "IDAT: " + zproblem; }` | Check 9: unpack the zlib data (Chapter 41). |
| 110–116 | `const int w = ...; const int h = ...; const int bytesPerPixel = (colourType == 6) ? 4 : 3; const long long rowBytes = 1 + ...; if (static_cast<long long>(rows.size()) != rowBytes * h) { ... }` | Check 10: exactly the right number of row bytes. |
| 118–119 | `Image result(w, h); std::vector<std::uint8_t> alphaResult(w * h, 255);` | The picture, and alpha (255 = solid, for RGB files). |
| 120–124 | `for (int y = 0; y < h; ++y) { const int start = static_cast<int>(y * rowBytes); if (rows[start] != 0) { return "row filters are not supported yet"; }` | Check 11, row by row: the filter byte. |
| 125–132 | `for (int x = 0; ...) { const int at = start + 1 + x * bytesPerPixel; result.setPixel(x, y, Colour{rows[at], rows[at + 1], rows[at + 2]}); if (bytesPerPixel == 4) { alphaResult[y * w + x] = rows[at + 3]; } } }` | Copy the pixels: R, G, B in order (no swapping this time!), and A. |
| 133–138 | `image = result; if (alpha != nullptr) { *alpha = alphaResult; } return "";` `}` | Hand back the picture (and the alpha, if asked). |
| 140–147 | `inline bool loadPNG(...) { Bytes file; if (!readFileBytes(fileName, file)) { return false; } return decodePNG(file, image, alpha).empty(); }` | Read a file and decode it. |
| 149 | `#endif` | End of the include guard. |

---

## Code, part 2: real PNG files

File: `ch42/write_png.cpp`

```cpp
#include <iostream>
#include <string>
#include <vector>
#include "pngfile.h"
#include "bezier.h"
#include "hsv.h"

bool samePictures(const Image& a, const Image& b) {
    if (a.width() != b.width() || a.height() != b.height()) {
        return false;
    }
    for (int y = 0; y < a.height(); ++y) {
        for (int x = 0; x < a.width(); ++x) {
            Colour p = a.getPixel(x, y);
            Colour q = b.getPixel(x, y);
            if (p.r != q.r || p.g != q.g || p.b != q.b) {
                return false;
            }
        }
    }
    return true;
}

Bytes pngFromParts(int width, int height, int bitDepth, int colourType, const Bytes& rows) {
    Bytes file;
    appendPngSignature(file);
    Bytes ihdr = makeIhdr(width, height, false);
    ihdr[8] = static_cast<std::uint8_t>(bitDepth);
    ihdr[9] = static_cast<std::uint8_t>(colourType);
    appendChunk(file, "IHDR", ihdr);
    appendChunk(file, "IDAT", zlibStore(rows));
    appendChunk(file, "IEND", Bytes{});
    return file;
}

void report(const char* label, const Bytes& file) {
    Image ignored(0, 0);
    std::string problem = decodePNG(file, ignored);
    std::cout << "  " << label << ": " << (problem.empty() ? "accepted" : "refused (" + problem + ")")
              << "\n";
}

int main() {
    Image tiny(3, 2);
    tiny.setPixel(0, 0, colours::red);
    tiny.setPixel(1, 0, colours::green);
    tiny.setPixel(2, 0, colours::blue);
    tiny.setPixel(0, 1, colours::white);
    tiny.setPixel(2, 1, colours::yellow);
    Bytes tinyPng = makePngBytes(tiny);
    std::cout << "tiny.png, " << tinyPng.size() << " bytes:\n";
    for (int i = 0; i < static_cast<int>(tinyPng.size()); i += 16) {
        std::cout << "  " << hexByte(static_cast<std::uint8_t>(i)) << ":";
        for (int j = i; j < i + 16 && j < static_cast<int>(tinyPng.size()); ++j) {
            std::cout << " " << hexByte(tinyPng[j]);
        }
        std::cout << "\n";
    }

    Image heart(300, 300, Colour{255, 240, 245});
    std::vector<PointF> outline;
    appendCubic(outline, PointF{150.0, 260.0}, PointF{40.0, 180.0}, PointF{50.0, 40.0},
                PointF{150.0, 95.0});
    appendCubic(outline, PointF{150.0, 95.0}, PointF{250.0, 40.0}, PointF{260.0, 180.0},
                PointF{150.0, 260.0});
    fillPolygonAA(heart, outline, Colour{220, 30, 70});

    Image disk(200, 200, Colour{250, 140, 30});
    std::vector<std::uint8_t> diskAlpha(200 * 200);
    for (int y = 0; y < 200; ++y) {
        for (int x = 0; x < 200; ++x) {
            diskAlpha[y * 200 + x] = toByte(circleCoverage(100.0, 100.0, 80.0, x, y, 4));
        }
    }

    Image rainbow(301, 101);
    std::vector<std::uint8_t> fadeAlpha(301 * 101);
    for (int y = 0; y < 101; ++y) {
        for (int x = 0; x < 301; ++x) {
            rainbow.setPixel(x, y, toColour(hsvToRgb(HSV{x * 360.0 / 301.0, 1.0, 1.0})));
            fadeAlpha[y * 301 + x] = static_cast<std::uint8_t>(255 - y * 255 / 100);
        }
    }

    if (!savePNG(tiny, "tiny.png") || !savePNG(heart, "heart.png") ||
        !savePNG(disk, "disk.png", &diskAlpha) || !savePNG(rainbow, "fade.png", &fadeAlpha) ||
        !saveBMP(heart, "heart.bmp")) {
        std::cout << "could not write the files\n";
        return 1;
    }
    std::cout << "heart: PNG " << makePngBytes(heart).size() << " bytes, BMP "
              << makeBmpBytes(heart).size() << " bytes\n";

    Image heartBack(0, 0);
    Image diskBack(0, 0);
    std::vector<std::uint8_t> diskAlphaBack;
    Image fadeBack(0, 0);
    std::vector<std::uint8_t> fadeAlphaBack;
    bool ok = loadPNG("heart.png", heartBack) && loadPNG("disk.png", diskBack, &diskAlphaBack) &&
              loadPNG("fade.png", fadeBack, &fadeAlphaBack);
    std::cout << "read back: " << (ok ? "all loaded" : "LOAD FAILED") << ", heart "
              << (samePictures(heart, heartBack) ? "same" : "DIFFERENT") << ", disk "
              << (samePictures(disk, diskBack) && diskAlpha == diskAlphaBack ? "same" : "DIFFERENT")
              << ", fade "
              << (samePictures(rainbow, fadeBack) && fadeAlpha == fadeAlphaBack ? "same" : "DIFFERENT")
              << "\n";
    std::cout << "disk.png is " << makePngBytes(disk, &diskAlpha).size() << " bytes, fade.png is "
              << makePngBytes(rainbow, &fadeAlpha).size() << " bytes\n";

    std::cout << "broken PNG files:\n";
    report("the good file", tinyPng);
    Bytes wrong = tinyPng;
    wrong[19] = 9;
    report("width changed", wrong);
    Bytes rows = makePngRows(tiny, nullptr);
    report("colour type 3", pngFromParts(3, 2, 8, 3, rows));
    report("16 bits per channel", pngFromParts(3, 2, 16, 2, rows));
    Bytes filtered = rows;
    filtered[10] = 1;
    report("row 1 uses filter 1", pngFromParts(3, 2, 8, 2, filtered));
    report("one row missing", pngFromParts(3, 3, 8, 2, rows));
    wrong = tinyPng;
    wrong.resize(wrong.size() - 12);
    report("no IEND", wrong);
    return 0;
}
```

Build and run (from the `code/ch42` folder):

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common write_png.cpp -o write_png
./write_png
```

### Line by line

**Helpers (lines 1–41)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–6 | the `#include` lines | Printing, strings, lists, the new header, the drawing library (`bezier.h`) and `hsv.h`. |
| 8–22 | `bool samePictures(const Image& a, const Image& b) { ... }` | Are two pictures exactly the same? (Chapter 39.) |
| 24–34 | `Bytes pngFromParts(int width, int height, int bitDepth, int colourType, const Bytes& rows) { ... ihdr[8] = ...; ihdr[9] = ...; ... }` | Build a PNG with any IHDR values and any row bytes — with **correct** CRCs and Adler-32 — so that we can test the decoder's later checks (Section 42.5). Bytes 8 and 9 of IHDR's data are the bit depth and colour type. |
| 36–41 | `void report(const char* label, const Bytes& file) { ... }` | Decode and print "accepted" or the reason. |

**The tiny PNG (lines 43–58)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 44–49 | `Image tiny(3, 2); ...` | Chapter 41's 3 × 2 picture. |
| 50–58 | `Bytes tinyPng = makePngBytes(tiny);` and the dump loop | All 88 bytes (Section 42.2). |

**Three more pictures (lines 60–83)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 60–66 | `Image heart(300, 300, ...); ... fillPolygonAA(heart, outline, ...);` | Chapter 34's heart. |
| 68–74 | `Image disk(200, 200, Colour{250, 140, 30}); std::vector<std::uint8_t> diskAlpha(200 * 200); ... diskAlpha[y * 200 + x] = toByte(circleCoverage(100.0, 100.0, 80.0, x, y, 4)); ...` | The orange disk with alpha = coverage (Chapter 39). |
| 76–83 | `Image rainbow(301, 101); std::vector<std::uint8_t> fadeAlpha(301 * 101); ... rainbow.setPixel(x, y, toColour(hsvToRgb(HSV{x * 360.0 / 301.0, 1.0, 1.0}))); fadeAlpha[y * 301 + x] = static_cast<std::uint8_t>(255 - y * 255 / 100); ...` | The rainbow, fading from solid (y = 0) to invisible (y = 100). |

**Saving and sizes (lines 85–92)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 85–90 | `if (!savePNG(tiny, "tiny.png") \|\| !savePNG(heart, "heart.png") \|\| !savePNG(disk, "disk.png", &diskAlpha) \|\| !savePNG(rainbow, "fade.png", &fadeAlpha) \|\| !saveBMP(heart, "heart.bmp")) { ... }` | Write four PNG files (two with alpha) and a BMP for comparison. |
| 91–92 | `std::cout << "heart: PNG " << makePngBytes(heart).size() << ... makeBmpBytes(heart).size() ...` | The sizes of Section 42.4. |

**Reading back (lines 94–108)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 94–100 | `Image heartBack(0, 0); ... bool ok = loadPNG("heart.png", heartBack) && loadPNG("disk.png", diskBack, &diskAlphaBack) && loadPNG("fade.png", fadeBack, &fadeAlphaBack);` | Load three of the files from disk, with their alpha. |
| 101–106 | `std::cout << "read back: " << ... samePictures(disk, diskBack) && diskAlpha == diskAlphaBack ...` | Pixels **and** alpha must match exactly. |
| 107–108 | `std::cout << "disk.png is " << makePngBytes(disk, &diskAlpha).size() << ...` | The sizes of the RGBA files. |

**Broken files (lines 110–126)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 111 | `report("the good file", tinyPng);` | It must be accepted. |
| 112–114 | `Bytes wrong = tinyPng; wrong[19] = 9; report(...);` | Byte 0x13 is the low byte of the width: the IHDR CRC catches it. |
| 115–117 | `Bytes rows = makePngRows(tiny, nullptr); report("colour type 3", pngFromParts(3, 2, 8, 3, rows)); report("16 bits per channel", pngFromParts(3, 2, 16, 2, rows));` | A palette picture and a 16-bit picture: not supported. |
| 118–120 | `Bytes filtered = rows; filtered[10] = 1; report(...);` | Byte 10 is the filter byte of row 1 (row 0 takes bytes 0–9). |
| 121 | `report("one row missing", pngFromParts(3, 3, 8, 2, rows));` | IHDR says 3 rows, but the data has 2. |
| 122–124 | `wrong = tinyPng; wrong.resize(wrong.size() - 12); report("no IEND", wrong);` | Remove the 12-byte IEND chunk. |
| 125–126 | `return 0;` `}` | Done. |

### What you should see

```
tiny.png, 88 bytes:
  00: 89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52
  10: 00 00 00 03 00 00 00 02 08 02 00 00 00 12 16 F1
  20: 4D 00 00 00 1F 49 44 41 54 78 01 01 14 00 EB FF
  30: 00 FF 00 00 00 FF 00 00 00 FF 00 FF FF FF 00 00
  40: 00 FF FF 00 49 CA 07 F9 33 EB 21 7D 00 00 00 00
  50: 49 45 4E 44 AE 42 60 82
heart: PNG 270388 bytes, BMP 270054 bytes
read back: all loaded, heart same, disk same, fade same
disk.png is 160278 bytes, fade.png is 121778 bytes
broken PNG files:
  the good file: accepted
  width changed: refused (the IHDR chunk has a wrong CRC)
  colour type 3: refused (only 8-bit RGB and RGBA pictures are supported)
  16 bits per channel: refused (only 8-bit RGB and RGBA pictures are supported)
  row 1 uses filter 1: refused (row filters are not supported yet)
  one row missing: refused (wrong amount of pixel data)
  no IEND: refused (there is no IEND chunk)
```

And five files. Open `disk.png` and `fade.png` in a browser to see the transparency.

---

## Small examples

### Example 1 — The size of an uncompressed PNG

A 64 × 64 RGBA icon: rows 64 × (1 + 256) = 16,448 → 1 block → zlib 16,448 + 11 = 16,459 → PNG 8 + 25 + 12 + 16,459 + 12 = **16,516** bytes.

### Example 2 — The smallest PNG

A 1 × 1 RGB picture: rows 4 bytes → zlib 15 → PNG 8 + 25 + 27 + 12 = **72** bytes.

### Example 3 — Reading the colour type

IHDR data `00 00 01 00 00 00 00 80 08 06 00 00 00`: width 256, height 128, 8 bits, colour type **6** (RGBA).

### Example 4 — Half-transparent white

A pixel `FF FF FF 80` in an RGBA row: white, alpha 128 — about half see-through. On a black page it looks mid-grey; on a white page, pure white.

### Example 5 — Chunk order

IHDR first, IEND last, IDAT chunks **together** (no other chunk between two IDATs), and PLTE (if any) before the first IDAT. Ancillary chunks may go in between, with a few rules of their own.

---

## Common mistakes

⚠️ **Forgetting the filter byte** — the picture comes out slanted and shifted.

⚠️ **B, G, R order** (from BMP habit) — PNG is **R, G, B**.

⚠️ **The wrong colour type** — writing 4 bytes per pixel with colour type 2 (or 3 bytes with type 6) makes the "wrong amount of data" error in every viewer.

⚠️ **CRC over the length** — the CRC covers type + data only (Chapter 40).

⚠️ **Splitting zlib data per row.** All the rows go into **one** zlib stream (which can then be cut into several IDAT chunks anywhere).

⚠️ **Thinking an RGB PNG has alpha 255 in the file.** RGB files have no alpha byte at all; "255" is just what the decoder reports.

⚠️ **Refusing ancillary chunks.** Skip unknown chunks with a small first letter; only unknown **critical** chunks are a problem.

---

## Practice

🏋️ **1.** Compute the file size of an uncompressed 100 × 50 RGB PNG and the matching BMP.

🏋️ **2.** Write `savePNG` for a picture with a **single** alpha value for every pixel (for example, a 50 %-transparent photo).

🏋️ **3.** Convert every BMP in a folder to PNG (one at a time, by name): `loadBMP`, then `savePNG`.

🏋️ **4.** Add a `tEXt` chunk with "Software" + 0 + "my picture program" between IHDR and IDAT. Do viewers still open the file? Does `decodePNG`?

🏋️ **5.** Change `makePngBytes` to split the zlib data into IDAT chunks of at most 8,192 bytes. Check that browsers and `decodePNG` still read it.

🏋️ **6.** Make a "glass ball": a blue disk whose alpha is 255 at the edge and 100 in the middle (alpha = lerp(100, 255, distance / radius)), times the coverage.

🏋️ **7.** Write a grey PNG (colour type 0: one byte per pixel) for a `Image` that is already grey. How many bytes do you save?

🏋️ **8.** Why must the decoder join all IDAT data **before** unpacking it, instead of unpacking each IDAT on its own?

---

## Answers

**1.**
> rows: 50 × (1 + 300) = 15,050 → 1 block → zlib 15,061 → PNG 8 + 25 + 12 + 15,061 + 12 = **15,118** bytes.
> BMP: row size 300 (a multiple of 4) → 54 + 300 × 50 = **15,054** bytes.

**2.**

```cpp
bool savePNGWithAlpha(const Image& image, const std::string& fileName, std::uint8_t a) {
    std::vector<std::uint8_t> alpha(image.width() * image.height(), a);
    return savePNG(image, fileName, &alpha);
}
```

**3.**

```cpp
Image picture(0, 0);
if (loadBMP("photo.bmp", picture) && savePNG(picture, "photo.png")) {
    std::cout << "converted\n";
}
```

**4.**
> Insert `appendChunk(file, "tEXt", text);` after the IHDR line (building `text` as in Chapter 40, Practice 5). Viewers ignore it (some show it in "file properties"); `decodePNG` skips it, because 't' is a small letter.

**5.**

```cpp
Bytes z = zlibStore(makePngRows(image, alpha));
for (int pos = 0; pos < static_cast<int>(z.size()); pos += 8192) {
    int end = std::min(pos + 8192, static_cast<int>(z.size()));
    appendChunk(file, "IDAT", Bytes(z.begin() + pos, z.begin() + end));
}
```

> Both read it: the decoder joins the IDAT data first (Section 42.5). The file is 12 bytes bigger per extra chunk.

**6.**

```cpp
double d = distance(Vec2{x + 0.5, y + 0.5}, Vec2{100.0, 100.0});
double a = lerp(100.0, 255.0, std::min(1.0, d / 80.0));
double coverage = circleCoverage(100.0, 100.0, 80.0, x, y, 4);
alpha[y * 200 + x] = static_cast<std::uint8_t>(a * coverage + 0.5);
```

**7.**
> Write IHDR with colour type 0, and each row as 1 filter byte + 1 byte per pixel (the grey value, for example `c.r`). A 300 × 300 grey picture: rows 300 × 301 = 90,300 bytes instead of 270,300 — about **two thirds** smaller.

**8.**
> The split into IDAT chunks can be anywhere — in the middle of a block header, or even in the middle of the Adler-32. A single IDAT is usually not valid zlib data on its own; only all of them together, in order, are.

---

## Summary

🧠 A PNG = **signature + IHDR + IDAT(zlib(rows)) + IEND**. Our version: 8-bit, colour type 2 (RGB) or 6 (RGBA), filter byte 0, stored blocks — simple, and **conformant**: every program opens it.

🧠 Rows: **1 + 3w** (RGB) or **1 + 4w** (RGBA) bytes, colours in **R, G, B (A)** order, not premultiplied.

🧠 Transparency works in every browser. For smooth shapes, **alpha = coverage**.

🧠 Uncompressed PNG is a little **bigger** than BMP. Compression comes in Chapters 43–45.

🧠 The decoder: walk chunks, check IHDR/IEND/CRCs, skip ancillary chunks, refuse unknown critical ones, **join all IDATs**, unpack zlib, check the size and each filter byte.

---

## Next chapter

Why would anyone compress pixels **differently** from text? Because neighbouring pixels are usually **similar**, not equal. In Chapter 43 we meet PNG's five **filters** — None, Sub, Up, Average and Paeth — which replace each byte by its **difference** from a neighbour. A smooth gradient becomes a long list of zeros and small numbers, which the compression of Chapters 44–45 can squeeze very well. We will write all five filters, their reverse, and a rule for choosing the best filter for each row.
