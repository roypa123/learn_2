# Chapter 4 — Bits, Bytes and Hexadecimal

> **Part 1 · Chapter 4 of 82**
> **You need:** Chapters 1–3 · **You will make:** a program that prints numbers as binary and hex, and splits a colour into bytes

---

## What you will learn

- What a **bit** and a **byte** are.
- How to count in **binary** (base 2), and change binary to normal numbers and back.
- Why one colour value goes from **0 to 255**.
- How to read and write **hexadecimal** (base 16), like `FF` and `#FF8000`.
- Which C++ types hold exactly one, two or four bytes: `std::uint8_t`, `std::uint16_t`, `std::uint32_t`.
- How to **split** a big number into bytes and **join** bytes back, with `>>`, `<<`, `&` and `|`.
- What happens when a byte gets **too big** (wrap-around).

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **bit** | The smallest piece of data: a 0 or a 1. |
| **binary** | Writing numbers with only the digits 0 and 1 (base 2). |
| **decimal** | Our normal way of writing numbers, with digits 0–9 (base 10). |
| **base** | How many different digits a number system uses. |
| **place value** | How much a digit is worth because of where it stands. |
| **byte** | 8 bits together. It holds a number from 0 to 255. |
| **hexadecimal (hex)** | Writing numbers with 16 digits: 0–9 and A–F (base 16). |
| **unsigned** | A type that holds only zero and positive numbers. |
| **bit shift** | Moving all the bits left or right. |
| **mask** | A pattern of bits used to keep some bits and clear others. |
| **wrap-around** | When a number gets too big for its type and starts again from 0. |

---

## 4.1 A bit: one switch

📖 **New word: bit** — the smallest piece of data. It is either **0** or **1**.

Think of a light switch. It is **off** (0) or **on** (1). Nothing in between.

Inside the computer, memory is billions of tiny switches. Each one is a bit.

One bit can say only two things:

| Bit | Could mean |
|---|---|
| 0 | off, no, black |
| 1 | on, yes, white |

A black-and-white image could use **one bit per pixel**: 0 for black, 1 for white. We make exactly this kind of image in Chapter 10 (the PBM format).

But one bit is not enough for grey, or for colour. We need more bits.

---

## 4.2 Many bits: counting in binary

With **two** bits, we get more patterns:

| Bits | Pattern number |
|---|---|
| 00 | 0 |
| 01 | 1 |
| 10 | 2 |
| 11 | 3 |

Two bits → **4** patterns. Three bits → **8** patterns. Each extra bit **doubles** the number of patterns.

🔢 **Maths: how many patterns?**

> 1 bit → 2 patterns
> 2 bits → 2 × 2 = 4
> 3 bits → 2 × 2 × 2 = 8
> 4 bits → 16
> 8 bits → 2 × 2 × 2 × 2 × 2 × 2 × 2 × 2 = 256

We write "2 multiplied by itself 8 times" as **2⁸**. So **2⁸ = 256**.

### Place value

📖 **New word: decimal** — our normal numbers, with ten digits: 0 1 2 3 4 5 6 7 8 9.

📖 **New word: place value** — how much a digit is worth because of where it stands.

In decimal, the number **352** means:

```
  3        5       2
  │        │       │
 ×100     ×10     ×1
  │        │       │
 300   +   50  +   2   = 352
```

Each place is worth **10 times** the place to its right: 1, 10, 100, 1000…

📖 **New word: binary** — writing numbers with only two digits, 0 and 1.

📖 **New word: base** — how many different digits a number system uses. Decimal is base 10. Binary is base 2.

In binary, each place is worth **2 times** the place to its right:

```
place value:  128   64   32   16    8    4    2    1
```

### Binary to decimal

🔢 **Maths: what is binary `00001101` in decimal?**

Write the place values above the bits. Add the place values where the bit is 1.

```
place value:  128  64  32  16   8   4   2   1
bit:            0   0   0   0   1   1   0   1
                                ↓   ↓       ↓
                                8 + 4   +   1  = 13
```

So binary `00001101` = decimal **13**.

### Decimal to binary

🔢 **Maths: what is decimal 200 in binary?**

Go from the **biggest** place value to the smallest. At each one, ask: "does it fit in what is left?"

| Place | Does it fit in what is left? | Bit | Left over |
|---|---|---|---|
| 128 | 128 ≤ 200? yes | 1 | 200 − 128 = 72 |
| 64 | 64 ≤ 72? yes | 1 | 72 − 64 = 8 |
| 32 | 32 ≤ 8? no | 0 | 8 |
| 16 | 16 ≤ 8? no | 0 | 8 |
| 8 | 8 ≤ 8? yes | 1 | 8 − 8 = 0 |
| 4 | no | 0 | 0 |
| 2 | no | 0 | 0 |
| 1 | no | 0 | 0 |

Read the bits from top to bottom: **`11001000`**.

Check: 128 + 64 + 8 = 200 ✓.

---

## 4.3 A byte: 8 bits, 0 to 255

📖 **New word: byte** — 8 bits together.

A byte is the **basic unit** of computer memory. Files are made of bytes. Memory is counted in bytes.

🔢 **Maths: the smallest and biggest byte**

> smallest: `00000000` = 0
> biggest:  `11111111` = 128 + 64 + 32 + 16 + 8 + 4 + 2 + 1 = 255

So one byte holds a number from **0 to 255**. That is **256** different values (0 counts too).

### Why colour values go from 0 to 255

In Chapter 2 we said each pixel needs a red, a green and a blue value. Most images store **each of these in one byte**.

| Value | Meaning |
|---|---|
| 0 | none of this colour (that light is off) |
| 128 | about half (but see Chapter 17 — it is not really "half bright"!) |
| 255 | full (that light is fully on) |

256 levels of each colour is enough that our eyes cannot see the steps between them in most pictures.

🔢 **Maths: how many colours can one RGB pixel show?**

> 256 reds × 256 greens × 256 blues
> 256 × 256 = 65,536
> 65,536 × 256 = 16,777,216

That is about **16.7 million colours**. People often call this "24-bit colour", because 3 bytes × 8 bits = 24 bits.

🧠 **Remember:** One byte = 8 bits = a number from **0 to 255**. One RGB pixel usually uses **3 bytes**.

---

## 4.4 Hexadecimal: a short way to write bytes

Binary is long. `11001000` is hard to read. Decimal does not line up nicely with bytes. So programmers use a third way.

📖 **New word: hexadecimal** (short: **hex**) — writing numbers with **16** digits.

The 16 digits are:

```
hex digit:   0 1 2 3 4 5 6 7 8 9 A  B  C  D  E  F
its value:   0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
```

After 9, we use **letters**: A means 10, B means 11, up to F which means 15.

### The magic: one hex digit = 4 bits

4 bits give 2⁴ = 16 patterns. One hex digit has 16 values. They match **exactly**.

| 4 bits | hex | | 4 bits | hex |
|---|---|---|---|---|
| 0000 | 0 | | 1000 | 8 |
| 0001 | 1 | | 1001 | 9 |
| 0010 | 2 | | 1010 | A |
| 0011 | 3 | | 1011 | B |
| 0100 | 4 | | 1100 | C |
| 0101 | 5 | | 1101 | D |
| 0110 | 6 | | 1110 | E |
| 0111 | 7 | | 1111 | F |

So one byte (8 bits) is **always exactly 2 hex digits**.

🔢 **Maths: 200 in hex**

> 200 in binary is `1100 1000` (from Section 4.2).
> Split it into two halves of 4 bits: `1100` and `1000`.
> `1100` = C, `1000` = 8.
> So 200 = **C8** in hex.

### Hex to decimal

In hex, each place is worth **16 times** the place to its right: 1, 16, 256…

🔢 **Maths: what is hex `C8` in decimal?**

> C8 = (C × 16) + (8 × 1)
> C = 12
> = (12 × 16) + 8
> = 192 + 8
> = **200** ✓

🔢 **Maths: what is hex `FF`?**

> FF = (15 × 16) + 15 = 240 + 15 = **255** — the biggest byte.

### Writing hex in C++

In C++ we write `0x` in front of a hex number:

```cpp
int a = 0xFF;   // 255
int b = 0xC8;   // 200
int c = 0x10;   // 16
```

### Colour codes

You may have seen colours written like **`#FF8000`** in web pages or paint programs. That is **3 bytes in hex**, one after another:

```
#  FF   80   00
   │    │    │
  red green blue
  255  128    0     → orange
```

🧠 **Remember:** **2 hex digits = 1 byte.** `0x00` = 0, `0xFF` = 255. A colour code `#RRGGBB` is three bytes: red, green, blue.

---

## 4.5 C++ types with an exact size

You know `int`, `char` and `unsigned`. But their sizes are **not fixed** by the C++ rules. An `int` is often 4 bytes, but not always.

Image files need **exact** sizes. A BMP file says "these 4 bytes are the width". If we write 8 bytes by mistake, the file is broken.

So we use the types from `<cstdint>`:

📖 **New word: unsigned** — a type that holds only zero and positive numbers. No minus sign. That is what we want for colour bytes.

| Type | Bytes | Bits | Smallest | Biggest |
|---|---|---|---|---|
| `std::uint8_t` | 1 | 8 | 0 | 255 |
| `std::uint16_t` | 2 | 16 | 0 | 65,535 |
| `std::uint32_t` | 4 | 32 | 0 | 4,294,967,295 |
| `std::int32_t` | 4 | 32 | −2,147,483,648 | 2,147,483,647 |

The `u` means **unsigned**. The number is the count of **bits**. `_t` just means "type".

We use:
- `std::uint8_t` for **one colour value** (red, green or blue).
- `std::uint16_t` and `std::uint32_t` for **sizes and numbers inside file headers** (Part 6).

⚠️ **Careful — the most common byte bug.** `std::uint8_t` is really a kind of `char` on almost every compiler. So `std::cout` prints it as a **letter**, not a number!

```cpp
std::uint8_t v = 65;
std::cout << v;                    // prints: A    (65 is the code for 'A')
std::cout << static_cast<int>(v);  // prints: 65
```

Always **cast to `int`** before you print a byte as a number. Our code does this.

---

## 4.6 Bigger numbers from several bytes

A width of 1,920 does not fit in one byte (the biggest is 255). So files store big numbers in **two or four bytes**.

🔢 **Maths: two bytes make one number from 0 to 65,535**

With two bytes, one is the **high** byte (worth more) and one is the **low** byte.

> value = high × 256 + low

Why 256? Because the low byte counts 0 to 255. After 255, the high byte goes up by one, exactly like 99 → 100 in decimal.

Example: 1,920 as two bytes:

> 1,920 ÷ 256 = 7, with 1,920 − 7 × 256 = 1,920 − 1,792 = 128 left over.
> high = 7, low = 128
> check: 7 × 256 + 128 = 1,792 + 128 = 1,920 ✓

In hex: 7 = `0x07`, 128 = `0x80`. So 1,920 = **`0x0780`**. Look: the hex digits are just the two bytes side by side. Hex makes this easy to see.

Four bytes work the same way, with place values 1, 256, 65,536 and 16,777,216.

---

## 4.7 Bit shifts: moving bits left and right

📖 **New word: bit shift** — moving all the bits of a number left or right.

C++ has two shift operators:
- `a << n` — move the bits of `a` **left** by `n` places. New places on the right are filled with 0.
- `a >> n` — move the bits of `a` **right** by `n` places. Bits that fall off the right end are lost.

🔢 **Maths: shifting left multiplies by 2**

```
  13      = 0000 1101
  13 << 1 = 0001 1010 = 26     (13 × 2)
  13 << 2 = 0011 0100 = 52     (13 × 4)
```

Each shift left **doubles** the number, just like adding a 0 to the end of a decimal number multiplies it by 10.

> a << 8 = a × 256 (because 2⁸ = 256)
> a << 16 = a × 65,536

🔢 **Maths: shifting right divides by 2 (and drops the remainder)**

```
  200      = 1100 1000
  200 >> 4 = 0000 1100 = 12    (200 ÷ 16 = 12.5 → 12)
```

> a >> 4 = a ÷ 16, rounded down
> a >> 8 = a ÷ 256, rounded down

So `200 >> 4` gives **12**, which is `C` — the **left** hex digit of `C8`. A shift by 4 moves one hex digit away.

---

## 4.8 Masks: keeping only some bits

📖 **New word: mask** — a pattern of bits that says "keep these bits, clear the rest".

The `&` operator (bitwise AND) compares two numbers **bit by bit**. A result bit is 1 only if **both** bits are 1.

🔢 **Maths: keeping the low 4 bits of 200**

```
       200 = 1100 1000
 &    0x0F = 0000 1111     ← mask: 1s where we want to keep bits
 ----------------------
             0000 1000 = 8
```

So `200 & 0x0F` = **8**, which is the **right** hex digit of `C8`.

The `|` operator (bitwise OR) is 1 if **either** bit is 1. We use it to **join** parts together:

```
   0x07 << 8 = 0000 0111 0000 0000
 | 0x80      = 0000 0000 1000 0000
 ---------------------------------
               0000 0111 1000 0000 = 0x0780 = 1,920
```

### The two key recipes

🧠 **Remember — split a number into bytes:**

```cpp
byte0 =  value        & 0xFF;   // lowest byte
byte1 = (value >> 8)  & 0xFF;
byte2 = (value >> 16) & 0xFF;
byte3 = (value >> 24) & 0xFF;   // highest byte
```

🧠 **Remember — join bytes into a number:**

```cpp
value = byte0 | (byte1 << 8) | (byte2 << 16) | (byte3 << 24);
```

We use these recipes in **every** file format in Part 6 (BMP, PNG, GIF).

---

## 4.9 When a byte gets too big: wrap-around

📖 **New word: wrap-around** — when an unsigned number gets too big for its type, it starts again from 0.

A `std::uint8_t` can hold only 0 to 255. What is 250 + 10?

🔢 **Maths: 250 + 10 in one byte**

> Real answer: 260.
> 260 does not fit (biggest is 255).
> The byte keeps only the low 8 bits: 260 − 256 = **4**.

It is like a car's distance counter that only has 3 digits: after 999 it shows 000.

```
 ... 253 → 254 → 255 → 0 → 1 → 2 → 3 → 4
```

This matters a lot for images. If you make a bright pixel (250) "a bit brighter" (+10), it becomes **almost black** (4)! You get ugly dark spots in bright areas. Chapter 14 shows how to stop this with **clamping**.

⚠️ **Careful:** For **unsigned** types, wrap-around is a defined rule. For **signed** types (like `int`), going past the biggest value is an error in C++ (called "undefined behaviour"). Do maths in `int` or `double`, check the range, and only then store into a `std::uint8_t`.

---

## Code

File: `ch04/bytes.cpp`

```cpp
#include <iostream>
#include <cstdint>
#include <string>

std::string toBinary(std::uint8_t value) {
    std::string result;
    for (int bit = 7; bit >= 0; --bit) {
        if ((value >> bit) & 1) {
            result += '1';
        } else {
            result += '0';
        }
    }
    return result;
}

std::string toHex(std::uint8_t value) {
    const std::string digits = "0123456789ABCDEF";
    std::string result;
    result += digits[value >> 4];
    result += digits[value & 0x0F];
    return result;
}

int main() {
    const std::uint8_t values[] = {0, 1, 13, 128, 200, 255};
    for (std::uint8_t v : values) {
        std::cout << "decimal " << static_cast<int>(v)
                  << " = binary " << toBinary(v)
                  << " = hex " << toHex(v) << "\n";
    }

    const std::uint32_t orange = 0xFF8000;
    std::uint8_t red   = static_cast<std::uint8_t>((orange >> 16) & 0xFF);
    std::uint8_t green = static_cast<std::uint8_t>((orange >> 8) & 0xFF);
    std::uint8_t blue  = static_cast<std::uint8_t>(orange & 0xFF);
    std::cout << "\norange #FF8000:\n";
    std::cout << "  red   = " << static_cast<int>(red)   << " (hex " << toHex(red)   << ")\n";
    std::cout << "  green = " << static_cast<int>(green) << " (hex " << toHex(green) << ")\n";
    std::cout << "  blue  = " << static_cast<int>(blue)  << " (hex " << toHex(blue)  << ")\n";

    std::uint32_t joined = (static_cast<std::uint32_t>(red) << 16)
                         | (static_cast<std::uint32_t>(green) << 8)
                         | static_cast<std::uint32_t>(blue);
    std::cout << "  joined back = " << joined
              << (joined == orange ? " (same as before)" : " (different!)") << "\n";

    std::uint8_t bright = 250;
    bright = static_cast<std::uint8_t>(bright + 10);
    std::cout << "\n250 + 10 in one byte = " << static_cast<int>(bright) << "\n";

    std::uint8_t letter = 65;
    std::cout << "uint8_t 65 printed directly: " << letter << "\n";
    std::cout << "uint8_t 65 printed as int:   " << static_cast<int>(letter) << "\n";
    return 0;
}
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1 | `#include <iostream>` | Lets us print. |
| 2 | `#include <cstdint>` | Gives us `std::uint8_t` and `std::uint32_t`. |
| 3 | `#include <string>` | Lets us build text with `std::string`. |
| 5 | `std::string toBinary(std::uint8_t value) {` | A function that turns one byte into 8 characters of `0` and `1`. |
| 6 | `std::string result;` | Starts with empty text. We add one character per bit. |
| 7 | `for (int bit = 7; bit >= 0; --bit) {` | Look at the bits from the **left** (bit 7, worth 128) to the **right** (bit 0, worth 1). We go left to right because that is how we write numbers. |
| 8 | `if ((value >> bit) & 1) {` | Two steps. `value >> bit` moves the bit we want to the far right. `& 1` keeps **only** that far-right bit (mask `00000001`). The result is 1 or 0. |
| 9 | `result += '1';` | The bit is 1: add the character `'1'`. |
| 10–12 | `} else { result += '0'; }` | The bit is 0: add the character `'0'`. |
| 13 | `}` | End of the loop over 8 bits. |
| 14 | `return result;` | Give back the 8 characters. |
| 15 | `}` | End of `toBinary`. |
| 17 | `std::string toHex(std::uint8_t value) {` | A function that turns one byte into 2 hex characters. |
| 18 | `const std::string digits = "0123456789ABCDEF";` | The 16 hex digits in order. `digits[12]` is `'C'`. |
| 19 | `std::string result;` | Starts with empty text. |
| 20 | `result += digits[value >> 4];` | `value >> 4` keeps the **left** 4 bits (Section 4.7). For 200, that is 12 → `'C'`. |
| 21 | `result += digits[value & 0x0F];` | `value & 0x0F` keeps the **right** 4 bits (Section 4.8). For 200, that is 8 → `'8'`. |
| 22 | `return result;` | Gives back `"C8"`. |
| 23 | `}` | End of `toHex`. |
| 25 | `int main() {` | The program starts here. |
| 26 | `const std::uint8_t values[] = {0, 1, 13, 128, 200, 255};` | Some bytes to show. The compiler counts them (6) for us. |
| 27 | `for (std::uint8_t v : values) {` | Go through each byte. |
| 28 | `std::cout << "decimal " << static_cast<int>(v)` | Print the byte as a normal number. The **cast to `int`** is needed, or it prints as a letter (Section 4.5). |
| 29 | `<< " = binary " << toBinary(v)` | Then print it in binary. |
| 30 | `<< " = hex " << toHex(v) << "\n";` | Then print it in hex, and end the line. |
| 31 | `}` | End of the loop. |
| 33 | `const std::uint32_t orange = 0xFF8000;` | One 32-bit number that holds a whole colour: red `FF`, green `80`, blue `00`. |
| 34 | `std::uint8_t red = static_cast<std::uint8_t>((orange >> 16) & 0xFF);` | Shift right by 16 bits (4 hex digits) so `FF` is at the bottom. `& 0xFF` keeps only that byte. The cast says "yes, I want to store this in one byte". |
| 35 | `std::uint8_t green = ... ((orange >> 8) & 0xFF);` | Shift by 8 so `80` is at the bottom. Keep one byte → 128. |
| 36 | `std::uint8_t blue = ... (orange & 0xFF);` | No shift needed. Keep the lowest byte → 0. |
| 37 | `std::cout << "\norange #FF8000:\n";` | A heading, with an empty line before it. |
| 38–40 | `std::cout << "  red   = " ...` | Print each part as a number (cast to `int`) and as hex. |
| 42 | `std::uint32_t joined = (static_cast<std::uint32_t>(red) << 16)` | Start joining. First make `red` a 32-bit number, then shift it left by 16. We cast **before** shifting so there is room for the shifted bits. |
| 43 | `\| (static_cast<std::uint32_t>(green) << 8)` | OR in green, shifted left by 8. |
| 44 | `\| static_cast<std::uint32_t>(blue);` | OR in blue, with no shift. |
| 45 | `std::cout << "  joined back = " << joined` | Print the joined number in decimal: 16,744,448. |
| 46 | `<< (joined == orange ? " (same as before)" : " (different!)") << "\n";` | Check that splitting and joining gave back the same number. The `? :` picks one of two texts. |
| 48 | `std::uint8_t bright = 250;` | A bright byte. |
| 49 | `bright = static_cast<std::uint8_t>(bright + 10);` | `bright + 10` is done in `int`, so it is 260. Storing 260 in one byte keeps only the low 8 bits → **4**. This is wrap-around. |
| 50 | `std::cout << "\n250 + 10 in one byte = " ...` | Print the surprising result. |
| 52 | `std::uint8_t letter = 65;` | A byte with the value 65. |
| 53 | `std::cout << "uint8_t 65 printed directly: " << letter << "\n";` | Prints `A`, because `std::cout` treats the byte as a character. |
| 54 | `std::cout << "uint8_t 65 printed as int:   " << static_cast<int>(letter) << "\n";` | Prints `65`, because we cast it to `int` first. |
| 55 | `return 0;` | The program finished with no problem. |
| 56 | `}` | End of `main`. |

### What you should see

```
decimal 0 = binary 00000000 = hex 00
decimal 1 = binary 00000001 = hex 01
decimal 13 = binary 00001101 = hex 0D
decimal 128 = binary 10000000 = hex 80
decimal 200 = binary 11001000 = hex C8
decimal 255 = binary 11111111 = hex FF

orange #FF8000:
  red   = 255 (hex FF)
  green = 128 (hex 80)
  blue  = 0 (hex 00)
  joined back = 16744448 (same as before)

250 + 10 in one byte = 4
uint8_t 65 printed directly: A
uint8_t 65 printed as int:   65
```

🔢 **Maths: check the "joined back" number**

> 0xFF8000 = 255 × 65,536 + 128 × 256 + 0
> 255 × 65,536 = 16,711,680
> 128 × 256 = 32,768
> 16,711,680 + 32,768 = **16,744,448** ✓

---

## Small examples

### Example 1 — Binary of 77

| Place | Fits? | Bit | Left |
|---|---|---|---|
| 128 | no | 0 | 77 |
| 64 | yes | 1 | 13 |
| 32 | no | 0 | 13 |
| 16 | no | 0 | 13 |
| 8 | yes | 1 | 5 |
| 4 | yes | 1 | 1 |
| 2 | no | 0 | 1 |
| 1 | yes | 1 | 0 |

77 = `01001101`. Split into halves: `0100` = 4, `1101` = D. So 77 = **`0x4D`**.

### Example 2 — Read a web colour

`#3366CC`:
> red = 0x33 = 3 × 16 + 3 = 51
> green = 0x66 = 6 × 16 + 6 = 102
> blue = 0xCC = 12 × 16 + 12 = 204

A medium blue: lots of blue, some green, a little red.

### Example 3 — Get the "high" and "low" byte of 1,000

```cpp
std::uint16_t n = 1000;
int low  = n & 0xFF;          // 1000 & 255
int high = (n >> 8) & 0xFF;   // 1000 / 256
```

> high = 1,000 ÷ 256 = 3 (rounded down)
> low = 1,000 − 3 × 256 = 1,000 − 768 = 232
> check: 3 × 256 + 232 = 1,000 ✓
> In hex: 3 = `0x03`, 232 = `0xE8` → 1,000 = `0x03E8`.

### Example 4 — How much memory does an image need?

A 1,920 × 1,080 RGB image, 3 bytes per pixel:

> pixels = 2,073,600 (from Chapter 2)
> bytes = 2,073,600 × 3 = 6,220,800

That is about **6.2 million bytes** — roughly 6 megabytes — for **one** Full HD picture, with no compression. This is why PNG compression (Chapters 41–45) is useful.

---

## Common mistakes

⚠️ **Printing a `std::uint8_t` directly.** It prints a letter (or nothing visible). Always write `static_cast<int>(v)`.

⚠️ **Shifting a byte before making it bigger.** `red << 16` works in practice because C++ turns `red` into an `int` first, but for **24 bits and more**, a shift into the sign bit of an `int` causes trouble. Cast to `std::uint32_t` **first**, then shift, as in our code.

⚠️ **Forgetting `& 0xFF`.** `orange >> 8` alone gives `0xFF80`, not `0x80`. The mask removes the higher bytes.

⚠️ **Mixing up `&` and `&&`.** `&` works on each bit. `&&` means "and" for true/false. `200 & 15` is 8. `200 && 15` is `true`.

⚠️ **Wrap-around on bright pixels.** Adding to a byte near 255 jumps to a small number. Do the maths in `int`, then clamp (Chapter 14).

⚠️ **Thinking hex `10` means ten.** Hex `10` = 1 × 16 + 0 = **16**.

---

## Practice

🏋️ **1.** Change binary `10110010` into decimal.

🏋️ **2.** Change decimal 99 into binary, then into hex.

🏋️ **3.** What is `0x2A` in decimal? What is `0x100`?

🏋️ **4.** What are the red, green and blue values of the colour `#80FF40`?

🏋️ **5.** Work out `90 >> 2` and `90 << 1`. Check them with multiplying and dividing.

🏋️ **6.** Work out `0xB7 & 0x0F` and `0xB7 >> 4`. What do the two answers mean?

🏋️ **7.** A `std::uint8_t` holds 5. We subtract 10. What value does it hold now? (Hint: wrap-around also works downward.)

🏋️ **8.** Write the 4 bytes (lowest first) of the number `0x12345678`, using the recipe from Section 4.8.

---

## Answers

**1.**
```
place:  128  64  32  16   8   4   2   1
bit:      1   0   1   1   0   0   1   0
```
> 128 + 32 + 16 + 2 = **178**

**2.**
> 99: 64 fits → 1, left 35. 32 fits → 1, left 3. 16 no → 0. 8 no → 0. 4 no → 0. 2 fits → 1, left 1. 1 fits → 1, left 0.
> 128 doesn't fit, so the first bit is 0.
> binary = `01100011`
> halves: `0110` = 6, `0011` = 3 → hex **`0x63`**
> check: 6 × 16 + 3 = 96 + 3 = 99 ✓

**3.**
> 0x2A = 2 × 16 + 10 = 32 + 10 = **42**
> 0x100 = 1 × 256 + 0 × 16 + 0 = **256** (one more than the biggest byte, so it needs two bytes)

**4.**
> red = 0x80 = 8 × 16 + 0 = **128**
> green = 0xFF = **255**
> blue = 0x40 = 4 × 16 + 0 = **64**

A bright yellow-green.

**5.**
> 90 >> 2 = 90 ÷ 4 = 22.5 → **22** (rounded down)
> 90 << 1 = 90 × 2 = **180**

In binary: 90 = `01011010`. Shift right by 2: `00010110` = 16 + 4 + 2 = 22 ✓. Shift left by 1: `10110100` = 128 + 32 + 16 + 4 = 180 ✓.

**6.**
> 0xB7 & 0x0F = **0x07** = 7 (the right hex digit)
> 0xB7 >> 4 = **0x0B** = 11 (the left hex digit)

These are exactly the two halves `toHex` uses on lines 20 and 21 of our code.

**7.**
> 5 − 10 = −5 in real maths.
> A byte cannot hold −5. It wraps around downward:
> −5 + 256 = **251**

So the pixel goes from almost black (5) to almost white (251). This is the opposite problem from Section 4.9, and it is just as ugly.

**8.**
> byte0 = 0x12345678 & 0xFF = **0x78**
> byte1 = (0x12345678 >> 8) & 0xFF = 0x123456 & 0xFF = **0x56**
> byte2 = (0x12345678 >> 16) & 0xFF = 0x1234 & 0xFF = **0x34**
> byte3 = (0x12345678 >> 24) & 0xFF = 0x12 & 0xFF = **0x12**

Lowest first: **78 56 34 12**. Notice they look "backwards". This order is called **little-endian**, and BMP files use it. Chapter 36 explains it fully.

---

## Summary

🧠 A **bit** is 0 or 1. A **byte** is 8 bits and holds **0 to 255**.

🧠 In **binary**, place values are 1, 2, 4, 8, 16, 32, 64, 128.

🧠 In **hex**, digits go 0–9 then A–F (10–15). **Two hex digits = one byte.** `0xFF` = 255.

🧠 One RGB pixel = 3 bytes = 24 bits = about 16.7 million possible colours.

🧠 Use `std::uint8_t`, `std::uint16_t`, `std::uint32_t` for exact sizes. **Cast to `int` before printing a byte.**

🧠 `>>` and `<<` move bits. `&` keeps bits (mask). `|` joins bits.

🧠 Split: `(value >> 8*k) & 0xFF`. Join: `b0 | (b1 << 8) | (b2 << 16) | (b3 << 24)`.

🧠 Unsigned bytes **wrap around**: 250 + 10 = 4. Do the maths in `int` first.

---

## Next chapter

We now know a colour is three bytes. But **why** red, green and blue? Why does red + green make **yellow**, when in paint it makes brown? In Chapter 5 we learn **the RGB colour model** and how light mixing really works.
