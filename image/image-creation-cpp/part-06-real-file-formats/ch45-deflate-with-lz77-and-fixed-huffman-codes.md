# Chapter 45 — Deflate with LZ77 and Fixed Huffman Codes

> **Part 6 · Chapter 45 of 82**
> **You need:** Chapters 1–44 (especially 41, 43 and 44) · **You will make:** `deflate.h` (LZ77 matching, Deflate blocks with fixed Huffman codes, a full Deflate **decoder** for all three block types, `savePNGCompressed` and `loadPNGFull`), small PNG files — the flag becomes **107 times** smaller than its BMP — and a reader that opens PNG files made by other programs

---

## What you will learn

- **LZ77**: "copy the bytes from back there" — and why it breaks Huffman's 1-bit floor.
- Why a copy may **overlap** itself, and how that turns into a run.
- How to find copies quickly with a **hash** and **chains**.
- Deflate's one alphabet for bytes, lengths and "end of block", with **extra bits**.
- The **fixed Huffman codes** of block type 1, worked bit by bit.
- How to read **dynamic** blocks (type 2) — the kind other programs write.
- The real sizes of our PNG files, and how to open other programs' PNGs.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **LZ77** | A method that replaces repeated bytes by "copy L bytes from D bytes back". |
| **literal** | A byte written as itself. |
| **match** | A copy: a length and a distance. |
| **window** | How far back a copy may reach: 32,768 bytes in Deflate. |
| **hash** | A small number computed from some bytes, used to find equal bytes quickly. |
| **chain** | A list of earlier positions that had the same hash. |
| **extra bits** | Plain bits after a code that pick one value out of a range. |
| **fixed codes** | Huffman codes written in the standard itself, so they need not be stored. |
| **dynamic codes** | Huffman codes made for one block and stored at its start. |
| **inflate** | Decompress Deflate data (the opposite of "deflate"). |

---

## 45.1 Beyond the 1-bit floor

Chapter 44 ended with a problem. The filtered sky is almost all zeros, but Huffman coding needs at least **1 bit per byte**, so 180,200 bytes never get below 22,525 bytes. Think about a row of 900 zeros. Writing "0" 900 times is silly. We would rather say: "**900 more of the same**".

In 1977, Abraham Lempel and Jacob Ziv published a method that does this. It is called **LZ77** after them.

📖 **New words: literal and match** — LZ77 turns the data into a list of two kinds of items:

> a **literal**: one byte, written as itself
> a **match**: "copy **length** bytes, starting **distance** bytes back"

🔢 **Maths: ABRACADABRA ABRACADABRA** (the program prints this)

```
"ABRACADABRA ABRACADABRA": 'A' 'B' 'R' 'A' 'C' 'A' 'D' (4, 7) ' ' (11, 12)
```

> 'A' 'B' 'R' 'A' 'C' 'A' 'D' — seven literals: nothing like them came before
> (4, 7): copy **4** bytes from **7** back. Position 7 − 7 = 0: "ABRA" ✓
> ' ' — a literal space
> (11, 12): copy **11** bytes from **12** back: the whole first word, "ABRACADABRA" ✓

23 bytes become 10 items. The decoder rebuilds the text by doing the copies.

📖 **New word: window** — a match may reach back at most **32,768** bytes in Deflate, and copy **3 to 258** bytes. The last 32,768 bytes are the **window**: the part of the past that the decoder must keep.

💡 Why at least 3? A match costs about as many bits as two literals (Section 45.4). Copying 1 or 2 bytes would not save anything.

---

## 45.2 Copies that overlap

Here is the surprise:

```
"AAAAAAAAAA": 'A' (9, 1)
```

"Copy 9 bytes from 1 back" — but only **1** byte exists so far! It works because the decoder copies **one byte at a time**, and each copied byte is available for the next step:

```
   output: A                 copy from 1 back: A → AA
   output: AA                again:            A → AAA
   ...                       9 times →         AAAAAAAAAA
```

🧠 **Remember:** when the distance is smaller than the length, the copy **overlaps** the bytes it is making. Then a match is a **repeat**: distance 1 repeats one byte, distance 3 repeats one RGB pixel, distance 901 repeats the row above (in our 300-pixel PNG rows).

Another example:

```
"blah blah blah blah!": 'b' 'l' 'a' 'h' ' ' (14, 5) '!'
```

The match (14, 5) copies "blah " and keeps going over its own output for 14 bytes.

🔢 **Maths: the filtered sky** (Chapter 43, "Best" filters)

> row 0, 901 bytes: the filter byte 1, the literals 40 90 200 and 0, then **(258, 1)** (258, 1) (258, 1) (122, 1) — **9 items**
> row 100: **(258, 16218)** — the start of a row 18 rows earlier that was exactly the same — then (258, 1) (258, 1) (127, 1) — **4 items**
> all 200 rows, 180,200 bytes: only **825 items**

No more 1-bit floor: a 258-byte match costs only 13 bits with distance 1 (symbol 285 has 8 bits and no extra bits; distance code 0 has 5), and 25 bits with distance 16,218.

---

## 45.3 Finding matches

For each position i, we want the **longest** earlier place where the same bytes start. Trying every earlier position would be far too slow: 180,000 positions × 32,768 tries. We need a quick way to find **candidates**.

📖 **New word: hash** — a small number computed from some bytes. Equal bytes always give the same hash. We hash the **next 3 bytes** (a match is at least 3 bytes long):

> hash3 = ((byte₀ × 1024) XOR (byte₁ × 32) XOR byte₂) AND 32,767

`<< 10` is × 1024 and `<< 5` is × 32 (Chapter 4). XOR mixes the bits, and AND 32,767 keeps the result between 0 and 32,767. Different bytes can share a hash too — then the comparison just finds a short match, and we move on.

📖 **New word: chain** — for every hash value, we remember the **most recent** position with that hash (`head`), and for every position, the position **before** it with the same hash (`previous`). Following `previous` walks back through all earlier positions with the same hash, newest first:

```
   head[h] → 950 → previous[950] = 49 → previous[49] = 7 → previous[7] = −1 (the end)
```

At each position, our `findMatches`:

> 1. Walks the chain of hash3(i), at most **64** steps (`maxTries`), and only while the distance is ≤ 32,768.
> 2. Compares the bytes at each candidate with the bytes at i, and keeps the **longest** match (the first one wins a tie, so the **nearest**).
> 3. Stops early if a match is as long as possible (258, or the rest of the data).
> 4. If the best match has at least 3 bytes, writes it; otherwise writes a literal.
> 5. Adds **every** position it passed over to the chains, so later positions can match them.

This is called **greedy** matching: take the best match **now**, without looking ahead. Real compressors sometimes wait one byte to see whether a better match starts there ("lazy matching"). Greedy is simpler and good enough for us.

⚠️ The comparison `data[candidate + length] == data[i + length]` may run past position i into the bytes being matched — that is exactly the overlap of Section 45.2, and it is correct: the decoder will have made those bytes by then.

---

## 45.4 One alphabet for everything

Now we must turn literals and matches into bits. Deflate uses **two** Huffman alphabets.

**1. The literal/length alphabet (0–285):**

| symbols | meaning |
|---|---|
| 0–255 | a **literal** byte |
| 256 | **end of block** |
| 257–285 | a match **length** (3–258) |

There are 256 possible lengths but only 29 length symbols. So each symbol stands for a **range**, and some plain **extra bits** after it say which length in that range:

📖 **New word: extra bits** — plain bits (written lowest bit first, with `putBits`) after a code, to choose one value from its range.

| symbol | extra bits | lengths | | symbol | extra bits | lengths |
|---|---|---|---|---|---|---|
| 257–264 | 0 | 3–10 | | 277–280 | 4 | 67–130 |
| 265–268 | 1 | 11–18 | | 281–284 | 5 | 131–257 |
| 269–272 | 2 | 19–34 | | 285 | 0 | 258 |
| 273–276 | 3 | 35–66 | | | | |

**2. The distance alphabet (0–29)**, also with extra bits (0 to 13):

| codes | extra bits | distances |
|---|---|---|
| 0–3 | 0 | 1–4 |
| 4–5 | 1 | 5–8 |
| 6–7 | 2 | 9–16 |
| … | … | … (each pair doubles the range) |
| 28–29 | 13 | 16,385–32,768 |

The exact start of every range is in the tables `kLengthBase` and `kDistanceBase` in our header (copied from the Deflate standard, RFC 1951).

🔢 **Maths: length 11, distance 12** (the program prints this)

> length 11: the largest base ≤ 11 is **11**, at index 8 → symbol 257 + 8 = **265**, 1 extra bit with value 11 − 11 = **0**
> distance 12: the largest base ≤ 12 is **9**, at index 6 → distance code **6**, 2 extra bits with value 12 − 9 = **3**

```
length 11 = symbol 265 + 1 extra bit (0); distance 12 = distance code 6 + 2 extra bits (3)
```

A match is always written as: **length symbol, its extra bits, distance code, its extra bits**. The decoder knows that a distance follows every length, so the distance codes can use their own alphabet.

⚠️ Length 258 has its own symbol, 285, with no extra bits. Symbol 284 with 5 extra bits could also say 258 (227 + 31), but the standard forbids it. Our `lengthIndex` searches from the **top**, so 258 always finds 285.

---

## 45.5 Fixed Huffman codes

📖 **New words: fixed codes and dynamic codes** — a Deflate block can use Huffman codes written in the **standard itself** (block type 1, **fixed**), or codes made for this block and stored at its start (block type 2, **dynamic**).

The fixed codes are given by their **lengths**. With Chapter 44's `canonicalCodes`, the lengths are all we need:

| symbols | code length |
|---|---|
| 0–143 | 8 bits |
| 144–255 | 9 bits |
| 256–279 | 7 bits |
| 280–287 | 8 bits |
| distance codes 0–29 | 5 bits each |

(286 and 287 have codes but are never used. Distance codes 30 and 31 exist in the standard's fixed code but are never used either; we leave them out.)

The program prints some of the codes:

```
fixed code of symbol 0: 00110000
fixed code of symbol 65: 01110001
fixed code of symbol 143: 10111111
fixed code of symbol 144: 110010000
fixed code of symbol 255: 111111111
fixed code of symbol 256: 0000000
fixed code of symbol 257: 0000001
fixed code of symbol 280: 11000000
```

🔢 **Maths: check one canonical code**

> countOfLength: 7 → 24 (256–279), 8 → 152 (0–143 and 280–287), 9 → 112 (144–255)
> nextCode[7] = 0 → symbol 256 = **0000000**, 257 = 0000001, …
> nextCode[8] = (0 + 24) × 2 = 48 = **00110000** → symbol 0 ✓, and symbol 65 = 48 + 65 = 113 = **01110001** ✓
> nextCode[9] = (48 + 152) × 2 = 400 = **110010000** → symbol 144 ✓

Why these lengths? Bytes 0–143 include all ordinary text characters, which come up more often. The common short lengths (257–279) get 7 bits. It is a reasonable guess for "typical" data — and no code table needs to be stored, so even tiny blocks can be compressed.

---

## 45.6 A whole block, bit by bit

A block starts with a 3-bit header, written as numbers (lowest bit first):

> **BFINAL** (1 bit): 1 = this is the last block
> **BTYPE** (2 bits): 0 = stored (Chapter 41), 1 = fixed codes, 2 = dynamic codes, 3 = not allowed

Then the codes of all items, and finally the code for **256** (end of block).

🔢 **Maths: the size of ABRACADABRA ABRACADABRA**

> header: 3 bits
> 7 literals (all < 144): 7 × 8 = 56
> (4, 7): length 4 = symbol 258 (7 bits, 0 extra); distance 7 = code 5 (5 bits, 1 extra bit) → 13
> ' ': 8
> (11, 12): symbol 265 (7 bits + 1 extra) + code 6 (5 bits + 2 extra) → 15
> end of block, symbol 256: 7
> total: 3 + 56 + 13 + 8 + 15 + 7 = **102 bits** → 13 bytes

With the zlib header (2 bytes) and the Adler-32 (4 bytes): **19 bytes**, instead of 34 with a stored block:

```
zlib: 78 01 73 74 0A 72 74 76 74 01 51 0A 48 6C 00 48 55 06 09
19 bytes instead of 34 (stored); read back: ABRACADABRA ABRACADABRA
```

🔢 **Maths: the first data byte, 0x73**

> bit 0: BFINAL = **1**
> bits 1–2: BTYPE = 1, lowest bit first → bit 1 = **1**, bit 2 = **0**
> bits 3–7: the first 5 bits of 'A' = `01110001`, top bit first → 0, 1, 1, 1, 0
> byte: 1 + 2 + 16 + 32 + 64 = 115 = **0x73** ✓

(The last 3 bits of 'A', `001`, start the next byte.)

Python's `zlib.decompress` — the standard zlib library — accepts every stream our encoder makes. We checked that for all the data in this chapter.

---

## 45.7 `zlibCompress`: never worse than stored

Fixed codes give bytes 144–255 **9 bits**. For data that does not repeat (like real random bytes), a Deflate block can come out **bigger** than the data. So `zlibCompress` makes both versions and keeps the smaller:

> 1. `zlibStore` (Chapter 41): the stored version.
> 2. `deflateFixed`: one fixed-code block for all the data (a compressed block may be any length).
> 3. If the compressed version (+ 2 header bytes + 4 Adler bytes) is not smaller, return the stored one.

The zlib header stays **78 01**. Chapter 41 called bits 6–7 of the second byte the "compression level hint" (its official name is FLEVEL): it says how hard the compressor tried. In 01 they are 0, "fastest"; in DA they are 3, "maximum". It is only a **hint** for people; decoders ignore it. Any of 78 01, 78 5E, 78 9C, 78 DA works.

---

## 45.8 Reading Deflate data

📖 **New word: inflate** — to decompress Deflate data. Our `zlibDecompress` replaces Chapter 41's `zlibUnstore`: it reads the same zlib header and Adler-32, but every block type in between.

```
   check the zlib header (as in Chapter 41)
   repeat:
       BFINAL = 1 bit, BTYPE = 2 bits
       type 0: skip to the next byte boundary; LEN, NLEN, copy LEN bytes   (Chapter 41)
       type 1: decode symbols with the fixed codes until 256
       type 2: read the code tables (Section 45.9), then decode until 256
       type 3: error
   until BFINAL was 1
   skip to the next byte boundary; check the Adler-32
```

⚠️ Stored blocks now sit **inside the bit stream**. After the 3 header bits, the rest of that byte is skipped, and LEN starts at the next whole byte. In Chapter 41 this was invisible: the header byte 01 had its 5 unused bits already 0.

Decoding a compressed block:

> 1. Decode a symbol with the literal/length tree (Chapter 44's `decodeSymbol`).
> 2. Below 256: a literal — append it.
> 3. 256: the block ends.
> 4. 257–285: read the extra bits → the **length**; decode a distance code, read its extra bits → the **distance**; copy **one byte at a time** (Section 45.2).

Checks: unknown symbols (286, 287), a distance further back than the bytes made so far, data that ends in the middle, and a size limit of a billion bytes (a tiny file can claim to unpack into a huge one — a "zip bomb").

---

## 45.9 Dynamic blocks: codes made for the data

Most PNG files from other programs use **block type 2**: Huffman codes built (by Chapter 44's method) for this block's data. The decoder needs those codes, so the block starts with them. Of course, only the **code lengths** are stored (Chapter 44, Section 44.7) — and even they are compressed.

The block header:

| field | bits | meaning |
|---|---|---|
| HLIT | 5 | number of literal/length code lengths − 257 (257–286) |
| HDIST | 5 | number of distance code lengths − 1 (1–30) |
| HCLEN | 4 | number of "code length code" lengths − 4 (4–19) |
| | 3 each | the lengths of the **code length codes**, in a strange order |
| | Huffman | the literal/length and distance code lengths, coded with the code length codes |

Yes: the code lengths are themselves Huffman-coded, with a third, small alphabet of 19 symbols:

| symbol | meaning |
|---|---|
| 0–15 | this code length |
| 16 | repeat the **previous** length 3–6 times (2 extra bits) |
| 17 | repeat **0** 3–10 times (3 extra bits) |
| 18 | repeat **0** 11–138 times (7 extra bits) |

That answers Chapter 44's Practice 7: long runs of unused symbols (length 0) cost only a few bits with symbol 18.

The lengths of these 19 symbols come in this order:

```
   16 17 18 0 8 7 9 6 10 5 11 4 12 3 13 2 14 1 15
```

The rare lengths (like 15 or 1) are at the end. Since HCLEN may stop early, they can be left out when they are not used (and then count as 0).

🔢 **Maths: reading a header** (the PNG of Section 45.12)

```
  zlib header 78 DA, last block 1, block type 2, 258 literal/length codes, 12 distance codes, 18 code length codes
```

> HLIT = 1 → 257 + 1 = **258** literal/length lengths (bytes, 256, and one length symbol, 257)
> HDIST = 11 → **12** distance lengths
> HCLEN = 14 → **18** code length lengths: all of the order except the last one (15)
> then: 18 × 3 bits, build a small tree, and decode 258 + 12 = 270 lengths with it

Our `readDynamicTrees` does exactly this, with checks (a repeat with nothing before it, too many lengths, no code for 256, lengths that do not fit), and then builds the two trees with `buildDecoder`.

---

## 45.10 Why we do not write dynamic blocks

We **read** dynamic blocks, but we only **write** fixed ones. A dynamic encoder needs more: Deflate allows code lengths of at most **15** bits (Chapter 44 promised to explain how compressors keep within that).

Huffman's algorithm can make longer codes when some symbols are very rare. Real compressors fix this in one of two ways:

- **Package-merge** — a cleverer algorithm that finds the best code with a length limit directly.
- **Repair** — build the normal tree, then move the too-deep leaves up and push some others down, until all lengths are ≤ 15 (zlib does something like this).

There is a simple trick too: if any length is over 15, make the counts **flatter** (for example, halve every count and add 1) and build the tree again. Rare symbols then get relatively more weight and shallower leaves.

For our pictures, fixed codes already work very well, because LZ77 does most of the work. The program shows it: our 100-byte PNG beats the other program's 174 bytes (Section 45.12). A dynamic encoder would win a few more percent — a project for later.

---

## 45.11 The real sizes

```
file sizes (BMP, PNG of Chapter 42, compressed PNG):
  flag: 180054, 180278, 1683 (107.0 times smaller than BMP), read back the same
  sky: 180054, 180278, 1746 (103.1 times smaller than BMP), read back the same
  sunset: 180054, 180278, 1769 (101.8 times smaller than BMP), read back the same
  blend: 180054, 180278, 3132 (57.5 times smaller than BMP), read back the same
  noise: 180054, 180278, 131616 (1.4 times smaller than BMP), read back the same
  disk (RGBA): Chapter 42 160278, now 3278, alpha read back the same
```

Chapter 37 promised PNG files "often 3 to 10 times smaller for pictures like ours". These simple pictures do **much** better: the flag, the sky and the sunset are about **100 times** smaller. After filtering they are long runs of zeros, and LZ77 turns each run into a few matches.

- **blend**: 57 times smaller. Its filtered rows have small numbers here and there (Chapter 43), and they break up the matches.
- **disk**: 160,278 → 3,278 bytes: the inside and the outside are flat; only the edge needs real bytes.
- **noise**: still 1.4 times smaller. Our noise is **grey**: R = G = B in every pixel, so the same three-byte groups come again and again, and LZ77 copies them. Truly random bytes would not shrink at all — then `zlibCompress` would choose a stored block.

And every file reads back exactly the same: PNG is **lossless**.

💡 Photos compress much less than our pictures: often to a half or a third of the BMP size. They are full of tiny random differences, a bit like our noise.

---

## 45.12 Opening PNG files from other programs

Chapter 43 split the PNG decoder into three steps so that only the middle one had to change. Here it is:

```
   decodePNGFull(file)
      1. readPngStart(file)      → check chunks and IHDR; join the IDAT data   (Chapter 43)
      2. zlibDecompress(zdata)   → the filtered rows, from ANY Deflate data     (new)
      3. pngPixels(info, rows)   → check the size, unfilter, copy the pixels    (Chapter 43)
```

The program has a 174-byte PNG built into it (the list `kOtherPng`). It was made by a different program: a short Python script using the **zlib** library (the same library that most PNG programs, like libpng, use), at its highest level. It is an 8 × 8 picture: red grows to the right, green grows downwards, and blue is a checkerboard of 128 and 200.

```
a PNG made by another program (174 bytes):
  Chapter 42's decodePNG: IDAT: compressed blocks are not supported yet
  zlib header 78 DA, last block 1, block type 2, 258 literal/length codes, 12 distance codes, 18 code length codes
  decodePNGFull: accepted, 8 x 8 pixels
  pixel (0, 0) = 0 0 128, pixel (7, 7) = 255 255 128
  our savePNGCompressed makes it 100 bytes
```

Chapter 42's decoder refuses it; the new one opens it. The pixels are right: (0, 0) has red 0, green 0 and blue 128 (a checkerboard square with x + y even); (7, 7) has red 255 and green 255.

Why is our file **smaller**? That program wrote all rows with filter **None**. Our encoder uses the best filter for each row, which turns the gradients into zeros. Filters matter as much as the compressor.

Now try your own files: `loadPNGFull("screenshot.png", picture)`. It works for any PNG that is **8-bit RGB or RGBA** and not interlaced. It still refuses grey, palette, 16-bit and interlaced PNGs (with a clear message). Chapter 42's table said those are a Practice idea — and the hard part, Deflate, is now done.

🧠 **From now on**, the book saves PNG files with `savePNGCompressed` and reads them with `loadPNGFull`.

---

## Code, part 1: `deflate.h`

File: `common/deflate.h` (new). It includes `huffman.h` (bits and Huffman codes, Chapter 44), which brings in everything from Chapters 36–43.

```cpp
#ifndef DEFLATE_H
#define DEFLATE_H

#include <algorithm>
#include <array>
#include <cstdint>
#include <string>
#include <vector>
#include "huffman.h"

const int kMinMatch = 3;
const int kMaxMatch = 258;
const int kWindowSize = 32768;
const int kEndOfBlock = 256;
const int kMaxInflated = 1000000000;

const std::array<int, 29> kLengthBase = {3,  4,  5,  6,  7,  8,  9,  10, 11, 13,  15,  17,  19,  23, 27,
                                         31, 35, 43, 51, 59, 67, 83, 99, 115, 131, 163, 195, 227, 258};
const std::array<int, 29> kLengthExtra = {0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2,
                                          2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 0};
const std::array<int, 30> kDistanceBase = {1, 2, 3, 4, 5, 7, 9, 13, 17, 25,
                                           33, 49, 65, 97, 129, 193, 257, 385, 513, 769,
                                           1025, 1537, 2049, 3073, 4097,
                                           6145, 8193, 12289, 16385, 24577};
const std::array<int, 30> kDistanceExtra = {0, 0, 0, 0, 1, 1, 2, 2,  3,  3,  4,  4,  5,  5,  6,
                                            6, 7, 7, 8, 8, 9, 9, 10, 10, 11, 11, 12, 12, 13, 13};
const std::array<int, 19> kCodeLengthOrder = {16, 17, 18, 0, 8, 7, 9, 6, 10, 5,
                                              11, 4,  12, 3, 13, 2, 14, 1, 15};

struct Lz77Token {
    int literal = 0;
    int length = 0;
    int distance = 0;
};

inline int hash3(const Bytes& data, int i) {
    return ((data[i] << 10) ^ (data[i + 1] << 5) ^ data[i + 2]) & (kWindowSize - 1);
}

inline std::vector<Lz77Token> findMatches(const Bytes& data, int maxTries) {
    std::vector<Lz77Token> tokens;
    const int n = static_cast<int>(data.size());
    std::vector<int> head(kWindowSize, -1);
    std::vector<int> previous(n, -1);
    int i = 0;
    while (i < n) {
        int bestLength = 0;
        int bestDistance = 0;
        if (i + kMinMatch <= n) {
            const int maxLength = std::min(kMaxMatch, n - i);
            int candidate = head[hash3(data, i)];
            int tries = 0;
            while (candidate >= 0 && i - candidate <= kWindowSize && tries < maxTries) {
                int length = 0;
                while (length < maxLength && data[candidate + length] == data[i + length]) {
                    ++length;
                }
                if (length > bestLength) {
                    bestLength = length;
                    bestDistance = i - candidate;
                }
                if (bestLength == maxLength) {
                    break;
                }
                candidate = previous[candidate];
                ++tries;
            }
        }
        int step = 1;
        if (bestLength >= kMinMatch) {
            tokens.push_back(Lz77Token{0, bestLength, bestDistance});
            step = bestLength;
        } else {
            tokens.push_back(Lz77Token{data[i], 0, 0});
        }
        for (int k = i; k < i + step; ++k) {
            if (k + kMinMatch <= n) {
                const int h = hash3(data, k);
                previous[k] = head[h];
                head[h] = k;
            }
        }
        i += step;
    }
    return tokens;
}

inline int lengthIndex(int length) {
    int k = 28;
    while (kLengthBase[k] > length) {
        --k;
    }
    return k;
}

inline int distanceIndex(int distance) {
    int k = 29;
    while (kDistanceBase[k] > distance) {
        --k;
    }
    return k;
}

inline std::vector<int> fixedLiteralLengths() {
    std::vector<int> lengths(288, 8);
    for (int s = 144; s < 256; ++s) {
        lengths[s] = 9;
    }
    for (int s = 256; s < 280; ++s) {
        lengths[s] = 7;
    }
    return lengths;
}

inline std::vector<int> fixedDistanceLengths() {
    return std::vector<int>(30, 5);
}

inline void writeFixedBlock(BitWriter& w, const std::vector<Lz77Token>& tokens, bool last) {
    const std::vector<int> litLengths = fixedLiteralLengths();
    const std::vector<int> litCodes = canonicalCodes(litLengths);
    const std::vector<int> distCodes = canonicalCodes(fixedDistanceLengths());
    putBits(w, last ? 1 : 0, 1);
    putBits(w, 1, 2);
    for (const Lz77Token& t : tokens) {
        if (t.length == 0) {
            putCode(w, litCodes[t.literal], litLengths[t.literal]);
            continue;
        }
        const int k = lengthIndex(t.length);
        putCode(w, litCodes[257 + k], litLengths[257 + k]);
        putBits(w, t.length - kLengthBase[k], kLengthExtra[k]);
        const int d = distanceIndex(t.distance);
        putCode(w, distCodes[d], 5);
        putBits(w, t.distance - kDistanceBase[d], kDistanceExtra[d]);
    }
    putCode(w, litCodes[kEndOfBlock], litLengths[kEndOfBlock]);
}

inline Bytes deflateFixed(const Bytes& data) {
    BitWriter w;
    writeFixedBlock(w, findMatches(data, 64), true);
    return w.bytes;
}

inline Bytes zlibCompress(const Bytes& data) {
    const Bytes stored = zlibStore(data);
    const Bytes packed = deflateFixed(data);
    if (packed.size() + 6 >= stored.size()) {
        return stored;
    }
    Bytes z = {0x78, 0x01};
    z.insert(z.end(), packed.begin(), packed.end());
    putU32BE(z, adler32(data, 0, static_cast<int>(data.size())));
    return z;
}

inline std::string inflateCodes(BitReader& r, const std::vector<DecodeNode>& litTree,
                                const std::vector<DecodeNode>& distTree, Bytes& out) {
    while (true) {
        const int s = decodeSymbol(r, litTree);
        if (s < 0) {
            return "a bad literal or length code";
        }
        if (s < 256) {
            out.push_back(static_cast<std::uint8_t>(s));
            if (static_cast<long long>(out.size()) > kMaxInflated) {
                return "too much data";
            }
            continue;
        }
        if (s == kEndOfBlock) {
            return "";
        }
        if (s - 257 >= 29) {
            return "a bad length code";
        }
        const int k = s - 257;
        const int extra = getBits(r, kLengthExtra[k]);
        if (extra < 0) {
            return "the data ends inside a match";
        }
        const int d = decodeSymbol(r, distTree);
        if (d < 0) {
            return "a bad distance code";
        }
        const int dextra = getBits(r, kDistanceExtra[d]);
        if (dextra < 0) {
            return "the data ends inside a match";
        }
        const int length = kLengthBase[k] + extra;
        const int distance = kDistanceBase[d] + dextra;
        if (distance > static_cast<int>(out.size())) {
            return "a match reaches back before the start";
        }
        if (static_cast<long long>(out.size()) + length > kMaxInflated) {
            return "too much data";
        }
        const int from = static_cast<int>(out.size()) - distance;
        for (int i = 0; i < length; ++i) {
            const std::uint8_t b = out[from + i];
            out.push_back(b);
        }
    }
}

inline std::string readDynamicTrees(BitReader& r, std::vector<DecodeNode>& litTree,
                                    std::vector<DecodeNode>& distTree) {
    const int hlit = getBits(r, 5);
    const int hdist = getBits(r, 5);
    const int hclen = getBits(r, 4);
    if (hlit < 0 || hdist < 0 || hclen < 0) {
        return "the data ends inside a block header";
    }
    const int literalCount = hlit + 257;
    const int distanceCount = hdist + 1;
    if (literalCount > 286 || distanceCount > 30) {
        return "too many codes in a block header";
    }
    std::vector<int> lengthLengths(19, 0);
    for (int i = 0; i < hclen + 4; ++i) {
        const int v = getBits(r, 3);
        if (v < 0) {
            return "the data ends inside a block header";
        }
        lengthLengths[kCodeLengthOrder[i]] = v;
    }
    std::vector<DecodeNode> lengthTree;
    std::string problem = buildDecoder(lengthLengths, lengthTree);
    if (!problem.empty()) {
        return "code length codes: " + problem;
    }
    std::vector<int> lengths;
    const int total = literalCount + distanceCount;
    while (static_cast<int>(lengths.size()) < total) {
        const int s = decodeSymbol(r, lengthTree);
        if (s < 0) {
            return "a bad code length code";
        }
        if (s < 16) {
            lengths.push_back(s);
            continue;
        }
        int value = 0;
        int extraBits = 7;
        int base = 11;
        if (s == 16) {
            if (lengths.empty()) {
                return "a repeat with nothing to repeat";
            }
            value = lengths.back();
            extraBits = 2;
            base = 3;
        } else if (s == 17) {
            extraBits = 3;
            base = 3;
        }
        const int extra = getBits(r, extraBits);
        if (extra < 0) {
            return "the data ends inside a block header";
        }
        const int repeat = base + extra;
        if (static_cast<int>(lengths.size()) + repeat > total) {
            return "a bad repeat of code lengths";
        }
        lengths.insert(lengths.end(), repeat, value);
    }
    if (lengths[kEndOfBlock] == 0) {
        return "there is no end-of-block code";
    }
    const std::vector<int> litLengths(lengths.begin(), lengths.begin() + literalCount);
    const std::vector<int> distLengths(lengths.begin() + literalCount, lengths.end());
    problem = buildDecoder(litLengths, litTree);
    if (problem.empty()) {
        problem = buildDecoder(distLengths, distTree);
    }
    return problem;
}

inline std::string zlibDecompress(const Bytes& z, Bytes& out) {
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
    std::vector<DecodeNode> fixedLit;
    std::vector<DecodeNode> fixedDist;
    buildDecoder(fixedLiteralLengths(), fixedLit);
    buildDecoder(fixedDistanceLengths(), fixedDist);
    BitReader r{&z, 16};
    bool last = false;
    while (!last) {
        const int lastBit = getBit(r);
        const int type = getBits(r, 2);
        if (lastBit < 0 || type < 0) {
            return "the data ends before the last block";
        }
        last = (lastBit == 1);
        std::string problem;
        if (type == 0) {
            r.bit = (r.bit + 7) / 8 * 8;
            const int pos = static_cast<int>(r.bit / 8);
            if (!hasBytes(z, pos, 4)) {
                return "a block header is cut off";
            }
            const int length = getU16(z, pos);
            if (getU16(z, pos + 2) != (~length & 0xFFFF)) {
                return "LEN and NLEN do not match";
            }
            if (!hasBytes(z, pos + 4, length)) {
                return "a block is longer than the data";
            }
            out.insert(out.end(), z.begin() + pos + 4, z.begin() + pos + 4 + length);
            r.bit += 8LL * (4 + length);
        } else if (type == 1) {
            problem = inflateCodes(r, fixedLit, fixedDist, out);
        } else if (type == 2) {
            std::vector<DecodeNode> litTree;
            std::vector<DecodeNode> distTree;
            problem = readDynamicTrees(r, litTree, distTree);
            if (problem.empty()) {
                problem = inflateCodes(r, litTree, distTree, out);
            }
        } else {
            return "block type 3 does not exist";
        }
        if (!problem.empty()) {
            return problem;
        }
    }
    const int pos = static_cast<int>((r.bit + 7) / 8);
    if (!hasBytes(z, pos, 4)) {
        return "the Adler-32 is missing";
    }
    if (getU32BE(z, pos) != adler32(out, 0, static_cast<int>(out.size()))) {
        return "the Adler-32 is wrong";
    }
    return "";
}

inline Bytes makePngBytesCompressed(const Image& image,
                                    const std::vector<std::uint8_t>* alpha = nullptr) {
    Bytes file;
    const int width = image.width();
    const int height = image.height();
    if (width <= 0 || height <= 0) {
        return file;
    }
    if (alpha != nullptr && static_cast<int>(alpha->size()) != width * height) {
        alpha = nullptr;
    }
    const int bpp = (alpha != nullptr) ? 4 : 3;
    if ((1LL + bpp * static_cast<long long>(width)) * height > 100000000LL) {
        return file;
    }
    const Bytes rows = filterScanlines(makePngRows(image, alpha), bpp * width, bpp, kFilterBest);
    appendPngSignature(file);
    appendChunk(file, "IHDR", makeIhdr(width, height, alpha != nullptr));
    appendChunk(file, "IDAT", zlibCompress(rows));
    appendChunk(file, "IEND", Bytes{});
    return file;
}

inline bool savePNGCompressed(const Image& image, const std::string& fileName,
                              const std::vector<std::uint8_t>* alpha = nullptr) {
    Bytes file = makePngBytesCompressed(image, alpha);
    if (file.empty()) {
        return false;
    }
    return writeBytes(fileName, file);
}

inline std::string decodePNGFull(const Bytes& file, Image& image,
                                 std::vector<std::uint8_t>* alpha = nullptr) {
    PngInfo info;
    Bytes zdata;
    std::string problem = readPngStart(file, info, zdata);
    if (!problem.empty()) {
        return problem;
    }
    Bytes rows;
    problem = zlibDecompress(zdata, rows);
    if (!problem.empty()) {
        return "IDAT: " + problem;
    }
    return pngPixels(info, rows, image, alpha);
}

inline bool loadPNGFull(const std::string& fileName, Image& image,
                        std::vector<std::uint8_t>* alpha = nullptr) {
    Bytes file;
    if (!readFileBytes(fileName, file)) {
        return false;
    }
    return decodePNGFull(file, image, alpha).empty();
}

#endif
```

### Line by line

**Constants and tables (lines 1–34)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–9 | include guard and `#include` lines | `std::min`, `std::array`, exact-size integers, strings, lists, and Chapter 44's header. |
| 11–14 | `const int kMinMatch = 3; const int kMaxMatch = 258; const int kWindowSize = 32768; const int kEndOfBlock = 256;` | The limits of Section 45.1, and the end-of-block symbol. |
| 15 | `const int kMaxInflated = 1000000000;` | The decoder never makes more than a billion bytes (Section 45.8). |
| 17–20 | `kLengthBase` and `kLengthExtra` | For length symbols 257–285 (index 0–28): the first length of each range, and its number of extra bits (Section 45.4). |
| 21–26 | `kDistanceBase` and `kDistanceExtra` | The same for distance codes 0–29. |
| 27–28 | `const std::array<int, 19> kCodeLengthOrder = {16, 17, 18, 0, 8, ...};` | The order of the code length code lengths in a dynamic header (Section 45.9). |
| 30–34 | `struct Lz77Token { int literal = 0; int length = 0; int distance = 0; };` | One LZ77 item. `length == 0` means a literal (the byte is in `literal`); otherwise a match. |

**Finding matches (lines 36–86)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 36–38 | `inline int hash3(const Bytes& data, int i) { return ((data[i] << 10) ^ (data[i + 1] << 5) ^ data[i + 2]) & (kWindowSize - 1); }` | The hash of the 3 bytes at i (Section 45.3). `kWindowSize - 1` = 32,767: the AND keeps 15 bits. |
| 40–45 | `inline std::vector<Lz77Token> findMatches(const Bytes& data, int maxTries) { ... std::vector<int> head(kWindowSize, -1); std::vector<int> previous(n, -1); int i = 0;` | `head[h]`: the newest position with hash h. `previous[p]`: the next older one. −1 = none. |
| 46–48 | `while (i < n) { int bestLength = 0; int bestDistance = 0;` | One item per pass. |
| 49–52 | `if (i + kMinMatch <= n) { const int maxLength = std::min(kMaxMatch, n - i); int candidate = head[hash3(data, i)]; int tries = 0;` | Only search if 3 bytes are left. A match may not run past the end of the data. |
| 53 | `while (candidate >= 0 && i - candidate <= kWindowSize && tries < maxTries) {` | Walk the chain: stop at its end, when the distance gets too big, or after `maxTries` steps. |
| 54–57 | `int length = 0; while (length < maxLength && data[candidate + length] == data[i + length]) { ++length; }` | Count how many bytes match. It may run into the overlap (Section 45.3, ⚠️). |
| 58–61 | `if (length > bestLength) { bestLength = length; bestDistance = i - candidate; }` | Keep the longest; on a tie the earlier (nearer) candidate stays. |
| 62–64 | `if (bestLength == maxLength) { break; }` | Nothing can be longer: stop searching. |
| 65–68 | `candidate = previous[candidate]; ++tries; }` `}` | The next older candidate. |
| 69–75 | `int step = 1; if (bestLength >= kMinMatch) { tokens.push_back(Lz77Token{0, bestLength, bestDistance}); step = bestLength; } else { tokens.push_back(Lz77Token{data[i], 0, 0}); }` | A match of 3 or more bytes, or a literal. `step` is how many bytes this item covers. |
| 76–82 | `for (int k = i; k < i + step; ++k) { if (k + kMinMatch <= n) { const int h = hash3(data, k); previous[k] = head[h]; head[h] = k; } }` | Add every covered position to its chain: it becomes the newest, and the old newest becomes its `previous`. |
| 83–86 | `i += step;` `}` `return tokens;` `}` | Move on. |

**Lengths and distances to symbols (lines 88–102)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 88–94 | `inline int lengthIndex(int length) { int k = 28; while (kLengthBase[k] > length) { --k; } return k; }` | The largest base ≤ length, searching from the top (so 258 → index 28 = symbol 285). |
| 96–102 | `inline int distanceIndex(int distance) { ... }` | The same for distances. |

**Fixed codes and the encoder (lines 104–156)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 104–113 | `inline std::vector<int> fixedLiteralLengths() { std::vector<int> lengths(288, 8); for (...144...256...) { lengths[s] = 9; } for (...256...280...) { lengths[s] = 7; } return lengths; }` | The fixed code lengths of Section 45.5: 8 everywhere, then 9 and 7 where needed. |
| 115–117 | `inline std::vector<int> fixedDistanceLengths() { return std::vector<int>(30, 5); }` | 30 distance codes of 5 bits. |
| 119–122 | `inline void writeFixedBlock(BitWriter& w, const std::vector<Lz77Token>& tokens, bool last) { ... litCodes = canonicalCodes(litLengths); ... distCodes = canonicalCodes(fixedDistanceLengths());` | Turn the lengths into codes (Chapter 44). |
| 123–124 | `putBits(w, last ? 1 : 0, 1); putBits(w, 1, 2);` | The block header: BFINAL and BTYPE = 1 (Section 45.6). |
| 125–129 | `for (const Lz77Token& t : tokens) { if (t.length == 0) { putCode(w, litCodes[t.literal], litLengths[t.literal]); continue; }` | A literal: its code, top bit first. |
| 130–132 | `const int k = lengthIndex(t.length); putCode(w, litCodes[257 + k], litLengths[257 + k]); putBits(w, t.length - kLengthBase[k], kLengthExtra[k]);` | A match: the length symbol, then the extra bits (a number: lowest bit first). |
| 133–136 | `const int d = distanceIndex(t.distance); putCode(w, distCodes[d], 5); putBits(w, t.distance - kDistanceBase[d], kDistanceExtra[d]); }` | Then the distance code and its extra bits. |
| 137–138 | `putCode(w, litCodes[kEndOfBlock], litLengths[kEndOfBlock]);` `}` | End of block. |
| 140–144 | `inline Bytes deflateFixed(const Bytes& data) { BitWriter w; writeFixedBlock(w, findMatches(data, 64), true); return w.bytes; }` | All the data in one final block, with up to 64 tries per position. |
| 146–151 | `inline Bytes zlibCompress(const Bytes& data) { const Bytes stored = zlibStore(data); const Bytes packed = deflateFixed(data); if (packed.size() + 6 >= stored.size()) { return stored; }` | Make both versions; keep the stored one unless compression really wins (Section 45.7). |
| 152–156 | `Bytes z = {0x78, 0x01}; z.insert(...packed...); putU32BE(z, adler32(...)); return z;` `}` | zlib header, the Deflate block, and the Adler-32 (big-endian, Chapter 41). |

**Decoding symbols (lines 158–205)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 158–164 | `inline std::string inflateCodes(BitReader& r, const std::vector<DecodeNode>& litTree, const std::vector<DecodeNode>& distTree, Bytes& out) { while (true) { const int s = decodeSymbol(r, litTree); if (s < 0) { return "..."; }` | Decode one compressed block, with whichever trees it uses (fixed or dynamic). |
| 165–171 | `if (s < 256) { out.push_back(...); if (... > kMaxInflated) { return "too much data"; } continue; }` | A literal. |
| 172–177 | `if (s == kEndOfBlock) { return ""; } if (s - 257 >= 29) { return "a bad length code"; }` | The end, or symbols 286–287, which must never appear. |
| 178–182 | `const int k = s - 257; const int extra = getBits(r, kLengthExtra[k]); if (extra < 0) { return "the data ends inside a match"; }` | The length's extra bits (`getBits` of 0 bits gives 0). |
| 183–190 | `const int d = decodeSymbol(r, distTree); if (d < 0) { ... } const int dextra = getBits(r, kDistanceExtra[d]); if (dextra < 0) { ... }` | The distance code and its extra bits. |
| 191–198 | `const int length = kLengthBase[k] + extra; const int distance = kDistanceBase[d] + dextra; if (distance > ...out.size()...) { return "a match reaches back before the start"; } if (... + length > kMaxInflated) { ... }` | The real numbers, and two checks. |
| 199–205 | `const int from = ...out.size()... - distance; for (int i = 0; i < length; ++i) { const std::uint8_t b = out[from + i]; out.push_back(b); } } }` | Copy one byte at a time, so overlapping copies work (Section 45.2). We copy the byte into `b` first, because `push_back` may move the list's memory. |

**Dynamic code tables (lines 207–278)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 207–214 | `inline std::string readDynamicTrees(BitReader& r, std::vector<DecodeNode>& litTree, std::vector<DecodeNode>& distTree) { const int hlit = getBits(r, 5); const int hdist = getBits(r, 5); const int hclen = getBits(r, 4); if (...) { ... }` | The three counts of Section 45.9. |
| 215–219 | `const int literalCount = hlit + 257; const int distanceCount = hdist + 1; if (literalCount > 286 \|\| distanceCount > 30) { ... }` | 5 bits could say up to 288 and 32; more than 286 and 30 is not allowed. |
| 220–227 | `std::vector<int> lengthLengths(19, 0); for (int i = 0; i < hclen + 4; ++i) { const int v = getBits(r, 3); ... lengthLengths[kCodeLengthOrder[i]] = v; }` | Read 3-bit lengths in the special order. The ones not read stay 0. |
| 228–232 | `std::vector<DecodeNode> lengthTree; std::string problem = buildDecoder(lengthLengths, lengthTree); if (...) { return "code length codes: " + problem; }` | Build the small tree for the 19-symbol alphabet. |
| 233–243 | `std::vector<int> lengths; const int total = literalCount + distanceCount; while (...size() < total) { const int s = decodeSymbol(r, lengthTree); ... if (s < 16) { lengths.push_back(s); continue; }` | Both lists of lengths are read as **one** list. Symbols 0–15 are lengths. |
| 244–257 | `int value = 0; int extraBits = 7; int base = 11; if (s == 16) { ... value = lengths.back(); extraBits = 2; base = 3; } else if (s == 17) { extraBits = 3; base = 3; }` | The three repeat symbols: 16 repeats the previous length (3 + 2 bits), 17 repeats 0 (3 + 3 bits), 18 repeats 0 (11 + 7 bits). |
| 258–266 | `const int extra = getBits(r, extraBits); if (extra < 0) { ... } const int repeat = base + extra; if (... + repeat > total) { ... } lengths.insert(lengths.end(), repeat, value);` | How many times, a check, and `insert(end, count, value)` adds `count` copies of `value`. |
| 267–270 | `}` `if (lengths[kEndOfBlock] == 0) { return "there is no end-of-block code"; }` | Without a code for 256, the block could never end. |
| 271–278 | `const std::vector<int> litLengths(lengths.begin(), lengths.begin() + literalCount); const std::vector<int> distLengths(...); problem = buildDecoder(litLengths, litTree); if (problem.empty()) { problem = buildDecoder(distLengths, distTree); } return problem; }` | Split the list in two and build both trees. |

**The zlib decoder (lines 280–349)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 280–295 | `inline std::string zlibDecompress(const Bytes& z, Bytes& out) { ... }` (the header checks) | Exactly the checks of Chapter 41's `zlibUnstore`. |
| 296–299 | `std::vector<DecodeNode> fixedLit; std::vector<DecodeNode> fixedDist; buildDecoder(fixedLiteralLengths(), fixedLit); buildDecoder(fixedDistanceLengths(), fixedDist);` | The fixed trees, ready for type-1 blocks. (These lengths always fit, so we ignore the returned text.) |
| 300–301 | `BitReader r{&z, 16}; bool last = false;` | The bit stream starts after the 2 header bytes: bit 16. |
| 302–309 | `while (!last) { const int lastBit = getBit(r); const int type = getBits(r, 2); if (...) { ... } last = (lastBit == 1); std::string problem;` | Each block's header. |
| 310–312 | `if (type == 0) { r.bit = (r.bit + 7) / 8 * 8; const int pos = static_cast<int>(r.bit / 8);` | A stored block: skip to the next byte boundary (round the bit position up to a multiple of 8). |
| 313–324 | the LEN/NLEN checks, `out.insert(...)`, `r.bit += 8LL * (4 + length);` | As in Chapter 41; then move the bit position past LEN, NLEN and the data. |
| 325–326 | `} else if (type == 1) { problem = inflateCodes(r, fixedLit, fixedDist, out);` | Fixed codes. |
| 327–333 | `} else if (type == 2) { std::vector<DecodeNode> litTree; std::vector<DecodeNode> distTree; problem = readDynamicTrees(r, litTree, distTree); if (problem.empty()) { problem = inflateCodes(r, litTree, distTree, out); }` | Dynamic codes: read the tables, then the same symbol loop. |
| 334–340 | `} else { return "block type 3 does not exist"; } if (!problem.empty()) { return problem; } }` | Type 3, or a problem inside the block. |
| 341–349 | `const int pos = static_cast<int>((r.bit + 7) / 8); if (!hasBytes(z, pos, 4)) { ... } if (getU32BE(z, pos) != adler32(...)) { ... } return "";` `}` | The Adler-32 starts at the next whole byte after the last block. |

**PNG files (lines 351–408)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 351–362 | `inline Bytes makePngBytesCompressed(const Image& image, const std::vector<std::uint8_t>* alpha = nullptr) { ... }` | Like `makePngBytesFiltered` (Chapter 43): size checks, the alpha check, and bpp. |
| 363–365 | `if ((1LL + bpp * static_cast<long long>(width)) * height > 100000000LL) { return file; }` | At most 100 million row bytes: the match finder keeps one `int` per byte. |
| 366 | `const Bytes rows = filterScanlines(makePngRows(image, alpha), bpp * width, bpp, kFilterBest);` | Filtered rows (the best filter for each row). |
| 367–372 | the four `append…` lines, with `zlibCompress(rows)` in the IDAT | The only change from Chapter 43: the compressor. |
| 374–381 | `inline bool savePNGCompressed(...) { ... }` | Build and write. |
| 383–397 | `inline std::string decodePNGFull(const Bytes& file, Image& image, std::vector<std::uint8_t>* alpha = nullptr) { ... problem = zlibDecompress(zdata, rows); ... return pngPixels(info, rows, image, alpha); }` | Chapter 43's `decodePNGFiltered`, with `zlibDecompress` in the middle (Section 45.12). |
| 399–406 | `inline bool loadPNGFull(...) { ... return decodePNGFull(file, image, alpha).empty(); }` | Read a file and decode it. |
| 408 | `#endif` | End of the include guard. |

---

## Code, part 2: real compression

File: `ch45/deflate.cpp`

```cpp
#include <cmath>
#include <iostream>
#include <string>
#include <vector>
#include "deflate.h"
#include "antialias.h"

const Bytes kOtherPng = {
    0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A, 0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,
    0x00, 0x00, 0x00, 0x08, 0x00, 0x00, 0x00, 0x08, 0x08, 0x02, 0x00, 0x00, 0x00, 0x4B, 0x6D, 0x29,
    0xDC, 0x00, 0x00, 0x00, 0x75, 0x49, 0x44, 0x41, 0x54, 0x78, 0xDA, 0x0D, 0xCB, 0x41, 0x01, 0x00,
    0x30, 0x08, 0x02, 0x40, 0xC3, 0x10, 0xC6, 0x32, 0x74, 0xA0, 0x82, 0x65, 0xCC, 0x40, 0x06, 0xCB,
    0xB0, 0xDD, 0xFF, 0xAA, 0x4A, 0x28, 0x77, 0x89, 0xE5, 0x29, 0x6D, 0xF9, 0x4A, 0x29, 0x57, 0xC1,
    0x80, 0x1A, 0x26, 0x34, 0xF0, 0x42, 0x07, 0x07, 0xAA, 0x6A, 0xA1, 0xDD, 0x2D, 0xB6, 0xA7, 0xB5,
    0xED, 0x6B, 0xA5, 0xFF, 0xA0, 0x41, 0x35, 0x4D, 0x6A, 0xE8, 0xA5, 0x8E, 0x0E, 0xFF, 0x18, 0x61,
    0xDC, 0x23, 0x8E, 0x67, 0xB4, 0xE3, 0x1B, 0x65, 0xFE, 0x58, 0x63, 0xD5, 0x6B, 0xAE, 0x66, 0xBD,
    0xAB, 0x5B, 0x67, 0xFF, 0x38, 0xE1, 0xDC, 0x27, 0x9E, 0xE7, 0xB4, 0xE7, 0x3B, 0xE5, 0xFE, 0x88,
    0x11, 0x75, 0xCC, 0x68, 0xE2, 0x8D, 0x2E, 0x4E, 0xF4, 0x00, 0x96, 0xAD, 0x68, 0x91, 0x8A, 0x0D,
    0x4C, 0xBF, 0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E, 0x44, 0xAE, 0x42, 0x60, 0x82};

std::string oneDecimal(double v) {
    const long long tenths = std::llround(v * 10.0);
    return std::to_string(tenths / 10) + "." + std::to_string(tenths % 10);
}

void printTokens(const std::string& text) {
    const Bytes data(text.begin(), text.end());
    std::cout << "\"" << text << "\":";
    for (const Lz77Token& t : findMatches(data, 64)) {
        if (t.length == 0) {
            std::cout << " '" << static_cast<char>(t.literal) << "'";
        } else {
            std::cout << " (" << t.length << ", " << t.distance << ")";
        }
    }
    std::cout << "\n";
}

std::string asBinary(int code, int length) {
    std::string s;
    for (int i = length - 1; i >= 0; --i) {
        s += ((code >> i) & 1) ? '1' : '0';
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
    const std::string problem = zlibDecompress(z, out);
    std::cout << "  " << label << ": "
              << (problem.empty() ? "accepted, " + std::to_string(out.size()) + " bytes"
                                  : "refused (" + problem + ")")
              << "\n";
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
    printTokens("AAAAAAAAAA");
    printTokens("ABRACADABRA ABRACADABRA");
    printTokens("blah blah blah blah!");

    const std::vector<int> litLengths = fixedLiteralLengths();
    const std::vector<int> litCodes = canonicalCodes(litLengths);
    const int symbols[8] = {0, 65, 143, 144, 255, 256, 257, 280};
    for (int s : symbols) {
        std::cout << "fixed code of symbol " << s << ": " << asBinary(litCodes[s], litLengths[s])
                  << "\n";
    }
    const int k = lengthIndex(11);
    const int d = distanceIndex(12);
    std::cout << "length 11 = symbol " << 257 + k << " + " << kLengthExtra[k] << " extra bit ("
              << 11 - kLengthBase[k] << "); distance 12 = distance code " << d << " + "
              << kDistanceExtra[d] << " extra bits (" << 12 - kDistanceBase[d] << ")\n";

    const std::string text = "ABRACADABRA ABRACADABRA";
    const Bytes data(text.begin(), text.end());
    const Bytes z = zlibCompress(data);
    printBytes("zlib:", z);
    Bytes back;
    std::string problem = zlibDecompress(z, back);
    std::cout << z.size() << " bytes instead of " << zlibStore(data).size() << " (stored); read back: "
              << (problem.empty() ? std::string(back.begin(), back.end()) : problem) << "\n";

    Image flag(300, 200);
    Image sky(300, 200);
    Image sunset(300, 200);
    Image blend(300, 200);
    Image noise(300, 200);
    unsigned int seed = 12345;
    for (int y = 0; y < 200; ++y) {
        for (int x = 0; x < 300; ++x) {
            Colour c = colours::white;
            if (x < 100) {
                c = Colour{0, 85, 164};
            } else if (x >= 200) {
                c = Colour{239, 65, 53};
            }
            flag.setPixel(x, y, c);
            sky.setPixel(x, y, lerpColour(Colour{40, 90, 200}, Colour{250, 200, 120}, y / 199.0));
            sunset.setPixel(x, y, lerpColour(Colour{250, 120, 40}, Colour{80, 20, 120}, x / 299.0));
            blend.setPixel(x, y, Colour{static_cast<std::uint8_t>(x * 255 / 299),
                                        static_cast<std::uint8_t>(y * 255 / 199),
                                        static_cast<std::uint8_t>((x + y) * 255 / 498)});
            seed = seed * 1103515245u + 12345u;
            const std::uint8_t v = static_cast<std::uint8_t>(seed >> 24);
            noise.setPixel(x, y, Colour{v, v, v});
        }
    }

    const Image* pictures[5] = {&flag, &sky, &sunset, &blend, &noise};
    const std::string names[5] = {"flag", "sky", "sunset", "blend", "noise"};
    std::cout << "\nfile sizes (BMP, PNG of Chapter 42, compressed PNG):\n";
    for (int i = 0; i < 5; ++i) {
        const int bmp = static_cast<int>(makeBmpBytes(*pictures[i]).size());
        const int png = static_cast<int>(makePngBytesCompressed(*pictures[i]).size());
        const std::string fileName = names[i] + ".png";
        Image loaded(0, 0);
        const bool ok = savePNGCompressed(*pictures[i], fileName) && loadPNGFull(fileName, loaded) &&
                        samePictures(*pictures[i], loaded);
        std::cout << "  " << names[i] << ": " << bmp << ", " << makePngBytes(*pictures[i]).size()
                  << ", " << png << " (" << oneDecimal(static_cast<double>(bmp) / png)
                  << " times smaller than BMP), read back " << (ok ? "the same" : "DIFFERENT") << "\n";
    }

    Image disk(200, 200, Colour{250, 140, 30});
    std::vector<std::uint8_t> diskAlpha(200 * 200);
    for (int y = 0; y < 200; ++y) {
        for (int x = 0; x < 200; ++x) {
            diskAlpha[y * 200 + x] = toByte(circleCoverage(100.0, 100.0, 80.0, x, y, 4));
        }
    }
    Image diskBack(0, 0);
    std::vector<std::uint8_t> alphaBack;
    const bool diskOk = savePNGCompressed(disk, "disk.png", &diskAlpha) &&
                        loadPNGFull("disk.png", diskBack, &alphaBack) && alphaBack == diskAlpha;
    std::cout << "  disk (RGBA): Chapter 42 " << makePngBytes(disk, &diskAlpha).size() << ", now "
              << makePngBytesCompressed(disk, &diskAlpha).size() << ", alpha read back "
              << (diskOk ? "the same" : "DIFFERENT") << "\n";

    std::cout << "\na PNG made by another program (" << kOtherPng.size() << " bytes):\n";
    Image other(0, 0);
    std::cout << "  Chapter 42's decodePNG: " << decodePNG(kOtherPng, other) << "\n";
    PngInfo info;
    Bytes zdata;
    readPngStart(kOtherPng, info, zdata);
    BitReader r{&zdata, 16};
    const int lastBit = getBit(r);
    const int type = getBits(r, 2);
    const int hlit = getBits(r, 5);
    const int hdist = getBits(r, 5);
    const int hclen = getBits(r, 4);
    std::cout << "  zlib header " << hexByte(zdata[0]) << " " << hexByte(zdata[1]) << ", last block "
              << lastBit << ", block type " << type << ", " << hlit + 257 << " literal/length codes, "
              << hdist + 1 << " distance codes, " << hclen + 4 << " code length codes\n";
    problem = decodePNGFull(kOtherPng, other);
    std::cout << "  decodePNGFull: " << (problem.empty() ? "accepted" : problem) << ", "
              << other.width() << " x " << other.height() << " pixels\n";
    const Colour first = other.getPixel(0, 0);
    const Colour last = other.getPixel(7, 7);
    std::cout << "  pixel (0, 0) = " << static_cast<int>(first.r) << " " << static_cast<int>(first.g)
              << " " << static_cast<int>(first.b) << ", pixel (7, 7) = " << static_cast<int>(last.r)
              << " " << static_cast<int>(last.g) << " " << static_cast<int>(last.b) << "\n";
    std::cout << "  our savePNGCompressed makes it " << makePngBytesCompressed(other).size()
              << " bytes\n";

    std::cout << "\nbroken zlib data:\n";
    const Bytes hello = {'h', 'e', 'l', 'l', 'o'};
    const Bytes good = zlibCompress(hello);
    report("the good data", good);
    Bytes wrong = good;
    wrong[2] = static_cast<std::uint8_t>(wrong[2] | 0x06);
    report("block type 3", wrong);
    wrong = good;
    wrong.back() = static_cast<std::uint8_t>(wrong.back() ^ 0x01);
    report("Adler-32 changed", wrong);
    wrong = good;
    wrong.resize(5);
    report("cut after 5 bytes", wrong);
    BitWriter w;
    writeFixedBlock(w, std::vector<Lz77Token>{Lz77Token{0, 5, 3}}, true);
    wrong = Bytes{0x78, 0x01};
    wrong.insert(wrong.end(), w.bytes.begin(), w.bytes.end());
    report("a copy from 3 bytes back at the start", wrong);
    return 0;
}
```

Build and run it from the `code/ch45` folder:

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common deflate.cpp -o deflate
./deflate
```

### Line by line

**The other program's PNG and the helpers (lines 1–78)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–6 | the `#include` lines | `<cmath>` for `std::llround`, printing, strings, lists, the new header, and `antialias.h` for the disk's coverage (Chapter 27). |
| 8–19 | `const Bytes kOtherPng = { 0x89, 0x50, ... };` | The 174 bytes of the PNG of Section 45.12, written as numbers. It starts with the signature `89 50 4E 47` (Chapter 40). |
| 21–24 | `std::string oneDecimal(double v) { ... }` | One digit after the point (Chapter 43). |
| 26–37 | `void printTokens(const std::string& text) { ... for (const Lz77Token& t : findMatches(data, 64)) { if (t.length == 0) { ... '" << static_cast<char>(t.literal) << "'" ... } else { ... "(" << t.length << ", " << t.distance << ")" ... } } ... }` | Print the LZ77 items of a text: literals in quotes, matches as (length, distance). |
| 39–45 | `std::string asBinary(int code, int length) { ... }` | A code as text (Chapter 44). |
| 47–53 | `void printBytes(const char* label, const Bytes& b) { ... }` | Bytes in hex. |
| 55–62 | `void report(const char* label, const Bytes& z) { ... zlibDecompress(z, out) ... }` | Decompress and print "accepted" or the problem. |
| 64–78 | `bool samePictures(const Image& a, const Image& b) { ... }` | Chapter 39's comparison. |

**LZ77 and the fixed codes (lines 81–105)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 81–83 | three `printTokens(...)` lines | The examples of Sections 45.1 and 45.2. |
| 85–91 | `const std::vector<int> litLengths = fixedLiteralLengths(); const std::vector<int> litCodes = canonicalCodes(litLengths); const int symbols[8] = {...}; for (int s : symbols) { ... }` | Some fixed codes, at the edges of the ranges (Section 45.5). |
| 92–96 | `const int k = lengthIndex(11); const int d = distanceIndex(12); std::cout << ...` | The worked example of Section 45.4. |
| 98–105 | `const Bytes z = zlibCompress(data); printBytes("zlib:", z); ... zlibDecompress(z, back) ...` | The 19-byte stream of Section 45.6, and the text read back. |

**The pictures (lines 107–161)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 107–131 | the five pictures | The same five pictures as in Chapter 43. |
| 133–135 | `const Image* pictures[5] = {...}; const std::string names[5] = {...}; std::cout << ...` | Lists and a heading. |
| 136–142 | `const int bmp = ...makeBmpBytes(...).size()...; const int png = ...makePngBytesCompressed(...).size()...; ... const bool ok = savePNGCompressed(...) && loadPNGFull(fileName, loaded) && samePictures(...);` | The BMP size (Chapter 37) and the compressed PNG size; then save the PNG, load it from disk, and compare. |
| 143–146 | `std::cout << "  " << names[i] << ": " << bmp << ", " << makePngBytes(*pictures[i]).size() << ...oneDecimal(static_cast<double>(bmp) / png)...` | The three sizes and how many times smaller than BMP. |
| 148–154 | `Image disk(200, 200, ...); ... diskAlpha[y * 200 + x] = toByte(circleCoverage(100.0, 100.0, 80.0, x, y, 4)); ...` | Chapter 42's transparent disk. |
| 155–161 | `const bool diskOk = savePNGCompressed(disk, "disk.png", &diskAlpha) && loadPNGFull("disk.png", diskBack, &alphaBack) && alphaBack == diskAlpha; std::cout << ...` | Save with alpha (bpp 4), load, and check the alpha. |

**The other program's PNG (lines 163–187)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 163–165 | `... Image other(0, 0); std::cout << "  Chapter 42's decodePNG: " << decodePNG(kOtherPng, other) << "\n";` | The old decoder refuses it. |
| 166–174 | `PngInfo info; Bytes zdata; readPngStart(kOtherPng, info, zdata); BitReader r{&zdata, 16}; const int lastBit = getBit(r); const int type = getBits(r, 2); const int hlit = getBits(r, 5); ...` | Get the zlib data (Chapter 43's step 1) and read the first block header by hand, after the 2-byte zlib header. |
| 175–177 | `std::cout << "  zlib header " << hexByte(zdata[0]) << ...` | Section 45.9's numbers. |
| 178–180 | `problem = decodePNGFull(kOtherPng, other); std::cout << ...` | The new decoder opens it. |
| 181–185 | `const Colour first = other.getPixel(0, 0); const Colour last = other.getPixel(7, 7); std::cout << ...` | Two corner pixels, to check the result. |
| 186–187 | `std::cout << "  our savePNGCompressed makes it " << makePngBytesCompressed(other).size() << " bytes\n";` | Our own size for the same picture. |

**Broken data (lines 189–208)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 189–192 | `const Bytes hello = {'h', 'e', 'l', 'l', 'o'}; const Bytes good = zlibCompress(hello); report("the good data", good);` | "hello" with fixed codes: 14 bytes (stored would be 16). |
| 193–195 | `Bytes wrong = good; wrong[2] = static_cast<std::uint8_t>(wrong[2] \| 0x06); report("block type 3", wrong);` | Bits 1–2 of the first data byte are BTYPE; switching both on makes 3. |
| 196–198 | `wrong.back() = ...wrong.back() ^ 0x01...;` | Flip one bit of the Adler-32. |
| 199–201 | `wrong = good; wrong.resize(5);` | Keep only 5 bytes: the bits run out in the middle of a code. |
| 202–206 | `BitWriter w; writeFixedBlock(w, std::vector<Lz77Token>{Lz77Token{0, 5, 3}}, true); wrong = Bytes{0x78, 0x01}; wrong.insert(...); report(...);` | A block whose first item is a match: there is nothing to copy from. (No Adler-32 is needed; the decoder stops first.) |
| 207–208 | `return 0;` `}` | Done. |

### What you should see

```
"AAAAAAAAAA": 'A' (9, 1)
"ABRACADABRA ABRACADABRA": 'A' 'B' 'R' 'A' 'C' 'A' 'D' (4, 7) ' ' (11, 12)
"blah blah blah blah!": 'b' 'l' 'a' 'h' ' ' (14, 5) '!'
fixed code of symbol 0: 00110000
fixed code of symbol 65: 01110001
fixed code of symbol 143: 10111111
fixed code of symbol 144: 110010000
fixed code of symbol 255: 111111111
fixed code of symbol 256: 0000000
fixed code of symbol 257: 0000001
fixed code of symbol 280: 11000000
length 11 = symbol 265 + 1 extra bit (0); distance 12 = distance code 6 + 2 extra bits (3)
zlib: 78 01 73 74 0A 72 74 76 74 01 51 0A 48 6C 00 48 55 06 09
19 bytes instead of 34 (stored); read back: ABRACADABRA ABRACADABRA

file sizes (BMP, PNG of Chapter 42, compressed PNG):
  flag: 180054, 180278, 1683 (107.0 times smaller than BMP), read back the same
  sky: 180054, 180278, 1746 (103.1 times smaller than BMP), read back the same
  sunset: 180054, 180278, 1769 (101.8 times smaller than BMP), read back the same
  blend: 180054, 180278, 3132 (57.5 times smaller than BMP), read back the same
  noise: 180054, 180278, 131616 (1.4 times smaller than BMP), read back the same
  disk (RGBA): Chapter 42 160278, now 3278, alpha read back the same

a PNG made by another program (174 bytes):
  Chapter 42's decodePNG: IDAT: compressed blocks are not supported yet
  zlib header 78 DA, last block 1, block type 2, 258 literal/length codes, 12 distance codes, 18 code length codes
  decodePNGFull: accepted, 8 x 8 pixels
  pixel (0, 0) = 0 0 128, pixel (7, 7) = 255 255 128
  our savePNGCompressed makes it 100 bytes

broken zlib data:
  the good data: accepted, 5 bytes
  block type 3: refused (block type 3 does not exist)
  Adler-32 changed: refused (the Adler-32 is wrong)
  cut after 5 bytes: refused (a bad literal or length code)
  a copy from 3 bytes back at the start: refused (a match reaches back before the start)
```

And six small PNG files. Open them in a browser: they look exactly like the big ones of Chapters 42 and 43.

---

## Small examples

### Example 1 — A run of one byte

300 zeros: `0` (258, 1) (41, 1). One literal and two matches.

### Example 2 — Repeating a pixel

The bytes of 100 red pixels, `FF 00 00 FF 00 00 …`: three literals, then (258, 3) and (39, 3). Distance **3** = one RGB pixel back.

### Example 3 — The extra bits of a long match

Length 100: the largest base ≤ 100 is 99 (index 22) → symbol **279**, 4 extra bits with value **1**.

### Example 4 — The extra bits of a far distance

Distance 1,000: the largest base ≤ 1,000 is 769 (code 19) → distance code **19**, 8 extra bits with value **231**.

### Example 5 — An empty block

Compressing no data at all with fixed codes: header (3 bits) + end of block (7 bits) = 10 bits = 2 bytes, `03 00`. With the zlib header and the Adler-32 (`00 00 00 01`), that is 8 bytes — smaller than the 11-byte stored version, so `zlibCompress` uses it.

---

## Common mistakes

⚠️ **Copying a match with one block copy** (like `insert`) — it breaks overlapping copies. Copy one byte at a time.

⚠️ **Mixing the bit orders** — Huffman codes top bit first; header fields and extra bits lowest bit first.

⚠️ **Forgetting the byte boundary** — a stored block's LEN starts at the next whole byte; so does the Adler-32 after the last block.

⚠️ **Using symbol 284 for length 258** — the standard says 285.

⚠️ **Reading distance codes with the literal tree** — after a length always comes a **distance** code, with its own tree.

⚠️ **Trusting the data** — check distances, repeat counts and the output size. A tiny file can claim to unpack into gigabytes.

⚠️ **Matches shorter than 3** — Deflate has no symbol for lengths 1 and 2.

---

## Practice

🏋️ **1.** Write the LZ77 items for `abcabcabcabc` by hand. Check with `printTokens`.

🏋️ **2.** Which literal/length symbol and extra bits give length **20**? Which distance code and extra bits give distance **100**?

🏋️ **3.** What is the fixed code of the literal **200**? (Use nextCode[9] = 400.)

🏋️ **4.** Change `maxTries` in `deflateFixed` from 64 to 1, and then to 1,000. What happens to the sizes of the five pictures, and to the running time?

🏋️ **5.** Write a converter: load any PNG with `loadPNGFull` and save it again with `savePNGCompressed`. Try it on a screenshot. Is your file bigger or smaller than the original?

🏋️ **6.** Make 200 × 200 pictures that compress **badly** even with filters and LZ77, without using random numbers. (Hint: think about what makes filters fail, and what makes matches short.)

🏋️ **7.** "Lazy matching": at position i, find the best match; then also look at i + 1. If the match there is longer, write a literal for byte i and use the match at i + 1. Explain why this can help.

🏋️ **8.** Why must the decoder keep at least the last 32,768 bytes of output, even if a program only wants to write them to a file?

---

## Answers

**1.**
> 'a' 'b' 'c' then **(9, 3)**: copy 9 bytes from 3 back, overlapping (Section 45.2).

**2.**
> Length 20: the largest base ≤ 20 is 19 (index 12) → symbol **269**, 2 extra bits with value 20 − 19 = **1**.
> Distance 100: the largest base ≤ 100 is 97 (code 13) → distance code **13**, 5 extra bits with value 100 − 97 = **3**.

**3.**
> 200 is in 144–255: 9 bits, code 400 + (200 − 144) = 456 = **111001000**.

**4.**
> With 1 try, the finder only looks at the newest position with the same hash, so it misses some longer matches: the files get a little bigger (for our very regular pictures, only a little — the newest candidate is usually the best). With 1,000 tries, the files get at most a little smaller, and the program gets slower, especially on the noise picture, where the chains are long and the matches short. "How hard to try" is exactly what zlib's levels 1–9 change.

**5.**

```cpp
Image picture(0, 0);
if (loadPNGFull("screenshot.png", picture) && savePNGCompressed(picture, "again.png")) {
    std::cout << "converted\n";
}
```

> Screenshots are often 8-bit RGB or RGBA, so this works for many of them. Our file is usually **bigger** than the original: other programs use dynamic Huffman codes (Section 45.10) and try harder. For simple pictures with gradients, ours can be smaller (Section 45.12). A screenshot with transparency loses it here — pass an alpha list to both functions to keep it.

**6.**
> For example: colours from a formula that jumps a lot and almost never repeats, such as red = (x × 37 + y × 101) % 256, green = (x × x + y) % 256, blue = (x × y × 7) % 256 (each with `static_cast<std::uint8_t>`). Filters fail when neighbours are not similar; LZ77 fails when byte groups do not come back. (Any formula has patterns, so it will still compress a little.)

**7.**
> Greedy takes the first match it finds, even if it is short, and may then "use up" the bytes that would have started a much longer match one byte later. Lazy matching costs one literal (8–9 bits) but can save many more bits with the longer match. zlib does this at its higher levels.

**8.**
> A later match may copy from up to 32,768 bytes back. The decoder can only do that copy if it still has those bytes. (Our decoder keeps the whole output in memory, which covers this automatically.)

---

## Summary

🧠 **LZ77** replaces repeated bytes by **(length, distance)** matches: lengths 3–258, distances 1–32,768. A match may **overlap** itself; then it is a repeat.

🧠 Matches are found with a **hash** of 3 bytes and **chains** of earlier positions; we take the longest match (greedy), with at most 64 tries.

🧠 Deflate codes literals, end-of-block (256) and lengths (257–285) in **one** alphabet, distances in another; ranges are refined with **extra bits**.

🧠 **Fixed codes** (block type 1) come from fixed lengths 8, 9, 7, 8 and 5, through canonical codes. **Dynamic codes** (type 2) store Huffman-coded lengths, with repeat symbols 16, 17 and 18.

🧠 `zlibCompress` never does worse than stored; `zlibDecompress` reads all three block types.

🧠 Filters + LZ77 + Huffman: our simple pictures become **50 to 100 times** smaller than BMP, losslessly. `loadPNGFull` opens 8-bit RGB/RGBA PNGs from other programs.

---

## Next chapter

Our pictures can now be saved small and read back from anywhere. One thing is still missing before we start editing photos: **text**. In Chapter 46 — the last chapter of Part 6 — we design a tiny **bitmap font**: every letter is a small grid of on/off pixels, stored in a few bytes. We will draw labels, captions and numbers onto our pictures, at any size and colour, with smooth edges.
