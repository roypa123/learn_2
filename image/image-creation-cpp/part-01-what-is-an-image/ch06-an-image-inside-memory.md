# Chapter 6 — An Image Inside Memory

> **Part 1 · Chapter 6 of 82**
> **You need:** Chapters 1–5 · **You will make:** a pixel buffer in a `std::vector`, with functions to set pixels safely, and a print-out of every byte

---

## What you will learn

- Why computer memory is **one long line** of bytes, not a grid.
- How to put a 2D grid of pixels into that 1D line (**row by row**).
- The most important formula in this book: **index = y × width + x**.
- How to go back from an index to (x, y).
- How to store **three bytes per pixel** (R, G, B), and find each one.
- How much memory an image needs.
- Why we use **one** `std::vector<std::uint8_t>` for the whole image.
- How to write a pixel **safely**, even when (x, y) is outside.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **memory** | The place where a running program keeps its data. |
| **address** | The number of one byte's place in memory. |
| **buffer** | A block of memory that holds data, like all the pixels of an image. |
| **pixel buffer** | A buffer that holds all the pixels of one image. |
| **row-major order** | Storing a grid **one whole row after another**, top row first. |
| **index** | The position of one item in a list, starting at 0. |
| **interleaved** | Storing R, G, B of one pixel together: RGB RGB RGB … |
| **planar** | Storing all reds first, then all greens, then all blues. |
| **row size** (also called **stride**) | How many bytes one row of the image takes. |
| **remainder** | What is left over after dividing. 7 ÷ 4 = 1, remainder 3. |

---

## 6.1 Memory is one long line

📖 **New word: memory** — the place where a running program keeps its data.

You can think of memory as a very, very long street of houses. Each house holds **one byte**. Each house has a number.

📖 **New word: address** — the number of one byte's place in memory.

```
address:  1000  1001  1002  1003  1004  1005  1006 ...
         +-----+-----+-----+-----+-----+-----+-----+
value:   | 255 |  0  |  0  | 17  | 200 |  4  | 99  | ...
         +-----+-----+-----+-----+-----+-----+-----+
```

The street goes in **one direction**. There are no "rows" in memory. There is only "this byte, then the next byte, then the next".

But an image is a **grid** with rows and columns (Chapter 3). So we need a rule to put a 2D grid onto a 1D street.

---

## 6.2 Putting a grid into a line: row by row

📖 **New word: row-major order** — storing a grid one **whole row** after another, starting with the top row.

Take a small image, 4 pixels wide and 3 pixels tall. Give each pixel a letter:

```
        x=0  x=1  x=2  x=3
 y=0     A    B    C    D
 y=1     E    F    G    H
 y=2     I    J    K    L
```

In row-major order, we write row 0, then row 1, then row 2:

```
 A B C D | E F G H | I J K L
 └ row 0 ┘ └ row 1 ┘ └ row 2 ┘
```

📖 **New word: index** — the position of one item in a list, starting at 0.

```
index:  0 1 2 3   4 5 6 7   8 9 10 11
pixel:  A B C D   E F G H   I J K  L
```

This is exactly the order from Chapter 3: top to bottom, and left to right inside each row. It is also the order that most image files use. So when we save a file in Chapter 8, we can write the pixels **in the order they are already in memory**.

🧠 **Remember:** Pixels are stored **row by row, top row first, left to right inside each row**.

---

## 6.3 The formula: index = y × width + x

Now the big question: pixel **(x, y)** — at which index is it?

Think about pixel **G**, at (2, 1).

- To get to row 1, we must **skip all of row 0**. Row 0 has `width` = 4 pixels.
- Then, inside row 1, we move **x = 2** more places.

```
 A B C D | E F G
 └ skip ┘  └x=2┘
  4 pixels  ↑
            G is here: 4 + 2 = 6
```

🔢 **Maths: the general rule**

To reach row `y`, we skip `y` whole rows. Each row has `width` pixels.

> pixels to skip = y × width
> then move x more
> **index = y × width + x**

🔢 **Maths: check every example with width = 4**

| Pixel | (x, y) | y × width + x | index |
|---|---|---|---|
| A | (0, 0) | 0 × 4 + 0 | 0 |
| D | (3, 0) | 0 × 4 + 3 | 3 |
| E | (0, 1) | 1 × 4 + 0 | 4 |
| G | (2, 1) | 1 × 4 + 2 | 6 |
| J | (1, 2) | 2 × 4 + 1 | 9 |
| L | (3, 2) | 2 × 4 + 3 | 11 |

Look at the line in Section 6.2. Every answer is correct.

🔢 **Maths: a bigger example**

An image is 1,920 pixels wide. Where is pixel (100, 50)?

> index = 50 × 1,920 + 100
> 50 × 1,920 = 96,000
> index = 96,000 + 100 = 96,100

So pixel (100, 50) is the **96,100th** pixel in memory (counting from 0).

⚠️ **Careful:** It is **y × width**, not y × height, and not x × width. We multiply **y** because each step down skips a **whole row**, and a row is **width** long.

🧠 **Remember:** **index = y × width + x.** This is the most important formula in the book. You will use it in almost every chapter.

---

## 6.4 Going back: from index to (x, y)

Sometimes we have an index and we want (x, y). For example, when we loop over every pixel in one simple loop.

📖 **New word: remainder** — what is left over after dividing. 7 ÷ 4 = 1 with remainder 3, because 1 × 4 = 4, and 7 − 4 = 3.

🔢 **Maths: the rule**

> y = index ÷ width (whole-number division, drop the decimals)
> x = remainder of index ÷ width

Why? Every `width` pixels, we start a new row. So "how many whole rows fit" is y, and "how much is left over" is x.

In C++:

```cpp
int y = index / width;   // whole-number division (both are int)
int x = index % width;   // % gives the remainder
```

🔢 **Maths: index 7 with width = 4**

> y = 7 ÷ 4 = 1 (with 3 left over)
> x = 3
> So index 7 is pixel (3, 1).

Look at Section 6.2: index 7 is **H**, and H is at (3, 1) ✓.

🔢 **Maths: index 96,100 with width = 1,920**

> y = 96,100 ÷ 1,920 = 50 (because 50 × 1,920 = 96,000, and 51 × 1,920 = 97,920 is too big)
> x = 96,100 − 96,000 = 100
> So (100, 50) ✓, the same as Section 6.3.

---

## 6.5 Three bytes per pixel

So far, each pixel was one item. But a colour pixel has **three bytes**: R, G and B (Chapter 5).

📖 **New word: interleaved** — storing the R, G, B of one pixel **together**, then the next pixel's R, G, B, and so on.

```
pixel:      A           B           C        ...
bytes:  R  G  B  |  R  G  B  |  R  G  B  | ...
index:  0  1  2     3  4  5     6  7  8
```

Each pixel takes **3** places. So pixel number `p` starts at byte number `p × 3`.

🔢 **Maths: the byte index of a channel**

> pixel index = y × width + x
> first byte (red) = pixel index × 3
> green = first byte + 1
> blue = first byte + 2

Or in one line:

> **byte = (y × width + x) × 3 + channel**

where channel is **0 for red, 1 for green, 2 for blue**.

🔢 **Maths: where is the green byte of pixel G at (2, 1), width 4?**

> pixel index = 1 × 4 + 2 = 6
> first byte = 6 × 3 = 18
> green = 18 + 1 = **19**

So the red of G is byte 18, green is 19, blue is 20.

📖 **New word: planar** — another way: store **all** the reds first, then all the greens, then all the blues.

```
planar:  R R R R ... | G G G G ... | B B B B ...
```

Some programs use planar storage. But almost all image **files** in this book (PPM, BMP, PNG) use **interleaved**. So we use interleaved too.

---

## 6.6 Row size

📖 **New word: row size** (also called **stride**) — how many bytes one row of the image takes.

With 3 bytes per pixel:

> row size = width × 3

For width 4: row size = 12 bytes. For width 1,920: row size = 5,760 bytes.

This gives another way to write the byte formula, which is often easier to think about:

> **byte = y × rowSize + x × 3 + channel**

🔢 **Maths: check it is the same as Section 6.5**

> (y × width + x) × 3 + channel
> = y × width × 3 + x × 3 + channel
> = y × (width × 3) + x × 3 + channel
> = y × rowSize + x × 3 + channel ✓

Both formulas give the same answer. We multiplied the bracket out.

Why does row size matter? In Chapter 36 we meet the BMP format. In BMP, each row must be a multiple of **4 bytes** long, so the row size is sometimes **bigger** than width × 3. Then only the "row size" formula works. Learning it now makes Chapter 36 easy.

---

## 6.7 How much memory?

🔢 **Maths: total bytes**

> total bytes = width × height × 3

| Image | width × height × 3 | Bytes |
|---|---|---|
| 4 × 3 | 4 × 3 × 3 | 36 |
| 100 × 100 | 100 × 100 × 3 | 30,000 |
| 800 × 600 | 800 × 600 × 3 | 1,440,000 |
| 1,920 × 1,080 | 1,920 × 1,080 × 3 | 6,220,800 |

A computer today has billions of bytes of memory. So even large images fit easily. But we must still be careful with **very** big images and with copying images many times.

💡 **Tip:** Programmers measure big amounts of bytes in **kilobytes** (KB, about a thousand), **megabytes** (MB, about a million) and **gigabytes** (GB, about a billion). 6,220,800 bytes is about **6.2 MB**.

---

## 6.8 Why one `std::vector<std::uint8_t>`?

📖 **New word: buffer** — a block of memory that holds data.

📖 **New word: pixel buffer** — a buffer that holds all the pixels of an image.

We will hold the pixel buffer in **one** `std::vector<std::uint8_t>`, with `width × height × 3` bytes:

```cpp
std::vector<std::uint8_t> pixels(width * height * 3, 0);
```

You know `std::vector`. But why this exact choice? Let us look at the other choices and why we do **not** use them.

| Choice | Problem |
|---|---|
| `int picture[3][4][3];` (a fixed C++ array) | The size must be known **when you compile**. Real images have sizes we only know when the program runs (for example, when we read a file in Chapter 12). Big arrays also can crash on the stack. |
| `std::vector<std::vector<Colour>>` (a vector of rows) | Each row is a **separate** block of memory. It is slower, and it cannot be written to a file in one go. |
| `std::vector<int>` | An `int` is 4 bytes. We only need 1 byte per channel. It wastes 3 out of every 4 bytes. |
| **`std::vector<std::uint8_t>`** ✓ | One block, the exact size, bytes in the **same order as in the file**. |

🧠 **Remember:** Our image is **one** `std::vector<std::uint8_t>` of size `width × height × 3`, interleaved RGB, row-major, top row first. In Chapter 11 we wrap it in an `Image` class, but inside, it stays exactly like this.

The second argument, `0`, fills every byte with 0. So a new image starts **all black**.

---

## 6.9 Setting a pixel safely

To set pixel (x, y) to a colour, we:

1. Check that (x, y) is **inside** (Chapter 3). If not, do nothing.
2. Find the first byte: `(y × width + x) × 3`.
3. Write R, G and B into that byte and the next two.

Why step 1? If we forget it, a pixel at x = 4 in a 4-wide image would write into the **next row** (x = 4 is really index 4 = the first pixel of row 1). And a pixel far outside would write past the end of the vector, which is a serious bug (the program may crash, or worse, silently change other data).

🔢 **Maths: what goes wrong without the check**

> width = 4, we wrongly set (4, 0)
> index = 0 × 4 + 4 = 4
> index 4 is pixel E = (0, 1)!

So a mistake at the right edge **appears at the left edge of the next row**. If you ever see a shape "wrap around" to the other side of an image, this is why.

---

## Code

File: `ch06/buffer.cpp`

```cpp
#include <iostream>
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

int main() {
    const int width = 4;
    const int height = 3;
    std::vector<std::uint8_t> pixels(width * height * 3, 0);

    std::cout << "pixels: " << width * height
              << ", bytes: " << pixels.size() << "\n\n";

    setPixel(pixels, width, height, 0, 0, 255, 0, 0);
    setPixel(pixels, width, height, 3, 0, 0, 255, 0);
    setPixel(pixels, width, height, 1, 1, 255, 255, 255);
    setPixel(pixels, width, height, 3, 2, 0, 0, 255);
    setPixel(pixels, width, height, 9, 9, 255, 255, 0);

    for (int y = 0; y < height; ++y) {
        std::cout << "row " << y << ":";
        for (int x = 0; x < width; ++x) {
            int i = (y * width + x) * 3;
            std::cout << "  " << toHex(pixels[i])
                      << toHex(pixels[i + 1]) << toHex(pixels[i + 2]);
        }
        std::cout << "\n";
    }

    std::cout << "\nall bytes in memory order:\n";
    const int rowSize = width * 3;
    for (int i = 0; i < static_cast<int>(pixels.size()); ++i) {
        std::cout << toHex(pixels[i]) << ' ';
        if ((i + 1) % rowSize == 0) {
            std::cout << "\n";
        }
    }

    int index = 7;
    std::cout << "\npixel number " << index
              << " is at x = " << index % width
              << ", y = " << index / width << "\n";
    return 0;
}
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–3 | `#include <iostream>` / `<cstdint>` / `<string>` | Printing, exact byte types, text. Same as before. |
| 4 | `#include <vector>` | Lets us use `std::vector` for the pixel buffer. |
| 6–12 | `std::string toHex(...) { ... }` | Same function as Chapters 4 and 5: one byte → two hex digits. |
| 14–16 | `bool isInside(...) { ... }` | Same function as Chapter 3: is (x, y) a real pixel? |
| 18 | `void setPixel(std::vector<std::uint8_t>& pixels, int width, int height,` | A function that sets one pixel. It takes the buffer **by reference** (`&`) so it changes the real buffer, not a copy. It also needs the width and height of the image. |
| 19 | `int x, int y, std::uint8_t r, std::uint8_t g, std::uint8_t b) {` | Which pixel (x, y) and which colour (r, g, b). |
| 20 | `if (!isInside(x, y, width, height)) {` | Step 1 of Section 6.9: if (x, y) is **not** inside the image… |
| 21 | `return;` | …stop here and do nothing. This makes "drawing outside the picture" harmless. |
| 22 | `}` | End of the check. |
| 23 | `int i = (y * width + x) * 3;` | Step 2: the index of the pixel's **first** byte (its red byte). This is the formula from Section 6.5 with channel = 0. |
| 24 | `pixels[i]     = r;` | Step 3: write red into the first byte. |
| 25 | `pixels[i + 1] = g;` | Write green into the next byte. |
| 26 | `pixels[i + 2] = b;` | Write blue into the byte after that. |
| 27 | `}` | End of `setPixel`. |
| 29 | `int main() {` | The program starts here. |
| 30 | `const int width = 4;` | Our image is 4 pixels wide. |
| 31 | `const int height = 3;` | …and 3 pixels tall. The same size as the letter grid in Section 6.2. |
| 32 | `std::vector<std::uint8_t> pixels(width * height * 3, 0);` | The pixel buffer: 4 × 3 × 3 = 36 bytes, all set to 0. So the image starts all black. |
| 34 | `std::cout << "pixels: " << width * height` | Print the number of pixels: 12. |
| 35 | `<< ", bytes: " << pixels.size() << "\n\n";` | Print the number of bytes: 36. `pixels.size()` is the length of the vector. |
| 37 | `setPixel(pixels, width, height, 0, 0, 255, 0, 0);` | Make the top-left pixel (0, 0) **red**. |
| 38 | `setPixel(pixels, width, height, 3, 0, 0, 255, 0);` | Make the top-right pixel (3, 0) **green**. |
| 39 | `setPixel(pixels, width, height, 1, 1, 255, 255, 255);` | Make pixel (1, 1) **white**. |
| 40 | `setPixel(pixels, width, height, 3, 2, 0, 0, 255);` | Make the bottom-right pixel (3, 2) **blue**. |
| 41 | `setPixel(pixels, width, height, 9, 9, 255, 255, 0);` | Try to make (9, 9) yellow. It is **outside**, so `setPixel` does nothing. No crash, no mess. |
| 43 | `for (int y = 0; y < height; ++y) {` | Print the image row by row, top to bottom. |
| 44 | `std::cout << "row " << y << ":";` | A label at the start of each row. |
| 45 | `for (int x = 0; x < width; ++x) {` | Go across the row. |
| 46 | `int i = (y * width + x) * 3;` | The index of this pixel's red byte. The same formula as line 23. |
| 47 | `std::cout << "  " << toHex(pixels[i])` | Print two spaces, then the red byte in hex. |
| 48 | `<< toHex(pixels[i + 1]) << toHex(pixels[i + 2]);` | Then green and blue. Together they look like a colour code from Chapter 4, such as `FF0000`. |
| 49 | `}` | End of one row. |
| 50 | `std::cout << "\n";` | New line. |
| 51 | `}` | End of all rows. |
| 53 | `std::cout << "\nall bytes in memory order:\n";` | A heading. Now we show the buffer **as it really is**: one long line of bytes. |
| 54 | `const int rowSize = width * 3;` | One row is 4 × 3 = 12 bytes (Section 6.6). |
| 55 | `for (int i = 0; i < static_cast<int>(pixels.size()); ++i) {` | Go through **every byte**, from 0 to 35. We cast `size()` to `int` so we compare two numbers of the same kind (this avoids a warning). |
| 56 | `std::cout << toHex(pixels[i]) << ' ';` | Print the byte in hex and a space. |
| 57 | `if ((i + 1) % rowSize == 0) {` | After every 12th byte (when `i + 1` is 12, 24 or 36)… |
| 58 | `std::cout << "\n";` | …start a new line. This is **only for printing**. In memory there are no line breaks. |
| 59–60 | `}` / `}` | End of the `if` and the loop. |
| 62 | `int index = 7;` | A pixel index to turn back into (x, y). |
| 63 | `std::cout << "\npixel number " << index` | Print the index. |
| 64 | `<< " is at x = " << index % width` | x = 7 % 4 = 3 (the remainder, Section 6.4). |
| 65 | `<< ", y = " << index / width << "\n";` | y = 7 / 4 = 1 (whole-number division). |
| 66 | `return 0;` | The program finished with no problem. |
| 67 | `}` | End of `main`. |

### What you should see

```
pixels: 12, bytes: 36

row 0:  FF0000  000000  000000  00FF00
row 1:  000000  FFFFFF  000000  000000
row 2:  000000  000000  000000  0000FF

all bytes in memory order:
FF 00 00 00 00 00 00 00 00 00 FF 00 
00 00 00 FF FF FF 00 00 00 00 00 00 
00 00 00 00 00 00 00 00 00 00 00 FF 

pixel number 7 is at x = 3, y = 1
```

Look at the first line of bytes. `FF 00 00` is the red pixel (0, 0). Then 6 zero bytes for two black pixels. Then `00 FF 00` is the green pixel (3, 0).

🔢 **Maths: check where the white pixel's bytes are**

> (1, 1): pixel index = 1 × 4 + 1 = 5
> first byte = 5 × 3 = 15
> In the second printed line, bytes 12, 13, 14 are `00 00 00` (pixel (0, 1)), and bytes 15, 16, 17 are `FF FF FF` ✓.

And the yellow pixel at (9, 9) does not appear anywhere. `setPixel` ignored it, as we wanted.

---

## Small examples

### Example 1 — Fill the whole image with one colour

```cpp
for (int y = 0; y < height; ++y) {
    for (int x = 0; x < width; ++x) {
        setPixel(pixels, width, height, x, y, 0, 128, 255);
    }
}
```

Every pixel becomes (0, 128, 255), a sky blue. Every row prints as `0080FF  0080FF  0080FF  0080FF`.

### Example 2 — The same fill with one simple loop

Because the bytes are one long line, we can also fill by **pixel index**, with no x or y at all:

```cpp
for (int p = 0; p < width * height; ++p) {
    pixels[p * 3]     = 0;
    pixels[p * 3 + 1] = 128;
    pixels[p * 3 + 2] = 255;
}
```

This gives exactly the same buffer. It is a little faster, because there is no bounds check and no `y * width + x`. We use this style when **every** pixel gets the same treatment, like the colour changes in Chapter 47.

### Example 3 — A vertical line

To draw a line going **down** at x = 2:

```cpp
for (int y = 0; y < height; ++y) {
    setPixel(pixels, width, height, 2, y, 255, 255, 0);
}
```

> The pixel indexes are: 0 × 4 + 2 = 2, 1 × 4 + 2 = 6, 2 × 4 + 2 = 10.
> They are 4 apart — exactly one **width** apart.

🧠 Moving **down** one pixel = moving **width** places in the buffer (or rowSize bytes).

### Example 4 — Read a pixel back

```cpp
int i = (2 * width + 3) * 3;   // pixel (3, 2)
std::cout << static_cast<int>(pixels[i]) << ", "
          << static_cast<int>(pixels[i + 1]) << ", "
          << static_cast<int>(pixels[i + 2]) << "\n";
```

> i = (2 × 4 + 3) × 3 = 11 × 3 = 33

It prints `0, 0, 255` — the blue pixel we set on line 40.

---

## Common mistakes

⚠️ **`x * width + y` instead of `y * width + x`.** This is the most common bug in image code. The picture comes out scrambled or turned. Say it out loud: "**y rows down, times the width, plus x**".

⚠️ **Forgetting `× 3`.** `pixels[y * width + x]` is the **pixel** index, not the **byte** index. Without `× 3`, you write into the wrong pixel's bytes, and colours look mixed up.

⚠️ **No bounds check.** A pixel just past the right edge appears at the start of the next row. A pixel far outside writes past the vector's end.

⚠️ **Using `height` in the index.** The index never uses `height`. Only `width` (or row size). `height` is only used for the bounds check and the total size.

⚠️ **Thinking memory has rows.** It does not. Rows exist only in **our** formula. When we print a new line every 12 bytes, that is only for us to read.

⚠️ **Printing bytes without casting or `toHex`.** `std::cout << pixels[i]` prints a strange character, not a number (Chapter 4).

---

## Practice

🏋️ **1.** An image is 10 pixels wide. What is the pixel index of (7, 3)? What is the byte index of its blue channel?

🏋️ **2.** An image is 10 pixels wide. Pixel index 47 — what are its x and y?

🏋️ **3.** How many bytes does a 640 × 480 RGB image need?

🏋️ **4.** An image is 5 pixels wide. What is the row size? Which byte is the red channel of the **first** pixel of row 3?

🏋️ **5.** In an image 8 pixels wide, someone forgets the bounds check and sets pixel (8, 2). Which pixel really changes?

🏋️ **6.** Change `buffer.cpp` to draw a horizontal line across row 1 in yellow (255, 255, 0). What does row 1 print?

🏋️ **7.** Change `buffer.cpp` so the image is 6 × 2. Set the bottom-right pixel to white. Which bytes in "memory order" become `FF`?

🏋️ **8.** Write a function `getRed(pixels, width, x, y)` that returns the red value of pixel (x, y) as an `int`.

---

## Answers

**1.**
> pixel index = 3 × 10 + 7 = 37
> first byte = 37 × 3 = 111
> blue = 111 + 2 = **113**

**2.**
> y = 47 ÷ 10 = **4** (whole-number division)
> x = 47 % 10 = **7** (remainder)
> check: 4 × 10 + 7 = 47 ✓

**3.**
> 640 × 480 = 307,200 pixels
> 307,200 × 3 = **921,600 bytes** (about 0.9 MB)

**4.**
> row size = 5 × 3 = **15 bytes**
> first pixel of row 3 is (0, 3)
> byte = 3 × 15 + 0 × 3 + 0 = **45**

**5.**
> index = 2 × 8 + 8 = 24
> 24 = 3 × 8 + 0, so it is pixel **(0, 3)** — the first pixel of the **next** row.

(If the image had only 3 rows, index 24 would be past the end, and the program would write into memory it does not own.)

**6.** Add after line 41:

```cpp
for (int x = 0; x < width; ++x) {
    setPixel(pixels, width, height, x, 1, 255, 255, 0);
}
```

Row 1 now prints `FFFF00  FFFF00  FFFF00  FFFF00`. The white pixel at (1, 1) is **overwritten** by yellow, because we set it later.

**7.**
> width = 6, height = 2 → 6 × 2 × 3 = 36 bytes (the same total as before!)
> bottom-right = (5, 1)
> pixel index = 1 × 6 + 5 = 11
> first byte = 11 × 3 = 33
> So bytes **33, 34 and 35** — the last three bytes — become `FF`.

The row size is now 18, so the program prints two lines of 18 bytes, and the last line ends with `FF FF FF`.

**8.**

```cpp
int getRed(const std::vector<std::uint8_t>& pixels, int width, int x, int y) {
    int i = (y * width + x) * 3;
    return pixels[i];
}
```

The `const` and `&` mean: read the real buffer, do not copy it, and do not change it. Returning `int` means the caller can print it directly, without a cast. (A full version would also check bounds. Our `Image` class in Chapter 11 does this.)

---

## Summary

🧠 Memory is **one long line of bytes**. A grid must be laid out in it by a rule.

🧠 The rule: **row-major order** — top row first, left to right.

🧠 **pixel index = y × width + x.**

🧠 Back again: **y = index / width**, **x = index % width**.

🧠 RGB is **interleaved**: R G B R G B … **byte = (y × width + x) × 3 + channel** (0 = red, 1 = green, 2 = blue).

🧠 **row size = width × 3**. Moving down one pixel = moving one row size forward.

🧠 Memory needed = **width × height × 3** bytes.

🧠 We use **one** `std::vector<std::uint8_t>` and **always check bounds** before writing a pixel.

---

## Next chapter

Part 1 is done! We know what a pixel is, how colour works, and how an image lives in memory. In **Part 2** we finally make **real image files**. Chapter 7 starts with the base skill: writing **exact bytes** into a file with C++, and seeing them again.
