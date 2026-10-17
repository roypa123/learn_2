# Chapter 5 — How Colour Works: the RGB Model

> **Part 1 · Chapter 5 of 82**
> **You need:** Chapters 1–4 · **You will make:** a program that prints a colour table, with real colour squares in the terminal

---

## What you will learn

- Why **light** mixes differently from **paint**.
- Why red, green and blue are the **primary colours of light**.
- The 8 "corner" colours you get from 0 and 255 alone.
- How to make **in-between** colours, greys, lighter colours and darker colours.
- The **RGB cube**: a way to picture every colour as a point.
- How to find the **opposite** colour.
- How to change a colour value between **0–255** and **0.0–1.0**.
- How to show **real colours** in the terminal.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **additive mixing** | Mixing **light**. Each colour adds more light. Everything together makes white. |
| **subtractive mixing** | Mixing **paint or ink**. Each colour takes light away. Everything together makes dark brown or black. |
| **primary colours** | The few colours we mix to make all the others. |
| **channel** | One of the three parts of a colour: the red channel, green channel or blue channel. |
| **RGB** | Red, Green, Blue. A colour written as three numbers. |
| **grey** | A colour with no "colour": the red, green and blue values are equal. |
| **RGB cube** | A picture of all RGB colours as points inside a cube. |
| **complement** | The opposite colour. Added together with the first colour, it makes white. |
| **normalised value** | A value moved into the range 0.0 to 1.0. |
| **escape code** | Special characters that tell the terminal to do something, like change colour. |

---

## 5.1 Mixing light vs mixing paint

At school you may have learned: "red + yellow + blue are the primary colours, and mixing all paints gives brown."

That is true **for paint**. But a screen does not use paint. A screen makes **light**. And light mixes in a **different way**.

📖 **New word: additive mixing** — mixing light. Each new colour **adds more light**. All colours together make **white**.

📖 **New word: subtractive mixing** — mixing paint or ink. Each paint **soaks up** (takes away) some light. All paints together make **dark brown or black**.

```
  LIGHT (screens)                  PAINT (paper)
  start: black (no light)          start: white paper (all light comes back)
  add red light   → red            add yellow paint → yellow
  add green light → yellow!        add blue paint   → green
  add blue light  → white!         add red paint    → dark brown
```

🧠 **Remember:** In this book we work with **light**. Red light + green light = **yellow** light. Red + green + blue light = **white**.

### Why does red + green light look yellow?

Remember Chapter 2: your eye has three kinds of cones. Real yellow light (about 580 nm) excites the "red" cone and the "green" cone, but not the "blue" cone.

Red light excites the red cone. Green light excites the green cone. Shine **both** together, and the red and green cones are excited, the blue one is not. **The same three numbers reach the brain.** So the brain says "yellow".

---

## 5.2 The primary colours of light

📖 **New word: primary colours** — the few colours we mix to make all others.

For light, the primaries are **red, green and blue**. They match the three cones in the eye (Chapter 2). By changing how bright each one is, we can make almost every colour a person can see.

📖 **New word: channel** — one of the three parts of a colour. A colour has a **red channel**, a **green channel** and a **blue channel**.

📖 **New word: RGB** — red, green, blue. We write a colour as three numbers in this order: **(R, G, B)**.

From Chapter 4, each channel is one byte: **0 to 255**.

- **0** means that light is **off**.
- **255** means that light is **fully on**.

So `(255, 0, 0)` means "red fully on, green off, blue off". That is **pure red**.

---

## 5.3 The eight corner colours

If every channel can only be 0 or 255, there are 2 × 2 × 2 = **8** colours. Learn these well. They are the "corners" of all colours.

| R | G | B | Colour | Why |
|---|---|---|---|---|
| 0 | 0 | 0 | **black** | no light at all |
| 255 | 0 | 0 | **red** | only red |
| 0 | 255 | 0 | **green** | only green |
| 0 | 0 | 255 | **blue** | only blue |
| 255 | 255 | 0 | **yellow** | red + green |
| 0 | 255 | 255 | **cyan** | green + blue (a light sky blue) |
| 255 | 0 | 255 | **magenta** | red + blue (a pink-purple) |
| 255 | 255 | 255 | **white** | all three |

```
          red
         /   \
   yellow     magenta
     /    white    \
 green ───────────── blue
       \   cyan   /
```

Each **secondary** colour (yellow, cyan, magenta) is made of **two** primaries. It sits between them in the picture.

💡 **Tip:** A trick to remember: each secondary colour is "white **minus** one primary".
- yellow = white − blue
- cyan = white − red
- magenta = white − green

---

## 5.4 Colours in between

The channels can be **any** value from 0 to 255, not only 0 or 255. This gives us all the other colours.

| (R, G, B) | What you see | Why |
|---|---|---|
| (128, 0, 0) | dark red | red at about half power |
| (255, 128, 0) | orange | full red, some green (between red and yellow) |
| (128, 0, 128) | purple | half red, half blue |
| (255, 192, 203) | pink | full red, lots of green and blue (red mixed with white) |
| (139, 69, 19) | brown | a dark orange |
| (0, 128, 0) | dark green | green at about half power |

🔢 **Maths: why is orange "between" red and yellow?**

> red    = (255,   0, 0)
> yellow = (255, 255, 0)
> Only green is different: 0 in red, 255 in yellow.
> Halfway: green = (0 + 255) ÷ 2 = 127.5 → about 128.
> So halfway between red and yellow is (255, 128, 0) = **orange**.

This "halfway" idea is the start of **interpolation**. Chapter 13 makes it exact: we can find the colour 10% of the way, or 73% of the way, between any two colours.

---

## 5.5 Greys

📖 **New word: grey** — a colour where **red, green and blue are equal**.

When all three channels are the same, no colour "wins". You see only brightness.

| (R, G, B) | Colour |
|---|---|
| (0, 0, 0) | black |
| (64, 64, 64) | dark grey |
| (128, 128, 128) | middle grey |
| (192, 192, 192) | light grey (often called "silver") |
| (255, 255, 255) | white |

So there are **256 greys**, from black to white.

🧠 **Remember:** R = G = B means **grey**. The bigger the number, the lighter the grey.

⚠️ **Careful:** (128, 128, 128) **looks** like a middle grey to us. But it gives out only about **22%** of the light of white, not 50%! Our eyes and screens are not "straight-line". Chapter 17 (gamma) explains this.

---

## 5.6 The RGB cube

📖 **New word: RGB cube** — a picture where each colour is a **point** inside a cube.

Use the three channels as three directions, like the x and y of Chapter 3, plus one more. In the drawing below:

- blue grows to the **right** (0 on the left side, 255 on the right side)
- green grows **upward** (0 at the bottom, 255 at the top)
- red grows **toward you** (the front face has red = 255, the back face has red = 0)

```
              green (0,255,0) ●───────────● cyan (0,255,255)
                             /│          /│
                            / │         / │
          yellow (255,255,0)●───────────● white (255,255,255)
                           │  │        │  │
                           │  ● black  │  ● blue (0,0,255)
                           │ / (0,0,0) │ /
                           │/          │/
              red (255,0,0)●───────────● magenta (255,0,255)
```

- The 8 corners are the 8 colours from Section 5.3.
- **Black** and **white** are opposite corners.
- The straight line from black to white goes through the middle of the cube. Every point on it has R = G = B. That line is **all the greys**.

Why is this picture useful? Because now **a colour is a point**, and we can use **geometry** on colours:

- The **distance** between two colours (Chapter 3's Pythagoras, in 3 directions) tells how different they are. We use this in Chapter 52 (dithering).
- Moving along a **straight line** between two points makes a smooth gradient (Chapter 13).
- Adding and scaling colours is like adding and scaling arrows (Chapter 14).

🔢 **Maths: how different are red and orange?**

> red = (255, 0, 0), orange = (255, 128, 0)
> dR = 0, dG = 128, dB = 0
> distance = √(0² + 128² + 0²) = √16,384 = 128

> red and blue: (255, 0, 0) and (0, 0, 255)
> dR = 255, dG = 0, dB = 255
> distance = √(255² + 255²) = √(65,025 + 65,025) = √130,050 ≈ 360.6

So red is much "closer" to orange (128) than to blue (about 361). That matches what our eyes say.

---

## 5.7 Lighter and darker

### Darker: move toward black

To make a colour darker, make **every channel smaller by the same fraction**.

🔢 **Maths: orange at half brightness**

> orange = (255, 128, 0)
> multiply each channel by 0.5:
> R = 255 × 0.5 = 127.5 → 128
> G = 128 × 0.5 = 64
> B = 0 × 0.5 = 0
> darker orange = (128, 64, 0) — a brown

Multiplying by **0** gives black. Multiplying by **1** leaves the colour as it is.

### Lighter: move toward white

To make a colour lighter, move each channel **part of the way toward 255**.

🔢 **Maths: orange, half way to white**

> For each channel: new = old + (255 − old) × 0.5
> R = 255 + (255 − 255) × 0.5 = 255 + 0 = 255
> G = 128 + (255 − 128) × 0.5 = 128 + 63.5 = 191.5 → 192
> B = 0 + (255 − 0) × 0.5 = 0 + 127.5 = 127.5 → 128
> lighter orange = (255, 192, 128) — a soft peach colour

⚠️ **Careful:** Do **not** just add a number to each channel. Orange + 100 would give (355, 228, 100). 355 does not fit in a byte, and it **wraps around** (Chapter 4) to 99! Always keep the result between 0 and 255. Chapter 14 shows the safe way (clamping).

---

## 5.8 Opposite colours

📖 **New word: complement** — the opposite colour. A colour plus its complement makes white.

🔢 **Maths: the complement of a colour**

> complement = (255 − R, 255 − G, 255 − B)

| Colour | Complement |
|---|---|
| red (255, 0, 0) | (0, 255, 255) = cyan |
| green (0, 255, 0) | (255, 0, 255) = magenta |
| blue (0, 0, 255) | (255, 255, 0) = yellow |
| black (0, 0, 0) | (255, 255, 255) = white |
| orange (255, 128, 0) | (0, 127, 255) = a bright sky blue |

Check: orange + its complement = (255 + 0, 128 + 127, 0 + 255) = (255, 255, 255) = white ✓.

Doing this to **every pixel** gives a "photo negative" image. Chapter 47 does this. In Chapter 2's practice you already did it to grey numbers: `9 − value`.

---

## 5.9 Colours as 0.0 to 1.0

📖 **New word: normalised value** — a value moved into the range **0.0 to 1.0**.

Bytes (0–255) are good for **storing** colours in files. But for **maths**, 0.0 to 1.0 is much easier:

- 0.5 clearly means "half".
- Multiplying two colours stays in range: 0.5 × 0.5 = 0.25. With bytes, 128 × 128 = 16,384 — far too big.
- Light calculations in Parts 9 and 10 use 0.0–1.0.

🔢 **Maths: byte → normalised**

> normalised = byte ÷ 255

> 0 ÷ 255 = 0.0
> 255 ÷ 255 = 1.0
> 128 ÷ 255 ≈ 0.502
> 51 ÷ 255 = 0.2

🔢 **Maths: normalised → byte**

> byte = normalised × 255, then **round** to the nearest whole number

> 0.2 × 255 = 51.0 → 51
> 0.502 × 255 = 128.01 → 128
> 0.5 × 255 = 127.5 → 128 (we round .5 up)

To **round** in C++ without extra functions, we add 0.5 and then cut off the decimals:

> 127.5 + 0.5 = 128.0 → cut → 128
> 51.3 + 0.5 = 51.8 → cut → 51
> 51.6 + 0.5 = 52.1 → cut → 52

`static_cast<int>(x)` "cuts off" the decimals. So `static_cast<int>(x + 0.5)` rounds a positive number to the nearest whole number. Chapter 13 explains rounding in more detail, including negative numbers.

⚠️ **Careful:** In C++, `128 / 255` is **0**, because both are `int` and integer division drops the decimals. Write `128 / 255.0` (with `.0`) to get 0.50196…

🧠 **Remember:** Store as bytes (0–255). Do maths as `double` (0.0–1.0). Convert with `÷ 255.0` and `× 255 + 0.5`.

---

## 5.10 Real colour in the terminal

We still cannot write an image file (that is Chapter 8). But most modern terminals can show colours.

📖 **New word: escape code** — special characters that tell the terminal to do something, instead of printing.

This text sets the **background colour** of the next characters to (R, G, B):

```
ESC [ 48 ; 2 ; R ; G ; B m
```

- `ESC` is a special character with the value 27. In C++ we write it as `"\x1b"` (27 in hex is `1B`).
- `48` means "background colour". (`38` would mean "text colour".)
- `2` means "the next three numbers are R, G, B".
- `m` ends the code.

And this text puts everything back to normal:

```
ESC [ 0 m
```

So, to show a red square:

```cpp
std::cout << "\x1b[48;2;255;0;0m      \x1b[0m";
```

The 6 spaces get a red background. We see a red bar.

⚠️ **Careful:** This works in **Windows Terminal**, the **VS Code terminal**, and almost all macOS and Linux terminals. The very old Windows "Command Prompt" window may print strange characters like `←[48;2;255;0;0m` instead. If that happens, open the program in Windows Terminal or VS Code. The colour **numbers** in the output are still correct.

💡 **Tip:** This is **not** a library. It is just text that our program prints. The terminal program chooses to show it as colour.

---

## Code

File: `ch05/colours.cpp`

```cpp
#include <iostream>
#include <cstdint>
#include <string>

struct Colour {
    std::uint8_t r;
    std::uint8_t g;
    std::uint8_t b;
};

std::string toHex(std::uint8_t value) {
    const std::string digits = "0123456789ABCDEF";
    std::string result;
    result += digits[value >> 4];
    result += digits[value & 0x0F];
    return result;
}

void printSwatch(Colour c) {
    std::cout << "\x1b[48;2;" << static_cast<int>(c.r) << ';'
              << static_cast<int>(c.g) << ';'
              << static_cast<int>(c.b) << "m      \x1b[0m";
}

void printColour(const std::string& name, Colour c) {
    printSwatch(c);
    std::cout << "  " << name;
    for (int i = static_cast<int>(name.size()); i < 9; ++i) {
        std::cout << ' ';
    }
    std::cout << " #" << toHex(c.r) << toHex(c.g) << toHex(c.b)
              << "  (" << static_cast<int>(c.r) << ", "
              << static_cast<int>(c.g) << ", "
              << static_cast<int>(c.b) << ")\n";
}

int main() {
    printColour("black",   {0, 0, 0});
    printColour("red",     {255, 0, 0});
    printColour("green",   {0, 255, 0});
    printColour("blue",    {0, 0, 255});
    printColour("yellow",  {255, 255, 0});
    printColour("cyan",    {0, 255, 255});
    printColour("magenta", {255, 0, 255});
    printColour("white",   {255, 255, 255});
    printColour("grey",    {128, 128, 128});
    printColour("orange",  {255, 128, 0});

    Colour orange = {255, 128, 0};
    Colour opposite = {
        static_cast<std::uint8_t>(255 - orange.r),
        static_cast<std::uint8_t>(255 - orange.g),
        static_cast<std::uint8_t>(255 - orange.b)
    };
    std::cout << "\nopposite of orange:\n";
    printColour("opposite", opposite);

    double g = orange.g / 255.0;
    int back = static_cast<int>(g * 255.0 + 0.5);
    std::cout << "\ngreen of orange as 0..1: " << g << "\n";
    std::cout << "and back to 0..255:      " << back << "\n";
    return 0;
}
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–3 | `#include <iostream>` / `<cstdint>` / `<string>` | Printing, exact byte types, and text. Same as Chapter 4. |
| 5 | `struct Colour {` | A small type that holds **one colour**. We will use a type like this for the rest of the book. |
| 6 | `std::uint8_t r;` | The red channel, 0–255. |
| 7 | `std::uint8_t g;` | The green channel, 0–255. |
| 8 | `std::uint8_t b;` | The blue channel, 0–255. The order is always **r, g, b**. |
| 9 | `};` | End of the type. One `Colour` uses exactly 3 bytes of data. |
| 11–17 | `std::string toHex(std::uint8_t value) { ... }` | The same function as Chapter 4: one byte → two hex digits. Line 14 takes the left 4 bits (`>> 4`), line 15 takes the right 4 bits (`& 0x0F`). |
| 19 | `void printSwatch(Colour c) {` | A function that prints a small bar in colour `c`. "Swatch" means a small sample of a colour. |
| 20 | `std::cout << "\x1b[48;2;" << static_cast<int>(c.r) << ';'` | Start the escape code: ESC, `[48;2;`, then the red number. We cast to `int`, or the byte prints as a letter (Chapter 4). |
| 21 | `<< static_cast<int>(c.g) << ';'` | Then the green number and a `;`. |
| 22 | `<< static_cast<int>(c.b) << "m      \x1b[0m";` | Then the blue number and `m` to end the code. Then 6 spaces, which appear in the colour. Then `ESC[0m` to switch colours back to normal. |
| 23 | `}` | End of `printSwatch`. |
| 25 | `void printColour(const std::string& name, Colour c) {` | Prints one full line: swatch, name, hex code and numbers. |
| 26 | `printSwatch(c);` | First, the colour bar. |
| 27 | `std::cout << "  " << name;` | Two spaces, then the colour's name. |
| 28 | `for (int i = static_cast<int>(name.size()); i < 9; ++i) {` | Add spaces until the name part is 9 characters long. This lines up the hex codes in a neat column. "black" has 5 letters, so we add 4 spaces. |
| 29 | `std::cout << ' ';` | One space. |
| 30 | `}` | End of the padding loop. |
| 31 | `std::cout << " #" << toHex(c.r) << toHex(c.g) << toHex(c.b)` | Print the colour code: `#` and three bytes in hex, red first. |
| 32 | `<< "  (" << static_cast<int>(c.r) << ", "` | Then the numbers in brackets, starting with red. |
| 33 | `<< static_cast<int>(c.g) << ", "` | Green. |
| 34 | `<< static_cast<int>(c.b) << ")\n";` | Blue, a closing bracket, and a new line. |
| 35 | `}` | End of `printColour`. |
| 37 | `int main() {` | The program starts here. |
| 38–47 | `printColour("black", {0, 0, 0});` … | Print the 8 corner colours (Section 5.3), plus grey and orange. `{0, 0, 0}` makes a `Colour` right there, with r, g, b in that order. |
| 49 | `Colour orange = {255, 128, 0};` | Store orange in a variable, so we can use it again. |
| 50 | `Colour opposite = {` | Start making the complement (Section 5.8). |
| 51 | `static_cast<std::uint8_t>(255 - orange.r),` | Red: 255 − 255 = 0. The maths happens in `int`; the cast stores it back into one byte. It always fits, because 255 − (0 to 255) is always 0 to 255. |
| 52 | `static_cast<std::uint8_t>(255 - orange.g),` | Green: 255 − 128 = 127. |
| 53 | `static_cast<std::uint8_t>(255 - orange.b)` | Blue: 255 − 0 = 255. |
| 54 | `};` | End of the complement. It is (0, 127, 255). |
| 55 | `std::cout << "\nopposite of orange:\n";` | A heading. |
| 56 | `printColour("opposite", opposite);` | Show the complement. |
| 58 | `double g = orange.g / 255.0;` | Change green (128) into the range 0.0–1.0. The `.0` makes it a `double` division (Section 5.9). |
| 59 | `int back = static_cast<int>(g * 255.0 + 0.5);` | Change it back to 0–255, with rounding: × 255, + 0.5, then cut off the decimals. |
| 60 | `std::cout << "\ngreen of orange as 0..1: " << g << "\n";` | Print the normalised value. `std::cout` shows about 6 digits. |
| 61 | `std::cout << "and back to 0..255:      " << back << "\n";` | Print the byte again. It should be 128, the same as we started with. |
| 62 | `return 0;` | The program finished with no problem. |
| 63 | `}` | End of `main`. |

### What you should see

In a colour terminal, each line starts with a coloured bar. Here the bar is shown as `[██████]`:

```
[██████]  black     #000000  (0, 0, 0)
[██████]  red       #FF0000  (255, 0, 0)
[██████]  green     #00FF00  (0, 255, 0)
[██████]  blue      #0000FF  (0, 0, 255)
[██████]  yellow    #FFFF00  (255, 255, 0)
[██████]  cyan      #00FFFF  (0, 255, 255)
[██████]  magenta   #FF00FF  (255, 0, 255)
[██████]  white     #FFFFFF  (255, 255, 255)
[██████]  grey      #808080  (128, 128, 128)
[██████]  orange    #FF8000  (255, 128, 0)

opposite of orange:
[██████]  opposite  #007FFF  (0, 127, 255)

green of orange as 0..1: 0.501961
and back to 0..255:      128
```

💡 **Tip:** The black bar may be hard to see on a black terminal. That is correct!

---

## Small examples

### Example 1 — Make your own colour

Add this line to `main`:

```cpp
printColour("pink", {255, 192, 203});
```

You see a soft pink: lots of red, and quite a lot of green and blue too. Pink is "red mixed with white".

### Example 2 — A row of greys

```cpp
for (int v = 0; v <= 255; v += 51) {
    std::uint8_t b = static_cast<std::uint8_t>(v);
    printSwatch({b, b, b});
}
std::cout << "\n";
```

`v` takes the values 0, 51, 102, 153, 204, 255. That is 6 greys, from black to white, each 51 apart (255 ÷ 5 = 51). They print in one row, because `printSwatch` does not print a new line.

### Example 3 — Darker by half

```cpp
Colour darker = {
    static_cast<std::uint8_t>(orange.r * 0.5 + 0.5),
    static_cast<std::uint8_t>(orange.g * 0.5 + 0.5),
    static_cast<std::uint8_t>(orange.b * 0.5 + 0.5)
};
printColour("dark org", darker);
```

> R: 255 × 0.5 + 0.5 = 128.0 → 128
> G: 128 × 0.5 + 0.5 = 64.5 → 64
> B: 0 × 0.5 + 0.5 = 0.5 → 0

Result: (128, 64, 0), a brown. This matches Section 5.7.

### Example 4 — Read a colour from its hex code

What is `#00CED1`?
> R = 0x00 = 0
> G = 0xCE = 12 × 16 + 14 = 206
> B = 0xD1 = 13 × 16 + 1 = 209

Mostly green and blue, equal-ish, no red → a **cyan-like** colour (it is called "dark turquoise").

---

## Common mistakes

⚠️ **Thinking of paint.** On a screen, red + green = **yellow**, and red + green + blue = **white**. Paint rules do not apply.

⚠️ **Writing the channels in the wrong order.** It is always **R, G, B**. `{0, 0, 255}` is blue, not red. (BMP files store B, G, R — we will be very careful in Chapter 36.)

⚠️ **Adding to make a colour lighter.** It can go past 255 and wrap around. Move toward 255 by a fraction instead (Section 5.7).

⚠️ **Integer division.** `128 / 255` is `0`. Use `128 / 255.0`.

⚠️ **Rounding by cutting.** `static_cast<int>(127.9)` is 127, not 128. Add 0.5 first.

⚠️ **Printing the byte without a cast.** `std::cout << c.r` prints a character, not a number.

---

## Practice

🏋️ **1.** What colour is (0, 0, 128)? What colour is (255, 255, 128)?

🏋️ **2.** Write the (R, G, B) of a grey that is exactly in the middle between dark grey (64, 64, 64) and white.

🏋️ **3.** What is the complement of (200, 50, 100)? Check that the two add up to white.

🏋️ **4.** Make cyan (0, 255, 255) **25% darker** (multiply by 0.75). Show every step, with rounding.

🏋️ **5.** Make blue (0, 0, 255) **25% of the way** toward white. Show every step.

🏋️ **6.** Change the byte 77 into a normalised value (3 decimal places). Then change 0.3 into a byte.

🏋️ **7.** In the RGB cube, what is the distance between black (0, 0, 0) and white (255, 255, 255)? (Hint: Pythagoras with three differences: √(dR² + dG² + dB²).)

🏋️ **8.** Change `colours.cpp` so it also prints the complement of **every** colour in the list, right next to it. (Hint: change `printColour` to call `printSwatch` a second time.)

---

## Answers

**1.**
- (0, 0, 128): only blue, at about half → **dark blue** (often called "navy").
- (255, 255, 128): full red and green (yellow) plus some blue → **light yellow**.

**2.**
> middle of 64 and 255 = (64 + 255) ÷ 2 = 319 ÷ 2 = 159.5 → 160
> So **(160, 160, 160)**. All three channels are equal, so it is still grey.

**3.**
> complement = (255 − 200, 255 − 50, 255 − 100) = **(55, 205, 155)**
> add: (200 + 55, 50 + 205, 100 + 155) = (255, 255, 255) ✓ white

**4.**
> R = 0 × 0.75 = 0 → 0
> G = 255 × 0.75 = 191.25 → +0.5 = 191.75 → cut → 191
> B = 255 × 0.75 = 191.25 → 191
> darker cyan = **(0, 191, 191)**

**5.** Rule: new = old + (255 − old) × 0.25
> R = 0 + (255 − 0) × 0.25 = 63.75 → 64
> G = 0 + 255 × 0.25 = 63.75 → 64
> B = 255 + (255 − 255) × 0.25 = 255 + 0 = 255
> lighter blue = **(64, 64, 255)**

**6.**
> 77 ÷ 255 = 0.30196… ≈ **0.302**
> 0.3 × 255 = 76.5 → + 0.5 = 77.0 → **77**

Notice: 77 → 0.302 → 77. The trip there and back gives the same byte.

**7.**
> dR = dG = dB = 255
> dR² = 255 × 255 = 65,025
> sum = 65,025 × 3 = 195,075
> √195,075 ≈ **441.7**

This is the **biggest** distance between any two colours: two opposite corners of the cube.

**8.** One way is to change `printColour` like this:

```cpp
void printColour(const std::string& name, Colour c) {
    printSwatch(c);
    Colour opp = {
        static_cast<std::uint8_t>(255 - c.r),
        static_cast<std::uint8_t>(255 - c.g),
        static_cast<std::uint8_t>(255 - c.b)
    };
    printSwatch(opp);
    std::cout << "  " << name;
    // ... the rest stays the same
}
```

Now each line shows two bars: the colour and its opposite. Red sits next to cyan, blue next to yellow, black next to white.

---

## Summary

🧠 Screens mix **light** (additive). Red + green = **yellow**. All three = **white**.

🧠 A colour is **(R, G, B)**, each channel 0–255. Always in that order.

🧠 The 8 corners: black, red, green, blue, yellow, cyan, magenta, white.

🧠 **R = G = B** is a grey.

🧠 Colours are **points in the RGB cube**. Distance between colours = √(dR² + dG² + dB²).

🧠 Darker: multiply every channel by a number below 1. Lighter: move each channel part of the way to 255.

🧠 Complement: **(255 − R, 255 − G, 255 − B)**.

🧠 Normalised = byte ÷ 255.0. Byte = normalised × 255 + 0.5, then cut.

---

## Next chapter

We know what **one** pixel is. In Chapter 6 we store a **whole image** in memory: thousands of pixels, one after another, in a `std::vector`. We find out exactly **where** each pixel's three bytes live, with the most important formula in this book: **index = y × width + x**.
