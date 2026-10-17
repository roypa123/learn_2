#ifndef SRGB_H
#define SRGB_H

#include <algorithm>
#include <array>
#include <cmath>
#include "colourf.h"

inline double srgbToLinear(double v) {
    if (v <= 0.04045) {
        return v / 12.92;
    }
    return std::pow((v + 0.055) / 1.055, 2.4);
}

inline double linearToSrgb(double l) {
    l = std::clamp(l, 0.0, 1.0);
    if (l <= 0.0031308) {
        return 12.92 * l;
    }
    return 1.055 * std::pow(l, 1.0 / 2.4) - 0.055;
}

inline std::array<double, 256> makeLinearTable() {
    std::array<double, 256> table{};
    for (int i = 0; i < 256; ++i) {
        table[i] = srgbToLinear(i / 255.0);
    }
    return table;
}

inline const std::array<double, 256>& linearTable() {
    static const std::array<double, 256> table = makeLinearTable();
    return table;
}

inline ColourF toLinear(Colour c) {
    const std::array<double, 256>& t = linearTable();
    return ColourF{t[c.r], t[c.g], t[c.b]};
}

inline Colour fromLinear(ColourF l) {
    return toColour(ColourF{linearToSrgb(l.r), linearToSrgb(l.g), linearToSrgb(l.b)});
}

inline Colour lerpLinear(Colour a, Colour b, double t) {
    ColourF la = toLinear(a);
    ColourF lb = toLinear(b);
    return fromLinear(la + (lb - la) * t);
}

inline double luminance(Colour c) {
    ColourF l = toLinear(c);
    return 0.2126 * l.r + 0.7152 * l.g + 0.0722 * l.b;
}

#endif
