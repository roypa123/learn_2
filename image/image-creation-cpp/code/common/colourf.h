#ifndef COLOURF_H
#define COLOURF_H

#include <algorithm>
#include <cmath>
#include "image.h"

struct ColourF {
    double r = 0.0;
    double g = 0.0;
    double b = 0.0;
};

inline ColourF operator+(ColourF a, ColourF b) {
    return ColourF{a.r + b.r, a.g + b.g, a.b + b.b};
}

inline ColourF operator-(ColourF a, ColourF b) {
    return ColourF{a.r - b.r, a.g - b.g, a.b - b.b};
}

inline ColourF operator*(ColourF a, double s) {
    return ColourF{a.r * s, a.g * s, a.b * s};
}

inline ColourF operator*(double s, ColourF a) {
    return a * s;
}

inline ColourF operator*(ColourF a, ColourF b) {
    return ColourF{a.r * b.r, a.g * b.g, a.b * b.b};
}

inline ColourF operator/(ColourF a, double s) {
    return ColourF{a.r / s, a.g / s, a.b / s};
}

inline ColourF toColourF(Colour c) {
    return ColourF{c.r / 255.0, c.g / 255.0, c.b / 255.0};
}

inline std::uint8_t toByte(double v) {
    double clamped = std::clamp(v, 0.0, 1.0);
    return static_cast<std::uint8_t>(clamped * 255.0 + 0.5);
}

inline Colour toColour(ColourF c) {
    return Colour{toByte(c.r), toByte(c.g), toByte(c.b)};
}

inline double length(ColourF c) {
    return std::sqrt(c.r * c.r + c.g * c.g + c.b * c.b);
}

#endif
