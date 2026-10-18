# Chapter 41 — PNG, Part 2: zlib, Stored Blocks and Adler-32

> **Part 6 · Chapter 41 of 82**
> **You need:** Chapters 1–40 (especially 4, 36 and 40) · **You will make:** `zlib.h` (Adler-32, `zlibStore` and a careful `zlibUnstore`), and a program that packs text and pixel rows into zlib data byte by byte, and catches damaged copies

---

## What you will learn

- What **zlib** and **Deflate** are, and how they fit inside a PNG file.
- The 2-byte **zlib header**, and its strange "divisible by 31" check.
- Deflate's simplest block: the **stored** block, which holds bytes without compressing them.
- How Deflate stores its first **bits** — lowest bit first.
- **LEN** and **NLEN**, and the **one's complement**.
- Why big data must be split into blocks of at most 65,535 bytes.
- The **Adler-32** checksum: two running sums and a prime number.
- How PNG lays out its pixel rows (one extra byte per row) before handing them to zlib.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **zlib** | A small wrapper around compressed data: a header, the data, and a checksum. |
| **Deflate** | The compression method inside zlib (and ZIP files, and PNG). |
| **block** | One piece of Deflate data, with its own little header. |
| **stored block** | A Deflate block that holds bytes as they are, not compressed. |
| **bit field** | A few bits inside a byte, used as one small number. |
| **one's complement** | A number with every bit flipped (`~` in C++). |
| **modulus** | The number you divide by when taking a remainder (`%`). |
| **prime number** | A whole number bigger than 1 that only 1 and itself divide exactly. |
| **scanline** | One row of pixels, as stored in a PNG (with a filter byte in front). |
| **filter byte** | The first byte of each PNG row, saying how the row was "filtered" (0 = not at all). |

---

## 41.1 Boxes inside boxes

A PNG file does not store its pixels directly. They are packed like this:

```
   PNG file
   └── IDAT chunk(s)                 (Chapter 40: length, type, data, CRC)
       └── zlib data                 (this chapter: header, Deflate data, Adler-32)
           └── Deflate blocks        (this chapter: stored blocks; Chapter 45: compressed blocks)
               └── the pixel rows    (Section 41.8: a filter byte + the pixels of each row)
```

📖 **New words: zlib and Deflate** — **Deflate** is a compression method from 1993, used in ZIP files, in web pages sent over the internet, and in PNG. **zlib** is a thin wrapper around Deflate data: a 2-byte header in front and a 4-byte checksum at the end.

Real Deflate compression is clever — and long. It takes Chapters 44 and 45. But Deflate also allows **stored** blocks, which hold bytes without compressing them at all. A PNG made with stored blocks is a perfectly valid PNG: it is just not small. So this chapter builds zlib with stored blocks, and Chapter 42 uses it to make real PNG files at once.

---

## 41.2 The zlib header

zlib data starts with two bytes, called **CMF** and **FLG**. We always write **78 01**.

📖 **New word: bit field** — a few bits inside a byte, used as one small number. Each zlib header byte holds two bit fields:

```
   CMF = 0x78 = 0111 1000
              └─┬┘ └─┬┘
                │    └── bits 0–3: compression method, 8 = Deflate
                └─────── bits 4–7: window size, 7 = 2^(7 + 8) = 32,768 bytes

   FLG = 0x01 = 0000 0001
                ││└──┬──┘
                ││   └── bits 0–4: check bits (Section 41.3)
                │└────── bit 5:    preset dictionary (0 = no)
                └─────── bits 6–7: compression level hint (0 = "fastest")
```

To read a bit field: shift it down and mask it (Chapter 4). For example, the method is `cmf & 0x0F` and the window is `cmf >> 4`.

(The **window** is how far back the compressor may look for repeated data, Chapter 45. Stored blocks never look back, so the value does not matter to us, but 7 is the normal choice.)

---

## 41.3 The "% 31" check

The 5 check bits in FLG are chosen so that the two header bytes, read as one big-endian 16-bit number, are **divisible by 31**:

> **(CMF × 256 + FLG) % 31 == 0**

🔢 **Maths: 78 01**

> 0x7801 = 7 × 4096 + 8 × 256 + 0 × 16 + 1 = 28,672 + 2,048 + 1 = **30,721** = 31 × 991 ✓

The program checks three common headers:

```
header 7801 = 30721 = 31 x 991 remainder 0
header 789C = 30876 = 31 x 996 remainder 0
header 78DA = 30938 = 31 x 998 remainder 0
```

(78 9C is what most programs write — "default compression". 78 DA means "best compression". Only the hint in bits 6–7 differs, and the check bits change to keep the % 31 rule.)

Why? It is a tiny sanity check: two random bytes pass it only about 1 time in 31. A reader that finds a header failing it knows at once that this is not zlib data.

🔢 **Maths: finding the check bits yourself**

> CMF = 0x78, and we want level 0, no dictionary: FLG = 0b000_0_ccccc
> 0x7800 = 30,720 = 31 × 990 + 30, so we must add 31 − 30 = **1** → FLG = 0x01 ✓

---

## 41.4 Stored blocks

📖 **New words: block and stored block** — Deflate data is a list of **blocks**. Each block begins with a 3-bit header:

- **BFINAL** (1 bit): 1 if this is the **last** block;
- **BTYPE** (2 bits): 0 = **stored**, 1 = compressed with fixed codes, 2 = compressed with custom codes (3 is not allowed).

### Bits, lowest first

Deflate is a stream of **bits**, not bytes, and it fills each byte starting from its **lowest** bit (bit 0). So the 3 header bits go into bits 0, 1 and 2 of the first byte:

```
   bit:  7 6 5 4 3   2 1   0
         0 0 0 0 0   0 0   1
         └───┬───┘   └┬┘   └── BFINAL = 1 (last block)
             │        └─────── BTYPE  = 00 (stored)
             └──────────────── unused: a stored block skips to the next whole byte
```

So the first byte of a stored block is simply **0x01** (the last block) or **0x00** (more blocks follow). The other 5 bits are wasted: after the header, a stored block jumps to the start of the next byte.

(This "lowest bit first" order will matter a lot in Chapter 45, where codes have many different lengths. For stored blocks, it just means "the final flag is the **1** bit".)

### LEN and NLEN

Then come four bytes:

- **LEN** (2 bytes, **little-endian**!): how many bytes the block holds, 0 to 65,535;
- **NLEN** (2 bytes, little-endian): LEN with **every bit flipped**;

and then the LEN bytes themselves, exactly as they are.

⚠️ Yes, **little-endian** — while the zlib header and the Adler-32 at the end are big-endian. Deflate was designed separately, by someone who read bits lowest-first. It is a famous trap.

📖 **New word: one's complement** — a number with every bit flipped: 0 becomes 1, 1 becomes 0. In C++ that is the `~` operator. For 16 bits: `~length & 0xFFFF`.

🔢 **Maths: LEN = 5**

> LEN = 0x0005 → bytes **05 00**
> NLEN = ~0x0005 = 0xFFFA → bytes **FA FF**
> Check: LEN + NLEN = 0x0005 + 0xFFFA = 0xFFFF: always all ones.

NLEN is a check: if the length bytes were damaged, NLEN will almost surely not match, and the reader stops instead of copying the wrong number of bytes.

### Big data: many blocks

LEN has only 16 bits, so a stored block holds at most **65,535** bytes. Bigger data is split into several blocks, and only the **last** one has BFINAL = 1.

🔢 **Maths: 150,000 bytes**

> 150,000 = 65,535 + 65,535 + 18,930 → **3 blocks**
> size = 2 (header) + 3 × 5 (block headers) + 150,000 + 4 (Adler-32) = **150,021** bytes

```
150000 bytes stored in 150021 bytes, read back the same
the second block starts with: 00 FF FF 00 00
```

The second block's header: 00 (not the last, stored), LEN `FF FF` = 65,535, NLEN `00 00`.

---

## 41.5 Adler-32

At the very end of the zlib data comes a 4-byte checksum of the **original** (uncompressed) bytes, **big-endian**. It is not CRC-32 (that protects the PNG chunks) but a simpler one called **Adler-32**, after its inventor, Mark Adler.

📖 **New words: modulus and prime number** — Adler-32 keeps two running sums, and after every step takes the remainder when dividing by **65,521**: the **modulus**. 65,521 is the biggest **prime number** smaller than 2¹⁶ = 65,536. (A prime is only divisible by 1 and itself: 2, 3, 5, 7, 11, 13, …) A prime modulus mixes the bits better than, say, 65,536 would.

The recipe:

> **a** starts at **1**; for each byte: a = (a + byte) % 65521
> **b** starts at **0**; for each byte, after updating a: b = (b + a) % 65521
> **Adler-32 = b × 65536 + a** (b in the top 16 bits, a in the bottom 16)

- **a** is 1 + the sum of all the bytes.
- **b** is the sum of all the a's along the way. Each byte is added into b once for every step after it, so **early bytes count more** — and that is what makes the order of the bytes matter (the weakness of a simple sum, Chapter 40).

🔢 **Maths: "Wiki" by hand**

```
Adler-32 step by step for "Wiki":
  'W' (87): a = 88, b = 88
  'i' (105): a = 193, b = 281
  'k' (107): a = 300, b = 581
  'i' (105): a = 405, b = 986
```

> Adler-32 = 986 × 65536 + 405 = 0x03DA × 0x10000 + 0x0195 = **0x03DA0195**

The usual check value is the text "Wikipedia", whose Adler-32 is **11E60398**:

```
Adler-32 of "Wiki" = 03DA0195, of "Wikipedia" = 11E60398
```

💡 Why a different checksum from CRC-32? Adler-32 is **faster** (just two additions per byte, no table), which mattered for the slow computers of the 1990s. It is a little weaker than CRC-32, especially for short data — but PNG protects every chunk with CRC-32 as well.

---

## 41.6 zlib of "hello", byte by byte

```
zlib of "hello": 78 01 01 05 00 FA FF 68 65 6C 6C 6F 06 2C 02 15
```

| bytes | meaning |
|---|---|
| 78 01 | zlib header: Deflate, 32 KB window, check bits |
| 01 | block header: BFINAL = 1, BTYPE = 00 (stored) |
| 05 00 | LEN = 5 (little-endian) |
| FA FF | NLEN = ~5 |
| 68 65 6C 6C 6F | "hello", as it is |
| 06 2C 02 15 | Adler-32 of "hello" (big-endian) |

2 + 5 + 5 + 4 = **16** bytes to "compress" 5 bytes: stored blocks always make data a little **bigger**:

> **zlib size = data + 2 + 5 × (number of blocks) + 4**

Even empty data needs one (empty, final) block:

```
zlib of nothing: 78 01 01 00 00 FF FF 00 00 00 01
```

(The Adler-32 of nothing is a = 1, b = 0 → **00000001**.)

💡 You can check that our bytes are real zlib: any program with a zlib library — Python's `zlib.decompress`, for example — turns them back into "hello". That is how this chapter's output was tested.

---

## 41.7 Reading zlib carefully

`zlibUnstore` does the reverse, with every check (Chapter 38's lesson — never trust data):

1. at least 2 header bytes; method 8; **% 31** passes; no preset dictionary;
2. for each block: a header byte is there; BTYPE must be **0** (compressed blocks need Chapter 45); 4 more bytes for LEN and NLEN; **NLEN = ~LEN**; all LEN bytes are inside the data; copy them;
3. stop after the block with BFINAL = 1;
4. 4 more bytes for the Adler-32, and they must equal the Adler-32 of everything copied.

The program breaks the "hello" data in five ways:

```
broken zlib data:
  the good data: accepted, 5 bytes
  header check broken: refused (the header check (% 31) fails)
  block type 1: refused (compressed blocks are not supported yet)
  NLEN wrong: refused (LEN and NLEN do not match)
  cut short: refused (a block is longer than the data)
  one letter changed: refused (the Adler-32 is wrong)
```

The last one is the interesting one: "hello" became "jello", a perfectly legal stored block — only the **Adler-32** notices.

---

## 41.8 PNG rows: scanlines and filter bytes

📖 **New words: scanline and filter byte** — before PNG hands its pixels to zlib, it lays them out row by row, and puts **one extra byte** in front of every row: the **filter byte**. It says how that row was "filtered" — changed to compress better (Chapter 43). Filter **0** means "not filtered at all": the row's bytes are just the pixels.

For 8-bit RGB, each pixel is **R, G, B** — the normal order, not BMP's B, G, R — and there is **no padding**:

> **scanline = 1 filter byte + 3 × width bytes** (4 × width with alpha)
> **all the rows = height × (1 + 3 × width)**

🔢 **Maths: a 3 × 2 picture**

> top row: red, green, blue; bottom row: white, black, yellow
> 2 × (1 + 9) = **20** bytes

```
PNG rows of a 3 x 2 picture: 00 FF 00 00 00 FF 00 00 00 FF 00 FF FF FF 00 00 00 FF FF 00
and stored with zlib: 78 01 01 14 00 EB FF 00 FF 00 00 00 FF 00 00 00 FF 00 FF FF FF 00 00 00 FF FF 00 49 CA 07 F9
```

Read the rows: `00` (filter 0), `FF 00 00` red, `00 FF 00` green, `00 00 FF` blue; `00` (filter 0), `FF FF FF` white, `00 00 00` black, `FF FF 00` yellow. In the zlib version: LEN `14 00` = 20, NLEN `EB FF`.

Those 31 zlib bytes are exactly what goes into the IDAT chunk. Add Chapter 40's signature, IHDR and IEND around them, and we have a PNG. That is Chapter 42.

---

## Code, part 1: `zlib.h`

File: `common/zlib.h` (new). It includes `png.h`.

```cpp
#ifndef ZLIB_H
#define ZLIB_H

#include <algorithm>
#include <cstdint>
#include <string>
#include "png.h"

const std::uint32_t kAdlerModulus = 65521;
const int kMaxStoredBlock = 65535;

inline std::uint32_t adler32(const Bytes& data, int from, int count) {
    std::uint32_t a = 1;
    std::uint32_t b = 0;
    for (int i = from; i < from + count; ++i) {
        a = (a + data[i]) % kAdlerModulus;
        b = (b + a) % kAdlerModulus;
    }
    return (b << 16) | a;
}

inline Bytes zlibStore(const Bytes& data) {
    Bytes out;
    out.push_back(0x78);
    out.push_back(0x01);
    const int total = static_cast<int>(data.size());
    int pos = 0;
    do {
        const int length = std::min(kMaxStoredBlock, total - pos);
        const bool last = (pos + length == total);
        out.push_back(last ? 0x01 : 0x00);
        putU16(out, static_cast<std::uint16_t>(length));
        putU16(out, static_cast<std::uint16_t>(~length & 0xFFFF));
        out.insert(out.end(), data.begin() + pos, data.begin() + pos + length);
        pos += length;
    } while (pos < total);
    putU32BE(out, adler32(data, 0, total));
    return out;
}

inline std::string zlibUnstore(const Bytes& z, Bytes& out) {
    out.clear();
    if (z.size() > 2147483647u || !hasBytes(z, 0, 2)) {
        return "too short for the zlib header";
    }
    const int cmf = z[0];
    const int flg = z[1];
    if ((cmf & 0x0F) != 8) {
        return "not deflate data";
    }
    if ((cmf * 256 + flg) % 31 != 0) {
        return "the header check (% 31) fails";
    }
    if ((flg & 0x20) != 0) {
        return "a preset dictionary is not supported";
    }
    int pos = 2;
    bool last = false;
    while (!last) {
        if (!hasBytes(z, pos, 1)) {
            return "the data ends before the last block";
        }
        const int header = z[pos];
        last = (header & 0x01) != 0;
        const int type = (header >> 1) & 0x03;
        if (type != 0) {
            return "compressed blocks are not supported yet";
        }
        if (!hasBytes(z, pos + 1, 4)) {
            return "a block header is cut off";
        }
        const int length = getU16(z, pos + 1);
        const int check = getU16(z, pos + 3);
        if (check != (~length & 0xFFFF)) {
            return "LEN and NLEN do not match";
        }
        pos += 5;
        if (!hasBytes(z, pos, length)) {
            return "a block is longer than the data";
        }
        out.insert(out.end(), z.begin() + pos, z.begin() + pos + length);
        pos += length;
    }
    if (!hasBytes(z, pos, 4)) {
        return "the Adler-32 is missing";
    }
    if (getU32BE(z, pos) != adler32(out, 0, static_cast<int>(out.size()))) {
        return "the Adler-32 is wrong";
    }
    return "";
}

#endif
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–7 | include guard and `#include` lines | `std::min`; exact-size integers; strings for messages; and the file-format branch with `putU16`, `getU16` (little-endian), `putU32BE` and `getU32BE` (big-endian). |
| 9 | `const std::uint32_t kAdlerModulus = 65521;` | The prime of Section 41.5. |
| 10 | `const int kMaxStoredBlock = 65535;` | The biggest LEN (16 bits). |
| 12–14 | `inline std::uint32_t adler32(const Bytes& data, int from, int count) { std::uint32_t a = 1; std::uint32_t b = 0;` | Adler-32 of `count` bytes from `from`. |
| 15–18 | `for (...) { a = (a + data[i]) % kAdlerModulus; b = (b + a) % kAdlerModulus; }` | The two running sums. Both stay below 65,521, so they never overflow 32 bits. |
| 19–20 | `return (b << 16) \| a;` `}` | b in the top half, a in the bottom half. |
| 22–25 | `inline Bytes zlibStore(const Bytes& data) { Bytes out; out.push_back(0x78); out.push_back(0x01);` | Wrap data in zlib with stored blocks. First the header (Section 41.2). |
| 26–28 | `const int total = static_cast<int>(data.size()); int pos = 0; do {` | A **do … while** loop runs its body at least once — so even empty data gets one (empty) block. |
| 29–30 | `const int length = std::min(kMaxStoredBlock, total - pos); const bool last = (pos + length == total);` | This block takes up to 65,535 bytes; it is the last one if it reaches the end. |
| 31 | `out.push_back(last ? 0x01 : 0x00);` | BFINAL and BTYPE = 00 (Section 41.4). |
| 32–33 | `putU16(out, static_cast<std::uint16_t>(length)); putU16(out, static_cast<std::uint16_t>(~length & 0xFFFF));` | LEN and NLEN, little-endian. |
| 34–36 | `out.insert(out.end(), data.begin() + pos, data.begin() + pos + length); pos += length; } while (pos < total);` | The block's bytes, as they are; then the next block, while bytes are left. |
| 37–39 | `putU32BE(out, adler32(data, 0, total));` `return out;` `}` | The Adler-32 of the original data, big-endian. |
| 41–42 | `inline std::string zlibUnstore(const Bytes& z, Bytes& out) { out.clear();` | Unwrap zlib data with stored blocks into `out`. Returns `""` on success, or the problem (Section 41.7). |
| 43–56 | the header checks | Size; method 8 (`cmf & 0x0F`); the **% 31** check; no preset dictionary (bit 5 of FLG, `flg & 0x20`). |
| 57–59 | `int pos = 2; bool last = false; while (!last) {` | Read blocks until the final one. |
| 60–65 | `if (!hasBytes(z, pos, 1)) { ... } const int header = z[pos]; last = (header & 0x01) != 0; const int type = (header >> 1) & 0x03;` | The block header: BFINAL is bit 0, BTYPE is bits 1–2 (shift down by 1, keep 2 bits). |
| 66–68 | `if (type != 0) { return "compressed blocks are not supported yet"; }` | Types 1 and 2 need Chapter 45. |
| 69–76 | `if (!hasBytes(z, pos + 1, 4)) { ... } const int length = getU16(z, pos + 1); const int check = getU16(z, pos + 3); if (check != (~length & 0xFFFF)) { ... }` | LEN and NLEN must both be there, and NLEN must be LEN flipped. |
| 77–82 | `pos += 5; if (!hasBytes(z, pos, length)) { ... } out.insert(...); pos += length;` | Skip the 5-byte block header; the block's bytes must be inside the data; copy them. |
| 83 | `}` | Next block. |
| 84–89 | `if (!hasBytes(z, pos, 4)) { ... } if (getU32BE(z, pos) != adler32(out, 0, static_cast<int>(out.size()))) { ... }` | The Adler-32 must be there and must match what we copied. |
| 90–91 | `return "";` `}` | Everything checked. |
| 93 | `#endif` | End of the include guard. |

---

## Code, part 2: zlib by hand

File: `ch41/zlib_store.cpp`

```cpp
#include <iostream>
#include <string>
#include "zlib.h"

Bytes bytesOf(const std::string& text) {
    return Bytes(text.begin(), text.end());
}

std::string hex32(std::uint32_t v) {
    Bytes four;
    putU32BE(four, v);
    std::string s;
    for (std::uint8_t b : four) {
        s += hexByte(b);
    }
    return s;
}

void printBytes(const char* label, const Bytes& b) {
    std::cout << label;
    for (std::uint8_t v : b) {
        std::cout << " " << hexByte(v);
    }
    std::cout << "\n";
}

void report(const char* label, const Bytes& z) {
    Bytes out;
    std::string problem = zlibUnstore(z, out);
    std::cout << "  " << label << ": "
              << (problem.empty() ? "accepted, " + std::to_string(out.size()) + " bytes"
                                  : "refused (" + problem + ")")
              << "\n";
}

int main() {
    Bytes wiki = bytesOf("Wiki");
    std::uint32_t a = 1;
    std::uint32_t b = 0;
    std::cout << "Adler-32 step by step for \"Wiki\":\n";
    for (std::uint8_t ch : wiki) {
        a = (a + ch) % kAdlerModulus;
        b = (b + a) % kAdlerModulus;
        std::cout << "  '" << static_cast<char>(ch) << "' (" << static_cast<int>(ch) << "): a = " << a
                  << ", b = " << b << "\n";
    }
    std::cout << "Adler-32 of \"Wiki\" = " << hex32(adler32(wiki, 0, 4)) << ", of \"Wikipedia\" = "
              << hex32(adler32(bytesOf("Wikipedia"), 0, 9)) << "\n";

    const int headers[3] = {0x7801, 0x789C, 0x78DA};
    for (int h : headers) {
        std::cout << "header " << hexByte(static_cast<std::uint8_t>(h >> 8))
                  << hexByte(static_cast<std::uint8_t>(h & 0xFF)) << " = " << h << " = 31 x "
                  << h / 31 << " remainder " << h % 31 << "\n";
    }

    Bytes hello = bytesOf("hello");
    Bytes packed = zlibStore(hello);
    printBytes("zlib of \"hello\":", packed);

    Bytes big(150000);
    for (int i = 0; i < 150000; ++i) {
        big[i] = static_cast<std::uint8_t>(i % 251);
    }
    Bytes bigPacked = zlibStore(big);
    Bytes back;
    std::string problem = zlibUnstore(bigPacked, back);
    std::cout << "150000 bytes stored in " << bigPacked.size() << " bytes, read back "
              << (problem.empty() && back == big ? "the same" : "DIFFERENT") << "\n";
    std::cout << "the second block starts with:";
    for (int i = 2 + 5 + kMaxStoredBlock; i < 2 + 5 + kMaxStoredBlock + 5; ++i) {
        std::cout << " " << hexByte(bigPacked[i]);
    }
    std::cout << "\n";
    Bytes empty;
    printBytes("zlib of nothing:", zlibStore(empty));

    std::cout << "broken zlib data:\n";
    report("the good data", packed);
    Bytes wrong = packed;
    wrong[1] = 0x02;
    report("header check broken", wrong);
    wrong = packed;
    wrong[2] = 0x03;
    report("block type 1", wrong);
    wrong = packed;
    wrong[5] = 0x00;
    report("NLEN wrong", wrong);
    wrong = packed;
    wrong.resize(10);
    report("cut short", wrong);
    wrong = packed;
    wrong[7] = 'j';
    report("one letter changed", wrong);

    Image tiny(3, 2);
    tiny.setPixel(0, 0, colours::red);
    tiny.setPixel(1, 0, colours::green);
    tiny.setPixel(2, 0, colours::blue);
    tiny.setPixel(0, 1, colours::white);
    tiny.setPixel(2, 1, colours::yellow);
    Bytes rows;
    for (int y = 0; y < tiny.height(); ++y) {
        rows.push_back(0);
        for (int x = 0; x < tiny.width(); ++x) {
            Colour c = tiny.getPixel(x, y);
            rows.push_back(c.r);
            rows.push_back(c.g);
            rows.push_back(c.b);
        }
    }
    printBytes("PNG rows of a 3 x 2 picture:", rows);
    printBytes("and stored with zlib:", zlibStore(rows));
    return 0;
}
```

Build and run (from the `code/ch41` folder):

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common zlib_store.cpp -o zlib_store
./zlib_store
```

### Line by line

**Helpers (lines 1–34)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–3 | the `#include` lines | Printing, strings, and the new header. |
| 5–7 | `Bytes bytesOf(const std::string& text) { ... }` | The bytes of a text (Chapter 40). |
| 9–17 | `std::string hex32(std::uint32_t v) { ... }` | A 32-bit number as 8 hex digits (Chapter 40). |
| 19–25 | `void printBytes(const char* label, const Bytes& b) { ... }` | Print a label and bytes in hex. |
| 27–34 | `void report(const char* label, const Bytes& z) { Bytes out; std::string problem = zlibUnstore(z, out); std::cout << ... (problem.empty() ? "accepted, " + std::to_string(out.size()) + " bytes" : "refused (" + problem + ")") ... }` | Try to unwrap some zlib data and print the result. `std::to_string` turns a number into text, so it can be joined with `+`. |

**Adler-32 and the header (lines 36–55)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 37–46 | `Bytes wiki = bytesOf("Wiki"); std::uint32_t a = 1; std::uint32_t b = 0; ... for (std::uint8_t ch : wiki) { a = ...; b = ...; std::cout << ...; }` | Adler-32's two sums, printed after every letter (Section 41.5). `static_cast<char>(ch)` prints the letter itself. |
| 47–48 | `std::cout << "Adler-32 of \"Wiki\" = " << hex32(adler32(wiki, 0, 4)) << ...` | The finished checksums of "Wiki" and "Wikipedia". |
| 50–55 | `const int headers[3] = {0x7801, 0x789C, 0x78DA}; for (int h : headers) { ... h / 31 << " remainder " << h % 31 ... }` | Three zlib headers, and the % 31 check (Section 41.3). |

**Storing (lines 57–76)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 57–59 | `Bytes hello = bytesOf("hello"); Bytes packed = zlibStore(hello); printBytes(...);` | "hello" in zlib (Section 41.6). |
| 61–64 | `Bytes big(150000); for (...) { big[i] = static_cast<std::uint8_t>(i % 251); }` | 150,000 bytes of test data (the pattern 0, 1, …, 250, 0, 1, …). |
| 65–69 | `Bytes bigPacked = zlibStore(big); Bytes back; std::string problem = zlibUnstore(bigPacked, back); std::cout << ... (problem.empty() && back == big ? "the same" : "DIFFERENT") ...` | Three blocks, and a round trip (Section 41.4). |
| 70–74 | `for (int i = 2 + 5 + kMaxStoredBlock; i < 2 + 5 + kMaxStoredBlock + 5; ++i) { ... }` | The second block's header starts after the zlib header (2), the first block's header (5) and its 65,535 bytes. |
| 75–76 | `Bytes empty; printBytes("zlib of nothing:", zlibStore(empty));` | The smallest zlib data. |

**Damage (lines 78–94)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 79 | `report("the good data", packed);` | The good "hello". |
| 80–82 | `Bytes wrong = packed; wrong[1] = 0x02; report(...);` | 0x7802 = 30,722 is not divisible by 31. |
| 83–85 | `wrong[2] = 0x03;` | Block header 011: final, type 1. |
| 86–88 | `wrong[5] = 0x00;` | The first NLEN byte: NLEN becomes 0xFF00. |
| 89–91 | `wrong.resize(10);` | Only 3 of the 5 "hello" bytes are left. |
| 92–94 | `wrong[7] = 'j';` | "hello" → "jello" (byte 7 is the 'h'). |

**PNG rows (lines 96–115)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 96–101 | `Image tiny(3, 2); tiny.setPixel(0, 0, colours::red); ...` | A 3 × 2 picture; pixel (1, 1) stays black. |
| 102–111 | `Bytes rows; for (int y = 0; ...) { rows.push_back(0); for (int x = 0; ...) { Colour c = tiny.getPixel(x, y); rows.push_back(c.r); rows.push_back(c.g); rows.push_back(c.b); } }` | PNG's row layout (Section 41.8): filter byte 0, then R, G, B for each pixel, top row first. |
| 112–115 | `printBytes("PNG rows of a 3 x 2 picture:", rows); printBytes("and stored with zlib:", zlibStore(rows));` `return 0;` `}` | The 20 row bytes, and the 31 bytes of zlib data an IDAT chunk would hold. |

### What you should see

```
Adler-32 step by step for "Wiki":
  'W' (87): a = 88, b = 88
  'i' (105): a = 193, b = 281
  'k' (107): a = 300, b = 581
  'i' (105): a = 405, b = 986
Adler-32 of "Wiki" = 03DA0195, of "Wikipedia" = 11E60398
header 7801 = 30721 = 31 x 991 remainder 0
header 789C = 30876 = 31 x 996 remainder 0
header 78DA = 30938 = 31 x 998 remainder 0
zlib of "hello": 78 01 01 05 00 FA FF 68 65 6C 6C 6F 06 2C 02 15
150000 bytes stored in 150021 bytes, read back the same
the second block starts with: 00 FF FF 00 00
zlib of nothing: 78 01 01 00 00 FF FF 00 00 00 01
broken zlib data:
  the good data: accepted, 5 bytes
  header check broken: refused (the header check (% 31) fails)
  block type 1: refused (compressed blocks are not supported yet)
  NLEN wrong: refused (LEN and NLEN do not match)
  cut short: refused (a block is longer than the data)
  one letter changed: refused (the Adler-32 is wrong)
PNG rows of a 3 x 2 picture: 00 FF 00 00 00 FF 00 00 00 FF 00 FF FF FF 00 00 00 FF FF 00
and stored with zlib: 78 01 01 14 00 EB FF 00 FF 00 00 00 FF 00 00 00 FF 00 FF FF FF 00 00 00 FF FF 00 49 CA 07 F9
```

---

## Small examples

### Example 1 — Reading a block header

The byte `00`: BFINAL 0, BTYPE 00 → stored, more blocks follow. The byte `01`: stored, last. The byte `03`: BFINAL 1, BTYPE 01 → compressed with fixed codes (Chapter 45). The byte `05`: BFINAL 1, BTYPE 10 → compressed with custom codes.

### Example 2 — NLEN by hand

LEN = 1000 = 0x03E8 → bytes `E8 03`. NLEN = 0xFFFF − 0x03E8 = **0xFC17** → bytes `17 FC`.

### Example 3 — Adler-32 of one byte

The byte 'A' (65): a = 1 + 65 = 66, b = 0 + 66 = 66 → 66 × 65536 + 66 = **0x00420042**.

### Example 4 — The size of a picture's zlib data

A 300 × 300 RGB picture: rows = 300 × (1 + 900) = 270,300 bytes → 5 blocks (4 full ones of 65,535 and one of 8,160) → zlib = 270,300 + 2 + 25 + 4 = **270,331** bytes.

### Example 5 — Why "a" starts at 1

If a started at 0, a list of zero bytes would always give a = 0 and b = 0, so the checksum could not tell 10 zero bytes from 1,000 zero bytes. Starting at 1 makes b grow by 1 for every byte, so the **length** shows up in the checksum.

---

## Common mistakes

⚠️ **Big-endian LEN.** LEN and NLEN are **little-endian**; the zlib header and the Adler-32 are big-endian.

⚠️ **Forgetting NLEN**, or writing NLEN = −LEN instead of ~LEN. ~5 = 0xFFFA, but −5 as 16 bits is 0xFFFB.

⚠️ **Blocks longer than 65,535 bytes.** Split them.

⚠️ **No final block.** The last block must have BFINAL = 1, or a reader keeps waiting for more.

⚠️ **Adler-32 of the wrong bytes.** It covers the **original** data — not the zlib header, not the block headers.

⚠️ **Adler-32 starting at a = 0.** It starts at a = 1, b = 0.

⚠️ **Forgetting the filter byte** at the start of each PNG row. Without it, every row is one byte short, and the picture comes out slanted and colour-shifted.

---

## Practice

🏋️ **1.** Write the zlib bytes (with a stored block) for the 3-byte text "abc" by hand. (Adler-32 of "abc" is 024D0127.)

🏋️ **2.** Check by hand: is 78 5E a valid zlib header? Is 78 9D?

🏋️ **3.** How many bytes does `zlibStore` make for 65,535 bytes of data? For 65,536?

🏋️ **4.** Compute the Adler-32 of "abc" by hand and check the value in Practice 1.

🏋️ **5.** Change `zlibStore` to use blocks of at most 1,000 bytes. Does `zlibUnstore` still read the result correctly? (It should: any block size is allowed.)

🏋️ **6.** How many bytes are the PNG rows of a 640 × 480 RGB picture? And of an RGBA one?

🏋️ **7.** Write `bool zlibLooksValid(const Bytes& z)` that only checks the header (method 8 and % 31), and test it on the first two bytes of some files: a BMP, a PPM, a PNG's IDAT data.

🏋️ **8.** Why can't NLEN catch every damaged LEN? (Hint: what if **both** LEN and NLEN are damaged?)

---

## Answers

**1.**
> `78 01` · `01` · `03 00` · `FC FF` · `61 62 63` · `02 4D 01 27` — 15 bytes.

**2.**
> 0x785E = 30,814 = 31 × 994 → **valid** (level hint 1). 0x789D = 30,877 = 31 × 996 + 1 → **not** valid.

**3.**
> 65,535: one block → 65,535 + 2 + 5 + 4 = **65,546**. 65,536: two blocks (65,535 + 1) → 65,536 + 2 + 10 + 4 = **65,552**.

**4.**
> 'a' = 97: a = 98, b = 98. 'b' = 98: a = 196, b = 294. 'c' = 99: a = 295, b = 589.
> 589 = 0x024D, 295 = 0x0127 → **0x024D0127** ✓

**5.**

```cpp
const int length = std::min(1000, total - pos);
```

> Yes: 150,000 bytes become 150 blocks of 1,000, and the file is 150,000 + 2 + 750 + 4 = 150,756 bytes — the reader does not care about block sizes.

**6.**
> RGB: 480 × (1 + 1920) = **922,080** bytes. RGBA: 480 × (1 + 2560) = **1,229,280** bytes.

**7.**

```cpp
bool zlibLooksValid(const Bytes& z) {
    return hasBytes(z, 0, 2) && (z[0] & 0x0F) == 8 && (z[0] * 256 + z[1]) % 31 == 0;
}
```

> A BMP starts with "BM" = 0x42: method 2 → no. A PPM "P6": 0x50 → method 0 → no. A PNG's IDAT data: yes, usually 78 9C or 78 DA.

**8.**
> If LEN and NLEN are both damaged in a way that keeps NLEN = ~LEN (for example, a program wrote the wrong length but computed NLEN from it), the check passes. Then the **Adler-32** (and the PNG chunk's CRC) are the next line of defence.

---

## Summary

🧠 PNG pixels → **rows** (a filter byte + R G B (A) per pixel) → **zlib** → **IDAT** chunks.

🧠 zlib = **2-byte header** (78 01; CMF·256 + FLG divisible by **31**) + **Deflate blocks** + **Adler-32** (big-endian).

🧠 A **stored block**: 1 byte (BFINAL in bit 0, BTYPE 00) + **LEN** + **NLEN = ~LEN** (both **little-endian**) + LEN bytes. At most 65,535 bytes per block.

🧠 **Adler-32**: a = 1 + Σ bytes, b = Σ a, both mod **65,521**; result **b·65536 + a**. "Wikipedia" → 11E60398.

🧠 Stored blocks make data slightly **bigger**: + 2 + 5 per block + 4.

🧠 A PNG row = **1 + 3 × width** bytes (filter byte 0 = no filter); no padding; colours in **R, G, B** order.

---

## Next chapter

We have all the pieces: the signature, IHDR, IEND and CRC-32 from Chapter 40, and zlib with stored blocks from this chapter. In Chapter 42 we put them together into `savePNG` — and open our pictures, with **transparency**, in any web browser. We will also write a reader for our own PNG files, and see just how big uncompressed PNGs are (bigger than BMP!) — the reason the last chapters of Part 6 are all about compression.
