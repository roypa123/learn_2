#ifndef ELLIPSES_H
#define ELLIPSES_H

#include <cmath>
#include "circles.h"

inline void fillEllipse(Image& image, double cx, double cy, double a, double b, Colour c,
                        double alpha = 1.0) {
    if (a <= 0.0 || b <= 0.0) {
        return;
    }
    int x0 = static_cast<int>(std::floor(cx - a));
    int y0 = static_cast<int>(std::floor(cy - b));
    int x1 = static_cast<int>(std::ceil(cx + a));
    int y1 = static_cast<int>(std::ceil(cy + b));
    Rect box = clipToImage(Rect{x0, y0, x1, y1}, image);
    double a2 = a * a;
    double b2 = b * b;
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            double dx = (x + 0.5) - cx;
            double dy = (y + 0.5) - cy;
            if (b2 * dx * dx + a2 * dy * dy <= a2 * b2) {
                if (alpha >= 1.0) {
                    image.setPixel(x, y, c);
                } else {
                    blendPixel(image, x, y, c, alpha);
                }
            }
        }
    }
}

inline void plotFour(Image& image, int cx, int cy, int x, int y, Colour c) {
    image.setPixel(cx + x, cy + y, c);
    image.setPixel(cx - x, cy + y, c);
    image.setPixel(cx - x, cy - y, c);
    image.setPixel(cx + x, cy - y, c);
}

inline void drawEllipse(Image& image, int cx, int cy, int a, int b, Colour c) {
    if (a < 0 || b < 0) {
        return;
    }
    const long long a2 = static_cast<long long>(a) * a;
    const long long b2 = static_cast<long long>(b) * b;
    int x = 0;
    int y = b;
    long long d = 4 * b2 - 4 * a2 * b + a2;
    while (b2 * x < a2 * y) {
        plotFour(image, cx, cy, x, y, c);
        ++x;
        if (d < 0) {
            d += 4 * b2 * (2 * x + 1);
        } else {
            --y;
            d += 4 * b2 * (2 * x + 1) - 8 * a2 * y;
        }
    }
    const long long u = 2LL * x + 1;
    const long long v = y - 1LL;
    d = b2 * u * u + 4 * a2 * v * v - 4 * a2 * b2;
    while (y >= 0) {
        plotFour(image, cx, cy, x, y, c);
        --y;
        if (d > 0) {
            d += 4 * a2 * (1 - 2 * y);
        } else {
            ++x;
            d += 4 * a2 * (1 - 2 * y) + 8 * b2 * x;
        }
    }
    while (x <= a) {
        plotFour(image, cx, cy, x, 0, c);
        ++x;
    }
}

#endif
