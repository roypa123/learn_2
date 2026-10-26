# Chapter 54 — Making Our Own Random Numbers

> **Part 8 · Chapter 54 of 82**
> **You need:** Chapters 1–53 (especially 4, 27 and 39) · **You will make:** `random.h` (two random number generators, random doubles, ranges and whole numbers, a hash that gives a fixed random value to any (x, y), jittered sample positions, white noise), and `random.png`: three "pair pictures" that test generators, white noise, a random value per square, and a sky of stars

---

## What you will learn

- How a computer, which always does exactly what it is told, can make numbers that **look** random.
- How Chapter 39's little formula — the **linear congruential generator** — works, and where it is weak.
- A better generator, **xorshift**, made only of shifts and XOR.
- How to turn raw 32-bit numbers into doubles from 0 to 1, ranges, and dice rolls.
- How to **test** a generator with counts and with a picture.
- A **hash**: a random value that belongs to a position (x, y) — the key tool for the next chapters.
- **Jittered** sampling, which Chapter 27 promised for smoother nearly-flat edges.

---

## New words in this chapter

| Word | Simple meaning |
|---|---|
| **pseudo-random** | Made by a fixed rule, but looking random. |
| **seed** | The starting number of a generator. The same seed gives the same numbers. |
| **state** | The number a generator keeps, and changes, at each step. |
| **period** | How many numbers come out before the list starts repeating. |
| **LCG** | Linear congruential generator: state = state × a + c, wrapped at 2³². |
| **XOR** | "Exclusive or": a bit is 1 where exactly one of two bits is 1. |
| **xorshift** | A generator made of three shift-and-XOR steps. |
| **hash** | A function that scrambles its input into a random-looking number — always the same for the same input. |
| **jitter** | A small random move of a sample point inside its cell. |

---

## 54.1 Why pictures need random numbers

Part 8 makes pictures from maths. Many natural things look **random**: stars in the sky, the grain of wood, clouds, sand, the speckles on an egg. To draw them we need numbers that look like nobody chose them.

C++ has a ready-made `<random>` library. Chapter 1 promised we would not use it: we want to see how random numbers are **made**. It is surprisingly little code.

📖 **New word: pseudo-random** — a computer cannot toss a coin. It can only follow rules. But a clever rule can make a list of numbers with no pattern that you (or a picture) can notice. "Pseudo" means "pretend". Pseudo-random numbers are actually **better** for pictures than truly random ones: run the program again, and you get exactly the same picture.

Every generator in this chapter works the same way:

> 1. Keep one number, the **state**.
> 2. To get the next random number: change the state with a fixed rule, and give it out.

📖 **New words: state, seed** — the state is the generator's memory. The **seed** is the state you start with. The same seed always gives the same list.

---

## 54.2 Chapter 39's generator: the LCG

Chapter 39 made its noisy test picture with this line:

```
seed = seed * 1103515245u + 12345u;
```

📖 **New word: LCG** — a **linear congruential generator**: multiply the state by a number a, add a number c, and keep only the remainder after dividing by m.

> **next = (a × state + c) mod m**, with a = 1,103,515,245, c = 12,345, m = 2³²

We never write "mod 2³²" in the code: a `std::uint32_t` (or `unsigned int`) holds only 32 bits, so anything above 2³² simply falls off — unsigned numbers wrap around safely (Chapter 4). The wrapping **is** the mod.

🔢 **Maths: a tiny LCG by hand**

With small numbers you can see what happens. Take a = 5, c = 3, m = 16, seed 1:

> 5 × 1 + 3 = 8 → **8**
> 5 × 8 + 3 = 43 → 43 mod 16 = **11**
> 5 × 11 + 3 = 58 → 58 mod 16 = **10**
> 5 × 10 + 3 = 53 → **5**, then 12, 15, 14, 9, 0, 3, 2, 13, 4, 7, 6, and back to **1**

All 16 numbers 0 … 15 come out once, in a jumbled order, then the list repeats.

📖 **New word: period** — the length of the list before it repeats. Here 16, the most possible. Chapter 39's LCG also has the most possible period, 2³² = 4,294,967,296: its a and c were chosen so (c must be odd, and a − 1 must be a multiple of 4).

The program prints the first numbers from the seed 12345:

```
Chapter 39's generator from 12345: 3554416254 2802067423 3596950572 229283573
  top 8 bits (the greys of Chapter 39): 211 167 214 13
```

Chapter 39 used the **top** 8 bits (`seed >> 24`) as its grey values: 211, 167, 214, 13 … That was a good choice, and here is why.

---

## 54.3 The weak spot: the low bits

Look at the **lowest** bit of each number (`& 1`, Chapter 4):

```
  lowest bit of the first 16: 0101010101010101
```

It just goes 0, 1, 0, 1 … — the least random thing imaginable!

🔢 **Maths: why the lowest bit flips**

> a = 1,103,515,245 is odd and c = 12,345 is odd.
> If the state is even: odd × even = even, + odd = **odd**.
> If the state is odd: odd × odd = odd, + odd = **even**.
> So the state is odd, even, odd, even … for ever.

The same thing happens, more slowly, in the other low bits: the lowest k bits of an LCG repeat after only 2^k steps. The lowest 8 bits (`& 255`) repeat after 256 steps. The high bits are much better, because they are mixed by the carries from all the bits below them.

**A test with pairs.** Take numbers two at a time, (first, second), as bytes 0 … 255. There are 256 × 256 = 65,536 possible pairs. Draw 65,536 pairs and count how many **different** pairs appear:

```
different pairs among 65536 pairs of bytes: low bits of Chapter 39's 128, its top bits 41308, xorshift 41420
```

- **Low bits: only 128.** They repeat every 256 numbers, which is just 128 pairs, again and again.
- **Top bits: 41,308.** What should a perfect generator give? Throwing 65,536 pairs at random into 65,536 boxes leaves some boxes empty and fills some twice: we expect about 65,536 × (1 − 1/e) ≈ **41,427** different pairs (e = 2.718…, Chapter 50). 41,308 is close.

In `random.png`, the "pairs" pictures plot each pair as a dot at (first, second). The low bits make only 128 dots, lined up in **straight rows** — a pattern your eye spots at once. The top bits make an even sprinkle with no pattern.

🧠 **Rule:** from an LCG, use the **top** bits only.

---

## 54.4 A better generator: xorshift

📖 **New word: XOR** — the "exclusive or" of two bits is 1 when exactly **one** of them is 1:

```
   0 ^ 0 = 0     0 ^ 1 = 1     1 ^ 0 = 1     1 ^ 1 = 0
```

For whole numbers, C++'s `^` does this to every bit pair (Chapter 4 showed `&` and `|`; `^` is their cousin).

📖 **New word: xorshift** — George Marsaglia's generator (2003). Three steps, each "shift a copy of the state and XOR it in":

```
state ^= state << 13;
state ^= state >> 17;
state ^= state << 5;
```

🔢 **Maths: what one step does**

> `state << 13` moves every bit 13 places to the left (the top 13 fall off).
> XOR-ing that into the state mixes each bit with the bit 13 places below it.
> `>> 17` then mixes in bits from 17 places above; `<< 5` from 5 below.
> After the three steps, every bit depends on many bits of the old state — high bits and low bits alike.

It has period 2³² − 1: it visits every 32-bit number **except 0**. (Practice 6: why not 0?) So the seed must not be 0; `makeRandom` swaps a 0 seed for another number.

```
xorshift from 12345: 3336926330 1697253807 2816511904 1955480042
  lowest bit of the first 16: 0100100000010110
```

The lowest bit now looks random, and the pair test gives 41,420 — very close to the 41,427 of a perfect generator. Xorshift is what `nextNumber` uses from now on.

💡 Xorshift is not perfect either (experts have stronger tests it fails), but for pictures it is excellent — and it is only three lines.

---

## 54.5 Useful shapes of random numbers

Raw 32-bit numbers are not what pictures need. We need:

**A double from 0 to 1** (`randomDouble`):

> take the top 24 bits: nextNumber >> 8 gives 0 … 16,777,215
> divide by 2²⁴ = 16,777,216 → a value from 0 up to (but never reaching) 1

Why 24 bits? A `double` holds 53 bits of precision, so 24 fit exactly, and every result is a whole number of 1 / 16,777,216 steps — evenly spaced. And it can never be exactly 1, which keeps the next two functions safe.

**A double in a range** (`randomRange(r, low, high)`): low + (high − low) × randomDouble — Chapter 13's lerp!

**A whole number from low to high, both included** (`randomInt`):

> low + ⌊randomDouble × (high − low + 1)⌋
> For a die (1 … 6): randomDouble × 6 is 0 … 5.999…, the whole part is 0 … 5, plus 1 → **1 … 6**.

Because randomDouble is never 1, the result is never high + 1.

🔢 **The program's checks**

```
100000 random doubles: average 0.4996, per tenth: 10116 10084 9763 10105 9985 9878 10175 9978 9904 10012
6000 dice rolls, ones to sixes: 1001 958 991 1062 1015 973
```

> The average of evenly spread values from 0 to 1 should be 0.5 → 0.4996 ✓.
> Each tenth (0 … 0.1, 0.1 … 0.2, …) should get about 10,000 of the 100,000 → all between 9,763 and 10,175 ✓.
> Each face of the die should come up about 1,000 times in 6,000 rolls → 958 … 1,062 ✓.

⚠️ **Why not exactly 10,000 each?** Real randomness is never perfectly even. If a generator gave exactly 10,000 in every tenth every time, that would be suspicious! Differences of about √10,000 = 100 are normal.

---

## 54.6 A random value for each position: hashing

A generator gives a **list**: the 1st number, the 2nd, the 3rd… Sometimes we need something different: a random value that **belongs to a place**. The next chapter (value noise) puts a random value on every corner of a grid, and must be able to ask "what is the value at corner (3, 7)?" — at any time, in any order, and get the **same** answer each time.

📖 **New word: hash** — a function that **scrambles** its input into a random-looking number. Same input → same output; a slightly different input → a completely different output.

Our `hash2(x, y, seed)`:

```
h = seed + x × 374761393 + y × 668265263     (wrapping at 2³²)
h = (h ^ (h >> 13)) × 1274126177
h = h ^ (h >> 16)
```

The big odd multipliers spread x and y over all 32 bits; the shift-XORs mix the high bits back down into the low ones (like xorshift). `hashDouble` turns the result into 0 … 1, exactly like `randomDouble`.

```
hash of (3, 7): 0.7641, again 0.7641, hash of (4, 7): 0.4679
```

The same corner gives the same value; its neighbour gives a completely different one. In `random.png`, "hash per square" gives every 16 × 16 square its own random grey, from `hashDouble(x / 16, y / 16, 1)`. Change the seed (the last number) and you get a new, different pattern.

---

## 54.7 Jittered samples

Chapter 27 (Section 27.4) found a weak spot in supersampling: on a **nearly flat** edge, all 4 samples in one row of the 4 × 4 grid are at the same height, so they go in or out together. The coverage then only takes 5 values — 0, 4, 8, 12 or 16 samples — and the edge shows small steps. Chapter 27 promised a fix with random numbers.

📖 **New word: jitter** — keep the 4 × 4 cells, but put each sample at a **random** place inside its cell instead of at the cell's centre:

> grid: offset = (i + 0.5) / n (Chapter 27's `sampleOffset`)
> jittered: offset = (i + randomDouble) / n (`jitteredOffset`)

Every sample stays in its own cell, so the samples are still spread over the pixel. But no two of them are at exactly the same height any more.

🔢 **The test.** The program takes the edge y = 5 + 0.025 x — rising only 1 pixel over 40 pixels — and the pixels of row 5, x = 0 … 39. The part **below** the edge is "inside". The exact number of samples inside is 16 × (1 − 0.025 × (x + 0.5)):

```
nearly flat edge, samples inside (of 16), first 10 pixels:
  exact:    15.8 15.4 15.0 14.6 14.2 13.8 13.4 13.0 12.6 12.2
  grid:     16 16 16 16 16 12 12 12 12 12
  jittered: 16 16 15 16 14 15 14 12 12 12
over 40 pixels: different values used: grid 5, jittered 15; average error: grid 1.0, jittered 0.6 samples
```

The grid jumps from 16 straight to 12: a visible **step**. The jittered samples follow the real slope much more closely — not perfectly (15, 16, 14 go up and down a little), but with 15 different values instead of 5, and a smaller average error. Its mistakes are small and random; the eye sees fine **noise** instead of steps, and minds it much less.

---

## 54.8 A sky of stars

The last tile of `random.png` uses everything at once: 300 stars, each at a random x and y (`randomInt(sky, 0, 255)`) with a random brightness (100 … 255), on a dark blue background. Change the seed 2024 and the sky changes; keep it, and you get the same sky every time.

---

## Code, part 1: `random.h`

File: `common/random.h` (new). It includes `warp.h` (and through it Chapters 1–53: `Image`, `Colour`, and everything else).

```cpp
#ifndef RANDOM_H
#define RANDOM_H

#include <cstdint>
#include "warp.h"

inline std::uint32_t lcgNext(std::uint32_t& state) {
    state = state * 1103515245u + 12345u;
    return state;
}

inline std::uint32_t xorshiftNext(std::uint32_t& state) {
    state ^= state << 13;
    state ^= state >> 17;
    state ^= state << 5;
    return state;
}

struct Random {
    std::uint32_t state = 2463534242u;
};

inline Random makeRandom(std::uint32_t seed) {
    return Random{(seed == 0) ? 2463534242u : seed};
}

inline std::uint32_t nextNumber(Random& r) {
    return xorshiftNext(r.state);
}

inline double randomDouble(Random& r) {
    return (nextNumber(r) >> 8) / 16777216.0;
}

inline double randomRange(Random& r, double low, double high) {
    return low + (high - low) * randomDouble(r);
}

inline int randomInt(Random& r, int low, int high) {
    return low + static_cast<int>(randomDouble(r) * (high - low + 1));
}

inline std::uint32_t hash2(int x, int y, std::uint32_t seed) {
    std::uint32_t h = seed + static_cast<std::uint32_t>(x) * 374761393u +
                      static_cast<std::uint32_t>(y) * 668265263u;
    h = (h ^ (h >> 13)) * 1274126177u;
    return h ^ (h >> 16);
}

inline double hashDouble(int x, int y, std::uint32_t seed) {
    return (hash2(x, y, seed) >> 8) / 16777216.0;
}

inline double jitteredOffset(int i, int n, Random& r) {
    return (i + randomDouble(r)) / n;
}

inline Image whiteNoise(int width, int height, Random& r) {
    Image noise(width, height);
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            const std::uint8_t v = static_cast<std::uint8_t>(nextNumber(r) >> 24);
            noise.setPixel(x, y, Colour{v, v, v});
        }
    }
    return noise;
}

#endif
```

### Line by line

**Two generators (lines 1–29)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–5 | include guard and `#include` lines | `std::uint32_t`, and Chapter 53's header. |
| 7–10 | `inline std::uint32_t lcgNext(std::uint32_t& state) { state = state * 1103515245u + 12345u; return state; }` | Chapter 39's LCG (Section 54.2). `state` is a reference, so the caller's state changes. The `u` makes the numbers unsigned, so the wrap-around is safe. |
| 12–17 | `inline std::uint32_t xorshiftNext(std::uint32_t& state) { state ^= state << 13; state ^= state >> 17; state ^= state << 5; return state; }` | Marsaglia's xorshift (Section 54.4). `a ^= b` means `a = a ^ b`. |
| 19–21 | `struct Random { std::uint32_t state = 2463534242u; };` | A generator object: just its state. The default state is the starting value from Marsaglia's paper. |
| 23–25 | `inline Random makeRandom(std::uint32_t seed) { return Random{(seed == 0) ? 2463534242u : seed}; }` | A generator from a seed. A seed of 0 would stay 0 for ever, so it is replaced. |
| 27–29 | `inline std::uint32_t nextNumber(Random& r) { return xorshiftNext(r.state); }` | The next raw 32-bit number. |

**Useful shapes (lines 31–41)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 31–33 | `inline double randomDouble(Random& r) { return (nextNumber(r) >> 8) / 16777216.0; }` | The top 24 bits, divided by 2²⁴: 0 ≤ value < 1 (Section 54.5). The `.0` makes it a double division. |
| 35–37 | `inline double randomRange(Random& r, double low, double high) { return low + (high - low) * randomDouble(r); }` | A double from `low` up to `high`. |
| 39–41 | `inline int randomInt(Random& r, int low, int high) { return low + static_cast<int>(randomDouble(r) * (high - low + 1)); }` | A whole number from `low` to `high`, both included. `static_cast<int>` cuts off the fraction (for positive values that is ⌊ ⌋). |

**Hashing (lines 43–52)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 43–45 | `inline std::uint32_t hash2(int x, int y, std::uint32_t seed) { std::uint32_t h = seed + static_cast<std::uint32_t>(x) * 374761393u + static_cast<std::uint32_t>(y) * 668265263u;` | Spread x and y over all 32 bits (Section 54.6). The casts make negative x and y work too: they wrap to big unsigned numbers. |
| 46–48 | `h = (h ^ (h >> 13)) * 1274126177u; return h ^ (h >> 16); }` | Mix the bits twice. |
| 50–52 | `inline double hashDouble(int x, int y, std::uint32_t seed) { return (hash2(x, y, seed) >> 8) / 16777216.0; }` | The hash as a double 0 … 1. |

**Samples and noise (lines 54–69)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 54–56 | `inline double jitteredOffset(int i, int n, Random& r) { return (i + randomDouble(r)) / n; }` | A random position inside cell i of n (Section 54.7). |
| 58–67 | `inline Image whiteNoise(int width, int height, Random& r) { ... const std::uint8_t v = static_cast<std::uint8_t>(nextNumber(r) >> 24); noise.setPixel(x, y, Colour{v, v, v}); ... }` | Every pixel its own random grey, from the top 8 bits. "White noise" because it has every kind of detail, fine and coarse, equally (like white light has every colour). |
| 69 | `#endif` | End of the include guard. |

---

## Code, part 2: testing random numbers

File: `ch54/random.cpp`

```cpp
#include <cmath>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>
#include "random.h"
#include "deflate.h"

std::string fourDecimals(double v) {
    const long long n = std::llround(v * 10000.0);
    std::string digits = std::to_string(n % 10000);
    while (digits.size() < 4) {
        digits = "0" + digits;
    }
    return std::to_string(n / 10000) + "." + digits;
}

std::string oneDecimal(double v) {
    const long long n = std::llround(v * 10.0);
    return std::to_string(n / 10) + "." + std::to_string(n % 10);
}

const int kLowLcg = 0;
const int kTopLcg = 1;
const int kTopXorshift = 2;

int nextByte(int kind, std::uint32_t& state) {
    if (kind == kLowLcg) {
        return static_cast<int>(lcgNext(state) & 255u);
    }
    if (kind == kTopLcg) {
        return static_cast<int>(lcgNext(state) >> 24);
    }
    return static_cast<int>(xorshiftNext(state) >> 24);
}

int differentPairs(int kind) {
    std::vector<bool> seen(256 * 256, false);
    std::uint32_t state = 12345;
    int count = 0;
    for (int i = 0; i < 65536; ++i) {
        const int a = nextByte(kind, state);
        const int b = nextByte(kind, state);
        if (!seen[a * 256 + b]) {
            seen[a * 256 + b] = true;
            ++count;
        }
    }
    return count;
}

Image pairPlot(int kind) {
    Image plot(256, 256);
    std::uint32_t state = 12345;
    for (int i = 0; i < 20000; ++i) {
        const int a = nextByte(kind, state);
        const int b = nextByte(kind, state);
        plot.setPixel(a, b, colours::white);
    }
    return plot;
}

bool belowEdge(double x, double y) {
    return y > 5.0 + 0.025 * x;
}

int countDifferent(const std::vector<int>& values) {
    std::vector<bool> seen(17, false);
    int count = 0;
    for (int v : values) {
        if (!seen[v]) {
            seen[v] = true;
            ++count;
        }
    }
    return count;
}

int main() {
    std::uint32_t state = 12345;
    std::cout << "Chapter 39's generator from 12345:";
    for (int i = 0; i < 4; ++i) {
        std::cout << " " << lcgNext(state);
    }
    state = 12345;
    std::cout << "\n  top 8 bits (the greys of Chapter 39):";
    for (int i = 0; i < 4; ++i) {
        std::cout << " " << (lcgNext(state) >> 24);
    }
    state = 12345;
    std::cout << "\n  lowest bit of the first 16: ";
    for (int i = 0; i < 16; ++i) {
        std::cout << (lcgNext(state) & 1u);
    }
    state = 12345;
    std::cout << "\nxorshift from 12345:";
    for (int i = 0; i < 4; ++i) {
        std::cout << " " << xorshiftNext(state);
    }
    state = 12345;
    std::cout << "\n  lowest bit of the first 16: ";
    for (int i = 0; i < 16; ++i) {
        std::cout << (xorshiftNext(state) & 1u);
    }
    std::cout << "\n\ndifferent pairs among 65536 pairs of bytes: low bits of Chapter 39's "
              << differentPairs(kLowLcg) << ", its top bits " << differentPairs(kTopLcg)
              << ", xorshift " << differentPairs(kTopXorshift) << "\n";

    Random r = makeRandom(1);
    std::vector<int> buckets(10, 0);
    double sum = 0.0;
    for (int i = 0; i < 100000; ++i) {
        const double v = randomDouble(r);
        sum += v;
        ++buckets[static_cast<int>(v * 10.0)];
    }
    std::cout << "\n100000 random doubles: average " << fourDecimals(sum / 100000.0) << ", per tenth:";
    for (int b : buckets) {
        std::cout << " " << b;
    }
    std::vector<int> dice(7, 0);
    for (int i = 0; i < 6000; ++i) {
        ++dice[randomInt(r, 1, 6)];
    }
    std::cout << "\n6000 dice rolls, ones to sixes:";
    for (int face = 1; face <= 6; ++face) {
        std::cout << " " << dice[face];
    }
    std::cout << "\nhash of (3, 7): " << fourDecimals(hashDouble(3, 7, 1)) << ", again "
              << fourDecimals(hashDouble(3, 7, 1)) << ", hash of (4, 7): "
              << fourDecimals(hashDouble(4, 7, 1)) << "\n";

    Random jitter = makeRandom(7);
    std::vector<int> grid;
    std::vector<int> jittered;
    double gridError = 0.0;
    double jitterError = 0.0;
    for (int x = 0; x < 40; ++x) {
        int inGrid = 0;
        int inJitter = 0;
        for (int j = 0; j < 4; ++j) {
            for (int i = 0; i < 4; ++i) {
                inGrid += belowEdge(x + sampleOffset(i, 4), 5 + sampleOffset(j, 4)) ? 1 : 0;
                const double jx = x + jitteredOffset(i, 4, jitter);
                const double jy = 5 + jitteredOffset(j, 4, jitter);
                inJitter += belowEdge(jx, jy) ? 1 : 0;
            }
        }
        const double exact = 16.0 * (1.0 - 0.025 * (x + 0.5));
        grid.push_back(inGrid);
        jittered.push_back(inJitter);
        gridError += std::fabs(inGrid - exact);
        jitterError += std::fabs(inJitter - exact);
    }
    std::cout << "\nnearly flat edge, samples inside (of 16), first 10 pixels:\n  exact:   ";
    for (int x = 0; x < 10; ++x) {
        std::cout << " " << oneDecimal(16.0 * (1.0 - 0.025 * (x + 0.5)));
    }
    std::cout << "\n  grid:    ";
    for (int x = 0; x < 10; ++x) {
        std::cout << " " << grid[x];
    }
    std::cout << "\n  jittered:";
    for (int x = 0; x < 10; ++x) {
        std::cout << " " << jittered[x];
    }
    std::cout << "\nover 40 pixels: different values used: grid " << countDifferent(grid)
              << ", jittered " << countDifferent(jittered) << "; average error: grid "
              << oneDecimal(gridError / 40.0)
              << ", jittered " << oneDecimal(jitterError / 40.0) << " samples\n";

    Random sky = makeRandom(2024);
    Image stars(256, 256, Colour{10, 10, 30});
    for (int i = 0; i < 300; ++i) {
        const int x = randomInt(sky, 0, 255);
        const int y = randomInt(sky, 0, 255);
        const std::uint8_t v = static_cast<std::uint8_t>(randomInt(sky, 100, 255));
        stars.setPixel(x, y, Colour{v, v, v});
    }
    Image blocks(256, 256);
    for (int y = 0; y < 256; ++y) {
        for (int x = 0; x < 256; ++x) {
            const std::uint8_t v = static_cast<std::uint8_t>(hashDouble(x / 16, y / 16, 1) * 255.0);
            blocks.setPixel(x, y, Colour{v, v, v});
        }
    }
    Random noiseRandom = makeRandom(99);
    const Image tiles[6] = {pairPlot(kLowLcg), pairPlot(kTopLcg), pairPlot(kTopXorshift),
                            whiteNoise(256, 256, noiseRandom), blocks, stars};
    const std::string names[6] = {"pairs: low bits", "pairs: top bits", "pairs: xorshift",
                                  "white noise", "hash per square", "stars"};
    Image sheet(3 * 266 + 10, 2 * 280 + 10, colours::white);
    for (int i = 0; i < 6; ++i) {
        const int left = 10 + (i % 3) * 266;
        const int top = 10 + (i / 3) * 280;
        for (int y = 0; y < 256; ++y) {
            for (int x = 0; x < 256; ++x) {
                sheet.setPixel(left + x, top + y, tiles[i].getPixel(x, y));
            }
        }
        drawText(sheet, left, top + 260, names[i], colours::black);
    }
    if (!savePNGCompressed(sheet, "random.png")) {
        std::cout << "could not write random.png\n";
        return 1;
    }
    std::cout << "wrote random.png\n";
    return 0;
}
```

Build and run it from the `code/ch54` folder:

```
g++ -std=c++17 -Wall -Wextra -O2 -I ../common random.cpp -o random
./random
```

### Line by line

**Helpers (lines 1–77)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 1–7 | the `#include` lines | `std::llround` and `std::fabs`, `std::uint32_t`, printing, strings, lists, the new header, and `deflate.h`. |
| 9–21 | `std::string fourDecimals(double v) { ... }` and `std::string oneDecimal(double v) { ... }` | Fixed numbers of decimals (as in Chapters 50 and 51). |
| 23–25 | `const int kLowLcg = 0; const int kTopLcg = 1; const int kTopXorshift = 2;` | Names for the three byte sources we test. |
| 27–35 | `int nextByte(int kind, std::uint32_t& state) { if (kind == kLowLcg) { return static_cast<int>(lcgNext(state) & 255u); } if (kind == kTopLcg) { return static_cast<int>(lcgNext(state) >> 24); } return static_cast<int>(xorshiftNext(state) >> 24); }` | One byte (0 … 255): the lowest 8 bits of the LCG, its top 8 bits, or the top 8 bits of xorshift. |
| 37–50 | `int differentPairs(int kind) { std::vector<bool> seen(256 * 256, false); std::uint32_t state = 12345; int count = 0; for (int i = 0; i < 65536; ++i) { const int a = nextByte(kind, state); const int b = nextByte(kind, state); if (!seen[a * 256 + b]) { seen[a * 256 + b] = true; ++count; } } return count; }` | The pair test of Section 54.3. `seen` has one box per possible pair; we count the boxes filled for the first time. `a` and `b` are read in two separate lines, so their order is certain. |
| 52–61 | `Image pairPlot(int kind) { Image plot(256, 256); ... plot.setPixel(a, b, colours::white); ... }` | The same pairs as white dots on black: 20,000 of them. |
| 63–65 | `bool belowEdge(double x, double y) { return y > 5.0 + 0.025 * x; }` | Is a point below the nearly flat edge of Section 54.7? |
| 67–77 | `int countDifferent(const std::vector<int>& values) { std::vector<bool> seen(17, false); ... }` | How many different sample counts (0 … 16) appear in a list. |

**Generators and the pair test (lines 80–107)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 80–89 | `std::uint32_t state = 12345; ... lcgNext(state) ... state = 12345; ... (lcgNext(state) >> 24) ...` | Four LCG numbers from 12345, then (after resetting the state to the same seed) the same four numbers' top bytes — Chapter 39's first greys. |
| 90–104 | `... (lcgNext(state) & 1u) ... xorshiftNext(state) ... (xorshiftNext(state) & 1u) ...` | The lowest bits of both generators, and xorshift's first numbers. Each part starts again from the seed 12345. |
| 105–107 | `std::cout << ... differentPairs(kLowLcg) << ... differentPairs(kTopLcg) << ... differentPairs(kTopXorshift) << "\n";` | The three pair counts. |

**Shapes and the hash (lines 109–131)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 109–120 | `Random r = makeRandom(1); std::vector<int> buckets(10, 0); double sum = 0.0; for (int i = 0; i < 100000; ++i) { const double v = randomDouble(r); sum += v; ++buckets[static_cast<int>(v * 10.0)]; } ...` | 100,000 doubles: their average, and how many fall in each tenth. v × 10 is 0 … 9.99…, so the bucket is 0 … 9 (never 10, because v < 1). |
| 121–128 | `std::vector<int> dice(7, 0); for (int i = 0; i < 6000; ++i) { ++dice[randomInt(r, 1, 6)]; } ...` | 6,000 dice rolls. `dice` has 7 boxes so that `dice[6]` exists; box 0 is not used. |
| 129–131 | `std::cout << "\nhash of (3, 7): " << fourDecimals(hashDouble(3, 7, 1)) << ...` | The same corner twice, and its neighbour (Section 54.6). |

**Jittered samples (lines 133–170)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 133–137 | `Random jitter = makeRandom(7); std::vector<int> grid; std::vector<int> jittered; double gridError = 0.0; double jitterError = 0.0;` | A generator for the jitter, the results, and the total errors. |
| 138–148 | `for (int x = 0; x < 40; ++x) { ... inGrid += belowEdge(x + sampleOffset(i, 4), 5 + sampleOffset(j, 4)) ? 1 : 0; const double jx = x + jitteredOffset(i, 4, jitter); const double jy = 5 + jitteredOffset(j, 4, jitter); inJitter += belowEdge(jx, jy) ? 1 : 0; ... }` | For each pixel (x, 5): count the 16 grid samples and the 16 jittered samples below the edge. jx and jy are computed on separate lines, so the random numbers are used in a known order. |
| 149–154 | `const double exact = 16.0 * (1.0 - 0.025 * (x + 0.5)); grid.push_back(inGrid); jittered.push_back(inJitter); gridError += std::fabs(inGrid - exact); jitterError += std::fabs(inJitter - exact); }` | The true count (the edge crosses the pixel's middle at 5 + 0.025 (x + 0.5), and the inside part is the rest of the pixel), and the errors. |
| 155–170 | `std::cout << ... oneDecimal(16.0 * (1.0 - 0.025 * (x + 0.5))) ... grid[x] ... jittered[x] ... countDifferent(grid) ... oneDecimal(gridError / 40.0) ...` | Print the first 10 pixels, then the summary over all 40. |

**Stars, squares and the picture (lines 172–209)**

| Line | Code | What it does, in simple words |
|---|---|---|
| 172–179 | `Random sky = makeRandom(2024); Image stars(256, 256, Colour{10, 10, 30}); for (int i = 0; i < 300; ++i) { const int x = randomInt(sky, 0, 255); const int y = randomInt(sky, 0, 255); const std::uint8_t v = ...randomInt(sky, 100, 255)...; stars.setPixel(x, y, Colour{v, v, v}); }` | 300 stars (Section 54.8). |
| 180–186 | `Image blocks(256, 256); for (y) { for (x) { const std::uint8_t v = static_cast<std::uint8_t>(hashDouble(x / 16, y / 16, 1) * 255.0); ... } }` | One hashed grey per 16 × 16 square: x / 16 is the same for 16 pixels in a row. |
| 187–191 | `Random noiseRandom = makeRandom(99); const Image tiles[6] = {pairPlot(kLowLcg), pairPlot(kTopLcg), pairPlot(kTopXorshift), whiteNoise(256, 256, noiseRandom), blocks, stars}; const std::string names[6] = {...};` | The six tiles and their names. |
| 192–209 | `Image sheet(3 * 266 + 10, 2 * 280 + 10, colours::white); for (...) { ... drawText(sheet, left, top + 260, names[i], colours::black); } if (!savePNGCompressed(sheet, "random.png")) { ... }` … `return 0;` `}` | A 3 × 2 sheet of 256 × 256 tiles, and save it. |

### What you should see

```
Chapter 39's generator from 12345: 3554416254 2802067423 3596950572 229283573
  top 8 bits (the greys of Chapter 39): 211 167 214 13
  lowest bit of the first 16: 0101010101010101
xorshift from 12345: 3336926330 1697253807 2816511904 1955480042
  lowest bit of the first 16: 0100100000010110

different pairs among 65536 pairs of bytes: low bits of Chapter 39's 128, its top bits 41308, xorshift 41420

100000 random doubles: average 0.4996, per tenth: 10116 10084 9763 10105 9985 9878 10175 9978 9904 10012
6000 dice rolls, ones to sixes: 1001 958 991 1062 1015 973
hash of (3, 7): 0.7641, again 0.7641, hash of (4, 7): 0.4679

nearly flat edge, samples inside (of 16), first 10 pixels:
  exact:    15.8 15.4 15.0 14.6 14.2 13.8 13.4 13.0 12.6 12.2
  grid:     16 16 16 16 16 12 12 12 12 12
  jittered: 16 16 15 16 14 15 14 12 12 12
over 40 pixels: different values used: grid 5, jittered 15; average error: grid 1.0, jittered 0.6 samples
wrote random.png
```

In `random.png`:

- **pairs: low bits** — only 128 dots, lined up in neat rows: an obvious pattern.
- **pairs: top bits** and **pairs: xorshift** — an even sprinkle of dots all over the square, no pattern.
- **white noise** — grey "TV snow".
- **hash per square** — a 16 × 16 board of random greys.
- **stars** — a dark sky with 300 stars of different brightness.

---

## Small examples

### Example 1 — The next LCG number by hand

From state 0: 0 × 1,103,515,245 + 12,345 = **12,345**. (That is why "seed 12345" and "the number after 0" are the same thing.)

### Example 2 — An XOR

12 ^ 10: 1100 ^ 1010 = **0110** = 6.

### Example 3 — A random double

nextNumber = 2,147,483,648 (2³¹): >> 8 gives 8,388,608; / 16,777,216 = **0.5**.

### Example 4 — A die from a double

randomDouble = 0.71: 0.71 × 6 = 4.26 → whole part 4 → 1 + 4 = **5**.

### Example 5 — A range

randomRange with low = −1, high = 1 and randomDouble = 0.25: −1 + 2 × 0.25 = **−0.5**.

---

## Common mistakes

⚠️ **Using the low bits of an LCG** — `lcgNext(s) % 2` gives 0, 1, 0, 1 … Use the top bits (or xorshift).

⚠️ **A seed of 0 for xorshift** — it stays 0 for ever.

⚠️ **Signed numbers** — `int` overflow is an error in C++ (Chapter 4). Generators must use **unsigned** types like `std::uint32_t`.

⚠️ **Two random calls in one expression** — `PointF{randomDouble(r), randomDouble(r)}` is fine (braces are evaluated left to right), but `f(randomDouble(r), randomDouble(r))` may evaluate its arguments in either order, so x and y could swap between compilers. Use separate lines.

⚠️ **A new generator for every pixel with the same seed** — every pixel then gets the same "random" number. Make one generator and keep using it, or use a hash of (x, y).

⚠️ **Expecting perfectly even counts** — real randomness wobbles (Section 54.5).

---

## Practice

🏋️ **1.** Run the tiny LCG of Section 54.2 (a = 5, c = 3, m = 16) from the seed 1 and write down whether each number is odd or even. What pattern do you see?

🏋️ **2.** With a = 4, c = 1, m = 16, seed 0, what happens? Why is this a bad choice of a?

🏋️ **3.** Write `Colour randomColour(Random& r)`: a random colour with each channel 0 … 255.

🏋️ **4.** Write `void shuffle(std::vector<int>& list, Random& r)` that puts a list in random order (the Fisher–Yates way: for i from the end down to 1, swap item i with a random item 0 … i).

🏋️ **5.** Write `PointF randomPointInCircle(Random& r, PointF centre, double radius)`: pick random points in the square around the circle until one is inside.

🏋️ **6.** Why can xorshift never reach 0 from a non-zero state, and why does 0 stay 0?

🏋️ **7.** Why is it useful that the same seed always gives the same picture?

🏋️ **8.** Write `double circleCoverageJittered(double cx, double cy, double r, int x, int y, int n, Random& rng)`, Chapter 27's `circleCoverage` with jittered samples.

---

## Answers

**1.**
> 1 → 8 → 11 → 10 → 5 → 12 → 15 → 14 → 9 → 0 → 3 → 2 → 13 → 4 → 7 → 6 → 1
> odd, even, odd, even, odd, even … — it flips every time, exactly as in Section 54.3 (a = 5 and c = 3 are both odd).

**2.**
> 0 → 1 → 5 → 21 mod 16 = 5 → 5 → 5 … It gets stuck at 5. a − 1 = 3 is not a multiple of 4 (and a = 4 is even), so the full period is impossible.

**3.**

```cpp
Colour randomColour(Random& r) {
    const std::uint8_t red = static_cast<std::uint8_t>(nextNumber(r) >> 24);
    const std::uint8_t green = static_cast<std::uint8_t>(nextNumber(r) >> 24);
    const std::uint8_t blue = static_cast<std::uint8_t>(nextNumber(r) >> 24);
    return Colour{red, green, blue};
}
```

**4.**

```cpp
void shuffle(std::vector<int>& list, Random& r) {
    for (int i = static_cast<int>(list.size()) - 1; i >= 1; --i) {
        const int j = randomInt(r, 0, i);
        std::swap(list[i], list[j]);
    }
}
```

> Every order is equally likely. (`std::swap` comes with `<algorithm>`.)

**5.**

```cpp
PointF randomPointInCircle(Random& r, PointF centre, double radius) {
    while (true) {
        const double dx = randomRange(r, -radius, radius);
        const double dy = randomRange(r, -radius, radius);
        if (dx * dx + dy * dy <= radius * radius) {
            return PointF{centre.x + dx, centre.y + dy};
        }
    }
}
```

> The circle covers π/4 ≈ 79 % of the square, so on average about 1.3 tries are needed. (Picking a random angle and a random distance instead would crowd the points near the centre.)

**6.**
> Each step is "state ^= shifted copy of state". If the result were 0, the state would have to equal its own shifted copy, which only 0 does — so a non-zero state never becomes 0. And 0 shifted is 0, and 0 ^ 0 = 0: 0 stays 0.

**7.**
> You can make the same picture again, test a change and compare, or fix a bug that only shows on one particular sky. A picture made with seed 2024 is the same on every computer. And to get a **new** picture, you just change the seed.

**8.**

```cpp
double circleCoverageJittered(double cx, double cy, double r, int x, int y, int n, Random& rng) {
    int inside = 0;
    for (int j = 0; j < n; ++j) {
        for (int i = 0; i < n; ++i) {
            const double dx = x + jitteredOffset(i, n, rng) - cx;
            const double dy = y + jitteredOffset(j, n, rng) - cy;
            if (dx * dx + dy * dy <= r * r) {
                ++inside;
            }
        }
    }
    return static_cast<double>(inside) / (n * n);
}
```

---

## Summary

🧠 **Pseudo-random** numbers come from a fixed rule applied to a **state**; the **seed** is where it starts. Same seed, same numbers.

🧠 The **LCG** (state × 1103515245 + 12345, wrapped at 2³²) has the full **period**, but its **low bits** are poor: use its top bits.

🧠 **Xorshift** (three shift-and-XOR steps) is better and tiny. Never seed it with 0.

🧠 Top 24 bits / 2²⁴ → a double in 0 … 1; from that, ranges and whole numbers. Test with counts and with a **pair picture**.

🧠 A **hash** of (x, y) gives a fixed random value per position, in any order. **Jittered** samples turn Chapter 27's steps into fine noise.

---

## Next chapter

White noise is too wild for clouds or hills: neighbouring pixels have nothing to do with each other. In Chapter 55 we make **value noise**: random values only at the corners of a grid (from `hashDouble`), and smooth blending in between (Chapter 13's lerp, with a gentler curve) — the first step towards the soft, natural textures of Chapters 56 and 57.
