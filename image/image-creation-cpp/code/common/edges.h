#ifndef EDGES_H
#define EDGES_H

#include <algorithm>
#include <cmath>
#include <vector>
#include "blur.h"
#include "hsv.h"

struct GreyF {
    int width = 0;
    int height = 0;
    std::vector<double> data;
};

inline GreyF makeGreyF(int width, int height) {
    return GreyF{width, height, std::vector<double>(width * height, 0.0)};
}

inline double greyAt(const GreyF& g, int x, int y) {
    const int cx = std::clamp(x, 0, g.width - 1);
    const int cy = std::clamp(y, 0, g.height - 1);
    return g.data[cy * g.width + cx];
}

inline GreyF toGreyF(const Image& image) {
    GreyF g = makeGreyF(image.width(), image.height());
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            g.data[y * g.width + x] = 255.0 * luma(toColourF(image.getPixel(x, y)));
        }
    }
    return g;
}

inline GreyF convolveGrey(const GreyF& src, const Kernel& k) {
    const int r = k.size / 2;
    GreyF out = makeGreyF(src.width, src.height);
    for (int y = 0; y < src.height; ++y) {
        for (int x = 0; x < src.width; ++x) {
            double sum = 0.0;
            for (int j = 0; j < k.size; ++j) {
                for (int i = 0; i < k.size; ++i) {
                    sum += k.weights[j * k.size + i] * greyAt(src, x + i - r, y + j - r);
                }
            }
            out.data[y * src.width + x] = sum;
        }
    }
    return out;
}

inline Kernel sharpenKernel() {
    return Kernel{3, {0, -1, 0, -1, 5, -1, 0, -1, 0}};
}

inline Kernel laplacianKernel() {
    return Kernel{3, {0, 1, 0, 1, -4, 1, 0, 1, 0}};
}

inline Kernel sobelX() {
    return Kernel{3, {-1, 0, 1, -2, 0, 2, -1, 0, 1}};
}

inline Kernel sobelY() {
    return Kernel{3, {-1, -2, -1, 0, 0, 0, 1, 2, 1}};
}

inline GreyF magnitudeOf(const GreyF& gx, const GreyF& gy) {
    GreyF m = makeGreyF(gx.width, gx.height);
    for (int i = 0; i < static_cast<int>(m.data.size()); ++i) {
        m.data[i] = std::sqrt(gx.data[i] * gx.data[i] + gy.data[i] * gy.data[i]);
    }
    return m;
}

inline GreyF sobelMagnitude(const GreyF& g) {
    return magnitudeOf(convolveGrey(g, sobelX()), convolveGrey(g, sobelY()));
}

inline double directionDegrees(double gx, double gy) {
    return wrapHue(radiansToDegrees(std::atan2(gy, gx)));
}

inline double largestValue(const GreyF& g) {
    double largest = 0.0;
    for (double v : g.data) {
        largest = std::max(largest, std::fabs(v));
    }
    return largest;
}

inline Image greyFToImage(const GreyF& g, double scale, double offset = 0.0) {
    Image image(g.width, g.height);
    for (int y = 0; y < g.height; ++y) {
        for (int x = 0; x < g.width; ++x) {
            const std::uint8_t v = clampByte(offset + scale * g.data[y * g.width + x]);
            image.setPixel(x, y, Colour{v, v, v});
        }
    }
    return image;
}

inline Image edgeMap(const GreyF& magnitude, double level) {
    Image image(magnitude.width, magnitude.height);
    for (int y = 0; y < magnitude.height; ++y) {
        for (int x = 0; x < magnitude.width; ++x) {
            const bool edge = magnitude.data[y * magnitude.width + x] >= level;
            image.setPixel(x, y, edge ? colours::white : colours::black);
        }
    }
    return image;
}

inline Image directionColours(const GreyF& gx, const GreyF& gy, double largest) {
    Image image(gx.width, gx.height);
    for (int y = 0; y < gx.height; ++y) {
        for (int x = 0; x < gx.width; ++x) {
            const double a = gx.data[y * gx.width + x];
            const double b = gy.data[y * gx.width + x];
            const double strength = std::min(1.0, std::sqrt(a * a + b * b) / largest);
            image.setPixel(x, y, toColour(hsvToRgb(HSV{directionDegrees(a, b), 1.0, strength})));
        }
    }
    return image;
}

inline Image unsharpMask(const Image& image, double sigma, double amount, bool linearLight = false) {
    const std::vector<double> w = gaussianWeights(sigma);
    const PixelsF sharp = toPixelsF(image, linearLight);
    const PixelsF soft = blurColumns(blurRows(sharp, w, EdgeMode::Clamp), w, EdgeMode::Clamp);
    PixelsF out = sharp;
    for (int i = 0; i < static_cast<int>(out.data.size()); ++i) {
        out.data[i] = sharp.data[i] + (sharp.data[i] - soft.data[i]) * amount;
    }
    return fromPixelsF(out, linearLight);
}

#endif
