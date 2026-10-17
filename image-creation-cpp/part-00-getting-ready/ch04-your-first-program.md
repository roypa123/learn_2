# Chapter 04 — Your First C++ Program

> Part 0 — Getting Ready · Chapter 04 of 90 · about 10 pages

---

## What you will learn

- How to write a C++ program in a `.cpp` file.
- How to **compile** it and **run** it.
- What **every line** of a small program means: `#include`, `int main()`, `{ }`, `std::cout`, `<<`, `"text"`, `\n`, `;`, `return 0`.
- How to print a small **picture made of letters** — our first "image"!
- How to read **error messages** and fix them.

---

## Words you need

| Word | Simple meaning |
|---|---|
| **program** | A list of instructions for the computer. |
| **statement** | One instruction in C++. It usually ends with `;`. |
| **function** | A named group of instructions. `main` is a function. |
| **main** | The function where every C++ program **starts**. |
| **header** | A file of ready tools from the standard library. We add it with `#include`. |
| **string** (text) | Letters, numbers and symbols between double quotes `"like this"`. |
| **output** | What the program shows or gives back. Here: text in the terminal. |
| **semicolon** | The sign `;`. It marks the end of a statement, like a full stop ends a sentence. |
| **curly braces** | The signs `{` and `}`. They hold a group of statements together. |
| **error** | A mistake the compiler finds. The program is **not** made until you fix it. |
| **warning** | Something that is allowed but looks like a mistake. The program **is** made. |

---

## 1. The big idea

A program is like a **letter of instructions** to a helper.
A good letter has a clear form:

```
  Dear helper,                       ← who it is for / where it starts
     1. Say "Hello!"                 ← the instructions,
     2. Say "I can make pictures."      one by one, in order
  Thank you. The end.                ← how it finishes
```

A C++ program also has a fixed form:

```cpp
#include <iostream>                  // get the tools for printing

int main() {                         // the program starts here
    std::cout << "Hello!\n";         // instruction 1
    std::cout << "I can make pictures.\n";   // instruction 2
    return 0;                        // finish: "all went well"
}                                    // the end of main
```

The computer follows the instructions **from top to bottom, one at a time**, starting at `main`.

🧠 **Remember:** Every C++ program starts in `main`, and runs its statements in order, from top to bottom.

---

## 2. The three steps: write, compile, run

Every time you make a program, you do three steps:

```
 ┌─────────────┐       ┌─────────────┐       ┌─────────────┐
 │ 1. WRITE    │  ──►  │ 2. COMPILE  │  ──►  │ 3. RUN      │
 │ hello.cpp   │       │ g++ ...     │       │ .\hello.exe │
 │ (editor)    │       │ (terminal)  │       │ (terminal)  │
 └─────────────┘       └─────────────┘       └─────────────┘
        ▲                     │
        └──── error? fix ─────┘
```

If the compiler finds an error in step 2, you go back to step 1, fix the code, and compile again.

---

## 3. The code

Go to your Chapter 4 folder (`C:\pictures-code\ch04`, or `~/pictures-code/ch04` on Mac/Linux).
Open your text editor. Make a new file. Type this program **exactly**:

```cpp
#include <iostream>

int main() {
    std::cout << "Hello!\n";
    std::cout << "I am going to make pictures with C++.\n";
    return 0;
}
```

Save the file as **`hello.cpp`** in the `ch04` folder.

### Compile it

In the terminal (in the `ch04` folder), type:

```
g++ -std=c++17 -Wall -O2 hello.cpp -o hello.exe
```

If you typed everything correctly, the compiler prints **nothing** and a new prompt appears.
"Nothing" is good news! It means: no errors, no warnings.
Type `ls`. You will see a new file: `hello.exe`.

### Run it

**Windows (PowerShell):**

```
.\hello.exe
```

**Mac / Linux:**

```
./hello.exe
```

📖 **New word: `.\` or `./`** — "in this folder". The terminal does not look for programs in the current folder unless you say so. `.\hello.exe` means "run the program `hello.exe` that is **here**."

### Result

```
Hello!
I am going to make pictures with C++.
```

🎉 **Congratulations!** You wrote, compiled and ran a C++ program.

---

## 4. Code explained, line by line

Here is the program again, with line numbers:

```
1  #include <iostream>
2
3  int main() {
4      std::cout << "Hello!\n";
5      std::cout << "I am going to make pictures with C++.\n";
6      return 0;
7  }
```

### Line 1: `#include <iostream>`

- `#include` means: "**copy in** a set of ready tools here."
- `<iostream>` is the name of the set. Its name means **i**nput / **o**utput **stream**.
  - **Input** = information coming **in** to the program (like from the keyboard).
  - **Output** = information going **out** of the program (like text on the screen).
  - **Stream** = a flow of characters, one after another, like water in a river.
- We need `<iostream>` because it gives us `std::cout`, the tool that prints text.
- This line is part of the **standard library**. It comes with every C++ compiler. It is **not** an extra package.
- Lines starting with `#` do **not** end with `;`.

### Line 2: (empty)

- An empty line. The computer ignores it. It is only there to make the code easier for **people** to read.

### Line 3: `int main() {`

This line has four parts:

| Part | Meaning |
|---|---|
| `int` | This function gives back a whole number when it finishes. (`int` is short for **int**eger, a whole number like 0, 1, 42, or −5.) |
| `main` | The name of the function. `main` is special: **every** C++ program starts here. |
| `()` | Round brackets. A function can receive information inside them. `main` receives nothing, so they are empty. |
| `{` | An opening curly brace. It means: "the instructions of `main` start here." |

📖 **New word: function** — a named group of instructions. You can think of `main` as a box with the name "main" on it. Inside the box are the steps of the program.

### Line 4: `std::cout << "Hello!\n";`

This is our first **statement**. It prints `Hello!` and moves to a new line. Let us take it apart:

| Part | Meaning |
|---|---|
| (4 spaces) | Indentation. It shows that this line is **inside** `main`. The computer does not need it, but people do. |
| `std::` | "From the **st**an**d**ard library." `std` is the family name of all standard tools. `::` means "the one inside". So `std::cout` means "the `cout` that belongs to `std`." |
| `cout` | "**c**haracter **out**put". This is the screen (the terminal window). Say it "see-out". |
| `<<` | "Send to". It pushes the text on the right **into** `cout`. Think of it as an arrow pointing to the left: the text flows into the screen. |
| `"Hello!\n"` | The text to print. The double quotes `"` show where the text starts and ends. The quotes themselves are **not** printed. |
| `\n` | A special code that means "**n**ew line". It is two characters when you type it, but it is **one** invisible character inside the program. It moves the cursor to the start of the next line. |
| `;` | The end of the statement. Like a full stop at the end of a sentence. **Every statement needs it.** |

```
    std::cout   <<   "Hello!\n"   ;
    └───┬───┘   └┬┘  └────┬───┘  └┬┘
     the screen  send   the text  end of
                 to               statement
```

### Line 5: `std::cout << "I am going to make pictures with C++.\n";`

- The same idea as line 4. It prints a second sentence, then a new line.
- Because the computer runs statements **in order**, this text comes **after** `Hello!`.

### Line 6: `return 0;`

- `return` means: "**finish** this function and give back a value."
- `0` is the value we give back. For `main`, the value `0` means "**the program finished well, with no problems**." Any other number means "something went wrong."
- Who receives this 0? The terminal (the operating system). It is not printed on the screen.
- It ends with `;` because it is a statement.

💡 **Tip:** In `main` only, C++ lets you leave out `return 0;`. The program then gives back 0 by itself. But we always write it in this book, because it is clear.

### Line 7: `}`

- The closing curly brace. It means: "the instructions of `main` **end** here."
- Every `{` must have a matching `}`.

🧠 **Remember:** `#include` brings in tools. `main` is where the program starts. `{` and `}` hold the statements. Each statement ends with `;`. `std::cout << "text";` prints text.

---

## 5. What does the compiler see? Spaces and lines

The compiler mostly does not care about spaces and new lines between the parts. So this ugly program also works:

```cpp
#include <iostream>
int main(){std::cout<<"Hello!\n";return 0;}
```

But it is **hard to read**. Programmers write code for **people** first and computers second. So we always:

- put each statement on its own line,
- use 4 spaces of indentation inside `{ }`,
- put spaces around `<<`.

⚠️ **Careful:** Spaces **inside** the quotes **do** matter. `"Hello!"` and `"Hel lo!"` print different text.

---

## 6. Our first picture: printing with letters

Before we can save real image files, we need to learn more C++. But we can already make a **picture made of letters** in the terminal. This is called **ASCII art**.

📖 **New word: ASCII art** — a picture made from letters and symbols, like `#`, `.`, `*`. (ASCII is a list of letters and symbols that computers use. We meet it again in Chapter 20.)

Remember from Chapter 1: a picture is a **grid**. Each position has one "colour". Here, `#` is one colour and `.` is another.

Make a new file **`house.cpp`**:

```cpp
#include <iostream>

int main() {
    std::cout << "....#....\n";
    std::cout << "...###...\n";
    std::cout << "..#####..\n";
    std::cout << ".#######.\n";
    std::cout << "..#...#..\n";
    std::cout << "..#.#.#..\n";
    std::cout << "..#####..\n";
    return 0;
}
```

Compile and run it:

```
g++ -std=c++17 -Wall -O2 house.cpp -o house.exe
.\house.exe
```

**Result:**

```
....#....
...###...
..#####..
.#######.
..#...#..
..#.#.#..
..#####..
```

A house! 🏠 Each line of text is one **row** of the picture. Each character is one "pixel". The picture is 9 pixels wide and 7 pixels tall.

**Code explained:**

| Line(s) | What it does |
|---|---|
| 1 | Brings in `std::cout`. |
| 3 | The program starts. |
| 4 | Prints row 0 (the top of the roof, one `#` in the middle) and a new line. |
| 5–7 | Print rows 1–3. Each row has 2 more `#` than the row above, so the roof gets wider. |
| 8–10 | Print rows 4–6: the walls (`#` at the sides), a door (`#` in the middle of row 5) and the floor. |
| 11 | The program finishes well. |
| 12 | The end of `main`. |

🧠 **Remember:** A real image file works the same way: rows of pixels, from top to bottom. The only difference is that each pixel will hold a **colour number** instead of a letter.

---

## 7. Reading error messages

Everyone makes mistakes. The compiler helps you find them. Let us make a mistake **on purpose**.

Open `hello.cpp`. Remove the `;` at the end of line 4:

```cpp
    std::cout << "Hello!\n"
```

Save and compile again. You will see something like:

```
hello.cpp: In function 'int main()':
hello.cpp:4:28: error: expected ';' before 'std'
    4 |     std::cout << "Hello!\n"
      |                            ^
      |                            ;
    5 |     std::cout << "I am going to make pictures with C++.\n";
      |     ~~~
```

How to read it:

| Part | Meaning |
|---|---|
| `hello.cpp` | The file with the problem. |
| `4` | **Line 4.** |
| `28` | Column 28 (the 28th character on the line). |
| `error:` | It is an error. No `.exe` was made. |
| `expected ';' before 'std'` | "I expected a `;` here, before the next `std`." |
| The `^` mark | Points to the exact place. |
| The `;` under it | g++ even suggests what to add! |

Put the `;` back, save, and compile again. The error is gone.

💡 **Tip:** If you see **many** errors, fix only the **first** one, then compile again. One mistake can make the compiler confused, so it reports more errors that are not real.

💡 **Tip:** Sometimes the compiler reports the error on the line **after** the real mistake. A missing `;` on line 4 is only noticed when the compiler reaches line 5. So always look at the line given **and the line before it**.

---

## 8. Small examples

Make each example in its own file in the `ch04` folder. Compile with
`g++ -std=c++17 -Wall -O2 NAME.cpp -o NAME.exe` and run with `.\NAME.exe` (or `./NAME.exe`).

### Example 04.1 — Print your name

**Goal:** Change the text that is printed.

**Code (`name.cpp`):**

```cpp
#include <iostream>

int main() {
    std::cout << "My name is Sam.\n";
    return 0;
}
```

**Explanation:** The same form as `hello.cpp`. Only the text between the quotes is different. Put your own name instead of Sam.

**Result:**

```
My name is Sam.
```

### Example 04.2 — What happens without `\n`?

**Goal:** See why we need `\n`.

**Code (`no_newline.cpp`):**

```cpp
#include <iostream>

int main() {
    std::cout << "Red";
    std::cout << "Green";
    std::cout << "Blue";
    return 0;
}
```

**Explanation:** There is no `\n`. So the computer never moves to a new line. Each text is printed straight after the one before.

**Result:**

```
RedGreenBlue
```

All three words are joined together on one line. Now add `\n` to each text (`"Red\n"` and so on) and run it again. Each word is on its own line.

### Example 04.3 — Many pieces in one statement

**Goal:** Use `<<` more than once in one statement.

**Code (`chain.cpp`):**

```cpp
#include <iostream>

int main() {
    std::cout << "Red " << "Green " << "Blue" << "\n";
    return 0;
}
```

**Explanation:** You can send many pieces into `cout`, one after another, with many `<<`. They are printed from left to right. Here we send four pieces: `"Red "`, `"Green "`, `"Blue"`, and a new line. The spaces inside the quotes keep the words apart.

**Result:**

```
Red Green Blue
```

### Example 04.4 — Printing numbers

**Goal:** Print numbers and let the computer do maths.

**Code (`numbers.cpp`):**

```cpp
#include <iostream>

int main() {
    std::cout << "Width: " << 9 << "\n";
    std::cout << "Height: " << 7 << "\n";
    std::cout << "Pixels: " << 9 * 7 << "\n";
    return 0;
}
```

**Explanation:**
- Line 4 prints the text `Width: `, then the **number** 9 (no quotes!), then a new line.
- Line 5 prints the height in the same way.
- Line 6 prints `9 * 7`. The `*` sign means "times". The computer works out 9 × 7 = 63 **before** printing. This is the number of pixels in our house picture (9 wide, 7 tall).

**Result:**

```
Width: 9
Height: 7
Pixels: 63
```

⚠️ **Careful:** `"9 * 7"` (with quotes) prints the text `9 * 7`. `9 * 7` (without quotes) prints `63`. Quotes mean "print exactly these characters". No quotes means "work out the value".

### Example 04.5 — A small heart

**Goal:** Draw a different ASCII picture.

**Code (`heart.cpp`):**

```cpp
#include <iostream>

int main() {
    std::cout << ".##...##.\n";
    std::cout << "####.####\n";
    std::cout << "#########\n";
    std::cout << ".#######.\n";
    std::cout << "..#####..\n";
    std::cout << "...###...\n";
    std::cout << "....#....\n";
    return 0;
}
```

**Explanation:** Seven rows, each 9 characters wide. `#` is the heart's colour and `.` is the background. Every row has exactly 9 characters, so the picture is a neat rectangle. If one row had 8 characters, the picture would look broken.

**Result:**

```
.##...##.
####.####
#########
.#######.
..#####..
...###...
....#....
```

### Example 04.6 — A spelling mistake

**Goal:** See the error for a wrong name.

**Code (`typo.cpp`):**

```cpp
#include <iostream>

int main() {
    std::cot << "Hello!\n";
    return 0;
}
```

**Explanation:** We typed `cot` instead of `cout`. There is no tool called `std::cot`.

**Result:** The compiler prints something like:

```
typo.cpp:4:10: error: 'cot' is not a member of 'std'; did you mean 'cout'?
```

It tells you the line (4), the problem (`cot` does not exist in `std`), and even suggests the right word. Fix it to `cout` and compile again.

### Example 04.7 — A missing quote

**Goal:** See the error when a quote is missing.

**Code (`quote.cpp`):**

```cpp
#include <iostream>

int main() {
    std::cout << "Hello!\n;
    return 0;
}
```

**Explanation:** The closing `"` is missing. The compiler cannot see where the text ends.

**Result:** An error such as `missing terminating " character`. Look at line 4, and add the `"` before the `;`.

### Example 04.8 — Forgetting `#include`

**Goal:** See why line 1 is needed.

**Code (`no_include.cpp`):**

```cpp
int main() {
    std::cout << "Hello!\n";
    return 0;
}
```

**Explanation:** Without `#include <iostream>`, the compiler does not know `std::cout`.

**Result:** An error such as `'cout' is not a member of 'std'`, often with a note: `'std::cout' is defined in header '<iostream>'; this is probably fixable by adding '#include <iostream>'`. The compiler tells you the fix!

---

## 9. Common mistakes

⚠️ **Forgetting the `;`** at the end of a statement. → Error `expected ';'`.

⚠️ **Wrong capital letters.** `Std::Cout` or `Main` are wrong. C++ is **case sensitive**: small and capital letters are different. Write `std::cout` and `main`.

📖 **New word: case sensitive** — small letters and capital letters are treated as different letters. `a` and `A` are not the same.

⚠️ **Using the wrong quotes.** Use straight double quotes `"`. Curly quotes `“ ”` (which Word and some websites make) are errors.

⚠️ **Using `/n` instead of `\n`.** The new-line code uses a **backslash** `\`, not a forward slash `/`. `"Hello/n"` prints `Hello/n`.

⚠️ **Forgetting to save** before you compile. The compiler reads the file on the disk, not what is on your screen. If you didn't save, it compiles the old version. (In VS Code, a white dot on the file's tab means "not saved". Press **Ctrl + S**.)

⚠️ **Forgetting to compile** after changing the code. If you change `hello.cpp` but only run `hello.exe`, you run the **old** program. Always compile again first.

⚠️ **Running without `.\`** on Windows. `hello.exe` alone gives "not recognized". Use `.\hello.exe`.

---

## 10. Try it yourself

🏋️ **Practice 1.** Write a program `three_lines.cpp` that prints these three lines:

```
I like red.
I like green.
I like blue.
```

🏋️ **Practice 2.** Write a program `area.cpp` that prints `A picture 16 by 16 has 256 pixels.` — but let the computer work out the 256 using `16 * 16`.

🏋️ **Practice 3.** Draw a 5 × 5 ASCII picture of a **frame** (a square border) with `#` and `.`, like the answer to Practice 4 in Chapter 1.

🏋️ **Practice 4.** Find the **three** mistakes in this program:

```cpp
#include <iostream>

int Main() {
    std::cout << "Pictures!\n"
    return 0;
```

🏋️ **Practice 5.** What does this print? Think first, then run it to check.

```cpp
#include <iostream>

int main() {
    std::cout << "A" << "B\n" << "C";
    std::cout << "D\n";
    return 0;
}
```

---

## 11. Answers

**Answer 1.**

```cpp
#include <iostream>

int main() {
    std::cout << "I like red.\n";
    std::cout << "I like green.\n";
    std::cout << "I like blue.\n";
    return 0;
}
```

**Answer 2.**

```cpp
#include <iostream>

int main() {
    std::cout << "A picture 16 by 16 has " << 16 * 16 << " pixels.\n";
    return 0;
}
```

Look at the spaces: there is a space at the end of `"... has "` and at the start of `" pixels.\n"`. Without them, the number would touch the words.

**Answer 3.**

```cpp
#include <iostream>

int main() {
    std::cout << "#####\n";
    std::cout << "#...#\n";
    std::cout << "#...#\n";
    std::cout << "#...#\n";
    std::cout << "#####\n";
    return 0;
}
```

**Answer 4.**
1. `Main` must be `main` (small m). With `Main`, there is no `main` function, so the program cannot start. (You get an error like `undefined reference to 'main'` or `undefined reference to 'WinMain'`.)
2. Line 4 is missing `;` at the end.
3. The closing `}` of the function is missing at the end.

**Answer 5.**

```
AB
CD
```

Step by step: the first statement prints `A`, then `B` and a new line, then `C`. The cursor is now after `C`. The second statement prints `D` straight after `C`, then a new line.

---

## Summary

🧠 The three steps: **write** (`.cpp`) → **compile** (`g++ ...`) → **run** (`.\name.exe`).

🧠 `#include <iostream>` brings in `std::cout`.

🧠 Every program starts in `int main() { ... }` and runs statements from top to bottom.

🧠 `std::cout << "text";` prints text. `\n` starts a new line. `<<` can be used many times in a row.

🧠 Each statement ends with `;`. Every `{` needs a `}`. C++ is case sensitive.

🧠 Error messages tell you the **file**, the **line**, and the **problem**. Fix the first error first.

🧠 A picture is rows of "pixels" from top to bottom. We drew our first pictures with letters.

---

## What comes next

In Part 1 we learn the C++ we need for pictures, one small piece at a time. We start with more about output, statements, and **comments** — notes in the code that the computer ignores but people love.

➡️ Next: [Chapter 05 — Output, Statements and Comments](../part-01-cpp-from-zero/ch05-output-statements-comments.md)
