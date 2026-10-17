# Chapter 8 — The PPM Text Format (P3)

> **Part 2 · Chapter 8 of 82**
> **You need:** Chapters 1–7 · **You will make:** `first.ppm` (your first real image!) and `gradient.ppm` (a 256 × 256 colour picture)

---

## What you will learn

- What every image file needs: a **header** and the **pixel data**.
- What the **PPM** family of formats is, and why it is perfect for beginners.
- The exact rules of the **P3** format, byte by byte.
- How a viewer **reads** a P3 file, step by step.
- How to write a P3 file from our pixel buffer.
- How to make a big colourful image with only two loops.
- How big a P3 file is, and why that leads us to Chapter 9.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **header** | The first part of a file. It describes the rest of the file. |
| **pixel data** | The part of the file that holds the colours of the pixels. |
| **magic number** | A few bytes at the very start of a file that say what type of file it is. |
| **Netpbm** | A family of very simple image formats: PBM, PGM and PPM. |
| **PPM** | "Portable PixMap". The Netpbm format for **colour** images. |
| **plain format** | A Netpbm format that stores numbers as **text** (P1, P2, P3). |
| **whitespace** | Characters that make empty space: space, tab, new line, carriage return. |
| **maximum value (maxval)** | The number that means "full brightness" in this file. Usually 255. |
| **comment** | Text in a file that a program skips. It is only for people. |
| **parse** | To read text and work out what it means. |

---

## 8.1 What does an image file need?

At the end of Chapter 7, we saved our 36 pixel bytes into a file. But no viewer could open it. Why?

Imagine someone gives you 36 numbers and says "this is a picture". You would ask:

1. **Is it really a picture?** Or is it music, or text?
2. **How wide is it?** 36 bytes could be 12 pixels: 12 × 1, 6 × 2, 4 × 3, 3 × 4, 2 × 6 or 1 × 12!
3. **What does each number mean?** Is 255 bright? Is 100 bright?

A real image file answers these questions **before** the pixels.

📖 **New word: header** — the first part of a file. It describes the rest of the file.

📖 **New word: pixel data** — the part of the file that holds the colours.

```
┌──────────────────────────────┐
│ HEADER                       │  ← "I am a colour image, 3 × 2, max 255"
├──────────────────────────────┤
│ PIXEL DATA                   │  ← the colours, in row-major order
└──────────────────────────────┘
```

Every image format in this book has these two parts. Some (like PNG) add more parts. But the idea is always the same.

### The magic number

📖 **New word: magic number** — a few bytes at the very start of a file that say what type it is.

Viewers look at the first bytes to decide what the file is. Some examples you will meet in this book:

| Format | First bytes | As text |
|---|---|---|
| PPM (text) | `50 33` | `P3` |
| PPM (binary) | `50 36` | `P6` |
| BMP | `42 4D` | `BM` |
| PNG | `89 50 4E 47` | `.PNG` |
| GIF | `47 49 46 38` | `GIF8` |

---

## 8.2 The Netpbm family

📖 **New word: Netpbm** — a family of very simple image formats, made in the 1980s so that images could be sent easily between different computers.

There are three kinds of image, and each has a **text** version and a **binary** version:

| Magic | Name | Pixels | Stored as |
|---|---|---|---|
| `P1` | PBM | black and white (1 bit) | text |
| `P2` | PGM | grey | text |
| `P3` | **PPM** | **colour (RGB)** | **text** |
| `P4` | PBM | black and white | binary |
| `P5` | PGM | grey | binary |
| `P6` | PPM | colour | binary |

📖 **New word: PPM** — "Portable PixMap". The Netpbm format for colour images.

📖 **New word: plain format** — the text versions (P1, P2, P3). Every number is written in normal digits, so a person can read the file in a text editor.

Why start with P3?

- It is **text**. You can open it in any text editor and **read** it.
- It is **easy to check**. If something is wrong, you can see it.
- It has **almost no rules**. The header is three numbers.
- Its pixel data is in **the same order as our buffer** (row-major, top row first, R G B).

In Chapter 9 we use P6 (binary). In Chapter 10 we use P1, P2, P4 and P5.

---

## 8.3 The rules of P3

A P3 file is text. It has, in this order:

1. The magic number: the two characters **`P3`**.
2. **Whitespace**.
3. The **width**, as text digits.
4. Whitespace.
5. The **height**, as text digits.
6. Whitespace.
7. The **maximum value**, as text digits.
8. Whitespace.
9. Then **width × height × 3** numbers, as text, each separated by whitespace: R G B of the first pixel, R G B of the second pixel, and so on.

📖 **New word: whitespace** — characters that make empty space: space (32), tab (9), line feed (10) and carriage return (13).

The rules say **any amount** of whitespace is fine. One space, ten spaces, a new line — all mean the same thing: "this number ended, the next one starts". This makes P3 very forgiving.

📖 **New word: maximum value (maxval)** — the number that means "full brightness". With maxval 255, the value 255 is full and 0 is none, exactly like our bytes. (Section 8.7 shows other values.)

📖 **New word: comment** — text that a program skips. In P3, a `#` starts a comment, and it goes to the end of that line.

### Our first image, as a P3 file

Here is the picture we will make. It is 3 pixels wide and 2 pixels tall:

```
        x=0      x=1      x=2
y=0     red      green    blue
y=1     yellow   white    black
```

And here is the whole file:

```
P3
3 2
255
255 0 0
0 255 0
0 0 255

255 255 0
255 255 255
0 0 0

```

Let us read it line by line.

| Line | Text | Meaning |
|---|---|---|
| 1 | `P3` | "I am a colour image with text numbers." |
| 2 | `3 2` | width = 3, height = 2. **Width first.** |
| 3 | `255` | maxval = 255. |
| 4 | `255 0 0` | pixel (0, 0): red |
| 5 | `0 255 0` | pixel (1, 0): green |
| 6 | `0 0 255` | pixel (2, 0): blue |
| 7 | (empty) | just whitespace. We put it here so a person can see where a row ends. A viewer ignores it. |
| 8 | `255 255 0` | pixel (0, 1): yellow |
| 9 | `255 255 255` | pixel (1, 1): white |
| 10 | `0 0 0` | pixel (2, 1): black |
| 11 | (empty) | whitespace again. |

🧠 **Remember:** A P3 file is: `P3`, width, height, maxval, then R G B for every pixel, in row-major order. All as text, separated by whitespace.

### One pixel per line

We put each pixel on its **own line**. The P3 rules say lines **should not be longer than 70 characters**. One pixel is at most `255 255 255` = 11 characters, so we are always safe, even for a very wide image. (Many viewers accept longer lines, but some old ones do not. One pixel per line works everywhere.)

---

## 8.4 How a viewer reads P3

📖 **New word: parse** — to read text and work out what it means.

A viewer **parses** the file like this:

```
1. Read 2 characters.           → "P3"   OK, a text PPM.
2. Skip whitespace and comments.
3. Read digits until whitespace → "3"    width = 3
4. Skip whitespace.
5. Read digits                  → "2"    height = 2
6. Skip whitespace.
7. Read digits                  → "255"  maxval = 255
8. Repeat 3 × 2 × 3 = 18 times:
     skip whitespace, read digits → one channel value
9. Done. Show the picture.
```

🔢 **Maths: how many numbers does the viewer read in step 8?**

> width × height × 3 = 3 × 2 × 3 = 18

If our file has **fewer** than 18 numbers, the viewer stops with an error (or shows black pixels). If it has **more**, the extra ones are ignored. So the header and the data **must agree**.

🔢 **Maths: how the viewer turns text "255" into the number 255**

It reads one digit at a time and builds the number:

> start: n = 0
> read '2' (code 50): digit = 50 − 48 = 2. n = 0 × 10 + 2 = 2
> read '5' (code 53): digit = 5. n = 2 × 10 + 5 = 25
> read '5' (code 53): digit = 5. n = 25 × 10 + 5 = 255
> read ' ' (whitespace): stop. The number is **255**.

Each new digit **multiplies the old value by 10** and adds the digit. We will write exactly this code ourselves in Chapter 12, when we **read** PPM files.

---

## 8.5 The bytes of the header

Remember Chapter 7: text is bytes too. Here are the first 11 bytes of `first.ppm`, as a hex dump:

```
0000:  50 33 0A 33 20 32 0A 32 35 35 0A
        P  3 \n  3 sp  2 \n  2  5  5 \n
```

| Bytes | Characters | Meaning |
|---|---|---|
| `50 33` | `P3` | magic number |
| `0A` | `\n` | whitespace |
| `33` | `3` | width (one digit) |
| `20` | space | whitespace |
| `32` | `2` | height |
| `0A` | `\n` | whitespace |
| `32 35 35` | `255` | maxval (three digits) |
| `0A` | `\n` | whitespace |

🔢 **Maths: the size of first.ppm**

Count the characters on each line, plus 1 for each `\n`:

| Line | Text | Characters + `\n` |
|---|---|---|
| 1 | `P3` | 2 + 1 = 3 |
| 2 | `3 2` | 3 + 1 = 4 |
| 3 | `255` | 3 + 1 = 4 |
| 4 | `255 0 0` | 7 + 1 = 8 |
| 5 | `0 255 0` | 7 + 1 = 8 |
| 6 | `0 0 255` | 7 + 1 = 8 |
| 7 | (empty) | 0 + 1 = 1 |
| 8 | `255 255 0` | 9 + 1 = 10 |
| 9 | `255 255 255` | 11 + 1 = 12 |
| 10 | `0 0 0` | 5 + 1 = 6 |
| 11 | (empty) | 0 + 1 = 1 |

> 3 + 4 + 4 + 8 + 8 + 8 + 1 + 10 + 12 + 6 + 1 = **65 bytes**

The picture has only 6 pixels, which is 18 bytes of colour in memory. The P3 file needs 65 bytes. Text is **big**. Keep this in mind for Section 8.8.

### Should we use binary mode for a text file?

P3 is text, so text mode would also work: on Windows, each `\n` becomes `0D 0A`, and `0D` is also whitespace. A viewer reads the same picture.

But we still open the file with `std::ios::binary`. Then the file has **exactly the same bytes on every computer** (65 bytes, not 76 on Windows), and our size calculations and hex dumps always match. It is a good habit for all image files.

---

## 8.6 Writing a P3 file in C++

From Chapter 7 we know: `<<` on a stream writes numbers **as text**. That is exactly what P3 wants!

```cpp
file << "P3\n";
file << width << " " << height << "\n";
file << "255\n";
```

This writes the header. Then for each pixel, in row-major order (the same order as our buffer, Chapter 6):

```cpp
file << static_cast<int>(pixels[i]) << " "
     << static_cast<int>(pixels[i + 1]) << " "
     << static_cast<int>(pixels[i + 2]) << "\n";
```

⚠️ **Careful:** The `static_cast<int>` is **very** important here. Without it, `file << pixels[i]` writes the `std::uint8_t` as a **character** (Chapter 4). The byte 255 would be written as one strange character instead of the three digits `2`, `5`, `5`. The viewer would not understand it.

---

## 8.7 Other maximum values

The maxval does not have to be 255. It can be any number from **1** to **65,535**.

🔢 **Maths: what a value means**

> brightness = value ÷ maxval

| maxval | value | brightness |
|---|---|---|
| 255 | 255 | 255 ÷ 255 = 1.0 (full) |
| 255 | 51 | 51 ÷ 255 = 0.2 |
| 1 | 1 | 1 ÷ 1 = 1.0 (full) |
| 1 | 0 | 0.0 (none) |
| 4 | 2 | 2 ÷ 4 = 0.5 |
| 15 | 15 | 1.0 |

So this file is also a red-green-blue / yellow-white-black image:

```
P3
3 2
1
1 0 0   0 1 0   0 0 1
1 1 0   1 1 1   0 0 0
```

With maxval 1, each channel can only be "off" (0) or "on" (1). That gives the 8 corner colours from Chapter 5, and nothing in between.

In this book we almost always use **255**, because our buffer holds bytes (0–255).

---

## 8.8 A big picture with two loops

Six pixels are hard to see. Let us make a **256 × 256** image.

Here is the idea: make the **red** value equal to **x**, and the **green** value equal to **y**. Keep blue at 128.

- On the **left** edge (x = 0), there is no red. On the **right** edge (x = 255), red is full.
- At the **top** (y = 0), there is no green. At the **bottom** (y = 255), green is full.

```
(0,0) dark blue-ish ─────────► (255,0) pink-ish (red + blue)
   │
   │
   ▼
(0,255) green-ish ──────────► (255,255) yellow-ish (red + green)
```

🔢 **Maths: the four corners** (blue is always 128)

| Corner | x | y | (R, G, B) | Colour |
|---|---|---|---|---|
| top-left | 0 | 0 | (0, 0, 128) | dark blue |
| top-right | 255 | 0 | (255, 0, 128) | pink |
| bottom-left | 0 | 255 | (0, 255, 128) | spring green |
| bottom-right | 255 | 255 | (255, 255, 128) | light yellow |

Why 256 × 256? Because then x and y go from 0 to **255** — exactly the range of a byte. We can use x as a colour value directly, with no maths. (In Chapter 13 we learn to make gradients for **any** size, using interpolation.)

🔢 **Maths: how big is gradient.ppm?**

> pixels = 256 × 256 = 65,536
> in memory: 65,536 × 3 = 196,608 bytes

For the file, count the characters. Each pixel line is `R G B\n`: the digits, plus 2 spaces and 1 new line.

The numbers 0 to 255 have:
> 0–9: 10 numbers × 1 digit = 10 digits
> 10–99: 90 numbers × 2 digits = 180 digits
> 100–255: 156 numbers × 3 digits = 468 digits
> total for one pass through 0–255: 10 + 180 + 468 = **658 digits**

> red digits: each of the 256 rows goes through x = 0…255 → 658 × 256 = 168,448
> green digits: each value of y is used for a whole row of 256 pixels → 658 × 256 = 168,448
> blue digits: always "128" = 3 digits × 65,536 = 196,608
> spaces and new lines: 3 × 65,536 = 196,608
> empty line after each row: 256
> header `P3\n256 256\n255\n`: 3 + 8 + 4 = 15

> total = 168,448 + 168,448 + 196,608 + 196,608 + 256 + 15 = **730,383 bytes**

The file is about **3.7 times** bigger than the pixel bytes in memory (730,383 ÷ 196,608 ≈ 3.7). For a big photo, that is a lot of waste. Chapter 9 fixes this with the binary P6 format.

---

## Code

File: `ch08/ppm_p3.cpp`

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
    file << "P3\n";
    file << width << " " << height << "\n";
    file << "255\n";
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

    if (!writePPM_P3("first.ppm", width, height, pixels)) {
        std::cout << "could not write first.ppm\n";
        return 1;
    }
    std::cout << "wrote first.ppm\n";

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

    if (!writePPM_P3("gradient.ppm", size, size, gradient)) {
        std::cout << "could not write gradient.ppm\n";
        return 1;
    }
    std::cout << "wrote gradient.ppm\n";
    return 0;
}
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–5 | `#include ...` | Printing, files, bytes, text and vectors. Same as Chapter 7. |
| 7–9 | `bool isInside(...) { ... }` | Same as Chapter 3: is (x, y) inside the image? |
| 11–20 | `void setPixel(...) { ... }` | Same as Chapter 6: check bounds, find the first byte with `(y * width + x) * 3`, write R, G, B. |
| 22 | `bool writePPM_P3(const std::string& fileName, int width, int height,` | A function that saves a pixel buffer as a P3 file. It needs the file name and the size… |
| 23 | `const std::vector<std::uint8_t>& pixels) {` | …and the pixel buffer. `const &` means "read it, do not copy it, do not change it". It returns `true` if it worked. |
| 24 | `std::ofstream file(fileName, std::ios::binary);` | Open the file. Binary mode, so the bytes are the same on every computer (Section 8.5). |
| 25–27 | `if (!file) { return false; }` | If the file could not open, stop and say "it did not work". |
| 28 | `file << "P3\n";` | The magic number, then a new line (whitespace). |
| 29 | `file << width << " " << height << "\n";` | The width, a space, the height, a new line. `<<` writes the `int`s as text digits. |
| 30 | `file << "255\n";` | The maxval, 255, then a new line. Our buffer holds bytes, so 255 is "full". |
| 31 | `for (int y = 0; y < height; ++y) {` | Go through the rows, **top to bottom** — the order P3 wants. |
| 32 | `for (int x = 0; x < width; ++x) {` | Inside each row, go **left to right**. |
| 33 | `int i = (y * width + x) * 3;` | The index of this pixel's red byte (Chapter 6). |
| 34 | `file << static_cast<int>(pixels[i]) << " "` | Write red as text, then a space. The cast to `int` makes `<<` write **digits**, not a character (Section 8.6). |
| 35 | `<< static_cast<int>(pixels[i + 1]) << " "` | Write green as text, then a space. |
| 36 | `<< static_cast<int>(pixels[i + 2]) << "\n";` | Write blue as text, then a new line. One pixel per line (Section 8.3). |
| 37 | `}` | End of one row. |
| 38 | `file << "\n";` | An empty line after each row. A viewer treats it as whitespace. It is only there so **people** can see the rows in a text editor. |
| 39 | `}` | End of all rows. |
| 40 | `return static_cast<bool>(file);` | `true` if every write worked. The file closes when the function ends. |
| 41 | `}` | End of `writePPM_P3`. |
| 43 | `int main() {` | The program starts here. |
| 44 | `const int width = 3;` | Our first image is 3 pixels wide… |
| 45 | `const int height = 2;` | …and 2 pixels tall. |
| 46 | `std::vector<std::uint8_t> pixels(width * height * 3, 0);` | The pixel buffer: 3 × 2 × 3 = 18 bytes, all 0 (black). |
| 48 | `setPixel(pixels, width, height, 0, 0, 255, 0, 0);` | Top-left (0, 0): red. |
| 49 | `setPixel(pixels, width, height, 1, 0, 0, 255, 0);` | Top-middle (1, 0): green. |
| 50 | `setPixel(pixels, width, height, 2, 0, 0, 0, 255);` | Top-right (2, 0): blue. |
| 51 | `setPixel(pixels, width, height, 0, 1, 255, 255, 0);` | Bottom-left (0, 1): yellow (red + green). |
| 52 | `setPixel(pixels, width, height, 1, 1, 255, 255, 255);` | Bottom-middle (1, 1): white. |
| 53 | `setPixel(pixels, width, height, 2, 1, 0, 0, 0);` | Bottom-right (2, 1): black. The buffer is already black, so this line changes nothing. We keep it so the code shows **all six** pixels clearly. |
| 55 | `if (!writePPM_P3("first.ppm", width, height, pixels)) {` | Save the image. If saving did **not** work… |
| 56 | `std::cout << "could not write first.ppm\n";` | …say so… |
| 57 | `return 1;` | …and stop with "problem". |
| 58 | `}` | End of the check. |
| 59 | `std::cout << "wrote first.ppm\n";` | Say that it worked. |
| 61 | `const int size = 256;` | The second image is 256 × 256 (Section 8.8). |
| 62 | `std::vector<std::uint8_t> gradient(size * size * 3, 0);` | Its buffer: 256 × 256 × 3 = 196,608 bytes. |
| 63 | `for (int y = 0; y < size; ++y) {` | Every row… |
| 64 | `for (int x = 0; x < size; ++x) {` | …and every pixel in the row. |
| 65 | `setPixel(gradient, size, size, x, y,` | Set pixel (x, y) of the gradient. Width and height are both `size`. |
| 66 | `static_cast<std::uint8_t>(x),` | Red = x. x goes 0 to 255, so it fits in a byte. The cast says so. |
| 67 | `static_cast<std::uint8_t>(y),` | Green = y. |
| 68 | `128);` | Blue = 128 for every pixel. |
| 69–70 | `}` / `}` | End of the two loops. |
| 72–75 | `if (!writePPM_P3("gradient.ppm", ...)) { ... return 1; }` | Save the gradient. Stop if it fails. |
| 76 | `std::cout << "wrote gradient.ppm\n";` | Say that it worked. |
| 77 | `return 0;` | The program finished with no problem. |
| 78 | `}` | End of `main`. |

### What you should see

In the terminal:

```
wrote first.ppm
wrote gradient.ppm
```

Then open **`first.ppm`** in your image viewer (Chapter 1, Section 1.9). **Zoom in a lot.** You should see:

```
┌───────┬───────┬───────┐
│  red  │ green │ blue  │
├───────┼───────┼───────┤
│yellow │ white │ black │
└───────┴───────┴───────┘
```

🎉 **This is your first image, made from scratch.** Every byte in that file was decided by your code.

Now open **`gradient.ppm`**. You see a smooth square of colour: dark blue at the top-left, pink at the top-right, green at the bottom-left and light yellow at the bottom-right.

Also open `first.ppm` in a **text editor** (Notepad, VS Code, …). You will see the exact text from Section 8.3.

💡 **Tip:** If your viewer makes `first.ppm` look blurry when zoomed, look for a "smoothing" or "interpolation" setting and turn it off (Chapter 1).

---

## Small examples

### Example 1 — Write a P3 file by hand

You do not even need C++ to make a P3 file. Open a text editor, type this, and save it as `hand.ppm`:

```
P3
# a 2 x 2 image, typed by hand
2 2
255
255 0 0     0 0 255
0 0 255     255 0 0
```

It is a tiny **checkerboard**: red, blue / blue, red. The line starting with `#` is a comment, and the viewer skips it. Many spaces between pixels are fine, because any whitespace works.

### Example 2 — A mistake in the header

Change line 29 of the code to write the height first:

```cpp
file << height << " " << width << "\n";   // WRONG order
```

The file now says `2 3`: width 2, height 3. The viewer reads the 18 numbers as **2 pixels per row, 3 rows**:

```
red     green
blue    yellow
white   black
```

The pixels are all there, but in the wrong places. The header must say **width first**.

### Example 3 — Stripes with the remainder

Make every **4th** column white and the others black, in a 16 × 4 image:

```cpp
for (int y = 0; y < 4; ++y) {
    for (int x = 0; x < 16; ++x) {
        if (x % 4 == 0) {
            setPixel(pixels, 16, 4, x, y, 255, 255, 255);
        }
    }
}
```

> x % 4 == 0 is true for x = 0, 4, 8, 12.

So there are 4 white vertical stripes, each 1 pixel wide, at x = 0, 4, 8 and 12. (`%` is the remainder from Chapter 6.)

### Example 4 — Count the numbers in the file

For a 10 × 5 image:
> numbers in the pixel data = 10 × 5 × 3 = 150
> numbers in the header = 3 (width, height, maxval)
> total = 153 numbers (plus the magic `P3`)

---

## Common mistakes

⚠️ **Writing bytes without `static_cast<int>`.** The file gets strange characters instead of digits. The viewer says the file is broken.

⚠️ **Height before width.** The header is **width, then height**. Otherwise the picture is rearranged (Example 2).

⚠️ **Too few numbers.** If the loops miss some pixels, the file has fewer than width × height × 3 numbers. The viewer shows an error or black pixels.

⚠️ **No whitespace between numbers.** `255 0 0255 0 0` has `0255` stuck together. The viewer reads it as the number 255 and everything after it is shifted.

⚠️ **Spaces before `P3`.** The magic number must be the **very first** two bytes of the file.

⚠️ **Not zooming in.** A 3 × 2 image is 6 tiny dots. Zoom in before you decide it did not work.

---

## Practice

🏋️ **1.** Write (by hand, in a text editor) a P3 file for a 1 × 3 image: red on top, green in the middle, blue at the bottom. Open it.

🏋️ **2.** How many bytes is the file `P3\n1 1\n255\n255 255 255\n`? (Count every character.)

🏋️ **3.** Change `ppm_p3.cpp` so the gradient has red = x, green = 0, blue = y. What colours are at the four corners?

🏋️ **4.** Make a 256 × 256 **grey** gradient from black on the left to white on the right. (Hint: Chapter 5 — grey means R = G = B.)

🏋️ **5.** Make a 200 × 200 image that is all orange (255, 128, 0).

🏋️ **6.** A P3 file has the header `P3 4 3 15`. How many numbers must the pixel data have? What brightness does the value 5 mean?

🏋️ **7.** Make a 64 × 64 image with a **white border** 1 pixel thick around a black inside. (Hint: a pixel is on the border if x is 0 or 63, or y is 0 or 63.)

---

## Answers

**1.**

```
P3
1 3
255
255 0 0
0 255 0
0 0 255
```

Width 1, height 3. One pixel per row.

**2.**
> `P3\n` = 3
> `1 1\n` = 4
> `255\n` = 4
> `255 255 255\n` = 12
> total = 3 + 4 + 4 + 12 = **23 bytes**

**3.** Change lines 66–68 to `static_cast<std::uint8_t>(x), 0, static_cast<std::uint8_t>(y)`.

| Corner | (R, G, B) | Colour |
|---|---|---|
| top-left (0, 0) | (0, 0, 0) | black |
| top-right (255, 0) | (255, 0, 0) | red |
| bottom-left (0, 255) | (0, 0, 255) | blue |
| bottom-right (255, 255) | (255, 0, 255) | magenta |

**4.** Use x for all three channels:

```cpp
std::uint8_t v = static_cast<std::uint8_t>(x);
setPixel(gradient, size, size, x, y, v, v, v);
```

Every column is one grey. Column 0 is (0, 0, 0) black, column 255 is (255, 255, 255) white. Every row looks the same.

**5.**

```cpp
const int w = 200, h = 200;
std::vector<std::uint8_t> img(w * h * 3, 0);
for (int y = 0; y < h; ++y) {
    for (int x = 0; x < w; ++x) {
        setPixel(img, w, h, x, y, 255, 128, 0);
    }
}
writePPM_P3("orange.ppm", w, h, img);
```

**6.**
> numbers = 4 × 3 × 3 = **36**
> brightness of 5 = 5 ÷ 15 ≈ **0.33** (one third)

(And yes — `P3 4 3 15` on **one line** is fine. Spaces are whitespace too.)

**7.**

```cpp
const int n = 64;
std::vector<std::uint8_t> img(n * n * 3, 0);
for (int y = 0; y < n; ++y) {
    for (int x = 0; x < n; ++x) {
        bool border = (x == 0 || x == n - 1 || y == 0 || y == n - 1);
        if (border) {
            setPixel(img, n, n, x, y, 255, 255, 255);
        }
    }
}
writePPM_P3("border.ppm", n, n, img);
```

The last pixel is at `n − 1` = 63, not 64 (Chapter 3).

🔢 How many pixels are white?
> top row 64 + bottom row 64 = 128
> left and right columns, without the corners already counted: 62 + 62 = 124
> total = 128 + 124 = **252**
> (Check: all pixels 64 × 64 = 4,096; inside black square 62 × 62 = 3,844; 4,096 − 3,844 = 252 ✓.)

---

## Summary

🧠 An image file = **header** (what it is, how big) + **pixel data** (the colours).

🧠 The **magic number** at the start says the file type. P3 starts with the text `P3`.

🧠 A P3 file is text: `P3`, **width**, **height**, **maxval**, then R G B for every pixel, row-major, top row first.

🧠 Any whitespace separates numbers. `#` starts a comment.

🧠 Brightness = value ÷ maxval. We use maxval **255**.

🧠 Write channels with `static_cast<int>` so `<<` writes **digits**.

🧠 P3 is easy to read but **big**: about 3.7 times the pixel bytes for our gradient.

---

## Next chapter

In Chapter 9 we keep the same simple header, but write the pixel data as **raw bytes** instead of text. The format is called **P6**. Our 730,383-byte gradient will shrink to under 200,000 bytes, and writing it will take just **one** call to `write`.
