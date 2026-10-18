#ifndef CONVOLVE_H
#define CONVOLVE_H

#include <algorithm>
#include <vector>
#include "histogram.h"

struct Kernel {
    int size = 1;
    std::vector<double> weights;
};

enum class EdgeMode { Zero, Clamp, Mirror, Wrap };

inline double kernelSum(const Kernel& k) {
    double sum = 0.0;
    for (double w : k.weights) {
        sum += w;
    }
    return sum;
}

inline Kernel identityKernel() {
    return Kernel{3, {0, 0, 0, 0, 1, 0, 0, 0, 0}};
}

inline Kernel boxKernel(int size) {
    return Kernel{size, std::vector<double>(size * size, 1.0 / (size * size))};
}

inline int edgeIndex(int i, int n, EdgeMode mode) {
    if (i >= 0 && i < n) {
        return i;
    }
    if (mode == EdgeMode::Zero) {
        return -1;
    }
    if (mode == EdgeMode::Clamp) {
        return std::clamp(i, 0, n - 1);
    }
    if (mode == EdgeMode::Mirror) {
        const int period = 2 * n;
        int m = i % period;
        if (m < 0) {
            m += period;
        }
        return (m < n) ? m : period - 1 - m;
    }
    int m = i % n;
    if (m < 0) {
        m += n;
    }
    return m;
}

inline ColourF readPixel(const Image& src, int x, int y, EdgeMode mode, bool linearLight) {
    const int ex = edgeIndex(x, src.width(), mode);
    const int ey = edgeIndex(y, src.height(), mode);
    if (ex < 0 || ey < 0) {
        return ColourF{0.0, 0.0, 0.0};
    }
    const Colour c = src.getPixel(ex, ey);
    return linearLight ? toLinear(c) : toColourF(c);
}

inline Colour writePixel(ColourF value, bool linearLight) {
    return linearLight ? fromLinear(value) : toColour(value);
}

inline Colour convolvePixel(const Image& src, int x, int y, const Kernel& k, EdgeMode mode,
                            bool linearLight) {
    const int r = k.size / 2;
    ColourF sum{0.0, 0.0, 0.0};
    for (int j = 0; j < k.size; ++j) {
        for (int i = 0; i < k.size; ++i) {
            const double w = k.weights[j * k.size + i];
            if (w != 0.0) {
                sum = sum + readPixel(src, x + i - r, y + j - r, mode, linearLight) * w;
            }
        }
    }
    return writePixel(sum, linearLight);
}

inline Image convolve(const Image& src, const Kernel& k, EdgeMode mode = EdgeMode::Clamp,
                      bool linearLight = false) {
    Image out(src.width(), src.height());
    for (int y = 0; y < src.height(); ++y) {
        for (int x = 0; x < src.width(); ++x) {
            out.setPixel(x, y, convolvePixel(src, x, y, k, mode, linearLight));
        }
    }
    return out;
}

#endif
