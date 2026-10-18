#ifndef BLUR_H
#define BLUR_H

#include <cmath>
#include <vector>
#include "convolve.h"

struct PixelsF {
    int width = 0;
    int height = 0;
    std::vector<ColourF> data;
};

inline PixelsF toPixelsF(const Image& image, bool linearLight) {
    PixelsF p{image.width(), image.height(), {}};
    p.data.reserve(image.width() * image.height());
    for (int y = 0; y < image.height(); ++y) {
        for (int x = 0; x < image.width(); ++x) {
            const Colour c = image.getPixel(x, y);
            p.data.push_back(linearLight ? toLinear(c) : toColourF(c));
        }
    }
    return p;
}

inline Image fromPixelsF(const PixelsF& p, bool linearLight) {
    Image image(p.width, p.height);
    for (int y = 0; y < p.height; ++y) {
        for (int x = 0; x < p.width; ++x) {
            image.setPixel(x, y, writePixel(p.data[y * p.width + x], linearLight));
        }
    }
    return image;
}

inline std::vector<double> gaussianWeights(double sigma) {
    const int r = static_cast<int>(std::ceil(3.0 * sigma));
    std::vector<double> w(2 * r + 1);
    double sum = 0.0;
    for (int i = 0; i <= 2 * r; ++i) {
        const double d = i - r;
        w[i] = std::exp(-(d * d) / (2.0 * sigma * sigma));
        sum += w[i];
    }
    for (double& v : w) {
        v /= sum;
    }
    return w;
}

inline std::vector<double> boxWeights(int radius) {
    return std::vector<double>(2 * radius + 1, 1.0 / (2 * radius + 1));
}

inline Kernel kernelFromWeights(const std::vector<double>& w) {
    const int n = static_cast<int>(w.size());
    Kernel k{n, std::vector<double>(n * n)};
    for (int j = 0; j < n; ++j) {
        for (int i = 0; i < n; ++i) {
            k.weights[j * n + i] = w[j] * w[i];
        }
    }
    return k;
}

inline PixelsF blurRows(const PixelsF& src, const std::vector<double>& w, EdgeMode mode) {
    const int r = static_cast<int>(w.size()) / 2;
    PixelsF out{src.width, src.height, std::vector<ColourF>(src.data.size())};
    for (int y = 0; y < src.height; ++y) {
        for (int x = 0; x < src.width; ++x) {
            ColourF sum{0.0, 0.0, 0.0};
            for (int k = 0; k < static_cast<int>(w.size()); ++k) {
                const int sx = edgeIndex(x + k - r, src.width, mode);
                if (sx >= 0) {
                    sum = sum + src.data[y * src.width + sx] * w[k];
                }
            }
            out.data[y * src.width + x] = sum;
        }
    }
    return out;
}

inline PixelsF blurColumns(const PixelsF& src, const std::vector<double>& w, EdgeMode mode) {
    const int r = static_cast<int>(w.size()) / 2;
    PixelsF out{src.width, src.height, std::vector<ColourF>(src.data.size())};
    for (int y = 0; y < src.height; ++y) {
        for (int x = 0; x < src.width; ++x) {
            ColourF sum{0.0, 0.0, 0.0};
            for (int k = 0; k < static_cast<int>(w.size()); ++k) {
                const int sy = edgeIndex(y + k - r, src.height, mode);
                if (sy >= 0) {
                    sum = sum + src.data[sy * src.width + x] * w[k];
                }
            }
            out.data[y * src.width + x] = sum;
        }
    }
    return out;
}

inline Image separableBlur(const Image& image, const std::vector<double>& w,
                           EdgeMode mode = EdgeMode::Clamp, bool linearLight = true) {
    const PixelsF across = blurRows(toPixelsF(image, linearLight), w, mode);
    return fromPixelsF(blurColumns(across, w, mode), linearLight);
}

inline Image gaussianBlur(const Image& image, double sigma, EdgeMode mode = EdgeMode::Clamp,
                          bool linearLight = true) {
    if (sigma <= 0.0) {
        return image;
    }
    return separableBlur(image, gaussianWeights(sigma), mode, linearLight);
}

inline PixelsF boxRowsFast(const PixelsF& src, int r) {
    PixelsF out{src.width, src.height, std::vector<ColourF>(src.data.size())};
    const double scale = 1.0 / (2 * r + 1);
    for (int y = 0; y < src.height; ++y) {
        const ColourF* row = &src.data[y * src.width];
        ColourF sum{0.0, 0.0, 0.0};
        for (int k = -r; k <= r; ++k) {
            sum = sum + row[edgeIndex(k, src.width, EdgeMode::Clamp)];
        }
        for (int x = 0; x < src.width; ++x) {
            out.data[y * src.width + x] = sum * scale;
            const ColourF entering = row[edgeIndex(x + r + 1, src.width, EdgeMode::Clamp)];
            const ColourF leaving = row[edgeIndex(x - r, src.width, EdgeMode::Clamp)];
            sum = sum + entering - leaving;
        }
    }
    return out;
}

inline PixelsF transposed(const PixelsF& src) {
    PixelsF out{src.height, src.width, std::vector<ColourF>(src.data.size())};
    for (int y = 0; y < src.height; ++y) {
        for (int x = 0; x < src.width; ++x) {
            out.data[x * src.height + y] = src.data[y * src.width + x];
        }
    }
    return out;
}

inline Image boxBlurFast(const Image& image, int radius, bool linearLight = true) {
    const PixelsF across = boxRowsFast(toPixelsF(image, linearLight), radius);
    const PixelsF down = boxRowsFast(transposed(across), radius);
    return fromPixelsF(transposed(down), linearLight);
}

#endif
