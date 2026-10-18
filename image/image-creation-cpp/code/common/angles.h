#ifndef ANGLES_H
#define ANGLES_H

#include <algorithm>
#include <cmath>
#include <vector>
#include "vec2.h"

const double kPi = 3.14159265358979323846;

inline double degreesToRadians(double degrees) {
    return degrees * kPi / 180.0;
}

inline double radiansToDegrees(double radians) {
    return radians * 180.0 / kPi;
}

inline Vec2 fromAngle(double radians) {
    return Vec2{std::cos(radians), std::sin(radians)};
}

inline PointF pointOnCircle(PointF centre, double r, double radians) {
    return centre + fromAngle(radians) * r;
}

inline PointF pointOnEllipse(PointF centre, double a, double b, double radians) {
    return PointF{centre.x + a * std::cos(radians), centre.y + b * std::sin(radians)};
}

inline double angleOf(Vec2 v) {
    return std::atan2(v.y, v.x);
}

inline double angleBetween(Vec2 a, Vec2 b) {
    double la = length(a);
    double lb = length(b);
    if (la == 0.0 || lb == 0.0) {
        return 0.0;
    }
    double c = std::clamp(dot(a, b) / (la * lb), -1.0, 1.0);
    return std::acos(c);
}

inline std::vector<PointF> regularPolygon(PointF centre, double r, int sides,
                                          double startRadians) {
    std::vector<PointF> points;
    for (int i = 0; i < sides; ++i) {
        double angle = startRadians + 2.0 * kPi * i / sides;
        points.push_back(pointOnCircle(centre, r, angle));
    }
    return points;
}

inline std::vector<PointF> starPoints(PointF centre, double outer, double inner, int tips,
                                      double startRadians) {
    std::vector<PointF> points;
    for (int i = 0; i < 2 * tips; ++i) {
        double angle = startRadians + kPi * i / tips;
        double r = (i % 2 == 0) ? outer : inner;
        points.push_back(pointOnCircle(centre, r, angle));
    }
    return points;
}

#endif
