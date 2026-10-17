# Master Plan — Image Creation From Scratch in C++

This file holds the **rules** for writing this book.
Read it before writing any new chapter. Every chapter must follow it.

---

## 1. The request (from `image/text.md`)

| # | Request | What it means for this book |
|---|---|---|
| 1 | Image creation from scratch | We make image files ourselves, byte by byte. |
| 2 | C++, no additional package | Only the C++ standard library: `<fstream>`, `<vector>`, `<cstdint>`, `<cmath>`, `<string>`, `<array>`, `<algorithm>`, `<random>` is **not** used (we write our own random numbers). No `stb_image`, no `libpng`, no `zlib`, no OpenCV, no SDL. |
| 3 | Already knows basic C++ | **Never teach** variables, `if`, loops, functions, `std::vector`, `struct`/`class`, references, headers. We *use* them freely. We **do** explain C++ features that matter for images and are often unknown to beginners: binary file mode, `uint8_t`, bit shifts, bit masks, endianness, `reinterpret_cast`, integer overflow, float-to-int rounding. |
| 4 | Theory and mathematics, descriptively | Every algorithm starts with the idea, then the maths step by step with real numbers, then the code. |
| 5 | Very beginner friendly | Beginner in **graphics and maths**, not in C++. School maths is enough; everything above that is taught. |
| 6 | Very descriptive, about 800 pages | 1 page ≈ 300 words. 82 chapters × ~10 pages + appendices ≈ 830 pages. |
| 7 | Small examples | Every section has at least one tiny example (a 3×2 image, a 4-pixel line, one colour). |
| 8 | Everything in order | A chapter only uses ideas from earlier chapters. No forward references except "we will see this in Chapter N". |
| 9 | Every bit of code explained | Every code block is followed by a line-by-line table. No line is skipped. |
| 10 | Simple English, a 10-year-old can follow | Short sentences. One idea per sentence. No idioms. |
| 11 | Separate folder inside `image/` | Everything lives in `image/image-creation-cpp/`. |

---

## 2. Page budget

- 1 page ≈ 300 words (code and tables count).
- Each chapter: **2,700–3,300 words** (about 9–11 pages).
- Parts and chapters are listed in `README.md`. Do not change the order without updating README and PROGRESS.

---

## 3. Writing rules (simple English)

| Rule | Good example |
|---|---|
| Short sentences. One idea each. | "A pixel is one small square. It has one colour." |
| Explain a new word the first time. | 📖 **New word: resolution** — how many pixels an image has, across and down. |
| No idioms, no slang, no jokes that need culture. | Not "a piece of cake". Say "easy". |
| Use "we" and "you". | "Now we draw a line." |
| One name for one thing, always. | Always "pixel". Never "dot" in one place and "point" in another. |
| Maths step by step with real numbers. | "x = 3, y = 2, width = 5 → index = 2 × 5 + 3 = 13." |
| Draw pictures with text (ASCII) where it helps. | Grids, number lines, arrows. |
| Remind the reader of earlier chapters. | "Remember from Chapter 6: index = y × width + x." |
| Do not explain basic C++. | Write `for (int x = 0; x < w; ++x)` and explain *why* we go across x, not what `for` is. |

### Signs used in every chapter

| Sign | Meaning |
|---|---|
| 📖 **New word** | A new word, explained simply. |
| 🔢 **Maths** | A maths idea, worked step by step. |
| 💡 **Tip** | A helpful idea. |
| ⚠️ **Careful** | A common mistake. |
| 🧠 **Remember** | The most important idea of the section. |
| 🏋️ **Practice** | A small task. Answers are at the end of the chapter. |

---

## 4. Chapter template (every chapter, in this order)

```
# Chapter N — Title

> **Part X · Chapter N of 82**
> **You need:** Chapters … · **You will make:** <file name(s)>

## What you will learn            (3–6 bullet points)
## New words in this chapter      (table: word | simple meaning)
## N.1 … N.k  Theory sections     (idea → picture → 🔢 maths with numbers → small example)
## Code                           (full program, then line-by-line table)
## Small examples                 (at least 3, each tiny, each explained)
## Common mistakes                (⚠️ list)
## Practice                       (🏋️ 4–8 tasks)
## Answers                        (full answers, explained)
## Summary                        (🧠 5–8 short points)
## Next chapter                   (one or two sentences)
```

### Code explanation table format

Every code block is followed by:

```
| Line | Code | What it does, in simple words |
|---|---|---|
| 1 | `#include <fstream>` | Lets us write files. |
```

Long programs may be explained in groups of lines, but **every line must be covered**.

---

## 5. Code rules

1. Standard C++17. Must compile with `g++ -std=c++17 -Wall -Wextra file.cpp`.
2. Only standard headers. No third-party code at all.
3. Image files are written by our own code. We view them with any normal image viewer.
4. Use fixed-size integer types for bytes: `std::uint8_t`, `std::uint16_t`, `std::uint32_t`.
5. Always open image files with `std::ios::binary` (except text formats like P3, where we explain why).
6. Coordinate system: **(0, 0) is the top-left pixel**, x goes right, y goes down. Say this again whenever it matters.
7. Pixel index: `index = y * width + x`. Byte index for RGB: `(y * width + x) * 3`.
8. The shared code we build grows chapter by chapter in `code/`. Each chapter's programs live in `code/chNN/`.
9. Keep programs small. A new idea gets a new small program first, then it joins the library.

---

## 6. Folder layout

```
image/image-creation-cpp/
  README.md                 table of contents (all 82 chapters)
  MASTER_PLAN.md            these rules
  PROGRESS.md               what is done, what is next
  part-01-what-is-an-image/
    ch01-how-to-use-this-book.md
    ...
  part-02-first-image-files/
  ...
  appendices/
  code/
    ch08/ppm_p3_first.cpp
    ...
```

---

## 7. Quality checklist (before marking a chapter done)

- [ ] 2,700+ words.
- [ ] No basic C++ teaching.
- [ ] Every new word explained once, in the "New words" table and in the text.
- [ ] Every maths step shown with real numbers.
- [ ] Every code line explained.
- [ ] At least 3 small examples.
- [ ] Practice with full answers.
- [ ] Only uses ideas from earlier chapters.
- [ ] Code also saved in `code/chNN/`.
- [ ] PROGRESS.md updated.
