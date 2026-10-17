#ifndef ALPHA_H
#define ALPHA_H

#include <algorithm>
#include "srgb.h"

struct ColourFA {
    double r = 0.0;
    double g = 0.0;
    double b = 0.0;
    double a = 0.0;
};

inline ColourFA withAlpha(ColourF c, double a) {
    return ColourFA{c.r, c.g, c.b, a};
}

inline ColourFA overStraight(ColourFA src, ColourFA dst) {
    double outA = src.a + dst.a * (1.0 - src.a);
    if (outA <= 0.0) {
        return ColourFA{};
    }
    double k = dst.a * (1.0 - src.a);
    return ColourFA{(src.r * src.a + dst.r * k) / outA,
                    (src.g * src.a + dst.g * k) / outA,
                    (src.b * src.a + dst.b * k) / outA,
                    outA};
}

inline ColourFA premultiply(ColourFA c) {
    return ColourFA{c.r * c.a, c.g * c.a, c.b * c.a, c.a};
}

inline ColourFA unpremultiply(ColourFA c) {
    if (c.a <= 0.0) {
        return ColourFA{};
    }
    return ColourFA{c.r / c.a, c.g / c.a, c.b / c.a, c.a};
}

inline ColourFA overPremultiplied(ColourFA src, ColourFA dst) {
    double k = 1.0 - src.a;
    return ColourFA{src.r + dst.r * k, src.g + dst.g * k, src.b + dst.b * k, src.a + dst.a * k};
}

inline Colour blendOver(Colour dst, Colour src, double alpha) {
    alpha = std::clamp(alpha, 0.0, 1.0);
    ColourF ld = toLinear(dst);
    ColourF ls = toLinear(src);
    return fromLinear(ls * alpha + ld * (1.0 - alpha));
}

inline void blendPixel(Image& image, int x, int y, Colour src, double alpha) {
    if (!image.isInside(x, y)) {
        return;
    }
    image.setPixel(x, y, blendOver(image.getPixel(x, y), src, alpha));
}

#endif
