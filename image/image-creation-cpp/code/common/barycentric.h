#ifndef BARYCENTRIC_H
#define BARYCENTRIC_H

#include <algorithm>
#include <cmath>
#include "fill.h"

struct Barycentric {
    double l0 = 0.0;
    double l1 = 0.0;
    double l2 = 0.0;
};

inline Barycentric barycentric(PointF a, PointF b, PointF c, PointF p) {
    double area2 = edgeFunction(a, b, c);
    if (area2 == 0.0) {
        return Barycentric{-1.0, -1.0, -1.0};
    }
    Barycentric w;
    w.l0 = edgeFunction(b, c, p) / area2;
    w.l1 = edgeFunction(c, a, p) / area2;
    w.l2 = edgeFunction(a, b, p) / area2;
    return w;
}

inline PointF fromBarycentric(PointF a, PointF b, PointF c, Barycentric w) {
    return PointF{w.l0 * a.x + w.l1 * b.x + w.l2 * c.x,
                  w.l0 * a.y + w.l1 * b.y + w.l2 * c.y};
}

inline bool allPositive(Barycentric w) {
    return w.l0 >= 0.0 && w.l1 >= 0.0 && w.l2 >= 0.0;
}

inline ColourF mixThree(ColourF ca, ColourF cb, ColourF cc, Barycentric w) {
    return ca * w.l0 + cb * w.l1 + cc * w.l2;
}

inline void fillTriangleColours(Image& image, PointF a, PointF b, PointF c,
                                Colour ca, Colour cb, Colour cc, bool linearLight = true) {
    double area2 = edgeFunction(a, b, c);
    if (area2 == 0.0) {
        return;
    }
    if (area2 < 0.0) {
        std::swap(b, c);
        std::swap(cb, cc);
        area2 = -area2;
    }
    ColourF fa = linearLight ? toLinear(ca) : toColourF(ca);
    ColourF fb = linearLight ? toLinear(cb) : toColourF(cb);
    ColourF fc = linearLight ? toLinear(cc) : toColourF(cc);
    int x0 = static_cast<int>(std::floor(std::min({a.x, b.x, c.x})));
    int y0 = static_cast<int>(std::floor(std::min({a.y, b.y, c.y})));
    int x1 = static_cast<int>(std::ceil(std::max({a.x, b.x, c.x})));
    int y1 = static_cast<int>(std::ceil(std::max({a.y, b.y, c.y})));
    Rect box = clipToImage(Rect{x0, y0, x1, y1}, image);
    bool topLeft0 = isTopLeft(b, c);
    bool topLeft1 = isTopLeft(c, a);
    bool topLeft2 = isTopLeft(a, b);
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            PointF p{x + 0.5, y + 0.5};
            double w0 = edgeFunction(b, c, p);
            double w1 = edgeFunction(c, a, p);
            double w2 = edgeFunction(a, b, p);
            if (edgeCovers(w0, topLeft0) && edgeCovers(w1, topLeft1) &&
                edgeCovers(w2, topLeft2)) {
                Barycentric w{w0 / area2, w1 / area2, w2 / area2};
                ColourF mixed = mixThree(fa, fb, fc, w);
                image.setPixel(x, y, linearLight ? fromLinear(mixed) : toColour(mixed));
            }
        }
    }
}

#endif
