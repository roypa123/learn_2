#ifndef BEZIER_H
#define BEZIER_H

#include <algorithm>
#include <cmath>
#include <vector>
#include "combine.h"

inline PointF lerpPoint(PointF a, PointF b, double t) {
    return a + (b - a) * t;
}

inline PointF quadraticPoint(PointF p0, PointF p1, PointF p2, double t) {
    PointF a = lerpPoint(p0, p1, t);
    PointF b = lerpPoint(p1, p2, t);
    return lerpPoint(a, b, t);
}

inline PointF cubicPoint(PointF p0, PointF p1, PointF p2, PointF p3, double t) {
    PointF a = lerpPoint(p0, p1, t);
    PointF b = lerpPoint(p1, p2, t);
    PointF c = lerpPoint(p2, p3, t);
    return quadraticPoint(a, b, c, t);
}

inline PointF cubicPointFormula(PointF p0, PointF p1, PointF p2, PointF p3, double t) {
    double u = 1.0 - t;
    return p0 * (u * u * u) + p1 * (3.0 * u * u * t) + p2 * (3.0 * u * t * t) + p3 * (t * t * t);
}

inline Vec2 cubicTangent(PointF p0, PointF p1, PointF p2, PointF p3, double t) {
    double u = 1.0 - t;
    return (p1 - p0) * (3.0 * u * u) + (p2 - p1) * (6.0 * u * t) + (p3 - p2) * (3.0 * t * t);
}

inline int segmentsFor(double controlLength) {
    return std::max(1, static_cast<int>(std::ceil(controlLength / 4.0)));
}

inline void appendQuadratic(std::vector<PointF>& path, PointF p0, PointF p1, PointF p2) {
    int n = segmentsFor(distance(p0, p1) + distance(p1, p2));
    if (path.empty()) {
        path.push_back(p0);
    }
    for (int i = 1; i <= n; ++i) {
        path.push_back(quadraticPoint(p0, p1, p2, static_cast<double>(i) / n));
    }
}

inline void appendCubic(std::vector<PointF>& path, PointF p0, PointF p1, PointF p2, PointF p3) {
    int n = segmentsFor(distance(p0, p1) + distance(p1, p2) + distance(p2, p3));
    if (path.empty()) {
        path.push_back(p0);
    }
    for (int i = 1; i <= n; ++i) {
        path.push_back(cubicPoint(p0, p1, p2, p3, static_cast<double>(i) / n));
    }
}

inline void drawCubic(Image& image, PointF p0, PointF p1, PointF p2, PointF p3, Colour c) {
    std::vector<PointF> path;
    appendCubic(path, p0, p1, p2, p3);
    drawPolylineWu(image, path, c);
}

inline std::vector<PointF> smoothPath(const std::vector<PointF>& points) {
    std::vector<PointF> path;
    int n = static_cast<int>(points.size());
    if (n < 2) {
        return points;
    }
    for (int i = 0; i + 1 < n; ++i) {
        PointF before = points[std::max(i - 1, 0)];
        PointF from = points[i];
        PointF to = points[i + 1];
        PointF after = points[std::min(i + 2, n - 1)];
        PointF handle1 = from + (to - before) / 6.0;
        PointF handle2 = to - (after - from) / 6.0;
        appendCubic(path, from, handle1, handle2, to);
    }
    return path;
}

inline std::vector<PointF> bezierCircle(PointF centre, double r) {
    const double k = 0.5522847498;
    double h = k * r;
    PointF right = centre + Vec2{r, 0.0};
    PointF bottom = centre + Vec2{0.0, r};
    PointF left = centre + Vec2{-r, 0.0};
    PointF top = centre + Vec2{0.0, -r};
    std::vector<PointF> path;
    appendCubic(path, right, right + Vec2{0.0, h}, bottom + Vec2{h, 0.0}, bottom);
    appendCubic(path, bottom, bottom + Vec2{-h, 0.0}, left + Vec2{0.0, h}, left);
    appendCubic(path, left, left + Vec2{0.0, -h}, top + Vec2{-h, 0.0}, top);
    appendCubic(path, top, top + Vec2{h, 0.0}, right + Vec2{0.0, -h}, right);
    return path;
}

#endif
