# Chapter 01 — How to Use This Book

> Part 0 — Getting Ready · Chapter 01 of 90 · about 8 pages

---

## What you will learn

- What this book will teach you.
- What "making an image from scratch" means.
- Why we use C++ and **no extra packages**.
- How each chapter is built, so you always know where to look.
- How to read code, maths boxes and pictures in this book.
- How to study well, even if your English is not perfect.

---

## Words you need

| Word | Simple meaning |
|---|---|
| **image** | A picture. A photo, a drawing, or a picture on a screen. |
| **computer program** | A list of instructions that a computer follows, one by one. |
| **code** | The words and symbols we write to make a computer program. |
| **C++** | A language for writing code. We say it "see plus plus". |
| **pixel** | One tiny coloured square. A picture on a screen is made of many pixels. |
| **file** | A thing on your computer that holds information, like a photo or a letter. |
| **package / library** | Code that someone else wrote, that you can add to your program. We will **not** use any. |
| **from scratch** | From the very beginning. You make everything yourself. |

---

## 1. The big idea

Think about a big wall made of small square tiles.
Each tile has **one colour**.
If you stand close to the wall, you only see coloured squares.
If you walk far away, the squares are too small to see one by one.
Now your eyes see a **picture**: maybe a face, a tree, or the sun.

```
Close to the wall:            Far from the wall:

 ■ ■ ■ ■ ■ ■ ■ ■
 ■ ■ □ □ □ □ ■ ■                 a smiling face
 ■ □ ■ □ □ ■ □ ■                 (your eyes join
 ■ □ □ □ □ □ □ ■                  the squares
 ■ □ ■ □ □ ■ □ ■                  together)
 ■ ■ □ ■ ■ □ ■ ■
 ■ ■ ■ ■ ■ ■ ■ ■
```

A picture on a computer screen works **in the same way**.
The screen is a wall of tiny squares.
Each tiny square is called a **pixel**.
Each pixel has **one colour**.

📖 **New word: pixel** — the smallest part of a picture on a computer. It is one tiny square with one colour. The word comes from "picture element".

So, to make a picture with a computer, we only need to answer two questions:

1. **How many pixels** does the picture have? (How wide? How tall?)
2. **What colour** is each pixel?

That is it. Every picture you have ever seen on a computer — a photo of your family, a cartoon, a video game — is just **a grid of pixels**, and **one colour for each pixel**.

In this book, **you** will write the code that decides the colour of every pixel.
Then **you** will write the code that saves those colours into an image file.
Then you can open the file and see your picture.

🧠 **Remember:** A computer picture is a grid of tiny squares called pixels. Each pixel has one colour.

---

## 2. What does "from scratch" mean here?

Many people make pictures with code by using a **library**.

📖 **New word: library** — a big box of code that another person already wrote. You can use it in your program. It saves time, but it hides how things work.

For example, a library can give you one command like `draw_circle()` or `save_png()`.
You call it, and the circle appears. But you do **not learn how** the circle was drawn.

In this book we do it differently:

| With a library | In this book (from scratch) |
|---|---|
| `save_png("photo.png")` — done, but you don't know how. | We learn what is inside an image file, byte by byte, and write it ourselves. |
| `draw_circle(...)` — done. | We learn the maths of a circle, and decide for every pixel: "is it inside the circle?" |
| `blur(...)` — done. | We learn how blur works: each pixel becomes the average of its neighbours. |

We **only** use the parts that come with C++ itself.
This is called the **C++ standard library**.

📖 **New word: standard library** — tools that come **inside** every C++ installation. Every C++ compiler has them. You do not need to download them. Examples: printing text, saving files, doing maths like square roots.

So "no extra packages" means:

- ✅ We **may** use tools that come with C++ (`<iostream>`, `<fstream>`, `<vector>`, `<cmath>`, `<string>`).
- ❌ We **do not** download or install any other code library.

💡 **Tip:** When you understand how things work from scratch, you will find libraries easy later. You will know what they do inside.

---

## 3. Why C++?

There are many programming languages. Why do we use C++?

1. **C++ is fast.** A picture can have millions of pixels. C++ can work on all of them very quickly.
2. **C++ lets you touch every byte.** An image file is a list of numbers (bytes). C++ lets us write each byte exactly how we want.
3. **C++ is used for real graphics.** Video games, photo editors, and film effects are often written in C++.
4. **C++ is free.** You can install it on Windows, Mac and Linux at no cost.

⚠️ **Careful:** C++ has a reputation for being hard. That is because it has **many** features. But we only learn the features we **need** for pictures. We learn them slowly, one at a time. You can do it.

---

## 4. The journey through this book

The book has 15 parts. Each part builds on the part before it.
Here is the journey, like a map:

```
 Part 0  Getting ready        → install tools, run your first program
   │
 Part 1  C++ from zero        → learn just enough C++
   │
 Part 2  What is an image?    → pixels, colours, numbers, bytes
   │
 Part 3  First image files    → save real pictures (PPM and BMP files)
   │
 Part 4  Image toolkit        → reusable code for every later chapter
   │
 Part 5  Colour maths         → mixing colours, gradients
   │
 Part 6  Drawing shapes       → lines, circles, triangles
   │
 Part 7  Smooth edges         → no more "stairs" on edges, see-through colours
   │
 Part 8  Geometry             → turn, move and grow shapes
   │
 Part 9  Curves               → smooth curved lines
   │
 Part 10 Patterns & fractals  → randomness, clouds, the Mandelbrot set
   │
 Part 11 Changing images      → blur, sharpen, resize photos
   │
 Part 12 Text                 → letters made of pixels
   │
 Part 13 3D pictures          → cubes, light, shadows, ray tracing
   │
 Part 14 Projects             → put everything together
```

🧠 **Remember:** Read in order. Chapter 45 (circles) uses ideas from Chapter 35 (distance), which uses ideas from Chapter 7 (maths in C++). If you skip, you may get lost.

---

## 5. How every chapter is built

Every chapter in this book has **the same parts, in the same order**.
When you know the order, you always know where to look.

| Part of the chapter | What it gives you |
|---|---|
| **What you will learn** | A short list of goals. |
| **Words you need** | A table of new words with simple meanings. Read it first! |
| **1. The big idea** | A story or a picture from daily life, to understand the idea. |
| **Theory sections** | The idea in detail, with maths shown step by step. |
| **The code** | One complete program. |
| **Code explained, line by line** | What **every** line of the program does, and why. |
| **Small examples** | Many small programs, each with a goal, the code, an explanation and the result. |
| **Common mistakes** | Mistakes that many beginners make, and how to fix them. |
| **Try it yourself** | Small tasks for you. |
| **Answers** | Answers to every task. Try first, then look! |
| **Summary** | The most important points, in a short list. |
| **What comes next** | A link to the next chapter. |

---

## 6. How to read code in this book

Code is always shown in a grey box like this:

```cpp
#include <iostream>

int main() {
    std::cout << "Hello!\n";
    return 0;
}
```

Do not worry if you don't understand this code yet. Chapter 4 explains every line.

Some important things about code boxes:

1. **Type it exactly.** In C++, small things matter. A missing `;` (semicolon) is an error. A capital letter in the wrong place is an error. `Main` and `main` are **different** words to the computer.
2. **Spaces at the start of a line** (we call this **indentation**) are only to help **people** read the code. The computer does not need them. But please use them. They make code much easier to read.
3. **Line numbers.** When we explain code, we say "line 3" and so on. Count lines from the top of the box. Line 1 is the first line. Empty lines count too.

📖 **New word: indentation** — spaces at the start of a line. It shows which lines are "inside" other lines, like steps inside a bigger step.

When we explain code line by line, it looks like this:

| Line | Code | What it does |
|---|---|---|
| 1 | `#include <iostream>` | Lets us print text on the screen. |
| 3 | `int main() {` | The program starts here. |
| 4 | `std::cout << "Hello!\n";` | Prints the word Hello! |
| 5 | `return 0;` | Says "the program finished well". |
| 6 | `}` | The end of `main`. |

---

## 7. How to read maths in this book

Pictures need maths. But **don't be afraid**. We always:

1. Explain the idea in words first.
2. Show a small picture if it helps.
3. Do the maths with **real, small numbers**, step by step.
4. Only then show the general formula.

Maths boxes look like this:

> 🔢 **Maths: Where is the middle of a line?**
>
> A line goes from 2 to 8 on a number line.
>
> ```
> 0   1   2   3   4   5   6   7   8   9
>         A-----------------------B
>                     ↑
>                   middle
> ```
>
> Step 1: Add the two ends: 2 + 8 = 10.
> Step 2: Divide by 2: 10 ÷ 2 = 5.
> So the middle is at **5**.
>
> General formula: middle = (start + end) ÷ 2

In C++ we write "times" as `*` and "divide" as `/`.
So the formula above in C++ is `middle = (start + end) / 2;`.

| Maths sign | Meaning | In C++ |
|---|---|---|
| + | add | `+` |
| − | subtract (take away) | `-` |
| × | multiply (times) | `*` |
| ÷ | divide | `/` |
| = | is the same as | `==` (to check), `=` (to store a value) |
| √ | square root | `std::sqrt(...)` |
| x² | x times x | `x * x` |

You will learn all of these slowly, in Chapter 7 and later.

---

## 8. How to study well

Here are good habits. They work for children and adults.

1. **Short sessions.** 30 to 60 minutes is good. Your brain needs rest.
2. **Type, don't copy.** When you type code with your own fingers, you remember it.
3. **Change things.** After a program works, change a number. Run it again. What changed? This is the fastest way to learn.
4. **Make mistakes on purpose.** Remove a `;` and see the error message. Then you will know that error later.
5. **Say it in your own words.** After each chapter, explain the big idea to a friend, or to yourself, in your own language.
6. **Use a notebook.** Write new words and their meanings. Draw the grids and pictures.
7. **Look at the result.** In this book, the result is a picture. Open it. Look at it carefully. Is it what you expected?

💡 **Tip for readers whose English is not strong:** Every new word is in the "Words you need" table at the start of the chapter. All words are also collected in [Appendix C — Glossary](../appendices/c-glossary.md). You can translate these words into your own language and write them in your notebook.

---

## 9. What you need

| Thing | Do you need it? | Why |
|---|---|---|
| A computer (Windows, Mac or Linux) | ✅ Yes | To write and run code. |
| Internet | Only once | To download the free C++ compiler (Chapter 3). |
| Money | ❌ No | Everything in this book is free. |
| Maths knowledge | Only + − × ÷ | We teach all other maths in the book. |
| Coding knowledge | ❌ No | We start from zero. |
| A notebook and pen | 💡 Helpful | To write new words and draw grids. |

---

## 10. Small examples

In this first chapter there is no code to run yet. So the small examples are about **thinking like a picture maker**. This is the most important skill in the whole book.

### Example 01.1 — A 3 × 3 picture

**Goal:** Describe a tiny picture using only words and numbers.

**The picture:**

```
 ■ □ ■
 □ ■ □
 ■ □ ■
```

**Explanation:** This picture is 3 pixels wide and 3 pixels tall.
There are 3 × 3 = **9 pixels** in total.
■ means black. □ means white.
We can describe it row by row, from the top:

- Row 1: black, white, black
- Row 2: white, black, white
- Row 3: black, white, black

**Result:** We have described a whole picture using only words. A computer stores pictures in the same way, but it uses numbers instead of the words "black" and "white".

### Example 01.2 — Counting pixels

**Goal:** Find how many pixels a picture has.

**Explanation:** Number of pixels = width × height.

| Picture | Width | Height | Pixels |
|---|---|---|---|
| Tiny icon | 16 | 16 | 16 × 16 = 256 |
| Small picture | 100 | 50 | 100 × 50 = 5,000 |
| Phone photo | 4000 | 3000 | 4000 × 3000 = 12,000,000 |

**Result:** A phone photo has **12 million pixels**. That is why we need a fast language like C++. Our program must decide the colour of every single one.

### Example 01.3 — A rule instead of a list

**Goal:** Describe a picture with a **rule**, not a list.

**The picture (5 wide, 5 tall):**

```
 ■ ■ ■ ■ ■
 □ □ □ □ □
 ■ ■ ■ ■ ■
 □ □ □ □ □
 ■ ■ ■ ■ ■
```

**Explanation:** Number the rows 0, 1, 2, 3, 4 from the top. (Computers often start counting at 0. We explain why in Chapter 11.)
Rows 0, 2 and 4 are black. Rows 1 and 3 are white.
So the rule is: **"if the row number is even, the pixel is black; if it is odd, the pixel is white."**

**Result:** With one short rule, we can make a picture of **any** size — 5 rows or 5,000 rows. Most pictures in this book are made with rules like this. The rule is our code.

### Example 01.4 — A rule with columns

**Goal:** Change the rule to use columns.

**Explanation:** Number the columns 0, 1, 2, 3, 4 from the left.
Rule: **"if the column number is even, black; if it is odd, white."**

**Result:**

```
 ■ □ ■ □ ■
 ■ □ ■ □ ■
 ■ □ ■ □ ■
 ■ □ ■ □ ■
 ■ □ ■ □ ■
```

The stripes now go up and down, not left to right. One small change in the rule gives a very different picture.

### Example 01.5 — A rule with rows and columns together

**Goal:** Use the row and the column together.

**Explanation:** Rule: **"add the row number and the column number. If the answer is even, black. If it is odd, white."**

Let us test some pixels:

| Row | Column | Row + Column | Even or odd? | Colour |
|---|---|---|---|---|
| 0 | 0 | 0 | even | black |
| 0 | 1 | 1 | odd | white |
| 1 | 0 | 1 | odd | white |
| 1 | 1 | 2 | even | black |
| 2 | 3 | 5 | odd | white |

**Result:**

```
 ■ □ ■ □ ■
 □ ■ □ ■ □
 ■ □ ■ □ ■
 □ ■ □ ■ □
 ■ □ ■ □ ■
```

This is a **checkerboard** (like a chess board). In Chapter 63 we make big colourful checkerboards with exactly this rule.

### Example 01.6 — A rule for a shape

**Goal:** Make a shape with a rule.

**Explanation:** Rule for a 5 × 5 picture: **"if the row number and the column number are the same, black. Otherwise, white."**

**Result:**

```
 ■ □ □ □ □      row 0, column 0 → same → black
 □ ■ □ □ □      row 1, column 1 → same → black
 □ □ ■ □ □      row 2, column 2 → same → black
 □ □ □ ■ □      ...
 □ □ □ □ ■
```

We drew a **diagonal line**. In Part 6 we draw lines at **any** angle, using better rules.

---

## 11. Common mistakes

⚠️ **Skipping chapters.** Each chapter uses the ones before. If a chapter feels hard, go back one chapter.

⚠️ **Only reading, not typing.** Reading code is not enough. You learn by typing, running, and changing it.

⚠️ **Giving up at the first error.** Errors are normal. Every programmer sees errors every day. Appendix D helps you fix the common ones.

⚠️ **Being afraid of maths.** We show every step with small numbers. Take your time. Use paper.

⚠️ **Copying from the `code/` folder without trying first.** The folder is for **checking**, not for skipping the typing.

---

## 12. Try it yourself

🏋️ **Practice 1.** A picture is 20 pixels wide and 10 pixels tall. How many pixels does it have?

🏋️ **Practice 2.** Draw a 4 × 4 picture on paper with this rule: "if the row number is 0 or 3, black; otherwise, white." Count rows from 0.

🏋️ **Practice 3.** Draw a 4 × 4 picture with this rule: "if the column number is bigger than the row number, black; otherwise, white."

🏋️ **Practice 4.** Look at this picture. Write a rule for it.

```
 ■ ■ ■ ■
 ■ □ □ ■
 ■ □ □ ■
 ■ ■ ■ ■
```

🏋️ **Practice 5.** In your own words (in any language), explain what "from scratch" means in this book.

---

## 13. Answers

**Answer 1.** 20 × 10 = **200 pixels**.

**Answer 2.**

```
 ■ ■ ■ ■     row 0 → black
 □ □ □ □     row 1 → white
 □ □ □ □     row 2 → white
 ■ ■ ■ ■     row 3 → black
```

**Answer 3.** Check each pixel: is the column bigger than the row?

```
 □ ■ ■ ■     row 0: columns 1, 2, 3 are bigger than 0
 □ □ ■ ■     row 1: columns 2, 3 are bigger than 1
 □ □ □ ■     row 2: column 3 is bigger than 2
 □ □ □ □     row 3: no column is bigger than 3
```

This is a triangle!

**Answer 4.** One good rule: "if the row is 0 or 3, **or** the column is 0 or 3, black; otherwise, white."
This is a **frame** (a border). Rows 0 and 3 are the top and bottom edges. Columns 0 and 3 are the left and right edges.

**Answer 5.** Example answer: "From scratch means we do not use other people's code libraries. We write all the code ourselves, using only what comes with C++. So we understand how pictures and image files really work."

---

## Summary

🧠 A computer picture is a **grid of pixels**. Each pixel has **one colour**.

🧠 To make a picture, we decide **the size** and **the colour of every pixel**.

🧠 We often use a **rule** (code) to decide the colours, not a long list.

🧠 "From scratch" means **no extra libraries**. We use only the C++ standard library.

🧠 Every chapter has the same parts in the same order. Read in order. Type every program.

---

## What comes next

Before we write code, we need to know a few things about computers: what a **file** is, what a **folder** is, and how to use the **terminal** to give the computer commands.

➡️ Next: [Chapter 02 — Computers, Files, Folders and the Terminal](ch02-computers-files-terminal.md)
