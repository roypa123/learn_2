#ifndef TRANSFORM_H
#define TRANSFORM_H

#include <cmath>
#include <vector>
#include "angles.h"

inline Vec2 translate(Vec2 p, Vec2 offset) {
    return p + offset;
}

inline Vec2 scaleAbout(Vec2 p, Vec2 centre, double sx, double sy) {
    return Vec2{centre.x + sx * (p.x - centre.x), centre.y + sy * (p.y - centre.y)};
}

inline Vec2 rotate(Vec2 p, double radians) {
    double c = std::cos(radians);
    double s = std::sin(radians);
    return Vec2{p.x * c - p.y * s, p.x * s + p.y * c};
}

inline Vec2 rotateAbout(Vec2 p, Vec2 centre, double radians) {
    return centre + rotate(p - centre, radians);
}

inline std::vector<PointF> translatePoints(const std::vector<PointF>& points, Vec2 offset) {
    std::vector<PointF> result;
    for (PointF p : points) {
        result.push_back(translate(p, offset));
    }
    return result;
}

inline std::vector<PointF> scalePoints(const std::vector<PointF>& points, Vec2 centre, double sx,
                                       double sy) {
    std::vector<PointF> result;
    for (PointF p : points) {
        result.push_back(scaleAbout(p, centre, sx, sy));
    }
    return result;
}

inline std::vector<PointF> rotatePoints(const std::vector<PointF>& points, Vec2 centre,
                                        double radians) {
    std::vector<PointF> result;
    for (PointF p : points) {
        result.push_back(rotateAbout(p, centre, radians));
    }
    return result;
}

inline std::vector<PointF> tiltedEllipsePoints(PointF centre, double a, double b, double radians,
                                               int count) {
    std::vector<PointF> points;
    for (int i = 0; i < count; ++i) {
        double t = 2.0 * kPi * i / count;
        Vec2 p{a * std::cos(t), b * std::sin(t)};
        points.push_back(centre + rotate(p, radians));
    }
    return points;
}

inline bool insideTiltedEllipse(Vec2 p, PointF centre, double a, double b, double radians) {
    Vec2 q = rotate(p - centre, -radians);
    return (q.x / a) * (q.x / a) + (q.y / b) * (q.y / b) <= 1.0;
}

inline double tiltedEllipseCoverage(PointF centre, double a, double b, double radians, int x, int y,
                                    int n) {
    double c = std::cos(radians);
    double s = std::sin(radians);
    int inside = 0;
    for (int j = 0; j < n; ++j) {
        for (int i = 0; i < n; ++i) {
            double dx = x + sampleOffset(i, n) - centre.x;
            double dy = y + sampleOffset(j, n) - centre.y;
            double u = dx * c + dy * s;
            double v = -dx * s + dy * c;
            if ((u / a) * (u / a) + (v / b) * (v / b) <= 1.0) {
                ++inside;
            }
        }
    }
    return static_cast<double>(inside) / (n * n);
}

inline Rect tiltedEllipseBox(PointF centre, double a, double b, double radians) {
    double c = std::cos(radians);
    double s = std::sin(radians);
    double halfWidth = std::sqrt(a * a * c * c + b * b * s * s);
    double halfHeight = std::sqrt(a * a * s * s + b * b * c * c);
    int x0 = static_cast<int>(std::floor(centre.x - halfWidth));
    int y0 = static_cast<int>(std::floor(centre.y - halfHeight));
    int x1 = static_cast<int>(std::ceil(centre.x + halfWidth));
    int y1 = static_cast<int>(std::ceil(centre.y + halfHeight));
    return Rect{x0, y0, x1, y1};
}

inline void fillTiltedEllipseAA(Image& image, PointF centre, double a, double b, double radians,
                                Colour c, int n = 4) {
    if (a <= 0.0 || b <= 0.0 || n < 1) {
        return;
    }
    Rect box = clipToImage(tiltedEllipseBox(centre, a, b, radians), image);
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            paintCoverage(image, x, y, c, tiltedEllipseCoverage(centre, a, b, radians, x, y, n));
        }
    }
}

#endif
