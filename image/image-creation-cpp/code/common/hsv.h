#ifndef HSV_H
#define HSV_H

#include <algorithm>
#include <cmath>
#include "colourf.h"

struct HSV {
    double h = 0.0;
    double s = 0.0;
    double v = 0.0;
};

struct HSL {
    double h = 0.0;
    double s = 0.0;
    double l = 0.0;
};

inline double wrapHue(double h) {
    h = std::fmod(h, 360.0);
    if (h < 0.0) {
        h += 360.0;
    }
    return h;
}

inline double hueOf(ColourF c) {
    double maxC = std::max({c.r, c.g, c.b});
    double minC = std::min({c.r, c.g, c.b});
    double delta = maxC - minC;
    if (delta == 0.0) {
        return 0.0;
    }
    double h = 0.0;
    if (maxC == c.r) {
        h = 60.0 * ((c.g - c.b) / delta);
    } else if (maxC == c.g) {
        h = 60.0 * ((c.b - c.r) / delta + 2.0);
    } else {
        h = 60.0 * ((c.r - c.g) / delta + 4.0);
    }
    return wrapHue(h);
}

inline HSV rgbToHsv(ColourF c) {
    double maxC = std::max({c.r, c.g, c.b});
    double minC = std::min({c.r, c.g, c.b});
    HSV result;
    result.h = hueOf(c);
    result.v = maxC;
    result.s = (maxC == 0.0) ? 0.0 : (maxC - minC) / maxC;
    return result;
}

inline HSL rgbToHsl(ColourF c) {
    double maxC = std::max({c.r, c.g, c.b});
    double minC = std::min({c.r, c.g, c.b});
    double delta = maxC - minC;
    HSL result;
    result.h = hueOf(c);
    result.l = (maxC + minC) / 2.0;
    result.s = (delta == 0.0) ? 0.0 : delta / (1.0 - std::fabs(2.0 * result.l - 1.0));
    return result;
}

inline ColourF hueToRgb(double h, double c) {
    double hp = wrapHue(h) / 60.0;
    double x = c * (1.0 - std::fabs(std::fmod(hp, 2.0) - 1.0));
    if (hp < 1.0) {
        return ColourF{c, x, 0.0};
    }
    if (hp < 2.0) {
        return ColourF{x, c, 0.0};
    }
    if (hp < 3.0) {
        return ColourF{0.0, c, x};
    }
    if (hp < 4.0) {
        return ColourF{0.0, x, c};
    }
    if (hp < 5.0) {
        return ColourF{x, 0.0, c};
    }
    return ColourF{c, 0.0, x};
}

inline ColourF hsvToRgb(HSV hsv) {
    double c = hsv.v * hsv.s;
    double m = hsv.v - c;
    return hueToRgb(hsv.h, c) + ColourF{m, m, m};
}

inline ColourF hslToRgb(HSL hsl) {
    double c = (1.0 - std::fabs(2.0 * hsl.l - 1.0)) * hsl.s;
    double m = hsl.l - c / 2.0;
    return hueToRgb(hsl.h, c) + ColourF{m, m, m};
}

inline Colour shiftHue(Colour c, double degrees) {
    HSV hsv = rgbToHsv(toColourF(c));
    hsv.h = wrapHue(hsv.h + degrees);
    return toColour(hsvToRgb(hsv));
}

#endif
