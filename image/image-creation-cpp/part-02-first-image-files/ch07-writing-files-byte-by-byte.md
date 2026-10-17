# Chapter 7 — Writing Files Byte by Byte

> **Part 2 · Chapter 7 of 82**
> **You need:** Chapters 1–6 · **You will make:** `bytes.bin` (a file with exact bytes), a reader that loads it back, and a small **hex viewer**

---

## What you will learn

- What a file really is: **a named list of bytes**.
- Why "text files" and "binary files" are really the same thing.
- How to open a file for writing in **binary mode**, and why it matters on Windows.
- How to write **one byte** with `put`, and **many bytes** with `write`.
- What `reinterpret_cast<const char*>` does, and why `write` needs it.
- How to read every byte of a file back into a `std::vector<std::uint8_t>`.
- How to build a **hex viewer**: a program that shows every byte of any file.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **file** | A named list of bytes, kept on a disk. |
| **disk** | The part of the computer that keeps files when the power is off. |
| **character code** | The number that stands for a letter. In ASCII, `A` is 65. |
| **ASCII** | A common table of character codes for English letters, digits and signs. |
| **text file** | A file whose bytes are meant to be read as letters. |
| **binary file** | A file whose bytes are meant to be read as numbers (like pixels). |
| **stream** | A C++ object that sends bytes to (or takes bytes from) a file, one after another. |
| **text mode** | A way to open a file where C++ may change some bytes (like line endings). |
| **binary mode** | A way to open a file where every byte is written **exactly** as given. |
| **line ending** | The byte (or bytes) that mark the end of one line of text. |
| **hex dump** | A print-out of every byte of a file in hexadecimal. |
| **offset** | The position of a byte inside a file, counting from 0. |

---

## 7.1 What is a file?

📖 **New word: file** — a named list of bytes kept on a disk.

📖 **New word: disk** — the part of the computer that keeps files when the power is off (a hard disk or an SSD).

That is all a file is. A name, and bytes:

```
name:   bytes.bin
bytes:  48 69 21 0A 00 0D 80 FF ...
```

A file does **not** know what it "is". It does not know if it is a photo, a song or a letter. It is only bytes. **Programs** decide what the bytes mean.

- An image viewer reads the bytes and **guesses** they are an image (from the first few bytes and the file name).
- A text editor reads the same bytes as **letters**.

🧠 **Remember:** A file is just a list of bytes, from 0 to 255 each. Our image files will be exactly the bytes **we** choose.

### The size of a file

The size of a file is the number of bytes in it. A file with 20 bytes has a size of 20. In Chapter 6, a 4 × 3 image needed 36 bytes of memory. If we save those bytes, plus a small header, the file is a little more than 36 bytes.

---

## 7.2 Text files are bytes too

📖 **New word: character code** — the number that stands for a letter, a digit or a sign.

📖 **New word: ASCII** — a common table of character codes. It was made in the 1960s and is still used today.

Here are some ASCII codes:

| Character | Code (decimal) | Code (hex) |
|---|---|---|
| `0` (the digit) | 48 | 30 |
| `1` | 49 | 31 |
| `9` | 57 | 39 |
| `A` | 65 | 41 |
| `B` | 66 | 42 |
| `H` | 72 | 48 |
| `a` | 97 | 61 |
| `i` | 105 | 69 |
| space | 32 | 20 |
| `!` | 33 | 21 |
| new line | 10 | 0A |

So the text `Hi!` in a file is really the three bytes **72 105 33** (hex `48 69 21`).

📖 **New word: text file** — a file whose bytes are meant to be read as letters.

📖 **New word: binary file** — a file whose bytes are meant to be read as numbers.

There is **no real difference** in the file. The difference is only in how we **use** the bytes.

⚠️ **Careful:** The **digit** `5` is **not** the byte 5. The digit `5` is the byte **53** (48 + 5). This matters a lot in Chapter 8, where we write the number `255` as **three text characters** `2`, `5`, `5` (bytes 50 53 53), and in Chapter 9, where we write it as **one byte** 255.

🔢 **Maths: the code of a digit**

> code of digit d = 48 + d
> code of '7' = 48 + 7 = 55
> And back: digit = code − 48. Code 52 → 52 − 48 = 4.

---

## 7.3 Streams: sending bytes to a file

📖 **New word: stream** — a C++ object that sends bytes **to** a file (or takes bytes **from** a file), one after another, in order.

From `<fstream>` we use two types:

| Type | Direction |
|---|---|
| `std::ofstream` | **o**utput: program → file (writing) |
| `std::ifstream` | **i**nput: file → program (reading) |

You may already have used them for text, with `<<` and `>>`. For images we use them a bit differently.

### Opening a file

```cpp
std::ofstream file("bytes.bin", std::ios::binary);
```

- `"bytes.bin"` is the file name. The file is made in the **current folder** (usually the folder you ran the program from).
- If the file already exists, it is **emptied** first and then written again.
- `std::ios::binary` opens it in **binary mode** (Section 7.4).

### Did it open?

Opening can fail. For example, the folder may not exist, or another program may have the file locked. Always check:

```cpp
if (!file) {
    std::cout << "Could not open the file!\n";
    return 1;
}
```

`!file` is `true` when the stream is in a **failed** state. We check this after opening, and again after writing.

### Closing

The file is **closed** automatically when the `std::ofstream` object is destroyed — for example, at the end of the `{ }` block or function where it was made. Closing makes sure every byte has really been sent to the disk. You can also call `file.close();` yourself.

---

## 7.4 Text mode and binary mode — the hidden trap

📖 **New word: line ending** — the byte (or bytes) that mark the end of a line of text.

Different computers mark the end of a line in different ways:

| System | Line ending | Bytes |
|---|---|---|
| Linux, macOS | "line feed" | `0A` (10) |
| Windows | "carriage return" + "line feed" | `0D 0A` (13 10) |

In C++, `'\n'` is always the single byte **10**.

📖 **New word: text mode** — the normal way a file opens. On **Windows**, in text mode, C++ **changes every byte 10 into the two bytes 13 10** when writing. (And back again when reading.)

📖 **New word: binary mode** — with `std::ios::binary`, C++ writes **every byte exactly as given**. Nothing is changed.

### Why this destroys images

Imagine a pixel with the colour (10, 20, 30). We write the three bytes `0A 14 1E`.

In **text mode on Windows**, the file gets **four** bytes: `0D 0A 14 1E`.

```
what we wrote:      0A 14 1E  ...
what the file gets: 0D 0A 14 1E ...
                    ↑ an extra byte appeared!
```

Now every byte after it is **one place late**. The red of the next pixel is read as its green, the green as blue, and so on. The rest of the picture turns into stripes of wrong colours. Every byte with the value 10 adds another shift.

On Linux and macOS, text mode and binary mode are the same, so the bug **hides**. Your program works on one computer and breaks on another.

🧠 **Remember:** Image bytes are **always** written with `std::ios::binary`. Always. Even on Linux.

---

## 7.5 Writing one byte: `put`

```cpp
file.put(static_cast<char>(200));
```

`put` writes **one** byte. It takes a `char`.

Why the cast? Our bytes are `std::uint8_t` (0 to 255). On most computers, a `char` holds −128 to 127. The value 200 does not fit as a **number**, but the **8 bits** are the same:

🔢 **Maths: the same 8 bits, read two ways**

> 200 in binary = `11001000` (Chapter 4)
> As unsigned (0–255): 128 + 64 + 8 = 200
> As signed (−128–127): the left bit counts as **−128** instead of +128: −128 + 64 + 8 = **−56**

So `static_cast<char>(200)` gives the `char` −56. Its bits are `11001000`. `put` writes those bits. The file gets the byte **200** (hex `C8`). Nothing is lost.

💡 **Tip:** The rule "the left bit counts as −128" is called **two's complement**. You do not need to use it yourself. You only need to know: **the bits are kept**, so casting a byte to `char` and back is safe.

---

## 7.6 Writing many bytes: `write`

Writing one byte at a time works, but it is slow for big images (millions of calls). `write` sends a **whole block** in one call:

```cpp
file.write(reinterpret_cast<const char*>(data.data()), data.size());
```

Let us take this apart.

| Part | Meaning |
|---|---|
| `data.data()` | A pointer to the **first byte** inside the vector. The vector keeps its bytes in one block, one after another (Chapter 6), so this one pointer is enough. Its type is `const std::uint8_t*`. |
| `reinterpret_cast<const char*>(...)` | `write` wants a `const char*`, not a `const std::uint8_t*`. This cast says: "use the **same address**, but call the bytes `char`". No bytes are changed or moved. |
| `data.size()` | How many bytes to write. |

📖 **`reinterpret_cast`** — a C++ cast that keeps the same address but reads the memory as another type. It is usually dangerous. But reading any memory as `char` (bytes) is one of the few **always allowed** uses. Writing and reading raw bytes is exactly what it is for.

🔢 **Maths: what `write` does, step by step**

> Pointer to address 5000 (say), size 4.
> It writes the byte at 5000, then 5001, then 5002, then 5003.
> Four bytes, in memory order.

This is why the **memory order** of Chapter 6 matters: `write` sends our pixel buffer to the file in exactly that order.

⚠️ **Careful:** The second argument of `write` has the type `std::streamsize`, which is a **signed** type. `data.size()` is unsigned. Many compilers accept it with no warning, but to be clean we write `static_cast<std::streamsize>(data.size())`.

---

## 7.7 Reading bytes back

To check our files, we will read them back. We open with `std::ifstream` and **binary mode** (for the same reason as in Section 7.4: in text mode on Windows, `0D 0A` would turn into a single `0A`).

The simplest way to read **every** byte:

```cpp
char c;
while (file.get(c)) {
    data.push_back(static_cast<std::uint8_t>(c));
}
```

- `file.get(c)` reads **one** byte into `c`. It returns the stream, and the stream counts as `true` while reading works.
- At the end of the file, reading fails, the stream becomes `false`, and the loop stops.
- `static_cast<std::uint8_t>(c)` turns the `char` back into 0–255. The value −56 becomes 200 again (the same bits, Section 7.5).

This reads one byte per call, so it is slow for very big files. It is fine for this chapter. In Chapter 12, when we read whole images, we use a faster way with `read`.

---

## 7.8 A hex viewer

📖 **New word: hex dump** — a print-out of every byte of a file in hexadecimal.

📖 **New word: offset** — the position of a byte inside a file, counting from 0. (The same idea as an index in Chapter 6.)

Programmers use hex dumps all the time to **look inside** files. We will build one, and use it in **every** chapter of Part 2 and Part 6 to check that our files are right.

A hex dump shows **16 bytes per line**. Each line starts with the offset of its first byte, in hex:

```
0000:  48 69 21 0A 00 0D 80 FF CA FE BA BE 01 02 03 04
0010:  05 06 07 08
```

🔢 **Maths: why the second line starts at `0010`**

> Each line has 16 bytes.
> The first line holds offsets 0 to 15.
> The second line starts at offset 16.
> 16 in hex = 1 × 16 + 0 = `10`. Written with 4 digits: `0010`.

🔢 **Maths: which byte is at offset `0x0A`?**

> 0x0A = 10
> Line 1 holds offsets 0–15, so offset 10 is on line 1.
> Count from 0: 48(0) 69(1) 21(2) 0A(3) 00(4) 0D(5) 80(6) FF(7) CA(8) FE(9) **BA(10)**.

To print the offset with 4 hex digits, we reuse `toHex` from Chapter 4 twice: once for the **high byte** of the offset (`offset >> 8`) and once for the **low byte** (`offset & 0xFF`). This is the "split a number into bytes" recipe from Chapter 4.

---

## Code

File: `ch07/bytes_file.cpp`

```cpp
#include <iostream>
#include <fstream>
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

bool writeBytes(const std::string& fileName, const std::vector<std::uint8_t>& data) {
    std::ofstream file(fileName, std::ios::binary);
    if (!file) {
        return false;
    }
    file.write(reinterpret_cast<const char*>(data.data()),
               static_cast<std::streamsize>(data.size()));
    return static_cast<bool>(file);
}

std::vector<std::uint8_t> readBytes(const std::string& fileName) {
    std::vector<std::uint8_t> data;
    std::ifstream file(fileName, std::ios::binary);
    if (!file) {
        return data;
    }
    char c;
    while (file.get(c)) {
        data.push_back(static_cast<std::uint8_t>(c));
    }
    return data;
}

void hexDump(const std::vector<std::uint8_t>& data) {
    const int count = static_cast<int>(data.size());
    for (int i = 0; i < count; ++i) {
        if (i % 16 == 0) {
            std::cout << toHex(static_cast<std::uint8_t>((i >> 8) & 0xFF))
                      << toHex(static_cast<std::uint8_t>(i & 0xFF)) << ":  ";
        }
        std::cout << toHex(data[i]) << ' ';
        if (i % 16 == 15 || i == count - 1) {
            std::cout << "\n";
        }
    }
}

int main() {
    const std::vector<std::uint8_t> data = {
        72, 105, 33, 10, 0, 13, 128, 255,
        0xCA, 0xFE, 0xBA, 0xBE, 1, 2, 3, 4,
        5, 6, 7, 8
    };

    if (!writeBytes("bytes.bin", data)) {
        std::cout << "Could not write bytes.bin\n";
        return 1;
    }
    std::cout << "wrote " << data.size() << " bytes to bytes.bin\n";

    std::vector<std::uint8_t> back = readBytes("bytes.bin");
    std::cout << "read back " << back.size() << " bytes:\n";
    hexDump(back);

    std::cout << (back == data ? "same bytes: OK\n" : "bytes are different!\n");

    {
        std::ofstream textFile("text_mode.txt");
        textFile << "A\nB";
    }
    {
        std::ofstream binFile("binary_mode.txt", std::ios::binary);
        binFile << "A\nB";
    }
    std::cout << "\ntext mode file:   ";
    hexDump(readBytes("text_mode.txt"));
    std::cout << "binary mode file: ";
    hexDump(readBytes("binary_mode.txt"));
    return 0;
}
```

### Line by line

| Line | Code | What it does, in simple words |
|---|---|---|
| 1 | `#include <iostream>` | Printing. |
| 2 | `#include <fstream>` | File streams: `std::ofstream` and `std::ifstream`. |
| 3 | `#include <cstdint>` | `std::uint8_t`. |
| 4 | `#include <string>` | File names and `toHex` results. |
| 5 | `#include <vector>` | A list of bytes. |
| 7–13 | `std::string toHex(...) { ... }` | Same as Chapter 4: one byte → two hex digits. |
| 15 | `bool writeBytes(const std::string& fileName, const std::vector<std::uint8_t>& data) {` | A function that writes all bytes of `data` into a file. It returns `true` if it worked. |
| 16 | `std::ofstream file(fileName, std::ios::binary);` | Open (or make) the file for writing, in **binary mode** (Section 7.4). |
| 17 | `if (!file) {` | Did opening fail? |
| 18 | `return false;` | Then say "it did not work". |
| 19 | `}` | End of the check. |
| 20 | `file.write(reinterpret_cast<const char*>(data.data()),` | Write the whole block, starting at the first byte of the vector (Section 7.6). |
| 21 | `static_cast<std::streamsize>(data.size()));` | …and write this many bytes. The cast changes the size into the type `write` wants. |
| 22 | `return static_cast<bool>(file);` | After writing, the stream is still `true` only if every byte was written. We give that back. (The file closes when the function ends.) |
| 23 | `}` | End of `writeBytes`. |
| 25 | `std::vector<std::uint8_t> readBytes(const std::string& fileName) {` | A function that reads every byte of a file and gives them back in a vector. |
| 26 | `std::vector<std::uint8_t> data;` | Start with an empty list. |
| 27 | `std::ifstream file(fileName, std::ios::binary);` | Open the file for reading, in binary mode. |
| 28–30 | `if (!file) { return data; }` | If it could not open (for example, the file does not exist), give back the empty list. |
| 31 | `char c;` | A place to hold one byte while reading. |
| 32 | `while (file.get(c)) {` | Read one byte. Keep going while reading works. At the end of the file, the loop stops (Section 7.7). |
| 33 | `data.push_back(static_cast<std::uint8_t>(c));` | Add the byte to the list, as 0–255. |
| 34 | `}` | End of the loop. |
| 35 | `return data;` | Give back all the bytes. |
| 36 | `}` | End of `readBytes`. |
| 38 | `void hexDump(const std::vector<std::uint8_t>& data) {` | A function that prints bytes as a hex dump (Section 7.8). |
| 39 | `const int count = static_cast<int>(data.size());` | The number of bytes, as an `int`, so we can compare it with `i` without a warning. |
| 40 | `for (int i = 0; i < count; ++i) {` | Go through every byte. `i` is the offset. |
| 41 | `if (i % 16 == 0) {` | At the **start** of each line of 16 (offsets 0, 16, 32, …)… |
| 42 | `std::cout << toHex(static_cast<std::uint8_t>((i >> 8) & 0xFF))` | …print the high byte of the offset in hex… |
| 43 | `<< toHex(static_cast<std::uint8_t>(i & 0xFF)) << ":  ";` | …then the low byte, then a colon and two spaces. Together: 4 hex digits, like `0010`. |
| 44 | `}` | End of the line start. |
| 45 | `std::cout << toHex(data[i]) << ' ';` | Print this byte in hex, and a space. |
| 46 | `if (i % 16 == 15 \|\| i == count - 1) {` | After the 16th byte of a line (offsets 15, 31, …), **or** after the very last byte… |
| 47 | `std::cout << "\n";` | …end the line. |
| 48 | `}` | End of the line end. |
| 49 | `}` | End of the loop. |
| 50 | `}` | End of `hexDump`. |
| 52 | `int main() {` | The program starts here. |
| 53 | `const std::vector<std::uint8_t> data = {` | The 20 bytes we will write. We chose them to show special values. |
| 54 | `72, 105, 33, 10, 0, 13, 128, 255,` | `H`, `i`, `!` in ASCII; then **10** (line feed — the dangerous one); **0**; **13** (carriage return); **128** (the left bit only); **255** (the biggest byte). |
| 55 | `0xCA, 0xFE, 0xBA, 0xBE, 1, 2, 3, 4,` | Four bytes written in hex (programmers like `CAFEBABE` because it is easy to spot in a dump), then 1 to 4. |
| 56 | `5, 6, 7, 8` | Then 5 to 8. |
| 57 | `};` | End of the list. |
| 59 | `if (!writeBytes("bytes.bin", data)) {` | Write the file. If it did not work… |
| 60 | `std::cout << "Could not write bytes.bin\n";` | …say so… |
| 61 | `return 1;` | …and stop. `1` tells the system "there was a problem". |
| 62 | `}` | End of the check. |
| 63 | `std::cout << "wrote " << data.size() << " bytes to bytes.bin\n";` | Say how many bytes we wrote: 20. |
| 65 | `std::vector<std::uint8_t> back = readBytes("bytes.bin");` | Read the file back into a new vector. |
| 66 | `std::cout << "read back " << back.size() << " bytes:\n";` | Say how many bytes came back. It should also be 20. |
| 67 | `hexDump(back);` | Show every byte. |
| 69 | `std::cout << (back == data ? "same bytes: OK\n" : "bytes are different!\n");` | `==` on two vectors compares **every** element. If they are the same, the file is exactly right. |
| 71 | `{` | Start a small block. Anything made inside is destroyed at the `}`. |
| 72 | `std::ofstream textFile("text_mode.txt");` | Open a file **without** `std::ios::binary` — text mode. |
| 73 | `textFile << "A\nB";` | Write `A`, a line feed, and `B`. |
| 74 | `}` | End of the block. `textFile` is destroyed here, so the file is **closed**. Now we can read it. |
| 75–78 | `{ std::ofstream binFile(... std::ios::binary); binFile << "A\nB"; }` | The same three characters, but in **binary mode**. |
| 79 | `std::cout << "\ntext mode file:   ";` | A label. |
| 80 | `hexDump(readBytes("text_mode.txt"));` | Read the text-mode file and show its bytes. |
| 81 | `std::cout << "binary mode file: ";` | A label. |
| 82 | `hexDump(readBytes("binary_mode.txt"));` | Read the binary-mode file and show its bytes. |
| 83 | `return 0;` | The program finished with no problem. |
| 84 | `}` | End of `main`. |

### What you should see

On **Windows**:

```
wrote 20 bytes to bytes.bin
read back 20 bytes:
0000:  48 69 21 0A 00 0D 80 FF CA FE BA BE 01 02 03 04 
0010:  05 06 07 08 
same bytes: OK

text mode file:   0000:  41 0D 0A 42 
binary mode file: 0000:  41 0A 42 
```

On **Linux and macOS**, the last two lines are the same:

```
text mode file:   0000:  41 0A 42 
binary mode file: 0000:  41 0A 42 
```

Look at the Windows text-mode file: `41 0D 0A 42`. We wrote **3** bytes (`A`, `\n`, `B`), but the file has **4**. The extra `0D` is the trap from Section 7.4. In binary mode, the file has exactly the 3 bytes we wrote.

And in `bytes.bin`, the byte `0A` at offset 3 stayed **one** byte, because we used binary mode.

💡 **Tip:** You can also check the file size with your system's file explorer. `bytes.bin` should show **20 bytes**.

---

## Small examples

### Example 1 — Write bytes one at a time with `put`

```cpp
std::ofstream file("count.bin", std::ios::binary);
for (int v = 0; v < 256; ++v) {
    file.put(static_cast<char>(v));
}
```

This makes a file with **256 bytes**: 00, 01, 02, … FF. Every possible byte, once. The hex dump has 256 ÷ 16 = **16 lines**, from `0000:` to `00F0:`. The last line is `00F0:  F0 F1 F2 F3 F4 F5 F6 F7 F8 F9 FA FB FC FD FE FF`.

### Example 2 — Text numbers vs byte numbers

```cpp
std::ofstream a("text255.bin", std::ios::binary);
a << 255;                          // writes the characters '2' '5' '5'

std::ofstream b("byte255.bin", std::ios::binary);
b.put(static_cast<char>(255));     // writes one byte, 255
```

> text255.bin: `32 35 35` — 3 bytes (ASCII codes 50, 53, 53)
> byte255.bin: `FF` — 1 byte

`<<` on a stream always writes a number **as text**, even in binary mode. Binary mode only stops the line-ending change. To write a raw byte, use `put` or `write`. Chapter 8 uses text (`<<`). Chapter 9 uses raw bytes (`write`).

### Example 3 — Find a byte by its offset

In our dump, what is at offset `0x13`?

> 0x13 = 1 × 16 + 3 = 19
> Line 2 starts at offset 16 (`0010`). 19 − 16 = 3, so it is the 4th byte on line 2 (counting from 0: 05, 06, 07, **08**).

It is `08` — the last byte of the file. (A 20-byte file has offsets 0 to 19.)

### Example 4 — Save the Chapter 6 pixel buffer

The 4 × 3 buffer from Chapter 6 is a `std::vector<std::uint8_t>` of 36 bytes. We can save it with **one line**:

```cpp
writeBytes("pixels.raw", pixels);
```

The hex dump shows the same 36 bytes as Chapter 6, in 3 lines (16 + 16 + 4). But no image viewer can open it! It does not know the **width** or **height**. It does not even know it is a picture. A real image file needs a **header** at the start that says these things. That is the next chapter.

---

## Common mistakes

⚠️ **Forgetting `std::ios::binary`.** Works on Linux, breaks on Windows. Every byte 10 becomes two bytes, and the image is shifted.

⚠️ **Using `<<` for raw bytes.** `file << pixel` where `pixel` is a `std::uint8_t` writes it as a **character**, which is actually the right byte by accident, but `file << 200` (an `int`) writes the text `200` (3 bytes). Use `put` or `write` for raw bytes.

⚠️ **Reading the file before it is closed.** If the `std::ofstream` is still alive, some bytes may still be waiting in memory and not yet on the disk. Close it first (end its block, or call `close()`).

⚠️ **Not checking if the file opened.** If the folder does not exist, nothing is written, and there is no error unless you check.

⚠️ **Printing the dump without `toHex`.** Raw bytes in the terminal show strange signs or nothing at all.

⚠️ **Thinking the file name decides the type.** Naming a file `photo.png` does not make it a PNG. The **bytes inside** decide. (Viewers often look at the name first, though, so we still pick the right name.)

---

## Practice

🏋️ **1.** What bytes (in hex) does the text `Cat` take in a file? Use the ASCII table (`a` is 97, and the small letters go in order: `b` = 98, `c` = 99, …; `C` is 67, and `t` is 116).

🏋️ **2.** We write the byte 230 with `put`. What `char` value does `static_cast<char>(230)` give on a computer where `char` is signed? Does the file get the byte 230?

🏋️ **3.** On Windows, in text mode, we write the 5 bytes `01 0A 0A 02 0A`. How many bytes does the file have?

🏋️ **4.** A hex dump of a file has 7 full lines and one last line with 5 bytes. How big is the file? What is the offset of the last byte, in hex?

🏋️ **5.** Change `bytes_file.cpp` to write the bytes 250 to 255 after the other bytes. What does the second dump line look like now?

🏋️ **6.** Write a program that writes `count.bin` from Example 1 and prints its hex dump. Check the last line.

🏋️ **7.** Change `hexDump` to also print the **characters** at the end of each line (like real hex viewers): print the byte as a `char` if it is between 32 and 126, and a `.` otherwise. (The line will look like `48 69 21 0A ...  Hi!.....`.)

---

## Answers

**1.**
> `C` = 67 = 0x43
> `a` = 97 = 0x61
> `t` = 116 = 7 × 16 + 4 = 0x74
> So `43 61 74`.

**2.**
> 230 = `11100110`
> Signed: −128 + 64 + 32 + 4 + 2 = **−26**
> `put` writes the 8 bits `11100110`, so the file gets the byte **230** (`E6`). Yes.
> (Quick rule: for values above 127, signed value = value − 256. 230 − 256 = −26 ✓.)

**3.** Each `0A` becomes `0D 0A`. There are three `0A` bytes.
> 5 + 3 = **8 bytes**: `01 0D 0A 0D 0A 02 0D 0A`.

**4.**
> 7 × 16 + 5 = 112 + 5 = **117 bytes**
> Offsets go from 0 to 116.
> 116 = 7 × 16 + 4 = **0x74**
> (The last line starts at offset 112 = `0x70`, and the 5th byte on it is at 112 + 4 = 116.)

**5.** Add `250, 251, 252, 253, 254, 255` to the list (after `8`). The file now has 26 bytes. The second line becomes:

```
0010:  05 06 07 08 FA FB FC FD FE FF 
```

> 250 = 15 × 16 + 10 = `FA`, and so on up to 255 = `FF`.

**6.**

```cpp
std::vector<std::uint8_t> all;
for (int v = 0; v < 256; ++v) {
    all.push_back(static_cast<std::uint8_t>(v));
}
writeBytes("count.bin", all);
hexDump(readBytes("count.bin"));
```

The last line is `00F0:  F0 F1 F2 F3 F4 F5 F6 F7 F8 F9 FA FB FC FD FE FF`. Each line's offset is the same as its first byte, because byte n has the value n.

**7.** One way: keep the bytes of the current line, and print them as characters when the line ends.

```cpp
void hexDump(const std::vector<std::uint8_t>& data) {
    const int count = static_cast<int>(data.size());
    std::string chars;
    for (int i = 0; i < count; ++i) {
        if (i % 16 == 0) {
            std::cout << toHex(static_cast<std::uint8_t>((i >> 8) & 0xFF))
                      << toHex(static_cast<std::uint8_t>(i & 0xFF)) << ":  ";
            chars.clear();
        }
        std::cout << toHex(data[i]) << ' ';
        if (data[i] >= 32 && data[i] <= 126) {
            chars += static_cast<char>(data[i]);
        } else {
            chars += '.';
        }
        if (i % 16 == 15 || i == count - 1) {
            std::cout << " " << chars << "\n";
        }
    }
}
```

Codes 32 to 126 are the **printable** ASCII characters (space to `~`). Others, like 10 (line feed) or 0, would mess up the terminal, so we show a dot. The first line of `bytes.bin` ends with `Hi!.............` (the `H`, `i`, `!`, then 13 dots). This is very useful in Chapter 8, because a P3 file is **all** printable text.

---

## Summary

🧠 A **file** is a named list of bytes. Programs decide what the bytes mean.

🧠 Text is bytes too: **ASCII** gives each character a number. The digit `5` is byte **53**, not 5.

🧠 Open image files with **`std::ios::binary`**. Text mode on Windows turns byte 10 into 13 10 and breaks images.

🧠 `put(c)` writes one byte. `write(ptr, n)` writes n bytes from memory, in order.

🧠 `reinterpret_cast<const char*>(data.data())` lets `write` send our `std::uint8_t` buffer. The bytes do not change.

🧠 `<<` writes numbers **as text**. `put`/`write` write **raw bytes**.

🧠 A **hex dump** shows every byte, 16 per line, with the **offset** at the start. We use it to check every file we make.

---

## Next chapter

Saving the raw pixel bytes was not enough: a viewer needs to know the width, the height and the type. In Chapter 8 we add a small **header** and write our very first real image — a 3 × 2 picture in the **PPM** format — that any PPM viewer can open.
