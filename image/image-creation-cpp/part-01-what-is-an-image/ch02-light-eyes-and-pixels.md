# Chapter 2 — Light, Eyes and Pixels

> **Part 1 · Chapter 2 of 82**
> **You need:** Chapter 1 · **You will make:** a program that "draws" a picture from numbers in the terminal

---

## What you will learn

- What light is, in simple words, and what "colour" really means.
- How your eye sees colour with only **three** kinds of cells.
- Why a screen needs only **red, green and blue** to show almost every colour.
- What a pixel is, and why many small pixels look like a smooth picture.
- What **resolution** and **aspect ratio** mean, with the maths.
- How a picture can be written as **a grid of numbers**.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **light** | Energy that travels very fast and lets us see. |
| **wavelength** | The length of one "wave" of light. It decides the colour we see. |
| **nanometre (nm)** | One billionth of a metre. We measure wavelength in nanometres. |
| **spectrum** | All the colours of light, in order, like a rainbow. |
| **retina** | The thin layer at the back of the eye that senses light. |
| **cone cell** | A cell in the retina that senses colour. There are 3 kinds. |
| **rod cell** | A cell in the retina that senses dim light, but not colour. |
| **sub-pixel** | One tiny red, green or blue light inside one screen pixel. |
| **brightness** | How much light something gives out, or seems to give out. |
| **resolution** | How many pixels an image has: width × height. |
| **aspect ratio** | The shape of an image: width compared to height, like 16 : 9. |
| **sample** | One measured value at one place. A pixel is a sample of a picture. |

---

## 2.1 What is light?

📖 **New word: light** — energy that travels very, very fast and lets us see.

Light comes from the Sun, from a lamp, from a phone screen.
It flies through the air, hits things, and some of it comes into your eye.

Scientists describe light as a **wave**. Think of waves on water:

```
   ___       ___       ___
  /   \     /   \     /   \
 /     \___/     \___/     \___
 |<-------->|
  one wave
```

📖 **New word: wavelength** — the length of one wave, from one top to the next top.

Light waves are **very** short. We measure them in nanometres.

📖 **New word: nanometre (nm)** — one billionth of a metre.

🔢 **Maths: how small is a nanometre?**

> 1 metre = 1,000 millimetres
> 1 millimetre = 1,000 micrometres
> 1 micrometre = 1,000 nanometres
> So 1 metre = 1,000 × 1,000 × 1,000 nanometres = 1,000,000,000 nanometres.

A hair is about 0.1 millimetre thick. That is about **100,000 nanometres**.
Light that we can see has a wavelength of about **380 to 700 nanometres**.
So about 150 to 250 light waves fit across the width of one hair.

---

## 2.2 Colour is wavelength

Different wavelengths look like **different colours** to us.

📖 **New word: spectrum** — all the colours of light, in order of wavelength. A rainbow shows the spectrum.

```
wavelength (nm):  380    450    500    550    600    650    700
                   |------|------|------|------|------|------|
colour we see:    violet  blue   cyan  green  yellow orange  red
```

- Short waves (about 450 nm) look **blue**.
- Middle waves (about 550 nm) look **green**.
- Long waves (about 650 nm) look **red**.
- Waves shorter than 380 nm (ultraviolet) or longer than 700 nm (infrared) are **invisible** to us.

White light, like sunlight, is **a mix of all of them at once**. A glass prism can split white light into a rainbow. That shows the mix.

🧠 **Remember:** A colour is not "inside" an object. A red apple **sends back** mostly long-wave light and **soaks up** the rest. Our eye sees the long waves, and our brain says "red".

---

## 2.3 How your eye sees colour

📖 **New word: retina** — the thin layer at the back of your eye. It has millions of cells that sense light.

There are two kinds of light-sensing cells:

📖 **New word: rod cell** — senses dim light. It does not see colour. It helps you see at night.

📖 **New word: cone cell** — senses colour. It needs more light.

Here is the key fact for this whole book:

> **There are only three kinds of cone cells.**

| Cone | Best at | We call it |
|---|---|---|
| S cone ("short") | short waves, about 420 nm | the **blue** cone |
| M cone ("medium") | medium waves, about 530 nm | the **green** cone |
| L cone ("long") | long waves, about 560 nm | the **red** cone |

Each cone sends the brain **one number**: "how much light did I get?"
So for every point you look at, the brain gets only **three numbers**:

```
          light comes in
                │
     ┌──────────┼──────────┐
     ▼          ▼          ▼
  L cone      M cone     S cone
 ("red")    ("green")   ("blue")
     │          │          │
   0.8        0.6        0.1        ← three numbers
     └──────────┼──────────┘
                ▼
         brain: "orange!"
```

The brain turns the three numbers into a colour.

### Why this matters for computers

If the brain only gets three numbers, then we only need to **make those three numbers** to fool it.

We do not need to make the real orange light (about 600 nm).
We can mix a lot of **red light** with some **green light**.
The cones get almost the same three numbers.
The brain says "orange" — and it cannot tell the difference!

🧠 **Remember:** Because the eye has three kinds of cones, **three numbers — red, green, blue — are enough to describe a colour** for a human. This is why images store colour as **R, G, B**. Chapter 5 explains this in detail.

---

## 2.4 How a screen shows a picture

Look at a screen through a strong magnifying glass, or take a photo of it zoomed in. You will see something like this:

```
 R G B R G B R G B R G B
 R G B R G B R G B R G B
 R G B R G B R G B R G B
```

📖 **New word: sub-pixel** — one tiny light inside a screen pixel. It shines only red, only green, or only blue.

📖 **New word: pixel** — one small square of the picture. On a screen, one pixel is made of 3 sub-pixels: one red, one green, one blue.

```
 one pixel
 ┌───────┐
 │ R G B │   ← three tiny lights, side by side
 └───────┘
```

Each sub-pixel can be made **brighter or darker**.

📖 **New word: brightness** — how much light something gives out (or seems to give out).

| Red light | Green light | Blue light | What you see |
|---|---|---|---|
| full | off | off | red |
| off | full | off | green |
| off | off | full | blue |
| full | full | off | yellow |
| full | full | full | white |
| off | off | off | black |
| half | half | half | grey |

The lights are so small and so close that your eye cannot see them apart. It **mixes** them into one colour.

💡 **Tip:** Try it. Look at a white part of your screen with a magnifying glass, or zoom in with your phone camera. You will see red, green and blue lights — no white ones at all!

---

## 2.5 Many small squares make a smooth picture

A photo looks smooth. But it is really **a grid of squares**. Here is a circle made of pixels, very zoomed in:

```
. . . # # # . . .
. # # # # # # # .
. # # # # # # # .
# # # # # # # # #
# # # # # # # # #
# # # # # # # # #
. # # # # # # # .
. # # # # # # # .
. . . # # # . . .
```

With only 9 × 9 pixels, the circle looks like steps. Now imagine the same circle with **1,000 × 1,000** pixels. Each step would be so small that you could not see it. It would look perfectly round.

🧠 **Remember:** A computer image is **always** a grid of pixels. "Smooth" just means the pixels are too small to see.

---

## 2.6 A pixel is a sample

📖 **New word: sample** — one value measured at one place.

Think of a real scene: a sky, a tree, a cat. Colour changes **smoothly** from place to place. There are endless places.

A computer cannot store endless places. So it **measures the colour at a grid of places**, and stores only those.

```
real scene (smooth)          samples (a grid)
                             x   x   x   x
  ~~~sky~~~                  x   x   x   x
    ~tree~         ──►       x   x   x   x
  ~~~grass~~~                x   x   x   x
```

Each `x` is one sample. Each sample becomes one pixel.

This idea is very important later:

- In Chapter 27 (smooth edges) we take **many** samples inside one pixel and mix them.
- In Chapter 35 (resizing) we **re-sample** an image to a new grid.
- In Chapter 71 (ray tracing) we send one ray per sample.

For now, just remember: **one pixel = one colour = one sample**.

---

## 2.7 Resolution

📖 **New word: resolution** — how many pixels an image has, written as **width × height**.

| Name | Width | Height |
|---|---|---|
| a tiny icon | 16 | 16 |
| old TV (DVD) | 720 | 480 |
| "Full HD" | 1,920 | 1,080 |
| "4K" | 3,840 | 2,160 |

🔢 **Maths: counting pixels**

The number of pixels is width × height.

Full HD:
> width = 1,920
> height = 1,080
> pixels = 1,920 × 1,080
> Split it: 1,920 × 1,000 = 1,920,000
> and 1,920 × 80 = 153,600
> Add: 1,920,000 + 153,600 = 2,073,600

So a Full HD picture has **2,073,600 pixels** — about **2 million**.

4K:
> 3,840 × 2,160 = 8,294,400

That is about **8.3 million** pixels. Look: 3,840 is 2 × 1,920, and 2,160 is 2 × 1,080. Doubling **both** sides gives 2 × 2 = **4 times** as many pixels. (8,294,400 ÷ 2,073,600 = 4.)

🧠 **Remember:** Double the width **and** the height → four times the pixels → four times the work for our programs.

---

## 2.8 Aspect ratio

📖 **New word: aspect ratio** — the shape of an image: the width compared to the height.

We write it as `width : height`, made as small as possible.

🔢 **Maths: finding the aspect ratio of 1,920 × 1,080**

We look for a number that divides both. Let us divide both by 120:

> 1,920 ÷ 120 = 16
> 1,080 ÷ 120 = 9

So the aspect ratio is **16 : 9**. That is the shape of most screens today.

We can also write it as one number: 16 ÷ 9 ≈ **1.78**. That means the image is 1.78 times as wide as it is tall.

| Resolution | Aspect ratio | As one number |
|---|---|---|
| 1,920 × 1,080 | 16 : 9 | 1.78 |
| 1,024 × 768 | 4 : 3 | 1.33 |
| 500 × 500 | 1 : 1 | 1.00 (square) |
| 1,080 × 1,920 | 9 : 16 | 0.5625 (phone held tall) |

💡 **Tip:** Aspect ratio matters later. If we draw a circle on a 16 : 9 image but forget the aspect ratio, our circle becomes an oval. We use this in Chapter 60 (Mandelbrot) and Chapter 65 (camera).

---

## 2.9 A picture as a grid of numbers

Now let us make the big step. We forget colour for a moment and use only **grey**.

We say:
- `0` means **black** (no light).
- `9` means **white** (full light).
- Numbers in between are greys. `5` is a middle grey.

Then this grid of numbers:

```
0 0 0 0 0 0 0
0 9 9 0 9 9 0
0 9 9 0 9 9 0
0 0 0 0 0 0 0
0 9 0 0 0 9 0
0 0 9 9 9 0 0
0 0 0 0 0 0 0
```

…is a picture of a smiling face! Two square eyes, and a smile.

🧠 **Remember:** **An image is just a grid of numbers.** Each number says how bright one pixel is. That is the most important idea of Part 1.

In this chapter's code, we store a grid like this in C++ and **print** it in the terminal. We cannot make a real image file yet (that is Chapter 8). So we pretend: we print a dark-looking letter for small numbers and a bright-looking letter for big numbers.

We use this list of characters, from dark to bright:

```
index:      0   1   2   3   4   5   6   7   8   9
character: ' ' '.' ':' '-' '=' '+' '*' '#' '%' '@'
```

On a dark terminal, a space looks black and `@` looks bright, because it has the most "ink".

---

## Code

File: `ch02/number_picture.cpp`

```cpp
#include <iostream>
#include <string>

int main() {
    const int width = 7;
    const int height = 7;

    const int picture[height][width] = {
        {0, 0, 0, 0, 0, 0, 0},
        {0, 9, 9, 0, 9, 9, 0},
        {0, 9, 9, 0, 9, 9, 0},
        {0, 0, 0, 0, 0, 0, 0},
        {0, 9, 0, 0, 0, 9, 0},
        {0, 0, 9, 9, 9, 0, 0},
        {0, 0, 0, 0, 0, 0, 0},
    };

    const std::string shades = " .:-=+*#%@";

    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            int value = picture[y][x];
            char c = shades[value];
            std::cout << c << c;
        }
        std::cout << "\n";
    }
    return 0;
}
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1 | `#include <iostream>` | Lets us print with `std::cout`. |
| 2 | `#include <string>` | Lets us use `std::string` for the list of shade characters. |
| 4 | `int main() {` | The program starts here. |
| 5 | `const int width = 7;` | Our picture is 7 pixels across. |
| 6 | `const int height = 7;` | Our picture is 7 pixels down. |
| 8 | `const int picture[height][width] = {` | A grid of numbers: 7 rows, each with 7 numbers. The **first** index is the row (y), the **second** is the column (x). |
| 9–15 | `{0, 0, 0, ...},` | Each line is one **row** of the picture, from top to bottom. Each number is one pixel's brightness, from 0 (black) to 9 (white). |
| 16 | `};` | End of the grid. |
| 18 | `const std::string shades = " .:-=+*#%@";` | Ten characters, from darkest (space) to brightest (`@`). Character number 0 is the space; number 9 is `@`. |
| 20 | `for (int y = 0; y < height; ++y) {` | Go through the rows, **top to bottom**. `y` is the row number. Row 0 is the top. |
| 21 | `for (int x = 0; x < width; ++x) {` | Inside each row, go through the pixels **left to right**. `x` is the column number. |
| 22 | `int value = picture[y][x];` | Read the brightness of the pixel in row `y`, column `x`. Note the order: `[y]` first, then `[x]`. |
| 23 | `char c = shades[value];` | Turn the brightness (0–9) into a character. Brightness 9 → `shades[9]` → `'@'`. |
| 24 | `std::cout << c << c;` | Print the character **twice**. Why? Terminal characters are about twice as tall as they are wide. Two characters side by side look roughly **square**, like a pixel. |
| 25 | `}` | End of one row of pixels. |
| 26 | `std::cout << "\n";` | Go to a new line, so the next row prints underneath. |
| 27 | `}` | End of all rows. |
| 28 | `return 0;` | The program finished with no problem. |
| 29 | `}` | End of `main`. |

### What you should see

```

  @@@@  @@@@
  @@@@  @@@@

  @@      @@
    @@@@@@

```

(The empty lines are rows of `0`, which print as spaces.)

⚠️ **Careful:** Look at line 22 again. We write `picture[y][x]`, **not** `picture[x][y]`. The first index picks the **row**. This "y first" order will appear again and again in this book. Chapter 3 explains it fully.

---

## Small examples

### Example 1 — Change one pixel

Change row 5 (the 6th line) from `{0, 0, 9, 9, 9, 0, 0}` to `{0, 0, 9, 5, 9, 0, 0}`.
Now the middle of the smile prints `++` instead of `@@`. The smile has a "darker" spot. One number changed → one pixel changed.

### Example 2 — A grey gradient

Replace the picture with one row that goes from dark to bright:

```cpp
const int width = 10;
const int height = 1;
const int picture[height][width] = {
    {0, 1, 2, 3, 4, 5, 6, 7, 8, 9},
};
```

Output:

```
  ..::--==++**##%%@@
```

Each pixel is a little brighter than the one before. This is a **gradient**. Chapter 13 makes real gradients with real maths.

### Example 3 — Counting pixels in our picture

> width = 7, height = 7
> pixels = 7 × 7 = 49

How many are bright (9)? Count them: 4 in row 1, 4 in row 2, 2 in row 4, 3 in row 5.
> 4 + 4 + 2 + 3 = 13 bright pixels.
> 49 − 13 = 36 dark pixels.

### Example 4 — The aspect ratio of our terminal "pixel"

A terminal character is about **1 wide and 2 tall**. Its aspect ratio is 1 : 2, so it is tall and thin.
Two characters side by side: 2 wide and 2 tall → 2 : 2 = **1 : 1** → a square.
That is why we print each pixel as **two** characters.

---

## Common mistakes

⚠️ **Writing `picture[x][y]`.** This reads the grid the wrong way. Your face will be turned on its side (mirrored across the diagonal). Always use `[y][x]` with this kind of grid.

⚠️ **Using a number bigger than 9.** `shades` has only 10 characters (index 0 to 9). `shades[10]` reads past the end. That is a bug, and it may print rubbish or crash.

⚠️ **Thinking colour is "inside" an object.** Colour is what our **eyes and brain** make from the light that reaches them. This matters when we model light in Chapters 68 and 73.

⚠️ **Thinking more pixels is free.** Twice as wide and twice as tall is **four times** the pixels, so four times the work and four times the memory.

⚠️ **Mixing up resolution and aspect ratio.** 1,920 × 1,080 and 3,840 × 2,160 have **different** resolutions but the **same** aspect ratio (16 : 9).

---

## Practice

🏋️ **1.** Light with a wavelength of 650 nm — what colour do we see? And 450 nm?

🏋️ **2.** How many kinds of cone cells does a human eye have? Why does that mean images need **three** numbers per pixel?

🏋️ **3.** A screen pixel has its red and blue sub-pixels at full brightness, and its green sub-pixel off. What colour do you see? (Guess! Chapter 5 gives the full answer.)

🏋️ **4.** How many pixels does a 1,280 × 720 image have? Show every step.

🏋️ **5.** What is the aspect ratio of 1,280 × 720? (Hint: divide both by 80.)

🏋️ **6.** Change `number_picture.cpp` to draw a **plus sign** (+) on a 5 × 5 grid. Use 9 for the plus and 0 for the rest.

🏋️ **7.** Change the program so that **0 is bright and 9 is dark** (an "inverted" picture). You may only change **one line**.

🏋️ **8.** In Example 3 we counted 13 bright pixels. What **fraction** of all pixels is bright? Write it as a decimal.

---

## Answers

**1.** 650 nm looks **red**. 450 nm looks **blue**. (Look at the spectrum line in Section 2.2.)

**2.** **Three** kinds: S ("blue"), M ("green") and L ("red"). The brain gets only three numbers for each point. So if a screen makes the same three numbers, the brain sees the same colour. That is why each pixel stores three values: red, green and blue.

**3.** Red + blue light looks **magenta** (a pink-purple colour). Chapter 5 shows the full table of light mixes.

**4.**
> width = 1,280, height = 720
> pixels = 1,280 × 720
> 1,280 × 700 = 896,000
> 1,280 × 20 = 25,600
> 896,000 + 25,600 = 921,600

So **921,600 pixels** (just under 1 million).

**5.**
> 1,280 ÷ 80 = 16
> 720 ÷ 80 = 9

Aspect ratio **16 : 9** (the same shape as Full HD).

**6.**

```cpp
const int width = 5;
const int height = 5;
const int picture[height][width] = {
    {0, 0, 9, 0, 0},
    {0, 0, 9, 0, 0},
    {9, 9, 9, 9, 9},
    {0, 0, 9, 0, 0},
    {0, 0, 9, 0, 0},
};
```

The middle **column** (x = 2) is all 9s, and the middle **row** (y = 2) is all 9s. Together they make a plus.

**7.** Change line 23 to:

```cpp
char c = shades[9 - value];
```

When `value` is 0, `9 - 0 = 9` → `'@'` (bright). When `value` is 9, `9 - 9 = 0` → `' '` (dark). Everything is flipped. This is called **inverting**. We do it to real images in Chapter 47.

**8.**
> bright fraction = 13 ÷ 49
> 13 ÷ 49 ≈ 0.265

So about **0.27**, or 27%, of the pixels are bright.

---

## Summary

🧠 **Light** is a wave. Its **wavelength** decides its colour: short = blue, middle = green, long = red.

🧠 The eye has **three kinds of cone cells**. So three numbers — **red, green, blue** — are enough to describe a colour for people.

🧠 A screen pixel is made of **three sub-pixels**: red, green and blue. Our eye mixes them.

🧠 An image is a **grid of pixels**. Each pixel is one **sample** with one colour.

🧠 **Resolution** = width × height. Double both sides → four times the pixels.

🧠 **Aspect ratio** = the shape, like 16 : 9.

🧠 **An image is just a grid of numbers.** In C++ we read it as `[y][x]`: row first, then column.

---

## Next chapter

In Chapter 3 we look closely at **the grid itself**. Where is pixel (0, 0)? Which way does y go? How do we find a pixel's neighbours? We answer these with **coordinates**, and we write a program that prints a labelled grid.
