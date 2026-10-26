#ifndef WARP_H
#define WARP_H

#include <cmath>
#include <vector>
#include "dither.h"

enum class WarpKind { None, Wave, Ripple, Swirl, Bulge };

struct Warp {
    WarpKind kind = WarpKind::None;
    PointF centre{0.0, 0.0};
    double amount = 0.0;
    double size = 1.0;
};

inline PointF waveSource(PointF p, const Warp& w) {
    return PointF{p.x + w.amount * std::sin(2.0 * kPi * p.y / w.size), p.y};
}

inline PointF rippleSource(PointF p, const Warp& w) {
    const Vec2 d = p - w.centre;
    const double r = length(d);
    if (r == 0.0) {
        return p;
    }
    const double push = w.amount * std::sin(2.0 * kPi * r / w.size);
    return w.centre + d * ((r + push) / r);
}

inline PointF swirlSource(PointF p, const Warp& w) {
    const Vec2 d = p - w.centre;
    const double r = length(d);
    if (r >= w.size) {
        return p;
    }
    const double angle = w.amount * (1.0 - r / w.size);
    return w.centre + rotate(d, angle);
}

inline PointF bulgeSource(PointF p, const Warp& w) {
    const Vec2 d = p - w.centre;
    const double r = length(d);
    if (r == 0.0 || r >= w.size) {
        return p;
    }
    return w.centre + d * std::pow(r / w.size, w.amount - 1.0);
}

inline PointF warpSource(PointF p, const Warp& w) {
    if (w.kind == WarpKind::Wave) {
        return waveSource(p, w);
    }
    if (w.kind == WarpKind::Ripple) {
        return rippleSource(p, w);
    }
    if (w.kind == WarpKind::Swirl) {
        return swirlSource(p, w);
    }
    if (w.kind == WarpKind::Bulge) {
        return bulgeSource(p, w);
    }
    return p;
}

inline bool insideImage(const Image& image, PointF p) {
    return p.x >= 0.0 && p.x < image.width() && p.y >= 0.0 && p.y < image.height();
}

inline Image warpImage(const Image& source, const Warp& w, Colour outside,
                       bool linearLight = true) {
    Image result(source.width(), source.height());
    for (int y = 0; y < source.height(); ++y) {
        for (int x = 0; x < source.width(); ++x) {
            const PointF from = warpSource(PointF{x + 0.5, y + 0.5}, w);
            if (insideImage(source, from)) {
                result.setPixel(x, y, sampleBilinear(source, from, linearLight));
            } else {
                result.setPixel(x, y, outside);
            }
        }
    }
    return result;
}

inline Image warpForward(const Image& source, const Warp& w, Colour background, int& holes) {
    Image result(source.width(), source.height(), background);
    std::vector<bool> painted(source.width() * source.height(), false);
    for (int y = 0; y < source.height(); ++y) {
        for (int x = 0; x < source.width(); ++x) {
            const PointF to = warpSource(PointF{x + 0.5, y + 0.5}, w);
            const int tx = static_cast<int>(std::floor(to.x));
            const int ty = static_cast<int>(std::floor(to.y));
            if (tx >= 0 && tx < source.width() && ty >= 0 && ty < source.height()) {
                result.setPixel(tx, ty, source.getPixel(x, y));
                painted[ty * source.width() + tx] = true;
            }
        }
    }
    holes = 0;
    for (bool p : painted) {
        holes += p ? 0 : 1;
    }
    return result;
}

#endif
