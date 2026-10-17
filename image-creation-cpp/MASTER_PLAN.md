# Master Plan — Image Creation From Scratch in C++

This file holds the **rules** for writing the tutorial.
Every chapter must follow these rules. Read this file before you write a new chapter.

---

## 1. Goal (from the request in `image/text.md`)

1. Teach how to **create images from scratch**.
2. Use **C++ only**. **No extra packages or libraries.** Only the C++ standard library
   (`<iostream>`, `<fstream>`, `<vector>`, `<string>`, `<cmath>`, `<cstdint>`, …).
   We write every image file format **by hand, byte by byte**.
3. Explain the **theory and mathematics** in detail.
4. Be **very beginner friendly**. The reader may never have written code.
5. About **800 pages** in total.
6. Give **many small examples**.
7. Keep **everything in order**. A chapter only uses ideas from earlier chapters.
8. Explain **every bit of code**, line by line.
9. Use **very simple English**. A 10-year-old should be able to follow it.
   Many readers are not fluent in English.
10. Keep everything in its **own folder**: `image-creation-cpp/`.

---

## 2. Page budget

- We count **1 page ≈ 300 words** (this includes code and tables).
- There are **90 chapters** plus 5 appendices.
- Each chapter is about **8–10 pages**, which is **2,400–3,000 words**.
- 90 × 9 pages = about 810 pages, plus the appendices.

---

## 3. Writing rules (simple English)

| Rule | Example |
|---|---|
| Short sentences. One idea per sentence. | "A pixel is a tiny square. It has one colour." |
| Explain every new word **the first time** it is used. | 📖 **New word: compiler** — a program that turns your code into a program the computer can run. |
| No idioms or slang. | Not "a piece of cake". Say "easy". |
| Use "you" and "we". | "Now we draw a line." |
| Use the same word for the same thing every time. | Always say "pixel", never "dot" in one place and "point" in another. |
| Show the maths **step by step**, with real numbers. | "x = 3, y = 2, width = 5 → index = 2 × 5 + 3 = 13." |
| Use pictures made from text (ASCII art) where it helps. | Grids, arrows, number lines. |
| Repeat important ideas. Remind the reader of earlier chapters. | "Remember from Chapter 22: index = y × width + x." |

### Signs used in every chapter

| Sign | Meaning |
|---|---|
| 📖 **New word** | A new word, explained simply. |
| 💡 **Tip** | A helpful idea. |
| ⚠️ **Careful** | A common mistake. |
| 🧠 **Remember** | The most important thing in the section. |
| 🏋️ **Practice** | A small task for the reader. |
| 🔢 **Maths** | A maths explanation, worked step by step. |

---

## 4. Code rules

1. Use **standard C++17**. Compile with `g++ -std=c++17 -Wall file.cpp -o file.exe`.
2. **No libraries** outside the C++ standard library. No `stb_image`, no OpenCV, no SDL.
3. Every complete program is also saved in `code/chNN/` with the same name as in the chapter,
   so the reader can compare it with their own typing.
4. Every program is **small**. A new idea gets its own small program first.
5. Use clear, long names: `width`, `height`, `red`, not `w`, `h`, `r`
   (except loop counters `x`, `y`, `i`, which we explain).
6. **Every line of code is explained.** Use the "Code explained, line by line" section.
   Explain *what* the line does and *why* we need it.
7. After each program, show **what the output looks like** (text output, or an ASCII picture
   of the image, or a description of the image).

---

## 5. Chapter template (fixed order)

Every chapter has these sections **in this order**:

```
# Chapter NN — Title

> Part X — Part name · Chapter NN of 90 · about N pages

## What you will learn            (3–6 bullet points)
## Words you need                 (table: word | simple meaning)
## 1. The big idea                (a story or picture from daily life)
## 2. ... (theory sections)       (theory and maths, step by step)
## N. The code                    (one complete program)
## N+1. Code explained, line by line
## N+2. Small examples            (Example NN.1, NN.2, ... at least 5)
       Each example: Goal → Code → Explanation → Result
## N+3. Common mistakes           (⚠️ list)
## N+4. Try it yourself           (🏋️ exercises, at least 4)
## N+5. Answers                   (answers to every exercise)
## Summary                        (🧠 bullets)
## What comes next                (one or two sentences + link)
```

---

## 6. Folder layout

```
image-creation-cpp/
  README.md            ← welcome + full table of contents
  MASTER_PLAN.md       ← this file (rules)
  PROGRESS.md          ← what is done, what is next
  part-00-getting-ready/
  part-01-cpp-from-zero/
  part-02-what-is-an-image/
  ... (one folder per part, see README)
  appendices/
  code/
    ch04/hello.cpp
    ch24/red_image.cpp
    ...
```

Chapter file names: `chNN-short-name.md` (for example `ch04-your-first-program.md`).
The exact names are fixed in `README.md`. Earlier chapters link to later chapters
using these names, so **do not rename** them.

---

## 7. Order of ideas (why the parts are in this order)

1. **Part 0–1**: set up the tools and learn just enough C++.
2. **Part 2**: understand what an image *is* (pixels, colour, bytes) before writing one.
3. **Part 3**: write real image files (PPM, then BMP so Windows can open them).
4. **Part 4**: put the image code in a reusable `Image` class.
5. **Part 5–7**: colour maths, then shapes, then smooth edges.
6. **Part 8–10**: geometry, curves, patterns, randomness and fractals.
7. **Part 11–12**: change existing images (filters) and draw text.
8. **Part 13**: 3D pictures (projection, z-buffer, ray tracing).
9. **Part 14**: projects that bring everything together.
