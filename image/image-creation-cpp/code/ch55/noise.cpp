#include <cmath>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>
#include "noise.h"
#include "deflate.h"

std::string fourDecimals(double v) {
    const long long n = std::llround(v * 10000.0);
    std::string digits = std::to_string(n % 10000);
    while (digits.size() < 4) {
        digits = "0" + digits;
    }
    return std::to_string(n / 10000) + "." + digits;
}

double neighbourDifference(const Image& image) {
    double sum = 0.0;
    int count = 0;
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x + 1 < image.width(); ++x) {
            sum += std::abs(image.getPixel(x + 1, y).r - image.getPixel(x, y).r);
            ++count;
        }
    }
    return sum / count;
}

int graphY(double v) {
    return static_cast<int>(std::lround(100.0 - 90.0 * v));
}

Image makeGraph(std::uint32_t seed) {
    Image graph(160, 110, colours::white);
    for (int x = 0; x + 1 < 160; ++x) {
        for (int pass = 0; pass < 2; ++pass) {
            const bool smooth = (pass == 1);
            const int a = graphY(valueNoise1D(x / 20.0, seed, smooth));
            const int b = graphY(valueNoise1D((x + 1) / 20.0, seed, smooth));
            const Colour c = smooth ? colours::black : Colour{180, 180, 180};
            fillRect(graph, makeRect(x, std::min(a, b), 1, std::abs(a - b) + 1), c);
        }
    }
    for (int i = 0; i < 8; ++i) {
        fillRect(graph, makeRect(i * 20 - 1, graphY(hashDouble(i, 0, seed)) - 1, 3, 3), colours::red);
    }
    return graph;
}

int main() {
    const std::uint32_t seed = 1;
    std::cout << "corner values, seed 1:";
    for (int i = 0; i < 5; ++i) {
        std::cout << " " << fourDecimals(hashDouble(i, 0, seed));
    }
    std::cout << "\n\nt:          0 0.25 0.5 0.75 1\nsmoothstep:";
    for (int k = 0; k <= 4; ++k) {
        std::cout << " " << smoothstep(k / 4.0);
    }
    std::cout << "\nits slope: ";
    for (int k = 0; k <= 4; ++k) {
        const double t = k / 4.0;
        std::cout << " " << 6.0 * t * (1.0 - t);
    }
    std::cout << "\n\nbetween corners 1 and 2:\n  straight:";
    for (int k = 0; k <= 4; ++k) {
        std::cout << " " << fourDecimals(valueNoise1D(1.0 + k / 4.0, seed, false));
    }
    std::cout << "\n  smooth:  ";
    for (int k = 0; k <= 4; ++k) {
        std::cout << " " << fourDecimals(valueNoise1D(1.0 + k / 4.0, seed, true));
    }

    std::cout << "\n\ncorners around (2.5, 3.25): " << fourDecimals(hashDouble(2, 3, seed)) << " "
              << fourDecimals(hashDouble(3, 3, seed)) << " / " << fourDecimals(hashDouble(2, 4, seed))
              << " " << fourDecimals(hashDouble(3, 4, seed)) << "\nvalue noise at (2.5, 3.25): "
              << fourDecimals(valueNoise(2.5, 3.25, seed)) << "\n";

    Random r = makeRandom(5);
    const Image white = whiteNoise(160, 110, r);
    const Image straight = noiseImage(160, 110, 20.0, seed, false);
    const Image smooth = noiseImage(160, 110, 20.0, seed, true);
    std::cout << "\naverage change between neighbours: white noise "
              << fourDecimals(neighbourDifference(white)) << ", value noise "
              << fourDecimals(neighbourDifference(smooth)) << "\n";

    const std::vector<ColourStop> sky = {{0.0, Colour{60, 110, 200}}, {0.55, Colour{110, 160, 230}},
                                         {1.0, Colour{255, 255, 255}}};
    const std::vector<ColourStop> land = {{0.0, Colour{20, 40, 120}},    {0.45, Colour{50, 110, 190}},
                                          {0.5, Colour{230, 215, 150}},  {0.6, Colour{70, 140, 60}},
                                          {0.8, Colour{120, 110, 100}},  {0.9, Colour{250, 250, 250}},
                                          {1.0, Colour{250, 250, 250}}};
    const Image tiles[8] = {white,
                            straight,
                            smooth,
                            noiseImage(160, 110, 6.0, seed),
                            noiseImage(160, 110, 50.0, seed),
                            makeGraph(seed),
                            colourImage(noiseImage(160, 110, 24.0, 3), sky),
                            colourImage(noiseImage(160, 110, 30.0, 4), land)};
    const std::string names[8] = {"white noise", "straight lerp", "smoothstep", "cells of 6",
                                  "cells of 50",  "a row of it",   "sky",        "map"};
    Image sheet(4 * 170 + 10, 2 * 134 + 10, colours::white);
    for (int i = 0; i < 8; ++i) {
        const int left = 10 + (i % 4) * 170;
        const int top = 10 + (i / 4) * 134;
        for (int y = 0; y < 110; ++y) {
            for (int x = 0; x < 160; ++x) {
                sheet.setPixel(left + x, top + y, tiles[i].getPixel(x, y));
            }
        }
        drawText(sheet, left, top + 114, names[i], colours::black);
    }
    if (!savePNGCompressed(sheet, "noise.png")) {
        std::cout << "could not write noise.png\n";
        return 1;
    }
    std::cout << "wrote noise.png\n";
    return 0;
}
