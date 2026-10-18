# Chapter 36 — The BMP Format: Headers and Padding

> **Part 6 · Chapter 36 of 82**
> **You need:** Chapters 1–12 (especially 3, 4, 6, 7 and 9) · **You will make:** `bytes.h` (writing and reading little-endian numbers, a hex helper, and the BMP row size), and a program that builds a complete 78-byte BMP file in memory, prints every byte, and reads it back

---

## What you will learn

- What a **BMP** file is, and why it is a good first "real" format.
- The three parts of a BMP file: the **file header**, the **info header**, and the **pixel array**.
- Every field of both headers: its **offset**, its **size**, and what it means.
- **Little-endian** numbers, fully explained — how to write them and read them back.
- How **negative** numbers are stored in bytes.
- Why BMP rows are stored **bottom-up**.
- Why the colours are stored as **B, G, R**.
- Why each row is **padded** to a multiple of 4 bytes, and how to compute the padding.
- How to find any pixel inside a BMP file.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **BMP** (bitmap) | A simple picture file format made by Microsoft, understood by almost every computer. |
| **header** | The part at the start of a file that describes the rest (size, width, height, …). |
| **field** | One named value inside a header, like "width". |
| **offset** | How many bytes from the start of the file something begins. Byte 0 is the very first byte. |
| **little-endian** | Storing a number's bytes **smallest first**. |
| **big-endian** | Storing a number's bytes **biggest first**. |
| **signed** / **unsigned** | A number that can be negative / one that cannot. |
| **two's complement** | The way computers store negative whole numbers in bits. |
| **bottom-up** | Storing the bottom row of the picture first. |
| **padding** | Extra zero bytes added so that something has a required size. |
| **row size** (stride) | The number of bytes one row takes in the file, padding included. |
| **hex dump** | A listing of a file's bytes in hexadecimal. |
| **pixels per metre** | How big the picture should be when printed. |

---

## 36.1 Why BMP?

Our PPM files (Chapters 8 and 9) are wonderfully simple, but many programs cannot open them. Windows' Photos app, web browsers and most phones do not show PPM.

📖 **New word: BMP** — "bitmap", the picture format of Microsoft Windows since the late 1980s. Almost every computer can open a BMP file. Like PPM P6, it is **uncompressed**: the pixel colours are simply listed, byte by byte. So it is the perfect first "real" format: a little more complicated than PPM, but no hard maths.

It has a few strange habits, which earlier chapters warned about:

- its numbers are **little-endian** (Chapter 4, Practice 8; Chapter 9, Section 9.8);
- its rows go **bottom-up** (Chapter 3);
- its colours are **B, G, R** (Chapter 5, Chapter 12 Practice 5);
- its rows are **padded** to a multiple of 4 bytes (Chapter 6).

This chapter takes a BMP apart byte by byte. Chapter 37 turns it into a `saveBMP` function, and Chapter 38 into `loadBMP`.

💡 BMP has many versions and options (palettes, 16-bit and 32-bit pixels, compression, newer bigger headers). We use the most common, most widely supported kind: **24 bits per pixel, no compression, the 40-byte info header**. Every program that opens BMP files understands it.

---

## 36.2 The three parts

📖 **New word: header** — the part at the start of a file that tells a program how to read the rest. PPM had a tiny text header ("P6 3 2 255", Chapter 9). BMP has two binary headers.

```
 offset 0    ┌──────────────────────────┐
             │ file header   (14 bytes) │  "this is a BMP, this big, pixels start at …"
 offset 14   ├──────────────────────────┤
             │ info header   (40 bytes) │  width, height, bits per pixel, …
 offset 54   ├──────────────────────────┤
             │ pixel array              │  the colours, row by row, bottom row first
             │ (row size × height bytes)│
             └──────────────────────────┘
```

📖 **New word: offset** — the position of a byte, counted from the start of the file. The first byte is at offset **0**. So the info header starts at offset 14, and the pixels (in our kind of BMP) at offset 14 + 40 = **54**.

📖 **New word: field** — one named value inside a header. Each field has a fixed offset and a fixed size (2 or 4 bytes).

---

## 36.3 The file header (14 bytes)

| offset | size | field | our value | meaning |
|---|---|---|---|---|
| 0 | 2 | signature | `B` `M` (42 4D) | "this is a BMP file" (Chapter 8 showed it as a "magic number") |
| 2 | 4 | file size | 78 | the size of the whole file, in bytes |
| 6 | 2 | reserved | 0 | not used, always 0 |
| 8 | 2 | reserved | 0 | not used, always 0 |
| 10 | 4 | pixel offset | 54 | the offset where the pixel array starts |

Check: 2 + 4 + 2 + 2 + 4 = **14** ✓.

💡 The pixel offset matters: a program reading a BMP must jump to **this** offset to find the pixels, and not just assume 54. Other kinds of BMP have a bigger info header or a colour table (a "palette") in between.

---

## 36.4 The info header (40 bytes)

| offset | size | field | our value | meaning |
|---|---|---|---|---|
| 14 | 4 | header size | 40 | the size of this info header — it also tells which version it is |
| 18 | 4 | width | 3 | the width in pixels (**signed**) |
| 22 | 4 | height | 2 | the height in pixels (**signed** — Section 36.7) |
| 26 | 2 | planes | 1 | always 1 (a leftover from very old graphics cards) |
| 28 | 2 | bits per pixel | 24 | 24 = 3 bytes per pixel (B, G, R) |
| 30 | 4 | compression | 0 | 0 = none |
| 34 | 4 | image size | 24 | the size of the pixel array in bytes (padding included) |
| 38 | 4 | x pixels per metre | 2835 | the printing size (Section 36.10) |
| 42 | 4 | y pixels per metre | 2835 | the same, up and down |
| 46 | 4 | colours used | 0 | 0 = no palette (we store real colours) |
| 50 | 4 | important colours | 0 | 0 = all colours are important (nobody uses this) |

Check: 4 + 4 + 4 + 2 + 2 + 4 + 4 + 4 + 4 + 4 + 4 = **40** ✓, and 14 + 40 = **54** ✓.

---

## 36.5 Little-endian numbers

A 4-byte field like "file size = 78" must be written as **four bytes**. In Chapter 4 (Sections 4.6–4.8 and Practice 8) we learned how to split a number into bytes:

> byte k = (value >> (8 × k)) & 0xFF

for k = 0 (the **lowest** 8 bits), 1, 2 and 3 (the highest 8 bits).

But in which **order** do the four bytes go into the file?

📖 **New word: little-endian** — the **little end first**: byte 0 (the lowest), then byte 1, byte 2, byte 3.

📖 **New word: big-endian** — the **big end first**: byte 3 first, down to byte 0.

🔢 **Maths: 0x12345678**

> byte 0 = 0x78, byte 1 = 0x56, byte 2 = 0x34, byte 3 = 0x12
> little-endian (BMP): **78 56 34 12**
> big-endian (PNG, 16-bit PPM): **12 34 56 78**

🔢 **Maths: 78 (our file size)**

> 78 = 0x0000004E → bytes 0x4E, 0x00, 0x00, 0x00
> little-endian: **4E 00 00 00**

Little-endian looks "backwards" when you read a hex dump, because we write numbers with the biggest digit first. But it is natural for a computer: most PCs store numbers in their own memory little-endian, and the byte at the lowest address is the one worth the least, just like reading digits from the **right**. (The names come from *Gulliver's Travels*, where two countries fight a war over which end of a boiled egg to crack.)

### Writing: `putU32`

```cpp
inline void putU32(Bytes& out, std::uint32_t v) {
    out.push_back(static_cast<std::uint8_t>(v & 0xFF));
    out.push_back(static_cast<std::uint8_t>((v >> 8) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((v >> 16) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((v >> 24) & 0xFF));
}
```

Lowest byte first. `Bytes` is our short name for `std::vector<std::uint8_t>` — the bytes of a file, in order. We build the whole file in a `Bytes` list, and in Chapter 37 write it to disk in one go (Chapter 7).

### Reading: `getU32`

To read it back, we **join** the bytes again (Chapter 4's summary):

> value = b0 | (b1 << 8) | (b2 << 16) | (b3 << 24)

```cpp
return static_cast<std::uint32_t>(in[pos]) | (static_cast<std::uint32_t>(in[pos + 1]) << 8) |
       (static_cast<std::uint32_t>(in[pos + 2]) << 16) |
       (static_cast<std::uint32_t>(in[pos + 3]) << 24);
```

⚠️ Why the `static_cast<std::uint32_t>` before each shift? A `std::uint8_t` is turned into a plain `int` before shifting. `int` is signed, and shifting a byte like 0x80 left by 24 lands in the **sign bit** of the `int`, giving a negative `int` — a dark corner of C++ (in older versions of C++ it was not allowed at all). Turning each byte into `std::uint32_t` first keeps every shift in unsigned numbers, where it is always simple and correct.

🔢 **Maths: read 4E 00 00 00**

> 0x4E | (0x00 << 8) | (0x00 << 16) | (0x00 << 24) = 0x4E = **78** ✓

The 2-byte versions, `putU16` and `getU16`, are the same with only two bytes.

---

## 36.6 Negative numbers in bytes

📖 **New words: signed and unsigned** — an **unsigned** number cannot be negative (`std::uint32_t`: 0 to 4,294,967,295). A **signed** number can (`std::int32_t`: −2,147,483,648 to 2,147,483,647). The BMP width and height are **signed** — and the height really can be negative (Section 36.7).

How can 32 bits hold −2?

📖 **New word: two's complement** — the way (almost) every computer stores negative whole numbers. The rule for 32 bits:

> **−n is stored as the same bits as 2³² − n**

🔢 **Maths: −2**

> 2³² − 2 = 4,294,967,294 = 0xFFFFFFFE
> little-endian: **FE FF FF FF**

Think of a car's odometer that shows 4 digits: one step **below** 0000 is 9999. Two steps below is 9998. In the same way, two steps below 0 is 0xFFFFFFFE. The nice thing: adding works without any special rules. (−2) + 5: 0xFFFFFFFE + 5 = 0x1_00000003, and the top "1" falls off the end of 32 bits, leaving **3** ✓.

So to write a signed number, we just write its bits as an unsigned number, and to read one, we read the unsigned number and look at the same bits as signed:

```cpp
inline void putS32(Bytes& out, std::int32_t v) {
    putU32(out, static_cast<std::uint32_t>(v));
}

inline std::int32_t getS32(const Bytes& in, int pos) {
    return static_cast<std::int32_t>(getU32(in, pos));
}
```

(Turning an `int32_t` into a `uint32_t` is fully defined in C++: it gives exactly 2³² − n. The way back, for numbers above 2,147,483,647, is defined by every real compiler to give the two's complement value, and since C++20 the language itself guarantees it.)

The program prints:

```
0x12345678 as 4 little-endian bytes: 78 56 34 12
54 as 4 little-endian bytes: 36 00 00 00
-2 as 4 little-endian bytes: FE FF FF FF
read back: 305419896 = 0x12345678? yes, and -2
```

(305,419,896 is 0x12345678 written in ordinary decimal.)

---

## 36.7 Bottom-up rows

📖 **New word: bottom-up** — BMP stores the **bottom** row of the picture first, then the row above it, and the **top** row last.

Why? In maths graphs (and in the first graphics systems of OS/2 and Windows, which BMP came from), y goes **up**, so row 0 is at the bottom. Our pictures (and PPM, and PNG) use y going **down** (Chapter 3). So when writing a BMP, we visit our rows **backwards**:

```cpp
for (int y = picture.height() - 1; y >= 0; --y) {
```

— exactly the "flip every row" loop of Chapter 3, Example 4.

💡 **The negative height trick:** if the height field is **negative** (for example −2), the rows are stored **top-down** instead, like ours. Most programs understand it, but not all old ones, so we write bottom-up with a positive height. A BMP **reader** (Chapter 38) must handle both.

---

## 36.8 B, G, R

Each 24-bit pixel is three bytes, but in the order **blue, green, red** — the opposite of PPM's R, G, B. Why? Because a pixel is really one little-endian number 0xRRGGBB (red in the high byte, as in web colours like #FF8000), and little-endian stores its **lowest** byte — blue — first.

```cpp
void putPixelBGR(Bytes& out, Colour c) {
    out.push_back(c.b);
    out.push_back(c.g);
    out.push_back(c.r);
}
```

⚠️ Forget this, and red and blue swap: a red apple turns blue, a blue sky turns orange. (Chapter 12, Practice 5 made this swap on purpose.)

---

## 36.9 Padding: rows are multiples of 4 bytes

📖 **New word: padding** — extra zero bytes added so that something has a required size.

In a BMP file, **every row** must take a whole multiple of 4 bytes. (Old computers could read memory fastest in 4-byte steps, so every row was made to start on a 4-byte boundary.) A row of 3 pixels has 3 × 3 = 9 bytes of colour; the next multiple of 4 is 12, so **3 padding bytes** (zeros) are added at the end of the row.

📖 **New word: row size** (also called **stride**) — the number of bytes one row really takes, padding included. Chapter 6 promised it: "In BMP, … the row size is sometimes bigger than width × 3. Then only the row size formula works."

### The formula

> **row size = (width × 3 + 3) / 4 × 4**   (with integer division)

How does it work? Adding 3 and then dividing by 4 **rounds up** to the next whole number of 4-byte blocks; multiplying by 4 turns blocks back into bytes.

🔢 **Maths: width 3**

> 3 × 3 = 9 bytes → (9 + 3) / 4 = 12 / 4 = 3 blocks → 3 × 4 = **12** bytes → padding 12 − 9 = **3**

🔢 **Maths: width 4**

> 12 bytes → (12 + 3) / 4 = 15 / 4 = 3 (integer division) → **12** bytes → padding **0** (12 is already a multiple of 4)

The program prints a table:

```
width, pixel bytes, row size, padding:
  1, 3, 4, 1
  2, 6, 8, 2
  3, 9, 12, 3
  4, 12, 12, 0
  5, 15, 16, 1
  6, 18, 20, 2
  7, 21, 24, 3
  8, 24, 24, 0
```

The padding goes 1, 2, 3, 0, and repeats. It is never more than 3 bytes, and it is 0 whenever the width is a multiple of 4.

> **padding = row size − width × 3**

> **pixel array size = row size × height**

### Finding a pixel

With bottom-up rows and padding, pixel (x, y) of the picture (our coordinates: y = 0 at the top) starts at:

> **offset = pixel offset + (height − 1 − y) × row size + x × 3**

and its bytes are B, G, R in that order.

- (height − 1 − y): which row in the **file** — our top row (y = 0) is the file's **last** row.
- × row size: skip the whole rows before it, padding included.
- + x × 3: skip the pixels before it in its row.

---

## 36.10 Pixels per metre

📖 **New word: pixels per metre** — how big the picture should be when **printed** (screens ignore it). 2835 pixels per metre is about **72 dots per inch**:

> 72 dots per inch ÷ 0.0254 metres per inch = 2834.6 ≈ **2835** dots per metre

(0 is also allowed, meaning "unknown". We write 2835, which is what many programs write.)

---

## 36.11 Building a whole file by hand

The program builds a complete BMP for this 3 × 2 picture:

```
   top row (y = 0):     red    green   blue
   bottom row (y = 1):  white  black   yellow
```

🔢 **Maths: the sizes**

> row size = 12 (Section 36.9), pixel array = 12 × 2 = **24** bytes, file size = 14 + 40 + 24 = **78** bytes

📖 **New word: hex dump** — a listing of a file's bytes in hexadecimal, 16 per line, each line starting with the offset of its first byte (in hex). Here is our whole file:

```
the whole file, 78 bytes:
  00: 42 4D 4E 00 00 00 00 00 00 00 36 00 00 00 28 00
  10: 00 00 03 00 00 00 02 00 00 00 01 00 18 00 00 00
  20: 00 00 18 00 00 00 13 0B 00 00 13 0B 00 00 00 00
  30: 00 00 00 00 00 00 FF FF FF 00 00 00 00 FF FF 00
  40: 00 00 00 00 FF 00 FF 00 FF 00 00 00 00 00
```

Let us read it, field by field:

| offset (hex) | bytes | field | value |
|---|---|---|---|
| 00 | 42 4D | signature | "BM" |
| 02 | 4E 00 00 00 | file size | 0x4E = **78** |
| 06 | 00 00 00 00 | two reserved fields | 0, 0 |
| 0A | 36 00 00 00 | pixel offset | 0x36 = **54** |
| 0E | 28 00 00 00 | header size | 0x28 = **40** |
| 12 | 03 00 00 00 | width | **3** |
| 16 | 02 00 00 00 | height | **2** |
| 1A | 01 00 | planes | 1 |
| 1C | 18 00 | bits per pixel | 0x18 = **24** |
| 1E | 00 00 00 00 | compression | 0 |
| 22 | 18 00 00 00 | image size | 0x18 = **24** |
| 26 | 13 0B 00 00 | x pixels per metre | 0x0B13 = 11 × 256 + 19 = **2835** |
| 2A | 13 0B 00 00 | y pixels per metre | **2835** |
| 2E | 00 00 00 00 | colours used | 0 |
| 32 | 00 00 00 00 | important colours | 0 |
| 36 | FF FF FF · 00 00 00 · 00 FF FF · 00 00 00 | **bottom** row: white, black, yellow (B G R!), padding | |
| 42 | 00 00 FF · 00 FF 00 · FF 00 00 · 00 00 00 | **top** row: red, green, blue, padding | |

Look at yellow: (255, 255, 0) in R, G, B is **00 FF FF** in B, G, R. And red, (255, 0, 0), is **00 00 FF**.

(Offsets in the dump are hexadecimal: 0x36 = 54 is where the pixels start, and 0x42 = 66 = 54 + 12 is the start of the second row in the file.)

### Reading it back

Finally, the program reads its own bytes back, as Chapter 38's reader will:

```
reading it back: signature BM, file size 78, pixels start at 54, width 3, height 2, bits per pixel 24
pixel (2, 0) is at byte 72: R 0, G 0, B 255
pixel (0, 1) is at byte 54: R 255, G 255, B 255
```

🔢 **Maths: where is pixel (2, 0) (the blue one, top right)?**

> 54 + (2 − 1 − 0) × 12 + 2 × 3 = 54 + 12 + 6 = **72** ✓ — the bytes FF 00 00 (B = 255): blue ✓

🔢 **Maths: pixel (0, 1) (white, bottom left)?**

> 54 + (2 − 1 − 1) × 12 + 0 = **54** — the very first pixel bytes in the file ✓

---

## Code, part 1: `bytes.h`

File: `common/bytes.h` (new). It includes only `image.h`: file formats do not need the drawing library.

```cpp
#ifndef BYTES_H
#define BYTES_H

#include <cstdint>
#include <string>
#include <vector>
#include "image.h"

using Bytes = std::vector<std::uint8_t>;

inline void putU16(Bytes& out, std::uint16_t v) {
    out.push_back(static_cast<std::uint8_t>(v & 0xFF));
    out.push_back(static_cast<std::uint8_t>((v >> 8) & 0xFF));
}

inline void putU32(Bytes& out, std::uint32_t v) {
    out.push_back(static_cast<std::uint8_t>(v & 0xFF));
    out.push_back(static_cast<std::uint8_t>((v >> 8) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((v >> 16) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((v >> 24) & 0xFF));
}

inline void putS32(Bytes& out, std::int32_t v) {
    putU32(out, static_cast<std::uint32_t>(v));
}

inline std::uint16_t getU16(const Bytes& in, int pos) {
    return static_cast<std::uint16_t>(in[pos] | (in[pos + 1] << 8));
}

inline std::uint32_t getU32(const Bytes& in, int pos) {
    return static_cast<std::uint32_t>(in[pos]) | (static_cast<std::uint32_t>(in[pos + 1]) << 8) |
           (static_cast<std::uint32_t>(in[pos + 2]) << 16) |
           (static_cast<std::uint32_t>(in[pos + 3]) << 24);
}

inline std::int32_t getS32(const Bytes& in, int pos) {
    return static_cast<std::int32_t>(getU32(in, pos));
}

inline bool hasBytes(const Bytes& in, int pos, int count) {
    return pos >= 0 && count >= 0 && pos + count <= static_cast<int>(in.size());
}

inline std::string hexByte(std::uint8_t b) {
    const char digits[] = "0123456789ABCDEF";
    std::string s;
    s += digits[b >> 4];
    s += digits[b & 0x0F];
    return s;
}

inline int bmpRowSize(int width) {
    return (width * 3 + 3) / 4 * 4;
}

#endif
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#ifndef BYTES_H` / `#define BYTES_H` | Include guard. |
| 4–7 | `#include <cstdint>` / `<string>` / `<vector>` / `"image.h"` | Exact-size integers (Chapter 4); strings for `hexByte`; lists; and `Image` and `Colour`. |
| 9 | `using Bytes = std::vector<std::uint8_t>;` | A short name for "a list of bytes" (like `Vec2` in Chapter 29). The bytes of a file, in order. |
| 11–14 | `inline void putU16(Bytes& out, std::uint16_t v) { out.push_back(... v & 0xFF ...); out.push_back(... (v >> 8) & 0xFF ...); }` | Add a 2-byte number, little-endian: low byte, then high byte. |
| 16–21 | `inline void putU32(Bytes& out, std::uint32_t v) { ... }` | Add a 4-byte number, little-endian (Section 36.5). |
| 23–25 | `inline void putS32(Bytes& out, std::int32_t v) { putU32(out, static_cast<std::uint32_t>(v)); }` | A signed number: the same bits, written as unsigned (Section 36.6). |
| 27–29 | `inline std::uint16_t getU16(const Bytes& in, int pos) { return static_cast<std::uint16_t>(in[pos] \| (in[pos + 1] << 8)); }` | Read a 2-byte number starting at `pos`. (Two bytes never reach the sign bit of an `int`, so no cast is needed before the shift here.) |
| 31–35 | `inline std::uint32_t getU32(const Bytes& in, int pos) { return static_cast<std::uint32_t>(in[pos]) \| ... << 24); }` | Read a 4-byte number: join the bytes, each made `std::uint32_t` before shifting (Section 36.5). |
| 37–39 | `inline std::int32_t getS32(const Bytes& in, int pos) { return static_cast<std::int32_t>(getU32(in, pos)); }` | Read a signed number: the same bits, seen as signed. |
| 41–43 | `inline bool hasBytes(const Bytes& in, int pos, int count) { return pos >= 0 && count >= 0 && pos + count <= static_cast<int>(in.size()); }` | Are bytes pos … pos + count − 1 really there? A reader must check this before every read, or a short (broken) file makes it read past the end of the list (Chapter 12 had the same worry). |
| 45–51 | `inline std::string hexByte(std::uint8_t b) { const char digits[] = "0123456789ABCDEF"; std::string s; s += digits[b >> 4]; s += digits[b & 0x0F]; return s; }` | A byte as two hex digits: the high 4 bits and the low 4 bits (Chapter 4, Practice 6). |
| 53–55 | `inline int bmpRowSize(int width) { return (width * 3 + 3) / 4 * 4; }` | Bytes per row in a 24-bit BMP, padding included (Section 36.9). |
| 57 | `#endif` | End of the include guard. |

---

## Code, part 2: a BMP, byte by byte

File: `ch36/bmp_layout.cpp`

```cpp
#include <iostream>
#include <string>
#include "bytes.h"

void printBytes(const char* label, const Bytes& b) {
    std::cout << label;
    for (std::uint8_t v : b) {
        std::cout << " " << hexByte(v);
    }
    std::cout << "\n";
}

void putPixelBGR(Bytes& out, Colour c) {
    out.push_back(c.b);
    out.push_back(c.g);
    out.push_back(c.r);
}

int main() {
    Bytes number;
    putU32(number, 0x12345678);
    printBytes("0x12345678 as 4 little-endian bytes:", number);
    Bytes small;
    putU32(small, 54);
    printBytes("54 as 4 little-endian bytes:", small);
    Bytes negative;
    putS32(negative, -2);
    printBytes("-2 as 4 little-endian bytes:", negative);
    std::cout << "read back: " << getU32(number, 0) << " = 0x12345678? "
              << (getU32(number, 0) == 0x12345678 ? "yes" : "no") << ", and " << getS32(negative, 0)
              << "\n";

    std::cout << "width, pixel bytes, row size, padding:\n";
    for (int w = 1; w <= 8; ++w) {
        std::cout << "  " << w << ", " << w * 3 << ", " << bmpRowSize(w) << ", "
                  << bmpRowSize(w) - w * 3 << "\n";
    }

    Image picture(3, 2);
    picture.setPixel(0, 0, colours::red);
    picture.setPixel(1, 0, colours::green);
    picture.setPixel(2, 0, colours::blue);
    picture.setPixel(0, 1, colours::white);
    picture.setPixel(1, 1, colours::black);
    picture.setPixel(2, 1, colours::yellow);

    int rowSize = bmpRowSize(picture.width());
    int pixelBytes = rowSize * picture.height();
    int fileSize = 14 + 40 + pixelBytes;
    Bytes file;
    file.push_back('B');
    file.push_back('M');
    putU32(file, fileSize);
    putU16(file, 0);
    putU16(file, 0);
    putU32(file, 14 + 40);
    putU32(file, 40);
    putS32(file, picture.width());
    putS32(file, picture.height());
    putU16(file, 1);
    putU16(file, 24);
    putU32(file, 0);
    putU32(file, pixelBytes);
    putS32(file, 2835);
    putS32(file, 2835);
    putU32(file, 0);
    putU32(file, 0);
    for (int y = picture.height() - 1; y >= 0; --y) {
        for (int x = 0; x < picture.width(); ++x) {
            putPixelBGR(file, picture.getPixel(x, y));
        }
        for (int p = picture.width() * 3; p < rowSize; ++p) {
            file.push_back(0);
        }
    }

    std::cout << "the whole file, " << file.size() << " bytes:\n";
    for (int i = 0; i < static_cast<int>(file.size()); i += 16) {
        std::cout << "  " << hexByte(static_cast<std::uint8_t>(i)) << ":";
        for (int j = i; j < i + 16 && j < static_cast<int>(file.size()); ++j) {
            std::cout << " " << hexByte(file[j]);
        }
        std::cout << "\n";
    }

    std::cout << "reading it back: signature " << file[0] << file[1] << ", file size "
              << getU32(file, 2) << ", pixels start at " << getU32(file, 10) << ", width "
              << getS32(file, 18) << ", height " << getS32(file, 22) << ", bits per pixel "
              << getU16(file, 28) << "\n";
    int offset = static_cast<int>(getU32(file, 10));
    int height = getS32(file, 22);
    const int wanted[2][2] = {{2, 0}, {0, 1}};
    for (const auto& xy : wanted) {
        int x = xy[0];
        int y = xy[1];
        int at = offset + (height - 1 - y) * rowSize + x * 3;
        if (hasBytes(file, at, 3)) {
            std::cout << "pixel (" << x << ", " << y << ") is at byte " << at << ": R "
                      << static_cast<int>(file[at + 2]) << ", G " << static_cast<int>(file[at + 1])
                      << ", B " << static_cast<int>(file[at]) << "\n";
        }
    }
    return 0;
}
```

Build and run (from the `code/ch36` folder):

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common bmp_layout.cpp -o bmp_layout
./bmp_layout
```

### Line by line

**Helpers (lines 1–17)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–3 | the `#include` lines | Printing, strings, and the new header. |
| 5–11 | `void printBytes(const char* label, const Bytes& b) { std::cout << label; for (std::uint8_t v : b) { std::cout << " " << hexByte(v); } std::cout << "\n"; }` | Print a label and a list of bytes in hex. |
| 13–17 | `void putPixelBGR(Bytes& out, Colour c) { out.push_back(c.b); out.push_back(c.g); out.push_back(c.r); }` | Add one pixel in BMP order: blue, green, red (Section 36.8). |

**Little-endian numbers (lines 19–31)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 20–22 | `Bytes number; putU32(number, 0x12345678); printBytes(...);` | Section 36.5's example: 78 56 34 12. |
| 23–25 | `Bytes small; putU32(small, 54); ...` | 54 = 0x36: 36 00 00 00. |
| 26–28 | `Bytes negative; putS32(negative, -2); ...` | Two's complement: FE FF FF FF (Section 36.6). |
| 29–31 | `std::cout << "read back: " << getU32(number, 0) << ...` | Read both back: the reader undoes the writer. |

**Padding (lines 33–37)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 33–37 | `for (int w = 1; w <= 8; ++w) { std::cout << ... << bmpRowSize(w) << ", " << bmpRowSize(w) - w * 3 << "\n"; }` | The row size table of Section 36.9. |

**Building the file (lines 39–75)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 39–45 | `Image picture(3, 2); picture.setPixel(0, 0, colours::red);` … | The 3 × 2 picture of Section 36.11. |
| 47–49 | `int rowSize = bmpRowSize(picture.width()); int pixelBytes = rowSize * picture.height(); int fileSize = 14 + 40 + pixelBytes;` | 12, 24 and 78. |
| 50 | `Bytes file;` | The whole file will be built here. |
| 51–52 | `file.push_back('B');` / `file.push_back('M');` | The signature. A `char` like `'B'` is the byte 0x42 (Chapter 4). |
| 53–56 | `putU32(file, fileSize); putU16(file, 0); putU16(file, 0); putU32(file, 14 + 40);` | The rest of the file header: size, two reserved fields, pixel offset (Section 36.3). |
| 57–67 | `putU32(file, 40);` … `putU32(file, 0);` | The 11 fields of the info header, in order (Section 36.4). Width and height are written with `putS32`, because they are signed. |
| 68 | `for (int y = picture.height() - 1; y >= 0; --y) {` | Rows **bottom-up** (Section 36.7). |
| 69–71 | `for (int x = 0; x < picture.width(); ++x) { putPixelBGR(file, picture.getPixel(x, y)); }` | Each pixel of the row, left to right, as B, G, R. |
| 72–75 | `for (int p = picture.width() * 3; p < rowSize; ++p) { file.push_back(0); }` `}` | Padding: add zeros from the end of the colours up to the row size. (For width 3: p = 9, 10, 11 — three zeros.) |

**The hex dump (lines 77–84)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 77 | `std::cout << "the whole file, " << file.size() << " bytes:\n";` | 78. |
| 78–79 | `for (int i = 0; i < static_cast<int>(file.size()); i += 16) { std::cout << "  " << hexByte(static_cast<std::uint8_t>(i)) << ":";` | One line per 16 bytes, starting with its offset in hex. (Our file is shorter than 256 bytes, so one hex byte is enough for the offset.) |
| 80–82 | `for (int j = i; j < i + 16 && j < static_cast<int>(file.size()); ++j) { std::cout << " " << hexByte(file[j]); }` | The bytes of this line; the last line stops at the end of the file. |
| 83–84 | `std::cout << "\n";` `}` | End of the line. |

**Reading it back (lines 86–104)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 86–89 | `std::cout << "reading it back: signature " << file[0] << file[1] << ...` | `file[0]` and `file[1]` are `std::uint8_t`, which `std::cout` prints as **characters** (Chapter 4's warning) — here that is exactly what we want: "BM". The other fields are read with `getU32`, `getS32` and `getU16` at their offsets. |
| 90–91 | `int offset = static_cast<int>(getU32(file, 10));` / `int height = getS32(file, 22);` | Where the pixels start, and how many rows there are — read from the file, not from `picture`, as a real reader must. |
| 92–95 | `const int wanted[2][2] = {{2, 0}, {0, 1}}; for (const auto& xy : wanted) { int x = xy[0]; int y = xy[1];` | Two pixels to look up. `const auto&` lets the loop visit each little two-number array without copying it. |
| 96 | `int at = offset + (height - 1 - y) * rowSize + x * 3;` | The pixel formula of Section 36.9. |
| 97–101 | `if (hasBytes(file, at, 3)) { std::cout << ... file[at + 2] ... file[at + 1] ... file[at] ... }` | If the three bytes are there, print them as R, G, B — reading them in the order 2, 1, 0 turns B, G, R around. |
| 102–104 | `}` `return 0;` `}` | Done. (Nothing is written to disk yet — that is Chapter 37.) |

### What you should see

```
0x12345678 as 4 little-endian bytes: 78 56 34 12
54 as 4 little-endian bytes: 36 00 00 00
-2 as 4 little-endian bytes: FE FF FF FF
read back: 305419896 = 0x12345678? yes, and -2
width, pixel bytes, row size, padding:
  1, 3, 4, 1
  2, 6, 8, 2
  3, 9, 12, 3
  4, 12, 12, 0
  5, 15, 16, 1
  6, 18, 20, 2
  7, 21, 24, 3
  8, 24, 24, 0
the whole file, 78 bytes:
  00: 42 4D 4E 00 00 00 00 00 00 00 36 00 00 00 28 00
  10: 00 00 03 00 00 00 02 00 00 00 01 00 18 00 00 00
  20: 00 00 18 00 00 00 13 0B 00 00 13 0B 00 00 00 00
  30: 00 00 00 00 00 00 FF FF FF 00 00 00 00 FF FF 00
  40: 00 00 00 00 FF 00 FF 00 FF 00 00 00 00 00
reading it back: signature BM, file size 78, pixels start at 54, width 3, height 2, bits per pixel 24
pixel (2, 0) is at byte 72: R 0, G 0, B 255
pixel (0, 1) is at byte 54: R 255, G 255, B 255
```

---

## Small examples

### Example 1 — The size of a BMP

A 640 × 480 picture: row size = (1920 + 3) / 4 × 4 = **1920** (no padding, because 640 is a multiple of 4). Pixel array = 1920 × 480 = 921,600 bytes. File = **921,654** bytes. (A P6 PPM of the same picture: 921,600 bytes plus a 15-byte header.)

### Example 2 — An awkward width

A 101 × 50 picture: 303 bytes of colour per row → (303 + 3) / 4 = 76 → row size **304**, padding **1**. Pixel array = 304 × 50 = 15,200. File = **15,254** bytes.

### Example 3 — Reading a little-endian number

The bytes **E0 01 00 00** at offset 18 mean: 0xE0 + 0x01 × 256 = 224 + 256 = **480**. A width of 480.

### Example 4 — A negative height

The bytes **38 FF FF FF** at offset 22: as unsigned, 0xFFFFFF38 = 4,294,967,096; as signed, 4,294,967,096 − 4,294,967,296 = **−200**. The picture is 200 rows tall and stored **top-down**.

### Example 5 — The last byte of the file

For our 3 × 2 BMP: the top row of the picture is the **last** row in the file, from offset 66 to 77. Its last 3 bytes (75, 76, 77) are padding. So the last byte of the file is a padding 0.

---

## Common mistakes

⚠️ **Big-endian by accident.** Writing the high byte first makes 78 into 0x4E000000 = 1,308,622,848: programs will think the file is over a gigabyte.

⚠️ **Forgetting the padding.** For widths that are a multiple of 4 it "works", so the bug hides. Then a 3-pixel-wide picture comes out slanted and colour-shifted: each row starts 3 bytes too early.

⚠️ **Rows the wrong way up.** Writing our top row first makes the picture upside down.

⚠️ **R, G, B instead of B, G, R.** Red and blue swap.

⚠️ **Wrong size fields.** The file size must include both headers. The image size must include the padding.

⚠️ **Shifting bytes as `int`.** `in[pos + 3] << 24` with a byte ≥ 0x80 lands in the sign bit of an `int`. Cast to `std::uint32_t` first.

⚠️ **Assuming the pixels start at 54.** When reading, always use the pixel offset field.

⚠️ **Printing bytes as characters.** `std::cout << file[j]` prints a character, not a number. Use `hexByte`, or `static_cast<int>` (Chapter 4).

---

## Practice

🏋️ **1.** Write 1000 and 70,000 as 4 little-endian bytes in hex.

🏋️ **2.** Which number is stored in the 4 little-endian bytes **10 27 00 00**? And in **FF FF FF FF**, read as signed?

🏋️ **3.** Work out the row size, padding and file size for a 1 × 1 BMP and a 7 × 3 BMP.

🏋️ **4.** In the 7 × 3 BMP, at which byte does pixel (6, 0) start? And pixel (0, 2)?

🏋️ **5.** Write `putU32BigEndian` and `getU32BigEndian` (we will need them for PNG in Chapter 40).

🏋️ **6.** Change the program to write the rows **top-down** with a negative height. Which bytes of the dump change?

🏋️ **7.** Write a function `bool checkBmpHeader(const Bytes& file)` that returns true only if the file is at least 54 bytes long, starts with "BM", has bits per pixel 24, and compression 0.

🏋️ **8.** Why can the padding never be more than 3 bytes?

---

## Answers

**1.**
> 1000 = 0x000003E8 → **E8 03 00 00**
> 70,000 = 0x00011170 → **70 11 01 00**

**2.**
> 0x2710 = 2 × 4096 + 7 × 256 + 1 × 16 + 0 = 8192 + 1792 + 16 = **10,000**
> FF FF FF FF = 0xFFFFFFFF = 2³² − 1 → signed: −1 (one step below 0 on the odometer)

**3.**
> 1 × 1: 3 bytes → row size **4**, padding **1**, pixel array 4, file **58** bytes
> 7 × 3: 21 bytes → (21 + 3) / 4 × 4 = **24**, padding **3**, pixel array 72, file **126** bytes

**4.**
> pixel (6, 0) — the top row is the file's last row (row 2 in the file): 54 + 2 × 24 + 6 × 3 = 54 + 48 + 18 = **120**
> pixel (0, 2) — the bottom row, the file's first: 54 + 0 + 0 = **54**

**5.**

```cpp
inline void putU32BigEndian(Bytes& out, std::uint32_t v) {
    out.push_back(static_cast<std::uint8_t>((v >> 24) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((v >> 16) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((v >> 8) & 0xFF));
    out.push_back(static_cast<std::uint8_t>(v & 0xFF));
}

inline std::uint32_t getU32BigEndian(const Bytes& in, int pos) {
    return (static_cast<std::uint32_t>(in[pos]) << 24) |
           (static_cast<std::uint32_t>(in[pos + 1]) << 16) |
           (static_cast<std::uint32_t>(in[pos + 2]) << 8) | static_cast<std::uint32_t>(in[pos + 3]);
}
```

**6.**
> Write `putS32(file, -picture.height())` and loop `for (int y = 0; y < picture.height(); ++y)`.
> The height bytes at 0x16 become **FE FF FF FF** (−2), and the two pixel rows swap places: the red-green-blue row now comes first, at offset 54.

**7.**

```cpp
bool checkBmpHeader(const Bytes& file) {
    if (!hasBytes(file, 0, 54)) {
        return false;
    }
    if (file[0] != 'B' || file[1] != 'M') {
        return false;
    }
    return getU16(file, 28) == 24 && getU32(file, 30) == 0;
}
```

**8.**
> The padding fills the row up to the **next** multiple of 4. If 4 or more bytes were missing, a smaller multiple of 4 would already be big enough. So only 0, 1, 2 or 3 bytes can ever be needed.

---

## Summary

🧠 A 24-bit BMP is: **14-byte file header** + **40-byte info header** + **pixel array**. The pixels start at the offset given at byte 10 (54 for us).

🧠 All numbers are **little-endian**: lowest byte first. Write with `(v >> 8k) & 0xFF`; read with `b0 | b1 << 8 | b2 << 16 | b3 << 24` (as `std::uint32_t`).

🧠 Negative numbers use **two's complement**: −n has the same bits as 2³² − n.

🧠 Rows are **bottom-up** (a negative height means top-down). Pixels are **B, G, R**.

🧠 Each row is padded to a multiple of 4: **row size = (3 × width + 3) / 4 × 4**.

🧠 Pixel (x, y) starts at **offset + (height − 1 − y) × rowSize + 3x**.

---

## Next chapter

We built a BMP file in memory and checked every byte. In Chapter 37 we turn that into a proper `saveBMP(image, fileName)` function for **any** `Image`, write it to disk, and open it in an ordinary picture viewer for the first time — no special program needed. We will also save all our favourite pictures from Parts 4 and 5 as BMP files, and compare their sizes with PPM.
