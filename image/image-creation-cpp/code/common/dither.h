#ifndef DITHER_H
#define DITHER_H

#include <algorithm>
#include <cmath>
#include <vector>
#include "edges.h"

const int kBayer4[16] = {0, 8, 2, 10, 12, 4, 14, 6, 3, 11, 1, 9, 15, 7, 13, 5};

inline double bayerThreshold(int x, int y) {
    return (kBayer4[(y % 4) * 4 + (x % 4)] + 0.5) / 16.0;
}

inline double nearestLevel(double v, int levels) {
    const double steps = levels - 1;
    return std::floor(std::clamp(v, 0.0, 1.0) * steps + 0.5) / steps;
}

inline Image posterise(const Image& image, int levels) {
    Image out(image.width(), image.height());
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            const ColourF c = toColourF(image.getPixel(x, y));
            const ColourF q{nearestLevel(c.r, levels), nearestLevel(c.g, levels),
                            nearestLevel(c.b, levels)};
            out.setPixel(x, y, toColour(q));
        }
    }
    return out;
}

inline double orderedChannel(double v, double t, int levels, bool linearLight) {
    const double steps = levels - 1;
    const double low = std::floor(v * steps) / steps;
    if (low >= 1.0) {
        return 1.0;
    }
    const double high = low + 1.0 / steps;
    double f = (v - low) * steps;
    if (linearLight) {
        f = (srgbToLinear(v) - srgbToLinear(low)) / (srgbToLinear(high) - srgbToLinear(low));
    }
    return (f > t) ? high : low;
}

inline Image orderedDither(const Image& image, int levels, bool linearLight = true) {
    Image out(image.width(), image.height());
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            const ColourF c = toColourF(image.getPixel(x, y));
            const double t = bayerThreshold(x, y);
            const ColourF q{orderedChannel(c.r, t, levels, linearLight),
                            orderedChannel(c.g, t, levels, linearLight),
                            orderedChannel(c.b, t, levels, linearLight)};
            out.setPixel(x, y, toColour(q));
        }
    }
    return out;
}

inline std::vector<Colour> cubePalette(int levels) {
    std::vector<Colour> palette;
    for (int r = 0; r < levels; ++r) {
        for (int g = 0; g < levels; ++g) {
            for (int b = 0; b < levels; ++b) {
                const double s = 1.0 / (levels - 1);
                palette.push_back(toColour(ColourF{r * s, g * s, b * s}));
            }
        }
    }
    return palette;
}

inline double distanceSquared(ColourF a, ColourF b) {
    const ColourF d = a - b;
    return d.r * d.r + d.g * d.g + d.b * d.b;
}

inline int nearestIndex(ColourF c, const std::vector<ColourF>& palette) {
    int best = 0;
    for (int i = 1; i < static_cast<int>(palette.size()); ++i) {
        if (distanceSquared(c, palette[i]) < distanceSquared(c, palette[best])) {
            best = i;
        }
    }
    return best;
}

inline void addError(PixelsF& p, int x, int y, ColourF error, double weight) {
    if (x >= 0 && x < p.width && y >= 0 && y < p.height) {
        p.data[y * p.width + x] = p.data[y * p.width + x] + error * weight;
    }
}

inline Image floydSteinberg(const Image& image, const std::vector<Colour>& palette,
                            bool linearLight = true) {
    PixelsF work = toPixelsF(image, linearLight);
    std::vector<ColourF> values;
    for (Colour c : palette) {
        values.push_back(linearLight ? toLinear(c) : toColourF(c));
    }
    Image out(image.width(), image.height());
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            const ColourF old = work.data[y * work.width + x];
            const int k = nearestIndex(old, values);
            out.setPixel(x, y, palette[k]);
            const ColourF error = old - values[k];
            addError(work, x + 1, y, error, 7.0 / 16.0);
            addError(work, x - 1, y + 1, error, 3.0 / 16.0);
            addError(work, x, y + 1, error, 5.0 / 16.0);
            addError(work, x + 1, y + 1, error, 1.0 / 16.0);
        }
    }
    return out;
}

inline Colour averageColour(const Image& image) {
    ColourF sum{0.0, 0.0, 0.0};
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            sum = sum + toLinear(image.getPixel(x, y));
        }
    }
    return fromLinear(sum / (image.width() * image.height()));
}

#endif
