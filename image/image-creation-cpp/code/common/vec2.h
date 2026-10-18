#ifndef VEC2_H
#define VEC2_H

#include <algorithm>
#include <cmath>
#include <vector>
#include "wu.h"

using Vec2 = PointF;

inline Vec2 operator+(Vec2 a, Vec2 b) {
    return Vec2{a.x + b.x, a.y + b.y};
}

inline Vec2 operator-(Vec2 a, Vec2 b) {
    return Vec2{a.x - b.x, a.y - b.y};
}

inline Vec2 operator-(Vec2 v) {
    return Vec2{-v.x, -v.y};
}

inline Vec2 operator*(Vec2 v, double s) {
    return Vec2{v.x * s, v.y * s};
}

inline Vec2 operator*(double s, Vec2 v) {
    return Vec2{v.x * s, v.y * s};
}

inline Vec2 operator/(Vec2 v, double s) {
    return Vec2{v.x / s, v.y / s};
}

inline double dot(Vec2 a, Vec2 b) {
    return a.x * b.x + a.y * b.y;
}

inline double cross(Vec2 a, Vec2 b) {
    return a.x * b.y - a.y * b.x;
}

inline double length(Vec2 v) {
    return std::sqrt(dot(v, v));
}

inline double distance(Vec2 a, Vec2 b) {
    return length(b - a);
}

inline Vec2 normalize(Vec2 v) {
    double len = length(v);
    if (len == 0.0) {
        return Vec2{0.0, 0.0};
    }
    return v / len;
}

inline Vec2 perpendicular(Vec2 v) {
    return Vec2{-v.y, v.x};
}

inline Vec2 project(Vec2 v, Vec2 onto) {
    double d = dot(onto, onto);
    if (d == 0.0) {
        return Vec2{0.0, 0.0};
    }
    return onto * (dot(v, onto) / d);
}

inline Vec2 reflect(Vec2 v, Vec2 normal) {
    Vec2 n = normalize(normal);
    return v - n * (2.0 * dot(v, n));
}

inline double distanceToLine(Vec2 p, Vec2 a, Vec2 b) {
    double len = length(b - a);
    if (len == 0.0) {
        return length(p - a);
    }
    return std::fabs(cross(b - a, p - a)) / len;
}

inline Vec2 closestPointOnSegment(Vec2 p, Vec2 a, Vec2 b) {
    Vec2 ab = b - a;
    double d = dot(ab, ab);
    if (d == 0.0) {
        return a;
    }
    double t = std::clamp(dot(p - a, ab) / d, 0.0, 1.0);
    return a + ab * t;
}

inline double distanceToSegment(Vec2 p, Vec2 a, Vec2 b) {
    return length(p - closestPointOnSegment(p, a, b));
}

inline double capsuleCoverage(Vec2 a, Vec2 b, double radius, int x, int y, int n) {
    int inside = 0;
    for (int j = 0; j < n; ++j) {
        for (int i = 0; i < n; ++i) {
            Vec2 s{x + sampleOffset(i, n), y + sampleOffset(j, n)};
            if (distanceToSegment(s, a, b) <= radius) {
                ++inside;
            }
        }
    }
    return static_cast<double>(inside) / (n * n);
}

inline void fillCapsuleAA(Image& image, Vec2 a, Vec2 b, double radius, Colour c, int n = 4) {
    if (radius <= 0.0 || n < 1) {
        return;
    }
    const double halfDiagonal = 0.70711;
    int x0 = static_cast<int>(std::floor(std::min(a.x, b.x) - radius));
    int y0 = static_cast<int>(std::floor(std::min(a.y, b.y) - radius));
    int x1 = static_cast<int>(std::ceil(std::max(a.x, b.x) + radius));
    int y1 = static_cast<int>(std::ceil(std::max(a.y, b.y) + radius));
    Rect box = clipToImage(Rect{x0, y0, x1, y1}, image);
    for (int y = box.y0; y < box.y1; ++y) {
        for (int x = box.x0; x < box.x1; ++x) {
            double d = distanceToSegment(Vec2{x + 0.5, y + 0.5}, a, b);
            if (d <= radius - halfDiagonal) {
                image.setPixel(x, y, c);
            } else if (d < radius + halfDiagonal) {
                paintCoverage(image, x, y, c, capsuleCoverage(a, b, radius, x, y, n));
            }
        }
    }
}

inline void drawArrowAA(Image& image, Vec2 from, Vec2 to, double thickness, Colour c) {
    Vec2 d = to - from;
    double len = length(d);
    if (len == 0.0) {
        return;
    }
    Vec2 u = d / len;
    double headLength = std::min(len, thickness * 4.0);
    Vec2 base = to - u * headLength;
    Vec2 side = perpendicular(u) * (thickness / 2.0);
    Vec2 wing = perpendicular(u) * (thickness * 2.0);
    std::vector<PointF> shaft = {from + side, base + side, base - side, from - side};
    std::vector<PointF> head = {base + wing, to, base - wing};
    fillPathsAA(image, {shaft, head}, c);
}

#endif
