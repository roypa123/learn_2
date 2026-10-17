# Chapter 12 — Reading a PPM File Back

> **Part 2 · Chapter 12 of 82**
> **You need:** Chapters 1–11 · **You will make:** `loadPPM` in `image.h` (reads P3 and P6), and a program that loads an image, makes a **negative** of it, and saves it

---

## What you will learn

- Why reading images matters: **open → change → save**, and checking our own writers.
- How to read a **whole file** into memory quickly with `seekg`, `tellg` and `read`.
- How to **parse** a header with a **position** that moves through the bytes.
- How to skip whitespace **and comments**.
- How to turn digit characters into a number, by hand.
- How to **check** a file, so a broken file cannot crash our program.
- How to change any maxval into 0–255 with **integer rounding**.
- Why free functions in a header must be **`inline`**.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **parser** | Code that reads text or bytes and works out what they mean. |
| **position** (or **cursor**) | A number that says which byte we will look at next. |
| **validate** | To check that data follows the rules before we use it. |
| **robust** | Code that does not crash or misbehave, even when it gets bad input. |
| **round trip** | Saving data and loading it back, to check nothing changed. |
| **integer overflow** | When the result of `int` maths is too big for an `int`. |
| **inline function** | A function that is allowed to be defined in many `.cpp` files (for example, through a header). |

---

## 12.1 Why read images?

Until now our programs only **made** pictures. Reading gives us two new powers:

**1. Open → change → save.** Load any PPM picture, change its pixels, and save it again. Parts 3 and 7 do this a lot: grey (Chapter 15), brightness (47), blur (50), edges (51)…

**2. Check our own writers.**

📖 **New word: round trip** — save data, load it back, and compare. If anything changed, there is a bug.

```
Image ──savePPM──► file ──loadPPM──► Image
  │                                    │
  └───────────── same pixels? ─────────┘
```

We do this in this chapter's code with `first_binary.ppm`.

---

## 12.2 The plan

📖 **New word: parser** — code that reads text or bytes and works out what they mean.

Our parser works in **two steps**:

1. Read **all** the bytes of the file into a `std::vector<std::uint8_t>`.
2. Walk through that vector with a **position**, reading the header and then the pixels.

📖 **New word: position** (or **cursor**) — a number that says which byte we look at next.

```
bytes:     P  6  \n  3  _  2  \n  2  5  5  \n  FF 00 00 ...
index:     0  1  2   3  4  5  6   7  8  9  10  11 ...
                     ↑
                    pos = 3 → next we read the width
```

Each time we read something, we move `pos` forward past it.

Why read everything first, instead of reading from the stream bit by bit? Because then we can look at any byte with `bytes[pos]`, check how many bytes are left with `bytes.size() - pos`, and never worry about the stream failing halfway.

---

## 12.3 Reading a whole file quickly

In Chapter 7 we read files one byte at a time with `get`, and promised a faster way. Here it is:

```cpp
std::ifstream file(fileName, std::ios::binary | std::ios::ate);
const std::streamsize size = static_cast<std::streamsize>(file.tellg());
file.seekg(0, std::ios::beg);
bytes.resize(size);
file.read(reinterpret_cast<char*>(bytes.data()), size);
```

| Step | Code | Meaning |
|---|---|---|
| 1 | `std::ios::ate` | Open with the position **at the end** (Chapter 9). |
| 2 | `file.tellg()` | The position at the end = the file size (Chapter 9, Section 9.6). |
| 3 | `file.seekg(0, std::ios::beg)` | **Move** the read position: 0 bytes from the **beginning**. Now we are at the start again. `seekg` means "seek (go to) a position for getting". |
| 4 | `bytes.resize(size)` | Make the vector exactly big enough. |
| 5 | `file.read(...)` | Read `size` bytes **in one call**, straight into the vector's memory. It is the mirror of `write` from Chapter 7, so it needs a `char*` (not `const`, because it writes into the vector). |

One `read` call for the whole file is **much** faster than millions of `get` calls.

⚠️ **Careful:** `tellg` returns −1 if something went wrong. A size of −1 would be a disaster for `resize`. So we check `size < 0` before using it.

---

## 12.4 Skipping whitespace and comments

Remember the P3 and P6 rules (Chapters 8 and 9): between the header numbers there may be any whitespace, and **comments** starting with `#` that go to the end of the line.

```
P3
# a 2 x 2 test image with maxval 15
2 2
15
```

Our skip function loops:
- If the byte is **whitespace** (space, tab, `\n`, `\r`), move past it.
- If the byte is **`#`**, move forward until we reach a `\n` (the end of the comment line). The `\n` itself is then skipped as whitespace in the next round.
- Otherwise, **stop**: we have reached something real (a digit, we hope).

🔢 **Example: skipping from the end of `P3`**

> pos = 2: `\n` → whitespace → pos = 3
> pos = 3: `#` → comment → skip to the next `\n` (at the end of the comment line)
> the `\n` → whitespace → move past it
> next byte: `2` → not whitespace, not `#` → **stop**. We are at the width.

---

## 12.5 Reading a number, digit by digit

In Chapter 8 (Section 8.4) we saw how a viewer turns the text `255` into the number 255. Now we write it:

```cpp
value = 0;
while (the byte at pos is a digit) {
    value = value * 10 + (byte - '0');
    ++pos;
}
```

🔢 **Maths: reading `"128"`**

> start: value = 0
> `'1'` (code 49): digit = 49 − 48 = 1 → value = 0 × 10 + 1 = **1**
> `'2'` (code 50): digit = 2 → value = 1 × 10 + 2 = **12**
> `'8'` (code 56): digit = 8 → value = 12 × 10 + 8 = **128**
> next byte is a space → not a digit → stop. value = 128.

`byte - '0'` is the same as `code − 48` (Chapter 7, Section 7.2), because `'0'` **is** 48.

### Two safety checks

**Before** the loop: the first byte **must** be a digit. If it is a letter, or the file has ended, the file is broken, and we return `false`.

**Inside** the loop: if the number grows past **1,000,000**, we stop with `false`. Why? A broken file might contain `99999999999999` — too big for an `int`.

📖 **New word: integer overflow** — when `int` maths gives a result too big for an `int`.

🔢 **Maths: how big can an `int` be?**

> An `int` is usually 4 bytes = 32 bits, with one bit for the sign.
> The biggest value is 2³¹ − 1 = **2,147,483,647** (Chapter 4's table).
> If value = 999,999,999 and we read one more digit: 999,999,999 × 10 = 9,999,999,990 → too big!

For a **signed** `int`, overflow is not a "wrap-around" like with bytes. It is **undefined behaviour** (Chapter 4, Section 4.9): the program may do anything. So we stop **long before** that. No real image is a million pixels wide.

---

## 12.6 Validating the header

📖 **New word: validate** — to check that data follows the rules before we use it.

📖 **New word: robust** — code that does not crash, even with bad input.

Files can be **broken** (cut short while downloading, edited by mistake) or even made **on purpose** to crash programs. A robust loader checks everything before it trusts it.

| Check | Why |
|---|---|
| The file has at least 2 bytes | We read `bytes[0]` and `bytes[1]`. |
| It starts with `P3` or `P6` | Otherwise it is not a colour PPM. |
| Width, height and maxval are all numbers | Otherwise the header is broken. |
| width > 0, height > 0 | An image of size 0 or less makes no sense. |
| 0 < maxval ≤ 255 | We only support one byte per channel (Chapter 9, Section 9.8). |
| width × height ≤ 100,000,000 | So a broken header cannot make us try to use huge amounts of memory. |
| (P6) one whitespace after maxval | Chapter 9, Section 9.3. |
| (P6) enough bytes left for all pixels | Otherwise we would read past the end of the vector. |
| (P3) each value ≤ maxval | A value of 20 with maxval 15 breaks the rules. |

🔢 **Maths: why the 100,000,000 limit?**

> Say a broken file says width = 1,000,000 and height = 1,000,000.
> Both pass the "≤ 1,000,000" number check.
> pixels = 1,000,000 × 1,000,000 = 1,000,000,000,000 (one trillion)
> bytes = 3 trillion — about 3,000 GB of memory!
> Also, 1,000,000 × 1,000,000 does not fit in an `int`, so `width * height` would **overflow**.

So we compute `width × height` as a **`long long`** (a 64-bit integer that holds up to about 9 × 10¹⁸) and reject anything above 100 million pixels.

> 100,000,000 pixels × 3 = 300,000,000 bytes ≈ 300 MB. Big, but possible.
> A 4K image is only 8.3 million pixels (Chapter 2), well below the limit.

---

## 12.7 Reading the pixels

### P6 (binary)

After the maxval:
1. The byte at `pos` must be **one** whitespace. Skip exactly it (`++pos`). **Do not** call the skip function — it would also skip pixel bytes that happen to be 10 or 32 (Chapter 9)!
2. Check that at least `width × height × 3` bytes are left.
3. Read three bytes per pixel, row by row, and move `pos` forward by 3 each time.

🔢 **Maths: are there enough bytes in `first_binary.ppm`?**

> file size = 29 bytes (Chapter 9)
> after the header and its one whitespace: pos = 11
> bytes left = 29 − 11 = 18
> needed = 3 × 2 × 3 = 18
> 18 ≥ 18 → OK ✓

### P3 (text)

For each pixel, read **three numbers** with the same `readNumber` we used for the header. `readNumber` skips whitespace (and even comments) by itself, so any layout of the numbers works.

---

## 12.8 Scaling any maxval to 0–255

Our `Image` stores bytes from 0 to 255. But a file may use another maxval, like 15 (Chapter 8, Section 8.7). We must **scale** each value:

> byte = value × 255 ÷ maxval

🔢 **Maths: value 5 with maxval 15**

> 5 × 255 ÷ 15 = 1,275 ÷ 15 = **85**

But often the answer is not a whole number:

> value 2 with maxval 4: 2 × 255 ÷ 4 = 510 ÷ 4 = 127.5

Integer division would **cut** 127.5 to 127. We want to **round** it to 128 (Chapter 5, Section 5.9). With `double` we added 0.5. With integers, there is a matching trick:

> **rounded (a ÷ b) = (a + b ÷ 2) ÷ b** (all integer maths)

Adding **half of b** before dividing does the same job as adding 0.5 after dividing.

🔢 **Maths: check the trick**

> a = 510, b = 4: (510 + 4 ÷ 2) ÷ 4 = (510 + 2) ÷ 4 = 512 ÷ 4 = **128** ✓ (127.5 rounds to 128)
> a = 1,275, b = 15: (1,275 + 7) ÷ 15 = 1,282 ÷ 15 = 85.47 → cut → **85** ✓
> a = 3,825, b = 15 (value 15): (3,825 + 7) ÷ 15 = 3,832 ÷ 15 = 255.47 → **255** ✓ (full stays full)
> a = 0: (0 + 7) ÷ 15 = 0 ✓ (none stays none)

So our function is:

```cpp
(value * 255 + maxval / 2) / maxval
```

When maxval is 255, this gives back exactly the same value: (v × 255 + 127) ÷ 255 = v (because 127 ÷ 255 is less than 1). So for normal files, nothing changes.

We also make sure `value` is never bigger than maxval before scaling (a broken P6 file could have the byte 200 with maxval 15). Otherwise the answer would be bigger than 255 and **wrap around** (Chapter 4).

---

## 12.9 `inline` for functions in a header

📖 **New word: inline function** — a function that is allowed to be defined in many `.cpp` files.

In Chapter 11, every function was **inside** the `Image` class, and those are automatically inline. Now `loadPPM` and its helpers are **free functions** (outside any class), and they live in a header.

If two `.cpp` files of the same program both `#include "image.h"`, each would get its own copy of `loadPPM`. The linker would see **two definitions** of the same function and stop with an error like "multiple definition of `loadPPM`".

Writing **`inline`** in front of each function tells the linker: "this function may appear in several files; they are all the same; keep one". This is what makes a header-only library work.

🧠 **Remember:** Free functions defined in a header must be marked **`inline`**.

---

## Code, part 1: the new part of `image.h`

Add this code to `common/image.h`, **after** the end of the `Image` class (after its `};`) and **before** the final `#endif`. The line numbers are the real line numbers in the finished file.

```cpp
inline bool readFileBytes(const std::string& fileName, std::vector<std::uint8_t>& bytes) {
    std::ifstream file(fileName, std::ios::binary | std::ios::ate);
    if (!file) {
        return false;
    }
    const std::streamsize size = static_cast<std::streamsize>(file.tellg());
    if (size < 0) {
        return false;
    }
    file.seekg(0, std::ios::beg);
    bytes.resize(size);
    file.read(reinterpret_cast<char*>(bytes.data()), size);
    return static_cast<bool>(file);
}

inline bool isSpace(std::uint8_t c) {
    return c == ' ' || c == '\t' || c == '\n' || c == '\r';
}

inline void skipSpaceAndComments(const std::vector<std::uint8_t>& bytes, int& pos) {
    const int n = static_cast<int>(bytes.size());
    while (pos < n) {
        if (isSpace(bytes[pos])) {
            ++pos;
        } else if (bytes[pos] == '#') {
            while (pos < n && bytes[pos] != '\n') {
                ++pos;
            }
        } else {
            return;
        }
    }
}

inline bool readNumber(const std::vector<std::uint8_t>& bytes, int& pos, int& value) {
    skipSpaceAndComments(bytes, pos);
    const int n = static_cast<int>(bytes.size());
    if (pos >= n || bytes[pos] < '0' || bytes[pos] > '9') {
        return false;
    }
    value = 0;
    while (pos < n && bytes[pos] >= '0' && bytes[pos] <= '9') {
        value = value * 10 + (bytes[pos] - '0');
        if (value > 1000000) {
            return false;
        }
        ++pos;
    }
    return true;
}

inline std::uint8_t scaleToByte(int value, int maxval) {
    if (value > maxval) {
        value = maxval;
    }
    return static_cast<std::uint8_t>((value * 255 + maxval / 2) / maxval);
}

inline bool loadPPM(const std::string& fileName, Image& image) {
    std::vector<std::uint8_t> bytes;
    if (!readFileBytes(fileName, bytes) || bytes.size() < 2) {
        return false;
    }
    if (bytes[0] != 'P' || (bytes[1] != '3' && bytes[1] != '6')) {
        return false;
    }
    const bool binary = (bytes[1] == '6');
    int pos = 2;
    int width = 0;
    int height = 0;
    int maxval = 0;
    if (!readNumber(bytes, pos, width) || !readNumber(bytes, pos, height) ||
        !readNumber(bytes, pos, maxval)) {
        return false;
    }
    if (width <= 0 || height <= 0 || maxval <= 0 || maxval > 255) {
        return false;
    }
    if (static_cast<long long>(width) * height > 100000000LL) {
        return false;
    }

    Image result(width, height);
    if (binary) {
        if (pos >= static_cast<int>(bytes.size()) || !isSpace(bytes[pos])) {
            return false;
        }
        ++pos;
        const long long needed = static_cast<long long>(width) * height * 3;
        if (static_cast<long long>(bytes.size()) - pos < needed) {
            return false;
        }
        for (int y = 0; y < height; ++y) {
            for (int x = 0; x < width; ++x) {
                Colour c{scaleToByte(bytes[pos], maxval),
                         scaleToByte(bytes[pos + 1], maxval),
                         scaleToByte(bytes[pos + 2], maxval)};
                result.setPixel(x, y, c);
                pos += 3;
            }
        }
    } else {
        for (int y = 0; y < height; ++y) {
            for (int x = 0; x < width; ++x) {
                int r = 0;
                int g = 0;
                int b = 0;
                if (!readNumber(bytes, pos, r) || !readNumber(bytes, pos, g) ||
                    !readNumber(bytes, pos, b)) {
                    return false;
                }
                if (r > maxval || g > maxval || b > maxval) {
                    return false;
                }
                result.setPixel(x, y, Colour{scaleToByte(r, maxval),
                                             scaleToByte(g, maxval),
                                             scaleToByte(b, maxval)});
            }
        }
    }
    image = result;
    return true;
}
```

### Line by line

The first line of this part is line **91** of `image.h` (lines 1–89 are the class from Chapter 11, and line 90 is empty).

**Reading the file (lines 91–104)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 91 | `inline bool readFileBytes(const std::string& fileName, std::vector<std::uint8_t>& bytes) {` | Read a whole file into `bytes`. `inline` because it is a free function in a header (Section 12.9). Returns `true` if it worked. |
| 92 | `std::ifstream file(fileName, std::ios::binary \| std::ios::ate);` | Open for reading, binary mode, position at the end. |
| 93–95 | `if (!file) { return false; }` | The file does not exist or cannot be opened. |
| 96 | `const std::streamsize size = static_cast<std::streamsize>(file.tellg());` | The position at the end = the size (Section 12.3). |
| 97–99 | `if (size < 0) { return false; }` | `tellg` failed. Do not use a negative size. |
| 100 | `file.seekg(0, std::ios::beg);` | Go back to the beginning of the file. |
| 101 | `bytes.resize(size);` | Make room for exactly `size` bytes. (We checked it is not negative, so C++ can safely turn it into the vector's size type.) |
| 102 | `file.read(reinterpret_cast<char*>(bytes.data()), size);` | Read all bytes in one call, straight into the vector. |
| 103 | `return static_cast<bool>(file);` | `true` if all bytes were read. |
| 104 | `}` | End of `readFileBytes`. |

**Whitespace and comments (lines 106–123)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 106 | `inline bool isSpace(std::uint8_t c) {` | Is this byte whitespace? |
| 107 | `return c == ' ' \|\| c == '\t' \|\| c == '\n' \|\| c == '\r';` | Space (32), tab (9), line feed (10) or carriage return (13). Comparing a byte with `' '` compares it with 32. |
| 108 | `}` | End of `isSpace`. |
| 110 | `inline void skipSpaceAndComments(const std::vector<std::uint8_t>& bytes, int& pos) {` | Move `pos` past any whitespace and comments. `int& pos`: the function moves the **caller's** position. |
| 111 | `const int n = static_cast<int>(bytes.size());` | The number of bytes, as an `int`. |
| 112 | `while (pos < n) {` | Keep going until the end of the bytes (or until we stop on purpose). |
| 113–114 | `if (isSpace(bytes[pos])) { ++pos; }` | Whitespace: step over it. |
| 115 | `} else if (bytes[pos] == '#') {` | The start of a comment… |
| 116–118 | `while (pos < n && bytes[pos] != '\n') { ++pos; }` | …step forward until the end of the line. We stop **on** the `\n`; the next round of the outer loop skips it as whitespace. |
| 119–121 | `} else { return; }` | Anything else: it is real data. Stop and leave `pos` pointing at it. |
| 122–123 | `}` `}` | End of the loop and the function. |

**Reading a number (lines 125–140)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 125 | `inline bool readNumber(const std::vector<std::uint8_t>& bytes, int& pos, int& value) {` | Read one whole number, starting at `pos`. Put it into `value`. Move `pos` past it. |
| 126 | `skipSpaceAndComments(bytes, pos);` | First skip anything before the number. |
| 127 | `const int n = static_cast<int>(bytes.size());` | The number of bytes. |
| 128 | `if (pos >= n \|\| bytes[pos] < '0' \|\| bytes[pos] > '9') {` | If the file has ended, or the byte is not a digit… |
| 129 | `return false;` | …there is no number here. The file is broken. |
| 130 | `}` | End of the check. |
| 131 | `value = 0;` | Start building the number from 0. |
| 132 | `while (pos < n && bytes[pos] >= '0' && bytes[pos] <= '9') {` | While the byte is a digit… |
| 133 | `value = value * 10 + (bytes[pos] - '0');` | …shift the old value one decimal place to the left and add the new digit (Section 12.5). |
| 134–136 | `if (value > 1000000) { return false; }` | Too big to be real. Stop before an `int` could overflow. |
| 137 | `++pos;` | Move to the next byte. |
| 138 | `}` | End of the digit loop. `pos` now points at the first byte **after** the number. |
| 139 | `return true;` | We read a number. |
| 140 | `}` | End of `readNumber`. |

**Scaling (lines 142–147)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 142 | `inline std::uint8_t scaleToByte(int value, int maxval) {` | Change a value from 0–maxval into 0–255. |
| 143–145 | `if (value > maxval) { value = maxval; }` | Never allow a value above maxval (Section 12.8). |
| 146 | `return static_cast<std::uint8_t>((value * 255 + maxval / 2) / maxval);` | Scale with **integer rounding**: add half of the divisor before dividing. The result is always 0 to 255, so the cast is safe. |
| 147 | `}` | End of `scaleToByte`. |

**The loader: header (lines 149–171)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 149 | `inline bool loadPPM(const std::string& fileName, Image& image) {` | Load a PPM file into `image`. Returns `true` if it worked. If it fails, `image` is **not changed**. |
| 150 | `std::vector<std::uint8_t> bytes;` | The file's bytes will go here. |
| 151–153 | `if (!readFileBytes(fileName, bytes) \|\| bytes.size() < 2) { return false; }` | Read the file. Fail if it cannot be read, or is too short to hold a magic number. |
| 154–156 | `if (bytes[0] != 'P' \|\| (bytes[1] != '3' && bytes[1] != '6')) { return false; }` | The magic number must be `P3` or `P6`. |
| 157 | `const bool binary = (bytes[1] == '6');` | Remember which kind it is. |
| 158 | `int pos = 2;` | Start reading after the two magic bytes. |
| 159–161 | `int width = 0; int height = 0; int maxval = 0;` | The three header numbers. |
| 162–165 | `if (!readNumber(...width) \|\| !readNumber(...height) \|\| !readNumber(...maxval)) { return false; }` | Read them in order. If any one is missing, fail. (`\|\|` stops at the first failure.) |
| 166–168 | `if (width <= 0 \|\| height <= 0 \|\| maxval <= 0 \|\| maxval > 255) { return false; }` | Check their ranges (Section 12.6). |
| 169–171 | `if (static_cast<long long>(width) * height > 100000000LL) { return false; }` | Check the total number of pixels, in `long long` so it cannot overflow. `LL` makes the number 100,000,000 a `long long` too. |

**The loader: P6 pixels (lines 173–191)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 173 | `Image result(width, height);` | A new image of the right size. We fill this one, and only copy it into `image` at the very end. |
| 174 | `if (binary) {` | P6: raw bytes. |
| 175–177 | `if (pos >= ... \|\| !isSpace(bytes[pos])) { return false; }` | There must be a whitespace byte right after the maxval. |
| 178 | `++pos;` | Skip **exactly one** byte (Section 12.7). |
| 179 | `const long long needed = static_cast<long long>(width) * height * 3;` | How many pixel bytes must follow. |
| 180–182 | `if (static_cast<long long>(bytes.size()) - pos < needed) { return false; }` | Not enough bytes left? The file was cut short. Fail **before** reading past the end. |
| 183–184 | `for (int y ...) { for (int x ...) {` | Every pixel, row by row, top row first. |
| 185–187 | `Colour c{scaleToByte(bytes[pos], maxval), ...};` | Make a colour from the next three bytes, scaled to 0–255. |
| 188 | `result.setPixel(x, y, c);` | Store it. |
| 189 | `pos += 3;` | Move to the next pixel's bytes. |
| 190–191 | `}` `}` | End of the loops. |

**The loader: P3 pixels and the end (lines 192–213)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 192 | `} else {` | P3: text numbers. |
| 193–194 | `for (int y ...) { for (int x ...) {` | Every pixel. |
| 195–197 | `int r = 0; int g = 0; int b = 0;` | The three numbers of this pixel. |
| 198–201 | `if (!readNumber(...r) \|\| !readNumber(...g) \|\| !readNumber(...b)) { return false; }` | Read them. If the file runs out of numbers, fail. |
| 202–204 | `if (r > maxval \|\| g > maxval \|\| b > maxval) { return false; }` | A value bigger than maxval breaks the rules. |
| 205–207 | `result.setPixel(x, y, Colour{scaleToByte(r, maxval), ...});` | Scale and store. |
| 208–210 | `}` `}` `}` | End of the loops and of the P3 branch. |
| 211 | `image = result;` | Everything worked. **Now** copy the result into the caller's image. |
| 212 | `return true;` | Success. |
| 213 | `}` | End of `loadPPM`. |

Why fill `result` and copy at the end (line 211)? If the file fails halfway, we `return false` and the caller's `image` is **untouched**. A half-loaded image would be confusing.

---

## Code, part 2: a test program

File: `ch12/read_ppm.cpp`

```cpp
#include <iostream>
#include <fstream>
#include "image.h"

void printImage(const Image& img) {
    for (int y = 0; y < img.height(); ++y) {
        for (int x = 0; x < img.width(); ++x) {
            Colour c = img.getPixel(x, y);
            std::cout << "(" << static_cast<int>(c.r) << "," << static_cast<int>(c.g)
                      << "," << static_cast<int>(c.b) << ") ";
        }
        std::cout << "\n";
    }
}

int main() {
    {
        std::ofstream text("hand.ppm", std::ios::binary);
        text << "P3\n"
             << "# a 2 x 2 test image with maxval 15\n"
             << "2 2\n"
             << "15\n"
             << "15 0 0    0 15 0\n"
             << "0 0 15    5 5 5\n";
    }

    Image hand(1, 1);
    if (!loadPPM("hand.ppm", hand)) {
        std::cout << "could not load hand.ppm\n";
        return 1;
    }
    std::cout << "hand.ppm is " << hand.width() << " x " << hand.height() << ":\n";
    printImage(hand);

    Image first(3, 2);
    first.setPixel(0, 0, colours::red);
    first.setPixel(1, 0, colours::green);
    first.setPixel(2, 0, colours::blue);
    first.setPixel(0, 1, colours::yellow);
    first.setPixel(1, 1, colours::white);
    first.setPixel(2, 1, colours::black);
    first.savePPM("first_binary.ppm");

    Image back(1, 1);
    if (!loadPPM("first_binary.ppm", back)) {
        std::cout << "could not load first_binary.ppm\n";
        return 1;
    }
    std::cout << "\nfirst_binary.ppm is " << back.width() << " x " << back.height() << ":\n";
    printImage(back);

    for (int y = 0; y < back.height(); ++y) {
        for (int x = 0; x < back.width(); ++x) {
            Colour c = back.getPixel(x, y);
            Colour negative{static_cast<std::uint8_t>(255 - c.r),
                            static_cast<std::uint8_t>(255 - c.g),
                            static_cast<std::uint8_t>(255 - c.b)};
            back.setPixel(x, y, negative);
        }
    }
    back.savePPM("first_negative.ppm");
    std::cout << "\nnegative:\n";
    printImage(back);

    Image missing(1, 1);
    bool loaded = loadPPM("no_such_file.ppm", missing);
    std::cout << "\nloading a missing file: " << (loaded ? "worked?!" : "failed, as expected") << "\n";
    return 0;
}
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–2 | `#include <iostream>` / `<fstream>` | Printing, and `std::ofstream` to write a test file by hand. |
| 3 | `#include "image.h"` | Our library, now with `loadPPM`. |
| 5 | `void printImage(const Image& img) {` | Print every pixel of a (small!) image as numbers. `const Image&`: read only, no copy. |
| 6–7 | `for (int y ...) { for (int x ...) {` | Every pixel, row by row. |
| 8 | `Colour c = img.getPixel(x, y);` | Read the pixel. |
| 9–10 | `std::cout << "(" << static_cast<int>(c.r) << ...` | Print it as `(r,g,b)`, with casts so the bytes print as numbers. |
| 11–12 | `}` `std::cout << "\n";` | End of a row: new line. |
| 13–14 | `}` `}` | End of `printImage`. |
| 16 | `int main() {` | The program starts here. |
| 17 | `{` | A block, so the file is closed at its `}` (Chapter 7). |
| 18 | `std::ofstream text("hand.ppm", std::ios::binary);` | Make a test file. |
| 19 | `text << "P3\n"` | The magic number. |
| 20 | `<< "# a 2 x 2 test image with maxval 15\n"` | A **comment** line, to test `skipSpaceAndComments`. |
| 21 | `<< "2 2\n"` | width 2, height 2. |
| 22 | `<< "15\n"` | maxval **15**, to test scaling. |
| 23 | `<< "15 0 0    0 15 0\n"` | Row 0: full red, full green. Extra spaces between pixels test the whitespace rules. |
| 24 | `<< "0 0 15    5 5 5\n";` | Row 1: full blue, and a grey of 5 out of 15. |
| 25 | `}` | The file is closed here. |
| 27 | `Image hand(1, 1);` | An image to load into. Its size does not matter; `loadPPM` replaces it. |
| 28–31 | `if (!loadPPM("hand.ppm", hand)) { ...; return 1; }` | Load the file. Stop if it fails. |
| 32 | `std::cout << "hand.ppm is " << hand.width() << " x " << hand.height() << ":\n";` | Print the size we read: it should be 2 × 2. |
| 33 | `printImage(hand);` | Print the pixels, scaled to 0–255. |
| 35–41 | `Image first(3, 2); first.setPixel(...)` × 6 | Our usual 3 × 2 picture. |
| 42 | `first.savePPM("first_binary.ppm");` | Save it as P6. |
| 44 | `Image back(1, 1);` | Another image to load into. |
| 45–48 | `if (!loadPPM("first_binary.ppm", back)) { ...; return 1; }` | The **round trip**: load what we just saved. |
| 49–50 | `std::cout << ...; printImage(back);` | Print it. It must be the same six colours. |
| 52–53 | `for (int y ...) { for (int x ...) {` | Every pixel of the loaded image. |
| 54 | `Colour c = back.getPixel(x, y);` | Read it. |
| 55–57 | `Colour negative{static_cast<std::uint8_t>(255 - c.r), ...};` | Its **complement** (Chapter 5, Section 5.8): 255 minus each channel. |
| 58 | `back.setPixel(x, y, negative);` | Write it back. **Open → change → save** in action. |
| 59–60 | `}` `}` | End of the loops. |
| 61 | `back.savePPM("first_negative.ppm");` | Save the changed image. |
| 62–63 | `std::cout << "\nnegative:\n"; printImage(back);` | Print the negative. |
| 65 | `Image missing(1, 1);` | One more image. |
| 66 | `bool loaded = loadPPM("no_such_file.ppm", missing);` | Try to load a file that does not exist. |
| 67 | `std::cout << ... (loaded ? "worked?!" : "failed, as expected") << "\n";` | It must fail, quietly, with no crash. |
| 68 | `return 0;` | The program finished with no problem. |
| 69 | `}` | End of `main`. |

Compile it as in Chapter 11:

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common read_ppm.cpp -o read_ppm
```

### What you should see

```
hand.ppm is 2 x 2:
(255,0,0) (0,255,0) 
(0,0,255) (85,85,85) 

first_binary.ppm is 3 x 2:
(255,0,0) (0,255,0) (0,0,255) 
(255,255,0) (255,255,255) (0,0,0) 

negative:
(0,255,255) (255,0,255) (255,255,0) 
(0,0,255) (0,0,0) (255,255,255) 

loading a missing file: failed, as expected
```

Check the results:
- In `hand.ppm`, 15 (out of 15) became **255**, and 5 became **85** (Section 12.8).
- The round trip gave back **exactly** the six colours we saved. Our P6 writer and reader agree.
- The negative swapped red ↔ cyan, green ↔ magenta, blue ↔ yellow, yellow ↔ blue, white ↔ black (Chapter 5).

Open `first_negative.ppm` in your viewer: cyan, magenta, yellow / blue, black, white.

---

## Small examples

### Example 1 — Make a negative of any picture

Combine `loadPPM` and the negative loop into a small tool:

```cpp
Image img(1, 1);
if (loadPPM("photo.ppm", img)) {
    for (int y = 0; y < img.height(); ++y) {
        for (int x = 0; x < img.width(); ++x) {
            Colour c = img.getPixel(x, y);
            img.setPixel(x, y, Colour{static_cast<std::uint8_t>(255 - c.r),
                                      static_cast<std::uint8_t>(255 - c.g),
                                      static_cast<std::uint8_t>(255 - c.b)});
        }
    }
    img.savePPM("photo_negative.ppm");
}
```

Try it on `gradient.ppm` from Chapter 11. The dark blue corner becomes light yellow, and so on.

💡 **Tip:** Want to try it on a real photo? Many image programs (GIMP, IrfanView, XnView) can **export** a photo as PPM. Choose the "binary" or "raw" option to get P6.

### Example 2 — A file that is cut short

Make a P6 file that is missing its last byte:

```cpp
std::ofstream bad("short.ppm", std::ios::binary);
bad << "P6\n2 1\n255\n";
bad.put(static_cast<char>(255));
bad.put(0);
bad.put(0);
bad.put(0);
bad.put(static_cast<char>(255));   // only 5 pixel bytes, but 2 × 1 × 3 = 6 are needed
```

> bytes after the header = 5
> needed = 6
> 5 < 6 → `loadPPM` returns **false** (line 180)

Without that check, the loader would read `bytes[pos + 2]` past the end of the vector.

### Example 3 — Comments in odd places

This is a valid P3 file:

```
P3 # colour image
2 # width
1 # height
255 # maxval
255 255 255 # white
0 0 0 # black
```

Our parser loads it fine: `readNumber` calls `skipSpaceAndComments` before **every** number, so comments can appear anywhere between numbers.

### Example 4 — Integer rounding for other numbers

The trick from Section 12.8 works for any division:

> 7 ÷ 2 = 3.5 → rounded should be 4: (7 + 1) ÷ 2 = 8 ÷ 2 = **4** ✓
> 10 ÷ 3 = 3.33 → rounded should be 3: (10 + 1) ÷ 3 = 11 ÷ 3 = **3** ✓
> 11 ÷ 3 = 3.67 → rounded should be 4: (11 + 1) ÷ 3 = 12 ÷ 3 = **4** ✓

(Here b ÷ 2 is 1 for b = 2 and b = 3, using integer division.)

---

## Common mistakes

⚠️ **Skipping all whitespace after the P6 maxval.** Pixel bytes with the value 9, 10, 13 or 32 get eaten as "whitespace". The image shifts. Skip **exactly one** byte.

⚠️ **No check for "enough bytes left".** A short file makes the loader read past the end of the vector.

⚠️ **Computing `width * height` in `int`.** A broken header can make it overflow. Use `long long`.

⚠️ **Forgetting `inline`.** It works with one `.cpp` file, and breaks with "multiple definition" the day you have two.

⚠️ **Changing the caller's image before the load is finished.** On failure, they get a half-loaded picture. Fill a local `result` and copy at the end.

⚠️ **Opening in text mode.** On Windows, `0D 0A` in the pixel data would turn into `0A`, and the file would look one byte shorter.

---

## Practice

🏋️ **1.** Follow `readNumber` by hand on the bytes `"  42x"` starting at pos = 0. What is `value`, what is `pos` at the end, and what does it return?

🏋️ **2.** What does `readNumber` return for the bytes `"abc"`?

🏋️ **3.** Scale these values to 0–255 with the integer rounding trick: value 1 with maxval 3; value 2 with maxval 3; value 100 with maxval 100.

🏋️ **4.** A P6 file says `P6\n10 10\n255\n` and is 300 bytes long. Does `loadPPM` accept it? Why or why not?

🏋️ **5.** Write a program that loads `gradient.ppm` (Chapter 11), swaps the red and blue channels of every pixel, and saves it as `swapped.ppm`. What colour is the top-right corner now?

🏋️ **6.** Write a P3 file by hand with maxval 1 (Chapter 8, Section 8.7), load it with `loadPPM`, and print it. What values do you get?

🏋️ **7.** Write a small "PPM info" program that loads a file named on the command line and prints its width and height. (Hint: `int main(int argc, char* argv[])`, and `argv[1]` is the first argument.)

---

## Answers

**1.**
> skip: pos 0 is space → 1, pos 1 is space → 2, pos 2 is `'4'` → stop.
> `'4'`: value = 0 × 10 + 4 = 4, pos = 3
> `'2'`: value = 4 × 10 + 2 = 42, pos = 4
> `'x'`: not a digit → stop
> **value = 42, pos = 4, returns true.** (`pos` points at the `x`. The next `readNumber` would fail there.)

**2.** After skipping (nothing to skip), the first byte is `'a'`, not a digit. It returns **false**.

**3.**
> 1 with maxval 3: (1 × 255 + 3 ÷ 2) ÷ 3 = (255 + 1) ÷ 3 = 256 ÷ 3 = 85.33 → **85**
> 2 with maxval 3: (510 + 1) ÷ 3 = 511 ÷ 3 = 170.33 → **170**
> 100 with maxval 100: (25,500 + 50) ÷ 100 = 25,550 ÷ 100 = 255.5 → **255**

**4.**
> header = 3 + 6 + 4 = 13 bytes (`P6\n`, `10 10\n`, `255\n`)
> pos after the one whitespace = 13
> bytes left = 300 − 13 = 287
> needed = 10 × 10 × 3 = 300
> 287 < 300 → **No**, it is rejected. The file is 13 bytes short. A correct file would be 313 bytes (Chapter 9, Example 2).

**5.**

```cpp
Image img(1, 1);
if (loadPPM("gradient.ppm", img)) {
    for (int y = 0; y < img.height(); ++y) {
        for (int x = 0; x < img.width(); ++x) {
            Colour c = img.getPixel(x, y);
            img.setPixel(x, y, Colour{c.b, c.g, c.r});
        }
    }
    img.savePPM("swapped.ppm");
}
```

> top-right was (255, 0, 128). Swapped: (128, 0, 255) — a **violet**.

(This red ↔ blue swap is exactly what we must do for BMP files in Chapter 36, which store pixels as B, G, R.)

**6.** For example:

```
P3
2 1
1
1 0 1   0 1 1
```

`loadPPM` scales 1 → (1 × 255 + 0) ÷ 1 = 255 and 0 → 0. The output is `(255,0,255) (0,255,255)`: magenta and cyan.

**7.**

```cpp
#include <iostream>
#include "image.h"

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "use: ppminfo file.ppm\n";
        return 1;
    }
    Image img(1, 1);
    if (!loadPPM(argv[1], img)) {
        std::cout << "not a valid PPM file\n";
        return 1;
    }
    std::cout << argv[1] << ": " << img.width() << " x " << img.height() << "\n";
    return 0;
}
```

Run it as `ppminfo gradient.ppm` → `gradient.ppm: 256 x 256`.

---

## Summary

🧠 Reading lets us **open → change → save**, and **round-trip** test our writers.

🧠 Read a whole file fast: `ate` + `tellg` (size), `seekg` (back to start), `read` (all at once).

🧠 A parser walks through the bytes with a **position**, skipping whitespace and `#` comments.

🧠 Digits → number: **value = value × 10 + (byte − '0')**. Stop early if it gets too big.

🧠 **Validate everything**: magic, ranges, total size (in `long long`), and "enough bytes left".

🧠 P6: after maxval, skip **exactly one** byte.

🧠 Scale to 0–255 with integer rounding: **(value × 255 + maxval / 2) / maxval**.

🧠 Free functions in a header must be **`inline`**.

---

## Next chapter

**Part 2 is complete!** We can write and read real image files, in colour, grey, and black-and-white, with our own `Image` class. In **Part 3** we study the **mathematics of colour**. Chapter 13 starts with the most useful idea in all of graphics: **linear interpolation** — how to find any colour "part of the way" between two others, and make perfect gradients of any size.
