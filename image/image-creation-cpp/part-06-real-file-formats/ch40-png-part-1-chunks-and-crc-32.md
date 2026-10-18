# Chapter 40 — PNG, Part 1: Chunks and CRC-32

> **Part 6 · Chapter 40 of 82**
> **You need:** Chapters 1–39 (especially 4, 9 and 36) · **You will make:** `png.h` (big-endian helpers, CRC-32 two ways, the PNG signature, chunks, the IHDR header, and a chunk lister that checks every CRC), and a program that builds the skeleton of a PNG file and catches damaged copies of it

---

## What you will learn

- What **PNG** is, and the plan for the next four chapters.
- The 8-byte **signature**, and why every byte of it was chosen.
- How a PNG file is made of **chunks**: length, type, data and a check value.
- The **IHDR** chunk that describes the picture, and the **IEND** chunk that ends the file.
- **Big-endian** numbers (the opposite of BMP and TGA).
- What a **checksum** is, why simply adding bytes is not good enough, and how **CRC-32** works.
- How to compute CRC-32 bit by bit, and much faster with a **table**.
- How to walk through the chunks of any PNG file and spot damage.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **PNG** | Portable Network Graphics: the lossless, compressed picture format of the web. |
| **chunk** | One block of a PNG file: length, 4-letter type, data, CRC. |
| **chunk type** | The 4 letters that say what a chunk holds (IHDR, IDAT, IEND, …). |
| **critical chunk** | A chunk a reader must understand (its type starts with a capital letter). |
| **ancillary chunk** | An optional extra chunk a reader may skip (its type starts with a small letter). |
| **checksum** | A small number computed from data, stored with it, to detect damage. |
| **CRC** (cyclic redundancy check) | A very good kind of checksum, based on division. |
| **XOR** | "Exclusive or": a bit operation — 1 if the two bits differ, 0 if they are the same. |
| **polynomial** | Here: a pattern of bits used as the "divisor" of a CRC. |
| **lookup table** | A list of answers worked out in advance, so a slow calculation becomes one step. |

---

## 40.1 The plan: PNG in four chapters

📖 **New word: PNG** — **Portable Network Graphics**, made in 1996 as a free replacement for GIF. It is:

- **lossless** — the pixels come back exactly (Chapter 39);
- **compressed** — often several times smaller than BMP;
- able to store **alpha** — and every browser shows it;
- supported **everywhere**: browsers, phones, every operating system.

It is also more complicated than anything so far. So we build it in steps:

| chapter | what we add | result |
|---|---|---|
| **40** (this one) | the file structure: signature, chunks, CRC-32 | the skeleton of a PNG |
| 41 | zlib's container with **stored** (uncompressed) blocks, and Adler-32 | the pixel data, packed but not yet compressed |
| 42 | putting it together | **real PNG files** that open everywhere |
| 43 | filters | the trick that makes PNG compress well |

Then Chapters 44 and 45 add real compression (Huffman coding and Deflate).

---

## 40.2 The signature

Every PNG file starts with the same **8 bytes**:

```
   89  50  4E  47  0D  0A  1A  0A
   ‰   P   N   G   CR  LF  ^Z  LF
```

Each byte was chosen to **catch a mistake**:

| byte(s) | why |
|---|---|
| 0x89 | not a text character: a program that treats the file as text, or strips the top bit of each byte (old e-mail systems did), changes it |
| `P N G` | so people can recognise the file in a hex dump |
| 0x0D 0x0A | a Windows line ending (CR LF): if the file is copied in **text** mode, this becomes 0x0A (Chapter 7's warning) |
| 0x1A | "end of file" for old MS-DOS programs: printing the file with the `type` command stops here, instead of filling the screen with rubbish |
| 0x0A | a Unix line ending (LF): text-mode copying on other systems turns it into 0x0D 0x0A |

So if the signature is not exactly these 8 bytes, the file was damaged on its way — and a reader refuses it at once.

---

## 40.3 Chunks

📖 **New word: chunk** — after the signature, a PNG file is a list of **chunks**. Every chunk has the same four parts:

```
   ┌──────────┬──────────┬──────────────────┬──────────┐
   │  length  │   type   │       data       │   CRC    │
   │ 4 bytes  │ 4 bytes  │  "length" bytes  │ 4 bytes  │
   └──────────┴──────────┴──────────────────┴──────────┘
                └────── the CRC is computed over these ──────┘
                        (type + data, not the length)
```

- **length**: how many bytes of data (it does **not** count itself, the type or the CRC). It can be 0.
- **type**: 4 letters, like `IHDR`.
- **data**: the chunk's contents.
- **CRC**: a check value over the type and data (Section 40.6).

A chunk takes **12 + length** bytes in all.

📖 **New word: chunk type** — the 4 letters say what the chunk holds. The three we need:

| type | meaning |
|---|---|
| **IHDR** | "image header": width, height, colour type, … — always the **first** chunk |
| **IDAT** | "image data": the compressed pixels (Chapters 41–42); there can be several |
| **IEND** | "image end": always the **last** chunk, with no data (length 0) |

📖 **New words: critical and ancillary chunks** — the **case** of the first letter matters. A capital letter (IHDR, IDAT, IEND, PLTE) means **critical**: a reader that does not understand it must give up. A small letter means **ancillary** (optional): `tEXt` (a text comment), `gAMA` (gamma, Chapter 17), `pHYs` (pixels per metre, like BMP's), `tIME` (when it was made), … A reader may simply skip ancillary chunks it does not know. This is how PNG has been extended for 30 years without breaking old readers.

💡 Why chunks? Because a reader can **skip** any chunk without understanding it: read the length, jump over 12 + length bytes, and you are at the next chunk. New kinds of chunks can be added at any time.

---

## 40.4 Big-endian numbers

PNG stores every number **big-endian**: the **biggest** byte first — the opposite of BMP and TGA (Chapter 36, Section 36.5).

🔢 **Maths: 13 as 4 big-endian bytes**

> 13 = 0x0000000D → **00 00 00 0D** (BMP would write 0D 00 00 00)

Chapter 36's Practice 5 already wrote these helpers; now they go into the library:

```cpp
inline void putU32BE(Bytes& out, std::uint32_t v) {
    out.push_back(static_cast<std::uint8_t>((v >> 24) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((v >> 16) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((v >> 8) & 0xFF));
    out.push_back(static_cast<std::uint8_t>(v & 0xFF));
}
```

Big-endian is easier to read in a hex dump (the bytes are in the order we write digits), which is why it is also called **network byte order**: most internet protocols use it.

---

## 40.5 The IHDR chunk

The first chunk is always IHDR, with exactly **13** bytes of data:

| offset in data | size | field | our value | meaning |
|---|---|---|---|---|
| 0 | 4 | width | | in pixels, big-endian, at least 1 |
| 4 | 4 | height | | in pixels, big-endian, at least 1 |
| 8 | 1 | bit depth | **8** | bits per channel: 8 = one byte each for R, G, B (and A) |
| 9 | 1 | colour type | **2** or **6** | 2 = RGB (true-colour); 6 = RGB + alpha |
| 10 | 1 | compression method | 0 | always 0: zlib/Deflate (Chapter 41) |
| 11 | 1 | filter method | 0 | always 0: the five filters of Chapter 43 |
| 12 | 1 | interlace method | 0 | 0 = rows in order (1 = "Adam7", a fancy order for slow downloads — we do not use it) |

(Other colour types: 0 = grey, 3 = palette, 4 = grey + alpha. And bit depths 1, 2, 4 and 16 exist too. We only write 8-bit RGB and RGBA.)

🔢 **Maths: the IHDR data for a 4 × 2 RGB picture**

> width `00 00 00 04`, height `00 00 00 02`, then `08 02 00 00 00`

---

## 40.6 Checksums

📖 **New word: checksum** — a small number computed from some data and stored **with** it. Later, anyone can compute it again: if the answer differs from the stored one, the data has been **damaged**.

You already know one: the last digit of many ID numbers and barcodes is a check digit, so a mistyped number is caught.

### Why not just add the bytes?

The simplest checksum adds up all the bytes. But it misses very common kinds of damage:

```
simple sum: AB 131, BA 131; CRC-32: AB 30694C07, BA 824D4E7E
```

"AB" and "BA" have the **same** sum (65 + 66 = 131), so two swapped bytes go unnoticed. So do two errors that cancel out (one byte one too big, another one too small). We need a checksum where **every** byte's **position** matters, and where small changes stir the result up completely.

📖 **New word: CRC** — **cyclic redundancy check**. CRC-32 gives a 32-bit check value. It catches:

- **every** change of a single bit, anywhere;
- **every** change of 2 or 3 bits in chunks up to about 11,000 bytes;
- **every** burst of damage up to 32 bits long (like a scratch);
- all other damage, except about 1 time in 4 billion (2³²).

### The idea: a remainder

Think about ordinary division. 1234 ÷ 7 = 176, remainder **2**. If someone changes 1234 to 1244, the remainder becomes 1244 − 7 × 177 = **5** — different. The remainder is a "fingerprint" of the number. Change any digit and it (usually) changes.

CRC does the same with the bits of the data: it treats all the bits as one enormous number, divides it by a fixed 33-bit number, and keeps the **remainder** (32 bits). Two twists make it fast and good for computers:

📖 **New word: XOR** — "exclusive or", written `^` in C++: for each pair of bits, the result is **1 if they differ**, 0 if they are the same.

```
     1 1 0 0
   ^ 1 0 1 0
   ─────────
     0 1 1 0
```

1. The division uses **XOR instead of subtraction**. No borrowing, no carrying — each bit is handled on its own. This makes the maths a bit strange (it is called "arithmetic of polynomials over two numbers, 0 and 1"), but it makes the hardware very simple.

📖 **New word: polynomial** — 2. The fixed divisor is a carefully chosen bit pattern, called the **polynomial**. For CRC-32 it is 0x04C11DB7 (plus a 33rd top bit). Mathematicians chose it because it catches the most kinds of errors.

### Bit by bit

Here is the CRC-32 that PNG uses (the same one as ZIP files and Ethernet), one bit at a time:

```cpp
std::uint32_t crc = 0xFFFFFFFFu;
for each byte:
    crc ^= byte;
    repeat 8 times:
        if (crc & 1u) {
            crc = (crc >> 1) ^ 0xEDB88320u;
        } else {
            crc >>= 1;
        }
return crc ^ 0xFFFFFFFFu;
```

What does it do?

- `crc` is the running **remainder**. Each byte is mixed into it with XOR.
- For each of the byte's 8 bits: shift the remainder by one place. If the bit that falls off is 1, "subtract" (XOR) the polynomial. That is long division, one bit at a time — exactly like the steps of 1234 ÷ 7 on paper, but in base 2 with XOR.
- Why 0xEDB88320 and not 0x04C11DB7? It is the same polynomial **written backwards** (bit 0 ↔ bit 31). PNG feeds each byte's bits lowest first, so the whole calculation is done mirrored, which lets us shift **right** instead of left.
- Starting at 0xFFFFFFFF (all ones) and XOR-ing with 0xFFFFFFFF at the end are two small extras: without them, extra **zero** bytes at the start of the data would not change the CRC.

### The check value

Every CRC-32 implementation is tested with the 9 bytes of the text **"123456789"**. The right answer is **CBF43926**:

```
CRC-32 of "123456789": bit by bit CBF43926, with the table CBF43926
```

---

## 40.7 Faster: a lookup table

📖 **New word: lookup table** — the bit-by-bit version does 8 small steps per byte. But look: the 8 steps only depend on the **low 8 bits** of `crc ^ byte` — a number from 0 to 255. So we can work out the result of "8 steps" for all 256 possible values **once**, store them in a table, and then handle each byte in **one** step:

```cpp
crc = table[(crc ^ data[i]) & 0xFFu] ^ (crc >> 8);
```

- `(crc ^ data[i]) & 0xFF`: the 8 bits the 8 steps would have used;
- `table[...]`: what those 8 steps would have XOR-ed in;
- `crc >> 8`: the rest of the remainder, shifted along by 8 places.

The table is built with the same 8-step loop, once, the first time it is needed (like Chapter 17's `linearTable`, with a `static` variable):

```
table[1] = 77073096, table[128] = EDB88320, table[255] = 2D02EF8D
```

(table[128] is the polynomial itself: 128 = binary 1000 0000, so only the **last** of the 8 steps drops a 1.)

The answers are the same, but about 8 times faster — important for a picture with millions of bytes.

### Two famous CRCs

Every PNG file ends with the same 12 bytes, because IEND has no data:

> length `00 00 00 00`, type `49 45 4E 44` ("IEND"), CRC of "IEND" = **AE 42 60 82**

```
CRC-32 of "IEND": AE426082
```

If you open any PNG file in a hex viewer, its last 4 bytes are `AE 42 60 82`.

---

## 40.8 Building the skeleton

`appendChunk` builds a complete chunk at the end of a list of bytes:

1. the **length** (big-endian): the number of data bytes;
2. the 4 **type** letters;
3. the **data**;
4. the **CRC**, computed over the type and the data — which are already in the list, so we compute it **there**, starting at the type.

With the signature, an IHDR and an IEND, we get the skeleton of a 4 × 2 PNG:

```
signature + IHDR + IEND = 45 bytes:
  00: 89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52
  10: 00 00 00 04 00 00 00 02 08 02 00 00 00 F0 CA EA
  20: 34 00 00 00 00 49 45 4E 44 AE 42 60 82
```

| offset (hex) | bytes | meaning |
|---|---|---|
| 00 | 89 50 4E 47 0D 0A 1A 0A | the signature |
| 08 | 00 00 00 0D | IHDR length: 13 |
| 0C | 49 48 44 52 | "IHDR" |
| 10 | 00 00 00 04 · 00 00 00 02 · 08 02 00 00 00 | width 4, height 2, 8 bits, RGB, 0, 0, 0 |
| 1D | F0 CA EA 34 | CRC of the 17 bytes "IHDR" + data |
| 21 | 00 00 00 00 | IEND length: 0 |
| 25 | 49 45 4E 44 | "IEND" |
| 29 | AE 42 60 82 | CRC of "IEND" |

8 + (12 + 13) + (12 + 0) = **45** bytes ✓.

⚠️ This is **not yet a valid PNG**: it has no IDAT chunk, so there are no pixels. A viewer will refuse it. Chapters 41 and 42 add the pixels.

---

## 40.9 Walking through the chunks

A PNG reader starts by walking through the chunks:

1. check the 8 signature bytes;
2. at each position: read the length and type (8 bytes — are they there?);
3. check that the whole chunk (12 + length bytes) is inside the file — in `long long`, since the length comes from the file (Chapter 38's lesson);
4. compute the CRC over type + data and compare it with the stored one;
5. jump to the next chunk; stop after IEND.

Our `listChunks` does exactly that, and returns a list of `PngChunk`s — each with its type, where its data starts, its length, and whether its CRC was right. The program uses it on the skeleton and on three damaged copies:

```
the chunks: IHDR (13 bytes, CRC ok) IEND (0 bytes, CRC ok)
width changed to 5: IHDR (13 bytes, CRC WRONG) IEND (0 bytes, CRC ok)
last 6 bytes missing: IHDR (13 bytes, CRC ok) -- a chunk header is cut off
signature changed: -- no PNG signature
```

Changing **one** byte of the width (from 4 to 5) is caught at once by IHDR's CRC. A file that was cut short is caught by the size checks. And a wrong signature is refused before anything else is read.

💡 The CRC only checks for **damage**. It is not a lock: anyone who changes a chunk on purpose can simply compute a new CRC.

---

## Code, part 1: `png.h`

File: `common/png.h` (new). It includes `tga.h` (and through it, the whole file-format branch: `Bytes`, `hasBytes`, `writeBytes`, …).

```cpp
#ifndef PNG_H
#define PNG_H

#include <array>
#include <cstdint>
#include <string>
#include <vector>
#include "tga.h"

inline void putU32BE(Bytes& out, std::uint32_t v) {
    out.push_back(static_cast<std::uint8_t>((v >> 24) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((v >> 16) & 0xFF));
    out.push_back(static_cast<std::uint8_t>((v >> 8) & 0xFF));
    out.push_back(static_cast<std::uint8_t>(v & 0xFF));
}

inline std::uint32_t getU32BE(const Bytes& in, int pos) {
    return (static_cast<std::uint32_t>(in[pos]) << 24) |
           (static_cast<std::uint32_t>(in[pos + 1]) << 16) |
           (static_cast<std::uint32_t>(in[pos + 2]) << 8) | static_cast<std::uint32_t>(in[pos + 3]);
}

inline std::uint32_t crc32Bitwise(const Bytes& data, int from, int count) {
    std::uint32_t crc = 0xFFFFFFFFu;
    for (int i = from; i < from + count; ++i) {
        crc ^= data[i];
        for (int bit = 0; bit < 8; ++bit) {
            if (crc & 1u) {
                crc = (crc >> 1) ^ 0xEDB88320u;
            } else {
                crc >>= 1;
            }
        }
    }
    return crc ^ 0xFFFFFFFFu;
}

inline std::array<std::uint32_t, 256> makeCrcTable() {
    std::array<std::uint32_t, 256> table{};
    for (std::uint32_t n = 0; n < 256; ++n) {
        std::uint32_t c = n;
        for (int bit = 0; bit < 8; ++bit) {
            c = (c & 1u) ? ((c >> 1) ^ 0xEDB88320u) : (c >> 1);
        }
        table[n] = c;
    }
    return table;
}

inline const std::array<std::uint32_t, 256>& crcTable() {
    static const std::array<std::uint32_t, 256> table = makeCrcTable();
    return table;
}

inline std::uint32_t crc32(const Bytes& data, int from, int count) {
    const std::array<std::uint32_t, 256>& table = crcTable();
    std::uint32_t crc = 0xFFFFFFFFu;
    for (int i = from; i < from + count; ++i) {
        crc = table[(crc ^ data[i]) & 0xFFu] ^ (crc >> 8);
    }
    return crc ^ 0xFFFFFFFFu;
}

inline void appendPngSignature(Bytes& out) {
    const std::uint8_t signature[8] = {0x89, 'P', 'N', 'G', 0x0D, 0x0A, 0x1A, 0x0A};
    out.insert(out.end(), signature, signature + 8);
}

inline void appendChunk(Bytes& out, const std::string& type, const Bytes& data) {
    putU32BE(out, static_cast<std::uint32_t>(data.size()));
    const int typeStart = static_cast<int>(out.size());
    for (char ch : type) {
        out.push_back(static_cast<std::uint8_t>(ch));
    }
    out.insert(out.end(), data.begin(), data.end());
    putU32BE(out, crc32(out, typeStart, 4 + static_cast<int>(data.size())));
}

inline Bytes makeIhdr(int width, int height, bool withAlpha) {
    Bytes data;
    putU32BE(data, static_cast<std::uint32_t>(width));
    putU32BE(data, static_cast<std::uint32_t>(height));
    data.push_back(8);
    data.push_back(withAlpha ? 6 : 2);
    data.push_back(0);
    data.push_back(0);
    data.push_back(0);
    return data;
}

struct PngChunk {
    std::string type;
    int dataStart = 0;
    int length = 0;
    bool crcOk = false;
};

inline std::string listChunks(const Bytes& file, std::vector<PngChunk>& chunks) {
    chunks.clear();
    const std::uint8_t signature[8] = {0x89, 'P', 'N', 'G', 0x0D, 0x0A, 0x1A, 0x0A};
    if (file.size() > 2147483647u || !hasBytes(file, 0, 8)) {
        return "too short for the signature";
    }
    for (int i = 0; i < 8; ++i) {
        if (file[i] != signature[i]) {
            return "no PNG signature";
        }
    }
    int pos = 8;
    while (pos < static_cast<int>(file.size())) {
        if (!hasBytes(file, pos, 8)) {
            return "a chunk header is cut off";
        }
        const std::uint32_t length = getU32BE(file, pos);
        if (static_cast<long long>(pos) + 12 + length > static_cast<long long>(file.size())) {
            return "a chunk is longer than the file";
        }
        PngChunk chunk;
        for (int i = 0; i < 4; ++i) {
            chunk.type += static_cast<char>(file[pos + 4 + i]);
        }
        chunk.dataStart = pos + 8;
        chunk.length = static_cast<int>(length);
        const std::uint32_t stored = getU32BE(file, chunk.dataStart + chunk.length);
        chunk.crcOk = (stored == crc32(file, pos + 4, 4 + chunk.length));
        chunks.push_back(chunk);
        pos = chunk.dataStart + chunk.length + 4;
        if (chunk.type == "IEND") {
            break;
        }
    }
    return "";
}

#endif
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–8 | include guard and `#include` lines | `std::array` for the table; exact-size integers; strings for chunk types; lists; and the file-format branch. |
| 10–15 | `inline void putU32BE(Bytes& out, std::uint32_t v) { ... }` | Add a 4-byte number, **big-endian**: highest byte first (Section 40.4). |
| 17–21 | `inline std::uint32_t getU32BE(const Bytes& in, int pos) { return (static_cast<std::uint32_t>(in[pos]) << 24) \| ...; }` | Read one: the first byte is the highest. |
| 23–24 | `inline std::uint32_t crc32Bitwise(const Bytes& data, int from, int count) { std::uint32_t crc = 0xFFFFFFFFu;` | CRC-32 of `count` bytes starting at `from`, the slow, clear way (Section 40.6). Start with all ones. |
| 25–26 | `for (int i = from; i < from + count; ++i) { crc ^= data[i];` | Mix each byte into the low 8 bits of the remainder. |
| 27–33 | `for (int bit = 0; bit < 8; ++bit) { if (crc & 1u) { crc = (crc >> 1) ^ 0xEDB88320u; } else { crc >>= 1; } }` | One step of long division per bit: shift, and if a 1 fell off, XOR the (mirrored) polynomial. |
| 34–36 | `}` `return crc ^ 0xFFFFFFFFu;` `}` | Flip all the bits at the end. |
| 38–48 | `inline std::array<std::uint32_t, 256> makeCrcTable() { ... for (std::uint32_t n = 0; n < 256; ++n) { std::uint32_t c = n; for (int bit = 0; bit < 8; ++bit) { c = (c & 1u) ? ((c >> 1) ^ 0xEDB88320u) : (c >> 1); } table[n] = c; } return table; }` | For every possible low byte n, the result of the 8 steps (Section 40.7). |
| 50–53 | `inline const std::array<std::uint32_t, 256>& crcTable() { static const std::array<std::uint32_t, 256> table = makeCrcTable(); return table; }` | The table, built only once (the first call), and shared by every later call. |
| 55–62 | `inline std::uint32_t crc32(const Bytes& data, int from, int count) { ... crc = table[(crc ^ data[i]) & 0xFFu] ^ (crc >> 8); ... }` | The fast CRC-32: one table step per byte. Same answers as `crc32Bitwise`. |
| 64–67 | `inline void appendPngSignature(Bytes& out) { const std::uint8_t signature[8] = {0x89, 'P', 'N', 'G', 0x0D, 0x0A, 0x1A, 0x0A}; out.insert(out.end(), signature, signature + 8); }` | The 8 signature bytes (Section 40.2). `insert` can copy from a plain array: from its start to start + 8. |
| 69–70 | `inline void appendChunk(Bytes& out, const std::string& type, const Bytes& data) { putU32BE(out, static_cast<std::uint32_t>(data.size()));` | Add a whole chunk (Section 40.8). First its length. |
| 71–74 | `const int typeStart = static_cast<int>(out.size()); for (char ch : type) { out.push_back(static_cast<std::uint8_t>(ch)); }` | Remember where the type starts (the CRC begins there), then add the 4 letters. |
| 75 | `out.insert(out.end(), data.begin(), data.end());` | The data. |
| 76–77 | `putU32BE(out, crc32(out, typeStart, 4 + static_cast<int>(data.size())));` `}` | The CRC over type + data, which are now the last 4 + length bytes of `out`. |
| 79–89 | `inline Bytes makeIhdr(int width, int height, bool withAlpha) { ... data.push_back(8); data.push_back(withAlpha ? 6 : 2); data.push_back(0); data.push_back(0); data.push_back(0); return data; }` | The 13 bytes of IHDR data (Section 40.5): width, height, bit depth 8, colour type 2 or 6, and three zeros. |
| 91–96 | `struct PngChunk { std::string type; int dataStart = 0; int length = 0; bool crcOk = false; };` | What `listChunks` finds out about each chunk. |
| 98–99 | `inline std::string listChunks(const Bytes& file, std::vector<PngChunk>& chunks) { chunks.clear();` | Walk through a PNG's chunks (Section 40.9). Returns `""` if the walk reached the end, or a problem. |
| 100–108 | the signature checks | Too big (or too small) to be a PNG we can handle; then all 8 signature bytes must match. |
| 109–113 | `int pos = 8; while (pos < static_cast<int>(file.size())) { if (!hasBytes(file, pos, 8)) { return "a chunk header is cut off"; }` | From the first chunk on: is there room for the length and the type? |
| 114–117 | `const std::uint32_t length = getU32BE(file, pos); if (static_cast<long long>(pos) + 12 + length > static_cast<long long>(file.size())) { return "a chunk is longer than the file"; }` | The whole chunk must be inside the file — checked in `long long`, because `length` comes from the file and could be up to 4 billion. |
| 118–123 | `PngChunk chunk; for (int i = 0; i < 4; ++i) { chunk.type += static_cast<char>(file[pos + 4 + i]); } chunk.dataStart = pos + 8; chunk.length = static_cast<int>(length);` | Fill in the chunk's type, data position and length. |
| 124–125 | `const std::uint32_t stored = getU32BE(file, chunk.dataStart + chunk.length); chunk.crcOk = (stored == crc32(file, pos + 4, 4 + chunk.length));` | Compare the stored CRC with one computed over type + data. |
| 126–131 | `chunks.push_back(chunk); pos = chunk.dataStart + chunk.length + 4; if (chunk.type == "IEND") { break; } }` | Save it, jump to the next chunk, and stop after IEND (anything after IEND is ignored). |
| 132–133 | `return "";` `}` | The walk is complete. |
| 135 | `#endif` | End of the include guard. |

---

## Code, part 2: CRCs and a skeleton PNG

File: `ch40/png_chunks.cpp`

```cpp
#include <iostream>
#include <string>
#include <vector>
#include "png.h"

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

int simpleSum(const Bytes& data) {
    int sum = 0;
    for (std::uint8_t b : data) {
        sum += b;
    }
    return sum % 256;
}

void printChunks(const char* label, const Bytes& file) {
    std::vector<PngChunk> chunks;
    std::string problem = listChunks(file, chunks);
    std::cout << label << ":";
    for (const PngChunk& c : chunks) {
        std::cout << " " << c.type << " (" << c.length << " bytes, CRC "
                  << (c.crcOk ? "ok" : "WRONG") << ")";
    }
    if (!problem.empty()) {
        std::cout << " -- " << problem;
    }
    std::cout << "\n";
}

int main() {
    Bytes check = bytesOf("123456789");
    std::cout << "CRC-32 of \"123456789\": bit by bit " << hex32(crc32Bitwise(check, 0, 9))
              << ", with the table " << hex32(crc32(check, 0, 9)) << "\n";
    Bytes iend = bytesOf("IEND");
    std::cout << "CRC-32 of \"IEND\": " << hex32(crc32(iend, 0, 4)) << "\n";
    const std::array<std::uint32_t, 256>& table = crcTable();
    std::cout << "table[1] = " << hex32(table[1]) << ", table[128] = " << hex32(table[128])
              << ", table[255] = " << hex32(table[255]) << "\n";

    Bytes ab = bytesOf("AB");
    Bytes ba = bytesOf("BA");
    std::cout << "simple sum: AB " << simpleSum(ab) << ", BA " << simpleSum(ba)
              << "; CRC-32: AB " << hex32(crc32(ab, 0, 2)) << ", BA " << hex32(crc32(ba, 0, 2))
              << "\n";

    Bytes file;
    appendPngSignature(file);
    appendChunk(file, "IHDR", makeIhdr(4, 2, false));
    appendChunk(file, "IEND", Bytes{});
    std::cout << "signature + IHDR + IEND = " << file.size() << " bytes:\n";
    for (int i = 0; i < static_cast<int>(file.size()); i += 16) {
        std::cout << "  " << hexByte(static_cast<std::uint8_t>(i)) << ":";
        for (int j = i; j < i + 16 && j < static_cast<int>(file.size()); ++j) {
            std::cout << " " << hexByte(file[j]);
        }
        std::cout << "\n";
    }

    printChunks("the chunks", file);
    Bytes damaged = file;
    damaged[19] = 5;
    printChunks("width changed to 5", damaged);
    Bytes cut = file;
    cut.resize(cut.size() - 6);
    printChunks("last 6 bytes missing", cut);
    Bytes notPng = file;
    notPng[1] = 'Q';
    printChunks("signature changed", notPng);
    return 0;
}
```

Build and run (from the `code/ch40` folder):

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common png_chunks.cpp -o png_chunks
./png_chunks
```

### Line by line

**Helpers (lines 1–40)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–4 | the `#include` lines | Printing, strings, lists, and the new header. |
| 6–8 | `Bytes bytesOf(const std::string& text) { return Bytes(text.begin(), text.end()); }` | The bytes of a piece of text (each `char` becomes one byte). |
| 10–18 | `std::string hex32(std::uint32_t v) { Bytes four; putU32BE(four, v); std::string s; for (std::uint8_t b : four) { s += hexByte(b); } return s; }` | A 32-bit number as 8 hex digits, biggest first: CRCs are usually written this way. |
| 20–26 | `int simpleSum(const Bytes& data) { ... return sum % 256; }` | The naive checksum of Section 40.6, kept to one byte. |
| 28–40 | `void printChunks(const char* label, const Bytes& file) { std::vector<PngChunk> chunks; std::string problem = listChunks(file, chunks); ... }` | Walk a file's chunks and print each one's type, length and CRC result, then any problem. |

**CRCs (lines 42–56)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 43–45 | `Bytes check = bytesOf("123456789"); std::cout << ... hex32(crc32Bitwise(check, 0, 9)) << ... hex32(crc32(check, 0, 9)) ...` | The standard check value, computed both ways (Section 40.6). `\"` puts a `"` inside a string. |
| 46–47 | `Bytes iend = bytesOf("IEND"); ...` | The CRC every PNG ends with (Section 40.7). |
| 48–50 | `const std::array<std::uint32_t, 256>& table = crcTable(); ...` | Three entries of the table. |
| 52–56 | `Bytes ab = bytesOf("AB"); Bytes ba = bytesOf("BA"); ...` | The simple sum cannot tell swapped bytes apart; CRC-32 can. |

**The skeleton (lines 58–69)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 58–61 | `Bytes file; appendPngSignature(file); appendChunk(file, "IHDR", makeIhdr(4, 2, false)); appendChunk(file, "IEND", Bytes{});` | Signature, IHDR for a 4 × 2 RGB picture, and IEND with no data (Section 40.8). |
| 62–69 | the hex dump loop | Chapter 36's dump, 16 bytes per line. |

**Damage (lines 71–82)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 71 | `printChunks("the chunks", file);` | The good skeleton: two chunks, both CRCs right. |
| 72–74 | `Bytes damaged = file; damaged[19] = 5; printChunks(...);` | Byte 19 (0x13) is the low byte of the width: 4 becomes 5. |
| 75–77 | `Bytes cut = file; cut.resize(cut.size() - 6); printChunks(...);` | Cut into the IEND chunk. |
| 78–80 | `Bytes notPng = file; notPng[1] = 'Q'; printChunks(...);` | "PNG" becomes "QNG". |
| 81–82 | `return 0;` `}` | Done. (Nothing is written to disk: the skeleton is not yet a complete PNG.) |

### What you should see

```
CRC-32 of "123456789": bit by bit CBF43926, with the table CBF43926
CRC-32 of "IEND": AE426082
table[1] = 77073096, table[128] = EDB88320, table[255] = 2D02EF8D
simple sum: AB 131, BA 131; CRC-32: AB 30694C07, BA 824D4E7E
signature + IHDR + IEND = 45 bytes:
  00: 89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52
  10: 00 00 00 04 00 00 00 02 08 02 00 00 00 F0 CA EA
  20: 34 00 00 00 00 49 45 4E 44 AE 42 60 82
the chunks: IHDR (13 bytes, CRC ok) IEND (0 bytes, CRC ok)
width changed to 5: IHDR (13 bytes, CRC WRONG) IEND (0 bytes, CRC ok)
last 6 bytes missing: IHDR (13 bytes, CRC ok) -- a chunk header is cut off
signature changed: -- no PNG signature
```

---

## Small examples

### Example 1 — The size of a chunk

A `tEXt` chunk with 20 bytes of text takes 4 + 4 + 20 + 4 = **32** bytes.

### Example 2 — Reading a length

The bytes `00 00 2A 10` before a chunk type: big-endian 0x2A10 = 2 × 4096 + 10 × 256 + 1 × 16 + 0 = **10,768** bytes of data.

### Example 3 — Critical or ancillary?

`IDAT`: capital I → critical. `pHYs`: small p → ancillary, may be skipped. `gAMA`: ancillary.

### Example 4 — XOR by hand

0x5A ^ 0x0F = 0101 1010 ^ 0000 1111 = 0101 0101 = **0x55**. And 0x55 ^ 0x0F = 0x5A again: XOR-ing twice with the same value undoes it.

### Example 5 — One table step

The very first step for the byte 0x01, starting from crc = 0xFFFFFFFF: (0xFFFFFFFF ^ 0x01) & 0xFF = 0xFE → crc = table[0xFE] ^ 0x00FFFFFF. One look-up and one XOR replace 8 shift-and-test steps.

---

## Common mistakes

⚠️ **Little-endian by habit.** After BMP and TGA, it is easy to write `putU32` instead of `putU32BE`. PNG is **big-endian** everywhere.

⚠️ **CRC over the wrong bytes.** It covers the **type and data**, not the length.

⚠️ **Counting the type or CRC in the length.** The length is the data only.

⚠️ **Forgetting the starting value or the final XOR.** Both are 0xFFFFFFFF. Test with "123456789" → CBF43926.

⚠️ **Using the un-mirrored polynomial with right shifts.** With `>> 1`, the constant is 0xEDB88320, not 0x04C11DB7.

⚠️ **Trusting the chunk length.** Check it against the file size in `long long` before reading.

⚠️ **Wrong case in chunk types.** "Ihdr" is not "IHDR": the case of each letter has a meaning.

---

## Practice

🏋️ **1.** How many bytes does an IHDR chunk take in all? And the smallest possible PNG file, with one IDAT chunk of 12 bytes of data?

🏋️ **2.** Write the bytes of an IEND chunk from memory.

🏋️ **3.** Compute 0b1101 ^ 0b1011, and 0xFF ^ 0xA5.

🏋️ **4.** Check that `crc32` and `crc32Bitwise` agree on 1000 different byte lists (for example, the bytes 0, 1, 2, …, k for k from 0 to 999).

🏋️ **5.** Add a `tEXt` chunk to the skeleton, with the data `Author` + a zero byte + your name. Check its CRC with `listChunks`.

🏋️ **6.** Change `listChunks` to also refuse files whose **first** chunk is not IHDR, or whose IHDR length is not 13.

🏋️ **7.** Write a program that lists the chunks of a real PNG file from your computer (with `readFileBytes`). Which ancillary chunks does it have?

🏋️ **8.** Flip one bit anywhere in the IHDR data of the skeleton, 104 times (each of the 13 × 8 bits once). How many times does the CRC catch the change?

---

## Answers

**1.**
> IHDR: 12 + 13 = **25** bytes.
> 8 (signature) + 25 (IHDR) + 24 (IDAT: 12 + 12) + 12 (IEND) = **69** bytes.

**2.**
> `00 00 00 00 49 45 4E 44 AE 42 60 82`

**3.**
> 1101 ^ 1011 = **0110** (6). 0xFF ^ 0xA5 = **0x5A** (XOR with all ones flips every bit).

**4.**

```cpp
Bytes data;
int agree = 0;
for (int k = 0; k < 1000; ++k) {
    data.push_back(static_cast<std::uint8_t>(k));
    int n = static_cast<int>(data.size());
    if (crc32(data, 0, n) == crc32Bitwise(data, 0, n)) {
        ++agree;
    }
}
std::cout << agree << " of 1000 agree\n";
```

> 1000 of 1000.

**5.**

```cpp
Bytes text = bytesOf("Author");
text.push_back(0);
Bytes name = bytesOf("Ana");
text.insert(text.end(), name.begin(), name.end());
appendChunk(file, "tEXt", text);
```

> Add it **before** IEND (between the IHDR and IEND lines). `listChunks` then shows `tEXt (10 bytes, CRC ok)`.

**6.**

```cpp
if (chunks.empty() || chunks[0].type != "IHDR" || chunks[0].length != 13) {
    return "the first chunk must be a 13-byte IHDR";
}
```

> (After the loop, before `return "";`.)

**7.**
> Typical answers: `IHDR`, `sRGB`, `gAMA`, `pHYs`, many `IDAT`s, `IEND`. Pictures saved by phones and editors often add `tEXt`, `iTXt` or `eXIf` chunks with extra information.

**8.**
> **104** of 104: CRC-32 catches every 1-bit change (Section 40.6).

---

## Summary

🧠 A PNG file = **8-byte signature** + **chunks**. Signature: `89 50 4E 47 0D 0A 1A 0A` — designed to catch text-mode damage.

🧠 A chunk = **length** (4, data only) + **type** (4 letters) + **data** + **CRC-32** of type + data. Capital first letter = critical, small = ancillary.

🧠 **IHDR** (first, 13 bytes): width, height, bit depth 8, colour type 2 (RGB) or 6 (RGBA), 0, 0, 0. **IEND** (last, empty): ends with `AE 42 60 82`.

🧠 All PNG numbers are **big-endian**.

🧠 **CRC-32**: a remainder of XOR long division. Start 0xFFFFFFFF, per bit: shift right, XOR 0xEDB88320 if a 1 fell off; end with XOR 0xFFFFFFFF. "123456789" → **CBF43926**.

🧠 A **256-entry table** turns the 8 steps per byte into one.

🧠 A reader walks the chunks, checks every length against the file size, and every CRC.

---

## Next chapter

The skeleton has no pixels yet. PNG keeps its pixels in IDAT chunks, inside a container called **zlib**. In Chapter 41 we learn how zlib is built: a 2-byte header, the data in **blocks**, and a second checksum, **Adler-32**. We will use zlib's simplest kind of block, a **stored** block, which holds bytes without compressing them — and that is all we need to make our first PNG files in Chapter 42.
