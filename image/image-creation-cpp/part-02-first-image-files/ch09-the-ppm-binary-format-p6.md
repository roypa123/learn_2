# Chapter 9 — The PPM Binary Format (P6)

> **Part 2 · Chapter 9 of 82**
> **You need:** Chapters 1–8 · **You will make:** `first_binary.ppm`, `gradient_p6.ppm`, and a size comparison of P3 and P6

---

## What you will learn

- Why text is a slow and wasteful way to store pixels.
- The exact rules of the **P6** format: a text header, then **raw bytes**.
- The **one-whitespace rule** after the maxval, and the bug it causes if you break it.
- How to read a P6 file with a hex dump, byte by byte.
- How to write the whole pixel buffer with **one** `write` call.
- How to find the **size of a file** in C++.
- What P6 does when maxval is bigger than 255 (two bytes per value, **big-endian**).

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **raw bytes** | Bytes written exactly as they are in memory, not turned into text. |
| **binary format** | A file format that stores numbers as raw bytes. |
| **overhead** | Extra bytes that are not the real data (like spaces and digits for the same number). |
| **file position** | The place in a file where the next read or write happens. |
| **big-endian** | Storing a number of several bytes with the **biggest** (most important) byte **first**. |
| **little-endian** | Storing a number of several bytes with the **smallest** byte **first**. |
| **most significant byte** | The byte of a number that is worth the most (the "high" byte). |

---

## 9.1 The problem with text

In Chapter 8, our 256 × 256 gradient was **730,383 bytes** as P3. But the pixel buffer in memory was only **196,608 bytes**. Where do the extra bytes come from?

🔢 **Maths: the number 255, as text and as a raw byte**

> as text: the characters `2`, `5`, `5` and a space → **4 bytes** (`32 35 35 20`)
> as a raw byte: just `FF` → **1 byte**

📖 **New word: overhead** — extra bytes that are not the real data.

Text wastes space in two ways:
1. One number takes **1 to 3 digits** instead of exactly 1 byte.
2. Every number needs **whitespace** after it.

Text is also **slow**:
- Writing: the program must turn each byte into digits (255 → `'2'`, `'5'`, `'5'`).
- Reading: the viewer must turn digits back into a number (Chapter 8, Section 8.4).

For a big photo with millions of pixels, this is millions of small steps, in both directions.

📖 **New word: raw bytes** — bytes written exactly as they are in memory.

📖 **New word: binary format** — a format that stores numbers as raw bytes.

What if we write the pixel buffer **as it is**, as raw bytes, the way we did with `bytes.bin` in Chapter 7? That is the **P6** format.

---

## 9.2 The rules of P6

P6 has the **same header** as P3, with one change to the magic number. Only the **pixel data** is different.

1. The magic number: **`P6`**.
2. Whitespace.
3. The width, as text digits.
4. Whitespace.
5. The height, as text digits.
6. Whitespace.
7. The maxval, as text digits.
8. **Exactly one** whitespace character (usually `\n`).
9. Then **width × height × 3 raw bytes**: R G B of the first pixel, R G B of the second pixel, and so on — **row-major, top row first**.

So the header is still **text**, and the pixels are **binary**.

```
┌──────────────────────────────────┐
│ P6\n3 2\n255\n                    │  ← text header (11 bytes)
├──────────────────────────────────┤
│ FF 00 00  00 FF 00  00 00 FF     │  ← raw bytes, row 0
│ FF FF 00  FF FF FF  00 00 00     │  ← raw bytes, row 1
└──────────────────────────────────┘
```

There are **no spaces** between the pixel bytes. There are **no new lines** at the end of rows. The bytes just follow one another. The viewer knows where each row ends, because it knows the width from the header.

🔢 **Maths: where does row 1 start?**

> header = 11 bytes (offsets 0 to 10)
> row size = width × 3 = 3 × 3 = 9 bytes (Chapter 6)
> row 0 starts at offset 11
> row 1 starts at offset 11 + 9 = **20**

🧠 **Remember:** P6 = the P3 header with `P6`, then **exactly one** whitespace, then the pixel buffer, byte for byte.

---

## 9.3 The one-whitespace rule

In P3, any amount of whitespace was fine everywhere. In P6, the whitespace **after the maxval** must be **exactly one character**.

Why? Think like the viewer. After it reads the digits `255`, it skips **one** character, and then the next byte is the **red of the first pixel**. But that red byte could be **any** value — including 10 (`\n`) or 32 (space)! If the viewer skipped "all whitespace", it would also skip a dark-red pixel whose red value happens to be 10. So the rule must be "skip exactly one".

### The bug: an extra new line

Say we wrote the header with **two** new lines by mistake:

```cpp
file << "P6\n3 2\n255\n\n";   // WRONG: two \n after 255
```

```
correct:  ... 32 35 35 0A | FF 00 00 00 FF 00 ...
wrong:    ... 32 35 35 0A | 0A FF 00 00 00 FF 00 ...
                            ↑ the viewer thinks this is the first red!
```

🔢 **Maths: what the viewer now sees**

> pixel (0, 0): R = 0A (10), G = FF, B = 00 → (10, 255, 0) — green, not red!
> pixel (1, 0): R = 00, G = 00, B = FF → (0, 0, 255) — blue, not green!
> pixel (2, 0): R = 00, G = 00, B = 00 → black, not blue!

Every pixel is **shifted by one byte**. Red becomes green, green becomes blue. And the last byte of the file is missing, so the viewer may complain that the file is too short.

This is the same kind of bug as the Windows text-mode bug in Chapter 7. **One extra byte in the wrong place breaks everything after it.**

⚠️ **Careful:** Comments (`#`) are allowed in the P6 header **before** the maxval. But after the maxval, there must be exactly one whitespace and then the data. To be safe, we never write comments.

---

## 9.4 Our first P6 file, byte by byte

Here is the full hex dump of `first_binary.ppm` (the same 3 × 2 picture as Chapter 8):

```
0000:  50 36 0A 33 20 32 0A 32 35 35 0A FF 00 00 00 FF
0010:  00 00 00 FF FF FF 00 FF FF FF 00 00 00
```

Let us split it into parts:

| Offsets | Bytes | Meaning |
|---|---|---|
| 0–1 | `50 36` | `P6` — the magic number |
| 2 | `0A` | whitespace |
| 3 | `33` | `3` — width |
| 4 | `20` | whitespace (space) |
| 5 | `32` | `2` — height |
| 6 | `0A` | whitespace |
| 7–9 | `32 35 35` | `255` — maxval |
| 10 | `0A` | **the one** whitespace |
| 11–13 | `FF 00 00` | pixel (0, 0): red |
| 14–16 | `00 FF 00` | pixel (1, 0): green |
| 17–19 | `00 00 FF` | pixel (2, 0): blue |
| 20–22 | `FF FF 00` | pixel (0, 1): yellow |
| 23–25 | `FF FF FF` | pixel (1, 1): white |
| 26–28 | `00 00 00` | pixel (2, 1): black |

🔢 **Maths: the size of first_binary.ppm**

> header = 11 bytes
> pixels = 3 × 2 × 3 = 18 bytes
> total = 11 + 18 = **29 bytes**

As P3, the same picture was 65 bytes (Chapter 8). P6 is **less than half**.

🔢 **Maths: the offset of any byte in a P6 file**

> offset = headerSize + (y × width + x) × 3 + channel

Check pixel (1, 1), green (channel 1), with headerSize 11 and width 3:

> (1 × 3 + 1) × 3 + 1 = 4 × 3 + 1 = 13
> offset = 11 + 13 = **24**

In the table, offsets 23–25 are white `FF FF FF`, so offset 24 is its green: `FF` ✓.

This is just the Chapter 6 formula, plus the header size. The file **is** the pixel buffer, with a header in front.

---

## 9.5 Writing P6 in C++

The header is text, so we write it with `<<`, just like in Chapter 8:

```cpp
file << "P6\n" << width << " " << height << "\n255\n";
```

Count the whitespace after `255`: exactly one `\n` ✓.

Then the pixels. Our buffer is already in the right order: row-major, top row first, R G B (Chapter 6). So we send the **whole buffer** with **one** `write` call (Chapter 7):

```cpp
file.write(reinterpret_cast<const char*>(pixels.data()),
           static_cast<std::streamsize>(pixels.size()));
```

No loops. No casts to `int`. No spaces. One call.

⚠️ **Careful:** `std::ios::binary` is **required** here — not just a good habit like in Chapter 8. The pixel data is raw bytes, and any byte with the value 10 would become two bytes in text mode on Windows (Chapter 7). A dark pixel like (10, 10, 10) would break the whole image.

### Why one `write` is fast

`write` hands one block of memory to the system. The system copies it to the disk in big pieces. Compare this with P3, where for **each** channel the program must:

1. turn the byte into an `int`,
2. turn the `int` into 1 to 3 digit characters,
3. add a space or new line.

For a 4K image (about 8.3 million pixels, Chapter 2), that is about **25 million** numbers to turn into text. P6 skips all of that.

---

## 9.6 Finding the size of a file

📖 **New word: file position** — the place in a file where the next read or write happens. Like a bookmark.

To prove that P6 is smaller, we want our program to print the file sizes. Here is a short way to get the size of a file:

```cpp
std::ifstream file(fileName, std::ios::binary | std::ios::ate);
long long size = static_cast<long long>(file.tellg());
```

| Part | Meaning |
|---|---|
| `std::ios::binary` | Open in binary mode (so the size is the real number of bytes). |
| `\|` | Join two options together. (This is the bitwise OR from Chapter 4! Each option is one bit.) |
| `std::ios::ate` | "**at end**": after opening, put the file position at the **end** of the file. |
| `file.tellg()` | "**tell** me the position for **g**etting (reading)". At the end of the file, the position is the number of bytes in it. |

🔢 **Maths: why the position at the end is the size**

> A file with 29 bytes has offsets 0 to 28.
> The position "after the last byte" is 29.
> So the position at the end = the size = 29.

`tellg` returns a special type (`std::streampos`). We change it into a `long long`, a normal big integer. A file can be bigger than an `int` can hold (more than about 2 billion bytes), so `long long` is the safe choice.

---

## 9.7 How much smaller is P6?

🔢 **Maths: the gradient as P6**

> header `P6\n256 256\n255\n` = 3 + 8 + 4 = 15 bytes
> pixels = 256 × 256 × 3 = 196,608 bytes
> total = 15 + 196,608 = **196,623 bytes**

Compare:

| Format | Size of the 256 × 256 gradient |
|---|---|
| P3 (text) | 730,383 bytes |
| P6 (binary) | 196,623 bytes |

> 730,383 ÷ 196,623 ≈ 3.7

So P6 is about **3.7 times smaller** here. And the P6 size does **not** depend on the colours: it is always header + width × height × 3. (The P3 size depends on how many digits each value has. A black image is smaller as P3 than a white one!)

🔢 **Maths: the P6 size of a Full HD image**

> header `P6\n1920 1080\n255\n` = 3 + 10 + 4 = 17 bytes
> pixels = 1,920 × 1,080 × 3 = 6,220,800 bytes (Chapter 4)
> total = **6,220,817 bytes** (about 6.2 MB)

That is still big. P6 has **no compression**. In Part 6, PNG will make many images much smaller — but P6 remains the simplest, fastest way to save a picture.

---

## 9.8 Big maxval: two bytes per value

The maxval in P6 can also be bigger than 255, up to 65,535 (Chapter 8, Section 8.7). Then one byte is not enough for one channel. Each value takes **two bytes**.

📖 **New word: most significant byte** — the byte of a number that is worth the most. For 1,000 = `0x03E8`, the most significant byte is `03`.

📖 **New word: big-endian** — writing the **most significant byte first**. Like we write decimal numbers: the biggest digit is on the left.

📖 **New word: little-endian** — writing the **least significant byte first**. "Backwards" from how we write numbers.

P6 uses **big-endian**.

🔢 **Maths: the value 1,000 with maxval 65,535**

> 1,000 = 3 × 256 + 232 (Chapter 4, Example 3)
> high byte = 3 = `0x03`, low byte = 232 = `0xE8`
> big-endian (P6): `03 E8`
> little-endian: `E8 03`

In C++:

```cpp
file.put(static_cast<char>((value >> 8) & 0xFF));   // high byte first
file.put(static_cast<char>(value & 0xFF));          // then low byte
```

This is the "split a number into bytes" recipe from Chapter 4, written high byte first.

We will **not** use 16-bit PPM files in this book, because our buffer holds one byte per channel. But you now know what **endianness** is. In Chapter 36, the BMP format uses **little-endian** — the opposite order — for its header numbers. (Remember Chapter 4, Practice 8: `78 56 34 12`.)

🧠 **Remember:** **Big-endian** = biggest byte first (P6, PNG). **Little-endian** = smallest byte first (BMP, and most PCs' memory).

---

## Code

File: `ch09/ppm_p6.cpp`

```cpp
#include <iostream>
#include <fstream>
#include <cstdint>
#include <string>
#include <vector>

bool isInside(int x, int y, int width, int height) {
    return x >= 0 && x < width && y >= 0 && y < height;
}

void setPixel(std::vector<std::uint8_t>& pixels, int width, int height,
              int x, int y, std::uint8_t r, std::uint8_t g, std::uint8_t b) {
    if (!isInside(x, y, width, height)) {
        return;
    }
    int i = (y * width + x) * 3;
    pixels[i]     = r;
    pixels[i + 1] = g;
    pixels[i + 2] = b;
}

bool writePPM_P3(const std::string& fileName, int width, int height,
                 const std::vector<std::uint8_t>& pixels) {
    std::ofstream file(fileName, std::ios::binary);
    if (!file) {
        return false;
    }
    file << "P3\n" << width << " " << height << "\n255\n";
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            int i = (y * width + x) * 3;
            file << static_cast<int>(pixels[i]) << " "
                 << static_cast<int>(pixels[i + 1]) << " "
                 << static_cast<int>(pixels[i + 2]) << "\n";
        }
        file << "\n";
    }
    return static_cast<bool>(file);
}

bool writePPM_P6(const std::string& fileName, int width, int height,
                 const std::vector<std::uint8_t>& pixels) {
    std::ofstream file(fileName, std::ios::binary);
    if (!file) {
        return false;
    }
    file << "P6\n" << width << " " << height << "\n255\n";
    file.write(reinterpret_cast<const char*>(pixels.data()),
               static_cast<std::streamsize>(pixels.size()));
    return static_cast<bool>(file);
}

long long fileSize(const std::string& fileName) {
    std::ifstream file(fileName, std::ios::binary | std::ios::ate);
    if (!file) {
        return -1;
    }
    return static_cast<long long>(file.tellg());
}

int main() {
    const int width = 3;
    const int height = 2;
    std::vector<std::uint8_t> pixels(width * height * 3, 0);
    setPixel(pixels, width, height, 0, 0, 255, 0, 0);
    setPixel(pixels, width, height, 1, 0, 0, 255, 0);
    setPixel(pixels, width, height, 2, 0, 0, 0, 255);
    setPixel(pixels, width, height, 0, 1, 255, 255, 0);
    setPixel(pixels, width, height, 1, 1, 255, 255, 255);
    setPixel(pixels, width, height, 2, 1, 0, 0, 0);

    const int size = 256;
    std::vector<std::uint8_t> gradient(size * size * 3, 0);
    for (int y = 0; y < size; ++y) {
        for (int x = 0; x < size; ++x) {
            setPixel(gradient, size, size, x, y,
                     static_cast<std::uint8_t>(x),
                     static_cast<std::uint8_t>(y),
                     128);
        }
    }

    bool ok = writePPM_P6("first_binary.ppm", width, height, pixels);
    ok = ok && writePPM_P3("gradient_p3.ppm", size, size, gradient);
    ok = ok && writePPM_P6("gradient_p6.ppm", size, size, gradient);
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }

    std::cout << "first_binary.ppm: " << fileSize("first_binary.ppm") << " bytes\n";
    std::cout << "gradient_p3.ppm:  " << fileSize("gradient_p3.ppm") << " bytes\n";
    std::cout << "gradient_p6.ppm:  " << fileSize("gradient_p6.ppm") << " bytes\n";
    return 0;
}
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–5 | `#include ...` | Printing, files, bytes, text, vectors. Same as Chapter 8. |
| 7–9 | `bool isInside(...)` | Same as Chapter 3. |
| 11–20 | `void setPixel(...)` | Same as Chapter 6. |
| 22–39 | `bool writePPM_P3(...)` | Same as Chapter 8. The only change: line 28 writes the whole header with **one** `<<` chain instead of three lines. The bytes are exactly the same. We keep this function only to compare sizes. |
| 41 | `bool writePPM_P6(const std::string& fileName, int width, int height,` | Our new function: save a buffer as P6. Same inputs as `writePPM_P3`… |
| 42 | `const std::vector<std::uint8_t>& pixels) {` | …so you can swap one for the other with no other change. |
| 43 | `std::ofstream file(fileName, std::ios::binary);` | Open in **binary mode**. Here it is **required** (Section 9.5). |
| 44–46 | `if (!file) { return false; }` | Stop if the file could not open. |
| 47 | `file << "P6
" << width << " " << height << "
255
";` | The text header: `P6`, new line, width, space, height, new line, `255`, and **exactly one** new line (Section 9.3). |
| 48 | `file.write(reinterpret_cast<const char*>(pixels.data()),` | Write the **whole** pixel buffer in one go, starting at its first byte (Chapter 7, Section 7.6)… |
| 49 | `static_cast<std::streamsize>(pixels.size()));` | …all `width × height × 3` bytes of it. |
| 50 | `return static_cast<bool>(file);` | `true` if everything was written. |
| 51 | `}` | End of `writePPM_P6`. |
| 53 | `long long fileSize(const std::string& fileName) {` | A function that returns the size of a file in bytes, or −1 if it cannot open it. |
| 54 | `std::ifstream file(fileName, std::ios::binary \| std::ios::ate);` | Open for reading, in binary mode, with the position **at the end** (Section 9.6). |
| 55–57 | `if (!file) { return -1; }` | If the file does not exist, give back −1. A real size is never negative, so −1 clearly means "problem". |
| 58 | `return static_cast<long long>(file.tellg());` | The position at the end **is** the size. Change it into a `long long` and give it back. |
| 59 | `}` | End of `fileSize`. |
| 61 | `int main() {` | The program starts here. |
| 62–64 | `const int width = 3; ... pixels(...)` | The same 3 × 2 buffer as Chapter 8, all black. |
| 65–70 | `setPixel(...)` × 6 | The same six colours: red, green, blue / yellow, white, black. |
| 72–81 | `const int size = 256; ... }` | The same 256 × 256 gradient as Chapter 8: red = x, green = y, blue = 128. |
| 83 | `bool ok = writePPM_P6("first_binary.ppm", width, height, pixels);` | Save the small picture as P6. `ok` remembers if it worked. |
| 84 | `ok = ok && writePPM_P3("gradient_p3.ppm", size, size, gradient);` | Save the gradient as P3. With `&&`, this only runs if `ok` is still `true`, and `ok` stays `true` only if this also works. |
| 85 | `ok = ok && writePPM_P6("gradient_p6.ppm", size, size, gradient);` | Save the gradient as P6, the same way. |
| 86 | `if (!ok) {` | If **any** of the three failed… |
| 87 | `std::cout << "could not write the files
";` | …say so… |
| 88 | `return 1;` | …and stop with "problem". |
| 89 | `}` | End of the check. |
| 91 | `std::cout << "first_binary.ppm: " << fileSize("first_binary.ppm") << " bytes
";` | Print the size of the small P6 file. |
| 92 | `std::cout << "gradient_p3.ppm:  " << ...` | Print the size of the P3 gradient. |
| 93 | `std::cout << "gradient_p6.ppm:  " << ...` | Print the size of the P6 gradient. |
| 94 | `return 0;` | The program finished with no problem. |
| 95 | `}` | End of `main`. |

### What you should see

```
first_binary.ppm: 29 bytes
gradient_p3.ppm:  730383 bytes
gradient_p6.ppm:  196623 bytes
```

These match our maths in Sections 9.4 and 9.7, and in Chapter 8 (Section 8.8) — exactly.

Open `first_binary.ppm` and `gradient_p6.ppm` in your viewer. They look **exactly the same** as the P3 versions from Chapter 8. Only the file is different, not the picture.

Now try to open `first_binary.ppm` in a **text editor**. You will see `P6`, `3 2`, `255`, and then strange characters. Those are the raw pixel bytes. A text editor tries to show them as letters, and most of them are not printable letters. This is normal for a binary file.

---

## Small examples

### Example 1 — Change P3 into P6 in one word

Because `writePPM_P3` and `writePPM_P6` take the **same inputs**, changing your program from P3 to P6 is one edit:

```cpp
writePPM_P3("picture.ppm", w, h, img);   // before
writePPM_P6("picture.ppm", w, h, img);   // after
```

From now on, **we use P6** for all our images, until we write BMP and PNG in Part 6.

### Example 2 — A P6 file has a predictable size

For any P6 image with maxval 255:

> size = header + width × height × 3

| Image | header | pixels | total |
|---|---|---|---|
| 3 × 2 | `P6\n3 2\n255\n` = 11 | 18 | 29 |
| 10 × 10 | `P6\n10 10\n255\n` = 13 | 300 | 313 |
| 100 × 50 | `P6\n100 50\n255\n` = 14 | 15,000 | 15,014 |

🔢 Counting the header of 100 × 50: `P6\n` = 3, `100 50\n` = 7, `255\n` = 4 → 3 + 7 + 4 = 14.

If your file size does **not** match this, something is wrong: maybe text mode, maybe an extra space, maybe a wrong loop.

### Example 3 — Make the bug on purpose

Change line 47 to write **two** new lines after 255:

```cpp
file << "P6\n" << width << " " << height << "\n255\n\n";
```

Open `first_binary.ppm` again. Instead of red, green, blue / yellow, white, black, you will see colours like green, blue, black / … (Section 9.3). The file is now 30 bytes. Seeing a bug on purpose helps you recognise it later. **Remember to change it back!**

### Example 4 — Find a pixel by its offset

In `gradient_p6.ppm`, which pixel and channel is at offset 1,000?

> offset in pixel data = 1,000 − 15 (header) = 985
> pixel index = 985 ÷ 3 = 328, remainder 1 → channel 1 (green)
> y = 328 ÷ 256 = 1, x = 328 % 256 = 72
> So it is the **green** of pixel **(72, 1)**.
> Green = y = **1**. So the byte at offset 1,000 is `01`.

---

## Common mistakes

⚠️ **No `std::ios::binary`.** On Windows, every byte 10 becomes `0D 0A`. Dark images break most often (they have many small values).

⚠️ **More than one whitespace after the maxval.** Every pixel shifts by one byte. Red becomes green.

⚠️ **Writing the pixels with `<<` and `static_cast<int>`.** That makes **text** digits — you have made a P3 body with a P6 header. The viewer reads the digit characters as raw bytes and shows a mess.

⚠️ **Writing `P3` in the header of a binary file** (or `P6` on a text file). The magic number must match the data.

⚠️ **Adding spaces or new lines between rows.** P6 rows follow each other directly. Extra bytes shift everything.

⚠️ **Expecting P6 to be small.** P6 is smaller than P3, but it has **no compression**. A Full HD P6 file is about 6.2 MB.

---

## Practice

🏋️ **1.** What is the exact size of a 640 × 480 P6 file? Count the header byte by byte.

🏋️ **2.** A P6 file is 3 × 3. Its header is 11 bytes. At which offset does the **blue** byte of pixel (2, 1) sit?

🏋️ **3.** Write the full hex dump of a 2 × 1 P6 file with pixels white and magenta.

🏋️ **4.** A P6 file has the header `P6\n4 2\n255\n` (11 bytes) and the size of the whole file is 34 bytes. Is the file correct? If not, how many bytes are missing or extra?

🏋️ **5.** Write the value 40,000 as two bytes, **big-endian** and **little-endian**. (Hint: 40,000 = 156 × 256 + 64.)

🏋️ **6.** Change `ppm_p6.cpp` so it also writes the 3 × 2 picture as P3 (`first.ppm`), and prints both sizes. What are they?

🏋️ **7.** Make a 512 × 512 P6 image where red = x ÷ 2 and green = y ÷ 2 (integer division). Why do we divide by 2? What is the file size?

---

## Answers

**1.**
> `P6\n` = 3 bytes
> `640 480\n` = 3 + 1 + 3 + 1 = 8 bytes
> `255\n` = 4 bytes
> header = 3 + 8 + 4 = 15 bytes
> pixels = 640 × 480 × 3 = 921,600 bytes (Chapter 6, Practice 3)
> total = 15 + 921,600 = **921,615 bytes**

**2.**
> pixel index = 1 × 3 + 2 = 5
> byte in data = 5 × 3 + 2 (blue) = 17
> offset = 11 + 17 = **28**

**3.**
> header `P6\n2 1\n255\n`: `50 36 0A 32 20 31 0A 32 35 35 0A` (11 bytes)
> white = `FF FF FF`, magenta = `FF 00 FF`

```
0000:  50 36 0A 32 20 31 0A 32 35 35 0A FF FF FF FF 00
0010:  FF
```

17 bytes in total: 11 + 2 × 3 = 17 ✓. (`31` is the digit `1`, ASCII 49.)

**4.**
> expected = 11 + 4 × 2 × 3 = 11 + 24 = 35 bytes
> actual = 34 bytes
> **1 byte is missing.** The last channel of the last pixel is not there. (A common cause: a loop that stops one byte too early.)

**5.**
> 40,000 = 156 × 256 + 64
> high byte = 156 = 9 × 16 + 12 = `0x9C`
> low byte = 64 = `0x40`
> big-endian: **`9C 40`**
> little-endian: **`40 9C`**
> check: 0x9C40 = 156 × 256 + 64 = 39,936 + 64 = 40,000 ✓

**6.** Add `ok = ok && writePPM_P3("first.ppm", width, height, pixels);` and a print line. The sizes are **65 bytes** (P3, Chapter 8) and **29 bytes** (P6).

**7.**

```cpp
const int big = 512;
std::vector<std::uint8_t> img(big * big * 3, 0);
for (int y = 0; y < big; ++y) {
    for (int x = 0; x < big; ++x) {
        setPixel(img, big, big, x, y,
                 static_cast<std::uint8_t>(x / 2),
                 static_cast<std::uint8_t>(y / 2),
                 128);
    }
}
writePPM_P6("gradient512.ppm", big, big, img);
```

We divide by 2 because x goes up to **511**, which does not fit in a byte (the biggest is 255). 511 ÷ 2 = 255 (integer division drops the .5). So red goes from 0 to 255 across the whole width. Without the division, x = 256 would **wrap around** to 0 (Chapter 4), and you would see **two** gradients side by side!

> header `P6\n512 512\n255\n` = 3 + 8 + 4 = 15
> pixels = 512 × 512 × 3 = 786,432
> total = **786,447 bytes**

Each pair of columns has the same colour (x = 0 and 1 both give 0; x = 2 and 3 both give 1). Chapter 13 shows a better way to make a gradient of **any** width: interpolation.

---

## Summary

🧠 Text wastes space and time. **P6** stores pixels as **raw bytes**.

🧠 P6 = text header (`P6`, width, height, maxval) + **exactly one** whitespace + `width × height × 3` raw bytes.

🧠 One extra byte after the maxval **shifts every pixel**. Red becomes green.

🧠 Our pixel buffer is already in P6 order. Write it with **one** `write` call. **Binary mode is required.**

🧠 P6 size = header + width × height × 3. Always. Use this to check your files.

🧠 Get a file's size with `std::ios::ate` and `tellg()`.

🧠 **Big-endian** = biggest byte first (16-bit P6, and PNG later). **Little-endian** = smallest byte first (BMP later).

---

## Next chapter

Not every picture needs colour. In Chapter 10 we make **grey** images with PGM (one byte per pixel) and **black-and-white** images with PBM — where **8 pixels fit in one byte**, using the bit tricks from Chapter 4.
