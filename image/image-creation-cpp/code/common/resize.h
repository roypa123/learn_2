#ifndef RESIZE_H
#define RESIZE_H

#include <algorithm>
#include <cmath>
#include "bezier.h"

inline Image resizeNearest(const Image& source, int width, int height) {
    Image result(width, height);
    if (source.width() == 0 || source.height() == 0) {
        return result;
    }
    double scaleX = static_cast<double>(source.width()) / width;
    double scaleY = static_cast<double>(source.height()) / height;
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            int sx = static_cast<int>(std::floor((x + 0.5) * scaleX));
            int sy = static_cast<int>(std::floor((y + 0.5) * scaleY));
            result.setPixel(x, y, source.getPixel(sx, sy));
        }
    }
    return result;
}

inline Colour getPixelClamped(const Image& image, int x, int y) {
    x = std::clamp(x, 0, image.width() - 1);
    y = std::clamp(y, 0, image.height() - 1);
    return image.getPixel(x, y);
}

inline ColourF pixelAsF(const Image& image, int x, int y, bool linearLight) {
    Colour c = getPixelClamped(image, x, y);
    return linearLight ? toLinear(c) : toColourF(c);
}

inline Colour sampleBilinear(const Image& image, PointF p, bool linearLight = true) {
    double gx = p.x - 0.5;
    double gy = p.y - 0.5;
    int x0 = static_cast<int>(std::floor(gx));
    int y0 = static_cast<int>(std::floor(gy));
    double fx = gx - x0;
    double fy = gy - y0;
    ColourF c00 = pixelAsF(image, x0, y0, linearLight);
    ColourF c10 = pixelAsF(image, x0 + 1, y0, linearLight);
    ColourF c01 = pixelAsF(image, x0, y0 + 1, linearLight);
    ColourF c11 = pixelAsF(image, x0 + 1, y0 + 1, linearLight);
    ColourF top = c00 * (1.0 - fx) + c10 * fx;
    ColourF bottom = c01 * (1.0 - fx) + c11 * fx;
    ColourF mixed = top * (1.0 - fy) + bottom * fy;
    return linearLight ? fromLinear(mixed) : toColour(mixed);
}

inline Image resizeBilinear(const Image& source, int width, int height, bool linearLight = true) {
    Image result(width, height);
    if (source.width() == 0 || source.height() == 0) {
        return result;
    }
    double scaleX = static_cast<double>(source.width()) / width;
    double scaleY = static_cast<double>(source.height()) / height;
    for (int y = 0; y < height; ++y) {
        for (int x = 0; x < width; ++x) {
            PointF p{(x + 0.5) * scaleX, (y + 0.5) * scaleY};
            result.setPixel(x, y, sampleBilinear(source, p, linearLight));
        }
    }
    return result;
}

inline int firstCentreAtOrAfter(double edge) {
    return static_cast<int>(std::ceil(edge - 0.5));
}

inline Image resizeBox(const Image& source, int width, int height) {
    Image result(width, height);
    if (source.width() == 0 || source.height() == 0) {
        return result;
    }
    double scaleX = static_cast<double>(source.width()) / width;
    double scaleY = static_cast<double>(source.height()) / height;
    for (int y = 0; y < height; ++y) {
        int sy0 = firstCentreAtOrAfter(y * scaleY);
        int sy1 = std::max(firstCentreAtOrAfter((y + 1) * scaleY), sy0 + 1);
        for (int x = 0; x < width; ++x) {
            int sx0 = firstCentreAtOrAfter(x * scaleX);
            int sx1 = std::max(firstCentreAtOrAfter((x + 1) * scaleX), sx0 + 1);
            ColourF sum{0.0, 0.0, 0.0};
            for (int sy = sy0; sy < sy1; ++sy) {
                for (int sx = sx0; sx < sx1; ++sx) {
                    sum = sum + toLinear(getPixelClamped(source, sx, sy));
                }
            }
            int count = (sx1 - sx0) * (sy1 - sy0);
            result.setPixel(x, y, fromLinear(sum / count));
        }
    }
    return result;
}

inline void drawImageTransformedSmooth(Image& dest, const Image& source, const Mat3& t) {
    Mat3 back;
    if (!inverse(t, back)) {
        return;
    }
    Rect box = clipToImage(transformedBox(t, source.width(), source.height()), dest);
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            PointF s = applyToPoint(back, PointF{x + 0.5, y + 0.5});
            if (s.x >= 0.0 && s.x < source.width() && s.y >= 0.0 && s.y < source.height()) {
                dest.setPixel(x, y, sampleBilinear(source, s));
            }
        }
    }
}

#endif
