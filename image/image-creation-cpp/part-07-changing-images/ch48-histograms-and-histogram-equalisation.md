# Chapter 48 — Histograms and Histogram Equalisation

> **Part 7 · Chapter 48 of 82**
> **You need:** Chapters 1–47 (especially 15, 46 and 47) · **You will make:** `histogram.h` (counting values, cumulative counts, mean, percentiles, automatic levels, histogram equalisation, and drawing a histogram), and `histograms.png`: a dull picture, its automatic fix and its equalised version, each with its histogram

---

## What you will learn

- What a **histogram** is, and how to read one at a glance.
- How to compute the **mean**, the lowest and highest values, and **percentiles** from it.
- Why the darkest and brightest single pixels are a bad guide, and how percentiles fix that.
- **Automatic levels**: choosing Chapter 47's levels from the histogram.
- **Cumulative** counts, and **histogram equalisation**: spreading values so that all brightnesses are used about equally.
- Why equalisation never adds detail that was not there.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **histogram** | A count of how many pixels have each value, 0 to 255. |
| **bin** | One "box" of a histogram: one value, or a group of values. |
| **mean** | The average value. |
| **cumulative count** | How many pixels have this value **or a smaller one**. |
| **percentile** | The value below which a given part (say 1 %) of the pixels lie. |
| **outlier** | A rare value far away from the rest, like one very bright pixel. |
| **equalisation** | Remapping values so that every brightness is used about equally. |

---

## 48.1 Counting values

Look at a dull, grey picture. Is it too dark? Too bright? Too low in contrast? Our eyes can be fooled. Numbers cannot.

📖 **New word: histogram** — for each value v from 0 to 255, **how many** pixels have that value:

> h[v] = the number of pixels whose value is v

It is a list of 256 counts — the same shape as Chapter 47's lookup table, but holding counts:

```cpp
using Histogram = std::array<long long, 256>;
```

(`long long`, because a big photo has many millions of pixels.)

For a colour picture, we can count each channel separately (three histograms), or count the **grey** value of each pixel (Chapter 15's `greyByte`) — one histogram that shows lightness. We mostly use the grey one.

🔢 **Maths: a tiny picture** (4 × 2 grey pixels, the program's first example)

> values: 50 50 60 60 60 70 90 200
> h[50] = **2**, h[60] = **3**, h[70] = **1**, h[90] = **1**, h[200] = **1**; all other counts are 0
> total: 2 + 3 + 1 + 1 + 1 = **8** = the number of pixels ✓

The counts always add up to the number of pixels. That is a good check.

---

## 48.2 Reading a histogram

📖 **New word: bin** — one "box" of the histogram. With 256 bins, each bin is one value. For printing, the program groups 16 values per bin, so 16 bins fit on the screen.

A histogram drawn as a bar chart (value across, count up) tells a lot at once:

```
   too dark            too bright           low contrast         good contrast
   █                              █              ██
   ██                            ██             ████              ▄ ▄█▄  ▄
   ███▄                        ▄███             ████             ███████▄█▄
   ████▄▄▄___          ___▄▄▄█████            ▁▄████▄▁         ▄██████████▄
   0        255        0        255        0        255       0        255
```

- Bars piled up on the **left**: most pixels are dark.
- Piled up on the **right**: most pixels are bright.
- A narrow **heap in the middle**: few values are used — a grey, foggy picture.
- Spread over the **whole width**: good contrast.
- A tall bar at 0 or 255: **clipping** (Chapter 47) — many pixels lost their detail.

⚠️ A histogram tells you **how many** pixels have each value, but **not where** they are. A picture and its pixels shuffled at random have the same histogram.

---

## 48.3 Numbers from a histogram

The histogram is enough to compute many useful numbers — without looking at the picture again.

**Lowest and highest value:** the first and the last v whose count is not 0.

**Values used:** how many counts are not 0.

📖 **New word: mean** — the average value:

> mean = (sum of v × h[v]) / (number of pixels)

🔢 **Maths: the tiny picture**

> lowest **50**, highest **200**, 5 values used
> mean = (50 × 2 + 60 × 3 + 70 × 1 + 90 × 1 + 200 × 1) / 8 = (100 + 180 + 70 + 90 + 200) / 8 = 640 / 8 = **80**

```
tiny: lowest 50, highest 200, mean 80.0, 5 values used, 1% at 50, 99% at 200
```

The mean tells whether a picture is dark (well below 128) or bright (well above). It is also a good **centre** for Chapter 47's contrast.

---

## 48.4 Cumulative counts and percentiles

📖 **New word: cumulative count** — for each value, how many pixels have **this value or a smaller one**:

> c[v] = h[0] + h[1] + … + h[v]

It grows from left to right and ends at the total: c[255] = the number of pixels.

🔢 **Maths: the tiny picture**

| v | h[v] | c[v] |
|---|---|---|
| 50 | 2 | **2** |
| 60 | 3 | 2 + 3 = **5** |
| 70 | 1 | **6** |
| 90 | 1 | **7** |
| 200 | 1 | **8** |

(Between these values, c stays the same: c[61] … c[69] are all 5.)

📖 **New word: percentile** — the value below which a given part of the pixels lie. The **1st percentile** is the value that only the darkest 1 % of the pixels reach; the **99th percentile** is the value that only the brightest 1 % pass.

With the cumulative counts, it is easy: the p-th percentile is the **first** v where c[v] ≥ p × total.

🔢 **Maths: the median of the tiny picture**

> the median (the 50th percentile): 0.5 × 8 = 4 → the first v with c[v] ≥ 4 is **60** (c[60] = 5)

So half of the pixels are 60 or darker — even though the mean is 80. The one bright pixel (200) pulls the mean up, but not the median.

📖 **New word: outlier** — a rare value far away from the others, like that 200. A single dust speck, a reflection or a dead pixel is an outlier. It makes "lowest" and "highest" useless for choosing levels: one white pixel in a dull photo, and the highest value is 255 even though everything else ends at 150. Percentiles ignore such loners.

---

## 48.5 Automatic levels

Chapter 47's levels stretches a range [low, high] to 0 … 255. Now we can choose that range **from the picture**:

> low = the 1st percentile, high = the 99th percentile
> then apply `levelsTable(low, high)`

The darkest 1 % become black, the brightest 1 % white, and everything between is spread out. Many photo programs call this "auto contrast".

The program's test picture is a deliberately **dull** 256 × 160 grey scene: a faint gradient, a "sun" and some hills — all between 81 and 151.

```
dull: lowest 81, highest 151, mean 116.6, 71 values used, 1% at 84, 99% at 149
    0- 15 | 0
   ...
   80- 95 |########## 3892
   96-111 |############################# 11252
  112-127 |######################################## 15329
  128-143 |####################### 8655
  144-159 |##### 1832
  160-175 | 0
   ...
```

A narrow heap in the middle: low contrast. The 1st percentile is **84**, the 99th **149**, so the program applies levels 84 … 149:

🔢 **Maths: what levels 84 … 149 does**

> 84 → 0, 149 → 255, and each step of 1 becomes a step of 255 / 65 ≈ **3.9**
> 116 (near the mean) → (116 − 84) × 255 / 65 = 125.54 → **126**
> 81, 82, 83 → 0 and 150, 151 → 255: about 1 % of the pixels at each end are clipped

```
auto levels: lowest 0, highest 255, mean 127.7, 66 values used, 1% at 0, 99% at 255
    0- 15 |########### 1364
   16- 31 |############## 1680
   ...
  240-255 |########### 1328
```

The values now cover the full range. But the number of **different** values went **down**, from 71 to 66: 81, 82, 83 and 84 all became 0, and 150 and 151 both became 255. A point operation can **merge** values, but never split one value into two.

---

## 48.6 Histogram equalisation

Auto levels **stretches** the heap evenly, so its shape stays the same: a hill. But maybe the picture would look better if **every** brightness were used about equally — a **flat** histogram.

📖 **New word: equalisation** — a point operation chosen so that the new histogram is as flat as possible.

The idea: rank the pixels from darkest to brightest. A pixel that is darker than 30 % of the picture should get a new value 30 % of the way from black to white. The cumulative count tells us exactly that fraction:

> fraction of pixels at or below v = c[v] / total
> new value ≈ fraction × 255

Values with many pixels make c jump a lot, so they get spread far apart; rare values make c barely move, so they get squeezed together. That is exactly what flattens the histogram.

One small correction: the darkest value should become exactly 0. If the lowest value has c_min pixels, we use:

> **new = (c[v] − c_min) × 255 / (total − c_min)**, rounded

🔢 **Maths: equalising the tiny picture** (c_min = c[50] = 2, total = 8, so total − c_min = 6)

> 50: (2 − 2) × 255 / 6 = **0**
> 60: (5 − 2) × 255 / 6 = 127.5 → **128**
> 70: (6 − 2) × 255 / 6 = 170 → **170**
> 90: (7 − 2) × 255 / 6 = 212.5 → **213**
> 200: (8 − 2) × 255 / 6 = **255**

```
value  50: count 2, cumulative 2, equalised 0
value  60: count 3, cumulative 5, equalised 128
value  70: count 1, cumulative 6, equalised 170
value  90: count 1, cumulative 7, equalised 213
value 200: count 1, cumulative 8, equalised 255
```

Look at the gaps: 50, 60, 70, 90 were close together, and now they are spread across the whole range; the big jump from 90 to 200 became a small one (213 to 255), because only one pixel lives up there.

On the dull picture:

```
equalised: lowest 0, highest 255, mean 129.8, 69 values used, 1% at 3, 99% at 254
    0- 15 |################################ 2424
   16- 31 |################################# 2528
   ...
  240-255 |##################################### 2829
```

The bars are **almost flat** — compare them with the hill of auto levels. The mean is near the middle (129.8).

⚠️ **Equalisation does not add detail.** The picture still has only 69 different values; they are just spread out with **gaps** between them (the 256-bin histogram looks like a comb). If you look closely at a smooth gradient after strong equalisation, you may see **bands**. And equalisation can make things look unnatural: a foggy scene **should** be low in contrast. It is a strong tool; use it with care.

---

## 48.7 Drawing a histogram

`drawHistogram` draws a histogram as a picture: a frame 258 pixels wide (256 columns + 2 for the frame), one column per value, and a bar whose height is the count **scaled** so that the tallest bar fills the graph:

🔢 **Maths: scaling the bars**

> bar = round(h[v] × height / highest count)
> in whole numbers: (h[v] × height + highest / 2) / highest — adding half the divisor rounds instead of cutting
> a count of 300 with height 80 and a highest count of 1,000: (24,000 + 500) / 1,000 = **24** pixels

Under the frame, the text "0" and "255" mark the ends (Chapter 46). Open `histograms.png`: the dull picture with its narrow heap, the auto-levels picture with the same heap stretched wide, and the equalised picture with an even "comb".

---

## 48.8 Colour pictures

Our test picture is grey, so all three channels are equal. For a **colour** picture, there are two simple ways:

1. **One table for all channels**: build the table from the **grey** histogram and apply it to red, green and blue (what `applyTable` does). Colours keep their character; lightness changes.
2. **One table per channel**: equalise each channel's own histogram (`channelHistogram`) and use `applyTables`. This stretches each channel fully — which also **changes the colours**: a picture with a blue colour cast becomes more neutral, but a sunset may lose its orange.

Neither is "right"; they do different things. Practice 6 tries both.

---

## Code, part 1: `histogram.h`

File: `common/histogram.h` (new). It includes `pointops.h` (lookup tables and levels, Chapter 47).

```cpp
#ifndef HISTOGRAM_H
#define HISTOGRAM_H

#include <algorithm>
#include <array>
#include "pointops.h"

using Histogram = std::array<long long, 256>;

inline Histogram greyHistogram(const Image& image) {
    Histogram h{};
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            h[greyByte(image.getPixel(x, y))] += 1;
        }
    }
    return h;
}

inline Histogram channelHistogram(const Image& image, int channel) {
    Histogram h{};
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            const Colour c = image.getPixel(x, y);
            const int v = (channel == 0) ? c.r : (channel == 1) ? c.g : c.b;
            h[v] += 1;
        }
    }
    return h;
}

inline Histogram cumulative(const Histogram& h) {
    Histogram c{};
    long long sum = 0;
    for (int v = 0; v < 256; ++v) {
        sum += h[v];
        c[v] = sum;
    }
    return c;
}

inline long long histogramTotal(const Histogram& h) {
    return cumulative(h)[255];
}

inline int lowestValue(const Histogram& h) {
    for (int v = 0; v < 256; ++v) {
        if (h[v] > 0) {
            return v;
        }
    }
    return 0;
}

inline int highestValue(const Histogram& h) {
    for (int v = 255; v >= 0; --v) {
        if (h[v] > 0) {
            return v;
        }
    }
    return 0;
}

inline int usedValues(const Histogram& h) {
    int used = 0;
    for (long long n : h) {
        used += (n > 0) ? 1 : 0;
    }
    return used;
}

inline double histogramMean(const Histogram& h) {
    long long total = 0;
    double sum = 0.0;
    for (int v = 0; v < 256; ++v) {
        total += h[v];
        sum += static_cast<double>(v) * h[v];
    }
    return (total == 0) ? 0.0 : sum / total;
}

inline int percentile(const Histogram& h, double fraction) {
    const Histogram c = cumulative(h);
    const double wanted = fraction * c[255];
    for (int v = 0; v < 256; ++v) {
        if (c[v] >= wanted && c[v] > 0) {
            return v;
        }
    }
    return 255;
}

inline LookupTable autoLevelsTable(const Histogram& h, double clipFraction) {
    return levelsTable(percentile(h, clipFraction), percentile(h, 1.0 - clipFraction));
}

inline LookupTable equaliseTable(const Histogram& h) {
    const Histogram c = cumulative(h);
    const long long total = c[255];
    const long long first = h[lowestValue(h)];
    if (total == first) {
        return identityTable();
    }
    LookupTable t{};
    for (int v = 0; v < 256; ++v) {
        t[v] = (c[v] <= first) ? 0 : clampByte((c[v] - first) * 255.0 / (total - first));
    }
    return t;
}

inline void drawHistogram(Image& image, int x, int y, int height, const Histogram& h, Colour c) {
    const long long highest = *std::max_element(h.begin(), h.end());
    strokeRect(image, makeRect(x, y, 258, height + 2), 1, Colour{170, 170, 170});
    for (int v = 0; v < 256; ++v) {
        const int bar = (highest == 0) ? 0 : static_cast<int>((h[v] * height + highest / 2) / highest);
        fillRect(image, makeRect(x + 1 + v, y + 1 + height - bar, 1, bar), c);
    }
    drawText(image, x, y + height + 5, "0", colours::black);
    drawText(image, x + 258 - textWidth("255", 1), y + height + 5, "255", colours::black);
}

#endif
```

### Line by line

**Counting (lines 1–44)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–6 | include guard and `#include` lines | `std::max_element`, `std::array`, and Chapter 47's header (with the whole drawing library). |
| 8 | `using Histogram = std::array<long long, 256>;` | 256 counts (Section 48.1). |
| 10–18 | `inline Histogram greyHistogram(const Image& image) { Histogram h{}; for (...) { for (...) { h[greyByte(image.getPixel(x, y))] += 1; } } return h; }` | Count the grey value of every pixel. `h{}` starts with all counts 0. The value itself is the index. |
| 20–30 | `inline Histogram channelHistogram(const Image& image, int channel) { ... const int v = (channel == 0) ? c.r : (channel == 1) ? c.g : c.b; h[v] += 1; ... }` | Count one channel: 0 = red, 1 = green, 2 = blue (Section 48.8). |
| 32–40 | `inline Histogram cumulative(const Histogram& h) { Histogram c{}; long long sum = 0; for (...) { sum += h[v]; c[v] = sum; } return c; }` | A running total (Section 48.4). |
| 42–44 | `inline long long histogramTotal(const Histogram& h) { return cumulative(h)[255]; }` | The number of pixels counted. |

**Simple numbers (lines 46–91)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 46–53 | `inline int lowestValue(const Histogram& h) { for (int v = 0; v < 256; ++v) { if (h[v] > 0) { return v; } } return 0; }` | The first used value (0 for an empty histogram). |
| 55–62 | `inline int highestValue(const Histogram& h) { for (int v = 255; v >= 0; --v) { ... } return 0; }` | The last used value: search from the top. |
| 64–70 | `inline int usedValues(const Histogram& h) { int used = 0; for (long long n : h) { used += (n > 0) ? 1 : 0; } return used; }` | How many different values appear. |
| 72–80 | `inline double histogramMean(const Histogram& h) { ... sum += static_cast<double>(v) * h[v]; ... return (total == 0) ? 0.0 : sum / total; }` | Section 48.3's mean. An empty histogram gives 0 instead of dividing by 0. |
| 82–91 | `inline int percentile(const Histogram& h, double fraction) { const Histogram c = cumulative(h); const double wanted = fraction * c[255]; for (...) { if (c[v] >= wanted && c[v] > 0) { return v; } } return 255; }` | The first value whose cumulative count reaches the wanted part (Section 48.4). `c[v] > 0` skips the empty values at the start, so the 0th percentile is the lowest used value, not 0. |

**Tables from histograms (lines 93–109)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 93–95 | `inline LookupTable autoLevelsTable(const Histogram& h, double clipFraction) { return levelsTable(percentile(h, clipFraction), percentile(h, 1.0 - clipFraction)); }` | Section 48.5: levels from two percentiles. With 0.01: the 1st and 99th. |
| 97–100 | `inline LookupTable equaliseTable(const Histogram& h) { const Histogram c = cumulative(h); const long long total = c[255]; const long long first = h[lowestValue(h)];` | Section 48.6: the cumulative counts, the total, and c_min — the count of the lowest used value. |
| 101–103 | `if (total == first) { return identityTable(); }` | If the picture has only **one** value, there is nothing to spread out — and the formula would divide by 0. |
| 104–109 | `LookupTable t{}; for (int v = 0; v < 256; ++v) { t[v] = (c[v] <= first) ? 0 : clampByte((c[v] - first) * 255.0 / (total - first)); } return t;` `}` | The equalisation formula. Values up to the lowest used one get 0. `255.0` makes the division a `double` division. |

**Drawing (lines 111–122)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 111–113 | `inline void drawHistogram(Image& image, int x, int y, int height, const Histogram& h, Colour c) { const long long highest = *std::max_element(h.begin(), h.end()); strokeRect(image, makeRect(x, y, 258, height + 2), 1, Colour{170, 170, 170});` | Find the tallest count (`std::max_element` gives its position; `*` reads it), and draw the frame. |
| 114–117 | `for (int v = 0; v < 256; ++v) { const int bar = (highest == 0) ? 0 : static_cast<int>((h[v] * height + highest / 2) / highest); fillRect(image, makeRect(x + 1 + v, y + 1 + height - bar, 1, bar), c); }` | One 1-pixel-wide bar per value, standing on the bottom of the frame (Section 48.7). |
| 118–120 | `drawText(image, x, y + height + 5, "0", colours::black); drawText(image, x + 258 - textWidth("255", 1), y + height + 5, "255", colours::black);` `}` | Labels under both ends; "255" ends at the right edge of the frame. |
| 122 | `#endif` | End of the include guard. |

---

## Code, part 2: fixing a dull picture

File: `ch48/histogram.cpp`

```cpp
#include <cmath>
#include <iostream>
#include <string>
#include "histogram.h"
#include "deflate.h"

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

Image makeDull() {
    Image picture(256, 160);
    for (int y = 0; y < 160; ++y) {
        for (int x = 0; x < 256; ++x) {
            int v = 100 + x / 8 + y / 10;
            const int dx = x - 180;
            const int dy = y - 50;
            if (dx * dx + dy * dy <= 625) {
                v += 20;
            }
            const int slope = (x % 64 < 32) ? x % 32 : 31 - x % 32;
            if (y > 112 + slope / 2) {
                v -= 30;
            }
            const std::uint8_t g = static_cast<std::uint8_t>(v);
            picture.setPixel(x, y, Colour{g, g, g});
        }
    }
    return picture;
}

void printStats(const std::string& name, const Histogram& h) {
    std::cout << name << ": lowest " << lowestValue(h) << ", highest " << highestValue(h) << ", mean "
              << oneDecimal(histogramMean(h)) << ", " << usedValues(h) << " values used, 1% at "
              << percentile(h, 0.01) << ", 99% at " << percentile(h, 0.99) << "\n";
}

void printBars(const Histogram& h) {
    long long bins[16] = {};
    for (int v = 0; v < 256; ++v) {
        bins[v / 16] += h[v];
    }
    long long most = 0;
    for (long long n : bins) {
        most = std::max(most, n);
    }
    for (int b = 0; b < 16; ++b) {
        const int length = static_cast<int>((bins[b] * 40 + most / 2) / most);
        std::cout << padLeft(std::to_string(b * 16), 5) << "-" << padLeft(std::to_string(b * 16 + 15), 3)
                  << " |" << std::string(length, '#') << " " << bins[b] << "\n";
    }
}

int main() {
    Image tiny(4, 2);
    const int values[8] = {50, 50, 60, 60, 60, 70, 90, 200};
    for (int i = 0; i < 8; ++i) {
        const std::uint8_t g = static_cast<std::uint8_t>(values[i]);
        tiny.setPixel(i % 4, i / 4, Colour{g, g, g});
    }
    const Histogram th = greyHistogram(tiny);
    const Histogram tc = cumulative(th);
    const LookupTable te = equaliseTable(th);
    for (int v = 0; v < 256; ++v) {
        if (th[v] > 0) {
            std::cout << "value " << padLeft(std::to_string(v), 3) << ": count " << th[v]
                      << ", cumulative " << tc[v] << ", equalised " << static_cast<int>(te[v]) << "\n";
        }
    }
    printStats("tiny", th);

    const Image dull = makeDull();
    const Histogram before = greyHistogram(dull);
    std::cout << "\n";
    printStats("dull", before);
    printBars(before);

    Image stretched = dull;
    applyTable(stretched, autoLevelsTable(before, 0.01));
    const Histogram afterLevels = greyHistogram(stretched);
    std::cout << "\n";
    printStats("auto levels", afterLevels);
    printBars(afterLevels);

    Image equalised = dull;
    applyTable(equalised, equaliseTable(before));
    const Histogram afterEqualise = greyHistogram(equalised);
    std::cout << "\n";
    printStats("equalised", afterEqualise);
    printBars(afterEqualise);

    Image sheet(3 * 276 + 10, 295, colours::white);
    const Image* pictures[3] = {&dull, &stretched, &equalised};
    const Histogram* histograms[3] = {&before, &afterLevels, &afterEqualise};
    const std::string names[3] = {"original", "auto levels (1%)", "equalised"};
    for (int i = 0; i < 3; ++i) {
        const int left = 10 + i * 276;
        drawText(sheet, left, 10, names[i], colours::black);
        for (int y = 0; y < 160; ++y) {
            for (int x = 0; x < 256; ++x) {
                sheet.setPixel(left + 1 + x, 24 + y, pictures[i]->getPixel(x, y));
            }
        }
        drawHistogram(sheet, left, 192, 80, *histograms[i], Colour{60, 60, 60});
    }
    if (!savePNGCompressed(sheet, "histograms.png")) {
        std::cout << "could not write histograms.png\n";
        return 1;
    }
    std::cout << "\nwrote histograms.png\n";
    return 0;
}
```

Build and run it from the `code/ch48` folder:

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common histogram.cpp -o histogram
./histogram
```

### Line by line

**Helpers (lines 1–61)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–5 | the `#include` lines | `std::llround`, printing, strings, the new header, and `deflate.h` for saving. |
| 7–18 | `padLeft` and `oneDecimal` | Columns and one digit after the point (Chapter 43). |
| 20–24 | `Image makeDull() { Image picture(256, 160); for (...) { for (...) { int v = 100 + x / 8 + y / 10;` | A faint gradient from 100 (top left) to 146 (bottom right), in whole numbers. |
| 25–29 | `const int dx = x - 180; const int dy = y - 50; if (dx * dx + dy * dy <= 625) { v += 20; }` | A "sun": a disk of radius 25 (625 = 25²), 20 brighter. |
| 30–33 | `const int slope = (x % 64 < 32) ? x % 32 : 31 - x % 32; if (y > 112 + slope / 2) { v -= 30; }` | Hills: a zigzag line that goes up and down every 32 pixels; below it, 30 darker. |
| 34–39 | `const std::uint8_t g = static_cast<std::uint8_t>(v); picture.setPixel(x, y, Colour{g, g, g}); ... return picture; }` | A grey pixel. All values stay between 81 and 151 — a dull picture on purpose. |
| 41–45 | `void printStats(const std::string& name, const Histogram& h) { ... }` | One line of numbers (Sections 48.3 and 48.4). |
| 47–55 | `void printBars(const Histogram& h) { long long bins[16] = {}; for (...) { bins[v / 16] += h[v]; } long long most = 0; for (long long n : bins) { most = std::max(most, n); }` | Group the 256 counts into 16 bins of 16 values (Section 48.2), and find the biggest bin. |
| 56–61 | `for (int b = 0; b < 16; ++b) { const int length = static_cast<int>((bins[b] * 40 + most / 2) / most); std::cout << ... std::string(length, '#') << " " << bins[b] << "\n"; } }` | A text bar chart: the biggest bin gets 40 `#`s, the others in proportion. |

**The tiny picture (lines 64–79)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 64–69 | `Image tiny(4, 2); const int values[8] = {50, 50, 60, 60, 60, 70, 90, 200}; for (...) { ... tiny.setPixel(i % 4, i / 4, Colour{g, g, g}); }` | The 8 pixels of Section 48.1, row by row. |
| 70–72 | `const Histogram th = greyHistogram(tiny); const Histogram tc = cumulative(th); const LookupTable te = equaliseTable(th);` | Counts, cumulative counts and the equalisation table. |
| 73–79 | `for (...) { if (th[v] > 0) { std::cout << "value " ... } } printStats("tiny", th);` | One line for each used value (Section 48.6), then the numbers. |

**The dull picture, fixed twice (lines 81–99)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 81–85 | `const Image dull = makeDull(); const Histogram before = greyHistogram(dull); ... printStats("dull", before); printBars(before);` | The original and its histogram. |
| 87–92 | `Image stretched = dull; applyTable(stretched, autoLevelsTable(before, 0.01)); const Histogram afterLevels = greyHistogram(stretched); ...` | Automatic levels (Section 48.5), and the new histogram. |
| 94–99 | `Image equalised = dull; applyTable(equalised, equaliseTable(before)); ...` | Equalisation (Section 48.6). Both tables are built from the **original** histogram. |

**The picture file (lines 101–121)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 101–104 | `Image sheet(3 * 276 + 10, 295, colours::white); const Image* pictures[3] = {...}; const Histogram* histograms[3] = {...}; const std::string names[3] = {...};` | Three columns, 276 pixels apart. Pointers let one loop handle all three. |
| 105–114 | `for (...) { const int left = 10 + i * 276; drawText(sheet, left, 10, names[i], colours::black); for (...) { for (...) { sheet.setPixel(left + 1 + x, 24 + y, pictures[i]->getPixel(x, y)); } } drawHistogram(sheet, left, 192, 80, *histograms[i], Colour{60, 60, 60}); }` | Name, picture (one pixel in, so it lines up with the histogram's columns), and histogram underneath. `->` calls a function through a pointer. |
| 115–121 | `if (!savePNGCompressed(sheet, "histograms.png")) { ... }` … `return 0;` `}` | Save it. |

### What you should see

```
value  50: count 2, cumulative 2, equalised 0
value  60: count 3, cumulative 5, equalised 128
value  70: count 1, cumulative 6, equalised 170
value  90: count 1, cumulative 7, equalised 213
value 200: count 1, cumulative 8, equalised 255
tiny: lowest 50, highest 200, mean 80.0, 5 values used, 1% at 50, 99% at 200

dull: lowest 81, highest 151, mean 116.6, 71 values used, 1% at 84, 99% at 149
    0- 15 | 0
   16- 31 | 0
   32- 47 | 0
   48- 63 | 0
   64- 79 | 0
   80- 95 |########## 3892
   96-111 |############################# 11252
  112-127 |######################################## 15329
  128-143 |####################### 8655
  144-159 |##### 1832
  160-175 | 0
  176-191 | 0
  192-207 | 0
  208-223 | 0
  224-239 | 0
  240-255 | 0

auto levels: lowest 0, highest 255, mean 127.7, 66 values used, 1% at 0, 99% at 255
    0- 15 |########### 1364
   16- 31 |############## 1680
   32- 47 |########## 1212
   48- 63 |############ 1396
   64- 79 |#################### 2332
   80- 95 |############################### 3716
   96-111 |######################################## 4756
  112-127 |######################################## 4764
  128-143 |############################### 3748
  144-159 |############################## 3603
  160-175 |###################### 2570
  176-191 |############################# 3462
  192-207 |###################### 2628
  208-223 |############# 1564
  224-239 |####### 837
  240-255 |########### 1328

equalised: lowest 0, highest 255, mean 129.8, 69 values used, 1% at 3, 99% at 254
    0- 15 |################################ 2424
   16- 31 |################################# 2528
   32- 47 |############################## 2268
   48- 63 |################################# 2500
   64- 79 |######################################## 3048
   80- 95 |############################### 2376
   96-111 |################################## 2592
  112-127 |############################### 2392
  128-143 |########################### 2060
  144-159 |#################################### 2780
  160-175 |##################################### 2823
  176-191 |################################### 2682
  192-207 |############################# 2204
  208-223 |#################################### 2734
  224-239 |#################################### 2720
  240-255 |##################################### 2829

wrote histograms.png
```

Every block of bars adds up to 256 × 160 = **40,960** pixels — check one!

---

## Small examples

### Example 1 — A black-and-white picture

A picture after a threshold (Chapter 47) has only two bars: h[0] and h[255]. Its histogram says at once what part is white: h[255] / total.

### Example 2 — The mean of a gradient

A gradient that uses every value 0 … 255 exactly once per row has h[v] = (number of rows) for every v: a perfectly flat histogram, with mean (0 + 255) / 2 = **127.5**.

### Example 3 — A percentile

100 pixels: 10 of value 20, 85 of value 100, 5 of value 250. 1st percentile: 0.01 × 100 = 1 → c[20] = 10 ≥ 1 → **20**. 99th: 99 → c[100] = 95 < 99, c[250] = 100 ≥ 99 → **250**. Here the bright 5 % are not outliers: they are too many to ignore at the 1 % level.

### Example 4 — Equalising an already flat histogram

Every value used equally: c[v] = (v + 1) × k. Then new = (v + 1 − 1) × 255 / 255 = v: the identity. A flat histogram is already "equal".

### Example 5 — Equalising a two-value picture

Half the pixels 100, half 120: c_min = half, so 100 → **0** and 120 → (total − half) × 255 / (total − half) = **255**. Two close greys become black and white: maximum contrast.

---

## Common mistakes

⚠️ **Counting in `int`** — a 50-megapixel photo can overflow small counters in sums like v × h[v]. Use `long long` (or `double` for the sum).

⚠️ **Using the lowest and highest value for levels** — one stray pixel ruins it. Use percentiles.

⚠️ **Building the table from the changed picture** — compute the histogram **before** you change the picture, and build the table from it.

⚠️ **Forgetting the one-value case** — `equaliseTable` would divide by 0. Return the identity.

⚠️ **Expecting new detail** — equalisation and levels only spread out the values that are there. Merged values stay merged.

⚠️ **Integer bars** — `h[v] * height / highest` in whole numbers cuts down; add `highest / 2` first to round.

---

## Practice

🏋️ **1.** Compute the histogram, mean and median of the 6 values 10, 10, 10, 40, 40, 250 by hand.

🏋️ **2.** Equalise the 6 values of Practice 1 by hand. What do 10, 40 and 250 become?

🏋️ **3.** Write `int medianValue(const Histogram& h)` with `percentile`. Compare the median and the mean of the dull picture.

🏋️ **4.** Write `int mostCommonValue(const Histogram& h)` (the "mode": the value with the tallest bar).

🏋️ **5.** Change the clip fraction of auto levels from 0.01 to 0 and to 0.05. What happens to the lowest and highest values, and to the number of used values?

🏋️ **6.** Load a colour PNG. Equalise it in both ways of Section 48.8. Save both and compare the colours.

🏋️ **7.** Draw the three channel histograms of a colour picture on top of each other, in red, green and blue, with `drawHistogram`. (Hint: draw them into three separate pictures, or change `drawHistogram` to draw only the top pixel of each bar.)

🏋️ **8.** Why can't equalisation make a truly flat histogram for the tiny picture of Section 48.1, however you choose the table?

---

## Answers

**1.**
> h[10] = 3, h[40] = 2, h[250] = 1. Mean = (30 + 80 + 250) / 6 = 360 / 6 = **60**. Median: 0.5 × 6 = 3 → c[10] = 3 ≥ 3 → **10**.

**2.**
> c[10] = 3, c[40] = 5, c[250] = 6; c_min = 3, total − c_min = 3.
> 10 → **0**; 40 → (5 − 3) × 255 / 3 = **170**; 250 → **255**.

**3.**

```cpp
int medianValue(const Histogram& h) {
    return percentile(h, 0.5);
}
```

> For the dull picture, the median is **116** and the mean 116.6: almost the same, because its histogram is a fairly even hill with no big outliers.

**4.**

```cpp
int mostCommonValue(const Histogram& h) {
    int best = 0;
    for (int v = 1; v < 256; ++v) {
        if (h[v] > h[best]) {
            best = v;
        }
    }
    return best;
}
```

**5.**
> With 0, the levels are the lowest and highest values (81 … 151): nothing is clipped, all 71 values stay, but the stretch is a little weaker. With 0.05, the levels move inwards: the stretch is stronger, and more pixels at both ends are clipped (fewer used values).

**6.**

```cpp
Image photo(0, 0);
if (loadPNGFull("photo.png", photo)) {
    Image a = photo;
    applyTable(a, equaliseTable(greyHistogram(photo)));
    Image b = photo;
    applyTables(b, equaliseTable(channelHistogram(photo, 0)), equaliseTable(channelHistogram(photo, 1)),
                equaliseTable(channelHistogram(photo, 2)));
    savePNGCompressed(a, "equal_grey.png");
    savePNGCompressed(b, "equal_channels.png");
}
```

**7.**
> One way: copy `drawHistogram`, and instead of a full bar draw only one pixel at the top of each bar (`fillRect` of height 1 at `y + 1 + height - bar`). Call it three times on the same picture with the three channel histograms and three colours.

**8.**
> A point operation sends **all** pixels with the same old value to the same new value. The tiny picture has 3 pixels of value 60; they must stay together in one bar of height 3, while the value 70 has only 1 pixel. No table can split the bar of 3. Equalisation can only spread the bars apart — it makes the histogram flat **on average**, not bar by bar.

---

## Summary

🧠 A **histogram** counts the pixels of each value; its counts add up to the number of pixels. It shows dark, bright, low-contrast and clipped pictures at a glance — but not **where** the values are.

🧠 From it we get the **lowest/highest** values, the **mean** (Σ v × h[v] / total) and **percentiles** (from the **cumulative** counts).

🧠 **Auto levels** = levels between the 1st and 99th percentiles: it ignores **outliers**.

🧠 **Equalisation**: new = (c[v] − c_min) × 255 / (total − c_min). Common values get spread apart, rare ones squeezed: the histogram becomes flat **on average**.

🧠 Point operations can **merge** values, never split them: no new detail appears.

---

## Next chapter

Point operations see one pixel at a time. To **blur**, **sharpen** or find **edges**, a pixel must look at its **neighbours**. In Chapter 49 we meet the tool behind all of these: **convolution** — sliding a small grid of numbers (a **kernel**) over the picture and adding up "neighbour × weight". We will work through it slowly with small numbers, and handle the pixels at the edges of the picture.
