# Chapter 11 — Building an `Image` Class

> **Part 2 · Chapter 11 of 82**
> **You need:** Chapters 1–10 · **You will make:** `image.h` (the `Image` class we use for the rest of the book) and a test program

---

## What you will learn

- Why passing `pixels, width, height` to every function causes bugs.
- How to keep the pixel buffer and its size **together** in one class.
- What an **invariant** is, and the one invariant our `Image` class always keeps.
- A `Colour` type with **default values**, and a set of **named colours**.
- How to make a **header-only** file with **include guards**.
- Why the **order of members** matters in the constructor.
- How to tell the compiler where to find our header, with `-I`.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **library code** | Code we write once and use in many programs. |
| **header-only** | Library code that lives completely in a `.h` file. No `.cpp` file is needed. |
| **include guard** | Three lines that stop a header from being included twice in one program. |
| **invariant** | A rule about an object that is **always** true, from the moment it is made. |
| **encapsulation** | Hiding the inside of an object, so it can only be changed in safe ways. |
| **member initialiser list** | The part of a constructor after `:` that gives each member its first value. |
| **include path** | A folder where the compiler looks for header files. |

---

## 11.1 The problem with loose pieces

Look at a call from Chapter 8:

```cpp
setPixel(gradient, size, size, x, y, r, g, b);
```

The buffer, the width and the height are **three separate things**. Nothing stops us from mixing them up:

```cpp
setPixel(gradient, width, height, x, y, r, g, b);   // width and height of a DIFFERENT image!
```

This compiles. It runs. But it uses the wrong width, so `y × width + x` points at the **wrong pixel** (Chapter 6). These bugs are very hard to find, because the picture just looks "a bit wrong".

There are more risks:
- Someone could `push_back` into the vector, and then its size no longer matches width × height × 3.
- Someone could write `pixels[i]` directly and forget the bounds check.

The fix: put the buffer **and** its size into **one object**, and only allow safe actions on it. That is what a class is for.

📖 **New word: encapsulation** — hiding the inside of an object, so it can only be changed in safe ways.

---

## 11.2 What goes into the class?

Our `Image` class has:

**Private data** (hidden):

| Member | Meaning |
|---|---|
| `width_` | width in pixels |
| `height_` | height in pixels |
| `pixels_` | the buffer: `width_ × height_ × 3` bytes, RGB, row-major, top row first (Chapter 6) |

The `_` at the end of the names is a common habit. It shows "this is a member", so it does not clash with function names like `width()`.

**Public actions** (what users of the class may do):

| Function | What it does |
|---|---|
| `Image(w, h, fill)` | Make a new image, filled with one colour. |
| `width()`, `height()` | Ask for the size. |
| `isInside(x, y)` | Is (x, y) a real pixel? (Chapter 3) |
| `setPixel(x, y, colour)` | Set one pixel, safely. (Chapter 6) |
| `getPixel(x, y)` | Read one pixel. |
| `clear(colour)` | Fill the whole image with one colour. |
| `data()` | Look at the raw bytes (read only). |
| `savePPM(fileName)` | Save as P6. (Chapter 9) |

📖 **New word: invariant** — a rule about an object that is **always** true.

Our invariant:

> **`pixels_.size()` is always exactly `width_ × height_ × 3`.**

The constructor makes it true. No public function can break it (there is no way to add or remove bytes from outside). So every function inside the class can **trust** it. That is why `setPixel` only needs to check (x, y) — it never needs to check the vector's size.

🧠 **Remember:** An `Image` is its size **plus** its pixels, kept together. The buffer is always `width × height × 3` bytes.

---

## 11.3 The `Colour` type

In Chapter 5 we made a `Colour` struct. Now we give its members **default values**:

```cpp
struct Colour {
    std::uint8_t r = 0;
    std::uint8_t g = 0;
    std::uint8_t b = 0;
};
```

So `Colour c;` is black, not random bytes. We can still write `Colour{255, 128, 0}` to give all three values.

Passing one `Colour` instead of three bytes makes calls shorter and safer:

```cpp
setPixel(gradient, size, size, x, y, 255, 128, 0);   // before: 8 arguments
gradient.setPixel(x, y, Colour{255, 128, 0});        // after: 3 arguments
```

### Named colours

We also add the 8 corner colours from Chapter 5, with names:

```cpp
namespace colours {
    const Colour red {255, 0, 0};
    // ...
}
```

Now we can write `colours::red` instead of `Colour{255, 0, 0}`. The `namespace` keeps these names in their own group, so they do not clash with other names like a variable called `red`.

💡 **Tip:** A `const` variable at namespace scope in a header is safe to include in many `.cpp` files. Each file gets its own copy, and the linker does not complain.

---

## 11.4 A header-only file

📖 **New word: library code** — code we write once and use in many programs.

📖 **New word: header-only** — library code that lives completely in a `.h` file.

You know headers and `.cpp` files. Why put **everything** in one header?

- There is **one** file to copy into each project.
- There is **nothing extra to compile or link**. You just write `#include "image.h"`.
- Functions defined **inside** a class body are automatically allowed to appear in many `.cpp` files (they are "inline"). So there is no "defined twice" error.

For a library of this size, that is the simplest choice.

### Include guards

📖 **New word: include guard** — three lines that stop a header from being included twice.

```cpp
#ifndef IMAGE_H
#define IMAGE_H
// ... the whole header ...
#endif
```

| Line | Meaning |
|---|---|
| `#ifndef IMAGE_H` | "If the name `IMAGE_H` is **not** defined yet…" |
| `#define IMAGE_H` | "…define it now…" |
| (the header) | "…and read the header." |
| `#endif` | End of the "if". |

The **second** time the same header is included (for example, from another header later in the book), `IMAGE_H` is already defined, so everything up to `#endif` is skipped. Without this, the compiler would see `struct Colour` twice and stop with an error.

💡 **Tip:** Many compilers also understand `#pragma once` for the same job. It is shorter, but it is not part of the official C++ standard. Since this book uses only standard C++, we use include guards.

---

## 11.5 The constructor and the order of members

📖 **New word: member initialiser list** — the part of a constructor after the `:` that gives each member its first value.

```cpp
Image(int width, int height, Colour fill = colours::black)
    : width_(width > 0 ? width : 0),
      height_(height > 0 ? height : 0),
      pixels_(width_ * height_ * 3, 0) {
    clear(fill);
}
```

Three things to notice:

**1. Negative sizes become 0.** `width > 0 ? width : 0` means "use `width` if it is positive, otherwise 0". An image with width −5 makes no sense. An image with width 0 is empty but safe: it has 0 bytes, and `isInside` is always `false`.

🔢 **Maths: what if someone writes `Image img(-5, 10);`?**

> width_ = 0 (because −5 is not > 0)
> height_ = 10
> pixels_ size = 0 × 10 × 3 = 0 bytes
> The invariant holds: 0 = 0 × 10 × 3 ✓

**2. `pixels_` uses `width_` and `height_`.** This only works if `width_` and `height_` **already have their values** when `pixels_` is made.

⚠️ **Careful:** C++ initialises members in the order they are **declared in the class**, not the order you write them after the `:`. In our class, the members are declared like this (at the bottom):

```cpp
int width_;
int height_;
std::vector<std::uint8_t> pixels_;
```

`width_` and `height_` come **first**, so they are ready before `pixels_`. If you moved `pixels_` above `width_`, it would be made **first**, using `width_` and `height_` before they have values. The vector could get any size at all. This is a classic C++ trap. (Most compilers warn about it with `-Wall`.)

**3. The fill colour has a default.** `Colour fill = colours::black` means you may leave it out: `Image img(100, 50);` makes a black image. `Image img(100, 50, colours::white);` makes a white one.

---

## 11.6 Reading pixels and `const`

```cpp
Colour getPixel(int x, int y) const {
    if (!isInside(x, y)) {
        return colours::black;
    }
    int i = index(x, y);
    return Colour{pixels_[i], pixels_[i + 1], pixels_[i + 2]};
}
```

- The `const` after the `()` promises: this function does **not** change the image. You can call it on a `const Image&`.
- If (x, y) is **outside**, we return **black**. We must return *something*, and black is a calm choice. Later, in blur (Chapter 50), we will look at better choices for pixels outside the edge.
- `index(x, y)` is a small **private** helper that does `(y × width_ + x) × 3`. We write this formula **once**, in one place. If it is right there, it is right everywhere.

---

## 11.7 Where to put `image.h`

📖 **New word: include path** — a folder where the compiler looks for header files.

We will use `image.h` in almost every chapter from now on. So we keep **one** copy in a shared folder:

```
image-work/
  common/
    image.h          ← the one and only copy
  ch11/
    use_image.cpp
  ch12/
    ...
```

In `use_image.cpp` we write `#include "image.h"`. To tell the compiler to look in `common/`, we add `-I` and the folder:

```
cd image-work/ch11
g++ -std=c++17 -Wall -Wextra -O2 -I ../common use_image.cpp -o use_image
```

| Part | Meaning |
|---|---|
| `-I ../common` | "Also look for headers in the folder `common`, one level up." `..` means "the folder above". |

With Microsoft `cl`, the same flag is `/I ..\common`.

💡 **Tip:** In this book's own files, `image.h` is in `code/common/image.h`.

🧠 **Remember:** From now on, every program starts with `#include "image.h"` and is compiled with `-I ../common`. When a later chapter **adds** to `image.h`, it shows the new parts, and you add them to your one copy.

---

## Code, part 1: the library

File: `common/image.h`

```cpp
#ifndef IMAGE_H
#define IMAGE_H

#include <cstdint>
#include <fstream>
#include <string>
#include <vector>

struct Colour {
    std::uint8_t r = 0;
    std::uint8_t g = 0;
    std::uint8_t b = 0;
};

namespace colours {
    const Colour black   {0, 0, 0};
    const Colour white   {255, 255, 255};
    const Colour red     {255, 0, 0};
    const Colour green   {0, 255, 0};
    const Colour blue    {0, 0, 255};
    const Colour yellow  {255, 255, 0};
    const Colour cyan    {0, 255, 255};
    const Colour magenta {255, 0, 255};
}

class Image {
public:
    Image(int width, int height, Colour fill = colours::black)
        : width_(width > 0 ? width : 0),
          height_(height > 0 ? height : 0),
          pixels_(width_ * height_ * 3, 0) {
        clear(fill);
    }

    int width() const { return width_; }
    int height() const { return height_; }

    bool isInside(int x, int y) const {
        return x >= 0 && x < width_ && y >= 0 && y < height_;
    }

    void setPixel(int x, int y, Colour c) {
        if (!isInside(x, y)) {
            return;
        }
        int i = index(x, y);
        pixels_[i]     = c.r;
        pixels_[i + 1] = c.g;
        pixels_[i + 2] = c.b;
    }

    Colour getPixel(int x, int y) const {
        if (!isInside(x, y)) {
            return colours::black;
        }
        int i = index(x, y);
        return Colour{pixels_[i], pixels_[i + 1], pixels_[i + 2]};
    }

    void clear(Colour c) {
        for (int p = 0; p < width_ * height_; ++p) {
            pixels_[p * 3]     = c.r;
            pixels_[p * 3 + 1] = c.g;
            pixels_[p * 3 + 2] = c.b;
        }
    }

    const std::vector<std::uint8_t>& data() const { return pixels_; }

    bool savePPM(const std::string& fileName) const {
        std::ofstream file(fileName, std::ios::binary);
        if (!file) {
            return false;
        }
        file << "P6\n" << width_ << " " << height_ << "\n255\n";
        file.write(reinterpret_cast<const char*>(pixels_.data()),
                   static_cast<std::streamsize>(pixels_.size()));
        return static_cast<bool>(file);
    }

private:
    int index(int x, int y) const {
        return (y * width_ + x) * 3;
    }

    int width_;
    int height_;
    std::vector<std::uint8_t> pixels_;
};

#endif
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1 | `#ifndef IMAGE_H` | Include guard, part 1: only go on if `IMAGE_H` is not defined yet (Section 11.4). |
| 2 | `#define IMAGE_H` | Include guard, part 2: define it, so a second include skips everything. |
| 4 | `#include <cstdint>` | `std::uint8_t`. |
| 5 | `#include <fstream>` | `std::ofstream`, for `savePPM`. |
| 6 | `#include <string>` | `std::string`, for file names. |
| 7 | `#include <vector>` | `std::vector`, for the pixel buffer. |
| 9 | `struct Colour {` | One colour (Chapter 5). |
| 10–12 | `std::uint8_t r = 0;` … | Red, green, blue. `= 0` gives each one a default, so a plain `Colour c;` is black (Section 11.3). |
| 13 | `};` | End of `Colour`. |
| 15 | `namespace colours {` | A group of named colours. You use them as `colours::red`. |
| 16–23 | `const Colour black {0, 0, 0};` … | The 8 corner colours of the RGB cube (Chapter 5, Section 5.3). |
| 24 | `}` | End of the namespace. |
| 26 | `class Image {` | Our image class. |
| 27 | `public:` | Everything below, until `private:`, can be used from outside. |
| 28 | `Image(int width, int height, Colour fill = colours::black)` | The constructor. The fill colour is optional; if you leave it out, it is black. |
| 29 | `: width_(width > 0 ? width : 0),` | Set `width_`. A negative or zero width becomes 0 (Section 11.5). |
| 30 | `height_(height > 0 ? height : 0),` | The same for `height_`. |
| 31 | `pixels_(width_ * height_ * 3, 0) {` | Make the buffer with exactly `width_ × height_ × 3` bytes, all 0. This makes the **invariant** true. It uses `width_` and `height_`, which are already set because they are declared first (Section 11.5). |
| 32 | `clear(fill);` | Fill every pixel with the fill colour. |
| 33 | `}` | End of the constructor. |
| 35 | `int width() const { return width_; }` | Give back the width. `const`: it does not change the image. |
| 36 | `int height() const { return height_; }` | Give back the height. |
| 38–40 | `bool isInside(int x, int y) const { ... }` | Is (x, y) a real pixel? The same four tests as Chapter 3, using the image's own size. |
| 42 | `void setPixel(int x, int y, Colour c) {` | Set pixel (x, y) to colour `c`. |
| 43–45 | `if (!isInside(x, y)) { return; }` | Outside the image? Do nothing (Chapter 6, Section 6.9). |
| 46 | `int i = index(x, y);` | Find the pixel's first byte with our private helper (line 82). |
| 47–49 | `pixels_[i] = c.r;` … | Write red, green and blue into the three bytes. |
| 50 | `}` | End of `setPixel`. |
| 52 | `Colour getPixel(int x, int y) const {` | Read pixel (x, y). `const`: reading does not change the image. |
| 53–55 | `if (!isInside(x, y)) { return colours::black; }` | Outside? Give back black (Section 11.6). |
| 56 | `int i = index(x, y);` | The pixel's first byte. |
| 57 | `return Colour{pixels_[i], pixels_[i + 1], pixels_[i + 2]};` | Build a `Colour` from the three bytes and give it back. |
| 58 | `}` | End of `getPixel`. |
| 60 | `void clear(Colour c) {` | Fill the whole image with one colour. |
| 61 | `for (int p = 0; p < width_ * height_; ++p) {` | Go through every pixel by **pixel number** — no x or y needed (Chapter 6, Example 2). |
| 62–64 | `pixels_[p * 3] = c.r;` … | Write the three channels of pixel `p`. No bounds check is needed: `p` is always from 0 to `width_ × height_ − 1`, and the invariant says the buffer is big enough. |
| 65–66 | `}` `}` | End of the loop and of `clear`. |
| 68 | `const std::vector<std::uint8_t>& data() const { return pixels_; }` | Let other code **look** at the raw bytes (for example, to save other file formats). It returns a `const` reference: no copy, and no way to change the bytes or the size. The invariant stays safe. |
| 70 | `bool savePPM(const std::string& fileName) const {` | Save the image as a P6 file. `const`: saving does not change the image. |
| 71–74 | `std::ofstream file(fileName, std::ios::binary); if (!file) { return false; }` | Open in binary mode; stop if it fails. The same as Chapter 9. |
| 75 | `file << "P6\n" << width_ << " " << height_ << "\n255\n";` | The P6 header, with exactly one `\n` after 255. |
| 76–77 | `file.write(reinterpret_cast<const char*>(pixels_.data()), ...);` | Write the whole buffer in one call. |
| 78 | `return static_cast<bool>(file);` | `true` if it all worked. |
| 79 | `}` | End of `savePPM`. |
| 81 | `private:` | Everything below can only be used **inside** the class. |
| 82 | `int index(int x, int y) const {` | The private helper: where does pixel (x, y) start? |
| 83 | `return (y * width_ + x) * 3;` | The Chapter 6 formula. It is written **only here** in the whole library. |
| 84 | `}` | End of `index`. |
| 86 | `int width_;` | The width. Declared **first**… |
| 87 | `int height_;` | …then the height… |
| 88 | `std::vector<std::uint8_t> pixels_;` | …then the buffer. This order is important (Section 11.5). |
| 89 | `};` | End of the class. |
| 91 | `#endif` | End of the include guard. |

---

## Code, part 2: using the class

File: `ch11/use_image.cpp`

```cpp
#include <iostream>
#include "image.h"

void printColour(const std::string& label, Colour c) {
    std::cout << label << " = (" << static_cast<int>(c.r) << ", "
              << static_cast<int>(c.g) << ", "
              << static_cast<int>(c.b) << ")\n";
}

int main() {
    Image first(3, 2);
    first.setPixel(0, 0, colours::red);
    first.setPixel(1, 0, colours::green);
    first.setPixel(2, 0, colours::blue);
    first.setPixel(0, 1, colours::yellow);
    first.setPixel(1, 1, colours::white);
    first.setPixel(2, 1, colours::black);

    Image stripes(90, 60, colours::white);
    for (int y = 0; y < stripes.height(); ++y) {
        for (int x = 0; x < stripes.width(); ++x) {
            if (y < 20) {
                stripes.setPixel(x, y, Colour{255, 128, 0});
            } else if (y >= 40) {
                stripes.setPixel(x, y, Colour{0, 128, 255});
            }
        }
    }

    Image gradient(256, 256);
    for (int y = 0; y < gradient.height(); ++y) {
        for (int x = 0; x < gradient.width(); ++x) {
            Colour c{static_cast<std::uint8_t>(x), static_cast<std::uint8_t>(y), 128};
            gradient.setPixel(x, y, c);
        }
    }

    bool ok = first.savePPM("first.ppm");
    ok = ok && stripes.savePPM("stripes.ppm");
    ok = ok && gradient.savePPM("gradient.ppm");
    if (!ok) {
        std::cout << "could not write the files\n";
        return 1;
    }

    printColour("gradient (200, 50)", gradient.getPixel(200, 50));
    printColour("gradient (300, 300)", gradient.getPixel(300, 300));
    printColour("stripes (10, 30)", stripes.getPixel(10, 30));
    std::cout << "stripes is " << stripes.width() << " x " << stripes.height()
              << ", " << stripes.data().size() << " bytes\n";
    return 0;
}
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1 | `#include <iostream>` | Printing. |
| 2 | `#include "image.h"` | Our library. The quotes `" "` (not `< >`) mean "our own header". The compiler finds it with `-I ../common`. |
| 4 | `void printColour(const std::string& label, Colour c) {` | A small helper that prints a label and a colour as three numbers. |
| 5–7 | `std::cout << label << " = (" << static_cast<int>(c.r) ...` | Print `label = (r, g, b)`. Each byte is cast to `int` so it prints as a number (Chapter 4). |
| 8 | `}` | End of `printColour`. |
| 10 | `int main() {` | The program starts here. |
| 11 | `Image first(3, 2);` | A 3 × 2 image. No fill colour given, so it is black. |
| 12–17 | `first.setPixel(0, 0, colours::red);` … | The six colours of our first image (Chapter 8), now with named colours. Compare with Chapter 8: each call is much shorter. |
| 19 | `Image stripes(90, 60, colours::white);` | A 90 × 60 image, filled with **white**. |
| 20–21 | `for (int y = 0; y < stripes.height(); ++y) { for (int x ...` | Every pixel. We ask the image for its size, so we can never use the wrong one. |
| 22–23 | `if (y < 20) { stripes.setPixel(x, y, Colour{255, 128, 0}); }` | The top third (rows 0 to 19): orange. |
| 24–25 | `else if (y >= 40) { stripes.setPixel(x, y, Colour{0, 128, 255}); }` | The bottom third (rows 40 to 59): sky blue. |
| 26–28 | `}` `}` `}` | Rows 20 to 39 are not touched, so they stay **white** from the fill. |
| 30 | `Image gradient(256, 256);` | A 256 × 256 black image. |
| 31–32 | `for (int y ...) { for (int x ...` | Every pixel. |
| 33 | `Colour c{static_cast<std::uint8_t>(x), static_cast<std::uint8_t>(y), 128};` | The gradient colour: red = x, green = y, blue = 128 (Chapter 8, Section 8.8). |
| 34 | `gradient.setPixel(x, y, c);` | Set it. |
| 35–36 | `}` `}` | End of the loops. |
| 38–40 | `bool ok = first.savePPM("first.ppm"); ...` | Save all three images as P6. |
| 41–44 | `if (!ok) { ...; return 1; }` | Stop if any save failed. |
| 46 | `printColour("gradient (200, 50)", gradient.getPixel(200, 50));` | Read back one pixel. It should be (200, 50, 128). |
| 47 | `printColour("gradient (300, 300)", gradient.getPixel(300, 300));` | Read a pixel **outside** the image. `getPixel` gives black, with no crash. |
| 48 | `printColour("stripes (10, 30)", stripes.getPixel(10, 30));` | A pixel in the middle stripe. It should be white. |
| 49–50 | `std::cout << "stripes is " << ... << stripes.data().size() << " bytes\n";` | Print the size, and the number of bytes in the buffer. |
| 51 | `return 0;` | The program finished with no problem. |
| 52 | `}` | End of `main`. |

### What you should see

```
gradient (200, 50) = (200, 50, 128)
gradient (300, 300) = (0, 0, 0)
stripes (10, 30) = (255, 255, 255)
stripes is 90 x 60, 16200 bytes
```

🔢 **Maths: check the byte count**

> 90 × 60 = 5,400 pixels
> 5,400 × 3 = **16,200 bytes** ✓ (the invariant)

Open `stripes.ppm`: three bands — orange, white and blue. `first.ppm` and `gradient.ppm` look exactly like Chapters 8 and 9. **The class changed how we write the code, not what the files contain.**

---

## Small examples

### Example 1 — A checkerboard with the class

The checkerboard from Chapter 10, now in colour, 8 × 8 squares of 10 pixels each:

```cpp
Image board(80, 80);
for (int y = 0; y < board.height(); ++y) {
    for (int x = 0; x < board.width(); ++x) {
        bool dark = ((x / 10) + (y / 10)) % 2 == 0;
        board.setPixel(x, y, dark ? colours::black : colours::white);
    }
}
board.savePPM("board.ppm");
```

> `x / 10` is the square's column (0 to 7). `y / 10` is its row.
> Pixel (25, 13): 25 / 10 = 2, 13 / 10 = 1, 2 + 1 = 3, 3 % 2 = 1 → not dark → **white**.

### Example 2 — Drawing outside is harmless

```cpp
Image small(10, 10);
for (int x = -5; x < 20; ++x) {
    small.setPixel(x, 5, colours::red);
}
```

The loop tries 25 pixels, from x = −5 to x = 19. Only x = 0 to 9 are inside. The other 15 calls do nothing. The result: one red line across row 5, exactly 10 pixels long. No crash, and no "wrap-around" to the next row.

### Example 3 — Copying an image

Because `Image` only holds an `int`, an `int` and a `std::vector`, C++ can copy it for us:

```cpp
Image copy = gradient;          // a full, separate copy of all 196,608 bytes
copy.setPixel(0, 0, colours::white);
```

Changing `copy` does **not** change `gradient`. (This is useful later, for example in blur, where we read from one image and write into another.)

⚠️ But copying a big image takes time and memory. Pass images to functions as `const Image&` (read only) or `Image&` (to change), not by value.

### Example 4 — A function that takes an `Image`

```cpp
void drawBorder(Image& img, Colour c) {
    for (int x = 0; x < img.width(); ++x) {
        img.setPixel(x, 0, c);
        img.setPixel(x, img.height() - 1, c);
    }
    for (int y = 0; y < img.height(); ++y) {
        img.setPixel(0, y, c);
        img.setPixel(img.width() - 1, y, c);
    }
}
```

This works for **any** image, of any size, because it asks the image for its own width and height. Compare with Chapter 8, Practice 7, where we had to pass `n` around.

---

## Common mistakes

⚠️ **Changing the member order.** If `pixels_` is declared before `width_` and `height_`, the vector is made with garbage sizes. Keep the order: `width_`, `height_`, `pixels_`.

⚠️ **Forgetting `-I ../common`.** The compiler says something like "`image.h`: No such file or directory".

⚠️ **Several copies of `image.h`.** If each chapter folder has its own copy, a fix in one copy does not reach the others. Keep **one** copy in `common/`.

⚠️ **Passing an `Image` by value.** `void draw(Image img)` copies the whole image, and changes are lost when the function ends. Use `Image&`.

⚠️ **Thinking `getPixel` outside gives an error.** It gives **black**. If your shape suddenly has black edges where it touches the border of the image, this may be why.

⚠️ **Writing `Colour{300, 0, 0}`.** 300 does not fit into a `std::uint8_t`. With braces, the compiler gives an error ("narrowing"). That is good! It stops a wrap-around bug before it happens.

---

## Practice

🏋️ **1.** What is the invariant of our `Image` class? Which line makes it true?

🏋️ **2.** `Image a(0, 100);` — how many bytes are in its buffer? What does `a.isInside(0, 0)` return?

🏋️ **3.** Write a program that makes a 100 × 100 image, all cyan, and saves it.

🏋️ **4.** Add a function `fillRow(Image& img, int y, Colour c)` that colours a whole row. Use it to draw a red line across row 50 of a 100 × 100 image.

🏋️ **5.** Add a member function `int byteCount() const` to `Image` that returns the number of bytes in the buffer. (Hint: one line.)

🏋️ **6.** Why does `getPixel` need the `const` after its `()`? Write one line of code that would **not** compile without it.

🏋️ **7.** Make an image with **4 vertical stripes** of equal width, coloured red, green, blue and yellow, 200 × 100. (Hint: the stripe number is `x / 50`.)

---

## Answers

**1.** `pixels_.size()` is always `width_ × height_ × 3`. Line 31 makes it true: `pixels_(width_ * height_ * 3, 0)`. No public function adds or removes bytes, so it stays true.

**2.**
> width_ = 0 (0 is not > 0), height_ = 100
> bytes = 0 × 100 × 3 = **0**
> `isInside(0, 0)`: 0 < width_ is 0 < 0 → false → returns **false**

**3.**

```cpp
#include "image.h"

int main() {
    Image img(100, 100, colours::cyan);
    img.savePPM("cyan.ppm");
    return 0;
}
```

The fill colour does all the work. No loops needed.

**4.**

```cpp
void fillRow(Image& img, int y, Colour c) {
    for (int x = 0; x < img.width(); ++x) {
        img.setPixel(x, y, c);
    }
}

// in main:
Image img(100, 100, colours::white);
fillRow(img, 50, colours::red);
img.savePPM("row.ppm");
```

`Image&`: the function changes the **real** image.

**5.** Inside the `public:` part of the class:

```cpp
int byteCount() const { return static_cast<int>(pixels_.size()); }
```

**6.** Without `const`, you cannot call `getPixel` on a `const Image`. For example, this would not compile:

```cpp
void printTopLeft(const Image& img) {
    Colour c = img.getPixel(0, 0);   // error if getPixel is not const
}
```

Functions like this — that only **read** an image — are very common (saving files, blur, edge detection), so the reading functions must be `const`.

**7.**

```cpp
Image img(200, 100);
const Colour stripeColours[4] = {colours::red, colours::green, colours::blue, colours::yellow};
for (int y = 0; y < img.height(); ++y) {
    for (int x = 0; x < img.width(); ++x) {
        int stripe = x / 50;
        img.setPixel(x, y, stripeColours[stripe]);
    }
}
img.savePPM("four_stripes.ppm");
```

> width 200 ÷ 4 stripes = 50 pixels each.
> x = 0–49 → stripe 0 (red), 50–99 → 1 (green), 100–149 → 2 (blue), 150–199 → 3 (yellow).
> The largest x is 199 → 199 / 50 = 3. So `stripe` is never 4, and we never read past the end of the array.

---

## Summary

🧠 Passing `pixels, width, height` separately invites mix-ups. An **`Image` class** keeps them together.

🧠 The **invariant**: the buffer always has exactly `width × height × 3` bytes.

🧠 `Colour` has default values (black), and `colours::red` etc. give us named colours.

🧠 `image.h` is **header-only**, with **include guards**. Keep **one** copy in `common/`, and compile with `-I ../common`.

🧠 Members are initialised in **declaration order**: `width_` and `height_` must come before `pixels_`.

🧠 `setPixel` ignores pixels outside. `getPixel` gives black outside.

🧠 Reading functions are `const`. Pass images as `const Image&` or `Image&`.

---

## Next chapter

So far we only **write** images. In Chapter 12 we **read** them: we write our own small parser for PPM files (both P3 and P6), turning text digits into numbers by hand, and we add `loadPPM` to `image.h`. Then we can open a picture, change it, and save it again.
