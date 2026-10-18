# Chapter 44 — Compression Theory: Huffman Coding

> **Part 6 · Chapter 44 of 82**
> **You need:** Chapters 1–43 (especially 4, 39, 41 and 43) · **You will make:** `huffman.h` (counting, Huffman code lengths, canonical codes, a bit writer and a bit reader, a decoding tree, and a small compressor of our own), and the first real size win of the book: the filtered sky shrinks from 180,200 to 22,910 bytes

---

## What you will learn

- Why giving every byte 8 bits wastes space.
- What a **prefix code** is, and why it can be read without any separators.
- **Huffman's algorithm**: the best code lengths, built by joining the two rarest symbols again and again.
- How much compression is possible at all: **information** and **entropy**.
- **Canonical codes**: how to rebuild a whole code from its lengths only (Deflate does exactly this).
- How to write and read single **bits**, in the order Deflate uses.
- Why filters (Chapter 43) and Huffman coding work so well **together**.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **symbol** | One item we want to store. Here: one byte value, 0–255. |
| **code** | The bits we write for a symbol. |
| **prefix code** | A code where no code is the start of another code. |
| **code tree** | A tree whose left/right steps spell the codes; symbols sit at the leaves. |
| **leaf** | A point of the tree with no branches below it. |
| **Huffman code** | The prefix code with the shortest total length for given counts. |
| **entropy** | The smallest average number of bits per symbol that any such code could reach. |
| **canonical code** | A Huffman code arranged in a fixed order, so the lengths alone describe it. |
| **bit stream** | A long list of bits, packed into bytes. |

---

## 44.1 Eight bits for every byte

Every file so far has stored each byte as **8 bits**. That is a **fixed-length code**: every symbol gets the same number of bits.

📖 **New words: symbol and code** — a **symbol** is one thing we want to store (here, a byte value from 0 to 255). Its **code** is the list of bits we write for it.

Eight bits can tell apart 2⁸ = 256 different values. But look at a filtered sky row from Chapter 43:

```
   4 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 ...
```

Almost every byte is **0**. Spending 8 bits on each of them is a waste. If 0 had a **1-bit** code, the row would take about **one eighth** of the space.

🔢 **Maths: a small alphabet**

> The text `ABRACADABRA` has 11 letters but only **5 different** symbols: A, B, C, D, R.
> 5 symbols need 3 bits each (2² = 4 is too few, 2³ = 8 is enough): 11 × 3 = **33 bits**.
> As 8-bit bytes: 11 × 8 = **88 bits**.

Can we do better than 33? Yes — because the letters are not equally common. A appears **5** times, but C and D only **once**.

---

## 44.2 Short codes for common symbols

The idea is old. **Morse code** (1830s) gives the most common English letter, E, the shortest signal: a single dot. Rare letters like Q get long ones.

Let us try that for ABRACADABRA:

```
   A = 0      B = 1      R = 01      C = 10      D = 11      (a bad try!)
```

The text becomes `0 1 01 0 10 0 11 0 1 01 0` — but written as one bit stream, without spaces:

```
   010101001101010
```

Now try to read it back. Does it start with "A, B" (0, 1) or with "R" (01)? We cannot tell! Morse code solves this with **pauses** between letters. But a pause is a third kind of signal — we only have 0 and 1.

⚠️ A variable-length code needs a rule that makes the end of each code **obvious**.

---

## 44.3 Prefix codes

📖 **New word: prefix code** — a code in which **no code is the start (the "prefix") of another code**.

Here is one for our five letters:

```
   A = 0      B = 100      C = 101      D = 110      R = 111
```

No code starts with another one: A is "0", and every other code starts with "1". The four 3-bit codes are all different.

Now read `0100111…` from the left:

> "0" is a code → **A**. Start again.
> "1" is not a code; "10" is not a code; "100" → **B**. Start again.
> "1", "11", "111" → **R** …

There is never a choice. As soon as the bits read so far form a code, that **must** be the symbol — because no longer code starts with them.

📖 **New words: code tree and leaf** — a prefix code is easiest to see as a **tree**. Start at the top (the **root**). Each bit is a step: **0 = left**, **1 = right**. Every symbol sits at a **leaf** — a point with no branches below it:

```
                    (root)
                   /      \
                 0/        \1
                 A          *
                         0/   \1
                         *     *
                       0/ \1  0/ \1
                       B   C  D   R
```

- The **code** of a symbol = the steps from the root down to its leaf. B: right, left, left = `100`.
- The **length** of a code = the depth of its leaf.
- **Decoding**: start at the root, follow one step per bit, and when you reach a leaf, write its symbol and jump back to the root.

Because symbols sit only at **leaves**, no code can be the start of another — that would need a symbol in the middle of a path. Every tree like this gives a prefix code, and every prefix code gives a tree.

🔢 **Maths: the cost of this code**

> A: 5 × 1 bit = 5
> B, R: 2 × 3 + 2 × 3 = 12
> C, D: 1 × 3 + 1 × 3 = 6
> total **23 bits** — instead of 33 (3-bit codes) or 88 (bytes)

---

## 44.4 Huffman's algorithm

How do we find the **best** tree for given counts? In 1952, a student named **David Huffman** found a simple answer:

📖 **New word: Huffman code** — the prefix code with the **smallest total number of bits** for the given counts. It is built like this:

> 1. Make one **leaf** for each symbol that appears, weighted by its count.
> 2. Take the **two** items with the **smallest** weights. Join them under a new **node**, whose weight is their sum.
> 3. Repeat step 2 until only **one** item is left. That is the root.

Rare symbols are joined first, so they end up **deep** in the tree (long codes). Common symbols are joined last, so they stay near the **root** (short codes).

🔢 **Maths: Huffman for ABRACADABRA**

Counts: A 5, B 2, C 1, D 1, R 2.

| step | the two smallest | new node | items left |
|---|---|---|---|
| 1 | C (1) and D (1) | CD = 2 | A 5, B 2, R 2, CD 2 |
| 2 | B (2) and R (2) | BR = 4 | A 5, CD 2, BR 4 |
| 3 | CD (2) and BR (4) | CDBR = 6 | A 5, CDBR 6 |
| 4 | A (5) and CDBR (6) | root = 11 | root 11 |

In step 2, there were **three** items of weight 2 (B, R and CD). Any two of them would give a code just as short. We need **one fixed rule** so that our program always gives the same result: we take the item that was made **first** (leaves first, in symbol order, then new nodes in the order they were made).

The tree:

```
                  root 11
                 /       \
               A 5      CDBR 6
                       /      \
                     CD 2     BR 4
                    /   \    /    \
                   C     D  B      R
```

Depths: A = **1**; B, C, D, R = **3**. Total 5 × 1 + 6 × 3 = **23 bits**. It is the same as the code of Section 44.3 — that code **was** a Huffman code.

💡 Why is it the best? A short sketch: in the best tree, the two rarest symbols can always sit side by side at the very bottom (moving a rarer symbol deeper never costs more). Join them into one symbol, and the same argument works again for the smaller problem. Huffman's algorithm does exactly that, step by step.

⚠️ A Huffman code is the best **code that gives each symbol its own whole number of bits**. It cannot give a symbol 0.4 bits. Keep this in mind for Section 44.6.

---

## 44.5 Code lengths from the tree

Our program does not draw the tree. It stores all items in one list, `nodes`:

```
   index:  0    1    2    3    4    5     6     7       8
   item:   A5   B2   C1   D1   R2   CD2   BR4   CDBR6   root11
```

The leaves come first. Each new node is added at the end, and it remembers its two **children** by index (node 5 has children 2 and 3).

To find the depths, notice: a node is always added **after** its children. So if we walk the list **backwards** — from the root at index 8 down to index 0 — we always reach a parent before its children:

> depth[8] = 0 (the root)
> node 8 → its children 0 (A) and 7 get depth 1
> node 7 → children 5 and 6 get depth 2
> node 6 → children 1 (B) and 4 (R) get depth 3
> node 5 → children 2 (C) and 3 (D) get depth 3
> leaves: write their depth as the code **length**

No recursion and no extra stack — just one loop.

⚠️ **Two special cases.** No symbols at all: there is nothing to code. Only **one** symbol (for example, a file of only zeros): the tree would be just a root with no steps, a code of **0 bits** — but we could never tell how many symbols there are by reading bits. So we give that symbol a **1-bit** code.

---

## 44.6 How small can it get? Information and entropy

Is 23 bits the best possible for ABRACADABRA? For any code that uses whole bits per symbol, yes. But there is a deeper limit, found by **Claude Shannon** in 1948.

The idea: a symbol that appears with probability **p** carries **−log₂ p** bits of information.

🔢 **Maths: log₂**

> log₂ x is "the power of 2 that gives x": log₂ 8 = 3 (because 2³ = 8), log₂ 2 = 1, log₂ 1 = 0.
> For a probability p ≤ 1, log₂ p is negative or 0, so −log₂ p is positive.
> A symbol with p = 1/2 carries −log₂(1/2) = **1 bit**. With p = 1/8: **3 bits**.

Rare symbols carry **more** information: if something almost always happens, hearing that it happened tells you little.

📖 **New word: entropy** — the total information of all symbols: add **count × (−log₂ p)** for every symbol. No code that writes one code per symbol can use fewer bits.

🔢 **Maths: the entropy of ABRACADABRA** (11 letters)

> A: p = 5/11, −log₂(5/11) = 1.1375 bits, × 5 = 5.687
> B, R: p = 2/11, −log₂(2/11) = 2.4594 bits, × 4 = 9.838
> C, D: p = 1/11, −log₂(1/11) = 3.4594 bits, × 2 = 6.919
> total ≈ **22.44 bits**

Huffman reaches **23**: very close. The gap comes from whole bits: A "deserves" 1.14 bits and gets 1.

The gap can be **big** when one symbol is very common. In the filtered flag of Chapter 43, 179,992 of the 180,200 bytes are 0. Zero "deserves" only −log₂(179,992 / 180,200) ≈ **0.0017 bits** — but a Huffman code gives it at least **1 bit**. So 180,200 bytes can never get below 180,200 bits = **22,525 bytes** with Huffman alone, even though the entropy is only about 300 bytes. Keep this number in mind: Chapter 45 removes this limit.

💡 `entropyBits` in our header computes this limit, using `std::log2` from `<cmath>`.

---

## 44.7 Canonical codes: only the lengths

A decoder needs the **same code** as the encoder. Must we store the whole tree in the file? No. Deflate (and so PNG) stores only the **code lengths**, and both sides build the codes from the lengths with one fixed rule.

📖 **New word: canonical code** — a prefix code arranged by this rule:

> 1. Shorter codes come before longer codes (as binary numbers).
> 2. Codes of the **same length** are given out in **symbol order**, counting up by 1.

Every set of lengths that fits in a tree gives exactly **one** canonical code. And the lengths are all that Huffman's algorithm really decides — any code with the same lengths is just as short.

The rule, as Deflate's standard writes it:

> count how many codes have each length: `countOfLength[len]`
> code = 0
> for len = 1, 2, 3, …: code = (code + countOfLength[len − 1]) × 2; **nextCode[len] = code**
> then, in symbol order, each symbol of length len gets `nextCode[len]`, and `nextCode[len]` goes up by 1.

🔢 **Maths: the canonical code of ABRACADABRA**

> lengths: A 1, B 3, C 3, D 3, R 3 → countOfLength: length 1 → 1, length 2 → 0, length 3 → 4
> len 1: code = (0 + 0) × 2 = 0 → nextCode[1] = **0**
> len 2: code = (0 + 1) × 2 = 2 → nextCode[2] = 2 (no symbol uses it)
> len 3: code = (2 + 0) × 2 = 4 → nextCode[3] = **4**
> A (length 1) → **0**
> B → 4 = **100**, C → 5 = **101**, D → 6 = **110**, R → 7 = **111**

These are the codes of Section 44.3.

Why does "+ countOfLength, × 2" work? Adding the count skips past all the codes of the shorter length already given out. Multiplying by 2 adds a 0 bit at the end: it moves to the first code **one bit longer** that does not start with any code given out so far.

### Lengths that do not fit

Not every list of lengths can be a tree. Three codes of length 1 are impossible: one bit has only two values. In the rule above, the third code would get the value 2, which needs **two** bits.

🔢 **Maths: the check**

> A code of length len must be smaller than 2^len.
> lengths A 1, B 1, C 1: nextCode[1] = 0 → A = 0, B = 1, C = **2** ≥ 2¹ → too many codes

Our `canonicalCodes` marks such a symbol with −1, and the decoder refuses the lengths ("too many codes for their lengths"). Damaged or made-up files can contain such lengths, so the check matters.

💡 There is a neat formula behind this: a set of lengths fits into a tree exactly when the sum of 2^(−len) is at most 1. For A 1, B 3, C 3, D 3, R 3: 1/2 + 4 × 1/8 = **1** — a full tree. For three codes of length 1: 3/2 > 1 — impossible.

---

## 44.8 Writing bits

Our files are made of bytes, but Huffman codes are made of bits. We need a **bit writer**: something that collects bits and packs them, 8 at a time, into bytes.

📖 **New word: bit stream** — a long list of bits, packed into bytes.

Two choices must be made, and Deflate (Chapter 45) fixes both. We follow Deflate from the start:

> 1. **Inside each byte, bits are filled from the lowest bit up**: the first bit goes to bit 0 (value 1), the next to bit 1 (value 2), … the eighth to bit 7 (value 128). Then a new byte starts.
> 2. **Numbers** (like a length or a count) are written **lowest bit first** — `putBits`. **Huffman codes** are written **first bit of the code first** (the top bit) — `putCode`.

Rule 2 sounds strange, but it has a reason: a Huffman code must be read **step by step from the root**, so its first step must come first. A plain number is just copied, so Deflate uses the natural order for its bit stream.

🔢 **Maths: one byte by hand** (the program prints it)

> `putCode(110, 3 bits)`: the bits 1, 1, 0 (top bit first) go to bits 0, 1, 2 of the byte → 1 + 2 = **3**
> `putBits(5, 3 bits)`: 5 = binary 101; lowest bit first: 1, 0, 1 go to bits 3, 4, 5 → 8 + 32 = **40**
> the byte: 3 + 40 = 43 = **0x2B**

```
putCode(110, 3 bits) then putBits(5, 3 bits) gives the byte 2B
```

🔢 **Maths: ABRACADABRA as bits**

> A B R A C A D A B R A → 0 100 111 0 101 0 110 0 100 111 0
> joined: `01001110101011001001110` (23 bits)
> first byte: bits 0, 1, 0, 0, 1, 1, 1, 0 → bit 1 (2) + bit 4 (16) + bit 5 (32) + bit 6 (64) = 114 = **0x72**

```
  packed into bytes: 72 35 39
```

Three bytes instead of eleven. (The last byte has one unused bit, which stays 0.)

⚠️ When you print a byte, its bit 7 is on the **left**. With our order, the **first** bit of the stream is on the **right**. So a bit stream "printed byte by byte" looks scrambled. That is normal.

---

## 44.9 Reading bits and decoding

The **bit reader** does the reverse: it remembers a **bit position** in the bytes, and `getBit` returns bit (position mod 8) of byte (position / 8), then moves on. At the end of the data it returns −1.

To **decode**, we build the code tree of Section 44.3 from the lengths:

> 1. Compute the canonical codes from the lengths (Section 44.7).
> 2. Start with a tree that has only a root.
> 3. For each symbol, follow its code bits from the root, adding a new node wherever a step does not exist yet. Put the symbol in the last node.

Then decoding a symbol is: start at the root; read a bit; go left (0) or right (1); repeat until the node has a symbol.

Two things can go wrong with bad data:

- **The lengths do not fit** — refuse them while building (Section 44.7).
- **A step leads nowhere** — if the lengths leave an empty branch (for example, a single code `0` and nothing on the `1` side), a `1` bit leads nowhere. Or the bits run out in the middle of a code. Either way: "a code is missing or unknown".

---

## 44.10 A small file format of our own

To test everything, we pack data into a simple format of our own. It is **not** a standard; no other program reads it. It just lets us measure real sizes:

```
   4 bytes      the number of symbols, big-endian (Chapter 40)
   256 bytes    the code length of every byte value (0 = not used)
   ...          the bit stream
```

🔢 **Maths: ABRACADABRA**

> 4 + 256 + 3 = **263 bytes** — much **bigger** than the 11-byte text!

The 260-byte header is a fixed cost, so this only pays off for long data. (Deflate stores its lengths in a cleverer, compressed way — Chapter 45 shows it.)

⚠️ Code lengths are limited to **30** in our code, so that every code fits into an `int`. Huffman lengths only get that long with very strange counts (the counts would have to grow like 1, 1, 2, 3, 5, 8, 13, … for 30 steps). Deflate allows at most **15**; Chapter 45 explains how real compressors keep within that.

---

## 44.11 Filters plus Huffman

Now the test we have been waiting for. The program takes four pictures of Chapter 43 (300 × 200, so 200 × 901 = 180,200 row bytes each) and compresses their rows twice: **without** filters, and with the **best filter** for each row.

```
the PNG rows of each picture (180200 bytes), Huffman-coded:
  flag: no filter 60335, best filters 22815 bytes (limit 562), decoded the same
  sky: no filter 166298, best filters 22910 bytes (limit 1094), decoded the same
  blend: no filter 179770, best filters 26739 bytes (limit 15576), decoded the same
  noise: no filter 180460, best filters 180460 bytes (limit 180336), decoded the same
```

("limit" = the entropy of Section 44.6 in bytes, rounded up, plus our 260-byte header.)

What it means:

- **sky**: without filters, Huffman barely helps (166,298 bytes): the sky has 206 different byte values, none of them much more common than the others. With filters, almost every byte is 0, and the file shrinks to **22,910 bytes** — about **8 times smaller**. Filters and Huffman need each other.
- **flag**: even without filters, the flag has only 7 different byte values (white 255 gets 2 bits, the others 3), so Huffman already shrinks it to 60,335 bytes. With filters: 22,815.
- **blend**: filtered, it has many 0s and a few small numbers: 26,739 bytes, 6.7 times smaller.
- **noise**: nothing helps. All 256 values are about equally common, so every code is 8 bits long, and the file is 260 bytes **bigger** than the data. Random data cannot be compressed — not by any method.

🔢 **Maths: the 1-bit floor**

> flag, with filters: 179,992 zeros × 1 bit + 199 × 2 bits (the "2" filter bytes) + 9 rare bytes × 5–6 bits = 180,437 bits
> = 22,555 bytes + 260 = **22,815** ✓
> The floor: 180,200 symbols × 1 bit = 22,525 bytes. The limit: 562 bytes.

The flag and the sky are stuck just above the floor. A 1-bit code for "0" is still too long when 0 appears 900 times in a row. What we want to say is: "**the next 897 bytes are the same as before**". That is the idea of **LZ77**, the other half of Deflate — Chapter 45.

---

## Code, part 1: `huffman.h`

File: `common/huffman.h` (new). It includes `pngfilter.h` (for `Bytes` and the PNG rows we want to compress).

```cpp
#ifndef HUFFMAN_H
#define HUFFMAN_H

#include <algorithm>
#include <cmath>
#include <cstdint>
#include <string>
#include <vector>
#include "pngfilter.h"

const int kMaxCodeLength = 30;

inline std::vector<long long> countBytes(const Bytes& data) {
    std::vector<long long> counts(256, 0);
    for (std::uint8_t v : data) {
        counts[v] += 1;
    }
    return counts;
}

struct HuffmanNode {
    long long weight = 0;
    int symbol = -1;
    int left = -1;
    int right = -1;
};

inline int takeSmallest(const std::vector<HuffmanNode>& nodes, std::vector<bool>& taken) {
    int best = -1;
    for (int i = 0; i < static_cast<int>(nodes.size()); ++i) {
        if (!taken[i] && (best < 0 || nodes[i].weight < nodes[best].weight)) {
            best = i;
        }
    }
    taken[best] = true;
    return best;
}

inline std::vector<int> huffmanLengths(const std::vector<long long>& counts) {
    std::vector<int> lengths(counts.size(), 0);
    std::vector<HuffmanNode> nodes;
    for (int s = 0; s < static_cast<int>(counts.size()); ++s) {
        if (counts[s] > 0) {
            nodes.push_back(HuffmanNode{counts[s], s, -1, -1});
        }
    }
    if (nodes.empty()) {
        return lengths;
    }
    if (nodes.size() == 1) {
        lengths[nodes[0].symbol] = 1;
        return lengths;
    }
    std::vector<bool> taken(nodes.size(), false);
    int waiting = static_cast<int>(nodes.size());
    while (waiting > 1) {
        const int first = takeSmallest(nodes, taken);
        const int second = takeSmallest(nodes, taken);
        nodes.push_back(HuffmanNode{nodes[first].weight + nodes[second].weight, -1, first, second});
        taken.push_back(false);
        waiting -= 1;
    }
    std::vector<int> depth(nodes.size(), 0);
    for (int i = static_cast<int>(nodes.size()) - 1; i >= 0; --i) {
        if (nodes[i].symbol >= 0) {
            lengths[nodes[i].symbol] = depth[i];
        } else {
            depth[nodes[i].left] = depth[i] + 1;
            depth[nodes[i].right] = depth[i] + 1;
        }
    }
    return lengths;
}

inline std::vector<int> canonicalCodes(const std::vector<int>& lengths) {
    int maxLength = 0;
    for (int len : lengths) {
        maxLength = std::max(maxLength, len);
    }
    std::vector<int> countOfLength(maxLength + 1, 0);
    for (int len : lengths) {
        if (len > 0) {
            countOfLength[len] += 1;
        }
    }
    std::vector<long long> nextCode(maxLength + 1, 0);
    long long code = 0;
    for (int len = 1; len <= maxLength; ++len) {
        code = (code + countOfLength[len - 1]) << 1;
        nextCode[len] = code;
    }
    std::vector<int> codes(lengths.size(), -1);
    for (int s = 0; s < static_cast<int>(lengths.size()); ++s) {
        const int len = lengths[s];
        if (len > 0 && nextCode[len] < (1LL << len)) {
            codes[s] = static_cast<int>(nextCode[len]);
        }
        if (len > 0) {
            nextCode[len] += 1;
        }
    }
    return codes;
}

inline long long codedBits(const std::vector<long long>& counts, const std::vector<int>& lengths) {
    long long bits = 0;
    for (int s = 0; s < static_cast<int>(counts.size()); ++s) {
        bits += counts[s] * lengths[s];
    }
    return bits;
}

inline double entropyBits(const std::vector<long long>& counts) {
    long long total = 0;
    for (long long c : counts) {
        total += c;
    }
    double bits = 0.0;
    for (long long c : counts) {
        if (c > 0) {
            bits -= c * std::log2(static_cast<double>(c) / total);
        }
    }
    return bits;
}

struct BitWriter {
    Bytes bytes;
    int used = 0;
};

inline void putBit(BitWriter& w, int bit) {
    if (w.used == 0) {
        w.bytes.push_back(0);
    }
    if (bit != 0) {
        w.bytes.back() = static_cast<std::uint8_t>(w.bytes.back() | (1 << w.used));
    }
    w.used = (w.used + 1) % 8;
}

inline void putBits(BitWriter& w, int value, int count) {
    for (int i = 0; i < count; ++i) {
        putBit(w, (value >> i) & 1);
    }
}

inline void putCode(BitWriter& w, int code, int length) {
    for (int i = length - 1; i >= 0; --i) {
        putBit(w, (code >> i) & 1);
    }
}

struct BitReader {
    const Bytes* bytes = nullptr;
    long long bit = 0;
};

inline int getBit(BitReader& r) {
    const long long at = r.bit / 8;
    if (at >= static_cast<long long>(r.bytes->size())) {
        return -1;
    }
    const int bit = ((*r.bytes)[at] >> (r.bit % 8)) & 1;
    r.bit += 1;
    return bit;
}

inline int getBits(BitReader& r, int count) {
    int value = 0;
    for (int i = 0; i < count; ++i) {
        const int bit = getBit(r);
        if (bit < 0) {
            return -1;
        }
        value |= bit << i;
    }
    return value;
}

struct DecodeNode {
    int child[2] = {-1, -1};
    int symbol = -1;
};

inline std::string buildDecoder(const std::vector<int>& lengths, std::vector<DecodeNode>& tree) {
    tree.assign(1, DecodeNode{});
    for (int len : lengths) {
        if (len < 0 || len > kMaxCodeLength) {
            return "a code length is out of range";
        }
    }
    const std::vector<int> codes = canonicalCodes(lengths);
    for (int s = 0; s < static_cast<int>(lengths.size()); ++s) {
        if (lengths[s] == 0) {
            continue;
        }
        if (codes[s] < 0) {
            return "too many codes for their lengths";
        }
        int node = 0;
        for (int i = lengths[s] - 1; i >= 0; --i) {
            const int bit = (codes[s] >> i) & 1;
            if (tree[node].child[bit] < 0) {
                tree[node].child[bit] = static_cast<int>(tree.size());
                tree.push_back(DecodeNode{});
            }
            node = tree[node].child[bit];
        }
        tree[node].symbol = s;
    }
    return "";
}

inline int decodeSymbol(BitReader& r, const std::vector<DecodeNode>& tree) {
    int node = 0;
    while (tree[node].symbol < 0) {
        const int bit = getBit(r);
        if (bit < 0) {
            return -1;
        }
        node = tree[node].child[bit];
        if (node < 0) {
            return -1;
        }
    }
    return tree[node].symbol;
}

inline Bytes huffmanCompress(const Bytes& data) {
    Bytes out;
    const std::vector<int> lengths = huffmanLengths(countBytes(data));
    for (int len : lengths) {
        if (len > kMaxCodeLength) {
            return out;
        }
    }
    const std::vector<int> codes = canonicalCodes(lengths);
    putU32BE(out, static_cast<std::uint32_t>(data.size()));
    for (int len : lengths) {
        out.push_back(static_cast<std::uint8_t>(len));
    }
    BitWriter w;
    for (std::uint8_t v : data) {
        putCode(w, codes[v], lengths[v]);
    }
    out.insert(out.end(), w.bytes.begin(), w.bytes.end());
    return out;
}

inline std::string huffmanDecompress(const Bytes& packed, Bytes& out) {
    out.clear();
    if (!hasBytes(packed, 0, 4 + 256)) {
        return "too short for the header";
    }
    const std::uint32_t count = getU32BE(packed, 0);
    if (count > 100000000u) {
        return "too much data";
    }
    std::vector<int> lengths(256);
    for (int s = 0; s < 256; ++s) {
        lengths[s] = packed[4 + s];
    }
    std::vector<DecodeNode> tree;
    const std::string problem = buildDecoder(lengths, tree);
    if (!problem.empty()) {
        return problem;
    }
    BitReader r{&packed, 8LL * (4 + 256)};
    for (std::uint32_t i = 0; i < count; ++i) {
        const int s = decodeSymbol(r, tree);
        if (s < 0) {
            return "a code is missing or unknown";
        }
        out.push_back(static_cast<std::uint8_t>(s));
    }
    return "";
}

#endif
```

### Line by line

**Counting (lines 1–19)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–9 | include guard and `#include` lines | `<algorithm>` for `std::max`, `<cmath>` for `std::log2`, and everything from Chapters 36–43. |
| 11 | `const int kMaxCodeLength = 30;` | The longest code we allow, so every code fits into an `int` (Section 44.10). |
| 13–19 | `inline std::vector<long long> countBytes(const Bytes& data) { std::vector<long long> counts(256, 0); for (std::uint8_t v : data) { counts[v] += 1; } return counts; }` | How often each byte value appears. The byte itself is the index. |

**Huffman's algorithm (lines 21–73)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 21–26 | `struct HuffmanNode { long long weight = 0; int symbol = -1; int left = -1; int right = -1; };` | One item of the list (Section 44.5): its weight; for a leaf, its symbol; for a joined node, the indexes of its two children. −1 means "none". |
| 28–29 | `inline int takeSmallest(const std::vector<HuffmanNode>& nodes, std::vector<bool>& taken) { int best = -1;` | Find the lightest item that has not been joined yet. `taken[i]` is true once item i has a parent. |
| 30–34 | `for (...) { if (!taken[i] && (best < 0 \|\| nodes[i].weight < nodes[best].weight)) { best = i; } }` | Look at every free item. Only a **strictly** smaller weight replaces the best so far, so on a tie the **earlier** item wins (Section 44.4). |
| 35–37 | `taken[best] = true; return best;` `}` | Mark it as used and return its index. |
| 39–41 | `inline std::vector<int> huffmanLengths(const std::vector<long long>& counts) { std::vector<int> lengths(counts.size(), 0); std::vector<HuffmanNode> nodes;` | Code lengths for all symbols; 0 = "not used". Any number of symbols works (Deflate needs 286 later). |
| 42–46 | `for (int s = 0; ...) { if (counts[s] > 0) { nodes.push_back(HuffmanNode{counts[s], s, -1, -1}); } }` | Step 1: a leaf for each symbol that appears, in symbol order. |
| 47–53 | `if (nodes.empty()) { return lengths; } if (nodes.size() == 1) { lengths[nodes[0].symbol] = 1; return lengths; }` | The two special cases of Section 44.5. |
| 54–55 | `std::vector<bool> taken(nodes.size(), false); int waiting = static_cast<int>(nodes.size());` | Nothing is joined yet; `waiting` counts the items without a parent. |
| 56–58 | `while (waiting > 1) { const int first = takeSmallest(nodes, taken); const int second = takeSmallest(nodes, taken);` | Step 2: the two lightest free items. |
| 59–62 | `nodes.push_back(HuffmanNode{nodes[first].weight + nodes[second].weight, -1, first, second}); taken.push_back(false); waiting -= 1; }` | Join them: a new node at the end of the list, free itself. Two items lose their freedom and one is added, so `waiting` goes down by 1. When it is 1, the last node is the root. |
| 63 | `std::vector<int> depth(nodes.size(), 0);` | The depth of each item; the root (the last item) has depth 0. |
| 64 | `for (int i = static_cast<int>(nodes.size()) - 1; i >= 0; --i) {` | Walk the list backwards: parents before children (Section 44.5). |
| 65–66 | `if (nodes[i].symbol >= 0) { lengths[nodes[i].symbol] = depth[i];` | A leaf: its depth is the code length. |
| 67–70 | `} else { depth[nodes[i].left] = depth[i] + 1; depth[nodes[i].right] = depth[i] + 1; }` | A joined node: its children are one step deeper. |
| 71–73 | `}` `return lengths;` `}` | Done. |

**Canonical codes (lines 75–103)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 75–79 | `inline std::vector<int> canonicalCodes(const std::vector<int>& lengths) { int maxLength = 0; for (int len : lengths) { maxLength = std::max(maxLength, len); }` | Find the longest length. The lengths must be 0 … 30. |
| 80–85 | `std::vector<int> countOfLength(maxLength + 1, 0); for (int len : lengths) { if (len > 0) { countOfLength[len] += 1; } }` | How many codes have each length. `countOfLength[0]` stays 0, as the rule needs. |
| 86–91 | `std::vector<long long> nextCode(maxLength + 1, 0); long long code = 0; for (int len = 1; len <= maxLength; ++len) { code = (code + countOfLength[len - 1]) << 1; nextCode[len] = code; }` | The first code of each length (Section 44.7). `<< 1` is "× 2". `long long`, because with bad lengths the values can get bigger than the codes themselves. |
| 92 | `std::vector<int> codes(lengths.size(), -1);` | −1 = "no code" (unused, or impossible). |
| 93–97 | `for (...) { const int len = lengths[s]; if (len > 0 && nextCode[len] < (1LL << len)) { codes[s] = static_cast<int>(nextCode[len]); }` | In symbol order, give out the next code of that length — but only if it fits into `len` bits (the check of Section 44.7). `1LL << len` is 2^len. |
| 98–103 | `if (len > 0) { nextCode[len] += 1; }` `}` `return codes;` `}` | Count up, even after a code did not fit, so all later codes of that length also come out too big. |

**Measuring (lines 105–125)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 105–111 | `inline long long codedBits(const std::vector<long long>& counts, const std::vector<int>& lengths) { ... bits += counts[s] * lengths[s]; ... }` | The total size of the bit stream: each symbol's count times its code length. |
| 113–117 | `inline double entropyBits(const std::vector<long long>& counts) { long long total = 0; for (long long c : counts) { total += c; }` | The total number of symbols. |
| 118–125 | `double bits = 0.0; for (long long c : counts) { if (c > 0) { bits -= c * std::log2(static_cast<double>(c) / total); } } return bits; }` | Add count × (−log₂ p) for every symbol that appears (Section 44.6). Unused symbols are skipped: log₂ 0 does not exist. |

**Writing bits (lines 127–152)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 127–130 | `struct BitWriter { Bytes bytes; int used = 0; };` | The bytes written so far, and how many bits of the last byte are used (0 = start a new byte). |
| 132–135 | `inline void putBit(BitWriter& w, int bit) { if (w.used == 0) { w.bytes.push_back(0); }` | Write one bit. Start a fresh, all-zero byte when needed. |
| 136–138 | `if (bit != 0) { w.bytes.back() = static_cast<std::uint8_t>(w.bytes.back() \| (1 << w.used)); }` | A 1 bit: switch on bit number `used` of the last byte with a mask (Chapter 4). A 0 bit is already there. |
| 139–140 | `w.used = (w.used + 1) % 8;` `}` | Next bit position; after bit 7, back to 0 (a new byte next time). |
| 142–146 | `inline void putBits(BitWriter& w, int value, int count) { for (int i = 0; i < count; ++i) { putBit(w, (value >> i) & 1); } }` | A number, **lowest bit first**: bit i of the value is `(value >> i) & 1`. |
| 148–152 | `inline void putCode(BitWriter& w, int code, int length) { for (int i = length - 1; i >= 0; --i) { putBit(w, (code >> i) & 1); } }` | A Huffman code, **top bit first** (Section 44.8). |

**Reading bits (lines 154–179)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 154–157 | `struct BitReader { const Bytes* bytes = nullptr; long long bit = 0; };` | Which bytes we read, and the position in **bits** from the start. A pointer, so the reader does not copy the data. |
| 159–163 | `inline int getBit(BitReader& r) { const long long at = r.bit / 8; if (at >= static_cast<long long>(r.bytes->size())) { return -1; }` | The byte that holds the next bit. Past the end: −1. |
| 164–167 | `const int bit = ((*r.bytes)[at] >> (r.bit % 8)) & 1; r.bit += 1; return bit;` `}` | Bit number (position mod 8) of that byte — the same order as `putBit`. |
| 169–179 | `inline int getBits(BitReader& r, int count) { int value = 0; for (...) { const int bit = getBit(r); if (bit < 0) { return -1; } value \|= bit << i; } return value; }` | The reverse of `putBits`: the first bit read is bit 0 of the number. Chapter 45 needs this. |

**The decoding tree (lines 181–228)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 181–184 | `struct DecodeNode { int child[2] = {-1, -1}; int symbol = -1; };` | One point of the tree: where step 0 and step 1 lead (−1 = nowhere), and the symbol if it is a leaf. |
| 186–187 | `inline std::string buildDecoder(const std::vector<int>& lengths, std::vector<DecodeNode>& tree) { tree.assign(1, DecodeNode{});` | Build the tree from the lengths (Section 44.9). Start with only the root, at index 0. |
| 188–192 | `for (int len : lengths) { if (len < 0 \|\| len > kMaxCodeLength) { return "a code length is out of range"; } }` | Bad lengths from a damaged file are refused before any shifting. |
| 193 | `const std::vector<int> codes = canonicalCodes(lengths);` | The codes (Section 44.7). |
| 194–200 | `for (...) { if (lengths[s] == 0) { continue; } if (codes[s] < 0) { return "too many codes for their lengths"; }` | Skip unused symbols; refuse lengths that do not fit into a tree. |
| 201–203 | `int node = 0; for (int i = lengths[s] - 1; i >= 0; --i) { const int bit = (codes[s] >> i) & 1;` | Walk from the root, one code bit at a time, top bit first. |
| 204–208 | `if (tree[node].child[bit] < 0) { tree[node].child[bit] = static_cast<int>(tree.size()); tree.push_back(DecodeNode{}); } node = tree[node].child[bit];` | If that step does not exist yet, add a new node at the end of the list. Then take the step. |
| 209–213 | `}` `tree[node].symbol = s;` `}` `return "";` `}` | The last node is this symbol's leaf. |
| 215–217 | `inline int decodeSymbol(BitReader& r, const std::vector<DecodeNode>& tree) { int node = 0; while (tree[node].symbol < 0) {` | Read one symbol: walk down until we stand on a leaf. |
| 218–221 | `const int bit = getBit(r); if (bit < 0) { return -1; }` | The data ran out in the middle of a code. |
| 222–228 | `node = tree[node].child[bit]; if (node < 0) { return -1; } } return tree[node].symbol; }` | Take the step. A step to nowhere means the bits are not a valid code. |

**Our small compressor (lines 230–280)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 230–237 | `inline Bytes huffmanCompress(const Bytes& data) { Bytes out; const std::vector<int> lengths = huffmanLengths(countBytes(data)); for (int len : lengths) { if (len > kMaxCodeLength) { return out; } }` | Count, build the lengths, and give up (an empty result) in the very rare case of a too-long code. |
| 238–242 | `const std::vector<int> codes = canonicalCodes(lengths); putU32BE(out, ...data.size()...); for (int len : lengths) { out.push_back(...len...); }` | The header of Section 44.10: the count (Chapter 40's big-endian writer) and 256 lengths. |
| 243–246 | `BitWriter w; for (std::uint8_t v : data) { putCode(w, codes[v], lengths[v]); }` | The bit stream: one code per byte. |
| 247–249 | `out.insert(out.end(), w.bytes.begin(), w.bytes.end()); return out;` `}` | Header + bits. |
| 251–255 | `inline std::string huffmanDecompress(const Bytes& packed, Bytes& out) { out.clear(); if (!hasBytes(packed, 0, 4 + 256)) { return "too short for the header"; }` | The reverse. It returns `""` or a problem, like all our readers. |
| 256–259 | `const std::uint32_t count = getU32BE(packed, 0); if (count > 100000000u) { return "too much data"; }` | A safety limit, as in Chapter 38. |
| 260–263 | `std::vector<int> lengths(256); for (int s = 0; s < 256; ++s) { lengths[s] = packed[4 + s]; }` | Read the 256 lengths. |
| 264–268 | `std::vector<DecodeNode> tree; const std::string problem = buildDecoder(lengths, tree); if (...) { return problem; }` | Build (and check) the decoding tree. |
| 269 | `BitReader r{&packed, 8LL * (4 + 256)};` | The bit stream starts after the 260-byte header: at bit 2,080. |
| 270–277 | `for (std::uint32_t i = 0; i < count; ++i) { const int s = decodeSymbol(r, tree); if (s < 0) { return "a code is missing or unknown"; } out.push_back(...s...); } return "";` | Decode exactly `count` symbols. |
| 278–280 | `}` `#endif` | End of the function and of the include guard. |

---

## Code, part 2: Huffman at work

File: `ch44/huffman.cpp`

```cpp
#include <cmath>
#include <iostream>
#include <string>
#include <vector>
#include "huffman.h"

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

int main() {
    const std::string text = "ABRACADABRA";
    const Bytes data(text.begin(), text.end());
    const std::vector<long long> counts = countBytes(data);
    const std::vector<int> lengths = huffmanLengths(counts);
    const std::vector<int> codes = canonicalCodes(lengths);
    std::cout << "\"" << text << "\":\n";
    for (int s = 0; s < 256; ++s) {
        if (counts[s] > 0) {
            std::cout << "  '" << static_cast<char>(s) << "' count " << counts[s] << ", length "
                      << lengths[s] << ", code " << asBinary(codes[s], lengths[s]) << "\n";
        }
    }
    std::cout << "  " << codedBits(counts, lengths) << " bits instead of " << 8 * data.size()
              << "; the best possible is " << entropyBits(counts) << " bits\n";

    BitWriter w;
    std::string allBits;
    for (std::uint8_t v : data) {
        putCode(w, codes[v], lengths[v]);
        allBits += asBinary(codes[v], lengths[v]);
    }
    std::cout << "  the bits in order: " << allBits << "\n";
    printBytes("  packed into bytes:", w.bytes);

    BitWriter order;
    putCode(order, 6, 3);
    putBits(order, 5, 3);
    std::cout << "putCode(110, 3 bits) then putBits(5, 3 bits) gives the byte "
              << hexByte(order.bytes[0]) << "\n";

    const Bytes packed = huffmanCompress(data);
    Bytes back;
    std::string problem = huffmanDecompress(packed, back);
    const std::string result = problem.empty() ? std::string(back.begin(), back.end()) : problem;
    std::cout << "compressed: " << packed.size() << " bytes (4 + 256 + " << packed.size() - 260
              << "), decompressed: " << result << "\n";

    std::vector<int> bad(256, 0);
    bad['A'] = 1;
    bad['B'] = 1;
    bad['C'] = 1;
    std::vector<DecodeNode> tree;
    std::cout << "three codes of length 1: " << buildDecoder(bad, tree) << "\n";
    Bytes cut = packed;
    cut.pop_back();
    problem = huffmanDecompress(cut, back);
    std::cout << "the last byte missing: " << problem << "\n";

    Image flag(300, 200);
    Image sky(300, 200);
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
            blend.setPixel(x, y, Colour{static_cast<std::uint8_t>(x * 255 / 299),
                                        static_cast<std::uint8_t>(y * 255 / 199),
                                        static_cast<std::uint8_t>((x + y) * 255 / 498)});
            seed = seed * 1103515245u + 12345u;
            const std::uint8_t v = static_cast<std::uint8_t>(seed >> 24);
            noise.setPixel(x, y, Colour{v, v, v});
        }
    }

    const Image* pictures[4] = {&flag, &sky, &blend, &noise};
    const std::string names[4] = {"flag", "sky", "blend", "noise"};
    std::cout << "\nthe PNG rows of each picture (180200 bytes), Huffman-coded:\n";
    for (int i = 0; i < 4; ++i) {
        const Bytes plain = makePngRows(*pictures[i], nullptr);
        const Bytes filtered = filterScanlines(plain, 900, 3, kFilterBest);
        const Bytes small = huffmanCompress(filtered);
        problem = huffmanDecompress(small, back);
        const bool same = problem.empty() && back == filtered;
        const long long limit = std::llround(std::ceil(entropyBits(countBytes(filtered)) / 8.0));
        std::cout << "  " << names[i] << ": no filter " << huffmanCompress(plain).size()
                  << ", best filters " << small.size() << " bytes (limit " << limit + 260 << "), "
                  << (same ? "decoded the same" : "DECODE FAILED") << "\n";
    }
    return 0;
}
```

Build and run it from the `code/ch44` folder:

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common huffman.cpp -o huffman
./huffman
```

### Line by line

**Helpers (lines 1–21)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–5 | the `#include` lines | `<cmath>` for `std::ceil` and `std::llround`, printing, strings, lists, and the new header. |
| 7–13 | `std::string asBinary(int code, int length) { ... s += ((code >> i) & 1) ? '1' : '0'; ... }` | A code as text, top bit first: (6, 3) → "110". |
| 15–21 | `void printBytes(const char* label, const Bytes& b) { ... }` | Print bytes in hex (Chapter 36's `hexByte`). |

**ABRACADABRA (lines 24–46)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 24–25 | `const std::string text = "ABRACADABRA"; const Bytes data(text.begin(), text.end());` | The text as bytes (A = 65, B = 66, …). |
| 26–28 | `counts = countBytes(data); lengths = huffmanLengths(counts); codes = canonicalCodes(lengths);` | The three steps: count, lengths, codes. |
| 29–35 | `for (int s = 0; s < 256; ++s) { if (counts[s] > 0) { std::cout << ... static_cast<char>(s) << ... asBinary(codes[s], lengths[s]) ... } }` | Print each letter that appears, with its count, length and code. |
| 36–37 | `std::cout << "  " << codedBits(counts, lengths) << " bits instead of " << 8 * data.size() << ... entropyBits(counts) ...` | 23 bits, 88 bits, and the entropy of Section 44.6. |
| 39–44 | `BitWriter w; std::string allBits; for (std::uint8_t v : data) { putCode(w, codes[v], lengths[v]); allBits += asBinary(...); }` | Write the codes into a bit stream, and also collect them as text. |
| 45–46 | print the bits and the bytes | Section 44.8. |

**The bit order (lines 48–52)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 48–52 | `BitWriter order; putCode(order, 6, 3); putBits(order, 5, 3); std::cout << ... hexByte(order.bytes[0]) ...` | The worked byte of Section 44.8: 0x2B. |

**Our format and broken data (lines 54–70)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 54–56 | `const Bytes packed = huffmanCompress(data); Bytes back; std::string problem = huffmanDecompress(packed, back);` | Compress and decompress the text. |
| 57–59 | `const std::string result = problem.empty() ? std::string(back.begin(), back.end()) : problem; std::cout << ...` | Print the text that came back — or the problem. |
| 61–66 | `std::vector<int> bad(256, 0); bad['A'] = 1; bad['B'] = 1; bad['C'] = 1; ... buildDecoder(bad, tree) ...` | Three codes of length 1 cannot fit (Section 44.7). `'A'` is used as the index 65. |
| 67–70 | `Bytes cut = packed; cut.pop_back(); problem = huffmanDecompress(cut, back); ...` | The 23 bits need 3 bytes; with only 2, the bits run out. |

**Four pictures (lines 72–94)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 72–94 | the four pictures and their loops | The flag, sky, blend and noise pictures of Chapter 43, made exactly the same way. |

**Filters plus Huffman (lines 96–111)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 96–98 | `const Image* pictures[4] = {...}; const std::string names[4] = {...}; std::cout << ...` | The four pictures and a heading. |
| 99–101 | `const Bytes plain = makePngRows(*pictures[i], nullptr); const Bytes filtered = filterScanlines(plain, 900, 3, kFilterBest);` | The PNG rows without filters (Chapter 42) and with the best filter for each row (Chapter 43). |
| 102–104 | `const Bytes small = huffmanCompress(filtered); problem = huffmanDecompress(small, back); const bool same = problem.empty() && back == filtered;` | Compress the filtered rows and check that they come back exactly. |
| 105 | `const long long limit = std::llround(std::ceil(entropyBits(countBytes(filtered)) / 8.0));` | The entropy in whole bytes, rounded up. |
| 106–108 | `std::cout << "  " << names[i] << ": no filter " << huffmanCompress(plain).size() << ...` | Both sizes, the limit (+ 260 for our header), and the check. |
| 109–111 | `}` `return 0;` `}` | Done. |

### What you should see

```
"ABRACADABRA":
  'A' count 5, length 1, code 0
  'B' count 2, length 3, code 100
  'C' count 1, length 3, code 101
  'D' count 1, length 3, code 110
  'R' count 2, length 3, code 111
  23 bits instead of 88; the best possible is 22.4441 bits
  the bits in order: 01001110101011001001110
  packed into bytes: 72 35 39
putCode(110, 3 bits) then putBits(5, 3 bits) gives the byte 2B
compressed: 263 bytes (4 + 256 + 3), decompressed: ABRACADABRA
three codes of length 1: too many codes for their lengths
the last byte missing: a code is missing or unknown

the PNG rows of each picture (180200 bytes), Huffman-coded:
  flag: no filter 60335, best filters 22815 bytes (limit 562), decoded the same
  sky: no filter 166298, best filters 22910 bytes (limit 1094), decoded the same
  blend: no filter 179770, best filters 26739 bytes (limit 15576), decoded the same
  noise: no filter 180460, best filters 180460 bytes (limit 180336), decoded the same
```

---

## Small examples

### Example 1 — Two symbols

Data `0 0 0 1` (three zeros, one 1). Huffman joins the two leaves at once: both get length **1**. Canonical codes: 0 → `0`, 1 → `1`. 4 bits. The entropy is 3.24 bits — Huffman cannot go below 1 bit per symbol.

### Example 2 — Equal counts

Four symbols, each appearing 10 times. Every code gets length **2**: 00, 01, 10, 11. For equal counts, Huffman gives a plain fixed-length code.

### Example 3 — Canonical codes from lengths

Lengths: a 2, b 1, c 3, d 3. countOfLength: 1 → 1, 2 → 1, 3 → 2. nextCode[1] = 0, nextCode[2] = (0 + 1) × 2 = 2, nextCode[3] = (2 + 1) × 2 = 6. Codes: b = `0`, a = `10`, c = `110`, d = `111`.

### Example 4 — Do these lengths fit?

Lengths 1, 2, 2, 2: 1/2 + 3 × 1/4 = 5/4 > 1 → **no**. Lengths 2, 2, 2, 3, 3: 3 × 1/4 + 2 × 1/8 = **1** → yes, a full tree.

### Example 5 — Reading a bit stream

Byte `0x0D` = binary 0000 1101. Read lowest bit first: **1, 0, 1, 1**, 0, 0, 0, 0. With the ABRACADABRA code, `1 0 1` is C, then `1 0 …` continues the next code.

---

## Common mistakes

⚠️ **A code that is the start of another** — not a prefix code; the decoder cannot know where a code ends. Huffman trees never do this.

⚠️ **No fixed rule for ties** — the encoder and the decoder must build the **same** code. With canonical codes, only the lengths travel, and the rule is fixed.

⚠️ **Mixing up the bit orders** — numbers lowest bit first (`putBits`), Huffman codes top bit first (`putCode`), and each byte filled from bit 0.

⚠️ **Forgetting the single-symbol case** — a 0-bit code cannot be counted. Give it 1 bit.

⚠️ **Trusting the lengths in a file** — check that they fit (`codes[s] < 0`) and that they are not too long.

⚠️ **Expecting Huffman to shrink random data** — nothing can. Our format even makes it 260 bytes bigger.

---

## Practice

🏋️ **1.** Build the Huffman code for the text `MISSISSIPPI` by hand (M 1, I 4, S 4, P 2), with our tie rule. How many bits does it take?

🏋️ **2.** Compute the canonical codes for the lengths: A 2, B 2, C 2, D 3, E 3.

🏋️ **3.** Is `0, 10, 110, 111` a prefix code? Is `0, 01, 11`? Explain with a tree.

🏋️ **4.** Write `std::string decodeText(const Bytes& stream, int bitCount, const std::vector<DecodeNode>& tree)` that decodes exactly `bitCount` bits and returns the letters.

🏋️ **5.** Compress the PNG rows of the sky with each **single** filter (None, Sub, Up, Average, Paeth). Which one is smallest after Huffman? Is it the same filter that "Best" mostly chose?

🏋️ **6.** Compute the entropy of a picture where 99 % of the bytes are 0 and 1 % are 1. How many bits per byte does Huffman use? How many does the entropy allow?

🏋️ **7.** Our header stores 256 lengths in 256 bytes, though each length is at most 30. How could you store them in fewer bytes? (Hint: most are 0.)

🏋️ **8.** Why do we compress the **filter bytes** of each row too, together with the pixel bytes? Would it be better to leave them out?

---

## Answers

**1.**
> Leaves in symbol order: I 4, M 1, P 2, S 4.
> Step 1: M (1) + P (2) = MP 3. Step 2: the smallest are MP (3) and then I (4) — I comes before S → IMP 7. Step 3: S (4) + IMP (7) = root 11.
> Lengths: S 1, I 2, M 3, P 3. Bits: 4 × 1 + 4 × 2 + 1 × 3 + 2 × 3 = **21 bits** (instead of 88).

**2.**
> countOfLength: 2 → 3, 3 → 2. nextCode[1] = 0, nextCode[2] = (0 + 0) × 2 = 0, nextCode[3] = (0 + 3) × 2 = 6.
> A = `00`, B = `01`, C = `10`, D = `110`, E = `111`.

**3.**
> `0, 10, 110, 111`: yes — every code ends at a leaf (it is the tree of a Huffman code).
> `0, 01, 11`: no — `0` is the start of `01`. In the tree, the symbol for `0` would sit on the path to `01`, not at a leaf.

**4.**

```cpp
std::string decodeText(const Bytes& stream, int bitCount, const std::vector<DecodeNode>& tree) {
    BitReader r{&stream, 0};
    std::string text;
    while (r.bit < bitCount) {
        const int s = decodeSymbol(r, tree);
        if (s < 0) {
            break;
        }
        text += static_cast<char>(s);
    }
    return text;
}
```

> For ABRACADABRA, call it with the 3 bytes `72 35 39` and `bitCount` 23. Without the count, the unused last bit (a 0) would be read as one more A.

**5.**

```cpp
for (int mode = kFilterNone; mode <= kFilterBest; ++mode) {
    Bytes rows = filterScanlines(makePngRows(sky, nullptr), 900, 3, mode);
    std::cout << kFilterNames[mode] << ": " << huffmanCompress(rows).size() << "\n";
}
```

> (Copy `kFilterNames` from Chapter 43.) The sizes: None 166,298, Sub 23,419, Up 38,423, Average 34,713, Paeth **22,910**, Best **22,910**. Sub and Paeth are close, because both turn each sky row into almost only zeros; Best is exactly Paeth's size, because it chose Paeth for 199 of the 200 rows (and Sub for the top row, where the two are the same). Up is much bigger: its rows are full of 1s.

**6.**
> −(0.99 × log₂ 0.99 + 0.01 × log₂ 0.01) = 0.99 × 0.0145 + 0.01 × 6.644 ≈ **0.081 bits per byte**. Huffman uses **1 bit** per byte (two symbols, each 1 bit) — more than 12 times the limit.

**7.**
> For example: store only the symbols that are used (a count, then pairs "symbol, length"), or store each length in 5 bits with `putBits`. Deflate goes further: it **Huffman-codes the lengths themselves**, with special codes for "repeat the last length" and "many zeros" (Chapter 45).

**8.**
> The filter bytes are part of the data that the PNG decoder needs, and they are in the same zlib stream. They are only 200 of 180,200 bytes, and they repeat a lot (199 rows of filter 4 in the sky), so they cost very little. Leaving them out would break the PNG format.

---

## Summary

🧠 Fixed 8-bit codes waste space when some byte values are much more common than others.

🧠 A **prefix code** (no code starts another) can be read without separators; it is a **tree** with symbols at the leaves.

🧠 **Huffman**: join the two lightest items until one is left. Rare symbols end up deep (long codes), common ones near the root.

🧠 The **entropy** (Σ count × −log₂ p) is the limit for one-code-per-symbol coding; Huffman is close, but never below **1 bit per symbol**.

🧠 **Canonical codes**: only the **lengths** are stored; codes of each length are counted out in symbol order. Check that the lengths fit (2^(−len) adds up to at most 1).

🧠 Bits fill each byte from bit 0; numbers go **lowest bit first**, Huffman codes **top bit first** — Deflate's rules.

🧠 Filters + Huffman: the sky shrinks from 180,200 to 22,910 bytes. The 1-bit floor remains.

---

## Next chapter

Huffman coding needs at least one bit for every byte — still 900 bits for a row of 900 zeros. In Chapter 45 we add the missing half of PNG's compression, **LZ77**: "copy the 897 bytes that start 3 bytes back". Together with Huffman codes, this is **Deflate**. Our `zlib` will finally compress for real, our PNG files will become many times smaller than BMP, and `loadPNG` will open PNG files made by other programs.
