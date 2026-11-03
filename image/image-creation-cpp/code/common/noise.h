#ifndef NOISE_H
#define NOISE_H

#include <algorithm>
#include <cmath>
#include <vector>
#include "random.h"

inline double smoothstep(double t) {
    return t * t * (3.0 - 2.0 * t);
}

inline double valueNoise1D(double x, std::uint32_t seed, bool smooth = true) {
    const int i = static_cast<int>(std::floor(x));
    const double t = smooth ? smoothstep(x - i) : x - i;
    return lerp(hashDouble(i, 0, seed), hashDouble(i + 1, 0, seed), t);
}

inline double valueNoise(double x, double y, std::uint32_t seed, bool smooth = true) {
    const int ix = static_cast<int>(std::floor(x));
    const int iy = static_cast<int>(std::floor(y));
    const double tx = smooth ? smoothstep(x - ix) : x - ix;
    const double ty = smooth ? smoothstep(y - iy) : y - iy;
    const double top = lerp(hashDouble(ix, iy, seed), hashDouble(ix + 1, iy, seed), tx);
    const double bottom = lerp(hashDouble(ix, iy + 1, seed), hashDouble(ix + 1, iy + 1, seed), tx);
    return lerp(top, bottom, ty);
}

inline Image noiseImage(int width, int height, double cellSize, std::uint32_t seed,
                        bool smooth = true) {
    Image image(width, height);
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            const double v = valueNoise((x + 0.5) / cellSize, (y + 0.5) / cellSize, seed, smooth);
            const std::uint8_t g = toByte(v);
            image.setPixel(x, y, Colour{g, g, g});
        }
    }
    return image;
}

struct ColourStop {
    double at = 0.0;
    Colour colour;
};

inline Colour colourRamp(double v, const std::vector<ColourStop>& stops) {
    if (v <= stops.front().at) {
        return stops.front().colour;
    }
    for (int i = 1; i < static_cast<int>(stops.size()); ++i) {
        if (v <= stops[i].at) {
            const double t = (v - stops[i - 1].at) / (stops[i].at - stops[i - 1].at);
            return lerpColour(stops[i - 1].colour, stops[i].colour, t);
        }
    }
    return stops.back().colour;
}

inline Image colourImage(const Image& grey, const std::vector<ColourStop>& stops) {
    Image image(grey.width(), grey.height());
    for (int y = 0; y < grey.height(); ++y) {
        for (int x = 0; x < grey.width(); ++x) {
            image.setPixel(x, y, colourRamp(grey.getPixel(x, y).r / 255.0, stops));
        }
    }
    return image;
}

#endif
