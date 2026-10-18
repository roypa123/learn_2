#ifndef POINTOPS_H
#define POINTOPS_H

#include <array>
#include <cmath>
#include <cstdint>
#include "font.h"
#include "grey.h"

using LookupTable = std::array<std::uint8_t, 256>;

inline std::uint8_t clampByte(double v) {
    if (v <= 0.0) {
        return 0;
    }
    if (v >= 255.0) {
        return 255;
    }
    return static_cast<std::uint8_t>(v + 0.5);
}

inline LookupTable identityTable() {
    LookupTable t{};
    for (int v = 0; v < 256; ++v) {
        t[v] = static_cast<std::uint8_t>(v);
    }
    return t;
}

inline LookupTable brightnessTable(int amount) {
    LookupTable t{};
    for (int v = 0; v < 256; ++v) {
        t[v] = clampByte(v + amount);
    }
    return t;
}

inline LookupTable contrastTable(double factor, double centre = 128.0) {
    LookupTable t{};
    for (int v = 0; v < 256; ++v) {
        t[v] = clampByte((v - centre) * factor + centre);
    }
    return t;
}

inline LookupTable invertTable() {
    LookupTable t{};
    for (int v = 0; v < 256; ++v) {
        t[v] = static_cast<std::uint8_t>(255 - v);
    }
    return t;
}

inline LookupTable thresholdTable(int level) {
    LookupTable t{};
    for (int v = 0; v < 256; ++v) {
        t[v] = (v >= level) ? 255 : 0;
    }
    return t;
}

inline LookupTable gammaTable(double gamma) {
    LookupTable t{};
    for (int v = 0; v < 256; ++v) {
        t[v] = clampByte(255.0 * std::pow(v / 255.0, gamma));
    }
    return t;
}

inline LookupTable exposureTable(double factor) {
    LookupTable t{};
    for (int v = 0; v < 256; ++v) {
        t[v] = clampByte(255.0 * linearToSrgb(srgbToLinear(v / 255.0) * factor));
    }
    return t;
}

inline LookupTable levelsTable(int low, int high) {
    if (high <= low) {
        high = low + 1;
    }
    LookupTable t{};
    for (int v = 0; v < 256; ++v) {
        t[v] = clampByte((v - low) * 255.0 / (high - low));
    }
    return t;
}

inline LookupTable combineTables(const LookupTable& first, const LookupTable& second) {
    LookupTable t{};
    for (int v = 0; v < 256; ++v) {
        t[v] = second[first[v]];
    }
    return t;
}

inline void applyTables(Image& image, const LookupTable& red, const LookupTable& green,
                        const LookupTable& blue) {
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            const Colour c = image.getPixel(x, y);
            image.setPixel(x, y, Colour{red[c.r], green[c.g], blue[c.b]});
        }
    }
}

inline void applyTable(Image& image, const LookupTable& t) {
    applyTables(image, t, t, t);
}

inline void makeGrey(Image& image) {
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            image.setPixel(x, y, toGrey(image.getPixel(x, y)));
        }
    }
}

inline double tableAverage(const LookupTable& t) {
    double sum = 0.0;
    for (std::uint8_t v : t) {
        sum += v;
    }
    return sum / 256.0;
}

inline void drawCurve(Image& image, int x, int y, int size, const LookupTable& t, Colour c) {
    strokeRect(image, makeRect(x, y, size + 1, size + 1), 1, Colour{170, 170, 170});
    drawLine(image, x, y + size, x + size, y, Colour{225, 225, 225});
    for (int v = 0; v < 255; ++v) {
        const int x0 = x + v * size / 255;
        const int y0 = y + size - t[v] * size / 255;
        const int x1 = x + (v + 1) * size / 255;
        const int y1 = y + size - t[v + 1] * size / 255;
        drawLine(image, x0, y0, x1, y1, c);
    }
}

#endif
