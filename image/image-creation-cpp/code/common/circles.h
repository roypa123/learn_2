#ifndef CIRCLES_H
#define CIRCLES_H

#include <cmath>
#include "lines.h"

inline void drawCircleNaive(Image& image, int cx, int cy, int r, Colour c) {
    for (int x = -r; x <= r; ++x) {
        int y = roundToInt(std::sqrt(static_cast<double>(r * r - x * x)));
        image.setPixel(cx + x, cy + y, c);
        image.setPixel(cx + x, cy - y, c);
    }
}

inline void plotEight(Image& image, int cx, int cy, int x, int y, Colour c) {
    image.setPixel(cx + x, cy + y, c);
    image.setPixel(cx + y, cy + x, c);
    image.setPixel(cx - y, cy + x, c);
    image.setPixel(cx - x, cy + y, c);
    image.setPixel(cx - x, cy - y, c);
    image.setPixel(cx - y, cy - x, c);
    image.setPixel(cx + y, cy - x, c);
    image.setPixel(cx + x, cy - y, c);
}

inline void drawCircle(Image& image, int cx, int cy, int r, Colour c) {
    if (r < 0) {
        return;
    }
    int x = r;
    int y = 0;
    int d = 1 - r;
    while (x >= y) {
        plotEight(image, cx, cy, x, y, c);
        ++y;
        if (d < 0) {
            d += 2 * y + 1;
        } else {
            --x;
            d += 2 * (y - x) + 1;
        }
    }
}

inline void fillCircle(Image& image, double cx, double cy, double radius, Colour c,
                       double alpha = 1.0) {
    int x0 = static_cast<int>(std::floor(cx - radius));
    int y0 = static_cast<int>(std::floor(cy - radius));
    int x1 = static_cast<int>(std::ceil(cx + radius));
    int y1 = static_cast<int>(std::ceil(cy + radius));
    Rect box = clipToImage(Rect{x0, y0, x1, y1}, image);
    double r2 = radius * radius;
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            double dx = (x + 0.5) - cx;
            double dy = (y + 0.5) - cy;
            if (dx * dx + dy * dy <= r2) {
                if (alpha >= 1.0) {
                    image.setPixel(x, y, c);
                } else {
                    blendPixel(image, x, y, c, alpha);
                }
            }
        }
    }
}

#endif
