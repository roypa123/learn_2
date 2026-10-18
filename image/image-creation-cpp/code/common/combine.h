#ifndef COMBINE_H
#define COMBINE_H

#include <algorithm>
#include <cmath>
#include "matrix.h"

inline Mat3 rotationAbout(PointF centre, double radians) {
    return translation(centre.x, centre.y) * rotation(radians) * translation(-centre.x, -centre.y);
}

inline Mat3 scalingAbout(PointF centre, double sx, double sy) {
    return translation(centre.x, centre.y) * scaling(sx, sy) * translation(-centre.x, -centre.y);
}

inline bool inverse(const Mat3& t, Mat3& result) {
    double det = determinant(t);
    if (std::fabs(det) < 1e-12) {
        return false;
    }
    double a = t.m[0][0];
    double b = t.m[0][1];
    double c = t.m[1][0];
    double d = t.m[1][1];
    Mat3 r;
    r.m[0][0] = d / det;
    r.m[0][1] = -b / det;
    r.m[1][0] = -c / det;
    r.m[1][1] = a / det;
    double tx = t.m[0][2];
    double ty = t.m[1][2];
    r.m[0][2] = -(r.m[0][0] * tx + r.m[0][1] * ty);
    r.m[1][2] = -(r.m[1][0] * tx + r.m[1][1] * ty);
    result = r;
    return true;
}

inline Rect transformedBox(const Mat3& t, int width, int height) {
    PointF corners[4] = {PointF{0.0, 0.0}, PointF{static_cast<double>(width), 0.0},
                         PointF{static_cast<double>(width), static_cast<double>(height)},
                         PointF{0.0, static_cast<double>(height)}};
    PointF first = applyToPoint(t, corners[0]);
    double minX = first.x;
    double maxX = first.x;
    double minY = first.y;
    double maxY = first.y;
    for (int i = 1; i < 4; ++i) {
        PointF p = applyToPoint(t, corners[i]);
        minX = std::min(minX, p.x);
        maxX = std::max(maxX, p.x);
        minY = std::min(minY, p.y);
        maxY = std::max(maxY, p.y);
    }
    return Rect{static_cast<int>(std::floor(minX)), static_cast<int>(std::floor(minY)),
                static_cast<int>(std::ceil(maxX)), static_cast<int>(std::ceil(maxY))};
}

inline void drawImageForward(Image& dest, const Image& source, const Mat3& t) {
    for (int y = 0; y < source.height(); ++y) {
        for (int x = 0; x < source.width(); ++x) {
            PointF p = applyToPoint(t, PointF{x + 0.5, y + 0.5});
            int dx = static_cast<int>(std::floor(p.x));
            int dy = static_cast<int>(std::floor(p.y));
            dest.setPixel(dx, dy, source.getPixel(x, y));
        }
    }
}

inline void drawImageTransformed(Image& dest, const Image& source, const Mat3& t) {
    Mat3 back;
    if (!inverse(t, back)) {
        return;
    }
    Rect box = clipToImage(transformedBox(t, source.width(), source.height()), dest);
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            PointF s = applyToPoint(back, PointF{x + 0.5, y + 0.5});
            int sx = static_cast<int>(std::floor(s.x));
            int sy = static_cast<int>(std::floor(s.y));
            if (source.isInside(sx, sy)) {
                dest.setPixel(x, y, source.getPixel(sx, sy));
            }
        }
    }
}

#endif
