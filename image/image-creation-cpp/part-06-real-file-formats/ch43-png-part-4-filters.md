# Chapter 43 — PNG, Part 4: Filters

> **Part 6 · Chapter 43 of 82**
> **You need:** Chapters 1–42 (especially 4, 13, 39, 41 and 42) · **You will make:** `pngfilter.h` (the five PNG filters, their reverse, a rule that picks the best filter for each row, `savePNGFiltered` and `loadPNGFiltered`), and five filtered PNG files: `flag.png`, `sky.png`, `sunset.png`, `blend.png` and `noise.png`

---

## What you will learn

- Why neighbouring pixels are usually **similar**, but not **equal** — and why that matters for compression.
- PNG's five **filters**: None, Sub, Up, Average and Paeth.
- How to **undo** each filter exactly, with no loss at all.
- How "wrap-around" (Chapter 4) turns a negative difference into a byte.
- A simple rule for choosing the best filter for **each row**.
- How to measure what a filter does, even before we have real compression.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **filter** | A rule that replaces each byte by its difference from a guess. |
| **prediction** | The guess: a value worked out from bytes we already know. |
| **residual** | What is left: the real byte minus the prediction. |
| **unfilter** | Undo a filter: add the prediction back. |
| **bpp** | Bytes per pixel: 3 for RGB, 4 for RGBA. |
| **adaptive** | Choosing again for every row, instead of one choice for the whole picture. |
| **heuristic** | A simple rule of thumb that is usually good, but not always the best. |

---

## 43.1 Similar is not equal

In Chapter 39 we packed pictures with **RLE**: "this pixel, 120 times". It worked very well for the flag, whose rows are long runs of one colour. It did nothing for noise.

Now look at the first four pixels of a **sunset** gradient that goes from orange on the left to purple on the right (this chapter's program makes it):

```
   x:      0               1               2               3
        (250, 120, 40)  (249, 120, 40)  (249, 119, 41)  (248, 119, 41)
```

No two pixels are equal, so RLE finds no runs at all. But they are **very similar**: each one is the one before it, plus or minus 1. Most pictures are like this — photos, gradients, shadows, smooth edges. Neighbouring pixels are **close**, not the same.

Here is the trick. Instead of storing each byte, store **how much it differs** from its neighbour on the left:

```
   bytes:        250 120  40   249 120  40   249 119  41   248 119  41
   differences:  250 120  40    -1   0   0     0  -1  +1    -1   0   0
```

The first pixel stays as it is (there is nothing to its left). After that, everything is 0 or ±1. A list of tiny numbers, mostly zeros, is **much** easier to compress than the original list. Chapter 44 will show why: a compressor gives the **common** values **short** codes.

📖 **New word: filter** — a rule that replaces each byte by its difference from a **guess**. PNG has five filters. Each row of the picture says which one it uses: that is the **filter byte** at the start of every row (Chapter 41). So far we always wrote 0, "no filter".

🧠 **Remember:** a filter does **not** make the data smaller. It makes the same amount of data **easier to compress**. Every filter can be undone exactly: PNG stays **lossless**.

---

## 43.2 Prediction and residual

📖 **New words: prediction and residual** — every filter works the same way:

> 1. Make a **prediction**: a guess for the byte, worked out from bytes that are **already known**.
> 2. Store the **residual**: the real byte minus the prediction.

A good prediction gives residuals close to 0. The five filters differ only in **how they guess**:

| filter type | name | prediction |
|---|---|---|
| 0 | None | 0 (so the residual is the byte itself) |
| 1 | Sub | the byte on the **left** |
| 2 | Up | the byte **above** |
| 3 | Average | the average of left and above, rounded down |
| 4 | Paeth | left, above or above-left, whichever is closest to left + above − above-left |

When we read the file, we make the **same** prediction (from bytes we have already rebuilt) and **add** the residual back. That is all.

---

## 43.3 Filters work on bytes

Filters do not look at pixels or colours. They look at **bytes**, one at a time, and compare a byte with the byte **in the same place** in the pixel to its left (red with red, green with green, and so on).

📖 **New word: bpp** — **bytes per pixel**: 3 for RGB, 4 for RGBA. The byte "on the left" is the byte **bpp** places earlier in the row.

For each byte **x**, PNG names three neighbours:

```
        row above:   ...  c  b  ...         c = above-left, b = above
        this row:    ...  a  x  ...         a = left,       x = the byte we are filtering

  ("left" = bpp bytes back, not 1 byte back)
```

For an RGB row whose bytes are numbered 0, 1, 2, …:

```
   byte number:   0  1  2 | 3  4  5 | 6  7  8 | ...
                  R  G  B | R  G  B | R  G  B
   for byte 4 (green of pixel 1): a = byte 1 (green of pixel 0)
```

**Outside the picture** — left of the first pixel, or above the top row — every neighbour counts as **0**. So in the top row, "Up" predicts 0, and in the first pixel of each row, "Sub" predicts 0.

🔢 **Maths: the positions**

> byte i of the row, with bpp = 3:
> a = row[i − 3] (0 if i < 3)
> b = above[i]  (0 for the top row)
> c = above[i − 3] (0 if i < 3, or for the top row)

---

## 43.4 Negative differences and wrap-around

A difference can be negative: 194 − 198 = −4. But a filtered byte is still a **byte**, 0 to 255. PNG solves this with **wrap-around** (Chapter 4, Section 4.9): all filter sums are done **modulo 256**.

🔢 **Maths: mod 256**

> −4 → −4 + 256 = **252**
> −1 → **255**
> 300 → 300 − 256 = **44**

In C++ this happens by itself: converting an `int` to `std::uint8_t` keeps only the lowest 8 bits, which is the same as "mod 256":

```cpp
std::uint8_t r = static_cast<std::uint8_t>(194 - 198);   // 252
```

And going back works too: 198 + 252 = 450 → 450 − 256 = **194** ✓. Wrap-around loses nothing.

💡 It helps to **read** a byte above 127 as a negative number: 255 = −1, 254 = −2, 252 = −4, 128 = −128. (This is how a **signed** byte, `std::int8_t`, stores negative numbers.) So "252" in a filtered row really means "a little smaller than predicted".

---

## 43.5 Sub and Up, with real numbers

Here are two RGB rows of 4 pixels each (12 bytes). The program prints them as its first lines:

```
above:       100 150 200 104 152 196 108 154 192 112 156 188
row:         102 151 198 106 153 194 110 155 190 114 157 186
```

The row is a smooth gradient: red and green go **up** a little, blue goes **down** a little. The row above is very close to it.

### Sub: x − a

🔢 **Maths: Sub on the row**

> pixel 0: nothing on the left, a = 0: 102 − 0 = **102**, 151 − 0 = **151**, 198 − 0 = **198**
> pixel 1: 106 − 102 = **4**, 153 − 151 = **2**, 194 − 198 = −4 → **252**
> pixel 2: 110 − 106 = **4**, 155 − 153 = **2**, 190 − 194 = −4 → **252**
> pixel 3: the same: **4 2 252**

```
     Sub (1) 102 151 198   4   2 252   4   2 252   4   2 252
```

### Up: x − b

🔢 **Maths: Up on the row**

> 102 − 100 = **2**, 151 − 150 = **1**, 198 − 200 = −2 → **254**, and the same for every pixel.

```
      Up (2)   2   1 254   2   1 254   2   1 254   2   1 254
```

Up is even better here: **every** byte is tiny, because the row above is so similar.

---

## 43.6 Average

**Average** predicts the **average of left and above**, rounded **down**: ⌊(a + b) / 2⌋.

🔢 **Maths: Average on the row**

> pixel 0: a = 0, so the prediction is half the byte above:
> (0 + 100) / 2 = 50 → 102 − 50 = **52**; (0 + 150) / 2 = 75 → **76**; (0 + 200) / 2 = 100 → **98**
> pixel 1: (102 + 104) / 2 = 103 → 106 − 103 = **3**
> (151 + 152) / 2 = 151.5 → rounded down **151** → 153 − 151 = **2**
> (198 + 196) / 2 = 197 → 194 − 197 = −3 → **253**

```
 Average (3)  52  76  98   3   2 253   3   2 253   3   2 253
```

⚠️ The sum a + b can be up to 255 + 255 = **510**. It must be computed in an `int`, not in a byte — a byte would wrap at 256 and give the wrong average. In our code, a and b are `int`s, and C++'s integer division `/ 2` rounds down for positive numbers, exactly as PNG wants.

---

## 43.7 Paeth

The cleverest filter is named after **Alan Paeth**, who invented it. It looks at all three neighbours a, b and c.

The idea: imagine the brightness of the picture as a gently sloping surface. If the surface is flat and tilted, then going **right** changes a byte by the same amount in both rows:

```
        c  b         b − c = "how much going right changes things" (in the row above)
        a  x         so x ≈ a + (b − c)
```

So a good first guess is **p = a + b − c**. But p itself is not used. Paeth then picks **whichever of a, b and c is closest to p**:

> p = a + b − c
> pa = |p − a|, pb = |p − b|, pc = |p − c|
> if pa ≤ pb and pa ≤ pc → predict **a**
> else if pb ≤ pc → predict **b**
> else → predict **c**

⚠️ The order of the ties matters: **a first, then b, then c**. Every PNG program must break ties the same way, or the picture would be rebuilt wrongly.

🔢 **Maths: five examples** (the program prints them)

| a | b | c | p = a + b − c | pa, pb, pc | prediction |
|---|---|---|---|---|---|
| 50 | 60 | 70 | 40 | 10, 20, 30 | **a = 50** |
| 100 | 120 | 100 | 120 | 20, 0, 20 | **b = 120** |
| 50 | 150 | 100 | 100 | 50, 50, 0 | **c = 100** |
| 10 | 10 | 10 | 10 | 0, 0, 0 | **a = 10** (a tie: a wins) |
| 200 | 40 | 60 | 180 | 20, 140, 120 | **a = 200** |

Look at the second line: c = a means "nothing changes going down on the left", so Paeth copies **b** (going down changes nothing here either). In the third line, the row above and the left byte disagree, and c sits in the middle.

💡 Why not use p itself? Because p can be wrong by a lot near **edges** (where a colour changes suddenly). Choosing one of the **real** neighbours keeps the prediction sensible.

🔢 **Maths: Paeth on our row**

> pixel 0: a = 0, c = 0, b = 100 → p = 100, pa = 100, pb = 0 → predict b → 102 − 100 = **2** (like Up)
> pixel 1, red: a = 102, b = 104, c = 100 → p = 106; pa = 4, pb = 2, pc = 6 → predict b → **2**

On this row, Paeth chooses b every time, so it gives the **same** bytes as Up:

```
   Paeth (4)   2   1 254   2   1 254   2   1 254   2   1 254
```

📖 **Remember:** in the **top row**, b and c are 0, so p = a and Paeth predicts **a** (it acts like Sub). At the **left edge**, a and c are 0, so p = b and Paeth predicts **b** (like Up).

---

## 43.8 Undoing a filter

📖 **New word: unfilter** — to undo a filter, make the **same prediction** and **add** the residual (mod 256):

> filter:   residual = x − prediction  (mod 256)
> unfilter: x = residual + prediction  (mod 256)

The prediction must use exactly the same a, b and c as when the file was written. These are the **original** bytes, not the residuals. When reading, we rebuild the row **from left to right**, so when we reach byte i, bytes i − 3 (the "a") are already rebuilt. The row above was rebuilt before this row. Everything we need is ready.

🔢 **Maths: unfilter Sub**

> residuals: 102 151 198 4 2 252 …
> byte 0: 102 + 0 = **102**; byte 1: **151**; byte 2: **198**
> byte 3: 4 + 102 = **106**; byte 4: 2 + 151 = **153**; byte 5: 252 + 198 = 450 → 450 − 256 = **194** ✓

⚠️ **The most common bug**: using the **filtered** bytes of the row above (or on the left) as a, b, c. The neighbours are always the **real** pixel bytes. In the encoder, we keep a copy of the **unfiltered** row to be the "above" of the next row.

The program filters the example row with all five filters, unfilters it again, and checks:

```
              score 295, unfilters back to the row
```

---

## 43.9 Choosing a filter for each row

Each row can use a **different** filter. Which one should we choose?

📖 **New word: adaptive** — choosing again **for every row**. The PNG standard recommends it for most pictures.

We cannot know the final compressed size without compressing. So we use a **heuristic**.

📖 **New word: heuristic** — a simple rule of thumb that is usually good, but not always the best.

The rule the PNG standard suggests:

> Try all five filters on the row. Read each residual byte as a **signed** number (−128 … 127). Add up their **sizes** (absolute values). Choose the filter with the **smallest sum**.

We call this sum the **score**. A byte v counts as v if v < 128, and as 256 − v otherwise (so 252 counts as 4, 255 counts as 1).

🔢 **Maths: the scores of our row**

> None: 102 + (256 − 151) + (256 − 198) + 106 + … = **1096**
> Sub: 102 + 105 + 58 + 3 × (4 + 2 + 4) = 265 + 30 = **295**
> Up: 4 × (2 + 1 + 2) = **20**
> Average: 52 + 76 + 98 + 3 × (3 + 2 + 3) = 226 + 24 = **250**
> Paeth: **20**

Up and Paeth tie with 20. Our rule keeps the **first** filter that reaches the smallest score, so it picks **Up**:

```
best filter for this row: Up
```

💡 Why the sum of sizes? Small residuals (close to 0, positive or negative) are what compress well. A sum of sizes is a cheap measure of "how close to 0". Real compressors sometimes try other rules, but this one is simple and good.

⚠️ **Do not** add the bytes as **unsigned** numbers. Then 255 (which means −1, a very good residual) would count as 255 — the worst possible. The signed view is the whole point.

---

## 43.10 Five pictures, measured

The program makes five 300 × 200 pictures:

| picture | what it is |
|---|---|
| **flag** | three flat stripes (Chapter 39) |
| **sky** | a **vertical** gradient: each row one colour (Chapter 39) |
| **sunset** | a **horizontal** gradient: each column one colour |
| **blend** | red grows to the right, green grows downwards, blue grows along the diagonal |
| **noise** | random grey pixels (Chapter 39) |

For each picture and each filter (and "Best", our adaptive rule), it counts the **zero bytes** in the filtered rows and the **average score per byte**. There are 300 × 3 × 200 = 180,000 bytes per picture (not counting the filter bytes).

```
zero bytes, in %             None     Sub      Up Average   Paeth    Best
  flag                         11      99     100      99     100     100
  sky                           0     100      35      48     100     100
  sunset                        0      61     100      90     100     100
  blend                         0      54      50      21      83      83
  noise                         0       0       0       0       0       0
```

What the table says:

- **flag**: Up gives 100 %: every row equals the one above (only the top row has non-zero bytes, and they are rounded away). Sub gives 99 %: only the bytes where a stripe starts are non-zero.
- **sky**: each row is one colour, so **Sub** is nearly all zeros (only the first pixel of each row is not). Up gives only 35 %: the colour changes a little from row to row (`1 1 0 1 1 0 …`), so Up's residuals are small, but not zero.
- **sunset**: the opposite of sky. Each **column** is one colour, so **Up** is perfect.
- **blend**: it changes in **both** directions. Only **Paeth** (83 % zeros) handles that well. (The bytes are not exactly a flat surface, because of the rounding in `x * 255 / 299`.)
- **noise**: no filter helps. Random numbers cannot be predicted — that is what "random" means.

And the average score per byte (smaller is better):

```
average score per byte       None     Sub      Up Average   Paeth    Best
  flag                       35.0     0.5     0.2     1.0     0.0     0.0
  sky                        88.9     0.3     1.0     1.0     0.0     0.0
  sunset                     75.8     0.6     0.4     0.6     0.0     0.0
  blend                      70.6     0.6     0.8     1.1     0.2     0.2
  noise                      64.2    63.9    64.2    64.1    64.1    61.9
```

Without a filter, an average byte is about 70 "steps" from 0. With the best filter, it is 0.2 or less (for every picture except noise). On noise, "Best" is a little better than any single filter, because it picks a different filter for each row:

```
filters chosen by Best (rows):
  flag: None 0 Sub 1 Up 199 Average 0 Paeth 0
  sky: None 0 Sub 1 Up 0 Average 0 Paeth 199
  sunset: None 0 Sub 1 Up 199 Average 0 Paeth 0
  blend: None 0 Sub 1 Up 0 Average 0 Paeth 199
  noise: None 55 Sub 34 Up 43 Average 41 Paeth 27
```

🔢 **Maths: why Sub always wins the top row**

> In the top row, b = c = 0. So Up predicts 0 (= None), Average predicts ⌊a / 2⌋, and Paeth predicts a (= Sub).
> Up gives the same bytes as None, and Paeth the same bytes as Sub. So the top row really has only three choices: None, Sub and Average. For smooth pictures, Sub wins — and because Sub comes before Paeth, a tie goes to Sub.

🔢 **Maths: why Paeth wins the sky**

> In the sky, every row is one colour, so the byte above is equal to the byte above-left: b = c.
> Then p = a + b − c = **a**, and pa = 0: Paeth predicts **a** — and a is exactly x. Residual **0**.
> At the left edge, Paeth predicts b (Section 43.7): residuals like 1 1 0 (the row above is slightly different).
> So each row has at most 3 non-zero bytes. In total only 392 of the 180,000 bytes are not 0 (99.8 %).

Paeth "notices" that the picture changes downwards, but not across — without being told.

---

## 43.11 But the files are not smaller!

The program saves all five pictures with the "Best" filters, and prints their sizes:

```
  sky.png: 180278 bytes (without filters 180278), read back the same, Chapter 42's loadPNG refuses it
```

Exactly the **same size** as without filters. Of course: our zlib still uses **stored** blocks (Chapter 41), which copy every byte as it is. 180,000 zeros take 180,000 bytes, just like 180,000 other numbers.

🔢 **Maths: the size**

> rows: 200 × (1 + 900) = 180,200 bytes → 3 stored blocks → zlib 180,200 + 2 + 3 × 5 + 4 = 180,221
> PNG: 8 + 25 + (12 + 180,221) + 12 = **180,278** bytes — with or without filters

Filters are only half of the job. The other half is a compressor that gives the **common** bytes (here: 0) **short** codes. That is **Huffman coding**, in Chapter 44. There we will compress the filtered sky and see it shrink.

💡 These files are still perfectly good PNGs. Open them in a browser: they look the same as before. Every PNG viewer understands all five filters.

⚠️ Chapter 42's `loadPNG` **refuses** them ("row filters are not supported yet"). That is why this chapter has a new loader, `loadPNGFiltered`.

---

## 43.12 A decoder in three steps

Chapter 42's `decodePNG` did everything in one long function. To add filters, we split the work into three parts — and we keep `pngfile.h` exactly as it was:

```
   decodePNGFiltered(file)
      1. readPngStart(file)        → check chunks and IHDR; join the IDAT data   (like Chapter 42)
      2. zlibUnstore(zdata)        → the filtered rows                           (Chapter 41)
      3. pngPixels(info, rows)     → check the size, UNFILTER, copy the pixels   (new)
```

Step 1 is Chapter 42's checks 1–8, moved into a function of their own. Step 3 is checks 10 and 11, but check 11 changes: instead of refusing any filter byte that is not 0, we now refuse only filter types **above 4** ("unknown filter type 5"), and unfilter the rest.

💡 Why split it? In Chapter 45, step 2 will become a real Deflate decoder. Then we only replace the **middle** line — steps 1 and 3 stay the same.

---

## Code, part 1: `pngfilter.h`

File: `common/pngfilter.h` (new). It includes `pngfile.h`.

```cpp
#ifndef PNGFILTER_H
#define PNGFILTER_H

#include <cstdint>
#include <string>
#include <vector>
#include "pngfile.h"

const int kFilterNone = 0;
const int kFilterSub = 1;
const int kFilterUp = 2;
const int kFilterAverage = 3;
const int kFilterPaeth = 4;
const int kFilterBest = 5;

inline int absInt(int v) {
    return (v < 0) ? -v : v;
}

inline int paethPredictor(int a, int b, int c) {
    const int p = a + b - c;
    const int pa = absInt(p - a);
    const int pb = absInt(p - b);
    const int pc = absInt(p - c);
    if (pa <= pb && pa <= pc) {
        return a;
    }
    if (pb <= pc) {
        return b;
    }
    return c;
}

inline int predictByte(int filter, int a, int b, int c) {
    if (filter == kFilterSub) {
        return a;
    }
    if (filter == kFilterUp) {
        return b;
    }
    if (filter == kFilterAverage) {
        return (a + b) / 2;
    }
    if (filter == kFilterPaeth) {
        return paethPredictor(a, b, c);
    }
    return 0;
}

inline Bytes filterRow(int filter, const Bytes& row, const Bytes& above, int bpp) {
    Bytes out(row.size());
    for (int i = 0; i < static_cast<int>(row.size()); ++i) {
        const int a = (i >= bpp) ? row[i - bpp] : 0;
        const int b = above[i];
        const int c = (i >= bpp) ? above[i - bpp] : 0;
        out[i] = static_cast<std::uint8_t>(row[i] - predictByte(filter, a, b, c));
    }
    return out;
}

inline Bytes unfilterRow(int filter, const Bytes& filtered, const Bytes& above, int bpp) {
    Bytes row(filtered.size());
    for (int i = 0; i < static_cast<int>(filtered.size()); ++i) {
        const int a = (i >= bpp) ? row[i - bpp] : 0;
        const int b = above[i];
        const int c = (i >= bpp) ? above[i - bpp] : 0;
        row[i] = static_cast<std::uint8_t>(filtered[i] + predictByte(filter, a, b, c));
    }
    return row;
}

inline long long rowScore(const Bytes& filtered) {
    long long sum = 0;
    for (std::uint8_t v : filtered) {
        sum += (v < 128) ? v : 256 - v;
    }
    return sum;
}

inline int bestFilter(const Bytes& row, const Bytes& above, int bpp) {
    int best = kFilterNone;
    long long bestScore = rowScore(row);
    for (int f = kFilterSub; f <= kFilterPaeth; ++f) {
        const long long score = rowScore(filterRow(f, row, above, bpp));
        if (score < bestScore) {
            best = f;
            bestScore = score;
        }
    }
    return best;
}

inline Bytes filterScanlines(const Bytes& rows, int rowLength, int bpp, int mode) {
    Bytes out;
    Bytes above(rowLength, 0);
    const int height = static_cast<int>(rows.size()) / (1 + rowLength);
    for (int y = 0; y < height; ++y) {
        const int start = y * (1 + rowLength) + 1;
        const Bytes row(rows.begin() + start, rows.begin() + start + rowLength);
        const int filter = (mode == kFilterBest) ? bestFilter(row, above, bpp) : mode;
        const Bytes filtered = filterRow(filter, row, above, bpp);
        out.push_back(static_cast<std::uint8_t>(filter));
        out.insert(out.end(), filtered.begin(), filtered.end());
        above = row;
    }
    return out;
}

inline std::string unfilterScanlines(const Bytes& rows, int rowLength, int bpp, Bytes& out) {
    out.clear();
    Bytes above(rowLength, 0);
    const int height = static_cast<int>(rows.size()) / (1 + rowLength);
    for (int y = 0; y < height; ++y) {
        const int start = y * (1 + rowLength) + 1;
        const int filter = rows[start - 1];
        if (filter > kFilterPaeth) {
            return "unknown filter type " + std::to_string(filter);
        }
        const Bytes filtered(rows.begin() + start, rows.begin() + start + rowLength);
        const Bytes row = unfilterRow(filter, filtered, above, bpp);
        out.push_back(0);
        out.insert(out.end(), row.begin(), row.end());
        above = row;
    }
    return "";
}

inline Bytes makePngBytesFiltered(const Image& image, int mode,
                                  const std::vector<std::uint8_t>* alpha = nullptr) {
    Bytes file;
    const int width = image.width();
    const int height = image.height();
    if (width <= 0 || height <= 0 || mode < kFilterNone || mode > kFilterBest) {
        return file;
    }
    if (alpha != nullptr && static_cast<int>(alpha->size()) != width * height) {
        alpha = nullptr;
    }
    const int bpp = (alpha != nullptr) ? 4 : 3;
    if ((1LL + bpp * static_cast<long long>(width)) * height > 1000000000LL) {
        return file;
    }
    const Bytes rows = filterScanlines(makePngRows(image, alpha), bpp * width, bpp, mode);
    appendPngSignature(file);
    appendChunk(file, "IHDR", makeIhdr(width, height, alpha != nullptr));
    appendChunk(file, "IDAT", zlibStore(rows));
    appendChunk(file, "IEND", Bytes{});
    return file;
}

inline bool savePNGFiltered(const Image& image, const std::string& fileName, int mode,
                            const std::vector<std::uint8_t>* alpha = nullptr) {
    Bytes file = makePngBytesFiltered(image, mode, alpha);
    if (file.empty()) {
        return false;
    }
    return writeBytes(fileName, file);
}

struct PngInfo {
    int width = 0;
    int height = 0;
    int bytesPerPixel = 0;
};

inline std::string readPngStart(const Bytes& file, PngInfo& info, Bytes& zdata) {
    std::vector<PngChunk> chunks;
    const std::string problem = listChunks(file, chunks);
    if (!problem.empty()) {
        return problem;
    }
    if (chunks.empty() || chunks[0].type != "IHDR" || chunks[0].length != 13) {
        return "the first chunk must be a 13-byte IHDR";
    }
    if (chunks.back().type != "IEND") {
        return "there is no IEND chunk";
    }
    zdata.clear();
    for (const PngChunk& c : chunks) {
        if (!c.crcOk) {
            return "the " + c.type + " chunk has a wrong CRC";
        }
        const bool critical = c.type[0] >= 'A' && c.type[0] <= 'Z';
        if (critical && !isKnownChunk(c.type)) {
            return "unknown critical chunk " + c.type;
        }
        if (c.type == "IDAT") {
            zdata.insert(zdata.end(), file.begin() + c.dataStart,
                         file.begin() + c.dataStart + c.length);
        }
    }
    const int d = chunks[0].dataStart;
    const std::uint32_t width = getU32BE(file, d);
    const std::uint32_t height = getU32BE(file, d + 4);
    const int bitDepth = file[d + 8];
    const int colourType = file[d + 9];
    if (width == 0 || height == 0 || static_cast<long long>(width) * height > 100000000LL) {
        return "bad width or height";
    }
    if (bitDepth != 8 || (colourType != 2 && colourType != 6)) {
        return "only 8-bit RGB and RGBA pictures are supported";
    }
    if (file[d + 10] != 0 || file[d + 11] != 0 || file[d + 12] != 0) {
        return "unknown compression, filter or interlace method";
    }
    info.width = static_cast<int>(width);
    info.height = static_cast<int>(height);
    info.bytesPerPixel = (colourType == 6) ? 4 : 3;
    return "";
}

inline std::string pngPixels(const PngInfo& info, const Bytes& rows, Image& image,
                             std::vector<std::uint8_t>* alpha) {
    const int w = info.width;
    const int h = info.height;
    const int bpp = info.bytesPerPixel;
    const long long rowBytes = 1 + static_cast<long long>(bpp) * w;
    if (static_cast<long long>(rows.size()) != rowBytes * h) {
        return "wrong amount of pixel data";
    }
    Bytes plain;
    const std::string problem = unfilterScanlines(rows, bpp * w, bpp, plain);
    if (!problem.empty()) {
        return problem;
    }
    Image result(w, h);
    std::vector<std::uint8_t> alphaResult(w * h, 255);
    for (int y = 0; y < h; ++y) {
        for (int x = 0; x < w; ++x) {
            const int at = static_cast<int>(y * rowBytes) + 1 + x * bpp;
            result.setPixel(x, y, Colour{plain[at], plain[at + 1], plain[at + 2]});
            if (bpp == 4) {
                alphaResult[y * w + x] = plain[at + 3];
            }
        }
    }
    image = result;
    if (alpha != nullptr) {
        *alpha = alphaResult;
    }
    return "";
}

inline std::string decodePNGFiltered(const Bytes& file, Image& image,
                                     std::vector<std::uint8_t>* alpha = nullptr) {
    PngInfo info;
    Bytes zdata;
    std::string problem = readPngStart(file, info, zdata);
    if (!problem.empty()) {
        return problem;
    }
    Bytes rows;
    problem = zlibUnstore(zdata, rows);
    if (!problem.empty()) {
        return "IDAT: " + problem;
    }
    return pngPixels(info, rows, image, alpha);
}

inline bool loadPNGFiltered(const std::string& fileName, Image& image,
                            std::vector<std::uint8_t>* alpha = nullptr) {
    Bytes file;
    if (!readFileBytes(fileName, file)) {
        return false;
    }
    return decodePNGFiltered(file, image, alpha).empty();
}

#endif
```

### Line by line

**The filter numbers (lines 1–18)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–7 | include guard and `#include` lines | Exact-size integers, strings, lists, and everything from Chapters 36–42. |
| 9–13 | `const int kFilterNone = 0;` … `const int kFilterPaeth = 4;` | The five filter types, with names, so the code says `kFilterUp` instead of a bare `2`. These numbers are written into the file. |
| 14 | `const int kFilterBest = 5;` | Not a PNG filter! It is **our** code for "choose the best filter for each row" (Section 43.9). It is never written into a file. |
| 16–18 | `inline int absInt(int v) { return (v < 0) ? -v : v; }` | The size of a number: −4 → 4. (We write our own, so we need no extra header.) |

**The predictions (lines 20–48)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 20–24 | `inline int paethPredictor(int a, int b, int c) { const int p = a + b - c; const int pa = absInt(p - a); ... }` | Paeth's first guess p, and how far each neighbour is from it (Section 43.7). All in `int`: p can be from −255 to 510. |
| 25–27 | `if (pa <= pb && pa <= pc) { return a; }` | a wins if it is at least as close as both others (ties go to a). |
| 28–30 | `if (pb <= pc) { return b; }` | Otherwise b, if it is at least as close as c. |
| 31–32 | `return c;` `}` | Otherwise c. |
| 34–40 | `inline int predictByte(int filter, int a, int b, int c) { if (filter == kFilterSub) { return a; } if (filter == kFilterUp) { return b; }` | The prediction of each filter (Section 43.2). |
| 41–43 | `if (filter == kFilterAverage) { return (a + b) / 2; }` | The average, rounded down. a + b is an `int`, so 510 is no problem. |
| 44–46 | `if (filter == kFilterPaeth) { return paethPredictor(a, b, c); }` | Paeth. |
| 47–48 | `return 0;` `}` | None (and anything else) predicts 0. |

**Filtering and unfiltering one row (lines 50–70)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 50–51 | `inline Bytes filterRow(int filter, const Bytes& row, const Bytes& above, int bpp) { Bytes out(row.size());` | Filter one row (without its filter byte). `above` is the row above, unfiltered; for the top row it is all zeros. |
| 52 | `for (int i = 0; i < static_cast<int>(row.size()); ++i) {` | Every byte, left to right. |
| 53–55 | `const int a = (i >= bpp) ? row[i - bpp] : 0; const int b = above[i]; const int c = (i >= bpp) ? above[i - bpp] : 0;` | The three neighbours (Section 43.3). Left of the first pixel they are 0. |
| 56 | `out[i] = static_cast<std::uint8_t>(row[i] - predictByte(filter, a, b, c));` | The residual. It may be negative; the cast to a byte wraps it mod 256 (Section 43.4). |
| 57–59 | `}` `return out;` `}` | Done. |
| 61–62 | `inline Bytes unfilterRow(int filter, const Bytes& filtered, const Bytes& above, int bpp) { Bytes row(filtered.size());` | The reverse (Section 43.8). `row` is filled from left to right. |
| 63–66 | `for (...) { const int a = (i >= bpp) ? row[i - bpp] : 0; const int b = above[i]; const int c = ...;` | The same neighbours — and **a comes from `row`**, the bytes already rebuilt, not from `filtered`. |
| 67 | `row[i] = static_cast<std::uint8_t>(filtered[i] + predictByte(filter, a, b, c));` | Add the prediction back, mod 256. |
| 68–70 | `}` `return row;` `}` | The original row. |

**Choosing a filter (lines 72–91)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 72–73 | `inline long long rowScore(const Bytes& filtered) { long long sum = 0;` | The score of Section 43.9. `long long` because a long row could add up to a big number. |
| 74–76 | `for (std::uint8_t v : filtered) { sum += (v < 128) ? v : 256 - v; }` | Read each byte as signed and add its size: 3 → 3, 252 → 4, 255 → 1. |
| 77–78 | `return sum;` `}` | Smaller is better. |
| 80–82 | `inline int bestFilter(const Bytes& row, const Bytes& above, int bpp) { int best = kFilterNone; long long bestScore = rowScore(row);` | Start with None: its residuals are the row itself. |
| 83–84 | `for (int f = kFilterSub; f <= kFilterPaeth; ++f) { const long long score = rowScore(filterRow(f, row, above, bpp));` | Try filters 1 to 4. |
| 85–88 | `if (score < bestScore) { best = f; bestScore = score; }` | Keep a filter only if it is **strictly** better. On a tie, the earlier filter stays (Up beats Paeth in Section 43.9). |
| 89–91 | `}` `return best;` `}` | The winner's number. |

**Whole pictures (lines 93–126)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 93–96 | `inline Bytes filterScanlines(const Bytes& rows, int rowLength, int bpp, int mode) { Bytes out; Bytes above(rowLength, 0); const int height = ...;` | Input: rows in Chapter 42's form (filter byte 0, then `rowLength` bytes). `above` starts as zeros: the row "above the top row". |
| 97–99 | `for (int y = 0; ...) { const int start = y * (1 + rowLength) + 1; const Bytes row(rows.begin() + start, rows.begin() + start + rowLength);` | Copy row y, skipping its filter byte. |
| 100 | `const int filter = (mode == kFilterBest) ? bestFilter(row, above, bpp) : mode;` | Either the same filter for every row, or the best one for this row. |
| 101–103 | `const Bytes filtered = filterRow(filter, row, above, bpp); out.push_back(...filter...); out.insert(out.end(), filtered.begin(), filtered.end());` | Write the filter byte, then the residuals. |
| 104 | `above = row;` | The **unfiltered** row becomes the next row's "above" (Section 43.8, ⚠️). |
| 105–107 | `}` `return out;` `}` | All rows, filtered. |
| 109–112 | `inline std::string unfilterScanlines(const Bytes& rows, int rowLength, int bpp, Bytes& out) { out.clear(); Bytes above(rowLength, 0); ...` | The reverse. It returns `""` or a problem, like our other readers. The caller has already checked the size. |
| 113–118 | `for (...) { const int start = ...; const int filter = rows[start - 1]; if (filter > kFilterPaeth) { return "unknown filter type " + std::to_string(filter); }` | Read the filter byte and refuse types above 4. |
| 119–120 | `const Bytes filtered(...); const Bytes row = unfilterRow(filter, filtered, above, bpp);` | Rebuild the row. |
| 121–123 | `out.push_back(0); out.insert(out.end(), row.begin(), row.end()); above = row;` | Write it out **with filter byte 0** — so the result has exactly Chapter 42's layout. The rebuilt row is the next "above". |
| 124–126 | `}` `return "";` `}` | Done. |

**Writing filtered PNGs (lines 128–158)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 128–135 | `inline Bytes makePngBytesFiltered(const Image& image, int mode, const std::vector<std::uint8_t>* alpha = nullptr) { ... if (width <= 0 \|\| height <= 0 \|\| mode < kFilterNone \|\| mode > kFilterBest) { return file; }` | Like `makePngBytes` (Chapter 42), with one more argument: the filter mode, 0–5. A bad mode gives an empty result. |
| 136–142 | the alpha size check, `bpp`, and the size limit | The same as Chapter 42, lines 35–41. |
| 143 | `const Bytes rows = filterScanlines(makePngRows(image, alpha), bpp * width, bpp, mode);` | The **only** new idea: make Chapter 42's rows, then filter them. |
| 144–149 | the four `append…` lines, `return file;` `}` | Signature, IHDR, IDAT and IEND, as before. |
| 151–158 | `inline bool savePNGFiltered(const Image& image, const std::string& fileName, int mode, ...) { ... }` | Build and write. |

**Reading filtered PNGs (lines 160–269)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 160–164 | `struct PngInfo { int width = 0; int height = 0; int bytesPerPixel = 0; };` | What step 1 learns from IHDR and step 3 needs (Section 43.12). |
| 166–171 | `inline std::string readPngStart(const Bytes& file, PngInfo& info, Bytes& zdata) { std::vector<PngChunk> chunks; const std::string problem = listChunks(file, chunks); if (...) { return problem; }` | Step 1. Check 1: walk the chunks (Chapter 40). |
| 172–177 | the IHDR and IEND checks | Checks 2 and 3, as in Chapter 42. |
| 178–191 | `zdata.clear(); for (const PngChunk& c : chunks) { ... }` | Checks 4 and 5, and join all IDAT data (Chapter 42, Section 42.5). |
| 192–205 | read the IHDR fields and the three checks | Checks 6, 7 and 8, word for word as in Chapter 42. |
| 206–210 | `info.width = static_cast<int>(width); info.height = ...; info.bytesPerPixel = (colourType == 6) ? 4 : 3; return "";` `}` | Hand back what we learned. |
| 212–216 | `inline std::string pngPixels(const PngInfo& info, const Bytes& rows, Image& image, std::vector<std::uint8_t>* alpha) { const int w = info.width; ... const int bpp = info.bytesPerPixel;` | Step 3. `rows` is the unpacked zlib data. |
| 217–220 | `const long long rowBytes = 1 + static_cast<long long>(bpp) * w; if (static_cast<long long>(rows.size()) != rowBytes * h) { return "wrong amount of pixel data"; }` | Check 10: exactly the right number of bytes. |
| 221–225 | `Bytes plain; const std::string problem = unfilterScanlines(rows, bpp * w, bpp, plain); if (!problem.empty()) { return problem; }` | The new check 11: unfilter every row, refusing unknown filter types. |
| 226–236 | `Image result(w, h); std::vector<std::uint8_t> alphaResult(w * h, 255); for (...) { for (...) { const int at = static_cast<int>(y * rowBytes) + 1 + x * bpp; result.setPixel(...); if (bpp == 4) { ... } } }` | Copy the pixels out of `plain`, exactly like Chapter 42, lines 118–132 (the `+ 1` skips each row's filter byte, now always 0). |
| 237–242 | `image = result; if (alpha != nullptr) { *alpha = alphaResult; } return "";` `}` | Hand back the picture and the alpha. |
| 244–251 | `inline std::string decodePNGFiltered(const Bytes& file, Image& image, std::vector<std::uint8_t>* alpha = nullptr) { PngInfo info; Bytes zdata; std::string problem = readPngStart(file, info, zdata); if (...) { return problem; }` | The new decoder. Step 1. |
| 252–256 | `Bytes rows; problem = zlibUnstore(zdata, rows); if (!problem.empty()) { return "IDAT: " + problem; }` | Step 2: unpack the zlib data (check 9). Chapter 45 replaces this line. |
| 257–258 | `return pngPixels(info, rows, image, alpha);` `}` | Step 3. |
| 260–267 | `inline bool loadPNGFiltered(...) { Bytes file; if (!readFileBytes(fileName, file)) { return false; } return decodePNGFiltered(file, image, alpha).empty(); }` | Read a file and decode it. It opens Chapter 42's files too (filter 0 is just "None"). |
| 269 | `#endif` | End of the include guard. |

---

## Code, part 2: filters at work

File: `ch43/filters.cpp`

```cpp
#include <cmath>
#include <iostream>
#include <string>
#include "pngfilter.h"

const char* const kFilterNames[6] = {"None", "Sub", "Up", "Average", "Paeth", "Best"};

std::string padLeft(const std::string& text, int width) {
    std::string s = text;
    while (static_cast<int>(s.size()) < width) {
        s = " " + s;
    }
    return s;
}

std::string oneDecimal(double v) {
    const long long tenths = std::llround(v * 10.0);
    return std::to_string(tenths / 10) + "." + std::to_string(tenths % 10);
}

void printRow(const std::string& label, const Bytes& row) {
    std::cout << label;
    for (std::uint8_t v : row) {
        std::cout << padLeft(std::to_string(v), 4);
    }
    std::cout << "\n";
}

bool samePictures(const Image& a, const Image& b) {
    if (a.width() != b.width() || a.height() != b.height()) {
        return false;
    }
    for (int y = 0; y < a.height(); ++y) {
        for (int x = 0; x < a.width(); ++x) {
            Colour p = a.getPixel(x, y);
            Colour q = b.getPixel(x, y);
            if (p.r != q.r || p.g != q.g || p.b != q.b) {
                return false;
            }
        }
    }
    return true;
}

int main() {
    const Bytes above = {100, 150, 200, 104, 152, 196, 108, 154, 192, 112, 156, 188};
    const Bytes row = {102, 151, 198, 106, 153, 194, 110, 155, 190, 114, 157, 186};
    printRow("above:      ", above);
    printRow("row:        ", row);
    for (int f = kFilterNone; f <= kFilterPaeth; ++f) {
        const Bytes filtered = filterRow(f, row, above, 3);
        const bool back = unfilterRow(f, filtered, above, 3) == row;
        printRow(padLeft(kFilterNames[f], 8) + " (" + std::to_string(f) + ")", filtered);
        std::cout << "              score " << rowScore(filtered)
                  << (back ? ", unfilters back to the row\n" : ", UNFILTER FAILED\n");
    }
    std::cout << "best filter for this row: " << kFilterNames[bestFilter(row, above, 3)] << "\n";

    const int tests[5][3] = {{50, 60, 70}, {100, 120, 100}, {50, 150, 100}, {10, 10, 10},
                             {200, 40, 60}};
    for (const auto& t : tests) {
        std::cout << "Paeth(a = " << t[0] << ", b = " << t[1] << ", c = " << t[2]
                  << ") = " << paethPredictor(t[0], t[1], t[2]) << "\n";
    }

    Image flag(300, 200);
    Image sky(300, 200);
    Image sunset(300, 200);
    Image blend(300, 200);
    Image noise(300, 200);
    unsigned int seed = 12345;
    for (int y = 0; y < 200; ++y) {
        for (int x = 0; x < 300; ++x) {
            Colour c = colours::white;
            if (x < 100) {
                c = Colour{0, 85, 164};
            } else if (x >= 200) {
                c = Colour{239, 65, 53};
            }
            flag.setPixel(x, y, c);
            sky.setPixel(x, y, lerpColour(Colour{40, 90, 200}, Colour{250, 200, 120}, y / 199.0));
            sunset.setPixel(x, y, lerpColour(Colour{250, 120, 40}, Colour{80, 20, 120}, x / 299.0));
            blend.setPixel(x, y, Colour{static_cast<std::uint8_t>(x * 255 / 299),
                                        static_cast<std::uint8_t>(y * 255 / 199),
                                        static_cast<std::uint8_t>((x + y) * 255 / 498)});
            seed = seed * 1103515245u + 12345u;
            const std::uint8_t v = static_cast<std::uint8_t>(seed >> 24);
            noise.setPixel(x, y, Colour{v, v, v});
        }
    }

    const Image* pictures[5] = {&flag, &sky, &sunset, &blend, &noise};
    const std::string names[5] = {"flag", "sky", "sunset", "blend", "noise"};
    const std::string columns = "    None     Sub      Up Average   Paeth    Best\n";
    std::cout << "\nzero bytes, in %" << std::string(9, ' ') << columns;
    std::string scoreTable = "average score per byte" + std::string(3, ' ') + columns;
    for (int i = 0; i < 5; ++i) {
        const Bytes plain = makePngRows(*pictures[i], nullptr);
        std::cout << "  " << names[i] << std::string(23 - names[i].size(), ' ');
        scoreTable += "  " + names[i] + std::string(23 - names[i].size(), ' ');
        for (int mode = kFilterNone; mode <= kFilterBest; ++mode) {
            const Bytes rows = filterScanlines(plain, 900, 3, mode);
            long long zeros = 0;
            long long score = 0;
            for (int y = 0; y < 200; ++y) {
                const Bytes filtered(rows.begin() + y * 901 + 1, rows.begin() + y * 901 + 901);
                for (std::uint8_t v : filtered) {
                    zeros += (v == 0) ? 1 : 0;
                }
                score += rowScore(filtered);
            }
            std::cout << padLeft(std::to_string(std::llround(zeros * 100.0 / 180000.0)), 8);
            scoreTable += padLeft(oneDecimal(score / 180000.0), 8);
        }
        std::cout << "\n";
    }
    std::cout << scoreTable;

    std::cout << "\nfilters chosen by Best (rows):\n";
    for (int i = 0; i < 5; ++i) {
        const Bytes rows = filterScanlines(makePngRows(*pictures[i], nullptr), 900, 3, kFilterBest);
        int used[5] = {0, 0, 0, 0, 0};
        for (int y = 0; y < 200; ++y) {
            used[rows[y * 901]] += 1;
        }
        std::cout << "  " << names[i] << ":";
        for (int f = kFilterNone; f <= kFilterPaeth; ++f) {
            std::cout << " " << kFilterNames[f] << " " << used[f];
        }
        std::cout << "\n";
    }

    std::cout << "\nfiles:\n";
    for (int i = 0; i < 5; ++i) {
        const std::string fileName = names[i] + ".png";
        if (!savePNGFiltered(*pictures[i], fileName, kFilterBest)) {
            std::cout << "could not write " << fileName << "\n";
            return 1;
        }
        Image back(0, 0);
        Image oldBack(0, 0);
        const bool ok = loadPNGFiltered(fileName, back) && samePictures(*pictures[i], back);
        const bool oldOk = loadPNG(fileName, oldBack);
        std::cout << "  " << fileName << ": " << makePngBytesFiltered(*pictures[i], kFilterBest).size()
                  << " bytes (without filters " << makePngBytes(*pictures[i]).size() << "), read back "
                  << (ok ? "the same" : "DIFFERENT") << ", Chapter 42's loadPNG "
                  << (oldOk ? "accepts it" : "refuses it") << "\n";
    }

    Bytes rows = filterScanlines(makePngRows(sky, nullptr), 900, 3, kFilterBest);
    rows[901 * 7] = 5;
    Bytes broken;
    appendPngSignature(broken);
    appendChunk(broken, "IHDR", makeIhdr(300, 200, false));
    appendChunk(broken, "IDAT", zlibStore(rows));
    appendChunk(broken, "IEND", Bytes{});
    Image ignored(0, 0);
    const std::string problem = decodePNGFiltered(broken, ignored);
    std::cout << "row 7 with filter type 5: "
              << (problem.empty() ? "accepted" : "refused (" + problem + ")") << "\n";
    return 0;
}
```

Build and run it from the `code/ch43` folder:

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common filters.cpp -o filters
./filters
```

### Line by line

**Helpers (lines 1–43)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–4 | the `#include` lines | `<cmath>` for `std::llround` (round to the nearest whole number), printing, strings, and the new header. |
| 6 | `const char* const kFilterNames[6] = {"None", "Sub", "Up", "Average", "Paeth", "Best"};` | Names for printing, by filter number. |
| 8–14 | `std::string padLeft(const std::string& text, int width) { ... }` | Add spaces in front until the text is `width` characters wide, so the columns line up. |
| 16–19 | `std::string oneDecimal(double v) { const long long tenths = std::llround(v * 10.0); return std::to_string(tenths / 10) + "." + std::to_string(tenths % 10); }` | Print a number with exactly one digit after the point: 88.94 → 889 tenths → "88.9". (Plain `std::cout` would print 0.0 as "0".) |
| 21–27 | `void printRow(const std::string& label, const Bytes& row) { ... }` | Print a label and the bytes, each 4 characters wide. |
| 29–43 | `bool samePictures(const Image& a, const Image& b) { ... }` | Chapter 39's comparison. |

**The example row (lines 46–64)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 46–49 | `const Bytes above = {...}; const Bytes row = {...}; printRow(...); printRow(...);` | The two rows of Section 43.5. |
| 50–52 | `for (int f = kFilterNone; f <= kFilterPaeth; ++f) { const Bytes filtered = filterRow(f, row, above, 3); const bool back = unfilterRow(f, filtered, above, 3) == row;` | Each filter, and a check that unfiltering gives the row back. `==` compares two lists byte by byte. |
| 53–56 | `printRow(padLeft(kFilterNames[f], 8) + " (" + std::to_string(f) + ")", filtered); std::cout << "              score " << rowScore(filtered) << ...` | Print the residuals and their score. |
| 57 | `std::cout << "best filter for this row: " << kFilterNames[bestFilter(row, above, 3)] << "\n";` | The choice of Section 43.9. |
| 59–64 | `const int tests[5][3] = {...}; for (const auto& t : tests) { ... paethPredictor(t[0], t[1], t[2]) ... }` | The five Paeth examples of Section 43.7. `const auto& t` is one row of the table: three numbers. |

**Five pictures (lines 66–90)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 66–71 | `Image flag(300, 200); ... Image noise(300, 200); unsigned int seed = 12345;` | Five pictures of the same size, and Chapter 39's random seed. |
| 72–80 | the flag stripes | Chapter 39's flag. |
| 81 | `sky.setPixel(x, y, lerpColour(..., y / 199.0));` | The vertical gradient: depends only on y. |
| 82 | `sunset.setPixel(x, y, lerpColour(Colour{250, 120, 40}, Colour{80, 20, 120}, x / 299.0));` | The horizontal gradient: depends only on x. |
| 83–85 | `blend.setPixel(x, y, Colour{... x * 255 / 299 ..., ... y * 255 / 199 ..., ... (x + y) * 255 / 498 ...});` | Red goes 0 → 255 across, green 0 → 255 down, blue 0 → 255 along the diagonal (x + y goes up to 299 + 199 = 498). |
| 86–90 | `seed = seed * 1103515245u + 12345u; ...` | Chapter 39's noise. |

**The two tables (lines 92–117)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 92–93 | `const Image* pictures[5] = {...}; const std::string names[5] = {...};` | The pictures and their names, so one loop handles all five. |
| 94–96 | `const std::string columns = "..."; std::cout << "\nzero bytes, in %" << std::string(9, ' ') << columns; std::string scoreTable = ...;` | The table headings. The second table is collected in a string and printed after the first. `std::string(9, ' ')` is 9 spaces. |
| 97–100 | `for (int i = 0; i < 5; ++i) { const Bytes plain = makePngRows(*pictures[i], nullptr); ... }` | For each picture: its rows with filter byte 0 (Chapter 42), and the start of both table lines. |
| 101–104 | `for (int mode = kFilterNone; mode <= kFilterBest; ++mode) { const Bytes rows = filterScanlines(plain, 900, 3, mode); long long zeros = 0; long long score = 0;` | Each mode, 0–5. A row has 300 × 3 = 900 bytes. |
| 105–111 | `for (int y = 0; y < 200; ++y) { const Bytes filtered(rows.begin() + y * 901 + 1, rows.begin() + y * 901 + 901); ... }` | Each filtered row is 901 bytes; skip its filter byte, count its zeros, and add its score. |
| 112–113 | `std::cout << padLeft(std::to_string(std::llround(zeros * 100.0 / 180000.0)), 8); scoreTable += padLeft(oneDecimal(score / 180000.0), 8);` | Zeros as a whole percentage, and the average score per byte. |
| 114–117 | `}` `std::cout << "\n";` `}` `std::cout << scoreTable;` | End the line; after all pictures, print the second table. |

**Which filters did Best choose? (lines 119–131)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 119–122 | `... const Bytes rows = filterScanlines(..., kFilterBest); int used[5] = {0, 0, 0, 0, 0};` | Filter adaptively, and count the filters. |
| 123–125 | `for (int y = 0; y < 200; ++y) { used[rows[y * 901]] += 1; }` | The filter byte is the first byte of each 901-byte row. |
| 126–131 | print the five counts | One line per picture. |

**Files (lines 133–148)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 133–139 | `const std::string fileName = names[i] + ".png"; if (!savePNGFiltered(*pictures[i], fileName, kFilterBest)) { ... return 1; }` | Save each picture with the best filter for each row. |
| 140–143 | `Image back(0, 0); Image oldBack(0, 0); const bool ok = loadPNGFiltered(fileName, back) && samePictures(...); const bool oldOk = loadPNG(fileName, oldBack);` | Load it with the new loader (must give the same picture) and with Chapter 42's loader (which must refuse it). |
| 144–148 | `std::cout << "  " << fileName << ": " << makePngBytesFiltered(...).size() << " bytes (without filters " << makePngBytes(...).size() << ...` | The sizes, with and without filters (Section 43.11). |

**A broken file (lines 150–162)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 150–151 | `Bytes rows = filterScanlines(makePngRows(sky, nullptr), 900, 3, kFilterBest); rows[901 * 7] = 5;` | The sky's filtered rows, with the filter byte of row 7 changed to 5 — a type that does not exist. |
| 152–156 | `Bytes broken; appendPngSignature(broken); appendChunk(broken, "IHDR", ...); appendChunk(broken, "IDAT", zlibStore(rows)); appendChunk(broken, "IEND", Bytes{});` | Build a PNG around it, with correct CRCs and Adler-32, so that only the filter check can catch it. |
| 157–160 | `Image ignored(0, 0); const std::string problem = decodePNGFiltered(broken, ignored); std::cout << ...` | Decode and print the reason. |
| 161–162 | `return 0;` `}` | Done. |

### What you should see

```
above:       100 150 200 104 152 196 108 154 192 112 156 188
row:         102 151 198 106 153 194 110 155 190 114 157 186
    None (0) 102 151 198 106 153 194 110 155 190 114 157 186
              score 1096, unfilters back to the row
     Sub (1) 102 151 198   4   2 252   4   2 252   4   2 252
              score 295, unfilters back to the row
      Up (2)   2   1 254   2   1 254   2   1 254   2   1 254
              score 20, unfilters back to the row
 Average (3)  52  76  98   3   2 253   3   2 253   3   2 253
              score 250, unfilters back to the row
   Paeth (4)   2   1 254   2   1 254   2   1 254   2   1 254
              score 20, unfilters back to the row
best filter for this row: Up
Paeth(a = 50, b = 60, c = 70) = 50
Paeth(a = 100, b = 120, c = 100) = 120
Paeth(a = 50, b = 150, c = 100) = 100
Paeth(a = 10, b = 10, c = 10) = 10
Paeth(a = 200, b = 40, c = 60) = 200

zero bytes, in %             None     Sub      Up Average   Paeth    Best
  flag                         11      99     100      99     100     100
  sky                           0     100      35      48     100     100
  sunset                        0      61     100      90     100     100
  blend                         0      54      50      21      83      83
  noise                         0       0       0       0       0       0
average score per byte       None     Sub      Up Average   Paeth    Best
  flag                       35.0     0.5     0.2     1.0     0.0     0.0
  sky                        88.9     0.3     1.0     1.0     0.0     0.0
  sunset                     75.8     0.6     0.4     0.6     0.0     0.0
  blend                      70.6     0.6     0.8     1.1     0.2     0.2
  noise                      64.2    63.9    64.2    64.1    64.1    61.9

filters chosen by Best (rows):
  flag: None 0 Sub 1 Up 199 Average 0 Paeth 0
  sky: None 0 Sub 1 Up 0 Average 0 Paeth 199
  sunset: None 0 Sub 1 Up 199 Average 0 Paeth 0
  blend: None 0 Sub 1 Up 0 Average 0 Paeth 199
  noise: None 55 Sub 34 Up 43 Average 41 Paeth 27

files:
  flag.png: 180278 bytes (without filters 180278), read back the same, Chapter 42's loadPNG refuses it
  sky.png: 180278 bytes (without filters 180278), read back the same, Chapter 42's loadPNG refuses it
  sunset.png: 180278 bytes (without filters 180278), read back the same, Chapter 42's loadPNG refuses it
  blend.png: 180278 bytes (without filters 180278), read back the same, Chapter 42's loadPNG refuses it
  noise.png: 180278 bytes (without filters 180278), read back the same, Chapter 42's loadPNG refuses it
row 7 with filter type 5: refused (unknown filter type 5)
```

(The percentages are rounded: "100" for the sky with Sub really means 99.7 %.) And five PNG files that every viewer opens.

---

## Small examples

### Example 1 — Sub on a grey row

A grey picture stored as RGB, one row: (10, 10, 10) (12, 12, 12) (15, 15, 15). Sub: `10 10 10 2 2 2 3 3 3`.

### Example 2 — Up on the top row

In the top row, b = 0, so Up gives the bytes **unchanged** — exactly like None.

### Example 3 — Wrap-around back and forth

x = 3, a = 250. Sub: 3 − 250 = −247 → −247 + 256 = **9**. Unfilter: 9 + 250 = 259 → 259 − 256 = **3** ✓.

### Example 4 — Average with a big sum

a = 255, b = 255, x = 0. Prediction ⌊510 / 2⌋ = 255. Residual 0 − 255 = −255 → **1**. (In a byte, 255 + 255 would have wrapped to 254, and the prediction would be 127 — wrong.)

### Example 5 — The score of a row

Residuals `0 1 255 0 254 3`: sizes 0 + 1 + 1 + 0 + 2 + 3 = **7**.

---

## Common mistakes

⚠️ **Using the filtered neighbours** — a, b and c are always the **original** bytes. Keep the unfiltered row as "above".

⚠️ **The neighbour 1 byte back** — "left" means the same colour channel in the pixel to the left: **bpp** bytes back (3 or 4), not 1.

⚠️ **Forgetting the 0 outside** — left of the first pixel and above the top row, a, b and c are 0.

⚠️ **Computing the Average in a byte** — a + b can be 510. Use `int`.

⚠️ **Breaking Paeth's ties differently** — a, then b, then c. Any other order rebuilds wrong pixels.

⚠️ **Scoring unsigned bytes** — 255 means −1, a very small residual. Read bytes above 127 as negative.

⚠️ **Expecting smaller files now** — with stored blocks, filters do not change the size. They pay off with real compression (Chapters 44–45).

---

## Practice

🏋️ **1.** Filter the RGB row (20, 40, 60) (22, 41, 58) with **Sub**, by hand. Then unfilter your answer.

🏋️ **2.** Compute Paeth(a = 30, b = 90, c = 40) and Paeth(a = 90, b = 30, c = 60).

🏋️ **3.** The row above is `10 20 30 10 20 30` and the row is `11 21 31 12 22 32` (bpp 3). Filter it with **Average**.

🏋️ **4.** Why does the top row of a picture never benefit from Up? Which filters are left that can still help there?

🏋️ **5.** Write `int countZeros(const Bytes& b)` and use it to show that the "Best" sky has 179,608 zero bytes out of 180,000.

🏋️ **6.** Change the rule in `bestFilter` to "most zero bytes wins" instead of "smallest score". Which filters does it choose for the noise picture? Is that sensible?

🏋️ **7.** Save a transparent picture (Chapter 42's `disk.png`) with `savePNGFiltered(disk, "disk.png", kFilterBest, &diskAlpha)`. Check that it opens in a browser and that `loadPNGFiltered` gives the same alpha back. Which bpp is used?

🏋️ **8.** Explain why the decoder must unfilter the rows **in order, from top to bottom**, and why it cannot start in the middle of the picture.

---

## Answers

**1.**
> Sub: 20 40 60 (nothing on the left), then 22 − 20 = **2**, 41 − 40 = **1**, 58 − 60 = −2 → **254**.
> Unfilter: 20 40 60, then 2 + 20 = 22, 1 + 40 = 41, 254 + 60 = 314 → 314 − 256 = **58** ✓.

**2.**
> p = 30 + 90 − 40 = 80; pa = 50, pb = 10, pc = 40 → **b = 90**.
> p = 90 + 30 − 60 = 60; pa = 30, pb = 30, pc = 0 → **c = 60**.

**3.**
> pixel 0 (a = 0): ⌊10 / 2⌋ = 5 → 11 − 5 = **6**; ⌊20 / 2⌋ = 10 → **11**; ⌊30 / 2⌋ = 15 → **16**.
> pixel 1: ⌊(11 + 10) / 2⌋ = 10 → 12 − 10 = **2**; ⌊(21 + 20) / 2⌋ = 20 → **2**; ⌊(31 + 30) / 2⌋ = 30 → **2**.
> Result: `6 11 16 2 2 2`.

**4.**
> Above the top row, everything is 0, so Up predicts 0: it is the same as None. Sub (and Paeth, which acts like Sub there) can still help, and so can Average, which predicts half of the left byte.

**5.**

```cpp
int countZeros(const Bytes& b) {
    int n = 0;
    for (std::uint8_t v : b) {
        n += (v == 0) ? 1 : 0;
    }
    return n;
}
```

> Filter the sky with `kFilterBest`, then add `countZeros` of each 900-byte row without its filter byte (the filter bytes are 1 and 4, never 0, so counting all 180,200 bytes gives the same answer): **179,608**.

**6.**
> For noise, every row has only 3 to 18 zeros out of 900 bytes, whatever the filter, so the choice is close to random: None 64 rows, Sub 50, Up 39, Average 39, Paeth 8. That is fine for noise (no filter helps), but in general "most zeros" ignores bytes like 1 and 255, which also compress well. The sum of sizes is a better measure for photos.

**7.**
> It works: `makePngBytesFiltered` sees the alpha list and uses **bpp = 4**, so "left" is 4 bytes back and the alpha bytes are compared with the alpha of the pixel to the left. `loadPNGFiltered(…, &alphaBack)` gives `alphaBack == diskAlpha`.

**8.**
> To rebuild row y, we need the **rebuilt** row y − 1 (for b and c). To rebuild that, we need row y − 2, and so on, up to the top row. Within a row, we also need the rebuilt bytes on the left (for a). So the decoder must go top to bottom, left to right. (Only rows that use None or Sub could be rebuilt alone.)

---

## Summary

🧠 Neighbouring pixels are **similar**, not equal. A **filter** stores each byte as a **residual**: the byte minus a **prediction** from its neighbours.

🧠 Five filters: **None** (0), **Sub** (left), **Up** (above), **Average** (⌊(left + above) / 2⌋), **Paeth** (the neighbour closest to left + above − above-left; ties a, b, c).

🧠 Filters work on **bytes**; "left" is **bpp** bytes back; outside the picture everything is **0**; all sums are **mod 256**.

🧠 **Unfilter** = the same prediction, from the **already rebuilt** bytes, **plus** the residual. Nothing is lost.

🧠 Choose a filter **per row**: the smallest sum of residual sizes, reading bytes as **signed**.

🧠 Filters turn smooth pictures into almost all zeros — but files only get smaller with real compression (Chapters 44–45).

---

## Next chapter

We now have rows that are mostly zeros. How do we store "mostly zeros" in fewer bytes? In Chapter 44 we learn **Huffman coding**: common values get **short** codes (maybe just 1 bit), rare values get long ones. We will build Huffman codes from counts, write and read them **bit by bit**, and finally see our filtered sky shrink to a small part of its size.
