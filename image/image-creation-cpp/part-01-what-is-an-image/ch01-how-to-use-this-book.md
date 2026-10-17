# Chapter 1 — How to Use This Book

> **Part 1 · Chapter 1 of 82**
> **You need:** basic C++ (you already have it) · **You will make:** a project folder and a small test program

---

## What you will learn

- What this book will teach you, and what it will **not** teach you.
- What "from scratch" means in this book.
- How every chapter is built, so you always know where to look.
- How to set up one folder for all your work.
- How to check that your compiler is ready for the rest of the book.
- Which programs you can use to **look at** the images you make.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **image** | A picture that is stored inside a computer. |
| **pixel** | One very small square of colour. An image is made of many pixels. |
| **file format** | The rules for how the bytes inside a file are arranged. |
| **from scratch** | Starting from nothing. We build everything ourselves. |
| **library** | Code that someone else wrote, which you add to your program. |
| **standard library** | The code that comes with every C++ compiler, like `<vector>` and `<fstream>`. |
| **image viewer** | A program that opens an image file and shows it on the screen. |
| **algorithm** | A list of exact steps that solves a problem. |

---

## 1.1 What this book is about

This book teaches you how to **make pictures with C++**.

Not by using a drawing program.
Not by calling a library that does the work for you.
You will write **every part yourself**.

At the start, your pictures will be very small.
The first one will be only **3 pixels wide and 2 pixels tall**.
That is 6 small squares of colour. That is all.

By the end of the book, your programs will make pictures like these:

- smooth colour gradients, like a sunset sky
- lines, circles, triangles and curves with smooth edges
- text, drawn with your own font
- blurred, sharpened and edge-detected photos
- clouds, marble and wood made from maths (we call this **noise**)
- the famous Mandelbrot fractal
- a 3D cube with light and shadow
- shiny glass and mirror balls, made with **ray tracing**
- a short moving picture (an animated GIF)

And you will save them in real file formats, like **BMP**, **PNG** and **GIF**.
You will write the code for these formats yourself, **byte by byte**.

🧠 **Remember:** In this book, *you* write every line. Nothing is hidden.

---

## 1.2 What "from scratch" means

📖 **New word: from scratch** — starting from nothing. We do not use ready-made parts.

📖 **New word: library** — code that someone else wrote. You add it to your program so you do not have to write that part.

Many people make images in C++ with libraries. Some well-known ones are:

| Library | What it does |
|---|---|
| `stb_image` | reads and writes PNG, JPG, BMP |
| `libpng` | reads and writes PNG |
| `zlib` | compresses data (PNG needs this) |
| OpenCV | changes photos (blur, edges, and much more) |
| SDL, SFML | shows pictures in a window |

These are good tools. But they **hide** how images work.
You call one function, and a picture appears. You do not learn *why*.

In this book we use **none of them**.

📖 **New word: standard library** — the code that comes with every C++ compiler. For example `<vector>`, `<string>`, `<fstream>` and `<cmath>`.

We only use the standard library. This is the full list of headers we will use in the whole book:

| Header | Why we need it |
|---|---|
| `<iostream>` | print messages to the terminal |
| `<fstream>` | write and read files |
| `<vector>` | hold all the pixels of an image |
| `<string>` | file names and text |
| `<cstdint>` | exact byte types like `std::uint8_t` |
| `<cmath>` | `std::sqrt`, `std::sin`, `std::cos`, `std::floor` |
| `<algorithm>` | `std::min`, `std::max`, `std::clamp`, `std::swap` |
| `<array>` | small fixed lists, like 3 colour values |

That is all. If a header is not on this list, we do not use it.

💡 **Tip:** We do not even use `<random>`. In Chapter 54 we write our own random number maker, so you can see how it works.

---

## 1.3 What this book will NOT teach

You told us you already know basic C++. So this book does **not** explain:

- variables and types like `int`, `double`, `bool`
- `if`, `else`, `switch`
- `for` and `while` loops
- functions, parameters and return values
- `std::vector` and `std::string` basics
- `struct` and `class`
- references (`&`) and `const`
- how to split code into `.h` and `.cpp` files

We **use** these all the time. We do not stop to teach them.

But some C++ ideas are very important for images, and many people who know basic C++ have never used them. **These we do explain carefully**, when we first need them:

| C++ idea | Chapter |
|---|---|
| `std::uint8_t` and other fixed-size integers | 4 |
| writing a file in **binary mode** | 7 |
| bit shifts `<<` and `>>` | 4, 36 |
| bit masks with `&` and `|` | 4, 40 |
| **endianness** (the order of bytes in a number) | 36 |
| what happens when an integer is too big (**overflow**) | 14 |
| turning a `double` into an `int` correctly (rounding) | 13 |
| `reinterpret_cast` for writing raw bytes | 7 |

⚠️ **Careful:** "Basic C++" here means the list above. If you have only used C++ for a few days, it is fine. Just look up a loop or a function when you need to. The image ideas are what this book is for.

---

## 1.4 What you DO need to know in maths

You need only **school maths**:

- adding, subtracting, multiplying, dividing
- fractions and decimals, like 0.5 and 1/4
- negative numbers
- what a square and a square root are (3 × 3 = 9, √9 = 3)

Everything else, we teach. This includes:

- coordinates (Chapter 3)
- binary and hexadecimal numbers (Chapter 4)
- interpolation (Chapter 13)
- slopes and lines (Chapter 20)
- the equation of a circle (Chapter 22)
- sine and cosine (Chapter 30)
- vectors and matrices (Chapters 29, 32, 64)
- complex numbers (Chapter 60)
- the quadratic formula (Chapter 72)

🔢 **Maths:** Each time we use maths, we do it **step by step, with real numbers**. For example, we will never just write "index = y × w + x". We will write:

> x = 3, y = 2, w = 5
> index = 2 × 5 + 3
> index = 10 + 3
> index = 13

You can follow every step with a pencil.

💡 **Tip:** Keep a notebook and a pencil near you. Drawing a small grid on paper helps a lot.

---

## 1.5 How every chapter is built

Every chapter has the **same parts in the same order**. So you always know where to look.

| Part of the chapter | What is inside |
|---|---|
| **What you will learn** | A short list of goals. |
| **New words** | A table of every new word, with a simple meaning. |
| **Theory sections** (1.1, 1.2, …) | The idea first, then a picture, then the maths, then a small example. |
| **Code** | A full program, then a table that explains **every line**. |
| **Small examples** | At least three tiny examples, each explained. |
| **Common mistakes** | Things that often go wrong, and how to fix them. |
| **Practice** | Small tasks for you. |
| **Answers** | Full answers to the practice tasks, explained. |
| **Summary** | The most important points, in a few short lines. |
| **Next chapter** | What comes next. |

### The signs

You will see these signs everywhere:

| Sign | Meaning |
|---|---|
| 📖 **New word** | A new word, explained simply. |
| 🔢 **Maths** | Maths, worked step by step. |
| 💡 **Tip** | A helpful idea. |
| ⚠️ **Careful** | A common mistake. Read these! |
| 🧠 **Remember** | The most important idea in a section. |
| 🏋️ **Practice** | A task for you to try. |

### How code is explained

After every program, there is a table like this one:

| Line | Code | What it does, in simple words |
|---|---|---|
| 1 | `#include <fstream>` | Lets us write files. |
| 2 | `int main() {` | The program starts here. |

No line is skipped. If a line is the same as in an earlier chapter, we still list it, but we keep the words short and say "same as Chapter N".

---

## 1.6 The order of the book

📖 **New word: algorithm** — a list of exact steps that solves a problem. For example, "how to draw a line from one pixel to another" is an algorithm.

The book is in **11 parts**. Each part uses only what came before it.

```
Part 1  What is an image?         ← ideas: pixels, numbers, colour, memory
   │
Part 2  First image files         ← we save our first real pictures
   │
Part 3  Maths of colour           ← gradients, grey, HSV, gamma, transparency
   │
Part 4  Drawing shapes            ← lines, circles, triangles, smooth edges
   │
Part 5  Moving and bending        ← vectors, angles, rotation, curves, resizing
   │
Part 6  Real file formats         ← BMP, TGA, PNG (with our own compression)
   │
Part 7  Changing images           ← blur, sharpen, edges, dithering
   │
Part 8  Pictures from maths       ← noise, fractals, Voronoi, L-systems
   │
Part 9  3D by rasterisation       ← camera, cube, light, textures
   │
Part 10 Ray tracing               ← spheres, shadows, mirrors, glass
   │
Part 11 Moving pictures           ← animation, GIF, final project
```

🧠 **Remember:** Read the chapters **in order**. Each chapter stands on the ones before it. If you skip, you will meet words and code you do not know.

---

## 1.7 Setting up your folder

We will keep all our work in **one folder**. Make it now.

Pick any place on your computer. For example:

- Windows: `C:\image-work\`
- macOS or Linux: `~/image-work/`

Inside it, we will make one small folder for each chapter that has code:

```
image-work/
  ch01/
    check.cpp
  ch03/
  ch04/
  ...
```

The images you make will also go into these folders.

💡 **Tip:** This book's own code is in the folder `code/` next to this file. Each chapter's programs are in `code/chNN/`. You can compare your code with it. But **type the code yourself first**. Typing it helps you learn it.

---

## 1.8 Checking your compiler

You already know how to compile C++. In this book we always compile like this:

```
g++ -std=c++17 -Wall -Wextra -O2 check.cpp -o check
```

| Part | Meaning |
|---|---|
| `g++` | the compiler (you may use `clang++` or Microsoft `cl` instead) |
| `-std=c++17` | use the C++17 rules; all book code needs C++17 or newer |
| `-Wall -Wextra` | show many warnings; warnings often point to real mistakes in image code |
| `-O2` | make the program fast; later chapters do millions of pixel calculations |
| `check.cpp` | the source file |
| `-o check` | the name of the program to make |

With Microsoft Visual C++, the same idea is:

```
cl /std:c++17 /W4 /O2 /EHsc check.cpp
```

Now we write one small program. It checks **two things** that the whole book depends on:

1. Your compiler uses C++17 or newer.
2. A "byte" type on your computer is exactly 8 bits.

Do not worry if you do not know what "8 bits" means yet. Chapter 4 explains it fully. For now we only want to see the program say **OK**.

---

## Code

File: `ch01/check.cpp`

```cpp
#include <iostream>
#include <cstdint>
#include <climits>

int main() {
    std::cout << "C++ version number: " << __cplusplus << "\n";

    if (__cplusplus >= 201703L) {
        std::cout << "C++17 or newer: OK\n";
    } else {
        std::cout << "C++17 or newer: NO - please add -std=c++17\n";
    }

    std::cout << "Bits in one char: " << CHAR_BIT << "\n";
    std::cout << "Size of std::uint8_t: " << sizeof(std::uint8_t) << " byte\n";
    std::cout << "Size of std::uint32_t: " << sizeof(std::uint32_t) << " bytes\n";

    if (CHAR_BIT == 8 && sizeof(std::uint32_t) == 4) {
        std::cout << "Byte sizes: OK\n";
    } else {
        std::cout << "Byte sizes: unusual computer\n";
    }

    std::cout << "Ready to make images!\n";
    return 0;
}
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1 | `#include <iostream>` | Lets us print text with `std::cout`. |
| 2 | `#include <cstdint>` | Gives us exact-size number types like `std::uint8_t` and `std::uint32_t`. We will use these for every image. |
| 3 | `#include <climits>` | Gives us `CHAR_BIT`: the number of bits in one byte on this computer. |
| 5 | `int main() {` | The program starts here. |
| 6 | `std::cout << "C++ version number: " << __cplusplus << "\n";` | `__cplusplus` is a number that the compiler fills in. It tells which C++ rules are used. C++17 gives `201703`. C++20 gives `202002`. |
| 8 | `if (__cplusplus >= 201703L) {` | Checks if the number is 201703 or bigger. The `L` at the end means "long number". It is needed because the number is large. |
| 9 | `std::cout << "C++17 or newer: OK\n";` | Prints OK when the compiler is new enough. |
| 10–12 | `} else { ... }` | Otherwise, prints a message that tells you to add `-std=c++17`. |
| 14 | `std::cout << "Bits in one char: " << CHAR_BIT << "\n";` | Prints how many bits are in one `char`. On almost every computer it is 8. |
| 15 | `... sizeof(std::uint8_t) ...` | `sizeof` tells how many bytes a type uses. `std::uint8_t` must be 1 byte. |
| 16 | `... sizeof(std::uint32_t) ...` | `std::uint32_t` must be 4 bytes. We use 4-byte numbers inside BMP and PNG files later. |
| 18 | `if (CHAR_BIT == 8 && sizeof(std::uint32_t) == 4) {` | Both checks must be true. `&&` means "and". |
| 19 | `std::cout << "Byte sizes: OK\n";` | Prints OK when both are true. |
| 20–22 | `} else { ... }` | Prints a warning on a very unusual computer. You will almost never see this. |
| 24 | `std::cout << "Ready to make images!\n";` | A friendly last message. |
| 25 | `return 0;` | Tells the system the program finished with no problem. |
| 26 | `}` | End of `main`. |

### What you should see

```
C++ version number: 201703
C++17 or newer: OK
Bits in one char: 8
Size of std::uint8_t: 1 byte
Size of std::uint32_t: 4 bytes
Byte sizes: OK
Ready to make images!
```

The first number may be bigger, like `202002`. That is fine. Bigger means newer.

⚠️ **Careful:** With Microsoft `cl`, `__cplusplus` shows `199711` even with `/std:c++17`, unless you also add the flag `/Zc:__cplusplus`. So on `cl`, compile with:
```
cl /std:c++17 /Zc:__cplusplus /W4 /O2 /EHsc check.cpp
```

---

## 1.9 How to look at your images

📖 **New word: image viewer** — a program that opens an image file and shows it on the screen.

Our code makes the files. But to **see** them, we need an image viewer.

📖 **New word: file format** — the rules for how bytes are arranged inside a file. For example, PPM, BMP and PNG are file formats.

In Part 2 we use a very simple format called **PPM**. Not every viewer can open PPM files. These can:

| Your computer | Programs that open PPM |
|---|---|
| Windows | IrfanView, GIMP, XnView, Paint.NET (with plugin) |
| macOS | Preview (built in), GIMP |
| Linux | most image viewers (Eye of GNOME, Gwenview, feh), GIMP |
| Any | many free web pages called "PPM viewer" |

From Chapter 37 we also write **BMP** files, and from Chapter 42 **PNG** files. Every computer opens those with no extra program.

💡 **Tip:** Our first images are tiny, like 3 × 2 pixels. On screen, that is smaller than a grain of rice! In your viewer, **zoom in** a lot (800% or more). Most viewers make each pixel a clear square when you zoom in.

⚠️ **Careful:** Some viewers make tiny images **blurry** when you zoom in. They try to "smooth" the picture. Look for an option called "nearest neighbour", "no smoothing" or "pixelated". We learn what "nearest neighbour" means in Chapter 35.

Using a viewer is **not** using a library. The viewer only *shows* the file. Our C++ code *makes* the file, with no help.

---

## Small examples

### Example 1 — What a "6-pixel image" looks like

Our first image (Chapter 8) is 3 pixels across and 2 pixels down:

```
+-----+-----+-----+
| red |green|blue |
+-----+-----+-----+
|yellow|white|black|
+-----+-----+-----+
```

That is all it is: 6 squares, each with one colour. Every image in the world — a photo, a game screen, a film — is the same idea, just with many more squares. A normal phone photo has about **12 million** of them.

### Example 2 — "From scratch" vs. "with a library"

With a library, saving a PNG might be one line:

```cpp
// NOT used in this book:
stbi_write_png("out.png", w, h, 3, pixels, w * 3);
```

In this book, saving a PNG takes **Chapters 40 to 45**. We write the chunks, the checksums and the compression ourselves. It is more work. But after it, you **know** what is inside every PNG file in the world.

### Example 3 — Reading the order of the book

Say you want to draw a smooth circle. Which chapters do you need?

- Chapter 22: circles.
- Chapter 27 or 28: smooth edges.
- And all of Parts 1–3 before them, because they build pixels, files and colours.

So you cannot jump straight to Chapter 22. This is why we say: **read in order**.

### Example 4 — A maths step, the book way

Question: "An image is 4 pixels wide and 3 pixels tall. How many pixels does it have?"

> width = 4
> height = 3
> pixels = width × height
> pixels = 4 × 3
> pixels = 12

Every maths step in this book is written like this.

---

## Common mistakes

⚠️ **Skipping chapters.** Later chapters use words and code from earlier ones. If something is unclear, go back to the chapter it came from. The chapter number is always given.

⚠️ **Forgetting `-std=c++17`.** Some older compilers use an older standard by default. Then later code (like `std::clamp` in Chapter 14) will not compile.

⚠️ **Turning warnings off.** Image code has many small number mistakes, like mixing `int` and `double`. The flags `-Wall -Wextra` catch many of them. Keep them on.

⚠️ **Thinking a tiny image did not work.** A 3 × 2 image looks like *nothing* until you zoom in. Zoom in before you decide something is wrong.

⚠️ **Copying instead of typing.** You will learn much more if you type the code. Small typing mistakes teach you what each part does.

---

## Practice

🏋️ **1.** Make the folder `image-work/` and the folder `image-work/ch01/` on your computer.

🏋️ **2.** Type `check.cpp`, compile it with the command from Section 1.8, and run it. Write down the "C++ version number" you see.

🏋️ **3.** Compile `check.cpp` **without** `-std=c++17`. Does the version number change? (It might, or it might not. It depends on your compiler.)

🏋️ **4.** An image is 5 pixels wide and 4 pixels tall. How many pixels does it have? Write every step, like in Example 4.

🏋️ **5.** A phone camera makes photos that are 4,000 pixels wide and 3,000 pixels tall. How many pixels is that?

🏋️ **6.** Look at the table in Section 1.2. Which header do we need to write a file? Which header do we need for `std::sqrt`?

🏋️ **7.** Install or find one image viewer that can open PPM files on your computer (Section 1.9). You will need it in Chapter 8.

---

## Answers

**1.** There is no output to check. Just make sure both folders exist, and that `ch01` is inside `image-work`.

**2.** You will usually see `201703` (C++17), `202002` (C++20), or `202302` (C++23). Any of these is fine. If you see `199711` or `201402`, add `-std=c++17` (or, on Microsoft `cl`, add `/Zc:__cplusplus`).

**3.** New compilers often use C++17 or newer by default, so the number may stay the same. Older compilers may show `201402` (C++14). This is why we **always** write `-std=c++17`: then we know which rules we get.

**4.**
> width = 5
> height = 4
> pixels = width × height
> pixels = 5 × 4
> pixels = 20

**5.**
> width = 4,000
> height = 3,000
> pixels = 4,000 × 3,000
> First, 4 × 3 = 12.
> Then count the zeros: 4,000 has 3 zeros and 3,000 has 3 zeros. That is 6 zeros.
> pixels = 12 followed by 6 zeros = 12,000,000

That is **twelve million** pixels. People call this "12 megapixels". (*Mega* means million.)

**6.** To write a file we need `<fstream>`. For `std::sqrt` we need `<cmath>`.

**7.** On macOS, Preview already works. On Linux, your normal viewer likely works. On Windows, a free viewer such as IrfanView or GIMP works well. Test it later, in Chapter 8, with your first image.

---

## Summary

🧠 This book teaches how to make images **from scratch** in C++.

🧠 We use **only the C++ standard library**. No image libraries, no extra packages.

🧠 We do **not** teach basic C++. We **do** teach the C++ ideas that images need, like bytes, binary files and bit operations.

🧠 All maths is taught **step by step, with real numbers**. School maths is enough to start.

🧠 Every chapter has the same parts. Every line of code is explained.

🧠 Read the chapters **in order**.

🧠 Compile with `g++ -std=c++17 -Wall -Wextra -O2`.

🧠 Use an image viewer to *see* your files, and **zoom in** on tiny images.

---

## Next chapter

In Chapter 2 we ask a simple question: **what is a picture, really?** We look at light, at how our eyes see colour, and at how a screen fools our eyes with tiny squares called pixels.
