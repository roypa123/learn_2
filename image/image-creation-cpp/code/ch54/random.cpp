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
