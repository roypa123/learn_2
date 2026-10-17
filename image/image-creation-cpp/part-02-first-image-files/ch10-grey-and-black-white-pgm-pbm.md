# Chapter 10 — Grey and Black-and-White Images (PGM, PBM)

> **Part 2 · Chapter 10 of 82**
> **You need:** Chapters 1–9 · **You will make:** `grey.pgm` (a grey gradient), `checker.pbm` (a tiny checkerboard) and `disk.pbm` (a black circle)

---

## What you will learn

- Why grey images need only **one byte per pixel**, and where we use them later.
- The **PGM** format: P2 (text) and P5 (binary).
- The **PBM** format: P1 (text) and P4 (binary), with **1 bit per pixel**.
- Why in PBM, **1 means black** (the opposite of what you may expect).
- How to **pack 8 pixels into 1 byte**, using shifts and OR from Chapter 4.
- Why each PBM row is **padded** to a whole number of bytes.
- How to draw a filled circle using distance and pixel centres (Chapter 3).

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **greyscale** | An image that has only greys: one brightness value per pixel, no colour. |
| **PGM** | "Portable GrayMap". The Netpbm format for grey images. |
| **PBM** | "Portable BitMap". The Netpbm format for black-and-white images. |
| **bit depth** | How many bits are used for one pixel (or one channel). |
| **bit packing** | Putting several small values (like single bits) into one byte. |
| **most significant bit (MSB)** | The bit of a byte that is worth the most: bit 7, worth 128. |
| **padding** | Extra unused bits or bytes added so that something fills a whole unit. |
| **mask image** | A black-and-white image that says "yes" or "no" for each pixel. |

---

## 10.1 Why grey images?

📖 **New word: greyscale** — an image with only greys. Each pixel has **one** brightness value, not three.

In Chapter 5 we learned that a grey has R = G = B. So storing three equal bytes is a waste. A grey image stores **one** byte per pixel:

| | Colour (PPM) | Grey (PGM) |
|---|---|---|
| bytes per pixel | 3 | **1** |
| 256 × 256 image | 196,608 bytes | **65,536 bytes** |

📖 **New word: bit depth** — how many bits are used for one pixel. Colour PPM: 24 bits per pixel. Grey PGM: 8 bits per pixel. Black-and-white PBM: **1** bit per pixel.

Grey images are not only for black-and-white photos. Later in this book we use them for many things:

| Use | Chapter |
|---|---|
| A photo turned into grey | 15 |
| A **histogram** of brightness | 48 |
| The result of **edge detection** | 51 |
| **Noise** patterns (clouds, marble) | 55–57 |
| A **depth buffer** (how far each pixel is) | 67 |

---

## 10.2 PGM: the grey format

📖 **New word: PGM** — "Portable GrayMap". It works exactly like PPM, but with **one value per pixel**.

### P2: the text version

```
P2
4 2
255
0 85 170 255
255 170 85 0
```

| Part | Meaning |
|---|---|
| `P2` | magic number: grey, text |
| `4 2` | width 4, height 2 |
| `255` | maxval |
| `0 85 170 255` | row 0: black, dark grey, light grey, white |
| `255 170 85 0` | row 1: the same, the other way round |

🔢 **Maths: how many numbers?**

> width × height = 4 × 2 = **8** numbers (not × 3 — one value per pixel)

### P5: the binary version

The same rules as P6 (Chapter 9), but **one byte per pixel**:

1. `P5`
2. whitespace, width, whitespace, height, whitespace, maxval
3. **exactly one** whitespace
4. `width × height` raw bytes, row-major, top row first

The hex dump of the 4 × 2 image above, as P5:

```
0000:  50 35 0A 34 20 32 0A 32 35 35 0A 00 55 AA FF FF
0010:  AA 55 00
```

> header `P5\n4 2\n255\n` = 3 + 4 + 4 = 11 bytes
> pixels = 4 × 2 = 8 bytes
> total = **19 bytes**

Check: 85 = 5 × 16 + 5 = `0x55`, 170 = 10 × 16 + 10 = `0xAA` ✓.

### A grey buffer

For a grey image, our buffer is a `std::vector<std::uint8_t>` with `width × height` bytes. The index formula is Chapter 6's formula **without** `× 3`:

> **index = y × width + x**

🧠 **Remember:** PGM = PPM with **one** value per pixel. Grey buffer index = **y × width + x**.

---

## 10.3 PBM: black and white, 1 bit per pixel

📖 **New word: PBM** — "Portable BitMap". Each pixel is **only** black or white.

So each pixel needs only **one bit** (Chapter 4): 0 or 1.

⚠️ **Careful: in PBM, 1 means BLACK and 0 means WHITE.**

This is the **opposite** of PGM, where 0 is black. Why? PBM was made for **printers** and **fax machines**. On paper, a 1 meant "put ink here", and ink is black. So think of it as "1 = ink".

| Format | 0 means | 1 means |
|---|---|---|
| PGM (maxval 1) | black | white |
| **PBM** | **white** | **black** |

### P1: the text version

```
P1
5 5
0 0 1 0 0
0 0 1 0 0
1 1 1 1 1
0 0 1 0 0
0 0 1 0 0
```

This is a black **plus sign** on a white background (the same shape as Chapter 2, Practice 6).

PBM has **no maxval** in the header — a pixel can only be 0 or 1, so there is nothing to say. The header is just the magic number, the width and the height.

💡 **Tip:** In P1, the spaces between the 0s and 1s are **optional**. `00100` is also allowed, because each pixel is always exactly one digit. (In P2 and P3, spaces are needed, because a number can have several digits.)

---

## 10.4 P4: packing 8 pixels into one byte

📖 **New word: bit packing** — putting several small values into one byte.

In P4 (binary PBM), each pixel is **one bit**. A byte has 8 bits. So **one byte holds 8 pixels**.

📖 **New word: most significant bit (MSB)** — the bit worth the most in a byte: bit 7, worth 128 (Chapter 4).

The rule: the **leftmost pixel** goes into the **most significant bit**.

```
pixel x:     0   1   2   3   4   5   6   7
bit number:  7   6   5   4   3   2   1   0
worth:      128  64  32  16   8   4   2   1
```

🔢 **Maths: pack the row `1 0 1 1 0 0 0 1`**

> x=0 → bit 7: 1 × 128 = 128
> x=1 → bit 6: 0
> x=2 → bit 5: 1 × 32 = 32
> x=3 → bit 4: 1 × 16 = 16
> x=4 → bit 3: 0
> x=5 → bit 2: 0
> x=6 → bit 1: 0
> x=7 → bit 0: 1 × 1 = 1
> byte = 128 + 32 + 16 + 1 = 177 = **`0xB1`**

Look: the pixels **are** the binary number, read left to right: `10110001` = 177. That is why the leftmost pixel goes into the biggest bit — the bits are in the same order as we draw them.

### Which byte, which bit?

🔢 **Maths: pixel x in a row**

> byte inside the row = x ÷ 8 (whole-number division)
> bit number = 7 − (x % 8)

Examples:

| x | x ÷ 8 | x % 8 | bit = 7 − (x % 8) |
|---|---|---|---|
| 0 | 0 | 0 | 7 |
| 5 | 0 | 5 | 2 |
| 7 | 0 | 7 | 0 |
| 8 | 1 | 0 | 7 (first bit of the **second** byte) |
| 13 | 1 | 5 | 2 |

### Setting a bit

To turn bit number `b` on in a byte, we use **OR** with a mask that has only that bit (Chapter 4):

> mask = 1 << b
> byte = byte | mask

🔢 **Maths: turn on bit 5 in the byte `10000000`**

> mask = 1 << 5 = `00100000` = 32
> `10000000` | `00100000` = `10100000` = 160

OR never turns a bit **off**. A bit that was already 1 stays 1. So we can set the bits one at a time, in any order.

---

## 10.5 Row padding

📖 **New word: padding** — extra unused bits or bytes, added so that something fills a whole unit.

What if the width is **not** a multiple of 8? Say width = 10.

> 10 pixels = 10 bits. That is 1 full byte (8 bits) + 2 more bits.

P4 has a rule: **every row starts at a new byte**. So the last byte of each row is only partly used. The unused bits are **padding**, and we set them to 0.

```
width = 10:

        byte 0                byte 1
row 0: [x0 x1 x2 x3 x4 x5 x6 x7] [x8 x9 0  0  0  0  0  0 ]
row 1: [x0 x1 x2 x3 x4 x5 x6 x7] [x8 x9 0  0  0  0  0  0 ]
                                        └──── padding ────┘
```

🔢 **Maths: bytes per row**

We need to divide by 8 and round **up** (any leftover bits still need a whole byte).

A trick to round **up** with whole-number division: **add 7 first**.

> rowBytes = (width + 7) ÷ 8

| width | width + 7 | ÷ 8 | rowBytes |
|---|---|---|---|
| 8 | 15 | 1 | 1 |
| 10 | 17 | 2 | 2 |
| 16 | 23 | 2 | 2 |
| 17 | 24 | 3 | 3 |
| 64 | 71 | 8 | 8 |

Why does +7 work? If width is a multiple of 8, adding 7 is not enough to reach the next multiple, so the answer does not change. If there is **any** leftover (1 to 7 pixels), adding 7 pushes it past the next multiple of 8, so the answer goes up by 1. Exactly what we want.

🔢 **Maths: the full position of pixel (x, y)**

> byte index = y × rowBytes + x ÷ 8
> bit number = 7 − (x % 8)

Look at the first line: it is Chapter 6's "row size" formula, with a row size of `rowBytes` and "x ÷ 8" instead of "x × 3". This is why we learned row size in Chapter 6. (BMP in Chapter 36 has padding too, but in whole bytes.)

🧠 **Remember:** P4: 8 pixels per byte, leftmost pixel in bit 7, **1 = black**, each row padded to `(width + 7) / 8` bytes.

---

## 10.6 A mask image

📖 **New word: mask image** — a black-and-white image that says "yes" or "no" for every pixel.

In our code, before we pack the bits, we first build a simple buffer with **one byte per pixel**, where each byte is 0 or 1:

> 1 = "yes, this pixel is part of the shape" (black in PBM)
> 0 = "no" (white in PBM)

This is easy to fill with `if` tests, using the index `y × width + x`. Then `packBits` turns it into P4 bytes.

Masks are very useful. In Chapter 25 we fill shapes, and a mask says which pixels are inside. In Chapter 27 we use many small masks to make smooth edges.

### A filled circle

In Chapter 3 we drew a small "circle" using distance. Now we do it properly, using the **pixel centre** (Chapter 3, Section 3.9).

A pixel (x, y) is **inside** a circle with centre (cx, cy) and radius r when its centre is close enough:

> dx = (x + 0.5) − cx
> dy = (y + 0.5) − cy
> inside if dx² + dy² ≤ r²

🔢 **Maths: a 64 × 64 image, circle centre (32, 32), radius 24**

> r² = 24 × 24 = 576

Pixel (32, 10):
> dx = 32.5 − 32 = 0.5
> dy = 10.5 − 32 = −21.5
> dx² + dy² = 0.25 + 462.25 = 462.5
> 462.5 ≤ 576 → **inside** (black)

Pixel (10, 10):
> dx = 10.5 − 32 = −21.5
> dy = −21.5
> dx² + dy² = 462.25 + 462.25 = 924.5
> 924.5 > 576 → **outside** (white)

Why use the centre (32.0, 32.0) and the pixel centres (x + 0.5)? The image goes from 0 to 64 across, so its exact middle is 32.0. Pixels 31 and 32 have centres 31.5 and 32.5, which are both 0.5 from the middle. So the circle is **perfectly balanced** — the left half mirrors the right half.

---

## Code

File: `ch10/pgm_pbm.cpp`

```cpp
#include <iostream>
#include <fstream>
#include <cstdint>
#include <string>
#include <vector>

std::string toHex(std::uint8_t value) {
    const std::string digits = "0123456789ABCDEF";
    std::string result;
    result += digits[value >> 4];
    result += digits[value & 0x0F];
    return result;
}

long long fileSize(const std::string& fileName) {
    std::ifstream file(fileName, std::ios::binary | std::ios::ate);
    if (!file) {
        return -1;
    }
    return static_cast<long long>(file.tellg());
}

bool writePGM_P5(const std::string& fileName, int width, int height,
                 const std::vector<std::uint8_t>& grey) {
    std::ofstream file(fileName, std::ios::binary);
    if (!file) {
        return false;
    }
    file << "P5\n" << width << " " << height << "\n255\n";
    file.write(reinterpret_cast<const char*>(grey.data()),
               static_cast<std::streamsize>(grey.size()));
    return static_cast<bool>(file);
}

std::vector<std::uint8_t> packBits(int width, int height,
                                   const std::vector<std::uint8_t>& mask) {
    const int rowBytes = (width + 7) / 8;
    std::vector<std::uint8_t> packed(rowBytes * height, 0);
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            if (mask[y * width + x] != 0) {
                int byteIndex = y * rowBytes + x / 8;
                int bitNumber = 7 - (x % 8);
                packed[byteIndex] = static_cast<std::uint8_t>(
                    packed[byteIndex] | (1 << bitNumber));
            }
        }
    }
    return packed;
}

bool writePBM_P4(const std::string& fileName, int width, int height,
                 const std::vector<std::uint8_t>& mask) {
    std::ofstream file(fileName, std::ios::binary);
    if (!file) {
        return false;
    }
    std::vector<std::uint8_t> packed = packBits(width, height, mask);
    file << "P4\n" << width << " " << height << "\n";
    file.write(reinterpret_cast<const char*>(packed.data()),
               static_cast<std::streamsize>(packed.size()));
    return static_cast<bool>(file);
}

int main() {
    const int gw = 256;
    const int gh = 64;
    std::vector<std::uint8_t> grey(gw * gh, 0);
    for (int y = 0; y < gh; ++y) {
        for (int x = 0; x < gw; ++x) {
            grey[y * gw + x] = static_cast<std::uint8_t>(x);
        }
    }

    const int cw = 10;
    const int ch = 4;
    std::vector<std::uint8_t> checker(cw * ch, 0);
    for (int y = 0; y < ch; ++y) {
        for (int x = 0; x < cw; ++x) {
            if ((x + y) % 2 == 0) {
                checker[y * cw + x] = 1;
            }
        }
    }

    const int dw = 64;
    const int dh = 64;
    const double cx = 32.0;
    const double cy = 32.0;
    const double radius = 24.0;
    std::vector<std::uint8_t> disk(dw * dh, 0);
    for (int y = 0; y < dh; ++y) {
        for (int x = 0; x < dw; ++x) {
            double dx = (x + 0.5) - cx;
            double dy = (y + 0.5) - cy;
            if (dx * dx + dy * dy <= radius * radius) {
                disk[y * dw + x] = 1;
            }
        }
    }

    std::vector<std::uint8_t> packed = packBits(cw, ch, checker);
    const int rowBytes = (cw + 7) / 8;
    std::cout << "checker packed bytes:\n";
    for (int y = 0; y < ch; ++y) {
        std::cout << "  row " << y << ":";
        for (int b = 0; b < rowBytes; ++b) {
            std::cout << " " << toHex(packed[y * rowBytes + b]);
        }
        std::cout << "\n";
    }

    bool ok = writePGM_P5("grey.pgm", gw, gh, grey);
    ok = ok && writePBM_P4("checker.pbm", cw, ch, checker);
    ok = ok && writePBM_P4("disk.pbm", dw, dh, disk);
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }
    std::cout << "grey.pgm:    " << fileSize("grey.pgm") << " bytes\n";
    std::cout << "checker.pbm: " << fileSize("checker.pbm") << " bytes\n";
    std::cout << "disk.pbm:    " << fileSize("disk.pbm") << " bytes\n";
    return 0;
}
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–5 | `#include ...` | Printing, files, bytes, text, vectors. |
| 7–13 | `std::string toHex(...)` | Same as Chapter 4. We use it to print the packed bytes. |
| 15–21 | `long long fileSize(...)` | Same as Chapter 9: open at the end, `tellg` gives the size. |
| 23 | `bool writePGM_P5(const std::string& fileName, int width, int height,` | Save a **grey** buffer as P5. |
| 24 | `const std::vector<std::uint8_t>& grey) {` | The buffer has `width × height` bytes, one per pixel. |
| 25 | `std::ofstream file(fileName, std::ios::binary);` | Binary mode — required for raw bytes (Chapter 9). |
| 26–28 | `if (!file) { return false; }` | Stop if the file did not open. |
| 29 | `file << "P5\n" << width << " " << height << "\n255\n";` | The header: `P5`, width, height, maxval 255, and **exactly one** `\n`. The same pattern as P6. |
| 30 | `file.write(reinterpret_cast<const char*>(grey.data()),` | Write the whole grey buffer at once… |
| 31 | `static_cast<std::streamsize>(grey.size()));` | …all `width × height` bytes. |
| 32 | `return static_cast<bool>(file);` | `true` if it all worked. |
| 33 | `}` | End of `writePGM_P5`. |
| 35 | `std::vector<std::uint8_t> packBits(int width, int height,` | A function that turns a **mask** (one byte per pixel, 0 or 1) into **P4 bytes** (8 pixels per byte). |
| 36 | `const std::vector<std::uint8_t>& mask) {` | The mask buffer has `width × height` bytes. |
| 37 | `const int rowBytes = (width + 7) / 8;` | Bytes per row, rounded **up** (Section 10.5). |
| 38 | `std::vector<std::uint8_t> packed(rowBytes * height, 0);` | The packed buffer, all zeros. Zero bits are white, **and** the padding bits stay 0, as the rule wants. |
| 39 | `for (int y = 0; y < height; ++y) {` | Every row… |
| 40 | `for (int x = 0; x < width; ++x) {` | …every pixel in the row. |
| 41 | `if (mask[y * width + x] != 0) {` | Is this pixel part of the shape? (The mask index has no `× 3`: one byte per pixel.) |
| 42 | `int byteIndex = y * rowBytes + x / 8;` | Which byte holds this pixel's bit (Section 10.5). |
| 43 | `int bitNumber = 7 - (x % 8);` | Which bit inside that byte. The leftmost pixel gets bit 7 (Section 10.4). |
| 44 | `packed[byteIndex] = static_cast<std::uint8_t>(` | Store the new byte value… |
| 45 | `packed[byteIndex] \| (1 << bitNumber));` | …which is the old value OR a mask with only `bitNumber` set. This turns that one bit on and leaves the others alone. The cast is needed because `\|` gives an `int`. |
| 46–48 | `}` `}` `}` | End of the `if` and the two loops. |
| 49 | `return packed;` | Give back the packed bytes. |
| 50 | `}` | End of `packBits`. |
| 52 | `bool writePBM_P4(const std::string& fileName, int width, int height,` | Save a mask as a binary PBM. |
| 53 | `const std::vector<std::uint8_t>& mask) {` | The mask: 1 = black, 0 = white. |
| 54–57 | `std::ofstream file(...); if (!file) { return false; }` | Open in binary mode; stop if it fails. |
| 58 | `std::vector<std::uint8_t> packed = packBits(width, height, mask);` | Pack the mask into P4 bytes. |
| 59 | `file << "P4\n" << width << " " << height << "\n";` | The header: `P4`, width, height, and **one** `\n`. **No maxval** in PBM (Section 10.3). |
| 60 | `file.write(reinterpret_cast<const char*>(packed.data()),` | Write all the packed bytes… |
| 61 | `static_cast<std::streamsize>(packed.size()));` | …`rowBytes × height` of them. |
| 62 | `return static_cast<bool>(file);` | `true` if it all worked. |
| 63 | `}` | End of `writePBM_P4`. |
| 65 | `int main() {` | The program starts here. |
| 66–67 | `const int gw = 256; const int gh = 64;` | The grey gradient is 256 wide and 64 tall. (`g` for grey.) |
| 68 | `std::vector<std::uint8_t> grey(gw * gh, 0);` | One byte per pixel: 256 × 64 = 16,384 bytes. |
| 69–70 | `for (int y ...) { for (int x ...) {` | Every pixel. |
| 71 | `grey[y * gw + x] = static_cast<std::uint8_t>(x);` | The grey value is x: black on the left, white on the right. Index without `× 3`. |
| 72–73 | `}` `}` | End of the loops. |
| 75–76 | `const int cw = 10; const int ch = 4;` | The checkerboard is 10 × 4. The width 10 is **not** a multiple of 8, so we will see padding. |
| 77 | `std::vector<std::uint8_t> checker(cw * ch, 0);` | The mask, all 0 (white). |
| 78–79 | `for (int y ...) { for (int x ...) {` | Every pixel. |
| 80 | `if ((x + y) % 2 == 0) {` | A checkerboard: when x + y is even, the pixel is black. Moving one step in any direction changes x + y by 1, so neighbours always have different colours. |
| 81 | `checker[y * cw + x] = 1;` | Mark it black. |
| 82–84 | `}` `}` `}` | End of the `if` and loops. |
| 86–87 | `const int dw = 64; const int dh = 64;` | The disk image is 64 × 64. |
| 88–89 | `const double cx = 32.0; const double cy = 32.0;` | The centre of the circle: the exact middle of the image. |
| 90 | `const double radius = 24.0;` | The radius in pixels. |
| 91 | `std::vector<std::uint8_t> disk(dw * dh, 0);` | The mask, all white. |
| 92–93 | `for (int y ...) { for (int x ...) {` | Every pixel. |
| 94 | `double dx = (x + 0.5) - cx;` | Across distance from the circle centre to this **pixel's centre** (Section 10.6). |
| 95 | `double dy = (y + 0.5) - cy;` | Down distance, the same way. |
| 96 | `if (dx * dx + dy * dy <= radius * radius) {` | Inside the circle? We compare **squared** distances, so we do not need a square root (Chapter 3). |
| 97 | `disk[y * dw + x] = 1;` | Mark it black. |
| 98–100 | `}` `}` `}` | End of the `if` and loops. |
| 102 | `std::vector<std::uint8_t> packed = packBits(cw, ch, checker);` | Pack the checkerboard so we can **look** at the bytes. |
| 103 | `const int rowBytes = (cw + 7) / 8;` | (10 + 7) / 8 = 2 bytes per row. |
| 104 | `std::cout << "checker packed bytes:\n";` | A heading. |
| 105 | `for (int y = 0; y < ch; ++y) {` | For each row… |
| 106 | `std::cout << "  row " << y << ":";` | …print a label… |
| 107–109 | `for (int b = 0; b < rowBytes; ++b) { ... toHex(packed[y * rowBytes + b]); }` | …and each byte of that row in hex. |
| 110 | `std::cout << "\n";` | New line after each row. |
| 111 | `}` | End of the rows. |
| 113–115 | `bool ok = writePGM_P5(...); ok = ok && writePBM_P4(...); ...` | Save all three files. `ok` stays `true` only if all of them work (as in Chapter 9). |
| 116–119 | `if (!ok) { ...; return 1; }` | Stop if any failed. |
| 120–122 | `std::cout << "grey.pgm:    " << fileSize(...) ...` | Print the three file sizes. |
| 123 | `return 0;` | The program finished with no problem. |
| 124 | `}` | End of `main`. |

### What you should see

```
checker packed bytes:
  row 0: AA 80
  row 1: 55 40
  row 2: AA 80
  row 3: 55 40
grey.pgm:    16398 bytes
checker.pbm: 16 bytes
disk.pbm:    521 bytes
```

🔢 **Maths: check row 0 of the checkerboard**

> Row 0 (y = 0): black where x + 0 is even → x = 0, 2, 4, 6, 8.
> Pixels: `1 0 1 0 1 0 1 0 | 1 0` then 6 padding zeros.
> Byte 0: `10101010` = 128 + 32 + 8 + 2 = 170 = **`AA`** ✓
> Byte 1: `10000000` = 128 = **`80`** ✓ (x = 8 is black, x = 9 is white, then padding)

> Row 1 (y = 1): black where x + 1 is even → x = 1, 3, 5, 7, 9.
> Byte 0: `01010101` = 64 + 16 + 4 + 1 = 85 = **`55`** ✓
> Byte 1: `01000000` = 64 = **`40`** ✓ (x = 9 is bit 6)

🔢 **Maths: check the file sizes**

> grey.pgm: header `P5\n256 64\n255\n` = 3 + 7 + 4 = 14, pixels 256 × 64 = 16,384 → **16,398** ✓
> checker.pbm: header `P4\n10 4\n` = 3 + 5 = 8, data 2 × 4 = 8 → **16** ✓
> disk.pbm: header `P4\n64 64\n` = 3 + 6 = 9, data 8 × 64 = 512 → **521** ✓

Open the files in your viewer:
- `grey.pgm`: a band going smoothly from black (left) to white (right).
- `checker.pbm`: a tiny checkerboard (zoom in!), black in the top-left corner.
- `disk.pbm`: a black circle on white.

Compare `disk.pbm` with a P6 colour version of the same picture: 64 × 64 × 3 = 12,288 bytes. The PBM is **24 times smaller** (12,288 ÷ 512 = 24), because each pixel uses 1 bit instead of 24 bits.

---

## Small examples

### Example 1 — The same plus sign, as P1 and P4

The 5 × 5 plus from Section 10.3, as P4:

> rowBytes = (5 + 7) / 8 = 1
> row `0 0 1 0 0` → `00100` + 3 padding → `00100000` = **`20`**
> row `1 1 1 1 1` → `11111000` = 128 + 64 + 32 + 16 + 8 = 248 = **`F8`**

So the 5 data bytes are `20 20 F8 20 20`. The whole file: header `P4\n5 5\n` (7 bytes) + 5 = **12 bytes**.

### Example 2 — Invert a mask

To swap black and white, change every 0 into 1 and every 1 into 0:

```cpp
for (std::uint8_t& v : disk) {
    v = static_cast<std::uint8_t>(1 - v);
}
```

> 1 − 0 = 1, 1 − 1 = 0.

Now `disk.pbm` shows a **white** circle on a **black** background.

### Example 3 — Read one bit back

Is pixel (9, 1) of the checkerboard black?

> byteIndex = 1 × 2 + 9 / 8 = 2 + 1 = 3 → `packed[3]` = `0x40` = `01000000`
> bitNumber = 7 − (9 % 8) = 7 − 1 = 6
> (0x40 >> 6) & 1 = `00000001` & 1 = 1 → **black** ✓

This is the same `(value >> bit) & 1` test as `toBinary` in Chapter 4.

### Example 4 — Bytes per row for some widths

| width | rowBytes | padding bits per row |
|---|---|---|
| 1 | 1 | 7 |
| 8 | 1 | 0 |
| 9 | 2 | 7 |
| 20 | 3 | 4 |
| 100 | 13 | 4 |

> padding bits = rowBytes × 8 − width. For 20: 3 × 8 − 20 = 24 − 20 = 4.

---

## Common mistakes

⚠️ **Thinking 1 means white in PBM.** In PBM, **1 = black**. Your picture comes out inverted.

⚠️ **Putting the first pixel in bit 0.** The leftmost pixel goes into **bit 7** (the MSB). If you use bit 0, every group of 8 pixels is mirrored.

⚠️ **Forgetting row padding.** If you pack the bits of all rows one after another without starting each row at a new byte, every row after the first is shifted. The picture turns into slanted stripes.

⚠️ **`width / 8` instead of `(width + 7) / 8`.** For width 10, `10 / 8 = 1` byte, but we need 2. The last pixels of every row are lost and the rows shift.

⚠️ **Writing a maxval in a PBM header.** PBM has no maxval. If you write `P4\n10 4\n255\n`, the viewer reads `255\n` as the first 4 bytes of pixel data.

⚠️ **Using `× 3` in a grey or mask index.** Grey and mask buffers have **one** byte per pixel: `y × width + x`.

---

## Practice

🏋️ **1.** Write a P2 file by hand for a 3 × 1 grey image: black, middle grey (128), white.

🏋️ **2.** How big is a 640 × 480 P5 file?

🏋️ **3.** Pack the 8 pixels `0 1 1 0 1 0 0 1` into one byte. Write it in binary, decimal and hex.

🏋️ **4.** A P4 image is 20 pixels wide and 3 pixels tall. How many bytes of pixel data does it have? In which byte and which bit is pixel (17, 2)?

🏋️ **5.** Change the checkerboard so each square is **2 × 2 pixels** instead of 1 × 1. (Hint: use `(x / 2 + y / 2) % 2`.)

🏋️ **6.** Make a 64 × 64 PBM with a black **ring**: pixels whose distance from the centre is between 16 and 24.

🏋️ **7.** Make a 256 × 256 PGM where the grey value is `(x + y) / 2`. What value is at (255, 255)? At (100, 50)?

---

## Answers

**1.**

```
P2
3 1
255
0 128 255
```

**2.**
> header `P5\n640 480\n255\n` = 3 + 8 + 4 = 15
> pixels = 640 × 480 = 307,200
> total = **307,215 bytes** (one third of the P6 pixels, Chapter 9 Practice 1)

**3.**
> bits = `01101001`
> = 64 + 32 + 8 + 1 = **105**
> halves `0110` = 6, `1001` = 9 → **`0x69`**

**4.**
> rowBytes = (20 + 7) / 8 = 27 / 8 = 3
> data = 3 × 3 = **9 bytes**
> byteIndex = 2 × 3 + 17 / 8 = 6 + 2 = **8** (the last byte)
> bitNumber = 7 − (17 % 8) = 7 − 1 = **6**

**5.** Change the test on line 80 to:

```cpp
if ((x / 2 + y / 2) % 2 == 0) {
```

> `x / 2` is the same for x = 0 and 1, the same for 2 and 3, and so on. So pixels come in pairs. The same happens with y. Each "square" is now 2 × 2 pixels.

**6.**

```cpp
double d2 = dx * dx + dy * dy;
if (d2 >= 16.0 * 16.0 && d2 <= 24.0 * 24.0) {
    disk[y * dw + x] = 1;
}
```

> inner² = 256, outer² = 576. A pixel is black when 256 ≤ d² ≤ 576.

**7.**

```cpp
grey[y * gw + x] = static_cast<std::uint8_t>((x + y) / 2);
```

(with `gw = gh = 256`)

> (255, 255): (255 + 255) / 2 = 510 / 2 = **255** (white)
> (100, 50): (100 + 50) / 2 = 150 / 2 = **75** (dark grey)

The biggest possible value is 255, so it always fits in a byte. The picture is a **diagonal** gradient: black at the top-left, white at the bottom-right.

---

## Summary

🧠 **PGM** stores grey images: **one byte per pixel**. P2 = text, P5 = binary.

🧠 Grey buffer index = **y × width + x** (no × 3).

🧠 **PBM** stores black-and-white images: **one bit per pixel**. P1 = text, P4 = binary. **No maxval.**

🧠 In PBM, **1 = black**, 0 = white.

🧠 P4 packs **8 pixels per byte**, leftmost pixel in **bit 7**. Set a bit with `byte |= 1 << bit`.

🧠 Each P4 row is padded: **rowBytes = (width + 7) / 8**. Pixel (x, y) is in byte `y × rowBytes + x / 8`, bit `7 − x % 8`.

🧠 A **mask** (0 or 1 per pixel) is an easy way to build black-and-white shapes.

---

## Next chapter

We now have many small functions: `setPixel`, `writePPM_P6`, `writePGM_P5`… and we pass `pixels, width, height` to all of them. In Chapter 11 we put it all together in one tidy **`Image` class** in a header file, `image.h`, that we will use for the rest of the book.
