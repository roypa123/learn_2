# Chapter 39 — The TGA Format

> **Part 6 · Chapter 39 of 82**
> **You need:** Chapters 1–38 (especially 18, 27, 36 and 38) · **You will make:** `tga.h` (a run-length encoder, `makeTgaBytes`, `saveTGA`, `decodeTGA` and `loadTGA`), `flag.tga`, `sky.tga`, `noise.tga`, and `disk.tga` — a smooth orange disk with **real transparency**

---

## What you will learn

- What a **TGA** file is, and where it is used.
- Its small 18-byte header, field by field.
- How TGA stores **alpha** (transparency) properly — something BMP does badly.
- Our very first **compression** method: **run-length encoding** (RLE).
- How RLE **packets** work, how to write an encoder and a decoder, and how to read the bytes by hand.
- When compression helps a lot, and when it makes files **bigger**.
- How to read a compressed file safely.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **TGA** (Targa) | A simple picture format from the 1980s, still used in games and 3D programs. |
| **true-colour** | Each pixel stores its own colour (not a number pointing into a colour table). |
| **colour map** (palette) | A table of colours; pixels store a position in the table instead of a colour. |
| **image descriptor** | The last header byte: how many alpha bits, and which corner the pixels start from. |
| **compression** | Storing the same information in fewer bytes. |
| **lossless** | Compression that gives back **exactly** the original. |
| **run** | Several equal things one after another, like "red, red, red, red". |
| **run-length encoding** (RLE) | Storing a run as "how many" + "what", instead of repeating it. |
| **packet** | One piece of an RLE stream: a header byte, followed by pixel bytes. |
| **raw packet** | A packet that lists several different pixels as they are. |
| **compression ratio** | Original size ÷ compressed size: how many times smaller. |

---

## 39.1 What is TGA?

📖 **New word: TGA** — short for **Truevision Graphics Adapter** (also called **Targa**), the format made in 1984 for Truevision's graphics cards. It is still popular in **games** and **3D programs** for textures, because it is simple, fast to read, and stores **alpha** well.

Compared with BMP (Chapters 36–38):

| | BMP | TGA |
|---|---|---|
| header | 54 bytes | **18** bytes |
| numbers | little-endian | little-endian (the same!) |
| colour order | B, G, R | B, G, R (the same!) |
| rows | bottom-up (or top-down) | bottom-up **or top-down**, chosen by one bit |
| row padding | to a multiple of 4 | **none** |
| alpha | poorly supported | **well supported** (32-bit, 8 alpha bits) |
| compression | rarely used | simple **RLE** is common |
| signature | "BM" | **none** at the start (Section 39.3) |

⚠️ Many everyday viewers (for example Windows Photos) do **not** open TGA files. Free programs like **GIMP**, Krita, Paint.NET (with a plugin), and most game and 3D tools do. That is the price of a format made for specialists.

---

## 39.2 The 18-byte header

📖 **New words: true-colour and colour map** — in a **true-colour** picture each pixel stores its own colour. Old formats could also use a **colour map** (a palette): a table of, say, 256 colours, with each pixel storing just a number from 0 to 255. We only use true-colour.

| offset | size | field | our value | meaning |
|---|---|---|---|---|
| 0 | 1 | ID length | 0 | length of an optional text after the header (we write none) |
| 1 | 1 | colour map type | 0 | 0 = no colour map |
| 2 | 1 | image type | **2** or **10** | 2 = true-colour, uncompressed; 10 = true-colour, **RLE** |
| 3 | 5 | colour map details | 0 0 0 0 0 | unused when there is no colour map |
| 8 | 2 | x origin | 0 | where to place the picture on a screen (nobody uses it) |
| 10 | 2 | y origin | 0 | the same |
| 12 | 2 | width | | in pixels, little-endian, up to 65,535 |
| 14 | 2 | height | | in pixels, little-endian, up to 65,535 |
| 16 | 1 | pixel depth | **24** or **32** | bits per pixel: B, G, R or B, G, R, A |
| 17 | 1 | image descriptor | **0x20** or **0x28** | Section 39.4 |

Check: 1 + 1 + 1 + 5 + 2 + 2 + 2 + 2 + 1 + 1 = **18** ✓.

Then come the pixels, straight after the header (and after the ID text, if the ID length is not 0).

🔢 **Maths: a 4 × 2 picture**

> 18 header bytes + 4 × 2 × 3 = 24 pixel bytes = **42** bytes (no padding, ever)

The program prints its header and its top row:

```
a 4 x 2 TGA is 42 bytes
header: 00 00 02 00 00 00 00 00 00 00 00 00 04 00 02 00 18 20
top row: 00 00 FF 00 FF 00 FF 00 00 FF FF FF
```

Read it: type 02 (uncompressed), width `04 00` = 4, height `02 00` = 2, depth 0x18 = 24, descriptor 0x20. The top row is red (00 00 FF), green (00 FF 00), blue (FF 00 00) and white (FF FF FF) — B, G, R order, as in BMP.

---

## 39.3 No signature

A BMP starts with "BM"; a PNG with 0x89 "PNG". A TGA file starts with… the ID length, usually 0. There is **no signature** at the start. (Newer TGA files may have a 26-byte **footer** at the very end that ends with the text "TRUEVISION-XFILE.", but it is optional, and we do not write it.)

So a TGA reader cannot be sure a file **is** a TGA. It can only check that the header makes sense: a known image type, a sensible depth, a non-zero size, and enough bytes. That is exactly what `decodeTGA` does — and why the file name ending (`.tga`) matters more for TGA than for other formats.

---

## 39.4 The image descriptor: alpha bits and the origin

📖 **New word: image descriptor** — the last header byte. Its 8 bits hold two things we need:

```
   bit:   7   6   5   4   3   2   1   0
          0   0   │   0   └─────┬─────┘
                  │             └── number of alpha bits per pixel (0 or 8)
                  └── 1 = rows start at the TOP (top-down), 0 = bottom-up
```

(Bit 4 means "pixels go right to left" — almost never used, and bits 6–7 must be 0.)

🔢 **Maths: our two values**

> 24-bit, top-down: bit 5 = 0x20, no alpha bits → **0x20**
> 32-bit, top-down, 8 alpha bits: 0x20 + 8 = **0x28**

We always write **top-down** (bit 5 set). It is the simplest — our rows are already top-down — and every TGA reader understands it. Our reader handles both: if bit 5 is 0, the first row in the file is the **bottom** row, like BMP.

> **topDown = (descriptor & 0x20) != 0** (a mask, Chapter 4)

---

## 39.5 Real transparency

Chapter 18 introduced **alpha**: how see-through each pixel is, from 0 (invisible) to 255 (solid). Our `Image` class has no alpha — it stores R, G, B only. But a TGA file can carry it, so we pass the alpha values **separately**, as a list with one byte per pixel:

```cpp
std::vector<std::uint8_t> alpha(200 * 200);
```

Pixel (x, y)'s alpha is at index **y × width + x** — the same row-by-row order as everything else (Chapter 6).

What alpha should a smooth disk have? Chapter 27 told us: **alpha = coverage**. A pixel half covered by the disk should be half see-through. So the program fills an orange 200 × 200 picture and sets each pixel's alpha from Chapter 27's `circleCoverage`:

```cpp
double coverage = circleCoverage(100.0, 100.0, 80.0, x, y, 4);
alpha[y * 200 + x] = toByte(coverage);
```

`toByte` (Chapter 14) turns 0…1 into 0…255. The result, `disk.tga`, is a solid orange square in which **only the disk** is visible: put it on top of another picture in GIMP or a game, and the square's corners vanish, leaving a smooth round edge. (Its RGB is orange everywhere, even where alpha is 0 — invisible pixels can have any colour.)

In 32-bit pixels, each pixel is **B, G, R, A**:

```
   orange (250, 140, 30), fully solid:     1E 8C FA FF
   the same, invisible (outside the disk): 1E 8C FA 00
```

```
disk.tga: alpha at the centre 255, at a corner 0, alpha the same: yes
```

The program reads the file back with `loadTGA`, which can return the alpha list too, and checks every alpha value.

💡 In Chapter 42 our PNG files will store transparency too — and every web browser shows it.

---

## 39.6 Compression: run-length encoding

📖 **New words: compression and lossless** — **compression** stores the same information in fewer bytes. **Lossless** compression gives back **exactly** the original bytes, bit for bit. (JPEG photos use **lossy** compression: smaller, but not exactly the same. We only use lossless methods in this book.)

Look at a flag: three stripes of one colour each. In a 300 × 200 flag, a row is "blue 100 times, white 100 times, red 100 times". Storing all 300 pixels — 900 bytes — repeats the same 3 bytes over and over.

📖 **New word: run** — several equal things in a row.

📖 **New word: run-length encoding** — store each run as **how many** plus **what**: "100 × blue, 100 × white, 100 × red". That is the whole idea. People do it naturally: "four red balloons" instead of "a red balloon, a red balloon, a red balloon, a red balloon".

### Packets

📖 **New word: packet** — TGA's RLE stores the pixels as a series of **packets**. Each packet starts with one **header byte**:

```
   bit 7 = 1: a RUN packet   — one pixel follows; it is repeated (count) times
   bit 7 = 0: a RAW packet   — (count) different pixels follow, one after another
   bits 0–6:  count − 1      (so count is 1 to 128)
```

📖 **New word: raw packet** — for pixels that are **not** repeated, a run of length 1 would waste a header byte per pixel. A raw packet lists up to 128 different pixels after one header.

Why "count − 1"? A packet never holds 0 pixels, so storing count − 1 lets 7 bits (0–127) mean 1–128 — one more than 127.

🔢 **Maths: the header byte**

> a run of 4: 0x80 | (4 − 1) = 0x80 | 0x03 = **0x83**
> a raw packet of 1 pixel: 1 − 1 = **0x00**
> a run of 128 (the longest): 0x80 | 127 = **0xFF**
> reading 0x82: bit 7 is 1 → run; 0x82 & 0x7F = 2 → count **3**

### A row, by hand

Take a row of 8 pixels: **red, red, red, red, green, blue, blue, blue**. Uncompressed: 8 × 3 = 24 bytes.

> red × 4 → a run packet: `83` + red (B G R `00 00 FF`)
> green × 1 → a raw packet: `00` + green (`00 FF 00`)
> blue × 3 → a run packet: `82` + blue (`FF 00 00`)

```
8 pixels, 24 bytes, packed into 12:
  83 00 00 FF 00 00 FF 00 82 FF 00 00
```

Half the size. (A run of 2 costs 1 + 3 = 4 bytes instead of 6, so even short runs help.)

### The encoder's plan

For each row, starting at pixel i:

1. Count how many pixels from i are equal to pixel i (at most 128): that is `run`.
2. If run ≥ 2: write a **run** packet, and jump ahead by run.
3. Otherwise: collect pixels into a **raw** packet, and stop just before a pixel that **starts a run** (it equals the pixel after it) — or at 128 pixels, or the end of the row. Write the raw packet.

We start fresh packets at the beginning of every row. The TGA rules allow a packet to continue from one row into the next, but many readers do not like it, so good writers never do it — and our reader accepts both.

---

## 39.7 When does RLE help?

📖 **New word: compression ratio** — original size ÷ compressed size.

The program compresses three 300 × 200 pictures:

```
flag: uncompressed 180018 bytes, RLE 2418 bytes, read back the same
sky: uncompressed 180018 bytes, RLE 2418 bytes, read back the same
noise: uncompressed 180018 bytes, RLE 180244 bytes, read back the same
```

🔢 **Maths: the flag**

> each row: 3 runs of 100 → 3 packets of 4 bytes = **12** bytes (instead of 900)
> 200 rows × 12 + 18 = **2,418** bytes — a compression ratio of 180,018 / 2,418 ≈ **74**

🔢 **Maths: the sky**

> a vertical gradient: every **row** is one colour (the colour changes only from row to row)
> 300 = 128 + 128 + 44 → 3 run packets per row → also **12** bytes per row → 2,418 bytes

🔢 **Maths: the noise**

> every pixel is a random grey (made with a simple formula; Chapter 54 explains random numbers). Neighbours are almost never equal.
> almost everything goes into raw packets of 128 pixels: 128 × 3 = 384 bytes + 1 header byte
> each row needs at least 3 packets (128 + 128 + 44) → at least 3 extra bytes per row → about 600 extra bytes in all
> The file grew to **180,244** — 226 bytes **bigger** than uncompressed (fewer than 600, because now and then two neighbours happen to be equal, and a run of 2 saves 2 bytes).

🧠 **Remember:** RLE is great for pictures with **large flat areas** (flags, icons, cartoons, screenshots, simple drawings), and useless — even slightly harmful — for **noisy** pictures and photos, where neighbouring pixels are almost never exactly equal. No lossless method can shrink every file: some must get bigger (Practice 8). A good writer could check and choose uncompressed when RLE does not help (Practice 5).

And horizontal gradients? Every pixel in a row differs from its neighbour, so RLE does nothing there either. The PNG format (Chapters 40–45) is much cleverer: it can compress smooth gradients well too.

---

## 39.8 Reading RLE safely

A compressed file is **more** dangerous to read than an uncompressed one. Each packet's header byte says how many pixels follow — and a broken (or evil) file can say anything. Our decoder checks, for every packet:

1. **Is there a header byte?** If the file ends before all the pixels are decoded: "the file ends in the middle of the pixels".
2. **Does the packet fit in the picture?** If done + count > width × height: "a packet goes past the last pixel". Without this check, a few bytes like `FF FF FF …` could make the decoder write millions of pixels.
3. **Are the packet's pixel bytes in the file?** A run needs 1 pixel's bytes, a raw packet count × that: otherwise "the file ends in the middle of a packet".

The decoder first turns all the packets into one plain list of pixel bytes (`pixels`), exactly as an uncompressed file would have stored them. Then **one** loop puts them into the picture, row by row, the right way up — the same loop for both types.

The program tests the reader with the good tiny file and five broken versions:

```
broken files:
  the good file: accepted
  type 1: refused (only true-colour TGA files (type 2 or 10) are supported)
  16 bits per pixel: refused (only 24 and 32 bits per pixel are supported)
  width 0: refused (bad width or height)
  last 2 bytes missing: refused (the file ends in the middle of a packet)
  a run of 128 pixels: refused (a packet goes past the last pixel)
```

(The tiny 4 × 2 RLE file has two packets: a raw packet of 4 different pixels for the top row, and a run of 4 black pixels for the bottom row. Changing the first header byte to 0xFF claims a run of 128 pixels in a picture with only 8.)

---

## Code, part 1: `tga.h`

File: `common/tga.h` (new). It includes `bmpload.h` (for `Bytes`, the little-endian helpers, `writeBytes` and `readFileBytes`).

```cpp
#ifndef TGA_H
#define TGA_H

#include <cstdint>
#include <string>
#include <vector>
#include "bmpload.h"

const int kTgaHeaderSize = 18;

inline bool samePixel(const Bytes& row, int a, int b, int bytesPerPixel) {
    for (int i = 0; i < bytesPerPixel; ++i) {
        if (row[a * bytesPerPixel + i] != row[b * bytesPerPixel + i]) {
            return false;
        }
    }
    return true;
}

inline void appendPixelBytes(Bytes& out, const Bytes& row, int index, int bytesPerPixel) {
    for (int i = 0; i < bytesPerPixel; ++i) {
        out.push_back(row[index * bytesPerPixel + i]);
    }
}

inline void encodeRleRow(Bytes& out, const Bytes& row, int bytesPerPixel) {
    const int count = static_cast<int>(row.size()) / bytesPerPixel;
    int i = 0;
    while (i < count) {
        int run = 1;
        while (i + run < count && run < 128 && samePixel(row, i, i + run, bytesPerPixel)) {
            ++run;
        }
        if (run >= 2) {
            out.push_back(static_cast<std::uint8_t>(0x80 | (run - 1)));
            appendPixelBytes(out, row, i, bytesPerPixel);
            i += run;
        } else {
            int raw = 1;
            while (i + raw < count && raw < 128 &&
                   !(i + raw + 1 < count && samePixel(row, i + raw, i + raw + 1, bytesPerPixel))) {
                ++raw;
            }
            out.push_back(static_cast<std::uint8_t>(raw - 1));
            for (int k = 0; k < raw; ++k) {
                appendPixelBytes(out, row, i + k, bytesPerPixel);
            }
            i += raw;
        }
    }
}

inline Bytes makeTgaBytes(const Image& image, const std::vector<std::uint8_t>* alpha, bool rle) {
    Bytes file;
    const int width = image.width();
    const int height = image.height();
    if (width <= 0 || height <= 0 || width > 65535 || height > 65535) {
        return file;
    }
    const bool withAlpha =
        alpha != nullptr && static_cast<int>(alpha->size()) == width * height;
    const int bytesPerPixel = withAlpha ? 4 : 3;

    file.push_back(0);
    file.push_back(0);
    file.push_back(rle ? 10 : 2);
    for (int i = 0; i < 5; ++i) {
        file.push_back(0);
    }
    putU16(file, 0);
    putU16(file, 0);
    putU16(file, static_cast<std::uint16_t>(width));
    putU16(file, static_cast<std::uint16_t>(height));
    file.push_back(static_cast<std::uint8_t>(bytesPerPixel * 8));
    file.push_back(withAlpha ? 0x28 : 0x20);

    for (int y = 0; y < height; ++y) {
        Bytes row;
        for (int x = 0; x < width; ++x) {
            Colour c = image.getPixel(x, y);
            row.push_back(c.b);
            row.push_back(c.g);
            row.push_back(c.r);
            if (withAlpha) {
                row.push_back((*alpha)[y * width + x]);
            }
        }
        if (rle) {
            encodeRleRow(file, row, bytesPerPixel);
        } else {
            file.insert(file.end(), row.begin(), row.end());
        }
    }
    return file;
}

inline bool saveTGA(const Image& image, const std::string& fileName, bool rle = false,
                    const std::vector<std::uint8_t>* alpha = nullptr) {
    Bytes file = makeTgaBytes(image, alpha, rle);
    if (file.empty()) {
        return false;
    }
    return writeBytes(fileName, file);
}

inline std::string decodeTGA(const Bytes& file, Image& image,
                             std::vector<std::uint8_t>* alpha = nullptr) {
    if (file.size() > 2147483647u) {
        return "file too big";
    }
    if (!hasBytes(file, 0, kTgaHeaderSize)) {
        return "too short for the header";
    }
    const int idLength = file[0];
    const int type = file[2];
    const int width = getU16(file, 12);
    const int height = getU16(file, 14);
    const int depth = file[16];
    const bool topDown = (file[17] & 0x20) != 0;
    if (file[1] != 0) {
        return "colour-mapped TGA files are not supported";
    }
    if (type != 2 && type != 10) {
        return "only true-colour TGA files (type 2 or 10) are supported";
    }
    if (depth != 24 && depth != 32) {
        return "only 24 and 32 bits per pixel are supported";
    }
    if (width == 0 || height == 0) {
        return "bad width or height";
    }
    if (static_cast<long long>(width) * height > 100000000LL) {
        return "picture too big";
    }
    const int bytesPerPixel = depth / 8;
    const int pixelCount = width * height;
    int pos = kTgaHeaderSize + idLength;

    Bytes pixels;
    pixels.reserve(pixelCount * bytesPerPixel);
    if (type == 2) {
        if (!hasBytes(file, pos, pixelCount * bytesPerPixel)) {
            return "the pixels are not inside the file";
        }
        pixels.assign(file.begin() + pos, file.begin() + pos + pixelCount * bytesPerPixel);
    } else {
        int done = 0;
        while (done < pixelCount) {
            if (!hasBytes(file, pos, 1)) {
                return "the file ends in the middle of the pixels";
            }
            const int header = file[pos];
            ++pos;
            const int count = (header & 0x7F) + 1;
            if (done + count > pixelCount) {
                return "a packet goes past the last pixel";
            }
            const bool isRun = (header & 0x80) != 0;
            const int dataBytes = isRun ? bytesPerPixel : count * bytesPerPixel;
            if (!hasBytes(file, pos, dataBytes)) {
                return "the file ends in the middle of a packet";
            }
            for (int k = 0; k < count; ++k) {
                const int from = isRun ? pos : pos + k * bytesPerPixel;
                for (int i = 0; i < bytesPerPixel; ++i) {
                    pixels.push_back(file[from + i]);
                }
            }
            pos += dataBytes;
            done += count;
        }
    }

    Image result(width, height);
    std::vector<std::uint8_t> alphaResult(pixelCount, 255);
    for (int row = 0; row < height; ++row) {
        const int y = topDown ? row : height - 1 - row;
        for (int x = 0; x < width; ++x) {
            const int at = (row * width + x) * bytesPerPixel;
            result.setPixel(x, y, Colour{pixels[at + 2], pixels[at + 1], pixels[at]});
            if (bytesPerPixel == 4) {
                alphaResult[y * width + x] = pixels[at + 3];
            }
        }
    }
    image = result;
    if (alpha != nullptr) {
        *alpha = alphaResult;
    }
    return "";
}

inline bool loadTGA(const std::string& fileName, Image& image,
                    std::vector<std::uint8_t>* alpha = nullptr) {
    Bytes file;
    if (!readFileBytes(fileName, file)) {
        return false;
    }
    return decodeTGA(file, image, alpha).empty();
}

#endif
```

### Line by line

**The encoder (lines 1–51)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–7 | include guard and `#include` lines | Exact-size integers, strings, lists, and the file-format branch so far. |
| 9 | `const int kTgaHeaderSize = 18;` | The header size (Section 39.2). |
| 11–18 | `inline bool samePixel(const Bytes& row, int a, int b, int bytesPerPixel) { ... }` | Are pixels a and b of a row of pixel bytes equal? Compare all 3 (or 4) bytes. |
| 20–24 | `inline void appendPixelBytes(Bytes& out, const Bytes& row, int index, int bytesPerPixel) { ... }` | Copy one pixel's bytes to the end of `out`. |
| 26–27 | `inline void encodeRleRow(Bytes& out, const Bytes& row, int bytesPerPixel) { const int count = static_cast<int>(row.size()) / bytesPerPixel;` | RLE-encode one row (Section 39.6). `count` is the number of pixels in it. |
| 28–29 | `int i = 0; while (i < count) {` | i is the first pixel not yet encoded. |
| 30–33 | `int run = 1; while (i + run < count && run < 128 && samePixel(row, i, i + run, bytesPerPixel)) { ++run; }` | Step 1: how many pixels from i are the same as pixel i (at most 128, not past the row's end). |
| 34–37 | `if (run >= 2) { out.push_back(static_cast<std::uint8_t>(0x80 \| (run - 1))); appendPixelBytes(out, row, i, bytesPerPixel); i += run; }` | Step 2: a run packet — header with bit 7 set, then the pixel once. |
| 38–43 | `} else { int raw = 1; while (i + raw < count && raw < 128 && !(i + raw + 1 < count && samePixel(row, i + raw, i + raw + 1, bytesPerPixel))) { ++raw; }` | Step 3: grow a raw packet. Pixel i + raw joins it **unless** it equals the pixel after it — then a run starts there, and the raw packet must stop. |
| 44–48 | `out.push_back(static_cast<std::uint8_t>(raw - 1)); for (int k = 0; k < raw; ++k) { appendPixelBytes(out, row, i + k, bytesPerPixel); } i += raw;` | The raw header (bit 7 is 0), then all its pixels. |
| 49–51 | `}` `}` `}` | End of the if, the loop and the function. |

**Writing (lines 53–104)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 53 | `inline Bytes makeTgaBytes(const Image& image, const std::vector<std::uint8_t>* alpha, bool rle) {` | Build a whole TGA file. `alpha` is a **pointer** to the alpha list, or `nullptr` for "no alpha" (a pointer can say "nothing", a reference cannot). |
| 54–59 | `Bytes file; ... if (width <= 0 \|\| height <= 0 \|\| width > 65535 \|\| height > 65535) { return file; }` | The width and height fields are 2 bytes: at most 65,535. An empty list means failure (as in Chapter 37). |
| 60–62 | `const bool withAlpha = alpha != nullptr && static_cast<int>(alpha->size()) == width * height; const int bytesPerPixel = withAlpha ? 4 : 3;` | Use alpha only if there is a list with exactly one value per pixel. `alpha->size()` means "the size of the list `alpha` points to". |
| 64–69 | `file.push_back(0); file.push_back(0); file.push_back(rle ? 10 : 2); for (int i = 0; i < 5; ++i) { file.push_back(0); }` | ID length 0, no colour map, the image type, and five zero bytes of colour map details. |
| 70–73 | `putU16(file, 0); putU16(file, 0); putU16(file, static_cast<std::uint16_t>(width)); putU16(file, static_cast<std::uint16_t>(height));` | x origin, y origin, width, height — 2 bytes each, little-endian. |
| 74–75 | `file.push_back(static_cast<std::uint8_t>(bytesPerPixel * 8)); file.push_back(withAlpha ? 0x28 : 0x20);` | Depth 24 or 32, and the image descriptor (Section 39.4): top-down, with 8 alpha bits if needed. |
| 77–87 | `for (int y = 0; y < height; ++y) { Bytes row; for (int x = 0; ...) { Colour c = image.getPixel(x, y); row.push_back(c.b); row.push_back(c.g); row.push_back(c.r); if (withAlpha) { row.push_back((*alpha)[y * width + x]); } }` | Rows top-down. Each row's pixel bytes are first collected in `row`: B, G, R, and A if needed. `(*alpha)[i]` means "item i of the list `alpha` points to". |
| 88–93 | `if (rle) { encodeRleRow(file, row, bytesPerPixel); } else { file.insert(file.end(), row.begin(), row.end()); } }` | Compress the row, or copy it as it is. |
| 94–95 | `return file;` `}` | Done. |
| 97–104 | `inline bool saveTGA(const Image& image, const std::string& fileName, bool rle = false, const std::vector<std::uint8_t>* alpha = nullptr) { ... }` | Build and write. By default: uncompressed, no alpha. |

**Reading (lines 106–202)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 106–107 | `inline std::string decodeTGA(const Bytes& file, Image& image, std::vector<std::uint8_t>* alpha = nullptr) {` | Read a TGA from bytes. It returns `""` on success, or the reason it failed. (Unlike BMP, some problems only show up **while** decoding the packets, so the checks and the decoding are in one function.) If `alpha` points to a list, it receives the alpha values. |
| 108–113 | the size checks | Not too big for `int` positions; at least the 18 header bytes. |
| 114–119 | `const int idLength = file[0];` … `const bool topDown = (file[17] & 0x20) != 0;` | Read the fields we need. |
| 120–134 | five checks | No colour map; type 2 or 10; depth 24 or 32; non-zero size; not more than 100 million pixels. |
| 135–137 | `const int bytesPerPixel = depth / 8; const int pixelCount = width * height; int pos = kTgaHeaderSize + idLength;` | The pixels start after the header **and** the ID text. |
| 139–140 | `Bytes pixels; pixels.reserve(pixelCount * bytesPerPixel);` | All the pixel bytes, uncompressed, will be collected here. |
| 141–145 | `if (type == 2) { if (!hasBytes(file, pos, pixelCount * bytesPerPixel)) { return ...; } pixels.assign(file.begin() + pos, file.begin() + pos + pixelCount * bytesPerPixel); }` | Uncompressed: check that all the pixel bytes are there, then copy them in one go. |
| 146–148 | `} else { int done = 0; while (done < pixelCount) {` | RLE: decode packets until every pixel is done. |
| 149–154 | `if (!hasBytes(file, pos, 1)) { return ...; } const int header = file[pos]; ++pos; const int count = (header & 0x7F) + 1;` | Check 1, then read the header byte: the low 7 bits + 1 is the count. |
| 155–157 | `if (done + count > pixelCount) { return "a packet goes past the last pixel"; }` | Check 2. |
| 158–162 | `const bool isRun = (header & 0x80) != 0; const int dataBytes = isRun ? bytesPerPixel : count * bytesPerPixel; if (!hasBytes(file, pos, dataBytes)) { return ...; }` | Check 3: the packet's pixel bytes must be in the file. |
| 163–168 | `for (int k = 0; k < count; ++k) { const int from = isRun ? pos : pos + k * bytesPerPixel; for (...) { pixels.push_back(file[from + i]); } }` | Expand the packet: a run copies the **same** pixel count times; a raw packet copies count different pixels. |
| 169–172 | `pos += dataBytes; done += count; } }` | Move past the packet. |
| 174–175 | `Image result(width, height); std::vector<std::uint8_t> alphaResult(pixelCount, 255);` | The picture, and alpha values (255 = solid, for 24-bit files). |
| 176–185 | `for (int row = 0; ...) { const int y = topDown ? row : height - 1 - row; for (int x = 0; ...) { const int at = (row * width + x) * bytesPerPixel; result.setPixel(x, y, Colour{pixels[at + 2], pixels[at + 1], pixels[at]}); if (bytesPerPixel == 4) { alphaResult[y * width + x] = pixels[at + 3]; } } }` | Place the pixels, the right way up: B, G, R turned into R, G, B, and the fourth byte as alpha. No padding to skip. |
| 186–191 | `image = result; if (alpha != nullptr) { *alpha = alphaResult; } return "";` `}` | Hand back the picture, and the alpha if it was asked for. |
| 193–200 | `inline bool loadTGA(...) { Bytes file; if (!readFileBytes(fileName, file)) { return false; } return decodeTGA(file, image, alpha).empty(); }` | Read the file and decode it. |
| 202 | `#endif` | End of the include guard. |

---

## Code, part 2: headers, packets, sizes and a transparent disk

File: `ch39/tga.cpp`

```cpp
#include <iostream>
#include <string>
#include <vector>
#include "tga.h"
#include "antialias.h"

void printBytes(const char* label, const Bytes& b, int from, int count) {
    std::cout << label;
    for (int i = from; i < from + count && i < static_cast<int>(b.size()); ++i) {
        std::cout << " " << hexByte(b[i]);
    }
    std::cout << "\n";
}

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

int main() {
    Image tiny(4, 2);
    tiny.setPixel(0, 0, colours::red);
    tiny.setPixel(1, 0, colours::green);
    tiny.setPixel(2, 0, colours::blue);
    tiny.setPixel(3, 0, colours::white);
    Bytes plain = makeTgaBytes(tiny, nullptr, false);
    std::cout << "a 4 x 2 TGA is " << plain.size() << " bytes\n";
    printBytes("header:", plain, 0, kTgaHeaderSize);
    printBytes("top row:", plain, kTgaHeaderSize, 12);

    Bytes row;
    const Colour rowColours[8] = {colours::red,  colours::red,  colours::red,  colours::red,
                                  colours::green, colours::blue, colours::blue, colours::blue};
    for (Colour c : rowColours) {
        row.push_back(c.b);
        row.push_back(c.g);
        row.push_back(c.r);
    }
    Bytes packed;
    encodeRleRow(packed, row, 3);
    std::cout << "8 pixels, " << row.size() << " bytes, packed into " << packed.size() << ":\n";
    printBytes(" ", packed, 0, static_cast<int>(packed.size()));

    Image flag(300, 200);
    for (int y = 0; y < 200; ++y) {
        for (int x = 0; x < 300; ++x) {
            Colour c = colours::white;
            if (x < 100) {
                c = Colour{0, 85, 164};
            } else if (x >= 200) {
                c = Colour{239, 65, 53};
            }
            flag.setPixel(x, y, c);
        }
    }
    Image noise(300, 200);
    unsigned int seed = 12345;
    for (int y = 0; y < 200; ++y) {
        for (int x = 0; x < 300; ++x) {
            seed = seed * 1103515245u + 12345u;
            std::uint8_t v = static_cast<std::uint8_t>(seed >> 24);
            noise.setPixel(x, y, Colour{v, v, v});
        }
    }
    Image sky(300, 200);
    for (int y = 0; y < 200; ++y) {
        Colour c = lerpColour(Colour{40, 90, 200}, Colour{250, 200, 120}, y / 199.0);
        for (int x = 0; x < 300; ++x) {
            sky.setPixel(x, y, c);
        }
    }

    const Image* pictures[3] = {&flag, &sky, &noise};
    const std::string names[3] = {"flag", "sky", "noise"};
    for (int i = 0; i < 3; ++i) {
        Bytes raw = makeTgaBytes(*pictures[i], nullptr, false);
        Bytes rle = makeTgaBytes(*pictures[i], nullptr, true);
        Image back(0, 0);
        std::string problem = decodeTGA(rle, back);
        bool same = problem.empty() && samePictures(*pictures[i], back);
        std::cout << names[i] << ": uncompressed " << raw.size() << " bytes, RLE " << rle.size()
                  << " bytes, read back " << (same ? "the same" : "DIFFERENT") << "\n";
        if (!saveTGA(*pictures[i], names[i] + ".tga", true)) {
            std::cout << "could not write " << names[i] << ".tga\n";
            return 1;
        }
    }

    Image disk(200, 200, Colour{250, 140, 30});
    std::vector<std::uint8_t> alpha(200 * 200);
    for (int y = 0; y < 200; ++y) {
        for (int x = 0; x < 200; ++x) {
            double coverage = circleCoverage(100.0, 100.0, 80.0, x, y, 4);
            alpha[y * 200 + x] = toByte(coverage);
        }
    }
    if (!saveTGA(disk, "disk.tga", true, &alpha)) {
        std::cout << "could not write disk.tga\n";
        return 1;
    }
    Image diskBack(0, 0);
    std::vector<std::uint8_t> alphaBack;
    if (!loadTGA("disk.tga", diskBack, &alphaBack)) {
        std::cout << "could not load disk.tga\n";
        return 1;
    }
    std::cout << "disk.tga: alpha at the centre " << static_cast<int>(alphaBack[100 * 200 + 100])
              << ", at a corner " << static_cast<int>(alphaBack[0]) << ", alpha the same: "
              << (alphaBack == alpha ? "yes" : "no") << "\n";

    std::cout << "broken files:\n";
    Bytes good = makeTgaBytes(tiny, nullptr, true);
    Bytes tests[6] = {good, good, good, good, good, good};
    tests[1][2] = 1;
    tests[2][16] = 16;
    tests[3][12] = 0;
    tests[3][13] = 0;
    tests[4].resize(tests[4].size() - 2);
    tests[5][kTgaHeaderSize] = 0xFF;
    const char* labels[6] = {"the good file", "type 1", "16 bits per pixel", "width 0",
                             "last 2 bytes missing", "a run of 128 pixels"};
    for (int i = 0; i < 6; ++i) {
        Image ignored(0, 0);
        std::string problem = decodeTGA(tests[i], ignored);
        std::cout << "  " << labels[i] << ": "
                  << (problem.empty() ? "accepted" : "refused (" + problem + ")") << "\n";
    }
    return 0;
}
```

Build and run (from the `code/ch39` folder):

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common tga.cpp -o tga
./tga
```

### Line by line

**Helpers (lines 1–29)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–5 | the `#include` lines | Printing, strings, lists, the new header, and `antialias.h` for `circleCoverage` (Chapter 27). |
| 7–13 | `void printBytes(const char* label, const Bytes& b, int from, int count) { ... }` | Print `count` bytes starting at `from`, in hex. |
| 15–29 | `bool samePictures(const Image& a, const Image& b) { ... }` | Are two pictures exactly the same? |

**The tiny file and the packed row (lines 31–53)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 32–36 | `Image tiny(4, 2); tiny.setPixel(0, 0, colours::red); ...` | A 4 × 2 picture: red, green, blue, white on top; black below. |
| 37–40 | `Bytes plain = makeTgaBytes(tiny, nullptr, false);` and the prints | The 42-byte uncompressed file: its header and top row (Section 39.2). |
| 42–49 | `Bytes row; const Colour rowColours[8] = {...}; for (Colour c : rowColours) { row.push_back(c.b); ... }` | The row of Section 39.6 as B, G, R bytes. |
| 50–53 | `Bytes packed; encodeRleRow(packed, row, 3); ...` | Pack it and print the packets. |

**Three pictures (lines 55–98)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 55–66 | `Image flag(300, 200); ... Colour c = colours::white; if (x < 100) { c = Colour{0, 85, 164}; } else if (x >= 200) { c = Colour{239, 65, 53}; } ...` | A three-stripe flag: blue, white, red. |
| 67–75 | `Image noise(300, 200); unsigned int seed = 12345; ... seed = seed * 1103515245u + 12345u; std::uint8_t v = static_cast<std::uint8_t>(seed >> 24); ...` | Random-looking greys. Each step multiplies and adds; the number wraps around at 2³² (unsigned numbers wrap safely, Chapter 4), and its top 8 bits are the grey. This is a "linear congruential generator" — Chapter 54 explains it properly. |
| 76–82 | `Image sky(300, 200); for (int y ...) { Colour c = lerpColour(..., y / 199.0); for (int x ...) { sky.setPixel(x, y, c); } }` | A vertical gradient: blue at the top to orange at the bottom, each row one colour. |
| 84–85 | `const Image* pictures[3] = {&flag, &sky, &noise}; const std::string names[3] = {...};` | The three pictures and their names. |
| 86–93 | `Bytes raw = makeTgaBytes(*pictures[i], nullptr, false); Bytes rle = makeTgaBytes(*pictures[i], nullptr, true); Image back(0, 0); std::string problem = decodeTGA(rle, back); bool same = ...; std::cout << ...` | Both sizes, and a round trip through the **compressed** version (Section 39.7). |
| 94–98 | `if (!saveTGA(*pictures[i], names[i] + ".tga", true)) { ... }` | Save each one RLE-compressed. |

**The transparent disk (lines 100–120)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 100–101 | `Image disk(200, 200, Colour{250, 140, 30}); std::vector<std::uint8_t> alpha(200 * 200);` | An orange square, and one alpha value per pixel. |
| 102–107 | `for (...) { for (...) { double coverage = circleCoverage(100.0, 100.0, 80.0, x, y, 4); alpha[y * 200 + x] = toByte(coverage); } }` | Alpha = coverage of a disk with radius 80 (Section 39.5). |
| 108–111 | `if (!saveTGA(disk, "disk.tga", true, &alpha)) { ... }` | Save it as 32-bit, RLE. `&alpha` passes the list's address (a pointer). |
| 112–117 | `Image diskBack(0, 0); std::vector<std::uint8_t> alphaBack; if (!loadTGA("disk.tga", diskBack, &alphaBack)) { ... }` | Load it back, asking for the alpha too. |
| 118–120 | `std::cout << "disk.tga: alpha at the centre " << ... << (alphaBack == alpha ? "yes" : "no") << "\n";` | Two sample values, and `==` compares the two whole lists. |

**Broken files (lines 122–140)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 123–124 | `Bytes good = makeTgaBytes(tiny, nullptr, true); Bytes tests[6] = {good, good, good, good, good, good};` | Six copies of the good RLE file. |
| 125–130 | `tests[1][2] = 1;` … `tests[5][kTgaHeaderSize] = 0xFF;` | Break five of them: type 1 (colour-mapped), 16 bits per pixel, width 0 (both width bytes), the last 2 bytes cut off, and a first packet header claiming a run of 128 (Section 39.8). |
| 131–132 | `const char* labels[6] = {...};` | Their names. |
| 133–140 | `for (int i = 0; i < 6; ++i) { Image ignored(0, 0); std::string problem = decodeTGA(tests[i], ignored); std::cout << ...; }` `return 0;` `}` | Decode each and print the verdict. |

### What you should see

```
a 4 x 2 TGA is 42 bytes
header: 00 00 02 00 00 00 00 00 00 00 00 00 04 00 02 00 18 20
top row: 00 00 FF 00 FF 00 FF 00 00 FF FF FF
8 pixels, 24 bytes, packed into 12:
  83 00 00 FF 00 00 FF 00 82 FF 00 00
flag: uncompressed 180018 bytes, RLE 2418 bytes, read back the same
sky: uncompressed 180018 bytes, RLE 2418 bytes, read back the same
noise: uncompressed 180018 bytes, RLE 180244 bytes, read back the same
disk.tga: alpha at the centre 255, at a corner 0, alpha the same: yes
broken files:
  the good file: accepted
  type 1: refused (only true-colour TGA files (type 2 or 10) are supported)
  16 bits per pixel: refused (only 24 and 32 bits per pixel are supported)
  width 0: refused (bad width or height)
  last 2 bytes missing: refused (the file ends in the middle of a packet)
  a run of 128 pixels: refused (a packet goes past the last pixel)
```

Open `disk.tga` in GIMP (or another program that understands TGA): you see a smooth orange disk on a checkerboard — GIMP's way of showing "transparent here".

---

## Small examples

### Example 1 — Decoding packets by hand

The bytes `81 00 00 00 01 FF FF FF 00 FF 00`:

> `81`: run, count 2 → black (00 00 00) twice
> `01`: raw, count 2 → `FF FF FF` (white), then `00 FF 00` — in B, G, R order that is **green**
> → black, black, white, green

### Example 2 — The longest run

A row of 1000 white pixels: 1000 = 7 × 128 + 104 → 8 run packets × 4 bytes = **32** bytes instead of 3000.

### Example 3 — The worst case

A row of 300 all-different pixels: 3 raw packets (128 + 128 + 44) → 900 + 3 = **903** bytes. At most one extra byte per 128 pixels: about 0.8 % bigger.

### Example 4 — A 32-bit header

A 64 × 64 sprite with alpha, top-down: depth **0x20** (32), descriptor **0x28**. Uncompressed size: 18 + 64 × 64 × 4 = **16,402** bytes.

### Example 5 — A bottom-up file from another program

Descriptor 0x08 (8 alpha bits, bit 5 clear): the first row in the file is the **bottom** row. Our reader puts file row 0 at y = height − 1.

---

## Common mistakes

⚠️ **Storing count instead of count − 1.** Then every run is one pixel too long, and the decoder runs off the end of the picture.

⚠️ **Runs longer than 128.** 7 bits can only say up to 127 (meaning 128). Split long runs.

⚠️ **Forgetting the descriptor bit.** With 0x00 instead of 0x20, readers think the file is bottom-up and show it upside down.

⚠️ **Forgetting the alpha bits in the descriptor.** A 32-bit file with descriptor 0x20 (0 alpha bits) may have its alpha ignored.

⚠️ **Trusting packet counts.** Always check that a packet fits in the picture and in the file.

⚠️ **Forgetting the ID text.** Pixels start at 18 + ID length, not always at 18.

⚠️ **Expecting compression to always help.** On noisy pictures RLE makes files slightly bigger.

---

## Practice

🏋️ **1.** Encode this row by hand (24-bit): white, white, black, red, red, red, red, red. How many bytes?

🏋️ **2.** Decode `02 FF 00 00 00 FF 00 00 00 FF 80 FF FF FF`.

🏋️ **3.** Save one of your pictures as an uncompressed TGA (`saveTGA(picture, "name.tga")`) and as RLE. Compare their sizes with the BMP.

🏋️ **4.** Write a `checkerTGA` test: a 256 × 256 checkerboard with 1-pixel squares, and another with 32-pixel squares. Which one does RLE shrink, and by how much?

🏋️ **5.** Write `saveTGASmallest`, which builds both versions and writes whichever is smaller.

🏋️ **6.** Make a smooth **ring** with alpha: alpha = coverage of the big circle minus coverage of a smaller circle.

🏋️ **7.** Write a TGA → BMP converter. What happens to the alpha?

🏋️ **8.** Why can **no** lossless compression method make **every** file smaller? (Hint: count how many different files of 2 bytes there are, and how many files are shorter than 2 bytes.)

---

## Answers

**1.**
> white × 2 → `81 FF FF FF`; black × 1 → raw `00 00 00 00`; red × 5 → `84 00 00 FF`
> **12** bytes (instead of 24)

**2.**
> `02`: raw, 3 pixels: `FF 00 00` blue, `00 FF 00` green, `00 00 FF` red
> `80`: run, count 1: `FF FF FF` white
> → blue, green, red, white

**3.**
> For pictures with large flat areas (like the Chapter 34 heart, whose background and middle are each one colour), the RLE file is much smaller than the BMP — only the smooth edge pixels need raw packets; the uncompressed TGA is 36 bytes smaller than the BMP (an 18-byte header instead of 54) — plus the BMP's padding, if any.

**4.**
> 1-pixel squares: every pixel differs from its neighbour → all raw → slightly **bigger** (each 256-pixel row needs 2 raw packets: 768 + 2 bytes).
> 32-pixel squares: each row is 8 runs of 32 → 8 × 4 = 32 bytes per row instead of 768 → about **24 times smaller**.

**5.**

```cpp
bool saveTGASmallest(const Image& image, const std::string& fileName) {
    Bytes raw = makeTgaBytes(image, nullptr, false);
    Bytes rle = makeTgaBytes(image, nullptr, true);
    if (raw.empty()) {
        return false;
    }
    return writeBytes(fileName, (rle.size() < raw.size()) ? rle : raw);
}
```

**6.**

```cpp
double outer = circleCoverage(100.0, 100.0, 80.0, x, y, 4);
double inner = circleCoverage(100.0, 100.0, 50.0, x, y, 4);
alpha[y * 200 + x] = toByte(outer - inner);
```

**7.**
> `Image p(0, 0); if (loadTGA("in.tga", p)) { saveBMP(p, "out.bmp"); }` — the alpha is simply **lost**: our 24-bit BMP has no place for it, so invisible pixels show their stored colour (the orange square becomes fully visible).

**8.**
> There are 256 × 256 = 65,536 different 2-byte files, but only 1 + 256 = 257 files shorter than 2 bytes (the empty file and the 256 one-byte files). If every 2-byte file got smaller, at least two of them would have to become the **same** shorter file — and then the decoder could not know which one to give back. So some files must stay the same size or grow.

---

## Summary

🧠 **TGA**: an 18-byte header, little-endian, pixels B, G, R (A), **no padding**, no signature.

🧠 Header: type **2** (uncompressed) or **10** (RLE); depth **24** or **32**; descriptor bit 5 (0x20) = top-down, low 4 bits = alpha bits (8).

🧠 TGA stores **alpha** properly. For smooth shapes, **alpha = coverage**.

🧠 **RLE**: packets with a header byte — bit 7 = run (1 pixel, repeated) or raw (several pixels); low 7 bits = count − 1 (1 to 128).

🧠 RLE is **lossless**. It shrinks flat pictures enormously and makes noisy pictures slightly bigger.

🧠 A decoder must check that every packet fits in the picture **and** in the file.

---

## Next chapter

Now for the big one: **PNG**, the format of the web. It is lossless, stores transparency, compresses far better than RLE — and every browser and phone shows it. It takes four chapters. Chapter 40 starts with PNG's structure: the 8-byte **signature**, **chunks** (IHDR, IDAT, IEND), **big-endian** numbers, and the **CRC-32** check that detects damaged files.
