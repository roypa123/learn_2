#ifndef LINES_H
#define LINES_H

#include <algorithm>
#include <cmath>
#include "draw.h"

inline int roundToInt(double v) {
    return static_cast<int>(std::floor(v + 0.5));
}

inline void drawLineNaive(Image& image, int x0, int y0, int x1, int y1, Colour c) {
    if (x0 == x1) {
        for (int y = std::min(y0, y1); y <= std::max(y0, y1); ++y) {
            image.setPixel(x0, y, c);
        }
        return;
    }
    double slope = static_cast<double>(y1 - y0) / (x1 - x0);
    for (int x = std::min(x0, x1); x <= std::max(x0, x1); ++x) {
        double y = y0 + slope * (x - x0);
        image.setPixel(x, roundToInt(y), c);
    }
}

inline void drawLineDDA(Image& image, int x0, int y0, int x1, int y1, Colour c) {
    int dx = x1 - x0;
    int dy = y1 - y0;
    int steps = std::max(std::abs(dx), std::abs(dy));
    if (steps == 0) {
        image.setPixel(x0, y0, c);
        return;
    }
    double xStep = static_cast<double>(dx) / steps;
    double yStep = static_cast<double>(dy) / steps;
    for (int i = 0; i <= steps; ++i) {
        double x = x0 + xStep * i;
        double y = y0 + yStep * i;
        image.setPixel(roundToInt(x), roundToInt(y), c);
    }
}

#endif
