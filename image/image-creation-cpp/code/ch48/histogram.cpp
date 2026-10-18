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
