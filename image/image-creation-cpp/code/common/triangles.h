#ifndef TRIANGLES_H
#define TRIANGLES_H

#include <algorithm>
#include <cmath>
#include "ellipses.h"

struct PointF {
    double x = 0.0;
    double y = 0.0;
};

inline double edgeFunction(PointF a, PointF b, PointF p) {
    return (b.x - a.x) * (p.y - a.y) - (b.y - a.y) * (p.x - a.x);
}

inline double triangleArea(PointF a, PointF b, PointF c) {
    return std::fabs(edgeFunction(a, b, c)) / 2.0;
}

inline bool isTopLeft(PointF from, PointF to) {
    double ex = to.x - from.x;
    double ey = to.y - from.y;
    return (ey == 0.0 && ex > 0.0) || ey < 0.0;
}

inline bool edgeCovers(double e, bool topLeft) {
    return e > 0.0 || (e == 0.0 && topLeft);
}

inline void fillTriangle(Image& image, PointF a, PointF b, PointF c, Colour col,
                         double alpha = 1.0) {
    double area2 = edgeFunction(a, b, c);
    if (area2 == 0.0) {
        return;
    }
    if (area2 < 0.0) {
        std::swap(b, c);
    }
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
                if (alpha >= 1.0) {
                    image.setPixel(x, y, col);
                } else {
                    blendPixel(image, x, y, col, alpha);
                }
            }
        }
    }
}

inline void drawTriangle(Image& image, Point a, Point b, Point c, Colour col) {
    drawLine(image, a.x, a.y, b.x, b.y, col, false);
    drawLine(image, b.x, b.y, c.x, c.y, col, false);
    drawLine(image, c.x, c.y, a.x, a.y, col, false);
}

inline void fillConvexPolygon(Image& image, const std::vector<PointF>& points, Colour col,
                              double alpha = 1.0) {
    const int n = static_cast<int>(points.size());
    for (int i = 1; i + 1 < n; ++i) {
        fillTriangle(image, points[0], points[i], points[i + 1], col, alpha);
    }
}

#endif
